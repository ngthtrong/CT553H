"""Kiểm khớp nguyên mẫu G3 với đường huấn luyện/runner (PROTOCOL §7). Chênh tối đa phải < 1e-9.

  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/calibration-p6-2026-10-22/verify.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
import sys, json, csv, io, contextlib
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(HERE))
import run_calibration as cal       # noqa: E402
import predict as pr                # noqa: E402
rc, rd, dr = cal.rc, cal.rd, cal.dr
TOL = 1e-9
report = {}


def check(name, a, b, tol=TOL):
    m = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
    report[name] = {'max_abs_diff': m, 'n': int(np.size(a)), 'pass': bool(m < tol)}
    print(f'{name:55s} max|Δ| = {m:.3e}  {"OK" if m < tol else "FAIL"}', flush=True)
    assert m < tol, name


def main():
    model = pr.load_model()
    tp = np.load(TOPIC / 'data/processed/calibration-p6-trainpath.npz', allow_pickle=False)
    peps, Xc, y, idx, rowg, groups, _ = rc.build(rc.EXT_PSI_MAX, f'ext{rc.EXT_PSI_MAX}')
    assert list(peps) == list(tp['peps'])
    d = rd.load_all(degron_psi_max=rc.EXT_PSI_MAX)
    peps2, rows, y2, idx2 = dr.rows_and_labels(d['sat'], 'sat')
    assert list(peps2) == list(peps) and len(rows) == len(y)
    check('nhãn y: load_all vs cache', y2, y)

    # 1. đặc trưng dựng độc lập trong predict.py == ma trận cache
    Xp = np.array([pr.featurize(s, p, a) for s, p, a in rows])
    check('đặc trưng predict.featurize vs cache X', Xp, Xc[:, :180])

    # 2. điểm thô và xác suất qua đường predict == đường huấn luyện (Ridge.predict, sklearn)
    score = Xp @ model['coef'] + float(model['intercept'][0])
    check('điểm thô: predict vs Ridge.predict', score, tp['score'])
    check('xác suất platt: predict vs sklearn', pr.calibrate(model, score, 'platt'), tp['platt'])
    check('xác suất iso: predict vs sklearn', pr.calibrate(model, score, 'iso'), tp['iso'])

    # 3. đường UniProt -> tile -> predict_tile cho mọi peptide
    up = pr.load_uniprot()
    worst_s = worst_p = 0.0
    n_cmp = 0
    for k, pep in enumerate(peps):
        a, b = idx[k]
        acc, n = pep.split('_')[0], int(pep.split('_')[-1])
        seq = pr.tile_seq(up[acc], n)
        assert seq == rows[a][0], pep
        cells, s, p, rank = pr.predict_tile(model, seq)
        lut = {c: (si, pi) for c, si, pi in zip(cells, s, p)}
        for j in range(a, b):
            si, pi = lut[(rows[j][1], rows[j][2])]
            worst_s = max(worst_s, abs(si - score[j]))
            worst_p = max(worst_p, abs(pi - pr.calibrate(model, score[j:j + 1])[0]))
            n_cmp += 1
    check('UniProt->tile->predict_tile: điểm vs đường huấn luyện', [worst_s], [0.0])
    check('UniProt->tile->predict_tile: xác suất', [worst_p], [0.0])
    report['tile_path_cells_compared'] = n_cmp

    # 4. CLI: CSV ghi ra khớp predict_tile (định dạng %.10g)
    pep = peps[0]
    buf = io.StringIO()
    out = HERE / 'example-output.csv'
    with contextlib.redirect_stderr(io.StringIO()):
        pr.main(['--uniprot', pep.split('_')[0], '--tile', pep.split('_')[-1], '--out', str(out)])
    rows_csv = list(csv.DictReader(out.open()))
    seq = pr.tile_seq(up[pep.split('_')[0]], int(pep.split('_')[-1]))
    cells, s, p, rank = pr.predict_tile(model, seq)
    check('CLI CSV: điểm', [float(r['score_dpsi_raw']) for r in rows_csv], s, 5e-9)
    check('CLI CSV: xác suất', [float(r['p_dpsi_ge_1_calibrated']) for r in rows_csv], p, 5e-9)
    assert len(rows_csv) == 28 * 19

    # 5. runner: điểm outer-test của MỌI (seed, fold) tái tạo từ hệ số fold bằng đường predict
    oof = np.load(TOPIC / 'data/processed/calibration-p6-oof.npz', allow_pickle=False)
    base = set(rc.build(rd.DEGRON_PSI_MAX, 'base')[0])
    sel = [k for k, pep in enumerate(peps) if pep in base]
    rows_b = [rows[j] for k in sel for j in range(*idx[k])]
    X0 = rc.build(rd.DEGRON_PSI_MAX, 'base')[1]
    check('đặc trưng bộ gốc: predict.featurize vs cache X0', np.array([pr.featurize(*r) for r in rows_b]), X0[:, :180])
    Xb = Xp[np.concatenate([np.arange(*idx[k]) for k in sel])]
    off = np.concatenate([[0], np.cumsum(oof['test_fold_sizes'])])
    worst = 0.0
    for si, seed in enumerate(rc.SEEDS):
        for f in range(5):
            te = oof['test_rows'][off[f]:off[f + 1]]
            w, b = oof['coef'][si * 5 + f], oof['intercept'][si * 5 + f]
            worst = max(worst, float(np.abs(Xb[te] @ w + b - oof['score_by_seed'][si][te]).max()))
    check('runner: điểm outer-test 15 (seed,fold) vs hệ số fold', [worst], [0.0])

    (HERE / 'verify.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print('TẤT CẢ KHỚP (< 1e-9) ->', HERE / 'verify.json')


if __name__ == '__main__':
    main()
