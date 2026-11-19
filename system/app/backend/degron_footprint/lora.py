"""LoRA-D effect model (plan 2.12, implementation plan WP10): ESM-2 35M with rank-8 LoRA adapters, three seeds.

Recipe of the branch-1 refit (research/lora-refit-transfer-2026-11-16, campaign aa4fc2b7ce29abf9), written again here
from its description rather than imported, so that the parity test compares two implementations (NFR-04, RG-01):

* backbone: facebook/esm2_t12_35M_UR50D at a pinned revision, float32, eval mode, no pooling layer; the 28 residue
  tokens of `last_hidden_state` (special tokens removed);
* LoRA on every attention `query` and `value` projection: y = W x + b + (alpha / r) * B (A x), r = 8, alpha = 16;
* features per substitution: delta = H(mutant) - H(wild type); [delta at the mutated position, mean of delta over the
  28 residues, wild-type one-hot (20), mutant one-hot (20), wild-type composition (20)];
* head: Linear(2*480+60, 64) -> ReLU -> Dropout (inactive) -> Linear(64, 1) = raw DeltaPSI score;
* ensemble: mean of the three seeds' raw scores, then a three-class multinomial logistic calibrator on that mean
  (fitted on ensemble out-of-fold predictions of W only); P(DeltaPSI >= 1) is the probability of class 2.

The bundle has no pickle: adapters, head and calibrator are .npz arrays, the backbone is safetensors, and every file is
checked against the SHA-256 in the manifest before anything is built (NFR-06). The manifest itself is the registered
`weights_path`/`weights_sha256` of the model row. PyTorch and Transformers are optional dependencies
(requirements-lora.txt): without them this loader reports a WeightsError and the npz model keeps serving.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
from pathlib import Path
from typing import Any

import numpy as np

from .constants import AA_INDEX, TILE_LEN, TOP_K
from .features import substitutions
from .model import LOADERS, TilePrediction, WeightsError, rank_scores, sha256_file

KIND = 'torch_lora'
MANIFEST_SCHEMA = 1
EVENT_CLASS = 2                     # classes: 0 = DeltaPSI <= -1, 1 = neutral, 2 = DeltaPSI >= 1
BATCH = 64                          # mutant sequences per forward pass (all have 28 residues: no padding)


def composition_features(seq: str, cells: list[tuple[int, str]]) -> np.ndarray:
    """(n, 60): wild-type one-hot at the position, mutant one-hot, composition of the wild-type tile."""
    n = len(cells)
    out = np.zeros((n, 60), dtype=np.float32)
    rows = np.arange(n)
    pos0 = np.fromiter((p - 1 for p, _ in cells), dtype=np.int64, count=n)
    idx = np.fromiter((AA_INDEX[c] for c in seq), dtype=np.int64, count=len(seq))
    mut = np.fromiter((AA_INDEX[a] for _, a in cells), dtype=np.int64, count=n)
    out[rows, idx[pos0]] = 1.0
    out[rows, 20 + mut] = 1.0
    comp = np.zeros(20, dtype=np.float32)
    for c in seq:                                   # same accumulation order as the research code (float32 sums)
        comp[AA_INDEX[c]] += np.float32(1.0 / len(seq))
    out[:, 40:60] = comp
    return out


def learned_state_digest(names: list[str], arrays: dict[str, np.ndarray]) -> str:
    """SHA-256 over name bytes then float32 bytes, in training order (degron_v3.local_training.model_digest)."""
    h = hashlib.sha256()
    for name in names:
        h.update(name.encode())
        h.update(np.ascontiguousarray(arrays[name], dtype=np.float32).tobytes())
    return h.hexdigest()


def merge_lora(net: Any) -> int:
    """Replace every LoRA-wrapped Linear by one Linear with W + (alpha / r) * B A (plan-system 1.4). Returns the number
    of merged layers. The result is the same function up to float rounding."""
    import torch
    from torch import nn
    merged = 0
    with torch.no_grad():
        for name, module in list(net.backbone.named_modules()):
            if hasattr(module, 'lora_A') and hasattr(module, 'original'):
                lin: nn.Linear = module.original
                lin.weight += module.scale * (module.lora_B @ module.lora_A)
                parent, _, leaf = name.rpartition('.')
                setattr(net.backbone.get_submodule(parent) if parent else net.backbone, leaf, lin)
                merged += 1
    return merged


def seed_spread(per_seed: np.ndarray) -> np.ndarray:
    """Population standard deviation (ddof = 0) over the seed axis of (n_seeds, n_cells) raw scores, in float64."""
    return np.std(np.asarray(per_seed, dtype=np.float64), axis=0, ddof=0)


def softmax_rows(z: np.ndarray) -> np.ndarray:
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


class LoraEnsembleModel:
    """ModelAdapter for the LoRA-D ensemble. Files are verified at start-up; the network is built on first use."""

    kind = KIND

    def __init__(self, model_id: str, manifest_path: Path, manifest: dict[str, Any]):
        self.model_id = model_id
        self.manifest = manifest
        self.bundle = manifest_path.parent / manifest['bundle_dir']
        self.calibrators = ('platt',)               # multinomial logistic on the raw score (Platt-style); no isotonic
        self.default_calibrator = 'platt'
        cal = np.load(self.bundle / manifest['calibrator']['file'], allow_pickle=False)
        self.cal_coef = np.asarray(cal['coef'], dtype=np.float64).reshape(-1)       # (3,)
        self.cal_intercept = np.asarray(cal['intercept'], dtype=np.float64)         # (3,)
        self.cal_classes = [int(c) for c in cal['classes']]
        if self.cal_classes != [0, 1, 2]:
            raise WeightsError('calibrator classes differ from [0, 1, 2]')
        ts = manifest.get('training_sequences')
        if ts is None:
            raise WeightsError('manifest has no training_sequences: TRAINING_PEPTIDE could not be warned for this model')
        seqs = (self.bundle / ts['file']).read_text(encoding='ascii').split()
        if len(seqs) != ts['count']:
            raise WeightsError('training sequence count differs from the manifest')
        # Tiles this model was trained on (W, 235 peptides): the API warns TRAINING_PEPTIDE from this set, not from the
        # npz model's 176 training peptides.
        self.training_sequences: frozenset[str] = frozenset(seqs)
        self._lock = threading.Lock()
        self._net: Any = None
        self.threads = int(os.environ.get('DF_LORA_THREADS', '0') or 0) or min(4, os.cpu_count() or 1)
        # plan-system 1.4: mutant sequences per forward pass, and whether the LoRA update is merged into the frozen
        # weights at load time (W + alpha/r * B A). Merging changes float rounding only; see LORA.md for the parity
        # rule (<= 1e-5 against the fixture keeps the model id).
        self.batch = int(os.environ.get('DF_LORA_BATCH', '0') or 0) or BATCH
        self.merge = os.environ.get('DF_LORA_MERGE', '0') == '1'

    # ------------------------------------------------------------------ loading
    @classmethod
    def from_file(cls, model_id: str, path: Path, expected_sha256: str | None) -> LoraEnsembleModel:
        if not path.is_file():
            raise WeightsError('weights file is missing')
        if expected_sha256 is not None and sha256_file(path) != expected_sha256:
            raise WeightsError('weights file hash differs from the registered value')
        try:
            manifest = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise WeightsError(f'manifest cannot be read: {type(exc).__name__}') from exc
        if manifest.get('schema_version') != MANIFEST_SCHEMA or manifest.get('kind') != KIND:
            raise WeightsError('manifest is not a torch_lora bundle of a known schema')
        bundle = path.parent / manifest['bundle_dir']
        for rel, meta in sorted(manifest['files'].items()):
            f = (bundle / rel).resolve()
            if not f.is_relative_to(bundle.resolve()) or not f.is_file():
                raise WeightsError(f'bundle file is missing: {rel}')
            if f.stat().st_size != meta['bytes'] or sha256_file(f) != meta['sha256']:
                raise WeightsError(f'bundle file hash differs from the manifest: {rel}')
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
        except ImportError as exc:
            raise WeightsError('PyTorch/Transformers are not installed (backend/requirements-lora.txt)') from exc
        return cls(model_id, path, manifest)

    def _build(self) -> Any:
        import torch
        from torch import nn
        from transformers import AutoModel, AutoTokenizer

        torch.set_num_threads(self.threads)
        m = self.manifest
        base = self.bundle / m['base']['dir']
        rank, alpha = int(m['adapter']['rank']), float(m['adapter']['alpha'])
        targets = tuple(m['adapter']['targets'])

        class LoRALinear(nn.Module):
            def __init__(self, original: nn.Linear):
                super().__init__()
                self.original = original
                self.scale = alpha / rank
                self.lora_A = nn.Parameter(torch.zeros(rank, original.in_features))
                self.lora_B = nn.Parameter(torch.zeros(original.out_features, rank))

            def forward(self, x):
                return self.original(x) + nn.functional.linear(nn.functional.linear(x, self.lora_A), self.lora_B) * self.scale

        class Regressor(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.backbone = AutoModel.from_pretrained(str(base), local_files_only=True, trust_remote_code=False,
                                                          dtype=torch.float32, add_pooling_layer=False)
                for name, module in list(self.backbone.named_modules()):
                    if isinstance(module, nn.Linear) and name.rsplit('.', 1)[-1] in targets:
                        parent, _, leaf = name.rpartition('.')
                        setattr(self.backbone.get_submodule(parent), leaf, LoRALinear(module))
                dim = self.backbone.config.hidden_size
                self.head = nn.Sequential(nn.Linear(2 * dim + 60, 64), nn.ReLU(), nn.Dropout(0.2), nn.Linear(64, 1))

        tokenizer = AutoTokenizer.from_pretrained(str(base), local_files_only=True, trust_remote_code=False)
        seeds = []
        for entry in m['seeds']:
            z = np.load(self.bundle / entry['file'], allow_pickle=False)
            names = [str(n) for n in z['__order__']]
            arrays = {n: z[n] for n in names}
            if learned_state_digest(names, arrays) != entry['learned_state_sha256']:
                raise WeightsError(f'adapter of seed {entry["seed"]} differs from the refit learned state')
            net = Regressor()
            params = dict(net.named_parameters())
            if set(names) != {n for n in params if 'lora_' in n or n.startswith('head.')}:
                raise WeightsError('adapter parameter names do not match the network')
            with torch.no_grad():
                for n in names:
                    if tuple(params[n].shape) != arrays[n].shape:
                        raise WeightsError(f'shape of {n} differs')
                    params[n].copy_(torch.from_numpy(np.ascontiguousarray(arrays[n], dtype=np.float32)))
            net.eval().requires_grad_(False)
            if self.merge:
                merge_lora(net)
            seeds.append(net)
        return tokenizer, seeds

    def _ensure(self) -> Any:
        with self._lock:
            if self._net is None:
                self._net = self._build()
            return self._net

    # ------------------------------------------------------------------ scoring
    def _hidden(self, tokenizer: Any, net: Any, sequences: list[str]) -> Any:
        import torch
        enc = tokenizer(sequences, return_tensors='pt', padding=True, return_special_tokens_mask=True, truncation=False)
        special = enc.pop('special_tokens_mask').bool()
        mask = enc['attention_mask'].bool() & ~special
        if not bool(torch.all(mask.sum(1) == TILE_LEN)):
            raise ValueError('tokenizer did not return 28 residue tokens')
        hidden = net.backbone(**enc).last_hidden_state
        out = hidden[mask].reshape(len(sequences), TILE_LEN, -1)
        if not bool(out.isfinite().all()):
            raise ValueError('non-finite hidden states')
        return out

    def raw_scores(self, seq: str) -> tuple[np.ndarray, list[tuple[int, str]]]:
        """(n_seeds, 532) raw scores and the substitution list (same order as the npz model)."""
        import torch
        if len(seq) != TILE_LEN:
            raise ValueError(f'tile must have {TILE_LEN} residues')
        tokenizer, nets = self._ensure()
        cells = substitutions(seq)
        mutants = [seq[:p - 1] + a + seq[p:] for p, a in cells]
        pos0 = torch.as_tensor([p - 1 for p, _ in cells])
        aux = torch.from_numpy(composition_features(seq, cells))
        out = np.empty((len(nets), len(cells)), dtype=np.float64)
        with torch.inference_mode():
            for k, net in enumerate(nets):
                wt = self._hidden(tokenizer, net, [seq])
                for lo in range(0, len(cells), self.batch):
                    hi = min(lo + self.batch, len(cells))
                    mut = self._hidden(tokenizer, net, mutants[lo:hi])
                    delta = mut - wt
                    rows = torch.arange(hi - lo)
                    pooled = torch.cat([delta[rows, pos0[lo:hi]], delta.mean(1)], 1)
                    y = net.head(torch.cat([pooled.float(), aux[lo:hi]], 1)).squeeze(-1)
                    out[k, lo:hi] = y.double().numpy()
        return out, cells

    def calibrate(self, score: np.ndarray, which: str | None = None) -> np.ndarray:
        which = which or self.default_calibrator
        if which != 'platt':
            raise ValueError(which)
        z = np.outer(score, self.cal_coef) + self.cal_intercept
        return softmax_rows(z)[:, EVENT_CLASS]

    def predict_tile(self, seq: str, calibrator: str | None = None) -> TilePrediction:
        per_seed, cells = self.raw_scores(seq)
        score = per_seed.astype(np.float32).mean(axis=0, dtype=np.float32).astype(np.float64)
        prob = self.calibrate(score, calibrator)
        rank = rank_scores(score)
        seeds = per_seed.astype(np.float64)                # the float32 network outputs, exactly (plan-system 1.3)
        return TilePrediction(
            positions=np.fromiter((p for p, _ in cells), dtype=np.int64, count=len(cells)),
            wt=[seq[p - 1] for p, _ in cells], mut=[a for _, a in cells],
            score=score, prob=prob, rank=rank, top10=rank <= TOP_K,
            seed_sd=seed_spread(seeds), seed_min=seeds.min(axis=0), seed_max=seeds.max(axis=0))


LOADERS[KIND] = LoraEnsembleModel.from_file        # type: ignore[assignment]

__all__ = ['LoraEnsembleModel', 'KIND', 'composition_features', 'learned_state_digest', 'merge_lora', 'seed_spread',
           'softmax_rows']
