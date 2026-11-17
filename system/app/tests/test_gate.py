"""WP7: the R3 domain gate (DOM-01, ETL-05 of test-plan.md; DEVIATIONS.md §7). Golden tests against the research code
research/r3-domain-gate-2026-10-22/run_r3.py and its frozen outputs."""
from __future__ import annotations

import importlib.util
import json
import math
import shutil
from pathlib import Path

import numpy as np
import pytest

from degron_footprint.domain import NullGate, load_gate
from degron_footprint.gate_r3 import R3Gate, card_for, features, features_matrix, sigmoid

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'CLAUDE.md').exists())
R3 = ROOT / 'research/r3-domain-gate-2026-10-22'
CARD = json.loads((R3 / 'run-kaggle-20261022/gate-card.json').read_text(encoding='utf-8'))
AAS = 'ACDEFGHIKLMNPQRSTVWY'


@pytest.fixture(scope='module')
def run_r3():
    spec = importlib.util.spec_from_file_location('run_r3_golden', R3 / 'run_r3.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)                      # module level only defines constants and functions
    return mod


@pytest.fixture(scope='module')
def seqs():
    rng = np.random.default_rng(17)
    out = [''.join(rng.choice(list(AAS), 28)) for _ in range(500)]
    return out + ['A' * 28, 'W' * 28, 'DIMFLVDSSGSIGPENFSKMKTFMKNLV']


def test_dom01_features_equal_research(run_r3, seqs):
    assert run_r3.AAS == AAS and run_r3.NF == 420
    S = np.array([[run_r3.AA2I[c] for c in s] for s in seqs], dtype=np.int8)
    ref = run_r3.feats(S)
    assert np.array_equal(features_matrix(seqs), ref)
    assert all(np.array_equal(features(s), ref[i]) for i, s in enumerate(seqs[:50]))


def test_dom01_tier2_is_raw_counts_times_coef_plus_intercept(run_r3, seqs, r3_gate):
    """run_r3.fit returns b = ȳ − x̄·coef, so the prediction is feats·coef + b on raw (uncentred) counts; this closes
    the open question of DEVIATIONS.md §7 about the centring of the intercept."""
    z = np.load(R3 / 'run-kaggle-20261022/gate-weights.npz')
    S = np.array([[run_r3.AA2I[c] for c in s] for s in seqs], dtype=np.int8)
    ref = run_r3.feats(S) @ z['tier2_coef'] + z['tier2_intercept'][0]
    got = np.array([r3_gate.predict_screen_psi(s) for s in seqs])
    assert np.max(np.abs(got - ref)) < 1e-12
    st, _ = zip(*r3_gate.assess_many(seqs), strict=True)
    one = [r3_gate.assess(s).status for s in seqs]
    assert list(st) == one


def test_dom01_cuts_and_coefficients_match_the_card(run_r3, r3_gate):
    cuts = r3_gate.cuts()
    assert cuts['tier1']['in_at_or_below'] == pytest.approx(CARD['tier1']['x_cut_for_P_in'], abs=1e-12)
    assert cuts['tier1']['out_at_or_above'] == pytest.approx(CARD['tier1']['x_cut_for_P_out'], abs=1e-12)
    assert cuts['tier2']['in_at_or_below'] == pytest.approx(CARD['tier2']['x_cut_for_P_in'], abs=1e-12)
    assert cuts['tier2']['out_at_or_above'] == pytest.approx(CARD['tier2']['x_cut_for_P_out'], abs=1e-12)
    assert r3_gate.m1 == pytest.approx((10.187, -3.275), abs=5e-4) and r3_gate.m2 == pytest.approx((8.457, -1.911), abs=5e-4)
    assert (r3_gate.p_in, r3_gate.p_out) == (run_r3.P_IN, run_r3.P_OUT)


@pytest.mark.parametrize('x, status', [(1.0, 'measured_in_domain'), (2.68, 'measured_in_domain'),
                                       (2.70, 'measured_borderline'), (3.10, 'measured_borderline'),
                                       (3.12, 'measured_out_of_domain'), (4.0, 'measured_out_of_domain')])
def test_dom01_tier1_three_states(r3_gate, x, status):
    assert r3_gate.tier1_status(x) == status


def test_sigmoid_is_stable():
    assert sigmoid(1000.0) == 1.0 and sigmoid(-1000.0) == 0.0
    assert sigmoid(0.0) == 0.5 and math.isclose(sigmoid(2.0) + sigmoid(-2.0), 1.0)


def test_typed_sequence_with_nonstandard_residue_is_not_assessed(r3_gate):
    assert r3_gate.assess('A' * 27 + 'X') is None and r3_gate.assess('A' * 27) is None


def test_tampered_weights_disable_the_gate(tmp_path):
    w = tmp_path / 'gate-r3-v1.npz'
    shutil.copyfile(R3 / 'run-kaggle-20261022/gate-weights.npz', w)
    card = card_for(w, 'gate-r3-v1', CARD)
    (tmp_path / 'gate.json').write_text(json.dumps(card))
    assert isinstance(load_gate(None, tmp_path / 'gate.json'), R3Gate)
    card['weights_sha256'] = '0' * 64
    (tmp_path / 'gate.json').write_text(json.dumps(card))
    assert isinstance(load_gate(None, tmp_path / 'gate.json'), NullGate)
    assert isinstance(load_gate(None, tmp_path / 'missing.json'), NullGate)


def test_api_borderline_is_scored_with_a_warning_and_out_is_refused(client):
    """D-5 as proposed: borderline is scored with a warning; out-of-domain is refused unless overridden."""
    tile1 = client.get('/v1/proteins/P12345/tiles').json()['tiles'][0]['sequence']
    j = client.post('/v1/predict', json={'sequence': tile1}).json()
    assert j['domain']['status'] == 'predicted_borderline' and len(j['cells']) == 532
    assert 'DOMAIN_BORDERLINE' in [w['code'] for w in j['warnings']]
    r = client.post('/v1/predict', json={'sequence': 'A' * 28})          # x̂ ≈ 5.29 → P ≈ 0.16
    assert r.status_code == 422 and r.json()['code'] == 'OUT_OF_DOMAIN' and '4.0' not in r.json()['message']
    j = client.post('/v1/predict', json={'sequence': 'A' * 28, 'override_domain': True}).json()
    assert j['domain']['status'] == 'predicted_out_of_domain'
    assert j['domain']['psi_wt_measured'] is None
