import { useMemo, useRef, useState } from 'react';
import { AMINO_ACIDS, N_CELLS, TILE_LENGTH } from '../api/types';
import type { Cell, ClinvarVariant, MeasuredCell, TileInfo } from '../api/types';
import { probabilityColor, rawScoreColor } from '../lib/colors';
import { fmtProb, fmtScore } from '../lib/format';
import type { ScaleMode } from './ScaleToggle';

const CELL = 28;
const LABEL_W = 76;
const HEAD_H = 28;
const COLS = AMINO_ACIDS.length;

export const cellKey = (position: number, aa: string): string => `${position}:${aa}`;

type Clinsig = ClinvarVariant['clinsig'];
export const CLINVAR_LABEL: Record<Clinsig, string> = {
  pathogenic: 'pathogenic',
  likely_pathogenic: 'likely pathogenic',
  vus: 'uncertain significance',
  likely_benign: 'likely benign',
  benign: 'benign',
  conflicting: 'conflicting interpretations',
  other: 'other',
};

/** A different shape per class, so that the class does not depend on colour (ui-design §5). */
function Glyph({ clinsig, cx, cy }: { clinsig: Clinsig; cx: number; cy: number }) {
  const r = 6;
  switch (clinsig) {
    case 'pathogenic':
      return <path className="glyph filled" d={`M${cx} ${cy - r}L${cx + r} ${cy}L${cx} ${cy + r}L${cx - r} ${cy}Z`} />;
    case 'likely_pathogenic':
      return <path className="glyph" d={`M${cx} ${cy - r}L${cx + r} ${cy}L${cx} ${cy + r}L${cx - r} ${cy}Z`} />;
    case 'vus':
      return <circle className="glyph" cx={cx} cy={cy} r={r - 1} />;
    case 'likely_benign':
      return <path className="glyph" d={`M${cx} ${cy - r}L${cx + r} ${cy + r}L${cx - r} ${cy + r}Z`} />;
    case 'benign':
      return <path className="glyph filled" d={`M${cx} ${cy - r}L${cx + r} ${cy + r}L${cx - r} ${cy + r}Z`} />;
    case 'conflicting':
      return <rect className="glyph" x={cx - r + 1} y={cy - r + 1} width={2 * r - 2} height={2 * r - 2} />;
    default:
      return <path className="glyph" d={`M${cx - r} ${cy - r}L${cx + r} ${cy + r}M${cx + r} ${cy - r}L${cx - r} ${cy + r}`} />;
  }
}

export function ClinvarLegend({ classes }: { classes: Clinsig[] }) {
  if (classes.length === 0) return null;
  return (
    <ul className="legend" aria-label="ClinVar marker shapes" style={{ listStyle: 'none', padding: 0 }}>
      {classes.map((c) => (
        <li key={c}>
          <svg width="16" height="16" viewBox="-2 -2 20 20" aria-hidden="true" className="heatmap" style={{ verticalAlign: 'middle' }}>
            <Glyph clinsig={c} cx={8} cy={8} />
          </svg>{' '}
          {CLINVAR_LABEL[c]}
        </li>
      ))}
    </ul>
  );
}

interface Props {
  cells: Cell[];
  tile: TileInfo;
  mode: ScaleMode;
  eventDefinition: string;
  measured?: MeasuredCell[];
  clinvar?: ClinvarVariant[];
  /** Attribution + disclaimer, repeated in the detail card for ClinVar variants (rule W-6). */
  clinvarNote?: string;
  selectedKey: string | null;
  onSelect: (c: Cell) => void;
}

/**
 * 28 x 19 effect matrix as one SVG (ui-design §7). It is an ARIA grid with a single tab stop and arrow-key
 * navigation; selection and hover do not re-render the 560 cells beyond the two outline rectangles.
 */
