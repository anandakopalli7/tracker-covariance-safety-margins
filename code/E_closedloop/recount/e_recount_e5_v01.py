"""e_recount_e5_v01.py - second program for set E5 (caution-matched closed-loop dropout test, A12 6). Written from
E_A12_6_v01.md and the raw files; the first program was not read. Reuses e_recount_v04.py (outcomes, mask law, validity,
compare_pair) and e_recount_export_e4_v01.py (summaries) by import. Python 3.12 + numpy.

  cal   <runs_dir> --out X                          calibration shares and g_D from the e5c_ runs
  match --out X [--arrays-dir D]                    g_N for each g_D in {4, 8, 16, 32} from F's masked open-loop arrays
  main  <runs_dir> --settings S --cal CAL.json --match MATCH.json --out-outcomes X --out-compare Y --export A_RECOUNT_E5.json
"""
import argparse
import datetime
import glob
from fractions import Fraction
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E_DIR = HERE.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


R = _load('e_recount_v04', HERE / 'e_recount_v04.py')
X4 = _load('e_recount_export_e4_v01', HERE / 'e_recount_export_e4_v01.py')

GS = (4, 8, 16, 32)
TARGET = 0.20
ARR_DIR = r'ARS_TRIAL\revision_v13\work\F_dropout\out\arrays\DR'
MASKS5 = E_DIR / 'out' / 'E5_MASKS_v01.json'
PBAR_DR_SHA = '4b373f6e3863028049425bed0aa2eb68a4d1e7bdd2ab8269f2edfb6ff2127560'   # P-bar_DR in packet v05


# ----------------------------------------------------------------------------- outcomes with the dropout validity
class _Shim:
    """The three attributes check_dropout reads, without loading frames and truth."""

    def __init__(self, run_dir):
        self.summary = R.read_json(Path(run_dir) / 'SUMMARY.json')
        self.case = self.summary.get('case')
        self.cap = R.capture_dir(Path(run_dir), self.case)
        self.arm_method = R.read_json(self.cap / 'ARM_METHOD_v01.json') if self.cap is not None and (self.cap / 'ARM_METHOD_v01.json').exists() else None


def identity_reasons(shim, job, want_g):
    """Per-run identity: tracker CANMOT; arm = the job's arm (SUMMARY and job id) and E_F0 or E_N; knobs.g = the job's g (SUMMARY
    e_job.g) and, if want_g is given, the setting's g for the arm; P-bar_DR hash for E_F0."""
    am = shim.arm_method or {}
    s = shim.summary
    why = []
    if am.get('tracker') != 'CANMOT':
        why.append('tracker_%r_not_CANMOT' % (am.get('tracker'),))
    arm = am.get('arm')
    if arm not in ('E_F0', 'E_N'):
        why.append('arm_%r_not_E_F0_or_E_N' % (arm,))
    if arm != s.get('arm'):
        why.append('arm_%r_differs_from_summary_arm_%r' % (arm, s.get('arm')))
    m = re.search(r'_(e_f0|e_n)(?:_g\d+(?:p\d+)?)?$', re.sub(r'__r\d+$', '', job))
    jarm = {'e_f0': 'E_F0', 'e_n': 'E_N'}.get(m.group(1)) if m else None
    if jarm != arm:
        why.append('arm_%r_differs_from_job_id_arm_%r' % (arm, jarm))
    g = (am.get('knobs') or {}).get('g')
    jg = (s.get('e_job') or {}).get('g')
    tol = lambda x, y: x is not None and y is not None and abs(float(x) - float(y)) <= 1e-9 * max(1.0, abs(float(y)))
    if not tol(g, jg):
        why.append('knobs_g_%r_differs_from_job_g_%r' % (g, jg))
    if want_g is not None and arm in want_g and want_g[arm] is not None and not tol(g, want_g[arm]):
        why.append('knobs_g_%r_differs_from_setting_%r' % (g, want_g[arm]))
    if arm == 'E_F0' and am.get('pbar_sha256') != PBAR_DR_SHA:
        why.append('pbar_sha256_%r_not_P-bar_DR' % (am.get('pbar_sha256'),))
    return why


