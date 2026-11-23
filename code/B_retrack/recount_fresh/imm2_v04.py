"""Package B, v13 (A12 s3c): independent second program (recount) for IMM2's keys, on top of the frozen recount_fresh.py / rf_core.py
(imported, never edited), following the pattern of immr_v03.py.  Written from A12_3c_IMM2_v02.md and the raw inputs.
Usage (python -I -B -X utf8 imm2_v04.py ...):
  --test-old-as IMM [--K 2000]   this code path on the 35 old runs with the old B1 arrays; compares with B.IMM.* of out\\TESTOLD_A_RECOUNT_B.json
                                 and testold_boot_IMM.npz (ungated); outputs *_IMM2_as_IMM*
  --fresh [--K 20000]            105 fresh C runs, arrays B_retrack\\out\\retrack_fresh\\IMM2\\<rid>_arrays.npz; key prefix B.IMM2C.; gated
  --new --runs-root R [--K ..]   new lead-braking runs (CASES_L12_v13.json, reserve == False, REPLACEMENTS_L12_v13.json if present,
                                 ids pl12_<case>_native, ascending, only ids with R\\<rid>\\LOGS_OK); arrays B_retrack\\out\\retrack_new\\IMM2\\;
                                 key prefix B.IMM2N.; gated
  --combine                      adds only B.IMM2C.* and/or B.IMM2N.* keys to B_retrack\\out\\A_RECOUNT_B.json (refuses if an existing key would
                                 change; backup under a new name); gated
Gates: LOCK_A10_2.txt, LOCK_A10_2c.txt, LOCK_A11.txt and LOCK_A12a.txt all must exist (checked before any fresh/new file is touched).
Extra keys: p_one_sided = #{b: RR_b <= 0} / #{b: RR_b finite}, p_n_finite, RR_b = D_N / denE (finite iff denE > 0).
"""
import sys, os, json, argparse, hashlib, shutil, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import recount_fresh as RF

if sys.platform == 'win32':
    import ctypes
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)

V13 = RF.V13
BR = RF.BR
CD = RF.CD
OUTD = RF.OUTD
LOCKS4 = [RF.LOCK, RF.LOCK_C, V13 + r'\LOCK_A11.txt', V13 + r'\LOCK_A12a.txt']
SEED = 20261911
VARNAME = 'IMM2'
RF.VARS[VARNAME] = 'IMM2'     # fresh_path non-CV/IMM branch: BR\out\retrack_fresh\IMM2\<rid>_arrays.npz


def check_locks4():
    miss = [p for p in LOCKS4 if not os.path.exists(p)]
    if miss:
        raise SystemExit('REFUSED: fresh and new runs are sealed; missing ' + ', '.join(miss))
    return {os.path.basename(p): hashlib.sha256(open(p, 'rb').read()).hexdigest() for p in LOCKS4}


def new_run_ids(runs_root):
    d = json.load(open(CD + r'\l12\CASES_L12_v13.json'))
    cases = d['cases'] if isinstance(d, dict) else d
    base = [c['case'] for c in cases if c.get('reserve') is False]
    assert len(base) == 150, len(base)
    rep = {}
    rp = CD + r'\l12\REPLACEMENTS_L12_v13.json'
    if os.path.exists(rp):
        r = json.load(open(rp))
        rep = r['replacements'] if 'replacements' in r else r
        print('replacements applied to:', {k: v for k, v in rep.items() if k in base}, flush=True)
    else:
        print('NOTE: no REPLACEMENTS_L12_v13.json; none applied', flush=True)
    ids = sorted('pl12_%s_native' % rep.get(c, c) for c in base)
    assert len(set(ids)) == len(ids)
    kept = [i for i in ids if os.path.exists(runs_root + '\\' + i + '\\LOGS_OK')]
    print('new ids: %d listed, %d with LOGS_OK' % (len(ids), len(kept)), flush=True)
    return kept


def compute(mode, K, test_as=None, runs_root=None):
    orig_setup = RF.setup

    def setup(m):
        if m == 'old':
            names, pathf, nr, seed = orig_setup('old')
            return names, (lambda nm, run: RF.old_path(test_as, run)), nr, seed
        if m == 'fresh':
            return orig_setup('fresh')       # RF.check_locks inside; our four-lock check ran before
        if m == 'new':
            ids = new_run_ids(runs_root)
            f = lambda nm, rid: r'%s\out\retrack_new\IMM2\%s_arrays.npz' % (BR, rid)
            return ids, f, len(ids), SEED
        raise ValueError(m)
    RF.setup = setup
    try:
        res, out, sens = RF.per_variant(VARNAME, mode, K)
    finally:
        RF.setup = orig_setup
    den = out['denE']
    with np.errstate(divide='ignore', invalid='ignore'):
        rr = np.where(den > 0, out['D_N'] / den, np.nan)
    fin = np.isfinite(rr)
    res['p_one_sided'] = float(np.sum(rr[fin] <= 0) / fin.sum()) if fin.any() else float('nan')
    res['p_n_finite'] = int(fin.sum())
    return res, out, sens


