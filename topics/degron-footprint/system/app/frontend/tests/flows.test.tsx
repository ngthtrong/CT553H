import { act, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { handle } from '../mock/handler';
import { API, HttpResponse, http, server } from './server';
import { REAL_TILE, renderApp } from './utils';

let downloads: { name: string; blob: Blob | null }[] = [];

/** jsdom's Blob has no text(); FileReader works for the blobs that fetch() returns in this environment. */
function readBlob(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(String(r.result));
    r.onerror = () => reject(r.error);
    r.readAsText(blob);
  });
}
let lastBlob: Blob | null = null;

beforeEach(() => {
  downloads = [];
  lastBlob = null;
  URL.createObjectURL = vi.fn((b: Blob | MediaSource) => {
    lastBlob = b as Blob;
    return 'blob:mock';
  });
  URL.revokeObjectURL = vi.fn();
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function (this: HTMLAnchorElement) {
    downloads.push({ name: this.download, blob: lastBlob });
  });
});
afterEach(() => vi.restoreAllMocks());

async function typeAndPredict(user: ReturnType<typeof userEvent.setup>, seq: string) {
  await user.type(screen.getByLabelText(/Tile sequence/), seq);
  await user.click(screen.getByRole('button', { name: 'Predict' }));
}

const before = (a: Element, b: Element) => Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);

describe('E2E-01 typed sequence', () => {
  it('shows the warning before the heatmap, 28 rows, the model id and the evidence label', async () => {
    const user = userEvent.setup();
    const { location } = renderApp('/');
    await typeAndPredict(user, REAL_TILE);
    const banner = await screen.findByTestId('domain-banner');
    expect(banner).toHaveAttribute('data-status', 'unknown');
    const warning = screen.getByTestId('warning-list');
    const heatmap = screen.getByTestId('heatmap');
    expect(before(banner, warning)).toBe(true);
    expect(before(warning, heatmap)).toBe(true);
    expect(warning).toHaveTextContent(/domain of this tile is unknown/);
    expect(heatmap.querySelectorAll('[role="row"]')).toHaveLength(29);
    expect(screen.getByTestId('evidence-label')).toHaveTextContent('development OOF benchmark, not external validation');
    expect(screen.getAllByText('mock-m3-ext4.0-platt-v1').length).toBeGreaterThan(0);
    // Privacy: the sequence is in no address, history state or browser storage.
    const loc = location();
    expect(JSON.stringify(loc)).not.toContain(REAL_TILE);
    expect(loc.pathname).toBe('/result');
    for (const store of [window.localStorage, window.sessionStorage]) {
      for (let i = 0; i < store.length; i += 1) expect(store.getItem(store.key(i)!)).not.toContain(REAL_TILE);
    }
  });

  it('forgets the sequence after a reload by design', async () => {
    renderApp('/result');
    expect(await screen.findByText(/There is no sequence in memory/)).toBeInTheDocument();
  });

  it('lowercase input is normalised and accepted', async () => {
    const user = userEvent.setup();
    renderApp('/');
    await typeAndPredict(user, ` ${REAL_TILE.toLowerCase()} `);
    expect(await screen.findByTestId('heatmap')).toBeInTheDocument();
  });
});

describe('E2E-08 invalid input', () => {
  it('blocks without a request, names the problem, and focuses the field', async () => {
    const user = userEvent.setup();
    const seen: string[] = [];
    server.events.on('request:start', ({ request }) => seen.push(request.url));
    renderApp('/');
    const input = screen.getByLabelText(/Tile sequence/);

    await typeAndPredict(user, 'DIMFLV');
    expect(screen.getByRole('alert')).toHaveTextContent('The sequence must have exactly 28 amino acids; it has 6.');
    expect(input).toHaveFocus();

    await user.clear(input);
    await user.type(input, 'DIMFLVBSSGSIGPENFSKMKTFMKNLV');
    expect(screen.getByRole('alert')).toHaveTextContent("Position 7: 'B' is not a standard amino acid.");
    await user.click(screen.getByRole('button', { name: 'Predict' }));
    expect(input).toHaveFocus();

    await user.clear(input);
    expect(screen.getByRole('button', { name: 'Predict' })).toBeDisabled();
    expect(screen.getByText(/Enter a sequence of exactly 28 amino acids/)).toBeInTheDocument();
    expect(seen.filter((u) => u.includes('/v1/predict'))).toHaveLength(0);
  });
});

