from comp import *
import os
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "lectures", "degron-footprint", "assets", "figures")


def s01(d):
    s = d.slide("Residue-Level Prediction of Degron Mutation Effects from Experimental Protein-Stability Data", dark=True, section=1, size=38, title_h=1.9,
                notes="Tiêu đề theo khuôn [bài toán] bằng [nguồn nhãn]; chưa đặt tên mô hình (lựa chọn 3 của Trọng). Không dùng chữ 'enhanced/improved/novel'. "
                      "Dải 28 ô là hình minh họa một peptide 28 residue; các ô san hô = residue mang tín hiệu degron (lấy đúng vị trí 15–19 của peptide ví dụ ở slide 16).")
    s.shapes.title.top = Inches(1.35)
    chip(d, MX, 0.7, 3.9, "Undergraduate thesis proposal · CT553H", fill="24475A", color=BG, size=12, h=0.34, bold=False)
    d.text(MX, 3.0, 7.2, 1.0, [P("Software Engineering, College of Information and Communication Technology", size=15, color="C9D6DC"),
                                P("Can Tho University", size=15, color="C9D6DC")], nm="affiliation")
    d.text(8.2, 3.0, 4.5, 1.2, [P(runs=[("Student  ", {"color": GREY}), ("Nguyễn Thế Trọng — B2305615", {"bold": True})], size=15, color=BG),
                                P(runs=[("Advisor  ", {"color": GREY}), ("Dr. Hồ Quang Thái", {"bold": True})], size=15, color=BG, space=6),
                                P("Progress report, week 6 · October 2026", size=15, color=AMBER, space=10)], nm="people")
    cells = strip(d, MX, 4.9, 28, 0.34, gap=0.052, coral=(), fills=["2F4B59"] * 28, nm="peptide cell")
    hot = [d.rect(MX + i * (0.34 + 0.052), 4.9, 0.34, 0.34, fill=CORAL, nm=f"degron residue {i + 1}") for i in range(14, 19)]
    d.text(MX, 5.4, 11, 0.3, [P("Illustration: one 28-residue peptide; coral residues are the ones that carry the degron signal.", size=11, color=GREY)], nm="caption")
    d.anim(hot)


def s02(d):
    s = d.slide("Proteins are chains of amino acid residues, and one residue can change", section=2,
                notes="Phân biệt residue (vị trí) và loại acid amin (chất nằm ở vị trí đó) phải nói ngay ở đây: cả đề tài đứng trên ma trận 28 vị trí × 20 loại. "
                      "Animation 3 bước: chuỗi → gập → đột biến M7V. GIF: Protein synthesis (Translation), Tekksavvy, CC BY-SA 3.0 (Commons).")
    d.text(MX, 1.6, 7.9, 2.0, [
        P("Proteins do the work of the cell: catalysis, signalling, structure, transport.", size=17, bold=True),
        B("A protein is a linear chain of amino acids; each link is a residue", size=14),
        B("20 standard amino acid types; the order is the sequence, e.g. GAKTYIMQRQLS…", size=14),
        B("The sequence sets the 3-D fold, and the fold sets the function", size=14),
    ], nm="intro")
    d.table(MX, 3.55, [1.9, 6.0], [["Term", "Meaning"], ["Residue", "one position in the chain: “position 7”"],
                                   ["Amino acid type", "what sits at that position: “methionine”"]], size=13, bold_first_col=True, nm="terms")
    d.text(MX, 4.85, 7.9, 0.6, [P(runs=[("A mutation ", {"bold": True}), ("changes the type at one residue: ", {}), ("M7V", {"bold": True, "mono": True, "color": CORAL}),
                                       (" = methionine → valine at position 7.", {})], size=14)], nm="mutation def")
    # GIF
    d.rect(9.0, 1.6, 3.73, 3.73, fill="FFFFFF", line=LINE, shape="round", nm="gif card")
    d.pic(os.path.join(A, "translation.gif"), 9.05, 1.65, w=3.63, h=3.63, alt="Animated schematic of mRNA translation by a ribosome adding amino acids to a growing chain")
    d.text(9.0, 5.4, 3.73, 0.55, [P("Translation: a ribosome links amino acids into a chain. Animation: Tekksavvy, CC BY-SA 3.0, Wikimedia Commons.", size=10, color=MUTED)], nm="gif caption")
    # chain
    seq = "GAKTYIMQRQLS"
    beads, nums = [], []
    for i, ch in enumerate(seq):
        x = MX + i * 0.62
        beads.append(d.rect(x, 5.75, 0.46, 0.46, fill=STEEL, shape="oval", nm=f"residue {i + 1}", paras=[P(ch, size=13, bold=True, mono=True, color=BG, align="c")], margin=0))
        nums.append(d.text(x, 6.24, 0.46, 0.22, [P(str(i + 1), size=10, color=MUTED, align="c")], nm=f"index {i + 1}"))
    fold = chip(d, 8.2 - 0.1, 5.78, 0.9, "fold", fill=STEEL_T, color=STEEL, size=12, h=0.36, nm="fold label")
    ar = d.rect(8.0, 5.85, 0.2, 0.22, fill=GREY, shape="rarrow", nm="arrow")
    mut = d.rect(MX + 6 * 0.62, 5.75, 0.46, 0.46, fill=CORAL, shape="oval", nm="mutated residue", paras=[P("V", size=13, bold=True, mono=True, color=BG, align="c")], margin=0)
    mlab = chip(d, MX + 6 * 0.62 - 0.35, 6.5, 1.16, "M7V  mutation", fill=CORAL_T, color=CORAL, size=11, h=0.28, nm="mutation label")
    d.anim(beads + nums, [fold, ar], [mut, mlab])
    # fold/mutation both on the beads row; keep text separation
    d.text(MX, 5.4, 6, 0.3, [P("Click: chain  →  fold  →  mutation", size=10, color=MUTED, italic=True)], nm="hint")
    d.shift(0.4)


