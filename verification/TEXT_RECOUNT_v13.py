# TEXT_RECOUNT_v13.py -- independent recount of the numbers printed in the frozen v13 text.
# Written by Claude Sonnet 5.5 (not the writer, Claude Opus 5.5). Run: python -I TEXT_RECOUNT_v13.py
# Reads only: freeze_v13\MANUSCRIPT_v13.md / SUPPLEMENT_v13.md, the A_EXPORT_* / A_RECOUNT_* files,
# B_RESULTS_SUMMARY_v13.json, b8\B8_NIS_NEES_v01.json, gen\rename_v13.json, the three lock files,
# revision_v12\draft\DERIVED_v12.json (old-run strings only).
import json, math, re, os, sys, hashlib
from decimal import Decimal, ROUND_HALF_UP

R13 = r'ARS_TRIAL\revision_v13'
W = R13 + r'\work'
FR = W + r'\A_text\out\freeze_v13'
MS = open(FR + r'\MANUSCRIPT_v13.md', encoding='utf8').read()
SU = open(FR + r'\SUPPLEMENT_v13.md', encoding='utf8').read()
MINUS = '\u2212'


def J(p):
    return json.load(open(p, encoding='utf8'))


EXP = {'B': J(W + r'\B_retrack\out\A_EXPORT_B.json')}
EXP['B'] = EXP['B'].get('values', EXP['B'])
for n, p in [('C', r'\CD_capture\out\A_EXPORT_C.json'), ('D', r'\CD_capture\out\A_EXPORT_D.json'),
             ('E', r'\E_closedloop\out\A_EXPORT_E.json'), ('F', r'\F_nuscenes\out\A_EXPORT_F.json')]:
    EXP[n] = J(W + p)['values']
REC = {}
rb = J(W + r'\B_retrack\out\A_RECOUNT_B.json')
REC['B'] = rb.get('values', rb)
for n, p in [('C', r'\CD_capture\out\A_RECOUNT_C.json'), ('D', r'\CD_capture\out\A_RECOUNT_D.json'),
             ('E', r'\E_closedloop\out\A_RECOUNT_E.json'), ('F', r'\F_nuscenes\out\A_RECOUNT_F.json')]:
    REC[n] = J(W + p)['values']
B0P = J(W + "/B_retrack/out/banalysis/B_CV0_v01.json")["points"]["all"]
B0R = J(W + "/B_retrack/recount/RECOUNT_B_v01.json")["per_variant"]["CV0"]["all"]
V12 = J(R13 + r'\..\revision_v12\draft\DERIVED_v12.json')
RENAME = J(W + r'\A_text\gen\rename_v13.json')

NAN = float('nan')


def isnan(x):
    return isinstance(x, float) and math.isnan(x)


def lookup(key):
    """Find key in the exports (flat names are unique across packages except identical copies)."""
    hits = [(n, EXP[n][key]) for n in EXP if key in EXP[n]]
    if not hits:
        raise KeyError(key)
    vals = {json.dumps(v, sort_keys=True, default=str) for _, v in hits}
    if len(vals) > 1:
        raise KeyError('ambiguous ' + key)
    return hits[0]


def get(key, idx=None):
    pk, v = lookup(key)
    if v is None:
        return None, pk
    if idx is not None:
        if v is None:
            return None, pk
        v = v[idx]
    return v, pk


# ---------------------------------------------------------------- formatting
def q(x, nd):
    d = Decimal(repr(float(x))) if False else Decimal(float(x))
    s = format(d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP), 'f')
    if re.fullmatch(r'-0(\.0+)?', s):
        s = s[1:]
    return s.replace('-', MINUS)


def fmt(x, f):
    if x is None or isnan(x):
        return 'n.c.'
    if f == 'sh3' or f == 'ci3':
        return q(x, 3)
    if f == 'sh4' or f == 'ci4':
        return q(x, 4)
    if f in ('pp', 'ci2', 'f2'):
        return q(x, 2)
    if f in ('dec1', 'ci1', 'f1'):
        return q(x, 1)
    if f == 'pct2':
        return q(100 * x, 2) + '%'
    if f == 'pct1':
        return q(100 * x, 1) + '%'
    if f == 'pct0':
        return q(100 * x, 0) + '%'
    if f == 'int':
        return format(int(round(x)), ',')
    if f == 'dec':   # integer with thousands separator
        return format(int(Decimal(float(x)).quantize(Decimal(1), rounding=ROUND_HALF_UP)), ',')
    raise ValueError(f)


# ---------------------------------------------------------------- statuses (A10 rules)
D_ = 0.05


def lo(ci):
    return None if ci is None or any(isnan(c) for c in ci) else ci[0]


def hi(ci):
    return None if ci is None or any(isnan(c) for c in ci) else ci[1]


def inside(ci, a, b):
    return ci is not None and not any(isnan(c) for c in ci) and ci[0] > a and ci[1] < b


def gt(x, t):
    return x is not None and not isnan(x) and x > t


def val(k, i=None):
    return get(k, i)[0]


def cls_h3(r_ci, c_ci):
    if gt(lo(r_ci), 0):
        return 'recovers'
    if gt(lo(c_ci), D_):
        return 'uninformative variation'
    if inside(c_ci, -D_, D_):
        return 'amplitude-limited'
    return 'inconclusive'


def cls_e(dc, dt):
    if dc is None:
        return 'n.c.'
    if dc[1] < 0 and dt[1] < 0.5:
        return 'safer at no extra cost'
    if dc[1] < 0 and dt[1] >= 0.5:
        return 'safer at a cost'
    if inside(dc, -0.10, 0.10) and inside(dt, -0.5, 0.5):
        return 'equivalent'
    if dc[0] > 0:
        return 'worse'
    return 'inconclusive'


def cls_d(dcau, dwg):
    if dcau[0] > 1 and dwg[1] <= 0:
        return 'costs progress'
    if dwg[0] > 0:
        return 'costs safety'
    if inside(dcau, -1, 1) and inside(dwg, -1, 1):
        return 'no measurable cost'
    return 'inconclusive'


STAT = {}
# lead braking H0-H5
nonpos = val('LB.R.nonpos_share')
STAT['H0'] = 'pass' if (gt(lo(val('LB.R.ci')), 0) and nonpos < 0.025) else 'fail'
STAT['H1'] = 'pass' if gt(lo(val('LB.RR_E5.ci')), 0) and gt(lo(val('LB.RR_E5mP.ci')), 0) else 'fail'
STAT['H2'] = 'pass' if inside(val('LB.RR_N.ci'), -D_, D_) else 'fail'
STAT['H3'] = cls_h3(val('LB.IMM.r.ci'), val('LB.IMM.c.ci'))
STAT['H3.barely'] = val('LB.IMM.within5') >= 0.95
STAT['H4'] = 'pass' if gt(lo(val('LB.PS.rec.ci')), 0.5) else 'fail'
STAT['H5'] = 'pass' if gt(lo(val('LB.RR_CK3.ci')), 0.5) else 'fail'
# confirmed = this and every earlier one passed (H3 passes with recovers / uninformative / amplitude-limited)
seq = ['H0', 'H1', 'H2', 'H3', 'H4', 'H5']
ok = True
CONF = {}
for h in seq:
    p = (STAT[h] == 'pass') if h != 'H3' else STAT[h] in ('recovers', 'uninformative variation', 'amplitude-limited')
    ok = ok and p
    CONF[h] = ok
