"""The stage11 math with minibatch resume, including RNG and validation progress."""
from pathlib import Path
import hashlib
import json
import time

import numpy as np
import torch

from .common import atomic_json, seeds
from .data import balanced_weights
from .local_control import atomic_torch, load_torch, fingerprint, rng_state, restore_rng


def model_digest(model):
    h = hashlib.sha256()
    for name, value in model.learned_state().items():
        h.update(name.encode()); h.update(value.numpy().tobytes())
    return h.hexdigest()


def predict(model, frame, path, control, batch=8):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    identity = fingerprint(dict(model=model_digest(model),
        cells=frame.cell_id.tolist(), batch=batch, campaign=control.campaign.name))
    progress = path.with_suffix('.json')
    done = 0
    if path.exists() and progress.exists():
        saved = json.loads(progress.read_text())
        if saved['identity'] != identity:
            raise ValueError('Prediction checkpoint has different model/input identity')
        done = saved['completed']
        values = np.load(path, mmap_mode='r+')
        assert values.shape == (len(frame),)
        assert hashlib.sha256(values[:done].tobytes()).hexdigest() == saved['prefix_sha256']
    else:
        values = np.lib.format.open_memmap(path, mode='w+', dtype='float32', shape=(len(frame),))
    model.eval()
    with torch.no_grad():
        for start in range(done, len(frame), batch):
            values[start:start+batch] = model(frame.iloc[start:start+batch]).detach().cpu().numpy()
            end = min(start+batch, len(frame))
            assert np.isfinite(values[start:end]).all()
            if end % 256 == 0 or end == len(frame) or control.stopping():
                values.flush()
                atomic_json(progress, dict(identity=identity, completed=end,
                    prefix_sha256=hashlib.sha256(values[:end].tobytes()).hexdigest()))
            control.log(f'predict {end}/{len(frame)}', rows=end, total_rows=len(frame))
            control.check()
    return np.asarray(values).copy()


def fit(model, train, validation, seed, path, control, epochs=20, batch=8,
        lr=.0001, refit=False, balanced=False):
    path = Path(path)
    identity = fingerprint(dict(job=control.job, campaign=control.campaign.name,
        train=train.cell_id.tolist(), validation=validation.cell_id.tolist(),
        seed=seed, epochs=epochs, batch=batch, lr=lr, refit=refit, balanced=balanced))
    parameters = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=lr, weight_decay=.01)
    state = load_torch(path, identity)
    if state:
        model.restore(state['learned_state']); optimizer.load_state_dict(state['optimizer'])
        if state['finished']:
            model.restore(state['best_state'])
            return state['best_epoch'], state['best']
        restore_rng(state['rng'])
        epoch, cursor, evaluated = state['epoch'], state['cursor'], state['evaluated']
        best, best_epoch, best_state = state['best'], state['best_epoch'], state['best_state']
        control.log(f'RESUME {path.name} epoch={epoch} row={cursor}/{len(train)}', force=True)
    else:
        epoch, cursor, evaluated = 1, 0, False
        best, best_epoch, best_state = float('inf'), 0, None
    weights = balanced_weights(train) if balanced else np.ones(len(train))
    device = next(model.parameters()).device

    def save(finished=False):
        atomic_torch(path, dict(schema_version=2, identity=identity,
            learned_state=model.learned_state(), optimizer=optimizer.state_dict(),
            epoch=epoch, cursor=cursor, evaluated=evaluated, finished=finished,
            best=best, best_epoch=best_epoch, best_state=best_state, rng=rng_state()))
        control.committed(f'{path.name} epoch={epoch} row={cursor}/{len(train)}')

    while epoch <= epochs:
        if evaluated:
            epoch += 1; cursor = 0; evaluated = False
            continue
        if cursor == 0:
            seeds(seed*100000+epoch)
        order = np.random.default_rng(seed*100000+epoch).permutation(len(train))
        model.train()
        started = time.monotonic()
        for start in range(cursor, len(order), batch):
            rows = order[start:start+batch]
            target = torch.as_tensor(train.iloc[rows].dpsi_mean.to_numpy(), dtype=torch.float32, device=device)
            weight = torch.as_tensor(weights[rows], dtype=torch.float32, device=device)
            loss = ((model(train.iloc[rows])-target)**2*weight).mean()
            assert torch.isfinite(loss), 'Nonfinite loss'
            optimizer.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(parameters, 1.); optimizer.step()
            cursor = min(start+batch, len(order)); control.steps += 1
            control.log(f'{path.stem} epoch={epoch}/{epochs} batch={(cursor+batch-1)//batch}/{(len(order)+batch-1)//batch} loss={loss.item():.6f}',
                        epoch=epoch, cursor=cursor, total_rows=len(order), loss=loss.item())
            if control.due():
                save()
            control.check()
        # Commit the trained epoch before a possibly interrupted validation pass.
        save()
        vmse = -float(epoch) if refit else float(np.mean((predict(model, validation,
            path.parent / f'{path.stem}-validation-{epoch}.npy', control, batch)-validation.dpsi_mean.to_numpy())**2))
        if vmse < best-1e-6:
            best, best_epoch, best_state = vmse, epoch, model.learned_state()
        evaluated = True
        finished = epoch == epochs or (not refit and epoch-best_epoch >= 4)
        save(finished)
        control.log(f'EPOCH DONE epoch={epoch} validation_mse={vmse:.8f} best_epoch={best_epoch} seconds={time.monotonic()-started:.1f}', force=True)
        control.check()
        if finished:
            break
    assert best_state is not None
    model.restore(best_state)
    return best_epoch, best
