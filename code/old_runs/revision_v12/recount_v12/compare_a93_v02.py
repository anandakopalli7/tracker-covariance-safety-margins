"""Compares the corrected first program for A9-3 (analysis/out/A9_3_PHASE_SCALE_CV_v02.json) with the recount's values
(RECOUNT_VALUES_v12.json, saved before the recount saw any first-program output). Written 19 Nov 2026 by the revision session
after the recount reported the A9-3 disagreements; it reads only the two JSON files. Output: RECOUNT_COMPARE_A93_v02.md.
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
R = json.loads((HERE / 'RECOUNT_VALUES_v12.json').read_text(encoding='utf-8'))['A9_3']
F = json.loads((HERE.parent / 'analysis' / 'out' / 'A9_3_PHASE_SCALE_CV_v02.json').read_text(encoding='utf-8'))
rows = []


def cmp(label, rv, fv):
    rows.append((label, rv, fv, abs(rv - fv)))


ta = F['a_truth_phase']; ra = R['a_truth_phase']
cmp('truth: in-sample share', ra['gain_in_share'], ta['insample']['share'])
cmp('truth: LORO G_cv share', ra['G_cv_share'], ta['loro']['G_cv_share'])
cmp('truth: LORO G_cv (pp)', ra['G_cv_pp'], ta['loro']['G_cv_pp'])
cmp('truth: LORO G_cv_vs_in share', ra['G_cv_vs_in_share'], ta['loro']['G_cv_vs_in_share'])
cmp('truth: LORO sum(F1_cv - F1_in)', -ra['single_cv_vs_in_sum'], ta['loro']['raw']['F1cv_minus_F1'])
e = F['b_estimated_phase']['-1.0']; rb = R['b_estimated_phase']
cmp('estimated: in-sample share', rb['gain_in_share'], e['insample']['share'])
cmp('estimated: LORO G_cv share', rb['G_cv_share'], e['loro']['G_cv_share'])
cmp('estimated: LORO G_cv (pp)', rb['G_cv_pp'], e['loro']['G_cv_pp'])
cmp('estimated: LORO G_cv_vs_in share', rb['G_cv_vs_in_share'], e['loro']['G_cv_vs_in_share'])
cmp('estimated: agreement', R['b_agreement'], e['agreement'])
L = ['# A9-3: the corrected first program (v02) against the recount', '',
     'v02 drops the held-out point of a level at which some fold has no qualifying choice (the recount\'s reading). '
     'Values compared to 1e-9.', '', '| Value | Recount | First program v02 | Abs. difference | Agree |', '|---|---|---|---|---|']
for lab, rv, fv, dd in rows:
    L.append('| %s | %r | %r | %.3g | %s |' % (lab, rv, fv, dd, 'yes' if dd <= 1e-9 else 'NO'))
n_ok = sum(1 for r in rows if r[3] <= 1e-9)
L += ['', '%d of %d values agree within 1e-9.' % (n_ok, len(rows))]
(HERE / 'RECOUNT_COMPARE_A93_v02.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('\n'.join(L))
