#!/usr/bin/env python3
"""Build the learning artifact from saved evidence; never launch research jobs."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parents[1]
BUILD=HERE/'build'
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())

def run(args, **kwargs):
    return subprocess.run(args,check=True,cwd=HERE,**kwargs)

def references(evidence):
    out=['# Danh mục bằng chứng và tài liệu đọc thêm',
         '## Cách truy nguyên số liệu',
         'Mã NC là kết quả/audit nghiên cứu đã lưu; KH là kế hoạch, không chứng minh kết quả; '
         'PM là hồ sơ trạng thái phần mềm, có kiểm tra lịch sử và phần chưa triển khai. '
         'Sổ `evidence.json` đi cùng tài liệu ghi đường dẫn nguồn và SHA-256; sách dùng mã để '
         'giữ nội dung học dễ đọc. Tất cả được đối chiếu ở mốc 03/11/2026. '
         'Nguồn gốc có thể chứa phạm vi hẹp hoặc cảnh báo chi tiết hơn đoạn tóm tắt trong sách.',
         '## Nghiên cứu đã lưu — NC']
    for group,title in [('NC',None),('KH','## Kế hoạch thực thi — KH'),('PM','## Phần mềm và prototype — PM')]:
        if title:out.append(title)
        for rec in evidence['sources']:
            if rec['id'].startswith(group):
                sid=rec['id'];out.append(f"- []{{#source-{sid.lower()}}}**{sid} — {rec['title']}.** Bản ghi nội bộ trong repository; xem sổ bằng chứng đi kèm để tra bản gốc.")
    out += ['## Tài liệu nền bên ngoài — TL',
      '- []{#source-tl-01}**TL-01 — NHGRI, Transcription.** Định nghĩa phiên mã; '
      '[thuật ngữ chính thức](https://www.genome.gov/genetics-glossary/Transcription).',
      '- []{#source-tl-02}**TL-02 — NHGRI, Translation.** Định nghĩa dịch mã; '
      '[thuật ngữ chính thức](https://www.genome.gov/genetics-glossary/Translation).',
      '- []{#source-tl-03}**TL-03 — Zhang và cộng sự (2023).** '
      '*Elucidation of E3 ubiquitin ligase specificity through proteome-wide internal degron mapping*. '
      'Molecular Cell. [DOI 10.1016/j.molcel.2023.08.022](https://doi.org/10.1016/j.molcel.2023.08.022); '
      '[toàn văn trên PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10594193/). '
      'Dữ liệu Mendeley phiên bản 2: [DOI 10.17632/32h94v2yv2.2](https://doi.org/10.17632/32h94v2yv2.2). '
      'Quy tắc dựng nhãn và kiểm tính toán của đề tài xem NC-01/NC-21.',
      '- []{#source-tl-04}**TL-04 — Lin và cộng sự (2023).** '
      '*Evolutionary-scale prediction of atomic-level protein structure with a language model*. '
      'Science 379(6637), 1123–1130. [DOI 10.1126/science.ade2574](https://doi.org/10.1126/science.ade2574). '
      'Nguồn nền về ESM; không phải bằng chứng model của đề tài đã đạt một metric ΔPSI.',
      '- []{#source-tl-05}**TL-05 — Hu và cộng sự (2022).** '
      '*LoRA: Low-Rank Adaptation of Large Language Models*. ICLR. '
      '[Bài gốc](https://openreview.net/pdf?id=nZeVKeeFYf9). '
      'Nguồn giải thích LoRA; khả thi/chất lượng trên assay của đề tài phải kiểm riêng.',
      '## Nguồn hình và cách tạo tài liệu',
      'Các biểu đồ định lượng được sinh từ JSON NC và có mã nguồn đi kèm; heatmap HIF1A là nhãn đo '
      'đã lưu, không phải suy luận mới. Hình count là ví dụ tự đặt. Ảnh Workspace v2 là fixture '
      'tổng hợp từ PM-03. Các sơ đồ là diễn giải do tài liệu học dựng, có bản Draw.io chỉnh sửa được.',
      'Quy trình tổng hợp áp dụng skill Notion research documentation theo phạm vi PDF local; '
      'không tạo hoặc ghi trang Notion. Sơ đồ dùng '
      '[Draw.io skill của Agents365-ai](https://github.com/agents365-ai/drawio-skill), '
      'bản ghim được ghi trong hồ sơ cài đặt ở repository. '
      'Công cụ hỗ trợ tác giả không thay thế việc kiểm số liệu và giới hạn khoa học.']
    return '\n\n'.join(out)+'\n'

def link_citations(text):
    # Convert compact bracketed source lists to clickable internal references.
    pattern=r'\[((?:NC|KH|PM|TL)-\d{2}(?:[;, ]+(?:NC|KH|PM|TL)-\d{2})*)\]'
    def replace(match):
        codes=re.findall(r'(?:NC|KH|PM|TL)-\d{2}',match[1])
        return '['+'; '.join(f'[{c}](#source-{c.lower()})' for c in codes)+']'
    return re.sub(pattern,replace,text)

def main():
    for binary in ['pandoc','xelatex','pdftotext','pdffonts','pdfinfo']:
        if not shutil.which(binary):raise SystemExit(f'Missing build dependency: {binary}')
    BUILD.mkdir(exist_ok=True)
    run([sys.executable,'scripts/collect_evidence.py'])
    run([sys.executable,'scripts/generate_figures.py'])
    evidence=json.loads((HERE/'evidence.json').read_text())
    chapters=sorted((HERE/'chapters').glob('*.md'))
    manuscript='\n\n'.join(p.read_text().strip() for p in chapters)+'\n\n'+references(evidence)
    for key,val in evidence['values'].items():
        manuscript=manuscript.replace('{{'+key+'}}',val)
    assert not re.search(r'\{\{[A-Z_]+\}\}',manuscript),'Unresolved evidence placeholder'
    manuscript=link_citations(manuscript)
    (BUILD/'study-guide.md').write_text(manuscript)
    run(['pandoc','build/study-guide.md','--standalone','--from=markdown+fenced_divs+link_attributes',
         '--to=latex','--top-level-division=chapter','--number-sections','--no-highlight',
         '--lua-filter=scripts/callouts.lua','--template=assets/template.tex','--output=build/study-guide.tex'])
    last=None
    for attempt in range(5):
        proc=run(['xelatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                  '-output-directory=build','build/study-guide.tex'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (BUILD/f'xelatex-{attempt+1}.txt').write_text(proc.stdout)
        aux=b''.join((BUILD/f'study-guide.{ext}').read_bytes() for ext in ['aux','toc','lof'] if (BUILD/f'study-guide.{ext}').exists())
        digest=hashlib.sha256(aux).hexdigest()
        if attempt>=1 and digest==last:break
        last=digest
    else:raise SystemExit('References did not stabilize in five XeLaTeX passes')
    log=(BUILD/'study-guide.log').read_text()
    bad=[line for line in log.splitlines() if re.search(r'Overfull \\[hv]box|Missing character:|undefined references|multiply defined|LaTeX Error',line)]
    if bad:raise SystemExit('PDF checks failed:\n'+'\n'.join(bad))
    shutil.copyfile(BUILD/'study-guide.pdf',HERE/'study-guide.pdf')
    run(['pdftotext','-layout','study-guide.pdf','build/study-guide.txt'])
    source_map=['# Chỉ mục nguồn của tài liệu học','', 'Mốc đọc: 03/11/2026. Không chứa metric local chạy dở.','']
    for rec in evidence['sources']:
        source_map.append(f"- **{rec['id']}** — {rec['title']}: [{rec['path']}]({Path(os.path.relpath(ROOT/rec['path'],HERE))}); SHA-256 `{rec['sha256']}`.")
    (HERE/'source-map.md').write_text('\n'.join(source_map)+'\n')
    print(f'Built study-guide.pdf from {len(chapters)+1} chapters; references stable after {attempt+1} passes')

if __name__=='__main__':
    main()
