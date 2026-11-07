"""Execute all delivered notebooks in local smoke mode; never run official training."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from jupyter_client import AsyncKernelManager
from jupyter_client.kernelspec import KernelSpecManager

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=TOPIC/'data/processed/v3-validation')
    ap.add_argument('--stages', default='all')
    args = ap.parse_args(); args.out = args.out.resolve(); args.out.mkdir(parents=True, exist_ok=True)
    os.environ.update(OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2',
        TOKENIZERS_PARALLELISM='false', HF_HUB_OFFLINE='1', MPLBACKEND='Agg',
        JUPYTER_RUNTIME_DIR=str(args.out/'runtime'), IPYTHONDIR=str(args.out/'ipython'))
    kernel_root = args.out/'kernels'; spec = kernel_root/'degron-v3-local'; spec.mkdir(parents=True, exist_ok=True)
    (spec/'kernel.json').write_text(json.dumps(dict(argv=[sys.executable, '-m', 'ipykernel_launcher',
        '-f', '{connection_file}', '--HistoryManager.hist_file=:memory:'], display_name='Degron v3 validation', language='python')))
    ksm = KernelSpecManager(kernel_dirs=[str(kernel_root)])
    checks = []
    if args.stages != 'all' and (args.out/'validation.json').exists():
        checks = json.loads((args.out/'validation.json').read_text())['notebooks']
    chosen = args.stages.split(',')
    paths = sorted((HERE/'notebooks').glob('*.ipynb'), key=lambda p: 12 if p.name[:2] == '10' else int(p.name[:2]))
    for path in paths:
        stage = path.name[:2]
        if args.stages != 'all' and stage not in chosen:
            continue
        nb = nbformat.read(path, as_version=4)
        if nb.metadata.get('degron_v3', {}).get('kind') == 'all_in_one':
            continue  # Validated separately by validate_all_in_one.py, not a numbered stage runner.
        extra = {}
        if stage == '00': extra['reproduce_legacy'] = True
        if stage == '07':
            candidates = [p for p in (args.out/'results/smoke').glob('01-*') if p.is_dir()
                          and (p/'ordered-w5-D-oof.parquet').is_file()]
            extra['training_output'] = str(max(candidates, key=lambda p: p.stat().st_mtime))
        if stage == '10': extra['results_root'] = str(args.out/'results')
        # Parameters are modified only in executed validation copies, never the delivery originals.
        nb.cells[2].source += '\n'+f'CODE_DIR={str(HERE)!r}\nDATA_DIR={str(TOPIC/"data/processed/v3-fullpsi")!r}\nOUTPUT_ROOT={str(args.out/"results")!r}\nSETTINGS.update({extra!r})'
        started = time.monotonic(); status, error = 'pass', None
        print('EXECUTE', stage, flush=True)
        km = AsyncKernelManager(kernel_name='degron-v3-local', kernel_spec_manager=ksm)
        client = NotebookClient(nb, km=km, timeout=1800, resources={'metadata': {'path': str(ROOT)}})
        try:
            client.execute()
            assert all(c.get('execution_count') is not None for c in nb.cells if c.cell_type == 'code')
        except Exception as exc:
            status, error = 'failed', f'{type(exc).__name__}: {exc}'[-6000:]
        finally:
            # A supplied KernelManager is not owned/closed by nbclient automatically.
            # Without this, twelve Python/torch kernels accumulate in host RAM.
            client._cleanup_kernel()
        nbformat.write(nb, args.out/path.name)
        html, _ = HTMLExporter().from_notebook_node(nb)
        (args.out/(path.stem+'.html')).write_text(html)
        images = sum(o.get('output_type') == 'display_data' and 'image/png' in o.get('data', {})
            for c in nb.cells if c.cell_type == 'code' for o in c.get('outputs', []))
        checks = [c for c in checks if c['stage'] != stage]
        checks.append(dict(stage=stage, notebook=path.name, status=status, error=error,
            notebook_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            seconds=round(time.monotonic()-started, 2), rendered_png_outputs=images))
        checks.sort(key=lambda c: int(c['stage']))
        report = dict(mode='smoke_only', notebooks=checks, official_gpu_training='not_run',
            note='Saved executed notebooks and HTML; figure files require visual inspection separately.')
        (args.out/'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        (HERE/'notebook-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        print(stage, status, 'seconds', checks[-1]['seconds'], flush=True)
        if status == 'failed':
            print(error, flush=True); raise SystemExit(1)


if __name__ == '__main__':
    main()
