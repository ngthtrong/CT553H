"""Read-only provenance and alignment gates for the locked prioritization replay.

No model deserialization or inference. ``audit(output_dir)`` writes only the
new replay's input-manifest.json after all gates have passed.
"""
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path, PureWindowsPath
import subprocess

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
ROAD = ROOT / "research/kaggle-roadmap-2026-10-31"
DATA = ROOT / "data/processed/v3-fullpsi"
LOCAL = ROAD / "output/local/ef138c84579c842e"
KAGGLE = ROAD / "output/official/369cb2fe6a1e31e0"
IDENTITY = "b0376e05d690d991c95143d6122b5418e457318394da032928d0d1e53f914738"
SEEDS = (17, 29, 43)
META = ["peptide_id", "group_id", "outer_fold", "psi_stratum", "dpsi_mean"]
POLICIES = {
    "lora-D": "esm2_35m-lora-D",
    "ridge-w5-D": "ordered-w5-D",
    "frozen-D": "esm2_35m-frozen-D",
    "lora-B": "esm2_35m-lora-B",
}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_oof(frame, reference, recipe, identity=IDENTITY):
    """Fail on cohort/metadata gaps; align by cell ID, never row position."""
    required = {"cell_id", "seed", "prediction", "recipe", "mode", "data_identity", *META}
    require(required.issubset(frame.columns), f"{recipe}: missing columns {required-set(frame.columns)}")
    require(not frame[list(required)].isna().any().any(), f"{recipe}: null required value")
    require(set(frame.seed) == set(SEEDS), f"{recipe}: incomplete/unexpected seeds")
    require(set(frame.recipe) == {recipe}, f"{recipe}: wrong recipe")
    require(set(frame["mode"]) == {"official"}, f"{recipe}: smoke/non-official input")
    require(set(frame.data_identity) == {identity}, f"{recipe}: wrong data identity")
    require(not frame.duplicated(["seed", "cell_id"]).any(), f"{recipe}: duplicate seed/cell ID")
    require(np.isfinite(frame[["prediction", "dpsi_mean"]].to_numpy(float)).all(), f"{recipe}: nonfinite value")
    columns = {}
    for seed in SEEDS:
        part = frame.loc[frame.seed == seed].set_index("cell_id").sort_index()
        require(part.index.equals(reference.index), f"{recipe} seed{seed}: cohort mismatch; no intersection permitted")
        pd.testing.assert_frame_equal(part[META], reference[META], check_dtype=False, check_exact=True)
        # Some sources omit explicit amino-acid metadata. A canonical cell ID
        # binds these to the measured saturation table; compare when present.
        for col in ["wt_aa", "mut_aa", "position_1based"]:
            if col in part:
                require(np.array_equal(part[col], reference[col]), f"{recipe}: {col} mismatch")
        columns[f"seed{seed}"] = part.prediction.to_numpy(float)
    result = pd.DataFrame(columns, index=reference.index)
    result["ensemble"] = result.mean(axis=1)
    return result


class Inventory:
    def __init__(self):
        self.files = {}

    def source(self, path, expected=None, authority=None):
        path = Path(path).resolve()
        require(path.is_relative_to(ROOT), f"Input outside repository: {path}")
        require(path.is_file() and path.stat().st_size > 0, f"Missing/empty input: {path}")
        key = path.relative_to(ROOT).as_posix()
        if key not in self.files:
            self.files[key] = {"bytes": path.stat().st_size, "sha256": sha256(path), "verified_against": []}
        record = self.files[key]
        if expected is not None:
            require(record["sha256"] == expected["sha256"], f"SHA256 mismatch: {key}")
            if "bytes" in expected:
                require(record["bytes"] == expected["bytes"], f"Size mismatch: {key}")
            if authority and authority not in record["verified_against"]:
                record["verified_against"].append(authority)
        return path

    def read_json(self, path, **kwargs):
        return json.loads(self.source(path, **kwargs).read_text(encoding="utf8"))


