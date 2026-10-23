import { AMINO_ACIDS } from '../api/types';
import type { Cell, TileInfo } from '../api/types';
import { fmtProb, fmtScore } from '../lib/format';
import type { ScaleMode } from './ScaleToggle';
import { cellKey } from './Heatmap';

/** The heatmap as a plain accessible table (ui-design §6 "table view"; default on narrow screens). */
export function MatrixTable({ cells, tile, mode, eventDefinition }: { cells: Cell[]; tile: TileInfo; mode: ScaleMode; eventDefinition: string }) {
  const by = new Map(cells.map((c) => [cellKey(c.position, c.mut_aa), c]));
  return (
    <div className="table-wrap" tabIndex={0} role="region" aria-label="Effect matrix as a table, scrollable">
      <table className="data" data-testid="matrix-table">
        <caption className="visually-hidden">
          {mode === 'prob' ? `Probability ${eventDefinition}` : 'Raw score'} for each substitution. Rows are positions, columns are the substituted amino acids.
        </caption>
        <thead>
          <tr>
            <th scope="col">Position</th>
            {AMINO_ACIDS.split('').map((a) => (
              <th key={a} scope="col" className="num">{a}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {tile.sequence.split('').map((wt, i) => (
            <tr key={i}>
              <th scope="row">{i + 1} {wt}</th>
              {AMINO_ACIDS.split('').map((a) => {
                const c = by.get(cellKey(i + 1, a));
                return (
                  <td key={a} className="num">
                    {a === wt || !c ? 'wt' : mode === 'prob' ? fmtProb(c.p_dpsi_ge_1_calibrated) : fmtScore(c.score_dpsi_raw)}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
