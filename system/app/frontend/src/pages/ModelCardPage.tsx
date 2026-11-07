import type { ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { ErrorBanner } from '../components/ErrorBanner';
import { useDocumentTitle } from '../lib/hooks';

/** Flatten a free-form metrics object into rows of (path, value). Numbers are shown as the API sent them. */
export function flattenMetrics(value: unknown, path = ''): { key: string; value: string }[] {
  if (value === null || value === undefined) return [];
  if (Array.isArray(value)) {
    if (value.every((v) => typeof v === 'number')) return [{ key: path, value: `[${value.join(', ')}]` }];
    return value.flatMap((v, i) => flattenMetrics(v, `${path}[${i}]`));
  }
  if (typeof value === 'object') {
    return Object.entries(value as Record<string, unknown>).flatMap(([k, v]) => flattenMetrics(v, path ? `${path}.${k}` : k));
  }
  return [{ key: path, value: String(value) }];
}

function inline(text: string): ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/).map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**') && part.length > 4) return <strong key={i}>{part.slice(2, -2)}</strong>;
    if (part.startsWith('`') && part.endsWith('`') && part.length > 2) return <code key={i}>{part.slice(1, -1)}</code>;
    return part;
  });
}

/**
 * Minimal safe renderer for card_markdown: headings, bullet lists, paragraphs, **bold** and `code`.
 * Everything is built as React nodes, so no HTML in the text is ever interpreted.
 */
export function SimpleMarkdown({ text }: { text: string }) {
  const out: ReactNode[] = [];
  let list: string[] = [];
  let para: string[] = [];
  const flushList = () => {
    if (list.length) {
      out.push(<ul key={`u${out.length}`}>{list.map((l, i) => <li key={i}>{inline(l)}</li>)}</ul>);
      list = [];
    }
  };
  const flushPara = () => {
    if (para.length) {
      out.push(<p key={`p${out.length}`}>{inline(para.join(' '))}</p>);
      para = [];
    }
  };
  for (const line of text.split(/\r?\n/)) {
    const h = /^(#{1,4})\s+(.*)$/.exec(line);
    const li = /^\s*[-*]\s+(.*)$/.exec(line);
    if (li?.[1] !== undefined) {
      flushPara();
      list.push(li[1]);
    } else if (h?.[2] !== undefined) {
      flushPara();
      flushList();
      out.push(<h3 key={`h${out.length}`}>{inline(h[2])}</h3>);
    } else if (line.trim() === '') {
      flushPara();
      flushList();
    } else {
      flushList();
      para.push(line.trim());
    }
  }
  flushPara();
  flushList();
  return <>{out}</>;
}

export function ModelCardPage() {
  useDocumentTitle('Model card');
  const models = useQuery({ queryKey: ['models'], queryFn: ({ signal }) => api.listModels(signal), retry: false, staleTime: 300_000 });
  const defaultId = models.data?.items.find((m) => m.is_default && m.role === 'effect')?.model_id ?? models.data?.items.find((m) => m.is_default)?.model_id;
  const card = useQuery({
    queryKey: ['model', defaultId],
    queryFn: ({ signal }) => api.getModel(defaultId!, signal),
    enabled: defaultId !== undefined,
    retry: false,
    staleTime: 300_000,
  });

  if (models.isError) return <><h1>Model card</h1><ErrorBanner error={models.error} onRetry={() => void models.refetch()} /></>;
  if (models.isPending || (defaultId !== undefined && card.isPending)) return <p role="status" aria-live="polite">Loading the model card…</p>;
  if (card.isError) return <><h1>Model card</h1><ErrorBanner error={card.error} onRetry={() => void card.refetch()} /></>;
  if (!card.data) return <><h1>Model card</h1><p>No model is registered.</p></>;

  const m = card.data;
  const metrics = flattenMetrics(m.metrics);
  return (
    <>
      <h1>Model <code>{m.model_id}</code></h1>
      <p>
        Status: <strong>{m.status}</strong>
        {m.is_default ? ' (default)' : ''} · role: {m.role}
        {m.kind ? ` · kind: ${m.kind}` : ''}
        {m.frozen_at ? ` · frozen ${m.frozen_at}` : ''}
      </p>
      <dl className="card">
        <dt><strong>What it predicts</strong></dt>
        <dd>{m.event_definition} in the GPS assay (Zhang et al. 2023)</dd>
        <dt><strong>Domain</strong></dt>
        <dd>{m.domain_description}</dd>
        <dt><strong>Evidence</strong></dt>
        <dd>{m.evidence_label}</dd>
        <dt><strong>Weights SHA-256</strong></dt>
        <dd><code>{m.weights_sha256}</code></dd>
      </dl>

      <h2>Performance</h2>
      <p className="muted">Values are read from the API; source file: <code>{m.metrics_source_file}</code>.</p>
      {metrics.length === 0 ? <p>No metrics are registered for this model.</p> : (
        <table className="data" data-testid="metrics-table">
          <caption className="visually-hidden">Metrics of the model</caption>
          <thead><tr><th scope="col">Metric</th><th scope="col">Value</th></tr></thead>
          <tbody>{metrics.map((r) => <tr key={r.key}><th scope="row">{r.key}</th><td>{r.value}</td></tr>)}</tbody>
        </table>
      )}
      {m.calibration && (
        <>
          <h2>Calibration</h2>
          <table className="data">
            <caption className="visually-hidden">Calibration of the probability</caption>
            <thead><tr><th scope="col">Item</th><th scope="col">Value</th></tr></thead>
            <tbody>{flattenMetrics(m.calibration).map((r) => <tr key={r.key}><th scope="row">{r.key}</th><td>{r.value}</td></tr>)}</tbody>
          </table>
        </>
      )}

      <h2>Trained on</h2>
      <ul>
        {m.trained_on_sources.map((s) => (
          <li key={s.source_id}>{s.name} ({s.version}) — {s.license_name}. {s.attribution_text}</li>
        ))}
      </ul>

      <h2>Description and limitations</h2>
      <div className="card" data-testid="card-markdown"><SimpleMarkdown text={m.card_markdown} /></div>

      <h2>Sources not used</h2>
      <p className="muted">Examined and deliberately neither served nor used to train this model.</p>
      {m.not_used_sources.length === 0 ? <p>None.</p> : (
        <ul data-testid="not-used-sources">
          {m.not_used_sources.map((x) => (
            <li key={x.source_id}><strong>{x.name}</strong>: {x.reason}</li>
          ))}
        </ul>
      )}

      <h2>Registered models</h2>
      <table className="data">
        <caption className="visually-hidden">Registered models and their status</caption>
        <thead><tr><th scope="col">Model</th><th scope="col">Role</th><th scope="col">Kind</th><th scope="col">Status</th><th scope="col">Default</th></tr></thead>
        <tbody>
          {models.data.items.map((x) => (
            <tr key={x.model_id}><th scope="row">{x.model_id}</th><td>{x.role}</td><td>{x.kind ?? ''}</td><td>{x.status}</td><td>{x.is_default ? 'yes' : 'no'}</td></tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
