import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Play } from 'lucide-react';
import { api, workspace } from '../api/client';
import type { JobRequest, ProteinSummary } from '../api/types';
import { MAX_PEPTIDES, MAX_PROTEIN, MAX_PROTEINS, coverage, parseBatch, parseProteins } from '../lib/batch';
import { resolveModel, useModels } from '../lib/models';
import { ErrorBanner } from './ErrorBanner';
import { useSlowModelConfirm } from './ModelSelect';
import { ProteinSearch } from './ProteinSearch';
import { Banner, Button, Field } from './ui';
import { ProjectPicker } from './workspace';

const PERSISTED = 'Job inputs and results are stored in the chosen project on this computer until you delete them.';

function useSubmit(projectId: string, modelId: string | undefined) {
  const navigate = useNavigate();
  const models = useModels();
  const slow = useSlowModelConfirm(resolveModel(models.data?.items, modelId));
  const m = useMutation({
    mutationFn: (body: JobRequest) => workspace.submitJob(projectId, modelId ? { ...body, model_id: modelId } : body),
    onSuccess: (job) => navigate(`/jobs/${job.job_id}`),
  });
  /** Submits after the slow-model confirmation when the estimate for `tiles` is long (plan-system 1.1). */
  const submit = (body: JobRequest, tiles: number) => slow.run(tiles, () => m.mutate(body));
  return { ...m, submit, dialog: slow.dialog };
}

/** BatchInput, peptide mode (FR-24): pasted records or multi-record FASTA → stable ids, preview before submit. */
export function PeptideBatchForm({ initialProject, modelId }: { initialProject: string; modelId?: string }) {
  const [project, setProject] = useState(initialProject);
  const [text, setText] = useState('');
  const [override, setOverride] = useState(false);
  const preview = parseBatch(text);
  const submit = useSubmit(project, modelId);
  const canSubmit = Boolean(project) && !preview.blocking && text.trim().length > 0;
  return (
    <form
      className="stack"
      onSubmit={(e) => {
        e.preventDefault();
        if (canSubmit) submit.submit({ mode: 'peptides', override_domain: override, peptides: preview.entries.map(({ input_id, sequence }) => ({ input_id, sequence })) }, preview.valid);
      }}
    >
      <ProjectPicker value={project} onChange={setProject} />
      <Field label="Peptides" hint={`Up to ${MAX_PEPTIDES} records: FASTA (">id" lines), "id,SEQUENCE" lines, or one 28-residue sequence per line.`}>
        {({ id, describedBy }) => (
          <textarea id={id} className="ui-textarea" value={text} onChange={(e) => setText(e.target.value)} aria-describedby={describedBy} spellCheck={false} autoComplete="off" translate="no" />
        )}
      </Field>
      {text.trim() && (
        <section className="panel" aria-labelledby="batch-preview-h" data-testid="batch-preview">
          <h2 id="batch-preview-h" style={{ marginTop: 0, fontSize: 'var(--text-lg)' }}>Before you submit</h2>
          <dl className="kv">
            <dt>Records</dt><dd className="num">{preview.entries.length} of at most {MAX_PEPTIDES}</dd>
            <dt>Valid</dt><dd className="num">{preview.valid}</dd>
            <dt>Invalid (listed as refused)</dt><dd className="num">{preview.invalid}</dd>
            <dt>Repeated sequences</dt><dd className="num">{preview.duplicateSequences} (each keeps its own id)</dd>
            <dt>Work</dt><dd>{preview.valid} tiles × 532 substitutions</dd>
          </dl>
          {preview.invalid > 0 && (
            <details>
              <summary>Show the {preview.invalid} invalid entries</summary>
              <ul>{preview.entries.filter((e) => e.problem).map((e) => <li key={e.input_id}><span className="mono">{e.input_id}</span>: {e.problem}</li>)}</ul>
            </details>
          )}
          {preview.blocking && <Banner tone="danger" title="Cannot submit">{preview.blocking}</Banner>}
          <Banner tone="warn" title="Domain">Each peptide gets its domain status from the R3 gate; out-of-domain peptides are refused unless you allow them below. Borderline peptides are scored with a warning.</Banner>
        </section>
      )}
      <label><input type="checkbox" checked={override} onChange={(e) => setOverride(e.target.checked)} /> Score out-of-domain peptides anyway (recorded in the job)</label>
      <p className="muted">{PERSISTED}</p>
      <div className="row">
        <Button type="submit" variant="primary" icon={Play} disabled={!canSubmit} busy={submit.isPending}>Submit batch job</Button>
        {!project && <span className="muted">Choose a project first.</span>}
      </div>
      {submit.isError && <ErrorBanner error={submit.error} />}
      {submit.dialog}
    </form>
  );
}

