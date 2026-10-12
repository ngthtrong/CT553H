# Nhật ký đề tài `tme-senescence-scrnaseq`

> Mới nhất ở trên. Các mục dưới đây được tách nguyên văn từ nhật ký chung cũ (`docs/common/work-log.md`) ngày 12/10/2026. Câu chữ "chốt/quyết định" bên dưới là lịch sử; trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../../DECISIONS.md).

---

## 07/10/2026 (tối, muộn) — chạy SenMayo trên GSE103322: **dừng hướng 2**

- Áp đúng [bốn ngưỡng đặt trước](../../surveys/advisor-4-directions-analysis.md) lên số thật của **GSE103322** (5.902 tế bào, 17 bệnh nhân): `n_patients` 17 **đạt**; `patients_with_ge20_positives` **7/8 KHÔNG đạt**; `concentration_ratio` 1,85 (dải phải cân mẫu); `signature_coverage` 0,97 **đạt**. Phải đạt cả bốn → **dừng hướng 2**. Không nới ngưỡng.
- **Phát hiện nặng hơn, độc lập với ngưỡng:** điểm SenMayo chủ yếu theo **loại tế bào**, không theo senescence — **70% tế bào dương là fibroblast**, tế bào **T và B không có tế bào dương nào**. Chấm ngưỡng riêng theo loại tế bào thì fibroblast chỉ còn **1 bệnh nhân** có ≥20 dương, và tế bào ung thư có 3 bệnh nhân với `concentration_ratio = 3,35` (**vượt ngưỡng dừng 3,0**). Đây là lỗi SenSeqNet lặp lại ở mức loại tế bào thay vì mức họ protein. **GSE131907 không chạy** — dataset lớn hơn không sửa được chuyện này.
- **Khuyến nghị mới: chuyển sang ứng viên B** (site phospho theo nhóm kinase) — ứng viên duy nhất có benchmark non-homologous do dbPTM công bố, và rơi đúng khuôn T1. A là lựa chọn hai, nhớ cổng mở về tập test độc lập.
- **Đính chính trong ngày:** bản 06/10 viết "A và B đều đã qua cổng dữ liệu" — **sai với A**; A chỉ có holdout 10% trên cùng một microarray. Đã sửa ở mục 0, 2.6, 6, 7.2.
- **Dùng được cho tuần 6:** kết quả âm này có số, trên dữ liệu công khai, và trả lời đúng câu "vấn đề tồn đọng là gì". Nói đúng cách: đây là lý do không chọn hướng 2, không phải một đóng góp đã hoàn thành.
- **Còn dở:** PR #3 đã merge nhưng **chỉ chứa 2 commit đầu**; bốn commit sau nằm ở PR mới. Code chạy thật ở PR #4 (nhánh `claude/project-thread-l271f1`).

---

## 07/10/2026 (khuya) — `tme-senescence-scrnaseq`: chạy SenMayo trên GSE103322 thật, trượt 1/4 ngưỡng và điểm đi theo loại tế bào

- Sinh viên thêm domain NCBI vào danh sách cho phép; GEO trả 200. Đã tải **GSE103322** (HNSCC, Smart-seq2, 5.902 tế bào), chuyển sang h5ad bằng [convert_gse103322.py](code/preprocessing/convert_gse103322.py), chấm SenMayo (117 gene, phủ 113). Kết quả và giả định: [README của preprocessing](code/preprocessing/README.md).
- **Bốn ngưỡng đặt trước:** 17 bệnh nhân (đạt), **7 bệnh nhân có ≥ 20 tế bào dương (trượt, cần ≥ 8)**, `concentration_ratio` 1,848 (đạt kèm trọng số), độ phủ 0,966 (đạt).
- **Phát hiện quan trọng hơn bốn ngưỡng:** 70% tế bào dương là fibroblast, T/B cell bằng 0, nên chênh lệch giữa bệnh nhân chủ yếu là chênh lệch thành phần loại tế bào. Đặt lại ngưỡng trong từng loại: fibroblast chỉ 1 bệnh nhân có ≥ 20 tế bào dương, tế bào ung thư 3 bệnh nhân và `concentration_ratio` 3,35. Nhãn proxy từ điểm SenMayo trên dataset này về cơ bản là nhãn loại tế bào.
- Mã bệnh nhân suy từ tên tế bào: ra 17, không phải 18 như GEO ghi; 109 tế bào ở plate trộn bị loại khỏi thống kê theo bệnh nhân.
- Script được sửa thêm: `--skip-norm` cho dữ liệu đã log hóa, loại tế bào không rõ bệnh nhân, thống kê theo loại tế bào, `concentration_ratio_per_patient`. Thêm `within_celltype.py`.
- **Còn dở:** chưa cập nhật mục 7 của [phân tích 4 hướng](../../surveys/advisor-4-directions-analysis.md) (thread phân tích sở hữu file đó). GSE131907 chưa tải.

---

## 07/10/2026 (tối) — thử tải scRNA-seq khối u để chấm SenMayo: bị chặn mạng, đã viết sẵn script

- **Không tải được dataset nào.** Mạng của môi trường cloud chặn gần hết host dữ liệu, đã thử và ghi đúng mã trả về: `ftp.ncbi.nlm.nih.gov` (GEO), `zenodo.org`, `cellxgene`, `huggingface.co`, `figshare`, `cells.ucsc.edu`, `ha-dkfz.github.io` — **403 ở bước CONNECT**. Chỉ `raw.githubusercontent.com` và PyPI đi được. Đã ghi vào [resources.md](../../../resources/README.md).
- **Đã làm được phần không cần dataset:** cài scanpy 1.12.4; lấy danh sách gene SenMayo từ bộ chữ ký HA-DKFZ; viết [senmayo_score.py](code/preprocessing/senmayo_score.py) đếm tế bào/bệnh nhân, chấm điểm SenMayo và báo **mức dồn tế bào dương theo bệnh nhân**; kiểm trên ma trận tổng hợp 3.000 tế bào (chạy đúng, `top1_patient_share_of_positives = 0,7667` khớp cấu trúc đã cấy). Đây là phép kiểm phần mềm, không phải kết quả sinh học.
- **Cảnh báo phải mang theo:** danh sách lấy được có **117 gene, không phải 125** như bài gốc công bố; **chưa xác định được 8 gene chênh lệch** vì phụ lục là xlsx không lấy được. Không gọi file này là "SenMayo 125 gene" trong tài liệu gửi GVHD.
- Đã thêm slug `tme-senescence-scrnaseq` vào [danh sách đề tài](../../../topics/README.md) ở trạng thái đang khảo sát, chỉ có code, chưa có tài liệu đề tài riêng.
- **Còn dở:** chờ sinh viên chọn một trong hai đường — cho phép host GEO trong cài đặt môi trường cloud, hoặc tải trên máy của sinh viên. Script chạy được ngay khi có file.