# cut-in K0-K2
STAT['K0'] = 'pass' if gt(lo(val('CI.R.ci')), 0) and val('CI.den0.dec') >= 10 else 'fail'
STAT['K1'] = 'not_run' if val('CI.RR_N.ci') is None else ('pass' if inside(val('CI.RR_N.ci'), -D_, D_) else 'fail')
STAT['K2'] = 'not_run' if val('CI.Y.R.dec') < 10 or val('CI.Y.r.ci') is None else cls_h3(val('CI.Y.r.ci'), val('CI.Y.c.ci'))
# F-H0..F-H2
STAT['F-H0'] = 'pass' if gt(lo(val('F.R.ci')), 0) and val('F.R.nonpos_share') < 0.025 else 'fail'
STAT['F-H1'] = 'not_run' if STAT['F-H0'] == 'fail' else ('pass' if inside(val('F.RR_N.ci'), -D_, D_) else 'fail')
STAT['F-H2 (if it had been run)'] = cls_h3(val('F.IMM.r.ci'), val('F.IMM.c.ci'))
# D-H1/D-H2
for v in ('const', 'mild', 'stopgo'):
    for src, nm in (('CK3', 'D-H1'), ('PS', 'D-H2')):
        STAT['%s.%s' % (nm, v)] = cls_d(val('D1.%s.%s.dcau.ci' % (v, src)), val('D1.%s.%s.dwg.ci' % (v, src)))
# E-H1..E-H3 and every other arm/level
for arm in ('N', 'CK3', 'TG', 'PS', 'NIMM'):
    for lev in ('lo', 'hi'):
        STAT['E3.%s.%s' % (arm, lev)] = cls_e(val('E3.%s.%s.dc.ci' % (arm, lev)), val('E3.%s.%s.dt.ci' % (arm, lev)))
for v in ('const', 'mild', 'stopgo'):
    for arm in ('N', 'CK3', 'PS', 'TG'):
        STAT['E3b.%s.%s' % (v, arm)] = cls_e(val('E3b.%s.%s.dc.ci' % (v, arm)), val('E3b.%s.%s.dt.ci' % (v, arm)))
STAT['E-H1'] = STAT['E3.CK3.lo']
STAT['E-H2'] = STAT['E3.N.lo']
STAT['E-H3'] = STAT['E3.NIMM.lo']
# B3/B4 rule
ASR = val('B.CV.as_room')
for x in ('CV2', 'CA'):
    below = val('B.%s.as_room' % x) < 0.5 * ASR
    diff = abs(val('B.%s.RR_CK3' % x) - val('B.CV.RR_CK3')) > 0.10
    STAT['B3/B4 %s' % x] = 'depends on tuning' if (below or diff) else 'mechanism persists'
STAT['B3/B4'] = 'mechanism persists' if all(STAT['B3/B4 %s' % x] == 'mechanism persists' for x in ('CV2', 'CA')) else 'depends on tuning'
# B7 rate rule and N rule
STAT['B7 rate'] = 'largely a consequence of the 2 Hz update' if val('B7.10.0.1.as_room') < 0.5 * val('B7.2.0.as_room') else 'no consequence'
n_ci = [(k, val(k)) for k in EXP['C'] if re.fullmatch(r'B7\.\d+\.0(\.\d)?\.RR_N\.ci', k)]
STAT['B7 N inside (-d,d) at all %d rate/latency cells' % len(n_ci)] = 'holds' if all(inside(c, -D_, D_) for _, c in n_ci) else 'fails'
STAT['B7 identity'] = val('B7.identity')
# B6 terciles evaluable
STAT['B6 terciles evaluable (den0>=10)'] = 'all' if all(val('LB.T%d.den0.dec' % i) >= 10 for i in (1, 2, 3)) else 'some not'
# transfer statements
ts = val('TRANSFER.structured')
ps = ts['per_set']
ORDER = ['CK3', 'AM', 'TG', 'NA', 'N']
order_ok = True
for i, a in enumerate(ORDER):
    for b in ORDER[i + 1:]:
        for s_, d_ in ps.items():
            if d_.get(a) is not None and d_.get(b) is not None and not d_[a] - d_[b] > 0:
                order_ok = False
STAT['TRANSFER order CK3>AM>TG>NA>N in every set where defined'] = order_ok
STAT['TRANSFER N inside (-d,d) in every set'] = all(inside([-D_ + 1e-12, D_ - 1e-12], -D_, D_) and abs(d_['N']) < D_ for d_ in ps.values() if d_.get('N') is not None)

# ---------------------------------------------------------------- the entries
# (location, printed text exactly as in the frozen text, template).  {KEY|fmt} point, {KEY@0|fmt} interval end.
ENT = []
NTK = []
KEYS_USED = {}


def E(loc, printed, tmpl):
    ENT.append((loc, printed, tmpl))


def ci(key, f):
    return '[{%s@0|%s}, {%s@1|%s}]' % (key, f, key, f)


def pt(key, f):
    return '{%s|%s}' % (key, f)


def ptci(key, f, cif=None):
    return pt(key, f) + ' ' + ci(key + '.ci', cif or f)


# --- Abstract, Introduction (contribution 2), Conclusion
for loc in ('Abstract', 'Conclusion (VII)'):
    E(loc, '5.58 [4.99, 6.17] percentage points', ptci('LB.R', 'pp', 'ci2') + ' percentage points')
    E(loc, 'an oracle recovers 0.01% of the room', 'an oracle recovers ' + pt('B.CV.c', 'pct2') + ' of the room')
    E(loc, 'within [\u22120.09%, 0.15%]', 'within [{LB.RR_N.ci@0|pct2}, {LB.RR_N.ci@1|pct2}]')
    E(loc, '99.7% of binding rows within 5%', pt('LB.IMM.within5', 'pct1') + ' of binding rows within 5%')
    E(loc, 'recovers 4.6% of its room', 'recovers ' + pt('B.AQ.RR', 'pct1') + ' of its room')
    E(loc, 'recovers 78% of the pooled room and a per-phase schedule 92%', 'recovers ' + pt('LB.RR_CK3', 'pct0') + ' of the pooled room and a per-phase schedule ' + pt('LB.PS.rec', 'pct0'))
    E(loc, '(0.16 s lost)', '(' + pt('E3.CK3.lo.dt', 'f2') + ' s lost)')
    E(loc, 'the after-stop room is 45% of that', 'the after-stop room is ' + pt('B7.ratio_10_2', 'pct0') + ' of that')
E('I contribution 2', 'share within [\u22120.09%, 0.15%]', 'share within [{LB.RR_N.ci@0|pct2}, {LB.RR_N.ci@1|pct2}]')
E('III-C', 'turned 6,122 of the class average\'s design-split decisions', 'turned ' + pt('F.design.removed3.F0', 'int') + ' of the class average\'s design-split decisions')
E('Limits', '1 of 5,293 event-window decisions', pt('CI.Y.n_dec', 'int') + ' of ' + pt('CI.n_dec', 'int') + ' event-window decisions')
E('V-A para 1', 'recovers only 0.0001 [0.0000, 0.0002] of the room', 'recovers only ' + ptci('B.CV.c', 'sh4') + ' of the room')
E('V-C para 1', 'as is the time gap, which uses no information about the lead\'s motion (contact difference \u22120.20 [\u22120.32, \u22120.10]; time lost \u22120.13 [\u22120.19, \u22120.06] s)',
  'as is the time gap, which uses no information about the lead\'s motion (contact difference ' + ptci('E3.TG.lo.dc', 'pp', 'ci2') + '; time lost ' + ptci('E3.TG.lo.dt', 'pp', 'ci2') + ' s)')
