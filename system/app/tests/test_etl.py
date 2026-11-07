"""ETL group of test-plan.md §6.5 on the miniature data tree."""
from __future__ import annotations

import shutil

import pytest
import yaml
from sqlalchemy import func, select

from db.models import ClinvarVariant, DataSource, EtlInput, EtlRun, MeasuredCell, ModelVersion, Protein, Tile
from db.session import make_engine
from etl import load as etl

from . import minidata
from .conftest import APP


def migrate(url):
    from alembic import command
    from alembic.config import Config
    cfg = Config(str(APP / 'backend/alembic.ini'))
    cfg.set_main_option('sqlalchemy.url', url)
    command.upgrade(cfg, 'head')


def fresh_tree(tmp_path, **kw):
    mini = minidata.build(tmp_path / 'tree', **kw)
    url = f"sqlite:///{tmp_path / 'e.db'}"
    migrate(url)
    return mini, url


def run(mini, url, scope='all', **kw):
    return etl.run(url, mini['topic'], mini['sources'], mini['params'], scope, mini['model_dir'], **kw)


def test_first_load_counts(mini_db):
    r = mini_db['report']
    assert r['tables']['protein']['inserted'] == 3
    assert r['tables']['tile']['inserted'] == 5 + 4 + 0           # tiles of P12345, P22222, none for O00001
    assert r['training_peptides'] == 1 and r['training_tile_mismatches'] == 0
    assert r['training_cells'] == r['tables']['measured_cell']['inserted']
    assert r['tiles_per_domain_status'] == {'measured_in_domain': 2, 'measured_out_of_domain': 2,
                                            'measured_unreliable': 3, 'unknown': 1}
    assert r['screen_rows'] == 10 and r['screen_rows_unmatched'] == 2
    assert r['screen_rows_unmatched_reasons'] == {'tile_index_beyond_last_window': 1, 'beyond_last_window_by_1': 1,
                                                  'accession_not_in_snapshot': 1}
    assert r['screen_matched_not_scorable'] == 1


def test_domain_statuses_in_database(mini_db):
    eng = make_engine(mini_db['url'])
    with eng.connect() as c:
        rows = {(t.uniprot_acc, t.tile_index): t for t in c.execute(select(Tile))}
    assert rows[('P12345', 1)].domain_status == 'measured_in_domain'
    assert rows[('P12345', 2)].domain_status == 'measured_out_of_domain'
    assert rows[('P12345', 3)].domain_status == 'measured_unreliable'
    assert rows[('P12345', 4)].domain_status == 'measured_unreliable' and rows[('P12345', 4)].psi_wt_measured is None
    assert rows[('P12345', 5)].domain_status == 'unknown' and rows[('P12345', 5)].screen_peptide_id is None
    assert rows[('P22222', 1)].domain_status == 'measured_in_domain'          # PSI 4.0, reads 10: boundary is inside
    assert rows[('P22222', 2)].domain_status == 'measured_out_of_domain'
    assert rows[('P22222', 3)].domain_status == 'measured_unreliable'
    assert rows[('P22222', 4)].scorable is False and rows[('P22222', 4)].domain_status == 'unknown'


def test_etl01_changed_byte_aborts_and_is_recorded(tmp_path):
    mini, url = fresh_tree(tmp_path)
    p = mini['files']['screen']
    p.write_bytes(p.read_bytes() + b' ')
    with pytest.raises(etl.HashMismatch):
        run(mini, url)
    eng = make_engine(url)
    with eng.connect() as c:
        bad = c.execute(select(EtlInput).where(EtlInput.sha256_expected != EtlInput.sha256_actual)).fetchall()
        assert len(bad) == 1 and bad[0].file_path == 'interim/screen.tsv'
        assert c.execute(select(func.count()).select_from(Protein)).scalar() == 0     # nothing was loaded
        assert c.execute(select(EtlRun.status)).scalar() == 'failed'


