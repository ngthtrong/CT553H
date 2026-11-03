"""Build the explanatory deck from saved evidence; never fit models or inspect locked T."""
from pathlib import Path
from html import escape as esc
import ast
import hashlib
import json
import math
import re
import textwrap

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data/README.md').exists())
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
RESEARCH = TOPIC / 'research'
OLD = HERE.parent / 'deck-research-overview-2026-11-02'
PAPER = 'https://pubmed.ncbi.nlm.nih.gov/37738965/'
NIGMS = 'https://www.nigms.nih.gov/image-gallery/3764'
PROJECT_TITLE = 'Dự đoán hiệu ứng đột biến degron ở mức residue và xây dựng công cụ hỗ trợ phân tích'
sources = {}

def read(relative):
    p = TOPIC / relative
    sources[relative] = hashlib.sha256(p.read_bytes()).hexdigest()
    return json.loads(p.read_text(encoding='utf8'))

ANALYSIS_PATH = 'research/kaggle-roadmap-2026-10-31/output-analysis.json'
DETAILS_PATH = 'research/kaggle-roadmap-2026-10-31/output-analysis-details.json'
DATA_PATH = 'research/kaggle-roadmap-2026-10-31/dataset-build.json'
NEURAL_PATH = 'research/kaggle-roadmap-2026-10-31/degron_v3/neural.py'
FEATURE_PATH = 'research/kaggle-roadmap-2026-10-31/degron_v3/features.py'
analysis = read(ANALYSIS_PATH)
details = read(DETAILS_PATH)
dataset = read(DATA_PATH)
hif = read('research/slide-figures-2026-10-15/example-matrix.json')
for name in [NEURAL_PATH, FEATURE_PATH, 'research/README.md', 'system/README.md',
             'research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md',
             'research/full-data-audit/psi-build.json']:
    sources[name] = hashlib.sha256((TOPIC / name).read_bytes()).hexdigest()

GREEN='#18974C'; DARK='#0A5032'; CORAL='#C76242'; BLUE='#477CA7'
INK='#193A2B'; SAGE='#D0DEBB'; LINE='#D6DFD3'; PAPER_BG='#F6F7F2'

# Reuse only the drawing helpers, without importing or running the old generator.
old_source=(OLD/'build-deck.py').read_text(encoding='utf8')
helper_names={'text','box','edge','svg','process','heat','designs','label_pipeline',
              'groups_diagram','protein_process','architecture','metrics_diagram'}
for node in ast.parse(old_source).body:
    if isinstance(node, ast.FunctionDef) and node.name in helper_names:
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(OLD/'build-deck.py'),'exec'))

def fmt(v, digits=4):
    return f'{v:.{digits}f}'.replace('.',',')

def metric(recipe,key='mae'):
    return analysis['recipes'][recipe]['ensemble']['all'][key]

def frag(n, body):
    return f'<g class="fragment" data-step="{n}">{body}</g>'

def visual(body):
    return '<div class="visual">'+body+'</div>'

def image(name,alt,cls='figure'):
    return f'<img class="{cls}" src="assets/{name}" alt="{esc(alt,quote=True)}">'

def split(left,right,equal=False):
    return f'<div class="split {"equal" if equal else ""}"><div class="visual">{left}</div><div class="aside">{right}</div></div>'

def badge(s,warn=False):
    return f'<span class="context {"warn" if warn else ""}">{s}</span>'

def lines(values):
    return ''.join(f'<p>{v}</p>' for v in values)

def seq(value,x=50,y=120,step=44,hot=None,col=CORAL):
    s=''
    for i,aa in enumerate(value):
        c=col if i==hot else SAGE
        s+=f'<rect x="{x+i*step}" y="{y}" width="{step-5}" height="45" rx="5" fill="{c}"/>'
        s+=text(x+i*step+(step-5)/2,y+30,aa,23,'white' if i==hot else INK,weight=600)
    return s

def tiles(x,y,columns=28,rows=20,size=12,scan=False):
    s=''
    aas='ACDEFGHIKLMNPQRSTVWY';sequence=hif['sequence']
    for j,aa in enumerate(aas[:rows]):
        for i in range(columns):
            wt=sequence[i % len(sequence)]
            replacement='R' if wt in 'ACDEGILSTV' else 'A' if wt in 'HKNQRY' else 'S'
            fill=LINE if aa==wt or (scan and aa!=replacement) else GREEN
            s+=f'<rect x="{x+i*size}" y="{y+j*size}" width="{size-1}" height="{size-1}" fill="{fill}"/>'
    return s

def embedding(x,y,columns=15,rows=6,hot=False):
    s=''
    for i in range(columns):
        for j in range(rows):
            c=CORAL if hot and i==7 else BLUE
            opacity=.2+((i*7+j*11)%7)*.1
            s+=f'<rect x="{x+i*25}" y="{y+j*23}" width="21" height="19" rx="1" fill="{c}" opacity="{opacity}"/>'
    return s

