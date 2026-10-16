from comp import *
from part1 import A
import os


def s23(d):
    s = d.slide("The software deliverable: residue-level predictions with measured uncertainty", section=8, title_h=0.5, size=26,
                notes="Lý lẽ 'vì sao là phần mềm' là chỗ quan trọng nhất: nút thắt của bài toán không chỉ là độ chính xác mà là nhiễu đo (75,9% phần dư sau oracle thành phần là nhiễu đo, full-data-audit). "
                      "⚠ Sản phẩm CHƯA XÂY: mọi ô là thiết kế. Bảng so sánh chỉ ghi những dòng đã kiểm (14–15/10/2026); KHÔNG thêm dòng 'batch submission' (MetaDegron và DegronMD đều có); ô nào chưa kiểm được thì ghi 'not checked'. Degformer CÓ xuất ma trận 28×20, nên khác biệt nằm ở ba dòng dưới. "
                      "'Calibrated' là mục tiêu thiết kế, chưa chọn phương pháp (ensemble theo seed hoặc conformal trên tập hiệu chỉnh tách theo cụm); đừng hứa độ phủ. Dịch vụ KHÔNG phát phân loại gây bệnh (D-036). Nếu hiển thị ClinVar thì ghi công và câu phủ nhận phải đi kèm. Lời D-034 không lên slide.")
    d.text(MX, 1.12, 5.2, 0.3, [P("The bottleneck is measurement noise, not accuracy alone", size=12.5, bold=True, color=STEEL)], nm="stat head")
    sts = [("75.9%", "of the residual after a composition oracle is measurement noise"), ("0.4965", "Jaccard of footprint residues between replicates"), ("0.9458 · 0.9519", "measurement ceilings")]
    for i, (n, t) in enumerate(sts):
        d.rect(MX + i * 1.76, 1.5, 1.68, 1.15, fill=PANEL, shape="round", nm=f"stat {i + 1}",
               paras=[P(n, size=17 if i < 2 else 13, bold=True, color=INK, align="c"), P(t, size=10, color=MUTED, align="c")], margin=0.08)
    d.text(MX, 2.75, 5.2, 0.75, [P("A tool that returns one confident answer misrepresents the data. The useful output is a prediction with its uncertainty, stated against what the assay can resolve.", size=11)], nm="so what")
    # flow
    fx = 6.1
    d.rect(fx, 1.12, W - MX - fx, 2.3, fill="FFFBEF", line="B08A1E", dash=True, shape="round", nm="flow panel")
    d.text(fx + 0.15, 1.17, 3, 0.25, [P("[proposed, not built]", size=10, bold=True, color="8A6A12")], nm="flow tag")
    q = d.rect(fx + 0.15, 1.85, 1.5, 0.85, fill="FFFFFF", line=GREY, shape="round", nm="query", paras=[P("query", size=12, bold=True, align="c"), P("sequence + optional mutation", size=10, color=MUTED, align="c")], margin=0.05)
    d.rect(fx + 1.7, 2.17, 0.25, 0.2, fill=GREY, shape="rarrow", nm="flow arrow 1")
    m = d.rect(fx + 2.0, 1.85, 1.1, 0.85, fill=STEEL, shape="round", nm="model", paras=[P("model", size=13, bold=True, color=BG, align="c")], margin=0.05)
    d.rect(fx + 3.15, 2.17, 0.25, 0.2, fill=GREY, shape="rarrow", nm="flow arrow 2")
    o = d.rect(fx + 3.45, 1.7, 3.0 - 0.1, 1.15, fill="FFFFFF", line=TEAL, shape="round", nm="outputs",
               paras=[P("28 × 20 ΔPSI heatmap with per-cell uncertainty", size=11, bold=True, align="c"), P("+ per-position bar, next to the measurement ceiling", size=10, color=MUTED, align="c")], margin=0.08)
    for i, t in enumerate(["OOD", "compartment", "provenance"]):
        chip(d, fx + 3.45 + i * 1.0, 1.35, 0.92, t, fill=AMBER_T, line="B08A1E", size=10, h=0.26, nm=f"flag {t}")
    d.anim([q, m], [o])
    rows = [["Feature", "Detail"],
            ["28 × 20 ΔPSI + map", "for any 28-residue peptide or protein window"],
            ["Per-cell uncertainty", "calibrated, reported next to the measured ceiling"],
            ["Arbitrary mutation", "user-specified substitution, not a precomputed table"],
            ["API", "programmatic access beside the web interface"],
            ["Out-of-distribution flag", "warns for a protein cluster unseen in training"],
            ["Compartment flag", "labels are cytosolic; nuclear or secreted contexts flagged"],
            ["Label provenance", "each measured cell shown with source and replicate values"]]
    d.table(MX, 3.6, [1.85, 3.5], rows, size=10, bold_first_col=True, nm="features")
    crows = [["Tool", "Output unit", "API", "Any mutation on the web", "Uncertainty vs measured ceiling", "Provenance · compartment flag"],
             ["DEGRONOPEDIA", "motif", "–", "–", "–", "–"], ["MetaDegron", "peptide", "–", "–", "–", "–"], ["PAP Colab", "tile", "–", "–", "–", "–"],
             ["Zhang SVM", "peptide", "–", "–", "–", "–"], ["Degformer", "28×20", "–", "–", "–", "–"],
             [[("This service", {"bold": True, "color": CORAL})], [("28×20 + map", {"bold": True})], [("●", {"bold": True, "color": "1F7A6F"})], [("●", {"bold": True, "color": "1F7A6F"})], [("●", {"bold": True, "color": "1F7A6F"})], [("●", {"bold": True, "color": "1F7A6F"})]]]
    d.table(6.1, 3.6, [1.4, 1.05, 0.5, 1.15, 1.35, 1.18], crows, size=10, bold_first_col=True, aligns=["l", "l", "c", "c", "c", "c"], row_fills={6: CORAL_T}, nm="comparison")
    source(d, "○ designed, not built. Comparison as checked on 14–15 Oct 2026 from each tool's paper, page or source; Degformer has no publication. Any ClinVar annotation shown carries ClinVar's attribution and its “not for direct diagnostic use” notice.", y=6.58)


