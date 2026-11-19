"""Self-contained HTML report of one saved analysis (plan-system 3.5).

Built from the stored snapshot only (A-6): the same numbers, warnings and provenance as the screen and the exports.
Reading order follows the interface (ui-design §3.3, R-1): limitations, domain and warnings come before any number.
No script, no external resource (RPT-03): styles are inline, the matrix and footprint are inline SVG, and the response
carries its own Content-Security-Policy. Printing to PDF is left to the browser (print stylesheet); no server-side PDF
renderer is installed (DEVIATIONS §14).

Colours: probability uses reversed Viridis through 11 fixed stops (the interface interpolates d3's 256-colour ramp, so
shades may differ slightly); WT cells are hatched; values are always printed in the tables.
"""
from __future__ import annotations

from datetime import UTC, datetime
from html import escape
from typing import Any

from degron_footprint.constants import DISCLAIMER_EXPORT, TOP_K

AMINO = 'ACDEFGHIKLMNPQRSTVWY'
# matplotlib/d3 Viridis at t = 0, 0.1, …, 1
VIRIDIS = ['#440154', '#482475', '#414487', '#355f8d', '#2a788e', '#21918c', '#22a884', '#44bf70', '#7ad151',
           '#bddf26', '#fde725']
REPORT_CSP = ("default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'; "
              "frame-ancestors 'none'")
# A <meta> policy cannot carry frame-ancestors (browsers ignore it and warn); the HTTP header keeps it.
REPORT_CSP_META = "default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'"
SPREAD_LABEL = ('Spread between the 3 training seeds of the ensemble (population SD of their raw scores) — not a '
                'confidence interval and not a prediction error.')


def _hex(c: str) -> tuple[int, int, int]:
    return int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)


def prob_color(p: float) -> str:
    """Reversed Viridis: 0 → light yellow, 1 → dark purple (ui-design §5)."""
    t = 1.0 - min(1.0, max(0.0, p))
    i = min(9, int(t * 10))
    f = t * 10 - i
    a, b = _hex(VIRIDIS[i]), _hex(VIRIDIS[i + 1])
    r, g, bl = (round(a[k] + (b[k] - a[k]) * f) for k in range(3))
    return f'#{r:02x}{g:02x}{bl:02x}'


def _e(v: Any) -> str:
    return escape('' if v is None else str(v), quote=True)


def _fmt(v: float | None, digits: int = 3) -> str:
    return '—' if v is None else f'{v:.{digits}f}'


def _matrix_svg(cells: list[dict], seq: str) -> str:
    size, left, head = 18, 44, 20
    by = {(c['position'], c['mut_aa']): c for c in cells}
    w, h = left + 20 * size, head + len(seq) * size
    out = [f'<svg class="matrix" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
           f'aria-label="Calibrated probability of each substitution; rows are positions, columns substituted amino '
           f'acids; wild-type cells are hatched. The values are in the tables of this report.">',
           '<defs><pattern id="wt" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<rect width="5" height="5" fill="#ffffff"/><line x1="0" y1="0" x2="0" y2="5" stroke="#333" '
           'stroke-width="1.5"/></pattern></defs>']
    for j, aa in enumerate(AMINO):
        out.append(f'<text x="{left + j * size + size / 2}" y="{head - 6}" text-anchor="middle">{aa}</text>')
    for i, wt in enumerate(seq):
        y = head + i * size
        out.append(f'<text x="2" y="{y + size - 5}">{i + 1:>2} {_e(wt)}</text>')
        for j, aa in enumerate(AMINO):
            x = left + j * size
            c = by.get((i + 1, aa))
            fill = 'url(#wt)' if aa == wt or c is None else prob_color(c['p_dpsi_ge_1_calibrated'])
            title = (f'{i + 1} {wt}: wild type' if c is None else
                     f"{i + 1} {wt}→{aa}: p={c['p_dpsi_ge_1_calibrated']:.3f}, raw={c['score_dpsi_raw']:.3f}, "
                     f"rank {c['rank_in_tile']}")
            out.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{fill}" stroke="#fff" '
                       f'stroke-width="0.5"><title>{_e(title)}</title></rect>')
    out.append('</svg>')
    return ''.join(out)


