/**
 * Parsing of peptide-batch and whole-protein input (UC-08; FR-24/25/36; api-spec §5). Pure functions: the preview the
 * user sees before submitting is computed here, the server re-validates everything.
 */
import { checkSequence } from './validate';

export const MAX_PEPTIDES = 100;
export const MAX_PROTEIN = 10_000;
export const TILE = 28;
export const STEP = 23;

export interface ParsedPeptide {
  input_id: string;
  sequence: string;
  /** Null when the entry is valid; otherwise why the server will refuse it (it is still submitted and listed). */
  problem: string | null;
}

export interface BatchPreview {
  entries: ParsedPeptide[];
  valid: number;
  invalid: number;
  duplicateSequences: number;
  overLimit: boolean;
  /** Errors that block submission (no entry, too many, unreadable FASTA). */
  blocking: string | null;
}

function uniqueId(base: string, used: Set<string>): string {
  const clean = base.trim().slice(0, 180) || 'peptide';
  let id = clean;
  for (let n = 2; used.has(id); n += 1) id = `${clean}-${n}`;
  used.add(id);
  return id;
}

/**
 * Accepted forms, one peptide per record:
 *  - multi-record FASTA (`>id description` then sequence lines); the first word of the header is the id
 *  - `id<TAB or comma or spaces>SEQUENCE` lines
 *  - bare sequences, one per line (ids peptide-1, peptide-2, … in input order)
 * Headers are kept as data; ids are made unique by a numeric suffix so duplicates stay distinguishable.
 */
export function parseBatch(text: string): BatchPreview {
  const used = new Set<string>();
  const raw: { id: string; seq: string }[] = [];
  const lines = text.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  if (lines.some((l) => l.startsWith('>'))) {
    let current: { id: string; seq: string } | null = null;
    for (const l of lines) {
      if (l.startsWith('>')) {
        current = { id: l.slice(1).trim().split(/\s+/)[0] ?? '', seq: '' };
        raw.push(current);
      } else if (current) current.seq += l.replace(/\s+/g, '');
      else return { entries: [], valid: 0, invalid: 0, duplicateSequences: 0, overLimit: false, blocking: 'FASTA text must start with a ">" header line.' };
    }
  } else {
    lines.forEach((l, i) => {
      const m = /^(\S+)[\t, ]+(\S+)$/.exec(l);
      raw.push(m ? { id: m[1]!, seq: m[2]! } : { id: `peptide-${i + 1}`, seq: l.replace(/\s+/g, '') });
    });
  }
  const entries = raw.map(({ id, seq }) => {
    const check = checkSequence(seq);
    return { input_id: uniqueId(id || 'peptide', used), sequence: check.value, problem: check.issue?.message ?? null };
  });
  const counts = new Map<string, number>();
  for (const e of entries) if (!e.problem) counts.set(e.sequence, (counts.get(e.sequence) ?? 0) + 1);
  const duplicateSequences = [...counts.values()].reduce((s, n) => s + n - 1, 0);
  const invalid = entries.filter((e) => e.problem).length;
  const overLimit = entries.length > MAX_PEPTIDES;
  const blocking = entries.length === 0 ? 'Paste at least one peptide.' : overLimit ? `A job takes at most ${MAX_PEPTIDES} peptides; this has ${entries.length}.` : null;
  return { entries, valid: entries.length - invalid, invalid, duplicateSequences, overLimit, blocking };
}

export interface ProteinPreview {
  input_id: string;
  sequence: string;
  length: number;
  tiles: number;
  /** Residue intervals no full window covers (only the C-terminal end can be uncovered, windows start at 1). */
  uncovered: { start: number; end: number }[];
  unscorable: number[];
  blocking: string | null;
}

export function tileCount(length: number): number {
  return length < TILE ? 0 : Math.floor((length - TILE) / STEP) + 1;
}

