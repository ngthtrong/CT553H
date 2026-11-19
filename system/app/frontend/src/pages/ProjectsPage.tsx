import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { FolderKanban, FolderPlus } from 'lucide-react';
import { workspace } from '../api/client';
import { ErrorBanner } from '../components/ErrorBanner';
import { Banner, Button, Dialog, EmptyState, Field, Skeleton } from '../components/ui';
import { useDocumentTitle } from '../lib/hooks';
import { fmtDateTime } from '../lib/format';

/** UC-10, screen 9.1: local projects with their counts; no account, no expiry. */
export function ProjectsPage() {
  useDocumentTitle('Projects');
  const navigate = useNavigate();
  const qc = useQueryClient();
  const q = useQuery({ queryKey: ['projects'], queryFn: ({ signal }) => workspace.listProjects(0, 200, signal), retry: false });
  const [open, setOpen] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const create = useMutation({
    mutationFn: () => workspace.createProject(name.trim(), description.trim()),
    onSuccess: (p) => {
      void qc.invalidateQueries({ queryKey: ['projects'] });
      setOpen(false);
      navigate(`/projects/${p.project_id}`);
    },
  });
  const nameError = name.trim().length > 200 ? 'At most 200 characters.' : null;

  return (
    <div className="stack">
      <div className="page-head">
        <div>
          <h1>Projects</h1>
          <p>Saved analyses, jobs and imported data, kept on this computer until you delete them.</p>
        </div>
        <Button variant="primary" icon={FolderPlus} onClick={() => { setName(''); setDescription(''); create.reset(); setOpen(true); }}>
          New project
        </Button>
      </div>
      {q.isPending && <Skeleton lines={4} label="Loading projects" />}
      {q.isError && <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />}
      {q.isSuccess && q.data.items.length === 0 && (
        <EmptyState icon={FolderKanban} title="No project yet" action={<Button variant="primary" icon={FolderPlus} onClick={() => setOpen(true)}>Create the first project</Button>}>
          A quick prediction does not need a project; saving, batch jobs and imports do.
        </EmptyState>
      )}
      {q.isSuccess && q.data.items.length > 0 && (
        <ul className="grid-cards" aria-label="Projects" data-testid="project-list" style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {q.data.items.map((p) => (
            <li key={p.project_id} className="panel stack" style={{ gap: 'var(--space-2)' }}>
              <h2 style={{ margin: 0, fontSize: '1.1rem' }}>
                <Link to={`/projects/${p.project_id}`}>{p.name}</Link>
              </h2>
              {p.description && <p className="muted" style={{ margin: 0 }}>{p.description}</p>}
              {p.deletion_pending && <Banner tone="danger" title="Deletion not finished">Open the project to retry it.</Banner>}
              <dl className="kv">
                <dt>Analyses</dt><dd className="num">{p.counts.analyses}</dd>
                <dt>Jobs</dt><dd className="num">{p.counts.jobs}</dd>
                <dt>Datasets</dt><dd className="num">{p.counts.datasets}</dd>
                <dt>Updated</dt><dd>{fmtDateTime(p.updated_at)}</dd>
              </dl>
            </li>
          ))}
        </ul>
      )}
      <Dialog
        open={open}
        title="New project"
        onClose={() => setOpen(false)}
        actions={
          <>
            <Button onClick={() => setOpen(false)}>Cancel</Button>
            <Button variant="primary" busy={create.isPending} disabled={!name.trim() || Boolean(nameError)} onClick={() => create.mutate()}>
              Create project
            </Button>
          </>
        }
      >
        <form onSubmit={(e) => { e.preventDefault(); if (name.trim() && !nameError) create.mutate(); }}>
          <Field label="Name" required error={nameError}>
            {({ id, describedBy, invalid }) => (
              <input id={id} className="ui-input" value={name} onChange={(e) => setName(e.target.value)} aria-describedby={describedBy} aria-invalid={invalid || undefined} maxLength={210} />
            )}
          </Field>
          <Field label="Description" hint="Optional; for example the protein or question.">
            {({ id, describedBy }) => <textarea id={id} className="ui-textarea" style={{ fontFamily: 'var(--font-sans)', minHeight: '5rem' }} value={description} onChange={(e) => setDescription(e.target.value)} aria-describedby={describedBy} />}
          </Field>
        </form>
        {create.isError && <ErrorBanner error={create.error} />}
      </Dialog>
    </div>
  );
}
