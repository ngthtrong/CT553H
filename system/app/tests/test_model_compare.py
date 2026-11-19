"""Comparison of two saved analyses / two models (plan-system 2.2): CMP-01…03."""
from __future__ import annotations

import csv
import io

import numpy as np

from tests.conftest import mk_client
from tests.contract import check
from tests.test_seed_spread import _with_ensemble

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'
OTHER = 'MKTAYIAKQRQISFVKSHFSRQLEERLG'


def _ranks(v: np.ndarray) -> np.ndarray:
    order = np.argsort(v, kind='mergesort')
    r = np.empty(len(v))
    r[order] = np.arange(1, len(v) + 1)
    for x in np.unique(v):                                    # average ranks for ties
        m = v == x
        r[m] = r[m].mean()
    return r


def _setup(mini, dbcopy):
    c, app = mk_client(mini, dbcopy)
    _with_ensemble(app, dbcopy)                               # registers 'fake-lora' (DB row for the model FK)
    # make the second model really different: rescale and perturb its raw scores deterministically
    reg = app.state.core.registry
    inner = reg.models['fake-lora'].adapter

    class Shifted:
        calibrators, default_calibrator, training_sequences = ('platt',), 'platt', frozenset()

        def predict_tile(self, seq, calibrator=None):
            from degron_footprint.model import TilePrediction, rank_scores
            base = inner.predict_tile(seq, 'platt')
            score = base.score * 0.7 + np.sin(np.arange(len(base.score))) * 0.3
            prob = 1 / (1 + np.exp(-(2.0 * score - 1.0)))
            rank = rank_scores(score)
            return TilePrediction(positions=base.positions, wt=base.wt, mut=base.mut, score=score, prob=prob,
                                  rank=rank, top10=rank <= 54)
    reg.models['fake-lora'].adapter = Shifted()
    pid = c.post('/v1/projects', json={'name': 'cmp'}).json()['project_id']

    def save(body):
        r = c.post(f'/v1/projects/{pid}/analyses', json={'request': body})
        assert r.status_code == 201, r.text
        return r.json()
    a = save({'sequence': SEQ})
    b = save({'sequence': SEQ, 'model_id': 'fake-lora'})
    return c, pid, a, b, save


