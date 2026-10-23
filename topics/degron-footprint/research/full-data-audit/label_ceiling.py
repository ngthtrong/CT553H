#!/usr/bin/env python3
"""Trần thực nghiệm do chính nhãn đặt ra, đo bằng hai replicate độc lập.

Câu hỏi quyết định của đề tài: mô hình phải vượt precision@3 = 0,6045 (cận của lớp mô hình
chỉ dựa thành phần, đo trên Replicate 1). Nhưng nếu **chính nhãn** không lặp lại được tới mức
đó, thì không có mô hình nào chứng minh được cải thiện: ta sẽ chỉ đo nhiễu.

Phép đo: coi ΔPSI của Replicate 1 như một "mô hình dự đoán hoàn hảo về sinh học nhưng có
nhiễu đo", rồi chấm nó trên nhãn của Replicate 2 bằng đúng precision@3 mà đề tài dùng.
Đây là **trần trên thực nghiệm**: một mô hình thật không thể biết nhiều hơn một phép đo lặp
của cùng đại lượng, trừ khi nó khử được nhiễu.

Đồng thời phân rã phương sai trên **cùng một cơ sở trung bình macro theo peptide** với audit
12/10, để so sánh hợp lệ với con số 35,0%.

Ngưỡng giữ nguyên: reads >= 10, PSI WT <= 3,0, >= 21 vị trí, dương nếu dPSI >= 1,0.
"""

import json
import math
import random
import re
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
PROC = TOPIC / "data/processed"
PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)$")

READ_MIN = 10
DEGRON_PSI_MAX = 3.0
RESCUE_DELTA = 1.0
MIN_POS = 21
TOP_K = 3
SEED = 0


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
    """AA.Seq theo peptide, lấy từ CSV của tác giả (chỉ để biết residue WT tại mỗi vị trí)."""
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
            pep, pos, aa = m.group("pep"), int(m.group("pos")), r["AA.Seq"]
            if pos == 0:
                seqs[pep] = aa
            else:
                subs[(pep, pos)] = aa
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
        if not d or w > DEGRON_PSI_MAX or len(d) < MIN_POS:
            continue
        out[pep] = {p: v - w for p, v in d.items()}
    return out


def precision_at_k(scores, labels, k=TOP_K, rng=None):
    """Tỉ lệ vị trí dương trong top-k theo score. Tie xử lý bằng chọn đều ngẫu nhiên."""
    positives = {p for p, d in labels.items() if d >= RESCUE_DELTA}
    if not positives:
        return None
    common = [p for p in scores if p in labels]
    if len(common) < k:
        return None
    rng.shuffle(common)                      # phá tie không thiên vị
    common.sort(key=lambda p: -scores[p])
    top = common[:k]
    return sum(1 for p in top if p in positives) / k


