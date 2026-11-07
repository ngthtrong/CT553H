"""UT and PB groups of test-plan.md §6.1-6.2 that need no database."""
from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from degron_footprint import export
from degron_footprint.constants import AAS, N_SUBSTITUTIONS, TOP_K
from degron_footprint.domain import status_from_measurement
from degron_footprint.errors import DomainError
from degron_footprint.features import feature_matrix, substitutions
from degron_footprint.model import RidgePlattModel, WeightsError, rank_scores
from degron_footprint.prediction import build_domain, build_result, warnings_for
from degron_footprint.provenance import ModelInfo
from degron_footprint.validation import (
    check_accession,
    check_tile_index,
    is_scorable,
    n_tiles,
    normalize_sequence,
    tile_bounds,
    tile_sequence,
)

from . import minidata

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'
tiles28 = st.text(alphabet=AAS, min_size=28, max_size=28)


@pytest.fixture(scope='module')
def model(tmp_path_factory):
    p = tmp_path_factory.mktemp('w') / 'm.npz'
    minidata.write_model(p)
    return RidgePlattModel.from_file('test', p, minidata.sha256(p))


def test_ut02_boundary_positions_and_context_blocks():
    X, cells = feature_matrix(SEQ)
    assert X.shape == (N_SUBSTITUTIONS, 180) and len(cells) == 532
    first = X[0]                                  # position 1: no left context, right context present
    assert first[60:60 + 3 * 20].sum() == 0       # offsets -3,-2,-1 are zero blocks
    assert first[60 + 3 * 20:].sum() == 3         # offsets +1,+2,+3 one-hot
    last = X[-1]                                  # position 28
    assert last[60 + 3 * 20:].sum() == 0 and last[60:60 + 60].sum() == 3
    assert np.allclose(X[:, 40:60].sum(axis=1), 1.0)         # composition is a distribution
    assert (X[:, :20].sum(axis=1) == 1).all() and (X[:, 20:40].sum(axis=1) == 1).all()


def test_substitutions_order_and_count():
    cells = substitutions(SEQ)
    assert len(cells) == 532
    assert cells[0] == (1, 'A') and cells[-1][0] == 28
    assert all(SEQ[p - 1] != a for p, a in cells)


def test_ut04_ranking_is_a_permutation_with_stable_ties():
    s = np.array([0.5, 0.5, 0.1, 0.9])
    assert list(rank_scores(s)) == [2, 3, 4, 1]                  # ties keep input order
    assert TOP_K == 54


def test_ut05_tile_generator():
    assert [n_tiles(x) for x in (0, 27, 28, 50, 51, 120)] == [0, 0, 1, 1, 2, 5]
    assert tile_bounds(1) == (1, 28) and tile_bounds(2) == (24, 51)
    prot = 'A' * 100
    assert tile_sequence(prot, 1) == 'A' * 28 and tile_sequence(prot, 4) == 'A' * 28
    assert tile_sequence(prot, 5) is None and tile_sequence(prot, 0) is None
    assert is_scorable('A' * 28) and not is_scorable('A' * 27 + 'X') and not is_scorable('A' * 27)


@pytest.mark.parametrize('psi,reads,expected', [
    (4.0, 10, 'measured_in_domain'), (4.0 + 1e-9, 10, 'measured_out_of_domain'),
    (2.0, 9.999, 'measured_unreliable'), (2.0, 10.0, 'measured_in_domain'), (None, 100, 'measured_unreliable'),
    (float('nan'), 100, 'measured_unreliable'), (2.0, None, 'measured_unreliable')])
def test_ut06_domain_status_boundaries(psi, reads, expected):
    assert status_from_measurement(psi, reads) == expected


def test_ut07_normalisation():
    assert normalize_sequence('  ' + SEQ.lower() + '\n') == SEQ
    with pytest.raises(DomainError) as e:
        normalize_sequence(SEQ[:14] + ' ' + SEQ[15:])             # internal blank: 28 long but not a residue
    assert e.value.code == 'INVALID_CHARACTER' and 'Position 15' in e.value.message


@pytest.mark.parametrize('raw,code', [
    (SEQ[:-1], 'INVALID_LENGTH'), (SEQ + 'A', 'INVALID_LENGTH'), ('', 'INVALID_LENGTH'),
    ('B' + SEQ[1:], 'INVALID_CHARACTER'), (SEQ[:-1] + '1', 'INVALID_CHARACTER'), (SEQ[:-1] + '*', 'INVALID_CHARACTER'),
    (SEQ[:-1] + '\x00', 'INVALID_CHARACTER'), (SEQ[:-1] + 'é', 'INVALID_CHARACTER'), (12, 'INVALID_REQUEST')])
def test_codes_of_bad_sequences(raw, code):
    with pytest.raises(DomainError) as e:
        normalize_sequence(raw)
    assert e.value.code == code and e.value.status == 422 and e.value.field == 'sequence'


def test_error_message_echoes_one_character_at_most():
    with pytest.raises(DomainError) as e:
        normalize_sequence('Z' * 5 + 'SECRETSECRETSECRETSECR' + 'A')       # length 28, bad first char
    assert 'SECRET' not in e.value.message and "'Z'" in e.value.message


