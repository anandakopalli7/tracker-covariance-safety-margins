"""Write session A's exports for packages C and D (work/A_text/RESULTS_INTERFACE_v13.md sec. 1): out/A_EXPORT_C.json and
out/A_EXPORT_D.json from the first programs; out/A_RECOUNT_C.json and out/A_RECOUNT_D.json from the second programs, with the same
keys. New file, 20 Nov 2026 (Claude Opus 5.5), written before Lock 2. The mapping is clerical: no value is computed here except counts
read from run summaries (contact runs), 1 - share for LB.R.nonpos_share, and Fig. 2's frontier curves (frontiers_first, add4).

Usage: python -I make_export_cd_v13.py first|second [--test-old]
Inputs (first): analysis/out/{C_LEAD_H0_H5_v13, C_CUTIN_K0_K2_v13, D_NONBRAKING_DH1_DH2_v13, D2_EVENT_TABLE_v13}.json and the family
outputs analysis/out/{S57A, TRK, B7, S57B}_v13.json (each with a flat "values" dict under A's names). Second: recount/out/{RC_C_LEAD_v13,
RC_C_CUTIN_v13, RC_S57A_v13, RC_TRK_v13, RC_S57B_v13}.json, recount_d/out/{RC_D_NONBRAKING_v13, RC_D2_EVENT_TABLE_v13}.json.
--test-old: the TESTOLD_ variants (old runs), written to out/TESTOLD_A_{EXPORT|RECOUNT}_{C|D}.json.
Precedence: the core outputs first; a family value for a key the core already has is checked for equality (1e-9) and listed in
"overlaps"; families fill the rest. Keys of A's list that no input produces are listed in "not_produced" (required ones first).
"""
import datetime, hashlib, json, math, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; REV = CD.parent.parent
LOCK2 = REV / 'LOCK_A10_2.txt'
KEYS = json.loads((HERE / 'A_KEYS_CD_v13.json').read_text(encoding='utf-8'))['keys']
ARGS = sys.argv[1:]; WHO = ARGS[0]; TEST = '--test-old' in ARGS
PFX = 'TESTOLD_' if TEST else ''


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


OVR = {k: ARGS[ARGS.index('--' + k) + 1] for k in ('lead', 'cutin', 'dnb', 'd2') if '--' + k in ARGS}
ROLE = {}


def load(p, role=None):
    p = pathlib.Path(OVR[role]) if role in OVR else pathlib.Path(p)
    return (json.loads(p.read_text(encoding='utf-8')), p) if p.is_file() else (None, p)


def fnum(x):
    if x is None: return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(x) or math.isinf(x) else x


def fpair(c):
    if c is None or not isinstance(c, (list, tuple)) or len(c) != 2: return None
    a, b = fnum(c[0]), fnum(c[1])
    return None if a is None or b is None else [a, b]


def cal_first(level, rule):
    if rule and str(rule).startswith('calibrated'): return 'calibrated'
    return 'nominal99' if level is not None and abs(float(level) - 0.99) < 1e-12 else 'nominal95'


def cal_second(st):
    if not st: return None
    lev = st.get('level_used'); cl = st.get('calibrated_level')
    if cl is not None and lev is not None and abs(float(lev) - float(cl)) < 1e-12: return 'calibrated'
    return 'nominal99' if lev is not None and abs(float(lev) - 0.99) < 1e-12 else 'nominal95'


class V(dict):
    def iv(self, key, point, ci, level, cal):
        self[key] = fnum(point); self[key + '.ci'] = fpair(ci)
        self[key + '.level'] = None if level is None else float(level); self[key + '.cal'] = cal

    def nominal(self, key, d, cikey='ci'):              # a descriptive summary with a nominal 95% interval
        if d is None: self.iv(key, None, None, 0.95, 'nominal95'); return
        self.iv(key, d.get('point'), d.get(cikey), 0.95, 'nominal95')


def contacts(prefix):
    """Runs ending at first contact (A10 sec. 5.1), from the run summaries (first_contact_frame not null)."""
    if TEST: return None
    n = 0; seen = 0
    for s in (CD / 'runs').glob(prefix + '*/' + prefix + '*/SUMMARY.json'):
        d = json.loads(s.read_text(encoding='utf-8')); seen += 1
        n += d.get('first_contact_frame') is not None
    return n if seen else None


