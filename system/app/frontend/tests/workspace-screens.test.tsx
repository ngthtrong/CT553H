/**
 * WP9: one or more tests per v0.2 screen (Projects, Project workspace, New analysis batch/protein, Job, Saved analysis
 * with comparison and annotations, Import, Dataset) plus the pure helpers behind them. Data is created through the same
 * mock handler that MSW serves (synthetic numbers).
 */
import { screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { handle } from '../mock/handler';
import type { Cell } from '../src/api/types';
import { parseBatch, parseProtein } from '../src/lib/batch';
import { footprint } from '../src/lib/footprint';
import { REAL_TILE, renderApp } from './utils';

function api(method: string, url: string, body?: unknown) {
  const out = handle(method, url, { 'content-type': 'application/json' }, body === undefined ? '' : JSON.stringify(body));
  return out.body ? JSON.parse(out.body) : null;
}

function seedProject(name = 'Seed project') {
  return api('POST', '/v1/projects', { name }).project_id as string;
}

describe('lib/batch', () => {
  it('parses FASTA with stable unique ids and counts invalid and repeated entries', () => {
    const p = parseBatch(`>a x\n${REAL_TILE}\n>a\n${REAL_TILE}\n>b\nACD`);
    expect(p.entries.map((e) => e.input_id)).toEqual(['a', 'a-2', 'b']);
    expect([p.valid, p.invalid, p.duplicateSequences, p.blocking]).toEqual([2, 1, 1, null]);
  });
  it('parses id,sequence lines and bare lines, and blocks more than 100 records', () => {
    expect(parseBatch(`x,${REAL_TILE}\n${REAL_TILE}`).entries.map((e) => e.input_id)).toEqual(['x', 'peptide-2']);
    expect(parseBatch(Array.from({ length: 101 }, () => REAL_TILE).join('\n')).blocking).toMatch(/at most 100/);
  });
  it.each([[27, 0, []], [28, 1, []], [50, 1, [{ start: 29, end: 50 }]], [51, 2, []]])('protein of %i residues → %i windows', (len, tiles, uncovered) => {
    const p = parseProtein(`>prot\n${'A'.repeat(len)}`);
    expect(p.tiles).toBe(tiles);
    expect(p.uncovered).toEqual(uncovered);
    expect(Boolean(p.blocking)).toBe(tiles === 0);
  });
  it('marks windows with a non-standard residue as unscorable', () => {
    // X is residue 31: only window 2 (24–51) contains it
    expect(parseProtein(`${'A'.repeat(30)}X${'A'.repeat(20)}`).unscorable).toEqual([2]);
  });
});

describe('lib/footprint', () => {
  it('equals the per-position mean recomputed from the 532 cells within 1e-9 (plan 2.11)', () => {
    const r = api('POST', '/v1/predict', { sequence: REAL_TILE });
    const cells = r.cells as Cell[];
    for (const mode of ['prob', 'raw'] as const) {
      const rows = footprint(cells, REAL_TILE, mode);
      expect(rows).toHaveLength(28);
      for (const row of rows) {
        const at = cells.filter((c) => c.position === row.position);
        expect(at).toHaveLength(19);
        const v = at.map((c) => (mode === 'prob' ? c.p_dpsi_ge_1_calibrated : c.score_dpsi_raw));
        expect(Math.abs(row.mean - v.reduce((s, x) => s + x, 0) / 19)).toBeLessThan(1e-9);
        expect(row.wt).toBe(REAL_TILE[row.position - 1]);
      }
    }
  });
});

describe('9.1 Projects', () => {
  it('shows the empty state, then the project cards with their counts', async () => {
    renderApp('/projects');
    expect(await screen.findByText('No project yet')).toBeInTheDocument();
  });
  it('lists projects with counts', async () => {
    const pid = seedProject('Card project');
    api('POST', `/v1/projects/${pid}/analyses`, { request: { sequence: REAL_TILE } });
    renderApp('/projects');
    const list = await screen.findByTestId('project-list');
    const card = within(list).getByRole('link', { name: 'Card project' }).closest('li')!;
    expect(within(card).getByText('Analyses').nextElementSibling).toHaveTextContent('1');
  });
});

describe('9.2 Project workspace', () => {
  it('shows history rows from the summary and the jobs tab', async () => {
    const pid = seedProject();
    api('POST', `/v1/projects/${pid}/analyses`, { request: { uniprot_id: 'A6NMZ7', tile_index: 28 } });
    api('POST', `/v1/projects/${pid}/jobs`, { mode: 'peptides', peptides: [{ input_id: 'a', sequence: REAL_TILE }] });
    const { location } = renderApp(`/projects/${pid}`);
    const table = await screen.findByRole('table', { name: 'Analysis history' });
    expect(within(table).getByRole('link', { name: /A6NMZ7 tile 28/ })).toBeInTheDocument();
    await userEvent.click(screen.getByRole('tab', { name: /Jobs/ }));
    expect(await screen.findByRole('table', { name: 'Jobs' })).toBeInTheDocument();
    expect(location().search).toBe('?tab=jobs');
    expect(JSON.stringify(location())).not.toContain(REAL_TILE);
  });
  it('asks for confirmation with the dependency summary before deleting', async () => {
    const pid = seedProject('To delete');
    api('POST', `/v1/projects/${pid}/analyses`, { request: { sequence: REAL_TILE } });
    renderApp(`/projects/${pid}`);
    await userEvent.click(await screen.findByRole('button', { name: 'Delete…' }));
    expect(await screen.findByTestId('delete-dependencies')).toHaveTextContent('1 saved analyses');
    expect(api('GET', `/v1/projects/${pid}`).project_id).toBe(pid);           // nothing deleted yet
  });
});

describe('9.3 New analysis', () => {
  it('previews a peptide batch before submitting', async () => {
    const pid = seedProject();
    renderApp(`/new?mode=batch&project=${pid}`);
    await userEvent.type(await screen.findByRole('textbox', { name: 'Peptides' }), `${REAL_TILE}{enter}ACD`);
    const preview = screen.getByTestId('batch-preview');
    expect(preview).toHaveTextContent('2 of at most 100');
    expect(within(preview).getByText('Invalid (listed as refused)').nextElementSibling).toHaveTextContent('1');
    expect(screen.getByRole('button', { name: 'Submit batch job' })).toBeEnabled();
  });
  it('keeps the single-peptide input as the default mode', async () => {
    renderApp('/new');
    expect(await screen.findByLabelText(/Tile sequence/)).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: /Single peptide/ })).toBeChecked();
  });
});

