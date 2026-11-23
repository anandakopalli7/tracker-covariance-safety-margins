"""Package B, v13 (A11 s6): per-variant recount for key name IMMr (B1r, the re-tuned IMM), written as a new module on top of the
frozen recount_fresh.py / rf_core.py (imported, not edited).  Same keys as B.IMM.*, same draw, same definitions.
Usage (python -I -B -X utf8 immr_v03.py ...):
  --test-old-as IMM [--K 2000]   runs this code path on the 35 old runs with the old B1 arrays; compares with B.IMM.* of
                                 out\\TESTOLD_A_RECOUNT_B.json (ungated)
  --fresh [--K 20000]            105 fresh runs, arrays B_retrack\\out\\retrack_fresh\\B1R\\<rid>_arrays.npz; REFUSES unless
                                 LOCK_A10_2.txt, LOCK_A10_2c.txt and LOCK_A11.txt all exist
  --combine-immr                 adds only the B.IMMr.* keys to B_retrack\\out\\A_RECOUNT_B.json (refuses if an existing key would
                                 change; backs up the old file as A_RECOUNT_B_v03_222keys.json or the next unused name); gated
"""
import sys, os, json, argparse, hashlib, shutil, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import recount_fresh as RF

NAME = 'IMMr'
V13 = RF.V13
LOCK_A11 = V13 + r'\LOCK_A11.txt'
LOCKS3 = [RF.LOCK, RF.LOCK_C, LOCK_A11]
RF.VARS[NAME] = 'B1R'          # fresh path: B_retrack\out\retrack_fresh\B1R\<rid>_arrays.npz (RF.fresh_path, non-CV/IMM branch)
OUTD = RF.OUTD


def check_locks3():
    miss = [p for p in LOCKS3 if not os.path.exists(p)]
    if miss:
        raise SystemExit('REFUSED: fresh runs are sealed; missing ' + ', '.join(miss))
    return {os.path.basename(p): hashlib.sha256(open(p, 'rb').read()).hexdigest() for p in LOCKS3}


def compute(mode, K, test_as=None):
    """mode 'fresh' (IMMr arrays) or 'old' (arrays of the old variant test_as, computed under key name IMMr)."""
    orig_setup = RF.setup

    def setup(m):
        names, pathf, nr, seed = orig_setup(m)
        if m == 'old':
            return names, (lambda nm, run: RF.old_path(test_as, run)), nr, seed
        return names, pathf, nr, seed
    RF.setup = setup
    try:
        return RF.per_variant(NAME, mode, K)
    finally:
        RF.setup = orig_setup


def keys_of(res):
    return {'B.%s.%s' % (NAME, k): v for k, v in res.items()}


def run_fresh(K):
    sha = check_locks3()                 # before any fresh file is touched
    print('locks:', sha, flush=True)
    res, out, sens = compute('fresh', K)
    sens['lock_sha256'] = sha
    os.makedirs(OUTD, exist_ok=True)
    np.savez(OUTD + r'\boot_%s.npz' % NAME, **out)
    json.dump(dict(res=res, sens=sens), open(OUTD + r'\part_fresh_%s.json' % NAME, 'w'), indent=1, default=float)
    print(NAME, 'written; total %.1fs' % sens['total_seconds'], flush=True)


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
    np.savez(OUTD + r'\testold_boot_%s_as_IMM.npz' % NAME, **out)
    json.dump(dict(res=res, sens=sens), open(OUTD + r'\part_testold_%s_as_IMM.json' % NAME, 'w'), indent=1, default=float)
    ref = json.load(open(OUTD + r'\TESTOLD_A_RECOUNT_B.json'))
    mine = {k.replace('B.%s.' % NAME, 'B.IMM.'): v for k, v in keys_of(json.loads(json.dumps(res, default=float))).items()}
    want = {k: v for k, v in ref.items() if k.startswith('B.IMM.')}
    agree = 0
    bad = []
    maxrel = 0.0
    for k in sorted(want):
        if k in mine and same(mine[k], want[k]):
            agree += 1
            for x, y in zip(_flat(mine[k]), _flat(want[k])):
                if isinstance(x, float) and isinstance(y, float) and not (math.isnan(x) or math.isnan(y)):
                    maxrel = max(maxrel, abs(x - y) / max(1.0, abs(y)))
        else:
            bad.append((k, mine.get(k), want[k]))
    extra = sorted(set(mine) - set(want))
    old_boot = np.load(OUTD + r'\testold_boot_IMM.npz')
    arr_ok = {k: bool(np.array_equal(out[k], old_boot[k][:K], equal_nan=True)) for k in out}
    print('KEYS: %d of %d agree (tol 1e-9 rel); max rel diff %.3g; extra keys in mine: %s' % (agree, len(want), maxrel, extra))
    print('disagreeing:', bad)
    print('per-resample arrays bit-equal to testold_boot_IMM.npz (first %d rows):' % K, arr_ok)


def run_combine():
    check_locks3()
    target = RF.FINAL_FRESH
    d = json.load(open(RF.OUTD + r'\part_fresh_%s.json' % NAME))
    new = json.loads(json.dumps(keys_of(d['res']), default=float))
    old = json.load(open(target))
    changed = [k for k in new if k in old and not same(old[k], new[k], 0.0)]
    if changed:
        raise SystemExit('REFUSED: existing keys would change: %s' % changed)
    base = os.path.dirname(target)
    bak = base + r'\A_RECOUNT_B_v03_222keys.json'
    i = 2
    while os.path.exists(bak):
        bak = base + r'\A_RECOUNT_B_v03_222keys_%d.json' % i
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
    g.add_argument('--test-old-as', metavar='NAME')
    g.add_argument('--combine-immr', action='store_true')
    ap.add_argument('--K', type=int, default=None)
    a = ap.parse_args()
    if a.fresh:
        run_fresh(a.K or 20000)
    elif a.combine_immr:
        run_combine()
    else:
        run_test_old(a.test_old_as, a.K or 2000)
