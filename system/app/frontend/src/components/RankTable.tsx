import { useEffect, useMemo, useRef, useState } from 'react';
import { AMINO_ACIDS, TILE_LENGTH } from '../api/types';
import type { Cell } from '../api/types';
import { fmtProb, fmtScore } from '../lib/format';
import { loadView, saveView } from '../lib/viewState';
import { cellKey } from './Heatmap';

export interface RankFilter {
  position: number | null;
  aa: string | null;
}

type SortKey = 'rank' | 'position' | 'wt' | 'mut' | 'raw' | 'prob';
interface Sort {
  key: SortKey;
  dir: 'asc' | 'desc';
}

interface Props {
  cells: Cell[];
  eventDefinition: string;
  filter: RankFilter;
  onFilter: (f: RankFilter) => void;
  selectedKey: string | null;
  onSelect: (c: Cell) => void;
  /** plan-system 5.2: remember sort and pinned substitutions under this id (never a sequence); null = not remembered */
  persistKey?: string | null;
}

const COLUMNS: { key: SortKey; label: (ev: string) => string; numeric: boolean }[] = [
  { key: 'rank', label: () => 'Rank', numeric: true },
  { key: 'position', label: () => 'Position', numeric: true },
  { key: 'wt', label: () => 'Wild type', numeric: false },
  { key: 'mut', label: () => 'Substituted', numeric: false },
  { key: 'raw', label: () => 'Raw score', numeric: true },
  { key: 'prob', label: (ev) => ev, numeric: true },
];

function compare(a: Cell, b: Cell, key: SortKey): number {
  switch (key) {
    case 'rank': return a.rank_in_tile - b.rank_in_tile;
    case 'position': return a.position - b.position || a.mut_aa.localeCompare(b.mut_aa);
    case 'wt': return a.wt_aa.localeCompare(b.wt_aa) || a.position - b.position;
    case 'mut': return a.mut_aa.localeCompare(b.mut_aa) || a.position - b.position;
    case 'raw': return a.score_dpsi_raw - b.score_dpsi_raw;
    case 'prob': return a.p_dpsi_ge_1_calibrated - b.p_dpsi_ge_1_calibrated;
  }
}

/**
 * All 532 substitutions, sortable and filterable (FR-07, FR-08). The table is not virtualised: 532 rows render
 * in one pass and keep native table semantics for screen readers (deviation from ui-design §3.3, see README).
 */
