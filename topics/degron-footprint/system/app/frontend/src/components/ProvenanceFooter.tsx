import type { Provenance } from '../api/types';
import { fmtDateTime } from '../lib/format';

/** Always-visible provenance (FR-14). */
export function ProvenanceFooter({ provenance: p }: { provenance: Provenance }) {
  return (
    <footer className="provenance" aria-label="Provenance of this result" data-testid="provenance">
      <strong>Provenance</strong>
      <dl>
        <dt>Model</dt>
        <dd>
          <code>{p.model_id}</code>
          {p.model_kind ? ` (${p.model_kind})` : ''}
        </dd>
        <dt>Weights SHA-256</dt>
        <dd>
          <code>{p.weights_sha256}</code>
        </dd>
        {p.feature_spec && (
          <>
            <dt>Features</dt>
            <dd>{p.feature_spec}</dd>
          </>
        )}
        <dt>Event</dt>
        <dd>{p.event_definition}</dd>
        <dt>Evidence</dt>
        <dd>{p.evidence_label}</dd>
        <dt>Domain</dt>
        <dd>{p.domain_description}</dd>
        <dt>Data sources</dt>
        <dd>
          {p.data_sources.map((s) => `${s.name} (${s.version}; ${s.license_name})`).join('; ') || 'none listed'}
        </dd>
        <dt>Code version</dt>
        <dd>{p.code_version}</dd>
        <dt>Generated</dt>
        <dd>{fmtDateTime(p.generated_at)}</dd>
      </dl>
      <ul>
        {p.disclaimers.map((d) => (
          <li key={d}>{d}</li>
        ))}
      </ul>
    </footer>
  );
}
