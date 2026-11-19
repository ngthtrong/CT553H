/** plan-system 2.3 — charts of the comparison with imported data (CMP-04, CMP-05). */
import { render, screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import type { Cell } from '../src/api/types';
import { ComparisonCharts } from '../src/components/ComparisonCharts';
import { blandAltman, calibrationBins, histogram, matchedPairs, type ComparisonRow } from '../src/lib/comparisonCharts';

const cell = (position: number, mut: string, s: number, p: number): Cell => ({
  position, wt_aa: 'D', mut_aa: mut, score_dpsi_raw: s, p_dpsi_ge_1_calibrated: p, rank_in_tile: 1, top10pct_in_tile: false,
});
const cells: Cell[] = [cell(1, 'A', 0.5, 0.1), cell(2, 'A', 1.5, 0.9), cell(3, 'A', -0.2, 0.05), cell(4, 'A', 1.1, 0.75)];
const row = (position: number, observed: number, predicted: number | null): ComparisonRow => ({
  position, wt_aa: 'D', mut_aa: 'A', observed, n_replicates: 1, units: 'PSI', predicted_dpsi_raw: predicted, residual: predicted === null ? null : predicted - observed,
});
const rows = [row(1, 0.6, 0.5), row(2, 1.2, 1.5), row(3, 0.0, -0.2), row(4, 0.4, 1.1)];

describe('lib/comparisonCharts', () => {
  it('pairs only rows with a predicted value and attaches the calibrated probability of the same cell', () => {
    const p = matchedPairs([...rows, row(5, 0.3, null)], cells);
    expect(p.map((x) => x.key)).toEqual(['1A', '2A', '3A', '4A']);
    expect(p[1]).toMatchObject({ predicted: 1.5, observed: 1.2, prob: 0.9 });
    expect(Math.abs(p[1]!.residual - 0.3)).toBeLessThan(1e-12);
  });
  it('histogram counts every residual once; Bland–Altman uses the sample SD', () => {
    const p = matchedPairs(rows, cells);
    expect(histogram(p.map((x) => x.residual), 4).reduce((a, b) => a + b.count, 0)).toBe(4);
    const ba = blandAltman(p);
    const d = [-0.1, 0.3, -0.2, 0.7];
    const m = d.reduce((a, b) => a + b, 0) / 4;
    const sd = Math.sqrt(d.reduce((a, b) => a + (b - m) ** 2, 0) / 3);
    expect(ba.meanDiff).toBeCloseTo(m, 12);
    expect(ba.sd).toBeCloseTo(sd, 12);
    expect(ba.upper).toBeCloseTo(m + 1.96 * sd, 12);
    expect(blandAltman(p.slice(0, 1)).sd).toBeNull();
  });
  it('calibration bins: mean probability against the observed share of ΔPSI ≥ 1, empty bins left out', () => {
    const bins = calibrationBins(matchedPairs(rows, cells), 5);
    expect(bins.map((b) => [b.lo, b.n])).toEqual([[0, 2], [3 / 5, 1], [4 / 5, 1]]);
    expect(bins[0]).toMatchObject({ observedRate: 0 });
    expect(bins.at(-1)).toMatchObject({ meanProb: 0.9, observedRate: 1 });
  });
});

describe('ComparisonCharts', () => {
  it('CMP-04: the scatter points are exactly the matched pairs, each chart states n', () => {
    render(<ComparisonCharts rows={rows} cells={cells} compatible units="PSI" />);
    const scatter = screen.getByTestId('chart-scatter');
    const pts = scatter.querySelectorAll('circle');
    expect([...pts].map((c) => [c.getAttribute('data-key'), Number(c.getAttribute('data-x')), Number(c.getAttribute('data-y'))]))
      .toEqual(rows.map((r) => [`${r.position}A`, r.predicted_dpsi_raw, r.observed]));
    for (const id of ['chart-scatter', 'chart-residuals', 'chart-bland-altman']) expect(screen.getByTestId(id)).toHaveTextContent('n = 4');
    expect(screen.getByTestId('chart-calibration')).toHaveTextContent('n = 4');
    expect(within(screen.getByTestId('chart-calibration')).getAllByTestId('calibration-bin')).toHaveLength(3);
  });
  it('CMP-05: an endpoint that is not comparable draws nothing and says why', () => {
    render(<ComparisonCharts rows={rows.map((r) => ({ ...r, predicted_dpsi_raw: null, residual: null }))} cells={cells} compatible={false} units="a.u." />);
    expect(screen.getByTestId('comparison-charts-unavailable')).toHaveTextContent('not declared comparable with GPS ΔPSI');
    expect(screen.queryByTestId('chart-calibration')).toBeNull();
    expect(screen.queryByTestId('chart-scatter')).toBeNull();
  });
});

describe('chart axes', () => {
  it('a narrow residual range never repeats a tick label', () => {
    const narrow = rows.map((r, i) => ({ ...r, observed: r.predicted_dpsi_raw! + 0.05 + i * 0.001, residual: -0.05 - i * 0.001 }));
    render(<ComparisonCharts rows={narrow} cells={cells} compatible units="PSI" />);
    const ticks = [...screen.getByTestId('chart-residuals').querySelectorAll('[data-tick]')].map((g) => g.getAttribute('data-tick'));
    expect(ticks.length).toBeGreaterThan(1);
    expect(new Set(ticks).size).toBe(ticks.length);
  });
});