describe('E2E-04 choose a protein', () => {
  it('searches a gene, picks a tile on the map and predicts it', async () => {
    const user = userEvent.setup();
    renderApp('/');
    await user.click(screen.getByRole('tab', { name: 'Choose a protein' }));
    await user.type(screen.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }), 'COL6');
    const option = await screen.findByRole('option', { name: /COL6A6/ });
    await user.click(option);

    expect(await screen.findByRole('heading', { name: 'COL6A6 (A6NMZ7)' })).toBeInTheDocument();
    expect(screen.getAllByRole('radio')).toHaveLength(98);
    expect(screen.getByRole('button', { name: 'Predict this tile' })).toBeDisabled();
    await user.click(screen.getByRole('radio', { name: /^tile 28,/ }));
    expect(screen.getByRole('heading', { name: /Selected: tile 28 \(residues 622–649\)/ })).toBeInTheDocument();
    expect(screen.getByText(REAL_TILE)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Predict this tile' }));

    expect(await screen.findByRole('heading', { name: /A6NMZ7 tile 28 \(residues 622–649\)/ })).toBeInTheDocument();
    expect(screen.getByTestId('warning-list')).toHaveTextContent('not an out-of-sample estimate');
    expect(screen.getByTestId('domain-banner')).toHaveAttribute('data-status', 'measured_in_domain');
  });

  it('says so when no protein matches and when the query is too short', async () => {
    const user = userEvent.setup();
    renderApp('/');
    await user.click(screen.getByRole('tab', { name: 'Choose a protein' }));
    await user.type(screen.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }), 'C');
    expect(screen.getByText('Type at least 2 characters.')).toBeInTheDocument();
    await user.type(screen.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }), 'ZZ');
    expect(await screen.findByText('No protein matches this search.')).toBeInTheDocument();
  });

  it('shows the list view for keyboard and screen-reader users, with non-scorable tiles disabled', async () => {
    const user = userEvent.setup();
    renderApp('/protein/A6NMZ7');
    await screen.findByRole('heading', { name: 'COL6A6 (A6NMZ7)' });
    await user.click(screen.getByRole('button', { name: 'Show a list of tiles' }));
    const row3 = screen.getByRole('button', { name: /Choose tile 3,/ });
    expect(row3).toBeDisabled();
    await user.click(screen.getByRole('button', { name: /Choose tile 28,/ }));
    expect(screen.getByRole('heading', { name: /Selected: tile 28/ })).toBeInTheDocument();
  });

  it('shows a message with the way out for an unknown accession and a tile out of range', async () => {
    renderApp('/protein/Q9ZZZZ');
    expect(await screen.findByText(/No reviewed human protein has the accession Q9ZZZZ/)).toBeInTheDocument();
  });

  it('states the valid range when the tile does not exist', async () => {
    renderApp('/result/uniprot/P60484/99');
    expect(await screen.findByText(/has tiles 1 to \d+/)).toBeInTheDocument();
    expect(screen.getByText(/Choose a tile within the range stated above/)).toBeInTheDocument();
  });
});

