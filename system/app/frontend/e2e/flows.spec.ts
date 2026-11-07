import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

const SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';

// SEC-03: under the production policy (E2E_PREVIEW=1) the page must not trigger a single CSP violation.
test.beforeEach(({ page }) => {
  page.on('console', (m) => {
    if (/Content Security Policy|violates the following/i.test(m.text())) throw new Error(`CSP violation: ${m.text()}`);
  });
  page.on('pageerror', (e) => {
    throw e;
  });
});

async function predictTyped(page: Page) {
  await page.goto('/');
  await page.getByLabel(/Tile sequence/).fill(SEQ);
  await page.getByRole('button', { name: 'Predict' }).click();
  await expect(page.getByTestId('heatmap')).toBeVisible();
}

test('E2E-01 typed sequence: domain and warning come first, 29 grid rows, nothing in the address or storage', async ({ page }) => {
  await predictTyped(page);
  await expect(page.getByTestId('domain-banner')).toHaveAttribute('data-status', 'unknown');
  await expect(page.getByTestId('warning-list')).toContainText('domain of this tile is unknown');
  const order = await page.evaluate(() => {
    const pos = (id: string) => document.querySelector(`[data-testid="${id}"]`)!.getBoundingClientRect().top;
    return [pos('domain-banner'), pos('warning-list'), pos('heatmap')];
  });
  expect(order[0]).toBeLessThan(order[1]!);
  expect(order[1]).toBeLessThan(order[2]!);
  expect(await page.locator('[data-testid="heatmap"] [role="row"]').count()).toBe(29);
  expect(page.url()).not.toContain(SEQ);
  const stored = await page.evaluate(() => JSON.stringify([{ ...localStorage }, { ...sessionStorage }, history.state]));
  expect(stored).not.toContain(SEQ);
  await expect(page.getByTestId('evidence-label')).toContainText('not external validation');
});

test('E2E-08 invalid input: no request is sent for what the client can check', async ({ page }) => {
  const requests: string[] = [];
  page.on('request', (r) => requests.push(r.url()));
  await page.goto('/');
  const input = page.getByLabel(/Tile sequence/);
  await input.fill('DIMFLVB');
  await expect(page.getByRole('alert')).toContainText("Position 7: 'B' is not a standard amino acid.");
  await page.getByRole('button', { name: 'Predict' }).click();
  await expect(input).toBeFocused();
  expect(requests.filter((u) => u.includes('/v1/predict'))).toHaveLength(0);
});

test('E2E-04 protein route: search, pick a tile, predict', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('tab', { name: 'Choose a protein' }).click();
  await page.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }).fill('COL6');
  await page.getByRole('option', { name: /COL6A6/ }).click();
  await expect(page.getByRole('radio')).toHaveCount(98);
  await page.getByRole('radio', { name: /^tile 28,/ }).click();
  await page.getByRole('button', { name: 'Predict this tile' }).click();
  await expect(page).toHaveURL(/\/result\/uniprot\/A6NMZ7\/28$/);
  await expect(page.getByTestId('warning-list')).toContainText('not an out-of-sample estimate');
});

test('E2E-09 out of domain: refusal, override, banner and the warning in the JSON export', async ({ page }) => {
  await page.goto('/result/uniprot/A6NMZ7/5');
  await expect(page.getByTestId('refusal')).toContainText('outside the domain of the model');
  await page.getByRole('button', { name: 'Score anyway' }).click();
  await expect(page.getByTestId('override-banner')).toBeVisible();
  const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Export JSON' }).click()]);
  expect(download.suggestedFilename()).toMatch(/^degron-footprint_.*_A6NMZ7-t5_\d{4}-\d{2}-\d{2}\.json$/);
  const body = JSON.parse(await (await import('node:fs/promises')).readFile((await download.path())!, 'utf8')) as { warnings: { code: string }[] };
  expect(body.warnings.map((w) => w.code)).toContain('OUT_OF_DOMAIN_OVERRIDDEN');
});