def s24(d):
    s = d.slide("The evaluation harness makes the comparisons a command, and most future queries lie outside training clusters", section=8, title_h=0.9, size=25,
                notes="Harness là phần (b) của trụ phần mềm (D-033): dịch vụ là trụ, harness là chương đánh giá; cũng là nơi thực hiện nghĩa vụ đối chứng Degformer dưới split cụm (D-028.8). Checkpoint Degformer là pickle (nạp thực thi mã tuỳ ý): chạy trong thư mục riêng, python3 -I (chữ 'isolated'). "
                      "⚠ KHÔNG đưa số ≈1.600 biến thể 'chấm được bằng đúng ô đã đo' lên slide này (D-036: chỉ là độ phủ, dễ bị đọc thành phép kiểm). 87,3% là theo cụm cov80 (13.814/15.819); theo protein thì 67,9% tile nằm trên protein chưa thấy: dùng một số trên slide, giữ số kia để trả lời. ClinVar là động lực của miền, không phải phép kiểm. Lời D-034 không lên slide.")
    d.text(MX, 1.45, 6.2, 0.3, [P("Evaluation harness: the method chapter, made re-runnable", size=13, bold=True, color=STEEL)], nm="harness head")
    names = ["composition baseline", "ΔPAP (cnn2w1, cnn2w7)", "Degformer checkpoint (isolated)", "the thesis model"]
    for i, t in enumerate(names):
        d.rect(MX, 1.9 + i * 0.58, 2.6, 0.48, fill=STEEL_T, line=STEEL, shape="round", nm=f"loader {i + 1}", paras=[P(t, size=11, bold=True, color=INK, align="c")], margin=0.05)
    d.rect(3.45, 1.9, 0.5, 2.22, fill=INK, shape="round", nm="split gate", paras=[], margin=0)
    d.text(3.35, 4.17, 0.7, 0.5, [P("same", size=10, bold=True, align="c"), P("split", size=10, bold=True, align="c")], nm="gate label", check=False)
    d.rect(4.25, 2.35, 2.55, 1.3, fill=TEAL_T, line=TEAL, shape="round", nm="report", paras=[P("one report", size=12, bold=True, color="1F7A6F", align="c"), P("Δ, CI, ceiling, MDE printed next to every number", size=10.5, align="c")], margin=0.08)
    d.rect(3.99, 2.9, 0.22, 0.2, fill=GREY, shape="rarrow", nm="to report")
    d.text(MX, 4.75, 6.2, 1.7, [B("One split for all: protein clusters, MMseqs2 ≥30% / 80%; overlapping clusters removed for cross-source tests", size=11.5),
                                B("Fixed seeds, config files and result JSON: every number traceable to a file", size=11.5),
                                P("→ The comparisons on slides 17 and 22 become a command anyone can re-run, not a table to trust.", size=11.5, bold=True, space=6)], nm="harness points")
    # right
    rx = 7.35
    rw = W - MX - rx
    d.text(rx, 1.45, rw, 0.3, [P("Application domain: what the service will be asked about", size=13, bold=True, color=STEEL)], nm="domain head")
    w1, w2 = rw * 0.127, rw * 0.873
    seen = d.rect(rx, 1.9, w1, 0.5, fill=TEAL, shape="rect", nm="seen clusters")
    uns = d.rect(rx + w1, 1.9, w2, 0.5, fill="E4B53A", shape="rect", nm="unseen clusters", paras=[P("unseen clusters  87.3%", size=13, bold=True, color=INK, align="c")], margin=0.04)
    d.text(rx, 2.45, rw, 0.5, [P(runs=[("seen 12.7%", {"bold": True, "color": "1F7A6F"}), ("   of 116,702 degron tiles in the GPS peptidome (PSI ≤ 3.0)", {})], size=11)], nm="bar caption")
    rows = [["", "Count"], ["Degron tiles in the GPS peptidome (PSI ≤ 3.0)", "116,702"], ["…on proteins", "17,287"], ["…in protein clusters unseen in training", "87.3%"],
            ["ClinVar variants of uncertain significance inside those regions", "530,412"]]
    gf, yb = d.table(rx, 3.05, [rw - 1.2, 1.2], rows, size=11, aligns=["l", "r"], nm="domain counts")
    d.rect(rx, yb + 0.2, rw, 1.1, fill=AMBER_T, shape="round", nm="implication",
           paras=[P("Most queries will be outside the training clusters, which is why the out-of-distribution flag and the cluster-split evaluation are part of the product, not optional extras.", size=11.5)], margin=0.15)
    d.anim([seen, uns], [])
    source(d, "Own counts, research/variant-coverage-2026-10-15. ○ harness and service designed, not built. ClinVar motivates the domain; it is not a validation target.", y=6.7)


