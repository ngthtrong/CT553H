"""Fixed numbers of the 28-residue tile model. Every one is mirrored in system/db-design.md §3."""
import math

CODE_VERSION = '0.1.0'

AAS = 'ACDEFGHIKLMNPQRSTVWY'
AA_INDEX = {a: i for i, a in enumerate(AAS)}

TILE_LEN = 28
TILE_STEP = 23
N_SUBSTITUTIONS = TILE_LEN * (len(AAS) - 1)      # 532
CONTEXT_WINDOW = 3
CONTEXT_OFFSETS = tuple(o for o in range(-CONTEXT_WINDOW, CONTEXT_WINDOW + 1) if o != 0)
N_FEATURES = 20 + 20 + 20 + 20 * len(CONTEXT_OFFSETS)      # 180

TOP_FRACTION = 0.10
TOP_K = math.ceil(TOP_FRACTION * N_SUBSTITUTIONS)           # 54

# Domain gate, from research/residue-task-derisk-2026-10-15/residue_data.py and the P0 configuration
DOMAIN_PSI_MAX = 4.0
READ_MIN = 10.0

EVENT_DEFINITION = 'P(DeltaPSI >= 1.0)'
EVIDENCE_LABEL = 'development OOF benchmark, not external validation'
DISCLAIMER_SCOPE = ('Scores are for the assay and domain on which the model was evaluated. '
                    'They are not probabilities of disease.')
DISCLAIMER_EXPORT = 'Not a probability of disease; not for diagnostic use.'
