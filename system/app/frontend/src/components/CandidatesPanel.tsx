import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { workspace } from '../api/client';
import { fmtProb, fmtScore } from '../lib/format';
import { ErrorBanner } from './ErrorBanner';
import { Banner, EmptyState, Select, Skeleton } from './ui';
import { DownloadButton } from './workspace';

/**
 * "Candidates to verify" (plan-system 2.6): the label first, then substitutions of this tile with their reasons. The
 * second analysis for the "models disagree" reason comes from the saved model comparisons of this analysis.
 */
export function CandidatesPanel({ analysisId, projectId }: { analysisId: string; projectId: string }) {
  const comps = useQuery({ queryKey: ['model-comparisons', projectId, analysisId], queryFn: ({ signal }) => workspace.listModelComparisons(projectId, analysisId, signal), retry: false });
  const partners = (comps.data?.items ?? []).map((x) => (x.analysis_a === analysisId ? { id: x.analysis_b, model: x.model_b } : { id: x.analysis_a, model: x.model_a }));
  const [partner, setPartner] = useState('');
  const q = useQuery({ queryKey: ['suggestions', analysisId, partner], queryFn: ({ signal }) => workspace.getSuggestions(analysisId, partner || undefined, signal), retry: false });
  return (
    <div className="stack" data-testid="candidates-panel">
      <Banner tone="info" title="Retrospective priority list" testId="candidates-label">{q.data?.label ?? 'Retrospective priority list, development benchmark; not an experimentally validated design.'}</Banner>
      <p className="muted">Reasons: high score but uncertain (top 10 % with a large spread between the 3 training seeds; ensembles only), the two models disagree (|ΔP| ≥ 0.2 against a compared analysis), a ClinVar variant at that residue. The list is never used to update the model.</p>
      {partners.length > 0 && (
        <Select label="Compare with" value={partner} onChange={(e) => setPartner(e.target.value)}
          options={[{ value: '', label: 'No second analysis' }, ...partners.map((p) => ({ value: p.id, label: `${p.model} (analysis ${p.id.slice(0, 8)})` }))]} />
      )}
      {q.isPending && <Skeleton />}
      {q.isError && <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />}
      {q.data && q.data.excluded_reason && <Banner tone="warn" title="No candidates">{q.data.excluded_reason}</Banner>}
      {q.data && !q.data.excluded_reason && q.data.candidates.length === 0 && (
        <EmptyState title="No candidate with a reason">No substitution of this tile meets a criterion{partners.length ? '' : '; compare with another model first (tab "Other model") to add the disagreement criterion'}.</EmptyState>
      )}
      {q.data && q.data.candidates.length > 0 && (
        <>
          <div className="ui-table__scroll">
            <table className="data" data-testid="candidates-table">
              <caption className="visually-hidden">Candidates to verify, in priority order</caption>
              <thead><tr><th scope="col" className="num">#</th><th scope="col">Substitution</th><th scope="col" className="num">Rank</th><th scope="col" className="num">P</th><th scope="col" className="num">P other</th><th scope="col" className="num">Seed SD</th><th scope="col">Reasons</th></tr></thead>
              <tbody>
                {q.data.candidates.map((c, i) => (
                  <tr key={`${c.position}${c.mut_aa}`}>
                    <td className="num">{i + 1}</td>
                    <td className="mono">{c.wt_aa}{c.position}{c.mut_aa}</td>
                    <td className="num">{c.rank_in_tile}</td>
                    <td className="num">{fmtProb(c.prob)}</td>
                    <td className="num">{c.prob_other === null ? '—' : fmtProb(c.prob_other)}</td>
                    <td className="num">{c.score_seed_sd === null ? '—' : fmtScore(c.score_seed_sd)}</td>
                    <td><ul className="reasons">{c.reasons.map((r) => <li key={r.code}>{r.text}</li>)}</ul></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <DownloadButton label="Export candidates CSV" fileName={`degron-footprint_candidates-${analysisId.slice(0, 8)}.csv`} fetchBlob={() => workspace.exportSuggestions(analysisId, partner || undefined)} />
        </>
      )}
    </div>
  );
}
