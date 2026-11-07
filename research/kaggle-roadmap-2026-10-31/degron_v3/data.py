import json
from pathlib import Path

import numpy as np
import pandas as pd
from .common import sha256


class Dataset:
    def __init__(self, root, verify=True):
        self.root = Path(root)
        self.manifest = json.loads((self.root / 'DATA_MANIFEST.json').read_text())
        assert self.manifest['schema_version'] == 3
        self.identity = sha256(self.root / 'DATA_MANIFEST.json')
        self.decompressed_files = []
        if verify:
            transport = json.loads((Path(__file__).with_name('gzip-content-hashes.json')).read_text())
            known = {f['path']: f for f in transport['files']} if transport['data_manifest_sha256'] == self.identity else {}
            for f in self.manifest['files']:
                path = self.root / f['path']
                if path.is_file():
                    assert sha256(path) == f['sha256'], f['path']
                    continue
                # Input services may expand gzip members while leaving the original
                # manifest intact. Only accept bytes pinned from the verified core
                # archive; recompression cannot reproduce arbitrary gzip headers.
                unpacked = path.with_suffix('') if path.suffix == '.gz' else None
                expected = known.get(f['path'])
                if unpacked is not None and unpacked.is_file() and expected and expected['gzip_sha256'] == f['sha256']:
                    if unpacked.stat().st_size != expected['content_bytes'] or sha256(unpacked) != expected['content_sha256']:
                        raise ValueError(f'Decompressed data checksum mismatch: {unpacked}')
                    self.decompressed_files.append(f['path'])
                    continue
                raise FileNotFoundError(
                    f'Missing manifest file: {path}. Upload the complete core data bundle. '
                    'An expanded .gz member is accepted only with a pinned content checksum '
                    'for this exact DATA_MANIFEST.json; do not disable verification.')
        self.peptides = pd.read_parquet(self.root / 'tables/peptides.parquet')
        self.sat = pd.read_parquet(self.root / 'tables/saturation-cells.parquet')
        self.wide = pd.read_parquet(self.root / 'splits/wide-outer.parquet')
        self.sat['outer_fold'] = self.sat.peptide_id.map(self.wide.set_index('peptide_id').outer_fold)
        assert self.sat.outer_fold.notna().all()

    def scanning(self, include_held=False):
        frame = pd.read_parquet(self.root / 'tables/scanning-cells.parquet')
        if not include_held:
            frame = frame[frame.partition != 'scan_T'].copy()
        return frame

    def role(self, frame, fold, seed):
        split = pd.read_parquet(self.root / f'splits/inner-seed{seed}.parquet')
        lookup = split[split.outer_fold == fold].set_index('group_id').role
        result = frame.group_id.map(lookup)
        assert result.notna().all()
        return result.to_numpy()

    def sample_smoke(self, frame, max_peptides=60):
        # Deterministic, metadata-only subset with all available folds/strata.
        selected = []
        for _, rows in frame.groupby(['outer_fold', 'psi_stratum'], observed=True):
            selected.extend(sorted(rows.peptide_id.unique())[:3])
        selected = sorted(set(selected))[:max_peptides]
        return frame[frame.peptide_id.isin(selected)].groupby('peptide_id', sort=False).head(32).copy().reset_index(drop=True)


def arm_mask(frame, arm):
    threshold = {'A': 3., 'B': 4., 'C': 5., 'D': np.inf, 'E': np.inf}[arm]
    return (frame.psi_wt_sat.to_numpy(float) <= threshold)


def balanced_weights(frame):
    counts = frame.groupby('peptide_id').size()
    peptide_strata = frame.drop_duplicates('peptide_id').groupby('psi_stratum', observed=True).size()
    w = np.asarray([1. / (counts[p] * peptide_strata[s])
                    for p, s in zip(frame.peptide_id, frame.psi_stratum)])
    return w / w.mean()
