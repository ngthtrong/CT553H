"""Baseline bắt buộc cho RQ2 và thí nghiệm nhỏ về phản hồi thiếu (bản thô).

Chạy từ thư mục gốc:  .venv/bin/python ml/personal-expense-management/experiments/rq2-baseline-recall/run.py

Phát lại toàn bộ khoản chi theo thứ tự thời gian (kiểm tra trước, học sau).
Chiến lược:
  B0 nhớ lại        ghi chú đã gặp -> nhãn lần gần nhất; chưa gặp -> không gợi ý
  B1 nhớ lại + ZS   như B0, chưa gặp -> embedding zero-shot (bge-m3, tên + mô tả)
Danh mục được "tạo" vào ngày đầu tiên nó được dùng; zero-shot chỉ chọn trong
các danh mục đã tồn tại tại thời điểm đó.

Phản hồi thiếu: khi gợi ý sai, người dùng chỉ sửa với xác suất p; nếu không,
nhãn sai được lưu vào bộ nhớ như nhãn thật. Không có gợi ý thì người dùng tự
chọn đúng. Tập dev của RQ1 vẫn được phát lại nhưng không tính điểm.
"""

import json
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
DATA = ROOT / "data" / "personal-expense-management"
CACHE = DATA / "interim" / "emb_bge-m3_titles.npz"  # dẫn xuất từ dữ liệu cá nhân, không lên git
CATEGORIES = ROOT / "ml" / "personal-expense-management" / "experiments" / "rq1-quick-check" / "categories.json"
DEV_IDS = ROOT / "ml" / "personal-expense-management" / "experiments" / "rq1-quick-check" / "results" / "dev_ids.csv"

FEEDBACK_P = [1.0, 0.9, 0.7, 0.5]
SEEDS = [0, 1, 2, 3, 4]
EARLY_DAYS = 30


def normalize(text: str, strip_accents: bool = False) -> str:
    text = " ".join(str(text).lower().split())
    if strip_accents:
        text = unicodedata.normalize("NFD", text.replace("đ", "d"))
        text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text


def load_stream() -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(DATA / "processed" / "transactions_anon.csv")
    exp = df[(df.direction == "EXPENSE") & df.expense_category.notna()].copy()
    exp["date"] = pd.to_datetime(exp.date)
    exp = exp.sort_values(["date", "id"], kind="stable").reset_index(drop=True)
    exp["key"] = exp.title.map(normalize)
    exp["key_noacc"] = exp.title.map(lambda t: normalize(t, strip_accents=True))
    exp["is_dev"] = exp.id.isin(pd.read_csv(DEV_IDS).id)
    exp["days_since_start"] = (exp.date - exp.date.min()).dt.days
    first_use = exp.groupby("expense_category").date.min()  # ngày danh mục được "tạo"
    return exp, first_use


def zero_shot_scores(stream: pd.DataFrame, cats: list[dict]) -> tuple[np.ndarray, list[str]]:
    """Ma trận cosine (giao dịch x danh mục), dùng cache nếu đã tính."""
    names = [c["name"] for c in cats]
    texts = [f'{c["name"]}: {c["description"]}' for c in cats]
    keys = sorted(stream.key.unique())
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=True)
        if list(z["keys"]) == keys and list(z["label_texts"]) == texts:
            idx = {k: i for i, k in enumerate(keys)}
            return z["sim"][[idx[k] for k in stream.key]], names
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("BAAI/bge-m3", device="cpu")
    note = model.encode(keys, normalize_embeddings=True, batch_size=64, show_progress_bar=False)
    lab = model.encode(texts, normalize_embeddings=True)
    sim = note @ lab.T
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez(CACHE, keys=np.array(keys, dtype=object), label_texts=np.array(texts, dtype=object), sim=sim)
    idx = {k: i for i, k in enumerate(keys)}
    return sim[[idx[k] for k in stream.key]], names


