import { Link, useLocation, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { ApiError } from '../api/errors';
import { ErrorBanner } from '../components/ErrorBanner';
import { ResultView } from '../components/ResultView';
import { useDocumentTitle } from '../lib/hooks';
import { ResultHeader } from './ResultPage';

function tokenFrom(hash: string): string | null {
  const m = /(?:^#|&)t=([A-Za-z0-9_-]{22,64})(?:&|$)/.exec(hash);
  return m?.[1] ?? null;
}

/** `/shared/:runId#t=TOKEN` — the token stays in the fragment and is sent only in a header. */
export function SharedPage() {
  const { runId = '' } = useParams();
  const { hash } = useLocation();
  const token = tokenFrom(hash);
  useDocumentTitle('Shared result');

  const q = useQuery({
    queryKey: ['run', runId],
    queryFn: ({ signal }) => api.getRun(runId, token ?? '', signal),
    enabled: token !== null,
    retry: false,
    staleTime: Infinity,
  });

  if (token === null) {
    return (
      <>
        <h1>Shared result</h1>
        <ErrorBanner
          error={new ApiError({ status: 401, code: 'TOKEN_REQUIRED', message: 'This link has no access token.' })}
        />
        <p className="muted">Copy the whole link, including the part after "#".</p>
      </>
    );
  }
  if (q.isPending) return <p role="status" aria-live="polite">Loading the shared result…</p>;
  if (q.isError) {
    return (
      <>
        <h1>Shared result</h1>
        <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />
        <p><Link to="/">Back to the input page</Link></p>
      </>
    );
  }
  return (
    <>
      <ResultHeader result={q.data} />
      <div className="banner" role="note">This is a shared result. It was stored on request and expires automatically.</div>
      <ResultView result={q.data} request={null} shared={{ runId, token }} />
    </>
  );
}