# ------------------------------------------------------------------------------------------------ first programs
def first_c(v, src):
    lead, p = load(CD / 'analysis' / 'out' / f'{PFX}C_LEAD_H0_H5_v13.json', 'lead'); src[str(p)] = lead is not None
    if lead:
        S, CM = lead['main'], lead['calibration_main']
        for ka, kk in (('R', 'R_gl'), ('RR_E5', 'RR_E5'), ('RR_E5mP', 'RR_E5_minus_E5p'), ('RR_N', 'RR_N'), ('RR_CK3', 'RR_CK3')):
            v.iv('LB.' + ka, S[kk]['point'], S[kk].get('ci_level'), CM[kk]['level'], cal_first(CM[kk]['level'], CM[kk].get('rule')))
        v['LB.R.dec'] = fnum(lead['room']['R_deceq']); v['LB.R.nonpos_share'] = fnum(1. - lead['room']['share_resamples_denE_gt0'])
        v['LB.n_dec'] = int(lead['room']['n']); v['LB.n_runs'] = int(lead['n_runs'])
        h3 = lead['H3']
        if h3.get('status') == 'run':
            cal = h3.get('calibration', {})
            for nm in ('r', 'c'):
                lev = cal.get(nm, {}).get('level', 0.95)
                v.iv('LB.IMM.' + nm, h3[nm]['point'], h3[nm].get('ci_level'), lev, cal_first(lev, cal.get(nm, {}).get('rule')))
            eff = h3.get('efficiency_r_over_c'); lev = cal.get('r', {}).get('level', 0.95)
            v.iv('LB.IMM.eff', eff and eff['point'], eff and eff.get('ci_level'), lev, cal_first(lev, cal.get('r', {}).get('rule')))
            v['LB.IMM.within5'] = fnum(h3['ratio_summary'].get('share_within_5pct'))
        h4 = lead['H4']; c4 = h4.get('calibration', {}).get('share_record', {}); l4 = c4.get('level', 0.95)
        v.iv('LB.PS.rec', h4['record_basis']['point'], h4['record_basis'].get('ci_level'), l4, cal_first(l4, c4.get('rule')))
        v.nominal('LB.PS.like', h4['like_for_like']); v.nominal('LB.PS.single', h4.get('single_scale'))
        for ka, kk in (('truth', 'truth_phase'), ('thr05', 'thr_-0.5'), ('thr20', 'thr_-2.0')):
            v.nominal('LB.PS.' + ka, h4['sensitivities'][kk]['record_basis'])
        for ka, kk in (('NA', 'NA'), ('AM', 'A1'), ('Q', 'Q'), ('TG', 'TG')):     # all evaluated decisions = LB.all (also W3's family)
            v.nominal('LB.all.RR_' + ka, lead['descriptive_RR_gl'].get(kk))
        v['LB.n_contact'] = None if TEST else contacts_list(lead['runs']); v['LB.n_replaced'] = None if TEST else 0
    cut, p = load(CD / 'analysis' / 'out' / f'{PFX}C_CUTIN_K0_K2_v13.json', 'cutin'); src[str(p)] = cut is not None
    if cut:
        K0, K1, K2, D = cut['K0'], cut['K1'], cut['K2'], cut['descriptive']
        cw = K0.get('calibration', {})
        v.iv('CI.R', K0['R_gl']['point'], K0['R_gl'].get('ci_level'), cw.get('R_gl', {}).get('level', 0.95),
             cal_first(cw.get('R_gl', {}).get('level', 0.95), cw.get('R_gl', {}).get('rule')))
        v.iv('CI.RR_N', K1['RR_N']['point'], K1['RR_N'].get('ci_level'), cw.get('RR_N', {}).get('level', 0.95),
             cal_first(cw.get('RR_N', {}).get('level', 0.95), cw.get('RR_N', {}).get('rule')))
        v['CI.den0.dec'] = fnum(K0['den0_deceq'])
        y = D.get('young', {})
        v['CI.Y.n_dec'] = int(y.get('n', 0))
        v['CI.Y.R.dec'] = 0.0 if v['CI.Y.n_dec'] == 0 else fnum((y.get('R_deceq') or {}).get('point'))   # no young decision: no room (K2's rule)
        v['CI.Y.within5'] = fnum((y.get('ratio') or {}).get('share_within_5pct'))
        if K2.get('status') == 'evaluated':
            cy = K2.get('calibration', {})
            for nm in ('r', 'c'):
                lev = cy.get(nm, {}).get('level', 0.95)
                v.iv('CI.Y.' + nm, K2[nm]['point'], K2[nm].get('ci_level'), lev, cal_first(lev, cy.get(nm, {}).get('rule')))
            eff = K2.get('efficiency_r_over_c'); lev = cy.get('r', {}).get('level', 0.95)
            v.iv('CI.Y.eff', eff and eff['point'], eff and eff.get('ci_level'), lev, cal_first(lev, cy.get('r', {}).get('rule')))
        else:
            for nm in ('r', 'c', 'eff'): v.iv('CI.Y.' + nm, None, None, None, None)
        for ka, kk in (('age0', 'young'), ('age1', 'mid'), ('age4', 'old'), ('untr', 'untracked')):
            d = D.get(kk, {})
            v[f'CI.{ka}.R.dec'] = fnum((d.get('R_deceq') or {}).get('point')); v[f'CI.{ka}.RR_N'] = fnum((d.get('RR_N') or {}).get('point'))
            v[f'CI.{ka}.n_dec'] = int(d.get('n', 0)); v[f'CI.{ka}.within5'] = fnum((d.get('ratio') or {}).get('share_within_5pct'))
        v['CI.n_dec'] = int(D['window']['n']); v['CI.n_runs'] = len(cut['runs'])
        v['CI.n_events'] = len(cut['runs']) - len(cut['runs_without_event'])
        v['CI.n_contact'] = contacts_cutin(cut); v['CI.n_replaced'] = None if TEST else 0


