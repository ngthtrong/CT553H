from comp import *
from part1 import A
import os


def s19(d):
    s = d.slide("Labels are rebuilt from raw counts, and the rebuild passes a validation gate", section=6, title_h=0.5, size=26,
                notes="Trả lời 'em đã làm gì với dữ liệu' bằng một con số kiểm được. Cổng kiểm: PSI dựng lại từ read thô khớp bảng của tác giả, sai lệch tối đa 5,0×10⁻⁷ trên 261.865 giá trị (research/full-data-audit/psi-build.json). "
                      "Tác giả chỉ công bố bảng PSI cho Replicate 1; dựng lại cho ra cả năm điều kiện, kể cả replicate 2, nên mới tính được trần đo lường. Ba construct sai trong bảng tác giả do lỗi tiêu đề: nêu ngắn gọn. Animation: phễu hẹp dần, người nghe thấy 91 đến từ đâu.")
    tiers = [("raw counts: 6 bins × 5 conditions", 3.8, GREY, "● gate: rebuilt PSI vs the authors' table, max deviation 5.0 × 10⁻⁷"),
             ("PSI rebuilt for 5 conditions", 3.8, STEEL, "261,868 / 261,999 / 264,036 / 134,608 / 134,563 ids"),
             ("8,831 scanning peptides", 3.2, STEEL, "all scanning constructs"),
             ("3,439 degrons", 2.7, STEEL, "PSI_WT ≤ 3.0"),
             ("2,624 with a footprint", 2.3, TEAL, "measured footprint present"),
             ("235 saturation matrices", 1.95, "7A5BA6", "full 28×20 designs"),
             ("91 degron matrices", 1.65, CORAL, "PSI_WT ≤ 3.0")]
    sh = []
    cx = 2.55
    for i, (t, w, c, crit) in enumerate(tiers):
        y = 1.2 + i * 0.7
        r = d.rect(cx - w / 2, y, w, 0.56, fill=c, shape="rect", nm=f"funnel tier {i + 1}", paras=[P(t, size=11, bold=True, color=BG, align="c")], margin=0.04)
        cr = d.text(4.65, y + 0.02, 2.45, 0.54, [P(crit, size=10, color=("1F7A6F" if i == 0 else MUTED), bold=(i == 0))], anchor="m", nm=f"criterion {i + 1}")
        sh += [r, cr]
    d.anim(sh[:4], sh[4:8], sh[8:])
    d.text(MX, 6.15, 6.5, 0.5, [P(runs=[("raw/", {"mono": True, "bold": True}), (" (never edited, checksummed) → ", {}), ("interim/", {"mono": True, "bold": True}), (" → ", {}), ("processed/", {"mono": True, "bold": True}), (": every derived file regenerable by a script", {})], size=11)], nm="three tiers")
    rows = [["Step", "What was done"],
            ["1", "Read per-bin raw counts: one file per bin per condition, 6 bins"],
            ["2", "Normalise: nb_i = b_i × factor_i, factors per condition with bin 1 as reference"],
            ["3", "Compute PSI = Σ i·nb_i / Σ nb_i for every construct"],
            ["4", "Validation gate: compare the rebuilt Replicate-1 PSI with the authors' table"]]
    gf, yb = d.table(7.4, 1.2, [0.6, 4.73], rows, size=11, bold_first_col=True, nm="rebuild steps")
    c1 = card(d, 7.4, yb + 0.15, 5.33, 1.2, "Gate result", "Maximum deviation 5.0 × 10⁻⁷ across 261,865 values: the reconstruction is correct, so the same code can build conditions the authors published no PSI table for.",
              accent="1F7A6F", tint=TEAL_T, hsize=12, bsize=11)
    c2 = card(d, 7.4, yb + 1.45, 5.33, 1.1, "Why it matters", "Only Replicate 1 was released. Rebuilding gives all five conditions, including the second replicate, which makes a measured noise ceiling computable at all.",
              accent=STEEL, tint=STEEL_T, hsize=12, bsize=11)
    c3 = card(d, 7.4, yb + 2.65, 5.33, 1.0, "Also found and corrected", "Three constructs mis-scored in the authors' table due to a header error: two with Sum = 0 / PSI = NA despite reads, one with PSI off by 0.62.",
              accent="8A6A12", tint=AMBER_T, hsize=12, bsize=11)
    source(d, "Own measurement. Rebuild command, per-condition normalisation factors and the validation JSON are in the repository.", y=6.7)