def main():
    rng = random.Random(SEED)
    seqs, subs = load_sequences()
    f1 = build_peptides(load_psi("rep1"))
    f2 = build_peptides(load_psi("rep2"))
    shared = sorted(f1.keys() & f2.keys())

    report = {"thresholds": {"read_min": READ_MIN, "degron_psi_max": DEGRON_PSI_MAX,
                             "rescue_delta": RESCUE_DELTA, "min_pos": MIN_POS,
                             "top_k": TOP_K, "seed": SEED},
              "n_peptides_covered_both": len(shared)}

    # --- A. trần thực nghiệm: rep1 chấm trên nhãn rep2, và ngược lại
    for src, dst, tag in ((f1, f2, "rep1_scores_on_rep2_labels"),
                          (f2, f1, "rep2_scores_on_rep1_labels")):
        vals, rand = [], []
        for pep in shared:
            labels = dst[pep]
            pos_labels = {p for p, d in labels.items() if d >= RESCUE_DELTA}
            if not pos_labels:
                continue
            v = precision_at_k(src[pep], labels, rng=rng)
            if v is None:
                continue
            vals.append(v)
            n_eval = len([p for p in src[pep] if p in labels])
            rand.append(TOP_K * len(pos_labels) / n_eval / TOP_K)
        if vals:
            report[tag] = {
                "n_peptides_scored": len(vals),
                "precision_at_3": round(sum(vals) / len(vals), 4),
                "random_baseline": round(sum(rand) / len(rand), 4),
            }

    # --- B. trần của chính nhãn, đối chiếu trực tiếp với 0,6045
    report["comparison"] = {
        "composition_bound_rep1_from_2026_10_12_audit": 0.6045,
        "unconstrained_oracle_rep1_from_2026_10_12_audit": 0.7792,
        "random_rep1_from_2026_10_12_audit": 0.1204,
        "meaning": ("Nếu precision@3 của replicate-chấm-replicate THẤP HƠN 0,6045 thì mục "
                    "tiêu G2 'vượt 0,6045' không kiểm chứng được trên nhãn một-replicate: "
                    "một phép đo lặp của cùng đại lượng sinh học còn không đạt mức đó."),
    }

    # --- C. phân rã phương sai, trung bình macro theo peptide, cùng cơ sở audit 12/10
    def pair_key(pep, pos):
        s, m = seqs.get(pep), subs.get((pep, pos))
        if not s or not m or pos > len(s) or pos > len(m):
            return None
        return (s[pos - 1], m[pos - 1])

    shares = {"total_var": [], "resid_after_pair_oracle": [], "noise_var": []}
    skipped = 0
    for pep in shared:
        common = [p for p in f1[pep] if p in f2[pep]]
        if len(common) < MIN_POS:
            continue
        # phương sai quan sát (dùng trung bình hai replicate làm giá trị tốt nhất của nhãn)
        avg = {p: (f1[pep][p] + f2[pep][p]) / 2 for p in common}
        m = sum(avg.values()) / len(avg)
        total = sum((v - m) ** 2 for v in avg.values()) / len(avg)
        # dư sau oracle trung bình theo nhóm cùng cặp thay thế
        groups = {}
        ok = True
        for p in common:
            key = pair_key(pep, p)
            if key is None:
                ok = False
                break
            groups.setdefault(key, []).append(p)
        if not ok:
            skipped += 1
            continue
        resid = 0.0
        for members in groups.values():
            gm = sum(avg[p] for p in members) / len(members)
            resid += sum((avg[p] - gm) ** 2 for p in members)
        resid /= len(common)
        # phương sai nhiễu của GIÁ TRỊ TRUNG BÌNH hai replicate = Var(d1-d2)/4
        nv = sum((f1[pep][p] - f2[pep][p]) ** 2 for p in common) / len(common) / 4
        if total > 0:
            shares["total_var"].append(total)
            shares["resid_after_pair_oracle"].append(resid / total)
            shares["noise_var"].append(nv / total)

    n = len(shares["total_var"])
    if n:
        resid_share = sum(shares["resid_after_pair_oracle"]) / n
        noise_share = sum(shares["noise_var"]) / n
        report["variance_decomposition_macro_per_peptide"] = {
            "n_peptides": n, "n_skipped_missing_sequence": skipped,
            "residual_share_after_pair_oracle": round(resid_share, 4),
            "noise_share_of_total": round(noise_share, 4),
            "noise_share_of_residual": round(noise_share / resid_share, 4)
            if resid_share > 0 else None,
            "learnable_context_share_upper_bound": round(max(0.0, resid_share - noise_share), 4),
            "basis": ("Nhãn = trung bình hai replicate. Var nhiễu của trung bình = Var(d1-d2)/4. "
                      "Mọi tỉ lệ chuẩn hóa theo phương sai của chính peptide rồi lấy trung bình "
                      "macro theo peptide, cùng cơ sở với con số 35,0% của audit 12/10."),
        }

    path = Path(__file__).parent / "label-ceiling.json"
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nghi:", path.name)


if __name__ == "__main__":
    main()
