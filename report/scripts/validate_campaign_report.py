"""Validate the completed-campaign thesis update and render review contact sheets.

Requires PyMuPDF and Pillow for rendering; never loads trained models. Run after
scripts/build.py and scripts/check_template.py. QA images go to ignored build/.
"""
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from datetime import datetime, timezone

import pymupdf as fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
TOPIC = next(p for p in ROOT.parents if (p / 'data/README.md').exists())
EVIDENCE = TOPIC / 'research/output-review-2026-11-06/results.json'
OUT = ROOT / 'build/review-2026-11-06'
OUT.mkdir(exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normal(text):
    return unicodedata.normalize('NFC', text)


def main():
    data = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    review = EVIDENCE.parent
    assert sha(review/'integrity-recheck.json') == data['fresh_integrity_recheck']['record_sha256']
    assert sha(review/'metadata-recovery.json') == data['metadata_recovery']['record_sha256']
    local_source = TOPIC / 'research/kaggle-roadmap-2026-10-31'
    for name, info in data['sources'].items():
        assert sha(local_source/name) == info['sha256'], name
    assert data['source_hashes_rechecked'] == 76
    assert len(data['recipes']) == 88
    table = (ROOT/'assets/ch4/tab-campaign-all.tex').read_text(encoding='utf-8')
    rows = [s for s in table.splitlines() if s.startswith(('Kaggle &','Local &'))]
    assert len(rows) == 88
    assert sum(s.startswith('Kaggle') for s in rows) == 47
    assert sum(s.startswith('Local') for s in rows) == 41
    # Check every emitted metric and seed count, in the generator's stable order.
    for row, recipe in zip(rows,sorted(data['recipes'],key=lambda r:(r['origin'],r['recipe']))):
        columns = [s.strip() for s in row.removesuffix('\\\\').split('&')]
        expected = [str(len(recipe['seeds']))] + [f"{recipe['ensemble']['all'][k]:.4f}" for k in ['mae','auroc_plus','auprc_plus','auroc_minus']]
        assert columns[2:] == expected, recipe['recipe']
    forbidden = re.compile(r'Overfull \\[hv]box|Missing character:|multiply[ -]defined|undefined references|undefined citations|(?:Reference|Citation).*undefined',re.I)
    pdfs = {}
    for folder in ['content','content-twoside']:
        path = ROOT/'build'/folder/'content.pdf'
        log = path.with_suffix('.log').read_text(encoding='utf-8',errors='replace')
        assert not forbidden.search(log), folder
        doc = fitz.open(path)
        texts = [normal(page.get_text()) for page in doc]
        combined = '\n'.join(texts)
        for token in ['633','0.3637','0.3650','0.8405','Campaign Completion and Integrity',
                      'Frozen','LoRA','Locked','Seed Stability and Inner Selection']:
            assert token in combined, (folder,token)
        assert 'Local expansion in progress' not in combined
        assert 'two tokenizer adapters are blocked' not in combined
        assert not re.search(r'output[/\\](?:local|official)|local-output-analysis\.json|output-analysis\.json',combined)
        assert all(abs(page.rect.width-595.276)<1 and abs(page.rect.height-841.89)<1 for page in doc)
        font_records = {}
        for page in doc:
            for font in page.get_fonts(full=True):
                xref = font[0]
                if xref:
                    name,ext,kind,buffer = doc.extract_font(xref)
                    assert buffer, (folder,name,'unembedded')
                    font_records[name] = {'type':kind,'extension':ext,'embedded_bytes':len(buffer)}
        assert any('TimesNewRoman' in name.replace(' ','') for name in font_records)
        assert sum(text.count('[PENDING') for text in texts) == 6
        abstract_pages = {}
        for i,text in enumerate(texts):
            if re.match(r'^\s*ABSTRACT\s',text):
                assert 'Keywords:' in text
                abstract_pages['english'] = i+1
            if re.match(r'^\s*TÓM TẮT\s',text):
                assert re.search(r'Từ\s*khóa:',text)
                abstract_pages['vietnamese'] = i+1
        assert len(abstract_pages) == 2, abstract_pages
        # All-page contact sheets expose blank/float-only pages and geometry.
        if folder == 'content':
            for start in range(0,len(doc),20):
                sheet = Image.new('RGB',(4*270,5*390),'#dddddd')
                draw = ImageDraw.Draw(sheet)
                for offset,page in enumerate(list(doc)[start:start+20]):
                    pix = page.get_pixmap(matrix=fitz.Matrix(.4,.4),alpha=False)
                    img = Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
                    x,y=(offset%4)*270,(offset//4)*390
                    sheet.paste(img,(x+15,y+22))
                    draw.text((x+15,y+5),f'PDF page {start+offset+1}',fill='black')
                sheet.save(OUT/f'contact-{start+1:03}-{min(start+20,len(doc)):03}.png')
            # New method/results, conclusions and appendices at readable resolution.
            keywords = ['Campaign lineage','Group-aware selection','Frozen pLM ridge results',
                        'Matched adaptation evidence','Probability and transfer limitations',
                        'Campaign Completion and Integrity','All saved OOF configurations',
                        'Single-seed and ensemble','Physical output inventory','Offline Research Campaign']
            for i,text in enumerate(texts):
                if i>20 and any(k in text for k in keywords):
                    doc[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(OUT/f'detail-{i+1:03}.png')
        pdfs[folder] = {'path':str(path.relative_to(ROOT)).replace('\\','/'),
                        'sha256':sha(path),'bytes':path.stat().st_size,'pages':len(doc),
                        'all_pages_A4':True,'fonts':font_records,'abstract_pages':abstract_pages,
                        'pending_markers':6,'layout_and_reference_errors':0}
    figures = {}
    for pattern in ['assets/ch4/fig-campaign-*.pdf','assets/diagrams/campaign-2026-11-06/*.pdf']:
        for path in ROOT.glob(pattern):
            figures[str(path.relative_to(ROOT)).replace('\\','/')] = {'sha256':sha(path),'bytes':path.stat().st_size}
    assert len(figures) == 5
    record = {'generated_utc':datetime.now(timezone.utc).isoformat(),
              'evidence_sha256':sha(EVIDENCE),'evidence_sources_rechecked':76,
              'fresh_integrity_recheck':data['fresh_integrity_recheck'],
              'metadata_recovery':data['metadata_recovery'],
              'complete_table_rows':88,'pdfs':pdfs,'new_figures':figures,
              'bibliography_backend':'BibTeX/IEEE',
              'build_tool':'scripts/build.py; XeTeX TeX Live 2026',
              'raster_review':'PyMuPDF 1.26.7; contact sheets and detail pages in ignored build/review-2026-11-06',
              'limits':['No new training or software acceptance run.','Existing scientific metric helpers reused; not an independent metrics implementation.',
                        'Source 03 November validation retained unchanged.']}
    (ROOT/'current-state-validation-2026-11-06.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'pdfs':{k:v['pages'] for k,v in pdfs.items()},'rows':88,'figures':5,'status':'pass'},indent=2))


if __name__ == '__main__':
    main()
