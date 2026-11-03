#!/usr/bin/env python3
"""Render every page for visual review; generated previews are not versioned."""
from pathlib import Path
import json
import pymupdf
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parents[1]
OUT=HERE/'previews'
OUT.mkdir(exist_ok=True)
for old in [*OUT.glob('contact-*.png'),*OUT.glob('page-*.png')]:old.unlink()
doc=pymupdf.open(HERE/'study-guide.pdf')
records=[]
for start in range(0,len(doc),12):
    stop=min(start+12,len(doc))
    rows=(stop-start+3)//4
    sheet=Image.new('RGB',(1600,rows*560),'#d9dfe2')
    pen=ImageDraw.Draw(sheet)
    for index,page in enumerate(doc.pages(start,stop)):
        pix=page.get_pixmap(matrix=pymupdf.Matrix(.61,.61))
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        x=(index%4)*400+(400-im.width)//2;y=(index//4)*560+28
        sheet.paste(im,(x,y))
        pen.text(((index%4)*400+12,(index//4)*560+8),f'PDF page {start+index+1}',fill='#102a33')
    dest=OUT/f'contact-{start+1:02d}-{stop:02d}.png'
    sheet.save(dest)
    records.append(dict(file=dest.name,pdf_pages=[start+1,stop]))
# Full-size samples include every figure and every chapter opening.
selected={0}
for level,title,page_no in doc.get_toc():
    if level==1:selected.add(page_no-1)
for index,page in enumerate(doc):
    if page.get_images() or 'Hình ' in page.get_text():selected.add(index)
for index in sorted(selected):
    doc[index].get_pixmap(matrix=pymupdf.Matrix(1.35,1.35)).save(OUT/f'page-{index+1:02d}.png')
(OUT/'manifest.json').write_text(json.dumps(dict(pages=len(doc),contact_sheets=records,large_previews=[i+1 for i in sorted(selected)]),indent=2)+'\n')
print(f'Rendered all {len(doc)} pages; {len(selected)} large previews')
