/**
 * The mock of the 24 planned workspace operations (mock/workspace.ts, implementation plan WP3.4). The screens of WP9
 * are developed against it, so its behaviour has to follow api-spec.md §4–§7 closely enough to be worth testing.
 */
import { describe, expect, it } from 'vitest';
import { handle } from '../mock/handler';

const SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV';

function call(method: string, url: string, body?: unknown, headers: Record<string, string> = {}) {
  const text = body === undefined ? '' : typeof body === 'string' ? body : JSON.stringify(body);
  const out = handle(method, url, { 'content-type': 'application/json', ...headers }, text);
  const json = out.body && out.headers['Content-Type']?.startsWith('application/json') ? JSON.parse(out.body) : null;
  return { status: out.status, json, text: out.body, headers: out.headers };
}

function project(name = 'Screen follow-up') {
  const r = call('POST', '/v1/projects', { name });
  expect(r.status).toBe(201);
  return r.json.project_id as string;
}

function upload(pid: string, csv: string, meta: Record<string, unknown> = {}) {
  const b = 'XBOUNDARY';
  const metadata = { name: 'gps-rep', assay: 'GPS', endpoint: 'delta_psi', units: 'PSI', source: 'lab notebook 12', reference_description: 'A6NMZ7 tile 28', compatibility: 'zhang_gps_dpsi', ...meta };
  const body = `--${b}\r\nContent-Disposition: form-data; name="metadata"\r\n\r\n${JSON.stringify(metadata)}\r\n--${b}\r\nContent-Disposition: form-data; name="file"; filename="obs.csv"\r\nContent-Type: text/csv\r\n\r\n${csv}\r\n--${b}--\r\n`;
  return call('POST', `/v1/projects/${pid}/datasets`, body, { 'content-type': `multipart/form-data; boundary=${b}` });
}

describe('projects (UC-10)', () => {
  it('creates, lists with counts, renames and refuses bad names', () => {
    const pid = project();
    expect(call('POST', '/v1/projects', { name: '' }).status).toBe(422);
    expect(call('PATCH', `/v1/projects/${pid}`, { name: 'Renamed' }).json.name).toBe('Renamed');
    const list = call('GET', '/v1/projects?limit=10');
    expect(list.json).toMatchObject({ total: 1, offset: 0, limit: 10 });
    expect(list.json.items[0].counts).toEqual({ analyses: 0, jobs: 0, datasets: 0 });
    expect(call('GET', '/v1/projects?limit=201').status).toBe(422);
    expect(call('GET', '/v1/projects/not-a-uuid').status).toBe(422);
  });

  it('deletes only after confirmation and reports dependencies first (HIST-03)', () => {
    const pid = project();
    call('POST', `/v1/projects/${pid}/analyses`, { request: { sequence: SEQ } });
    const first = call('DELETE', `/v1/projects/${pid}`);
    expect(first.status).toBe(409);
    expect(first.json.code).toBe('CONFIRMATION_REQUIRED');
    expect(first.json.dependencies.analyses).toBe(1);
    expect(call('GET', `/v1/projects/${pid}`).status).toBe(200);
    expect(call('DELETE', `/v1/projects/${pid}?confirm=true`).status).toBe(204);
    expect(call('GET', `/v1/projects/${pid}`).json.code).toBe('PROJECT_NOT_FOUND');
  });
});

describe('analyses (FR-32)', () => {
  it('saves a snapshot, reruns as a new record and flags a deleted parent', () => {
    const pid = project();
    const a = call('POST', `/v1/projects/${pid}/analyses`, { request: { sequence: SEQ } }).json;
    expect(a.result.cells).toHaveLength(532);
    const b = call('POST', `/v1/projects/${pid}/analyses`, { request: { sequence: SEQ }, parent_analysis_id: a.analysis_id }).json;
    expect(b.analysis_id).not.toBe(a.analysis_id);
    expect(b.parent_analysis_id).toBe(a.analysis_id);
    call('DELETE', `/v1/analyses/${a.analysis_id}?confirm=true`);
    expect(call('GET', `/v1/analyses/${b.analysis_id}`).json.parent_available).toBe(false);
    expect(call('GET', `/v1/analyses/${b.analysis_id}/export?format=csv`).text).toContain('score_dpsi_raw');
  });
});

