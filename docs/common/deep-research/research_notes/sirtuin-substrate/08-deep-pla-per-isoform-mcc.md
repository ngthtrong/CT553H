# Phép đo 288 vị trí: chưa làm được, nhưng đổi lại được một thứ tốt hơn

**Ngày:** 08/10/2026. **Việc được giao:** lấy 288 vị trí sirtuin curate của Deep-PLA và đối chiếu với nhãn mảng Rauh, để có phép đo chuyển miền thứ hai độc lập với [phép đo Sol 2012](03-data-inventory.md).

## 1. Phần không làm được, nói thẳng

**Không lấy được danh sách 288 vị trí từ môi trường cloud này.** Danh sách nằm trong Supplementary của bbz107, và Oxford University Press chặn:

| Nguồn thử | Kết quả |
|---|---|
| `academic.oup.com/bib/article/21/5/1798/5612158` | **403** `[tự kiểm]` |
| `academic.oup.com/bib/article-pdf/...` | **403** |
| `oup.silverchair-cdn.com/.../bbz107_supplementary_data.zip` (đoán đường dẫn) | **403** |
| `deeppla.cancerbio.info` và mirror `deeppla.omicsbio.info` | 200, nhưng **không có trang tải dữ liệu** (chỉ `index.php`, `webserver.php`, `help.php`, `contact.php`) |
| `plmd.biocuckoo.org` (CSDL nguồn của họ) | 200 nhưng chỉ còn **thư mục rỗng**, cơ sở dữ liệu coi như đã chết |
| `research.bioinformatics.udel.edu/iptmnet` (nguồn curate thay thế) | **503** |
| `awi.cuhk.edu.cn/dbPTM` | **403** |

**Việc cần sinh viên làm:** tải Supplementary của bbz107 bằng quyền truy cập đã dùng để lấy PDF (trang bài báo → mục *Supplementary data*), rồi đưa vào đây. Lúc đó phép đo đối chiếu chạy trong vài phút. Cho tới khi có file, kết luận "nhãn mảng gán bao nhiêu trong 288 vị trí đó là âm" vẫn là `[chưa kiểm]`.

## 2. Đổi lại: web server của họ công bố bảng hiệu năng từng isoform mà bài báo không có

Trang `help.php` của Deep-PLA có hai bảng đầy đủ — cross-validation (người) và test (phi-người) — với **số nhãn dương, số nhãn âm, và Sp/Sn/Pr tại ba ngưỡng High/Medium/Low cho từng enzyme** `[tác giả báo cáo]`. Bài báo chỉ báo AUC cho SIRT1 và cho họ HDAC gộp, nên đây là thông tin **không có trong bài**.

Từ đó **tự tính được MCC**, chỉ số mà họ không báo ở đâu cả: với P, N, Sn, Sp thì TP = Sn·P, FN = P − TP, TN = Sp·N, FP = N − TN, đủ để dựng ma trận nhầm lẫn.

### Cross-validation (người), ngưỡng High

| Isoform | Dương | Âm | Tỉ lệ dương nền | Sn | Sp | Pr | Pr / nền | **MCC (tự tính)** |
|---|---|---|---|---|---|---|---|---|
| SIRT1 | 185 | 2.982 | 5,84% | 0,514 | 0,949 | 0,374 | 6,4× | **0,403** |
| SIRT2 | 52 | 733 | 6,62% | 0,235 | 0,961 | 0,448 | 6,8× | **0,219** |
| SIRT3 | 30 | 522 | 5,43% | **0,077** | 0,964 | 0,340 | 6,3× | **0,049** |
| SIRT6 | 10 | 130 | 7,14% | 0,375 | 0,950 | 0,783 | 11,0× | **0,321** |
| SIRT7 | 12 | 279 | 4,12% | 0,143 | 0,827 | 0,100 | 2,4× | **−0,016** |
| HDAC gộp họ | 147 | 1.738 | 7,80% | 0,711 | 0,941 | 0,616 | 7,9× | **0,557** |

### Test (phi-người), ngưỡng High

| Isoform | Dương | Âm | Sn | Sp | Pr | **MCC (tự tính)** |
|---|---|---|---|---|---|---|
| SIRT1 | 33 | 601 | 0,364 | 0,950 | 0,286 | **0,280** |
| SIRT2 | 9 | 145 | 0,444 | 0,952 | 0,364 | **0,361** |
| SIRT3 | 17 | 190 | 0,353 | 0,953 | 0,400 | **0,323** |
| SIRT6 | **2** | 11 | 0,500 | 0,909 | 0,500 | 0,409 |
| SIRT7 | **4** | 25 | 0,500 | 0,960 | 0,667 | 0,521 |

