"""Equal-budget retrospective ranking of stored OOF; never loads a model.

Run from repository root:
  .venv/bin/python -I research/oof-prioritization-2026-11-07/evaluate.py
Outputs stay beside this script. Source data and campaigns are read-only.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
TZ = timezone(timedelta(hours=8))
METRICS = ['precision', 'hits', 'recall', 'enrichment', 'btr50', 'btr80',
           'btr50_fraction', 'btr80_fraction']


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def clean(x):
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (tuple, list, np.ndarray)):
        return [clean(v) for v in x]
    if isinstance(x, np.generic):
        return clean(x.item())
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x


def write_json(path, value):
    path.write_text(json.dumps(clean(value), ensure_ascii=False, indent=2,
                               allow_nan=False) + '\n', encoding='utf8')


def stable_hash(parts):
    return hashlib.sha256(json.dumps(parts, ensure_ascii=False,
                                     separators=(',', ':')).encode()).digest()


def tie_keys(peptide, ids, seed=1729):
    return np.array([stable_hash([int(seed), str(peptide), str(c)]).hex()
                     for c in ids])


def rank(scores, peptide, ids, seed=1729):
    return np.lexsort((tie_keys(peptide, ids, seed), -np.asarray(scores)))


def crossing_tie(scores, k):
    ordered = np.sort(np.asarray(scores))[::-1]
    return bool(k < len(ordered) and ordered[k-1] == ordered[k])


def budget_sizes(n, config):
    budgets = {f'k{k}': min(k, n) for k in config['fixed_budgets']}
    budgets.update({f'q{int(q*100):02d}': max(1, math.ceil(q*n))
                    for q in config['fraction_budgets']})
    return budgets


def measurements(labels, order, k):
    labels = np.asarray(labels, dtype=bool)
    n, h = len(labels), int(labels.sum())
    found = float(labels[order[:k]].sum())
    out = dict(n=n, total_hits=h, selected=k, hits=found, precision=found/k,
               recall=found/h if h else None,
               enrichment=(found/k)/(h/n) if h else None,
               null_reason=None if h else 'no_hits_in_candidate_pool')
    for r in [.5, .8]:
        key = f'btr{int(r*100)}'
        j = math.ceil(r*h)
        b = int(np.flatnonzero(labels[order])[j-1]+1) if h else None
        out[key] = b
        out[key+'_fraction'] = b/n if h else None
    return out


def random_expectation(n, h, k):
    out = dict(n=n, total_hits=h, selected=k, hits=k*h/n, precision=h/n,
               recall=k/n if h else None, enrichment=1.0 if h else None,
               null_reason=None if h else 'no_hits_in_candidate_pool')
    for r in [.5, .8]:
        key = f'btr{int(r*100)}'
        b = math.ceil(r*h)*(n+1)/(h+1) if h else None
        out[key] = b
        out[key+'_fraction'] = b/n if h else None
    return out


def validate_prediction_frame(frame, expected_ids, seeds):
    if frame.duplicated(['seed', 'cell_id']).any():
        raise ValueError('duplicate seed/cell_id')
    if set(frame.seed) != set(seeds):
        raise ValueError('missing or extra seed')
    if not np.isfinite(frame.prediction).all():
        raise ValueError('nonfinite prediction')
    for seed in seeds:
        if set(frame.loc[frame.seed == seed, 'cell_id']) != set(expected_ids):
            raise ValueError('cell_id cohort mismatch')


def paired_bootstrap(a, b, metric, replicates=5000, seed=1729, multiplicity=1):
    keys = ['peptide_id', 'group_id']
    joined = a[keys+[metric]].merge(b[keys+[metric]], on=keys,
                                    suffixes=('_a', '_b'), validate='one_to_one')
    assert len(joined) == len(a) == len(b), 'paired cohort mismatch'
    joined = joined.dropna(subset=[metric+'_a', metric+'_b'])
    if joined.empty:
        return dict(delta=None, ci95=None, ci_adjusted=None, peptides=0, groups=0,
                    reason='no_eligible_paired_peptides')
    joined['difference'] = joined[metric+'_a'] - joined[metric+'_b']
    grouped = joined.groupby('group_id', sort=True).difference.agg(['sum', 'count'])
    idx = np.random.default_rng(seed).integers(0, len(grouped),
                                             (replicates, len(grouped)))
    draws = grouped['sum'].to_numpy()[idx].sum(1)/grouped['count'].to_numpy()[idx].sum(1)
    q = .025/multiplicity
    return dict(delta=float(joined.difference.mean()),
                ci95=np.quantile(draws, [.025, .975]).tolist(),
                ci_adjusted=np.quantile(draws, [q, 1-q]).tolist(),
                adjusted_level=1-.05/multiplicity, multiplicity=multiplicity,
                peptides=len(joined), groups=len(grouped), replicates=replicates,
                bootstrap_seed=seed)


def mean_ci(rows, metric, config):
    other = rows.copy()
    other[metric] = np.where(rows[metric].notna(), 0., np.nan)
    result = paired_bootstrap(rows, other, metric, config['bootstrap_replicates'],
                              config['bootstrap_seed'])
    return result['ci95']


def scorer_checks():
    checks = {}
    for n in range(1, 7):
        for h in range(n+1):
            y = np.arange(n) < h
            permutations = list(itertools.permutations(range(n)))
            for k in range(1, n+1):
                expected = random_expectation(n, h, k)
                actual = [measurements(y, np.array(p), k) for p in permutations]
                for metric in METRICS:
                    values = [v[metric] for v in actual if v[metric] is not None]
                    if values:
                        assert np.isclose(np.mean(values), expected[metric], atol=1e-12)
                    else:
                        assert expected[metric] is None
    checks['exact_enumeration_random_n1_to_6_all_h_k'] = 'pass'
    assert measurements([0, 0], np.arange(2), 2)['recall'] is None
    assert measurements([1, 1], np.arange(2), 2)['precision'] == 1
    assert budget_sizes(3, {'fixed_budgets':[10], 'fraction_budgets':[.05]}) == {'k10':3,'q05':1}
    ids = np.array(['c', 'a', 'd', 'b']); score=np.ones(4)
    order = rank(score, 'p', ids)
    ix = np.array([2, 0, 3, 1])
    assert list(ids[order]) == list(ids[ix][rank(score[ix], 'p', ids[ix])])
    assert crossing_tie(score, 2) and not crossing_tie(score, 4)
    assert measurements([1, 0, 0, 1], np.array([3, 1, 2, 0]), 1)['btr80'] == 4
    checks['zero_all_hits_small_n_full_tie_btr_row_order'] = 'pass'
    good = pd.DataFrame({'cell_id':['a','b','a','b'],'seed':[17,17,29,29],
                         'prediction':[1.,2.,3.,4.]})
    validate_prediction_frame(good, ['a','b'], [17,29])
    for bad in [good.iloc[:2], pd.concat([good, good.iloc[:1]]), good.iloc[:-1],
                good.assign(prediction=[1,2,3,np.nan])]:
        try:
            validate_prediction_frame(bad, ['a','b'], [17,29])
        except ValueError:
            pass
        else:
            raise AssertionError('invalid frame accepted')
    checks['reject_missing_seed_duplicate_id_cohort_nonfinite'] = 'pass'
    # Unequal cluster sizes: target is peptide mean, not mean of cluster means.
    a = pd.DataFrame({'peptide_id':['a','b','c'],'group_id':['g1','g1','g2'],
                      'precision':[1.,1.,0.]})
    b = a.assign(precision=0.)
    paired = paired_bootstrap(a, b, 'precision', 100, 1729)
    assert paired['delta'] == 2/3 and paired['groups'] == 2
    checks['unequal_cluster_sizes_preserve_peptide_estimand'] = 'pass'
    return checks


def summarize(frame):
    row = dict(peptides=len(frame), groups=int(frame.group_id.nunique()),
               cells=int(frame.n.sum()), budget_total=int(frame.selected.sum()),
               selected_min=int(frame.selected.min()), selected_max=int(frame.selected.max()),
               hits_total=float(frame.hits.sum()), no_hit_peptides=int((frame.total_hits == 0).sum()))
    for m in METRICS:
        valid = frame[m].dropna()
        row[m] = float(valid.mean()) if len(valid) else None
        row[m+'_eligible_peptides'] = len(valid)
        row[m+'_eligible_groups'] = int(frame.loc[frame[m].notna(), 'group_id'].nunique())
    row['cutoff_tie_peptides'] = int(frame.cutoff_tie.fillna(False).sum())
    return row


def evaluate(reference, predictions, config):
    rows, curves, examples = [], [], []
    tie_draws = defaultdict(lambda: np.zeros(len(config['tie_sensitivity_seeds'])))
    tie_changed = defaultdict(int)
    tie_crossings = defaultdict(int)
    legacy_differences = defaultdict(lambda: dict(max_abs_precision_difference=0., different_peptide_budgets=0))
    old = module(ROOT/'research/kaggle-roadmap-2026-10-31/degron_v3/metrics.py', 'legacy_metrics')
    example_ids = set(reference.groupby('psi_stratum', observed=True).peptide_id.min())
    n_peptides = reference.peptide_id.nunique()
    for peptide, sub in reference.groupby('peptide_id', sort=True, observed=True):
        idx = sub.index
        ids = idx.to_numpy()
        n = len(sub)
        meta = dict(peptide_id=peptide, group_id=sub.group_id.iloc[0],
                    psi_stratum=sub.psi_stratum.iloc[0], outer_fold=int(sub.outer_fold.iloc[0]),
                    psi_wt=float(sub.psi_wt.iloc[0]))
        y = sub.dpsi_mean.to_numpy()
        for direction in config['directions']:
            label = y >= 1 if direction == 'plus' else y <= -1
            h = int(label.sum())
            base = dict(**meta, direction=direction,
                        hit_count_stratum='0' if h == 0 else ('1-2' if h <= 2 else 'ge3'))
            for name, k in budget_sizes(n, config).items():
                rows.append(dict(**base, policy='random', prediction_set='ensemble', budget=name,
                                 cutoff_tie=None, **random_expectation(n,h,k)))
            for k in config['curve_budgets']:
                curves.append(dict(**base, policy='random', budget_k=k,
                                   **random_expectation(n,h,min(k,n))))
            for policy, pred in predictions.items():
                for prediction_set in ['seed17','seed29','seed43','ensemble']:
                    score = pred.loc[idx, prediction_set].to_numpy()
                    score = score if direction == 'plus' else -score
                    ordering = rank(score, peptide, ids, config['tie_seed'])
                    for name, k in budget_sizes(n, config).items():
                        rows.append(dict(**base, policy=policy, prediction_set=prediction_set,
                                         budget=name, cutoff_tie=crossing_tie(score,k),
                                         **measurements(label,ordering,k)))
                        key = (policy,prediction_set,direction,name)
                        if crossing_tie(score,k):
                            tie_crossings[key] += 1
                            boundary = np.sort(score)[::-1][k-1]
                            strict = score > boundary
                            tied = np.flatnonzero(score == boundary)
                            needed = k-int(strict.sum())
                            strict_hits = int(label[strict].sum())
                            values = []
                            for seed in config['tie_sensitivity_seeds']:
                                tied_order = np.argsort(tie_keys(peptide,ids[tied],seed))
                                values.append((strict_hits+int(label[tied[tied_order[:needed]]].sum()))/k)
                            values = np.asarray(values)
                            tie_changed[key] += int(np.ptp(values) > 0)
                        else:
                            values = np.full(len(config['tie_sensitivity_seeds']), float(label[ordering[:k]].mean()))
                        tie_draws[key] += values/n_peptides
                    if prediction_set != 'ensemble':
                        continue
                    for curve_k in config['curve_budgets']:
                        curves.append(dict(**base, policy=policy, budget_k=curve_k,
                                           **measurements(label,ordering,min(curve_k,n))))
                    # Reconcile changed tie policy with original helper on identical denominator.
                    old_frame = sub.copy()
                    original = old.per_peptide(old_frame, pred.loc[idx,'ensemble'].to_numpy()).iloc[0]
                    for q in config['fraction_budgets']:
                        kq = max(1,math.ceil(q*n))
                        our = float(label[ordering[:kq]].mean())
                        expected = float(original[f'precision_{direction}_{q}'])
                        stable = float(label[np.argsort(-score,kind='stable')[:kq]].mean())
                        assert stable == expected
                        diff = abs(our-expected)
                        key_old = (policy,direction,f'q{int(q*100):02d}')
                        entry = legacy_differences[key_old]
                        entry['max_abs_precision_difference'] = max(entry['max_abs_precision_difference'],diff)
                        entry['different_peptide_budgets'] += int(diff > 0)
                        if diff:
                            assert crossing_tie(score,kq)
                    if peptide in example_ids:
                        for number, cell in enumerate(ordering[:min(10,n)],1):
                            r = sub.iloc[cell]
                            examples.append(dict(**meta, direction=direction, policy=policy,rank=number,
                                cell_id=ids[cell],position_1based=int(r.position_1based),
                                wt_aa=r.wt_aa,mut_aa=r.mut_aa,dpsi_mean=float(r.dpsi_mean),
                                prediction=float(pred.loc[ids[cell],'ensemble']),hit=bool(label[cell])))
    tie_report = [dict(policy=k[0],prediction_set=k[1],direction=k[2],budget=k[3],
                       cutoff_tie_peptides=tie_crossings[k],
                       peptides_with_hit_count_variation=tie_changed[k],
                       macro_precision_min=float(v.min()),macro_precision_max=float(v.max()),
                       macro_precision_mean=float(v.mean()),seeds=config['tie_sensitivity_seeds'])
                  for k,v in sorted(tie_draws.items())]
    old_report = [dict(policy=k[0],direction=k[1],budget=k[2],**v)
                  for k,v in sorted(legacy_differences.items())]
    return pd.DataFrame(rows),pd.DataFrame(curves),pd.DataFrame(examples),tie_report,old_report


def monte_carlo(reference, config):
    """Shared random permutations give jointly nested prefixes for every curve."""
    repetitions = config['random_replicates']
    points = config['curve_budgets']
    sums = {d:dict(hits=np.zeros((repetitions,len(points))),
                  recall=np.zeros((repetitions,len(points))),eligible=0,
                  btr50=np.zeros(repetitions),btr80=np.zeros(repetitions))
            for d in config['directions']}
    for peptide, sub in reference.groupby('peptide_id',sort=True,observed=True):
        # Canonical cell_id order makes replay independent of input row order.
        sub = sub.sort_index()
        n = len(sub)
        seed = int.from_bytes(stable_hash([config['random_seed'],str(peptide)])[:16],'little')
        rng = np.random.Generator(np.random.PCG64(seed))
        permutations = np.array([rng.permutation(n) for _ in range(repetitions)])
        ks = np.minimum(points,n)-1
        for direction in config['directions']:
            labels = sub.dpsi_mean.to_numpy() >= 1 if direction=='plus' else sub.dpsi_mean.to_numpy() <= -1
            h = int(labels.sum())
            cumulative = np.cumsum(labels[permutations],axis=1)
            counts = cumulative[:,ks]
            assert np.all(np.diff(counts,axis=1)>=0)
            sums[direction]['hits'] += counts
            if h:
                sums[direction]['eligible'] += 1
                sums[direction]['recall'] += counts/h
                for r in [.5,.8]:
                    target=math.ceil(r*h)
                    sums[direction][f'btr{int(r*100)}'] += np.argmax(cumulative>=target,axis=1)+1
    rows=[]
    for direction, val in sums.items():
        for j,k in enumerate(points):
            for metric in ['hits','recall']:
                denom=reference.peptide_id.nunique() if metric=='hits' else val['eligible']
                distribution=val[metric][:,j]/denom if denom else np.full(repetitions,np.nan)
                rows.append(dict(direction=direction,budget_k=k,metric=metric,
                    mean=float(distribution.mean()),conditional_q025=float(np.quantile(distribution,.025)),
                    conditional_q975=float(np.quantile(distribution,.975)),
                    monte_carlo_se=float(distribution.std(ddof=1)/math.sqrt(repetitions)),
                    eligible_peptides=denom,repetitions=repetitions,
                    band_type='conditional_random_allocation_not_cluster_CI'))
    return pd.DataFrame(rows),sums


def report_tables(frame,config):
    summaries=[]
    for keys,sub in frame.groupby(['policy','prediction_set','direction','budget'],sort=True):
        summaries.append(dict(zip(['policy','prediction_set','direction','budget'],keys),**summarize(sub)))
    strata=[]
    main=frame[(frame.prediction_set=='ensemble') & (frame.budget=='k10')]
    for kind in config['secondary_strata']:
        col='hit_count_stratum' if kind=='hit_count_0_1-2_ge3' else kind
        for keys,sub in main.groupby(['policy','direction',col],sort=True,observed=True):
            row = dict(policy=keys[0],direction=keys[1],stratum=kind,value=str(keys[2]),
                       **summarize(sub))
            for metric in METRICS:
                ci = mean_ci(sub,metric,config)
                row[metric+'_ci95_low'] = ci[0] if ci else None
                row[metric+'_ci95_high'] = ci[1] if ci else None
            strata.append(row)
    contrasts=[]
    for direction in config['directions']:
        for budget in frame.budget.unique():
            a=frame[(frame.policy=='lora-D')&(frame.prediction_set=='ensemble')&
                    (frame.direction==direction)&(frame.budget==budget)]
            for baseline in ['ridge-w5-D','random','frozen-D','lora-B']:
                b=frame[(frame.policy==baseline)&(frame.prediction_set=='ensemble')&
                        (frame.direction==direction)&(frame.budget==budget)]
                for metric in METRICS:
                    if metric.startswith('btr') and budget!='k10':
                        continue
                    primary=direction=='plus' and budget=='k10' and metric=='precision' and baseline in config['primary_baselines']
                    result=paired_bootstrap(a,b,metric,config['bootstrap_replicates'],
                                            config['bootstrap_seed'],2 if primary else 1)
                    contrasts.append(dict(policy='lora-D',baseline=baseline,direction=direction,
                        budget=budget,metric=metric,primary=primary,
                        interpretation='lower_better' if metric.startswith('btr') else 'higher_better',
                        delta_percentage_points=100*result['delta'] if metric=='precision' and result['delta'] is not None else None,
                        delta_total_hits=float(a.hits.sum()-b.hits.sum()) if metric=='precision' else None,
                        **result))
    return pd.DataFrame(summaries),pd.DataFrame(strata),contrasts


def plot_curves(curves,mc,config):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    colors={'lora-D':'#0072B2','ridge-w5-D':'#D55E00','frozen-D':'#009E73','lora-B':'#CC79A7','random':'#555555'}
    aggregate=[]
    fig,axes=plt.subplots(2,2,figsize=(13,9),layout='constrained')
    for i,direction in enumerate(['plus','minus']):
        for j,metric in enumerate(['hits','recall']):
            ax=axes[i,j]
            for policy in config['policies']:
                means=[]; lows=[]; highs=[]
                for k in config['curve_budgets']:
                    sub=curves[(curves.direction==direction)&(curves.policy==policy)&(curves.budget_k==k)]
                    valid=sub[metric].dropna()
                    mean=float(valid.mean()) if len(valid) else None
                    ci=mean_ci(sub,metric,config)
                    means.append(mean);lows.append(ci[0] if ci else np.nan);highs.append(ci[1] if ci else np.nan)
                    aggregate.append(dict(direction=direction,policy=policy,budget_k=k,metric=metric,
                        mean=mean,cluster_ci95_low=lows[-1],cluster_ci95_high=highs[-1],
                        eligible_peptides=len(valid),eligible_groups=int(sub.loc[sub[metric].notna(),'group_id'].nunique()),
                        actual_budget_total=int(sub.selected.sum())))
                ax.plot(config['curve_budgets'],means,label=policy,color=colors[policy],lw=1.8)
                if policy in ['lora-D','ridge-w5-D']:
                    ax.fill_between(config['curve_budgets'],lows,highs,color=colors[policy],alpha=.12)
            band=mc[(mc.direction==direction)&(mc.metric==metric)].sort_values('budget_k')
            ax.fill_between(band.budget_k,band.conditional_q025,band.conditional_q975,
                            color='#777777',alpha=.22,label='Random allocation 95% band')
            ax.set_xscale('log');ax.set_xlabel('Maximum selections per peptide (log scale)')
            ax.set_ylabel('Mean hits per peptide' if metric=='hits' else 'Mean recall (peptides with hits)')
            ax.set_title(('Positive: measured delta PSI >= 1' if direction=='plus' else 'Negative: measured delta PSI <= -1'))
            ax.grid(alpha=.2)
    axes[0,0].legend(fontsize=8)
    fig.suptitle('Retrospective OOF prioritization | W development cohort\nColored bands: paired protein-cluster bootstrap CI95; grey: conditional random allocations',fontsize=12)
    fig.savefig(HERE/'budget-curves.png',dpi=180)
    plt.close(fig)
    return pd.DataFrame(aggregate)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args()
    checks=scorer_checks()
    print('PASS scorer edge cases and exhaustive random formulas',flush=True)
    if args.check_only:
        print(json.dumps(checks,indent=2));return
    start=time.perf_counter();cpu=time.process_time()
    started=datetime.now(TZ).isoformat()
    config=json.loads((HERE/'config.json').read_text())
    config_sha=sha(HERE/'config.json')
    assert config['status']=='locked_before_utility'
    assert sha(ROOT/'tmp.md')==config['plan_source_sha256'], 'Plan changed after lock'
    # Record pre-run Git state, preserving all existing user changes.
    git_before=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        status=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),
        tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','HEAD','--binary'],cwd=ROOT)).hexdigest())
    audit_module=module(HERE/'audit_inputs.py','audit_inputs')
    reference,predictions,input_report=audit_module.audit(HERE)
    assert set(predictions)==set(config['policies'])-{'random'}
    print('PASS input gates; evaluating ranking policies',flush=True)
    frame,curves,examples,ties,legacy=evaluate(reference,predictions,config)
    print('PASS all policy/seed/direction/budget rankings',len(frame),flush=True)
    summary,strata,contrasts=report_tables(frame,config)
    mc,mc_distributions=monte_carlo(reference,config)
    curve_summary=plot_curves(curves,mc,config)
    mc_check=[]
    for row in mc.to_dict('records'):
        expected=curve_summary[(curve_summary.policy=='random')&(curve_summary.direction==row['direction'])&
            (curve_summary.metric==row['metric'])&(curve_summary.budget_k==row['budget_k'])].iloc[0]['mean']
        error=abs(row['mean']-expected)
        z=error/row['monte_carlo_se'] if row['monte_carlo_se']>1e-14 else 0.
        assert error<=max(6*row['monte_carlo_se'],1e-10)
        mc_check.append(dict(direction=row['direction'],metric=row['metric'],budget_k=row['budget_k'],
            analytic=expected,mc_mean=row['mean'],absolute_error=error,mc_se=row['monte_carlo_se'],z=z))
    for direction in config['directions']:
        random_rows=frame[(frame.policy=='random')&(frame.direction==direction)&(frame.budget=='k10')]
        for key in ['btr50','btr80']:
            distribution=mc_distributions[direction][key]/mc_distributions[direction]['eligible']
            expectation=float(random_rows[key].mean())
            se=float(distribution.std(ddof=1)/math.sqrt(config['random_replicates']))
            assert abs(distribution.mean()-expectation)<=max(6*se,1e-10)
            mc_check.append(dict(direction=direction,metric=key,analytic=expectation,
                mc_mean=float(distribution.mean()),mc_se=se))
    primary=[c for c in contrasts if c['primary']]
    assert len(primary)==2
    supports=all(c['ci_adjusted'][0]>0 for c in primary)
    # Every policy has the same exact selected count for every peptide/budget.
    assert frame.groupby(['peptide_id','direction','budget']).selected.nunique().max()==1
    assert len(frame[frame.prediction_set=='ensemble'])==235*5*2*6
    ensemble=frame[frame.prediction_set=='ensemble']
    local=HERE/'local';local.mkdir(exist_ok=True)
    frame.to_parquet(local/'all-seeds-per-peptide.parquet',index=False)
    curves.to_parquet(local/'per-peptide-curves.parquet',index=False)
    ensemble.to_csv(HERE/'per-peptide.csv',index=False)
    summary.to_csv(HERE/'summary.csv',index=False)
    strata.to_csv(HERE/'strata.csv',index=False)
    examples.to_csv(HERE/'ranking-examples.csv',index=False)
    curve_summary.to_csv(HERE/'budget-curves.csv',index=False)
    mc.to_csv(HERE/'random-reference.csv',index=False)
    result=dict(experiment_id=config['experiment_id'],generated_at=datetime.now(TZ).isoformat(),
        scientific_status=config['scientific_status'],config_sha256=config_sha,
        analysis_script_sha256=sha(__file__),input_manifest_sha256=sha(HERE/'input-manifest.json'),
        cohort=dict(cells=len(reference),peptides=int(reference.peptide_id.nunique()),groups=int(reference.group_id.nunique())),
        primary_endpoint='peptide-macro precision at min(10,N), measured dpsi_mean >= 1',
        primary_summary=summary[(summary.direction=='plus')&(summary.prediction_set=='ensemble')&(summary.budget=='k10')].to_dict('records'),
        primary_contrasts=primary,
        conclusion_rule='Both Bonferroni 97.5% cluster CIs above zero support both primary contrasts in this retrospective replay only.',
        supports_both_primary_contrasts=supports,
        secondary_contrasts= [c for c in contrasts if not c['primary']],
        per_seed_primary=summary[(summary.direction=='plus')&(summary.prediction_set!='ensemble')&(summary.budget=='k10')].to_dict('records'),
        tie_sensitivity=ties,legacy_helper_reconciliation=legacy,
        random_monte_carlo_checks=mc_check,
        caveats=['Development OOF repeatedly examined; no prospective independent validation.',
            'No wet-lab time or money measured. Selection counts are retrospective.',
            'Conditional bootstrap excludes retraining, new outer splits and new assay variation.',
            'Local LoRA vs Kaggle Ridge compares workflows, not LoRA adaptation alone.',
            'Event-free peptides remain in precision; undefined recall/enrichment/BTR are null.',
            'Known total hits are used for retrospective scoring only, not an implementable stopping rule.'])
    write_json(HERE/'results.json',result)
    validation=dict(status='pass',scorer_checks=checks,input_audit_status=input_report.get('status','see_input_manifest'),
        exact_equal_budget_all_policies=True,all_seeds_reported=True,ensemble_per_peptide_rows=len(ensemble),
        all_seed_per_peptide_rows=len(frame),no_hit_exclusions_from_precision=False,
        legacy_stable_tie_matches_helper=True,changed_ties_disclosed=True,
        random_2000_trials_match_analytic_within_6_mc_standard_errors=True,
        config_unchanged=sha(HERE/'config.json')==config_sha,git_before=git_before,
        verification_scope='Input integrity, numerical scorer checks and internal output consistency; no new training or wet lab.')
    write_json(HERE/'validation.json',validation)
    versions={}
    for name in ['numpy','pandas','scipy','pyarrow','matplotlib','sklearn']:
        versions[name]=__import__(name).__version__
    runtime=dict(started_at=started,finished_at=datetime.now(TZ).isoformat(),
        wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
        peak_process_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
        python=sys.version,executable=sys.executable,platform=platform.platform(),
        machine=platform.machine(),versions=versions,command='.venv/bin/python -I research/oof-prioritization-2026-11-07/evaluate.py',
        note='Analysis process only; RAM is Linux ru_maxrss, not sampled machine total. Not wet-lab cost.')
    write_json(HERE/'runtime.json',runtime)
    print(json.dumps(clean(dict(primary=primary,supports_both=supports,runtime=runtime)),ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
