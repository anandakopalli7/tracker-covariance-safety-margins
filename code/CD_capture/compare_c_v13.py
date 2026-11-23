"""Compare package C's first programs (analysis/c_lead_v13.py, c_cutin_v13.py) with the second programs (recount/rc_c_lead_v13.py,
rc_c_cutin_v13.py) per A10 sec. 10.1(c): counts exact; points and interval ends on the same draws within 1e-9; calibrated levels
equal; hypothesis outcomes and classifications equal. New file, 20 Nov 2026 (Claude Opus 5.5), written before Lock 2.

Usage: python -I compare_c_v13.py [--lead-a F --lead-b F] [--cutin-a F --cutin-b F] [--out F] [--test-old]
Defaults: analysis/out/C_LEAD_H0_H5_v13.json vs recount/out/RC_C_LEAD_v13.json; analysis/out/C_CUTIN_K0_K2_v13.json vs
recount/out/RC_C_CUTIN_v13.json; output out/COMPARE_C_v13.json (never overwritten).
--test-old: interval ends and calibrated levels are compared only with --matched (both programs run at the same sizes); points,
counts and outcomes are compared as usual; H3 and the H3-dependent outcomes are skipped (no IMM arrays for old runs).

An item marked required that is missing in either output is a disagreement; an optional one is listed as not compared.
"""
import json, math, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
TOL = 1e-9
CMP_IV = ('--test-old' not in sys.argv[1:]) or ('--matched' in sys.argv[1:])   # intervals and levels: always on fresh runs; on old runs only with --matched (same sizes)
MISSING = object()
A = sys.argv[1:]


def opt(k, d):
    return A[A.index(k) + 1] if k in A else d


def get(d, *path):
    for p in path:
        if isinstance(d, dict) and p in d: d = d[p]
        elif isinstance(d, list) and isinstance(p, int) and -len(d) <= p < len(d): d = d[p]
        else: return MISSING
    return d


def same(a, b, kind):
    if kind == 'exact':
        if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b): return True
        return a == b
    if kind == 'num':
        if a is None or b is None: return a is b
        a, b = float(a), float(b)
        if math.isnan(a) or math.isnan(b): return math.isnan(a) and math.isnan(b)
        if math.isinf(a) or math.isinf(b): return a == b
        return abs(a - b) <= TOL
    if kind == 'pair':
        return (a is MISSING) == (b is MISSING) and len(a) == len(b) and all(same(x, y, 'num') for x, y in zip(a, b))
    raise ValueError(kind)


class Cmp:
    def __init__(self): self.rows = []

    def add(self, name, a, b, kind, required=True):
        if a is MISSING or b is MISSING:
            st = 'MISSING' if required else 'not compared'
            self.rows.append(dict(item=name, status=st, first=None if a is MISSING else a, second=None if b is MISSING else b)); return
        ok = same(a, b, kind)
        self.rows.append(dict(item=name, status='agree' if ok else 'DISAGREE', kind=kind, first=a, second=b))


