/** plan-system 4.2 — local admin page (UI side). */
import { screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { API, HttpResponse, http, server } from './server';
import { REAL_TILE, renderApp } from './utils';

describe('4.2 admin page', () => {
  it('shows models, workers, queue and storage, and reloads the registry', async () => {
    renderApp('/admin');
    const page = await screen.findByTestId('admin-page');
    expect(within(page).getByTestId('admin-models')).toHaveTextContent('mock-retired-v0');
    expect(within(page).getByTestId('admin-models')).toHaveTextContent('not serving');
    expect(within(page).getByTestId('admin-queue')).toHaveTextContent('Workers alive1');
    expect(page.textContent).not.toContain(REAL_TILE);
    await userEvent.click(within(page).getByRole('button', { name: /Reload models/ }));
    expect(await within(page).findByTestId('admin-workers')).toBeInTheDocument();
  });
  it('explains a refusal from another computer', async () => {
    server.use(http.get(`${API}/v1/admin/status`, () => HttpResponse.json({ code: 'LOCAL_ONLY', message: 'The admin page answers only on this computer (DF_ADMIN_ALLOWED_NETWORKS).' }, { status: 403 })));
    renderApp('/admin');
    expect(await screen.findByText('Only on this computer')).toBeInTheDocument();
  });
});
