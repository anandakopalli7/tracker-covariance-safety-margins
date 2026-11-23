"""Revision v12, AMENDMENT_09 A9-7 step 1 (review item S2): critical scales of a constant time-gap margin. New file, 19 Nov 2026.
Construction as rev_f1_braking_prior_extract_v01.py (v11; planner rows and constraints rebuilt with the planner library through
oxsb_extract_v05's modules, read-only): for every constraint of every row, s = (r0 + v_e)^2 with v_e the row's speed at the
constraint's time (constraint column j < 60 of an actor block at sample j, column 60 + j at sample j + 1, as in gc.geometry);
critical scale gc.crit_rows(D, s). With g = h^2 a row is feasible when every clearance d >= h (r0 + v_e): a time gap h with a
standstill distance h r0. r0 = 2 m/s primary; 1 and 4 m/s as sensitivities.
Identity: the class-average critical values recomputed here equal the stored cF0 (all 35 evaluation runs).
Output: out/tg/<run>.npz (cTG1, cTG2, cTG4) and out/A9_7A_TG_EXTRACT_SUMMARY_v01.json.
Usage: python -B -X utf8 a9_7a_timegap_extract_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
OJ = P / '11_ojits'
sys.path.insert(0, str(OJ / 'A4' / 'code'))
import oxsb_extract_v05 as ex                # noqa: E402
c3 = ex.c3; sb = ex.sb; gc = ex.gc; rx = ex.rx; oc = ex.oc
consumer = ex.consumer; finite_primitive = ex.finite_primitive

OUTD = HERE / 'out' / 'tg'
OUTD.mkdir(parents=True, exist_ok=True)
SUMMARY = HERE / 'out' / 'A9_7A_TG_EXTRACT_SUMMARY_v01.json'
if SUMMARY.exists():
    sys.exit('REFUSED: %s exists' % SUMMARY)
PB = json.loads(gc.PBAR_FILE.read_text(encoding='utf-8'))['Pbar']
FIT_RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
R0S = (1., 2., 4.)
JIDX = np.concatenate([np.arange(60), np.arange(1, 61)])          # sample index of each of the 120 columns of an actor block


def same(a, b):
    return int((~((a == b) | (np.isnan(a) & np.isnan(b)))).sum())


def run_one(run):
    Lr = rx.load_run('fit', run, sb.YAW); cap = Lr['cap']
    z = np.load(c3.STORED / (run + '.npz'), allow_pickle=False)
    decs = list(gc.decisions(cap))
    ks = np.array([k for k, _ in decs], dtype=np.int64)
    if not (ks.shape == z['k'].shape and (ks == z['k']).all()):
        raise RuntimeError('decisions differ from the stored k')
    nd = len(decs)
    out = {'cTG%d' % r0: np.full((nd, 17), np.nan) for r0 in R0S}
    n_f0_diff = 0
    for di, (k, dec) in enumerate(decs):
        ms = dec['model_state']; actors = dec['actors']; now = dec['now']
        rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'], actors,
                                              dec['ego_length'], dec['ego_width'], now, consumer.Diagnostics())
        n = len(rows); assert n == 17
        na = len(actors); M = 120 * na
        if na == 0:
            for r0 in R0S:
                out['cTG%d' % r0][di] = z['cF0'][di]
            continue
        D = np.stack([x['d'] for x in rows]).reshape(n, M)
        N, TE, MU = gc.geometry(rows, actors, now)
        Sbar = gc.s_P(N, TE, [np.array(PB[oc.cls_of(a['name'])], float) for a in actors])
        n_f0_diff += same(gc.crit_rows(D, Sbar), z['cF0'][di])
        V = np.stack([np.asarray(x['v'], float) for x in rows])            # (17, 61)
        VE = np.tile(V[:, JIDX], (1, na))                                  # (17, M)
        for r0 in R0S:
            out['cTG%d' % r0][di] = gc.crit_rows(D, (r0 + VE) ** 2)
    np.savez_compressed(OUTD / (run + '.npz'), k=ks, meta=json.dumps(dict(run=run, code='a9_7a_timegap_extract_v01.py')), **out)
    return dict(run=run, n_dec=nd, cF0_rows_differ=n_f0_diff)


t00 = time.time(); rows_ = []
for i, run in enumerate(FIT_RUNS):
    rows_.append(run_one(run))
    print('%s (%d / %d, %.0f s): %s' % (run, i + 1, len(FIT_RUNS), time.time() - t00, rows_[-1]), flush=True)
SUMMARY.write_text(json.dumps(dict(code='a9_7a_timegap_extract_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-7',
                                   runs=rows_, total_cF0_rows_differ=sum(r['cF0_rows_differ'] for r in rows_),
                                   written=time.strftime('%Y-%m-%d %H:%M:%S'), seconds=time.time() - t00), indent=1), encoding='utf-8')
print('done (%.0f s)' % (time.time() - t00))
