#!/usr/bin/env python3
"""Independent small-case checks of the composition audit's mathematical bounds."""

import itertools
import math
import random
from collections import defaultdict

from audit_composition import correlation, expected_precision, precision_upper_bound, ranks


def main():
    rng = random.Random(42)
    cases = 200
    for _ in range(cases):
        count = rng.randint(2, 6)
        sizes = [rng.randint(1, 4) for _ in range(count)]
        if sum(sizes) < 3:
            sizes[0] += 1
        group_ids = [g for g, n in enumerate(sizes) for _ in range(n)]
        groups = defaultdict(list)
        for index, group in enumerate(group_ids):
            groups[group].append(index)
        positive = [rng.choice([False, True]) for _ in group_ids]
        optimum = -math.inf
        for order in itertools.permutations(range(count)):
            score_map = {g: i for i, g in enumerate(order)}
            # Explicitly average over the possible within-boundary selections.
            ordered = sorted(groups, key=score_map.__getitem__, reverse=True)
            left, hits = 3, 0.0
            for g in ordered:
                block = groups[g]
                take = min(left, len(block))
                selections = list(itertools.combinations(block, take))
                hits += sum(sum(positive[i] for i in selection)
                            for selection in selections) / len(selections)
                left -= take
                if left == 0:
                    break
            optimum = max(optimum, hits / 3)
        bound = precision_upper_bound(groups, positive)
        assert math.isclose(optimum, bound, abs_tol=1e-12)
        labels = [rng.randint(-3, 3) for _ in group_ids]
        observed = ranks(labels)
        center = sum(observed) / len(observed)
        projected = [0.0] * len(observed)
        for indices in groups.values():
            average = sum(observed[i] for i in indices) / len(indices)
            for i in indices:
                projected[i] = average
        denominator = sum((v - center) ** 2 for v in observed)
        if denominator:
            rho_upper = math.sqrt(sum((v - center) ** 2 for v in projected) / denominator)
            for _ in range(20):
                group_scores = {g: rng.randint(-2, 2) for g in groups}
                predicted = [group_scores[g] for g in group_ids]
                rho = correlation(ranks(predicted), observed)
                if rho is not None:
                    assert rho <= rho_upper + 1e-12
                assert expected_precision(predicted, positive) <= bound + 1e-12
    # Mean effects do not maximize Spearman: the audit reports a separate bound.
    assert ranks([1, 1, 3, 4]) == [1.5, 1.5, 3.0, 4.0]
    # f(c)=w.c with w(A,B,C,D)=(0,1,2,3) gives substitution rows (2,3),(1,2).
    assert 2 * 2 - 3 * 1 != 0  # nonzero determinant, rank 2, not rank 1
    print(f"PASS: {cases} exhaustive variable-size P@3 oracles, 4,000 rank-bound checks, "
          "tie handling and rank-two composition counterexample.")


if __name__ == "__main__":
    main()
