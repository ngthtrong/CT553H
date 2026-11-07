"""Check the progress update against reviewed source rows and rendered PDFs.

Run after make all/check. Does not train, load model objects or edit evidence.
Review images live in ignored build/review-progress-2026-11-06/.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote

import pymupdf as fitz
from PIL import Image, ImageDraw

REPORT = Path(__file__).resolve().parents[1]
TOPIC = next(p for p in REPORT.parents if (p / 'data/README.md').exists())
REVIEW = TOPIC / 'research/progress-review-2026-11-06'
OUT = REPORT / 'build/review-progress-2026-11-06'
OUT.mkdir(parents=True, exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    return unicodedata.normalize('NFC', text)


def main():
    audit = json.loads((REVIEW / 'local-audit.json').read_text())
    assert sha(REVIEW / 'local-audit.py') == audit['script_sha256']
    assert len(audit['recipe_metrics']) == 41
    assert audit['local_artifacts_verified'] == 4278
    assert audit['kaggle_artifacts_verified'] == 2986
    assert audit['data_manifest_files_verified'] == 32
    code = json.loads((REVIEW / 'source-inventory.code.json').read_text())
    assert code['pinned_code_hash_reproduced']
    assert all(v['pinned_hash_reproduced'] for v in code['individual_files'].values())
    source = json.loads((TOPIC / 'research/output-review-2026-11-06/results.json').read_text())
    table = (REPORT / 'assets/ch4/tab-campaign-all.tex').read_text()
    rows = [r for r in table.splitlines() if r.startswith(('Kaggle &', 'Local &'))]
    assert len(rows) == len(source['recipes']) == 88
    for row, recipe in zip(rows, sorted(source['recipes'], key=lambda r: (r['origin'], r['recipe']))):
        actual = [s.strip() for s in row.removesuffix('\\\\').split('&')][2:]
        expected = [str(len(recipe['seeds']))] + [f"{recipe['ensemble']['all'][key]:.4f}"
            for key in ['mae', 'auroc_plus', 'auprc_plus', 'auroc_minus']]
        assert actual == expected, recipe['recipe']
    # Check that generated residual rows and counts bind to the reviewed audit.
    for name in ['progress-numbers.tex', 'tab-progress-effect-errors.tex', 'tab-progress-largest-errors.tex']:
        text = (REPORT / 'assets/ch4' / name).read_text()
        assert sha(REVIEW / 'local-audit.json') in text, name
    for arm in ['B', 'D']:
        c = audit['matched_lora_minus_frozen'][arm]
        assert len(c['per_peptide']) == c['peptides_improved'] + c['peptides_worsened'] == 235
        assert all(v < 0 for v in c['leave_one_group_out_delta_range'])
    effect_table = (REPORT / 'assets/ch4/tab-progress-effect-errors.tex').read_text()
    worst_table = (REPORT / 'assets/ch4/tab-progress-largest-errors.tex').read_text()
    for recipe in audit['core_diagnostics'].values():
        for row in recipe['per_effect_class']:
            assert f"{row['mae']:.4f}" in effect_table
    for row in audit['core_diagnostics']['esm2_35m-lora-B']['largest_cell_errors'][:3]:
        assert f"{row['prediction']:.4f}" in worst_table
        assert f"{row['dpsi_mean']:.4f}" in worst_table
    broken = []
    link_count = 0
    for md in REVIEW.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', md.read_text()):
            if re.match(r'(?:https?://|mailto:|#)', link):
                continue
            path = unquote(link.split('#', 1)[0]).strip('<>')
            if not path:
                continue
            link_count += 1
            if not (md.parent / path).exists():
                broken.append(f'{md.name}: {link}')
    assert not broken, broken
    bib = (REPORT / 'bibliography/references.bib').read_text()
    keys = re.findall(r'@\w+\s*\{\s*([^,]+),', bib)
    assert len(keys) == len(set(keys))
    assert 'TO VERIFY' not in bib
    for path in list((REPORT/'chapters').rglob('*.tex')) + list((REPORT/'frontmatter').glob('*.tex')):
        for group in re.findall(r'\\cite\w*\{([^}]+)\}', path.read_text()):
            assert set(group.split(',')) <= set(keys), (path, group)
    forbidden = re.compile(r'Overfull \\[hv]box|Missing character:|multiply[ -]defined|undefined references|undefined citations|(?:Reference|Citation).*undefined', re.I)
    details = ['RESEARCH PROGRESS STATUS', 'From Proteins to Regulated Degradation',
        'Conceptual', 'Research Progress and Data Evolution', 'Residual Diagnostics',
        'Three largest absolute cell errors', 'Research questions, current evidence',
        'Provisional Findings', 'Recorded protocols']
    pdfs = {}
    for folder in ['content', 'content-twoside']:
        path = REPORT / 'build' / folder / 'content.pdf'
        assert not forbidden.search(path.with_suffix('.log').read_text(errors='replace'))
        doc = fitz.open(path)
        texts = [normalized(p.get_text()) for p in doc]
        combined = '\n'.join(texts)
        for token in ['RESEARCH PROGRESS STATUS', '0.3637', '0.3650', '0.8405',
                      'Research Progress and Data Evolution', 'Residual Diagnostics', '184', '164']:
            assert token in combined, (folder, token)
        assert not re.search(r'output[/\\](?:local|official)|local-output-analysis\.json|output-analysis\.json', combined)
        assert all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc)
        fonts = {}
        for page in doc:
            for font in page.get_fonts(full=True):
                if font[0]:
                    name, ext, kind, data = doc.extract_font(font[0])
                    assert data, (folder, name, 'unembedded font')
                    fonts[name] = {'extension': ext, 'type': kind}
            for link in page.get_links():
                if link['kind'] == fitz.LINK_GOTO:
                    assert 0 <= link['page'] < len(doc), (folder, page.number, link)
        assert any('TimesNewRoman' in name.replace(' ', '') for name in fonts)
        abstracts = {}
        detail_pages = []
        for i, value in enumerate(texts):
            if re.match(r'^\s*ABSTRACT\s', value):
                assert 'Keywords:' in value
                abstracts['english'] = i+1
            if re.match(r'^\s*TÓM TẮT\s', value):
                assert re.search(r'Từ\s*khóa:', value)
                abstracts['vietnamese'] = i+1
            if any(t in value for t in details) and (i < 10 or i > 18):
                doc[i].get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(OUT / f'{folder}-detail-{i+1:03}.png')
                detail_pages.append(i+1)
        assert len(abstracts) == 2
        for start in range(0, len(doc), 24):
            sheet = Image.new('RGB', (4*210, 6*310), '#dddddd')
            draw = ImageDraw.Draw(sheet)
            for offset, page in enumerate(list(doc)[start:start+24]):
                pix = page.get_pixmap(matrix=fitz.Matrix(.31, .31), alpha=False)
                img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
                x, y = (offset%4)*210, (offset//4)*310
                sheet.paste(img, (x+10, y+20))
                draw.text((x+10, y+4), f'{folder} {start+offset+1}', fill='black')
            sheet.save(OUT / f'{folder}-contact-{start+1:03}.png')
        pdfs[folder] = {'sha256': sha(path), 'pages': len(doc), 'bytes': path.stat().st_size,
                       'all_pages_A4': True, 'fonts': fonts, 'abstract_pages': abstracts,
                       'pending_markers': combined.count('[PENDING'), 'detail_pages': detail_pages,
                       'internal_link_destinations_valid': True}
    record = {'generated_utc': datetime.now(timezone.utc).isoformat(),
        'checked_local_audit_sha256': sha(REVIEW/'local-audit.json'),
        'code_inventory_sha256': sha(REVIEW/'source-inventory.code.json'),
        'review_local_links_checked': link_count, 'broken_review_local_links': [],
        'all_campaign_rows_matched_to_JSON': 88, 'bibliography_unique_entries': len(keys),
        'pdfs': pdfs, 'rendered_review_directory': str(OUT.relative_to(REPORT)),
        'bibliography_backend': 'biblatex/IEEE + Biber',
        'limits': ['Rendered images require human visual inspection in addition to this automated check.',
                   'No new training or biological validation; independent metric checks use saved predictions.',
                   'Historical PDF validation records retain their original scope and hashes.']}
    (REPORT/'progress-validation-2026-11-06.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'pdf_pages': {k:v['pages'] for k,v in pdfs.items()},
                      'review_local_links': link_count, 'campaign_rows': 88, 'bib_entries': len(keys)}, indent=2))


if __name__ == '__main__':
    main()