def contacts_cutin(cut):
    if TEST: return None
    n = 0; seen = 0
    for r in cut['runs']:
        s = CD / 'runs' / r['run'] / r['run'] / 'SUMMARY.json'
        if s.is_file():
            seen += 1; n += json.loads(s.read_text(encoding='utf-8')).get('first_contact_frame') is not None
    return n if seen == len(cut['runs']) else None


DV = (('const', 'constant'), ('mild', 'mild_braking'), ('stopgo', 'stop_and_go'))
D2C = (('c2', '2%'), ('c5', '5%'))


def first_d(v, src):
    d, p = load(CD / 'analysis' / 'out' / f'{PFX}D_NONBRAKING_DH1_DH2_v13.json', 'dnb'); src[str(p)] = d is not None
    if d:
        tot = 0
        for ka, kk in DV:
            var = d['variants'].get(kk)
            if var is None: continue
            tot += var['n_runs']
            for s in ('N', 'CK3', 'PS', 'TG'):
                so = var['sources'].get(s, {})
                v.nominal(f'D1.{ka}.{s}.dcau', so.get('caution_diff_pp')); v.nominal(f'D1.{ka}.{s}.dwg', so.get('wrong_go_diff_pp'))
        v['D1.n_runs'] = tot if tot else None
        nd = [d['variants'][kk]['sources']['F0'].get('decisions') for _, kk in DV if kk in d['variants']]
        v['D1.n_dec'] = int(sum(nd)) if nd and None not in nd else None
        v['D1.n_contact'] = None if TEST else contacts_list([r for _, kk in DV for r in d['variants'].get(kk, {}).get('runs', [])])
        v['D1.n_replaced'] = None if TEST else 0
    t, p = load(CD / 'analysis' / 'out' / f'{PFX}D2_EVENT_TABLE_v13.json', 'd2'); src[str(p)] = t is not None
    trs, prs = load(CD / 'analysis' / 'out' / f'{PFX}D2_RS_v13.json', 'd2rs'); src[str(prs)] = trs is not None
    # 3 s column from the stage-1 D2 script; reaction-and-stop column (judged until the stop ends, A10 sec. 1) from d2_rs_v13.py (stage 2)
    for sk, scn, tt in (('w3', '3s', t), ('rs', 'RS075', trs)):
        if tt:
            tab = tt['table'].get(scn)
            if tab is None: continue
            for s in ('F0', 'N', 'CK3', 'TG'):
                for ck, cc in D2C:
                    e = tab.get(s, {}).get(cc)
                    if e is None: continue
                    v[f'D2.{s}.{ck}.{sk}.runs'] = int(e['runs_with_wrong_go']); v[f'D2.{s}.{ck}.{sk}.vclose'] = fnum(e['median_of_run_medians'])


