# Thực hành đọc lại dự án và gợi ý tự kiểm {#practice}

## Buổi 1: kể được chuỗi phép đo

Vẽ lại construct → tế bào → FACS → bin → read count → PSI → ΔPSI. Dưới mỗi mũi tên, ghi vật đang đếm hoặc đại lượng đang tính. Dùng ví dụ count ở chương 3 để tính lại hai PSI và hiệu số. Đầu ra mong đợi là một trang giải thích, không cần chạy model.

**Điểm cần có trong câu trả lời:** DNA mang thiết kế; tế bào phát tín hiệu; read là sản phẩm giải trình tự chứ không phải số tế bào; count cần chuẩn hóa theo bin; WT phải cùng điều kiện; ΔPSI dương chỉ theo hướng tăng chỉ số ổn định reporter. Không đảo thành tăng hoạt tính degron.

## Buổi 2: theo dõi một mutation qua dữ liệu

Chọn một ô có số trong heatmap HIF1A đã đo. Ghi WT, vị trí, alt và giá trị; chọn thêm một ô thiếu. Mô tả lý do không thể gán ô thiếu bằng 0. Nếu chưa tra được residue gốc hoặc tọa độ protein, ghi “chưa xác minh” thay vì tự suy ra từ màu.

**Điểm cần có:** mutation key phải xác định WT/context; vị trí là 1-based hay 0-based cần nói rõ; 28×20 là 560 ô thiết kế, còn 532 phép thay khác WT; đồng nghĩa DNA và WT→WT không phải mutation amino acid; cùng vị trí protein ở hai tile có thể có context khác.

## Buổi 3: tự phát hiện một phép so không công bằng

Lập hai cột cho một cặp model: population, outer split, inner selection, số seed, ensemble, feature, budget, metric và CI. Điền các yếu tố khác nhau. Thử giải thích vì sao random split theo ô thường lạc quan khi peptide hoặc protein tương đồng xuất hiện ở cả hai phía.

**Điểm cần có:** split theo nhóm giữ phụ thuộc gần nhau trong cùng phía; cov80 nói coverage, không phải identity 80%; scaler/PCA fit train; AUROC không phải accuracy; MAE giảm là tốt, AUROC giảm thường là xấu; CI bootstrap ô không phản ánh đơn vị protein độc lập.

## Buổi 4: viết một trang đọc kết quả

Dùng ba phép so: Ridge D−B; CNN-D−pointwise-D; mCNN-E với CNN-D. Với mỗi phép, ghi số, dấu tốt/xấu, CI nếu có, loại phép so chính/mô tả và điều chưa suy được. Không cộng các cải thiện ở những cohort khác nhau.

**Điểm cần có:** D/E hỗ trợ giảm MAE nhưng chưa xác nhận mọi cận vượt mức thực dụng 0,02; E có đánh đổi miền PSI thấp; chênh trung bình 0,00051 chưa tạo người thắng ổn định; pLM chỉ là ESM2-35M trong nhóm kết quả đó. Ensemble subset 25% không tương đương một model chỉ thấy đúng 25% nhãn.

## Buổi 5: phân biệt kế hoạch và kết quả

Giải thích bằng sơ đồ hai nhánh frozen và LoRA: dữ liệu đi đâu, phần nào có gradient, epoch chọn từ đâu, checkpoint giữ gì và OOF xuất hiện khi nào. Chỉ dùng kế hoạch chương 14, không suy hiệu năng từ tốc độ hoặc một inner loss.

**Điểm cần có:** LoRA học A/B hạng thấp và head, frozen chỉ học head tương ứng; mode `eval` không tự tắt gradient; tokenizer phải khớp residue; cùng split nhưng khác dropout/optimizer vẫn có yếu tố gây nhiễu; phải đủ fold/seed, CI, calibration/artifact trước promotion; T không dùng chọn family.

## Buổi 6: kiểm ranh giới phần mềm

Từ ảnh Workspace v2, chọn ba tính năng nhìn có vẻ hoàn chỉnh rồi viết bằng chứng cần có để xác nhận backend thật. Thử tính tọa độ tile: start=24, j=5 ⇒ protein position=28. Với protein dài 80, tile 1–28, 24–51 và 47–74 còn hở 75–80.

**Điểm cần có:** prototype dùng fixture và bộ nhớ tab; lưu bền cần kiểm reload/restart và CSDL; job cần state/recovery/partial failure; import giữ endpoint/replicate/provenance; ClinVar cần mapping đúng; export cần model/data/source version. Baseline test lịch sử chưa nghiệm thu scope mới.

## Đọc nguồn an toàn trong checkout

Các lệnh sau chỉ đọc tài liệu/snapshot; không train, pause hoặc resume campaign. Chạy từ gốc repository. Máy cần Python 3 để đọc JSON; đây không phải hướng dẫn cài lại môi trường CUDA.

```bash
python3 -m json.tool \
  topics/degron-footprint/learning/evidence.json

python3 -m json.tool \
  topics/degron-footprint/learning/figure-manifest.json
```

Mở danh mục chương cuối trước khi đi vào từng kết quả gốc. Với nguồn NC, tìm population và phép so trước số tốt nhất. Với nguồn KH, đọc điều kiện thực thi và những việc chưa xong. Với nguồn PM, đọc trạng thái baseline/prototype/planned trước khi thử giao diện.

::: {.exercise title="Bài tổng hợp cuối"}
Viết khoảng một trang trả lời: đề tài dự đoán gì; nhãn được dựng thế nào; tại sao chia nhóm; ba phát hiện quan trọng nhất; một lựa chọn không có lợi; kế hoạch local đang kiểm câu hỏi gì; còn thiếu gì trước khi dùng model mới. Mỗi phát hiện gắn một mã nguồn. Đây là bài tự học, không có đánh giá năng lực người học được tự động ghi nhận.
:::
