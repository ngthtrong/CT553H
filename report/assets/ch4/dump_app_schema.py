"""Dump the application's physical data model from the code, not from the design notes.

Run with the application's own environment, from the repository root:

    system/app/.venv/bin/python -I report/assets/ch4/dump_app_schema.py

It imports the SQLAlchemy metadata of the service, cross-checks the table names
against the Alembic migrations, and writes app-schema.json next to this file.
build_app_assets.py then turns that snapshot into thesis tables, so the report
build itself does not need the application's dependencies.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data/README.md').exists())
APP = TOPIC / 'system/app'
sys.path.insert(0, str(APP / 'backend'))

from db.models import Base  # noqa: E402  (import needs the path above)

MIGRATIONS = sorted((APP / 'backend/migrations/versions').glob('[0-9]*.py'))
created, migration_files = {}, []
for path in MIGRATIONS:
    text = path.read_text(encoding='utf-8')
    migration_files.append({
        'file': path.name,
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'creates': sorted(set(re.findall(r"op\.create_table\(\s*'([a-z_]+)'", text))),
        'indexes': sorted(set(re.findall(r"op\.create_index\(\s*'([a-z_]+)'", text))),
    })
    for name in re.findall(r"op\.create_table\(\s*'([a-z_]+)'", text):
        created[name] = path.name

tables = []
for table in Base.metadata.sorted_tables:
    tables.append({
        'name': table.name,
        'columns': len(table.columns),
        'primary_key': [c.name for c in table.primary_key.columns],
        'foreign_keys': [{
            'column': sorted(c.name for c in fk.columns),
            'target': fk.elements[0].target_fullname,
            'ondelete': fk.ondelete,
        } for fk in table.foreign_key_constraints],
        'unique': [sorted(c.name for c in u.columns) for u in table.constraints
                   if u.__class__.__name__ == 'UniqueConstraint'],
        'checks': sum(1 for c in table.constraints if c.__class__.__name__ == 'CheckConstraint'),
        'indexes': [{'name': i.name, 'columns': [c.name for c in i.columns], 'unique': bool(i.unique)}
                    for i in table.indexes],
        'created_in': created.get(table.name),
    })

missing = [t['name'] for t in tables if t['created_in'] is None]
extra = sorted(set(created) - {t['name'] for t in tables})
if missing or extra:
    raise SystemExit(f'ORM and migrations disagree; orm-only={missing} migration-only={extra}')

snapshot = {
    'schema_version': 1,
    'generated_by': 'report/assets/ch4/dump_app_schema.py',
    'orm_source': 'system/app/backend/db/models.py',
    'orm_sha256': hashlib.sha256((APP / 'backend/db/models.py').read_bytes()).hexdigest(),
    'migrations': migration_files,
    'table_count': len(tables),
    'tables': tables,
}
(HERE / 'app-schema.json').write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8')
print(f"wrote app-schema.json: {len(tables)} tables, {len(migration_files)} migrations")