describe('E2E-09 out of domain', () => {
  it('refuses with the reason, then scores on request with a red banner and the warning in the export', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/A6NMZ7/5');
    const refusal = await screen.findByTestId('refusal');
    expect(refusal).toHaveTextContent('outside the domain of the model');
    expect(refusal).toHaveTextContent('4.8');
    expect(screen.queryByTestId('heatmap')).toBeNull();

    await user.click(within(refusal).getByRole('button', { name: 'Score anyway' }));
    const banner = await screen.findByTestId('override-banner');
    expect(banner).toHaveTextContent(/Out-of-domain override/);
    expect(screen.getByTestId('heatmap')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Export JSON' }));
    await waitFor(() => expect(downloads).toHaveLength(1));
    const json = JSON.parse(await readBlob(downloads[0]!.blob!)) as { warnings: { code: string }[] };
    expect(json.warnings.map((w) => w.code)).toContain('OUT_OF_DOMAIN_OVERRIDDEN');
  });

  it('"Choose another tile" returns to the tile picker', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/A6NMZ7/5');
    await user.click(await screen.findByRole('button', { name: 'Choose another tile' }));
    expect(await screen.findByRole('heading', { name: 'COL6A6 (A6NMZ7)' })).toBeInTheDocument();
  });
});

describe('E2E-03 / E2E-10 export', () => {
  it('downloads CSV and JSON with provenance, named after the model and tile, and the table matches', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('heatmap');

    await user.click(screen.getByRole('button', { name: 'Export CSV' }));
    await waitFor(() => expect(downloads).toHaveLength(1));
    expect(downloads[0]!.name).toMatch(/^degron-footprint_mock-m3-ext4\.0-platt-v1_A6NMZ7-t28_\d{4}-\d{2}-\d{2}\.csv$/);
    const csv = await readBlob(downloads[0]!.blob!);
    expect(csv).toMatch(/^# model_id=mock-m3-ext4\.0-platt-v1\n/);
    expect(csv).toContain('# evidence_label=development OOF benchmark');
    expect(csv).toContain('# warning=TRAINING_PEPTIDE');
    expect(csv.trim().split('\n').filter((l) => !l.startsWith('#') && !l.startsWith('peptide')).length).toBe(532);
    const row1 = screen.getByTestId('rank-table').querySelector('tbody tr')!;
    const rank1Raw = row1.querySelectorAll('td')[4]!.textContent!;
    const csvRank1 = csv.split('\n').find((l) => l.split(',')[7] === '1')!;
    expect(Number(csvRank1.split(',')[5]).toFixed(3)).toBe(rank1Raw);

    await user.click(screen.getByRole('button', { name: 'Export JSON' }));
    await waitFor(() => expect(downloads).toHaveLength(2));
    expect(downloads[1]!.name).toMatch(/\.json$/);
    const json = JSON.parse(await readBlob(downloads[1]!.blob!)) as { provenance: { weights_sha256: string }; cells: unknown[] };
    expect(json.cells).toHaveLength(532);
    expect(json.provenance.weights_sha256).toHaveLength(64);
  });

  it('does not put the typed sequence in the file name', async () => {
    const user = userEvent.setup();
    renderApp('/');
    await typeAndPredict(user, REAL_TILE);
    await screen.findByTestId('heatmap');
    await user.click(screen.getByRole('button', { name: 'Export CSV' }));
    await waitFor(() => expect(downloads).toHaveLength(1));
    expect(downloads[0]!.name).toMatch(/_user-seq_/);
    expect(downloads[0]!.name).not.toContain(REAL_TILE);
  });

  it('reports a failed export and keeps the result on screen', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('heatmap');
    server.use(http.post(`${API}/v1/export`, () => HttpResponse.error()));
    await user.click(screen.getByRole('button', { name: 'Export CSV' }));
    expect(await screen.findByText('The file could not be created. Your result is still here.')).toBeInTheDocument();
    expect(screen.getByTestId('heatmap')).toBeInTheDocument();
    expect(downloads).toHaveLength(0);
  });
});

