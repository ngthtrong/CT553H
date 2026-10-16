from comp import *
from part1 import A, FIG
import os, json, math
from PIL import Image

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "deck-external-2026-10-16", "assets", "measured-example.json")


def s15(d):
    s = d.slide("Task: from a 28-residue peptide to a 28×20 map of substitution effects", section=5, title_h=0.5, size=26,
                notes="'Unit of inference = protein cluster' phải nói sớm. Sau phiên 8 mức phạt đo được nhỏ hơn lo ngại: 91 peptide nằm trên 89 cụm; phạt thật nằm ở ô lồng trong peptide (ICC 0,0625, hệ số thiết kế 33,79, ≈1.416 ô độc lập hiệu dụng). Không trích 'dương giả trên 45%' như số của đề tài. "
                      "Thước đo chính của ma trận là AUROC mức ô (trần 0,9519), KHÔNG phải Spearman (trần 0,6989) (D-028 mục 2). Hình đầu ra là sơ đồ: không số liệu.")
    cells = strip(d, MX, 1.8, 28, 0.112, gap=0.01, fills=[LINE] * 28, nm="input residue")
    hot = [d.rect(MX + i * 0.122, 1.8, 0.112, 0.112, fill=CORAL, nm=f"input key residue {i}") for i in (14, 15, 16, 17, 18)]
    d.text(MX, 2.0, 3.4, 0.55, [P("input: a 28-residue peptide (optionally rASA, pLDDT)", size=11, color=MUTED)], nm="input label")
    d.rect(4.55, 1.45, 0.4, 0.3, fill=GREY, shape="rarrow", nm="arrow 1")
    mdl = d.rect(5.05, 1.3, 2.7, 1.2, fill=AMBER_T, line="B08A1E", dash=True, shape="round", nm="model (proposed)",
                 paras=[P("model", size=15, bold=True, color=STEEL, align="c"), P("architecture: see slide 21", size=11, align="c", color=MUTED)], margin=0.1)
    d.rect(7.85, 1.45, 0.4, 0.3, fill=GREY, shape="rarrow", nm="arrow 2")
    asp = Image.open(os.path.join(A, "grid-schematic.png")).size
    gw = 1.95
    d.pic(os.path.join(A, "grid-schematic.png"), 8.4, 1.15, w=gw, h=gw * asp[1] / asp[0], alt="Schematic 28 by 20 grid with a few highlighted cells")
    d.text(10.5, 1.15, 2.3, 1.0, [P("output 1", size=11, bold=True, color=STEEL), P("28 × 20 matrix: one ΔPSI per (position, amino acid)", size=11)], nm="output 1 label")
    d.pic(os.path.join(A, "dpsi-colorbar.png"), 10.5, 2.35, w=2.2, h=0.14, alt="Colour bar from coral (negative) through ivory (zero) to teal (positive)")
    d.text(10.5, 2.52, 2.3, 0.3, [P("− ΔPSI                 0                 + ΔPSI", size=10, color=MUTED, align="c")], nm="bar legend", check=False)
    chip(d, 10.5, 2.95, 2.23, "+ output 2: per-position map", fill=STEEL_T, color=STEEL, size=11, h=0.3, nm="output 2 chip")
    rows = [["Item", "Definition"],
            ["Input", "a 28-residue peptide sequence (optionally structural context: rASA, pLDDT)"],
            ["Output 1", "a 28 × 20 matrix of predicted ΔPSI: one value per (position, amino acid type)"],
            ["Output 2", "a per-position importance map: the 19 substitutions at each position aggregated"],
            ["Label", "ΔPSI = PSI(substituted) − PSI(wild type), both measured in the GPS assay"],
            ["Label sign", "ΔPSI > 0 → the substitution stabilised the peptide → the residue was part of a working degron"],
            ["Unit of inference", "the protein cluster (MMseqs2, ≥30% identity, 80% coverage), not the peptide and not the residue"]]
    d.table(MX, 3.55, [1.75, 5.95], rows, size=11.5, bold_first_col=True, nm="task definition")
    card(d, 8.55, 3.55, 4.18, 1.55, "Two framings of the same output, both reported",
         [P(runs=[("cell-level: ", {"bold": True}), ("is this one (position, amino acid) substitution stabilising? → AUROC", {})], size=11.5, space=2),
          P(runs=[("position-level: ", {"bold": True}), ("which positions carry the degron? → precision@3", {})], size=11.5, space=3)], accent=STEEL, tint=STEEL_T, hsize=12)
    card(d, 8.55, 5.2, 4.18, 1.4, "Scope", "Peptides are measured in isolation, fused to a reporter, in the cytosol. Results describe that system; transfer to intact proteins is a separate question with its own labels.",
         accent="8A6A12", tint=AMBER_T, hsize=12, bsize=11)
    d.anim([mdl])


