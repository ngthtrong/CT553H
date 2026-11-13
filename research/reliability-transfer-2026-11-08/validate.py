"""Validate the CPU diagnostic package with direct input calculations and edge cases.

Run only after analyze.py. Writes validation.json beside this script.
Does not import campaign metrics or any model/GPU runtime.
"""
import os
for _key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]:
    os.environ[_key] = "2"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import ast
from datetime import datetime, timezone, timedelta
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/"CLAUDE.md").exists())
ROAD = ROOT/"research/kaggle-roadmap-2026-10-31"
DATA = ROOT/"data/processed/v3-fullpsi"
LOCAL = ROAD/"output/local/ef138c84579c842e"


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def close(actual, expected, message, atol=1e-10):
    check(np.allclose(actual, expected, atol=atol, rtol=0, equal_nan=True), message)


def main():
    spec = importlib.util.spec_from_file_location("cpu_diagnostics", HERE/"analyze.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    config = json.loads((HERE/"config.json").read_text())
    result = json.loads((HERE/"results.json").read_text())
    inputs = json.loads((HERE/"input-manifest.json").read_text())
    runtime = json.loads((HERE/"runtime.json").read_text())
    checks = []
    check(result["config_sha256"] == digest(HERE/"config.json"), "Config changed")
    check(result["protocol_sha256"] == digest(HERE/"PROTOCOL.md"), "Protocol changed")
    check(result["analysis_sha256"] == digest(HERE/"analyze.py"), "Analysis code changed")
    check(result["input_manifest_sha256"] == digest(HERE/"input-manifest.json"), "Input manifest changed")
    for name, item in inputs["files"].items():
        path = ROOT/name
        check(path.stat().st_size == item["bytes"] and digest(path) == item["sha256"], f"Input changed: {name}")
    checks.append(dict(name="input_hashes_rechecked", files=len(inputs["files"])))
    for name, info in result["outputs"].items():
        f = pd.read_csv(HERE/name)
        check(len(f) == info["rows"] and list(f) == info["columns"], f"Output shape: {name}")
    checks.append(dict(name="all_declared_output_shapes", files=len(result["outputs"])))

    # CPU contract is supported by execution telemetry and a static import check.
    banned = {"torch", "transformers", "cupy", "tensorflow", "jax"}
    tree = ast.parse((HERE/"analyze.py").read_text())
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(x.name.split(".")[0] for x in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports & banned and not set(sys.modules) & banned, "Model runtime imported")
    check(runtime["gpu_execution"] is False and runtime["inference"] is False
          and runtime["training"] is False and runtime["model_deserialization"] is False, "Runtime contract")
    check(runtime["cuda_visible_devices"] == "" and runtime["forbidden_model_runtimes_imported"] == [], "GPU environment")
    checks.append(dict(name="cpu_only_contract", imported_model_runtimes=[]))

    # Formula tests cover macro estimand, unequal cluster sizes, missing classes,
    # event boundaries, short candidate lists, tie/row-order invariance and bins.
    toy = pd.DataFrame(dict(cell_id=["c3", "c1", "c2"], peptide_id=["p", "p", "q"],
                            group_id=["g", "g", "h"], psi_stratum=["le3"]*3,
                            outer_fold=[0]*3, dpsi_mean=[1., -1., 0.], prediction=[.9, -.8, .2]))
    m = mod.peptide_metrics(toy)
    close(m.mae.to_numpy(), [.15, .2], "Peptide macro grain")
    close(m.precision10_plus.to_numpy(), [.5, 0], "Threshold >=1 and N<k")
    close(m.precision10_minus.to_numpy(), [.5, 0], "Negative threshold <=-1")
    check(m.auroc_plus.isna().all(), "Ineligible AUROC must be null")
    close(mod.summary(m)["mae"], .175, "Macro != micro")
    try:
        mod.peptide_metrics(pd.concat([toy, toy.iloc[:1]], ignore_index=True))
        raise AssertionError("Duplicate was accepted")
    except ValueError:
        pass
    tie_ids = np.array(["d", "b", "a", "c"])
    first = tie_ids[mod.rank_order(np.ones(4), "p", tie_ids)]
    perm = np.array([3, 0, 2, 1])
    second = tie_ids[perm][mod.rank_order(np.ones(4), "p", tie_ids[perm])]
    check(np.array_equal(first, second), "Tie order changes with input row order")
    grouped = pd.DataFrame(dict(group_id=["a", "a", "b"], value=[1., 3., 9.]))
    ci = mod.cluster_ci(grouped, "value", config)
    close(ci["delta"], 13/3, "Peptide-macro point estimate changed to group-macro")
    rng = np.random.default_rng(config["bootstrap_seed"])
    members = [np.array([1., 3.]), np.array([9.])]
    draws = []
    for _ in range(config["bootstrap_replicates"]):
        choices = rng.integers(0, 2, 2)
        draws.append(np.concatenate([members[j] for j in choices]).mean())
    close(ci["ci95"], np.quantile(draws, [.025, .975]), "Unequal-cluster bootstrap")
    single = mod.cluster_ci(grouped.iloc[:2], "value", config)
    check(single["ci95"] is None and single["reason"] == "fewer_than_two_groups", "One-cluster CI")
    empty = mod.cluster_ci(grouped.iloc[:0], "value", config)
    check(empty["delta"] is None and empty["reason"] == "no_eligible_peptides", "Empty metric population")
    q = pd.DataFrame(dict(peptide_id=["x"], wt_sequence=["A"*28]))
    s = mod.nearest_similarity(q, pd.DataFrame(dict(peptide_id=["r"], wt_sequence=["A"*28])))
    close(s.max_aligned_identity.iloc[0], 1., "Identity exact match")
    close(s.max_query_5mer_coverage.iloc[0], 1., "5-mer exact match")
    synthetic = toy.copy()
    synthetic[["p_minus", "p_neutral", "p_plus"]] = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    cal, bins = mod.calibration_tables(synthetic, "toy", "toy", config)
    close(cal[0]["brier_micro"], 0, "Perfect multiclass Brier")
    close(cal[0]["ece_plus"], 0, "p=0/1 ECE endpoints")
    check(sum(b["cells"] for b in bins if b["axis"] == "all" and b["direction"] == "plus") == 3, "Bins lose p=1")
    check(all(b["null_reason"] == "empty_bin" for b in bins if b["cells"] == 0), "Empty-bin reason")
    checks.append(dict(name="meaningful_edge_cases", cases=["macro_grain", "N_below_budget", "event_boundaries", "AUROC_eligibility",
                       "duplicate_rejection", "tie_row_permutation", "unequal_cluster_sizes", "single_cluster", "empty_population",
                       "exact_sequence_similarity", "perfect_multiclass_probabilities", "p0_p1_and_empty_bins"]))

    sat = pd.read_parquet(DATA/"tables/saturation-cells.parquet").set_index("cell_id").sort_index()
    perf = pd.read_csv(HERE/"performance.csv")
    thresholds = pd.read_csv(HERE/"threshold-sensitivity.csv")
    pp = pd.read_csv(HERE/"per-peptide.csv")
    source_files = inputs["files"]
    independently_checked = []
    independent_consensus = {}
    for recipe in config["recipes"]:
        candidates = [ROOT/p for p in source_files if p.endswith("/"+recipe+"-oof.parquet")]
        check(len(candidates) == 1, "Ambiguous OOF provenance")
        f = pd.read_parquet(candidates[0])
        pred = f.prediction.astype(float).groupby(f.cell_id).mean().reindex(sat.index)
        independently = (pred-sat.dpsi_mean).abs().groupby(sat.peptide_id).mean()
        reported = perf[(perf.recipe == recipe) & (perf.prediction_set == "ensemble")
                        & (perf.cohort == "W-full") & (perf.axis == "all")].iloc[0]
        close(reported.mae, independently.mean(), f"Independent MAE: {recipe}")
        direct = {"mean": [], "both_halves": [], "half_a": [], "half_b": []}
        consensus_records = []
        selected_hits = 0
        for peptide, group in sat.groupby("peptide_id", sort=True):
            scores = pred.reindex(group.index).to_numpy()
            order = np.argsort(-scores, kind="stable")
            check(scores[order[9]] != scores[order[10]], "Independent selection requires no cutoff tie")
            selected = group.iloc[order[:10]]
            labels = {"mean": selected.dpsi_mean >= 1, "both_halves": (selected.dpsi_a >= 1) & (selected.dpsi_b >= 1),
                      "half_a": selected.dpsi_a >= 1, "half_b": selected.dpsi_b >= 1}
            selected_hits += int(labels["mean"].sum())
            consensus_records.append(dict(peptide_id=peptide, group_id=group.group_id.iloc[0],
                                          precision=float(labels["both_halves"].mean())))
            for key, value in labels.items():
                direct[key].append(value.mean())
        for target, values in direct.items():
            record = thresholds[(thresholds.recipe == recipe) & (thresholds.threshold == 1)
                                & (thresholds.direction == "plus") & (thresholds.target == target)].iloc[0]
            close(record.delta, np.mean(values), f"Independent threshold P10: {recipe}/{target}")
        close(reported.hits10_plus, selected_hits, f"Independent hit count: {recipe}")
        # Check every exact-scanning-pair mask against the independently read design.
        scan = pd.read_parquet(DATA/"tables/scanning-cells.parquet", columns=["scan_pair"])
        mask = (sat.wt_aa+sat.mut_aa).isin(set(scan.scan_pair))
        direct_subset = (pred[mask]-sat.loc[mask, "dpsi_mean"]).abs().groupby(sat.loc[mask, "peptide_id"]).mean().mean()
        reported_subset = perf[(perf.recipe == recipe) & (perf.prediction_set == "ensemble")
                               & (perf.cohort == "W-scanning-pairs") & (perf.axis == "all")].iloc[0]
        close(reported_subset.mae, direct_subset, "Directed-pair mask")
        independent_consensus[recipe] = pd.DataFrame(consensus_records).set_index("peptide_id")
        independently_checked.append(recipe)
    checks.append(dict(name="independent_raw_OOF_arithmetic", recipes=independently_checked,
                       calculations=["macro_MAE", "exact_20_pair_subset_MAE", "P10_mean_a_b_consensus", "hits10"]))

    original = json.loads((ROAD/"local-output-analysis.json").read_text())
    for arm in ["B", "D"]:
        recipe = f"esm2_35m-lora-{arm}"
        name = f"local:{recipe} minus local:esm2_35m-frozen-{arm}; mae"
        row = next(x for x in result["matched_and_utility_contrasts"] if x["a"] == recipe
                   and x["b"] == f"esm2_35m-frozen-{arm}" and x["cohort"] == "W-full"
                   and x["axis"] == "all" and x["metric"] == "mae")
        close(row["delta"], original["contrasts"][name]["delta"], "Original contrast delta", 2e-8)
        close(row["ci_adjusted"], original["contrasts"][name]["ci_adjusted"], "Original adjusted CI at float32 input precision", 2e-8)
    e5 = json.loads((ROOT/"research/oof-prioritization-2026-11-07/results.json").read_text())
    new = next(x for x in result["matched_and_utility_contrasts"] if x["a"] == "esm2_35m-lora-D"
               and x["b"] == "ordered-w5-D" and x["cohort"] == "W-full" and x["axis"] == "all"
               and x["metric"] == "precision10_plus")
    close(new["delta"], e5["primary_contrasts"][0]["delta"], "Existing E5 result changed")
    checks.append(dict(name="historical_results_reconciled", matched_MAE_CI_9875=2, E5_point_difference=True))

    # Independently obtain a consensus contrast CI from literal peptide rows.
    a = independent_consensus["esm2_35m-lora-D"]
    b = independent_consensus["ordered-w5-D"]
    delta = a.precision-b.precision
    group_members = [delta.loc[g.index].to_numpy() for _, g in a.groupby("group_id", sort=True)]
    rng = np.random.default_rng(config["bootstrap_seed"])
    draws = []
    for _ in range(config["bootstrap_replicates"]):
        ids = rng.integers(0, len(group_members), len(group_members))
        draws.append(np.concatenate([group_members[j] for j in ids]).mean())
    tcsv = pd.read_csv(HERE/"threshold-contrasts.csv")
    row = tcsv[(tcsv.threshold == 1) & (tcsv.direction == "plus") & (tcsv.target == "both_halves")
               & (tcsv.a == "esm2_35m-lora-D") & (tcsv.b == "ordered-w5-D")].iloc[0]
    close(row.delta, delta.mean(), "Independent consensus contrast delta")
    close(json.loads(row.ci95), np.quantile(draws, [.025, .975]), "Independent consensus paired CI", 1e-11)
    checks.append(dict(name="independent_consensus_paired_CI", replicates=len(draws)))

    tpath = next(ROOT/p for p in source_files if p.endswith("/held-scanning.parquet"))
    t = pd.read_parquet(tpath)
    for cohort, label, mask in [("T-rep1-full", "dpsi_rep1", np.ones(len(t), bool)),
                                ("T-intersection-mean12", "dpsi_rep12_mean", t.dpsi_rep2.notna().to_numpy())]:
        f = t.loc[mask]
        direct = (f.prediction-f[label]).abs().groupby(f.peptide_id).mean().mean()
        z = f[label].abs().groupby(f.peptide_id).mean().mean()
        saved = perf[(perf.cohort == cohort) & (perf.axis == "all")].iloc[0]
        close(saved.mae, direct, "T independent MAE")
        close(saved.zero_mae, z, "T independent zero MAE")
    # Independent bootstrap via literal peptide-membership arrays rather than sum/count aggregates.
    direct_t = t.assign(model_minus_zero_mae=(t.prediction-t.dpsi_rep1).abs()-t.dpsi_rep1.abs())
    per = direct_t.groupby(["peptide_id", "group_id"], as_index=False).model_minus_zero_mae.mean().sort_values("peptide_id")
    members = [g.model_minus_zero_mae.to_numpy() for _, g in per.groupby("group_id", sort=True)]
    rng = np.random.default_rng(config["bootstrap_seed"])
    draws = []
    for _ in range(config["bootstrap_replicates"]):
        choices = rng.integers(0, len(members), len(members))
        draws.append(np.concatenate([members[j] for j in choices]).mean())
    tc = next(x for x in result["transfer_vs_zero"] if x["cohort"] == "T-rep1-full" and x["axis"] == "all")
    close(tc["ci95"], np.quantile(draws, [.025, .975]), "Independent T cluster CI", 1e-11)
    checks.append(dict(name="independent_T_labels_MAE_zero_and_cluster_CI", bootstrap_replicates=len(draws)))

    calibration = pd.read_csv(HERE/"calibration.csv")
    for recipe in config["recipes"]:
        cp = next(ROOT/p for p in source_files if p.endswith("/"+recipe+"/calibrated-oof.parquet"))
        f = pd.read_parquet(cp)
        probs = f.groupby("cell_id")[["p_minus", "p_neutral", "p_plus"]].mean().reindex(sat.index).to_numpy()
        classes = np.where(sat.dpsi_mean <= -1, 0, np.where(sat.dpsi_mean >= 1, 2, 1))
        # Different algebra: sum(p^2)-2*p_true+1, rather than (p-one_hot)^2.
        errors = np.square(probs).sum(1)-2*probs[np.arange(len(sat)), classes]+1
        actual = calibration[(calibration.recipe == recipe) & (calibration.cohort == "W-full")
                             & (calibration.axis == "all")].iloc[0]
        close(actual.brier_micro, errors.mean(), "Independent W Brier")
        close(actual.brier_macro, pd.Series(errors).groupby(sat.peptide_id.to_numpy()).mean().mean(), "Independent macro Brier")
        if recipe != "ordered-w5-D":
            close(actual.brier_micro, original["calibration"][recipe]["multiclass_brier_cell_micro"], "Saved CV Brier")
    probs = t[["p_minus", "p_neutral", "p_plus"]].to_numpy()
    classes = np.where(t.dpsi_rep1 <= -1, 0, np.where(t.dpsi_rep1 >= 1, 2, 1))
    errors = np.square(probs).sum(1)-2*probs[np.arange(len(t)), classes]+1
    actual = calibration[(calibration.cohort == "T-rep1-full") & (calibration.axis == "all")].iloc[0]
    close(actual.brier_micro, errors.mean(), "Independent T Brier")
    close(actual.probability_bias_plus, probs[:, 2].mean()-(classes == 2).mean(), "Independent T probability bias")
    checks.append(dict(name="independent_multiclass_calibration", W_recipes=5, T=True, stored_cards_reconciled=4))

    # Correctness of source invariance is rechecked last as well.
    for name, item in inputs["files"].items():
        check(digest(ROOT/name) == item["sha256"], f"Input changed after validation: {name}")
    output_hashes = {name: dict(bytes=(HERE/name).stat().st_size, sha256=digest(HERE/name)) for name in result["outputs"]}
    mod.write_json("validation.json", dict(status="pass", checked_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
                   validator_sha256=digest(Path(__file__)), result_sha256=digest(HERE/"results.json"),
                   checks=checks, output_hashes=output_hashes,
                   scope="Numerical and input-invariance validation, not independent training/external biological validation.",
                   no_GPU_or_model_runtime=True))
    print("PASS", len(checks), "validation groups; source invariance and direct numerical checks")


if __name__ == "__main__":
    main()
