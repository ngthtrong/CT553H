import { describe, expect, it } from 'vitest';
import { checkSequence } from '../src/lib/validate';

describe('checkSequence (FR-01, FR-03; E2E-08 client side)', () => {
  it('accepts exactly 28 standard residues, ignoring case and surrounding spaces', () => {
    const r = checkSequence('  dimflvdssgsigpenfskmktfmknlv \n');
    expect(r.issue).toBeNull();
    expect(r.value).toBe('DIMFLVDSSGSIGPENFSKMKTFMKNLV');
  });

  it('names the length when it is wrong', () => {
    const r = checkSequence('DIMFLVDSSGSIGPENFSKMKTFMKNL');
    expect(r.issue?.kind).toBe('length');
    expect(r.issue?.message).toBe('The sequence must have exactly 28 amino acids; it has 27.');
  });

  it('names the first offending character and its position', () => {
    const r = checkSequence('DIMFLVBSSGSIGPENFSKMKTFMKNLV');
    expect(r.issue).toMatchObject({ kind: 'character', position: 7 });
    expect(r.issue?.message).toBe("Position 7: 'B' is not a standard amino acid.");
    expect(r.badIndices).toEqual([6]);
  });

  it.each(['*', '1', '-', 'X', 'U', 'O', 'Z', 'J'])('rejects %s', (ch) => {
    expect(checkSequence(`DIMFLVD${ch}SGSIGPENFSKMKTFMKNLV`).issue?.kind).toBe('character');
  });

  it('treats an inner space as a character problem', () => {
    expect(checkSequence('DIMFLVD SGSIGPENFSKMKTFMKNLV').issue?.message).toContain('a space or line break');
  });

  it('reports an empty string as a length problem of 0', () => {
    expect(checkSequence('').issue?.message).toContain('it has 0');
  });
});
