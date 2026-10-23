"""R6 giai đoạn C — trích embedding ESM-2 đóng băng ở bốn cỡ, lưu dạng cắt quanh điểm đột biến.

Với ô (peptide WT, vị trí p, acid amin a): Δ = h_mut − h_wt (mỗi vị trí 28 residue, d chiều, lớp cuối đã qua
LayerNorm cuối của `EsmModel`, cùng R2). Lưu:
  * crop[i] = Δ ở 15 vị trí p−7..p+7 (0 nếu ngoài trình tự), float16, [n, 15, d]    — cho mạng CNN/mCNN;
  * pool[i] = [Δ tại p ; trung bình Δ trên 28 vị trí], float16, [n, 2d]               — cho ridge kiểu R2.
Cỡ mô hình chốt ở PROTOCOL §3; không đổi sau khi thấy số.
"""
import time
from pathlib import Path

import numpy as np

import r6data as r6

MODELS = {                                         # khóa -> (id Hugging Face, số chiều), PROTOCOL §3
    'esm8': ('facebook/esm2_t6_8M_UR50D', 320),
    'esm35': ('facebook/esm2_t12_35M_UR50D', 480),
    'esm150': ('facebook/esm2_t30_150M_UR50D', 640),
    'esm650': ('facebook/esm2_t33_650M_UR50D', 1280),
}


def resolve_source(key, roots=('/kaggle/input', '/content')):
    """Ưu tiên bản ESM-2 đã gắn làm dataset/model (không cần Internet); nếu không có thì dùng HF hub."""
    token = MODELS[key][0].split('/')[1].lower().replace('-', '_').rsplit('_ur50d', 1)[0]     # esm2_t12_35m
    for r in roots:
        rp = Path(r)
        if rp.exists():
            for cfg in rp.rglob('config.json'):
                if token in str(cfg.parent).lower().replace('-', '_'):
                    return str(cfg.parent)
    return MODELS[key][0]


def make_embed_fn(key, dev, source=None):
    import torch
    from transformers import AutoTokenizer, EsmModel
    src = source or resolve_source(key)
    tok = AutoTokenizer.from_pretrained(src)
    model = EsmModel.from_pretrained(src, add_pooling_layer=False)
    model = (model.half() if dev == 'cuda' else model).to(dev).eval()
    assert model.config.hidden_size == MODELS[key][1], 'số chiều khác khai báo'

    def embed(seqs):
        enc = tok(list(seqs), return_tensors='pt', padding=False)
        assert enc['input_ids'].shape[1] == r6.L + 2, 'cần <cls> + 28 residue + <eos>'
        enc = {k: v.to(dev) for k, v in enc.items()}
        with torch.no_grad():
            h = model(**enc).last_hidden_state
        return h[:, 1:r6.L + 1, :].float()
    embed.source = src
    return embed


def extract(key, wt_seq, mut_seq, pos, pep_of_row, embed_fn, dev, crop_path, pool_path=None,
            batch=256, limit=None, log=print):
    """Ghi crop (và pool nếu có đường dẫn) ra .npy bằng memmap. Trả về số ô đã ghi."""
    import torch
    D = MODELS[key][1]
    n = len(mut_seq) if limit is None else limit
    wt_list = list(wt_seq)
    wt_h = torch.cat([embed_fn(wt_list[i:i + 64]) for i in range(0, len(wt_list), 64)]).to(dev)    # [P,28,D]
    crop_mm = np.lib.format.open_memmap(crop_path, mode='w+', dtype=np.float16, shape=(n, r6.CROP, D))
    pool_mm = (np.lib.format.open_memmap(pool_path, mode='w+', dtype=np.float16, shape=(n, 2 * D))
               if pool_path else None)
    pos0 = torch.from_numpy(np.asarray(pos, dtype=np.int64) - 1)
    pep = torch.from_numpy(np.asarray(pep_of_row, dtype=np.int64))
    offs = torch.arange(-r6.HALF, r6.HALF + 1, device=dev)
    t0 = time.time()
    for i in range(0, n, batch):
        j = min(n, i + batch)
        h = embed_fn(list(mut_seq[i:j]))
        delta = h - wt_h[pep[i:j].to(dev)]
        p0 = pos0[i:j].to(dev)
        q = p0[:, None] + offs[None, :]
        valid = (q >= 0) & (q < r6.L)
        crop = torch.gather(delta, 1, q.clamp(0, r6.L - 1)[:, :, None].expand(-1, -1, D)) * valid[:, :, None]
        if not torch.isfinite(crop).all():
            raise FloatingPointError(f'Δ embedding có NaN/Inf ở lô {i}:{j} ({key})')
        crop_mm[i:j] = crop.half().cpu().numpy()
        if pool_mm is not None:
            site = delta[torch.arange(j - i, device=dev), p0]
            pool_mm[i:j] = torch.cat([site, delta.mean(1)], 1).half().cpu().numpy()
        if (i // batch) % 80 == 0:
            log(f'  [{key}] {j}/{n} ô · {time.time() - t0:.0f}s')
    crop_mm.flush()
    if pool_mm is not None:
        pool_mm.flush()
    return n


def load_to_device(paths, dev, chunk=20000):
    """Nạp một hoặc nhiều .npy (float16, cùng số chiều sau) lên thiết bị theo từng khúc vào MỘT tensor cấp phát sẵn
    (tránh đỉnh bộ nhớ gấp đôi của torch.cat)."""
    import torch
    paths = [paths] if isinstance(paths, (str, Path)) else list(paths)
    mms = [np.load(p, mmap_mode='r') for p in paths]
    assert len({m.shape[1:] for m in mms}) == 1, 'các file crop khác hình dạng'
    out = torch.empty((sum(m.shape[0] for m in mms),) + mms[0].shape[1:], dtype=torch.float16, device=dev)
    o = 0
    for mm in mms:
        for i in range(0, mm.shape[0], chunk):
            blk = np.array(mm[i:i + chunk])
            out[o + i:o + i + len(blk)] = torch.from_numpy(blk).to(dev)
        o += mm.shape[0]
    return out
