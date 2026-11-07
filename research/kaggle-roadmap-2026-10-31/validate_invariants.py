"""Focused scientific/reproducibility checks for the delivered v3 pipeline."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())
sys.path.insert(0, str(HERE))
from degron_v3.common import atomic_json, sha256, execution
from degron_v3.data import Dataset, balanced_weights
from degron_v3.features import features
from degron_v3.plm import merge_shards, feature_data


def main():
    ds = Dataset(TOPIC/'data/processed/v3-fullpsi')
    results = {}
    scan = ds.scanning(include_held=True)
    for seed in (17, 29, 43):
        for fold in range(5):
            roles = ds.role(ds.sat, fold, seed)
            groups = {r: set(ds.sat.group_id[roles == r]) for r in ('train', 'validation', 'test')}
            assert all(not groups[a] & groups[b] for a, b in [('train', 'validation'), ('train', 'test'), ('validation', 'test')])
            assert set(ds.role(scan[scan.partition == 'scan_T'], fold, seed)) == {'held_source'}
    assert not set(scan.loc[scan.partition == 'scan_T', 'group_id']) & set(ds.sat.group_id)
    results['all_15_grouped_split_roles_and_scan_T'] = 'pass'
    frame = ds.sample_smoke(ds.sat).head(128)
    edited = frame.copy()
    for col in ['psi_wt_sat', 'dpsi_mean', 'outer_fold', 'replicate_disagreement']:
        edited[col] = 9999
    edited['group_id'] = 'changed'; edited['psi_stratum'] = 'changed'
    for kind in ('pair', 'composition', 'unordered', 'ordered'):
        assert np.array_equal(features(frame, kind), features(edited, kind))
    results['features_ignore_labels_PSI_counts_groups_folds'] = 'pass'
    train = ds.sat[ds.sat.outer_fold != 0]
    weights = pd.DataFrame(dict(peptide=train.peptide_id.to_numpy(), stratum=train.psi_stratum.to_numpy(),
                                weight=balanced_weights(train)))
    strata = weights.groupby('stratum').weight.sum()
    assert np.allclose(strata, strata.iloc[0])
    for _, rows in weights.groupby('stratum'):
        sums = rows.groupby('peptide').weight.sum()
        assert np.allclose(sums, sums.iloc[0])
    results['balanced_weights_equal_strata_and_peptides'] = 'pass'
    archive = TOPIC/'data/processed/packages/degron-data-v3-fullpsi.zip'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        manifest = json.loads(z.read('degron-data-v3-fullpsi/DATA_MANIFEST.json'))
        for item in manifest['files']:
            value = z.read('degron-data-v3-fullpsi/'+item['path'])
            assert hashlib.sha256(value).hexdigest() == item['sha256']
            if item['path'].endswith(('.json', '.md', '.log')):
                assert b'/home/' not in value and b'/tmp/' not in value, item['path']
    assert sha256(archive) == json.loads((HERE/'dataset-build.json').read_text())['sha256']
    results['zip_crc_manifest_hash_and_portable_metadata'] = 'pass'
    # Uneven shard sizes exercise the final minibatch and prevent accidental row overlap.
    with tempfile.TemporaryDirectory(prefix='degron-v3-invariants-') as td:
        td = Path(td); shards = []
        for i, count in enumerate((3, 5)):
            path = td/str(i); path.mkdir(); shards.append(path)
            np.save(path/'pool.npy', np.full((count, 4), i, dtype=np.float16))
            np.save(path/'crop.npy', np.full((count, 15, 2), i, dtype=np.float16))
            pd.DataFrame(dict(cell_id=[f'{i}-{j}' for j in range(count)], peptide_id='fixture')).to_parquet(path/'rows.parquet')
            atomic_json(path/'feature-manifest.json', dict(data_identity=ds.identity, model_id='fixture', revision='fixture',
                row_scope='sat', mode='smoke', dtype='float32', feature_kind='delta_site_and_mean', hidden_size=2,
                crop=True, status='complete', rows=count,
                files=[dict(path=p.name, sha256=sha256(p)) for p in sorted(path.iterdir())]))
        merge_shards(shards, td/'merged')
        requested = pd.DataFrame(dict(cell_id=['1-4', '0-0']))
        pooled, _ = feature_data(td/'merged', requested, ds.identity, allow_smoke=True)
        assert np.array_equal(pooled, [[1]*4, [0]*4])
        crops, _ = feature_data(td/'merged', requested, ds.identity, allow_smoke=True, crop=True)
        assert crops[0].shape == (15, 2) and np.all(crops[0] == 1)
        try:
            merge_shards([shards[0], shards[0]], td/'overlap')
        except AssertionError:
            pass
        else:
            raise AssertionError('Overlapping feature shards accepted')
        try:
            feature_data(td/'merged', requested, ds.identity, allow_smoke=False)
        except AssertionError:
            pass
        else:
            raise AssertionError('Smoke features accepted for official training')
        results['uneven_shards_mapping_overlap_and_smoke_rejection'] = 'pass'
        with execution(td/'resume', 'test', {'smoke': True, 'parameter': 1}):
            pass
        try:
            with execution(td/'resume', 'test', {'smoke': True, 'parameter': 2}):
                pass
        except AssertionError:
            pass
        else:
            raise AssertionError('Changed config resumed in place')
        results['resume_rejects_changed_config'] = 'pass'
    atomic_json(HERE/'invariant-validation.json', dict(status='pass', data_identity=ds.identity, checks=results))
    print(results)


if __name__ == '__main__':
    main()
