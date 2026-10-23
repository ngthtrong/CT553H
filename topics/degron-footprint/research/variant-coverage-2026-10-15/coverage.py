#!/usr/bin/env python3
"""Đo độ phủ biến thể missense ClinVar trên thư viện peptide degron của đề tài.

Câu hỏi phép kiểm này trả lời (điều kiện 1 của C-18): nếu đổi câu hỏi khung từ
"residue nào trong peptide quan trọng" sang "đột biến missense này có phá degron
hay không", thì có **bao nhiêu** biến thể thật nằm trong phạm vi đề tài?

Năm tầng độ phủ, phải báo tách nhau vì ý nghĩa khác nhau:

  * **sat**  — peptide bộ bão hòa (ma trận 19 thay thế đầy đủ). Biến thể rơi vào đây
               được **chấm bằng đúng ô đã đo** ⇒ xác minh được từng biến thể một.
  * **scan** — peptide degron bộ quét (một thay thế mỗi vị trí). Biến thể rơi vào đây
               có nhãn **mức vị trí** nhưng thường không đúng acid amin ⇒ xác minh
               được *vị trí* có là footprint hay không, không xác minh được ô.
  * **lib**  — toàn bộ thư viện quét, kể cả peptide KHÔNG phải degron. Đây là miền
               **đầu vào trong phân bố** của mô hình, không phải miền có nhãn dương.
  * **pepdome_degron** — tile peptidome GPS có PSI <= 3,0: vùng **đã đo là quyết định
               độ bền**, trên toàn hệ protein người. Biến thể rơi vào đây là biến thể
               mà câu hỏi "có phá degron không" **có nghĩa**, dù chưa có nhãn mức residue.
  * **pepdome_all** — mọi tile peptidome đo được (reads >= 10). Miền áp dụng rộng nhất;
               **không** phải bằng chứng vùng đó là degron.

Ba tầng đầu là thư viện **chọn lọc** (≈1,5 tile mỗi protein), hai tầng sau là bản tile
**đầy đủ** bước 23 trên toàn proteome. Lẫn hai loại này là lỗi đọc số nghiêm trọng nhất
của phép kiểm này.

Mọi ngưỡng lấy từ `residue_data.py` của phiên 8 (reads >= 10 · degron nếu PSI WT <= 3,0
· >= 21 vị trí đo được) để các con số nối được với D-031.

Kiểm chứng bắt buộc, không bỏ qua: toạ độ residue của ClinVar theo transcript RefSeq
**không** đương nhiên bằng toạ độ UniProt canonical. Script vì vậy **chỉ nhận** biến thể
mà acid amin hoang dã mà ClinVar ghi **khớp** acid amin tại đúng vị trí đó trong trình tự
UniProt. Tỉ lệ khớp được báo ra; biến thể không khớp bị loại và đếm riêng.

Chạy từ thư mục gốc repo:
    .venv/bin/python -I topics/degron-footprint/research/variant-coverage-2026-10-15/coverage.py
"""

import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / "data" / "README.md").exists())
sys.path.insert(0, str(TOPIC / "research/residue-task-derisk-2026-10-15"))

import residue_data as rd          # noqa: E402

CLINVAR = TOPIC / "data/raw/clinvar/variant_summary.txt.gz"
PEPDOME_XLSX = (TOPIC / "data/raw/geo-gse240610"
                / "GSE240610_Supplementary_Table_1_Raw_data_of_GPS_peptidome_screens__"
                  "Control_+_MLN4924_.xlsx")
PEPDOME_CACHE = TOPIC / "data/interim/gps-peptidome-rep1.tsv"
PEPDOME_SHEET = "I28 Control Replicate 1"
OUT = HERE / "coverage.json"
# Hai bảng theo từng biến thể lớn (4,5 MB + 1,4 MB) nên đi vào data/processed/ như mọi
# đầu ra sinh lại được, không vào research/. Chỉ bản tổng hợp nhỏ nằm cạnh script.
PROC_OUT = TOPIC / "data/processed"

TIERS = ("sat", "scan", "lib", "pepdome_degron", "pepdome_degron_psi20",
         "pepdome_degron_psi15", "pepdome_all")
LABELLED_TIERS = ("sat", "scan")

# p.Arg273His  ·  p.Arg273Ter  ·  p.Arg273=  ·  p.Arg273del ...
PCHANGE = re.compile(r"\(p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})\)")

THREE_TO_ONE = {
    "Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C", "Gln": "Q",
    "Glu": "E", "Gly": "G", "His": "H", "Ile": "I", "Leu": "L", "Lys": "K",
    "Met": "M", "Phe": "F", "Pro": "P", "Ser": "S", "Thr": "T", "Trp": "W",
    "Tyr": "Y", "Val": "V",
}

