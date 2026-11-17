"""Exports of saved work (api-spec §8): saved analyses (optionally with one comparison), and job manifests.

Everything is written from stored snapshots. The nine baseline score columns stay first and unchanged; added columns
are namespaced. Text that came from a user file is neutralised so a spreadsheet does not run it as a formula (SEC-02).
"""
from __future__ import annotations

import csv
import io
import re
from datetime import UTC, datetime
from typing import Any

from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from db.models import Comparison
from degron_footprint.errors import DomainError
from degron_footprint.export import COLUMNS, filename, to_csv
from degron_footprint.provenance import utc_iso

NO_STORE = {'Cache-Control': 'no-store'}
FORMULA_START = re.compile(r'^[=+\-@\t\r]')
COMPARISON_COLUMNS = ['measurement_observed', 'measurement_units', 'measurement_n_replicates',
                      'measurement_residual_pred_minus_obs']


def safe_cell(value: Any) -> Any:
    """Prefix text that a spreadsheet would evaluate (=, +, -, @, tab, CR) with an apostrophe. Numbers pass."""
    if isinstance(value, str) and FORMULA_START.match(value):
        return "'" + value
    return value


LINE_BREAKS = re.compile(r'[\r\n]+')


def _comment(key: str, value: Any) -> str:
    text = LINE_BREAKS.sub(' ', str(value))
    return f'# {key}={text}\n'


def comparison_for_export(s: Session, comparison_id: str, analysis_id: str) -> dict:
    c = s.get(Comparison, comparison_id)
    if c is None or c.analysis_id != analysis_id:
        raise DomainError('COMPARISON_NOT_FOUND', 'No comparison with this id belongs to this analysis.', 404,
                          'comparison_id')
    return {'comparison_id': c.comparison_id, 'dataset_id': c.dataset_id, 'replicate_id': c.replicate_id,
            'aggregation': c.aggregation, 'compatible': c.compatible, 'matched': c.matched, 'counts': c.counts,
            'mae': c.mae, 'spearman': c.spearman, 'metric_unavailable_reason': c.metric_unavailable_reason,
            'rows': c.rows, 'provenance': c.provenance}


def _clinvar_comments(snapshot: dict) -> list[str]:
    cv = (snapshot.get('annotations') or {}).get('clinvar') or {}
    out = [_comment('clinvar_state', cv.get('state', 'source_unavailable'))]
    if cv.get('clinvar_file_date'):
        out.append(_comment('clinvar_file_date', cv['clinvar_file_date']))
    for src in cv.get('sources') or []:
        out.append(_comment('attribution', f"{src['source_id']}: {src['attribution_text']}"))
        if src.get('disclaimer_text'):
            out.append(_comment('disclaimer_detail', src['disclaimer_text']))
    if cv.get('variants'):
        out.append(_comment('clinvar_variants', f"{len(cv['variants'])} (one-to-many; listed in the JSON export)"))
    return out


def analysis_csv(data: dict, comparison: dict | None) -> str:
    result, snap = data['result'], data['snapshot']
    base = to_csv(result)                                            # provenance comments + nine columns
    head, _, table = base.partition(','.join(COLUMNS) + '\n')
    extra = [_comment('analysis_id', data['analysis_id']), _comment('project_id', data['project_id']),
             _comment('analysis_created_at', data['created_at']), *_clinvar_comments(snap)]
    if comparison is None:
        return head + ''.join(extra) + ','.join(COLUMNS) + '\n' + table
    prov = comparison['provenance']
    extra += [_comment('comparison_id', comparison['comparison_id']),
              _comment('dataset_id', comparison['dataset_id']),
              _comment('dataset_revision', prov.get('dataset_revision')),
              _comment('replicate_or_aggregation', comparison['replicate_id'] or comparison['aggregation']),
              _comment('comparison_note', 'comparison only; not used to retrain the model')]
    by_key = {(r['position'], r['mut_aa']): r for r in comparison['rows']}
    out = io.StringIO()
    w = csv.writer(out, lineterminator='\n')
    w.writerow([*COLUMNS, *COMPARISON_COLUMNS])
    rows = csv.reader(io.StringIO(table))
    for row, cell in zip(rows, result['cells'], strict=True):
        r = by_key.get((cell['position'], cell['mut_aa']))
        w.writerow([*row, *([f"{r['observed']:.10g}", safe_cell(r['units']), r['n_replicates'],
                             '' if r['residual'] is None else f"{r['residual']:.10g}"] if r else ['', '', '', ''])])
    return head + ''.join(extra) + out.getvalue()


