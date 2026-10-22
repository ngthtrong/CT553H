"""Builds a miniature `topics/degron-footprint` data tree with synthetic proteins, so that ETL and API tests run
without the research data. Real-data tests (marker `realdata`) use the actual tree instead.

Proteins (sequences are synthetic, from a fixed seed):
  P12345 (GENE1, 120 aa, 5 tiles): tile 1 in domain and a training peptide; tile 2 out of domain (PSI 4.8);
         tile 3 unreliable (reads 5); tile 4 unreliable (PSI NA); tile 5 not in the screen -> unknown.
  P22222 (GENE2, 100 aa, 4 tiles): tile 1 PSI = 4.0 / reads = 10 (in, boundary); tile 2 PSI just above 4.0 (out);
         tile 3 reads 9.99 (unreliable); tile 4 contains X (not scorable).
  O00001 (GENE3, 20 aa): no tile.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import random
from pathlib import Path

import numpy as np
import yaml

AAS = 'ACDEFGHIKLMNPQRSTVWY'


def _seq(seed: int, n: int) -> str:
    rng = random.Random(seed)
    return ''.join(rng.choice(AAS) for _ in range(n))


PROTEINS = {
    'P12345': ('GENE1', 'Synthetic protein one', _seq(1, 120)),
    'P22222': ('GENE2', 'Synthetic protein two', _seq(2, 100)),
    'O00001': ('GENE3', 'Synthetic short protein', _seq(3, 20)),
}
# tile 4 of P22222 is made non-scorable
_p2 = PROTEINS['P22222'][2]
PROTEINS['P22222'] = (PROTEINS['P22222'][0], PROTEINS['P22222'][1], _p2[:3 * 23 + 5] + 'X' + _p2[3 * 23 + 6:])

SCREEN = [
    ('P12345_GENE1_1', 50.0, 2.0), ('P12345_GENE1_2', 60.0, 4.8), ('P12345_GENE1_3', 5.0, 2.0),
    ('P12345_GENE1_4', 50.0, None),
    ('P22222_GENE2_1', 10.0, 4.0), ('P22222_GENE2_2', 10.0, 4.0000001), ('P22222_GENE2_3', 9.99, 2.0),
    ('P22222_GENE2_4', 30.0, 2.5),
    ('P12345_GENE1_6', 30.0, 2.0),          # beyond the last window -> counted as unmatched
    ('Q99999_NOGENE_1', 30.0, 2.0),         # accession not in the snapshot -> counted as unmatched
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def write_fasta(path: Path) -> None:
    with gzip.open(path, 'wt') as fh:
        for acc, (gene, name, seq) in PROTEINS.items():
            fh.write(f'>sp|{acc}|{gene}_HUMAN {name} OS=Homo sapiens OX=9606 GN={gene} PE=1 SV=1\n')
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i + 60] + '\n')


def write_screen(path: Path) -> None:
    with path.open('w') as fh:
        fh.write('peptide\treads\tpsi\n')
        for pep, reads, psi in SCREEN:
            fh.write(f"{pep}\t{reads}\t{'NA' if psi is None else psi}\n")


def write_sat(path: Path) -> np.ndarray:
    """One training peptide, tile 1 of P12345, with 500 of its 532 cells (rows follow (position, aa) order)."""
    from degron_footprint.features import feature_matrix
    seq = PROTEINS['P12345'][2][:28]
    X, cells = feature_matrix(seq)
    keep = [i for i in range(len(cells)) if i % 17 != 3]        # drop some cells: rows are a sub-sequence
    rng = np.random.default_rng(5)
    y = rng.normal(0.1, 0.5, len(keep))
    np.savez(path, X=X[keep], y=y, idx=np.array([[0, len(keep)]]), peps=np.array(['P12345_GENE1_1']),
             groups=np.array(['P12345']), rowg=np.array(['P12345'] * len(keep)),
             wtkeys=np.array(['P12345_GENE1_1']), wtvals=np.array([2.0]))
    return y


def write_model(path: Path) -> None:
    rng = np.random.default_rng(11)
    np.savez(path, coef=rng.normal(0, 0.15, 180), intercept=np.array([-0.09]), alpha=np.array([10]),
             platt_coef=np.array([3.7]), platt_intercept=np.array([-3.4]),
             iso_x=np.linspace(-1, 1.5, 20), iso_y=np.linspace(0, 0.9, 20), calibrator=np.array('platt'),
             n_peptides=np.array([1]), n_cells=np.array([500]), n_clusters=np.array([1]))


def write_results(calib: Path, curve: Path) -> None:
    calib.write_text(json.dumps({
        'n_test_cells': 100, 'n_test_peptides': 3, 'n_test_clusters': 3, 'seeds': [17, 29, 43],
        'metrics': {'platt': {'brier': 0.09, 'brier_ci95': [0.08, 0.1], 'ece': 0.016, 'bss_vs_const': 0.19,
                              'mean_pred': 0.11, 'recalibration_line': {'intercept': 0.2, 'slope': 1.0}},
                    'raw': {'brier': 0.127, 'brier_ci95': [0.118, 0.136]}},
        'utility': {'top10pct': {'enrichment': {'mean': 4.0, 'ci95': [3.7, 4.3]}, 'precision': {'mean': 0.46}}}}))
    curve.write_text(json.dumps({'results': {'ridge': {'ext': {'macro_auroc_ensemble': 0.82,
                                                              'macro_auroc_per_seed': [0.82, 0.82, 0.82]}}},
                                 'verdict': {'ridge': {'delta': 0.0126}}}))


CLINVAR_HEADER = ['#AlleleID', 'Type', 'Name', 'GeneID', 'GeneSymbol', 'ClinicalSignificance', 'LastEvaluated',
                  'ReviewStatus', 'VariationID']


def write_clinvar(path: Path) -> None:
    s1 = PROTEINS['P12345'][2]
    rows = []

    def row(vid, pos, ref, alt, sig, gene='GENE1', ev='Mar 02, 2024', rev='criteria provided, single submitter'):
        rows.append(['1', 'single nucleotide variant', f'NM_1.1({gene}):c.1A>G (p.{three(ref)}{pos}{three(alt)})', '1',
                     gene, sig, ev, rev, str(vid)])
    row(101, 5, s1[4], 'W' if s1[4] != 'W' else 'A', 'Pathogenic')
    row(102, 30, s1[29], 'W' if s1[29] != 'W' else 'A', 'Uncertain significance')
    row(103, 31, s1[30], 'W' if s1[30] != 'W' else 'A', 'Likely benign')
    row(104, 10, 'W' if s1[9] != 'W' else 'A', 'G', 'Benign')             # wrong reference residue
    row(105, 119, s1[118], 'W' if s1[118] != 'W' else 'A', 'Pathogenic')   # inside the last window of P12345
    s2 = PROTEINS['P22222'][2]
    row(111, 99, s2[98], 'W' if s2[98] != 'W' else 'A', 'Pathogenic', gene='GENE2')   # past the last window of P22222 (97)
    row(101, 5, s1[4], 'W' if s1[4] != 'W' else 'A', 'Pathogenic')         # duplicate VariationID (second assembly)
    rows.append(['1', 'deletion', 'NM_1.1(GENE1):c.1del', '1', 'GENE1', 'Pathogenic', '-', '-', '999'])
    row(106, 7, s1[6], 'W' if s1[6] != 'W' else 'A', 'Conflicting classifications of pathogenicity')
    row(107, 8, s1[7], 'W' if s1[7] != 'W' else 'A', 'Pathogenic/Likely pathogenic')
    row(108, 9, s1[8], 'W' if s1[8] != 'W' else 'A', 'Benign/Likely benign')
    row(109, 11, s1[10], 'W' if s1[10] != 'W' else 'A', 'not provided')
    row(110, 5, 'A', 'T', 'Pathogenic', gene='NOPE')                       # gene not in the snapshot
    with gzip.open(path, 'wt') as fh:
        fh.write('\t'.join(CLINVAR_HEADER) + '\n')
        for r in rows:
            fh.write('\t'.join(r) + '\n')


_THREE = {'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys', 'Q': 'Gln', 'E': 'Glu', 'G': 'Gly',
          'H': 'His', 'I': 'Ile', 'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro', 'S': 'Ser',
          'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val'}


def three(a: str) -> str:
    return _THREE[a]


def build(root: Path, *, extra_sources: list[dict] | None = None) -> dict:
    """Write the tree under root; return {'topic', 'sources', 'params', 'model_dir'}."""
    topic = root / 'topic'
    data = topic / 'data'
    for d in ('raw', 'interim', 'processed'):
        (data / d).mkdir(parents=True, exist_ok=True)
    (data / 'README.md').write_text('# synthetic data tree for tests\n')
    (topic / 'research' / 'calib').mkdir(parents=True, exist_ok=True)
    (topic / 'research' / 'curve').mkdir(parents=True, exist_ok=True)
    fasta, screen = data / 'raw/proteins.fasta.gz', data / 'interim/screen.tsv'
    sat, model = data / 'processed/sat.npz', data / 'processed/model.npz'
    clin = data / 'raw/variant_summary.txt.gz'
    calib, curve = topic / 'research/calib/results.json', topic / 'research/curve/results.json'
    write_fasta(fasta)
    write_screen(screen)
    write_sat(sat)
    write_model(model)
    write_clinvar(clin)
    write_results(calib, curve)

    def base(sid, redistrib=True, cls='open', **kw):
        return {'source_id': sid, 'name': sid, 'version': 'test', 'citation': 'test', 'url': None,
                'license_name': 'test', 'license_class': cls, 'redistribution_ok': redistrib,
                'attribution_text': f'attribution of {sid}', 'retrieved_on': '2026-10-22', **kw}
    sources = [
        base('uniprot-2026_03', files=[{'role': 'protein_fasta', 'path': 'raw/proteins.fasta.gz', 'sha256': sha256(fasta)}],
             version='release 2026_03, test'),
        base('zhang2023-geo-gse240610', files=[{'role': 'screen_psi', 'path': 'interim/screen.tsv', 'sha256': sha256(screen)}]),
        base('zhang2023-mendeley-v2', files=[{'role': 'sat_labels', 'path': 'processed/sat.npz', 'sha256': sha256(sat)}]),
        base('clinvar-2026-10-12', cls='attribution_required',
             disclaimer_text='ClinVar is not for diagnostic use (test text).',
             files=[{'role': 'clinvar_summary', 'path': 'raw/variant_summary.txt.gz', 'sha256': sha256(clin)}]),
        base('own-model', files=[
            {'role': 'model_weights', 'path': 'processed/model.npz', 'sha256': sha256(model)},
            {'role': 'model_results', 'path': '../research/calib/results.json', 'sha256': sha256(calib)},
            {'role': 'curve_results', 'path': '../research/curve/results.json', 'sha256': sha256(curve)}]),
        base('koren2018-nihms967427', redistrib=False, cls='internal_only', load=False),
        *(extra_sources or []),
    ]
    sources_path = root / 'sources.yaml'
    sources_path.write_text(yaml.safe_dump({'sources': sources}, sort_keys=False))
    params = {'screen': {'read_min': 10.0, 'psi_max': 4.0}, 'tile': {'length': 28, 'step': 23},
              'model': {'model_id': 'test-model-v1', 'weights_file': 'test-model-v1.npz',
                        'frozen_at': '2026-10-22T00:00:00+00:00', 'feature_spec': 'm3-180 (test)',
                        'event_definition': 'P(DeltaPSI >= 1.0)',
                        'domain_description': 'synthetic test domain'},
              'clinvar': {'file_date': '2026-10-12'}}
    params_path = root / 'params.yaml'
    params_path.write_text(yaml.safe_dump(params))
    return {'topic': topic, 'sources': sources_path, 'params': params_path, 'model_dir': root / 'models',
            'files': {'fasta': fasta, 'screen': screen, 'sat': sat, 'model': model, 'clinvar': clin}}