def rows_table(headers,rows,cls=''):
    return '<table class="table '+cls+'"><thead><tr>'+''.join(f'<th>{x}</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'

def bars(labels,values,colors=None,xmax=.5,xlabel='MAE (PSI) · thấp hơn tốt hơn'):
    s='';x=390;span=555;top=40;step=65
    for i,(label,v) in enumerate(zip(labels,values)):
        y=top+i*step;c=(colors or [GREEN]*len(labels))[i]
        s+=text(x-18,y+23,label,20,anchor='end')
        s+=f'<rect x="{x}" y="{y}" width="{v/xmax*span}" height="33" rx="2" fill="{c}"/>'
        s+=text(x+v/xmax*span+12,y+23,fmt(v),20,anchor='start',weight=600)
    bottom=top+len(labels)*step
    s+=f'<line x1="{x}" y1="{bottom}" x2="{x+span}" y2="{bottom}" stroke="{LINE}"/>'
    for j in range(6):
        xx=x+j*span/5;s+=text(xx,bottom+28,fmt(j*xmax/5,1),17)
    s+=text(x+span/2,bottom+65,xlabel,19)
    return svg(s,'Biểu đồ: '+xlabel,w=1100,h=bottom+88)

def mutation():
    s=text(65,70,'WT · trình tự tham chiếu',23,anchor='start',weight=600)
    s+=seq('MAGLSKVT',65,95,72,3)
    s+=frag(1,edge(314,155,314,218,CORAL)+text(610,205,'Vị trí 4: L → P',28,CORAL,weight=600))
    s+=frag(1,text(65,260,'Mutant · trình tự sau thay thế',23,anchor='start',weight=600)+seq('MAGPSKVT',65,285,72,3))
    s+=text(900,100,'Một phép thay',28,DARK,weight=600)
    s+=text(900,150,['vị trí','AA ban đầu','AA thay vào'],23)
    return svg(s,'Ví dụ giả định L thành P tại vị trí 4',h=390)

def gps():
    s=text(165,30,'Cùng hệ reporter',23,DARK,weight=600)
    s+=box(20,65,155,65,'DsRed',color=CORAL)+text(100,165,'Tham chiếu',19)
    s+=box(205,65,140,65,'GFP',color=GREEN)+box(345,65,140,65,'Peptide',color=BLUE)
    s+=text(345,165,'Tín hiệu phụ thuộc độ bền',19)
    s+=frag(1,edge(490,100,550,100)+text(750,42,'Tỷ lệ GFP / DsRed',24,DARK,weight=600))
    heights=[35,65,110,130,75,40]
    for i,h in enumerate(heights):
        xx=580+i*72
        s+=frag(1,f'<rect x="{xx}" y="{235-h}" width="45" height="{h}" fill="{GREEN}" opacity="{.35+i*.11}"/>'+text(xx+22,270,i+1,20))
    s+=frag(1,text(790,314,'Sáu bin · từ kém bền đến bền hơn',21))
    s+=frag(2,text(305,365,'Phân bố số đọc đã chuẩn hóa',23,BLUE,weight=600)+edge(535,360,675,360)+text(875,370,'PSI ∈ [1; 6]',30,DARK,weight=600))
    return svg(s,'Minh họa hệ GFP peptide và DsRed, phân sáu bin và tạo PSI',h=410)

def delta_example():
    s=''
    for x,value,label,col in [(150,3.8,'Mutant',CORAL),(710,2.5,'WT',BLUE)]:
        s+=text(x+130,90,label,25,col,weight=600)+text(x+130,165,str(value).replace('.',','),70,col,weight=600)
    s+=frag(1,text(560,160,'−',64)+text(550,255,'ΔPSI = 3,8 − 2,5 = +1,3',42,DARK,weight=600))
    s+=frag(2,text(550,340,'Dương: reporter sau đột biến bền hơn trong assay này',25,DARK))
    return svg(s,'Ví dụ giả định PSI WT 2,5 và mutant 3,8 tạo delta PSI dương 1,3',h=390)

def mutation_space():
    s=text(240,80,'28 vị trí × 19 AA khác WT',28,DARK,weight=600)
    s+=text(240,195,'532',100,DARK,weight=600)+text(240,250,'phép thay đơn có thể thử',23)
    s+=frag(1,edge(470,180,565,180)+tiles(610,35,size=14)+text(800,365,'Mỗi ô là một phép thay',25,DARK,weight=600))
    return svg(s,'Không gian 532 phép thay đơn của một peptide dài 28 residue',h=400)

def record_diagram():
    s=tiles(30,50,columns=12,rows=12,size=17)
    s+=f'<rect x="{30+5*17}" y="{50+4*17}" width="16" height="16" fill="{CORAL}" class="pulse"/>'
    s+=edge(245,150,325,150,CORAL)+box(340,105,260,90,'Một phép thay',color=CORAL)
    s+=text(800,70,'Định danh mẫu',26,DARK,weight=600)
    for i,(k,v) in enumerate([('Peptide','một ngữ cảnh trình tự'),('Vị trí','4'),('Phép thay','L → P'),('Nhãn','PSI(mutant) − PSI(WT)')]):
        s+=text(650,130+i*47,k,20,anchor='start',weight=600)+text(800,130+i*47,v,20,anchor='start')
    return svg(s,'Khóa mẫu gồm peptide vị trí amino acid ban đầu và amino acid thay vào',h=370)

def input_label():
    s=text(240,35,'Đầu vào lúc dự đoán',27,DARK,weight=600)
    s+=box(35,75,410,80,'WT + vị trí + AA thay vào',color=BLUE)
    s+=edge(240,165,240,220,BLUE)+box(45,235,390,85,'Mô hình → ΔPSI dự đoán')
    s+=frag(1,text(815,35,'Nhãn lúc huấn luyện',27,DARK,weight=600)+box(600,75,440,80,'PSI(WT) và PSI(mutant)',color=CORAL)+edge(820,165,820,220,CORAL)+box(610,235,420,85,'ΔPSI thực nghiệm',color=CORAL))
    s+=frag(2,edge(600,277,450,277,CORAL)+text(550,370,'Nhãn hướng dẫn học; PSI không làm feature đầu vào',25,DARK,weight=600))
    return svg(s,'Tách đầu vào sequence-only khỏi nhãn PSI thực nghiệm',h=410)

def folds():
    s=''
    for j,col in enumerate([GREEN,BLUE,CORAL,DARK]):
        for i in range(3):
            xx=65+j*100+23*math.cos(i*2.1); yy=100+23*math.sin(i*2.1)
            s+=f'<circle cx="{xx}" cy="{yy}" r="12" fill="{col}"/>'
    s+=text(210,185,'Giữ nguyên nhóm protein',24,DARK,weight=600)
    s+=edge(430,100,590,95)+edge(430,120,590,250,CORAL)
    s+=box(610,35,450,90,'Train và validation','Fit / chọn tham số trong phần này')
    s+=box(610,205,450,90,'Nhóm kiểm tra ngoài','Chỉ dùng đánh giá',CORAL)
    s+=text(160,385,'Luân phiên',20,DARK,weight=600)
    for i in range(5):
        xx=300+i*140
        s+=f'<rect x="{xx}" y="355" width="120" height="44" rx="4" fill="{CORAL if i==0 else SAGE}"/>'+text(xx+60,385,f'Fold {i+1}',19,'white' if i==0 else INK)
    return svg(s,'Chia nhóm protein và luân phiên năm outer folds',h=430)

def ups():
    s=''
    for i in range(9):
        xx=30+i*16; yy=58+12*math.sin(i*.8)
        if i:s+=f'<line x1="{xx-16}" y1="{58+12*math.sin((i-1)*.8)}" x2="{xx}" y2="{yy}" stroke="{SAGE}" stroke-width="7"/>'
        s+=f'<circle cx="{xx}" cy="{yy}" r="8" fill="{CORAL if 3<=i<=5 else GREEN}"/>'
    s+=text(205,66,'Protein mang degron',24,DARK,anchor='start',weight=600)
    s+=edge(100,90,100,145)
    s+=f'<path d="M45 170 Q100 130 145 170 L120 190 L145 210 Q100 250 45 210 Z" fill="{SAGE}" stroke="{DARK}" stroke-width="3"/>'
    for i in range(3):s+=f'<circle class="pulse" cx="{140+i*12}" cy="{166-i*13}" r="7" fill="{CORAL}"/>'
    s+=text(205,177,['Nhận diện và','gắn ubiquitin'],24,DARK,anchor='start',weight=600)
    s+=text(205,240,'Nhờ hệ thống phù hợp',18,anchor='start')
    s+=edge(100,250,100,290)
    for i in range(5):s+=f'<ellipse cx="{60+i*18}" cy="335" rx="20" ry="38" fill="none" stroke="{DARK}" stroke-width="7" opacity="{.45+i*.12}"/>'
    s+=text(205,325,'Proteasome',25,DARK,anchor='start',weight=600)+text(205,364,'Cắt thành peptide ngắn',19,anchor='start')
    return svg(s,'Minh họa nguyên lý nhận diện degron gắn ubiquitin và phân hủy',w=520,h=410)

def metric_concepts():
    s=''
    for i,(title,col) in enumerate([('Sai số',GREEN),('Xếp hạng',BLUE),('Độ chắc chắn',CORAL)]):
        xx=30+i*365
        s+=text(xx+165,42,title,28,col,weight=600)
        if i==0:
            s+=f'<line x1="{xx+55}" y1="250" x2="{xx+270}" y2="105" stroke="{LINE}" stroke-width="2"/>'
            for j in range(4):
                x=xx+85+j*46;y=235-j*32
                s+=f'<circle cx="{x}" cy="{y}" r="8" fill="{GREEN}"/><line x1="{x}" y1="{y}" x2="{x}" y2="{y-27}" stroke="{CORAL}" stroke-width="3"/>'
            s+=text(xx+165,315,'MAE',29,col,weight=600)+text(xx+165,355,'Độ lệch dự đoán và đo',20)
        elif i==1:
            for j in range(5):
                h=145-j*23
                s+=f'<rect x="{xx+65+j*45}" y="{255-h}" width="30" height="{h}" fill="{BLUE}" opacity="{1-j*.13}"/>'
            s+=text(xx+165,315,'AUROC / AP',29,col,weight=600)+text(xx+165,355,'Ưu tiên các ô có ΔPSI ≥ 1',20)
        else:
            s+=f'<line x1="{xx+170}" y1="95" x2="{xx+170}" y2="265" stroke="{LINE}" stroke-width="2" stroke-dasharray="5 5"/>'
            s+=f'<line x1="{xx+70}" y1="180" x2="{xx+275}" y2="180" stroke="{CORAL}" stroke-width="4"/><line x1="{xx+70}" y1="167" x2="{xx+70}" y2="193" stroke="{CORAL}" stroke-width="3"/><line x1="{xx+275}" y1="167" x2="{xx+275}" y2="193" stroke="{CORAL}" stroke-width="3"/><circle cx="{xx+145}" cy="180" r="9" fill="{CORAL}"/>'
            s+=text(xx+170,285,'0',18)+text(xx+165,315,'Khoảng tin cậy',27,col,weight=600)+text(xx+165,355,'Bootstrap theo nhóm',20)
    return svg(s,'Khái niệm MAE AUROC AP và khoảng tin cậy minh họa',h=395)

def road_steps(labels,subs):
    n=len(labels);gap=35;w=(1060-(n-1)*gap)/n;s=''
    for i,(label,sub) in enumerate(zip(labels,subs)):
        xx=20+i*(w+gap)
        s+=box(xx,25,w,75,label,sub)
        if i<n-1:s+=edge(xx+w+3,62,xx+w+gap-5,62)
    return svg(s,'Các công việc cần thực hiện theo thứ tự phụ thuộc',h=185)

def ridge():
    s=seq('MAGLSKVT',50,40,60,3)+text(800,75,'L → P',32,CORAL,weight=600)
    for i,(label,sub,col) in enumerate([('Phép thay','WT và mutant one-hot',CORAL),('Thành phần','Tần suất 20 AA',GREEN),('Ngữ cảnh ±5','Thứ tự AA lân cận',BLUE)]):
        xx=40+i*365;s+=frag(1,box(xx,155,300,78,label,sub,col))
    s+=frag(2,text(550,350,'Đặc trưng × trọng số → một giá trị ΔPSI',30,DARK,weight=600))
    return svg(s,'Ridge kết hợp đặc trưng phép thay thành phần peptide và lân cận',h=410)

def onehot():
    s=seq('MAGLSKVT',45,45,53,3)+edge(485,68,590,68,BLUE)
    for i,a in enumerate('MAGLSKVT'):
        for j in range(6):
            s+=f'<rect x="{625+i*38}" y="{25+j*31}" width="30" height="24" fill="{BLUE if j==i%6 else LINE}"/>'
    s+=text(800,250,'One-hot · các hàng chỉ minh họa',20)
    s+=frag(1,f'<rect class="kernel-onehot" x="620" y="18" width="186" height="197" fill="none" stroke="{CORAL}" stroke-width="4" rx="4"/>'+text(340,235,['Bộ lọc học mẫu','ở vùng lân cận'],29,DARK,weight=600))
    s+=frag(2,text(550,350,'One-hot → CNN → đặc trưng → ΔPSI',32,DARK,weight=600))
    return svg(s,'Minh họa one-hot và bộ lọc CNN cục bộ',h=400)

def plm():
    s=text(80,45,'WT',24,BLUE,weight=600)+seq('MAGLSKVT',20,68,41,3,BLUE)
    s+=text(80,235,'Mutant',24,CORAL,weight=600)+seq('MAGPSKVT',20,258,41,3)
    s+=box(430,130,220,95,'ESM2-35M',color=BLUE)
    s+=edge(355,90,420,155,BLUE)+edge(355,280,420,205,CORAL)
    s+=frag(1,embedding(710,40,columns=13,rows=4)+embedding(710,240,columns=13,rows=4,hot=True)+text(880,162,'H_WT',24,BLUE,weight=600)+text(880,362,'H_mutant',24,CORAL,weight=600))
    s+=frag(2,text(530,395,'ΔH = H_mutant − H_WT',32,DARK,weight=600))
    return svg(s,'Hai trình tự qua cùng encoder ESM2 rồi lấy hiệu embedding',h=435)

def head_comparison(multi=False):
    s=''
    configs=[(1,35,'Pointwise · kernel 1',BLUE),(5,235,'CNN · kernel 5',GREEN)] if not multi else [(3,20,'Kernel 3',GREEN),(5,150,'Kernel 5',BLUE),(7,280,'Kernel 7',CORAL)]
    for kernel,y,label,col in configs:
        nr=3 if multi else 4
        s+=text(12,y+35,label,22,col,anchor='start',weight=600)+embedding(290,y,15,nr)
        s+=f'<rect class="kernel-window" x="285" y="{y-6}" width="{kernel*25}" height="{nr*23+6}" rx="3" stroke="{col}" stroke-width="3" fill="none"/>'
        s+=edge(690,y+35,800,y+35,col)+box(810,y+5,260,65,'Đặc trưng',color=col)
    if multi:s+=text(830,425,'Hợp nhất → ΔPSI',26,DARK,weight=600)
    else:s+=text(550,410,'Cùng embedding · khác cách head trộn các vị trí',25,DARK,weight=600)
    return svg(s,'So sánh các kernel tích chập trên biểu diễn ESM',h=455)

def tuning():
    s=''
    for i,(label,col) in enumerate([('Frozen',BLUE),('LoRA',CORAL)]):
        xx=45+i*560;s+=text(xx+220,40,label,33,col,weight=600)
        s+=box(xx,90,440,95,'Backbone ESM2 cố định',color=BLUE)
        if i:
            s+=f'<rect class="pulse" x="{xx+285}" y="145" width="135" height="70" rx="5" fill="{CORAL}"/>'+text(xx+353,176,['LoRA','được học'],19,'white',weight=600)
        s+=edge(xx+220,220,xx+220,260,col)+box(xx+90,270,260,70,'Head được học',color=GREEN)
    s+=text(550,405,'So cùng seed / fold và protocol · xét cả sai số lẫn chi phí',24,DARK,weight=600)
    return svg(s,'Frozen chỉ học head; LoRA học thêm các adapter trong backbone',h=440)

def training_scopes():
    s='';labels=['PSI(WT) ≤ 3','PSI(WT) ≤ 4','PSI(WT) ≤ 5','Toàn dải PSI','Toàn dải, cân bằng']
    for i,label in enumerate(labels):
        y=15+i*67
        s+=box(20,y,350,49,label,color=BLUE if i<3 else GREEN)
        s+=edge(390,y+25,725,180,GREEN,delay=i)
    s+=box(745,125,320,110,['Cùng tập đánh giá W'],'235 peptide · 221 nhóm',CORAL)
    return svg(s,'Năm phạm vi train đánh giá trên cùng tập W',h=395)

def priority():
    s=tiles(25,55,size=13)+text(207,360,'Ma trận hiệu ứng',25,DARK,weight=600)
    s+=edge(410,180,520,180,CORAL)
    for i,(label,w) in enumerate([('Ứng viên 1',240),('Ứng viên 2',185),('Ứng viên 3',130)]):
        yy=65+i*85;s+=text(550,yy+20,label,22,anchor='start')+f'<rect x="700" y="{yy}" width="{w}" height="28" rx="3" fill="{CORAL}"/>'
    s+=text(815,360,'Chọn → kiểm chứng thực nghiệm',25,DARK,weight=600)
    return svg(s,'Ma trận minh họa được chuyển thành danh sách ứng viên đột biến',h=410)

def summary_chain():
    s=seq('MAGLSKVT',45,55,48,3)+text(770,85,'Thay L → P ở vị trí 4',29,CORAL,weight=600)
    labels=[['Trình tự','và phép thay'],['Mô hình','đã học'],['ΔPSI','dự đoán'],['Ưu tiên','thí nghiệm']]
    for i,label in enumerate(labels):
        xx=35+i*275;col=[BLUE,DARK,CORAL,GREEN][i]
        s+=frag(i,box(xx,200,225,95,label,color=col))
        if i<3:s+=frag(i+1,edge(xx+235,248,xx+265,248,col))
    s+=text(550,380,'Bằng chứng hiện có: benchmark development trên dữ liệu Zhang',24,DARK,weight=600)
    return svg(s,'Chuỗi liên kết từ trình tự đến ưu tiên thí nghiệm',h=420)

slides=[]

def slide(title,section,body,insight='',notes='',refs=(),appendix=False,dark=False):
    slides.append(dict(number=len(slides)+1,title=title,section=section,body=body,insight=insight,
                       notes=notes,sources=list(refs),appendix=appendix,dark=dark))

slide(PROJECT_TITLE,'Degron footprint',
      '<div class="hero"><div><p class="eyebrow">CT553H · Giải thích đề tài</p><h1>'+esc(PROJECT_TITLE)+'</h1><p class="subtitle">Học máy dự đoán ΔPSI<br>Công cụ hỗ trợ ưu tiên thí nghiệm</p><div class="identity">Nguyễn Thanh Trọng · B2305615<br>GVHD: TS. Hồ Quang Thái<br>Đại học Cần Thơ · 03/11/2026</div></div><div class="hero-art">'+svg(tiles(110,50,size=14)+text(300,390,'Mỗi ô · một phép thay',23,DARK,weight=600),w=600,h=450)+'</div></div>',
      notes='Đây là deck giải thích đề tài từ nền tảng sinh học tới nghiên cứu học máy và phần mềm. Ma trận mở đầu minh họa thiết kế, không là kết quả inference. Mục tiêu là dự đoán hiệu ứng một thay thế amino acid đơn trên độ bền reporter.',refs=[PAPER,'research/README.md'],dark=True)

slide('Protein được tạo từ một chuỗi amino acid','Sinh học và bài toán',
      '<div class="split equal"><div class="protein-intro">'+image('fam188a.gif','Mô hình protein Fam188a quay minh họa cấu trúc gấp cuộn','protein-photo animated-gif')+image('fam188a-poster.png','Ảnh tĩnh của mô hình protein Fam188a','protein-photo gif-poster')+'<p class="photo-label">Mô hình cấu trúc protein · minh họa</p></div><div class="stack centered"><p class="concept-word">Protein → peptide → residue</p>'+visual(svg(seq('MAGLSKVT',25,85,64,3)+text(280,220,'Một chữ · một amino acid tại một vị trí',23),w=580,h=280))+'<p class="small">Peptide là đoạn chuỗi ngắn.<br>Residue là đơn vị amino acid trong chuỗi.</p></div></div>',
      'Mô hình đọc chuỗi chữ cái; mỗi chữ tương ứng một amino acid.',
      'GIF là mô hình dự đoán cấu trúc Fam188a của Nikolakhs, CC BY-SA 3.0. Không phải HIF1A hoặc cấu trúc degron đang khảo sát. Chuỗi tám AA là ví dụ giả định. Peptide trong nhiệm vụ chính dài 28 residue.',
      ['https://commons.wikimedia.org/wiki/File:I-TASSER_predicted_protein_fold_of_Fam188a.gif'])

video='<div class="movie"><video muted loop playsinline preload="metadata" poster="assets/proteasome-poster.jpg" aria-label="Mô phỏng proteasome xử lý protein gắn ubiquitin"><source src="assets/proteasome.mp4" type="video/mp4"></video><img class="video-print" src="assets/proteasome-poster.jpg" alt="Khung hình proteasome với cơ chất và chuỗi ubiquitin"><button class="video-toggle">Phát / dừng video</button><p class="small credit">Andreas Martin / HHMI · NIGMS · mô phỏng phân tử</p></div>'
slide('Degron tham gia quá trình phân hủy protein','Sinh học và bài toán',
      '<div class="split equal"><div class="stack centered">'+visual(ups())+'<p class="small">Degron: tín hiệu giúp hệ thống phù hợp nhận diện cơ chất cần phân hủy.</p></div>'+video+'</div>',
      'Nhận diện → gắn ubiquitin → proteasome xử lý protein.',
      'Sơ đồ đơn giản hóa hệ ubiquitin–proteasome, không mô tả mọi cơ chế phân hủy. E3 cùng các thành phần phù hợp góp phần nhận diện cơ chất. Video NIGMS 3764 của Andreas Martin/HHMI mô phỏng cơ chất gắn chuỗi ubiquitin, được máy AAA+ kéo mở; ubiquitin được tách trước khi cơ chất bị cắt. Video không là quan sát của dataset Zhang. Màu phân tử trong video theo tác giả, khác quy ước màu của sơ đồ.',[NIGMS,'https://www.nigms.nih.gov/image-gallery',PAPER])

slide('Một phép thay có thể làm thay đổi tín hiệu','Sinh học và bài toán',visual(mutation()),
      'WT là trình tự tham chiếu; mutant khác WT ở một amino acid.',
      'Ví dụ giả định MAGLSKVT thành MAGPSKVT, L4P. Thay thế có thể làm thay đổi hoạt động degron, song cũng có thể tác động qua cơ chế khác hoặc không có ảnh hưởng đáng kể. Không gán sự thay L/P này cho một degron đã được đo.',[PAPER])

slide('532 phép thay tạo nhu cầu ưu tiên thí nghiệm','Sinh học và bài toán',visual(mutation_space()),
      'Biết hoạt tính cả đoạn chưa xác định được phép thay nào nên thử trước.',
      '28 vị trí nhân 19 amino acid khác WT là 532 thay thế đơn tối đa. Ma trận có 20 hàng AA; ô WT→WT bị mask. Một peptide chỉ có dưới hoặc bằng 532 ô đo hợp lệ sau QC. Hình là sơ đồ thiết kế, không là dự đoán hay nhãn thực nghiệm.',[DATA_PATH])

slide('GPS chuyển tín hiệu huỳnh quang thành PSI','Sinh học và nhãn',
      badge('Minh họa nguyên lý đo · histogram không phải dữ liệu thực')+visual(gps()),
      'PSI càng cao: reporter càng bền trong hệ đo Zhang.',
      'GFP được gắn peptide; DsRed làm tín hiệu tham chiếu. Tế bào được phân sáu bin theo tỷ lệ GFP/DsRed, rồi giải trình tự để đếm construct. PSI là trung bình có trọng số theo các bin sau chuẩn hóa. Thang Zhang 1–6. Không đọc chiều cao histogram minh họa như số đo thật.',[PAPER,'research/full-data-audit/psi-build.json'])

slide('ΔPSI là hiệu ứng mà mô hình cần dự đoán','Sinh học và nhãn',
      badge('Ví dụ giả định')+visual(delta_example()),
      'Đầu ra là một giá trị liên tục: bài toán hồi quy.',
      'ΔPSI=PSI(mutant)−PSI(WT). Giá trị dương cho thấy reporter mutant bền hơn trong assay này; có thể phù hợp với degron bị suy yếu nhưng chưa xác định cơ chế. Không suy ra half-life định lượng, tác động trên protein nguyên vẹn hoặc gây bệnh. Ví dụ 2,5 và 3,8 không phải số liệu repo.',[PAPER])

slide('Saturation và scanning có độ phủ bổ sung','Dữ liệu',
      badge('Sơ đồ thiết kế · các ô màu biểu thị phép thay được khảo sát')+visual(designs()),
      'Saturation phủ nhiều loại thay thế; scanning mở rộng ngữ cảnh trình tự.',
      'Scanning dùng replacement phụ thuộc WT, theo các hướng R/A/S; trên alphabet tạo 20 kiểu WT→mutant trong 380 kiểu có hướng không đồng nghĩa. Saturation khảo sát 19 AA thay thế mỗi vị trí khi đủ dữ liệu. Không giả định mọi ô trong thiết kế đều qua QC.',[PAPER,'research/scan-sat-merge-2026-10-23/README.md'])

slide('Mỗi ô đột biến trở thành một bản ghi có nhãn','Dữ liệu',
      badge('Ví dụ khóa mẫu · giá trị trình tự minh họa')+visual(record_diagram()),
      'Đối chiếu đúng peptide, vị trí, phép thay và mốc WT trước khi tính ΔPSI.',
      'Mutation cell là khóa peptide/vị trí/WT/mutant, không là một protein độc lập. Scanning dùng mut0 đúng replicate. Saturation không có mut0; WT nội tại lấy trung vị các ô đồng nghĩa hợp lệ của từng nửa thí nghiệm. Không dùng BAG6 WT như replicate hoặc mốc saturation.',[DATA_PATH,'research/full-data-audit/saturation-matrix.json'])

slide('Dữ liệu sau QC giữ toàn dải PSI','Dữ liệu',
      '<div class="data-overview"><div><p class="eyebrow">Saturation</p><div class="big-number">122.412</div><p>ô đột biến · <strong>235 peptide</strong></p><div class="count-rule"></div><p class="small">Benchmark hiệu ứng ΔPSI</p></div><div><p class="eyebrow">Scanning</p><div class="big-number">224.470</div><p>ô đột biến sau QC</p><div class="count-rule"></div><p class="small">Học chuyển tiếp và đánh giá nguồn giữ lại</p></div></div><p class="data-bottom">235 peptide saturation thuộc <strong>221 nhóm protein</strong> trong W.<br>Giữ QC kỹ thuật; khảo sát phạm vi train bằng các ngưỡng PSI.</p>',
      'Số ô đột biến, số peptide và số nhóm protein là các đơn vị khác nhau.',
      'Số liệu được đọc từ dataset-build.json: saturation_cells 122412, saturation_peptides 235, saturation_groups 221, scan_cells 224470. Số scanning là toàn bộ sau QC, không phải số ô đều được dùng pretrain: scan_dev, scan_T và sat_overlap có vai trò riêng. Theo chỉnh sửa của người dùng, không trình bày các phiên bản dữ liệu hoặc so sánh tiến trình phiên bản.',[DATA_PATH])

slide('Pipeline nối dữ liệu, mô hình và công cụ','Quy trình học máy',
      visual(process(['Dữ liệu Zhang','QC và nhãn','Chia nhóm','Đặc trưng','Mô hình'],['Saturation / scanning','PSI → ΔPSI','Protein tương đồng','Sequence-only','Đối chứng rõ ràng']))+'<div class="pipeline-ending"><span>Đánh giá theo nhóm</span><b>→</b><span>Khóa và kiểm chứng</span><b>→</b><span>Công cụ hỗ trợ phân tích</span></div>',
      'Mỗi bước xử lý cần có lý do, đầu ra và bằng chứng truy vết.',
      'Sơ đồ định hướng nội dung. Các mô hình và so sánh ở benchmark development không tự chuyển thành model sản phẩm. Việc khóa cấu hình, calibration, tập T và kiểm chứng ngoài vẫn chưa hoàn tất theo snapshot tài liệu.',[DATA_PATH,'research/README.md'])

slide('Trình tự là đầu vào; PSI dùng để tạo nhãn','Quy trình học máy',visual(input_label()),
      'Khi dự đoán một phép thay mới, mô hình không được nhận PSI thực nghiệm.',
      'Input chính chỉ có WT sequence, vị trí và mutant AA. Không đưa PSI WT/mutant, read count, group/fold hoặc stratum vào feature. Tính ΔPSI từ hai phép đo là chuẩn bị nhãn; không phải cung cấp sẵn nhãn khi inference.',[FEATURE_PATH,DATA_PATH])

slide('Giữ cùng nhóm protein khi chia dữ liệu','Quy trình học máy',visual(folds()),
      'Năm outer folds đánh giá trên các nhóm được giữ ngoài huấn luyện.',
      'Chia theo nhóm tương đồng, chặn trùng sequence xuyên scanning/saturation. Trong mỗi outer fold, tuning và preprocessing chỉ dùng inner train/validation; sau đó refit trên outer train rồi đo outer test. Seed 17/29/43. 221 nhóm là đơn vị lấy mẫu lại cho CI. Các nhóm heuristic không chứng minh độc lập sinh học tuyệt đối.',[DATA_PATH,'research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md'])

slide('Ridge là đối chứng cho giá trị của ngữ cảnh','Mô hình và giả thuyết',visual(ridge()),
      'Câu hỏi: đặc trưng trình tự và một mô hình tuyến tính đã dự đoán được bao nhiêu?',
      'Ordered radius=5 tạo 40 feature WT/mutant, 20 composition và 200 ordered-neighbour features, tổng 260. Vị trí đột biến không đưa vào một cột số độc lập; dùng để lấy ngữ cảnh. Ridge regularization hạn chế trọng số lớn. Không khẳng định deep learning mặc nhiên hơn Ridge.',[FEATURE_PATH,ANALYSIS_PATH])

slide('One-hot CNN học các mẫu trình tự cục bộ','Mô hình và giả thuyết',
      badge('Sơ đồ one-hot rút gọn · không phải ma trận số đầy đủ')+visual(onehot()),
      'Đối chứng one-hot giúp kiểm tra lợi ích bổ sung của biểu diễn ESM.',
      'Head thực dùng crop 15 vị trí, 20 one-hot channels cộng chỉ báo trung tâm và 60 feature phép thay/thành phần. CNN kernel=5; đây là đối chứng cùng họ head khi không có delta ESM. Hình chỉ thể hiện nguyên lý.',[NEURAL_PATH,FEATURE_PATH])

slide('ESM2 biến trình tự thành biểu diễn số','Mô hình và giả thuyết',
      badge('Sơ đồ biểu diễn · màu các ô minh họa vector')+visual(plm()),
      'Hiệu embedding mô tả sự thay đổi biểu diễn giữa mutant và WT.',
      'WT và mutant qua cùng ESM2 pretrained; ΔH=H_mutant−H_WT. Ở head CNN, dùng crop quanh site và projection, kết hợp one-hot WT, center indicator và 60 feature phụ. Không mô tả các chiều embedding như đại lượng sinh học đo trực tiếp. Benchmark đang trình bày chỉ có ESM2-35M.',[NEURAL_PATH,ANALYSIS_PATH])

slide('Pointwise và CNN khác cách trộn vị trí','Mô hình và giả thuyết',visual(head_comparison()),
      'Embedding ESM đã có ngữ cảnh; kernel 5 trộn thêm các vị trí ở head.',
      'Pointwise dùng Conv1D kernel1; CNN dùng kernel5. Head còn max-pooling và center pooling, nên pointwise không đồng nghĩa toàn mô hình bỏ qua mọi vị trí khác. Số tham số head khác nhau; so sánh không cô lập hoàn toàn tác động trộn vị trí khỏi sức chứa. Cả hai giữ đầu vào phụ nhất quán.',[NEURAL_PATH,ANALYSIS_PATH])

slide('mCNN khảo sát nhiều độ rộng ngữ cảnh','Mô hình và giả thuyết',visual(head_comparison(True)),
      'Câu hỏi: kernel 3, 5 và 7 có cải thiện dự đoán so với một kernel?',
      'Mỗi nhánh có convolution, activation, max-pooling và center pooling. Các đặc trưng nhánh nối với feature phụ trước regression head. Đây là thiết kế đang được so sánh, không là bằng chứng nhiều kernel vượt một kernel.',[NEURAL_PATH])

slide('Frozen và LoRA học những tham số khác nhau','Mô hình và giả thuyết',visual(tuning()),
      'Lợi ích thích nghi PLM cần được đánh giá cùng chi phí và độ ổn định.',
      'Frozen chỉ cập nhật head. LoRA giữ weights backbone nền và học adapter tham số hạng thấp cùng head. Đây là nhánh fine-tuning riêng, không đồng nhất trực tiếp với CNN trên feature cache. Trong snapshot Kaggle chỉ frozen seed17 hoàn thành, LoRA chưa đủ OOF; chưa có phép so LoRA/frozen đầy đủ.',[ANALYSIS_PATH,'research/README.md'])

slide('Sai số, xếp hạng và CI trả lời các câu hỏi riêng','Đánh giá',
      visual(metric_concepts())+'<p class="metric-note">MAE đo sai số hồi quy · AUROC/AP đánh giá sự kiện dương bổ sung</p>',
      'MAE thấp hơn tốt hơn; AUROC/AP cao hơn tốt hơn trên cohort đủ điều kiện.',
      'MAE tính macro theo 235 peptide. AUROC/AP dương dùng 184 peptide đủ ≥3 ô mỗi lớp; không là accuracy. AP phụ thuộc tỷ lệ event. Bootstrap 5000 theo 221 nhóm protein, không resample 122412 ô như độc lập. MAE là metric chính cho hồi quy; AUROC đánh giá xếp hạng sự kiện phụ. Phần uncertainty đặt ở CI chênh lệch, không là xác suất từng mutation.',[ANALYSIS_PATH])

slide('Thí nghiệm A: nên học trên phạm vi PSI nào?','Thí nghiệm và kết quả',visual(training_scopes()),
      'Ngưỡng PSI chọn phạm vi train; mọi cấu hình được so trên cùng W.',
      'Các cấu hình trong protocol gọi A/B/C/D/E, nhưng màn chiếu dùng tên phạm vi dễ đọc. Test W giữ 235 peptide cùng 221 nhóm. PSI≤3/4/5 không là nhãn degron/non-degron tuyệt đối. Balanced thay trọng số trong train, không đổi population test.',[ANALYSIS_PATH,DATA_PATH])

improvement=(metric('ordered-w5-B')-metric('ordered-w5-D'))/metric('ordered-w5-B')*100
slide('Học toàn dải giúp Ridge giảm sai số hồi quy','Thí nghiệm và kết quả',
      '<div class="charts-two"><div><p class="chart-label">Cùng tập đánh giá W · MAE ↓</p>'+image('training-range.svg','MAE Ridge theo phạm vi PSI train')+'</div><div><p class="chart-label">Lợi ích khác nhau giữa các miền PSI</p>'+image('strata.svg','MAE Ridge theo miền PSI của test')+'</div></div>',
      f'Toàn dải giảm MAE khoảng <strong>{fmt(improvement,2)}%</strong> so với chỉ học PSI ≤ 4.',
      'Hai biểu đồ tái sử dụng từ deck trước; số liệu và hash nguồn được kiểm lại. D−B có CI97,5% điều chỉnh cho hai phép so chính, hỗ trợ cải thiện nhưng chưa chứng minh giảm ít nhất 0,02 PSI trên toàn CI. Cân bằng tốt hơn ở PSI cao, có đánh đổi ở miền thấp. Stratum PSI>5 không có event Δ≥1 hợp lệ; AUROC dương không xác định.',[ANALYSIS_PATH])

head_keys=['ordered-w5-D','esm2_35m-pointwise-D','esm2_35m-cnn-D','esm2_35m-mcnn-D','esm2_35m-mcnn-E']
head_names=['Ridge ngữ cảnh','ESM + Pointwise','ESM + CNN','ESM + mCNN','ESM + mCNN cân bằng']
explorer=[dict(recipe=k,name=n,mae=metric(k),auroc=metric(k,'auroc_plus'),ap=metric(k,'auprc_plus')) for k,n in zip(head_keys,head_names)]
slide('Thí nghiệm B: ESM2 và CNN có ích đến đâu?','Thí nghiệm và kết quả',
      '<div class="metric-picker"><button data-metric="mae" aria-pressed="true">MAE ↓</button><button data-metric="auroc" aria-pressed="false">AUROC dương ↑</button><button data-metric="ap" aria-pressed="false">AP dương ↑</button></div><div class="chart-explorer"><canvas id="recipeChart" aria-label="So sánh mô hình theo MAE AUROC và AP"></canvas><div class="print-fallback">'+bars(head_names,[x['mae'] for x in explorer],[LINE,BLUE,GREEN,DARK,CORAL])+'</div></div>',
      'Cùng W · ensemble ba seed · ESM2-35M · số liệu development.',
      'Bảng chính khớp bản paste: MAE Ridge 0,4078; pointwise 0,3897; CNN 0,3844; mCNN 0,3850; mCNN balanced 0,3838. Bốn dòng đầu cùng train toàn dải, dòng cuối đổi weighting. AUROC dương lần lượt khoảng 0,8319/0,8375/0,8488/0,8463/0,8470. Các nút đổi metric; PDF dùng bản MAE tĩnh. Chưa là kết quả locked T hoặc mô hình sản phẩm.',[ANALYSIS_PATH])

contrast=details['contrasts']['esm2_35m-mcnn-E minus esm2_35m-cnn-D; mae']
slide('Chênh lệch nhỏ cần được đọc cùng khoảng tin cậy','Thí nghiệm và kết quả',
      split(image('mcnn-ci.svg','Chênh lệch MAE mCNN cân bằng so CNN toàn dải và CI 95%'),
            '<span class="number">−0,000508</span><p>PSI · chênh lệch MAE</p><p>CI đi qua <strong>0</strong>.</p><p class="small">Hai cấu hình còn khác trọng số train.</p>'),
      'Chưa đủ bằng chứng kết luận mCNN vượt CNN.',
      f'Phép so trực tiếp mCNN-E minus CNN-D: delta={contrast["delta"]}; CI95 mô tả={contrast["ci95"]}, 5000 bootstrap theo nhóm. Đây là so sánh cả kiến trúc và train weighting; cùng train D, mCNN−CNN cũng chưa phân giải. CI ngoài phép so phạm vi train chính là mô tả, không hiệu chỉnh toàn bộ chọn recipe.',[DETAILS_PATH,ANALYSIS_PATH])

slide('Thí nghiệm C: chuyển giao còn những câu hỏi mở','Thí nghiệm và kết quả',
      split(image('transfer.svg','MAE one-hot CNN scratch và pretrain scanning'),
            '<p><strong>Scanning → saturation</strong><br>Cải thiện so với one-hot CNN học trực tiếp.</p><p><strong>ESM + scanning</strong><br>Chưa có phép so kết hợp trong snapshot.</p><p><strong>LoRA so với frozen</strong><br>Chưa đủ OOF để kết luận.</p>'),
      'Lợi ích chuyển giao phụ thuộc đầu vào, thiết kế và đối chứng.',
      'CNN transfer rep1 giảm MAE khoảng 0,006385 so scratch, CI95 mô tả [-0,009929;-0,003013]. Đây là one-hot CNN và saturation OOF, không là ESM+scanning hay kiểm chứng locked T. Mean12 chưa vượt rep1; quality weighting hiện có kết quả âm. Snapshot LoRA chưa đầy đủ. Không gộp chi phí/runtime hoặc kết quả local đang mở vào benchmark Kaggle.',[ANALYSIS_PATH,DETAILS_PATH])

slide('Ma trận hỗ trợ lựa chọn đột biến để kiểm chứng','Công cụ hỗ trợ phân tích',
      badge('Minh họa luồng sử dụng')+visual(priority())+'<div class="workflow"><span>Nhập peptide</span><span>Xem ma trận</span><span>Chọn phép thay</span><span>Xem chi tiết</span><span>Xuất kết quả</span></div>',
      'Dự đoán cung cấp danh sách ưu tiên cho thí nghiệm tiếp theo.',
      'Các ô và thanh trên hình minh họa luồng; không phải điểm inference. Công cụ cần giữ model/source version và miền áp dụng. Không đọc ΔPSI như xác suất bệnh hoặc kết luận cơ chế E3. Nếu có xác suất sự kiện, calibrator phải được đánh giá riêng cho model.', ['system/README.md'])

slide('Phân biệt baseline phục vụ và prototype giao diện','Công cụ hỗ trợ phân tích',
      '<div class="split ui-split"><div class="ui-frame">'+image('workspace-prototype.png','Prototype Workspace UI sử dụng fixture tổng hợp')+'<div class="ui-badge">Prototype · dữ liệu tổng hợp · chưa nối backend</div></div><div class="aside"><p><strong>Baseline đã có mã nguồn</strong><br>React + TypeScript<br>FastAPI</p><p class="small">Model phục vụ:<br><code>m3-ext4.0-platt-v1</code></p><p><strong>Model nghiên cứu mới</strong><br>Còn cần refit, kiểm chứng và tích hợp.</p></div></div>',
      'Điểm số trong ảnh minh họa giao diện là fixture tổng hợp.',
      'Screenshot tái sử dụng của Workspace UI v2, không là ứng dụng React baseline hoặc inference thật. PostgreSQL, persistent projects/history, batch jobs, protein tiling web flow, import/comparison còn phải triển khai/kiểm chứng. Model serving vẫn m3-ext4.0-platt-v1. Các test baseline ghi trong tài liệu là lịch sử, không được chạy lại trong phiên tạo deck.', ['system/README.md','system/design/workspace-ui-v2/README.md'])

slide('Những phần đã có và những phần cần hoàn thiện','Trạng thái và đóng góp',
      rows_table(['Hạng mục','Trạng thái theo tài liệu'],[
          ['Dữ liệu, QC và phép chia nhóm','Đã dựng và có hồ sơ truy vết'],
          ['Ridge / ESM2 / CNN / mCNN','Có kết quả development'],
          ['Mở rộng PLM / frozen–LoRA','Đang tiếp tục, chưa có kết luận cuối'],
          ['Calibration / T / nguồn ngoài','Chưa hoàn tất cho ứng viên mới'],
          ['FastAPI + React baseline','Đã có mã nguồn'],
          ['Workspace và tích hợp model mới','Còn cần triển khai / kiểm chứng']]),
      'Mốc tài liệu 03/11/2026 · kết quả nghiên cứu và tiến độ phần mềm được đọc riêng.',
      'Snapshot Kaggle cập nhật 01/11 11:18:07Z, phân tích ngày 02/11. Bản ghi local 03/11 12:38 UTC+8 ghi 456 job complete kế thừa, 178 pending, một checkpoint LoRA paused: ảnh chụp tiến độ, không xác nhận worker đang sống hoặc 635 thí nghiệm độc lập. Không dùng trạng thái job thay benchmark. Chưa đóng G2/G3.', ['research/README.md','system/README.md'])

slide('Đóng góp gắn với các bằng chứng có thể kiểm tra','Trạng thái và đóng góp',
      '<div class="contributions"><div><span class="chapter-number">01</span><h3>Dữ liệu và benchmark</h3><p>Nhãn, QC, provenance<br>và chia nhóm protein</p></div><div><span class="chapter-number">02</span><h3>Bằng chứng phương pháp</h3><p>Phạm vi PSI, biểu diễn,<br>head và học chuyển tiếp</p></div><div><span class="chapter-number">03</span><h3>Công cụ nghiên cứu</h3><p>Ma trận, ưu tiên phép thay<br>và truy vết kết quả</p></div></div>',
      'Giá trị nghiên cứu cần được chứng minh bằng phép so và phạm vi kết luận rõ ràng.',
      'Đây là các trục đóng góp đang phát triển. Đã có dữ liệu/benchmark và kết quả development, nhưng kiểm chứng cuối cùng và phần mềm mở rộng chưa hoàn tất. Không tuyên bố một kiến trúc mới, mọi protein đều tổng quát hóa tốt hoặc website là tính mới độc quyền.',[ANALYSIS_PATH,'system/README.md'])

slide('Khóa lựa chọn rồi kiểm chứng trước khi tích hợp','Hướng tiếp theo',
      '<div class="roadmap"><p class="eyebrow">Nghiên cứu mô hình</p>'+visual(road_steps(['Khóa cấu hình','Refit / export','Hiệu chuẩn','Đánh giá T'],['Chọn từ development','Đúng model đã chọn','Theo model / sự kiện','Theo protocol đã khóa']))+'<p class="eyebrow">Phát triển công cụ</p>'+visual(road_steps(['Tích hợp model','Workspace / lưu trữ','Kiểm chứng ứng dụng'],['Model card / miền áp dụng','Dữ liệu và lịch sử local','Phép tính / luồng sử dụng']))+'</div>',
      'Mở rộng PLM và LoRA cần phép so đầy đủ; mô hình mới cần quy trình phục vụ riêng.',
      'Stage final promotion hiện hỗ trợ Ridge ngữ cảnh; CNN cần final refit/export riêng. Cần khóa cấu hình/calibration trước đọc T. T của các thiết kế có lịch sử tiếp xúc khác nhau; mô tả đúng held-source thay vì mặc định hoàn toàn độc lập. Nguồn ngoài phải kiểm endpoint/provenance. Nghiên cứu model và phần mềm có thể làm song song.', ['research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md','system/README.md'])

slide('Từ trình tự đến một giả thuyết có thể kiểm chứng','Nhìn lại đề tài',visual(summary_chain()),
      'Mục tiêu: dự đoán hiệu ứng của từng phép thay để hỗ trợ nghiên cứu.',
      'Kết nối sinh học, nhãn thực nghiệm, đầu vào sequence-only, benchmark theo nhóm và công cụ. Bằng chứng đang có ủng hộ khảo sát ESM2 với CNN, nhưng chưa là kiểm chứng độc lập trên mọi nguồn hay hoàn tất sản phẩm. Slide lộ trình học sáu buổi đã được bỏ theo annotation của người dùng.',[ANALYSIS_PATH,'system/README.md'])

assert len(slides)==31

slide('Các thuật ngữ dùng trong deck','Phụ lục · thuật ngữ',rows_table(['Thuật ngữ','Cách hiểu trong đề tài'],[
    ['Residue / peptide','Một đơn vị AA trong chuỗi / một đoạn chuỗi ngắn'],
    ['WT / mutant','Trình tự tham chiếu / trình tự sau thay thế'],
    ['PSI / ΔPSI','Chỉ số độ bền reporter / thay đổi so với WT'],
    ['Embedding / head','Biểu diễn số / phần học dự đoán từ biểu diễn'],
    ['Fold / OOF','Phần chia nhóm / dự đoán khi mẫu nằm ngoài train'],
    ['Calibration / CI','Hiệu chuẩn xác suất / khoảng tin cậy thống kê']]),
    'Reporter stability là endpoint của phép đo đang dùng.',
    'Các định nghĩa chỉ phục vụ đọc deck. CI metric không là uncertainty interval cho từng dự đoán. PSI không là thời gian bán hủy; ΔPSI không là xác suất gây bệnh.',[PAPER,ANALYSIS_PATH],appendix=True)

slide('Từ read counts đến ΔPSI cần đúng mốc WT','Phụ lục · tạo nhãn',visual(label_pipeline())+
      '<p class="formula">PSI = Σ(bin × số đọc đã chuẩn hóa) / Σ(số đọc đã chuẩn hóa)</p>',
      'Read depth, replicate, chuỗi và tọa độ đều cần được kiểm trước khi giữ ô.',
      'Không dùng trực tiếp raw bin counts chưa chuẩn hóa vào công thức. PSI nguồn có bước chuẩn hóa theo bin/điều kiện; kiểm tái dựng 261865 giá trị khớp tác giả trong 5e-7 theo audit. Saturation reads≥10, ≥10 ô đồng nghĩa mỗi nửa và mutation cell có cả hai nửa hợp lệ. Mốc WT khác giữa saturation và scanning; BAG6 WT là điều kiện khác. Chỉ mô tả audit đã có, không tính lại dữ liệu thô trong phiên này.', ['research/full-data-audit/psi-build.json','research/full-data-audit/saturation-matrix.json',DATA_PATH],appendix=True)

slide('Ví dụ HIF1A: đọc ma trận nhãn thực nghiệm','Phụ lục · ví dụ thực nghiệm',
      split(image('hif-measured.svg','Ma trận nhãn delta PSI thực nghiệm của peptide HIF1A'),
            '<span class="number">529 / 532</span><p>phép thay có nhãn đo</p><p class="small">Cột: vị trí trong peptide<br>Hàng: AA thay vào<br>Màu: giá trị ΔPSI</p>'+badge('Nhãn đo thực nghiệm')),
      'Những vị trí khác nhau có thể phản ứng rất khác với phép thay.',
      'Q16665_HIF1A_25, tọa độ protein 553–580, WT PSI nội tại 2,1865. Có 529 ô đo, 186 ô ΔPSI≥1. Chọn ví dụ theo ≥500 ô và số ô dương lớn nhất, tie ID. Hình đo được tái sử dụng, không là inference mới hoặc phát hiện cơ chế HIF1A/VHL. Ô WT và thiếu được mask; không gán zero cho ô thiếu.', ['research/slide-figures-2026-10-15/example-matrix.json'],appendix=True)

slide('Bảng kết quả và đơn vị đánh giá','Phụ lục · metric và CI',
      rows_table(['Mô hình / phạm vi train','MAE ↓','AUROC dương ↑','AP dương ↑'],[
          [x['name'],fmt(x['mae']),fmt(x['auroc']),fmt(x['ap'])] for x in explorer])+
      '<div class="cohort-note">MAE: 235 peptide / 221 nhóm · AUROC và AP dương: 184 peptide đủ điều kiện<br>Ensemble seed 17, 29, 43 · năm outer folds · CI bootstrap theo nhóm protein</div>',
      'Bốn dòng đầu train toàn dải; mCNN cân bằng thay trọng số train.',
      'Các metric tính macro theo peptide, event dương Δ≥1, mỗi peptide ≥3 ô mỗi lớp. Đây là OOF development. AUROC khác cohort không so trực tiếp. MAE mCNN cân bằng−CNN toàn dải CI95 [-0,003157;+0,002223]. Chênh lệch CNN−pointwise CI95 [-0,010173;-0,000899], nhưng head capacity khác nhau.',[ANALYSIS_PATH,DETAILS_PATH],appendix=True)

ref_cards=[('Bài gốc và dữ liệu',PAPER,'Zhang và cộng sự · Molecular Cell 2023'),
           ('Dữ liệu và số liệu sau QC','../../research/kaggle-roadmap-2026-10-31/dataset-build.json','Kiểm kê ô, peptide, nhóm protein'),
           ('Kết quả và điều kiện so sánh','../../research/kaggle-roadmap-2026-10-31/output-analysis.md','Snapshot Kaggle · phân tích ngày 02/11'),
           ('Nguồn ngoài và mô hình đối chứng','../../research/README.md','Các audit PAP, Degformer và hồ sơ lịch sử'),
           ('Phạm vi phần mềm','../../system/README.md','Baseline, prototype và công việc còn mở'),
           ('Nguồn hình, video và ghi chú','asset-notices.md','Attribution, giấy phép và thay đổi tài sản')]
slide('Nguồn và bằng chứng có thể tra cứu theo chủ đề','Phụ lục · nguồn',
      '<div class="paper-source"><figure>'+image('zhang-graphical-abstract.png','Graphical abstract bài Zhang 2023, cắt từ bản PDF tác giả')+'<figcaption>Zhang và cộng sự, 2023 · Graphical abstract · CC BY 4.0</figcaption></figure><div class="references">'+''.join(f'<div><a href="{url}" target="_blank" rel="noopener">{name}</a><p>{desc}</p></div>' for name,url,desc in ref_cards)+'</div></div>',
      'Mở “Ghi chú” để xem nguồn và giới hạn của slide hiện tại.',
      'Nhãn tác giả, nhãn đo, minh họa, fixture và đề xuất được phân biệt. Hình/gif/video và mọi figure có nguồn, hash trong evidence.json. Các audit baseline PAP/Degformer và R0–R6 là lịch sử, khác population/protocol; không nối thành một đường tiến bộ hoặc so AUROC trực tiếp với W. Tài liệu bài báo có erratum Figure2A, DOI10.1016/j.molcel.2023.10.021; deck không dùng Figure2A. Không hiển thị các phiên bản dữ liệu trên màn chiếu.',[PAPER,'research/README.md','asset-notices.md'],appendix=True)

assert len(slides)==36

def href(source):
    if source.startswith('http'):return source
    if (HERE/source).exists():return source
    return '../../'+source

parts=[]
for s in slides:
    body=s['body']
    if re.search(r'dữ liệu\s+v[123]\b|lộ trình học|sáu buổi',re.sub('<[^>]+>',' ',s['title']+' '+body+' '+s['insight']),re.I):
        raise ValueError('Removed content appears on slide '+str(s['number']))
    header='' if s['number']==1 else f'<header><p class="eyebrow">{s["section"]}</p><h2>{s["title"]}</h2></header>'
    note=f'<p>{esc(s["notes"])}</p><h3>Nguồn truy vết</h3><ul>'+''.join(f'<li><a href="{esc(href(ref),quote=True)}" target="_blank" rel="noopener">{esc(ref)}</a></li>' for ref in s['sources'])+'</ul>'
    parts.append(f'<section class="slide {"dark" if s["dark"] else ""}" data-title="{esc(s["title"],quote=True)}" data-section="{s["section"]}" data-appendix="{str(s["appendix"]).lower()}" aria-label="{esc(s["title"],quote=True)}">{header}<div class="body">{body}</div><div class="insight">{s["insight"]}</div><aside class="speaker-notes">{note}</aside></section>')

html='''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>'''+esc(PROJECT_TITLE)+'''</title><link rel="stylesheet" href="deck.css"><link rel="stylesheet" href="explain.css"><script src="data.js" defer></script><script src="vendor/chart.umd.js" defer></script><script src="deck.js" defer></script></head><body><main id="viewport" aria-label="Bộ slide giải thích đề tài Degron"><div id="deck">'''+''.join(parts)+'''</div></main><div id="progress" aria-hidden="true"></div><nav id="toolbar" aria-label="Điều khiển trình chiếu"><button id="prev" aria-label="Bước trước">←</button><span class="counter" id="counter"></span><button id="next" aria-label="Bước tiếp">→</button><button id="overview-button">Mục lục</button><button id="notes-button">Ghi chú</button><button id="motion" aria-pressed="false">Dừng chuyển động</button><button class="long" id="full-button">Toàn màn hình</button><button id="help-button" aria-label="Hướng dẫn phím tắt">?</button></nav><div id="status" role="status" aria-live="polite"></div><dialog id="overview"><button class="close">Đóng</button><h2>Mục lục · 31 slide chính + 5 phụ lục</h2><div id="overview-grid"></div></dialog><dialog id="notes"><button class="close">Đóng</button><h2 id="notes-title"></h2><div id="notes-body"></div></dialog><dialog id="help"><button class="close">Đóng</button><h2>Điều khiển trình chiếu</h2><p>← → / Space: hiện từng bước rồi chuyển slide<br>Shift + ← →: chuyển thẳng slide<br>O: mục lục · N: ghi chú và nguồn<br>M: dừng / tiếp tục chuyển động · F: toàn màn hình<br>Home: về đầu · End: slide kết<br>Chạm nút hoặc vuốt ngang trên điện thoại.<br>PDF hiển thị đủ mọi bước với hình tĩnh thay thế video.</p></dialog></body></html>'''
(HERE/'index.html').write_text(html,encoding='utf8')
public=[{k:v for k,v in s.items() if k not in ['body','dark']} for s in slides]
(HERE/'slide-sources.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
notes_document='# Ghi chú người trình bày\n\n'+''.join(f'## {s["number"]}. {s["title"]}\n\n{s["notes"]}\n\nNguồn: '+', '.join(s['sources'])+'\n\n' for s in slides)
(HERE/'speaker-notes.md').write_text(notes_document.rstrip()+'\n',encoding='utf8')
(HERE/'data.js').write_text('window.DECK_DATA = '+json.dumps(dict(explorer=explorer),ensure_ascii=False)+';\n',encoding='utf8')
assets={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for directory in ['assets','vendor'] for p in (HERE/directory).rglob('*') if p.is_file()}
(HERE/'evidence.json').write_text(json.dumps(dict(source_sha256=sources,asset_sha256=assets,counts=dataset,
    compared_recipes=explorer,mcnn_minus_cnn=contrast,scientific_scope='Saved development results; no training, locked-T access or serving-model promotion',
    generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Built 31 main slides and 5 appendices, with speaker notes and evidence hashes.')
