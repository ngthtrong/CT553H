"""WP6: experimental import and comparison (UC-05, UC-09; IMP-01…04, SEC-02 of test-plan.md)."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import func, select, text

from db.models import ImportObservation
from db.session import make_engine

from .conftest import mk_client
from .contract import check

HEADER = 'peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id,missing_reason'
META = {'name': 'GPS follow-up', 'assay': 'GPS', 'endpoint': 'delta_psi', 'units': 'PSI', 'source': 'lab book 12',
        'reference_description': 'P12345 tile 1', 'compatibility': 'zhang_gps_dpsi'}


@pytest.fixture()
def wc(mini, dbcopy, tmp_path):
    c, app = mk_client(mini, dbcopy, workspace_dir=tmp_path / 'ws')
    with c:
        yield c, app, dbcopy


def project(c) -> str:
    return c.post('/v1/projects', json={'name': 'imports'}).json()['project_id']


def upload(c, pid, body: str | bytes, meta: dict | None = None, filename='../../etc/obs.csv'):
    data = body.encode() if isinstance(body, str) else body
    return c.post(f'/v1/projects/{pid}/datasets',
                  files={'file': (filename, data, 'text/csv')},
                  data={'metadata': json.dumps({**META, **(meta or {})})})


def commit(c, did, ack=True):
    return c.post(f'/v1/datasets/{did}', json={'action': 'commit', 'acknowledge_warnings': ack})


def analysis(c, pid):
    return c.post(f'/v1/projects/{pid}/analyses', json={'request': {'uniprot_id': 'P12345', 'tile_index': 1}}).json()


def ref_counts(url):
    with make_engine(url).connect() as conn:
        return {t: conn.execute(text(f'SELECT count(*) FROM {t}')).scalar()
                for t in ('protein', 'tile', 'measured_cell', 'clinvar_variant', 'model_version')}


# --- IMP-01: preview and validation ---------------------------------------------------------------------------------

def test_imp01_preview_reports_every_row_and_stores_nothing_committed(wc):
    c, app, url = wc
    pid = project(c)
    seq = analysis(c, pid)['result']['tile']['sequence']
    w1, w2 = seq[0], seq[1]
    body = '\n'.join([
        HEADER,
        f'p1,{seq},1,{w1},A,0.5,r1,',                       # 2 valid
        f'p1,{seq},2,{w2},A,,r1,below detection',           # 3 missing with reason
        f'p1,{seq},1,X,C,0.5,r1,',                          # 4 WT mismatch
        f'p1,{seq},1,{w1},C,inf,r1,',                       # 5 non-finite
        f'p1,{seq},1,{w1},A,0.5,r1,',                       # 6 duplicate of row 2
        f'p1,{seq},1,{w1},A,0.9,r1,',                       # 7 conflicting with row 2
        f'p1,{seq},3,{seq[2]},A,,r1,',                      # 8 empty value without reason
        f'=HYPERLINK("x"),{seq},4,{seq[3]},A,1.0,r1,',      # 9 formula text: warning only
        f'p1,{seq[:27]},1,{w1},A,1,r1,',                    # 10 wrong length
    ])
    r = upload(c, pid, body)
    assert r.status_code == 201, r.text
    d = r.json()
    check('Dataset', d)
    assert d['state'] == 'staged' and d['committable'] is False and d['revision'] == 1
    assert d['sha256'] == hashlib.sha256(body.encode()).hexdigest()
    assert d['counts'] == {'rows': 9, 'valid': 2, 'missing': 1, 'duplicate': 1, 'conflicting': 1, 'rejected': 4,
                           'warnings': 1, 'mapping_verified': 0, 'mapping_unverified': 0}
    by_row = {(i.get('row'), i['code']) for i in d['issues']}
    assert by_row >= {(4, 'WT_MISMATCH'), (5, 'NONFINITE_VALUE'), (6, 'DUPLICATE_KEY'), (7, 'CONFLICTING_VALUE'),
                      (8, 'MISSING_REASON'), (9, 'FORMULA_TEXT'), (10, 'INVALID_SEQUENCE')}
    stored = list((app.state.core.settings.workspace_dir / pid).iterdir())
    assert [p.name for p in stored] == [f"{d['dataset_id']}.csv"]          # generated name, not the upload's
    with make_engine(url).connect() as conn:
        assert conn.execute(select(func.count()).select_from(ImportObservation)).scalar() == 3
        assert conn.execute(select(ImportObservation.observed_value).where(
            ImportObservation.missing_reason.is_not(None))).scalar() is None    # never a silent zero
    assert commit(c, d['dataset_id']).json()['code'] == 'IMPORT_INVALID'


def test_imp01_tsv_with_bom(wc):
    c, _, _ = wc
    pid = project(c)
    seq = analysis(c, pid)['result']['tile']['sequence']
    body = '﻿' + HEADER.replace(',', '\t') + '\n' + f'p\t{seq}\t1\t{seq[0]}\tA\t0.1\tr1\t'
    d = upload(c, pid, body).json()
    assert d['committable'] is True and d['counts']['valid'] == 1


@pytest.mark.parametrize('meta, field', [({'endpoint': ''}, 'metadata.endpoint'), ({'compatibility': 'gps'},
                                         'metadata.compatibility'), ({'owner': 'x'}, 'metadata')])
def test_imp01_metadata_required(wc, meta, field):
    c, _, _ = wc
    r = upload(c, project(c), HEADER + '\n', meta)
    assert r.status_code == 422 and r.json()['code'] == 'IMPORT_INVALID' and r.json()['field'] == field


def test_imp01_inconsistent_dpsi_declaration_blocks(wc):
    c, _, _ = wc
    pid = project(c)
    seq = analysis(c, pid)['result']['tile']['sequence']
    d = upload(c, pid, HEADER + f'\np,{seq},1,{seq[0]},A,3.2,r1,', {'endpoint': 'PSI (absolute)'}).json()
    assert d['committable'] is False and d['issues'][0]['code'] == 'INCONSISTENT_ENDPOINT'
    ok = upload(c, pid, HEADER + f'\np,{seq},1,{seq[0]},A,3.2,r1,', {'endpoint': 'PSI', 'compatibility': 'other'})
    assert ok.json()['committable'] is True


def test_imp01_limits(mini, dbcopy, tmp_path):
    c, _ = mk_client(mini, dbcopy, workspace_dir=tmp_path / 'ws', max_import_rows=2, max_import_bytes=2000)
    with c:
        pid = project(c)
        seq = 'A' * 28
        rows = '\n'.join(f'p,{seq},{i},A,C,0.1,r1,' for i in range(1, 4))
        d = upload(c, pid, HEADER + '\n' + rows).json()
        assert any(i['code'] == 'TOO_MANY_ROWS' for i in d['issues']) and d['committable'] is False
        r = upload(c, pid, HEADER + '\n' + 'x' * 3000)
        assert r.status_code == 413


def test_imp01_missing_column_and_not_utf8(wc):
    c, _, _ = wc
    pid = project(c)
    assert upload(c, pid, 'peptide_id,position\np,1').json()['issues'][0]['code'] == 'MISSING_COLUMN'
    assert upload(c, pid, b'\xff\xfe\x00bad').json()['issues'][0]['code'] == 'ENCODING'
    r = c.post(f'/v1/projects/{pid}/datasets', json={'file': 'x'})
    assert r.status_code == 422


# --- IMP-02: commit lifecycle ---------------------------------------------------------------------------------------

def test_imp02_commit_needs_acknowledged_warnings_and_is_immutable(wc):
    c, _, url = wc
    pid = project(c)
    seq = analysis(c, pid)['result']['tile']['sequence']
    body = HEADER + f'\n@formula,{seq},1,{seq[0]},A,0.4,r1,'
    reference = ref_counts(url)
    d = upload(c, pid, body).json()
    assert d['committable'] is True
    assert commit(c, d['dataset_id'], ack=False).json()['field'] == 'acknowledge_warnings'
    done = commit(c, d['dataset_id']).json()
    assert done['state'] == 'committed' and done['committable'] is False and 'committed_at' in done
    assert commit(c, d['dataset_id']).json() == done                         # idempotent, unchanged
    again = upload(c, pid, body).json()
    assert again['revision'] == 2 and again['dataset_id'] != d['dataset_id']
    assert ref_counts(url) == reference                                      # D-8/D-11: reference untouched
    page = c.get(f'/v1/projects/{pid}/datasets').json()
    check('DatasetPage', page)
    assert page['total'] == 2


def test_imp02_expired_preview(wc):
    c, app, url = wc
    pid = project(c)
    seq = analysis(c, pid)['result']['tile']['sequence']
    d = upload(c, pid, HEADER + f'\np,{seq},1,{seq[0]},A,0.4,r1,').json()
    other = upload(c, pid, HEADER + f'\np,{seq},2,{seq[1]},A,0.4,r1,').json()
    past = datetime.now(UTC) - timedelta(hours=1)
    with make_engine(url).begin() as conn:
        conn.execute(text('UPDATE import_dataset SET expires_at = :t'), {'t': past})
    r = commit(c, d['dataset_id'])
    assert r.status_code == 409 and r.json()['code'] == 'IMPORT_EXPIRED'
    assert c.get(f"/v1/datasets/{d['dataset_id']}").json()['state'] == 'expired'
    assert app.state.core.purge_expired() >= 1
    files = {p.name for p in (app.state.core.settings.workspace_dir / pid).iterdir()}
    assert f"{other['dataset_id']}.csv" not in files
    assert c.get(f"/v1/datasets/{other['dataset_id']}").json()['state'] == 'expired'


def test_imp02_delete_dataset(wc):
    c, app, _ = wc
    pid = project(c)
    a = analysis(c, pid)
    seq = a['result']['tile']['sequence']
    d = upload(c, pid, HEADER + f'\np,{seq},1,{seq[0]},A,0.4,r1,').json()
    commit(c, d['dataset_id'])
    c.post(f"/v1/analyses/{a['analysis_id']}/comparisons", json={'dataset_id': d['dataset_id'], 'replicate_id': 'r1'})
    r = c.delete(f"/v1/datasets/{d['dataset_id']}")
    assert r.status_code == 409 and r.json()['dependencies'] == {'observations': 1, 'comparisons': 1}
    assert c.delete(f"/v1/datasets/{d['dataset_id']}?confirm=true").status_code == 204
    assert c.get(f"/v1/analyses/{a['analysis_id']}/comparisons").json()['total'] == 0
    assert not list((app.state.core.settings.workspace_dir / pid).iterdir())


# --- IMP-03: alignment and mapping ----------------------------------------------------------------------------------

def test_imp03_protein_mapping_checked_against_reference(wc):
    c, _, _ = wc
    pid = project(c)
    seq = analysis(c, pid)['result']['tile']['sequence']
    head = HEADER + ',uniprot_id,reference_release,start_pos'
    d = upload(c, pid, '\n'.join([
        head,
        f'p,{seq},1,{seq[0]},A,0.4,r1,,P12345,2026_03,1',     # verified
        f'p,{seq},2,{seq[1]},A,0.4,r1,,P12345,2026_03,5',     # conflict: the reference differs at start 5
        f'p,{seq},3,{seq[2]},A,0.4,r1,,P12345,2019_01,1',     # other release: unverified (warning)
        f'p,{seq},4,{seq[3]},A,0.4,r1,,P12345,,1',            # partial mapping
    ])).json()
    assert d['counts']['mapping_verified'] == 1 and d['counts']['mapping_unverified'] == 1
    codes = {(i.get('row'), i['code']) for i in d['issues']}
    assert {(3, 'MAPPING_CONFLICT'), (4, 'MAPPING_UNVERIFIED'), (5, 'PARTIAL_MAPPING')} <= codes


# --- IMP-04: comparison ---------------------------------------------------------------------------------------------

def _cells(a, k=4):
    """k substitutions at positions 1…2 sorted by predicted score (ascending)."""
    cells = [x for x in a['result']['cells'] if x['position'] <= 2][:k]
    return sorted(cells, key=lambda x: x['score_dpsi_raw'])


def test_imp04_metrics_match_hand_calculation(wc):
    c, _, _ = wc
    pid = project(c)
    a = analysis(c, pid)
    seq = a['result']['tile']['sequence']
    cells = _cells(a)
    d_off = [0.5, -1.0, 0.25, 2.0]                     # residual = predicted − observed = d
    reversed_obs = [4.0, 3.0, 2.0, 1.0]                # strictly decreasing in predicted order → Spearman −1
    lines = [HEADER]
    for x, d in zip(cells, d_off, strict=True):
        lines.append(f"p,{seq},{x['position']},{x['wt_aa']},{x['mut_aa']},{x['score_dpsi_raw'] - d!r},r1,")
    for x, o in zip(cells, reversed_obs, strict=True):
        lines.append(f"p,{seq},{x['position']},{x['wt_aa']},{x['mut_aa']},{o},r2,")
        lines.append(f"p,{seq},{x['position']},{x['wt_aa']},{x['mut_aa']},{o + 1.0},r3,")
        lines.append(f"p,{seq},{x['position']},{x['wt_aa']},{x['mut_aa']},{o + 5.0},r4,")
    lines.append(f"other,{'A' * 28},1,A,C,9.0,r1,")    # a different peptide: unmatched
    ds = upload(c, pid, '\n'.join(lines)).json()
    assert ds['committable'], ds['issues']
    commit(c, ds['dataset_id'])
    url = f"/v1/analyses/{a['analysis_id']}/comparisons"

    r1 = c.post(url, json={'dataset_id': ds['dataset_id'], 'replicate_id': 'r1'})
    assert r1.status_code == 201, r1.text
    one = r1.json()
    check('Comparison', one)
    assert one['compatible'] is True and one['matched'] == 4
    assert one['mae'] == pytest.approx(0.9375, abs=1e-12)
    assert [row['residual'] for row in sorted(one['rows'], key=lambda r: r['predicted_dpsi_raw'])] == \
        pytest.approx(d_off, abs=1e-12)
    assert one['counts']['unmatched_sequence'] == 1 and one['counts']['other_replicates'] == 12

    r2 = c.post(url, json={'dataset_id': ds['dataset_id'], 'replicate_id': 'r2'}).json()
    assert r2['spearman'] == pytest.approx(-1.0, abs=1e-12)

    med = c.post(url, json={'dataset_id': ds['dataset_id'], 'aggregation': 'median'}).json()
    by = {(r['position'], r['mut_aa']): r for r in med['rows']}
    x0 = cells[0]
    # replicates for x0: pred−0.5, 4, 5, 9 → median of four = (4 + 5) / 2 = 4.5 when pred−0.5 < 4
    vals = sorted([x0['score_dpsi_raw'] - 0.5, 4.0, 5.0, 9.0])
    assert by[(x0['position'], x0['mut_aa'])]['observed'] == pytest.approx((vals[1] + vals[2]) / 2, abs=1e-12)
    assert by[(x0['position'], x0['mut_aa'])]['n_replicates'] == 4
    mean_cmp = c.post(url, json={'dataset_id': ds['dataset_id'], 'aggregation': 'mean'}).json()
    assert {(r['position'], r['mut_aa']): r for r in mean_cmp['rows']}[(x0['position'], x0['mut_aa'])]['observed'] \
        == pytest.approx(sum(vals) / 4, abs=1e-12)
    assert mean_cmp['provenance']['note'] == 'comparison only; not used to retrain the model'
    assert c.get(f"/v1/comparisons/{one['comparison_id']}").json() == one
    listed = c.get(url).json()
    check('ComparisonPage', listed)
    assert listed['total'] == 4


def test_imp04_spearman_unavailable_and_incompatible_endpoint(wc):
    c, _, _ = wc
    pid = project(c)
    a = analysis(c, pid)
    seq = a['result']['tile']['sequence']
    x = _cells(a, 2)
    two = upload(c, pid, '\n'.join([HEADER] + [f"p,{seq},{v['position']},{v['wt_aa']},{v['mut_aa']},1.0,r1,"
                                               for v in x])).json()
    commit(c, two['dataset_id'])
    cmp = c.post(f"/v1/analyses/{a['analysis_id']}/comparisons",
                 json={'dataset_id': two['dataset_id'], 'replicate_id': 'r1'}).json()
    assert cmp['spearman'] is None and cmp['mae'] is not None and 'three pairs' in cmp['metric_unavailable_reason']
    other = upload(c, pid, '\n'.join([HEADER, f"p,{seq},{x[0]['position']},{x[0]['wt_aa']},{x[0]['mut_aa']},12.5,r1,"]),
                   {'name': 'half-life', 'endpoint': 'half-life', 'units': 'h', 'compatibility': 'other'}).json()
    commit(c, other['dataset_id'])
    inc = c.post(f"/v1/analyses/{a['analysis_id']}/comparisons",
                 json={'dataset_id': other['dataset_id'], 'replicate_id': 'r1'}).json()
    assert inc['compatible'] is False and inc['mae'] is None and inc['spearman'] is None
    assert inc['rows'][0]['residual'] is None and inc['rows'][0]['predicted_dpsi_raw'] is None
    assert inc['rows'][0]['units'] == 'h'


def test_imp04_refusals(wc):
    c, _, _ = wc
    a_pid, b_pid = project(c), project(c)
    a = analysis(c, a_pid)
    seq = a['result']['tile']['sequence']
    staged = upload(c, a_pid, HEADER + f'\np,{seq},1,{seq[0]},A,0.4,r1,').json()
    url = f"/v1/analyses/{a['analysis_id']}/comparisons"
    assert c.post(url, json={'dataset_id': staged['dataset_id'], 'replicate_id': 'r1'}).json()['code'] == \
        'DATASET_NOT_COMMITTED'
    foreign = upload(c, b_pid, HEADER + f'\np,{seq},1,{seq[0]},A,0.4,r1,').json()
    commit(c, foreign['dataset_id'])
    assert c.post(url, json={'dataset_id': foreign['dataset_id'], 'replicate_id': 'r1'}).status_code == 404
    commit(c, staged['dataset_id'])
    assert c.post(url, json={'dataset_id': staged['dataset_id']}).status_code == 422
    assert c.post(url, json={'dataset_id': staged['dataset_id'], 'replicate_id': 'zz'}).json()['field'] == 'replicate_id'


def test_imp04_export_with_comparison_neutralises_formulas(wc):
    c, _, _ = wc
    pid = project(c)
    a = analysis(c, pid)
    seq = a['result']['tile']['sequence']
    x = _cells(a, 1)[0]
    d = upload(c, pid, HEADER + f"\np,{seq},{x['position']},{x['wt_aa']},{x['mut_aa']},0.7,r1,",
               {'name': 'odd', 'units': '=1+1', 'endpoint': 'other', 'compatibility': 'other'}).json()
    commit(c, d['dataset_id'])
    cmp = c.post(f"/v1/analyses/{a['analysis_id']}/comparisons",
                 json={'dataset_id': d['dataset_id'], 'replicate_id': 'r1'}).json()
    csv_text = c.get(f"/v1/analyses/{a['analysis_id']}/export?format=csv&comparison_id={cmp['comparison_id']}").text
    header = next(ln for ln in csv_text.splitlines() if ln.startswith('peptide,'))
    assert header.endswith('measurement_observed,measurement_units,measurement_n_replicates,'
                           'measurement_residual_pred_minus_obs')
    assert "'=1+1" in csv_text and ',=1+1' not in csv_text
    assert '# comparison_note=comparison only; not used to retrain the model' in csv_text
    other = c.post('/v1/projects', json={'name': 'z'}).json()['project_id']
    b = analysis(c, other)
    r = c.get(f"/v1/analyses/{b['analysis_id']}/export?format=csv&comparison_id={cmp['comparison_id']}")
    assert r.status_code == 404 and r.json()['code'] == 'COMPARISON_NOT_FOUND'