describe('jobs (UC-08)', () => {
  it('runs a peptide batch to partial, keeping refused inputs in the manifest', () => {
    const pid = project();
    const sub = call('POST', `/v1/projects/${pid}/jobs`, { mode: 'peptides', peptides: [{ input_id: 'ok', sequence: SEQ }, { input_id: 'short', sequence: 'ACD' }] });
    expect(sub.status).toBe(202);
    expect(sub.json.counts).toEqual({ pending: 1, refused: 1 });
    let job = sub.json;
    for (let i = 0; i < 5 && !['completed', 'partial', 'failed'].includes(job.state); i += 1) job = call('GET', `/v1/jobs/${job.job_id}`).json;
    expect(job.state).toBe('partial');
    const items = call('GET', `/v1/jobs/${job.job_id}/items`).json.items;
    expect(items.map((i: { state: string }) => i.state)).toEqual(['succeeded', 'refused']);
    expect(items[1].error.code).toBe('INVALID_LENGTH');
    const csv = call('GET', `/v1/jobs/${job.job_id}/export?format=csv`).text;
    expect(csv.trim().split('\n')).toHaveLength(4); // comment, header, two manifest rows
  });

  it('tiles a protein with step 23 and reports the uncovered C-terminal residues (BATCH-04)', () => {
    const pid = project();
    // PTEN, 403 residues: tiles = (403-28)//23+1 = 17, last end = 16*23+28 = 396 → 397…403 uncovered
    const job = call('POST', `/v1/projects/${pid}/jobs`, { mode: 'protein', protein: { uniprot_id: 'P60484' } }).json;
    expect(job.total).toBe(17);
    expect(job.coverage.uncovered).toEqual([{ start: 397, end: 403 }]);
    const items = call('GET', `/v1/jobs/${job.job_id}/items?limit=200`).json.items;
    expect(items[1]).toMatchObject({ tile_index: 2, start_pos: 24, end_pos: 51 });
  });

  it('cancels idempotently and keeps finished items (BATCH-03)', () => {
    const pid = project();
    const peptides = Array.from({ length: 4 }, (_, i) => ({ input_id: `p${i}`, sequence: SEQ }));
    const job = call('POST', `/v1/projects/${pid}/jobs`, { mode: 'peptides', peptides }).json;
    call('GET', `/v1/jobs/${job.job_id}`);
    call('GET', `/v1/jobs/${job.job_id}`); // first item done, second running
    const c1 = call('POST', `/v1/jobs/${job.job_id}/cancel`).json;
    const c2 = call('POST', `/v1/jobs/${job.job_id}/cancel`).json;
    expect(c1.state).toBe('cancelled');
    expect(c2).toEqual(c1);
    expect(c1.counts).toEqual({ succeeded: 1, cancelled: 3 });
  });

  it('rejects more than 100 peptides and a protein shorter than one tile', () => {
    const pid = project();
    const many = Array.from({ length: 101 }, (_, i) => ({ input_id: `p${i}`, sequence: SEQ }));
    expect(call('POST', `/v1/projects/${pid}/jobs`, { mode: 'peptides', peptides: many }).status).toBe(413);
    expect(call('POST', `/v1/projects/${pid}/jobs`, { mode: 'protein', protein: { input_id: 'x', sequence: 'A'.repeat(27) } }).json.code).toBe('INVALID_LENGTH');
  });
});

