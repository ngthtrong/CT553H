from comp import *
from part1 import A, FIG
import math, os


def s06(d):
    s = d.slide("Measured degron regions are enriched for disease variants, at region level", section=2, size=26, title_h=0.5,
                notes="Slide trả lời câu GVHD nhấn mạnh nhất (vì sao cần nghiên cứu). Số 2,148 là TỰ ĐO (ClinVar 12/10/2026, 2,56 triệu missense, MH theo 3.114 protein). "
                      "BA DÒNG 'does and does not say' là bắt buộc, không tách khỏi con số (D-033, D-036): mức residue ba phép đo đều nhất quán với rỗng (AUC 0,5166 [0,479; 0,554]). "
                      "Không nói 'validated against ClinVar', 'degrons are mutation hotspots', 'pathogenic because it breaks a degron'. "
                      "Nếu hỏi vì sao bỏ khung ung thư: 7/8 degron lái ung thư kinh điển không hiện trong assay (D-035). PNPO D33V là số của tác giả. "
                      "Chân slide: ghi công ClinVar (PMID 29165669) + câu phủ nhận chẩn đoán, bắt buộc.")
    # left: two directions
    r1 = d.rect(MX, 1.2, 5.75, 0.92, fill=CORAL_T, shape="round", nm="direction 1",
                paras=[P(runs=[("Degron destroyed", {"bold": True, "color": CORAL}), ("  →  the protein escapes degradation and accumulates", {})], size=13)], margin=0.15)
    r2 = d.rect(MX, 2.22, 5.75, 1.18, fill=TEAL_T, shape="round", nm="direction 2",
                paras=[P(runs=[("Degron created", {"bold": True, "color": "1F7A6F"}), ("  →  a healthy protein is cleared early: loss of function, e.g. PNPO D33V (Voutsinos et al., Sci Adv 2026)", {})], size=13)], margin=0.15)
    d.rect(MX, 3.55, 5.75, 2.15, fill=PANEL, shape="round", nm="limits panel")
    d.text(MX + 0.15, 3.62, 5.45, 2.05, [P("What this number does and does not say", size=13, bold=True, color=INK),
                                          B("It is a region-level association; whether the individual residues in a degron carry the disease signal is not established by our data", size=12),
                                          B("Variants are not over-represented in degrons by location: 33.4% of variants vs 32.4% of tiles", size=12),
                                          B("Conservation and disorder are not yet controlled for", size=12)], nm="limits")
    # right: forest plot
    d.text(6.65, 1.1, 6.08, 0.75, [P("How much clinical variation falls in degrons? We measured it.", size=15, bold=True),
                                    P("ClinVar, 2.56 million missense variants, mapped onto every peptide the GPS screen measured", size=12, color=MUTED, space=1)], nm="right heading")
    d.rect(6.65, 1.9, 6.08, 2.35, fill="FFFFFF", line=LINE, shape="round", nm="forest panel")
    d.text(6.8, 1.96, 5.8, 0.5, [P("Pathogenic vs benign, within the same protein: inside a measured degron vs elsewhere in that protein", size=11.5, color=INK)], nm="forest label")
    x0, x1 = 7.1, 12.3

    def X(v):
        return x0 + (math.log(v) - math.log(0.5)) / (math.log(3) - math.log(0.5)) * (x1 - x0)
    d.line(x0, 3.75, x1, 3.75, color=GREY, lw=1, nm="axis")
    for v in (0.5, 1, 2, 3):
        d.line(X(v), 3.72, X(v), 3.8, color=GREY, lw=1, nm=f"tick {v}")
        d.text(X(v) - 0.3, 3.82, 0.6, 0.25, [P(str(v), size=10, color=MUTED, align="c")], nm=f"tick label {v}")
    d.text(x0, 4.02, x1 - x0, 0.22, [P("odds ratio (log scale)", size=10, color=MUTED, align="c")], nm="axis title")
    d.line(X(1), 2.6, X(1), 3.75, color=INK, lw=1.2, dash=True, nm="OR = 1")
    ci = d.line(X(2.072), 3.2, X(2.227), 3.2, color=CORAL, lw=4, nm="CI")
    pt = d.rect(X(2.148) - 0.11, 3.09, 0.22, 0.22, fill=CORAL, shape="oval", nm="OR point")
    lb = d.text(X(2.148) - 1.0, 2.62, 2.0, 0.4, [P("OR 2.148  [2.072, 2.227]", size=13, bold=True, color=CORAL, align="c")], nm="OR label")
    st1 = d.rect(6.65, 4.4, 2.95, 0.85, fill=STEEL_T, shape="round", nm="stat strata",
                 paras=[P("3,114 proteins", size=17, bold=True, color=STEEL), P("strata (Mantel–Haenszel)", size=11, color=INK)], margin=0.12)
    st2 = d.rect(9.78, 4.4, 2.95, 0.85, fill=STEEL_T, shape="round", nm="stat VUS",
                 paras=[P("530,412 VUS", size=17, bold=True, color=STEEL), P("inside these regions, no tool assigns a mechanism", size=11, color=INK)], margin=0.12)
    ch = chip(d, 6.65, 5.4, 6.08, "region level only: residue level not established", fill=AMBER_T, color="6B5210", size=12, h=0.34, nm="region chip")
    d.anim([r1, r2], [ci, pt, lb], [st1, st2, ch])
    d.text(MX, 5.85, W - 2 * MX, 0.5, [P("Degrons are also a drug-design target: targeted protein degradation works by recruiting the degradation machinery to a protein of interest. Knowing which residues control degron strength is upstream of that design problem.", size=12)], nm="drug design")
    source(d, "Own measurement, ClinVar variant_summary of 12 Oct 2026 (Landrum et al., NAR 2018, PMID 29165669). ClinVar classifications are not for diagnostic use; this thesis does not predict disease or claim therapeutic effect.", y=6.45)


