"""Candidates to verify (plan-system 2.6)."""
from __future__ import annotations

from tests.contract import check
from tests.test_model_compare import _setup


def test_suggestions_are_reproducible_and_every_candidate_has_reasons(mini, dbcopy):
    c, pid, a, b, save = _setup(mini, dbcopy)            # a: npz, b: a rescaled second model on the same tile
    url = f"/v1/analyses/{a['analysis_id']}/suggestions?compare_with={b['analysis_id']}&limit=30"
    r = c.get(url)
    assert r.status_code == 200, r.text
    data = r.json()
    check('Suggestions', data)
    assert data['label'].startswith('Retrospective priority list')
    assert data['candidates'] and all(x['reasons'] for x in data['candidates'])
    assert {x['code'] for x in data['candidates'][0]['reasons']} >= {'models_disagree'}
    for x in data['candidates']:
        for reason in x['reasons']:
            if reason['code'] == 'models_disagree':
                assert abs(x['prob_other'] - x['prob']) >= 0.2 and abs(reason['value'] - (x['prob_other'] - x['prob'])) < 1e-12
    # order: reasons count, then the higher probability
    keys = [(-len(x['reasons']), -max(x['prob'], x['prob_other'] or -1)) for x in data['candidates']]
    assert keys == sorted(keys)
    assert c.get(url).json() == data                     # same input, same list
    # the npz model has no seed spread: no high_score_uncertain reason
    assert all(rr['code'] != 'high_score_uncertain' for x in data['candidates'] for rr in x['reasons'])
    csv_text = c.get(url + '&format=csv').text
    assert csv_text.splitlines()[0].startswith('# analysis_id=') and 'models_disagree' not in csv_text
    assert 'P differs by' in csv_text
    # without a second analysis, nothing disagrees: only ClinVar reasons (if any) remain
    alone = c.get(f"/v1/analyses/{a['analysis_id']}/suggestions").json()
    assert all(rr['code'] == 'clinvar_variant' for x in alone['candidates'] for rr in x['reasons'])


def test_suggestions_with_seed_spread_and_out_of_domain(mini, dbcopy):
    from tests.test_seed_spread import _Ensemble
    c, pid, a, b, save = _setup(mini, dbcopy)
    app = c.app
    reg = app.state.core.registry
    base = reg.models['test-model-v1']
    reg.models['fake-lora'].adapter = _Ensemble(base.adapter)        # ensemble with seed spread
    e = save({'sequence': 'MKTAYIAKQRQISFVKSHFSRQLEERLG', 'model_id': 'fake-lora'})
    data = c.get(f"/v1/analyses/{e['analysis_id']}/suggestions?limit=100").json()
    cut = data['criteria']['spread_cut']
    assert cut is not None
    hs = [x for x in data['candidates'] if any(r['code'] == 'high_score_uncertain' for r in x['reasons'])]
    assert hs and all(x['rank_in_tile'] <= 54 and x['score_seed_sd'] >= cut for x in hs)
    # a tile scored outside the domain (override): no candidates unless asked
    out = save({'uniprot_id': 'P12345', 'tile_index': 2, 'override_domain': True})
    d = c.get(f"/v1/analyses/{out['analysis_id']}/suggestions").json()
    assert d['candidates'] == [] and 'outside the training domain' in d['excluded_reason']
    d2 = c.get(f"/v1/analyses/{out['analysis_id']}/suggestions?include_out_of_domain=true").json()
    assert d2['excluded_reason'] is None
    # bad requests
    assert c.get(f"/v1/analyses/{a['analysis_id']}/suggestions?compare_with={e['analysis_id']}").status_code == 422
    assert c.get(f"/v1/analyses/{a['analysis_id']}/suggestions?limit=0").status_code == 422
    assert c.get(f"/v1/analyses/{a['analysis_id']}/suggestions?format=xml").status_code == 400


def test_clinvar_variants_of_the_snapshot_become_reasons(mini, dbcopy):
    c, pid, a, b, save = _setup(mini, dbcopy)
    t = save({'uniprot_id': 'P12345', 'tile_index': 1})
    variants = [v for v in c.get(f"/v1/analyses/{t['analysis_id']}").json()['snapshot']['annotations']['clinvar']['variants']
                if v.get('residue_matches') is not False]
    assert variants
    data = c.get(f"/v1/analyses/{t['analysis_id']}/suggestions?limit=100").json()
    got = {(x['position'], x['mut_aa']) for x in data['candidates'] if any(r['code'] == 'clinvar_variant' for r in x['reasons'])}
    assert got == {(v['position'], v['alt_aa']) for v in variants}
    assert all('not a diagnosis' in r['text'] for x in data['candidates'] for r in x['reasons'] if r['code'] == 'clinvar_variant')
