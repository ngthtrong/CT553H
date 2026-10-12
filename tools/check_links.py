#!/usr/bin/env python3
"""Kiểm tra link tương đối trong mọi file .md/.html được git theo dõi.

Chạy từ bất kỳ đâu trong repo:  python3 tools/check_links.py
Trả mã 1 nếu có link hỏng. Bỏ qua link http(s), mailto, anchor thuần và link sinh bằng JavaScript.
"""
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "DECISIONS.md").exists())
LINK_MD = re.compile(r"\]\(<([^>]+)>\)|\]\(([^)\s]+)\)")
LINK_ATTR = re.compile(r"""(?:href|src)=["']([^"']+)["']""")


CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def targets(text, is_html):
    if not is_html:  # trong .md bỏ qua code; trong .html chỉ xét href/src
        text = CODE.sub("", text)
        for m in LINK_MD.finditer(text):
            yield m.group(1) or m.group(2)
    if is_html or "<img" in text or "<a " in text:
        for m in LINK_ATTR.finditer(text):
            yield m.group(1)


def main():
    files = subprocess.check_output(
        ["git", "-c", "core.quotepath=off", "ls-files", "-z", "--cached", "--others",
         "--exclude-standard", "*.md", "*.html"], cwd=ROOT).decode().split("\0")
    broken = 0
    for rel in filter(None, files):
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for t in targets(text, rel.endswith(".html")):
            if re.match(r"^[a-z][a-z0-9+.-]*:", t, re.I) or t.startswith(("#", "//")):
                continue
            if any(c in t for c in "{}$+") or t.startswith("'"):
                continue
            p = urllib.parse.unquote(t.split("#")[0])
            if p and not (path.parent / p).exists():
                print(f"{rel}: {t}")
                broken += 1
    print(f"{broken} link hỏng" if broken else "Không có link hỏng.")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
