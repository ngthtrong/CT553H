#!/usr/bin/env python3
"""Audit scanning labels and optimistic bounds for composition-only predictors.

No model fitting. Oracles use the evaluated labels and are NOT test performance.
Protein clusters, if supplied, must come from full-length sequences, not 28-mers.
"""

import argparse
import csv
import hashlib
import io
import json
import math
import random
import re
import statistics
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


ROOT = next(p for p in Path(__file__).resolve().parents if (p / "DECISIONS.md").exists())
TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "log.md").exists())  # thư mục đề tài
PATTERN = re.compile(r"^(?P<peptide>.+)_mut(?P<position>\d+)$")
READ_MIN = 10
PSI_MAX = 3.0
RESCUE_DELTA = 1.0
MIN_POSITIONS = 21
K = 3
REPLACEMENT = dict.fromkeys("AGVLISTCDE", "R")
REPLACEMENT.update(dict.fromkeys("MWFP", "S"))
REPLACEMENT.update(dict.fromkeys("YNQKRH", "A"))


def ranks(values):
    ordered = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    start = 0
    while start < len(ordered):
        end = start + 1
        while end < len(ordered) and values[ordered[end]] == values[ordered[start]]:
            end += 1
        rank = (start + 1 + end) / 2
        for index in ordered[start:end]:
            result[index] = rank
        start = end
    return result