Bảng số đầy đủ ba ngưỡng: [data/deep-pla-sirtuin-mcc-derived.csv](data/deep-pla-sirtuin-mcc-derived.csv).

## 3. Đọc bảng này thế nào

**Mô hình sirtuin của Deep-PLA yếu, và yếu nhất đúng ở chỗ quan trọng.** SIRT3 có độ nhạy **7,7%** ở ngưỡng High trong cross-validation, MCC **0,049** — gần như không phân biệt được gì. SIRT7 có MCC **−0,016**, tức **tệ hơn ngẫu nhiên** ở ngưỡng đó. Chỉ SIRT1 (MCC 0,403) và mô hình HDAC gộp họ (0,557) là có giá trị thực dụng; SIRT2 ở mức 0,219.

**Và mô hình gộp họ tốt hơn mọi mô hình từng isoform.** MCC 0,557 của "HDACs" cao hơn SIRT1 (0,403) và cao gấp hơn mười lần SIRT3. `[suy luận]` Điều này nói rằng ở cỡ dữ liệu 10–185 vị trí, **việc tách theo isoform làm hại nhiều hơn làm lợi** — đúng lập luận ủng hộ một mô hình đa nhãn dùng chung biểu diễn, thay vì bảy mô hình rời, mà [04-evaluation-design.md](04-evaluation-design.md) đề xuất ở bậc B8. Deep-PLA vô tình cung cấp bằng chứng cho thiết kế của đề tài.

**Test phi-người trông tốt hơn CV, nhưng đừng tin con số.** SIRT6 có **2** vị trí dương và SIRT7 có **4**. Ở cỡ đó, đổi một dự đoán là MCC nhảy hàng chục phần trăm; khoảng tin cậy rộng gần hết miền [−1, 1]. Không được dẫn MCC 0,409 và 0,521 như bằng chứng.

## 4. Phản biện với chính phép tính của tôi

1. **MCC suy từ số đã làm tròn.** Sn và Sp trên `help.php` làm tròn 4 chữ số; P, N là số nguyên. Sai số lan truyền nhỏ nhưng khác 0, nên nên đọc MCC ở hai chữ số, không ba.
2. **P, N trên web server lệch nhẹ so với Table 1 của bài:** SIRT1 **185** (web) so với **184** (Table 1), EP300 511 so với 510; các isoform khác trùng khớp. `[chưa kiểm]` lý do lệch 1.
3. **Dòng "HDACs" lệch nhiều hơn:** web server ghi 147 vị trí dương, Table 1 ghi 94 cho mục "HDACs". Chưa giải thích được `[chưa kiểm]`.
4. **Tỉ lệ dương nền là tạo tác của cách họ dựng tập âm**, không phải tỉ lệ sinh học. Nên MCC ở bảng này so được **giữa các enzyme trong cùng bài**, nhưng **không** so được với MCC của một bài khác có cách lấy mẫu âm khác. Đây đúng là lý do mà benchmark phải chạy lại mọi thứ trên cùng một giao thức.
5. Ngưỡng High/Medium/Low là của họ, không phải ngưỡng tối ưu MCC. MCC tối ưu của họ có thể cao hơn các số trên.

## 5. Hệ quả cho đề tài

Điều này **củng cố** khung benchmark ở [07-deep-pla-hdac-coverage.md](07-deep-pla-hdac-coverage.md) §4, và thêm một luận điểm mạnh hơn dự kiến:

> Ba bộ dự đoán cơ chất sirtuin đã công bố, không bộ nào báo MCC. Khi tự tính MCC từ chính số liệu Deep-PLA công bố, bốn trong năm mô hình isoform của họ có MCC dưới 0,33, một mô hình âm, và mô hình **gộp họ** lại tốt hơn mọi mô hình tách theo isoform.

Đó là một phát hiện có thể nói trực tiếp với GVHD, không cần chờ thêm dữ liệu, và nó biện minh cho hai quyết định thiết kế cùng lúc: dùng MCC/AUPRC thay Sn/Sp/Pr, và chia sẻ biểu diễn giữa các isoform thay vì bảy mô hình rời.

## 6. Tái lập

```
curl -sS http://deeppla.cancerbio.info/help.php -o help.html   # 200, có hai bảng hiệu năng
```
Rồi tách bảng bằng regex `<table>…</table>`, và tính MCC từ (P, N, Sn, Sp) như §2. Script: `scratchpad/scripts/mcc.py` (không lưu vào repo vì chỉ là vài dòng số hoá bảng trên).
