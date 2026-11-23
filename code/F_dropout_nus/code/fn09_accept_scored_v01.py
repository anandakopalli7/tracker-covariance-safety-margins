"""AMENDMENT_12 sec. 5b, acceptance supplement: do the last-bit differences between the pod's accept arrays (masks OFF,
punish_num = 1) and F's laptop arrays change any SCORED value? New file, 22 Nov 2026 (Claude Opus 5.5, worker of package F).
No masked value: this reproduces F's exported unmasked T1 values (out\\F_HELDOUT_v02.json, populations.*.T1) from both array sets.
Machinery as fn06 / F's f06: F's load_runs with the clearance under the departure (clear_v02, decision ticks checked), populations
0 = all evaluated decisions, 1 = in-path lead; trk_score_v01.gridless / rr_gl; f06k_kernel_v01 (checked against rr_gl on the first 25
resamples); scene bootstrap default_rng(20261923).integers(0, 150, (20000, 150)) as counts.
Per array set (F = work\\F_nuscenes\\cache\\arrays_T1\\val, POD = HOME\\cache\\arrays_accept\\val): full-sample R_pp, R_deceq, n, D_N,
RR_N (both populations) and the 20,000 resample values of R = denE / 201, D_N and n (population 0). Output: the largest absolute
differences between the two sets, the 95% intervals of R from both, and F's exported values for reference.
Usage: python -I -B fn09_accept_scored_v01.py   (scoring environment, numba)
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fn_common_v01 as FC                   # noqa: E402  (before numpy)
import json, time                            # noqa: E402
import numpy as np                           # noqa: E402
sys.path.insert(0, str(FC.WORK / 'shared' / 'trackers'))
import trk_score_v01 as TS                   # noqa: E402
import f06k_kernel_v01 as K                  # noqa: E402
L = TS.L
NLEV = L.NLEV


def load(adir):
    runs = []
    for nm in sorted(FC.splits()['val']):
        z = np.load(adir / (nm + '.npz'), allow_pickle=False)
        meta = json.loads(str(z['meta']))
        ev = z['evaluated'].astype(bool)
        c2 = np.load(FC.SRC_CACHE / 'clear_v02' / 'val' / (nm + '.npz'), allow_pickle=False)
        if not np.array_equal(c2['sweep'], z['sweep']) or not np.array_equal(np.isnan(c2['clear']), np.isnan(z['clear'])):
            raise RuntimeError('clear_v02 does not match the arrays of %s' % nm)
        inpath = z['inpath'].astype(bool)
        runs.append(dict(run=nm, desired=float(meta['desired']), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(c2['clear']),
                         vbar=z['vbar'], masks=(ev, ev & inpath), ev=ev, n_dec=int(ev.size),
                         crit={k: np.asarray(z['c' + k], float) for k in ('F0', 'E', 'N')}, sel={}, late={}))
    return runs


def main():
    FC.require_split('val')
    outf = FC.OUT / 'ACCEPT3_SCORED_v01.json'
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    t0 = time.time()
    n = 150
    idx = np.random.default_rng(20261923).integers(0, n, (20000, n))
    CNT = np.bincount((idx + n * np.arange(20000)[:, None]).ravel(), minlength=20000 * n).reshape(20000, n).astype(np.float64)
    res = {}; boot = {}
    for label, adir in (('F', FC.SRC_CACHE / 'arrays_T1' / 'val'), ('POD', FC.CACHE / 'arrays_accept' / 'val')):
        runs = load(adir)
        G = TS.gridless(runs, ['F0', 'E', 'N'])
        ent = {}
        for pop in (0, 1):
            p = TS.rr_gl(G, 'F0', 'E', ['N'], pop)
            ent['pop%d' % pop] = dict(n=p['n'], R_pp=p['R_pp'], R_deceq=p['R_deceq'], D_N=p['D']['N'], RR_N=p['RR']['N'],
                                      D_N_deceq=p['D_deceq']['N'])
        args = K.pack([G[k] for k in ('F0', 'E', 'N')], 0)
        o = K.eval_many(CNT, *args)
        worst = 0.
        for b in range(25):
            ref = TS.rr_gl(G, 'F0', 'E', ['N'], 0, CNT[b])
            for x, y in ((ref['denE'], o[b, 1]), (ref['n'], o[b, 0]), (ref['D']['N'], o[b, 2])):
                worst = max(worst, abs(x - y) / max(abs(x), abs(y), 1e-12))
        if worst > 1e-9:
            raise RuntimeError('fast evaluator differs from the reference (%s)' % worst)
        boot[label] = dict(R=o[:, 1] / NLEV, D_N=o[:, 2], n=o[:, 0])
        ent['R_ci95'] = L.pct(boot[label]['R']); ent['share_R_nonpositive'] = float(np.mean(~(boot[label]['R'] > 0)))
        ent['verify_max_rel'] = worst
        res[label] = ent
    dif = {}
    for pop in ('pop0', 'pop1'):
        for k in ('n', 'R_pp', 'R_deceq', 'D_N', 'RR_N', 'D_N_deceq'):
            a, b = res['F'][pop][k], res['POD'][pop][k]
            dif['%s.%s' % (pop, k)] = 0. if (np.isnan(a) and np.isnan(b)) else float(abs(a - b))
    for k in ('R', 'D_N', 'n'):
        a, b = boot['F'][k], boot['POD'][k]
        both = np.isnan(a) & np.isnan(b)
        dif['boot.' + k] = float(np.max(np.where(both, 0., np.abs(a - b))))
        dif['boot.%s.bits_differ' % k] = int(np.sum(~((a == b) | both)))
    dif['R_ci95'] = [abs(x - y) for x, y in zip(res['F']['R_ci95'], res['POD']['R_ci95'])]
    fx = json.loads((FC.SRC / 'out' / 'F_HELDOUT_v02.json').read_text(encoding='utf-8'))
    exported = {pn: fx['populations'][pn]['T1'] for pn in ('all', 'inpath')}
    exported['R_ci_all'] = fx['populations']['all']['boot']['R']
    doc = dict(code='fn09_accept_scored_v01.py', note='unmasked T1 values of record reproduced from both array sets; no masked value',
               values=res, abs_differences=dif, F_exported_T1=exported, seconds=round(time.time() - t0, 1), written=FC.clock(),
               code_sha256=FC.sha256_file(pathlib.Path(__file__)))
    outf.write_text(FC.jdump(doc), encoding='utf-8')
    print(json.dumps(dif))


if __name__ == '__main__':
    main()
