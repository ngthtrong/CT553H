# Chạy notebook Kaggle v3

Hướng dẫn từng phiên, snapshot dataset, Save Version và resume: [MULTI-SESSION.md](MULTI-SESSION.md).

**Muốn dùng một notebook thay cho12 file đơn:** import [12-all-in-one.ipynb](notebooks/12-all-in-one.ipynb), chỉ gắn core data v3, bật Internet/GPU. Runner đã đóng kèm, không cần code/weights dataset riêng. Hướng dẫn cấu hình, soft budget và resume: [ALL-IN-ONE.md](ALL-IN-ONE.md). Các mục dưới đây mô tả cách dùng notebook đơn.

**Lỗi `FileNotFoundError: .../references/proteins.fasta.gz`:** nếu input đã giải nén
thành `proteins.fasta`, import lại notebook all-in-one đã sửa và restart session.
Runner mới kiểm cả dạng gzip và dạng đã giải nén bằng SHA ghim từ core ZIP gốc;
không cần sửa manifest/bỏ kiểm hash. Xem mục xử lý lỗi trong [ALL-IN-ONE.md](ALL-IN-ONE.md).

## 1. Các file cần đưa lên Kaggle

Từ repo, các ZIP nằm ở `topics/degron-footprint/data/processed/packages/`:

1. **`degron-data-v3-fullpsi.zip`**: dữ liệu lõi dùng chung cho cả 12 notebook,
   khoảng98,75MB decimal. Tạo một Kaggle Dataset riêng cho dữ liệu này.
2. **`degron-code-v3-<hash>.zip`**: code, notebook, registry revision và protocol.
   Tên chính xác/SHA trong [code-build.json](code-build.json). Tạo Kaggle Dataset
   riêng cho code; gắn đúng version mới nhất khi có sửa code.
3. Weights pLM cần thiết, hoặc bật Internet và `DOWNLOAD_WEIGHTS=True`.
   Tài sản offline giữ cấu trúc `<model_id>/status.json` và `<model_id>/<revision>/...`.
   Chỉ lấy model có `status=complete`. **Không upload `.partial` như model hoàn chỉnh.**
   Snapshot không có status/manifest của downloader sẽ không được tự đoán là đúng.

Đã có thêm **ZIP weights riêng cho ESM2-8M/35M/650M** đã kiểm SHA,
`degron-weights-v3-fd5593922ec4.zip` (khoảng2,78GB decimal); tên/SHA tại
[weights-build.json](weights-build.json). Gắn ZIP này như Kaggle input để chạy offline
các checkpoint đó. Nó không chứa17 checkpoint khác trong registry. Trạng thái tải hiện thời của toàn bộ20 model nằm trong weights-status.json.

Chưa có thao tác upload/publish trong phiên chuẩn bị này. Core data không chứa
weights/embeddings. Không gắn nhiều version code/data cùng lúc nếu muốn auto-discovery;
nếu cần, đặt `CODE_DIR` và `DATA_DIR` trỏ đúng thư mục có manifest.

Import notebook từ thư mục [notebooks/](notebooks/). Stage01 chạy CPU; stage02/03/05/06/11
dùng GPU khi chạy official. Đối với stage02 chỉ gắn/tải các model định kiểm trong phiên:

```python
SMOKE = True
INSTALL_DEPENDENCIES = True   # chỉ lần đầu nếu môi trường thiếu/sai dependency
DOWNLOAD_WEIGHTS = True       # Internet cần bật; nếu gắn weights offline thì False
SETTINGS.update(model_ids=["esm2_8m", "esm2_35m"])
```

`requirements-kaggle.txt` pin Transformers5.17.0 và các dependency cần dùng. Không thay
bản torch CUDA Kaggle bằng wheel CPU. Sau cài dependency, restart kernel nếu runtime
đã import thư viện bản cũ. Notebook ghi `env.json`; local CPU validation không xác nhận
CUDA/VRAM hoặc việc image Kaggle hiện tại có sẵn dependency đúng bản.

## 2. Smoke trước, official sau

Mỗi file mặc định **SMOKE=True**. Chạy từ cell đầu tới cuối; kiểm `status.json` và
ảnh/bảng. Smoke04/05 dùng fixture feature ngẫu nhiên; smoke11 dùng ESM2-8M và nhãn thật
để kiểm học/lưu LoRA. Không dùng bất kỳ điểm smoke nào để chọn model hoặc báo kết quả.

Để chạy thực nghiệm đủ dữ liệu, sửa cell tham số:

```python
SMOKE = False
INSTALL_DEPENDENCIES = False  # nếu môi trường đã đúng
DOWNLOAD_WEIGHTS = False     # nếu đã gắn complete weights
```

