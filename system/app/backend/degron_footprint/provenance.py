"""Provenance (api-spec.md §6): built from registry rows, never typed by hand."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .constants import CODE_VERSION, DISCLAIMER_SCOPE


def utc_iso(dt: datetime | None = None) -> str:
    dt = dt or datetime.now(UTC)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


@dataclass(frozen=True)
class ModelInfo:
    """The registered facts about one effect model that the API shows."""

    model_id: str
    kind: str
    weights_sha256: str
    feature_spec: str
    event_definition: str
    evidence_label: str
    domain_description: str
    trained_on_sources: tuple[dict, ...] = field(default_factory=tuple)


def source_ref(row: dict) -> dict:
    """The five fields of DataSourceRef."""
    return {k: row[k] for k in ('source_id', 'name', 'version', 'license_name', 'attribution_text')}


def build_provenance(model: ModelInfo, extra_sources: list[dict] | None = None,
                     generated_at: datetime | None = None) -> dict:
    """Training sources of the model, plus every source of any overlay or lookup used; deduplicated by id.

    The ClinVar diagnostic disclaimer (and any other `disclaimer_text`) is added whenever its source is listed.
    """
    seen: dict[str, dict] = {}
    for s in [*model.trained_on_sources, *(extra_sources or [])]:
        seen.setdefault(s['source_id'], s)
    disclaimers = [DISCLAIMER_SCOPE]
    for s in seen.values():
        text = s.get('disclaimer_text')
        if text and text not in disclaimers:
            disclaimers.append(text)
    return {
        'model_id': model.model_id,
        'model_kind': model.kind,
        'weights_sha256': model.weights_sha256,
        'feature_spec': model.feature_spec,
        'event_definition': model.event_definition,
        'evidence_label': model.evidence_label,
        'domain_description': model.domain_description,
        'data_sources': [source_ref(s) for s in seen.values()],
        'code_version': CODE_VERSION,
        'generated_at': utc_iso(generated_at),
        'disclaimers': disclaimers,
    }
