"""One-notebook orchestration of the existing v3 experiments, with durable task state.

The scientific runners remain authoritative. This layer wires dependencies, expands
GPU jobs, caches verified outputs, and records partial/resource/source outcomes.
"""
import gc
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile

import numpy as np
import pandas as pd

from .common import atomic_json, environment, sha256
from .data import Dataset
from .metrics import summarize, per_peptide, paired_ci
from .plm import specification, registry, resolve_snapshot

HERE = Path(__file__).resolve().parents[1]
ORDER = ['00', '01', '02', '03', '04', '05', '06', '11', '08', '09', '07', '10']


def identity(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def size_tree(root):
    return sum(p.stat().st_size for p in Path(root).rglob('*') if p.is_file() and not p.is_symlink())


class Pipeline:
    def __init__(self, data_root, output_root, *, smoke=True, model_ids=None,
                 sections=None, overrides=None, weight_roots=None, auto_download=True,
                 resume_from='', max_tasks=None, max_hours=8., max_output_gib=16.,
                 external_table=None, structure_table=None, run_saprot=False,
                 saprot_model='saprot_35m', finetune_model='esm2_35m', calibration_task='01'):
        from run_stage import defaults
        self.ds = Dataset(data_root)
        self.smoke = bool(smoke)
        self.sections = set(ORDER if sections is None else sections)
        assert self.sections <= set(ORDER), 'Unknown section'
        self.overrides = overrides or {}
        assert set(self.overrides) <= set(ORDER)
        # Operational paths/identity and held-source inputs are wired by this layer.
        protected = {'smoke', 'data_identity', 'implementation_sha256', 'protocol_sha256',
            'weight_roots', 'preflight_report', 'pooled_features', 'crop_features', 'results_root',
            'training_output', 'row_scope', 'row_start', 'row_stop', 'model_id', 'model_ids',
            'external_table', 'structure_table', 'run_saprot', 'saprot_model', 'finetune_model'}
        for section, values in self.overrides.items():
            assert not protected & set(values), f'Use dedicated pipeline parameters, not {section} overrides: {protected & set(values)}'
        chosen = ['esm2_35m'] if model_ids is None else model_ids
        if chosen == 'all':
            chosen = [m['id'] for m in registry()['models'] if m['family'] != 'saprot']
        assert isinstance(chosen, list) and len(chosen) and len(chosen) == len(set(chosen))
        for model in chosen:
            assert specification(model)['family'] != 'saprot', 'SaProt belongs in the conditional structure branch'
        self.models = ['esm2_8m'] if self.smoke else chosen
        self.finetune_model = 'esm2_8m' if self.smoke else finetune_model
        assert specification(self.finetune_model)['family'] != 'saprot'
        self.external = str(Path(external_table).resolve()) if external_table else None
        self.structure = str(Path(structure_table).resolve()) if structure_table else None
        self.run_saprot = bool(run_saprot)
        self.saprot_model = saprot_model
        self.calibration_task = calibration_task
        self.base = defaults(self.smoke)
        sources = sorted((HERE/'degron_v3').glob('*.py'))+[HERE/'run_stage.py', HERE/'download_weights.py']
        self.code_sha = hashlib.sha256(b''.join(p.read_bytes() for p in sources)).hexdigest()
        self.protocol_sha = sha256(HERE/'EXECUTION-PROTOCOL.md')
        self.plan = dict(schema_version=1, mode='smoke' if self.smoke else 'official',
            data_identity=self.ds.identity, implementation_sha256=self.code_sha,
            protocol_sha256=self.protocol_sha, registry_sha256=sha256(HERE/'model-registry.json'),
            dependency_spec_sha256=sha256(HERE/'requirements-kaggle.txt'),
            models=self.models, finetune_model=self.finetune_model,
            overrides=self.overrides, external_sha256=sha256(self.external) if self.external else None,
            structure_sha256=sha256(self.structure) if self.structure else None,
            run_saprot=self.run_saprot, saprot_model=self.saprot_model,
            calibration_task=calibration_task,
            selection_recipe=self.overrides.get('07', {}).get('selected_recipe', 'ordered-w5-D'))
        self.plan_id = identity(self.plan)
        self.output_root = Path(output_root).resolve()
        self.root = self.output_root/self.plan['mode']/self.plan_id[:16]
        self.max_bytes = int(max_output_gib*2**30)
        self.max_tasks, self.max_hours = max_tasks, max_hours
        self.started, self.executed, self.stopped = time.monotonic(), 0, False
        self.auto_download = auto_download
        self.download_root = self.output_root/'weights'
        self.weight_roots = list(dict.fromkeys([str(self.download_root)]+list(weight_roots or [])+['/kaggle/input']))
        env = environment()
        self.runtime = dict(cuda=env.get('cuda'), devices=env.get('devices'), versions=env['versions'])
        self.state = dict(schema_version=1, role='pipeline_results', plan_id=self.plan_id,
            plan=self.plan, tasks={}, scientific_status='development_not_gate_closure')
        self.tasks = self._tasks()
        self._verified_files = {}
        if resume_from:
            self.restore(resume_from)
        self.root.mkdir(parents=True, exist_ok=True)
        if (self.root/'pipeline-manifest.json').exists():
            saved = json.loads((self.root/'pipeline-manifest.json').read_text())
            assert saved['plan_id'] == self.plan_id
            self.state = saved
        self.state.pop('session_stop_reason', None)
        self._save()

    def _tasks(self):
        jobs = []
        def add(section, key=None, **settings):
            jobs.append(dict(section=section, key=key or section, settings=settings))
        add('00'); add('01')
        needed = list(dict.fromkeys(self.models+([] if self.smoke else ['esm2_35m'])+[self.finetune_model]
                     +([self.saprot_model] if self.structure and self.run_saprot else [])))
        for model in needed: add('02', '02-'+model, model_ids=[model])
        for model in self.models+([] if self.smoke or 'esm2_35m' in self.models else ['esm2_35m']):
            add('03', '03-'+model, model_id=model, crop=model == ('esm2_8m' if self.smoke else 'esm2_35m'))
        add('04')
        if self.smoke:
            add('05'); add('06'); add('11')
        else:
            cfg = dict(self.base, **self.overrides.get('05', {}))
            for seed in cfg['seeds']:
                for head in cfg['heads']:
                    for arm in cfg['neural_arms']:
                        add('05', f'05-{head}-{arm}-s{seed}', heads=[head], neural_arms=[arm], seeds=[seed])
            add('06')
            cfg = dict(self.base, **self.overrides.get('11', {}))
            for seed in cfg['seeds']:
                for mode in cfg['finetune_modes']:
                    for arm in cfg['finetune_arms']:
                        add('11', f'11-{mode}-{arm}-s{seed}', finetune_modes=[mode], finetune_arms=[arm], seeds=[seed])
        add('08'); add('09'); add('07')
        return jobs

    def _save(self):
        self.state['updated_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        atomic_json(self.root/'pipeline-manifest.json', self.state)

    def _record(self, job, status, **more):
        self.state['tasks'][job['key']] = dict(section=job['section'], status=status, **more)
        self._save()

    def task_path(self, key):
        record = self.state['tasks'].get(key, {})
        if record.get('status') != 'complete' or not self._files_valid(record):
            return None
        return self.root/record['path']

    def _files_valid(self, record):
        for entry in record.get('files', []):
            p = self.root/entry['path']
            if not p.is_file() or p.stat().st_size != entry['bytes']:
                return False
            token = (str(p), p.stat().st_mtime_ns, entry['bytes'], entry['sha256'])
            if token not in self._verified_files:
                self._verified_files[token] = sha256(p) == entry['sha256']
            if not self._verified_files[token]: return False
        return bool(record.get('files'))

    def _valid(self, job, signature):
        record = self.state['tasks'].get(job['key'], {})
        if record.get('status') != 'complete' or record.get('signature') != signature:
            return False
        return self._files_valid(record)

    def _budget(self):
        reason = None
        if self.max_tasks is not None and self.executed >= self.max_tasks:
            reason = 'max_tasks'
        elif self.max_hours is not None and (time.monotonic()-self.started)/3600 >= self.max_hours:
            reason = 'max_hours'
        elif size_tree(self.output_root) >= self.max_bytes:
            reason = 'max_output_gib'
        if reason:
            self.stopped = True
            self.state['session_stop_reason'] = reason
            self._save()
        return not self.stopped

    def _ensure_weights(self, model):
        try:
            return resolve_snapshot(model, self.weight_roots)
        except FileNotFoundError:
            if not self.auto_download:
                raise FileNotFoundError(f'Weights missing for {model}; enable AUTO_DOWNLOAD or attach complete weights')
        self.download_root.mkdir(parents=True, exist_ok=True)
        command = [sys.executable, '-I', str(HERE/'download_weights.py'), '--models', model,
                   '--out', str(self.download_root), '--workers', '1', '--backend', 'http']
        subprocess.run(command+['--metadata-only'], check=True)
        meta = json.loads((self.download_root/model/'status.json').read_text())
        assert meta['status'] in ('metadata_ready', 'complete'), meta.get('error', meta['status'])
        # Conservative reserve: refuse a checkpoint that cannot coexist with current output.
        if meta['bytes_expected']+size_tree(self.output_root) > self.max_bytes:
            raise MemoryError(f'{model} download exceeds MAX_OUTPUT_GIB; use a separate input asset or a larger output budget')
        if shutil.disk_usage(self.output_root).free < meta['bytes_expected']+(2<<30):
            raise MemoryError('Insufficient disk headroom for weights')
        subprocess.run(command, check=True)
        return resolve_snapshot(model, self.weight_roots)

    def _preflight(self, model):
        path = self.task_path('02-'+model)
        if not path: return None
        record = self.state['tasks']['02-'+model]
        if record.get('runtime') != self.runtime: return None
        rows = json.loads((path/'preflight.json').read_text())['models']
        return path/'preflight.json' if any(r['model_id'] == model and r['status'] == 'feasible' for r in rows) else None

    def _config(self, job):
        stage = job['section']
        cfg = dict(self.base, **self.overrides.get(stage, {}))
        cfg.update(job['settings'])
        cfg.update(weight_roots=self.weight_roots, implementation_sha256=self.code_sha)
        dependencies = []
        if stage != '00': dependencies.append('00')
        if stage == '02':
            cfg['preflight_runtime'] = self.runtime
        if stage == '03':
            model = cfg['model_id']; dependencies.append('02-'+model)
            report = self._preflight(model)
            if report: cfg['preflight_report'] = str(report)
            else: return None, dependencies, 'Model must pass preflight on current runtime'
        if stage == '04' and not self.smoke:
            cfg['pooled_features'] = {}
            for model in self.models:
                report = self._preflight(model)
                state = self.state['tasks'].get('02-'+model, {})
                if not report:
                    if state.get('outcome') == 'resource_blocked': continue
                    return None, ['02-'+model], 'Candidate eligibility has not been resolved; do not silently shrink family comparison'
                key = '03-'+model; dependencies.append(key)
                path = self.task_path(key)
                if not path: return None, dependencies, 'Features incomplete'
                cfg['pooled_features'][model] = str(path)
            if not cfg['pooled_features']: return None, dependencies, 'No feasible candidate features'
        if stage == '05' and not self.smoke:
            dependencies.append('03-esm2_35m')
            path = self.task_path('03-esm2_35m')
            if path: cfg['crop_features'] = {'esm2_35m': str(path)}
        if stage == '11':
            model = self.finetune_model; dependencies.append('02-'+model)
            cfg['finetune_model'] = model
            if not self._preflight(model): return None, dependencies, 'Fine-tuning needs feasible model preflight'
        if stage == '08': cfg['external_table'] = self.external
        if stage == '09':
            cfg.update(structure_table=self.structure, run_saprot=self.run_saprot, saprot_model=self.saprot_model)
            if self.structure and self.run_saprot:
                key = '02-'+self.saprot_model; dependencies.append(key)
                report = self._preflight(self.saprot_model)
                if report: cfg['preflight_report'] = str(report)
                else: return None, dependencies, 'SaProt structure training needs preflight'
        if stage == '07':
            # All planned development jobs must resolve before this driver reads held-source labels.
            dev = [j['key'] for j in self.tasks if j['section'] in ('01', '04', '05', '06', '11')]
            dependencies += dev
            dependencies.append(self.calibration_task)
            source = self.task_path(self.calibration_task)
            if source:
                cfg['training_output'] = str(source)
                cfg['calibration_oof_sha256'] = sha256(source/(cfg['selected_recipe']+'-oof.parquet'))
        feature_paths = {**cfg.get('pooled_features', {}), **cfg.get('crop_features', {})}
        if feature_paths:
            cfg['input_feature_sha256'] = {key: sha256(Path(path)/'feature-manifest.json') for key, path in feature_paths.items()}
        return cfg, dependencies, None

    def run_group(self, section):
        assert section in ORDER
        if section == '10': return self.aggregate() if section in self.sections else pd.DataFrame([dict(status='not_selected')])
        if section not in self.sections:
            return pd.DataFrame([dict(section=section, status='not_selected_this_session')])
        from .stages import run
        for job in [j for j in self.tasks if j['section'] == section]:
            cfg, dependencies, reason = self._config(job)
            if cfg is None or any(not self.task_path(k) for k in dependencies):
                previous = self.state['tasks'].get(job['key'], {})
                if previous.get('status') == 'complete' and self._files_valid(previous):
                    previous['session_note'] = reason or 'Dependency unavailable; previous verified outputs retained'
                    self._save()
                    continue
                self._record(job, 'waiting_dependency', reason=reason or 'Complete dependencies first', dependencies=dependencies)
                continue
            signature = identity(dict(config=cfg, data=self.ds.identity, protocol=self.protocol_sha))
            if self._valid(job, signature):
                print('CACHED', job['key'], flush=True); continue
            if self.stopped or not self._budget():
                # Preserve an existing completed record if the session budget is exhausted.
                continue
            model = (cfg['model_ids'][0] if section == '02' else cfg['model_id'] if section == '03'
                     else self.finetune_model if section == '11'
                     else self.saprot_model if section == '09' and self.structure and self.run_saprot else None)
            if model:
                try:
                    self._ensure_weights(model)
                except (FileNotFoundError, MemoryError) as exc:
                    self._record(job, 'weights_pending', reason=str(exc), runtime=self.runtime)
                    continue
            out = self.root/'tasks'/(job['key']+'-'+signature[:12])
            self._record(job, 'running', signature=signature, path=out.relative_to(self.root).as_posix())
            print('RUN', job['key'], flush=True)
            try:
                run(section, self.ds.root, out, cfg)
                files = [dict(path=p.relative_to(self.root).as_posix(), bytes=p.stat().st_size, sha256=sha256(p))
                         for p in sorted(out.rglob('*')) if p.is_file()]
                outcome = 'complete'
                if section == '02':
                    checks = json.loads((out/'preflight.json').read_text())['models']
                    outcome = 'feasible' if all(r['status'] == 'feasible' for r in checks) else 'resource_blocked'
                if section == '08' and not self.external: outcome = 'source_pending'
                if section == '09' and not self.structure: outcome = 'structure_pending'
                self._record(job, 'complete', outcome=outcome, signature=signature,
                    path=out.relative_to(self.root).as_posix(), files=files, runtime=self.runtime)
                self.executed += 1
            except Exception as exc:
                self._record(job, 'failed', error=f'{type(exc).__name__}: {exc}', signature=signature,
                             path=out.relative_to(self.root).as_posix())
                raise
            finally:
                gc.collect()
                import torch
                if torch.cuda.is_available(): torch.cuda.empty_cache()
        return self.summary().query('section == @section').reset_index(drop=True)

    def summary(self):
        return pd.DataFrame([dict(task=j['key'], section=j['section'],
            status=self.state['tasks'].get(j['key'], {}).get('status', 'pending'),
            outcome=self.state['tasks'].get(j['key'], {}).get('outcome'),
            detail=self.state['tasks'].get(j['key'], {}).get('reason', '')) for j in self.tasks])

    def aggregate(self):
        """Combine task OOF by recipe/identical cohort, retaining distinct seeds and structure coverage."""
        buckets = {}
        for job in self.tasks:
            if job['section'] not in ('01', '04', '05', '06', '09', '11'): continue
            path = self.task_path(job['key'])
            if not path: continue
            for file in sorted(path.glob('*-oof.parquet')):
                data = pd.read_parquet(file)
                assert set(data['mode']) == {self.plan['mode']} and set(data.data_identity) == {self.ds.identity}
                cohort = identity(sorted(set(data.cell_id)))
                for recipe, group in data.groupby('recipe'):
                    buckets.setdefault((recipe, cohort), []).append(group)
        rows, reports, peptide_scores = [], {}, {}
        destination = self.root/'aggregate'; destination.mkdir(exist_ok=True)
        for (recipe, cohort), pieces in buckets.items():
            data = pd.concat(pieces, ignore_index=True)
            assert not data[['cell_id', 'seed']].duplicated().any(), f'Duplicate recipe/seed OOF: {recipe}'
            cells = set(data.cell_id)
            for seed, part in data.groupby('seed'):
                assert set(part.cell_id) == cells, 'Different per-seed cohorts cannot form an ensemble'
            frame = self.ds.sat[self.ds.sat.cell_id.isin(cells)].copy()
            full = len(frame) == len(self.ds.sat)
            if not self.smoke and not full:
                assert 'cohort' in recipe, 'Incomplete full-W official OOF is not a finished experiment'
            ensemble = data.groupby('cell_id').prediction.mean().reindex(frame.cell_id).to_numpy()
            report = dict(ensemble=summarize(frame, ensemble), per_seed={str(s): summarize(
                frame, r.set_index('cell_id').prediction.reindex(frame.cell_id).to_numpy()) for s, r in data.groupby('seed')})
            key = recipe+'-'+cohort[:12]
            reports[key] = report
            peptide_scores[(recipe, cohort)] = per_peptide(frame, ensemble)
            rows.append(dict(recipe=recipe, cohort=cohort[:12], cells=len(frame),
                full_W=full, seeds=','.join(map(str, sorted(data.seed.unique()))),
                n_seeds=data.seed.nunique(), macro_mae=report['ensemble']['all']['mae']))
        contrasts = {}
        for (recipe, cohort), pp in peptide_scores.items():
            if recipe in ('ordered-w5-D', 'ordered-w5-E') and ('ordered-w5-B', cohort) in peptide_scores:
                contrasts[recipe+'-B'] = paired_ci(pp, peptide_scores[('ordered-w5-B', cohort)],
                    n_boot=100 if self.smoke else 5000, multiplicity=2)
        table = pd.DataFrame(rows)
        table.to_csv(destination/'evidence.csv', index=False)
        atomic_json(destination/'evidence.json', dict(mode=self.plan['mode'], data_identity=self.ds.identity,
            reports=reports, contrasts=contrasts, results=rows,
            note='Full W and mapped/smoke cohorts remain separate; seeds are not independent datasets. No automatic model selection from outer scores.'))
        status = self.summary()
        status.to_csv(self.root/'pipeline-status.csv', index=False)
        self.state['coverage'] = dict(planned=len(status), complete=int((status.status == 'complete').sum()),
            optional_outcomes=status.outcome.dropna().value_counts().to_dict())
        self._save()
        return table

    def export(self, include_features=False):
        """Checkpoint archive excludes pretrained weights; full directory is also a Kaggle output."""
        # Refresh coverage even if stage10 was not selected or a soft budget was reached.
        self.summary().to_csv(self.root/'pipeline-status.csv', index=False)
        self._save()
        files = [p for p in sorted(self.root.rglob('*')) if p.is_file() and
                 (include_features or p.name not in ('pool.npy', 'crop.npy'))]
        estimate = sum(p.stat().st_size for p in files)
        if size_tree(self.output_root)+estimate > self.max_bytes:
            return dict(status='archive_skipped_storage_budget', directory=str(self.root),
                note='Save the full output directory with Kaggle Save Version; no output was deleted.')
        archive = self.root.parent/(self.root.name+'-checkpoint.zip')
        index = dict(plan_id=self.plan_id, include_features=include_features,
            files=[dict(path=p.relative_to(self.root).as_posix(), sha256=sha256(p), bytes=p.stat().st_size) for p in files])
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as z:
            z.writestr('SNAPSHOT.json', json.dumps(index))
            for p in files: z.write(p, p.relative_to(self.root))
        return dict(status='exported', archive=str(archive), sha256=sha256(archive),
            include_features=include_features, note='Without feature arrays, stage03 is recomputed on ZIP restore; model/checkpoint tasks remain reusable.')

    def restore(self, source):
        source = Path(source)
        assert not self.root.exists(), 'Resume only into an empty campaign directory; existing local runs resume automatically'
        if source.is_dir():
            saved = json.loads((source/'pipeline-manifest.json').read_text())
            assert saved['plan_id'] == self.plan_id, 'Changed scientific plan/code/data: use a new campaign'
            if size_tree(source) > self.max_bytes: raise MemoryError('Resume directory exceeds MAX_OUTPUT_GIB')
            assert not any(p.is_symlink() for p in source.rglob('*')), 'Restore only self-contained trusted output directories'
            shutil.copytree(source, self.root)
        else:
            with zipfile.ZipFile(source) as z:
                index = json.loads(z.read('SNAPSHOT.json'))
                assert index['plan_id'] == self.plan_id
                assert sum(p.file_size for p in z.infolist()) <= self.max_bytes
                for info in z.infolist():
                    name = Path(info.filename)
                    assert not name.is_absolute() and '..' not in name.parts
                for entry in index['files']:
                    value = z.read(entry['path'])
                    assert hashlib.sha256(value).hexdigest() == entry['sha256']
                self.root.mkdir(parents=True)
                for entry in index['files']:
                    target = self.root/entry['path']; target.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(entry['path']) as src, target.open('wb') as dst: shutil.copyfileobj(src, dst)
