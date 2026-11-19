"""WP4: projects and saved analyses (UC-10; HIST-01…03 of test-plan.md), on private copies of the mini database."""
from __future__ import annotations

import logging
import uuid

import pytest
from sqlalchemy import func, select, text

from db.models import AnalysisCell, AnalysisRun, Project
from db.session import make_engine

from .conftest import mk_client
from .contract import check

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'


@pytest.fixture()
def wc(mini, dbcopy, tmp_path):
    """A client with its own database copy and workspace directory."""
    c, app = mk_client(mini, dbcopy, workspace_dir=tmp_path / 'ws')
    with c:
        yield c, app, dbcopy


def new_project(c, name='Follow-up of GENE1') -> str:
    r = c.post('/v1/projects', json={'name': name, 'description': 'tiles 1-3'})
    assert r.status_code == 201, r.text
    check('Project', r.json())
    return r.json()['project_id']


def save(c, pid, **request):
    return c.post(f'/v1/projects/{pid}/analyses', json={'request': request})


# --- HIST-01: projects --------------------------------------------------------------------------------------------

def test_hist01_project_crud_and_listing(wc):
    c, _, _ = wc
    a = new_project(c, 'A')
    b = new_project(c, 'B')
    assert c.patch(f'/v1/projects/{a}', json={'name': 'A renamed'}).json()['name'] == 'A renamed'
    page = c.get('/v1/projects?limit=1').json()
    check('ProjectPage', page)
    assert page['total'] == 2 and len(page['items']) == 1
    assert page['items'][0]['project_id'] == a                      # most recently updated first
    assert c.get(f'/v1/projects/{b}').json()['counts'] == {'analyses': 0, 'jobs': 0, 'datasets': 0}


@pytest.mark.parametrize('body, field', [({}, 'name'), ({'name': ''}, 'name'), ({'name': 'x' * 201}, 'name'),
                                         ({'name': 7}, 'name'), ({'name': 'ok', 'owner': 'me'}, None)])
def test_hist01_project_validation(wc, body, field):
    c, _, _ = wc
    r = c.post('/v1/projects', json=body)
    assert r.status_code == 422 and r.json()['field'] == field


@pytest.mark.parametrize('url', ['/v1/projects/not-a-uuid', '/v1/projects?limit=0', '/v1/projects?limit=201',
                                 '/v1/projects?offset=-1'])
def test_hist01_bad_ids_and_pages(wc, url):
    c, _, _ = wc
    assert c.get(url).status_code == 422


def test_hist01_unknown_project(wc):
    c, _, _ = wc
    r = c.get(f'/v1/projects/{uuid.uuid4()}')
    assert r.status_code == 404 and r.json()['code'] == 'PROJECT_NOT_FOUND'


def test_hist01_preview_is_not_stored(wc, caplog):
    """An unsaved prediction leaves no workspace row and no sequence in the log (NFR-09, SEC-01)."""
    c, _, url = wc
    new_project(c)
    caplog.set_level(logging.INFO)
    assert c.post('/v1/predict', json={'sequence': SEQ}).status_code == 200
    with make_engine(url).connect() as conn:
        assert conn.execute(select(func.count()).select_from(AnalysisRun)).scalar() == 0
    assert SEQ not in caplog.text


# --- HIST-02: saved analyses --------------------------------------------------------------------------------------

def test_hist02_save_and_reopen_after_restart(mini, wc):
    c, _, url = wc
    pid = new_project(c)
    r = save(c, pid, uniprot_id='P12345', tile_index=1)
    assert r.status_code == 201, r.text
    saved = r.json()
    check('SavedAnalysis', saved)
    assert len(saved['result']['cells']) == 532
    snap = saved['snapshot']
    assert snap['model']['weights_sha256'] == saved['result']['provenance']['weights_sha256']
    assert snap['annotations']['clinvar']['state'] == 'available'
    assert snap['annotations']['reference']['uniprot_release']
    c2, _ = mk_client(mini, url)                                       # a fresh process on the same database
    with c2:
        again = c2.get(f"/v1/analyses/{saved['analysis_id']}").json()
    assert again == saved
    listed = c.get(f'/v1/projects/{pid}/analyses').json()
    check('SavedAnalysisPage', listed)
    assert listed['total'] == 1 and 'result' not in listed['items'][0]
    assert listed['items'][0]['tile']['tile_index'] == 1 and listed['items'][0]['warning_codes'] == ['TRAINING_PEPTIDE']
    assert c.get(f'/v1/projects/{pid}').json()['counts']['analyses'] == 1
    with make_engine(url).connect() as conn:
        assert conn.execute(select(func.count()).select_from(AnalysisCell)).scalar() == 532


