"""Exercise Git protection against real staged blobs in an isolated temp repo."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    spec = importlib.util.spec_from_file_location('branch1_guard', HERE / 'check-git-staging.py')
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    temp_root = Path(tempfile.gettempdir()).resolve()
    sandbox = tempfile.TemporaryDirectory(prefix='ct553h-git-guard-')
    root = Path(sandbox.name).resolve()
    assert root.parent == temp_root and root.name.startswith('ct553h-git-guard-')
    results = []
    try:
        subprocess.run(['git', 'init', '--quiet', str(root)], check=True, capture_output=True)
        guard.ROOT = root
        scenarios = [
            ('small_results', [('research/lora-refit-transfer-2026-11-16/results.json', 12)], True),
            ('tiny_checkpoint', [('research/lora-refit-transfer-2026-11-16/model.pt', 12)], False),
            ('checkpoint_previous', [('research/lora-refit-transfer-2026-11-16/model.pt.previous', 12)], False),
            ('raw_data', [('data/raw/example.csv', 12)], False),
            ('source_metadata', [('data/README.md', 12), ('data/raw/example/SOURCE.md', 12)], True),
            ('single_large_blob', [('large.txt', 11 * 2**20)], False),
            ('large_staged_set', [(f'part-{i}.txt', 9 * 2**20) for i in range(3)], False),
            ('forced_predictions', [('research/kaggle-roadmap-2026-10-31/output/local/demo/jobs/score/held.parquet', 12)], False),
            ('stop_file', [('research/kaggle-roadmap-2026-10-31/output/local/demo/STOP', 0)], False),
        ]
        for name, files, allowed in scenarios:
            subprocess.run(['git', 'read-tree', '--empty'], cwd=root, check=True, capture_output=True)
            for filename, length in files:
                path = root / filename
                assert path.resolve().is_relative_to(root)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'x' * length)
                subprocess.run(['git', 'add', '--', filename], cwd=root, check=True, capture_output=True)
            result = guard.inspect()
            passed = (result['status'] == 'pass') == allowed
            results.append(dict(case=name, expected_allowed=allowed, passed=passed,
                                staged_bytes=result['bytes'], reasons=result['reasons']))
            if not passed:
                raise AssertionError(results[-1])
    finally:
        # This removes only the verified directory created by this validator.
        assert root.parent == temp_root and root.name.startswith('ct553h-git-guard-')
        sandbox.cleanup()
    output = dict(status='pass', isolated_temporary_repository=True,
                  workspace_index_and_objects_untouched=True, cases=results)
    (HERE / 'git-safety-validation.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
