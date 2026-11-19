"""Phép kiểm similarity cho mục 1.15, theo SIMILARITY-PROTOCOL.md 17/11/2026.

Chẩn đoán hậu kiểm trên T đã từng được khảo sát. Chỉ đọc kết quả per-peptide đã
tính ở job aggregate-refit; không nạp model, không suy luận, không GPU.
Không đóng G2/G3, không đổi mô hình phục vụ, không sửa campaign.

Chạy từ gốc repo:
    .venv/bin/python -I research/lora-refit-transfer-2026-11-16/analyze-similarity.py
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
CAMPAIGN = REPO / 'research/kaggle-roadmap-2026-10-31/output/local/aa4fc2b7ce29abf9'
AGGREGATE = CAMPAIGN / 'jobs/aggregate-refit'
RELIABILITY = REPO / 'research/reliability-transfer-2026-11-08'
PROTOCOL_SHA = 'd74dc18d24bc25804f8bcf226647897ab40f3a13f896818818b201964ea7393e'

CONTRASTS = [('esm2_35m-lora-D', 'esm2_35m-frozen-D'), ('esm2_35m-lora-D', 'ordered-w5-D')]
STRATA_CONTRAST = ('esm2_35m-lora-D', 'zero')
STRATA_ORDER = ['le3', 'gt3_le4', 'gt4_le5', 'gt5']


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def paired_ci(pairs, replicates, seed, multiplicity):
    """Cùng công thức với degron_v3/metrics.py:paired_ci; bootstrap theo nhóm."""
    grouped = pairs.groupby('group_id').delta.agg(['sum', 'count'])
    rng = np.random.default_rng(seed)
    sampled = rng.integers(0, len(grouped), size=(replicates, len(grouped)))
    draws = grouped['sum'].to_numpy()[sampled].sum(1) / grouped['count'].to_numpy()[sampled].sum(1)
    q = .025 / multiplicity
    return dict(delta=float(pairs.delta.mean()),
                ci95=np.quantile(draws, [.025, .975]).tolist(),
                ci_adjusted=np.quantile(draws, [q, 1 - q]).tolist(),
                multiplicity=multiplicity, peptides=int(len(pairs)),
                clusters=int(len(grouped)), bootstrap=int(replicates))


def delta_frame(recipes, a, b):
    """Hiệu MAE từng peptide, ghép theo peptide_id."""
    left = recipes[a][['peptide_id', 'group_id', 'psi_stratum', 'mae']]
    right = recipes[b][['peptide_id', 'mae']]
    pairs = left.merge(right, on='peptide_id', suffixes=('_a', '_b'), validate='one_to_one').dropna()
    pairs = pairs.copy()
    pairs['delta'] = pairs.mae_a - pairs.mae_b
    return pairs


def main():
    assert sha256(HERE / 'SIMILARITY-PROTOCOL.md') == PROTOCOL_SHA, 'Protocol đã đổi sau khi khoá'

    config = json.loads((RELIABILITY / 'config.json').read_text())
    bins = config['identity_bins']
    replicates, seed = config['bootstrap_replicates'], config['bootstrap_seed']

    recipes = {}
    for name in ['esm2_35m-lora-D', 'esm2_35m-frozen-D', 'ordered-w5-D', 'zero']:
        recipes[name] = pd.read_csv(AGGREGATE / f'{name}-per-peptide.csv')
        assert len(recipes[name]) == 1410, name

    similarity = pd.read_csv(RELIABILITY / 'similarity.csv')
    similarity = similarity[similarity.cohort == 'T'][
        ['peptide_id', 'max_aligned_identity', 'max_query_5mer_coverage', 'reference_peptides']]
    assert len(similarity) == 1410 and similarity.peptide_id.is_unique
    reference_peptides = sorted(set(similarity.reference_peptides))
    assert reference_peptides == [235], reference_peptides

    published = json.loads((AGGREGATE / 'results.json').read_text())['contrasts']

    # Kiểm tự chứng: tái tạo contrast toàn cohort đã công bố.
    selfcheck = []
    for a, b in CONTRASTS:
        pairs = delta_frame(recipes, a, b)
        got = paired_ci(pairs, replicates, seed, 2)
        want = published[f'{a}_minus_{b}']
        diff = abs(got['delta'] - want['delta'])
        assert diff <= 1e-9, (a, b, diff)
        assert got['peptides'] == want['peptides'] and got['clusters'] == want['clusters']
        selfcheck.append(dict(contrast=f'{a}_minus_{b}', recomputed_delta=got['delta'],
                              published_delta=want['delta'], absolute_difference=float(diff),
                              ci95_max_absolute_difference=float(
                                  max(abs(x - y) for x, y in zip(got['ci95'], want['ci95'])))))

    # Phép kiểm chính: delta theo bin similarity.
    rows, by_contrast = [], {}
    for a, b in CONTRASTS:
        pairs = delta_frame(recipes, a, b).merge(similarity, on='peptide_id', validate='one_to_one')
        assert len(pairs) == 1410
        pairs['identity_bin'] = pd.cut(pairs.max_aligned_identity, bins, right=False).astype(str)
        by_contrast[f'{a}_minus_{b}'] = pairs
        rows.extend((f'{a}_minus_{b}', value) for value in sorted(set(pairs.identity_bin)))
    multiplicity = len(rows)

    contrasts_out, table = {}, []
    for a, b in CONTRASTS:
        name = f'{a}_minus_{b}'
        pairs = by_contrast[name]
        entry = {}
        for value, sub in pairs.groupby('identity_bin', sort=True):
            record = paired_ci(sub, replicates, seed, multiplicity)
            record.update(mean_identity=float(sub.max_aligned_identity.mean()),
                          min_identity=float(sub.max_aligned_identity.min()),
                          max_identity=float(sub.max_aligned_identity.max()),
                          max_5mer_coverage=float(sub.max_query_5mer_coverage.max()))
            entry[value] = record
            table.append(dict(contrast=name, identity_bin=value, **record))
        rho = spearmanr(pairs.max_aligned_identity, pairs.delta)
        contrasts_out[name] = dict(
            bins=entry,
            spearman_identity_vs_delta=dict(
                rho=float(rho.statistic), pvalue=float(rho.pvalue), peptides=int(len(pairs)),
                note='Mô tả, theo peptide, không gom cụm; không phải kiểm định cơ chế.'))

    # Bổ sung cho L3: delta theo strata, contrast LoRA-D trừ zero.
    a, b = STRATA_CONTRAST
    strata_pairs = delta_frame(recipes, a, b)
    strata_multiplicity = strata_pairs.psi_stratum.nunique()
    strata_out = {}
    for value, sub in strata_pairs.groupby('psi_stratum', sort=True):
        strata_out[value] = paired_ci(sub, replicates, seed, strata_multiplicity)

    # Quy tắc đọc đã khoá ở protocol §5.
    verdicts = {}
    for name, entry in contrasts_out.items():
        populated = [k for k in sorted(entry['bins']) if entry['bins'][k]['peptides'] > 0]
        bottom = populated[0]
        below = {k: entry['bins'][k]['ci95'][1] < 0 for k in populated}
        if below[bottom]:
            verdict = 'H-S_does_not_explain_advantage'
        elif any(below[k] for k in populated[1:]):
            verdict = 'H-S_supported'
        else:
            verdict = 'unresolved'
        verdicts[name] = dict(verdict=verdict, bottom_bin=bottom,
                              populated_bins=populated,
                              bins_with_ci95_below_zero=[k for k in populated if below[k]])

    result = dict(
        schema_version=1,
        protocol_sha256=PROTOCOL_SHA,
        campaign='aa4fc2b7ce29abf9',
        scientific_status='development_not_gate_closure',
        evaluation='posthoc_diagnostic_on_previously_examined_held_source',
        hypothesis='similarity_construct: lợi thế LoRA-D trên T đến từ đồng dạng trình tự với W',
        denominators=dict(peptides=1410, clusters=730, cells=39234),
        identity_reference=dict(peptides=235, cohort='W training peptides',
                                metric='max_aligned_identity, căn vị trí trên 28 aa',
                                source='research/reliability-transfer-2026-11-08/similarity.csv'),
        parameters=dict(identity_bins=bins, bootstrap_replicates=replicates,
                        bootstrap_seed=seed, cluster='group_id', multiplicity=multiplicity),
        selfcheck=selfcheck,
        contrasts=contrasts_out,
        verdicts=verdicts,
        strata_lora_minus_zero=strata_out,
        inputs=[dict(path=str(p.relative_to(REPO)), sha256=sha256(p)) for p in [
            AGGREGATE / 'esm2_35m-lora-D-per-peptide.csv',
            AGGREGATE / 'esm2_35m-frozen-D-per-peptide.csv',
            AGGREGATE / 'ordered-w5-D-per-peptide.csv',
            AGGREGATE / 'zero-per-peptide.csv',
            RELIABILITY / 'similarity.csv',
            RELIABILITY / 'config.json']],
        limitations=[
            'max_aligned_identity là proxy cục bộ; không thay MMseqs2 hay audit remote homology.',
            'Không bao gồm phơi nhiễm trình tự trong pretraining của ESM2.',
            'Liên hệ thống kê, không phải cơ chế; không kết luận nhân quả.',
            'T đã từng được khảo sát; phép kiểm này không nâng T thành nguồn độc lập.',
            'Chẩn đoán thứ cấp; không đóng G2/G3 và không đổi mô hình phục vụ.'])

    (HERE / 'similarity-results.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    pd.DataFrame(table).to_csv(HERE / 'similarity-contrasts.csv', index=False)

    print(json.dumps(dict(selfcheck=selfcheck, verdicts=verdicts), ensure_ascii=False, indent=2))
    print('\nbins:')
    for name, entry in contrasts_out.items():
        for value, record in sorted(entry['bins'].items()):
            print(f"  {name} {value}: delta={record['delta']:+.4f} "
                  f"ci95=[{record['ci95'][0]:+.4f}, {record['ci95'][1]:+.4f}] "
                  f"peptides={record['peptides']} clusters={record['clusters']}")
        r = entry['spearman_identity_vs_delta']
        print(f"  {name} spearman(identity, delta)={r['rho']:+.4f} p={r['pvalue']:.3g}")
    print('\nstrata lora-D minus zero:')
    for value in STRATA_ORDER:
        if value in strata_out:
            record = strata_out[value]
            print(f"  {value}: delta={record['delta']:+.4f} "
                  f"ci95=[{record['ci95'][0]:+.4f}, {record['ci95'][1]:+.4f}] "
                  f"peptides={record['peptides']} clusters={record['clusters']}")


if __name__ == '__main__':
    main()
