import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

// WP9 flows on the mock API (synthetic numbers): projects, save/reopen/rerun, batch and protein jobs, import and
// comparison, deletion with a dependency summary. Every test makes its own project, since the mock keeps state.
const SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';
const SEQ2 = 'MKTAYIAKQRQISFVKSHFSRQLEERLG';

async function newProject(page: Page, name: string): Promise<string> {
  await page.goto('/projects');
  await page.getByRole('button', { name: 'New project' }).click();
  await page.getByRole('dialog').getByLabel(/Name/).fill(name);
  await page.getByRole('dialog').getByRole('button', { name: 'Create project' }).click();
  await expect(page.getByRole('heading', { level: 1, name })).toBeVisible();
  return page.url().split('/projects/')[1]!.split('?')[0]!;
}

async function noBiologyInBrowserState(page: Page) {
  expect(page.url()).not.toContain(SEQ);
  const stored = await page.evaluate(() => JSON.stringify({ ...localStorage }) + JSON.stringify({ ...sessionStorage }));
  expect(stored).not.toContain(SEQ);
  expect(stored).not.toContain(SEQ2);
}

test('UC-10 E2E projects: create, rename, empty history', async ({ page }) => {
  const pid = await newProject(page, `Proj ${Date.now()}`);
  await page.getByRole('button', { name: 'Rename' }).click();
  await page.getByRole('dialog').getByLabel(/Name/).fill('Renamed project');
  await page.getByRole('dialog').getByRole('button', { name: 'Save name' }).click();
  await expect(page.getByRole('heading', { level: 1, name: 'Renamed project' })).toBeVisible();
  await expect(page.getByText('No saved analysis')).toBeVisible();
  await page.goto('/projects');
  await expect(page.getByTestId('project-list').getByRole('link', { name: 'Renamed project' })).toBeVisible();
  expect(pid).toMatch(/^[0-9a-f-]{36}$/);
});

test('UC-01 → UC-03/10: save a preview, reopen the snapshot after reload, run again as a new record', async ({ page }) => {
  const pid = await newProject(page, `Save ${Date.now()}`);
  await page.goto('/');
  await page.getByLabel(/Tile sequence/).fill(SEQ);
  await page.getByRole('button', { name: 'Predict' }).click();
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await expect(page.getByTestId('footprint-track')).toBeVisible();
  await page.getByRole('button', { name: 'Save to project' }).click();
  await page.getByRole('dialog').getByLabel('Project').selectOption(pid);
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
  await expect(page).toHaveURL(/\/analyses\/[0-9a-f-]{36}$/);
  await expect(page.locator('.ui-banner__title', { hasText: 'Saved snapshot' })).toBeVisible();
  await page.reload();
  await expect(page.getByTestId('heatmap')).toBeVisible();                      // read back from the server
  await page.getByRole('tab', { name: 'ClinVar and annotations' }).click();
  await expect(page.getByTestId('annotation-status')).toHaveAttribute('data-state', 'mapping_unavailable');
  await page.getByRole('tab', { name: 'Matrix and ranking' }).click();
  const first = page.url();
  await page.getByRole('button', { name: 'Run again' }).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
  await expect(page).not.toHaveURL(first);
  await expect(page.getByRole('link', { name: /analysis [0-9a-f]{8}/ })).toBeVisible();
  await page.goto(`/projects/${pid}`);
  await expect(page.getByRole('table', { name: 'Analysis history' }).locator('tbody tr')).toHaveCount(2);
  await noBiologyInBrowserState(page);
});

