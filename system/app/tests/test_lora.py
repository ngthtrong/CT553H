"""Optional LoRA-D model (plan 2.12, WP10): bundle verification, registry/default selection, calibrator errors, ETL
registration, and parity of the serving implementation with the research implementation (when PyTorch is installed and
the exported bundle exists in data/processed)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml
from sqlalchemy import select

import etl.load as etl
from db.models import ModelVersion
from db.session import make_engine, make_session_factory
from degron_footprint.features import feature_matrix, substitutions
from degron_footprint.lora import LoraEnsembleModel, composition_features, learned_state_digest, softmax_rows
from degron_footprint.model import WeightsError
from tests import minidata
from tests.conftest import BACKEND, TOPIC, mk_client, pg_create, pg_drop

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'
REAL_MANIFEST = (TOPIC / 'data/processed/lora-d-serving-v1/esm2-35m-lora-d-v1.json') if TOPIC else None
HAVE_TORCH = importlib.util.find_spec('torch') is not None and importlib.util.find_spec('transformers') is not None


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fake_bundle(root: Path, model_id: str = 'esm2-35m-lora-d-aa4fc2b7') -> Path:
    """A structurally valid bundle with tiny placeholder weights (enough for hashing, ETL and registry tests)."""
    name = 'esm2-35m-lora-d-v1'
    b = root / name
    (b / 'base').mkdir(parents=True)
    np.savez(b / 'calibrator.npz', coef=np.array([[-2.0], [0.0], [2.0]]), intercept=np.array([0.5, 1.0, -1.5]),
             classes=np.array([0, 1, 2]))
    names = ['head.3.bias']
    np.savez(b / 'adapter-seed17.npz', __order__=np.array(names), **{'head.3.bias': np.zeros(1, np.float32)})
    (b / 'base' / 'config.json').write_text('{}')
    (b / 'training-sequences.txt').write_text(SEQ + '\n')
    files = {f.relative_to(b).as_posix(): {'sha256': sha(f), 'bytes': f.stat().st_size}
             for f in sorted(b.rglob('*')) if f.is_file()}
    contrast = {'delta': -0.04, 'ci_adjusted': [-0.05, -0.03], 'multiplicity': 2, 'peptides': 10, 'clusters': 5,
                'bootstrap': 50}
    manifest = {
        'schema_version': 1, 'kind': 'torch_lora', 'model_id': model_id, 'bundle_dir': name,
        'scientific_status': 'development_not_gate_closure', 'serving_promotion': 'not_authorized_by_research_execution',
        'claim_boundary': 'test bundle', 'base': {'repo': 'facebook/esm2_t12_35M_UR50D', 'revision': 'r' * 40,
                                                   'dir': 'base', 'dtype': 'float32'},
        'adapter': {'rank': 8, 'alpha': 16, 'targets': ['query', 'value']}, 'features': 'test features',
        'seeds': [{'seed': 17, 'file': 'adapter-seed17.npz', 'learned_state_sha256': learned_state_digest(
            names, {'head.3.bias': np.zeros(1, np.float32)})}],
        'calibrator': {'file': 'calibrator.npz', 'fit': 'ensemble OOF W only', 'train_cells': 10, 'T_fit_cells': 0},
        'training': {'cells': 10}, 'event_definition': 'P(DeltaPSI >= 1.0)',
        'training_sequences': {'file': 'training-sequences.txt', 'count': 1},
        'evaluation': {'evaluation': 'test', 'denominators': {'peptides': 10, 'groups': 5}, 'peptide_macro_mae': 0.3,
                       'contrasts': {'esm2_35m-lora-D_minus_esm2_35m-frozen-D': contrast,
                                     'esm2_35m-lora-D_minus_ordered-w5-D': contrast},
                       'gt5_peptide_macro_mae': {'esm2_35m-lora-D': 0.36, 'zero': 0.35}},
        'files': files}
    m = root / f'{name}.json'
    m.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    return m


# ----------------------------------------------------------------------------- pure functions
def test_composition_features_equal_the_first_60_m3_features():
    X, cells = feature_matrix(SEQ)
    np.testing.assert_allclose(composition_features(SEQ, cells), X[:, :60].astype(np.float32), atol=1e-7)


def test_calibrator_softmax_rows_sum_to_one_and_are_monotone_in_the_event():
    p = softmax_rows(np.outer(np.linspace(-3, 3, 61), [-2.0, 0.0, 2.0]) + np.array([0.5, 1.0, -1.5]))
    assert np.allclose(p.sum(1), 1) and np.all(np.diff(p[:, 2]) > 0)


# ----------------------------------------------------------------------------- bundle verification (NFR-06)
def test_bundle_hash_checks(tmp_path, monkeypatch):
    m = fake_bundle(tmp_path)
    with pytest.raises(WeightsError, match='registered value'):
        LoraEnsembleModel.from_file('x', m, '0' * 64)
    with pytest.raises(WeightsError, match='missing'):
        LoraEnsembleModel.from_file('x', tmp_path / 'nope.json', None)
    monkeypatch.setitem(sys.modules, 'torch', None)          # whatever is installed: behave as without PyTorch
    with pytest.raises(WeightsError, match='PyTorch'):
        LoraEnsembleModel.from_file('x', m, sha(m))
    (m.parent / 'esm2-35m-lora-d-v1' / 'base' / 'config.json').write_text('{"tampered": true}')
    with pytest.raises(WeightsError, match='differs from the manifest'):
        LoraEnsembleModel.from_file('x', m, sha(m))


# ----------------------------------------------------------------------------- ETL registration
def lora_tree(root: Path) -> dict:
    staging = root / 'staging'
    staging.mkdir()
    m = fake_bundle(staging)
    mini = minidata.build(root, extra_sources=[{
        'source_id': 'own-model-esm2-35m-lora-d-v1', 'name': 'lora', 'version': 'test', 'citation': 'test',
        'url': None, 'license_name': 'test', 'license_class': 'open', 'redistribution_ok': True,
        'attribution_text': 'lora test', 'retrieved_on': '2026-11-17',
        'files': [{'role': 'lora_manifest', 'path': 'processed/lora/esm2-35m-lora-d-v1.json', 'sha256': sha(m)}]}])
    dest = mini['topic'] / 'data/processed/lora'
    dest.mkdir(parents=True)
    (staging / 'esm2-35m-lora-d-v1.json').rename(dest / 'esm2-35m-lora-d-v1.json')
    (staging / 'esm2-35m-lora-d-v1').rename(dest / 'esm2-35m-lora-d-v1')
    params = yaml.safe_load(mini['params'].read_text())
    params['lora'] = {'model_id': 'esm2-35m-lora-d-aa4fc2b7', 'manifest_file': 'esm2-35m-lora-d-v1.json',
                      'frozen_at': '2026-11-16T20:59:00+00:00', 'domain_description': 'test'}
    mini['params'].write_text(yaml.safe_dump(params))
    mini['lora_dir'] = dest
    return mini


def migrated(tmp_path) -> str:
    from alembic import command
    from alembic.config import Config
    url = pg_create() if BACKEND == 'postgresql' else f'sqlite:///{tmp_path / "lora.db"}'
    cfg = Config(str(Path(etl.APP_DIR) / 'backend/alembic.ini'))
    cfg.set_main_option('sqlalchemy.url', url)
    command.upgrade(cfg, 'head')
    return url


def test_etl_registers_lora_as_frozen_non_default_then_is_idempotent_and_refuses_tampering(tmp_path, monkeypatch):
    mini = lora_tree(tmp_path)
    url = migrated(tmp_path)
    try:
        rep = etl.run(url, mini['topic'], mini['sources'], mini['params'], 'none', mini['model_dir'])
        assert rep['lora_manifest_sha256'] == sha(mini['model_dir'] / 'esm2-35m-lora-d-v1.json')
        engine = make_engine(url)
        with make_session_factory(engine)() as s:
            rows = {r.model_id: r for r in s.execute(select(ModelVersion)).scalars()}
        lora = rows['esm2-35m-lora-d-aa4fc2b7']
        assert (lora.kind, lora.status, lora.is_default, lora.role) == ('torch_lora', 'frozen', False, 'effect')
        assert rows['test-model-v1'].is_default is True
        assert 'not external validation' in lora.evidence_label and 'zero predictor is' in lora.card_markdown
        again = etl.run(url, mini['topic'], mini['sources'], mini['params'], 'none', mini['model_dir'])
        assert again['tables']['model_version'].get('inserted', 0) == 0
        assert again['tables']['model_version'].get('updated', 0) == 0
        # the API: LoRA reported as not serving when PyTorch is absent, npz stays the default, service healthy
        monkeypatch.setitem(sys.modules, 'torch', None)
        c, app = mk_client(mini, url)
        assert c.get('/healthz').json()['default_model_id'] == 'test-model-v1'
        assert 'PyTorch' in app.state.core.registry.errors['esm2-35m-lora-d-aa4fc2b7']
        r = c.post('/v1/predict', json={'sequence': SEQ, 'model_id': 'esm2-35m-lora-d-aa4fc2b7'})
        assert r.status_code == 404
        # DF_DEFAULT_MODEL_ID naming a model that is not serving keeps the registry default
        c2, app2 = mk_client(mini, url, default_model_id='esm2-35m-lora-d-aa4fc2b7')
        assert c2.get('/healthz').json()['default_model_id'] == 'test-model-v1'
        # a bundle file changed after export: the ETL refuses it
        (mini['lora_dir'] / 'esm2-35m-lora-d-v1' / 'base' / 'config.json').write_text('{"x": 1}')
        with pytest.raises(etl.HashMismatch):
            etl.run(url, mini['topic'], mini['sources'], mini['params'], 'none', mini['model_dir'])
        # --lora no skips it entirely
        etl.run(url, mini['topic'], mini['sources'], mini['params'], 'none', mini['model_dir'], lora='no')
        engine.dispose()
    finally:
        if BACKEND == 'postgresql':
            pg_drop(url)


# ----------------------------------------------------------------------------- default model and calibrator errors
class _OnlyPlatt:
    """Wraps the npz adapter but offers only 'platt', like LoRA-D."""

    def __init__(self, inner):
        self.inner = inner
        self.model_id = 'fake-lora'
        self.calibrators = ('platt',)
        self.default_calibrator = 'platt'
        self.training_sequences = frozenset({SEQ})

    def predict_tile(self, seq, calibrator=None):
        return self.inner.predict_tile(seq, 'platt')


def test_default_model_setting_and_unavailable_calibrator(mini, dbcopy):
    from api.service import LoadedModel
    c, app = mk_client(mini, dbcopy)
    reg = app.state.core.registry
    base = reg.models['test-model-v1']
    reg.models['fake-lora'] = LoadedModel(base.info.__class__(**{**base.info.__dict__, 'model_id': 'fake-lora',
                                                                  'kind': 'torch_lora'}),
                                          _OnlyPlatt(base.adapter), False)
    r = c.post('/v1/predict', json={'sequence': SEQ, 'model_id': 'fake-lora', 'calibrator': 'iso'})
    assert r.status_code == 422 and (r.json()['code'], r.json()['field']) == ('INVALID_REQUEST', 'calibrator')
    assert 'no calibrator "iso"' in r.json()['message']
    r = c.post('/v1/predict', json={'sequence': SEQ, 'model_id': 'fake-lora'})
    assert r.status_code == 200 and r.json()['provenance']['model_id'] == 'fake-lora'
    # TRAINING_PEPTIDE follows the chosen model's own training set (LoRA-D: W), typed input included
    assert 'TRAINING_PEPTIDE' in [w['code'] for w in r.json()['warnings']]
    assert 'TRAINING_PEPTIDE' not in [w['code'] for w in c.post('/v1/predict', json={'sequence': SEQ}).json()['warnings']]
    assert r.json()['provenance']['model_kind'] == 'torch_lora'
    # jobs pin the model and refuse the same calibrator at submission
    p = c.post('/v1/projects', json={'name': 'lora calibrator'}).json()
    body = {'mode': 'peptides', 'peptides': [{'input_id': 'a', 'sequence': SEQ}], 'model_id': 'fake-lora',
            'calibrator': 'iso'}
    r = c.post(f'/v1/projects/{p["project_id"]}/jobs', json=body)
    assert r.status_code == 422 and r.json()['field'] == 'calibrator'


def test_default_model_id_setting_picks_another_serving_model(mini, dbcopy):
    from api.service import load_registry
    engine = make_engine(dbcopy)
    with make_session_factory(engine)() as s, s.begin():
        row = s.get(ModelVersion, 'test-model-v1')
        clone = ModelVersion(**{k: getattr(row, k) for k in ModelVersion.__table__.columns.keys()})
        clone.model_id, clone.is_default = 'test-model-copy', False
        s.add(clone)
    factory = make_session_factory(engine)
    assert load_registry(factory, mini['model_dir']).default_id == 'test-model-v1'
    assert load_registry(factory, mini['model_dir'], 'test-model-copy').default_id == 'test-model-copy'
    reg = load_registry(factory, mini['model_dir'], 'no-such-model')
    assert reg.default_id == 'test-model-v1' and 'no-such-model' in reg.errors
    engine.dispose()
    # the API reports the effective default everywhere: health, model list, model card, predictions
    c, _ = mk_client(mini, dbcopy, default_model_id='test-model-copy')
    assert c.get('/healthz').json()['default_model_id'] == 'test-model-copy'
    assert c.get('/healthz').json()['default_model_source'] == 'setting'                  # plan-system 4.3
    flags = {m['model_id']: m['is_default'] for m in c.get('/v1/models').json()['items'] if m['role'] == 'effect'}
    assert flags == {'test-model-v1': False, 'test-model-copy': True}
    assert c.get('/v1/models/test-model-copy').json()['is_default'] is True
    assert c.post('/v1/predict', json={'sequence': SEQ}).json()['provenance']['model_id'] == 'test-model-copy'


def test_empty_default_model_setting_means_none():
    from api.config import Settings
    assert Settings(default_model_id='').default_model_id is None
    assert Settings(default_model_id=' ').default_model_id is None


def test_settings_ignore_the_compose_dotenv_in_the_working_directory(tmp_path, monkeypatch):
    """system/app/.env holds Docker Compose values (DF_TRUST_PROXY=true); a host process must not read it."""
    from api.config import Settings
    (tmp_path / '.env').write_text('DF_TRUST_PROXY=true\nDF_ALLOWED_ORIGINS=["http://localhost:8080"]\n')
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv('DF_TRUST_PROXY', raising=False)
    monkeypatch.delenv('DF_ALLOWED_ORIGINS', raising=False)
    st = Settings()
    assert st.trust_proxy is False and st.allowed_origins == ['http://localhost:5173']


# ----------------------------------------------------------------------------- parity with the research implementation
@pytest.mark.slow
@pytest.mark.realdata
@pytest.mark.skipif(not HAVE_TORCH, reason='PyTorch/Transformers not installed (backend/requirements-lora.txt)')
@pytest.mark.skipif(REAL_MANIFEST is None or not REAL_MANIFEST.is_file(), reason='LoRA-D bundle not exported')
def test_lora_parity_with_the_research_implementation():
    """NFR-04 / RG-01: the serving implementation reproduces the research implementation's per-seed raw scores,
    ensemble score and P(DeltaPSI >= 1) on two full tiles (fixture written by etl/export_lora.py)."""
    assert REAL_MANIFEST is not None
    model = LoraEnsembleModel.from_file('esm2-35m-lora-d-aa4fc2b7', REAL_MANIFEST, sha(REAL_MANIFEST))
    fx = np.load(model.bundle / 'parity-fixture.npz', allow_pickle=False)
    assert len(model.training_sequences) == 235
    assert str(fx['tile_w_sequence']) in model.training_sequences
    # both fixture tiles are W peptides (the e2e "typed" sequence is one too): parity concerns implementations only
    assert str(fx['tile_typed_sequence']) in model.training_sequences
    for key in ('tile_w', 'tile_typed'):
        seq = str(fx[f'{key}_sequence'])
        per_seed, cells = model.raw_scores(seq)
        assert cells == substitutions(seq) and per_seed.shape == (3, 532)
        np.testing.assert_allclose(per_seed, fx[f'{key}_per_seed'], atol=1e-5, rtol=0)
        pred = model.predict_tile(seq)
        np.testing.assert_allclose(pred.score, fx[f'{key}_score'], atol=1e-5, rtol=0)
        np.testing.assert_allclose(pred.prob, fx[f'{key}_prob'], atol=1e-5, rtol=0)
        assert pred.top10.sum() == 54 and sorted(pred.rank.tolist()) == list(range(1, 533))
        assert np.all((pred.prob > 0) & (pred.prob < 1))


def test_training_peptide_warned_for_typed_input_with_each_model(mini, dbcopy):
    """plan-system 1.5: a typed sequence that repeats a training tile is warned with the npz model (its 176 peptides,
    read from the reference DB) and with a model carrying its own set; a sequence outside both sets is not."""
    c, app = mk_client(mini, dbcopy)
    npz = app.state.core.registry.models['test-model-v1']
    assert npz.adapter.training_sequences                       # filled by the registry from in_training_set
    tiles = c.get('/v1/proteins/P12345/tiles').json()['tiles']
    train_seq = next(t['sequence'] for t in tiles if t['tile_index'] == 1)    # tile 1 is a training peptide (API-02)
    assert train_seq in npz.adapter.training_sequences and SEQ not in npz.adapter.training_sequences

    def codes(body):
        return [w['code'] for w in c.post('/v1/predict', json=body).json()['warnings']]

    assert 'TRAINING_PEPTIDE' in codes({'sequence': train_seq})
    assert 'TRAINING_PEPTIDE' not in codes({'sequence': SEQ})
    from api.service import LoadedModel
    reg = app.state.core.registry
    reg.models['fake-lora'] = LoadedModel(npz.info.__class__(**{**npz.info.__dict__, 'model_id': 'fake-lora',
                                                                 'kind': 'torch_lora'}), _OnlyPlatt(npz.adapter), False)
    # the other model answers from its own set only ({SEQ}), not from the npz model's
    assert 'TRAINING_PEPTIDE' in codes({'sequence': SEQ, 'model_id': 'fake-lora'})
    assert 'TRAINING_PEPTIDE' not in codes({'sequence': train_seq, 'model_id': 'fake-lora'})
    # stored tiles keep the previous behaviour with the npz model
    assert 'TRAINING_PEPTIDE' in codes({'uniprot_id': 'P12345', 'tile_index': 1})


def test_start_up_logs_the_default_model_source_and_hash(mini, dbcopy, caplog):
    """plan-system 4.3: one log line names the default model, where it came from and its weights hash."""
    import logging
    with caplog.at_level(logging.INFO, logger='api.service'):
        _, app = mk_client(mini, dbcopy)
    lines = [r.getMessage() for r in caplog.records if r.getMessage().startswith('default model:')]
    sha = app.state.core.registry.default.info.weights_sha256
    assert lines == [f'default model: test-model-v1 source=registry kind=ridge_platt weights_sha256={sha}']
    caplog.clear()
    with caplog.at_level(logging.INFO, logger='api.service'):
        mk_client(mini, dbcopy, default_model_id='no-such-model')
    assert any('source=registry' in r.getMessage() for r in caplog.records)
    assert any('DF_DEFAULT_MODEL_ID=no-such-model is not serving' in r.getMessage() for r in caplog.records)


@pytest.mark.slow
@pytest.mark.realdata
@pytest.mark.skipif(not HAVE_TORCH, reason='PyTorch/Transformers not installed (backend/requirements-lora.txt)')
@pytest.mark.skipif(REAL_MANIFEST is None or not REAL_MANIFEST.is_file(), reason='LoRA-D bundle not exported')
def test_merged_lora_stays_within_1e5_of_the_fixture(monkeypatch):
    """plan-system 1.4 b (PERF-02): merging W + alpha/r * B A at load changes float rounding only (<= 1e-5)."""
    assert REAL_MANIFEST is not None
    monkeypatch.setenv('DF_LORA_MERGE', '1')
    model = LoraEnsembleModel.from_file('esm2-35m-lora-d-aa4fc2b7', REAL_MANIFEST, sha(REAL_MANIFEST))
    assert model.merge
    fx = np.load(model.bundle / 'parity-fixture.npz', allow_pickle=False)
    per_seed, _ = model.raw_scores(str(fx['tile_w_sequence']))
    assert float(np.max(np.abs(per_seed - fx['tile_w_per_seed'].astype(np.float64)))) <= 1e-5
    _, nets = model._ensure()
    assert not any(hasattr(m, 'lora_A') for m in nets[0].backbone.modules())          # every LoRA layer merged
