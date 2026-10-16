from comp import *
from part1 import A, FIG
import os, json, math
from PIL import Image


def s10(d):
    s = d.slide("Group 2: measured maps and sequence models are the closest prior work", section=3, title_h=0.5, size=26,
                notes="Slide quan trọng nhất của phần 3 và dễ sai nhất. (1) PHẢI nói Degformer đã xuất ma trận 28×20; câu 'chưa sản phẩm nào xuất 28×20' đã bị bác bỏ. Cách nói đúng: nhiệm vụ không còn trống, nhưng ĐIỀU KIỆN ĐÁNH GIÁ còn trống. "
                      "(2) 0,9162–0,9463 là self-reported, ghi 'self-reported correlations', không ghi ρ. (3) Phép đo bất biến hoán vị của PAP là TỰ ĐO (Pearson 1.000000): nhãn nguồn phải rõ. "
                      "(4) Larsen 2025 là preprint; đừng nói nó là test trình tự chưa thấy (97,4% TF đã có trong peptidome GPS). Hình Fig. 4: Voutsinos et al. Sci Adv 2026, DOI 10.1126/sciadv.adz3483, CC BY-NC 4.0.")
    d.text(MX, 1.15, 4.6, 3.4, [P("What they achieved: this is where the field's labels come from", size=12.5, bold=True, color=STEEL),
                                B("Koren 2018: GPS peptidome screening; the “C-end rule” E3 adaptors", size=11.5),
                                B("Zhang 2023: added scanning and saturation mutagenesis; fingerprints for 219 degrons; own SVM predicts peptidome PSI at Pearson 0.8955 (260,989 peptides)", size=11.5),
                                B("Voutsinos 2026: >200,000 30-residue tiles from >5,000 proteins; 19% strong, 30% intermediate, 51% non-degrons; PAP CNN reaches Pearson 0.82 / 0.87 held-out", size=11.5),
                                B("Larsen 2025 (preprint): all 1,626 human transcription factors, with PAP / rASA / pLDDT annotation", size=11.5),
                                B("Degformer 2026: the most direct precedent, a transformer on Zhang's tables that does output a 28×20 ΔPSI matrix; self-reported correlations 0.9162–0.9463", size=11.5)], nm="achieved")
    d.pic(os.path.join(FIG, "voutsinos2026-f4.jpg"), 5.4, 1.2, w=3.75, h=3.75 * 338 / 800, alt="Voutsinos et al. 2026 Fig. 4: PAP two-channel architecture and held-out scatter plots")
    d.text(5.4, 2.9, 3.75, 1.2, [P("Voutsinos et al., Sci Adv 2026, Fig. 4: PAP architecture and held-out scatter plots. DOI 10.1126/sciadv.adz3483. CC BY-NC 4.0.", size=10, color=MUTED)], nm="figure caption")
    # permutation test
    d.rect(9.35, 1.15, 3.38, 3.4, fill="FFFFFF", line=LINE, shape="round", nm="permutation panel")
    d.text(9.5, 1.2, 3.1, 0.3, [P("The permutation test on PAP", size=12.5, bold=True)], nm="permutation title")
    cols = [STEEL, TEAL, "D9A21B", CORAL, GREY, "7A5BA6", "5B7380"]
    order = [0, 1, 2, 3, 4, 5, 6, 2, 0, 5, 3, 1]
    shuf = [order[i] for i in (7, 3, 10, 0, 5, 11, 2, 8, 6, 1, 9, 4)]
    o1 = strip(d, 9.5, 1.65, 12, 0.22, gap=0.03, fills=[cols[c] for c in order], nm="original residue")
    d.text(9.5, 1.92, 3.1, 0.25, [P("original peptide", size=10, color=MUTED)], nm="orig label")
    ar = d.rect(10.85, 2.2, 0.3, 0.3, fill=GREY, shape="darrow", nm="shuffle arrow")
    al = d.text(11.2, 2.2, 1.4, 0.3, [P("shuffle order", size=11, bold=True, color=CORAL)], nm="shuffle label")
    o2 = strip(d, 9.5, 2.6, 12, 0.22, gap=0.03, fills=[cols[c] for c in shuf], nm="shuffled residue")
    d.text(9.5, 2.87, 3.1, 0.25, [P("shuffled peptide", size=10, color=MUTED)], nm="shuf label")
    b1 = d.rect(9.5, 3.3, 1.15, 0.45, fill=STEEL_T, shape="round", nm="score original", paras=[P("score", size=12, bold=True, color=STEEL, align="c")], margin=0.02)
    eq = d.text(10.65, 3.28, 0.55, 0.5, [P("=", size=28, bold=True, color=CORAL, align="c")], nm="equals", check=False)
    b2 = d.rect(11.2, 3.3, 1.15, 0.45, fill=STEEL_T, shape="round", nm="score shuffled", paras=[P("score", size=12, bold=True, color=STEEL, align="c")], margin=0.02)
    pr = d.text(9.5, 3.85, 3.1, 0.6, [P("Pearson(original, shuffled) = 1.000000", size=11.5, bold=True, color=CORAL), P("own measurement", size=10, color=MUTED)], nm="pearson")
    d.anim([ar, al] + o2, [b1, eq, b2, pr])
    rows = [["Work", "Limitation relevant to the residue-level question"],
            ["Zhang SVM, PAP, Larsen", "Prediction unit is the whole peptide or tile: one score per segment, so no ranking of residues within it"],
            ["PAP specifically", "Internal channel is Conv1D(kernel=1) + global average pooling → permutation-invariant: shuffling residue order leaves its score unchanged (own measurement)"],
            ["Degformer", "Random train/test split with 4.09% identical-sequence leakage; duplicate sequences with conflicting labels; the head reads the CLS token only, so the matrix is assembled from 532 forward passes; blind test set absent from the repo, so headline numbers are not reproducible"]]
    d.table(MX, 4.75, [2.2, 9.93], rows, size=11, bold_first_col=True, nm="limitations")
    source(d, "PAP architecture and permutation test: own re-implementation of the authors' MIT-licensed code. Degformer: own reading of its full source and own leakage measurement on its shipped CSV.", y=6.58)


