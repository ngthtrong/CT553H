import { AMINO_ACIDS, TILE_LENGTH } from '../api/types';

export interface SequenceIssue {
  kind: 'length' | 'character';
  message: string;
  /** 1-based position of the first offending character (character issues only). */
  position?: number;
}

export interface SequenceCheck {
  /** Trimmed and upper-cased, as the server will do it. */
  value: string;
  /** Indices (0-based) of characters that are not standard amino acids. */
  badIndices: number[];
  issue: SequenceIssue | null;
}

function describeChar(ch: string): string {
  if (ch === ' ' || ch === '\t' || ch === '\n') return 'a space or line break';
  if (ch === '*') return "'*' (a stop symbol)";
  return `'${ch}'`;
}

/** Client-side check of a typed tile. Mirrors the server rules of api-spec §3 step 4. */
export function checkSequence(raw: string): SequenceCheck {
  const value = raw.trim().toUpperCase();
  const badIndices: number[] = [];
  for (let i = 0; i < value.length; i += 1) {
    if (!AMINO_ACIDS.includes(value.charAt(i))) badIndices.push(i);
  }
  if (badIndices.length > 0) {
    const first = badIndices[0] ?? 0;
    return {
      value,
      badIndices,
      issue: {
        kind: 'character',
        position: first + 1,
        message:
          badIndices.length === 1
            ? `Position ${first + 1}: ${describeChar(value.charAt(first))} is not a standard amino acid.`
            : `Position ${first + 1}: ${describeChar(value.charAt(first))} is not a standard amino acid (${badIndices.length} characters are not standard).`,
      },
    };
  }
  if (value.length !== TILE_LENGTH) {
    return {
      value,
      badIndices,
      issue: {
        kind: 'length',
        message: `The sequence must have exactly ${TILE_LENGTH} amino acids; it has ${value.length}.`,
      },
    };
  }
  return { value, badIndices, issue: null };
}
