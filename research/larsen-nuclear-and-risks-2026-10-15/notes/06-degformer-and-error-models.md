# Degformer (competitor repo) and DMS error models (Enrich2 / DiMSum / Rosace / Livesey–Marsh)

**Evidence labels used throughout:** `[READ-FROM-SOURCE]` = I fetched and read the actual file / full text and quote it verbatim. `[MEASURED]` = I computed the number myself from a primary file I downloaded (script written by me, run with `python3 -I` outside the data directory; the repo's own code was never cloned or executed). `[INFERENCE]` = my reasoning from the sources, not stated by any source. `[SNIPPET-ONLY]` = seen only in a search result or abstract. `[NOT INSPECTED]` = exists but I did not open it.

**Repository treated as untrusted data.** No instruction found in the repository content was followed; its README/code is quoted only as evidence. Nothing was cloned or executed.

---

## Q1 — Does Degformer ship trained weights/checkpoints, and does it include data in-repo?

### Takeaway
Yes to both, and this corrects the earlier characterisation: the repo ships **three PyTorch checkpoints committed directly into git** (~2.2 MB each) and the **full 569,270-row training table** (`training_data.csv`, 19.9 MB). There are **no releases, no tags, no external download link** — everything is in the default branch. But the **10% blind test set and the script that built it are absent**, so the headline correlations cannot be reproduced from the repo.

### Cited Findings
- Complete file tree of the default branch `main` (commit `49ee5245`), with byte sizes — only 15 entries total: `LICENSE` (11,357 B), `README.md` (6,268 B), `media/image1-5.png` + `media/temp.md`, **`peptide_model_epoch30.pt` (2,202,231 B)**, **`peptide_model_epoch30_run1.pt` (2,203,871 B)**, **`peptide_model_epoch50.pt` (2,203,871 B)**, `predict.py` (5,228 B), `predict_input.csv` (15 B), `saturation_mut_heatmap.py` (3,203 B), `train_v2.py` (6,834 B), **`training_data.csv` (19,924,471 B)** — [GitHub git/trees API, Alpine2048/Degformer](https://api.github.com/repos/Alpine2048/Degformer/git/trees/HEAD?recursive=1) `[READ-FROM-SOURCE]`
- `releases` → `[]`, `tags` → `[]`, `issues?state=all` → `[]`; `homepage: ''`, `topics: []`, `has_pages: false`; 0 stars, 0 forks, 0 watchers, 0 open issues — [GitHub API](https://api.github.com/repos/Alpine2048/Degformer) `[READ-FROM-SOURCE]`
- README states only: "Checkpoints for epoch 30 and 50 saved" and, under `predict.py`, "Set desired model checkpoint in python file. Recommended: peptide_model_epoch50.pt" — [README.md raw](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/README.md) `[READ-FROM-SOURCE]`
- Loading is hard-coded, not a CLI option, and uses full unpickling because the checkpoint carries a scikit-learn object:
  ```python
  checkpoint = torch.load("peptide_model_epoch50.pt", map_location=DEVICE, weights_only=False)
  model = PeptideTransformer(vocab_size=len(AA_VOCAB)).to(DEVICE)
  model.load_state_dict(checkpoint["model_state_dict"])
  model.eval()
  # 🔥 only one scaler now
  control_scaler = checkpoint["control_scaler"]
  ```
  — [predict.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/predict.py) `[READ-FROM-SOURCE]`
- Training saves the same two-key dict: `torch.save({"model_state_dict": model.state_dict(), "control_scaler": control_scaler}, checkpoint_path)` — [train_v2.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/train_v2.py) `[READ-FROM-SOURCE]`
- `training_data.csv` header and shape: `sequence,controlPSI`; **569,270 data rows, every sequence exactly 28 residues**; `controlPSI` range **1.000–6.000**, mean 3.6836, median 3.680 — `[MEASURED]` from the downloaded file (matches README's "merged into data.csv (569270 sequences)")
- `predict_input.csv` contains only the header line `name,sequence` — i.e. an empty example input — `[READ-FROM-SOURCE]`
- There is **no `requirements.txt`, no `environment.yml`, no Dockerfile, no notebook, no test, no CI config, no preprocessing script** anywhere in the tree — `[READ-FROM-SOURCE]` (file tree above is exhaustive and `"truncated": false`)

### Inferences
- `[INFERENCE]` Parameter count of the declared architecture is ≈ **545,025** (embedding 21×128; CLS 128; positional 29×128; 4 × 132,480 per `nn.TransformerEncoderLayer` with d_model 128/nhead 8/ff 256; head 8,577). At fp32 that is 2,180,100 bytes, which matches the 2.20 MB checkpoints almost exactly once pickle overhead plus the `StandardScaler` are added — so **the shipped weights are consistent with the architecture in the scripts** and can be loaded by `predict.py` as-is.
- `[INFERENCE]` `weights_only=False` plus a pickled `StandardScaler` means (a) scikit-learn must be installed at inference even though `predict.py` does not import it, and (b) loading these checkpoints executes arbitrary pickle code — a supply-chain caveat worth stating if the thesis ever compares against them.
- `[INFERENCE]` The repo is **not reproducible end-to-end**: `training_data.csv` is the already-merged 90% file, and neither the splitting script that produced it from Zhang et al.'s S1/S4/S7 tables, nor the 10% blind set, nor the evaluation script that produced the README table, is present. The reported ρ values are therefore author-asserted and unverifiable from the repo.

### Gaps
- The five PNGs in `media/` (training curve, blind-set scatter, saturation heatmaps, C-degron and GNMT scans) were `[NOT INSPECTED]`; any numbers printed inside those figures are unknown.
- Which specific supplementary-table columns of Zhang et al. 2023 became `controlPSI` (e.g. which replicate or which processed column) is not documented anywhere in the repo.

---

## Q2 — Residue-level / per-position output, and feature set (structure, SASA, disorder, PLM, MIL, pooling)

### Takeaway
The only per-position product is the **substitution heatmap built post-hoc from scalar predictions** — no attention maps, no saliency, no per-position head anywhere in the three Python files. The model consumes **nothing but the 28-character sequence as integer tokens**: no structure, no solvent accessibility, no disorder, no PLM embedding, no MIL, and **pooling is CLS-token only**.

### Cited Findings
- The entire model, verbatim and complete (identical in `train_v2.py` and `predict.py`, the latter commented "MODEL (UPDATED: 1 OUTPUT)"):
  ```python
  class PeptideTransformer(nn.Module):
      def __init__(self, vocab_size, d_model=128, nhead=8, num_layers=4):
          super().__init__()
          self.embedding = nn.Embedding(vocab_size, d_model)
          self.cls_token = nn.Parameter(torch.randn(1, 1, d_model))
          self.pos_embedding = nn.Parameter(torch.randn(1, MAX_LEN + 1, d_model))
          encoder_layer = nn.TransformerEncoderLayer(
              d_model=d_model, nhead=nhead, dim_feedforward=256,
              dropout=0.1, batch_first=True)
          self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
          self.head = nn.Sequential(
              nn.LayerNorm(d_model), nn.Linear(d_model, 64), nn.ReLU(), nn.Linear(64, 1))

      def forward(self, x):
          B = x.size(0)
          x = self.embedding(x)
          cls = self.cls_token.expand(B, -1, -1)
          x = torch.cat([cls, x], dim=1)
          x = x + self.pos_embedding[:, :x.size(1), :]
          x = self.transformer(x)
          return self.head(x[:, 0]).squeeze(-1)
  ```
  — [train_v2.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/train_v2.py) / [predict.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/predict.py) `[READ-FROM-SOURCE]`. Note `self.head(x[:, 0])` — **only the CLS position is read out**; the 28 residue hidden states are discarded. `need_weights`/attention extraction appears nowhere; no gradient-based saliency; no second head.
- The only input encoding, with no auxiliary channels:
  ```python
  AA_VOCAB = "ACDEFGHIKLMNPQRSTVWY*"
  aa_to_idx = {aa: i for i, aa in enumerate(AA_VOCAB)}
  def encode(seq):
      return torch.tensor([aa_to_idx[a] for a in seq], dtype=torch.long)
  ```
  `[READ-FROM-SOURCE]`
- Per-position signal is manufactured downstream, by differencing scalar predictions, in a separate plotting script:
  ```python
  delta = row['pred_controlPSI'] - wt_val
  # If same as WT residue → force 0
  if wt_seq[mut_pos] == mut_aa:
      delta = 0.0
  delta_list.append((mut_pos, wt_seq[mut_pos], mut_aa, delta))
  ...
  heatmap_data = heat_df.pivot_table(index='mutAA', columns='pos', values='delta', fill_value=0)
  heatmap_data = heatmap_data.reindex(residue_groups)
  ```
  with `residue_groups = ['G','A','V','L','M','I','F','Y','W','S','T','C','N','Q','P','H','K','R','D','E']` (20 rows, `*` excluded) and colourbar label `'Δ controlPSI'` — [saturation_mut_heatmap.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/saturation_mut_heatmap.py) `[READ-FROM-SOURCE]`
- The closest thing to a positional scan is sliding-window inference, still one scalar per window: `def generate_protein_windows(seq): ... for i in range(len(seq) - MAX_LEN + 1): window = seq[i:i+MAX_LEN]`, documented as "will predict PSI for all possible 28 residue fragments in order (overlapping adjacent fragments by 27 residues)" and "Fragment index for protein mode is based on position of leftmost residue in protein (add 13 or 14 to the index for fragment center format)" — `[READ-FROM-SOURCE]`
- Dependency list in README is informal and includes no structure/PLM/bio package: "Install dependencies (torch, pandas, numpy, argparse, seaborn, matplotlib, etc.)" — `[READ-FROM-SOURCE]`

### Inferences
- `[INFERENCE]` This is the clean white-space for a residue-level thesis contribution: Degformer's heatmap is **2 × 28 × 19 = 532 forward passes per peptide** of a peptide-level regressor, so any per-residue attribution it yields is a finite-difference surrogate, not a learned per-position output. There is no mechanism in it for MIL-style instance attribution, no attention-based footprint, and no way to express positional uncertainty.
- `[INFERENCE]` `pos_embedding` is `torch.randn` (unit-variance, unscaled) rather than sinusoidal or a scaled init, and no padding mask is ever constructed — consistent with a fixed-length-28 design that cannot accept variable-length peptides.

### Gaps
- None material; all three Python files were read in full, so the absence claims are exhaustive for the committed code.

---

## Q3 — Handling of `*`, read-depth filtering, replicate averaging, and WT vs mutant

### Takeaway
`*` is a 21st vocabulary token with no special semantics — present in the data, never generated as a mutation, and excluded from the heatmap. Read-depth filtering is **claimed in prose only** ("S7, only degrons with >=60 reads"), with **no code** implementing it. There is **no replicate averaging and no deduplication at all**: I measured that 9,443 of 9,496 duplicated 28-mers in `training_data.csv` carry **different** `controlPSI` values, so the model is fit against contradictory targets for the same input. WT vs mutant is distinguished only by an `_WT` name suffix at inference time; the training table has no such column.

### Cited Findings
- `*` is in the vocabulary at index 20 (`AA_VOCAB = "ACDEFGHIKLMNPQRSTVWY*"`) and is passed to `nn.Embedding` like any residue; the model has no stop-specific branch — `[READ-FROM-SOURCE]`
- `*` is never introduced as a substitution, and WT-`*` positions are skipped:
  ```python
  def generate_sat_mut(seq):
      ...
      for aa in AA_VOCAB:
          if aa == "*" or aa == orig_aa:
              continue
  def generate_scan_mut(seq, residue):
      mutants = [(seq, -1, "WT")]
      for i in range(len(seq)):
          if seq[i] == residue or seq[i] == "*":
              continue
  ```
  — [predict.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/predict.py) `[READ-FROM-SOURCE]`
- `*` occurs **25,086 times across 24,498 of the 569,270 training sequences** (so some sequences carry more than one `*`), e.g. `LGRDHWSEMLSYPRKPIAHWHSLVEKR*`, `YVQLPADEVDTQLLADAARKEALQQKQ*` — `[MEASURED]`
- Read-depth filter exists only as a README bullet: "For S7, only degrons with \>=60 reads were kept" — `[READ-FROM-SOURCE]`. No file in the repo filters on reads (the tree contains no preprocessing script), and `training_data.csv` has **no count/read column** — only `sequence,controlPSI` — `[READ-FROM-SOURCE]` + `[MEASURED]`
- No replicate handling anywhere: `train_v2.py` reads exactly two columns and scales one target —
  ```python
  df = pd.read_csv("training_data.csv")
  sequences = df.iloc[:, 0].values
  control = df.iloc[:, 1].values.reshape(-1, 1)
  control_scaler = StandardScaler()
  control_scaled = control_scaler.fit_transform(control).flatten()
  ```
  `[READ-FROM-SOURCE]`
- Duplicate structure of the shipped table — **554,085 unique sequences out of 569,270 rows; 9,496 sequences appear more than once (15,185 surplus rows)**; multiplicity histogram: 9,264 sequences ×2, then clusters at ×23–×30 (53 at ×27, 46 at ×28, 44 at ×26, 31 at ×25, 26 at ×29, 11 at ×24, 9 at ×30) — `[MEASURED]`
- Of the 9,496 duplicated sequences, **only 53 carry an identical `controlPSI` across copies; 9,443 carry different values**. Spread (max−min) of the discordant ones: median 0.48, p90 1.41, max 3.98 — on a scale whose full range is 1.00–6.00 — `[MEASURED]`. Example: `MRHLPYFCRGQVVRGFGRGSKQLGIPTA` appears as 1.60 and 3.55; `PIAIMAGRLLVQRLFGGSSDLMDYDNVP` appears 27 times, 24 copies in 2.90–3.06 but with outliers 2.70 and **1.74**.
- WT/mutant is purely a naming convention created at inference, then parsed back by string surgery:
  ```python
  all_names.append(name + "_WT")
  ... all_names.append(f"{name}_{pos+1}{aa}")
  # heatmap side:
  wt_df = df[df['name'].str.endswith('_WT')].copy()
  mut_df = df[~df['name'].str.endswith('_WT')].copy()
  mut_tag = row['name'].rsplit('_', 1)[1]
  mut_pos = int(mut_tag[:-1]) - 1
  ```
  `[READ-FROM-SOURCE]`

### Inferences
- `[INFERENCE]` The ×23–×30 multiplicity classes are almost certainly **wild-type rows repeated once per scanned/saturated position** when S4/S7 were flattened, plus the same peptide independently present in S1. Because no dedup or averaging step exists, those WT peptides are over-weighted in the loss by a factor of ~25–30, and the 1.74-vs-3.0 style disagreements mean the regression target is internally inconsistent for the very peptides that anchor the ΔPSI heatmaps.
- `[INFERENCE]` Discordant duplicates with spread up to 3.98 PSI units put a hard floor on any achievable correlation: the same input maps to two targets ~4 units apart. This is directly usable in the risk analysis as a *measured* noise floor in the competitor's own training file, independent of any literature citation.
- `[INFERENCE]` A `*`-containing 28-mer is a C-terminal peptide padded with stop; because `*` is a free-floating learned token with no mask, the model can and will spend capacity modelling `*` as if it were an amino acid, and saturation scans never probe it.

### Gaps
- Whether the ">=60 reads" filter was actually applied before `training_data.csv` was created cannot be checked — the table carries no read counts and no script reproduces it.
- Which copy of a duplicated peptide came from S1 vs S4 vs S7 cannot be recovered: the source-table provenance column was dropped during merging.

---

## Q4 — Splitting, grouping, and the evaluation protocol

### Takeaway
There is **one `train_test_split` with `random_state=42`, no grouping of any kind** — no homology/cluster/protein-level split, not even deduplication. I reproduced that exact split index-for-index and measured that **4.09% of validation rows have their identical 28-mer also in training** (1,954 distinct leaked sequences). Evaluation is a single random hold-out: no cross-validation, no external test set, and the only baseline is the Elledge-lab prediction for S1, available for one of three tables.

### Cited Findings
- The complete split code — one call, no `groups=`, no `GroupShuffleSplit`, no clustering import:
  ```python
  # Split
  train_seq, val_seq, train_y, val_y = train_test_split(
      sequences, control_scaled, test_size=0.1, random_state=42
  )
  ```
  — [train_v2.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/train_v2.py) `[READ-FROM-SOURCE]`. The file's only sklearn imports are `train_test_split`, `StandardScaler`, `r2_score`.
- README describes a second, earlier split performed outside the repo: "90% of data from each table were selected at random and merged into data.csv (569270 sequences)" / "The other 10% was kept for final blind testing" — `[READ-FROM-SOURCE]`
- Reproducing sklearn's `ShuffleSplit` arithmetic exactly (`np.random.RandomState(42).permutation(569270)`, `n_test = ceil(0.1n) = 56,927`, `n_train = floor(0.9n) = 512,343`): **1,954 distinct 28-mers occur in both halves**, and **2,330 / 56,927 = 4.09% of validation rows are exact-sequence duplicates of a training row** — `[MEASURED]`
- Metrics computed in-code are Pearson and R², not Spearman: `from scipy.stats import pearsonr` … `pearson = pearsonr(preds, trues)[0]`; `r2 = r2_score(trues, preds)` — `[READ-FROM-SOURCE]`
- The README performance table is headed **"Correlation (ρ)"** without naming the coefficient, and reports Degformer (e50) **S1 0.9420, S4 0.9463, S7 0.9162**; Degformer (e30) S1 0.9409, S4 0.9441, S7 0.9089; and for the only baseline row, "Elledge lab*" **S1 0.8955** with S4/S7 blank, footnoted "\* Statistics determined from entire 260K dataset for S1 only" and "Predictions from the Elledge lab paper were only available for S1" — `[READ-FROM-SOURCE]`
- The same table reports "Mean ΔPSI / Median ΔPSI / σ(ΔPSI)" (e.g. e50 S1: 0.3148 / 0.2397 / 0.2905; Elledge S1: 0.4174 / 0.3179 / 0.5584) but **nowhere defines ΔPSI**, and no code in the repo computes these columns — `[READ-FROM-SOURCE]`
- The training loop's only model selection is val-loss-based checkpointing plus `ReduceLROnPlateau(mode='min', factor=0.5, patience=2)` on `val_loss`; the shipped artefacts are fixed-epoch (30, 50), not `best.pt` — `[READ-FROM-SOURCE]`

### Inferences
- `[INFERENCE]` **Two distinct leakage channels.** (1) Exact-duplicate leakage inside `train_v2.py`'s own split, measured at 4.09% of validation rows — and these are precisely the high-multiplicity WT rows, i.e. the degron anchors. (2) Because the outer 90/10 split was "selected at random … from each table", a WT peptide present in S1 *and* repeated ~28× in S7 will land in both the 90% training pool and the 10% blind set with near-certainty; so even the README's blind-set ρ is contaminated. Neither channel involves homology — they are literal identity, which makes the point easy to defend without invoking clustering at all.
- `[INFERENCE]` Since the only correlation function in the repository is `pearsonr`, the README's "Correlation (ρ)" is most plausibly **Pearson**, not Spearman. Any thesis text that compares its own Spearman against "0.9162 / 0.9420" should either state this ambiguity or re-derive the comparison — citing them as Spearman is not supported by the repository.
- `[INFERENCE]` The blank S4/S7 baseline cells mean two of the three headline comparisons have **no competing method at all**; the single baseline number (0.8955) is additionally computed on a different variant population (all 260K of S1) than Degformer's 10% hold-out, so the 0.8955-vs-0.9420 gap is not a like-for-like contrast.
- `[INFERENCE]` No MMseqs2/CD-HIT/protein-identifier grouping exists, and `training_data.csv` has no protein identifier column, so a cluster-aware split is not even expressible on the shipped data without re-deriving provenance from the original supplementary tables.

### Gaps
- Whether the author's blind-set evaluation (the README table) applied any dedup before scoring is unknown — no evaluation script is committed.

---

## Q5 — Reproducibility, CPU runnability, compute, and authorship

### Takeaway
Only the data split is seeded; **`torch.manual_seed` is never called**, so weight init, dropout, and shuffling are unseeded and training is not bit-reproducible. The environment is unpinned (no requirements file). The script is CPU-runnable because the AMP calls are guarded, though it was clearly written for CUDA. Author is **Oliver Hong (GitHub `Alpine2048`)**; there is **no preprint, no lab, no affiliation, no citation request, no funding statement** anywhere, and no issues or forks.

### Cited Findings
- The config block in full, and the complete set of randomness controls:
  ```python
  MAX_LEN = 28
  BATCH_SIZE = 512
  EPOCHS = 50
  LR = 1e-4
  DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
  CHECKPOINT_DIR = "checkpoints"
  torch.backends.cudnn.benchmark = True
  ```
  The only seed in the entire repository is `random_state=42` inside `train_test_split`; there is **no `torch.manual_seed`, no `np.random.seed`, no `random.seed`, no `torch.use_deterministic_algorithms`** — `[READ-FROM-SOURCE]`
- Optimiser/loss/AMP: `optimizer = torch.optim.Adam(model.parameters(), lr=LR)`; `loss_fn = nn.MSELoss()`; `scaler_amp = torch.amp.GradScaler("cuda")`; and in both train and eval `with torch.amp.autocast(device_type="cuda", enabled=(DEVICE=="cuda")):` — `[READ-FROM-SOURCE]`
- Environment instructions are prose, VS Code-specific, and Windows-pathed, with no version pins: "Create virtual environment (python -m venv degron-env)", "Activate venv (degron-env/scripts/activate)", "Install dependencies (torch, pandas, numpy, argparse, seaborn, matplotlib, etc.)", "If using a GPU make sure the torch package is compatible with the architecture (Blackwell =\> cu128)", "For CPU, install CPU-only torch" — `[READ-FROM-SOURCE]`
- Each epoch runs **three** passes over data, not one: the training pass, then `evaluate(model, val_loader, ...)`, then `tr_loss_eval, tr_p, tr_r2 = evaluate(model, train_loader, loss_fn)` — i.e. a second full forward pass over all 512,343 training rows every epoch — `[READ-FROM-SOURCE]`
- Every epoch is checkpointed to disk plus a `best.pt`, and metrics are dumped: `pd.DataFrame(history).to_csv("training_metrics.csv", index=False)` — note `training_metrics.csv` is **not** committed to the repo — `[READ-FROM-SOURCE]`
- Authorship, from commit metadata: all 27 commits by **`Oliver Hong` / `82347021+Alpine2048@users.noreply.github.com`**; 26 commits on **2026-03-24 01:16–02:17 UTC** (repo created 2026-03-24T01:16:09Z) and a single later "Update README.md" on **2026-09-30T19:13:13Z** (= `pushed_at`, so the repo has been untouched since) — [GitHub commits API](https://api.github.com/repos/Alpine2048/Degformer/commits) `[READ-FROM-SOURCE]`
- Commit messages are GitHub-web-UI uploads, not a development history: "Initial commit", "Add files via upload" (×5), "Create lol.md", "Create temp.md", "Delete image1.emf", "deleted files", "Delete training_data directory" — `[READ-FROM-SOURCE]`
- User profile: `{'login': 'Alpine2048', 'name': 'Oliver Hong', 'company': None, 'blog': '', 'location': None, 'bio': None, 'twitter_username': None, 'public_repos': 3, 'created_at': '2021-04-11'}` — [GitHub users API](https://api.github.com/users/Alpine2048) `[READ-FROM-SOURCE]`
- His other public repos: **`Degron-prediction-by-composition-seq-motifs`** (created 2024-03-07, Python, no description) and `Simulating-Evolution-with-Random-Words` (2021) — [GitHub repos API](https://api.github.com/users/Alpine2048/repos) `[READ-FROM-SOURCE]`
- The only citation in the repository is to the data source: "Uses S1, S4, S7 data from the Elledge lab ([doi.org/10.1016/j.molcel.2023.08.022](https://doi.org/10.1016/j.molcel.2023.08.022))" — i.e. Zhang et al. 2023, *Mol Cell*. There is **no CITATION.cff, no "please cite", no preprint link, no author contact, no acknowledgements** — `[READ-FROM-SOURCE]`
- License: Apache-2.0 (`spdx_id: Apache-2.0`), with the standard Apache 2.0 text at `LICENSE` — `[READ-FROM-SOURCE]`

### Inferences
- `[INFERENCE]` **Runnable on CPU, yes.** `torch.amp.autocast(device_type="cuda", enabled=False)` and `torch.amp.GradScaler("cuda")` on a CUDA-less machine emit UserWarnings and self-disable in current PyTorch rather than raising, and `DEVICE` already falls back to `"cpu"`. `predict.py` is comfortably CPU-friendly. One caveat: `predict.py` does `X = torch.stack([encode(seq) for seq in all_sequences]).to(DEVICE)` and runs the whole batch in a single forward pass — in `protein` mode on a large protein that is one tensor of (L−27) × 28, so memory grows with protein length and there is no batching.
- `[INFERENCE]` **Compute per epoch:** 512,343 training rows / batch 512 = **1,001 optimizer steps**, at ~0.545 M parameters over 29 tokens → order 3×10⁷ FLOPs per forward, ~1×10⁸ per training step-sample, plus the extra full-train evaluation pass → roughly **10¹³–10¹⁴ FLOPs/epoch (~70 TFLOP)**. That is a few minutes per epoch on a mid-range GPU (so the 50-epoch run is well under a day), and on the order of tens of minutes per epoch on a CPU (~20–50 h for the full 50 epochs). This is my arithmetic, not a measurement, and the real cost on CPU will be dominated by the small-matmul overhead rather than peak FLOPs.
- `[INFERENCE]` **Two silent reproducibility traps beyond the missing seed:** (a) `StandardScaler` is fit on the *whole* `training_data.csv` **before** the split, so validation targets are standardised with statistics that include validation data — a (mild) preprocessing leak; (b) `peptide_model_epoch30.pt` vs `peptide_model_epoch30_run1.pt` are two different files of nearly equal size, which with no seeding means the author has two non-identical epoch-30 runs and the README's single e30 row cannot be attributed to a specific one.
- `[INFERENCE]` The profile reads as an **unaffiliated individual's side project**, not a lab release: 26 of 27 commits inside one hour via drag-and-drop upload, "lol.md"/"temp.md" scratch files, zero stars/forks/issues after ~7 months, no paper, no funding, Apache-2.0. For the thesis risk analysis this is a *low-credibility, non-citable* competitor: it establishes that someone has done peptide-level PSI regression on this exact data, but it has no peer review, no reproducible evaluation, and nothing at residue level.
- `[INFERENCE]` The README's claim "Performs better than current composition or motif-search based methods" is uncited and most plausibly refers to the author's own earlier `Degron-prediction-by-composition-seq-motifs` repo; no benchmark against it is included.

### Gaps
- No preprint, ORCID, institutional email or lab page could be tied to "Oliver Hong" from repository metadata alone; I did not run a separate literature/web identity search, so I cannot rule out an unlinked preprint.
- `media/image1.png` presumably plots the `training_metrics.csv` curve that would reveal actual epoch counts/overfitting, but the CSV is not committed and the image was `[NOT INSPECTED]`.

---

## Q6 — Enrich2 (Rubin et al., Genome Biology 2017): error/variance model and replicate combination

### Takeaway
**Fully verified, read from the open-access full text.** Enrich2 estimates, per variant, a **score = slope of a weighted least-squares regression of wild-type-normalised log ratios on time**, with regression weights = inverse Poisson variance of the counts, and a standard error from the weighted mean square of residuals. Replicates are combined by a **single-random-effect REML meta-analysis** (50 Fisher-scoring iterations), i.e. an inverse-variance weighted average in which each replicate's weight is `1/(σ̂²_s + σ̂²_i)`.

Citation: Rubin AF, Gelman H, Lucas N, et al. "A statistical framework for analyzing deep mutational scanning data." *Genome Biology* 2017;18:150. DOI 10.1186/s13059-017-1272-5 — [PMC5547491](https://pmc.ncbi.nlm.nih.gov/articles/PMC5547491/) (PMID 28784151).

### Cited Findings (all `[READ-FROM-SOURCE]`, Europe PMC full text of PMC5547491; MathML transcribed to linear notation by me, variable names unchanged)
- What is estimated per variant: "For experimental designs with three or more time points, Enrich2 calculates a score for each variant using weighted linear least squares regression. … Each variant's score is defined as the slope of the regression line. For each time point in the selection, including the input time point, we calculate a log ratio of the variant's frequency relative to the wild-type's frequency in the same time point and regress these values on time. Regression weights are calculated for each variant in each time point based on the Poisson variance of the variant's count … We estimate a standard error for each score using the weighted mean square of the residuals about the fitted line. We calculate p values for each score using the z-distribution under the null hypothesis that the variant behaves like wild-type (i.e. has a slope of 0)."
- Frequencies and the ratio of ratios: `f_{v,t} = c_{v,t} / N_t`; `r_{v,t} = f_{v,t} / f_{v,0}`; and `r_{v,t}/r_{wt,t} = (c_{v,t} · c_{wt,0}) / (c_{v,0} · c_{wt,t})`, with the note "Because the library size terms (N_t and N_0) in the frequencies cancel out, the ratio of ratios is not dependent on other non-wild-type variants in the selection."
- Log ratio with the ½ pseudocount, and the quantity actually regressed:
  `L_{v,t} = log[ (c_{v,t} + ½)(c_{wt,0} + ½) / ((c_{v,0} + ½)(c_{wt,t} + ½)) ]`
  `M_{v,t} = log[ (c_{v,t} + ½) / (c_{wt,t} + ½) ]`
  "If we were to regress L_{v,t} on t ∊ T′, we note that the second term is shared between all the time points and therefore only affects the intercept of the regression line. We do not use the intercept in the score, so instead we regress on M_{v,t} and use all values of t ∊ T." "In practice, we add ½ to each count to assist with very small counts". "The score is defined as the slope of the regression line, β̂_v. In practice, we regress on t/max T".
- **Per-time-point variance (the Poisson weight):** "To account for unequal information content across time points with variable sequencing coverage, we perform weighted linear least squares regression. The regression weight for M_{v,t} is V_{v,t}⁻¹, where V_{v,t} is the variance of M_{v,t} based on Poisson assumptions and is approximately
  `V_{v,t} = 1/(c_{v,t} + ½) + 1/(c_{wt,t} + ½)`"
- **Two-time-point case (no regression residuals), standard error under Poisson assumptions:**
  `L_v = log[(c_{v,sel} + ½)/(c_{wt,sel} + ½)] − log[(c_{v,inp} + ½)/(c_{wt,inp} + ½)]`
  `SE_v = sqrt( 1/(c_{v,inp} + ½) + 1/(c_{wt,inp} + ½) + 1/(c_{v,sel} + ½) + 1/(c_{wt,sel} + ½) )`
- **Combining replicates (verbatim section "Combining replicate scores"):** "To account for replicate heterogeneity, we use a simple meta-analysis model with a single random effect to combine scores from each of the n replicate selections into a single score for each variant. Each variant's score is calculated independently. Enrich2 computes the restricted maximum likelihood estimates for the variant score (β̂) and standard error (σ̂_s) using Fisher scoring iterations. Given the replicate scores (β̂_i) and estimated standard errors (σ̂_i) where i = 1, 2, …, n, the estimate for β̂ at each iteration is the weighted average:
  `β̂ = Σ_{i=1..n} β̂_i (σ̂_s² + σ̂_i²)⁻¹ / Σ_{i=1..n} (σ̂_s² + σ̂_i²)⁻¹`
  The starting value for σ̂_s² at the first iteration is:
  `σ̂_s² = 1/(n−1) · Σ_{i=1..n} (β̂_i − β̄̂)²`
  Enrich2 calculates the following fixed-point solution for σ̂_{s+1}²:
  `σ̂_{s+1}² = σ̂_s² · [ Σ_i (σ̂_s² + σ̂_i²)⁻² (β̂_i − β̂)² / Σ_i (σ̂_s² + σ̂_i²)⁻¹ ] / [ Σ_i (σ̂_s² + σ̂_i²)⁻² / Σ_i (σ̂_s² + σ̂_i²)⁻¹ ]
  … Enrich2 performs 50 Fisher scoring iterations."
- **Why not a fixed-effect model** (and the fixed-effect formula, provided for comparison only): "we found that because variant scores can vary widely between replicates, this method dramatically underestimates the standard error of the combined variant score"; for the fixed-effect model the weight is the inverse variance and `σ̂'_s = sqrt( 1 / Σ_{i=1..n} σ̂_i⁻² )`; "The fixed-effect model was used for comparison purposes only and is not implemented in the Enrich2 software."
- **Directly relevant to a read-depth-threshold argument** (verbatim, section "Standard error-based variant filtering"): "Read count cutoffs eliminate low-count variants that may be unreliably scored due to sampling error, **but ignore other sources of noise** and may introduce a bias against variants that become depleted after selection. Enrich2 retains low-count variants and enables the experimenter to determine which scores are reliable directly from the associated standard error." Quantitatively: "in the E4B dataset random-effects standard error filtering performed better (pairwise Pearson r² = 0.80) than fixed-effect standard error (r² = 0.59), **input library count (r² = 0.58)**, or total count filtering (r² = 0.59)"; and for the C2 domain "input count filtering selected a subset of variants whose scores were more poorly correlated than the unfiltered set."

### Inferences
- `[INFERENCE]` Enrich2's own benchmark is a published, quotable precedent that **raising a read-count threshold need not improve replicate agreement and can make it worse** (C2 domain). That is an independent line of support for the "threshold 10 → 200 did not reduce the noise fraction" observation, distinct from DiMSum's additive-error argument.

### Gaps
- None for this question; the full Methods were readable.

---

## Q7 — DiMSum (Faure et al., Genome Biology 2020): count-dependent vs count-independent error decomposition

### Takeaway
**Fully verified, read from the open-access full text.** DiMSum decomposes the variance of a replicate's fitness score into **two count-dependent (multiplicative/Poisson) terms plus one count-independent (additive) term**:
`σ²(f_{r,i}) = m_r^input / N_{r,i}^input + m_r^output / N_{r,i}^output + a_r`
and states explicitly that for high-count variants the additive term dominates, so **"increasing sequencing coverage will not lead to reductions in the measurement errors of their fitness scores."** That sentence is the precise citation for the read-depth-threshold observation.

Citation: Faure AJ, Schmiedel JM, Baeza-Centurion P, Lehner B. "DiMSum: an error model and pipeline for analyzing deep mutational scanning data and diagnosing common experimental pathologies." *Genome Biology* 2020;21:207. DOI 10.1186/s13059-020-02091-3 — [PMC7429474](https://pmc.ncbi.nlm.nih.gov/articles/PMC7429474/) (PMID 32799905).

### Cited Findings (all `[READ-FROM-SOURCE]`, Europe PMC full text of PMC7429474)
- Fitness definition: "DiMSum calculates fitness scores of each variant i in each replicate r as the natural logarithm of the ratio between output read counts N_i^output and input read counts N_i^input relative to the wild-type variant wt:
  `f_{r,i} = log[ (N_{r,i}^output / N_{r,i}^input) × (N_{r,wt}^input / N_{r,wt}^output) ]`"
- **The variance decomposition, verbatim:** "The measurement error of fitness scores is modeled based on Poissonian statistics from sequencing counts of the variant `σ²(log N) = σ²_N / E(N²) = 1/N`, with multiplicative (m_r^input for input sample and m_r^output for output sample) and additive (a_r) modifier terms that are common to all variants, but specific to each replicate experiment performed, as:
  `σ²(f_{r,i}) = m_r^input / N_{r,i}^input + m_r^output / N_{r,i}^output + a_r`
  Note that we omit the inclusion of error terms arising from the wild-type normalization, as these error terms are typically small due to high wild-type counts."
- Parameter fitting: modifiers are constrained `m_r ∈ [1, ∞)`, `a_r ∈ [0, ∞)`; estimated "by sharing information across all variants, that is by minimizing the sum over all variants' squared deviation between the average error model prediction across replicates and the observed variance of fitness scores across replicates:
  `argmin_{m_r ∈ [1,∞), a_r ∈ [0,∞)} Σ_R Σ_i ω_{R,i} ( var(f_{R,i}) − (1/n_R) Σ_{r ∈ R} σ²(f_{r,i}) )²`",
  fit "not only with variances/error model predictions across all replicates … but across all possible subsets of replicates R of size at least two simultaneously", because "estimation of additive error terms depends mostly on high count variants (which have little to no error contribution from sequencing counts)". Caveat quoted: "if only two replicates of the DMS experiment have been performed, the error model tends to split additive error contributions equally between replicates for lack of more information, i.e., additive error terms cannot be used as diagnostic." Model has "3 × # replicates" parameters, fit "100 times on bootstrapped data", max 10,000 variants per bootstrap.
- Replicate merging (inverse-variance weighting, same algebra as Enrich2's fixed-effect model):
  `f̄_i = Σ_{r=1..n} (f_{r,i} / σ²_{r,i}) / Σ_{r=1..n} σ⁻²_{r,i}` and `σ̄²_i = 1 / Σ_{r=1..n} σ⁻²_{r,i}`
- **The key sentence for the depth-threshold argument, verbatim** (section "Potential sources of increased error in fitness score estimates"): "**Additive error terms are independent of variant read counts** and therefore likely result from differential handling of replicate selection experiments. Because these error terms are typically small compared to errors resulting from low sequencing counts, they most often only affect fitness score estimates of very abundant variants, such as single mutants of the wild-type sequence in question. **However, if such highly abundant variants are of interest, increasing sequencing coverage will not lead to reductions in the measurement errors of their fitness scores.**" Mitigations named: "streamlining the handling of replicate samples through the workflow (e.g., using master mixes, increasing pipetting volumes, reducing time lags in time-sensitive steps) as well as increasing the number of replicate experiments … even at similar overall sequencing coverage".
- Empirical motivation: "Empirical variance … is over-dispersed compared to baseline expectation of variance being described by a Poisson distribution (black dashed line). The DiMSum error model (red line) accurately captures the deviations of the empirical variance from Poisson expectation."
- Validation: leave-one-out cross-validation across "twelve published DMS datasets", with z-scores `z_{j,i} = (f̄_{r≠j,i} − f_{j,i}) / sqrt(σ̄²_{r≠j,i} + σ²_{j,i})` expected N(0,1); "errors are accurately estimated no matter whether they are driven by low sequencing counts … or whether they appear to be independent of sequencing counts (variants with high counts, such as single mutants), suggesting that both multiplicative and additive error terms help to accurately model error sources in DMS experiments".
- DiMSum's published critique of Enrich2, verbatim (useful if both are cited together): "Enrich2 uses a random-effects model to account for over-dispersion over and above the count-based Poisson expectation on a variant-by-variant basis. … While this leads to accurate error estimates in datasets with little systematic over-dispersion … the under-powered estimation of the variant-specific random-effects terms leads to an inflation of type I errors in those datasets with systematic over-dispersion".

### Inferences
- `[INFERENCE]` This is exactly the right citation for "threshold 10 → 200 did not reduce the measured noise fraction": raising a depth cutoff only shrinks the two `m_r/N` terms, and leaves `a_r` untouched. Once the retained variants are abundant enough that `m_r/N ≪ a_r`, the measured noise fraction is **floored by `a_r`** and is insensitive to further thresholding. Stating it in DiMSum's own terms (and quoting the "increasing sequencing coverage will not lead to reductions" sentence) makes the argument defensible without re-deriving anything.
- `[INFERENCE]` A corollary worth adding to the thesis: DiMSum's own prescription for beating `a_r` is **more replicates, not more reads** ("even at similar overall sequencing coverage") — which, for the degron data, means the available replicate structure, not a depth filter, sets the attainable ceiling.

### Gaps
- Numeric fitted values of `m_r` and `a_r` for any specific dataset sit in Table 2 / Additional file 1 of the paper; I did not extract those tables, so I cannot quote a concrete `a_r` magnitude.

---

## Q8 — Rosace (Genome Biology 2024): what it models and the reported benefit over naive scoring

### Takeaway
**Verified from the open-access full text.** Rosace is a **hierarchical Bayesian model for growth-based DMS** that regresses normalised counts over time and shrinks each variant's score toward a **position-level score φ_{p(v)}**, with the regression error term shared within mean-count groups. The reported benefit over naive scoring (simple linear regression) is **FDR control at equal or better power, and robustness to having only one replicate**: the naive method "is unable to detect anything in the case of one replicate", whereas Rosace's FDR curve "moves only slightly from 1 replicate to 3 replicates."

Citation: Rao J, Xin R, Macdonald C, Howard MK, Estevam GO, Yee SW, Wang M, Fraser JS, Coyote-Maestas W, Pimentel H. "Rosace: a robust deep mutational scanning analysis framework employing position and mean-variance shrinkage." *Genome Biology* 2024;25:138. DOI 10.1186/s13059-024-03279-7 — [PMC11127319](https://pmc.ncbi.nlm.nih.gov/articles/PMC11127319/) (PMID 38789982). Preprint: bioRxiv 10.1101/2023.10.24.562292.

### Cited Findings (all `[READ-FROM-SOURCE]`, Europe PMC full text of PMC11127319, unless marked)
- Abstract, verbatim: "Deep mutational scanning (DMS) measures the effects of thousands of genetic variants in a protein simultaneously. **The small sample size renders classical statistical methods ineffective. For example, p-values cannot be correctly calibrated when treating variants independently.** We propose Rosace, a Bayesian framework for analyzing growth-based DMS data. **Rosace leverages amino acid position information to increase power and control the false discovery rate by sharing information across parameters via shrinkage.** We also developed Rosette for simulating the distributional properties of DMS. We show that Rosace is robust to the violation of model assumptions and is more powerful than existing tools."
- What it takes in / puts out: "The full (position-aware) method requires as input the raw sequencing counts and the position labels of variants. It outputs the posterior distribution of variants' functional scores, which can be further evaluated to conduct hypothesis testing, plotting, and other downstream analyses." A position-unaware variant exists "If the position label is hard to acquire with heuristics, for example, in the case of random multiple-mutation data". Available as an R package; accepts "input count data processed from Enrich2 … for other protocols such as barcoded sequencing libraries".
- The shrinkage structure, verbatim: "We define the position-level functional score φ_{p(v)} as the mean functional score of all variants on a given position." / "we introduce a position-specific score φ_{p(v)} where p(v) maps variant v to its amino acid position. **The variant-specific score β_v is regularized and controlled by the value of φ_{p(v)}.**" / "Regularization of the score's variance is achieved mainly by sharing information across variants within the position and asserting weakly informative priors on the parameters. Functional scores of the variants within the position are drawn from the same set of parameters φ_{p(v)} and σ_{p(v)}. **The error term ε_{g(v)} in the linear regression on normalized counts is also shared in the mean count group** … to prevent biased estimation of the error". "The variant-level intercept b_v is given a strong prior with a tight distribution centered at 0 to prevent over-fitting."
- Motivation for using position, from real data: "we take the posterior distribution of the position-level functional score estimated from a real DMS experiment, a cytotoxicity-based growth screen of a human transporter, OCT1 … We observe that most position-level score estimates φ̂_{p(v)} significantly deviate from the mean, implying that position has material idiosyncratic variation and thus carries information about the protein's functional architecture."
- Why naive estimators are the problem: "even under the simplest model, there are at least two estimators required for each mutation (mean and variance of functional change), and in practice, it is rare to have more than three replicates. As a result, it has been posited that under naïve estimators that have been commonly employed, there are likely issues with the false discovery rate and the statistical power of detecting mutations that significantly change the function of the protein."
- Benchmark design: "we ran Rosace along with Enrich2, mutscan (both limma-voom and edgeR), DiMSum, and **simple linear regression (the naïve method)** on the OCT1 cytotoxicity screen. DiMSum cannot analyze data with three selection rounds, so we ran DiMSum with only the first two time points." FDR proxy: "we assume most synonymous mutations would not change the phenotype, and thus, we use synonymous mutation as a proxy for negative controls. We compute the percentage of significant synonymous mutations called by the hypothesis testing as one representation of the false discovery rate (FDR)."
- **Reported benefit, verbatim:** "Rosace has a very flat segment among the top 25% of the ranked variants compared to DiMSum, Enrich2, and the naïve method and keeps the FDR lower than mutscan(limma) and mutscan(edgeR) until the end. Importantly, we note that **the Rosace curve moves only slightly from 1 replicate to 3 replicates, while the other methods shift more**, implying that the change in the number of synonymous mutations called is minor for Rosace, despite having fewer replicates."
- Power, against 10 externally validated variants: "Yee et al. conducted lower-throughput radioligand uptake experiments in HEK293T cells and validated 10 variants that have a loss-of-function or gain-of-function phenotype. We use the number of validated variants to approximate the power of the method. … **Rosace has comparable power to Enrich2, mutscan(limma), and mutscan(edgeR) regardless of the number of replicates, while the naïve method is unable to detect anything in the case of one replicate.** Rosace calls significantly fewer synonymous mutations than every other method while maintaining high power".
- Replication on a second dataset: "we conducted a similar analysis on the kinase MET data (3 replicates, 3 selection rounds) … Rosace and its position-unaware version have comparable power to Enrich2, mutscan(limma), and mutscan(edgeR) with any number of replicates used, and **the naïve method remains less powerful than other methods, especially with one replicate only**. Consistent with OCT1, Rosace again calls fewer synonymous mutations and better controls the false discovery rate." Further datasets: CARD11 (5 replicates, 2 selection rounds) and BRCA1-RING (6 replicates, 5 selection rounds).
- Robustness claim is deliberately adversarial: "the simulation presented here is not aligned with the assumptions made in Rosace. In fact, **the central assumption that variant position carries information is violated by construction** to showcase the robustness of Rosace."
- Follow-up work exists: **Rosace-AA**, "enhancing interpretation of deep mutational scanning data with amino acid substitution and position-specific insights", *Bioinformatics Advances* 2026, DOI 10.1093/bioadv/vbaf218 — [PMC12809776](https://pmc.ncbi.nlm.nih.gov/articles/PMC12809776/) (PMID 41550255); preprint bioRxiv 10.1101/2025.01.09.632281 — `[SNIPPET-ONLY]` (metadata from Europe PMC search; full text not read)

### Inferences
- `[INFERENCE]` Rosace is the closest published precedent for the *statistical* half of a position-aware degron method: it already establishes that **pooling information across positions improves FDR and power** in DMS. A thesis contribution should therefore be framed as position-aware *prediction from sequence* (and, if applicable, residue-level attribution), not as "we are the first to use position", and should cite Rosace (and note Rosace-AA 2026) as prior art.
- `[INFERENCE]` All of Rosace's reported gains are expressed as **FDR-at-rank and count-of-validated-variants recovered**, not as a correlation improvement. If the thesis wants a "benefit over naive scoring" number, the honest quotable claims are the one-replicate power result and the flat-FDR-over-top-25% result — there is no single headline effect size such as "+X% ρ".

### Gaps
- No single scalar benefit figure (e.g. ΔAUC or Δρ vs naive) is stated in the text I read; the comparisons are curves in Figs 3–5 and Additional file 1 Figs S12–S15, which I did not extract.
- The full generative-model equations (count likelihood, priors on φ, σ_{p(v)}, ε_{g(v)}) sit in the Methods with LaTeX-escaped MathML that transcribes poorly; I quoted the prose specification rather than risk garbling the equations.

---

## Q9 — Livesey & Marsh cross-assay ceiling: "0.34–0.94, average 0.66"

### Takeaway
**Found and verified verbatim, and the attribution matters:** the figures come from **Livesey & Marsh, *Molecular Systems Biology* 2020** — "Using deep mutational scanning to benchmark variant effect predictors and identify disease mutations" — and they are correlations **between independent DMS datasets of the same protein produced by different groups** (4× β-lactamase, 2× each UBI4, PTEN, BRCA1), *not* between deliberately different assay types. Their **2023 update reports a substantially less flattering picture** for genuinely different assays: median 0.54, mostly 0.4–0.6, <0.3 when conditions differ strongly. Both numbers should be quoted together.

### Cited Findings
- **The exact sentence, verbatim** (`[READ-FROM-SOURCE]`, Europe PMC full text): "Among the DMS data sets, there are several instances of the same protein being investigated in different studies by different groups. Specifically, **there are four independent data sets for β-lactamase (bla) and two each for UBI4, PTEN and BRCA1.** There are also two data sets for the influenza protein HA, but these were from different strains, so not directly comparable. To assess the reproducibility of DMS and its viability as a benchmark, we calculated Spearman's correlation coefficient between the functional scores of each DMS set in the same protein. Our results (Table EV3) demonstrate a **range of correlations from 0.94 (bla(a)/(b)) to 0.34 (PTEN(a)/(b)). The average correlations observed over all pairs of analyses were 0.66.** Some level of variance is expected due to differences in experimental method, fitness assays and conditions between experiments. Overall, the moderately high correlations suggest that DMS scores constitute a reasonably robust benchmark despite differing experimental [conditions]." — Livesey BJ, Marsh JA, *Mol Syst Biol* 2020;16(7):e9380, DOI 10.15252/msb.20199380 — [PMC7336272](https://pmc.ncbi.nlm.nih.gov/articles/PMC7336272/) (PMID 32627955)
- Same paper, how multi-dataset proteins were handled downstream: "Where multiple DMS data sets are present for a single protein, we averaged the normalised correlations of each predictor between these data sets, and treated the resulting values as scores from a single protein." `[READ-FROM-SOURCE]`
- **The 2023 update, which revises the picture for different assays** (`[READ-FROM-SOURCE]`): "Many DMS datasets provide multiple scores covering different experimental conditions and sometimes entirely different fitness assays of the same protein … We calculated the absolute Spearman's correlations between these score sets in the same protein to gauge the reproducibility of DMS results under different conditions. **The strongest correlations (> 0.9) were between experiments in extremely similar conditions, while assays investigating fitness under highly varying experimental conditions or using alternate fitness metrics often resulted in much lower correlations (< 0.3). Most correlations observed between alternative assays were in a range between 0.4 and 0.6 (median 0.54; Table EV3)**, which is similar to the level of correlation between DMS and the top VEPs in our previous study." — Livesey BJ, Marsh JA, "Updated benchmarking of variant effect predictors using deep mutational scanning", *Mol Syst Biol* 2023;19(8):e11474, DOI 10.15252/msb.202211474 — [PMC10407742](https://pmc.ncbi.nlm.nih.gov/articles/PMC10407742/) (PMID 37310135)
- Related, for a VEP-side ceiling if needed (`[READ-FROM-SOURCE]`): "The strongest correlations approached ρ = 0.8 for some DMS datasets (GCH1, PPARG, GDI1), while several others demonstrated relatively poor correlations even for the best-performing VEPs around ρ = 0.3 (LDLRAP1, TPK1). **The average correlation of the top-performing predictors for each protein was 0.58.**" — Livesey & Marsh, "Variant effect predictor correlation with functional assays is reflective of clinical classification performance", *Genome Biology* 2025;26:60, DOI 10.1186/s13059-025-03575-w — [PMC12016141](https://pmc.ncbi.nlm.nih.gov/articles/PMC12016141/) (PMID 40264194)
- The most recent paper in this line, relevant to assay-vs-predictor disagreement (`[READ-FROM-SOURCE]`, same text, no 0.34/0.66 figures in it): "MAVEs … are limited by experimental noise and the choice of assay, which may not capture all disease-relevant mechanisms. Expanding the use of MAVEs to assay distinct phenotypes is critical. **A single assay may miss important variant effects.** For example, VAMP-seq may overlook catalytic impairment at active sites." — Livesey & Marsh et al., "Why variant effect predictors and multiplexed assays agree and disagree", *Nature Communications* 2026, DOI 10.1038/s41467-026-77211-x — [PMC13620131](https://pmc.ncbi.nlm.nih.gov/articles/PMC13620131/) (PMID 42805995)

### Inferences
- `[INFERENCE]` **Correct the framing in the thesis.** "0.34–0.94, average 0.66" is *inter-study reproducibility of the same nominal measurement on the same protein* (Livesey & Marsh 2020, n = pairs drawn from 4 proteins — bla, UBI4, PTEN, BRCA1), and the authors themselves read it optimistically ("reasonably robust benchmark"). It is **not** a cross-assay-type ceiling. If the argument needs a cross-assay ceiling, the defensible number is the 2023 update's **median 0.54, mostly 0.4–0.6, <0.3 across strongly differing conditions**.
- `[INFERENCE]` Used carefully, this is a strong argument for a residue-level degron thesis: if two independent measurements of the same protein agree at only ρ≈0.34–0.66 (and alternative assays at ~0.54), then a competitor's single-random-hold-out ρ of 0.94 on one assay is measuring **memorisation of one assay's idiosyncrasies**, not the biology — all the more so given the measured 4.09% exact-duplicate leakage in Degformer's split (Q4) and the ≤3.98-unit internal disagreement in its own training labels (Q3).

### Gaps
- The per-pair numbers behind "0.34–0.94" live in **Table EV3** of the 2020 paper (and the 2023 paper's own Table EV3 for the median 0.54); I read the main-text statements, not the supplementary tables, so individual protein-pair values are not quoted here.
- Neither paper gives a confidence interval or n for the "average 0.66" figure; from the text it is an unweighted mean over pairs from only four proteins, so it should be cited as indicative, not as a precise ceiling.
