"""Write a Vietnamese evidence report from completed CPU analysis and validation."""
import hashlib
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"]*len(headers)) + " |",
                       *["| " + " | ".join(map(str, row)) + " |" for row in rows]])


def pct(x):
    return f"{100*float(x):.2f}%"


def ci(x, scale=1):
    if isinstance(x, str):
        x = json.loads(x)
    return "[" + "; ".join(f"{v*scale:+.4f}" for v in x) + "]"


def main():
    r = json.loads((HERE/"results.json").read_text())
    v = json.loads((HERE/"validation.json").read_text())
    inv = json.loads((HERE/"input-manifest.json").read_text())
    runtime = json.loads((HERE/"runtime.json").read_text())
    assert v["status"] == "pass"
    assert v["result_sha256"] == hashlib.sha256((HERE/"results.json").read_bytes()).hexdigest()
    perf = pd.read_csv(HERE/"performance.csv")
    ts = pd.read_csv(HERE/"threshold-sensitivity.csv")
    tc = pd.read_csv(HERE/"threshold-contrasts.csv")
    cal = pd.read_csv(HERE/"calibration.csv")
    sm = pd.read_csv(HERE/"similarity-contrasts.csv")
    sim = pd.read_csv(HERE/"similarity.csv")
    agreement = pd.read_csv(HERE/"label-agreement.csv")
    names = {"esm2_35m-lora-B": "LoRA-B", "esm2_35m-lora-D": "LoRA-D", "esm2_35m-frozen-B": "Frozen-B",
             "esm2_35m-frozen-D": "Frozen-D", "ordered-w5-D": "W5-D"}
    transfer_rows = []
    for cohort in ["W-full", "W-mutant-RAS", "W-scanning-pairs", "T-rep1-full", "T-intersection-rep1", "T-intersection-rep2", "T-intersection-mean12"]:
        f = perf[(perf.recipe == "ordered-w5-D") & (perf.cohort == cohort) & (perf.axis == "all")
                 & (perf.prediction_set.isin(["ensemble", "locked-final"]))].iloc[0]
        contrast = next(x for x in r["transfer_vs_zero"] if x["cohort"] == cohort and x["axis"] == "all")
        transfer_rows.append([cohort, f"{int(f.cells):,}", int(f.peptides), f"{f.mae:.6f}", f"{f.zero_mae:.6f}",
                              f"{contrast['delta']:+.6f}", ci(contrast["ci95"])])
    core_rows = []
    for arm in ["B", "D"]:
        c = next(x for x in r["matched_and_utility_contrasts"] if x["a"] == f"esm2_35m-lora-{arm}"
                 and x["b"] == f"esm2_35m-frozen-{arm}" and x["metric"] == "mae" and x["axis"] == "all" and x["cohort"] == "W-full")
        core_rows.append([arm, f"{c['delta']:+.6f}", ci(c["ci_adjusted"])])
    consensus_rows = []
    for recipe in ["esm2_35m-lora-D", "esm2_35m-frozen-D", "ordered-w5-D", "esm2_35m-lora-B", "esm2_35m-frozen-B"]:
        f = ts[(ts.recipe == recipe) & (ts.threshold == 1) & (ts.direction == "plus")].set_index("target")
        consensus_rows.append([names[recipe], pct(f.loc["mean", "delta"]), pct(f.loc["half_a", "delta"]),
                               pct(f.loc["half_b", "delta"]), pct(f.loc["both_halves", "delta"])])
    con = tc[(tc.a == "esm2_35m-lora-D") & (tc.b == "ordered-w5-D") & (tc.threshold == 1)
             & (tc.direction == "plus") & (tc.target == "both_halves")].iloc[0]
    j = agreement[(agreement.threshold == 1) & (agreement.psi_stratum == "all")].set_index("direction")
    label_rows = [[d, pct(j.loc[d, "prevalence_mean"]), pct(j.loc[d, "event_xor_rate"]), f"{j.loc[d, 'event_jaccard']:.4f}"]
                  for d in ["plus", "minus"]]
    sim_rows = [[row.arm, row.identity_bin, int(row.peptides), int(row.groups), f"{row.delta:+.6f}", ci(row.ci95)]
                for row in sm.itertuples()]
    cal_rows = [[names[row.recipe], row.cohort, f"{row.brier_micro:.6f}", f"{row.ece_plus:.6f}",
                f"{row.ece_minus:.6f}", f"{row.probability_bias_plus:+.6f}"]
               for row in cal[cal.axis == "all"].itertuples()]
    strata_rows = [[x["value"], x["peptides"], f"{x['delta']:+.6f}", ci(x["ci95"])]
                   for x in r["transfer_vs_zero"] if x["cohort"] == "T-rep1-full" and x["axis"] == "psi_stratum"]
    text = f"""# Kiểm chứng độ tin cậy và giới hạn chuyển miền — đợt CPU 08/11/2026

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent.
- Origin Mode: validate; phân tích chẩn đoán trên artifact đã lưu.
- Verification Status: **VERIFIED trong phạm vi số học/input đã kiểm**;
  không phải tái huấn luyện độc lập hoặc external biological validation.
- Version Label: reliability_transfer_cpu_v1.
- Commit nguồn: `{inv['source_commit']}`. Thời điểm tính: `{r['generated_at']}`.

## Kết luận chính

**[ĐO] Đã thực hiện phân tích CPU, không train/refit/inference và không GPU.**
Matched LoRA–frozen được tái kiểm; diagnostic mới cho thấy bất đồng event giữa
hai nửa assay, lợi ích trên target consensus và giới hạn chuyển miền W5 vẫn
còn sau khi xét directed substitution design hoặc target trung bình replicate.

**[DIỄN GIẢI]** Kết quả hỗ trợ độ bền development trong các phép kiểm đã định;
không đủ để tuyên bố LoRA tổng quát hóa trên T, nguồn mới hoặc protein tự nhiên.
Chưa thay model phục vụ hoặc quyết định G2/G3. [Protocol](PROTOCOL.md),
[config](config.json), [kết quả JSON](results.json), [kiểm số học](validation.json).

## 1. Phạm vi và tính toàn vẹn

- W: 122.412 cell, 235 peptide, 221 nhóm; seed 17/29/43, năm outer fold.
- T rep1 đã lưu: 39.234 cell, 1.410 peptide, 730 nhóm; cùng nguồn Zhang.
- Kiểm SHA/kích thước **{inv['file_count']} input**, {inv['bytes_checked']:,} byte,
  trước và sau phân tích; 32 file của bundle cũng được kiểm theo manifest.
- Kiểm 15 assignment seed/fold; OOF phải đủ cohort, metadata, seed và nhãn.
- Hợp WT/mutant đo được của W và toàn scanning có **{r['exact_sequence_audit']['unique_sequences']:,}
  sequence duy nhất, 0 exact sequence được gán vào hai group khác nhau**.
  Các observation lặp sequence trong cùng group được giữ nguyên.
- Hash chứng minh bytes/lineage đã lưu, không tái chứng minh training execution,
  checkpoint tensor, remote homology hoặc độc lập sinh học hoàn toàn.

[Input manifest](input-manifest.json) giữ từng nguồn và authority hash. Không
đụng vào manifest/state/checkpoint/dữ liệu gốc. [Nhật ký precision](AMENDMENTS.md)
giải thích float64 accumulation và chênh làm tròn với các báo cáo lịch sử.

## 2. Độ bền matched comparison

MAE là peptide-macro; dấu âm LoRA−frozen có lợi. B chỉ giới hạn train/refit
PSI≤4, validation/test vẫn full-range. Ensemble trung bình prediction ba seed.

{table(['Arm', 'ΔMAE LoRA−frozen', 'CI98,75% đã đối chiếu'], core_rows)}

**[ĐO]** CI family gốc được tái tạo trong sai số precision input float32.
Đây là family bốn contrast hậu kiểm gốc, không hiệu chỉnh toàn bộ lịch sử thử
model. Các bảng [performance](performance.csv), [per-peptide](per-peptide.csv)
và [seed contrasts](seed-contrasts.csv) giữ mọi seed/fold/subset đã chỉ định.
Ba seed dùng chung outer partition và nhãn, không là ba nghiên cứu độc lập.

## 3. Replicate và độ nhạy định nghĩa hit

Pearson ΔPSI a/b = **{r['replicate']['pearson_a_b']:.4f}**; bất đồng tuyệt đối
trung bình **{r['replicate']['mean_absolute_disagreement']:.4f} PSI**.
Đây là hai nửa assay theo pipeline nguồn, chưa xác nhận hai biological
replicate độc lập. Count support tối thiểu a/b =
{r['replicate']['support_min_a']:.4f}/{r['replicate']['support_min_b']:.4f};
đơn vị là **tổng count đã chuẩn hóa**, không phải raw sequencing reads.

Với threshold ±1, các tỷ lệ dưới là **cell-micro**:

{table(['Event', 'Prevalence nhãn mean', 'Hai nửa khác nhãn', 'Jaccard a/b'], label_rows)}

**[DIỄN GIẢI]** Event âm hiếm và độ trùng event thấp hơn chiều dương. Jaccard
không tách được measurement noise, shared-reference uncertainty hoặc biology.
Miền PSI>5 không có event dương ở threshold 1 trong cả hai nửa; Jaccard ghi
null có lý do, không điền 0.

Giữ score và top10 cố định; thay **target chấm**, không re-rank theo nhãn:

{table(['Policy', 'Mean≥1', 'Nửa a≥1', 'Nửa b≥1', 'Cả a và b≥1'], consensus_rows)}

**[ĐO]** Với target consensus dương, LoRA-D−W5-D =
**{100*con.delta:+.2f} điểm %**, CI95 mô tả **{ci(con.ci95, 100)} điểm %**.
Đây là target chặt hơn, không phải lower confidence bound cho hit thật.
Giữ cả peptide không hit trong precision, cùng 2.350 lựa chọn mỗi policy.
Không thay kết quả primary replay 07/11 hoặc chọn threshold tốt nhất.

Toàn bộ threshold .75/1/1.25, hai chiều, bốn target và các baseline được báo tại
[threshold sensitivity](threshold-sensitivity.csv), [paired contrasts](threshold-contrasts.csv).
CI mới là mô tả, không globally-adjusted. [Disagreement errors](disagreement-errors.csv)
và [bounds](prediction-bounds.csv) là hậu kiểm nhãn/WT PSI, không feature/gate deploy.

## 4. Tương đồng peptide với tập refit

Identity là phần residue **đúng cùng vị trí trên 28 AA**, không sequence alignment;
5-mer coverage là proxy local-motif. Reference W loại outer-test group, áp arm
B/D đúng population; reference T là toàn W của final W5.

{table(['Arm', 'Bin identity', 'Peptide', 'Group', 'ΔMAE LoRA−frozen', 'CI95 mô tả'], sim_rows)}

Max aligned identity ở W là **{sim[sim.cohort == 'W'].max_aligned_identity.max():.4f}**,
ở T→W **{sim[sim.cohort == 'T'].max_aligned_identity.max():.4f}**.
Bins từ .5 trở lên không có quan sát W; không suy độ bền ở miền không được đo.
Lợi ích matched vẫn hiện trong các bin có dữ liệu, nhưng hai proxy này không
phát hiện mọi alignment lệch vị trí/remote homology/PLM pretraining exposure.
Không thay grouping/split và không gọi kiểm này là retraining với split chặt hơn.

[Similarity từng peptide](similarity.csv), [contrast theo bin](similarity-contrasts.csv).

## 5. Chuyển miền: substitution design và target replicate

Scanning có 20 directed WT→mutant pairs. W-mutant-RAS giữ mọi replacement vào
R/A/S; W-scanning-pairs chỉ giữ đúng 20 pairs. Các mask chỉ dùng để chấm score
đã lưu, không train lại hoặc match đầy đủ protein/assay/target.

{table(['Cohort/target', 'Cell', 'Peptide', 'MAE W5', 'MAE zero', 'W5−zero', 'CI95 mô tả'], transfer_rows)}

**[ĐO]** Trên W-scanning-pairs, lợi thế W5 so zero còn có CI phía âm; trên T
rep1 full CI chứa 0. Khi đổi target trên cùng intersection 39.112 cell/1.407
peptide/730 nhóm sang mean12, CI vẫn chứa 0 và point estimate đổi phía.

**[DIỄN GIẢI]** Khác substitution design hoặc chỉ dùng rep1 chưa đủ giải thích
hay khắc phục giới hạn hồi quy quan sát được. Không coi đây là phân rã nhân
quả hoặc kết luận model tuyệt đối không thể transfer. T và W khác protein,
sampling, prevalence và design; so W OOF với final T còn khác fit procedure.
P@10 trên candidate pool T/W khác kích thước cũng không cùng tỷ lệ sàng lọc.

Theo miền PSI trên T rep1:

{table(['WT PSI', 'Peptide', 'W5−zero MAE', 'CI95 mô tả'], strata_rows)}

**[ĐO]** Miền WT PSI cao có sai số W5 cao hơn zero trong các CI mô tả được
báo; miền thấp có lợi ích. Không chọn lại recipe hoặc tạo gate bằng test PSI.
LoRA vẫn **chưa có prediction trên T**. Không đánh đồng diagnostic này với
independent external validation.

## 6. Calibration đã lưu

Brier dưới đây là ba lớp, cell-micro; bảng CSV có thêm peptide-macro. ECE dùng
10 bin equal-width. Bias xác suất = mean predicted probability−observed rate.

{table(['Model', 'Cohort', 'Brier3', 'ECE+', 'ECE−', 'Bias P+'], cal_rows)}

**[ĐO]** W5 có probability bias dương trên T; reliability/ECE xấu hơn W ở
endpoint dương dù Brier T thấp hơn. Brier giữa hai population khác prevalence
không chứng minh calibration T tốt hơn. Calibration trung bình toàn W cũng
có thể che bias theo PSI. LoRA Brier thấp hơn frozen nhưng ECE+ cao hơn.

Không fit/recalibrate trên T. Fold calibrator, refit score distribution và
final serving calibration vẫn phải phân biệt. [Calibration table](calibration.csv),
[reliability bins và denominator](reliability-bins.csv).
Bin W5 P+ cao nhất trên W chỉ có một cell/một nhóm; không diễn giải điểm đó
như một ước lượng reliability chính xác. Hình đánh dấu các bin dưới 20 cell.

![Chẩn đoán CPU](diagnostics.png)

Hình A: CI ghép cặp W5−zero; hình B: point estimate cho các target khác nhau;
hình C: reliability bins, không phải CI; hình D: event overlap hai nửa assay.
Không có prospective wet-lab result trong hình.

## 7. Bằng chứng còn thiếu và quyết định tiếp

1. **Chưa đo:** LoRA/frozen trên T, nguồn mới độc lập, repeated grouped
   repartition/retraining, remote-homology sensitivity đầy đủ.
2. **Không tự chuyển sang train mới:** trước hết khóa use case/endpoint,
   compute budget và practical threshold; giữ các outcome chưa phân giải.
3. [NEXT-EVALUATION.md](NEXT-EVALUATION.md) là thiết kế chưa chạy cho LoRA-D,
   frozen-D, W5, zero; giữ T là nguồn đã xem và tách nguồn mới độc lập.
4. Final refit/export, serving policy và G2/G3 là bước riêng. Không dùng audit
   này để tự đóng gate hoặc thay model sản phẩm.

## 8. Tái tạo, kiểm chứng và tài nguyên

Từ gốc repo với môi trường phân tích CPU có phiên bản ở
[requirements-analysis.txt](requirements-analysis.txt):

```bash
.venv/bin/python -I research/reliability-transfer-2026-11-08/analyze.py
.venv/bin/python -I research/reliability-transfer-2026-11-08/validate.py
.venv/bin/python -I research/reliability-transfer-2026-11-08/plot.py
.venv/bin/python -I research/reliability-transfer-2026-11-08/write_report.py
.venv/bin/python -I research/reliability-transfer-2026-11-08/check_delivery.py
```

Không cài đè requirements này lên môi trường CUDA Windows. Cần bundle/OOF/
calibration local đã pin; clone Git riêng không đủ để tái tạo.

Lượt phân tích cuối: **{runtime['wall_seconds']:.2f} giây wall**, {runtime['cpu_seconds']:.2f}
giây CPU, peak RSS **{runtime['peak_rss_mib']:.1f} MiB**, cấu hình hai CPU thread.
Không import torch/transformers/cupy/tensorflow/jax; CUDA_VISIBLE_DEVICES rỗng;
không load model. Đây là tài nguyên phân tích, không training hoặc wet-lab cost.

Validator có **{len(v['checks'])} nhóm kiểm**, gồm tính trực tiếp từ OOF,
mean/consensus P@10, T target/zero và CI bằng triển khai resampling khác;
edge cases macro/cluster không đều, no class, N<k, tie permutation, bins 0/1.
Kiểm hash input lại sau cùng. Không phải phản biện mù hoặc một nghiên cứu độc lập.
[Biên bản bàn giao](delivery-validation.json) và [manifest artifact](artifact-manifest.json)
giữ phạm vi kiểm, liên kết, hash mã/kết quả và xác nhận kiểm hình trực quan.

## 9. Fallacy scan — 11/11 nhóm được xét

| Loại | Đánh giá trong phạm vi này |
|---|---|
| Simpson | Báo PSI strata; không dùng trung bình toàn W/T để khẳng định mọi miền tốt. |
| Ecological fallacy | Peptide-macro không thành kết luận từng mutation/protein. |
| Berkson/selection | W/T đã QC/chọn nguồn; không đại diện proteome ngẫu nhiên. |
| Collider | Strata nhãn/noise là hậu kiểm; không suy causal mechanism hoặc dùng để deploy. |
| Base-rate neglect | Báo prevalence, zero baseline, no-hit và denominator metric. |
| Regression to mean | Không có prospective pre/post; label agreement không là cải thiện assay. |
| Survivorship | Giữ đủ cohort từng metric; intersection replicate được báo tách riêng. |
| Look elsewhere | Mọi grid đã định được báo; CI phụ mô tả, không correction toàn lịch sử. |
| Forking paths | Dữ liệu/metric đã xem; protocol này không phải preregistration độc lập. |
| Correlation/causation | Không quy lỗi cho duy nhất noise/design hoặc tuyên bố savings. |
| Reverse causality | Prediction lưu trước diagnostic; không xác nhận E3/clinical mechanism. |

**AI disclosure:** Codex hỗ trợ mã, kiểm số học và tổng hợp. Một session cùng
ngữ cảnh, không subagent/cross-model review. Giới hạn đầy đủ ở
`results.json.limitations`; tệp theo peptide lớn của threshold ở `local/` bị
Git ignore. Không commit/push, sửa report/proposal/data/campaign/serving.
"""
    (HERE/"README.md").write_text(text, encoding="utf8")
    print("PASS Vietnamese diagnostic report generated")


if __name__ == "__main__":
    main()