export function RankTable({ cells, eventDefinition, filter, onFilter, selectedKey, onSelect, persistKey = null }: Props) {
  const [sort, setSortState] = useState<Sort>(() => {
    const s = loadView(persistKey).sort;
    return s && COLUMNS.some((c) => c.key === s.key) ? (s as Sort) : { key: 'rank', dir: 'asc' };
  });
  const [pinned, setPinned] = useState<string[]>(() => loadView(persistKey).pinned ?? []);
  const setSort = (f: (s: Sort) => Sort) => setSortState((s) => { const next = f(s); saveView(persistKey, { sort: next }); return next; });
  const togglePin = (key: string) => setPinned((p) => {
    const next = p.includes(key) ? p.filter((k) => k !== key) : [...p, key];
    saveView(persistKey, { pinned: next });
    return next;
  });
  const byKey = useMemo(() => new Map(cells.map((c) => [cellKey(c.position, c.mut_aa), c])), [cells]);
  const pinnedCells = pinned.map((k) => byKey.get(k)).filter(Boolean) as Cell[];
  const selectedRow = useRef<HTMLTableRowElement | null>(null);

  const rows = useMemo(() => {
    const kept = cells.filter((c) => (filter.position === null || c.position === filter.position) && (filter.aa === null || c.mut_aa === filter.aa));
    const sign = sort.dir === 'asc' ? 1 : -1;
    return [...kept].sort((a, b) => sign * compare(a, b, sort.key));
  }, [cells, filter, sort]);

  useEffect(() => {
    selectedRow.current?.scrollIntoView?.({ block: 'nearest' });
  }, [selectedKey]);

  function toggle(key: SortKey) {
    setSort((s) => (s.key === key ? { key, dir: s.dir === 'asc' ? 'desc' : 'asc' } : { key, dir: key === 'prob' || key === 'raw' ? 'desc' : 'asc' }));
  }

  return (
    <section aria-labelledby="rank-heading">
      <h2 id="rank-heading">Ranking ({cells.length} substitutions)</h2>
      {pinnedCells.length > 0 && (
        <div className="panel" data-testid="pinned-list">
          <h3 style={{ marginTop: 0, fontSize: 'var(--text-md, 1rem)' }}>Pinned ({pinnedCells.length})</h3>
          <ul className="reasons">
            {pinnedCells.map((c) => (
              <li key={cellKey(c.position, c.mut_aa)}>
                <span className="mono">{c.wt_aa}{c.position}{c.mut_aa}</span> · rank {c.rank_in_tile} · raw {fmtScore(c.score_dpsi_raw)} · P {fmtProb(c.p_dpsi_ge_1_calibrated)}{' '}
                <button type="button" className="link" onClick={() => togglePin(cellKey(c.position, c.mut_aa))}>Unpin</button>
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="row">
        <label>
          Position{' '}
          <select data-shortcut-search value={filter.position ?? ''} onChange={(e) => onFilter({ ...filter, position: e.target.value === '' ? null : Number(e.target.value) })}>
            <option value="">all</option>
            {Array.from({ length: TILE_LENGTH }, (_, i) => (
              <option key={i} value={i + 1}>{i + 1}</option>
            ))}
          </select>
        </label>
        <label>
          Substituted amino acid{' '}
          <select value={filter.aa ?? ''} onChange={(e) => onFilter({ ...filter, aa: e.target.value === '' ? null : e.target.value })}>
            <option value="">all</option>
            {AMINO_ACIDS.split('').map((a) => (
              <option key={a} value={a}>{a}</option>
            ))}
          </select>
        </label>
        <span aria-live="polite" className="muted">
          Showing {rows.length} of {cells.length}
        </span>
      </div>
      <div className="table-wrap" tabIndex={0} role="region" aria-label="Ranking table, scrollable">
        <table className="data" data-testid="rank-table">
          <caption className="visually-hidden">
            Substitutions ranked by raw score within the tile. The probability column is {eventDefinition}.
          </caption>
          <thead>
            <tr>
              {COLUMNS.map((col) => (
                <th
                  key={col.key}
                  scope="col"
                  className={col.numeric ? 'num' : undefined}
                  aria-sort={sort.key === col.key ? (sort.dir === 'asc' ? 'ascending' : 'descending') : 'none'}
                >
                  <button type="button" onClick={() => toggle(col.key)}>
                    {col.label(eventDefinition)}
                    <span aria-hidden="true">{sort.key === col.key ? (sort.dir === 'asc' ? '▲' : '▼') : ''}</span>
                  </button>
                </th>
              ))}
              <th scope="col">Top 10 %</th>
              <th scope="col">Pin</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((c) => {
              const key = cellKey(c.position, c.mut_aa);
              const isSel = key === selectedKey;
              return (
                <tr
                  key={key}
                  ref={isSel ? selectedRow : undefined}
                  aria-current={isSel ? 'true' : undefined}
                  onClick={() => onSelect(c)}
                >
                  <td className="num">{c.rank_in_tile}</td>
                  <td className="num">{c.position}</td>
                  <td>{c.wt_aa}</td>
                  <td>
                    <button type="button" className="link" onClick={(e) => { e.stopPropagation(); onSelect(c); }} aria-label={`Select position ${c.position}, ${c.wt_aa} to ${c.mut_aa}`}>
                      {c.mut_aa}
                    </button>
                  </td>
                  <td className="num">{fmtScore(c.score_dpsi_raw)}</td>
                  <td className="num">{fmtProb(c.p_dpsi_ge_1_calibrated)}</td>
                  <td>{c.top10pct_in_tile ? 'yes' : 'no'}</td>
                  <td>
                    <button type="button" className="link" aria-pressed={pinned.includes(key)} onClick={(e) => { e.stopPropagation(); togglePin(key); }} aria-label={`Pin ${c.wt_aa}${c.position}${c.mut_aa}`}>
                      {pinned.includes(key) ? '★' : '☆'}
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {rows.length === 0 && <p style={{ padding: '0.75rem' }}>No substitutions match the filters.</p>}
      </div>
    </section>
  );
}
