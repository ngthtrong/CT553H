import { useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { RefreshCw } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { ApiError } from '../api/errors';
import { isStoredTile } from '../api/types';
import type { PredictionResult, TileRequest } from '../api/types';
import { ErrorBanner } from '../components/ErrorBanner';
import { useSlowModelConfirm } from '../components/ModelSelect';
import { RefusalNotice } from '../components/RefusalNotice';
import { ResultView } from '../components/ResultView';
import { SaveAnalysisDialog } from '../components/SaveAnalysisDialog';
import { Button } from '../components/ui';
import { useDocumentTitle } from '../lib/hooks';
import { effectModels, modelQuery, useModelParam, useModels } from '../lib/models';
import { requestStore } from '../state/requestStore';

export function ResultHeader({ result }: { result: PredictionResult | undefined; fallback?: string }) {
  if (!result) return null;
  const t = result.tile;
  const name = t.uniprot_id ? `${t.uniprot_id} tile ${t.tile_index} (residues ${t.start_pos}–${t.end_pos})` : 'Typed tile';
  return (
    <>
      <h1>{name}</h1>
      <p>
        <span className="seq" translate="no">{t.sequence}</span>
        <br />
        <span className="muted">
          Model <code>{result.provenance.model_id}</code> · <Link to={`/model/${encodeURIComponent(result.provenance.model_id)}`}>Model card</Link>
        </span>
      </p>
    </>
  );
}

/**
 * "Run with another model" (plan-system 1.1, A-5): scores the same input with another serving model as a new
 * prediction. The current result is not changed; only the model id goes into the address.
 */
export function RerunWithModel({ current, onPick }: { current: string; onPick: (modelId: string) => void }) {
  const models = useModels();
  const others = effectModels(models.data?.items).filter((m) => m.serving && m.model_id !== current);
  const [choice, setChoice] = useState('');
  const picked = others.find((m) => m.model_id === choice) ?? others[0];
  const slow = useSlowModelConfirm(picked);
  if (others.length === 0) return null;
  return (
    <div className="row rerun-model" data-testid="rerun-model">
      <label>
        <span className="visually-hidden">Other model</span>
        <select className="ui-select" value={picked?.model_id ?? ''} onChange={(e) => setChoice(e.target.value)} aria-label="Other model">
          {others.map((m) => <option key={m.model_id} value={m.model_id}>{m.model_id}</option>)}
        </select>
      </label>
      <Button icon={RefreshCw} onClick={() => picked && slow.run(1, () => onPick(picked.model_id))}>Run with another model</Button>
      {slow.dialog}
    </div>
  );
}

function Loader({ request, backTo, onRerun }: { request: TileRequest; backTo: string; onRerun: (modelId: string) => void }) {
  const navigate = useNavigate();
  const [override, setOverride] = useState(false);
  const stored = isStoredTile(request);
  const effective = useMemo<TileRequest>(() => (override ? { ...request, override_domain: true } : request), [request, override]);

  const q = useQuery({
    queryKey: ['predict', effective],
    queryFn: ({ signal }) => api.predict(effective, signal),
    retry: false,
    staleTime: Infinity,
    // A typed sequence must not outlive the page in the cache (ui-design §9).
    gcTime: stored ? 300_000 : 0,
  });

  useDocumentTitle(q.data?.tile.uniprot_id ? `${q.data.tile.uniprot_id} tile ${q.data.tile.tile_index}` : 'Result');

  if (q.isPending) {
    return (
      <>
        <h1>Scoring…</h1>
        <p role="status" aria-live="polite">Scoring 532 substitutions…</p>
        <div className="skeleton" aria-hidden="true" />
        <button type="button" onClick={() => navigate(backTo)}>Cancel</button>
      </>
    );
  }

  if (q.isError) {
    const err = q.error;
    if (err instanceof ApiError && err.code === 'OUT_OF_DOMAIN') {
      return (
        <>
          <h1>Result</h1>
          <RefusalNotice error={err} onOverride={() => setOverride(true)} onBack={() => navigate(backTo)} />
        </>
      );
    }
    return (
      <>
        <h1>Result</h1>
        <ErrorBanner error={err} onRetry={() => void q.refetch()} />
        <p><Link to={backTo}>Choose another tile</Link></p>
      </>
    );
  }

  return (
    <>
      <ResultHeader result={q.data} />
      <ResultView
        result={q.data}
        request={effective}
        actions={<><SaveAnalysisDialog request={effective} /><RerunWithModel current={q.data.provenance.model_id} onPick={onRerun} /></>}
      />
    </>
  );
}

/** `/result/uniprot/:acc/:n` — addressed by accession and index, so the URL carries no user input. */
export function StoredResultPage() {
  const { acc = '', n = '' } = useParams();
  const navigate = useNavigate();
  const [modelId] = useModelParam();
  const index = Number(n);
  if (!Number.isInteger(index) || index < 1) {
    return (
      <>
        <h1>Result</h1>
        <div className="banner danger" role="alert"><span className="label">Error</span>The tile number in the address is not valid.</div>
      </>
    );
  }
  const request: TileRequest = modelId ? { uniprot_id: acc, tile_index: index, model_id: modelId } : { uniprot_id: acc, tile_index: index };
  return (
    <Loader
      key={`${acc}/${index}/${modelId ?? ''}`}
      request={request}
      backTo={`/protein/${acc}${modelQuery(modelId)}`}
      onRerun={(m) => navigate(`/result/uniprot/${acc}/${index}${modelQuery(m)}`)}
    />
  );
}

/** `/result` — a typed sequence is read from memory; after a reload there is nothing to show by design. */
export function TypedResultPage() {
  const [request, setRequest] = useState(() => requestStore.get());
  useDocumentTitle('Result');
  if (!request) {
    return (
      <>
        <h1>Result</h1>
        <div className="banner" role="status">
          There is no sequence in memory. A typed sequence is never kept in the address or in the browser storage, so it is gone
          after a reload. <Link to="/">Enter it again</Link>.
        </div>
      </>
    );
  }
  return (
    <Loader
      key={request.model_id ?? ''}
      request={request}
      backTo="/"
      onRerun={(m) => { const next = { ...request, model_id: m }; requestStore.set(next); setRequest(next); }}
    />
  );
}