def contacts_list(rids):
    n = 0; seen = 0
    for r in rids:
        s = CD / 'runs' / r / r / 'SUMMARY.json'
        if s.is_file():
            seen += 1; n += json.loads(s.read_text(encoding='utf-8')).get('first_contact_frame') is not None
    return n if rids and seen == len(rids) else None


# ------------------------------------------------------------------------------------------------ second programs
def second_c(v, src):
    lead, p = load(CD / 'recount' / 'out' / ('RC_C_LEAD_TESTOLD_v13.json' if TEST else 'RC_C_LEAD_v13.json'), 'lead'); src[str(p)] = lead is not None
    if lead:
        I, CS = lead['intervals'], lead['calibration']['stats']
        for ka, kk in (('R', 'R_gl_pp'), ('RR_E5', 'RR_E5'), ('RR_E5mP', 'RR_E5_minus_E5p'), ('RR_N', 'RR_N'), ('RR_CK3', 'RR_CK3')):
            v.iv('LB.' + ka, I[kk]['point'], I[kk]['ci'], I[kk]['level'], cal_second(CS.get(kk)))
        v['LB.R.dec'] = fnum(lead['point']['gridless']['R_gl_deceq']); v['LB.R.nonpos_share'] = fnum(1. - lead['bootstrap']['share_den_gt0'])
        v['LB.n_dec'] = int(lead['counts']['n_evaluated']); v['LB.n_runs'] = int(lead['counts']['n_runs'])
        h3 = lead['hypotheses'].get('H3', {})
        if 'r' in h3:
            for nm in ('r', 'c'):
                v.iv('LB.IMM.' + nm, h3[nm]['point'], h3[nm]['ci'], h3[nm]['level'], cal_second(CS.get('IMM_' + nm)))
            eff = h3.get('efficiency_r_over_c')
            v.iv('LB.IMM.eff', eff and eff['point'], eff and eff['ci'], h3['r']['level'], cal_second(CS.get('IMM_r')))
            v['LB.IMM.within5'] = fnum(lead.get('IMM', {}).get('margin_ratio', {}).get('share_within_5pct'))
        k4 = 'H4_rec_est_-1.0'
        v.iv('LB.PS.rec', I[k4]['point'], I[k4]['ci'], I[k4]['level'], cal_second(CS.get(k4)))
        lf = I['H4_lfl_est_-1.0']; v.iv('LB.PS.like', lf['point'], lf['ci95'], 0.95, 'nominal95')
        for ka, kk in (('truth', 'truth'), ('thr05', 'est_-0.5'), ('thr20', 'est_-2.0')):
            x = I['H4_rec_' + kk]; v.iv('LB.PS.' + ka, x['point'], x['ci95'], 0.95, 'nominal95')
        for ka, kk in (('NA', 'NA'), ('AM', 'A1'), ('Q', 'Q'), ('TG', 'TG')):
            x = lead.get('descriptive', {}).get(kk); v.iv('LB.all.RR_' + ka, x and x.get('point'), x and x.get('ci95'), 0.95, 'nominal95')
        v['LB.n_contact'] = None if TEST else contacts_list(lead['runs']); v['LB.n_replaced'] = None if TEST else 0
    cut, p = load(CD / 'recount' / 'out' / ('RC_C_CUTIN_TESTOLD_v13.json' if TEST else 'RC_C_CUTIN_v13.json'), 'cutin'); src[str(p)] = cut is not None
    if cut:
        H, CS, D = cut['hypotheses'], cut['calibration']['stats'], cut['descriptive']
        x = H['K0']['R_gl_pp']; v.iv('CI.R', x['point'], x['ci'], x['level'], cal_second(CS.get('W_R_gl_pp')))
        x = H['K1']['RR_gl_N']; v.iv('CI.RR_N', x['point'], x['ci'], x['level'], cal_second(CS.get('W_RR_N')))
        v['CI.den0.dec'] = fnum(H['K0']['den0_deceq'])
        y = D.get('young', {}); mr = cut.get('margin_ratio', {})
        v['CI.Y.n_dec'] = int(y.get('n', 0))
        v['CI.Y.R.dec'] = 0.0 if v['CI.Y.n_dec'] == 0 else fnum((y.get('R_gl_deceq') or {}).get('point'))
        v['CI.Y.within5'] = fnum(mr.get('young', {}).get('share_within_5pct'))
        k2 = H['K2']
        if k2.get('evaluable'):
            for nm in ('r', 'c'): v.iv('CI.Y.' + nm, k2[nm]['point'], k2[nm]['ci'], k2[nm]['level'], cal_second(CS.get('Y_' + nm)))
            eff = k2.get('efficiency_r_over_c')
            v.iv('CI.Y.eff', eff and eff['point'], eff and eff['ci'], k2['r']['level'], cal_second(CS.get('Y_r')))
        else:
            for nm in ('r', 'c', 'eff'): v.iv('CI.Y.' + nm, None, None, None, None)
        for ka, kk in (('age0', 'young'), ('age1', 'age_1_4'), ('age4', 'age_ge4'), ('untr', 'untracked')):
            d = D.get(kk, {})
            v[f'CI.{ka}.R.dec'] = fnum((d.get('R_gl_deceq') or {}).get('point')); v[f'CI.{ka}.RR_N'] = fnum((d.get('RR_gl_N') or {}).get('point'))
            v[f'CI.{ka}.n_dec'] = int(d.get('n', 0)); v[f'CI.{ka}.within5'] = fnum(mr.get(kk, {}).get('share_within_5pct'))
        v['CI.n_dec'] = int(cut['counts']['window']); v['CI.n_runs'] = int(cut['events']['of'])
        v['CI.n_events'] = int(cut['events']['found'])
        v['CI.n_contact'] = None if TEST else contacts_list(cut['runs']); v['CI.n_replaced'] = None if TEST else 0


