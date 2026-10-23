"""ETL: load the reference database from topics/degron-footprint/data (db-design.md §7).

    PYTHONPATH=backend python -m etl.load --db sqlite:///.data/dev.db [--clinvar-scope in-tiles]

Idempotent: every table is synchronised by natural key; a second run with unchanged inputs inserts and updates
nothing and says so in the report. It never modifies the data directory. It aborts, loading nothing from a file,
if the file's SHA-256 differs from sources.yaml or if its source may not be redistributed.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from collections.abc import Iterable, Iterator
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from sqlalchemy import Connection, Table, and_, bindparam, delete, select, text

HERE = Path(__file__).resolve().parent
APP_DIR = HERE.parent
sys.path.insert(0, str(APP_DIR / 'backend'))

from db.models import Base  # noqa: E402
from db.session import make_engine  # noqa: E402
from degron_footprint.features import feature_matrix  # noqa: E402
from degron_footprint.model import sha256_file  # noqa: E402
from degron_footprint.sources import BLOCKED_SOURCE_IDS  # noqa: E402
from degron_footprint.validation import is_scorable, n_tiles  # noqa: E402

T = Base.metadata.tables
BATCH = 10_000


class EtlError(Exception):
    """A rule of the ETL was broken; nothing from the offending file is loaded."""


class LicenceBlock(EtlError):
    pass


class HashMismatch(EtlError):
    pass


# ------------------------------------------------------------------ configuration
def find_topic() -> Path:
    for p in HERE.parents:
        if (p / 'data' / 'README.md').exists():
            return p
    raise EtlError('cannot find topics/degron-footprint (marker data/README.md)')


def load_config(sources_path: Path, params_path: Path) -> tuple[dict, dict]:
    sources = yaml.safe_load(sources_path.read_text(encoding='utf-8'))['sources']
    params = yaml.safe_load(params_path.read_text(encoding='utf-8'))
    return {s['source_id']: s for s in sources}, params


def file_of(sources: dict, role: str) -> tuple[dict, dict]:
    """(source, file entry) that provides `role`."""
    for s in sources.values():
        for f in s.get('files', []):
            if f['role'] == role:
                return s, f
    raise EtlError(f'no source provides role {role!r}')


def git_commit(repo: Path) -> str:
    try:
        head = subprocess.run(['git', '-C', str(repo), 'rev-parse', '--short', 'HEAD'], capture_output=True,
                              text=True, timeout=10).stdout.strip() or 'unknown'
        dirty = subprocess.run(['git', '-C', str(repo), 'status', '--porcelain', '--', str(APP_DIR)],
                               capture_output=True, text=True, timeout=10).stdout.strip()
        return head + ('-dirty' if dirty else '')
    except Exception:
        return 'unknown'


# ------------------------------------------------------------------ synchronisation
def _clean(v: Any) -> Any:
    if isinstance(v, float) and v != v:
        return None
    return v


def sync(conn: Connection, table: Table, keys: list[str], rows: list[dict], compare: list[str]) -> Counter:
    """Insert missing rows, update changed ones, leave equal ones. Returns Counter(inserted, updated, unchanged)."""
    out: Counter = Counter()
    if not rows:
        return out
    kcols = [table.c[k] for k in keys]
    ccols = [table.c[c] for c in compare]
    existing: dict[tuple, tuple] = {}
    if len(keys) == 1:
        keyvals = [r[keys[0]] for r in rows]
        for i in range(0, len(keyvals), 5000):
            chunk = keyvals[i:i + 5000]
            for rec in conn.execute(select(*kcols, *ccols).where(kcols[0].in_(chunk))):
                existing[tuple(rec[:1])] = tuple(rec[1:])
    else:
        # composite key: restrict by the first key column, then filter in Python
        first = sorted({r[keys[0]] for r in rows})
        for i in range(0, len(first), 5000):
            chunk = first[i:i + 5000]
            for rec in conn.execute(select(*kcols, *ccols).where(kcols[0].in_(chunk))):
                existing[tuple(rec[:len(keys)])] = tuple(rec[len(keys):])
    ins, upd = [], []
    for r in rows:
        k = tuple(r[c] for c in keys)
        new = tuple(_clean(r[c]) for c in compare)
        old = existing.get(k)
        if old is None:
            ins.append({**r, **{c: _clean(r[c]) for c in compare}})
        elif tuple(_normalise(o) for o in old) != tuple(_normalise(n) for n in new):
            upd.append(r)
        else:
            out['unchanged'] += 1
    for i in range(0, len(ins), BATCH):
        conn.execute(table.insert(), ins[i:i + BATCH])
    if upd:
        stmt = (table.update().where(and_(*[table.c[k] == bindparam('b_' + k) for k in keys]))
                .values({c: bindparam(c) for c in compare}))
        for i in range(0, len(upd), BATCH):
            conn.execute(stmt, [{**{c: _clean(r[c]) for c in compare}, **{'b_' + k: r[k] for k in keys}}
                                for r in upd[i:i + BATCH]])
    out['inserted'] += len(ins)
    out['updated'] += len(upd)
    return out


def _normalise(v: Any) -> Any:
    if isinstance(v, datetime):
        return v.replace(tzinfo=UTC) if v.tzinfo is None else v.astimezone(UTC)
    if isinstance(v, str):
        return v.rstrip(' ') if len(v) in (1, 28, 64) else v      # CHAR(n) columns come back padded on some servers
    return v


class Report:
    def __init__(self) -> None:
        self.tables: dict[str, dict[str, int]] = {}
        self.notes: dict[str, Any] = {}

    def add(self, name: str, c: Counter) -> None:
        cur = Counter(self.tables.get(name, {}))
        cur.update(c)
        self.tables[name] = {k: int(v) for k, v in cur.items()}

    def changed(self) -> int:
        return sum(v.get('inserted', 0) + v.get('updated', 0) for v in self.tables.values())


# ------------------------------------------------------------------ step 0: gate
def gate(conn: Connection, etl_run_id: int, sources: dict, topic: Path, roles: Iterable[str],
         report: Report) -> dict[str, Path]:
    """Hash every input of the requested roles; refuse blocked sources. Returns role -> verified path."""
    paths: dict[str, Path] = {}
    checks = []
    for role in roles:
        src, f = file_of(sources, role)
        if not src.get('redistribution_ok', False) or src['source_id'] in BLOCKED_SOURCE_IDS:
            raise LicenceBlock(f"source {src['source_id']!r} may not be redistributed; refusing to load role {role!r}")
        path = (topic / 'data' / f['path']).resolve() if not f['path'].startswith('../') \
            else (topic / 'data' / f['path']).resolve()
        if not path.is_file():
            raise EtlError(f'input file missing: {f["path"]}')
        actual = sha256_file(path)
        expected = f.get('sha256')
        checks.append((src['source_id'], f['path'], expected or actual, actual))
        if expected and expected != actual:
            for sid, p, e, a in checks:
                conn.execute(T['etl_input'].insert().values(
                    etl_run_id=etl_run_id, source_id=sid, file_path=p, sha256_expected=e, sha256_actual=a))
            raise HashMismatch(f'{f["path"]}: expected {expected[:12]}…, found {actual[:12]}…')
        paths[role] = path
    for sid, p, e, a in checks:
        conn.execute(T['etl_input'].insert().values(
            etl_run_id=etl_run_id, source_id=sid, file_path=p, sha256_expected=e, sha256_actual=a))
    report.notes['inputs_verified'] = [{'file': p, 'sha256': a} for _, p, _, a in checks]
    return paths


# ------------------------------------------------------------------ step 1: data_source
def step_sources(conn: Connection, sources: dict, report: Report) -> None:
    rows = []
    for s in sources.values():
        sha = next((f.get('sha256') for f in s.get('files', []) if f.get('sha256')), None)
        rows.append({
            'source_id': s['source_id'], 'name': s['name'], 'version': s['version'], 'citation': s['citation'],
            'url': s.get('url'), 'license_name': s['license_name'], 'license_class': s['license_class'],
            'redistribution_ok': bool(s['redistribution_ok']), 'attribution_text': s['attribution_text'],
            'disclaimer_text': s.get('disclaimer_text'), 'sha256': sha,
            'retrieved_on': date.fromisoformat(str(s['retrieved_on'])) if s.get('retrieved_on') else None})
    cols = ['name', 'version', 'citation', 'url', 'license_name', 'license_class', 'redistribution_ok',
            'attribution_text', 'disclaimer_text', 'sha256', 'retrieved_on']
    report.add('data_source', sync(conn, T['data_source'], ['source_id'], rows, cols))


# ------------------------------------------------------------------ step 2: protein
def read_fasta(path: Path) -> Iterator[tuple[str, str, str | None, str | None]]:
    """-> (accession, sequence, gene, protein name). Rejects duplicate accessions."""
    acc: str | None = None
    buf: list[str] = []
    header = ''
    seen: set[str] = set()

    def emit():
        if acc is None:
            return None
        if acc in seen:
            raise EtlError(f'duplicate accession {acc}')
        seen.add(acc)
        gn = re.search(r'\bGN=(\S+)', header)
        name = re.match(r'sp\|[^|]+\|\S+\s+(.*?)\s+OS=', header)
        return acc, ''.join(buf), gn.group(1) if gn else None, name.group(1) if name else None

    with gzip.open(path, 'rt') as fh:
        for line in fh:
            if line.startswith('>'):
                rec = emit()
                if rec:
                    yield rec
                header = line[1:].strip()
                parts = header.split('|')
                acc = parts[1] if len(parts) >= 3 else None
                buf = []
            else:
                buf.append(line.strip())
    rec = emit()
    if rec:
        yield rec


def step_protein(conn: Connection, fasta: Path, source_id: str, release: str, report: Report) -> dict[str, str]:
    seqs: dict[str, str] = {}
    rows = []
    for acc, seq, gene, name in read_fasta(fasta):
        seqs[acc] = seq
        rows.append({'uniprot_acc': acc, 'gene_symbol': gene, 'protein_name': name, 'length': len(seq),
                     'sequence': seq, 'uniprot_release': release, 'source_id': source_id})
    cols = ['gene_symbol', 'protein_name', 'length', 'sequence', 'uniprot_release', 'source_id']
    c: Counter = Counter()
    for i in range(0, len(rows), 2000):
        c.update(sync(conn, T['protein'], ['uniprot_acc'], rows[i:i + 2000], cols))
    report.add('protein', c)
    return seqs


# ------------------------------------------------------------------ steps 3-4: tile and screen
def read_screen(path: Path) -> dict[tuple[str, int], tuple[str, float | None, float | None]]:
    out: dict[tuple[str, int], tuple[str, float | None, float | None]] = {}
    with path.open(encoding='utf-8') as fh:
        next(fh)
        for line in fh:
            pep, reads, psi = line.rstrip('\n').split('\t')
            head, _, n = pep.rpartition('_')
            acc = head.split('_', 1)[0]
            try:
                n_i = int(n)
            except ValueError:
                continue
            r = None if reads in ('NA', '') else float(reads)
            p = None if psi in ('NA', '') else float(psi)
            out[(acc, n_i)] = (pep, r, p)
    return out


def tier1_status(psi: float | None, reads: float | None, read_min: float, psi_max: float) -> str:
    if psi is None or reads is None or reads < read_min:
        return 'measured_unreliable'
    return 'measured_in_domain' if psi <= psi_max else 'measured_out_of_domain'


def step_tiles(conn: Connection, seqs: dict[str, str], screen: dict, uniprot_source: str, params: dict,
               report: Report) -> None:
    L, step = params['tile']['length'], params['tile']['step']
    rm, pm = params['screen']['read_min'], params['screen']['psi_max']
    matched: set[tuple[str, int]] = set()
    counts: Counter = Counter()
    sync_c: Counter = Counter()
    accs = sorted(seqs)
    cols = ['start_pos', 'end_pos', 'sequence', 'scorable', 'screen_peptide_id', 'psi_wt_measured',
            'reads_measured', 'domain_status', 'source_id']
    for i in range(0, len(accs), 1500):
        rows = []
        for acc in accs[i:i + 1500]:
            seq = seqs[acc]
            for n in range(1, n_tiles(len(seq)) + 1):
                start = (n - 1) * step + 1
                ts = seq[start - 1:start - 1 + L]
                ok = is_scorable(ts)
                pep, reads, psi = screen.get((acc, n), (None, None, None))
                status = 'unknown'
                if pep is not None:
                    matched.add((acc, n))
                    if ok:
                        status = tier1_status(psi, reads, rm, pm)
                    else:
                        counts['screen_matched_not_scorable'] += 1
                counts[status] += 1 if ok else 0
                rows.append({'uniprot_acc': acc, 'tile_index': n, 'start_pos': start, 'end_pos': start + L - 1,
                             'sequence': ts, 'scorable': ok, 'screen_peptide_id': pep,
                             'psi_wt_measured': psi if pep is not None else None,
                             'reads_measured': reads if pep is not None else None,
                             'domain_status': status, 'source_id': uniprot_source})
        sync_c.update(sync(conn, T['tile'], ['uniprot_acc', 'tile_index'], rows, cols))
    report.add('tile', sync_c)
    unmatched = [k for k in screen if k not in matched]
    reasons: Counter = Counter()
    for acc, n in unmatched:
        if acc not in seqs:
            reasons['accession_not_in_snapshot'] += 1
        else:
            reasons['tile_index_beyond_last_window'] += 1
            excess = n - n_tiles(len(seqs[acc]))
            reasons['beyond_last_window_by_1' if excess == 1 else 'beyond_last_window_by_2' if excess == 2
                    else 'beyond_last_window_by_3_or_more'] += 1
    report.notes['tiles_per_domain_status'] = {k: int(v) for k, v in counts.items() if k != 'screen_matched_not_scorable'}
    report.notes['screen_rows'] = len(screen)
    report.notes['screen_rows_unmatched'] = len(unmatched)
    report.notes['screen_rows_unmatched_reasons'] = dict(reasons)
    report.notes['screen_matched_not_scorable'] = int(counts['screen_matched_not_scorable'])


# ------------------------------------------------------------------ step 5: measured cells
def step_measured(conn: Connection, npz: Path, seqs: dict[str, str], source_id: str, report: Report) -> None:
    z = np.load(npz, allow_pickle=False)
    X, y, idx, peps = z['X'], z['y'], z['idx'], z['peps']
    tile_ids = {(r.uniprot_acc, r.tile_index): (r.tile_id, r.sequence) for r in conn.execute(
        select(T['tile'].c.uniprot_acc, T['tile'].c.tile_index, T['tile'].c.tile_id, T['tile'].c.sequence))}
    rows: list[dict] = []
    mismatches = 0
    for pep, (a, b) in zip(peps, idx, strict=False):
        acc, n = str(pep).split('_')[0], int(str(pep).split('_')[-1])
        key = (acc, n)
        if key not in tile_ids:
            mismatches += int(b - a)
            continue
        tile_id, tseq = tile_ids[key]
        Xall, cells = feature_matrix(tseq)
        j = 0
        for r in range(int(a), int(b)):
            while j < len(cells) and np.abs(Xall[j] - X[r, :180]).max() > 1e-9:
                j += 1
            if j == len(cells):                    # row not found in order: tile sequence or order disagrees
                mismatches += 1
                j = 0
                continue
            pos, aa = cells[j]
            rows.append({'tile_id': tile_id, 'position': pos, 'mut_aa': aa, 'delta_psi': float(y[r]),
                         'in_training_set': True, 'source_id': source_id})
            j += 1
    if mismatches:
        raise EtlError(f'ETL-04: {mismatches} training cells do not match the UniProt-derived tile features')
    c: Counter = Counter()
    for i in range(0, len(rows), 20000):
        c.update(sync(conn, T['measured_cell'], ['tile_id', 'position', 'mut_aa'], rows[i:i + 20000],
                      ['delta_psi', 'in_training_set', 'source_id']))
    report.add('measured_cell', c)
    report.notes['training_peptides'] = int(len(peps))
    report.notes['training_cells'] = len(rows)
    report.notes['training_tile_mismatches'] = mismatches


# ------------------------------------------------------------------ step 6: ClinVar
PCHANGE = re.compile(r'\(p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})\)')
THREE = {'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 'Cys': 'C', 'Gln': 'Q', 'Glu': 'E', 'Gly': 'G',
         'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K', 'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S',
         'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V'}


def clinsig_class(text_: str) -> str:
    t = text_.lower()
    if 'conflicting' in t:
        return 'conflicting'
    if 'pathogenic' in t:
        return 'pathogenic' if re.search(r'(?<!likely )pathogenic', t) else 'likely_pathogenic'
    if 'uncertain' in t:
        return 'vus'
    if 'benign' in t:
        return 'benign' if re.search(r'(?<!likely )benign', t) else 'likely_benign'
    return 'other'


def parse_eval_date(s: str) -> date | None:
    for fmt in ('%b %d, %Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def stream_clinvar(path: Path) -> Iterator[dict]:
    seen: set[str] = set()
    with gzip.open(path, 'rt', errors='replace') as fh:
        header = fh.readline().lstrip('#').rstrip('\n').split('\t')
        col = {n: i for i, n in enumerate(header)}
        need = ('Name', 'GeneSymbol', 'ClinicalSignificance', 'VariationID')
        miss = [n for n in need if n not in col]
        if miss:
            raise EtlError(f'ClinVar file lacks columns {miss}')
        rs, le = col.get('ReviewStatus'), col.get('LastEvaluated')
        for line in fh:
            f = line.rstrip('\n').split('\t')
            if len(f) <= col['Name']:
                continue
            vid = f[col['VariationID']]
            if vid in seen:
                continue
            m = PCHANGE.search(f[col['Name']])
            if not m:
                continue
            ref, alt = THREE.get(m.group(1)), THREE.get(m.group(3))
            if not ref or not alt or ref == alt:
                continue
            seen.add(vid)
            yield {'variation_id': int(vid), 'gene': f[col['GeneSymbol']].split(';')[0].split('|')[0].strip(),
                   'pos': int(m.group(2)), 'ref': ref, 'alt': alt, 'clinsig': clinsig_class(f[col['ClinicalSignificance']]),
                   'review_status': (f[rs].strip() or None) if rs is not None and len(f) > rs else None,
                   'last_evaluated': parse_eval_date(f[le]) if le is not None and len(f) > le else None}


def step_clinvar(conn: Connection, path: Path, seqs: dict[str, str], genes: dict[str, str | None], source_id: str,
                 file_date: date, scope: str, report: Report) -> None:
    gene2acc: dict[str, list[str]] = {}
    for acc, g in genes.items():
        if g:
            gene2acc.setdefault(g, []).append(acc)
    in_domain: set[tuple[str, int]] = set()
    if scope == 'degron-only':
        t = T['tile']
        in_domain = {(r.uniprot_acc, r.tile_index) for r in conn.execute(
            select(t.c.uniprot_acc, t.c.tile_index).where(t.c.domain_status == 'measured_in_domain'))}
    cols = ['uniprot_acc', 'protein_pos', 'ref_aa', 'alt_aa', 'clinsig', 'review_status', 'last_evaluated',
            'clinvar_file_date', 'source_id']
    stats: Counter = Counter()
    seen_ids: set[int] = set()
    batch: list[dict] = []
    sync_c: Counter = Counter()

    def flush():
        nonlocal batch
        if batch:
            sync_c.update(sync(conn, T['clinvar_variant'], ['variation_id'], batch, cols))
            batch = []

    for v in stream_clinvar(path):
        stats['missense_read'] += 1
        accs = gene2acc.get(v['gene'])
        if not accs:
            stats['gene_not_in_snapshot'] += 1
            continue
        hit = None
        for acc in sorted(accs):
            s = seqs[acc]
            if v['pos'] <= len(s) and s[v['pos'] - 1] == v['ref']:
                hit = acc
                break
        if hit is None:
            stats['reference_residue_mismatch'] += 1
            continue
        nmax = n_tiles(len(seqs[hit]))
        if scope in ('in-tiles', 'degron-only'):
            if nmax == 0 or v['pos'] > (nmax - 1) * 23 + 28:
                stats['outside_all_tiles'] += 1
                continue
        if scope == 'degron-only':
            n_hi = (v['pos'] - 1) // 23 + 1
            if not any((hit, n) in in_domain for n in (n_hi - 1, n_hi) if n >= 1):
                stats['outside_in_domain_tiles'] += 1
                continue
        seen_ids.add(v['variation_id'])
        batch.append({'variation_id': v['variation_id'], 'uniprot_acc': hit, 'protein_pos': v['pos'],
                      'ref_aa': v['ref'], 'alt_aa': v['alt'], 'clinsig': v['clinsig'],
                      'review_status': v['review_status'], 'last_evaluated': v['last_evaluated'],
                      'clinvar_file_date': file_date, 'source_id': source_id})
        if len(batch) >= 20000:
            flush()
    flush()
    existing = {r[0] for r in conn.execute(select(T['clinvar_variant'].c.variation_id))}
    stale = sorted(existing - seen_ids)
    for i in range(0, len(stale), 5000):
        conn.execute(delete(T['clinvar_variant']).where(T['clinvar_variant'].c.variation_id.in_(stale[i:i + 5000])))
    sync_c['deleted'] += len(stale)
    report.add('clinvar_variant', sync_c)
    stats['loaded'] = len(seen_ids)
    report.notes['clinvar'] = {'scope': scope, **{k: int(v) for k, v in stats.items()}}


# ------------------------------------------------------------------ step 7: model
def build_model_card(params: dict, res: dict, curve: dict) -> tuple[dict, dict, str]:
    m = params['model']
    pl, raw = res['metrics']['platt'], res['metrics']['raw']
    util = res.get('utility', {}).get('top10pct', {})
    ridge_ext = curve['results']['ridge']['ext']
    metrics = {
        'source_file': 'research/calibration-p6-2026-10-22/results.json',
        'curve_source_file': 'research/learning-curve-2026-10-22/results.json',
        'evidence': 'development out-of-fold benchmark on 91 peptides / 89 clusters; not external validation',
        'auroc_macro_ensemble_ext4.0': ridge_ext['macro_auroc_ensemble'],
        'auroc_macro_per_seed': ridge_ext['macro_auroc_per_seed'],
        'p0_verdict_ridge': curve.get('verdict', {}).get('ridge'),
        'brier_platt': pl['brier'], 'brier_platt_ci95': pl['brier_ci95'],
        'brier_raw': raw['brier'], 'brier_raw_ci95': raw['brier_ci95'],
        'ece_platt': pl['ece'], 'bss_vs_base_rate_platt': pl['bss_vs_const'],
        'enrichment_top10pct': util.get('enrichment'), 'precision_top10pct': util.get('precision'),
        'n_test_cells': res['n_test_cells'], 'n_test_peptides': res['n_test_peptides'],
        'n_test_clusters': res['n_test_clusters'], 'seeds': res['seeds'],
    }
    calibration = {
        'method': 'platt (default), isotonic available', 'mean_predicted_probability_platt': pl['mean_pred'],
        'recalibration_line_platt': pl['recalibration_line'],
        'note': 'Probabilities are for the event DeltaPSI >= 1.0 in the training domain; they run about 13 % low on '
                'the original 91-peptide domain.',
    }
    ci = metrics['brier_platt_ci95']
    card = f"""# Model card: {m['model_id']}

