"""Read-only inventory for planning branch 1; writes only the requested report.

Does not initialize a campaign, load model weights, read T outcomes, or repair
historical paths. Inherited paths are resolved by their already pinned campaign
ID, within output/local, and checked against the original plan/file hashes.
"""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PureWindowsPath
import platform
import shutil
import statistics
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').is_file())
V3 = ROOT / 'research/kaggle-roadmap-2026-10-31'
LOCAL = V3 / 'output/local'
CAMPAIGN = LOCAL / 'ef138c84579c842e'
DATA = ROOT / 'data/processed/degron-data-v3-fullpsi'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def command(*args, input_bytes=None):
    result = subprocess.run(args, cwd=ROOT, input=input_bytes, capture_output=True, timeout=60)
    return dict(returncode=result.returncode, stdout=result.stdout.decode('utf8', 'replace').strip(),
                stderr=result.stderr.decode('utf8', 'replace').strip())


def inventory(path):
    files = [p for p in path.rglob('*') if p.is_file()] if path.exists() else []
    return dict(path=relative(path), files=len(files), bytes=sum(p.stat().st_size for p in files))


def package(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'environment-audit.json')
    args = parser.parse_args()
    import pandas as pd
    import torch

    report = dict(schema_version=1, observed_at=datetime.now().astimezone().isoformat(),
                  scope='planning inventory; no training, model inference or T-outcome analysis',
                  root=str(ROOT), python=sys.version, executable=sys.executable,
                  platform=platform.platform())
    report['audit_script_sha256'] = sha(Path(__file__))
    report['packages'] = {name: package(name) for name in [
        'torch', 'transformers', 'numpy', 'pandas', 'pyarrow', 'scipy',
        'scikit-learn', 'safetensors', 'protobuf', 'accelerate', 'sentencepiece',
        'matplotlib', 'peft', 'openpyxl']}
    report['cuda'] = dict(available=torch.cuda.is_available(), toolkit=torch.version.cuda)
    if torch.cuda.is_available():
        free, total = torch.cuda.mem_get_info()
        report['cuda'].update(device=torch.cuda.get_device_name(0),
                              capability=list(torch.cuda.get_device_capability(0)),
                              free_bytes=free, total_bytes=total)
    report['gpu_probe'] = command('nvidia-smi', '--query-gpu=name,memory.total,memory.free,driver_version',
                                  '--format=csv,noheader')
    report['disks'] = {drive: dict(zip(['total', 'used', 'free'], shutil.disk_usage(drive)))
                       for drive in sorted({ROOT.anchor, Path(sys.executable).anchor, 'C:/'})
                       if Path(drive).exists()}
    if os.name == 'nt':
        report['host'] = command('powershell', '-NoProfile', '-Command',
            "@{cpu=(Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors);"
            "ram_bytes=(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory;"
            "python_processes=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match 'python'} | "
            "Select-Object ProcessId,Name,CommandLine)} | ConvertTo-Json -Depth 4")

    report['git'] = {name: command('git', *values) for name, values in {
        'head': ['rev-parse', 'HEAD'], 'branch': ['branch', '--show-current'],
        'status': ['status', '--short'], 'objects': ['count-objects', '-vH'],
        'autocrlf': ['config', '--get', 'core.autocrlf'],
        'connectivity': ['fsck', '--connectivity-only', '--no-reflogs']}.items()}
    index = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=ROOT)
    entries = []
    for row in filter(None, index.split(b'\0')):
        metadata, raw_name = row.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        entries.append((oid.decode(), raw_name.decode('utf8'), stage.decode()))
    queried = command('git', 'cat-file', '--batch-check=%(objectname) %(objectsize)',
                      input_bytes=('\n'.join(x[0] for x in entries) + '\n').encode())
    if queried['returncode'] != 0:
        raise RuntimeError(queried)
    sizes = {line.split()[0]: int(line.split()[1]) for line in queried['stdout'].splitlines()}
    tracked = sorted([dict(path=name, bytes=sizes[oid], stage=stage) for oid, name, stage in entries],
                     key=lambda value: value['bytes'], reverse=True)
    report['git']['tracked_inventory'] = dict(files=len(tracked), bytes=sum(x['bytes'] for x in tracked),
        largest=tracked[:15], over_10_mib=[x for x in tracked if x['bytes'] > 10 * 2**20],
        model_tensor_files=[x for x in tracked if x['path'].endswith(('.pt', '.safetensors', '.pt.previous'))])
    canaries = [f'research/kaggle-roadmap-2026-10-31/output/local/0000000000000000/{name}' for name in [
        'plan.json', 'state.json', 'STOP', 'session.json', 'jobs/refit-lora-D-17/model.pt',
        'jobs/refit-lora-D-17/refit.pt.previous', 'jobs/score-held-lora-D-17/held-scanning.parquet',
        'jobs/refit-lora-D-17/fit.json', 'jobs/calibrate-final-lora-D/model-card.json',
        'jobs/aggregate-refit/results.json']]
    report['git']['ignore_canaries'] = command('git', 'check-ignore', '-v', '--no-index', '--stdin',
                                              input_bytes=('\n'.join(canaries) + '\n').encode())
    report['storage'] = [inventory(p) for p in [LOCAL, V3 / 'output/weights', V3 / 'output/official', DATA]]
    old_plan = read(CAMPAIGN / 'plan.json')
    state = read(CAMPAIGN / 'state.json')
    report['source_campaign'] = dict(id=CAMPAIGN.name, plan_sha256=sha(CAMPAIGN / 'plan.json'),
        state_sha256=sha(CAMPAIGN / 'state.json'), counts=dict(Counter(x['status'] for x in state['jobs'].values())),
        original_data_path=old_plan['config']['data'], data_identity=old_plan['data_identity'])
    implementation = b''.join(p.read_bytes() for p in sorted((V3 / 'degron_v3').glob('*.py')))
    implementation += (V3 / 'local-runner.py').read_bytes()
    current_code_hash = hashlib.sha256(implementation).hexdigest()
    report['implementation'] = dict(current_sha256=current_code_hash,
        source_sha256=old_plan['code_sha256'], matches_source=current_code_hash == old_plan['code_sha256'],
        hash_policy='sha256 of concatenated sorted degron_v3/*.py raw bytes plus local-runner.py')
    config = read(V3 / 'local-plan.json')
    latest = read(LOCAL / 'latest.json')
    report['path_checks'] = dict(configured_data=config['data'], configured_data_exists=(ROOT / config['data']).exists(),
        actual_data=relative(DATA), actual_data_exists=DATA.exists(), latest_value=latest,
        latest_path_exists=Path(latest['campaign']).exists(), original_paths_not_modified=True)
    manifest = read(DATA / 'DATA_MANIFEST.json')
    data_checks = []
    for record in manifest['files']:
        path = DATA / record['path']
        valid = path.is_file() and sha(path) == record['sha256']
        data_checks.append(dict(path=record['path'], valid=valid))
    report['data'] = dict(manifest_sha256=sha(DATA / 'DATA_MANIFEST.json'),
                         matches_source=sha(DATA / 'DATA_MANIFEST.json') == old_plan['data_identity'],
                         checks=data_checks, all_valid=all(x['valid'] for x in data_checks))
    # Counts and identifiers only: do not load held-source target columns.
    w = pd.read_parquet(DATA / 'tables/saturation-cells.parquet', columns=['cell_id', 'peptide_id', 'group_id'])
    scan = pd.read_parquet(DATA / 'tables/scanning-cells.parquet', columns=['partition', 'cell_id', 'peptide_id', 'group_id'])
    report['data']['W'] = dict(cells=len(w), peptides=w.peptide_id.nunique(), groups=w.group_id.nunique())
    report['data']['scan_T_before_rep1_filter'] = dict(cells=int((scan.partition == 'scan_T').sum()),
        peptides=scan.loc[scan.partition == 'scan_T', 'peptide_id'].nunique(),
        groups=scan.loc[scan.partition == 'scan_T', 'group_id'].nunique())

    folds, epoch_policy = [], []
    for mode in ['lora', 'frozen']:
        for seed in [17, 29, 43]:
            epochs, cell_ids = [], []
            for fold in range(5):
                job = f'tune-{mode}-D-{seed}-{fold}'
                record = state['jobs'][job]
                recorded_origin = record.get('artifact_campaign', str(CAMPAIGN))
                origin_id = PureWindowsPath(recorded_origin).name if '\\' in recorded_origin else Path(recorded_origin).name
                if len(origin_id) != 16 or any(c not in '0123456789abcdef' for c in origin_id):
                    raise ValueError(f'Invalid campaign ID: {origin_id}')
                origin = LOCAL / origin_id
                if origin != CAMPAIGN and sha(origin / 'plan.json') != record['source_plan_sha256']:
                    raise ValueError(f'Inherited source plan changed: {job}')
                item = dict(job=job, origin=origin_id, recorded_origin_exists=Path(recorded_origin).exists(),
                            status=record['status'], files=[])
                for filename in ['fit.json', 'oof.parquet']:
                    path = origin / 'jobs' / job / filename
                    pinned = next(x for x in record['files'] if x['path'] == f'jobs/{job}/{filename}')
                    valid = path.is_file() and path.stat().st_size == pinned['bytes'] and sha(path) == pinned['sha256']
                    item['files'].append(dict(path=relative(path), valid=valid, sha256=pinned['sha256'], bytes=pinned['bytes']))
                    if not valid:
                        raise ValueError(f'Source artifact differs: {path}')
                fit = read(origin / 'jobs' / job / 'fit.json')
                epochs.append(fit['selected_epoch'])
                item['selected_epoch'] = fit['selected_epoch']
                oof = pd.read_parquet(origin / 'jobs' / job / 'oof.parquet', columns=['cell_id'])
                cell_ids.extend(oof.cell_id.tolist())
                folds.append(item)
            epoch_policy.append(dict(mode=mode, seed=seed, selected_epochs=epochs, median=statistics.median(epochs),
                oof_cells=len(cell_ids), unique_oof_cells=len(set(cell_ids)),
                exact_W_coverage=len(cell_ids) == len(w) and set(cell_ids) == set(w.cell_id)))
    report['development_folds'] = dict(count=len(folds), records=folds, epoch_policy=epoch_policy)
    weights = V3 / 'output/weights/esm2_35m'
    weight_status = read(weights / 'status.json')
    snapshot = weights / weight_status['revision']
    report['weights_35m'] = dict(status=weight_status['status'], revision=weight_status['revision'],
        snapshot=relative(snapshot), files=[dict(path=x['path'], valid=(snapshot / x['path']).is_file()
        and sha(snapshot / x['path']) == x['sha256']) for x in weight_status['files']])
    baseline = CAMPAIGN / 'jobs/locked-transfer-w5/ordered-w5-D/held-scanning.parquet'
    baseline_record = next(x for x in state['jobs']['locked-transfer-w5']['files']
                           if x['path'].endswith('/held-scanning.parquet'))
    report['w5_baseline'] = dict(path=relative(baseline), valid=sha(baseline) == baseline_record['sha256'])
    report['koren'] = {relative(p): p.exists() for p in [ROOT / 'data/raw/koren-2018/NIHMS967427-supplement-11.xlsx',
                                                       ROOT / 'data/interim/koren-2018-cells.tsv']}
    report['limitations'] = [
        'CUDA availability/memory query only; no forward/backward or inference parity tested.',
        'T counts here precede rep1 QC; primary rep1 count remains pinned by the evaluation protocol.',
        'Only the requested 30 D-fold fit/OOF artifacts and W5 held predictions were hash-checked, not every historical artifact.',
        'No source-path, Git history, campaign state, or data files were changed.']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=int, allow_nan=False) + '\n', encoding='utf8')
    print(json.dumps(dict(report=str(args.output), data_valid=report['data']['all_valid'],
        folds=len(folds), epoch_policy=epoch_policy, storage=report['storage']), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
