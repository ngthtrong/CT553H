import { useState } from 'react';
import type { Cell } from '../api/types';
import { fmtProb, fmtScore } from '../lib/format';

/**
 * Top-k prioritisation of one tile (plan.md 2.11). The evidence label comes before any number in the DOM: the ranking
 * is a retrospective development benchmark within this tile, not a validated or cross-tile prioritisation.
 */
export function PriorityPanel({ cells, eventDefinition }: { cells: Cell[]; eventDefinition: string }) {
  const [k, setK] = useState(10);
  const top = [...cells].sort((a, b) => a.rank_in_tile - b.rank_in_tile).slice(0, k);
  return (
    <section className="panel" aria-labelledby="priority-h" data-testid="priority-panel">
      <h2 id="priority-h" style={{ marginTop: 0 }}>Top {k} substitutions to test first</h2>
      <p className="ui-banner ui-banner--warn" data-testid="priority-label" style={{ margin: '0 0 var(--space-3)' }}>
        Retrospective, development benchmark: ranked within this tile by {eventDefinition}. Not a validated
        prioritisation and not comparable across tiles or proteins.
      </p>
      <label>
        Show{' '}
        <select value={k} onChange={(e) => setK(Number(e.target.value))} aria-label="Number of substitutions">
          {[5, 10, 20].map((n) => <option key={n} value={n}>{n}</option>)}
        </select>
      </label>
      <ol className="priority-list">
        {top.map((c) => (
          <li key={`${c.position}${c.mut_aa}`}>
            <span className="mono">{c.wt_aa}{c.position}{c.mut_aa}</span>
            <span className="num">{eventDefinition} = {fmtProb(c.p_dpsi_ge_1_calibrated)}</span>
            <span className="num muted">raw {fmtScore(c.score_dpsi_raw)}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}