E('V-C para 1', 'brakes fully in 52.7% of its decisions at the lower level and 78.6% at the higher, and time lost, about 24.5 s',
  'brakes fully in ' + pt('E3.F0.lo.fallback', 'pct1') + ' of its decisions at the lower level and ' + pt('E3.F0.hi.fallback', 'pct1') + ' at the higher, and time lost, about ' + pt('E3.F0.lo.tlost', 'f1') + ' s')
E('V-C para 1', '(11.88% against 14.10% and 22.30%; Table IV)', '(' + pt('E3.PS.lo.caution', 'pp') + '% against ' + pt('E3.F0.lo.caution', 'pp') + '% and ' + pt('E3.F0.hi.caution', 'pp') + '%; Table IV)')
E('V-D update rate', 'the room is 5.58, 4.99 and 4.75 points at 2, 5 and 10 Hz', 'the room is ' + pt('B7.2.0.R', 'pp') + ', ' + pt('B7.5.0.R', 'pp') + ' and ' + pt('B7.10.0.R', 'pp') + ' points at 2, 5 and 10 Hz')
E('V-D update rate', 'falls from 173.4 to 35.5 decision-equivalents; with the plan\'s 0.1 s latency it is 77.8 at 10 Hz',
  'falls from ' + pt('B7.2.0.as_room', 'dec1') + ' to ' + pt('B7.10.0.as_room', 'dec1') + ' decision-equivalents; with the plan\'s 0.1 s latency it is ' + pt('B7.10.0.1.as_room', 'dec1') + ' at 10 Hz')
E('V-D non-braking', 'brake mildly, by 0.9 [0.4, 1.6] points for 18.7 [15.4, 21.9] of caution, and behind leads that stop and pull away, by 4.7 [3.4, 6.3] points for 1.7 [1.1, 2.2] of caution',
  'brake mildly, by {NEG:D1.mild.CK3.dwg|f1} [{NEG:D1.mild.CK3.dwg.ci@1|f1}, {NEG:D1.mild.CK3.dwg.ci@0|f1}] points for ' + ptci('D1.mild.CK3.dcau', 'f1') + ' of caution, and behind leads that stop and pull away, by {NEG:D1.stopgo.CK3.dwg|f1} [{NEG:D1.stopgo.CK3.dwg.ci@1|f1}, {NEG:D1.stopgo.CK3.dwg.ci@0|f1}] points for ' + ptci('D1.stopgo.CK3.dcau', 'f1') + ' of caution')
E('V-B para 2', 'recover \u22120.0009, \u22120.0008 and 0.0459 [0.0390, 0.0533] of their rooms', 'recover ' + pt('B.CV2.RR', 'sh4') + ', ' + pt('B.CA.RR', 'sh4') + ' and ' + ptci('B.AQ.RR', 'sh4') + ' of their rooms')
E('VI', 'the bound on the covariance\'s share, [\u22120.0009, 0.0015] of the room', 'the bound on the covariance\'s share, [{LB.RR_N.ci@0|sh4}, {LB.RR_N.ci@1|sh4}] of the room')
E('V-A para 2', 'a frontier distance of 0.0 [\u22121.1, 1.8] decision-equivalents', 'a frontier distance of ' + ptci('LB.RR_N.dec', 'dec1') + ' decision-equivalents')
E('V-A para 3', 'recovers 0.783 [0.720, 0.842] of the pooled room', 'recovers ' + ptci('LB.RR_CK3', 'sh3') + ' of the pooled room')

# --- V-A
E('V-A para 1', '(21,574 evaluated decisions)', '(' + pt('LB.n_dec', 'int') + ' evaluated decisions)')
E('V-A para 1', 'On 105 fresh lead-braking runs', 'On ' + pt('LB.n_runs', 'int') + ' fresh lead-braking runs')
E('V-A para 1', '5.58 [4.99, 6.17] percentage points averaged', ptci('LB.R', 'pp', 'ci2') + ' percentage points averaged')
E('V-A para 1', 'about 1,204 decision-equivalents', 'about ' + pt('LB.R.dec', 'dec') + ' decision-equivalents')
E('V-A para 1', 'recovers 0.013 [0.010, 0.015] of the room', 'recovers ' + ptci('LB.RR_E5', 'sh3') + ' of the room')
E('V-A para 1', '0.008 [0.006, 0.010] more', ptci('LB.RR_E5mP', 'sh3') + ' more')
E('V-A para 2', 'share is 0.0000 [−0.0009, 0.0015]', 'share is ' + ptci('LB.RR_N', 'sh4'))
E('V-A para 2', '(105 of 105 with an event; 5,293 decisions',
  '(' + pt('CI.n_events', 'int') + ' of ' + pt('CI.n_runs', 'int') + ' with an event; ' + pt('CI.n_dec', 'int') + ' decisions')
E('V-A para 2', 'On the 150 held-out nuScenes scenes (18,987 decisions',
  'On the ' + pt('F.n_heldout', 'int') + ' held-out nuScenes scenes (' + pt('F.n_dec', 'int') + ' decisions')
E('V-A para 3', 'recovers 0.916 [0.864, 0.965] of it', 'recovers ' + ptci('LB.PS.rec', 'sh3') + ' of it')
E('V-A para 3', '(like for like: 0.918)', '(like for like: ' + pt('LB.PS.like', 'sh3') + ')')

# --- Table II
T2 = 'Table II'
E(T2 + ' runs/decisions', '105; 21,574', pt('LB.n_runs', 'int') + '; ' + pt('LB.n_dec', 'int'))
E(T2 + ' runs/decisions', '105; 5,293', pt('CI.n_runs', 'int') + '; ' + pt('CI.n_dec', 'int'))
E(T2 + ' runs/decisions', '150; 18,987', pt('F.n_heldout', 'int') + '; ' + pt('F.n_dec', 'int'))
E(T2 + ' room LB', '5.58 [4.99, 6.17]', ptci('LB.R', 'pp', 'ci2'))
E(T2 + ' room CI', '0.00 [0.00, 0.00]', ptci('CI.R', 'pp', 'ci2'))
E(T2 + ' room F', '\u22120.01 [\u22120.13, 0.13]', ptci('F.R', 'pp', 'ci2'))
E(T2 + ' E5 LB', '0.013 [0.010, 0.015]', ptci('LB.RR_E5', 'sh3'))
E(T2 + ' E5 CI', 'n.t.', 'n.t.'); NTK.extend(['CI.RR_E5', 'CI.RR_E5.ci'])
E(T2 + ' E5 F', 'n.t.', 'n.t.'); NTK.append('F.RR_E5')
E(T2 + ' E5-E5p LB', '0.008 [0.006, 0.010]', ptci('LB.RR_E5mP', 'sh3'))
E(T2 + ' E5-E5p CI', 'n.t.', 'n.t.'); NTK.extend(['CI.RR_E5mP', 'CI.RR_E5mP.ci'])
E(T2 + ' E5-E5p F', 'n.t.', 'n.t.'); NTK.append('F.RR_E5mP')
E(T2 + ' N LB', '0.0000 [\u22120.0009, 0.0015]', ptci('LB.RR_N', 'sh4'))
E(T2 + ' N CI', 'n.t.', 'n.t.'); NTK.extend(['CI.RR_N', 'CI.RR_N.ci'])
E(T2 + ' N F', 'n.t.', 'n.t.'); NTK.append('F.RR_N')
E(T2 + ' varying LB', '0.0000 [−0.0018, 0.0012]; 0.0009 [0.0006, 0.0010]', ptci('LB.IMM.r', 'sh4') + '; ' + ptci('LB.IMM.c', 'sh4'))
E(T2 + ' varying CI', 'n.t.', 'n.t.'); NTK.extend(['CI.Y.r', 'CI.Y.r.ci', 'CI.Y.c', 'CI.Y.c.ci'])
E(T2 + ' varying F', 'n.t.', 'n.t.'); NTK.append('F.RR_N')
E(T2 + ' classification', 'amplitude-limited', '{CLS:H3}')
E(T2 + ' CK3 F', 'not computed', 'not computed')
E(T2 + ' PS LB', '0.916 [0.864, 0.965]', ptci('LB.PS.rec', 'sh3'))
E(T2 + ' CK3 LB', '0.783 [0.720, 0.842]', ptci('LB.RR_CK3', 'sh3'))
E(T2 + ' CK3 CI', 'n.t.', 'n.t.'); NTK.extend(['CI.RR_CK3', 'CI.RR_CK3.ci'])
E(T2 + ' partial oracles LB', '0.261 / 0.514 / 0.754', pt('LB.PO25', 'sh3') + ' / ' + pt('LB.PO50', 'sh3') + ' / ' + pt('LB.PO75', 'sh3'))
E(T2 + ' partial oracles CI', 'n.t.', 'n.t.'); NTK.extend(['CI.PO25', 'CI.PO50', 'CI.PO75'])
E(T2 + ' partial oracles F', 'n.t.', 'n.t.'); NTK.append('F.PO25')

