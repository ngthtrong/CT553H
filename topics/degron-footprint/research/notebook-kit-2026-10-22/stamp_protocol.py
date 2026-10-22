#!/usr/bin/env python3
"""Chốt SHA-256 của PROTOCOL.md vào notebook: thay giá trị của biến `PROTOCOL_SHA256` (ô tham số).

  python3 -I stamp_protocol.py <notebook.ipynb> <PROTOCOL.md>

Ô tham số phải chứa một dòng dạng  PROTOCOL_SHA256 = "__STAMP__"  (hoặc một hex đã stamp trước đó).
Chạy lại sau MỖI lần PROTOCOL.md đổi; nbkit.check_protocol sẽ dừng notebook nếu SHA không khớp, tức là
tiêu chí chốt trước không sửa lặng lẽ sau khi viết notebook. Chỉ stamp khi PROTOCOL đã được chốt thật.
"""
import hashlib
import json
import re
import sys
from pathlib import Path


def main(nb_path, protocol_path):
    sha = hashlib.sha256(Path(protocol_path).read_bytes()).hexdigest()
    nb = json.loads(Path(nb_path).read_text())
    pat = re.compile(r'(PROTOCOL_SHA256\s*=\s*)["\'][^"\']*["\']')
    n = 0
    for c in nb['cells']:
        if c['cell_type'] != 'code':
            continue
        src = ''.join(c['source'])
        new, k = pat.subn(lambda m: f'{m.group(1)}"{sha}"', src)
        if k:
            c['source'] = new.splitlines(keepends=True)
            n += k
    if not n:
        sys.exit('không thấy dòng PROTOCOL_SHA256 = "..." trong notebook')
    Path(nb_path).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')
    print(f'đã stamp {nb_path}: PROTOCOL_SHA256 = {sha}')


if __name__ == '__main__':
    main(*sys.argv[1:3])
