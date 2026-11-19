/** plan-system 2.6 — candidates to verify (UI side). */
import { screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { handle, MOCK_SLOW_MODEL_ID } from '../mock/handler';
import { renderApp } from './utils';

function api(method: string, url: string, body?: unknown) {
  const out = handle(method, url, { 'content-type': 'application/json' }, body === undefined ? '' : JSON.stringify(body));
  return out.body ? JSON.parse(out.body) : null;
}
const before = (a: Element, b: Element) => Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);

describe('2.6 candidates', () => {
  it('lists candidates with reasons after the label, using a saved model comparison as the second analysis', async () => {
    const user = userEvent.setup();
    const pid = api('POST', '/v1/projects', { name: 'cand' }).project_id as string;
    const a = api('POST', `/v1/projects/${pid}/analyses`, { request: { uniprot_id: 'A6NMZ7', tile_index: 1 } });
    const b = api('POST', `/v1/projects/${pid}/analyses`, { request: { uniprot_id: 'A6NMZ7', tile_index: 1, model_id: MOCK_SLOW_MODEL_ID } });
    api('POST', '/v1/analyses/compare', { analysis_a: a.analysis_id, analysis_b: b.analysis_id, save: true });
    renderApp(`/analyses/${a.analysis_id}`);
    await user.click(await screen.findByRole('tab', { name: 'Candidates' }));
    const panel = await screen.findByTestId('candidates-panel');
    const label = within(panel).getByTestId('candidates-label');
    expect(label).toHaveTextContent('not an experimentally validated design');
    // no second analysis selected: synthetic mock data have no ClinVar here, so nothing qualifies
    await user.selectOptions(within(panel).getByLabelText('Compare with'), b.analysis_id);
    const table = await within(panel).findByTestId('candidates-table');
    expect(before(label, table)).toBe(true);
    const rows = within(table).getAllByRole('row').slice(1);
    expect(rows.length).toBeGreaterThan(0);
    for (const r of rows) expect(r).toHaveTextContent(/P differs by|ClinVar/);
    expect(within(panel).getByRole('button', { name: /Export candidates CSV/ })).toBeInTheDocument();
  });
});