test('UC-08 peptide batch: preview, submit, progress to partial, open one matrix', async ({ page }) => {
  const pid = await newProject(page, `Batch ${Date.now()}`);
  await page.goto(`/new?mode=batch&project=${pid}`);
  await page.getByRole('textbox', { name: 'Peptides' }).fill(`>pep-a first\n${SEQ}\n>pep-b\nACDE\n>pep-a\n${SEQ2}`);
  const preview = page.getByTestId('batch-preview');
  await expect(preview).toContainText('3 of at most 100');
  await expect(preview.getByText('Invalid (listed as refused)').locator('xpath=following-sibling::dd[1]')).toHaveText('1');
  await page.getByRole('button', { name: 'Submit batch job' }).click();
  await expect(page).toHaveURL(/\/jobs\//);
  await expect(page.getByRole('heading', { name: 'Peptide batch job' })).toBeVisible();
  await expect(page.locator('.ui-pill[data-status="partial"]').first()).toBeVisible({ timeout: 20_000 });
  const table = page.getByTestId('job-item-table');
  await expect(table.getByText('pep-a-2')).toBeVisible();                       // duplicate header made unique
  await expect(table.getByText('INVALID_LENGTH')).toBeVisible();
  await table.getByRole('link', { name: 'Open matrix' }).first().click();
  await expect(page.getByTestId('heatmap')).toBeVisible();
  await noBiologyInBrowserState(page);
});

test('UC-08 whole protein: windows, uncovered C-terminus, coverage on the job page', async ({ page }) => {
  const pid = await newProject(page, `Protein ${Date.now()}`);
  await page.goto(`/new?mode=protein&project=${pid}`);
  await page.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }).fill('PTEN');
  await page.getByRole('option', { name: /PTEN/ }).click();
  const preview = page.getByTestId('protein-preview');
  await expect(preview).toContainText('17 tiles of 28 residues');
  await expect(preview).toContainText('residues 397–403');
  await page.getByRole('button', { name: 'Submit protein job' }).click();
  await expect(page.getByTestId('protein-coverage')).toContainText('397–403');
  await expect(page.getByRole('progressbar', { name: 'Items finished' })).toBeVisible();
});