def s25(d):
    s = d.slide("Plan for the remaining weeks: a hard checkpoint at week 10, then the software", section=9, title_h=0.5, size=26,
                notes="Thứ tự tuần đã dịch lên một bậc so với D-029 (việc tuần 7 cũ đã làm xong ở phiên 8). Điểm kiểm cứng cuối tuần 10 giữ theo D-028 mục 3 và nói ra trước GVHD là điểm mạnh. Bảng tuần là SUY RA từ D-029 + D-031, chưa phải quyết định ghi sổ: nếu Trọng muốn làm căn cứ thì cần một mục quyết định mới sửa D-029. "
                      "Ba 'cổng' G1/G2/G3 là khung nội bộ của repo, KHÔNG phải của học phần nên slide gọi là readiness check. KHÔNG nêu trên slide rằng không có đề tài dự phòng (D-026); nếu GVHD hỏi thì trả lời thẳng. Rủi ro 'cả hai nguồn nhãn mức residue đều của Zhang 2023' vẫn mở: không lên slide, nếu hỏi thì nói thẳng.")
    d.text(MX, 1.12, 8, 0.3, [P("Where the thesis stands (week 6): internal readiness checks, not course gates", size=12.5, bold=True, color=STEEL)], nm="checks head")
    gs = [("G1", "Labels are independent experimental measurements", "● met: all labels measured, none generated by this pipeline", TEAL_T, "1F7A6F"),
          ("G2", "A measurable positive contribution", "● first positive result: +0.0289 over the composition class, +0.0300 over the published control, CIs exclude zero. ○ The matrix gap (−0.0420) is the remaining target", TEAL_T, "1F7A6F"),
          ("G3", "A feasible application", "▲ designed, not built: prediction service with measured uncertainty + evaluation harness (slides 23–24)", AMBER_T, "8A6A12")]
    for i, (g, h, b, t, c) in enumerate(gs):
        card(d, MX + i * 4.07, 1.5, 3.95, 1.55, f"{g}  {h}", b, accent=c, tint=t, hsize=12.5, bsize=11.5)
    weeks = [("Week 7", "architecture variants A / B / C on one grid, aimed at the 0.7693 target", "a measured delta on the matrix, with CI"),
             ("Week 8", "ablations · seed stability · Degformer re-run under the cluster split", "controlled comparison table"),
             ("Week 9", "representation grid (PLM vs one-hot) · error analysis by group", "where the gain comes from, where it fails"),
             ("Week 10", "hard checkpoint: if the matrix target is not met, report a bounded negative and shift weight to benchmark + application", "checkpoint: pivot if no positive delta"),
             ("Weeks 11–13", "software: prediction service (28×20, map, uncertainty, API, flags) and the evaluation harness", "the deliverable for criterion 5"),
             ("Weeks 14–15", "thesis write-up and defence", "")]
    cs = []
    for i, (h, b, o) in enumerate(weeks):
        x = MX + i * 2.04
        hot = (i == 3)
        r = d.rect(x, 3.45, 1.93, 2.6, fill=(CORAL_T if hot else PANEL), line=(CORAL if hot else None), lw=2, shape="round", nm=f"week card {i + 1}")
        t = d.text(x + 0.1, 3.53, 1.73, 2.45, [P(h, size=13, bold=True, color=(CORAL if hot else STEEL)), P(b, size=11, space=3)] + ([P("→ " + o, size=11, bold=True, color=(CORAL if hot else INK), space=4)] if o else []), nm=f"week text {i + 1}")
        cs += [r, t]
    flag = d.rect(MX + 3 * 2.04 + 0.1, 3.23, 0.2, 0.2, fill=CORAL, shape="tri", nm="week 10 flag")
    d.anim(cs[:6], cs[6:], [flag])
    d.text(MX, 6.2, 12.1, 0.45, [P("Reproducibility commitments: fixed seeds; configuration and results written to files; every number in the thesis traceable to a result file; all derived data regenerable by script from checksummed raw data.", size=11)], nm="reproducibility")