Official default seeds17/29/43, 5 grouped folds, common inner validation. Protocol
hash được kiểm trước run. Nếu hash/config/code/data đổi, dùng output directory mới;
không bỏ assert để reuse checkpoint cũ.

Output chung: `/kaggle/working/degron-v3/{smoke,official}/<stage>-<config-hash>/`.
Cell cuối tạo `<stage>-<hash>-results.zip` ở thư mục cha. Tải cả notebook đã execute,
ZIP, env/run manifest; giữ cả kết quả âm và model resource-blocked.

## 3. Thứ tự và tham số từng nhánh

**00 → 01** trước. Official00 kiểm schema/splits và tái lập hai mốc Ridge lịch sử.
Nếu không khớp, dừng và giữ `gates.json`, traceback, env; không bypass gate.
Stage01 fit mới A–E và các đối chứng, curve W5-D; xem OOF, comparisons và số peptide
đủ điều kiện thay vì chỉ nhìn AUROC. PSI cao không có event dương vẫn dùng hồi quy.

**02 → 03 → 04** cho family/scale. 02 kiểm weights/tokenizer/forward/tài nguyên,
trả `feasible` hoặc `blocked`. Các model3B/6B/15B có thể cần phần cứng lớn hơn Kaggle
session đã chọn. Runner hiện chưa sharding/offload; không tự coi hai T4 là một GPU.
Model bị chặn không được suy thành kết quả sinh học kém.

Stage03, một checkpoint/scope mỗi lượt:

```python
SETTINGS.update(
    model_id="esm2_35m",
    preflight_report="/kaggle/input/<output-02>/<02-run>/preflight.json",
    row_scope="sat", row_start=0, row_stop=None,
    crop=True, batch_size=8,
)
```

Chọn đúng đường dẫn thật sau khi gắn output02. Chỉ ESM35/shortlist cần crop; đặt
`crop=False` cho các model chỉ dùng pooled feature để tiết kiệm dung lượng. Khi chia
shard, dùng các khoảng không giao; giữ cùng model/revision/dtype/data. Ghép bằng:

```python
import sys
sys.path.insert(0, str(CODE_ROOT))
from degron_v3.plm import merge_shards
merge_shards(["/kaggle/input/<shard-a>/<run>", "/kaggle/input/<shard-b>/<run>"],
             "/kaggle/working/esm35-merged")
```

Hoặc CLI `merge_features.py --out <new-folder> <shard-a> <shard-b>`. Hàm kiểm hash,
disjoint row IDs và content identity; không ghép hai model/precision khác nhau.
Stage04 cần bundle phủ **toàn bộ sat rows** của từng model:

```python
SETTINGS["pooled_features"] = {
    "esm2_35m": "/kaggle/input/<esm35-features>/<run>",
    "esm2_650m": "/kaggle/input/<esm650-features>/<run>",
}
```

Danh sách trong notebook chỉ là cấu hình; thêm đủ checkpoint khả thi vào phép so
chung trước khi chạy. Không thêm candidate dựa trên điểm outer-test đã xem. Có thể
gộp nhiều input feature Kaggle Datasets; bundle core không cần dựng lại.

**05 — train head**:

```python
SETTINGS["crop_features"] = {"esm2_35m": "/kaggle/input/<esm35-crop>/<run>"}
SETTINGS.update(heads=["pointwise", "cnn", "mcnn"], neural_arms=["B", "D", "E"])
```

Stage05 train one-hot controls và ESM35 heads; chọn epoch inner rồi refit, lưu model
từng seed/fold. K1 là matched information control; số tham số k1/k5 được báo thực tế.

**06 — scanning/quality/transfer** dùng core, không cần pLM. Default gồm Ridge và
CNN scratch/scan-pretrain→sat-fine-tune. `scan_neural_transfer=False` chỉ chạy phần
Ridge nếu cần chia công việc thành phiên. Rep1/mean12 dùng cùng intersection cohort;
BAG6 WT không được tự thêm. T không vào pretraining.

**11 — fine-tune model pretrained cho ΔPSI**:

```python
SETTINGS.update(finetune_model="esm2_35m", finetune_modes=["frozen", "lora"],
                finetune_arms=["B", "D"], finetune_batch=8, finetune_epochs=20)
```

Default rank8 Q/V và head64, lr1e-4. LoRA cập nhật tham số attention thật; file
`*-fit.json` chứa `changed_parameters`, số trainable parameters và pinned base revision.
`*-model.pt` lưu adapter/head mới; cần base weights đúng revision khi phục hồi.
Muốn full fine-tuning ESM2-8M/35M dùng `finetune_modes=["frozen","full"]`.
Không pretrain pLM từ đầu và không tự mở full tuning model lớn.

