"""Source ids that the code refers to by name (they are rows of `data_source`, written by the ETL)."""
SRC_ZHANG_SAT = 'zhang2023-mendeley-v2'          # saturation labels: the model's training data
SRC_ZHANG_GEO = 'zhang2023-geo-gse240610'        # GPS peptidome screen: tier-1 domain status
CLINVAR_PREFIX = 'clinvar-'

# Sources that must never be served or loaded into a public table (db-design §6). Enforced by the ETL.
BLOCKED_SOURCE_IDS = frozenset({'koren2018-nihms967427', 'metadegron', 'elm-academic', 'larsen2025-github'})

# Shown on the model card ("not used" list, ui-design §3.5, E2E-07). The ids are exactly BLOCKED_SOURCE_IDS, so the
# page cannot disagree with what the ETL refuses to load (a unit test checks this). Reasons are taken from
# data/README.md and research/koren-s4-audit-2026-10-22/.
NOT_USED_SOURCES: tuple[dict[str, str], ...] = (
    {'source_id': 'koren2018-nihms967427',
     'name': 'Koren et al. 2018, Cell, Table S4 (C-terminal degron saturation mutagenesis)',
     'reason': 'Author manuscript outside the PMC Open Access subset, so it may be used internally only and not served. '
               'It also failed the data gate: 5 new protein clusters against the required 20, a 3-bin PSI scale '
               'against 6 bins, and 23-residue C-terminal peptides instead of 28-residue internal tiles.'},
    {'source_id': 'metadegron',
     'name': 'MetaDegron (Briefings in Bioinformatics 2024) tables and ELM-derived degron motifs',
     'reason': 'The repository has no licence and the ELM data are under an academic licence, so they are not served. '
               'Their labels are binary motif or E3 calls, not DeltaPSI, and are not converted into DeltaPSI values.'},
    {'source_id': 'elm-academic',
     'name': 'ELM database (degron motif instances)',
     'reason': 'Academic licence; used only for internal provenance checks, not served and not used for training.'},
    {'source_id': 'larsen2025-github',
     'name': 'Larsen et al. 2025, transcription-factor tiles',
     'reason': 'The repository is MIT but whether the licence covers the data files is unconfirmed (awaiting the authors), '
               'so the tiles are neither served nor used for training.'},
)