def s26(d):
    s = d.slide("Questions for discussion", section=10, title_h=0.5, size=30,
                notes="⚠ CẦN TRỌNG TỰ VIẾT: Q1 (xin duyệt khung ba trụ, C-5) và Q4 (phạm vi phần mềm) phải viết lại theo khung ba trụ (việc 9 của brief). Hai ô amber là chỗ giữ chỗ; thay trước buổi gặp. "
                      "Q1 là C-5: việc phải làm, chưa làm; hỏi xong ghi vào project/meetings/ và cập nhật DECISIONS.md. Q2 xin xác nhận lại lời GVHD 11/10 ('kỳ vọng kiến trúc chưa ai dùng') so với 12/10 (chấp nhận đóng góp dạng công cụ). "
                      "Q3 đổi sau phiên 8: hỏi cách đọc kết quả hai mặt. Nếu còn thời gian: có nên dành ngân sách cho chuyển giao sang protein nguyên vẹn (MaveDB, 9 gene) hay dồn vào nhiệm vụ chính; xin ghi biên bản lời D-034.")
    qs = [("1  Contribution shape", None), ("2  Architecture novelty", "The intended novelty is a weak-supervision question: can abundant bag-level labels (260k peptides, 212k tiles), which do not identify positional parameters, be mined for residue-level output through an MIL/attention bridge, and beat a per-position head trained on the smaller cell-level set? Component mechanisms are established prior art. Is that the right level at which to place the novelty claim?"),
          ("3  Reading the two-sided result", "The model is ahead of the published control on the context axis (+0.0300) and behind it on the substitution matrix (−0.0420), and the ranking reverses between cell-level and position-level metrics. Should the thesis commit to one headline metric, or report the split result as the finding?"), ("4  Application scope", None)]
    pos = [(MX, 1.2), (6.85, 1.2), (MX, 3.75), (6.85, 3.75)]
    for (h, b), (x, y) in zip(qs, pos):
        if b is None:
            d.rect(x, y, 5.88, 2.35, fill=AMBER_T, line="B08A1E", dash=True, shape="round", nm=f"question {h[0]} (to be written)")
            d.text(x + 0.2, y + 0.12, 5.5, 2.1, [P(h, size=15, bold=True, color="8A6A12"),
                                                P("Wording to be finalised by Nguyễn Thế Trọng after the three-pillar framework (C-5) is settled; see the one-page framework handout.", size=12, italic=True, space=4)], nm=f"question {h[0]} text")
        else:
            card(d, x, y, 5.88, 2.35, h, b, accent=STEEL, tint=PANEL, hsize=15, bsize=13.5)
    d.rect(MX, 6.7 - 0.05, 0.01, 0.01, fill=None, nm="spacer")
    d.text(MX, 6.35, 12.1, 0.4, [P(runs=[("Thank you. ", {"bold": True}), ("Data, scripts, result files and the decision log are in the project repository.", {})], size=13)], nm="thanks")


