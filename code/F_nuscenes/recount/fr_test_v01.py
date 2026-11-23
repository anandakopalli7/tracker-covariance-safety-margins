"""Package F recount: tests on synthetic arrays. New file, 19 Nov 2026 (Claude Fable 5.2).
1. The fast path (own events + numba kernel2; kernel is its plainer first version, required equal bit for bit) against the scoring library of record: for the full sample and a few resamples,
   every source's curve is rebuilt by brute force with optA_lib_v02.select_grid and stats_scored at g = 0 and just above every
   critical value in [0, 1e3) (the gridless curve's definition: every scale at which a selection can change), and D is formed
   by optA_lib_v02.eval_scoring. Both horizons, both populations, sources F0, E, N, TG, E5_x, E5 (1.1029, 0.05), E5p, PO25, PO50, PO75.
2. The kernel's levels against numpy.linspace (exact).
3. Mid-ranks against a direct O(n^2) count.
4. The calibration rule on constructed coverage tables.
5. Departure path (20 Nov): clearances read through K.swap_clear_v02. With synth\\clear_v02 (equal to the arrays') the scenes
   are identical to the arrays'; with synth\\clear_v02mod (some contacts removed) the fast path still equals the library path,
   and K.removed_counts equals a plain loop. (The v02 scripts are compared with the v01 outputs by fr_test_v02_scripts.py.)
Usage: python -I fr_test_v01.py        (run fr_synth_v01.py first)
"""
import sys, time
sys.dont_write_bytecode = True
import numpy as np
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import fr_core_v01 as K
import fr_run_v01 as R

L = K.L
ROOT = K.HERE / 'synth'
TOL = 1e-9


def brute_tables(scenes, crit_fn, h, pop, w):
    hk = R.HKEYS[h]; mf = R.mask_fn(h, pop)
    vals = [0.]
    for k, z in enumerate(scenes):
        c = crit_fn(k, z)[mf(k, z)]
        c = c[np.isfinite(c) & (c >= 0) & (c < K.GMAX)]
        vals.append(np.nextafter(c, np.inf))
    G = np.unique(np.concatenate([np.atleast_1d(v) for v in vals]))
    T = np.zeros((G.size, L.NST))
    for k, z in enumerate(scenes):
        if w[k] == 0:
            continue
        clear = L.clean_clear(z[hk['clear']])
        sel = L.select_grid(crit_fn(k, z), G, z['idx55'])
        T += w[k] * L.stats_scored(sel, clear, clear > 0., z['vbar'], z['des'], [mf(k, z)])[:, 0, :]
    return T


def test_fast_vs_library(sub=None, trks=('T1', 'IMM'), pops=R.POPS):
    keys = ['sweep', 'idx55', 'vbar', 'des', 'inpath', 'evaluated', 'evaluated2', 'clear', 'clear2'] + \
           [a + s for a in ('cF0', 'cN', 'cE', 'cTG') for s in ('', '_2')]
    worst = 0.
    ncmp = 0
    for trk in trks:
        names, scenes = K.load_split(trk, 'val', keys, root=ROOT)
        if sub:
            scenes = K.swap_clear_v02(names, scenes, 'val', root=ROOT, sub=sub)
        scenes = scenes[:12]; n = len(scenes)
        rng = np.random.default_rng(5)
        W = np.concatenate([np.ones((1, n)), K.counts_of(rng.integers(0, n, (3, n)), n)])
        for h in (3, 2):
            suf = R.HKEYS[h]['suf']; ek = R.HKEYS[h]['ev']
            ev = np.concatenate([z[ek] for z in scenes]).astype(bool)
            cF0 = np.concatenate([z['cF0' + suf] for z in scenes]); cE = np.concatenate([z['cE' + suf] for z in scenes])
            cN = np.concatenate([z['cN' + suf] for z in scenes])
            rs = K.ratio_summary(cF0, cN, ev)
            c5, u, _ = K.e5_scales(cF0, cE, ev, rs['median'], rs['A'])
            cut = np.concatenate([[0], np.cumsum([z[ek].size for z in scenes])])
            e5, uu, _ = K.e5_scales(cF0, cE, ev, K.E5_M, K.E5_A)
            up = K.permute_u(uu, ev, cut)
            for k in range(len(scenes)):                    # the permutation stays within scenes and within evaluated decisions
                q = slice(cut[k], cut[k + 1])
                assert np.array_equal(np.sort(up[q][ev[q]]), np.sort(uu[q][ev[q]]))
                assert np.array_equal(up[q][~ev[q]], uu[q][~ev[q]])
            assert not np.array_equal(up, uu)
            e5p = K.scales_from_u(cF0, up, K.E5_M, K.E5_A)
            po = K.po_scales(cF0, cE)
            Uref = np.random.default_rng(20261919).random(cF0.shape[0])
            assert np.array_equal(po[1], np.where((Uref < 0.5)[:, None], cE, cF0), equal_nan=True)
            fns = [('F0', lambda k, z: z['cF0' + suf]), ('E', lambda k, z: z['cE' + suf]), ('N', lambda k, z: z['cN' + suf]),
                   ('TG', lambda k, z: z['cTG' + suf]), ('E5x', lambda k, z: c5[cut[k]:cut[k + 1]]),
                   ('E5', lambda k, z: e5[cut[k]:cut[k + 1]]), ('E5p', lambda k, z: e5p[cut[k]:cut[k + 1]]),
                   ('PO25', lambda k, z: po[0][cut[k]:cut[k + 1]]), ('PO50', lambda k, z: po[1][cut[k]:cut[k + 1]]),
                   ('PO75', lambda k, z: po[2][cut[k]:cut[k + 1]])]
            NM = [nm for nm, _ in fns[1:]]
            for pop in pops:
                ncmp += 1
                pk, info = R.build_pack(scenes, h, pop, fns)
                fast = K.kernel2(W, *pk)
                slow = K.kernel(W, *pk)
                assert np.array_equal(fast, slow, equal_nan=True), (fast, slow)      # the two own kernels: bit for bit
                for b in range(W.shape[0]):
                    Tp = {nm: brute_tables(scenes, fn, h, pop, W[b]) for nm, fn in fns}
                    e = L.eval_scoring(Tp, NM)
                    ref = np.array([e['n'], e['c0'], e['C']] + [e['D'][x] for x in NM])
                    assert abs(e['D']['E'] - e['denE']) < 1e-12
                    d = np.abs(fast[b] - ref)
                    assert np.isfinite(ref).all(), ref
                    assert d.max() <= TOL, (trk, h, pop, b, fast[b], ref)
                    worst = max(worst, d.max())
                print('  %s %d s %-6s ok: n %d, R_gl %.4f pp, RR %s'
                      % (trk, h, pop, fast[0, 0], fast[0, 3] / 201,
                         ' '.join('%s %.4f' % (x, fast[0, 3 + j] / fast[0, 3]) for j, x in enumerate(NM) if j)), flush=True)
    print('%s fast path = library path on %d comparisons (4 weightings each), max abs difference %.3g (tolerance %g)'
          % ('5.' if sub else '1.', ncmp, worst, TOL))


