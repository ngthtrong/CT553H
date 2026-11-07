import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

// Integration with the real FastAPI service (`make -C system/app dev-api`, http://127.0.0.1:8000) through the Vite proxy.
// Run with: E2E_REAL=1 npx playwright test --project=chromium-desktop
// Expectations come from the database built by the backend ETL (A6NMZ7 has 98 tiles; tile 28 is a training peptide;
// tile 7 is measured outside the domain, PSI 5.10). They are checked against the live API, not typed from memory.

test.skip(process.env.E2E_REAL !== '1', 'needs the real backend');

const SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';

test('typed sequence: real domain warning, real evidence label and model id', async ({ page }) => {
  await page.goto('/');
  await page.getByLabel(/Tile sequence/).fill(SEQ);
  await page.getByRole('button', { name: 'Predict' }).click();
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await expect(page.getByTestId('domain-banner')).toHaveAttribute('data-status', 'unknown');
  await expect(page.getByTestId('warning-list')).toContainText('not measured in the GPS screen');
  await expect(page.getByTestId('evidence-label')).toContainText('development OOF benchmark, not external validation');
  await expect(page.getByTestId('provenance')).toContainText('m3-ext4.0-platt-v1');
  await expect(page.getByTestId('provenance')).toContainText('Zhang et al. 2023');
});

test('stored tile: values on screen equal the API response, and the grid has all 532 cells', async ({ page, request }) => {
  const api = await request.post('/v1/predict', { data: { uniprot_id: 'A6NMZ7', tile_index: 28 } });
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
  expect(text).toMatch(/^# model_id=m3-ext4\.0-platt-v1/m);
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
  await expect(page.getByRole('heading', { name: /Model m3-ext4\.0-platt-v1/ })).toBeVisible();
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
