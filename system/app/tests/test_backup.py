"""Backup and restore (plan-system 4.1): OPS-01…03 on the SQLite target (the Docker round trip is recorded in
tests/results/backup-roundtrip.json)."""
from __future__ import annotations

import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest

from tests.conftest import mk_client

APP = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ops_backup', APP / 'ops/backup.py')
ops = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ops)

pytestmark = pytest.mark.sqlite_only
SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'


@pytest.fixture()
def installed(mini, dbcopy, tmp_path):
    """A small installation with a project, a saved analysis, a job and an imported file."""
    ws = tmp_path / 'ws'
    c, app = mk_client(mini, dbcopy, workspace_dir=ws)
    pid = c.post('/v1/projects', json={'name': 'backup me'}).json()['project_id']
    assert c.post(f'/v1/projects/{pid}/analyses', json={'request': {'sequence': SEQ}}).status_code == 201
    c.post(f'/v1/projects/{pid}/jobs', json={'mode': 'peptides', 'peptides': [{'input_id': 'a', 'sequence': SEQ}]})
    csv = f'peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id\np,{SEQ},1,D,A,0.5,r1\n'
    meta = {'name': 'obs', 'assay': 'GPS', 'endpoint': 'delta_psi', 'units': 'PSI', 'source': 'lab',
            'reference_description': 'ref', 'compatibility': 'zhang_gps_dpsi'}
    r = c.post(f'/v1/projects/{pid}/datasets', data={'metadata': json.dumps(meta)},
               files={'file': ('obs.csv', csv.encode(), 'text/csv')})
    assert r.status_code in (200, 201), r.text
    app.state.core.engine.dispose()
    db = Path(dbcopy.removeprefix('sqlite:///'))
    return ops.SqliteTarget(db, ws), pid


def files_of(ws: Path) -> dict[str, str]:
    return {str(p.relative_to(ws)): ops.sha256(p) for p in sorted(ws.rglob('*')) if p.is_file()}


def test_ops01_backup_delete_restore_gives_the_same_data(installed, tmp_path):
    target, pid = installed
    before_state = ops.state_of(target)
    before_files = files_of(target.workspace)
    assert before_state['counts']['project'] >= 1 and before_files                 # the import file exists
    out = ops.backup(target, tmp_path / 'b1')
    m = json.loads((out / 'manifest.json').read_text())
    assert m['schema_revision'] == ops.migration_head() == '0008'
    assert m['counts'] == before_state['counts'] and m['consistent'] is True
    assert set(m['files']) == {'database.sqlite', 'workspace.tar.gz'}
    assert any(x['weights_sha256'] for x in m['models'])
    assert (out.stat().st_mode & 0o777) == 0o700
    # lose everything
    target.db.unlink()
    import shutil
    shutil.rmtree(target.workspace)
    lines: list[str] = []
    ops.restore(target, out, yes=True, out=lines.append)
    assert ops.state_of(target) == before_state
    assert files_of(target.workspace) == before_files
    with sqlite3.connect(target.db) as con:
        assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert con.execute('SELECT count(*) FROM project WHERE project_id = ?', (pid,)).fetchone()[0] == 1
    assert any('OVERWRITE' in x for x in lines)


def test_ops02_damaged_or_foreign_backups_are_refused_before_any_change(installed, tmp_path):
    target, _ = installed
    out = ops.backup(target, tmp_path / 'b2')
    before = ops.state_of(target)
    # a byte changed in the dump
    db = out / 'database.sqlite'
    data = bytearray(db.read_bytes())
    data[-1] ^= 1
    db.write_bytes(bytes(data))
    with pytest.raises(ops.BackupError, match='SHA-256'):
        ops.restore(target, out, yes=True, out=lambda *_: None)
    # manifest edited / missing / other schema
    out2 = ops.backup(target, tmp_path / 'b3')
    mf = json.loads((out2 / 'manifest.json').read_text())
    (out2 / 'manifest.json').write_text(json.dumps({**mf, 'schema_revision': '0004'}))
    with pytest.raises(ops.BackupError, match='schema revision 0004'):
        ops.restore(target, out2, yes=True, out=lambda *_: None)
    (out2 / 'manifest.json').write_text('{not json')
    with pytest.raises(ops.BackupError, match='not valid JSON'):
        ops.verify(out2)
    (out2 / 'manifest.json').unlink()
    with pytest.raises(ops.BackupError, match='manifest.json is missing'):
        ops.verify(out2)
    assert ops.state_of(target) == before


def test_ops03_nothing_is_overwritten_without_confirmation(installed, tmp_path):
    target, pid = installed
    out = ops.backup(target, tmp_path / 'b4')
    # change the installation after the backup
    with sqlite3.connect(target.db) as con:
        con.execute("UPDATE project SET name = 'changed later' WHERE project_id = ?", (pid,))
    with pytest.raises(ops.BackupError, match='not confirmed'):
        ops.restore(target, out, ask=lambda _prompt: 'no', out=lambda *_: None)
    with sqlite3.connect(target.db) as con:
        assert con.execute('SELECT name FROM project WHERE project_id = ?', (pid,)).fetchone()[0] == 'changed later'
    ops.restore(target, out, ask=lambda _prompt: 'restore', out=lambda *_: None)
    with sqlite3.connect(target.db) as con:
        assert con.execute('SELECT name FROM project WHERE project_id = ?', (pid,)).fetchone()[0] == 'backup me'


def test_backup_refuses_a_non_empty_output_directory(installed, tmp_path):
    target, _ = installed
    d = tmp_path / 'full'
    d.mkdir()
    (d / 'x').write_text('x')
    with pytest.raises(ops.BackupError, match='not empty'):
        ops.backup(target, d)
    assert ops.main(['restore', str(tmp_path / 'none'), '--sqlite', str(target.db), '--yes']) == 2
