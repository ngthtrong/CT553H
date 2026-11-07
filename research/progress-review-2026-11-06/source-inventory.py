"""Reconcile original Windows source-byte hashes without changing source files.

Only source-inventory.code.json is written. Enumerate per-file LF/CRLF forms of
the exact current source text, matching the runner's concatenation rule.
"""
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())
R = TOPIC/'research/kaggle-roadmap-2026-10-31'
plan = json.loads((R/'output/local/ef138c84579c842e/plan.json').read_text())
paths = sorted((R/'degron_v3').glob('*.py'))+[R/'local-runner.py']
options = [(p.read_bytes().replace(b'\r\n',b'\n'),
            p.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')) for p in paths]
matches = []


def search(i, state, bits):
    if i == len(paths):
        if state.hexdigest() == plan['code_sha256']:
            matches.append(bits)
        return
    for bit, payload in enumerate(options[i]):
        branch = state.copy(); branch.update(payload)
        search(i+1,branch,bits+[bit])


search(0,hashlib.sha256(),[])
assert len(matches) == 1
individual = {}
for name, key in [('EXECUTION-PROTOCOL.md','protocol_sha256'),('model-registry.json','registry_sha256')]:
    raw = (R/name).read_bytes()
    reconstructed = raw.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
    assert hashlib.sha256(reconstructed).hexdigest() == plan[key]
    individual[name] = {'actual_sha256':hashlib.sha256(raw).hexdigest(),
        'pinned_sha256':plan[key],'reconstruction':'CRLF','pinned_hash_reproduced':True}
result = {
    'generated_local':datetime.now(timezone(timedelta(hours=8))).isoformat(),
    'campaign':'ef138c84579c842e', 'pinned_code_sha256':plan['code_sha256'],
    'current_raw_code_sha256':hashlib.sha256(b''.join(p.read_bytes() for p in paths)).hexdigest(),
    'pinned_code_hash_reproduced':True,'matching_newline_assignments':len(matches),
    'per_file_newline_reconstruction':{p.relative_to(R).as_posix():['LF','CRLF'][bit] for p,bit in zip(paths,matches[0])},
    'individual_files':individual,
    'meaning':'Same current source text reproduces the pinned runtime code/protocol/registry byte hashes using original newline conventions; original sources were not modified.',
    'limit':'This checks saved source identity, not the ability to resume the original Windows CUDA runtime on Linux.',
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(HERE/'source-inventory.code.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS original code, protocol and registry hashes reconciled by newlines')
