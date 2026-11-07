"""R1 — Degformer sạch cụm: huấn luyện lại kiến trúc đã công bố trên bảng 569.270 dòng SAU KHI loại các hàng
chạm cụm outer-test (từng fold), rồi chấm ΔPSI = pred(mutant) − pred(WT) trên đúng 47.847 ô outer-test của G2.

Tiêu chí và độ lệch so với script tác giả chốt ở PROTOCOL.md. Notebook chỉ gọi `run()`; logic nằm ở đây.
Chạy trên GPU (Kaggle/Colab); kiểm cục bộ chỉ bằng `selftest_r1.py` (vài bước trên dữ liệu giả).
"""
import ast
import csv
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
sys.path.insert(0, str(TOPIC / 'research/notebook-kit-2026-10-22'))

RAWD = TOPIC / 'data/raw/degformer-isolated'
PROC = TOPIC / 'data/processed'
TRAIN_CSV = RAWD / 'training_data.csv'
EXCL = PROC / 'r1-row-exclusion.npz'
SEQTAB = PROC / 'r12-seqtable.npz'
G2_DIR = TOPIC / 'research/g2-saturation-2026-10-18'
VOCAB = 'ACDEFGHIKLMNPQRSTVWY*'
EXPECTED_PARAMS = 545025            # PROTOCOL §4: đếm trên PeptideTransformer(21) của predict.py
SEEDS_ALL = (17, 29, 43)

# cấu hình huấn luyện: hằng số lấy từ train_v2.py (đọc bằng AST); phần còn lại chốt ở PROTOCOL §5
CFG = {'val_frac': 0.10, 'patience_stop': 10, 'plateau_factor': 0.5, 'plateau_patience': 2,
       'eval_batch': 4096}


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def published_constants():
    tree = ast.parse((RAWD / 'train_v2.py').read_text())
    want = {'MAX_LEN', 'BATCH_SIZE', 'EPOCHS', 'LR'}
    out = {}
    for n in tree.body:
        if (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
                and n.targets[0].id in want):
            out[n.targets[0].id] = ast.literal_eval(n.value)
    assert set(out) == want, out
    return out


def degformer_class():
    """Dựng PeptideTransformer từ AST của predict.py (SHA kiểm theo manifest G2); không import mã tải về."""
    import torch
    from torch import nn
    m = json.loads((G2_DIR / 'source-manifest.json').read_text())['files']
    for f in ('predict.py', 'train_v2.py', 'training_data.csv'):
        assert sha256_file(RAWD / f) == m[f]['sha256'], f'SHA lệch: {f}'
    node = next(n for n in ast.parse((RAWD / 'predict.py').read_text()).body
                if isinstance(n, ast.ClassDef) and n.name == 'PeptideTransformer')
    node2 = next(n for n in ast.parse((RAWD / 'train_v2.py').read_text()).body
                 if isinstance(n, ast.ClassDef) and n.name == 'PeptideTransformer')
    assert ast.dump(node) == ast.dump(node2), 'class trong predict.py khác train_v2.py'
    ns = {'torch': torch, 'nn': nn, 'MAX_LEN': 28}
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'reviewed-degformer-class', 'exec'), ns)
    return ns['PeptideTransformer']


def encode_seqs(seqs):
    lut = np.full(256, 255, dtype=np.uint8)
    for i, a in enumerate(VOCAB):
        lut[ord(a)] = i
    arr = np.frombuffer(''.join(seqs).encode('ascii'), dtype=np.uint8).reshape(len(seqs), 28)
    out = lut[arr]
    assert not (out == 255).any(), 'ký tự ngoài từ vựng'
    return out


