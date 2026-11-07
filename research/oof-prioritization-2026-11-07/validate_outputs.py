"""Independent arithmetic verification from canonical labels and saved raw OOF.

Does not import evaluate.py or audit_inputs.py, deserialize models, train, or
infer. Writes only independent-validation.json after all comparisons pass.
"""
from datetime import datetime, timezone, timedelta
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
ROAD = ROOT / "research/kaggle-roadmap-2026-10-31"
LOCAL = ROAD / "output/local/ef138c84579c842e/jobs/collect-core"
KAGGLE = ROAD / "output/official/369cb2fe6a1e31e0/tasks/01-78cc356ba4f4"
DATA = ROOT / "data/processed/v3-fullpsi"
OOF = {
    "lora-D": LOCAL / "esm2_35m-lora-D-oof.parquet",
    "ridge-w5-D": KAGGLE / "ordered-w5-D-oof.parquet",
    "frozen-D": LOCAL / "esm2_35m-frozen-D-oof.parquet",
    "lora-B": LOCAL / "esm2_35m-lora-B-oof.parquet",
}
METRICS = ("precision", "hits", "recall", "enrichment", "btr50", "btr80", "btr50_fraction", "btr80_fraction")
NUMERIC = ("n", "total_hits", "selected", "psi_wt", *METRICS)
SEEDS = (17, 29, 43)


def require(value, message):
    if not value:
        raise AssertionError(message)


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def equal(actual, expected, context):
    if expected is None or (isinstance(expected, float) and math.isnan(expected)):
        require(pd.isna(actual), f"{context}: expected null, got {actual}")
    else:
        require(not pd.isna(actual) and np.isclose(float(actual), float(expected), atol=1e-12, rtol=1e-12), f"{context}: {actual} != {expected}")


def check_sources(manifest):
    checked_bytes = 0
    for relative, expected in manifest["sources"].items():
        path = ROOT / relative
        require(path.resolve().is_relative_to(ROOT), f"Outside-root source {relative}")
        require(path.is_file(), f"Missing source {relative}")
        require(path.stat().st_size == expected["bytes"], f"Source size changed: {relative}")
        require(digest(path) == expected["sha256"], f"Source SHA256 changed: {relative}")
        checked_bytes += expected["bytes"]
    return {"source_files": len(manifest["sources"]), "source_bytes": checked_bytes, "all_recorded_source_hashes_unchanged": True}


def load_predictions(reference, config):
    prediction = {}
    for policy, path in OOF.items():
        frame = pd.read_parquet(path)
        require(not frame.duplicated(["seed", "cell_id"]).any(), f"{policy}: duplicate OOF")
        require(set(frame.seed) == set(SEEDS), f"{policy}: seed gap")
        require(set(frame["mode"]) == {"official"}, f"{policy}: smoke OOF")
        require(set(frame.data_identity) == {config["data_identity"]}, f"{policy}: identity mismatch")
        require(set(frame.recipe) == {path.stem.removesuffix("-oof")}, f"{policy}: recipe mismatch")
        parts = []
        for seed in SEEDS:
            part = frame[frame.seed == seed].set_index("cell_id").sort_index()
            require(part.index.equals(reference.index), f"{policy}: exact W cohort mismatch")
            for col in ["peptide_id", "group_id", "psi_stratum", "outer_fold", "dpsi_mean"]:
                require(np.array_equal(part[col], reference[col]), f"{policy}: metadata differs at {col}")
            values = part.prediction.to_numpy(dtype=float)
            require(np.isfinite(values).all(), f"{policy}: nonfinite prediction")
            parts.append(values)
        # Arithmetic ensemble of all three seed predictions; no saved utility
        # tables or evaluate.py helper contributes to these reconstructed scores.
        prediction[policy] = pd.Series(np.mean(np.stack(parts), axis=0), index=reference.index)
    return prediction


