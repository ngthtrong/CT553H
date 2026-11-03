"""Localize the approved Vietnamese deck without changing its scientific data."""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'deck-explained-2026-11-03'
TOPIC=next(p for p in HERE.parents if (p/'data/README.md').exists())
title_source=TOPIC/'report/config/metadata.tex'
title_match=re.search(r'\\newcommand\{\\ThesisTitle\}\{([^}]+)\}',title_source.read_text(encoding='utf8'))
assert title_match, 'The thesis metadata must declare its English title'
PROJECT_TITLE=title_match[1]
translations=json.loads((HERE/'translation.json').read_text(encoding='utf8'))
notes=json.loads((HERE/'notes-en.json').read_text(encoding='utf8'))
metadata=json.loads((SOURCE/'slide-sources.json').read_text(encoding='utf8'))
assert len(notes)==len(metadata)==36
translations[metadata[0]['title']]=PROJECT_TITLE
for row,note in zip(metadata,notes):translations[row['notes']]=note

def tr(value):
    if value in translations:return translations[value]
    if re.fullmatch(r'[−+]?\d+,\d+',value):return value.replace(',','.')
    return value

class Localizer(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
    def handle_decl(self,value):self.parts.append('<!'+value+'>')
    def handle_starttag(self,tag,attrs):
        raw=self.get_starttag_text()
        for key,value in attrs:
            if key in ['alt','title','aria-label','data-title','data-section'] and value is not None:
                translated=tr(value)
                raw=re.sub(r'(\s'+re.escape(key)+r'=)([\"\']).*?\2',lambda m:m[1]+'"'+escape(translated,quote=True)+'"',raw,count=1)
        if tag=='html':raw=raw.replace('lang="vi"','lang="en"')
        self.parts.append(raw)
    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
    def handle_endtag(self,tag):self.parts.append('</'+tag+'>')
    def handle_data(self,value):self.parts.append(escape(tr(value),quote=False))
    def handle_comment(self,value):self.parts.append('<!--'+value+'-->')

parser=Localizer();parser.feed((SOURCE/'index.html').read_text(encoding='utf8'))
html=''.join(parser.parts)
# The same wrapped Vietnamese suffix occurs in two road-map captions.
html=re.sub(r'(Numerical and workflow</text><text[^>]*>)of applicability',r'\1checks',html)
html=re.sub(r'>Model(</text><text[^>]*>)trained</text>',r'>Trained\1model</text>',html)
assert '<h1>'+escape(PROJECT_TITLE)+'</h1>' in html, 'Slide 1 must show the thesis title'
(HERE/'index.html').write_text(html,encoding='utf8')

english_rows=[]
for row,note in zip(metadata,notes):
    r=dict(row,title=tr(row['title']),section=tr(row['section']),notes=note)
    # Footer strings may contain emphasis tags. Translate their text nodes too.
    local=Localizer();local.feed(row['insight']);r['insight']=''.join(local.parts)
    english_rows.append(r)
(HERE/'slide-sources.json').write_text(json.dumps(english_rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
document='# Speaker notes\n\n'+''.join(f'## {r["number"]}. {r["title"]}\n\n{r["notes"]}\n\nSources: '+', '.join(r['sources'])+'\n\n' for r in english_rows)
(HERE/'speaker-notes.md').write_text(document.rstrip()+'\n',encoding='utf8')

data=json.loads((SOURCE/'data.js').read_text().split('=',1)[1].strip().rstrip(';'))
for row in data['explorer']:row['name']=tr(row['name'])
(HERE/'data.js').write_text('window.DECK_DATA = '+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf8')
js=(SOURCE/'deck.js').read_text(encoding='utf8')
js_translations={'Phụ lục':'Appendix','bước':'step','Tiếp tục chuyển động':'Resume motion','Dừng chuyển động':'Pause motion',
                 'MAE (PSI) · thấp hơn tốt hơn':'MAE (PSI) · lower is better',
                 'AUROC dương · cao hơn tốt hơn':'Positive-event AUROC · higher is better',
                 'AP dương · cao hơn tốt hơn':'Positive-event AP · higher is better'}
for a,b in sorted(js_translations.items(),key=lambda item:-len(item[0])):js=js.replace(a,b)
js=js.replace(".toFixed(4).replace('.',',')",'.toFixed(4)')
(HERE/'deck.js').write_text(js,encoding='utf8')

evidence=json.loads((SOURCE/'evidence.json').read_text(encoding='utf8'))
evidence['source_sha256']['report/config/metadata.tex']=hashlib.sha256(title_source.read_bytes()).hexdigest()
for row in evidence['compared_recipes']:row['name']=tr(row['name'])
evidence['asset_sha256']={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['assets','vendor'] for p in (HERE/folder).rglob('*') if p.is_file()}
evidence['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
evidence['language']='en'
evidence['localization_sources']={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['translation.json','notes-en.json','prepare-figures.py']}
evidence['vietnamese_source_html_sha256']=hashlib.sha256((SOURCE/'index.html').read_bytes()).hexdigest()
(HERE/'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Built the English deck: 31 main slides + 5 appendices; scientific values unchanged.')
