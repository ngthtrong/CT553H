#!/usr/bin/env python3
"""Dựng lại PSI từ read thô cho MỌI điều kiện của Zhang 2023, không chỉ Replicate 1.

Vì sao cần: audit trước chỉ dùng `I28 Scanning Mutagenesis Replicate 1.csv` (file duy nhất
tác giả đã tính sẵn PSI). Nhưng ZIP còn chứa read thô của **Replicate 2** và của **mẫu BAG6 WT**,
cộng 12 mẫu **saturation** — chưa ai trong repo tính PSI cho chúng. Không có replicate thứ hai
thì không tách được nhiễu đo khỏi tín hiệu ngữ cảnh, tức không trả lời được rủi ro số hai
của đề tài.

Công thức, suy ra từ Replicate 1 và đã khớp chính xác:
    factor_i = (Σ_rows b_1) / (Σ_rows b_i)      # bin 1 làm chuẩn
    nb_i     = b_i × factor_i
    Sum      = Σ_i nb_i
    PSI      = (Σ_i i × nb_i) / Sum             # thang 1..6, THẤP = bị phân hủy nhanh

Cổng kiểm: chạy với --validate thì script dựng PSI của Replicate 1 từ 6 file read thô và
so với cột PSI trong CSV của tác giả. Nếu lệch quá ngưỡng thì dừng, không ghi kết quả.

Dùng:
    build_psi.py --condition rep1 --validate
    build_psi.py --condition rep2
    build_psi.py --condition wt
    build_psi.py --condition saturation
"""

import argparse
import csv
import json
import math
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
SCAN = TOPIC / "data/interim/zhang-scanning-unzip/I28 Scanning (Completed)"
SAT = TOPIC / "data/interim/zhang-saturation-unzip/I28 CRL Saturation (Completed)"
OUT = TOPIC / "data/processed"

# Script gộp của tác giả đọc 6 file count với header=TRUE trên file KHÔNG có header, nên
# dòng dữ liệu đầu của mỗi file bị ăn mất. Dòng đầu: S1=mut10, S2=mut17, S3..S6=mut24.
# Hệ quả trong CSV công bố: mut10 và mut17 có Sum=0/PSI=NA dù có read; mut24 mất bin 3..6
# nên PSI của nó lệch 0,62. Ba id này được loại khỏi phép so sánh và ghi lại tường minh.
HEADER_BUG_IDS = {
    "A0A0B4J1Y8_IGLV9-49_1_mut10",
    "A0A0B4J1Y8_IGLV9-49_1_mut17",
    "A0A0B4J1Y8_IGLV9-49_1_mut24",
}

CONDITIONS = {
    "rep1": (SCAN / "Replicate 1 (BAG6 genotype unclear)",
             ["LIB054277_GEN00225351_S1.txt", "LIB054277_GEN00225352_S2.txt",
              "LIB054277_GEN00225353_S3.txt", "LIB054277_GEN00225354_S4.txt",
              "LIB054277_GEN00225355_S5.txt", "LIB054277_GEN00225356_S6.txt"]),
    "rep2": (SCAN / "Replicate 2 (BAG6 genotype unclear)",
             ["LIB054277_GEN00225357_S7.txt", "LIB054277_GEN00225358_S8.txt",
              "LIB054277_GEN00225359_S9.txt", "LIB054277_GEN00225360_S10.txt",
              "LIB054277_GEN00225361_S11.txt", "LIB054277_GEN00225362_S12.txt"]),
    "wt": (SCAN / "WT (BAG6 WT)",
           ["LIB057578_GEN00252086_S1.txt", "LIB057578_GEN00252087_S2.txt",
            "LIB057578_GEN00252088_S3.txt", "LIB057578_GEN00252089_S4.txt",
            "LIB057578_GEN00252090_S5.txt", "LIB057578_GEN00252091_S6.txt"]),
    # Saturation: 12 mẫu. Theo thứ tự file S1..S12 tác giả đặt; 6 bin đầu là replicate A,
    # 6 bin sau là replicate B. Giả định này được KIỂM bằng tương quan PSI hai nửa (xem
    # audit_all.py); nếu tương quan thấp thì thứ tự bin không phải như vậy.
    "sat_a": (SAT, [f"LIB055029_GEN002309{n}_S{i}.txt" for i, n in
                    zip(range(1, 7), [21, 22, 23, 24, 25, 26])]),
    "sat_b": (SAT, [f"LIB055029_GEN002309{n}_S{i}.txt" for i, n in
                    zip(range(7, 13), [27, 28, 29, 30, 31, 32])]),
}


def read_counts(path, drop_first=False):
    """drop_first mô phỏng lỗi của tác giả: bỏ dòng dữ liệu đầu tiên như thể nó là header."""
    counts = {}
    with path.open(encoding="utf-8", errors="replace") as fh:
        for index, line in enumerate(fh):
            if drop_first and index == 0:
                continue
            if not line.strip():
                continue
            name, _, value = line.rstrip("\n").partition("\t")
            counts[name] = counts.get(name, 0) + int(float(value))
    return counts


