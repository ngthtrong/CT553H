import { Fragment, useMemo, useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { scaleLinear } from 'd3-scale';
import { workspace } from '../api/client';
import { AMINO_ACIDS, type ModelComparison } from '../api/types';
import { diffColor } from '../lib/colors';
import { fmtProb, fmtScore } from '../lib/format';
import { Banner } from './ui';
import { DownloadButton } from './workspace';

const CELL = 18;
const LEFT = 44;
const HEAD = 20;

function fmtMetric(v: number | null | undefined, digits = 3): string {
  return v === null || v === undefined ? 'not defined' : v.toFixed(digits);
}

/** 28 × 20 grid of P_B − P_A on the BrBG scale; wild-type cells hatched; values in the cell titles and the table below. */
function DiffHeatmap({ c }: { c: ModelComparison }) {
  const by = useMemo(() => new Map(c.cells.map((x) => [`${x.position}${x.mut_aa}`, x])), [c.cells]);
  const limit = Math.max(0.01, ...c.cells.map((x) => Math.abs(x.prob_b - x.prob_a)));
  const seq = c.tile.sequence;
  const w = LEFT + 20 * CELL;
  const h = HEAD + seq.length * CELL;
  const stops = Array.from({ length: 11 }, (_, i) => diffColor(((i - 5) / 5) * limit, limit));
  return (
    <figure style={{ margin: 0 }} data-testid="model-diff-heatmap">
      <div className="colorbar" style={{ background: `linear-gradient(90deg, ${stops.join(', ')})` }} role="img"
        aria-label={`Colour bar from ${(-limit).toFixed(2)} (model A higher, brown) through 0 to ${limit.toFixed(2)} (model B higher, teal)`} />
      <div className="row muted" style={{ justifyContent: 'space-between', width: 260, gap: 0 }}>
        <span>{(-limit).toFixed(2)} A higher</span><span>0</span><span>{limit.toFixed(2)} B higher</span>
      </div>
      <div className="heatmap-scroll">
        <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} role="img" className="heatmap"
          aria-label="Difference of calibrated probability, model B minus model A, for each substitution; the table of largest disagreements lists the values.">
          <defs>
            <pattern id="mc-wt" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect width="6" height="6" style={{ fill: 'var(--bg)' }} />
              <line x1="0" y1="0" x2="0" y2="6" style={{ stroke: 'var(--text)', strokeWidth: 2 }} />
            </pattern>
          </defs>
          {AMINO_ACIDS.split('').map((aa, j) => <text key={aa} x={LEFT + j * CELL + CELL / 2} y={HEAD - 6} textAnchor="middle" className="chart-tick">{aa}</text>)}
          {seq.split('').map((wt, i) => (
            <g key={i}>
              <text x={2} y={HEAD + i * CELL + CELL - 5} className="chart-tick">{i + 1} {wt}</text>
              {AMINO_ACIDS.split('').map((aa, j) => {
                const x = by.get(`${i + 1}${aa}`);
                return (
                  <rect key={aa} x={LEFT + j * CELL} y={HEAD + i * CELL} width={CELL} height={CELL} className="cell"
                    style={{ fill: aa === wt || !x ? 'url(#mc-wt)' : diffColor(x.prob_b - x.prob_a, limit) }}>
                    <title>{x ? `${i + 1} ${wt}→${aa}: A ${fmtProb(x.prob_a)}, B ${fmtProb(x.prob_b)}, B − A ${(x.prob_b - x.prob_a).toFixed(3)}` : `${i + 1} ${wt}: wild type`}</title>
                  </rect>
                );
              })}
            </g>
          ))}
        </svg>
      </div>
      <figcaption className="muted">P(ΔPSI ≥ 1) of model B minus model A. Hatched = wild type.</figcaption>
    </figure>
  );
}

