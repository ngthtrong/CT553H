"""WP2 of the implementation plan: workspace tables (migration 0002), borderline domain states (0003) and workspace
paths. Test IDs from system/test-plan.md where one applies (HIST-03, SEC-02, DEP-01); the rest check db-design §11
invariants directly."""
from __future__ import annotations

import os
import shutil
import sqlite3
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from api.workspace import WorkspacePathError, dataset_relpath, project_dir, remove_project_dir, resolve_stored
from db.models import (
    AnalysisCell,
    AnalysisJob,
    AnalysisRun,
    Comparison,
    ImportDataset,
    ImportObservation,
    JobItem,
    ModelVersion,
    Project,
)
from db.session import make_engine, make_session_factory

APP = Path(__file__).resolve().parents[1]
REFERENCE = ('protein', 'tile', 'measured_cell', 'clinvar_variant', 'model_version', 'data_source')
WORKSPACE = ('project', 'analysis_job', 'job_item', 'analysis_run', 'analysis_cell', 'import_dataset',
             'import_observation', 'comparison')
SEQ = 'MKTAYIAKQRQISFVKSHFSRQLEERLG'
NOW = datetime(2026, 11, 16, 12, 0, tzinfo=UTC)


def alembic_cfg(url: str) -> Config:
    cfg = Config(str(APP / 'backend/alembic.ini'))
    cfg.set_main_option('sqlalchemy.url', url)
    return cfg


def counts(url: str, tables) -> dict[str, int]:
    with make_engine(url).connect() as c:
        return {t: c.execute(text(f'SELECT count(*) FROM {t}')).scalar_one() for t in tables}


def uid() -> str:
    return str(uuid.uuid4())


@pytest.fixture()
def ws(dbcopy):
    """A session on a private copy of the miniature database at head, plus the effect model id."""
    eng = make_engine(dbcopy)
    session = make_session_factory(eng)()
    model_id = session.scalars(select(ModelVersion.model_id).where(ModelVersion.role == 'effect')).first()
    yield session, model_id, dbcopy
    session.close()
    eng.dispose()


def add_project(s, name='p') -> str:
    pid = uid()
    s.add(Project(project_id=pid, name=name, created_at=NOW, updated_at=NOW))
    s.flush()
    return pid


def add_job(s, pid, model_id) -> str:
    jid = uid()
    s.add(AnalysisJob(job_id=jid, project_id=pid, mode='peptides', total=1, input_snapshot={}, configuration_snapshot={},
                      model_id=model_id, model_sha256='0' * 64, calibrator='platt', created_at=NOW, updated_at=NOW))
    s.add(JobItem(job_id=jid, item_id='i1', ordinal=1, input_id='pep-1', sequence=SEQ, updated_at=NOW))
    s.flush()
    return jid


def run_row(pid, model_id, **kw) -> AnalysisRun:
    base = dict(analysis_id=uid(), project_id=pid, model_id=model_id, input_kind='sequence', input_sequence=SEQ,
                domain_status='unknown', result={}, provenance={}, annotation_snapshot={}, created_at=NOW)
    base.update(kw)
    return AnalysisRun(**base)


def dataset_row(pid, **kw) -> ImportDataset:
    did = kw.pop('dataset_id', uid())
    base = dict(dataset_id=did, project_id=pid, name='screen', revision=1, state='staged',
                file_path=dataset_relpath(pid, did, '.csv'), sha256='a' * 64, assay='GPS', endpoint='delta_psi',
                units='PSI', source='lab', reference_description='ref', compatibility='zhang_gps_dpsi',
                committable=True, counts={}, validation_report=[], created_at=NOW, expires_at=NOW + timedelta(hours=24))
    base.update(kw)
    return ImportDataset(**base)


# --- migration ----------------------------------------------------------------------------------------------------

def test_head_has_all_workspace_tables(mini_db):
    assert counts(mini_db['url'], WORKSPACE) == dict.fromkeys(WORKSPACE, 0)
    with make_engine(mini_db['url']).connect() as c:
        assert c.execute(text('SELECT version_num FROM alembic_version')).scalar_one() == '0003'