# Nhóm ý nghĩa lâm sàng. ClinVar trộn nhiều nhãn trong một ô, nên phân nhóm theo
# chuỗi con, thứ tự ưu tiên từ trên xuống.
def sig_bucket(s):
    t = s.lower()
    if "conflicting" in t:
        return "conflicting"
    if "pathogenic" in t and "benign" not in t:
        return "pathogenic"          # gồm cả Likely pathogenic
    if "uncertain" in t:
        return "vus"
    if "benign" in t:
        return "benign"
    return "other"


# Degron lái ung thư đã được công nhận trong y văn, để kiểm điểm.
# [chưa xác minh trong repo] — danh sách lấy từ kiến thức nền, phải trích dẫn
# trước khi đưa vào tài liệu đề tài.
DRIVER_DEGRONS = {
    "CTNNB1": "P35222",    # exon 3, Ser33/Ser37/Thr41/Ser45 — gan, đại trực tràng
    "NFE2L2": "Q16236",    # motif DLG (29-31) + ETGE (79-82) — phổi vảy
    "MYC":    "P01106",    # degron FBXW7 quanh Thr58/Ser62
    "CCNE1":  "P24864",    # degron FBXW7
    "HIF1A":  "Q16665",    # degron VHL, Pro402/Pro564
    "NOTCH1": "P46531",    # PEST domain
    "FBXW7":  "Q969H0",    # chính E3, để đối chiếu
    "TP53":   "P04637",    # đối chứng: TP53 KHÔNG phải degron driver điển hình
}


def uniprot_genes():
    """accession -> gene symbol, và gene symbol -> {accession} (snapshot UniProt người)."""
    acc2gene, gene2acc = {}, defaultdict(set)
    path = TOPIC / "data/raw/human-reviewed-2026-10-12.fasta.gz"
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if not line.startswith(">"):
                continue
            parts = line.split("|")
            if len(parts) < 3:
                continue
            acc = parts[1]
            m = re.search(r"\bGN=(\S+)", line)
            if not m:
                continue
            gene = m.group(1)
            acc2gene[acc] = gene
            gene2acc[gene].add(acc)
    return acc2gene, gene2acc


def peptide_span(pep):
    """peptide -> (accession, start, end) theo quy tắc tile (n-1)*23, dài 28, 1-indexed."""
    parts = pep.split("_")
    try:
        n = int(parts[-1])
    except ValueError:
        return None
    start = (n - 1) * rd.TILE_STEP + 1
    return parts[0], start, start + rd.TILE_LEN - 1


def cache_peptidome():
    """Rút sheet replicate 1 của Table S1 ra TSV ở interim/ (475k dòng, xlsx đọc rất chậm)."""
    if PEPDOME_CACHE.exists():
        return
    import openpyxl
    wb = openpyxl.load_workbook(PEPDOME_XLSX, read_only=True, data_only=True)
    ws = wb[PEPDOME_SHEET]
    n = 0
    PEPDOME_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with PEPDOME_CACHE.open("w", encoding="utf-8") as out:
        out.write("peptide\treads\tpsi\n")
        for row in ws.iter_rows(values_only=True):
            pep, reads, psi = (row + (None, None, None))[:3]
            if not pep or pep in ("Peptide",) or str(pep).startswith("Table S1"):
                continue
            out.write(f"{pep}\t{reads}\t{psi}\n")
            n += 1
    wb.close()
    print(f"[cache] {PEPDOME_CACHE.name}: {n} dòng", file=sys.stderr)


def load_peptidome(read_min=rd.READ_MIN, degron_psi_max=rd.DEGRON_PSI_MAX):
    """-> (set peptide đo được, set peptide degron). Cùng ngưỡng với residue_data."""
    cache_peptidome()
    all_peps, degron = set(), set()
    with PEPDOME_CACHE.open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            pep, reads, psi = line.rstrip("\n").split("\t")
            try:
                if float(reads) < read_min:
                    continue
                value = float(psi)
            except ValueError:
                continue                      # 'NA' hoặc ô rỗng
            all_peps.add(pep)
            if value <= degron_psi_max:
                degron.add(pep)
    return all_peps, degron


