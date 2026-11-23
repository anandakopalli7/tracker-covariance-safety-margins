"""e_recount_e6_v01.py - second program for set E6 (closed-loop caution frontier under detection dropouts, A13 E6). Written from
E_A13_E6_v01.md and the raw files; the first program was not read. Reuses e_recount_e5_v01.py (which loads e_recount_v04.py and
e_recount_export_e4_v01.py) by import. Python 3.12 + numpy.

  main <runs_dir> --settings S --out-outcomes X --out-compare Y --export Z [--masks-table T] [--no-lock-check] [--status ran]

Arm labels from (arm, prefix, g): e5 E_N -> N; e5 E_F0 -> F0D4; e6 E_F0 g=8 -> F0D8; e6 E_F0 g=16 -> F0D16. Runs are paired by case and
label, never by the job's level label. Refuses to overwrite an output file and (unless --no-lock-check) to run without LOCK_A13a.txt.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E_DIR = HERE.parent
LOCK = HERE.parents[2] / 'LOCK_A13a.txt'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


E5 = sys.modules.get('e_recount_e5_v01') or _load('e_recount_e5_v01', HERE / 'e_recount_e5_v01.py')
R = E5.R
X4 = E5.X4

LABELS = ('N', 'F0D4', 'F0D8', 'F0D16')
LOCKED_G = {'F0D4': 4.0, 'F0D8': 8.0, 'F0D16': 16.0}
BOOT_SEED = 20261922
BOOT_N = 20000
MASKS5 = E5.MASKS5
ST_EMPTY = 'no common no-contact case'
ST_NONMONO = 'non-monotone'
ST_NOTBR = 'not bracketed'
ST_48 = 'bracketed 4-8'
ST_816 = 'bracketed 8-16'


def close(x, y):
    return x is not None and y is not None and abs(float(x) - float(y)) <= 1e-9 * max(1.0, abs(float(y)))


# ----------------------------------------------------------------------------- labels and validity
def label_of(prefix, row):
    arm = row.get('arm')
    if prefix == 'e5_':
        return {'E_N': 'N', 'E_F0': 'F0D4'}.get(arm)
    if prefix == 'e6_' and arm == 'E_F0':
        g = row.get('g')
        for lab in ('F0D8', 'F0D16'):
            if close(g, LOCKED_G[lab]) and g is not None:
                return lab
    return None


def labelled_rows(runs_dir, masks_table, g_N):
    """All e5_ and e6_ runs of record with the arm label and the locked-g validity rule applied."""
    out = []
    for prefix in ('e5_', 'e6_'):
        for r in E5.e5_outcomes(runs_dir, prefix, masks_table, None):
            r['prefix'] = prefix
            lab = label_of(prefix, r)
            r['label'] = lab
            if lab is not None and r.get('valid'):
                want = g_N if lab == 'N' else LOCKED_G[lab]
                if not close(r.get('g'), want):
                    r['valid'] = False
                    r['invalid_reasons'] = list(r.get('invalid_reasons') or []) + ['g_%r_not_locked_%r_for_%s' % (r.get('g'), want, lab)]
            out.append(r)
    return out


def by_label(rows, notes=None):
    """{label: {case: row}} over valid runs with a label (last run_id in sorted order wins, as the E5 recount)."""
    d = {lab: {} for lab in LABELS}
    for r in sorted((r for r in rows if r.get('valid') and r.get('label') in d), key=lambda r: r['run_id']):
        if notes is not None and r['case'] in d[r['label']]:
            notes.append('duplicate valid run for %s case %s: using %s over %s' % (r['label'], r['case'], r['run_id'], d[r['label']][r['case']]['run_id']))
        d[r['label']][r['case']] = r
    return d


# ----------------------------------------------------------------------------- the estimator (E6.5)
def point_delta(c, t):
    """c, t: length-4 sequences (N, F0D4, F0D8, F0D16) of c_a and t_a (t may be None/NaN when T is empty).
    Returns (bracket, c_F0_at_tN, delta); the last two None unless bracketed."""
    if any(x is None or (isinstance(x, float) and math.isnan(x)) for x in t):
        return ST_EMPTY, None, None
    tN, t4, t8, t16 = (float(x) for x in t)
    if not (t4 < t8 < t16):
        return ST_NONMONO, None, None
    if tN < t4 or tN > t16:
        return ST_NOTBR, None, None
    cN, c4, c8, c16 = (float(x) for x in c)
    if tN <= t8:
        lo_t, hi_t, lo_c, hi_c, st = t4, t8, c4, c8, ST_48
    else:
        lo_t, hi_t, lo_c, hi_c, st = t8, t16, c8, c16, ST_816
    w = (tN - lo_t) / (hi_t - lo_t)
    cF = lo_c + w * (hi_c - lo_c)
    return st, cF, cN - cF


def delta_vec(c, t):
    """Vector form of point_delta over resamples: c (B,4), t (B,4) with NaN t where no drawn case is in T. NaN where undefined."""
    with np.errstate(invalid='ignore', divide='ignore'):
        tN, t4, t8, t16 = t[:, 0], t[:, 1], t[:, 2], t[:, 3]
        ok = ~np.isnan(t).any(axis=1) & (t4 < t8) & (t8 < t16) & (tN >= t4) & (tN <= t16)
        first = tN <= t8
        lo_t = np.where(first, t4, t8)
        hi_t = np.where(first, t8, t16)
        lo_c = np.where(first, c[:, 1], c[:, 2])
        hi_c = np.where(first, c[:, 2], c[:, 3])
        w = (tN - lo_t) / (hi_t - lo_t)
        cF = lo_c + w * (hi_c - lo_c)
        d = c[:, 0] - cF
    return np.where(ok, d, np.nan)


def primary_from_arrays(C, TL, inT, idx):
    """C (n,4) contact 0/1, TL (n,4) time lost (anything where not inT), inT (n,) bool, idx (B,n) resample index matrix (K sorted).
    Returns the primary dict."""
    n = C.shape[0]
    B = idx.shape[0]
    nT = int(inT.sum())
    c = [float(np.mean(C[:, a])) if n else None for a in range(4)]
    t = [float(np.mean(TL[inT, a])) if nT else None for a in range(4)]
    st, cF, delta = point_delta(c, t) if n else (ST_EMPTY, None, None)
    if n == 0:
        dstar = np.full(B, np.nan)
    else:
        cs = np.stack([C[:, a][idx].mean(axis=1) for a in range(4)], axis=1)
        w = inT[idx]
        cnt = w.sum(axis=1)
        with np.errstate(invalid='ignore', divide='ignore'):
            ts = np.stack([np.where(w, TL[:, a][idx], 0.0).sum(axis=1) / cnt for a in range(4)], axis=1)
        ts[cnt == 0, :] = np.nan
        dstar = delta_vec(cs, ts)
    fin = dstar[~np.isnan(dstar)]
    p_one = (1 + int(np.sum(np.isnan(dstar) | (dstar >= 0)))) / (B + 1)
    ub95 = float(np.quantile(fin, 0.95)) if fin.size else None
    ci = [float(np.quantile(fin, 0.025)), float(np.quantile(fin, 0.975))] if fin.size else None
    bracketed = st in (ST_48, ST_816)
    return dict(n_cases=n, n_nocontact_all=nT, c=c, t=t, bracket=st, c_F0_at_tN=cF, delta=delta, ub95=ub95, ci=ci,
                finite_share=float(fin.size / B), p_one=float(p_one), pass_alone=bool(bracketed and ub95 is not None and ub95 < 0))


def primary(arms):
    """arms {label: {case: valid row}}. K = cases valid in all four, sorted by case id string; T = K cases with no contact in any."""
    K = sorted(set(arms['N']) & set(arms['F0D4']) & set(arms['F0D8']) & set(arms['F0D16']))
    n = len(K)
    C = np.array([[float(arms[l][k]['contact']) for l in LABELS] for k in K], dtype=float).reshape(n, 4)
    inT = np.array([all(not arms[l][k]['contact'] for l in LABELS) for k in K], dtype=bool)
    TL = np.zeros((n, 4))
    for i, k in enumerate(K):
        if inT[i]:
            for j, l in enumerate(LABELS):
                v = arms[l][k].get('time_lost_s')
                if v is None or (isinstance(v, float) and math.isnan(v)):
                    raise SystemExit('FAILED: no-contact run %s %s has undefined time_lost_s' % (l, k))
                TL[i, j] = float(v)
    idx = np.random.default_rng(BOOT_SEED).integers(0, n, (BOOT_N, n)) if n else np.zeros((BOOT_N, 0), dtype=np.int64)
    res = primary_from_arrays(C, TL, inT, idx)
    res['K'] = K
    return res


# ----------------------------------------------------------------------------- export
def build_values(arms, prim, comps, status):
    V = {'E6.status': status, 'E6.n_cases': prim['n_cases'], 'E6.n_nocontact_all': prim['n_nocontact_all']}
    for j, l in enumerate(LABELS):
        V['E6.pt.%s.c' % l] = prim['c'][j]
        V['E6.pt.%s.t' % l] = prim['t'][j]
    V['E6.bracket'] = prim['bracket']
    V['E6.c_F0_at_tN'] = prim['c_F0_at_tN']
    V['E6.delta'] = prim['delta']
    V['E6.delta.ub95'] = prim['ub95']
    V['E6.delta.ci'] = prim['ci']
    V['E6.finite_share'] = prim['finite_share']
    V['E6.p_one'] = prim['p_one']
    V['E6.pass_alone'] = prim['pass_alone']
    for l in LABELS:
        X4.arm_summary(list(arms[l].values()), 'E6.' + l, V)
    for s, c in comps.items():
        pre = 'E6.s%d' % s
        X4.four(c, pre, V, False)
        V[pre + '.mcnemar_p'] = c.get('mcnemar_p') if c.get('pairs', 0) > 0 else None
        V[pre + '.class'] = c.get('classification')
        V[pre + '.pairs'] = c.get('pairs', 0)
    return V


def jsonable(x):
    if isinstance(x, (np.floating,)):
        x = float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return X4.clean(x)


def cmd_main(a):
    outs = [Path(a.out_outcomes), Path(a.out_compare), Path(a.export)]
    for o in outs:
        if o.exists():
            raise SystemExit('REFUSED: output exists, will not overwrite: %s' % o)
    if not a.no_lock_check and not LOCK.exists():
        raise SystemExit('REFUSED: %s does not exist (lock gate)' % LOCK)
    st = R.read_json(a.settings)
    st = st.get('settings', st) if isinstance(st.get('settings', None), dict) else st
    g_N = st.get('g_N')
    if g_N is None:
        raise SystemExit('FAILED: settings has no g_N')
    g_N = float(g_N)
    rows = labelled_rows(a.runs_dir, a.masks_table, g_N)
    R.write_json(dict(schema='E6_RECOUNT_OUTCOMES_v01', runs_dir=str(a.runs_dir), n_runs=len(rows), runs=rows), a.out_outcomes)
    notes = []
    arms = by_label(rows, notes)
    prim = primary(arms)
    comps = {}
    for s, lab in ((8, 'F0D8'), (16, 'F0D16')):
        comps[s] = R.compare_pair(arms['N'], arms[lab], 'N vs %s (E6)' % lab,
                                  dict(set='E6', arm='N', reference=lab, level=None, hypothesis='E6-s%d' % s))
    R.write_json(dict(schema='E6_RECOUNT_COMPARE_v01', primary=prim, secondary={str(s): c for s, c in comps.items()}, notes=notes,
                      n_runs=len(rows), n_valid=sum(1 for r in rows if r.get('valid')),
                      n_valid_by_label={l: len(arms[l]) for l in LABELS}), a.out_compare)
    V = build_values(arms, prim, comps, a.status)
    keys = R.read_json(KEYS_FILE)['keys'] if Path(KEYS_FILE).exists() else None
    if keys is not None and sorted(keys) != sorted(V):
        raise SystemExit('FAILED: export keys differ from E6_EXPORT_KEYS_v01.json: %s' % sorted(set(keys) ^ set(V)))
    me = Path(__file__).resolve()
    out = dict(package='E', set='E6', written=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), program=me.name,
               program_sha256=hashlib.sha256(me.read_bytes()).hexdigest(), values={k: jsonable(V[k]) for k in V})
    Path(a.export).write_text(json.dumps(out, indent=1, allow_nan=False), encoding='utf-8')
    print('wrote %s: %d keys; n=%d, T=%d, %s, delta %s, p_one %s' % (a.export, len(V), prim['n_cases'], prim['n_nocontact_all'],
                                                                   prim['bracket'], prim['delta'], prim['p_one']))


KEYS_FILE = E_DIR / 'tests' / 'out' / 'E6_EXPORT_KEYS_v01.json'


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('cmd', choices=['main'])
    p.add_argument('runs_dir')
    p.add_argument('--settings', required=True)
    p.add_argument('--out-outcomes', required=True)
    p.add_argument('--out-compare', required=True)
    p.add_argument('--export', required=True)
    p.add_argument('--masks-table', default=str(MASKS5), help='locked E5_MASKS_v01.json; none = no check (tests)')
    p.add_argument('--no-lock-check', action='store_true', help='synthetic tests only')
    p.add_argument('--status', default='ran')
    a = p.parse_args(argv)
    cmd_main(a)


if __name__ == '__main__':
    main()
