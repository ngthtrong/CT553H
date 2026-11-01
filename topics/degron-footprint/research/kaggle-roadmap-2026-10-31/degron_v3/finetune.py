"""Train new pLM mutation-effect models: matched frozen head / LoRA / full tuning.

LoRA uses the standard W x + alpha/r B A x construction, implemented in torch;
it does not need a second library to execute remote code.
"""
from pathlib import Path
import json
import math

import numpy as np
import pandas as pd
import torch
from torch import nn
import torch.nn.functional as F

from .common import seeds, atomic_json
from .data import arm_mask, balanced_weights
from .features import features
from .metrics import summarize
from .plm import Encoder


class LoRALinear(nn.Module):
    def __init__(self, original, rank=8, alpha=16):
        super().__init__()
        self.original = original.requires_grad_(False)
        self.rank, self.scale = rank, alpha/rank
        self.lora_A = nn.Parameter(torch.empty(rank, original.in_features, device=original.weight.device,
                                              dtype=original.weight.dtype))
        self.lora_B = nn.Parameter(torch.zeros(original.out_features, rank, device=original.weight.device,
                                               dtype=original.weight.dtype))
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))

    def forward(self, x):
        return self.original(x) + F.linear(F.linear(x, self.lora_A), self.lora_B)*self.scale


def inject_lora(model, rank=8, alpha=16):
    chosen = []
    for name, module in list(model.named_modules()):
        if isinstance(module, nn.Linear) and name.rsplit('.', 1)[-1] in ('query', 'value', 'q_proj', 'v_proj', 'q', 'v'):
            parent_name, _, leaf = name.rpartition('.')
            parent = model.get_submodule(parent_name) if parent_name else model
            setattr(parent, leaf, LoRALinear(module, rank, alpha)); chosen.append(name)
    assert chosen, 'No compatible attention projections found; adapter architecture must be reviewed'
    return chosen


class MutationRegressor(nn.Module):
    def __init__(self, encoder, mode='lora', seed=17, rank=8):
        super().__init__()
        self.encoder = encoder
        self.backbone = encoder.model
        self.targets = []
        seeds(seed)
        if mode == 'lora':
            self.targets = inject_lora(self.backbone, rank)
        elif mode == 'full':
            self.backbone.requires_grad_(True)
        else:
            assert mode == 'frozen'
        with torch.no_grad():
            dimension = encoder.tensor(['ACDEFGHIKLMNPQRSTVWYACDEFGHIKL'[:28]]).shape[-1]
        seeds(seed)  # matched head initialization for frozen versus LoRA
        self.head = nn.Sequential(nn.Linear(2*dimension+60, 64), nn.ReLU(), nn.Dropout(.2), nn.Linear(64, 1)).to(encoder.device)
        self.mode = mode

    def forward(self, frame):
        self.backbone.eval()  # same backbone dropout policy across matched branches
        wt = self.encoder.tensor(frame.wt_sequence.tolist())
        mut = self.encoder.tensor(frame.mutant_sequence.tolist())
        delta = mut-wt
        position = torch.as_tensor(frame.position_1based.to_numpy()-1, device=wt.device)
        pooled = torch.cat([delta[torch.arange(len(frame), device=wt.device), position], delta.mean(1)], 1)
        aux = torch.as_tensor(features(frame, 'composition'), device=wt.device)
        return self.head(torch.cat([pooled.float(), aux], 1)).squeeze(-1)

    def learned_state(self):
        return {name: value.detach().cpu().clone() for name, value in self.named_parameters() if value.requires_grad}

    def restore(self, state):
        parameters = dict(self.named_parameters())
        assert set(state) == {k for k, p in parameters.items() if p.requires_grad}
        with torch.no_grad():
            for name, value in state.items():
                parameters[name].copy_(value.to(parameters[name].device))


def infer(model, frame, batch=8):
    model.eval(); result = []
    with torch.no_grad():
        for start in range(0, len(frame), batch):
            result.append(model(frame.iloc[start:start+batch]).cpu().numpy())
    return np.concatenate(result)


def fit(model, train, validation, seed, path, epochs=20, batch=8, lr=.0001, refit=False, balanced=False):
    parameters = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=lr, weight_decay=.01)
    start, best, best_epoch, best_state = 0, float('inf'), 0, None
    path = Path(path)
    if path.exists():
        saved = torch.load(path, map_location='cpu', weights_only=True)
        model.restore(saved['learned_state']); optimizer.load_state_dict(saved['optimizer'])
        start, best, best_epoch, best_state = saved['epoch'], saved['best'], saved['best_epoch'], saved['best_state']
    w = balanced_weights(train) if balanced else np.ones(len(train))
    for epoch in range(start+1, epochs+1):
        seeds(seed*100000+epoch); model.train()
        order = np.random.default_rng(seed*100000+epoch).permutation(len(train))
        for lo in range(0, len(order), batch):
            rows = order[lo:lo+batch]; sub = train.iloc[rows]
            target = torch.as_tensor(sub.dpsi_mean.to_numpy(), dtype=torch.float32, device=model.encoder.device)
            weight = torch.as_tensor(w[rows], dtype=torch.float32, device=model.encoder.device)
            loss = ((model(sub)-target)**2*weight).mean()
            assert torch.isfinite(loss)
            optimizer.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(parameters, 1.); optimizer.step()
        vmse = -float(epoch) if refit else float(np.mean((infer(model, validation, batch)-validation.dpsi_mean.to_numpy())**2))
        if vmse < best-1e-6:
            best, best_epoch, best_state = vmse, epoch, model.learned_state()
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(dict(learned_state=model.learned_state(), optimizer=optimizer.state_dict(),
                        epoch=epoch, best=best, best_epoch=best_epoch, best_state=best_state), path)
        print('pLM fit', epoch, 'validation_mse', vmse, flush=True)
        if not refit and epoch-best_epoch >= 4:
            break
    assert best_state is not None
    model.restore(best_state)
    return best_epoch, best


