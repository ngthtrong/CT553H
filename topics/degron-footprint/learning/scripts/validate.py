#!/usr/bin/env python3
"""Check scientific scope, source freshness, native exports and the final PDF."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
import pymupdf

HERE=Path(__file__).resolve().parents[1]
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def compact(text):return re.sub(r'\s+','',unicodedata.normalize('NFC',text))

def main():
    evidence=json.loads((HERE/'evidence.json').read_text())
    assert len(evidence['sources'])==31
    for source in evidence['sources']:
        assert digest(ROOT/source['path'])==source['sha256'],f"Stale source: {source['id']}"
        if source['id']=='KH-03':
            assert source['path'].endswith('/plan.json'),'Partial local outputs must be excluded'
    chapter_files=sorted((HERE/'chapters').glob('*.md'))
    assert len(chapter_files)==18
    body=(HERE/'build/study-guide.md').read_text()
    assert not re.search(r'\{\{[A-Z_]+\}\}',body)
    local=(HERE/'chapters/14-local-training-direction.md').read_text()
    assert 'không công bố kết quả local' in local
    assert '455' not in local and '635' not in local
    assert not re.search(r'(?:MAE|AUROC|Brier)\s*[=:]\s*\d',local)
    assert 'e7097449883a51d8' not in body
    assert 'fixture tổng hợp' in body and 'ví dụ tự đặt' in body.lower()
    expected_ids={s['id'] for s in evidence['sources']}|{f'TL-{n:02d}' for n in range(1,6)}
    seen_ids=set(re.findall(r'\b(?:NC|KH|PM|TL)-\d{2}\b',body))
    assert seen_ids==expected_ids,seen_ids^expected_ids
    for key,value in evidence['values'].items():
        assert value in body,f'Missing substituted value: {key}'
    assert evidence['values']['CNN_D']=='0,38435'
    assert evidence['values']['MCNN_E']=='0,38385'
    assert evidence['values']['W5_D']=='0,40780'
    v3=evidence['fullpsi']['recipes']
    assert abs(v3['esm2_35m-cnn-D']['ensemble']['all']['mae']-
               v3['esm2_35m-pointwise-D']['ensemble']['all']['mae']+0.00533893)<1e-6
    diagrams=json.loads((HERE/'diagram-manifest.json').read_text())
    assert len(diagrams)==12
    exported=[]
    for rec in diagrams:
        stem=HERE/'assets/diagrams'/rec['name']
        proc=subprocess.run(['python3',str(ROOT/'.agents/skills/drawio-skill/scripts/validate.py'),
                             str(stem.with_suffix('.drawio')),'--json'],check=True,capture_output=True,text=True)
        result=json.JSONDecoder().raw_decode(proc.stdout)[0]
        assert result['errors']==0 and result['warnings']==0
        tree=ET.parse(stem.with_suffix('.drawio'))
        labels=[c.attrib['value'] for c in tree.iter('mxCell') if c.attrib.get('vertex')=='1']
        with pymupdf.open(stem.with_suffix('.pdf')) as pdf:
            assert len(pdf)==1
            native_text=compact(pdf[0].get_text())
            # Native PDFs can silently use a Letter page and clip the right side.
            for label in labels:
                assert compact(label) in native_text,f'Clipped native PDF label: {rec["name"]}: {label}'
            width,height=pdf[0].rect.width,pdf[0].rect.height
        assert stem.with_suffix('.png').stat().st_size>5000
        exported.append(dict(name=rec['name'],labels=len(labels),complete=True,
                             pdf_size_pt=[round(width,2),round(height,2)]))
    figures=json.loads((HERE/'figure-manifest.json').read_text())
    assert len(figures)==10
    assert Counter(r['kind'] for r in figures)=={'measured':8,'illustrative':1,'synthetic-ui':1}
    for rec in figures:
        assert (HERE/'assets/figures'/(rec['name']+'.png')).exists()
    log=(HERE/'build/study-guide.log').read_text()
    bad=re.findall(r'.*(?:Overfull \\[hv]box|Missing character:|undefined references|multiply defined|LaTeX Error).*',log)
    assert not bad,bad
    fonts=subprocess.check_output(['pdffonts',str(HERE/'study-guide.pdf')],text=True)
    for line in fonts.splitlines()[2:]:
        assert re.search(r'\byes\s+yes\s+yes\b',line),line
    with pymupdf.open(HERE/'study-guide.pdf') as doc:
        pages=len(doc);toc=doc.get_toc();links=[];texts=[];out_of_page=[]
        for n,page in enumerate(doc,1):
            assert abs(page.rect.width-595.276)<1 and abs(page.rect.height-841.89)<1
            text=page.get_text();texts.append(text)
            assert len(text.strip())>30,f'Blank page: {n}'
            assert '\ufffd' not in text
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        box=pymupdf.Rect(span['bbox'])
                        if box.x0<-1 or box.y0<-1 or box.x1>page.rect.width+1 or box.y1>page.rect.height+1:
                            out_of_page.append(dict(page=n,text=span['text']))
            for link in page.get_links():
                if link['kind'] in (pymupdf.LINK_GOTO,pymupdf.LINK_NAMED):assert 0<=link['page']<pages
                elif link['kind']==pymupdf.LINK_URI:assert link['uri'].startswith('https://')
                else:raise AssertionError(f'Unexpected PDF link: {link}')
                links.append(link['kind'])
        assert not out_of_page,out_of_page
        chapter_bookmarks=[row for row in toc if row[0]==1]
        assert len(chapter_bookmarks)==19
        alltext='\n'.join(texts)
        assert '0,38435' in alltext and '0,40780' in alltext and '122.412' in alltext
        for bad_text in ['[PENDING]','topics/degron-footprint/research/','file://','e7097449883a51d8']:
            assert bad_text not in alltext,bad_text
        local_start=next(row[2] for row in chapter_bookmarks if 'Train local đang' in row[1])
        local_end=next(row[2] for row in chapter_bookmarks if row[1].startswith('Phần mềm:'))-1
    artifact_files=chapter_files+list((HERE/'scripts').glob('*'))+list((HERE/'assets').rglob('*'))
    artifact_hashes={str(p.relative_to(HERE)):digest(p) for p in artifact_files if p.is_file()}
    result=dict(status='pass',date='2026-11-03',pages=pages,chapters=19,
                diagrams=12,other_figures=10,evidence_sources=31,external_background_sources=5,
                pdf_sha256=digest(HERE/'study-guide.pdf'),fonts_embedded=True,a4_all_pages=True,
                overflow_or_missing_glyphs=False,bookmarks=len(toc),links=len(links),
                local_plan_pdf_pages=[local_start,local_end],partial_local_scores_excluded=True,
                native_diagrams=exported,artifact_hashes=artifact_hashes,
                limits=['No new model training or app acceptance tests',
                        'Scientific conclusions remain development-scoped',
                        'Automated PDF checks do not replace page-image inspection'])
    (HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'PASS: {pages} A4 pages; 19 chapters; 22 figures; 31 saved sources; all native PDF labels complete')

if __name__=='__main__':main()
