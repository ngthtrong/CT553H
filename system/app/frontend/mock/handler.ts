/**
 * Mock of the Degron Footprint API, written from openapi.yaml and api-spec.md.
 *
 * ALL NUMBERS HERE ARE SYNTHETIC FIXTURES for developing the interface. They are not model output.
 * The model id, evidence label and card say so on screen, so a mock result cannot pass for a real one.
 * The real service is the FastAPI backend; this file only lets the interface run and be tested without it.
 */

export interface MockResponse {
  status: number;
  headers: Record<string, string>;
  body: string;
}

const AA = 'ACDEFGHIKLMNPQRSTVWY';
const MODEL_ID = 'mock-m3-ext4.0-platt-v1';
const REAL_TILE = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'; // A6NMZ7 tile 28, UniProt 2026_03
export const OUT_OF_DOMAIN_RUN_EXPIRED = '00000000-0000-4000-8000-000000000410';

const PROTEINS = [
  { uniprot_id: 'A6NMZ7', gene_symbol: 'COL6A6', protein_name: 'Collagen alpha-6(VI) chain', length: 2263 },
  { uniprot_id: 'P60484', gene_symbol: 'PTEN', protein_name: 'Phosphatidylinositol 3,4,5-trisphosphate 3-phosphatase and dual-specificity protein phosphatase PTEN', length: 403 },
  { uniprot_id: 'P04637', gene_symbol: 'TP53', protein_name: 'Cellular tumor antigen p53', length: 393 },
];

function nTiles(length: number): number {
  return Math.floor((length - 28) / 23) + 1;
}