def test_hist02_snapshot_does_not_follow_reference_changes(wc):
    """Replacing ClinVar/tile data after saving must not change the saved analysis (A-6, db-design §11)."""
    c, _, url = wc
    pid = new_project(c)
    saved = save(c, pid, uniprot_id='P12345', tile_index=1).json()
    with make_engine(url).begin() as conn:
        conn.execute(text('DELETE FROM clinvar_variant'))
        conn.execute(text("UPDATE tile SET domain_status = 'unknown', psi_wt_measured = NULL "
                          "WHERE uniprot_acc = 'P12345' AND tile_index = 1"))
    assert c.get(f"/v1/analyses/{saved['analysis_id']}").json() == saved


def test_hist02_typed_sequence_has_no_clinvar_lookup(wc):
    c, _, _ = wc
    pid = new_project(c)
    snap = save(c, pid, sequence=SEQ).json()['snapshot']
    assert snap['annotations']['clinvar']['state'] == 'mapping_unavailable'
    assert snap['request']['input_kind'] == 'sequence'


def test_hist02_rerun_is_a_new_record_and_parent_may_go(wc):
    c, _, _ = wc
    pid = new_project(c)
    first = save(c, pid, sequence=SEQ).json()
    r = c.post(f'/v1/projects/{pid}/analyses', json={'request': {'sequence': SEQ}, 'parent_analysis_id': first['analysis_id']})
    second = r.json()
    assert r.status_code == 201 and second['analysis_id'] != first['analysis_id']
    assert second['parent_analysis_id'] == first['analysis_id'] and second['parent_available'] is True
    assert c.delete(f"/v1/analyses/{first['analysis_id']}?confirm=true").status_code == 204
    reopened = c.get(f"/v1/analyses/{second['analysis_id']}").json()
    assert reopened['parent_analysis_id'] == first['analysis_id'] and reopened['parent_available'] is False


def test_hist02_parent_from_other_project_refused(wc):
    c, _, _ = wc
    a, b = new_project(c, 'a'), new_project(c, 'b')
    first = save(c, a, sequence=SEQ).json()
    r = c.post(f'/v1/projects/{b}/analyses', json={'request': {'sequence': SEQ}, 'parent_analysis_id': first['analysis_id']})
    assert r.status_code == 404 and r.json()['code'] == 'ANALYSIS_NOT_FOUND'


def test_hist02_invalid_request_saves_nothing(wc):
    c, _, url = wc
    pid = new_project(c)
    r = save(c, pid, sequence='ACD')
    assert r.status_code == 422 and r.json()['code'] == 'INVALID_LENGTH'
    r = save(c, pid, uniprot_id='P12345', tile_index=2)            # out of domain without override
    assert r.json()['code'] == 'OUT_OF_DOMAIN'
    with make_engine(url).connect() as conn:
        assert conn.execute(select(func.count()).select_from(AnalysisRun)).scalar() == 0


def test_hist02_export_from_snapshot(wc):
    c, _, url = wc
    pid = new_project(c)
    saved = save(c, pid, uniprot_id='P12345', tile_index=1).json()
    csv_text = c.get(f"/v1/analyses/{saved['analysis_id']}/export?format=csv").text
    lines = [ln for ln in csv_text.splitlines() if not ln.startswith('#')]
    assert lines[0] == ('peptide,tile,position,wt_aa,mut_aa,score_dpsi_raw,p_dpsi_ge_1_calibrated,rank_in_tile,'
                        'top10pct_in_tile,score_seed_sd,score_seed_min,score_seed_max')     # seed spread: plan-system 1.3
    assert len(lines) == 533
    assert f"# analysis_id={saved['analysis_id']}" in csv_text and '# clinvar_state=available' in csv_text
    assert SEQ not in c.get(f"/v1/analyses/{saved['analysis_id']}/export?format=csv").headers['content-disposition']
    with make_engine(url).begin() as conn:
        conn.execute(text('DELETE FROM clinvar_variant'))
    payload = c.get(f"/v1/analyses/{saved['analysis_id']}/export?format=json").json()
    assert payload['snapshot']['annotations']['clinvar']['state'] == 'available'     # history, not today's table
    assert c.get(f"/v1/analyses/{saved['analysis_id']}/export?format=xml").json()['code'] == 'INVALID_FORMAT'


# --- HIST-03: deletion --------------------------------------------------------------------------------------------

