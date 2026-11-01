"""Execute the self-contained notebook, including a budget stop and ZIP resume."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import argparse

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from jupyter_client import AsyncKernelManager
from jupyter_client.kernelspec import KernelSpecManager

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())


def execute_direct(nb):
    """Execute actual notebook cells in IPython when sandbox disallows kernel sockets."""
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.utils.capture import capture_output
    from traitlets.config import Config
    config = Config(); config.HistoryManager.hist_file = ':memory:'
    class HeadlessShell(InteractiveShell):
        def enable_gui(self, gui=None):
            if gui not in (None, 'inline'):
                raise ValueError(f'Unexpected GUI in headless notebook validation: {gui}')
            self.active_eventloop = None
    shell = InteractiveShell.instance() if InteractiveShell.initialized() else HeadlessShell.instance(config=config)
    shell.reset(new_session=False)
    count = 0
    for cell in nb.cells:
        if cell.cell_type != 'code': continue
        count += 1; cell.execution_count = count
        with capture_output() as captured:
            result = shell.run_cell(cell.source, store_history=False)
        outputs = []
        if captured.stdout: outputs.append(nbformat.v4.new_output('stream', name='stdout', text=captured.stdout))
        if captured.stderr: outputs.append(nbformat.v4.new_output('stream', name='stderr', text=captured.stderr))
        outputs += [nbformat.v4.new_output('display_data', data=x.data, metadata=x.metadata) for x in captured.outputs]
        cell.outputs = outputs
        result.raise_error()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--engine', choices=['direct', 'nbclient'], default='direct')
    ap.add_argument('--out', type=Path, default=TOPIC/'data/processed/v3-validation/all-in-one')
    args = ap.parse_args()
    out = args.out.resolve()
    assert not (out/'working').exists(), 'Use a clean validation output before rerunning this harness'
    out.mkdir(parents=True, exist_ok=True)
    os.environ.update(OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2',
        TOKENIZERS_PARALLELISM='false', HF_HUB_OFFLINE='1', JUPYTER_RUNTIME_DIR=str(out/'runtime'),
        IPYTHONDIR=str(out/'ipython'))
    kernel_root = out/'kernels'; spec = kernel_root/'degron-v3-master'; spec.mkdir(parents=True, exist_ok=True)
    (spec/'kernel.json').write_text(json.dumps(dict(argv=[sys.executable, '-m', 'ipykernel_launcher',
        '-f', '{connection_file}', '--HistoryManager.hist_file=:memory:'],
        display_name='Degron v3 master validation', language='python')))
    ksm = KernelSpecManager(kernel_dirs=[str(kernel_root)])
    source = HERE/'notebooks/12-all-in-one.ipynb'
    checks = []
    resume = ''
    root = None
    for label, limit in [('budget-stop', 2), ('resume-all', None)]:
        nb = nbformat.read(source, as_version=4)
        nb.cells[2].source += '\n'+f'''INSTALL_DEPENDENCIES = False
AUTO_DOWNLOAD = False
OUTPUT_ROOT = {str(out/'working')!r}
DATA_DIR = {str(TOPIC/'data/processed/v3-fullpsi')!r}
MAX_NEW_TASKS = {limit!r}
RESUME_FROM = {resume!r}
OVERRIDES = {{"00": {{"reproduce_legacy": True}}}}
'''
        start = time.monotonic()
        km = AsyncKernelManager(kernel_name='degron-v3-master', kernel_spec_manager=ksm)
        client = NotebookClient(nb, km=km, timeout=1800, resources={'metadata': {'path': str(ROOT)}})
        print('EXECUTE', label, flush=True)
        status, error = 'pass', None
        try:
            if args.engine == 'direct': execute_direct(nb)
            else: client.execute()
            assert all(c.execution_count is not None for c in nb.cells if c.cell_type == 'code')
        except Exception as exc:
            status, error = 'failed', f'{type(exc).__name__}: {exc}'[-8000:]
        finally:
            if args.engine == 'nbclient': client._cleanup_kernel()
        nbformat.write(nb, out/(label+'.ipynb'))
        html, _ = HTMLExporter().from_notebook_node(nb)
        (out/(label+'.html')).write_text(html)
        checks.append(dict(run=label, status=status, seconds=round(time.monotonic()-start, 2), error=error))
        report = dict(mode='CPU_smoke_only', notebook_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            runs=checks, official_GPU='not_run', execution_engine=args.engine,
            jupyter_kernel_execution='not_run_sandbox_socket_permission' if args.engine == 'direct' else 'executed')
        (HERE/'all-in-one-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        print(label, status, flush=True)
        if error:
            print(error, flush=True); raise SystemExit(1)
        manifests = list((out/'working/smoke').glob('*/pipeline-manifest.json'))
        assert len(manifests) == 1
        root = manifests[0].parent
        state = json.loads(manifests[0].read_text())
        if label == 'budget-stop':
            assert sum(t['status'] == 'complete' for t in state['tasks'].values()) == 2
            assert state['session_stop_reason'] == 'max_tasks'
            resume = str(root.parent/(root.name+'-checkpoint.zip'))
            assert Path(resume).is_file()
            shutil.move(root, out/'first-session-directory')
        else:
            assert len(state['tasks']) == 11 and all(t['status'] == 'complete' for t in state['tasks'].values())
            assert state['tasks']['08']['outcome'] == 'source_pending'
            assert state['tasks']['09']['outcome'] == 'structure_pending'
            stream = '\n'.join(o.get('text', '') for c in nb.cells if c.cell_type == 'code' for o in c.get('outputs', []))
            assert 'CACHED 00' in stream and 'CACHED 01' in stream
            feature = root/state['tasks']['03-esm2_8m']['path']/'feature-manifest.json'
            assert json.loads(feature.read_text())['model_id'] == 'esm2_8m'
            models = list((root/state['tasks']['11']['path']).glob('*-model.pt'))
            assert len(models) == 2
            evidence = json.loads((root/'aggregate/evidence.json').read_text())
            assert any(r['recipe'] == 'esm2_8m-lora-D' for r in evidence['results'])
            report.update(tasks=11, stage_routes_including_aggregation=12, cached_tasks_on_resume=['00', '01'],
                actual_plm_smoke='ESM2-8M features and frozen/LoRA task training',
                pending_sources=['external', 'structure'], checkpoint_zip=str((root.parent/(root.name+'-checkpoint.zip')).relative_to(ROOT)),
                exported_png=str((root/'summary.png').relative_to(ROOT)))
            (HERE/'all-in-one-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    # A small ZIP omits feature arrays: reconstruct them using the original checkpoint,
    # but reuse already trained heads when the feature content identity is unchanged.
    archive = str(root.parent/(root.name+'-checkpoint.zip'))
    shutil.move(root, out/'second-session-directory')
    pipeline_type = sys.modules['degron_v3.pipeline'].Pipeline
    restored = pipeline_type(TOPIC/'data/processed/v3-fullpsi', out/'working', smoke=True,
        weight_roots=[str(TOPIC/'data/raw/plm-weights-v3')], auto_download=False,
        overrides={'00': {'reproduce_legacy': True}}, resume_from=archive)
    assert restored.task_path('03-esm2_8m') is None
    calls = []; original = restored._ensure_weights
    def checked_weights(model):
        calls.append(model); return original(model)
    restored._ensure_weights = checked_weights
    restored.run_group('03'); assert calls == ['esm2_8m']
    assert restored.task_path('03-esm2_8m')
    restored.run_group('04'); restored.run_group('11')
    assert restored.executed == 1, 'Only missing feature extraction should run; fitted models must stay cached'
    try:
        pipeline_type(TOPIC/'data/processed/v3-fullpsi', out/'working', smoke=True,
            overrides={'00': {'reproduce_legacy': False}}, resume_from=archive)
    except AssertionError:
        pass
    else:
        raise AssertionError('Changed scientific plan accepted for resume')
    restored.aggregate(); exported = restored.export()
    if 'archive' in exported: exported['archive'] = str(Path(exported['archive']).relative_to(ROOT))
    report.update(missing_feature_arrays_recomputed=True, downstream_models_reused=True,
        weights_checked_before_reextraction=True, changed_plan_resume_rejected=True, final_export=exported,
        status='pass')
    (HERE/'all-in-one-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print('PASS:12 stage routes, budget stop, verified cache and ZIP resume', flush=True)


if __name__ == '__main__':
    main()
