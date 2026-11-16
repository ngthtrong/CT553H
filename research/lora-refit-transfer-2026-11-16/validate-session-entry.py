"""Check launcher handoff and time budgets without launching training."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import json
import sys
import time
import uuid
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').is_file())
sys.path.insert(0,str(ROOT/'research/kaggle-roadmap-2026-10-31'))
from degron_v3 import local_campaign


def main():
    spec=importlib.util.spec_from_file_location('session_entry',HERE/'session-entry.py')
    entry=importlib.util.module_from_spec(spec);spec.loader.exec_module(entry)
    folder=HERE/'local'/('launcher-validation-'+uuid.uuid4().hex);folder.mkdir(parents=True)
    old_latest=local_campaign.latest;old_argv=sys.argv[:];calls=[]
    def fake_module(name,path):
        if name=='existing_local_entry':return SimpleNamespace(main=lambda:0)
        return SimpleNamespace(after_core=lambda campaign,deadline:(calls.append(dict(campaign=str(campaign),deadline=deadline)) or 0))
    entry.module=fake_module;local_campaign.latest=lambda:folder
    tests=[]
    try:
        for args,complete,expected in [(['run','--hours','0'],True,'unlimited'),
            (['run','--hours=0'],True,'unlimited'),(['run','--hours','2'],True,'limited'),
            (['run','--hours','0'],False,'no_supplement_when_core_paused')]:
            (folder/'state.json').write_text(json.dumps(dict(jobs={'finalize-branch1':{'status':'complete'}} if complete else {})),encoding='utf8')
            calls.clear();sys.argv=['session-entry.py',*args];started=time.time();assert entry.main()==0
            if expected=='unlimited':assert len(calls)==1 and calls[0]['deadline']==0
            elif expected=='limited':assert len(calls)==1 and started+7199<calls[0]['deadline']<time.time()+7201
            else:assert not calls
            tests.append(dict(arguments=args,expected=expected,status='pass'))
    finally:
        local_campaign.latest=old_latest;sys.argv=old_argv
    result=dict(status='pass',scope='launcher_handoff_no_training_or_inference',tests=tests)
    (HERE/'session-entry-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
