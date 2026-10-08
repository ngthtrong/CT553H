# Deep-PLA phủ những HDAC nào — đã đọc toàn văn, và câu trả lời là xấu

**Ngày:** 08/10/2026. **Nguồn:** toàn văn bbz107 (PDF do sinh viên cung cấp) + web server chính thức `http://deeppla.cancerbio.info`. Đây là việc chặn số 1 ở mục 11.2 của [báo cáo khảo sát sâu](../../reports/sirtuin-substrate-deep-research.md).

## 1. Trả lời dứt khoát

Web server chính thức của Deep-PLA ghi nguyên văn `[tác giả báo cáo]`:

> "Deep-PLA is a web server developed for understanding the reversible enzyme-specific lysine acetylation regulation for histone acetyltransferases (HATs) including CREBBP, EP300, HAT1, KAT2A, KAT2B, KAT5 and KAT8, and deacetylases (HDACs) including **HDAC1, HDAC2, HDAC3, HDAC6, SIRT1, SIRT2, SIRT3, SIRT6, and SIRT7**."

Vậy **9 HDAC = 4 HDAC cổ điển + 5 sirtuin**. Thiếu đúng **SIRT4 và SIRT5**.

**Hệ quả:** câu "chưa ai dự đoán vị trí deacetyl hóa đặc hiệu isoform sirtuin ở mức residue" **sai từ năm 2020**. Và điều cay đắng hơn: năm isoform Deep-PLA có đúng là bao gồm cả **SIRT1, SIRT2, SIRT3** — ba isoform duy nhất mà [06-seven-isoform-feasibility.md](06-seven-isoform-feasibility.md) kết luận là còn khả thi về sinh học. Deep-PLA **không** phủ SIRT4 và SIRT5, tức là nó bỏ đúng hai isoform mà sinh học nói không nên làm. Chồng lấn nằm trọn ở phần đáng làm.

Thêm một tiền lệ còn sớm hơn, do chính Deep-PLA dẫn `[tác giả báo cáo]`: "Later, they added **class I HDAC and SIRT7 substrate predictive functions into ASEB**" (tài liệu [30, 31] của bbz107). Tức **dự đoán cơ chất đặc hiệu SIRT7 đã có từ thời ASEB**, trước Deep-PLA.

## 2. Nhưng dữ liệu của họ rất nhỏ — đây là chỗ duy nhất còn khác biệt

Table 1 của bbz107, cột Human `[tác giả báo cáo]`:

| Enzyme | Protein | Vị trí (human) | | Enzyme | Protein | Vị trí (human) |
|---|---|---|---|---|---|---|
| HDAC1 | 25 | 47 | | **SIRT1** | 76 | **184** |
| HDAC2 | 14 | 28 | | **SIRT2** | 27 | **52** |
| HDAC3 | 18 | 37 | | **SIRT3** | 20 | **30** |
| HDAC6 | 14 | 17 | | **SIRT6** | 5 | **10** |
| HDACs (gộp họ) | 54 | 94 | | **SIRT7** | 6 | **12** |

Tổng cho năm sirtuin: **288 vị trí trên 134 protein**. Toàn bộ tập huấn luyện HDAC là **317 vị trí người**; tập kiểm tra là **84 vị trí phi-người** `[tác giả báo cáo]`.

So với mảng Rauh: **6.801 vị trí × 7 isoform**. Chênh khoảng **24 lần** chỉ riêng số vị trí, và Deep-PLA không có SIRT4/SIRT5 nào.

Quan trọng hơn số lượng là **loại nhãn**: nhãn của Deep-PLA được **text-mining từ PubMed** — tức là các cơ chất *đã được báo cáo trong tài liệu*, phần lớn là bằng chứng **trong tế bào hoặc trên protein nguyên**. Nhãn của mảng Rauh là **hoạt tính trên peptide tự do in vitro**, có hệ thống và không thiên lệch theo mức độ nổi tiếng của protein. Hai bộ nhãn **đo hai thứ khác nhau**, và đó là điều kiện tốt nhất còn lại cho đề tài.

## 3. Deep-PLA không báo cáo những gì

- **Không có chỉ số cho từng sirtuin ngoài SIRT1.** Bài chỉ báo "The AUC scores of SIRT1 and HDACs were **0,8283** and **0,8921**" `[tác giả báo cáo]`. Không có AUC riêng cho SIRT2, SIRT3, SIRT6, SIRT7 trong phần thân bài.
- **Dữ liệu nhỏ tới mức không chạy nổi 10-fold:** "Due to the data limitations, only **5-fold** cross-validations were carried out for HAT1, KAT8, **SIRT3, SIRT6, SIRT7** and HDAC6" `[tác giả báo cáo]`. SIRT6 có 10 vị trí, SIRT7 có 12 — ở cỡ đó, AUC gần như không phát biểu được gì.
- **Chỉ số dùng là Sn, Sp, Pr và AUC** (công thức 1–3 trong Methods). **Không có MCC, không có AUPRC** — đúng hai chỉ số mà [04-evaluation-design.md](04-evaluation-design.md) kết luận là bắt buộc khi mất cân bằng nặng.
- **Không có đánh giá trong tế bào** theo kiểu đo lại trên acetylome KO/KD.
- **Có một điểm họ làm tốt, phải ghi nhận:** tập kiểm tra là **vị trí trên protein phi-người**, nên có một dạng kiểm soát đồng dạng/độc lập nguồn thật, không phải chia ngẫu nhiên. Đừng nói Deep-PLA không kiểm soát rò rỉ.
- Một chi tiết dùng được: họ đo và thấy **AUC không đổi đáng kể khi cửa sổ vượt ±12 residue** (Figure S3, Table S3) trên EP300 và SIRT1 `[tác giả báo cáo]` — đây là căn cứ có nguồn cho việc chọn cửa sổ 13-mer, thay vì chọn tùy ý.

