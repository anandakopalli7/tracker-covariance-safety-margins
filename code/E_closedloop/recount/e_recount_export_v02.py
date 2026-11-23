"""e_recount_export_v02.py - writes A_RECOUNT_E.json (RESULTS_INTERFACE_v13.md sections 1 and 3, "E") from the outputs of the
second program (e_recount_v03.py): outcomes (E3, E3b), compare, brake (E1), calibration (E2) and matched. Written from the
interface and the captions of Tables S9 and IV only; the first program was not read.  Python 3 standard library only.

python -I -B e_recount_export_v02.py --e3 o_e3.json --e3b o_e3b.json --compare cmp.json --e1 e1.json --calib calib.json
        --matched matched.json --status ran --e1-attempts 1 --out A_RECOUNT_E.json
"""
import argparse
import datetime
import hashlib
import json
import math
import statistics
from pathlib import Path

ARMS = {'N': 'E_N', 'CK3': 'E_CK3', 'TG': 'E_TG', 'PS': 'E_PS', 'NIMM': 'E_N_IMM', 'F0': 'E_F0', 'F0IMM': 'E_F0_IMM'}
REF = {'N': 'E_F0', 'CK3': 'E_F0', 'TG': 'E_F0', 'PS': 'E_F0', 'NIMM': 'E_F0_IMM'}       # NIMM against F0IMM, the others against F0
LEVS = ('lo', 'hi')
VARIANTS = {'const': 'constant', 'mild': 'mild_braking', 'stopgo': 'stop_and_go'}
B_ARMS = ('N', 'CK3', 'PS', 'TG')
STATUS_ARG = ('ran', 'stopped_brake', 'stopped_other')


