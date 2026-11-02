"""Build a 34-slide faculty research briefing and 16 visual appendices."""
from pathlib import Path
from html import escape as esc
import json
import math
import textwrap

HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'data/README.md').exists())
R=TOPIC/'research'
evidence=json.loads((HERE/'evidence.json').read_text(encoding='utf8'))
a=json.loads((R/'kaggle-roadmap-2026-10-31/output-analysis.json').read_text(encoding='utf8'))
d=json.loads((R/'kaggle-roadmap-2026-10-31/output-analysis-details.json').read_text(encoding='utf8'))
hif=json.loads((R/'slide-figures-2026-10-15/example-matrix.json').read_text(encoding='utf8'))
GREEN='#18974C'; DARK='#0A5032'; CORAL='#C76242'; BLUE='#477CA7'; INK='#193A2B'; SAGE='#D0DEBB'; LINE='#D6DFD3'
slides=[]

def text(x,y,value,size=22,color=INK,anchor='middle',weight=400):
    vals=value if isinstance(value,list) else str(value).split('\n')
    return ''.join(f'<text x="{x}" y="{y+i*(size*1.32)}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{esc(str(v))}</text>' for i,v in enumerate(vals))

def box(x,y,w,h,label,sub='',color=GREEN):
    lines=label if isinstance(label,list) else textwrap.wrap(label,width=max(11,int(w/12)))
    sy=y+h/2-(len(lines)-1)*14+7
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="white" stroke="{color}" stroke-width="2"/>'
    s+=text(x+w/2,sy,lines,22,color,weight=600)
    if sub:s+=text(x+w/2,y+h+32,textwrap.wrap(sub,22),18)
    return s

def edge(x1,y1,x2,y2,color=GREEN,moving=True,delay=0):
    angle=math.atan2(y2-y1,x2-x1);wing=9
    p1=(x2-wing*math.cos(angle-.45),y2-wing*math.sin(angle-.45));p2=(x2-wing*math.cos(angle+.45),y2-wing*math.sin(angle+.45))
    s=f'<path d="M{x1} {y1} L{x2} {y2} M{p1[0]} {p1[1]} L{x2} {y2} L{p2[0]} {p2[1]}" stroke="{color}" stroke-width="2.2" fill="none"/>'
    if moving:s+=f'<circle class="flow" cx="{x1}" cy="{y1}" r="5" fill="{color}" style="--dx:{x2-x1}px;--dy:{y2-y1}px;animation-delay:-{delay}s"/>'
    return s

def svg(contents,label='Sơ đồ minh họa',w=1100,h=430):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label,quote=True)}"><title>{esc(label)}</title>{contents}</svg>'

def process(labels,subs=None,colors=None):
    n=len(labels);gap=34;w=min(210,(1080-(n-1)*gap)/n);total=n*w+(n-1)*gap;x0=(1100-total)/2;s=''
    for i,label in enumerate(labels):
        x=x0+i*(w+gap);col=(colors or [GREEN]*n)[i]
        s+=box(x,142,w,100,label,(subs or ['']*n)[i],col)
        if i<n-1:s+=edge(x+w+2,192,x+w+gap-5,192,col,delay=i)
    return svg(s,'Quy trình: '+'; '.join(labels))

def sequence(x=50,y=130,sequence=None,step=30,highlight=11,mutant=False):
    seq=sequence or hif['sequence'];s=''
    for i,aa in enumerate(seq):
        hot=i==highlight;fill=CORAL if hot else SAGE
        s+=f'<rect x="{x+i*step}" y="{y}" width="{step-3}" height="34" rx="3" fill="{fill}"/>'
        s+=text(x+i*step+(step-3)/2,y+24,('D' if mutant and hot else aa),18,'white' if hot else INK,weight=600)
    return s

def heat(x=0,y=0,cw=16,ch=12,design=False,scan=False):
    aa=hif['aa_order'];s=''
    for j,letter in enumerate(aa):
        for i,row in enumerate(hif['matrix']):
            v=row.get(letter)
            if design:
                target='R' if hif['sequence'][i] in 'ACDEGILSTV' else 'A' if hif['sequence'][i] in 'HKNQRY' else 'S'
                fill=GREEN if (not scan or letter==target) and letter!=hif['sequence'][i] else '#E3E8DF'
            elif v is None:fill='#DCE4D7'
            elif v<0:fill=BLUE
            elif v<.5:fill='#E1E7D3'
            elif v<1:fill='#E6CDB0'
            elif v<2:fill='#DE9472'
            else:fill='#BC5038'
            s+=f'<rect x="{x+i*cw}" y="{y+j*ch}" width="{cw-1}" height="{ch-1}" fill="{fill}"/>'
    return s

def mutation_diagram():
    s=sequence(45,70,step=33)+text(45,48,'Trình tự tham chiếu',20,anchor='start')
    s+=edge(425,120,425,190,CORAL)+box(300,195,250,78,'Thay P bằng D','Tại vị trí 12',CORAL)
    s+=edge(560,234,660,234,CORAL)+heat(690,128,12,9,design=True)
    s+=f'<rect class="pulse" x="{690+11*12}" y="{128+hif["aa_order"].index("D")*9}" width="11" height="8" fill="{CORAL}"/>'
    s+=text(855,360,['Một phép thay','một ô hiệu ứng'],24,DARK,weight=600)
    return svg(s,'Một phép thay tại một vị trí tạo một ô trong ma trận hiệu ứng')

def protein_process():
    s=''
    for i in range(14):
        x=60+i*22;y=190+28*math.sin(i*.75)
        if i:s+=f'<line x1="{60+(i-1)*22}" y1="{190+28*math.sin((i-1)*.75)}" x2="{x}" y2="{y}" stroke="{SAGE}" stroke-width="9"/>'
        s+=f'<circle cx="{x}" cy="{y}" r="10" fill="{CORAL if 5<=i<=7 else GREEN}"/>'
    s+=text(210,280,'Protein mang degron',24,weight=600)
    s+=edge(370,190,485,190,delay=1)
    s+=f'<path class="pulse" d="M500 125 Q620 85 640 170 L580 170 L580 212 L640 212 Q610 300 500 255Z" fill="{SAGE}" stroke="{DARK}" stroke-width="3"/>'
    s+=text(565,340,['Nhận diện','và gắn ubiquitin'],21)
    for i in range(4):s+=f'<circle class="flow" cx="660" cy="{160+i*20}" r="7" fill="{CORAL}" style="--dx:190px;animation-delay:-{i+1}s"/>'
    s+=edge(660,190,820,190,delay=2)
    for i in range(5):s+=f'<ellipse cx="{870+i*19}" cy="190" rx="27" ry="64" fill="none" stroke="{DARK}" stroke-width="10" opacity="{.45+i*.1}"/>'
    s+=text(906,310,'Proteasome',23,weight=600)
    for i in range(5):s+=f'<circle class="flow" cx="980" cy="{155+i*18}" r="5" fill="{GREEN}" style="--dx:90px;animation-delay:-{i}s"/>'
    return svg(s,'Minh họa nguyên lý nhận diện degron, gắn ubiquitin và phân hủy protein')

def assay_diagram():
    s=box(25,120,180,98,['Peptide gắn','reporter'],'Đo tỷ lệ huỳnh quang')+edge(215,170,300,170)
    for i,h in enumerate([35,80,125,100,60,30]):
        x=330+i*66;s+=f'<rect x="{x}" y="{270-h}" width="42" height="{h}" fill="{GREEN}" opacity="{.35+i*.1}"/>'
        s+=text(x+21,305,str(i+1),19)
        s+=f'<circle class="flow" cx="300" cy="90" r="5" fill="{CORAL}" style="--dx:{x-279}px;--dy:{170-h}px;animation-delay:-{i*.7}s"/>'
    s+=text(520,350,'Phân vào sáu bin',23,weight=600)+edge(745,170,815,170)
    s+=box(830,120,235,98,'PSI','Chỉ số độ bền reporter')
    return svg(s,'Minh họa reporter, phân bin và chỉ số PSI; histogram chỉ minh họa nguyên lý')

