#!/usr/bin/env python3
"""Chuyển GSE103322 (Puram et al. 2017, HNSCC, Smart-seq2) từ bảng txt.gz sang .h5ad.

File gốc trên GEO là một bảng gene × tế bào, tab-separated, KHÔNG phải count thô:
GEO ghi giá trị đã chuẩn hóa và log hóa (theo bài gốc là log2(TPM/10 + 1) — [chưa kiểm
lại trong bài báo ở phiên này]). Vì vậy khi chấm điểm phải chạy senmayo_score.py với
--skip-norm.

Năm dòng đầu sau tiêu đề là metadata theo tế bào:
    processed by Maxima enzyme / Lymph node / classified as cancer cell /
    classified as non-cancer cells / non-cancer cell type

Bảng không có cột bệnh nhân. Mã bệnh nhân suy từ tên tế bào:
    HNSCC17_..., HN26_..., HNSCC_17_P9_...  -> HNSCC17, HNSCC26, HNSCC17
Giả định: tiền tố "HN<n>" và "HNSCC<n>" cùng chỉ một bệnh nhân <n>. Hai plate
"HNSCC_combo1/2" trộn nhiều bệnh nhân và tên tế bào không cho biết của ai, nên để
trống (NaN) và bị loại khỏi mọi thống kê theo bệnh nhân.

Chạy từ thư mục gốc của repo:

    python3 archive/topics/tme-senescence-scrnaseq/code/preprocessing/convert_gse103322.py \
        --input archive/topics/tme-senescence-scrnaseq/data/raw/GSE103322_HNSCC_all_data.txt.gz \
        --out archive/topics/tme-senescence-scrnaseq/data/processed/GSE103322.h5ad
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

META_ROWS = {
    "processed by Maxima enzyme": "maxima_enzyme",
    "Lymph node": "lymph_node",
    "classified  as cancer cell": "is_cancer",
    "classified as non-cancer cells": "is_noncancer",
    "non-cancer cell type": "noncancer_type",
}


def patient_from_name(name: str) -> str | None:
    if name.startswith("HNSCC_combo"):
        return None
    m = re.match(r"^HNSCC_(\d+)_", name) or re.match(r"^(?:HNSCC|HN)(\d+)_", name)
    return f"HNSCC{int(m.group(1))}" if m else None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    import anndata as ad
    import numpy as np
    import pandas as pd
    import scipy.sparse as sp

    df = pd.read_csv(args.input, sep="\t", index_col=0, low_memory=False)
    meta_idx = [i for i in df.index[:5]]
    if [i.strip() for i in meta_idx] != [k.strip() for k in META_ROWS]:
        raise SystemExit(f"Năm dòng metadata không đúng như mong đợi: {meta_idx}")

    meta = df.iloc[:5].T
    meta.columns = list(META_ROWS.values())
    expr = df.iloc[5:].astype(np.float32)
    expr.index = [str(g).strip("'\"") for g in expr.index]

    obs = pd.DataFrame(index=[str(c) for c in df.columns])
    obs["patient"] = [patient_from_name(c) for c in obs.index]
    for col in ("maxima_enzyme", "lymph_node", "is_cancer", "is_noncancer"):
        obs[col] = pd.Series(pd.to_numeric(meta[col].values, errors="coerce"), index=obs.index).astype("Int8")
    nct = meta["noncancer_type"].astype(str).str.strip().str.lstrip("-")
    # Loại tế bào gộp: cancer / loại không ung thư / "unresolved" (không được phân loại)
    obs["celltype"] = np.where(
        obs["is_cancer"] == 1,
        "cancer",
        np.where(nct.isin(["0", "0.0", "", "nan"]), "unresolved", nct.values),
    )

    adata = ad.AnnData(X=sp.csr_matrix(expr.T.values), obs=obs)
    adata.var_names = expr.index
    adata.var_names_make_unique()
    adata.uns["source"] = "GEO GSE103322, GSE103322_HNSCC_all_data.txt.gz"
    adata.uns["values"] = "đã log hóa sẵn trên GEO (log2(TPM/10+1) theo bài gốc, chưa kiểm); dùng --skip-norm"

    args.out.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(args.out, compression="gzip")
    print(f"{adata.n_obs} tế bào × {adata.n_vars} gene; "
          f"{obs['patient'].nunique()} bệnh nhân suy được, {obs['patient'].isna().sum()} tế bào không rõ bệnh nhân")
    print(obs["celltype"].value_counts().to_string())
    print(f"Ghi: {args.out}")


if __name__ == "__main__":
    main()
