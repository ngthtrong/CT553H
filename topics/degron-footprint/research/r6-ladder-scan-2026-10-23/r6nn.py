"""R6 giai đoạn E–G — đầu CNN / mCNN trên cửa sổ ±7 quanh điểm đột biến.

Một họ mô hình duy nhất `ConvHead`; hai biểu diễn:
  * 'onehot': kênh = [one-hot WT (20) ; chỉ báo trung tâm (1)];
  * 'esmXX' : kênh = [one-hot WT (20) ; chỉ báo trung tâm (1) ; Linear(d→32)(Δ embedding)] — tức CHỈ thêm kênh Δ embedding.
Phần "đầu" nhận thêm đặc trưng toàn cục của M3: cặp (WT, mut) one-hot (40) và thành phần peptide (20), cộng
chỉ báo nguồn khi trộn scanning. Vì vậy 'onehot' chứa thông tin của M3 (ngữ cảnh ±3 nằm trong cửa sổ ±7).
Mọi siêu tham số cố định (PROTOCOL §3), không điều chỉnh theo từng cấu hình.
"""
import numpy as np
import torch
from torch import nn
import torch.nn.functional as Fn

import r6data as r6

HP = dict(proj=32, hidden=64, drop_in=0.2, drop=0.3, lr=1e-3, wd=1e-2, batch=1024, max_epochs=40, patience=6)
FT = dict(lr=3e-4, max_epochs=30, patience=6)              # tinh chỉnh sau tiền huấn luyện trên scanning
PRE = dict(lr=1e-3, max_epochs=30, patience=4)             # tiền huấn luyện trên scanning


class ConvHead(nn.Module):
    def __init__(self, D, ks, F, use_src=False, proj=HP['proj'], hidden=HP['hidden'],
                 drop_in=HP['drop_in'], drop=HP['drop']):
        super().__init__()
        self.D, self.ks, self.use_src = D, tuple(ks), use_src
        cin = 21 + (proj if D else 0)
        if D:
            self.in_drop = nn.Dropout(drop_in)
            self.proj = nn.Linear(D, proj)
        self.convs = nn.ModuleList([nn.Conv1d(cin, F, k, padding=k // 2) for k in self.ks])
        feat = 2 * F * len(self.ks) + 60 + int(use_src)
        self.head = nn.Sequential(nn.Dropout(drop), nn.Linear(feat, hidden), nn.ReLU(),
                                  nn.Dropout(drop), nn.Linear(hidden, 1))

    def forward(self, wt_idx, crop, f60, src=None):
        B, Lc = wt_idx.shape
        valid = (wt_idx < 20).unsqueeze(-1)
        oh = Fn.one_hot(wt_idx.long().clamp(max=19), 20).float() * valid
        center = torch.zeros(B, Lc, 1, device=wt_idx.device)
        center[:, Lc // 2] = 1.0
        x = [oh, center]
        if self.D:
            x.append(Fn.gelu(self.proj(self.in_drop(crop.float()))) * valid)
        x = torch.cat(x, -1).transpose(1, 2)                                    # [B, C, L]
        vmask = valid.transpose(1, 2).float()                                   # [B, 1, L]
        feats = []
        for conv in self.convs:
            h = Fn.relu(conv(x)) * vmask
            feats += [h.amax(2), h[:, :, Lc // 2]]
        z = torch.cat(feats + [f60] + ([src.unsqueeze(1)] if self.use_src else []), 1)
        return self.head(z).squeeze(1)


class Pack:
    """Tensor trên thiết bị, chỉ mục theo hàng toàn cục (bão hòa trước, scanning sau)."""

    def __init__(self, dev, wt_idx, f60, y, crop=None, src=None):
        self.dev = dev
        self.wt_idx = torch.as_tensor(wt_idx, dtype=torch.int8, device=dev)
        self.f60 = torch.as_tensor(f60, dtype=torch.float32, device=dev)
        self.y = torch.as_tensor(y, dtype=torch.float32, device=dev)
        self.crop = crop
        self.src = None if src is None else torch.as_tensor(src, dtype=torch.float32, device=dev)
        self.D = 0 if crop is None else int(crop.shape[2])

    def batch(self, rows):
        return (self.wt_idx[rows], None if self.crop is None else self.crop[rows], self.f60[rows],
                None if self.src is None else self.src[rows])


def _eval_mse(model, pack, rows, bs=8192):
    model.eval()
    tot, n = 0.0, 0
    with torch.no_grad():
        for i in range(0, len(rows), bs):
            r = rows[i:i + bs]
            tot += float(((model(*pack.batch(r)) - pack.y[r]) ** 2).sum())
            n += len(r)
    return tot / max(n, 1)


def predict(model, pack, rows, bs=8192):
    model.eval()
    rows_t = torch.as_tensor(rows, device=pack.dev)
    out = []
    with torch.no_grad():
        for i in range(0, len(rows_t), bs):
            out.append(model(*pack.batch(rows_t[i:i + bs])).double().cpu().numpy())
    return np.concatenate(out)


def fit(pack, tr, va, spec, seed, init_state=None, lr=None, max_epochs=None, patience=None):
    """Huấn luyện một mạng; chọn epoch theo MSE trên `va`; trả về (model, thông tin)."""
    dev = pack.dev
    torch.manual_seed(seed)
    model = ConvHead(pack.D, spec['ks'], spec['F'], use_src=spec.get('use_src', False)).to(dev)
    if init_state is not None:
        model.load_state_dict(init_state)
    else:
        with torch.no_grad():
            model.head[-1].bias.fill_(float(pack.y[torch.as_tensor(tr, device=dev)].mean()))
    lr, max_epochs, patience = lr or HP['lr'], max_epochs or HP['max_epochs'], patience or HP['patience']
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=HP['wd'])
    tr_t, va_t = torch.as_tensor(tr, device=dev), torch.as_tensor(va, device=dev)
    g = torch.Generator().manual_seed(seed)
    best, state, best_ep, bad, ep = float('inf'), None, 0, 0, 0
    for ep in range(1, max_epochs + 1):
        model.train()
        perm = tr_t[torch.randperm(len(tr_t), generator=g).to(dev)]
        for i in range(0, len(perm), HP['batch']):
            rows = perm[i:i + HP['batch']]
            loss = ((model(*pack.batch(rows)) - pack.y[rows]) ** 2).mean()
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
        v = _eval_mse(model, pack, va_t)
        if v < best - 1e-6:
            best, best_ep, bad = v, ep, 0
            state = {k: t.detach().clone() for k, t in model.state_dict().items()}
        else:
            bad += 1
            if bad >= patience:
                break
    model.load_state_dict(state)
    return model, {'best_epoch': best_ep, 'best_val_mse': best, 'stopped_at_epoch': ep,
                   'hit_epoch_cap': bool(ep == max_epochs and bad == 0)}