def s11(d):
    s = d.slide("Group 3: adjacent models ask other questions but set the bar for evidence", section=3, title_h=0.5, size=25,
                notes="Nhóm này là nguồn của hai quy ước đánh giá đề tài sẽ dùng; khi dùng ba cách làm của LeBlanc phải ghi 'theo LeBlanc et al. 2026', không trình bày như lựa chọn riêng. "
                      "Trích dẫn đầy đủ ở phụ lục A1. rASA đơn lẻ cho Spearman 0,45 (Schulze & Lindorff-Larsen); mô hình tốt nhất 0,555 so với trần 0,568 (LeBlanc).")
    rows = [["Work", "What it predicts", "Relation to this thesis"],
            ["AlphaMissense (2023, Science)", "whether a missense variant is pathogenic", "Different question: pathogenicity, no mechanism. This thesis adds a mechanism; it does not replace it"],
            ["Schulze & Lindorff-Larsen (2026, eLife)", "effect of substitutions on cellular abundance (6 VAMP-seq experiments, 31,614 variants)", "Substitution matrices conditioned only on buried vs exposed already predict abundance well and are proposed as a strong baseline; rASA alone gives Spearman 0.45"],
            ["LeBlanc et al. (2026, Cell Systems)", "activation-domain strength on a tile library; separates abundance from coactivator binding", "Not a degron paper, but sets the methodological bar: weight stability across seeds and bootstraps, comparison with the replicate ceiling (best model 0.555 vs ceiling 0.568), split by protein cluster"]]
    gf, yb = d.table(MX, 1.2, [3.0, 3.6, 5.53], rows, size=11.5, bold_first_col=True, nm="adjacent models")
    y = yb + 0.3
    qs = [("AlphaMissense", "Is it pathogenic?", STEEL_T, STEEL), ("Schulze & Lindorff-Larsen", "How abundant is it?", STEEL_T, STEEL),
          ("LeBlanc et al.", "How strong an activation domain?", STEEL_T, STEEL), ("This thesis", "Which residue controls degradation?", CORAL_T, CORAL)]
    cs = []
    for i, (a, b, t, c) in enumerate(qs):
        cs.append(d.rect(MX + i * 3.06, y, 2.92, 1.0, fill=t, shape="round", nm=f"question {i + 1}", paras=[P(a, size=11, bold=True, color=c), P(b, size=14, bold=True, color=INK)], margin=0.12))
    d.text(MX, y + 1.05, 12.1, 0.3, [P("what is predicted", size=10, color=MUTED)], nm="axis label")
    box = d.rect(MX, y + 1.5, 12.13, 0.7, fill=PANEL, line=GREY, shape="round", nm="conventions",
                 paras=[P(runs=[("Evaluation conventions we adopt (following LeBlanc et al. 2026): ", {"bold": True}), ("simple structural baseline · replicate ceiling next to every number · protein-cluster split · seed stability", {})], size=13)], margin=0.15)
    d.anim(cs[:3], [cs[3]], [box])
    source(d, "Schulze & Lindorff-Larsen, eLife 13, DOI 10.7554/eLife.103721 · LeBlanc et al., Cell Systems 17(9):101701, DOI 10.1016/j.cels.2026.101701 (both read in full).", y=6.6)


