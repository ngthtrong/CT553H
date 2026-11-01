"""Pinned, local-only pLM adapters; no trust_remote_code or hosted inference."""
import gc
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import pandas as pd

from .common import atomic_json, sha256


def registry():
    return json.loads((Path(__file__).resolve().parents[1] / 'model-registry.json').read_text())


def specification(model_id):
    return next(m for m in registry()['models'] if m['id'] == model_id)


def resolve_snapshot(model_id, roots):
    for root in map(Path, roots):
        if not root.exists():
            continue
        candidates = [root / model_id / 'status.json']
        candidates += list(root.glob(f'*/{model_id}/status.json'))
        candidates += list(root.glob(f'*/*/{model_id}/status.json'))
        candidates += list(root.rglob(f'{model_id}/status.json'))
        if (root / 'status.json').is_file():
            candidates.append(root / 'status.json')
        for status in candidates:
            if not status.is_file():
                continue
            d = json.loads(status.read_text())
            if d.get('model_id') != model_id or d.get('status') != 'complete':
                continue
            snapshot = status.parent / d['revision']
            assert snapshot.is_dir(), 'Weight status exists but snapshot is missing'
            for f in d['files']:
                p = snapshot / f['path']
                assert p.is_file() and p.stat().st_size == f['bytes'], p
                # Full weight hashes verified by downloader; preflight checks them again.
            return snapshot, d
    raise FileNotFoundError(f'No COMPLETE pinned local weights for {model_id}; attach that model asset and its status.json')


class Encoder:
    def __init__(self, model_id, roots, device='cuda', dtype='float16', trainable=False):
        import torch
        from transformers import AutoTokenizer, AutoModel, T5EncoderModel
        self.spec = specification(model_id)
        self.path, self.lock = resolve_snapshot(model_id, roots)
        self.device = torch.device(device)
        self.dtype = getattr(torch, dtype)
        self.tokenizer = AutoTokenizer.from_pretrained(str(self.path), local_files_only=True,
                                                        trust_remote_code=False)
        factory = T5EncoderModel if self.spec['family'] in ('prott5', 'ankh') else AutoModel
        kwargs = {'add_pooling_layer': False} if self.spec['family'] in ('esm2', 'esm1b', 'esm1v', 'saprot') else {}
        self.model = factory.from_pretrained(str(self.path), local_files_only=True,
                    trust_remote_code=False, dtype=self.dtype, **kwargs).to(self.device).eval()
        self.model.requires_grad_(trainable)
        self.model_id = model_id

    def encode_input(self, sequences):
        import torch
        if self.spec['family'] in ('prott5', 'ankh'):
            texts = [' '.join(s) for s in sequences]
        else:
            texts = list(sequences)
        encoded = self.tokenizer(texts, return_tensors='pt', padding=True,
                                 return_special_tokens_mask=True, truncation=False)
        special = encoded.pop('special_tokens_mask').bool()
        mask = encoded['attention_mask'].bool() & ~special
        assert torch.all(mask.sum(1) == 28), 'Tokenizer must return exactly 28 residue tokens'
        encoded = {k: v.to(self.device) for k, v in encoded.items()}
        return encoded, mask.to(self.device)

    def tensor(self, sequences):
        inputs, mask = self.encode_input(sequences)
        hidden = self.model(**inputs).last_hidden_state
        # Padding/special-token placement differs among ESM/T5/Ankh.
        result = hidden[mask].reshape(len(sequences), 28, -1)
        assert result.isfinite().all(), 'Nonfinite pLM hidden states'
        return result

    def __call__(self, sequences):
        import torch
        with torch.inference_mode():
            return self.tensor(sequences).float().cpu().numpy()


