"""Test of the E4 mask law in e_recount_v04.py. python -I -B recount\\test\\test_mask_law_v04.py (from work\\E_closedloop)."""
import collections
import importlib.util
import sys
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'e_recount_v04.py'
spec = importlib.util.spec_from_file_location('rv4', P)
R = importlib.util.module_from_spec(spec)
sys.modules['rv4'] = R
spec.loader.exec_module(R)

N_IDS, N_TICKS = 2000, 69
draws = starts = 0
Ls = collections.Counter()
max_stretch = 0
row0 = 0
adj = 0
for j in range(N_IDS):
    m, w, d, st = R.dropout_mask('syn_case_%05d' % j, N_TICKS)
    draws += d
    starts += st
    row0 += m[0]
    for (a, L) in w:
        if a + L < N_TICKS:         # not cut by the run end
            Ls[L] += 1
    # longest stretch of consecutive ones
    run = best = 0
    for x in m:
        run = run + 1 if x else 0
        best = max(best, run)
    max_stretch = max(max_stretch, best)
    for (a, L), (b, _) in zip(w, w[1:]):
        if b <= a + L:              # next window starts at the gap row or inside: forbidden
            adj += 1
tot = sum(Ls.values())
print('ids', N_IDS, 'ticks', N_TICKS, 'draws', draws, 'starts', starts, 'start rate %.4f' % (starts / draws))
print('L counts (uncut windows)', dict(sorted(Ls.items())), 'shares', {k: round(v / tot, 3) for k, v in sorted(Ls.items())})
print('longest stretch', max_stretch, 'row 0 masked count', row0, 'windows without a gap row', adj)
assert abs(starts / draws - 0.10) < 0.01
assert max_stretch <= 3 and row0 == 0 and adj == 0
assert all(abs(v / tot - 1 / 3) < 0.03 for v in Ls.values()) and set(Ls) == {1, 2, 3}
for c in ('c1109_eval_0480', 'c1109_eval_0726', 'c1109_tune_0000'):
    print(c, ''.join(str(x) for x in R.dropout_mask(c, N_TICKS)[0]))
print('MASK LAW TEST PASSED')