def second_d(v, src):
    d, p = load(CD / 'recount_d' / 'out' / ('RC_D_NONBRAKING_v13_TESTOLD.json' if TEST else 'RC_D_NONBRAKING_v13.json'), 'dnb'); src[str(p)] = d is not None
    if d:
        tot = 0; rids = []
        for ka, kk in DV:
            var = d['variants'].get(kk)
            if var is None: continue
            tot += var['n_runs']; rids += var.get('runs', [])
            for s in ('N', 'CK3', 'PS', 'TG'):
                so = var['sources'].get(s, {})
                v.nominal(f'D1.{ka}.{s}.dcau', so.get('d_caution')); v.nominal(f'D1.{ka}.{s}.dwg', so.get('d_wrong_go'))
        v['D1.n_runs'] = tot if tot else None
        nd = [d['variants'][kk]['sources'].get('N', {}).get('n_decisions') for _, kk in DV if kk in d['variants']]
        v['D1.n_dec'] = int(sum(nd)) if nd and None not in nd else None
        v['D1.n_contact'] = None if TEST else contacts_list(rids); v['D1.n_replaced'] = None if TEST else 0
    t, p = load(CD / 'recount_d' / 'out' / ('RC_D2_EVENT_TABLE_v13_TESTOLD.json' if TEST else 'RC_D2_EVENT_TABLE_v13.json'), 'd2'); src[str(p)] = t is not None
    if t:
        # 3 s column only: the frozen core recount's 'react_stop_tau0p75' column is the 61-frame clearance (superseded, A10 sec. 1);
        # the reaction-and-stop column comes from recount_d/rc_d2_rs_v13.py (stage 2) as a family file with A's keys.
        for sk, scn in (('w3', 'commit_3s'),):
            tab = {s_: x.get(scn) or {} for s_, x in t['table'].items()}
            if tab is None: continue
            for s in ('F0', 'N', 'CK3', 'TG'):
                for ck, cc in (('c2', '2'), ('c5', '5')):
                    e = tab.get(s, {}).get(cc) or tab.get(s, {}).get(cc + '.0')
                    if e is None: continue
                    v[f'D2.{s}.{ck}.{sk}.runs'] = int(e['n_runs_with_wrong_go']); v[f'D2.{s}.{ck}.{sk}.vclose'] = fnum(e['median_of_run_medians_mps'])