def preflight(model_ids, roots, out, smoke=False):
    import torch
    probe = ['ACDEFGHIKLMNPQRSTVWYACDEFGHIKL'[:28], 'VCDEFGHIKLMNPQRSTVWYACDEFGHIKL'[:28]]
    reports = []
    for model_id in model_ids:
        report = dict(model_id=model_id, status='checking', mode='smoke' if smoke else 'official')
        encoder = None
        try:
            snapshot, lock = resolve_snapshot(model_id, roots)
            for f in lock['files']:
                assert sha256(snapshot / f['path']) == f['sha256'], f['path']
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            dtype = 'float16' if device == 'cuda' else 'float32'
            bytes_weight = sum(f['bytes'] for f in lock['files'] if f['path'].endswith(('.bin', '.safetensors')))
            if device == 'cpu' and bytes_weight > (1 << 30):
                raise MemoryError('Large-model CPU preflight is disabled; use GPU Kaggle runtime')
            if device == 'cuda':
                # Downloaded files can be fp32; this is a conservative load headroom check.
                capacity = torch.cuda.get_device_properties(0).total_memory
                if bytes_weight / 2 + (2 << 30) > capacity:
                    raise MemoryError('Needs explicit model sharding/offload; automatic precision/quantization substitution forbidden')
                torch.cuda.reset_peak_memory_stats()
            encoder = Encoder(model_id, roots, device, dtype)
            inputs = [''.join(a+'#' for a in s) for s in probe] if encoder.spec['family'] == 'saprot' else probe
            encoder(inputs[:1])
            start = time.monotonic(); h = encoder(inputs)
            seconds = time.monotonic()-start
            again = encoder(inputs)
            token_checks = []
            base_tokens, base_mask = encoder.encode_input(inputs[:1])
            for position in (1, 2, 14, 27, 28):
                p = position-1
                seq = probe[0]; aa = 'V' if seq[p] != 'V' else 'A'
                mutant = seq[:p]+aa+seq[p+1:]
                text = ''.join(a+'#' for a in mutant) if encoder.spec['family'] == 'saprot' else mutant
                encoded, mask = encoder.encode_input([text])
                changed = (base_tokens['input_ids'][base_mask] != encoded['input_ids'][mask]).nonzero().flatten().tolist()
                assert changed == [p], f'Token/substitution alignment failed at {position}: {changed}'
                token_checks.append(position)
            report.update(status='feasible', revision=lock['revision'], repo=lock['repo'],
                hidden_size=h.shape[2], shape=list(h.shape), device=device, dtype=dtype,
                batch=2, sequences_per_second=2/seconds,
                repeat_max_abs=float(np.max(np.abs(h-again))),
                peak_vram_bytes=torch.cuda.max_memory_allocated() if device == 'cuda' else 0,
                residue_alignment_positions=token_checks, wt_identity_max_abs=float(np.max(np.abs(h-again))),
                parameters=sum(p.numel() for p in encoder.model.parameters()))
            assert np.allclose(h, again, atol=.01, rtol=.005), 'Unstable repeatability'
            atomic_json(Path(out) / f'{model_id}-lock.json', dict(**report, weights=lock['files']))
        except (FileNotFoundError, MemoryError, ImportError, ValueError, RuntimeError, AssertionError) as e:
            report.update(status='blocked', reason=f'{type(e).__name__}: {e}')
        finally:
            if encoder is not None:
                del encoder
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        reports.append(report)
        atomic_json(Path(out) / 'preflight.json', dict(models=reports))
        print(model_id, report['status'], flush=True)
    return pd.DataFrame(reports)


def prefix_hash(array, n):
    h = hashlib.sha256()
    for i in range(0, n, 256):
        h.update(np.ascontiguousarray(array[i:min(n, i+256)]).tobytes())
    return h.hexdigest()


