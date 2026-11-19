import { useState } from 'react';
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { CheckCircle2, FileUp } from 'lucide-react';
import { workspace } from '../api/client';
import type { Dataset, ImportMetadata } from '../api/types';
import { ErrorBanner } from '../components/ErrorBanner';
import { Banner, Button, Field, Select, Skeleton, StatusPill } from '../components/ui';
import { DeleteConfirmation, ProjectPicker } from '../components/workspace';
import { fmtDateTime } from '../lib/format';
import { useDocumentTitle } from '../lib/hooks';

const NOTE = 'Comparison only; not used to retrain the model.';
const COLUMNS = 'peptide_id, wt_sequence, position, wt_aa, mut_aa, observed_value, replicate_id; optional missing_reason, uniprot_id + reference_release + start_pos';

/** ValidationReport: counts, file hash, row-specific issues, staged versus committed. */
export function ValidationReport({ d }: { d: Dataset }) {
  const errors = d.issues.filter((i) => i.severity === 'error');
  const warnings = d.issues.filter((i) => i.severity === 'warning');
  return (
    <section className="panel stack" aria-labelledby="report-h" data-testid="validation-report">
      <div className="row" style={{ justifyContent: 'space-between' }}>
        <h2 id="report-h" style={{ margin: 0, fontSize: '1.1rem' }}>{d.metadata.name} · revision {d.revision}</h2>
        <StatusPill status={d.state} />
      </div>
      <dl className="kv">
        <dt>File SHA-256</dt><dd className="mono">{d.sha256}</dd>
        <dt>Endpoint (units)</dt><dd>{d.metadata.endpoint} ({d.metadata.units}) · {d.metadata.compatibility === 'zhang_gps_dpsi' ? 'declared comparable with GPS ΔPSI' : 'other endpoint (no pooled metric)'}</dd>
        {Object.entries(d.counts).map(([k, v]) => <div key={k} style={{ display: 'contents' }}><dt>{k.replaceAll('_', ' ')}</dt><dd className="num">{v}</dd></div>)}
      </dl>
      {errors.length > 0 && (
        <Banner tone="danger" title={`${errors.length} blocking issue${errors.length > 1 ? 's' : ''}`}>
          Fix the file and upload it again; this preview cannot be committed.
        </Banner>
      )}
      {warnings.length > 0 && <Banner tone="warn" title={`${warnings.length} warning${warnings.length > 1 ? 's' : ''}`}>Committing requires acknowledging them.</Banner>}
      {d.issues.length > 0 && (
        <div className="ui-table__scroll" style={{ maxHeight: '20rem' }}>
          <table className="data">
            <caption className="visually-hidden">Validation issues by row</caption>
            <thead><tr><th scope="col" className="num">Row</th><th scope="col">Severity</th><th scope="col">Code</th><th scope="col">What to correct</th></tr></thead>
            <tbody>
              {d.issues.map((i, n) => (
                <tr key={`${i.row ?? 'file'}-${i.code}-${n}`}>
                  <td className="num">{i.row ?? 'file'}</td>
                  <td>{i.severity}</td>
                  <td><code>{i.code}</code></td>
                  <td>{i.message}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <p className="muted">{NOTE} Missing values are kept as missing, never read as 0.</p>
    </section>
  );
}

/** ImportWizard (9.10, UC-09): file + metadata → staged preview → acknowledge warnings → commit an immutable revision. */
export function ImportPage() {
  useDocumentTitle('Import data');
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [project, setProject] = useState(params.get('project') ?? '');
  const [file, setFile] = useState<File | null>(null);
  const [meta, setMeta] = useState<ImportMetadata>({ name: '', assay: 'GPS', endpoint: 'delta_psi', units: 'PSI', source: '', reference_description: '', compatibility: 'zhang_gps_dpsi' });
  const [ack, setAck] = useState(false);
  const preview = useMutation({ mutationFn: () => workspace.previewImport(project, file!, meta), onSuccess: () => setAck(false) });
  const commit = useMutation({
    mutationFn: (d: Dataset) => workspace.commitDataset(d.dataset_id, ack),
    onSuccess: (d) => { void qc.invalidateQueries({ queryKey: ['datasets', d.project_id] }); navigate(`/datasets/${d.dataset_id}`); },
  });
  const set = (k: keyof ImportMetadata) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setMeta((m) => ({ ...m, [k]: e.target.value }));
  const required: (keyof ImportMetadata)[] = ['name', 'assay', 'endpoint', 'units', 'source', 'reference_description'];
  const ready = Boolean(project && file && required.every((k) => String(meta[k] ?? '').trim()));
  const d = preview.data;
  const hasWarnings = d?.issues.some((i) => i.severity === 'warning') ?? false;
  const text = (k: keyof ImportMetadata, label: string, hint?: string) => (
    <Field label={label} required={required.includes(k)} hint={hint}>
      {({ id, describedBy }) => <input id={id} className="ui-input" value={String(meta[k] ?? '')} onChange={set(k)} aria-describedby={describedBy} />}
    </Field>
  );
  return (
    <div className="stack">
      <div className="page-head">
        <div>
          <h1>Import experimental data</h1>
          <p>{NOTE}</p>
        </div>
      </div>
      <form className="panel" onSubmit={(e) => { e.preventDefault(); if (ready) preview.mutate(); }}>
        <ProjectPicker value={project} onChange={setProject} />
        <Field label="CSV or TSV file" required hint={`Up to 10 MiB / 100,000 rows. Columns: ${COLUMNS}.`}>
          {({ id, describedBy }) => <input id={id} type="file" accept=".csv,.tsv,text/csv,text/tab-separated-values" className="ui-input" aria-describedby={describedBy} onChange={(e) => setFile(e.target.files?.[0] ?? null)} />}
        </Field>
        {text('name', 'Dataset name', 'A new file with the same name becomes a new revision.')}
        <div className="grid-cards">
          {text('assay', 'Assay')}
          {text('assay_version', 'Assay version')}
          {text('endpoint', 'Endpoint')}
          {text('units', 'Units')}
        </div>
        {text('source', 'Source or citation')}
        {text('reference_description', 'Reference description', 'For example the protein, tile or construct.')}
        <Select label="Comparability" value={meta.compatibility} onChange={set('compatibility')}
          options={[{ value: 'zhang_gps_dpsi', label: 'Same endpoint as the model (GPS ΔPSI, PSI units)' }, { value: 'other', label: 'Other endpoint (shown in its own units, no pooled metric)' }]} />
        {text('rights_note', 'Rights or provenance note')}
        <Button type="submit" variant="primary" icon={FileUp} disabled={!ready} busy={preview.isPending}>Validate file</Button>
        {preview.isError && <ErrorBanner error={preview.error} />}
      </form>
      {d && (
        <>
          <ValidationReport d={d} />
          {d.committable && (
            <div className="panel stack">
              {hasWarnings && <label><input type="checkbox" checked={ack} onChange={(e) => setAck(e.target.checked)} /> I have read the warnings and want to commit anyway</label>}
              <p>Committing stores revision {d.revision} in the project. It cannot be edited afterwards; a corrected file becomes a new revision.</p>
              <Button variant="primary" icon={CheckCircle2} disabled={hasWarnings && !ack} busy={commit.isPending} onClick={() => commit.mutate(d)}>Commit dataset</Button>
              {commit.isError && <ErrorBanner error={commit.error} />}
            </div>
          )}
        </>
      )}
    </div>
  );
}

/** DatasetList entry / deletion (9.11, UC-09, UC-10). */
export function DatasetPage() {
  const { id = '' } = useParams();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const q = useQuery({ queryKey: ['dataset', id], queryFn: ({ signal }) => workspace.getDataset(id, signal), retry: false });
  useDocumentTitle('Dataset');
  if (q.isPending) return <Skeleton lines={5} label="Loading dataset" />;
  if (q.isError) return (<><h1>Dataset</h1><ErrorBanner error={q.error} onRetry={() => void q.refetch()} /></>);
  const d = q.data;
  return (
    <div className="stack">
      <nav aria-label="Breadcrumb" className="muted"><Link to="/projects">Projects</Link> / <Link to={`/projects/${d.project_id}?tab=datasets`}>Project</Link> / Dataset</nav>
      <div className="page-head">
        <div>
          <h1>{d.metadata.name}</h1>
          <p>Uploaded {fmtDateTime(d.created_at)}{d.committed_at ? ` · committed ${fmtDateTime(d.committed_at)}` : ''}</p>
        </div>
        <DeleteConfirmation what={`dataset “${d.metadata.name}” revision ${d.revision}`} remove={(confirm) => workspace.deleteDataset(d.dataset_id, confirm)}
          onDeleted={() => { void qc.invalidateQueries({ queryKey: ['datasets', d.project_id] }); navigate(`/projects/${d.project_id}?tab=datasets`); }} />
      </div>
      {d.state === 'staged' && <Banner tone="warn" title="Staged, not committed">This preview is not part of the project yet and expires if it is not committed. Open the import page to commit a validated file.</Banner>}
      {d.state === 'expired' && <Banner tone="info" title="Preview expired">Upload the file again to continue.</Banner>}
      <dl className="kv panel">
        <dt>Assay</dt><dd>{d.metadata.assay}{d.metadata.assay_version ? ` (${d.metadata.assay_version})` : ''}</dd>
        <dt>Source</dt><dd>{d.metadata.source}</dd>
        <dt>Reference</dt><dd>{d.metadata.reference_description}</dd>
        {d.metadata.rights_note && <><dt>Rights</dt><dd>{d.metadata.rights_note}</dd></>}
      </dl>
      <ValidationReport d={d} />
    </div>
  );
}
