[← Bài trước](08-contribution.md) · Bài 9/10 · [Bài sau: Dữ liệu thật →](10-data-up-close.md)

# Bài 9 — Rủi ro và điều có thể làm đề tài sụp

Bài này tồn tại để bạn không bị bất ngờ. Xếp theo mức nguy hiểm.

---

![Rủi ro xếp theo mức nguy hiểm](figures/fig-14-risks.svg)

*Sơ đồ tự dựng. Chi tiết từng rủi ro ở dưới.*

---

## Rủi ro 1 — ~~lực thống kê~~ → **đã giải quyết 13/10/2026**

**Vấn đề đã nêu:** chia test theo cụm protein chỉ còn **221–322 footprint**. Với n ≈ 250, một cải thiện nhỏ có thể không chứng minh được.

**✅ Đã tính, và tập test đủ lực.** So với baseline thành phần trung thực (0,4897) thì chỉ cần **18** peptide. So với mốc oracle 0,6045 thì cần **209**, và n = 221–322 cho lực **0,82–0,94**. Kết luận vững ở cả ba cách xử lý tie.

**Việc còn lại từ rủi ro này:** dùng **split coverage 80%** (271–322) chứ không phải cov50, vì ở n = 221 lực chỉ 0,82. Và khi có mô hình thật thì phải tính lại lực bằng độ lệch chuẩn của chính cặp so sánh đó.

Nguồn: [full-data-audit mục 5](../../topics/degron-footprint/research/full-data-audit/README.md), giải thích dễ hiểu ở [bài 10](10-data-up-close.md).

> **Rủi ro số một mới: nhãn mức residue chỉ lặp lại khoảng một nửa.** Hai lần đo độc lập đồng ý "peptide này có footprint" ở mức **89,3%**, nhưng đồng ý **đúng vị trí nào** chỉ ở mức **Jaccard 0,4965**, và chỉ **16,0%** peptide có tập vị trí dương giống hệt. Đề tài dự đoán đúng ở mức residue đó, nên đây là trần cứng cho mọi mô hình. Không chữa được bằng siết ngưỡng reads (đã thử, thất bại).

**Nếu sụp:** giảm độ chặt của phép chia cụm (cov80 cho 271–322 thay vì 221–301), hoặc bổ sung bộ nhân của [Larsen 2025](papers/larsen-2025.md), hoặc kích hoạt dự phòng.

---

## Rủi ro 2 — phần dư 35% có thể chỉ là nhiễu

**Vấn đề:** đề tài trông cậy vào việc 35,0% phương sai ΔPSI còn lại sau oracle thành phần là **ngữ cảnh học được**. Nhưng:

- dữ liệu dùng **một replicate**, không phải trung bình nhiều lần
- ngưỡng reads tối thiểu **thấp**
- nhãn genotype BAG6 của replicate này **chưa rõ**
- **chưa ai tách** phần ngữ cảnh khỏi phần nhiễu đo

Nếu phần lớn 35% đó là nhiễu thí nghiệm, thì **không mô hình nào học được nó**, và dư địa 0,1747 là ảo.

> **⚠ Cập nhật 13/10/2026 — đã kiểm, và lo ngại này phần lớn là đúng.** Dựng được lần đo thứ hai từ read thô nên tách được trực tiếp:
>
> | | |
> |---|---:|
> | Phần dư sau oracle thành phần | 0,3612 |
> | Trong đó là **nhiễu đo** | **75,9%** |
> | **Ngữ cảnh học được, cận trên** | **0,0872** |
>
> Tức phần có thể học thêm là khoảng **8,7%** phương sai, **không phải 35,0%**. Dư địa 0,1747 thì **đúng là ảo**, nhưng vì một lý do khác nữa: nó là hiệu của hai oracle đọc nhãn test. Dư địa thật là **0,1617** so với baseline thành phần trung thực.
>
> **Đã thử chữa và thất bại:** siết ngưỡng reads từ 10 lên 200 **không** giảm tỉ lệ nhiễu (giữ 0,72–0,77) mà mất một nửa dữ liệu. Nhiễu ~0,24–0,34 được xác nhận **bốn lần độc lập** ⇒ là tính chất của thí nghiệm GPS. **Đừng thử lại hướng này.**
>
> Chi tiết dễ hiểu: [bài 10 mục 6](10-data-up-close.md). Số liệu: [full-data-audit](../../topics/degron-footprint/research/full-data-audit/README.md).

---

## Rủi ro 3 — G3, ứng dụng không khác biệt được

**Vấn đề:** đã có **bốn** tiền lệ — [DEGRONOPEDIA](papers/degronopedia-2024.md), máy chủ web [MetaDegron](papers/metadegron-2024.md), Colab của nhóm PAP, và — **mới phát hiện 13/10** — **mô hình học máy của chính nhóm Zhang 2023**, dự đoán PSI toàn peptidome (Pearson 0,8955, RMSE 0,563 trên 260.989 peptide), nằm trong file Mendeley 393 MB mà repo chưa từng tải. Cái thứ tư **khác phạm vi** (dự đoán ở mức peptide, không phải mức residue) nên không phải đối thủ trực tiếp, nhưng **phải nêu** trong đề cương. Tiêu chí 5 của GVHD không thể thiếu, nhưng "làm thêm một web nữa" không phải đóng góp.