def test_departure_path():
    keys = ['sweep', 'idx55', 'evaluated', 'evaluated2', 'clear', 'clear2', 'cF0', 'cE', 'cF0_2', 'cE_2']
    names, old = K.load_split('T1', 'train', keys, root=ROOT)
    same = K.swap_clear_v02(names, old, 'train', root=ROOT)
    for a, b in zip(old, same):
        for k in keys:
            assert np.array_equal(a[k], b[k], equal_nan=True)
    new = K.swap_clear_v02(names, old, 'train', root=ROOT, sub='clear_v02mod')
    for ck, ek, suf in (('clear', 'evaluated', ''), ('clear2', 'evaluated2', '_2')):
        for x in ('F0', 'E'):
            z0 = K.removed_counts(old, same, 'c' + x + suf, ck, ek)
            assert z0['removed'] == 0 and z0['added'] == 0 and z0['pairs_unsafe_to_safe'] == 0 and z0['pairs_safe_to_unsafe'] == 0
            got = K.removed_counts(old, new, 'c' + x + suf, ck, ek)
            rem = add = p1 = p2 = 0
            for zo, zn in zip(old, new):
                for i in range(zo[ek].size):
                    if not zo[ek][i]:
                        continue
                    sel = int(zo['idx55'][i])
                    for j in range(17):
                        if zo['c' + x + suf][i, j] >= 1.0:
                            sel = j
                            break
                    uo = not (zo[ck][i, sel] > 0); un = not (zn[ck][i, sel] > 0)
                    rem += uo and not un; add += (not uo) and un
                    for j in range(17):
                        a_ = zo[ck][i, j] > 0; b_ = zn[ck][i, j] > 0
                        p1 += (not a_) and b_; p2 += a_ and (not b_)
            assert (got['removed'], got['added'], got['pairs_unsafe_to_safe'], got['pairs_safe_to_unsafe']) == (rem, add, p1, p2)
            assert got['removed'] > 0 and got['added'] == 0
    print('5. departure path: clear_v02 equal to the arrays gives identical scenes; removed counts equal a plain loop')
    test_fast_vs_library(sub='clear_v02mod', trks=('T1',), pops=('all',))


def test_levels():
    rng = np.random.default_rng(1)
    for _ in range(20000):
        c0 = rng.uniform(0, 30); C = c0 + rng.uniform(0, 40) * rng.random() ** 3
        step = (C - c0) / 200
        lev = np.array([l * step + c0 for l in range(201)]); lev[200] = C
        assert np.array_equal(lev, np.linspace(c0, C, 201))
    print('2. levels equal numpy.linspace exactly (20,000 draws)')


def test_midrank():
    rng = np.random.default_rng(2)
    r = np.round(rng.normal(size=300), 1); r[rng.random(300) < 0.1] = np.nan
    rk, n = K.midrank(r)
    f = np.isfinite(r)
    for i in np.nonzero(f)[0]:
        ref = (r[f] < r[i]).sum() + ((r[f] == r[i]).sum() + 1) / 2.
        assert rk[i] == ref
    assert n == f.sum() and np.isnan(rk[~f]).all()
    print('3. mid-ranks ok')


def test_calibration():
    rng = np.random.default_rng(3)
    c = rng.random((2000, 1)) < np.linspace(0.96, 0.999, 100)[None, :]
    d = K.calibrate_decide(np.sort(c, axis=1))
    assert d['level'] == 0.95
    p = np.linspace(0.925, 0.999, 100)
    u = rng.random((2000, 1)); c1 = u < p[None, :]
    d = K.calibrate_decide(c1, c1)
    k = int(np.argmax(c1.mean(axis=0) >= 0.95))
    assert d['candidate_level'] == K.LEVELS[k] and d['level'] in (K.LEVELS[k], 0.99), d
    d2 = K.calibrate_decide(c1, np.roll(c1, 30, axis=1) | c1)
    print('4. calibration rule ok:', d['rule'], '| mc_sd %.5f' % d['mc_sd'], '|', d2['rule'])


if __name__ == '__main__':
    t0 = time.time()
    test_levels(); test_midrank(); test_calibration(); test_departure_path()
    if '--departure-only' not in sys.argv:
        test_fast_vs_library()
    print('ALL TESTS PASSED (%.0f s)' % (time.time() - t0))
