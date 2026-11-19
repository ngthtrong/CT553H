import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

// WP1 acceptance: every primitive and the shell pass axe (WCAG 2.1 AA incl. contrast) in both themes at the four
// review widths (NFR-12 + skill breakpoints merged: 360 / 768 / 1280 / 1440), with no horizontal page scroll.
const WIDTHS = [360, 768, 1280, 1440];

for (const theme of ['light', 'dark'] as const) {
  test(`WP1 styleguide and shell, ${theme} theme, four widths`, async ({ page }) => {
    await page.addInitScript((t) => localStorage.setItem('df-theme', t), theme);
    for (const width of WIDTHS) {
      await page.setViewportSize({ width, height: 900 });
      await page.goto('/__styleguide');
      await expect(page.getByRole('heading', { name: 'Styleguide' })).toBeVisible();
      await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
      const font = await page.evaluate(() => getComputedStyle(document.body).fontFamily);
      expect(font).toContain('Roboto');
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow, `horizontal scroll at ${width}`).toBeLessThanOrEqual(0);
      const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
      const bad = res.violations.map((v) => `${v.id} (${v.impact}): ${v.nodes.length} node(s), e.g. ${v.nodes[0]?.target.join(' ')}`);
      expect(bad, `${theme} at ${width}px`).toEqual([]);
    }
  });
}

test('WP1 narrow shell: the menu button opens the sidebar navigation', async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 800 });
  await page.goto('/__styleguide');
  const nav = page.getByRole('navigation', { name: 'Main' });
  await expect(nav).toBeHidden();
  await page.getByRole('button', { name: 'Open menu' }).click();
  await expect(nav).toBeVisible();
  await expect(page.getByRole('button', { name: 'Close menu' })).toHaveAttribute('aria-expanded', 'true');
  await nav.getByRole('link', { name: 'Model & evidence' }).click();
  await expect(page).toHaveURL(/\/model$/);
  await expect(nav).toBeHidden();
});

test('WP1 the fonts are served by the application, not a CDN (NFR-09)', async ({ page }) => {
  const external: string[] = [];
  page.on('request', (r) => {
    const u = new URL(r.url());
    if (u.hostname !== 'localhost' && u.hostname !== '127.0.0.1') external.push(r.url());
  });
  await page.goto('/__styleguide');
  await page.waitForLoadState('networkidle');
  // document.fonts.check() is also true for a family that is not declared at all, so require loaded faces of both families
  const loaded = await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([document.fonts.load('16px "Roboto Variable"'), document.fonts.load('16px "Roboto Mono Variable"')]);
    return [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, ''));
  });
  expect(loaded).toContain('Roboto Variable');
  expect(loaded).toContain('Roboto Mono Variable');
  expect(external).toEqual([]);
});
