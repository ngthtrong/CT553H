"""Validation of uploaded experimental observations (UC-09; FR-28/29/36; api-spec §6). Implementation plan WP6.

Pure functions: bytes in, rows + issues + counts out. Nothing here executes file content, builds a path or SQL from it,
or touches the reference tables; an import is comparison data only and is never used to retrain the model (D-8).
"""
from __future__ import annotations

import csv
import email.parser
import email.policy
import hashlib
import io
import json
import math
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from degron_footprint.errors import DomainError

AA = frozenset('ACDEFGHIKLMNPQRSTVWY')
REQUIRED = ('peptide_id', 'wt_sequence', 'position', 'wt_aa', 'mut_aa', 'observed_value', 'replicate_id')
OPTIONAL = ('missing_reason', 'uniprot_id', 'reference_release', 'start_pos')
MAPPING = ('uniprot_id', 'reference_release', 'start_pos')
META_REQUIRED = ('name', 'assay', 'endpoint', 'units', 'source', 'reference_description', 'compatibility')
META_OPTIONAL = ('assay_version', 'rights_note')
MAX_ISSUES = 500
FORMULA = re.compile(r'^[=+\-@\t\r]')
INT = re.compile(r'^[0-9]{1,6}$')
DPSI_ENDPOINTS = {'deltapsi', 'dpsi', 'δpsi'}
DPSI_UNITS = {'psi', 'psiunits', 'deltapsi', 'dpsi', 'δpsi'}


def _norm(text: str) -> str:
    return re.sub(r'[^0-9a-zδ]', '', text.lower())


@dataclass
class Report:
    rows: list[dict] = field(default_factory=list)
    issues: list[dict] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=lambda: dict.fromkeys(
        ('rows', 'valid', 'missing', 'duplicate', 'conflicting', 'rejected', 'warnings', 'mapping_verified',
         'mapping_unverified'), 0))
    suffix: str = '.csv'
    issues_truncated: int = 0

    def issue(self, severity: str, code: str, message: str, row: int | None = None) -> None:
        if severity == 'warning':
            self.counts['warnings'] += 1
        if len(self.issues) >= MAX_ISSUES:
            self.issues_truncated += 1
            return
        item: dict[str, Any] = {'severity': severity, 'code': code, 'message': message}
        if row is not None:
            item['row'] = row
        self.issues.append(item)

    @property
    def committable(self) -> bool:
        return not any(i['severity'] == 'error' for i in self.issues) and self.counts['rejected'] == 0 \
            and self.counts['duplicate'] == 0 and self.counts['conflicting'] == 0 and self.counts['valid'] > 0

    def issue_list(self) -> list[dict]:
        if not self.issues_truncated:
            return self.issues
        return [*self.issues, {'severity': 'warning', 'code': 'ISSUES_TRUNCATED',
                               'message': f'{self.issues_truncated} further issues are counted but not listed.'}]


# --- multipart ------------------------------------------------------------------------------------------------------

def parse_multipart(body: bytes, content_type: str) -> dict[str, bytes]:
    """multipart/form-data → {field name: bytes}, with the standard library (no file name is ever used as a path)."""
    if not content_type.lower().startswith('multipart/form-data') or 'boundary=' not in content_type:
        raise DomainError('INVALID_REQUEST', 'Send multipart/form-data with the fields "file" and "metadata".', 422)
    msg = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(
        b'Content-Type: ' + content_type.encode('latin-1') + b'\r\nMIME-Version: 1.0\r\n\r\n' + body)
    if not msg.is_multipart():
        raise DomainError('INVALID_REQUEST', 'The multipart body could not be read.', 422)
    out: dict[str, bytes] = {}
    for part in msg.iter_parts():
        name = part.get_param('name', header='content-disposition')
        if isinstance(name, str) and name in ('file', 'metadata') and name not in out:
            payload = part.get_payload(decode=True)
            out[name] = payload if isinstance(payload, bytes) else b''
    if 'file' not in out or 'metadata' not in out:
        raise DomainError('INVALID_REQUEST', 'Both "file" and "metadata" fields are required.', 422)
    return out