def e5_outcomes(runs_dir, prefix, masks_table, want_g=None):
    R.PUNISH_NUM = 3
    if masks_table.lower() != 'none':
        R.load_masks_table(masks_table)
    else:
        R.MASKS_TABLE = None
    recs = R.runs_of_record(runs_dir, prefix)
    rows = []
    for b in sorted(recs):
        try:
            row = R.run_outcome(recs[b])
            shim = _Shim(recs[b])
            dr, ms, info = R.check_dropout(shim, 3)
            dr = dr + identity_reasons(shim, b, want_g)
            row['masked_share'] = ms
            if dr:
                row['invalid_reasons'] = list(row.get('invalid_reasons') or []) + dr
                row['valid'] = False
            if info and info['n_distinct_ticks'] != info['n_updates']:
                row.setdefault('warnings', []).append('detection rows: %d distinct ticks, n_updates %d' % (info['n_distinct_ticks'], info['n_updates']))
            rows.append(row)
        except Exception as e:
            rows.append(dict(run_id=recs[b].name, job=b, valid=False, invalid_reasons=['read_error:%r' % (e,)]))
    return rows


# ----------------------------------------------------------------------------- cal
def g_of(row):
    m = re.search(r'_g(\d+(?:p\d+)?)$', re.sub(r'__r\d+$', '', row.get('job') or row['run_id']))
    return float(m.group(1).replace('p', '.')) if m else row.get('g')


def pick_g_D(counts):
    """counts {g: (contacts, n)}. Distance |contacts/n - 1/5| = |5 contacts - n| / (5 n) as exact Fractions; the first minimum over
    g ascending (ties to the smaller g). Every share < 0.05 (exactly: 20 contacts < n) -> g = 4, low power."""
    counts = {g: (c, n) for g, (c, n) in counts.items() if n}
    if not counts:
        return None, None
    if all(Fraction(c, n) < Fraction(1, 20) for c, n in counts.values()):
        return 4, True
    best = min(sorted(counts), key=lambda g: abs(Fraction(5 * counts[g][0] - counts[g][1], 5 * counts[g][1])))
    return best, False


def cmd_cal(a):
    rows = e5_outcomes(a.runs_dir, 'e5c_', a.masks_table)
    per = {}
    for r in rows:
        g = g_of(r)
        d = per.setdefault(g, dict(g=g, n_runs=0, n_valid=0, contacts=0))
        d['n_runs'] += 1
        if r.get('valid'):
            d['n_valid'] += 1
            d['contacts'] += int(bool(r.get('contact')))
    for d in per.values():
        d['share'] = d['contacts'] / d['n_valid'] if d['n_valid'] else None
    shares = {g: d['share'] for g, d in per.items() if d['share'] is not None}
    g_D, low = pick_g_D({g: (d['contacts'], d['n_valid']) for g, d in per.items() if g is not None})
    out = dict(schema='E5_RECOUNT_CAL_v01', runs_dir=str(a.runs_dir), per_g=[per[g] for g in sorted(per, key=lambda x: (x is None, x))],
               g_D=g_D, low_power=low, runs=rows)
    R.write_json(out, a.out)
    print('wrote %s: shares %s, g_D %s, low_power %s' % (a.out, {g: (None if v is None else round(v, 4)) for g, v in sorted(shares.items())}, g_D, low))


