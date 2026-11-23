"""Revision v12, AMENDMENT_09 A9-7 step 2 (review item S2): the time-gap margin scored like every source. New file, 19 Nov 2026.
3 s commitment: RR of TG2 (r0 = 2 m/s), TG1, TG4 for all decisions, ego moving and the three phases (draw of record, intervals for
TG2 in all populations and for TG1, TG4 pooled). Reaction-and-stop (tau = 0.75 s, 6 m/s^2, judged until the stop ends): RR0 pooled
and with the ego moving. The braking prediction and the acceleration margin are scored alongside as anchors (values of record).
Usage: python -B -X utf8 a9_7b_timegap_score_v01.py
"""
import time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_7B_TIMEGAP_SCORE_v01.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
runs = C.load_runs()
TG = A.HERE / 'out' / 'tg'; EXT = A.V11 / 'out' / 'ext'; KEY = L.vkey(0.75, 6.0)
for r in runs:
    z = np.load(TG / (r['run'] + '.npz'), allow_pickle=False)
    x = np.load(EXT / (r['run'] + '.npz'), allow_pickle=False)
    if not (np.array_equal(z['k'], r['k']) and np.array_equal(x['k'], r['k'])):
        raise SystemExit('REFUSED: decision ticks differ for %s' % r['run'])
    for nm in ('cTG1', 'cTG2', 'cTG4'):
        r['crit'][nm[1:]] = z[nm]
    r['safe_x'] = {'est': L.clean_clear(x['clearX_' + KEY]) > 0.}
CNT = C.cnt_of_record()
SRC = ['TG2', 'TG1', 'TG4', 'CK3', 'A1']
PN = ['all', 'moving', 'phase0', 'phase1', 'phase2']
doc = dict(code='a9_7b_timegap_score_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-7')
X = C.tables(runs, ('W1',), ['F0', 'E'] + SRC)
pts = C.points(X, ['E'] + SRC, pops=range(5))
Rb = C.boot(X, ['E'] + SRC, (), list(range(5)), CNT)
w1 = {}
for pi, pn in enumerate(PN):
    p = pts[pi]; b = Rb[pi]
    ent = dict(n=p['n'], R_pp=p['denE'] / L.NLEV)
    for a in SRC:
        ent['RR_' + a] = L.summ(C.rat(b['D'][a], b['denE']), L.ratio(p['D'][a], p['denE']))
        ent['D_%s_deceq' % a] = L.dec_eq(p['D'][a], p['n'])
    w1[pn] = ent
doc['w1'] = w1
print('W1 done (%.0f s): %s' % (time.time() - t00, {pn: round(w1[pn]['RR_TG2']['point'], 3) for pn in PN}), flush=True)
XR = C.tables(runs, ('X', 'est'), ['F0', 'E', 'O'] + SRC)
ptr = C.points(XR, ['E', 'O'] + SRC, pops=[0, 1])
Rr = C.boot(XR, ['E', 'O'] + SRC, (), [0, 1], CNT)
wr = {}
for pi, pn in ((0, 'all'), (1, 'moving')):
    p = ptr[pi]; b = Rr[pi]
    ent = dict(n=p['n'], den0_deceq=L.dec_eq(p['D']['O'], p['n']))
    for a in SRC:
        ent['RR0_' + a] = L.summ(C.rat(b['D'][a], b['D']['O']), L.ratio(p['D'][a], p['D']['O']))
    wr[pn] = ent
doc['stop_t0p75_a6'] = wr
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
A.write_out(OUTF, doc)
print('written %s (%.0f s)' % (OUTF, time.time() - t00))