def s07(d):
    s = d.slide("GPS profiling turns degradation into a number: low PSI means a strong degron", section=3, title_h=0.5,
                notes="Chiều của PSI và ΔPSI là HAI CHỖ đã nhầm trong tài liệu học của repo: PSI thấp = bị phân hủy nhanh = degron mạnh; ΔPSI > 0 = đột biến làm bền. In to, giữ đúng chiều ở mọi hình. "
                      "'in the dataset used here' vì số bin khác nhau giữa các bài (Zhang 6, Voutsinos 4, Larsen 4 cổng, thang đảo). "
                      "GIF: GFP (PDB 1EMA) của Erik A. Rodriguez, CC BY-SA 4.0, đã giảm kích thước/giảm số khung từ bản gốc Commons. Trích dẫn: Koren et al., Cell 173(7):1622, 2018.")
    steps = [("1", "Synthesise a library of short peptides, each fused to a fluorescent reporter (GFP)"),
             ("2", "Express one peptide per cell, next to a second, stable reporter as internal control"),
             ("3", "Sort cells by the reporter ratio with FACS into stability bins"),
             ("4", "Sequence each bin; a peptide's bin distribution gives its stability score")]
    d.text(MX, 1.15, 5.9, 0.3, [P("Global Protein Stability (GPS) profiling, introduced by Koren et al., Cell 2018", size=13, bold=True, color=STEEL)], nm="intro")
    for i, (n, t) in enumerate(steps):
        y = 1.6 + i * 0.98
        d.rect(MX, y, 5.9, 0.88, fill=PANEL, shape="round", nm=f"step {n} panel")
        d.rect(MX + 0.15, y + 0.19, 0.5, 0.5, fill=STEEL, shape="oval", nm=f"step {n} number", paras=[P(n, size=16, bold=True, color=BG, align="c")], margin=0)
        d.text(MX + 0.85, y + 0.08, 4.9, 0.74, [P(t, size=13.5)], anchor="m", nm=f"step {n}")
    d.rect(6.75, 1.6, 2.3, 2.935, fill="000000", shape="rect", nm="gif black card")
    d.pic(os.path.join(A, "gfp-small.gif"), 6.75, 1.6, w=2.3, h=2.935, alt="Rotating structure of green fluorescent protein (GFP), chromophore in yellow")
    d.text(6.75, 4.62, 2.3, 0.9, [P("GFP, the reporter (PDB 1EMA). Erik A. Rodriguez, CC BY-SA 4.0, Wikimedia Commons; reduced size and frame rate.", size=10, color=MUTED)], nm="gif caption")
    # PSI box
    d.rect(9.3, 1.6, 3.43, 2.2, fill="FFFFFF", line=LINE, shape="round", nm="psi panel")
    d.text(9.45, 1.68, 3.15, 0.3, [P("Protein Stability Index (PSI)", size=13, bold=True)], nm="psi head")
    d.pic(os.path.join(A, "psi-gradient.png"), 9.45, 2.12, w=3.13, h=0.3, alt="Gradient from coral (PSI 1) to teal (PSI 6)")
    d.text(9.45, 2.12, 3.13, 0.3, [P("1", size=12, bold=True, color=BG), ], nm="psi 1", check=False, margin=0.06)
    d.text(9.45, 2.12, 3.13, 0.3, [P("6", size=12, bold=True, color=BG, align="r")], nm="psi 6", check=False, margin=0.06)
    d.text(9.45, 2.5, 1.5, 0.7, [P("low PSI", size=12, bold=True, color=CORAL), P("degraded fast = strong degron", size=11)], nm="low")
    d.text(11.1, 2.5, 1.5, 0.7, [P("high PSI", size=12, bold=True, color="1F7A6F", align="r"), P("stable = not a degron", size=11, align="r")], nm="high")
    d.text(9.45, 3.3, 3.15, 0.4, [P("Scale 1…6 (6 bins) in the dataset used here", size=10.5, color=MUTED)], nm="scale note")
    card(d, 9.3, 3.95, 3.43, 1.7, "Mutation effect", [P(runs=[("ΔPSI = PSI(mutant) − PSI(wild type)", {"bold": True})], size=13, space=2),
                                                       P("ΔPSI > 0: the mutation stabilised the peptide, so the substituted residue was part of a working degron.", size=12, space=3)],
         accent=CORAL, tint=CORAL_T)
    source(d, "Koren I, Timms RT, Kula T, Xu Q, Li MZ, Elledge SJ. Cell 173(7):1622–1635.e14, 2018. DOI 10.1016/j.cell.2018.04.028", y=6.0)