def s12(d):
    s = d.slide("The gap is provable: a composition-only model cannot rank residues inside a degron", section=4, title_h=0.5, size=25,
                notes="Tài sản mạnh nhất của đề tài, nên mở đầu phần lập luận. Nói rõ 'provable' và nói rõ đây là TỰ ĐO. 89,7% là trên 2.624 peptide có footprint (68,9% là trên bộ quét, giữ để trả lời nếu hỏi). "
                      "Khi nói '+0,0289' PHẢI nói kèm 80% của nó là thành phần của lân cận ±3, không phải thứ tự hay vị trí tuyệt đối (C-17). Câu chuyển: 'PAP is not a bad model; it was trained for a segment-level score. Using it for residue-level effects is using it outside its design.' "
                      "Animation: hai peptide cùng thành phần, khác thứ tự → nhãn đổi vị trí → điểm số của mô hình không nhích.")
    d.text(MX, 1.12, 6.6, 0.75, [P("PAP is not a bad model: it was trained for a segment-level score. Using it for residue-level effects is using it outside its design.", size=13, italic=True, color=STEEL)], nm="lead")
    d.text(MX, 1.92, 6.6, 1.9, [P("The argument", size=13, bold=True),
                                B("PAP's internal channel is Conv1D(kernel=1) → GlobalAveragePooling, so its score is a function of amino acid composition only", size=12),
                                B("The effect of substituting a→b is Δf = f(c − e_a + e_b) − f(c): no position index appears", size=12),
                                B("So every substitution with the same amino acid pair gets an identical effect, wherever it sits", size=12)], nm="argument")
    d.table(MX, 3.85, [4.1, 2.5], [["Own measurement, scanning set", "Peptides"],
                                  ["with a measured footprint", "2,624"],
                                  ["…and a same-pair group holding both a positive and a non-positive position", [("2,353 (89.7%)", {"bold": True, "color": CORAL})]]], size=11.5, aligns=["l", "r"], nm="measurement table")
    d.text(MX, 5.2, 6.6, 0.55, [P("Verified by 200 exhaustive comparisons, 4,000 rank-bound checks, an explicit rank-2 counterexample, and the permutation test on PAP (Pearson 1.000000).", size=11)], nm="verification")
    card(d, MX, 5.8, 6.6, 0.88, "The gap now has a price", "Local-neighbourhood features on top of a composition-only model are worth +0.0289 cell-level AUROC (CI [0.0264, 0.0313]; 1,599 clusters); 80% of it is composition in a ±3 neighbourhood.",
         accent=TEAL, tint=TEAL_T, hsize=12, bsize=11)
    # diagram
    d.rect(7.55, 1.12, 5.18, 5.56, fill="FFFFFF", line=LINE, shape="round", nm="diagram panel")
    d.text(7.7, 1.2, 4.9, 0.3, [P("Same residues, different order", size=13, bold=True)], nm="diagram title")
    seqA, seqB = "SAGDVDTLAFDG", "SAADVDTLGFDG"
    cA = strip(d, 7.75, 1.95, 12, 0.36, gap=0.04, fills=["E3E9EC"] * 12, labels=list(seqA), size=11, nm="peptide A")
    hA = d.rect(7.75 + 2 * 0.40, 1.95, 0.36, 0.36, fill=CORAL, shape="rect", nm="A footprint residue", paras=[P("G", size=11, bold=True, mono=True, color=BG, align="c")], margin=0)
    d.text(7.75, 1.55, 4.8, 0.3, [P("peptide A: measured footprint at position 3", size=11, color=CORAL, bold=True)], nm="A label")
    cB = strip(d, 7.75, 3.0, 12, 0.36, gap=0.04, fills=["E3E9EC"] * 12, labels=list(seqB), size=11, nm="peptide B")
    hB = d.rect(7.75 + 8 * 0.40, 3.0, 0.36, 0.36, fill=CORAL, shape="rect", nm="B footprint residue", paras=[P("G", size=11, bold=True, mono=True, color=BG, align="c")], margin=0)
    lB = d.text(7.75, 2.6, 4.8, 0.3, [P("peptide B: same residues, footprint at position 9", size=11, color=CORAL, bold=True)], nm="B label")
    # meters
    m = []
    for k, (yy, lab) in enumerate([(4.0, "composition-only model, peptide A"), (4.6, "composition-only model, peptide B")]):
        m.append(d.text(7.75, yy - 0.28, 4.8, 0.26, [P(lab, size=10.5, color=MUTED)], nm=f"meter label {k}"))
        m.append(d.rect(7.75, yy, 4.8, 0.2, fill="E3E9EC", shape="round", nm=f"meter track {k}"))
        m.append(d.rect(7.75, yy, 3.0, 0.2, fill=STEEL, shape="round", nm=f"meter value {k}"))
    eq = d.rect(8.0, 5.1, 4.3, 0.42, fill=CORAL_T, shape="round", nm="identical score", paras=[P("identical score: the dial does not move", size=12.5, bold=True, color=CORAL, align="c")], margin=0.05)
    big = d.rect(7.75, 5.65, 4.8, 0.85, fill=INK, shape="round", nm="89.7 statistic",
                 paras=[P(runs=[("89.7%", {"size": 22, "bold": True, "color": AMBER}), ("  of 2,624 peptides are in this situation", {"size": 12})], color=BG, align="c")], margin=0.1)
    d.anim([lB, hB] + cB, m + [eq], [big])
    source(d, "Own measurement; scripts and JSON results in the thesis repository. Illustration (peptides A and B) is schematic.", y=6.72)


