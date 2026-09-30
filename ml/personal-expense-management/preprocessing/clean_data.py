"""Làm sạch và ẩn danh bộ dữ liệu chi tiêu cá nhân (export từ Notion).

Chạy:  python ml/personal-expense-management/preprocessing/clean_data.py
Đầu vào: data/personal-expense-management/raw/notion-export.csv (bản xuất Notion, không bị sửa).
Đầu ra:
  data/personal-expense-management/processed/transactions_clean.csv  bản đầy đủ, CHƯA ẩn danh, chỉ dùng riêng
  data/personal-expense-management/processed/transactions_anon.csv   bản đã ẩn danh tên người, dùng để gửi GVHD
Danh sách tên cần ẩn danh nằm ở data/personal-expense-management/raw/anonymize_names.txt, sửa file đó rồi chạy lại.
"""
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "personal-expense-management"
RAW = DATA / "raw" / "notion-export.csv"
OUT = DATA / "processed"
NAMES = DATA / "raw" / "anonymize_names.txt"

BULK_IMPORT_DAYS = {"2024-12-05", "2024-12-06", "2026-06-01"}
ADJUSTMENT_PAT = r"cân bằng số liệu|điều chỉnh chênh lệch"
TRIP_PAT = r"đài loan|malay"


def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFC", str(s)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip()


def load_names() -> tuple[list[str], list[str]]:
    names, protected = [], []
    for line in NAMES.read_text(encoding="utf-8").splitlines():
        line = unicodedata.normalize("NFC", line.split("#", 1)[0].strip().lower())
        if line.startswith("!"):
            protected.append(line[1:].strip())
        elif line:
            names.append(line)
    # tên dài thay trước để "a thành" không bị "thành" thay mất một nửa; cùng độ dài thì theo ABC để mã [Pxx] cố định
    return sorted(set(names), key=lambda n: (-len(n), n)), protected


def word(s: str) -> str:
    return rf"(?<!\w){re.escape(s)}(?!\w)"


def anonymize(text: str, mapping: dict[str, str], protected: list[str]) -> str:
    out, kept = text, {}
    for i, phrase in enumerate(protected):
        key = f"\x00{i}\x00"
        out = re.sub(word(phrase), lambda m: kept.setdefault(key, m.group(0)) and key, out, flags=re.IGNORECASE)
    for name, alias in mapping.items():
        out = re.sub(word(name), alias, out, flags=re.IGNORECASE)
    for key, original in kept.items():
        out = out.replace(key, original)
    return out


def main() -> None:
    raw = pd.read_csv(RAW, encoding="utf-8-sig")
    df = pd.DataFrame({
        "id": range(1, len(raw) + 1),
        "date": pd.to_datetime(raw["Date"], format="%d/%m/%Y"),
        "title": raw["Title"].map(norm_text),
        "amount_vnd": raw["Cost"].str.replace(r"[₫,]", "", regex=True).astype(int),
        "direction": raw["Ex/In"].map({"Expenses": "EXPENSE", "In-come": "INCOME"}),
        "expense_category": raw["Type Expenses"],
        "income_category": raw["Type In come"],
        "special": raw["Special"],
        "created_at": pd.to_datetime(raw["Created time"], format="%B %d, %Y %I:%M %p"),
    })
    special = df["special"].fillna("")
    for tag in ["Monthly", "BigM", "BigY", "Annual", "Vay"]:
        df[f"is_{tag.lower()}"] = special.str.contains(tag)
    df["is_regular"] = special.eq("")

    title_lc = df["title"].str.lower()
    df["flag_adjustment"] = title_lc.str.contains(ADJUSTMENT_PAT)
    df["flag_loan_flow"] = df["income_category"].eq("Cho vay") | df["expense_category"].eq("Cho vay")
    df["flag_trip_lump_sum"] = title_lc.str.contains(TRIP_PAT)
    df["flag_missing_label"] = df["direction"].eq("EXPENSE") & df["expense_category"].isna()
    df["flag_possible_duplicate"] = df.duplicated(
        ["title", "amount_vnd", "date", "direction", "expense_category"], keep=False)

    # nhãn khác với nhãn chiếm đa số của cùng một nội dung (vd. "xăng" gán AC thay vì DC)
    exp = df[df["direction"].eq("EXPENSE") & df["expense_category"].notna()]
    majority = exp.groupby(title_lc[exp.index])["expense_category"].agg(lambda s: s.value_counts().index[0])
    df["flag_label_minority"] = df.index.isin(exp.index) & df["expense_category"].ne(title_lc.map(majority))

    df["is_backfilled"] = df["created_at"].dt.strftime("%Y-%m-%d").isin(BULK_IMPORT_DAYS)
    df["entry_lag_days"] = (df["created_at"].dt.normalize() - df["date"]).dt.days.where(~df["is_backfilled"])

    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "transactions_clean.csv", index=False, encoding="utf-8")

    names, protected = load_names()
    mapping = {n: f"[P{i:02d}]" for i, n in enumerate(names, 1)}
    anon = df.drop(columns=["created_at"]).copy()
    anon["title"] = anon["title"].map(lambda t: anonymize(t, mapping, protected))
    anon.to_csv(OUT / "transactions_anon.csv", index=False, encoding="utf-8")

    changed = (anon["title"] != df["title"]).sum()
    print(f"{len(df)} dòng -> {OUT}")
    print(f"ẩn danh {len(names)} tên, {changed} dòng bị thay đổi nội dung")
    for col in [c for c in df.columns if c.startswith("flag_")]:
        print(f"  {col}: {int(df[col].sum())}")


if __name__ == "__main__":
    main()