def keyed(res, prefix):
    return {prefix + k: v for k, v in json.loads(json.dumps(res, default=float)).items()}


def run_set(kind, K, runs_root=None):
    sha = check_locks4()
    print('locks:', sha, flush=True)
    tag = 'IMM2C' if kind == 'fresh' else 'IMM2N'
    res, out, sens = compute(kind, K, runs_root=runs_root)
    sens['lock_sha256'] = sha
    os.makedirs(OUTD, exist_ok=True)
    np.savez(OUTD + r'\boot_%s.npz' % tag, **out)
    json.dump(dict(res=res, sens=sens), open(OUTD + r'\part_%s_%s.json' % (kind, tag), 'w'), indent=1, default=float)
    print(tag, 'written; p = %s over %d finite; total %.1fs' % (res['p_one_sided'], res['p_n_finite'], sens['total_seconds']), flush=True)


def same(a, b, tol=1e-9):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        if math.isnan(a) and math.isnan(b):
            return True
        return abs(a - b) <= tol * max(1.0, abs(b))
    return a == b


def _flat(v):
    return v if isinstance(v, list) else [v]


def run_test_old(src, K):
    if src != 'IMM':
        raise SystemExit('--test-old-as supports IMM only')
    res, out, sens = compute('old', K, test_as='IMM')
    os.makedirs(OUTD, exist_ok=True)
    np.savez(OUTD + r'\testold_boot_IMM2_as_IMM.npz', **out)
    json.dump(dict(res=res, sens=sens), open(OUTD + r'\part_testold_IMM2_as_IMM.json', 'w'), indent=1, default=float)
    ref = json.load(open(OUTD + r'\TESTOLD_A_RECOUNT_B.json'))
    mine = keyed(res, 'B.IMM.')
    want = {k: v for k, v in ref.items() if k.startswith('B.IMM.')}
    agree, bad, maxrel = 0, [], 0.0
    for k in sorted(want):
        if k in mine and same(mine[k], want[k]):
            agree += 1
            for x, y in zip(_flat(mine[k]), _flat(want[k])):
                if isinstance(x, float) and isinstance(y, float) and not (math.isnan(x) or math.isnan(y)):
                    maxrel = max(maxrel, abs(x - y) / max(1.0, abs(y)))
        else:
            bad.append(k)
    extra = sorted(set(mine) - set(want))
    ob = np.load(OUTD + r'\testold_boot_IMM.npz')
    arr_ok = {k: bool(np.array_equal(out[k], ob[k][:K], equal_nan=True)) for k in out}
    print('KEYS: %d of %d agree (tol 1e-9 rel); max rel diff %.3g; extra keys in mine: %s' % (agree, len(want), maxrel, extra))
    print('disagreeing keys (interval keys differ by construction when K < 2000):', bad)
    for k in bad:
        print('  ', k, mine.get(k), want[k])
    print('per-resample arrays bit-equal to testold_boot_IMM.npz (first %d rows):' % K, arr_ok)


def run_combine():
    check_locks4()
    target = RF.FINAL_FRESH
    new = {}
    for tag, pre in (('IMM2C', 'fresh'), ('IMM2N', 'new')):
        p = OUTD + r'\part_%s_%s.json' % (pre, tag)
        if os.path.exists(p):
            new.update(keyed(json.load(open(p))['res'], 'B.%s.' % tag))
    if not new:
        raise SystemExit('REFUSED: no part_fresh_IMM2C.json or part_new_IMM2N.json')
    old = json.load(open(target))
    changed = [k for k in new if k in old and not same(old[k], new[k], 0.0)]
    if changed:
        raise SystemExit('REFUSED: existing keys would change: %s' % changed)
    base = os.path.dirname(target)
    stem = base + r'\A_RECOUNT_B_v04_before_IMM2'
    bak = stem + '.json'
    i = 2
    while os.path.exists(bak):
        bak = stem + '_%d.json' % i
        i += 1
    shutil.copy2(target, bak)
    added = [k for k in new if k not in old]
    merged = dict(old)
    merged.update({k: new[k] for k in added})
    json.dump(merged, open(target, 'w'), indent=1, default=float)
    print('added %d keys; old file kept as %s; total keys %d (was %d)' % (len(added), bak, len(merged), len(old)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--fresh', action='store_true')
    g.add_argument('--new', action='store_true')
    g.add_argument('--test-old-as', metavar='NAME')
    g.add_argument('--combine', action='store_true')
    ap.add_argument('--runs-root', default=None)
    ap.add_argument('--K', type=int, default=None)
    a = ap.parse_args()
    if a.fresh:
        run_set('fresh', a.K or 20000)
    elif a.new:
        if not a.runs_root:
            raise SystemExit('--new needs --runs-root')
        run_set('new', a.K or 20000, a.runs_root)
    elif a.combine:
        run_combine()
    else:
        run_test_old(a.test_old_as, a.K or 2000)
