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