def finetune_stage(ds, out, config):
    torch.set_num_threads(2)
    model_id = config.get('finetune_model', 'esm2_35m')
    if config['smoke']:
        model_id = 'esm2_8m'
    modes = config.get('finetune_modes', ['frozen', 'lora'])
    if 'full' in modes:
        assert model_id in ('esm2_8m', 'esm2_35m'), 'Full tuning larger pLM requires a separate resource-locked protocol'
    frame = ds.sample_smoke(ds.sat) if config['smoke'] else ds.sat.copy()
    out = Path(out); summaries = []
    for mode in modes:
        for arm in config.get('finetune_arms', ['B', 'D']):
            recipe = f'{model_id}-{mode}-{arm}'; results = []
            for seed in config['seeds']:
                predicted = np.full(len(frame), np.nan)
                for fold in ([0] if config['smoke'] else range(5)):
                    role = ds.role(frame, fold, seed); keep = arm_mask(frame, arm)
                    tr = frame.loc[(role == 'train') & keep].copy()
                    va = frame.loc[role == 'validation'].copy()
                    test_indices = np.flatnonzero(role == 'test')
                    if config['smoke']:
                        tr, va, test_indices = tr.head(8), va.head(4), test_indices[:4]
                    assert min(len(tr), len(va), len(test_indices)) > 0
                    encoder = Encoder(model_id, config['weight_roots'],
                                      'cuda' if torch.cuda.is_available() else 'cpu', 'float32')
                    model = MutationRegressor(encoder, mode, seed)
                    initial = model.learned_state()
                    epoch, vmse = fit(model, tr, va, seed, out / f'{recipe}-{seed}-{fold}-inner.pt',
                        epochs=config.get('finetune_epochs', 20), batch=config.get('finetune_batch', 8), balanced=arm == 'E')
                    calibration = va[['cell_id', 'peptide_id', 'group_id', 'dpsi_mean']].copy()
                    calibration['prediction'] = infer(model, va, config.get('finetune_batch', 8))
                    calibration.to_parquet(out / f'{recipe}-seed{seed}-fold{fold}-calibration.parquet', index=False)
                    final = frame.loc[np.isin(role, ['train', 'validation']) & keep].copy()
                    if config['smoke']:
                        final = final.head(8)
                    model.restore(initial)
                    fit(model, final, va, seed, out / f'{recipe}-{seed}-{fold}-refit.pt', epochs=epoch,
                        batch=config.get('finetune_batch', 8), refit=True, balanced=arm == 'E')
                    learned = model.learned_state()
                    changed = [name for name in learned if not torch.equal(learned[name], initial[name])]
                    assert changed, 'No new parameters learned'
                    if mode == 'lora':
                        assert any('lora_' in name for name in changed), 'LoRA weights did not update'
                    predicted[test_indices] = infer(model, frame.iloc[test_indices], config.get('finetune_batch', 8))
                    torch.save(dict(learned_state=learned, model_id=model_id, mode=mode, arm=arm,
                        seed=seed, fold=fold, data_identity=ds.identity, base_revision=encoder.lock['revision'],
                        lora_targets=model.targets, selected_epoch=epoch, training_mode='smoke' if config['smoke'] else 'official'),
                        out / f'{recipe}-{seed}-{fold}-model.pt')
                    atomic_json(out / f'{recipe}-{seed}-{fold}-fit.json', dict(selected_epoch=epoch,
                        validation_mse=vmse, trainable_parameters=sum(p.numel() for p in model.parameters() if p.requires_grad),
                        changed_parameters=changed, base_revision=encoder.lock['revision']))
                    del model, encoder
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                valid = np.isfinite(predicted); assert valid.all() or config['smoke']
                rows = frame.loc[valid, ['cell_id', 'peptide_id', 'group_id', 'outer_fold', 'psi_stratum', 'dpsi_mean']].copy()
                rows['prediction'] = predicted[valid]; rows['seed'] = seed; rows['recipe'] = recipe
                rows['mode'] = 'smoke' if config['smoke'] else 'official'; rows['data_identity'] = ds.identity
                results.append(rows)
            result = pd.concat(results)
            result.to_parquet(out / f'{recipe}-oof.parquet', index=False)
            mean = result.groupby('cell_id').prediction.mean()
            evaluated = frame[frame.cell_id.isin(mean.index)]
            report = summarize(evaluated, mean.reindex(evaluated.cell_id).to_numpy())
            atomic_json(out / f'{recipe}-results.json', report)
            summaries.append(dict(recipe=recipe, **report['all']))
    return pd.DataFrame(summaries)
