"""Input validation, in the order of api-spec.md §3. All failures raise DomainError with a stable code."""
from __future__ import annotations

import re

from .constants import AA_INDEX, TILE_LEN, TILE_STEP
from .errors import DomainError

ACCESSION_RE = re.compile(r'^([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$')
MODEL_ID_RE = re.compile(r'^[a-z0-9][a-z0-9.\-]{1,63}$')


def _show(ch: str) -> str:
    """A single offending character, printable and bounded; never more of the input than this."""
    if ch.isascii() and ch.isprintable() and ch != ' ':
        return f"'{ch}'"
    return f'U+{ord(ch):04X}'


def normalize_sequence(raw: object) -> str:
    """Trim, upper-case, then require exactly 28 standard amino acids."""
    if not isinstance(raw, str):
        raise DomainError('INVALID_REQUEST', 'The sequence must be a string.', 422, 'sequence')
    seq = raw.strip().upper()
    if len(seq) != TILE_LEN:
        raise DomainError('INVALID_LENGTH',
                          f'The sequence must have exactly {TILE_LEN} amino acids; it has {len(seq)}.',
                          422, 'sequence')
    for i, ch in enumerate(seq, 1):
        if ch not in AA_INDEX:
            raise DomainError(
                'INVALID_CHARACTER',
                f'Position {i} holds {_show(ch)}, which is not one of the 20 standard amino acids '
                '(A C D E F G H I K L M N P Q R S T V W Y).', 422, 'sequence')
    return seq


def check_accession(raw: object, field: str = 'uniprot_id') -> str:
    if not isinstance(raw, str) or not ACCESSION_RE.fullmatch(raw):
        raise DomainError('INVALID_REQUEST', 'The UniProt accession has an invalid format (for example P60484).',
                          422, field)
    return raw


def n_tiles(length: int) -> int:
    """Number of full 28-residue windows with step 23 (db-design §3.1)."""
    return 0 if length < TILE_LEN else (length - TILE_LEN) // TILE_STEP + 1


def tile_bounds(tile_index: int) -> tuple[int, int]:
    start = (tile_index - 1) * TILE_STEP + 1
    return start, start + TILE_LEN - 1


def tile_sequence(protein_seq: str, tile_index: int) -> str | None:
    start = (tile_index - 1) * TILE_STEP
    s = protein_seq[start:start + TILE_LEN]
    return s if tile_index >= 1 and len(s) == TILE_LEN else None


def is_scorable(seq: str) -> bool:
    return len(seq) == TILE_LEN and all(c in AA_INDEX for c in seq)


def check_tile_index(value: object, n_max: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise DomainError('INVALID_REQUEST', 'tile_index must be an integer.', 422, 'tile_index')
    if value < 1 or value > n_max:
        if n_max == 0:
            msg = f'This protein is shorter than {TILE_LEN} residues and has no tile.'
        else:
            msg = f'tile_index must be between 1 and {n_max} for this protein.'
        raise DomainError('TILE_OUT_OF_RANGE', msg, 422, 'tile_index')
    return value
