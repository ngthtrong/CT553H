"""API group of test-plan.md §6.4 plus the security and privacy checks of §6.8, on the miniature database."""
from __future__ import annotations

import gzip
import hashlib
import json
import logging
import re
from datetime import UTC, datetime, timedelta
from urllib.parse import quote

import pytest
from sqlalchemy import select, text

from db.models import ModelVersion, PredictionCell, PredictionRun
from db.session import make_engine

from .conftest import mk_client
from .contract import check

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'


def predict(c, **body):
    return c.post('/v1/predict', json=body)


def codes(r):
    j = r.json()
    return j['code'], j.get('field')


# ----------------------------------------------------------------------------- predict
def test_api01_sequence(client):
    r = predict(client, sequence=SEQ)
    assert r.status_code == 200
    j = r.json()
    check('PredictionResult', j)
    assert len(j['cells']) == 532 and j['domain']['status'] == 'unknown'
    assert [w['code'] for w in j['warnings']] == ['DOMAIN_UNKNOWN']
    assert r.headers['cache-control'] == 'no-store' and r.headers['x-request-id']
    p = j['provenance']
    assert p['model_id'] == 'test-model-v1' and len(p['weights_sha256']) == 64
    assert p['event_definition'] == 'P(DeltaPSI >= 1.0)' and 'not external validation' in p['evidence_label']
    assert any('not probabilities of disease' in d for d in p['disclaimers'])
    assert j['tile'] == {'uniprot_id': None, 'tile_index': None, 'start_pos': None, 'end_pos': None, 'sequence': SEQ}
    assert 'set-cookie' not in r.headers


def test_cells_order_and_content(client):
    cells = predict(client, sequence=SEQ).json()['cells']
    assert [c['position'] for c in cells[:19]] == [1] * 19 and cells[19]['position'] == 2
    assert cells[0]['wt_aa'] == 'D' and cells[0]['mut_aa'] == 'A'
    assert all(c['wt_aa'] != c['mut_aa'] for c in cells)
    assert sorted(c['rank_in_tile'] for c in cells) == list(range(1, 533))
    assert sum(c['top10pct_in_tile'] for c in cells) == 54


def test_api02_uniprot_tile(client):
    r = predict(client, uniprot_id='P12345', tile_index=1)
    j = r.json()
    assert r.status_code == 200
    check('PredictionResult', j)
    assert j['tile']['start_pos'] == 1 and j['tile']['end_pos'] == 28 and j['tile']['uniprot_id'] == 'P12345'
    assert j['domain']['status'] == 'measured_in_domain' and j['domain']['psi_wt_measured'] == 2.0
    assert [w['code'] for w in j['warnings']] == ['TRAINING_PEPTIDE']
    ids = {s['source_id'] for s in j['provenance']['data_sources']}
    assert ids == {'zhang2023-mendeley-v2', 'uniprot-2026_03', 'zhang2023-geo-gse240610'}
    j2 = predict(client, uniprot_id='P12345', tile_index=3).json()
    assert j2['tile']['start_pos'] == 47 and j2['tile']['end_pos'] == 74


def test_api10_request_shape_errors(client):
    r = client.post('/v1/predict', content=b'{not json', headers={'content-type': 'application/json'})
    assert r.status_code == 400 and codes(r) == ('INVALID_REQUEST', None)
    assert client.post('/v1/predict', json=[1, 2]).status_code == 400
    r = predict(client, sequence=SEQ, color='red')
    assert r.status_code == 422 and codes(r) == ('INVALID_REQUEST', None) and 'color' not in r.text
    assert predict(client, sequence=SEQ, uniprot_id='P12345', tile_index=1).status_code == 422
    assert predict(client, uniprot_id='P12345').status_code == 422           # accession without tile
    assert predict(client).status_code == 422
    assert predict(client, sequence=SEQ, calibrator='magic').status_code == 422
    assert predict(client, sequence=SEQ, override_domain='yes').status_code == 422
    assert predict(client, sequence=SEQ, model_id=5).status_code == 422
    assert codes(predict(client, sequence=12345)) == ('INVALID_REQUEST', 'sequence')


@pytest.mark.parametrize('seq,n', [(SEQ[:-1], 27), (SEQ + 'A', 29), ('', 0)])
def test_api11_length(client, seq, n):
    r = predict(client, sequence=seq)
    assert r.status_code == 422 and codes(r) == ('INVALID_LENGTH', 'sequence') and f'it has {n}' in r.json()['message']


@pytest.mark.parametrize('bad,pos', [('B', 1), ('X', 28), ('1', 14), ('*', 3), (' ', 9), ('\t', 9)])
def test_api12_characters(client, bad, pos):
    s = list(SEQ)
    s[pos - 1] = bad
    r = predict(client, sequence=''.join(s))
    assert r.status_code == 422 and codes(r) == ('INVALID_CHARACTER', 'sequence')
    assert f'Position {pos}' in r.json()['message']