@pytest.mark.sqlite_only
def test_workspace_migrations_keep_reference_rows_and_downgrade(dbcopy):
    """Up/down of 0002/0003 on a loaded database leaves every reference table with the same rows (WP2.5)."""
    before = counts(dbcopy, REFERENCE)
    command.downgrade(alembic_cfg(dbcopy), '0001')
    assert counts(dbcopy, REFERENCE) == before
    with make_engine(dbcopy).connect() as c:
        names = {r[0] for r in c.exec_driver_sql("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert not names & set(WORKSPACE)
    command.upgrade(alembic_cfg(dbcopy), 'head')
    assert counts(dbcopy, REFERENCE) == before
    with sqlite3.connect(dbcopy.removeprefix('sqlite:///')) as c:
        assert c.execute('PRAGMA foreign_key_check').fetchall() == []
        assert c.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'


def test_borderline_states_accepted_and_downgrade_refuses_to_drop_them(dbcopy):
    eng = make_engine(dbcopy)
    with eng.begin() as c:
        tile_id = c.execute(text("SELECT tile_id FROM tile WHERE domain_status = 'measured_in_domain' LIMIT 1")).scalar()
        assert tile_id is not None
        c.execute(text("UPDATE tile SET domain_status = 'measured_borderline' WHERE tile_id = :t"), {'t': tile_id})
    with pytest.raises(RuntimeError, match='borderline'):
        command.downgrade(alembic_cfg(dbcopy), '0002')
    with eng.begin() as c:
        c.execute(text("UPDATE tile SET domain_status = 'measured_in_domain' WHERE tile_id = :t"), {'t': tile_id})
    command.downgrade(alembic_cfg(dbcopy), '0002')
    with eng.begin() as c, pytest.raises(IntegrityError):
        c.execute(text("UPDATE tile SET domain_status = 'measured_borderline' WHERE tile_id = :t"), {'t': tile_id})
    eng.dispose()


@pytest.mark.sqlite_only
def test_rebuild_refuses_with_foreign_keys_on(dbcopy):
    """The SQLite rebuild of `tile` would cascade into measured_cell if foreign keys were on; the migration refuses."""
    eng = make_engine(dbcopy)                    # the application engine switches foreign keys on
    cfg = alembic_cfg(dbcopy)
    with eng.begin() as conn:
        cfg.attributes['connection'] = conn
        with pytest.raises(RuntimeError, match='foreign_keys'):
            command.downgrade(cfg, '0002')
    eng.dispose()
    assert counts(dbcopy, ('measured_cell',))['measured_cell'] > 0


DEV_BACKUP = APP / '.data/backup/dev-2026-11-16.db'


@pytest.mark.slow
@pytest.mark.sqlite_only
@pytest.mark.skipif(not DEV_BACKUP.exists(), reason='dev.db backup not present')
def test_migrations_on_copy_of_dev_db(tmp_path):
    """WP2 acceptance on the real 453 MB database: the backup is copied, never migrated in place."""
    path = tmp_path / 'dev.db'
    shutil.copy(DEV_BACKUP, path)
    path.chmod(0o600)
    url = f'sqlite:///{path}'
    before = counts(url, REFERENCE)
    command.upgrade(alembic_cfg(url), 'head')
    assert counts(url, REFERENCE) == before
    assert counts(url, WORKSPACE) == dict.fromkeys(WORKSPACE, 0)
    command.downgrade(alembic_cfg(url), '0001')
    assert counts(url, REFERENCE) == before


PG_URL = os.environ.get('DF_TEST_PG_URL')


@pytest.mark.skipif(not PG_URL, reason='DF_TEST_PG_URL not set (local PostgreSQL 16 integration)')
def test_migrations_on_postgres():
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext

    from db.models import Base
    cfg = alembic_cfg(PG_URL)
    command.downgrade(cfg, 'base')
    command.upgrade(cfg, 'head')
    eng = make_engine(PG_URL)
    with eng.connect() as conn:
        assert compare_metadata(MigrationContext.configure(conn), Base.metadata) == []
    command.downgrade(cfg, 'base')
    command.upgrade(cfg, 'head')
    eng.dispose()


# --- db-design §11 invariants -------------------------------------------------------------------------------------

def test_run_cannot_point_at_another_projects_job(ws):
    s, model_id, _ = ws
    a, b = add_project(s, 'a'), add_project(s, 'b')
    job = add_job(s, a, model_id)
    s.add(run_row(b, model_id, job_id=job, item_id='i1'))
    with pytest.raises(IntegrityError):
        s.flush()
    s.rollback()


def test_comparison_cannot_cross_projects(ws):
    s, model_id, _ = ws
    a, b = add_project(s, 'a'), add_project(s, 'b')
    run = run_row(a, model_id)
    ds = dataset_row(b)
    s.add_all([run, ds])
    s.flush()
    s.add(Comparison(comparison_id=uid(), project_id=a, analysis_id=run.analysis_id, dataset_id=ds.dataset_id,
                     aggregation='mean', compatible=True, matched=0, counts={}, rows=[], provenance={},
                     created_at=NOW))
    with pytest.raises(IntegrityError):
        s.flush()
    s.rollback()


def test_one_run_per_job_item(ws):
    s, model_id, _ = ws
    pid = add_project(s)
    job = add_job(s, pid, model_id)
    s.add(run_row(pid, model_id, job_id=job, item_id='i1'))
    s.flush()
    s.add(run_row(pid, model_id, job_id=job, item_id='i1'))
    with pytest.raises(IntegrityError):
        s.flush()
    s.rollback()


@pytest.mark.parametrize('fields', [
    {'state': 'running'},                                            # a running item must hold a lease
    {'tile_index': 2, 'start_pos': 23, 'end_pos': 50},               # start must be (n-1)*23+1 = 24
    {'domain_status': 'borderline'},                                 # only the two qualified borderline states exist
])
def test_job_item_constraints(ws, fields):
    s, model_id, _ = ws
    pid = add_project(s)
    jid = add_job(s, pid, model_id)
    s.add(JobItem(job_id=jid, item_id='i2', ordinal=2, input_id='x', updated_at=NOW, **fields))
    with pytest.raises(IntegrityError):
        s.flush()
    s.rollback()


@pytest.mark.parametrize('value, reason', [(None, None), (1.5, 'below detection')])
def test_observation_needs_value_or_reason_not_both(ws, value, reason):
    s, _, _ = ws
    pid = add_project(s)
    ds = dataset_row(pid)
    s.add(ds)
    s.flush()
    s.add(ImportObservation(observation_id=uid(), dataset_id=ds.dataset_id, row_number=1, peptide_id='p', wt_sequence=SEQ,
                            position=1, wt_aa='M', mut_aa='A', replicate_id='r1', observed_value=value,
                            missing_reason=reason))
    with pytest.raises(IntegrityError):
        s.flush()
    s.rollback()


def test_new_file_is_new_revision_not_overwrite(ws):
    s, _, _ = ws
    pid = add_project(s)
    s.add(dataset_row(pid, revision=1))
    s.commit()
    s.add(dataset_row(pid, revision=1))
    with pytest.raises(IntegrityError):
        s.flush()
    s.rollback()
    s.add(dataset_row(pid, revision=2))
    s.flush()


def test_project_delete_cascades_owned_rows_only(ws):
    """HIST-03 (database part): deleting a project removes its rows and nothing else."""
    s, model_id, url = ws
    keep, gone = add_project(s, 'keep'), add_project(s, 'gone')
    for pid in (keep, gone):
        job = add_job(s, pid, model_id)
        run = run_row(pid, model_id, job_id=job, item_id='i1')
        ds = dataset_row(pid, state='committed', committed_at=NOW, expires_at=None)
        s.add_all([run, ds])
        s.flush()
        s.add(AnalysisCell(analysis_id=run.analysis_id, position=1, mut_aa='A', wt_aa='M', score_raw=0.1,
                           prob_calibrated=0.2, rank_in_tile=1, top10=True))
        s.add(ImportObservation(observation_id=uid(), dataset_id=ds.dataset_id, row_number=1, peptide_id='p',
                                wt_sequence=SEQ, position=1, wt_aa='M', mut_aa='A', replicate_id='r1',
                                observed_value=0.5))
        s.add(Comparison(comparison_id=uid(), project_id=pid, analysis_id=run.analysis_id, dataset_id=ds.dataset_id,
                         replicate_id='r1', compatible=True, matched=1, counts={}, rows=[], provenance={},
                         created_at=NOW))
    s.commit()
    reference = counts(url, REFERENCE)
    s.delete(s.get(Project, gone))
    s.commit()
    after = counts(url, WORKSPACE)
    assert after == {'project': 1, 'analysis_job': 1, 'job_item': 1, 'analysis_run': 1, 'analysis_cell': 1,
                     'import_dataset': 1, 'import_observation': 1, 'comparison': 1}
    assert counts(url, REFERENCE) == reference
    assert s.get(Project, keep) is not None


# --- workspace paths (SEC-02, NFR-08) -----------------------------------------------------------------------------

@pytest.mark.parametrize('bad', ['../etc', '..', '', 'A' * 36, '{12345678-1234-1234-1234-123456789abc}',
                                 '12345678-1234-1234-1234-123456789ABC', '/tmp/x', 'urn:uuid:12345678-1234-1234-1234-123456789abc'])
def test_project_dir_rejects_anything_but_canonical_uuid(tmp_path, bad):
    with pytest.raises(WorkspacePathError):
        project_dir(tmp_path, bad)


def test_paths_are_generated_and_stay_inside_root(tmp_path):
    pid, did = uid(), uid()
    rel = dataset_relpath(pid, did, '.tsv')
    assert rel == f'{pid}/{did}.tsv'
    assert resolve_stored(tmp_path, rel) == (tmp_path / rel).resolve()
    with pytest.raises(WorkspacePathError):
        dataset_relpath(pid, did, '.xlsx')
    for stored in (f'{pid}/../{did}.csv', f'/{pid}/{did}.csv', f'{pid}/{did}.csv/..', 'evil.csv'):
        with pytest.raises(WorkspacePathError):
            resolve_stored(tmp_path, stored)


def test_symlink_out_of_root_is_refused(tmp_path):
    root, outside = tmp_path / 'ws', tmp_path / 'outside'
    root.mkdir()
    outside.mkdir()
    pid = uid()
    (root / pid).symlink_to(outside, target_is_directory=True)
    with pytest.raises(WorkspacePathError):
        project_dir(root, pid)


def test_remove_project_dir_reports_failure_for_retry(tmp_path, monkeypatch):
    pid = uid()
    d = tmp_path / pid
    d.mkdir()
    (d / 'x.csv').write_text('a')
    assert remove_project_dir(tmp_path, uid()) is None          # never created: nothing to do

    def boom(*_a, **_k):
        raise PermissionError(13, 'Permission denied')
    monkeypatch.setattr('api.workspace.shutil.rmtree', boom)
    assert 'PermissionError' in remove_project_dir(tmp_path, pid)
    assert d.exists()
    monkeypatch.undo()
    assert remove_project_dir(tmp_path, pid) is None
    assert not d.exists()