def s16(d):
    dat = json.load(open(SRC))
    seq, order = dat["sequence"], dat["aa_order"]
    cells = {(c["position"], c["aa"]): c["mean_delta"] for c in dat["cells"]}
    foot = range(15, 20)
    n_pos = sum(1 for p in foot for a in order if (p, a) in cells and cells[(p, a)] > 0)
    n_tot = sum(1 for p in foot for a in order if (p, a) in cells)
    ex = dat["example_cell"]
    s = d.slide("One worked example: a measured ΔPSI matrix, read one cell and then one row", section=5, title_h=0.5, size=26,
                notes="Dữ liệu thật: peptide O00468_AGRN_82 từ psi-sat_a/b.tsv, chọn bằng quy tắc cố định (peptide đầu theo thứ tự từ điển có ≥520 ô đo), kèm SHA-256 đầu vào (assets/figs-meta.json). "
                      "⚠ Cả 91 peptide bão hòa đều ở phía ĐÁNH GIÁ trong thiết kế cross-source hiện hành, nên đây là minh họa nhãn đo, KHÔNG phải 'peptide trong tập train', không dùng để chọn mô hình. "
                      "Không dùng ví dụ M7V +1,4 của tài liệu học (đó là số giả định). Con số kiểm 5,0×10⁻⁷ là kết quả đo thật (research/full-data-audit/psi-build.json).")
    img = os.path.join(A, "example-heatmap.png")
    iw, ih = Image.open(img).size
    h = 5.3
    w = h * iw / ih
    X0, Y0 = MX, 1.15
    d.pic(img, X0, Y0, w=w, h=h, alt="Measured 28 by 20 ΔPSI heatmap for peptide O00468_AGRN_82 with per-position bars")

    def cx(j):
        return X0 + w * (0.09 + 0.64 * (j + 0.5) / 20)

    def cy(i):
        return Y0 + h * (0.06 + 0.77 * (i + 0.5) / 28)
    cw, ch_ = w * 0.64 / 20, h * 0.77 / 28
    ex_j = order.index(ex["aa"])
    ring = d.rect(cx(ex_j) - cw * 0.6, cy(ex["position"] - 1) - ch_ * 0.6, cw * 1.2, ch_ * 1.2, line=INK, lw=2.5, shape="oval", nm="example cell ring")
    row = d.rect(X0 + w * 0.09 - 0.03, cy(14) - ch_ * 0.5 - 0.02, w * 0.64 + 0.06, ch_ * 5 + 0.04, line=INK, lw=2.5, shape="rect", nm="footprint rows box")
    rx = X0 + w + 0.3
    d.text(rx, 1.15, W - MX - rx, 1.35, [P("Peptide  O00468_AGRN_82", size=13, bold=True, mono=True),
                                         P(dat["sequence"], size=11, mono=True, color=MUTED, space=2),
                                         P(runs=[("Wild-type PSI ", {}), (f"{dat['wt_psi']:.3f}", {"bold": True}), (": low, so this peptide is a degron", {})], size=12.5, space=4),
                                         P(f"{dat['n_measured_cells']} measured cells (28 positions × 19 substitutions), mean of two replicates", size=12, space=2)], nm="peptide info")
    c1 = card(d, rx, 2.75, W - MX - rx, 1.45, "Reading one cell",
              f"Position {ex['position']} → {ex['aa']}: ΔPSI = {ex['mean_delta']:.2f} (replicates {ex['replicate_a_delta']:.2f} and {ex['replicate_b_delta']:.2f}). Not stabilising, so no evidence this residue is part of the working degron.",
              accent=INK, tint=PANEL, hsize=12.5, bsize=11.5)
    c2 = card(d, rx, 4.3, W - MX - rx, 1.55, "Reading a row",
              f"At positions 15–19 ({seq[14:19]}) {n_pos} of {n_tot} measured substitutions stabilise the peptide. That block is its footprint, the residues the degron depends on.",
              accent=TEAL, tint=TEAL_T, hsize=12.5, bsize=11.5)
    d.anim([ring, c1], [row, c2])
    source(d, "Own rebuild from Zhang et al. 2023 raw counts; PSI reconstruction validated against the authors' table (max deviation 5.0 × 10⁻⁷ over 261,865 values). Measured illustration: saturation peptides sit on the evaluation side of the split, so this is not a training example.", y=6.55)


