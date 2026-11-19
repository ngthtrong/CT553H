import { useQuery } from '@tanstack/react-query';
import { scaleLinear } from 'd3-scale';
import { Link } from 'react-router-dom';
import { workspace } from '../api/client';
import type { AgreementSeries } from '../api/types';
import { fmtDateTime } from '../lib/format';
import { ErrorBanner } from './ErrorBanner';
import { Banner, EmptyState, Skeleton } from './ui';

type Point = AgreementSeries['points'][number];
const W = 520, H = 180, M = { l: 52, r: 12, t: 12, b: 30 };

function Trend({ points, metric, label }: { points: Point[]; metric: 'mae' | 'spearman'; label: string }) {
  const pts = points.map((p, i) => ({ i, v: p[metric], p })).filter((x) => x.v !== null) as { i: number; v: number; p: Point }[];
  if (pts.length === 0) return null;
  const x = scaleLinear().domain([0, Math.max(1, points.length - 1)]).range([M.l, W - M.r]);
  const lo = Math.min(...pts.map((d) => d.v)), hi = Math.max(...pts.map((d) => d.v));
  const y = scaleLinear().domain(metric === 'spearman' ? [-1, 1] : [0, Math.max(hi * 1.15, lo + 0.05)]).range([H - M.b, M.t]).nice();
  const fy = y.tickFormat(5);
  return (
    <figure className="chart" data-testid={`agreement-${metric}`}>
      <svg viewBox={`0 0 ${W} ${H}`} className="chart__svg" role="img" aria-label={`${label} of ${pts.length} comparisons in time order; flagged points are marked with a ring; the table lists the values.`}>
        <line x1={M.l} x2={W - M.r} y1={H - M.b} y2={H - M.b} className="chart-axis" />
        <line x1={M.l} x2={M.l} y1={M.t} y2={H - M.b} className="chart-axis" />
        {y.ticks(4).map((t) => <text key={t} x={M.l - 6} y={y(t) + 4} textAnchor="end" className="chart-tick">{fy(t)}</text>)}
        {points.map((p, i) => <text key={p.comparison_id} x={x(i)} y={H - M.b + 14} textAnchor="middle" className="chart-tick">{i + 1}</text>)}
        {pts.length > 1 && <polyline points={pts.map((d) => `${x(d.i)},${y(d.v)}`).join(' ')} className="chart-line" />}
        {pts.map((d) => (
          <g key={d.p.comparison_id}>
            <circle cx={x(d.i)} cy={y(d.v)} r={4} className="chart-point" />
            {d.p.flags.length > 0 && <circle cx={x(d.i)} cy={y(d.v)} r={8} className="chart-flag" />}
            <text x={x(d.i) + 6} y={y(d.v) - 6} className="chart-tick">n={d.p.n}</text>
          </g>
        ))}
        <text x={12} y={(M.t + H - M.b) / 2} textAnchor="middle" transform={`rotate(-90 12 ${(M.t + H - M.b) / 2})`} className="chart-label">{label}</text>
      </svg>
      <figcaption><strong>{label}</strong> per saved comparison, numbered in time order (table below). Ring = flagged.</figcaption>
    </figure>
  );
}

/** plan-system 4.4: agreement with imported measurements over time; warnings only, never an automatic action. */
export function AgreementPanel({ projectId }: { projectId: string }) {
  const q = useQuery({ queryKey: ['agreement', projectId], queryFn: ({ signal }) => workspace.getAgreement(projectId, signal), retry: false });
  if (q.isPending) return <Skeleton />;
  if (q.isError) return <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />;
  const s = q.data;
  const shown = s.points.filter((p) => p.compatible);
  return (
    <div className="stack" data-testid="agreement-panel">
      <Banner tone="info" title="Comparison only, not an independent validation">Each point is a saved comparison of an analysis with imported measurements. {s.caveat}</Banner>
      {shown.length === 0 ? (
        <EmptyState title="No comparable comparison yet">Compare a saved analysis with a committed dataset whose endpoint is GPS ΔPSI (Comparison tab of an analysis).</EmptyState>
      ) : (
        <>
          {s.flagged > 0 && <Banner tone="warn" title={`${s.flagged} comparison${s.flagged > 1 ? 's' : ''} clearly worse than earlier ones`} testId="agreement-flags">{s.caveat}</Banner>}
          <div className="figs-row">
            <Trend points={shown} metric="mae" label="MAE" />
            <Trend points={shown} metric="spearman" label="Spearman ρ" />
          </div>
          <div className="ui-table__scroll">
            <table className="data" data-testid="agreement-table">
              <caption className="visually-hidden">Saved comparisons in time order</caption>
              <thead><tr><th scope="col" className="num">#</th><th scope="col">Date</th><th scope="col">Dataset</th><th scope="col">Model · tile</th><th scope="col" className="num">n</th><th scope="col" className="num">MAE</th><th scope="col" className="num">Spearman</th><th scope="col">Flag</th></tr></thead>
              <tbody>
                {shown.map((p, i) => (
                  <tr key={p.comparison_id}>
                    <td className="num">{i + 1}</td><td>{fmtDateTime(p.created_at)}</td>
                    <td>{p.dataset_name ?? p.dataset_id.slice(0, 8)}{p.dataset_revision ? ` r${p.dataset_revision}` : ''}</td>
                    <td><Link to={`/analyses/${p.analysis_id}`}>{p.model_id} · {p.tile}</Link></td>
                    <td className="num">{p.n}</td><td className="num">{p.mae === null ? '—' : p.mae.toFixed(3)}</td>
                    <td className="num">{p.spearman === null ? '—' : p.spearman.toFixed(3)}</td>
                    <td>{p.flags.length ? p.flags.map((f) => f.text).join(' ') : '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="muted">Flag rule: n ≥ {String(s.rules.min_n)} and at least {String(s.rules.min_earlier)} earlier points; MAE above {String(s.rules.mae_ratio)} × their mean, or Spearman more than {String(s.rules.spearman_drop)} below their mean. Nothing changes the model.</p>
        </>
      )}
    </div>
  );
}