def test_api13_accession(client):
    r = predict(client, uniprot_id='P99999', tile_index=1)
    assert r.status_code == 404 and codes(r) == ('UNKNOWN_ACCESSION', 'uniprot_id')
    r = predict(client, uniprot_id='not-an-id', tile_index=1)
    assert r.status_code == 422 and codes(r) == ('INVALID_REQUEST', 'uniprot_id')


@pytest.mark.parametrize('idx', [0, 6, -3])
def test_api14_tile_range(client, idx):
    r = predict(client, uniprot_id='P12345', tile_index=idx)
    assert r.status_code == 422 and codes(r) == ('TILE_OUT_OF_RANGE', 'tile_index') and 'between 1 and 5' in r.json()['message']


def test_short_protein_has_no_tile(client):
    r = predict(client, uniprot_id='O00001', tile_index=1)
    assert codes(r)[0] == 'TILE_OUT_OF_RANGE' and 'no tile' in r.json()['message']


def test_api15_not_scorable(client):
    r = predict(client, uniprot_id='P22222', tile_index=4)
    assert r.status_code == 422 and codes(r)[0] == 'TILE_NOT_SCORABLE'


def test_api16_models(client, dbcopy, mini):
    r = predict(client, sequence=SEQ, model_id='nope-v9')
    assert r.status_code == 404 and codes(r) == ('MODEL_NOT_FOUND', 'model_id')
    assert predict(client, sequence=SEQ, model_id='BAD ID!!').status_code == 404
    assert predict(client, sequence=SEQ, model_id='test-model-v1').status_code == 200
    eng = make_engine(dbcopy)
    with eng.begin() as c:
        row = dict(c.execute(select(ModelVersion)).mappings().one())
        row.update(model_id='cand-v1', is_default=False, status='candidate', frozen_at=None)
        c.execute(ModelVersion.__table__.insert().values(**row))
    c2, _ = mk_client(mini, dbcopy)
    assert predict(c2, sequence=SEQ, model_id='cand-v1').status_code == 404       # candidate models never serve
    ids = [m['model_id'] for m in c2.get('/v1/models').json()['items']]
    assert ids[0] == 'test-model-v1' and 'cand-v1' in ids


def test_api17_body_limit(client):
    big = {'sequence': SEQ, 'model_id': 'x' * 5000}
    r = client.post('/v1/predict', json=big)
    assert r.status_code == 413 and codes(r)[0] == 'PAYLOAD_TOO_LARGE'

    def chunks():                                             # chunked upload without Content-Length
        yield b'{"sequence": "' + b'A' * 3000
        yield b'A' * 3000 + b'"}'
    r = client.post('/v1/predict', content=chunks(), headers={'content-type': 'application/json'})
    assert r.status_code == 413


def test_api18_domain_statuses(client):
    expect = {('P12345', 1): 'measured_in_domain', ('P12345', 3): 'measured_unreliable',
              ('P12345', 4): 'measured_unreliable', ('P12345', 5): 'unknown', ('P22222', 1): 'measured_in_domain',
              ('P22222', 3): 'measured_unreliable'}
    for (acc, n), st in expect.items():
        j = predict(client, uniprot_id=acc, tile_index=n).json()
        assert j['domain']['status'] == st, (acc, n)
        want = {'measured_unreliable': 'DOMAIN_UNRELIABLE', 'unknown': 'DOMAIN_UNKNOWN'}.get(st)
        assert (want in [w['code'] for w in j['warnings']]) == bool(want)
    tile1 = client.get('/v1/proteins/P12345/tiles').json()['tiles'][0]['sequence']
    j = predict(client, sequence=tile1).json()                # typed sequence equal to a stored tile is not looked up
    assert j['domain']['status'] == 'unknown' and j['tile']['uniprot_id'] is None


def test_api19_out_of_domain_refused_then_overridden(client):
    r = predict(client, uniprot_id='P12345', tile_index=2)
    assert r.status_code == 422 and codes(r)[0] == 'OUT_OF_DOMAIN' and '(4.8)' in r.json()['message']
    assert 'cells' not in r.json()
    r = predict(client, uniprot_id='P12345', tile_index=2, override_domain=True)
    j = r.json()
    assert r.status_code == 200 and j['domain']['status'] == 'measured_out_of_domain'
    assert 'OUT_OF_DOMAIN_OVERRIDDEN' in [w['code'] for w in j['warnings']]
    assert predict(client, uniprot_id='P22222', tile_index=2).status_code == 422          # PSI just above 4.0