def extract(ds, model_id, roots, out, config, frame_override=None):
    import torch
    scope = config.get('row_scope', 'sat')
    frame = ds.sat if scope == 'sat' else ds.scanning(include_held=scope == 'scan_T')
    if scope != 'sat':
        frame = frame[frame.partition == scope].copy()
    if scope == 'scan_T':
        lock = json.loads(Path(config['selection_lock']).read_text())
        assert lock['data_identity'] == ds.identity and model_id in lock['model_ids']
    if frame_override is not None:
        assert scope == 'sat' and model_id.startswith('saprot_')
        frame = frame_override.copy()
    if config['smoke']:
        frame = frame.head(12).copy()
    start = config.get('row_start', 0); stop = config.get('row_stop')
    frame = frame.iloc[start:stop].reset_index(drop=True)
    assert len(frame)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if not config['smoke']:
        preflight_path = config.get('preflight_report')
        assert preflight_path, 'Set preflight_report to stage02/preflight.json from this runtime before official extraction'
        report = json.loads(Path(preflight_path).read_text())
        checks = [m for m in report['models'] if m['model_id'] == model_id and m['status'] == 'feasible']
        assert len(checks) == 1, 'Model must pass tokenizer/resource/forward preflight; do not bypass blocked models'
        _, pinned = resolve_snapshot(model_id, roots)
        assert checks[0]['revision'] == pinned['revision'] and checks[0]['device'] == device
    encoder = Encoder(model_id, roots, device, 'float16' if device == 'cuda' else 'float32')
    h = encoder([frame.wt_sequence.iloc[0]])
    dim = h.shape[2]; n = len(frame); out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    identity = dict(data_identity=ds.identity, model_id=model_id, revision=encoder.lock['revision'],
        row_scope=scope, row_ids_sha256=hashlib.sha256('\n'.join(frame.cell_id).encode()).hexdigest(),
        mode='smoke' if config['smoke'] else 'official', dtype=str(encoder.dtype),
        feature_kind='delta_site_and_mean', hidden_size=dim, rows=n, crop=bool(config.get('crop', False)))
    identity['sequence_inputs_sha256'] = hashlib.sha256('\n'.join(frame.wt_sequence+'|'+frame.mutant_sequence).encode()).hexdigest()
    metadata_path = out / 'feature-manifest.json'
    progress_path = out / 'progress.json'
    mode = 'r+' if (out / 'pool.npy').exists() else 'w+'
    if mode == 'r+':
        old = json.loads(progress_path.read_text())
        assert old['identity'] == identity, 'Changed extraction config/data: use a new output directory'
    pooled = np.lib.format.open_memmap(out / 'pool.npy', mode=mode, dtype='float16', shape=(n, 2*dim))
    crop = np.lib.format.open_memmap(out / 'crop.npy', mode=mode, dtype='float16', shape=(n, 15, dim)) if identity['crop'] else None
    completed = json.loads(progress_path.read_text())['completed'] if mode == 'r+' else 0
    if completed:
        assert prefix_hash(pooled, completed) == old['prefix_sha256'], 'Corrupt feature prefix'
    frame[['cell_id', 'peptide_id']].to_parquet(out / 'rows.parquet', index=False)
    wt_cache = {}
    batch = config.get('batch_size', 8 if device == 'cuda' else 2)
    for i in range(completed, n, batch):
        rows = frame.iloc[i:i+batch]
        missing = [s for s in dict.fromkeys(rows.wt_sequence) if s not in wt_cache]
        if missing:
            for seq, hidden in zip(missing, encoder(missing)):
                wt_cache[seq] = hidden
        mutated = encoder(rows.mutant_sequence.tolist())
        delta = mutated-np.stack([wt_cache[s] for s in rows.wt_sequence])
        positions = rows.position_1based.to_numpy(int)-1
        values = np.concatenate([delta[np.arange(len(rows)), positions], delta.mean(1)], axis=1)
        assert np.isfinite(values).all()
        pooled[i:i+len(rows)] = values
        if crop is not None:
            for j, p in enumerate(positions):
                for k, offset in enumerate(range(-7, 8)):
                    crop[i+j, k] = delta[j, p+offset] if 0 <= p+offset < 28 else 0
            crop.flush()
        pooled.flush()
        # Record complete batches atomically. The prefix hash is finalized/checkpointed every ~512 rows.
        if (i // batch) % max(1, 512//batch) == 0 or i+len(rows) == n:
            atomic_json(progress_path, dict(identity=identity, completed=i+len(rows),
                                             prefix_sha256=prefix_hash(pooled, i+len(rows))))
            print('extracted', i+len(rows), '/', n, flush=True)
    identity.update(status='complete', files=[dict(path=p.name, sha256=sha256(p))
        for p in (out/'pool.npy', out/'rows.parquet')], crop_file='crop.npy' if crop is not None else None)
    if crop is not None:
        identity['files'].append(dict(path='crop.npy', sha256=sha256(out/'crop.npy')))
    atomic_json(metadata_path, identity)
    return identity


def merge_shards(paths, out):
    """Validate disjoint shards and stream into one feature bundle, without full RAM loading."""
    paths, out = [Path(p) for p in paths], Path(out)
    assert paths and not out.exists(), 'Merge into a new output directory'
    metas = [json.loads((p/'feature-manifest.json').read_text()) for p in paths]
    keys = ['data_identity', 'model_id', 'revision', 'row_scope', 'mode', 'dtype', 'feature_kind', 'hidden_size', 'crop']
    for p, m in zip(paths, metas):
        assert m['status'] == 'complete' and all(m[k] == metas[0][k] for k in keys)
        for f in m['files']:
            assert sha256(p/f['path']) == f['sha256']
    rows = pd.concat([pd.read_parquet(p/'rows.parquet') for p in paths], ignore_index=True)
    assert not rows.cell_id.duplicated().any(), 'Overlapping shard rows'
    out.mkdir(parents=True)
    for kind in ['pool.npy']+(['crop.npy'] if metas[0]['crop'] else []):
        example = np.load(paths[0]/kind, mmap_mode='r')
        target = np.lib.format.open_memmap(out/kind, mode='w+', dtype=example.dtype, shape=(len(rows),)+example.shape[1:])
        offset = 0
        for p in paths:
            source = np.load(p/kind, mmap_mode='r')
            for i in range(0, len(source), 256):
                chunk = source[i:i+256]
                target[offset+i:offset+i+len(chunk)] = chunk
            offset += len(source)
        target.flush()
    rows.to_parquet(out/'rows.parquet', index=False)
    meta = {k: metas[0][k] for k in keys}
    meta.update(status='complete', rows=len(rows), shard_manifest_sha256=[sha256(p/'feature-manifest.json') for p in paths],
        row_ids_sha256=hashlib.sha256('\n'.join(rows.cell_id).encode()).hexdigest(),
        crop_file='crop.npy' if metas[0]['crop'] else None,
        files=[dict(path=p.name, sha256=sha256(p)) for p in sorted(out.iterdir())])
    atomic_json(out/'feature-manifest.json', meta)
    return meta


def feature_data(path, frame, data_identity, allow_smoke=False, crop=False):
    path = Path(path)
    meta = json.loads((path / 'feature-manifest.json').read_text())
    assert meta['status'] == 'complete' and meta['data_identity'] == data_identity
    assert allow_smoke or meta['mode'] == 'official', 'Smoke features cannot enter official training'
    for f in meta['files']:
        assert sha256(path / f['path']) == f['sha256'], f['path']
    rows = pd.read_parquet(path / 'rows.parquet')
    indices = rows.reset_index().set_index('cell_id')['index'].reindex(frame.cell_id)
    assert indices.notna().all(), 'Feature bundle does not cover requested rows; merge shards first'
    kind = 'crop.npy' if crop else 'pool.npy'
    array = np.load(path / kind, mmap_mode='r')
    if crop:
        return IndexedArray(array, indices.to_numpy(int)), meta
    return np.asarray(array[indices.to_numpy(int)], dtype=np.float32), meta


class IndexedArray:
    """Keep a crop memmap on CPU; read only the minibatch requested by the head."""
    def __init__(self, array, index):
        self.array, self.index = array, index
        self.shape = (len(index),) + array.shape[1:]

    def __getitem__(self, rows):
        return self.array[self.index[rows]]
