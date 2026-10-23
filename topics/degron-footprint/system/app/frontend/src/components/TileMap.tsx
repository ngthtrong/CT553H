import { useRef, useState } from 'react';
import type { TileSummary } from '../api/types';
import { STATUS } from '../lib/domain';

const GLYPH = { solid: '●', hatched: '▨', dotted: '◌', empty: '○' } as const;

export function tileDescription(t: TileSummary): string {
  const s = STATUS[t.domain_status];
  const psi = t.psi_wt_measured !== null && t.psi_wt_measured !== undefined ? `, tile PSI ${t.psi_wt_measured.toFixed(2)}` : '';
  return `tile ${t.tile_index}, residues ${t.start_pos}–${t.end_pos}, ${s.label.toLowerCase()}${psi}${t.scorable ? '' : ', cannot be scored'}`;
}

export function DomainLegend() {
  return (
    <ul className="legend" aria-label="Legend of the tile map" style={{ listStyle: 'none', padding: 0 }}>
      <li><span className="swatch solid" aria-hidden="true" /> ● in domain</li>
      <li><span className="swatch hatched" aria-hidden="true" /> ▨ outside the domain</li>
      <li><span className="swatch dotted" aria-hidden="true" /> ◌ unreliable measurement</li>
      <li><span className="swatch empty" aria-hidden="true" /> ○ unknown (no marker)</li>
      <li>p = predicted, not measured</li>
    </ul>
  );
}

interface Props {
  tiles: TileSummary[];
  selected?: number | null;
  onSelect: (index: number) => void;
}

/** One box per tile, N to C terminus. A radio group with roving focus; patterns repeat the colour (ui-design §3.2). */
export function TileMap({ tiles, selected = null, onSelect }: Props) {
  const enabled = tiles.filter((t) => t.scorable);
  const firstEnabled = enabled[0]?.tile_index;
  const [focusIdx, setFocusIdx] = useState<number | null>(selected);
  const refs = useRef(new Map<number, HTMLButtonElement>());
  const tabStop = focusIdx !== null && tiles.some((t) => t.tile_index === focusIdx && t.scorable) ? focusIdx : (selected ?? firstEnabled);

  function move(from: number, delta: number | 'start' | 'end') {
    const idxs = enabled.map((t) => t.tile_index);
    if (idxs.length === 0) return;
    let next: number | undefined;
    if (delta === 'start') next = idxs[0];
    else if (delta === 'end') next = idxs[idxs.length - 1];
    else {
      const pos = idxs.indexOf(from);
      next = idxs[Math.min(idxs.length - 1, Math.max(0, pos + delta))];
    }
    if (next !== undefined) {
      setFocusIdx(next);
      refs.current.get(next)?.focus();
    }
  }

  function onKeyDown(e: React.KeyboardEvent, t: TileSummary) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      move(t.tile_index, 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      move(t.tile_index, -1);
    } else if (e.key === 'Home') {
      e.preventDefault();
      move(t.tile_index, 'start');
    } else if (e.key === 'End') {
      e.preventDefault();
      move(t.tile_index, 'end');
    }
  }

  return (
    <div role="radiogroup" aria-label={`Tiles of the protein, ${tiles.length} in order from the N to the C terminus`} className="tilemap">
      {tiles.map((t) => {
        const s = STATUS[t.domain_status];
        const label = tileDescription(t);
        return (
          <button
            key={t.tile_index}
            ref={(el) => {
              if (el) refs.current.set(t.tile_index, el);
              else refs.current.delete(t.tile_index);
            }}
            type="button"
            role="radio"
            className={`tile ${s.pattern}`}
            aria-checked={selected === t.tile_index}
            aria-disabled={!t.scorable || undefined}
            aria-label={label}
            title={label}
            tabIndex={t.tile_index === tabStop ? 0 : -1}
            onFocus={() => t.scorable && setFocusIdx(t.tile_index)}
            onKeyDown={(e) => onKeyDown(e, t)}
            onClick={() => t.scorable && onSelect(t.tile_index)}
          >
            <span aria-hidden="true">{t.tile_index}</span>
            {s.predicted && (
              <span className="p" aria-hidden="true">
                p
              </span>
            )}
            <span className="visually-hidden">{GLYPH[s.pattern]}</span>
          </button>
        );
      })}
    </div>
  );
}
