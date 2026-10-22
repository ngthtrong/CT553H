"""Dựng và kiểm notebook .ipynb từ mã Python (không cần Jupyter). Chỉ stdlib; `nbformat` (nếu có) dùng để validate.

    from nbbuild import md, code, write_notebook, BOOTSTRAP, validate
    write_notebook(path, [md('# Tiêu đề'), code(BOOTSTRAP), code('...')], title='R0')

Notebook sinh ra KHÔNG chứa đầu ra (outputs rỗng); đầu ra chỉ có sau khi Trọng chạy trên Kaggle/Colab.
`validate(path)` kiểm: JSON hợp lệ, nbformat (nếu cài), mỗi ô code biên dịch được (`compile`), có ô tham số
`PROTOCOL_SHA256`, và không có chuỗi bị cấm (token, đường dẫn máy cá nhân, Koren/MetaDegron/Larsen/ClinVar thô).
"""
import ast
import json
import re
import sys
import uuid
from pathlib import Path

# Ô 0 dùng chung cho MỌI notebook: tìm gói mã (đã gắn vào notebook hoặc đã upload) rồi nạp nbkit.
BOOTSTRAP = r'''# --- bootstrap (giống hệt ở mọi notebook): tìm gói mã `degron-code*` và nạp nbkit ---
import sys, os, glob, zipfile

def _find_nbkit_dir():
    pats = ['/kaggle/input/**/notebook-kit-2026-10-22/nbkit.py',
            '/content/**/notebook-kit-2026-10-22/nbkit.py']
    for p in pats:
        hit = glob.glob(p, recursive=True)
        if hit:
            return os.path.dirname(hit[0])
    extra = os.environ.get('DEGRON_PACKAGES', '')      # chạy local: thư mục chứa các zip
    zips = (glob.glob(extra + '/degron-code*.zip') if extra else []) + (glob.glob('/content/degron-code*.zip') + glob.glob('/content/drive/MyDrive/**/degron-code*.zip', recursive=True)
            + glob.glob('./degron-code*.zip') + glob.glob('data/processed/packages/degron-code*.zip'))
    if zips:
        dest = '/tmp/degron-code-boot'
        zipfile.ZipFile(zips[0]).extractall(dest)
        return glob.glob(dest + '/**/notebook-kit-2026-10-22', recursive=True)[0]
    raise FileNotFoundError('Không thấy gói mã degron-code (dataset đã gắn vào notebook chưa?) — xem RUN.md bước 3-4')

sys.path.insert(0, _find_nbkit_dir())
import nbkit
print('nbkit:', nbkit.__file__)
'''

FORBIDDEN = [r'ghp_[A-Za-z0-9]{20,}', r'github_pat_', r'/home/ngthtrong', r'api[_-]?key\s*=', r'password\s*=',
             r'data/raw/koren', r'metadegron/repo', r'larsen-2025', r'clinvar/variant_summary']


def _cell_id():
    return uuid.uuid4().hex[:8]


def md(text):
    return {'cell_type': 'markdown', 'id': _cell_id(), 'metadata': {}, 'source': text.strip('\n').splitlines(True)}


def code(text):
    return {'cell_type': 'code', 'id': _cell_id(), 'metadata': {}, 'execution_count': None, 'outputs': [],
            'source': text.strip('\n').splitlines(True)}


def write_notebook(path, cells, title=''):
    nb = {'cells': cells, 'nbformat': 4, 'nbformat_minor': 5,
          'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                       'language_info': {'name': 'python'}, 'title': title}}
    Path(path).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')
    return Path(path)


def validate(path, need_protocol_param=True):
    """Trả về danh sách lỗi (rỗng = tốt)."""
    errs = []
    nb = json.loads(Path(path).read_text())
    try:
        import nbformat
        nbformat.validate(nbformat.reads(json.dumps(nb), as_version=4))
    except ImportError:
        pass
    except Exception as e:             # noqa: BLE001
        errs.append(f'nbformat: {str(e)[:200]}')
    has_param = False
    for i, c in enumerate(nb['cells']):
        src = ''.join(c['source'])
        for pat in FORBIDDEN:
            if re.search(pat, src, re.I):
                errs.append(f'ô {i}: chuỗi bị cấm /{pat}/')
        if c['cell_type'] == 'code':
            # bỏ magic %/! để compile
            clean = '\n'.join(('pass' if l.lstrip().startswith(('%', '!')) else l) for l in src.splitlines())
            try:
                ast.parse(clean)
                compile(clean, f'<cell {i}>', 'exec')
            except SyntaxError as e:
                errs.append(f'ô {i}: SyntaxError {e}')
            if 'PROTOCOL_SHA256' in src:
                has_param = True
            if c.get('outputs'):
                errs.append(f'ô {i}: có outputs (notebook phải sạch trước khi chạy)')
    if need_protocol_param and not has_param:
        errs.append('thiếu ô tham số PROTOCOL_SHA256')
    return errs


if __name__ == '__main__':
    bad = 0
    for p in sys.argv[1:]:
        e = validate(p)
        print(('OK  ' if not e else 'FAIL') + ' ' + p)
        for x in e:
            print('   -', x)
        bad += bool(e)
    sys.exit(1 if bad else 0)
