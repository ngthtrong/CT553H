/** plan-system 2.2 — compare two models on one saved analysis (UI side of CMP-01…03). */
import { screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { handle, MOCK_SLOW_MODEL_ID } from '../mock/handler';
import { contrastRatio, diffColor, luminance } from '../src/lib/colors';
import { renderApp } from './utils';

function api(method: string, url: string, body?: unknown) {
  const out = handle(method, url, { 'content-type': 'application/json' }, body === undefined ? '' : JSON.stringify(body));
  return { status: out.status, data: out.body ? JSON.parse(out.body) : null };
}
const before = (a: Element, b: Element) => Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);

describe('2.2 model comparison', () => {
  it('runs the other model as a new analysis, stores the comparison and opens it: label first, metrics, disagreements', async () => {
    const user = userEvent.setup();
    const pid = api('POST', '/v1/projects', { name: 'mc' }).data.project_id as string;
    const a = api('POST', `/v1/projects/${pid}/analyses`, { request: { uniprot_id: 'A6NMZ7', tile_index: 1 } }).data;
    const { location } = renderApp(`/analyses/${a.analysis_id}`);
    await user.click(await screen.findByRole('tab', { name: 'Other model' }));
    const panel = await screen.findByTestId('model-compare-panel');
    expect(within(panel).getByLabelText('Other model')).toHaveValue(MOCK_SLOW_MODEL_ID);
    await user.click(within(panel).getByRole('button', { name: 'Compare with another model' }));
    await user.click(await screen.findByRole('button', { name: 'Start anyway' }));          // 38 s per tile: confirm
    const view = await screen.findByTestId('model-comparison');
    expect(location().pathname).toMatch(/^\/model-comparisons\/[0-9a-f-]{36}$/);
    const label = within(view).getByTestId('model-comparison-label');
    expect(label).toHaveTextContent('does not tell which model is right');
    expect(before(label, within(view).getByTestId('model-comparison-metrics'))).toBe(true);
    expect(within(view).getByTestId('model-side-a')).toHaveTextContent('mock-m3-ext4.0-platt-v1');
    expect(within(view).getByTestId('model-side-b')).toHaveTextContent(MOCK_SLOW_MODEL_ID);
    expect(within(view).getByTestId('model-comparison-metrics')).toHaveTextContent('Substitutions compared532');
    expect(within(within(view).getByTestId('model-disagreements')).getAllByRole('row')).toHaveLength(21);
    expect(within(view).getByTestId('model-diff-heatmap').querySelectorAll('rect.cell')).toHaveLength(560);
    expect(within(view).getByRole('button', { name: /Export comparison CSV/ })).toBeInTheDocument();
    // the comparison is listed on the first analysis afterwards
    const listed = api('GET', `/v1/projects/${pid}/model-comparisons?analysis_id=${a.analysis_id}`).data;
    expect(listed.total).toBe(1);
  }, 20000);

  it('refuses analyses of different tiles (CMP-02 in the mock)', () => {
    const pid = api('POST', '/v1/projects', { name: 'mc2' }).data.project_id as string;
    const a = api('POST', `/v1/projects/${pid}/analyses`, { request: { uniprot_id: 'A6NMZ7', tile_index: 1 } }).data;
    const b = api('POST', `/v1/projects/${pid}/analyses`, { request: { uniprot_id: 'A6NMZ7', tile_index: 2 } }).data;
    const r = api('POST', '/v1/analyses/compare', { analysis_a: a.analysis_id, analysis_b: b.analysis_id });
    expect(r.status).toBe(422);
    expect(r.data.field).toBe('analysis_b');
  });

  it('the difference scale is diverging BrBG: brown for A higher, teal for B higher, light at 0', () => {
    const rgb = (c: string) => c.match(/\d+/g)!.map(Number) as [number, number, number];
    const [r0, , b0] = rgb(diffColor(-1, 1));
    const [r1, g1, b1] = rgb(diffColor(1, 1));
    expect(r0).toBeGreaterThan(b0);                           // brown end
    expect(g1).toBeGreaterThan(r1);                           // teal end
    expect(b1).toBeGreaterThan(r1);
    expect(luminance(diffColor(0, 1))).toBeGreaterThan(0.8);  // near-white agreement
    expect(contrastRatio(diffColor(-1, 1), diffColor(1, 1))).toBeGreaterThan(1);
    expect(diffColor(5, 1)).toBe(diffColor(1, 1));            // clamped
    expect(Math.abs(luminance(diffColor(-0.5, 1)) - luminance(diffColor(0.5, 1)))).toBeLessThan(0.15);   // roughly symmetric
  });
});