test('UC-09 import and UC-05 comparison: validate, commit, compare a saved analysis', async ({ page }) => {
  const pid = await newProject(page, `Import ${Date.now()}`);
  // save an analysis to compare with
  await page.goto('/');
  await page.getByLabel(/Tile sequence/).fill(SEQ);
  await page.getByRole('button', { name: 'Predict' }).click();
  await page.getByRole('button', { name: 'Save to project' }).click();
  await page.getByRole('dialog').getByLabel('Project').selectOption(pid);
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
  await expect(page).toHaveURL(/\/analyses\//);
  const analysisUrl = page.url();
  // import a small dataset with one warning (formula-like id) and one blocking-free set of rows
  const csv = ['peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id,missing_reason',
    `=p1,${SEQ},1,D,A,0.5,r1,`, `p1,${SEQ},1,D,A,0.7,r2,`, `p1,${SEQ},2,I,A,0.2,r1,`, `p1,${SEQ},3,M,A,,r1,below detection`].join('\n');
  await page.goto(`/import?project=${pid}`);
  await page.getByLabel(/CSV or TSV file/).setInputFiles({ name: 'obs.csv', mimeType: 'text/csv', buffer: Buffer.from(csv) });
  await page.getByLabel(/Dataset name/).fill('Follow-up GPS');
  await page.getByLabel(/Source or citation/).fill('Lab book 12');
  await page.getByLabel(/Reference description/).fill('A6NMZ7 tile 28');
  await page.getByRole('button', { name: 'Validate file' }).click();
  const report = page.getByTestId('validation-report');
  await expect(report).toContainText('Staged (not committed)');
  await expect(report).toContainText('FORMULA_TEXT');
  await expect(page.getByRole('button', { name: 'Commit dataset' })).toBeDisabled();
  await page.getByLabel(/I have read the warnings/).check();
  await page.getByRole('button', { name: 'Commit dataset' }).click();
  await expect(page).toHaveURL(/\/datasets\//);
  await expect(page.getByTestId('validation-report')).toContainText('Committed');
  // compare
  await page.goto(analysisUrl);
  await page.getByRole('tab', { name: 'Comparison' }).click();
  const dataset = page.getByRole('combobox', { name: 'Dataset' });
  const value = await dataset.locator('option', { hasText: 'Follow-up GPS' }).getAttribute('value');
  await dataset.selectOption(value!);
  await page.getByRole('button', { name: 'Compare' }).click();
  const result = page.getByTestId('comparison-result');
  await expect(result).toContainText('Matched substitutions (n)');
  await expect(result).toContainText('not used to retrain the model');
  await expect(result.getByRole('table', { name: 'Matched substitutions' }).locator('tbody tr')).toHaveCount(2);
  // plan-system 2.3: charts of the matched pairs, after the "comparison only" label, with n; axe on the result
  const charts = result.getByTestId('comparison-charts');
  await expect(charts).toBeVisible();
  await expect(charts.getByTestId('chart-scatter').locator('circle')).toHaveCount(2);
  await expect(charts.getByTestId('chart-scatter')).toContainText('n = 2');
  const order = await page.evaluate(() => {
    const note = document.querySelector('[data-testid="comparison-note"]')!;
    const chart = document.querySelector('[data-testid="comparison-charts"]')!;
    return Boolean(note.compareDocumentPosition(chart) & Node.DOCUMENT_POSITION_FOLLOWING);
  });
  expect(order).toBe(true);
  const res = await new AxeBuilder({ page }).include('[data-testid="comparison-result"]').withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  expect(res.violations.map((v) => `${v.id}: ${v.nodes[0]?.target.join(' ')}`)).toEqual([]);
});

test('UC-10 HIST-03: deleting a project shows what goes with it before deleting', async ({ page }) => {
  const pid = await newProject(page, `Delete ${Date.now()}`);
  await page.goto('/');
  await page.getByLabel(/Tile sequence/).fill(SEQ);
  await page.getByRole('button', { name: 'Predict' }).click();
  await page.getByRole('button', { name: 'Save to project' }).click();
  await page.getByRole('dialog').getByLabel('Project').selectOption(pid);
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
  await page.goto(`/projects/${pid}`);
  await page.getByRole('button', { name: 'Delete…' }).click();
  await expect(page.getByTestId('delete-dependencies')).toContainText('1 saved analyses');
  await page.getByRole('button', { name: 'Keep it' }).click();
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  await page.getByRole('button', { name: 'Delete…' }).click();
  await page.getByRole('button', { name: 'Delete permanently' }).click();
  await expect(page).toHaveURL(/\/projects$/);
});

for (const theme of ['light', 'dark'] as const) {
  test(`A11Y-01 axe on the workspace screens, ${theme} theme`, async ({ page }) => {
    await page.addInitScript((t) => localStorage.setItem('df-theme', t), theme);
    const pid = await newProject(page, `Axe ${theme} ${Date.now()}`);
    const routes = ['/projects', `/projects/${pid}`, `/projects/${pid}?tab=jobs`, `/projects/${pid}?tab=datasets`, `/new?mode=batch&project=${pid}`,
      `/new?mode=protein&project=${pid}`, `/import?project=${pid}`, '/sources'];
    for (const route of routes) {
      await page.goto(route);
      await page.waitForLoadState('networkidle');
      const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
      const bad = res.violations.map((v) => `${v.id} (${v.impact}): ${v.nodes.length} node(s), e.g. ${v.nodes[0]?.target.join(' ')}`);
      expect(bad, `${route} in ${theme}`).toEqual([]);
    }
  });
}

test('A11Y-02 keyboard only: create a project, submit a batch, open a result (UC-10, UC-08)', async ({ page }) => {
  await page.goto('/projects');
  await page.getByRole('button', { name: 'New project' }).focus();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.keyboard.type(`Keys ${Date.now()}`);                 // the dialog puts focus in its first field
  await page.keyboard.press('Enter');                               // submits the form
  await expect(page).toHaveURL(/\/projects\/[0-9a-f-]{36}$/);
  await page.getByRole('tab', { name: /Analysis history/ }).focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.getByRole('tab', { name: /Jobs/ })).toHaveAttribute('aria-selected', 'true');
  await page.getByRole('button', { name: 'New analysis' }).focus();
  await page.keyboard.press('Enter');
  await page.getByRole('radio', { name: /Peptide batch/ }).focus();
  await page.keyboard.press('Space');
  await page.getByRole('textbox', { name: 'Peptides' }).focus();
  await page.keyboard.type(SEQ);
  await page.getByRole('button', { name: 'Submit batch job' }).focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('.ui-pill[data-status="completed"]').first()).toBeVisible({ timeout: 20_000 });
  await page.getByRole('link', { name: 'Open matrix' }).first().focus();
  await page.keyboard.press('Enter');
  await expect(page.getByTestId('heatmap')).toBeVisible();
});

