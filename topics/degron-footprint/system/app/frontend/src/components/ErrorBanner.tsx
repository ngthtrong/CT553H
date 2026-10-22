import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ApiError, ERROR_HINTS } from '../api/errors';
import { api } from '../api/client';

function useCountdown(seconds: number | null): number {
  const [left, setLeft] = useState(seconds ?? 0);
  useEffect(() => {
    setLeft(seconds ?? 0);
    if (!seconds) return undefined;
    const t = setInterval(() => setLeft((s) => (s > 0 ? s - 1 : 0)), 1000);
    return () => clearInterval(t);
  }, [seconds]);
  return left;
}

/** Maps an error to the message of ui-design §3.4. The server message is shown first, then a client hint. */
export function ErrorBanner({ error, onRetry }: { error: unknown; onRetry?: () => void }) {
  const err = error instanceof ApiError ? error : null;
  const left = useCountdown(err?.code === 'RATE_LIMITED' ? (err.retryAfter ?? 30) : null);
  const unavailable = err?.code === 'SERVICE_UNAVAILABLE' || err?.code === 'NETWORK';

  // While the service is unavailable, poll /healthz every 10 s and offer a retry as soon as it answers.
  const health = useQuery({
    queryKey: ['healthz'],
    queryFn: ({ signal }) => api.health(signal),
    enabled: unavailable,
    refetchInterval: 10_000,
    retry: false,
    gcTime: 0,
  });

  if (!err) {
    return (
      <div className="banner danger" role="alert">
        <span className="label">Error</span>Something went wrong. Try again.
      </div>
    );
  }

  const hint = ERROR_HINTS[err.code];

  if (err.code === 'RATE_LIMITED') {
    return (
      <div className="banner danger" role="alert">
        <span className="label">Error</span>Too many requests. Try again in {left} second{left === 1 ? '' : 's'}.
        {onRetry && (
          <>
            {' '}
            <button type="button" onClick={onRetry} disabled={left > 0}>
              Try again
            </button>
          </>
        )}
      </div>
    );
  }

  if (err.code === 'RUN_EXPIRED') {
    return (
      <div className="banner" role="alert">
        <span className="label">Expired</span>This shared result has expired.
      </div>
    );
  }

  if (err.code === 'SERVICE_UNAVAILABLE') {
    const ready = health.data?.status === 'ok';
    return (
      <div className="banner danger" role="alert">
        <span className="label">Error</span>The service is not ready (model or database unavailable).{' '}
        {ready ? (
          <>
            It seems to be back.{' '}
            <button type="button" className="link" onClick={onRetry}>
              Retry
            </button>
          </>
        ) : (
          <span className="muted">Checking every 10 seconds.</span>
        )}
      </div>
    );
  }

  return (
    <div className="banner danger" role="alert">
      <span className="label">Error</span>
      {err.message}
      {hint && <> {hint}</>}
      {err.requestId && (
        <span className="muted">
          {' '}
          (reference {err.requestId})
        </span>
      )}
      {onRetry && err.code === 'NETWORK' && (
        <>
          {' '}
          <button type="button" className="link" onClick={onRetry}>
            Retry
          </button>
        </>
      )}
    </div>
  );
}
