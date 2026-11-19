import { mkdirSync } from 'node:fs';
import { expect, test, type Page } from '@playwright/test';

// WP12.1: screenshots of the real application with real data (both themes) for report/appendices and the defence.
// Run against an API on a COPY of .data/dev.db with the embedded worker:  SCREENSHOTS=1 E2E_REAL=1 npx playwright test e2e/screenshots.spec.ts
test.skip(process.env.SCREENSHOTS !== '1', 'screenshots only on request');
test.setTimeout(240_000);

const OUT = '../docs/screenshots';
const SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';

async function shot(page: Page, name: string, theme: string) {
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: `${OUT}/${theme}/${name}.png`, fullPage: false });
}

for (const theme of ['light', 'dark'] as const) {
  test(`screens with real data, ${theme}`, async ({ page, request }) => {
    mkdirSync(`${OUT}/${theme}`, { recursive: true });
    await page.addInitScript((t) => localStorage.setItem('df-theme', t), theme);
    await page.setViewportSize({ width: 1440, height: 900 });
    const pid = ((await (await request.post('/v1/projects', { data: { name: 'PTEN degron follow-up', description: 'Saturation scan of PTEN tiles and a GPS replicate' } })).json()) as { project_id: string }).project_id;
    const saved = (await (await request.post(`/v1/projects/${pid}/analyses`, { data: { request: { uniprot_id: 'A6NMZ7', tile_index: 28 } } })).json()) as { analysis_id: string; result: { tile: { sequence: string }; cells: { position: number; wt_aa: string; mut_aa: string; score_dpsi_raw: number }[] } };
    await request.post(`/v1/projects/${pid}/analyses`, { data: { request: { sequence: SEQ } } });
    const job = (await (await request.post(`/v1/projects/${pid}/jobs`, { data: { mode: 'protein', protein: { uniprot_id: 'P60484' } } })).json()) as { job_id: string };
    const seq = saved.result.tile.sequence;
    const rows = saved.result.cells.slice(0, 12).flatMap((c) => [
      `pep28,${seq},${c.position},${c.wt_aa},${c.mut_aa},${(c.score_dpsi_raw + 0.3).toFixed(3)},r1`,
      `pep28,${seq},${c.position},${c.wt_aa},${c.mut_aa},${(c.score_dpsi_raw - 0.2).toFixed(3)},r2`]);
    const csv = ['peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id', ...rows].join('\n');
    const ds = (await (await request.post(`/v1/projects/${pid}/datasets`, { multipart: { file: { name: 'gps-rep.csv', mimeType: 'text/csv', buffer: Buffer.from(csv) },
      metadata: JSON.stringify({ name: 'GPS follow-up (illustration)', assay: 'GPS', endpoint: 'delta_psi', units: 'PSI', source: 'Illustrative values derived from the prediction, not a measurement', reference_description: 'A6NMZ7 tile 28', compatibility: 'zhang_gps_dpsi' }) } })).json()) as { dataset_id: string };
    await request.post(`/v1/datasets/${ds.dataset_id}`, { data: { action: 'commit', acknowledge_warnings: true } });
    await request.post(`/v1/analyses/${saved.analysis_id}/comparisons`, { data: { dataset_id: ds.dataset_id, aggregation: 'mean' } });

    await page.goto('/projects'); await shot(page, '01-projects', theme);
    await page.goto(`/projects/${pid}`); await shot(page, '02-project-history', theme);
    await page.goto(`/new?mode=protein&project=${pid}`);
    await page.getByRole('combobox', { name: 'Gene symbol or UniProt accession' }).fill('PTEN');
    await page.getByRole('option', { name: /P60484/ }).click();
    await expect(page.getByTestId('protein-preview')).toBeVisible(); await shot(page, '03-new-analysis-protein', theme);
    await page.goto('/protein/A6NMZ7'); await shot(page, '04-tile-picker', theme);
    await page.goto('/result/uniprot/A6NMZ7/28'); await expect(page.getByTestId('heatmap')).toBeVisible(); await shot(page, '05-result-matrix', theme);
    await page.getByTestId('footprint-track').scrollIntoViewIfNeeded(); await shot(page, '05b-footprint-track', theme);
    await page.goto(`/jobs/${job.job_id}`);
    await expect(page.locator('.ui-pill[data-status="completed"], .ui-pill[data-status="partial"]').first()).toBeVisible({ timeout: 120_000 });
    await shot(page, '06-job-progress', theme);
    // plan-system 2.1: protein-level footprint of the finished job
    await expect(page.getByTestId('protein-footprint')).toBeVisible();
    await page.getByTestId('protein-footprint').evaluate((e) => e.scrollIntoView({ block: 'start' })); await shot(page, '06b-protein-footprint', theme);
    await page.goto(`/analyses/${saved.analysis_id}/report?format=html`.replace('/analyses/', '/v1/analyses/'));
    await expect(page.getByText('Read this first')).toBeVisible(); await shot(page, '07b-report', theme);      // plan-system 3.5
    await page.goto(`/analyses/${saved.analysis_id}`); await expect(page.getByTestId('heatmap')).toBeVisible(); await shot(page, '07-saved-analysis', theme);
    await page.getByRole('tab', { name: 'Comparison' }).click();
    await page.getByRole('button', { name: /GPS follow-up/ }).click(); await expect(page.getByTestId('comparison-result')).toBeVisible();
    await page.getByTestId('comparison-result').evaluate((e) => e.scrollIntoView({ block: 'start' })); await shot(page, '08-comparison', theme);
    await page.getByTestId('comparison-charts').evaluate((e) => e.scrollIntoView({ block: 'start' })); await shot(page, '08b-comparison-charts', theme);   // 2.3
    await page.getByRole('tab', { name: 'ClinVar and annotations' }).click(); await shot(page, '09-annotations', theme);
    await page.goto(`/import?project=${pid}`); await shot(page, '10-import', theme);
    await page.goto(`/datasets/${ds.dataset_id}`); await shot(page, '11-dataset', theme);
    await page.goto('/model'); await shot(page, '12-model', theme);
    await page.goto('/sources'); await shot(page, '13-sources', theme);
  });
}