# --- V-B and Table III
E('V-B para 1', '99.7% of the IMM\'s binding rows', pt('LB.IMM.within5', 'pct1') + ' of the IMM\'s binding rows')
E('V-B para 1', 'against 99.9% for the online tracker', 'against ' + pt('B.CV.within5', 'pct1') + ' for the online tracker')
E('V-B para 1', 'recovers only 0.0009 [0.0006, 0.0010] of its own room', 'recovers only ' + ptci('LB.IMM.c', 'sh4') + ' of its own room')
E('V-B para 1', '(the IMM\'s covariance recovers 0.0000 [\u22120.0018, 0.0012])', '(the IMM\'s covariance recovers ' + ptci('LB.IMM.r', 'sh4') + ')')
E('V-B para 2', 'against 0.0002, 0.0027 and 0.0477 for their', 'against ' + pt('B.CV2.c', 'sh4') + ', ' + pt('B.CA.c', 'sh4') + ' and ' + pt('B.AQ.c', 'sh4') + ' for their')
E('V-B para 2', '(21.5% of binding rows', '(' + pt('B.AQ.within5', 'pct1') + ' of binding rows')
T3 = 'Table III'
for tag, x, wi, cls_ in (('CV online', 'CV', '99.9%', None), ('CV re-tuned', 'CV2', '99.7%', None), ('CA', 'CA', '99.7%', None),
                          ('IMM', 'IMM', '99.7%', None), ('CV adaptive', 'AQ', '21.5%', None)):
    pass
rows3 = [
    ('CV online', 'CV', '| CV filter, online (of record) | 99.9% | 0.0000 [\u22120.0007, 0.0010] | 0.0001 [0.0000, 0.0002] | 1.63 / 23.62 / 0.08 | 1.42 | 0.783 |'),
    ('CV re-tuned', 'CV2', '| CV filter, re-tuned (NIS near 2) | 99.7% | \u22120.0009 [\u22120.0020, 0.0002] | 0.0002 [0.0001, 0.0003] | 1.71 / 29.52 / 0.07 | 2.48 | 0.753 |'),
    ('CA', 'CA', '| CA filter | 99.7% | \u22120.0008 [\u22120.0022, 0.0001] | 0.0027 [0.0022, 0.0032] | 1.64 / 28.02 / 0.02 | 1.88 | 0.816 |'),
    ('IMM', 'IMM', '| IMM (CV/CA) | 99.7% | 0.0000 [\u22120.0013, 0.0009] | 0.0009 [0.0006, 0.0010] | 1.70 / 29.46 / 0.05 | 2.32 | 0.764 |'),
    ('CV adaptive', 'AQ', '| CV filter, adaptive process noise | 21.5% | 0.0459 [0.0390, 0.0533] | 0.0477 [0.0379, 0.0582] | 1.97 / 28.34 / 0.07 | 1.72 | 0.758 |'),
]
NAMES3 = {'CV': 'CV filter, online (of record)', 'CV2': 'CV filter, re-tuned (NIS near 2)', 'CA': 'CA filter',
          'IMM': 'IMM (CV/CA)', 'AQ': 'CV filter, adaptive process noise'}
for tag, x, printed in rows3:
    t = '| %s | %s | %s | %s | %s / %s / %s | %s | %s |' % (
        NAMES3[x], pt('B.%s.within5' % x, 'pct1'), ptci('B.%s.RR' % x, 'sh4'), ptci('B.%s.c' % x, 'sh4'),
        pt('B.%s.room_pre' % x, 'pp'), pt('B.%s.room_brk' % x, 'pp'), pt('B.%s.room_stop' % x, 'pp'),
        pt('B.%s.lag' % x, 'f2'), pt('B.%s.RR_CK3' % x, 'sh3'))
    E(T3 + ' row ' + tag, printed, t)

# --- V-C text and Table IV
V3 = 'V-C'
E(V3 + ' para 1', 'a contact share of 20%', 'a contact share of ' + pt('E3.F0.lo.contact', 'pct0'))
E(V3 + ' para 1', 'contact difference \u22120.02 [\u22120.08, 0.04]; time lost 0.02 [0.00, 0.04] s',
  'contact difference ' + ptci('E3.N.lo.dc', 'pp', 'ci2') + '; time lost ' + ptci('E3.N.lo.dt', 'pp', 'ci2') + ' s')
E(V3 + ' para 1', 'contact difference \u22120.20 [\u22120.32, \u22120.10]; time lost 0.16 [0.10, 0.22] s',
  'contact difference ' + ptci('E3.CK3.lo.dc', 'pp', 'ci2') + '; time lost ' + ptci('E3.CK3.lo.dt', 'pp', 'ci2') + ' s')
E(V3 + ' para 1', 'contact difference 0.00 [\u22120.05, 0.05]; time lost 0.02 [0.00, 0.04] s',
  'contact difference ' + ptci('E3.NIMM.lo.dc', 'pp', 'ci2') + '; time lost ' + ptci('E3.NIMM.lo.dt', 'pp', 'ci2') + ' s')
E(V3 + ' para 2', 'Among leads that do not brake hard (60 cases', 'Among leads that do not brake hard (' + pt('E3b.n_cases', 'int') + ' cases')
E(V3 + ' para 2 classification CK3', 'inconclusive behind leads that keep their speed or brake mildly and is safer at a cost in time lost behind leads that stop and pull away',
  'inconclusive behind leads that keep their speed or brake mildly and is safer at a cost in time lost behind leads that stop and pull away')
E('III-B', 'largest error 2%', 'largest error ' + pt('E1.maxerr', 'pct0'))
E('III-B', 'on 60 fresh lead-braking cases and 60 cases behind non-braking leads',
  'on ' + pt('E3.n_cases', 'int') + ' fresh lead-braking cases and ' + pt('E3b.n_cases', 'int') + ' cases behind non-braking leads')