def lead(c, a, b, test_old):
    c.add('lead: run list', get(a, 'runs'), get(b, 'runs'), 'exact')
    c.add('lead: n_runs', get(a, 'n_runs'), get(b, 'counts', 'n_runs'), 'exact')
    c.add('lead: E5 n_evaluated', get(a, 'e5_u', 'n_evaluated'), get(b, 'E5', 'n_evaluated'), 'exact')
    c.add('lead: E5 n_with_ratio', get(a, 'e5_u', 'n_with_ratio'), get(b, 'E5', 'n_with_ratio'), 'exact')
    for ka, kb in (('R_gl', 'R_gl_pp'), ('RR_E5', 'RR_E5'), ('RR_E5_minus_E5p', 'RR_E5_minus_E5p'), ('RR_N', 'RR_N'), ('RR_CK3', 'RR_CK3')):
        c.add(f'lead: {ka} point', get(a, 'main', ka, 'point'), get(b, 'point', 'stats', kb), 'num')
        if CMP_IV:
            c.add(f'lead: {ka} calibrated level', get(a, 'calibration_main', ka, 'level'), get(b, 'calibration', 'stats', kb, 'level_used'), 'exact')
            c.add(f'lead: {ka} interval at that level', get(a, 'main', ka, 'ci_level'), get(b, 'intervals', kb, 'ci'), 'pair')
            c.add(f'lead: {ka} 95% interval', get(a, 'main', ka, 'ci'), get(b, 'intervals', kb, 'ci95'), 'pair')
    # H3 (IMM; not run on old runs)
    if not test_old:
        c.add('lead: H3 classification', get(a, 'H3', 'classification'), get(b, 'hypotheses', 'H3', 'classification'), 'exact')
        for s in ('r', 'c'):
            c.add(f'lead: H3 {s} point', get(a, 'H3', s, 'point'), get(b, 'hypotheses', 'H3', s, 'point'), 'num')
            c.add(f'lead: H3 {s} calibrated level', get(a, 'H3', 'calibration', s, 'level'), get(b, 'calibration', 'stats', 'IMM_' + s, 'level_used'), 'exact')
            c.add(f'lead: H3 {s} interval at that level', get(a, 'H3', s, 'ci_level'), get(b, 'hypotheses', 'H3', s, 'ci'), 'pair')
        c.add('lead: H3 barely_varies', get(a, 'H3', 'barely_varies'), get(b, 'hypotheses', 'H3', 'barely_varies'), 'exact')
        c.add('lead: IMM room R_pp', get(a, 'H3', 'room_IMM', 'R_pp'), get(b, 'point', 'stats', 'IMM_R_gl_pp'), 'num', required=False)
    # H4: primary (estimated phase, threshold -1.0) and three sensitivities, record basis and like for like
    for va, vb in ((None, 'est_-1.0'), ('truth_phase', 'truth'), ('thr_-0.5', 'est_-0.5'), ('thr_-2.0', 'est_-2.0')):
        for basis, bk in (('record_basis', 'rec'), ('like_for_like', 'lfl')):
            pa = ('H4', basis) if va is None else ('H4', 'sensitivities', va, basis)
            kb = f'H4_{bk}_{vb}'
            c.add(f'lead: {kb} point', get(a, *pa, 'point'), get(b, 'point', 'stats', kb), 'num')
            if CMP_IV:
                c.add(f'lead: {kb} 95% interval', get(a, *pa, 'ci'), get(b, 'intervals', kb, 'ci95'), 'pair')
    if CMP_IV:
        c.add('lead: H4 primary (record basis) calibrated level', get(a, 'H4', 'calibration', 'share_record', 'level'),
              get(b, 'calibration', 'stats', 'H4_rec_est_-1.0', 'level_used'), 'exact')
        c.add('lead: H4 primary interval at that level', get(a, 'H4', 'record_basis', 'ci_level'), get(b, 'intervals', 'H4_rec_est_-1.0', 'ci'), 'pair')
    # descriptive RR_gl
    for k in ('NA', 'A1', 'Q', 'TG'):
        c.add(f'lead: descriptive RR_gl({k}) point', get(a, 'descriptive_RR_gl', k, 'point'), get(b, 'descriptive', k, 'point'), 'num')
        if CMP_IV:
            c.add(f'lead: descriptive RR_gl({k}) 95% interval', get(a, 'descriptive_RR_gl', k, 'ci'), get(b, 'descriptive', k, 'ci95'), 'pair')
    # outcomes
    for h in ('H0', 'H1', 'H2', 'H3', 'H4', 'H5'):
        if test_old and h in ('H3', 'H4', 'H5'):   # old runs: H3 is skipped, so the two programs' sequences differ by design
            continue
        c.add(f'lead: {h} passes', get(a, 'sequence', h, 'passes'), get(b, 'hypotheses', h, 'passes'), 'exact')
        c.add(f'lead: {h} confirmed', get(a, 'sequence', h, 'confirmed'), get(b, 'hypotheses', h, 'confirmed'), 'exact')


POPS = (('all_evaluated', 'all'), ('window', 'window'), ('young', 'young'), ('mid', 'age_1_4'), ('old', 'age_ge4'), ('untracked', 'untracked'),
        ('sec[-1,0)', 'sec_-1_0'), ('sec[0,1)', 'sec_0_1'), ('sec[1,2)', 'sec_1_2'), ('sec[2,3)', 'sec_2_3'), ('sec[3,4)', 'sec_3_4'))


