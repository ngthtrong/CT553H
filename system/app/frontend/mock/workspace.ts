/**
 * Mock of the 24 planned workspace operations of openapi.yaml (projects, analyses, jobs, datasets, comparisons),
 * so the v0.2 screens can be built and tested before the backend exists (implementation plan WP3.4).
 *
 * ALL NUMBERS ARE SYNTHETIC FIXTURES. Scores come from the same fake predictor as the single-tile mock; comparison
 * metrics are computed from whatever the test or developer imports. State lives in memory and is cleared by
 * resetWorkspace(). Job progress is simulated: every read of a running job finishes one more item, so polling
 * screens see pending → running → terminal without timers.
 */
import { createHash, randomUUID } from 'node:crypto';
import type { components } from '../src/api/schema';

type S = components['schemas'];
type Project = S['Project'];
type SavedAnalysis = S['SavedAnalysis'];
type PredictionResult = S['PredictionResult'];
type Job = S['Job'];
type JobItem = S['JobItem'];
type Dataset = S['Dataset'];
type ImportMetadata = S['ImportMetadata'];
type ValidationIssue = S['ValidationIssue'];
type Comparison = S['Comparison'];

export interface MockResponse {
  status: number;
  headers: Record<string, string>;
  body: string;
}

type Predicted = { ok: true; result: unknown; request: Record<string, unknown> } | { ok: false; response: MockResponse };

export interface WorkspaceDeps {
  predict(body: string): Predicted;
  ok(body: unknown, headers?: Record<string, string>, status?: number): MockResponse;
  err(status: number, code: string, message: string, field?: string | null): MockResponse;
  exportResult(result: unknown, format: string): MockResponse;
  proteins: { uniprot_id: string; length: number }[];
  tileSequence(acc: string, n: number): string;
}

const AA = /^[ACDEFGHIKLMNPQRSTVWY]+$/;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const MAX_PEPTIDES = 100;
const MAX_PROTEIN = 10_000;
const MAX_IMPORT_BYTES = 10 * 1024 * 1024;
const MAX_IMPORT_ROWS = 100_000;

interface StoredJob {
  job: Job;
  items: (JobItem & { request: Record<string, unknown> })[];
}
interface StoredDataset {
  dataset: Dataset;
  rows: Observation[];
}
interface Observation {
  peptide_id: string;
  wt_sequence: string;
  position: number;
  wt_aa: string;
  mut_aa: string;
  replicate_id: string;
  observed_value: number | null;
  missing_reason: string | null;
}

const projects = new Map<string, Project>();
const analyses = new Map<string, SavedAnalysis>();
const jobs = new Map<string, StoredJob>();
const datasets = new Map<string, StoredDataset>();
const comparisons = new Map<string, Comparison>();

export function resetWorkspace(): void {
  projects.clear();
  analyses.clear();
  jobs.clear();
  datasets.clear();
  comparisons.clear();
}

const now = () => new Date().toISOString();

function page<T>(all: T[], url: URL, deps: WorkspaceDeps): MockResponse {
  const offset = Number(url.searchParams.get('offset') ?? 0);
  const limit = Number(url.searchParams.get('limit') ?? 50);
  if (!Number.isInteger(offset) || offset < 0) return deps.err(422, 'INVALID_REQUEST', 'offset must be a non-negative integer.', 'offset');
  if (!Number.isInteger(limit) || limit < 1 || limit > 200) return deps.err(422, 'INVALID_REQUEST', 'limit must be 1…200.', 'limit');
  return deps.ok({ items: all.slice(offset, offset + limit), total: all.length, offset, limit });
}

function parseJson(body: string): Record<string, unknown> | null {
  try {
    const v: unknown = JSON.parse(body);
    return v && typeof v === 'object' && !Array.isArray(v) ? (v as Record<string, unknown>) : null;
  } catch {
    return null;
  }
}

function touch(projectId: string): void {
  const p = projects.get(projectId);
  if (p) p.updated_at = now();
}

function counted(p: Project): Project {
  const id = p.project_id;
  return {
    ...p,
    counts: {
      analyses: [...analyses.values()].filter((a) => a.project_id === id).length,
      jobs: [...jobs.values()].filter((j) => j.job.project_id === id).length,
      datasets: [...datasets.values()].filter((d) => d.dataset.project_id === id).length,
    },
  };
}

