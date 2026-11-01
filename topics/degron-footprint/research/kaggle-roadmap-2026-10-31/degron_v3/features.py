import numpy as np
from .common import AA_INDEX


def features(frame, kind='ordered', radius=5):
    """Only sequence/position/substitution inputs; no PSI/read/group/fold features."""
    n = len(frame)
    pair = np.zeros((n, 40), dtype=np.float32)
    composition = np.zeros((n, 20), dtype=np.float32)
    unordered = np.zeros((n, 20), dtype=np.float32)
    ordered = np.zeros((n, 2 * radius * 20), dtype=np.float32)
    for i, (seq, position, mutant) in enumerate(zip(frame.wt_sequence, frame.position_1based, frame.mut_aa)):
        position = int(position) - 1
        assert len(seq) == 28 and seq[position] != mutant
        pair[i, AA_INDEX[seq[position]]] = 1
        pair[i, 20 + AA_INDEX[mutant]] = 1
        for aa in seq:
            composition[i, AA_INDEX[aa]] += 1 / len(seq)
        offsets = list(range(-radius, 0)) + list(range(1, radius + 1))
        valid = sum(0 <= position + o < len(seq) for o in offsets)
        for k, offset in enumerate(offsets):
            p = position + offset
            if 0 <= p < len(seq):
                index = AA_INDEX[seq[p]]
                ordered[i, k * 20 + index] = 1
                unordered[i, index] += 1 / valid
    if kind == 'pair':
        return pair
    if kind == 'composition':
        return np.concatenate([pair, composition], 1)
    if kind == 'unordered':
        return np.concatenate([pair, composition, unordered], 1)
    if kind == 'ordered':
        return np.concatenate([pair, composition, ordered], 1)
    raise ValueError(kind)


def crop_inputs(frame, radius=7):
    indices = np.full((len(frame), 2 * radius + 1), 20, dtype=np.int64)
    for i, (seq, pos) in enumerate(zip(frame.wt_sequence, frame.position_1based)):
        for k, offset in enumerate(range(-radius, radius + 1)):
            p = int(pos) - 1 + offset
            if 0 <= p < len(seq):
                indices[i, k] = AA_INDEX[seq[p]]
    return indices, features(frame, 'composition')