def test_etl02_second_run_changes_nothing(tmp_path):
    mini, url = fresh_tree(tmp_path)
    first = run(mini, url)
    assert first['reference_rows_changed'] > 0
    second = run(mini, url)
    assert second['reference_rows_changed'] == 0
    for t, c in second['tables'].items():
        assert c.get('inserted', 0) == 0 and c.get('updated', 0) == 0 and c.get('deleted', 0) == 0, t
    eng = make_engine(url)
    with eng.connect() as c:
        assert c.execute(select(func.count()).select_from(Tile)).scalar() == 9


def test_etl02_changed_input_updates_in_place(tmp_path):
    mini, url = fresh_tree(tmp_path)
    run(mini, url)
    # new screen: PSI of P12345 tile 1 rises above 4; the pinned hash in sources.yaml is refreshed accordingly
    scr = mini['files']['screen']
    scr.write_text(scr.read_text().replace('P12345_GENE1_1\t50.0\t2.0', 'P12345_GENE1_1\t50.0\t4.5'))
    doc = yaml.safe_load(mini['sources'].read_text())
    for s in doc['sources']:
        for f in s.get('files', []):
            if f['role'] == 'screen_psi':
                f['sha256'] = minidata.sha256(scr)
    mini['sources'].write_text(yaml.safe_dump(doc, sort_keys=False))
    r = run(mini, url)
    assert r['tables']['tile'].get('updated') == 1
    with make_engine(url).connect() as c:
        st = c.execute(select(Tile.domain_status).where(Tile.uniprot_acc == 'P12345', Tile.tile_index == 1)).scalar()
    assert st == 'measured_out_of_domain'


def test_etl03_blocked_source_cannot_be_loaded(tmp_path):
    mini, url = fresh_tree(tmp_path)
    doc = yaml.safe_load(mini['sources'].read_text())
    for s in doc['sources']:
        if s['source_id'] == 'zhang2023-geo-gse240610':
            s.update(redistribution_ok=False, license_class='internal_only')
    mini['sources'].write_text(yaml.safe_dump(doc, sort_keys=False))
    with pytest.raises(etl.LicenceBlock):
        run(mini, url)
    with make_engine(url).connect() as c:
        for model in (Protein, Tile, MeasuredCell, ClinvarVariant):
            assert c.execute(select(func.count()).select_from(model)).scalar() == 0


def test_etl03_blocked_source_in_register_but_never_loaded(mini_db):
    with make_engine(mini_db['url']).connect() as c:
        k = c.execute(select(DataSource).where(DataSource.source_id == 'koren2018-nihms967427')).one()
        assert k.redistribution_ok is False and k.license_class == 'internal_only'
        ids = {r[0] for r in c.execute(select(Tile.source_id).distinct())}
        ids |= {r[0] for r in c.execute(select(MeasuredCell.source_id).distinct())}
        ids |= {r[0] for r in c.execute(select(ClinvarVariant.source_id).distinct())}
    assert 'koren2018-nihms967427' not in ids


def test_database_refuses_servable_internal_only_source(mini_db):
    """The CHECK of data_source: a source that may not be redistributed cannot carry an open class."""
    from sqlalchemy.exc import IntegrityError
    with make_engine(mini_db['url']).begin() as c, pytest.raises(IntegrityError):
        c.execute(DataSource.__table__.insert().values(
            source_id='bad', name='x', version='x', citation='x', license_name='x', license_class='open',
            redistribution_ok=False, attribution_text='x'))


def test_etl04_training_cells_checked_against_uniprot_tile(tmp_path):
    mini, url = fresh_tree(tmp_path)
    import numpy as np
    z = dict(np.load(mini['files']['sat']))
    z['X'] = z['X'].copy()
    z['X'][5, 40:60] += 0.01                                 # a tile whose composition disagrees
    np.savez(mini['files']['sat'], **z)
    doc = yaml.safe_load(mini['sources'].read_text())
    for s in doc['sources']:
        for f in s.get('files', []):
            if f['role'] == 'sat_labels':
                f['sha256'] = minidata.sha256(mini['files']['sat'])
    mini['sources'].write_text(yaml.safe_dump(doc, sort_keys=False))
    with pytest.raises(etl.EtlError, match='ETL-04'):
        run(mini, url)