def parse_metadata(raw: bytes) -> dict[str, Any]:
    try:
        meta = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        raise DomainError('IMPORT_INVALID', '"metadata" must be a JSON object.', 422, 'metadata') from None
    if not isinstance(meta, dict):
        raise DomainError('IMPORT_INVALID', '"metadata" must be a JSON object.', 422, 'metadata')
    unknown = set(meta) - set(META_REQUIRED) - set(META_OPTIONAL)
    if unknown:
        raise DomainError('IMPORT_INVALID', 'metadata has a field that is not part of the interface.', 422, 'metadata')
    for key in META_REQUIRED:
        value = meta.get(key)
        if not isinstance(value, str) or not value.strip():
            raise DomainError('IMPORT_INVALID', f'metadata.{key} is required.', 422, f'metadata.{key}')
    for key in (*META_REQUIRED, *META_OPTIONAL):
        if key in meta and (not isinstance(meta[key], str) or len(meta[key]) > (200 if key == 'name' else 2000)):
            raise DomainError('IMPORT_INVALID', f'metadata.{key} must be text of bounded length.', 422,
                              f'metadata.{key}')
    if meta['compatibility'] not in ('zhang_gps_dpsi', 'other'):
        raise DomainError('IMPORT_INVALID', 'metadata.compatibility must be "zhang_gps_dpsi" or "other".', 422,
                          'metadata.compatibility')
    return {k: meta[k].strip() for k in (*META_REQUIRED, *META_OPTIONAL) if k in meta}


# --- rows -----------------------------------------------------------------------------------------------------------

ProteinLookup = Callable[[str], tuple[str, str] | None]       # accession -> (release, sequence)


def validate(data: bytes, meta: dict[str, Any], max_rows: int, protein: ProteinLookup) -> Report:
    rep = Report()
    if meta['compatibility'] == 'zhang_gps_dpsi' and (_norm(meta['endpoint']) not in DPSI_ENDPOINTS
                                                      or _norm(meta['units']) not in DPSI_UNITS):
        rep.issue('error', 'INCONSISTENT_ENDPOINT', 'Declared comparable with GPS ΔPSI, but the endpoint/units do not '
                  'say ΔPSI in PSI units. Fix the declaration or choose compatibility "other".')
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        rep.issue('error', 'ENCODING', 'The file is not UTF-8 text.')
        return rep
    first = text.split('\n', 1)[0]
    delim = '\t' if '\t' in first else ','
    rep.suffix = '.tsv' if delim == '\t' else '.csv'
    reader = csv.reader(io.StringIO(text), delimiter=delim)
    try:
        header = [h.strip() for h in next(reader)]
    except StopIteration:
        rep.issue('error', 'EMPTY_FILE', 'The file has no header row.')
        return rep
    missing = [c for c in REQUIRED if c not in header]
    if missing:
        rep.issue('error', 'MISSING_COLUMN', f"Missing required column(s): {', '.join(missing)}.")
        return rep
    if len(set(header)) != len(header):
        rep.issue('error', 'DUPLICATE_COLUMN', 'A column name appears twice.')
        return rep
    for h in header:
        if h not in REQUIRED and h not in OPTIONAL:
            rep.issue('warning', 'UNKNOWN_COLUMN', f'Column "{h[:40]}" is not part of the import schema and is ignored.')
    col = {h: i for i, h in enumerate(header)}
    seen: dict[tuple, tuple[int, float | None]] = {}
    for line_no, cells in enumerate(reader, start=2):
        if not any(c.strip() for c in cells):
            continue
        rep.counts['rows'] += 1
        if rep.counts['rows'] > max_rows:
            rep.issue('error', 'TOO_MANY_ROWS', f'The file has more than {max_rows} data rows.')
            break
        row = _row(rep, cells, col, line_no, protein)
        if row is None:
            rep.counts['rejected'] += 1
            continue
        key = (row['wt_sequence'], row['position'], row['mut_aa'], row['replicate_id'])
        if key in seen:
            first_row, first_value = seen[key]
            if first_value == row['observed_value']:
                rep.counts['duplicate'] += 1
                rep.issue('error', 'DUPLICATE_KEY', f'Same (wt_sequence, position, mut_aa, replicate_id) as row '
                          f'{first_row}; remove the repeat.', line_no)
            else:
                rep.counts['conflicting'] += 1
                rep.issue('error', 'CONFLICTING_VALUE', f'Same key as row {first_row} with a different value; the '
                          'earlier value is not overwritten. Use distinct replicate_id values.', line_no)
            continue
        seen[key] = (line_no, row['observed_value'])
        rep.counts['missing' if row['observed_value'] is None else 'valid'] += 1
        rep.rows.append(row)
    return rep


