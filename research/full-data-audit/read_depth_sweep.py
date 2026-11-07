#!/usr/bin/env python3
"""Nhiễu đo và trần nhãn thay đổi thế nào theo ngưỡng độ sâu reads.

Phát hiện dẫn tới script này: trong bộ bão hòa, 28 construct WT độc lập ở ~1.600 reads cho
PSI lệch nhau chỉ SD 0,031; còn ở ngưỡng reads >= 10 mà audit 12/10 dùng, nhiễu ΔPSI lên tới
SD ~0,30 và chiếm 75,9% phương sai dư. Vậy phần lớn "nhiễu" có thể chỉ là hệ quả của ngưỡng
reads quá thoáng, chứ không phải giới hạn của assay.

Nếu đúng, đây là tin tốt cho đề tài: siết ngưỡng reads sẽ lấy lại tín hiệu, đổi lấy số peptide
ít hơn. Script này đo chính xác sự đánh đổi đó, trên cả hai trục cùng lúc:
  - nhiễu đo và phần ngữ cảnh học được còn lại (phân rã phương sai macro theo peptide);
  - trần thực nghiệm precision@3 (một replicate chấm trên nhãn replicate kia);
  - số footprint còn lại, tức cỡ tập test khả dụng.
"""

import csv
import json
import math
import random
import re
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
PROC = TOPIC / "data/processed"
SCAN_CSV = (TOPIC / "data/interim/zhang-scanning-unzip/I28 Scanning (Completed)"
            / "Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv")
PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)$")

DEGRON_PSI_MAX, RESCUE_DELTA, MIN_POS, TOP_K = 3.0, 1.0, 21, 3
THRESHOLDS = [10, 25, 50, 100, 200, 400, 800]
SEED = 0


def load_raw(condition):
    out = {}
    with (PROC / f"psi-{condition}.tsv").open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            psi, total = float(p[1]), float(p[2])
            if not math.isnan(psi):
                out[p[0]] = (psi, total)
    return out


def load_pairs():
    csv.field_size_limit(10 ** 7)
    seqs, subs = {}, {}
    with SCAN_CSV.open(newline="", encoding="utf-8", errors="replace") as fh:
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


def build(raw, read_min):
    wt, mut = {}, {}
    for name, (psi, total) in raw.items():
        if total < read_min:
            continue
        m = PAT.match(name)
        if not m:
            continue
        pep, pos = m.group("pep"), int(m.group("pos"))
        if pos == 0:
            wt[pep] = psi
        else:
            mut.setdefault(pep, {})[pos] = psi
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


def main():
    r1, r2 = load_raw("rep1"), load_raw("rep2")
    seqs, subs = load_pairs()
    rows = []
    for read_min in THRESHOLDS:
        rng = random.Random(SEED)
        f1, f2 = build(r1, read_min), build(r2, read_min)
        shared = sorted(f1.keys() & f2.keys())
        n_fp1 = sum(1 for p, d in f1.items()
                    if any(v >= RESCUE_DELTA for v in d.values()))

        resid_shares, noise_shares = [], []
        ceil_vals, base_vals = [], []
        for pep in shared:
            common = [p for p in f1[pep] if p in f2[pep]]
            if len(common) < MIN_POS:
                continue
            avg = {p: (f1[pep][p] + f2[pep][p]) / 2 for p in common}
            m = sum(avg.values()) / len(avg)
            total_var = sum((v - m) ** 2 for v in avg.values()) / len(avg)
            groups, ok = {}, True
            for p in common:
                s, sm = seqs.get(pep), subs.get((pep, p))
                if not s or not sm or p > len(s) or p > len(sm):
                    ok = False
                    break
                groups.setdefault((s[p - 1], sm[p - 1]), []).append(p)
            if not ok:
                continue
            resid = 0.0
            for members in groups.values():
                gm = sum(avg[p] for p in members) / len(members)
                resid += sum((avg[p] - gm) ** 2 for p in members)
            resid /= len(common)
            nv = sum((f1[pep][p] - f2[pep][p]) ** 2 for p in common) / len(common) / 4
            if total_var > 0:
                resid_shares.append(resid / total_var)
                noise_shares.append(nv / total_var)
            # trần thực nghiệm và baseline thành phần, chấm trên nhãn replicate 2
            comp = {}
            for members in groups.values():
                gm = sum(f1[pep][p] for p in members) / len(members)
                for p in members:
                    comp[p] = gm
            a = p_at_k(f1[pep], f2[pep], rng)
            b = p_at_k(comp, f2[pep], rng)
            if a is not None and b is not None:
                ceil_vals.append(a)
                base_vals.append(b)

        n = len(resid_shares)
        if not n or not ceil_vals:
            continue
        resid = sum(resid_shares) / n
        noise = sum(noise_shares) / n
        diffs = [a - b for a, b in zip(ceil_vals, base_vals)]
        md = sum(diffs) / len(diffs)
        sd = math.sqrt(sum((d - md) ** 2 for d in diffs) / (len(diffs) - 1))
        rows.append({
            "read_min": read_min,
            "n_footprints_rep1": n_fp1,
            "n_peptides_shared_scored": len(ceil_vals),
            "residual_share_after_pair_oracle": round(resid, 4),
            "noise_share_of_total": round(noise, 4),
            "noise_share_of_residual": round(noise / resid, 4) if resid else None,
            "learnable_context_upper_bound": round(max(0.0, resid - noise), 4),
            "precision_at_3_replicate_ceiling": round(sum(ceil_vals) / len(ceil_vals), 4),
            "precision_at_3_composition_baseline": round(sum(base_vals) / len(base_vals), 4),
            "paired_gap": round(md, 4), "paired_sd": round(sd, 4),
            "mde_at_n_250_power_080": round((1.959963984540054 + 0.8416212335729143)
                                            * sd / math.sqrt(250), 4),
        })
        print(f"reads>={read_min:4d}  fp={n_fp1:5d}  scored={len(ceil_vals):5d}  "
              f"nhiễu/dư={noise / resid if resid else 0:.3f}  "
              f"ngữ cảnh≤{max(0.0, resid - noise):.4f}  "
              f"trần P@3={sum(ceil_vals) / len(ceil_vals):.4f}  "
              f"baseline={sum(base_vals) / len(base_vals):.4f}", flush=True)

    out = {"thresholds_swept": THRESHOLDS,
           "fixed": {"degron_psi_max": DEGRON_PSI_MAX, "rescue_delta": RESCUE_DELTA,
                     "min_pos": MIN_POS, "top_k": TOP_K, "seed": SEED},
           "rows": rows,
           "interpretation": (
               "Đọc theo hai cột cùng lúc: siết reads thì nhiễu giảm và phần ngữ cảnh học được "
               "tăng, nhưng n_footprints_rep1 giảm nên tập test nhỏ đi. Điểm chọn ngưỡng là nơi "
               "paired_gap còn lớn hơn mde_at_n_250_power_080 mà n_footprints vẫn đủ chia theo "
               "cụm protein.")}
    path = Path(__file__).parent / "read-depth-sweep.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\nghi:", path.name)


if __name__ == "__main__":
    main()
