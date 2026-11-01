"""Merge stage03 feature shards with strict row/model/data/hash checks."""
import argparse
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from degron_v3.plm import merge_shards

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('shards', nargs='+', type=Path)
    args = ap.parse_args()
    print(merge_shards(args.shards, args.out))
