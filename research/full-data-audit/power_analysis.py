#!/usr/bin/env python3
"""Lực thống kê của tập test 221–322 footprint — việc chặn của đề tài.

Câu hỏi: với tập test chia theo cụm protein (221–322 footprint), có phát hiện được cải thiện
precision@3 so với mốc 0,6045 hay không?

Điểm then chốt: effect size phải lấy từ dư địa THẬT. Audit 12/10 ngầm dùng 0,1747
(= 0,7792 − 0,6045), nhưng 0,7792 là oracle đọc chính nhãn test nên không đạt được.
[label_ceiling.py] đo được trần thực nghiệm bằng replicate độc lập: 0,6514.
Dư địa thật = 0,6514 − 0,6045 = 0,0469.

Phép kiểm: precision@3 là trung bình macro theo peptide, mỗi peptide cho một giá trị trong
{0, 1/3, 2/3, 1}. So sánh với mốc dùng kiểm one-sample trên chênh lệch theo từng peptide
(paired, vì cùng peptide được chấm bởi cả hai phương pháp) — đây là thiết kế đúng và mạnh hơn
kiểm hai mẫu độc lập. Độ lệch chuẩn của chênh lệch theo peptide được ĐO từ dữ liệu thật
(rep1-chấm-rep2 so với baseline thành phần trên cùng peptide), không giả định.

Dùng: power_analysis.py
"""

import json
import math
import random
import re
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
PROC = TOPIC / "data/processed"
PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)$")

READ_MIN, DEGRON_PSI_MAX, RESCUE_DELTA, MIN_POS, TOP_K = 10, 3.0, 1.0, 21, 3
SEED = 0
TEST_SIZES = [221, 271, 301, 322, 500, 1000, 2000]
ALPHA = 0.05


def load_psi(condition):
    out = {}
    with (PROC / f"psi-{condition}.tsv").open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            psi, total = float(p[1]), float(p[2])
            if not math.isnan(psi) and total >= READ_MIN:
                out[p[0]] = psi
    return out


def load_sequences():
    import csv
    csv.field_size_limit(10 ** 7)
    path = (TOPIC / "data/interim/zhang-scanning-unzip/I28 Scanning (Completed)"
            / "Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv")
    seqs, subs = {}, {}
    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            m = PAT.match(r["Gene"])
            if not m:
                continue
            pep, pos = m.group("pep"), int(m.group("pos"))
            if pos == 0:
                seqs[pep] = r["AA.Seq"]
            else:
                subs[(pep, pos)] = r["AA.Seq"]
    return seqs, subs


def build_peptides(psi):
    wt, mut = {}, {}
    for name, value in psi.items():
        m = PAT.match(name)
        if not m:
            continue
        pep, pos = m.group("pep"), int(m.group("pos"))
        if pos == 0:
            wt[pep] = value
        else:
            mut.setdefault(pep, {})[pos] = value
    out = {}
    for pep, w in wt.items():
        d = mut.get(pep)
        if d and w <= DEGRON_PSI_MAX and len(d) >= MIN_POS:
            out[pep] = {p: v - w for p, v in d.items()}
    return out


def p_at_k(scores, labels, rng):
    positives = {p for p, d in labels.items() if d >= RESCUE_DELTA}
    if not positives:
        return None
    common = [p for p in scores if p in labels]
    if len(common) < TOP_K:
        return None
    rng.shuffle(common)
    common.sort(key=lambda p: -scores[p])
    return sum(1 for p in common[:TOP_K] if p in positives) / TOP_K


