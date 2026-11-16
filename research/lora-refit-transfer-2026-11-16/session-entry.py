"""Thin launcher: existing runner first, optional supplemental analysis second."""
import importlib.util
import argparse
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').is_file())
ENTRY=ROOT/'research/kaggle-roadmap-2026-10-31/local-runner.py'


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);value=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value);return value


def main():
    started=time.time();args=sys.argv[1:];action=args[0] if args else ''
    options=argparse.ArgumentParser(add_help=False);options.add_argument('--hours',type=float,default=2)
    hours=options.parse_known_args(args)[0].hours
    sys.argv=[str(ENTRY),*args]
    result=module('existing_local_entry',ENTRY).main()
    if result:return result
    if action=='status':
        status=HERE/'koren-run-status.json'
        if status.exists():print('Supplemental Koren:',status.read_text(encoding='utf8'),flush=True)
        return 0
    if action!='run':return 0
    from degron_v3.local_campaign import latest
    campaign=latest();state=json.loads((campaign/'state.json').read_text())
    if state['jobs'].get('finalize-branch1',{}).get('status')!='complete':
        print('Koren supplemental step is queued after core completion; existing checkpoints retained.',flush=True)
        return 0
    return module('supplemental_koren',HERE/'score-koren.py').after_core(campaign,started+hours*3600 if hours else 0)


if __name__=='__main__':raise SystemExit(main())
