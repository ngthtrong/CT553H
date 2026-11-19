"""One-command backup and restore of a local Degron Footprint installation (plan-system 4.1).

    python ops/backup.py backup  [--out DIR]                      # Docker stack (default), project degron-footprint
    python ops/backup.py restore DIR [--yes]
    python ops/backup.py backup  --sqlite .data/dev.db --workspace .data/workspace      # host development install

A backup is a directory with the database (PostgreSQL custom-format dump, or a consistent SQLite copy made with the
SQLite backup API), the project files (`workspace.tar.gz`) and `manifest.json`: SHA-256 and size of every file, the
schema revision (Alembic), the registered models with their weights hashes, row counts and the creation time.
Model weights and the reference data are **not** included: they are rebuilt by the ETL.

Restore checks the manifest first (every hash), refuses a backup whose schema revision differs from the code's
migration head, prints what will be overwritten and asks for confirmation (typing "restore"; --yes skips the question,
and without a terminal the restore is refused unless --yes is given). Nothing is changed before all checks pass.

A backup contains user sequences, saved analyses and imported observations: keep it like the installation itself
(INSTALL.md §6). Standard library only; the Docker mode calls the `docker` CLI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

APP = Path(__file__).resolve().parents[1]
FORMAT_VERSION = 1
COUNTED = ('project', 'analysis_run', 'analysis_cell', 'analysis_job', 'job_item', 'import_dataset',
           'import_observation', 'comparison')
HELPER_IMAGE = 'postgres:16-alpine'          # already pulled for the db service; has sh and tar
CONFIRM_WORD = 'restore'


class BackupError(Exception):
    pass


# ---------------------------------------------------------------------------------------------------------- helpers
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def migration_head(versions: Path = APP / 'backend/migrations/versions') -> str:
    """The revision no other revision builds on (single linear history)."""
    revs, downs = set(), set()
    for f in versions.glob('*.py'):
        text = f.read_text(encoding='utf-8')
        r = re.search(r"^revision\s*=\s*'([^']+)'", text, re.M)
        d = re.search(r"^down_revision\s*=\s*'([^']+)'", text, re.M)
        if r:
            revs.add(r.group(1))
        if d:
            downs.add(d.group(1))
    heads = revs - downs
    if len(heads) != 1:
        raise BackupError(f'cannot determine a single migration head: {sorted(heads)}')
    return heads.pop()


def run(cmd: list[str], *, stdin=None, stdout=None, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdin=stdin, stdout=stdout if stdout is not None else subprocess.PIPE,
                          stderr=subprocess.PIPE, check=check)


# ---------------------------------------------------------------------------------------------------------- targets
class SqliteTarget:
    kind = 'sqlite'

    def __init__(self, db: Path, workspace: Path):
        self.db, self.workspace = db, workspace

    def describe(self) -> str:
        return f'SQLite database {self.db} and project files in {self.workspace}'

    def query(self, sql: str) -> list[tuple]:
        con = sqlite3.connect(f'file:{self.db}?mode=ro', uri=True)
        try:
            return con.execute(sql).fetchall()
        finally:
            con.close()

    def reachable(self) -> bool:
        return self.db.is_file()

    def dump_db(self, out: Path) -> Path:
        dest = out / 'database.sqlite'
        src = sqlite3.connect(f'file:{self.db}?mode=ro', uri=True)
        dst = sqlite3.connect(dest)
        try:
            src.backup(dst)                                  # consistent snapshot even while the app writes
        finally:
            dst.close()
            src.close()
        return dest

    def dump_workspace(self, out: Path) -> Path:
        dest = out / 'workspace.tar.gz'
        with tarfile.open(dest, 'w:gz') as tar:
            if self.workspace.is_dir():
                for p in sorted(self.workspace.rglob('*')):
                    tar.add(p, arcname=str(p.relative_to(self.workspace)), recursive=False)
        return dest

    def restore(self, backup: Path) -> None:
        self.db.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.db.with_suffix(self.db.suffix + '.restore-tmp')
        shutil.copyfile(backup / 'database.sqlite', tmp)
        os.replace(tmp, self.db)
        for side in ('-wal', '-shm'):
            Path(str(self.db) + side).unlink(missing_ok=True)
        if self.workspace.exists():
            shutil.rmtree(self.workspace)
        self.workspace.mkdir(parents=True)
        with tarfile.open(backup / 'workspace.tar.gz', 'r:gz') as tar:
            tar.extractall(self.workspace, filter='data')    # no absolute paths, links outside or device files


class DockerTarget:
    kind = 'postgresql'

    def __init__(self, project: str, compose_dir: Path = APP, services: bool = True):
        self.project, self.compose_dir, self.services = project, compose_dir, services
        self.volume = f'{project}_workspace'

    def _compose(self, *args: str) -> list[str]:
        return ['docker', 'compose', '--project-directory', str(self.compose_dir), '-p', self.project, *args]

    def describe(self) -> str:
        return (f'PostgreSQL database "degron" of Docker project "{self.project}" and its project-file volume '
                f'"{self.volume}"')

    def _psql(self, sql: str) -> str:
        return run(self._compose('exec', '-T', 'db', 'psql', '-U', 'degron', '-d', 'degron', '-At', '-F', '\t',
                                 '-c', sql)).stdout.decode()

    def query(self, sql: str) -> list[tuple]:
        return [tuple(line.split('\t')) for line in self._psql(sql).splitlines() if line]

    def reachable(self) -> bool:
        return run(self._compose('exec', '-T', 'db', 'pg_isready', '-U', 'degron', '-d', 'degron'),
                   check=False).returncode == 0

    def dump_db(self, out: Path) -> Path:
        dest = out / 'database.dump'
        with open(dest, 'wb') as fh:
            run(self._compose('exec', '-T', 'db', 'pg_dump', '-U', 'degron', '-d', 'degron', '-Fc'), stdout=fh)
        return dest

    def dump_workspace(self, out: Path) -> Path:
        dest = out / 'workspace.tar.gz'
        with open(dest, 'wb') as fh:
            run(['docker', 'run', '--rm', '-v', f'{self.volume}:/w:ro', HELPER_IMAGE, 'tar', 'czf', '-', '-C', '/w',
                 '.'], stdout=fh)
        return dest

    def restore(self, backup: Path) -> None:
        if self.services:
            run(self._compose('stop', 'worker', 'api'), check=False)      # no writes while the data are replaced
        try:
            with open(backup / 'database.dump', 'rb') as fh:
                run(self._compose('exec', '-T', 'db', 'pg_restore', '-U', 'degron', '-d', 'degron', '--clean',
                                  '--if-exists', '--no-owner', '--single-transaction'), stdin=fh)
            with open(backup / 'workspace.tar.gz', 'rb') as fh:
                run(['docker', 'run', '--rm', '-i', '-v', f'{self.volume}:/w', HELPER_IMAGE, 'sh', '-c',
                     'find /w -mindepth 1 -delete && tar xzf - -C /w'], stdin=fh)
        finally:
            if self.services:
                run(self._compose('start', 'api', 'worker'), check=False)


# ---------------------------------------------------------------------------------------------------------- state
def state_of(target) -> dict[str, Any]:
    rev = target.query('SELECT version_num FROM alembic_version')
    counts = {t: int(target.query(f'SELECT count(*) FROM {t}')[0][0]) for t in COUNTED}
    models = [{'model_id': r[0], 'role': r[1], 'kind': r[2], 'weights_sha256': r[3],
               'is_default': str(r[4]).lower() in ('1', 't', 'true')}
              for r in target.query('SELECT model_id, role, kind, weights_sha256, is_default FROM model_version '
                                    'ORDER BY model_id')]
    return {'schema_revision': rev[0][0] if rev else None, 'counts': counts, 'models': models}


# ---------------------------------------------------------------------------------------------------------- backup
def backup(target, out: Path | None = None) -> Path:
    if not target.reachable():
        raise BackupError(f'the database is not reachable: {target.describe()}')
    stamp = datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')
    out = out or APP / '.data/backups' / f'backup-{stamp}'
    if out.exists() and any(out.iterdir()):
        raise BackupError(f'{out} exists and is not empty; choose another --out')
    out.mkdir(parents=True, exist_ok=True)
    os.chmod(out, 0o700)
    t0 = time.perf_counter()
    before = state_of(target)
    files = [target.dump_db(out), target.dump_workspace(out)]
    after = state_of(target)
    manifest = {
        'format_version': FORMAT_VERSION, 'created_at': datetime.now(UTC).isoformat(timespec='seconds'),
        'backend': target.kind, 'source': target.describe(), 'schema_revision': after['schema_revision'],
        'models': after['models'], 'counts': after['counts'],
        'consistent': before['counts'] == after['counts'],
        'files': {f.name: {'bytes': f.stat().st_size, 'sha256': sha256(f)} for f in files},
        'not_included': ['model weights (rebuilt by the ETL)', 'reference data are inside the database dump'],
        'privacy': 'Contains user sequences, saved analyses and imported observations; store it like the installation.',
        'seconds': round(time.perf_counter() - t0, 2),
    }
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    for f in out.iterdir():
        os.chmod(f, 0o600)
    return out


# ---------------------------------------------------------------------------------------------------------- restore
def verify(backup_dir: Path, head: str | None = None) -> dict:
    mf = backup_dir / 'manifest.json'
    if not mf.is_file():
        raise BackupError('manifest.json is missing: not a backup directory')
    try:
        manifest = json.loads(mf.read_text(encoding='utf-8'))
    except ValueError as exc:
        raise BackupError(f'manifest.json is not valid JSON: {exc}') from exc
    if manifest.get('format_version') != FORMAT_VERSION:
        raise BackupError(f'unknown backup format {manifest.get("format_version")!r}')
    files = manifest.get('files') or {}
    expected = {'database.dump' if manifest.get('backend') == 'postgresql' else 'database.sqlite', 'workspace.tar.gz'}
    if set(files) != expected:
        raise BackupError(f'manifest lists {sorted(files)}, expected {sorted(expected)}')
    for name, meta in files.items():
        f = backup_dir / name
        if not f.is_file():
            raise BackupError(f'{name} is missing')
        if f.stat().st_size != meta.get('bytes') or sha256(f) != meta.get('sha256'):
            raise BackupError(f'{name} does not match its SHA-256 in the manifest (damaged or edited)')
    head = head or migration_head()
    if manifest.get('schema_revision') != head:
        raise BackupError(f'the backup has schema revision {manifest.get("schema_revision")}, this code expects '
                          f'{head}; restore it with the code version that made it, then upgrade')
    return manifest


def restore(target, backup_dir: Path, *, yes: bool = False, ask=input, out=print, head: str | None = None) -> dict:
    manifest = verify(backup_dir, head)
    if manifest['backend'] != target.kind:
        raise BackupError(f'the backup is for {manifest["backend"]}, the target is {target.kind}')
    try:
        current = state_of(target) if target.reachable() else None
    except (subprocess.CalledProcessError, sqlite3.Error):
        current = None                                       # empty database (no schema yet): nothing to show
    out(f'Backup {backup_dir} of {manifest["created_at"]} (schema {manifest["schema_revision"]}).')
    out(f'This will OVERWRITE: {target.describe()}.')
    out('  now:    ' + (', '.join(f'{k}={v}' for k, v in current['counts'].items()) if current
                        else 'empty or unreadable database'))
    out('  backup: ' + ', '.join(f'{k}={v}' for k, v in manifest['counts'].items()))
    if not yes:
        if not sys.stdin.isatty() and ask is input:
            raise BackupError('confirmation needed: run in a terminal, or pass --yes')
        if ask(f'Type "{CONFIRM_WORD}" to continue: ').strip() != CONFIRM_WORD:
            raise BackupError('not confirmed; nothing was changed')
    t0 = time.perf_counter()
    target.restore(backup_dir)
    restored = state_of(target)
    if restored['counts'] != manifest['counts'] or restored['schema_revision'] != manifest['schema_revision']:
        raise BackupError(f'restored state differs from the manifest: {restored["counts"]}')
    out(f'Restored in {time.perf_counter() - t0:.1f} s; counts match the manifest.')
    return {'seconds': round(time.perf_counter() - t0, 2), 'counts': restored['counts']}


# ---------------------------------------------------------------------------------------------------------- CLI
def make_target(a) -> SqliteTarget | DockerTarget:
    if a.sqlite:
        return SqliteTarget(Path(a.sqlite), Path(a.workspace or APP / '.data/workspace'))
    return DockerTarget(a.project, services=not a.no_services)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('backup', 'restore'):
        p = sub.add_parser(name)
        p.add_argument('--project', default='degron-footprint', help='Docker Compose project name')
        p.add_argument('--sqlite', help='SQLite database file instead of the Docker stack')
        p.add_argument('--workspace', help='project-file directory for --sqlite (default .data/workspace)')
        p.add_argument('--no-services', action='store_true', help='do not stop/start api and worker (restore)')
        if name == 'backup':
            p.add_argument('--out', type=Path)
        else:
            p.add_argument('backup', type=Path)
            p.add_argument('--yes', action='store_true', help='do not ask for confirmation')
    a = ap.parse_args(argv)
    try:
        target = make_target(a)
        if a.cmd == 'backup':
            d = backup(target, a.out)
            m = json.loads((d / 'manifest.json').read_text())
            size = sum(v['bytes'] for v in m['files'].values())
            print(f'Backup written to {d} ({size / 1e6:.1f} MB, {m["seconds"]} s, schema {m["schema_revision"]}).')
            print('It contains sequences and imported data: keep it private.')
        else:
            restore(target, a.backup, yes=a.yes)
    except (BackupError, subprocess.CalledProcessError, OSError) as exc:
        detail = ''
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            detail = exc.stderr.decode(errors='replace').strip()[-400:]
        print(f'error: {exc}' + (f'\n{detail}' if detail else ''), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


__all__ = ['backup', 'restore', 'verify', 'migration_head', 'SqliteTarget', 'DockerTarget', 'BackupError']
