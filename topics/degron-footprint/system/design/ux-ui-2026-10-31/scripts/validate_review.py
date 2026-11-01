"""Browser/render checks for the design artifact, not the application.

Run with a Python environment containing playwright and Pillow. The browser
executable can be selected by --browser; no Figma tools are called.
"""
import argparse
import asyncio
import json
from pathlib import Path
from collections import Counter
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent.parent

def walk(n):
    yield n
    for c in n['children']:
        yield from walk(c)

def geometry(n,screen,issues,scroll=False):
    scrolling=scroll or n.get('scrollX',False)
    for c in n['children']:
        if not scrolling and (c['x'] < -2 or c['x']+c['width'] > n['width']+3):
            issues.append({'screen':screen,'parent':n['name'],'child':c['name'],'type':'horizontal overflow','right':round(c['x']+c['width']-n['width'],2)})
        if c['y'] < -2 or c['y']+c['height'] > n['height']+3:
            issues.append({'screen':screen,'parent':n['name'],'child':c['name'],'type':'vertical overflow','bottom':round(c['y']+c['height']-n['height'],2)})
        geometry(c,screen,issues,scrolling)

async def main(args):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=args.browser,headless=True,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1600,'height':1100},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        await page.goto(args.url)
        await page.wait_for_function('window.reviewReady === true')
        await page.evaluate('document.fonts.ready')
        data=await page.evaluate('window.exportDesign()')
        (ROOT/'design-spec.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
        issues=[]; all_ids={s['id'] for s in data['screens']}; unresolved=[]; counts=Counter(); matrix_counts={}; small_controls=[]
        for s in data['screens']:
            geometry(s['node'],s['id'],issues)
            nodes=list(walk(s['node']))
            counts.update(n['type'] for n in nodes)
            scored=[n for n in nodes if n['name'].startswith('Cell / ')]
            wt=[n for n in nodes if n['name'].startswith('WT / ')]
            if scored or wt:matrix_counts[s['id']]={'scored':len(scored),'wt':len(wt),'rows':len([n for n in nodes if n['name'].startswith('Position ')])}
            unresolved += [{'screen':s['id'],'target':n['target']} for n in nodes if n['target'] and n['target'] not in all_ids]
            small_controls += [{'screen':s['id'],'name':n['name'],'height':n['height']} for n in nodes if n['role'] and n['role'].startswith('Button/') and n['height']<44]
        await page.locator('#screen-select').select_option('DF03')
        await page.get_by_role('button',name='Predict 532 substitutions',exact=True).click()
        await page.wait_for_function("location.hash==='#DF18'")
        custom_path=await page.locator('#screen-name').inner_text()
        await page.locator('#screen-select').select_option('DF09')
        first=page.locator('#canvas [role=gridcell]').first
        await first.focus();await page.keyboard.press('ArrowRight')
        keyboard=await page.evaluate("document.activeElement.getAttribute('role')==='gridcell'")
        screenshots=ROOT/'previews';screenshots.mkdir(exist_ok=True)
        # Remove review chrome for artifact screenshots, preserving product layers.
        await page.add_style_tag(content='.review-bar,.review-heading,#cell-status{display:none!important}.stage{padding:0!important}#canvas{margin:0!important;box-shadow:none!important}')
        for screen in args.capture.split(','):
            await page.locator('#screen-select').select_option(screen,force=True)
            await page.wait_for_timeout(60)
            await page.evaluate("document.querySelector('#canvas').firstElementChild.style.transform='none'")
            await page.locator('#canvas > .artboard').screenshot(path=str(screenshots/f'{screen.lower()}.png'))
        report={'scope':'Local design review only; no Figma-native or application acceptance claimed','screens':len(data['screens']),'by_group':dict(Counter('desktop' if s['id'].startswith('DF') else 'state' if s['id'].startswith('ST') else 'mobile' if s['id'].startswith('M') else 'direction' for s in data['screens'])),'node_types':dict(counts),'matrix_counts':matrix_counts,'console_errors':errors,'geometry_issues':issues,'unresolved_targets':unresolved,'button_targets_below_44px':small_controls,'custom_input_route':custom_path,'matrix_keyboard_arrow':keyboard,'fonts_loaded':await page.evaluate("document.fonts.check('400 14px Roboto')&&document.fonts.check('400 13px \"Roboto Mono\"')"),'screenshots':[f'previews/{x.name}' for x in sorted(screenshots.glob('*.png'))]}
        (ROOT/'review-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='screenshots'},ensure_ascii=False))
        await browser.close()

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--url',default='http://127.0.0.1:8877/review.html');ap.add_argument('--browser',required=True);ap.add_argument('--capture',default='DF01,DF03,DF04,DF07,DF09,DF11,DF13,DF15,DF19,M02,M03,UX01');asyncio.run(main(ap.parse_args()))
