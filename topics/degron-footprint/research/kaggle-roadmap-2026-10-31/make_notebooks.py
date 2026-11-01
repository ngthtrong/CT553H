"""Generate clean runnable experiment notebooks; all research logic lives in modules."""
import hashlib
import json
from pathlib import Path

import nbformat as nbf

HERE = Path(__file__).resolve().parent

BOOT = '''import os, sys, json, hashlib
from pathlib import Path

def find_bundle(kind, explicit):
    if explicit:
        return Path(explicit).resolve()
    # Local checkout support; Kaggle uses manifest-based discovery below.
    for root in (Path.cwd(), *Path.cwd().parents):
        candidate = root / ("topics/degron-footprint/research/kaggle-roadmap-2026-10-31" if kind == "code"
                            else "topics/degron-footprint/data/processed/v3-fullpsi")
        if (candidate / ("degron_v3/stages.py" if kind == "code" else "DATA_MANIFEST.json")).is_file():
            return candidate
    marker = "CODE_MANIFEST.json" if kind == "code" else "DATA_MANIFEST.json"
    found = []
    for p in Path("/kaggle/input").rglob(marker):
        data = json.loads(p.read_text())
        if data.get("schema_version") == 3 and data.get("role") == ("trusted_code" if kind == "code" else "core_data"):
            found.append(p.parent)
    if len(found) != 1:
        raise RuntimeError(f"Expected one v3 {kind} bundle, got {found}. Set CODE_DIR/DATA_DIR explicitly.")
    return found[0]

CODE_ROOT = find_bundle("code", CODE_DIR)
DATA_ROOT = find_bundle("data", DATA_DIR)
if INSTALL_DEPENDENCIES:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(CODE_ROOT/"requirements-kaggle.txt")], check=True)
if (CODE_ROOT / "CODE_MANIFEST.json").exists():
    code_manifest = json.loads((CODE_ROOT / "CODE_MANIFEST.json").read_text())
    for item in code_manifest["files"]:
        assert hashlib.sha256((CODE_ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"], item["path"]
sys.path.insert(0, str(CODE_ROOT))
from run_stage import defaults
from degron_v3.stages import run
assert hashlib.sha256((CODE_ROOT / "EXECUTION-PROTOCOL.md").read_bytes()).hexdigest() == PROTOCOL_SHA256
config = defaults(SMOKE)
config.update(SETTINGS)
config["weight_roots"] = [str(DATA_ROOT.parents[1] / "raw/plm-weights-v3"),
    "/kaggle/input", "/kaggle/working/plm-weights-v3"]
code_parts = sorted((CODE_ROOT / "degron_v3").glob("*.py"))
config["implementation_sha256"] = hashlib.sha256(b"".join(p.read_bytes() for p in code_parts)).hexdigest()
if DOWNLOAD_WEIGHTS:
    import subprocess
    requested = config["model_ids"] if STAGE == "02" else [config["finetune_model"] if STAGE == "11" else config["model_id"]]
    if SMOKE:
        requested = ["esm2_8m"]
    subprocess.run([sys.executable, "-I", str(CODE_ROOT / "download_weights.py"),
        "--models", ",".join(requested), "--out", "/kaggle/working/plm-weights-v3",
        "--backend", "http"], check=True)
base = Path(OUTPUT_ROOT) if OUTPUT_ROOT else (Path("/kaggle/working/degron-v3") if Path("/kaggle").exists() else Path.cwd()/"degron-v3-output")
identity = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:12]
OUT = base / ("smoke" if SMOKE else "official") / (STAGE + "-" + identity)
print("Stage", STAGE, "SMOKE", SMOKE, "data", DATA_ROOT, "output", OUT)
'''

