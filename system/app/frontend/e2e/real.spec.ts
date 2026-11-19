import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

// Integration with the real FastAPI service (`make -C system/app dev-api`, http://127.0.0.1:8000) through the Vite proxy.
// Run with: E2E_REAL=1 npx playwright test --project=chromium-desktop
// Expectations come from the database built by the backend ETL (A6NMZ7 has 98 tiles; tile 28 is a training peptide;
// tile 7 is measured outside the domain, PSI 5.10). They are checked against the live API, not typed from memory.

test.skip(process.env.E2E_REAL !== '1', 'needs the real backend');

const SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';

// The model that answers requests naming none (DF_DEFAULT_MODEL_ID may make it LoRA-D, plan 2.12); read from the service,
// not typed. LoRA-D scores a tile in tens of seconds on the CPU, so API calls and downloads get longer timeouts then.
let DEFAULT_MODEL = '';
let SLOW = false;
let EVIDENCE = '';
const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** plan-system 1.1: a slow model (LoRA-D once measured) asks before starting; confirm it when it appears. */
async function confirmIfSlow(page: import('@playwright/test').Page) {
  const start = page.getByRole('button', { name: 'Start anyway' });
  try {
    await start.waitFor({ state: 'visible', timeout: 1500 });
    await start.click();
  } catch {
    // fast model or not yet measured: no dialog
  }
}

test.beforeAll(async ({ playwright }, info) => {
  const api = await playwright.request.newContext({ baseURL: info.project.use.baseURL });
  const health = (await (await api.get('/healthz')).json()) as { default_model_id: string };
  DEFAULT_MODEL = health.default_model_id;
  const card = (await (await api.get(`/v1/models/${DEFAULT_MODEL}`)).json()) as { kind: string; evidence_label: string };
  SLOW = card.kind === 'torch_lora';
  EVIDENCE = card.evidence_label;
  await api.dispose();
});

test.beforeEach(async ({ page }) => {
  page.setDefaultTimeout(SLOW ? 300_000 : 30_000);
});

test('typed sequence: real domain warning, real evidence label and model id', async ({ page }) => {
  await page.goto('/');
  await page.getByLabel(/Tile sequence/).fill(SEQ);
  await page.getByRole('button', { name: 'Predict' }).click();
  await confirmIfSlow(page);
  await expect(page.getByTestId('heatmap')).toBeVisible();
  // R3 gate tier 2 (16 Nov 2026): this sequence predicts screen PSI ≈ 2.97 → P(in domain) ≈ 0.94
  await expect(page.getByTestId('domain-banner')).toHaveAttribute('data-status', 'predicted_in_domain');
  await expect(page.getByTestId('warning-list')).toContainText('comes from a gate model');
  // the evidence label of the model that answered (npz: development OOF benchmark; LoRA-D: post-hoc transfer), never stronger
  await expect(page.getByTestId('evidence-label')).toContainText(EVIDENCE);
  await expect(page.getByTestId('evidence-label')).toContainText('not external validation');
  await expect(page.getByTestId('provenance')).toContainText(DEFAULT_MODEL);
  await expect(page.getByTestId('provenance')).toContainText('Zhang et al. 2023');
});

test('stored tile: values on screen equal the API response, and the grid has all 532 cells', async ({ page, request }) => {
  const api = await request.post('/v1/predict', { data: { uniprot_id: 'A6NMZ7', tile_index: 28 }, timeout: SLOW ? 300_000 : 30_000 });
  expect(api.status()).toBe(200);
  const body = (await api.json()) as { cells: { position: number; mut_aa: string; p_dpsi_ge_1_calibrated: number; rank_in_tile: number }[] };
  await page.goto('/result/uniprot/A6NMZ7/28');
  await expect(page.getByTestId('warning-list')).toContainText('not an out-of-sample estimate');
  await expect(page.locator('[data-testid="heatmap"] [role="gridcell"]')).toHaveCount(28 * 20);
  const first = body.cells.find((c) => c.rank_in_tile === 1)!;
  const row = page.getByTestId('rank-table').locator('tbody tr').first();
  await expect(row.locator('td').nth(1)).toHaveText(String(first.position));
  await expect(row.locator('td').nth(3)).toHaveText(first.mut_aa);
  await expect(row.locator('td').nth(5)).toHaveText(first.p_dpsi_ge_1_calibrated.toFixed(3));
  expect(page.url()).not.toContain(SEQ);
});