def replay(stream, first_use, sim, names, strategy, key_col, p, rng) -> pd.DataFrame:
    memory: dict[str, str] = {}
    name_idx = {n: i for i, n in enumerate(names)}
    rows = []
    for i, r in enumerate(stream.itertuples(index=False)):
        key, truth = getattr(r, key_col), r.expense_category
        seen = key in memory
        if seen:
            pred = memory[key]
        elif strategy == "B1":
            active = [name_idx[n] for n, d in first_use.items() if d <= r.date]
            pred = names[active[int(np.argmax(sim[i, active]))]]
        else:
            pred = None  # không gợi ý, người dùng tự chọn
        correct = pred == truth
        if pred is None or correct:
            stored = truth
        else:
            stored = truth if rng.random() < p else pred  # sửa hoặc chấp nhận nhãn sai
        memory[key] = stored
        rows.append((seen, pred is not None, correct))
    res = stream[["id", "date", "days_since_start", "is_dev"]].copy()
    res[["seen", "suggested", "correct"]] = rows
    return res


def summarize(res: pd.DataFrame) -> dict:
    s = res[~res.is_dev]
    months = s.date.dt.to_period("M").nunique()
    unseen = s[~s.seen]
    return {
        "n_scored": len(s),
        "share_seen": s.seen.mean(),
        "accuracy": s.correct.mean(),
        "accuracy_seen": s[s.seen].correct.mean(),
        "accuracy_unseen": unseen.correct.mean(),
        "accuracy_first_30d": s[s.days_since_start < EARLY_DAYS].correct.mean(),
        "manual_per_month": (~s.correct).sum() / months,  # gợi ý sai hoặc không có gợi ý
        "manual_unseen_per_month": (~unseen.correct).sum() / months,
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    cats = json.loads(CATEGORIES.read_text(encoding="utf-8"))["categories"]
    stream, first_use = load_stream()
    sim, names = zero_shot_scores(stream, cats)

    rows, monthly = [], []
    for strategy in ("B0", "B1"):
        for key_col in ("key", "key_noacc"):
            for p in FEEDBACK_P:
                seeds = SEEDS if p < 1.0 else SEEDS[:1]  # p = 1 là tất định
                runs = []
                for seed in seeds:
                    res = replay(stream, first_use, sim, names, strategy, key_col, p, np.random.default_rng(seed))
                    runs.append(summarize(res))
                    if p == 1.0 and key_col == "key":
                        m = res[~res.is_dev].groupby(res.date.dt.to_period("M").astype(str))
                        monthly.append(m.correct.mean().rename(strategy))
                agg = pd.DataFrame(runs)
                row = {"strategy": strategy, "key": key_col, "feedback_p": p, "n_seeds": len(seeds)}
                row |= agg.mean().to_dict()
                row["accuracy_std"] = agg.accuracy.std() if len(seeds) > 1 else 0.0
                rows.append(row)
                print(f"{strategy} {key_col:9s} p={p:.1f} acc={row['accuracy']:.3f} "
                      f"unseen={row['accuracy_unseen']:.3f} first30d={row['accuracy_first_30d']:.3f}")

    pd.DataFrame(rows).round(4).to_csv(OUT / "summary.csv", index=False)
    pd.concat(monthly, axis=1).round(4).rename_axis("month").to_csv(OUT / "monthly_accuracy.csv")
    (OUT / "config.json").write_text(json.dumps({
        "feedback_p": FEEDBACK_P, "seeds": SEEDS, "early_days": EARLY_DAYS,
        "zero_shot": "BAAI/bge-m3, tên + mô tả, chỉ chọn trong danh mục đã tạo",
        "categories_file": "ml/personal-expense-management/experiments/rq1-quick-check/categories.json (bản nháp của Claude)",
        "category_created": "ngày đầu tiên danh mục được dùng",
        "scored": "mọi khoản chi có nhãn, trừ tập dev của RQ1",
    }, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