function hash(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function unit(s: string): number {
  return hash(s) / 4294967295;
}

type Status = 'measured_in_domain' | 'measured_out_of_domain' | 'measured_unreliable' | 'predicted_in_domain' | 'predicted_out_of_domain' | 'unknown';

interface TileFixture {
  status: Status;
  psi: number | null;
  reads: number | null;
  scorable: boolean;
}

function tileFixture(acc: string, n: number): TileFixture {
  if (acc === 'A6NMZ7') {
    if (n === 28) return { status: 'measured_in_domain', psi: 1.88187026524536, reads: 38.380389871414, scorable: true };
    if (n === 5) return { status: 'measured_out_of_domain', psi: 4.8, reads: 51.2, scorable: true };
    if (n === 7) return { status: 'measured_unreliable', psi: 2.9, reads: 3.1, scorable: true };
    if (n === 9) return { status: 'unknown', psi: null, reads: null, scorable: true };
    if (n === 11) return { status: 'predicted_in_domain', psi: null, reads: null, scorable: true };
    if (n === 12) return { status: 'predicted_out_of_domain', psi: null, reads: null, scorable: true };
    if (n === 3 || n === 4) return { status: 'unknown', psi: null, reads: null, scorable: false };
  }
  const u = unit(`${acc}/${n}`);
  if (u < 0.15) return { status: 'unknown', psi: null, reads: null, scorable: true };
  if (u < 0.3) return { status: 'measured_out_of_domain', psi: 4.2 + u, reads: 40, scorable: true };
  return { status: 'measured_in_domain', psi: 1.2 + 2.6 * u, reads: 30 + 20 * u, scorable: true };
}

function tileSequence(acc: string, n: number): string {
  if (acc === 'A6NMZ7' && n === 28) return REAL_TILE;
  let s = '';
  for (let i = 0; i < 28; i += 1) s += AA.charAt(hash(`${acc}/${n}/${i}`) % 20);
  return s;
}

const SOURCE_ZHANG = {
  source_id: 'zhang2023-mendeley-v2',
  name: 'Zhang et al. 2023 saturation mutagenesis',
  version: 'Mendeley Data v2',
  license_name: 'CC BY 4.0',
  attribution_text: 'Zhang et al. 2023, Mol Cell (doi 10.17632/32h94v2yv2.2)',
};
const SOURCE_CLINVAR = {
  source_id: 'clinvar-2026-10',
  name: 'NCBI ClinVar',
  version: 'variant_summary 2026-10-12',
  license_name: 'NCBI terms of use (attribution required)',
  attribution_text: 'Variants from NCBI ClinVar (Landrum et al.), file of 2026-10-12.',
};
const CLINVAR_DISCLAIMER = 'ClinVar data are not for diagnostic use; they are shown for research only.';

function provenance(extra: { clinvar?: boolean } = {}) {
  return {
    model_id: MODEL_ID,
    model_kind: 'ridge_platt',
    weights_sha256: 'deadbeef'.repeat(8),
    feature_spec: 'm3-180: wt one-hot | mutant one-hot | tile composition | context -3..+3',
    event_definition: 'P(DeltaPSI >= 1.0)',
    evidence_label: 'development OOF benchmark, not external validation (MOCK FIXTURE: synthetic numbers, not model output)',
    domain_description: '28-mer internal tiles, GPS assay (Zhang 2023), intrinsic PSI(WT) <= 4.0',
    data_sources: extra.clinvar ? [SOURCE_ZHANG, SOURCE_CLINVAR] : [SOURCE_ZHANG],
    code_version: 'mock',
    generated_at: new Date().toISOString(),
    disclaimers: extra.clinvar
      ? ['Scores are for the assay and domain on which the model was evaluated. They are not probabilities of disease.', CLINVAR_DISCLAIMER]
      : ['Scores are for the assay and domain on which the model was evaluated. They are not probabilities of disease.'],
  };
}

function err(status: number, code: string, message: string, field: string | null = null, headers: Record<string, string> = {}): MockResponse {
  return { status, headers: { 'Content-Type': 'application/json', 'X-Request-Id': 'mock-req', ...headers }, body: JSON.stringify({ code, message, field }) };
}

function ok(body: unknown, headers: Record<string, string> = {}, status = 200): MockResponse {
  return { status, headers: { 'Content-Type': 'application/json', 'X-Request-Id': 'mock-req', ...headers }, body: JSON.stringify(body) };
}

interface Cell {
  position: number;
  wt_aa: string;
  mut_aa: string;
  score_dpsi_raw: number;
  p_dpsi_ge_1_calibrated: number;
  rank_in_tile: number;
  top10pct_in_tile: boolean;
}

const REAL_FIRST = [
  { mut: 'A', s: -0.04768813161, p: 0.02801670181 },
  { mut: 'C', s: -0.1650532933, p: 0.01836623325 },
  { mut: 'E', s: 0.1907540759, p: 0.06485567777 },
];

function makeCells(seq: string, real: boolean): Cell[] {
  const cells: Cell[] = [];
  for (let i = 0; i < 28; i += 1) {
    const wt = seq.charAt(i);
    for (const aa of AA) {
      if (aa === wt) continue;
      let s = (unit(`${seq}|${i}|${aa}`) - 0.45) * 2.4;
      let p = 1 / (1 + Math.exp(-(2.2 * s - 2.3)));
      const r = real && i === 0 ? REAL_FIRST.find((x) => x.mut === aa) : undefined;
      if (r) {
        s = r.s;
        p = r.p;
      }
      cells.push({ position: i + 1, wt_aa: wt, mut_aa: aa, score_dpsi_raw: s, p_dpsi_ge_1_calibrated: p, rank_in_tile: 0, top10pct_in_tile: false });
    }
  }
  const order = [...cells].sort((a, b) => b.score_dpsi_raw - a.score_dpsi_raw);
  order.forEach((c, i) => {
    c.rank_in_tile = i + 1;
    c.top10pct_in_tile = i + 1 <= 54;
  });
  return cells;
}

const WARN = {
  DOMAIN_UNKNOWN: 'The domain of this tile is unknown. The model was trained only on tiles that behave as degrons (wild-type PSI <= 4.0) and cannot check this one.',
  DOMAIN_UNRELIABLE: 'The measurement of this tile rests on too few reads; whether it is in the domain is uncertain.',
  PREDICTED_DOMAIN: 'The domain status of this tile was predicted by a gate model, not measured.',
  TRAINING_PEPTIDE: 'This tile is among the peptides the model was trained on; its scores are not an out-of-sample estimate.',
  OUT_OF_DOMAIN_OVERRIDDEN: 'This tile is outside the domain of the model and was scored by explicit override. The numbers are not meaningful.',
};

const ACC_RE = /^([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$/;
const KNOWN_FIELDS = new Set(['sequence', 'uniprot_id', 'tile_index', 'model_id', 'calibrator', 'override_domain', 'ttl_days', 'format']);

type Parsed = { ok: true; result: unknown; request: Record<string, unknown> } | { ok: false; response: MockResponse };

function runPredict(body: string, extraFields: string[] = []): Parsed {
  if (body.length > 4096) return { ok: false, response: err(413, 'PAYLOAD_TOO_LARGE', 'The request is larger than 4 KiB.') };
  let req: Record<string, unknown>;
  try {
    const parsed: unknown = JSON.parse(body);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('not an object');
    req = parsed as Record<string, unknown>;
  } catch {
    return { ok: false, response: err(400, 'INVALID_REQUEST', 'The request body is not valid JSON.') };
  }
  for (const k of Object.keys(req)) {
    if (!KNOWN_FIELDS.has(k) || (!['sequence', 'uniprot_id', 'tile_index', 'model_id', 'calibrator', 'override_domain'].includes(k) && !extraFields.includes(k))) {
      return { ok: false, response: err(422, 'INVALID_REQUEST', `Unknown field "${k}".`, k) };
    }
  }
  const hasSeq = 'sequence' in req;
  const hasAcc = 'uniprot_id' in req || 'tile_index' in req;
  if (hasSeq === hasAcc || (hasAcc && !('uniprot_id' in req && 'tile_index' in req))) {
    return { ok: false, response: err(422, 'INVALID_REQUEST', 'Give either a sequence, or a UniProt accession together with a tile index.') };
  }
  if ('model_id' in req && req.model_id !== MODEL_ID) {
    return { ok: false, response: err(404, 'MODEL_NOT_FOUND', 'No frozen effect model has this id.', 'model_id') };
  }
  const override = req.override_domain === true;

  let seq: string;
  let tileInfo: Record<string, unknown>;
  let fx: TileFixture | null = null;
  let acc = '';
  let n = 0;
  if (hasSeq) {
    seq = String(req.sequence).trim().toUpperCase();
    if (seq.length !== 28) return { ok: false, response: err(422, 'INVALID_LENGTH', `The sequence must have exactly 28 amino acids; it has ${seq.length}.`, 'sequence') };
    const bad = [...seq].findIndex((c) => !AA.includes(c));
    if (bad >= 0) return { ok: false, response: err(422, 'INVALID_CHARACTER', `Position ${bad + 1}: '${seq.charAt(bad)}' is not a standard amino acid.`, 'sequence') };
    tileInfo = { uniprot_id: null, tile_index: null, start_pos: null, end_pos: null, sequence: seq };
  } else {
    acc = String(req.uniprot_id);
    if (!ACC_RE.test(acc)) return { ok: false, response: err(422, 'INVALID_REQUEST', 'This is not a UniProt accession.', 'uniprot_id') };
    const p = PROTEINS.find((x) => x.uniprot_id === acc);
    if (!p) return { ok: false, response: err(404, 'UNKNOWN_ACCESSION', `No reviewed human protein has the accession ${acc}.`, 'uniprot_id') };
    n = Number(req.tile_index);
    const max = nTiles(p.length);
    if (!Number.isInteger(n) || n < 1 || n > max) return { ok: false, response: err(422, 'TILE_OUT_OF_RANGE', `Tile ${String(req.tile_index)} does not exist; ${acc} has tiles 1 to ${max}.`, 'tile_index') };
    fx = tileFixture(acc, n);
    if (!fx.scorable) return { ok: false, response: err(422, 'TILE_NOT_SCORABLE', 'This tile cannot be scored because it contains a non-standard residue.', 'tile_index') };
    seq = tileSequence(acc, n);
    tileInfo = { uniprot_id: acc, tile_index: n, start_pos: (n - 1) * 23 + 1, end_pos: (n - 1) * 23 + 28, sequence: seq };
  }

  const status: Status = fx?.status ?? 'unknown';
  const warnings: { code: string; message: string }[] = [];
  if (status === 'measured_out_of_domain' || status === 'predicted_out_of_domain') {
    if (!override) {
      return {
        ok: false,
        response: err(422, 'OUT_OF_DOMAIN', `The wild-type PSI of this tile (${fx?.psi !== null && fx?.psi !== undefined ? fx.psi.toFixed(1) : 'predicted'}) is above the 4.0 limit of the training domain. Set override_domain to true to score it anyway.`),
      };
    }
    warnings.push({ code: 'OUT_OF_DOMAIN_OVERRIDDEN', message: WARN.OUT_OF_DOMAIN_OVERRIDDEN });
  }
  if (status === 'unknown') warnings.push({ code: 'DOMAIN_UNKNOWN', message: WARN.DOMAIN_UNKNOWN });
  if (status === 'measured_unreliable') warnings.push({ code: 'DOMAIN_UNRELIABLE', message: WARN.DOMAIN_UNRELIABLE });
  if (status.startsWith('predicted')) warnings.push({ code: 'PREDICTED_DOMAIN', message: WARN.PREDICTED_DOMAIN });
  const training = acc === 'A6NMZ7' && n === 28;
  if (training) warnings.push({ code: 'TRAINING_PEPTIDE', message: WARN.TRAINING_PEPTIDE });

  const message =
    status === 'measured_in_domain' ? 'Tile PSI measured in the GPS peptidome screen (replicate 1).'
    : status === 'unknown' ? 'No measurement or gate model covers this tile.'
    : status === 'measured_unreliable' ? 'Measured, but with too few reads to be reliable.'
    : status === 'measured_out_of_domain' ? 'Tile PSI measured in the GPS peptidome screen; above the training limit.'
    : 'Predicted by a gate model.';

  return {
    ok: true,
    request: req,
    result: {
      provenance: provenance(),
      tile: tileInfo,
      domain: { status, psi_wt_measured: fx?.psi ?? null, reads_measured: fx?.reads ?? null, gate_model_id: status.startsWith('predicted') ? 'mock-gate-r3-candidate' : null, message },
      warnings,
      cells: makeCells(seq, training),
    },
  };
}

function csvOf(result: { provenance: ReturnType<typeof provenance>; tile: { uniprot_id: string | null; tile_index: number | null }; domain: { status: string }; warnings: { code: string; message: string }[]; cells: Cell[] }): string {
  const p = result.provenance;
  const peptide = result.tile.uniprot_id ? `${result.tile.uniprot_id}_${result.tile.tile_index}` : 'user_seq';
  const lines = [
    `# model_id=${p.model_id}`,
    `# weights_sha256=${p.weights_sha256}`,
    `# event_definition=${p.event_definition}`,
    `# evidence_label=${p.evidence_label}`,
    `# domain_status=${result.domain.status}`,
    ...result.warnings.map((w) => `# warning=${w.code}`),
    `# data_sources=${p.data_sources.map((s) => s.source_id).join(',')}`,
    `# generated_at=${p.generated_at}`,
    '# disclaimer=Not a probability of disease; not for diagnostic use.',
    'peptide,tile,position,wt_aa,mut_aa,score_dpsi_raw,p_dpsi_ge_1_calibrated,rank_in_tile,top10pct_in_tile',
    ...result.cells.map((c) => `${peptide},${result.tile.tile_index ?? 0},${c.position},${c.wt_aa},${c.mut_aa},${c.score_dpsi_raw.toPrecision(10)},${c.p_dpsi_ge_1_calibrated.toPrecision(10)},${c.rank_in_tile},${c.top10pct_in_tile ? 1 : 0}`),
  ];
  return `${lines.join('\n')}\n`;
}

function fileResponse(result: ReturnType<typeof makePredictionForExport>, format: string): MockResponse {
  if (format === 'csv') return { status: 200, headers: { 'Content-Type': 'text/csv; charset=utf-8', 'X-Request-Id': 'mock-req' }, body: csvOf(result) };
  return ok({ ...result, exported_at: new Date().toISOString() });
}
type ExportShape = Parameters<typeof csvOf>[0];
function makePredictionForExport(r: unknown): ExportShape {
  return r as ExportShape;
}

interface StoredRun {
  result: unknown;
  token: string;
  expires: string;
}
const runs = new Map<string, StoredRun>();

export function resetMock(): void {
  runs.clear();
}

function randomToken(): string {
  const bytes = new Uint8Array(24);
  crypto.getRandomValues(bytes);
  return Buffer.from(bytes).toString('base64url');
}

export function handle(method: string, rawUrl: string, headers: Record<string, string | undefined>, bodyText: string): MockResponse {
  const url = new URL(rawUrl, 'http://mock.local');
  const path = url.pathname;
  const m = method.toUpperCase();
  const get = (name: string) => headers[name.toLowerCase()] ?? headers[name];

  if (path === '/healthz' && m === 'GET') return ok({ status: 'ok', version: 'mock', model_loaded: true, default_model_id: MODEL_ID, database: 'ok' });

  if (path === '/v1/predict' && m === 'POST') {
    const r = runPredict(bodyText);
    return r.ok ? ok(r.result, { 'Cache-Control': 'no-store' }) : r.response;
  }

  if (path === '/v1/export' && m === 'POST') {
    const r = runPredict(bodyText, ['format']);
    if (!r.ok) return r.response;
    const fmt = String(r.request.format ?? '');
    if (fmt !== 'csv' && fmt !== 'json') return err(400, 'INVALID_FORMAT', 'The format must be csv or json.', 'format');
    return fileResponse(makePredictionForExport(r.result), fmt);
  }

  if (path === '/v1/proteins' && m === 'GET') {
    const q = (url.searchParams.get('query') ?? '').trim();
    if (q.length < 2 || q.length > 32) return err(422, 'INVALID_REQUEST', 'The query must have 2 to 32 characters.', 'query');
    const needle = q.toUpperCase();
    const items = PROTEINS.filter((p) => (p.gene_symbol ?? '').startsWith(needle) || p.uniprot_id.startsWith(needle)).map((p) => ({ ...p, n_tiles: nTiles(p.length) }));
    return ok({ items });
  }

  const tiles = /^\/v1\/proteins\/([^/]+)\/tiles$/.exec(path);
  if (tiles && m === 'GET') {
    const acc = decodeURIComponent(tiles[1] ?? '');
    const p = PROTEINS.find((x) => x.uniprot_id === acc);
    if (!p) return err(404, 'UNKNOWN_ACCESSION', `No reviewed human protein has the accession ${acc}.`);
    const list = Array.from({ length: nTiles(p.length) }, (_, i) => {
      const n = i + 1;
      const f = tileFixture(acc, n);
      return { tile_index: n, start_pos: i * 23 + 1, end_pos: i * 23 + 28, sequence: tileSequence(acc, n), scorable: f.scorable, domain_status: f.status, psi_wt_measured: f.psi, reads_measured: f.reads };
    });
    return ok({ protein: { ...p, n_tiles: list.length }, tiles: list, provenance: provenance() });
  }

  const overlay = /^\/v1\/proteins\/([^/]+)\/tiles\/(\d+)\/(measured|clinvar)$/.exec(path);
  if (overlay && m === 'GET') {
    const acc = decodeURIComponent(overlay[1] ?? '');
    const n = Number(overlay[2]);
    const p = PROTEINS.find((x) => x.uniprot_id === acc);
    if (!p) return err(404, 'UNKNOWN_ACCESSION', `No reviewed human protein has the accession ${acc}.`);
    if (n < 1 || n > nTiles(p.length)) return err(404, 'TILE_OUT_OF_RANGE', `Tile ${n} does not exist.`);
    const tile = { uniprot_id: acc, tile_index: n, start_pos: (n - 1) * 23 + 1, end_pos: (n - 1) * 23 + 28, sequence: tileSequence(acc, n) };
    const training = acc === 'A6NMZ7' && n === 28;
    if (overlay[3] === 'measured') {
      const cells = training
        ? [3, 7, 10, 14, 17, 20, 25].flatMap((pos) => ['A', 'W', 'R'].filter((a) => a !== REAL_TILE.charAt(pos - 1)).map((a) => ({ position: pos, mut_aa: a, delta_psi: Number(((unit(`m${pos}${a}`) - 0.3) * 2.2).toFixed(2)), in_training_set: true })))
        : [];
      return ok({ tile, cells, provenance: provenance() });
    }
    const variants = training
      ? [
          { variation_id: 900001, protein_pos: 635, position: 14, ref_aa: 'P', alt_aa: 'L', clinsig: 'likely_benign', review_status: 'criteria provided, single submitter', last_evaluated: '2024-03-01' },
          { variation_id: 900002, protein_pos: 631, position: 10, ref_aa: 'G', alt_aa: 'R', clinsig: 'pathogenic', review_status: 'criteria provided, multiple submitters', last_evaluated: '2025-01-15' },
          { variation_id: 900003, protein_pos: 628, position: 7, ref_aa: 'D', alt_aa: 'N', clinsig: 'vus', review_status: 'criteria provided, single submitter', last_evaluated: '2023-11-20' },
          { variation_id: 900004, protein_pos: 641, position: 20, ref_aa: 'M', alt_aa: 'V', clinsig: 'benign', review_status: 'reviewed by expert panel', last_evaluated: '2022-06-09' },
          { variation_id: 900005, protein_pos: 638, position: 17, ref_aa: 'F', alt_aa: 'L', clinsig: 'conflicting', review_status: 'conflicting classifications', last_evaluated: '2024-09-30' },
          { variation_id: 900006, protein_pos: 625, position: 4, ref_aa: 'F', alt_aa: 'S', clinsig: 'likely_pathogenic', review_status: 'criteria provided, single submitter', last_evaluated: '2025-05-05' },
        ]
      : [];
    return ok({ tile, variants, clinvar_file_date: '2026-10-12', provenance: provenance({ clinvar: true }) });
  }

  if (path === '/v1/models' && m === 'GET') {
    return ok({
      items: [
        { model_id: MODEL_ID, role: 'effect', kind: 'ridge_platt', status: 'frozen', is_default: true },
        { model_id: 'mock-gate-r3-candidate', role: 'gate', kind: 'ridge', status: 'candidate', is_default: false },
      ],
    });
  }
  const model = /^\/v1\/models\/([^/]+)$/.exec(path);
  if (model && m === 'GET') {
    const id = decodeURIComponent(model[1] ?? '');
    if (id !== MODEL_ID) return err(404, 'MODEL_NOT_FOUND', 'No model has this id.');
    return ok({
      model_id: MODEL_ID,
      role: 'effect',
      kind: 'ridge_platt',
      status: 'frozen',
      is_default: true,
      weights_sha256: 'deadbeef'.repeat(8),
      event_definition: 'P(DeltaPSI >= 1.0)',
      domain_description: '28-mer internal tiles, GPS assay (Zhang 2023), intrinsic PSI(WT) <= 4.0',
      evidence_label: 'development OOF benchmark, not external validation (MOCK FIXTURE: synthetic numbers, not model output)',
      metrics: { oof_auroc: { estimate: 0.8208 }, brier: { platt: 0.0925, raw: 0.1272 }, top10_enrichment: { estimate: 4.02, ci95: [3.7, 4.35] } },
      metrics_source_file: 'calibration-p6-2026-10-22/results.json (values copied for interface development)',
      calibration: { method: 'platt', event: 'P(DeltaPSI >= 1.0)' },
      trained_on_sources: [SOURCE_ZHANG],
      card_markdown: [
        '# Mock model card',
        'This card is a fixture for developing the interface. The numbers are not produced by the running service.',
        '## Known limitations',
        '- Probabilities are about 13 % low on the original domain.',
        '- Development benchmark; no external validation exists.',
      ].join('\n'),
      not_used_sources: [
        { source_id: 'koren2018-nihms967427', name: 'Koren et al. 2018, Cell, Table S4', reason: 'No open licence, internal use only; it failed the data gate (5 new clusters against 20 required).' },
        { source_id: 'metadegron', name: 'MetaDegron tables and ELM-derived degron motifs', reason: 'Repository without a licence; labels are binary, not DeltaPSI.' },
        { source_id: 'elm-academic', name: 'ELM database (degron motif instances)', reason: 'Academic licence; internal provenance checks only.' },
        { source_id: 'larsen2025-github', name: 'Larsen et al. 2025, transcription-factor tiles', reason: 'Licence of the data files unconfirmed.' },
      ],
      frozen_at: '2026-10-22T00:00:00Z',
    });
  }

  if (path === '/v1/sources' && m === 'GET') {
    return ok({
      items: [
        { ...SOURCE_ZHANG, citation: 'Zhang et al. 2023', url: 'https://doi.org/10.17632/32h94v2yv2.2', disclaimer_text: null },
        { source_id: 'uniprot-2026-03', name: 'UniProtKB/Swiss-Prot', version: 'release 2026_03', citation: 'UniProt Consortium', url: 'https://www.uniprot.org', license_name: 'CC BY 4.0', attribution_text: 'UniProt Consortium, UniProtKB/Swiss-Prot 2026_03.', disclaimer_text: null },
        { ...SOURCE_CLINVAR, citation: 'Landrum et al.', url: 'https://www.ncbi.nlm.nih.gov/clinvar/', disclaimer_text: CLINVAR_DISCLAIMER },
      ],
    });
  }

  if (path === '/v1/runs' && m === 'POST') {
    const r = runPredict(bodyText, ['ttl_days']);
    if (!r.ok) return r.response;
    const days = Number(r.request.ttl_days ?? 7);
    const id = crypto.randomUUID();
    const token = randomToken();
    const expires = new Date(Date.now() + days * 86_400_000).toISOString();
    runs.set(id, { result: r.result, token, expires });
    return ok({ run_id: id, share_token: token, expires_at: expires, result: r.result }, {}, 201);
  }

  const run = /^\/v1\/runs\/([^/]+)(\/export)?$/.exec(path);
  if (run && m === 'GET') {
    const id = decodeURIComponent(run[1] ?? '');
    const token = get('x-share-token');
    if (!token) return err(401, 'TOKEN_REQUIRED', 'A share token is required.');
    if (id === OUT_OF_DOMAIN_RUN_EXPIRED) return err(410, 'RUN_EXPIRED', 'This shared result has expired.');
    const stored = runs.get(id);
    if (!stored || stored.token !== token) return err(404, 'RUN_NOT_FOUND', 'No shared result matches this link.');
    if (run[2]) {
      const fmt = url.searchParams.get('format');
      if (fmt !== 'csv' && fmt !== 'json') return err(400, 'INVALID_FORMAT', 'The format must be csv or json.', 'format');
      return fileResponse(makePredictionForExport(stored.result), fmt);
    }
    return ok(stored.result);
  }

  return err(404, 'INVALID_REQUEST', 'No such endpoint.');
}