def bar(d, x, w, val, fill, nm, y0=5.9, ppu=15.4, vmin=0.70, line=None, lab=True, labcol=INK):
    top = y0 - (val - vmin) * ppu
    r = d.rect(x, top, w, y0 - top, fill=fill, line=line, shape="rect", nm=nm)
    t = d.text(x - 0.12, top - 0.26, w + 0.24, 0.24, [P(f"{val:.4f}", size=10.5, bold=True, color=labcol, align="c")], nm=nm + " value")
    return r, t


def s17(d):
    s = d.slide("Feasibility: ahead on the context axis, behind on the substitution matrix", section=5, title_h=0.5, size=26,
                notes="Slide trung thực nhất. (1) Câu chân slide 'measurement ceiling ≠ achievable performance' là BẮT BUỘC (lỗi đã mắc hai lần trong repo); không viết 'headroom to the ceiling'. (2) Không dùng 0,6045 và 0,7792 (oracle đọc nhãn test, D-025 loại). "
                      "(3) Thước đo chính là AUROC mức ô (D-028 mục 2); precision@3 để phụ lục. (4) 'Committed in advance': ngưỡng 0,0123 gắn với cặp ghép M3−M0 đã đo, cặp mới cần ước lượng lại. MDE cũ 0,071 đã sai (suy từ phương sai không ghép cặp). "
                      "(5) 'ranking reverses by metric' phải giữ: M3 thắng ở mức vị trí (Spearman 0,4440 vs 0,3553) và thua ở mức ô; báo từng thước đo riêng. Animation: bộ quét (thắng) → bộ bão hòa (chưa thắng) → mũi tên khoảng cách −0,0420.")
    y0, ppu, vmin = 5.85, 15.0, 0.70
    d.line(1.0, y0, 7.0, y0, color=INK, lw=1.25, nm="baseline")
    d.line(1.0, y0, 1.0, y0 - 0.27 * ppu, color=INK, lw=1.25, nm="y axis")
    for v in (0.70, 0.75, 0.80, 0.85, 0.90, 0.95):
        yy = y0 - (v - vmin) * ppu
        d.line(0.95, yy, 1.0, yy, color=INK, lw=1, nm=f"tick {v}")
        d.text(0.35, yy - 0.12, 0.55, 0.24, [P(f"{v:.2f}", size=10, color=MUTED, align="r")], nm=f"tick label {v}")
        d.line(1.0, yy, 7.0, yy, color=LINE, lw=0.5, nm=f"grid {v}")
    d.text(MX, 1.15, 6.5, 0.3, [P("Cell-level AUROC, own measurements (axis starts at 0.70)", size=11.5, bold=True)], nm="chart title")
    sc = [("ΔPAP w1", 0.7943, GREY), ("ΔPAP w7", 0.8357, GREY), ("M0", 0.8393, STEEL_T), ("M3", 0.8682, STEEL)]
    g1 = []
    for i, (lb, v, c) in enumerate(sc):
        x = 1.25 + i * 0.72
        r, t = bar(d, x, 0.55, v, c, f"scanning {lb}", y0, ppu, vmin, line=STEEL if c == STEEL_T else None)
        l = d.text(x - 0.1, y0 + 0.04, 0.75, 0.22, [P(lb, size=10, align="c")], nm=f"scanning label {lb}")
        g1 += [r, t, l]
    cl1 = d.line(1.15, y0 - (0.9458 - vmin) * ppu, 4.2, y0 - (0.9458 - vmin) * ppu, color=INK, lw=1.5, dash=True, nm="scanning ceiling")
    cl1t = d.text(1.15, y0 - (0.9458 - vmin) * ppu - 0.27, 3.0, 0.24, [P("ceiling 0.9458", size=10.5, bold=True)], nm="scanning ceiling label")
    sa = [("M0", 0.7071, STEEL_T), ("M3", 0.7273, STEEL), ("ΔPAP w1", 0.7693, CORAL)]
    g2 = []
    for i, (lb, v, c) in enumerate(sa):
        x = 4.75 + i * 0.72
        r, t = bar(d, x, 0.55, v, c, f"saturation {lb}", y0, ppu, vmin, line=STEEL if c == STEEL_T else None, labcol=CORAL if c == CORAL else INK)
        l = d.text(x - 0.1, y0 + 0.04, 0.75, 0.22, [P(lb, size=10, align="c")], nm=f"saturation label {lb}")
        g2 += [r, t, l]
    cl2 = d.line(4.65, y0 - (0.9519 - vmin) * ppu, 7.0, y0 - (0.9519 - vmin) * ppu, color=INK, lw=1.5, dash=True, nm="saturation ceiling")
    cl2t = d.text(4.65, y0 - (0.9519 - vmin) * ppu - 0.27, 2.4, 0.24, [P("ceiling 0.9519", size=10.5, bold=True)], nm="saturation ceiling label")
    tl = d.line(4.65, y0 - (0.7693 - vmin) * ppu, 6.8, y0 - (0.7693 - vmin) * ppu, color=CORAL, lw=1.5, dash=True, nm="target line")
    gap = d.line(5.75, y0 - (0.7273 - vmin) * ppu - 0.3, 5.75, y0 - (0.7693 - vmin) * ppu + 0.03, color=CORAL, lw=2.5, arrow=True, nm="gap arrow")
    gapt = d.text(4.6, y0 - (0.7693 - vmin) * ppu - 0.58, 1.1, 0.5, [P("−0.0420", size=12, bold=True, color=CORAL, align="r"), P("target", size=10.5, color=CORAL, align="r")], nm="gap label")
    d.text(1.1, y0 + 0.3, 3.1, 0.55, [P("Scanning set", size=11.5, bold=True), P("1,985 clusters · 2,994 peptides · 83,446 cells", size=10, color=MUTED)], nm="cluster title 1")
    d.text(4.65, y0 + 0.3, 2.5, 0.55, [P("Saturation matrix", size=11.5, bold=True), P("89 clusters · 91 peptides · 47,847 cells", size=10, color=MUTED)], nm="cluster title 2")
    d.anim(g1 + [cl1, cl1t], g2 + [cl2, cl2t], [tl, gap, gapt])
    rx, rw = 7.55, W - MX - 7.55
    card(d, rx, 1.15, rw, 1.1, "Where the model is ahead (paired by peptide, bootstrapped by cluster)",
         [P("M3 − M0 = +0.0289, CI [0.0264, 0.0313], wins on 72.5% of peptides", size=11.5, space=2), P("M3 − ΔPAP cnn2w7 = +0.0300, CI [0.0234, 0.0366]", size=11.5, space=2)], accent="1F7A6F", tint=TEAL_T, hsize=11.5)
    card(d, rx, 2.35, rw, 1.35, "Where it is still behind: the stated target",
         [P("Matrix: M3 − ΔPAP cnn2w1 = −0.0420, CI [−0.0580, −0.0256]", size=11.5, space=2), P("The ranking reverses by metric: at position level M3 has Spearman 0.4440 vs 0.3553, so claims are reported per metric, never pooled", size=11.5, space=2)], accent=CORAL, tint=CORAL_T, hsize=11.5)
    rows = [["Statistical power, computed in advance", ""],
            ["MDE, paired M3 − M0, saturation (80% power)", "0.0123"],
            ["Unpaired equivalent", "0.0491"],
            ["Scanning set", "0.0025–0.0036"],
            ["Cell ICC · design effect · effective cells", "0.0625 · 33.79 · ≈1,416"]]
    gf, yb = d.table(rx, 3.8, [3.2, rw - 3.2], rows, size=10.5, aligns=["l", "r"], nm="power", min_row=0.27)
    d.text(rx, yb + 0.06, rw, 0.95, [P("Committed in advance: a result below 0.0123 on that comparison is reported as indistinguishable, not as a win; new comparisons get their own estimate. Residue-set agreement between replicates is Jaccard 0.4965, so report uncertainty, not one confident answer.", size=10.5)], nm="commitment")
    source(d, "Measurement ceilings are an upper bound on what the labels can score, not a promise of achievable performance. All values: own measurements, scripts and JSON in the repository.", y=6.7)


