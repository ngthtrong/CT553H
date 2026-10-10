# Quyết định và phạm vi đề tài: đặc hiệu E3–degron

> **Đề tài đã chốt ngày 11/10/2026** theo quyết định của sinh viên. Slug: `degron-e3-specificity`. Chưa có phê duyệt chính thức của GVHD — cần báo cáo ở buổi tuần 6.

## 1. Tên đề tài

**Dự đoán đặc hiệu E3–degron ở mức residue bằng học đa thể hiện có điều kiện và cổng phơi lộ cấu trúc.**

- Trang trình bày (bố cục 6 mục, mở bằng `file://`): [presentation.html](presentation.html)
- Báo cáo kiểm chứng chi tiết: [../../../common/deep-research/reports/degron-topic-report/index.html](../../../common/deep-research/reports/degron-topic-report/index.html)
- Script và kết quả audit tái tạo được: [../../../common/deep-research/research_notes/degron/](../../../common/deep-research/research_notes/degron/)

## 2. Vì sao chọn đề tài này

Quyết định dựa trên các phép đo tự thực hiện ngày 11/10/2026, không dựa trên số dẫn lại từ bài báo:

1. **Mô hình tốt nhất hiện có không đọc được vị trí.** Tự dựng lại PAP (bài *Science Advances* 2026) bằng numpy từ trọng số công bố, rồi đảo ngẫu nhiên thứ tự acid amin trong từng tile: điểm **không đổi**, Pearson(gốc, đảo) = **1,000000**. Mô hình đó bất biến hoán vị — không biểu diễn được motif nào — mà vẫn đạt Pearson 0,869.
2. **Thang điểm khối đã bão hòa.** Tác giả có sẵn bản `cnn2w7` (cửa sổ 7, bắt được motif) trong repo; tự chạy lại: nó chỉ hơn **+0,0032 Pearson**. Nên "thêm năng lực bắt motif" không còn là trục đóng góp.
3. **Nhãn cho phần còn thiếu đã tồn tại từ 2023 mà chưa ai dùng.** Sàng lọc Zhang 2023 có **15 adaptor CRL cộng BAG6** gán bằng CRISPR, **219 footprint** đột biến bão hòa, và residue quan trọng cho hơn 5.000 degron. Không mô hình nào mô hình hóa nhãn này.
4. **Cả ba bộ dữ liệu đều tải được và đã tự đếm** (xem mục 4).

## 3. Phạm vi

**Trong phạm vi:** protein người, trọng tâm bào tương; 16 E3 có nhãn CRISPR; dự đoán ở mức đoạn peptide và residue; kiểm chứng trên dữ liệu đột biến thực nghiệm; một ứng dụng web.

**Ngoài phạm vi, phải nói rõ trong luận văn:**

- Không dự đoán protein có thực sự bị phân hủy nhanh trong một tế bào cụ thể (còn phụ thuộc E3 nào được biểu hiện, chaperone, định vị dưới tế bào).
- Không phủ hơn 600 E3 của người, chỉ 16 cái có nhãn.
- Không thay thế mô hình dự đoán độc tính biến thể; chỉ bổ sung cơ chế.

## 4. Ba bộ dữ liệu, đã tải và tự đếm

| | Bộ 1 — bản đồ bào tương | Bộ 2 — GPS-peptidome | Bộ 3 — biến thể protein nguyên vẹn |
|---|---|---|---|
| Nguồn | Voutsinos 2026, *Sci Adv* | Zhang 2023, *Mol Cell*, GEO **GSE240610** | MaveDB (API) |
| Vai trò | Huấn luyện chính | **Nhãn đặc hiệu E3 + test khác assay** | Test trên protein nguyên vẹn |
| Số phép đo | 212.658 đoạn | 475.507 đoạn × 3 lần đo | **69.209 biến thể duy nhất** |
| Độ dài đoạn | 30 aa, chồng 15 | 28 aa, bước 23 | — |
| Thang đo | Điểm liên tục 0–1 | PSI 1–6, Degron Index | Độ dồi dào protein |
| Nhãn E3 | Không | **15 adaptor CRL + BAG6** | Không |
| Dữ liệu theo residue | Không | **219 footprint; >5.000 degron** | Có (biến thể điểm) |
| Giấy phép | MIT | GEO công khai | CC0 |

Tập kiểm tra dùng: **428 gene hiệu dụng / 15.820 tile**, tính từ dữ liệu — **không** dùng danh sách 527 gene công bố, vì 96 gene trong đó thực ra nằm hết ở tập huấn luyện.

## 5. Kiến trúc đề xuất: CMIL-E3

GVHD **kỳ vọng một kiến trúc chưa ai dùng** (thông tin ngày 11/10/2026). Kiến trúc đề xuất có sáu thành phần, mỗi thành phần gắn với một phép đo cụ thể:

