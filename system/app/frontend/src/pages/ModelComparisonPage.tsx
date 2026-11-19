import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { workspace } from '../api/client';
import { ErrorBanner } from '../components/ErrorBanner';
import { ModelComparisonView } from '../components/ModelComparisonView';
import { Skeleton } from '../components/ui';
import { fmtDateTime } from '../lib/format';
import { useDocumentTitle } from '../lib/hooks';

/** A saved comparison of two analyses / two models (plan-system 2.2). */
export function ModelComparisonPage() {
  const { id = '' } = useParams();
  useDocumentTitle('Model comparison');
  const q = useQuery({ queryKey: ['model-comparison', id], queryFn: ({ signal }) => workspace.getModelComparison(id, signal), retry: false, staleTime: Infinity });
  if (q.isPending) return <Skeleton lines={6} label="Loading the comparison" />;
  if (q.isError) return <><h1>Model comparison</h1><ErrorBanner error={q.error} onRetry={() => void q.refetch()} /><Link to="/projects">Projects</Link></>;
  const c = q.data;
  const t = c.tile;
  return (
    <div className="stack">
      <nav aria-label="Breadcrumb" className="muted"><Link to="/projects">Projects</Link> / <Link to={`/projects/${c.project_id}`}>Project</Link> / Model comparison</nav>
      <div>
        <h1>Model comparison: {t.uniprot_id ? `${t.uniprot_id} tile ${t.tile_index}` : 'typed tile'}</h1>
        <p><span className="seq" translate="no">{t.sequence}</span><br /><span className="muted">Saved {c.created_at ? fmtDateTime(c.created_at) : ''}</span></p>
      </div>
      <ModelComparisonView c={c} />
    </div>
  );
}
