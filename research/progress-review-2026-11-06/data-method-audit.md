# Kiểm toán dữ liệu, nhãn và tính tương thích phương pháp — 06/11/2026

## Mức bằng chứng

[ĐỐI CHIẾU MÃ/JSON] Đọc loader, builder v3, metadata/schema, JSON lịch sử và các kết quả đã lưu. Không dựng lại dữ liệu, không tải nguồn mới, không sửa `data/`, không train. Kiểm hash/prediction trực tiếp của campaign được ghi riêng ở [local-audit.md](local-audit.md). Sổ [data/README.md](../../data/README.md) cung cấp provenance/giấy phép; số đếm dưới lấy thêm từ JSON kết quả tương ứng, không xem mô tả README là phép đo mới.

## Nguồn, đơn vị và nhãn

| Thành phần | Nguồn/định nghĩa dùng thực tế | Vai trò và giới hạn |
|---|---|---|
| Zhang mutagenesis | Mendeley Data v2, DOI `10.17632/32h94v2yv2.2`; sáu FACS bin, read/count và các condition | Nguồn nhãn chính. PSI thuộc reporter fusion trong assay này, không phải thời gian bán hủy hay ΔΔG gấp cuộn. |
| Reference sequence | UniProt human reviewed snapshot release 2026_03 và các accession bổ sung đã ghi nguồn | Kiểm residue/tile/canonical mapping. Cụm dựa full-protein sequence là heuristic, không bảo đảm không còn local motif/homology xa. |
| Voutsinos/PAP | Repo ghim `9b3eafa6bd9730c558cd018063fa0180edf9db1a` | Baseline điểm peptide và pretraining P3. Không dùng điểm degron làm nhãn ground truth cho mutation CT553H. |
| Koren S4 | Supplementary S4; PSI ba bin, construct khác Zhang | Audit nguồn có dữ liệu nhưng chưa có external prediction campaign mới. 5 cụm mới, không đạt cổng mở train≥20 cụm. Không gộp ΔPSI giữa thang 1–3 và 1–6. |
| Larsen, MaveDB, ClinVar, MetaDegron | Các audit nguồn riêng trong repository | Context/annotation hoặc ứng viên validation. Không nằm trong core v3 Zhang/UniProt; không tự gọi là external validation đã chạy. |

**PSI và ΔPSI.** Sau chuẩn hóa count giữa bin theo quy trình nguồn, PSI là trung bình có trọng số chỉ số bin 1…6; PSI cao tương ứng reporter ổn định hơn trong assay. Đối với saturation, mỗi nửa a/b có WT nội tại là trung vị các ô đồng nghĩa hợp lệ; mỗi ô có `dpsi_a/b = psi_mut_a/b − psi_wt_a/b`; nhãn là trung bình hai ΔPSI. Scanning dùng `_mut0` của đúng replicate. `psi-wt.tsv` là condition BAG6 WT riêng, không phải mốc thay thế cho a/b hay rep1/rep2. `build_psi.py` và [psi-build.json](../full-data-audit/psi-build.json) lưu lỗi header/chuẩn hóa và tái lập nguồn.

Một **protein** có thể cho nhiều **peptide**. Một peptide 28 residue có tối đa 28×19=532 **mutation cell** thay thế không đồng nghĩa; mỗi cell có thể có nhiều **observation** replicate/half. Số observation không phải số cell độc lập. WT→WT dùng cho reference/QC, không tính như mutation dự đoán. Đơn vị split/CI là nhóm protein, metric có thể tính tại cell rồi macro theo peptide.

## Phiên bản dữ liệu và vì sao số đếm thay đổi

