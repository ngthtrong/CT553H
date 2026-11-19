import type { ReactNode } from 'react';
import { scaleLinear } from 'd3-scale';
import type { Cell } from '../api/types';
import { blandAltman, calibrationBins, EVENT_THRESHOLD, histogram, matchedPairs, type ComparisonRow } from '../lib/comparisonCharts';
import { Banner } from './ui';

const W = 320;
const H = 230;
const M = { l: 58, r: 12, t: 10, b: 36 };
const IW = W - M.l - M.r;
const IH = H - M.t - M.b;

function extent(values: number[], pad = 0.05): [number, number] {
  const lo = Math.min(...values);
  const hi = Math.max(...values);
  const span = hi - lo || 1;
  return [lo - span * pad, hi + span * pad];
}

function Axes({ x, y, xLabel, yLabel }: { x: ReturnType<typeof scaleLinear<number>>; y: ReturnType<typeof scaleLinear<number>>; xLabel: string; yLabel: string }) {
  // d3 picks the precision from the tick step, so a narrow range never prints the same label twice
  const fx = x.tickFormat(5);
  const fy = y.tickFormat(5);
  return (
    <g className="chart-axes" aria-hidden="true">
      <line x1={M.l} x2={M.l + IW} y1={M.t + IH} y2={M.t + IH} className="chart-axis" />
      <line x1={M.l} x2={M.l} y1={M.t} y2={M.t + IH} className="chart-axis" />
      {x.ticks(5).map((t) => (
        <g key={`x${t}`} data-tick={fx(t)}>
          <line x1={x(t)} x2={x(t)} y1={M.t + IH} y2={M.t + IH + 4} className="chart-axis" />
          <text x={x(t)} y={M.t + IH + 15} textAnchor="middle" className="chart-tick">{fx(t)}</text>
        </g>
      ))}
      {y.ticks(5).map((t) => (
        <g key={`y${t}`}>
          <line x1={M.l - 4} x2={M.l} y1={y(t)} y2={y(t)} className="chart-axis" />
          <text x={M.l - 6} y={y(t) + 4} textAnchor="end" className="chart-tick">{fy(t)}</text>
        </g>
      ))}
      <text x={M.l + IW / 2} y={H - 4} textAnchor="middle" className="chart-label">{xLabel}</text>
      <text x={11} y={M.t + IH / 2} textAnchor="middle" transform={`rotate(-90 11 ${M.t + IH / 2})`} className="chart-label">{yLabel}</text>
    </g>
  );
}

