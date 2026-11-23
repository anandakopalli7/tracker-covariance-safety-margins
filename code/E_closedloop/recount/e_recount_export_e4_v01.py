"""e_recount_export_e4_v01.py - writes A_RECOUNT_E4.json (set E4, detection dropout, A11 6d.7) from the outputs of the second
program (e_recount_v04.py): E4 outcomes, compare_e4 and matched. Written from the pre-registration text only; the first program
was not read. Python 3 standard library only.

python -I -B e_recount_export_e4_v01.py --e4 o_e4.json --compare-e4 cmp_e4.json --matched matched.json --punish-num 3 --out A_RECOUNT_E4.json
A level that is not complete (compare_e4 'complete' false) gets no values; E4.L.completed / E4.H.completed say which.
"""
import argparse
import datetime
import hashlib
import json
import math
import statistics
from pathlib import Path

ARMS = {'F0': 'E_F0', 'N': 'E_N', 'F0IMM': 'E_F0_IMM', 'NIMM': 'E_N_IMM'}
MATCH_KEY = {'N': 'N', 'F0IMM': 'F0_IMM', 'NIMM': 'N_IMM'}      # key of the arm in the matched recount's levels_out[lev]['arms']
CMP_ARMS = ('N', 'NIMM')
LEVS = ('lo', 'hi')
DESC = (('d_vimp', 'impact_speed_mps'), ('d_restgap', 'rest_gap_m'), ('d_peakdec', 'peak_decel_mps2'),
        ('d_jerk', 'rms_jerk_mps3'), ('d_fallback', 'fallback_share'))


