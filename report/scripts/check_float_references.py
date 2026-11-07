#!/usr/bin/env python3
"""Check built float lists against labels, prose references and printed PDF pages.

Uses only the standard library and Poppler. This checks numbering and reference
consistency, not visual whitespace, figure readability or scientific correctness.
"""
from collections import defaultdict
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def groups(text, start=0, count=None):
    """Read adjacent TeX groups, respecting nested and escaped braces."""
    result = []
    pos = start
    while count is None or len(result) < count:
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos >= len(text) or text[pos] != '{':
            break
        begin = pos + 1
        depth = 1
        pos += 1
        while pos < len(text) and depth:
            if text[pos] == '\\':
                pos += 2
                continue
            if text[pos] == '{':
                depth += 1
            elif text[pos] == '}':
                depth -= 1
            pos += 1
        if depth:
            raise ValueError('Unclosed TeX group')
        result.append(text[begin:pos - 1])
    return result


def title(text):
    # Numeric source macros can stay protected in \newlabel while \numberline
    # expands them. Resolve the same no-argument definitions before comparing.
    macros = {}
    for path in (ROOT / 'assets/ch4').glob('*numbers.tex'):
        source = path.read_text()
        for match in re.finditer(r'\\(?:newcommand|providecommand)\s*(?=\{)', source):
            fields = groups(source, match.end(), 2)
            if len(fields) == 2 and re.fullmatch(r'\\[A-Za-z]+', fields[0]):
                macros[fields[0][1:]] = fields[1]
    for _ in range(5):
        expanded = re.sub(r'\\([A-Za-z]+)(?:\s*\{\})?',
                          lambda m: macros.get(m[1], m[0]), text)
        if expanded == text:
            break
        text = expanded
    text = re.sub(r'\\(?:ignorespaces|relax)\b\s*', '', text).replace('{}', '')
    text = text.replace(r'\mitDelta', r'\Delta')  # unicode-math expansion in list writes
    text = re.sub(r'(\\[A-Za-z]+)\s+(?=\{)', r'\1', text)
    return ' '.join(text.split()).rstrip('.')


def check_variant(folder):
    directory = ROOT / 'build' / folder
    labels = {}
    for path in directory.rglob('*.aux'):
        for line in path.read_text().splitlines():
            if not line.startswith(r'\newlabel{'):
                continue
            name, value = groups(line, len(r'\newlabel'), 2)
            if not name.startswith(('fig:', 'tab:')):
                continue
            fields = groups(value)
            if len(fields) < 4:
                raise ValueError(f'{folder}: malformed label {name}')
            if name in labels:
                raise ValueError(f'{folder}: duplicate label {name}')
            labels[name] = fields

    pdf = directory / 'content.pdf'
    pages = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], check=True,
                           capture_output=True, text=True).stdout.split('\f')
    destination_text = subprocess.run(['pdfinfo', '-dests', str(pdf)], check=True,
                                      capture_output=True, text=True).stdout
    destinations = {name: int(page) for page, name in
                    re.findall(r'^\s*(\d+)\s+\[[^\n]*\]\s+"([^"]+)"\s*$',
                               destination_text, re.M)}
    body = [i for i, page in enumerate(pages)
            if any(line.strip() == 'PART 1. INTRODUCTION' for line in page.splitlines())]
    if len(body) != 1:
        raise ValueError(f'{folder}: cannot locate Arabic page 1')
    source = '\n'.join(re.sub(r'(?<!\\)%[^\n]*', '', p.read_text())
                       for subdir in ['chapters', 'appendices']
                       for p in (ROOT / subdir).rglob('*.tex'))
    # References inside captions are not prose references to the figure itself.
    prose = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', source, flags=re.S)
    refs = set(re.findall(r'\\(?:ref|autoref|cref|Cref)\{(fig:[^}]+)\}', prose))
    figures = {name for name in labels if name.startswith('fig:')}
    if figures != refs:
        raise ValueError(f'{folder}: unreferenced figures {sorted(figures - refs)}; '
                         f'unknown figure references {sorted(refs - figures)}')

    matched = set()
    counts = {}
    for kind, suffix, prefix in [('figure', 'lof', 'Figure'), ('table', 'lot', 'Table')]:
        seen_numbers = set()
        previous = defaultdict(int)
        last_page = 0
        last_chapter = -1
        entries = []
        for line in (directory / f'content.{suffix}').read_text().splitlines():
            if not line.startswith(r'\contentsline '):
                continue
            entry_kind, value, page, anchor = groups(line, len(r'\contentsline'), 4)
            if entry_kind != kind or not value.startswith(r'\numberline '):
                raise ValueError(f'{folder}: invalid {kind} list entry')
            number, caption = groups(value, len(r'\numberline'), 2)
            chapter, index = number.rsplit('.', 1)
            chapter_order = int(chapter) if chapter.isdigit() else 100 + ord(chapter)
            if chapter_order < last_chapter:
                raise ValueError(f'{folder}: {kind} chapters are out of order')
            last_chapter = chapter_order
            if number in seen_numbers or int(index) != previous[chapter] + 1:
                raise ValueError(f'{folder}: nonsequential {kind} number {number}')
            previous[chapter] = int(index)
            seen_numbers.add(number)
            owners = [(name, fields) for name, fields in labels.items()
                      if fields[3] == anchor]
            if len(owners) != 1:
                raise ValueError(f'{folder}: {kind} {number} has {len(owners)} labels')
            name, fields = owners[0]
            if fields[:2] != [number, page] or title(fields[2]) != title(caption):
                raise ValueError(f'{folder}: list/label mismatch for {name}')
            if not name.startswith('fig:' if kind == 'figure' else 'tab:'):
                raise ValueError(f'{folder}: wrong label prefix {name}')
            if int(page) < last_page:
                raise ValueError(f'{folder}: {kind} pages are out of order')
            last_page = int(page)
            physical = body[0] + int(page) - 1
            printed = ' '.join(pages[physical].split())
            if not re.search(r'\b' + prefix + r'\s+' + re.escape(number) + r'\.(?:\s|$)', printed):
                raise ValueError(f'{folder}: missing printed caption for {name} on page {page}')
            if destinations.get(anchor) != physical + 1:
                raise ValueError(f'{folder}: wrong PDF destination for {name}')
            matched.add(name)
            entries.append((name, number, page, title(caption)))
        counts[kind] = entries
    if matched != labels.keys():
        raise ValueError(f'{folder}: float labels absent from lists: {sorted(labels.keys() - matched)}')
    print(f'{folder}: {len(counts["figure"])} figures, {len(counts["table"])} tables; '
          'sequential numbers, list titles/pages, PDF destinations and figure references agree')
    return counts


def main():
    try:
        one = check_variant('content')
        two = check_variant('content-twoside')
        if one != two:
            raise ValueError('One-/two-sided float inventories differ')
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from error
    print('PASS: float reference consistency in both thesis variants.')


if __name__ == '__main__':
    main()
