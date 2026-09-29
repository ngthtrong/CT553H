"""Kiểm tra nhanh RQ1 (bản thô): embedding zero-shot trên tập dev ~10%.

Chạy từ thư mục gốc:  .venv/bin/python ml/experiments/rq1-kiem-tra-nhanh/run.py

Mỗi ghi chú chi tiêu được gán vào danh mục có embedding gần nhất (cosine) với
embedding của tên (hoặc tên + mô tả) danh mục. Không học gì từ dữ liệu thật.
Kết quả chỉ ghi id giao dịch, không ghi nội dung ghi chú.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, f1_score

SEED = 42
DEV_FRAC = 0.10
FREQUENT_MIN = 5  # ghi chú xuất hiện >= 5 lần trong toàn bộ khoản chi là "hay gặp"
MODELS = {
    "e5-small": ("intfloat/multilingual-e5-small", "query: ", "passage: "),
    "e5-base": ("intfloat/multilingual-e5-base", "query: ", "passage: "),
    "bge-m3": ("BAAI/bge-m3", "", ""),
}

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "results"


def load_dev() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "data" / "processed" / "transactions_anon.csv")
    exp = df[(df.direction == "EXPENSE") & df.expense_category.notna()].copy()
    exp["key"] = exp.title.str.lower().str.strip()
    exp["frequent"] = exp.key.map(exp.key.value_counts()) >= FREQUENT_MIN
    return exp.sample(frac=DEV_FRAC, random_state=SEED).sort_values("id")


def scores(y_true, y_pred, labels) -> dict:
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    cats = json.loads((HERE / "categories.json").read_text(encoding="utf-8"))["categories"]
    names = [c["name"] for c in cats]
    label_texts = {
        "name": names,
        "name+desc": [f'{c["name"]}: {c["description"]}' for c in cats],
    }
    dev = load_dev()
    labels = sorted(dev.expense_category.unique())  # Macro-F1 trên các nhãn có trong dev
    dev[["id"]].to_csv(OUT / "dev_ids.csv", index=False)
    y = dev.expense_category.to_numpy()

    rows, per_cat, preds = [], [], pd.DataFrame({"id": dev.id, "true": y})

    def record(method: str, variant: str, pred: np.ndarray, top3: np.ndarray | None = None) -> None:
        r = {"method": method, "variant": variant, **scores(y, pred, labels)}
        r["top3_accuracy"] = float(np.mean([t in p for t, p in zip(y, top3)])) if top3 is not None else None
        for part, mask in (("frequent", dev.frequent.to_numpy()), ("rare", ~dev.frequent.to_numpy())):
            r[f"accuracy_{part}"] = accuracy_score(y[mask], pred[mask])
        rows.append(r)
        f1s = f1_score(y, pred, labels=labels, average=None, zero_division=0)
        per_cat.extend({"method": method, "variant": variant, "category": c, "support": int((y == c).sum()), "f1": f}
                       for c, f in zip(labels, f1s))
        preds[f"{method}|{variant}"] = pred

    # Baseline
    rng = np.random.default_rng(SEED)
    record("baseline", "random-uniform", rng.choice(names, size=len(y)))
    record("baseline", "majority(AC)*", np.full(len(y), "AC"))  # * cần biết phân bố nhãn, người dùng mới không có
    lower = dev.title.str.lower()
    match = [next((n for n in names if n.lower() in t), "AC") for t in lower]
    record("baseline", "name-match", np.array(match))

    # Embedding zero-shot
    for short, (model_id, q_prefix, p_prefix) in MODELS.items():
        model = SentenceTransformer(model_id, device="cpu")
        note_emb = model.encode([q_prefix + t for t in dev.title], normalize_embeddings=True, batch_size=64)
        for variant, texts in label_texts.items():
            cat_emb = model.encode([p_prefix + t for t in texts], normalize_embeddings=True)
            sim = note_emb @ cat_emb.T
            order = np.argsort(-sim, axis=1)
            pred = np.array(names)[order[:, 0]]
            top3 = np.array(names)[order[:, :3]]
            record(f"embedding:{short}", variant, pred, top3)
            print(f"{short:9s} {variant:10s} acc={rows[-1]['accuracy']:.3f} macroF1={rows[-1]['macro_f1']:.3f}")

    pd.DataFrame(rows).round(4).to_csv(OUT / "summary.csv", index=False)
    pd.DataFrame(per_cat).round(4).to_csv(OUT / "per_category.csv", index=False)
    preds.to_csv(OUT / "predictions.csv", index=False)
    (OUT / "config.json").write_text(json.dumps({
        "seed": SEED, "dev_frac": DEV_FRAC, "n_dev": len(dev), "frequent_min": FREQUENT_MIN,
        "n_frequent": int(dev.frequent.sum()), "models": {k: v[0] for k, v in MODELS.items()},
        "categories_file": "categories.json (bản nháp của Claude, chưa được người làm đề tài duyệt)",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
