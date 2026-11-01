"""Build core v3 without modifying legacy inputs, then package it for Kaggle."""
import argparse
from collections import defaultdict
import gzip
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from degron_v3.common import AAS, SEEDS, UnionFind, atomic_json, sha256, stratum
import numpy as np
import pandas as pd

TOPIC = next(p for p in HERE.parents if (p / 'data/README.md').exists())
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
DEST = TOPIC / 'data/processed/v3-fullpsi'


def load_module():
    path = TOPIC / 'research/residue-task-derisk-2026-10-15/residue_data.py'
    spec = importlib.util.spec_from_file_location('v3_residue_source', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def table(path):
    frame = pd.read_csv(path, sep='\t')
    frame = frame[np.isfinite(frame.psi) & (frame['sum'] >= 10)]
    return frame.set_index('id').to_dict('index')


def parquet(frame, path):
    frame.to_parquet(path, index=False, compression='zstd')


def write_gzip(source, dest):
    with Path(source).open('rb') as fi, Path(dest).open('wb') as out:
        with gzip.GzipFile(filename='', mode='wb', fileobj=out, mtime=0) as fo:
            shutil.copyfileobj(fi, fo)


def protein_hits(proteins, folder, mmseqs):
    fasta = folder / 'query-proteins.fasta'
    fasta.write_text(''.join(f'>{a}\n{s}\n' for a, s in sorted(proteins.items())))
    output = folder / 'protein-hits.tsv'
    command = [mmseqs, 'easy-search', str(fasta), str(fasta), str(output),
               str(folder / 'mmseqs-tmp'), '--min-seq-id', '0.3', '-c', '0.5', '--cov-mode', '0',
               '-s', '7.5', '--max-seqs', '10000', '--threads', '2',
               '--format-output', 'query,target,pident,alnlen,qcov,tcov']
    lock = folder / 'protein-hits-input.json'
    signature = dict(fasta_sha256=sha256(fasta), command=command)
    if not output.exists() or not lock.exists() or json.loads(lock.read_text()) != signature:
        print('MMseqs protein search', len(proteins), 'proteins', flush=True)
        with (folder / 'mmseqs.log').open('w') as log:
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
        atomic_json(lock, signature)
    return output


def build(dest, mmseqs):
    rd = load_module()
    print('Loading trusted legacy label loader', flush=True)
    data = rd.load_all(degron_psi_max=float('inf'))
    assert len(data['sat']) == 235
    conditions = {c: table(rd.PROC / f'psi-{c}.tsv') for c in ('sat_a', 'sat_b', 'rep1', 'rep2')}
    proteome = {}
    full_map_path = rd.INTERIM / 'protein-id30-cov80-proteome_cluster.tsv'
    for line in full_map_path.read_text().splitlines():
        group, acc = line.split('\t')[:2]
        proteome[acc] = group
    dest.mkdir(parents=True, exist_ok=True)
    for name in ('tables', 'references', 'source-snapshots', 'splits', 'historical', 'build-audit'):
        (dest / name).mkdir(exist_ok=True)
    excluded, peptide_rows, sat_rows, scan_rows, obs_rows, ref_rows = [], [], [], [], [], []
    sat, scan = data['sat'], data['scan']
    seqs, subs = data['seqs'], data['subs']
    psi2 = {k: v['psi'] for k, v in conditions['rep2'].items()}
    rep2 = rd.build_scanning(psi2, seqs, subs, degron_psi_max=float('inf'))
    all_names = sorted(set(sat) | set(scan) | set(rep2))
    valid_names = []
    for name in all_names:
        acc = rd.accession(name)
        v = sat.get(name) or scan.get(name) or rep2.get(name)
        if acc not in proteome or acc not in data['uniprot']:
            excluded.append(dict(source_id='all', row_key=name, reason='missing_proteome_mapping'))
            continue
        if len(v['seq']) != 28 or any(a not in AAS for a in v['seq']):
            excluded.append(dict(source_id='all', row_key=name, reason='not_standard_28mer'))
            continue
        valid_names.append(name)
        psi_sat = sat[name]['psi_wt'] if name in sat else None
        peptide_rows.append(dict(peptide_id=name, accession=acc, wt_sequence=v['seq'], length=28,
            protein_start_1based=(int(name.rsplit('_', 1)[1]) - 1) * 23 + 1,
            coordinate_origin='legacy_canonical_tile_and_source_sequence',
            sequence_sha256=__import__('hashlib').sha256(v['seq'].encode()).hexdigest(),
            psi_wt_sat=psi_sat, psi_stratum=stratum(psi_sat) if psi_sat is not None else None,
            psi_wt_scan_rep1=scan.get(name, {}).get('wt'), psi_wt_scan_rep2=rep2.get(name, {}).get('wt'),
            legacy_cluster_id=data['clusters'].get(acc), proteome_cluster_id=proteome[acc],
            mapping_status='mapped', has_saturation=name in sat))
    names_set = set(valid_names)
    group_uf = UnionFind(sorted({proteome[rd.accession(p)] for p in valid_names}))
    protein_pool = {rd.accession(p): data['uniprot'][rd.accession(p)] for p in valid_names}
    hits = protein_hits(protein_pool, dest / 'build-audit', mmseqs)
    hit_edges = 0
    for line in hits.open():
        a, b, pid, length, qc, tc = line.rstrip().split('\t')
        if a != b and float(pid) >= 30 and int(length) >= 50:
            group_uf.union(proteome[a], proteome[b]); hit_edges += 1
    sequence_owner = {}
    exact_edges = 0
    def register_sequence(sequence, name):
        nonlocal exact_edges
        owner = sequence_owner.get(sequence)
        if owner is not None:
            ga, gb = proteome[rd.accession(owner)], proteome[rd.accession(name)]
            if group_uf.find(ga) != group_uf.find(gb):
                group_uf.union(ga, gb); exact_edges += 1
        else:
            sequence_owner[sequence] = name
    for row in peptide_rows:
        register_sequence(row['wt_sequence'], row['peptide_id'])
    def observation(cell, name, condition, pos, aa, reference, measured_id):
        measured = conditions[condition].get(measured_id)
        if measured is None:
            return None
        r = dict(observation_id=f'{cell}:{condition}', cell_id=cell, peptide_id=name,
                 source_id='zhang_saturation' if condition.startswith('sat') else 'zhang_scanning',
                 assay_id='zhang_gps6', condition_id='sat_halves' if condition.startswith('sat') else 'scanning_replicates_genotype_unclear',
                 replicate_id=condition, position_1based=pos, mut_aa=aa,
                 psi_mut=measured['psi'], psi_wt=reference, dpsi=measured['psi'] - reference,
                 read_sum=measured['sum'], qc_status='reads_ge10',
                 **{f'nb{i}': measured[f'nb{i}'] for i in range(1, 7)})
        obs_rows.append(r)
        return r
    for name, v in sat.items():
        assert name in names_set, f'Saturation core unexpectedly excluded: {name}'
        for half, tag in [('a', 'sat_a'), ('b', 'sat_b')]:
            synonymous = [f'{name}_mut{i}{a.lower()}' for i, a in enumerate(v['seq'], 1)
                          if f'{name}_mut{i}{a.lower()}' in conditions[tag]]
            assert len(synonymous) >= 10
            ref_rows.append(dict(wt_reference_id=f'{name}:{tag}', peptide_id=name,
                source_id='zhang_saturation', replicate_id=tag, estimator='median_synonymous',
                psi_wt=v['wt_internal'][half], n_synonymous=len(synonymous),
                member_ids=json.dumps(synonymous)))
        for (pos, aa), (da, db) in v['cells'].items():
            cell = f'sat:{name}:{pos}:{aa}'
            a = observation(cell, name, 'sat_a', pos, aa, v['wt_internal']['a'], f'{name}_mut{pos}{aa.lower()}')
            b = observation(cell, name, 'sat_b', pos, aa, v['wt_internal']['b'], f'{name}_mut{pos}{aa.lower()}')
            assert a is not None and b is not None
            assert abs(a['dpsi'] - da) < 1e-12 and abs(b['dpsi'] - db) < 1e-12
            mutant = v['seq'][:pos - 1] + aa + v['seq'][pos:]
            register_sequence(mutant, name)
            sat_rows.append(dict(cell_id=cell, peptide_id=name, position_1based=pos,
                wt_aa=v['seq'][pos - 1], mut_aa=aa, mutant_sequence=mutant,
                dpsi_a=da, dpsi_b=db, dpsi_mean=(da + db) / 2,
                psi_mut_a=a['psi_mut'], psi_mut_b=b['psi_mut'], reads_a=a['read_sum'], reads_b=b['read_sum'],
                wt_reference_id_a=f'{name}:sat_a', wt_reference_id_b=f'{name}:sat_b',
                replicate_disagreement=abs(da - db), source_id='zhang_saturation', assay_id='zhang_gps6'))
    for name in sorted((set(scan) | set(rep2)) & names_set):
        v = scan.get(name) or rep2[name]
        for tag, source in [('rep1', scan), ('rep2', rep2)]:
            if name in source:
                ref_rows.append(dict(wt_reference_id=f'{name}:{tag}', peptide_id=name,
                    source_id='zhang_scanning', replicate_id=tag, estimator='measured_mut0',
                    psi_wt=source[name]['wt'], n_synonymous=1, member_ids=json.dumps([f'{name}_mut0'])))
        cells = set(scan.get(name, {}).get('cells', {})) | set(rep2.get(name, {}).get('cells', {}))
        for pos in sorted(cells):
            mutant = subs.get((name, pos))
            if mutant is None or len(mutant) != 28 or sum(a != b for a, b in zip(v['seq'], mutant)) != 1:
                excluded.append(dict(source_id='scanning', row_key=f'{name}:{pos}', reason='not_exact_single_substitution'))
                continue
            aa = mutant[pos - 1]
            if aa not in AAS or aa == v['seq'][pos - 1]:
                continue
            cell = f'scan:{name}:{pos}:{aa}'
            ob = {}
            for tag, source in [('rep1', scan), ('rep2', rep2)]:
                if pos in source.get(name, {}).get('cells', {}):
                    ob[tag] = observation(cell, name, tag, pos, aa, source[name]['wt'], f'{name}_mut{pos}')
            da = ob.get('rep1', {}).get('dpsi'); db = ob.get('rep2', {}).get('dpsi')
            register_sequence(mutant, name)
            scan_rows.append(dict(cell_id=cell, peptide_id=name, position_1based=pos,
                wt_aa=v['seq'][pos - 1], mut_aa=aa, mutant_sequence=mutant,
                dpsi_rep1=da, dpsi_rep2=db, dpsi_rep12_mean=(da + db) / 2 if da is not None and db is not None else None,
                availability_mask=int(da is not None) + 2 * int(db is not None),
                reads_rep1=ob.get('rep1', {}).get('read_sum'), reads_rep2=ob.get('rep2', {}).get('read_sum'),
                wt_reference_id_rep1=f'{name}:rep1' if da is not None else None,
                wt_reference_id_rep2=f'{name}:rep2' if db is not None else None,
                scan_pair=v['seq'][pos - 1] + aa, source_id='zhang_scanning', assay_id='zhang_gps6'))
    peptides = pd.DataFrame(peptide_rows)
    peptides['group_id'] = peptides.proteome_cluster_id.map(lambda g: 'G-' + group_uf.find(g))
    sat_frame, scan_frame = pd.DataFrame(sat_rows), pd.DataFrame(scan_rows)
    assert len(sat_frame) == 122412 and len(sat_frame.peptide_id.unique()) == 235
    assert not sat_frame.cell_id.duplicated().any() and not scan_frame.cell_id.duplicated().any()
    indexed = peptides.set_index('peptide_id')
    for frame in (sat_frame, scan_frame):
        for col in ('group_id', 'wt_sequence', 'psi_wt_sat', 'psi_stratum', 'accession'):
            frame[col] = frame.peptide_id.map(indexed[col])
    # Greedy deterministic grouped folds balance stratum counts and cell counts using metadata only.
    sat_peptides = peptides[peptides.has_saturation].copy()
    group_counts = pd.crosstab(sat_peptides.group_id, sat_peptides.psi_stratum).reindex(
        columns=['le3', 'gt3_le4', 'gt4_le5', 'gt5'], fill_value=0)
    assert len(group_counts) >= 5
    order = sorted(group_counts.index, key=lambda g: (-group_counts.loc[g].sum(), g))
    loads = np.zeros((5, 4)); assignment = {}
    scale = np.maximum(group_counts.sum(axis=0).to_numpy(), 1)
    for group in order:
        vec = group_counts.loc[group].to_numpy()
        scores = []
        for f in range(5):
            candidate = loads.copy(); candidate[f] += vec
            scores.append(float(np.square(candidate / scale).sum()))
        f = min(range(5), key=lambda k: (scores[k], loads[k].sum(), k))
        assignment[group] = f; loads[f] += vec
    wide = sat_peptides[['peptide_id', 'group_id', 'psi_stratum']].copy()
    wide['outer_fold'] = wide.group_id.map(assignment).astype(int)
    parquet(wide, dest / 'splits/wide-outer.parquet')
    # Entirely disjoint scanning groups are split before any supervised scanning use.
    sat_groups = set(wide.group_id)
    parts = []
    for _, row in peptides.iterrows():
        g = row.group_id
        value = int(__import__('hashlib').sha256(('scan-partition-v3:' + g).encode()).hexdigest()[:8], 16)
        partition = 'sat_overlap' if g in sat_groups else 'scan_T' if value % 5 == 0 else 'scan_dev'
        parts.append(dict(peptide_id=row.peptide_id, group_id=g, partition=partition))
    partitions = pd.DataFrame(parts)
    partition_by_group = dict(zip(partitions.group_id, partitions.partition))
    parquet(partitions, dest / 'splits/scanning-partitions.parquet')
    scan_frame['partition'] = scan_frame.peptide_id.map(partitions.set_index('peptide_id').partition)
    all_groups = sorted(set(peptides.group_id))
    for seed in SEEDS:
        rows = []
        for fold in range(5):
            allowed = [g for g in all_groups if assignment.get(g) != fold and
                       partition_by_group[g] != 'scan_T']
            # Hold ~20% by group. Validation IDs are common to all data arms/model families.
            rng = np.random.default_rng(seed + fold * 1009)
            shuffled = list(rng.permutation(sorted(g for g in allowed if g in sat_groups)))
            val = set(shuffled[:max(1, len(shuffled) // 5)])
            for g in all_groups:
                partition = 'scan_T' if partition_by_group[g] == 'scan_T' else None
                role = 'held_source' if partition else 'test' if assignment.get(g) == fold else 'validation' if g in val else 'train'
                rows.append(dict(group_id=g, outer_fold=fold, seed=seed, role=role))
        parquet(pd.DataFrame(rows), dest / f'splits/inner-seed{seed}.parquet')
    for name, frame in [('peptides', peptides), ('saturation-cells', sat_frame), ('scanning-cells', scan_frame),
                        ('observations', pd.DataFrame(obs_rows)), ('wt-references', pd.DataFrame(ref_rows)),
                        ('exclusion-log', pd.DataFrame(excluded))]:
        parquet(frame, dest / f'tables/{name}.parquet')
    seq_table = pd.DataFrame([dict(sequence_id='S-' + __import__('hashlib').sha256(s.encode()).hexdigest(), sequence=s)
                              for s in sorted(sequence_owner)])
    parquet(seq_table, dest / 'tables/sequence-table.parquet')
    for condition in conditions:
        write_gzip(rd.PROC / f'psi-{condition}.tsv', dest / f'source-snapshots/psi-{condition}.tsv.gz')
    sequence_map = pd.DataFrame([dict(peptide_id=p, wt_sequence=seqs.get(p)) for p in sorted(seqs)])
    sequence_map.to_csv(dest / 'source-snapshots/scanning-sequence-map.tsv.gz', sep='\t', index=False)
    shutil.copyfile(rd.RAW / 'human-reviewed-2026-10-12.fasta.gz', dest / 'references/proteins.fasta.gz')
    for source, name in [(rd.CLUSTER_TSV, 'clusters-legacy-cov80.tsv'), (full_map_path, 'clusters-proteome-cov80.tsv'),
                         (rd.INTERIM / 'protein-id30-cov50_cluster.tsv', 'clusters-cov50.tsv')]:
        shutil.copyfile(source, dest / 'references' / name)
    historical = [('g2-saturation-2026-10-18/results.json', 'g2-reference.json'),
                  ('learning-curve-2026-10-22/results.json', 'p0-reference.json'),
                  ('r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json', 'r6-reference.json')]
    for source, name in historical:
        shutil.copyfile(TOPIC / 'research' / source, dest / 'historical' / name)
    for source, name in [('learning-curve-sat-base.npz', 'legacy-base.npz'),
                         ('learning-curve-sat-ext4.0.npz', 'legacy-ext4.npz')]:
        shutil.copyfile(rd.PROC / source, dest / 'historical' / name)
    shutil.copyfile(TOPIC / 'research/g2-saturation-2026-10-18/results.json', dest / 'splits/legacy-outer.json')
    audit = dict(status='pass', protein_hit_edges=hit_edges, exact_sequence_union_edges=exact_edges,
        protein_hit_rule='MMseqs2 id>=0.30 cov50 bidirectional alnlen>=50 on used canonical proteins',
        saturation_groups=int(wide.group_id.nunique()), saturation_peptides=235, saturation_cells=len(sat_frame),
        scan_cells=len(scan_frame), scanning_partition_counts=partitions.groupby('partition').size().to_dict(),
        folds=wide.groupby(['outer_fold', 'psi_stratum']).size().unstack(fill_value=0).to_dict('index'),
        note='Full-proteome cov80 plus local cov50 hits and exact WT/mutant unions. Still heuristic homology control.')
    atomic_json(dest / 'splits/cross-split-audit.json', audit)
    sources = [rd.SCAN_CSV, rd.RAW / 'human-reviewed-2026-10-12.fasta.gz', rd.CLUSTER_TSV, full_map_path]
    sources += [rd.PROC / f'psi-{c}.tsv' for c in conditions]
    source_manifest = [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p), bytes=p.stat().st_size) for p in sources]
    atomic_json(dest / 'build-audit/source-manifest.json', source_manifest)
    (dest / 'README.md').write_text('# Degron v3 full-PSI\n\nZhang2023 experimental labels (CC BY 4.0) and UniProt sequences/derived clusters (CC BY 4.0).\n'
        'Source DOI: https://doi.org/10.17632/32h94v2yv2.2\n'
        'Mutation-effect reporter task; development CV, not independent clinical validation.\n'
        'Saturation PSI(WT) is metadata, never an input feature. See manifests and split audit.\n')
    files = package_files(dest)
    manifest = dict(schema_version=3, bundle_id='degron-data-v3-fullpsi', role='core_data',
        builder_sha256=sha256(Path(__file__)), scientific_status='development_data_not_new_experimental_measurements',
        audit=audit, files=[dict(path=p.relative_to(dest).as_posix(), bytes=p.stat().st_size, sha256=sha256(p),
                                license='CC BY 4.0', source='Zhang2023_or_UniProt_derived') for p in files])
    atomic_json(dest / 'DATA_MANIFEST.json', manifest)
    return manifest


def package_files(dest):
    # Runtime logs can contain machine-specific absolute paths. Keep them locally,
    # but do not put them into the portable scientific data bundle.
    excluded = {'DATA_MANIFEST.json', 'mmseqs.log', 'protein-hits-input.json'}
    return [p for p in sorted(dest.rglob('*')) if p.is_file() and 'mmseqs-tmp' not in p.parts
            and p.name not in excluded]


def finalize_existing(dest):
    """Repackage this implementation session's draft bundle, without reclustering."""
    manifest = json.loads((dest / 'DATA_MANIFEST.json').read_text())
    for source, name in [('learning-curve-sat-base.npz', 'legacy-base.npz'),
                         ('learning-curve-sat-ext4.0.npz', 'legacy-ext4.npz')]:
        shutil.copyfile(TOPIC / 'data/processed' / source, dest / 'historical' / name)
    manifest['builder_sha256'] = sha256(Path(__file__))
    manifest['files'] = [dict(path=p.relative_to(dest).as_posix(), bytes=p.stat().st_size, sha256=sha256(p),
                            license='CC BY 4.0', source='Zhang2023_or_UniProt_derived')
                         for p in package_files(dest)]
    atomic_json(dest / 'DATA_MANIFEST.json', manifest)
    return manifest


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, default=DEST)
    ap.add_argument('--mmseqs', default=shutil.which('mmseqs'))
    ap.add_argument('--finalize-draft', action='store_true', help='Finalize the current-session draft v3 package only')
    args = ap.parse_args()
    if (args.out / 'DATA_MANIFEST.json').exists() and not args.finalize_draft:
        raise FileExistsError('Dataset already built; use a new --out for changed data/code')
    assert args.finalize_draft or args.mmseqs, 'MMseqs2 required for strict grouped package'
    manifest = finalize_existing(args.out) if args.finalize_draft else build(args.out, args.mmseqs)
    packages = TOPIC / 'data/processed/packages'; packages.mkdir(exist_ok=True)
    target = packages / 'degron-data-v3-fullpsi.zip'
    if target.exists() and not args.finalize_draft:
        raise FileExistsError('ZIP already exists; preserve old package or choose a new version')
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=5) as z:
        z.write(args.out / 'DATA_MANIFEST.json', 'degron-data-v3-fullpsi/DATA_MANIFEST.json')
        for entry in manifest['files']:
            z.write(args.out / entry['path'], 'degron-data-v3-fullpsi/' + entry['path'])
    (target.with_suffix('.zip.sha256')).write_text(f'{sha256(target)}  {target.name}\n')
    atomic_json(HERE / 'dataset-build.json', dict(zip=str(target.relative_to(ROOT)), bytes=target.stat().st_size,
                                                sha256=sha256(target), **manifest['audit']))
    print('BUILT', target, target.stat().st_size, flush=True)


if __name__ == '__main__':
    main()
