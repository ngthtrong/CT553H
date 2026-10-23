# RUN — chạy notebook trên Kaggle / Colab và mang kết quả về

Dành cho Trọng. Mọi bước dưới đây là **việc tay của người**; tôi (Claude) không upload gì lên dịch vụ ngoài. Giao diện Kaggle/Colab thay đổi theo thời gian: tên nút ghi dưới đây là **mô tả, chưa kiểm** — đối chiếu với giao diện thực.

## 0. Thứ tự chạy

| Thứ tự | Notebook (thư mục `research/…`) | GPU | Internet | Thời gian ước lượng (**chưa benchmark**) | Phụ thuộc |
|---:|---|:--:|:--:|---|---|
| 1 | `r0-reproduce-notebook-2026-10-22/00-reproduce.ipynb` | không | không | vài phút | — |
| 2 | `r3-domain-gate-2026-10-22/r3-domain-gate.ipynb` | không | không | vài phút | R0 ĐẠT (đặt `R0_CONFIRMED = True`) |
| 3 | `r2-esm-features-2026-10-22/r2-esm.ipynb` | có | **có** (tải trọng số) | xem README của R2 | R0 ĐẠT |
| 4 | `r1-degformer-clean-2026-10-22/r1-degformer-clean.ipynb` | có | không | xem README của R1 | R0 ĐẠT |
| 5 | `r6-ladder-scan-2026-10-23/r6-ladder-scan.ipynb` (**một** notebook cho mọi giai đoạn) | có | **có** (tải 4 cỡ ESM-2) | xem README của R6; ô benchmark in giờ GPU thật | R0 ĐẠT; cần **gói dữ liệu v2** (có `r6-scantable.npz`): `make_data_package.py --version v2` |

R0 đỏ ⇒ **dừng, gửi `gates.json` + `env.json` cho tôi**, đừng chạy các notebook sau.

## 1. Dựng gói trên máy (tôi đã làm một lần; làm lại khi mã hoặc PROTOCOL đổi)

Từ gốc repo:

```bash
K=topics/degron-footprint/research/notebook-kit-2026-10-22
python3 -I $K/make_data_package.py --list     # xem danh sách file, giấy phép, kích thước — DUYỆT trước khi upload
python3 -I $K/make_data_package.py            # -> topics/degron-footprint/data/processed/packages/degron-data-v1.zip
python3 -I $K/make_code_package.py            # -> .../packages/degron-code-<commit>-dirty.zip
```

Ra hai file zip + hai file `.sha256` ở `topics/degron-footprint/data/processed/packages/`. **Đọc danh sách `--list` trước khi upload**: đó là các file sẽ rời máy bạn. Chỉ có nguồn được phép (Zhang 2023 và cache dẫn xuất, Voutsinos MIT, UniProt, Degformer Apache-2.0, GEO GSE240610 — công khai, phải trích dẫn). Không có Koren, MetaDegron, Larsen, ClinVar.

## 2. Kaggle (nền tảng chính)

1. Đăng nhập kaggle.com. **Xác minh số điện thoại** (thường là điều kiện để bật GPU và Internet) `[CHƯA XÁC MINH]`.
2. **Tạo dataset dữ liệu:** *Datasets → New Dataset* → tải lên `degron-data-v1.zip` → tên `degron-data-v1` → để **Private** → *Create*. Kaggle thường tự giải nén zip; `nbkit` xử lý cả hai trường hợp (đã giải nén hoặc còn zip).
3. **Tạo dataset mã:** làm tương tự với `degron-code-<commit>-dirty.zip` → tên `degron-code`. Mỗi lần dựng lại gói mã: vào dataset → *New Version* → tải zip mới.
4. **Tạo notebook:** *Code → New Notebook* → *File → Import Notebook* → chọn file `.ipynb` trong repo (bảng ở mục 0).
5. **Gắn dữ liệu:** panel bên phải *Input → Add Input* → thêm **cả hai** dataset (`degron-data-v1`, `degron-code`).
6. **Cài đặt** (*Session options / Settings*): *Accelerator* = **None** cho R0 và R3, **GPU** cho R1/R2; *Internet* = **Off**, trừ R2 (cần tải trọng số mô hình) thì **On**.
7. **Chạy:** *Run All* (R0 ~vài phút). Đọc dòng cuối: `R0 ĐẠT` hoặc `R0 HỎNG: …`.
8. **Lưu & tải kết quả:** cách chắc nhất là *Save Version → Save & Run All (Commit)* để đầu ra được giữ lại; rồi vào tab *Output* tải `…-results.zip` (nằm trong `/kaggle/working/out/`). Nếu chỉ chạy tương tác, **tải ngay trước khi đóng phiên** vì `/kaggle/working` bị xoá khi phiên kết thúc.

