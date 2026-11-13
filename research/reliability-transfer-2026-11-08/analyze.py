"""CPU-only diagnostics of stored predictions. Never imports a model runtime.

Run: .venv/bin/python -I research/reliability-transfer-2026-11-08/analyze.py
All writes are confined to this directory; upstream inputs are hashed twice.
"""
from __future__ import annotations

import os
for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "2"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from collections import defaultdict
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path, PureWindowsPath
import platform
import resource
import subprocess
import sys
import time

import numpy as np
import pandas as pd
import scipy
import sklearn
from sklearn.metrics import average_precision_score, roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
DATA = ROOT / "data/processed/v3-fullpsi"
ROAD = ROOT / "research/kaggle-roadmap-2026-10-31"
LOCAL = ROAD / "output/local/ef138c84579c842e"
TZ = timezone(timedelta(hours=8))
META = ["peptide_id", "group_id", "outer_fold", "psi_stratum", "dpsi_mean"]
FORBIDDEN = {"torch", "transformers", "cupy", "tensorflow", "jax"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def clean(value):
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [clean(v) for v in value]
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def write_json(name, value):
    (HERE / name).write_text(json.dumps(clean(value), ensure_ascii=False, indent=2,
                                       allow_nan=False) + "\n", encoding="utf8")


class Inventory:
    def __init__(self):
        self.files = {}

    def source(self, path, expected=None, authority="observed_current_bytes"):
        path = Path(path).resolve()
        require(path.is_relative_to(ROOT), f"Input outside repository: {path}")
        require(path.is_file() and path.stat().st_size > 0, f"Missing/empty input: {path}")
        key = path.relative_to(ROOT).as_posix()
        if key not in self.files:
            self.files[key] = dict(bytes=path.stat().st_size, sha256=sha(path), authorities=[])
        record = self.files[key]
        if expected:
            require(record["sha256"] == expected["sha256"], f"SHA mismatch: {key}")
            require("bytes" not in expected or record["bytes"] == expected["bytes"], f"Size mismatch: {key}")
        if authority not in record["authorities"]:
            record["authorities"].append(authority)
        return path

    def read_json(self, path, **kwargs):
        return json.loads(self.source(path, **kwargs).read_text(encoding="utf8"))

    def verify_unchanged(self):
        for name, record in self.files.items():
            path = ROOT / name
            require(path.stat().st_size == record["bytes"] and sha(path) == record["sha256"],
                    f"Input changed during analysis: {name}")


def rank_order(prediction, peptide, ids, seed=1729):
    keys = [hashlib.sha256(json.dumps([seed, str(peptide), str(c)], ensure_ascii=False,
                                    separators=(",", ":")).encode()).hexdigest() for c in ids]
    return np.lexsort((np.asarray(keys), -np.asarray(prediction, float)))


def cluster_ci(rows, column, config, multiplicity=1):
    part = rows[["group_id", column]].dropna()
    if part.empty:
        return dict(delta=None, ci95=None, ci_adjusted=None, peptides=0, groups=0,
                    reason="no_eligible_peptides")
    group = part.groupby("group_id", sort=True)[column].agg(["sum", "count"])
    result = dict(delta=float(part[column].mean()), peptides=len(part), groups=len(group),
                  multiplicity=multiplicity, replicates=config["bootstrap_replicates"])
    if len(group) < 2:
        return dict(**result, ci95=None, ci_adjusted=None, reason="fewer_than_two_groups")
    rng = np.random.default_rng(config["bootstrap_seed"])
    draws = []
    for start in range(0, config["bootstrap_replicates"], 256):
        n = min(256, config["bootstrap_replicates"] - start)
        indices = rng.integers(0, len(group), size=(n, len(group)))
        draws.extend(group["sum"].to_numpy()[indices].sum(1) / group["count"].to_numpy()[indices].sum(1))
    q = .025 / multiplicity
    return dict(**result, ci95=np.quantile(draws, [.025, .975]).tolist(),
                ci_adjusted=np.quantile(draws, [q, 1-q]).tolist(), reason=None)


def peptide_metrics(frame, prediction="prediction", label="dpsi_mean", threshold=1., budget=10):
    require(not frame.cell_id.duplicated().any(), "Duplicate cells in metric population")
    require(np.isfinite(frame[[prediction, label]].to_numpy(float)).all(), "Nonfinite metric input")
    result = []
    for peptide, part in frame.groupby("peptide_id", sort=True):
        require(part.group_id.nunique() == 1, "Peptide has multiple groups")
        y, p = part[label].to_numpy(float), part[prediction].to_numpy(float)
        row = dict(peptide_id=peptide, group_id=part.group_id.iloc[0], cells=len(part),
                   psi_stratum=part.psi_stratum.iloc[0], outer_fold=int(part.outer_fold.iloc[0]),
                   mae=float(np.abs(p-y).mean()), rmse=float(np.sqrt(np.square(p-y).mean())),
                   zero_mae=float(np.abs(y).mean()), signed_error_micro_within_peptide=float((p-y).mean()))
        row["model_minus_zero_mae"] = row["mae"] - row["zero_mae"]
        for direction, hit, score in [("plus", y >= threshold, p), ("minus", y <= -threshold, -p)]:
            order = rank_order(score, peptide, part.cell_id.to_numpy())
            k = min(budget, len(part))
            count = int(hit.sum())
            eligible = min(count, len(hit)-count) >= 3
            row.update({"precision10_"+direction: float(hit[order[:k]].mean()),
                        "hits10_"+direction: int(hit[order[:k]].sum()),
                        "prevalence_"+direction: float(hit.mean()), "budget10": k,
                        "auroc_"+direction: float(roc_auc_score(hit, score)) if eligible else np.nan,
                        "ap_"+direction: float(average_precision_score(hit, score)) if eligible else np.nan,
                        "event_metric_null_reason_"+direction: None if eligible else "fewer_than_three_events_or_nonevents"})
        result.append(row)
    return pd.DataFrame(result)


def summary(rows):
    out = dict(cells=int(rows.cells.sum()), peptides=len(rows), groups=int(rows.group_id.nunique()),
               selections=int(rows.budget10.sum()))
    for key in ["mae", "rmse", "zero_mae", "model_minus_zero_mae", "precision10_plus", "precision10_minus",
                "prevalence_plus", "prevalence_minus", "auroc_plus", "ap_plus", "auroc_minus", "ap_minus"]:
        out[key] = float(rows[key].mean()) if rows[key].notna().any() else None
        if key.startswith(("auroc", "ap_")):
            out[key+"_eligible_peptides"] = int(rows[key].notna().sum())
    out["hits10_plus"] = int(rows.hits10_plus.sum())
    out["hits10_minus"] = int(rows.hits10_minus.sum())
    return out


def contrast(a, b, metric, config, multiplicity=1):
    pairs = a[["peptide_id", "group_id", metric]].merge(
        b[["peptide_id", "group_id", metric]], on="peptide_id", how="outer",
        suffixes=("_a", "_b"), validate="one_to_one", indicator=True)
    require((pairs._merge == "both").all(), "Different peptide cohorts in paired contrast")
    require((pairs.group_id_a == pairs.group_id_b).all(), "Group mismatch in contrast")
    pairs["group_id"] = pairs.group_id_a
    pairs["difference"] = pairs[metric+"_a"] - pairs[metric+"_b"]
    return cluster_ci(pairs, "difference", config, multiplicity)


def nearest_similarity(query, reference):
    """Aligned identity and unique-query 5-mer coverage; no homology claim."""
    require(len(reference) > 0, "Empty similarity reference")
    ref = reference.sort_values("peptide_id")
    rseq = np.asarray([list(s.encode("ascii")) for s in ref.wt_sequence], dtype=np.uint8)
    require(rseq.shape[1] == 28, "Reference length is not 28")
    ref_kmers = [set(s[i:i+5] for i in range(24)) for s in ref.wt_sequence]
    out = []
    for row in query.itertuples(index=False):
        seq = np.frombuffer(row.wt_sequence.encode("ascii"), dtype=np.uint8)
        require(len(seq) == 28, "Query length is not 28")
        identical = (rseq == seq).mean(1)
        best = int(np.argmax(identical))
        kmers = set(row.wt_sequence[i:i+5] for i in range(24))
        coverage = [len(kmers & k) / len(kmers) for k in ref_kmers]
        out.append(dict(peptide_id=row.peptide_id, max_aligned_identity=float(identical[best]),
                        nearest_peptide_id=ref.peptide_id.iloc[best],
                        max_query_5mer_coverage=float(max(coverage)), reference_peptides=len(ref)))
    return pd.DataFrame(out)


def exact_sequence_audit(sat, scan):
    owners = {}
    duplicates = 0
    for f in [sat, scan]:
        wt = f[["wt_sequence", "group_id"]].drop_duplicates()
        for seq, group in list(wt.itertuples(index=False, name=None)) + list(
                f[["mutant_sequence", "group_id"]].itertuples(index=False, name=None)):
            if seq in owners:
                require(owners[seq] == group, "Exact WT/mutant sequence assigned to different groups")
                duplicates += 1
            else:
                owners[seq] = group
    return dict(unique_sequences=len(owners), same_group_repeated_sequence_records=duplicates,
                cross_group_exact_sequences=0, scope="WT and measured mutants across W and all scanning partitions")


def calibration_tables(frame, recipe, cohort, config):
    pcols = ["p_minus", "p_neutral", "p_plus"]
    probs = frame[pcols].to_numpy(float)
    require(np.isfinite(probs).all() and (probs >= 0).all() and (probs <= 1).all(), "Invalid probability")
    require(np.allclose(probs.sum(1), 1., atol=1e-12, rtol=0), "Probabilities do not sum to 1")
    y = frame.dpsi_mean.to_numpy()
    classes = np.where(y <= -1, 0, np.where(y >= 1, 2, 1))
    brier = np.square(probs - np.eye(3)[classes]).sum(1)
    rows, bins = [], []
    for axis, value, ix in [("all", "all", np.ones(len(frame), bool))] + [
            ("psi_stratum", str(s), (frame.psi_stratum == s).to_numpy()) for s in sorted(frame.psi_stratum.unique())]:
        f = frame.loc[ix]
        row = dict(recipe=recipe, cohort=cohort, axis=axis, value=value, cells=int(ix.sum()),
                   peptides=f.peptide_id.nunique(), groups=f.group_id.nunique(),
                   brier_micro=float(brier[ix].mean()),
                   brier_macro=float(pd.Series(brier[ix]).groupby(f.peptide_id.to_numpy()).mean().mean()),
                   log_loss_micro=float(-np.log(np.clip(probs[ix, classes[ix]], config["log_epsilon"], 1)).mean()))
        for direction, ci in [("minus", 0), ("plus", 2)]:
            event, prob = classes[ix] == ci, probs[ix, ci]
            bi = np.minimum((prob * config["ece_bins"]).astype(int), config["ece_bins"]-1)
            ece = 0.
            for j in range(config["ece_bins"]):
                keep = bi == j
                bf = f.iloc[np.flatnonzero(keep)]
                observed = float(event[keep].mean()) if keep.any() else None
                meanp = float(prob[keep].mean()) if keep.any() else None
                if keep.any():
                    ece += keep.mean() * abs(observed-meanp)
                bins.append(dict(recipe=recipe, cohort=cohort, axis=axis, value=value, direction=direction,
                                 bin=j, lower=j/config["ece_bins"], upper=(j+1)/config["ece_bins"],
                                 cells=int(keep.sum()), peptides=bf.peptide_id.nunique(), groups=bf.group_id.nunique(),
                                 observed_rate=observed, mean_probability=meanp,
                                 null_reason=None if keep.any() else "empty_bin"))
            row.update({"observed_rate_"+direction: float(event.mean()),
                        "mean_probability_"+direction: float(prob.mean()),
                        "probability_bias_"+direction: float(prob.mean()-event.mean()), "ece_"+direction: float(ece)})
        rows.append(row)
    return rows, bins


def main():
    started, cpu_started = time.monotonic(), time.process_time()
    config = json.loads((HERE/"config.json").read_text())
    require(config["gpu_allowed"] is False and config["training_allowed"] is False
            and config["model_deserialization_allowed"] is False, "CPU analysis contract changed")
    inventory = Inventory()
    data_manifest = inventory.read_json(DATA/"DATA_MANIFEST.json")
    require(sha(DATA/"DATA_MANIFEST.json") == config["data_identity"], "Data identity changed")
    entries = {x["path"]: x for x in data_manifest["files"]}
    for name, item in entries.items():
        inventory.source(DATA/name, item, "DATA_MANIFEST.json")
    previous = inventory.read_json(ROOT/"research/oof-prioritization-2026-11-07/input-manifest.json")
    for name, item in previous["sources"].items():
        inventory.source(ROOT/name, item, "prioritization-input-manifest")
    original = inventory.read_json(ROAD/"local-output-analysis.json")
    kaggle = inventory.read_json(ROAD/"output/official/369cb2fe6a1e31e0/pipeline-manifest.json")
    state = inventory.read_json(LOCAL/"state.json")
    for path in [HERE/"config.json", HERE/"PROTOCOL.md", ROAD/"EXECUTION-PROTOCOL.md",
                 ROAD/"degron_v3/stages.py", ROOT/"research/full-data-audit/build_psi.py"]:
        inventory.source(path)

    def local_file(job, filename):
        record = state["jobs"][job]
        require(record["status"] == "complete", f"Job incomplete: {job}")
        origin = LOCAL.parent / PureWindowsPath(record["artifact_campaign"]).name if record.get("artifact_campaign") else LOCAL
        require(origin.name in {LOCAL.name, "e7097449883a51d8"}, "Unexpected artifact lineage")
        relative = f"jobs/{job}/{filename}"
        entry = next(x for x in record["files"] if x["path"] == relative)
        return inventory.source(origin/relative, entry, "campaign-state:"+job)

    kentries = {x["path"]: x for task in kaggle["tasks"].values() if task["status"] == "complete" for x in task["files"]}
    w5path = "tasks/01-78cc356ba4f4/ordered-w5-D-oof.parquet"
    w5path = inventory.source(ROAD/"output/official/369cb2fe6a1e31e0"/w5path, kentries[w5path], "Kaggle pipeline-manifest")
    sat = pd.read_parquet(DATA/"tables/saturation-cells.parquet")
    wide = pd.read_parquet(DATA/"splits/wide-outer.parquet")
    sat = sat.merge(wide, on=["peptide_id", "group_id", "psi_stratum"], validate="many_to_one")
    sat = sat.set_index("cell_id", drop=False).sort_index()
    require(dict(cells=len(sat), peptides=sat.peptide_id.nunique(), groups=sat.group_id.nunique()) == config["expected_W"], "Wrong W cohort")
    require(np.allclose(sat.dpsi_mean, (sat.dpsi_a+sat.dpsi_b)/2, atol=1e-12, rtol=0), "Mean label mismatch")
    require(sat.groupby("group_id").outer_fold.nunique().max() == 1, "Outer group crosses folds")
    split_checks = []
    for seed in config["seeds"]:
        f = pd.read_parquet(DATA/f"splits/inner-seed{seed}.parquet")
        require(not f.duplicated(["outer_fold", "group_id"]).any(), "Multiple group roles")
        for fold, part in f.groupby("outer_fold"):
            test = set(part.loc[part.role == "test", "group_id"])
            require(test == set(sat.loc[sat.outer_fold == fold, "group_id"]), "Test assignment mismatch")
            require(not test & set(part.loc[part.role != "test", "group_id"]), "Role overlap")
            split_checks.append(dict(seed=seed, fold=int(fold), groups_by_role=part.groupby("role").group_id.nunique().to_dict()))
    scan = pd.read_parquet(DATA/"tables/scanning-cells.parquet")
    exact = exact_sequence_audit(sat, scan)
    print("PASS input hashes, group roles and exact-sequence audit", flush=True)

    outputs = {}
    def csv(name, rows):
        f = rows if isinstance(rows, pd.DataFrame) else pd.DataFrame(rows)
        f.to_csv(HERE/name, index=False, float_format="%.12g")
        outputs[name] = dict(rows=len(f), columns=f.columns.tolist())

    scan_pairs = set(scan.scan_pair)
    require(len(scan_pairs) == 20, "Scanning design changed")
    masks = {"W-full": np.ones(len(sat), bool), "W-mutant-RAS": sat.mut_aa.isin(list("RAS")).to_numpy(),
             "W-scanning-pairs": (sat.wt_aa+sat.mut_aa).isin(scan_pairs).to_numpy()}
    predictions, metrics, performance, pp_all, precision_audit = {}, {}, [], [], []
    for recipe in config["recipes"]:
        path = w5path if recipe == "ordered-w5-D" else local_file("collect-core", recipe+"-oof.parquet")
        frame = pd.read_parquet(path)
        require(set(frame.seed) == set(config["seeds"]), "Incomplete OOF seeds")
        require(set(frame["mode"]) == {"official"} and set(frame.data_identity) == {config["data_identity"]}, "OOF identity/mode mismatch")
        require(set(frame.recipe) == {recipe}, "Wrong OOF recipe")
        require(not frame.duplicated(["seed", "cell_id"]).any(), "Duplicate seed/cell")
        pred = {}
        for seed in config["seeds"]:
            f = frame[frame.seed == seed].set_index("cell_id").sort_index()
            require(f.index.equals(sat.index), "OOF cohort gap")
            pd.testing.assert_frame_equal(f[META], sat[META], check_dtype=False, check_exact=True)
            require(np.isfinite(f.prediction).all(), "Nonfinite OOF")
            pred[f"seed{seed}"] = f.prediction.to_numpy(dtype=float)
        pred["ensemble"] = np.mean(list(pred.values()), axis=0)
        native = frame.groupby("cell_id").prediction.mean().reindex(sat.index).to_numpy(dtype=float)
        precision_audit.append(dict(recipe=recipe, stored_dtype=str(frame.prediction.dtype),
                                   ensemble_accumulation="float64", max_abs_difference_from_native_groupby=float(np.max(np.abs(native-pred["ensemble"])))),
                              )
        predictions[recipe] = pred
        for prediction_set, p in pred.items():
            for cohort, mask in masks.items():
                if prediction_set != "ensemble" and cohort != "W-full":
                    continue
                f = sat.loc[mask].copy(); f["prediction"] = p[mask]
                pp = peptide_metrics(f)
                metrics[recipe, prediction_set, cohort] = pp
                pp_all.append(pp.assign(recipe=recipe, prediction_set=prediction_set, cohort=cohort))
                performance.append(dict(recipe=recipe, prediction_set=prediction_set, cohort=cohort, axis="all", value="all", **summary(pp)))
                if prediction_set == "ensemble":
                    for axis in ["psi_stratum", "outer_fold"]:
                        for value, sub in pp.groupby(axis, sort=True):
                            performance.append(dict(recipe=recipe, prediction_set=prediction_set, cohort=cohort,
                                                    axis=axis, value=str(value), **summary(sub)))
        if recipe != "ordered-w5-D":
            require(abs(metrics[recipe, "ensemble", "W-full"].mae.mean()-original["local_recipes"][recipe]["ensemble"]["all"]["mae"]) < 2e-8,
                    "Stored development MAE cannot be reproduced")
        print("METRICS", recipe, flush=True)

    contrasts = []
    for a, b in [("esm2_35m-lora-B", "esm2_35m-frozen-B"), ("esm2_35m-lora-D", "esm2_35m-frozen-D"),
                 ("esm2_35m-lora-D", "ordered-w5-D")]:
        for cohort in masks:
            pa, pb = metrics[a, "ensemble", cohort], metrics[b, "ensemble", cohort]
            for metric in ["mae", "auroc_plus", "precision10_plus", "precision10_minus"]:
                mult = 4 if cohort == "W-full" and b != "ordered-w5-D" and metric in ["mae", "auroc_plus"] else 1
                contrasts.append(dict(a=a, b=b, cohort=cohort, axis="all", value="all", metric=metric,
                                      inference="original_family_replay" if mult == 4 else "descriptive_posthoc",
                                      **contrast(pa, pb, metric, config, mult)))
            for axis in ["psi_stratum", "outer_fold"]:
                for value, sub in pa.groupby(axis, sort=True):
                    other = pb[pb[axis] == value]
                    contrasts.append(dict(a=a, b=b, cohort=cohort, axis=axis, value=str(value), metric="mae",
                                          inference="descriptive_posthoc", **contrast(sub, other, "mae", config)))

    # Similarity uses the actual arm's outer-refit cohort, without modifying any fit.
    peptides = sat[["peptide_id", "group_id", "wt_sequence", "psi_wt_sat", "outer_fold"]].drop_duplicates().reset_index(drop=True)
    similarities = []
    for arm in ["B", "D"]:
        for fold in range(5):
            query = peptides[peptides.outer_fold == fold]
            ref = peptides[peptides.outer_fold != fold]
            if arm == "B":
                ref = ref[ref.psi_wt_sat <= 4]
            require(not set(query.group_id) & set(ref.group_id), "Similarity reference sees test group")
            similarities.append(nearest_similarity(query, ref).assign(cohort="W", arm=arm, outer_fold=fold))
    sim = pd.concat(similarities, ignore_index=True)
    similarity_metrics = []
    for arm in ["B", "D"]:
        s = sim[(sim.cohort == "W") & (sim.arm == arm)]
        a = metrics[f"esm2_35m-lora-{arm}", "ensemble", "W-full"].merge(s, on=["peptide_id", "outer_fold"], validate="one_to_one")
        b = metrics[f"esm2_35m-frozen-{arm}", "ensemble", "W-full"].set_index("peptide_id")
        a["difference"] = a.mae-a.peptide_id.map(b.mae)
        a["identity_bin"] = pd.cut(a.max_aligned_identity, config["identity_bins"], right=False).astype(str)
        for value, sub in a.groupby("identity_bin", sort=True):
            similarity_metrics.append(dict(arm=arm, identity_bin=value, mean_identity=sub.max_aligned_identity.mean(),
                                           max_5mer_coverage=sub.max_query_5mer_coverage.max(),
                                           **cluster_ci(sub, "difference", config)))

    # Replicate sensitivity retains fixed scores and candidate pools.
    disagreement = sat.replicate_disagreement.to_numpy()
    require(np.allclose(disagreement, np.abs(sat.dpsi_a-sat.dpsi_b), atol=1e-12, rtol=0), "Disagreement metadata mismatch")
    label_agreement, threshold_rows, noise_rows = [], [], []
    for threshold in config["effect_thresholds"]:
        for direction, sign in [("plus", 1), ("minus", -1)]:
            ha = sign*sat.dpsi_a.to_numpy() >= threshold
            hb = sign*sat.dpsi_b.to_numpy() >= threshold
            hm = sign*sat.dpsi_mean.to_numpy() >= threshold
            for value in ["all", *sorted(sat.psi_stratum.unique())]:
                ix = np.ones(len(sat), bool) if value == "all" else (sat.psi_stratum == value).to_numpy()
                union = (ha | hb)[ix].sum()
                label_agreement.append(dict(threshold=threshold, direction=direction, psi_stratum=value,
                                            cells=int(ix.sum()), peptides=sat.loc[ix].peptide_id.nunique(),
                                            prevalence_mean=float(hm[ix].mean()), event_xor_rate=float((ha[ix] != hb[ix]).mean()),
                                            event_jaccard=float((ha & hb)[ix].sum()/union) if union else None,
                                            no_event_in_either_half=not bool(union), consensus_rate=float((ha & hb)[ix].mean())))
            labels = {"mean": hm, "half_a": ha, "half_b": hb, "both_halves": ha & hb}
            for recipe, pred in predictions.items():
                for peptide, part in sat.groupby("peptide_id", sort=True):
                    positions = sat.index.get_indexer(part.index)
                    order = rank_order(sign*pred["ensemble"][positions], peptide, part.cell_id.to_numpy(), config["tie_seed"])
                    chosen = positions[order[:min(config["budget_per_peptide"], len(part))]]
                    for target, hit in labels.items():
                        threshold_rows.append(dict(recipe=recipe, threshold=threshold, direction=direction, target=target,
                                                   peptide_id=peptide, group_id=part.group_id.iloc[0], cells=len(part), selected=len(chosen),
                                                   precision=float(hit[chosen].mean()), prevalence=float(hit[positions].mean())))
    tr = pd.DataFrame(threshold_rows)
    threshold_summary = []
    for key, sub in tr.groupby(["recipe", "threshold", "direction", "target"], sort=True):
        threshold_summary.append(dict(zip(["recipe", "threshold", "direction", "target"], key),
                                      prevalence_macro=sub.prevalence.mean(), selections=int(sub.selected.sum()),
                                      **cluster_ci(sub, "precision", config)))
    threshold_contrasts = []
    for key, part in tr.groupby(["threshold", "direction", "target"], sort=True):
        for a, b in [("esm2_35m-lora-D", "ordered-w5-D"), ("esm2_35m-lora-D", "esm2_35m-frozen-D"),
                     ("esm2_35m-lora-B", "esm2_35m-frozen-B")]:
            pa, pb = part[part.recipe == a], part[part.recipe == b]
            threshold_contrasts.append(dict(zip(["threshold", "direction", "target"], key), a=a, b=b,
                                           inference="descriptive_posthoc_not_globally_adjusted",
                                           **contrast(pa, pb, "precision", config)))
    seed_contrasts = []
    for seed in config["seeds"]:
        for arm in ["B", "D"]:
            a = metrics[f"esm2_35m-lora-{arm}", f"seed{seed}", "W-full"]
            b = metrics[f"esm2_35m-frozen-{arm}", f"seed{seed}", "W-full"]
            for metric in ["mae", "auroc_plus", "precision10_plus"]:
                seed_contrasts.append(dict(seed=seed, arm=arm, metric=metric,
                                           **contrast(a, b, metric, config)))
    bins = pd.cut(disagreement, config["disagreement_bins"], right=False).astype(str)
    for recipe, pred in predictions.items():
        f = sat.assign(error=np.abs(pred["ensemble"]-sat.dpsi_mean), disagreement_bin=bins)
        for value, sub in f.groupby("disagreement_bin", observed=True):
            p = sub.groupby(["peptide_id", "group_id"], as_index=False).agg(mae=("error", "mean"))
            noise_rows.append(dict(recipe=recipe, disagreement_bin=value, cells=len(sub),
                                   **cluster_ci(p, "mae", config)))
    lower, upper = 1-sat.psi_wt_sat.to_numpy(), 6-sat.psi_wt_sat.to_numpy()
    require(((sat.dpsi_mean.to_numpy() >= lower-1e-7) & (sat.dpsi_mean.to_numpy() <= upper+1e-7)).all(), "Observed labels violate assay bounds")
    bounds = []
    for recipe, pred in predictions.items():
        p = pred["ensemble"]
        for value in ["all", *sorted(sat.psi_stratum.unique())]:
            ix = np.ones(len(sat), bool) if value == "all" else (sat.psi_stratum == value).to_numpy()
            bounds.append(dict(recipe=recipe, psi_stratum=value, cells=int(ix.sum()),
                               prediction_outside_measured_WT_bounds_rate=float(((p < lower-1e-7) | (p > upper+1e-7))[ix].mean())))
    print("PASS similarity and replicate/threshold diagnostics", flush=True)

    # Transfer is diagnostic on the previously inspected T, with its locked score unchanged.
    transfer = pd.read_parquet(local_file("locked-transfer-w5", "ordered-w5-D/held-scanning.parquet"))
    require(dict(cells=len(transfer), peptides=transfer.peptide_id.nunique(), groups=transfer.group_id.nunique()) == config["expected_T"], "Wrong T cohort")
    require(not transfer.cell_id.duplicated().any(), "Duplicate T cell")
    require(np.isfinite(transfer.dpsi_rep1).all(), "Primary T missing rep1")
    require(np.array_equal(transfer.dpsi_mean, transfer.dpsi_rep1), "T target changed from rep1")
    require(not set(transfer.group_id) & set(sat.group_id), "T/W group overlap")
    require(not set(transfer.group_id) & set(scan.loc[scan.partition == "scan_dev", "group_id"]), "T/dev overlap")
    canonical = scan.set_index("cell_id").loc[transfer.cell_id]
    for col in ["group_id", "peptide_id", "wt_aa", "mut_aa", "dpsi_rep1", "dpsi_rep2", "dpsi_rep12_mean", "partition"]:
        pd.testing.assert_series_equal(transfer[col].reset_index(drop=True), canonical[col].reset_index(drop=True), check_names=False, check_dtype=False, check_exact=True)
    require(set(transfer.partition) == {"scan_T"}, "Wrong scanning partition")
    transfer["outer_fold"] = -1
    require(transfer.psi_stratum.notna().all(), "Missing T PSI stratum")
    ts = nearest_similarity(transfer[["peptide_id", "wt_sequence"]].drop_duplicates(), peptides).assign(cohort="T", arm="D", outer_fold=-1)
    csv("similarity.csv", pd.concat([sim, ts], ignore_index=True))
    transfer_contrasts = []
    available = transfer.dpsi_rep1.notna() & transfer.dpsi_rep2.notna()
    tcohorts = {"T-rep1-full": (transfer, "dpsi_rep1"),
                "T-intersection-rep1": (transfer.loc[available], "dpsi_rep1"),
                "T-intersection-rep2": (transfer.loc[available], "dpsi_rep2"),
                "T-intersection-mean12": (transfer.loc[available], "dpsi_rep12_mean")}
    for cohort, (f, label) in tcohorts.items():
        pp = peptide_metrics(f, label=label)
        metrics["ordered-w5-D", "locked-final", cohort] = pp
        pp_all.append(pp.assign(recipe="ordered-w5-D", prediction_set="locked-final", cohort=cohort))
        for axis in ["all", "psi_stratum"]:
            subsets = [("all", pp)] if axis == "all" else pp.groupby("psi_stratum", sort=True)
            for value, sub in subsets:
                performance.append(dict(recipe="ordered-w5-D", prediction_set="locked-final", cohort=cohort,
                                        axis=axis, value=value, **summary(sub)))
                transfer_contrasts.append(dict(cohort=cohort, axis=axis, value=value, metric="W5_minus_zero_mae",
                                               inference="descriptive_posthoc", **cluster_ci(sub, "model_minus_zero_mae", config)))
    for cohort in masks:
        pp = metrics["ordered-w5-D", "ensemble", cohort]
        for value, sub in [("all", pp), *list(pp.groupby("psi_stratum", sort=True))]:
            transfer_contrasts.append(dict(cohort=cohort, axis="all" if value == "all" else "psi_stratum", value=value,
                                           metric="W5_minus_zero_mae", inference="descriptive_posthoc", **cluster_ci(sub, "model_minus_zero_mae", config)))

    calibration, reliability = [], []
    for recipe in config["recipes"]:
        job = "locked-transfer-w5" if recipe == "ordered-w5-D" else "calibrate-core"
        cf = pd.read_parquet(local_file(job, recipe+"/calibrated-oof.parquet"))
        require(not cf.duplicated(["seed", "cell_id"]).any(), "Duplicate calibration OOF")
        require(set(cf.seed) == set(config["seeds"]), "Calibration missing seed")
        for seed, f in cf.groupby("seed"):
            f = f.set_index("cell_id").sort_index()
            require(f.index.equals(sat.index), "Calibration cohort gap")
            pd.testing.assert_frame_equal(f[META], sat[META], check_dtype=False, check_exact=True)
            require(np.array_equal(f.prediction, predictions[recipe][f"seed{seed}"]), "Calibrated/raw prediction mismatch")
        pcols = ["p_minus", "p_neutral", "p_plus"]
        f = sat.copy()
        f[pcols] = cf.groupby("cell_id")[pcols].mean().reindex(sat.index)
        rows, rb = calibration_tables(f, recipe, "W-full", config)
        calibration.extend(rows); reliability.extend(rb)
    rows, rb = calibration_tables(transfer, "ordered-w5-D", "T-rep1-full", config)
    calibration.extend(rows); reliability.extend(rb)

    csv("performance.csv", performance)
    csv("per-peptide.csv", pd.concat(pp_all, ignore_index=True))
    csv("similarity-contrasts.csv", similarity_metrics)
    csv("label-agreement.csv", label_agreement)
    csv("threshold-sensitivity.csv", threshold_summary)
    csv("threshold-contrasts.csv", threshold_contrasts)
    csv("seed-contrasts.csv", seed_contrasts)
    csv("disagreement-errors.csv", noise_rows)
    csv("prediction-bounds.csv", bounds)
    csv("calibration.csv", calibration)
    csv("reliability-bins.csv", reliability)
    # Per-peptide threshold rows aid independent validation; no cell predictions are duplicated.
    (HERE/"local").mkdir(exist_ok=True)
    tr.to_csv(HERE/"local/threshold-per-peptide.csv", index=False, float_format="%.12g")
    inventory.verify_unchanged()
    require(not FORBIDDEN & set(sys.modules), "Unexpected GPU/model runtime imported")
    limitations = [
        "Posthoc diagnostics on repeatedly examined development W and previously inspected held-source T.",
        "No LoRA predictions on T; no independent external validation, retraining, model inference or GPU execution.",
        "Similarity uses aligned 28-AA identity and query 5-mer coverage, not remote homology or pretrained-corpus audit.",
        "Bootstrap conditions on stored predictions; training/model-selection/outer-partition uncertainty is not included.",
        "New CI/strata/threshold diagnostics are descriptive and not globally multiplicity-adjusted.",
        "Half a/b consensus is a changed target, not a probability interval or an independent biological replicate.",
        "W subset masks do not match protein, assay, target replicate or full joint distribution to T.",
        "T rep1 versus rep2/mean12 is a paired label sensitivity on intersection, not a new locked test.",
        "Measured test WT PSI is used only for diagnostic strata/bounds; no clipping or new model input.",
        "Input hashes verify bytes and saved assignments, not original training execution or checkpoint tensor correctness.",
        "Normalized count support is not raw sequencing depth; replicate disagreement is not known measurement variance.",
        "No G2/G3 acceptance, serving promotion, software performance or wet-lab resource benefit is established."
    ]
    write_json("input-manifest.json", dict(status="pass", data_identity=config["data_identity"],
                files=inventory.files, file_count=len(inventory.files), bytes_checked=sum(x["bytes"] for x in inventory.files.values()),
                checked_again_after_analysis=True, split_checks=split_checks, exact_sequence_audit=exact,
                source_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), limitations=limitations))
    write_json("results.json", dict(experiment_id=config["experiment_id"], generated_at=datetime.now(TZ).isoformat(),
                scientific_status=config["scientific_status"], config_sha256=sha(HERE/"config.json"), protocol_sha256=sha(HERE/"PROTOCOL.md"),
                analysis_sha256=sha(Path(__file__)), input_manifest_sha256=sha(HERE/"input-manifest.json"),
                W=config["expected_W"], T=config["expected_T"], scan_pairs=sorted(scan_pairs),
                replicate=dict(pearson_a_b=float(sat.dpsi_a.corr(sat.dpsi_b)),
                               mean_absolute_disagreement=float(disagreement.mean()), median_absolute_disagreement=float(np.median(disagreement)),
                               support_min_a=float(sat.reads_a.min()), support_min_b=float(sat.reads_b.min()), support_unit="normalized_count_sum"),
                matched_and_utility_contrasts=contrasts, transfer_vs_zero=transfer_contrasts,
                T_replicate_intersection=dict(cells=int(available.sum()), peptides=transfer.loc[available].peptide_id.nunique(), groups=transfer.loc[available].group_id.nunique()),
                exact_sequence_audit=exact, outputs=outputs, limitations=limitations,
                numerical_precision=precision_audit,
                pending=dict(lora_T="not_evaluated_no_saved_predictions", independent_source="reviewed_compatible_source_not_supplied",
                             final_serving="outside_this_diagnostic_run", G2_G3="no_decision_changed")))
    write_json("runtime.json", dict(wall_seconds=time.monotonic()-started, cpu_seconds=time.process_time()-cpu_started,
                peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024, platform=platform.platform(),
                python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__, scipy=scipy.__version__, sklearn=sklearn.__version__,
                configured_cpu_threads=2, cuda_visible_devices=os.environ["CUDA_VISIBLE_DEVICES"],
                forbidden_model_runtimes_imported=sorted(FORBIDDEN & set(sys.modules)),
                training=False, inference=False, model_deserialization=False, gpu_execution=False))
    print("PASS CPU diagnostics complete; input files unchanged", flush=True)


if __name__ == "__main__":
    main()