## 4. Hệ quả cho đề tài: trục tính mới sinh học coi như hết

Bảng tiền lệ cho riêng "dự đoán cơ chất/vị trí deacetyl hóa đặc hiệu isoform sirtuin":

| Công trình | Năm | Mức | Isoform phủ | Nhãn | Số vị trí |
|---|---|---|---|---|---|
| ASEB (mở rộng) | ~2012–2015 | residue | class I HDAC + **SIRT7** | curate tài liệu | không rõ `[chưa kiểm]` |
| **Deep-PLA** | 2020 | **residue** | **SIRT1, 2, 3, 6, 7** | text-mining PubMed | 288 (người) |
| DeepSIRT | 2021 | protein | SIRT1–7 | danh sách target | không rõ `[chưa kiểm]` |
| Ridgeway | 2025 | residue | SIRT1–7 | mảng Rauh, nhị phân | 6.801 × 7 |

Bốn công trình, ba mức, và **ba trong bốn là mức residue**. Không còn cách nào đóng khung "bài toán sinh học mới". Mọi câu có chữ "đầu tiên" về mặt sinh học đều sẽ bị bắt lỗi, và Deep-PLA lại nằm ở một tạp chí (Briefings in Bioinformatics) mà GVHD chắc chắn biết.

**Nhưng phán quyết THU HẸP của báo cáo không đổi — nó còn được củng cố.** Lý do: đóng góp mà báo cáo giữ lại không phải "một bộ dự đoán mới", mà là **phép đo xem các bộ dự đoán đã công bố có đúng trong tế bào hay không, với nhãn âm thật và chỉ số đúng**. Trước khi đọc Deep-PLA, phép đo đó có **một** đối tượng (Ridgeway 2025). Bây giờ nó có **ba**: Deep-PLA 2020, DeepSIRT 2021, Ridgeway 2025 — ba bộ dự đoán, ba loại nhãn huấn luyện khác nhau (tài liệu curate / danh sách target / mảng peptide), chưa ai trong số đó báo cáo MCC hay AUPRC, và chưa ai đo trên acetylome KO/KD có nhãn âm.

Đề tài vì vậy nên chuyển hẳn thành **một benchmark**: *ba bộ dự đoán cơ chất sirtuin đã công bố, đo lại trên cùng một tập đánh giá trong tế bào có nhãn âm, với chỉ số chịu được mất cân bằng, và có kiểm soát rò rỉ ở mức protein và đồng dạng.* Đây là dạng đóng góp mà cộng đồng kinase đã làm (benchmarKIN 2025) nhưng cộng đồng sirtuin thì chưa `[chưa tìm thấy, không kết luận là chưa từng có]`.

**Một lợi ích cụ thể, đo được ngay:** 288 vị trí curate của Deep-PLA là nhãn dương **độc lập với mảng Rauh**. Việc làm được trong tuần 1: đếm xem bao nhiêu trong 288 vị trí đó nằm trong 6.801 vị trí mảng, và mảng gán chúng dương hay âm. Nếu mảng gán phần lớn chúng là **âm**, đó là một phép đo thứ hai, độc lập với phép đo Sol 2012, cho cùng kết luận "nhãn in vitro không chuyển được" — và nó mạnh hơn, vì 288 vị trí đó là cơ chất đã được xác nhận bằng thực nghiệm trên protein nguyên.

## 5. Câu phải chuẩn bị cho GVHD

> *"Deep-PLA 2020 đã dự đoán vị trí deacetyl hóa cho SIRT1, 2, 3, 6, 7 ở mức residue. Vậy em còn làm gì mới?"*

Trả lời: "Em không làm bộ dự đoán mới. Deep-PLA huấn luyện trên 288 vị trí curate từ tài liệu, Ridgeway trên 6.801 vị trí mảng peptide, DeepSIRT ở mức protein — ba loại nhãn khác nhau, và **không bài nào báo cáo MCC hay AUPRC, cũng không bài nào đo lại trong tế bào với nhãn âm**. Em đo cả ba trên một tập đánh giá trong tế bào em dựng từ dữ liệu KO/KD công khai, với chỉ số chịu được mất cân bằng và kiểm soát rò rỉ theo protein và đồng dạng. Kết quả sơ bộ của em cho thấy nhãn in vitro gần như không chuyển được — MCC khoảng 0."

## 6. Việc tiếp theo, đã thay đổi thứ tự

1. **Lấy 288 vị trí curate của Deep-PLA** (từ web server hoặc Supplementary của bbz107) và đối chiếu với nhãn mảng Rauh. Đây giờ là việc có giá trị cao nhất: nó là phép đo chuyển miền thứ hai, độc lập.
2. Đọc DeepSIRT toàn văn, lấy đúng mức và tập dữ liệu, để bảng tiền lệ ở §4 đủ bốn dòng không còn `[chưa kiểm]`.
3. Tra ASEB (tài liệu [30, 31] của bbz107) xem phần SIRT7 của nó dùng dữ liệu gì.
4. Viết lại khung đề tài từ "bộ dự đoán đặc hiệu isoform" thành **benchmark chuyển miền cho ba bộ dự đoán đã công bố**.