def load_inputs():
    """Trả về dict: bảng huấn luyện, mặt nạ loại, nhóm validation, ô outer-test, folds (đã kiểm trùng G2)."""
    import residue_data as rd
    import run_curve as rc
    from nbkit import StableGroupKFold as GroupKFold   # cùng fold với G2 trên mọi bản sklearn
    with TRAIN_CSV.open() as fh:
        r = csv.reader(fh)
        next(r)
        rows = [(a, float(b)) for a, b in r]
    seqs = [a for a, _ in rows]
    y = np.array([b for _, b in rows], dtype=np.float64)
    ex = np.load(EXCL)
    assert str(ex['train_sha256']) == sha256_file(TRAIN_CSV), 'mặt nạ loại dựng cho bảng huấn luyện khác'
    assert int(ex['n_rows']) == len(seqs)
    st = np.load(SEQTAB)
    base_n = int(st['base_n'])
    peps0, X0, y0, idx0, rowg0, groups0, _ = rc.build(rd.DEGRON_PSI_MAX, 'base')
    assert np.array_equal(st['y'][:base_n], y0), 'bảng trình tự lệch nhãn bộ gốc'
    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    g2 = json.loads((G2_DIR / 'results.json').read_text())
    assert [sorted(set(rowg0[te])) for _, te in folds] == [f['test_clusters'] for f in g2['folds']], \
        'folds không trùng G2'
    mut = st['mut_seq'][:base_n]
    wt = st['wt_seq'][st['pep_of_row'][:base_n]]
    return {'seqs': seqs, 'enc': encode_seqs(seqs), 'y': y, 'excl': ex['excl'], 'group': ex['group'],
            'mut_u8': encode_seqs(mut.tolist()), 'wt_u8': encode_seqs(wt.tolist()),
            'folds_te': [te for _, te in folds], 'y0': y0, 'idx0': np.asarray(idx0), 'peps0': list(peps0),
            'groups0': np.asarray(groups0), 'base_n': base_n,
            'test_seqs': [set(mut[te].tolist()) | set(wt[te].tolist()) for _, te in folds]}


def check_no_test_leak(inp):
    """Cổng: sau khi loại, không còn sequence nào của ô/WT outer-test trong tập huấn luyện của fold."""
    out = []
    for f in range(5):
        left = {inp['seqs'][i] for i in np.nonzero(~inp['excl'][f])[0]}
        n = len(left & inp['test_seqs'][f])
        assert n == 0, f'fold {f}: còn {n} sequence test trong tập huấn luyện'
        out.append({'fold': f, 'remaining_rows': int((~inp['excl'][f]).sum()),
                    'excluded_rows': int(inp['excl'][f].sum())})
    return out


def _predict(net, u8, dev, bs, torch):
    out = []
    net.eval()
    with torch.no_grad():
        for i in range(0, len(u8), bs):
            x = torch.from_numpy(u8[i:i + bs]).to(dev).long()
            out.append(net(x).float().cpu().numpy())
    return np.concatenate(out)


