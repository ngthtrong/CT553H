#!/usr/bin/env python3
"""Đặt lại ngưỡng SenMayo TRONG từng loại tế bào rồi đếm tế bào dương theo bệnh nhân.

Lý do: trên GSE103322, điểm SenMayo toàn dataset bị chi phối bởi loại tế bào (phần lớn
tế bào dương là fibroblast), nên con số theo bệnh nhân ở senmayo_score.py lẫn thành phần
loại tế bào của từng bệnh nhân. Script này hỏi: nếu chỉ so tế bào cùng loại với nhau,
tế bào dương có còn rải đủ trên nhiều bệnh nhân không?

Đọc file *.senmayo-scores.csv do senmayo_score.py ghi ra (cần cột patient và celltype).

    python3 ml/tme-senescence-scrnaseq/preprocessing/within_celltype.py \
        --scores ml/tme-senescence-scrnaseq/preprocessing/results/GSE103322.h5ad.senmayo-scores.csv \
        --celltypes Fibroblast cancer
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scores", required=True, type=Path)
    ap.add_argument("--celltypes", nargs="+", required=True)
    ap.add_argument("--patient-key", default="patient")
    ap.add_argument("--celltype-key", default="celltype")
    ap.add_argument("--quantile", type=float, default=0.95)
    args = ap.parse_args()

    d = pd.read_csv(args.scores, index_col=0).dropna(subset=[args.patient_key])
    summary, detail = [], []
    for ct in args.celltypes:
        x = d[d[args.celltype_key] == ct]
        pos = x["senmayo"] >= x["senmayo"].quantile(args.quantile)
        cells = x.groupby(args.patient_key).size()
        npos = pos.groupby(x[args.patient_key]).sum().reindex(cells.index, fill_value=0)
        ratio = (npos / npos.sum()) / (cells / cells.sum())
        top = npos.idxmax()
        summary.append({
            "celltype": ct,
            "n_cells": len(x),
            "n_patients": int(cells.size),
            "n_positive": int(pos.sum()),
            "patients_with_ge20_positives": int((npos >= 20).sum()),
            "patients_with_ge10_positives": int((npos >= 10).sum()),
            "top1_patient_of_positives": top,
            "concentration_ratio": round(float(ratio[top]), 3),
            "max_concentration_ratio": round(float(ratio.max()), 3),
        })
        for p in cells.index:
            detail.append({"celltype": ct, "patient": p, "cells": int(cells[p]), "positives": int(npos[p])})

    out = args.scores.parent
    stem = args.scores.name.replace(".senmayo-scores.csv", "")
    s = pd.DataFrame(summary)
    s.to_csv(out / f"{stem}.within-celltype-summary.csv", index=False)
    pd.DataFrame(detail).sort_values(["celltype", "positives"], ascending=[True, False]).to_csv(
        out / f"{stem}.within-celltype-per-patient.csv", index=False
    )
    print(s.to_string(index=False))


if __name__ == "__main__":
    main()