export function coverage(length: number): { tiles: number; uncovered: { start: number; end: number }[] } {
  const tiles = tileCount(length);
  const lastEnd = tiles ? (tiles - 1) * STEP + TILE : 0;
  return { tiles, uncovered: tiles && lastEnd < length ? [{ start: lastEnd + 1, end: length }] : [] };
}

/** One FASTA record (or a bare sequence) for a whole-protein job. */
export function parseProtein(text: string): ProteinPreview {
  const lines = text.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  const headers = lines.filter((l) => l.startsWith('>'));
  const empty = { input_id: '', sequence: '', length: 0, tiles: 0, uncovered: [], unscorable: [] };
  if (headers.length > 1) return { ...empty, blocking: 'Give one protein record; use a peptide batch for several sequences.' };
  const input_id = headers.length ? (headers[0]!.slice(1).trim().split(/\s+/)[0] ?? '') || 'protein' : 'protein';
  const sequence = lines.filter((l) => !l.startsWith('>')).join('').replace(/\s+/g, '').toUpperCase();
  if (!sequence) return { ...empty, input_id, blocking: 'Paste a protein sequence or a FASTA record.' };
  if (/[^A-Z]/.test(sequence)) return { ...empty, input_id, sequence, length: sequence.length, blocking: 'Only one-letter amino-acid codes are allowed.' };
  if (sequence.length > MAX_PROTEIN) return { ...empty, input_id, sequence, length: sequence.length, blocking: `At most ${MAX_PROTEIN} residues; this has ${sequence.length}.` };
  const { tiles, uncovered } = coverage(sequence.length);
  if (tiles === 0) return { ...empty, input_id, sequence, length: sequence.length, blocking: `The protein has ${sequence.length} residues, fewer than one ${TILE}-residue tile.` };
  const unscorable: number[] = [];
  for (let n = 1; n <= tiles; n += 1) {
    const w = sequence.slice((n - 1) * STEP, (n - 1) * STEP + TILE);
    if (checkSequence(w).issue) unscorable.push(n);
  }
  return { input_id, sequence, length: sequence.length, tiles, uncovered, unscorable, blocking: null };
}

export const MAX_PROTEINS = 20;

export interface ProteinsPreview {
  records: ProteinPreview[];
  totalLength: number;
  totalTiles: number;
  blocking: string | null;
}

/**
 * One or more FASTA records for a whole-protein job (plan-system 3.3). Each record is checked like a single protein; a
 * record with an error is listed with it (the server refuses that protein only); the residue limit is the total.
 */
export function parseProteins(text: string): ProteinsPreview {
  const chunks: string[] = [];
  for (const line of text.split(/\r?\n/)) {
    if (line.trim().startsWith('>') || chunks.length === 0) chunks.push(line);
    else chunks[chunks.length - 1] += `\n${line}`;
  }
  const records = chunks.map((c) => c.trim()).filter(Boolean).map((c, i) => {
    const r = parseProtein(c);
    return c.startsWith('>') || i > 0 ? r : { ...r, input_id: r.input_id || 'protein' };
  });
  const ids = records.map((r) => r.input_id);
  const totalLength = records.reduce((s, r) => s + r.length, 0);
  let blocking: string | null = null;
  if (records.length === 0) blocking = 'Paste a protein sequence or FASTA records.';
  else if (records.length > MAX_PROTEINS) blocking = `At most ${MAX_PROTEINS} proteins in one job.`;
  else if (new Set(ids).size !== ids.length) blocking = 'Two records have the same id; give each record its own name after ">".';
  else if (totalLength > MAX_PROTEIN) blocking = `At most ${MAX_PROTEIN} residues in total; these records have ${totalLength}.`;
  else if (records.length === 1 && records[0]!.blocking) blocking = records[0]!.blocking;
  else if (records.every((r) => r.blocking)) blocking = 'No record can be scored.';
  return { records, totalLength, totalTiles: records.reduce((s, r) => s + (r.blocking ? 0 : r.tiles), 0), blocking };
}