# ----------------------------------------------------------------------------- match
def cmd_match(a):
    rc, _ = None, None
    spec = importlib.util.spec_from_file_location('rev_common_v01', R.RUNS_V11)
    sys.path.insert(0, str(Path(R.RUNS_V11).parent))
    rc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rc)
    L = rc.L
    grid = np.concatenate([[0.], np.logspace(-2, 3, 201)])
    assert np.array_equal(grid, rc.GRID), 'grid of record differs from [0] + logspace(-2, 3, 201)'
    gD = np.array([float(g) for g in GS])
    files = sorted(glob.glob(str(Path(a.arrays_dir) / '*.npz')))
    TN = TF = None
    for f in files:
        z = np.load(f, allow_pickle=False)
        m = json.loads(str(z['meta']))
        ev = z['evaluated'].astype(bool)
        clear1 = L.clean_clear(z['clear'])
        safe = clear1 > 0.
        idx55 = z['idx55']
        desired = float(m['desired'])
        for crit, grd, which in ((z['cN'], grid, 'N'), (z['cF0'], gD, 'F')):
            sel = L.select_grid(crit, grd, idx55)
            st = L.stats_scored(sel, clear1, safe, z['vbar'], desired, (ev,))[:, 0, :]
            if which == 'N':
                TN = st if TN is None else TN + st
            else:
                TF = st if TF is None else TF + st
    cN = L.rates(TN)[1]
    cF = L.rates(TF)[1]
    rows = []
    for j, g in enumerate(GS):
        i = int(np.argmin(np.abs(np.asarray(cN) - cF[j])))          # first minimum = the smaller scale
        rows.append(dict(g_D=g, caution_F0D=float(cF[j]), g_N=float(grid[i]), grid_index=i, caution_N=float(cN[i]),
                         caution_diff=float(cN[i] - cF[j])))      # SIGNED: caution_N - caution_F0D (pp)
    out = dict(schema='E5_RECOUNT_MATCH_v01', arrays_dir=str(a.arrays_dir), n_files=len(files), grid_size=len(grid), rows=rows)
    R.write_json(out, a.out)
    print('wrote %s: %d files' % (a.out, len(files)))
    for r in rows:
        print('  g_D %-3g caution_F0D %.6f  g_N %.10g (index %d)  caution_N %.6f  diff(N-F0D) %+.6f' % (
            r['g_D'], r['caution_F0D'], r['g_N'], r['grid_index'], r['caution_N'], r['caution_diff']))


