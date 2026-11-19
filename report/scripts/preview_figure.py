"""Render one figure file of assets/figures/ on its own, for quick visual review.

Usage (from report/):  python3 scripts/preview_figure.py <name> [--dpi 110]
Builds assets/figures/<name>.tex inside a minimal document that loads the same fonts,
packages, macros and figure style as the thesis, at the thesis text width (15.5 cm),
and writes build/preview/<name>.pdf and build/preview/<name>.png. Standard library only;
needs xelatex and pdftoppm. This is a preview, not the thesis build.
"""
from pathlib import Path
import argparse
import subprocess
import sys

REPORT = Path(__file__).resolve().parents[1]
OUT = REPORT / 'build' / 'preview'

DOC = r"""\documentclass[fontsize=13bp]{scrreprt}
\usepackage[paperwidth=17.5cm,paperheight=29cm,margin=1cm]{geometry}
\input{template/typography}
\input{template/packages}
\input{assets/figures/style}
\input{assets/ch4/numbers}
\input{assets/ch4/campaign-numbers}
\input{assets/ch4/transfer-numbers}
\input{assets/ch4/app-numbers}
\input{assets/ch4/progress-numbers}
\input{assets/ch4/priority-numbers}
\providecommand{\citep}[1]{[#1]}
\usepackage[active,tightpage]{preview}
\setlength\PreviewBorder{4pt}
\pagestyle{empty}
\begin{document}
\begin{preview}
\begin{minipage}{15.5cm}\centering
\input{assets/figures/%s}
\end{minipage}
\end{preview}
\end{document}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('--dpi', type=int, default=110)
    args = ap.parse_args()
    src = REPORT / 'assets' / 'figures' / f'{args.name}.tex'
    if not src.exists():
        sys.exit(f'missing {src}')
    OUT.mkdir(parents=True, exist_ok=True)
    tex = OUT / f'{args.name}.tex'
    tex.write_text(DOC % args.name, encoding='utf-8')
    run = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error',
                          f'-output-directory={OUT}', str(tex)],
                         cwd=REPORT, capture_output=True, text=True)
    log = (OUT / f'{args.name}.log').read_text(encoding='utf-8', errors='replace')
    problems = [l for l in log.splitlines()
                if l.startswith('!') or 'Overfull' in l or 'Missing character' in l]
    if run.returncode != 0 or problems:
        print('\n'.join(problems[:20]) or run.stdout[-3000:])
        sys.exit(1)
    subprocess.run(['pdftoppm', '-r', str(args.dpi), '-png', '-singlefile', '-cropbox',
                    str(OUT / f'{args.name}.pdf'), str(OUT / args.name)], check=True)
    print(OUT / f'{args.name}.png')


if __name__ == '__main__':
    main()
