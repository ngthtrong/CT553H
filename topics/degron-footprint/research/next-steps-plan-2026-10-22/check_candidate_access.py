#!/usr/bin/env python3
"""Kiểm truy cập các endpoint dữ liệu ứng viên cho kế hoạch 22/10/2026.

Chỉ gửi HEAD (fallback GET 1 byte), KHÔNG tải payload, KHÔNG gửi chuỗi của đề tài
lên server. Mục đích duy nhất: ghi lại HTTP status / content-type / content-length
để nhãn truy cập trong README là [ĐO] chứ không phải phỏng đoán.

Chạy từ gốc repo:  .venv/bin/python -I topics/degron-footprint/research/next-steps-plan-2026-10-22/check_candidate_access.py
"""
import json
import pathlib
import socket
import urllib.error
import urllib.request
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
UA = "degron-footprint-thesis/1.0 (academic access check; mailto:ngthtrong204@gmail.com)"
TIMEOUT = 30

# (khóa, nhãn, url). URL là trang/endpoint công bố dữ liệu, không phải trang bài báo.
TARGETS = [
    ("koren2018_cell",      "Koren 2018 Cell — trang bài + supplementary (GPS C-degron, saturation)",
     "https://www.cell.com/cell/fulltext/S0092-8674(18)30521-X"),
    ("koren2018_pmc",       "Koren 2018 — bản PMC (đường vòng nếu Cell chặn), PMID 29779948",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC6003881/"),
    ("timms2023_cdegron",   "Timms 2023 Mol Cell — C-degron ubiquitin-independent, PSI GPS-ORFeome",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC10237035/"),
    ("ndegron_jcb2024",     "JCB 2024 — DPP + N-degron, N24mer saturation, ΔPSI",
     "https://rupress.org/jcb/article/223/8/e202311035/276811/"),
    ("ndegron_jcb2024_pmc", "Shimshon 2024 JCB — bản PMC, PMID 38874443",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC11178506/"),
    ("ncys_pnas2025",       "Bekturova 2025 PNAS — N-terminal cysteine, N-terminome library",
     "https://www.pnas.org/doi/10.1073/pnas.2501681122"),
    ("ncys_pnas2025_pmc",   "Bekturova 2025 PNAS — bản PMC, PMID 40794836",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC12377780/"),
    ("glue_biorxiv2026",    "bioRxiv 09/2026 — disease mutations as genetic glues, ZNF711 saturation",
     "https://www.biorxiv.org/content/10.64898/2026.09.17.752235v1.full"),
    ("domainome_nature",    "Human Domainome 1 — Nature 2025 (aPCA ~500 domain)",
     "https://www.nature.com/articles/s41586-024-08370-4"),
    ("mavedb_api_openapi", "MaveDB API — mô tả OpenAPI (để dựng truy vấn score set)",
     "https://api.mavedb.org/api/v1/openapi.json"),
    ("proteingym",          "ProteinGym — benchmark DMS, trang chủ",
     "https://proteingym.org/"),
    ("tsuboyama_zenodo",    "Tsuboyama 2023 — Zenodo K50/ΔG processed datasets",
     "https://zenodo.org/records/7844779"),
    ("aspa_natcomm",        "ASPA DMS 2024 — Nat Commun (abundance + degron tile)",
     "https://www.nature.com/articles/s41467-024-48481-0"),
    ("parkin_natcomm",      "Parkin mutational atlas 2024 — Nat Commun (VAMP-seq + degron tile)",
     "https://www.nature.com/articles/s41467-024-45829-4"),
    ("e3_crispr_ncb2023",   "Nat Cell Biol 2023 — multiplex CRISPR E3–substrate",
     "https://www.nature.com/articles/s41556-023-01229-2"),
    ("degronopedia",        "DEGRONOPEDIA — trang tài liệu (trang /download trả 404)",
     "https://degronopedia.com/degronopedia/documentation"),
    ("elm_downloads",       "ELM — trang downloads (motif, academic license)",
     "http://elm.eu.org/downloads.html"),
]


def probe(url: str) -> dict:
    out: dict = {"url": url}
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                out.update(
                    method=method,
                    status=resp.status,
                    final_url=resp.geturl(),
                    content_type=resp.headers.get("Content-Type"),
                    content_length=resp.headers.get("Content-Length"),
                )
                return out
        except urllib.error.HTTPError as e:
            out.update(method=method, status=e.code, error=f"HTTPError {e.code} {e.reason}",
                       content_type=e.headers.get("Content-Type") if e.headers else None)
            if method == "GET":
                return out
        except (urllib.error.URLError, socket.timeout, OSError) as e:
            out.update(method=method, status=None, error=f"{type(e).__name__}: {e}")
            if method == "GET":
                return out
    return out


def main() -> None:
    results = []
    for key, label, url in TARGETS:
        rec = {"key": key, "label": label}
        rec.update(probe(url))
        results.append(rec)
        print(f"{rec.get('status')!s:>6}  {key}")
    payload = {
        "checked_on": date.today().isoformat(),
        "note": "Chỉ HEAD/GET trang công bố. Status 200 nghĩa là endpoint trả nội dung, "
                "KHÔNG đồng nghĩa dữ liệu dùng được hay giấy phép cho phép nhập.",
        "user_agent": UA,
        "results": results,
    }
    (HERE / "candidate-access.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n-> {HERE / 'candidate-access.json'}")


if __name__ == "__main__":
    main()