def cutin(c, a, b, test_old):
    ra = {r['run']: r for r in get(a, 'runs')} if get(a, 'runs') is not MISSING else {}
    rb = {r['run']: r for r in get(b, 'per_run')} if get(b, 'per_run') is not MISSING else {}
    c.add('cut-in: run list', sorted(ra), sorted(rb), 'exact')
    for run in sorted(set(ra) & set(rb)):
        c.add(f'cut-in: {run} event tick', ra[run].get('event_tick'), rb[run].get('event_tick'), 'exact')
        c.add(f'cut-in: {run} evaluated', ra[run].get('n_eval'), rb[run].get('n_evaluated'), 'exact')
        c.add(f'cut-in: {run} window', ra[run].get('n_window'), get(rb[run], 'counts', 'window'), 'exact')
        for sa, sb in (('<1s', 'young'), ('1-4s', 'age_1_4'), ('>=4s', 'age_ge4'), ('untracked', 'untracked')):
            c.add(f'cut-in: {run} window {sa}', get(ra[run], 'window_strata', sa), get(rb[run], 'counts', sb), 'exact')
    for pa, pb in POPS:
        n = get(a, 'descriptive', pa, 'n')
        c.add(f'cut-in: {pa} decisions', None if n is MISSING else int(n), get(b, 'counts', pb), 'exact')
        c.add(f'cut-in: {pa} R_gl point', get(a, 'descriptive', pa, 'R_pp', 'point'), get(b, 'descriptive', pb, 'R_gl_pp', 'point'), 'num')
        c.add(f'cut-in: {pa} R_deceq point', get(a, 'descriptive', pa, 'R_deceq', 'point'), get(b, 'descriptive', pb, 'R_gl_deceq', 'point'), 'num')
        c.add(f'cut-in: {pa} den0_deceq point', get(a, 'descriptive', pa, 'den0_deceq', 'point'), get(b, 'descriptive', pb, 'den0_deceq', 'point'), 'num')
        c.add(f'cut-in: {pa} RR_gl(N) point', get(a, 'descriptive', pa, 'RR_N', 'point'), get(b, 'descriptive', pb, 'RR_gl_N', 'point'), 'num')
        for q in ('n', 'median', 'q05', 'q95', 'A'):
            qa, qb = get(a, 'descriptive', pa, 'ratio', q), get(b, 'margin_ratio', pb, q)
            if q != 'n' and qa is MISSING and get(a, 'descriptive', pa, 'ratio', 'n') == 0 and get(b, 'margin_ratio', pb, 'n') == 0:
                qa = float('nan')                         # empty population: the first program omits the quantiles, the recount writes NaN
            c.add(f'cut-in: {pa} ratio {q}', qa, qb, 'num', required=False)
        if CMP_IV:
            c.add(f'cut-in: {pa} R_gl 95% interval', get(a, 'descriptive', pa, 'R_pp', 'ci'), get(b, 'descriptive', pb, 'R_gl_pp', 'ci95'), 'pair')
            c.add(f'cut-in: {pa} RR_gl(N) 95% interval', get(a, 'descriptive', pa, 'RR_N', 'ci'), get(b, 'descriptive', pb, 'RR_gl_N', 'ci95'), 'pair')
    c.add('cut-in: K0 R_gl point', get(a, 'K0', 'R_gl', 'point'), get(b, 'hypotheses', 'K0', 'R_gl_pp', 'point'), 'num')
    c.add('cut-in: K0 den0_deceq', get(a, 'K0', 'den0_deceq'), get(b, 'hypotheses', 'K0', 'den0_deceq'), 'num')
    c.add('cut-in: K1 RR_gl(N) point', get(a, 'K1', 'RR_N', 'point'), get(b, 'hypotheses', 'K1', 'RR_gl_N', 'point'), 'num')
    if CMP_IV:
        c.add('cut-in: K0 R_gl calibrated level', get(a, 'K0', 'calibration', 'R_gl', 'level'), get(b, 'calibration', 'stats', 'W_R_gl_pp', 'level_used'), 'exact')
        c.add('cut-in: K0 R_gl interval at that level', get(a, 'K0', 'R_gl', 'ci_level'), get(b, 'hypotheses', 'K0', 'R_gl_pp', 'ci'), 'pair')
        c.add('cut-in: K1 RR_gl(N) calibrated level', get(a, 'K0', 'calibration', 'RR_N', 'level'), get(b, 'calibration', 'stats', 'W_RR_N', 'level_used'), 'exact')
        c.add('cut-in: K1 RR_gl(N) interval at that level', get(a, 'K1', 'RR_N', 'ci_level'), get(b, 'hypotheses', 'K1', 'RR_gl_N', 'ci'), 'pair')
    c.add('cut-in: K2 evaluable', get(a, 'K2', 'status') == 'evaluated', get(b, 'hypotheses', 'K2', 'evaluable'), 'exact')
    if get(a, 'K2', 'status') == 'evaluated' or get(b, 'hypotheses', 'K2', 'evaluable') is True:
        c.add('cut-in: K2 classification', get(a, 'K2', 'classification'), get(b, 'hypotheses', 'K2', 'classification'), 'exact')
        for s in ('r', 'c'):
            c.add(f'cut-in: K2 {s} point', get(a, 'K2', s, 'point'), get(b, 'hypotheses', 'K2', s, 'point'), 'num')
            if CMP_IV:
                c.add(f'cut-in: K2 {s} calibrated level', get(a, 'K2', 'calibration', s, 'level'), get(b, 'calibration', 'stats', 'Y_' + s, 'level_used'), 'exact')
                c.add(f'cut-in: K2 {s} interval at that level', get(a, 'K2', s, 'ci_level'), get(b, 'hypotheses', 'K2', s, 'ci'), 'pair')
    for h in ('K0', 'K1', 'K2'):
        pa_, pb_ = get(a, 'sequence', h, 'passes'), get(b, 'hypotheses', h, 'passes')
        ca_, cb_ = get(a, 'sequence', h, 'confirmed'), get(b, 'hypotheses', h, 'confirmed')
        if h == 'K2' and get(b, 'hypotheses', 'K2', 'evaluable') is False and get(a, 'K2', 'status') == 'not evaluable':
            # "not evaluable": the recount writes None, the first program False (neither passes nor is confirmed)
            pb_ = False if pb_ is None else pb_; cb_ = False if cb_ is None else cb_
        c.add(f'cut-in: {h} passes', pa_, pb_, 'exact')
        c.add(f'cut-in: {h} confirmed', ca_, cb_, 'exact')