def independent_tables(reference, predictions, config):
    rows, rank_indices = [], {}
    budgets = [(f"k{k}", "fixed", k) for k in config["fixed_budgets"]]
    budgets += [(f"q{int(q*100):02d}", "fraction", q) for q in config["fraction_budgets"]]
    for peptide, part in reference.groupby("peptide_id", sort=True):
        part = part.sort_index()
        n = len(part)
        ids = part.index.tolist()
        # Python sorted of digest bytes is an independent implementation of the
        # locked hexadecimal SHA256 tie order used by the main numpy scorer.
        keys = [hashlib.sha256(json.dumps([1729, str(peptide), str(cell)], ensure_ascii=False, separators=(",", ":")).encode()).digest() for cell in ids]
        for direction in ("plus", "minus"):
            y = part.dpsi_mean.to_numpy(float)
            hit = (y >= 1) if direction == "plus" else (y <= -1)
            h = int(hit.sum())
            for policy in [*OOF, "random"]:
                if policy != "random":
                    raw_score = predictions[policy].loc[ids].to_numpy()
                    score = raw_score if direction == "plus" else -raw_score
                    order = np.asarray(sorted(range(n), key=lambda i: (-score[i], keys[i])))
                    rank_indices[peptide, policy, direction] = ids, order
                    hit_ranks = np.flatnonzero(hit[order]) + 1
                for name, kind, budget in budgets:
                    k = min(int(budget), n) if kind == "fixed" else max(1, math.ceil(budget*n))
                    if policy == "random":
                        found = k * h / n
                        b50 = math.ceil(.5*h)*(n+1)/(h+1) if h else None
                        b80 = math.ceil(.8*h)*(n+1)/(h+1) if h else None
                        boundary = None
                    else:
                        found = int(hit[order[:k]].sum())
                        b50 = int(hit_ranks[math.ceil(.5*h)-1]) if h else None
                        b80 = int(hit_ranks[math.ceil(.8*h)-1]) if h else None
                        boundary = bool(k < n and score[order[k-1]] == score[order[k]])
                    rows.append({"peptide_id": peptide, "group_id": part.group_id.iloc[0],
                        "psi_stratum": part.psi_stratum.iloc[0], "outer_fold": int(part.outer_fold.iloc[0]),
                        "psi_wt": float(part.psi_wt_sat.iloc[0]),
                        "policy": policy, "direction": direction, "budget": name,
                        "n": n, "total_hits": h, "selected": k, "hits": found, "precision": found/k,
                        "recall": found/h if h else None, "enrichment": (found/k)/(h/n) if h else None,
                        "btr50": b50, "btr80": b80,
                        "btr50_fraction": b50/n if h else None, "btr80_fraction": b80/n if h else None,
                        "null_reason": None if h else "no_hits_in_candidate_pool", "cutoff_tie": boundary})
    return pd.DataFrame(rows), rank_indices


def check_per_peptide(expected, stored):
    keys = ["peptide_id", "policy", "direction", "budget"]
    require(set(stored.prediction_set) == {"ensemble"}, "Unexpected prediction set in ensemble CSV")
    require(not stored.duplicated(keys).any(), "Duplicate per-peptide row")
    a, b = expected.set_index(keys).sort_index(), stored.set_index(keys).sort_index()
    require(a.index.equals(b.index), "Per-peptide cohort/policy/direction/budget coverage differs")
    for col in NUMERIC:
        require(np.allclose(a[col].to_numpy(float), b[col].to_numpy(float), atol=1e-12, rtol=1e-12, equal_nan=True), f"Per-peptide numeric mismatch: {col}")
    for col in ["group_id", "psi_stratum", "outer_fold"]:
        require(np.array_equal(a[col], b[col]), f"Per-peptide metadata mismatch: {col}")
    for col in ["null_reason", "cutoff_tie"]:
        require(a[col].fillna("NULL").equals(b[col].fillna("NULL")), f"Per-peptide field mismatch: {col}")
    require(stored.groupby(["peptide_id", "direction", "budget"]).selected.nunique().max() == 1, "Unequal selection budgets")
    return {"rows_recomputed": len(a), "all_ensemble_budgets_and_directions_match": True,
            "all_metric_nulls_and_reasons_match": True, "equal_budget_each_peptide": True}


def aggregate(rows):
    out = {"peptides": len(rows), "groups": rows.group_id.nunique(), "cells": rows.n.sum(),
           "budget_total": rows.selected.sum(), "selected_min": rows.selected.min(), "selected_max": rows.selected.max(),
           "hits_total": rows.hits.sum(), "no_hit_peptides": int((rows.total_hits == 0).sum()),
           "cutoff_tie_peptides": int(rows.cutoff_tie.fillna(False).sum())}
    for metric in METRICS:
        eligible = rows[rows[metric].notna()]
        out[metric] = float(eligible[metric].mean()) if len(eligible) else None
        out[metric+"_eligible_peptides"] = len(eligible)
        out[metric+"_eligible_groups"] = eligible.group_id.nunique()
    return out


