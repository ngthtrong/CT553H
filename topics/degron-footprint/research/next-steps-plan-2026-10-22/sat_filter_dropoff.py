"""Đếm vì sao bộ bão hòa thô còn 91 peptide trong benchmark G2, và nới ngưỡng degron
thì thêm được bao nhiêu peptide.

Chỉ **đọc** pipeline nhãn hiện có (`residue_data.py`), không huấn luyện, không ghi vào
`data/`. Kết quả ghi `sat-filter-dropoff.json` cạnh file này.

Chạy từ gốc repo:
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/next-steps-plan-2026-10-22/sat_filter_dropoff.py
"""
import sys, statistics, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "residue-task-derisk-2026-10-15"))
import residue_data as rd

seqs, subs = rd.load_scan_csv()
uniprot = rd.load_uniprot()
sat_a, sat_b = rd.load_psi("sat_a"), rd.load_psi("sat_b")

def parse(table):
    cells = {}
    for name, value in table.items():
        m = rd.SAT_PAT.match(name)
        if m:
            cells.setdefault(m.group("pep"), {})[(int(m.group("pos")), m.group("aa").upper())] = value
    return cells

ca, cb = parse(sat_a), parse(sat_b)
allpep = sorted(set(ca) | set(cb))
reasons = {}
psi_wt_kept, psi_wt_dropped_thresh = [], []
for pep in allpep:
    truth = seqs.get(pep); derived = rd.derive_sequence(pep, uniprot)
    if truth:
        if not derived or derived[:len(truth)] != truth:
            reasons[pep] = "seq_mismatch"; continue
        seq = truth
    elif derived:
        seq = derived
    else:
        reasons[pep] = "no_sequence"; continue
    if len(seq) < rd.TILE_LEN:
        reasons[pep] = "too_short"; continue
    wt_cells = {(i, r) for i, r in enumerate(seq, start=1)}
    refs = {}
    for tag, half in (("a", ca), ("b", cb)):
        d = half.get(pep, {})
        vals = [d[k] for k in wt_cells if k in d]
        if len(vals) >= 10:
            refs[tag] = statistics.median(vals)
    if len(refs) < 2:
        reasons[pep] = "wt_refs_lt_10_cells"; continue
    psi_wt = (refs["a"] + refs["b"]) / 2
    if psi_wt > rd.DEGRON_PSI_MAX:
        reasons[pep] = "not_degron_psi_wt_gt_3"; psi_wt_dropped_thresh.append(psi_wt); continue
    keys = (set(ca.get(pep, {})) & set(cb.get(pep, {}))) - wt_cells
    keys = {k for k in keys if k[1] in rd.AAS and 1 <= k[0] <= len(seq)
            and seq[k[0]-1] in rd.AAS and seq[k[0]-1] != k[1]}
    if not keys:
        reasons[pep] = "no_cells"; continue
    reasons[pep] = "KEPT"; psi_wt_kept.append(psi_wt)

from collections import Counter
c = Counter(reasons.values())
print("tổng peptide bão hòa thô:", len(allpep))
for k, v in c.most_common():
    print(f"  {k:28s} {v}")
if psi_wt_dropped_thresh:
    d = sorted(psi_wt_dropped_thresh)
    print(f"\nPSI WT của nhóm bị loại vì > 3,0: n={len(d)} min={d[0]:.2f} "
          f"median={statistics.median(d):.2f} max={d[-1]:.2f}")
    for t in (3.5, 4.0, 4.5, 5.0):
        print(f"  nếu nới ngưỡng degron lên {t}: thêm {sum(1 for x in d if x <= t)} peptide")

payload = {
    "note": "Đếm bằng cách chạy lại đúng chuỗi bộ lọc của residue_data.build_saturation, "
            "không huấn luyện lại G2. Ngưỡng hiện hành DEGRON_PSI_MAX = "
            f"{rd.DEGRON_PSI_MAX}.",
    "total_raw_peptides": len(allpep),
    "dropoff_counts": dict(c.most_common()),
    "psi_wt_kept": {"n": len(psi_wt_kept),
                    "median": statistics.median(psi_wt_kept) if psi_wt_kept else None},
    "psi_wt_dropped_by_degron_threshold": {
        "n": len(psi_wt_dropped_thresh),
        "min": min(psi_wt_dropped_thresh) if psi_wt_dropped_thresh else None,
        "median": statistics.median(psi_wt_dropped_thresh) if psi_wt_dropped_thresh else None,
        "max": max(psi_wt_dropped_thresh) if psi_wt_dropped_thresh else None,
    },
    "extra_peptides_if_threshold_relaxed_to": {
        str(t): sum(1 for x in psi_wt_dropped_thresh if x <= t)
        for t in (3.5, 4.0, 4.5, 5.0)
    },
}
(HERE / "sat-filter-dropoff.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"\n-> {HERE / 'sat-filter-dropoff.json'}")