test('search, tile map with all statuses, pick tile 28', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('tab', { name: 'Choose a protein' }).click();
  await page.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }).fill('COL6A6');
  await page.getByRole('option', { name: /COL6A6/ }).click();
  await expect(page.getByRole('radio')).toHaveCount(98);
  await expect(page.locator('.tile.hatched').first()).toBeVisible();
  await page.getByRole('radio', { name: /^tile 28,/ }).click();
  await page.getByRole('button', { name: 'Predict this tile' }).click();
  await confirmIfSlow(page);
  await expect(page.getByTestId('domain-banner')).toHaveAttribute('data-status', 'measured_in_domain');
});

test('a tile measured outside the domain is refused, and scored with a red banner on request', async ({ page }) => {
  await page.goto('/result/uniprot/A6NMZ7/7');
  await expect(page.getByTestId('refusal')).toContainText('outside the domain of the model');
  await page.getByRole('button', { name: 'Score anyway' }).click();
  await expect(page.getByTestId('override-banner')).toBeVisible();
  await expect(page.getByTestId('heatmap')).toBeVisible();
});

test('measured and ClinVar layers show real data with the attribution beside the toggle', async ({ page }) => {
  await page.goto('/result/uniprot/A6NMZ7/28');
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await expect(page.getByTestId('clinvar-notice')).toContainText(/ClinVar/i);
  await page.getByRole('checkbox', { name: 'Measured ΔPSI' }).check();
  await expect.poll(() => page.locator('.measured-ring').count()).toBeGreaterThan(0);
  await page.getByRole('checkbox', { name: 'ClinVar variants' }).check();
  await expect.poll(() => page.locator('[data-testid="heatmap"] .glyph').count()).toBeGreaterThan(0);
});

test('CSV and JSON exports come from the server and carry the provenance', async ({ page }) => {
  await page.goto('/result/uniprot/A6NMZ7/28');
  await expect(page.getByTestId('heatmap')).toBeVisible();
  const [csv] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Export CSV' }).click()]);
  const text = await (await import('node:fs/promises')).readFile((await csv.path())!, 'utf8');
  expect(text).toMatch(new RegExp(`^# model_id=${esc(DEFAULT_MODEL)}`, 'm'));
  expect(text.split('\n').filter((l) => l && !l.startsWith('#') && !l.startsWith('peptide'))).toHaveLength(532);
});