export function Heatmap({ cells, tile, mode, eventDefinition, measured, clinvar, clinvarNote, selectedKey, onSelect }: Props) {
  const byKey = useMemo(() => new Map(cells.map((c) => [cellKey(c.position, c.mut_aa), c])), [cells]);
  const measuredBy = useMemo(() => new Map((measured ?? []).map((m) => [cellKey(m.position, m.mut_aa), m])), [measured]);
  const clinvarBy = useMemo(() => {
    const m = new Map<string, ClinvarVariant[]>();
    for (const v of clinvar ?? []) {
      const k = cellKey(v.position, v.alt_aa);
      m.set(k, [...(m.get(k) ?? []), v]);
    }
    return m;
  }, [clinvar]);
  const limit = useMemo(() => Math.max(0, ...cells.map((c) => Math.abs(c.score_dpsi_raw))), [cells]);

  const [focus, setFocus] = useState<{ r: number; c: number }>({ r: 0, c: 0 });
  const [active, setActive] = useState<{ r: number; c: number } | null>(null);
  const refs = useRef(new Map<string, SVGRectElement>());
  const seq = tile.sequence;

  const fill = (c: Cell) => (mode === 'prob' ? probabilityColor(c.p_dpsi_ge_1_calibrated) : rawScoreColor(c.score_dpsi_raw, limit));

  function describe(r: number, col: number): string {
    const pos = r + 1;
    const wt = seq.charAt(r);
    const aa = AMINO_ACIDS.charAt(col);
    if (aa === wt) return `position ${pos}, wild type ${wt}, no substitution`;
    const c = byKey.get(cellKey(pos, aa));
    if (!c) return `position ${pos}, ${wt} to ${aa}, no value`;
    let s = `position ${pos}, ${wt} to ${aa}, probability ${eventDefinition} ${fmtProb(c.p_dpsi_ge_1_calibrated)}, raw score ${fmtScore(c.score_dpsi_raw)}, rank ${c.rank_in_tile} of ${N_CELLS}`;
    const m = measuredBy.get(cellKey(pos, aa));
    if (m) s += `, measured ΔPSI ${m.delta_psi.toFixed(2)}`;
    const v = clinvarBy.get(cellKey(pos, aa));
    if (v) s += `, ClinVar: ${v.map((x) => CLINVAR_LABEL[x.clinsig]).join(', ')}`;
    return s;
  }

  function moveTo(r: number, c: number) {
    const rr = Math.min(TILE_LENGTH - 1, Math.max(0, r));
    const cc = Math.min(COLS - 1, Math.max(0, c));
    setFocus({ r: rr, c: cc });
    refs.current.get(`${rr}:${cc}`)?.focus();
  }

  function onKeyDown(e: React.KeyboardEvent, r: number, c: number) {
    switch (e.key) {
      case 'ArrowRight': e.preventDefault(); moveTo(r, c + 1); break;
      case 'ArrowLeft': e.preventDefault(); moveTo(r, c - 1); break;
      case 'ArrowDown': e.preventDefault(); moveTo(r + 1, c); break;
      case 'ArrowUp': e.preventDefault(); moveTo(r - 1, c); break;
      case 'Home': e.preventDefault(); moveTo(r, 0); break;
      case 'End': e.preventDefault(); moveTo(r, COLS - 1); break;
      case 'Enter':
      case ' ': {
        e.preventDefault();
        const cell = byKey.get(cellKey(r + 1, AMINO_ACIDS.charAt(c)));
        if (cell) onSelect(cell);
        break;
      }
      case 'Escape': {
        // Leave the grid: move focus to the region around it.
        (e.currentTarget.closest('[data-heatmap-region]') as HTMLElement | null)?.focus();
        break;
      }
      default:
    }
  }

  const shown = active ?? (selectedKey ? selectedPos(selectedKey) : null);
  function selectedPos(k: string): { r: number; c: number } | null {
    const [p, aa] = k.split(':');
    const c = AMINO_ACIDS.indexOf(aa ?? '');
    return p && c >= 0 ? { r: Number(p) - 1, c } : null;
  }

  const width = LABEL_W + COLS * CELL;
  const height = HEAD_H + TILE_LENGTH * CELL;
  const selPos = selectedKey ? selectedPos(selectedKey) : null;
  const classesPresent = Array.from(new Set((clinvar ?? []).map((v) => v.clinsig)));

  // Colour bar stops (probability or raw score), computed from the same functions as the cells.
  const stops = Array.from({ length: 11 }, (_, i) => {
    const t = i / 10;
    return mode === 'prob' ? probabilityColor(t) : rawScoreColor((t * 2 - 1) * (limit || 1), limit);
  });

  const detail = shown ? detailFor(shown.r, shown.c) : null;
  function detailFor(r: number, col: number) {
    const pos = r + 1;
    const wt = seq.charAt(r);
    const aa = AMINO_ACIDS.charAt(col);
    if (aa === wt) return { text: `Position ${pos}: wild type ${wt}. There is no substitution in this cell.`, variants: [] as ClinvarVariant[] };
    const c = byKey.get(cellKey(pos, aa));
    const m = measuredBy.get(cellKey(pos, aa));
    const v = clinvarBy.get(cellKey(pos, aa)) ?? [];
    if (!c) return { text: `Position ${pos}, ${wt} to ${aa}: no value.`, variants: v };
    return {
      text: `Position ${pos}, ${wt} → ${aa}. Probability ${eventDefinition}: ${fmtProb(c.p_dpsi_ge_1_calibrated)}. Raw score: ${fmtScore(c.score_dpsi_raw)} (${c.score_dpsi_raw < 0 ? 'negative' : 'positive'}). Rank ${c.rank_in_tile} of ${N_CELLS}${c.top10pct_in_tile ? ' (top 10 %)' : ''}.${m ? ` Measured ΔPSI: ${m.delta_psi.toFixed(2)}.` : ''}`,
      variants: v,
    };
  }

  return (
    <div data-heatmap-region tabIndex={-1}>
      <div className="row" style={{ margin: '0.5rem 0' }}>
        <div>
          <div
            className="colorbar"
            data-testid="colorbar"
            style={{ background: `linear-gradient(90deg, ${stops.join(', ')})` }}
            role="img"
            aria-label={mode === 'prob' ? 'Colour bar from probability 0 (light) to 1 (dark)' : 'Colour bar of the raw score from negative (orange) through 0 to positive (purple)'}
          />
          <div className="row muted" style={{ justifyContent: 'space-between', width: 260, gap: 0 }}>
            {mode === 'prob' ? (
              <><span>0</span><span>0.5</span><span>1</span></>
            ) : (
              <><span>{(-limit).toFixed(2)}</span><span>0</span><span>{limit.toFixed(2)}</span></>
            )}
          </div>
        </div>
        <p className="muted" style={{ margin: 0, flex: 1, minWidth: 220 }}>
          {mode === 'prob'
            ? `Probability that the substitution raises PSI by at least one bin (weakens the degron signal) in this assay: ${eventDefinition}. Darker is more likely.`
            : 'Raw score: regression output of ΔPSI, not a probability. Orange is negative, purple is positive.'}
        </p>
      </div>

      <div className="heatmap-scroll">
        <svg className="heatmap" width={width} height={height} viewBox={`0 0 ${width} ${height}`} data-testid="heatmap">
          <defs>
            <pattern id="wt-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect width="6" height="6" style={{ fill: 'var(--bg)' }} />
              <line x1="0" y1="0" x2="0" y2="6" style={{ stroke: 'var(--text)', strokeWidth: 2 }} />
            </pattern>
          </defs>
          <g role="grid" aria-label="Predicted effect of each substitution. Rows are positions of the tile, columns are the substituted amino acids." aria-rowcount={TILE_LENGTH + 1} aria-colcount={COLS + 1}>
            <g role="row" aria-rowindex={1}>
              <text role="columnheader" x={4} y={HEAD_H - 8} aria-label="Position and wild type">pos</text>
              {AMINO_ACIDS.split('').map((aa, c) => (
                <text key={aa} role="columnheader" x={LABEL_W + c * CELL + CELL / 2} y={HEAD_H - 8} textAnchor="middle">
                  {aa}
                </text>
              ))}
            </g>
            {seq.split('').map((wt, r) => (
              <g key={r} role="row" aria-rowindex={r + 2}>
                <text role="rowheader" x={4} y={HEAD_H + r * CELL + CELL / 2 + 4}>
                  {String(r + 1).padStart(2, ' ')} {wt}
                </text>
                {AMINO_ACIDS.split('').map((aa, c) => {
                  const isWt = aa === wt;
                  const cell = isWt ? undefined : byKey.get(cellKey(r + 1, aa));
                  const x = LABEL_W + c * CELL;
                  const y = HEAD_H + r * CELL;
                  const key = `${r}:${c}`;
                  return (
                    <rect
                      key={key}
                      ref={(el) => {
                        if (el) refs.current.set(key, el);
                        else refs.current.delete(key);
                      }}
                      role="gridcell"
                      className="cell"
                      x={x}
                      y={y}
                      width={CELL}
                      height={CELL}
                      style={{ fill: isWt ? 'url(#wt-hatch)' : cell ? fill(cell) : 'var(--surface)' }}
                      tabIndex={focus.r === r && focus.c === c ? 0 : -1}
                      aria-label={describe(r, c)}
                      aria-selected={selectedKey === cellKey(r + 1, aa) ? true : undefined}
                      onFocus={() => {
                        setFocus({ r, c });
                        setActive({ r, c });
                      }}
                      onBlur={() => setActive(null)}
                      onMouseEnter={() => setActive({ r, c })}
                      onMouseLeave={() => setActive(null)}
                      onKeyDown={(e) => onKeyDown(e, r, c)}
                      onClick={() => {
                        setFocus({ r, c });
                        if (cell) onSelect(cell);
                      }}
                    >
                      <title>{describe(r, c)}</title>
                    </rect>
                  );
                })}
              </g>
            ))}
          </g>
          {/* Layers and outlines are drawn after the cells and ignore the pointer. */}
          {[...measuredBy.keys()].map((k) => {
            const [p, aa] = k.split(':');
            const c = AMINO_ACIDS.indexOf(aa ?? '');
            if (!p || c < 0) return null;
            return <rect key={`m${k}`} className="measured-ring" x={LABEL_W + c * CELL + 3} y={HEAD_H + (Number(p) - 1) * CELL + 3} width={CELL - 6} height={CELL - 6} />;
          })}
          {[...clinvarBy.entries()].map(([k, vs]) => {
            const [p, aa] = k.split(':');
            const c = AMINO_ACIDS.indexOf(aa ?? '');
            const v = vs[0];
            if (!p || c < 0 || !v) return null;
            return <Glyph key={`v${k}`} clinsig={v.clinsig} cx={LABEL_W + c * CELL + CELL - 9} cy={HEAD_H + (Number(p) - 1) * CELL + 9} />;
          })}
          {selPos && <rect className="cell-selected" x={LABEL_W + selPos.c * CELL + 1} y={HEAD_H + selPos.r * CELL + 1} width={CELL - 2} height={CELL - 2} />}
          {active && <rect className="cell-focus" x={LABEL_W + active.c * CELL + 1} y={HEAD_H + active.r * CELL + 1} width={CELL - 2} height={CELL - 2} />}
        </svg>
      </div>
      <p className="muted" style={{ margin: '0.25rem 0' }}>
        Hatched cell = wild type (no substitution).{' '}
        {measured && measured.length > 0 && 'Outlined cell = measured ΔPSI available. '}
        {clinvar && clinvar.length > 0 && 'Marker = ClinVar variant.'}
      </p>
      <ClinvarLegend classes={classesPresent} />

      <div className="cell-details" role="status" aria-live="polite" data-testid="cell-details">
        {detail ? (
          <>
            <div>{detail.text}</div>
            {measured && measured.length > 0 && (
              <div className="muted">Measured values are part of the training data of this model; they are not a validation.</div>
            )}
            {detail.variants.length > 0 && (
              <div>
                {detail.variants.map((v) => (
                  <div key={v.variation_id}>
                    ClinVar {v.variation_id}: {v.ref_aa}
                    {v.protein_pos}
                    {v.alt_aa}, {CLINVAR_LABEL[v.clinsig]}
                    {v.review_status ? ` (${v.review_status})` : ''}.
                  </div>
                ))}
                {clinvarNote && <div className="muted">{clinvarNote}</div>}
              </div>
            )}
          </>
        ) : (
          <span className="muted">Hover or focus a cell to see its values. Press Enter to select it in the ranking table.</span>
        )}
      </div>
    </div>
  );
}