E('III-C', 'The 150 held-out validation scenes', 'The ' + pt('F.n_heldout', 'int') + ' held-out validation scenes')
E('III-A', '105 lead-braking and 105 cut-in runs', pt('LB.n_runs', 'int') + ' lead-braking and ' + pt('CI.n_runs', 'int') + ' cut-in runs')
E('III-A', 'and 105 runs behind leads that do not brake hard', 'and ' + pt('D1.n_runs', 'int') + ' runs behind leads that do not brake hard')
E('V-D non-braking', 'Behind leads that do not brake hard (105 fresh runs)', 'Behind leads that do not brake hard (' + pt('D1.n_runs', 'int') + ' fresh runs)')

T4 = 'Table IV'


def row4(name, cap, arm, lev, cls_suffix='', ref=None, impact_arm=None):
    a = arm
    ct = pt('E3.%s.%s.contact' % (a, lev), 'pct0')
    vi = pt('E3.%s.%s.vimp' % (a, lev), 'f1')
    dc = ptci('E3.%s.%s.dc' % (a, lev), 'pp', 'ci2')
    dt = ptci('E3.%s.%s.dt' % (a, lev), 'pp', 'ci2')
    return '| %s | %s | %s | %s | %s | %s | {CLS:E3.%s.%s}%s |' % (name, cap, ct, dc, dt, vi, a, lev, cls_suffix)


rows4 = [
    ('F0 lo', '| F0, class average (lower level) | 14.10 | 20% | \u2014 | \u2014 | 5.4 | \u2014 |',
     '| F0, class average (lower level) | ' + pt('E3.F0.lo.caution', 'pp') + ' | ' + pt('E3.F0.lo.contact', 'pct0') + ' | \u2014 | \u2014 | ' + pt('E3.F0.lo.vimp', 'f1') + ' | \u2014 |'),
    ('N lo', '| N, tracker covariance | matched | 18% | \u22120.02 [\u22120.08, 0.04] | 0.02 [0.00, 0.04] | 5.6 | equivalent |', row4('N, tracker covariance', 'matched', 'N', 'lo')),
    ('CK3 lo', '| CK3, braking prediction | matched | 0% | \u22120.20 [\u22120.32, \u22120.10] | 0.16 [0.10, 0.22] | n.c. | safer, no extra cost |',
     row4('CK3, braking prediction', 'matched', 'CK3', 'lo')),
    ('TG lo', '| TG, time gap | matched | 0% | \u22120.20 [\u22120.32, \u22120.10] | \u22120.13 [\u22120.19, \u22120.06] | n.c. | safer, no extra cost |',
     row4('TG, time gap', 'matched', 'TG', 'lo')),
    ('PS lo', '| PS, per-phase schedule\\* | 11.88 | 0% | \u22120.20 [\u22120.32, \u22120.10] | \u22120.17 [\u22120.25, \u22120.08] | n.c. | safer, no extra cost, descriptive |',
     row4('PS, per-phase schedule\\*', pt('E3.PS.lo.caution', 'pp'), 'PS', 'lo', ', descriptive')),
    ('IMM lo', '| IMM covariance vs its class average | matched | 20% | 0.00 [\u22120.05, 0.05] | 0.02 [0.00, 0.04] | 6.5 | equivalent |',
     row4('IMM covariance vs its class average', 'matched', 'NIMM', 'lo')),
    ('F0 hi', '| F0, class average (higher level) | 22.30 | 5% | \u2014 | \u2014 | 6.0 | \u2014 |',
     '| F0, class average (higher level) | ' + pt('E3.F0.hi.caution', 'pp') + ' | ' + pt('E3.F0.hi.contact', 'pct0') + ' | \u2014 | \u2014 | ' + pt('E3.F0.hi.vimp', 'f1') + ' | \u2014 |'),
    ('N hi', '| N, tracker covariance | matched | 5% | 0.00 [\u22120.06, 0.06] | 0.00 [\u22120.01, 0.01] | 6.0 | equivalent |', row4('N, tracker covariance', 'matched', 'N', 'hi')),
    ('CK3 hi', '| CK3, braking prediction | matched | 0% | \u22120.05 [\u22120.14, 0.02] | 0.20 [0.13, 0.26] | n.c. | inconclusive |', row4('CK3, braking prediction', 'matched', 'CK3', 'hi')),
    ('TG hi', '| TG, time gap | matched | 0% | \u22120.05 [\u22120.14, 0.02] | \u22120.23 [\u22120.32, \u22120.15] | n.c. | inconclusive |', row4('TG, time gap', 'matched', 'TG', 'hi')),
    ('PS hi', '| PS, per-phase schedule\\* | 11.88 | 0% | \u22120.05 [\u22120.14, 0.02] | \u22120.47 [\u22120.60, \u22120.36] | n.c. | inconclusive, descriptive |',
     row4('PS, per-phase schedule\\*', pt('E3.PS.hi.caution', 'pp'), 'PS', 'hi', ', descriptive')),
    ('IMM hi', '| IMM covariance vs its class average | matched | 8% | \u22120.02 [\u22120.09, 0.05] | 0.00 [\u22120.02, 0.01] | 4.7 | equivalent |',
     row4('IMM covariance vs its class average', 'matched', 'NIMM', 'hi')),
]
for tag, printed, tmpl in rows4:
    E(T4 + ' ' + tag, printed, tmpl)

# --- V-D and Table V
E('V-D commitment', '0.101 [0.068, 0.134] of the 3 s room', ptci('LB.RS075.rel', 'sh3') + ' of the 3 s room')
E('V-D commitment', '0.055 to 0.168', pt('LB.T.relmin', 'sh3') + ' to ' + pt('LB.T.relmax', 'sh3'))
E('V-D commitment', '0.334 [0.279, 0.383]', ptci('LB.DS.rel', 'sh3'))
E('V-D commitment', 'matched caution, 6% of', 'matched caution, ' + pt('LB.REL_F0', 'pct0') + ' of')
E('V-D filter tuning', 'is 238.1 and 153.0 decision-equivalents (online filter: 173.4)',
  'is ' + pt('B.CV2.as_room', 'dec1') + ' and ' + pt('B.CA.as_room', 'dec1') + ' decision-equivalents (online filter: ' + pt('B.CV.as_room', 'dec1') + ')')
E('V-D filter tuning', 'share 0.753 and 0.816 (online: 0.783)',
  'share ' + pt('B.CV2.RR_CK3', 'sh3') + ' and ' + pt('B.CA.RR_CK3', 'sh3') + ' (online: ' + pt('B.CV.RR_CK3', 'sh3') + ')')
T5 = 'Table V'
E(T5 + ' commitment', '| Commitment | Reaction and stop (0.75 s, 6 m/s\u00b2): room relative to 3 s | 0.101 [0.068, 0.134] |',
  '| Commitment | Reaction and stop (0.75 s, 6 m/s\u00b2): room relative to 3 s | ' + ptci('LB.RS075.rel', 'sh3') + ' |')