def s18(d):
    s = d.slide("Data: seven sources, all pinned and checksummed, about 2.3 GB on disk", section=6, title_h=0.5, size=26,
                notes="ClinVar (nguồn 7): KHÔNG có giấy phép kiểu CC; điều kiện là ghi công + câu phủ nhận chẩn đoán phải đi theo đầu ra; file ghi đè mỗi tuần nên muốn tái lập phải dùng bản archive tháng 10/2026; vai là 'motivation only' (D-036). "
                      "Larsen: MIT là giấy phép phần mềm; Trọng ĐÃ GỬI email xin xác nhận MIT phủ cả file dữ liệu và đang chờ trả lời (C-11a), nên ô giấy phép ghi 'đang chờ xác nhận' thay vì 'đã hoàn tất'. "
                      "Nguồn 5 là mức tile, không có nhãn mức residue: vai là test chuyển assay.")
    rows = [["#", "Source", "Identifier pinned", "Licence", "Role in the thesis"],
            ["1", "Zhang et al. 2023: scanning + saturation mutagenesis", "Mendeley Data 10.17632/32h94v2yv2.2 (v2), all 5 files", "CC BY 4.0", "primary labels: measured mutation effects"],
            ["2", "Zhang et al. 2023: GPS peptidome PSI table", "NCBI GEO GSE240610", "GEO terms", "peptide-level context, author SVM comparison; application domain (116,702 degron tiles)"],
            ["3", "Voutsinos et al. 2026: tile library + PAP model", "GitHub KULL-Centre/_2025_Voutsinos_degron_cytosol @ 9b3eafa6", "MIT (code + data in repo)", "baseline model + benchmark population"],
            ["4", "MaveDB: 26 score sets, 9 genes", "API, URNs recorded", "CC0", "intact-protein transfer check"],
            ["5", "Larsen et al. 2025: transcription-factor tiles", "GitHub KULL-Centre/_2025_Larsen_… @ v1.0", "MIT in repo; coverage of the data file awaiting author reply", "cross-assay / cross-compartment test at tile level"],
            ["6", "UniProtKB/Swiss-Prot human 2026_03; AlphaFold DB v6 (8 structures)", "REST, snapshot pinned", "CC BY 4.0", "wild-type sequences; structural context"],
            ["7", "ClinVar variant_summary: 2.56 M missense variants", "NCBI FTP, file of 12 Oct 2026, SHA-256 recorded", "attribution required (PMID 29165669); not for diagnostic use", "motivation only: region-level enrichment (slide 6); not a validation target"]]
    gf, yb = d.table(MX, 1.2, [0.4, 3.1, 3.1, 2.35, 3.18], rows, size=11.5, bold_first_col=False, nm="data sources",
                     fills={(7, 4): AMBER_T, (7, 3): AMBER_T, (5, 3): AMBER_T})
    d.rect(MX, yb + 0.15, W - 2 * MX, 0.62, fill=TEAL_T, shape="round", nm="integrity",
           paras=[P(runs=[("Integrity: ", {"bold": True, "color": "1F7A6F"}), ("SHA-256 recorded for every file; the Mendeley set matches the publisher's checksums. Download dates, pinned revisions, per-file provenance and a reprocessing log live in the repository's data README.", {})], size=12)], margin=0.15)
    source(d, "Licences verified per source on 13–15 Oct 2026. Paper licence and data licence can differ: Larsen et al. is CC BY-NC-ND as a preprint, while its tile-level data file is MIT in the authors' GitHub repository.", y=yb + 0.9)