**Cách xử lý:** nhắm vào thứ cả ba đều không có — **ma trận vị trí × acid amin thay vào, dựa trên nhãn đột biến thực nghiệm**. Phải kiểm lại ba sản phẩm đó thật sự không xuất ra thứ này.

---

## Rủi ro 4 — kiến trúc có thể không thắng, hoặc không cần thiết

Hai nhánh:

**4a. MIL không cần thiết.** Khi đã có nhãn mức residue, một đầu hồi quy theo vị trí là mô hình tự nhiên. Nếu nó đã đủ thì cơ chế túi là phức tạp không cần thiết. Đây là **đối chứng bắt buộc**, không phải việc có thể bỏ qua.

**4b. Kiến trúc khu trú không thắng trên thang điểm đoạn.** Có dấu hiệu: đổi phép gộp làm Pearson sụt 0,824 → 0,344, entropy theo vị trí gần tối đa (3,294/3,401). Nhưng **phép thử đó không công bằng** (dùng trọng số huấn luyện cho gộp trung bình), nên chưa kết luận được.

**Cách xử lý:** không đặt đóng góp lên thang điểm đoạn. Dùng bậc 2 và 3 ([bài 7](07-evaluation.md)).

---

## Rủi ro 5 — tính mới bị thu hẹp thêm

Đã bị thu hẹp hai lần rồi:

| Lần | Phát hiện | Mất gì |
|---|---|---|
| 11/10 | [BioBlobs](papers/bioblobs-2025.md) đã dùng attention-MIL trên protein; [OmniESI](papers/omniesi-2025.md) đã dùng điều biến có điều kiện | Không được nói cơ chế là mới |
| 11/10 | [Larsen 2025](papers/larsen-2025.md) đã dùng rASA/pLDDT và đã làm bản đồ ΔPAP *in silico* | "Dùng cấu trúc" và "giải thích biến thể" không còn mới |

**Việc còn chưa làm:** tra danh sách trích dẫn của bài 2026 và tra nội bộ [MetaDegron](papers/metadegron-2024.md). Có thể còn phát hiện nữa.

**Cách xử lý:** phát biểu hẹp từ đầu — *mới ở chỗ ghép và ở chỗ đặt cổng phơi lộ tại bước gộp, chưa thấy áp cho degron*. Nếu nói hẹp sẵn thì một phát hiện mới không làm sụp tuyên bố.

---

## Rủi ro 6 — thước đo không thống nhất với GVHD

**Vấn đề:** GVHD có thể quen nhìn Pearson trên thang điểm đoạn, vì đó là con số bài báo in. Nhưng ở đó trần chỉ còn **+0,0032**.

**Cách xử lý:** hỏi và thống nhất **trước khi bắt đầu**, ở buổi gặp tuần 6. Đây là một câu cụ thể nên đưa vào bản chuẩn bị.

---

## Rủi ro 7 — nợ kỹ thuật nhỏ cần dọn

Không nguy hiểm nhưng sẽ gây rắc rối nếu để lâu:

| Việc | Chi tiết |
|---|---|
| 19 footprint đã map accession nhưng chưa khớp peptide, cộng 3 footprint thiếu trình tự | **cần curate** |
| 9 accession chưa lấy được trình tự UniProt | đã loại khỏi phép chia cụm, **không được giả làm singleton** |
| 813 peptide có stop `*` cuối (336 là footprint) | phải mask, **không coi `*` là acid amin** |
| Cụm MMseqs2 trong `interim/` ghi đường dẫn tuyệt đối cũ | chạy lại `prepare_protein_clusters.py` nếu cần ([resources](../../resources/README.md)) |
| Phép chia 80/10/10 qua 5 seed | là **phép thử đo quy mô**, **chưa phải benchmark chính thức được chốt** |

---

## Tóm lại: ba việc trước khi viết dòng code huấn luyện đầu tiên

1. **Tính lực thống kê** trên n = 221–322. Rẻ, dữ liệu đã có. Quyết định đề tài đứng hay sụp.
2. **Kiểm tính ổn định của nhãn** giữa replicate và theo độ sâu reads. Quyết định dư địa 0,1747 là thật hay ảo.
3. **Thống nhất thước đo với GVHD** ở tuần 6. Quyết định đề tài được đánh giá bằng thước nào.

Cả ba đều **không cần GPU** và **không cần tải thêm dữ liệu**.

---

[← Bài trước](08-contribution.md) · [Bài sau: Dữ liệu thật →](10-data-up-close.md) · [Về hub](README.md)
