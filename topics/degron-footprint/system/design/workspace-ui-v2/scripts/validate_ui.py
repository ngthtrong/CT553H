"""Verify the local design prototype, not backend/scientific acceptance.

Requires an existing Python environment with Playwright and an existing browser.
Run a loopback HTTP server for the prototype before invoking this script.
"""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parent.parent

async def validate(args):
    report = {'scope': 'Interactive UI design review only; synthetic data, no model/backend acceptance',
              'date': '2026-11-01', 'checks': [], 'console_errors': [], 'screenshots': [], 'accessibility': []}
    def check(name, condition, detail=None):
        report['checks'].append({'name': name, 'passed': bool(condition), 'detail': detail})
        assert condition, f'{name}: {detail}'
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=args.browser, headless=True, args=['--no-sandbox'])
        report['environment'] = {'browser': browser.version, 'engine': 'Chromium',
                                 'desktop_viewport': {'width':1440,'height':1050},
                                 'responsive_widths':[360,768,1280], 'local_only':True}
        report['tested_ui_sha256'] = {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                     for name in ['index.html','tokens.css','styles.css','fixtures.js','app.js']}
        context = await browser.new_context(viewport={'width':1440,'height':1050}, color_scheme='light', accept_downloads=True)
        axe = ROOT.parents[1]/'app/frontend/node_modules/axe-core/axe.min.js'
        if axe.exists():
            await context.add_init_script(path=str(axe))
        page = await context.new_page()
        page.on('pageerror', lambda error: report['console_errors'].append(str(error)))
        async def visit(path):
            await page.goto(args.url+'#'+path)
            await page.locator('main h1').wait_for()
            await page.evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
            await page.evaluate('document.fonts.ready')
        async def capture(name):
            hidden_toast=await page.add_style_tag(content='#toast{visibility:hidden!important}')
            await page.screenshot(path=str(ROOT/'previews'/name),full_page=True)
            await hidden_toast.evaluate('e=>e.remove()')
            report['screenshots'].append('previews/'+name)
        async def audit(name):
            if not axe.exists():
                report['accessibility'].append({'page':name,'status':'not run; axe-core not available'})
                return
            result = await page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>n.target)})),incomplete:r.incomplete.length};}")
            report['accessibility'].append({'page':name,**result})
            check('axe '+name, not result['violations'], result['violations'])
        try:
            await visit('/analyses/a-demo')
            check('matrix cell contract',await page.locator('[data-cell]').count()==532 and await page.locator('[data-wt]').count()==28)
            before=await page.evaluate("Boolean(document.querySelector('.notice').compareDocumentPosition(document.querySelector('[role=grid]'))&Node.DOCUMENT_POSITION_FOLLOWING)")
            check('domain warning precedes scores',before)
            await capture('result-light.png')
            await audit('result-light')
            first=page.locator('[data-cell][tabindex="0"]')
            original=await first.get_attribute('data-cell')
            await first.focus()
            await page.keyboard.press('ArrowRight')
            check('matrix keyboard navigation',await page.locator('[data-cell][tabindex="0"]').get_attribute('data-cell')!=original)
            await page.get_by_role('button',name='Add to shortlist',exact=True).click()
            check('shortlist adds selected substitution',(await page.evaluate('footprintReview.counts.shortlist'))==1)
            await page.get_by_role('button',name='Ranking',exact=False).first.click()
            await page.locator('#position-filter').select_option('1')
            await page.locator('#amino-filter').select_option('D')
            check('WT substitution is excluded',await page.get_by_text('No substitutions match.',exact=True).count()==1)
            await page.get_by_role('button',name='Clear filters',exact=True).click()
            await capture('ranking.png')
            await page.get_by_role('button',name='Export',exact=True).click()
            async with page.expect_download() as d:
                await page.get_by_role('button',name='JSON + provenance',exact=True).click()
            payload=json.loads(Path(await (await d.value).path()).read_text())
            check('export is complete and labelled',len(payload['cells'])==532 and payload['fixture'] and payload['domain']=='unknown' and 'no model inference' in payload['disclaimer'].lower())
            await page.get_by_role('button',name='Save as new snapshot',exact=True).click()
            await page.locator('#save-name').fill('Review snapshot')
            await page.get_by_role('button',name='Save snapshot',exact=True).click()
            check('save creates a separate snapshot',(await page.evaluate('footprintReview.counts.analyses'))==2)
            await page.get_by_role('button',name='Run again',exact=True).click()
            check('rerun leaves saved history intact',(await page.evaluate('footprintReview.counts.analyses'))==2 and page.url.endswith('#/result'))
            await visit('/projects/p-col6a6')
            await capture('project-history.png')
            await audit('project-history')
            await visit('/projects/p-empty')
            await visit('/analyses/a-demo')
            check('snapshot restores its own project context','COL6A6 exploration' in await page.locator('.breadcrumbs').inner_text())
            await visit('/projects')
            await capture('projects.png')
            await page.get_by_role('button',name='Create project',exact=True).first.click()
            await page.locator('#project-name').fill('Review project')
            await page.get_by_role('button',name='Create project',exact=True).last.click()
            await page.get_by_text('No analyses yet',exact=True).wait_for()
            check('project creation and empty state',await page.get_by_text('No analyses yet',exact=True).count()==1)
            await visit('/new')
            await page.locator('#sequence').fill('B'*28)
            await page.get_by_role('button',name='Preview substitutions',exact=True).click()
            check('invalid alphabet blocks result',await page.locator('#sequence-error').inner_text()!='' and page.url.endswith('#/new'))
            await page.locator('#sequence').fill(' dimflvdssgsigpenfskmktfmknlv ')
            await page.get_by_role('button',name='Preview substitutions',exact=True).click()
            await page.get_by_role('heading',name='Custom peptide',exact=True).wait_for()
            check('case and surrounding whitespace normalize',await page.get_by_role('heading',name='Custom peptide',exact=True).count()==1)
            await page.get_by_role('button',name='ClinVar',exact=True).click()
            check('unmapped input has mapping unavailable',await page.get_by_text('Mapping unavailable',exact=True).count()>=1)
            check('input is absent from URL and browser storage','DIMFLV' not in page.url.upper() and await page.evaluate('localStorage.length===0 && sessionStorage.length===0'))
            await visit('/new')
            await capture('new-analysis.png')
            await audit('new-analysis')
            await page.locator('#reference-query').fill('COL6A6')
            await page.get_by_role('button',name='Search reference example',exact=True).click()
            await page.locator('.tile-button').first.wait_for()
            check('reference tile geometry',await page.locator('.tile-button').count()==98 and await page.get_by_text('Uncovered C terminus: 2260–2263 (4 residues)',exact=True).count()==1)
            await capture('protein-tiles.png')
            await visit('/new')
            await page.get_by_role('button',name='Peptide batch',exact=False).click()
            await page.get_by_role('button',name='Load example',exact=True).click()
            await page.get_by_role('button',name='Validate & preview',exact=True).click()
            check('batch requires a project',await page.locator('#input-error').inner_text()=='Choose a project before validating this job.')
            await page.locator('#job-project').select_option('p-col6a6')
            await page.get_by_role('button',name='Validate & preview',exact=True).click()
            check('batch preview retains invalid records',await page.get_by_text('3 items · 2 syntactically valid · 1 invalid',exact=True).count()==1)
            await capture('batch-preview.png')
            await page.locator('#job-consent').check()
            await page.get_by_role('button',name='Submit preview job',exact=True).click()
            await expect(page.locator('main [role=status]')).to_contain_text('partial')
            await capture('job-partial.png')
            async with page.expect_download() as d:
                await page.get_by_role('button',name='Export manifest',exact=True).click()
            manifest=json.loads(Path(await (await d.value).path()).read_text())
            check('partial job manifest reconciles',len(manifest['items'])==3 and sum(x['status']=='succeeded' for x in manifest['items'])==2 and sum(x['status']=='failed' for x in manifest['items'])==1)
            await visit('/new')
            await page.get_by_role('button',name='Whole protein',exact=False).click()
            await page.locator('#job-project').select_option('p-col6a6')
            await page.locator('#protein-input').fill('>synthetic-80-residue-protein\n'+'ACDEFGHIKLMNPQRSTVWY'*4)
            await page.get_by_role('button',name='Validate & preview',exact=True).click()
            check('whole protein retains terminal gap',await page.get_by_text('80 residues · 3 full windows · uncovered terminal residues: 6 (75–80)',exact=True).count()==1)
            await page.locator('#job-consent').check()
            await page.get_by_role('button',name='Submit preview job',exact=True).click()
            await page.get_by_role('button',name='Cancel job…',exact=True).click()
            await page.get_by_role('button',name='Cancel job',exact=True).click()
            check('job cancellation is terminal',await page.get_by_text('cancelled',exact=True).count()>=1 and await page.locator('main [role=status]').inner_text()!='')
            await visit('/import')
            await page.locator('#import-project').select_option('p-col6a6')
            await page.locator('#dataset-name').fill('Review observations')
            await page.locator('#assay-name').fill('GPS v1')
            await page.locator('#dataset-source').fill('Synthetic interface test; not experimental evidence')
            seq='DIMFLVDSSGSIGPENFSKMKTFMKNLV'
            header='peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id,missing_reason\n'
            duplicate=(header+f'one,{seq},14,P,W,1.12,rep-1,\ntwo,{seq},14,P,W,2.1,rep-1,\n').encode()
            await page.locator('#import-file').set_input_files({'name':'duplicate.csv','mimeType':'text/csv','buffer':duplicate})
            await page.get_by_role('button',name='Validate file',exact=True).click()
            await page.wait_for_selector('#ack-import')
            check('duplicate import blocks commit',await page.get_by_role('button',name='Commit dataset',exact=True).is_disabled())
            await capture('import-errors.png')
            valid=(header+f'one,{seq},14,P,W,1.12,rep-1,\ntwo,{seq},17,F,A,0.47,rep-1,\nthree,{seq},11,S,L,-0.28,rep-1,\nfour,{seq},19,K,R,,rep-1,not measured\n').encode()
            await page.locator('#import-file').set_input_files({'name':'observations.csv','mimeType':'text/csv','buffer':valid})
            await page.get_by_role('button',name='Validate file',exact=True).click()
            await page.wait_for_selector('#ack-import')
            check('source-file hash is correct',await page.get_by_text('SHA-256: '+hashlib.sha256(valid).hexdigest(),exact=True).count()==1)
            await capture('import-validation.png')
            await audit('import-validation')
            await page.locator('#ack-import').check()
            await page.get_by_role('button',name='Commit dataset',exact=True).click()
            await page.get_by_role('heading',name='Review observations',exact=True).wait_for()
            check('commit creates one dataset',await page.get_by_role('heading',name='Review observations',exact=True).count()==1 and await page.evaluate('footprintReview.counts.datasets')==2)
            await page.get_by_role('button',name='Compare with analysis',exact=True).click()
            await page.get_by_role('heading',name='Prediction & observation',exact=True).wait_for()
            check('comparison distinguishes missing observations',await page.get_by_text('matched numeric pairs',exact=True).count()==1 and 'n=3' in await page.locator('.stat-strip').inner_text() and 'missing measurements' in await page.locator('.stat-strip').inner_text())
            await capture('comparison.png')
            await audit('comparison')
            await page.get_by_role('button',name='Review states',exact=False).click()
            await page.get_by_role('button',name='Out-of-domain refusal',exact=True).click()
            check('refusal hides all scores',await page.locator('[data-cell]').count()==0)
            await page.get_by_role('button',name='Score anyway…',exact=True).click()
            await page.get_by_role('button',name='Confirm override',exact=True).click()
            check('explicit override carries warning',await page.get_by_text('Out-of-domain override · illustrative scenario',exact=True).count()==1 and await page.locator('[data-cell]').count()==532)
            await capture('domain-override.png')
            await page.get_by_role('button',name='Review states',exact=False).click()
            await page.get_by_role('button',name='Source not loaded',exact=True).click()
            check('ClinVar source unavailable is explicit',await page.get_by_text('Source not loaded',exact=True).count()>=1)
            await capture('clinvar-unavailable.png')
            await page.get_by_role('button',name='Review states',exact=False).click()
            await page.get_by_role('button',name='Unknown domain',exact=True).click()
            await page.get_by_role('button',name='Switch color theme',exact=True).click()
            await capture('result-dark.png')
            await audit('result-dark')
            for size in [360,768,1280]:
                mobile=await context.new_page()
                await mobile.set_viewport_size({'width':size,'height':950})
                mobile.on('pageerror',lambda error:report['console_errors'].append(str(error)))
                await mobile.goto(args.url+'#/analyses/a-demo')
                await mobile.locator('main h1').wait_for()
                width=await mobile.evaluate('document.documentElement.scrollWidth')
                check(f'no page overflow at {size}px',width<=size,{'scrollWidth':width,'viewport':size})
                if size==360:
                    check('mobile starts with ranking',await mobile.locator('#position-filter').count()==1)
                    mutation=await mobile.locator('[data-action=select-rank]').first.bounding_box()
                    check('mobile exposes substitution identity without scrolling',mutation['x']>=0 and mutation['x']+mutation['width']<=size,mutation)
                    await mobile.screenshot(path=str(ROOT/'previews/mobile-ranking.png'),full_page=True)
                    report['screenshots'].append('previews/mobile-ranking.png')
                    await mobile.get_by_role('button',name='Toggle navigation',exact=True).click()
                    check('mobile navigation opens',await mobile.locator('body').evaluate("e=>e.classList.contains('nav-open')"))
                if size==1280:
                    rect=await mobile.locator('[data-cell] rect').first.bounding_box()
                    check('matrix cells at least 24px at 1280px',rect['width']>=24 and rect['height']>=24,rect)
                await mobile.close()
            offline=await context.new_page()
            await offline.goto((ROOT/'index.html').as_uri())
            await offline.locator('[data-cell]').first.wait_for()
            await offline.evaluate('document.fonts.ready')
            check('opens directly as a local file',await offline.locator('[data-cell]').count()==532)
            check('bundled fonts load offline',await offline.evaluate('document.fonts.check(\'400 14px Roboto\') && document.fonts.check(\'400 12px "Roboto Mono"\')'))
            await offline.close()
            check('no JavaScript exceptions',not report['console_errors'],report['console_errors'])
            report['passed']=True
        except Exception as e:
            report['passed']=False
            report['failure']=str(e)
            await page.screenshot(path=str(ROOT/'previews/validation-failure.png'),full_page=True)
            raise
        finally:
            (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
            print(json.dumps({k:v for k,v in report.items() if k not in ('screenshots','accessibility')},ensure_ascii=False))
            await browser.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--url',default='http://127.0.0.1:8891/')
    parser.add_argument('--browser',required=True)
    asyncio.run(validate(parser.parse_args()))
