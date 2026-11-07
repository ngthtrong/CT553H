from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
import torch.nn.functional as F

from .common import atomic_json, seeds
from .data import arm_mask, balanced_weights
from .features import crop_inputs
from .metrics import summarize
from .plm import feature_data


class ConvHead(nn.Module):
    def __init__(self, dimension=0, kernels=(5,), filters=96, projection=32):
        super().__init__()
        self.dimension = dimension
        self.projection = nn.Linear(dimension, projection) if dimension else None
        self.convs = nn.ModuleList([nn.Conv1d(21 + (projection if dimension else 0), filters, k, padding=k//2)
                                    for k in kernels])
        self.head = nn.Sequential(nn.Dropout(.3), nn.Linear(2*filters*len(kernels)+60, 64),
                                  nn.ReLU(), nn.Dropout(.3), nn.Linear(64, 1))

    def forward(self, indices, context, delta=None):
        valid = indices < 20
        oh = F.one_hot(indices.clamp(max=19), 20).float()*valid.unsqueeze(-1)
        center = torch.zeros((*indices.shape, 1), device=indices.device)
        center[:, indices.shape[1]//2] = 1
        blocks = [oh, center]
        if self.projection is not None:
            assert delta is not None
            if not torch.is_tensor(delta):
                delta = torch.as_tensor(np.asarray(delta), device=indices.device)
            blocks.append(F.gelu(self.projection(delta.float()))*valid.unsqueeze(-1))
        x = torch.cat(blocks, -1).transpose(1, 2)
        extracted = []
        for conv in self.convs:
            h = F.relu(conv(x))*valid.unsqueeze(1)
            extracted += [h.amax(-1), h[:, :, indices.shape[1]//2]]
        return self.head(torch.cat(extracted+[context], 1)).squeeze(-1)


def predict(model, xx, context, delta, rows, batch=512):
    model.eval(); result = []
    with torch.no_grad():
        for lo in range(0, len(rows), batch):
            r = rows[lo:lo+batch]
            result.append(model(xx[r], context[r], delta[r] if delta is not None else None).cpu().numpy())
    return np.concatenate(result)


def fit_head(factory, xx, context, delta, y, tr, va, seed, out, epochs=40,
             patience=6, lr=.001, initial=None, refit_epochs=None, weights=None):
    """Checkpoint model/optimizer each epoch, deterministic per-epoch RNG on resume."""
    seeds(seed)
    net = factory().to(xx.device)
    if initial is not None:
        net.load_state_dict(initial)
    optimizer = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=.01)
    checkpoint = Path(out)
    start, best, best_epoch, best_state = 0, float('inf'), 0, None
    if checkpoint.exists():
        state = torch.load(checkpoint, map_location=xx.device, weights_only=True)
        net.load_state_dict(state['model']); optimizer.load_state_dict(state['optimizer'])
        start, best, best_epoch, best_state = state['epoch'], state['best'], state['best_epoch'], state['best_state']
    target_epochs = refit_epochs if refit_epochs is not None else epochs
    wt = torch.as_tensor(weights if weights is not None else np.ones(len(y)), dtype=torch.float32, device=xx.device)
    for epoch in range(start+1, target_epochs+1):
        seeds(seed*100000+epoch)
        net.train()
        order = np.random.default_rng(seed*100000+epoch).permutation(tr)
        for lo in range(0, len(order), 256):
            r = order[lo:lo+256]
            loss = (torch.square(net(xx[r], context[r], delta[r] if delta is not None else None)-y[r])*wt[r]).mean()
            optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
        if refit_epochs is None:
            score = float(np.square(predict(net, xx, context, delta, va)-y[va].cpu().numpy()).mean())
        else:
            score = -float(epoch)
        if score < best-1e-6:
            best, best_epoch = score, epoch
            best_state = {k: v.detach().cpu().clone() for k, v in net.state_dict().items()}
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        torch.save(dict(model=net.state_dict(), optimizer=optimizer.state_dict(), epoch=epoch,
                        best=best, best_epoch=best_epoch, best_state=best_state), checkpoint)
        if refit_epochs is None and epoch-best_epoch >= patience:
            break
    assert best_state is not None
    net.load_state_dict(best_state)
    return net, best_epoch, best


def neural_stage(ds, out, config):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_num_threads(2)
    frame = ds.sample_smoke(ds.sat) if config['smoke'] else ds.sat.reset_index(drop=True)
    idx, f60 = crop_inputs(frame)
    xx = torch.as_tensor(idx, device=device); aux = torch.as_tensor(f60, device=device)
    y = torch.as_tensor(frame.dpsi_mean.to_numpy(), dtype=torch.float32, device=device)
    feature_paths = config.get('crop_features', {})
    sources = {'onehot': None}
    if config['smoke']:
        # Clearly synthetic feature fixture tests crop/head plumbing, never used in scientific output.
        sources['synthetic_smoke'] = np.random.default_rng(17).normal(size=(len(frame), 15, 8)).astype('float32')
    for model_id, path in feature_paths.items():
        values, _ = feature_data(path, frame, ds.identity, config['smoke'], crop=True)
        sources[model_id] = values
    if not config['smoke'] and config.get('require_esm35', True):
        assert 'esm2_35m' in sources, 'Stage05 requires the ESM35 crop feature bundle from stage03'
    summaries = []
    for source, values in sources.items():
        delta = values
        dimension = 0 if delta is None else delta.shape[-1]
        for head in config.get('heads', ['pointwise', 'cnn', 'mcnn']):
            kernels = {'pointwise': (1,), 'cnn': (5,), 'mcnn': (3, 5, 7)}[head]
            filters = 32 if head == 'mcnn' else 96
            factory = lambda: ConvHead(dimension, kernels, filters)
            for arm in config.get('neural_arms', ['B', 'D', 'E']):
                recipe = f'{source}-{head}-{arm}'
                rows_out = []
                for seed in config['seeds']:
                    pred = np.full(len(frame), np.nan)
                    folds = [0] if config['smoke'] else sorted(frame.outer_fold.unique())
                    for fold in folds:
                        role = ds.role(frame, int(fold), seed)
                        mask = arm_mask(frame, arm)
                        tr = np.flatnonzero((role == 'train') & mask)
                        va = np.flatnonzero(role == 'validation'); te = np.flatnonzero(role == 'test')
                        assert min(len(tr), len(va), len(te)) > 0
                        if config['smoke']:
                            tr, va, te = tr[:128], va[:64], te[:128]
                        weights = np.ones(len(frame))
                        if arm == 'E':
                            weights[tr] = balanced_weights(frame.iloc[tr])
                        net, epoch, vmse = fit_head(factory, xx, aux, delta, y, tr, va, seed,
                            Path(out) / f'{recipe}-{seed}-{fold}-inner.pt', epochs=config['epochs'], weights=weights)
                        calibration = frame.iloc[va][['cell_id', 'peptide_id', 'group_id', 'dpsi_mean']].copy()
                        calibration['prediction'] = predict(net, xx, aux, delta, va)
                        calibration.to_parquet(Path(out) / f'{recipe}-seed{seed}-fold{fold}-calibration.parquet', index=False)
                        final = np.flatnonzero(np.isin(role, ['train', 'validation']) & mask)
                        if config['smoke']:
                            final = final[:192]
                        if arm == 'E':
                            weights[final] = balanced_weights(frame.iloc[final])
                        net, _, _ = fit_head(factory, xx, aux, delta, y, final, va, seed,
                            Path(out) / f'{recipe}-{seed}-{fold}-refit.pt', refit_epochs=epoch, weights=weights)
                        pred[te] = predict(net, xx, aux, delta, te)
                        torch.save(dict(model_state=net.state_dict(), dimension=dimension, kernels=list(kernels),
                            filters=filters, arm=arm, seed=seed, fold=int(fold), selected_epoch=epoch,
                            data_identity=ds.identity, mode='smoke' if config['smoke'] else 'official'),
                            Path(out) / f'{recipe}-{seed}-{fold}-model.pt')
                        atomic_json(Path(out) / f'{recipe}-{seed}-{fold}-fit.json',
                            dict(epoch=epoch, validation_mse=vmse, parameters=sum(p.numel() for p in net.parameters())))
                    keep = np.isfinite(pred)
                    assert keep.all() or config['smoke']
                    result = frame.loc[keep, ['cell_id', 'peptide_id', 'group_id', 'outer_fold', 'psi_stratum', 'dpsi_mean']].copy()
                    result['prediction'] = pred[keep]; result['seed'] = seed; result['recipe'] = recipe
                    result['mode'] = 'smoke' if config['smoke'] else 'official'; result['data_identity'] = ds.identity
                    rows_out.append(result)
                result = pd.concat(rows_out)
                result.to_parquet(Path(out) / f'{recipe}-oof.parquet', index=False)
                mean = result.groupby('cell_id').prediction.mean()
                evaluated = frame[frame.cell_id.isin(mean.index)]
                report = summarize(evaluated, mean.reindex(evaluated.cell_id).to_numpy())
                atomic_json(Path(out) / f'{recipe}-results.json', report)
                summaries.append(dict(recipe=recipe, **report['all']))
                print('trained', recipe, flush=True)
    return pd.DataFrame(summaries)


def scanning_neural_stage(ds, out, config):
    """Train scanning pretext regressors, then new saturation CNNs; scan_T never read."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_num_threads(2)
    sat = ds.sample_smoke(ds.sat) if config['smoke'] else ds.sat.reset_index(drop=True)
    scan = ds.scanning()
    scan = scan[(scan.partition == 'scan_dev') & scan.dpsi_rep1.notna() & scan.dpsi_rep2.notna()].copy()
    assert not set(scan.group_id) & set(ds.sat.group_id)
    if config['smoke']:
        scan = scan.head(64)
    joined = pd.concat([sat, scan], ignore_index=True)
    idx, f60 = crop_inputs(joined)
    xx, aux = torch.as_tensor(idx, device=device), torch.as_tensor(f60, device=device)
    scan_rows = np.arange(len(sat), len(joined))
    summaries = []
    factory = lambda: ConvHead(0, (5,), 96)
    for target in (None, 'dpsi_rep1', 'dpsi_rep12_mean'):
        recipe = 'cnn-transfer-'+('scratch' if target is None else target)+'-D'
        ys = np.r_[sat.dpsi_mean.to_numpy(), scan[target].to_numpy() if target else np.zeros(len(scan))]
        y = torch.as_tensor(ys, dtype=torch.float32, device=device)
        predictions = []
        for seed in config['seeds']:
            initial = None
            if target:
                pretrained, _, _ = fit_head(factory, xx, aux, None, y, scan_rows, [], seed,
                    Path(out) / f'{recipe}-{seed}-pretrain.pt',
                    refit_epochs=config.get('scan_pretrain_epochs', 1 if config['smoke'] else 5))
                initial = {k: v.detach().cpu().clone() for k, v in pretrained.state_dict().items()}
            pred = np.full(len(sat), np.nan)
            for fold in ([0] if config['smoke'] else range(5)):
                role = ds.role(sat, fold, seed)
                tr, va, te = [np.flatnonzero(role == r) for r in ('train', 'validation', 'test')]
                if config['smoke']:
                    tr, va, te = tr[:64], va[:32], te[:64]
                net, epoch, vmse = fit_head(factory, xx, aux, None, y, tr, va, seed,
                    Path(out) / f'{recipe}-{seed}-{fold}-inner.pt', epochs=config['epochs'], initial=initial)
                cal = sat.iloc[va][['cell_id', 'peptide_id', 'group_id', 'dpsi_mean']].copy()
                cal['prediction'] = predict(net, xx, aux, None, va)
                cal.to_parquet(Path(out) / f'{recipe}-seed{seed}-fold{fold}-calibration.parquet', index=False)
                final = np.flatnonzero(np.isin(role, ['train', 'validation']))
                if config['smoke']:
                    final = final[:96]
                net, _, _ = fit_head(factory, xx, aux, None, y, final, va, seed,
                    Path(out) / f'{recipe}-{seed}-{fold}-refit.pt', refit_epochs=epoch, initial=initial)
                pred[te] = predict(net, xx, aux, None, te)
                torch.save(dict(model_state=net.state_dict(), data_identity=ds.identity, recipe=recipe,
                    pretrain_target=target, pretrain_cells=len(scan) if target else 0,
                    selected_epoch=epoch, seed=seed, fold=fold), Path(out) / f'{recipe}-{seed}-{fold}-model.pt')
                atomic_json(Path(out) / f'{recipe}-{seed}-{fold}-fit.json', dict(validation_mse=vmse,
                    selected_epoch=epoch, pretrain_groups=len(set(scan.group_id)) if target else 0))
            keep = np.isfinite(pred)
            rows = sat.loc[keep, ['cell_id', 'peptide_id', 'group_id', 'outer_fold', 'psi_stratum', 'dpsi_mean']].copy()
            rows['prediction'] = pred[keep]; rows['seed'] = seed; rows['recipe'] = recipe
            rows['data_identity'] = ds.identity; rows['mode'] = 'smoke' if config['smoke'] else 'official'
            predictions.append(rows)
        result = pd.concat(predictions)
        result.to_parquet(Path(out) / f'{recipe}-oof.parquet', index=False)
        mean = result.groupby('cell_id').prediction.mean()
        evaluated = sat[sat.cell_id.isin(mean.index)]
        report = summarize(evaluated, mean.reindex(evaluated.cell_id).to_numpy())
        atomic_json(Path(out) / f'{recipe}-results.json', report)
        summaries.append(dict(recipe=recipe, **report['all']))
    return pd.DataFrame(summaries)
