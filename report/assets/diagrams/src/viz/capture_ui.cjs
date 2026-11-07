const { chromium } = require('@playwright/test');
const OUT = '/home/ngthtrong/CT553H/report/assets/diagrams/src/viz/inputs/';
const SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';
const H = Number(process.env.VH || 820);
async function clean(page){ await page.evaluate(()=>{ if(document.activeElement) document.activeElement.blur(); window.scrollTo(0,0); }); await page.waitForTimeout(200); }
async function shotTop(page, path, rows){
  await clean(page);
  const t = page.getByTestId('rank-table').locator('tbody tr').nth(rows);
  const bb = await t.boundingBox();
  await page.screenshot({ path, fullPage: true, clip: { x: 0, y: 0, width: 1280, height: Math.round(bb.y + bb.height + 24) } });
}
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: H }, deviceScaleFactor: 2, colorScheme: 'light' });
  await ctx.addInitScript(() => { try { localStorage.setItem('theme', 'light'); } catch {} });
  const page = await ctx.newPage();
  const base = 'http://localhost:5173';
  const only = (process.env.ONLY || '').split(',').filter(Boolean);
  const want = (n) => only.length === 0 || only.includes(n);

  if (want('a')) {
    await page.goto(base + '/');
    await page.getByLabel(/Tile sequence/).fill(SEQ);
    await page.waitForTimeout(500);
    await page.screenshot({ path: OUT + 'ui-input.png' });
    await page.getByRole('tab', { name: 'Choose a protein' }).click();
    await page.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }).fill('COL6A6');
    await page.getByRole('option', { name: /COL6A6/ }).waitFor();
    await page.waitForTimeout(500);
    await page.screenshot({ path: OUT + 'ui-input-search.png' });
    await page.getByRole('option', { name: /COL6A6/ }).click();
    await page.getByRole('radio', { name: /^tile 28,/ }).waitFor();
    await page.getByRole('radio', { name: /^tile 28,/ }).click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: OUT + 'ui-tile-picker.png' });
  }
  if (want('b')) {
    await page.goto(base + '/result/uniprot/A6NMZ7/28');
    await page.getByTestId('heatmap').waitFor();
    await page.waitForTimeout(800);
    await shotTop(page, OUT + 'ui-result-in-domain.png', 7);
  }
  if (want('c')) {
    await page.goto(base + '/result/uniprot/A6NMZ7/7');
    await page.getByTestId('refusal').waitFor();
    await page.waitForTimeout(500);
    await clean(page);
    await page.screenshot({ path: OUT + 'ui-result-out-of-domain.png' });
  }
  if (want('d')) {
    await page.goto(base + '/');
    await page.getByRole('tab', { name: 'Paste a sequence' }).click();
    await page.getByLabel(/Tile sequence/).fill(SEQ);
    await page.getByRole('button', { name: 'Predict' }).click();
    await page.getByTestId('heatmap').waitFor();
    await page.waitForTimeout(800);
    await shotTop(page, OUT + 'ui-result-unknown.png', 7);
  }
  if (want('e')) {
    await page.goto(base + '/model');
    await page.waitForTimeout(1200);
    await clean(page);
    await page.screenshot({ path: OUT + 'ui-model-card.png', fullPage: true });
  }
  if (want('f')) {
    await page.goto(base + '/result/uniprot/A6NMZ7/28');
    const hm = page.getByTestId('heatmap');
    await hm.waitFor();
    await page.waitForTimeout(800);
    await clean(page);
    await hm.screenshot({ path: OUT + 'ui-heatmap-only.png' });
    await clean(page);
    const lg = await page.getByText(/Probability that the substitution raises/).boundingBox();
    const hb = await hm.boundingBox();
    const x0 = Math.min(hb.x, lg.x) - 24, x1 = 1160;
    await page.screenshot({ path: OUT + 'ui-heatmap-crop.png', fullPage: true, clip: { x: Math.max(0, x0), y: lg.y - 14, width: x1 - Math.max(0, x0), height: hb.y + hb.height - lg.y + 70 } });
  }
  await browser.close();
})();
