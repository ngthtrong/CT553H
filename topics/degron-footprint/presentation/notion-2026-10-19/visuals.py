"""Sơ đồ giáo dục tự dựng; không sinh số liệu thực nghiệm."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / 'visuals'
OUT.mkdir(exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
INK, BLUE, GREEN, RED, BG = '#183542', '#386FA4', '#258D82', '#C94D64', '#F7FAFC'

def font(size=24, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def base(title, subtitle):
    im = Image.new('RGB', (1400, 690), BG)
    d = ImageDraw.Draw(im)
    d.text((50, 28), title, font=font(33, True), fill=INK)
    d.text((50, 82), subtitle, font=font(22), fill=INK)
    return im, d

def box(d, xy, title, lines, color=BLUE):
    x,y,w,h = xy
    d.rounded_rectangle((x,y,x+w,y+h), radius=18, fill='white', outline=color, width=3)
    d.text((x+20,y+17), title, font=font(23,True), fill=color)
    for i,line in enumerate(lines):
        d.text((x+20,y+59+i*33), line, font=font(21), fill=INK)

def arrow(d, x, y, x2, y2, color=INK):
    d.line((x,y,x2,y2), fill=color, width=4)
    d.polygon([(x2,y2),(x2-14,y2-8),(x2-14,y2+8)], fill=color)

im,d = base('Degron nằm ở đâu trong câu chuyện phân hủy protein?',
            'Sơ đồ khái niệm: một con đường phân hủy qua ubiquitin–proteasome.')
box(d,(50,175,320,230),'1 · Tín hiệu degron',['Một vùng trình tự có thể','tham gia nhận diện.','Degron ≠ toàn protein.'])
box(d,(530,175,330,230),'2 · Nhận diện và gắn nhãn',['E3 cùng hệ ubiquitin','tham gia gắn ubiquitin','lên protein cơ chất.'],GREEN)
box(d,(1020,175,330,230),'3 · Phân hủy',['Proteasome phân giải','protein đã được đưa','tới hệ thống này.'],RED)
arrow(d,380,285,515,285); arrow(d,870,285,1005,285)
d.rounded_rectangle((50,460,1350,615),radius=20,fill='#E7F0F7')
d.text((75,479),'Vị trí của đề tài',font=font(26,True),fill=BLUE)
d.text((75,525),'Thay đổi peptide degron → đo thay đổi độ bền reporter → học dự đoán hiệu ứng.',font=font(23),fill=INK)
d.text((75,564),'Assay không tự xác định E3 hay chứng minh cơ chế trên protein nguyên vẹn.',font=font(21),fill=INK)
d.text((50,644),'Minh họa giản lược do dự án tự dựng; không phải mọi degron đều dùng cùng một cơ chế.',font=font(19),fill=INK)
im.save(OUT/'biology.png')

frames=[]
for step in range(4):
    im,d=base('Một phép thay thế tương ứng với một ô trong ma trận',
              'Ví dụ giả định, rút gọn còn 7 vị trí × 5 amino acid thay thế; không phải dữ liệu đo.')
    seq='MKTALVA'
    d.text((55,155),'Tham chiếu',font=font(24,True),fill=INK)
    d.text((55,200),'Đột biến A4V',font=font(24,True),fill=BLUE)
    for i,a in enumerate(seq):
        d.text((300+i*42,155),a,font=font(29,True),fill=INK)
        d.text((300+i*42,200),'V' if i==3 else a,font=font(29,True),fill=RED if i==3 else INK)
    box(d,(55,310,495,150),'Cách đọc',['A4V: vị trí 4, A được thay bằng V.','Mỗi thay thế cần một dự đoán riêng.'])
    x0,y0,cw,ch=730,220,85,59
    for col,a in enumerate('AVGSD'):
        d.text((x0+col*cw+27,y0-44),a,font=font(25,True),fill=INK)
    for row in range(7):
        d.text((x0-48,y0+row*ch+13),str(row+1),font=font(23),fill=INK)
        for col,a in enumerate('AVGSD'):
            xy=(x0+col*cw,y0+row*ch,x0+(col+1)*cw-5,y0+(row+1)*ch-5)
            same=(seq[row]==a)
            fill='#E5EBEF' if same else 'white'
            if step>=2 and row==3 and col==1: fill='#A5D9D2'
            d.rectangle(xy,fill=fill,outline='#D3DFE5',width=2)
            if same:d.text((xy[0]+28,xy[1]+9),'—',font=font(23),fill=INK)
    d.text((730,137),'Amino acid thay thế →',font=font(23,True),fill=INK)
    d.text((680,640),'Ô xám: giữ nguyên amino acid tham chiếu.',font=font(18),fill=INK)
    if step>=1:
        d.rounded_rectangle((420,151,460,241),radius=8,outline=RED,width=3)
        arrow(d,560,220,710,425,BLUE)
    if step>=2:
        d.rectangle((x0+cw,y0+3*ch,x0+2*cw-5,y0+4*ch-5),outline=RED,width=5)
    if step>=3:
        d.text((55,500),'ΔPSI = +1,0  (giả định)',font=font(28,True),fill=GREEN)
        d.text((55,548),'Reporter bền hơn so với tham chiếu.',font=font(23),fill=INK)
        d.text((55,586),'Chưa suy ra tính gây bệnh.',font=font(22),fill=INK)
    frames.append(im)
frames[-1].save(OUT/'mutation-map.png')
frames[0].save(OUT/'mutation-map.gif',save_all=True,append_images=frames[1:],duration=[1300,1100,1100,2200],loop=0)

im,d=base('Từ tín hiệu huỳnh quang đến nhãn hiệu ứng đột biến',
          'GPS: peptide gắn reporter GFP; phân nhóm tế bào theo tỉ lệ GFP/DsRed.')
box(d,(50,160,370,190),'1 · Gắn peptide vào GFP',['Đo tham chiếu và đột biến','trong điều kiện tương ứng.'])
box(d,(520,160,350,190),'2 · Phân thành 6 nhóm',['Theo tỉ lệ GFP/DsRed.','Giải trình tự để có số đếm.'],GREEN)
box(d,(970,160,380,190),'3 · Chuẩn hóa và tính PSI',['Trung bình có trọng số','của nhóm 1 đến nhóm 6.'])
arrow(d,430,255,505,255);arrow(d,880,255,955,255)
for i in range(6):
    x=90+i*145
    d.rounded_rectangle((x,420,x+115,485),radius=12,fill=['#EDF6F3','#D9EDE6','#B8DDD1','#8BC9B6','#57AD94','#258D82'][i])
    d.text((x+44,433),str(i+1),font=font(28,True),fill=INK)
d.text((90,505),'PSI thấp: reporter kém bền',font=font(22),fill=INK)
d.text((590,505),'PSI cao: reporter bền hơn',font=font(22),fill=INK)
d.text((90,570),'ΔPSI = PSI(đột biến) − PSI(tham chiếu)',font=font(30,True),fill=BLUE)
d.text((90,625),'Minh họa quy trình; màu sáu nhóm không phải cường độ huỳnh quang đo thực tế.',font=font(20),fill=INK)
im.save(OUT/'assay.png')

thumbs=[]
for p in ['biology.png','mutation-map.png','assay.png']:
    a=Image.open(OUT/p);a.thumbnail((1000,495));thumbs.append(a.copy())
sheet=Image.new('RGB',(1000,495*3),'white')
for i,a in enumerate(thumbs):sheet.paste(a,(0,i*495))
sheet.save(OUT/'preview.png')
print('Created biology.png, mutation-map.png/gif, assay.png, preview.png')
