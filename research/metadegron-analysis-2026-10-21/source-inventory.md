# Kiểm kê nguồn

[ĐO] Repo [BioDataStudy/MetaDegron](https://github.com/BioDataStudy/MetaDegron) ghim `ca12c0cf9d2e2d76655689973ac45c6c063a899d`, commit ngày `2024-06-20T20:57:29+08:00`. Có 80 file được git theo dõi, tổng 33,062,312 byte; gồm 8 Python, 6 notebook và 15 PHP, cùng JavaScript/CSS và tài sản web. Cây đầy đủ: [repository-tree.md](repository-tree.md). [repository-inventory.json](repository-inventory.json), [inventory-sources.py](inventory-sources.py).

[ĐO] Có `models/degron_DL.h5`, `degron_DL.json`, `classifier_XGBoost.pickle`, `uniref50_v2/options.json`; không có file LICENSE trong cây ghim. SHA-256 **mọi file tải giữ lại**, gồm từng bảng và trọng số nhỏ, nằm trong [source-manifest.json](source-manifest.json). Không đưa payload nguồn, hình hoặc checkpoint vào phần git theo dõi. [repository-inventory.json](repository-inventory.json).

[ĐỌC-MÃ] README nêu Python 3.7, TensorFlow 1.15, Keras 2.3.1, allennlp 0.9.0, h5py 2.10.0, protobuf 3.20 và thư viện khoa học; có XGBoost trong mã dù hướng dẫn cài không liệt kê đầy đủ. Không có requirements/environment/setup đóng gói. Danh sách import và vị trí mã: [code-audit.json](code-audit.json). Không chạy lệnh cài đặt của repo.

## Các kênh nguồn đã thử

| Nguồn | Trạng thái và nội dung | Quyền sử dụng đã kiểm |
|---|---|---|
| [Bài báo DOI](https://doi.org/10.1093/bib/bbae519) / [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/) | [ĐO] Publisher trực tiếp 403; PMC HTML và Europe PMC XML đọc được toàn văn | [NGUỒN] Bài ghi CC BY 4.0; nguyên văn tuyên bố nằm trong manifest |
| Supplementary của PMC | [ĐO] URL XLSX lẻ trả challenge HTML dù status 200; ZIP supplementaryFiles của Europe PMC có XLSX thật | [NGUỒN] Thuộc tài liệu kèm bài; quyền các nguồn nhập như ELM cần kiểm riêng |
| GitHub | [ĐO] Clone thành công; dữ liệu/thuộc tính, mã train/predict, checkpoint và web code có sẵn | [CHƯA XÁC MINH] Không có LICENSE; metadata GitHub không thay giấy phép |
| [Server HTTP](http://modinfor.com/MetaDegron/) | [ĐO] Home, Prediction, Tutorial và Download đọc được qua HTTP; HTTPS timeout; Download hiện không có link dữ liệu trong nội dung nhận được | [CHƯA XÁC MINH] Chỉ dẫn chính sách UTHealth trả 403; Terms.php 404; không submit |
| Trọng số SeqVec / all_train_embedding.npy | [ĐO] Hai endpoint README chỉ trả HTTP 200; payload quá giới hạn fetcher nên không giữ bản tải | [CHƯA XÁC MINH] Không có SHA đầy đủ cho file không tải xong; không tuyên bố đã audit object NPY đó |
| Zenodo/Figshare | [NGUỒN] Tra các truy vấn ghi ở discovery-searches.json chưa xác định deposit riêng của MetaDegron | [CHƯA XÁC MINH] Không kết luận không tồn tại |
| [ELM downloads](http://elm.eu.org/downloads.html) | [ĐO] Đọc query protein cho mẫu; endpoint không query chỉ có giới hạn mặc định, không phải toàn CSDL | [NGUỒN] Academic License đọc nguyên văn từ PDF; dùng nghiên cứu nội bộ, không tự suy ra quyền tích hợp/phân phối |
| Bảng review 2017 | [ĐO] HTTP 200 nhưng nội dung báo chỉ ELTEnet được truy cập | [CHƯA XÁC MINH] Không lấy được bảng gốc |
| [DegronMD](https://pmc.ncbi.nlm.nih.gov/articles/PMC10701100/) | [ĐO] XML bài đọc được; trang Download 403 | [NGUỒN] Bài CC BY 4.0; [CHƯA XÁC MINH] quyền toàn bộ dữ liệu web và nguồn nhập |

[ĐO] Bằng chứng truy cập, status, ngày, URL cuối, content validation và lỗi chính xác: [source-manifest.json](source-manifest.json); truy vấn tìm kiếm: [discovery-searches.json](discovery-searches.json). Script [fetch-sources.py](fetch-sources.py) chỉ tải byte, không chạy nội dung. Các file HTML challenge được giữ làm bằng chứng lỗi, không đếm là bảng.

## Từ nguồn đến kết quả

[ĐỌC-MÃ] `data/degron_data.txt` ↔ supplementary S2 là danh sách curate; `annotated_degrons_properties.tsv` là tập con có thuộc tính; background ở `data/` và `supporting_file/` là hai pool khác nhau, không tráo cho nhau. S4 có Positive và Simulated; pool âm thực sự được notebook benchmarking đọc lại là `simulated_degron2.csv`. Danh sách schema và số dòng từng file: [dataset-audit.json](dataset-audit.json), [table-schemas.md](table-schemas.md).

[NGUỒN] S2 trỏ review *Degrons in cancer*, ELM, *Tripartite degrons* và bài Nature Cancer; không có bằng chứng MetaDegron trực tiếp thu nhãn từ DEGRONOPEDIA. DEGRONOPEDIA/DegronMD xuất hiện như tài nguyên được thảo luận. [Toàn văn](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/).

[CHƯA XÁC MINH] Không gán giấy phép mã GitHub từ giấy phép bài báo. Việc đọc và ghi số đếm không đồng nghĩa cho phép phân phối lại bảng gốc hay nhúng regex ELM vào ứng dụng công khai. Chưa nhập nguồn mới vào huấn luyện chính.
