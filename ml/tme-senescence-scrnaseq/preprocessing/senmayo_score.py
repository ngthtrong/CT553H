#!/usr/bin/env python3
"""Đếm tế bào/bệnh nhân và chấm điểm senescence SenMayo trên một dataset scRNA-seq.

Dùng cho ứng viên "phát hiện tế bào lão hóa trong vi môi trường khối u" (hướng 2
trong docs/common/deep-research/reports/advisor-4-directions-analysis.md). Script
chỉ trả về **số liệu mô tả để đánh giá tính khả thi**: có đủ tế bào dương để huấn
luyện hay không, và tế bào dương có bị dồn vào một vài bệnh nhân hay không.

Script KHÔNG kết luận tế bào nào là senescent. Điểm SenMayo là điểm biểu hiện của
một chữ ký gene, không phải nhãn thực nghiệm; xem mục 7.1 của tài liệu phân tích.

Chạy từ thư mục gốc của repo:

    python3 ml/tme-senescence-scrnaseq/preprocessing/senmayo_score.py \
        --input data/tme-senescence-scrnaseq/raw/<file>.h5ad \
        --patient-key patient \
        --out ml/tme-senescence-scrnaseq/preprocessing/results/

Đầu vào nhận .h5ad (AnnData) hoặc một thư mục 10x (matrix.mtx(.gz) + barcodes +
features/genes). Với thư mục 10x, nhãn bệnh nhân phải nằm ở một file metadata
riêng (--obs-csv), vì mtx không mang metadata.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_GENES = HERE / "senmayo_genes.txt"


def load_signature(path: Path) -> list[str]:
    genes = sorted({line.strip().upper() for line in path.read_text().splitlines() if line.strip()})
    if not genes:
        sys.exit(f"Danh sách gene rỗng: {path}")
    return genes


def load_adata(path: Path, obs_csv: Path | None):
    import scanpy as sc

    if path.is_dir():
        adata = sc.read_10x_mtx(path, var_names="gene_symbols", cache=False)
    elif path.suffix == ".h5ad":
        adata = sc.read_h5ad(path)
    elif path.suffix == ".h5":
        adata = sc.read_10x_h5(path)
    else:
        sys.exit(f"Chưa hỗ trợ định dạng {path.suffix}; dùng .h5ad, .h5 hoặc thư mục 10x")

    if obs_csv is not None:
        import pandas as pd

        meta = pd.read_csv(obs_csv, index_col=0)
        common = adata.obs_names.intersection(meta.index)
        if len(common) == 0:
            sys.exit("Không có barcode nào khớp giữa ma trận và file metadata")
        adata = adata[common].copy()
        adata.obs = adata.obs.join(meta, how="left")
    return adata


def pick_patient_key(adata, requested: str | None) -> str | None:
    if requested:
        if requested not in adata.obs.columns:
            sys.exit(
                f"Không có cột '{requested}' trong obs. Các cột có: {list(adata.obs.columns)}"
            )
        return requested
    # Các tên thường gặp trong dataset công khai; chỉ dùng khi người chạy không chỉ định.
    for cand in ("patient", "patient_id", "donor", "donor_id", "sample", "sample_id", "orig.ident"):
        if cand in adata.obs.columns:
            return cand
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, type=Path, help=".h5ad, .h5 hoặc thư mục 10x")
    ap.add_argument("--obs-csv", type=Path, default=None, help="metadata theo barcode (bắt buộc với thư mục 10x)")
    ap.add_argument("--genes", type=Path, default=DEFAULT_GENES, help="danh sách gene chữ ký, một gene một dòng")
    ap.add_argument("--patient-key", default=None, help="tên cột obs chứa mã bệnh nhân")
    ap.add_argument("--celltype-key", default=None, help="tên cột obs chứa loại tế bào, nếu có")
    ap.add_argument("--quantile", type=float, default=0.95, help="ngưỡng phân vị để gọi là 'dương' (mặc định 0,95)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=Path, default=HERE / "results", help="thư mục ghi kết quả")
    args = ap.parse_args()

    import numpy as np
    import scanpy as sc

    np.random.seed(args.seed)
    args.out.mkdir(parents=True, exist_ok=True)

    signature = load_signature(args.genes)
    adata = load_adata(args.input, args.obs_csv)

    report: dict = {
        "input": str(args.input),
        "seed": args.seed,
        "quantile": args.quantile,
        "n_cells": int(adata.n_obs),
        "n_genes": int(adata.n_vars),
        "signature_file": str(args.genes),
        "signature_size": len(signature),
    }

    var_upper = {str(v).upper() for v in adata.var_names}
    present = [g for g in signature if g in var_upper]
    report["signature_present"] = len(present)
    report["signature_coverage"] = round(len(present) / len(signature), 4)
    report["signature_missing"] = [g for g in signature if g not in var_upper]
    if len(present) < 0.6 * len(signature):
        report["warning_coverage"] = (
            "Dưới 60% gene chữ ký có trong dataset; điểm không đáng tin, không báo cáo như kết quả."
        )

    pkey = pick_patient_key(adata, args.patient_key)
    report["patient_key"] = pkey
    report["obs_columns"] = [str(c) for c in adata.obs.columns]
    if pkey is None:
        report["warning_patient"] = (
            "Không tìm được cột bệnh nhân. Không thể gom nhóm theo bệnh nhân, "
            "nên dataset này KHÔNG dùng được cho split theo bệnh nhân."
        )
    else:
        counts = adata.obs[pkey].astype(str).value_counts()
        report["n_patients"] = int(counts.size)
        report["cells_per_patient"] = {str(k): int(v) for k, v in counts.items()}
        report["cells_per_patient_median"] = float(counts.median())
        report["top1_patient_share"] = round(float(counts.iloc[0]) / adata.n_obs, 4)

    if args.celltype_key and args.celltype_key in adata.obs.columns:
        ct = adata.obs[args.celltype_key].astype(str).value_counts()
        report["n_celltypes"] = int(ct.size)
        report["cells_per_celltype"] = {str(k): int(v) for k, v in ct.items()}

    # Chuẩn hóa tối thiểu. Nếu dữ liệu đã log thì bỏ qua bằng --skip-norm ở phiên bản sau;
    # hiện tại giả định đầu vào là count thô, và ghi rõ giả định đó vào báo cáo.
    adata.var_names = [str(v).upper() for v in adata.var_names]
    adata.var_names_make_unique()
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    report["preprocessing"] = "normalize_total(1e4) + log1p (giả định đầu vào là count thô)"

    sc.tl.score_genes(adata, present, score_name="senmayo", random_state=args.seed)
    scores = np.asarray(adata.obs["senmayo"], dtype=float)
    thr = float(np.quantile(scores, args.quantile))
    pos = scores >= thr
    report["score_mean"] = round(float(scores.mean()), 4)
    report["score_std"] = round(float(scores.std()), 4)
    report["threshold"] = round(thr, 4)
    report["n_positive"] = int(pos.sum())
    report["positive_fraction"] = round(float(pos.mean()), 4)
    report["note_threshold"] = (
        "Ngưỡng là phân vị trong chính dataset này, nên tỉ lệ dương gần đúng bằng "
        "(1 - quantile) theo định nghĩa. Con số có ý nghĩa là PHÂN BỐ tế bào dương "
        "theo bệnh nhân và theo loại tế bào, không phải tỉ lệ dương."
    )

    if pkey is not None:
        import pandas as pd

        per = pd.crosstab(adata.obs[pkey].astype(str), pos)
        per.columns = [str(c) for c in per.columns]
        poscol = "True" if "True" in per.columns else per.columns[-1]
        rate = (per[poscol] / per.sum(axis=1)).sort_values(ascending=False)
        report["positive_rate_per_patient"] = {str(k): round(float(v), 4) for k, v in rate.items()}
        report["positive_rate_spread"] = {
            "min": round(float(rate.min()), 4),
            "median": round(float(rate.median()), 4),
            "max": round(float(rate.max()), 4),
        }
        share = (per[poscol] / per[poscol].sum()).sort_values(ascending=False)
        report["top1_patient_share_of_positives"] = round(float(share.iloc[0]), 4)
        report["note_concentration"] = (
            "Nếu một vài bệnh nhân chiếm phần lớn tế bào dương thì split theo bệnh nhân "
            "sẽ cho fold rất mất cân bằng — đây là con số quyết định tính khả thi."
        )

    out_json = args.out / f"{args.input.name}.senmayo-report.json"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    obs_cols = ["senmayo"] + [c for c in (pkey, args.celltype_key) if c]
    adata.obs[obs_cols].to_csv(args.out / f"{args.input.name}.senmayo-scores.csv")

    print(json.dumps({k: v for k, v in report.items() if not isinstance(v, dict)}, indent=2, ensure_ascii=False))
    print(f"\nGhi: {out_json}")


if __name__ == "__main__":
    main()
