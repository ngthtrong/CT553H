"""Generate one self-contained Kaggle notebook with reviewed v3 runner sources embedded."""
import base64
import hashlib
import io
import json
from pathlib import Path
import zipfile

import nbformat as nbf

HERE = Path(__file__).resolve().parent

PARAMETERS = '''# Chỉ cần gắn dataset degron-data-v3-fullpsi; code đã có trong notebook.
SMOKE = True
INSTALL_DEPENDENCIES = True
AUTO_DOWNLOAD = True
DATA_DIR = ""                  # tự tìm đúng DATA_MANIFEST nếu để trống
OUTPUT_ROOT = ""               # mặc định /kaggle/working/degron-v3-all
EXTRA_WEIGHT_ROOTS = []        # tùy chọn: weights đã gắn từ Kaggle Input

# SMOKE luôn dùng ESM2-8M thật; official mặc định ESM2-35M.
MODEL_IDS = ["esm2_35m"]       # hoặc "all" để lập kế hoạch mọi sequence family/scale
FINETUNE_MODEL = "esm2_35m"
CALIBRATION_TASK = "01"       # task chứa recipe đã khóa; default ordered-w5-D
SECTIONS = None               # None: toàn luồng; ví dụ ["00", "01"] cho một phiên
OVERRIDES = {}                # ví dụ {"11": {"finetune_modes": ["frozen", "lora"]}}

RESUME_FROM = ""              # thư mục campaign hoặc *-checkpoint.zip của version trước
MAX_NEW_TASKS = None          # ví dụ 3: chạy tối đa 3 job mới, rồi xuất trạng thái
SESSION_HOURS = 8.0           # soft limit: kiểm giữa các job, không ngắt job đang chạy
MAX_OUTPUT_GIB = 16.0         # soft budget cho outputs + weights tải trong phiên
EXPORT_FEATURES_IN_ZIP = False  # False: ZIP nhỏ; feature vẫn nằm trong output directory

EXTERNAL_TABLE = None
STRUCTURE_TABLE = None
RUN_SAPROT = False            # cần bảng cấu trúc/mapping đã review và official mode
SAPROT_MODEL = "saprot_35m"
'''