describe('9.9 Job', () => {
  it('polls to a terminal state and lists refused items with their reason', async () => {
    const pid = seedProject();
    const job = api('POST', `/v1/projects/${pid}/jobs`, { mode: 'peptides', peptides: [{ input_id: 'ok', sequence: REAL_TILE }, { input_id: 'bad', sequence: 'ACD' }] });
    renderApp(`/jobs/${job.job_id}`);
    expect(await screen.findByRole('progressbar', { name: 'Items finished' })).toBeInTheDocument();
    await waitFor(() => expect(document.querySelector('.ui-pill[data-status="partial"]')).not.toBeNull(), { timeout: 8000 });
    const table = await screen.findByTestId('job-item-table');
    expect(within(table).getByText('INVALID_LENGTH')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Cancel job' })).not.toBeInTheDocument();
  }, 15000);
});

describe('9.6–9.8 Saved analysis', () => {
  it('reads the snapshot, shows the footprint and the annotation state', async () => {
    const pid = seedProject();
    const a = api('POST', `/v1/projects/${pid}/analyses`, { request: { sequence: REAL_TILE } });
    renderApp(`/analyses/${a.analysis_id}`);
    expect(await screen.findByText('Saved snapshot')).toBeInTheDocument();
    expect(screen.getByTestId('footprint-track')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Run again' })).toBeInTheDocument();
    await userEvent.click(screen.getByRole('tab', { name: 'ClinVar and annotations' }));
    expect(screen.getByTestId('annotation-status')).toHaveAttribute('data-state', 'mapping_unavailable');
    await userEvent.click(screen.getByRole('tab', { name: 'Comparison' }));
    expect(await screen.findByText('No committed dataset in this project')).toBeInTheDocument();
  });
});

describe('9.10–9.11 Import and dataset', () => {
  it('sends the file with its metadata and shows the validation report; blocking errors leave no Commit button', async () => {
    // jsdom hands MSW an empty body for a File inside FormData (the SHA-256 is that of ""), so the report here is the
    // "missing columns" one. The acknowledge-then-commit path runs in a real browser: e2e/workspace.spec.ts (UC-09).
    const pid = seedProject();
    renderApp(`/import?project=${pid}`);
    const csv = `peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id\n=p,${REAL_TILE},1,D,A,0.5,r1`;
    await userEvent.upload(await screen.findByLabelText(/CSV or TSV file/), new File([csv], 'obs.csv', { type: 'text/csv' }));
    expect(screen.getByRole('button', { name: 'Validate file' })).toBeDisabled();       // metadata still missing
    await userEvent.type(screen.getByLabelText(/Dataset name/), 'My data');
    await userEvent.type(screen.getByLabelText(/Source or citation/), 'lab');
    await userEvent.type(screen.getByLabelText(/Reference description/), 'tile 28');
    await userEvent.click(screen.getByRole('button', { name: 'Validate file' }));
    const report = await screen.findByTestId('validation-report');
    expect(report).toHaveTextContent('Staged (not committed)');
    expect(report).toHaveTextContent('not used to retrain the model');
    expect(report).toHaveTextContent('MISSING_COLUMN');
    expect(screen.queryByRole('button', { name: 'Commit dataset' })).not.toBeInTheDocument();
  });
  it('shows a staged dataset as not committed', async () => {
    const pid = seedProject();
    const b = 'B';
    const body = `--${b}\r\nContent-Disposition: form-data; name="metadata"\r\n\r\n${JSON.stringify({ name: 'staged', assay: 'GPS', endpoint: 'delta_psi', units: 'PSI', source: 's', reference_description: 'r', compatibility: 'zhang_gps_dpsi' })}\r\n--${b}\r\nContent-Disposition: form-data; name="file"; filename="x.csv"\r\n\r\npeptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id\np,${REAL_TILE},1,D,A,0.5,r1\r\n--${b}--\r\n`;
    const d = JSON.parse(handle('POST', `/v1/projects/${pid}/datasets`, { 'content-type': `multipart/form-data; boundary=${b}` }, body).body);
    renderApp(`/datasets/${d.dataset_id}`);
    expect(await screen.findByText('Staged, not committed')).toBeInTheDocument();
    expect(screen.getByTestId('validation-report')).toHaveTextContent(d.sha256);
  });
});

describe('plan 2.11 priority panel', () => {
  it('puts the retrospective label before the numbers and lists the top k by rank', async () => {
    renderApp('/result/uniprot/A6NMZ7/28');
    const panel = await screen.findByTestId('priority-panel');
    const label = within(panel).getByTestId('priority-label');
    const first = within(panel).getAllByRole('listitem')[0]!;
    expect(label.compareDocumentPosition(first) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(label).toHaveTextContent(/Retrospective, development benchmark/);
    expect(within(panel).getAllByRole('listitem')).toHaveLength(10);
    await userEvent.selectOptions(within(panel).getByLabelText('Number of substitutions'), '5');
    expect(within(panel).getAllByRole('listitem')).toHaveLength(5);
  });
});