Có thể chia GPU budget theo **arm/mode/seed**, chẳng hạn một phiên lora-D-seed17:
`finetune_modes=["lora"], finetune_arms=["D"], seeds=[17]`. Giữ nguyên epoch/grid và
protocol, chạy đủ các seed/fold còn lại; đừng diễn giải lượt một seed là ensemble3.
Mỗi phiên vẫn hoàn thành 5 folds cho seed đã chọn. Checkpoint theo epoch có resume;
nếu bị giới hạn thời gian, mang nguyên thư mục run từ output trước về **đúng OUT**
trước cell Thực hiện. Chỉ phục hồi artifact do chính pipeline tin cậy sinh ra.

**07 — calibration/refit và held transfer**:

```python
SETTINGS.update(training_output="/kaggle/input/<stage01-results>/<01-run>",
                selected_recipe="ordered-w5-D")
```

Đường dẫn là thư mục chứa `<recipe>-oof.parquet`, không phải ZIP. W5 có final refit,
calibrator/export và T score. Có thể calibration CV cho recipe family/CNN/LoRA, nhưng
final promotion tự động của các kiến trúc này chưa triển khai; không dùng model CV
như một model production duy nhất. Không đổi recipe sau khi xem held results.
Extract featureT yêu cầu `selection_lock` và model IDs đã khóa; không dùng T để tune.
Với recipe dùng pLM, đặt thêm `selected_model_ids=["<model_id>"]` trong stage07;
stage03 T đặt `row_scope="scan_T"`, `selection_lock=<selection-lock.json>` và giữ
model/preflight/feature definition đã khóa. Hiện cần tự thực hiện final refit của
head pLM trước chấm T; việc extract T không tự hoàn tất final promotion đó.

**08/09**: thiếu nguồn thật thì pending. Stage08 nhận CSV/Parquet schema
`peptide_id,wt_sequence,position_1based,mut_aa,effect,assay_id,units,source_id`, chỉ audit
endpoint/overlap; chưa tự predict external. Stage09 nhận Parquet
`peptide_id,combined_sequence,structure_source,structure_sha256,chain_residue_map`;
56 ký tự AA/3Di xen kẽ, amino-acid part phải khớp WT28. Sau review nguồn/mapping,
đặt `run_saprot=True`, `saprot_model="saprot_35m"`, `preflight_report=<02 JSON>` để
fit true/masked3Di và W5 trên cùng cohort. Cấu trúc WT giữ nguyên cho mutant là giả định.

**10** nhận `results_root` chứa các outputs đã giải nén. Chỉ nhận đúng data identity,
mode và official OOF đầy đủ. Bảng cohort cấu trúc con cần phân tích riêng, chưa trộn
với benchmark full W. Cần tập hợp đủ seed và chạy CI/ensemble đúng định nghĩa trước
kết luận; stage10 không tự biến nhiều run một seed thành ensemble3 đã được kiểm.

## 4. Dừng và tiếp tục đúng cách

- Hash/fold/tokenizer/assert sai: dừng, giữ output; sửa nguồn hoặc code có version.
- OOM: lưu blocked status/tài nguyên. Không tự giảm precision/quantization rồi reuse
  feature cũ dưới cùng tên. Đổi cấu hình cần run identity mới và kiểm preflight lại.
- Notebook mới sửa code/dependency: tạo Kaggle Dataset version code mới, reconnect,
  restart runtime; kiểm `degron_v3.__file__` trước rerun để tránh module cache cũ.
- Đầu ra `status=complete` có nghĩa stage hoàn tất theo mode; đọc thêm pending/blocked
  ở bảng kết quả. Smoke complete không có nghĩa scientific gate đã đạt.

Tái dựng local (không cần cho Kaggle): `build_dataset.py --out <new-folder>` với nguồn
repo/MMseqs; `make_notebooks.py`; `package_code.py`. Kiểm smoke đã giao bằng
`.venv/bin/python -I .../validate_notebooks.py --out <fresh-validation-folder>`;
Jupyter cần loopback socket và kernel `.venv`. Kiểm official GPU vẫn cần thực hiện
trên Kaggle, ghi runtime/environment thực tế và giữ notebook đã execute.

Tải tiếp weights ở local: chạy `download_weights.py --models all --workers 8 --backend http --small-first`
(không chạy hai job cùng đích), hoặc chọn `--models <id>`. Script resume `.partial`, pin revision,
kiểm HF hash trước khi đánh dấu complete. `weights_status.py --verify` cập nhật bản kiểm kê;
`package_weights.py --models <id1,id2>` tạo ZIP riêng chỉ từ checkpoint đã hoàn tất.
