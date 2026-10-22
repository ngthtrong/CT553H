"""Kiểm hai mức nào cho cùng phân hoạch trên 176 peptide (base + ext4.0). Ghi partition-equivalence.json.

  .venv/bin/python -I topics/degron-footprint/research/recluster-sensitivity-2026-10-22/partition_equivalence.py
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
import numpy as np
import run, run_curve as A
rd = A.rd
peps0 = list(A.build(rd.DEGRON_PSI_MAX, 'base')[0])
pepsE = list(A.build(A.EXT_PSI_MAX, f'ext{A.EXT_PSI_MAX}')[0])
allp = peps0 + [p for p in pepsE if p not in set(peps0)]
parts = {}
for code, (desc, tsv) in run.LEVELS.items():
    m = run.load_map(tsv)
    g = [m.get(rd.accession(p), rd.accession(p)) for p in allp]
    parts[code] = frozenset(frozenset(p for p, x in zip(allp, g) if x == c) for c in set(g))
codes = list(parts)
classes = []
for c in codes:
    for cl in classes:
        if parts[cl[0]] == parts[c]:
            cl.append(c); break
    else:
        classes.append([c])
out = {'n_peptides': len(allp),
       'distinct_partitions': [{'levels': cl, 'n_groups': len(parts[cl[0]])} for cl in classes]}
(HERE / 'partition-equivalence.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(out, ensure_ascii=False))
