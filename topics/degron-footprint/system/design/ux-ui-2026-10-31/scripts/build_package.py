"""Package the reviewed node specification as a native Figma plugin."""
from pathlib import Path
import json
import zipfile

ROOT=Path(__file__).resolve().parent.parent

def main():
    spec=json.loads((ROOT/'design-spec.json').read_text())
    plugin=ROOT/'figma-plugin';plugin.mkdir(exist_ok=True)
    notice='/* Lucide / Feather icon licence notices\n'+(ROOT/'assets/lucide-license.txt').read_text().replace('*/','* /')+'\n*/\n'
    code=notice+'const DESIGN='+json.dumps(spec,ensure_ascii=False,separators=(',',':'))+';\n'+(ROOT/'scripts/plugin-template.js').read_text()
    (plugin/'code.js').write_text(code)
    manifest={'name':'Degron Footprint UX/UI Import','id':'REPLACE_WITH_FIGMA_ASSIGNED_ID','api':'1.0.0','editorType':['figma'],'main':'code.js','documentAccess':'dynamic-page','networkAccess':{'allowedDomains':['none']}}
    (plugin/'manifest.template.json').write_text(json.dumps(manifest,indent=2)+'\n')
    screen_map=[]
    for s in spec['screens']:
        if s['id'].startswith('DF'):
            uc={'DF01':['UC-10'],'DF02':['UC-10'],'DF03':['UC-01'],'DF04':['UC-04'],'DF05':['UC-08'],'DF06':['UC-04','UC-08'],'DF07':['UC-08'],'DF08':['UC-08'],'DF09':['UC-01','UC-02','UC-03'],'DF10':['UC-02','UC-10'],'DF11':['UC-06'],'DF12':['UC-09'],'DF13':['UC-09'],'DF14':['UC-09','UC-10'],'DF15':['UC-05'],'DF16':['UC-07'],'DF17':['UC-07'],'DF18':['UC-01'],'DF19':['UC-01']}[s['id']]
        else:
            uc={'ST01':['UC-10'],'ST02':['UC-03'],'ST03':['UC-10'],'ST04':['UC-01'],'ST05':['UC-06'],'ST06':['UC-08'],'ST07':['UC-05'],'ST08':['UC-01'],'ST09':['UC-10'],'ST10':['UC-10'],'ST11':['UC-09'],'ST12':['UC-01'],'ST13':['UC-03'],'ST14':['UC-03'],'ST15':['UC-10'],'ST16':['UC-09','UC-10'],'ST17':['UC-10'],'ST18':['UC-08'],'ST19':['UC-01'],'ST20':['UC-09'],'ST21':['UC-02'],'ST22':['UC-01'],'ST23':['UC-10'],'M01':['UC-01'],'M02':['UC-01','UC-02'],'M03':['UC-01'],'UX01':[],'UX02':[]}[s['id']]
        mapping={'UC-01':(['FR-01','FR-03','FR-04','FR-05','FR-06','FR-09','FR-10','FR-11','FR-14'],['DOM-01','E2E-01','E2E-08','E2E-09','E2E-12']), 'UC-02':(['FR-07','FR-08'],['E2E-02','UT-04']), 'UC-03':(['FR-12','FR-13','FR-23','FR-34'],['RG-02','API-31','E2E-10','BATCH-06']), 'UC-04':(['FR-02','FR-15','FR-16','FR-25'],['E2E-04','BATCH-04']), 'UC-05':(['FR-17','FR-29','FR-30','FR-34'],['IMP-03','IMP-04']), 'UC-06':(['FR-18','FR-35'],['ANN-01','E2E-06']), 'UC-07':(['FR-19','FR-21','FR-22'],['E2E-07']), 'UC-08':(['FR-24','FR-25','FR-26','FR-27','FR-36'],['BATCH-01','BATCH-02','BATCH-03','BATCH-04','BATCH-05','BATCH-06']), 'UC-09':(['FR-28','FR-29','FR-30','FR-36'],['IMP-01','IMP-02','IMP-03','IMP-04']), 'UC-10':(['FR-31','FR-32','FR-33','FR-14','FR-27'],['HIST-01','HIST-02','HIST-03'])}
        screen_map.append({'id':s['id'],'title':s['title'],'width':s['width'],'height':s['node']['height'],'use_cases':uc,'requirements':sorted({fr for u in uc for fr in mapping[u][0]}),'acceptance_references':sorted({test for u in uc for test in mapping[u][1]}),'relation_scope':'Related UC-level requirements and planned acceptance references; not implementation verification','review_url':'review.html#'+s['id'],'figma_screen_status':'NOT_CREATED_BY_MCP; available in reviewed native import spec'})
    (ROOT/'screen-map.json').write_text(json.dumps(screen_map,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(ROOT/'figma-import-package.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in [plugin/'code.js',plugin/'manifest.template.json',plugin/'README.md',ROOT/'scripts/configure_plugin.py',ROOT/'README.md',ROOT/'review-validation.json',ROOT/'screen-map.json',ROOT/'assets/lucide-license.txt',ROOT/'assets/sds-license.txt']:
            if f.exists():z.write(f,f.relative_to(ROOT))
    print(f'Packaged {len(spec["screens"])} design frames; native Figma execution remains pending.')

if __name__=='__main__':main()
