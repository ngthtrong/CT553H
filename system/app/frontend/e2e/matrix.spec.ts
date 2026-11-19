import { expect, test } from '@playwright/test';

// WP11.2 / NFR-12: the main screens in Chromium, Firefox and WebKit at 360 / 768 / 1280 / 1440 px — no horizontal page
// scroll, the page heading is visible, and controls keep 44-px touch targets on narrow screens. Mock API.
const WIDTHS = [360, 768, 1280, 1440];
const SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';

test('NFR-12 browser × width matrix', async ({ page, request }) => {
  const pid = ((await (await request.post('/v1/projects', { data: { name: `Matrix ${Date.now()}` } })).json()) as { project_id: string }).project_id;
  const saved = (await (await request.post(`/v1/projects/${pid}/analyses`, { data: { request: { uniprot_id: 'A6NMZ7', tile_index: 28 } } })).json()) as { analysis_id: string };
  const job = (await (await request.post(`/v1/projects/${pid}/jobs`, { data: { mode: 'peptides', peptides: [{ input_id: 'a', sequence: SEQ }] } })).json()) as { job_id: string };
  const routes = ['/projects', `/projects/${pid}`, `/new?mode=batch&project=${pid}`, '/protein/A6NMZ7', '/result/uniprot/A6NMZ7/28',
    `/analyses/${saved.analysis_id}`, `/jobs/${job.job_id}`, `/import?project=${pid}`, '/model', '/sources'];
  for (const width of WIDTHS) {
    await page.setViewportSize({ width, height: 900 });
    for (const route of routes) {
      await page.goto(route);
      await expect(page.getByRole('heading', { level: 1 }).first()).toBeVisible();
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow, `${route} at ${width}px`).toBeLessThanOrEqual(0);
      if (width === 360) {
        const small = await page.evaluate(() =>
          [...document.querySelectorAll<HTMLElement>('button:not(.link), select, input[type="checkbox"], input[type="radio"]')]
            .filter((e) => e.offsetParent !== null && !e.closest('th') && !e.closest('.tile') && !e.closest('dialog'))
            .map((e) => (e instanceof HTMLInputElement && e.closest('label') ? e.closest('label')! : e))
            .filter((e) => e.getBoundingClientRect().height < 44)
            .map((e) => e.outerHTML.slice(0, 80)));
        expect(small, `${route} touch targets`).toEqual([]);
      }
    }
  }
});