STAGES = [
 ('00', 'data-audit-and-splits', 'Audit dữ liệu, kiểm fold và tái lập mốc', {},
  'CPU. Official chạy cả legacy reproduction. Không huấn luyện model mới ở audit; stage01 trở đi có fitting.'),
 ('01', 'full-psi-and-linear-controls', 'Huấn luyện baseline và kiểm giả thuyết bỏ ngưỡng PSI', {},
  'CPU. Fit model mới cho A/B/C/D/E và đối chứng ngữ cảnh; lưu model từng fold cùng OOF.'),
 ('02', 'plm-preflight', 'Kiểm checkpoint, tokenizer và tài nguyên pLM', {},
  'GPU cho official. DOWNLOAD_WEIGHTS=True tải đúng pinned snapshot khi chưa gắn model assets. Không gửi chuỗi lên inference API.'),
 ('03', 'frozen-plm-features', 'Trích feature pLM theo model/shard',
  {'model_id':'esm2_35m','row_scope':'sat','row_start':0,'row_stop':None,'crop':True,'preflight_report':''},
  'GPU. Một model/scope mỗi phiên. Giảm ROW_STOP hoặc chia row_start/row_stop khi cần shard; model ID và dtype phải giữ nguyên khi ghép.'),
 ('04', 'plm-family-and-scale', 'Huấn luyện đầu mới để so họ/cỡ pLM', {'pooled_features':{}},
  'Gắn output feature stage03 vào POOLED_FEATURES. Smoke dùng feature fixture ngẫu nhiên có nhãn rõ, không phải kết quả pLM.'),
 ('05', 'matched-heads-and-data-regime', 'Huấn luyện pointwise/CNN/mCNN mới', {'crop_features':{}},
  'GPU. Official yêu cầu ESM35 crop bundle; one-hot là đối chứng. Smoke kiểm head bằng fixture, không suy hiệu năng thật.'),
 ('06', 'scanning-quality-and-transfer', 'Huấn luyện với replicate và chuyển nguồn scanning', {},
  'CPU/GPU. Scanning T bị loại trước fitting. Rep1 và mean12 được so trên cùng tập intersection.'),
 ('07', 'locked-transfer-and-calibration', 'Hiệu chuẩn, refit model và kiểm chuyển nguồn',
  {'training_output':'','selected_recipe':'ordered-w5-D'},
  'Đặt TRAINING_OUTPUT tới stage01/04/05/11. W5 được refit/export và chấm T; các họ khác có cross-fit calibration, cần final promotion riêng trước phục vụ.'),
 ('08', 'external-source-audit-and-evaluation', 'Audit nguồn ngoài và tính tương thích', {'external_table':None},
  'Không có bảng đã review thì ghi source_pending; không sinh dữ liệu thay thế. Không padding hoặc biến endpoint khác thành ΔPSI.'),
 ('09', 'saprot-structure-controls', 'SaProt và đối chứng cấu trúc trên cùng cohort', {'structure_table':None},
  'Không có mapping 3Di/cấu trúc thì ghi structure_pending; weights SaProt không thay thế dữ liệu cấu trúc.'),
 ('10', 'evidence-aggregation', 'Tổng hợp bằng chứng và kết quả âm', {'results_root':'/kaggle/working/degron-v3'},
  'Chỉ đọc OOF cùng data identity và mode; official không nhận smoke hoặc OOF thiếu.'),
 ('11', 'plm-finetune', 'Huấn luyện pLM mới bằng LoRA hoặc full fine-tuning',
  {'finetune_model':'esm2_35m','finetune_modes':['frozen','lora'],'finetune_arms':['B','D']},
  'GPU. LoRA cập nhật tham số attention và regression head trên ΔPSI thật. Frozen head là đối chứng. Full tuning hỗ trợ ESM2 8M/35M bằng finetune_modes=["frozen","full"]. Smoke dùng 8M và kiểm tham số đã đổi.'),
]


