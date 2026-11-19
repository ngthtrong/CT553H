import { Fragment, useState } from 'react';
import { Link } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { GitCompareArrows } from 'lucide-react';
import { workspace } from '../api/client';
import type { Cell, ClinvarVariant, Comparison, ComparisonRequest } from '../api/types';
import type { ComparisonRow } from '../lib/comparisonCharts';
import { ComparisonCharts } from './ComparisonCharts';
import { CLINVAR_LABEL } from './Heatmap';
import { ErrorBanner } from './ErrorBanner';
import type { SnapshotAnnotations } from './ResultView';
import { Banner, Button, EmptyState, Field, Select, Skeleton } from './ui';
import { DownloadButton } from './workspace';

const NOTE = 'Comparison only; imported measurements are not used to retrain the model and are not an independent validation.';

function ComparisonResult({ c, analysisId, cells }: { c: Comparison; analysisId: string; cells: Cell[] }) {
  const prov = c.provenance as { dataset_name?: string; dataset_revision?: number; endpoint?: string; units?: string; replicate_id?: string | null; aggregation?: string | null };
  const rows = c.rows as { position: number; wt_aa: string; mut_aa: string; observed: number; n_replicates: number; units: string; predicted_dpsi_raw: number | null; residual: number | null }[];
  return (
    <section className="panel stack" aria-label="Comparison result" data-testid="comparison-result">
      <p style={{ margin: 0 }}>
        <strong>{prov.dataset_name}</strong> revision {prov.dataset_revision} · {prov.endpoint} ({prov.units}) ·{' '}
        {prov.replicate_id ? `replicate ${prov.replicate_id}` : `${prov.aggregation} of replicates`}
      </p>
      {!c.compatible && <Banner tone="warn" title="Different endpoint">{c.metric_unavailable_reason}</Banner>}
      <dl className="kv">
        <dt>Matched substitutions (n)</dt><dd className="num">{c.matched}</dd>
        {Object.entries(c.counts).filter(([k]) => k !== 'matched').map(([k, v]) => (
          <Fragment key={k}><dt>{k.replaceAll('_', ' ')}</dt><dd className="num">{v}</dd></Fragment>
        ))}
        <dt>MAE (predicted raw ΔPSI − observed)</dt><dd className="num">{c.mae === null ? 'not defined' : c.mae.toFixed(3)}</dd>
        <dt>Spearman ρ</dt><dd className="num">{c.spearman === null ? 'not defined' : c.spearman.toFixed(3)}</dd>
      </dl>
      {c.compatible && c.metric_unavailable_reason && <Banner tone="info" title="Metric not defined">{c.metric_unavailable_reason}</Banner>}
      <p className="muted">{NOTE} The calibrated probability is compared only with the observed event ΔPSI ≥ 1 (calibration chart), never with the ΔPSI value itself.</p>
      <ComparisonCharts rows={rows as ComparisonRow[]} cells={cells} compatible={c.compatible} units={prov.units ?? ''} />
      <div className="ui-table__scroll" style={{ maxHeight: '22rem' }}>
        <table className="data">
          <caption className="visually-hidden">Matched substitutions</caption>
          <thead><tr><th scope="col">Substitution</th><th scope="col" className="num">Observed ({prov.units})</th><th scope="col" className="num">Replicates</th>{c.compatible && <><th scope="col" className="num">Predicted raw ΔPSI</th><th scope="col" className="num">Residual</th></>}</tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={`${r.position}${r.mut_aa}`}>
                <td className="mono">{r.wt_aa}{r.position}{r.mut_aa}</td>
                <td className="num">{r.observed.toFixed(3)}</td>
                <td className="num">{r.n_replicates}</td>
                {c.compatible && <><td className="num">{r.predicted_dpsi_raw?.toFixed(3)}</td><td className="num">{r.residual?.toFixed(3)}</td></>}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <DownloadButton label="Export CSV with this comparison" fileName={`degron-footprint_analysis-${analysisId.slice(0, 8)}_comparison.csv`} fetchBlob={() => workspace.exportAnalysis(analysisId, 'csv', c.comparison_id)} />
    </section>
  );
}

