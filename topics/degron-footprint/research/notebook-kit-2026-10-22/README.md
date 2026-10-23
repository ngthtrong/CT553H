# Bộ công cụ notebook (Kaggle / Colab) — 22/10/2026

Hạ tầng dùng chung cho mọi thí nghiệm **huấn luyện** từ đây về sau (R0, R1, R2, R3, R5 trong [next-phase-plan](../next-phase-plan-2026-10-22/README.md)). Quyết định của Trọng (22/10): dùng hạn mức miễn phí mặc định (Kaggle chính, Colab dự phòng); **Trọng tự chạy notebook và tải kết quả về**; không huấn luyện cục bộ. Hướng dẫn từng bước cho người chạy: [RUN.md](RUN.md).

Nguyên tắc `[ĐỀ XUẤT]` đã áp dụng:

- **Mã thật vẫn là file `.py` trong repo.** Notebook chỉ là lớp mỏng gọi chúng; không nhân đôi logic vào ô code.
- **Gói mã + gói dữ liệu**, ghép lại thành cây thư mục giống repo (có `CLAUDE.md` và `data/README.md` làm marker, nên các script tìm `ROOT`/`TOPIC` y như cục bộ).
- **PROTOCOL chốt bằng SHA-256 nhúng trong notebook**: sửa `PROTOCOL.md` sau khi chốt thì notebook dừng.
- **Cổng tự kiểm trước khi chạy** (R0 tái lập mốc; từng notebook tự dựng lại mốc của riêng nó nếu có).
- **Giấy phép quyết định cái gì được lên dịch vụ ngoài.** Gói dữ liệu từ chối cứng Koren 2018, MetaDegron, Larsen 2025, ClinVar thô (theo tên đường dẫn và theo trường giấy phép).

## File trong thư mục

| File | Việc |
|---|---|
| [make_data_package.py](make_data_package.py) | Dựng `data/processed/packages/degron-data-v1.zip` + `.sha256`. `--list` in danh sách, giấy phép, kích thước để duyệt **trước** khi upload; không ghi gì. Danh sách lấy từ REGISTRY trong file và từ mọi `research/*/data-needs.json` |
| [make_code_package.py](make_code_package.py) | Dựng `degron-code-<commit>[-dirty].zip` từ **working tree** (vì có thay đổi chưa commit); ghi commit, cờ dirty, SHA-256 từng file vào `CODE_MANIFEST.json`. `CLAUDE.md` và `data/README.md` trong gói chỉ là **stub** (bản thật chứa thông tin cá nhân/sổ nguồn gốc, không đi cùng gói) |
| [nbkit.py](nbkit.py) | Thư viện dùng chung cho notebook (stdlib + numpy). API ổn định, xem bên dưới |
| [nbbuild.py](nbbuild.py) | Sinh/kiểm `.ipynb` từ mã Python: `md`, `code`, `write_notebook`, `BOOTSTRAP` (ô 0 dùng chung), `validate` |
| [stamp_protocol.py](stamp_protocol.py) | `python3 -I stamp_protocol.py <nb> <PROTOCOL.md>`: ghi SHA-256 PROTOCOL vào dòng `PROTOCOL_SHA256 = "..."` |

Các gói zip nằm ở `data/processed/packages/` (gitignore). Mỗi lần mã hay PROTOCOL đổi, dựng lại gói mã và **tải lại thành phiên bản mới của dataset**.

## API `nbkit` (không đổi chữ ký)

```
detect_platform()                       -> 'kaggle' | 'colab' | 'local'
find_packages(platform, search)         -> {'code': Path|None, 'data': Path|None}   # thư mục đã giải nén HOẶC .zip
compose_workspace(code_pkg, data_pkg, ws) -> Path        # cây ghi được, idempotent; từ chối zip có đường dẫn nguy hiểm / nguồn bị cấm
verify_manifest(ws, experiment, deep)   -> dict          # SHA-256 từng file thí nghiệm cần; dừng nếu lệch
set_seeds(seed, deterministic=True)
env_report(ws)                          -> dict          # python, thư viện, GPU, commit/dirty của gói mã, SHA manifest dữ liệu
check_protocol(ws, rel_path, sha)       -> str           # dừng nếu PROTOCOL đổi sau khi chốt
class Gates: .check(name, observed, expected, tol, strict=True) / .assert_all() / .to_dict()
setup(experiment, protocol, protocol_sha256, needs, threads, seeds, require_gpu, pip) -> Context
Context: .ws .topic .research .data .out .platform .env .gates
         .path(rel) .add_to_path(*research_dirs) .save(name, obj) .finalize(files)
```

`ctx.finalize()` ghi `env.json` + `gates.json`, gom file kết quả, nén thành `<thí nghiệm>-results.zip` để tải về.

## Thêm một thí nghiệm mới

1. Tạo `research/<tên>/` với `PROTOCOL.md` (chốt trước), `run_<tên>.py` (hàm `run(ctx)`), `build_notebook.py`.
2. Nếu cần file dữ liệu ngoài REGISTRY: viết `research/<tên>/data-needs.json` (`experiment`, `files[{path, license, source}]`; chỉ giấy phép trong danh sách cho phép).
3. `python3 -I build_notebook.py` → `python3 -I ../notebook-kit-2026-10-22/stamp_protocol.py <nb> PROTOCOL.md` → `python3 -I ../notebook-kit-2026-10-22/nbbuild.py <nb>` (validate).
4. Dựng lại gói mã và gói dữ liệu (xem RUN.md bước 1).

## Kiểm cục bộ đã làm (không phải huấn luyện)

`[ĐO]` 22/10/2026, máy cục bộ: dựng hai gói; `nbkit.setup` ghép cây thư mục và khớp SHA-256 mọi file; chạy từng ô của `00-reproduce.ipynb` (ridge, ~35 giây CPU) và của `r3-domain-gate.ipynb` ở chế độ `SMOKE`. Hai notebook qua `nbformat` validate và mọi ô code qua `compile`. **Chưa chạy trên Kaggle/Colab**; những khác biệt giữa nền tảng (phiên bản thư viện, đường dẫn dataset) chỉ lộ ra ở lần chạy thật, đó là lý do R0 là bước đầu tiên.

## Giới hạn

- Hạn mức GPU, độ dài phiên, thao tác giao diện Kaggle/Colab **không được kiểm** ở đây (`[CHƯA XÁC MINH]`); RUN.md ghi những chỗ cần Trọng đối chiếu với giao diện thực.
- GPU có thể không tất định ở chữ số cuối; R0/PROTOCOL từng thí nghiệm đặt dung sai nêu trước.
- Gói mã dựng từ working tree có thay đổi chưa commit (`dirty=true` ghi trong manifest); khi chốt kết quả cuối nên commit rồi dựng lại gói để `git_commit` khớp.
