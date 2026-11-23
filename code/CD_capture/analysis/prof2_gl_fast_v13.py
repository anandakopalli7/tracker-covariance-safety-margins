import pathlib, sys, time, pickle
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode = True; sys.path.insert(0, str(HERE))
import gl_fast_v13 as GF, numba
P = pickle.load(open(HERE / 'out' / 'prof_prep_old.pkl', 'rb'))
W = np.random.default_rng(1).multinomial(P.nrun, np.ones(P.nrun) / P.nrun, size=200).astype(float)
GF.evaluate(P, W[:2])
for th in (1, 4, 8):
    numba.set_num_threads(th)
    t = time.time(); GF.evaluate(P, W); dt = time.time() - t
    print('threads %d: %.2f ms per eval; %.0f ns per event-thread' % (th, 1000 * dt / 200, 1e9 * dt * th / 200 / P.ev_off[-1]), flush=True)