# ------------------------------------------------------------------------------------------------ A10 sec. 5.6: what may be said to transfer
TCODES = ('CK3', 'AM', 'TG', 'NA', 'N')
V12_A91 = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out\A9_1_PLACEBO_GRIDLESS_v01.json')


def transfer_structured(v):
    """A's TRANSFER.structured (A10 sec. 5.6): RR_gl(N) inside (-delta, delta) at its point in every run set where it is defined, and the
    pairs [a, b] of CK3, AM, TG, NA, N with point RR_gl(a) - RR_gl(b) > 0 in every set where both are defined (and in at least one).
    Sets: tuning (package B's export: TU.*), old (the 35 old evaluation runs: v12's A9-1 gridless values of record for N, NA, AM, CK3;
    TG gridless from this program's own old-run test, as v12 recorded TG on the grid only), fresh (this export), F (held-out real logs,
    F's export, only if F.status == 'heldout'). A set whose export does not exist yet is skipped and named in 'sets_missing'."""
    sets = {}; missing = []
    bx = (CD.parent / 'B_retrack' / 'out' / ('A_EXPORT_B.json' if WHO == 'first' else 'A_RECOUNT_B.json'))
    if bx.is_file():
        b = json.loads(bx.read_text(encoding='utf-8')); b = b['values'] if isinstance(b.get('values'), dict) else b
        sets['tuning'] = {c: fnum(b.get('TU.RR_' + c)) for c in TCODES}
    else: missing.append('tuning (%s)' % bx.name)
    if V12_A91.is_file():
        g = json.loads(V12_A91.read_text(encoding='utf-8'))['c_gridless']['all']
        old = dict(N=g['RR_N'], NA=g['RR_NA'], AM=g['RR_A1'], CK3=g['RR_CK3'], TG=None)
        if WHO == 'first':
            t, _ = load(CD / 'analysis' / 'out' / 'TESTOLD_C_LEAD_H0_H5_v13.json')
            old['TG'] = fnum(t['descriptive_RR_gl']['TG']['point']) if t else None
        else:
            cands = sorted((CD / 'recount' / 'out').glob('RC_C_LEAD_TESTOLD_*matched*.json'))
            if cands:
                t = json.loads(cands[-1].read_text(encoding='utf-8'))
                old['TG'] = fnum(((t.get('point', {}).get('descriptive', {}) or {}).get('TG', {}) or {}).get('RR_gl'))
        sets['old'] = {c: fnum(x) for c, x in old.items()}
    sets['fresh'] = dict(N=fnum(v.get('LB.RR_N')), CK3=fnum(v.get('LB.RR_CK3')), NA=fnum(v.get('LB.all.RR_NA')),
                         AM=fnum(v.get('LB.all.RR_AM')), TG=fnum(v.get('LB.all.RR_TG')))
    fx = (CD.parent / 'F_nuscenes' / 'out' / ('A_EXPORT_F.json' if WHO == 'first' else 'A_RECOUNT_F.json'))
    if fx.is_file():
        f = json.loads(fx.read_text(encoding='utf-8')); f = f['values'] if isinstance(f.get('values'), dict) else f
        if f.get('F.status') == 'heldout':
            sets['F'] = {c: fnum(f.get('F.RR_' + c)) for c in TCODES}
        else: missing.append('F (status %s, not held-out)' % f.get('F.status'))
    else: missing.append('F (%s)' % fx.name)
    ns = [s['N'] for s in sets.values() if s.get('N') is not None]
    inside = bool(ns) and all(-0.05 < x < 0.05 for x in ns)
    orders = []
    for a in TCODES:
        for b_ in TCODES:
            if a == b_: continue
            both = [(s[a], s[b_]) for s in sets.values() if s.get(a) is not None and s.get(b_) is not None]
            if both and all(x - y > 0 for x, y in both): orders.append([a, b_])
    return dict(N_inside_delta_all_sets=inside, orderings=orders, sets=sorted(sets), sets_missing=missing,
                per_set={k: s for k, s in sets.items()})


# ------------------------------------------------------------------------------------------------ Fig. 2 frontier curves (FREEZE_CD_2_add4)
# (prefix, calibration job, {exported source name: source in the job}); IMM, F0_IMM and E_IMM are the IMM tracker's own N, F0 and E
FRONT = (('LB', 'lead_main', dict(F0='F0', E='E', E5='E5', N='N', CK3='CK3')),
         ('LB', 'lead_imm', dict(IMM='N', F0_IMM='F0', E_IMM='E')),
         ('CI', 'cutin_window', dict(F0='F0', E='E', N='N')))


