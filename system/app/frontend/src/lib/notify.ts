/**
 * Opt-in browser notification when a job finishes (plan-system 1.7). Local Notification API only: no push service, no
 * service worker. The text names the job by its short id and counts; it never contains a sequence or an input id.
 */
export type NotifySupport = 'unsupported' | 'default' | 'granted' | 'denied';

export function notifySupport(): NotifySupport {
  if (typeof window === 'undefined' || typeof window.Notification === 'undefined') return 'unsupported';
  return window.Notification.permission as NotifySupport;
}

export async function requestNotify(): Promise<NotifySupport> {
  if (notifySupport() === 'unsupported') return 'unsupported';
  try {
    return (await window.Notification.requestPermission()) as NotifySupport;
  } catch {
    return 'denied';
  }
}

export function jobFinishedText(jobId: string, state: string, succeeded: number, total: number): { title: string; body: string } {
  return { title: 'Degron Footprint: job finished', body: `Job ${jobId.slice(0, 8)} is ${state}: ${succeeded} of ${total} items succeeded.` };
}

/** Shows the notification only when the user allowed it; returns whether one was shown. */
export function notifyJobFinished(jobId: string, state: string, succeeded: number, total: number): boolean {
  if (notifySupport() !== 'granted') return false;
  const { title, body } = jobFinishedText(jobId, state, succeeded, total);
  try {
    new window.Notification(title, { body, tag: `df-job-${jobId}` });
    return true;
  } catch {
    return false;
  }
}