def s20(d):
    s = d.slide("Two label sets, two roles: scanning for scale, saturation for the full matrix", section=6, title_h=0.5, size=25,
                notes="⚠ Bảng này đã sửa sau phiên 8: bộ quét CŨNG là nhãn hiệu ứng đột biến và lớn hơn (1.985 cụm so với 89). BỎ câu 'n = 91 là cỡ mẫu của phần mức residue'; n = 91 chỉ là cỡ mẫu phần ma trận 19 thay thế. Nhãn mức tile (Voutsinos, Larsen) thì vẫn không đỡ được tuyên bố mức residue. "
                      "Bộ bão hòa không có phép đo hoang dã riêng: ô đồng nghĩa là WT nội tại (28 ô mỗi peptide). '*' cuối trình tự (813 peptide 27 aa) phải được mask. Trường dữ liệu đầy đủ ở phụ lục A2. 'Dương giả >45%' là cảnh báo chung từ y văn, không phải số đo trên dữ liệu này.")
    rows = [["", "Scanning set", "Saturation set"],
            ["Design", "one substitution per position, almost all →R (20 distinct WT→mut pairs)", "all 20 amino acids at each of 28 positions: a full matrix"],
            ["Raw size", "≈ 262,000 constructs × 2 replicates, 9,590 peptides", "134,608 / 134,563 constructs, 249 peptides"],
            ["Degron peptides (PSI_WT ≤ 3.0)", [("2,994", {"bold": True})], [("91", {"bold": True})]],
            ["Protein clusters", [("1,985", {"bold": True})], [("89", {"bold": True})]],
            ["Scored cells", [("83,446", {"bold": True})], [("47,847", {"bold": True})]],
            ["Measurement ceiling (cell-level AUROC)", [("0.9458", {"bold": True})], [("0.9519", {"bold": True})]],
            ["Replicate agreement", "residue-set Jaccard 0.4965", "PSI 0.9544, ΔPSI 0.8335; noise 16.7% of variance"],
            ["Role", [("sample size and the context axis", {"bold": True, "color": STEEL})], [("the 19-substitution matrix, and confirmation across label sources", {"bold": True, "color": STEEL})]]]
    gf, yb = d.table(MX, 1.2, [2.3, 2.5, 2.7], rows, size=10.5, bold_first_col=True, nm="label sets")
    # records
    rx = 8.35
    rw = W - MX - rx
    d.rect(rx, 1.2, rw, 1.75, fill=INK, shape="round", nm="records panel")
    d.text(rx + 0.15, 1.27, rw - 0.3, 1.65, [P("processed/psi-*.tsv: one row per construct", size=10.5, color=AMBER, bold=True),
                                            P("id                            psi    sum", size=10, mono=True, color=GREY, space=3),
                                            P("A0A0B4J1Y8_IGLV9-49_1_mut24 1.884  364.9", size=10, mono=True, color=BG, space=2),
                                            P("A0A0B4J1Y8_IGLV9-49_1_mut26 2.168  199.1", size=10, mono=True, color=BG, space=2),
                                            P("A2RUQ5_C17orf102_2_mut10a   4.916  484.4", size=10, mono=True, color=BG, space=2),
                                            P("psi: 1…6, low = degraded = strong degron", size=10, color=GREY, space=3)], nm="records")
    # split sketch
    d.rect(rx, 3.1, rw, 2.0, fill="FFFFFF", line=LINE, shape="round", nm="split panel")
    d.text(rx + 0.12, 3.15, rw - 0.24, 0.28, [P("Split by protein cluster", size=11.5, bold=True)], nm="split title")
    groups = [(rx + 0.2, 3.55, STEEL), (rx + 1.05, 3.55, STEEL), (rx + 0.2, 4.3, STEEL), (rx + 1.05, 4.3, STEEL), (rx + 2.45, 3.55, CORAL), (rx + 2.45, 4.3, CORAL)]
    for gi, (gx, gy, c) in enumerate(groups):
        d.rect(gx, gy, 0.72, 0.6, fill=None, line=c, lw=1.5, shape="round", nm=f"cluster {gi + 1}")
        for k in range(4):
            d.rect(gx + 0.1 + (k % 2) * 0.28, gy + 0.1 + (k // 2) * 0.22, 0.17, 0.17, fill=c, shape="oval", nm=f"peptide {gi + 1}.{k + 1}")
    d.line(rx + 2.1, 3.45, rx + 2.1, 4.95, color=INK, lw=1.75, dash=True, nm="cut line")
    d.text(rx + 0.12, 4.9, 1.9, 0.2, [P("train", size=10, color=STEEL, bold=True)], nm="train label")
    d.text(rx + 2.45, 4.9, 1.2, 0.2, [P("test", size=10, color=CORAL, bold=True)], nm="test label")
    d.text(rx + 3.2, 3.5, rw - 3.3, 1.5, [P("the cut runs around clusters, never through one", size=10, color=MUTED)], nm="cut note")
    cons = card(d, MX, yb + 0.15, 7.5, 1.15, "Design consequence",
                [P("Learn the context axis on the scanning set, confirm the matrix on the saturation set. 61 of 89 saturation clusters also occur in the scanning set, so overlapping clusters are removed from training for every cross-source evaluation.", size=11, space=2)], accent=STEEL, tint=STEEL_T, hsize=12)
    d.text(rx, 5.2, rw, 1.45, [B("MMseqs2, ≥30% identity, 80% coverage: 5,088 clusters over 6,573 proteins", size=10.5, space=1),
                               B("labels are the mean of two replicates; every table reports the ceiling", size=10.5, space=1),
                               B("130 peptides appear in both sets and go to the same side", size=10.5, space=1),
                               B("BAG6-WT is a different condition, never pooled", size=10.5, space=1)], nm="split rules")
    source(d, "Own counts and measurements throughout. The protein cluster, not the peptide, is the unit of inference.", y=6.7)


def s21(d):
    s = d.slide("Proposed approach: a numeric target and a weak-supervision question", section=7, title_h=0.5, size=26,
                notes="SƯỜN: kiến trúc chưa chạy. Lý lẽ đã đổi sau phiên 8: KHÔNG nói 'MIL so với đầu theo vị trí chưa có tiền lệ' (mô típ chuẩn đã có, C-17 mục a); tính mới đặt ở GIÁM SÁT YẾU. "
                      "Năm câu cấm: 'novel aggregation mechanism' (BioBlobs 2025 có tiền lệ attention-MIL trên protein); 'MIL robust to noisy labels' (Ilse 2018 nói về nhãn vắng mặt, không phải nhiễu); 'nobody has placed an exposure gate at the pooling step' (Yang et al. PLOS Comput Biol 2026 là tập mẹ); 'MIL vs per-position head has no precedent'; mọi dạng 'nobody has done X'. "
                      "rASA/pLDDT không có phương sai trên nhãn chính, nên cổng phơi lộ không nằm trên đường găng (D-028 mục 1). Cần điền sau: chọn A/B/C, sơ đồ tensor, delta so với 0,7693 kèm bất định, ablation ô chéo.")
    blocks = [("data sources + counts", STEEL_T, False), ("filter, label, cluster split", STEEL_T, False), ("representation", STEEL_T, False), ("model (3 variants)", AMBER_T, True), ("evaluation + ceiling", TEAL_T, False)]
    bs = []
    for i, (t, c, prop) in enumerate(blocks):
        x = MX + i * 2.48
        bs.append(d.rect(x, 1.2, 2.2, 0.8, fill=c, line=("B08A1E" if prop else None), dash=prop, shape="round", nm=f"workflow block {i + 1}",
                         paras=[P(t, size=12, bold=True, color=INK, align="c")] + ([P("[proposed]", size=10, color="8A6A12", align="c")] if prop else []), margin=0.06))
        if i < 4:
            d.rect(x + 2.22, 1.5, 0.24, 0.2, fill=GREY, shape="rarrow", nm=f"flow arrow {i + 1}")
    vs = []
    for i, lab in enumerate(["A", "B", "C"]):
        vs.append(chip(d, MX + 3 * 2.48 + 0.1 + i * 0.7, 2.08, 0.62, lab, fill=AMBER_T, line="B08A1E", dash=True, size=12, h=0.28, nm=f"variant {lab}"))
    rows = [["Fixed and measured", "Decision"],
            ["Task", "residue-level effect: 28×20 matrix + per-position map"],
            ["Labels", "measured ΔPSI, mean of two replicates; two sets, two roles"],
            ["Primary metric", "cell-level AUROC (ceilings 0.9458 / 0.9519); secondary: position-level Spearman, precision@3"],
            ["Split", "protein cluster, MMseqs2 ≥30% / 80%; overlapping clusters removed for cross-source tests"],
            ["Baselines", "composition-only 0.8393 · ΔPAP cnn2w1 0.7943 · ΔPAP cnn2w7 0.8357 · best model 0.8682 (scanning)"],
            ["Detection threshold", "0.0123 (saturation, paired M3 − M0) · 0.0025–0.0036 (scanning)"],
            ["Where information sits", "±3 neighbourhood composition (80% of gain); absolute position ≈ 0"]]
    d.table(MX, 2.5, [1.65, 3.85], rows, size=11, bold_first_col=True, nm="fixed")
    rx = 6.4
    rw = W - MX - rx
    tg = d.rect(rx, 2.5, rw, 0.8, fill=CORAL_T, shape="round", nm="target",
                paras=[P(runs=[("Open, the architecture: ", {"bold": True, "color": CORAL}), ("beat 0.7693 cell-level AUROC on the substitution matrix. The current model is 0.0420 behind; the ceiling is 0.9519.", {})], size=12)], margin=0.15)
    vrows = [["Variant", "Idea", "Status"],
             ["A", "per-position head trained on cell-level labels: the standard choice, and the one to beat", "to be run"],
             ["B", "attention-MIL bridge: peptide as bag, ±3 windows as instances, pre-trained on the large bag-level sets (260k peptides, 212k tiles)", "to be run"],
             ["C", "hybrid: bag loss + cell loss with weight λ", "to be run"]]
    gf, yb = d.table(rx, 3.4, [0.7, 4.4, rw - 5.1], vrows, size=11, bold_first_col=True, fills={(1, 2): AMBER_T, (2, 2): AMBER_T, (3, 2): AMBER_T}, nm="variants")
    d.text(rx, yb + 0.1, rw, 1.75, [P("Novelty, at the level the evidence supports: a weak-supervision question.", size=11.5, bold=True, color=STEEL),
                                    P("Bag-level labels are abundant but do not identify positional parameters (28.9% of coefficients separable from zero); cell-level labels do (53.3%) but are fewer. A literature search on 15 Oct 2026 did not find an MIL/attention bridge reported for this; a negative answer is also a usable result. Attention-MIL on proteins, conditional modulation and accessibility features are established prior art, not claimed as new.", size=11, space=2)], nm="novelty")
    d.anim(bs[:3], [bs[3]] + vs, [bs[4]])
    source(d, "○ proposed, no measurement yet. Representation choice (PLM vs one-hot) is part of the same experiment grid. Own diagram, proposed, not yet validated.", y=6.72)


def s22(d):
    s = d.slide("Evaluation plan: one controlled comparison per row, four already measured", section=7, title_h=0.5, size=25,
                notes="Bảng đã đổi tính chất sau phiên 8: bốn dòng đầu ĐÃ có kết quả. Giữ ký hiệu ●/○ để GVHD thấy ngay đâu là đã đo. Khi chưa chạy thì ô ghi 'not measured', KHÔNG điền số minh họa. "
                      "Rủi ro LeBlanc 'thành phần > vị trí' trả lời bằng số: trên nhãn mức peptide/tile thành phần ổn định hơn vị trí ≈56 lần; trên nhãn hiệu ứng đột biến còn 2,2 lần, và tỉ lệ hệ số ngữ cảnh tách khỏi 0 tăng từ 28,9% lên 53,3%. "
                      "Nói kèm điều ngược lại: bộ bão hòa một mình thiếu lực cho tham số ngữ cảnh (25% trên 89 cụm), đó là lý do học ngữ cảnh trên bộ quét và xác nhận ma trận trên bộ bão hòa. Quy ước báo trần theo LeBlanc et al. 2026.")
    G, O = TEAL_T, AMBER_T
    rows = [["Question", "Held fixed", "Metric", "Status"],
            ["Does a residue-level model beat the composition baseline?", "split, labels, window", "cell-level AUROC", "● +0.0289, CI [0.0264, 0.0313]"],
            ["Does it beat the closest published control (ΔPAP)?", "same test clusters, paired", "paired difference + bootstrap CI", "● +0.0300 (scanning) · ○ −0.0420 (matrix)"],
            ["At which scale does the information sit?", "one feature block changed at a time", "same split, same metric", "● decomposed (slide 14)"],
            ["Are context weights stable across bootstraps?", "—", "sign agreement, |μ|/SD", "● 53.3% separable, sign agreement 0.90"],
            ["Does the MIL bridge recover residue information from bag-level labels?", "window, loss, budget, seeds", "bag metric and localisation metric", "○ not measured"],
            ["Does representation or architecture drive the gain?", "representation × model grid", "same split, same metric", "○ not measured"],
            ["Does it beat Degformer under a cluster split?", "its checkpoint re-run on our split", "same metrics", "○ not measured"],
            ["Where does the model fail?", "per-group sample counts", "error analysis by group", "○ not measured"]]
    fills = {(i, 3): (G if i <= 4 else O) for i in range(1, 9)}
    gf, yb = d.table(MX, 1.2, [3.45, 2.25, 2.0, 2.15], rows, size=11, fills=fills, nm="evaluation plan")
    d.text(MX, yb + 0.15, 9.85, 1.0, [P(runs=[("Committed in advance: ", {"bold": True}), ("thresholds are computed before ablations (0.0123 for the paired M3 − M0 comparison on the saturation set; 0.0025–0.0036 on scanning); a result below threshold is reported as indistinguishable, not as a win. Bootstrap is at protein-cluster level, paired by peptide.", {})], size=11),
                                       P("Every results table prints the measured ceiling next to the model number and reports each metric separately, because the model ranking reverses between cell-level and position-level scoring (ceiling convention after LeBlanc et al. 2026).", size=11, space=4)], nm="commitments")
    # grid
    gx, gy = 10.7, 1.55
    d.text(10.5, 1.15, 2.3, 0.3, [P("Experiment grid", size=12, bold=True)], nm="grid title")
    d.text(gx + 0.95, gy, 0.5, 0.3, [P("one-hot", size=10, align="c")], nm="col 1", check=False)
    d.text(gx + 1.5, gy, 0.5, 0.3, [P("PLM", size=10, align="c")], nm="col 2", check=False)
    for i, lab in enumerate(["composition", "per-position", "MIL bridge", "hybrid"]):
        y = gy + 0.38 + i * 0.58
        d.text(gx - 0.2, y + 0.12, 1.1, 0.3, [P(lab, size=10, align="r")], nm=f"row {lab}", check=False)
        for j in range(2):
            done = (i == 0 and j == 0)
            d.rect(gx + 0.95 + j * 0.55, y, 0.5, 0.5, fill=(TEAL_T if done else AMBER_T), line=(TEAL if done else "B08A1E"), shape="rect", nm=f"grid cell {lab} {j}",
                   paras=[P("●" if done else "—", size=12, bold=True, color=("1F7A6F" if done else "8A6A12"), align="c")], margin=0)
    d.text(10.5, 4.15, 2.25, 1.0, [P("model × representation: teal = baseline measured, amber = not yet run", size=10, color=MUTED)], nm="grid caption")
    source(d, "● measured, with result files · ○ planned, no number yet.", y=6.72)
