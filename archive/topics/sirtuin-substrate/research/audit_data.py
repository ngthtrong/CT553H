"""Audit downloaded tables only; no model fitting or biological label invention."""
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "DECISIONS.md").exists())
TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "log.md").exists())  # thư mục đề tài
RAW = TOPIC / "data/raw"
OUT = Path(__file__).with_name("audit-results.json")


def excel(name, **kwargs):
    return pd.read_excel(RAW / name, engine="openpyxl", **kwargs)


def main():
    rauh = excel("41467_2013_BFncomms3327_MOESM80_ESM.xlsx", header=None, skiprows=4)
    labels = excel("42004_2025_1717_MOESM17_ESM.xlsx", usecols=range(9))
    cellular = excel("42004_2025_1717_MOESM16_ESM.xlsx")
    features = pd.read_csv(RAW / "github-sirt_training_feature_set.csv")
    rauh_key = rauh[0].str.replace("Z", "X", regex=False)
    assert rauh_key.is_unique and labels.Site.is_unique
    aligned = rauh.assign(key=rauh_key).set_index("key").loc[labels.Site]
    y = labels.iloc[:, 2:9].to_numpy(dtype=int)
    category = aligned.iloc[:, [1 + 4 * i for i in range(7)]].to_numpy(float)
    ratio = aligned.iloc[:, [2 + 4 * i for i in range(7)]].to_numpy(float)
    efficiency = aligned.iloc[:, [4 + 4 * i for i in range(7)]].to_numpy(float)
    omitted = rauh.loc[~rauh_key.isin(labels.Site), [0, 29, 30]]
    train_pairs = set()
    train_proteins = set()
    for key in features.uid_pos:
        match = re.fullmatch(r"(.+)_(\d+)_c\d+", key)
        if match:
            train_pairs.add((match[1], int(match[2])))
            train_proteins.add(match[1])
    test_pairs = list(zip(cellular.iloc[:, 0], cellular.iloc[:, 2].astype(int)))
    deeppla = excel("deeppla-table-s1.xlsx", header=2).dropna(subset=["UniProt", "Position"])
    deeppla_sirt = deeppla[deeppla.Enzyme.str.contains("SIRT", na=False)].copy()
    deep_pairs = set(zip(deeppla_sirt.UniProt, deeppla_sirt.Position.astype(int)))
    ev1 = excel("weinert-zip-embj0034-2620-sd2.xlsx", sheet_name="Dataset EV1", header=37)
    ev1 = ev1[ev1.id.notna()]
    ratio_column = "Ratio SIRT3 KO/WT Hebert et al"
    numeric_ko = pd.to_numeric(ev1[ratio_column], errors="coerce")
    zhang = excel("41598_2022_6793_MOESM2_ESM.xlsx", header=1)
    zhang = zhang[pd.to_numeric(zhang.Order, errors="coerce").notna()]
    hits = excel("41598_2022_6793_MOESM3_ESM.xlsx")
    hits = hits[hits.UniquePepID.notna()]
    result = {
        "rauh": {
            "rows": len(rauh), "unique_peptides": rauh[0].nunique(),
            "lengths": rauh[0].str.len().value_counts().to_dict(),
            "central_lysine_rows": int((rauh[0].str[6] == "K").sum()),
            "masked_Z_rows": int(rauh[0].str.contains("Z").sum()),
            "missing_accession_rows": int(rauh[30].isna().sum()),
            "missing_measurement_cells": int(rauh.iloc[:, 1:29].isna().sum().sum()),
            "multi_accession_rows": int(rauh[30].str.contains(";", na=False).sum()),
            "ratio_error_medians": [float(rauh[3+4*i].median()) for i in range(7)],
            "omitted_from_ridgeway": omitted.values.tolist(),
        },
        "ridgeway_labels": {
            "rows": len(labels), "accession_strings": labels.iloc[:, 0].nunique(),
            "synthetic_rows": int((labels.iloc[:, 0] == "SYNTHETIC").sum()),
            "masked_X_rows": int(labels.Site.str.contains("X").sum()),
            "positive_counts": y.sum(axis=0).tolist(),
            "exclusive_positive_counts": y[y.sum(axis=1)==1].sum(axis=0).tolist(),
            "label_cardinality": pd.Series(y.sum(axis=1)).value_counts().sort_index().to_dict(),
            "mismatches_efficiency_ge1": (y != (efficiency >= 1)).sum(axis=0).tolist(),
            "mismatches_category_ge1": (y != (category >= 1)).sum(axis=0).tolist(),
            "mismatches_signal_ratio_ge1": (y != (ratio >= 1)).sum(axis=0).tolist(),
            "missing_cells": int(labels.isna().sum().sum()),
        },
        "ridgeway_cellular": {
            "rows": len(cellular), "proteins": cellular.iloc[:, 0].nunique(),
            "unique_site_keys": len(set(test_pairs)),
            "unique_tryptic_peptides": cellular.iloc[:, 3].nunique(),
            "OE_negative_KD_positive_rows": int(((cellular.iloc[:,4]<0)&(cellular.iloc[:,5]>0)).sum()),
            "predicted_positive": int(cellular.iloc[:,7].sum()),
            "positive_detection_fraction": float(cellular.iloc[:,7].mean()),
            "score_ge_half_matches_labels": bool(((cellular.iloc[:,6]>=.5).astype(int)==cellular.iloc[:,7]).all()),
            "overlapping_train_site_keys": sum(k in train_pairs for k in test_pairs),
            "test_rows_on_train_proteins": sum(k[0] in train_proteins for k in test_pairs),
            "site_key_overlap_is_annotation_only": True,
        },
        "deeppla": {
            "annotation_rows": len(deeppla),
            "sirtuin_annotations_by_enzyme_and_species": deeppla_sirt.groupby(["Enzyme", "Organism"]).size().to_dict(),
            "cellular_test_site_keys_already_annotated": sum(k in deep_pairs for k in test_pairs),
            "train_site_keys_already_annotated": len(train_pairs & deep_pairs),
        },
        "weinert_EV1": {
            "rows": len(ev1), "unique_accession_strings": ev1["UniProt ID"].nunique(),
            "SIRT3_KO_WT_numeric_rows_imported_from_Hebert": int(numeric_ko.notna().sum()),
            "SIRT3_KO_WT_imported_ratio_ge2_rows_NOT_positive_calls": int((numeric_ko>=2).sum()),
            "imported_ratio_columns": [c for c in ev1.columns if "Hebert" in str(c)],
            "has_site_differential_p_or_q_column": any(re.search(r"(^p.?value|^q.?value|^FDR)", str(c), re.I) for c in ev1.columns),
        },
        "zhang": {
            "S1_quantitative_rows": len(zhang), "S1_columns": [str(c) for c in zhang.columns],
            "S2_peptide_hit_rows": len(hits),
            "S2_unique_tryptic_peptides": hits.iloc[:,3].nunique(),
            "S2_reported_ac_lys_sum": int(hits.iloc[:,4].sum()),
            "has_site_differential_p_or_q_column": any(re.search(r"(^p.?value|^q.?value|^FDR)", str(c), re.I) for c in zhang.columns),
        },
    }
    result["deeppla"]["sirtuin_annotations_by_enzyme_and_species"] = {
        f"{enzyme} | {species}": int(count)
        for (enzyme, species), count in result["deeppla"]["sirtuin_annotations_by_enzyme_and_species"].items()
    }
    # Streaming SD13 avoids holding 2.5 million spreadsheet cells in memory.
    import openpyxl
    book = openpyxl.load_workbook(RAW / "42004_2025_1717_MOESM15_ESM.xlsx", read_only=True, data_only=True)
    found = {}
    seen = set()
    count = duplicates = 0
    for row in book.active.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        count += 1
        key = (row[0], int(row[1]))
        duplicates += key in seen
        seen.add(key)
        if key in test_pairs:
            found[key] = (row[5], row[6], row[2])
    matched = sum(k in found for k in test_pairs)
    result["ridgeway_proteome"] = {
        "rows": count, "duplicate_accession_position_keys": duplicates,
        "cellular_keys_matched": matched,
        "cellular_SIRT2_scores_matching_at_1e_minus8": sum(
            k in found and abs(found[k][0] - cellular.iloc[i,6])<1e-8 for i,k in enumerate(test_pairs)),
        "cellular_SIRT2_binary_labels_matching": sum(
            k in found and found[k][1] == cellular.iloc[i,7] for i,k in enumerate(test_pairs)),
        "SD13_positive_on_149_cellular_keys": sum(found[k][1] for k in test_pairs if k in found),
        "score_discrepancy_examples": [
            {"accession": k[0], "position": k[1], "SD13": found[k][0], "SD14": float(cellular.iloc[i,6])}
            for i,k in enumerate(test_pairs[:3]) if k in found],
    }
    canonical = labels.Site[~labels.Site.str.contains("X")].tolist()
    train_chars = np.array([list(sequence) for sequence in canonical])
    local_identities = []
    for key in test_pairs:
        if key in found and len(found[key][2]) == 13 and "X" not in found[key][2]:
            matches = (train_chars == np.array(list(found[key][2]))).sum(axis=1)
            local_identities.append(int(matches.max()))
    result["ridgeway_cellular"]["local_13mer_audit"] = {
        "test_windows_compared_without_X": len(local_identities),
        "train_windows_compared_without_X": len(canonical),
        "test_windows_with_exact_train_window": sum(i == 13 for i in local_identities),
        "test_windows_with_at_least_10_of_13_matches": sum(i >= 10 for i in local_identities),
        "method": "Ungapped equal-position matches of SD13 windows against SD15; NOT full-protein homology",
    }
    inputs = [p for p in RAW.iterdir() if p.suffix in {".xlsx", ".csv"} and p.read_bytes()[:2] == b"PK"]
    inputs += list(RAW.glob("github-*.csv"))
    result["input_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2,
                              default=lambda value: value.item()) + "\n")
    print(f"Saved {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