def s03(d):
    s = d.slide("Protein level is set by a balance: synthesis against degradation", section=2,
                notes="Slide này giải thích vì sao độ bền là đại lượng đáng dự đoán. Cố ý không có con số định lượng. Phương trình viết ở dạng tốc độ dP/dt (không đồng nhất lượng với tốc độ). "
                      "Animation: mũi tên tổng hợp → mũi tên phân hủy nặng hơn → mức protein tụt.")
    # visual
    cell = d.rect(2.2, 2.0, 2.6, 3.4, fill=STEEL_T, line=STEEL, lw=1.5, shape="round", nm="cell")
    d.text(2.2, 1.62, 2.6, 0.32, [P("protein level in the cell", size=12, bold=True, color=STEEL, align="c")], nm="cell label")
    level = d.rect(2.35, 2.2, 2.3, 3.05, fill=STEEL, shape="rect", nm="protein level")
    cover = d.rect(2.35, 2.2, 2.3, 1.55, fill=STEEL_T, shape="rect", nm="level drop")
    syn = d.rect(0.6, 2.75, 1.5, 0.75, fill=TEAL, shape="rarrow", nm="synthesis arrow", paras=[P("in", size=13, bold=True, color=BG, align="c")], margin=0.02)
    syl = d.text(0.6, 3.55, 1.5, 0.5, [P("synthesis", size=14, bold=True, color=TEAL, align="c")], nm="synthesis label")
    deg = d.rect(4.9, 3.4, 1.9, 1.15, fill=CORAL, shape="rarrow", nm="degradation arrow", paras=[P("out", size=14, bold=True, color=BG, align="c")], margin=0.02)
    dgl = d.text(4.9, 4.6, 1.9, 0.5, [P("degradation", size=14, bold=True, color=CORAL, align="c")], nm="degradation label")
    d.text(0.6, 5.6, 6.2, 0.6, [P("Click: synthesis  →  faster degradation  →  the level falls", size=10, color=MUTED, italic=True)], nm="hint")
    d.anim([syn, syl], [deg, dgl], [cover])
    # text
    d.rect(7.3, 1.6, 5.43, 0.8, fill=INK, shape="round", nm="equation",
           paras=[P(runs=[("dP/dt  =  rate of synthesis  −  rate of degradation", {})], size=17, bold=True, color=BG, align="c")], margin=0.15)
    d.text(7.3, 2.65, 5.43, 2.4, [P("Cells destroy proteins on purpose, and constantly:", size=15, bold=True),
                                  B("to switch signals off on schedule (cell-cycle regulators, transcription factors)", size=14),
                                  B("to clear misfolded or damaged copies before they aggregate", size=14),
                                  B("to adjust quickly to changed conditions", size=14)], nm="reasons")
    card(d, 7.3, 5.0, 5.43, 1.45, "Consequence", "A protein that is made correctly but destroyed too fast is just as absent as one that was never made. Degradation is a control layer in its own right.",
         accent=CORAL, tint=CORAL_T, bsize=14, hsize=15)
    d.shift(0.4)


