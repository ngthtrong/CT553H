/**
 * Components shared by the workspace screens (ui-design §12.5): DeleteConfirmation, ProjectPicker, the domain badge of a
 * history row and the download button for server exports. Server state is keyed by ids; no biological payload goes into
 * the URL or browser storage.
 */
import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { AlertTriangle, Download, Trash2 } from 'lucide-react';
import { workspace } from '../api/client';
import { ApiError } from '../api/errors';
import type { DomainStatus } from '../api/types';
import { STATUS } from '../lib/domain';
import { saveBlob } from '../lib/download';
import { Banner, Button, Dialog, Select } from './ui';

const DEP_LABEL: Record<string, string> = {
  analyses: 'saved analyses', jobs: 'jobs', job_items: 'job items', running_jobs: 'unfinished jobs (they are cancelled first)',
  datasets: 'datasets', observations: 'imported observations', comparisons: 'comparisons',
};

/**
 * Two-step deletion (FR-33, HIST-03): the first request without confirmation returns the dependency summary (HTTP 409)
 * and deletes nothing; only the explicit second step deletes. A failed file cleanup is shown with a retry.
 */
export function DeleteConfirmation({ what, remove, onDeleted, label = 'Delete…' }: {
  what: string;
  remove: (confirm: boolean) => Promise<void>;
  onDeleted: () => void;
  label?: string;
}) {
  const [open, setOpen] = useState(false);
  const [deps, setDeps] = useState<Record<string, number> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function start() {
    setError(null);
    setBusy(true);
    try {
      await remove(false);
      onDeleted();                                         // nothing depended on it and the server deleted it
    } catch (e) {
      if (e instanceof ApiError && e.code === 'CONFIRMATION_REQUIRED') {
        setDeps(e.dependencies ?? {});
        setOpen(true);
      } else setError(e instanceof Error ? e.message : 'The deletion failed.');
    } finally {
      setBusy(false);
    }
  }

  async function confirm() {
    setBusy(true);
    setError(null);
    try {
      await remove(true);
      setOpen(false);
      onDeleted();
    } catch (e) {
      setError(e instanceof ApiError && e.status === 503
        ? `${e.message} Nothing was reported as deleted; you can retry.`
        : e instanceof Error ? e.message : 'The deletion failed.');
    } finally {
      setBusy(false);
    }
  }

  const listed = Object.entries(deps ?? {}).filter(([, n]) => n > 0);
  return (
    <>
      <Button variant="danger" icon={Trash2} onClick={() => void start()} busy={busy && !open}>
        {label}
      </Button>
      {error && !open && <Banner tone="danger" live title="Not deleted">{error}</Banner>}
      <Dialog
        open={open}
        title={`Delete ${what}?`}
        onClose={() => setOpen(false)}
        actions={
          <>
            <Button onClick={() => setOpen(false)}>Keep it</Button>
            <Button variant="danger" icon={Trash2} busy={busy} onClick={() => void confirm()}>
              {error ? 'Retry deletion' : 'Delete permanently'}
            </Button>
          </>
        }
      >
        {listed.length ? (
          <>
            <p>This also removes:</p>
            <ul data-testid="delete-dependencies">
              {listed.map(([k, n]) => (
                <li key={k}>
                  <span className="num">{n}</span> {DEP_LABEL[k] ?? k}
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p>Nothing else depends on it.</p>
        )}
        <p className="muted">Reference data, model weights and other projects are not affected. Backups outside this application are not deleted.</p>
        {error && <Banner tone="danger" live title="Deletion incomplete">{error}</Banner>}
      </Dialog>
    </>
  );
}

/** Choose the project that receives a saved analysis, a job or an import. */
export function ProjectPicker({ value, onChange, label = 'Project' }: { value: string; onChange: (id: string) => void; label?: string }) {
  const q = useQuery({ queryKey: ['projects'], queryFn: ({ signal }) => workspace.listProjects(0, 200, signal), retry: false });
  const items = q.data?.items ?? [];
  if (q.isPending) return <p className="muted">Loading projects…</p>;
  if (!items.length) return <Banner tone="info" title="No project yet">Create a project first; saved work is kept in a project on this computer.</Banner>;
  return (
    <Select
      label={label}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      options={[{ value: '', label: 'Choose a project…' }, ...items.map((p) => ({ value: p.project_id, label: p.name }))]}
    />
  );
}

/** Domain status as text plus pattern hint, never colour alone (W-2). */
export function DomainBadge({ status }: { status: DomainStatus }) {
  const s = STATUS[status];
  return (
    <span className={`ui-pill ${s.needsWarning ? 'ui-pill--warn' : 'ui-pill--neutral'}`} data-status={status}>
      {s.needsWarning && <AlertTriangle size={14} aria-hidden="true" />}
      {s.label}
    </span>
  );
}

export function DownloadButton({ label, fileName, fetchBlob }: { label: string; fileName: string; fetchBlob: () => Promise<Blob> }) {
  const [state, setState] = useState<'idle' | 'busy' | 'error'>('idle');
  return (
    <>
      <Button
        icon={Download}
        busy={state === 'busy'}
        onClick={async () => {
          setState('busy');
          try {
            saveBlob(await fetchBlob(), fileName);
            setState('idle');
          } catch {
            setState('error');
          }
        }}
      >
        {label}
      </Button>
      {state === 'error' && <Banner tone="danger" live>The file could not be created. Nothing on this page was lost.</Banner>}
    </>
  );
}

export function useInvalidateWorkspace() {
  const qc = useQueryClient();
  return () => void qc.invalidateQueries({ predicate: (q) => ['projects', 'project', 'analyses', 'jobs', 'datasets'].includes(String(q.queryKey[0])) });
}
