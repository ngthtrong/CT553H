"""R6 — điều phối các giai đoạn. Notebook chỉ gọi các hàm ở đây; kiểm cục bộ bằng `selftest_r6.py`.

Giai đoạn (PROTOCOL §4): 0 cổng + kiểm chéo nguồn · A ridge ngữ cảnh rộng · B ridge + scanning · C trích ESM-2 ·
D ridge + ESM theo cỡ · E mạng CNN/mCNN · F quét cỡ ESM với mCNN · G mạng + scanning.
Mọi điểm OOF lưu ở `r6-oof-<tên>.npz` (khóa s17, s29, s43), nên có thể tổng hợp lại ngoài notebook:
    python -I run_r6.py <thư-mục-chứa-r6-oof-*.npz>
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r6data as r6                                   # noqa: E402
import r6stats as st                                  # noqa: E402
import derisk as dr                                   # noqa: E402

cm = r6.cm
SEEDS = r6.SEEDS
ALPHAS = cm.ALPHAS
WIDTHS = (5, 7, 10)                                   # PROTOCOL §4 giai đoạn A (đối chứng: 3)
SIZES = ('esm8', 'esm35', 'esm150', 'esm650')
PRIMARY_SIZE = 'esm35'
LC_RESULTS = cm.TOPIC / 'research/learning-curve-2026-10-22/results.json'
R2_RESULTS = cm.TOPIC / 'research/r2-esm-features-2026-10-22'

# cấu hình mạng: khóa -> (biểu diễn, cửa sổ tích chập, số bộ lọc mỗi cửa sổ)   PROTOCOL §3
NN_SPECS = {
    'oh_cnn1': ('onehot', (5,), 96),
    'oh_mcnn': ('onehot', (3, 5, 7), 32),
    'esm35_cnn1': ('esm35', (5,), 96),
    'esm35_mcnn': ('esm35', (3, 5, 7), 32),
    'esm8_mcnn': ('esm8', (3, 5, 7), 32),
    'esm150_mcnn': ('esm150', (3, 5, 7), 32),
    'esm650_mcnn': ('esm650', (3, 5, 7), 32),
}
SCAN_MODES = ('scan_pool', 'scan_ft')


# ------------------------------------------------------------------ lưu / nạp OOF
def _fname(name):
    return f'r6-oof-{name.replace("+", "__")}.npz'


def save_oof(out_dir, name, oof):
    np.savez(Path(out_dir) / _fname(name), **{f's{s}': a for s, a in oof.items()})


def load_one_oof(d, name):
    z = np.load(Path(d) / _fname(name))
    return {int(k[1:]): z[k] for k in z.files if k.startswith('s')}


def have_oof(d, name, seeds=SEEDS):
    p = Path(d) / _fname(name)
    if not p.exists():
        return False
    z = np.load(p)
    return all(f's{s}' in z.files and np.isfinite(z[f's{s}']).all() for s in seeds)


def load_all_oof(d):
    res = {}
    for p in sorted(Path(d).glob('r6-oof-*.npz')):
        z = np.load(p)
        name = p.stem[len('r6-oof-'):].replace('__', '+')
        oof = {int(k[1:]): z[k] for k in z.files if k.startswith('s')}
        if all(np.isfinite(a).all() for a in oof.values()):
            res[name] = oof
    return res


# ------------------------------------------------------------------ ridge
def ridge_sat(data, X, seeds=SEEDS, folds=range(5)):
    """Ridge trên một ma trận đặc trưng X [92.337, p] bằng đúng đường chia của R2."""
    base_n, yc = data['base_n'], data['yc']
    out = {s: np.full(base_n, np.nan) for s in seeds}
    alphas = {}
    for fold in folds:
        for seed in seeds:
            tr, va, te, _ = cm.pool_split(data, seed, fold)
            pred, a = cm.ridge_full(X, yc, tr, va, te)
            out[seed][te] = pred
            alphas[f's{seed}f{fold}'] = a
    return out, alphas


def ridge_aug(X, y, tr, va, te, extra):
    """Ridge với hàng phụ `extra` luôn ở phía train; α chọn bằng MSE trên `va` (chỉ ô bão hòa)."""
    from sklearn.linear_model import Ridge
    trx = np.concatenate([tr, extra])
    best = min((float(np.mean((Ridge(alpha=a).fit(X[trx], y[trx]).predict(X[va]) - y[va]) ** 2)), a)
               for a in ALPHAS)[1]
    full = np.concatenate([tr, va, extra])
    return Ridge(alpha=best).fit(X[full], y[full]).predict(X[te]), best


def ridge_scan(data, scan, mode, seeds=SEEDS, folds=range(5)):
    """mode 'pool': ridge trên bão hòa ∪ scanning, thêm cột chỉ báo nguồn;
    mode 'prior': ridge trên scanning (α chọn trên 20% cụm giữ lại), rồi ridge phần dư trên bão hòa."""
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import GroupShuffleSplit
    base_n, yc = data['base_n'], data['yc']
    n_sat = len(yc)
    Xs = data['Xc'][:, :180]
    sv, sc = r6.sat_view(data), r6.scan_view(scan)
    Xsc = r6.cell_features(sc['wt_int'], sc['pep_of_row'], sc['pos'], sc['aa'], 3)
    out = {s: np.full(base_n, np.nan) for s in seeds}
    alphas = {}
    if mode == 'pool':
        X = np.vstack([np.c_[Xs, np.zeros(n_sat)], np.c_[Xsc, np.ones(len(Xsc))]])
        y = np.concatenate([yc, scan['y']])
    for fold in folds:
        srows = r6.scan_train_rows(scan, set(data['fold_clusters'][fold]))
        assert not set(scan['rowg'][srows]) & set(data['fold_clusters'][fold])
        for seed in seeds:
            tr, va, te, _ = cm.pool_split(data, seed, fold)
            if mode == 'pool':
                pred, a = ridge_aug(X, y, tr, va, te, n_sat + srows)
            else:
                gi, hi = next(GroupShuffleSplit(1, test_size=.2, random_state=seed)
                              .split(srows, groups=scan['rowg'][srows]))
                a1 = min((float(np.mean((Ridge(alpha=a).fit(Xsc[srows[gi]], scan['y'][srows[gi]])
                                         .predict(Xsc[srows[hi]]) - scan['y'][srows[hi]]) ** 2)), a)
                         for a in ALPHAS)[1]
                f1 = Ridge(alpha=a1).fit(Xsc[srows], scan['y'][srows])
                resid = yc - f1.predict(Xs)
                g, a = cm.ridge_full(Xs, resid, tr, va, te)
                pred = g + f1.predict(Xs[te])
                alphas[f's{seed}f{fold}_stage1'] = a1
            out[seed][te] = pred
            alphas[f's{seed}f{fold}'] = a
    return out, alphas


# ------------------------------------------------------------------ cổng và kiểm chéo nguồn
def run_gates(data, scan, oof_m3, gates):
    """Cổng bắt buộc (PROTOCOL §7). Trả về thông tin mô tả."""
    st_ = data['st']
    gates.check('n_sat_cells', len(data['yc']), 92337, 0)
    sv = r6.sat_view(data)
    Xw = r6.cell_features(sv['wt_int'], sv['pep_of_row'], sv['pos'], sv['aa'], 3)
    gates.check('featurizer_equals_cache_maxabs', float(np.abs(Xw - data['Xc'][:, :180]).max()), 0.0, 1e-12)
    lc = json.loads(LC_RESULTS.read_text())['results']['ridge']['ext']
    summ = st.summarize_oof(oof_m3, data['y0'], data['idx0'])
    gates.check('M3_ensemble_vs_P0', summ['macro_auroc_ensemble'], lc['macro_auroc_ensemble'], 1e-4)
    for s, ref in zip(SEEDS, lc['macro_auroc_per_seed']):
        gates.check(f'M3_seed{s}_vs_P0', summ['macro_auroc_per_seed'][str(s)], ref, 2e-4)
    assert all(len(w) == r6.L for w in scan['wt_seq']) and all(len(m) == r6.L for m in scan['mut_seq'])
    leaks = []
    for fold in range(5):
        rows = r6.scan_train_rows(scan, set(data['fold_clusters'][fold]))
        leaks.append(len(set(scan['rowg'][rows]) & set(data['fold_clusters'][fold])))
    gates.check('scan_rows_in_test_clusters', sum(leaks), 0, 0)
    n_overlap = [len(set(scan['rowg'][scan['keep']]) & set(data['fold_clusters'][f])) for f in range(5)]
    n_excl = [int(len(scan['keep']) - len(r6.scan_train_rows(scan, set(data['fold_clusters'][f])))) for f in range(5)]
    return {'summary_M3': {k: summ[k] for k in ('macro_auroc_per_seed', 'macro_auroc_ensemble')},
            'scan_clusters_overlapping_test_per_fold': n_overlap, 'scan_cells_excluded_per_fold': n_excl,
            'scan_cells_total': int(len(scan['keep']))}


def cross_source_audit(data, scan):
    """MÔ TẢ (không phải tiêu chí): scanning vs bão hòa trên CÙNG ô (peptide, vị trí, acid amin thay)."""
    from scipy.stats import pearsonr, spearmanr
    s = data['st']
    names = s['peps'][s['pep_of_row']]
    sat_lab = {(n, int(p), a): float(y) for n, p, a, y in zip(names, s['pos'], s['aa'], s['y'])}
    sat_base = {(n, int(p), a) for n, p, a in zip(names[:data['base_n']], s['pos'][:data['base_n']],
                                                  s['aa'][:data['base_n']])}
    out = {}
    for tag, subset in (('all_shared_wt_le_4.0', None), ('base91_shared_wt_le_3.0', sat_base)):
        sc_n, st_n = [], []
        peps = set()
        for i in scan['keep']:
            k = (scan['peps'][scan['pep_of_row'][i]], int(scan['pos'][i]), scan['aa'][i])
            if k in sat_lab and (subset is None or k in subset):
                sc_n.append(scan['y'][i]); st_n.append(sat_lab[k]); peps.add(k[0])
        sc_n, st_n = np.array(sc_n), np.array(st_n)
        if len(sc_n) < 30:
            out[tag] = {'n_cells': int(len(sc_n))}
            continue
        ps, pt = sc_n >= 1.0, st_n >= 1.0
        po = float((ps == pt).mean())
        pe = ps.mean() * pt.mean() + (1 - ps.mean()) * (1 - pt.mean())
        out[tag] = {'n_peptides': len(peps), 'n_cells': int(len(sc_n)),
                    'pearson': float(pearsonr(sc_n, st_n)[0]), 'spearman': float(spearmanr(sc_n, st_n).statistic),
                    'ols_slope_sat_on_scan': float(np.polyfit(sc_n, st_n, 1)[0]),
                    'mean_dpsi_scan': float(sc_n.mean()), 'mean_dpsi_sat': float(st_n.mean()),
                    'positive_rate_scan': float(ps.mean()), 'positive_rate_sat': float(pt.mean()),
                    'binary_agreement': po, 'cohen_kappa': float((po - pe) / (1 - pe)),
                    'auroc_scan_dpsi_for_sat_positive': dr.auroc(list(sc_n), list(pt))}
    return out


# ------------------------------------------------------------------ mạng
def build_pack(rep, data, scan, dev, cache_dir, with_scan=False):
    """Gom tensor cho một biểu diễn. Hàng 0..N_sat-1 bão hòa, N_sat.. scanning (theo chỉ số dòng của bảng scanning)."""
    import r6esm
    import r6nn
    sv = r6.sat_view(data)
    wt_idx = r6.crop_wt_idx(sv['wt_int'], sv['pep_of_row'], sv['pos'])
    f60 = data['Xc'][:, :60]
    y = data['yc']
    src = None
    if with_scan:
        sc = r6.scan_view(scan)
        wt_idx = np.concatenate([wt_idx, r6.crop_wt_idx(sc['wt_int'], sc['pep_of_row'], sc['pos'])])
        f60 = np.vstack([f60, r6.cell_features(sc['wt_int'], sc['pep_of_row'], sc['pos'], sc['aa'], 3)[:, :60]])
        y = np.concatenate([y, scan['y']])
        src = np.concatenate([np.zeros(len(data['yc'])), np.ones(len(scan['y']))])
    crop = None
    if rep != 'onehot':
        files = [Path(cache_dir) / f'crop-{rep}-sat.npy']
        if with_scan:
            files.append(Path(cache_dir) / f'crop-{rep}-scan.npy')
        crop = r6esm.load_to_device(files, dev)
        assert crop.shape[0] == len(y), 'crop và nhãn lệch số hàng'
    return r6nn.Pack(dev, wt_idx, f60, y, crop=crop, src=src)


def run_nn(name, rep, ks, F, pack, data, scan, mode=None, seeds=SEEDS, folds=range(5), out_dir=None, log=print,
           subsample=None):
    """Huấn luyện/đánh giá một cấu hình trên 5 fold × seed; tiếp tục được nếu phiên bị ngắt.
    mode: None | 'scan_pool' | 'scan_ft'. `subsample`: dict chỉ dùng cho SMOKE (tr/va/te cố định)."""
    import r6nn
    from sklearn.model_selection import GroupShuffleSplit
    key = name if mode is None else f'{name}+{mode}'
    base_n, n_sat = data['base_n'], len(data['yc'])
    path = Path(out_dir) / _fname(key) if out_dir else None
    meta_path = Path(out_dir) / (_fname(key)[:-4] + '.meta.json') if out_dir else None
    oof = {s: np.full(base_n, np.nan) for s in seeds}
    done, meta = set(), []
    if path is not None and path.exists() and meta_path.exists():
        z = np.load(path)
        meta = json.loads(meta_path.read_text())
        done = {(m['seed'], m['fold']) for m in meta}
        for s in seeds:
            if f's{s}' in z.files:
                oof[s] = z[f's{s}'].copy()
        log(f'[{key}] tiếp tục: đã xong {sorted(done)}')
    spec = {'ks': ks, 'F': F, 'use_src': mode == 'scan_pool'}
    t0 = time.time()
    for seed in seeds:
        for fold in folds:
            if (seed, fold) in done:
                continue
            tr, va, te, _ = cm.pool_split(data, seed, fold)
            if subsample is not None:
                tr, va, te = subsample['tr'], subsample['va'], subsample['te']
            srows = None
            if mode is not None:
                srows = r6.scan_train_rows(scan, set(data['fold_clusters'][fold]))
                if subsample is not None:
                    srows = srows[:subsample.get('n_scan', 2000)]
            torch_seed = seed * 1000 + fold
            info = {}
            if mode is None:
                model, info = r6nn.fit(pack, tr, va, spec, torch_seed)
            elif mode == 'scan_pool':
                tr2 = np.concatenate([tr, n_sat + srows])
                model, info = r6nn.fit(pack, tr2, va, spec, torch_seed)
            else:                                                               # scan_ft
                gi, hi = next(GroupShuffleSplit(1, test_size=.2, random_state=seed)
                              .split(srows, groups=scan['rowg'][srows]))
                m1, i1 = r6nn.fit(pack, n_sat + srows[gi], n_sat + srows[hi], spec, torch_seed, **r6nn.PRE)
                model, info = r6nn.fit(pack, tr, va, spec, torch_seed,
                                       init_state={k: v.clone() for k, v in m1.state_dict().items()}, **r6nn.FT)
                info['pretrain'] = i1
            pred = r6nn.predict(model, pack, te)
            assert np.isfinite(pred).all()
            oof[seed][te] = pred
            meta.append({'seed': seed, 'fold': fold, 'n_train': int(len(tr)), **info})
            if path is not None:
                save_oof(out_dir, key, oof)
                meta_path.write_text(json.dumps(meta, indent=1) + '\n')
            log(f'[{key}] seed {seed} fold {fold}: epoch tốt nhất {info.get("best_epoch")}'
                f' · val MSE {info.get("best_val_mse", float("nan")):.4f} · {time.time() - t0:.0f}s')
    return oof, meta


# ------------------------------------------------------------------ tổng hợp
def build_contrasts(S, groups0):
    """Các phép so ghép cặp của PROTOCOL §5-§6. S: {tên cấu hình: summarize_oof}."""
    C = {}

    def add(name, a, b, m=1, family=''):
        if a in S and b in S:
            C[name] = {'a': a, 'b': b, 'family': family, **st.contrast(S[a], S[b], groups0, m=m)}
    add('P_esm35_mcnn_vs_ridge', 'esm35_mcnn', 'ridge_M3', 1, 'primary')
    add('S1_esm35_mcnn_vs_oh_mcnn', 'esm35_mcnn', 'oh_mcnn', 1, 'secondary')
    add('S2_oh_mcnn_vs_ridge', 'oh_mcnn', 'ridge_M3', 1, 'secondary')
    add('S3_oh_cnn1_vs_ridge', 'oh_cnn1', 'ridge_M3', 1, 'secondary')
    add('S4_esm35_cnn1_vs_ridge', 'esm35_cnn1', 'ridge_M3', 1, 'secondary')
    add('S5_oh_mcnn_vs_oh_cnn1', 'oh_mcnn', 'oh_cnn1', 1, 'secondary')
    add('S6_esm35_mcnn_vs_esm35_cnn1', 'esm35_mcnn', 'esm35_cnn1', 1, 'secondary')
    add('S7_esm35_mcnn_vs_ridge_W5', 'esm35_mcnn', 'ridge_W5', 1, 'secondary')           # thêm sau khi xem GĐ A (PROTOCOL §12)
    add('S8_oh_mcnn_vs_ridge_W5', 'oh_mcnn', 'ridge_W5', 1, 'secondary')
    for w in WIDTHS:
        add(f'A_ridge_W{w}_vs_W3', f'ridge_W{w}', 'ridge_M3', len(WIDTHS), 'A')
    for mode in ('pool', 'prior'):
        add(f'B_ridge_scan_{mode}_vs_ridge', f'ridge_scan_{mode}', 'ridge_M3', 2, 'B')
        add(f'Bd_ridge_scan_{mode}_t3_vs_ridge', f'ridge_scan_{mode}_t3', 'ridge_M3', 1, 'descriptive')
    for k in SIZES:
        add(f'D_ridge_{k}_vs_M3', f'ridge_{k}', 'ridge_M3', len(SIZES), 'D')
    for k in ('esm8', 'esm150', 'esm650'):
        add(f'F_{k}_mcnn_vs_esm35_mcnn', f'{k}_mcnn', 'esm35_mcnn', 3, 'F')
    for base in ('oh_mcnn', 'esm35_mcnn'):
        for mode in SCAN_MODES:
            add(f'G_{base}_{mode}_vs_scratch', f'{base}+{mode}', base, 4, 'G')
    return C


def aggregate(oof_all, data):
    """Từ mọi OOF đã có -> summaries + contrasts (đúng PROTOCOL §6)."""
    y0, idx0, groups0 = data['y0'], data['idx0'], data['groups0']
    S = {k: st.summarize_oof(v, y0, idx0) for k, v in oof_all.items()}
    C = build_contrasts(S, groups0)
    out = {'summaries': {k: {kk: vv for kk, vv in v.items() if kk != '_per_seed_pp'} for k, v in S.items()},
           'contrasts': C}
    return out


def print_table(agg, log=print):
    log(f'{"cấu hình":34s} {"AUROC":>7s}  {"Δ so đối chứng":>15s}  {"CI (95% / hiệu chỉnh)":>26s}  kết luận')
    for k, v in agg['summaries'].items():
        log(f'{k:34s} {v["macro_auroc_ensemble"]:7.4f}')
    for name, c in agg['contrasts'].items():
        ci = c['ci_adj']
        log(f'{name:40s} Δ={c["delta"]:+.4f} CI[{ci[0]:+.4f}, {ci[1]:+.4f}] m={c["m"]} -> {c["verdict"]}')


if __name__ == '__main__':                          # tổng hợp lại từ thư mục OOF đã tải về
    d = Path(sys.argv[1])
    data = r6.load_sat()
    agg = aggregate(load_all_oof(d), data)
    agg['runner_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print_table(agg)
    (HERE / 'results-reaggregated.json').write_text(json.dumps(agg, indent=2, ensure_ascii=False) + '\n')