| View/phiên bản | Peptide | Cell | Group | Ý nghĩa |
|---|---:|---:|---:|---|
| Saturation thô trước QC | 248 | Không suy số từ 532×248 | Chưa áp dụng | [sat-filter-dropoff.json](../next-steps-plan-2026-10-22/sat-filter-dropoff.json) lưu drop-off; 13 peptide bị loại kỹ thuật, không được “bù” nhãn. |
| H-sat WT PSI≤3 | 91 | 47.847 | 89 legacy cov80 | G2 test; [results.json](../g2-saturation-2026-10-18/results.json). |
| Legacy pool≤4 | 176 | 92.337 | 172 legacy cov80 | 85 peptide/44.490 cell mới; chỉ thêm vào outer-train cho P0/R6 sau loại cụm test. [ladder.json](../residue-task-derisk-2026-10-15/ladder.json). |
| Legacy no PSI limit | 235 | 122.412 | 227 theo legacy fallback | Cùng nhãn nhưng coverage mapping cũ không đầy đủ; không coi 227 singleton/fallback group là chứng cứ đã map toàn bộ. [ladder.json](../residue-task-derisk-2026-10-15/ladder.json). |
| Pool R3/full proteome trước union | 235 | Không phải bảng cell test R3 | 222 | Nhóm cov80 full proteome; task là domain classification. [R3 results](../r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json). |
| W-v3 full PSI | 235 | 122.412 | 221 sau union | [dataset-build.json](../kaggle-roadmap-2026-10-31/dataset-build.json): full proteome cov80, local cov50 hits, exact sequence union. Group count mới không phải nhãn mới. |
| Scanning H-scan≤3 | 2.994 | 83.446 | 1.985 legacy cov80 | Coverage≥21 vị trí/peptide; R/A/S substitution design, không phải 19 loại thay tại mỗi vị trí. [model.json](../residue-task-derisk-2026-10-15/model.json). |
| Scanning≤4 trong scan–sat merge | 4.809 | 133.960 | 2.909 | Bộ lọc/mapping lịch sử của merge; [results.json](../scan-sat-merge-2026-10-23/results.json) `meta.scan.thr4.0`. |
| Scanning≤4 trong R6 | 4.802 | 133.764 | 2.902 | Bộ lọc sequence/map R6 chặt khác merge; không sửa hai số cho khớp bằng tay. [posthoc-r6.json](../r6-ladder-scan-2026-10-23/posthoc-r6.json). |
| Scanning v3 union replicate | 8.181 qua partition | 224.470 | Xem split/manifest | Partition count là peptide: 1.278 `sat_overlap`, 5.489 `scan_dev`, 1.414 `scan_T`; không phải số mutation cell. [dataset-build.json](../kaggle-roadmap-2026-10-31/dataset-build.json). |

W-v3 có strata ≤3:91, (3,4]:85, (4,5]:36, >5:23 peptide. Như vậy full-range đổi cả lượng nhãn và phân phối tác động/PSI. Tỷ lệ event dương và khả năng phân biệt event thay đổi theo vùng; không suy D tốt hơn B trung bình nghĩa D tốt hơn ở mọi stratum. Từ thang PSI bounded [1,6], `ΔPSI` nằm trong [−5,+5], với biên khả dĩ phụ thuộc WT PSI: WT cao ít headroom tăng nhưng có nhiều headroom giảm. Đây là ràng buộc phép đo, không phải cơ chế mutation đã xác nhận.

## QC có trong mã và các quyết định có ảnh hưởng

