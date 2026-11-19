import type { Cell } from '../api/types';
import type { ScaleMode } from '../components/ScaleToggle';

export interface FootprintRow {
  position: number;
  wt: string;
  /** Mean over the 19 substitutions of the position, in the scale of the matrix (probability or raw ΔPSI). */
  mean: number;
  max: number;
  /** Substitutions of this position in the top 10 % of the tile. */
  top10: number;
}

/**
 * Footprint track (9.5b, proposed addition to ui-design): one summary per position, recomputed from the same 532 cells
 * the matrix shows, never from another source. Ranking stays per tile.
 */
/** The quantity of a cell in a view; the seed spread is 0 when absent (the view is hidden then). */
export function cellValue(c: Cell, mode: ScaleMode): number {
  if (mode === 'prob') return c.p_dpsi_ge_1_calibrated;
  if (mode === 'spread') return c.score_seed_sd ?? 0;
  return c.score_dpsi_raw;
}

/** True when every cell has the seed spread of an ensemble (LoRA-D); older snapshots and the npz model have none. */
export function hasSeedSpread(cells: Cell[]): boolean {
  return cells.length > 0 && cells.every((c) => typeof c.score_seed_sd === 'number' && typeof c.score_seed_min === 'number' && typeof c.score_seed_max === 'number');
}

export function footprint(cells: Cell[], sequence: string, mode: ScaleMode): FootprintRow[] {
  const rows: FootprintRow[] = [];
  for (let pos = 1; pos <= sequence.length; pos += 1) {
    const at = cells.filter((c) => c.position === pos);
    const values = at.map((c) => cellValue(c, mode));
    rows.push({
      position: pos,
      wt: sequence.charAt(pos - 1),
      mean: values.length ? values.reduce((s, v) => s + v, 0) / values.length : Number.NaN,
      max: values.length ? Math.max(...values) : Number.NaN,
      top10: at.filter((c) => c.top10pct_in_tile).length,
    });
  }
  return rows;
}
