"""Read existing labels/cluster maps; write only the small roadmap inventory.

No data/ writes, network, model inference, training or fold assignment.
Run from the repository root with python3 -I. --check compares with inventory.json.
"""
import argparse
import hashlib
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for block in iter(lambda: fh.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def inventory():
    source = TOPIC / 'research/residue-task-derisk-2026-10-15/residue_data.py'
    spec = importlib.util.spec_from_file_location('roadmap_residue_data', source)
    rd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rd)
    data = rd.load_all(degron_psi_max=float('inf'))
    full_path = rd.INTERIM / 'protein-id30-cov80-proteome_cluster.tsv'
    full = {}
    for line in full_path.read_text().splitlines():
        group, accession = line.split('\t')[:2]
        full[accession] = group
    strata = []
    for label, low, high in [('le3', None, 3), ('gt3_le4', 3, 4),
                             ('gt4_le5', 4, 5), ('gt5', 5, None)]:
        selected = {p: v for p, v in data['sat'].items()
                    if (low is None or v['psi_wt'] > low)
                    and (high is None or v['psi_wt'] <= high)}
        n = pos = neg = eligible_pos = eligible_neg = 0
        for values in selected.values():
            ys = [sum(pair) / 2 for pair in values['cells'].values()]
            cp = sum(y >= 1 for y in ys)
            cn = sum(y <= -1 for y in ys)
            n += len(ys)
            pos += cp
            neg += cn
            eligible_pos += cp >= 3 and len(ys) - cp >= 3
            eligible_neg += cn >= 3 and len(ys) - cn >= 3
        strata.append(dict(stratum=label, peptides=len(selected), cells=n,
                           positive_ge1=pos, negative_le_minus1=neg,
                           eligible_positive_auroc_min3_per_class=eligible_pos,
                           eligible_negative_auroc_min3_per_class=eligible_neg))
    mappings = {}
    for label in ('sat', 'scan'):
        names = data[label]
        missing = [p for p in names if rd.accession(p) not in data['clusters']]
        mappings[label] = dict(
            peptides=len(names),
            cells=sum(len(v['cells']) for v in names.values()),
            missing_legacy_cluster=len(missing),
            legacy_missing_resolved_by_proteome=sum(rd.accession(p) in full for p in missing),
            missing_proteome_cluster=sum(rd.accession(p) not in full for p in names),
            strict_proteome_clusters=len({full[rd.accession(p)] for p in names
                                          if rd.accession(p) in full}),
        )
    legacy_json = TOPIC / 'research/g2-saturation-2026-10-18/results.json'
    old = json.loads(legacy_json.read_text())
    old_fold = {c: f['fold'] for f in old['folds'] for c in f['test_clusters']}
    assigned = defaultdict(set)
    for pep, value in data['sat'].items():
        if value['psi_wt'] <= 3:
            acc = rd.accession(pep)
            assigned[full[acc]].add(old_fold[data['clusters'].get(acc, acc)])
    inputs = [source, full_path, rd.CLUSTER_TSV, rd.SCAN_CSV, legacy_json,
              rd.RAW / 'human-reviewed-2026-10-12.fasta.gz']
    inputs += [rd.PROC / f'psi-{condition}.tsv'
               for condition in ('sat_a', 'sat_b', 'rep1', 'rep2')]
    return dict(
        schema_version=1, date='2026-10-31',
        status='read_only_inventory_not_a_new_training_experiment',
        saturation=dict(peptides=len(data['sat']),
                        proteins=len({rd.accession(p) for p in data['sat']}),
                        cells=sum(len(v['cells']) for v in data['sat'].values()),
                        strata=strata),
        mapping=mappings,
        legacy_base_proteome_groups=len(assigned),
        legacy_base_proteome_groups_crossing_old_folds=sum(len(v) > 1 for v in assigned.values()),
        note='Cluster inventory precedes new exact-sequence/hit union and fold assignment. '
             'Scanning counts precede new full-proteome mapping QC; no singleton imputation.',
        sources=[dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size,
                      sha256=sha256(p)) for p in inputs],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = inventory()
    target = HERE / 'inventory.json'
    if args.check:
        assert json.loads(target.read_text()) == report, 'inventory or source bytes changed'
        print('INVENTORY MATCH: labels, counts and source hashes')
    else:
        target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
        print('WROTE', target.relative_to(ROOT))
    print(json.dumps(dict(saturation=report['saturation'], mapping=report['mapping']),
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