def train_fold(Net, enc, y, keep_idx, group, test_mut, test_wt, seed, fold, dev, consts,
               max_epochs=None, log=print):
    """Huấn luyện một (seed, fold). Trả (điểm ô test, bản ghi)."""
    import torch
    from sklearn.model_selection import GroupShuffleSplit
    use_amp = dev == 'cuda'
    max_epochs = max_epochs or consts['EPOCHS']
    ti, vi = next(GroupShuffleSplit(n_splits=1, test_size=CFG['val_frac'], random_state=seed)
                  .split(keep_idx, groups=group[keep_idx]))
    tr, va = keep_idx[ti], keep_idx[vi]
    assert not (set(group[tr]) & set(group[va])), 'validation chia theo nhóm bị rò'
    mu, sd = float(y[tr].mean()), float(y[tr].std())
    Xtr = torch.from_numpy(enc[tr]).to(dev)
    Ytr = torch.from_numpy(((y[tr] - mu) / sd).astype(np.float32)).to(dev)
    Xva = torch.from_numpy(enc[va]).to(dev)
    Yva = torch.from_numpy(((y[va] - mu) / sd).astype(np.float32)).to(dev)
    torch.manual_seed(seed * 1000 + fold)
    net = Net(len(VOCAB)).to(dev)
    assert sum(p.numel() for p in net.parameters()) == EXPECTED_PARAMS
    opt = torch.optim.Adam(net.parameters(), lr=consts['LR'])
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, mode='min', factor=CFG['plateau_factor'],
                                                       patience=CFG['plateau_patience'])
    scaler = torch.amp.GradScaler('cuda', enabled=use_amp)
    gen = torch.Generator()
    gen.manual_seed(seed * 1000 + fold)
    bs = consts['BATCH_SIZE']
    best, best_ep, state, curve = 1e99, 0, None, []
    for epoch in range(1, max_epochs + 1):
        t0 = time.time()
        net.train()
        perm = torch.randperm(len(tr), generator=gen).to(dev)
        tot = torch.zeros((), device=dev)
        for i in range(0, len(tr), bs):
            b = perm[i:i + bs]
            with torch.autocast(device_type='cuda', enabled=use_amp):
                p = net(Xtr[b].long())
            loss = torch.nn.functional.mse_loss(p.float(), Ytr[b])
            opt.zero_grad(set_to_none=True)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
            tot += loss.detach() * len(b)
        net.eval()
        vs = 0.0
        with torch.no_grad(), torch.autocast(device_type='cuda', enabled=use_amp):
            for i in range(0, len(va), CFG['eval_batch']):
                vs += float(torch.nn.functional.mse_loss(net(Xva[i:i + CFG['eval_batch']].long()).float(),
                                                         Yva[i:i + CFG['eval_batch']], reduction='sum'))
        vloss = vs / len(va)
        sched.step(vloss)
        rec = {'epoch': epoch, 'train_mse': float(tot) / len(tr), 'val_mse': vloss,
               'lr': opt.param_groups[0]['lr'], 'seconds': round(time.time() - t0, 1)}
        curve.append(rec)
        log(f'  seed {seed} fold {fold} epoch {epoch:2d} train {rec["train_mse"]:.4f} '
            f'val {vloss:.4f} lr {rec["lr"]:.1e} {rec["seconds"]}s')
        if vloss < best - 1e-6:
            best, best_ep = vloss, epoch
            state = {k: v.detach().clone() for k, v in net.state_dict().items()}
        if epoch - best_ep >= CFG['patience_stop']:
            break
    net.load_state_dict(state)
    pm = _predict(net, test_mut, dev, CFG['eval_batch'], torch)
    pw = _predict(net, test_wt, dev, CFG['eval_batch'], torch)
    score = (pm - pw) * sd
    rec = {'seed': seed, 'fold': fold, 'n_train': int(len(tr)), 'n_val': int(len(va)),
           'train_target_mean': mu, 'train_target_sd': sd, 'best_epoch': best_ep, 'best_val_mse': best,
           'stopped_at_epoch': len(curve), 'hit_epoch_cap': len(curve) == max_epochs and best_ep >= max_epochs - 1,
           'curve': curve}
    return score, rec, state


def benchmark(Net, enc, dev, consts, steps=40):
    """Đo thời gian 1 bước (batch đủ cỡ) để ước lượng giờ GPU trước khi chạy thật."""
    import torch
    net = Net(len(VOCAB)).to(dev)
    opt = torch.optim.Adam(net.parameters(), lr=consts['LR'])
    use_amp = dev == 'cuda'
    scaler = torch.amp.GradScaler('cuda', enabled=use_amp)
    bs = consts['BATCH_SIZE']
    x = torch.from_numpy(enc[:bs]).to(dev).long()
    yb = torch.randn(bs, device=dev)
    for k in range(steps + 5):
        if k == 5:
            if dev == 'cuda':
                torch.cuda.synchronize()
            t0 = time.time()
        with torch.autocast(device_type='cuda', enabled=use_amp):
            p = net(x)
        loss = torch.nn.functional.mse_loss(p.float(), yb)
        opt.zero_grad(set_to_none=True)
        scaler.scale(loss).backward()
        scaler.step(opt)
        scaler.update()
    if dev == 'cuda':
        torch.cuda.synchronize()
    return (time.time() - t0) / steps


