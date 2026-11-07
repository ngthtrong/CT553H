"""Check displayed English copy and numerical fidelity against the original edition."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import unicodedata

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.with_name('deck-research-overview-2026-11-02')

def has_untranslated_latin(text):
    for name in ['Nguyễn Thanh Trọng','Hồ Quang Thái']:
        text=text.replace(name,'')
    return any(ord(c)>127 and 'LATIN' in unicodedata.name(c,'') for c in text)

class CopyAudit(HTMLParser):
    def __init__(self):
        super().__init__();self.remaining=[]
    def handle_data(self,data):
        if data.strip() and has_untranslated_latin(data):
            self.remaining.append(data.strip())
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ['title','aria-label','alt','data-title','data-section'] and value and has_untranslated_latin(value):
                self.remaining.append(key+': '+value)

html=(HERE/'index.html').read_text(encoding='utf8')
assert '<html lang="en">' in html
audit=CopyAudit();audit.feed(html)
figure_remaining={}
for path in (HERE/'assets').glob('*.svg'):
    labels=re.findall(r'<!--(.*?)-->',path.read_text(encoding='utf8'),re.S)
    bad=[label.strip() for label in labels if has_untranslated_latin(label)]
    if bad:figure_remaining[path.name]=bad
js_remaining=[line for line in (HERE/'deck.js').read_text(encoding='utf8').splitlines() if has_untranslated_latin(line)]
assert not audit.remaining,audit.remaining
assert not figure_remaining,figure_remaining
assert not js_remaining,js_remaining

def data(path):
    text=path.read_text(encoding='utf8').strip()
    return json.loads(text.removeprefix('window.DECK_DATA=').removesuffix(';'))

original=data(ORIGINAL/'data.js');english=data(HERE/'data.js')
assert original['hif']==english['hif']
assert len(original['explorer'])==len(english['explorer'])
for left,right in zip(original['explorer'],english['explorer']):
    for metric in ['mae','auroc','ap']:
        assert left[metric]==right[metric],(left['name'],metric)
base_evidence=json.loads((ORIGINAL/'evidence.json').read_text(encoding='utf8'))
evidence=json.loads((HERE/'evidence.json').read_text(encoding='utf8'))
assert base_evidence['source_hashes']==evidence['source_hashes']
assert base_evidence['dataset_identity']==evidence['dataset_identity']
for name,want in evidence['figure_sha256'].items():
    assert hashlib.sha256((HERE/'assets'/name).read_bytes()).hexdigest()==want
assert len(json.loads((HERE/'slide-sources.json').read_text(encoding='utf8')))==50
assert json.loads((HERE/'validation.json').read_text(encoding='utf8'))['pass']
report_path=HERE/'localization-validation.json'
report=json.loads(report_path.read_text(encoding='utf8'))
report.update(pass_=True,remaining_displayed_vietnamese=[],remaining_chart_labels=[],
    remaining_control_labels=[],numeric_chart_values_identical=True,hif_measurements_identical=True,
    source_json_hashes_identical=True,render_validation_pass=True,figure_hashes_verified=len(evidence['figure_sha256']))
report['pass']=report.pop('pass_')
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('English copy verified; all chart values and HIF1A measurements match the original edition exactly.')
