import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { contrastRatio } from '../src/lib/colors';

const css = readFileSync(resolve(process.cwd(), 'src/styles.css'), 'utf8');

function tokens(selectorStart: string): Record<string, string> {
  const start = css.indexOf(selectorStart);
  const open = css.indexOf('{', start);
  const close = css.indexOf('}', open);
  const out: Record<string, string> = {};
  for (const m of css.slice(open + 1, close).matchAll(/--([a-z-]+):\s*(#[0-9a-fA-F]{6});/g)) out[m[1]!] = m[2]!;
  return out;
}

const themes: Record<string, Record<string, string>> = {
  light: tokens(':root,'),
  dark: tokens("html[data-theme='dark']"),
};

// A11Y-04 / NFR-11: text >= 4.5:1, UI components and focus ring >= 3:1.
const TEXT_PAIRS: [string, string][] = [
  ['text', 'bg'], ['text', 'surface'], ['muted', 'bg'], ['muted', 'surface'], ['accent', 'bg'], ['accent-text', 'accent'],
  ['warn-text', 'warn-bg'], ['danger-text', 'danger-bg'], ['tile-fill-text', 'tile-fill'], ['accent', 'surface'],
];
const UI_PAIRS: [string, string][] = [['border', 'bg'], ['focus', 'bg'], ['focus', 'surface'], ['tile-fill', 'bg'], ['tile-hatch', 'bg'], ['warn-border', 'warn-bg'], ['danger-border', 'danger-bg']];

describe.each(Object.keys(themes))('%s theme tokens', (name) => {
  const t = themes[name]!;
  it('defines every token used by the pairs', () => {
    for (const [a, b] of [...TEXT_PAIRS, ...UI_PAIRS]) {
      expect(t[a], `--${a}`).toBeDefined();
      expect(t[b], `--${b}`).toBeDefined();
    }
  });
  it.each(TEXT_PAIRS)('text %s on %s is at least 4.5:1', (a, b) => {
    expect(contrastRatio(t[a]!, t[b]!)).toBeGreaterThanOrEqual(4.5);
  });
  it.each(UI_PAIRS)('component %s on %s is at least 3:1', (a, b) => {
    expect(contrastRatio(t[a]!, t[b]!)).toBeGreaterThanOrEqual(3);
  });
});