1. **Read và count.** Loader chỉ lấy PSI đủ tổng reads≥10. Đây là ngưỡng kỹ thuật cố định của pipeline, không bảo đảm sai số đo giống nhau cho mọi cell; replicate disagreement không phải phương sai đã biết. Audit read-depth lịch sử nằm ở [read-depth-sweep.json](../full-data-audit/read-depth-sweep.json).
2. **Saturation reference.** `residue_data.build_saturation` yêu cầu ít nhất 10 ô đồng nghĩa mỗi nửa; kiểm sequence từ source với canonical tile; giữ ô không đồng nghĩa có mặt cả a và b, vị trí/residue hợp lệ. Không nội suy cell thiếu. Bỏ ngưỡng PSI ở v3 **không bỏ QC**.
3. **Scanning reference và coverage.** `build_scanning` yêu cầu `_mut0`, chuỗi source hợp lệ và ≥21 vị trí đo; rep1/rep2 xây riêng. Union v3 giữ mask availability; chỉ `dpsi_rep12_mean` khi cả hai có đo. T dùng target rep1 đã ghi; không trộn với BAG6 WT.
4. **Proteome mapping.** Builder v3 loại 17 scanning peptide không map được vào reference, thay vì giả singleton. 45 saturation peptide thiếu nhóm legacy map được qua bảng toàn proteome. Việc đổi grouping có thể đổi hàng train/test dù nhãn không đổi.
5. **Tổ hợp homology.** Builder dùng cov80 toàn proteome và union các protein hit identity≥30%, alignment≥50 aa theo search cov50 hai chiều; sau đó union sequence trùng trên saturation+scanning. [dataset-build.json](../kaggle-roadmap-2026-10-31/dataset-build.json) ghi 12.863 hit edges và 0 edge exact-sequence bổ sung, còn 221 nhóm saturation. Không dùng “zero cross-group exact hit” để khẳng định hết mọi motif leakage.
6. **Splitting.** Five outer W folds group-disjoint; phân bổ greedy dựa peptide-stratum metadata, không dựa hiệu năng model. Inner groups theo seed chung cho các arm. Scanning được khóa theo nhóm thành overlap/dev/T trước supervised use; dev không được chứa outer-test/validation groups trong các fit liên quan.
7. **Biến đổi và tuning.** v3 fit scaling/PCA chỉ trên train cho lựa chọn inner, rồi refit outer-train hợp lệ. Historical R6 Ridge refit train∪validation còn neural head không refit như v3; cùng fold không đồng nghĩa cùng ngân sách dữ liệu cuối.
8. **Sequence-only input.** WT sequence, vị trí và mutant AA là input. WT PSI dùng tạo nhãn, lọc train B, stratify, domain-gate task và phân tích. PSI mutant, ΔPSI, reads, group/fold/stratum không là feature main model. Domain gate R3 dùng measured/predicted screen PSI ở task riêng, không biến thành main mutation feature ngầm.

Nguồn mã trực tiếp: [residue_data.py](../residue-task-derisk-2026-10-15/residue_data.py), [build_dataset.py](../kaggle-roadmap-2026-10-31/build_dataset.py), [DATASET.md](../kaggle-roadmap-2026-10-31/DATASET.md), [EXECUTION-PROTOCOL.md](../kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md). Phần “đặc tả 31/10 chưa dựng” dưới DATASET là lịch sử, không lấn át `dataset-build.json` đã PASS 01/11.

## So sánh nào trả lời được câu hỏi nào?

| Câu hỏi | Phép so hợp lệ hiện có | Kết luận được phép và giới hạn |
|---|---|---|
| Mở WT PSI range có giúp? | P0 cùng H-sat test; v3 B/D/E cùng W folds, inner/test full PSI | P0 chỉ≤3 test; v3 mới đánh giá full-range. Không gộp thành một hiệu ứng đơn vì đổi grouping và metric. |
| Scanning có ích? | Merge/R6 trên H-sat; v3 transfer/sat-only trên W | Hiệu quả phụ thuộc representation, target replicate và learner. Scanning chỉ R/A/S, không cung cấp coverage đều 19 mutant. |
| PLM có ích? | R2 PCA/Ridge; R6 ESM-vs-onehot cùng head; v3 đối chứng pointwise/CNN | R2 không đủ bằng chứng không phủ định R6 hay v3 khác recipe; không quy chênh lệch tất cả cho PLM nếu auxiliary inputs/training khác. |
| mCNN hơn CNN? | R6 S6; v3 cùng runtime/fold/representation | Chênh nhỏ và CI chứa 0 không xác nhận ưu thế; cũng không chứng minh tương đương trừ tiêu chí equivalence riêng đã định. |
| Fine-tuning tốt hơn frozen? | Local v3 LoRA-vs-frozen matched | Bằng chứng về rank-8 LoRA q/v ESM35 theo schedule đã chạy; không có arm full fine-tuning, không gọi nó đã được kiểm. |
| Generalization tới nguồn mới? | T-v3 W5-D | T cùng lab, cùng nguồn đã thăm dò, rep1 R/A/S; không phải LoRA/external cohort. Homology grouping giảm risk trong tiêu chí đã audit, không xóa mọi dependence. |

## Kiểm kê vấn đề phương pháp và thông tin còn thiếu