def s13(d):
    s = d.slide("Why now: measured residue-level labels exist only since 2023", section=4, title_h=0.5, size=26,
                notes="Câu search statement ở chân slide là BẮT BUỘC, viết đúng dạng 'queries run on 15 Oct 2026 returned no…', tuyệt đối KHÔNG viết 'nobody has done this'. "
                      "Nhóm diễn giải biến thể: viết đúng 'mechanistic hypothesis', KHÔNG viết 'explains why a variant is pathogenic' (D-036). Nhà thực nghiệm: 'prioritisation tool', không phải công cụ quyết định (Jaccard 0,50). Không thêm lại nhóm PROTAC. "
                      "Nếu hỏi 'đã có Degformer rồi thì sao': nhiệm vụ đã có người làm, nhưng chưa ai làm dưới điều kiện đánh giá đứng được (split theo cụm, trần nhãn, bất định); đo được 4,09% rò rỉ trình tự y hệt.")
    ax_y = 2.15
    X = lambda yr: 0.9 + (yr - 2018) * 1.15
    d.line(X(2018), ax_y, X(2026), ax_y, color=GREY, lw=2, nm="timeline axis")
    for yr in range(2018, 2027):
        d.line(X(yr), ax_y - 0.05, X(yr), ax_y + 0.05, color=GREY, lw=1.5, nm=f"tick {yr}")
        d.text(X(yr) - 0.3, ax_y + 0.07, 0.6, 0.22, [P(str(yr), size=10, color=MUTED, align="c")], nm=f"year {yr}")
    data = [(2018, "Koren 2018", "GPS screening"), (2023, "Zhang 2023", "first large set of measured mutation effects"),
            (2025, "Larsen 2025", "TF map (preprint)"), (2026, "Voutsinos 2026", "reference map + baseline model")]
    tools = [(2024, "DEGRONOPEDIA · MetaDegron", "tools, 2024"), (2026, "Degformer", "GitHub, 2026")]
    ms = []
    for yr, a, b in data:
        wlab = {2018: 1.4, 2023: 1.9, 2025: 1.1, 2026: 1.3}[yr]
        xx = X(yr) - wlab / 2 + (0.2 if yr == 2026 else 0) - (0.1 if yr == 2025 else 0)
        ms.append(d.rect(X(yr) - 0.07, ax_y - 0.07, 0.14, 0.14, fill=STEEL, shape="oval", nm=f"data milestone {yr}"))
        ms.append(d.text(xx, 1.2, wlab, 0.8, [P(a, size=11, bold=True, color=STEEL, align="c"), P(b, size=10, color=INK, align="c")], anchor="b", nm=f"data label {yr}"))
    for yr, a, b in tools:
        ms.append(d.rect(X(yr) - 0.07, ax_y - 0.07, 0.14, 0.14, fill=TEAL, shape="oval", nm=f"tool milestone {yr}"))
        ms.append(d.text(X(yr) - 0.9, ax_y + 0.32, 1.8, 0.5, [P(a, size=10.5, bold=True, color="1F7A6F", align="c"), P(b, size=10, align="c")], nm=f"tool label {yr}"))
    gap = d.rect(11.2, 1.25, 1.53, 1.85, fill=AMBER_T, line="B08A1E", dash=True, shape="round", nm="open gap",
                 paras=[P("residue-level model + evaluation conditions", size=11.5, bold=True, color="6B5210", align="c")], margin=0.08)
    rows = [["Missing piece", "Current state"],
            ["A model trained on the residue-level objective", "Published degron models are trained on segment scores; per-residue use is outside their design"],
            ["Evaluation conditions for residue-level claims", "Closest precedent (Degformer): random split with measurable leakage, no label ceiling, no per-prediction uncertainty"],
            ["A measured noise ceiling beside reported numbers", "Own measurement: cell-level ceilings 0.9458 (scanning) and 0.9519 (saturation); replicate residue-set agreement Jaccard 0.4965"],
            ["At which scale the information sits", "Own decomposition: peptide composition → ±3 neighbourhood → order → absolute position. A literature search on 15 Oct 2026 did not find this breakdown published for degrons"]]
    tb, yb = d.table(MX, 3.3, [2.75, 4.85], rows, size=11, bold_first_col=True, nm="missing pieces")
    users = [("Variant interpretation", "530,412 VUS sit in measured degron regions (slide 6): a mechanistic hypothesis to complement pathogenicity scores, i.e. does a substitution stabilise or destabilise the peptide, and by how much", STEEL),
             ("Experimental biologists", "A prioritisation tool: “test these 3 residues first”, with calibrated uncertainty", TEAL),
             ("Bioinformatics / ML researchers", "A reference task with a measured ceiling, honest baselines and a homology-controlled split", "7A5BA6")]
    uc = []
    yy = 3.3
    for i, (h, b, c) in enumerate(users):
        hh = [1.5, 0.9, 0.9][i]
        uc.append(card(d, 8.45, yy, 4.28, hh, h, b, accent=c, hsize=12, bsize=11))
        yy += hh + 0.1
    d.anim(ms[:2], ms[2:8] + [gap])
    source(d, "Search statement: PubMed and Europe PMC queries run on 15 Oct 2026 returned no degron-prediction tool published in 2025–2026 beyond those listed; of 19 papers citing Larsen 2025 and Voutsinos 2026, none is a residue-level footprint model.", y=5.95, w=7.6)