function confirmRequired(url: URL, deps: WorkspaceDeps, dependencies: Record<string, number>): MockResponse | null {
  if (url.searchParams.get('confirm') === 'true') return null;
  return {
    ...deps.err(409, 'CONFIRMATION_REQUIRED', 'Deleting removes the records listed in dependencies. Repeat with confirm=true.'),
    body: JSON.stringify({ code: 'CONFIRMATION_REQUIRED', message: 'Deleting removes the records listed in dependencies. Repeat with confirm=true.', field: null, dependencies }),
  };
}

function deleteAnalysisCascade(id: string): void {
  analyses.delete(id);
  for (const [cid, c] of comparisons) if (c.analysis_id === id) comparisons.delete(cid);
}

function deleteDatasetCascade(id: string): void {
  datasets.delete(id);
  for (const [cid, c] of comparisons) if (c.dataset_id === id) comparisons.delete(cid);
}

function newAnalysis(projectId: string, result: unknown, request: Record<string, unknown>, parent: string | null): SavedAnalysis {
  const r = result as PredictionResult;
  const a: SavedAnalysis = {
    analysis_id: randomUUID(),
    project_id: projectId,
    parent_analysis_id: parent,
    parent_available: parent === null ? undefined : analyses.has(parent),
    created_at: now(),
    result: r,
    snapshot: {
      snapshot_version: 1,
      request,
      model_id: r.provenance.model_id,
      domain_status: r.domain.status,
      annotation_sources: r.provenance.data_sources,
    },
  };
  analyses.set(a.analysis_id, a);
  touch(projectId);
  return a;
}

function summary(a: SavedAnalysis): S['SavedAnalysisSummary'] {
  const r = a.result;
  return {
    analysis_id: a.analysis_id,
    project_id: a.project_id,
    parent_analysis_id: a.parent_analysis_id ?? null,
    job_id: null,
    created_at: a.created_at,
    input_kind: r.tile.uniprot_id ? 'uniprot_tile' : 'sequence',
    tile: r.tile,
    domain_status: r.domain.status,
    model_id: r.provenance.model_id,
    warning_codes: r.warnings.map((w) => w.code),
  };
}

// --- jobs -----------------------------------------------------------------------------------------------------------

function itemFor(ordinal: number, inputId: string, request: Record<string, unknown>, extra: Partial<JobItem> = {}) {
  return { item_id: `item-${String(ordinal).padStart(5, '0')}`, input_id: inputId, state: 'pending' as JobItem['state'], request, ...extra };
}

