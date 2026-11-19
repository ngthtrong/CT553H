/** plan-system 1.7 — job ETA, progress in the tab title, opt-in browser notification (BATCH-08/09, UI side). */
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { handle } from '../mock/handler';
import { jobFinishedText } from '../src/lib/notify';
import { REAL_TILE, renderApp } from './utils';

function api(method: string, url: string, body?: unknown) {
  const out = handle(method, url, { 'content-type': 'application/json' }, body === undefined ? '' : JSON.stringify(body));
  return out.body ? JSON.parse(out.body) : null;
}

class FakeNotification {
  static permission: NotificationPermission = 'default';
  static requestPermission = vi.fn(async () => { FakeNotification.permission = 'granted'; return 'granted' as NotificationPermission; });
  static shown: { title: string; body?: string }[] = [];
  constructor(title: string, opts?: NotificationOptions) { FakeNotification.shown.push({ title, body: opts?.body }); }
}

afterEach(() => {
  vi.unstubAllGlobals();
  FakeNotification.permission = 'default';
  FakeNotification.shown = [];
  FakeNotification.requestPermission.mockClear();
});

function bigJob() {
  const pid = api('POST', '/v1/projects', { name: 'eta' }).project_id as string;
  const peptides = Array.from({ length: 8 }, (_, i) => ({ input_id: `pep-${i}`, sequence: REAL_TILE }));
  return api('POST', `/v1/projects/${pid}/jobs`, { mode: 'peptides', peptides });
}

describe('1.7 job ETA and notification', () => {
  it('shows the ETA once measured and the progress in the tab title', async () => {
    const job = bigJob();
    renderApp(`/jobs/${job.job_id}`);
    expect(await screen.findByTestId('job-eta')).toHaveTextContent('estimated after 3 finished items');
    await waitFor(() => expect(screen.getByTestId('job-eta')).toHaveTextContent(/≈ \d+ s/), { timeout: 8000 });
    expect(document.title).toMatch(/^\d+% · Job \d+\/8 · Degron Footprint$/);
    await waitFor(() => expect(document.title).toBe('Job completed · Degron Footprint'), { timeout: 15000 });
    expect(screen.queryByTestId('job-eta')).toBeNull();
  }, 25000);

  it('asks for permission only when the user opts in, then notifies once without any sequence', async () => {
    vi.stubGlobal('Notification', FakeNotification);
    const job = bigJob();
    renderApp(`/jobs/${job.job_id}`);
    const box = await screen.findByRole('checkbox', { name: /Notify me in this browser/ });
    expect(FakeNotification.requestPermission).not.toHaveBeenCalled();
    await userEvent.click(box);
    expect(FakeNotification.requestPermission).toHaveBeenCalledTimes(1);
    await waitFor(() => expect(FakeNotification.shown).toHaveLength(1), { timeout: 15000 });
    const n = FakeNotification.shown[0]!;
    expect(n.body).toBe(`Job ${job.job_id.slice(0, 8)} is completed: 8 of 8 items succeeded.`);
    expect(JSON.stringify(n)).not.toContain(REAL_TILE);
    expect(JSON.stringify(n)).not.toContain('pep-');
  }, 25000);

  it('does not notify without the opt-in, even when the browser already allows it', async () => {
    FakeNotification.permission = 'granted';
    vi.stubGlobal('Notification', FakeNotification);
    const job = bigJob();
    renderApp(`/jobs/${job.job_id}`);
    await waitFor(() => expect(document.title).toBe('Job completed · Degron Footprint'), { timeout: 15000 });
    expect(FakeNotification.shown).toHaveLength(0);
  }, 25000);

  it('the notification text names the job and counts only', () => {
    expect(jobFinishedText('12345678-aaaa', 'partial', 3, 5)).toEqual({ title: 'Degron Footprint: job finished', body: 'Job 12345678 is partial: 3 of 5 items succeeded.' });
  });
});