def main():
    out = HERE / 'notebooks'; out.mkdir(exist_ok=True)
    protocol = hashlib.sha256((HERE / 'EXECUTION-PROTOCOL.md').read_bytes()).hexdigest()
    for stage, name, title, settings, note in STAGES:
        params = '\n'.join([f'STAGE = {stage!r}', 'SMOKE = True',
            'CODE_DIR = ""', 'DATA_DIR = ""', 'OUTPUT_ROOT = ""', 'DOWNLOAD_WEIGHTS = False', 'INSTALL_DEPENDENCIES = False',
            f'PROTOCOL_SHA256 = {protocol!r}', f'SETTINGS = {settings!r}'])
        notebook = nbf.v4.new_notebook(cells=[
            nbf.v4.new_markdown_cell(f'# {stage} — {title}\n\n{note}\n\n'
                '**Chưa có kết quả official trong file này.** SMOKE chỉ kiểm hạ tầng; muốn huấn luyện đủ fold/seed đặt SMOKE=False. '
                'Lưu notebook đã chạy và output ZIP trước khi kết thúc phiên Kaggle.'),
            nbf.v4.new_markdown_cell('## Tham số\nGắn code v3 + data v3 và model/feature assets cần thiết. Chỉ bật Internet khi cần cài dependency hoặc tải weights.'),
            nbf.v4.new_code_cell(params),
            nbf.v4.new_markdown_cell('## Môi trường và provenance\nKaggle cần numpy/pandas/pyarrow/scipy/scikit-learn/torch/transformers/sentencepiece/accelerate. Xem requirements-kaggle.txt; không tự thay bản torch CUDA đang có.'),
            nbf.v4.new_code_cell(BOOT),
            nbf.v4.new_markdown_cell('## Thực hiện\nRunner lưu model mới, dự đoán, trạng thái và checkpoint tùy stage. Lỗi cổng phải được giải quyết trước lượt official.'),
            nbf.v4.new_code_cell('result = run(STAGE, DATA_ROOT, OUT, config)\ndisplay(result.head(30))'),
            nbf.v4.new_markdown_cell('## Kiểm tra và đồ thị\nHình chỉ lấy từ output vừa chạy. Không sử dụng điểm smoke trong kết luận khoa học.'),
            nbf.v4.new_code_cell('''get_ipython().run_line_magic("matplotlib", "inline")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
numeric = result.select_dtypes(include="number")
if len(result) and len(numeric.columns):
    column = "mae" if "mae" in numeric else "macro_mae" if "macro_mae" in numeric else numeric.columns[0]
    label_column = next((c for c in ["recipe", "psi_stratum", "model_id"] if c in result), None)
    labels = result[label_column].astype(str) if label_column else result.index.astype(str)
    fig, ax = plt.subplots(figsize=(10, max(3, .3*min(len(result), 30))))
    ax.barh(list(labels[:30]), result[column].iloc[:30])
    ax.set_xlabel(column + (" (ΔPSI)" if column in ["mae", "macro_mae"] else ""))
    ax.set_title(("SMOKE — " if SMOKE else "") + "Stage " + STAGE)
    fig.tight_layout(); fig.savefig(OUT / "summary.png", dpi=150); plt.show()
else:
    print("Không có metric số để vẽ; đọc trạng thái pending/blocked trong output.")'''),
            nbf.v4.new_markdown_cell('## Lưu và bước tiếp\nFile ZIP gồm kết quả stage; weights pLM gốc được quản lý riêng để tránh nhân bản các file lớn.'),
            nbf.v4.new_code_cell('''import zipfile
archive = OUT.parent / (OUT.name + "-results.zip")
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for path in sorted(OUT.rglob("*")):
        if path.is_file():
            z.write(path, path.relative_to(OUT))
print("Output:", OUT)
print("ZIP:", archive)
print("SMOKE: không dùng để báo cáo khoa học" if SMOKE else "Đọc gates/status/OOF và giữ cả kết quả âm.")''')])
        notebook.metadata.update(kernelspec=dict(name='python3', display_name='Python 3', language='python'),
                                 language_info=dict(name='python'),
                                 degron_v3=dict(stage=stage, protocol_sha256=protocol, outputs='not_executed'))
        target = out / f'{stage}-{name}.ipynb'
        nbf.validate(notebook); nbf.write(notebook, target)
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                compile(cell.source, str(target), 'exec')
        print(target.name)


if __name__ == '__main__':
    main()