def s08(d):
    s = d.slide("Prior work at a glance", section=3, title_h=0.5, size=28,
                notes="Slide dễ sai tên nhất, dùng đúng danh sách tác giả ở phụ lục A1. Hai điều phải giữ đúng: (a) Larsen 2025 là PREPRINT; (b) Degformer KHÔNG có bài báo, ghi 'GitHub, no publication'. "
                      "Mức bằng chứng: Degpred [CHƯA KIỂM] chỉ tóm tắt; DEGRONOPEDIA, MetaDegron, DegronMD [NGUỒN]; Degformer đọc toàn bộ mã nguồn. "
                      "Animation: hiện 9 dòng, dừng, rồi dòng 'This thesis' để người nghe tự thấy chỗ trống ở cột prediction unit.")
    hdr = ["Work", "Year · venue", "Method group", "Prediction unit", "Labels", "Output"]
    rows = [hdr,
            ["Koren et al.", "2018 · Cell", "experimental screen", "peptide (C-terminal)", "GPS, measured", "degron catalogue"],
            ["Degpred (Hou et al.)", "2022 · BMC Biol", "BERT sequence model", "degron location in protein", "curated motifs + E3 interactions", "proteome-wide degron map"],
            ["Zhang et al.", "2023 · Mol Cell", "screen + ML", "peptide", "GPS + mutagenesis, measured", "fingerprints, DegronID; SVM for PSI"],
            ["DegronMD (Xu et al.)", "2023 · Mol Biol Evol", "pattern + ML knowledgebase", "degron location; mutation impact", "curated + evolutionary / structural features", "degrome map, 89,318 mutations"],
            ["DEGRONOPEDIA (Szulc et al.)", "2024 · NAR", "database + ML web server", "degron motif; terminus stability", "curated motifs, structure", "annotation, proteolysis simulation"],
            ["MetaDegron (Zheng et al.)", "2024 · Brief Bioinform", "PLM + multimodal features", "is this peptide an E3 degron", "~300 curated degrons, 21 E3s", "per-E3 degron classification"],
            ["Voutsinos et al. (PAP)", "2026 · Sci Adv", "experimental map + CNN", "30-aa tile", "GPS, measured, >200k tiles", "tile degron score"],
            ["Larsen et al.", "2025 · bioRxiv (preprint)", "experimental map", "30-aa tile (TFs)", "sort-seq abundance, measured", "TF degron map"],
            ["Degformer", "2026 · GitHub, no publication", "transformer", "peptide (28-mer)", "Zhang 2023 tables", "PSI; 28×20 ΔPSI matrix"]]
    colw = [2.15, 1.85, 1.95, 2.1, 2.2, 1.88]
    grp = {1: STEEL_T, 7: STEEL_T, 8: STEEL_T, 2: TEAL_T, 4: TEAL_T, 5: TEAL_T, 6: TEAL_T, 3: PANEL, 9: PANEL}
    gf, yb = d.table(MX, 1.2, colw, rows, size=11.5, bold_first_col=True, row_fills=grp, min_row=0.34, nm="prior work table")
    last = [["This thesis", "·", "·", [("individual residue", {"bold": True, "color": CORAL})], [("GPS mutagenesis, measured", {"bold": True})], [("28×20 ΔPSI matrix + per-position map", {"bold": True})]]]
    lt, yb2 = d.table(MX, yb + 0.08, colw, last, size=11.5, header=False, bold_first_col=True, row_fills={0: CORAL_T}, nm="this thesis row")
    leg_y = yb2 + 0.1
    for i, (c, t) in enumerate([(STEEL_T, "experimental maps"), (TEAL_T, "databases, motif and language-model tools"), (PANEL, "screen + ML on mutagenesis")]):
        d.rect(MX + [0, 2.2, 6.2][i], leg_y + 0.02, 0.22, 0.16, fill=c, line=LINE, nm=f"legend {i + 1}")
        d.text(MX + [0, 2.2, 6.2][i] + 0.3, leg_y - 0.02, 3.6, 0.25, [P(t, size=10, color=MUTED)], nm=f"legend text {i + 1}")
    d.text(MX + 8.7, leg_y - 0.02, 3.4, 0.25, [P("Degformer read from source code, not a paper", size=10, color=MUTED, align="r")], nm="evidence note")
    d.anim([lt])


