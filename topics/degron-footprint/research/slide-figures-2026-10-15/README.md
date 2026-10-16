# Hình sinh từ dữ liệu cho bộ slide 16/10/2026

> Việc số 2 trong bảng "Việc phải làm trước khi dựng slide" của
> [slide-content-2026-10-15.md](../../presentation/slide-content-2026-10-15.md): **slide 16 cần một ví dụ
> ma trận 28×20 sinh từ dữ liệu, không được đặt số minh họa vào**.
>
> **Nhãn bằng chứng: tự đo.** Không có mô hình nào tham gia; đây là **nhãn thực nghiệm** đã dựng lại từ
> read thô của Zhang et al. 2023.

## Chạy

```bash
.venv/bin/python topics/degron-footprint/research/slide-figures-2026-10-15/make_example_matrix.py \
  --out-svg topics/degron-footprint/presentation/deck-2026-10-16/figures/example-matrix.svg
```

Đầu ra: [`example-matrix.json`](example-matrix.json) (số liệu + xuất xứ) và, nếu đưa `--out-svg`, một heatmap
28×20 kèm bar per-position cho [deck-2026-10-16](../../presentation/deck-2026-10-16/README.md).

Script nạp dữ liệu qua đúng bộ nạp dùng chung
[`residue-task-derisk-2026-10-15/residue_data.py`](../residue-task-derisk-2026-10-15/residue_data.py),
nên các ngưỡng (`reads ≥ 10`, degron nếu `PSI_WT ≤ 3,0`, ô dương nếu `ΔPSI ≥ 1,0`) khớp với mọi con số đã
công bố nội bộ của đề tài.

## Quy tắc chọn peptide — cố định, không chọn tay

1. chỉ peptide degron của **bộ bão hòa**;
2. phải đo đủ **≥ 500 ô** trong tổng 28×19 ô khác WT;
3. xếp theo **số ô dương** giảm dần, hoà thì lấy id nhỏ nhất;
4. lấy phần tử đầu.

## Kết quả hiện tại

| | |
|---|---|
| Peptide | `Q16665_HIF1A_25` |
| Trình tự | `QDTDLDLEMLAPYIPMDDDFQLRSFDQL` — residue **553–580** của HIF1A |
| PSI hoang dã (WT nội tại, trung bình hai nửa) | **2,186** ⇒ là degron |
| Ô đo được / ô dương | **529** / **186** |
| Dải ΔPSI | −0,515 … **+3,107** |
| Cụm protein | `Q16665`, **có** trong bộ quét |

**Footprint đo được nằm ở vị trí 10–14** (`L-A-P-Y-I`, tức residue 562–566), mạnh nhất ở vị trí 11–14
(ΔPSI trung bình 2,07–2,19) và vị trí 12 có **19/19** thay thế đều làm bền. Vị trí 23 (`R`) là đối chứng âm
tự nhiên: ΔPSI trung bình **−0,31**.

⚠ **Mắt nối tới y văn là tra cứu, không phải kết quả của đề tài.** Vị trí 10–12 là `L562-A563-P564` — lõi
**LXXLAP** của HIF1A, mà **P564** là vị trí hydroxyl hóa proline được E3 ligase **VHL** nhận diện
(Yu et al., *PNAS* 2001, [PMID 11504942](https://pubmed.ncbi.nlm.nih.gov/11504942/)). Nghĩa là nhãn đo được
**tái hiện một vị trí degron kinh điển** mà assay không hề được cho biết trước. Trên slide phải gắn nhãn
`literature cross-check`, **không** trình bày như phát hiện mới.

ℹ Chọn HIF1A là có chủ ý: theo [D-035](../../../../DECISIONS.md#d-035) nó là degron **duy nhất** trong 8 degron
lái ung thư kinh điển **hiện ra** trong assay. Dùng nó làm ví dụ **không** đồng nghĩa quay lại mạch dẫn
"đột biến lái ung thư" — mạch đó đã bị bỏ.

## Về train/test

Brief yêu cầu "chọn peptide trong tập train". Trong thiết kế hiện hành — học trục ngữ cảnh trên **bộ quét**,
xác nhận ma trận trên **bộ bão hòa** ([D-031](../../../../DECISIONS.md#d-031)) — thì **cả 91 peptide bão hòa đều
nằm phía đánh giá**; không tồn tại peptide bão hòa "trong tập train". Script vì vậy **ghi rõ trạng thái split**
trong JSON thay vì giả định một tập train không có thật.

Điều này **không gây rò rỉ**: slide 16 chỉ hiện **nhãn đo được**, không có đầu ra mô hình. Caption trên slide
nói đúng như vậy. Khi nào có mô hình và muốn vẽ **dự đoán** cho một peptide, phải chọn lại theo split thật.

## Xuất xứ

`example-matrix.json` ghi SHA-256 của `data/processed/psi-sat_a.tsv` và `psi-sat_b.tsv`, các ngưỡng, quy tắc
chọn và số peptide bão hòa tại thời điểm chạy. Dựng lại hai file đầu vào đó:
[full-data-audit §10](../full-data-audit/README.md) (`build_psi.py --condition all --validate`).
