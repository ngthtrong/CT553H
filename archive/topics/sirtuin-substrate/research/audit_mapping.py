"""Check the 149 annotated cellular sites against retrieved UniProt sequences."""
import hashlib
import json
import re
from pathlib import Path

import pandas as pd

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "DECISIONS.md").exists())
TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "log.md").exists())  # thư mục đề tài
RAW = TOPIC / "data/raw"


def main():
    tables = sorted(RAW.glob("uniprot-cellular-part*-2026-10-08.tsv"))
    if len(tables) != 2:
        raise RuntimeError("Download both UniProt query parts before running mapping audit")
    sequences = {}
    for path in tables:
        table = pd.read_csv(path, sep="\t")
        sequences.update(zip(table.Entry, table.Sequence))
    isoform = RAW / "uniprot-P06753-2.fasta"
    if isoform.exists():
        sequences["P06753-2"] = "".join(isoform.read_text().splitlines()[1:])
    data = pd.read_excel(RAW / "42004_2025_1717_MOESM16_ESM.xlsx")
    records = []
    for row in data.itertuples(index=False, name=None):
        accession, _, position, modified = row[:4]
        position = int(position)
        sequence = sequences.get(accession)
        peptide = re.sub(r"\([^)]*\)", "", modified)
        annotated_offsets = [len(re.sub(r"\([^)]*\)", "", modified[:match.start()]))
                             for match in re.finditer(r"K\([^)]*\)", modified)]
        lysine_ok = bool(sequence and 0 < position <= len(sequence) and sequence[position-1] == "K")
        peptide_ok = bool(sequence and any(
            position-1-offset >= 0 and sequence[position-1-offset:position-1-offset+len(peptide)] == peptide
            for offset in annotated_offsets))
        records.append({"accession": accession, "position": position,
                        "sequence_retrieved_for_exact_accession": sequence is not None,
                        "residue_is_K": lysine_ok,
                        "annotated_tryptic_peptide_matches_at_site": peptide_ok})
    result = {"retrieval_date": "2026-10-08", "reference": "UniProt live retrieval; not historical RefSeq v54",
              "test_rows": len(records), "sequence_accessions": len(sequences),
              "site_rows_with_sequence": sum(r["sequence_retrieved_for_exact_accession"] for r in records),
              "site_rows_residue_is_K": sum(r["residue_is_K"] for r in records),
              "site_rows_peptide_matches": sum(r["annotated_tryptic_peptide_matches_at_site"] for r in records),
              "exceptions": [r for r in records if not r["annotated_tryptic_peptide_matches_at_site"]],
              "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in tables + [isoform]}}
    output = Path(__file__).with_name("mapping-audit-results.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"exceptions", "input_sha256"}}))


if __name__ == "__main__":
    main()