## 3. Colab (dự phòng)

1. Mở colab.research.google.com → *File → Upload notebook* → chọn `.ipynb`.
2. *Runtime → Change runtime type*: CPU cho R0/R3, **T4 GPU** cho R1/R2.
3. Tải hai zip lên `/content` (panel *Files* → upload) **hoặc** đặt vào Google Drive rồi `from google.colab import drive; drive.mount('/content/drive')` trước khi chạy ô 2. Tên file phải bắt đầu bằng `degron-code` và `degron-data`.
4. *Runtime → Run all*. Kết quả ở `/content/out/…-results.zip`; tải qua panel *Files*.

## 4. Đặt kết quả về repo

Giải nén `…-results.zip` vào thư mục thí nghiệm, đặt tên có nền tảng và ngày, ví dụ:

```
topics/degron-footprint/research/r0-reproduce-notebook-2026-10-22/run-kaggle-20261023/
    results.json  env.json  gates.json  verify.json
topics/degron-footprint/research/r3-domain-gate-2026-10-22/run-kaggle-20261023/
    results.json  gate-weights.npz  gate-card.json  env.json  gates.json
```

Kèm **notebook đã thực thi** (Kaggle: *Download* notebook từ trang phiên bản; Colab: *File → Download .ipynb*), lược đầu ra quá lớn trước khi commit. `gate-weights.npz` và checkpoint không lên git. Rồi báo tôi: tôi đọc `results.json`, đối chiếu tiêu chí chốt trước, viết README kết quả và cập nhật sổ nguồn gốc `data/README.md`.

## 5. Sự cố thường gặp

| Triệu chứng | Nguyên nhân hay gặp | Xử lý |
|---|---|---|
| `Không thấy gói mã degron-code` ở ô 2 | Chưa gắn dataset mã vào notebook | *Add Input* lại (mục 2, bước 5) |
| `manifest dữ liệu không khớp` | Upload dở, hoặc dữ liệu bị đổi | Kiểm `.sha256` của zip, upload lại |
| `PROTOCOL.md đã đổi sau khi chốt` | Gói mã dựng trước khi sửa PROTOCOL | Dựng lại gói mã, tải version mới; **không** tắt kiểm này |
| `thiếu marker CLAUDE.md` | Gói mã không đúng | Dựng lại bằng `make_code_package.py` |
| `Thí nghiệm này cần GPU` | Accelerator = None | Bật GPU trong Settings, chạy lại |
| R0 HỎNG ở một cổng AUROC | Phiên bản scikit-learn/numpy khác | Gửi `env.json` + `gates.json`; đừng chạy tiếp |
| `pip install` thất bại | Internet = Off | Bật Internet (chỉ R2) |

## 6. Việc KHÔNG làm

- Không dán token GitHub/Kaggle hay khoá API vào notebook; không `git clone` repo private từ notebook.
- Không tải Koren/MetaDegron/Larsen/ClinVar thô lên dataset (gói dữ liệu sẽ từ chối, đừng thêm tay).
- Không sửa `PROTOCOL_SHA256` bằng tay để qua kiểm tra.
- Không chạy lại một notebook nhiều lần rồi chọn lần có kết quả thuận lợi: tiêu chí đã chốt, báo lần chạy đầu hợp lệ (trừ khi cổng R0 hỏng vì môi trường, được sửa rồi chạy lại và ghi rõ).