# ----------------------------------------------------------------------------- main
def cmd_main(a):
    st0 = R.read_json(a.settings) if (a.settings and Path(a.settings).exists()) else {}
    st0 = st0.get('settings', st0) if isinstance(st0.get('settings', None), dict) else st0
    rows = e5_outcomes(a.runs_dir, 'e5_', a.masks_table, {'E_F0': st0.get('g_D'), 'E_N': st0.get('g_N')})
    R.write_json(dict(schema='E5_RECOUNT_OUTCOMES_v01', runs_dir=str(a.runs_dir), n_runs=len(rows), runs=rows), a.out_outcomes)
    # one level (A12 6.6): pair over all valid runs by case, whatever the job's level label ('D' in the real runs)
    notes = []
    odd = sorted({str(r.get('level')) for r in rows if r.get('level') not in (None, 'D')})
    if odd:
        raise SystemExit('FAILED: e5_ runs with a level label other than D or None: %s' % odd)
    arm_n, arm_f = {}, {}
    for r in sorted((r for r in rows if r.get('valid')), key=lambda r: r['run_id']):
        d = {'E_N': arm_n, 'E_F0': arm_f}.get(r.get('arm'))
        if d is None:
            continue
        if r['case'] in d:
            notes.append('duplicate valid run for %s case %s: using %s over %s' % (r['arm'], r['case'], r['run_id'], d[r['case']]['run_id']))
        d[r['case']] = r
    c = R.compare_pair(arm_n, arm_f, 'E_N vs E_F0 (E5)', dict(set='E5', arm='E_N', reference='E_F0', level=None, hypothesis='E5-H1'))
    cases = c['cases']
    p_one = None
    if len(cases) >= 1:
        d = np.array([float(arm_n[k]['contact']) - float(arm_f[k]['contact']) for k in cases])
        rng = np.random.default_rng(R.BOOT_SEED)
        ix = rng.integers(0, len(d), size=(R.BOOT_N, len(d)))
        p_one = float(np.mean(d[ix].mean(axis=1) >= 0.0))
    c['p_one'] = p_one
    cal = R.read_json(a.cal)
    mt = R.read_json(a.match)
    g_D = cal['g_D']
    row = next((r for r in mt['rows'] if r['g_D'] == g_D), None)
    chk = []
    close = lambda x, y: x is not None and y is not None and abs(float(x) - float(y)) <= 1e-9 * max(1.0, abs(float(y)))
    if not (a.settings and Path(a.settings).exists()):
        chk.append('settings file %s not found' % a.settings)
        st = {}
    else:
        st = R.read_json(a.settings)
        st = st.get('settings', st) if isinstance(st.get('settings', None), dict) else st
        if row is None:
            chk.append('no match row for g_D %r' % (g_D,))
        else:
            for key, mine in (('g_D', g_D), ('g_N', row['g_N']), ('g_N_index', row['grid_index']), ('caution_F0D_pct', row['caution_F0D']),
                              ('caution_N_pct', row['caution_N']), ('caution_diff_pp', row['caution_diff'])):
                if key not in st:
                    chk.append('settings has no %s' % key)
                elif not close(st[key], mine):
                    chk.append('settings %s %r differs from the recount %r' % (key, st[key], mine))
        if 'low_power' not in st or bool(st['low_power']) != bool(cal['low_power']):
            chk.append('settings low_power %r differs from the recount %r' % (st.get('low_power'), cal['low_power']))
        sh = st.get('shares') or {}
        for d_ in cal['per_g']:
            k = None if d_['g'] is None else str(float(d_['g']))
            if k not in sh:
                chk.append('settings has no share for g %s' % k)
            elif not close(sh[k], d_['share']):
                chk.append('settings share %s %r differs from the recount %r' % (k, sh[k], d_['share']))
    sg_D, sg_N = st.get('g_D'), st.get('g_N')
    for r in rows:
        g = r.get('g')
        want = (sg_D if r.get('arm') == 'E_F0' else sg_N)
        if want is not None and g is not None and not close(g, want):
            chk.append('run %s g %r differs from the setting %r' % (r['run_id'], g, want))
    for m in chk:
        print('SETTINGS CHECK FAILED:', m)
    R.write_json(dict(schema='E5_RECOUNT_COMPARE_v01', comparison=c, settings_check=chk, notes=notes,
                      n_runs=len(rows), n_valid=sum(1 for r in rows if r.get('valid'))), a.out_compare)

    # ---- export
    e5 = X4.of_record(rows)
    V = {'E5.status': a.status}
    for s in GS:
        sh = next((d['share'] for d in cal['per_g'] if d['g'] == s), None)
        V['E5.cal.g%d.contact' % s] = sh
    V['E5.g_D'] = g_D
    V['E5.low_power'] = cal['low_power']
    V['E5.g_N'] = row['g_N'] if row else None
    V['E5.caution_F0D'] = row['caution_F0D'] if row else None
    V['E5.caution_N'] = row['caution_N'] if row else None
    V['E5.caution_diff'] = row['caution_diff'] if row else None
    V['E5.n_cases'] = len({r['case'] for r in e5})
    for short, arm in (('F0D', 'E_F0'), ('N', 'E_N')):
        X4.arm_summary([r for r in e5 if r.get('arm') == arm], 'E5.' + short, V)
    X4.four(c, 'E5', V, True)
    V['E5.class'] = c.get('classification')
    V['E5.p_one'] = p_one
    V['E5.mcnemar_p'] = c.get('mcnemar_p') if c.get('pairs', 0) > 0 else None
    me = Path(__file__).resolve()
    out = dict(package='E', set='E5', written=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), program=me.name,
               program_sha256=hashlib.sha256(me.read_bytes()).hexdigest(), values={k: X4.clean(V[k]) for k in V})
    Path(a.export).write_text(json.dumps(out, indent=1), encoding='utf-8')
    print('wrote %s: %d keys; pairs %d, class %s, p_one %s' % (a.export, len(V), c.get('pairs', 0), c.get('classification'), p_one))
    if chk:
        raise SystemExit('FAILED: %d mismatch(es) between E5_SETTINGS and the recount / runs (see SETTINGS CHECK above)' % len(chk))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest='cmd', required=True)
    mk = lambda s: s.add_argument('--masks-table', default=str(MASKS5), help='locked E5_MASKS_v01.json; none = no check (tests)')
    s = sp.add_parser('cal')
    s.add_argument('runs_dir')
    s.add_argument('--out', required=True)
    mk(s)
    s.set_defaults(f=cmd_cal)
    s = sp.add_parser('match')
    s.add_argument('--out', required=True)
    s.add_argument('--arrays-dir', default=ARR_DIR)
    s.set_defaults(f=cmd_match)
    s = sp.add_parser('main')
    s.add_argument('runs_dir')
    s.add_argument('--settings', required=True)
    s.add_argument('--cal', required=True)
    s.add_argument('--match', required=True)
    s.add_argument('--out-outcomes', required=True)
    s.add_argument('--out-compare', required=True)
    s.add_argument('--export', required=True)
    s.add_argument('--status', default='ran')
    mk(s)
    s.set_defaults(f=cmd_main)
    a = p.parse_args(argv)
    a.f(a)


if __name__ == '__main__':
    main()
