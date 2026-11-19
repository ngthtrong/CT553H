import { expect, test } from '@playwright/test';

test('NFR-12 360 px: no horizontal page scroll, table view first, touch targets of 44 px', async ({ page }) => {
  await page.goto('/result/uniprot/P60484/1');
  await expect(page.getByTestId('matrix-table')).toBeVisible();
  await expect(page.getByTestId('heatmap')).toHaveCount(0);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(0);
  const small = await page.evaluate(() =>
    [...document.querySelectorAll<HTMLElement>('button:not(.link), select, input[type="checkbox"], input[type="radio"]')]
      .filter((e) => e.offsetParent !== null && !e.closest('th') && !e.closest('.tile'))
      .map((e) => (e instanceof HTMLInputElement && e.closest('label') ? e.closest('label')! : e))
      .filter((e) => e.getBoundingClientRect().height < 44)
      .map((e) => e.outerHTML.slice(0, 80)),
  );
  expect(small).toEqual([]);
  await page.getByRole('button', { name: 'Show the heatmap' }).click();
  await expect(page.getByTestId('heatmap')).toBeVisible();
});

test('VIZ-04 360 px: the protein footprint scrolls inside its box, the page never scrolls sideways', async ({ page }) => {
  test.setTimeout(90_000);
  await page.goto('/projects');
  await page.getByRole('button', { name: 'New project' }).click();
  await page.getByRole('dialog').getByLabel(/Name/).fill(`Narrow ${Date.now()}`);
  await page.getByRole('dialog').getByRole('button', { name: 'Create project' }).click();
  await expect(page).toHaveURL(/\/projects\/[0-9a-f-]{36}/);
  const pid = page.url().split('/projects/')[1]!.split('?')[0]!;
  await page.goto(`/new?mode=protein&project=${pid}`);
  await page.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }).fill('PTEN');
  await page.getByRole('option', { name: /PTEN/ }).click();
  await page.getByRole('checkbox', { name: /Score out-of-domain tiles anyway/ }).check();
  await page.getByRole('button', { name: 'Submit protein job' }).click();
  await expect(page.getByTestId('protein-footprint')).toBeVisible({ timeout: 60_000 });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(0);
});