function Scatter({ c, mode }: { c: ModelComparison; mode: 'prob' | 'raw' }) {
  const W = 320, H = 260, M = { l: 52, r: 10, t: 10, b: 38 };
  const xs = c.cells.map((x) => (mode === 'prob' ? x.prob_a : x.raw_a));
  const ys = c.cells.map((x) => (mode === 'prob' ? x.prob_b : x.raw_b));
  const lo = Math.min(...xs, ...ys), hi = Math.max(...xs, ...ys);
  const sx = scaleLinear().domain(mode === 'prob' ? [0, 1] : [lo, hi]).range([M.l, W - M.r]).nice();
  const sy = scaleLinear().domain(sx.domain() as [number, number]).range([H - M.b, M.t]);
  const [d0, d1] = sx.domain() as [number, number];
  const fx = sx.tickFormat(5);
  return (
    <figure className="chart" data-testid="model-scatter">
      <svg viewBox={`0 0 ${W} ${H}`} className="chart__svg" role="img" aria-label={`${c.cells.length} substitutions, model A (x) against model B (y), ${mode === 'prob' ? 'calibrated probability' : 'raw score'}; dashed line is equality.`}>
        <line x1={M.l} x2={W - M.r} y1={H - M.b} y2={H - M.b} className="chart-axis" />
        <line x1={M.l} x2={M.l} y1={M.t} y2={H - M.b} className="chart-axis" />
        {sx.ticks(5).map((t) => <text key={`x${t}`} x={sx(t)} y={H - M.b + 14} textAnchor="middle" className="chart-tick">{fx(t)}</text>)}
        {sx.ticks(5).map((t) => <text key={`y${t}`} x={M.l - 6} y={sy(t) + 4} textAnchor="end" className="chart-tick">{fx(t)}</text>)}
        <line x1={sx(d0)} y1={sy(d0)} x2={sx(d1)} y2={sy(d1)} className="chart-ref" />
        {c.cells.map((x, i) => <circle key={`${x.position}${x.mut_aa}`} cx={sx(xs[i]!)} cy={sy(ys[i]!)} r={2.2} className="chart-point" />)}
        <text x={(M.l + W - M.r) / 2} y={H - 6} textAnchor="middle" className="chart-label">model A</text>
        <text x={12} y={(M.t + H - M.b) / 2} textAnchor="middle" transform={`rotate(-90 12 ${(M.t + H - M.b) / 2})`} className="chart-label">model B</text>
      </svg>
      <figcaption><strong>A against B.</strong> n = {c.cells.length}; {mode === 'prob' ? 'calibrated probability' : 'raw score'}; dashed line y = x.</figcaption>
    </figure>
  );
}

function Side({ tag, s }: { tag: string; s: ModelComparison['provenance']['a'] }): ReactNode {
  return (
    <div className="panel" data-testid={`model-side-${tag}`}>
      <h3 style={{ marginTop: 0 }}>Model {tag.toUpperCase()}: <code>{s.model_id}</code></h3>
      <dl className="kv">
        <dt>Analysis</dt><dd><Link to={`/analyses/${s.analysis_id}`}>{s.analysis_id.slice(0, 8)}</Link></dd>
        <dt>Evidence</dt><dd>{s.evidence_label}</dd>
        <dt>Domain</dt><dd><code>{s.domain_status}</code></dd>
        <dt>Warnings</dt><dd>{s.warning_codes.length ? s.warning_codes.join(', ') : 'none'}</dd>
        <dt>Weights SHA-256</dt><dd className="mono">{s.weights_sha256.slice(0, 16)}…</dd>
      </dl>
    </div>
  );
}

