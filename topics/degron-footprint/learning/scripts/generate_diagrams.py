#!/usr/bin/env python3
"""Editable draw.io teaching diagrams, rendered by the actual native CLI."""
from pathlib import Path
from contextlib import contextmanager
import json
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parents[1]
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
OUT=HERE/'assets/diagrams';OUT.mkdir(parents=True,exist_ok=True)
SKILL=ROOT/'.agents/skills/drawio-skill'
manifest=[]

def diagram(name,nodes,edges,kind='conceptual'):
    mx=ET.Element('mxfile',host='drawio',version='32.6.1')
    page=ET.SubElement(mx,'diagram',id=name,name=name)
    graph=ET.SubElement(page,'mxGraphModel',grid='1',gridSize='10',page='0',background='#ffffff')
    r=ET.SubElement(graph,'root');ET.SubElement(r,'mxCell',id='0');ET.SubElement(r,'mxCell',id='1',parent='0')
    for ident,label,x,y,w,h,planned in nodes:
        fill,stroke=('#FFF2CC','#A97A22') if planned else ('#E7F2F4','#167D8D')
        style=f'rounded=1;arcSize=10;whiteSpace=wrap;html=1;convertToSvg=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontColor=#243C46;fontFamily=DejaVu Sans;fontSize=24;spacing=12;'
        if planned:style+='dashed=1;'
        c=ET.SubElement(r,'mxCell',id=ident,value=label,style=style,vertex='1',parent='1')
        ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    positions={n[0]:n[2:6] for n in nodes}
    for i,(a,b,label) in enumerate(edges):
        ax,ay,aw,ah=positions[a];bx,by,bw,bh=positions[b]
        if abs(ay-by)<30:
            pins='exitX=1;exitY=0.5;entryX=0;entryY=0.5;' if bx>ax else 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'
        else:pins='exitX=0.5;exitY=1;entryX=0.5;entryY=0;'
        # The nested-split validation edges use distinct bottom/top attachment ports.
        if name=='nested-splits' and a=='outer-train':
            pins=('exitX=0.25;exitY=1;entryX=0.5;entryY=0;' if b=='inner-train'
                  else 'exitX=0.75;exitY=1;entryX=0.5;entryY=0;')
        if name=='nested-splits' and b=='select':
            pins=('exitX=0.5;exitY=1;entryX=0.25;entryY=0;' if a=='inner-train'
                  else 'exitX=0.5;exitY=1;entryX=0.75;entryY=0;')
        if name=='nested-splits' and a=='groups':
            pins=f'exitX={0.25 if b=="outer-train" else 0.75};exitY=1;entryX=0.5;entryY=0;'
        if name=='esm-heads' and a=='esm':
            port={'point':0.15,'cnn':0.5,'mcnn':0.85}[b]
            pins=f'exitX={port};exitY=1;entryX=0.5;entryY=0;'
        if name=='esm-heads' and b=='score':
            port={'point':0.15,'cnn':0.5,'mcnn':0.85}[a]
            pins=f'exitX=0.5;exitY=1;entryX={port};entryY=0;'
        if name=='calibration-and-domain' and a=='prob':
            pins='exitX=1;exitY=0.5;entryX=1;entryY=0.5;'
        if name=='calibration-and-domain' and a=='gate':
            pins='exitX=0.5;exitY=1;entryX=0.7;entryY=0;'
        if name=='scanning-transfer' and a=='sat':
            pins=f'exitX={0.25 if b=="finetune" else 0.75};exitY=1;entryX={0.75 if b=="finetune" else 0.25};entryY=0;'
        if name=='scanning-transfer' and b=='compare':
            pins=f'exitX=0.5;exitY=1;entryX={0.25 if a=="finetune" else 0.75};entryY=0;'
        st='edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endSize=10;endFill=1;strokeWidth=2;strokeColor=#36545D;fontSize=20;fontFamily=DejaVu Sans;labelBackgroundColor=#ffffff;'+pins
        c=ET.SubElement(r,'mxCell',id=f'edge-{i}',value=label,style=st,edge='1',parent='1',source=a,target=b)
        geom=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        if name=='calibration-and-domain' and a=='prob':
            pts=ET.SubElement(geom,'Array',attrib={'as':'points'})
            for px,py in [(1140,105),(1140,685)]:
                ET.SubElement(pts,'mxPoint',x=str(px),y=str(py))
    path=OUT/f'{name}.drawio';ET.indent(mx);ET.ElementTree(mx).write(path,encoding='utf-8',xml_declaration=True)
    result=subprocess.run(['python3',str(SKILL/'scripts/validate.py'),str(path),'--score','--json'],capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    validation=json.JSONDecoder().raw_decode(result.stdout)[0]
    manifest.append(dict(name=name,kind=kind,nodes=len(nodes),validation=validation))

def chain(name,labels,planned=(),cols=2,kind='conceptual'):
    nodes=[]
    w,h,gap=400,130,160
    if cols==3:w,h,gap=290,130,110
    for i,label in enumerate(labels):
        row,col=divmod(i,cols)
        if row%2:col=cols-1-col
        nodes.append((f'step-{i}',label,40+col*(w+gap),40+row*240,w,h,i in planned))
    diagram(name,nodes,[(f'step-{i}',f'step-{i+1}','') for i in range(len(labels)-1)],kind)

chain('learning-map',['1. Sinh học và\nđại lượng cần dự đoán','2. Thực nghiệm\nđược chuyển thành nhãn','3. Chia nhóm\nđể kiểm soát rò rỉ','4. Đối chứng\nvà cách đọc bằng chứng','5. Kết quả\nlịch sử và full-PSI','6. Hướng local\nvà tích hợp còn lại'],planned=(5,))
chain('gene-protein-degradation',['DNA: chứa thông tin\ncủa gene','Phiên mã: tạo\nbản sao RNA','Dịch mã tại ribosome:\ntạo chuỗi amino acid','Protein: chức năng\nphụ thuộc bối cảnh','Nhánh UPS phù hợp:\nE3, ubiquitin, proteasome','Thay đổi lượng protein:\nphụ thuộc cả tạo và hủy'])
chain('gps-measurement',['Construct DNA\ncho một WT/mutant','Tế bào biểu hiện\nGFP–peptide và DsRed','FACS: phân nhóm tế bào\ntheo GFP/DsRed','Thu sáu bin riêng\nDNA → PCR → giải trình tự','Read count theo\nconstruct và từng bin','Chuẩn hóa count\nTính PSI riêng mỗi lần đo','WT đúng cùng điều kiện\nLấy hiệu mutant − WT','Nhãn ΔPSI\nKhông phải xác suất'])
chain('mutation-unit',['WT minh họa\nM A L A K L A','A4V: vị trí 4\nthay A bằng V','Mutant minh họa\nM A L V K L A','Một ô: WT + vị trí + alt\nMột peptide: L × 20'])
chain('data-pipeline',['Nguồn đã ghim\nCount, sequence, metadata','QC kỹ thuật\nGiữ lý do loại/thiếu','Ánh xạ WT, tile\nvà tọa độ residue','Dựng WT riêng replicate\nTính và gộp ΔPSI','Hợp nhóm tương đồng\nTách scanning dev/T','Khóa fold và protocol\nLưu manifest, hash'],kind='source-backed-conceptual')
diagram('nested-splits',[
 ('groups','Nhóm protein\n(không tách từng ô)',420,20,400,110,False),
 ('outer-train','Outer-train\nđược phép học',120,230,400,110,False),
 ('outer-test','Outer-test\nkhóa đến cuối',780,230,360,110,False),
 ('inner-train','Inner-train\nfit scaler/PCA/model',20,460,350,130,False),
 ('inner-val','Inner-validation\nchọn α / epoch',440,460,350,130,False),
 ('select','Chọn cấu hình\nchỉ theo validation',210,690,400,110,False),
 ('refit','Khởi tạo / refit\ntrên outer-train hợp lệ',210,900,400,120,False),
 ('evaluate','Dự đoán outer-test\nGộp thành OOF',780,900,360,120,False)],
 [('groups','outer-train',''),('groups','outer-test',''),('outer-train','inner-train',''),('outer-train','inner-val',''),
  ('inner-train','select',''),('inner-val','select',''),('select','refit',''),('refit','evaluate',''),('outer-test','evaluate','')])
chain('feature-controls',['Cặp thay thế\nWT amino acid → mutant','Thêm composition\nđếm thành phần peptide','Thêm ngữ cảnh không thứ tự\nđếm amino acid trong cửa sổ','Thêm ngữ cảnh có thứ tự\nmỗi offset là một kênh'])
diagram('esm-heads',[
 ('wtmut','WT và mutant\ncùng mutation key',430,20,400,110,False),
 ('esm','ESM2-35M đóng băng\nbiểu diễn từng residue',430,240,400,120,False),
 ('point','Pointwise\nkernel 1',20,490,330,120,False),
 ('cnn','CNN\nkernel 5',465,490,330,120,False),
 ('mcnn','mCNN\nkernel 3 / 5 / 7',910,490,330,120,False),
 ('score','Đầu hồi quy → ΔPSI\nCùng cohort, fold, seed',430,760,400,130,False)],
 [('wtmut','esm',''),('esm','point',''),('esm','cnn',''),('esm','mcnn',''),('point','score',''),('cnn','score',''),('mcnn','score','')])
diagram('scanning-transfer',[
 ('scan','Scanning development\nnhãn ΔPSI quét',20,20,400,130,False),
 ('random','Nhánh đối chứng\nkhởi tạo ngẫu nhiên',650,20,400,130,False),
 ('pretrain','Tiền huấn luyện\nCNN one-hot',20,260,400,130,False),
 ('scratch','CNN cùng kiến trúc\nchưa học scanning',650,260,400,130,False),
 ('sat','Saturation outer-train\nđược phép dùng',330,500,400,130,False),
 ('finetune','Fine-tune saturation\nnhánh pretrain',20,750,400,130,False),
 ('train','Train saturation\nnhánh scratch',650,750,400,130,False),
 ('compare','Cùng outer-test\nso hai nhánh đã khóa',330,1010,400,130,False)],
 [('scan','pretrain',''),('random','scratch',''),('pretrain','finetune',''),('scratch','train',''),
  ('sat','finetune',''),('sat','train',''),('finetune','compare',''),('train','compare','')])
diagram('calibration-and-domain',[
 ('effect','Nhánh hiệu ứng\nmodel → score ΔPSI',40,40,400,130,False),
 ('prob','Calibrator trên score\nP(ΔPSI ≥ 1)',640,40,400,130,False),
 ('domain','Nhánh miền sử dụng\nPSI sàng / trình tự',40,330,400,130,False),
 ('gate','Gate: P(trong miền)\nin / borderline / out',640,330,400,130,False),
 ('ui','Kết quả cần cả hai\nscore/prob + domain + nguồn',340,620,400,130,True)],
 [('effect','prob',''),('domain','gate',''),('prob','ui',''),('gate','ui','')])
chain('local-training-plan',['Giữ data/protocol\nPin code, runtime, weights','Preflight tokenizer\n28 residue, finite, VRAM','Frozen feature từng pLM\nRidge/PCA64 làm head chung','Đối chứng ESM2-35M\nfrozen và LoRA cùng runtime','Đủ fold/seed rồi\ncollect OOF, ensemble, CI','Calibrate / final export\nđúng mô hình được chọn','W5-D đã khóa cho T\nkhông dùng T chọn pLM','Đánh giá phần mềm local\nlưu bền, khôi phục, đúng nguồn'],planned=tuple(range(8)),kind='plan-only')
diagram('software-boundaries',[
 ('research','Nghiên cứu offline\ndata → fit → đánh giá',20,30,400,130,False),
 ('model','Artefact baseline đã khóa\nweights + card + nguồn',620,30,400,130,False),
 ('react','Baseline giao diện\nReact + TypeScript',20,330,400,130,False),
 ('api','Baseline API\nFastAPI + inference',620,330,400,130,False),
 ('workspace','Mở rộng workspace\nprojects / import / jobs',20,630,400,130,True),
 ('storage','Worker + PostgreSQL\nlưu bền và recovery',620,630,400,130,True)],
 [('research','model',''),('model','api',''),('react','api',''),('workspace','storage',''),('api','storage','')],kind='implementation-and-plan')

@contextmanager
def display_env():
    env=os.environ.copy();process=None
    if os.name!='nt' and not env.get('DISPLAY') and env.get('XVFB_BINARY'):
        process=subprocess.Popen([env['XVFB_BINARY'],'-displayfd','1','-screen','0','1800x1400x24','-nolisten','tcp'],
                                 stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,env=env)
        number=process.stdout.readline().strip()
        if not number:raise RuntimeError('Xvfb did not start')
        env['DISPLAY']=':'+number
    try:yield env
    finally:
        if process:
            process.terminate();process.wait(timeout=10)

binary=os.environ.get('DRAWIO_BINARY') or shutil.which('drawio') or shutil.which('draw.io')
if not binary:raise SystemExit('Set DRAWIO_BINARY to the native draw.io executable; editable XML was generated.')
with display_env() as env:
    for record in manifest:
        path=OUT/(record['name']+'.drawio')
        for fmt in ['png','pdf']:
            dest=path.with_suffix('.'+fmt)
            args=[binary,'-x','-f',fmt,'-o',str(dest),str(path),'--disable-gpu']
            if fmt=='png':args[1:1]=['--width','1800']
            if fmt=='pdf':args[1:1]=['--crop']
            if os.name!='nt':args.append('--no-sandbox')
            result=subprocess.run(args,env=env,capture_output=True,text=True,timeout=45)
            if result.returncode or not dest.is_file():raise RuntimeError(result.stdout+result.stderr)
        print('Rendered',record['name'],flush=True)
(HERE/'diagram-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