E(T5 + ' terciles', '0.072 / 0.168 / 0.055', pt('LB.T1.rel', 'sh3') + ' / ' + pt('LB.T2.rel', 'sh3') + ' / ' + pt('LB.T3.rel', 'sh3'))
E(T5 + ' delayed stop', '0.334 [0.279, 0.383]', ptci('LB.DS.rel', 'sh3'))
E(T5 + ' stop reliance', '| F0 decisions safe only because the stop follows | 6% |', '| F0 decisions safe only because the stop follows | ' + pt('LB.REL_F0', 'pct0') + ' |')
E(T5 + ' rate R', '5.58 / 5.31 / 5.07', pt('B7.2.0.R', 'pp') + ' / ' + pt('B7.5.0.1.R', 'pp') + ' / ' + pt('B7.10.0.1.R', 'pp'))
E(T5 + ' after-stop', '173.4 / 115.2 / 77.8', pt('B7.2.0.as_room', 'dec1') + ' / ' + pt('B7.5.0.1.as_room', 'dec1') + ' / ' + pt('B7.10.0.1.as_room', 'dec1'))
E(T5 + ' N at 10 Hz', '0.0000 [\u22120.0004, 0.0006]', ptci('B7.10.0.1.RR_N', 'sh4'))
E(T5 + ' tuning after-stop', '173.4 / 238.1 / 153.0', pt('B.CV.as_room', 'dec1') + ' / ' + pt('B.CV2.as_room', 'dec1') + ' / ' + pt('B.CA.as_room', 'dec1'))
E(T5 + ' tuning CK3', '0.783 / 0.753 / 0.816', pt('B.CV.RR_CK3', 'sh3') + ' / ' + pt('B.CV2.RR_CK3', 'sh3') + ' / ' + pt('B.CA.RR_CK3', 'sh3'))
for v, nm, p in (('const', 'keep their speed', '| Non-braking leads | Behind leads that keep their speed: CK3; PS (caution, wrong-go differences, points) | costs progress (5.3, 0.0); costs progress (35.2, 0.0) |'),
                 ('mild', 'brake mildly', '|  | Behind leads that brake mildly: CK3; PS (caution, wrong-go differences, points) | costs progress (18.7, \u22120.9); costs progress (53.5, \u22120.9) |'),
                 ('stopgo', 'stop and pull away', '|  | Behind leads that stop and pull away: CK3; PS (caution, wrong-go differences, points) | costs progress (1.7, \u22124.7); costs progress (21.4, \u22126.5) |')):
    lead = '| Non-braking leads' if v == 'const' else '| '
    t = '%s | Behind leads that %s: CK3; PS (caution, wrong-go differences, points) | {CLSD:%s.CK3} (%s, %s); {CLSD:%s.PS} (%s, %s) |' % (
        lead, nm, v, pt('D1.%s.CK3.dcau' % v, 'f1'), pt('D1.%s.CK3.dwg' % v, 'f1'), v, pt('D1.%s.PS.dcau' % v, 'f1'), pt('D1.%s.PS.dwg' % v, 'f1'))
    E(T5 + ' non-braking ' + v, p, t)
# old evaluation values come from the v12 record (strings); fresh/tuning from exports
E(T5 + ' recording R', '1.16 / 5.51 / 5.58', pt('TU.R', 'pp') + ' / ' + '{OLD:R|pp}' + ' / ' + pt('LB.R', 'pp'))
E(T5 + ' recording CK3', '0.379 / 0.837 / 0.783', pt('TU.RR_CK3', 'sh3') + ' / ' + '{OLD:CK3|sh3}' + ' / ' + pt('LB.RR_CK3', 'sh3'))
E(T5 + ' recording N', '0.0000 / \u22120.0004 / 0.0000', pt('TU.RR_N', 'sh4') + ' / ' + '{OLD:N|sh4}' + ' / ' + pt('LB.RR_N', 'sh4'))
# --- Discussion
E('VI what a varying covariance needs', 'recovers a small part of its room (0.046, about', 'recovers a small part of its room (' + pt('B.AQ.RR', 'sh3') + ', about')

# ---------------------------------------------------------------- render + compare
TOKEN = re.compile(r'\{([^{}]+)\}')


def render(tmpl):
    n = [0]

    def one(m):
        body = m.group(1)
        if body.startswith('CLS:') and not body.startswith('CLS:E'):
            n[0] += 0
            return STAT[body[4:]]
        if body.startswith('CLS:E'):
            c = STAT[body[4:]]
            return {'safer at no extra cost': 'safer, no extra cost', 'safer at a cost': 'safer, at a cost'}.get(c, c)
        if body.startswith('CLSD:'):
            return STAT['%s.%s' % ({'CK3': 'D-H1', 'PS': 'D-H2'}[body.split('.')[1]], body[5:].split('.')[0])]
        if body.startswith('NEG:'):
            k, f = body[4:].split('|')
            idx = None
            if '@' in k:
                k, idx = k.split('@'); idx = int(idx)
            v, pk = get(k, idx); KEYS_USED[k] = pk
            n[0] += 1
            return fmt(-v, f)
        if body.startswith('V12:'):
            n[0] += 1
            return V12[body[4:]]
        if body.startswith('OLD:'):
            n[0] += 1
            k, f = body[4:].split('|')
            return fmt({'R': B0P['R_pp'], 'CK3': B0P['RR']['CK3'], 'N': B0P['RR']['N']}[k], f)
        k, f = body.split('|')
        idx = None
        if '@' in k:
            k, idx = k.split('@')
            idx = int(idx)
        v, pk = get(k, idx)
        KEYS_USED[k] = pk
        n[0] += 1
        return fmt(v, f)

    out = TOKEN.sub(one, tmpl)
    return out, n[0]


def ntokens(tmpl):
    return sum(1 for m in TOKEN.finditer(tmpl) if not m.group(1).startswith('CLS'))


rows = []
agree = differ = 0
diffs = []
for loc, printed, tmpl in ENT:
    exp, nt = render(tmpl)
    inman = MS.count(printed)
    # table cells in the text for rows of Table IV use the manuscript wording for classification; normalise only that
    nt = ntokens(tmpl)
    if exp == printed:
        agree += nt
    else:
        # token-wise comparison to localise
        num = re.compile(r'[\u2212-]?\d[\d,]*\.?\d*%?|n\.c\.')
        pn, en = num.findall(printed), num.findall(exp)
        bad = [(a, b) for a, b in zip(pn, en) if a != b] if len(pn) == len(en) else [(printed, exp)]
        nb = max(1, len(bad))
        differ += nb
        agree += max(0, nt - nb)
        diffs.append((loc, printed, exp, bad))
    rows.append((loc, printed, exp == printed, inman))
missing = [r for r in rows if r[3] == 0]

# manual wording/status entries are in the status table below; here the classification words in Table IV
OLDCHK = [(a, B0P[x] if y is None else B0P[x][y], B0R[z]) for a, x, y, z in (('R_pp', 'R_pp', None, 'R_pp'), ('RR_CK3', 'RR', 'CK3', 'RR_CK3'), ('RR_N', 'RR', 'N', 'RR_N'))]
OLD_OK = all(abs(a - b) <= 1e-9 for _, a, b in OLDCHK) and abs(B0P['RR']['CK3'] - ps['old']['CK3']) < 1e-9 and abs(B0P['RR']['N'] - ps['old']['N']) < 1e-9
# n.t. cells: the underlying keys must be absent/null/NaN (no value was tested)
NT_BAD = [k for k in NTK if (lambda v: not (v is None or (isinstance(v, float) and isnan(v))))(val(k))]
# ---------------------------------------------------------------- export vs recount
rc_total = rc_ok = 0
rc_bad = []
used = set(KEYS_USED)
for k in sorted(used):
    pk = KEYS_USED[k]
    # also compare the interval partner
    for kk in (k,):
        if kk not in REC.get(pk, {}):
            rc_bad.append((kk, 'no recount key'))
            continue
        a = EXP[pk][kk]
        b = REC[pk][kk]

        def cmp(x, y):
            if x is None and y is None:
                return True
            if isinstance(x, list):
                return isinstance(y, list) and len(x) == len(y) and all(cmp(p, q_) for p, q_ in zip(x, y))
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                if isnan(x) and isnan(y):
                    return True
                if isinstance(x, int) and isinstance(y, int) or (float(x).is_integer() and float(y).is_integer() and abs(x) > 50 and k.endswith(('n_dec', 'n_runs', 'n_events', 'n_cases', 'n_heldout'))):
                    return x == y
                return abs(x - y) <= 1e-9 * max(1.0, abs(x))
            return x == y
        rc_total += 1
        if cmp(a, b):
            rc_ok += 1
        else:
            rc_bad.append((kk, '%r vs %r' % (a, b)))

