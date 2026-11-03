"""Download cited media and render the selected, licensed paper illustration."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile
import urllib.request

HERE=Path(__file__).resolve().parent
ASSETS=HERE/'assets'
ORIGINAL='https://www.timmslab.com/media/papers/2023_Mol_Cell_Elucidation_of_E3_ubiquitin_ligase_specificity_through_proteome-wide_internal_degron_mapping_naf6vNE.pdf'
MOVIE='https://www.nigms.nih.gov/sites/nigms/files/image-and-video-gallery/AllDegProcesses.mp4'
cache=Path(tempfile.gettempdir())/'degron-media-review'
cache.mkdir(exist_ok=True)

def get(url,p):
    if not p.exists():
        with urllib.request.urlopen(url,timeout=60) as response:p.write_bytes(response.read())
    return p

video=get(MOVIE,ASSETS/'proteasome.mp4')
paper=get(ORIGINAL,cache/'zhang-2023.pdf')
import pymupdf
import imageio_ffmpeg
doc=pymupdf.open(paper)
assert 'CC BY license' in doc[1].get_text(), 'Verify source licence before extracting figures'
page=doc[0]
clip=pymupdf.Rect(54/603*page.rect.width,173/783*page.rect.height,343/603*page.rect.width,461/783*page.rect.height)
page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=clip).save(ASSETS/'zhang-graphical-abstract.png')
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-ss','6','-i',str(video),'-frames:v','1','-update','1','-y',str(ASSETS/'proteasome-poster.jpg')],check=True)
records=[dict(path='assets/proteasome.mp4',url=MOVIE,source_page='https://www.nigms.nih.gov/image-gallery/3764',
              credit='Andreas Martin / HHMI, via NIGMS',licence='CC BY-NC-SA 3.0',modifications='Unmodified movie; poster frame extracted at 6 seconds'),
         dict(path='assets/zhang-graphical-abstract.png',url=ORIGINAL,credit='Zhang et al., Molecular Cell 83 (2023), DOI 10.1016/j.molcel.2023.08.022',
              licence='CC BY 4.0',licence_evidence='PDF page 2 explicitly declares CC BY 4.0; reviewed 2026-11-03',
              modifications='Graphical abstract cropped from PDF page 1 and rasterized; no relabelling of figure',
              original_sha256=hashlib.sha256(paper.read_bytes()).hexdigest())]
for r in records:r['sha256']=hashlib.sha256((HERE/r['path']).read_bytes()).hexdigest()
(HERE/'media-sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Prepared cited video, poster and graphical abstract.')