function Chart({ title, testId, summary, caption, children }: { title: string; testId: string; summary: string; caption: ReactNode; children: ReactNode }) {
  return (
    <figure className="chart" data-testid={testId}>
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${title}. ${summary}`} className="chart__svg">{children}</svg>
      <figcaption><strong>{title}.</strong> {caption}</figcaption>
    </figure>
  );
}

/**
 * Charts for the comparison with imported data (plan-system 2.3): only matched pairs of a compatible endpoint (FR-30),
 * always with n, after the "not an independent validation" label. SVG with d3-scale; no chart library.
 */
export function ComparisonCharts({ rows, cells, compatible, units }: { rows: ComparisonRow[]; cells: Cell[]; compatible: boolean; units: string }) {
  if (!compatible) {
    return (
      <Banner tone="info" title="No charts for this dataset" testId="comparison-charts-unavailable">
        Its endpoint is not declared comparable with GPS ΔPSI, so predicted and observed values are not plotted together and no
        calibration is drawn (FR-30). The observations are listed below in their own units.
      </Banner>
    );
  }
  const pairs = matchedPairs(rows, cells);
  const n = pairs.length;
  if (n === 0) return <p className="muted" data-testid="comparison-charts-unavailable">No matched substitution to plot.</p>;

  const all = [...pairs.map((p) => p.predicted), ...pairs.map((p) => p.observed)];
  const [lo, hi] = extent(all);
  const xs = scaleLinear().domain([lo, hi]).range([M.l, M.l + IW]).nice();
  const ys = scaleLinear().domain([lo, hi]).range([M.t + IH, M.t]).nice();
  const [d0, d1] = xs.domain() as [number, number];

  const hist = histogram(pairs.map((p) => p.residual));
  const hx = scaleLinear().domain([hist[0]!.lo, hist[hist.length - 1]!.hi]).range([M.l, M.l + IW]).nice();
  const hy = scaleLinear().domain([0, Math.max(...hist.map((b) => b.count))]).range([M.t + IH, M.t]).nice();

  const ba = blandAltman(pairs);
  const means = pairs.map((p) => (p.predicted + p.observed) / 2);
  const diffs = pairs.map((p) => p.predicted - p.observed);
  const bx = scaleLinear().domain(extent(means)).range([M.l, M.l + IW]).nice();
  const by = scaleLinear().domain(extent([...diffs, ba.upper ?? 0, ba.lower ?? 0, 0])).range([M.t + IH, M.t]).nice();

  const cal = calibrationBins(pairs);
  const nCal = cal.reduce((a, b) => a + b.n, 0);
  const cx = scaleLinear().domain([0, 1]).range([M.l, M.l + IW]);
  const cy = scaleLinear().domain([0, 1]).range([M.t + IH, M.t]);

  return (
    <div className="stack" data-testid="comparison-charts">
      <div className="chart-grid">
        <Chart title="Predicted against observed" testId="chart-scatter" summary={`${n} matched substitutions; dashed line is equality.`}
          caption={<>n = {n}. Predicted raw ΔPSI score (x) against the observed value in {units} (y); the dashed line is y = x.</>}>
          <Axes x={xs} y={ys} xLabel="predicted raw ΔPSI" yLabel={`observed (${units})`} />
          <line x1={xs(d0)} y1={ys(d0)} x2={xs(d1)} y2={ys(d1)} className="chart-ref" />
          {pairs.map((p) => <circle key={p.key} cx={xs(p.predicted)} cy={ys(p.observed)} r={3} className="chart-point" data-key={p.key} data-x={p.predicted} data-y={p.observed} />)}
        </Chart>

        <Chart title="Residuals" testId="chart-residuals" summary={`Histogram of ${n} residuals, predicted minus observed.`}
          caption={<>n = {n}. Predicted raw ΔPSI − observed, {hist.length} equal-width bins.</>}>
          <Axes x={hx} y={hy} xLabel="residual (predicted − observed)" yLabel="count" />
          {hist.map((b) => (
            <rect key={b.lo} x={hx(b.lo) + 0.5} y={hy(b.count)} width={Math.max(0, hx(b.hi) - hx(b.lo) - 1)} height={M.t + IH - hy(b.count)} className="chart-bar" data-count={b.count} />
          ))}
        </Chart>

        <Chart title="Bland–Altman" testId="chart-bland-altman"
          summary={ba.sd === null ? `${n} pair; limits need two pairs.` : `Bias ${ba.meanDiff.toFixed(3)}, limits ${ba.lower!.toFixed(3)} to ${ba.upper!.toFixed(3)}.`}
          caption={<>n = {n}. Mean of the two values (x) against their difference (y); solid line bias {ba.meanDiff.toFixed(3)}{ba.sd !== null ? <>, dashed lines 95 % limits of agreement {ba.lower!.toFixed(3)} to {ba.upper!.toFixed(3)} (± 1.96 SD)</> : ' (limits need at least two pairs)'}.</>}>
          <Axes x={bx} y={by} xLabel="mean of predicted and observed" yLabel="predicted − observed" />
          <line x1={M.l} x2={M.l + IW} y1={by(ba.meanDiff)} y2={by(ba.meanDiff)} className="chart-bias" />
          {ba.upper !== null && <line x1={M.l} x2={M.l + IW} y1={by(ba.upper)} y2={by(ba.upper)} className="chart-ref" />}
          {ba.lower !== null && <line x1={M.l} x2={M.l + IW} y1={by(ba.lower)} y2={by(ba.lower)} className="chart-ref" />}
          {pairs.map((p, i) => <circle key={p.key} cx={bx(means[i]!)} cy={by(diffs[i]!)} r={3} className="chart-point" />)}
        </Chart>

        <Chart title="Calibration" testId="chart-calibration"
          summary={`${cal.length} probability bins over ${nCal} substitutions; dashed diagonal is perfect calibration.`}
          caption={<>n = {nCal}. Mean calibrated P(ΔPSI ≥ {EVENT_THRESHOLD}) per bin (x) against the share of observed ΔPSI ≥ {EVENT_THRESHOLD} (y); point labels give n per bin. Few pairs make this curve unstable.</>}>
          <Axes x={cx} y={cy} xLabel={`predicted P(ΔPSI ≥ ${EVENT_THRESHOLD})`} yLabel={`observed share ΔPSI ≥ ${EVENT_THRESHOLD}`} />
          <line x1={cx(0)} y1={cy(0)} x2={cx(1)} y2={cy(1)} className="chart-ref" />
          {cal.length > 1 && <polyline points={cal.map((b) => `${cx(b.meanProb)},${cy(b.observedRate)}`).join(' ')} className="chart-line" />}
          {cal.map((b) => (
            <g key={b.lo} data-testid="calibration-bin" data-n={b.n}>
              <circle cx={cx(b.meanProb)} cy={cy(b.observedRate)} r={4} className="chart-point" />
              <text x={cx(b.meanProb) + 6} y={cy(b.observedRate) - 6} className="chart-tick">n={b.n}</text>
            </g>
          ))}
        </Chart>
      </div>
      <div className="visually-hidden">
        <table>
          <caption>Calibration bins</caption>
          <thead><tr><th scope="col">Probability bin</th><th scope="col">n</th><th scope="col">Mean predicted</th><th scope="col">Observed share</th></tr></thead>
          <tbody>{cal.map((b) => <tr key={b.lo}><td>{b.lo.toFixed(1)}–{b.hi.toFixed(1)}</td><td>{b.n}</td><td>{b.meanProb.toFixed(3)}</td><td>{b.observedRate.toFixed(3)}</td></tr>)}</tbody>
        </table>
      </div>
    </div>
  );
}
