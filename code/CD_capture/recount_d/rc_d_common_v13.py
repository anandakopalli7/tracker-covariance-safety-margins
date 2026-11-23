"""Recount (second program) for package D of revision v13: shared helpers. Claude Fable 5.2, 19 Nov 2026.
Written from AMENDMENT_10_v13.md (sec. 0, 2, 5.5, 6, 10.1) and work\\CD_capture\\CD_DEFINITIONS_v13.md, WITHOUT reading the first
programs (work\\CD_capture\\analysis\\). Imports, read-only: optA_lib_v02 (scoring library of record) and v11's rev_common_v01
(loader of the 35 old evaluation runs). Writes only into recount_d\\out\\ and never overwrites.

Sealing: fresh-run arrays, runs and archives are read only if LOCK_A10_2.txt exists (require_lock()).
"""
import json, pathlib, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
CD = HERE.parent                                   # work\CD_capture
ROOT = CD.parent.parent                            # revision_v13
LOCK2 = ROOT / 'LOCK_A10_2.txt'
ARRAYS = CD / 'arrays'
OUT = HERE / 'out'
V11 = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis')
V12OUT = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out')
OLD_ARCH = pathlib.Path(r'<library folder>\archives')
CASES_C = CD / 'CASES_C_v13.json'
CASES_D1 = CD / 'd1' / 'CASES_D1_v13.json'

sys.path.insert(0, str(V11))
import rev_common_v01 as C                         # noqa: E402  (v11 loader; imports optA_lib_v02)
L = C.L
GRID = C.GRID
I_G1 = int(np.argmin(np.abs(GRID - 1.0)))
assert GRID[I_G1] == 1.0 and GRID.size == 202

NBOOT = 20000
SEED_BOOT = 20261911


def require_lock():
    """Fresh runs are sealed until Lock 2."""
    if not LOCK2.exists():
        raise SystemExit('REFUSED: %s does not exist; fresh runs are sealed (use --test-old)' % LOCK2)


def write_once(path, doc):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, 'x', encoding='utf-8') as f:
            f.write(json.dumps(doc, indent=1, default=float, allow_nan=True))
    except FileExistsError:
        raise SystemExit('REFUSED: %s exists (never overwritten; pass another --tag)' % path)


def clock():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def est_phase(vhat, ahat_long, lead_found, thr=-1.0):
    """A10 sec. 2.4 (re-implemented): 2 = stopped (lead track, speed <= 0.5); 1 = braking (lead track, speed > 0.5, acceleration
    along its velocity finite and <= thr); 0 otherwise or with no lead track."""
    v = np.asarray(vhat, float); a = np.asarray(ahat_long, float); f = np.asarray(lead_found).astype(bool)
    out = np.zeros(v.shape, np.int64)
    with np.errstate(invalid='ignore'):
        out[f & (v > 0.5) & np.isfinite(a) & (a <= thr)] = 1
        out[f & (v <= 0.5)] = 2
    return out


def _des(x):
    d = np.asarray(x, float)
    return float(d.reshape(-1)[0]) if d.size == 1 else d


def old_runs():
    """The 35 old evaluation runs in the array format used below (exploratory data of record)."""
    runs = []
    for r in C.load_runs():
        ld = np.load(V12OUT / 'lead' / (r['run'] + '.npz'), allow_pickle=False)
        tg = np.load(V12OUT / 'tg' / (r['run'] + '.npz'), allow_pickle=False)
        if not (np.array_equal(ld['k'], r['k']) and np.array_equal(tg['k'], r['k'])):
            raise RuntimeError('REFUSED %s: decision ticks of the lead / TG arrays differ' % r['run'])
        cr = r['crit']
        runs.append(dict(run=r['run'], k=np.asarray(r['k']), ev=r['ev'].astype(bool), des=float(r['desired']),
                         clear1=r['clear1'], vbar=r['vbar'], idx55=r['idx55'],
                         crit={'F0': cr['F0'], 'N': cr['N'], 'NA': cr['NA'], 'AM': cr['A1'], 'CK3': cr['CK3'], 'Q': cr['Q'],
                               'TG': tg['cTG2']},
                         vhat=ld['vhat'], ahat_long=ld['ahat_long'], lead_found=ld['lead_found'].astype(bool),
                         cache=r['cache']))
    return runs


def fresh_run(rid, need_tg=True, need_rs=False, variant_kind='__any__'):
    """One fresh run from arrays\\CV0\\<rid>.npz (after Lock 2 only)."""
    require_lock()
    z = np.load(ARRAYS / 'CV0' / (rid + '.npz'), allow_pickle=False)
    meta = json.loads(str(z['meta']))
    if meta.get('run_id') != rid:
        raise RuntimeError('REFUSED %s: meta run_id is %r' % (rid, meta.get('run_id')))
    lv = meta.get('lead_variant')
    kind = lv.get('kind') if isinstance(lv, dict) else lv
    if variant_kind != '__any__' and kind != variant_kind:
        raise RuntimeError('REFUSED %s: lead_variant %r, expected %r' % (rid, kind, variant_kind))
    d = dict(run=rid, case=meta.get('case'), family=meta.get('family'), k=z['k'], ev=(z['evaluated'] == 1), des=_des(z['des']),
             clear1=L.clean_clear(z['clear']), vbar=z['vbar'], idx55=z['idx55'],
             crit={'F0': z['cF0'], 'N': z['cN'], 'NA': z['cNA'], 'AM': z['cA1'], 'CK3': z['cCK3'], 'Q': z['cQ']},
             vhat=z['vhat'], ahat_long=z['ahat_long'], lead_found=z['lead_found'].astype(bool))
    if need_tg:
        d['crit']['TG'] = z['cTG2']
    if need_rs:
        d['clearR'] = L.clean_clear(z['clearR075'])
    return d


def cases_c_lead():
    """(run id, case) of C lead braking: pc13_<case>_native for the lead_braking rows of CASES_C_v13.json (file order)."""
    doc = json.loads(CASES_C.read_text(encoding='utf-8'))
    rows = [x for x in doc['cases'] if x['family'] == 'lead_braking']
    if any(x.get('lead_variant') for x in rows):
        raise RuntimeError('REFUSED: a C lead-braking case has a lead_variant')
    return [('pc13_%s_native' % x['case'], x['case']) for x in rows]


def cases_d1():
    """({kind: [run ids]}, file_order_is_sorted) for the d1_openloop rows of CASES_D1_v13.json; run id pd13_<case id>_native,
    returned in ascending run-id order."""
    doc = json.loads(CASES_D1.read_text(encoding='utf-8'))
    out = {}; order_ok = True
    for x in doc['cases']:
        if x.get('role') != 'd1_openloop':
            continue
        out.setdefault(x['lead_variant']['kind'], []).append('pd13_%s_native' % (x.get('case') or x['id']))
    for kd in out:
        order_ok = order_ok and (out[kd] == sorted(out[kd]))
        out[kd] = sorted(out[kd])
    return out, order_ok


def run_table(r, sel, safe_x):
    """Summed statistics (G, NST) of one run over its evaluated decisions for selections sel (G, n). Caution by the 3 s commitment
    (clear1), wrong go by safe_x (the scoring's safe set)."""
    return L.stats_scored(sel, r['clear1'], safe_x, r['vbar'], r['des'], (r['ev'],))[:, 0, :]


def grid_sel(r, src):
    return L.select_grid(r['crit'][src], GRID, r['idx55'])


def pct(b):
    b = np.asarray(b, float); f = np.isfinite(b)
    return [float(x) for x in np.percentile(b[f], [2.5, 97.5])] if f.any() else [float('nan'), float('nan')]
