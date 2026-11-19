"""Command line for the local Degron Footprint service (plan-system 3.4).

    python -m api.cli [--api URL | --offline] predict --sequence SEQ [--model ID] [--format json|csv] [--out FILE]
    python -m api.cli predict --uniprot P60484 --tile 3
    python -m api.cli job --project ID --fasta proteins.fa [--wait] [--export csv --out manifest.csv]
    python -m api.cli job --project ID --peptides peptides.csv --wait
    python -m api.cli export job JOB_ID --format csv --out manifest.csv
    python -m api.cli export analysis ANALYSIS_ID --format json
    python -m api.cli compare ANALYSIS_A ANALYSIS_B [--save]

`--api` (default $DF_API_URL or http://127.0.0.1:8080) talks to a running service. `--offline` runs the same service
code in this process on $DF_DATABASE_URL (prediction, saved analyses, jobs drained by an in-process worker, exports,
comparisons) — never a separate scoring path (D-9, RG-01). Results go to stdout or --out; the log on stderr carries
counts and ids only, never a sequence (NFR-09).
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any

from .client import ApiError, Client

log = logging.getLogger('api.cli')


class Offline:
    """The service's own functions in-process (same validation, scoring, storage and exports as the API)."""

    def __init__(self) -> None:
        from db.session import make_engine, make_session_factory

        from .config import Settings
        from .core import build_core
        self.settings = Settings()
        engine = make_engine(self.settings.database_url)
        self.core = build_core(self.settings, engine, make_session_factory(engine))

    def predict(self, **tile: Any) -> dict:
        from .client import _tile_request
        from .requests import parse_predict
        req = parse_predict(_tile_request(tile.get('sequence'), tile.get('uniprot_id'), tile.get('tile_index'),
                                          tile.get('model_id'), tile.get('calibrator'), tile.get('override_domain')))
        with self.core.factory() as s:
            return self.core.predictor.predict(req, s if req.sequence is None else None).result

    def export(self, fmt: str = 'csv', **tile: Any) -> str:
        from degron_footprint.export import to_csv, to_json_payload
        result = self.predict(**tile)
        return to_csv(result) if fmt == 'csv' else json.dumps(to_json_payload(result))

    def submit_job(self, project_id: str, body: dict) -> dict:
        from . import jobs
        from . import workspace_store as ws
        with self.core.factory() as s, s.begin():
            ws.require_active(ws.get_project(s, ws.parse_id(project_id, 'project_id')))
            job = jobs.submit(s, self.core.predictor, self.settings, project_id, body, self.core.gate.gate_model_id,
                              self.core.gate.weights_sha256)
            return jobs.job_dict(s, job)

    def wait_job(self, job_id: str, **_: Any) -> dict:
        from .worker import from_core
        from_core(self.core, owner=f'cli:{os.getpid()}').drain()
        return self.job(job_id)

    def job(self, job_id: str) -> dict:
        from . import jobs
        with self.core.factory() as s:
            return jobs.job_dict(s, jobs.get_job(s, job_id))

    def export_job(self, job_id: str, fmt: str = 'csv') -> str:
        from . import exports
        job = self.job(job_id)
        gen = exports.job_csv(self.core.factory, job) if fmt == 'csv' else exports.job_json(self.core.factory, job)
        return ''.join(part.decode() if isinstance(part, bytes) else part for part in gen)

    def export_analysis(self, analysis_id: str, fmt: str = 'csv') -> str:
        from . import exports
        from . import workspace_store as ws
        with self.core.factory() as s:
            data = ws.analysis_dict(s, ws.get_analysis(s, analysis_id))
        resp = exports.analysis_file(data, fmt)
        return bytes(resp.body).decode()

    def compare(self, analysis_a: str, analysis_b: str, save: bool = False) -> dict:
        from . import model_compare
        with self.core.factory() as s, s.begin():
            out, _saved = model_compare.compare(s, analysis_a, analysis_b, save)
            return out


# ---------------------------------------------------------------------------------------------------------- inputs
def read_fasta(path: Path) -> list[dict]:
    records: list[dict] = []
    name: str | None = None
    seq: list[str] = []
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line.startswith('>'):
            if name is not None or seq:
                records.append({'input_id': name or f'protein-{len(records) + 1}', 'sequence': ''.join(seq)})
            name, seq = (line[1:].split() or [f'protein-{len(records) + 1}'])[0], []
        elif line:
            seq.append(line)
    if name is not None or seq:
        records.append({'input_id': name or f'protein-{len(records) + 1}', 'sequence': ''.join(seq)})
    return records


def read_peptides(path: Path) -> list[dict]:
    """`id,SEQUENCE` lines (header optional) or a FASTA file of 28-residue peptides."""
    text = path.read_text(encoding='utf-8')
    if text.lstrip().startswith('>'):
        return read_fasta(path)
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        parts = [p.strip() for p in re.split(r'[,\t]', line) if p.strip()]
        if not parts or parts[0].lower() in ('input_id', 'id', 'peptide_id'):
            continue
        out.append({'input_id': parts[0], 'sequence': parts[1]} if len(parts) > 1 else
                   {'input_id': f'p{i}', 'sequence': parts[0]})
    return out


def emit(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding='utf-8')
        log.info('written %s (%d bytes)', out, len(text.encode()))
    else:
        sys.stdout.write(text if text.endswith('\n') else text + '\n')