def build_spans(data):
    """Các tầng -> {accession: [(start, end, peptide), ...]}.

    Ba ngưỡng degron cho tầng peptidome, vì ngưỡng PSI <= 3,0 của D-025 được chọn cho
    thư viện quét, **chưa ai kiểm nó chặt đến đâu trên toàn peptidome**. Nếu 1/3 tile
    của proteome vượt ngưỡng thì "nằm trong degron" gần như không mang thông tin, và
    điều đó phải nói ra.
    """
    pepdome_all, pepdome_degron = load_peptidome()
    _, pepdome_d20 = load_peptidome(degron_psi_max=2.0)
    _, pepdome_d15 = load_peptidome(degron_psi_max=1.5)
    universes = {
        "sat": set(data["sat"]),
        "scan": set(data["scan"]),
        "lib": set(data["seqs"]),
        "pepdome_degron": pepdome_degron,
        "pepdome_degron_psi20": pepdome_d20,
        "pepdome_degron_psi15": pepdome_d15,
        "pepdome_all": pepdome_all,
    }
    spans = {}
    for tag, peps in universes.items():
        idx = defaultdict(list)
        for pep in peps:
            s = peptide_span(pep)
            if s:
                acc, start, end = s
                idx[acc].append((start, end, pep))
        spans[tag] = idx
    return spans, {k: len(v) for k, v in universes.items()}


def measured_positions(data):
    """(peptide, vị trí) và (peptide, vị trí, acid amin) đã đo, cho hai tầng có nhãn.

    Phân biệt này quan trọng: khớp **vị trí** chỉ cho phép nói "vị trí này có là footprint
    hay không"; khớp **đúng ô** (có cả acid amin thay vào) mới cho phép nói "biến thể
    đúng của ClinVar này đã được đo".

    Bộ bão hòa khoá ô theo `(vị trí, acid amin)` — chữ cái thường trong ID peptide
    (`_mut10a`) là **danh tính acid amin** thay vào, không phải số thứ tự; `build_saturation`
    dựa vào đúng tính chất đó để tìm ô đồng nghĩa.
    Bộ quét khoá theo `vị trí`, giá trị `(acid amin, ΔPSI)` — mỗi vị trí **một** thay thế.
    """
    pos_only, exact = {}, {}
    for tag in LABELLED_TIERS:
        sp, se = set(), set()
        for pep, rec in data[tag].items():
            for key, value in rec["cells"].items():
                if isinstance(key, tuple):              # bão hòa: (pos, aa)
                    pos, aa = key
                else:                                   # quét: pos -> (aa, dpsi)
                    pos, aa = key, (value[0] if isinstance(value, tuple) else None)
                sp.add((pep, pos))
                if aa:
                    se.add((pep, pos, aa.upper()))
        pos_only[tag], exact[tag] = sp, se
    return pos_only, exact


def stream_clinvar():
    """Sinh bản ghi biến thể missense, đã bỏ trùng VariationID.

    ClinVar ghi mỗi biến thể **một dòng cho mỗi assembly** (GRCh37 + GRCh38), nên phải
    bỏ trùng. `ClinicalSignificance` là phân loại **dòng mầm**; phân loại **soma** nằm ở
    cột `Oncogenicity` riêng — mạch ung thư của C-18 cần cột sau, nên lấy cả hai.
    """
    seen = set()
    with gzip.open(CLINVAR, "rt", errors="replace") as fh:
        header = fh.readline().lstrip("#").rstrip("\n").split("\t")
        col = {name: i for i, name in enumerate(header)}
        need = ("Name", "GeneSymbol", "ClinicalSignificance", "VariationID", "Type")
        missing = [n for n in need if n not in col]
        if missing:
            raise SystemExit(f"ClinVar thiếu cột: {missing}; header={header[:12]}")
        onc_col = col.get("Oncogenicity")
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) <= col["Name"]:
                continue
            vid = f[col["VariationID"]]
            if vid in seen:
                continue
            m = PCHANGE.search(f[col["Name"]])
            if not m:
                continue
            ref3, pos, alt3 = m.group(1), int(m.group(2)), m.group(3)
            ref1, alt1 = THREE_TO_ONE.get(ref3), THREE_TO_ONE.get(alt3)
            if not ref1 or not alt1 or ref1 == alt1:
                continue                      # bỏ nonsense/synonymous/không chuẩn
            seen.add(vid)
            gene = f[col["GeneSymbol"]].split(";")[0].split("|")[0].strip()
            onc = f[onc_col].strip() if onc_col is not None and len(f) > onc_col else ""
            yield (gene, ref1, pos, alt1, sig_bucket(f[col["ClinicalSignificance"]]),
                   vid, onc)