for (const theme of ['light', 'dark'] as const) {
  test(`VIZ-03 protein footprint after a whole-protein job: label first, opens a tile, axe (${theme})`, async ({ page }) => {
    test.setTimeout(90_000);
    await page.addInitScript((t) => localStorage.setItem('df-theme', t), theme);
    const pid = await newProject(page, `Footprint ${theme} ${Date.now()}`);
    await page.goto(`/new?mode=protein&project=${pid}`);
    await page.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }).fill('PTEN');
    await page.getByRole('option', { name: /PTEN/ }).click();
    await page.getByRole('checkbox', { name: /Score out-of-domain tiles anyway/ }).check();
    await page.getByRole('button', { name: 'Submit protein job' }).click();
    const fp = page.getByTestId('protein-footprint');
    await expect(fp).toBeVisible({ timeout: 60_000 });
    await expect(fp.getByTestId('protein-footprint-label')).toContainText('not a phenotype of the whole protein');
    await expect(fp.getByTestId('pfp-tile')).toHaveCount(17);
    const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    expect(res.violations.map((v) => `${v.id}: ${v.nodes[0]?.target.join(' ')}`)).toEqual([]);
    await fp.getByRole('button', { name: 'Show as a table' }).click();
    await fp.getByRole('link', { name: 'Open tile 2' }).click();
    await expect(page).toHaveURL(/\/analyses\//);
    await expect(page.getByTestId('heatmap').or(page.getByTestId('matrix-table'))).toBeVisible();
  });
}

test('CMP (mock) compare with another model from a saved analysis: label first, axe on the comparison page', async ({ page }) => {
  const pid = await newProject(page, `Models ${Date.now()}`);
  await page.goto('/result/uniprot/A6NMZ7/28');
  await page.getByRole('button', { name: 'Save to project' }).click();
  await page.getByRole('dialog').getByLabel('Project').selectOption(pid);
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
  await expect(page).toHaveURL(/\/analyses\//);
  await page.getByRole('tab', { name: 'Other model' }).click();
  await page.getByRole('button', { name: 'Compare with another model' }).click();
  await page.getByRole('button', { name: 'Start anyway' }).click();
  await expect(page).toHaveURL(/\/model-comparisons\//);
  await expect(page.getByTestId('model-comparison-label')).toContainText('does not tell which model is right');
  await expect(page.getByTestId('model-disagreements').locator('tbody tr')).toHaveCount(20);
  const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  expect(res.violations.map((v) => `${v.id}: ${v.nodes[0]?.target.join(' ')}`)).toEqual([]);
  await page.setViewportSize({ width: 360, height: 800 });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  const wide = await page.evaluate(() => [...document.querySelectorAll<HTMLElement>('main *')]
    .filter((e) => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1)
    .map((e) => `${e.tagName}.${e.className} ${Math.round(e.getBoundingClientRect().right)}`).slice(0, 8));
  expect(overflow, wide.join(' | ')).toBeLessThanOrEqual(0);
  // plan-system 2.6: the first analysis now has a partner for the "models disagree" reason
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.getByTestId('model-side-a').getByRole('link').click();
  await page.getByRole('tab', { name: 'Candidates' }).click();
  const panel = page.getByTestId('candidates-panel');
  const partner = await panel.getByLabel('Compare with').locator('option').nth(1).getAttribute('value');
  await panel.getByLabel('Compare with').selectOption(partner!);
  await expect(panel.getByTestId('candidates-table')).toBeVisible();
  await expect(panel.getByTestId('candidates-label')).toContainText('not an experimentally validated design');
  const res2 = await new AxeBuilder({ page }).include('[data-testid="candidates-panel"]').withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  expect(res2.violations.map((v) => `${v.id}: ${v.nodes[0]?.target.join(' ')}`)).toEqual([]);
});

test.describe('UX-04 first visit', () => {
  test.use({ storageState: { cookies: [], origins: [] } });
  test('the guide shows once, is keyboard operable and passes axe; the glossary opens with Enter', async ({ page }) => {
    await page.goto('/projects');
    const guide = page.getByTestId('onboarding');
    await expect(guide).toBeVisible();
    const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    expect(res.violations.map((v) => `${v.id}: ${v.nodes[0]?.target.join(' ')}`)).toEqual([]);
    await guide.getByRole('button', { name: 'Next' }).focus();
    await page.keyboard.press('Enter');
    await expect(guide).toContainText('step 2 of 4');
    await guide.getByRole('button', { name: 'Skip the guide' }).click();
    await page.reload();
    await expect(page.getByTestId('onboarding')).toHaveCount(0);
    await page.goto('/result/uniprot/A6NMZ7/28');
    await page.getByRole('button', { name: 'What is Tile?' }).focus();
    await page.keyboard.press('Enter');
    await expect(page.getByRole('note').filter({ hasText: 'A full 28-residue window' })).toBeVisible();
    const res2 = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    expect(res2.violations.map((v) => `${v.id}: ${v.nodes[0]?.target.join(' ')}`)).toEqual([]);
    await page.keyboard.press('Escape');
    await expect(page.getByRole('note').filter({ hasText: 'A full 28-residue window' })).toBeHidden();
  });
});
