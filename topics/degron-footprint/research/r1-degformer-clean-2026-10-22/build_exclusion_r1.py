"""R1 — dựng mặt nạ loại hàng khỏi bảng huấn luyện Degformer (569.270 dòng), TỪNG outer fold.

Đây là bước CHUẨN BỊ DỮ LIỆU chạy cục bộ (không huấn luyện). Luật loại (hợp của ba luật, chốt ở PROTOCOL §3):
  E1  trùng khít: hàng có sequence = một ô đột biến hoặc WT của peptide outer-test của fold;
  E2  gần trùng: khoảng cách Hamming <= 8 (identity >= 20/28) tới một WT peptide outer-test của fold;
  E3  mức protein: hàng chứa một 12-mer của protein P (UniProt người đã ghim) mà
        (a) P thuộc cụm cov80 outer-test của fold, hoặc
        (b) P có hit MMseqs2 (id >= 0,30, e <= 1e-3, alnlen >= 50) vào một thành viên của cụm outer-test.
Các ngưỡng giống P3 (`pretrain-p3-2026-10-22/build_exclusion.py`), áp trên protein thay vì gene Voutsinos.

Đầu ra:
  data/processed/r1-row-exclusion.npz   (mặt nạ từng luật, từng fold; nhóm validation theo protein)
  research/r1-degformer-clean-2026-10-22/exclusion-summary.json   (đếm mỗi luật, mỗi fold)

Chạy từ gốc repo (mmseqs 2 luồng):
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/r1-degformer-clean-2026-10-22/build_exclusion_r1.py
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '2')
import csv
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.model_selection import GroupKFold

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
import residue_data as rd          # noqa: E402,F401
import run_curve as rc             # noqa: E402

RAW = TOPIC / 'data/raw'
PROC = TOPIC / 'data/processed'
TRAIN_CSV = RAW / 'degformer-isolated/training_data.csv'
SEQTAB = PROC / 'r12-seqtable.npz'
UNIPROT = RAW / 'human-reviewed-2026-10-12.fasta.gz'
FULL = PROC / 'proteins-full.fasta'
CLUSTERS = TOPIC / 'data/interim/protein-id30-cov80_cluster.tsv'
OUT = PROC / 'r1-row-exclusion.npz'
SUMMARY = HERE / 'exclusion-summary.json'

KMER = 12
HAMMING_MAX = 8
MIN_ID, MAX_E, MIN_ALN = 0.30, '1e-3', 50
MULT_CAP = 200                      # 12-mer xuất hiện ở > cap protein: bỏ qua (lặp/độ phức tạp thấp), báo số lượng
AA = 'ACDEFGHIKLMNPQRSTVWY'
LUT = np.full(256, -1, dtype=np.int64)
for i, a in enumerate(AA):
    LUT[ord(a)] = i


def read_fasta(path):
    op = gzip.open if str(path).endswith('.gz') else open
    out, acc, buf = {}, None, []
    with op(path, 'rt') as fh:
        for line in fh:
            if line.startswith('>'):
                if acc:
                    out[acc] = ''.join(buf)
                h = line[1:].strip()
                acc = h.split('|')[1] if '|' in h else h.split()[0]
                buf = []
            else:
                buf.append(line.strip())
        if acc:
            out[acc] = ''.join(buf)
    return out


def kmer_codes(seq_arr, k=KMER):
    """seq_arr: mảng int64 (0..19, -1 = không chuẩn). Trả về (mã 12-mer, hợp lệ) của mọi cửa sổ."""
    n = len(seq_arr) - k + 1
    if n <= 0:
        return np.zeros(0, dtype=np.int64), np.zeros(0, dtype=bool)
    code = np.zeros(n, dtype=np.int64)
    ok = np.ones(n, dtype=bool)
    for j in range(k):
        s = seq_arr[j:j + n]
        ok &= s >= 0
        code |= (np.where(s >= 0, s, 0) << (5 * j))
    return code, ok


def encode(seq):
    return LUT[np.frombuffer(seq.encode('ascii'), dtype=np.uint8)]


def main():
    # ---------- phép chia outer: tái lập đúng folds của G2 ----------
    peps0, X0, y0, idx0, rowg0, groups0, _ = rc.build(rd.DEGRON_PSI_MAX, 'base')
    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]
    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    assert fold_clusters == [f['test_clusters'] for f in g2['folds']], 'folds không trùng G2'
    st = np.load(SEQTAB)
    base_n = int(st['base_n'])
    assert np.array_equal(st['y'][:base_n], y0)
    mut_seq = st['mut_seq'][:base_n]
    wt_seq_cell = st['wt_seq'][st['pep_of_row'][:base_n]]
    pep_cluster = np.asarray(st['groups'])[:len(peps0)]
    print(f'cổng: 5 fold trùng G2 · bảng trình tự {base_n} ô gốc', flush=True)

    # ---------- bảng huấn luyện ----------
    seqs = []
    with TRAIN_CSV.open() as fh:
        r = csv.reader(fh)
        next(r)
        for row in r:
            seqs.append(row[0])
    N = len(seqs)
    assert N == 569270, N
    train_sha = hashlib.sha256(TRAIN_CSV.read_bytes()).hexdigest()
    A = np.frombuffer(''.join(seqs).replace('*', '#').encode('ascii'), dtype=np.uint8).reshape(N, 28)
    print(f'{N} dòng huấn luyện · sha256 {train_sha[:16]}…', flush=True)

    # ---------- E1/E2 theo fold ----------
    E1 = np.zeros((5, N), dtype=bool)
    E2 = np.zeros((5, N), dtype=bool)
    seq_index = defaultdict(list)
    for i, s in enumerate(seqs):
        seq_index[s].append(i)
    for f, (_, te) in enumerate(folds):
        test_cells = set(mut_seq[te].tolist()) | set(wt_seq_cell[te].tolist())
        for s in test_cells:
            for i in seq_index.get(s, ()):
                E1[f, i] = True
        wts = sorted(set(wt_seq_cell[te].tolist()))
        W = np.frombuffer(''.join(wts).encode('ascii'), dtype=np.uint8).reshape(len(wts), 28)
        for w in W:                               # Hamming <= 8 tới từng WT test
            E2[f] |= (A != w[None, :]).sum(1) <= HAMMING_MAX
        print(f'fold {f}: {len(wts)} WT test · E1 {int(E1[f].sum())} · E2 {int(E2[f].sum())}', flush=True)

    # ---------- E3: ánh xạ hàng -> protein bằng 12-mer ----------
    U = read_fasta(UNIPROT)
    full = read_fasta(FULL)
    for a, s in full.items():
        U.setdefault(a, s)
    accs = sorted(U)
    print(f'vũ trụ protein: {len(accs)}', flush=True)
    kc, kp = [], []
    for pi, a in enumerate(accs):
        c, ok = kmer_codes(encode(U[a]))
        kc.append(c[ok])
        kp.append(np.full(int(ok.sum()), pi, dtype=np.int32))
    kc = np.concatenate(kc)
    kp = np.concatenate(kp)
    order = np.argsort(kc, kind='stable')
    kc, kp = kc[order], kp[order]
    print(f'chỉ mục 12-mer: {len(kc)} mục', flush=True)

    rows_enc = np.where(A == ord('#'), -1, LUT[A])
    pair_r, pair_p = [], []
    n_capped = 0
    for s in range(28 - KMER + 1):
        code = np.zeros(N, dtype=np.int64)
        ok = np.ones(N, dtype=bool)
        for j in range(KMER):
            col = rows_enc[:, s + j]
            ok &= col >= 0
            code |= (np.where(col >= 0, col, 0) << (5 * j))
        lo = np.searchsorted(kc, code, 'left')
        hi = np.searchsorted(kc, code, 'right')
        cnt = np.where(ok, hi - lo, 0)
        capped = cnt > MULT_CAP
        n_capped += int(capped.sum())
        cnt = np.where(capped, 0, cnt)
        sel = np.nonzero(cnt)[0]
        if len(sel):
            rep = np.repeat(sel, cnt[sel])
            offs = np.arange(cnt[sel].sum()) - np.repeat(np.cumsum(cnt[sel]) - cnt[sel], cnt[sel])
            pair_r.append(rep.astype(np.int32))
            pair_p.append(kp[np.repeat(lo[sel], cnt[sel]) + offs])
    pr = np.concatenate(pair_r)
    pp = np.concatenate(pair_p)
    key = np.unique(pr.astype(np.int64) * len(accs) + pp)
    pr, pp = (key // len(accs)).astype(np.int32), (key % len(accs)).astype(np.int32)
    mapped = np.zeros(N, dtype=bool)
    mapped[pr] = True
    print(f'ánh xạ 12-mer: {int(mapped.sum())}/{N} dòng ({mapped.mean():.3%}) · cặp (dòng, protein) {len(pr)} '
          f'· 12-mer bỏ vì lặp > {MULT_CAP}: {n_capped}', flush=True)

    # nhóm validation theo protein: protein nhỏ nhất ánh xạ được; dòng không ánh xạ -> nhóm riêng
    first_p = np.full(N, np.iinfo(np.int64).max, dtype=np.int64)
    np.minimum.at(first_p, pr, pp)
    group = np.where(mapped, first_p, -1 - np.arange(N)).astype(np.int64)

    # ---------- cụm outer-test -> protein thành viên ----------
    rep_of = {}
    with CLUSTERS.open() as fh:
        for line in fh:
            rep, mem = line.rstrip('\n').split('\t')[:2]
            rep_of[mem] = rep
    acc_index = {a: i for i, a in enumerate(accs)}
    members = defaultdict(set)
    for m, rep in rep_of.items():
        members[rep].add(m)
    test_members_all = {}
    for cl in sorted(set().union(*map(set, fold_clusters))):
        for m in members[cl]:
            if m in U:
                test_members_all[m] = cl

    # ---------- MMseqs2: protein có dòng ánh xạ vs thành viên cụm test ----------
    mm = shutil.which('mmseqs')
    assert mm, 'không thấy mmseqs'
    query_accs = sorted({accs[i] for i in set(pp.tolist())})
    hits = defaultdict(set)                      # query acc -> {target acc}
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / 'q.fa').write_text(''.join(f'>{a}\n{U[a]}\n' for a in query_accs))
        (td / 't.fa').write_text(''.join(f'>{a}\n{U[a]}\n' for a in sorted(test_members_all)))
        subprocess.run([mm, 'easy-search', str(td / 'q.fa'), str(td / 't.fa'), str(td / 'o.tsv'),
                        str(td / 'tmp'), '--min-seq-id', str(MIN_ID), '-e', MAX_E, '--threads', '2',
                        '-s', '7.5', '--format-output', 'query,target,fident,alnlen,evalue'],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for line in (td / 'o.tsv').read_text().splitlines():
            q, t, fid, aln, ev = line.split('\t')
            if float(fid) >= MIN_ID and int(aln) >= MIN_ALN:
                hits[q].add(t)
    print(f'MMseqs2: {len(query_accs)} protein truy vấn · {len(hits)} có hit vào cụm test', flush=True)

    E3 = np.zeros((5, N), dtype=bool)
    E3a = np.zeros((5, N), dtype=bool)
    n_prot_excl = []
    for f in range(5):
        tcl = set(fold_clusters[f])
        t_f = {a for a, cl in test_members_all.items() if cl in tcl}
        direct = {a for a in t_f}
        viahit = {q for q, ts in hits.items() if ts & t_f}
        bad_a = np.zeros(len(accs), dtype=bool)
        for a in direct:
            bad_a[acc_index[a]] = True
        bad_all = bad_a.copy()
        for a in viahit:
            bad_all[acc_index[a]] = True
        E3a[f, pr[bad_a[pp]]] = True
        E3[f, pr[bad_all[pp]]] = True
        n_prot_excl.append({'fold': f, 'n_test_member_proteins': len(t_f), 'n_by_hit': len(viahit - direct),
                            'n_excluded_proteins': int(bad_all.sum())})
        print(f'fold {f}: protein loại {int(bad_all.sum())} ({len(t_f)} thành viên cụm + '
              f'{len(viahit - direct)} qua hit) · E3 {int(E3[f].sum())} dòng', flush=True)

    excl = E1 | E2 | E3
    # ---------- kiểm sau cùng ----------
    for f, (_, te) in enumerate(folds):
        keep = ~excl[f]
        test_seqs = set(mut_seq[te].tolist()) | set(wt_seq_cell[te].tolist())
        left = {seqs[i] for i in np.nonzero(keep)[0]}
        assert not (left & test_seqs), f'fold {f}: còn sequence test trong tập huấn luyện'
    summary = {
        'rules': {'E1': 'sequence trùng khít ô test hoặc WT test', 'E2': f'Hamming <= {HAMMING_MAX} tới WT test',
                  'E3': f'12-mer của protein thuộc cụm test hoặc có hit MMseqs2 (id>={MIN_ID}, e<={MAX_E}, aln>={MIN_ALN})'},
        'kmer': KMER, 'multiplicity_cap': MULT_CAP, 'n_kmer_windows_skipped_by_cap': n_capped,
        'n_train_rows': N, 'train_csv_sha256': train_sha,
        'n_rows_mapped_to_protein': int(mapped.sum()), 'fraction_mapped': float(mapped.mean()),
        'n_universe_proteins': len(accs), 'n_query_proteins_mmseqs': len(query_accs),
        'per_fold': [{'fold': f, 'n_test_cells': int(len(folds[f][1])),
                      'n_test_clusters': len(fold_clusters[f]),
                      'E1': int(E1[f].sum()), 'E2': int(E2[f].sum()), 'E3': int(E3[f].sum()),
                      'E3_direct_cluster_only': int(E3a[f].sum()),
                      'excluded_union': int(excl[f].sum()), 'remaining': int((~excl[f]).sum()),
                      'excluded_fraction': float(excl[f].mean()), **n_prot_excl[f]} for f in range(5)],
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limitation': 'Hàng không ánh xạ được vào UniProt người đã ghim chỉ bị loại bởi E1/E2; '
                      'paralog nằm ngoài vũ trụ protein sẽ không bị phát hiện.',
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
    np.savez_compressed(OUT, excl=excl, E1=E1, E2=E2, E3=E3, group=group,
                        train_sha256=np.asarray(train_sha), n_rows=np.asarray(N))
    print(f'-> {OUT}\n-> {SUMMARY}')
    for pf in summary['per_fold']:
        print(f"  fold {pf['fold']}: loại {pf['excluded_union']} ({pf['excluded_fraction']:.2%}), còn {pf['remaining']}")


if __name__ == '__main__':
    main()
