"""Second program (recount2), OPTIONAL part: scoring at (tau 0.75 s, A 6 m/s2) with the extended truth.

Own extended clearances (recount2\\out\\<run>.npz, written by recount2_ext_v01.py) scored with the earlier independent recount
library revision_v11\\recount\\rc_lib_v01.py (grid of 202 scales, selection, step frontier, 201 levels, perfect oracle).
Wrong go = the selected row's extended clearance <= 0.  Caution axis = the 3 s commitment clearance (clear > 0), unchanged.
  denE  = sum over the 201 levels of F_F0 - F_E (wrong go by the extended clearance)
  den0  = sum over levels of F_F0 - F_O, O = first row with extended clearance > 0, else the fallback row
  ratio = denE(extended) / denE(3 s), given for both readings of "3 s": the reaction-and-stop scoring on the 61-frame window
          (the scoring of record) and the 3 s commitment scoring.
Does not open revision_v11\\analysis. Writes RECOUNT2_SCORING_v01.json into this folder.
Usage: python -B -X utf8 recount2_score_v01.py
"""
import json, pathlib, sys
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'recount'))
import rc_lib_v01 as rc                            # noqa: E402

KEY = 't0p75_a6p0'


def build(ds, field, masks_fn):
    rows = []
    for d in ds:
        safe_c = d['clear'] > 0.
        safe_w = safe_c if field == 'W1' else (d[field] > 0.)
        rows.append(rc.run_row(d, masks_fn(d), safe_w, safe_c, False))
    return np.stack(rows)


def masks2(d):
    return [np.ones(d['n'], bool), d['v0'] > 0.5]


def main():
    ds = rc.load_all()
    n_cache_differs = 0
    for d in ds:
        z = np.load(HERE / 'out' / (d['run'] + '.npz'), allow_pickle=False)
        ev = z['evaluated'].astype(bool)
        if not np.array_equal(ev, d['ev_all']):
            raise RuntimeError('%s: evaluated flags differ' % d['run'])
        d['rsX'] = np.asarray(z['clearX_' + KEY], float)[ev]
        d['rs61'] = np.asarray(z['clear61_' + KEY], float)[ev]
        d['lateX'] = np.asarray(z['late_' + KEY])[ev]
        d['censX'] = np.asarray(z['cens_' + KEY])[ev]
        if np.isnan(d['rsX']).any() or np.isnan(d['rs61']).any():
            raise RuntimeError('%s: NaN clearance in an evaluated decision' % d['run'])
        n_cache_differs += int(((d['rs61'] > 0) != (d['rs'] > 0)).sum())
        # worst case: every late, 61-frame-safe, censored pair counted unsafe
        d['rsXw'] = np.where(d['censX'] & (d['rs61'] > 0), -1., d['rsX'])
    out = dict(program='recount2_score_v01.py (optional part; own extended clearances + rc_lib_v01.py)', key=KEY,
               n_runs=len(ds), n_decisions=int(sum(d['n'] for d in ds)), n_flag_differs_own61_vs_cache=n_cache_differs, pops={})
    res = {}
    for name, field in (('W1_3s_commitment', 'W1'), ('RS_61frames_cache', 'rs'), ('RS_61frames_own', 'rs61'), ('RS_extended', 'rsX'),
                        ('RS_extended_censored_unsafe', 'rsXw')):
        M = build(ds, field, masks2)
        n, D, nl = rc.evaluate(M.sum(0)[None], 2)
        res[name] = (n, D, nl)
    for pi, pop in enumerate(('all', 'moving')):
        e = {}
        for name, (n, D, nl) in res.items():
            e[name] = dict(n=float(n[0, pi]), denE=float(D[0, pi, 1]), R_pp=float(D[0, pi, 1]) / rc.NLEV, den0=float(D[0, pi, -1]),
                           D={a: float(D[0, pi, ai]) for ai, a in enumerate(rc.ARMS)}, nan_levels=int(nl[0, pi]))
        x = e['RS_extended']
        e['denE_ext_over_denE_RS61'] = x['denE'] / e['RS_61frames_own']['denE']
        e['denE_ext_over_denE_W1'] = x['denE'] / e['W1_3s_commitment']['denE']
        e['den0_ext_over_den0_RS61'] = x['den0'] / e['RS_61frames_own']['den0']
        e['den0_ext_over_den0_W1'] = x['den0'] / e['W1_3s_commitment']['den0']
        out['pops'][pop] = e
    rc.jdump(out, HERE / 'RECOUNT2_SCORING_v01.json')
    for pop, e in out['pops'].items():
        print(pop)
        for name in res:
            print('  %-28s n %d denE %.6f den0 %.6f' % (name, e[name]['n'], e[name]['denE'], e[name]['den0']))
        print('  denE ext / RS61 %.6f ; ext / W1 %.6f' % (e['denE_ext_over_denE_RS61'], e['denE_ext_over_denE_W1']))


if __name__ == '__main__':
    main()