def frontiers_first(v, src):
    """A's Fig. 2 (coordinator 21 Nov 2026, option (a); added by FREEZE_CD_2_add4): '<LB|CI>.frontier.<SRC>' = [[caution %],
    [wrong go %]] on the 201 levels of the gridless step frontier (A10 sec. 2.3), full sample, all evaluated decisions (CI: the event
    window). Inputs: the frozen calibration jobs analysis/out/calib/<label>.job.npz, i.e. the gl_fast Prepared objects of the
    full-sample statistics (SHA-256 checked against <label>.meta.json), evaluated once with unit run weights by the frozen kernel
    analysis/gl_fast_v13.evaluate, as calib_remote_v13.py does. Refuses unless the curves reproduce the exported point values exactly
    (LB.R, LB.RR_E5, LB.RR_N, LB.RR_CK3; LB.IMM.r, LB.IMM.c on the IMM's own room; CI.R). An undefined point is null."""
    import numpy as np
    sys.dont_write_bytecode = True
    if str(CD / 'analysis') not in sys.path: sys.path.insert(0, str(CD / 'analysis'))
    import gl_fast_v13 as GF
    cdir = CD / 'analysis' / 'out' / 'calib'
    for pre, label, keys in FRONT:
        job = cdir / f'{label}.job.npz'; meta = json.loads((cdir / f'{label}.meta.json').read_text(encoding='utf-8'))
        if sha(job) != meta['job_sha256']: raise SystemExit('REFUSED: %s differs from its meta.json' % job.name)
        z = np.load(job, allow_pickle=False); src[str(job)] = True
        if str(z['kind']) != 'GL': raise SystemExit('REFUSED: %s is not a gridless job' % job.name)
        P = type('Prepared', (), {})()
        P.names = [str(x) for x in z['names']]; P.pop = int(z['pop']); P.T0 = [x for x in z['T0']]
        P.d = np.ascontiguousarray(z['d']); P.ri = z['ri'].astype(np.int64); P.keep = z['keep'].astype(np.int64)
        P.ev_off = z['ev_off'].astype(np.int64); P.keep_off = z['keep_off'].astype(np.int64); P.nrun = P.T0[0].shape[0]
        e = GF.evaluate(P, np.ones((1, P.nrun))); F = e['F'][0]; lev = e['lev'][0]; den = float(e['denE'][0])
        D = {a: float(x[0]) for a, x in e['D'].items()}
        if label == 'lead_main':
            chk = [('LB.R', den / 201.), ('LB.RR_E5', D['E5'] / den), ('LB.RR_N', D['N'] / den), ('LB.RR_CK3', D['CK3'] / den)]
        elif label == 'lead_imm':
            chk = [('LB.IMM.r', D['N'] / den), ('LB.IMM.c', D['E5x'] / den)]
        else:
            chk = [('CI.R', den / 201.)]
        bad = [(k, v.get(k), x) for k, x in chk if v.get(k) != x]
        if bad: raise SystemExit('REFUSED: the frontier curves do not reproduce the exported values: %s' % bad)
        for k, a in keys.items():
            v[f'{pre}.frontier.{k}'] = [[fnum(x) for x in lev], [fnum(x) for x in F[P.names.index(a)]]]


# ------------------------------------------------------------------------------------------------ families, assembly
AO, RO, DO = CD / 'analysis' / 'out', CD / 'recount' / 'out', CD / 'recount_d' / 'out'
# family files with a flat "values" dict under A's names: (fresh path, old-run test path); --fam NAME=PATH overrides one
FAM_FIRST = dict(S57A=(AO / 'C_S57A_v13.json', AO / 'TESTOLD_S57A_v13.json'),
                 B7=(AO / 'C_B7_v13.json', AO / 'TESTOLD_B7_v13_final.json'),
                 B7CI=(AO / 'C_B7CI_v13.json', AO / 'TESTOLD_B7_v13_ci.json'),
                 S57B=(AO / 'S57B_v13.json', AO / 'TESTOLD_S57B_v13.json'),
                 HAND=(RO / 'HAND_CHECK_v13.json', RO / 'TESTOLD_HAND_CHECK_v13.json'))