/** ComparisonPanel (9.7, UC-05): one committed dataset, one replicate or an explicit aggregation. */
export function ComparisonPanel({ analysisId, projectId, cells }: { analysisId: string; projectId: string; cells: Cell[] }) {
  const qc = useQueryClient();
  const datasets = useQuery({ queryKey: ['datasets', projectId], queryFn: ({ signal }) => workspace.listDatasets(projectId, 0, 200, signal), retry: false });
  const existing = useQuery({ queryKey: ['comparisons', analysisId], queryFn: ({ signal }) => workspace.listComparisons(analysisId, signal), retry: false });
  const [dataset, setDataset] = useState('');
  const [how, setHow] = useState<'replicate' | 'mean' | 'median'>('mean');
  const [replicate, setReplicate] = useState('');
  const [shown, setShown] = useState<string | null>(null);
  const compare = useMutation({
    mutationFn: () => {
      const body: ComparisonRequest = how === 'replicate' ? { dataset_id: dataset, replicate_id: replicate.trim() } : { dataset_id: dataset, aggregation: how };
      return workspace.compare(analysisId, body);
    },
    onSuccess: (c) => { setShown(c.comparison_id); void qc.invalidateQueries({ queryKey: ['comparisons', analysisId] }); },
  });
  if (datasets.isPending || existing.isPending) return <Skeleton />;
  if (datasets.isError) return <ErrorBanner error={datasets.error} />;
  const committed = datasets.data.items.filter((d) => d.state === 'committed');
  const list = existing.data?.items ?? [];
  const current = list.find((c) => c.comparison_id === shown) ?? (compare.data?.comparison_id === shown ? compare.data : undefined);
  return (
    <div className="stack">
      <Banner tone="info" title="Comparison only" testId="comparison-note">{NOTE}</Banner>
      {committed.length === 0 ? (
        <EmptyState title="No committed dataset in this project" action={<Link to={`/import?project=${projectId}`}>Import a CSV/TSV</Link>}>
          Staged previews cannot be compared; commit a dataset first.
        </EmptyState>
      ) : (
        <form className="panel" onSubmit={(e) => { e.preventDefault(); if (dataset && (how !== 'replicate' || replicate.trim())) compare.mutate(); }}>
          <Select label="Dataset" value={dataset} onChange={(e) => setDataset(e.target.value)}
            options={[{ value: '', label: 'Choose a committed dataset…' }, ...committed.map((d) => ({ value: d.dataset_id, label: `${d.metadata.name} (revision ${d.revision}; ${d.metadata.endpoint}, ${d.metadata.units})` }))]} />
          <fieldset>
            <legend>Replicates</legend>
            <label><input type="radio" name="cmp-how" checked={how === 'mean'} onChange={() => setHow('mean')} /> Mean of replicates</label>
            <label><input type="radio" name="cmp-how" checked={how === 'median'} onChange={() => setHow('median')} /> Median of replicates</label>
            <label><input type="radio" name="cmp-how" checked={how === 'replicate'} onChange={() => setHow('replicate')} /> One replicate</label>
          </fieldset>
          {how === 'replicate' && (
            <Field label="Replicate id">{({ id, describedBy }) => <input id={id} className="ui-input" value={replicate} onChange={(e) => setReplicate(e.target.value)} aria-describedby={describedBy} />}</Field>
          )}
          <Button type="submit" variant="primary" icon={GitCompareArrows} busy={compare.isPending} disabled={!dataset || (how === 'replicate' && !replicate.trim())}>Compare</Button>
          {compare.isError && <ErrorBanner error={compare.error} />}
        </form>
      )}
      {current && <ComparisonResult c={current} analysisId={analysisId} cells={cells} />}
      {list.length > 0 && (
        <section aria-labelledby="cmp-list-h">
          <h3 id="cmp-list-h">Saved comparisons</h3>
          <ul>
            {list.map((c) => (
              <li key={c.comparison_id}>
                <button type="button" className="link" onClick={() => setShown(c.comparison_id)}>
                  {(c.provenance as { dataset_name?: string }).dataset_name} · n = {c.matched}{c.compatible ? '' : ' · separate units'}
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}

const CLINVAR_STATE: Record<string, { tone: 'info' | 'warn' | 'danger' | 'success'; title: string; text: string }> = {
  available: { tone: 'success', title: 'ClinVar variants found', text: 'Missense variants of this tile at the time of the analysis.' },
  no_match: { tone: 'info', title: 'No matching variant', text: 'ClinVar was loaded and has no missense variant in this tile. Absence is not evidence that a substitution is benign.' },
  mapping_unavailable: { tone: 'info', title: 'Mapping unavailable', text: 'A typed sequence has no verified UniProt mapping, so ClinVar was not looked up. No annotation is guessed.' },
  source_unavailable: { tone: 'warn', title: 'Source unavailable', text: 'ClinVar was not loaded when this analysis was saved. This does not mean there are no variants.' },
  mapping_conflict: { tone: 'danger', title: 'Mapping conflict', text: 'At least one ClinVar reference residue differs from the tile residue at that position; those variants are flagged below.' },
};

/** AnnotationStatus (9.8, UC-06): ClinVar and measured layers from the analysis snapshot, four empty cases kept apart. */
export function AnnotationStatus({ annotations }: { annotations: SnapshotAnnotations }) {
  const cv = annotations.clinvar ?? { state: 'source_unavailable' };
  const state = CLINVAR_STATE[cv.state ?? 'source_unavailable'] ?? CLINVAR_STATE.source_unavailable!;
  const variants = (cv.variants ?? []) as (ClinvarVariant & { residue_matches?: boolean })[];
  const measured = annotations.measured;
  return (
    <div className="stack">
      <section aria-labelledby="ann-clinvar-h">
        <h3 id="ann-clinvar-h">ClinVar</h3>
        <div data-testid="annotation-status" data-state={cv.state}><Banner tone={state.tone} title={state.title}>{state.text}</Banner></div>
        {cv.clinvar_file_date && <p className="muted">ClinVar file dated {cv.clinvar_file_date} (snapshot of the analysis).</p>}
        {variants.length > 0 && (
          <div className="ui-table__scroll">
            <table className="data">
              <caption className="visually-hidden">ClinVar variants in the tile</caption>
              <thead><tr><th scope="col">Variant</th><th scope="col">Protein position</th><th scope="col">Classification</th><th scope="col">Review status</th><th scope="col">Reference residue</th></tr></thead>
              <tbody>
                {variants.map((v) => (
                  <tr key={v.variation_id}>
                    <td className="mono">{v.ref_aa}{v.position}{v.alt_aa}</td>
                    <td className="num">{v.protein_pos}</td>
                    <td>{CLINVAR_LABEL[v.clinsig] ?? v.clinsig}</td>
                    <td>{v.review_status ?? 'not given'}</td>
                    <td>{v.residue_matches === false ? <strong>does not match the tile</strong> : 'matches the tile'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {(cv.sources ?? []).map((s) => (
          <p key={s.attribution_text} className="muted">{s.attribution_text}{s.disclaimer_text ? ` ${s.disclaimer_text}` : ''}</p>
        ))}
        <p className="muted">ClinVar classifications are not diagnoses, and the model scores are not probabilities of disease.</p>
      </section>
      <section aria-labelledby="ann-measured-h">
        <h3 id="ann-measured-h">Measured ΔPSI (training reference)</h3>
        <p>
          {measured?.state === 'available'
            ? `${measured.cells?.length ?? 0} measured substitutions. These are training data of this model, not a validation.`
            : measured?.state === 'mapping_unavailable'
              ? 'Not applicable: a typed sequence has no measured reference.'
              : 'This tile has no measured saturation data.'}
        </p>
      </section>
    </div>
  );
}
