"""Build the offline review without changing the application or calling Figma."""
from pathlib import Path
import json
import base64

ROOT = Path(__file__).resolve().parent.parent

def main():
    config = json.loads((ROOT / 'authoring-config.json').read_text())
    first = (ROOT / 'scripts/03-workspace-analysis.js').read_text().split('// Read-back evidence')[0]
    source = '\n'.join([
        "await Promise.all(['400 14px Roboto','500 14px Roboto','400 13px \"Roboto Mono\"'].map(f=>document.fonts.load(f)));",
        'const CONFIG=' + json.dumps(config, ensure_ascii=False) + ';',
        (ROOT / 'scripts/review-engine.js').read_text(), first,
        (ROOT / 'scripts/04-results-import-evidence.js').read_text(),
        (ROOT / 'scripts/05-states-responsive-direction.js').read_text(),
        (ROOT / 'scripts/review-renderer.js').read_text(),
    ]).replace('</script', '<\\/script')
    html = '''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"><title>Degron Footprint — UX/UI review</title><style>
    @font-face{font-family:Roboto;src:url(assets/roboto.ttf);font-weight:100 900;font-display:swap}@font-face{font-family:"Roboto Mono";src:url(assets/roboto-mono.ttf);font-weight:100 700;font-display:swap}
    *{box-sizing:border-box}body{margin:0;background:#e8eeea;color:#172b22;font:14px/1.5 Roboto,Arial,sans-serif}.review-bar{background:#fff;border-bottom:1px solid #ccd9d0;padding:12px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;position:sticky;top:0;z-index:20}.review-brand{font-weight:700}.review-note{font-size:12px;color:#506159}.review-bar select,.review-bar button{font:inherit;border:1px solid #bdcdc3;border-radius:7px;background:#fff;padding:8px 12px;min-height:40px;color:#183b2c}.review-bar button{cursor:pointer}.review-bar button:hover{background:#e7f3ed}.review-heading{padding:14px 20px;display:flex;justify-content:space-between;gap:16px;color:#42604f}.stage{padding:0 16px 32px;overflow:hidden}.canvas{margin:0 auto;box-shadow:0 12px 40px #163b2420}.artboard{overflow:visible}.vnode{min-width:0}.vtext{border:0!important}.hotspot{cursor:pointer}.hotspot:hover{filter:brightness(.96)}.hotspot:focus-visible,[role=gridcell]:focus-visible{outline:3px solid #2964dc;outline-offset:3px}#measure{position:absolute;top:0;left:-30000px;width:1800px;visibility:hidden}#cell-status{position:fixed;bottom:0;left:0;background:#142a24;color:white;font-size:12px;padding:4px 12px;z-index:30;pointer-events:none}#cell-status:empty{display:none}@media(max-width:600px){.review-bar{gap:8px;padding:8px}.review-note{width:100%}.review-bar select{max-width:100%;width:100%}.review-heading{padding:10px 8px}.stage{padding:0 8px 24px}}
    </style><header class="review-bar"><span class="review-brand">Degron Footprint · UX/UI</span><span class="review-note">Thiết kế đề xuất · dữ liệu minh họa · prototype không chạy inference/lưu dữ liệu</span><select id="screen-select" aria-label="Chọn giao diện"></select><button data-go="DF01">Dự án</button><button data-go="DF09">Kết quả</button><button data-go="DF12">Import</button><button data-go="M02">Mobile</button><button data-go="UX01">Theme</button></header><div class="review-heading"><span id="screen-name"></span><span id="zoom"></span></div><main id="stage" class="stage"><div id="canvas" class="canvas"></div></main><div id="measure"></div><div id="cell-status" aria-live="polite"></div><script type="module">'''+source+'''</script></html>'''
    for name in ['roboto','roboto-mono']:
        data=base64.b64encode((ROOT/'assets'/f'{name}.ttf').read_bytes()).decode()
        html=html.replace(f'url(assets/{name}.ttf)',f'url(data:font/ttf;base64,{data})')
    notices='\n\n'.join((ROOT/'assets'/n).read_text() for n in ['lucide-license.txt','roboto-license.txt','roboto-mono-license.txt'])
    html=html.replace('</html>','<!-- Third-party licence notices\n'+notices.replace('--','- -')+'\n--></html>')
    # This archived review must not be confused with the approved replacement.
    html = html.replace('<header class="review-bar">', '<div role="note" style="background:#fff0d2;color:#543b00;padding:12px 20px;font:14px/1.5 Arial,sans-serif;border-bottom:1px solid #9e7a23">BẢN CŨ — Không dùng để duyệt UI hiện tại. <a style="color:#174f40;font-weight:bold" href="../workspace-ui-v2/index.html">Mở Workspace UI v2 (hướng B đã chọn ngày 01/11/2026)</a>.</div>' + '<header class="review-bar">', 1)
    (ROOT / 'review.html').write_text(html)
    print('Built', ROOT / 'review.html')

if __name__ == '__main__':
    main()
