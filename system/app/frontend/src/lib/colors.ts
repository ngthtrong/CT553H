import { scaleDiverging, scaleSequential } from 'd3-scale';
import { interpolatePuOr, interpolateViridis } from 'd3-scale-chromatic';

/** Probability 0..1: viridis reversed so that the highest probability is the darkest (ui-design §5). */
export function probabilityColor(p: number): string {
  const t = Math.min(1, Math.max(0, p));
  return scaleSequential(interpolateViridis).domain([1, 0])(t);
}

/**
 * Raw score, diverging around 0 (ColorBrewer PuOr: orange = negative, purple = positive).
 * `limit` is the largest absolute score of the tile, so the scale is symmetric.
 */
export function rawScoreColor(score: number, limit: number): string {
  const m = limit > 0 ? limit : 1;
  // d3's PuOr runs purple to orange; the interface wants orange for negative and purple for positive.
  return scaleDiverging((t: number) => interpolatePuOr(1 - t)).domain([-m, 0, m])(score);
}

/** Relative luminance of a CSS colour given as "rgb(r, g, b)" or "#rrggbb" (WCAG 2.1). */
export function luminance(color: string): number {
  const rgb = parseColor(color);
  const lin = rgb.map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  }) as [number, number, number];
  return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
}

export function contrastRatio(a: string, b: string): number {
  const la = luminance(a);
  const lb = luminance(b);
  const [hi, lo] = la >= lb ? [la, lb] : [lb, la];
  return (hi + 0.05) / (lo + 0.05);
}

function parseColor(color: string): [number, number, number] {
  const hex = /^#([0-9a-f]{6})$/i.exec(color.trim());
  if (hex?.[1]) {
    const n = parseInt(hex[1], 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  const m = /^rgba?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)/i.exec(color.trim());
  if (m) return [Number(m[1]), Number(m[2]), Number(m[3])];
  throw new Error(`Unsupported colour: ${color}`);
}
