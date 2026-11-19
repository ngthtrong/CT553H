"""Agreement with imported data over time (plan-system 4.4): CMP-06, CMP-07."""
from __future__ import annotations

import json

from tests.conftest import mk_client
from tests.contract import check

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'


def _dataset(c, pid, cells, offset, name):
    lines = ['peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id']
    for i, x in enumerate(cells):
        obs = x['score_dpsi_raw'] + offset + (0.05 if i % 2 else -0.05)
        lines.append(f"p,{SEQ},{x['position']},{x['wt_aa']},{x['mut_aa']},{obs:.4f},r1")
    meta = {'name': name, 'assay': 'GPS', 'endpoint': 'delta_psi', 'units': 'PSI', 'source': 'test',
            'reference_description': 'typed', 'compatibility': 'zhang_gps_dpsi'}
    d = c.post(f'/v1/projects/{pid}/datasets', data={'metadata': json.dumps(meta)},
               files={'file': ('o.csv', '\n'.join(lines).encode(), 'text/csv')}).json()
    assert c.post(f"/v1/datasets/{d['dataset_id']}", json={'action': 'commit', 'acknowledge_warnings': True}).status_code == 200
    return d['dataset_id']


def test_cmp06_series_matches_saved_comparisons_and_flags_a_worse_point(mini, dbcopy, tmp_path):
    c, app = mk_client(mini, dbcopy, workspace_dir=tmp_path / 'ws')
    pid = c.post('/v1/projects', json={'name': 'agree'}).json()['project_id']
    a = c.post(f'/v1/projects/{pid}/analyses', json={'request': {'sequence': SEQ}}).json()
    cells = sorted(a['result']['cells'], key=lambda x: x['rank_in_tile'])[:10]
    saved = []
    for offset, name in ((0.0, 'run 1'), (0.02, 'run 2'), (1.5, 'run 3 other lab')):
        did = _dataset(c, pid, cells, offset, name)
        r = c.post(f"/v1/analyses/{a['analysis_id']}/comparisons", json={'dataset_id': did, 'aggregation': 'mean'})
        assert r.status_code == 201, r.text
        saved.append(r.json())
    before_default = app.state.core.registry.default_id
    s = c.get(f'/v1/projects/{pid}/agreement').json()
    check('AgreementSeries', s)
    assert [p['comparison_id'] for p in s['points']] == [x['comparison_id'] for x in saved]
    for p, x in zip(s['points'], saved, strict=True):
        assert (p['n'], p['mae'], p['spearman']) == (x['matched'], x['mae'], x['spearman'])
    assert [bool(p['flags']) for p in s['points']] == [False, False, True]
    assert s['points'][2]['flags'][0]['code'] == 'mae_worse' and s['flagged'] == 1
    assert 'does not by itself mean that the model is wrong' in s['caveat']
    # CMP-07: nothing automatic happened — same default model, registry unchanged, no new analysis or job
    assert app.state.core.registry.default_id == before_default
    assert c.get(f'/v1/projects/{pid}').json()['counts'] == {'analyses': 1, 'jobs': 0, 'datasets': 3}
    assert c.get('/v1/projects/00000000-0000-4000-8000-000000000000/agreement').status_code == 404