def test_cmp01_metrics_equal_numpy_and_cmp03_export_carries_both_provenances(mini, dbcopy):
    c, pid, a, b, _ = _setup(mini, dbcopy)
    r = c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id'], 'analysis_b': b['analysis_id']})
    assert r.status_code == 200, r.text
    out = r.json()
    check('ModelComparison', out)
    assert out['comparison_id'] is None and out['label'].startswith('Descriptive comparison')
    key = lambda x: (x['position'], x['mut_aa'])                                           # noqa: E731
    ca = sorted(a['result']['cells'], key=key)
    cb = sorted(b['result']['cells'], key=key)
    ra, rb = np.array([x['score_dpsi_raw'] for x in ca]), np.array([x['score_dpsi_raw'] for x in cb])
    pa, pb = np.array([x['p_dpsi_ge_1_calibrated'] for x in ca]), np.array([x['p_dpsi_ge_1_calibrated'] for x in cb])
    m = out['metrics']
    assert m['n_cells'] == 532
    assert abs(m['pearson_raw'] - np.corrcoef(ra, rb)[0, 1]) < 1e-12
    assert abs(m['spearman_raw'] - np.corrcoef(_ranks(ra), _ranks(rb))[0, 1]) < 1e-12
    assert abs(m['spearman_prob'] - np.corrcoef(_ranks(pa), _ranks(pb))[0, 1]) < 1e-12
    assert abs(m['mean_abs_diff_raw'] - np.mean(np.abs(ra - rb))) < 1e-12
    assert abs(m['mean_abs_diff_prob'] - np.mean(np.abs(pa - pb))) < 1e-12
    top_a = {key(x) for x in ca if x['rank_in_tile'] <= 54}
    top_b = {key(x) for x in cb if x['rank_in_tile'] <= 54}
    assert m['top_k_overlap'] == len(top_a & top_b)
    assert abs(m['top_k_jaccard'] - len(top_a & top_b) / len(top_a | top_b)) < 1e-12
    d = out['disagreements']
    assert len(d) == 20 and [abs(x['diff_prob']) for x in d] == sorted((abs(x['diff_prob']) for x in d), reverse=True)
    assert abs(abs(d[0]['diff_prob']) - np.max(np.abs(pa - pb))) < 1e-12
    assert out['provenance']['a']['model_id'] == 'test-model-v1' and out['provenance']['b']['model_id'] == 'fake-lora'
    # reproducible
    again = c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id'], 'analysis_b': b['analysis_id']}).json()
    assert again['metrics'] == m and again['disagreements'] == d
    # saved, listed, reopened identically, exported (CMP-03)
    s = c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id'], 'analysis_b': b['analysis_id'], 'save': True})
    assert s.status_code == 201
    cid = s.json()['comparison_id']
    got = c.get(f'/v1/model-comparisons/{cid}').json()
    check('ModelComparison', got)
    assert got['metrics'] == m and got['cells'] == out['cells']
    page = c.get(f'/v1/projects/{pid}/model-comparisons').json()
    check('ModelComparisonPage', page)
    assert page['total'] == 1 and page['items'][0]['model_b'] == 'fake-lora'
    assert c.get(f"/v1/projects/{pid}/model-comparisons?analysis_id={a['analysis_id']}").json()['total'] == 1
    text = c.get(f'/v1/model-comparisons/{cid}/export?format=csv').text
    comments = dict(ln[2:].split('=', 1) for ln in text.splitlines() if ln.startswith('# '))
    for side, ana in (('a', a), ('b', b)):
        assert comments[f'{side}_analysis_id'] == ana['analysis_id']
        assert comments[f'{side}_weights_sha256'] == ana['result']['provenance']['weights_sha256']
        assert comments[f'{side}_evidence_label'] == ana['result']['provenance']['evidence_label']
    rows = list(csv.reader(io.StringIO('\n'.join(ln for ln in text.splitlines() if not ln.startswith('#')))))
    assert rows[0][:7] == ['position', 'wt_aa', 'mut_aa', 'raw_a', 'raw_b', 'prob_a', 'prob_b'] and len(rows) == 533
    js = c.get(f'/v1/model-comparisons/{cid}/export?format=json')
    assert js.headers['content-disposition'].startswith('attachment;') and js.json()['provenance'] == got['provenance']


def test_cmp02_different_sequences_and_bad_requests_are_refused(mini, dbcopy):
    c, pid, a, b, save = _setup(mini, dbcopy)
    other = save({'sequence': OTHER})
    r = c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id'], 'analysis_b': other['analysis_id']})
    assert r.status_code == 422 and r.json()['field'] == 'analysis_b' and 'different tile sequences' in r.json()['message']
    r = c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id'], 'analysis_b': a['analysis_id']})
    assert r.status_code == 422
    assert c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id']}).status_code == 422
    assert c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id'], 'analysis_b': b['analysis_id'],
                                                'x': 1}).status_code == 422
    r = c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id'],
                                             'analysis_b': '00000000-0000-4000-8000-000000000000'})
    assert r.status_code == 404
    assert c.get('/v1/model-comparisons/00000000-0000-4000-8000-000000000000').status_code == 404
    assert c.get('/v1/model-comparisons/x/export?format=csv').status_code == 422


def test_deleting_an_analysis_removes_its_model_comparisons_after_confirmation(mini, dbcopy):
    c, pid, a, b, _ = _setup(mini, dbcopy)
    cid = c.post('/v1/analyses/compare', json={'analysis_a': a['analysis_id'], 'analysis_b': b['analysis_id'],
                                               'save': True}).json()['comparison_id']
    r = c.delete(f"/v1/analyses/{b['analysis_id']}?confirm=false")
    assert r.status_code == 409 and r.json()['dependencies']['model_comparisons'] == 1
    assert c.delete(f"/v1/analyses/{b['analysis_id']}?confirm=true").status_code == 204
    assert c.get(f'/v1/model-comparisons/{cid}').status_code == 404
    r = c.delete(f'/v1/projects/{pid}?confirm=false')
    assert r.status_code == 409 and r.json()['dependencies']['model_comparisons'] == 0
