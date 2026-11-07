"""RG group of test-plan.md §6.3 and the real-data parts of UT-01 and ETL-04/05.

These tests need the research data (marker `realdata`; skipped when the data tree is absent). They compare the
service path with the research path (calibration-p6 predict.py / trainpath.npz) on all 92,337 training cells.
What this shows and does not show is stated in test-plan.md §2: a shared error in the labels or weights would pass.
"""
from __future__ import annotations

import csv
import importlib.util
import io

import numpy as np
import pytest
import yaml
from fastapi.testclient import TestClient
from sqlalchemy import select

from api.main import create_app
from db.models import MeasuredCell, Tile
from db.session import make_engine
from degron_footprint.features import feature_matrix
from degron_footprint.model import RidgePlattModel, sha256_file
from etl import load as etl

from .conftest import APP, CONTRACT, TOPIC, settings_for

pytestmark = pytest.mark.realdata
RESEARCH = TOPIC / 'research/calibration-p6-2026-10-22' if TOPIC else None
SOURCE_WEIGHTS = TOPIC / 'data/processed/calibration-p6-model.npz' if TOPIC else None
TOL = 1e-9


@pytest.fixture(scope='module')
def real(tmp_path_factory):
    from alembic import command
    from alembic.config import Config
    root = tmp_path_factory.mktemp('real')
    url = f'sqlite:///{root / "real.db"}'
    cfg = Config(str(APP / 'backend/alembic.ini'))
    cfg.set_main_option('sqlalchemy.url', url)
    command.upgrade(cfg, 'head')
    report = etl.run(url, None, None, None, 'none', root / 'models')
    app = create_app(settings_for({'model_dir': root / 'models'}, url))
    return {'url': url, 'report': report, 'client': TestClient(app), 'app': app, 'models': root / 'models'}