def rj(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def clean(x):
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    return x


def of_record(rows):
    """Valid runs only; one per (arm, level, lead_variant, case): the last by run id (as the compare step does)."""
    d = {}
    for r in sorted((r for r in rows if r.get('valid')), key=lambda r: r['run_id']):
        d[(r.get('arm'), r.get('level'), r.get('lead_variant'), r.get('case'))] = r
    return list(d.values())


def mean(v):
    return sum(v) / len(v) if v else None


def median(v):
    return float(statistics.median(v)) if v else None


def defined(rows, key):
    return [float(r[key]) for r in rows if r.get(key) is not None]


def arm_summary(rows, pre, V):
    """Table S9 / IV caption definitions, over the arm-and-level's valid runs of record."""
    if not rows:
        for s in ('contact', 'vimp', 'tlost', 'restgap', 'peakdec', 'jerk', 'fallback'):
            V[pre + '.' + s] = None
        return
    V[pre + '.contact'] = sum(1 for r in rows if r.get('contact')) / len(rows)
    V[pre + '.vimp'] = median(defined(rows, 'impact_speed_mps'))              # runs with contact
    V[pre + '.tlost'] = mean(defined(rows, 'time_lost_s'))                    # runs without contact (null with contact)
    V[pre + '.restgap'] = mean(defined(rows, 'rest_gap_m'))
    V[pre + '.peakdec'] = median(defined(rows, 'peak_decel_mps2'))
    V[pre + '.jerk'] = median(defined(rows, 'rms_jerk_mps3'))
    # share of decisions in full braking, pooled over the arm's assessment decisions: sum of counts / sum of decisions
    num = den = 0
    for r in rows:
        n = r.get('n_assessment_decisions'); s = r.get('fallback_share')
        if n and s is not None:
            num += int(round(s * n)); den += int(n)
    V[pre + '.fallback'] = (num / den) if den else None


def find(comps, **kw):
    for c in comps:
        if all(c.get(k) == v for k, v in kw.items()) and not c.get('extra_pair'):
            return c
    return None


def diffs(c, pre, V):
    ok = c is not None and c.get('pairs', 0) > 0 and 'contact_diff' in c
    V[pre + '.dc'] = c['contact_diff'] if ok else None
    V[pre + '.dc.ci'] = [c['contact_diff_lo'], c['contact_diff_hi']] if ok else None
    V[pre + '.dt'] = c.get('time_lost_diff') if ok else None
    lo = c.get('time_lost_lo') if ok else None
    hi = c.get('time_lost_hi') if ok else None
    V[pre + '.dt.ci'] = [lo, hi] if lo is not None and hi is not None else None
    # descriptive paired mean differences (arm minus reference) with the same bootstrap interval (A10 7.5)
    oc = c.get('outcomes', {}) if ok else {}
    for name, key in (('d_vimp', 'impact_speed_mps'), ('d_restgap', 'rest_gap_m'), ('d_peakdec', 'peak_decel_mps2'),
                      ('d_jerk', 'rms_jerk_mps3'), ('d_fallback', 'fallback_share')):
        o = oc.get(key)
        V[pre + '.' + name] = o.get('mean_diff') if o else None
        V[pre + '.' + name + '.ci'] = [o['ci_lo'], o['ci_hi']] if o and o.get('ci_lo') is not None and o.get('ci_hi') is not None else None


def gkey(g):
    return 'g' + ('%g' % g).replace('.', '_')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--e3', required=True)
    p.add_argument('--e3b', required=True)
    p.add_argument('--compare', required=True)
    p.add_argument('--e1', required=True)
    p.add_argument('--calib', required=True)
    p.add_argument('--matched', required=True)
    p.add_argument('--status', required=True, choices=STATUS_ARG)
    p.add_argument('--e1-attempts', type=int, default=1)
    p.add_argument('--lock2', default=None, help='default: revision_v13\\LOCK_A10_2.txt if it exists')
    p.add_argument('--out', required=True)
    a = p.parse_args(argv)
    me = Path(__file__).resolve()
    lock = Path(a.lock2) if a.lock2 else me.parents[3] / 'LOCK_A10_2.txt'
    lock_sha = hashlib.sha256(lock.read_bytes()).hexdigest() if lock.exists() else None

    e3 = of_record(rj(a.e3)['runs'])
    e3b = of_record(rj(a.e3b)['runs'])
    comps = rj(a.compare)['comparisons']
    V = {}
    V['E.status'] = a.status

    # ---- E1 (brake test)
    b = rj(a.e1)
    byid = {r['run_id']: r for r in b['runs']}
    errs = []
    for sp in (5, 10, 15):
        ps = (b.get('per_speed') or {}).get(str(sp))
        r = byid.get(ps['run_id']) if ps and ps.get('run_id') else None
        pre = 'E1.v%d' % sp
        if r and r.get('stop_dist_m') is not None and r.get('model_dist_m'):
            V[pre + '.dist'] = r['stop_dist_m']
            V[pre + '.model'] = r['model_dist_m']
            V[pre + '.err'] = abs(r['stop_dist_m'] / r['model_dist_m'] - 1.0)
            errs.append(V[pre + '.err'])
        else:
            V[pre + '.dist'] = V[pre + '.model'] = V[pre + '.err'] = None
    V['E1.maxerr'] = max(errs) if errs else None
    V['E1.attempts'] = a.e1_attempts

    # ---- E2 (calibration)
    c2 = rj(a.calib)
    for r in c2['per_g']:
        V['E2.%s.contact' % gkey(r['g'])] = r['share']
    V['E2.g_lo'] = c2['g_lo']
    V['E2.g_hi'] = c2['g_hi']
    V['E2.low_power'] = bool(c2['low_power'])

    # ---- E3
    mt = rj(a.matched)['levels_out']
    for short, arm in ARMS.items():
        for lev in LEVS:
            pre = 'E3.%s.%s' % (short, lev)
            arm_summary([r for r in e3 if r.get('arm') == arm and r.get('level') == lev], pre, V)
            if short in REF:
                diffs(find(comps, set='E3', arm=arm, reference=REF[short], level=lev), pre, V)
            if short == 'F0':
                V[pre + '.caution'] = (mt.get(lev) or {}).get('F0_caution_at_gL')
            if short == 'PS':
                psd = ((mt.get(lev) or {}).get('arms') or {}).get('PS')
                V[pre + '.caution'] = psd.get('caution') if psd else None
    V['E3.PS.caution_matched'] = False
    V['E3.n_cases'] = len({r['case'] for r in e3})
    V['E3.NIMM.dropped'] = not (any(r['arm'] == 'E_N_IMM' for r in e3) and any(r['arm'] == 'E_F0_IMM' for r in e3))
    for h, short in (('EH1', 'CK3'), ('EH2', 'N'), ('EH3', 'NIMM')):
        c = find(comps, set='E3', arm=ARMS[short], reference=REF[short], level='lo')
        V[h] = c.get('classification') if c else None

    # ---- E3b
    for vk, kind in VARIANTS.items():
        for short in B_ARMS:
            c = find(comps, set='E3b', arm=ARMS[short], reference='E_F0', level='lo', lead_variant=kind)
            diffs(c, 'E3b.%s.%s' % (vk, short), V)
    V['E3b.n_cases'] = len({r['case'] for r in e3b})

    out = dict(package='E', written=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), program=me.name,
               program_sha256=hashlib.sha256(me.read_bytes()).hexdigest(), lock2_sha256=lock_sha,
               values={k: clean(V[k]) for k in V})
    Path(a.out).write_text(json.dumps(out, indent=1), encoding='utf-8')
    print('wrote %s: %d keys' % (a.out, len(V)))


if __name__ == '__main__':
    main()