def test_calibrator_choice(client):
    a = predict(client, sequence=SEQ, calibrator='platt').json()['cells']
    b = predict(client, sequence=SEQ, calibrator='iso').json()['cells']
    assert a[0]['score_dpsi_raw'] == b[0]['score_dpsi_raw'] and a[:50] != b[:50]


def test_nfr05_deterministic(client):
    a = predict(client, uniprot_id='P12345', tile_index=1).json()
    b = predict(client, uniprot_id='P12345', tile_index=1).json()
    assert a['cells'] == b['cells'] and a['domain'] == b['domain']


# ----------------------------------------------------------------------------- reference
def test_api20_protein_search(client):
    r = client.get('/v1/proteins', params={'query': 'gene1'})
    assert r.status_code == 200 and [x['gene_symbol'] for x in r.json()['items']] == ['GENE1']
    assert r.json()['items'][0]['n_tiles'] == 5 and r.json()['items'][0]['length'] == 120
    assert [x['uniprot_id'] for x in client.get('/v1/proteins', params={'query': 'P12'}).json()['items']] == ['P12345']
    items = client.get('/v1/proteins', params={'query': 'GENE'}).json()['items']
    assert [x['gene_symbol'] for x in items] == ['GENE1', 'GENE2', 'GENE3']
    assert len(client.get('/v1/proteins', params={'query': 'GENE', 'limit': 2}).json()['items']) == 2
    check('ProteinSummary', items[0])
    assert client.get('/v1/proteins', params={'query': 'G'}).status_code == 422
    assert client.get('/v1/proteins').status_code == 400
    assert client.get('/v1/proteins', params={'query': 'GENE', 'limit': 51}).status_code == 422
    assert client.get('/v1/proteins', params={'query': '%%'}).status_code == 422
    assert client.get('/v1/proteins', params={'query': "x'; DROP TABLE tile;--"}).status_code == 422
    assert client.get('/v1/proteins', params={'query': 'ZZZZZ'}).json() == {'items': []}


def test_api21_tiles(client):
    r = client.get('/v1/proteins/P12345/tiles')
    j = r.json()
    assert r.status_code == 200
    check('TileList', j)
    assert [t['tile_index'] for t in j['tiles']] == [1, 2, 3, 4, 5] and j['protein']['n_tiles'] == 5
    assert [t['domain_status'] for t in j['tiles']] == [
        'measured_in_domain', 'measured_out_of_domain', 'measured_unreliable', 'measured_unreliable', 'unknown']
    assert client.get('/v1/proteins/O00001/tiles').json()['tiles'] == []
    assert client.get('/v1/proteins/P99999/tiles').status_code == 404
    assert client.get('/v1/proteins/xyz/tiles').status_code == 422
    t4 = client.get('/v1/proteins/P22222/tiles').json()['tiles'][3]
    assert t4['scorable'] is False


def test_api22_measured_overlay(client):
    j = client.get('/v1/proteins/P12345/tiles/1/measured').json()
    check('MeasuredOverlay', j)
    assert len(j['cells']) > 400 and all(c['in_training_set'] for c in j['cells'])
    assert any('Zhang' in s['name'] or s['source_id'] == 'zhang2023-mendeley-v2' for s in j['provenance']['data_sources'])
    assert client.get('/v1/proteins/P12345/tiles/2/measured').json()['cells'] == []
    r = client.get('/v1/proteins/P12345/tiles/9/measured')
    assert r.status_code == 404 and codes(r)[0] == 'TILE_OUT_OF_RANGE'
    assert client.get('/v1/proteins/P12345/tiles/abc/measured').status_code == 422
    assert client.get('/v1/proteins/P99999/tiles/1/measured').status_code == 404


def test_api23_clinvar_overlay(client):
    r = client.get('/v1/proteins/P12345/tiles/1/clinvar')
    j = r.json()
    assert r.status_code == 200
    check('ClinvarOverlay', j)
    assert {v['variation_id'] for v in j['variants']} == {101, 106, 107, 108, 109}
    assert all(1 <= v['position'] <= 28 and v['position'] == v['protein_pos'] for v in j['variants'])
    assert j['clinvar_file_date'] == '2026-10-12'
    assert any('not for diagnostic use' in d for d in j['provenance']['disclaimers'])
    assert any(s['source_id'].startswith('clinvar-') for s in j['provenance']['data_sources'])
    t2 = client.get('/v1/proteins/P12345/tiles/2/clinvar').json()['variants']
    assert {v['variation_id'] for v in t2} == {102, 103} and {v['position'] for v in t2} == {7, 8}


