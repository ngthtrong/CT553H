"""Render the report from final machine-readable artifacts, using stdlib only."""
import csv
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_json(name):
    return json.loads((HERE/name).read_text())


def rows(name):
    with (HERE/name).open() as stream:
        return list(csv.DictReader(stream))


def table(header, data):
    return '\n'.join(['| '+' | '.join(header)+' |',
                      '| '+' | '.join(['---']*len(header))+' |']+
                     ['| '+' | '.join(map(str,r))+' |' for r in data])


def main():
    result=read_json('results.json'); valid=read_json('validation.json')
    independent=read_json('independent-validation.json')
    runtime=read_json('runtime.json'); inputs=read_json('input-manifest.json')
    assert valid['status']=='pass' and independent['status']=='pass'
    primary={r['policy']:r for r in result['primary_summary']}
    names=['lora-D','ridge-w5-D','random','frozen-D','lora-B']
    primary_table=table(['Chính sách','Precision@10','Hit / 2.350 lựa chọn','Recall@10'],[
        [name,f"{100*primary[name]['precision']:.2f}%",f"{primary[name]['hits_total']:.2f}" if name=='random' else str(int(primary[name]['hits_total'])),
         f"{100*primary[name]['recall']:.2f}%"] for name in names])
    contrast_table=table(['LoRA-D trừ','Δ precision (điểm %)','CI95 mô tả','CI97,5 Bonferroni'],[
        [c['baseline'],f"{100*c['delta']:+.2f}",
         f"[{100*c['ci95'][0]:+.2f}; {100*c['ci95'][1]:+.2f}]",
         f"[{100*c['ci_adjusted'][0]:+.2f}; {100*c['ci_adjusted'][1]:+.2f}]"]
        for c in result['primary_contrasts']])
    seed_table=table(['Chính sách','Seed 17','Seed 29','Seed 43','Ensemble'],[
        [name,*[f"{100*next(x for x in result['per_seed_primary'] if x['policy']==name and x['prediction_set']==f'seed{s}')['precision']:.2f}%" for s in [17,29,43]],
         f"{100*primary[name]['precision']:.2f}%"] for name in names if name!='random'])
    btr_table=table(['Chính sách','Lựa chọn để đạt 50% hit','Lựa chọn để đạt 80% hit'],[
        [name,f"{primary[name]['btr50']:.2f}",f"{primary[name]['btr80']:.2f}"]
        for name in ['lora-D','ridge-w5-D','random']])
    summary=rows('summary.csv')
    minus={r['policy']:r for r in summary if r['prediction_set']=='ensemble' and r['direction']=='minus' and r['budget']=='k10'}
    minus_table=table(['Chính sách','Precision@10 âm','Hit âm / 2.350'],[
        [name,f"{100*float(minus[name]['precision']):.2f}%",f"{float(minus[name]['hits_total']):.2f}" if name=='random' else str(int(float(minus[name]['hits_total'])))]
        for name in names])
    stratum=rows('strata.csv')
    strata_table=[]
    for value in ['le3','gt3_le4','gt4_le5','gt5']:
        selected={r['policy']:r for r in stratum if r['stratum']=='psi_stratum' and r['value']==value and r['direction']=='plus'}
        strata_table.append([value,selected['lora-D']['peptides'],*[f"{100*float(selected[name]['precision']):.2f}%" for name in ['lora-D','ridge-w5-D']]])
    strata_table=table(['PSI(WT)','Peptide','LoRA-D P@10','W5-D P@10'],strata_table)
    ties=[r for r in result['tie_sensitivity'] if r['prediction_set']=='ensemble' and r['direction']=='plus' and r['budget']=='k10']
    tie_table=table(['Chính sách','Peptide có tie ở ngưỡng k10','P@10 thấp nhất–cao nhất, 100 seed'],[
        [r['policy'],r['cutoff_tie_peptides'],f"{100*r['macro_precision_min']:.4f}%–{100*r['macro_precision_max']:.4f}%"] for r in ties])
    pp=rows('per-peptide.csv')
    min_n=min(int(r['n']) for r in pp);max_n=max(int(r['n']) for r in pp)
    legacy_changed=sum(r['different_peptide_budgets'] for r in result['legacy_helper_reconciliation'])
    favorable=sum(r['primary'] and r['ci_adjusted'][0]>0 for r in result['primary_contrasts'])
    text=f'''## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run, tiếp theo kiểm số học và tái lập
- Origin Date: 2026-11-07
- Verification Status: VERIFIED cho tính toán/input đã lưu, không phải wet-lab validation
- Version Label: oof_priority_result_v1

# Ưu tiên mutation với cùng ngân sách — đánh giá hồi cứu OOF

**[ĐO] LoRA-D tìm được 1.260 hit dương trong 2.350 lựa chọn, so với 1.087 của
Ridge W5-D và kỳ vọng random 229,86.** Precision@10 tương ứng 53,62%, 46,26%
và 9,78%. Cả {favorable}/2 CI hiệu chỉnh của hai contrast chính đều nằm trên 0.
Nguồn số chuẩn: [results.json](results.json), [summary.csv](summary.csv).

**[DIỄN GIẢI] Kết quả hỗ trợ ưu tiên mutation tốt hơn hai đối chứng trong
replay development này.** Đã có bằng chứng định lượng hồi cứu của CT553H;
chưa có lượt wet lab mới, số giờ/tiền tiết kiệm đã đo, kiểm định độc lập ngoài
development hoặc quyết định nghiệm thu G2/G3. Mô hình phục vụ không thay đổi.

## Thiết kế và input

[Protocol đã khóa](PROTOCOL.md), [config.json](config.json) và [nhật ký bổ sung
độ bao phủ](AMENDMENTS.md) giữ thiết kế trước chấm và thay đổi triển khai sau
lượt đầu. Người dùng đã yêu cầu thực hiện `tmp.md`; không suy đây là tiền đăng
ký độc lập với dữ liệu development từng được khảo sát.

- W full-PSI: **235 peptide, 221 group, 122.412 mutation đơn không đồng nghĩa**.
- Ba seed 17/29/43, năm outer fold; rank bên trong peptide, không rank toàn
  proteome. Trung bình prediction ba seed rồi mới rank cho ensemble.
- Candidate/peptide: {min_n}–{max_n}; tất cả đủ 10 lựa chọn. Ngân sách chính
  bằng 10/peptide, tổng 2.350 cho mọi policy; k=5,20 và top 5/10/20% là phụ.
- Hit dương: ΔPSI thực nghiệm >=1. Hit âm: ΔPSI <=-1, rank theo -prediction.
- Giữ **37 peptide không hit dương** và **84 không hit âm** trong Precision.
  Recall/enrichment/budget-to-recall dùng 198 peptide có hit dương hoặc 151 có
  hit âm; `null` có lý do trong [per-peptide.csv](per-peptide.csv).
- Random chọn đều không hoàn lại. Bảng chính dùng kỳ vọng giải tích, không
  lấy một lượt random thuận lợi. Có 2.000 random permutation/peptide để kiểm
  số học và vẽ dải dao động; prefix các ngân sách lồng nhau trong cùng lượt.
- Tie dùng hash SHA-256 của seed/peptide/cell, seed chính 1729; kiểm 100 seed
  0..99 ở cả sáu ngân sách, mọi policy/seed/hướng, không chọn seed tốt nhất.

[Input manifest](input-manifest.json) kiểm SHA-256/kích thước của
{inputs['source_file_count']} file dùng thực sự ({inputs['source_bytes_checked']:,} byte), exact cohort mỗi seed,
metadata/nhãn, mode/recipe/identity và split. 45 OOF fold local khớp collection;
45 lựa chọn epoch được tính lại từ validation prediction đã lưu. Quần thể
calibration/selection của 60 fold loại outer-test. Không deserialize model.

Giới hạn audit: nhóm fit local được dựng lại từ split/arm và mã, không có
danh sách nhóm thực tế trong checkpoint; không tái chạy train. Không có prediction
từng alpha Ridge nên chưa tái chứng minh lựa chọn alpha; chỉ đối chiếu metadata,
nhóm fit và quần thể validation. Chi tiết ở `input-manifest.json.limitations`.

## Kết quả chính: hit dương, 10 lựa chọn/peptide

{primary_table}

Precision là peptide-macro trên 235 peptide; Recall là peptide-macro trên 198
peptide có hit dương. Số random là kỳ vọng, có thể không nguyên. Frozen-D và
LoRA-B là phân tích phụ đã chỉ định, không dùng để chọn lại recipe chính.

### Hai contrast chính

{contrast_table}

Paired bootstrap 5.000 lần lấy mẫu **group_id**, mang toàn bộ peptide của mỗi
nhóm được lấy. Estimand vẫn là peptide-macro. CI97,5 dùng Bonferroni cho đúng
hai contrast chính; các CI95 khác là mô tả. So W5, LoRA-D có thêm **173 hit**
trên cùng 2.350 lựa chọn trong replay. So random kỳ vọng, chênh khoảng
**1.030,14 hit**; đây không phải số hit của một campaign random wet lab đã chạy.

### Từng seed

{seed_table}

Các seed dùng chung outer split và nhãn, không phải ba nghiên cứu độc lập.
LoRA-B ensemble cao hơn LoRA-D 0,34 điểm %, nhưng CI95 của D−B là
[-2,06; +1,34] điểm %: chưa phân giải, không đổi recipe chính sau xem utility.

## Ngân sách để thu hồi hit đã biết — phân tích phụ

{btr_table}

Các số là trung bình trên 198 peptide có hit dương; mục tiêu là ceil(r × tổng
hit của peptide). Chênh LoRA-D−W5 khi thu hồi 50% hit: -10,67 lựa chọn/peptide,
CI95 [-16,48; -4,96]; khi thu hồi 80%: -16,17, CI95 [-24,45; -7,64].
Các số giảm lựa chọn là **hồi cứu**, chưa phải số assay/giờ/tiền tránh được
trong thực tế. Tổng hit chỉ biết vì đã có nhãn, không dùng làm quy tắc dừng
khi triển khai wet lab.

## Chiều âm, phân tầng và độ nhạy

{minus_table}

Chiều âm là phụ; LoRA-D−W5 Precision@10 = +9,66 điểm %, CI95 [7,13; 12,35].
Không gộp hai chiều thành một điểm thành công.

{strata_table}

Mức lợi ích thay đổi theo PSI(WT): miền (4,5] gần tương đương về point estimate;
miền >5 không có hit dương trong dữ liệu. [strata.csv](strata.csv) báo toàn bộ
fold, PSI và độ thưa hit, denominator cùng CI95 mô tả; không chọn subgroup tốt
để thay kết luận toàn W. Độ thưa hit là phân tầng nhãn, không phải thang đo độ
khó sinh học hay điều kiện chọn trước thí nghiệm.

{tie_table}

Đối chiếu helper cũ: khi cùng thứ tự dòng/tie stable, top 5/10/20% khớp helper.
Đổi sang hash tie có {legacy_changed} hàng peptide–policy–hướng–tỷ lệ khác precision;
mọi chênh đều nằm tại cutoff có tie. Đây là khác biệt có chủ đích, được báo
trong `results.json.legacy_helper_reconciliation`, không trộn với kết quả cũ.

![Đường cong ngân sách](budget-curves.png)

Dải màu là CI95 bootstrap theo protein của **từng đường**, không phải CI của
chênh giữa hai đường; dùng bảng contrast để đánh giá chênh. Dải xám là 95%
dao động phân bổ random có điều kiện trên cohort cố định, không phải CI theo
protein. Trục ngân sách log; k thực tế bị chặn bởi số candidate của peptide.
[CSV đường cong](budget-curves.csv), [random reference](random-reference.csv).

## Ví dụ và kiểm chứng

[ranking-examples.csv](ranking-examples.csv) giữ top 10, vị trí, WT→mutant,
prediction, ΔPSI thực và hit cho peptide đầu tiên theo thứ tự từ điển trong
mỗi PSI stratum, mọi policy và hai hướng. Không chọn riêng case thuận lợi.

[validation.json](validation.json) kiểm công thức bằng liệt kê mọi permutation
với N=1..6; no/all hits, N<k, full tie, thiếu seed, duplicate/cell mismatch,
đảo thứ tự dòng, BTR và cluster không cùng kích thước. 2.000 lượt random khớp
kỳ vọng trong sai số Monte Carlo đã báo. [independent-validation.json](independent-validation.json)
tái tính primary/CI trực tiếp bằng một triển khai khác, kiểm bảng và input
không đổi; đây là kiểm số học độc lập, không phải một nghiên cứu độc lập.

[validation.md](validation.md) giữ kiểm 11 loại lỗi diễn giải thống kê và giới
hạn. Hai ngữ cảnh native hỗ trợ triển khai/audit; không có cross-model review,
không có xác nhận người dùng đã đọc toàn bộ nguồn.

## Tái tạo và runtime

Từ gốc repo, dùng môi trường phân tích có các phiên bản trong
[requirements-analysis.txt](requirements-analysis.txt):

```bash
.venv/bin/python -I research/oof-prioritization-2026-11-07/evaluate.py
.venv/bin/python -I research/oof-prioritization-2026-11-07/validate_outputs.py
python3 research/oof-prioritization-2026-11-07/write_report.py
```

Không cần GPU hoặc load model. Lượt cuối: {runtime['wall_seconds']:.2f} giây wall,
{runtime['cpu_seconds']:.2f} giây CPU, peak process RSS {runtime['peak_process_rss_mib']:.1f} MiB
trên Linux/WSL, Python {runtime['python'].split()[0]}; [runtime.json](runtime.json).
Đây là tài nguyên tính toán chấm OOF, không phải chi phí/thời gian wet lab.

Artifact nhẹ gồm mã/config/protocol/manifest/JSON/CSV/PNG được giữ trong thư
mục này. Bảng toàn seed, curve từng peptide, log và bản lượt đầu ở `local/`,
được Git ignore. Không ghi đè campaign state/manifest, phân tích cũ, dữ liệu
gốc, hồ sơ wet lab, checkpoint hoặc mô hình phục vụ. Clone Git riêng không
đủ để tái chạy nếu thiếu các OOF và bundle dữ liệu đã pin.

**AI disclosure:** Codex hỗ trợ triển khai, kiểm input/số học và soạn báo cáo.
Phép đánh giá là hậu kiểm development, không sửa được lịch sử chọn model hoặc
bao gồm bất định do outer split/huấn luyện mới/assay mới. Các CI và hiệu chỉnh
hai contrast không biến kết quả thành prospective wet-lab validation.
'''
    (HERE/'README.md').write_text(text,encoding='utf8')
    checks=[
        ('Simpson','NOTE','Đối chiếu PSI và fold: không quan sát đảo dấu so W5; mức lợi ích không đồng nhất. Không kết luận cho các phân tầng chưa xét.'),
        ('Ecological fallacy','NOTE','Estimand peptide-macro; không suy mọi mutation/protein đều tốt hơn.'),
        ('Berkson / selection','CAUTION','W là cohort đã chọn/QC, không phải mọi peptide tự nhiên; không tái lập QC hay khảo sát missingness nguồn.'),
        ('Collider bias','NOTE','Primary không điều kiện thêm vào nhãn; phân tầng số hit là mô tả hậu kiểm, không suy quan hệ nhân quả.'),
        ('Base rate neglect','NOTE','Random là prevalence theo peptide; no-hit giữ trong Precision; denominator Recall khác được công bố.'),
        ('Regression to mean','NOTE','Không có pre/post trên nhóm cực trị; không suy cải thiện thực nghiệm từ replay.'),
        ('Survivorship','NOTE','Giữ toàn bộ 235 peptide, cả 37 không hit dương và 84 không hit âm; nguồn sau QC vẫn có giới hạn chọn mẫu.'),
        ('Look elsewhere','CAUTION','Hiệu chỉnh hai contrast chính; toàn bộ ngân sách/hướng/recipe phụ được báo, CI phụ chỉ mô tả.'),
        ('Forking paths','CAUTION','Khóa config trước utility nhưng dữ liệu/model development đã được xem; amendment được giữ, không phải preregistration.'),
        ('Correlation / causation','CAUTION','Không diễn giải ưu thế replay thành tác động nhân quả lên wet lab hoặc tiết kiệm thực tế.'),
        ('Reverse causality','NOTE','Prediction OOF được lưu trước replay; không đặt kết luận cơ chế nhân quả hay clinical từ điểm dự đoán.'),
    ]
    validation='''## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate
- Origin Date: 2026-11-07
- Verification Status: VERIFIED trong phạm vi kiểm số học trực tiếp; CAUTION về suy rộng khoa học
- Version Label: oof_priority_validation_v1

# Kiểm chứng và giới hạn

Input audit, scorer edge cases và kiểm độc lập primary/CI đều PASS, xem
[input-manifest.json](input-manifest.json), [validation.json](validation.json)
và [independent-validation.json](independent-validation.json).
Lượt đầu và lượt cuối giữ nguyên bảng per-peptide, summary và hai primary
contrast (bản đầu được lưu local); chỉ mở rộng độ bao phủ tie/CI phân tầng.
Các kiểm này không chứng nhận pipeline huấn luyện từ đầu hoặc wet lab.

Hai contrast chính dùng CI97,5 Bonferroni; không tính p-value mới hoặc
gán mức hiệu quả thực tiễn chưa được đối tác wet lab định nghĩa. Tất cả
secondary contrast/CI và phân tầng là mô tả trên development.

## Fallacy scan — 11/11 loại được xét trong phạm vi báo cáo

'''+table(['Loại','Trạng thái','Quan sát/giới hạn'],checks)+'''

## Kiểm artifact

- Figure đã được mở kiểm trực quan: hai hướng, trục log, label/legend/dải CI
  hiện đầy đủ; CSV tách conditional random band khỏi cluster CI.
- README giữ denominator và kết quả không thuận lợi/không phân giải.
- Không có train/refit/inference mới, `.pt`/pickle load, nguồn ngoài mới,
  model phục vụ mới, hoặc dữ liệu gửi tới dịch vụ mô hình ngoài.
- Nguồn raw/campaign/output phân tích cũ được đối chiếu hash; không sửa manifest
  để ép identity. Không có commit hoặc push.
'''
    (HERE/'validation.md').write_text(validation,encoding='utf8')
    artifacts={}
    for p in sorted(HERE.iterdir()):
        if p.is_file() and p.name!='artifact-manifest.json':
            artifacts[p.name]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    (HERE/'artifact-manifest.json').write_text(json.dumps(dict(
        generated_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),files=artifacts),
        ensure_ascii=False,indent=2)+'\n')
    print('Rendered README.md, validation.md, artifact-manifest.json')


if __name__=='__main__':
    main()