def check_summaries(expected, stored, result):
    stored = stored[stored.prediction_set == "ensemble"]
    keys = ["policy", "direction", "budget"]
    require(not stored.duplicated(keys).any(), "Duplicate ensemble summary")
    summary = stored.set_index(keys)
    require(len(summary) == 5*2*6, "Missing ensemble summary combinations")
    primary = {}
    for key, part in expected.groupby(keys, sort=True):
        require(key in summary.index, f"Missing summary {key}")
        computed = aggregate(part)
        for field, value in computed.items():
            equal(summary.loc[key, field], value, f"summary:{key}:{field}")
        if key[1:] == ("plus", "k10"):
            primary[key[0]] = computed
    require(len(result["primary_summary"]) == 5, "Primary result summary incomplete")
    for row in result["primary_summary"]:
        require(row["direction"] == "plus" and row["budget"] == "k10" and row["prediction_set"] == "ensemble", "Primary summary scope changed")
        for field, value in primary[row["policy"]].items():
            equal(row[field], value, f"results primary:{row['policy']}:{field}")
    return primary


def independent_primary_ci(expected, result, config):
    main = expected[(expected.direction == "plus") & (expected.budget == "k10")]
    policies = main.pivot(index=["peptide_id", "group_id"], columns="policy", values="precision").reset_index()
    groups = sorted(policies.group_id.unique())
    group_index = pd.Categorical(policies.group_id, categories=groups).codes
    counts = np.bincount(group_index)
    # Construct cluster multiplicities independently, then average weighted
    # peptide differences. This retains all peptides of a resampled cluster.
    draws = np.random.default_rng(1729).integers(len(groups), size=(5000, len(groups)))
    multiplicities = np.stack([np.bincount(row, minlength=len(groups)) for row in draws])
    checks = []
    for baseline in ("ridge-w5-D", "random"):
        delta = (policies["lora-D"] - policies[baseline]).to_numpy()
        sums = np.bincount(group_index, weights=delta, minlength=len(groups))
        distribution = (multiplicities @ sums) / (multiplicities @ counts)
        calculated = {"delta": float(delta.mean()), "ci95": np.quantile(distribution, [.025, .975]).tolist(),
                      "ci_adjusted": np.quantile(distribution, [.0125, .9875]).tolist(),
                      "delta_percentage_points": float(delta.mean()*100),
                      "delta_total_hits": float(main[main.policy == "lora-D"].hits.sum()-main[main.policy == baseline].hits.sum()),
                      "groups": len(groups), "peptides": len(policies), "replicates": 5000, "bootstrap_seed": 1729,
                      "multiplicity": 2, "adjusted_level": .975}
        candidates = [row for row in result["primary_contrasts"] if row["baseline"] == baseline]
        require(len(candidates) == 1, f"Missing primary contrast {baseline}")
        stored = candidates[0]
        require(stored["primary"] and stored["metric"] == "precision" and stored["direction"] == "plus" and stored["budget"] == "k10", "Primary contrast definition changed")
        for field, value in calculated.items():
            if isinstance(value, list):
                require(np.allclose(stored[field], value, atol=1e-12, rtol=1e-12), f"Primary CI mismatch: {baseline}/{field}")
            else:
                equal(stored[field], value, f"primary contrast:{baseline}:{field}")
        checks.append({"baseline": baseline, **calculated})
    supported = all(row["ci_adjusted"][0] > 0 for row in checks)
    require(supported == result["supports_both_primary_contrasts"], "Conclusion-rule mismatch")
    require(config["bootstrap_replicates"] == 5000 and config["bootstrap_seed"] == 1729 and config["primary_contrasts"] == 2, "Locked CI configuration changed")
    return checks