def test_clinvar_overlay_unavailable_when_not_loaded(mini, mini_db, dbcopy):
    eng = make_engine(dbcopy)
    with eng.begin() as c:
        c.execute(text('DELETE FROM clinvar_variant'))
    c2, _ = mk_client(mini, dbcopy)
    r = c2.get('/v1/proteins/P12345/tiles/1/clinvar')
    assert r.status_code == 503 and codes(r)[0] == 'SERVICE_UNAVAILABLE'


def test_api24_models(client):
    j = client.get('/v1/models').json()
    check('ModelSummary', j['items'][0])
    assert j['items'][0]['is_default'] is True
    card = client.get('/v1/models/test-model-v1').json()
    check('ModelCard', card)
    assert card['metrics_source_file'].endswith('results.json') and card['frozen_at'] == '2026-10-22T00:00:00Z'
    assert card['trained_on_sources'][0]['source_id'] == 'zhang2023-mendeley-v2'
    # E2E-07: the card lists the sources that are deliberately not used, and they are exactly the ones the ETL blocks
    from degron_footprint.sources import BLOCKED_SOURCE_IDS
    assert {x['source_id'] for x in card['not_used_sources']} == set(BLOCKED_SOURCE_IDS)
    for x in card['not_used_sources']:
        check('NotUsedSource', x)
        assert x['reason'].strip()
    assert any('Koren' in x['name'] for x in card['not_used_sources'])
    assert client.get('/v1/models/unknown-1').status_code == 404
    assert client.get('/v1/models/Bad Id').status_code == 404


def test_api25_sources_hide_blocked(client):
    j = client.get('/v1/sources').json()
    ids = {s['source_id'] for s in j['items']}
    assert 'koren2018-nihms967427' not in ids and 'zhang2023-mendeley-v2' in ids
    for s in j['items']:
        check('DataSource', s)
    cv = next(s for s in j['items'] if s['source_id'].startswith('clinvar-'))
    assert cv['disclaimer_text']


# ----------------------------------------------------------------------------- health, cors, limits
def test_api26_health_variants(mini, mini_db, dbcopy, tmp_path):
    c, _ = mk_client(mini, mini_db['url'])
    j = c.get('/healthz').json()
    assert c.get('/healthz').status_code == 200
    check('Health', j)
    assert j == {'status': 'ok', 'version': j['version'], 'model_loaded': True,
                 'default_model_id': 'test-model-v1', 'database': 'ok'}
    # weights missing
    c2, _ = mk_client(mini, mini_db['url'], model_dir=tmp_path / 'empty')
    r = c2.get('/healthz')
    assert r.status_code == 503 and r.json()['model_loaded'] is False and r.json()['status'] == 'degraded'
    assert predict(c2, sequence=SEQ).status_code == 503 and codes(predict(c2, sequence=SEQ))[0] == 'SERVICE_UNAVAILABLE'
    # hash mismatch: a different weights file under the registered name
    bad = tmp_path / 'tampered'
    bad.mkdir()
    (bad / 'test-model-v1.npz').write_bytes((mini['model_dir'] / 'test-model-v1.npz').read_bytes() + b'\0')
    c3, _ = mk_client(mini, mini_db['url'], model_dir=bad)
    assert c3.get('/healthz').status_code == 503
    # database down at start
    c4, _ = mk_client(mini, f'sqlite:///{tmp_path}/no/such/dir/x.db')
    r = c4.get('/healthz')
    assert r.status_code == 503 and r.json()['database'] == 'unavailable'
    # database goes away after start: reference endpoints answer 503, a typed sequence still scores
    c5, app5 = mk_client(mini, dbcopy)
    app5.state.core.engine.dispose()
    (tmp_path / 'copy.db').unlink()
    # sqlite keeps working on an unlinked file for open handles; force failure on the next connect instead
    app5.state.core.factory.kw['bind'] = make_engine(f'sqlite:///{tmp_path}/no/such/dir/y.db')
    assert c5.get('/v1/proteins/P12345/tiles').status_code == 503
    assert codes(c5.get('/v1/proteins/P12345/tiles'))[0] == 'SERVICE_UNAVAILABLE'
    assert predict(c5, sequence=SEQ).status_code == 200


def test_api27_rate_limit(mini, mini_db):
    c, _ = mk_client(mini, mini_db['url'], rate_limit_predict=60, rate_limit_reference=5)
    statuses = [predict(c, sequence='short').status_code for _ in range(61)]
    assert statuses[:60] == [422] * 60 and statuses[60] == 429
    r = predict(c, sequence='short')
    assert codes(r)[0] == 'RATE_LIMITED' and int(r.headers['retry-after']) >= 1
    assert c.get('/healthz').status_code == 200                       # health is exempt
    assert [c.get('/v1/models').status_code for _ in range(6)] == [200] * 5 + [429]


