#!/usr/bin/env python3
"""Nạp hai nguồn nhãn MỨC RESIDUE của đề tài, dùng chung cho mọi script trong thư mục này.

Hai nguồn, hai vai (xem D-028 mục 5 và reframe §11.3):

  * **Bộ quét** (`scan`): mỗi vị trí của peptide bị thay bằng MỘT acid amin.
    Nhãn ô = ΔPSI(vị trí) so với PSI hoang dã đo trực tiếp (`_mut0`).
    Cỡ lớn (nghìn peptide), một thay thế mỗi vị trí.
  * **Bộ bão hòa** (`sat`): mỗi vị trí bị thay bằng CẢ 20 acid amin, hai nửa độc lập.
    Nhãn ô = ΔPSI(vị trí, acid amin) so với WT nội tại (trung vị ô đồng nghĩa).
    Cỡ nhỏ (n = 91 sau ngưỡng degron), đầy đủ ma trận.

Mọi ngưỡng giữ đúng như các phiên trước để số so sánh được:
reads >= 10 · peptide degron nếu PSI WT <= 3,0 · ô dương nếu ΔPSI >= 1,0 · >= 21 vị trí đo được.

Quy tắc tile `(n-1)*23`, dài 28, đã được kiểm hai lần ở `full-data-audit/saturation_matrix.py`;
ở đây giữ nguyên kiểm (a): peptide nào có trình tự thật trong bộ quét mà suy ra không khớp thì BỊ LOẠI.
"""

import csv
import gzip
import math
import re
import statistics
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
PROC = TOPIC / "data/processed"
RAW = TOPIC / "data/raw"
INTERIM = TOPIC / "data/interim"
SCAN_CSV = (INTERIM / "zhang-scanning-unzip/I28 Scanning (Completed)"
            / "Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv")
CLUSTER_TSV = INTERIM / "protein-id30-cov80_cluster.tsv"

SCAN_PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)$")
SAT_PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)(?P<aa>[a-z])$")

TILE_STEP = 23
TILE_LEN = 28
READ_MIN = 10
DEGRON_PSI_MAX = 3.0
RESCUE_DELTA = 1.0
MIN_POS = 21
AAS = "ACDEFGHIKLMNPQRSTVWY"


# ---------------------------------------------------------------- nạp nguyên liệu

def load_psi(condition, read_min=READ_MIN):
    out = {}
    with (PROC / f"psi-{condition}.tsv").open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            psi, total = float(p[1]), float(p[2])
            if not math.isnan(psi) and total >= read_min:
                out[p[0]] = psi
    return out