describe('E2E-12 every result variant', () => {
  const variants: { name: string; route: string; typed?: boolean; status: string; warning: RegExp | null; override?: boolean }[] = [
    { name: 'typed (unknown)', route: '/', typed: true, status: 'unknown', warning: /unknown/ },
    { name: 'measured, training peptide', route: '/result/uniprot/A6NMZ7/28', status: 'measured_in_domain', warning: /not an out-of-sample estimate/ },
    { name: 'measured, ordinary', route: '/result/uniprot/P60484/1', status: 'measured_in_domain', warning: null },
    { name: 'unreliable', route: '/result/uniprot/A6NMZ7/7', status: 'measured_unreliable', warning: /too few reads/ },
    { name: 'predicted', route: '/result/uniprot/A6NMZ7/11', status: 'predicted_in_domain', warning: /predicted/ },
    { name: 'overridden', route: '/result/uniprot/A6NMZ7/12?x', status: 'predicted_out_of_domain', warning: /predicted/, override: true },
  ];

  it.each(variants)('$name: domain first, event near the probabilities, evidence label, disclaimer', async (v) => {
    const user = userEvent.setup();
    if (v.typed) {
      renderApp('/');
      await typeAndPredict(user, REAL_TILE);
    } else {
      renderApp(v.route.replace('?x', ''));
      if (v.override) await user.click(await screen.findByRole('button', { name: 'Score anyway' }));
    }
    const banner = await screen.findByTestId('domain-banner');
    expect(banner).toHaveAttribute('data-status', v.status);
    expect(before(banner, screen.getByTestId('heatmap'))).toBe(true);
    if (v.warning) {
      const w = screen.getByTestId('warning-list');
      expect(w).toHaveTextContent(v.warning);
      expect(before(w, screen.getByTestId('heatmap'))).toBe(true);
    } else {
      expect(screen.queryByTestId('warning-list')).toBeNull();
    }
    if (v.override) expect(screen.getByTestId('override-banner')).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: /P\(DeltaPSI >= 1\.0\)/ })).toBeInTheDocument();
    expect(screen.getByText(/Probability that the substitution raises PSI/)).toHaveTextContent('P(DeltaPSI >= 1.0)');
    expect(screen.getByTestId('evidence-label')).toHaveTextContent('not external validation');
    expect(screen.getByTestId('provenance')).toHaveTextContent('They are not probabilities of disease');
    expect(screen.getByTestId('provenance')).toHaveTextContent('Zhang et al. 2023 saturation mutagenesis');
  });

  it('never shows scores when the response lacks the domain status or the model version', async () => {
    const full = JSON.parse(handle('POST', '/v1/predict', {}, JSON.stringify({ uniprot_id: 'P60484', tile_index: 1 })).body) as Record<string, unknown>;
    delete full.domain;
    server.use(http.post(`${API}/v1/predict`, () => HttpResponse.json(full)));
    renderApp('/result/uniprot/P60484/1');
    const alert = await screen.findByTestId('unshowable');
    expect(alert).toHaveTextContent('The scores are not shown');
    expect(screen.queryByTestId('heatmap')).toBeNull();
    expect(screen.queryByTestId('rank-table')).toBeNull();
  });

  it('switches between probability and raw score and offers a table view', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/P60484/1');
    await screen.findByTestId('heatmap');
    await user.click(screen.getByRole('radio', { name: 'Raw score' }));
    expect(screen.getByText(/Raw score: regression output/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Show as a table' }));
    expect(screen.getByTestId('matrix-table')).toBeInTheDocument();
    expect(screen.queryByTestId('heatmap')).toBeNull();
  });
});

describe('E2E-05 measured layer', () => {
  it('outlines the cells and says the values are training data', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('heatmap');
    await user.click(screen.getByRole('checkbox', { name: 'Measured ΔPSI' }));
    expect(await screen.findAllByText(/part of the training data of this model; they are not a validation/)).not.toHaveLength(0);
    await waitFor(() => expect(screen.getByTestId('heatmap').querySelectorAll('.measured-ring').length).toBeGreaterThan(0));
  });

  it('says there is no measured data for an ordinary tile', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/P60484/1');
    await screen.findByTestId('heatmap');
    await user.click(screen.getByRole('checkbox', { name: 'Measured ΔPSI' }));
    expect(await screen.findByText('No measured data for this tile.')).toBeInTheDocument();
  });

  it('disables the layers with the reason for a typed sequence', async () => {
    const user = userEvent.setup();
    renderApp('/');
    await typeAndPredict(user, REAL_TILE);
    await screen.findByTestId('heatmap');
    expect(screen.getByRole('checkbox', { name: 'Measured ΔPSI' })).toBeDisabled();
    expect(screen.getByRole('checkbox', { name: 'ClinVar variants' })).toBeDisabled();
    expect(screen.getByText(/available only for a tile chosen from a protein/)).toBeInTheDocument();
  });
});