def run(ctx, seeds=SEEDS_ALL, folds=range(5), smoke=False, log=print):
    """Chạy R1. ctx: nbkit.Context. Ghi r1-preds-seed*.npz và r1-train-log-seed*.json vào ctx.out."""
    import torch
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    consts = published_constants()
    log('hằng số công bố (train_v2.py):', consts, '· thiết bị:', dev)
    Net = degformer_class()
    inp = load_inputs()
    leak = check_no_test_leak(inp)
    ctx.gates.check('param_count', sum(p.numel() for p in Net(len(VOCAB)).parameters()), EXPECTED_PARAMS, 0)
    ctx.save('r1-exclusion-check.json', leak)
    lc = json.loads((TOPIC / 'research/learning-curve-2026-10-22/results.json').read_text())
    ref = [x for x in lc['results']['ridge']['ext']['per_peptide'] if x is not None]
    ctx.gates.check('ridge_ext_reference_macro', float(np.mean(ref)), 0.8208223589063638, 1e-9)

    n_tr_est = int(0.9 * inp['excl'].shape[1] * 0.93)
    step_s = benchmark(Net, inp['enc'], dev, consts)
    ep_s = step_s * (n_tr_est / consts['BATCH_SIZE'])
    log(f'benchmark: {step_s*1000:.1f} ms/bước → ~{ep_s:.0f} s/epoch → tối đa '
        f'{ep_s*consts["EPOCHS"]/60:.0f} phút/fold, {ep_s*consts["EPOCHS"]*5*len(seeds)/3600:.1f} giờ cho '
        f'{len(seeds)} seed (cận trên: không dừng sớm; chưa tính đánh giá validation)')
    ctx.save('r1-benchmark.json', {'device': dev, 'ms_per_step': step_s * 1000, 'est_epoch_seconds': ep_s,
                                   'seeds': list(seeds)})

    work = ctx.out.parent / 'r1-work'
    work.mkdir(exist_ok=True)
    max_epochs = 1 if smoke else None
    for seed in seeds:
        done_p = work / f'pred-seed{seed}.npz'
        scores = np.full(inp['base_n'], np.nan)
        done = np.zeros(5, dtype=bool)
        logs = []
        if done_p.exists():
            z = np.load(done_p)
            scores, done = z['scores'], z['done']
            logs = json.loads((work / f'log-seed{seed}.json').read_text())
            log(f'seed {seed}: nạp lại tiến độ, fold xong: {np.nonzero(done)[0].tolist()}')
        for f in folds:
            if done[f]:
                continue
            keep = np.nonzero(~inp['excl'][f])[0]
            if smoke:
                keep = keep[:20000]
            te = inp['folds_te'][f]
            if smoke:
                te = te[:512]
            sc, rec, state = train_fold(Net, inp['enc'], inp['y'], keep, inp['group'],
                                        inp['mut_u8'][te], inp['wt_u8'][te], seed, f, dev, consts,
                                        max_epochs=max_epochs, log=log)
            scores[te] = sc
            done[f] = True
            rec['excluded_rows'] = int(inp['excl'][f].sum())
            logs.append(rec)
            torch.save({'state_dict': state, 'seed': seed, 'fold': f}, work / f'ckpt-seed{seed}-fold{f}.pt')
            np.savez_compressed(done_p, scores=scores, done=done)
            (work / f'log-seed{seed}.json').write_text(json.dumps(logs))
            ctx.save(f'r1-train-log-seed{seed}.json', logs)
            np.savez_compressed(ctx.out / f'r1-preds-seed{seed}.npz', scores=scores, done=done,
                                smoke=np.asarray(bool(smoke)))
            ctx.finalize()                       # zip từng phần: tải về được dù phiên bị ngắt
            log(f'✔ seed {seed} fold {f}: epoch tốt nhất {rec["best_epoch"]}, val_mse {rec["best_val_mse"]:.4f}')
    return inp
