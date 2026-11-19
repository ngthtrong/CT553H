import { expect, test } from '@playwright/test';

// UX-01 (plan-system 4.6): visual regression of the main screens on the mock API (deterministic synthetic data), light
// and dark, 1440 and 360 px, Chromium only. Pages without timestamps or random ids, so the images are stable.
// Update the baselines after an intended UI change:  npx playwright test e2e/visual.spec.ts --update-snapshots
const SCREENS: [string, string][] = [
  ['new-analysis', '/'],
  ['tile-picker', '/protein/A6NMZ7'],
  ['result-training-tile', '/result/uniprot/A6NMZ7/28'],
  ['result-out-of-domain', '/result/uniprot/A6NMZ7/7'],
  ['model-card', '/model'],
  ['about', '/about'],
];

for (const theme of ['light', 'dark'] as const) {
  for (const width of [1440, 360] as const) {
    test(`UX-01 ${theme} ${width}px`, async ({ page }) => {
      test.setTimeout(120_000);
      await page.addInitScript((t) => localStorage.setItem('df-theme', t), theme);
      await page.setViewportSize({ width, height: 900 });
      for (const [name, route] of SCREENS) {
        await page.goto(route);
        await page.waitForLoadState('networkidle');
        await page.evaluate(() => document.fonts.ready);
        // a sticky top bar lands at a scroll-dependent place in a full-page capture; static makes the image stable
        await page.addStyleTag({ content: '.shell__topbar { position: static !important; }' });
        await page.evaluate(() => window.scrollTo(0, 0));
        await expect(page).toHaveScreenshot(`${name}-${theme}-${width}.png`, {
          fullPage: true, animations: 'disabled', caret: 'hide', maxDiffPixelRatio: 0.002,
        });
      }
    });
  }
}
