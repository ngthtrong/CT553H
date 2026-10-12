#!/usr/bin/env python3
"""Đổi tên (hoặc chuyển) một thư mục đề tài và sửa mọi link tương đối trỏ tới nó.

Ví dụ:
    python3 tools/rename_topic.py plm-calibration-audit 1-plm-calibration-audit
    python3 tools/rename_topic.py topics/legal-qa-grounding archive/topics/legal-qa-grounding

Tên không có dấu "/" được hiểu là nằm trong topics/. Dùng `git mv` nên giữ lịch sử.
Thư mục data/ (không lên git) nằm trong thư mục đề tài nên đi theo cùng. Đường dẫn dạng chữ
"topics/<cũ>/" trong tài liệu và script cũng được thay.
Thêm --dry để chỉ in ra những gì sẽ đổi.
"""
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "DECISIONS.md").exists())
LINK_MD = re.compile(r"(\]\()(<?)([^)>\s]+|[^)>]+(?=>))(>?)(\))")
LINK_ATTR = re.compile(r"""((?:href|src)=)(["'])([^"']+)(\2)""")


def norm(arg):
    return arg.strip("/") if "/" in arg else f"topics/{arg}"


def main():
    args = [a for a in sys.argv[1:] if a != "--dry"]
    dry = "--dry" in sys.argv
    if len(args) != 2:
        sys.exit(__doc__)
    old, new = norm(args[0]), norm(args[1])
    if not (ROOT / old).is_dir():
        sys.exit(f"Không thấy thư mục {old}")
    if (ROOT / new).exists():
        sys.exit(f"{new} đã tồn tại")

    def mp(p):  # đường dẫn repo-relative cũ -> mới
        return new + p[len(old):] if p == old or p.startswith(old + "/") else p

    def fix(target, src_old, src_new):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith(("#", "//")):
            return target
        if any(c in target for c in "{}$+"):
            return target
        path, sep, anchor = target.partition("#")
        if not path:
            return target
        raw = urllib.parse.unquote(path)
        abs_old = os.path.normpath(os.path.join(os.path.dirname(src_old), raw))
        abs_new = mp(abs_old)
        if abs_new == abs_old and src_new == src_old:
            return target
        rel = os.path.relpath(abs_new, os.path.dirname(src_new) or ".")
        if raw.endswith("/") and not rel.endswith("/"):
            rel += "/"
        if " " in raw and "%20" not in path:
            rel = rel  # giữ khoảng trắng nếu link gốc dùng <...>
        else:
            rel = urllib.parse.quote(rel, safe="/.-_~:")
        return rel + (sep + anchor if sep else "")

    # đường dẫn dạng chữ (lệnh, backtick) tính từ gốc repo, ví dụ `topics/<cũ>/data/raw`
    plain = re.compile(r"(?<![\w/.-])" + re.escape(old) + r"(?=/|`|\s|$)")
    text_files = [f for f in subprocess.check_output(
        ["git", "-c", "core.quotepath=off", "ls-files", "-z", "*.md", "*.html", "*.py", "*.txt"],
        cwd=ROOT).decode().split("\0") if f]

    changed = []
    for f in text_files:
        f_new = mp(f)
        text = (ROOT / f).read_text(encoding="utf-8")
        out = text
        if f.endswith((".md", ".html")):
            out = LINK_MD.sub(lambda m: m.group(1) + m.group(2) + fix(m.group(3), f, f_new) + m.group(4) + m.group(5), out)
            out = LINK_ATTR.sub(lambda m: m.group(1) + m.group(2) + fix(m.group(3), f, f_new) + m.group(4), out)
        out = plain.sub(new, out)
        if out != text:
            changed.append((f, out))

    print(f"git mv {old} {new}; sửa link trong {len(changed)} file")
    if dry:
        for f, _ in changed:
            print("  ", f)
        return
    (ROOT / new).parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["git", "mv", old, new], cwd=ROOT)
    for f, out in changed:
        (ROOT / mp(f)).write_text(out, encoding="utf-8")
    print("Xong. Chạy python3 tools/check_links.py để kiểm lại.")


if __name__ == "__main__":
    main()
