# P3 — tiền huấn luyện nhãn tile (Voutsinos) rồi tinh chỉnh ΔPSI — 22/10/2026

Tiêu chí chốt **trước khi chạy** ở [PROTOCOL.md](PROTOCOL.md); README này chỉ báo kết quả. Kết quả đầy đủ: [results.json](results.json); tóm tắt loại rò rỉ: [exclusion-summary.json](exclusion-summary.json); nhật ký chạy: [run.log](run.log). Không đổi trạng thái G2/G3, không sửa đề cương hay slide.

**[ĐO] Kết quả một dòng.** Tiền huấn luyện nhãn tile **không giúp, và làm xấu đi**: ở cấu hình chính (ext 4,0) mạng khởi tạo từ tile đạt **0,8098**, thấp hơn cả cùng mạng khởi tạo ngẫu nhiên (**0,8175**) và ridge M3 (**0,8208**); ở cấu hình phụ (base 3,0) thấp rõ rệt (**0,7726** so với 0,8009 và 0,8082). Cả hai tiêu chí A và B đều **không đạt** ở cả hai cấu hình. Kết luận theo bảng chốt trước: **"Chưa đủ bằng chứng cho lợi ích của tiền huấn luyện"**. Đúng với dự đoán tiền đăng ký §7 về chiều (A không đạt), nhưng chiều âm ở cấu hình phụ mạnh hơn dự đoán.

## 1. Thiết kế (tóm tắt, chi tiết ở PROTOCOL)

- Nguồn: 212.616 tile 30-mer / 5.302 gene (sau bỏ 42 dòng điều khiển/ký tự lạ). Nhãn `y = −degron_score`, z-score.
- Encoder: đúng `Gate` của `gate_no_pap`. Tile → 30 hàng M3 180 chiều ở chế độ chỉ-hoang-dã (`mut`=0), dự đoán tile = trung bình đầu ra trên 30 vị trí. Khởi tạo bằng khởi tạo của seed, nên nhánh `rand` và `pre` **bắt đầu cùng điểm**; tinh chỉnh giống hệt nhau (lưới lr {2×10⁻³, 5×10⁻⁴} chọn bằng MSE inner validation).
- Chống rò rỉ, riêng từng outer fold, **trước** mọi bước học: loại cả gene nếu MMseqs2 (id≥0,30, alnlen≥50), 12-mer hoặc tên gene chạm protein của cụm outer-test.

## 2. Cổng tự kiểm đã qua `[ĐO]`

- 5 fold trùng khớp `folds` của G2; `tile_feats` khớp `derisk.featurize` trên một 28-mer ngẫu nhiên (trừ khối `mut`); mỗi fold có `assert` không còn gene bị loại trong tập tiền huấn luyện.
- Tái lập (ensemble ba seed): ridge **0,8082 / 0,8208** (base / ext) khớp tuyệt đối; `gate_no_pap` lr 2×10⁻³ **0,8016 / 0,8154** so với mốc 0,8015 / 0,8154 (lệch 1×10⁻⁴ ở base, trong ngưỡng 5×10⁻⁴).

## 3. Loại rò rỉ `[ĐO]`

Hợp ba luật trên cả 89 cụm test: **550 gene / 31.286 tile** (MMseqs2 503 gene, 12-mer 182, tên gene 55). Số bị loại từng fold, **không đều**:

| Fold | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| Gene loại | 318 | 34 | 176 | 99 | 44 |
| Tile loại | 17.613 | 2.430 | 9.893 | 5.372 | 3.029 |

`[DIỄN GIẢI]` Fold 0 mất nhiều gene vì cụm test chứa các họ có nhiều paralog trong thư viện Voutsinos. Luật MMseqs2 không đặt ngưỡng phủ nên chặt hơn định nghĩa cụm cov80; đây là lựa chọn thiên về an toàn và đã chốt trước. Phần còn lại ≥ 175.000 tile mỗi fold cho tiền huấn luyện. Tiền huấn luyện **học được** nhiệm vụ của nó: Pearson trên 10% gene giữ riêng là **0,864** (khoảng 0,857–0,868 qua 15 lần), dừng ở epoch 7–10.

## 4. Kết quả `[ĐO]`

AUROC mức ô, macro theo peptide, điểm ensemble ba seed (trong ngoặc: từng seed 17 / 29 / 43).

| Cấu hình | ridge M3 | `rand` | `pre` |
|---|---:|---:|---:|
| **ext 4,0 (chính)** | **0,8208** (0,8204 · 0,8210 · 0,8209) | 0,8175 (0,8150 · 0,8138 · 0,8067) | 0,8098 (0,7971 · 0,7879 · 0,7946) |
| base 3,0 (phụ) | 0,8082 (0,8062 · 0,8068 · 0,8081) | 0,8009 (0,7899 · 0,7863 · 0,7870) | 0,7726 (0,7604 · 0,7518 · 0,7444) |