BOOTSTRAP = '''import base64, hashlib, io, json, os, sys, zipfile
from pathlib import Path

payload = base64.b64decode(EMBEDDED_RUNNERS)
assert hashlib.sha256(payload).hexdigest() == EMBEDDED_SHA256
base = Path(OUTPUT_ROOT) if OUTPUT_ROOT else (Path("/kaggle/working/degron-v3-all") if Path("/kaggle").exists() else Path.cwd()/"degron-v3-all")
CODE_ROOT = base/"code"/EMBEDDED_SHA256[:16]
CODE_ROOT.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(io.BytesIO(payload)) as archive:
    manifest = json.loads(archive.read("EMBEDDED-MANIFEST.json"))
    for entry in manifest["files"]:
        relative = Path(entry["path"])
        assert not relative.is_absolute() and ".." not in relative.parts
        data = archive.read(entry["path"])
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
        target = CODE_ROOT/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert hashlib.sha256(target.read_bytes()).hexdigest() == entry["sha256"]
        else:
            target.write_bytes(data)
    (CODE_ROOT/"EMBEDDED-MANIFEST.json").write_text(json.dumps(manifest, indent=2))

if DATA_DIR:
    DATA_ROOT = Path(DATA_DIR).resolve()
else:
    local = [p/"topics/degron-footprint/data/processed/v3-fullpsi" for p in (Path.cwd(), *Path.cwd().parents)]
    local = [p for p in local if (p/"DATA_MANIFEST.json").is_file()]
    if local:
        DATA_ROOT = local[0]
    else:
        matches = []
        for path in Path("/kaggle/input").rglob("DATA_MANIFEST.json"):
            item = json.loads(path.read_text())
            if item.get("schema_version") == 3 and item.get("role") == "core_data": matches.append(path.parent)
        assert len(matches) == 1, f"Set DATA_DIR to one core v3 bundle; found {matches}"
        DATA_ROOT = matches[0]

if INSTALL_DEPENDENCIES:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(CODE_ROOT/"requirements-kaggle.txt")], check=True)
sys.path.insert(0, str(CODE_ROOT))
# A fresh Save & Run All session avoids imported modules from an older embedded bundle.
import degron_v3
assert Path(degron_v3.__file__).resolve().parent == CODE_ROOT/"degron_v3", "Restart kernel after changing embedded code"
from degron_v3.pipeline import Pipeline

weight_roots = list(EXTRA_WEIGHT_ROOTS)
for ancestor in (Path.cwd(), *Path.cwd().parents):
    candidate = ancestor/"topics/degron-footprint/data/raw/plm-weights-v3"
    if candidate.is_dir(): weight_roots.append(str(candidate))
pipeline = Pipeline(DATA_ROOT, base, smoke=SMOKE, model_ids=MODEL_IDS,
    sections=SECTIONS, overrides=OVERRIDES, weight_roots=weight_roots, auto_download=AUTO_DOWNLOAD,
    resume_from=RESUME_FROM, max_tasks=MAX_NEW_TASKS, max_hours=SESSION_HOURS,
    max_output_gib=MAX_OUTPUT_GIB, external_table=EXTERNAL_TABLE, structure_table=STRUCTURE_TABLE,
    run_saprot=RUN_SAPROT, saprot_model=SAPROT_MODEL, finetune_model=FINETUNE_MODEL,
    calibration_task=CALIBRATION_TASK)
# Kaggle expands an uploaded checkpoint ZIP into a directory. Preserve its imported
# control index under a different name so export() writes one fresh SNAPSHOT.json.
# This is archive bookkeeping only: embedded runners and scientific plan stay unchanged.
imported_index = pipeline.root/"SNAPSHOT.json"
if imported_index.is_file():
    content = imported_index.read_bytes()
    preserved = pipeline.root/"resume-indexes"/(hashlib.sha256(content).hexdigest()+".json")
    preserved.parent.mkdir(parents=True, exist_ok=True)
    if preserved.exists():
        assert preserved.read_bytes() == content
        imported_index.unlink()  # identical metadata remains preserved
    else:
        imported_index.rename(preserved)
print("Data:", DATA_ROOT)
if pipeline.ds.decompressed_files:
    print("Verified expanded gzip members:", pipeline.ds.decompressed_files)
print("Campaign:", pipeline.root)
print("Mode:", pipeline.plan["mode"], "Models:", pipeline.models)
display(pipeline.summary())
'''

NOTES = [
 ('00', 'Audit dữ liệu và tái lập mốc', 'Official kiểm historical reproduction; lỗi hash/fold/nhãn phải dừng.'),
 ('01', 'Huấn luyện Ridge mới và kiểm full-PSI', 'A–E, đối chứng pair/composition/unordered/ordered; learning curve W5 theo nhóm.'),
 ('02', 'Weights và preflight pLM', 'Tự tải checkpoint còn thiếu; kiểm ngân sách trước tải. Chỉ model qua preflight mới được trích feature.'),
 ('03', 'Trích feature theo model', 'Tự nhận preflight, dùng crop cho ESM35 anchor. Smoke trích12 ô với ESM8M thật.'),
 ('04', 'Huấn luyện head so family/scale', 'Tự nhận pooled features đầy đủ. Smoke dùng fixture, không phải benchmark pLM thật.'),
 ('05', 'Huấn luyện pointwise/CNN/mCNN', 'Tự nhận ESM35 crop. Official chia job theo head/arm/seed để tiếp tục nhiều phiên.'),
 ('06', 'Replicate, quality và scanning transfer', 'Ridge và CNN scratch/pretrain→fine-tune; không dùng scan_T để train.'),
 ('11', 'Fine-tune pLM mới bằng LoRA', 'Frozen comparator + LoRA Q/V/head. Official chia job theo mode/arm/seed; smoke train ESM8M thật.'),
 ('08', 'Nguồn ngoài', 'Không có EXTERNAL_TABLE thì source_pending. Có bảng thì audit; không tự đổi endpoint thành ΔPSI.'),
 ('09', 'Cấu trúc và SaProt', 'Không có STRUCTURE_TABLE thì structure_pending. True/masked3Di cần mapping thật và RUN_SAPROT=True.'),
 ('07', 'Khóa recipe, calibration và transfer', 'Chờ các job development đã lập kế hoạch hoàn tất. Mặc định W5-D; final promotion tự động hiện chỉ có W5.'),
 ('10', 'Tổng hợp kết quả và coverage', 'Gộp đúng recipe/cohort/seed, tách full W khỏi cohort cấu trúc/smoke. Không tự chọn model theo điểm outer-test.'),
]