describe('E2E-06 ClinVar layer', () => {
  it('shows attribution and the diagnostic disclaimer beside the toggle before it is used, and in the hover card', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/A6NMZ7/28');
    await screen.findByTestId('heatmap');
    const toggle = screen.getByRole('checkbox', { name: 'ClinVar variants' });
    const notice = await waitFor(() => {
      const n = screen.getByTestId('clinvar-notice');
      expect(n).toHaveTextContent('NCBI ClinVar');
      return n;
    });
    expect(notice).toHaveTextContent('not for diagnostic use');
    expect(toggle.closest('fieldset')).toContainElement(notice);

    await user.click(toggle);
    await waitFor(() => expect(screen.getByTestId('heatmap').querySelectorAll('.glyph')).toHaveLength(6));
    expect(screen.getByRole('list', { name: 'ClinVar marker shapes' })).toHaveTextContent('likely pathogenic');
    act(() => screen.getByLabelText(/^position 10, G to R/).focus());
    const card = screen.getByTestId('cell-details');
    expect(card).toHaveTextContent('ClinVar 900002: G631R, pathogenic');
    expect(card).toHaveTextContent('not for diagnostic use');
  });
});

describe('E2E-07 model card and about', () => {
  it('reads the metrics from the API and lists the excluded sources', async () => {
    renderApp('/model');
    expect(await screen.findByRole('heading', { name: /Model mock-m3-ext4\.0-platt-v1/ })).toBeInTheDocument();
    const metrics = screen.getByTestId('metrics-table');
    expect(metrics).toHaveTextContent('oof_auroc.estimate');
    expect(metrics).toHaveTextContent('0.8208');
    expect(metrics).toHaveTextContent('top10_enrichment.ci95');
    expect(screen.getByText(/development OOF benchmark, not external validation/)).toBeInTheDocument();
    const notUsed = screen.getByTestId('not-used-sources');
    expect(within(notUsed).getAllByRole('listitem')).toHaveLength(4);
    expect(notUsed).toHaveTextContent('Koren et al. 2018, Cell, Table S4');
    expect(notUsed).toHaveTextContent('MetaDegron');
    expect(notUsed).toHaveTextContent('Larsen et al. 2025');
    expect(screen.getByTestId('card-markdown')).not.toHaveTextContent('Koren');
    expect(screen.getByText('mock-gate-r3-candidate')).toBeInTheDocument();
  });

  it('lists every data source with its licence and attribution', async () => {
    renderApp('/about');
    const table = await screen.findByTestId('sources-table');
    expect(within(table).getAllByRole('row')).toHaveLength(4);
    expect(table).toHaveTextContent('CC BY 4.0');
    expect(table).toHaveTextContent('NCBI terms of use (attribution required)');
    expect(table).toHaveTextContent('not for diagnostic use');
    expect(screen.getByText(/It gives no diagnosis, no risk of disease/)).toBeInTheDocument();
  });
});