def s14(d):
    s = d.slide("Contribution: three pillars; method measured, two cells still open", section=4, title_h=0.5, size=26,
                notes="Chỗ mạnh nhất là bảng phân rã: nó TỰ HẠ cách nói 'vị trí thắng thành phần'. Câu đúng: 'composition at which scale?'. Câu chân slide bắt buộc: thắng ΔPAP là thắng một mô hình dùng ngoài thiết kế; M0 chỉ-thành-phần HOÀ ΔPAP cnn2w7 (+0,0008, CI [−0,0057; 0,0074]). "
                      "Trụ 1 ghi 'region level' theo D-036. Lời GVHD xác nhận trụ phần mềm (D-034) KHÔNG lên slide, nói miệng và xin ghi biên bản ở slide 26. Mốc đã khoá: 0,7693 / trần 0,9519 / ngưỡng 0,0123.")
    pill = [("1  Urgency", "why the question is worth asking", "● measured, region level: OR 2.148 within-protein (slide 6)", TEAL),
            ("2  Method", "residue-level prediction, proof of the gap, evaluation protocol, new architecture", "● C1–C3 measured  ·  ○ C4 open", STEEL),
            ("3  Software", "prediction service with measured uncertainty, reproducible evaluation harness", "○ C5 designed, not built (slides 23–24)", "B08A1E")]
    for i, (h, b, e, c) in enumerate(pill):
        card(d, MX + i * 4.07, 1.15, 3.95, 1.1, h, [P(b, size=10.5, space=1), P(e, size=10.5, bold=True, color=c, space=2)], accent=c, hsize=13, bsize=10.5)
    rows = [["#", "Contribution", "Status"],
            ["C1", "Proof that the current model class cannot localise degron residues: 89.7% of footprint peptides, explicit rank-2 counterexample, permutation test on PAP (Pearson 1.000000)", "● measured"],
            ["C2", "Evaluation protocol for the residue-level task: two label sets with distinct roles, measured ceilings (0.9458 / 0.9519), composition baseline, published-model control, cluster split, pre-computed detection threshold (MDE 0.0123)", "● measured"],
            ["C3", "Decomposition of where the predictive information sits, and a model that beats the closest published control on the context axis: +0.0300 over ΔPAP cnn2w7 (CI [0.0234, 0.0366])", "● first positive result"],
            ["C4", "Architecture closing the gap on the substitution matrix: currently −0.0420 behind ΔPAP cnn2w1 (target: beat 0.7693, ceiling 0.9519)", "○ open: the work ahead"],
            ["C5", "Software: residue-level prediction service with uncertainty anchored to the measured ceiling, plus a harness that re-runs prior models under the same cluster split", "○ designed, built in weeks 11–13"]]
    fills = {(1, 2): TEAL_T, (2, 2): TEAL_T, (3, 2): TEAL_T, (4, 2): AMBER_T, (5, 2): AMBER_T}
    gf, yb = d.table(MX, 2.4, [0.55, 9.6, 1.98], rows, size=10.5, fills=fills, bold_first_col=True, nm="contributions")
    # decomposition bar
    by = yb + 0.38
    d.text(MX, by - 0.32, 8.6, 0.28, [P("Where the information sits: contribution to the +0.0289 gain", size=11.5, bold=True)], nm="bar title")
    tot = 0.0232 + 0.0057 + 0.0002
    segs = [(0.0232, STEEL, "±3 neighbourhood composition  +0.0232 (80%)"), (0.0057, "7A97BC", "order  +0.0057"), (0.0002, CORAL, "")]
    x = MX
    parts = []
    for v, c, lab in segs:
        w = 8.6 * v / tot
        parts.append(d.rect(x, by, max(w, 0.04), 0.4, fill=c, shape="rect", nm=f"segment {lab[:12] or 'absolute position'}"))
        x += w
    d.text(MX, by + 0.45, 6.9, 0.25, [P("±3 neighbourhood composition  +0.0232 (80%)", size=10.5, bold=True, color=STEEL)], nm="seg label 1")
    d.text(MX + 7.0, by + 0.45, 1.7, 0.25, [P("order +0.0057", size=10.5, color="4A6A92")], nm="seg label 2")
    d.text(MX + 6.5, by + 0.7, 2.3, 0.25, [P("absolute position +0.0002 (nil)", size=10.5, bold=True, color=CORAL, align="r")], nm="seg label 3")
    q = d.rect(9.45, by - 0.05, 3.28, 1.0, fill=CORAL_T, shape="round", nm="right question",
               paras=[P(runs=[("Not ", {}), ("“composition or position?”", {"bold": True}), (" but ", {}), ("“composition at which scale?”", {"bold": True, "color": CORAL})], size=12.5)], margin=0.12)
    d.anim(parts, [q])
    source(d, "● own measurement with result files · ○ open. Beating ΔPAP is beating a model used outside its design: no model has been trained for this task, which is the gap claimed here.", y=6.62)
