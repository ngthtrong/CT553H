/** plan-system 3.3 — several proteins in one job (UI side of BATCH-10). */
import { screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { handle } from '../mock/handler';
import { parseProteins } from '../src/lib/batch';
import { renderApp } from './utils';

const A = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'.repeat(3);           // 84 residues: 3 windows
const B = 'MKTAYIAKQRQISFVKSHFSRQLEERLG'.repeat(2);           // 56 residues: 2 windows

describe('parseProteins', () => {
  it('splits FASTA records, keeps per-record problems and checks the total limit', () => {
    const p = parseProteins(`>alpha\n${A}\n>beta\n${B}\n>tiny\nACDE`);
    expect(p.records.map((r) => [r.input_id, r.tiles])).toEqual([['alpha', 3], ['beta', 2], ['tiny', 0]]);
    expect(p.records[2]!.blocking).toMatch(/fewer than one/);
    expect(p.blocking).toBeNull();
    expect(p.totalTiles).toBe(5);
    expect(parseProteins(`>x\n${A}\n>x\n${B}`).blocking).toMatch(/same id/);
    expect(parseProteins(`>a\n${'A'.repeat(6000)}\n>b\n${'A'.repeat(6000)}`).blocking).toMatch(/in total/);
  });
});

describe('3.3 multi-protein job', () => {
  it('previews each protein, submits one job, shows the coverage of each and a footprint per protein', async () => {
    const user = userEvent.setup();
    const pid = JSON.parse(handle('POST', '/v1/projects', { 'content-type': 'application/json' }, JSON.stringify({ name: 'multi' })).body!).project_id as string;
    const { location } = renderApp(`/new?mode=protein&project=${pid}`);
    await user.click(await screen.findByRole('radio', { name: /FASTA records/ }));
    const ta = screen.getByRole('textbox', { name: /FASTA records/ });
    await user.click(ta);
    await user.paste(`>alpha\n${A}\n>beta\n${B}`);
    const table = await screen.findByTestId('proteins-preview-table');
    expect(within(table).getAllByRole('row')).toHaveLength(3);
    expect(screen.getByTestId('protein-preview')).toHaveTextContent('5 windows × 532 substitutions');
    await user.click(screen.getByRole('checkbox', { name: /Score out-of-domain tiles anyway/ }));
    await user.click(screen.getByRole('button', { name: 'Submit protein job' }));
    await waitFor(() => expect(location().pathname).toMatch(/^\/jobs\//));
    const cov = await screen.findByTestId('protein-coverage');
    expect(cov).toHaveTextContent('Protein coverage (2 proteins)');
    expect(cov).toHaveTextContent('alpha (typed, no accession)');
    expect(cov).toHaveTextContent('beta (typed, no accession)');
    const select = await screen.findByTestId('footprint-protein', {}, { timeout: 15000 });
    expect(within(select).getAllByRole('option').map((o) => o.textContent)).toEqual(['alpha', 'beta']);
    expect(within(screen.getByTestId('protein-footprint')).getAllByTestId('pfp-tile')).toHaveLength(3);
    await user.selectOptions(select, 'beta');
    await waitFor(() => expect(within(screen.getByTestId('protein-footprint')).getAllByTestId('pfp-tile')).toHaveLength(2));
  }, 30000);
});
