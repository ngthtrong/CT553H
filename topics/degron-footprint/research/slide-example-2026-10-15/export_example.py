#!/usr/bin/env python3
"""Export a measured saturation illustration; never train or change a benchmark split.

Uses the existing, audited label builder. No saturation-training split has been
recorded: the figure must not be called a training example. The current transfer
benchmark holds out the entire saturation set. Selection is lexical, with a
completeness requirement, not based on the size of an effect.
"""
import hashlib
import importlib.util
import json
import statistics
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "CLAUDE.md").exists())
TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
OUT = TOPIC / "presentation/deck-external-2026-10-16/assets"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    module = TOPIC / "research/residue-task-derisk-2026-10-15/residue_data.py"
    spec = importlib.util.spec_from_file_location("residue_data", module)
    rd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rd)
    seqs, _ = rd.load_scan_csv()
    sat = rd.build_saturation(rd.load_psi("sat_a"), rd.load_psi("sat_b"), seqs, rd.load_uniprot())
    pep = next(p for p in sorted(sat) if len(sat[p]["cells"]) >= 520)
    v = sat[pep]
    aas = "AVILMFWYSTNQCDEKRHGP"  # hydrophobic / polar / charged / special
    assert len(aas) == 20 and len(set(aas)) == 20
    cells = [{"position": pos, "aa": aa, "replicate_a_delta": a,
              "replicate_b_delta": b, "mean_delta": (a + b) / 2}
             for (pos, aa), (a, b) in v["cells"].items()]
    # First measured non-synonymous cell in lexical order; no effect-based choice.
    cell = cells[0]
    sources = [TOPIC / "data/processed/psi-sat_a.tsv", TOPIC / "data/processed/psi-sat_b.tsv",
               rd.SCAN_CSV, TOPIC / "data/raw/human-reviewed-2026-10-12.fasta.gz", module]
    j = {"peptide": pep, "sequence": v["seq"], "wt_psi": v["psi_wt"],
         "wt_references": v["wt_internal"], "aa_order": aas, "n_measured_cells": len(cells),
         "selection": "first lexical peptide with >=520 measured non-synonymous cells",
         "split_status": "measured illustration; all saturation clusters held out in current transfer benchmark; no saturation-training split recorded",
         "example_cell": cell, "cells": cells,
         "sources": [{"path": str(p.relative_to(ROOT)), "sha256": digest(p)} for p in sources]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "measured-example.json").write_text(json.dumps(j, indent=2) + "\n")

    def color(x):
        end = (42, 157, 143) if x >= 0 else (209, 73, 91)
        t = min(abs(x) / 3, 1)
        return "#" + "".join(f"{round(250 + (c - 250) * t):02x}" for c in end)

    lookup = {(c["position"], c["aa"]): c for c in cells}
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 790 650" role="img" aria-label="Measured 28 by 20 saturation matrix and position mean">',
             '<rect width="790" height="650" fill="#FAFBFC"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#15323F;font-size:13px}.mono{font-family:monospace}</style>']
    for k, aa in enumerate(aas):
        parts.append(f'<text x="{103+k*23}" y="29" text-anchor="middle" class="mono">{aa}</text>')
    parts.append('<text x="609" y="29">Mean ΔPSI</text>')
    for pos in range(1, 29):
        y = 44 + (pos - 1) * 18
        parts.append(f'<text x="83" y="{y+12}" text-anchor="end" class="mono">{pos:02} {v["seq"][pos-1]}</text>')
        vals = []
        for k, aa in enumerate(aas):
            c = lookup.get((pos, aa)); x = 92 + k * 23
            syn = aa == v["seq"][pos-1]
            fill = "#ffffff" if syn else color(c["mean_delta"]) if c else "#d5dce0"
            border = "#15323F" if syn else "#fff"
            parts.append(f'<rect x="{x}" y="{y}" width="22" height="17" fill="{fill}" stroke="{border}" stroke-width="{1.8 if syn else .5}"/>')
            if c: vals.append(c["mean_delta"])
        mean = statistics.mean(vals)
        bw = abs(mean) * 47
        bx = 618 if mean >= 0 else 618 - bw
        parts.append(f'<rect x="{bx:.2f}" y="{y+2}" width="{bw:.2f}" height="13" fill="{color(mean)}"/>')
        if pos == cell["position"]:
            x = 92 + aas.index(cell["aa"]) * 23
            parts.append(f'<rect x="{x-1}" y="{y-1}" width="24" height="19" fill="none" stroke="#386FA4" stroke-width="3"/>')
    parts.append('<line x1="618" y1="44" x2="618" y2="548" stroke="#8FA3AD"/>')
    for i in range(200):
        parts.append(f'<rect x="{130+i*2}" y="576" width="2" height="13" fill="{color(-3+6*i/199)}"/>')
    parts += ['<text x="130" y="610">−3 destabilising</text>', '<text x="320" y="610">0</text>',
              '<text x="426" y="610">+3 stabilising</text>',
              '<text x="92" y="638">Black outline: synonymous WT reference · grey: missing · measured, not predicted</text>', '</svg>']
    (OUT / "measured-matrix.svg").write_text("\n".join(parts) + "\n")
    print(json.dumps({k: j[k] for k in ("peptide", "sequence", "wt_psi", "n_measured_cells", "example_cell")}, indent=2))


if __name__ == "__main__":
    main()
