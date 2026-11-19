# Optional LoRA-D model (plan 2.12, implementation plan WP10)

The service can serve the branch-1 candidate **LoRA-D** (`esm2-35m-lora-d-aa4fc2b7`) next to the frozen ridge model
`m3-ext4.0-platt-v1`. It is registered as a frozen effect model but **not as the default**: the npz model answers every
request that names no model, until a separate serving decision sets `DF_DEFAULT_MODEL_ID`. The research status stays
`development_not_gate_closure`; the model card of the campaign says `serving_promotion:
not_authorized_by_research_execution`, and nothing here changes that.

## What it is

| Part | Value | Source |
| --- | --- | --- |
| Backbone | ESM-2 35M, `facebook/esm2_t12_35M_UR50D` @ `6fbf070e…`, float32, MIT | pinned research snapshot |
| Adapter | LoRA r = 8, alpha = 16 on every attention `query`/`value`; head Linear(1020, 64)–ReLU–Linear(64, 1) | refit `model.pt` of seeds 17, 29, 43 |
| Ensemble | mean of the three raw scores, then a three-class multinomial logistic calibrator | `final-calibrator.joblib`, fit on ensemble OOF of W only (`T_fit_cells: 0`) |
| Output | `score_dpsi_raw` = ensemble raw DeltaPSI; `p_dpsi_ge_1_calibrated` = probability of class `DeltaPSI >= 1` | same fields as the npz model |
| Calibrator values | only `platt` (the logistic calibrator); `iso` → 422 `INVALID_REQUEST` (field `calibrator`) | |

The serving code (`degron_footprint/lora.py`) is written again from the recipe instead of importing `degron_v3`, so the
parity test compares two implementations. The domain gate (R3) is applied to every model alike.

## Bundle (no pickle)

`make lora-bundle` (or `.venv-lora/bin/python etl/export_lora.py`) reads the campaign artifacts read-only, checks every
SHA-256 pinned by `jobs/model-card-parity/model-card.json`, and writes outside git:

```text
data/processed/lora-d-serving-v1/esm2-35m-lora-d-v1.json   manifest = weights_path / weights_sha256 of the model row
data/processed/lora-d-serving-v1/esm2-35m-lora-d-v1/
    adapter-seed{17,29,43}.npz   learned LoRA + head tensors (float32) and their training order
    calibrator.npz               coef (3, 1), intercept (3,), classes [0, 1, 2]
    base/                        ESM-2 35M snapshot (config, safetensors, tokenizer)
    parity-fixture.npz           research-implementation scores of two full tiles
```

The manifest pins every file's SHA-256; the API checks them all at start-up and the learned-state digest of each seed
against the refit `fit.json` when it builds the network (on the first request). `etl/sources.yaml` pins the manifest
hash, so the ETL refuses a changed bundle. The fixture comes from a CPU run, so a re-export on another machine may differ
at float precision; then pin the new manifest hash.

## Installing and turning it on

```bash
# local: a separate environment, so the default .venv stays numpy-only
python3 -m venv .venv-lora && .venv-lora/bin/pip install -r backend/requirements-dev.txt -r backend/requirements-lora.txt
make etl                                             # registers LoRA-D when the bundle exists (--lora auto|yes|no)
DF_DEFAULT_MODEL_ID=esm2-35m-lora-d-aa4fc2b7 ...     # optional: make it the default (serving decision)

# Docker: in .env
WITH_LORA=1                                          # backend image with PyTorch CPU + Transformers
DF_DEFAULT_MODEL_ID=                                 # empty = npz model stays the default
DF_LORA_THREADS=4
```

Without PyTorch the registry leaves LoRA-D out (`registry.errors`: "PyTorch/Transformers are not installed"), requests
naming it get 404 `MODEL_NOT_FOUND`, and the service stays healthy on the npz model. A `DF_DEFAULT_MODEL_ID` that is not
serving keeps the registry default and logs why. `/healthz`, `/v1/models` and `/v1/models/{id}` report the effective
default.

## Evidence (measured 17 Nov 2026)

| Check | Result | File |
| --- | --- | --- |
| Calibrator: scikit-learn `predict_proba` vs the softmax used in serving, 2,401 grid points | max diff 0.0 | `tests/results/lora-bundle.json` |
| Cross-runtime parity: research implementation, 32 W rows, CUDA (Windows campaign) vs CPU (WSL) | max diff 3.0e-6 (atol 1e-5) | same |
| Serving vs research implementation, 2 tiles × 532 substitutions, per seed / ensemble / probability | max diff 0.0 | same; `tests/test_lora.py::test_lora_parity_with_the_research_implementation` |
| Latency, RAM, image size | see `tests/results/latency-lora.json` | `tests/measure_latency_lora.py` |

The parity rows and both fixture tiles are W peptides the model was trained on (the e2e "typed" sequence is one too);
parity is about implementations, not accuracy. The accuracy
evidence of the model (post-hoc transfer on a previously examined held-out source, with the zero predictor better in the
PSI(WT) > 5 stratum) is in the model card (`GET /v1/models/esm2-35m-lora-d-aa4fc2b7`) and in
`research/lora-refit-transfer-2026-11-16/results.json`.
