import { describe, expect, it } from 'vitest';
import { effectiveWarnings, isOverridden, unshowableReason } from '../src/lib/domain';
import type { PredictionResult } from '../src/api/types';
import { handle } from '../mock/handler';

function result(body: unknown): PredictionResult {
  return body as PredictionResult;
}

const sample = (req: object) => result(JSON.parse(handle('POST', '/v1/predict', {}, JSON.stringify(req)).body));

describe('domain rules (W-2, W-3; "never a score without domain and model")', () => {
  it('adds the required warning when the server omitted it for an unknown tile', () => {
    const r = sample({ sequence: 'DIMFLVDSSGSIGPENFSKMKTFMKNLV' });
    r.warnings = [];
    expect(effectiveWarnings(r).map((w) => w.code)).toEqual(['DOMAIN_UNKNOWN']);
  });

  it('adds nothing for a measured in-domain tile', () => {
    expect(effectiveWarnings(sample({ uniprot_id: 'P60484', tile_index: 2 }))).toEqual([]);
  });

  it('does not duplicate a warning the server sent', () => {
    const r = sample({ sequence: 'DIMFLVDSSGSIGPENFSKMKTFMKNLV' });
    expect(effectiveWarnings(r)).toHaveLength(1);
  });

  it('detects an override', () => {
    expect(isOverridden(sample({ uniprot_id: 'A6NMZ7', tile_index: 5, override_domain: true }))).toBe(true);
    expect(isOverridden(sample({ uniprot_id: 'A6NMZ7', tile_index: 28 }))).toBe(false);
  });

  it('refuses to show a response without domain status or model version', () => {
    const r = sample({ uniprot_id: 'A6NMZ7', tile_index: 28 });
    expect(unshowableReason(r)).toBeNull();
    expect(unshowableReason({ ...r, domain: undefined })).toMatch(/domain status/);
    expect(unshowableReason({ ...r, provenance: { ...r.provenance, model_id: '' } })).toMatch(/model version/);
    expect(unshowableReason({ ...r, cells: [] })).toMatch(/no scores/);
    expect(unshowableReason(null)).toMatch(/empty/);
  });
});
