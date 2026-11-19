import { useState } from 'react';
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { FileUp, FlaskConical, Pencil } from 'lucide-react';
import { workspace } from '../api/client';
import type { Dataset, Job, SavedAnalysisSummary } from '../api/types';
import { AgreementPanel } from '../components/AgreementPanel';
import { ErrorBanner } from '../components/ErrorBanner';
import { Banner, Button, DataTable, Dialog, EmptyState, Field, Skeleton, StatusPill, Tabs, tabPanelProps } from '../components/ui';
import { DeleteConfirmation, DomainBadge } from '../components/workspace';
import { fmtDateTime } from '../lib/format';
import { useDocumentTitle } from '../lib/hooks';

const TABS_ID = 'project-tabs';
type Tab = 'history' | 'jobs' | 'datasets' | 'agreement';

function tileLabel(a: SavedAnalysisSummary): string {
  const t = a.tile;
  return t.uniprot_id ? `${t.uniprot_id} tile ${t.tile_index} (${t.start_pos}–${t.end_pos})` : 'Typed peptide';
}

/** UC-10, screen 9.2: one project with Analysis history · Jobs · Experimental datasets. */
export function ProjectPage() {
  const { id = '' } = useParams();
  const [params, setParams] = useSearchParams();
  const tab = (['history', 'jobs', 'datasets', 'agreement'].includes(params.get('tab') ?? '') ? params.get('tab') : 'history') as Tab;
  const navigate = useNavigate();
  const qc = useQueryClient();
  const project = useQuery({ queryKey: ['project', id], queryFn: ({ signal }) => workspace.getProject(id, signal), retry: false });
  const analyses = useQuery({ queryKey: ['analyses', id], queryFn: ({ signal }) => workspace.listAnalyses(id, 0, 200, signal), retry: false, enabled: tab === 'history' });
  const jobs = useQuery({ queryKey: ['jobs', id], queryFn: ({ signal }) => workspace.listJobs(id, 0, 200, signal), retry: false, enabled: tab === 'jobs' });
  const datasets = useQuery({ queryKey: ['datasets', id], queryFn: ({ signal }) => workspace.listDatasets(id, 0, 200, signal), retry: false, enabled: tab === 'datasets' });
  const [renaming, setRenaming] = useState(false);
  const [name, setName] = useState('');
  const rename = useMutation({
    mutationFn: () => workspace.renameProject(id, { name: name.trim() }),
    onSuccess: () => {
      setRenaming(false);
      void qc.invalidateQueries({ queryKey: ['project', id] });
      void qc.invalidateQueries({ queryKey: ['projects'] });
    },
  });
  useDocumentTitle(project.data?.name ?? 'Project');

  if (project.isPending) return <Skeleton lines={5} label="Loading project" />;
  if (project.isError) return (<><h1>Project</h1><ErrorBanner error={project.error} onRetry={() => void project.refetch()} /><Link to="/projects">All projects</Link></>);
  const p = project.data;

  return (
    <div className="stack">
      <nav aria-label="Breadcrumb" className="muted"><Link to="/projects">Projects</Link> / {p.name}</nav>
      <div className="page-head">
        <div>
          <h1>{p.name}</h1>
          {p.description && <p>{p.description}</p>}
          <p>Updated {fmtDateTime(p.updated_at)}</p>
        </div>
        <div className="row">
          <Button variant="primary" icon={FlaskConical} onClick={() => navigate(`/new?project=${p.project_id}`)}>New analysis</Button>
          <Button icon={FileUp} onClick={() => navigate(`/import?project=${p.project_id}`)}>Import data</Button>
          <Button icon={Pencil} onClick={() => { setName(p.name); rename.reset(); setRenaming(true); }}>Rename</Button>
          <DeleteConfirmation
            what={`project “${p.name}”`}
            remove={(confirm) => workspace.deleteProject(id, confirm)}
            onDeleted={() => { void qc.invalidateQueries({ queryKey: ['projects'] }); navigate('/projects'); }}
          />
        </div>
      </div>
      {p.deletion_pending && (
        <Banner tone="danger" title="Deletion not finished">A previous deletion could not remove the project files. Delete again to retry; nothing new can be saved here meanwhile.</Banner>
      )}

      <Tabs
        id={TABS_ID}
        label="Project sections"
        active={tab}
        onChange={(t) => setParams({ tab: t }, { replace: true })}
        tabs={[
          { id: 'history', label: 'Analysis history', count: p.counts.analyses },
          { id: 'jobs', label: 'Jobs', count: p.counts.jobs },
          { id: 'datasets', label: 'Experimental datasets', count: p.counts.datasets },
          { id: 'agreement', label: 'Agreement over time' },
        ]}
      />
      <div {...tabPanelProps(TABS_ID, tab)}>
        {tab === 'history' && (analyses.isPending ? <Skeleton /> : analyses.isError ? <ErrorBanner error={analyses.error} /> : analyses.data.items.length === 0 ? (
          <EmptyState title="No saved analysis" action={<Button variant="primary" onClick={() => navigate(`/new?project=${p.project_id}`)}>New analysis</Button>}>
            Results are saved only when you choose “Save to project”; a quick preview is not stored.
          </EmptyState>
        ) : (
          <DataTable<SavedAnalysisSummary>
            caption="Analysis history"
            rows={analyses.data.items}
            rowKey={(a) => a.analysis_id}
            onRowClick={(a) => navigate(`/analyses/${a.analysis_id}`)}
            columns={[
              { key: 'date', header: 'Saved', render: (a) => fmtDateTime(a.created_at), sortValue: (a) => a.created_at },
              { key: 'input', header: 'Input', render: (a) => <Link to={`/analyses/${a.analysis_id}`}>{tileLabel(a)}</Link>, sortValue: tileLabel },
              { key: 'domain', header: 'Domain', render: (a) => <DomainBadge status={a.domain_status} />, sortValue: (a) => a.domain_status },
              { key: 'warnings', header: 'Warnings', render: (a) => (a.warning_codes.length ? a.warning_codes.join(', ').replaceAll('_', ' ').toLowerCase() : 'none') },
              { key: 'model', header: 'Model', render: (a) => <code>{a.model_id}</code> },
              { key: 'origin', header: 'Origin', render: (a) => (a.job_id ? <Link to={`/jobs/${a.job_id}`}>job</Link> : a.parent_analysis_id ? 'run again' : 'saved') },
              { key: 'id', header: 'Run ID', render: (a) => <span className="mono">{a.analysis_id.slice(0, 8)}</span> },
            ]}
          />
        ))}
        {tab === 'jobs' && (jobs.isPending ? <Skeleton /> : jobs.isError ? <ErrorBanner error={jobs.error} /> : jobs.data.items.length === 0 ? (
          <EmptyState title="No job" action={<Button variant="primary" onClick={() => navigate(`/new?project=${p.project_id}&mode=batch`)}>Submit a batch</Button>}>
            Peptide batches and whole-protein scans run as jobs and continue after a restart.
          </EmptyState>
        ) : (
          <DataTable<Job>
            caption="Jobs"
            rows={jobs.data.items}
            rowKey={(j) => j.job_id}
            onRowClick={(j) => navigate(`/jobs/${j.job_id}`)}
            columns={[
              { key: 'date', header: 'Submitted', render: (j) => fmtDateTime(j.created_at), sortValue: (j) => j.created_at },
              { key: 'mode', header: 'Mode', render: (j) => <Link to={`/jobs/${j.job_id}`}>{j.mode === 'protein' ? 'Whole protein' : 'Peptide batch'}</Link> },
              { key: 'state', header: 'Status', render: (j) => <StatusPill status={j.state} />, sortValue: (j) => j.state },
              { key: 'done', header: 'Succeeded', render: (j) => `${j.counts.succeeded ?? 0} / ${j.total}`, numeric: true },
              { key: 'refused', header: 'Refused / failed', render: (j) => `${j.counts.refused ?? 0} / ${j.counts.failed ?? 0}`, numeric: true },
            ]}
          />
        ))}
        {tab === 'datasets' && (datasets.isPending ? <Skeleton /> : datasets.isError ? <ErrorBanner error={datasets.error} /> : datasets.data.items.length === 0 ? (
          <EmptyState title="No imported dataset" action={<Button variant="primary" icon={FileUp} onClick={() => navigate(`/import?project=${p.project_id}`)}>Import a CSV/TSV</Button>}>
            Imported measurements are used only for comparison, never to retrain the model.
          </EmptyState>
        ) : (
          <DataTable<Dataset>
            caption="Experimental datasets"
            rows={datasets.data.items}
            rowKey={(d) => d.dataset_id}
            onRowClick={(d) => navigate(`/datasets/${d.dataset_id}`)}
            columns={[
              { key: 'name', header: 'Dataset', render: (d) => <Link to={`/datasets/${d.dataset_id}`}>{d.metadata.name}</Link>, sortValue: (d) => d.metadata.name },
              { key: 'rev', header: 'Revision', render: (d) => d.revision, sortValue: (d) => d.revision, numeric: true },
              { key: 'state', header: 'State', render: (d) => <StatusPill status={d.state} />, sortValue: (d) => d.state },
              { key: 'endpoint', header: 'Endpoint (units)', render: (d) => `${d.metadata.endpoint} (${d.metadata.units})` },
              { key: 'rows', header: 'Valid rows', render: (d) => d.counts.valid ?? 0, numeric: true },
              { key: 'date', header: 'Uploaded', render: (d) => fmtDateTime(d.created_at), sortValue: (d) => d.created_at },
            ]}
          />
        ))}
        {tab === 'agreement' && <AgreementPanel projectId={p.project_id} />}
      </div>

      <Dialog open={renaming} title="Rename project" onClose={() => setRenaming(false)} actions={<><Button onClick={() => setRenaming(false)}>Cancel</Button><Button variant="primary" busy={rename.isPending} disabled={!name.trim() || name.trim().length > 200} onClick={() => rename.mutate()}>Save name</Button></>}>
        <Field label="Name" required error={name.trim().length > 200 ? 'At most 200 characters.' : null}>
          {({ id: fid, describedBy, invalid }) => <input id={fid} className="ui-input" value={name} onChange={(e) => setName(e.target.value)} aria-describedby={describedBy} aria-invalid={invalid || undefined} />}
        </Field>
        {rename.isError && <ErrorBanner error={rename.error} />}
      </Dialog>
    </div>
  );
}