def _row(rep: Report, cells: list[str], col: dict[str, int], n: int, protein: ProteinLookup) -> dict | None:
    def get(name: str) -> str:
        i = col.get(name)
        return cells[i].strip() if i is not None and i < len(cells) else ''

    def reject(code: str, message: str) -> dict | None:
        rep.issue('error', code, message, n)
        return None                                   # the row is not kept

    peptide_id, rep_id = get('peptide_id'), get('replicate_id')
    if not peptide_id or len(peptide_id) > 200:
        return reject('INVALID_PEPTIDE_ID', 'peptide_id is required (at most 200 characters).')
    if not rep_id or len(rep_id) > 200:
        return reject('MISSING_REPLICATE', 'replicate_id is required; use one declared id for single replicates.')
    seq = get('wt_sequence').upper()
    if len(seq) != 28 or any(c not in AA for c in seq):
        return reject('INVALID_SEQUENCE', 'wt_sequence must be exactly 28 standard amino acids.')
    pos_text = get('position')
    if not INT.fullmatch(pos_text) or not 1 <= int(pos_text) <= 28:
        return reject('INVALID_POSITION', 'position must be an integer from 1 to 28 within the peptide.')
    pos = int(pos_text)
    wt, mut = get('wt_aa').upper(), get('mut_aa').upper()
    if wt != seq[pos - 1]:
        return reject('WT_MISMATCH', f'wt_aa does not match residue {pos} of wt_sequence.')
    if len(mut) != 1 or mut not in AA or mut == wt:
        return reject('INVALID_MUTANT', 'mut_aa must be one standard letter different from wt_aa.')
    value_text, reason = get('observed_value'), get('missing_reason')
    value: float | None
    if value_text == '':
        if not reason:
            return reject('MISSING_REASON', 'An empty observed_value needs a missing_reason; it is never read as 0.')
        value = None
    else:
        try:
            value = float(value_text)
        except ValueError:
            return reject('INVALID_VALUE', 'observed_value must be a number.')
        if not math.isfinite(value):
            return reject('NONFINITE_VALUE', 'observed_value must be finite (no NaN or infinity).')
        if reason:
            rep.issue('warning', 'REASON_WITH_VALUE', 'missing_reason is ignored because a value is present.', n)
            reason = ''
    mapping = {k: get(k) for k in ('uniprot_id', 'reference_release', 'start_pos')}
    given = [k for k, v in mapping.items() if v]
    acc = release = None
    start: int | None = None
    if given:
        if len(given) != 3:
            return reject('PARTIAL_MAPPING', 'uniprot_id, reference_release and start_pos go together.')
        if not INT.fullmatch(mapping['start_pos']) or int(mapping['start_pos']) < 1:
            return reject('INVALID_START', 'start_pos must be a positive integer (1-based protein coordinate).')
        acc, release, start = mapping['uniprot_id'], mapping['reference_release'], int(mapping['start_pos'])
        ref = protein(acc)
        if ref is None or ref[0] != release:
            rep.counts['mapping_unverified'] += 1
            rep.issue('warning', 'MAPPING_UNVERIFIED', 'The accession/release is not the loaded reference; the row is '
                      'aligned by sequence only, not by protein coordinate.', n)
        elif ref[1][start - 1:start + 27] != seq:
            rep.counts['conflicting'] += 1
            return reject('MAPPING_CONFLICT', 'wt_sequence differs from the reference protein at start_pos.')
        else:
            rep.counts['mapping_verified'] += 1
    for name, text_value in (('peptide_id', peptide_id), ('replicate_id', rep_id), ('missing_reason', reason)):
        if FORMULA.match(text_value):
            rep.issue('warning', 'FORMULA_TEXT', f'{name} starts like a spreadsheet formula; it is stored as text and '
                      'neutralised in exports.', n)
    return {'row_number': n, 'peptide_id': peptide_id, 'wt_sequence': seq, 'position': pos, 'wt_aa': wt,
            'mut_aa': mut, 'replicate_id': rep_id, 'observed_value': value, 'missing_reason': reason or None,
            'uniprot_acc': acc, 'reference_release': release, 'start_pos': start}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
