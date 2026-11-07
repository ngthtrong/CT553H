#!/usr/bin/env python3
"""Audit sàng peptidome GPS của Zhang 2023, gồm SVM của chính tác giả và nhánh MLN4924.

Vì sao quan trọng: thẻ đề tài đánh giá cổng G3 dựa trên ba sản phẩm đã có (DEGRONOPEDIA,
MetaDegron, Colab của nhóm PAP) và **không biết** rằng Zhang 2023 đã kèm một mô hình học máy
dự đoán PSI cho toàn bộ peptidome, huấn luyện trên 5% và 10% dữ liệu, phủ hoàn toàn.
Đó là baseline đã công bố **trên chính bộ dữ liệu đề tài dùng**, nên phải đo nó trước khi
tuyên bố bất kỳ đóng góp dương nào.

Nguồn: Mendeley 10.17632/32h94v2yv2.2, "I28 GPS Peptidome Screen and MLN4924 and SVM.zip".

Đo:
  1. Hiệu năng SVM của tác giả: Observed.PSI so với Predicted.PSI, ở 5% và 10% train.
  2. Cột replicate.error của chính tác giả — ước lượng nhiễu của họ.
  3. Độ lặp lại Control Rep 1 so với Rep 2 trên thang peptidome (ước lượng nhiễu thứ ba,
     độc lập với bộ scanning và bộ bão hòa).
  4. deltaPSI.MLN4924: peptide nào phụ thuộc CRL.
Đọc theo luồng, không nạp cả file vào RAM.
"""

import csv
import json
import math
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
BASE = (TOPIC / "data/interim/zhang-gps-unzip/I28 Initial MLN4924 SVM (Completed)")
READ_MIN = 10


class Acc:
    """Tích lũy thống kê hai biến theo luồng, không giữ dữ liệu."""

    def __init__(self):
        self.n = 0
        self.sx = self.sy = self.sxx = self.syy = self.sxy = 0.0
        self.sd = self.sdd = 0.0

    def add(self, x, y):
        self.n += 1
        self.sx += x
        self.sy += y
        self.sxx += x * x
        self.syy += y * y
        self.sxy += x * y
        d = x - y
        self.sd += d
        self.sdd += d * d

    def result(self):
        n = self.n
        if n < 3:
            return None
        cov = self.sxy / n - (self.sx / n) * (self.sy / n)
        vx = self.sxx / n - (self.sx / n) ** 2
        vy = self.syy / n - (self.sy / n) ** 2
        md = self.sd / n
        var_d = max(0.0, self.sdd / n - md * md)
        return {
            "n": n,
            "pearson": round(cov / math.sqrt(vx * vy), 4) if vx > 0 and vy > 0 else None,
            "mean_x": round(self.sx / n, 4), "mean_y": round(self.sy / n, 4),
            "sd_x": round(math.sqrt(vx), 4), "sd_y": round(math.sqrt(vy), 4),
            "mean_diff": round(md, 4), "sd_diff": round(math.sqrt(var_d), 4),
            "rmse": round(math.sqrt(self.sdd / n), 4),
        }


def number(value):
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(f) else f


def audit_svm(path, tag, report):
    acc = Acc()
    rep_err, mln = [], []
    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            obs, pred = number(row.get("Observed.PSI")), number(row.get("Predicted.PSI"))
            if obs is not None and pred is not None:
                acc.add(obs, pred)
            e = number(row.get("replicate.error"))
            if e is not None:
                rep_err.append(abs(e))
            d = number(row.get("deltaPSI.MLN4924"))
            if d is not None:
                mln.append(d)
    out = {"author_svm_observed_vs_predicted": acc.result()}
    if rep_err:
        rep_err.sort()
        n = len(rep_err)
        out["author_replicate_error_column"] = {
            "n": n, "median_abs": round(rep_err[n // 2], 4),
            "p90_abs": round(rep_err[int(n * 0.9)], 4),
            "mean_abs": round(sum(rep_err) / n, 4),
            "meaning": "Ước lượng sai số giữa hai replicate do chính tác giả ghi.",
        }
    if mln:
        mln.sort()
        n = len(mln)
        out["mln4924_delta_psi"] = {
            "n": n, "median": round(mln[n // 2], 4),
            "p05": round(mln[int(n * 0.05)], 4), "p95": round(mln[int(n * 0.95)], 4),
            "n_stabilised_ge_1": sum(1 for x in mln if x >= 1.0),
            "frac_stabilised_ge_1": round(sum(1 for x in mln if x >= 1.0) / n, 4),
            "meaning": ("MLN4924 ức chế neddylation nên chặn CRL. deltaPSI >= 1 là peptide "
                        "bền lên rõ khi chặn CRL, tức phụ thuộc CRL."),
        }
    report[tag] = out


def audit_replicates(report):
    """Control Rep 1 so Rep 2, khớp theo Gene, chỉ giữ cả hai đạt ngưỡng reads."""
    rep1 = {}
    csv.field_size_limit(10 ** 7)
    with (BASE / "I28 Control Replicate 1.csv").open(newline="", encoding="utf-8",
                                                     errors="replace") as fh:
        for row in csv.DictReader(fh):
            psi, total = number(row["PSI"]), number(row["Sum"])
            if psi is not None and total is not None and total >= READ_MIN:
                rep1[row["Gene"]] = psi
    acc = Acc()
    with (BASE / "I28 Control Replicate 2.csv").open(newline="", encoding="utf-8",
                                                     errors="replace") as fh:
        for row in csv.DictReader(fh):
            psi, total = number(row["PSI"]), number(row["Sum"])
            if psi is None or total is None or total < READ_MIN:
                continue
            other = rep1.get(row["Gene"])
            if other is not None:
                acc.add(other, psi)
    res = acc.result()
    if res:
        res["sd_noise_single_replicate"] = round(res["sd_diff"] / math.sqrt(2), 4)
        res["meaning"] = ("Nhiễu PSI mức peptide trên thang toàn peptidome. So với bộ scanning "
                          "(sd chênh ~0,46 ở reads>=10) để biết nhiễu là tính chất của assay "
                          "hay của riêng thư viện quét.")
    report["control_replicate_reproducibility"] = res
    report["control_replicate_reproducibility"]["read_min"] = READ_MIN


def main():
    report = {"source": ("Mendeley 10.17632/32h94v2yv2.2, "
                         "I28 GPS Peptidome Screen and MLN4924 and SVM.zip")}
    for frac in ("10", "5"):
        path = BASE / ("Machine Learning Prediction of I28 Peptidome PSI "
                       f"(Complete Coverage & {frac}% Training).csv")
        if path.exists():
            print(f"đọc SVM {frac}% ...", flush=True)
            audit_svm(path, f"svm_{frac}pct_training", report)
    print("đọc hai replicate control ...", flush=True)
    audit_replicates(report)

    report["implication_for_topic"] = (
        "Zhang 2023 đã công bố một mô hình dự đoán PSI trên chính peptidome này. Mọi tuyên bố "
        "đóng góp của đề tài phải so với baseline này, không chỉ so với DEGRONOPEDIA / "
        "MetaDegron / PAP. Lưu ý phạm vi khác nhau: baseline này dự đoán PSI mức PEPTIDE, còn "
        "đề tài nhắm footprint và hiệu ứng đột biến mức RESIDUE — là nhiệm vụ khác, nên đây "
        "không phải đối thủ trực tiếp, nhưng phải nêu và không được bỏ qua."
    )
    path = Path(__file__).parent / "gps-peptidome-audit.json"
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nghi:", path.name)


if __name__ == "__main__":
    main()