def analysis_file(data: dict, fmt: str, comparison: dict | None = None) -> Response:
    name = filename(data['result'], fmt).replace('degron-footprint_', f"degron-footprint_analysis-{data['analysis_id'][:8]}_")
    headers = {**NO_STORE, 'Content-Disposition': f'attachment; filename="{name}"'}
    if fmt == 'csv':
        return Response(analysis_csv(data, comparison), media_type='text/csv; charset=utf-8', headers=headers)
    payload = {**data, 'exported_at': utc_iso(datetime.now(UTC))}
    if comparison is not None:
        payload['comparison'] = comparison
    return JSONResponse(payload, headers=headers)


# --- job manifests (BATCH-06, FR-34) ---------------------------------------------------------------------------------

JOB_COLUMNS = ['project_id', 'job_id', 'item_id', 'input_id', 'uniprot_id', 'reference_release', 'start_pos',
               'end_pos', 'protein_position', 'status', 'error_code', 'domain_status']
CHUNK = 200


def _job_items(factory, job_id: str):
    """(item, analysis or None) for every item in manifest order, read in chunks so big jobs stream."""
    from sqlalchemy import select

    from db.models import AnalysisRun, JobItem
    offset = 0
    while True:
        with factory() as s:
            rows = s.execute(select(JobItem, AnalysisRun)
                             .outerjoin(AnalysisRun, (AnalysisRun.job_id == JobItem.job_id)
                                        & (AnalysisRun.item_id == JobItem.item_id))
                             .where(JobItem.job_id == job_id).order_by(JobItem.ordinal)
                             .offset(offset).limit(CHUNK)).all()
            batch = [(it, run.result if run is not None else None) for it, run in rows]
        if not batch:
            return
        yield from batch
        offset += CHUNK


def job_csv(factory, job: dict):
    from degron_footprint.constants import DISCLAIMER_EXPORT
    from degron_footprint.export import peptide_label
    cfg = job['configuration_snapshot']
    head = [('job_id', job['job_id']), ('project_id', job['project_id']), ('mode', job['mode']),
            ('state', job['state']), ('model_id', cfg.get('model_id')), ('weights_sha256', cfg.get('weights_sha256')),
            ('calibrator', cfg.get('calibrator')), ('gate_model_id', cfg.get('gate_model_id') or 'none'),
            ('override_domain', cfg.get('override_domain')), ('code_version', cfg.get('code_version')),
            ('created_at', job['created_at']), ('disclaimer', DISCLAIMER_EXPORT),
            ('note', 'One row per scored substitution; unscored items have one manifest row with empty scores. '
                     'Ranks are within each tile; overlapping protein windows are not merged.')]
    for src in cfg.get('sources') or []:
        head.append(('source', f"{src['source_id']} {src['version']}"))
    yield ''.join(_comment(k, v) for k, v in head)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow([*COLUMNS, *JOB_COLUMNS])
    yield buf.getvalue()
    for item, result in _job_items(factory, job['job_id']):
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator='\n')
        meta = [job['project_id'], job['job_id'], item.item_id, safe_cell(item.input_id), item.uniprot_acc or '',
                item.reference_release or '', item.start_pos or '', item.end_pos or '']
        tail = [item.state, (item.error or {}).get('code', ''), item.domain_status or '']
        if result is None:
            w.writerow([*([''] * len(COLUMNS)), *meta, '', *tail])
        else:
            label, tile_no = peptide_label(result)
            for c in result['cells']:
                ppos = item.start_pos + c['position'] - 1 if item.start_pos else ''
                w.writerow([label, tile_no, c['position'], c['wt_aa'], c['mut_aa'], f"{c['score_dpsi_raw']:.10g}",
                            f"{c['p_dpsi_ge_1_calibrated']:.10g}", c['rank_in_tile'], int(c['top10pct_in_tile']),
                            *meta, ppos, *tail])
        yield buf.getvalue()


def job_json(factory, job: dict):
    """{job, manifest[], analyses[]} written incrementally; analyses are the stored results."""
    import json

    from .jobs import item_dict
    yield '{"job":' + json.dumps(job) + ',"exported_at":' + json.dumps(utc_iso(datetime.now(UTC))) + ',"manifest":['
    analyses = []
    first = True
    for item, result in _job_items(factory, job['job_id']):
        yield ('' if first else ',') + json.dumps(item_dict(item, None))
        first = False
        if result is not None:
            analyses.append(item.item_id)
    yield '],"analyses":['
    first = True
    for item, result in _job_items(factory, job['job_id']):
        if result is not None:
            yield ('' if first else ',') + json.dumps({'item_id': item.item_id, 'result': result})
            first = False
    yield ']}'
