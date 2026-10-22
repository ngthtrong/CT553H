"""R3 — phân tích CỤC BỘ NHẸ (không huấn luyện) để trả lời các điều [CHƯA XÁC MINH] trước khi chốt PROTOCOL.

Câu hỏi:
  Q1. Tile của sàng peptidome GPS (gps-peptidome-rep1.tsv, tên `ACC_GENE_n`) có cùng định danh/quy tắc tile
      `(n-1)*23, dài 28` với 176 peptide của bộ ΔPSI không?
  Q2. PSI đo của tile trong sàng có cùng thang với PSI(WT) nội tại (trung vị ô đồng nghĩa) dùng để định nghĩa
      miền `PSI(WT) <= 4,0` không (tương quan, lệch, đồng thuận phân loại)?
  Q3. Sàng phủ bao nhiêu tile toàn proteome, và tỉ lệ tile `PSI <= 4,0`?
  Q4. Độ tin cậy của PSI đo: phụ thuộc số reads thế nào (để chốt ngưỡng reads của tầng tra cứu).

Chạy từ gốc repo:  .venv/bin/python -I topics/degron-footprint/research/r3-domain-gate-2026-10-22/local_analysis.py
Chỉ đọc dữ liệu; không phân cụm mới, không huấn luyện. Kết quả -> local-analysis.json
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
import residue_data as rd  # noqa: E402

PEPTIDOME = TOPIC / 'data/interim/gps-peptidome-rep1.tsv'
READ_MIN = rd.READ_MIN        # 10
DOMAIN = [3.0, 4.0]


def spearman(a, b):
    from scipy.stats import spearmanr
    r = spearmanr(a, b)
    return float(r[0])


def auroc(score, label):
    from scipy.stats import rankdata
    label = np.asarray(label, bool)
    n1, n0 = label.sum(), (~label).sum()
    if n1 == 0 or n0 == 0:
        return None
    r = rankdata(score)
    return float((r[label].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def load_peptidome():
    rows = {}
    n_na = 0
    with PEPTIDOME.open(encoding='utf-8') as fh:
        next(fh)
        for line in fh:
            p = line.rstrip('\n').split('\t')
            try:
                reads = float(p[1])
            except ValueError:
                reads = float('nan')
            psi = float('nan') if p[2] == 'NA' else float(p[2])
            if math.isnan(psi):
                n_na += 1
            rows[p[0]] = (reads, psi)
    return rows, n_na


def main():
    out = {'script': 'local_analysis.py', 'read_min': READ_MIN}
    pept, n_na = load_peptidome()
    uniprot = rd.load_uniprot()
    out['peptidome'] = {'n_rows': len(pept), 'n_psi_na': n_na}

    # ---- Q1: quy tắc tile và định danh
    def parts(name):
        s = name.split('_')
        try:
            return s[0], int(s[-1])
        except ValueError:
            return None, None
    in_up = full = ok_tile = bad_tile = 0
    for name in pept:
        acc, n = parts(name)
        if acc in uniprot:
            in_up += 1
            if rd.derive_sequence(name, uniprot) is not None:
                full += 1
    out['Q1_naming'] = {
        'n_peptidome_names_parse_ok': sum(1 for n in pept if parts(n)[0] is not None),
        'n_with_accession_in_uniprot_snapshot': in_up,
        'n_with_full_28mer_by_rule': full,
        'note': 'quy tắc tile (n-1)*23, dài 28 — đúng quy tắc residue_data.derive_sequence; trình tự thật của '
                'tile sàng KHÔNG có trong file (chỉ có tên) nên không đối chiếu trực tiếp được; đối chiếu gián '
                'tiếp qua Q2 (cùng tên -> cùng PSI?)'}

    # ---- 176 peptide của bộ ΔPSI (cache ext 4.0) và 248 thô qua build_saturation(psi_max rất lớn)
    z = np.load(TOPIC / 'data/processed/learning-curve-sat-ext4.0.npz', allow_pickle=True)
    peps176 = list(z['peps'])
    seqs, _ = rd.load_scan_csv()
    sat = rd.build_saturation(rd.load_psi('sat_a'), rd.load_psi('sat_b'), seqs, uniprot,
                              degron_psi_max=99.0)
    rep1 = rd.load_psi('rep1')                      # PSI mốc WT của sàng quét (tên _mut0)
    # file nhãn miền cho runner R3 (gói dữ liệu): peptide, PSI(WT) nội tại, thuộc 176 hay không, cụm
    clusters = {}
    for l in (TOPIC / 'data/interim/protein-id30-cov80-proteome_cluster.tsv').read_text().splitlines():
        r, m = l.split('\t')[:2]
        clusters[m] = r
    pool_path = TOPIC / 'data/processed/r3-sat-wt-pool.tsv'
    with pool_path.open('w', encoding='utf-8') as fh:
        fh.write('peptide\tpsi_wt_internal\tin_176\taccession\tcluster_cov80\n')
        for pep in sorted(sat):
            acc = rd.accession(pep)
            fh.write(f'{pep}\t{sat[pep]["psi_wt"]:.10g}\t{int(pep in set(peps176))}\t{acc}\t'
                     f'{clusters.get(acc, acc)}\n')
    out['sat_pool'] = {'n_peptides_after_technical_filters': len(sat),
                       'n_in_176': len(set(sat) & set(peps176)),
                       'n_176_not_in_pool': len(set(peps176) - set(sat))}

    # ---- Q2: PSI tile (sàng peptidome) vs PSI(WT) nội tại (bão hòa)
    names = [p for p in sat if p in pept]
    out['Q2_overlap'] = {'n_sat_pool': len(sat), 'n_in_peptidome_file': len(names),
                         'n_with_psi': 0}
    A, B, RD, WTSC = [], [], [], []
    for p in names:
        reads, psi = pept[p]
        if math.isnan(psi) or reads < READ_MIN:
            continue
        A.append(psi)
        B.append(sat[p]['psi_wt'])
        RD.append(reads)
        WTSC.append(rep1.get(f'{p}_mut0', float('nan')))
    A, B, RD, WTSC = map(np.asarray, (A, B, RD, WTSC))
    out['Q2_overlap']['n_with_psi'] = int(len(A))
    q2 = {'n': int(len(A)),
          'pearson': float(np.corrcoef(A, B)[0, 1]), 'spearman': spearman(A, B),
          'mean_diff_peptidome_minus_sat_internal': float((A - B).mean()),
          'median_abs_diff': float(np.median(np.abs(A - B))),
          'slope_ols_sat_on_peptidome': float(np.polyfit(A, B, 1)[0]),
          'intercept_ols': float(np.polyfit(A, B, 1)[1]),
          'rmse': float(np.sqrt(((A - B) ** 2).mean()))}
    ok = ~np.isnan(WTSC)
    if ok.sum() > 10:
        q2['vs_scanning_wt_mut0'] = {'n': int(ok.sum()),
                                     'pearson': float(np.corrcoef(A[ok], WTSC[ok])[0, 1]),
                                     'mean_diff': float((A[ok] - WTSC[ok]).mean())}
    cls = {}
    for t in DOMAIN:
        lab = B <= t
        pred = A <= t
        cls[f'threshold_{t}'] = {
            'n_in_domain_by_sat_wt': int(lab.sum()),
            'accuracy': float((pred == lab).mean()),
            'auroc_peptidome_psi_for_in_domain': auroc(-A, lab),
            'sensitivity': float((pred & lab).sum() / max(1, lab.sum())),
            'specificity': float((~pred & ~lab).sum() / max(1, (~lab).sum()))}
    q2['classification_agreement'] = cls
    # phụ thuộc reads
    by_reads = {}
    for lo, hi in ((10, 30), (30, 100), (100, 1e9)):
        m = (RD >= lo) & (RD < hi)
        if m.sum() >= 8:
            by_reads[f'{lo}-{hi:g}'] = {'n': int(m.sum()),
                                        'pearson': float(np.corrcoef(A[m], B[m])[0, 1]),
                                        'rmse': float(np.sqrt(((A[m] - B[m]) ** 2).mean()))}
    q2['by_reads'] = by_reads
    out['Q2_scale'] = q2

    # ---- Q3: phủ proteome
    n_prot = len(uniprot)
    tiles_full = 0
    for acc, s in uniprot.items():
        L = len(s)
        if L >= rd.TILE_LEN:
            tiles_full += (L - rd.TILE_LEN) // rd.TILE_STEP + 1
    measured = psis = 0
    meas_vals = []
    n_meas_in_full = 0
    for name, (reads, psi) in pept.items():
        if math.isnan(psi) or reads < READ_MIN:
            continue
        measured += 1
        meas_vals.append(psi)
        if parts(name)[0] in uniprot and rd.derive_sequence(name, uniprot) is not None:
            n_meas_in_full += 1
    mv = np.asarray(meas_vals)
    out['Q3_coverage'] = {
        'n_proteins_snapshot': n_prot, 'n_full_28mer_tiles_in_proteome_by_rule': int(tiles_full),
        'n_peptidome_rows': len(pept), 'n_rows_with_psi_and_reads_ge_10': measured,
        'n_measured_tiles_matching_full_tile_by_rule': n_meas_in_full,
        'coverage_of_proteome_tiles': n_meas_in_full / tiles_full,
        'share_psi_le_3.0': float((mv <= 3.0).mean()), 'share_psi_le_4.0': float((mv <= 4.0).mean()),
        'psi_quantiles': {str(q): float(np.quantile(mv, q)) for q in (.05, .25, .5, .75, .95)},
        'n_proteins_with_any_measured_tile': len({parts(n)[0] for n, (r, p) in pept.items()
                                                   if not math.isnan(p) and r >= READ_MIN}),
        'note': 'tile_full = tile 28-mer đủ độ dài theo quy tắc; tile cuối ngắn hơn 28 aa bị bỏ'}

    # ---- Q4: tin cậy theo reads (độ phân tán PSI giữa hai tile cùng chuỗi không có; dùng phân bố reads)
    rv = np.asarray([r for r, p in pept.values() if not math.isnan(p)])
    out['Q4_reads'] = {'quantiles_reads': {str(q): float(np.quantile(rv, q)) for q in (.05, .25, .5, .75, .95)},
                       'share_reads_ge_10': float((rv >= READ_MIN).mean()),
                       'share_reads_ge_30': float((rv >= 30).mean())}

    (HERE / 'local-analysis.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