def test_accession_and_tile_index():
    assert check_accession('P60484') == 'P60484' and check_accession('A0A024R161')
    for bad in ('p60484', 'P6048', 'P60484X', '', 7, None):
        with pytest.raises(DomainError):
            check_accession(bad)
    assert check_tile_index(3, 5) == 3
    for bad, n in ((0, 5), (6, 5), (-1, 5), (1, 0)):
        with pytest.raises(DomainError) as e:
            check_tile_index(bad, n)
        assert e.value.code == 'TILE_OUT_OF_RANGE'
    for bad in (True, 1.5, '1'):
        with pytest.raises(DomainError) as e:
            check_tile_index(bad, 5)
        assert e.value.code == 'INVALID_REQUEST'


def test_ut03_calibrators_match_closed_form(model):
    s = np.linspace(-1.5, 2.0, 50)
    assert np.allclose(model.calibrate(s, 'platt'), 1 / (1 + np.exp(-(3.7 * s - 3.4))), atol=1e-12)
    assert np.allclose(model.calibrate(s, 'iso'), np.interp(s, model.iso_x, model.iso_y), atol=1e-12)
    with pytest.raises(ValueError):
        model.calibrate(s, 'nope')


def test_ut09_weights_hash_checked(tmp_path):
    p = tmp_path / 'w.npz'
    minidata.write_model(p)
    good = minidata.sha256(p)
    RidgePlattModel.from_file('m', p, good)
    with pytest.raises(WeightsError, match='hash'):
        RidgePlattModel.from_file('m', p, '0' * 64)
    with pytest.raises(WeightsError, match='missing'):
        RidgePlattModel.from_file('m', tmp_path / 'absent.npz', good)
    bad = tmp_path / 'bad.npz'
    bad.write_bytes(b'not an npz')
    with pytest.raises(WeightsError):
        RidgePlattModel.from_file('m', bad, None)


@settings(max_examples=40, deadline=None)
@given(tiles28)
def test_pb01_any_valid_tile_gives_532_finite_cells(model, seq):
    pred = model.predict_tile(seq)
    assert len(pred.score) == 532 and np.isfinite(pred.score).all()
    assert ((pred.prob >= 0) & (pred.prob <= 1)).all()
    assert sorted(pred.rank) == list(range(1, 533))               # PB-04: a permutation
    assert pred.rank[np.argmax(pred.score)] == 1
    assert pred.top10.sum() == TOP_K


@settings(max_examples=40, deadline=None)
@given(tiles28)
def test_pb03_determinism_and_pb05_monotone_calibration(model, seq):
    a, b = model.predict_tile(seq), model.predict_tile(seq)
    assert a.score.tobytes() == b.score.tobytes() and a.prob.tobytes() == b.prob.tobytes()
    order = np.argsort(a.score)
    assert (np.diff(a.prob[order]) >= -1e-12).all()               # Platt is non-decreasing in the score


@settings(max_examples=60, deadline=None)
@given(st.text(max_size=60))
def test_pb02_bad_strings_give_coded_errors(raw):
    if len(raw.strip()) == 28 and all(c in AAS for c in raw.strip().upper()):
        return
    with pytest.raises(DomainError) as e:
        normalize_sequence(raw)
    assert e.value.code in ('INVALID_LENGTH', 'INVALID_CHARACTER')


def _result(model, seq=SEQ):
    pred = model.predict_tile(seq)
    info = ModelInfo('test', 'ridge_platt', 'a' * 64, 'spec', 'P(DeltaPSI >= 1.0)', 'development OOF benchmark',
                     'domain', ({'source_id': 'z', 'name': 'Zhang', 'version': '1', 'license_name': 'CC BY 4.0',
                                 'attribution_text': 'Zhang 2023'},))
    tile = {'uniprot_id': 'P12345', 'tile_index': 2, 'start_pos': 24, 'end_pos': 51, 'sequence': seq}
    return build_result(info, pred, tile, build_domain('unknown', None, None), warnings_for('unknown', False, False))


def test_ut08_csv_writer(model):
    r = _result(model)
    out = export.to_csv(r)
    lines = out.split('\n')
    comments = [x for x in lines if x.startswith('#')]
    assert comments[0].startswith('# model_id=test') and any(x.startswith('# disclaimer=') for x in comments)
    body = [x for x in lines if x and not x.startswith('#')]
    assert body[0] == ','.join(export.COLUMNS) and len(body) == 533
    assert body[1].startswith('P12345_2,2,1,') and '\r' not in out
    first = body[1].split(',')
    assert first[5] == f"{r['cells'][0]['score_dpsi_raw']:.10g}"


def test_csv_comment_values_cannot_forge_rows(model):
    r = _result(model)
    r['provenance']['domain_description'] = 'line one\nP12345_2,2,1,A,A,9,9,1,1'
    out = export.to_csv(r)
    assert sum(1 for x in out.split('\n') if x.startswith('P12345_2')) == 532


def test_filename_never_holds_the_sequence(model):
    r = _result(model)
    assert SEQ not in export.filename(r, 'csv')
    r['tile']['uniprot_id'] = None
    assert 'user-seq' in export.filename(r, 'json')