def main():
    files = sorted((HERE/'degron_v3').glob('*.py'))+[HERE/p for p in
        ('run_stage.py', 'download_weights.py', 'model-registry.json', 'EXECUTION-PROTOCOL.md', 'requirements-kaggle.txt',
         'degron_v3/gzip-content-hashes.json')]
    manifest = dict(schema_version=1, role='reviewed_embedded_code',
        files=[dict(path=p.relative_to(HERE).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files])
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in files:
            # Fixed timestamps make the embedded source identity deterministic.
            info = zipfile.ZipInfo(p.relative_to(HERE).as_posix(), (2026, 11, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, p.read_bytes())
        info = zipfile.ZipInfo('EMBEDDED-MANIFEST.json', (2026, 11, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, json.dumps(manifest, sort_keys=True))
    content = data.getvalue(); checksum = hashlib.sha256(content).hexdigest()
    cells = [
        nbf.v4.new_markdown_cell('# Degron v3 — một notebook điều phối toàn bộ thực nghiệm\n\n'
            'Chỉ cần **dataset core v3 + Internet + GPU** khi chạy nhánh model. Mã runner được đóng kèm, kiểm SHA trước sử dụng; không cần dataset code/weights riêng. '
            '**SMOKE=True** là mặc định. Có huấn luyện Ridge/CNN và fine-tune pLM bằng LoRA; không pretrain pLM từ đầu.\n\n'
            'Một notebook có thể chạy qua nhiều Save Versions. Gộp file không làm mọi model/fold/seed vừa một phiên Kaggle. '
            'Job thiếu tài nguyên/nguồn phải được báo rõ. Source ngoài và cấu trúc vẫn cần input thật; phạm vi/giới hạn giữ như12 notebook gốc.'),
        nbf.v4.new_markdown_cell('## 1. Tham số\nChọn SECTIONS và MAX_NEW_TASKS theo phiên; giữ nguyên MODEL_IDS/OVERRIDES khi resume cùng campaign. '
            'Official mặc định35M và toàn protocol; MODEL_IDS="all" có model rất lớn, không bảo đảm tải/chạy vừa phiên. '
            'SESSION_HOURS chỉ kiểm giữa job, không bảo đảm job nặng dừng trước giới hạn Kaggle.'),
        nbf.v4.new_code_cell(PARAMETERS),
        nbf.v4.new_markdown_cell('## 2. Mã runner đi kèm\nPayload chỉ chứa mã nghiên cứu đã review, registry và dependency/protocol. '
            'Không chứa dữ liệu nhãn hoặc weights. Có thể xem các `.py` đã giải nén ở CODE_ROOT; không chạy remote model Python.'),
        nbf.v4.new_code_cell(f'EMBEDDED_SHA256 = {checksum!r}\nEMBEDDED_RUNNERS = {base64.b64encode(content).decode()!r}'),
        nbf.v4.new_markdown_cell('## 3. Chuẩn bị và lập kế hoạch\nTự tìm core data, kiểm source SHA, cài dependency và xác định campaign theo data/code/plan. '
            'Khi không có weights local/input, AUTO_DOWNLOAD=True tải đúng model; không gửi sequence qua API inference.'),
        nbf.v4.new_code_cell(BOOTSTRAP),
    ]
    for section, title, note in NOTES:
        cells += [nbf.v4.new_markdown_cell(f'## {section} — {title}\n{note}'),
                  nbf.v4.new_code_cell(f'display(pipeline.run_group({section!r}))')]
    cells += [
        nbf.v4.new_markdown_cell('## Báo cáo\nBảng trạng thái cho biết đã làm gì và còn gì pending. Biểu đồ smoke chỉ kiểm luồng; không dùng chọn model. '
            'Feature được kiểm/cache bằng hash; nhiệm vụ hoàn tất sẽ được bỏ qua khi resume đúng campaign.'),
        nbf.v4.new_code_cell('''display(pipeline.summary())
evidence = pipeline.aggregate()
display(evidence.head(30))
get_ipython().run_line_magic("matplotlib", "inline")
import matplotlib.pyplot as plt
if len(evidence):
    fig, ax = plt.subplots(figsize=(11, max(4, .32*min(len(evidence), 30))))
    shown = evidence.head(30)
    labels = shown.recipe + " [" + shown.cohort + "]"
    ax.barh(labels, shown.macro_mae)
    ax.set_xlabel("Peptide-macro MAE (ΔPSI)")
    ax.set_title(("SMOKE — " if SMOKE else "") + "Separate recipe/cohort rows; see n_seeds")
    fig.tight_layout(); fig.savefig(pipeline.root/"summary.png", dpi=140); plt.show()
else:
    print("Chưa có OOF; xem tasks pending/blocked và session_stop_reason.")'''),
        nbf.v4.new_markdown_cell('## Save Version và chạy tiếp\n'
            'Lần đầu: bật Internet/GPU rồi **Save Version → Save & Run All**. '
            'Lần sau: gắn output version trước, đặt RESUME_FROM tới thư mục campaign có pipeline-manifest.json (giữ cả feature), '
            'hoặc checkpoint ZIP. Giữ OUTPUT_ROOT mặc định và toàn bộ cấu hình khoa học; đổi SECTIONS/MAX_NEW_TASKS được phép. '
            'Weights tải về nằm riêng ngoài ZIP, có thể dùng lại từ output đã gắn. ZIP mặc định bỏ pool/crop để tránh nhân đôi feature; '
            'restore ZIP sẽ trích lại các feature thiếu. Không bỏ assert khi code/data/plan khác. '
            'Nếu upload checkpoint ZIP thành Dataset để resume nhiều phiên, đặt EXPORT_FEATURES_IN_ZIP=True để giữ feature; '
            'SNAPSHOT.json do Kaggle giải nén được giữ trong resume-indexes để ZIP phiên sau có đúng một chỉ mục mới. '
            'Nếu đang có campaign local, để RESUME_FROM="" để dùng cache local. Full directory cũng được giữ trong Kaggle output. '
            'Quick Save sau chạy tay cần bật lưu output files. Chưa có phép đo official trong notebook sạch này.'),
        nbf.v4.new_code_cell('export_result = pipeline.export(include_features=EXPORT_FEATURES_IN_ZIP)\ndisplay(export_result)\nprint("Campaign:", pipeline.root)\nprint("State:", pipeline.root/"pipeline-manifest.json")'),
    ]
    nb = nbf.v4.new_notebook(cells=cells, metadata=dict(
        kernelspec=dict(name='python3', display_name='Python 3', language='python'),
        language_info=dict(name='python'), degron_v3=dict(kind='all_in_one', embedded_sha256=checksum)))
    nbf.validate(nb)
    for cell in nb.cells:
        if cell.cell_type == 'code': compile(cell.source, 'all-in-one', 'exec')
    path = HERE/'notebooks/12-all-in-one.ipynb'
    nbf.write(nb, path)
    print(path.name, 'embedded bytes', len(content), 'sha256', checksum)


if __name__ == '__main__':
    main()