test('share link round trip', async ({ page, browser }) => {
  await page.goto('/result/uniprot/P60484/1');
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await page.getByRole('button', { name: 'Create share link…' }).click();
  await page.getByRole('button', { name: 'Store and create link' }).click();
  const link = await page.getByLabel('Share link', { exact: true }).inputValue();
  expect(link).toMatch(/\/shared\/[0-9a-f-]{36}#t=/);
  const other = await browser.newContext();
  const p2 = await other.newPage();
  await p2.goto(link);
  await expect(p2.getByText(/This is a shared result/)).toBeVisible();
  await expect(p2.getByTestId('heatmap')).toBeVisible();
  await other.close();
});

test('model card and sources come from the API', async ({ page }) => {
  await page.goto('/model');
  await expect(page.getByRole('heading', { name: `Model ${DEFAULT_MODEL}` })).toBeVisible();
  await expect(page.getByTestId('metrics-table').locator('tbody tr').first()).toBeVisible();
  // E2E-07: the list of sources that are deliberately not used comes from the API
  const notUsed = page.getByTestId('not-used-sources');
  await expect(notUsed).toContainText('Koren');
  await expect(notUsed).toContainText('MetaDegron');
  await expect(notUsed.locator('li')).toHaveCount(4);
  await page.goto('/about');
  await expect(page.getByTestId('sources-table').locator('tbody tr')).not.toHaveCount(0);
});

test('unknown accession and a tile that does not exist give a specific message', async ({ page }) => {
  await page.goto('/protein/Q9ZZZZ');
  await expect(page.locator('.banner.danger')).toBeVisible();
  await page.goto('/result/uniprot/P60484/9999');
  await expect(page.locator('.banner.danger')).toContainText(/9999|tile/i);
});

test('axe, light theme, on real-data pages', async ({ page }) => {
  for (const route of ['/', '/result/uniprot/A6NMZ7/28', '/model', '/about']) {
    await page.goto(route);
    await page.waitForLoadState('networkidle');
    const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    expect(res.violations.map((v) => `${v.id}: ${v.nodes[0]?.target.join(' ')}`), route).toEqual([]);
  }
});

// WP9 against the real service with the embedded worker (DF_EMBEDDED_WORKER=1 make dev-api): projects, a saved
// snapshot read back from SQLite, a batch job scored by the worker, an import and a comparison.
test('workspace on the real backend: save, reopen, batch job, import and compare', async ({ page, request }) => {
  const name = `E2E real ${Date.now()}`;
  const project = await (await request.post('/v1/projects', { data: { name } })).json() as { project_id: string };
  const pid = project.project_id;
  await page.goto('/result/uniprot/A6NMZ7/28');
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await page.getByRole('button', { name: 'Save to project' }).click();
  await page.getByRole('dialog').getByLabel('Project').selectOption(pid);
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
  await expect(page).toHaveURL(/\/analyses\//);
  const analysisUrl = page.url();
  await page.reload();
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await page.getByRole('tab', { name: 'ClinVar and annotations' }).click();
  await expect(page.getByTestId('annotation-status')).toHaveAttribute('data-state', /available|no_match|mapping_conflict/);

  await page.goto(`/new?mode=batch&project=${pid}`);
  await page.getByRole('textbox', { name: 'Peptides' }).fill(`>a\n${SEQ}\n>b\nACDE`);
  await page.getByRole('button', { name: 'Submit batch job' }).click();
  await confirmIfSlow(page);
  await expect(page.locator('.ui-pill[data-status="partial"]').first()).toBeVisible({ timeout: SLOW ? 300_000 : 30_000 });
  await expect(page.getByTestId('job-item-table')).toContainText('INVALID_LENGTH');

  const seq = (await (await request.get('/v1/proteins/A6NMZ7/tiles')).json() as { tiles: { tile_index: number; sequence: string }[] }).tiles.find((t) => t.tile_index === 28)!.sequence;
  const csv = ['peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id',
    `p,${seq},1,${seq[0]},A,0.5,r1`, `p,${seq},2,${seq[1]},A,0.1,r1`, `p,${seq},3,${seq[2]},A,1.2,r1`].join('\n');
  await page.goto(`/import?project=${pid}`);
  await page.getByLabel(/CSV or TSV file/).setInputFiles({ name: 'obs.csv', mimeType: 'text/csv', buffer: Buffer.from(csv) });
  await page.getByLabel(/Dataset name/).fill('Real GPS check');
  await page.getByLabel(/Source or citation/).fill('test');
  await page.getByLabel(/Reference description/).fill('A6NMZ7 tile 28');
  await page.getByRole('button', { name: 'Validate file' }).click();
  await expect(page.getByTestId('validation-report')).toContainText('Staged (not committed)');
  await page.getByRole('button', { name: 'Commit dataset' }).click();
  await expect(page.getByTestId('validation-report')).toContainText('Committed');
  await page.goto(analysisUrl);
  await page.getByRole('tab', { name: 'Comparison' }).click();
  const dataset = page.getByRole('combobox', { name: 'Dataset' });
  await dataset.selectOption((await dataset.locator('option', { hasText: 'Real GPS check' }).getAttribute('value'))!);
  await page.getByRole('button', { name: 'Compare' }).click();
  await expect(page.getByTestId('comparison-result').getByRole('table', { name: 'Matched substitutions' }).locator('tbody tr')).toHaveCount(3);
  // tidy up: the deletion goes through the dependency summary
  await page.goto(`/projects/${pid}`);
  await page.getByRole('button', { name: 'Delete…' }).click();
  await expect(page.getByTestId('delete-dependencies')).toContainText('saved analyses');
  await page.getByRole('button', { name: 'Delete permanently' }).click();
  await expect(page).toHaveURL(/\/projects$/);
});

// NF-06 / NFR-03 on the real service: click Predict → painted heatmap, 20 runs, Chromium on this host.
test('NF-06 real backend click-to-heatmap', async ({ page }, info) => {
  // NF-06 is measured on the npz default; LoRA-D latency is measured separately (tests/results/latency-lora.json)
  test.skip(SLOW, 'default model is LoRA-D: NF-06 would take 20 × ~40 s and would overwrite the npz measurement');
  const { writeFileSync } = await import('node:fs');
  const ms: number[] = [];
  for (let i = 0; i < 20; i += 1) {
    await page.goto('/');
    await page.getByLabel(/Tile sequence/).fill(SEQ);
    const t0 = Date.now();
    await page.getByRole('button', { name: 'Predict' }).click();       // NF-06 runs only with a fast default: no dialog
    await page.locator('[data-testid="heatmap"] [role="gridcell"]').first().waitFor();
    ms.push(Date.now() - t0);
  }
  const sorted = [...ms].sort((a, b) => a - b);
  const p95 = sorted[Math.ceil(0.95 * sorted.length) - 1]!;
  writeFileSync('../tests/results/nf06-real.json', JSON.stringify({ date: new Date().toISOString(), browser: info.project.name, runs: ms.length,
    p50_ms: sorted[Math.floor(sorted.length / 2)], p95_ms: p95, max_ms: sorted.at(-1), proposed_p95_ms: 1500,
    note: 'Vite dev server proxy to uvicorn on loopback, WSL2 laptop; includes client routing and SVG paint' }, null, 2) + '\n');
  expect(p95).toBeLessThan(5000);
});

/** GET that waits out the service's own rate limit (429 + Retry-After) when the suite has just made many requests. */
async function getJson<T>(request: import('@playwright/test').APIRequestContext, url: string): Promise<T> {
  for (let i = 0; i < 5; i += 1) {
    const r = await request.get(url);
    if (r.status() !== 429) return (await r.json()) as T;
    await new Promise((res) => setTimeout(res, (Number(r.headers()['retry-after'] ?? '5') + 1) * 1000));
  }
  throw new Error(`${url}: still rate limited`);
}

test('MSEL-04 one tile with both models from the interface; the saved snapshot pins the chosen model', async ({ page, request }) => {
  const items = (await getJson<{ items: { model_id: string; role: string; serving: boolean; kind: string }[] }>(request, '/v1/models')).items;
  const serving = items.filter((m) => m.role === 'effect' && m.serving);
  test.skip(serving.length < 2, 'needs two serving effect models (WITH_LORA=1)');
  test.setTimeout(600_000);
  page.setDefaultTimeout(300_000);
  const other = serving.find((m) => m.model_id !== DEFAULT_MODEL)!;
  const project = await (await request.post('/v1/projects', { data: { name: `MSEL-04 ${Date.now()}` } })).json() as { project_id: string };
  await page.goto('/result/uniprot/A6NMZ7/1');
  await confirmIfSlow(page);
  await expect(page.getByTestId('provenance')).toContainText(DEFAULT_MODEL);
  const rerun = page.getByTestId('rerun-model');
  await rerun.getByRole('combobox').selectOption(other.model_id);
  await rerun.getByRole('button', { name: 'Run with another model' }).click();
  await confirmIfSlow(page);
  await expect(page).toHaveURL(new RegExp(`/result/uniprot/A6NMZ7/1\\?model=${esc(other.model_id)}$`));
  await expect(page.getByTestId('provenance')).toContainText(other.model_id);
  await page.getByRole('button', { name: 'Save to project' }).click();
  await page.getByRole('dialog').getByLabel('Project').selectOption(project.project_id);
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
  await expect(page).toHaveURL(/\/analyses\//);
  const aid = page.url().split('/analyses/')[1]!;
  const saved = await getJson<{ result: { provenance: { model_id: string } } }>(request, `/v1/analyses/${aid}`);
  expect(saved.result.provenance.model_id).toBe(other.model_id);
  // the model list now has a measured time for both models (expected_tile_seconds)
  const after = (await getJson<{ items: { model_id: string; expected_tile_seconds: number | null }[] }>(request, '/v1/models')).items;
  for (const m of serving) expect(after.find((x) => x.model_id === m.model_id)?.expected_tile_seconds).not.toBeNull();
});

test('RPT real backend: the HTML report of a saved analysis renders with its own CSP and no request elsewhere', async ({ page, request }) => {
  const project = await (await request.post('/v1/projects', { data: { name: `RPT ${Date.now()}` } })).json() as { project_id: string };
  const saved = await (await request.post(`/v1/projects/${project.project_id}/analyses`, { data: { request: { uniprot_id: 'A6NMZ7', tile_index: 28 } }, timeout: 300_000 })).json() as { analysis_id: string };
  const violations: string[] = [];
  const outside: string[] = [];
  page.on('console', (m) => { if (/Content Security Policy|violates/i.test(m.text())) violations.push(m.text()); });
  page.on('request', (r) => { if (!r.url().includes(`/v1/analyses/${saved.analysis_id}/report`)) outside.push(r.url()); });
  const resp = await page.goto(`/v1/analyses/${saved.analysis_id}/report?format=html`);
  expect(resp?.status()).toBe(200);
  expect(resp?.headers()['content-security-policy']).toContain("style-src 'unsafe-inline'");
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Degron Footprint — analysis report');
  await expect(page.getByText('Read this first')).toBeVisible();
  await expect(page.locator('svg.matrix > rect')).toHaveCount(560);
  expect(await page.locator('body').evaluate((b) => getComputedStyle(b).maxWidth)).toBe('960px');   // inline styles applied
  expect(violations).toEqual([]);
  expect(outside).toEqual([]);
});

test('CMP real backend: two models on one tile, saved comparison opens with its metrics and exports both provenances', async ({ page, request }) => {
  const items = (await getJson<{ items: { model_id: string; role: string; serving: boolean }[] }>(request, '/v1/models')).items;
  const serving = items.filter((m) => m.role === 'effect' && m.serving);
  test.skip(serving.length < 2, 'needs two serving effect models (WITH_LORA=1)');
  test.setTimeout(600_000);
  const project = await (await request.post('/v1/projects', { data: { name: `CMP ${Date.now()}` } })).json() as { project_id: string };
  const save = async (model: string) => (await (await request.post(`/v1/projects/${project.project_id}/analyses`,
    { data: { request: { uniprot_id: 'A6NMZ7', tile_index: 1, model_id: model } }, timeout: 300_000 })).json()) as { analysis_id: string };
  const a = await save(serving[0]!.model_id);
  const b = await save(serving[1]!.model_id);
  const r = await request.post('/v1/analyses/compare', { data: { analysis_a: a.analysis_id, analysis_b: b.analysis_id, save: true } });
  expect(r.status()).toBe(201);
  const cmp = (await r.json()) as { comparison_id: string; metrics: { n_cells: number; spearman_raw: number | null } };
  expect(cmp.metrics.n_cells).toBe(532);
  await page.goto(`/model-comparisons/${cmp.comparison_id}`);
  await expect(page.getByTestId('model-comparison-label')).toContainText('does not tell which model is right');
  await expect(page.getByTestId('model-side-a')).toContainText(serving[0]!.model_id);
  await expect(page.getByTestId('model-side-b')).toContainText(serving[1]!.model_id);
  const csv = await (await request.get(`/v1/model-comparisons/${cmp.comparison_id}/export?format=csv`)).text();
  expect(csv).toContain(`# a_model_id=${serving[0]!.model_id}`);
  expect(csv).toContain(`# b_model_id=${serving[1]!.model_id}`);
});
