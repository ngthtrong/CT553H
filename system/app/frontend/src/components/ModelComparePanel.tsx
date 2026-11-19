import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { GitCompareArrows } from 'lucide-react';
import { workspace } from '../api/client';
import type { TileRequest } from '../api/types';
import { effectModels, useModels } from '../lib/models';
import { ErrorBanner } from './ErrorBanner';
import { useSlowModelConfirm } from './ModelSelect';
import { Banner, Button, EmptyState, Select, Skeleton } from './ui';

/**
 * "Compare with another model" (plan-system 2.2) on a saved analysis: scores the same input with another serving model
 * as a new analysis linked to this one (A-5), then stores the comparison and opens it. Lists earlier comparisons.
 */
export function ModelComparePanel({ analysisId, projectId, modelId, rerun }: { analysisId: string; projectId: string; modelId: string; rerun: TileRequest }) {
  const navigate = useNavigate();
  const models = useModels();
  const others = effectModels(models.data?.items).filter((m) => m.serving && m.model_id !== modelId);
  const [choice, setChoice] = useState('');
  const picked = others.find((m) => m.model_id === choice) ?? others[0];
  const slow = useSlowModelConfirm(picked);
  const saved = useQuery({ queryKey: ['model-comparisons', projectId, analysisId], queryFn: ({ signal }) => workspace.listModelComparisons(projectId, analysisId, signal), retry: false });
  const run = useMutation({
    mutationFn: async () => {
      const b = await workspace.saveAnalysis(projectId, { ...rerun, model_id: picked!.model_id }, analysisId);
      return workspace.compareAnalyses(analysisId, b.analysis_id, true);
    },
    onSuccess: (c) => navigate(`/model-comparisons/${c.comparison_id}`),
  });
  if (models.isPending || saved.isPending) return <Skeleton />;
  return (
    <div className="stack" data-testid="model-compare-panel">
      <Banner tone="info" title="Descriptive comparison">Comparing two models shows where they agree and differ on this tile; it does not tell which one is right. The second result is saved as a new analysis linked to this one.</Banner>
      {others.length === 0 ? (
        <EmptyState title="No other model is serving">Only one effect model is available in this installation.</EmptyState>
      ) : (
        <form className="panel row" onSubmit={(e) => { e.preventDefault(); if (picked) slow.run(1, () => run.mutate()); }}>
          <Select label="Other model" value={picked?.model_id ?? ''} onChange={(e) => setChoice(e.target.value)} options={others.map((m) => ({ value: m.model_id, label: m.model_id }))} />
          <Button type="submit" variant="primary" icon={GitCompareArrows} busy={run.isPending}>Compare with another model</Button>
          {run.isError && <ErrorBanner error={run.error} />}
          {slow.dialog}
        </form>
      )}
      {saved.data && saved.data.items.length > 0 && (
        <section aria-labelledby="mc-saved-h">
          <h3 id="mc-saved-h">Saved model comparisons</h3>
          <ul data-testid="model-comparison-list">
            {saved.data.items.map((x) => (
              <li key={x.comparison_id}>
                <Link to={`/model-comparisons/${x.comparison_id}`}>{x.model_a} vs {x.model_b}</Link>
                <span className="muted"> · Spearman {x.spearman_raw === null ? 'not defined' : x.spearman_raw.toFixed(2)} · top 10 % Jaccard {x.top_k_jaccard === null ? '—' : x.top_k_jaccard.toFixed(2)}</span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
