"""Prediction cache (plan-system 1.2): CACHE-01…04."""
from __future__ import annotations

import logging

import numpy as np
import pytest

from degron_footprint.cache import PredictionCache, cache_key
from tests.conftest import mk_client

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'
OTHER = 'MKTAYIAKQRQISFVKSHFSRQLEERLG'


class CountingAdapter:
    """Wraps a real adapter and counts real computations."""

    def __init__(self, inner):
        self.inner = inner
        self.calls = 0
        self.calibrators = inner.calibrators
        self.default_calibrator = inner.default_calibrator
        self.training_sequences = getattr(inner, 'training_sequences', None)

    def predict_tile(self, seq, calibrator=None):
        self.calls += 1
        return self.inner.predict_tile(seq, calibrator)


def _counting(app):
    lm = app.state.core.registry.models['test-model-v1']
    lm.adapter = CountingAdapter(lm.adapter)
    return lm.adapter


def test_cache01_hit_is_bit_identical_to_a_fresh_computation(mini, dbcopy):
    """NFR-05: the cached answer equals, bit for bit, the answer computed without any cache."""
    c_off, _ = mk_client(mini, dbcopy, prediction_cache='off')
    c, app = mk_client(mini, dbcopy)
    counter = _counting(app)
    fresh = c_off.post('/v1/predict', json={'sequence': SEQ}).json()
    first = c.post('/v1/predict', json={'sequence': SEQ}).json()
    second = c.post('/v1/predict', json={'sequence': SEQ}).json()
    assert counter.calls == 1                                   # second answer from the cache
    for r in (first, second):
        assert r['cells'] == fresh['cells']                     # float equality of every cell = identical bits in JSON
        assert r['warnings'] == fresh['warnings'] and r['domain'] == fresh['domain']
    # export of the same tile: also served from the cache, same numbers
    exp = c.post('/v1/export', json={'sequence': SEQ, 'format': 'json'}).json()
    assert counter.calls == 1 and exp['cells'] == fresh['cells']
    # stored tiles: domain and warnings are recomputed from the database on a hit, never cached
    a = c.post('/v1/predict', json={'uniprot_id': 'P12345', 'tile_index': 1}).json()
    b = c.post('/v1/predict', json={'uniprot_id': 'P12345', 'tile_index': 1}).json()
    assert counter.calls == 2 and a['cells'] == b['cells'] and b['warnings'] == a['warnings'] != []
    st = app.state.core.predictor.cache.stats()
    assert (st.mode, st.hits, st.misses, st.entries) == ('memory', 3, 2, 2)


def test_cache02_other_model_hash_calibrator_or_code_version_miss():
    k = cache_key(SEQ, 'm', 'a' * 64, 'platt')
    assert k != cache_key(OTHER, 'm', 'a' * 64, 'platt')
    assert k != cache_key(SEQ, 'm2', 'a' * 64, 'platt')
    assert k != cache_key(SEQ, 'm', 'b' * 64, 'platt')
    assert k != cache_key(SEQ, 'm', 'a' * 64, 'iso')
    assert k != cache_key(SEQ, 'm', 'a' * 64, 'platt', code_version='9.9.9')
    assert k == cache_key(SEQ, 'm', 'a' * 64, 'platt') and len(k) == 64


def test_cache02_calibrator_and_weights_change_through_the_api(mini, dbcopy):
    c, app = mk_client(mini, dbcopy)
    counter = _counting(app)
    platt = c.post('/v1/predict', json={'sequence': SEQ, 'calibrator': 'platt'}).json()
    iso = c.post('/v1/predict', json={'sequence': SEQ, 'calibrator': 'iso'}).json()
    assert counter.calls == 2                                   # another calibrator is another entry
    assert [x['p_dpsi_ge_1_calibrated'] for x in platt['cells']] != [x['p_dpsi_ge_1_calibrated'] for x in iso['cells']]
    # an omitted calibrator is the model default: same entry as asking for it explicitly
    default = app.state.core.registry.models['test-model-v1'].adapter.default_calibrator
    c.post('/v1/predict', json={'sequence': SEQ})
    assert counter.calls == 2 and default in ('platt', 'iso')
    # new weights under the same id (registry reload with another hash): the old entry is not used
    lm = app.state.core.registry.models['test-model-v1']
    lm.info = lm.info.__class__(**{**lm.info.__dict__, 'weights_sha256': 'f' * 64})
    c.post('/v1/predict', json={'sequence': SEQ})
    assert counter.calls == 3


