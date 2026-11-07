import { useId, useState } from 'react';
import { api } from '../api/client';
import { ApiError } from '../api/errors';
import type { ExportFormat, Provenance, TileRequest } from '../api/types';
import { exportFileName, saveBlob } from '../lib/download';
import { fmtDateTime } from '../lib/format';

interface Props {
  /** The request that produced the result. Null on a shared page, which exports by run id. */
  request: TileRequest | null;
  shared?: { runId: string; token: string };
  provenance: Provenance;
  /** Called with the underlying error, for example to log it without the input. */
  onError?: (e: unknown) => void;
}

interface Link {
  url: string;
  expires: string;
}

/** CSV/JSON download (FR-12, FR-13) and the optional share link (FR-20). A failure never removes the result (FR-23). */
export function ExportMenu({ request, shared, provenance, onError }: Props) {
  const id = useId();
  const [busy, setBusy] = useState<ExportFormat | 'share' | null>(null);
  const [message, setMessage] = useState<{ kind: 'ok' | 'error'; text: string } | null>(null);
  const [sharing, setSharing] = useState(false);
  const [ttl, setTtl] = useState(7);
  const [link, setLink] = useState<Link | null>(null);

  async function download(format: ExportFormat) {
    setBusy(format);
    setMessage(null);
    try {
      let blob: Blob;
      if (shared) blob = await api.exportRun(shared.runId, shared.token, format);
      else if (request) blob = await api.exportStateless(request, format);
      else throw new ApiError({ status: 0, code: 'BAD_RESPONSE', message: 'There is nothing to export.' });
      const name = exportFileName(provenance.model_id, request, null, format);
      saveBlob(blob, name);
      setMessage({ kind: 'ok', text: `Downloaded ${name}.` });
    } catch (e) {
      onError?.(e);
      setMessage({ kind: 'error', text: 'The file could not be created. Your result is still here.' });
    } finally {
      setBusy(null);
    }
  }

  async function createLink() {
    if (!request) return;
    setBusy('share');
    setMessage(null);
    try {
      const run = await api.createRun(request, ttl);
      // The token goes into the URL fragment so that it is not sent to the server or logged (api-spec §9).
      setLink({ url: `${window.location.origin}/shared/${run.run_id}#t=${run.share_token}`, expires: run.expires_at });
    } catch (e) {
      onError?.(e);
      setMessage({ kind: 'error', text: 'The share link could not be created. Your result is still here.' });
    } finally {
      setBusy(null);
    }
  }

  return (
    <section aria-labelledby={`${id}-h`} className="card">
      <h2 id={`${id}-h`} style={{ marginTop: 0 }}>Export</h2>
      <div className="row">
        <button type="button" onClick={() => void download('csv')} disabled={busy !== null}>Export CSV</button>
        <button type="button" onClick={() => void download('json')} disabled={busy !== null}>Export JSON</button>
        {request && !shared && (
          <button type="button" className="link" aria-expanded={sharing} onClick={() => setSharing((v) => !v)}>
            Create share link…
          </button>
        )}
      </div>
      <p className="muted" style={{ margin: '0.25rem 0' }}>
        Files contain the model version, data sources, domain status and the disclaimer. Nothing is stored on the server for an export.
      </p>
      {sharing && request && !shared && (
        <div className="card" role="group" aria-label="Share link options">
          <p>
            A share link stores this tile and its result on the server for the number of days you choose (1 to 30, default 7).
            Without the link nobody can read it. This is the only action that stores a sequence.
          </p>
          <label>
            Days stored{' '}
            <input type="number" min={1} max={30} value={ttl} onChange={(e) => setTtl(Math.min(30, Math.max(1, Number(e.target.value) || 7)))} />
          </label>{' '}
          <button type="button" className="primary" onClick={() => void createLink()} disabled={busy !== null}>
            Store and create link
          </button>
          {link && (
            <div role="status">
              <p>
                Link (shown once; expires {fmtDateTime(link.expires)}):
              </p>
              <input type="text" readOnly value={link.url} aria-label="Share link" className="mono" style={{ width: '100%' }} onFocus={(e) => e.currentTarget.select()} />
              <button
                type="button"
                onClick={() => void navigator.clipboard?.writeText(link.url).then(() => setMessage({ kind: 'ok', text: 'Link copied.' }), () => setMessage({ kind: 'error', text: 'The link could not be copied; select it and copy it by hand.' }))}
              >
                Copy link
              </button>
            </div>
          )}
        </div>
      )}
      {message && (
        <div
          className={message.kind === 'error' ? 'banner danger' : 'banner'}
          role={message.kind === 'error' ? 'alert' : 'status'}
          data-testid="export-message"
        >
          {message.text}
        </div>
      )}
    </section>
  );
}