def load_scan_csv():
    """Trình tự hoang dã theo peptide + acid amin thay vào ở từng (peptide, vị trí)."""
    csv.field_size_limit(10 ** 7)
    seqs, subs = {}, {}
    with SCAN_CSV.open(newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            m = SCAN_PAT.match(r["Gene"])
            if not m:
                continue
            pep, pos, aa = m.group("pep"), int(m.group("pos")), r["AA.Seq"]
            if pos == 0:
                seqs[pep] = aa.rstrip("*").upper()
            else:
                subs[(pep, pos)] = aa.rstrip("*").upper()
    return seqs, subs


def load_uniprot():
    up = {}
    with gzip.open(RAW / "human-reviewed-2026-10-12.fasta.gz", "rt") as fh:
        acc, buf = None, []
        for line in fh:
            if line.startswith(">"):
                if acc:
                    up[acc] = "".join(buf)
                acc = line.split("|")[1] if "|" in line else None
                buf = []
            else:
                buf.append(line.strip())
        if acc:
            up[acc] = "".join(buf)
    return up


def load_clusters():
    """accession -> đại diện cụm (MMseqs2 id30 cov80)."""
    rep = {}
    with CLUSTER_TSV.open(encoding="utf-8") as fh:
        for line in fh:
            r, m = line.rstrip("\n").split("\t")[:2]
            rep[m] = r
    return rep


def accession(peptide):
    return peptide.split("_")[0]


def derive_sequence(pep, uniprot):
    parts = pep.split("_")
    try:
        n = int(parts[-1])
    except ValueError:
        return None
    protein = uniprot.get(parts[0])
    if not protein:
        return None
    seq = protein[(n - 1) * TILE_STEP:(n - 1) * TILE_STEP + TILE_LEN]
    return seq if len(seq) == TILE_LEN else None


# ---------------------------------------------------------------- bộ quét (scanning)

def build_scanning(psi, seqs, subs, degron_psi_max=DEGRON_PSI_MAX, min_pos=MIN_POS):
    """-> {peptide: {"seq":..., "wt": psi0, "cells": {pos: (aa_mut, dpsi)}}}

    Chỉ giữ peptide degron (PSI WT <= ngưỡng) và đủ `min_pos` vị trí đo được.
    """
    wt, cells = {}, {}
    for name, value in psi.items():
        m = SCAN_PAT.match(name)
        if not m:
            continue
        pep, pos = m.group("pep"), int(m.group("pos"))
        if pos == 0:
            wt[pep] = value
        else:
            cells.setdefault(pep, {})[pos] = value
    out = {}
    for pep, w in wt.items():
        if w > degron_psi_max:
            continue
        seq = seqs.get(pep)
        if not seq or len(seq) < TILE_LEN:
            continue
        d = {}
        for pos, value in cells.get(pep, {}).items():
            aa = subs.get((pep, pos))
            if not aa or pos > len(seq) or len(aa) != len(seq):
                continue
            if aa[pos - 1] not in AAS or seq[pos - 1] not in AAS:
                continue
            d[pos] = (aa[pos - 1], value - w)
        if len(d) >= min_pos:
            out[pep] = {"seq": seq, "wt": w, "cells": d}
    return out


# ---------------------------------------------------------------- bộ bão hòa

def build_saturation(sat_a, sat_b, seqs, uniprot,
                     degron_psi_max=DEGRON_PSI_MAX, ext_wt=None):
    """-> {peptide: {"seq":..., "wt_internal": {"a":..,"b":..}, "cells": {(pos,aa): (da, db)}}}

    Ngưỡng peptide degron áp trên **WT nội tại** (trung bình hai nửa của trung vị ô đồng
    nghĩa) — đúng cách `pap_baseline.py` phần C đã làm, nên con số tái lập được mốc n = 91.
    Không dùng điều kiện `wt` (quét BAG6 WT) làm mốc, theo D-028 mục 5 ("không trộn BAG6 WT").

    `ext_wt` (tuỳ chọn, ví dụ PSI của `rep1`) chỉ để **ghi kèm** phép đo WT ngoài cùng
    genotype, phục vụ phân tích độ nhạy; nó không tham gia lọc.
    """
    def parse(table):
        cells = {}
        for name, value in table.items():
            m = SAT_PAT.match(name)
            if m:
                cells.setdefault(m.group("pep"), {})[
                    (int(m.group("pos")), m.group("aa").upper())] = value
        return cells

    ca, cb = parse(sat_a), parse(sat_b)
    out = {}
    for pep in sorted(set(ca) | set(cb)):
        truth = seqs.get(pep)
        derived = derive_sequence(pep, uniprot)
        if truth:
            if not derived or derived[:len(truth)] != truth:
                continue           # kiểm (a) thất bại -> loại, không đoán
            seq = truth
        elif derived:
            seq = derived
        else:
            continue
        if len(seq) < TILE_LEN:
            continue
        wt_cells = {(i, r) for i, r in enumerate(seq, start=1)}
        refs = {}
        for tag, half in (("a", ca), ("b", cb)):
            d = half.get(pep, {})
            vals = [d[k] for k in wt_cells if k in d]
            if len(vals) >= 10:
                refs[tag] = statistics.median(vals)
        if len(refs) < 2:
            continue
        psi_wt = (refs["a"] + refs["b"]) / 2
        if psi_wt > degron_psi_max:
            continue
        keys = (set(ca.get(pep, {})) & set(cb.get(pep, {}))) - wt_cells
        keys = {k for k in keys if k[1] in AAS and 1 <= k[0] <= len(seq)
                and seq[k[0] - 1] in AAS and seq[k[0] - 1] != k[1]}
        if not keys:
            continue
        out[pep] = {
            "seq": seq, "psi_wt": psi_wt,
            "psi_wt_external": (ext_wt or {}).get(f"{pep}_mut0"),
            "wt_internal": refs,
            "cells": {k: (ca[pep][k] - refs["a"], cb[pep][k] - refs["b"])
                      for k in sorted(keys)},
        }
    return out


def load_all(degron_psi_max=DEGRON_PSI_MAX):
    seqs, subs = load_scan_csv()
    uniprot = load_uniprot()
    rep1 = load_psi("rep1")
    scan = build_scanning(rep1, seqs, subs, degron_psi_max=degron_psi_max)
    sat = build_saturation(load_psi("sat_a"), load_psi("sat_b"),
                           seqs, uniprot, degron_psi_max=degron_psi_max, ext_wt=rep1)
    return {"scan": scan, "sat": sat, "seqs": seqs, "subs": subs,
            "uniprot": uniprot, "clusters": load_clusters(),
            "psi_rep1": rep1}


if __name__ == "__main__":
    data = load_all()
    rep = data["clusters"]
    for tag in ("scan", "sat"):
        peps = data[tag]
        accs = {accession(p) for p in peps}
        cl = {rep.get(a, a) for a in accs}
        n_cells = sum(len(v["cells"]) for v in peps.values())
        print(f"{tag}: {len(peps)} peptide · {len(accs)} protein · {len(cl)} cụm cov80 "
              f"· {n_cells} ô")