/** plan-system 2.2: two analyses of one tile side by side; descriptive only (label first, R-1). */
export function ModelComparisonView({ c }: { c: ModelComparison }) {
  const [mode, setMode] = useState<'prob' | 'raw'>('prob');
  const m = c.metrics;
  return (
    <div className="stack" data-testid="model-comparison">
      <Banner tone="info" title="Descriptive comparison" testId="model-comparison-label">{c.label}</Banner>
      <div className="chart-grid">
        <Side tag="a" s={c.provenance.a} />
        <Side tag="b" s={c.provenance.b} />
      </div>
      <section aria-labelledby="mc-metrics-h">
        <h2 id="mc-metrics-h">Agreement</h2>
        <dl className="kv panel" data-testid="model-comparison-metrics">
          <dt>Substitutions compared</dt><dd className="num">{m.n_cells}</dd>
          <dt>Spearman ρ, raw scores</dt><dd className="num">{fmtMetric(m.spearman_raw)}</dd>
          <dt>Pearson r, raw scores</dt><dd className="num">{fmtMetric(m.pearson_raw)}</dd>
          <dt>Spearman ρ, probabilities</dt><dd className="num">{fmtMetric(m.spearman_prob)}</dd>
          <dt>Mean |B − A|, raw score</dt><dd className="num">{fmtMetric(m.mean_abs_diff_raw)}</dd>
          <dt>Mean |B − A|, probability</dt><dd className="num">{fmtMetric(m.mean_abs_diff_prob)}</dd>
          <dt>Top 10 % shared (k = {m.top_k})</dt><dd className="num">{m.top_k_overlap} · Jaccard {fmtMetric(m.top_k_jaccard)}</dd>
        </dl>
        <p className="muted">Raw scores of different models need not share a scale, so their agreement is read by rank; the probability is on a common scale (same event, same assay).</p>
      </section>
      <section aria-labelledby="mc-figs-h">
        <h2 id="mc-figs-h">Where they differ</h2>
        <fieldset className="row" style={{ border: 0, padding: 0, margin: 0 }}>
          <legend className="visually-hidden">Quantity in the scatter</legend>
          <label><input type="radio" name="mc-mode" checked={mode === 'prob'} onChange={() => setMode('prob')} /> Probability</label>
          <label><input type="radio" name="mc-mode" checked={mode === 'raw'} onChange={() => setMode('raw')} /> Raw score</label>
        </fieldset>
        <div className="figs-row">
          <Scatter c={c} mode={mode} />
          <DiffHeatmap c={c} />
        </div>
      </section>
      <section aria-labelledby="mc-dis-h">
        <h2 id="mc-dis-h">Largest disagreements</h2>
        <div className="ui-table__scroll">
          <table className="data" data-testid="model-disagreements">
            <caption className="visually-hidden">Substitutions with the largest difference of probability between the two models</caption>
            <thead><tr><th scope="col">Substitution</th><th scope="col" className="num">P model A</th><th scope="col" className="num">P model B</th><th scope="col" className="num">B − A</th><th scope="col" className="num">Raw A</th><th scope="col" className="num">Raw B</th><th scope="col" className="num">Rank A</th><th scope="col" className="num">Rank B</th></tr></thead>
            <tbody>
              {c.disagreements.map((x) => (
                <Fragment key={`${x.position}${x.mut_aa}`}>
                  <tr>
                    <td className="mono">{x.wt_aa}{x.position}{x.mut_aa}</td>
                    <td className="num">{fmtProb(x.prob_a)}</td><td className="num">{fmtProb(x.prob_b)}</td>
                    <td className="num">{(x.prob_b - x.prob_a).toFixed(3)}</td>
                    <td className="num">{fmtScore(x.raw_a)}</td><td className="num">{fmtScore(x.raw_b)}</td>
                    <td className="num">{x.rank_a}</td><td className="num">{x.rank_b}</td>
                  </tr>
                </Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      {c.comparison_id && (
        <div className="row">
          <DownloadButton label="Export comparison CSV" fileName={`degron-footprint_model-comparison-${c.comparison_id.slice(0, 8)}.csv`} fetchBlob={() => workspace.exportModelComparison(c.comparison_id!, 'csv')} />
          <DownloadButton label="Export JSON" fileName={`degron-footprint_model-comparison-${c.comparison_id.slice(0, 8)}.json`} fetchBlob={() => workspace.exportModelComparison(c.comparison_id!, 'json')} />
        </div>
      )}
    </div>
  );
}