def a1(d):
    s = d.slide("Appendix A1 · References", section=0, title_h=0.5, size=26,
                notes="Danh sách tác giả đã đối chiếu qua PubMed ngày 15/10/2026 (bioRxiv API cho Larsen). Larsen 2025 là PREPRINT; Degformer không có bài báo. Tokheim/Liu giữ ở đây để trả lời nếu GVHD hỏi về ung thư (không lên slide 6 nữa).")
    refs = [
        "Koren I, Timms RT, Kula T, Xu Q, Li MZ, Elledge SJ. The eukaryotic proteome is shaped by E3 ubiquitin ligases targeting C-terminal degrons. Cell 173(7):1622–1635.e14, 2018. doi:10.1016/j.cell.2018.04.028",
        "Hou C, Li Y, Wang M, Wu H, Li T. Systematic prediction of degrons and E3 ubiquitin ligase binding via deep learning. BMC Biol 20(1):162, 2022. doi:10.1186/s12915-022-01364-6",
        "Zhang Z, Sie B, Chang A, Leng Y, Nardone C, Timms RT, Elledge SJ. Elucidation of E3 ubiquitin ligase specificity through proteome-wide internal degron mapping. Mol Cell 83(18):3377–3392.e6, 2023. doi:10.1016/j.molcel.2023.08.022",
        "Xu H, Hu R, Zhao Z. DegronMD. Mol Biol Evol 40(12), 2023. doi:10.1093/molbev/msad253",
        "Szulc NA, et al. DEGRONOPEDIA: a web server for proteome-wide inspection of degrons. Nucleic Acids Res 52(W1):W221–W232, 2024. doi:10.1093/nar/gkae238",
        "Zheng M, Lin S, Chen K, Hu R, Wang L, Zhao Z, Xu H. MetaDegron: multimodal feature-integrated protein language model for predicting E3 ligase targeted degrons. Brief Bioinform 25(6), 2024. doi:10.1093/bib/bbae519",
        "Voutsinos V, et al. A near-complete map of human cytosolic degrons and their relevance for disease. Sci Adv 12(6):eadz3483, 2026. doi:10.1126/sciadv.adz3483",
        "Larsen FB, Voutsinos V, et al. Comprehensive degron mapping in human transcription factors. bioRxiv 2025.05.16.654404 (preprint, not peer reviewed). doi:10.1101/2025.05.16.654404",
        "Degformer, GitHub Alpine2048/Degformer, Apache-2.0, created 24 Mar 2026. No publication.",
        "Schulze TK, Lindorff-Larsen K. Effects of residue substitutions on the cellular abundance of proteins. eLife 13, 2026. doi:10.7554/eLife.103721",
        "LeBlanc CJ, Agarwal P, Demaray JE, Hu G, Zintel MA, Lam AWY, Castro Hernandez JE, Staller MV. Interpretable biophysical neural networks of transcriptional activation domains. Cell Syst 17(9):101701, 2026. doi:10.1016/j.cels.2026.101701",
        "Landrum MJ, et al. ClinVar: improvements to accessing data. Nucleic Acids Res 2018. PMID 29165669",
        "Tokheim C, Wang X, Timms RT, …, Liu XS. Systematic characterization of mutations altering protein degradation in human cancers. Mol Cell 81(6):1292–1308.e11, 2021. doi:10.1016/j.molcel.2021.01.020",
        "Liu J, Tokheim C, Lee JD, …, Pandolfi PP, Wei W. Nat Commun 12:6704, 2021. doi:10.1038/s41467-021-26871-y",
    ]
    half = 7
    for c in range(2):
        paras = [P(f"{c * half + i + 1}.  {r}", size=11.5, space=7) for i, r in enumerate(refs[c * half:(c + 1) * half])]
        d.text(MX + c * 6.15, 1.2, 5.95, 5.4, paras, nm=f"references column {c + 1}")


