"""nbkit — thư viện dùng chung cho MỌI notebook huấn luyện của đề tài (Kaggle / Colab / local).

Chỉ stdlib + numpy (numpy nạp lười). Notebook là lớp mỏng; logic thí nghiệm nằm ở file .py trong
`research/<thí-nghiệm>/` và được gọi bằng `import` (không sao chép vào notebook).

Cách dùng điển hình (ô 0 của notebook):

    import sys, glob                       # tìm nbkit.py trong gói mã đã gắn vào notebook
    sys.path.insert(0, next(iter(glob.glob('/kaggle/input/*/topics/degron-footprint/research/notebook-kit-2026-10-22'))))
    import nbkit
    ctx = nbkit.setup('R0', protocol='research/r0-reproduce-notebook-2026-10-22/PROTOCOL.md',
                      protocol_sha256='<chốt bằng stamp_protocol.py>', needs=['R0'])

API ổn định (A2 và mọi notebook phụ thuộc, KHÔNG đổi chữ ký):

    detect_platform() -> 'kaggle' | 'colab' | 'local'
    find_packages(platform=None, search=None) -> {'code': Path|None, 'data': Path|None}
    compose_workspace(code_pkg, data_pkg, ws=None) -> Path          # cây thư mục giống repo
    verify_manifest(ws, experiment=None, deep=True) -> dict         # SHA-256 từng file cần
    set_seeds(seed, deterministic=True)
    env_report(ws=None) -> dict
    check_protocol(ws, rel_path, expected_sha256) -> str            # SHA thật; dừng nếu lệch
    write_results(ctx_or_dir, name, obj) -> Path
    class Gates: .check(name, observed, expected, tol) / .assert_all() / .to_dict()
    setup(experiment, protocol=None, protocol_sha256=None, needs=None, threads=2, seeds=None,
          require_gpu=False, pip=None) -> Context
    Context: .ws .topic .research .out .platform .env .gates .path(rel) .save(name,obj) .finalize(files)

Quy ước đường dẫn: gói mã và gói dữ liệu cùng dùng đường dẫn tương đối từ gốc repo, nên ghép lại
được cây thư mục có `CLAUDE.md` và `topics/degron-footprint/data/README.md` — hai marker mà
script nghiên cứu dùng để tìm `ROOT` và `TOPIC`.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.metadata as _md
import json
import os
import platform as _platform
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

__all__ = ['detect_platform', 'find_packages', 'compose_workspace', 'verify_manifest', 'set_seeds',
           'env_report', 'check_protocol', 'write_results', 'Gates', 'GateFailure', 'setup',
           'Context', 'StableGroupKFold', 'sha256_file', 'pip_install', 'TOPIC_REL', 'CODE_MARK', 'DATA_MARK']

TOPIC_REL = 'topics/degron-footprint'
CODE_MARK = 'CODE_MANIFEST.json'
DATA_MARK = 'DATA_MANIFEST.json'
WS_DEFAULT = {'kaggle': '/tmp/degron-ws', 'colab': '/content/degron-ws', 'local': None}
OUT_DEFAULT = {'kaggle': '/kaggle/working/out', 'colab': '/content/out', 'local': None}
DENY = ('koren', 'metadegron', 'larsen', 'clinvar')       # không bao giờ được nằm trong gói


class GateFailure(AssertionError):
    """Một cổng tự kiểm thất bại — dừng notebook, không chạy tiếp (theo PROTOCOL)."""


# ------------------------------------------------------------------ tiện ích
def sha256_file(path, chunk=1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(chunk), b''):
            h.update(b)
    return h.hexdigest()


def pip_install(*pkgs, quiet=True):
    """Cài thêm gói (cần bật Internet trên Kaggle). Trả về True nếu thành công."""
    cmd = [sys.executable, '-m', 'pip', 'install'] + (['-q'] if quiet else []) + list(pkgs)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print('pip install thất bại (Internet đã bật chưa?):\n', r.stderr[-800:])
    return r.returncode == 0


def detect_platform() -> str:
    if os.path.exists('/kaggle/input') or 'KAGGLE_KERNEL_RUN_TYPE' in os.environ:
        return 'kaggle'
    if 'COLAB_RELEASE_TAG' in os.environ or os.path.exists('/content') and 'google.colab' in sys.modules:
        return 'colab'
    return 'local'


# ------------------------------------------------------------------ tìm gói
def _walk(root, depth):
    root = Path(root)
    if not root.exists():
        return
    stack = [(root, 0)]
    while stack:
        d, k = stack.pop()
        try:
            entries = sorted(d.iterdir())
        except OSError:
            continue
        for e in entries:
            yield e
            if e.is_dir() and k < depth:
                stack.append((e, k + 1))


def find_packages(platform=None, search=None):
    """Tìm gói mã / gói dữ liệu. Mỗi gói có thể là THƯ MỤC đã giải nén (Kaggle tự giải nén zip
    khi tạo dataset) hoặc file .zip (Colab, local). Trả về Path hoặc None.

    search: danh sách thư mục thay cho mặc định (dùng khi kiểm thử).
    """
    platform = platform or detect_platform()
    if search is None and os.environ.get('DEGRON_PACKAGES'):
        search = [os.environ['DEGRON_PACKAGES']]       # ghi đè khi chạy local / kiểm thử
    if search is None:
        search = {'kaggle': ['/kaggle/input'],
                  'colab': ['/content', '/content/drive/MyDrive'],
                  'local': [str(Path(__file__).resolve().parents[2] / 'data/processed/packages')]}[platform]
    found = {'code': None, 'data': None}
    for root in search:
        for e in _walk(root, 4):
            if e.is_dir() and (e / CODE_MARK).exists() and not found['code']:
                found['code'] = e
            elif e.is_dir() and (e / DATA_MARK).exists() and not found['data']:
                found['data'] = e
            elif e.is_file() and e.suffix == '.zip':
                n = e.name.lower()
                if n.startswith('degron-code') and not found['code']:
                    found['code'] = e
                elif n.startswith('degron-data') and not found['data']:
                    found['data'] = e
    return found


def _extract(pkg: Path, dest: Path):
    if pkg.is_dir():
        shutil.copytree(pkg, dest, dirs_exist_ok=True)
    else:
        with zipfile.ZipFile(pkg) as z:
            for n in z.namelist():                      # gói là dữ liệu không tin cậy
                p = Path(n)
                if p.is_absolute() or '..' in p.parts:
                    raise ValueError(f'đường dẫn nguy hiểm trong zip: {n}')
                low = n.lower()
                if any(w in low for w in DENY):
                    raise ValueError(f'gói chứa nguồn bị cấm ({n}) — dừng')
            z.extractall(dest)


def compose_workspace(code_pkg, data_pkg, ws=None) -> Path:
    """Ghép gói mã + gói dữ liệu vào một cây thư mục GHI ĐƯỢC giống repo (idempotent)."""
    ws = Path(ws or WS_DEFAULT.get(detect_platform()) or Path.cwd() / 'degron-ws')
    stamp = ws / '.composed.json'
    def _sig(p):
        p = Path(p) if p else None
        if p is None or not p.exists():
            return None
        st = p.stat()
        return [str(p), st.st_size, st.st_mtime_ns if p.is_file() else 0]
    key = {'code': _sig(code_pkg), 'data': _sig(data_pkg)}
    if stamp.exists() and json.loads(stamp.read_text()) == key:
        return ws
    if ws.exists():
        shutil.rmtree(ws)
    ws.mkdir(parents=True)
    for pkg in (code_pkg, data_pkg):
        if pkg is None:
            raise FileNotFoundError('thiếu gói mã hoặc gói dữ liệu — xem RUN.md bước 2')
        _extract(Path(pkg), ws)
    for need in ('CLAUDE.md', f'{TOPIC_REL}/data/README.md'):
        if not (ws / need).exists():
            raise FileNotFoundError(f'cây thư mục thiếu marker {need}')
    stamp.write_text(json.dumps(key))
    return ws


class StableGroupKFold:
    """GroupKFold không phụ thuộc phiên bản scikit-learn (chỉ cần numpy).

    Mốc của đề tài (G2, learning-curve, R0-R3) chia fold bằng sklearn 1.9.1, nơi `GroupKFold` xếp cụm theo
    kích thước bằng `np.argsort(..., kind='stable')`. Bản sklearn cũ hơn (hay gặp trên Kaggle) dùng argsort
    mặc định (không ổn định) nên khi nhiều cụm cùng kích thước thì các fold khác đi -> cổng "folds trùng G2"
    đỏ dù không có lỗi dữ liệu. Lớp này lặp lại đúng thuật toán 1.9.1 (tham lam: cụm lớn nhất vào fold nhẹ nhất)."""

    def __init__(self, n_splits=5):
        self.n_splits = n_splits

    def split(self, X=None, y=None, groups=None):
        import numpy as np
        unique, gidx = np.unique(np.asarray(groups), return_inverse=True)
        if self.n_splits > len(unique):
            raise ValueError(f'n_splits={self.n_splits} > số nhóm {len(unique)}')
        size = np.bincount(gidx)
        load = np.zeros(self.n_splits)
        to_fold = np.zeros(len(unique))
        for g in np.argsort(size, kind='stable')[::-1]:
            k = np.argmin(load)
            load[k] += size[g]
            to_fold[g] = k
        fold_of_row = to_fold[gidx]
        for f in range(self.n_splits):
            yield np.where(fold_of_row != f)[0], np.where(fold_of_row == f)[0]


# ------------------------------------------------------------------ kiểm toàn vẹn
# Kaggle tự giải nén file .gz khi nạp dataset (human-reviewed-….fasta.gz -> .fasta), nhưng script nghiên cứu
# mở bằng gzip.open(….fasta.gz). Với file .gz liệt kê dưới đây (đường dẫn trong manifest -> SHA-256 của NỘI DUNG
# ĐÃ GIẢI NÉN), nbkit nén lại file thường thành .gz và so nội dung giải nén thay vì byte nén.
UNGZ_SHA256 = {
    'data/raw/human-reviewed-2026-10-12.fasta.gz':
        'bf1bc7e188e55199a2447fc20d25834db5f7f798daa818432370deb4a6b0df5e',
}


def _gz_sha256(p) -> str | None:
    import gzip
    h = hashlib.sha256()
    try:
        with gzip.open(p, 'rb') as fh:
            for b in iter(lambda: fh.read(1 << 20), b''):
                h.update(b)
    except (OSError, EOFError):
        return None
    return h.hexdigest()


def _regzip(plain: Path, gz: Path, expected_sha256: str):
    """Nén lại `plain` -> `gz` (mtime=0 cho xác định) sau khi chắc nội dung `plain` đúng SHA-256."""
    import gzip
    if sha256_file(plain) != expected_sha256:
        raise GateFailure(f'{plain.name}: nội dung không khớp SHA-256 {expected_sha256[:12]}…')
    with open(plain, 'rb') as src, open(gz, 'wb') as raw, \
            gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as dst:
        shutil.copyfileobj(src, dst)


def verify_manifest(ws, experiment=None, deep=True) -> dict:
    """Kiểm SHA-256 từng file dữ liệu. `experiment=None` kiểm hết; ngược lại chỉ file thí nghiệm cần.
    deep=False chỉ kiểm sự tồn tại + kích thước (nhanh hơn)."""
    ws = Path(ws)
    mf = json.loads((ws / DATA_MARK).read_text())
    want = [f for f in mf['files'] if experiment is None or experiment in f.get('experiments', [])]
    if experiment is not None and not want:
        raise KeyError(f'manifest không có file nào cho thí nghiệm {experiment!r}')
    bad = []
    for f in want:
        p = ws / TOPIC_REL / f['path']
        if not p.exists() and f['path'] in UNGZ_SHA256 and p.with_suffix('').exists():
            _regzip(p.with_suffix(''), p, UNGZ_SHA256[f['path']])     # Kaggle đã giải nén .gz
        if not p.exists():
            bad.append((f['path'], 'thiếu'))
        elif f['path'] in UNGZ_SHA256 and _gz_sha256(p) == UNGZ_SHA256[f['path']]:
            continue                      # .gz nén lại: byte nén khác bản gốc, nội dung giải nén khớp SHA-256
        elif p.stat().st_size != f['bytes']:
            bad.append((f['path'], f'kích thước {p.stat().st_size} != {f["bytes"]}'))
        elif deep and sha256_file(p) != f['sha256']:
            bad.append((f['path'], 'SHA-256 lệch'))
    rep = {'package': mf.get('package'), 'created': mf.get('created'), 'experiment': experiment,
           'n_checked': len(want), 'deep': deep, 'bad': bad, 'ok': not bad,
           'manifest_sha256': sha256_file(ws / DATA_MARK)}
    if bad:
        raise GateFailure(f'manifest dữ liệu không khớp: {bad[:5]}')
    return rep


def check_protocol(ws, rel_path, expected_sha256) -> str:
    """So SHA-256 của PROTOCOL.md trong gói mã với giá trị nhúng trong notebook.

    expected_sha256 = None/'' -> chỉ in SHA (dùng khi soạn; KHÔNG hợp lệ cho lần chạy chính thức)."""
    p = Path(ws) / (rel_path if rel_path.startswith('topics/') else f'{TOPIC_REL}/{rel_path}')
    sha = sha256_file(p)
    if expected_sha256 and not str(expected_sha256).startswith('__'):
        if sha != expected_sha256:
            raise GateFailure(f'PROTOCOL.md đã đổi sau khi chốt: {sha} != {expected_sha256}. '
                              'Tiêu chí chốt trước không được sửa sau khi viết notebook.')
        print(f'PROTOCOL khớp chốt trước: sha256={sha[:16]}…')
    else:
        print(f'⚠ CHƯA CHỐT PROTOCOL (notebook chưa được stamp). sha256={sha}')
    return sha


# ------------------------------------------------------------------ môi trường
def set_seeds(seed, deterministic=True):
    import random
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except Exception:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        if deterministic:
            os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
            torch.use_deterministic_algorithms(True, warn_only=True)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except Exception:
        pass


def _ver(name):
    try:
        return _md.version(name)
    except Exception:
        return None


def env_report(ws=None) -> dict:
    rep = {'timestamp_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'platform': detect_platform(), 'python': sys.version.split()[0],
           'os': _platform.platform(), 'cpu_count': os.cpu_count(),
           'packages': {n: _ver(n) for n in ('numpy', 'scipy', 'scikit-learn', 'pandas', 'torch',
                                             'transformers', 'fair-esm', 'nbformat')},
           'threads_env': {k: os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS')}}
    try:
        rep['mem_gb'] = round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 2 ** 30, 1)
    except (ValueError, OSError, AttributeError):
        pass
    try:
        import torch
        rep['cuda_available'] = bool(torch.cuda.is_available())
        if torch.cuda.is_available():
            rep['gpus'] = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
            rep['cuda'] = torch.version.cuda
    except Exception:
        rep['cuda_available'] = False
    if ws is not None:
        ws = Path(ws)
        for mark in (CODE_MARK, DATA_MARK):
            if (ws / mark).exists():
                m = json.loads((ws / mark).read_text())
                rep[mark.split('_')[0].lower() + '_package'] = {
                    k: m.get(k) for k in ('package', 'created', 'git_commit', 'dirty', 'version')
                    if k in m} | {'manifest_sha256': sha256_file(ws / mark)}
    return rep


# ------------------------------------------------------------------ cổng tái lập
class Gates:
    """Gom các cổng tự kiểm. `check` ghi lại mọi cổng; `assert_all` dừng nếu có cổng hỏng."""

    def __init__(self):
        self.items = []

    def check(self, name, observed, expected, tol, strict=True):
        diff = float(abs(float(observed) - float(expected)))
        ok = diff <= tol
        self.items.append({'name': name, 'observed': float(observed), 'expected': float(expected),
                           'abs_diff': diff, 'tol': float(tol), 'pass': bool(ok)})
        print(f'  cổng {name}: quan sát {float(observed):.6f} · mốc {float(expected):.6f} · '
              f'|Δ|={diff:.2e} (≤ {tol:g}) -> {"ĐẠT" if ok else "HỎNG"}')
        if strict and not ok:
            raise GateFailure(f'cổng {name!r} hỏng: |Δ|={diff:.3e} > {tol:g}')
        return ok

    def assert_all(self):
        bad = [g['name'] for g in self.items if not g['pass']]
        if bad:
            raise GateFailure(f'cổng hỏng: {bad}')
        return True

    def to_dict(self):
        return {'all_pass': all(g['pass'] for g in self.items), 'gates': self.items}


# ------------------------------------------------------------------ kết quả
def _json_default(o):
    try:
        import numpy as np
        if isinstance(o, np.generic):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
    except Exception:
        pass
    if isinstance(o, Path):
        return str(o)
    raise TypeError(type(o))


def write_results(ctx_or_dir, name, obj) -> Path:
    out = Path(getattr(ctx_or_dir, 'out', ctx_or_dir))
    out.mkdir(parents=True, exist_ok=True)
    p = out / name
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=_json_default) + '\n')
    return p


class Context:
    def __init__(self, experiment, ws, platform, out, env, gates):
        self.experiment, self.ws, self.platform, self.out = experiment, Path(ws), platform, Path(out)
        self.env, self.gates = env, gates
        self.topic = self.ws / TOPIC_REL
        self.research = self.topic / 'research'
        self.data = self.topic / 'data'

    def path(self, rel):
        """Đường dẫn trong cây repo ghép (tương đối từ topics/degron-footprint/)."""
        return self.topic / rel

    def add_to_path(self, *research_dirs):
        for d in research_dirs:
            p = str(self.research / d)
            if p not in sys.path:
                sys.path.insert(0, p)

    def save(self, name, obj):
        return write_results(self, name, obj)

    def finalize(self, files=()):
        """Ghi env.json + gates.json, gom file kết quả, nén thành <exp>-results.zip để tải về.

        files: đường dẫn (tuyệt đối hoặc tương đối từ topic) của các file sinh ra cần mang về
        (results.json cạnh script, checkpoint, ...)."""
        self.save('env.json', self.env)
        self.save('gates.json', self.gates.to_dict())
        for f in files:
            f = Path(f)
            f = f if f.is_absolute() else self.topic / f
            if f.exists():
                shutil.copy2(f, self.out / f.name)
            else:
                print(f'⚠ không thấy {f} để gom')
        zpath = self.out.parent / f'{self.experiment.lower()}-results.zip'
        with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(self.out.rglob('*')):
                if p.is_file():
                    z.write(p, p.relative_to(self.out))
        print(f'\n✔ Kết quả: {zpath} ({zpath.stat().st_size/1024:.0f} KB) — tải về và giải nén vào '
              f'research/<thư-mục-thí-nghiệm>/ (xem RUN.md bước 6).')
        return zpath


def setup(experiment, protocol=None, protocol_sha256=None, needs=None, threads=2, seeds=None,
          require_gpu=False, pip=None, search=None, ws=None, deep=True) -> Context:
    """Một lệnh cho ô 0: dò nền tảng, ghép cây thư mục, kiểm SHA, kiểm PROTOCOL, đặt luồng/seed."""
    os.environ['OPENBLAS_NUM_THREADS'] = str(threads)
    os.environ['OMP_NUM_THREADS'] = str(threads)
    os.environ['MKL_NUM_THREADS'] = str(threads)
    platform = detect_platform()
    pk = find_packages(platform, search)
    print(f'nền tảng: {platform} · gói mã: {pk["code"]} · gói dữ liệu: {pk["data"]}')
    if pip:
        pip_install(*pip)
    wsp = compose_workspace(pk['code'], pk['data'], ws)
    for n in (needs or [experiment]):
        rep = verify_manifest(wsp, n, deep=deep)
        print(f'manifest dữ liệu [{n}]: {rep["n_checked"]} file khớp SHA-256')
    if protocol:
        check_protocol(wsp, protocol, protocol_sha256)
    env = env_report(wsp)
    if require_gpu and not env.get('cuda_available'):
        raise RuntimeError('Thí nghiệm này cần GPU — bật Accelerator trong Settings rồi chạy lại.')
    out = Path(OUT_DEFAULT[platform] or wsp / 'out') / experiment
    out.mkdir(parents=True, exist_ok=True)
    if seeds:
        set_seeds(seeds[0])
    sys.path.insert(0, str(wsp / TOPIC_REL / 'research' / 'notebook-kit-2026-10-22'))
    print('môi trường:', json.dumps({k: env[k] for k in ('python', 'cpu_count', 'cuda_available')
                                      if k in env}))
    return Context(experiment, wsp, platform, out, env, Gates())
