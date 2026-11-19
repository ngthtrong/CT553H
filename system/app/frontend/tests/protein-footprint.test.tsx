/** plan-system 2.1 — protein-level footprint on the Job page (VIZ-01…04, UI side). */
import { screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { handle } from '../mock/handler';
import { renderApp } from './utils';

function api(method: string, url: string, body?: unknown) {
  const out = handle(method, url, { 'content-type': 'application/json' }, body === undefined ? '' : JSON.stringify(body));
  return out.body ? JSON.parse(out.body) : null;
}

const before = (a: Element, b: Element) => Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);

describe('2.1 protein footprint', () => {
  it('appears when the protein job has finished: label first, alternate lanes, a table with links to each tile', async () => {
    const pid = api('POST', '/v1/projects', { name: 'fp' }).project_id as string;
    const job = api('POST', `/v1/projects/${pid}/jobs`, { mode: 'protein', override_domain: true, protein: { uniprot_id: 'A6NMZ7' } });
    // finish the simulated job before rendering (each read advances one item)
    for (let i = 0; i < 300; i += 1) {
      const j = api('GET', `/v1/jobs/${job.job_id}`);
      if (['completed', 'partial', 'failed', 'cancelled'].includes(j.state)) break;
    }
    const fp = api('GET', `/v1/jobs/${job.job_id}/footprint`);
    expect(fp.tiles.length).toBe(fp.protein.tiles);
    // VIZ-01 on the mock: each position is the mean of 19 cells of its own tile
    const t1 = fp.tiles.find((t: { analysis_id: string | null }) => t.analysis_id);
    const a = api('GET', `/v1/analyses/${t1.analysis_id}`);
    const at = a.result.cells.filter((c: { position: number }) => c.position === 3);
    expect(Math.abs(t1.positions[2].mean_prob - at.reduce((s: number, c: { p_dpsi_ge_1_calibrated: number }) => s + c.p_dpsi_ge_1_calibrated, 0) / 19)).toBeLessThan(1e-9);

    renderApp(`/jobs/${job.job_id}`);
    const section = await screen.findByTestId('protein-footprint');
    const label = within(section).getByTestId('protein-footprint-label');
    expect(label).toHaveTextContent('not a phenotype of the whole protein');
    expect(before(label, within(section).getByTestId('protein-footprint-chart'))).toBe(true);
    const tiles = within(section).getAllByTestId('pfp-tile');
    expect(tiles).toHaveLength(fp.protein.tiles);
    // VIZ-02: two lanes, consecutive windows never share a lane
    const ys = tiles.slice(0, 2).map((g) => g.querySelector('rect')!.getAttribute('y'));
    expect(ys[0]).not.toBe(ys[1]);
    await userEvent.click(within(section).getByRole('button', { name: 'Show as a table' }));
    const table = within(section).getByTestId('protein-footprint-table');
    expect(within(table).getAllByRole('row')).toHaveLength(fp.protein.tiles + 1);
    expect(within(table).getAllByRole('link', { name: /Open tile/ }).length).toBeGreaterThan(0);
    await userEvent.click(within(section).getByRole('radio', { name: 'Mean raw score' }));
    await waitFor(() => expect(within(table).getByRole('table')).toHaveAccessibleName(/mean raw score/));
  }, 30000);

  it('is not shown for a peptide job', async () => {
    const pid = api('POST', '/v1/projects', { name: 'pep' }).project_id as string;
    const job = api('POST', `/v1/projects/${pid}/jobs`, { mode: 'peptides', peptides: [{ input_id: 'a', sequence: 'DIMFLVDSSGSIGPENFSKMKTFMKNLV' }] });
    renderApp(`/jobs/${job.job_id}`);
    await waitFor(() => expect(document.querySelector('.ui-pill[data-status="completed"]')).not.toBeNull(), { timeout: 8000 });
    expect(screen.queryByTestId('protein-footprint')).toBeNull();
  }, 15000);
});

describe('3.5 report link', () => {
  it('a saved analysis offers the HTML report by id only, in a new tab', async () => {
    const pid = api('POST', '/v1/projects', { name: 'rpt' }).project_id as string;
    const a = api('POST', `/v1/projects/${pid}/analyses`, { request: { uniprot_id: 'A6NMZ7', tile_index: 1 } });
    renderApp(`/analyses/${a.analysis_id}`);
    const link = await screen.findByTestId('report-link');
    expect(link.getAttribute('href')!.endsWith(`/v1/analyses/${a.analysis_id}/report?format=html`)).toBe(true);
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', 'noopener noreferrer');
  });
});
