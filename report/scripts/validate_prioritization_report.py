"""Check source-bound prioritisation assets and both rendered thesis variants.

Run after make all/check, with the analysis .venv Python. Writes only the
new dated validation JSON and ignored PDF review images, never old receipts.
"""
import csv
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import unicodedata

import pymupdf as fitz
from PIL import Image, ImageDraw

REPORT = Path(__file__).resolve().parents[1]
ROOT = next(p for p in REPORT.parents if (p/'CLAUDE.md').exists())
SOURCE = ROOT/'research/oof-prioritization-2026-11-07'
ASSETS = REPORT/'assets/ch4'
OUT = REPORT/'build/review-prioritization-2026-11-07'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_csv(path):
    with Path(path).open() as f:
        return list(csv.DictReader(f))


def norm(text):
    return ' '.join(unicodedata.normalize('NFC',text).split())


def table_rows(name):
    lines = (ASSETS/name).read_text().splitlines()
    return [[cell.strip() for cell in line.removesuffix(r'\\').split('&')]
            for line in lines if '&' in line][1:]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--visual-reviewed',action='store_true',
        help='Record caller-attested visual inspection of the rendered pages; not inferred by this script.')
    args=parser.parse_args()
    manifest=json.loads((ASSETS/'priority-assets.json').read_text())
    assert sha(ASSETS/'build_prioritization_assets.py')==manifest['generator_sha256']
    for name,expected in manifest['sources'].items():
        p=SOURCE/name
        assert sha(p)==expected['sha256'] and p.stat().st_size==expected['bytes'],name
    for name,expected in manifest['generated'].items():
        p=ASSETS/name
        assert sha(p)==expected['sha256'] and p.stat().st_size==expected['bytes'],name
    d=json.loads((SOURCE/'results.json').read_text())
    independent=json.loads((SOURCE/'independent-validation.json').read_text())
    assert independent['status']=='pass'
    assert d['cohort']==dict(cells=122412,peptides=235,groups=221)
    names={'lora-D':'LoRA-D','ridge-w5-D':'Ridge W5-D','random':'Random expectation',
           'frozen-D':'Frozen-D','lora-B':'LoRA-B'}
    order=list(names)
    primary={r['policy']:r for r in d['primary_summary']}
    pct=lambda value:f'{100*float(value):.2f}'
    summary=read_csv(SOURCE/'summary.csv')
    minus={r['policy']:r for r in summary if r['prediction_set']=='ensemble'
           and r['direction']=='minus' and r['budget']=='k10'}
    expected=[]
    for policy in order:
        r=primary[policy]
        expected.append([names[policy],pct(r['precision']),
             f"{r['hits_total']:.2f}" if policy=='random' else f"{int(r['hits_total']):,}",
             pct(r['recall']),pct(minus[policy]['precision'])])
        assert r['peptides']==235 and r['groups']==221 and r['budget_total']==2350
        assert r['no_hit_peptides']==37 and r['recall_eligible_peptides']==198
    assert table_rows('tab-priority-main.tex')==expected
    expected=[]
    for contrast in d['primary_contrasts']:
        interval=lambda x:'$['+f'{100*x[0]:.2f}, {100*x[1]:.2f}'+']$'
        expected.append([names[contrast['baseline']],f"{100*contrast['delta']:+.2f}",
                         interval(contrast['ci95']),interval(contrast['ci_adjusted'])])
        assert contrast['replicates']==5000 and contrast['multiplicity']==2
    assert table_rows('tab-priority-contrasts.tex')==expected
    expected=[[names[p],f"{primary[p]['btr50']:.2f}",f"{primary[p]['btr80']:.2f}"]
              for p in order[:3]]
    assert table_rows('tab-priority-recall-budget.tex')==expected
    expected=[]
    for budget,label in [('k5','$k=5$'),('k10','$k=10$'),('k20','$k=20$'),
                         ('q05',r'Top 5\%'),('q10',r'Top 10\%'),('q20',r'Top 20\%')]:
        selected={r['policy']:r for r in summary if r['prediction_set']=='ensemble'
                  and r['direction']=='plus' and r['budget']==budget}
        expected.append([label,f"{int(selected['lora-D']['budget_total']):,}",
                         *[pct(selected[p]['precision']) for p in order]])
    assert table_rows('tab-priority-budgets.tex')==expected
    expected=[]
    for policy in order:
        if policy=='random':continue
        expected.append([names[policy],*[pct(next(r for r in d['per_seed_primary']
            if r['policy']==policy and r['prediction_set']==f'seed{s}')['precision'])
            for s in [17,29,43]],pct(primary[policy]['precision'])])
    assert table_rows('tab-priority-seeds.tex')==expected
    expected=[]
    strata=read_csv(SOURCE/'strata.csv')
    for key,label in [('le3',r'$\le3$'),('gt3_le4',r'$(3,4]$'),('gt4_le5',r'$(4,5]$'),('gt5',r'$>5$')]:
        selected={r['policy']:r for r in strata if r['stratum']=='psi_stratum'
                  and r['direction']=='plus' and r['value']==key}
        expected.append([label,selected['lora-D']['peptides'],selected['lora-D']['no_hit_peptides'],
                         pct(selected['lora-D']['precision']),pct(selected['ridge-w5-D']['precision'])])
    assert table_rows('tab-priority-strata.tex')==expected
    # Ensure original 88-row campaign record remains intact.
    old=json.loads((ROOT/'research/output-review-2026-11-06/results.json').read_text())
    old_table=(ASSETS/'tab-campaign-all.tex').read_text()
    assert sum(line.startswith(('Kaggle &','Local &')) for line in old_table.splitlines())==len(old['recipes'])==88
    mandatory=['Equal-Budget Retrospective Prioritisation',
               'Equal-Budget Retrospective Mutation Prioritisation',
               'Retrospective Prioritisation Sensitivity','53.62','46.26','9.78',
               '1,260','1,087','229.86','3.36','11.39','38.64','48.83',
               '71.32','81.99','255.51','154.36','170.53','404.48',
               '51.91','50.13','52.77','6,225','12,399','24,611']
    indicators=['Equal-Budget Retrospective Prioritisation',
                'Equal-Budget Retrospective Mutation Prioritisation',
                'Primary positive Precision@10 differences',
                'Positive-hit budget curves','Positive Precision@10 by WT-PSI stratum',
                'Retrospective Prioritisation Sensitivity',
                'Mean selections to reach a known positive-hit recall']
    forbidden=re.compile(r'Overfull \\[hv]box|Missing character:|multiply[ -]defined|undefined references|undefined citations|(?:Reference|Citation).*undefined',re.I)
    OUT.mkdir(parents=True,exist_ok=True)
    pdfs={}
    for folder in ['content','content-twoside']:
        path=REPORT/'build'/folder/'content.pdf'
        assert not forbidden.search(path.with_suffix('.log').read_text(errors='replace'))
        doc=fitz.open(path)
        texts=[norm(p.get_text()) for p in doc]
        combined='\n'.join(texts)
        for token in mandatory: assert token in combined,(folder,token)
        assert not re.search(r'output[/\\](?:local|official)|oof-prioritization-2026|results\.json|input-manifest\.json|build_prioritization_assets\.py',combined)
        assert all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc)
        abstracts={}
        for language,heading,keyword in [('english','ABSTRACT','Keywords:'),('vietnamese','TÓM TẮT','Từ khóa:')]:
            found=[i for i,t in enumerate(texts) if t.startswith(heading+' ')]
            assert len(found)==1,(folder,language,found)
            i=found[0]
            assert re.sub(r'\s+','',keyword) in re.sub(r'\s+','',texts[i]),(folder,language,'abstract spills onto another page')
            assert all(value in texts[i] for value in ['53.62','46.26','9.78','173','3.36','11.39'])
            abstracts[language]=i+1
        fonts={};links=0;annotations=0
        for p in doc:
            for font in p.get_fonts(full=True):
                if font[0] and font[0] not in fonts:
                    name,ext,kind,data=doc.extract_font(font[0]);assert data,(folder,name)
                    fonts[font[0]]=name
            for link in p.get_links():
                if link['kind']==fitz.LINK_GOTO:
                    assert 0<=link['page']<len(doc),(folder,p.number,link)
                    links+=1
            annotations+=len(list(p.annots() or []))
        assert any('TimesNewRoman' in name.replace(' ','') for name in fonts.values())
        detail=set(abstracts.values())
        for i,text in enumerate(texts):
            if i>18 and any(token in text for token in indicators):
                detail.update(range(max(1,i),min(len(doc),i+3)+1))
            if text.startswith('RESEARCH PROGRESS STATUS '):detail.add(i+1)
            if 'same-budget retrospective replay directly tests mutation prioritisation' in text:detail.add(i+1)
        for n in sorted(detail):
            doc[n-1].get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).save(OUT/f'{folder}-page-{n:03}.png')
        sheets=[]
        selected=sorted(detail)
        for start in range(0,len(selected),12):
            sheet=Image.new('RGB',(4*260,3*385),'#dddddd')
            draw=ImageDraw.Draw(sheet)
            for offset,n in enumerate(selected[start:start+12]):
                pix=doc[n-1].get_pixmap(matrix=fitz.Matrix(.39,.39),alpha=False)
                im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
                x=(offset%4)*260;y=(offset//4)*385
                sheet.paste(im,(x+10,y+25));draw.text((x+10,y+7),f'{folder}, PDF page {n}',fill='black')
            destination=OUT/f'{folder}-contact-{start//12+1:02}.png'
            sheet.save(destination);sheets.append(destination.relative_to(REPORT).as_posix())
        pdfs[folder]=dict(sha256=sha(path),bytes=path.stat().st_size,pages=len(doc),
            all_A4=True,all_fonts_embedded=True,embedded_font_names=sorted(set(fonts.values())),
            abstracts_one_page_each=abstracts,new_result_tokens_found=mandatory,
            internal_link_destinations_checked=links,nonlink_annotations=annotations,
            pending_markers=combined.count('[PENDING'),detail_pages=selected,contact_sheets=sheets)
    record=dict(status='pass' if args.visual_reviewed else 'pass_automated_checks_visual_review_pending',
        checked_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
        source_result_sha256=sha(SOURCE/'results.json'),source_independent_validation_sha256=sha(SOURCE/'independent-validation.json'),
        asset_manifest_sha256=sha(ASSETS/'priority-assets.json'),
        generated_asset_count=len(manifest['generated']),generated_tables_checked=6,
        historical_campaign_rows_retained=88,pdfs=pdfs,
        report_source_hashes={str(p.relative_to(REPORT)):sha(p) for p in sorted([
            REPORT/'main.tex',REPORT/'README.md',REPORT/'assets/README.md',
            *list((REPORT/'chapters').rglob('*.tex')),
            *list((REPORT/'frontmatter').glob('*.tex')),
            REPORT/'appendices/b-supplementary-materials.tex',Path(__file__)])},
        scope='Report integration, source values and rendered artifacts only; no new model evaluation or wet lab.',
        visual_review=dict(status='caller_attested' if args.visual_reviewed else 'pending',
            meaning='Primary Codex session inspected contact sheets and new table/figure detail pages in both variants; no human attestation inferred.'),
        limitations=['Automated checks alone do not establish visual readability; --visual-reviewed records a caller attestation.',
            'Native helper completed a wording-scope audit; its final report-review pass was unavailable due to usage limit. Final check performed in the primary session.'])
    build_receipt=OUT/'build-receipt.json'
    if build_receipt.exists():
        receipt=json.loads(build_receipt.read_text())
        assert receipt['exit_code']==0,receipt
        record['build_receipt']=receipt
    acronym=OUT/'phase4_update/acronyms.json'
    if acronym.exists():
        advisory=json.loads(acronym.read_text())
        record['acronym_advisory']=dict(path=str(acronym.relative_to(REPORT)),
            sha256=sha(acronym),status=advisory['status'],coverage=advisory.get('coverage'),
            limitation='Scoped extracted draft only; Vietnamese unsupported; glossary/earlier body definitions omitted. WT and LoRA definition-shape warnings reviewed manually.')
    (REPORT/'prioritization-validation-2026-11-07.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=record['status'],pdfs={k:dict(pages=v['pages'],detail_pages=v['detail_pages']) for k,v in pdfs.items()}),indent=2))


if __name__=='__main__':
    main()