def test_rate_limiter_window_slides():
    from api.ratelimit import RateLimiter
    t = [0.0]
    rl = RateLimiter(60, clock=lambda: t[0])
    assert all(rl.check('a', 'p', 3)[0] for _ in range(3))
    ok, retry = rl.check('a', 'p', 3)
    assert not ok and 1 <= retry <= 61
    assert rl.check('b', 'p', 3)[0]                                  # another client is unaffected
    t[0] = 61.0
    assert rl.check('a', 'p', 3)[0]


def test_api28_cors(mini, mini_db):
    c, _ = mk_client(mini, mini_db['url'], allowed_origins=['http://localhost:5173'])
    ok = c.options('/v1/predict', headers={'Origin': 'http://localhost:5173', 'Access-Control-Request-Method': 'POST',
                                           'Access-Control-Request-Headers': 'content-type'})
    assert ok.status_code == 200 and ok.headers['access-control-allow-origin'] == 'http://localhost:5173'
    no = c.options('/v1/predict', headers={'Origin': 'http://evil.example', 'Access-Control-Request-Method': 'POST'})
    assert no.status_code == 400 and 'access-control-allow-origin' not in no.headers
    r = c.get('/v1/models', headers={'Origin': 'http://evil.example'})
    assert 'access-control-allow-origin' not in r.headers
    r = c.get('/v1/models', headers={'Origin': 'http://localhost:5173'})
    assert 'x-request-id' in r.headers['access-control-expose-headers'].lower()


def test_sec03_headers_and_error_shapes(client):
    r = client.get('/v1/models')
    assert r.headers['x-content-type-options'] == 'nosniff' and r.headers['referrer-policy'] == 'no-referrer'
    assert "default-src 'none'" in r.headers['content-security-policy']
    r = client.get('/nonexistent')
    assert r.status_code == 404 and set(r.json()) == {'code', 'message', 'field'}
    r = client.get('/v1/predict')
    assert r.status_code == 405 and set(r.json()) == {'code', 'message', 'field'}
    assert len({client.get('/healthz').headers['x-request-id'] for _ in range(5)}) == 5
    assert client.get('/docs').status_code == 404                     # documentation is off unless enabled


def test_gzip_when_asked(client):
    r = client.post('/v1/predict', json={'sequence': SEQ}, headers={'accept-encoding': 'gzip'})
    assert r.headers.get('content-encoding') == 'gzip' and r.json()['cells']


def test_openapi_served_is_the_contract(mini, mini_db):
    c, _ = mk_client(mini, mini_db['url'], enable_docs=True)
    j = c.get('/openapi.json').json()
    assert j['info']['title'] == 'Degron Footprint API' and '/v1/predict' in j['paths']
    assert j['openapi'].startswith('3.1')


# ----------------------------------------------------------------------------- export
def test_api30_csv_export(client):
    r = client.post('/v1/export', json={'sequence': SEQ, 'format': 'csv'})
    assert r.status_code == 200 and r.headers['content-type'].startswith('text/csv')
    assert re.fullmatch(r'attachment; filename="degron-footprint_test-model-v1_user-seq_\d{4}-\d\d-\d\d\.csv"',
                        r.headers['content-disposition'])
    lines = r.text.split('\n')
    assert lines[0].startswith('# model_id=') and any(x.startswith('# weights_sha256=') for x in lines)
    assert 'domain_status=unknown' in r.text and 'warnings=DOMAIN_UNKNOWN' in r.text
    body = [x for x in lines if x and not x.startswith('#')]
    assert len(body) == 533 and body[0].split(',')[0] == 'peptide' and body[1].startswith('user_seq,0,1,D,A,')
    r2 = client.post('/v1/export', json={'uniprot_id': 'P12345', 'tile_index': 1, 'format': 'csv'})
    assert [x for x in r2.text.split('\n') if x and not x.startswith('#')][1].startswith('P12345_1,1,1,')
    assert 'P12345-t1' in r2.headers['content-disposition']


def test_api31_json_export_equals_predict(client):
    a = client.post('/v1/export', json={'sequence': SEQ, 'format': 'json'}).json()
    b = predict(client, sequence=SEQ).json()
    assert 'exported_at' in a
    a.pop('exported_at')
    a['provenance'].pop('generated_at'), b['provenance'].pop('generated_at')
    assert a == b


def test_api32_bad_format(client):
    r = client.post('/v1/export', json={'sequence': SEQ, 'format': 'xml'})
    assert r.status_code == 400 and codes(r)[0] == 'INVALID_FORMAT'
    r = client.post('/v1/export', json={'sequence': SEQ})
    assert r.status_code == 422 and codes(r) == ('INVALID_REQUEST', 'format')
    assert client.post('/v1/export', json={'sequence': 'x', 'format': 'csv'}).status_code == 422