# ---------------------------------------------------------------------------------------------------------- main
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog='python -m api.cli', description='Degron Footprint command line (local service).')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--api', default=os.environ.get('DF_API_URL', 'http://127.0.0.1:8080'), help='service URL')
    mode.add_argument('--offline', action='store_true', help='run the service code in this process (DF_DATABASE_URL)')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('predict', help='score one 28-residue tile')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--sequence')
    g.add_argument('--uniprot')
    p.add_argument('--tile', type=int)
    p.add_argument('--model')
    p.add_argument('--calibrator', choices=['platt', 'iso'])
    p.add_argument('--override-domain', action='store_true')
    p.add_argument('--format', choices=['json', 'csv'], default='json')
    p.add_argument('--out')

    j = sub.add_parser('job', help='submit a peptide batch or protein job to a project')
    j.add_argument('--project', required=True)
    src = j.add_mutually_exclusive_group(required=True)
    src.add_argument('--fasta', type=Path, help='one or more protein FASTA records (protein job)')
    src.add_argument('--uniprot', nargs='+', help='one or more loaded accessions (protein job)')
    src.add_argument('--peptides', type=Path, help='id,SEQUENCE lines or FASTA of 28-residue peptides')
    j.add_argument('--model')
    j.add_argument('--override-domain', action='store_true')
    j.add_argument('--wait', action='store_true', help='wait until the job is finished (offline: run the worker here)')
    j.add_argument('--export', choices=['csv', 'json'], help='after --wait, write the job export')
    j.add_argument('--out')

    e = sub.add_parser('export', help='export a saved analysis or a job')
    e.add_argument('what', choices=['analysis', 'job'])
    e.add_argument('id')
    e.add_argument('--format', choices=['csv', 'json'], default='csv')
    e.add_argument('--out')

    c = sub.add_parser('compare', help='compare two saved analyses of the same tile (usually two models)')
    c.add_argument('analysis_a')
    c.add_argument('analysis_b')
    c.add_argument('--save', action='store_true')
    c.add_argument('--out')
    return ap


def run(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    logging.basicConfig(level=os.environ.get('DF_LOG_LEVEL', 'INFO'), stream=sys.stderr,
                        format='%(levelname)s %(name)s %(message)s')
    svc: Any = Offline() if a.offline else Client(a.api)
    try:
        if a.cmd == 'predict':
            if a.uniprot and a.tile is None:
                raise SystemExit('--tile is required with --uniprot')
            tile = {'sequence': a.sequence, 'uniprot_id': a.uniprot, 'tile_index': a.tile, 'model_id': a.model,
                    'calibrator': a.calibrator, 'override_domain': a.override_domain}
            if a.format == 'csv':
                emit(svc.export('csv', **tile), a.out)
            else:
                res = svc.predict(**tile)
                log.info('scored %d cells with %s; domain %s; warnings %s', len(res['cells']),
                         res['provenance']['model_id'], res['domain']['status'],
                         ','.join(w['code'] for w in res['warnings']) or 'none')
                emit(json.dumps(res, indent=2), a.out)
        elif a.cmd == 'job':
            body: dict[str, Any] = {'mode': 'protein', 'override_domain': a.override_domain}
            if a.peptides:
                body = {'mode': 'peptides', 'override_domain': a.override_domain, 'peptides': read_peptides(a.peptides)}
            elif a.fasta:
                recs = read_fasta(a.fasta)
                body.update({'protein': recs[0]} if len(recs) == 1 else {'proteins': recs})
            else:
                accs = [{'uniprot_id': x} for x in a.uniprot]
                body.update({'protein': accs[0]} if len(accs) == 1 else {'proteins': accs})
            if a.model:
                body['model_id'] = a.model
            job = svc.submit_job(a.project, body)
            log.info('job %s submitted: %d items, %d refused at submission', job['job_id'], job['total'],
                     job['counts'].get('refused', 0))
            if a.wait:
                job = svc.wait_job(job['job_id'])
                log.info('job %s %s: %s', job['job_id'], job['state'], json.dumps(job['counts']))
                if a.export:
                    emit(svc.export_job(job['job_id'], a.export), a.out)
                    return 0
            emit(json.dumps(job, indent=2), a.out)
        elif a.cmd == 'export':
            text = svc.export_job(a.id, a.format) if a.what == 'job' else svc.export_analysis(a.id, a.format)
            emit(text, a.out)
        elif a.cmd == 'compare':
            out = svc.compare(a.analysis_a, a.analysis_b, a.save)
            m = out['metrics']
            log.info('compared %s and %s: Spearman raw %s, top-10%% Jaccard %s', out['provenance']['a']['model_id'],
                     out['provenance']['b']['model_id'], m['spearman_raw'], m['top_k_jaccard'])
            emit(json.dumps(out, indent=2), a.out)
    except ApiError as exc:
        log.error('%s', exc)
        return 2
    except Exception as exc:                                  # DomainError in offline mode, file errors
        code = getattr(exc, 'code', type(exc).__name__)
        log.error('%s: %s', code, getattr(exc, 'message', str(exc)))
        return 2
    return 0


def main() -> None:                                           # pragma: no cover
    raise SystemExit(run())


if __name__ == '__main__':                                    # pragma: no cover
    main()