def priority_diagram():
    s=''
    for i in range(12):
        for j in range(8):
            x=80+i*26;y=80+j*26;hot=(i,j) in [(2,2),(5,5),(8,1),(10,6)]
            s+=f'<rect x="{x}" y="{y}" width="21" height="21" rx="3" fill="{CORAL if hot else SAGE}" class="{"pulse" if hot else ""}"/>'
    s+=text(230,345,'Nhiều phép thay có thể thử',22)+edge(415,185,575,185)
    for i in range(4):s+=box(605+i*109,140,88,88,['Ứng','viên'] if i==0 else str(i+1),color=CORAL)
    s+=text(820,300,'Ưu tiên để kiểm chứng',26,DARK,weight=600)
    return svg(s,'Sơ đồ ưu tiên một số phép thay theo ngân sách thí nghiệm; không phải số dự đoán cụ thể')

def designs():
    s=heat(30,85,16,12,True,True)+heat(620,85,16,12,True,False)
    s+=text(250,45,'Scanning',28,DARK,weight=600)+text(840,45,'Saturation',28,DARK,weight=600)
    s+=text(250,365,['Một phép thay ở mỗi vị trí','20 kiểu WT → mutant'],23)
    s+=text(840,365,['Nhiều phép thay ở mỗi vị trí','380 kiểu WT → mutant'],23)
    return svg(s,'Sơ đồ thiết kế scanning và saturation; ô xanh biểu thị loại phép thay được khảo sát')

def label_pipeline():
    s=box(10,120,155,100,'Read theo bin')+edge(175,170,225,170)
    s+=box(235,120,155,100,'PSI từng lần đo')
    s+=edge(400,170,470,95)+edge(400,170,470,260)
    s+=box(480,45,275,90,'WT đo trực tiếp','Scanning')+box(480,225,275,90,'WT từ ô đồng nghĩa','Saturation')
    s+=edge(765,90,850,170)+edge(765,270,850,170)
    s+=box(860,120,210,100,'Hiệu ứng ΔPSI','QC rồi giữ ô hợp lệ')
    return svg(s,'Tái dựng nhãn với mốc WT đúng theo từng thiết kế thí nghiệm')

def groups_diagram():
    s=''
    cols=[GREEN,BLUE,CORAL,DARK]
    for j,col in enumerate(cols):
        x=70+j*100
        for i in range(3):s+=f'<circle cx="{x+24*math.cos(i*2.1)}" cy="{120+24*math.sin(i*2.1)}" r="12" fill="{col}"/>'
    s+=text(210,210,'Giữ nguyên nhóm protein',24,weight=600)
    s+=edge(430,120,600,120)+edge(430,140,600,290,CORAL)
    s+=box(620,65,390,105,'Train và validation','Fit / chọn tham số trong phần này')
    s+=box(620,250,390,105,'Nhóm kiểm tra ngoài','Chỉ dùng đánh giá',CORAL)
    return svg(s,'Nhóm protein được giữ nguyên khi chia train, validation và nhóm kiểm tra ngoài')

def context_diagram():
    s=sequence(35,110,sequence='MLAPYIPMDDDFQLRS',step=55,highlight=7)
    s+=f'<rect class="scan-window" x="160" y="88" width="235" height="80" fill="none" stroke="{DARK}" stroke-width="4" rx="4"/>'
    s+=text(400,250,['Cùng phép thay','ngữ cảnh lân cận có thể khác'],28,weight=600)
    return svg(s,'Cửa sổ ngữ cảnh quanh vị trí đột biến',w=950,h=350)

def head_diagram(multi=False):
    s=''
    for i in range(12):
        for j in range(4):s+=f'<rect x="{45+i*39}" y="{65+j*30}" width="30" height="22" fill="{BLUE}" opacity="{.25+j*.15}"/>'
    s+=text(260,225,'Representation ESM',23)
    if multi:
        for j,(width,col) in enumerate([(105,GREEN),(183,BLUE),(261,CORAL)]):
            s+=f'<rect class="scan-window" x="75" y="{45+j*5}" width="{width}" height="145" fill="none" stroke="{col}" stroke-width="3"/>'
    else:s+=f'<rect class="scan-window" x="75" y="45" width="183" height="145" fill="none" stroke="{DARK}" stroke-width="4"/>'
    s+=edge(545,125,650,125)+box(665,80,235,90,'Dự đoán ΔPSI','Học head trên nhãn mutation')
    return svg(s,'Các bộ lọc tích chập quét qua representation',w=950,h=310)

def transfer_diagram():
    s=box(35,45,230,95,'Nhãn tile','Hoạt tính cả đoạn',BLUE)+box(35,235,230,95,'Nhãn mutation','Hiệu ứng phép thay',GREEN)
    s+=edge(280,90,450,90,BLUE)+edge(280,280,450,280,GREEN)
    s+=box(465,45,230,95,'Tiền huấn luyện','Học tốt nhiệm vụ tile',BLUE)+box(465,235,230,95,'Tinh chỉnh','Dự đoán ΔPSI',GREEN)
    s+=edge(710,90,880,190,CORAL)+edge(710,280,880,190,GREEN)
    s+=box(885,140,185,100,'Đánh giá','Cần đối chứng cùng encoder',CORAL)
    return svg(s,'Nhãn mức tile và nhãn mutation có mục tiêu khác nhau')

def domain_diagram():
    s=box(20,150,220,100,'Peptide đầu vào')+edge(250,200,405,200)
    s+=box(420,150,220,100,'Đánh giá miền')
    for y,label,col in [(55,'Trong miền',GREEN),(180,'Giáp ranh',BLUE),(305,'Ngoài miền',CORAL)]:
        s+=edge(650,200,805,y+36,col)+box(820,y,245,76,label,color=col)
    return svg(s,'Đánh giá miền dẫn đến dự đoán hoặc cảnh báo phù hợp')

def architecture():
    s=box(20,140,220,105,['Giao diện','React'],'Nhập / xem / xuất')+edge(250,190,400,190)
    s+=box(415,140,235,105,'FastAPI','Kiểm tra yêu cầu / điều phối')
    s+=edge(660,190,820,85)+edge(660,205,820,300,BLUE)
    s+=box(830,30,245,110,['Inference','và model card'],'Phiên bản / phạm vi')
    s+=box(830,255,245,110,['Dữ liệu local','và provenance'],'Nguồn / annotation / snapshot',BLUE)
    return svg(s,'Kiến trúc ứng dụng local và nguồn gốc kết quả')

def metrics_diagram():
    s=''
    for i,(label,desc,col) in enumerate([('Sai số','MAE',GREEN),('Xếp hạng','AUROC / AP',BLUE),('Ưu tiên thử nghiệm','Precision top-k',CORAL)]):
        x=30+i*365;s+=text(x+165,60,label,25,col,weight=600)
        if i==0:
            s+=f'<line x1="{x+70}" y1="240" x2="{x+260}" y2="120" stroke="{LINE}" stroke-width="2"/>'
            for j in range(4):
                yy=215-j*24;s+=f'<circle cx="{x+95+j*42}" cy="{yy}" r="8" fill="{GREEN}"/><line x1="{x+95+j*42}" y1="{yy}" x2="{x+95+j*42}" y2="{yy-26}" stroke="{CORAL}" stroke-width="3"/>'
        elif i==1:
            for j,h in enumerate([140,115,90,55,30]):s+=f'<rect x="{x+65+j*43}" y="{265-h}" width="27" height="{h}" fill="{col}" opacity="{1-j*.13}"/>'
        else:
            for j in range(20):s+=f'<circle cx="{x+65+j%5*45}" cy="{130+j//5*40}" r="13" fill="{CORAL if j<4 else SAGE}"/>'
        s+=text(x+165,340,desc,26,col,weight=600)
    return svg(s,'Sai số, xếp hạng và ưu tiên thí nghiệm là ba mục tiêu đánh giá khác nhau')