def normal_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def main():
    rng = random.Random(SEED)
    seqs, subs = load_sequences()
    f1, f2 = build_peptides(load_psi("rep1")), build_peptides(load_psi("rep2"))
    shared = sorted(f1.keys() & f2.keys())

    # Baseline "chỉ thành phần": score hằng trong nhóm cùng cặp (WT, thay vào), giá trị là
    # trung bình dPSI của nhóm — chính là oracle thành phần của audit 12/10, nhưng ước lượng
    # trên replicate 1 và chấm trên nhãn replicate 2 để không đọc nhãn test.
    diffs = []
    per_peptide = {"ceiling": [], "baseline": []}
    for pep in shared:
        labels = f2[pep]
        groups = {}
        skip = False
        for pos in f1[pep]:
            s, m = seqs.get(pep), subs.get((pep, pos))
            if not s or not m or pos > len(s) or pos > len(m):
                skip = True
                break
            groups.setdefault((s[pos - 1], m[pos - 1]), []).append(pos)
        if skip:
            continue
        comp = {}
        for members in groups.values():
            gm = sum(f1[pep][p] for p in members) / len(members)
            for p in members:
                comp[p] = gm
        a = p_at_k(f1[pep], labels, rng)      # trần thực nghiệm: replicate đầy đủ
        b = p_at_k(comp, labels, rng)         # baseline chỉ thành phần
        if a is None or b is None:
            continue
        per_peptide["ceiling"].append(a)
        per_peptide["baseline"].append(b)
        diffs.append(a - b)

    n = len(diffs)
    mean_d = sum(diffs) / n
    sd_d = math.sqrt(sum((d - mean_d) ** 2 for d in diffs) / (n - 1))
    mean_c = sum(per_peptide["ceiling"]) / n
    mean_b = sum(per_peptide["baseline"]) / n

    report = {
        "measured_on": {"n_peptides": n, "labels": "replicate 2", "scores": "replicate 1",
                        "note": "cả hai chấm trên cùng peptide nên dùng kiểm ghép cặp"},
        "observed": {
            "precision_at_3_replicate_ceiling": round(mean_c, 4),
            "precision_at_3_composition_baseline": round(mean_b, 4),
            "paired_mean_difference": round(mean_d, 4),
            "paired_sd_of_difference": round(sd_d, 4),
            "effect_size_dz": round(mean_d / sd_d, 4) if sd_d else None,
        },
        "power": {}, "mde": {},
    }

    z_a = 1.959963984540054        # hai phía, alpha = 0,05
    for n_test in TEST_SIZES:
        se = sd_d / math.sqrt(n_test)
        power = 1 - normal_cdf(z_a - mean_d / se) + normal_cdf(-z_a - mean_d / se)
        # MDE ở lực 0,80
        mde = (z_a + 0.8416212335729143) * se
        report["power"][f"n_{n_test}"] = round(power, 4)
        report["mde"][f"n_{n_test}"] = round(mde, 4)

    # cỡ mẫu cần để có lực 0,80 với đúng effect size đã đo
    if mean_d > 0:
        need = ((z_a + 0.8416212335729143) * sd_d / mean_d) ** 2
        report["n_required_for_power_080_at_observed_effect"] = math.ceil(need)

    # Hai mốc so sánh khác nhau, phải tách rõ:
    #  (a) baseline thành phần ước lượng trung thực từ replicate khác -> 0,4897 đo ở trên;
    #  (b) cận oracle 0,6045 của audit 12/10, chọn được nhờ NHÌN nhãn test nên không
    #      mô hình nào đạt; dùng nó làm mốc thì dư địa nhỏ hơn nhiều và sát biên phát hiện.
    bound = 0.6045
    gap_vs_bound = mean_c - bound
    report["against_theoretical_class_bound_0_6045"] = {
        "replicate_ceiling": round(mean_c, 4), "bound": bound,
        "headroom": round(gap_vs_bound, 4),
        "power": {}, "note": (
            "Dùng cùng sd ghép cặp đã đo. Đây là trường hợp sát biên: nếu đề tài cam kết "
            "'vượt 0,6045' thì ở cỡ test nhỏ nhất, MDE xấp xỉ bằng chính dư địa."),
    }
    for n_test in TEST_SIZES:
        se = sd_d / math.sqrt(n_test)
        power = (1 - normal_cdf(z_a - gap_vs_bound / se)
                 + normal_cdf(-z_a - gap_vs_bound / se))
        report["against_theoretical_class_bound_0_6045"]["power"][f"n_{n_test}"] = round(power, 4)
    if gap_vs_bound > 0:
        report["against_theoretical_class_bound_0_6045"]["n_required_for_power_080"] = math.ceil(
            ((z_a + 0.8416212335729143) * sd_d / gap_vs_bound) ** 2)

    report["caveat_sd"] = (
        "sd ghép cặp 0,2416 đo trên cặp (replicate đầy đủ, baseline thành phần). Một mô hình "
        "học được so với baseline có thể cho sd khác; khi có mô hình thật phải tính lại lực "
        "bằng sd của chính cặp đó, không dùng lại con số này.")

    report["interpretation"] = (
        "paired_mean_difference là dư địa THẬT giữa trần thực nghiệm (một phép đo lặp) và "
        "baseline chỉ thành phần, đo trên cùng peptide. Một mô hình học được không thể vượt "
        "trần này mà không khử nhiễu đo. So cỡ test 221–322 với "
        "n_required_for_power_080_at_observed_effect để biết tập test theo cụm protein có đủ "
        "lực hay không. MDE là mức cải thiện nhỏ nhất phát hiện được ở lực 0,80 với cỡ đó."
    )

    path = Path(__file__).parent / "power-analysis.json"
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nghi:", path.name)


if __name__ == "__main__":
    main()