def test_hist03_delete_needs_confirmation_and_spares_others(wc):
    c, _, url = wc
    keep, gone = new_project(c, 'keep'), new_project(c, 'gone')
    kept = save(c, keep, sequence=SEQ).json()
    save(c, gone, sequence=SEQ)
    with make_engine(url).connect() as conn:
        ref = {t: conn.execute(text(f'SELECT count(*) FROM {t}')).scalar()
               for t in ('protein', 'tile', 'clinvar_variant', 'model_version')}
    r = c.delete(f'/v1/projects/{gone}')
    assert r.status_code == 409 and r.json()['code'] == 'CONFIRMATION_REQUIRED'
    assert r.json()['dependencies']['analyses'] == 1
    assert c.get(f'/v1/projects/{gone}').status_code == 200
    assert c.delete(f'/v1/projects/{gone}?confirm=true').status_code == 204
    assert c.get(f'/v1/projects/{gone}').status_code == 404
    assert c.get(f"/v1/analyses/{kept['analysis_id']}").status_code == 200
    with make_engine(url).connect() as conn:
        assert {t: conn.execute(text(f'SELECT count(*) FROM {t}')).scalar() for t in ref} == ref
        assert conn.execute(select(func.count()).select_from(AnalysisCell)).scalar() == 532


def test_hist03_failed_file_cleanup_is_reported_and_retried(wc, monkeypatch):
    c, app, url = wc
    pid = new_project(c)
    save(c, pid, sequence=SEQ)
    d = app.state.core.settings.workspace_dir / pid
    d.mkdir(parents=True)
    (d / 'staged.csv').write_text('x')
    monkeypatch.setattr('api.routers.projects.remove_project_dir', lambda root, p: 'PermissionError: denied')
    r = c.delete(f'/v1/projects/{pid}?confirm=true')
    assert r.status_code == 503
    got = c.get(f'/v1/projects/{pid}').json()
    assert got['deletion_pending'] is True                              # visible, not silently "deleted"
    assert save(c, pid, sequence=SEQ).json()['code'] == 'JOB_STATE_CONFLICT'
    monkeypatch.undo()
    assert c.delete(f'/v1/projects/{pid}?confirm=true').status_code == 204
    assert not d.exists()
    with make_engine(url).connect() as conn:
        assert conn.execute(select(func.count()).select_from(Project)).scalar() == 0


def test_hist03_analysis_delete_confirmation(wc):
    c, _, _ = wc
    pid = new_project(c)
    a = save(c, pid, sequence=SEQ).json()['analysis_id']
    r = c.delete(f'/v1/analyses/{a}')
    assert r.status_code == 409 and r.json()['dependencies'] == {'comparisons': 0, 'model_comparisons': 0}
    assert c.delete(f'/v1/analyses/{a}?confirm=true').status_code == 204
    assert c.get(f'/v1/analyses/{a}').json()['code'] == 'ANALYSIS_NOT_FOUND'


def test_cors_allows_workspace_methods(wc):
    c, _, _ = wc
    r = c.options('/v1/projects/x', headers={'Origin': 'http://localhost:5173', 'Access-Control-Request-Method': 'DELETE'})
    assert 'DELETE' in r.headers.get('access-control-allow-methods', '')


# --- SEC-03: writes from another site --------------------------------------------------------------------------------

@pytest.mark.parametrize('headers', [{'Origin': 'https://evil.example'}, {'Sec-Fetch-Site': 'cross-site'}])
def test_sec03_cross_site_writes_are_refused(wc, headers):
    c, _, url = wc
    r = c.post('/v1/projects', json={'name': 'x'}, headers=headers)
    assert r.status_code == 403 and r.json()['code'] == 'INVALID_REQUEST'
    pid = new_project(c)
    assert c.delete(f'/v1/projects/{pid}?confirm=true', headers=headers).status_code == 403
    r = c.post(f'/v1/projects/{pid}/datasets', files={'file': ('a.csv', b'x', 'text/csv')}, data={'metadata': '{}'},
               headers=headers)
    assert r.status_code == 403
    with make_engine(url).connect() as conn:
        assert conn.execute(select(func.count()).select_from(Project)).scalar() == 1
    assert c.get('/v1/projects', headers=headers).status_code == 200            # reads are not affected


def test_sec03_allowed_and_same_origin_writes_pass(wc):
    c, _, _ = wc
    assert c.post('/v1/projects', json={'name': 'a'}, headers={'Origin': 'http://localhost:5173'}).status_code == 201
    assert c.post('/v1/projects', json={'name': 'b'}, headers={'Origin': 'http://testserver'}).status_code == 201
    assert c.post('/v1/projects', json={'name': 'c'}, headers={'Sec-Fetch-Site': 'same-origin'}).status_code == 201


@pytest.mark.parametrize('ctype', ['text/plain', 'application/x-www-form-urlencoded', None])
def test_sec03_json_body_must_be_declared_json(wc, ctype):
    """A text/plain or form body is what a page can send cross-site without a preflight."""
    c, _, _ = wc
    headers = {'content-type': ctype} if ctype else {}
    r = c.post('/v1/projects', content=b'{"name": "x"}', headers=headers)
    assert r.status_code == 415 and r.json()['code'] == 'INVALID_REQUEST'
    assert c.post('/v1/predict', content=f'{{"sequence": "{SEQ}"}}'.encode(), headers=headers).status_code == 415