describe('import and comparison (UC-05, UC-09)', () => {
  const header = 'peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id,missing_reason';

  it('blocks commit on errors and never fills a missing value with zero (IMP-01/02)', () => {
    const pid = project();
    const csv = [header, `p,${SEQ},1,D,A,0.5,r1,`, `p,${SEQ},1,X,A,0.5,r1,`, `p,${SEQ},2,I,A,,r1,`, `p,${SEQ},1,D,A,0.7,r1,`].join('\n');
    const d = upload(pid, csv).json;
    expect(d.state).toBe('staged');
    expect(d.committable).toBe(false);
    expect(d.counts).toMatchObject({ rows: 4, valid: 1, rejected: 2, duplicate: 1 });
    expect(d.issues.map((i: { code: string }) => i.code).sort()).toEqual(['DUPLICATE_KEY', 'MISSING_REASON', 'WT_MISMATCH']);
    expect(call('POST', `/v1/datasets/${d.dataset_id}`, { action: 'commit', acknowledge_warnings: true }).json.code).toBe('IMPORT_INVALID');
  });

  it('a second upload of the same name is a new revision', () => {
    const pid = project();
    const csv = [header, `p,${SEQ},1,D,A,0.5,r1,`].join('\n');
    expect(upload(pid, csv).json.revision).toBe(1);
    expect(upload(pid, csv).json.revision).toBe(2);
  });

  it('computes MAE, Spearman and residuals that match a hand calculation', () => {
    const pid = project();
    const a = call('POST', `/v1/projects/${pid}/analyses`, { request: { sequence: SEQ } }).json;
    const cells = a.result.cells.filter((c: { position: number }) => c.position <= 2).slice(0, 4) as { position: number; wt_aa: string; mut_aa: string; score_dpsi_raw: number }[];
    // replicate r1 = 2p + 1 (monotonic in p, so Spearman = 1); r2 = 2p + 3. mean = 2p + 2, median of two = 2p + 2.
    const rows = cells.flatMap((c) => [`p,${SEQ},${c.position},${c.wt_aa},${c.mut_aa},${2 * c.score_dpsi_raw + 1},r1,`, `p,${SEQ},${c.position},${c.wt_aa},${c.mut_aa},${2 * c.score_dpsi_raw + 3},r2,`]);
    const d = upload(pid, [header, ...rows].join('\n')).json;
    expect(call('POST', `/v1/analyses/${a.analysis_id}/comparisons`, { dataset_id: d.dataset_id, aggregation: 'mean' }).json.code).toBe('DATASET_NOT_COMMITTED');
    expect(call('POST', `/v1/datasets/${d.dataset_id}`, { action: 'commit', acknowledge_warnings: true }).json.state).toBe('committed');

    const r1 = call('POST', `/v1/analyses/${a.analysis_id}/comparisons`, { dataset_id: d.dataset_id, replicate_id: 'r1' }).json;
    const handMae = cells.reduce((s, c) => s + Math.abs(c.score_dpsi_raw - (2 * c.score_dpsi_raw + 1)), 0) / cells.length;
    expect(r1.matched).toBe(4);
    expect(r1.mae).toBeCloseTo(handMae, 12);
    expect(r1.spearman).toBeCloseTo(1, 12);
    expect(r1.rows[0].residual).toBeCloseTo(cells[0]!.score_dpsi_raw - (2 * cells[0]!.score_dpsi_raw + 1), 12);

    const mean = call('POST', `/v1/analyses/${a.analysis_id}/comparisons`, { dataset_id: d.dataset_id, aggregation: 'median' }).json;
    expect(mean.rows[0].observed).toBeCloseTo(2 * cells[0]!.score_dpsi_raw + 2, 12);
    expect(mean.rows[0].n_replicates).toBe(2);
    expect(mean.provenance.note).toBe('comparison only; not used to retrain the model');
    expect(call('GET', `/v1/comparisons/${mean.comparison_id}`).json).toEqual(mean);
  });

  it('keeps an incompatible endpoint in its own units with no pooled metric (IMP-04)', () => {
    const pid = project();
    const a = call('POST', `/v1/projects/${pid}/analyses`, { request: { sequence: SEQ } }).json;
    const c = a.result.cells[0];
    const d = upload(pid, [header, `p,${SEQ},${c.position},${c.wt_aa},${c.mut_aa},12.5,r1,`].join('\n'), { compatibility: 'other', units: 'half-life (h)' }).json;
    call('POST', `/v1/datasets/${d.dataset_id}`, { action: 'commit', acknowledge_warnings: true });
    const cmp = call('POST', `/v1/analyses/${a.analysis_id}/comparisons`, { dataset_id: d.dataset_id, replicate_id: 'r1' }).json;
    expect(cmp).toMatchObject({ compatible: false, mae: null, spearman: null, matched: 1 });
    expect(cmp.rows[0]).toMatchObject({ residual: null, units: 'half-life (h)' });
    expect(cmp.metric_unavailable_reason).toMatch(/not declared comparable/);
  });
});