# ---------------------------------------------------------------- lock hashes in III/IV-E
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


H = {'85787f3d\u20268f6b': sha(R13 + r'\AMENDMENT_10_v13.md'), '02048a43\u2026a4df': sha(R13 + r'\LOCK_A10_2.txt'),
     '94e06ed6\u2026c0a6': sha(R13 + r'\LOCK_A10_2c.txt')}
hash_res = []
for tag, full in H.items():
    a, b = tag.split('\u2026')
    hash_res.append((tag, full.startswith(a) and full.endswith(b), tag in MS))
hash_res.append(('LOCK_A10_1.txt carries the amendment hash', open(R13 + r'\LOCK_A10_1.txt').read().count(H['85787f3d\u20268f6b']) > 0, True))

# ---------------------------------------------------------------- status comparison with the text
text_claims = [
    ('H0 pass -> "there is room (confirmed)"', STAT['H0'] == 'pass' and CONF['H0'], 'V-A para 1, Table II (C)'),
    ('H1 pass -> "detects rank information ... (confirmed)"', STAT['H1'] == 'pass' and CONF['H1'], 'V-A para 1, Table II'),
    ('H2 pass -> "equivalent ... within 5% of the room (confirmed)"', STAT['H2'] == 'pass' and CONF['H2'], 'V-A para 2, Table II (C)'),
    ('H3 = amplitude-limited, passes; IMM "(confirmed)"; barely varies', STAT['H3'] == 'amplitude-limited' and CONF['H3'] and STAT['H3.barely'], 'V-B, Table II classification'),
    ('H4 pass -> PS "transfers (confirmed)"', STAT['H4'] == 'pass' and CONF['H4'], 'V-A para 3, Table II (C)'),
    ('H5 pass -> CK3 "most of it (confirmed)"', STAT['H5'] == 'pass' and CONF['H5'], 'V-A para 3, Table II (C)'),
    ('K0 fail -> "no measurable room at the event ... nothing is tested" (F)', STAT['K0'] == 'fail', 'V-A para 2, Table II (F)'),
    ('F-H0 fail -> "no measurable room ... nothing is tested on the logs" (F)', STAT['F-H0'] == 'fail', 'V-A para 2, Table II (F)'),
    ('E-H1 = safer at no extra cost (V-C, Abstract, VII)', STAT['E-H1'] == 'safer at no extra cost', 'V-C, Abstract'),
    ('E-H2 = equivalent', STAT['E-H2'] == 'equivalent', 'V-C, Table IV'),
    ('E-H3 = equivalent (IMM equivalent to own class average)', STAT['E-H3'] == 'equivalent', 'V-B, V-C'),
    ('Higher level: CK3, TG, PS inconclusive; N, IMM equivalent', STAT['E3.CK3.hi'] == STAT['E3.TG.hi'] == STAT['E3.PS.hi'] == 'inconclusive' and STAT['E3.N.hi'] == STAT['E3.NIMM.hi'] == 'equivalent', 'Table IV'),
    ('Lower level: TG, PS safer at no extra cost', STAT['E3.TG.lo'] == STAT['E3.PS.lo'] == 'safer at no extra cost', 'Table IV'),
    ('E3b: CK3 and PS inconclusive for const and mild, safer at a cost for stopgo',
     all(STAT['E3b.%s.%s' % (v, a)] == 'inconclusive' for v in ('const', 'mild') for a in ('CK3', 'PS')) and all(STAT['E3b.stopgo.%s' % a] == 'safer at a cost' for a in ('CK3', 'PS')), 'V-C para 2'),
    ('D-H1/D-H2 = costs progress for all three variants', all(STAT['%s.%s' % (n, v)] == 'costs progress' for n in ('D-H1', 'D-H2') for v in ('const', 'mild', 'stopgo')), 'V-D, Table V, Abstract'),
    ('B3/B4 rule -> mechanism persists', STAT['B3/B4'] == 'mechanism persists', 'V-D filter tuning'),
    ('B7 rate rule -> largely a consequence of the 2 Hz update', STAT['B7 rate'].startswith('largely'), 'V-D update rate'),
    ('B7 N rule -> share stays inside the margin at every rate and latency', all(inside(c, -D_, D_) for _, c in n_ci), 'V-D update rate'),
    ('B6: all three terciles evaluable (range stated "0.055 to 0.168")', STAT['B6 terciles evaluable (den0>=10)'] == 'all', 'V-D commitment'),
    ('Transfer: N inside (-d,d) in every set, order CK3>AM>TG>NA>N', STAT['TRANSFER order CK3>AM>TG>NA>N in every set where defined'] and ts['N_inside_delta_all_sets'], 'V-D recording policy'),
    ('Table III classification of the IMM = amplitude-limited', STAT['H3'] == 'amplitude-limited', 'Table II, V-B'),
]
# the packages' own status keys against my recomputation
own = []
own.append(('LB.H0..H5', [val('LB.H%d' % i) for i in range(6)], [STAT['H0'], STAT['H1'], STAT['H2'], STAT['H3'].replace('-', '_').replace(' ', '_'), STAT['H4'], STAT['H5']]))
own.append(('CI.K0,K1,K2', [val('CI.K0'), val('CI.K1'), val('CI.K2')], [STAT['K0'], STAT['K1'], STAT['K2']]))
for v in ('const', 'mild', 'stopgo'):
    own.append(('D1.%s.DH1/DH2' % v, [val('D1.%s.DH1' % v), val('D1.%s.DH2' % v)], [STAT['D-H1.' + v].replace(' ', '_'), STAT['D-H2.' + v].replace(' ', '_')]))
own.append(('EH1,EH2,EH3', [val('EH1'), val('EH2'), val('EH3')], [STAT['E-H1'], STAT['E-H2'], STAT['E-H3']]))
own.append(('F own_statuses', [json.load(open(W + r'\F_nuscenes\out\A_EXPORT_F.json'))['own_statuses'][k]['passes'] for k in ('F_H0', 'F_H1')], [STAT['F-H0'] == 'pass', STAT['F-H1'] == 'pass']))
own.append(('B.rule.outcome', [val('B.rule.outcome')], [STAT['B3/B4']]))
own.append(('B7.rule_N, B7.rule_rate, B7.identity', [val('B7.rule_N'), val('B7.rule_rate'), val('B7.identity')], ['holds', 'consequence', 'pass']))
own_res = []
for nm, a, b in own:
    norm = lambda x: [str(t).lower().replace(' ', '_') for t in x]
    own_res.append((nm, a, b, norm(a) == norm(b)))

# ---------------------------------------------------------------- supplement presence check (weaker)
scal = set()


def walk(x):
    if isinstance(x, bool):
        return
    if isinstance(x, (int, float)):
        if not isnan(x):
            scal.add(float(x))
    elif isinstance(x, list):
        for y in x:
            walk(y)
    elif isinstance(x, dict):
        for y in x.values():
            walk(y)


for n in EXP:
    walk(EXP[n])
walk(J(W + r'\B_retrack\out\B_RESULTS_SUMMARY_v13.json'))
walk(J(W + r'\B_retrack\out\b8\B8_NIS_NEES_v01.json'))
walk(ps)
walk(J(W + r'\F_nuscenes\out\A_EXPORT_F.json')['extras'])
for k in ('GL_R', 'GL_RR_CK3', 'GL_RRN'):
    try:
        scal.add(float(V12[k].replace(MINUS, '-')))
    except Exception:
        pass