def build(condition, restrict=None, emulate_author_bug=False):
    """Trả về {id: (PSI, Sum, [nb_1..nb_6])}. restrict: chỉ giữ id trong tập này.

    emulate_author_bug=True tái lập đúng pipeline đã công bố, kể cả lỗi header — dùng để
    chứng minh đã hiểu trọn pipeline. Bảng dùng cho phân tích thì để False (đã sửa).
    """
    directory, names = CONDITIONS[condition]
    bins = [read_counts(directory / n, drop_first=emulate_author_bug) for n in names]
    ids = set()
    for b in bins:
        ids |= b.keys()
    if restrict is not None:
        ids &= set(restrict)
    totals = [sum(b.get(i, 0) for i in ids) for b in bins]
    factors = [totals[0] / t if t else 0.0 for t in totals]
    out = {}
    for i in sorted(ids):
        nb = [bins[k].get(i, 0) * factors[k] for k in range(6)]
        total = sum(nb)
        psi = sum((k + 1) * nb[k] for k in range(6)) / total if total else float("nan")
        out[i] = (psi, total, nb)
    return out, factors, totals


def load_author_csv():
    path = SCAN / "Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv"
    csv.field_size_limit(10 ** 7)
    rows = {}
    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            psi = r["PSI"]
            rows[r["Gene"]] = (
                float(psi) if psi not in ("NA", "", "NaN") else float("nan"),
                float(r["Sum"]), r["AA.Seq"],
            )
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--condition", required=True, choices=list(CONDITIONS) + ["all"])
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--tolerance", type=float, default=1e-6)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    report = {}

    if args.validate:
        author = load_author_csv()
        # Chuẩn hóa của tác giả tính trên chính các hàng của CSV, nên restrict vào tập đó.
        mine, factors, totals = build("rep1", restrict=author.keys(), emulate_author_bug=True)
        fixed, _, _ = build("rep1", restrict=author.keys())
        diffs, missing, artifacts = [], 0, []
        for name, (psi_a, sum_a, _) in author.items():
            if name not in mine and name not in fixed:
                missing += 1
                continue
            if name in HEADER_BUG_IDS:
                psi_f, sum_f, _ = fixed[name]
                artifacts.append({"id": name, "author_psi": None if math.isnan(psi_a) else psi_a,
                                  "author_sum": sum_a, "rebuilt_psi": psi_f,
                                  "rebuilt_sum": sum_f})
                continue
            if name not in mine:
                missing += 1
                continue
            psi_m, sum_m, _ = mine[name]
            if math.isnan(psi_a) and math.isnan(psi_m):
                continue
            if math.isnan(psi_a) or math.isnan(psi_m):
                diffs.append(float("inf"))
                continue
            diffs.append(abs(psi_a - psi_m))
        worst = max(diffs) if diffs else 0.0
        report["validate_rep1"] = {
            "n_compared": len(diffs), "n_missing_from_counts": missing,
            "max_abs_psi_diff": worst, "tolerance": args.tolerance,
            "factors": factors, "bin_totals_over_csv_rows": totals,
            "author_header_bug_excluded": artifacts,
            "note": "khớp đạt khi mô phỏng đúng lỗi header của tác giả; bảng xuất ra đã sửa",
            "passed": worst <= args.tolerance,
        }
        print(f"[validate] so {len(diffs)} PSI, lệch lớn nhất {worst:.3e}, "
              f"{'ĐẠT' if worst <= args.tolerance else 'KHÔNG ĐẠT'}"
              f" (loại {len(artifacts)} id do lỗi header của tác giả)", flush=True)
        if worst > args.tolerance:
            raise SystemExit("Không tái lập được PSI của tác giả; dừng, không ghi kết quả.")

    todo = list(CONDITIONS) if args.condition == "all" else [args.condition]
    for cond in todo:
        table, factors, totals = build(cond)
        dest = OUT / f"psi-{cond}.tsv"
        with dest.open("w", encoding="utf-8") as fh:
            fh.write("id\tpsi\tsum\t" + "\t".join(f"nb{i}" for i in range(1, 7)) + "\n")
            for name, (psi, total, nb) in table.items():
                fh.write(f"{name}\t{psi:.10g}\t{total:.10g}\t"
                         + "\t".join(f"{x:.10g}" for x in nb) + "\n")
        report[cond] = {"n_ids": len(table), "factors": factors, "bin_totals": totals,
                        "output": str(dest.relative_to(TOPIC))}
        print(f"{cond}: {len(table)} id -> {dest.relative_to(TOPIC)}", flush=True)

    path = Path(__file__).parent / "psi-build.json"
    existing = json.loads(path.read_text()) if path.exists() else {}
    existing.update(report)
    path.write_text(json.dumps(existing, indent=1) + "\n", encoding="utf-8")
    print("report:", path.name)


if __name__ == "__main__":
    main()
