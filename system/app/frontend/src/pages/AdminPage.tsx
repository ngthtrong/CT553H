import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { RefreshCw } from 'lucide-react';
import { api } from '../api/client';
import { ApiError } from '../api/errors';
import type { AdminStatus } from '../api/types';
import { ErrorBanner } from '../components/ErrorBanner';
import { Banner, Button, Skeleton, StatusPill } from '../components/ui';
import { fmtDateTime } from '../lib/format';
import { useDocumentTitle } from '../lib/hooks';

type Models = { default_model_id: string | null; default_source: string | null; gate_model_id: string | null; loaded: { model_id: string; kind: string; weights_sha256: string; expected_tile_seconds: number | null }[]; not_loaded: { model_id: string; reason: string }[] };
type Workers = { alive: number; alive_after_seconds: number; warning?: string; recent: { owner: string; alive: boolean; last_seen_at: string | null; stopped_at: string | null; items_done: number }[] };
type Queue = { jobs_by_state: Record<string, number>; items_pending: number; items_running: number; oldest_open_job_seconds: number | null };

const mb = (b: number | null | undefined) => (b === null || b === undefined ? 'unknown' : `${(b / 1e6).toFixed(1)} MB`);

/** Local admin page (plan-system 4.2): counts and states only. Safe action: reload the registry (re-checks hashes). */
export function AdminPage() {
  useDocumentTitle('Admin');
  const qc = useQueryClient();
  const q = useQuery({ queryKey: ['admin-status'], queryFn: ({ signal }) => api.adminStatus(signal), retry: false, refetchInterval: 10_000 });
  const reload = useMutation({ mutationFn: () => api.reloadRegistry(), onSuccess: (s) => { qc.setQueryData(['admin-status'], s); void qc.invalidateQueries({ queryKey: ['models'] }); } });
  if (q.isPending) return <><h1>Admin</h1><Skeleton lines={6} label="Loading the status" /></>;
  if (q.isError) {
    const local = q.error instanceof ApiError && q.error.code === 'LOCAL_ONLY';
    return <><h1>Admin</h1>{local ? <Banner tone="warn" title="Only on this computer">{q.error.message}</Banner> : <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />}</>;
  }
  const s: AdminStatus = q.data;
  const models = s.models as Models;
  const workers = s.workers as Workers;
  const queue = s.queue as Queue;
  const cache = s.cache as Record<string, number | string>;
  const storage = s.storage as { database_bytes: number | null; workspace: { bytes: number; files: number } };
  const etl = s.etl as { status: string; finished_at: string | null; git_commit: string; numbers: Record<string, number> } | null;
  return (
    <div className="stack" data-testid="admin-page">
      <div className="page-head">
        <div>
          <h1>Admin</h1>
          <p className="muted">Counts and states of this installation; no sequence or imported value is shown. Refreshes every 10 s. Schema {s.schema_revision ?? 'unknown'} · code {s.code_version}.</p>
        </div>
        <Button icon={RefreshCw} busy={reload.isPending} onClick={() => reload.mutate()}>Reload models and check hashes</Button>
      </div>
      {reload.isError && <ErrorBanner error={reload.error} />}
      {workers.warning && <Banner tone="warn" title="No worker">{workers.warning}</Banner>}
      <section aria-labelledby="adm-models"><h2 id="adm-models">Models</h2>
        <p>Default <code>{models.default_model_id ?? 'none'}</code> (source {models.default_source ?? '—'}) · gate <code>{models.gate_model_id ?? 'none'}</code></p>
        <div className="ui-table__scroll"><table className="data" data-testid="admin-models"><caption className="visually-hidden">Models</caption>
          <thead><tr><th scope="col">Model</th><th scope="col">State</th><th scope="col">Kind</th><th scope="col" className="num">s per tile</th><th scope="col">Weights SHA-256</th></tr></thead>
          <tbody>
            {models.loaded.map((m) => <tr key={m.model_id}><th scope="row">{m.model_id}</th><td><StatusPill status="completed" label="serving" /></td><td>{m.kind}</td><td className="num">{m.expected_tile_seconds ?? '—'}</td><td className="mono">{m.weights_sha256.slice(0, 16)}…</td></tr>)}
            {models.not_loaded.map((m) => <tr key={m.model_id}><th scope="row">{m.model_id}</th><td><StatusPill status="failed" label="not serving" /></td><td colSpan={3}>{m.reason}</td></tr>)}
          </tbody></table></div>
      </section>
      <section aria-labelledby="adm-work"><h2 id="adm-work">Workers and queue</h2>
        <dl className="kv panel" data-testid="admin-queue">
          <dt>Workers alive</dt><dd className="num">{workers.alive} (reported within {workers.alive_after_seconds} s)</dd>
          <dt>Items pending / running</dt><dd className="num">{queue.items_pending} / {queue.items_running}</dd>
          <dt>Jobs by state</dt><dd>{Object.entries(queue.jobs_by_state).map(([k, v]) => `${k} ${v}`).join(', ') || 'none'}</dd>
          <dt>Oldest open job</dt><dd>{queue.oldest_open_job_seconds === null ? '—' : `${queue.oldest_open_job_seconds} s`}</dd>
        </dl>
        {workers.recent.length > 0 && (
          <div className="ui-table__scroll"><table className="data" data-testid="admin-workers"><caption className="visually-hidden">Recent workers</caption>
            <thead><tr><th scope="col">Worker</th><th scope="col">State</th><th scope="col">Last report</th><th scope="col" className="num">Items done</th></tr></thead>
            <tbody>{workers.recent.map((w) => <tr key={w.owner}><td className="mono">{w.owner}</td><td><StatusPill status={w.alive ? 'running' : 'cancelled'} label={w.alive ? 'alive' : w.stopped_at ? 'stopped' : 'silent'} /></td><td>{w.last_seen_at ? fmtDateTime(w.last_seen_at) : '—'}</td><td className="num">{w.items_done}</td></tr>)}</tbody>
          </table></div>
        )}
      </section>
      <section aria-labelledby="adm-store"><h2 id="adm-store">Cache, storage and reference data</h2>
        <dl className="kv panel">
          <dt>Prediction cache</dt><dd>{String(cache.mode)} · {cache.entries} entries · hits {cache.hits} / misses {cache.misses}</dd>
          <dt>Database</dt><dd>{mb(storage.database_bytes)}</dd>
          <dt>Project files</dt><dd>{mb(storage.workspace.bytes)} in {storage.workspace.files} files</dd>
          <dt>Last ETL</dt><dd>{etl ? `${etl.status}${etl.finished_at ? `, ${fmtDateTime(etl.finished_at)}` : ''} · commit ${etl.git_commit}` : 'no record'}</dd>
        </dl>
        <p className="muted">The reference data are loaded with <code>make docker-etl</code> and backed up with <code>make backup</code>; there is no ETL or delete action on this page.</p>
      </section>
    </div>
  );
}
