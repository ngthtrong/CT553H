import type { DomainStatus, PredictionResult, Warning } from '../api/types';

export interface StatusPresentation {
  label: string;
  /** One of four fill patterns (ui-design §3.2) so that colour is never the only carrier. */
  pattern: 'solid' | 'hatched' | 'dotted' | 'empty';
  predicted: boolean;
  /** Whether scores need an amber warning before the heatmap (rule W-2). */
  needsWarning: boolean;
}

export const STATUS: Record<DomainStatus, StatusPresentation> = {
  measured_in_domain: { label: 'In domain (measured)', pattern: 'solid', predicted: false, needsWarning: false },
  measured_out_of_domain: { label: 'Outside the domain (measured)', pattern: 'hatched', predicted: false, needsWarning: false },
  measured_unreliable: { label: 'Unreliable measurement', pattern: 'dotted', predicted: false, needsWarning: true },
  predicted_in_domain: { label: 'In domain (predicted)', pattern: 'solid', predicted: true, needsWarning: true },
  predicted_out_of_domain: { label: 'Outside the domain (predicted)', pattern: 'hatched', predicted: true, needsWarning: true },
  unknown: { label: 'Domain unknown', pattern: 'empty', predicted: false, needsWarning: true },
};

const FALLBACK_TEXT: Partial<Record<DomainStatus, { code: Warning['code']; message: string }>> = {
  unknown: {
    code: 'DOMAIN_UNKNOWN',
    message:
      'The domain of this tile is unknown. The model was trained only on tiles that behave as degrons (wild-type PSI ≤ 4.0) and cannot check this one.',
  },
  measured_unreliable: {
    code: 'DOMAIN_UNRELIABLE',
    message: 'The measurement of this tile rests on too few reads; whether it is in the domain is uncertain.',
  },
  predicted_in_domain: {
    code: 'PREDICTED_DOMAIN',
    message: 'The domain status of this tile is predicted, not measured.',
  },
  predicted_out_of_domain: {
    code: 'PREDICTED_DOMAIN',
    message: 'The domain status of this tile is predicted, not measured.',
  },
};

/**
 * Warnings to show above the heatmap. The server list is authoritative; if the server omitted the
 * warning that its own domain status requires (rule W-2), the client adds it rather than showing
 * scores without it.
 */
export function effectiveWarnings(result: PredictionResult): Warning[] {
  const out = [...result.warnings];
  const fb = FALLBACK_TEXT[result.domain.status];
  if (fb && !out.some((w) => w.code === fb.code)) out.push({ code: fb.code, message: fb.message });
  return out;
}

export function isOverridden(result: PredictionResult): boolean {
  return result.warnings.some((w) => w.code === 'OUT_OF_DOMAIN_OVERRIDDEN');
}

/**
 * The interface never shows a score without the domain status and the model version
 * (ui-design principle 1). Returns the reason when a response cannot be shown.
 */
export function unshowableReason(result: Partial<PredictionResult> | null | undefined): string | null {
  if (!result) return 'The response was empty.';
  if (!result.domain?.status) return 'The response has no domain status.';
  if (!result.provenance?.model_id) return 'The response has no model version.';
  if (!result.provenance.evidence_label || !result.provenance.event_definition) {
    return 'The response does not say what the numbers mean.';
  }
  if (!Array.isArray(result.cells) || result.cells.length === 0) return 'The response has no scores.';
  return null;
}
