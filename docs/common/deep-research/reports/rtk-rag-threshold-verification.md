# Kiểm chứng cách chọn ngưỡng G-mean trong RTK_RAG

> Kiểm ngày 01/10/2026 bằng cách tải và đọc JSON notebook gốc từ GitHub, không thực thi huấn luyện. Kết luận áp dụng cho mã và output lưu trong phiên bản được dẫn; chưa xác nhận phiên bản này tạo ra số liệu của bài báo.

## Nguồn cố định để mở lại

- Repo: `B1607/RTK_RAG`, commit `b7bd4c2347c7d44d24ae3d13e42082ba6cd62627` (HEAD được đọc khi kiểm tra).
- [Notebook CODE/MCNN_npy.ipynb tại commit này](https://github.com/B1607/RTK_RAG/blob/b7bd4c2347c7d44d24ae3d13e42082ba6cd62627/CODE/MCNN_npy.ipynb).
- [JSON gốc của notebook](https://raw.githubusercontent.com/B1607/RTK_RAG/b7bd4c2347c7d44d24ae3d13e42082ba6cd62627/CODE/MCNN_npy.ipynb).
- SHA-256 của tệp tải về: `1d4e1b61a2069e5adbd3d0954ad529731298ee7f55732f9c44ec442e6827160f`.

Trong giao diện notebook, tìm `def model_test` hoặc `gmeans`. Hàm nằm ở **ô thứ 10 nếu đếm tất cả các ô từ 1**, có nhãn thực thi `In [6]` (`cells[9]` trong JSON). Số ô và số lần thực thi là hai thứ khác nhau.

## Bằng chứng trực tiếp

Đoạn cốt lõi trong `model_test(model, x_test, y_test)`:

```python
fpr, tpr, thresholds = roc_curve(y_test[:,1], pred_test[:, 1])
gmeans = np.sqrt(tpr * (1-fpr))
ix = np.argmax(gmeans)
threshold = thresholds[ix]
y_pred = (pred_test[:, 1] >= threshold).astype(int)
```

Các dòng không liền nhau ở trên lần lượt nằm tại dòng 7, 21, 23, 25 và 27 trong ô định nghĩa hàm. Xem [mã JSON dòng 253–276](https://github.com/B1607/RTK_RAG/blob/b7bd4c2347c7d44d24ae3d13e42082ba6cd62627/CODE/MCNN_npy.ipynb?plain=1#L253-L276).

`pred_test` được tạo bằng `model.predict(x_test)`. `roc_curve` sử dụng nhãn thật `y_test` và điểm dự đoán để tính TPR/FPR ở các ngưỡng. G-mean ở đây là căn bậc hai của sensitivity × specificity. Sau khi chọn ngưỡng có G-mean lớn nhất, hàm tính confusion matrix bằng **cùng `y_test` và `y_pred`**, rồi tính MCC, F1, sensitivity, specificity và accuracy. Hàm không nhận một ngưỡng đã được chọn trên validation riêng.

### Những nhánh gọi hàm này

| Vị trí | Dữ liệu được truyền vào | Điều xác nhận được |
|---|---|---|
| Ô 11 (`In [7]`), nhánh `VALIDATION_MODE == "cross"` | `X_test`, `Y_test` lấy từ `test_index` của `KFold` trên dữ liệu huấn luyện | Ngưỡng được chọn bằng nhãn của chính fold giữ lại rồi chấm trên fold đó. [Lời gọi, dòng 738](https://github.com/B1607/RTK_RAG/blob/b7bd4c2347c7d44d24ae3d13e42082ba6cd62627/CODE/MCNN_npy.ipynb?plain=1#L738) |
| Ô 12 (`In [8]`), nhánh `VALIDATION_MODE == "independent"` | `x_test`, `y_test` | Nếu chạy nhánh này, cùng hàm sẽ chọn ngưỡng trên tập truyền vào để kiểm tra độc lập. [Lời gọi, dòng 784](https://github.com/B1607/RTK_RAG/blob/b7bd4c2347c7d44d24ae3d13e42082ba6cd62627/CODE/MCNN_npy.ipynb?plain=1#L784) |

## Output lưu sẵn và giới hạn

- Cấu hình đang lưu đặt `VALIDATION_MODE="cross"`, `DATASET="ATP_549"`, `DATA_TYPE="rag_prottrans"`.
- Ô 11 có output năm fold. Ví dụ fold đầu in `Best Threshold=0.020588556304574013, G-Mean=0.8822473601782946`, rồi MCC `0.4362`. Đây là **output đã lưu**, không phải kết quả chạy lại trong lần kiểm chứng này.
- Ô 12 có `execution_count=8` nhưng `outputs=[]`. Với cấu hình `cross`, lệnh `if` của ô này có thể đã bị bỏ qua. Không có output chứng minh việc chấm độc lập đã thực sự chạy trong bản lưu.
- Mã và output không hoàn toàn đồng bộ: `model_test` hiện trả **13** giá trị, nhưng lời gọi trong nhánh cross chỉ nhận **9**. Chạy nguyên trạng tới đây sẽ gây lỗi unpack. Vì thế không thể dùng output lưu sẵn để chứng minh toàn bộ notebook hiện tại tái chạy được hoặc xác định chính xác phiên bản sinh kết quả đó.
- Ô 2 import `import_test_die as load_data`, nhưng cây repo của commit này không có module đó; thư mục `CODE` chỉ có notebook và `import_data.py`. Tệp [import_data.py, dòng 22–35](https://github.com/B1607/RTK_RAG/blob/b7bd4c2347c7d44d24ae3d13e42082ba6cd62627/CODE/import_data.py#L22-L35) có đường dẫn ATP-549 và RTK-69, nhưng chưa thể coi đây chính là module đã được notebook dùng.

**Kết luận có thể bảo vệ:** mã công khai của hàm đánh giá chọn ngưỡng từ nhãn của tập đang chấm. Luồng gọi ở kiểm định chéo xác định rõ đó là fold giữ lại; nhánh độc lập cũng gọi cùng hàm. Chưa đủ bằng chứng để quy toàn bộ chỉ số trong bài báo hoặc ngưỡng của demo triển khai cho đoạn mã này.

## Hệ quả đối với RQ2

- Bằng chứng hỗ trợ **nhánh (a): chọn ngưỡng trên tập đánh giá so với chọn trên validation**. Nó không tự xác minh các giả thuyết về lọc đồng dạng hoặc thành phần kho truy hồi ở nhánh (b)/(c).
- Thí nghiệm phù hợp: giữ nguyên mô hình và điểm dự đoán test; so sánh ngưỡng G-mean chọn trên validation với ngưỡng G-mean chọn từ nhãn test. Nhánh dùng nhãn test chỉ là đối chứng hậu kiểm, không dùng để báo hiệu năng triển khai.
- Đo ΔMCC, ΔF1, sensitivity/specificity và G-mean. G-mean chọn trên test tối ưu đúng tiêu chí đó trên test; không có bảo đảm MCC hoặc F1 luôn cao hơn vì đó là các hàm mục tiêu khác.
- **AUPRC và AUROC không đổi nếu giữ nguyên nhãn/điểm dự đoán và chỉ đổi ngưỡng.** Trong notebook, hai diện tích này được tính từ điểm liên tục trước khi chọn ngưỡng. Không dùng ΔAUPRC làm bằng chứng cho riêng nhánh (a). AUPRC vẫn hữu ích khi nhánh (b)/(c) thay đổi dữ liệu, mô hình hoặc điểm dự đoán, nhưng phải thiết kế so sánh riêng.

## Cách trả lời “em thấy ở đâu?”

> Em thấy trong `CODE/MCNN_npy.ipynb` của repo RTK_RAG, hàm `model_test`, ô có nhãn `In [6]`. Hàm gọi `roc_curve` bằng `y_test`, lấy ngưỡng có G-mean lớn nhất, rồi tính confusion matrix và MCC/F1 bằng chính `y_test`. Nhánh cross-validation gọi hàm với fold giữ lại; nhánh independent cũng gọi cùng hàm nhưng không có output lưu. Em muốn hỏi thầy phiên bản dùng trong bài có chọn ngưỡng trên một validation riêng hay không, vì em mới xác nhận được mã công khai này.