def s09(d):
    s = d.slide("Group 1: motif and database tools give broad coverage, but their labels are curated", section=3, title_h=0.5, size=25,
                notes="Mức bằng chứng từng bài khác nhau: Degpred [CHƯA KIỂM], DEGRONOPEDIA/MetaDegron/DegronMD [NGUỒN]. Vì vậy các dòng 'fall short' viết ở mức 'not reported' / 'often random peptides', KHÔNG viết 'they leak' hay 'numbers are wrong'. "
                      "AUC 0,87–0,90 của MetaDegron: nói 'not comparable', đừng nói 'inflated'. Việc cần làm cho luận văn (không chặn buổi gặp): đọc toàn văn Degpred, kiểm cách chia tập của MetaDegron.")
    d.text(MX, 1.15, 7.5, 0.3, [P("Degpred (2022) · DegronMD (2023) · DEGRONOPEDIA (2024) · MetaDegron (2024)", size=13, bold=True, color=STEEL)], nm="tools")
    d.text(MX, 1.5, 7.5, 1.95, [P("What they achieved", size=14, bold=True),
                               B("Moved degron identification from a handful of known motifs to proteome scale (DegronMD reports 18,000+ new degron instances)", size=12.5),
                               B("Added surrounding biology: ubiquitination sites, disorder, structure, E3 assignment; DEGRONOPEDIA simulates proteolysis", size=12.5),
                               B("Delivered usable web tools with batch submission: the state of the art for “where are the degrons in my protein?”", size=12.5),
                               B("MetaDegron shows a protein language model beats feature-based prediction, across 21 E3s", size=12.5)], nm="achieved")
    d.text(MX, 3.5, 7.5, 0.3, [P("Where they fall short for this thesis's question", size=14, bold=True)], nm="short head")
    rows = [["Limitation", "Why it matters here"],
            ["Labels are curated motifs (a few hundred); negatives are often random peptides", "Measured negatives are much harder, so reported AUCs are not comparable to a measured-label benchmark"],
            ["Prediction unit is a motif or protein region", "They answer where is a degron, not which residue inside it matters"],
            ["Train/test similarity control not reported for small curated sets", "Homologous leakage cannot be excluded"]]
    d.table(MX, 3.85, [3.3, 4.2], rows, size=11.5, nm="limitations")
    # resolution axis
    d.rect(8.5, 1.15, 4.23, 4.85, fill="FFFFFF", line=LINE, shape="round", nm="axis panel")
    d.text(8.65, 1.2, 3.9, 0.3, [P("Resolution of the answer", size=13, bold=True)], nm="axis title")
    d.line(8.85, 1.65, 8.85, 5.75, color=GREY, lw=1.5, arrow=True, nm="resolution axis")
    levels = [("protein", "DegronMD (proteome-wide degrome map)", STEEL_T), ("region", "Degpred (degron location in protein)", STEEL_T), ("motif", "DEGRONOPEDIA · MetaDegron", STEEL_T)]
    shp = []
    for i, (lv, tool, col) in enumerate(levels):
        y = 1.65 + i * 1.0
        r = d.rect(9.05, y, 3.5, 0.82, fill=col, shape="round", nm=f"level {lv}", paras=[P(lv, size=13, bold=True, color=STEEL), P(tool, size=11)], margin=0.12)
        shp.append(r)
    emp = d.rect(9.05, 4.65, 3.5, 0.95, fill=AMBER_T, line="B08A1E", dash=True, shape="round", nm="level residue (empty)",
                 paras=[P("residue", size=14, bold=True, color=CORAL), P("no tool in this group answers here", size=11)], margin=0.12)
    d.anim(shp, [emp])
    d.rect(MX, 5.7, 7.5, 0.65, fill=CORAL_T, shape="round", nm="gap banner",
           paras=[P(runs=[("The gap this group leaves: ", {"bold": True, "color": CORAL}), ("these tools locate degrons; none is trained on measured mutation effects, so none ranks residues inside a degron.", {})], size=12)], margin=0.12)
    source(d, "Evidence level differs per work: Degpred seen through its abstract only; the other three read from their paper or tool page. Not comparable with a measured-label benchmark.", y=6.45)
