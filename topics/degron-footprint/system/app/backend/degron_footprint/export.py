"""CSV and JSON exports with provenance (api-spec.md §7). Same nine columns as the command-line prototype."""
from __future__ import annotations

import csv
import io
import re
from datetime import UTC, datetime

from .constants import DISCLAIMER_EXPORT
from .provenance import utc_iso

COLUMNS = ['peptide', 'tile', 'position', 'wt_aa', 'mut_aa', 'score_dpsi_raw',
           'p_dpsi_ge_1_calibrated', 'rank_in_tile', 'top10pct_in_tile']


def _clean(value: object) -> str:
    """Comment-line values never contain a line break, so a field cannot forge a table row."""
    return re.sub(r'[\r\n]+', ' ', str(value))


def peptide_label(result: dict) -> tuple[str, int]:
    t = result['tile']
    if t.get('uniprot_id') and t.get('tile_index'):
        return f"{t['uniprot_id']}_{t['tile_index']}", int(t['tile_index'])
    return 'user_seq', 0


def to_csv(result: dict) -> str:
    p, d = result['provenance'], result['domain']
    lines = [
        ('model_id', p['model_id']),
        ('weights_sha256', p['weights_sha256']),
        ('event_definition', p['event_definition']),
        ('evidence_label', p['evidence_label']),
        ('domain_status', d['status']),
        ('data_sources', ','.join(s['source_id'] for s in p['data_sources'])),
        ('generated_at', p['generated_at']),
        ('disclaimer', DISCLAIMER_EXPORT),
        ('domain_description', p['domain_description']),
        ('code_version', p['code_version']),
        ('warnings', ','.join(w['code'] for w in result['warnings']) or 'none'),
        ('feature_spec', p.get('feature_spec') or ''),
    ]
    for text in p['disclaimers']:
        lines.append(('disclaimer_detail', text))
    for s in p['data_sources']:
        lines.append(('attribution', f"{s['source_id']}: {s['attribution_text']} ({s['license_name']})"))
    out = io.StringIO()
    for k, v in lines:
        out.write(f'# {k}={_clean(v)}\n')
    w = csv.writer(out, lineterminator='\n')
    w.writerow(COLUMNS)
    label, tile_no = peptide_label(result)
    for c in result['cells']:
        w.writerow([label, tile_no, c['position'], c['wt_aa'], c['mut_aa'],
                    f"{c['score_dpsi_raw']:.10g}", f"{c['p_dpsi_ge_1_calibrated']:.10g}",
                    c['rank_in_tile'], int(c['top10pct_in_tile'])])
    return out.getvalue()


def to_json_payload(result: dict, exported_at: datetime | None = None) -> dict:
    return {**result, 'exported_at': utc_iso(exported_at or datetime.now(UTC))}


def filename(result: dict, fmt: str, today: datetime | None = None) -> str:
    """The sequence itself is never part of a file name."""
    p = result['provenance']['model_id']
    t = result['tile']
    day = (today or datetime.now(UTC)).strftime('%Y-%m-%d')
    who = f"{t['uniprot_id']}-t{t['tile_index']}" if t.get('uniprot_id') and t.get('tile_index') else 'user-seq'
    return f'degron-footprint_{p}_{who}_{day}.{fmt}'
