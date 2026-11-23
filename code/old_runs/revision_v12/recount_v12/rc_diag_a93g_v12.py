"""Diagnostic 7 (post comparison): per-phase LORO where no training triple qualifies at a level: fallback to the triple with
the lowest training caution (ties lowest W, then lowest index). Does not change RECOUNT_VALUES_v12.json."""
import json, numpy as np
exec(open('rc_diag_a93f_v12.py', encoding='utf-8').read().split('def loro')[0])


def loro(W, S, K, fb):
    HO = np.zeros((NLEV, 3)); nof = np.zeros(NLEV, int); nr = len(runs)
    for ri in range(nr):
        oth = np.array([j for j in range(nr) if j != ri])
        Wtr, Str, Ktr = W[oth].sum(0), S[oth].sum(0), K[oth].sum(0)
        c = 100. * triple(Str) / triple(Ktr); wv = triple(Wtr)
        ch = choose(c, wv, LEV)
        if fb == 'min_caution':
            cand = np.nonzero(c == c.min())[0]
            alt = cand[np.lexsort((cand, wv[cand]))[0]]
            ch = np.where(ch >= 0, ch, alt)
        ok = ch >= 0; nof += ~ok
        g0, rem = np.divmod(np.where(ok, ch, 0), NG * NG); g1, g2 = np.divmod(rem, NG)
        HO[ok] += np.stack([W[ri, 0, g0] + W[ri, 1, g1] + W[ri, 2, g2], S[ri, 0, g0] + S[ri, 1, g1] + S[ri, 2, g2],
                            K[ri, 0, g0] + K[ri, 1, g1] + K[ri, 2, g2]], 1)[ok]
    v = nof == 0
    c = 100. * HO[v, 1] / HO[v, 2]; w = 100. * HO[v, 0] / N_ALL
    Fps = R.step_front(np.concatenate([[c0], c]), np.concatenate([[w0], w]), LEV)
    return float(np.sum(F_F0 - Fps)), int(v.sum())


out = {}
for tag, pha in (('truth', [r['ph'] for r in runs]), ('estimated', [est_phase(r['run']) for r in runs])):
    W, S, K = tables(pha)
    out[tag] = loro(W, S, K, 'min_caution'); print(tag, out[tag], flush=True)
print('first program G_cv_vs_in raw: truth 973.3655006031364, estimated 1076.357056694813')
open('rc_diag_a93g_v12.json', 'w', encoding='utf-8').write(json.dumps(out, indent=1))
