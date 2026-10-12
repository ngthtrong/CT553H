# Dự đoán liên kết kinase–phosphosite zero-shot cho dark kinome (DARKIN)

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md). Cập nhật lần cuối: **12/10/2026** (mở lại để đào sâu; khảo sát gốc 10–11/10/2026).

| | |
|---|---|
| Lĩnh vực | Tin sinh học, PTM/phosphoryl hóa, học máy (xếp hạng zero-shot) |
| Dữ liệu | DARKIN (*Bioinformatics* 2025, btaf480; repo `tastanlab/darkin`, đã pin commit và audit) |
| Giai đoạn | Đã audit split/nhãn và đối chiếu SOTA; chưa chạy baseline |

## Bài toán
Biết một phosphosite, cần **xếp hạng kinase nào có thể phosphoryl hóa nó**, kể cả kinase "tối" (chưa có cơ chất được chú giải, chưa xuất hiện khi huấn luyện, tức zero-shot). Đầu vào là cửa sổ trình tự quanh site và thông tin/embedding kinase. Đầu ra là thứ hạng kinase cho mỗi site, đánh giá theo trục kinase (macro AP) và trục site.

Hướng ưu tiên trong [đánh giá 10/10](research/darkin-evaluation.md): chọn lọc và đặt trọng số các liên kết dự đoán để **cải thiện suy luận hoạt tính kinase** khi thư viện cơ chất thiếu chú giải. Đây là giả thuyết, chưa được chứng minh.

## Cổng G1/G2/G3
| Cổng | Trạng thái | Bằng chứng |
|---|---|---|
| G1 nhãn độc lập | Đạt — nhãn kinase–substrate được chú giải từ cơ sở dữ liệu | [darkin-audit/](research/darkin-audit/README.md) |
| G2 đóng góp dương | **Yếu.** Sáu phép kiểm (11/10) cho thấy: trụ tính mới **sụp** (bài DARKIN đã báo cả hai trục trên 4 split); cả 3 trục phương pháp (mCNN trên PLM, PU/thiếu nhãn, listwise ranking) **đều có tiền lệ**. Còn lại: khoảng trống RQ2 (hoạt tính hạ nguồn) | [05-six-checks-results.md](research/checks/05-six-checks-results.md) |
| G3 ứng dụng | Khả thi (tra cứu kinase cho site), chưa thiết kế chi tiết | [main-topic-decision-2026-10-10.md §5](research/main-topic-decision-2026-10-10.md) |

## Rủi ro chính
- Hướng đang **rất nóng**: DARKIN 2025, SAGEPhos (ICLR 2025), COMPASS-PTM (*Nat Commun* 2026), KinoPlex (*Nat Biotech* 2026), Prot2Token…
- SOTA công khai theo trục kinase chỉ khoảng 0,19–0,24 AP. Spread giữa 4 split (~0,024) lớn hơn nhiều so với std giữa các seed.
- Lại là dạng dự đoán mức site, đúng kiểu mà [D-017](../../DECISIONS.md#d-017) khuyên không bó vào.

## Việc tiếp theo
- Xác định xem RQ2 (suy luận hoạt tính kinase hạ nguồn, benchmarKIN) có đủ dữ liệu cho kinase ít chú giải không. Nếu không đủ thì hướng này khó vượt G2.

## Trong thư mục này
- [log.md](log.md) — nhật ký (10/10/2026).
- research/: [darkin-evaluation.md](research/darkin-evaluation.md) · [main-topic-decision-2026-10-10.md](research/main-topic-decision-2026-10-10.md) (khuyến nghị cũ; đọc kèm checks) · [checks/](research/checks/05-six-checks-results.md) (01–05) · [darkin-audit/](research/darkin-audit/README.md)
