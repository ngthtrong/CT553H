import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { workspace } from '../api/client';
import type { TileRequest } from '../api/types';
import { AnnotationStatus, ComparisonPanel } from '../components/AnalysisPanels';
import { ErrorBanner } from '../components/ErrorBanner';
import { ModelComparePanel } from '../components/ModelComparePanel';
import { CandidatesPanel } from '../components/CandidatesPanel';
import { ResultView, type SnapshotAnnotations } from '../components/ResultView';
import { SaveAnalysisDialog } from '../components/SaveAnalysisDialog';
import { Banner, Skeleton, Tabs, tabPanelProps } from '../components/ui';
import { DeleteConfirmation } from '../components/workspace';
import { fmtDateTime } from '../lib/format';
import { useDocumentTitle } from '../lib/hooks';
import { ResultHeader } from './ResultPage';

const TABS_ID = 'analysis-tabs';

/** Screen 9.6 (UC-03, UC-10) with the comparison (9.7) and annotation (9.8) tabs: a saved, immutable analysis. */
export function AnalysisPage() {
  const { id = '' } = useParams();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [tab, setTab] = useState('matrix');
  const q = useQuery({ queryKey: ['analysis', id], queryFn: ({ signal }) => workspace.getAnalysis(id, signal), retry: false, staleTime: Infinity });
  useDocumentTitle('Saved analysis');
  if (q.isPending) return <Skeleton lines={6} label="Loading the saved analysis" />;
  if (q.isError) return (<><h1>Saved analysis</h1><ErrorBanner error={q.error} onRetry={() => void q.refetch()} /><Link to="/projects">Projects</Link></>);
  const a = q.data;
  const snap = a.snapshot as { request?: { input_kind?: string; sequence?: string; uniprot_id?: string | null; tile_index?: number | null; override_domain?: boolean }; annotations?: SnapshotAnnotations; model?: { calibrator?: string }; protein_window?: { input_id: string; start_pos: number; end_pos: number } };
  const r = snap.request ?? {};
  // "Run again" re-submits the saved input (never edited) with a model the user picks (default: the service default);
  // the server links the new record (A-5).
  const rerun: TileRequest = r.uniprot_id && r.tile_index
    ? { uniprot_id: r.uniprot_id, tile_index: r.tile_index, override_domain: Boolean(r.override_domain) }
    : { sequence: r.sequence ?? a.result.tile.sequence, override_domain: Boolean(r.override_domain) };
  const annotations = snap.annotations ?? {};
  return (
    <div className="stack">
      <nav aria-label="Breadcrumb" className="muted"><Link to="/projects">Projects</Link> / <Link to={`/projects/${a.project_id}`}>Project</Link> / Saved analysis</nav>
      <div>
        <ResultHeader result={a.result} />
        <p className="muted">
          Saved {fmtDateTime(a.created_at)} · run <span className="mono">{a.analysis_id.slice(0, 8)}</span>
          {snap.model?.calibrator ? ` · calibrator ${snap.model.calibrator}` : ''}
          {snap.protein_window ? ` · window ${snap.protein_window.start_pos}–${snap.protein_window.end_pos} of ${snap.protein_window.input_id}` : ''}
        </p>
        {a.parent_analysis_id && (
          a.parent_available
            ? <p>Run again from <Link to={`/analyses/${a.parent_analysis_id}`}>analysis {a.parent_analysis_id.slice(0, 8)}</Link>.</p>
            : <Banner tone="info" title="Earlier run deleted">This analysis was run again from {a.parent_analysis_id.slice(0, 8)}, which has since been deleted.</Banner>
        )}
      </div>
      <Banner tone="info" title="Saved snapshot">This page shows the result as it was saved, with the model, gate and annotations of that day. It is never recomputed.</Banner>
      <Tabs id={TABS_ID} label="Analysis views" active={tab} onChange={setTab} tabs={[{ id: 'matrix', label: 'Matrix and ranking' }, { id: 'comparison', label: 'Comparison' }, { id: 'models', label: 'Other model' }, { id: 'candidates', label: 'Candidates' }, { id: 'annotations', label: 'ClinVar and annotations' }]} />
      <div {...tabPanelProps(TABS_ID, tab)}>
        {tab === 'matrix' && (
          <ResultView
            result={a.result}
            request={null}
            saved={{ analysisId: a.analysis_id, annotations }}
            actions={
              <>
                <SaveAnalysisDialog request={rerun} parentAnalysisId={a.analysis_id} label="Run again" defaultProject={a.project_id} chooseModel />
                <DeleteConfirmation
                  what="this saved analysis"
                  remove={(confirm) => workspace.deleteAnalysis(a.analysis_id, confirm)}
                  onDeleted={() => { void qc.invalidateQueries({ queryKey: ['analyses', a.project_id] }); navigate(`/projects/${a.project_id}`); }}
                />
              </>
            }
          />
        )}
        {tab === 'comparison' && <ComparisonPanel analysisId={a.analysis_id} projectId={a.project_id} cells={a.result.cells} />}
        {tab === 'models' && <ModelComparePanel analysisId={a.analysis_id} projectId={a.project_id} modelId={a.result.provenance.model_id} rerun={rerun} />}
        {tab === 'candidates' && <CandidatesPanel analysisId={a.analysis_id} projectId={a.project_id} />}
        {tab === 'annotations' && <AnnotationStatus annotations={annotations} />}
      </div>
    </div>
  );
}
