"""Entry point for visible Windows sessions; use repository .venv, python -I."""
import argparse
import os
from pathlib import Path
import sys

os.environ.setdefault('PYTHONUTF8','1')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('HF_HUB_OFFLINE','1')
os.environ.setdefault('TRANSFORMERS_OFFLINE','1')
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf8',errors='replace',line_buffering=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    run=sub.add_parser('run');run.add_argument('--hours',type=float,default=2)
    run.add_argument('--profile',choices=['all','core','models'],default='all')
    run.add_argument('--config',type=Path,default=HERE.parent/'lora-refit-transfer-2026-11-16/refit-plan.json')
    run.add_argument('--retry-failed',action='store_true');run.add_argument('--max-jobs',type=int)
    for action in ['pause','status']:
        action_parser=sub.add_parser(action)
        action_parser.add_argument('--campaign')
        if action=='pause':
            action_parser.add_argument('--wait',action=argparse.BooleanOptionalAction,default=True)
            action_parser.add_argument('--timeout',type=float,default=300)
    work=sub.add_parser('worker');work.add_argument('--campaign',required=True);work.add_argument('--job',required=True)
    work.add_argument('--deadline',type=float,default=0)
    args=parser.parse_args()
    from degron_v3 import local_campaign as campaign
    if args.action=='run':
        if args.hours<0:parser.error('--hours must be non-negative; 0 means unlimited')
        root=campaign.run(args.config,args.hours,args.profile,args.retry_failed,args.max_jobs)
        import json
        if any(record.get('status')=='failed' for record in json.loads((root/'state.json').read_text())['jobs'].values()):
            return 2
    elif args.action=='worker':return campaign.worker(args.campaign,args.job,args.deadline)
    elif args.action=='pause':
        if args.timeout<0:parser.error('--timeout must be non-negative')
        root=campaign.resolve_campaign(args.campaign) if args.campaign else campaign.latest()
        return campaign.pause(root,args.wait,args.timeout)
    else:campaign.status(campaign.resolve_campaign(args.campaign) if args.campaign else campaign.latest())
    return 0


if __name__=='__main__':
    raise SystemExit(main())