function submitJob(projectId: string, body: string, deps: WorkspaceDeps): MockResponse {
  const req = parseJson(body);
  if (!req) return deps.err(400, 'INVALID_REQUEST', 'The request body is not valid JSON.');
  const mode = req.mode;
  const items: StoredJob['items'] = [];
  let coverage: Record<string, unknown> | undefined;
  if (mode === 'peptides') {
    if ('protein' in req) return deps.err(422, 'INVALID_REQUEST', 'A peptide job takes peptides only.', 'protein');
    const list = req.peptides;
    if (!Array.isArray(list) || list.length < 1) return deps.err(422, 'INVALID_REQUEST', 'Give at least one peptide.', 'peptides');
    if (list.length > MAX_PEPTIDES) return deps.err(413, 'PAYLOAD_TOO_LARGE', `At most ${MAX_PEPTIDES} peptides per job.`, 'peptides');
    const seen = new Set<string>();
    for (const [i, raw] of list.entries()) {
      const p = raw as Record<string, unknown>;
      const id = String(p.input_id ?? '');
      if (!id || seen.has(id)) return deps.err(422, 'INVALID_REQUEST', 'Every peptide needs a unique input_id.', 'peptides');
      seen.add(id);
      const seq = String(p.sequence ?? '').replace(/\s+/g, '').toUpperCase();
      const bad = seq.length !== 28 ? 'INVALID_LENGTH' : !AA.test(seq) ? 'INVALID_CHARACTER' : null;
      items.push(
        itemFor(i + 1, id, { sequence: seq }, bad ? { state: 'refused', error: { code: bad, message: bad === 'INVALID_LENGTH' ? `The sequence has ${seq.length} residues; 28 are needed.` : 'The sequence contains a letter outside the 20 standard amino acids.' } } : {}),
      );
    }
  } else if (mode === 'protein') {
    if ('peptides' in req) return deps.err(422, 'INVALID_REQUEST', 'A protein job takes one protein only.', 'peptides');
    const prot = (req.protein ?? {}) as Record<string, unknown>;
    const acc = typeof prot.uniprot_id === 'string' ? prot.uniprot_id : null;
    const typed = typeof prot.sequence === 'string' ? prot.sequence.replace(/\s+/g, '').toUpperCase() : null;
    if ((acc === null) === (typed === null)) return deps.err(422, 'INVALID_REQUEST', 'Give exactly one of uniprot_id or sequence.', 'protein');
    let length: number;
    let seqAt: (n: number) => string;
    if (acc !== null) {
      const p = deps.proteins.find((x) => x.uniprot_id === acc);
      if (!p) return deps.err(404, 'UNKNOWN_ACCESSION', 'This accession is not in the loaded reference.', 'protein.uniprot_id');
      length = p.length;
      seqAt = (n) => deps.tileSequence(acc, n);
    } else {
      const s = typed ?? '';
      if (s.length > MAX_PROTEIN) return deps.err(413, 'PAYLOAD_TOO_LARGE', `At most ${MAX_PROTEIN} residues.`, 'protein.sequence');
      length = s.length;
      seqAt = (n) => s.slice((n - 1) * 23, (n - 1) * 23 + 28);
    }
    if (length < 28) return deps.err(422, 'INVALID_LENGTH', 'The protein is shorter than one 28-residue tile.', 'protein');
    const n = Math.floor((length - 28) / 23) + 1;
    const lastEnd = (n - 1) * 23 + 28;
    coverage = {
      protein_length: length,
      tiles: n,
      step: 23,
      tile_length: 28,
      uncovered: lastEnd < length ? [{ start: lastEnd + 1, end: length }] : [],
    };
    for (let i = 1; i <= n; i += 1) {
      const seq = seqAt(i);
      const start = (i - 1) * 23 + 1;
      const extra: Partial<JobItem> = { tile_index: i, start_pos: start, end_pos: start + 27 };
      if (!AA.test(seq)) Object.assign(extra, { state: 'refused', error: { code: 'TILE_NOT_SCORABLE', message: 'The window contains a non-standard residue.' } });
      const request = acc !== null ? { uniprot_id: acc, tile_index: i } : { sequence: seq };
      items.push(itemFor(i, String(prot.input_id ?? acc ?? 'protein'), request, extra));
    }
  } else {
    return deps.err(422, 'INVALID_REQUEST', 'mode must be peptides or protein.', 'mode');
  }
  const t = now();
  const job: Job = {
    job_id: randomUUID(),
    project_id: projectId,
    mode,
    state: 'pending',
    total: items.length,
    counts: {},
    cancel_requested: false,
    coverage,
    configuration_snapshot: { model_id: 'mock-m3-ext4.0-platt-v1', calibrator: 'platt', override_domain: req.override_domain === true, gate: null },
    created_at: t,
    updated_at: t,
  };
  const stored = { job, items };
  recount(stored);
  jobs.set(job.job_id, stored);
  touch(projectId);
  return deps.ok(job, {}, 202);
}