def main():
    test_old = '--test-old' in A
    la = pathlib.Path(opt('--lead-a', HERE / 'analysis' / 'out' / 'C_LEAD_H0_H5_v13.json'))
    lb = pathlib.Path(opt('--lead-b', HERE / 'recount' / 'out' / 'RC_C_LEAD_v13.json'))
    ca = pathlib.Path(opt('--cutin-a', HERE / 'analysis' / 'out' / 'C_CUTIN_K0_K2_v13.json'))
    cb = pathlib.Path(opt('--cutin-b', HERE / 'recount' / 'out' / 'RC_C_CUTIN_v13.json'))
    out = pathlib.Path(opt('--out', HERE / 'out' / ('COMPARE_C_v13_TESTOLD.json' if test_old else 'COMPARE_C_v13.json')))
    if out.exists(): raise SystemExit(f'REFUSED: {out} exists')
    ld = lambda p: json.loads(p.read_text(encoding='utf-8').replace('NaN', 'NaN'))
    c = Cmp()
    lead(c, ld(la), ld(lb), test_old)
    cutin(c, ld(ca), ld(cb), test_old)
    st = {}
    for r in c.rows: st[r['status']] = st.get(r['status'], 0) + 1
    import hashlib
    doc = dict(schema='COMPARE_C_V13', amendment='AMENDMENT_10_v13 sec. 10.1(c)', test_old=test_old, tolerance=TOL,
               inputs={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (la, lb, ca, cb)}, summary=st,
               verdict='AGREE' if not st.get('DISAGREE') and not st.get('MISSING') else 'DISAGREE OR MISSING', rows=c.rows)
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')
    print(json.dumps(dict(out=str(out), summary=st, verdict=doc['verdict'])))
    for r in c.rows:
        if r['status'] in ('DISAGREE', 'MISSING'): print(' ', r['status'], r['item'], '| first:', str(r['first'])[:80], '| second:', str(r['second'])[:80])


if __name__ == '__main__':
    main()