def correlation(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    xx = sum((v - mx) ** 2 for v in x)
    yy = sum((v - my) ** 2 for v in y)
    if not xx or not yy:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(xx * yy)


def expected_precision(scores, positive, k=K):
    """Uniform random tie-breaking; never resolve a tie with the outcome label."""
    blocks = defaultdict(list)
    for score, label in zip(scores, positive):
        blocks[score].append(label)
    remaining, hits = k, 0.0
    for score in sorted(blocks, reverse=True):
        labels = blocks[score]
        take = min(remaining, len(labels))
        hits += take * sum(labels) / len(labels)
        remaining -= take
        if remaining == 0:
            break
    return hits / k


def precision_upper_bound(groups, positive, k=K):
    """Exact maximum expected P@k over scores constant within each group.

The top k consists of full groups followed by at most one partial group.
For each candidate partial group, knapsack finds the best full groups.
All cross-group ties can be replaced by some strict group ordering without
decreasing the maximum expected number of positives.
"""
    counts = [(len(indices), sum(positive[i] for i in indices))
              for indices in groups.values()]
    best = 0.0
    for boundary, (size, hits) in enumerate(counts):
        dp = [-math.inf] * (k + 1)
        dp[0] = 0.0
        for index, (other_size, other_hits) in enumerate(counts):
            if index == boundary:
                continue
            for used in range(k, other_size - 1, -1):
                dp[used] = max(dp[used], dp[used - other_size] + other_hits)
        for used, full_hits in enumerate(dp):
            take = k - used
            if 0 <= take <= size and math.isfinite(full_hits):
                best = max(best, full_hits + take * hits / size)
    return best / k


def summary(values):
    values = sorted(v for v in values if v is not None and math.isfinite(v))
    if not values:
        return {"n": 0}
    return {"n": len(values), "mean": statistics.mean(values),
            "median": statistics.median(values),
            "p25": values[len(values) // 4], "p75": values[3 * len(values) // 4],
            "min": values[0], "max": values[-1]}


def peptide_metrics(peptide, sequence, wildtype, mutants, group_by="pair"):
    positions = sorted(mutants)
    values = [mutants[p][0] - wildtype for p in positions]
    positive = [v >= RESCUE_DELTA for v in values]
    groups = defaultdict(list)
    wild_identity_groups = defaultdict(list)
    for index, position in enumerate(positions):
        original = sequence[position - 1]
        replacement = mutants[position][1][position - 1]
        key = original + ">" + replacement if group_by == "pair" else original
        groups[key].append(index)
        wild_identity_groups[original].append(index)
    mean_values = [0.0] * len(values)
    mean_ranks = [0.0] * len(values)
    observed_ranks = ranks(values)
    repeated_ranges = []
    mixed_groups = 0
    for indices in groups.values():
        mean_value = statistics.mean(values[i] for i in indices)
        mean_rank = statistics.mean(observed_ranks[i] for i in indices)
        for index in indices:
            mean_values[index] = mean_value
            mean_ranks[index] = mean_rank
        if len(indices) >= 2:
            repeated_ranges.append(max(values[i] for i in indices)
                                   - min(values[i] for i in indices))
            labels = {positive[i] for i in indices}
            mixed_groups += len(labels) == 2
    residual_ss = sum((a - b) ** 2 for a, b in zip(values, mean_values))
    total_ss = sum((a - statistics.mean(values)) ** 2 for a in values)
    rank_ss = sum((v - statistics.mean(observed_ranks)) ** 2 for v in observed_ranks)
    projected_rank_ss = sum((v - statistics.mean(observed_ranks)) ** 2 for v in mean_ranks)
    upper = math.sqrt(min(1.0, projected_rank_ss / rank_ss)) if rank_ss else None
    return {
        "peptide": peptide, "protein": peptide.split("_")[0],
        "positions": len(positions), "wildtype_psi": wildtype,
        "rescue_positions": sum(positive),
        "footprint": wildtype <= PSI_MAX and len(positions) >= MIN_POSITIONS and any(positive),
        "repeated_pair_groups": len(repeated_ranges),
        "max_within_pair_range": max(repeated_ranges, default=0.0),
        "pair_groups_range_ge1": sum(v >= 1.0 for v in repeated_ranges),
        "mixed_rescue_pair_groups": mixed_groups,
        "wild_identity_groups_with_multiple_targets": sum(
            len({mutants[positions[i]][1][positions[i] - 1] for i in indices}) > 1
            for indices in wild_identity_groups.values()),
        "pair_oracle_mse": residual_ss / len(values),
        "pair_residual_fraction": residual_ss / total_ss if total_ss else None,
        "pair_mean_oracle_spearman": correlation(ranks(mean_values), observed_ranks),
        "pair_rankmean_oracle_spearman": correlation(ranks(mean_ranks), observed_ranks),
        "pair_spearman_relaxed_upper": upper,
        "pair_mean_oracle_p3": expected_precision(mean_values, positive),
        "pair_p3_exact_expected_upper": precision_upper_bound(groups, positive),
        "unrestricted_p3_upper": min(K, sum(positive)) / K,
        "random_p3": sum(positive) / len(positive),
    }


def aggregate(rows):
    fields = ["max_within_pair_range", "pair_oracle_mse", "pair_residual_fraction",
              "pair_mean_oracle_spearman", "pair_rankmean_oracle_spearman",
              "pair_spearman_relaxed_upper", "pair_mean_oracle_p3",
              "pair_p3_exact_expected_upper", "unrestricted_p3_upper", "random_p3"]
    proteins = Counter(row["protein"] for row in rows)
    return {"peptides": len(rows), "proteins_by_accession": len(proteins),
            "peptides_per_protein": summary(list(proteins.values())),
            "largest_protein_share": max(proteins.values(), default=0) / len(rows) if rows else None,
            "with_same_pair_range_ge1": sum(r["pair_groups_range_ge1"] > 0 for r in rows),
            "with_mixed_rescue_pair_group": sum(r["mixed_rescue_pair_groups"] > 0 for r in rows),
            "metrics": {field: summary([row[field] for row in rows]) for field in fields}}


def split_counts(library, footprints, mapping):
    groups = sorted(set(mapping.values()))
    outputs = []
    for seed in (0, 42, 87, 1001, 12345):
        shuffled = groups.copy()
        random.Random(seed).shuffle(shuffled)
        cut1, cut2 = int(len(shuffled) * .8), int(len(shuffled) * .9)
        by_split = {"train": set(shuffled[:cut1]), "validation": set(shuffled[cut1:cut2]),
                    "test": set(shuffled[cut2:])}
        record = {"seed": seed}
        for name, group_set in by_split.items():
            entries = [p for p in library if mapping.get(p.split("_")[0]) in group_set]
            fps = [p for p in footprints if mapping.get(p.split("_")[0]) in group_set]
            record[name] = {"groups": len(group_set), "library_peptides": len(entries),
                            "footprint_peptides": len(fps),
                            "footprint_proteins": len({p.split("_")[0] for p in fps})}
        outputs.append(record)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path,
                        default=TOPIC / "data/raw/I28 Scanning Mutagenesis.zip")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("composition-audit.json"))
    parser.add_argument("--processed", type=Path,
                        default=TOPIC / "data/processed")
    parser.add_argument("--clusters", type=Path, help="MMseqs cluster TSV: representative, member")
    args = parser.parse_args()
    args.processed.mkdir(parents=True, exist_ok=True)
    wildtypes, all_sequences, mutants = {}, {}, defaultdict(dict)
    library, lengths, transitions = set(), Counter(), Counter()
    total_rows = usable_rows = 0
    with zipfile.ZipFile(args.archive) as archive:
        members = [n for n in archive.namelist() if n.endswith("Replicate 1.csv") and not n.startswith("__MACOSX/")]
        if len(members) != 1:
            raise ValueError(f"Expected one replicate-1 CSV, got {members}")
        member = members[0]
        with archive.open(member) as handle:
            reader = csv.DictReader(io.TextIOWrapper(handle, encoding="utf-8-sig", newline=""))
            for row in reader:
                total_rows += 1
                match = PATTERN.fullmatch(row["Gene"])
                if not match:
                    raise ValueError(f"Unparsed identifier {row['Gene']}")
                peptide, position = match["peptide"], int(match["position"])
                sequence = row["AA.Seq"].upper().strip()
                library.add(peptide)
                lengths[len(sequence)] += 1
                if position == 0:
                    if peptide in all_sequences and all_sequences[peptide] != sequence:
                        raise ValueError(f"Conflicting wildtype sequence: {peptide}")
                    all_sequences[peptide] = sequence
                try:
                    psi, reads = float(row["PSI"]), float(row["Sum"])
                except (ValueError, TypeError):
                    continue
                if not math.isfinite(psi) or reads < READ_MIN:
                    continue
                usable_rows += 1
                if position == 0:
                    wildtypes[peptide] = psi
                else:
                    if position in mutants[peptide]:
                        raise ValueError(f"Duplicate mutant: {peptide} {position}")
                    mutants[peptide][position] = (psi, sequence)
    mismatches = []
    scheme_exceptions = Counter()
    for peptide, mutations in mutants.items():
        if peptide not in all_sequences:
            continue
        original = all_sequences[peptide]
        for position, (_, mutated) in mutations.items():
            if len(original) != len(mutated) or not 1 <= position <= len(original):
                mismatches.append([peptide, position, "length_or_position"])
                continue
            changed = [i + 1 for i, (a, b) in enumerate(zip(original, mutated)) if a != b]
            a, b = original[position - 1], mutated[position - 1]
            transitions[a + ">" + b] += 1
            if changed != [position]:
                mismatches.append([peptide, position, changed, a, b])
            if REPLACEMENT.get(a) != b:
                scheme_exceptions[f"{position}:{a}>{b}"] += 1
    if mismatches:
        raise ValueError(f"Scanning mutation scheme mismatch: {mismatches[:10]}")
    rows = [peptide_metrics(p, all_sequences[p], psi, mutants[p])
            for p, psi in sorted(wildtypes.items()) if mutants[p]]
    footprints = [row for row in rows if row["footprint"]]
    footprint_ids = {r["peptide"] for r in footprints}
    wild_identity_rows = [peptide_metrics(p, all_sequences[p], psi, mutants[p], "wild_identity")
                          for p, psi in sorted(wildtypes.items()) if mutants[p]]
    with (args.processed / "composition-peptides.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.processed / "protein-accessions.txt").write_text(
        "\n".join(sorted({p.split("_")[0] for p in library})) + "\n")
    mapping = {p.split("_")[0]: p.split("_")[0] for p in library}
    result = {
        "source": {"doi": "10.17632/32h94v2yv2.2", "archive": args.archive.name,
                   "sha256": hashlib.sha256(args.archive.read_bytes()).hexdigest(), "member": member},
        "definitions": {"reads_min": READ_MIN, "wildtype_psi_max": PSI_MAX,
                        "rescue_delta": RESCUE_DELTA, "min_positions": MIN_POSITIONS,
                        "precision_k": K, "ties": "expected uniform random tie-breaking",
                        "oracles": "evaluated labels used; optimistic bounds, not learned performance",
                        "spearman_upper": "Cauchy-Schwarz relaxation sqrt(SS_projected_ranks/SS_ranks)",
                        "group": "within peptide, identical wildtype AND replacement amino acids",
                        "p3_upper": "exact expected maximum over within-peptide substitution-pair-constant scores",
                        "noise": "no subtraction of measurement noise; single replicate, genotype unclear"},
        "counts": {"rows": total_rows, "usable_rows": usable_rows,
                   "library_peptides": len(library), "library_proteins_by_accession": len(mapping),
                   "sequence_lengths": dict(lengths), "mutation_scheme_mismatches": len(mismatches),
                   "wildtype_peptides_with_terminal_stop": sum(s.endswith("*") for s in all_sequences.values()),
                   "footprint_peptides_with_terminal_stop": sum(
                       all_sequences[p].endswith("*") for p in footprint_ids),
                   "observed_amino_acid_lengths": dict(Counter(len(s.removesuffix("*"))
                                                               for s in all_sequences.values())),
                   "standard_scheme_exceptions": dict(sorted(scheme_exceptions.items())),
                   "transitions": dict(sorted(transitions.items()))},
        "all_usable": aggregate(rows), "footprints": aggregate(footprints),
        "wild_identity_only_diagnostic": {
            "warning": "Not a composition bound when the replacement differs across positions",
            "footprints": aggregate([r for r in wild_identity_rows if r["footprint"]]),
        },
        "protein_disjoint_80_10_10": split_counts(library, {r["peptide"] for r in footprints}, mapping),
    }
    if args.clusters:
        with args.clusters.open() as handle:
            mapping = {member: representative for representative, member in csv.reader(handle, delimiter="\t")}
        covered = {p for p in library if p.split("_")[0] in mapping}
        fp_ids = {r["peptide"] for r in footprints}
        result["full_protein_cluster_source"] = {
            "file": args.clusters.name, "sha256": hashlib.sha256(args.clusters.read_bytes()).hexdigest(),
            "library_peptides_covered": len(covered), "library_peptides_missing": len(library - covered),
            "footprint_peptides_covered": len(fp_ids & covered),
            "footprint_peptides_missing": len(fp_ids - covered),
            "clusters": len(set(mapping.values())),
            "note": "Missing full-length sequences excluded, not assigned independent singleton clusters",
        }
        result["cluster_disjoint_80_10_10"] = split_counts(library, fp_ids, mapping)
        fasta = args.processed / "proteins-full.fasta"
        if fasta.exists():
            reference, accession, pieces = {}, None, []
            for line in fasta.read_text().splitlines():
                if line.startswith(">"):
                    if accession is not None:
                        reference[accession] = "".join(pieces)
                    accession, pieces = line[1:].split()[0], []
                else:
                    pieces.append(line.strip())
            if accession is not None:
                reference[accession] = "".join(pieces)
            exact = {p for p, seq in all_sequences.items()
                     if p.split("_")[0] in reference
                     and seq.removesuffix("*") in reference[p.split("_")[0]]}
            result["current_reference_qc"] = {
                "fasta_sha256": hashlib.sha256(fasta.read_bytes()).hexdigest(),
                "library_wildtype_peptides_exactly_contained": len(exact),
                "footprints_exactly_contained": len(fp_ids & exact),
                "footprints_mapped_but_not_exact": len((fp_ids & covered) - exact),
                "terminal_stop": "One terminal * removed for reference containment; mutation rows unchanged",
                "note": "Historical library versus current canonical sequence; mismatches need curation",
            }
            result["cluster_disjoint_exact_reference_subset_80_10_10"] = split_counts(
                exact, fp_ids & exact, mapping)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"counts": result["counts"], "footprints": result["footprints"]}, indent=2))


if __name__ == "__main__":
    main()