def _colorbar() -> str:
    stops = ''.join(f'<stop offset="{k / 10:.1f}" stop-color="{prob_color(k / 10)}"/>' for k in range(11))
    return ('<svg class="colorbar" viewBox="0 0 260 30" width="260" height="30" role="img" '
            'aria-label="Colour bar from probability 0 (light) to 1 (dark)">'
            f'<defs><linearGradient id="cb">{stops}</linearGradient></defs>'
            '<rect x="0" y="0" width="260" height="12" fill="url(#cb)" stroke="#999" stroke-width="0.5"/>'
            '<text x="0" y="26">0</text><text x="122" y="26">0.5</text><text x="250" y="26">1</text></svg>')


def footprint_rows(cells: list[dict], seq: str) -> list[dict]:
    """Same definition as the interface track: mean of the 19 substitutions of each position."""
    rows = []
    for pos in range(1, len(seq) + 1):
        at = [c for c in cells if c['position'] == pos]
        n = len(at) or 1
        rows.append({'position': pos, 'wt': seq[pos - 1],
                     'mean_prob': sum(c['p_dpsi_ge_1_calibrated'] for c in at) / n,
                     'mean_raw': sum(c['score_dpsi_raw'] for c in at) / n,
                     'top10': sum(1 for c in at if c['top10pct_in_tile'])})
    return rows


def _footprint_svg(rows: list[dict]) -> str:
    bar, row, head = 220, 14, 4
    h = head + len(rows) * row
    out = [f'<svg class="footprint" viewBox="0 0 {bar + 90} {h}" width="{bar + 90}" height="{h}" role="img" '
           'aria-label="Footprint: mean calibrated probability of the 19 substitutions at each position">']
    for i, r in enumerate(rows):
        y = head + i * row
        out.append(f'<text x="0" y="{y + 10}">{r["position"]:>2} {_e(r["wt"])}</text>'
                   f'<rect x="40" y="{y + 2}" width="{bar * r["mean_prob"]:.1f}" height="{row - 4}" fill="#5b6b7f"/>'
                   f'<text x="{bar + 46}" y="{y + 10}">{r["mean_prob"]:.2f}</text>')
    out.append('</svg>')
    return ''.join(out)


STYLE = """
:root { color-scheme: light; }
body { font: 14px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color: #1a1a1a; background: #fff;
       margin: 24px auto; max-width: 960px; padding: 0 16px; }
h1 { font-size: 22px; margin: 0 0 4px; } h2 { font-size: 17px; margin: 24px 0 8px; border-bottom: 1px solid #ccc; }
.muted { color: #555; } code, .mono { font-family: ui-monospace, "Roboto Mono", monospace; font-size: 12px; }
.seq { font-family: ui-monospace, monospace; letter-spacing: 1px; word-break: break-all; }
.box { border: 1px solid #999; border-left-width: 6px; padding: 8px 12px; margin: 8px 0; background: #fafafa; }
.box.warn { border-color: #a15c00; background: #fff6e5; } .box.danger { border-color: #b00020; background: #fdecee; }
.box.info { border-color: #2f5d8a; background: #eef4fa; }
.label { font-weight: 700; margin-right: 6px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0; font-size: 12px; }
th, td { border: 1px solid #ccc; padding: 3px 6px; text-align: left; vertical-align: top; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
svg text { font: 11px ui-monospace, monospace; fill: #1a1a1a; }
.figs { display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start; }
.wrap { overflow-x: auto; max-width: 100%; }
@page { size: A4; margin: 14mm; }
@media print { body { margin: 0; max-width: none; } .noprint { display: none; } h2 { break-after: avoid; }
               svg, table, .box { break-inside: avoid; } a { color: inherit; text-decoration: none; } }
"""


