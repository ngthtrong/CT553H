"""CLI shared by the Kaggle notebooks. Heavy training is for Kaggle, not a default local run."""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def defaults(smoke=True):
    models = json.loads((HERE / 'model-registry.json').read_text())['models']
    linear = [('ordered', 5, arm) for arm in ('A', 'B', 'C', 'D', 'E')]
    linear += [(kind, 5, arm) for kind in ('pair', 'composition', 'unordered') for arm in ('B', 'D')]
    linear += [('ordered', 3, 'B')]
    return dict(smoke=smoke, seeds=[17] if smoke else [17, 29, 43],
        alphas=[10.] if smoke else [.1, 1., 10., 100., 1000.],
        epochs=1 if smoke else 40, finetune_epochs=1 if smoke else 20,
        linear_recipes=[('ordered', 5, arm) for arm in ('B', 'D', 'E')] if smoke else linear,
        heads=['pointwise', 'cnn', 'mcnn'], neural_arms=['D'] if smoke else ['B', 'D', 'E'],
        finetune_model='esm2_35m', finetune_modes=['frozen', 'lora'],
        finetune_arms=['D'] if smoke else ['B', 'D'], finetune_batch=2 if smoke else 8,
        model_ids=['esm2_8m'] if smoke else [m['id'] for m in models if m['family'] != 'saprot'],
        model_id='esm2_8m' if smoke else 'esm2_35m', weight_roots=['/kaggle/input'],
        row_scope='sat', row_start=0, row_stop=None, crop=False, batch_size=2 if smoke else 8,
        pooled_features={}, crop_features={}, family_arms=['D'] if smoke else ['B', 'D'],
        training_output='', selected_recipe='ordered-w5-D', results_root='/kaggle/working/degron-v3',
        external_table=None, structure_table=None, reproduce_legacy=not smoke)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', required=True)
    ap.add_argument('--data', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--config', type=Path)
    ap.add_argument('--official', action='store_true')
    args = ap.parse_args()
    config = defaults(not args.official)
    if args.config:
        config.update(json.loads(args.config.read_text()))
    # Prevent resume across different code revisions, even when config names stay unchanged.
    import hashlib
    files = sorted((HERE/'degron_v3').glob('*.py'))
    config['implementation_sha256'] = hashlib.sha256(b''.join(p.read_bytes() for p in files)).hexdigest()
    from degron_v3.stages import run
    result = run(args.stage, args.data, args.out, config)
    print(result.to_string(index=False)[:8000])


if __name__ == '__main__':
    main()
