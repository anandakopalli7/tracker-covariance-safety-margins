"""Recount (second program): comparison with the first program's OUTPUT files (revision_v11\\analysis\\out\\*.json).
Run only after RECOUNT_RESULTS_v01.json and RECOUNT_REPORT_v01.md were written. The first program's code is not read.

Every numeric leaf of the first program's files REV_A (R11, R17), REV_B (R12a, R12b) and REV_C (R19, R20, S9) is walked.
For each leaf the recount's value is formed from the recount's own points and per-resample arrays (rc_arr_*_v01.npz,
rc_item4_boot_v01.npz, the item JSON files, rc_extra_counts_v01.json) by the formula written beside the key below; a leaf
the recount has no counterpart for is listed as "not compared". Tolerance 1e-9 absolute.

Origin classes of a compared number:
  brief      a number of the brief's list, present in RECOUNT_RESULTS_v01.json (written before the outputs were opened)
  pre-extra  present in RECOUNT_RESULTS_v01.json (so computed before the outputs were opened) but not on the brief's list
             (the share of denE under the 2 m gap; the arm Q in the truncation table)
  derived    formed here from the recount's stored points / resamples / counts of a brief analysis by a fixed formula
             (decision-equivalents, pp, basic interval, share or count of non-positive denominators, "outside" flag,
             further quantiles, one-sided and basic coverages)
  extra      an arm, population or scoring that the first program printed beyond the brief's list (rc_extra_v01.py,
             written after the outputs were opened; definitions from the brief or the allowed second-program library)
"""
import json, math, pathlib, time
from fractions import Fraction
import numpy as np
import rc_lib_v01 as L

H = L.HERE; OUT = H.parent / 'analysis' / 'out'
TOL = 1e-9
ARMS = list(L.ARMS) + ['CK3r', 'P25', 'P50', 'P75']
AI = {a: i for i, a in enumerate(ARMS)}; AO = len(ARMS)          # column of the perfect oracle O
MAP = dict(N='N', NA='NA', CK3='CK3', A1='AM', Q='Q', CK3r='CK3r', P25='P25', P50='P50', P75='P75')
EXTRA_ARMS = ('CK3r', 'P25', 'P50', 'P75')
POPS = ('all', 'moving', 'phase0', 'phase1', 'phase2')

recs = []; skipped = []


