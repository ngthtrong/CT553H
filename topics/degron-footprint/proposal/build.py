#!/usr/bin/env python3
"""Build editable Word and a stable, checked PDF from one Markdown source."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
SAMPLE = ROOT / 'report/guideline-thesis/Đề cương LV Mau (1).docx'
PDF_SAMPLE = SAMPLE.with_name('Đề cương LV Mau.pdf')
BUILD = HERE / 'build'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'

def run(args):
    result = subprocess.run([str(a) for a in args], cwd=HERE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout)
    return result.stdout

def reference_docx():
    """Retain source page geometry, set supported Word styles for authored content."""
    ref = BUILD / 'reference.docx'
    with ZipFile(SAMPLE) as src, ZipFile(ref, 'w', ZIP_DEFLATED) as dst:
        for entry in src.infolist():
            data = src.read(entry.filename)
            if entry.filename == 'word/styles.xml':
                tree = ET.fromstring(data)
                defaults = tree.find('w:docDefaults/w:rPrDefault/w:rPr', NS)
                if defaults is not None:
                    font = defaults.find('w:rFonts', NS)
                    if font is not None:
                        font.attrib.clear()
                        for key in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
                            font.set(W + key, 'Times New Roman')
                for style in tree.findall('w:style', NS):
                    if style.get(W + 'type') != 'paragraph':
                        continue
                    sid = style.get(W + 'styleId', '')
                    rp = style.find('w:rPr', NS)
                    if rp is None:
                        rp = ET.SubElement(style, W + 'rPr')
                    font = rp.find('w:rFonts', NS)
                    if font is None:
                        font = ET.SubElement(rp, W + 'rFonts')
                    font.attrib.clear()
                    for key in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
                        font.set(W + key, 'Times New Roman')
                    for tag in ('sz', 'szCs'):
                        size = rp.find('w:' + tag, NS)
                        if size is None:
                            size = ET.SubElement(rp, W + tag)
                        size.set(W + 'val', '28' if sid == 'Title' else '24')
                    color = rp.find('w:color', NS)
                    if color is None:
                        color = ET.SubElement(rp, W + 'color')
                    color.attrib.clear()
                    color.set(W + 'val', '000000')
                    pp = style.find('w:pPr', NS)
                    if pp is None:
                        pp = ET.SubElement(style, W + 'pPr')
                    spacing = pp.find('w:spacing', NS)
                    if spacing is None:
                        spacing = ET.SubElement(pp, W + 'spacing')
                    spacing.set(W + 'line', '276')
                    spacing.set(W + 'lineRule', 'auto')
                data = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
            dst.writestr(entry, data)
    return ref

def validate():
    pdf = HERE / 'proposal.pdf'
    info = run(['pdfinfo', pdf])
    assert '612 x 792 pts' in info, info
    text = run(['pdftotext', '-layout', pdf, '-'])
    headings = ['I. MỞ ĐẦU', 'II. CƠ SỞ LÝ THUYẾT', 'III. PHƯƠNG PHÁP NGHIÊN CỨU',
                'IV. ỨNG DỤNG THỰC TẾ VÀ NGUỒN DỮ LIỆU', 'V. CÁC DỰ ÁN LIÊN QUAN',
                'VI. DỰ KIẾN KẾT QUẢ VÀ ĐÓNG GÓP', 'VII. TÀI LIỆU THAM KHẢO']
    flat = ' '.join(text.split())
    for title in headings:
        assert title in flat, title
    assert 'Nguyễn Thanh Trọng' in text and 'B2305615' in text
    assert '0,8082' in text and '0,7693' in text
    with ZipFile(HERE / 'proposal.docx') as z:
        doc = ET.fromstring(z.read('word/document.xml'))
        word_text = ' '.join(x.text or '' for x in doc.findall('.//w:t', NS))
        for title in headings:
            assert title in word_text, title
        section = doc.find('.//w:sectPr', NS)
        size = section.find('w:pgSz', NS)
        assert size.get(W + 'w') == '12240' and size.get(W + 'h') == '15840'
    result = json.loads((ROOT / 'topics/degron-footprint/research/g2-saturation-2026-10-18/results.json').read_text())
    assert (result['n_peptides'], result['n_clusters'], result['n_cells']) == (91, 89, 47847)
    assert round(result['macro_auroc']['ridge'], 4) == .8082
    assert round(result['macro_auroc']['DeltaPAP'], 4) == .7693
    fonts = run(['pdffonts', pdf])
    assert 'TimesNewRoman' in fonts
    # Every font row must be embedded (emb column follows encoding).
    for row in fonts.splitlines()[2:]:
        assert re.search(r'\s+yes\s+(?:yes|no)\s+(?:yes|no)\s+\d+\s+\d+\s*$', row), row
    log = (BUILD / 'proposal.log').read_text()
    for forbidden in ['Overfull \\hbox', 'Overfull \\vbox', 'Missing character:', 'undefined references', 'multiply defined']:
        assert forbidden not in log, forbidden
    manifest = {
        'date': '2026-10-21', 'format': 'Letter, 1-inch margins, Times New Roman; geometry follows supplied sample',
        'pages': int(re.search(r'Pages:\s+(\d+)', info).group(1)),
        'checks': ['seven required sections in Word and PDF', 'student metadata', 'Letter page size',
                   'embedded fonts', 'no LaTeX overflow or missing glyphs', 'preliminary metrics match results.json'],
        'files': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [PDF_SAMPLE, SAMPLE, HERE/'proposal.md', HERE/'proposal.pdf', HERE/'proposal.docx', HERE/'references.bib', HERE/'header.tex', HERE/'layout.lua', HERE/'build.py']},
    }
    (HERE / 'validation.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'pages': manifest['pages'], 'checks': 'passed'}, ensure_ascii=False))

def link_citations():
    """Write build/source.md: each [n] / [n, m] / [n–m] links to its reference entry."""
    text = (HERE / 'proposal.md').read_text()
    head, sep, refs = text.partition('# VII. TÀI LIỆU THAM KHẢO')
    link = lambda n: f'[{n}](#ref-{n})'
    def cite(m):
        body = m.group(1)
        parts = re.split(r'(\s*,\s*|–)', body)
        return '[' + ''.join(link(x) if x.isdigit() else x for x in parts) + ']'
    head = re.sub(r'\[(\d+(?:(?:\s*,\s*|–)\d+)*)\](?!\()', cite, head)
    refs = re.sub(r'^(\d+)\. ', lambda m: f'{m.group(1)}. []{{#ref-{m.group(1)}}}', refs, flags=re.M)
    refs = re.sub(r'\[(\d+(?:–\d+)?)\]', cite, refs.replace('[8–10]', '[8–10]'))
    (BUILD / 'source.md').write_text(head + sep + refs)

if '--check' not in sys.argv:
    BUILD.mkdir(exist_ok=True)
    link_citations()
    ref = reference_docx()
    run(['pandoc', BUILD/'source.md', '--lua-filter', 'layout.lua', '--reference-doc', ref, '-o', 'proposal.docx'])
    fonts = '/mnt/c/Windows/Fonts/'
    run(['pandoc', BUILD/'source.md', '--lua-filter', 'layout.lua', '-s', '-t', 'latex', '-o', BUILD/'proposal.tex',
         '-V', 'documentclass=article', '-V', 'fontsize=12pt', '-V', 'papersize=letter',
         '-V', 'geometry:margin=1in', '-V', 'linestretch=1.15',
         '-V', 'mainfont=times.ttf', '-V', f'mainfontoptions:Path={fonts}',
         '-V', 'mainfontoptions:BoldFont=timesbd.ttf',
         '-V', 'mainfontoptions:ItalicFont=timesi.ttf',
         '-V', 'mainfontoptions:BoldItalicFont=timesbi.ttf',
         '--include-in-header', 'header.tex'])
    previous = None
    for attempt in range(5):
        run(['xelatex', '-halt-on-error', '-interaction=nonstopmode', '-output-directory', BUILD, BUILD/'proposal.tex'])
        aux = (BUILD/'proposal.aux').read_bytes()
        if aux == previous:
            break
        previous = aux
    else:
        raise RuntimeError('References did not stabilize after five passes')
    (HERE/'proposal.pdf').write_bytes((BUILD/'proposal.pdf').read_bytes())
validate()
