import type { Cell } from '../api/types';
import { footprint } from '../lib/footprint';
import type { ScaleMode } from './ScaleToggle';

const ROW = 28;      // same row height and header offset as Heatmap, so the positions line up
const HEAD = 28;
const BAR = 120;

/** FootprintTrack (9.5b): mean effect per position beside the matrix, sharing its position axis; a table for AT. */
export function FootprintTrack({ cells, sequence, mode, eventDefinition }: { cells: Cell[]; sequence: string; mode: ScaleMode; eventDefinition: string }) {
  const rows = footprint(cells, sequence, mode);
  const lo = mode === 'prob' ? 0 : Math.min(0, ...rows.map((r) => r.mean));
  const hi = mode === 'prob' ? 1 : Math.max(0, ...rows.map((r) => r.mean));
  const span = hi - lo || 1;
  const x0 = ((0 - lo) / span) * BAR;
  const label = mode === 'prob' ? `mean ${eventDefinition}` : mode === 'spread' ? 'mean seed spread (SD of 3 seeds, not an error bar)' : 'mean raw ΔPSI score';
  return (
    <figure className="footprint" data-testid="footprint-track" style={{ margin: 0 }}>
      <svg width={BAR + 64} height={HEAD + rows.length * ROW} role="img" aria-label={`Footprint: ${label} at each of the ${rows.length} positions`}>
        <text x={0} y={18} className="footprint-head">Footprint</text>
        <line x1={x0} x2={x0} y1={HEAD} y2={HEAD + rows.length * ROW} className="footprint-axis" />
        {rows.map((r, i) => {
          const w = ((r.mean - lo) / span) * BAR;
          const x = Math.min(w, x0);
          return (
            <g key={r.position}>
              <rect x={x} y={HEAD + i * ROW + 6} width={Math.abs(w - x0)} height={ROW - 12} className="footprint-bar" />
              <text x={BAR + 6} y={HEAD + i * ROW + 18} className="footprint-value">{r.mean.toFixed(2)}</text>
            </g>
          );
        })}
      </svg>
      <figcaption className="muted">{label[0]!.toUpperCase() + label.slice(1)} over the 19 substitutions of each position.</figcaption>
      {/* a table ignores width/overflow, so the hiding wrapper must be a block */}
      <div className="visually-hidden">
      <table>
        <caption>Footprint per position: {label}</caption>
        <thead><tr><th scope="col">Position</th><th scope="col">Wild type</th><th scope="col">Mean of 19 substitutions</th><th scope="col">Top 10 % substitutions</th></tr></thead>
        <tbody>{rows.map((r) => <tr key={r.position}><td>{r.position}</td><td>{r.wt}</td><td>{r.mean.toFixed(3)}</td><td>{r.top10}</td></tr>)}</tbody>
      </table>
      </div>
    </figure>
  );
}
