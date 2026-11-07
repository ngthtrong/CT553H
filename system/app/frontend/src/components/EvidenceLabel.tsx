import type { Provenance } from '../api/types';

/** Rule W-5: what kind of evidence the numbers are, visible without scrolling or clicking. */
export function EvidenceLabel({ provenance }: { provenance: Provenance }) {
  return (
    <p className="banner" data-testid="evidence-label">
      <strong>Evidence:</strong> {provenance.evidence_label}. <strong>Event:</strong> {provenance.event_definition}.
    </p>
  );
}