def test_cache03_no_sequence_in_logs(mini, dbcopy, caplog):
    c, app = mk_client(mini, dbcopy)
    with caplog.at_level(logging.DEBUG):
        c.post('/v1/predict', json={'sequence': SEQ})
        c.post('/v1/predict', json={'sequence': SEQ})
        app.state.core.predictor.cache.log_stats_if_changed()
    text = '\n'.join(r.getMessage() for r in caplog.records)
    assert 'prediction cache mode=memory entries=1 hits=1 misses=1' in text
    assert SEQ not in text
    key = cache_key(SEQ, 'test-model-v1', app.state.core.registry.models['test-model-v1'].info.weights_sha256, 'platt')
    assert key not in text


def test_cache04_default_is_memory_and_writes_nothing_to_disk(mini, dbcopy, tmp_path):
    from api.config import Settings
    assert Settings().prediction_cache == 'memory'
    ws = tmp_path / 'ws'
    c, app = mk_client(mini, dbcopy, workspace_dir=ws)
    c.post('/v1/predict', json={'sequence': SEQ})
    assert app.state.core.predictor.cache.directory is None
    assert not (tmp_path / 'prediction-cache').exists()
    assert not any(p.suffix == '.npz' for p in tmp_path.rglob('*'))


def test_cache_disk_mode_is_opt_in_and_survives_a_restart(mini, dbcopy, tmp_path):
    d = tmp_path / 'pc'
    c, app = mk_client(mini, dbcopy, prediction_cache='disk', prediction_cache_dir=d)
    first = c.post('/v1/predict', json={'sequence': SEQ}).json()
    files = list(d.glob('*.npz'))
    assert len(files) == 1 and SEQ not in files[0].name and (d.stat().st_mode & 0o777) == 0o700
    c2, app2 = mk_client(mini, dbcopy, prediction_cache='disk', prediction_cache_dir=d)      # new process
    counter = _counting(app2)
    again = c2.post('/v1/predict', json={'sequence': SEQ}).json()
    assert counter.calls == 0 and again['cells'] == first['cells']
    assert app2.state.core.predictor.cache.stats().disk_hits == 1
    # a damaged entry is ignored and recomputed, not served
    files[0].write_bytes(b'not an npz')
    c3, app3 = mk_client(mini, dbcopy, prediction_cache='disk', prediction_cache_dir=d)
    counter3 = _counting(app3)
    assert c3.post('/v1/predict', json={'sequence': SEQ}).json()['cells'] == first['cells']
    assert counter3.calls == 1 and app3.state.core.predictor.cache.stats().errors == 1


def test_cache_lru_bound_and_frozen_arrays(mini, dbcopy):
    c, app = mk_client(mini, dbcopy, prediction_cache_max_entries=1)
    counter = _counting(app)
    c.post('/v1/predict', json={'sequence': SEQ})
    c.post('/v1/predict', json={'sequence': OTHER})
    c.post('/v1/predict', json={'sequence': SEQ})                 # evicted by OTHER: computed again
    assert counter.calls == 3 and app.state.core.predictor.cache.stats().entries == 1
    pc = PredictionCache('memory', 4)
    lm = app.state.core.registry.models['test-model-v1']
    stored = pc.put('k', lm.adapter.predict_tile(SEQ))
    with pytest.raises(ValueError):
        stored.score[0] = np.inf                                  # a caller cannot corrupt the shared entry
    with pytest.raises(ValueError):
        PredictionCache('disk', 4, None)
