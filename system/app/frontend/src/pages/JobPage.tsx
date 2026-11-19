import { useEffect, useRef, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { ChevronLeft, ChevronRight, OctagonX } from 'lucide-react';
import { workspace } from '../api/client';
import type { Job, JobItem } from '../api/types';
import { ErrorBanner } from '../components/ErrorBanner';
import { ProteinFootprint } from '../components/ProteinFootprint';
import { Banner, Button, IconButton, LiveRegion, ProgressBar, Skeleton, StatusPill } from '../components/ui';
import { DomainBadge, DownloadButton } from '../components/workspace';
import { fmtDateTime } from '../lib/format';
import { useDocumentTitle } from '../lib/hooks';
import { fmtDuration } from '../lib/models';
import { notifyJobFinished, notifySupport, requestNotify, type NotifySupport } from '../lib/notify';

const TERMINAL = ['completed', 'partial', 'failed', 'cancelled'];
const PAGE = 50;

type OneCoverage = { protein_length: number; tiles: number; uncovered?: { start: number; end: number }[]; unscorable_windows?: { tile_index: number; start: number; end: number }[]; uniprot_id: string | null; reference_release?: string | null; input_id: string; refused?: string };

/** Coverage of one protein: windows on one axis, uncovered end and unscorable windows. */
function CoverageOne({ raw }: { raw: OneCoverage }) {
  // older or partial snapshots must not break the page; the cached object itself is never modified
  const c = { ...raw, uncovered: raw.uncovered ?? [], unscorable_windows: raw.unscorable_windows ?? [] };
  if (c.refused) return <p data-testid="coverage-refused"><strong>{c.input_id}</strong>: not scored (<code>{c.refused}</code>); see the item list.</p>;
  const pct = (pos: number) => `${((pos - 1) / c.protein_length) * 100}%`;
  const width = (a: number, b: number) => `${((b - a + 1) / c.protein_length) * 100}%`;
  const covered = c.protein_length - c.uncovered.reduce((s, u) => s + u.end - u.start + 1, 0);
  return (
    <div className="stack">
      <p className="muted" style={{ margin: 0 }}>
        {c.uniprot_id ? `${c.uniprot_id} (UniProt ${c.reference_release})` : `${c.input_id} (typed, no accession)`} · {c.protein_length} residues · {c.tiles} windows of 28, step 23
      </p>
      <div className="coverage-track" aria-hidden="true">
        <div className="coverage-covered" style={{ left: 0, width: width(1, covered) }} />
        {c.uncovered.map((u) => <div key={u.start} className="coverage-gap" style={{ left: pct(u.start), width: width(u.start, u.end) }} />)}
        {c.unscorable_windows.map((u) => <div key={u.tile_index} className="coverage-unscorable" style={{ left: pct(u.start), width: width(u.start, u.end) }} />)}
      </div>
      <ul className="legend" aria-label={`Coverage of ${c.input_id}`}>
        <li><span className="swatch solid" aria-hidden="true" /> Covered by full windows: residues 1–{covered}</li>
        <li><span className="swatch empty" aria-hidden="true" /> Not covered: {c.uncovered.length ? c.uncovered.map((u) => `${u.start}–${u.end}`).join(', ') : 'none'}</li>
        <li><span className="swatch hatched" aria-hidden="true" /> Unscorable windows: {c.unscorable_windows.length ? c.unscorable_windows.map((u) => `tile ${u.tile_index} (${u.start}–${u.end})`).join(', ') : 'none'}</li>
      </ul>
    </div>
  );
}

/** ProteinCoverage: one block per protein (several since plan-system 3.3). */
function ProteinCoverage({ job }: { job: Job }) {
  const raw = job.coverage as (OneCoverage & { version?: number; proteins?: OneCoverage[] }) | undefined;
  if (!raw) return null;
  const list = raw.version === 2 ? raw.proteins ?? [] : [raw];
  return (
    <section className="panel" aria-labelledby="coverage-h" data-testid="protein-coverage">
      <h2 id="coverage-h" style={{ marginTop: 0, fontSize: 'var(--text-lg)' }}>Protein coverage{list.length > 1 ? ` (${list.length} proteins)` : ''}</h2>
      {list.map((c) => <CoverageOne key={c.input_id} raw={c} />)}
      <p className="muted">Overlapping windows are scored separately and never averaged; open a tile to see its matrix.</p>
    </section>
  );
}

function JobItemTable({ jobId, mode, refreshKey }: { jobId: string; mode: Job['mode']; refreshKey: string }) {
  const [offset, setOffset] = useState(0);
  const q = useQuery({ queryKey: ['job-items', jobId, offset, refreshKey], queryFn: ({ signal }) => workspace.listJobItems(jobId, offset, PAGE, signal), retry: false, placeholderData: (prev) => prev });
  if (q.isPending) return <Skeleton />;
  if (q.isError) return <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />;
  const { items, total } = q.data;
  const last = Math.max(0, Math.ceil(total / PAGE) - 1);
  const page = Math.floor(offset / PAGE);
  return (
    <section aria-labelledby="items-h">
      <h2 id="items-h">Items</h2>
      <div className="ui-table__scroll">
        <table className="data" data-testid="job-item-table">
          <caption className="visually-hidden">Job items, page {page + 1} of {last + 1}</caption>
          <thead>
            <tr>
              <th scope="col">Item</th>
              <th scope="col">Input</th>
              {mode === 'protein' && <th scope="col">Window</th>}
              <th scope="col">Status</th>
              <th scope="col">Domain</th>
              <th scope="col">Result or reason</th>
            </tr>
          </thead>
          <tbody>
            {items.map((it: JobItem) => (
              <tr key={it.item_id}>
                <td className="mono">{it.item_id}</td>
                <td>{it.input_id}</td>
                {mode === 'protein' && <td className="num">{it.tile_index ? `tile ${it.tile_index} · ${it.start_pos}–${it.end_pos}` : ''}</td>}
                <td><StatusPill status={it.state} /></td>
                <td>{it.domain_status ? <DomainBadge status={it.domain_status} /> : <span className="muted">—</span>}</td>
                <td>
                  {it.analysis_id ? <Link to={`/analyses/${it.analysis_id}`}>Open matrix</Link> : it.error ? <span><code>{it.error.code}</code> {it.error.message}</span> : <span className="muted">—</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {total > PAGE && (
        <nav className="ui-pager" aria-label="Job items: pages">
          <IconButton icon={ChevronLeft} label="Previous page" disabled={page === 0} onClick={() => setOffset(offset - PAGE)} />
          <span className="num">Page {page + 1} of {last + 1} · {total} items</span>
          <IconButton icon={ChevronRight} label="Next page" disabled={page >= last} onClick={() => setOffset(offset + PAGE)} />
        </nav>
      )}
    </section>
  );
}

/** Opt-in notification when this job finishes (plan-system 1.7); asks the browser only after the user ticks the box. */
function NotifyWhenDone({ job, terminal }: { job: Job; terminal: boolean }) {
  const [support, setSupport] = useState<NotifySupport>(notifySupport);
  const [wanted, setWanted] = useState(false);
  const prev = useRef(terminal);
  useEffect(() => {
    if (!prev.current && terminal && wanted) notifyJobFinished(job.job_id, job.state, job.counts.succeeded ?? 0, job.total);
    prev.current = terminal;
  }, [terminal, wanted, job.job_id, job.state, job.counts.succeeded, job.total]);
  if (terminal) return null;
  if (support === 'unsupported') return <p className="muted" data-testid="notify">This browser cannot show a notification when the job finishes.</p>;
  return (
    <div data-testid="notify">
      <label>
        <input
          type="checkbox"
          checked={wanted && support === 'granted'}
          disabled={support === 'denied'}
          onChange={async (e) => {
            if (!e.target.checked) { setWanted(false); return; }
            const s = support === 'granted' ? support : await requestNotify();
            setSupport(s);
            setWanted(s === 'granted');
          }}
        />{' '}
        Notify me in this browser when the job finishes
      </label>
      <span className="muted">
        {support === 'denied'
          ? ' Notifications are blocked for this site in the browser settings.'
          : ' Shown by this browser only (no push service); the text has the job number and counts, never a sequence.'}
      </span>
    </div>
  );
}

/** Screen 9.9 (UC-08, UC-03): progress, cancellation, per-item outcomes; resumes from durable state after a restart. */
export function JobPage() {
  const { id = '' } = useParams();
  const qc = useQueryClient();
  const q = useQuery({
    queryKey: ['job', id],
    queryFn: ({ signal }) => workspace.getJob(id, signal),
    retry: false,
    refetchInterval: (query) => (query.state.data && TERMINAL.includes(query.state.data.state) ? false : 1000),
  });
  const cancel = useMutation({ mutationFn: () => workspace.cancelJob(id), onSuccess: (job) => qc.setQueryData(['job', id], job) });
  // The tab title carries the progress (plan-system 1.7), so a background tab shows it.
  const d = q.data;
  const doneNow = d ? d.total - (d.counts.pending ?? 0) - (d.counts.running ?? 0) : 0;
  useDocumentTitle(!d ? 'Job' : TERMINAL.includes(d.state) ? `Job ${d.state}` : `${d.total ? Math.floor((doneNow / d.total) * 100) : 0}% · Job ${doneNow}/${d.total}`);
  if (q.isPending) return <Skeleton lines={5} label="Loading job" />;
  if (q.isError) return (<><h1>Job</h1><ErrorBanner error={q.error} onRetry={() => void q.refetch()} /></>);
  const job = q.data;
  const c = job.counts;
  const finished = job.total - (c.pending ?? 0) - (c.running ?? 0);
  const terminal = TERMINAL.includes(job.state);
  const cfg = job.configuration_snapshot as { model_id?: string; calibrator?: string; gate_model_id?: string | null; override_domain?: boolean };
  return (
    <div className="stack">
      <nav aria-label="Breadcrumb" className="muted"><Link to="/projects">Projects</Link> / <Link to={`/projects/${job.project_id}?tab=jobs`}>Project</Link> / Job</nav>
      <div className="page-head">
        <div>
          <h1>{job.mode === 'protein' ? 'Whole-protein job' : 'Peptide batch job'}</h1>
          <p>Submitted {fmtDateTime(job.created_at)} · <span className="mono">{job.job_id.slice(0, 8)}</span></p>
        </div>
        <div className="row">
          <StatusPill status={job.state} label={job.cancel_requested && !terminal ? 'Cancelling…' : undefined} />
          {!terminal && (
            <Button variant="danger" icon={OctagonX} busy={cancel.isPending} disabled={job.cancel_requested} onClick={() => cancel.mutate()}>
              Cancel job
            </Button>
          )}
        </div>
      </div>
      <ProgressBar value={finished} max={job.total} label="Items finished" />
      <NotifyWhenDone job={job} terminal={terminal} />
      <LiveRegion message={terminal ? `Job ${job.state}: ${c.succeeded ?? 0} of ${job.total} succeeded.` : `${finished} of ${job.total} items finished.`} />
      <dl className="kv panel" data-testid="job-counts">
        <dt>Succeeded</dt><dd className="num">{c.succeeded ?? 0}</dd>
        <dt>Refused (input or domain)</dt><dd className="num">{c.refused ?? 0}</dd>
        <dt>Failed</dt><dd className="num">{c.failed ?? 0}</dd>
        <dt>Cancelled</dt><dd className="num">{c.cancelled ?? 0}</dd>
        <dt>Pending / running</dt><dd className="num">{c.pending ?? 0} / {c.running ?? 0}</dd>
        {!terminal && (
          <>
            <dt>Estimated time left</dt>
            <dd data-testid="job-eta">
              {job.eta_seconds === null || job.eta_seconds === undefined
                ? <span className="muted">estimated after 3 finished items</span>
                : <>≈ {fmtDuration(job.eta_seconds)} <span className="muted">(mean time of the last items × items left; an estimate)</span></>}
            </dd>
          </>
        )}
        <dt>Pinned model</dt><dd><code>{cfg.model_id}</code> · calibrator {cfg.calibrator} · gate {cfg.gate_model_id ?? 'none'}{cfg.override_domain ? ' · out-of-domain override on' : ''}</dd>
      </dl>
      {job.state === 'partial' && <Banner tone="warn" title="Partly completed">Some items were refused or failed; the others are saved. The reasons are listed per item.</Banner>}
      {job.state === 'failed' && <Banner tone="danger" title="No item succeeded">See the reason of each item below.</Banner>}
      {job.state === 'cancelled' && <Banner tone="info" title="Cancelled">Items finished before the cancellation are kept.</Banner>}
      {job.mode === 'protein' && <ProteinCoverage job={job} />}
      {job.mode === 'protein' && terminal && (c.succeeded ?? 0) > 0 && <ProteinFootprint jobId={job.job_id} />}
      <div className="row">
        <DownloadButton label="Export manifest CSV" fileName={`degron-footprint_job-${job.job_id.slice(0, 8)}.csv`} fetchBlob={() => workspace.exportJob(job.job_id, 'csv')} />
        <DownloadButton label="Export JSON" fileName={`degron-footprint_job-${job.job_id.slice(0, 8)}.json`} fetchBlob={() => workspace.exportJob(job.job_id, 'json')} />
      </div>
      <p className="muted">Exports contain every item and every score, not only the page shown.</p>
      <JobItemTable jobId={job.job_id} mode={job.mode} refreshKey={`${job.state}-${finished}`} />
    </div>
  );
}