def rj(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def clean(x):
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    if isinstance(x, (list, tuple)):
        return None if any(clean(v) is None for v in x) else [clean(v) for v in x]
    return x


def of_record(rows):
    d = {}
    for r in sorted((r for r in rows if r.get('valid')), key=lambda r: r['run_id']):
        d[(r.get('arm'), r.get('level'), r.get('case'))] = r
    return list(d.values())


def mean(v):
    return sum(v) / len(v) if v else None


def median(v):
    return float(statistics.median(v)) if v else None


def defined(rows, key):
    return [float(r[key]) for r in rows if r.get(key) is not None]


def arm_summary(rows, pre, V):
    if not rows:
        for s in ('contact', 'vimp', 'tlost', 'restgap', 'peakdec', 'jerk', 'fallback', 'masked'):
            V[pre + '.' + s] = None
        return
    V[pre + '.contact'] = sum(1 for r in rows if r.get('contact')) / len(rows)
    V[pre + '.vimp'] = median(defined(rows, 'impact_speed_mps'))
    V[pre + '.tlost'] = mean(defined(rows, 'time_lost_s'))
    V[pre + '.restgap'] = mean(defined(rows, 'rest_gap_m'))
    V[pre + '.peakdec'] = median(defined(rows, 'peak_decel_mps2'))
    V[pre + '.jerk'] = median(defined(rows, 'rms_jerk_mps3'))
    num = den = 0
    for r in rows:
        n = r.get('n_assessment_decisions')
        s = r.get('fallback_share')
        if n and s is not None:
            num += int(round(s * n))
            den += int(n)
    V[pre + '.fallback'] = (num / den) if den else None
    V[pre + '.masked'] = mean(defined(rows, 'masked_share'))


def four(c, pre, V, with_desc):
    """dc, dc.ci, dt, dt.ci (and the descriptive differences) from one compare_pair record; None where undefined."""
    ok = c is not None and c.get('pairs', 0) > 0 and 'contact_diff' in c
    V[pre + '.dc'] = c['contact_diff'] if ok else None
    V[pre + '.dc.ci'] = [c['contact_diff_lo'], c['contact_diff_hi']] if ok else None
    V[pre + '.dt'] = c.get('time_lost_diff') if ok else None
    lo = c.get('time_lost_lo') if ok else None
    hi = c.get('time_lost_hi') if ok else None
    V[pre + '.dt.ci'] = [lo, hi] if lo is not None and hi is not None else None
    if with_desc:
        oc = c.get('outcomes', {}) if ok else {}
        for name, key in DESC:
            o = oc.get(key)
            V[pre + '.' + name] = o.get('mean_diff') if o else None
            V[pre + '.' + name + '.ci'] = [o['ci_lo'], o['ci_hi']] if o and o.get('ci_lo') is not None and o.get('ci_hi') is not None else None


def find(comps, **kw):
    for c in comps:
        if all(c.get(k) == v for k, v in kw.items()):
            return c
    return None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--e4', required=True)
    p.add_argument('--compare-e4', required=True)
    p.add_argument('--matched', required=True)
    p.add_argument('--punish-num', type=int, required=True)
    p.add_argument('--status', default='ran')
    p.add_argument('--lock', default=None, help='default: revision_v13\\LOCK_A11b.txt if it exists')
    p.add_argument('--out', required=True)
    a = p.parse_args(argv)
    me = Path(__file__).resolve()
    lock = Path(a.lock) if a.lock else me.parents[3] / 'LOCK_A11b.txt'
    lock_sha = hashlib.sha256(lock.read_bytes()).hexdigest() if lock.exists() else None

    e4 = of_record(rj(a.e4)['runs'])
    cmp_ = rj(a.compare_e4)
    mt = rj(a.matched)['levels_out']
    done = {lev: bool(cmp_['levels'].get(lev, {}).get('complete')) for lev in LEVS}
    V = {'E4.status': a.status, 'E4.punish_num': a.punish_num, 'E4.n_cases': len({r['case'] for r in e4}),
         'E4.L.completed': done['lo'], 'E4.H.completed': done['hi']}
    for lev in LEVS:
        if not done[lev]:
            continue
        for short, arm in ARMS.items():
            pre = 'E4.%s.%s' % (short, lev)
            arm_summary([r for r in e4 if r.get('arm') == arm and r.get('level') == lev], pre, V)
            lv = mt.get(lev) or {}
            if short == 'F0':
                V[pre + '.caution'] = lv.get('F0_caution_at_gL')
            else:
                d = (lv.get('arms') or {}).get(MATCH_KEY[short])
                V[pre + '.caution'] = d.get('caution') if d else None
            ref = 'E_F0' if short in ('N', 'F0') else 'E_F0_IMM'
            if short in CMP_ARMS:
                c = find(cmp_['comparisons'], set='E4', arm=arm, level=lev)
                four(c, pre, V, True)
                V[pre + '.class'] = c.get('classification') if c else None
            c = find(cmp_['deg'], set='E4deg', arm=arm, level=lev)
            d = {}
            four(c, 'E4.deg.%s.%s' % (short, lev), d, False)
            V.update(d)
        for short in CMP_ARMS:
            r = find(cmp_['did'], set='E4did', arm=ARMS[short], level=lev)
            pre = 'E4.did.%s.%s' % (short, lev)
            V[pre + '.dc'] = r.get('dc') if r else None
            V[pre + '.dc.ci'] = [r['ci_lo'], r['ci_hi']] if r and r.get('ci_lo') is not None and r.get('ci_hi') is not None else None
    if done['lo']:
        V['E4H1'] = V.get('E4.N.lo.class')
        V['E4H2'] = V.get('E4.NIMM.lo.class')
    out = dict(package='E', set='E4', written=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), program=me.name,
               program_sha256=hashlib.sha256(me.read_bytes()).hexdigest(), lock_sha256=lock_sha,
               values={k: clean(V[k]) for k in V})
    Path(a.out).write_text(json.dumps(out, indent=1), encoding='utf-8')
    print('wrote %s: %d keys (L completed %s, H completed %s)' % (a.out, len(V), done['lo'], done['hi']))


if __name__ == '__main__':
    main()
