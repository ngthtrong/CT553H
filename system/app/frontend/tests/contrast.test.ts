import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { contrastRatio } from '../src/lib/colors';

const css = readFileSync(resolve(process.cwd(), 'src/styles/tokens.css'), 'utf8');

function block(selectorStart: string): string {
  const start = css.indexOf(selectorStart);
  if (start < 0) throw new Error(`no block ${selectorStart}`);
  const open = css.indexOf('{', start);
  return css.slice(open + 1, css.indexOf('}', open));
}

// layer 1: primitives (hex only); layer 2: purpose tokens may refer to primitives through var()
const primitives: Record<string, string> = {};
for (const m of block('/* ---- 1. primitives').matchAll(/--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6});/g)) primitives[m[1]!] = m[2]!;

function tokens(selectorStart: string): Record<string, string> {
  const out: Record<string, string> = {};
  for (const m of block(selectorStart).matchAll(/--([a-z-]+):\s*([^;]+);/g)) {
    const raw = m[2]!.trim();
    const ref = /^var\(--([a-z0-9-]+)\)$/.exec(raw);
    const hex = ref ? primitives[ref[1]!] : /^#[0-9a-fA-F]{6}$/.test(raw) ? raw : undefined;
    if (hex) out[m[1]!] = hex;
  }
  return out;
}

const themes: Record<string, Record<string, string>> = {
  light: tokens(':root,\nhtml[data-theme=\'light\']'),
  dark: tokens("html[data-theme='dark'] {"),
};

// A11Y-04 / NFR-11: text >= 4.5:1, UI components and focus ring >= 3:1.
const TEXT_PAIRS: [string, string][] = [
  ['text', 'bg'], ['text', 'surface'], ['muted', 'bg'], ['muted', 'surface'], ['accent', 'bg'], ['accent-text', 'accent'],
  ['warn-text', 'warn-bg'], ['danger-text', 'danger-bg'], ['tile-fill-text', 'tile-fill'], ['accent', 'surface'],
  ['text', 'subtle'], ['accent-ink', 'accent-soft'], ['text', 'accent-soft'], ['info-text', 'info-bg'],
];
const UI_PAIRS: [string, string][] = [['border', 'surface'], ['border', 'bg'], ['focus', 'bg'], ['focus', 'surface'], ['tile-fill', 'bg'], ['tile-hatch', 'bg'], ['warn-border', 'warn-bg'], ['danger-border', 'danger-bg']];

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