Các từ trạng thái dùng đúng bảy loại của yêu cầu: **chưa tìm thấy**, **không thể truy cập**, **chưa được thực hiện**, **chưa hoàn thành**, **không đầy đủ**, **mâu thuẫn**, **chưa được kiểm chứng**. Không gán “chưa thực hiện” chỉ do thiếu một file.

| Nội dung còn thiếu/vấn đề | Trạng thái | Ảnh hưởng | Nguồn đã kiểm | Cách bổ sung | Ưu tiên |
|---|---|---|---|---|---|
| External cohort hợp lệ cho candidate v3 | Chưa hoàn thành | Chưa kết luận qua nguồn/lab khác | Koren audit; v3 stage08 pending; local report | Audit quyền/schema/endpoint, pin cohort và recipe, rồi đánh giá riêng | Cao |
| Test T cho LoRA | Chưa được thực hiện trong campaign đã rà | Không chuyển lợi thế W thành kết luận transfer LoRA | local plan/analysis, W5-only locked-transfer | Chốt recipe và protocol mới trước evaluation; T đã xem nên không gọi untouched confirmation | Cao |
| Full fine-tuning đối chứng | Chưa tìm thấy trong campaign đã rà | Chỉ trả lời LoRA-vs-frozen, không trả lời mọi fine-tuning | model registry, plan, matched adaptation code | Chỉ đề xuất nếu cần và có budget; protocol rõ, không bắt buộc cho tiến độ | Trung bình |
| Structural/3Di bundle đủ mapping | Chưa hoàn thành | SaProt/cấu trúc chưa có benchmark hợp lệ | v3 stage09 pending; 8 PDB MaveDB cũ | Mapping chain/residue/pLDDT/3Di có provenance; kiểm coverage trước model | Trung bình |
| Final candidate refit/calibrator/export | Chưa hoàn thành | Calibration CV chưa dùng để thay serving baseline | collect/calibrate outputs; baseline model card | Chốt model, refit và calibrator, export/version/hash, parity inference | Cao |
| Fold/protein/mutation error analysis ngoài bảng hiện có | Không đầy đủ | Có thể bỏ sót fold/nhóm rất kém | strata/per-peptide output, các metric eligibility | Báo cell/peptide/group support, residual tails và uncertainty, giữ các failure | Trung bình |
| Tác động tới thời gian/chi phí wet lab | Chưa được kiểm chứng | Không được khẳng định tiết kiệm định lượng hoặc utility thực tế | report/source papers, ranking utility offline | Prospective selection study với ngân sách và control baseline | Cao nếu đưa claim ứng dụng |
| Mọi latent biological dependence đã loại | Chưa được kiểm chứng | CI vẫn theo heuristic grouping, không chứng minh mọi sequence độc lập | clustering rules, cross-split audit | Sensitivity theo local homology/motif/family; thêm cohort phù hợp | Trung bình |
| R6 README nhấn “điều mới duy nhất” W5 nhưng JSON nhận họ G | Mâu thuẫn trong tổng kết | Có thể bỏ kết quả dương scanning hoặc sai primary | R6 README mở đầu và results.contrasts | Báo primary riêng và hai contrast họ A/G; giữ hồ sơ lịch sử, không đổi phán quyết P | Trung bình |
| Replicate scanning được xem là genotype hoàn toàn tương đương | Chưa được kiểm chứng | Mean rep1/rep2 có thể trộn thiết kế nguồn chưa rõ | observation `assay_id`/`condition_id`, audit nguồn | Xác nhận mô tả condition từ nguồn; giữ rep1 và pair-mean thành arm riêng | Trung bình |
| Runtime hoặc phiên chạy phát sinh sau snapshot local | Chưa được kiểm chứng | Việc đọc artifact không xác nhận trạng thái Windows worker/sessions ngoài snapshot | state/log/manifest và local-audit | Kiểm trên máy thực thi hoặc đồng bộ snapshot nếu có run mới; không giả Kaggle là local mới | Thấp cho báo cáo mốc này |

Không có yêu cầu dừng toàn bộ báo cáo vì các thiếu hụt trên. Nội dung có bằng chứng vẫn được cập nhật; các endpoint chưa xác nhận giữ ở trạng thái pending/hypothesis.
