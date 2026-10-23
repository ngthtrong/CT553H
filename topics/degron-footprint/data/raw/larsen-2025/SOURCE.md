# Nguồn gốc — bộ nhân Larsen 2025 (`larsen-2025/`)

Tải **15/10/2026** theo C-10, chấp nhận ở D-028 mục 6.

## Xuất xứ

| | |
|---|---|
| Repo | https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors |
| Tag ghim | **`v1.0`** · commit `2698ecc6bc9933ad167477ab3ad40e5677eba39a` |
| Giấy phép | **MIT** — xem [LICENSE](LICENSE) (bản sao giữ nguyên trong thư mục này) |
| DOI Zenodo | [10.5281/zenodo.20490355](https://doi.org/10.5281/zenodo.20490355) — ⚠ Zenodo **trả 403 từ mạng này**, nên tải qua GitHub và trích DOI |
| Bài báo | Larsen và cộng sự, *Comprehensive degron mapping in human transcription factors*; bản preprint bioRxiv 2025.05.16.654404 ở **CC BY-NC-ND** — **dữ liệu không nằm sau giấy phép đó**, nó nằm trong repo MIT |
| Ngày tải | 15/10/2026 |

**Thông báo MIT bắt buộc giữ kèm:** Copyright (c) 2025 Linderstrøm-Lang Centre for Protein Science,
University of Copenhagen. Toàn văn trong [LICENSE](LICENSE).

⚠ **Chỗ mơ hồ pháp lý còn lại** (C-11a, D-028 mục 7): MIT nominally là giấy
phép **phần mềm** và deposit Zenodo đăng ký loại `Software`, nên về nguyên tắc có thể tranh luận MIT trao cho
script chứ không cho file `.csv.gz`. Lập luận phản lại mạnh hơn: `LICENSE` ở gốc repo **không có ngoại lệ**, và
README của repo gọi chính các file CSV là *"the main resulting data"*. **Đang chờ** một email xác nhận của tác giả.

## Danh mục file

| File | SHA-256 | Mô tả |
|---|---|---|
| `transfac_tiles.csv.gz` | `0c31057daeaaedde4b4a8aafa5d6d03035623f197aff0f277273322e04da2a2f` | 5.771.779 byte. **63.258 dòng dữ liệu** (21 cột) |
| `LICENSE` | — | Bản sao thông báo MIT |

**Không có script nào trong repo này tạo ra hai file trên** — chúng được `cp` nguyên vẹn từ bản `git clone`.

## Các trường đã dùng

`name` (ENSG_tileNNNN) · `gene` · `first_resi`/`last_resi` · `aa` (tile **30-aa, bước 15**) · `lib` · `zf` ·
`n` (số lần đo) · **`degron_score`/`degron_std`** · `abundance_score`/`abundance_std` · **`pap`**, `pap_ct`
(điểm PAP do tác giả tính) · `locnes`/`locnes_score` · **`tile_rasa_median`**, **`tile_plddt_median`**.

⚠ **Thang PSI của bộ này đảo chiều và chuẩn hoá lại so với GPS của Zhang** (sort-seq abundance reporter, 4
cổng, so với GPS 6 bin) — **không** so trực tiếp con số giữa hai bộ mà không chuẩn hoá.

## Audit khi tải (15/10/2026)

| Đại lượng | Giá trị |
|---|---:|
| Dòng dữ liệu | **63.258** |
| Tile có `degron_score` + `degron_std` | **59.016** |
| Gene (TF) | **1.627** |
| **Độ tin cậy `degron_score`** (từ sai số từng tile) | **0,9701** → trần r = **0,9849** |
| Tile có `tile_rasa_median` | 52.441 (88,9%) |
| **rASA** trung vị · SD · khoảng | **0,6900** · **0,2334** · 0,000–1,000 |
| Tỉ lệ tile có rASA > 0,7 | **0,4936** |
| pLDDT trung vị · SD | 56,20 · 24,45 |
| **Pearson(`pap`, `degron_score`)** | **−0,7899** |

**Hai kết luận của lần audit này:**

1. **Mốc PAP 0,79 do tác giả báo đã được tái lập độc lập** — |−0,7899| khớp bốn chữ số. Dấu âm vì
   `degron_score` ngược chiều PAP.
2. **Đây là chỗ duy nhất rASA/pLDDT có phương sai thật** (SD 0,2334; gần một nửa tile có rASA > 0,7), khác
   hẳn tập huấn luyện chính của đề tài, nơi mọi peptide 28-mer đều phơi lộ như nhau nên tham số cổng phơi lộ
   **không nhận diện được** (C-8, D-028 mục 1).
3. **Số 63.258 không khớp bất kỳ con số nào in trong bài** (58.781 / 58.992 / 62.992 / 63.011 / 63.230) —
   bài **không nhất quán với chính nó**. Khi trích phải dùng **số đếm được từ file**, kèm ghi chú.

## Dựng lại

```bash
git clone --depth 1 --branch v1.0 \
  https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors <tmp>
cp <tmp>/annotations/transfac_tiles.csv.gz <tmp>/LICENSE \
  topics/degron-footprint/data/raw/larsen-2025/
```