**What it predicts.** For each of the 532 single substitutions of a 28-residue internal tile, the calibrated
probability of the event `DeltaPSI >= 1.0` (the substitution stabilises the GFP reporter by at least one PSI unit)
in the GPS assay of Zhang et al. 2023.

**Model.** Ridge regression on 180 features (wild-type and mutant one-hot, tile composition, one-hot context at
offsets -3..+3), trained on 176 peptides / 92,337 cells (wild-type PSI <= 4.0), with Platt calibration.

**Evidence ({metrics['evidence']}).**
Macro AUROC {metrics['auroc_macro_ensemble_ext4.0']:.4f} (three seeds, ensemble).
Platt Brier {metrics['brier_platt']:.4f} (95 % CI {ci[0]:.4f} to {ci[1]:.4f}) against {metrics['brier_raw']:.4f} for the raw score.
Top 10 % of substitutions per tile enrich positives about {metrics['enrichment_top10pct']['mean']:.1f}-fold over random.
The 176 training peptides include those used for the numbers above only in cross-fitted folds; **the
interface's measured-data overlay is training data, not validation.**

**Limits.** Valid for 28-mer tiles of the GPS assay and tiles with wild-type PSI <= 4.0. A tile outside this domain,
or of unknown domain, is not covered. Probabilities are not probabilities of disease. No external validation exists.
"""
    return metrics, calibration, card


def step_model(conn: Connection, paths: dict[str, Path], params: dict, model_dir: Path, report: Report) -> None:
    m = params['model']
    model_dir.mkdir(parents=True, exist_ok=True)
    target = model_dir / m['weights_file']
    src = paths['model_weights']
    if not target.exists() or sha256_file(target) != sha256_file(src):
        shutil.copyfile(src, target)
    sha = sha256_file(target)
    res = json.loads(paths['model_results'].read_text(encoding='utf-8'))
    curve = json.loads(paths['curve_results'].read_text(encoding='utf-8'))
    metrics, calibration, card = build_model_card(params, res, curve)
    frozen = datetime.fromisoformat(m['frozen_at'])
    row = {
        'model_id': m['model_id'], 'role': 'effect', 'kind': 'ridge_platt', 'status': 'frozen', 'is_default': True,
        'tile_length': 28, 'feature_spec': m['feature_spec'], 'weights_path': m['weights_file'],
        'weights_sha256': sha, 'event_definition': m['event_definition'],
        'domain_description': m['domain_description'], 'metrics': metrics, 'calibration': calibration,
        'trained_on_sources': ['zhang2023-mendeley-v2'],
        'evidence_label': 'development OOF benchmark, not external validation', 'card_markdown': card,
        'created_at': frozen, 'frozen_at': frozen}
    cols = ['role', 'kind', 'status', 'is_default', 'tile_length', 'feature_spec', 'weights_path', 'weights_sha256',
            'event_definition', 'domain_description', 'metrics', 'calibration', 'trained_on_sources',
            'evidence_label', 'card_markdown', 'frozen_at']
    report.add('model_version', sync(conn, T['model_version'], ['model_id'], [row], cols))
    report.notes['model_weights_sha256'] = sha


# ------------------------------------------------------------------ driver
def run(db_url: str, data_dir_topic: Path | None = None, sources_path: Path | None = None,
        params_path: Path | None = None, clinvar_scope: str = 'in-tiles', model_dir: Path | None = None,
        engine=None) -> dict:
    topic = data_dir_topic or find_topic()
    sources, params = load_config(sources_path or HERE / 'sources.yaml', params_path or HERE / 'params.yaml')
    model_dir = model_dir or APP_DIR / 'backend' / 'models'
    engine = engine or make_engine(db_url)
    if clinvar_scope not in ('all', 'in-tiles', 'degron-only', 'none'):
        raise EtlError(f'unknown --clinvar-scope {clinvar_scope!r}')
    started = datetime.now(UTC)
    t0 = time.time()
    report = Report()
    with engine.begin() as conn:
        etl_run_id = conn.execute(T['etl_run'].insert().values(
            started_at=started, git_commit=git_commit(topic.parents[1] if len(topic.parents) > 1 else topic),
            status='running', report={})).inserted_primary_key[0]
    status = 'failed'
    error: str | None = None
    try:
        roles = ['protein_fasta', 'screen_psi', 'sat_labels', 'model_weights', 'model_results', 'curve_results']
        if clinvar_scope != 'none':
            roles.append('clinvar_summary')
        gate_error: EtlError | None = None
        paths: dict[str, Path] = {}
        with engine.begin() as conn:        # own transaction: the evidence of a failed gate must be kept
            step_sources(conn, sources, report)
            try:
                paths = gate(conn, etl_run_id, sources, topic, roles, report)
            except EtlError as exc:
                gate_error = exc
        if gate_error is not None:
            raise gate_error
        with engine.begin() as conn:
            step_model(conn, paths, params, model_dir, report)
            up_src, _ = file_of(sources, 'protein_fasta')
            geo_src, _ = file_of(sources, 'screen_psi')
            sat_src, _ = file_of(sources, 'sat_labels')
            seqs = step_protein(conn, paths['protein_fasta'], up_src['source_id'], _release(up_src), report)
            genes = {acc: g for acc, _, g, _ in read_fasta(paths['protein_fasta'])}
            screen = read_screen(paths['screen_psi'])
            step_tiles(conn, seqs, screen, up_src['source_id'], params, report)
            step_measured(conn, paths['sat_labels'], seqs, sat_src['source_id'], report)
            if clinvar_scope != 'none':
                cv_src, _ = file_of(sources, 'clinvar_summary')
                step_clinvar(conn, paths['clinvar_summary'], seqs, genes, cv_src['source_id'],
                             date.fromisoformat(str(params['clinvar']['file_date'])), clinvar_scope, report)
            del geo_src
        status = 'succeeded'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        out = {'tables': report.tables, **report.notes, 'seconds': round(time.time() - t0, 1),
               'reference_rows_changed': report.changed(), 'clinvar_scope': clinvar_scope}
        if error:
            out['error'] = error
        with engine.begin() as conn:
            conn.execute(T['etl_run'].update().where(T['etl_run'].c.etl_run_id == etl_run_id).values(
                finished_at=datetime.now(UTC), status=status, report=out))
    return out


def _release(src: dict) -> str:
    m = re.search(r'release (\S+?)[,\s]', src['version'] + ' ')
    return m.group(1) if m else src['version']


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--db', default='sqlite:///./degron.db', help='SQLAlchemy URL (default: SQLite file)')
    ap.add_argument('--clinvar-scope', default='in-tiles', choices=['all', 'in-tiles', 'degron-only', 'none'])
    ap.add_argument('--topic', type=Path, help='path of topics/degron-footprint (default: found from this file)')
    ap.add_argument('--sources', type=Path)
    ap.add_argument('--params', type=Path)
    ap.add_argument('--model-dir', type=Path)
    ap.add_argument('--report', type=Path, help='also write the report as JSON to this file')
    a = ap.parse_args(argv)
    try:
        rep = run(a.db, a.topic, a.sources, a.params, a.clinvar_scope, a.model_dir)
    except EtlError as exc:
        print(f'ETL aborted: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(rep, indent=2, default=str))
    if a.report:
        a.report.write_text(json.dumps(rep, indent=2, default=str), encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


__all__ = ['run', 'main', 'EtlError', 'LicenceBlock', 'HashMismatch', 'text', 'hashlib']
