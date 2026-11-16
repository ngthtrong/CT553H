"""Pin existing source artifacts before refit; never rewrite historical state."""
import os
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS']:
    os.environ.setdefault(name,'2')
from pathlib import Path
import statistics
import sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').is_file())
V3=ROOT/'research/kaggle-roadmap-2026-10-31'
sys.path.insert(0,str(V3))
from degron_v3.common import atomic_json,sha256
from degron_v3.data import Dataset
from degron_v3.local_refit import read,repo_path,cohort,ids_hash


def main():
    audit=read(HERE/'environment-audit.json')
    config=read(HERE/'refit-plan.json')
    pins={};folds=[];epochs={'lora':{},'frozen':{}}
    def pin(path,expected=None):
        path=Path(path).resolve();assert path.is_relative_to(ROOT)
        row=dict(path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,sha256=sha256(path))
        if expected:
            assert row['sha256']==expected['sha256'] and row['bytes']==expected['bytes']
        pins[row['path']]=row
        return row['path']
    source=V3/'output/local'/audit['source_campaign']['id']
    assert sha256(source/'plan.json')==audit['source_campaign']['plan_sha256']
    assert sha256(source/'state.json')==audit['source_campaign']['state_sha256']
    origins={source}
    for row in audit['development_folds']['records']:
        files={Path(x['path']).name:x for x in row['files']}
        fitpath=repo_path(files['fit.json']['path']);oofpath=repo_path(files['oof.parquet']['path'])
        pin(fitpath,files['fit.json']);pin(oofpath,files['oof.parquet'])
        origins.add(fitpath.parents[2])
        fit=read(fitpath)
        folds.append(dict(job=row['job'],mode=fit['mode'],seed=fit['seed'],fold=fit['fold'],
                          selected_epoch=fit['selected_epoch'],fit=fitpath.relative_to(ROOT).as_posix(),
                          oof=oofpath.relative_to(ROOT).as_posix()))
    for origin in origins:
        pin(origin/'plan.json');pin(origin/'state.json')
    for mode in epochs:
        for seed in config['seeds']:
            selected=[x['selected_epoch'] for x in folds if x['mode']==mode and x['seed']==seed]
            assert len(selected)==5
            epochs[mode][str(seed)]=int(statistics.median(selected))
    weights=V3/'output/weights/esm2_35m';status=read(weights/'status.json')
    assert status['status']=='complete';pin(weights/'status.json')
    for file in status['files']:
        pin(weights/status['revision']/file['path'],file)
    baseline=source/'jobs/locked-transfer-w5/ordered-w5-D/held-scanning.parquet'
    oldstate=read(source/'state.json')
    record=next(x for x in oldstate['jobs']['locked-transfer-w5']['files'] if x['path'].endswith('/held-scanning.parquet'))
    pin(baseline,record)
    ds=Dataset(ROOT/config['data']);pin(ds.root/'DATA_MANIFEST.json')
    held=cohort(ds,config['expected_T'])
    lock=dict(schema_version=1,source_campaign=source.name,data_identity=ds.identity,
        epochs=epochs,folds=folds,files=sorted(pins.values(),key=lambda x:x['path']),
        W_cell_ids_sha256=ids_hash(ds.sat.cell_id),T_cell_ids_sha256=ids_hash(held.cell_id),
        w5_baseline=baseline.relative_to(ROOT).as_posix(),
        source_revision='f4640b526a778fc386273dca2d07275f9d40abec',
        policy='Read-only source subset; path relocation via audited campaign IDs; no checkpoint inheritance')
    target=HERE/'source-lock.json'
    if target.exists():
        assert read(target)==lock,'Source lock differs; review and use a new protocol/campaign'
    else:atomic_json(target,lock)
    print('SOURCE LOCK READY:',target,'folds',len(folds),'files',len(pins),'epochs',epochs)


if __name__=='__main__':main()