def s04(d):
    s = d.slide("Ubiquitin–proteasome degradation has three steps; specificity lives in step one", section=2,
                notes="Con số 'over 600 E3 ligases' lấy từ DegronMD (Xu et al., Mol Biol Evol 40(12), 2023, DOI 10.1093/molbev/msad253). "
                      "GIF 2QJL là URM1, protein họ giống ubiquitin (nếp β-grasp), chỉ minh họa cấu trúc, KHÔNG phải ubiquitin hay E3 của người. Hsp90, CC BY-SA 3.0. "
                      "Ba bước animation khớp ba dòng bên trái.")
    steps = [("1  Recognition", "an E3 ubiquitin ligase binds a specific signal in the target protein"),
             ("2  Tagging", "the E3 transfers chains of ubiquitin, a small marker protein, onto the target"),
             ("3  Degradation", "the 26S proteasome recognises the chain, unfolds the target and cuts it into peptides")]
    for i, (h, b) in enumerate(steps):
        card(d, MX, 1.6 + i * 0.98, 5.9, 0.88, h, b, accent=[STEEL, AMBER if False else "B08A1E", CORAL][i], tint=[STEEL_T, AMBER_T, CORAL_T][i], hsize=14, bsize=12.5)
    gif = d.pic(os.path.join(A, "ubl-2qjl.gif"), MX, 4.65, w=1.9, h=1.634, alt="Rotating structure of a ubiquitin-like protein (URM1, PDB 2QJL)")
    d.text(2.7, 4.65, 3.8, 1.7, [P("Scale of the recognition problem", size=13, bold=True, color=STEEL),
                                 P("The human genome encodes over 600 E3 ligases, each recognising its own targets. The specificity of the whole system therefore lives in step 1.", size=13, space=3)], nm="scale")
    d.text(MX, 6.32, 5.9, 0.4, [P("Structure: ubiquitin-fold protein URM1 (PDB 2QJL), Hsp90, CC BY-SA 3.0.", size=10, color=MUTED)], nm="gif caption")
    # schematic (own diagram)
    d.rect(6.9, 1.6, 5.83, 4.7, fill="FFFFFF", line=LINE, shape="round", nm="schematic panel")
    d.text(7.05, 1.68, 3, 0.3, [P("own diagram, simplified", size=10, color=MUTED)], nm="schematic label")
    prot = d.rect(7.2, 3.95, 2.7, 0.85, fill="C9D4D9", shape="round", nm="target protein", paras=[P("target protein", size=12, color=INK, align="r")], margin=0.15, anchor="m")
    dg = d.rect(7.35, 4.05, 0.75, 0.65, fill=CORAL, shape="rect", nm="degron segment", paras=[P("degron", size=10, bold=True, color=BG, align="c")], margin=0)
    e3 = d.rect(7.0, 2.2, 1.9, 0.75, fill=STEEL, shape="round", nm="E3 ligase", paras=[P("E3 ligase", size=14, bold=True, color=BG, align="c")], margin=0.05)
    ln1 = d.line(7.72, 2.95, 7.72, 4.05, color=STEEL, lw=2.5, arrow=True, nm="binding")
    ubq = [d.rect(8.4 + i * 0.32, 3.62, 0.3, 0.3, fill=AMBER, line="B08A1E", lw=0.75, shape="oval", nm=f"ubiquitin {i + 1}") for i in range(4)]
    ubl = d.text(8.3, 3.2, 1.7, 0.3, [P("ubiquitin chain", size=11, bold=True, color="8A6A12")], nm="ubiquitin label")
    pro = d.rect(10.7, 2.1, 1.7, 2.2, fill="5B7380", shape="can", nm="proteasome", paras=[P("26S proteasome", size=12, bold=True, color=BG, align="c")], margin=0.05)
    arr = d.line(9.9, 4.2, 10.7, 3.5, color=CORAL, lw=2.5, arrow=True, nm="entry")
    frs = [d.rect(10.85 + i * 0.5, 4.65, 0.4, 0.18, fill=CORAL, shape="round", nm=f"peptide fragment {i + 1}") for i in range(3)]
    frl = d.text(10.7, 4.9, 1.9, 0.3, [P("short peptides", size=11, bold=True, color=CORAL)], nm="fragments label")
    d.text(7.05, 5.55, 5.5, 0.65, [P("Click through the three steps: recognition → tagging → degradation", size=10, color=MUTED, italic=True)], nm="hint")
    d.anim([e3, ln1], ubq + [ubl], [pro, arr] + frs + [frl])
    source(d, "Mechanism established in the literature. E3 count as reported in DegronMD, Xu et al., Mol Biol Evol 40(12), 2023.", y=6.72)
    d.shift(0.4)
    d.cur.shapes[-1].top = Inches(6.72)