@pytest.fixture(scope='module')
def research_predict():
    spec = importlib.util.spec_from_file_location('research_predict', RESEARCH / 'predict.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_etl05_real_report(real):
    r = real['report']
    assert r['training_peptides'] == 176 and r['training_cells'] == 92337 and r['training_tile_mismatches'] == 0
    assert r['tables']['protein']['inserted'] == 20431
    # inputs are pinned by SHA-256, so the counts are fixed; a change means the ETL or an input changed
    assert r['tables']['tile']['inserted'] == 482216
    assert r['tiles_per_domain_status'] == {'measured_in_domain': 187550, 'measured_out_of_domain': 160230,
                                            'measured_unreliable': 108005, 'unknown': 26397}
    assert r['screen_rows'] == 475506 and r['screen_rows_unmatched'] == 19687
    assert r['screen_rows_unmatched_reasons']['beyond_last_window_by_1'] == 16266
    assert all(v >= 0 for v in r['tiles_per_domain_status'].values())


def test_rg03_weights_hash(real):
    packaged = real['models'] / 'm3-ext4.0-platt-v1.npz'
    h = sha256_file(packaged)
    assert h == sha256_file(SOURCE_WEIGHTS) == '8bec0b04bdc7da698da98d91adea944dd43583f93bc67233600e6ae0075cd9c3'
    card = real['client'].get('/v1/models/m3-ext4.0-platt-v1').json()
    assert card['weights_sha256'] == h
    example = yaml.safe_load(CONTRACT.read_text())['paths']['/v1/predict']['post']['responses']['200']['content'][
        'application/json']['examples']['firstCells']['value']
    assert example['provenance']['weights_sha256'] == h


def test_ut01_features_equal_research_featurize(real, research_predict):
    """The vectorised builder equals the per-cell loop of predict.py on every cell of the 176 training tiles."""
    worst = 0.0
    n = 0
    with make_engine(real['url']).connect() as c:
        tiles = c.execute(select(Tile.sequence).join(MeasuredCell, MeasuredCell.tile_id == Tile.tile_id).distinct()).scalars().all()
    assert len(tiles) == 176
    for seq in tiles:
        X, cells = feature_matrix(seq)
        ref = np.array([research_predict.featurize(seq, p, a) for p, a in cells])
        worst = max(worst, float(np.abs(X - ref).max()))
        n += len(cells)
    assert n == 176 * 532 and worst < TOL


def test_ut01_features_equal_training_matrix(real):
    """The 180 features built from the UniProt-derived tile equal the matrix X the model was trained on (92,337 rows)."""
    z = np.load(TOPIC / 'data/processed/learning-curve-sat-ext4.0.npz', allow_pickle=False)
    X = z['X']
    with make_engine(real['url']).connect() as c:
        tmap = {(r.uniprot_acc, r.tile_index): (r.tile_id, r.sequence) for r in c.execute(select(
            Tile.uniprot_acc, Tile.tile_index, Tile.tile_id, Tile.sequence).join(
            MeasuredCell, MeasuredCell.tile_id == Tile.tile_id).distinct())}
        cells_of: dict[int, list[tuple[int, str]]] = {}
        for r in c.execute(select(MeasuredCell.tile_id, MeasuredCell.position, MeasuredCell.mut_aa)
                           .order_by(MeasuredCell.tile_id, MeasuredCell.position, MeasuredCell.mut_aa)):
            cells_of.setdefault(r.tile_id, []).append((r.position, r.mut_aa))
    worst, n = 0.0, 0
    for pep, (a, b) in zip(z['peps'], z['idx'], strict=False):
        tile_id, seq = tmap[(str(pep).split('_')[0], int(str(pep).split('_')[-1]))]
        Xt, cells = feature_matrix(seq)
        ix = {c: i for i, c in enumerate(cells)}
        sel = [ix[c] for c in cells_of[tile_id]]
        assert len(sel) == b - a
        worst = max(worst, float(np.abs(Xt[sel] - X[a:b, :180]).max()))
        n += b - a
    assert n == 92337 and worst < TOL, worst


def test_rg01_scores_equal_training_path(real):
    """All 92,337 cells: raw score, Platt and isotonic probability through the service model vs trainpath.npz."""
    tp = np.load(TOPIC / 'data/processed/calibration-p6-trainpath.npz', allow_pickle=False)
    model = RidgePlattModel.from_file('m', real['models'] / 'm3-ext4.0-platt-v1.npz', None)
    with make_engine(real['url']).connect() as c:
        tmap = {(r.uniprot_acc, r.tile_index): (r.tile_id, r.sequence) for r in c.execute(select(
            Tile.uniprot_acc, Tile.tile_index, Tile.tile_id, Tile.sequence).join(
            MeasuredCell, MeasuredCell.tile_id == Tile.tile_id).distinct())}
        cells_of = {}
        for r in c.execute(select(MeasuredCell.tile_id, MeasuredCell.position, MeasuredCell.mut_aa)
                           .order_by(MeasuredCell.tile_id, MeasuredCell.position, MeasuredCell.mut_aa)):
            cells_of.setdefault(r.tile_id, []).append((r.position, r.mut_aa))
    worst = {'score': 0.0, 'platt': 0.0, 'iso': 0.0}
    n = 0
    for pep, (a, b) in zip(tp['peps'], tp['idx'], strict=False):
        acc, tn = str(pep).split('_')[0], int(str(pep).split('_')[-1])
        tile_id, seq = tmap[(acc, tn)]
        want = cells_of[tile_id]
        assert len(want) == b - a
        pr = model.predict_tile(seq, 'platt')
        pi = model.predict_tile(seq, 'iso')
        lut = {(int(p), m): i for i, (p, m) in enumerate(zip(pr.positions, pr.mut, strict=False))}
        sel = [lut[w] for w in want]
        worst['score'] = max(worst['score'], float(np.abs(pr.score[sel] - tp['score'][a:b]).max()))
        worst['platt'] = max(worst['platt'], float(np.abs(pr.prob[sel] - tp['platt'][a:b]).max()))
        worst['iso'] = max(worst['iso'], float(np.abs(pi.prob[sel] - tp['iso'][a:b]).max()))
        n += b - a
    assert n == 92337
    assert max(worst.values()) < TOL, worst


def test_rg02_api_csv_equals_golden_file(real):
    r = real['client'].post('/v1/export', json={'uniprot_id': 'A6NMZ7', 'tile_index': 28, 'format': 'csv'})
    assert r.status_code == 200
    got = list(csv.DictReader(io.StringIO('\n'.join(x for x in r.text.split('\n') if not x.startswith('#')))))
    want = list(csv.DictReader((RESEARCH / 'example-output.csv').open()))
    assert len(got) == len(want) == 532
    for g, w in zip(got, want, strict=False):
        for k in ('tile', 'position', 'wt_aa', 'mut_aa', 'rank_in_tile', 'top10pct_in_tile'):
            assert g[k] == w[k], (k, g, w)
        assert abs(float(g['score_dpsi_raw']) - float(w['score_dpsi_raw'])) < 5e-9
        assert abs(float(g['p_dpsi_ge_1_calibrated']) - float(w['p_dpsi_ge_1_calibrated'])) < 5e-9
    assert got[0]['peptide'] == 'A6NMZ7_28' and want[0]['peptide'] == 'A6NMZ7_28'


def test_api_json_matches_contract_example(real):
    ex = yaml.safe_load(CONTRACT.read_text())['paths']['/v1/predict']['post']['responses']['200']['content'][
        'application/json']['examples']['firstCells']['value']
    j = real['client'].post('/v1/predict', json={'uniprot_id': 'A6NMZ7', 'tile_index': 28}).json()
    assert j['tile'] == ex['tile']
    assert j['domain']['status'] == ex['domain']['status']
    assert abs(j['domain']['psi_wt_measured'] - ex['domain']['psi_wt_measured']) < 1e-12
    assert abs(j['domain']['reads_measured'] - ex['domain']['reads_measured']) < 1e-9
    assert [w['code'] for w in j['warnings']] == [w['code'] for w in ex['warnings']]
    for got, want in zip(j['cells'][:3], ex['cells'], strict=False):
        assert got['rank_in_tile'] == want['rank_in_tile'] and got['top10pct_in_tile'] == want['top10pct_in_tile']
        assert abs(got['score_dpsi_raw'] - want['score_dpsi_raw']) < 1e-9
        assert abs(got['p_dpsi_ge_1_calibrated'] - want['p_dpsi_ge_1_calibrated']) < 1e-9
    assert j['provenance']['weights_sha256'] == ex['provenance']['weights_sha256']


def test_real_domain_gate_values(real):
    """Tile 28 of A6NMZ7 is measured in domain; a stable tile of the screen is refused unless overridden."""
    c = real['client']
    with make_engine(real['url']).connect() as conn:
        stable = conn.execute(select(Tile.uniprot_acc, Tile.tile_index, Tile.psi_wt_measured).where(
            Tile.domain_status == 'measured_out_of_domain').limit(1)).one()
    r = c.post('/v1/predict', json={'uniprot_id': stable.uniprot_acc, 'tile_index': stable.tile_index})
    assert r.status_code == 422 and r.json()['code'] == 'OUT_OF_DOMAIN'
    r = c.post('/v1/predict', json={'uniprot_id': stable.uniprot_acc, 'tile_index': stable.tile_index,
                                    'override_domain': True})
    assert r.status_code == 200 and r.json()['domain']['psi_wt_measured'] == pytest.approx(stable.psi_wt_measured)