def a2(d):
    s = d.slide("Appendix A2 · Record format and identifier decoding", section=0, title_h=0.5, size=26,
                notes="Quy tắc tile đã kiểm trên 128/130 peptide có trình tự biết trước; 2 peptide lệch bị loại. Hàng mẫu lấy thật từ data/processed/psi-rep1.tsv và psi-sat_a.tsv (dữ liệu không lên git).")
    rows = [["Field", "Type", "Meaning"],
            ["id", "string", "<ACCESSION>_<GENE>_<tile>_mut<pos><aa>, e.g. A2RUQ5_C17orf102_2_mut10a"],
            ["psi", "float, 1…6", "Protein Stability Index: low = degraded = strong degron"],
            ["sum", "float", "normalised read depth, used for filtering (scanning: sum ≥ 10)"],
            ["nb1…nb6", "float", "normalised reads in stability bins 1…6"]]
    gf, yb = d.table(MX, 1.2, [1.4, 1.5, 9.23], rows, size=12, bold_first_col=True, mono_cols=(0,), nm="fields")
    card(d, MX, yb + 0.25, 5.9, 1.9, "Identifier decoding", "accession → wild-type sequence. Tile n starts at residue (n−1)×23 + 1 and has length 28. mut10a = position 10 substituted to alanine. The tile rule is verified on 128 of 130 peptides with a known sequence; the 2 mismatches are excluded.",
         accent=STEEL, tint=STEEL_T, hsize=13, bsize=12)
    card(d, MX + 6.2, yb + 0.25, 5.93, 1.9, "Real rows (psi-rep1.tsv, psi-sat_a.tsv)",
         [P("A0A0B4J1Y8_IGLV9-49_1_mut24   1.884  364.9", size=11, mono=True, space=3), P("A0A0B4J1Y8_IGLV9-49_1_mut26   2.168  199.1", size=11, mono=True, space=2),
          P("A2RUQ5_C17orf102_2_mut10a     4.916  484.4", size=11, mono=True, space=2), P("columns: id, psi, sum (nb1…nb6 omitted)", size=10.5, color=MUTED, space=4)], accent=INK, tint=PANEL, hsize=13)
    d.text(MX, yb + 2.45, 12.1, 0.9, [B("Saturation set has no separate wild-type measurement: synonymous-codon cells (28 per peptide) serve as the internal wild type; median within-peptide PSI SD 0.0576", size=12),
                                      B("A trailing “*” (813 peptides of 27 aa) is masked, never fed to the model as a 21st token", size=12)], nm="notes")