describe('E2E-11 share link', () => {
  it('creates a link with the token only in the fragment, and opens it', async () => {
    const user = userEvent.setup();
    renderApp('/result/uniprot/P60484/1');
    await screen.findByTestId('heatmap');
    await user.click(screen.getByRole('button', { name: 'Create share link…' }));
    expect(screen.getByText(/This is the only action that stores a sequence/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Store and create link' }));
    const field = (await screen.findByLabelText('Share link')) as HTMLInputElement;
    const m = /\/shared\/([0-9a-f-]{36})#t=([A-Za-z0-9_-]{22,64})$/.exec(field.value);
    expect(m).not.toBeNull();
    const [, runId, token] = m!;
    expect(field.value.split('#')[0]).not.toContain(token);

    document.body.innerHTML = '';
    renderApp(`/shared/${runId}#t=${token}`);
    expect(await screen.findByText(/This is a shared result/)).toBeInTheDocument();
    expect(screen.getByTestId('heatmap')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Create share link…' })).toBeNull();
  });

  it('exports a shared run through the run endpoint', async () => {
    const user = userEvent.setup();
    const created = JSON.parse(handle('POST', '/v1/runs', {}, JSON.stringify({ uniprot_id: 'P60484', tile_index: 1 })).body) as { run_id: string; share_token: string };
    renderApp(`/shared/${created.run_id}#t=${created.share_token}`);
    await screen.findByTestId('heatmap');
    await user.click(screen.getByRole('button', { name: 'Export CSV' }));
    await waitFor(() => expect(downloads).toHaveLength(1));
    expect((await readBlob(downloads[0]!.blob!)).startsWith('# model_id=')).toBe(true);
  });

  it('shows the expiry message, a missing-token message, and a wrong-token message', async () => {
    const { unmount } = renderApp('/shared/00000000-0000-4000-8000-000000000410#t=AAAAAAAAAAAAAAAAAAAAAAAA');
    expect(await screen.findByText('This shared result has expired.')).toBeInTheDocument();
    unmount();
    renderApp('/shared/00000000-0000-4000-8000-000000000001');
    expect(await screen.findByText(/This link has no access token/)).toBeInTheDocument();
    document.body.innerHTML = '';
    renderApp('/shared/00000000-0000-4000-8000-000000000002#t=BBBBBBBBBBBBBBBBBBBBBBBB');
    expect(await screen.findByText(/No shared result matches this link/)).toBeInTheDocument();
  });
});

describe('service errors (ui-design §3.4)', () => {
  it('shows the countdown for a rate limit and disables the retry until it ends', async () => {
    server.use(http.post(`${API}/v1/predict`, () => HttpResponse.json({ code: 'RATE_LIMITED', message: 'Too many.', field: null }, { status: 429, headers: { 'Retry-After': '7' } })));
    renderApp('/result/uniprot/P60484/1');
    expect(await screen.findByText(/Too many requests\. Try again in 7 seconds\./)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Try again' })).toBeDisabled();
  });

  it('says the service is not ready on 503 and checks /healthz', async () => {
    server.use(http.post(`${API}/v1/predict`, () => HttpResponse.json({ code: 'SERVICE_UNAVAILABLE', message: 'x', field: null }, { status: 503 })));
    server.use(http.get(`${API}/healthz`, () => HttpResponse.json({ status: 'ok', version: 't', model_loaded: true, database: 'ok' })));
    renderApp('/result/uniprot/P60484/1');
    expect(await screen.findByText(/The service is not ready \(model or database unavailable\)\./)).toBeInTheDocument();
    expect(await screen.findByRole('button', { name: 'Retry' })).toBeInTheDocument();
  });

  it('survives a proxy error page that is not JSON', async () => {
    server.use(http.post(`${API}/v1/predict`, () => new HttpResponse('<html>502</html>', { status: 502, headers: { 'Content-Type': 'text/html' } })));
    renderApp('/result/uniprot/P60484/1');
    expect(await screen.findByText(/The service answered with HTTP 502/)).toBeInTheDocument();
  });

  it('says the service cannot be reached when the network fails', async () => {
    server.use(http.post(`${API}/v1/predict`, () => HttpResponse.error()));
    renderApp('/result/uniprot/P60484/1');
    expect(await screen.findByText(/The service could not be reached/)).toBeInTheDocument();
  });
});
