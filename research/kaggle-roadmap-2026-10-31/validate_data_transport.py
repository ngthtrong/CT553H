"""Reproduce expanded Kaggle input and reject missing/corrupt/unpinned bytes."""
import gzip
import json
from pathlib import Path
import shutil
import sys
import tempfile

import nbformat

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())
sys.path.insert(0, str(HERE))
from degron_v3.common import atomic_json, sha256
from degron_v3.data import Dataset


def rejected(action, exception):
    try:
        action()
    except exception:
        return
    raise AssertionError(f'Expected {exception.__name__}')


def main():
    source = TOPIC/'data/processed/v3-fullpsi'
    baseline = Dataset(source)
    checks = ['original_gzip_bundle_verified']
    with tempfile.TemporaryDirectory(prefix='degron-v3-gzip-') as td:
        td = Path(td)
        root = td/'input/datasets/owner/degron-data-v3-fullpsi/degron-data-v3-fullpsi'
        root.mkdir(parents=True)
        for path in source.rglob('*'):
            if not path.is_file():
                continue
            dest = root/path.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if path.name == 'DATA_MANIFEST.json':
                shutil.copyfile(path, dest)
            elif path.suffix == '.gz':
                with gzip.open(path, 'rb') as stream, dest.with_suffix('').open('wb') as out:
                    shutil.copyfileobj(stream, out)
            else:
                dest.symlink_to(path)
        expanded = Dataset(root)
        assert len(expanded.decompressed_files) == 6
        assert expanded.identity == baseline.identity
        assert expanded.sat.equals(baseline.sat)
        assert expanded.scanning(True).equals(baseline.scanning(True))
        checks.append('all_6_expanded_members_same_identity_labels_splits')

        fasta = root/'references/proteins.fasta'
        with fasta.open('r+b') as stream:
            first = stream.read(1)
            stream.seek(0); stream.write(bytes([first[0] ^ 1]))
        rejected(lambda: Dataset(root), ValueError)
        with fasta.open('r+b') as stream:
            stream.write(first)
        checks.append('tampered_expanded_bytes_rejected')

        saved = fasta.with_name('saved-fasta')
        fasta.rename(saved)
        rejected(lambda: Dataset(root), FileNotFoundError)
        saved.rename(fasta)
        checks.append('missing_expanded_member_rejected')

        table = root/'tables/peptides.parquet'
        table.unlink()
        rejected(lambda: Dataset(root), FileNotFoundError)
        table.symlink_to(source/'tables/peptides.parquet')
        checks.append('missing_parquet_rejected')

        manifest = root/'DATA_MANIFEST.json'
        original = manifest.read_bytes()
        manifest.write_bytes(original+b'\n')
        rejected(lambda: Dataset(root), FileNotFoundError)
        manifest.write_bytes(original)
        checks.append('unknown_manifest_cannot_reuse_pinned_content_hashes')

        compressed = root/'references/proteins.fasta.gz'
        compressed.write_bytes(b'corrupted gzip, valid expanded file still present')
        rejected(lambda: Dataset(root), AssertionError)
        compressed.unlink()
        compressed.symlink_to(source/'references/proteins.fasta.gz')
        assert len(Dataset(root).decompressed_files) == 5
        checks += ['corrupt_gzip_cannot_fall_back_to_expanded_copy', 'mixed_gzip_and_expanded_input_verified']

        # Exercise the delivered embedded code, not just imports from this checkout.
        compressed.unlink()
        notebook = HERE/'notebooks/12-all-in-one.ipynb'
        nb = nbformat.read(notebook, as_version=4)
        namespace = {'display': lambda value: None}
        exec(nb.cells[2].source, namespace)
        namespace.update(DATA_DIR=str(root), OUTPUT_ROOT=str(td/'working'),
            INSTALL_DEPENDENCIES=False, AUTO_DOWNLOAD=False, SECTIONS=['00'])
        exec(nb.cells[4].source, namespace)
        # The bootstrap intentionally rejects an old imported runner. Remove only
        # this validator's imports before loading the freshly embedded version.
        for name in list(sys.modules):
            if name == 'degron_v3' or name.startswith('degron_v3.'):
                del sys.modules[name]
        exec(nb.cells[6].source, namespace)
        pipeline = namespace['pipeline']
        assert len(pipeline.ds.decompressed_files) == 6
        pipeline.run_group('00')
        assert pipeline.state['tasks']['00']['status'] == 'complete'
        checks.append('actual_notebook_embedded_bootstrap_and_stage00_with_expanded_input')

    atomic_json(HERE/'data-transport-validation.json', dict(status='pass',
        mode='local_CPU_transport_regression', data_identity=baseline.identity,
        notebook_sha256=sha256(notebook),
        gzip_hash_registry_sha256=sha256(HERE/'degron_v3/gzip-content-hashes.json'),
        checks=checks, kaggle_execution='not_run'))
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
