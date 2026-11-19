"""Seed spread of the LoRA-D ensemble (plan-system 1.3): UNC-01…03 on the backend side."""
from __future__ import annotations

import csv
import io

import numpy as np
import pytest
from sqlalchemy import select

from db.models import AnalysisCell
from db.session import make_engine, make_session_factory
from degron_footprint.lora import LoraEnsembleModel, seed_spread
from degron_footprint.model import TilePrediction
from tests.conftest import mk_client
from tests.test_lora import REAL_MANIFEST, SEQ, _OnlyPlatt


class _Ensemble(_OnlyPlatt):
    """The npz scores plus a deterministic three-seed spread around them (shape and order of a real ensemble)."""

    def predict_tile(self, seq, calibrator=None):
        base = self.inner.predict_tile(seq, 'platt')
        offs = np.array([-0.1, 0.0, 0.25])[:, None] * (1 + np.arange(len(base.score)) % 3)[None, :]
        per_seed = base.score[None, :] + offs
        return TilePrediction(positions=base.positions, wt=base.wt, mut=base.mut, score=base.score, prob=base.prob,
                              rank=base.rank, top10=base.top10, seed_sd=seed_spread(per_seed),
                              seed_min=per_seed.min(0), seed_max=per_seed.max(0))


def _with_ensemble(app, url):
    """Register 'fake-lora' (a clone of the npz row, so saved analyses satisfy the model FK) served by _Ensemble."""
    from api.service import LoadedModel
    from db.models import ModelVersion
    eng = make_engine(url)
    with make_session_factory(eng)() as s, s.begin():
        row = s.get(ModelVersion, 'test-model-v1')
        clone = ModelVersion(**{k: getattr(row, k) for k in ModelVersion.__table__.columns.keys()})
        clone.model_id, clone.is_default = 'fake-lora', False
        s.add(clone)
    eng.dispose()
    reg = app.state.core.registry
    base = reg.models['test-model-v1']
    reg.models['fake-lora'] = LoadedModel(base.info.__class__(**{**base.info.__dict__, 'model_id': 'fake-lora',
                                                                  'kind': 'torch_lora'}),
                                          _Ensemble(base.adapter), False)


def test_seed_spread_definition_is_population_sd():
    per_seed = np.array([[1.0, 2.0], [3.0, 2.0], [5.0, 2.0]], dtype=np.float32)
    assert seed_spread(per_seed).tolist() == [pytest.approx(np.sqrt(8 / 3)), 0.0]
    assert seed_spread(per_seed).dtype == np.float64


@pytest.mark.realdata
@pytest.mark.skipif(REAL_MANIFEST is None or not REAL_MANIFEST.is_file(), reason='LoRA-D bundle not exported')
def test_unc01_seed_sd_matches_the_parity_fixture_exactly():
    """UNC-01: the served SD equals np.std(ddof=0) of the fixture's per-seed arrays, bit for bit (the network itself is
    covered by the parity test; here raw_scores returns the fixture so torch is not needed)."""
    assert REAL_MANIFEST is not None
    import json
    manifest = json.loads(REAL_MANIFEST.read_text())
    model = LoraEnsembleModel.__new__(LoraEnsembleModel)
    model.manifest, model.bundle = manifest, REAL_MANIFEST.parent / manifest['bundle_dir']
    cal = np.load(model.bundle / manifest['calibrator']['file'], allow_pickle=False)
    model.cal_coef = np.asarray(cal['coef'], dtype=np.float64).reshape(-1)
    model.cal_intercept = np.asarray(cal['intercept'], dtype=np.float64)
    model.default_calibrator = 'platt'
    fx = np.load(model.bundle / 'parity-fixture.npz', allow_pickle=False)
    from degron_footprint.features import substitutions
    for tile in ('tile_w', 'tile_typed'):
        seq, per_seed = str(fx[f'{tile}_sequence']), fx[f'{tile}_per_seed']
        model.raw_scores = lambda s, _p=per_seed: (_p.astype(np.float64), substitutions(s))   # type: ignore[method-assign]
        pred = model.predict_tile(seq)
        expect = np.std(per_seed.astype(np.float64), axis=0, ddof=0)
        assert np.array_equal(pred.seed_sd, expect)
        assert np.array_equal(pred.seed_min, per_seed.astype(np.float64).min(0))
        assert np.array_equal(pred.seed_max, per_seed.astype(np.float64).max(0))
        assert np.array_equal(pred.score.astype(np.float32), fx[f'{tile}_score'])       # ensemble score unchanged
        assert np.allclose(pred.prob, fx[f'{tile}_prob'], rtol=0, atol=1e-12)


def test_unc02_npz_model_returns_null_spread(client):
    cells = client.post('/v1/predict', json={'sequence': SEQ}).json()['cells']
    assert all(c['score_seed_sd'] is None and c['score_seed_min'] is None and c['score_seed_max'] is None for c in cells)


def test_unc03_ensemble_spread_in_api_snapshot_export_and_share(mini, dbcopy):
    c, app = mk_client(mini, dbcopy)
    _with_ensemble(app, dbcopy)
    r = c.post('/v1/predict', json={'sequence': SEQ, 'model_id': 'fake-lora'}).json()
    cells = r['cells']
    assert all(c_['score_seed_sd'] >= 0 and c_['score_seed_min'] <= c_['score_dpsi_raw'] + 0.3 for c_ in cells)
    assert all(c_['score_seed_min'] <= c_['score_seed_max'] for c_ in cells)
    # the stateless CSV export: nine FR-12 columns first, then the spread
    text = c.post('/v1/export', json={'sequence': SEQ, 'model_id': 'fake-lora', 'format': 'csv'}).text
    rows = list(csv.reader(io.StringIO('\n'.join(ln for ln in text.splitlines() if not ln.startswith('#')))))
    assert rows[0][9:] == ['score_seed_sd', 'score_seed_min', 'score_seed_max']
    assert float(rows[1][9]) == pytest.approx(cells[0]['score_seed_sd'], rel=1e-9)
    # a saved analysis keeps the spread in the snapshot and in analysis_cell
    pid = c.post('/v1/projects', json={'name': 'seed spread'}).json()['project_id']
    saved = c.post(f'/v1/projects/{pid}/analyses', json={'request': {'sequence': SEQ, 'model_id': 'fake-lora'}})
    assert saved.status_code == 201, saved.text
    a = saved.json()
    assert [x['score_seed_sd'] for x in a['result']['cells']] == [x['score_seed_sd'] for x in cells]
    eng = make_engine(dbcopy)
    with make_session_factory(eng)() as s:
        stored = s.scalars(select(AnalysisCell).where(AnalysisCell.analysis_id == a['analysis_id'])
                           .order_by(AnalysisCell.position, AnalysisCell.mut_aa)).all()
    eng.dispose()
    by_key = {(x['position'], x['mut_aa']): x for x in cells}
    assert all(row.score_seed_sd == by_key[(row.position, row.mut_aa)]['score_seed_sd'] for row in stored)
    # a share link rebuilt from prediction_cell is identical, spread included
    j = c.post('/v1/runs', json={'sequence': SEQ, 'model_id': 'fake-lora', 'ttl_days': 1}).json()
    again = c.get(f"/v1/runs/{j['run_id']}", headers={'X-Share-Token': j['share_token']}).json()
    assert again == j['result'] and again['cells'][0]['score_seed_sd'] is not None
