"""Validate pinned sources and CUDA forward/backward before the local campaign."""
import os
for name,value in [('OMP_NUM_THREADS','2'),('OPENBLAS_NUM_THREADS','2'),
                   ('CUBLAS_WORKSPACE_CONFIG',':4096:8'),('HF_HUB_OFFLINE','1'),('TRANSFORMERS_OFFLINE','1')]:
    os.environ.setdefault(name,value)
import argparse
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').is_file())
sys.path.insert(0,str(ROOT/'research/kaggle-roadmap-2026-10-31'))
from degron_v3.local_refit import preflight
from degron_v3.local_control import process_lock


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=HERE/'refit-plan.json')
    parser.add_argument('--scope',choices=['core','branch1'],default='core')
    args=parser.parse_args()
    if args.scope=='branch1':
        parser.error('Full branch1 is blocked by missing Koren S4/variable-length inference; use --scope core to run available work honestly.')
    base=ROOT/'research/kaggle-roadmap-2026-10-31/output/local'
    with process_lock(base/'session.lock'):
        with process_lock(base/'worker.lock'):
            print(json.dumps(preflight(args.config),ensure_ascii=False,indent=2))