/** Whole-protein mode (FR-25; several proteins since plan-system 3.3): accessions or FASTA records → full windows. */
export function WholeProteinForm({ initialProject, modelId }: { initialProject: string; modelId?: string }) {
  const [project, setProject] = useState(initialProject);
  const [source, setSource] = useState<'accession' | 'fasta'>('accession');
  const [selected, setSelected] = useState<ProteinSummary[]>([]);
  const [fasta, setFasta] = useState('');
  const [override, setOverride] = useState(false);
  const submit = useSubmit(project, modelId);
  const single = source === 'accession' && selected.length === 1 ? selected[0]! : null;
  const tiles = useQuery({
    queryKey: ['tiles', single?.uniprot_id],
    queryFn: ({ signal }) => api.listTiles(single!.uniprot_id, signal),
    enabled: single !== null,
    retry: false,
  });
  const typed = parseProteins(fasta);
  const rows = source === 'accession'
    ? selected.map((p) => ({ input_id: p.uniprot_id, label: `${p.uniprot_id} ${p.gene_symbol ?? ''}`.trim(), length: p.length, ...coverage(p.length), problem: p.length < 28 ? 'shorter than one tile' : null as string | null }))
    : typed.records.map((r) => ({ input_id: r.input_id, label: r.input_id, length: r.length, tiles: r.tiles, uncovered: r.uncovered, problem: r.blocking }));
  const totalLength = rows.reduce((s2, r) => s2 + r.length, 0);
  const totalTiles = rows.reduce((s2, r) => s2 + (r.problem ? 0 : r.tiles), 0);
  const outOfDomain = tiles.data?.tiles.filter((t) => t.domain_status.endsWith('out_of_domain')).length ?? 0;
  const borderline = tiles.data?.tiles.filter((t) => t.domain_status.endsWith('borderline')).length ?? 0;
  const blocking = source === 'accession'
    ? (selected.length === 0 ? 'Choose a protein.' : totalLength > MAX_PROTEIN ? `At most ${MAX_PROTEIN} residues in total; these have ${totalLength}.` : totalTiles === 0 ? 'Shorter than one tile.' : null)
    : typed.blocking;
  const canSubmit = Boolean(project) && !blocking;

  function body(): JobRequest {
    const list = source === 'accession'
      ? selected.map((p) => ({ uniprot_id: p.uniprot_id }))
      : typed.records.map((r) => ({ input_id: r.input_id, sequence: r.sequence }));
    return list.length === 1
      ? { mode: 'protein', override_domain: override, protein: list[0]! }
      : { mode: 'protein', override_domain: override, proteins: list };
  }

  return (
    <form className="stack" onSubmit={(e) => { e.preventDefault(); if (canSubmit) submit.submit(body(), totalTiles); }}>
      <ProjectPicker value={project} onChange={setProject} />
      <fieldset className="panel">
        <legend>Proteins</legend>
        <div className="row">
          <label><input type="radio" name="protein-source" checked={source === 'accession'} onChange={() => setSource('accession')} /> Loaded human proteins (UniProt)</label>
          <label><input type="radio" name="protein-source" checked={source === 'fasta'} onChange={() => setSource('fasta')} /> FASTA records</label>
        </div>
        {source === 'accession' ? (
          <>
            <ProteinSearch onSelect={(p) => setSelected((cur) => (cur.some((x) => x.uniprot_id === p.uniprot_id) || cur.length >= MAX_PROTEINS ? cur : [...cur, p]))} />
            {selected.length > 0 && (
              <ul className="chips" aria-label="Selected proteins" data-testid="selected-proteins">
                {selected.map((p) => (
                  <li key={p.uniprot_id}>
                    <strong>{p.uniprot_id}</strong> {p.gene_symbol ?? ''} · {p.length} residues{' '}
                    <button type="button" className="link" onClick={() => setSelected((cur) => cur.filter((x) => x.uniprot_id !== p.uniprot_id))} aria-label={`Remove ${p.uniprot_id}`}>Remove</button>
                  </li>
                ))}
              </ul>
            )}
            <p className="muted">Search again to add more proteins (up to {MAX_PROTEINS}).</p>
          </>
        ) : (
          <Field label="FASTA records" hint={`One or more records (">name" lines), up to ${MAX_PROTEINS}. Typed records are not given a UniProt accession; ClinVar is not looked up for them.`}>
            {({ id, describedBy }) => <textarea id={id} className="ui-textarea" value={fasta} onChange={(e) => setFasta(e.target.value)} aria-describedby={describedBy} spellCheck={false} translate="no" />}
          </Field>
        )}
      </fieldset>
      {rows.length > 0 && (
        <section className="panel" aria-labelledby="protein-preview-h" data-testid="protein-preview">
          <h2 id="protein-preview-h" style={{ marginTop: 0, fontSize: 'var(--text-lg)' }}>Before you submit</h2>
          {rows.length === 1 ? (
            <dl className="kv">
              <dt>Length</dt><dd className="num">{rows[0]!.length} residues (limit {MAX_PROTEIN})</dd>
              <dt>Full windows</dt><dd className="num">{rows[0]!.tiles} tiles of 28 residues, step 23</dd>
              <dt>Not covered</dt><dd>{rows[0]!.uncovered.length ? rows[0]!.uncovered.map((u) => `residues ${u.start}–${u.end}`).join(', ') : 'none'}</dd>
              {source === 'fasta' && <><dt>Unscorable windows</dt><dd>{typed.records[0]?.unscorable.length ? `tiles ${typed.records[0].unscorable.join(', ')} (non-standard residue)` : 'none'}</dd></>}
              {tiles.data && <><dt>Domain (R3 gate)</dt><dd>{outOfDomain} out of domain, {borderline} borderline</dd></>}
              <dt>Work</dt><dd>{rows[0]!.tiles} tiles × 532 substitutions</dd>
            </dl>
          ) : (
            <>
              <div className="ui-table__scroll"><table className="data" data-testid="proteins-preview-table">
                <caption className="visually-hidden">Proteins of the job</caption>
                <thead><tr><th scope="col">Protein</th><th scope="col" className="num">Residues</th><th scope="col" className="num">Windows</th><th scope="col">Not covered</th><th scope="col">Problem</th></tr></thead>
                <tbody>{rows.map((r) => (
                  <tr key={r.input_id}><th scope="row">{r.label}</th><td className="num">{r.length}</td><td className="num">{r.tiles}</td>
                    <td>{r.uncovered.length ? r.uncovered.map((u) => `${u.start}–${u.end}`).join(', ') : 'none'}</td>
                    <td>{r.problem ?? '—'}</td></tr>
                ))}</tbody>
              </table></div>
              <p>Total {totalLength} residues of at most {MAX_PROTEIN}; {totalTiles} windows × 532 substitutions. A protein with a problem is listed as refused in the job; the others are scored.</p>
            </>
          )}
          <p className="muted">Each window is scored on its own; overlapping positions keep their tile context and are never averaged. Ranks are per tile.</p>
          {blocking && <Banner tone="danger" title="Cannot submit">{blocking}</Banner>}
        </section>
      )}
      <label><input type="checkbox" checked={override} onChange={(e) => setOverride(e.target.checked)} /> Score out-of-domain tiles anyway (recorded in the job)</label>
      <p className="muted">{PERSISTED}</p>
      <div className="row">
        <Button type="submit" variant="primary" icon={Play} disabled={!canSubmit} busy={submit.isPending}>Submit protein job</Button>
        {!project && <span className="muted">Choose a project first.</span>}
      </div>
      {submit.isError && <ErrorBanner error={submit.error} />}
      {submit.dialog}
    </form>
  );
}