test('E2E-03 export CSV carries the provenance and 532 rows', async ({ page }) => {
  await page.goto('/result/uniprot/A6NMZ7/28');
  await expect(page.getByTestId('heatmap')).toBeVisible();
  const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Export CSV' }).click()]);
  const text = await (await import('node:fs/promises')).readFile((await download.path())!, 'utf8');
  expect(text).toMatch(/^# model_id=/);
  expect(text.split('\n').filter((l) => l && !l.startsWith('#') && !l.startsWith('peptide'))).toHaveLength(532);
});

test('E2E-10 a failed export keeps the result', async ({ page }) => {
  await page.goto('/result/uniprot/A6NMZ7/28');
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await page.route('**/v1/export', (route) => route.abort());
  await page.getByRole('button', { name: 'Export CSV' }).click();
  await expect(page.getByText('The file could not be created. Your result is still here.')).toBeVisible();
  await expect(page.getByTestId('heatmap')).toBeVisible();
});

test('E2E-11 share link: the token is in the fragment and opens in a new context', async ({ page, browser }) => {
  await page.goto('/result/uniprot/P60484/1');
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await page.getByRole('button', { name: 'Create share link…' }).click();
  await page.getByRole('button', { name: 'Store and create link' }).click();
  const link = await page.getByLabel('Share link', { exact: true }).inputValue();
  expect(link).toMatch(/\/shared\/[0-9a-f-]{36}#t=[A-Za-z0-9_-]{22,64}$/);
  const other = await browser.newContext();
  const p2 = await other.newPage();
  await p2.goto(link);
  await expect(p2.getByText(/This is a shared result/)).toBeVisible();
  await other.close();
});

test('A11Y-02 keyboard only: UC-01 to UC-03 without a mouse', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab'); // skip link
  await page.keyboard.press('Tab'); // brand
  await page.getByLabel(/Tile sequence/).focus();
  await page.keyboard.type(SEQ);
  await page.keyboard.press('Enter');
  await expect(page.getByTestId('heatmap')).toBeVisible();
  // Enter the grid with the keyboard, move, select a cell, and see the ranking row follow.
  await page.locator('[data-testid="heatmap"] [role="gridcell"][tabindex="0"]').focus();
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('ArrowRight');
  await page.keyboard.press('Enter');
  await expect(page.getByTestId('rank-table').locator('tr[aria-current="true"]')).toHaveCount(1);
  await page.getByRole('button', { name: 'Export CSV' }).focus();
  const [download] = await Promise.all([page.waitForEvent('download'), page.keyboard.press('Enter')]);
  expect(download.suggestedFilename()).toMatch(/_user-seq_/);
});

for (const theme of ['light', 'dark'] as const) {
  test(`A11Y-01 axe including colour contrast on every page, ${theme} theme`, async ({ page }) => {
    await page.addInitScript((t) => localStorage.setItem('df-theme', t), theme);
    const pages = ['/', '/protein/A6NMZ7', '/result/uniprot/A6NMZ7/28', '/result/uniprot/A6NMZ7/7', '/result/uniprot/A6NMZ7/5', '/model', '/about'];
    for (const route of pages) {
      await page.goto(route);
      await page.waitForLoadState('networkidle');
      if (route.includes('/28')) {
        await page.getByRole('checkbox', { name: 'ClinVar variants' }).check();
        await page.getByRole('checkbox', { name: 'Measured ΔPSI' }).check();
        await expect(page.getByRole('list', { name: 'ClinVar marker shapes' })).toBeVisible();
      }
      const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
      const bad = res.violations.map((v) => `${v.id} (${v.impact}): ${v.nodes.length} node(s), e.g. ${v.nodes[0]?.target.join(' ')}`);
      expect(bad, `${route} in ${theme}`).toEqual([]);
    }
  });
}

test('NF-06 (mock) time from clicking Predict to the painted heatmap', async ({ page }) => {
  const ms: number[] = [];
  for (let i = 0; i < 5; i += 1) {
    await page.goto('/');
    await page.getByLabel(/Tile sequence/).fill(SEQ);
    const t = await page.evaluate(
      () =>
        new Promise<number>((resolve) => {
          const start = performance.now();
          const obs = new MutationObserver(() => {
            if (document.querySelector('[data-testid="heatmap"] [role="gridcell"]')) {
              obs.disconnect();
              requestAnimationFrame(() => requestAnimationFrame(() => resolve(performance.now() - start)));
            }
          });
          obs.observe(document.body, { childList: true, subtree: true });
          (document.querySelector('button[type="submit"]') as HTMLButtonElement).click();
        }),
    );
    ms.push(t);
  }
  console.log(`NF-06 mock-API render times (ms): ${ms.map((x) => x.toFixed(0)).join(', ')}`);
  // Reported, not asserted against NFR-03: this runs on the mock, on this machine, and is not the measurement of record.
  expect(Math.max(...ms)).toBeLessThan(5000);
});