| Cấu hình | Phép so | Delta | CI 95% theo cụm | Delta từng seed | Đạt? |
|---|---|---:|---|---|:--:|
| ext | A: `pre` − `rand` | −0,0077 | [−0,0163; +0,0006] | −0,018 · −0,026 · −0,012 | Không |
| ext | B: `pre` − ridge | −0,0110 | [−0,0197; −0,0024] | −0,023 · −0,033 · −0,026 | Không |
| base | A: `pre` − `rand` | −0,0283 | [−0,0426; −0,0149] | −0,029 · −0,034 · −0,043 | Không |
| base | B: `pre` − ridge | −0,0356 | [−0,0509; −0,0215] | −0,046 · −0,055 · −0,064 | Không |

Mô tả (không dùng để quyết định):

- `pre` âm ở **cả ba seed, cả hai cấu hình, cả hai phép so**. Ở ext, CI của A chỉ chạm 0 từ phía âm; ở B và ở base thì CI nằm trọn dưới 0.
- lr được chọn: `rand` chọn 5×10⁻⁴ ở 13/15 lần, `pre` chọn 2×10⁻³ ở 11/15 (ext) và 13/15 (base). Epoch tốt nhất trung bình: `rand` 10,2 (ext) / 12,9 (base); `pre` **27,4** / **29,5**. Mạng tiền huấn luyện học lâu hơn ba lần mà ra kết quả kém hơn.
- Trên lưới lr cố định (ensemble ba seed), `pre` vẫn thua `rand`: ext 0,8074 / 0,8041 so với 0,8154 / 0,8174; base 0,7744 / 0,7734 so với 0,8016 / 0,8010 (lr 2×10⁻³ / 5×10⁻⁴). Kết quả không do lưới lr.
- Thêm nhãn nới ngưỡng (P0) vẫn giúp `rand` (0,8009 → 0,8175 với lưới lr này) nhưng không cứu `pre`.

## 5. Diễn giải `[DIỄN GIẢI]`

- **Không có bằng chứng cho lợi ích của tiền huấn luyện nhãn tile theo thiết kế này**, và có bằng chứng nó gây hại ở bộ nhỏ (base). Cách đọc hợp lý nhất: tiền huấn luyện đưa `Gate` về một vùng trọng số tối ưu cho *"residue ở ngữ cảnh nào thì tile là degron"*, nơi `wt` và ngữ cảnh làm hầu hết việc và khối `mut` không được học. Tinh chỉnh trên ΔPSI cần phép thay là biến chính, nên điểm khởi đầu này kém điểm khởi đầu ngẫu nhiên.
- Tiền huấn luyện không hỏng (Pearson 0,864 trên gene giữ riêng): lỗi nằm ở **chuyển giao**, không ở tiền huấn luyện. Phù hợp với khoảng cách qua assay đã đo 0,0773 AUROC ([reframe §9](../reframe-options-2026-10-15/README.md)).
- Khoảng cách lớn hơn ở base (−0,028) so với ext (−0,008) hợp với cách đọc "điểm khởi đầu xấu thì ít nhãn càng khó sửa", nhưng đây là diễn giải, chưa có thí nghiệm tách.
- **Không** kết luận "giám sát yếu từ tile vô ích": chỉ kết luận thiết kế *tiền huấn luyện chỉ-hoang-dã + tinh chỉnh toàn bộ* không chuyển giao. Các thiết kế khác (đóng băng encoder, tiền huấn luyện đa nhiệm với ΔPSI, dùng 17.820 trình tự dùng chung hai assay làm cầu nối) **chưa thử** và không được phép suy ra từ kết quả này.

## 6. Giới hạn

- `[ĐO]` Benchmark phát triển OOF, không phải kiểm chứng ngoài độc lập; chỉ một thiết kế tiền huấn luyện, một encoder, hai lr.
- `[ĐO]` Loại rò rỉ chặt (cả gene, local hit id≥30%). Có thể làm tiền huấn luyện yếu hơn so với không loại, nhưng đó là hướng an toàn; không có phép đo "nếu không loại thì sao" vì sẽ rò rỉ.
- `[ĐO]` Nhánh `rand` ở ext với lưới lr (0,8175) khác con số 0,8154 của learning-curve (chỉ lr 2×10⁻³). Mọi phép so A đều giữa hai nhánh **cùng lưới lr**; ridge so ở B không có lưới. Số 0,8154 vẫn được tái lập (cổng 2).
- `[ĐO]` Hai lr là lựa chọn của người viết; lưới lr cố định cho thấy kết luận không đổi (mục 4).

## 7. Dựng lại

```bash
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I topics/degron-footprint/research/pretrain-p3-2026-10-22/build_exclusion.py   # ~2,5 phút
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I topics/degron-footprint/research/pretrain-p3-2026-10-22/run_p3.py            # ~34 phút, 4 thread torch
```

Chạy lại tiếp tục từ `data/processed/p3-progress.pkl`. Lineage file: [data/README](../../data/README.md). Cần chạy `run_curve.py` (learning-curve) trước để có cache `learning-curve-sat-{base,ext4.0}.npz` và `results.json`.
