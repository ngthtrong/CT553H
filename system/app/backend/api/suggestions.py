"""Candidates to verify in one tile (plan-system 2.6): a retrospective priority list, never a validated design.

Criteria, each recorded as a reason with its number so the list can be checked by hand:

* ``high_score_uncertain`` — in the top 10 % of the tile (rank ≤ 54) **and** seed spread at or above the tile's 75th
  percentile (ensembles only: LoRA-D);
* ``models_disagree`` — another saved analysis of the same tile (usually another model) differs by
  |ΔP| ≥ DISAGREE_THRESHOLD in calibrated probability;
* ``clinvar_variant`` — a ClinVar missense variant at that position and residue in the analysis snapshot (reference
  residue matching the tile).

Order: number of reasons (desc), then the higher calibrated probability of the two analyses (desc), then rank, then
position and mutant — deterministic for the same inputs. Ranking only: nothing measured is fed back to any model (R-7).
A tile scored outside the domain (override) gives no candidates unless ``include_out_of_domain`` is asked.
"""
from __future__ import annotations

import csv
import io
from typing import Any

import numpy as np
from sqlalchemy.orm import Session

from degron_footprint.constants import TOP_K
from degron_footprint.errors import DomainError

from . import workspace_store as ws

LABEL = ('Retrospective priority list, development benchmark; not an experimentally validated design. It ranks '
         'substitutions of this tile only and is never used to update the model.')
DISAGREE_THRESHOLD = 0.2
SPREAD_QUANTILE = 0.75
OUT_OF_DOMAIN = ('measured_out_of_domain', 'predicted_out_of_domain')


def suggest(s: Session, analysis_id: str, other_id: str | None = None, limit: int = 20,
            include_out_of_domain: bool = False) -> dict[str, Any]:
    run = ws.get_analysis(s, analysis_id)
    res = run.result
    status = res['domain']['status']
    criteria: dict[str, Any] = {'top_k': TOP_K, 'spread_quantile': SPREAD_QUANTILE, 'disagree_threshold': DISAGREE_THRESHOLD}
    out: dict[str, Any] = {'analysis_id': analysis_id, 'compared_with': other_id, 'label': LABEL,
                           'criteria': criteria, 'domain_status': status, 'model_id': res['provenance']['model_id'],
                           'candidates': [], 'excluded_reason': None}
    if status in OUT_OF_DOMAIN and not include_out_of_domain:
        out['excluded_reason'] = ('The tile was scored outside the training domain (override); no candidate is '
                                  'proposed unless include_out_of_domain is set.')
        return out
    cells = {(c['position'], c['mut_aa']): c for c in res['cells']}
    other = None
    if other_id is not None:
        o = ws.get_analysis(s, other_id)
        if o.result['tile']['sequence'] != res['tile']['sequence'] or o.analysis_id == run.analysis_id:
            raise DomainError('INVALID_REQUEST', 'compare_with must be another analysis of the same tile sequence.',
                              422, 'compare_with')
        other = {(c['position'], c['mut_aa']): c for c in o.result['cells']}
        out['compared_model_id'] = o.result['provenance']['model_id']
    sds = [c.get('score_seed_sd') for c in res['cells']]
    has_spread = bool(sds) and all(isinstance(v, (int, float)) for v in sds)
    cut = float(np.quantile(np.asarray(sds, dtype=float), SPREAD_QUANTILE)) if has_spread else None
    criteria['spread_cut'] = cut
    clinvar: dict[tuple[int, str], list[dict]] = {}
    cv = ((run.annotation_snapshot or {}).get('clinvar') or {})
    for v in cv.get('variants') or []:
        if v.get('residue_matches') is False:
            continue
        clinvar.setdefault((int(v['position']), str(v['alt_aa'])), []).append(v)
    rows = []
    for key, c in cells.items():
        reasons = []
        if cut is not None and c['rank_in_tile'] <= TOP_K and c['score_seed_sd'] >= cut:
            reasons.append({'code': 'high_score_uncertain', 'value': c['score_seed_sd'],
                            'text': f"top 10 % (rank {c['rank_in_tile']}) with seed SD {c['score_seed_sd']:.3f} ≥ "
                                    f"{cut:.3f} (75th percentile of the tile)"})
        prob_b = None
        if other is not None and key in other:
            prob_b = other[key]['p_dpsi_ge_1_calibrated']
            d = prob_b - c['p_dpsi_ge_1_calibrated']
            if abs(d) >= DISAGREE_THRESHOLD:
                reasons.append({'code': 'models_disagree', 'value': d,
                                'text': f"P differs by {d:+.3f} between the two analyses (threshold {DISAGREE_THRESHOLD})"})
        if key in clinvar:
            sig = sorted({str(v.get('clinsig')) for v in clinvar[key]})
            reasons.append({'code': 'clinvar_variant', 'value': len(clinvar[key]),
                            'text': f"ClinVar variant(s) at this residue: {', '.join(sig)} (not a diagnosis)"})
        if reasons:
            best = max(c['p_dpsi_ge_1_calibrated'], prob_b if prob_b is not None else -1.0)
            rows.append(({'position': c['position'], 'wt_aa': c['wt_aa'], 'mut_aa': c['mut_aa'],
                          'score_dpsi_raw': c['score_dpsi_raw'], 'prob': c['p_dpsi_ge_1_calibrated'],
                          'prob_other': prob_b, 'rank_in_tile': c['rank_in_tile'],
                          'score_seed_sd': c.get('score_seed_sd'), 'reasons': reasons},
                         (-len(reasons), -best, c['rank_in_tile'], c['position'], c['mut_aa'])))
    rows.sort(key=lambda r: r[1])
    out['candidates'] = [r for r, _ in rows[:limit]]
    out['n_with_reason'] = len(rows)
    return out


def to_csv(data: dict) -> str:
    buf = io.StringIO()
    for k in ('analysis_id', 'compared_with', 'model_id', 'domain_status'):
        buf.write(f'# {k}={data.get(k)}\n')
    buf.write(f"# label={LABEL}\n# criteria={data['criteria']}\n")
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(['priority', 'substitution', 'rank_in_tile', 'score_dpsi_raw', 'prob', 'prob_other', 'score_seed_sd',
                'reasons'])
    for i, c in enumerate(data['candidates'], 1):
        w.writerow([i, f"{c['wt_aa']}{c['position']}{c['mut_aa']}", c['rank_in_tile'], f"{c['score_dpsi_raw']:.6g}",
                    f"{c['prob']:.6g}", '' if c['prob_other'] is None else f"{c['prob_other']:.6g}",
                    '' if c['score_seed_sd'] is None else f"{c['score_seed_sd']:.6g}",
                    '; '.join(r['text'] for r in c['reasons'])])
    return buf.getvalue()


__all__ = ['suggest', 'to_csv', 'LABEL', 'DISAGREE_THRESHOLD']