def check_examples(reference, predictions, rank_indices, examples):
    example_ids = set(reference.groupby("psi_stratum").peptide_id.min())
    expected_keys = {(peptide, policy, direction, rank) for peptide in example_ids for policy in OOF
                     for direction in ("plus", "minus") for rank in range(1, min(10, int((reference.peptide_id == peptide).sum()))+1)}
    keys = ["peptide_id", "policy", "direction", "rank"]
    require(not examples.duplicated(keys).any(), "Duplicate ranking example")
    require(set(examples[keys].itertuples(index=False, name=None)) == expected_keys, "Missing/extra ranking examples")
    for row in examples.itertuples(index=False):
        ids, ordering = rank_indices[row.peptide_id, row.policy, row.direction]
        require(ids[int(ordering[row.rank-1])] == row.cell_id, "Example rank differs from independently sorted score")
        original = reference.loc[row.cell_id]
        for field in ["peptide_id", "group_id", "psi_stratum", "wt_aa", "mut_aa"]:
            require(getattr(row, field) == original[field], f"Example metadata mismatch: {field}")
        for field in ["position_1based", "outer_fold", "dpsi_mean"]:
            equal(getattr(row, field), original[field], f"Example:{field}")
        equal(row.psi_wt, original.psi_wt_sat, "Example:psi_wt")
        equal(row.prediction, predictions[row.policy].loc[row.cell_id], "Example:prediction")
        require(bool(row.hit) == (original.dpsi_mean >= 1 if row.direction == "plus" else original.dpsi_mean <= -1), "Example hit label mismatch")
    return {"ranking_examples_checked": len(examples), "example_selection_uses_metadata_only": True}


def main():
    config = json.loads((HERE/"config.json").read_text())
    result = json.loads((HERE/"results.json").read_text())
    manifest = json.loads((HERE/"input-manifest.json").read_text())
    require(result["config_sha256"] == digest(HERE/"config.json"), "Result/config hash mismatch")
    require(result["input_manifest_sha256"] == digest(HERE/"input-manifest.json"), "Result/input manifest hash mismatch")
    require(result["analysis_script_sha256"] == digest(HERE/"evaluate.py"), "Result/scorer hash mismatch")
    source_check = check_sources(manifest)
    sat = pd.read_parquet(DATA/"tables/saturation-cells.parquet")
    wide = pd.read_parquet(DATA/"splits/wide-outer.parquet")
    reference = sat.merge(wide, on=["peptide_id", "group_id", "psi_stratum"], validate="many_to_one").set_index("cell_id").sort_index()
    require(not reference.index.duplicated().any() and (reference.wt_aa != reference.mut_aa).all(), "Canonical cell invalid")
    cohort = {"cells": len(reference), "peptides": reference.peptide_id.nunique(), "groups": reference.group_id.nunique()}
    require(cohort == result["cohort"] == config["expected_cohort"] == {"cells": 122412, "peptides": 235, "groups": 221}, "Cohort mismatch")
    predictions = load_predictions(reference, config)
    expected, ranking = independent_tables(reference, predictions, config)
    per_peptide_check = check_per_peptide(expected, pd.read_csv(HERE/"per-peptide.csv"))
    primary_summary = check_summaries(expected, pd.read_csv(HERE/"summary.csv"), result)
    ci_checks = independent_primary_ci(expected, result, config)
    example_check = check_examples(reference, predictions, ranking, pd.read_csv(HERE/"ranking-examples.csv"))
    outputs = {name: {"sha256": digest(HERE/name), "bytes": (HERE/name).stat().st_size}
               for name in ["results.json", "summary.csv", "per-peptide.csv", "ranking-examples.csv", "input-manifest.json", "config.json", "evaluate.py", "validate_outputs.py"]}
    # Numeric values are converted to builtin types via JSON encoder default;
    # NaN is disallowed so validation cannot silently mint undefined metrics.
    report = {"status": "pass", "generated_local": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
              "verification": "Separate implementation; no evaluate.py or audit_inputs.py import; same stored data and shared research context.",
              "cohort": cohort, "source_integrity": source_check, "per_peptide": per_peptide_check,
              "primary_summary_recomputed": primary_summary, "primary_contrasts_recomputed": ci_checks,
              "examples": example_check, "outputs_checked": outputs,
              "scope_limits": ["Recomputes deterministic retrospective arithmetic only; not a rerun of model training, a new split, or wet-lab validation.",
                               "All ensemble policies, both directions, six budgets, null denominators and ranking examples checked; per-seed ranking summaries and stochastic tie/MC bands are covered by the main scorer's checks, not independently rerun here."]}
    def convert(value):
        if isinstance(value, np.generic):
            return value.item()
        raise TypeError(type(value).__name__)
    (HERE/"independent-validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False, default=convert)+"\n")
    print(json.dumps({"status": "pass", "source_files": source_check["source_files"], "per_peptide_rows": per_peptide_check["rows_recomputed"], "primary": ci_checks}, ensure_ascii=False))


if __name__ == "__main__":
    main()