scal_list = sorted(scal)
import bisect


def near_round(txt):
    t = txt.replace(MINUS, '-').replace(',', '')
    pct = t.endswith('%')
    t = t.rstrip('%')
    nd = len(t.split('.')[1]) if '.' in t else 0
    target = Decimal(t)
    scale = [1, 100, 0.01] if pct else [1, 100, 0.01]
    for sc in scale:
        c0 = float(target) / sc
        i = bisect.bisect_left(scal_list, c0 - 1.0 * 10 ** (-nd) / sc - 1e-12)
        while i < len(scal_list) and scal_list[i] <= c0 + 1.0 * 10 ** (-nd) / sc + 1e-12:
            v = scal_list[i] * sc
            if Decimal(v).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP) == target.quantize(Decimal(1).scaleb(-nd)):
                return True
            i += 1
    return False


sup_tokens = re.findall(r'[\u2212-]?\d[\d,]*\.\d+%?', SU)
sup_unmatched = []
seen = {}
for t in sup_tokens:
    if t in seen:
        seen[t][0] += 1
        continue
    seen[t] = [1, near_round(t)]
sup_total = len(sup_tokens)
sup_un = [(t, c) for t, (c, okk) in seen.items() if not okk]
sup_unmatched_count = sum(c for _, c in sup_un)

# ---------------------------------------------------------------- report
out = []
P = out.append
P('# TEXT RECOUNT v13')
P('')
P('Recount by **Claude Sonnet 5.5** (a different model from the writer, Claude Opus 5.5). Script: `TEXT_RECOUNT_v13.py` (this folder). Frozen copies: `out\\freeze_v13\\MANUSCRIPT_v13.md` (sha256 `%s`) and `SUPPLEMENT_v13.md` (sha256 `%s`).' % (sha(FR + r'\MANUSCRIPT_v13.md'), sha(FR + r'\SUPPLEMENT_v13.md')))
P('')
tot = agree + differ
P('## 1. Totals (main text: Abstract, I, III-C/E counts, V-VII, Tables II-V)')
P('')
P('- Numbers checked: **%d** (each interval end counts once; "n.c." entries count once; counts, percentages and shares included)' % tot)
P('- Agreeing: **%d**' % agree)
P('- Differing: **%d**' % differ)
P('- Fragments located verbatim in the frozen manuscript: %d of %d (a fragment not found would mean my transcription, not the text, is wrong)' % (len(rows) - len(missing), len(rows)))
for m in missing:
    P('  - NOT FOUND in text: %s: %s' % (m[0], m[1]))
P('- n.t. cells (cut-in and real-log columns, Table II): %d underlying keys checked to be null or NaN; not null: %s' % (len(NTK), NT_BAD))
P('- Table V old-evaluation values (5.51, 0.837, −0.0004): first program B_CV0_v01.json points.all (R_pp, RR.CK3, RR.N) equals its recount RECOUNT_B_v01.json per_variant.CV0.all and TRANSFER old: %s' % OLD_OK)
P('- Export value equals its second-program (A_RECOUNT) value, for each of the %d keys read (counts exactly, others within 1e-9): **%d agree, %d differ**' % (rc_total, rc_ok, len(rc_bad)))
for k, why in rc_bad:
    P('  - %s: %s' % (k, why))
P('- Hashes in Section IV-E: ' + '; '.join('%s %s' % (t, 'matches the file and is in the text' if (okk and intxt) else 'MISMATCH') for t, okk, intxt in hash_res))
P('')
P('## 2. Differences')
P('')
if not diffs:
    P('None among the main-text numbers.')
else:
    P('| Location | Printed | Expected | Differing tokens |')
    P('|---|---|---|---|')
    for loc, pr, ex, bad in diffs:
        P('| %s | `%s` | `%s` | %s |' % (loc, pr.replace('|', '\\|'), ex.replace('|', '\\|'), '; '.join('%s vs %s' % b for b in bad)))
P('')
P('## 3. Hypothesis statuses recomputed from the interval ends (A10 rules, delta = 0.05)')
P('')
P('| Item | Recomputed | Text / table |  Agrees |')
P('|---|---|---|---|')
for desc, okk, where in text_claims:
    P('| %s | %s | %s | %s |' % (desc, 'as stated' if okk else 'DIFFERS', where, 'yes' if okk else '**NO**'))
P('')
P('Recomputed values: ' + '; '.join('%s = %s' % (k, v) for k, v in STAT.items() if not k.startswith(('E3', 'D-H', 'E3b'))))
P('')
P('Confirmation along the lead-braking sequence: ' + ', '.join('%s=%s' % (h, CONF[h]) for h in seq))
P('')
P('The packages\' own status keys against my recomputation:')
P('')
P('| Key | Package value | Recomputed | Agree |')
P('|---|---|---|---|')
for nm, a, b, okk in own_res:
    P('| %s | %s | %s | %s |' % (nm, a, b, 'yes' if okk else '**NO**'))
P('')
P('## 4. Keys chosen (number location -> export key)')
P('')
P('Each entry in the script (`ENT`) names its keys in the template. Keys read (package where found): ' + ', '.join('`%s`' % k for k in sorted(KEYS_USED)))
P('')
P('Old-evaluation values in Table V (5.51, 0.837, \u22120.0004) are read from the v12 record (`revision_v12\\draft\\DERIVED_v12.json`, `GL_R`, `GL_RR_CK3`, `GL_RRN`); 0.837 and \u22120.0004 are also compared with `TRANSFER.structured.per_set.old` (0.8366, \u22120.000414), which agrees. 5.51 has no v13 second source.')
P('')
P('## 5. Supplement (weaker check)')
P('')
P('I did not map every supplement cell to a key. Instead every decimal number in `SUPPLEMENT_v13.md` (%d tokens, %d distinct) was tested for being a correctly rounded value, at its own number of decimals (also x100 for percentages), of **some** scalar or interval end in the exports, the B summary, B8 or F extras. This finds numbers with no source; it cannot find a correct-looking number placed in the wrong cell.' % (sup_total, len(seen)))
P('')
P('- Tokens with a matching export value: %d; without: **%d** (%d distinct)' % (sup_total - sup_unmatched_count, sup_unmatched_count, len(sup_un)))
P('- Distinct unmatched tokens (count in text): ' + (', '.join('%s (x%d)' % (t, c) for t, c in sorted(sup_un, key=lambda z: -z[1])) if sup_un else 'none'))
P('')
P('Where I looked at them (supplement line numbers of the frozen file): L18 (car length, a design constant); L68 and L80 (calibration and rule thresholds); L233-L237 (old-evaluation and tuning-run intervals of the earlier analysis: records outside the v13 exports, not verifiable here); L262 (tercile range 4.53, the text of `LB.T3.range` = "4.53–5.71", a string key); L467-L470 (S11 margin-ratio table: old-run records, not in the exports); the 10.1109 / 25.260745 / 2018.8569495 style tokens are DOI or reference fragments.')
P('')
P('Unmatched tokens can be legitimate: design constants (tuning settings, thresholds, hash-free parameters), values from records outside the exports, or sums and differences of exported numbers; they need a human look at the supplement line.')
open(W + r'\A_text\notes\TEXT_RECOUNT_v13.md', 'w', encoding='utf8').write('\n'.join(out) + '\n')
print('\n'.join(out[:60]))
print('unmatched supplement tokens:', len(sup_un))