def s05(d):
    s = d.slide("A degron is the recognition signal, and the question is which residues carry it", section=2,
                notes="Câu scope statement là yêu cầu cứng, phải nằm ngay slide định nghĩa bài toán. Cụm 'autonomous degrons' theo D-035 (giới hạn của assay, đã đo). "
                      "Phân bố 19%/30%/51% (Voutsinos 2026) để dành tới slide 10. Animation zoom 3 tầng: protein → 28-mer → residue.")
    d.text(MX, 1.55, 6.3, 2.9, [
        P(runs=[("A degron ", {"bold": True}), ("is the short segment of a protein that an E3 ligase recognises to mark it for degradation: the “address label” of step 1.", {})], size=14),
        B("Typically a short linear motif: a few to a few tens of residues", size=13),
        B("Can sit at the N-terminus, C-terminus, or internally", size=13),
        B("Strength is graded, not binary: strong, intermediate, inactive", size=13),
        P("The thesis question is one level finer:", size=14, bold=True, color=CORAL, space=8),
        P("Within a degron, which individual residues determine its strength, and by how much does the strength change when one of them is substituted?", size=14, italic=True, space=2),
    ], nm="definition")
    # zoom visual
    d.rect(7.3, 1.55, 5.43, 3.0, fill="FFFFFF", line=LINE, shape="round", nm="zoom panel")
    blob = d.rect(7.55, 1.8, 1.5, 1.2, fill="C9D4D9", shape="oval", nm="whole protein", paras=[P("protein", size=11, color=MUTED, align="c")], anchor="b", margin=0.1)
    patch = d.rect(8.3, 1.95, 0.5, 0.4, fill=AMBER, shape="oval", nm="degron region")
    st = strip(d, 7.55, 3.65, 28, 0.15, gap=0.02, nm="residue")
    hot = [d.rect(7.55 + i * 0.17, 3.65, 0.15, 0.15, fill=CORAL, nm=f"key residue {i + 1}") for i in (14, 15, 16, 18)]
    d.text(7.55, 3.9, 4.8, 0.3, [P("28-residue peptide", size=11, color=MUTED)], nm="l2")
    q = chip(d, 10.0, 2.15, 2.5, "which residues?", fill=CORAL_T, color=CORAL, size=14, h=0.42, nm="question chip")
    zl = d.line(8.55, 2.35, 7.62, 3.65, color=GREY, lw=1, dash=True, nm="zoom line")
    d.anim([patch], [zl] + st, hot + [q])
    d.rect(MX, 4.85, W - 2 * MX, 1.25, fill=AMBER_T, shape="round", nm="scope panel")
    d.text(MX + 0.2, 4.93, W - 2 * MX - 0.4, 1.4, [
        P("Scope", size=13, bold=True, color="8A6A12"),
        P("Labels in this work are measured on isolated 28-residue peptides fused to a reporter, so the assay sees autonomous degrons: signals that work inside the 28-mer on their own. "
          "Degrons that need priming (for example phosphorylation by another kinase) are outside its reach. "
          "Predictions describe peptide-level stability and do not by themselves establish an effect on the intact protein or any therapeutic effect.", size=13, space=3)], nm="scope")
    d.shift(0.4)
