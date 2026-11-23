"""Diagnostic 3 (post comparison): as diagnostic 2 with the zero-margin fallback where no training scale qualifies."""
import json, numpy as np
exec(open('rc_diag_a93b_v12.py', encoding='utf-8').read().split('def heldout')[0])


def heldout(decode, fallback):
    HO = np.zeros((NLEV, 3)); nof = np.zeros(NLEV, int)
    for ri in range(len(runs)):
        oth = np.array([j for j in range(len(runs)) if j != ri])
        St = S[oth].sum(0).sum(0); Kt = K[oth].sum(0).sum(0); Wt = W[oth].sum(0).sum(0)
        ch = choose(100. * St / Kt, Wt, LEV); ok = ch >= 0; nof += ~ok; g = np.where(ok, ch, 0)
        if fallback:
            ok = np.ones_like(ok)
        g0, g1, g2 = decode(g)
        HO[ok] += np.stack([W[ri, 0, g0] + W[ri, 1, g1] + W[ri, 2, g2], S[ri, 0, g0] + S[ri, 1, g1] + S[ri, 2, g2],
                            K[ri, 0, g0] + K[ri, 1, g1] + K[ri, 2, g2]], 1)[ok]
    v = (nof == 0) | fallback
    c = 100. * HO[v, 1] / HO[v, 2]; w = 100. * HO[v, 0] / N_ALL
    F1 = R.step_front(np.concatenate([[c0], c]), np.concatenate([[w0], w]), LEV)
    return float(np.sum(F1 - F_F0))


z = lambda g: np.zeros_like(g)
out = {}
for fb in (False, True):
    for nm, dec in (('(g,g,g)', lambda g: (g, g, g)), ('(g,g,0)', lambda g: (g, g, z(g))), ('(0,g,0)', lambda g: (z(g), g, z(g)))):
        out['%s fallback=%s' % (nm, fb)] = heldout(dec, fb)
print(json.dumps(out, indent=1))
