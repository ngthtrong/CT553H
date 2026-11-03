"""Browser, media, PDF, evidence and annotation checks for this deck."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import sys
from PIL import Image, ImageDraw, ImageFont
import pymupdf
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
PREVIEWS=HERE/'previews'
PREVIEWS.mkdir(exist_ok=True)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

errors=[];network=[];failed=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport=dict(width=1440,height=900),device_scale_factor=1,offline=True)
    page=context.new_page()
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('requestfailed',lambda r:failed.append(dict(url=r.url,error=r.failure)))
    page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto((HERE/'index.html').as_uri())
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(200)
    counts=page.evaluate('({main:DECK.mainCount,total:DECK.total})')
    page.evaluate("document.body.classList.add('motion-paused')")
    results=[]
    for i in range(counts['total']):
        page.evaluate('(i)=>DECK.show(i,true)',i)
        page.wait_for_timeout(70)
        r=page.evaluate('''() => {
          const s=document.querySelector('.slide.active'),body=s.querySelector('.body'),b=s.getBoundingClientRect(),bb=body.getBoundingClientRect(),issues=[];
          const visible=e=>{const c=getComputedStyle(e),r=e.getBoundingClientRect();return c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity!==0&&r.width>0&&!e.closest('.speaker-notes,.print-fallback');};
          for(const e of s.querySelectorAll('h1,h2,h3,p,.insight,.context,.table,td,th,svg text,.big-number,.pipeline-ending,.workflow')){
            if(!visible(e))continue;const r=e.getBoundingClientRect(),limit=body.contains(e)?bb:b;
            if(r.left<limit.left-1.5||r.right>limit.right+1.5||r.top<limit.top-1.5||r.bottom>limit.bottom+1.5)issues.push({text:e.textContent.slice(0,100),tag:e.tagName,rect:{x:r.x,y:r.y,w:r.width,h:r.height},limit:{x:limit.x,y:limit.y,w:limit.width,h:limit.height}});
          }
          const imgs=[...s.querySelectorAll('img')].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.getAttribute('src'));
          const displayText=[...s.querySelectorAll('header,.body,.insight')].map(e=>e.innerText).join(' ');
          return {title:s.dataset.title,layoutIssues:issues,brokenImages:imgs,forbidden:/data\\s+v[123]\\b|six-session learning roadmap/i.test(displayText),visibleTextLength:displayText.length};
        }''')
        r['slide']=i+1;results.append(r)
        page.locator('#deck').screenshot(path=str(PREVIEWS/f'slide-{i+1:02}.png'),animations='disabled')

    # Test steps, skip navigation, overview, notes and normal keyboard interaction.
    page.evaluate('DECK.show(3)');page.keyboard.press('ArrowRight')
    step_works=page.evaluate('DECK.index===3 && DECK.step===1')
    page.keyboard.press('Shift+ArrowRight')
    skip_works=page.evaluate('DECK.index===4')
    page.locator('#overview-button').click();overview=page.locator('#overview-grid button').count()
    page.locator('#overview-grid button').nth(22).click()
    overview_jump=page.evaluate('DECK.index===22')
    page.locator('#notes-button').click();notes_work=len(page.locator('#notes-body').inner_text())>100
    page.keyboard.press('Escape')
    page.locator('[data-metric="ap"]').click()
    chart_works=page.evaluate('Chart.getChart(document.getElementById("recipeChart")).data.datasets[0].data[0]===DECK_DATA.explorer[0].ap')
    page.locator('[data-metric="mae"]').click()
    # Motion and real media need a separate unpaused check.
    page.evaluate("document.body.classList.remove('motion-paused');DECK.show(2,true)")
    video=page.locator('video')
    page.wait_for_timeout(1200)
    video_info=video.evaluate('(v)=>({readyState:v.readyState,width:v.videoWidth,height:v.videoHeight,duration:v.duration,time:v.currentTime,error:v.error?.message||null})')
    page.locator('#motion').click()
    media_paused=video.evaluate('(v)=>v.paused')
    css_paused=page.evaluate("document.getAnimations().filter(a=>a.playState==='running').length===0")
    page.emulate_media(reduced_motion='reduce')
    reduced_media=page.evaluate("getComputedStyle(document.querySelector('video')).display==='none' && getComputedStyle(document.querySelector('.video-print')).display!=='none'")
    page.evaluate('DECK.show(1,true)')
    reduced_gif=page.evaluate("getComputedStyle(document.querySelector('.animated-gif')).display==='none'")
    screens=[]
    for width,height in [(1280,720),(1920,1080),(390,844),(844,390)]:
        page.set_viewport_size(dict(width=width,height=height));page.evaluate('DECK.resize();DECK.show(6,true)')
        page.wait_for_timeout(50)
        screens.append(page.evaluate('''() => {const r=document.querySelector('#deck').getBoundingClientRect();return {width:innerWidth,height:innerHeight,documentOverflow:document.documentElement.scrollWidth>innerWidth,deckFits:r.left>=-1&&r.right<=innerWidth+1&&r.top>=-1&&r.bottom<=innerHeight+1};}'''))
    links=page.evaluate("[...document.querySelectorAll('a[href]')].map(e=>e.getAttribute('href')).filter(u=>!/^https?:|^#/.test(u))")
    broken_links=sorted(set(u for u in links if not (HERE/u).exists()))
    page.set_viewport_size(dict(width=1280,height=780))
    page.emulate_media(media='print',reduced_motion='reduce')
    print_canvas_hidden=page.locator('#recipeChart').evaluate("e=>getComputedStyle(e).display==='none'")
    print_fragments_visible=page.evaluate("[...document.querySelectorAll('.fragment.future')].every(e=>getComputedStyle(e).visibility==='visible')")
    page.pdf(path=str(HERE/'slides.pdf'),prefer_css_page_size=True,print_background=True,display_header_footer=False)
    browser.close()

pdf=pymupdf.open(HERE/'slides.pdf')
pdf_pages=[dict(page=i+1,characters=len(p.get_text().strip()),width=p.rect.width,height=p.rect.height) for i,p in enumerate(pdf)]
pdf_ok=len(pdf)==36 and all(p['characters']>80 and abs(p['width']/p['height']-16/9)<.01 for p in pdf_pages)
font=ImageFont.truetype(str(HERE/'vendor/be-vietnam-pro-regular.ttf'),16)
for group,start,end in [('main',0,31),('appendix',31,36)]:
    columns=4;tilew=400;tileh=250;rows=(end-start+columns-1)//columns
    sheet=Image.new('RGB',(columns*tilew,rows*tileh),'#dfe5dc');draw=ImageDraw.Draw(sheet)
    for j,i in enumerate(range(start,end)):
        im=Image.open(PREVIEWS/f'slide-{i+1:02}.png');im.thumbnail((388,218))
        xx=(j%columns)*tilew+6;yy=(j//columns)*tileh+6;sheet.paste(im,(xx,yy));draw.text((xx,yy+220),f'{i+1:02} · {results[i]["title"][:38]}',font=font,fill='#193a2b')
    sheet.save(PREVIEWS/f'contact-{group}.png')

reuse=json.loads((HERE/'reuse-manifest.json').read_text())
old=HERE/reuse['source']
old_unchanged=all((old/name).exists() and digest(old/name)==sha for name,sha in reuse['source_files_sha256'].items())
evidence=json.loads((HERE/'evidence.json').read_text())
topic=next(p for p in HERE.parents if (p/'data/README.md').exists())
evidence_ok=all(digest(topic/name)==sha for name,sha in evidence['source_sha256'].items())
asset_ok=all(digest(HERE/name)==sha for name,sha in evidence['asset_sha256'].items())
localization_hashes=all(digest(HERE/name)==sha for name,sha in evidence['localization_sources'].items())
VI=re.compile('[ăâđêôơưĂÂĐÊÔƠƯ\u1ea0-\u1ef9]')
class LanguageCheck(HTMLParser):
    def __init__(self):super().__init__();self.remaining=[]
    def inspect(self,value):
        cleaned=value.replace('Nguyễn Thanh Trọng','').replace('Hồ Quang Thái','')
        if VI.search(cleaned):self.remaining.append(value)
    def handle_data(self,value):self.inspect(value)
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if value and key in ['alt','aria-label','data-title','data-section']:self.inspect(value)
language=LanguageCheck();language.feed((HERE/'index.html').read_text())
language.inspect((HERE/'deck.js').read_text())
for f in (HERE/'assets').glob('*.svg'):
    svg_language=LanguageCheck();svg_language.feed(f.read_text());language.remaining.extend(svg_language.remaining)
html_language='lang="en"' in (HERE/'index.html').read_text()
source=HERE/'../deck-explained-2026-11-03'
def payload(p):return json.loads(p.read_text().split('=',1)[1].strip().rstrip(';'))
src_data=payload(source/'data.js')['explorer'];en_data=payload(HERE/'data.js')['explorer']
numeric_parity=[{k:v for k,v in r.items() if k!='name'} for r in src_data]==[{k:v for k,v in r.items() if k!='name'} for r in en_data]
src_slides=json.loads((source/'slide-sources.json').read_text());en_slides=json.loads((HERE/'slide-sources.json').read_text())
source_parity=[(r['number'],r['sources'],r['appendix']) for r in src_slides]==[(r['number'],r['sources'],r['appendix']) for r in en_slides]
notes_complete=len(en_slides)==36 and all(len(r['notes'])>100 for r in en_slides)
original_analysis=json.loads((topic/'research/kaggle-roadmap-2026-10-31/output-analysis.json').read_text())
original_details=json.loads((topic/'research/kaggle-roadmap-2026-10-31/output-analysis-details.json').read_text())
figures=json.loads((HERE/'figure-data.json').read_text())
def m(recipe):return original_analysis['recipes'][recipe]['ensemble']['all']['mae']
figure_parity=(figures['training-range']['values']==[m('ordered-w5-'+s) for s in 'ABCDE'] and
               figures['transfer']['values']==[m(s) for s in ['cnn-transfer-scratch-D','cnn-transfer-dpsi_rep1-D','cnn-transfer-dpsi_rep12_mean-D']] and
               figures['mcnn-ci']['values']['ci95']==original_details['contrasts']['esm2_35m-mcnn-E minus esm2_35m-cnn-D; mae']['ci95'] and
               figures['hif-measured']['values']['valid_cells']==529)
for arm in 'BDE':
    figure_parity=figure_parity and figures['strata']['values'][arm]==[original_analysis['recipes']['ordered-w5-'+arm]['ensemble']['strata'][s]['mae'] for s in ['le3','gt3_le4','gt4_le5','gt5']]
media_parity=all(digest(HERE/'assets'/n)==digest(source/'assets'/n) for n in ['fam188a.gif','fam188a-poster.png','proteasome.mp4','proteasome-poster.jpg','workspace-prototype.png','zhang-graphical-abstract.png'])
problem_slides=[r for r in results if r['layoutIssues'] or r['brokenImages'] or r['forbidden']]
# Chromium may cancel a video range request on navigation. A successfully decoded,
# advancing movie distinguishes that cancellation from a broken media resource.
cancelled_media=[r for r in failed if r['error']=='net::ERR_ABORTED' and r['url'].endswith('/assets/proteasome.mp4') and video_info['readyState']>=2 and video_info['time']>0 and not video_info['error']]
load_failures=[r for r in failed if r not in cancelled_media]
report=dict(pass_=False,counts=counts,slides=results,script_errors=errors,failed_requests=load_failures,cancelled_media_requests=cancelled_media,external_requests=network,
            broken_links=broken_links,step_navigation=step_works,skip_navigation=skip_works,overview_count=overview,
            overview_jump=overview_jump,notes=notes_work,chart=chart_works,video=video_info,media_paused=media_paused,
            css_paused=css_paused,reduced_media=reduced_media,reduced_gif=reduced_gif,screens=screens,pdf_pages=pdf_pages,
            print_canvas_hidden=print_canvas_hidden,print_fragments_visible=print_fragments_visible,
            language='en',remaining_vietnamese=language.remaining,html_language=html_language,numeric_parity=numeric_parity,
            source_parity=source_parity,notes_complete=notes_complete,figure_parity=figure_parity,media_parity=media_parity,localization_hashes_match=localization_hashes,
            old_deck_unchanged=old_unchanged,evidence_hashes_match=evidence_ok,asset_hashes_match=asset_ok)
report['pass']=all([counts==dict(main=31,total=36),not problem_slides,not errors,not load_failures,not network,not broken_links,
                    step_works,skip_works,overview==36,overview_jump,notes_work,chart_works,
                    video_info['readyState']>=2,video_info['time']>0,not video_info['error'],
                    media_paused,css_paused,reduced_media,reduced_gif,print_canvas_hidden,print_fragments_visible,pdf_ok,old_unchanged,evidence_ok,asset_ok,
                    not language.remaining,html_language,numeric_parity,source_parity,notes_complete,figure_parity,media_parity,localization_hashes,
                    all(not s['documentOverflow'] and s['deckFits'] for s in screens)])
del report['pass_']
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:report[k] for k in ['pass','counts','script_errors','failed_requests','broken_links','video','old_deck_unchanged','evidence_hashes_match']},ensure_ascii=False,indent=2))
print('Problem slides:',json.dumps(problem_slides,ensure_ascii=False))
sys.exit(0 if report['pass'] else 1)
