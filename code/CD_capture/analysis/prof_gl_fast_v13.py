"""Profiling helper (old runs only): cache the prepared gridless events of the main sources and time gl_fast.evaluate."""
import pathlib, sys, time, pickle
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
cache = HERE / 'out' / 'prof_prep_old.pkl'
import gl_fast_v13 as GF
import numba
if not cache.is_file():
    import cd_common_v13 as CC
    import trk_env_v01 as env; env.setup()
    import trk_score_v01 as TS
    runs = CC.load_old_lead()
    u, _ = TS.e5_u(runs, 'F0', 'E'); TS.add_oracle(runs, 'E5', 'F0', 1.1029, 0.05, u); TS.add_oracle(runs, 'E5p', 'F0', 1.1029, 0.05, TS.permute_u(runs, u))
    G = TS.gridless(runs, ['F0', 'E', 'N', 'E5', 'E5p', 'CK3'])
    P = GF.Prepared(G, ['F0', 'E', 'N', 'E5', 'E5p', 'CK3'], 0)
    pickle.dump(P, open(cache, 'wb'))
P = pickle.load(open(cache, 'rb'))
print('events per source', np.diff(P.ev_off), 'keep', np.diff(P.keep_off), 'threads', numba.get_num_threads(), flush=True)
W = np.random.default_rng(1).multinomial(P.nrun, np.ones(P.nrun) / P.nrun, size=1000).astype(float)
GF.evaluate(P, W[:2])
for B in (100, 1000):
    t = time.time(); GF.evaluate(P, W[:B]); dt = time.time() - t
    print('B=%d: %.3f s, %.2f ms per eval' % (B, dt, 1000 * dt / B), flush=True)
t = time.time()
T0b = np.empty((1000, len(P.names), P.T0[0].shape[1]))
for b in range(1000):
    for s in range(len(P.names)):
        T0b[b, s] = np.tensordot(W[b], P.T0[s], axes=(0, 0))
print('tensordot loop for 1000: %.3f s' % (time.time() - t))
t = time.time(); F, LEV = GF._frontiers(T0b, P.d, P.ri, P.keep, P.ev_off, P.keep_off, W, 201); print('numba kernel 1000: %.3f s' % (time.time() - t))
