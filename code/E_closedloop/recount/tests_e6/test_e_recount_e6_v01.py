"""Synthetic tests for e_recount_e6_v01.py. python -I -B test_e_recount_e6_v01.py"""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RC = HERE.parent
spec = importlib.util.spec_from_file_location('e_recount_e6_v01', RC / 'e_recount_e6_v01.py')
M = importlib.util.module_from_spec(spec)
sys.modules['e_recount_e6_v01'] = M
spec.loader.exec_module(M)

nan = float('nan')


def data(tN, t4=1.0, t8=2.0, t16=4.0):
    """5 cases; cases 0-3 no contact anywhere (T); case 4 has contact in F0D4 and F0D8 only.
    c = (N 0, F4 .2, F8 .2, F16 0); t = (tN, t4, t8, t16)."""
    C = np.zeros((5, 4))
    C[4, 1] = C[4, 2] = 1
    TL = np.zeros((5, 4))
    TL[:4, :] = [tN, t4, t8, t16]
    return C, TL, np.array([1, 1, 1, 1, 0], bool)


def full_idx(n, B=1):
    return np.tile(np.arange(n), (B, 1))


class T(unittest.TestCase):
    def test_bracket_4_8(self):
        r = M.primary_from_arrays(*data(1.5), full_idx(5))
        self.assertEqual(r['bracket'], 'bracketed 4-8')
        self.assertAlmostEqual(r['c_F0_at_tN'], 0.2, 12)      # w = .5, c4 = c8 = .2
        self.assertAlmostEqual(r['delta'], -0.2, 12)
        self.assertEqual((r['n_cases'], r['n_nocontact_all']), (5, 4))
        self.assertEqual(r['c'], [0.0, 0.2, 0.2, 0.0])
        self.assertEqual(r['t'], [1.5, 1.0, 2.0, 4.0])

    def test_bracket_8_16(self):
        r = M.primary_from_arrays(*data(3.0), full_idx(5))
        self.assertEqual(r['bracket'], 'bracketed 8-16')
        self.assertAlmostEqual(r['c_F0_at_tN'], 0.1, 12)      # w = .5 between .2 and 0
        self.assertAlmostEqual(r['delta'], -0.1, 12)

    def test_N_at_t8(self):
        r = M.primary_from_arrays(*data(2.0), full_idx(5))
        self.assertEqual(r['bracket'], 'bracketed 4-8')       # t_N <= t_F0D8 -> first pair, w = 1
        self.assertAlmostEqual(r['c_F0_at_tN'], 0.2, 12)

    def test_edges_inclusive(self):
        self.assertEqual(M.primary_from_arrays(*data(1.0), full_idx(5))['bracket'], 'bracketed 4-8')
        r = M.primary_from_arrays(*data(4.0), full_idx(5))
        self.assertEqual(r['bracket'], 'bracketed 8-16')
        self.assertAlmostEqual(r['c_F0_at_tN'], 0.0, 12)

    def test_not_bracketed(self):
        for tN in (0.5, 4.5):
            r = M.primary_from_arrays(*data(tN), full_idx(5))
            self.assertEqual(r['bracket'], 'not bracketed')
            self.assertIsNone(r['delta'])
            self.assertIsNone(r['c_F0_at_tN'])
            self.assertFalse(r['pass_alone'])
            self.assertAlmostEqual(r['p_one'], 1.0)           # all NaN -> 2/2 against H1
            self.assertEqual(r['finite_share'], 0.0)
            self.assertIsNone(r['ub95'])
            self.assertIsNone(r['ci'])

    def test_non_monotone(self):
        for t4, t8, t16 in ((2.0, 2.0, 4.0), (1.0, 4.0, 3.0), (3.0, 2.0, 4.0)):
            r = M.primary_from_arrays(*data(2.5, t4, t8, t16), full_idx(5))
            self.assertEqual(r['bracket'], 'non-monotone')
            self.assertIsNone(r['delta'])

    def test_empty_T(self):
        C, TL, inT = data(1.5)
        inT = np.zeros(5, bool)
        r = M.primary_from_arrays(C, TL, inT, full_idx(5, 3))
        self.assertEqual(r['bracket'], 'no common no-contact case')
        self.assertEqual(r['n_nocontact_all'], 0)
        self.assertEqual(r['t'], [None] * 4)
        self.assertEqual(r['c'], [0.0, 0.2, 0.2, 0.0])
        self.assertAlmostEqual(r['p_one'], 1.0)
        self.assertFalse(r['pass_alone'])

    def test_bootstrap_nan_multiplicity_quantiles(self):
        C, TL, inT = data(1.5)
        idx = np.array([[0, 1, 2, 3, 4],       # -0.2
                        [4, 4, 4, 4, 4],       # no drawn case in T -> NaN
                        [0, 0, 0, 0, 4],       # -0.2
                        [4, 4, 0, 0, 0],       # case 4 twice: c = (0,.4,.4,0) -> -0.4
                        [0, 1, 2, 3, 3]])      # no contact: 0.0 (>= 0 counts against H1)
        r = M.primary_from_arrays(C, TL, inT, idx)
        self.assertAlmostEqual(r['finite_share'], 4 / 5, 12)
        self.assertAlmostEqual(r['p_one'], (1 + 2) / 6, 12)   # the NaN and the 0.0
        self.assertAlmostEqual(r['ub95'], -0.2 + 0.85 * 0.2, 12)       # sorted [-.4,-.2,-.2,0], pos 2.85
        self.assertAlmostEqual(r['ci'][0], -0.4 + 0.075 * 0.2, 12)
        self.assertAlmostEqual(r['ci'][1], -0.2 + 0.925 * 0.2, 12)
        self.assertTrue(r['pass_alone'])

    def test_multiplicity_in_time_means(self):
        C = np.zeros((3, 4))
        C[2, 0] = 1
        TL = np.zeros((3, 4))
        TL[0] = [1, 1, 2, 4]
        TL[1] = [5, 1, 2, 4]
        inT = np.array([1, 1, 0], bool)
        full = M.primary_from_arrays(C, TL, inT, full_idx(3))
        self.assertEqual(full['t'], [3.0, 1.0, 2.0, 4.0])
        self.assertEqual(full['bracket'], 'bracketed 8-16')
        self.assertAlmostEqual(full['delta'], 1 / 3, 12)       # cF = 0
        idx = np.array([[1, 1, 1],    # tN* = 5 > t16 = 4 -> NaN (only through multiplicity)
                        [2, 2, 2],    # no T -> NaN
                        [0, 0, 2]])   # tN* = 1 = t4 -> 4-8, w = 0, cF = 0, delta = 1/3 (>= 0)
        r = M.primary_from_arrays(C, TL, inT, idx)
        self.assertAlmostEqual(r['finite_share'], 1 / 3, 12)
        self.assertAlmostEqual(r['p_one'], 1.0, 12)
        self.assertAlmostEqual(r['ub95'], 1 / 3, 12)
        self.assertAlmostEqual(r['ci'][0], 1 / 3, 12)
        self.assertAlmostEqual(r['ci'][1], 1 / 3, 12)
        self.assertFalse(r['pass_alone'])

    def test_vector_matches_scalar(self):
        rng = np.random.default_rng(1)
        c = rng.integers(0, 6, (500, 4)) / 5
        t = rng.integers(0, 6, (500, 4)).astype(float)
        t[::17, 2] = nan
        d = M.delta_vec(c, t)
        for i in range(500):
            st, cF, dl = M.point_delta(c[i], [None if np.isnan(x) else x for x in t[i]])
            if dl is None:
                self.assertTrue(np.isnan(d[i]))
            else:
                self.assertAlmostEqual(d[i], dl, 12)

    def test_ub95_known_array(self):
        a = np.arange(1.0, 101.0)
        self.assertAlmostEqual(float(np.quantile(a, 0.95)), 95.05, 12)
        self.assertAlmostEqual(float(np.quantile(a, 0.025)), 3.475, 12)

    # ---- full pipeline on fake rows
    def rows(self, ncase=6):
        arms = {l: {} for l in M.LABELS}
        for i in range(ncase):
            k = 'case%02d' % i
            for j, l in enumerate(M.LABELS):
                contact = 1 if (i == 0 and l != 'N') else 0
                arms[l][k] = dict(run_id='r_%s_%s' % (l, k), case=k, label=l, contact=contact,
                                  time_lost_s=None if contact else [1.5, 1.0, 2.0, 4.0][j] + 0.01 * i,
                                  impact_speed_mps=3.0 if contact else None, rest_gap_m=1.0, peak_decel_mps2=4.0,
                                  rms_jerk_mps3=5.0, fallback_share=0.1, n_assessment_decisions=10, masked_share=0.25)
        return arms

    def test_export_keys_and_json(self):
        arms = self.rows()
        prim = M.primary(arms)
        comps = {s: M.R.compare_pair(arms['N'], arms[l], 'x') for s, l in ((8, 'F0D8'), (16, 'F0D16'))}
        V = M.build_values(arms, prim, comps, 'ran')
        keys = json.loads(Path(M.KEYS_FILE).read_text())['keys']
        self.assertEqual(sorted(V), sorted(keys))
        self.assertEqual(len(keys), 65)
        self.assertEqual(prim['K'], ['case%02d' % i for i in range(6)])
        self.assertEqual(V['E6.n_cases'], 6)
        self.assertEqual(V['E6.n_nocontact_all'], 5)
        self.assertEqual(V['E6.bracket'], 'bracketed 4-8')
        self.assertAlmostEqual(V['E6.pt.N.t'], 1.5 + 0.01 * 3, 12)   # mean of 0.01*i, i=1..5
        self.assertEqual(V['E6.s8.pairs'], 6)
        s = json.dumps({k: M.jsonable(v) for k, v in V.items()}, allow_nan=False)
        self.assertNotIn('NaN', s)

    def test_export_undefined_is_null(self):
        arms = {l: {} for l in M.LABELS}
        prim = M.primary(arms)
        comps = {s: M.R.compare_pair(arms['N'], arms[l], 'x') for s, l in ((8, 'F0D8'), (16, 'F0D16'))}
        V = M.build_values(arms, prim, comps, 'ran')
        self.assertEqual(sorted(V), sorted(json.loads(Path(M.KEYS_FILE).read_text())['keys']))
        for k in ('E6.delta', 'E6.delta.ci', 'E6.delta.ub95', 'E6.pt.N.c', 'E6.pt.N.t', 'E6.s8.dc', 'E6.s8.dc.ci',
                  'E6.s8.mcnemar_p', 'E6.N.contact'):
            self.assertIsNone(M.jsonable(V[k]), k)
        self.assertEqual(V['E6.bracket'], 'no common no-contact case')
        self.assertIs(V['E6.pass_alone'], False)
        self.assertEqual(V['E6.p_one'], 1.0)
        self.assertEqual(V['E6.finite_share'], 0.0)
        json.dumps({k: M.jsonable(v) for k, v in V.items()}, allow_nan=False)

    def test_labels_and_locked_g(self):
        self.assertEqual(M.label_of('e5_', dict(arm='E_N', g=5.95662143529011)), 'N')
        self.assertEqual(M.label_of('e5_', dict(arm='E_F0', g=4.0)), 'F0D4')
        self.assertEqual(M.label_of('e6_', dict(arm='E_F0', g=8.0)), 'F0D8')
        self.assertEqual(M.label_of('e6_', dict(arm='E_F0', g=16.0)), 'F0D16')
        self.assertIsNone(M.label_of('e6_', dict(arm='E_F0', g=4.0)))
        self.assertIsNone(M.label_of('e6_', dict(arm='E_N', g=8.0)))
        rows = [dict(run_id='b', case='c', label='N', valid=True), dict(run_id='a', case='c', label='N', valid=True),
                dict(run_id='x', case='c', label='F0D8', valid=False), dict(run_id='y', case='c', label=None, valid=True)]
        d = M.by_label(rows)
        self.assertEqual(d['N']['c']['run_id'], 'b')
        self.assertEqual(d['F0D8'], {})

    def test_gates(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / 'o1.json').write_text('{}')
            args = ['main', str(td), '--settings', str(td / 's.json'), '--out-outcomes', str(td / 'o1.json'),
                    '--out-compare', str(td / 'o2.json'), '--export', str(td / 'o3.json')]
            with self.assertRaises(SystemExit) as e:
                M.main(args + ['--no-lock-check'])
            self.assertIn('overwrite', str(e.exception))
            (td / 'o1.json').unlink()
            old = M.LOCK
            M.LOCK = td / 'LOCK_A13a.txt'
            try:
                with self.assertRaises(SystemExit) as e:
                    M.main(args)
                self.assertIn('lock', str(e.exception))
            finally:
                M.LOCK = old


if __name__ == '__main__':
    unittest.main()