FAM_SECOND = dict(S57A=(RO / 'RC_S57A_v13.json', RO / 'TESTOLD_RC_S57A_v13_levels.json'),
                  B7=(RO / 'RC_B7_v13.json', RO / 'TESTOLD_RC_B7_v13_v3.json'),
                  B7CI=(RO / 'RC_B7_v13_cutin.json', RO / 'TESTOLD_RC_B7_v13_cutin_v1.json'),
                  S57B=(RO / 'RC_S57B_v13.json', RO / 'TESTOLD_RC_S57B_v13_final.json'),
                  D2RS=(DO / 'RC_D2_RS_v13.json', DO / 'RC_D2_RS_v13_TESTOLD.json'),
                  HAND=(RO / 'HAND_CHECK_v13.json', RO / 'TESTOLD_HAND_CHECK_v13.json'))
FAM_OVR = dict(x.split('=', 1) for x in (ARGS[ARGS.index('--fam') + 1].split(',') if '--fam' in ARGS else []))
NA_STR = 'not applicable'                     # B7CI as_room / lag (coordinator 03:35): kept as the families write them


def same(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(float(a) - float(b)) <= 1e-9
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b): return all(same(x, y) for x, y in zip(a, b))
    return a == b


def main():
    pkg_keys = {pk: {k['key']: k for k in KEYS[pk]} for pk in ('C', 'D')}
    v = V(); src = {}; overlaps = []
    if WHO == 'first':
        first_c(v, src); first_d(v, src); fmap = FAM_FIRST
        if not TEST: frontiers_first(v, src)                  # Fig. 2 curves, first program only (FREEZE_CD_2_add4)
    else:
        second_c(v, src); second_d(v, src); fmap = FAM_SECOND
    fams = [pathlib.Path(FAM_OVR[n]) if n in FAM_OVR else (pp[1] if TEST else pp[0]) for n, pp in fmap.items()]
    for fp in fams:
        doc, p = load(fp); src[str(p)] = doc is not None
        if not doc: continue
        for k, x in doc.get('values', {}).items():
            if isinstance(x, list) and len(x) == 2 and x[0] is None and x[1] is None: x = None   # an undefined interval is null (A sec. 1)
            if k in v:
                overlaps.append(dict(key=k, core=v[k], family=x, source=p.name, equal=same(v[k], x)))
            else:
                v[k] = x
    v['TRANSFER.structured'] = transfer_structured(v)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for pk in ('C', 'D'):
        mine = {k: x for k, x in v.items() if k.split('.')[0] in (('LB', 'CI', 'TU', 'B', 'B7', 'B7CI', 'TRANSFER', 'HAND') if pk == 'C' else ('D1', 'D2'))}
        want = pkg_keys[pk]
        base = lambda k: k[:-6] if k.endswith('.level') else (k[:-4] if k.endswith('.cal') else k)
        missing = sorted((k for k in want if k not in mine), key=lambda k: (not want[k]['required'], k))
        extra = sorted(k for k in mine if base(k) not in want and k not in want)
        doc = dict(package=pk, written=now, program=pathlib.Path(__file__).name + f' ({WHO})', program_sha256=sha(__file__),
                   lock2_sha256=sha(LOCK2) if LOCK2.is_file() else None, test_old=TEST, values=dict(sorted(mine.items())),
                   deviations=[], not_produced=dict(required=[k for k in missing if want[k]['required']],
                                                     supplement=[k for k in missing if not want[k]['required']]),
                   keys_not_in_A_list=extra, overlaps=[o for o in overlaps if o['key'] in mine],
                   inputs={k: (sha(k) if ok else None) for k, ok in src.items()})
        name = f'{PFX}A_{"EXPORT" if WHO == "first" else "RECOUNT"}_{pk}.json'
        out = CD / 'out' / name
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')
        bad = [o['key'] for o in doc['overlaps'] if not o['equal']]
        print(f'{name}: {len(mine)} values; A keys not produced: {len(doc["not_produced"]["required"])} required, '
              f'{len(doc["not_produced"]["supplement"])} supplement; overlaps {len(doc["overlaps"])} (unequal {bad})')


if __name__ == '__main__':
    main()