def audit(output_dir=None):
    inventory = Inventory()
    data_manifest = inventory.read_json(DATA / "DATA_MANIFEST.json")
    require(sha256(DATA / "DATA_MANIFEST.json") == IDENTITY, "Data identity changed")
    data_entries = {x["path"]: x for x in data_manifest["files"]}

    def data_path(relative):
        require(relative in data_entries, f"Unmanifested data input: {relative}")
        return inventory.source(DATA / relative, data_entries[relative], "DATA_MANIFEST.json")

    # Keep the original table order for validation-prediction array alignment.
    sat = pd.read_parquet(data_path("tables/saturation-cells.parquet"))
    wide = pd.read_parquet(data_path("splits/wide-outer.parquet"))
    require(not sat.cell_id.duplicated().any(), "Duplicate canonical cell ID")
    require(not wide.peptide_id.duplicated().any(), "Duplicate wide peptide")
    require(set(wide.outer_fold) == set(range(5)), "Incomplete outer folds")
    require(sat.cell_id.notna().all() and np.isfinite(sat.dpsi_mean).all(), "Null/nonfinite saturation cell")
    require((sat.wt_aa != sat.mut_aa).all(), "Synonymous cell in candidate pool")
    canonical_ids = "sat:" + sat.peptide_id + ":" + sat.position_1based.astype(str) + ":" + sat.mut_aa
    require(np.array_equal(canonical_ids, sat.cell_id), "Canonical mutation IDs do not encode metadata")
    for row in sat[["wt_sequence", "mutant_sequence", "position_1based", "wt_aa", "mut_aa"]].itertuples(index=False):
        pos = int(row.position_1based) - 1
        require(0 <= pos < len(row.wt_sequence), "Mutation outside peptide")
        require(row.wt_sequence[pos] == row.wt_aa, "WT amino acid mismatch")
        require(row.mutant_sequence == row.wt_sequence[:pos]+row.mut_aa+row.wt_sequence[pos+1:], "Not a single substitution")
    sat = sat.merge(wide, on=["peptide_id", "group_id", "psi_stratum"], how="left", validate="many_to_one")
    require(sat.outer_fold.notna().all(), "Mutation without matching outer split")
    require(sat.groupby("group_id").outer_fold.nunique().max() == 1, "Protein group crosses outer folds")
    reference = sat.set_index("cell_id").sort_index()
    reference["psi_wt"] = reference.psi_wt_sat
    cohort = {"cells": len(reference), "peptides": reference.peptide_id.nunique(), "groups": reference.group_id.nunique()}
    require(cohort == {"cells": 122412, "peptides": 235, "groups": 221}, f"Unexpected W cohort {cohort}")

    plan = inventory.read_json(LOCAL / "plan.json")
    state = inventory.read_json(LOCAL / "state.json")
    queue = inventory.read_json(LOCAL / "queue.json")
    lineage = inventory.read_json(LOCAL / "inheritance.json")
    require(plan["data_identity"] == IDENTITY and plan["source_campaign"] == KAGGLE.name, "Local plan mismatch")
    require({x["id"] for x in queue} == set(state["jobs"]), "Queue/state mismatch")
    source_name = PureWindowsPath(lineage["source_campaign"]).name
    require(source_name == "e7097449883a51d8", "Unexpected inherited campaign")
    inventory.source(LOCAL.parent/source_name/"state.json", {"sha256": lineage["source_state_sha256"]}, "inheritance.json")
    collection = inventory.read_json(LOCAL / "jobs/collect-core/collection.json")
    require(collection["mode"] == "official" and collection["data_identity"] == IDENTITY, "Collection identity/mode mismatch")
    kaggle_manifest = inventory.read_json(KAGGLE / "pipeline-manifest.json")
    require(kaggle_manifest["plan_id"][:16] == KAGGLE.name, "Kaggle campaign mismatch")
    require(kaggle_manifest["plan"]["data_identity"] == IDENTITY and kaggle_manifest["plan"]["mode"] == "official", "Kaggle identity/mode mismatch")
    kaggle_entries = {entry["path"]: entry for task in kaggle_manifest["tasks"].values() if task["status"] == "complete" for entry in task["files"]}

    def local_origin(job_id):
        record = state["jobs"][job_id]
        require(record["status"] == "complete", f"Incomplete job {job_id}")
        original = record.get("artifact_campaign")
        name = PureWindowsPath(original).name if original else LOCAL.name
        require(name in {LOCAL.name, "e7097449883a51d8"}, f"Unknown lineage {name}")
        origin = LOCAL.parent/name
        if origin != LOCAL:
            inventory.source(origin/"plan.json", {"sha256": record["source_plan_sha256"]}, f"state:{job_id}")
        return origin, {x["path"]: x for x in record["files"]}

    def local_file(job_id, filename):
        origin, entries = local_origin(job_id)
        rel = f"jobs/{job_id}/{filename}"
        require(rel in entries, f"Unmanifested local input {rel}")
        return inventory.source(origin/rel, entries[rel], f"state:{job_id}")

    def kaggle_file(filename):
        rel = f"tasks/01-78cc356ba4f4/{filename}"
        require(rel in kaggle_entries, f"Unmanifested Kaggle input {rel}")
        return inventory.source(KAGGLE/rel, kaggle_entries[rel], "pipeline-manifest.json:01")

    splits = {}
    split_checks = []
    for seed in SEEDS:
        split = pd.read_parquet(data_path(f"splits/inner-seed{seed}.parquet"))
        require(set(split.seed) == {seed}, "Inner split seed mismatch")
        require(set(split.outer_fold) == set(range(5)), "Inner split fold gap")
        require(not split.duplicated(["outer_fold", "group_id"]).any(), "Group has multiple roles")
        for fold in range(5):
            part = split[split.outer_fold == fold].set_index("group_id")
            require(set(part.role) == {"train", "validation", "test", "held_source"}, "Unexpected split roles")
            role = sat.group_id.map(part.role)
            require(role.notna().all(), "W group missing in inner split")
            require(set(sat.loc[role == "test", "group_id"]) == set(sat.loc[sat.outer_fold == fold, "group_id"]), "Outer-test group mismatch")
            require(not (role == "held_source").any(), "Held source included in W")
            splits[seed, fold] = role.to_numpy()
            split_checks.append({"seed": seed, "fold": fold, "W_cells_per_role": role.value_counts().to_dict(), "W_groups_per_role": sat.assign(role=role).groupby("role").group_id.nunique().to_dict()})

    predictions, policy_checks, fold_checks = {}, {}, []
    for policy, recipe in POLICIES.items():
        path = kaggle_file(recipe+"-oof.parquet") if policy == "ridge-w5-D" else local_file("collect-core", recipe+"-oof.parquet")
        frame = pd.read_parquet(path)
        predictions[policy] = validate_oof(frame, reference, recipe)
        for seed in SEEDS:
            for fold in range(5):
                role = splits[seed, fold]
                train = (role == "train") & ((sat.psi_wt_sat <= 4) if policy == "lora-B" else True)
                validation = role == "validation"
                test = role == "test"
                final = np.isin(role, ["train", "validation"]) & ((sat.psi_wt_sat <= 4) if policy == "lora-B" else True)
                test_groups = set(sat.loc[test, "group_id"])
                require(not test_groups & set(sat.loc[train | validation, "group_id"]), "Test group used for fit/selection")
                if policy == "ridge-w5-D":
                    info = json.loads(kaggle_file(f"{recipe}-seed{seed}-fold{fold}.json").read_text())
                    cal_path = kaggle_file(f"{recipe}-seed{seed}-fold{fold}-calibration.parquet")
                    require(info["mode"] == "official" and info["train_fraction"] == 1, "Ridge smoke/subsample")
                    require(set(info["training_groups"]) == set(sat.loc[final, "group_id"]), "Ridge refit groups mismatch")
                    for name, expected in [("n_train", train.sum()), ("n_validation", validation.sum()), ("n_test", test.sum()), ("n_refit", final.sum())]:
                        require(info[name] == int(expected), f"Ridge {name} mismatch")
                else:
                    mode, arm = ("frozen" if policy == "frozen-D" else "lora"), policy[-1]
                    job = f"tune-{mode}-{arm}-{seed}-{fold}"
                    info = json.loads(local_file(job, "fit.json").read_text())
                    require(info["mode"] == mode and info["arm"] == arm, "Local training recipe mismatch")
                    require(isinstance(info["selected_epoch"], int) and 1 <= info["selected_epoch"] <= 20, "Invalid selected epoch")
                    fold_oof = pd.read_parquet(local_file(job, "oof.parquet"))
                    collected = frame[(frame.seed == seed) & (frame.outer_fold == fold)].set_index("cell_id").sort_index()
                    individual = fold_oof.set_index("cell_id").sort_index()
                    pd.testing.assert_frame_equal(individual[collected.columns], collected, check_dtype=False, check_exact=True)
                    cal_path = local_file(job, "calibration.parquet")
                    _, entries = local_origin(job)
                    epoch_files = sorted((x for x in entries if Path(x).name.startswith("inner-validation-") and x.endswith(".npy")), key=lambda p: int(Path(p).stem.rsplit("-", 1)[1]))
                    epochs = [int(Path(x).stem.rsplit("-", 1)[1]) for x in epoch_files]
                    require(epochs == list(range(1, max(epochs)+1)), "Validation epoch gap")
                    best_mse, best_epoch = float("inf"), 0
                    for relative in epoch_files:
                        epoch = int(Path(relative).stem.rsplit("-", 1)[1])
                        values = np.load(local_file(job, Path(relative).name), allow_pickle=False)
                        require(values.shape == (int(validation.sum()),) and np.isfinite(values).all(), "Inner-validation array mismatch")
                        progress = json.loads(local_file(job, Path(relative).with_suffix(".json").name).read_text())
                        require(progress["completed"] == len(values), "Incomplete saved validation predictions")
                        require(hashlib.sha256(values.tobytes()).hexdigest() == progress["prefix_sha256"], "Validation prediction prefix mismatch")
                        mse = float(np.mean((values - sat.loc[validation, "dpsi_mean"].to_numpy())**2))
                        # The training code updates only at improvements >1e-6.
                        if mse < best_mse - 1e-6:
                            best_mse, best_epoch = mse, epoch
                    require(best_epoch == info["selected_epoch"], "Epoch selection mismatch")
                    require(abs(best_mse - info["validation_mse"]) < 1e-12, "Selected validation MSE mismatch")
                require(info["recipe"] == recipe and info["data_identity"] == IDENTITY and info["seed"] == seed and info["fold"] == fold, "Fit metadata mismatch")
                cal = pd.read_parquet(cal_path)
                require(not cal.cell_id.duplicated().any() and np.isfinite(cal.prediction).all(), "Invalid calibration rows")
                expected = sat.loc[validation].set_index("cell_id").sort_index()
                observed = cal.set_index("cell_id").sort_index()
                require(observed.index.equals(expected.index), "Calibration/selection cohort mismatch")
                pd.testing.assert_frame_equal(observed[["peptide_id", "group_id", "dpsi_mean"]], expected[["peptide_id", "group_id", "dpsi_mean"]], check_dtype=False, check_exact=True)
                require(not set(cal.group_id) & test_groups, "Calibration uses outer-test group")
                fold_checks.append({"policy": policy, "seed": seed, "fold": fold, "train_cells": int(train.sum()), "validation_cells": int(validation.sum()), "refit_cells": int(final.sum()), "test_cells": int(test.sum()), "selected_epoch": info.get("selected_epoch"), "alpha": info.get("alpha"), "validation_mse": info["validation_mse"], "calibration_excludes_test": True, "collection_matches_fold_oof": policy != "ridge-w5-D", "epoch_selection_replayed": policy != "ridge-w5-D"})
        if policy != "ridge-w5-D":
            report = collection["reports"][recipe]
            for name in ["ensemble", *[f"seed{s}" for s in SEEDS]]:
                error = np.abs(predictions[policy][name] - reference.dpsi_mean)
                mae = float(error.groupby(reference.peptide_id).mean().mean())
                expected_mae = report["ensemble"]["all"]["mae"] if name == "ensemble" else report["per_seed"][name[4:]]["all"]["mae"]
                require(abs(mae-expected_mae) < 1e-10, "Collection metric cannot be reproduced")
        policy_checks[policy] = {"recipe": recipe, "rows": len(frame), "seeds": list(SEEDS), "folds": sorted(int(x) for x in frame.outer_fold.unique()), "exact_W_cohort_each_seed": True, "duplicate_seed_cells": 0, "finite_predictions": True}

    # Pin existing reports as provenance, checking their recorded data/campaign.
    local_analysis = inventory.read_json(ROAD/"local-output-analysis.json")
    kaggle_analysis = inventory.read_json(ROAD/"output-analysis.json")
    require(local_analysis["data_identity"] == IDENTITY and local_analysis["campaign"] == LOCAL.name, "Local analysis lineage mismatch")
    require(kaggle_analysis["data_identity"] == IDENTITY and kaggle_analysis["source_manifest_sha256"] == sha256(KAGGLE/"pipeline-manifest.json"), "Kaggle analysis lineage mismatch")
    # Current source is for implementation traceability, not an assertion that
    # current bytes equal the original Windows source fingerprint.
    for relative in ["degron_v3/local_jobs.py", "degron_v3/local_training.py", "degron_v3/learning.py", "degron_v3/stages.py", "degron_v3/data.py", "degron_v3/metrics.py", "EXECUTION-PROTOCOL.md"]:
        inventory.source(ROAD/relative)
    inventory.source(__file__)
    inventory.source(HERE/"evaluate.py")
    for path in [ROOT/"tmp.md", HERE/"PROTOCOL.md", HERE/"config.json"]:
        if path.exists():
            inventory.source(path)
    working_diff = subprocess.check_output(["git", "diff", "--binary", "HEAD"], cwd=ROOT)
    result = {
        "status": "pass", "generated_local": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "data_identity": IDENTITY, "cohort": {k: int(v) for k, v in cohort.items()},
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "working_diff_sha256": hashlib.sha256(working_diff).hexdigest(),
        "working_diff_bytes": len(working_diff),
        "git_status_porcelain": subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).splitlines(),
        "policy_checks": policy_checks, "split_checks": split_checks, "fold_checks": fold_checks,
        "sources": inventory.files, "source_file_count": len(inventory.files),
        "source_bytes_checked": sum(x["bytes"] for x in inventory.files.values()),
        "source_fingerprints_recorded_by_original_plans": {"local_code_sha256": plan["code_sha256"], "local_protocol_sha256": plan["protocol_sha256"], "local_registry_sha256": plan["registry_sha256"], "kaggle_implementation_sha256": kaggle_manifest["plan"]["implementation_sha256"]},
        "limitations": [
            "Audit verifies the used artifact bytes and saved group-role assignments, not a re-run of training or a fresh remote-homology audit.",
            "Local training/refit group membership is reconstructed from stored splits and the recorded arm plus source implementation; fit.json does not store a realized training-group list. Checkpoints are not deserialized.",
            "Ridge alpha is checked against stored metadata and calibration population; candidate-alpha predictions are not stored, so alpha selection cannot be independently replayed without forbidden refitting.",
            "Local selected epochs are replayed from saved inner-validation predictions with the recorded >1e-6 improvement rule; this checks saved evidence, not original training execution.",
            "Calibrator isolation is checked on inner-validation input populations. Replay ranks raw predictions and does not load or fit any calibrator, including final serving calibration.",
            "OOF inputs omit position/WT/mutant columns; canonical measured cell IDs bind those fields, and explicit fields are checked when present.",
            "Only used dataset and campaign files are hashed; unused models/checkpoints and other campaign artifacts are outside this replay audit.",
        ],
    }
    if output_dir is not None:
        destination = Path(output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        (destination/"input-manifest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf8")
    return reference, predictions, result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE)
    args = parser.parse_args()
    reference, predictions, result = audit(args.output)
    print(json.dumps({"status": result["status"], "cohort": result["cohort"], "source_file_count": result["source_file_count"]}))
