import type { Cell } from '../api/types';

/** A comparison row as the API stores it (rows of `Comparison`). */
export interface ComparisonRow {
  position: number;
  wt_aa: string;
  mut_aa: string;
  observed: number;
  n_replicates: number;
  units: string;
  predicted_dpsi_raw: number | null;
  residual: number | null;
}

export interface Pair {
  key: string;
  predicted: number;
  observed: number;
  residual: number;
  /** Calibrated P(ΔPSI ≥ 1) of the same substitution in the saved analysis; null if the cell is missing. */
  prob: number | null;
}

/**
 * Pairs to draw (plan-system 2.3, FR-30): only matched rows with a predicted value, i.e. rows of a dataset whose
 * endpoint is declared comparable with GPS ΔPSI. Nothing is drawn for other endpoints.
 */
export function matchedPairs(rows: ComparisonRow[], cells: Cell[]): Pair[] {
  const prob = new Map(cells.map((c) => [`${c.position}${c.mut_aa}`, c.p_dpsi_ge_1_calibrated]));
  return rows
    .filter((r) => r.predicted_dpsi_raw !== null && r.residual !== null && Number.isFinite(r.observed))
    .map((r) => {
      const key = `${r.position}${r.mut_aa}`;
      return { key, predicted: r.predicted_dpsi_raw as number, observed: r.observed, residual: r.residual as number, prob: prob.get(key) ?? null };
    });
}

export interface Bin {
  lo: number;
  hi: number;
  count: number;
}

/** Equal-width histogram over [min, max]; the last bin includes its upper edge. */
export function histogram(values: number[], nBins = 12): Bin[] {
  if (values.length === 0) return [];
  const lo = Math.min(...values);
  const hi = Math.max(...values);
  const width = hi > lo ? (hi - lo) / nBins : 1;
  const bins: Bin[] = Array.from({ length: hi > lo ? nBins : 1 }, (_, i) => ({ lo: lo + i * width, hi: lo + (i + 1) * width, count: 0 }));
  for (const v of values) {
    const i = hi > lo ? Math.min(bins.length - 1, Math.floor((v - lo) / width)) : 0;
    bins[i]!.count += 1;
  }
  return bins;
}

export interface BlandAltman {
  n: number;
  meanDiff: number;
  /** Sample SD (n − 1) of predicted − observed; null below two pairs. */
  sd: number | null;
  upper: number | null;
  lower: number | null;
}

/** Bland–Altman summary of predicted raw ΔPSI − observed: bias and 95 % limits of agreement (± 1.96 SD). */
export function blandAltman(pairs: Pair[]): BlandAltman {
  const d = pairs.map((p) => p.predicted - p.observed);
  const n = d.length;
  const meanDiff = n ? d.reduce((a, b) => a + b, 0) / n : Number.NaN;
  if (n < 2) return { n, meanDiff, sd: null, upper: null, lower: null };
  const sd = Math.sqrt(d.reduce((a, b) => a + (b - meanDiff) ** 2, 0) / (n - 1));
  return { n, meanDiff, sd, upper: meanDiff + 1.96 * sd, lower: meanDiff - 1.96 * sd };
}

/** Observed event matching the model's event definition P(ΔPSI ≥ 1). */
export const EVENT_THRESHOLD = 1.0;

export interface CalibrationBin {
  lo: number;
  hi: number;
  n: number;
  meanProb: number;
  observedRate: number;
}

/**
 * Calibration by equal-width probability bins: mean predicted probability against the observed share of ΔPSI ≥ 1.
 * Only for a compatible endpoint; empty bins are left out (their n is 0).
 */
export function calibrationBins(pairs: Pair[], nBins = 5): CalibrationBin[] {
  const withProb = pairs.filter((p) => p.prob !== null) as (Pair & { prob: number })[];
  const out: CalibrationBin[] = [];
  for (let i = 0; i < nBins; i += 1) {
    const lo = i / nBins;
    const hi = (i + 1) / nBins;
    const inBin = withProb.filter((p) => p.prob >= lo && (i === nBins - 1 ? p.prob <= hi : p.prob < hi));
    if (inBin.length === 0) continue;
    out.push({
      lo, hi, n: inBin.length,
      meanProb: inBin.reduce((a, p) => a + p.prob, 0) / inBin.length,
      observedRate: inBin.filter((p) => p.observed >= EVENT_THRESHOLD).length / inBin.length,
    });
  }
  return out;
}