def build_report(data: dict, generated_at: datetime | None = None) -> str:
    """HTML of a SavedAnalysis (`analysis_dict`): limitations first, then figures, tables and provenance."""
    result, snap = data['result'], data['snapshot']
    prov, tile, domain = result['provenance'], result['tile'], result['domain']
    cells, warnings = result['cells'], result.get('warnings') or []
    seq = tile['sequence']
    name = (f"{tile['uniprot_id']} tile {tile['tile_index']} (residues {tile['start_pos']}–{tile['end_pos']})"
            if tile.get('uniprot_id') else 'Typed tile')
    now = (generated_at or datetime.now(UTC)).strftime('%Y-%m-%dT%H:%M:%SZ')
    spread = all(isinstance(c.get('score_seed_sd'), (int, float)) for c in cells) and bool(cells)
    top = sorted(cells, key=lambda c: c['rank_in_tile'])[:TOP_K]
    fp = footprint_rows(cells, seq)
    ann = snap.get('annotations') or {}
    cv = ann.get('clinvar') or {}
    model = snap.get('model') or {}
    p: list[str] = []
    p.append(f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
             f'<meta name="viewport" content="width=device-width, initial-scale=1">'
             f'<meta http-equiv="Content-Security-Policy" content="{REPORT_CSP_META}">'
             f'<meta name="referrer" content="no-referrer">'
             f'<title>Degron Footprint report · {_e(name)}</title><style>{STYLE}</style></head><body>')
    p.append(f'<h1>Degron Footprint — analysis report</h1><p class="muted">{_e(name)} · analysis '
             f'<span class="mono">{_e(data["analysis_id"])}</span> · saved {_e(data["created_at"])} · report generated '
             f'{_e(now)} from the stored snapshot (not recomputed)</p>')
    p.append('<p class="noprint muted">Use the browser\'s Print command to save this page as PDF.</p>')

    # ---- limitations, domain and warnings: before any number (R-1)
    p.append('<h2>Read this first</h2>')
    p.append(f'<div class="box info" data-section="evidence"><span class="label">Evidence</span>'
             f'{_e(prov["evidence_label"])}. Assay: GPS (Zhang et al. 2023). {_e(DISCLAIMER_EXPORT)}</div>')
    tone = 'danger' if 'OUT_OF_DOMAIN_OVERRIDDEN' in [w['code'] for w in warnings] else (
        'warn' if domain['status'] != 'measured_in_domain' else 'info')
    p.append(f'<div class="box {tone}" data-section="domain"><span class="label">Domain</span>'
             f'<code>{_e(domain["status"])}</code> — {_e(domain["message"])}</div>')
    for w in warnings:
        p.append(f'<div class="box warn" data-section="warning"><span class="label">Warning</span>'
                 f'<code>{_e(w["code"])}</code> {_e(w["message"])}</div>')
    for text in prov.get('disclaimers') or []:
        p.append(f'<div class="box" data-section="disclaimer">{_e(text)}</div>')
    if spread:
        p.append(f'<div class="box info" data-section="spread"><span class="label">Seed spread</span>'
                 f'{_e(SPREAD_LABEL)}</div>')

    # ---- input
    p.append(f'<h2>Input</h2><p class="seq">{_e(seq)}</p><p class="muted">Model <code>{_e(prov["model_id"])}</code> '
             f'({_e(prov.get("model_kind"))}) · event {_e(prov["event_definition"])} · domain: '
             f'{_e(prov["domain_description"])}</p>')

    # ---- figures
    p.append(f'<h2>Effect matrix and footprint</h2><p class="muted">Calibrated probability '
             f'{_e(prov["event_definition"])} for each substitution; darker is more likely. Hatched = wild type. '
             f'Footprint = mean of the 19 substitutions of each position. Each tile is scored in its own 28-residue '
             f'context.</p>')
    p.append(f'{_colorbar()}<div class="figs"><div class="wrap">{_matrix_svg(cells, seq)}</div>'
             f'<div class="wrap">{_footprint_svg(fp)}</div></div>')

    # ---- top-k
    p.append(f'<h2>Top {len(top)} substitutions by raw score (top 10 % of the tile)</h2>'
             '<p class="muted">Ranking within this tile only; retrospective, development benchmark — not a validated '
             'experimental design.</p>')
    extra = '<th class="num">Seed SD</th><th class="num">Seed min</th><th class="num">Seed max</th>' if spread else ''
    p.append('<table data-section="topk"><thead><tr><th class="num">Rank</th><th>Substitution</th>'
             f'<th class="num">Raw ΔPSI score</th><th class="num">P {_e(prov["event_definition"])}</th>{extra}'
             '</tr></thead><tbody>')
    for c in top:
        sd = (f'<td class="num">{_fmt(c.get("score_seed_sd"))}</td><td class="num">{_fmt(c.get("score_seed_min"))}'
              f'</td><td class="num">{_fmt(c.get("score_seed_max"))}</td>') if spread else ''
        p.append(f'<tr><td class="num">{c["rank_in_tile"]}</td><td class="mono">{_e(c["wt_aa"])}{c["position"]}'
                 f'{_e(c["mut_aa"])}</td><td class="num">{c["score_dpsi_raw"]:.4f}</td>'
                 f'<td class="num">{c["p_dpsi_ge_1_calibrated"]:.4f}</td>{sd}</tr>')
    p.append('</tbody></table>')
    p.append('<table data-section="footprint"><caption class="muted">Footprint per position</caption><thead><tr>'
             '<th class="num">Position</th><th>WT</th><th class="num">Mean P</th><th class="num">Mean raw</th>'
             '<th class="num">Top 10 % substitutions</th></tr></thead><tbody>')
    for r in fp:
        p.append(f'<tr><td class="num">{r["position"]}</td><td>{_e(r["wt"])}</td><td class="num">{r["mean_prob"]:.4f}'
                 f'</td><td class="num">{r["mean_raw"]:.4f}</td><td class="num">{r["top10"]}</td></tr>')
    p.append('</tbody></table>')

    # ---- annotations snapshot
    if cv:
        p.append(f'<h2>ClinVar (snapshot of the analysis)</h2><p>State: <code>{_e(cv.get("state"))}</code>'
                 f'{" · file " + _e(cv.get("clinvar_file_date")) if cv.get("clinvar_file_date") else ""}. '
                 'ClinVar classifications are not diagnoses, and the model scores are not probabilities of disease.</p>')
        variants = cv.get('variants') or []
        if variants:
            p.append('<table data-section="clinvar"><thead><tr><th>Variant</th><th>Classification</th>'
                     '<th>Review status</th></tr></thead><tbody>')
            for v in variants:
                p.append(f'<tr><td class="mono">{_e(v.get("ref_aa"))}{_e(v.get("position"))}{_e(v.get("alt_aa"))}</td>'
                         f'<td>{_e(v.get("clinsig"))}</td><td>{_e(v.get("review_status"))}</td></tr>')
            p.append('</tbody></table>')
        for src in cv.get('sources') or []:
            p.append(f'<p class="muted" data-section="attribution">{_e(src.get("attribution_text"))} '
                     f'{_e(src.get("disclaimer_text"))}</p>')

    # ---- provenance and attribution
    p.append('<h2>Provenance</h2><table data-section="provenance"><tbody>')
    rows = [('Analysis id', data['analysis_id']), ('Project id', data['project_id']),
            ('Saved at', data['created_at']), ('Result generated at', prov.get('generated_at')),
            ('Model id', prov['model_id']), ('Model kind', prov.get('model_kind')),
            ('Weights SHA-256', prov['weights_sha256']), ('Calibrator', model.get('calibrator')),
            ('Feature specification', prov.get('feature_spec')), ('Event definition', prov['event_definition']),
            ('Gate model', (snap.get('gate') or {}).get('gate_model_id') or domain.get('gate_model_id')),
            ('Code version', prov.get('code_version')), ('Warnings', ', '.join(w['code'] for w in warnings) or 'none')]
    for k, v in rows:
        p.append(f'<tr><th>{_e(k)}</th><td class="mono">{_e(v)}</td></tr>')
    p.append('</tbody></table><h2>Data sources and attribution</h2><table data-section="sources"><thead><tr>'
             '<th>Source</th><th>Version</th><th>Licence</th><th>Attribution</th></tr></thead><tbody>')
    for src in prov.get('data_sources') or []:
        p.append(f'<tr><td>{_e(src.get("name") or src.get("source_id"))}</td><td>{_e(src.get("version"))}</td>'
                 f'<td>{_e(src.get("license_name"))}</td><td>{_e(src.get("attribution_text"))}</td></tr>')
    p.append('</tbody></table>')
    p.append('<p class="muted">Degron Footprint is a local research tool. Scores describe one reporter assay and a '
             'development benchmark; they are not external validation and not probabilities of disease.</p>')
    p.append('</body></html>')
    return ''.join(p)


__all__ = ['build_report', 'footprint_rows', 'prob_color', 'REPORT_CSP', 'REPORT_CSP_META']
