import { useId, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { workspace } from '../api/client';
import type { DomainStatus, JobFootprint } from '../api/types';
import { probabilityColor, rawScoreColor } from '../lib/colors';
import { STATUS } from '../lib/domain';
import { fmtProb, fmtScore } from '../lib/format';
import { ErrorBanner } from './ErrorBanner';
import { Banner, Skeleton } from './ui';

type Mode = 'prob' | 'raw';
type Tile = JobFootprint['tiles'][number];

const LANE = 18;           // height of one tile lane
const GAP = 4;
const TOP = 6;
const BAND = 10;           // domain band below the lanes
const AXIS = 22;

function pxPerResidue(length: number): number {
  return Math.min(12, Math.max(2, 880 / length));
}

function tileSummary(t: Tile, mode: Mode): { mean: number; peak: number | null } | null {
  if (!t.positions.length) return null;
  const v = t.positions.map((p) => (mode === 'prob' ? p.mean_prob : p.mean_raw));
  const peakIdx = v.indexOf(Math.max(...v));
  return { mean: v.reduce((a, b) => a + b, 0) / v.length, peak: t.positions[peakIdx]?.protein_pos ?? null };
}

/**
 * Protein-level footprint (plan-system 2.1): one lane per alternate tile along the protein axis, each window in its own
 * 28-residue context; overlapping residues stay in two lanes and are never averaged. A table carries the same content
 * for narrow screens and assistive technology; clicking a tile opens its saved matrix.
 */
export function ProteinFootprint({ jobId }: { jobId: string }) {
  const [inputId, setInputId] = useState<string | undefined>(undefined);
  const q = useQuery({ queryKey: ['job-footprint', jobId, inputId], queryFn: ({ signal }) => workspace.getJobFootprint(jobId, signal, inputId), retry: false, staleTime: Infinity, placeholderData: (prev) => prev });
  const [mode, setMode] = useState<Mode>('prob');
  const [table, setTable] = useState(false);
  const navigate = useNavigate();
  const name = useId();
  const fp = q.data;
  const limit = useMemo(() => Math.max(0, ...(fp?.tiles.flatMap((t) => t.positions.map((p) => Math.abs(p.mean_raw))) ?? [0])), [fp]);
  if (q.isPending) return <Skeleton lines={3} label="Loading the protein footprint" />;
  if (q.isError) return <ErrorBanner error={q.error} onRetry={() => void q.refetch()} />;
  if (!fp) return null;

  const L = fp.protein.length;
  const k = pxPerResidue(L);
  const width = Math.ceil(L * k) + 2;
  const lanesH = TOP + 2 * LANE + GAP;
  const height = lanesH + BAND + AXIS + 6;
  const x = (pos: number) => 1 + (pos - 1) * k;
  const color = (v: number) => (mode === 'prob' ? probabilityColor(v) : rawScoreColor(v, limit));
  const ticks = Array.from({ length: 6 }, (_, i) => Math.max(1, Math.round((i * L) / 5)));
  const scored = fp.tiles.filter((t) => t.positions.length > 0).length;
  const ev = fp.model.event_definition;

  return (
    <section className="panel" aria-labelledby="pfp-h" data-testid="protein-footprint">
      <h2 id="pfp-h" style={{ marginTop: 0, fontSize: 'var(--text-lg)' }}>Footprint along the protein</h2>
      {/* the limitation comes before any number (R-1) */}
      <Banner tone="info" title="How to read this" testId="protein-footprint-label">{fp.label}</Banner>
      {(fp.proteins?.length ?? 0) > 1 && (
        <label className="row">
          <span>Protein</span>
          <select className="ui-select" value={fp.protein.input_id} onChange={(e) => setInputId(e.target.value)} data-testid="footprint-protein">
            {fp.proteins!.map((p) => <option key={p ?? ''} value={p ?? ''}>{p}</option>)}
          </select>
        </label>
      )}
      <div className="row matrix-toolbar">
        <fieldset className="row" style={{ border: 0, padding: 0, margin: 0 }}>
          <legend className="visually-hidden">Quantity shown along the protein</legend>
          <label><input type="radio" name={name} checked={mode === 'prob'} onChange={() => setMode('prob')} /> Mean probability {ev}</label>
          <label><input type="radio" name={name} checked={mode === 'raw'} onChange={() => setMode('raw')} /> Mean raw score</label>
        </fieldset>
        <button type="button" aria-pressed={table} onClick={() => setTable(!table)}>{table ? 'Show the chart' : 'Show as a table'}</button>
      </div>
      <p className="muted">
        {fp.protein.uniprot_id ?? fp.protein.input_id} · {L} residues · {scored} of {fp.protein.tiles} windows scored with <code>{fp.model.model_id}</code>.
        Each coloured cell is the mean of the 19 substitutions at that position of that window.
        {fp.uncovered.length ? ` Not covered by a full window: ${fp.uncovered.map((u) => `${u.start}–${u.end}`).join(', ')}.` : ''}
      </p>
      {!table && (
        <div className="heatmap-scroll" data-testid="protein-footprint-chart">
          <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} role="img"
            aria-label={`Footprint of ${scored} scored windows along ${L} residues, ${mode === 'prob' ? `mean probability ${ev}` : 'mean raw score'} per position; the table view lists the same values.`}>
            <defs>
              <pattern id="pfp-hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                <line x1="0" y1="0" x2="0" y2="5" style={{ stroke: 'var(--text)', strokeWidth: 1.5 }} />
              </pattern>
              <pattern id="pfp-dot" width="4" height="4" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="0.9" style={{ fill: 'var(--text)' }} />
              </pattern>
            </defs>
            {fp.uncovered.map((u) => (
              <rect key={`u${u.start}`} x={x(u.start)} y={TOP} width={(u.end - u.start + 1) * k} height={2 * LANE + GAP} className="pfp-uncovered" />
            ))}
            {fp.tiles.map((t) => {
              const lane = (t.tile_index - 1) % 2;
              const y = TOP + lane * (LANE + GAP);
              const status = t.domain_status as DomainStatus | null;
              const pattern = status ? STATUS[status]?.pattern : 'empty';
              const open = t.analysis_id ? () => navigate(`/analyses/${t.analysis_id}`) : undefined;
              return (
                <g key={t.item_id} data-testid="pfp-tile" data-tile={t.tile_index} onClick={open} style={{ cursor: open ? 'pointer' : 'default' }}>
                  <title>{`Tile ${t.tile_index}, residues ${t.start_pos}–${t.end_pos}: ${t.positions.length ? 'scored' : t.state}${status ? `, ${STATUS[status]?.label ?? status}` : ''}`}</title>
                  {t.positions.length
                    ? t.positions.map((p) => (
                        <rect key={p.protein_pos} x={x(p.protein_pos)} y={y} width={Math.max(1, k)} height={LANE} style={{ fill: color(mode === 'prob' ? p.mean_prob : p.mean_raw) }} />
                      ))
                    : <rect x={x(t.start_pos)} y={y} width={28 * k} height={LANE} className="pfp-unscored" />}
                  <rect x={x(t.start_pos)} y={y} width={28 * k} height={LANE} className="pfp-outline" />
                  <rect x={x(t.start_pos)} y={lanesH} width={28 * k - 1} height={BAND}
                    className={`pfp-domain pfp-domain--${pattern}`}
                    style={pattern === 'hatched' ? { fill: 'url(#pfp-hatch)' } : pattern === 'dotted' ? { fill: 'url(#pfp-dot)' } : undefined} />
                </g>
              );
            })}
            <line x1={1} x2={width - 1} y1={lanesH + BAND + 4} y2={lanesH + BAND + 4} className="footprint-axis" />
            {ticks.map((t) => (
              <text key={t} x={Math.min(width - 24, x(t))} y={lanesH + BAND + 18} className="footprint-value">{t}</text>
            ))}
          </svg>
        </div>
      )}
      {!table && (
        <ul className="legend" aria-label="Legend of the protein footprint">
          <li>Two lanes alternate so that the 5 residues shared by neighbouring windows stay separate.</li>
          <li>Band below: domain status of the window (solid in domain, hatched outside, dotted borderline or unreliable, empty unknown).</li>
          <li>Grey dashed box: window not scored (refused, failed or cancelled). Shaded background: residues without a full window.</li>
          <li>Click a window to open its 28 × 20 matrix.</li>
        </ul>
      )}
      <div className={table ? undefined : 'visually-hidden'} data-testid="protein-footprint-table">
        <div className="table-wrap" tabIndex={table ? 0 : -1} role="region" aria-label="Protein footprint as a table, scrollable">
          <table className="data">
            <caption className={table ? undefined : 'visually-hidden'}>Windows of the protein: {mode === 'prob' ? `mean probability ${ev}` : 'mean raw score'} over 28 positions</caption>
            <thead><tr><th scope="col">Tile</th><th scope="col">Residues</th><th scope="col">Domain</th><th scope="col">Training peptide</th><th scope="col">Window mean</th><th scope="col">Highest position</th><th scope="col">Matrix</th></tr></thead>
            <tbody>
              {fp.tiles.map((t) => {
                const sm = tileSummary(t, mode);
                const status = t.domain_status as DomainStatus | null;
                return (
                  <tr key={t.item_id}>
                    <th scope="row">{t.tile_index}</th>
                    <td className="num">{t.start_pos}–{t.end_pos}</td>
                    <td>{status ? STATUS[status]?.label ?? status : '—'}</td>
                    <td>{t.training_peptide === null ? '—' : t.training_peptide ? 'yes' : 'no'}</td>
                    <td className="num">{sm ? (mode === 'prob' ? fmtProb(sm.mean) : fmtScore(sm.mean)) : t.state}</td>
                    <td className="num">{sm?.peak ?? '—'}</td>
                    <td>{t.analysis_id ? <Link to={`/analyses/${t.analysis_id}`}>Open tile {t.tile_index}</Link> : '—'}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