def table(headers,rows,compact=False):
    return '<table class="table'+(' compact' if compact else '')+'"><thead><tr>'+''.join('<th>'+esc(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'

def image(name,alt,short=False):return f'<img class="figure{" short" if short else ""}" src="assets/{name}.svg" alt="{esc(alt,quote=True)}">'
def split(visual,aside,kind=''):return f'<div class="split {kind}"><div class="visual">{visual}</div><div class="aside">{aside}</div></div>'
def full(visual):return f'<div class="visual">{visual}</div>'
def metric(value,label):return f'<p><span class="number">{value}</span><span class="label">{label}</span></p>'
def context(s,warn=False):return f'<div class="context{" warn" if warn else ""}">{s}</div>'
def add(title,section,body,insight='',notes='',sources=(),dark=False,appendix=False):
    i=len(slides)+1
    srcs=list(sources) if not isinstance(sources,str) else [sources]
    if not notes:notes=insight
    source_html=''.join(f'<li><a href="../../research/{esc(p,quote=True)}" target="_blank" rel="noopener">{esc(p)}</a></li>' for p in srcs)
    note_html=f'<p>{esc(notes)}</p>'+(f'<h3>Nguồn truy vết</h3><ul>{source_html}</ul>' if srcs else '')
    slides.append(dict(number=i,title=title,section=section,insight=insight,notes=notes,sources=srcs,appendix=appendix))
    return f'<section class="slide{" dark" if dark else ""}" data-title="{esc(title,quote=True)}" data-section="{esc(section,quote=True)}" data-appendix="{str(appendix).lower()}" aria-label="{esc(title,quote=True)}"><header><p class="eyebrow">{esc(section)}</p><h2>{title}</h2></header><div class="body">{body}</div>'+(f'<div class="insight">{insight}</div>' if insight else '')+f'<aside class="speaker-notes">{note_html}</aside></section>'

NEW='kaggle-roadmap-2026-10-31/output-analysis.json'
DETAIL='kaggle-roadmap-2026-10-31/output-analysis-details.json'
SOURCES=[NEW,DETAIL]
parts=[]
coverart=svg('<g transform="translate(28 95)">'+heat(0,0,17,13)+f'<rect class="scan-window" x="80" y="-14" width="86" height="288" fill="none" stroke="#D0DEBB" stroke-width="3"/>'+text(235,325,'Mỗi ô là một phép thay',24,'#D0DEBB')+'</g>','Ma trận nhãn đo HIF1A dùng làm hình mở đầu',w=560,h=480)
cover=f'<div class="hero"><div><p class="eyebrow">CT553H · Trao đổi nghiên cứu</p><h1>Hiệu ứng đột biến<br>degron ở mức residue</h1><p class="subtitle">Giới thiệu đề tài, kết quả hiện có<br>và hướng nghiên cứu tiếp theo</p><div class="identity">Nguyễn Thanh Trọng · B2305615<br>GVHD: TS. Hồ Quang Thái<br>Đại học Cần Thơ</div></div><div class="hero-art">{coverart}<div class="hero-label">Từ trình tự đến bản đồ hiệu ứng</div></div></div>'
parts.append(add('Hiệu ứng đột biến degron ở mức residue','Giới thiệu',cover,notes='Buổi giới thiệu đề tài và trao đổi tiến độ; không phải bảo vệ hoàn tất. Hình mở đầu dùng ma trận nhãn đo HIF1A. Mục tiêu: người nghe hiểu bài toán, thấy bằng chứng và góp ý hướng tiếp theo.',sources='slide-figures-2026-10-15/example-matrix.json',dark=True))
parts.append(add('Degron tham gia quá trình phân hủy protein','Giới thiệu',split(protein_process(),'<img class="protein-photo animated-gif" src="assets/fam188a.gif" data-gif="assets/fam188a.gif" data-poster="assets/fam188a-poster.png" alt="Mô hình protein Fam188a quay, minh họa protein gấp cuộn"><img class="protein-photo gif-poster" src="assets/fam188a-poster.png" alt="Mô hình protein Fam188a tĩnh"><p class="photo-label">Protein gấp cuộn<br>Hình minh họa cấu trúc</p>','wide'),'Một phép thay amino acid có thể làm thay đổi tín hiệu nhận diện.',notes='Sơ đồ là nguyên lý đơn giản hóa UPS. GIF Fam188a của Nikolakhs, CC BY-SA 3.0, chỉ minh họa một protein gấp cuộn, không phải HIF1A/degron đã đo. Hoạt tính của đoạn peptide tách rời có thể khác trong protein nguyên vẹn.'))
parts.append(add('Một phép thay tạo một ô trong bản đồ hiệu ứng','Giới thiệu',full(mutation_diagram()),'Đầu vào: trình tự WT, vị trí và amino acid thay vào. Đầu ra: ΔPSI.',notes='WT là trình tự tham chiếu. Ma trận hiển thị 28 vị trí và 20 amino acid; ô WT→WT được mask, có 532 phép thay thật khi đủ dữ liệu. Đây là sơ đồ đầu ra, không phải dự đoán mô hình.',sources='model-selection-pipeline-2026-10-24/README.md'))
parts.append(add('GPS chuyển tín hiệu reporter thành nhãn ΔPSI','Giới thiệu',full(assay_diagram()),'<strong>ΔPSI = PSI(mutant) − PSI(WT).</strong> Dương: reporter bền hơn trong assay.',notes='Histogram là minh họa cách đo, không phải số liệu thực nghiệm. PSI của Zhang dùng sáu bin, thang 1–6; thấp là reporter kém bền. Không tự suy dấu ΔPSI thành cơ chế E3 hay khả năng gây bệnh.',sources='full-data-audit/psi-build.json'))
parts.append(add('Ví dụ HIF1A cho thấy hiệu ứng tập trung theo vị trí','Giới thiệu',split(image('hif-measured','Heatmap ΔPSI thực nghiệm của peptide HIF1A'),metric('529 / 532','phép thay có nhãn đo')+'<p>Vùng <strong>L–A–P–Y–I</strong> nổi bật trong bản đồ.</p>'+context('Nhãn thực nghiệm, không phải dự đoán')),'Cùng một peptide, những vị trí khác nhau phản ứng rất khác với đột biến.',notes='Peptide Q16665_HIF1A_25, vị trí protein 553–580. WT nội tại PSI2.1865; 186 ô ΔPSI≥1. Ví dụ được chọn theo ≥500 ô, nhiều ô dương nhất, hòa lấy ID nhỏ nhất. Đối chiếu motif HIF1A/VHL là y văn, không phải phát hiện cơ chế mới. Ô WT và ô thiếu đều được mask.',sources='slide-figures-2026-10-15/example-matrix.json'))
parts.append(add('Giá trị sử dụng là ưu tiên đột biến để kiểm chứng','Giới thiệu',full(priority_diagram()),'Ma trận → danh sách ưu tiên → thí nghiệm xác nhận.',notes='Không coi xếp hạng dự đoán là thay thế thực nghiệm. ClinVar là annotation và động lực nghiên cứu; liên hệ bệnh ở mức residue chưa thiết lập. Các ô trong hình chỉ mô tả lựa chọn, không phải điểm mô hình.',sources='variant-coverage-2026-10-15/README.md'))

parts.append(add('Công trình liên quan trả lời các câu hỏi khác nhau','Cơ sở và mục tiêu',table(['Hướng tiếp cận','Đối tượng chính','Liên hệ với đề tài'],[
 ['PAP','Hoạt tính cả peptide','Lấy chênh điểm khi thay amino acid'],['Degformer','PSI từ trình tự','Đã có ma trận hiệu ứng đột biến'],['MetaDegron','Motif / ứng viên degron','Bổ sung chú giải và ngữ cảnh E3'],['Đề tài hiện tại','Hiệu ứng từng phép thay','Nhãn đo + đối chứng + đánh giá theo nhóm']]),'Trọng tâm: bằng chứng dự đoán và đánh giá, cùng công cụ hỗ trợ phân tích.',notes='Không nhận ma trận hoặc web là tính mới độc quyền. Khác endpoint thì không so trực tiếp AUROC. MetaDegron có một classifier dùng chung với lựa chọn motif/E3; không phải mọi menu là một lớp E3 học độc lập.',sources='metadegron-analysis-2026-10-21/comparison-and-positioning.md'))
parts.append(add('Ba mục tiêu nối nghiên cứu với công cụ','Cơ sở và mục tiêu',full(process(['Dữ liệu có truy vết','Phương pháp được kiểm','Công cụ hỗ trợ phân tích'],['Tái dựng và kiểm chất lượng','Đối chứng / độ ổn định','Ma trận / ranking / export'])), 'Phạm vi chính: hiệu ứng đột biến đơn trên reporter peptide 28 amino acid.',notes='Không đặt dự đoán E3 hay chẩn đoán biến thể gây bệnh làm nhiệm vụ chính. Không có phép đo sinh học mới. Công cụ phục vụ hình thành giả thuyết và lựa chọn thí nghiệm.',sources='model-selection-pipeline-2026-10-24/README.md'))
parts.append(add('Các câu hỏi đang dẫn dắt hướng nghiên cứu','Cơ sở và mục tiêu',full(process(['Phân bố nhãn','Ngữ cảnh và ESM','Đầu mô hình','Chuyển nguồn','Giá trị sử dụng'],['Nên học miền nào?','Thông tin nằm ở đâu?','Cần tích chập không?','Có học thêm được?','Hữu ích và đáng tin?'])), 'Mỗi câu hỏi được kiểm bằng phép so phù hợp và giới hạn suy luận rõ ràng.',notes='Sơ đồ là quan hệ nghiên cứu, không là lịch chạy. Các kết quả được tổ chức theo câu hỏi, không theo mã phiên hay thứ tự thời gian.',sources='kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md'))

parts.append(add('Nguồn dữ liệu được dùng đúng vai trò','Dữ liệu và cách tiếp cận',full(process(['Zhang','UniProt','Voutsinos','ClinVar'],['Nhãn mutation ΔPSI','Trình tự / ánh xạ','Tile và baseline PAP','Annotation biến thể'],[GREEN,DARK,BLUE,CORAL])),'Nguồn mức tile và annotation không tự trở thành nhãn mutation.',notes='Core v3 chỉ chứa Zhang và UniProt, không chứa ClinVar/Koren/Larsen/MetaDegron hoặc weights. Larsen/MaveDB là nguồn khảo sát với endpoint khác. Phân biệt nguồn đã tải, đã audit và đã dùng fit.',sources=['kaggle-roadmap-2026-10-31/DATASET.md','full-data-audit/README.md']))
parts.append(add('Hai thiết kế đột biến có độ phủ bổ sung','Dữ liệu và cách tiếp cận',full(designs()),'Scanning mở rộng ngữ cảnh; saturation kiểm được đầy đủ các kiểu thay thế.',notes='Scanning có phép thay là hàm của WT: hướng R/A/S, tổng20 cặp có hướng trong380 cặp không đồng nghĩa. Hình biểu thị thiết kế lý tưởng, không khẳng định mọi ô đều qua QC.',sources='scan-sat-merge-2026-10-23/README.md'))
parts.append(add('Mốc WT phải phù hợp với từng thí nghiệm','Dữ liệu và cách tiếp cận',full(label_pipeline()),'Giữ riêng nguồn, điều kiện và replicate trước khi tạo nhãn hiệu ứng.',notes='Saturation không có mut0; dùng trung vị ô đồng nghĩa từng nửa. Scanning dùng mut0 đúng replicate. Không lấy BAG6 WT làm mốc saturation. PSI dựng lại261865 giá trị khớp tác giả trong5e-7 khi mô phỏng điều kiện tái lập.',sources=['full-data-audit/psi-build.json','full-data-audit/saturation-matrix.json']))
noise=svg(box(20,150,210,95,'Cùng phép thay')+edge(240,195,440,95)+edge(240,195,440,285,BLUE)+box(450,45,240,95,'Đo lần thứ nhất')+box(450,235,240,95,'Đo lần thứ hai',color=BLUE)+edge(700,95,880,190)+edge(700,285,880,190,BLUE)+box(890,140,180,100,'So độ lặp lại'), 'Minh họa đo lặp và kiểm độ tin cậy')
parts.append(add('Độ lặp lại của nhãn đặt giới hạn cho cách đọc kết quả','Dữ liệu và cách tiếp cận',split(noise,metric('0,8335','tương quan ΔPSI giữa hai nửa saturation')+'<p>235 peptide · 122.412 ô</p><p class="small">Độ tin cậy mức peptide khác với độ tin cậy từng vị trí.</p>'),'Phần dư sau mô hình có thể chứa cả tín hiệu và nhiễu đo.',notes='0.8335 là Pearson giữa hai nửa trên cohort saturation theo audit. Không so noise_share của tổng phương sai với noise_share của phần dư như cùng đại lượng. Replicate là mốc độ tin cậy của phép đo, không phải trần tuyệt đối cho mọi estimator.',sources=['full-data-audit/saturation-matrix.json','full-data-audit/replicate-audit.json']))
parts.append(add('Chia theo nhóm protein để kiểm khả năng tổng quát hóa','Dữ liệu và cách tiếp cận',full(groups_diagram()),'Miền hẹp: 91 peptide. Toàn dải: 235 peptide thuộc 221 nhóm protein.',notes='Hai thiết kế có population, eligibility và preprocessing khác, không nối AUROC thành một đường tiến bộ. V3 dùng5outer folds và3seed inner-validation; các transform chỉ fit trong train, epoch chọn rồi khởi tạo lại refit. Nhóm có homology heuristic, không chứng minh độc lập sinh học tuyệt đối.',sources='kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md'))
parts.append(add('Sai số, xếp hạng và ngân sách thí nghiệm là các mục tiêu riêng','Dữ liệu và cách tiếp cận',full(metrics_diagram()),'Tính theo peptide; khoảng tin cậy lấy mẫu lại theo nhóm protein.',notes='V3 MAE có235 peptide; event dương Δ≥1 có184peptide đủ điều kiện, âm Δ≤−1 có110. Mỗi lớp phải có≥3ô. Bootstrap5000 theo nhóm, không theo122412ô. AUROC không là accuracy; AP cần đọc với tần suất event.',sources=NEW))

parts.append(add('Ngữ cảnh cục bộ bổ sung thông tin ngoài phép thay','Kết quả và phân tích',split(image('context','Ablation giá trị ngữ cảnh trên scanning'),'<p><strong>Phần lớn lợi ích</strong> đến từ thành phần của vùng lân cận.</p><p>Giữ thêm thứ tự có lợi nhỏ hơn.</p>'+context('Đánh giá trên scanning')),'Đây là lý do cần baseline ngữ cảnh trước khi thử mô hình phức tạp.',notes='M0 pair+composition0.8393; unordered0.8625; ordered±3 0.8682. Ordered−M0 +.0289 CI[.0264,.0313]. Trung bình AUROC các seed trong nguồn này, không gán là ensemble v3. Mô hình tuyến tính composition hằng trong peptide không tự đổi thứ hạng giữa vị trí có cùng phép thay.',sources='residue-task-derisk-2026-10-15/model.json'))
parts.append(add('Học toàn dải PSI giảm sai số hồi quy của Ridge','Kết quả và phân tích',split(image('training-range','MAE của Ridge theo miền PSI train'),metric('5,94%','giảm MAE: toàn dải so với chỉ PSI ≤ 4')+'<p class="small">Chênh MAE: −0,0258 PSI<br>CI điều chỉnh: −0,0338 đến −0,0183.</p>'),'Cải thiện có bằng chứng; mức giảm tối thiểu 0,02 PSI chưa được bảo đảm trên toàn CI.',notes='Cùng235peptide test,221nhóm. Hai contrast Q1 dùng CI97.5% Bonferroni. Arm hẹp vẫn dùng validation toàn dải. Không đưa PSI(WT) vào feature hoặc dùng nó clip dự đoán.',sources=NEW))
parts.append(add('Lợi ích toàn dải tập trung ở miền PSI cao','Kết quả và phân tích',split(image('strata','MAE của ba cách train trên bốn miền PSI'),'<p>Miền PSI cao được cải thiện rõ hơn.</p><p><strong>Cân bằng dữ liệu</strong> có thể đánh đổi chất lượng miền PSI thấp.</p>'),'Chọn phân bố train cần xét cả mục tiêu toàn tập và miền sử dụng.',notes='Các strata có91/85/36/23peptide. Ridge full ở miền≤3 không thấy giảm quáguardrail. Cân bằng có cận CI AUROC hơi vượt−.01. >5 không có eventdươngΔ≥1 nên AUROC dươngnull đúng. Khi soCNN toàn dải/chỉ≤4, miền≤3 MAE tăng.00870 CI[.00329,.01411], không suy guardrailRidge sangCNN.',sources=SOURCES))
parts.append(add('ESM bổ sung tín hiệu cho baseline ngữ cảnh','Kết quả và phân tích',split(image('esm-linear','AUROC dương Ridge ngữ cảnh, Ridge với ESM và nested selection'),'<p>ESM-only và context+ESM có đánh đổi giữa MAE và xếp hạng.</p><p><strong>Chọn bằng validation</strong> đánh giá một quy trình lựa chọn.</p>'),'Trong benchmark toàn dải, mới ESM2-35M có kết quả; chưa kết luận được họ pLM tốt nhất.',notes='W5+ESM−W5 AUROC+.012548 CI95[.006216,.019670]. Nested selection MAE.397525 vsW5.407803, AUROC improvementCIphủ0. Không lấy fixedrecipe tốt nhất thay cho nested procedure. Bảng nhiều cỡ ESM trên thiết kế khác để phụ lục.',sources=NEW))
parts.append(add('CNN cải thiện thêm sau representation ESM','Kết quả và phân tích',split(image('heads','MAE của head one-hot và ESM trên train toàn dải'),'<div style="height:190px">'+head_diagram()+'</div><p>So với pointwise:<br><strong>MAE giảm 0,00534 PSI.</strong></p>'),'Phép so cùng đầu vào hỗ trợ giá trị trộn vị trí; kết quả one-hot còn chưa phân giải.',notes='ESMCNN−pointwise MAE CI95[−.010173,−.000899], AUROC+.011289CI[.003434,.019133]. Head parameter36833vs57185 nên chưa cô lập sức chứa. CI khácQ1 là mô tả, chưa điều chỉnh toàn khảo sát.',sources=NEW))
parts.append(add('Nhiều cửa sổ chưa chứng minh vượt một cửa sổ','Kết quả và phân tích',f'<div class="stack"><div style="height:185px">{head_diagram(True)}</div>{image("mcnn-ci","CI chênh lệch MAE giữa nhiều cửa sổ cân bằng và CNN toàn dải")}</div>','Đứng đầu MAE trong bảng development chưa đủ để chốt ứng viên.',notes='mCNNE MAE.383846vsCNND.384354, chênh−.000508CI95[−.003157,+.002223]. CùngD mCNN−CNN +.000639CIphủ0. B/D/E là lựa chọn phân bốtrain nội bộ, màn chiếu dùng tên đầy đủ. CNN chỉPSI≤4 đánggiữ nếuưu tiênmiềnthấp; toàn dải so nó chưađảm bảoguardrail.',sources=SOURCES))
parts.append(add('Học tốt nhãn tile chưa bảo đảm chuyển sang mutation effect','Kết quả và phân tích',split(transfer_diagram(),metric('0,8098','AUROC sau tiền huấn luyện tile')+metric('0,8175','cùng encoder, khởi tạo ngẫu nhiên')),'Kết quả âm giới hạn một thiết kế chuyển giao cụ thể, không bác bỏ mọi cách tiền huấn luyện.',notes='Cùngthiếtkế ext4 trên91peptide. Nguồn212616tile; encoderpretrainPearson.864 nhưng downstreampre−rand−.0077CI[−.0163,+.0006]. Nhánhpre−ridge−.011CIâm. Không so thẳng với số v3 hoặc quy thành pretraining pLM vô ích.',sources='pretrain-p3-2026-10-22/results.json'))
parts.append(add('Scanning pretrain có lợi cả ngoài các kiểu thay đã thấy','Kết quả và phân tích',split(image('transfer','MAE CNN scratch và CNN pretrain scanning'),'<p><strong>20 kiểu đã có:</strong><br>MAE giảm 0,00772.</p><p><strong>360 kiểu còn lại:</strong><br>MAE giảm 0,00631.</p>'+context('CI mô tả đều ở phía cải thiện')),'Quality weighting hiện làm tăng sai số; trung bình replicate chưa hơn rep1 rõ ràng.',notes='Transfer onehotCNN, không làESM+scanning. Cohort20 có6433ô;360 có115979ô,cùng235peptide221nhóm. Mean12−rep1CIphủ0. Quality−satonly +.004010. Scan_T không thamgiafit; kếtquả ởsaturationOOF khônglàtransferT.',sources=SOURCES))
parts.append(add('Đối chiếu Degformer cần kiểm cả chồng mẫu và ngân sách nhãn','Kết quả và phân tích',split(image('degformer','Đối chiếu Degformer retrain sạch cụm và Ridge trên cùng 91 peptide'),metric('91 / 91','WT peptide có trong train của checkpoint công bố')+'<p>Che ô trùng chưa tạo thành peptide chưa thấy.</p>'),'Retrain sạch cụm đạt AUROC 0,8068; chưa có bằng chứng vượt Ridge trên phép so này.',notes='Checkpoint.9248có88.12%ôtrùng. Retrainsạch.806775, Ridgeext.820822, delta−.014CI[−.0283,+.0010]=>khôngphânbiệtđược. Retrainkiếntrúcchỉ47knhãn.749978làthiếtkếriêng. Không coi chênhcheckpoint/retrain là causal leakage-only effect vì các điều kiện thay đổi.',sources='r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json'))
parts.append(add('Xếp hạng giúp tập trung ngân sách vào đột biến đáng thử','Kết quả và phân tích',split(image('utility','Precision dương theo ngân sách top-k so Ridge và ESM CNN'),metric('58,24%','precision dương khi chọn top 5%')+'<p>Ridge ngữ cảnh: 51,89%.</p><p class="small">Phía âm vẫn khó hơn; cần đọc cùng độ hiếm sự kiện.</p>'),'Đây là khả năng ưu tiên thí nghiệm, chưa phải xác suất đã được hiệu chuẩn.',notes='Precision macro trong184peptideeligibleplus. Top10CNN49.04%vsRidge44.29%. AP+.50947,rate+.124697 trêncùngcohort. AP−.213667,rate−.027336trên110peptide;precisiontop5−16.77%. Không dùngtopkzero-scorephụthuộctiebreaklàmrandom.',sources=NEW))
parts.append(add('Độ ổn định và chi phí cùng tham gia lựa chọn mô hình','Kết quả và phân tích',split(image('folds','MAE Ridge và CNN ESM qua năm nhóm kiểm tra ngoài'),metric('156 / 235','peptide có MAE tốt hơn Ridge')+'<p><strong>9,33 giờ</strong> task đã hoàn tất.</p><p class="small">Hai task frozen chiếm 7,23 giờ.<br>LoRA chưa có OOF hoàn chỉnh.</p>'),'Ensemble giúp giảm phương sai; seed và fold không phải các bộ dữ liệu độc lập.',notes='Tổngtaskseconds9.3265h,77.52%stage11frozen; chưa gồmLoRAdở. Chỉseed17frozenB/D. 35taskcomplete,1runningtrongsnapshotkhôngchứngminhremotecònsống. Frozenstage11chạybackbonemỗibatch; cache làhướngtốiưucầnparity, không cóbenchmarktăngtốc. Nguồn chốt ởsnapshotKaggle, khônggộpjoblocalđangchuẩnbị.',sources=SOURCES))
parts.append(add('Hiệu chuẩn nối điểm hồi quy với xác suất sự kiện','Kết quả và phân tích',f'<div class="charts-two"><div>{context("Ridge trên miền đánh giá 91 peptide")}{image("calibration","Đường reliability của Ridge với Platt")}</div><div>{image("brier","Brier của tần suất nền và Ridge đã hiệu chuẩn")}</div></div>','Bằng chứng hiệu chuẩn thuộc model đã kiểm; CNN mới cần quy trình hiệu chuẩn riêng.',notes='RidgeM3ext4PlattBrier.0925vsconst.1139,BSS.188. ScoreΔPSIclippedkhôngtựlàprobability. Reliabilitythiênthấpdo fitpoolkhácmiềntest; khônggọicalibrationhoànhảo. Protocolv3crossfitcalibrationkhácchitiếtP6, khôngmangnguyêncalibratorsangCNN.',sources='calibration-p6-2026-10-22/results.json'))
parts.append(add('Miền áp dụng cần được đánh giá cùng với dự đoán','Kết quả và phân tích',full(domain_diagram()),'PSI giữa các nguồn đo khác nhau; mô hình học peptide chưa xác nhận hiệu ứng protein nguyên vẹn.',notes='CổngR3khảosátchomiềntrainPSI≤4. PSIpeptidomescreenlệchWTintrinsic~.9,khôngdùngrawthreshold4trực tiếp. ÁpquaR3khoảng26%in9%border65%out. FullPSIkhôngtựchocổngđộcậymớivàkhôngchứngminhphục vụmọiprotein. Tíchhợpgateappcònmở.',sources='r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json'))

ui='<div class="ui-frame"><img src="assets/workspace-prototype.png" alt="Ảnh prototype giao diện workspace với ma trận và bảng thông tin ô"><div class="ui-highlight"></div><div class="ui-badge">Prototype giao diện · dữ liệu minh họa · chưa nối backend</div></div>'
parts.append(add('Công cụ đưa ma trận và danh sách ưu tiên vào cùng một luồng','Công cụ hỗ trợ phân tích',ui,'Nhập peptide → xem ma trận → chọn phép thay → chú giải → xuất kết quả.',notes='Ảnhchụpprototypeworkspaceuiv2hiệnhành. Tấtcảscore/probabilitydemo làsyntheticfixture; khônglàmodeloutput. BaselineReact/FastAPIđãcómãriêng; prototypekhôngnghiệmthubatchprojectsimports. Chỉdùngảnhthiếtkếđểminhhọaluồng.',sources='../system/design/workspace-ui-v2/README.md'))
parts.append(add('Một ứng dụng local giữ kết quả cùng nguồn gốc','Công cụ hỗ trợ phân tích',full(architecture()),'Mỗi kết quả đi cùng phiên bản model, nguồn dữ liệu và phạm vi sử dụng.',notes='StackđãchốtReactTypeScriptFastAPIlocal. SQLiteđãdùngchobaseline; PostgreSQLvàdurableworkspacelàphạmvicầntriểnkhaikiểm. KhôngcóyêucầupublishVPS. Sơđồkiếntrúcđịnhhướng, khônglàxácnhậnmọimoduleđãhoànthành.',sources='../system/README.md'))
parts.append(add('Phần mềm có nền tảng để tiếp tục mở rộng','Công cụ hỗ trợ phân tích',table(['Đã có nền tảng','Đang phát triển / cần tích hợp'],[
 ['Peptide đơn · ma trận · ranking','Batch và xử lý toàn protein'],['Xuất kết quả · model/source pages','Project và lịch sử bền vững'],['Inference đối chiếu với runner','Nhập và so dữ liệu thí nghiệm'],['Mã nền React / FastAPI','Model mới · calibration · domain gate']]),'Các kiểm thử baseline được giữ đúng phạm vi; chức năng mở rộng cần kiểm chứng riêng.',notes='Baselinebackend149pytest/frontend131vitestlàbằngchứnglịchsửghiởsystemREADME,chưachạylạitrongphiêndựngslide. Scopev0.2đãthiếtkếchưatriểnkhaixong; R3gatechưaloadđúngtrongapp. Tránhtrìnhtấtcảplannedendpointlàđãcó.',sources='../system/README.md'))

parts.append(add('Những gì đã thực hiện tạo nền tảng cho hướng nghiên cứu','Tiến độ và hướng tiếp theo',full(process(['Dữ liệu và đánh giá','Bằng chứng thực nghiệm','Công cụ phân tích'],['Nhãn / QC / nhóm protein','Ngữ cảnh / ESM / chuyển nguồn','Inference / UI / provenance'])),'Đã có kết quả development đáng chú ý và các giới hạn đủ rõ để chọn bước tiếp theo.',notes='KhôngtựđóngG2/G3hoặctuyênbốhoàntấtluậnvăn. Đónggópđangxâydựnggồmbenchmark/phươngpháp/đánhgiá/phầnmềm,khôngbắtbuộckiếntrúcmới. Các kết quả âm có vai trò thu hẹp hướng nghiên cứu.',sources=[NEW,'model-selection-pipeline-2026-10-24/README.md']))
nextsvg=svg(text(50,60,'Nghiên cứu mô hình',26,DARK,anchor='start',weight=600)+box(30,100,225,90,'Khóa ứng viên')+edge(265,145,370,145)+box(385,100,290,90,'Refit và hiệu chuẩn')+edge(685,145,790,145)+box(805,100,250,90,'Đánh giá chuyển nguồn')+text(50,290,'Phát triển công cụ',26,BLUE,anchor='start',weight=600)+box(30,330,225,76,'Tích hợp model',color=BLUE)+edge(265,368,370,368,BLUE)+box(385,330,290,76,'Workflow và lưu trữ',color=BLUE)+edge(685,368,790,368,BLUE)+box(805,330,250,76,'Kiểm chứng sử dụng',color=BLUE),'Hai hướng nghiên cứu và phát triển công cụ được thực hiện theo điều kiện phụ thuộc',h=450)
parts.append(add('Ưu tiên tiếp theo là khóa lựa chọn và kiểm chứng khả năng chuyển giao','Tiến độ và hướng tiếp theo',full(nextsvg),'LoRA và cấu trúc là các nhánh cân nhắc theo câu hỏi và nguồn lực.',notes='FinalpromotiontựđộnghiệnchỉW5; CNNcầnmodel-specificrefitexport. Khóarecipe/calibrationtrướckhiđọcT. Nguồnscanningđãthăm dòtronglịchsử,khônggọiđộclậphoàntoàn. KhôngcầnchờLoRAđểhoànthiệnbenchmarklõi.',sources='kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md'))
questions=svg(text(50,75,'Ưu tiên nghiên cứu',34,'#FFFFFF',anchor='start',weight=600)+text(50,125,'Sai số toàn dải hay ưu tiên hiệu ứng mạnh?',25,'#D0DEBB',anchor='start')+text(50,230,'Phạm vi kiểm chứng',34,'#FFFFFF',anchor='start',weight=600)+text(50,280,'Nguồn và mức độ tổng quát hóa nào phù hợp?',25,'#D0DEBB',anchor='start')+text(50,385,'Mức độ phát triển công cụ',34,'#FFFFFF',anchor='start',weight=600)+text(50,435,'Chức năng nào nên được ưu tiên tiếp theo?',25,'#D0DEBB',anchor='start'),'Ba nội dung trao đổi với giảng viên',h=480)
parts.append(add('Trao đổi về hướng nghiên cứu và bước tiếp theo','Trao đổi với giảng viên',full(questions),notes='Mời giảng viên góp ý mục tiêu và hướng ưu tiên. Đây là buổi giới thiệu/tiến độ, không phải nghiệm thu toàn bộ đề tài. Có thể mở overview hoặc phụ lục để trao đổi chi tiết.',dark=True))
assert len(slides)==34

def ap(title,body,insight='',notes='',sources=()):return add(title,'Phụ lục tra cứu',body,insight,notes,sources,appendix=True)
parts.append(ap('Cách đọc các thuật ngữ trong bài toán',full(metrics_diagram()),'Residue: amino acid tại một vị trí. WT: trình tự tham chiếu. OOF: dự đoán ngoài fold.',sources='model-selection-pipeline-2026-10-24/README.md'))
parts.append(ap('Chi tiết tạo nhãn và kiểm chất lượng',full(label_pipeline()),'Đồng nghĩa dùng làm WT nội tại; ô thiếu được mask; điều kiện đo được giữ riêng.',sources=['full-data-audit/psi-build.json','full-data-audit/saturation-matrix.json']))
parts.append(ap('Độ tin cậy phụ thuộc mức phân tích',table(['Đại lượng','Scanning','Saturation'],[['ΔPSI giữa các lần đo','Pearson 0,7229','Pearson 0,8335'],['Nhãn dương lặp lại','Jaccard vị trí 0,4965','Jaccard ô 0,6596'],['Population','Theo bộ lọc scanning','235 peptide / 122.412 ô']]),'Các cohort và mức vị trí/ô khác nhau; không diễn giải như phép so ghép cặp.',notes='SốpsiAgreement0.9239trongREADMEfullauditlàmốcsoWTkhôngphảiđúngrep1rep2; dùngđúngtrườngΔPSI. Khônggọi75.9%phầndưnhiễuvà16.7%tổngphươngsailàcùngmẫusố.',sources=['full-data-audit/replicate-audit.json','full-data-audit/saturation-matrix.json']))
parts.append(ap('Mô hình composition không phân biệt mọi vị trí',full(context_diagram()),'Trong cùng peptide, cùng cặp thay thế nhận cùng score nếu đầu vào chỉ có thành phần.',notes='Bấtbiếnápdụngchocompositionthuầntúy; khônggánchotoànPAPcókênhCterminal. M0thực tếcó40chiềupair+20composition. Oracleđọctestkhôngphảitestperformance.',sources=['composition-context-audit.md','residue-task-derisk-2026-10-15/model.json']))
parts.append(ap('Learning curve cần tách model đơn và ensemble',split(image('learning-curve','MAE trung bình seed theo tỷ lệ nhóm train'),'<p>Subset train khác nhau giữa các seed.</p><p>Ensemble có thể thấy hợp dữ liệu lớn hơn mỗi thành viên.</p>'),'Độ nhạy phân cụm là phép kiểm riêng; không đếm phân hoạch trùng nhau như bằng chứng mới.',sources=[DETAIL,'recluster-sensitivity-2026-10-22/results.json']))
parts.append(ap('Các thiết kế tương tác chưa vượt baseline ổn định',table(['Thiết kế','AUROC trên miền 91 peptide','Cách đọc'],[['Ridge','0,8082','Baseline cùng thiết kế'],['Gate + residual PAP','0,8002','Hiệu ứng gate đảo dấu theo seed'],['FiLM','0,8028','Chưa vượt Ridge'],['Bilinear','0,7933','Kết quả thấp hơn Ridge']]),'Đây là những thiết kế đã thử, không phải phủ định mọi tương tác phi tuyến.',sources=['g2-saturation-2026-10-18/results.json','g2-extension-2026-10-18/e2-candidates.json']))
parts.append(ap('Lọc trùng mức ô chưa loại được chồng mức peptide',split(image('degformer','Degformer retrain sạch cụm so đối chứng'),'<p>Checkpoint công bố có 42.163 / 47.847 ô mutation trong train.</p><p>WT của cả 91 peptide đều đã xuất hiện.</p>'),'Cần đánh giá theo peptide/nhóm protein được giữ riêng.',sources=['g2-saturation-2026-10-18/results.json','r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json']))
parts.append(ap('Khảo sát cỡ ESM thuộc các thiết kế riêng',table(['Biểu diễn Ridge bổ sung','AUROC · miền 91 peptide','Kết luận'],[['ESM2 8M','0,8214','CI chưa phân giải'],['ESM2 35M','0,8234','CI chưa phân giải'],['ESM2 150M','0,8207','CI chưa phân giải'],['ESM2 650M','0,8230','CI chưa phân giải']]),'Không so trực tiếp bảng này với AUROC của benchmark toàn dải.',notes='SốlấytừR6D,bổsungchoM3ext4. Cáccheckpointkháctrongregistrykhôngđồngnghĩađãđánhgiá. V3fullWchỉESM235M. 35Mpreflightforwardshape2x28x480vàfinite/repeatpass.',sources='r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json'))
explorer='<div class="metric-picker"><button data-metric="mae" aria-pressed="true">Sai số MAE</button><button data-metric="auroc" aria-pressed="false">AUROC dương</button><button data-metric="ap" aria-pressed="false">AP dương</button></div><div class="chart-explorer"><canvas id="recipeChart" role="img" aria-label="Biểu đồ tương tác so sánh các recipe, chuyển metric bằng ba nút"></canvas><img class="figure print-fallback" src="assets/tradeoff.svg" alt="So sánh MAE và AUROC của các ứng viên"></div>'
parts.append(ap('Đọc nhiều tiêu chí trên cùng các ứng viên',explorer,'Các điểm là ensemble dự đoán ba seed; vẫn là phân tích development.',sources=NEW))
parts.append(ap('Scanning transfer: tách các kiểu thay thế để kiểm chuyển giao',full(image('transfer-pairs','CI lợi ích scanning trên 20 và 360 kiểu thay thế')),'Cohort 20 có 6.433 ô; cohort 360 có 115.979 ô. Cùng 235 peptide.',notes='Mỗi peptidechỉtínhôtrongcohort. AUROCdươngeligible114và184nênkhôngsotrực tiếpmacrogiữahai cohort. HaiCIởhìnhlàhậukiểmmôtảkhôngđiềuchỉnhđa kiểmđịnh.',sources=DETAIL))
parts.append(ap('ClinVar hỗ trợ động lực ở mức vùng, chưa xác nhận mức residue',split(priority_diagram(),metric('2,15','odds ratio gây bệnh / lành tính ở mức vùng')+'<p>Đã phân tầng theo protein.</p><p class="small">Mắt nối ΔPSI với bệnh ở mức residue chưa được thiết lập.</p>'),'ClinVar phục vụ bối cảnh và annotation, không là ground truth ΔPSI.',notes='ORmh2.14783CI[2.07193,2.22651],3114tầng. Khôngliênhệnhânquả. Sat_exactAUC.6738CI[.489,.831]n51chưađạt; scan_posAUC.5166CIphủ.5. NguồnClinicalkhôngdùngchọnmodel.',sources=['variant-coverage-2026-10-15/enrichment.json','variant-coverage-2026-10-15/README.md']))
parts.append(ap('Nhãn E3 chưa đủ cho nhiệm vụ có điều kiện E3',table(['Adaptor / E3','Số peptide trong audit'],[['KLHL15','13'],['BAG6','4'],['ASB7 / FEM1B','2 mỗi nhóm'],['Các nhóm còn lại','Phần lớn 1 peptide']]),'Chỉ một nhóm có ít nhất năm peptide; không dùng số E3 trong menu thay cho số lớp có thể học.',sources='e3-labels-audit/README.md'))
parts.append(ap('Nguồn ngoài cần được đánh giá theo endpoint và khả năng sử dụng',table(['Nguồn','Giá trị khảo sát','Giới hạn'],[['Koren','Mutation ở degron đầu C','Khác thang / độ dài; chỉ 5 nhóm mới'],['Larsen','Hoạt tính tile trong nhân','Không bổ sung nhãn mutation ΔPSI'],['MaveDB','Hiệu ứng biến thể protein','Endpoint và cấu trúc cần audit riêng']]),'Khảo sát nguồn không đồng nghĩa đã có kết quả kiểm chứng ngoài cho model hiện tại.',notes='Korenchưađánhgiámôhình,vaitròcandidatetestnhỏvàquyềnsửdụngnộibộ. MaveDBexposureexploratorycònGCKassay/dimerconfound,cầnchạylạitrướckếtluậnmạnh. SaProttrue3Di chưaoutput; weightskhôngthaymappingstructure.',sources=['koren-s4-audit-2026-10-22/results.json','larsen-nuclear-and-risks-2026-10-15/README.md','architecture-check/README.md']))
parts.append(ap('Calibration và domain gate trả lời hai câu hỏi khác nhau',f'<div class="charts-two"><div>{context("Xác suất sự kiện có phù hợp không?")}{image("calibration","Reliability của model Ridge")}</div><div>{context("Peptide có thuộc miền áp dụng không?")}{domain_diagram()}</div></div>','Cả hai cần được kiểm lại khi đổi model hoặc thay phạm vi dữ liệu.',sources=['calibration-p6-2026-10-22/results.json','r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json']))
parts.append(ap('Tính tái lập nối dữ liệu, model và kết quả phục vụ',full(process(['Nguồn đã băm','Code / protocol','OOF và checkpoint','Inference / export'],['Phiên bản dữ liệu','Cấu hình / split','Mode official / smoke','Model card / provenance'])), 'Đã đối chiếu 2.986 file theo manifest; kiểm thử app nền không nghiệm thu chức năng mới.',notes='Integrity2986files3065290891bytes83OOF47recipes; reproducedanalysisexact. Những con sốtestapp149backend131frontendlàhistoricalbaselinekhôngchạylạitrongtaskslides. SnapshotKaggleupdated2026-11-01T11:18:07Z,khônggộplocalruntimekhác.',sources=[NEW,'../system/README.md']))
refs='<div class="references"><div><a href="../../../../resources/papers/analyzed-papers/README.md">Công trình liên quan</a><p>Zhang · Voutsinos · Degformer · MetaDegron · Larsen</p></div><div><a href="evidence.json">Số liệu và hash nguồn</a><p>JSON nghiên cứu, các figure và dữ liệu biểu đồ</p></div><div><a href="slide-sources.json">Truy vết từng slide</a><p>Điều kiện so sánh, ghi chú diễn giải và nguồn kết quả</p></div><div><a href="design-research.md">Khảo sát template và style</a><p>Penn State / Harvard Catalyst · Slidev Academic · EMBL</p></div><div><a href="asset-notices.md">Nguồn ảnh và giấy phép</a><p>GIF protein · font · Chart.js · sơ đồ tự dựng</p></div><div><a href="../../system/README.md">Phạm vi phần mềm</a><p>Baseline hiện có và các chức năng đang phát triển</p></div></div>'
parts.append(ap('Tài liệu và bằng chứng có thể tra cứu theo chủ đề',refs,'Mở “Ghi chú” để xem nguồn và giới hạn của slide đang trình bày.',notes='Khônggắnfootnotelênmọislidetheoyêucầu. Toànbộnguồnđượctậptrungtạiphụlục,notevàJSON. Websiteđượcdùngkhảosátdesigntrướckhidựng,khôngbổsungclaimhiệunăngmodel.',sources=NEW))
assert len(slides)==50

html='''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Degron-footprint · Giới thiệu và trao đổi nghiên cứu</title><link rel="stylesheet" href="deck.css"><script src="data.js" defer></script><script src="vendor/chart.umd.js" defer></script><script src="deck.js" defer></script></head><body><main id="viewport" aria-label="Bộ slide giới thiệu và trao đổi nghiên cứu"><div id="deck">'''+''.join(parts)+'''</div></main><div id="progress" aria-hidden="true"></div><nav id="toolbar" aria-label="Điều khiển trình chiếu"><button id="prev" aria-label="Slide trước">←</button><span class="counter" id="counter"></span><button id="next" aria-label="Slide tiếp">→</button><button id="overview-button">Mục lục</button><button id="notes-button">Ghi chú</button><button id="motion" aria-pressed="false">Dừng chuyển động</button><button class="long" id="full-button">Toàn màn hình</button><button id="help-button" aria-label="Hướng dẫn phím tắt">?</button></nav><div id="status" role="status" aria-live="polite"></div><dialog id="overview"><button class="close">Đóng</button><h2>Mục lục · 34 slide chính + 16 phụ lục</h2><div id="overview-grid"></div></dialog><dialog id="notes"><button class="close">Đóng</button><h2 id="notes-title"></h2><div id="notes-body"></div></dialog><dialog id="help"><button class="close">Đóng</button><h2>Điều khiển trình chiếu</h2><p>← → / Space: chuyển slide<br>O: mục lục · N: ghi chú và nguồn<br>M: dừng / tiếp tục chuyển động · F: toàn màn hình<br>Home: về đầu · End: phần trao đổi<br>Trên điện thoại: vuốt ngang hoặc dùng nút mũi tên.<br>In từ trình duyệt để xuất PDF tĩnh toàn bộ 50 slide.</p></dialog></body></html>'''
# The cover already contains its own heading; remove its empty header for more visual space.
start=html.find('<header>');end=html.find('</header>',start)
html=html[:start]+html[end+9:]
(HERE/'index.html').write_text(html,encoding='utf8')
(HERE/'slide-sources.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'speaker-notes.md').write_text('# Ghi chú người trình bày\n\n'+''.join(f'## {s["number"]}. {s["title"]}\n\n{s["notes"]}\n\nNguồn: '+', '.join(s['sources'])+'\n\n' for s in slides),encoding='utf8')
print(f'Built {len(slides)} slides: 34 main, 16 appendices.')
