/** plan-system 4.4 — agreement over time (UI side of CMP-06/07). */
import { screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { handle } from '../mock/handler';
import { API, HttpResponse, http, server } from './server';
import { renderApp } from './utils';

const pt = (i: number, mae: number, flags: { code: string; text: string }[] = []) => ({
  comparison_id: `00000000-0000-4000-8000-00000000000${i}`, analysis_id: '00000000-0000-4000-8000-0000000000aa', dataset_id: `00000000-0000-4000-8000-0000000000b${i}`,
  dataset_name: `run ${i}`, dataset_revision: 1, model_id: 'mock-m3-ext4.0-platt-v1', tile: 'A6NMZ7 tile 28', created_at: `2026-11-1${i}T10:00:00Z`,
  n: 10, compatible: true, mae, spearman: 0.6, flags,
});

describe('4.4 agreement over time', () => {
  it('shows the caveat first, both trends with n, the table and the flag as a warning only', async () => {
    const pid = JSON.parse(handle('POST', '/v1/projects', { 'content-type': 'application/json' }, JSON.stringify({ name: 'agree' })).body!).project_id as string;
    server.use(http.get(`${API}/v1/projects/${pid}/agreement`, () => HttpResponse.json({
      project_id: pid, caveat: 'A worse agreement may come from another assay, conditions, replicate handling or tiles; it does not by itself mean that the model is wrong. Nothing is changed automatically.',
      rules: { min_n: 5, min_earlier: 2, mae_ratio: 1.25, spearman_drop: 0.2 }, flagged: 1,
      points: [pt(1, 0.1), pt(2, 0.11), pt(3, 0.9, [{ code: 'mae_worse', text: 'MAE 0.900 is above 1.25 × the mean of 2 earlier comparisons (0.105).' }])],
    })));
    renderApp(`/projects/${pid}?tab=agreement`);
    const panel = await screen.findByTestId('agreement-panel');
    expect(panel.textContent!.indexOf('not an independent validation')).toBeLessThan(panel.textContent!.indexOf('MAE'));
    expect(within(panel).getByTestId('agreement-flags')).toHaveTextContent('does not by itself mean that the model is wrong');
    expect(within(panel).getByTestId('agreement-mae').querySelectorAll('circle.chart-flag')).toHaveLength(1);
    expect(within(within(panel).getByTestId('agreement-table')).getAllByRole('row')).toHaveLength(4);
    expect(within(panel).getByTestId('agreement-mae')).toHaveTextContent('n=10');
    expect(within(panel).queryByRole('button')).toBeNull();                // no action to change anything (CMP-07)
    await userEvent.click(screen.getByRole('tab', { name: /Analysis history/ }));
  });
});
