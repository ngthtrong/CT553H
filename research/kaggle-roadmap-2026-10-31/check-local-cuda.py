"""Check installed packages, pinned data, CUDA, and one-batch ESM35 updates.

Run with the repository .venv and python -I. Writes readiness evidence only;
never launches an official job or modifies imported Kaggle checkpoints.
"""
import argparse
from datetime import datetime, timezone
import gc
from importlib import metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data/README.md').exists())
REPO = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
sys.path.insert(0, str(HERE))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=TOPIC / 'data/processed/v3-fullpsi')
    parser.add_argument('--weights', type=Path, default=HERE / 'output/weights')
    parser.add_argument('--out', type=Path, default=HERE / 'run-local-2026-11-02')
    parser.add_argument('--requirements', type=Path, default=HERE / 'requirements-local-cuda.txt',
                        help='Use requirements-local-cuda-reuse.txt when selecting the cached Torch 2.13 wheel.')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault('HF_HUB_OFFLINE', '1')
    report = dict(scope='local_readiness_only', official_jobs_started=False,
                  generated_utc=datetime.now(timezone.utc).isoformat(),
                  interpreter=str(Path(sys.executable).resolve()),
                  data_root=str(args.data.resolve()), requirements=str(args.requirements.resolve()), checks={})
    try:
        import joblib
        import numpy as np
        import pandas as pd
        import torch
        from packaging.requirements import Requirement
        from degron_v3.common import atomic_json, environment, sha256
        from degron_v3.data import Dataset
        from degron_v3.features import features
        from degron_v3.finetune import MutationRegressor
        from degron_v3.plm import Encoder, preflight
        from degron_v3.stages import audit_stage

        report['environment'] = environment()
        torch.set_num_threads(2)
        package_checks = {}
        for requirements in [HERE / 'requirements-kaggle.txt', args.requirements]:
            for line in requirements.read_text(encoding='utf8').splitlines():
                line = line.strip()
                if not line or line.startswith(('#', '-')):
                    continue
                requirement = Requirement(line)
                installed = metadata.version(requirement.name)
                assert requirement.specifier.contains(installed), (str(requirement), installed)
                package_checks[str(requirement)] = installed
        report['checks']['requirements'] = package_checks
        checked = subprocess.run([sys.executable, '-m', 'pip', 'check'],
                                 capture_output=True, text=True, check=True)
        report['checks']['pip_check'] = checked.stdout.strip()

        assert torch.cuda.is_available(), 'CUDA is unavailable in this interpreter'
        torch.cuda.init()
        torch.manual_seed(17)
        value = torch.randn(256, 256, device='cuda', requires_grad=True)
        loss = (value @ value.T).square().mean()
        loss.backward()
        assert torch.isfinite(loss) and torch.isfinite(value.grad).all()
        report['checks']['cuda'] = dict(torch_version=torch.__version__, runtime=torch.version.cuda,
            name=torch.cuda.get_device_name(0), capability=list(torch.cuda.get_device_capability(0)),
            compiled_architectures=torch.cuda.get_arch_list(),
            vram_bytes=torch.cuda.get_device_properties(0).total_memory,
            matrix_forward_backward='pass')
        del value, loss
        torch.cuda.empty_cache()
        print('PASS packages and CUDA kernels', flush=True)

        ds = Dataset(args.data)
        source_root = HERE / 'output/official/369cb2fe6a1e31e0'
        source = json.loads((source_root / 'pipeline-manifest.json').read_text(encoding='utf8'))
        assert ds.identity == source['plan']['data_identity']
        report['source_campaign_plan_id'] = source['plan_id']
        audit_stage(ds, args.out, dict(smoke=True))
        assert not ds.sat.cell_id.duplicated().any()
        split_checks = []
        for seed in [17, 29, 43]:
            for fold in range(5):
                roles = ds.role(ds.sat, fold, seed)
                assert set(roles) == {'train', 'validation', 'test'}
                groups = {role: set(ds.sat.loc[roles == role, 'group_id'])
                          for role in ['train', 'validation', 'test']}
                for left, right in [('train', 'validation'), ('train', 'test'), ('validation', 'test')]:
                    assert groups[left].isdisjoint(groups[right])
                assert np.array_equal(roles == 'test', ds.sat.outer_fold.to_numpy() == fold)
                split_checks.append(dict(seed=seed, fold=fold,
                    groups={role: len(ids) for role, ids in groups.items()}))
        scan_meta = pd.read_parquet(ds.root / 'tables/scanning-cells.parquet',
                                    columns=['group_id', 'partition'])
        dev = set(scan_meta.loc[scan_meta.partition == 'scan_dev', 'group_id'])
        held = set(scan_meta.loc[scan_meta.partition == 'scan_T', 'group_id'])
        assert dev.isdisjoint(held) and dev.isdisjoint(set(ds.sat.group_id))
        assert held.isdisjoint(set(ds.sat.group_id))
        report['checks']['data'] = dict(data_identity=ds.identity,
            manifest_files_verified=len(ds.manifest['files']), saturation_cells=len(ds.sat),
            saturation_peptides=ds.sat.peptide_id.nunique(), groups=ds.sat.group_id.nunique(),
            scanning_cells=len(scan_meta), scanning_partition_cells=scan_meta.partition.value_counts().to_dict(),
            held_source_labels_used_for_training_or_evaluation=False,
            group_disjointness='pass', splits=split_checks)
        print('PASS data identity, labels, and 15 grouped splits', flush=True)

        original_task = source['tasks']['01']
        model_name = 'ordered-w5-D-seed17-fold0.joblib'
        model_path = source_root / original_task['path'] / model_name
        entry = next(item for item in original_task['files'] if item['path'].endswith('/' + model_name))
        assert sha256(model_path) == entry['sha256']
        # Trusted generated artifact with a verified imported-manifest hash.
        ridge = joblib.load(model_path)
        sample = ds.sat[ds.sat.outer_fold == 0].head(8)
        prediction = ridge.predict(features(sample, 'ordered', 5))
        saved = pd.read_parquet(model_path.parent / 'ordered-w5-D-oof.parquet')
        expected = saved[saved.seed == 17].set_index('cell_id').prediction.reindex(sample.cell_id).to_numpy()
        difference = float(np.max(np.abs(prediction - expected)))
        assert np.allclose(prediction, expected, atol=1e-6, rtol=1e-6)
        report['checks']['ridge_artifact'] = dict(status='pass', model=str(model_path.relative_to(REPO)),
                                                 max_abs_prediction_difference=difference, rows=len(sample))
        del ridge, saved

        preflight(['esm2_35m'], [args.weights], args.out, smoke=True)
        probe = json.loads((args.out / 'preflight.json').read_text(encoding='utf8'))['models'][0]
        report['checks']['esm35_preflight'] = probe
        assert probe['status'] == 'feasible', probe
        print('PASS pinned ESM35 weights, token alignment, GPU inference', flush=True)

        roles = ds.role(ds.sat, 0, 17)
        batch = ds.sat.loc[(roles == 'train') & (ds.sat.psi_wt_sat <= 4)].head(8).copy()
        assert len(batch) == 8
        target = torch.as_tensor(batch.dpsi_mean.to_numpy(), dtype=torch.float32, device='cuda')
        diagnostics = []
        partial = source_root / source['tasks']['11-lora-B-s17']['path'] / 'esm2_35m-lora-B-17-0-inner.pt'
        partial_config = json.loads((partial.parent / 'run-manifest.json').read_text(encoding='utf8'))['config']
        assert partial_config['data_identity'] == ds.identity
        assert partial_config['finetune_model'] == 'esm2_35m'
        assert partial_config['finetune_modes'] == ['lora']
        assert partial_config['finetune_arms'] == ['B'] and partial_config['seeds'] == [17]
        report['checks']['partial_checkpoint'] = dict(path=str(partial.relative_to(REPO)), sha256=sha256(partial),
                                                     matching_model_arm_seed_and_data=True)
        for mode, resume in [('frozen', False), ('lora', False), ('lora', True)]:
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
            encoder = Encoder('esm2_35m', [args.weights], 'cuda', 'float32')
            model = MutationRegressor(encoder, mode, seed=17)
            parameters = [p for p in model.parameters() if p.requires_grad]
            optimizer = torch.optim.AdamW(parameters, lr=.0001, weight_decay=.01)
            saved_epoch = None
            if resume:
                state = torch.load(partial, map_location='cpu', weights_only=True)
                model.restore(state['learned_state'])
                optimizer.load_state_dict(state['optimizer'])
                saved_epoch = state['epoch']
                del state
            before = model.learned_state()
            model.train()
            torch.cuda.synchronize()
            started = time.perf_counter()
            prediction = model(batch)
            loss = (prediction - target).square().mean()
            assert torch.isfinite(loss)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            assert all(p.grad is None or torch.isfinite(p.grad).all() for p in parameters)
            assert any(p.grad is not None and torch.count_nonzero(p.grad).item() for p in parameters)
            torch.nn.utils.clip_grad_norm_(parameters, 1.)
            optimizer.step()
            torch.cuda.synchronize()
            elapsed = time.perf_counter() - started
            after = model.learned_state()
            changed = [name for name in before if not torch.equal(before[name], after[name])]
            assert changed and (mode != 'lora' or any('lora_' in name for name in changed))
            diagnostics.append(dict(mode=mode, resumed=resume, resumed_epoch=saved_epoch,
                batch_size=len(batch), dtype='float32', sequence_length=28,
                trainable_parameters=sum(p.numel() for p in parameters),
                changed_parameters=len(changed), changed_lora_parameters=sum('lora_' in name for name in changed),
                peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                peak_reserved_bytes=torch.cuda.max_memory_reserved(),
                single_batch_seconds=elapsed, finite_forward_backward_update='pass',
                checkpoint_written=False))
            print('PASS diagnostic', mode, 'resume', resume, flush=True)
            del model, encoder, optimizer, parameters, before, after, loss, prediction
            gc.collect()
            torch.cuda.empty_cache()
        report['checks']['training_diagnostics'] = diagnostics
        report['checks']['diagnostic_training_cell_ids'] = batch.cell_id.tolist()
        report['ready_for_esm35_training'] = True
        report['status'] = 'pass'
        report['limitations'] = [
            'One-batch diagnostics validate functionality and memory on this sample; full-run throughput is unmeasured.',
            'Local Python/OS/GPU differ from Kaggle; bitwise continuation is not guaranteed.',
            'Windows paths and raw code line-ending hashes differ; campaign resume needs explicit local configuration.',
            'External and structure experiments still require their own reviewed inputs.',
            'CNN final refit/export is a separate implementation task from environment readiness.',
        ]
        atomic_json(args.out / 'readiness.json', report)
        print('SAVED', args.out / 'readiness.json', flush=True)
    except Exception as exc:
        report.update(status='failed', ready_for_esm35_training=False,
                      error=f'{type(exc).__name__}: {exc}', traceback=traceback.format_exc())
        (args.out / 'readiness.json').write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                                        default=str) + '\n', encoding='utf8')
        raise


if __name__ == '__main__':
    main()