# ----------------------------------------------------------------------------- shared runs
def make_run(c, ttl=None, **body):
    body = body or {'sequence': SEQ}
    if ttl is not None:
        body['ttl_days'] = ttl
    return c.post('/v1/runs', json=body)


def test_api40_create_run(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    r = make_run(c)
    j = r.json()
    assert r.status_code == 201
    check('RunCreated', j)
    token = j['share_token']
    assert len(token) == 22
    created = datetime.fromisoformat(j['result']['provenance']['generated_at'].replace('Z', '+00:00'))
    exp = datetime.fromisoformat(j['expires_at'].replace('Z', '+00:00'))
    assert exp - created == timedelta(days=7)
    eng = make_engine(dbcopy)
    with eng.connect() as conn:
        run = conn.execute(select(PredictionRun)).one()
        n = conn.execute(select(PredictionCell).where(PredictionCell.run_id == run.run_id)).fetchall()
    assert run.share_token_hash == hashlib.sha256(token.encode()).hexdigest() and len(n) == 532
    assert token.encode() not in open(dbcopy.removeprefix('sqlite:///'), 'rb').read()      # SEC-04: hash only


def test_api41_read_run_equals_original(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    j = make_run(c, uniprot_id='P12345', tile_index=1).json()
    r = c.get(f"/v1/runs/{j['run_id']}", headers={'X-Share-Token': j['share_token']})
    assert r.status_code == 200 and r.json() == j['result'] and r.headers['cache-control'] == 'no-store'
    j2 = make_run(c, sequence=SEQ, ttl_days=3).json()
    assert c.get(f"/v1/runs/{j2['run_id']}", headers={'X-Share-Token': j2['share_token']}).json() == j2['result']


def test_api42_token_rules(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    j = make_run(c).json()
    url = f"/v1/runs/{j['run_id']}"
    assert codes(c.get(url)) == ('TOKEN_REQUIRED', None) and c.get(url).status_code == 401
    wrong = c.get(url, headers={'X-Share-Token': 'x' * 22})
    assert wrong.status_code == 404 and codes(wrong)[0] == 'RUN_NOT_FOUND'
    unknown = c.get('/v1/runs/00000000-0000-4000-8000-000000000000', headers={'X-Share-Token': j['share_token']})
    assert unknown.status_code == 404 and unknown.json()['message'] == wrong.json()['message']      # no probing
    assert c.get('/v1/runs/not-a-uuid', headers={'X-Share-Token': j['share_token']}).status_code == 404
    assert j['share_token'] not in c.get(url, headers={'X-Share-Token': 'y' * 22}).text


def test_api43_expiry_and_purge(mini, dbcopy):
    c, app = mk_client(mini, dbcopy)
    eng = make_engine(dbcopy)
    j = make_run(c).json()
    past = datetime.now(UTC) - timedelta(minutes=5)
    with eng.begin() as conn:
        conn.execute(PredictionRun.__table__.update().values(created_at=past - timedelta(days=1), expires_at=past))
    r = c.get(f"/v1/runs/{j['run_id']}", headers={'X-Share-Token': j['share_token']})
    assert r.status_code == 410 and codes(r)[0] == 'RUN_EXPIRED'
    assert c.get(f"/v1/runs/{j['run_id']}", headers={'X-Share-Token': j['share_token']}).status_code == 404   # deleted on read
    j2 = make_run(c).json()
    with eng.begin() as conn:
        conn.execute(PredictionRun.__table__.update().values(created_at=past - timedelta(days=1), expires_at=past))
    assert app.state.core.purge_expired() == 1                                                            # UT-10
    with eng.connect() as conn:
        assert conn.execute(text('SELECT count(*) FROM prediction_run')).scalar() == 0
        assert conn.execute(text('SELECT count(*) FROM prediction_cell')).scalar() == 0
    del j2


@pytest.mark.parametrize('ttl', [0, 31, '7', True, 1.5, -1])
def test_run_ttl_validation(mini, dbcopy, ttl):
    c, _ = mk_client(mini, dbcopy)
    r = c.post('/v1/runs', json={'sequence': SEQ, 'ttl_days': ttl})
    assert r.status_code == 422 and codes(r) == ('INVALID_REQUEST', 'ttl_days')


def test_run_refuses_what_predict_refuses(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    assert c.post('/v1/runs', json={'uniprot_id': 'P12345', 'tile_index': 2}).status_code == 422
    assert c.post('/v1/runs', json={'sequence': 'ABC'}).status_code == 422
    with make_engine(dbcopy).connect() as conn:
        assert conn.execute(text('SELECT count(*) FROM prediction_run')).scalar() == 0     # nothing stored on failure


def test_api44_run_export(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    j = make_run(c, uniprot_id='P12345', tile_index=1).json()
    h = {'X-Share-Token': j['share_token']}
    csv_r = c.get(f"/v1/runs/{j['run_id']}/export", params={'format': 'csv'}, headers=h)
    assert csv_r.status_code == 200 and len([x for x in csv_r.text.split('\n') if x and not x.startswith('#')]) == 533
    js = c.get(f"/v1/runs/{j['run_id']}/export", params={'format': 'json'}, headers=h).json()
    js.pop('exported_at')
    assert js == j['result']
    assert c.get(f"/v1/runs/{j['run_id']}/export", params={'format': 'xml'}, headers=h).status_code == 400
    assert c.get(f"/v1/runs/{j['run_id']}/export", headers=h).status_code == 400
    assert c.get(f"/v1/runs/{j['run_id']}/export", params={'format': 'csv'}).status_code == 401


# ----------------------------------------------------------------------------- privacy and fuzz
def test_sec01_canaries_never_reach_logs_or_errors(mini, dbcopy, caplog):
    c, app = mk_client(mini, dbcopy)
    caplog.set_level(logging.DEBUG)
    canary_seq = 'WYFWYFWYFWYFWYFWYFWYFWYFWYFW'[:28]
    bad_canary = 'CANARYBADSEQUENCE'
    canary_acc = 'P12345'
    canary_field = 'canaryfield'
    r1 = predict(c, sequence=canary_seq)
    r2 = predict(c, sequence=bad_canary)
    r3 = predict(c, uniprot_id='P99999', tile_index=1)
    r4 = predict(c, sequence=canary_seq, **{canary_field: 1})
    r5 = c.get('/v1/proteins', params={'query': 'canaryquery'})
    run = make_run(c, sequence=canary_seq).json()
    c.get(f"/v1/runs/{run['run_id']}", headers={'X-Share-Token': run['share_token']})
    c.get('/v1/proteins/P99999/tiles')
    app.state.core.usage.flush(app.state.core.factory)
    server = [r for r in caplog.records if not r.name.startswith(('httpx', 'httpcore', 'asyncio'))]
    logged = '\n'.join(r.getMessage() for r in server)
    assert logged                                                          # the access log did run
    for secret in (canary_seq, bad_canary, 'P99999', run['share_token'], run['run_id'], canary_field,
                   'canaryquery', 'tile_index'):
        assert secret not in logged, secret
    assert canary_acc not in logged.replace('P12345X', '')                 # the real accession is not logged either
    for r in (r2, r3, r4, r5):
        assert bad_canary not in r.text and 'canaryquery' not in r.text
    assert 'GET /v1/proteins/{uniprot_id}/tiles' in logged and 'POST /v1/predict' in logged
    with make_engine(dbcopy).connect() as conn:                            # the counters hold templates only
        used = [row[0] for row in conn.execute(text('SELECT endpoint FROM usage_daily'))]
    assert used and all('P99999' not in u and canary_seq not in u for u in used)
    assert r1.status_code == 200


def test_sec01_sequence_stored_only_for_explicit_share(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    canary = 'WYFWYFWYFWYFWYFWYFWYFWYFWYFW'[:28]
    predict(c, sequence=canary)
    c.post('/v1/export', json={'sequence': canary, 'format': 'csv'})
    assert canary.encode() not in open(dbcopy.removeprefix('sqlite:///'), 'rb').read()
    make_run(c, sequence=canary)
    assert canary.encode() in open(dbcopy.removeprefix('sqlite:///'), 'rb').read()


FUZZ = ['', ' ', '\x00', '‮', '😀' * 28, 'A' * 10_000, "' OR 1=1 --", '../../etc/passwd', '%s%s%s', '{{7*7}}',
        '${jndi:ldap://x}', '\n' * 28, '<script>alert(1)</script>', 'Ｗ' * 28, 'A' * 27 + '퟿', '0' * 28, '١' * 28]


@pytest.mark.parametrize('payload', FUZZ)
def test_sec02_fuzzed_fields_give_coded_4xx(client, payload):
    for body in ({'sequence': payload}, {'uniprot_id': payload, 'tile_index': 1}, {'uniprot_id': 'P12345', 'tile_index': payload},
                 {'sequence': SEQ, 'model_id': payload}, {'sequence': SEQ, 'calibrator': payload}, {payload[:30]: 1}):
        r = client.post('/v1/predict', json=body)
        assert 400 <= r.status_code < 500, (body, r.status_code)
        j = r.json()
        assert set(j) == {'code', 'message', 'field'}
        assert len(payload) < 20 or payload not in r.text
    for path in (f'/v1/proteins/{payload}/tiles', f'/v1/proteins/P12345/tiles/{payload}/measured', f'/v1/models/{payload}',
                 f'/v1/runs/{payload}'):
        r = client.get(quote(path, safe='/{}'), headers={'X-Share-Token': 'z' * 22})
        assert r.status_code < 500
    assert client.get('/v1/proteins', params={'query': payload or 'ab'}).status_code in (200, 400, 422)


@pytest.mark.parametrize('qs', ['query=%00%00', 'query=' + 'A' * 2000, 'query=GENE&limit=abc', 'query=GENE&limit=-5'])
def test_sec02_query_strings(client, qs):
    r = client.get('/v1/proteins?' + qs)
    assert r.status_code in (400, 422) and set(r.json()) == {'code', 'message', 'field'}


def test_internal_errors_hide_details(mini, mini_db, monkeypatch):
    from fastapi.testclient import TestClient
    _, app = mk_client(mini, mini_db['url'])
    c = TestClient(app, raise_server_exceptions=False)

    def boom(*a, **k):
        raise RuntimeError('secret internal detail with /home/user/path')
    monkeypatch.setattr(app.state.core.predictor, 'predict', boom)
    r = predict(c, sequence=SEQ)
    assert r.status_code == 500 and r.json()['code'] == 'INTERNAL_ERROR' and 'secret' not in r.text
    assert 'traceback' not in r.text.lower()


def test_gate_adapter_is_pluggable(mini, mini_db, monkeypatch):
    """A gate model (experiment R3) can be plugged in without touching the API: unknown tiles then get predicted statuses."""
    from degron_footprint.domain import GateAssessment

    class FakeGate:
        available = True
        gate_model_id = 'gate-test-v1'

        def assess(self, seq):
            return GateAssessment('predicted_out_of_domain', 5.2, 'gate-test-v1')
    c, app = mk_client(mini, mini_db['url'])
    app.state.core.predictor.gate = FakeGate()
    r = predict(c, sequence=SEQ)
    assert r.status_code == 422 and codes(r)[0] == 'OUT_OF_DOMAIN' and 'predicted' in r.json()['message']
    r = predict(c, sequence=SEQ, override_domain=True)
    j = r.json()
    assert r.status_code == 200 and j['domain']['status'] == 'predicted_out_of_domain'
    assert j['domain']['gate_model_id'] == 'gate-test-v1'
    assert {'PREDICTED_DOMAIN', 'OUT_OF_DOMAIN_OVERRIDDEN'} <= {w['code'] for w in j['warnings']}
    # measured tiles keep their measured status; the gate only covers 'unknown'
    assert predict(c, uniprot_id='P12345', tile_index=1).json()['domain']['status'] == 'measured_in_domain'


def test_gate_files_with_unknown_kind_are_ignored(tmp_path):
    from degron_footprint.domain import NullGate, load_gate
    w, card = tmp_path / 'gate-weights.npz', tmp_path / 'gate-card.json'
    w.write_bytes(b'x')
    card.write_text(json.dumps({'kind': 'something-new'}))
    assert isinstance(load_gate(w, card), NullGate)
    assert isinstance(load_gate(None, None), NullGate)
    card.write_text('not json')
    assert isinstance(load_gate(w, card), NullGate)


def test_gzip_helper_unused():
    assert gzip.compress(b'') is not None


def test_background_jobs_purge_and_flush(mini, dbcopy):
    """The lifespan tasks: hourly purge and counter flush (shortened to one second here), and a final flush on shutdown."""
    import time

    from fastapi.testclient import TestClient

    from api.main import create_app

    from .conftest import settings_for
    eng = make_engine(dbcopy)
    app = create_app(settings_for(mini, dbcopy, background_jobs=True, purge_interval_seconds=1, usage_flush_seconds=1))
    with TestClient(app) as c:
        j = make_run(c).json()
        predict(c, sequence=SEQ)
        past = datetime.now(UTC) - timedelta(minutes=5)
        with eng.begin() as conn:
            conn.execute(PredictionRun.__table__.update().values(created_at=past - timedelta(days=1), expires_at=past))
        time.sleep(2.6)
        with eng.connect() as conn:
            assert conn.execute(text('SELECT count(*) FROM prediction_run')).scalar() == 0
            rows = conn.execute(text('SELECT endpoint, n_requests FROM usage_daily')).fetchall()
        assert ('POST /v1/predict', 1) in [tuple(r) for r in rows]
        predict(c, sequence=SEQ)
    with eng.connect() as conn:                           # the shutdown flush kept the last request
        total = conn.execute(text("SELECT sum(n_requests) FROM usage_daily WHERE endpoint = 'POST /v1/predict'")).scalar()
    assert total == 2
    assert j['run_id']