def und(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def add(sec, key, th, mine, origin):
    if isinstance(th, list):
        if mine is None:
            mine = [None] * len(th)
        mine = list(mine)
        if len(mine) != len(th):
            recs.append(dict(sec=sec, key=key + ' (length)', th=len(th), mine=len(mine), diff=abs(len(th) - len(mine)), status='DIFF', origin=origin)); return
        for i, (a, b) in enumerate(zip(th, mine)):
            add(sec, '%s[%d]' % (key, i), a, b, origin)
        return
    if isinstance(mine, (np.bool_,)):
        mine = bool(mine)
    if isinstance(mine, (np.integer,)):
        mine = int(mine)
    if isinstance(mine, (np.floating,)):
        mine = float(mine)
    if isinstance(th, bool) or isinstance(mine, bool) or isinstance(th, str):
        recs.append(dict(sec=sec, key=key, th=th, mine=mine, diff=None, status='equal' if th == mine else 'DIFF', origin=origin, kind='flag')); return
    if und(th) and und(mine):
        recs.append(dict(sec=sec, key=key, th=None, mine=None, diff=None, status='both undefined', origin=origin)); return
    if und(th) or und(mine):
        recs.append(dict(sec=sec, key=key, th=th, mine=mine, diff=None, status='DIFF', origin=origin)); return
    d = abs(float(th) - float(mine))
    recs.append(dict(sec=sec, key=key, th=th, mine=mine, diff=d, status='ok' if d <= TOL else 'DIFF', origin=origin))


def pct(v):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    if v.size == 0:
        return [float('nan'), float('nan')]
    return [float(x) for x in np.percentile(v, [2.5, 97.5])]


def div(a, b):
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.asarray(a, float) / np.asarray(b, float)


def ratio_block(sec, key, t, num0, den0, numb, denb, o_main, o_der):
    """their {point, ci, invalid_share, n_invalid, outside, basic} against num/den of the recount."""
    valid = np.isfinite(denb) & (denb > 0) & np.isfinite(numb)
    point = float(div(num0, den0))
    ci = pct(numb[valid] / denb[valid])
    fin = np.isfinite(point) and np.isfinite(ci[0])
    mine = dict(point=point, ci=ci, invalid_share=float((~valid).mean()), n_invalid=int((~valid).sum()),
                outside=bool(fin and not (ci[0] <= point <= ci[1])), basic=[2 * point - ci[1], 2 * point - ci[0]])
    for k, v in t.items():
        if k in mine:
            add(sec, key + '|' + k, v, mine[k], o_main if k in ('point', 'ci') else o_der)
        else:
            skipped.append(sec + '|' + key + '|' + k)


def den_block(sec, key, t, x0, xb, n0, nb, o_main, o_der):
    mine = dict(point=x0, R_pp=x0 / 201, pp=x0 / 201, dec_eq=x0 / 201 / 100 * n0)
    cls = dict(point=o_main, R_pp=o_main, pp=o_main, dec_eq=o_main, ci=o_main, dec_eq_ci=o_main, R_pp_ci=o_main, pp_ci=o_main, share_le0=o_der, n_le0=o_der)
    if xb is not None:
        mine.update(share_le0=float((xb <= 0).mean()), n_le0=int((xb <= 0).sum()), ci=pct(xb), dec_eq_ci=pct(xb / 201 / 100 * nb),
                    R_pp_ci=pct(xb / 201), pp_ci=pct(xb / 201))
    for k, v in t.items():
        if k in mine:
            add(sec, key + '|' + k, v, mine[k], cls[k])
        else:
            skipped.append(sec + '|' + key + '|' + k)


def pop_arrays(arr, pop):
    """(n0, D0 (A+1,), nb (B,), Db (B, A+1)) of a population of a stored configuration; 'strat' = phase-weighted."""
    if pop == 'strat':
        nt0, Dw0 = L.weighted(arr['n0'][None], arr['D0'][None]); ntb, Dwb = L.weighted(arr['nb'], arr['Db'])
        return float(nt0[0]), Dw0[0], ntb, Dwb
    p = pop if isinstance(pop, int) else POPS.index(pop)
    return float(arr['n0'][p]), arr['D0'][p], arr['nb'][:, p], arr['Db'][:, p]


def pop_block_A(sec, th, arr, pop, extra_section):
    n0, D0, nb, Db = pop_arrays(arr, pop)
    om = 'extra' if extra_section else 'brief'; od = 'extra' if extra_section else 'derived'
    gap_section = '|R17|' in sec
    for k, v in th.items():
        key = pop + '|' + k
        if k == 'n':
            add(sec, key, v, n0, om)
        elif k == 'den0':
            den_block(sec, key, v, float(D0[AO]), Db[:, AO], n0, nb, om, od)
        elif k == 'denE':
            den_block(sec, key, v, float(D0[1]), Db[:, 1], n0, nb, om, od)
        elif k == 'E_rr0':
            ratio_block(sec, key, v, D0[1], D0[AO], Db[:, 1], Db[:, AO], om, od)
        elif k == 'arms':
            for a, t in v.items():
                if a not in MAP:
                    skipped.append(sec + '|' + key + '|' + a); continue
                c = AI[MAP[a]]; xa = a in EXTRA_ARMS
                o1 = 'extra' if (xa or extra_section) else 'brief'; o2 = 'extra' if (xa or extra_section) else 'derived'
                for kk, vv in t.items():
                    kkey = key + '|' + a + '|' + kk
                    if kk == 'D':
                        add(sec, kkey, vv, float(D0[c]), o1)
                    elif kk == 'D_pp':
                        add(sec, kkey, vv, float(D0[c]) / 201, o2)
                    elif kk == 'D_dec_eq':
                        add(sec, kkey, vv, float(D0[c]) / 201 / 100 * n0, o2)
                    elif kk == 'D_dec_eq_ci':
                        add(sec, kkey, vv, pct(Db[:, c] / 201 / 100 * nb), o2)
                    elif kk == 'rr0':
                        ratio_block(sec, kkey, vv, D0[c], D0[AO], Db[:, c], Db[:, AO], o1, o2)
                    elif kk == 'rrE':
                        ratio_block(sec, kkey, vv, D0[c], D0[1], Db[:, c], Db[:, 1], ('pre-extra' if (gap_section and o1 == 'brief') else o1), o2)
                    else:
                        skipped.append(sec + '|' + kkey)
        else:
            skipped.append(sec + '|' + key)


def load_arr(name):
    z = np.load(H / ('rc_arr_%s_v01.npz' % name))
    return {k: z[k] for k in z.files}


def compare_D(explanations):
    """REV_D_BOOTSTRAP_v01.json (R9) against the recount's item-5 files, the stored record draw and the stored
    double-bootstrap counts (per outer sample: valid inner values, number below the truth, number at or below it, and the
    same two counts for the reflected point 2 * outer value - truth).
    Rules, all in exact integer arithmetic with the level L = p/q and a = 1 - L:
      two-sided percentile   share(inner <= truth) >= a/2  and  share(inner < truth) <= 1 - a/2        (the brief)
      basic                  the same two inequalities with the reflected point in place of the truth
      upper bound            share(inner < truth) <= L           lower bound   share(inner <= truth) >= 1 - L
      calibrated level       smallest level of the brief's grid (0.900, 0.901, ..., 0.999, 0.9995, 0.9999, 1.0) whose coverage is >= 0.95
    """
    fD = OUT / 'REV_D_BOOTSTRAP_v01.json'
    if not fD.exists():
        skipped.append('D (REV_D_BOOTSTRAP_v01.json not present in analysis/out)'); return
    D_ = json.load(open(fD, encoding='utf-8'))
    i5s = json.load(open(H / 'RECOUNT_item5_single_v01.json', encoding='utf-8'))
    i5d = json.load(open(H / 'RECOUNT_item5_double_v01.json', encoding='utf-8'))
    SM = dict(R='R', RR_N='RR_N', RR_NA='RR_NA', RR_A1='RR_AM', RR_CK3='RR_CK3', RR_Q='RR_Q', RR0_CK3='RR0_CK3', NA_minus_N='RR_NA_minus_RR_N')
    ORDER = ('R', 'RR_N', 'RR_NA', 'RR_AM', 'RR_CK3', 'RR_Q', 'RR0_CK3', 'RR_NA_minus_RR_N')          # order of rc_items_v01.STATS
    rec = np.load(H / 'rc_record_stats_v01.npz'); ck = np.load(H / 'rc_double_ckpt_v01.npz', allow_pickle=False)
    cn = ck['cnts'].astype(np.int64); ov = ck['oval']
    GRID = ['0.%03d' % i for i in range(900, 1000)] + ['0.9995', '0.9999', '1.0']
    for sname, v in D_['full_sample'].items():
        add('D|full_sample', sname, v, i5s['truth'][SM[sname]], 'brief')
    QL = [0, 0.05, 0.5, 2.5, 5, 25, 50, 75, 95, 97.5, 99.5, 99.95, 100]
    for sname, t in D_['D1_draw_of_record'].items():
        x = rec[SM[sname]]; fin = x[np.isfinite(x)]; pt = i5s['truth'][SM[sname]]; ci = pct(fin)
        mine = dict(point=pt, n_invalid=int((~np.isfinite(x)).sum()), mean=float(fin.mean()), sd=float(fin.std(ddof=1)),
                    q_0_0p05_0p5_2p5_5_25_50_75_95_97p5_99p5_99p95_100=np.percentile(fin, QL).tolist(),
                    share_below_point=float((fin < pt).mean()), share_equal_point=float((fin == pt).mean()), share_le_zero=float((fin <= 0).mean()),
                    n_distinct=int(np.unique(fin).size), percentile_95=ci, basic_95=[2 * pt - ci[1], 2 * pt - ci[0]],
                    bias_boot_mean_minus_point=float(fin.mean()) - pt)
        for kk, vv in t.items():
            if kk in mine:
                add('D|D1_draw_of_record', sname + '|' + kk, vv, mine[kk], 'brief' if kk in ('point', 'percentile_95', 'basic_95') else 'derived')
            else:
                skipped.append('D|D1_draw_of_record|%s|%s' % (sname, kk))
    d2 = D_['D2_double_bootstrap']
    add('D|D2_double_bootstrap', 'B_outer', d2['B_outer'], int(cn.shape[0]), 'brief')
    add('D|D2_double_bootstrap', 'B_inner', d2['B_inner'], int(ck['n_inner']), 'brief')

    def frac(lv):
        f = Fraction(lv); return f.numerator, f.denominator
    for sname, t in d2['stats'].items():
        si = ORDER.index(SM[sname]); pt = i5s['truth'][SM[sname]]
        use = cn[:, si, 0] > 0
        nv = cn[use, si, 0]; nlt = cn[use, si, 1]; nle = cn[use, si, 2]; nltr = cn[use, si, 3]; nler = cn[use, si, 4]
        nout = int(use.sum())
        x = rec[SM[sname]]; fin = x[np.isfinite(x)]

        def two(lv, a, b_):
            p, q = frac(lv); return int(np.sum((2 * q * b_ >= (q - p) * nv) & (2 * q * a <= (q + p) * nv)))

        def upper(lv):
            p, q = frac(lv); return int(np.sum(q * nlt <= p * nv))

        def lower(lv):
            p, q = frac(lv); return int(np.sum(q * nle >= (q - p) * nv))

        def calib(fn):
            for lv in GRID:
                if 100 * fn(lv) >= 95 * nout:
                    return lv
            return None
        cal_p = calib(lambda lv: two(lv, nlt, nle)); cal_b = calib(lambda lv: two(lv, nltr, nler)); cal_u = calib(upper)

        def interval(lv):
            a = 1 - Fraction(lv); lo, hi = np.percentile(fin, [float(100 * a / 2), float(100 * (1 - a / 2))]); return float(lo), float(hi)
        for kk, vv in t.items():
            key = sname + '|' + kk; S2 = 'D|D2_double_bootstrap'
            if kk == 'n_outer_valid':
                add(S2, key, vv, nout, 'derived')
            elif kk == 'outer_mean':
                add(S2, key, vv, float(np.nanmean(ov[:, si])), 'derived')
            elif kk in ('coverage_percentile', 'coverage_basic', 'coverage_upper_bound', 'coverage_lower_bound'):
                for lv, cv in vv.items():
                    if kk == 'coverage_percentile':
                        c = two(lv, nlt, nle)
                    elif kk == 'coverage_basic':
                        c = two(lv, nltr, nler)
                    elif kk == 'coverage_upper_bound':
                        c = upper(lv)
                    else:
                        c = lower(lv)
                    o = 'brief' if (kk == 'coverage_percentile' and float(lv) in (0.9, 0.95, 0.99, 0.999, 1.0)) else 'derived'
                    add(S2, '%s|%s' % (key, lv), cv, c / nout, o)
            elif kk == 'calibrated_nominal_percentile':
                add(S2, key, vv, None if cal_p is None else float(cal_p), 'brief')
                add(S2, key + ' (value in the recount results file)', vv, i5d['stats'][SM[sname]]['calibrated_level'], 'brief')
            elif kk == 'calibrated_nominal_basic':
                add(S2, key, vv, None if cal_b is None else float(cal_b), 'derived')
            elif kk == 'calibrated_nominal_upper_bound':
                add(S2, key, vv, None if cal_u is None else float(cal_u), 'derived')
            elif kk == 'mc_se_at_95':
                add(S2, key, vv, math.sqrt(0.95 * 0.05 / nout), 'derived')
            elif kk == 'calibrated_percentile_interval':
                add(S2, key, vv, None if cal_p is None else list(interval(cal_p)), 'brief')
            elif kk == 'calibrated_basic_interval':
                if cal_b is None:
                    add(S2, key, vv, None, 'derived')
                else:
                    lo, hi = interval(cal_b); add(S2, key, vv, [2 * pt - hi, 2 * pt - lo], 'derived')
            elif kk == 'calibrated_upper_bound':
                add(S2, key, vv, None if cal_u is None else float(np.percentile(fin, float(100 * Fraction(cal_u)))), 'derived')
            else:
                skipped.append(S2 + '|' + key)
        e = i5d['stats'][SM[sname]]
        explanations.setdefault('R9_coverage_at_095_exact_rule_and_float_rule', {})[sname] = [e['coverage']['0.950'], e['coverage_float_rule']['0.950']]
        explanations.setdefault('R9_calibrated_level_exact_rule_and_float_rule', {})[sname] = [e['calibrated_level'], e['calibrated_level_float_rule']]
    d3 = D_['D3_sensitivities']
    st = d3['stratified_by_alpha']
    for gk, gv in st['groups'].items():
        add('D|D3|stratified_by_alpha', 'groups|' + gk, gv, len(i5s['stratified_by_alpha']['groups'][gk]), 'brief')
    for sname, vv in st['ci'].items():
        add('D|D3|stratified_by_alpha', 'ci|' + sname, vv, i5s['stratified_by_alpha']['stats'][SM[sname]]['percentile'], 'brief')
    sr = d3['short_runs_left_out']; lr = i5s['long_runs']
    add('D|D3|short_runs_left_out', 'n_runs', sr['n_runs'], lr['n_runs'], 'brief')
    add('D|D3|short_runs_left_out', 'short_runs (names equal)', True, list(sr['short_runs']) == list(lr['short_runs'].keys()), 'brief')
    add('D|D3|short_runs_left_out', 'evaluated_in_short_runs', sr['evaluated_in_short_runs'], list(lr['short_runs'].values()), 'brief')
    for sname, vv in sr['point'].items():
        add('D|D3|short_runs_left_out', 'point|' + sname, vv, lr['stats'][SM[sname]]['point'], 'brief')
    for sname, vv in sr['ci'].items():
        add('D|D3|short_runs_left_out', 'ci|' + sname, vv, lr['stats'][SM[sname]]['percentile'], 'brief')
    if 'leave_one_run_out' in d3:
        # deterministic: each of the 35 runs left out in turn; min and max of each statistic (computed here, after the outputs were opened)
        from rc_items_v01 import stat_values
        ds = L.load_all(); M = L.build_M(ds, L.masks_all, 'W1', 0., False)
        _, Dl, _ = L.evaluate((np.ones((35, 35)) - np.eye(35)) @ M, 1)
        sv = stat_values(Dl[:, 0])
        for sname, vv in d3['leave_one_run_out'].items():
            x = sv[SM[sname]]
            for kk, val in vv.items():
                if kk in ('min', 'max'):
                    add('D|D3|leave_one_run_out', sname + '|' + kk, val, float(np.min(x) if kk == 'min' else np.max(x)), 'extra')
                else:
                    skipped.append('D|D3|leave_one_run_out|%s|%s' % (sname, kk))
    for k in d3:
        if k not in ('stratified_by_alpha', 'short_runs_left_out', 'alpha_source', 'leave_one_run_out'):
            skipped.append('D|D3_sensitivities|' + k)
    # distinct-value counts: the recount's resample values rounded to 12 decimals
    explanations['R9_n_distinct_recount_rounded_12_decimals'] = {s_: int(np.unique(np.round(rec[SM[s_]][np.isfinite(rec[SM[s_]])], 12)).size) for s_ in D_['D1_draw_of_record']}
    explanations['R9_n_distinct_first_program'] = {s_: t_.get('n_distinct') for s_, t_ in D_['D1_draw_of_record'].items()}
    explanations['first_program_files'] = {f: json.load(open(OUT / f, encoding='utf-8')).get('written') for f in
                                           ('REV_A_SIGNED_GAP_v01.json', 'REV_B_TRUNC_PHASESCALE_v01.json', 'REV_C_RATIO_TRACKS_v01.json', 'REV_D_BOOTSTRAP_v01.json')}


def main():
    A_ = json.load(open(OUT / 'REV_A_SIGNED_GAP_v01.json', encoding='utf-8'))
    B_ = json.load(open(OUT / 'REV_B_TRUNC_PHASESCALE_v01.json', encoding='utf-8'))
    C_ = json.load(open(OUT / 'REV_C_RATIO_TRACKS_v01.json', encoding='utf-8'))
    cnt = json.load(open(H / 'rc_extra_counts_v01.json', encoding='utf-8'))
    i4 = json.load(open(H / 'RECOUNT_item4_v01.json', encoding='utf-8'))
    i6 = json.load(open(H / 'RECOUNT_item6_v01.json', encoding='utf-8'))

    # ------------------------------------------------------------ REV_A: R11
    secmap = {'R11|W1_unsigned_of_record': ('W1_g0', True), 'R11|W1_signed': ('W1_g0_signed', False), 'R17|W1_gap2': ('W1_g2', False),
              'R17|WR_t0p75_a6p0_gap2': ('WR_t0p75_a6p0_g2', False), 'R17|ii_t0p75_a6p0_gap2': ('ii_t0p75_a6p0_g2', True),
              'R17|WR_t1p80_a6p0_gap2': ('WR_t1p80_a6p0_g2', True), 'R17|WR_t0p75_a4p0_gap2': ('WR_t0p75_a4p0_g2', True),
              'R17|WR_t0p75_a5p0_gap2': ('WR_t0p75_a5p0_g2', True), 'R17|WR_t0p75_a7p6_gap2': ('WR_t0p75_a7p6_g2', True)}
    arrs = {}
    for top in ('R11', 'R17'):
        for sk, sv in A_[top].items():
            sec = 'A|%s|%s' % (top, sk)
            if (top + '|' + sk) in secmap:
                name, xs = secmap[top + '|' + sk]
                arr = arrs.setdefault(name, load_arr(name))
                for pop, th in sv.items():
                    if pop in POPS or pop == 'strat':
                        pop_block_A(sec, th, arr, pop, xs)
                    elif pop == 'n_evaluated_without_safe_row':
                        add(sec, pop, th, cnt['no_safe_row'][name], 'extra' if xs else 'brief')
                    else:
                        skipped.append(sec + '|' + pop)
            elif sk == 'n_evaluated_without_W1_safe_row':
                add('A|R11', sk, sv, cnt['n_evaluated_without_W1_safe_row'], 'brief')
            elif sk == 'zero_margin_points_all':
                for a, t in sv.items():
                    for kk, vv in t.items():
                        add('A|R11|zero_margin_points_all', a + '|' + kk, vv, cnt['zero_margin_points_all'][a][kk], 'derived')
            elif sk == 'pair_counts':
                for kk, vv in sv.items():
                    add('A|R17|pair_counts', kk, vv, cnt.get(kk), 'derived')
            else:
                skipped.append(sec)

    # ------------------------------------------------------------ REV_B: R12a
    tr = load_arr('W1_g0_trunc'); w1 = arrs.get('W1_g0') or load_arr('W1_g0')
    TL = (0, 1, 2, 5, 10, 20)
    for tk, th in B_['R12a'].items():
        sec = 'B|R12a|' + tk
        if tk == 'post_stop_segment':
            mine = {s['run']: s for s in cnt['post_stop_segment']}
            for s in th:
                for kk, vv in s.items():
                    if kk != 'run':
                        add('B|R12a|post_stop_segment', s['run'] + '|' + kk, vv, mine[s['run']].get(kk), 'brief' if kk == 'k_stop' else 'derived')
            continue
        if tk == 'Tall':
            n0, D0, nb, Db = pop_arrays(w1, 'all'); xs = True
        elif tk.startswith('T') and tk[1:].isdigit() and int(tk[1:]) in TL:
            n0, D0, nb, Db = pop_arrays(tr, TL.index(int(tk[1:]))); xs = False
        else:
            skipped.append(sec); continue
        om = 'extra' if xs else 'brief'; od = 'extra' if xs else 'derived'
        for k, v in th.items():
            if k == 'T_s':
                add(sec, k, v, None if tk == 'Tall' else float(tk[1:]), om)
            elif k == 'n':
                add(sec, k, v, n0, om)
            elif k == 'R_pp':
                add(sec, k, v, float(D0[1]) / 201, om)
            elif k == 'denE':
                den_block(sec, k, v, float(D0[1]), Db[:, 1], n0, nb, om, od)
            elif k == 'den0':
                den_block(sec, k, v, float(D0[AO]), Db[:, AO], n0, nb, om, od)
            elif k == 'arms':
                for a, t in v.items():
                    c = AI[MAP[a]]
                    oma = 'pre-extra' if (a == 'Q' and om == 'brief') else om
                    for kk, vv in t.items():
                        kkey = 'arms|' + a + '|' + kk
                        if kk == 'D_dec_eq':
                            add(sec, kkey, vv, float(D0[c]) / 201 / 100 * n0, od)
                        elif kk == 'rrE':
                            ratio_block(sec, kkey, vv, D0[c], D0[1], Db[:, c], Db[:, 1], oma, od)
                        elif kk == 'rr0':
                            ratio_block(sec, kkey, vv, D0[c], D0[AO], Db[:, c], Db[:, AO], oma, od)
                        else:
                            skipped.append(sec + '|' + kkey)
            else:
                skipped.append(sec + '|' + k)

    # ------------------------------------------------------------ REV_B: R12b
    z = np.load(H / 'rc_item4_boot_v01.npz'); V = {k: z[k] for k in z.files}
    P4 = {k: v['point'] for k, v in i4['sums'].items()}
    # identities over the same levels (sums of frontier differences): gain_E = sum(F1_E - Fps_E) = gain_F0 + den_ps - den1;
    # Dx(A) = sum(F1_F0 - Fps_A) = gain_F0 + Dps(A)
    P4['gain_E'] = P4['gain_F0'] + P4['den_ps'] - P4['den1']; V['gain_E'] = V['gain_F0'] + V['den_ps'] - V['den1']
    nb4 = V['n']; n4 = P4['n']
    b = B_['R12b']
    sec = 'B|R12b|point'
    for k, v in b['point'].items():
        if k in ('n', 'den1', 'den0_1', 'gain_F0', 'den_ps', 'den0_ps'):
            add(sec, k, v, P4[k], 'brief')
        elif k == 'gain_E':
            add(sec, k, v, P4['gain_E'], 'derived')
        elif k in ('D1', 'Dps', 'Dx'):
            for a, vv in v.items():
                m = MAP[a]
                mine = P4['D1_' + m] if k == 'D1' else (P4['Dps_' + m] if k == 'Dps' else P4['gain_F0'] + P4['Dps_' + m])
                add(sec, k + '|' + a, vv, mine, 'brief' if k != 'Dx' else 'derived')
        elif k == 'n_unique':
            for a, vv in v.items():
                add(sec, k + '|' + a, vv, i4['point_info']['points'][MAP.get(a, a)], 'brief')
        else:
            skipped.append(sec + '|' + k)
    sec = 'B|R12b|summary'
    for k, v in b['summary'].items():
        if k == 'nboot':
            add(sec, k, v, int(nb4.size), 'brief')
        elif k in ('den1', 'den0_1', 'gain_F0', 'gain_E', 'den_ps', 'den0_ps'):
            o = 'derived' if k == 'gain_E' else 'brief'
            for kk, vv in v.items():
                mine = dict(point=P4[k], pp=P4[k] / 201, dec_eq=P4[k] / 201 / 100 * n4, ci=pct(V[k]), pp_ci=pct(V[k] / 201)).get(kk, 'x')
                if isinstance(mine, str):
                    skipped.append(sec + '|' + k + '|' + kk)
                else:
                    add(sec, k + '|' + kk, vv, mine, o if kk in ('point', 'ci') else 'derived')
        elif k in ('gain_F0_over_den1', 'den_ps_over_den1', 'gain_F0_over_den0_1'):
            num, den = k.split('_over_')
            ratio_block(sec, k, v, P4[num], P4[den], V[num], V[den], 'brief' if k != 'gain_F0_over_den0_1' else 'derived', 'derived')
        elif k == 'arms':
            for a, t in v.items():
                m = MAP[a]
                for kk, vv in t.items():
                    kkey = 'arms|' + a + '|' + kk
                    if kk == 'rr_single':
                        ratio_block(sec, kkey, vv, P4['D1_' + m], P4['den1'], V['D1_' + m], V['den1'], 'brief', 'derived')
                    elif kk == 'rr_ps':
                        ratio_block(sec, kkey, vv, P4['Dps_' + m], P4['den_ps'], V['Dps_' + m], V['den_ps'], 'brief', 'derived')
                    elif kk == 'rr0_ps':
                        ratio_block(sec, kkey, vv, P4['Dps_' + m], P4['den0_ps'], V['Dps_' + m], V['den0_ps'], 'brief', 'derived')
                    elif kk == 'Dps_over_den1':
                        ratio_block(sec, kkey, vv, P4['Dps_' + m], P4['den1'], V['Dps_' + m], V['den1'], 'derived', 'derived')
                    elif kk in ('Dps_dec_eq', 'D1_dec_eq'):
                        src = ('Dps_' if kk == 'Dps_dec_eq' else 'D1_') + m
                        add(sec, kkey + '|point', vv['point'], P4[src] / 201 / 100 * n4, 'derived')
                        add(sec, kkey + '|ci', vv['ci'], pct(V[src] / 201 / 100 * nb4), 'derived')
                    else:
                        skipped.append(sec + '|' + kkey)
        elif k == 'draw':
            pass
        else:
            skipped.append(sec + '|' + k)
    for k in b:
        if k not in ('point', 'summary'):
            skipped.append('B|R12b|' + k)

    # ------------------------------------------------------------ REV_C: R20, R19, S9
    for fk, fv in C_['R20'].items():
        if fk.startswith('recount_against'):
            skipped.append('C|R20|' + fk); continue
        for st, t in fv.items():
            mine = cnt['ratio'].get('%s|%s' % (fk, st))
            for kk, vv in t.items():
                if mine is None or kk not in mine:
                    skipped.append('C|R20|%s|%s|%s' % (fk, st, kk)); continue
                o = 'brief' if (st == 'all' and kk in ('rows', 'median_margin_ratio', 'off5_share')) else 'derived'
                add('C|R20', '%s|%s|%s' % (fk, st, kk), vv, mine[kk], o)
    r19 = C_['R19']
    bands = ['<0.5', '0.5-1', '1-2', '2-4', '>=4']
    for k, v in r19.items():
        sec = 'C|R19'
        if k == 'lead_braking_median_margin_ratio':
            add(sec, k, v, i6['families']['lead_braking']['median_m'], 'brief')
        elif k in ('ratio_by_track_age_all55', 'ratio_by_track_age_fit35'):
            ex = i6['extra_lead_braking_all_runs_margin_ratio' if k.endswith('all55') else 'extra_lead_braking_eval_margin_ratio']['by_age']
            for i, row in enumerate(v):
                m = ex[bands[i]]
                mine = dict(rows=m['rows'], off5_n=m['rows_outside_5pct'], off5_share=(m['rows_outside_5pct'] / m['rows'] if m['rows'] else None), median_m=m['median_m'])
                for kk, vv in row.items():
                    if kk in mine:
                        add(sec, '%s|%s|%s' % (k, row['track_age_s'], kk), vv, mine[kk], 'extra')
        elif k == 'evaluated_decisions_fit35':
            pa = i6['lead_braking_eval_prim_age']
            add(sec, k + '|n', v['n'], pa['n'], 'brief')
            for i, row in enumerate(v['by_track_age']):
                add(sec, '%s|by_track_age|%s' % (k, row['track_age_s']), row['n'], pa['bands'][bands[i]]['decisions'], 'brief')
            for kk, vv in v['by_misses'].items():
                add(sec, '%s|by_misses|%s' % (k, kk), vv, cnt['track']['by_misses'].get(kk), 'extra')
            add(sec, k + '|min_track_age_s', v['min_track_age_s'], cnt['track']['min_track_age_s'], 'extra')
            mine = {d['run']: d['n'] for d in cnt['track']['age_drops_in_stored_decisions']}
            add(sec, k + '|age_drops_in_stored_decisions (number of runs)', len(v['age_drops_in_stored_decisions']), len(mine), 'extra')
            for row in v['age_drops_in_stored_decisions']:
                add(sec, '%s|age_drops_in_stored_decisions|%s' % (k, row['run']), row['n'], mine.get(row['run']), 'extra')
            for kk in ('stored_decisions_with_track_younger_than_4s', 'stored_not_evaluated'):
                add(sec, k + '|' + kk, v[kk], cnt['track'][kk], 'extra')
        elif k in ('track_younger_than_4s', 'track_4s_or_older'):
            ag = load_arr('W1_g0_age'); p = 0 if k == 'track_younger_than_4s' else 1
            n0 = float(ag['n0'][p]); D0 = ag['D0'][p]
            mine = dict(n=n0, denE=float(D0[1]), den0=float(D0[AO]), den0_dec_eq=float(D0[AO]) / 201 / 100 * n0, denE_dec_eq=float(D0[1]) / 201 / 100 * n0,
                        D_N_dec_eq=float(D0[AI['N']]) / 201 / 100 * n0, D_NA_dec_eq=float(D0[AI['NA']]) / 201 / 100 * n0)
            for kk, vv in v.items():
                if kk in mine:
                    add(sec, k + '|' + kk, vv, mine[kk], 'extra')
                else:
                    skipped.append(sec + '|' + k + '|' + kk)
        else:
            skipped.append(sec + '|' + k)
    for k, v in C_['S9'].items():
        if k in ('n_off', 'n_runs_with_off_rows'):
            add('C|S9', k, v, cnt['S9'][k], 'extra')
        elif k in ('by_set', 'by_phase_fit_only'):
            for kk, vv in v.items():
                add('C|S9', k + '|' + kk, vv, cnt['S9'][k].get(kk), 'extra')
        else:
            skipped.append('C|S9|' + k)

    # ------------------------------------------------------------ REV_D: R9
    explanations = {}
    compare_D(explanations)

    # ------------------------------------------------------------ tests of the explanations of the differences
    # (i) R12b decision-equivalent intervals: does scaling every resample by the FULL-sample n reproduce the first program?
    alt = []
    for a, t in b['summary']['arms'].items():
        for kk in ('Dps_dec_eq', 'D1_dec_eq'):
            if kk in t:
                src = ('Dps_' if kk == 'Dps_dec_eq' else 'D1_') + MAP[a]
                c = pct(V[src] / 201 / 100 * n4)
                alt += [abs(c[0] - t[kk]['ci'][0]), abs(c[1] - t[kk]['ci'][1])]
    explanations['R12b_dec_eq_ci_with_full_sample_n'] = dict(n_values=len(alt), max_abs_diff_to_first_program=float(max(alt)) if alt else None)
    # (ii) ratio points the first program leaves undefined: is the recount's point denominator <= 0 in each, and only there?
    chk = dict(first_program_undefined=0, of_which_recount_denominator_le0=0, recount_denominator_le0_but_first_program_gives_a_number=0)
    for sk, sv in A_['R17'].items():
        if ('R17|' + sk) not in secmap:
            continue
        arr = arrs[secmap['R17|' + sk][0]]
        for pop in POPS + ('strat',):
            n0, D0, nb, Db = pop_arrays(arr, pop)
            blocks = [(t[kk], col) for a, t in sv[pop]['arms'].items() if a in MAP for kk, col in (('rrE', 1), ('rr0', AO))]
            blocks.append((sv[pop]['E_rr0'], AO))
            for blk, col in blocks:
                if und(blk['point']):
                    chk['first_program_undefined'] += 1; chk['of_which_recount_denominator_le0'] += int(not (D0[col] > 0))
                elif not (D0[col] > 0):
                    chk['recount_denominator_le0_but_first_program_gives_a_number'] += 1
    explanations['undefined_ratio_points_under_the_gap'] = chk

    # ------------------------------------------------------------ consistency of the stored arrays with RECOUNT_RESULTS_v01.json
    R = json.load(open(H / 'RECOUNT_RESULTS_v01.json', encoding='utf-8'))
    cons = []

    def cons_table(e, n0, D0, nb, Db, tag):
        def c(name, mine_pt, mine_ci=None):
            cons.append(abs(e[name]['point'] - mine_pt) if e[name]['point'] is not None and np.isfinite(mine_pt) else 0.)
            if mine_ci is not None and e[name].get('ci') is not None:
                cons.extend([abs(e[name]['ci'][0] - mine_ci[0]), abs(e[name]['ci'][1] - mine_ci[1])])
        c('denE', float(D0[1]), pct(Db[:, 1])); c('den0', float(D0[AO]), pct(Db[:, AO])); c('R_pp', float(D0[1]) / 201, pct(Db[:, 1] / 201))
        c('den0_deceq', float(D0[AO]) / 201 / 100 * n0, pct(Db[:, AO] / 201 / 100 * nb))
        for a in ('N', 'NA', 'AM', 'CK3', 'Q'):
            for nm, col in (('RR_', 1), ('RR0_', AO)):
                v = np.isfinite(Db[:, col]) & (Db[:, col] > 0)
                c(nm + a, float(div(D0[AI[a]], D0[col])), pct(Db[v, AI[a]] / Db[v, col]))
    for name, node in (('W1_g0_signed', R['item1']['pops']), ('W1_g2', R['item2']['scorings']['a_3s_commitment']['pops']),
                       ('WR_t0p75_a6p0_g2', R['item2']['scorings']['b_reaction_and_stop_t0p75_a6p0']['pops'])):
        arr = arrs.get(name) or load_arr(name)
        for pop in POPS + ('strat',):
            cons_table(node['phase_weighted' if pop == 'strat' else pop], *pop_arrays(arr, pop), tag=name)
    for ti, T in enumerate(TL):
        cons_table(R['item3']['T'][str(T)], *pop_arrays(tr, ti), tag='trunc')
    cons_max = float(np.nanmax(cons)) if cons else 0.

    # ------------------------------------------------------------ write
    num = [r for r in recs if r.get('kind') != 'flag']
    flags = [r for r in recs if r.get('kind') == 'flag']
    ndiff = [r for r in num if r['status'] == 'DIFF']; fdiff = [r for r in flags if r['status'] == 'DIFF']
    res = dict(written=time.strftime('%Y-%m-%d %H:%M:%S'), tolerance=TOL, n_numbers_compared=len(num), n_numbers_differ=len(ndiff),
               n_both_undefined=sum(r['status'] == 'both undefined' for r in num), n_flags_compared=len(flags), n_flags_differ=len(fdiff),
               max_abs_diff=max([r['diff'] for r in num if r['diff'] is not None] or [0.]),
               consistency_arrays_vs_results_json=dict(n=len(cons), max_abs_diff=cons_max), explanations=explanations,
               not_compared=skipped, records=recs)
    L.jdump(res, H / 'RECOUNT_COMPARE_v01.json')
    print('numbers compared %d, differ %d, both undefined %d; flags compared %d, differ %d; largest difference %.3g; not compared %d leaves; consistency %d values, max %.3g'
          % (len(num), len(ndiff), res['n_both_undefined'], len(flags), len(fdiff), res['max_abs_diff'], len(skipped), len(cons), cons_max))
    by = {}
    for r in num:
        k = (r['sec'].split('|')[0] + '|' + r['sec'].split('|')[1] + ('|' + r['sec'].split('|')[2] if len(r['sec'].split('|')) > 2 else ''), r['origin'])
        b_ = by.setdefault(k, [0, 0, 0, 0.])
        b_[0] += 1; b_[1] += r['status'] == 'DIFF'; b_[2] += r['status'] == 'both undefined'
        if r['diff'] is not None:
            b_[3] = max(b_[3], r['diff'])
    for k in sorted(by):
        print('  %-40s %-8s n %5d  differ %3d  both undefined %3d  max diff %.3g' % (k[0], k[1], by[k][0], by[k][1], by[k][2], by[k][3]))
    for r in ndiff[:60]:
        print('  DIFF', r['sec'], r['key'], r['th'], r['mine'], r['diff'], r['origin'])
    for r in fdiff[:20]:
        print('  FLAG DIFF', r['sec'], r['key'], r['th'], r['mine'])
    print('not compared (first 60):', skipped[:60])
    print('explanations', json.dumps(explanations)[:2500])
    write_md(res)


def g(x):
    if und(x):
        return 'undefined'
    if isinstance(x, bool) or isinstance(x, str):
        return str(x)
    if isinstance(x, int):
        return '%d' % x
    return repr(float(x))


def write_md(res):
    recs_ = res['records']
    num = [r for r in recs_ if r.get('kind') != 'flag']; flags = [r for r in recs_ if r.get('kind') == 'flag']
    nd = [r for r in num if r['status'] == 'DIFF']; fd = [r for r in flags if r['status'] == 'DIFF']
    ex = res['explanations']

    def group(r):
        k = r['key']
        if r['sec'].startswith('A|R17') and ('|rrE|point' in k or '|rrE|basic' in k) and und(r['th']):
            return 1
        if r['sec'] == 'B|R12b|summary' and ('dec_eq|ci' in k):
            return 2
        if r['sec'] == 'D|D1_draw_of_record' and k.endswith('n_distinct'):
            return 3
        return 0
    G = {i: [r for r in nd if group(r) == i] for i in (0, 1, 2, 3)}
    W = []
    w = W.append
    w('# Comparison of the recount (second program) with the first program, revision v11')
    w('')
    w('Written %s by `rc_compare_v01.py`, after `RECOUNT_RESULTS_v01.json` and `RECOUNT_REPORT_v01.md` were written. Only the first program\'s output files '
      '`revision_v11\\analysis\\out\\*.json` were read (never its code): %s. Tolerance: 1e-9 absolute, points and intervals alike (the intervals use the same draws).'
      % (res['written'], '; '.join('`%s` (written %s)' % (k, v) for k, v in ex.get('first_program_files', {}).items())))
    w('')
    w('## 1. Result')
    w('')
    nb = [r for r in num if r['origin'] == 'brief']
    w('- Numeric leaves of the first program\'s files that have a counterpart in the recount: **%d** (of these, %d are undefined in both programs, e.g. a ratio with a zero denominator or an empty band).' % (len(num), res['n_both_undefined']))
    w('- Differ beyond 1e-9: **%d**. Largest absolute difference among the %d that agree: %.3g.' % (len(nd), len(num) - len(nd) - res['n_both_undefined'], max([r['diff'] for r in num if r['status'] == 'ok'] or [0.])))
    w('- Of the %d numbers that are on the brief\'s list (class "brief": computed and written before the first program\'s outputs were opened): **%d differ**.' % (len(nb), sum(r['status'] == 'DIFF' for r in nb)))
    w('- True/false leaves compared: %d; differ: %d (all are the "point outside its interval" flag of the ratios of group 1 below).' % (len(flags), len(fd)))
    w('- The %d differences fall in three groups, each a difference of convention that was traced to its cause; none is a disagreement between the two scorings:' % len(nd))
    w('  1. %d numbers: ratios to denE under the 2 m gap whose point denominator is not positive. The first program prints no value; the recount printed the quotient.' % len(G[1]))
    w('  2. %d numbers: the decision-equivalent interval ends of the per-phase-scale table (R12b). The first program multiplies every resample by the full-sample n; the recount by the resample\'s own n.' % len(G[2]))
    w('  3. %d numbers: the count of distinct resample values (R9, draw of record), which depends on the last floating-point bit.' % len(G[3]))
    if G[0]:
        w('  4. **%d numbers not explained** (listed in section 3.4).' % len(G[0]))
    w('- The stored per-resample arrays used here reproduce the recount\'s own results file: %d values re-formed, largest difference %.3g.' % (res['consistency_arrays_vs_results_json']['n'], res['consistency_arrays_vs_results_json']['max_abs_diff']))
    w('')
    w('Classes of a compared number: **brief** = on the brief\'s list and in `RECOUNT_RESULTS_v01.json` (written before the outputs were opened); **pre-extra** = in that file but not on the brief\'s list; '
      '**derived** = formed at comparison time from the recount\'s stored points, resamples or counts by a fixed formula (decision-equivalents, pp, basic interval, shares of non-positive denominators, further quantiles and coverages); '
      '**extra** = an arm, population or scoring the first program printed beyond the brief (CK3 with F0\'s zero-margin point, the partial oracles P25/P50/P75, the published unsigned table, the other reaction-and-stop settings and count (ii) under the gap, track-age populations, leave-one-run-out), computed by `rc_extra_v01.py` after the outputs were opened, from the brief\'s definitions and the allowed second-program library.')
    w('')
    w('## 2. Agreement by file and section')
    w('')
    w('| first-program file, section | class | numbers | differ | undefined in both | largest difference among those that agree |')
    w('|---|---|---|---|---|---|')
    by = {}
    for r in num:
        p = r['sec'].split('|')
        k = ('|'.join(p[:3]), r['origin'])
        b_ = by.setdefault(k, [0, 0, 0, 0.])
        b_[0] += 1; b_[1] += r['status'] == 'DIFF'; b_[2] += r['status'] == 'both undefined'
        if r['status'] == 'ok':
            b_[3] = max(b_[3], r['diff'])
    names = dict(A='REV_A_SIGNED_GAP', B='REV_B_TRUNC_PHASESCALE', C='REV_C_RATIO_TRACKS', D='REV_D_BOOTSTRAP')
    for k in sorted(by):
        w('| %s, %s | %s | %d | %d | %d | %.3g |' % (names[k[0][0]], k[0][2:].replace('|', ' / '), k[1], by[k][0], by[k][1], by[k][2], by[k][3]))
    tot = {}
    for (s_, o), v in by.items():
        t = tot.setdefault(o, [0, 0, 0]); t[0] += v[0]; t[1] += v[1]; t[2] += v[2]
    w('')
    w('Totals by class: ' + '; '.join('%s %d compared, %d differ' % (o, t[0], t[1]) for o, t in sorted(tot.items())) + '.')
    w('')
    w('Brief items against sections: item 1 (R11) = REV_A R11 / W1_signed; item 2 (R17) = REV_A R17 / W1_gap2 and WR_t0p75_a6p0_gap2; item 3 (R12a) = REV_B R12a; item 4 (R12b) = REV_B R12b; '
      'item 5 (R9) = REV_D; item 6 (R19 / R20) = REV_C. The population the first program calls "strat" is the phase-weighted aggregate; its arm "A1" is AM.')
    w('')
    w('## 3. The differences')
    w('')
    w('### 3.1 Ratios to denE under the 2 m gap, point denominator not positive (%d numbers, %d flags)' % (len(G[1]), len(fd)))
    c = ex.get('undefined_ratio_points_under_the_gap', {})
    w('With the 2 m requirement the stored oracle margin source E is no longer better than the class average in several populations, so denE at the point is negative or zero there. '
      'For those cells the first program prints no point for the share of denE (NaN), hence no basic interval and "outside" = false; the recount printed the arithmetic quotient D / denE and the basic interval built on it. '
      'The percentile intervals of the same cells (over the resamples with a positive denominator) agree, and so do denE, den0, D and every RR0. '
      'Check: over all seven gap-2 scorings the first program leaves %s ratio points undefined; in %s of them the recount\'s point denominator is <= 0; cells where the recount\'s point denominator is <= 0 and the first program still prints a number: %s. '
      'Cause: the brief defines the interval over resamples with a positive denominator and does not say what the point is when its own denominator is not positive; the first program\'s reading (no value) is the sound one, since a share of a non-positive room has no meaning. '
      'These cells are not on the brief\'s list for item 2 (which asks for RR0, not for the share of denE). No number the paper could quote is affected.'
      % (c.get('first_program_undefined'), c.get('of_which_recount_denominator_le0'), c.get('recount_denominator_le0_but_first_program_gives_a_number')))
    w('')
    w('| section | key | first program | recount | class |')
    w('|---|---|---|---|---|')
    for r in G[1]:
        w('| %s | %s | %s | %s | %s |' % (r['sec'][2:].replace('|', ' / '), r['key'].replace('|', ' / '), g(r['th']), g(r['mine']), r['origin']))
    w('')
    w('Flags that differ (first program false, recount true): ' + '; '.join('%s / %s' % (r['sec'][2:].replace('|', ' / '), r['key'].replace('|', ' / ')) for r in fd) + '.')
    w('')
    w('### 3.2 Decision-equivalent intervals of the per-phase-scale table, R12b (%d numbers)' % len(G[2]))
    e2 = ex.get('R12b_dec_eq_ci_with_full_sample_n', {})
    w('Points agree. For the interval of a sum D expressed in decisions the recount takes the percentiles of D_b / 201 / 100 * n_b, with n_b the number of evaluated decisions of resample b (the rule of the project\'s Option A clarifications, and the rule the first program itself follows in REV_A, where all %d decision-equivalent interval ends agree). '
      'In REV_B R12b the first program\'s values equal the percentiles of D_b / 201 / 100 * 8290, the full-sample n: recomputed that way from the recount\'s resamples, all %s interval ends reproduce the first program\'s with largest difference %s. '
      'So the two programs agree on every resample value; the first program applies two different conventions in its two files. These decision-equivalent intervals are not on the brief\'s list.'
      % (sum(1 for r in num if r['sec'].startswith('A|') and 'dec_eq_ci' in r['key'] and r['status'] == 'ok'), e2.get('n_values'), e2.get('max_abs_diff_to_first_program')))
    w('')
    w('| key | first program (full-sample n) | recount (resample\'s own n) | absolute difference |')
    w('|---|---|---|---|')
    for r in G[2]:
        w('| %s | %s | %s | %.6g |' % (r['key'].replace('|', ' / '), g(r['th']), g(r['mine']), r['diff']))
    w('')
    w('### 3.3 Number of distinct resample values, R9 draw of record (%d numbers)' % len(G[3]))
    w('The recount counts values that differ in any floating-point bit; the first program\'s counts are smaller. Rounding the recount\'s resample values to 12 decimals (any of 10 to 13 gives the same) reproduces the first program\'s eight counts exactly: %s. '
      'For example 156 resamples have RR(N) equal to zero up to 1e-12 and not exactly zero in the recount. Every quantile, mean, standard deviation and share of the same draw agrees to 1e-9, so this is floating-point identity and not a difference of the draw or of the scoring.'
      % '; '.join('%s %s' % (k, v) for k, v in ex.get('R9_n_distinct_recount_rounded_12_decimals', {}).items()))
    w('')
    w('| statistic | first program | recount (exact floating-point values) | recount rounded to 12 decimals |')
    w('|---|---|---|---|')
    for r in G[3]:
        s_ = r['key'].split('|')[0]
        w('| %s | %s | %s | %s |' % (s_, g(r['th']), g(r['mine']), ex.get('R9_n_distinct_recount_rounded_12_decimals', {}).get(s_)))
    w('')
    if G[0]:
        w('### 3.4 Differences without an explanation (%d)' % len(G[0]))
        w('')
        w('| section | key | first program | recount | absolute difference | class |')
        w('|---|---|---|---|---|---|')
        for r in G[0]:
            w('| %s | %s | %s | %s | %s | %s |' % (r['sec'], r['key'], g(r['th']), g(r['mine']), r['diff'], r['origin']))
        w('')
    w('## 4. A reading that mattered and on which the two programs agree: the coverage rule of R9')
    w('The brief\'s rule compares shares of 1,000 inner values with a/2 and 1 - a/2. Evaluated in exact arithmetic (the recount\'s primary reading) all %d coverage values and all calibrated levels and intervals of the first program are reproduced. '
      'Evaluated naively in floating point, (1 - 0.95)/2 is 0.025000000000000022 and an outer sample with exactly 25 of 1,000 inner values at or below the truth is no longer covered. The recount computed both before the outputs were opened:'
      % sum(1 for r in num if r['sec'] == 'D|D2_double_bootstrap' and '|coverage_' in r['key']))
    w('')
    w('| statistic | coverage at nominal 0.95, exact rule | float rule | calibrated level, exact rule | float rule |')
    w('|---|---|---|---|---|')
    for s_ in ex.get('R9_coverage_at_095_exact_rule_and_float_rule', {}):
        a_ = ex['R9_coverage_at_095_exact_rule_and_float_rule'][s_]; b_ = ex['R9_calibrated_level_exact_rule_and_float_rule'][s_]
        w('| %s | %s | %s | %s | %s |' % (s_, a_[0], a_[1], b_[0], b_[1]))
    w('')
    w('The first program\'s numbers are those of the exact rule. Nothing differs; the table records how far a float reading would have moved the result (at most 0.0015 in a coverage and 0.001 in a calibrated level).')
    w('')
    w('## 5. Not compared')
    w('Leaves of the first program\'s four files without a counterpart in the recount: %s.' % ('; '.join('`%s`' % s_ for s_ in res['not_compared']) or 'none'))
    w('')
    w('Reasons: the m-out-of-n subsampling has no draw in the brief; `m_histogram`, `per_run` and `share_in_top5_runs` are diagnostics of the rows outside the 5 percent band beyond the counts compared; the others are notes, timings and the first program\'s own self-checks. '
      'Files of the first program not compared at all, because the recount brief does not cover their analyses: `REV_E1`, `REV_E2`, `REV_E3` (R10, extended truth), `REV_F1`, `REV_F2` (braking prior), `REV_G` (partial oracles over 50 draws), `REV_H` (run facts), `IDENTITY_REV` (the first program\'s identity check). '
      'Numbers of the recount without a counterpart in the first program: the truncation sensitivity (k_stop from the first evaluated phase-2 decision), the float-rule coverages, and the item-4 enumeration checks.')
    w('')
    w('## 6. Every compared number')
    w('Status: ok = within 1e-9; DIFF = beyond; both undefined = no value in either program; equal / DIFF for true-false leaves. Full precision is also in `RECOUNT_COMPARE_v01.json`.')
    w('')
    w('| section | key | first program | recount | abs. difference | class | status |')
    w('|---|---|---|---|---|---|---|')
    for r in recs_:
        w('| %s | %s | %s | %s | %s | %s | %s |' % (r['sec'], r['key'].replace('|', ' / '), g(r['th']), g(r['mine']), '' if r['diff'] is None else '%.3g' % r['diff'], r['origin'], r['status']))
    (H / 'RECOUNT_COMPARE_v01.md').write_text('\n'.join(W) + '\n', encoding='utf-8')
    print('written RECOUNT_COMPARE_v01.md (%d lines)' % len(W))


if __name__ == '__main__':
    main()