| # | Thành phần | Phép đo buộc phải có nó |
|---|---|---|
| 1 | Mỗi vị trí sinh một cửa sổ ứng viên motif; peptide là một "túi" cửa sổ | Mô hình hiện có bất biến hoán vị (Pearson gốc–đảo = 1,000000) |
| 2 | Embedding PLM **mức residue**, không gộp trước | Mọi mô hình đã công bố đều gộp trung bình hoặc dùng thành phần |
| 3 | **Điều kiện theo E3**, vector sinh từ trình tự miền nhận cơ chất của chính E3, điều biến kiểu FiLM | 16 E3 có nhãn CRISPR từ 2023 mà chưa ai dùng |
| 4 | **Attention có cổng** trên các thể hiện, thay global average pooling | Nhãn ở mức peptide, cơ chế ở mức cửa sổ con |
| 5 | **Cổng phơi lộ**: rASA và pLDDT nhân vào logit attention | Tác giả đo điểm chỉ tương quan độ dồi dào ở rASA > 0,7, nhưng chỉ dùng cấu trúc để phân tích sau |
| 6 | Hai đầu ra, huấn luyện đa nhiệm: điểm khối (phụ trợ) và đặc hiệu E3 (mục tiêu) | Nhãn B ít, nhãn A nhiều nhưng đã bão hòa |

**Điểm mới cốt lõi:** cổng phơi lộ đặt ở chỗ **gộp**, không phải đầu vào. Khi dự đoán trên peptide tách rời thì đặt cổng "phơi lộ hoàn toàn"; khi dự đoán trên protein nguyên vẹn thì đặt rASA thật. Cùng một mô hình giải thích cả hai chế độ, tức khoảng cách tile-so-với-protein trở thành một tham số của mô hình.

## 6. Thước đo, và điều phải thống nhất với GVHD trước khi bắt đầu

Thước đo chính **không phải** Pearson trên thang điểm khối. Ba bậc:

1. **Trong cùng sàng lọc**, holdout kiểm soát đồng dạng 428 gene. Để chứng minh chạy lại được baseline (đã làm: 0,8690), **không phải** để đặt đóng góp.
2. **Chuyển giữa hai sàng lọc khác assay.** Chưa ai đo, dữ liệu đã có.
3. **Nhiệm vụ cần motif — thước đo chính.** 219 footprint, residue quan trọng, gán adaptor CRL.

> **Phải nói với GVHD ngay:** phép đo cho thấy thay gộp trung bình bằng gộp max làm hiệu năng sụt **0,824 → 0,344**, entropy theo vị trí 3,294 trên tối đa 3,401 — tín hiệu thang điểm khối **dàn đều, không khu trú**. Nên **CMIL-E3 gần như chắc chắn không thắng trên thang điểm khối**. Nếu GVHD yêu cầu thắng trên thang đó thì phải thiết kế lại đề tài.

## 7. Ba cổng chặn chưa qua

Nếu một trong ba không qua, thiết kế phải đổi:

1. **Đọc toàn văn bài degron transcription factor** (Larsen, Voutsinos và cộng sự, tiền ấn 05/2025, 1.626 TF, dùng PAP cùng ESM-1b). Nếu họ đã làm phần đặc hiệu E3 thì đề tài phải đổi trục. Hiện chỉ đọc được tóm tắt; `biorxiv.org` bị chặn với WebFetch.
2. **Mở Table S3, S4, S6, S7 của Zhang 2023** và đếm nhãn E3 dùng được. Nếu quá ít thì thành phần 3 của kiến trúc phải bỏ.
3. **Tra hệ thống tính mới của kiến trúc.** Tuyên bố "không mô hình degron nào dùng attention đa thể hiện" hiện dựa trên đọc mã ba mô hình cộng vài lượt tìm web — chưa tra danh sách trích dẫn, và nội bộ MetaDegron chưa rõ.

## 8. Quy ước ngôn từ riêng của đề tài

- **Không dùng chữ "đầu tiên"** cho bất kỳ phần nào. Đã có ít nhất 5 công cụ dự đoán degron trước, và MetaDegron dùng PLM từ 2024.
- Phân biệt rõ **"thang điểm khối"** (bulk score, đã bão hòa) và **"đặc hiệu E3"** (bài toán của đề tài). Không trộn hai thứ thành một con số.
- Khi nói về kiểm soát đồng dạng của tác giả: nói **"tốt nhưng không hoàn hảo"** — tự đo được 14/428 gene (3,3%) vẫn có họ hàng trong train ở identity ≥30%, và một gene trùng 100% trên 77 residue với TRIM5.
- Nhận xét mã nguồn PAP luôn kèm: **script công bố trỏ vào cột DNA thay vì cột acid amin**, nên không chạy lại mã của họ mà tự dựng pipeline.
- Gọi 219 footprint là **"chuẩn thực nghiệm theo residue"**, không gọi là "ground truth tuyệt đối".

## 9. Tài nguyên tính toán — đã đo

Máy: AMD Ryzen 5 5500U, 12 luồng, 7 GB RAM, không GPU.

| | Thông lượng | Toàn bộ 212.658 tile | Cache mức residue |
|---|---|---|---|
| ESM-2 **35M** | 64,6 tile/s | **~55 phút** | 12,2 GB fp32 |
| ESM-2 **650M** | 5,3 tile/s | **~11 giờ** | **32,7 GB fp32** — vượt RAM |

Kết luận: dùng **35M để lặp thí nghiệm**, 650M chỉ một lượt cuối chạy qua đêm theo luồng. Kiến trúc cần embedding mức residue nên **đây là lý do cụ thể để xin GPU**.
