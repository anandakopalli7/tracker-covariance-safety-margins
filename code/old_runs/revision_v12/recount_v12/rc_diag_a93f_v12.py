"""Diagnostic 6 (post comparison): per-phase LORO with training sums formed as (total - left-out run) and via tensordot with
a 0/1 count vector, instead of summing the 34 runs. Does not change RECOUNT_VALUES_v12.json."""
import json, numpy as np
src = open('rc_diag_a93d_v12.py', encoding='utf-8').read().split('def triple')[0]
exec(src)


def triple(A):
    return ((A[0][:, None, None] + A[1][None, :, None]) + A[2][None, None, :]).ravel()


def choose(c, Wc, lev):
    o = np.argsort(c, kind='stable'); cs = c[o]; ws = Wc[o]; rm = np.minimum.accumulate(ws)
    p = np.searchsorted(cs, lev, side='right') - 1
    out = np.full(lev.size, -1, np.int64); ok = p >= 0
    best = rm[np.clip(p, 0, None)]; q = np.searchsorted(-rm, -best, side='left'); out[ok] = o[q[ok]]
    return out


def loro(W, S, K, mode):
    HO = np.zeros((NLEV, 3)); nof = np.zeros(NLEV, int); nr = len(runs)
    for ri in range(nr):
        oth = np.array([j for j in range(nr) if j != ri])
        if mode == 'sum34':
            Wtr, Str, Ktr = W[oth].sum(0), S[oth].sum(0), K[oth].sum(0)
        elif mode == 'total_minus':
            Wtr, Str, Ktr = W.sum(0) - W[ri], S.sum(0) - S[ri], K.sum(0) - K[ri]
        else:
            cn = np.ones(nr); cn[ri] = 0.
            Wtr, Str, Ktr = (np.tensordot(cn, A, axes=(0, 0)) for A in (W, S, K))
        ch = choose(100. * triple(Str) / triple(Ktr), triple(Wtr), LEV)
        ok = ch >= 0; nof += ~ok
        g0, rem = np.divmod(np.where(ok, ch, 0), NG * NG); g1, g2 = np.divmod(rem, NG)
        HO[ok] += np.stack([W[ri, 0, g0] + W[ri, 1, g1] + W[ri, 2, g2], S[ri, 0, g0] + S[ri, 1, g1] + S[ri, 2, g2],
                            K[ri, 0, g0] + K[ri, 1, g1] + K[ri, 2, g2]], 1)[ok]
    v = nof == 0
    c = 100. * HO[v, 1] / HO[v, 2]; w = 100. * HO[v, 0] / N_ALL
    Fps = R.step_front(np.concatenate([[c0], c]), np.concatenate([[w0], w]), LEV)
    return float(np.sum(F_F0 - Fps))


out = {}
for tag, pha in (('truth', [r['ph'] for r in runs]), ('estimated', [est_phase(r['run']) for r in runs])):
    W, S, K = tables(pha)
    for mode in ('sum34', 'total_minus', 'tensordot'):
        out['%s %s' % (tag, mode)] = loro(W, S, K, mode); print(tag, mode, out['%s %s' % (tag, mode)], flush=True)
print('first program G_cv_vs_in raw: truth 973.3655006031364, estimated 1076.357056694813')
open('rc_diag_a93f_v12.json', 'w', encoding='utf-8').write(json.dumps(out, indent=1))