function recount(s: StoredJob): void {
  const counts: Record<string, number> = {};
  for (const it of s.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
  s.job.counts = counts;
  const open = (counts.pending ?? 0) + (counts.running ?? 0);
  if (open === 0) {
    const ok = counts.succeeded ?? 0;
    if (s.job.cancel_requested) s.job.state = 'cancelled';
    else if (ok === s.items.length) s.job.state = 'completed';
    else s.job.state = ok > 0 ? 'partial' : 'failed';
  }
}

/** One simulated worker step per read: finish the running item, start the next pending one. */
function advance(s: StoredJob, deps: WorkspaceDeps): void {
  if (['completed', 'partial', 'failed', 'cancelled'].includes(s.job.state)) return;
  const running = s.items.find((i) => i.state === 'running');
  if (running) {
    const r = deps.predict(JSON.stringify(running.request));
    if (r.ok) {
      const a = newAnalysis(s.job.project_id, r.result, r.request, null);
      running.state = 'succeeded';
      running.analysis_id = a.analysis_id;
      running.domain_status = a.result.domain.status;
    } else {
      const e = JSON.parse(r.response.body) as { code: S['Error']['code']; message: string };
      running.state = e.code === 'OUT_OF_DOMAIN' ? 'refused' : 'failed';
      running.error = { code: e.code, message: e.message };
    }
  }
  const next = s.items.find((i) => i.state === 'pending');
  if (next && !s.job.cancel_requested) next.state = 'running';
  if (s.job.state === 'pending') s.job.state = 'running';
  s.job.updated_at = now();
  recount(s);
}

function cancelJob(s: StoredJob): void {
  if (['completed', 'partial', 'failed', 'cancelled'].includes(s.job.state)) return;
  s.job.cancel_requested = true;
  for (const it of s.items) if (it.state === 'pending' || it.state === 'running') it.state = 'cancelled';
  s.job.updated_at = now();
  recount(s);
}

const JOB_CSV_COLUMNS = ['project_id', 'job_id', 'item_id', 'input_id', 'uniprot_id', 'start_pos', 'end_pos', 'status', 'error_code', 'domain_status', 'analysis_id'];

function exportJob(s: StoredJob, format: string, deps: WorkspaceDeps): MockResponse {
  const manifest = s.items.map(({ request, ...it }) => ({ ...it, uniprot_id: (request.uniprot_id as string | undefined) ?? null }));
  if (format === 'json') {
    const body = { job: s.job, manifest, analyses: manifest.filter((i) => i.analysis_id).map((i) => analyses.get(i.analysis_id ?? '')) };
    return { status: 200, headers: { 'Content-Type': 'application/json', 'Content-Disposition': `attachment; filename="job-${s.job.job_id}.json"` }, body: JSON.stringify(body) };
  }
  if (format !== 'csv') return deps.err(400, 'INVALID_FORMAT', 'The format must be csv or json.', 'format');
  const lines = ['# synthetic mock export; not model output', JOB_CSV_COLUMNS.join(',')];
  for (const it of manifest) {
    lines.push([s.job.project_id, s.job.job_id, it.item_id, it.input_id, it.uniprot_id ?? '', it.start_pos ?? '', it.end_pos ?? '', it.state, it.error?.code ?? '', it.domain_status ?? '', it.analysis_id ?? ''].map(csvCell).join(','));
  }
  return { status: 200, headers: { 'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': `attachment; filename="job-${s.job.job_id}.csv"` }, body: lines.join('\n') + '\n' };
}

/** Neutralise spreadsheet formulas (SEC-02) and quote when needed. */
function csvCell(v: unknown): string {
  let t = String(v);
  if (/^[=+\-@\t\r]/.test(t)) t = `'${t}`;
  return /[",\n]/.test(t) ? `"${t.replace(/"/g, '""')}"` : t;
}

// --- import -------------------------------------------------------------------------------------------------------

function multipart(body: string, contentType: string): Record<string, string> | null {
  const m = /boundary=(?:"([^"]+)"|([^;]+))/.exec(contentType);
  const boundary = m?.[1] ?? m?.[2];
  if (!boundary) return null;
  const out: Record<string, string> = {};
  for (const part of body.split(`--${boundary}`)) {
    const sep = part.indexOf('\r\n\r\n');
    if (sep < 0) continue;
    const head = part.slice(0, sep);
    const name = /name="([^"]+)"/.exec(head)?.[1];
    if (name) out[name] = part.slice(sep + 4).replace(/\r\n$/, '');
  }
  return out;
}

const COLUMNS = ['peptide_id', 'wt_sequence', 'position', 'wt_aa', 'mut_aa', 'observed_value', 'replicate_id'];

function validate(text: string): { rows: Observation[]; issues: ValidationIssue[]; counts: Record<string, number> } {
  const lines = text.split(/\r?\n/).filter((l) => l.trim() !== '');
  const delim = (lines[0] ?? '').includes('\t') ? '\t' : ',';
  const header = (lines[0] ?? '').split(delim).map((h) => h.trim());
  const issues: ValidationIssue[] = [];
  const counts = { rows: Math.max(lines.length - 1, 0), valid: 0, missing: 0, rejected: 0, duplicate: 0 };
  const missingCols = COLUMNS.filter((c) => !header.includes(c));
  if (missingCols.length) {
    issues.push({ severity: 'error', code: 'MISSING_COLUMN', message: `Missing required column(s): ${missingCols.join(', ')}.` });
    return { rows: [], issues, counts };
  }
  if (lines.length - 1 > MAX_IMPORT_ROWS) issues.push({ severity: 'error', code: 'TOO_MANY_ROWS', message: `At most ${MAX_IMPORT_ROWS} rows.` });
  const col = (cells: string[], name: string) => (cells[header.indexOf(name)] ?? '').trim();
  const rows: Observation[] = [];
  const keys = new Set<string>();
  for (let i = 1; i < lines.length; i += 1) {
    const row = i + 1;
    const cells = (lines[i] ?? '').split(delim);
    const wt = col(cells, 'wt_sequence').toUpperCase();
    const pos = Number(col(cells, 'position'));
    const wtAa = col(cells, 'wt_aa').toUpperCase();
    const mutAa = col(cells, 'mut_aa').toUpperCase();
    const rawValue = col(cells, 'observed_value');
    const reason = header.includes('missing_reason') ? col(cells, 'missing_reason') : '';
    const rep = col(cells, 'replicate_id');
    const reject = (code: string, message: string) => {
      issues.push({ row, severity: 'error', code, message });
      counts.rejected += 1;
    };
    if (wt.length !== 28 || !AA.test(wt)) { reject('INVALID_SEQUENCE', 'wt_sequence must be 28 standard amino acids.'); continue; }
    if (!Number.isInteger(pos) || pos < 1 || pos > 28) { reject('INVALID_POSITION', 'position must be an integer 1…28.'); continue; }
    if (wt[pos - 1] !== wtAa) { reject('WT_MISMATCH', `wt_aa ${wtAa} does not match residue ${pos} of wt_sequence.`); continue; }
    if (!AA.test(mutAa) || mutAa.length !== 1 || mutAa === wtAa) { reject('INVALID_MUTANT', 'mut_aa must be one standard letter different from wt_aa.'); continue; }
    if (!rep) { reject('MISSING_REPLICATE', 'replicate_id is required.'); continue; }
    let value: number | null = null;
    if (rawValue === '') {
      if (!reason) { reject('MISSING_REASON', 'An empty observed_value needs a missing_reason.'); continue; }
      counts.missing += 1;
    } else {
      value = Number(rawValue);
      if (!Number.isFinite(value)) { reject('NONFINITE_VALUE', 'observed_value must be a finite number.'); continue; }
    }
    const key = `${wt}|${pos}|${mutAa}|${rep}`;
    if (keys.has(key)) {
      issues.push({ row, severity: 'error', code: 'DUPLICATE_KEY', message: 'Duplicate (wt_sequence, position, mut_aa, replicate_id); the earlier row is kept.' });
      counts.duplicate += 1;
      continue;
    }
    keys.add(key);
    if (/^[=+\-@]/.test(col(cells, 'peptide_id'))) issues.push({ row, severity: 'warning', code: 'FORMULA_TEXT', message: 'peptide_id starts like a spreadsheet formula; it is stored as text and neutralised on export.' });
    rows.push({ peptide_id: col(cells, 'peptide_id'), wt_sequence: wt, position: pos, wt_aa: wtAa, mut_aa: mutAa, replicate_id: rep, observed_value: value, missing_reason: value === null ? reason : null });
    counts.valid += 1;
  }
  return { rows, issues, counts };
}

function previewImport(projectId: string, body: string, contentType: string, deps: WorkspaceDeps): MockResponse {
  if (body.length > MAX_IMPORT_BYTES) return deps.err(413, 'PAYLOAD_TOO_LARGE', 'The file is larger than 10 MiB.');
  const parts = multipart(body, contentType);
  if (!parts || parts.file === undefined || parts.metadata === undefined) return deps.err(422, 'INVALID_REQUEST', 'Send a multipart form with file and metadata.');
  const meta = parseJson(parts.metadata) as ImportMetadata | null;
  const required = ['name', 'assay', 'endpoint', 'units', 'source', 'reference_description', 'compatibility'] as const;
  const missing = meta ? required.find((k) => !meta[k]) : 'metadata';
  if (!meta || missing) return deps.err(422, 'IMPORT_INVALID', `Metadata field "${missing}" is required.`, `metadata.${missing}`);
  const { rows, issues, counts } = validate(parts.file);
  const revision = 1 + [...datasets.values()].filter((d) => d.dataset.project_id === projectId && d.dataset.metadata.name === meta.name).length;
  const dataset: Dataset = {
    dataset_id: randomUUID(),
    project_id: projectId,
    revision,
    state: 'staged',
    sha256: createHash('sha256').update(parts.file).digest('hex'),
    metadata: meta,
    committable: !issues.some((i) => i.severity === 'error'),
    counts,
    issues,
    created_at: now(),
  };
  datasets.set(dataset.dataset_id, { dataset, rows });
  touch(projectId);
  return deps.ok(dataset, {}, 201);
}

// --- comparison ---------------------------------------------------------------------------------------------------

function ranks(v: number[]): number[] {
  const order = v.map((x, i) => [x, i] as const).sort((a, b) => a[0] - b[0]);
  const r = new Array<number>(v.length);
  for (let i = 0; i < order.length; ) {
    let j = i;
    while (j + 1 < order.length && order[j + 1]![0] === order[i]![0]) j += 1;
    for (let k = i; k <= j; k += 1) r[order[k]![1]] = (i + j) / 2 + 1;
    i = j + 1;
  }
  return r;
}

function spearman(x: number[], y: number[]): number | null {
  if (x.length < 3) return null;
  const rx = ranks(x);
  const ry = ranks(y);
  const mean = (a: number[]) => a.reduce((s, t) => s + t, 0) / a.length;
  const mx = mean(rx);
  const my = mean(ry);
  let num = 0;
  let dx = 0;
  let dy = 0;
  for (let i = 0; i < rx.length; i += 1) {
    num += (rx[i]! - mx) * (ry[i]! - my);
    dx += (rx[i]! - mx) ** 2;
    dy += (ry[i]! - my) ** 2;
  }
  return dx === 0 || dy === 0 ? null : num / Math.sqrt(dx * dy);
}

function compare(a: SavedAnalysis, body: string, deps: WorkspaceDeps): MockResponse {
  const req = parseJson(body);
  if (!req) return deps.err(400, 'INVALID_REQUEST', 'The request body is not valid JSON.');
  const ds = datasets.get(String(req.dataset_id ?? ''));
  if (!ds || ds.dataset.project_id !== a.project_id) return deps.err(404, 'DATASET_NOT_FOUND', 'No dataset with this id in the project.', 'dataset_id');
  if (ds.dataset.state !== 'committed') return deps.err(409, 'DATASET_NOT_COMMITTED', 'Commit the dataset before comparing.', 'dataset_id');
  const rep = typeof req.replicate_id === 'string' ? req.replicate_id : null;
  const agg = req.aggregation === 'mean' || req.aggregation === 'median' ? req.aggregation : null;
  if ((rep === null) === (agg === null)) return deps.err(422, 'INVALID_REQUEST', 'Choose one replicate or one aggregation (mean or median).');
  const seq = a.result.cells.length ? a.result.tile.sequence : '';
  const groups = new Map<string, number[]>();
  let missing = 0;
  let unmatched = 0;
  for (const o of ds.rows) {
    if (rep !== null && o.replicate_id !== rep) continue;
    if (o.wt_sequence !== seq) { unmatched += 1; continue; }
    if (o.observed_value === null) { missing += 1; continue; }
    const k = `${o.position}|${o.mut_aa}`;
    groups.set(k, [...(groups.get(k) ?? []), o.observed_value]);
  }
  const compatible = ds.dataset.metadata.compatibility === 'zhang_gps_dpsi';
  const rows: Record<string, unknown>[] = [];
  const pred: number[] = [];
  const obs: number[] = [];
  for (const c of a.result.cells) {
    const vals = groups.get(`${c.position}|${c.mut_aa}`);
    if (!vals) continue;
    const sorted = [...vals].sort((x, y) => x - y);
    const observed = agg === 'median' ? (sorted.length % 2 ? sorted[(sorted.length - 1) / 2]! : (sorted[sorted.length / 2 - 1]! + sorted[sorted.length / 2]!) / 2) : vals.reduce((s, t) => s + t, 0) / vals.length;
    rows.push({ position: c.position, wt_aa: c.wt_aa, mut_aa: c.mut_aa, observed, n_replicates: vals.length, predicted_dpsi_raw: c.score_dpsi_raw, residual: compatible ? c.score_dpsi_raw - observed : null, units: ds.dataset.metadata.units });
    pred.push(c.score_dpsi_raw);
    obs.push(observed);
  }
  const matched = rows.length;
  let reason: string | null = null;
  if (!compatible) reason = 'The dataset endpoint is not declared comparable with GPS ΔPSI; values are shown in their own units without pooled metrics.';
  else if (matched === 0) reason = 'No observation matches the analysed sequence.';
  const rho = compatible ? spearman(pred, obs) : null;
  if (compatible && matched > 0 && rho === null) reason = 'Spearman needs at least three pairs with varying values.';
  const cmp: Comparison = {
    comparison_id: randomUUID(),
    analysis_id: a.analysis_id,
    dataset_id: ds.dataset.dataset_id,
    compatible,
    matched,
    counts: { matched, unmatched, missing },
    mae: compatible && matched ? pred.reduce((s, p, i) => s + Math.abs(p - obs[i]!), 0) / matched : null,
    spearman: rho,
    metric_unavailable_reason: reason,
    rows,
    provenance: { dataset_revision: ds.dataset.revision, dataset_sha256: ds.dataset.sha256, replicate_id: rep, aggregation: agg, note: 'comparison only; not used to retrain the model' },
  };
  comparisons.set(cmp.comparison_id, cmp);
  return deps.ok(cmp, {}, 201);
}

// --- dispatch -----------------------------------------------------------------------------------------------------

export function handleWorkspace(m: string, url: URL, headers: Record<string, string | undefined>, body: string, deps: WorkspaceDeps): MockResponse | null {
  const path = url.pathname;
  const seg = path.split('/').slice(2); // ['projects', id, ...]
  const top = seg[0];
  if (!['projects', 'analyses', 'jobs', 'datasets', 'comparisons'].includes(top ?? '')) return null;
  const id = seg[1];
  if (id !== undefined && !UUID.test(id)) return deps.err(422, 'INVALID_REQUEST', 'The id is not a UUID.');

  if (top === 'projects') {
    if (id === undefined) {
      if (m === 'GET') return page([...projects.values()].sort((a, b) => b.updated_at.localeCompare(a.updated_at) || a.project_id.localeCompare(b.project_id)).map(counted), url, deps);
      if (m === 'POST') {
        const req = parseJson(body);
        const name = typeof req?.name === 'string' ? req.name.trim() : '';
        if (!name || name.length > 200) return deps.err(422, 'INVALID_REQUEST', 'The name must be 1…200 characters.', 'name');
        const t = now();
        const p: Project = { project_id: randomUUID(), name, description: typeof req?.description === 'string' ? req.description : '', created_at: t, updated_at: t, counts: { analyses: 0, jobs: 0, datasets: 0 } };
        projects.set(p.project_id, p);
        return deps.ok(p, {}, 201);
      }
      return null;
    }
    const p = projects.get(id);
    if (!p) return deps.err(404, 'PROJECT_NOT_FOUND', 'No project with this id.');
    const sub = seg[2];
    if (sub === undefined) {
      if (m === 'GET') return deps.ok(counted(p));
      if (m === 'PATCH') {
        const req = parseJson(body);
        if (!req) return deps.err(400, 'INVALID_REQUEST', 'The request body is not valid JSON.');
        if ('name' in req) {
          const name = typeof req.name === 'string' ? req.name.trim() : '';
          if (!name || name.length > 200) return deps.err(422, 'INVALID_REQUEST', 'The name must be 1…200 characters.', 'name');
          p.name = name;
        }
        if (typeof req.description === 'string') p.description = req.description;
        p.updated_at = now();
        return deps.ok(counted(p));
      }
      if (m === 'DELETE') {
        const c = counted(p).counts;
        const deps409 = confirmRequired(url, deps, { analyses: c.analyses, jobs: c.jobs, datasets: c.datasets, comparisons: [...comparisons.values()].filter((x) => analyses.get(x.analysis_id)?.project_id === id).length });
        if (deps409) return deps409;
        for (const [jid, j] of jobs) if (j.job.project_id === id) { cancelJob(j); jobs.delete(jid); }
        for (const [aid, a] of analyses) if (a.project_id === id) deleteAnalysisCascade(aid);
        for (const [did, d] of datasets) if (d.dataset.project_id === id) deleteDatasetCascade(did);
        projects.delete(id);
        return { status: 204, headers: {}, body: '' };
      }
      return null;
    }
    const byTime = <T extends { created_at: string }>(rows: T[], key: (r: T) => string) => rows.sort((a, b) => b.created_at.localeCompare(a.created_at) || key(a).localeCompare(key(b)));
    if (sub === 'analyses') {
      if (m === 'GET') return page(byTime([...analyses.values()].filter((a) => a.project_id === id), (a) => a.analysis_id).map(summary), url, deps);
      if (m === 'POST') {
        const req = parseJson(body);
        if (!req || typeof req.request !== 'object' || req.request === null) return deps.err(422, 'INVALID_REQUEST', 'Send {request: PredictRequest}.', 'request');
        const parent = typeof req.parent_analysis_id === 'string' ? req.parent_analysis_id : null;
        if (parent !== null && analyses.get(parent)?.project_id !== id) return deps.err(404, 'ANALYSIS_NOT_FOUND', 'The parent analysis is not in this project.', 'parent_analysis_id');
        const r = deps.predict(JSON.stringify(req.request));
        if (!r.ok) return r.response;
        return deps.ok(newAnalysis(id, r.result, r.request, parent), {}, 201);
      }
    }
    if (sub === 'jobs') {
      if (m === 'GET') return page(byTime([...jobs.values()].filter((j) => j.job.project_id === id).map((j) => j.job), (j) => j.job_id), url, deps);
      if (m === 'POST') return submitJob(id, body, deps);
    }
    if (sub === 'datasets') {
      if (m === 'GET') return page(byTime([...datasets.values()].filter((d) => d.dataset.project_id === id).map((d) => d.dataset), (d) => d.dataset_id), url, deps);
      if (m === 'POST') return previewImport(id, body, headers['content-type'] ?? '', deps);
    }
    return null;
  }

  if (id === undefined) return null;

  if (top === 'analyses') {
    const a = analyses.get(id);
    if (!a) return deps.err(404, 'ANALYSIS_NOT_FOUND', 'No saved analysis with this id.');
    const sub = seg[2];
    if (sub === undefined && m === 'GET') return deps.ok({ ...a, parent_available: a.parent_analysis_id ? analyses.has(a.parent_analysis_id) : undefined });
    if (sub === undefined && m === 'DELETE') {
      const deps409 = confirmRequired(url, deps, { comparisons: [...comparisons.values()].filter((c) => c.analysis_id === id).length });
      if (deps409) return deps409;
      deleteAnalysisCascade(id);
      return { status: 204, headers: {}, body: '' };
    }
    if (sub === 'export' && m === 'GET') return deps.exportResult(a.result, url.searchParams.get('format') ?? '');
    if (sub === 'comparisons') {
      if (m === 'GET') return page([...comparisons.values()].filter((c) => c.analysis_id === id), url, deps);
      if (m === 'POST') return compare(a, body, deps);
    }
    return null;
  }

  if (top === 'jobs') {
    const s = jobs.get(id);
    if (!s) return deps.err(404, 'JOB_NOT_FOUND', 'No job with this id.');
    const sub = seg[2];
    if (sub === undefined && m === 'GET') {
      advance(s, deps);
      return deps.ok(s.job);
    }
    if (sub === 'items' && m === 'GET') return page(s.items.map(({ request: _r, ...it }) => it), url, deps);
    if (sub === 'cancel' && m === 'POST') {
      cancelJob(s);
      return deps.ok(s.job, {}, 202);
    }
    if (sub === 'export' && m === 'GET') return exportJob(s, url.searchParams.get('format') ?? '', deps);
    return null;
  }

  if (top === 'datasets') {
    const d = datasets.get(id);
    if (!d) return deps.err(404, 'DATASET_NOT_FOUND', 'No dataset with this id.');
    if (m === 'GET') return deps.ok(d.dataset);
    if (m === 'POST') {
      const req = parseJson(body);
      if (req?.action !== 'commit') return deps.err(422, 'INVALID_REQUEST', 'Send {action: "commit", acknowledge_warnings}.', 'action');
      if (d.dataset.state === 'committed') return deps.ok(d.dataset);
      if (d.dataset.state === 'expired') return deps.err(409, 'IMPORT_EXPIRED', 'This preview has expired; upload the file again.');
      if (!d.dataset.committable) return deps.err(409, 'IMPORT_INVALID', 'Fix the blocking errors before committing.');
      if (d.dataset.issues.some((i) => i.severity === 'warning') && req.acknowledge_warnings !== true) return deps.err(409, 'IMPORT_INVALID', 'Acknowledge the warnings to commit.', 'acknowledge_warnings');
      d.dataset.state = 'committed';
      d.dataset.committed_at = now();
      return deps.ok(d.dataset);
    }
    if (m === 'DELETE') {
      const deps409 = confirmRequired(url, deps, { observations: d.rows.length, comparisons: [...comparisons.values()].filter((c) => c.dataset_id === id).length });
      if (deps409) return deps409;
      deleteDatasetCascade(id);
      return { status: 204, headers: {}, body: '' };
    }
    return null;
  }

  if (top === 'comparisons' && m === 'GET') {
    const c = comparisons.get(id);
    return c ? deps.ok(c) : deps.err(404, 'COMPARISON_NOT_FOUND', 'No comparison with this id.');
  }
  return null;
}
