import { describe, expect, it } from 'vitest';
import { contrastRatio, luminance, probabilityColor, rawScoreColor } from '../src/lib/colors';

describe('colour scales (ui-design §5)', () => {
  it('probability: the highest probability is the darkest and the scale is monotone', () => {
    const l = [0, 0.25, 0.5, 0.75, 1].map((p) => luminance(probabilityColor(p)));
    for (let i = 1; i < l.length; i += 1) expect(l[i]!).toBeLessThan(l[i - 1]!);
    expect(l[0]).toBeGreaterThan(0.5);
  });

  it('probability clamps outside 0..1', () => {
    expect(probabilityColor(-1)).toBe(probabilityColor(0));
    expect(probabilityColor(2)).toBe(probabilityColor(1));
  });

  it('raw score: negative is orange-brown, positive is purple, zero is near white', () => {
    const neg = /rgb\((\d+), (\d+), (\d+)\)/.exec(rawScoreColor(-1, 1))!.slice(1).map(Number) as [number, number, number];
    const pos = /rgb\((\d+), (\d+), (\d+)\)/.exec(rawScoreColor(1, 1))!.slice(1).map(Number) as [number, number, number];
    expect(neg[0]).toBeGreaterThan(neg[2]);
    expect(pos[2]).toBeGreaterThan(pos[0]);
    expect(luminance(rawScoreColor(0, 1))).toBeGreaterThan(0.85);
  });

  it('raw score: a zero limit does not divide by zero', () => {
    expect(rawScoreColor(0, 0)).toMatch(/^rgb/);
  });

  it('contrastRatio matches the WCAG reference (black on white is 21)', () => {
    expect(contrastRatio('#000000', '#ffffff')).toBeCloseTo(21, 5);
  });
});