def main():
    if not CLINVAR.exists():
        raise SystemExit(f"chưa có {CLINVAR}")

    data = rd.load_all()
    spans, universe_sizes = build_spans(data)
    measured, measured_exact = measured_positions(data)
    uniprot = data["uniprot"]
    acc2gene, gene2acc = uniprot_genes()

    # Hợp của mọi tầng: peptidome phủ gần như toàn proteome, nên KHÔNG được giới hạn
    # theo thư viện quét (làm vậy sẽ cắt mất chính tầng rộng nhất).
    lib_accs = set()
    for tag in TIERS:
        lib_accs |= set(spans[tag])
    lib_genes = defaultdict(set)
    for acc in lib_accs:
        g = acc2gene.get(acc)
        if g:
            lib_genes[g].add(acc)

    stats = Counter()
    hits = {tag: Counter() for tag in TIERS}
    cell_hits = {tag: Counter() for tag in LABELLED_TIERS}
    exact_hits = {tag: Counter() for tag in LABELLED_TIERS}
    hit_rows = []
    driver_rows = []

    onc_hits = {tag: Counter() for tag in TIERS}
    onc_total = Counter()

    for gene, ref1, pos, alt1, bucket, vid, onc in stream_clinvar():
        stats["missense_total"] += 1
        if onc:
            onc_total[onc] += 1
        accs = lib_genes.get(gene)
        if not accs:
            stats["gene_not_in_library"] += 1
            continue
        stats["gene_in_library"] += 1

        # Kiểm chứng toạ độ: acid amin hoang dã phải khớp UniProt.
        ok_acc = None
        for acc in accs:
            seq = uniprot.get(acc)
            if seq and pos <= len(seq) and seq[pos - 1] == ref1:
                ok_acc = acc
                break
        if not ok_acc:
            stats["refaa_mismatch"] += 1
            continue
        stats["refaa_validated"] += 1

        for tag in TIERS:
            for start, end, pep in spans[tag].get(ok_acc, ()):
                if start <= pos <= end:
                    hits[tag][bucket] += 1
                    if onc:
                        onc_hits[tag][onc] += 1
                    offset = pos - start + 1
                    if tag in LABELLED_TIERS:
                        if (pep, offset) in measured[tag]:
                            cell_hits[tag][bucket] += 1
                        if (pep, offset, alt1) in measured_exact[tag]:
                            exact_hits[tag][bucket] += 1
                    if tag == "scan":
                        hit_rows.append({
                            "variation_id": vid, "gene": gene, "accession": ok_acc,
                            "protein_pos": pos, "ref": ref1, "alt": alt1,
                            "significance": bucket, "peptide": pep,
                            "offset_in_peptide": offset,
                            "position_measured": (pep, offset) in measured["scan"],
                        })
                    break           # mỗi biến thể đếm một lần cho mỗi tầng

        if gene in DRIVER_DEGRONS:
            driver_rows.append({
                "gene": gene, "pos": pos, "ref": ref1, "alt": alt1,
                "significance": bucket,
                **{f"in_{tag}": any(s <= pos <= e for s, e, _ in spans[tag].get(ok_acc, ()))
                   for tag in TIERS},
            })

    # Độ phủ các degron lái ung thư: protein có trong thư viện không, tile nào.
    driver_cover = {}
    for gene, acc in DRIVER_DEGRONS.items():
        driver_cover[gene] = {
            "accession": acc,
            "in_uniprot_snapshot": acc in uniprot,
            "length": len(uniprot.get(acc, "")),
            **{f"{tag}_tiles": sorted((s, e) for s, e, _ in spans[tag].get(acc, ()))
               for tag in ("sat", "scan", "lib", "pepdome_degron")},
            "pepdome_all_n_tiles": len(spans["pepdome_all"].get(acc, ())),
        }

    result = {
        "universe_peptides": universe_sizes,
        "universe_proteins": {t: len(spans[t]) for t in spans},
        "measured_cells": {t: len(measured[t]) for t in measured},
        "clinvar_file_bytes": CLINVAR.stat().st_size,
        "pipeline": dict(stats),
        "hits_by_tier": {t: dict(hits[t]) for t in hits},
        "hits_total_by_tier": {t: sum(hits[t].values()) for t in hits},
        "hits_at_measured_position": {t: dict(cell_hits[t]) for t in cell_hits},
        "hits_at_exact_measured_cell": {t: dict(exact_hits[t]) for t in exact_hits},
        "measured_exact_cells": {t: len(measured_exact[t]) for t in measured_exact},
        "tile_fraction_degron": {
            t: round(universe_sizes[t] / universe_sizes["pepdome_all"], 4)
            for t in ("pepdome_degron", "pepdome_degron_psi20", "pepdome_degron_psi15")},
        "oncogenicity_all": dict(onc_total),
        "oncogenicity_by_tier": {t: dict(onc_hits[t]) for t in onc_hits},
        "driver_degron_coverage": driver_cover,
        "driver_variants_found": len(driver_rows),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    PROC_OUT.mkdir(parents=True, exist_ok=True)
    (PROC_OUT / "clinvar-scan-hits.json").write_text(
        json.dumps(hit_rows, indent=1, ensure_ascii=False), encoding="utf-8")
    (PROC_OUT / "clinvar-driver-variants.json").write_text(
        json.dumps(driver_rows, indent=1, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
