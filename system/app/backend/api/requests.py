"""Request body parsing for the prediction endpoints, in the validation order of api-spec.md §3."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from starlette.requests import Request

from degron_footprint.errors import DomainError
from degron_footprint.validation import MODEL_ID_RE, check_accession, normalize_sequence

PREDICT_FIELDS = {'sequence', 'uniprot_id', 'tile_index', 'model_id', 'calibrator', 'override_domain'}


@dataclass(frozen=True)
class PredictRequest:
    sequence: str | None
    uniprot_id: str | None
    tile_index: Any | None
    model_id: str | None
    calibrator: str | None
    override_domain: bool


async def read_json_body(request: Request, limit: int) -> Any:
    """Step 1: at most `limit` bytes, valid JSON object. Never reads more than limit + 1 bytes."""
    declared = request.headers.get('content-length')
    if declared is not None and declared.isdigit() and int(declared) > limit:
        raise DomainError('PAYLOAD_TOO_LARGE', f'The request body must not exceed {limit} bytes.', 413)
    chunks: list[bytes] = []
    total = 0
    async for chunk in request.stream():
        total += len(chunk)
        if total > limit:
            raise DomainError('PAYLOAD_TOO_LARGE', f'The request body must not exceed {limit} bytes.', 413)
        chunks.append(chunk)
    try:
        body = json.loads(b''.join(chunks))
    except (ValueError, RecursionError):
        raise DomainError('INVALID_REQUEST', 'The body is not valid JSON.', 400) from None
    if not isinstance(body, dict):
        raise DomainError('INVALID_REQUEST', 'The body must be a JSON object.', 400)
    return body


def parse_predict(body: dict, extra_fields: frozenset[str] = frozenset()) -> PredictRequest:
    """Steps 2 and 3 plus field typing. Sequence/accession/tile checks happen later (they need the database)."""
    for key in body:
        if key not in PREDICT_FIELDS and key not in extra_fields:
            # the name is attacker-controlled text: it is not echoed (SEC-02), so `field` stays null
            raise DomainError('INVALID_REQUEST', 'The request has a field that is not part of the interface.', 422)
    has_seq = body.get('sequence') is not None
    has_acc = body.get('uniprot_id') is not None
    has_idx = body.get('tile_index') is not None
    if has_seq and (has_acc or has_idx):
        raise DomainError('INVALID_REQUEST', 'Give either "sequence" or "uniprot_id" with "tile_index", not both.', 422)
    if not has_seq and not (has_acc and has_idx):
        raise DomainError('INVALID_REQUEST', 'Give "sequence", or "uniprot_id" together with "tile_index".', 422)
    calibrator = body.get('calibrator')
    if calibrator is not None and calibrator not in ('platt', 'iso'):
        raise DomainError('INVALID_REQUEST', 'calibrator must be "platt" or "iso".', 422, 'calibrator')
    override = body.get('override_domain', False)
    if not isinstance(override, bool):
        raise DomainError('INVALID_REQUEST', 'override_domain must be true or false.', 422, 'override_domain')
    model_id = body.get('model_id')
    if model_id is not None and not isinstance(model_id, str):
        raise DomainError('INVALID_REQUEST', 'model_id must be a string.', 422, 'model_id')
    return PredictRequest(body.get('sequence'), body.get('uniprot_id'), body.get('tile_index'), model_id,
                          calibrator, override)


def valid_model_id(value: str) -> bool:
    return bool(MODEL_ID_RE.fullmatch(value))


__all__ = ['PredictRequest', 'read_json_body', 'parse_predict', 'valid_model_id',
           'normalize_sequence', 'check_accession']