def test_etl05_report_is_stored_and_complete(mini_db):
    with make_engine(mini_db['url']).connect() as c:
        rep = c.execute(select(EtlRun.report).order_by(EtlRun.etl_run_id.desc())).scalars().first()
    for key in ('tables', 'tiles_per_domain_status', 'screen_rows_unmatched', 'training_tile_mismatches',
                'clinvar', 'inputs_verified', 'seconds'):
        assert key in rep, key
    assert all(v >= 0 for v in rep['tiles_per_domain_status'].values())


def test_clinvar_rules(mini_db):
    r = mini_db['report']['clinvar']
    assert r['scope'] == 'all'
    assert r['reference_residue_mismatch'] == 1 and r['gene_not_in_snapshot'] == 1
    with make_engine(mini_db['url']).connect() as c:
        rows = {v.variation_id: v for v in c.execute(select(ClinvarVariant))}
    assert set(rows) == {101, 102, 103, 105, 106, 107, 108, 109, 111}      # deletion, duplicate and mismatch left out
    assert rows[101].clinsig == 'pathogenic' and rows[102].clinsig == 'vus' and rows[103].clinsig == 'likely_benign'
    assert rows[106].clinsig == 'conflicting' and rows[107].clinsig == 'pathogenic'
    assert rows[108].clinsig == 'benign' and rows[109].clinsig == 'other'
    assert rows[101].last_evaluated.isoformat() == '2024-03-02'
    assert all(v.clinvar_file_date.isoformat() == '2026-10-12' for v in rows.values())


def test_clinvar_scopes(tmp_path):
    mini, url = fresh_tree(tmp_path)
    r = run(mini, url, 'in-tiles')
    assert r['clinvar']['outside_all_tiles'] == 1                     # variant 111, past the last window
    with make_engine(url).connect() as c:
        assert 111 not in {v[0] for v in c.execute(select(ClinvarVariant.variation_id))}
    r = run(mini, url, 'degron-only')
    assert r['clinvar']['outside_in_domain_tiles'] >= 1
    with make_engine(url).connect() as c:
        ids = {v[0] for v in c.execute(select(ClinvarVariant.variation_id))}
        assert ids and ids <= {101, 102, 103, 105, 106, 107, 108, 109}     # stale rows of the wider scope were removed
    r = run(mini, url, 'none')
    assert 'clinvar' not in r


def test_model_registered_with_hash_and_card(mini_db):
    with make_engine(mini_db['url']).connect() as c:
        m = c.execute(select(ModelVersion)).one()
    assert m.status == 'frozen' and m.is_default and m.role == 'effect'
    assert len(m.weights_sha256) == 64 and 'Model card' in m.card_markdown
    assert m.metrics['source_file'].endswith('results.json') and m.trained_on_sources == ['zhang2023-mendeley-v2']
    assert (mini_db['report']['model_weights_sha256'] == m.weights_sha256)


def test_unknown_scope_rejected(tmp_path):
    mini, url = fresh_tree(tmp_path)
    with pytest.raises(etl.EtlError):
        run(mini, url, 'everything')
    shutil.rmtree(tmp_path / 'tree')


def test_migration_matches_models_and_downgrades(tmp_path):
    """Revision 0001 creates exactly the tables, constraints and indexes of db/models.py, and can be undone."""
    from alembic import command
    from alembic.autogenerate import compare_metadata
    from alembic.config import Config
    from alembic.migration import MigrationContext

    from db.models import Base
    url = f"sqlite:///{tmp_path / 'm.db'}"
    cfg = Config(str(APP / 'backend/alembic.ini'))
    cfg.set_main_option('sqlalchemy.url', url)
    command.upgrade(cfg, 'head')
    with make_engine(url).connect() as conn:
        assert compare_metadata(MigrationContext.configure(conn), Base.metadata) == []
    command.downgrade(cfg, 'base')
    with make_engine(url).connect() as conn:
        tables = {r[0] for r in conn.exec_driver_sql("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert tables <= {'alembic_version'}
