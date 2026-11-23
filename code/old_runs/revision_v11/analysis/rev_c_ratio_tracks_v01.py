"""Revision v11, post hoc checks R19, R20 and S9 (ARS review of draft v10). New file, 18 Nov 2026.
Descriptive; declared in AMENDMENT_08 (revision_v11). Reads only the stored Gate R arrays (gateR_rt_v01, 223 runs) and, for the
evaluation runs, the A4 extraction's phase labels.

R20  The margin-ratio check of Fig. 2(b) per scenario family and set. For every evaluated decision and row with a finite positive
     critical scale under both N and F0: ratio of critical scales r = cN / cF0; margin ratio m = 1 / sqrt(r) (the tracker's
     margin over the class average's at the binding constraint, if the same constraint binds). Reported: rows, median m, the
     share of rows more than 5% from the family's median, percentiles of m. This is a recount of
     09_redesign/review/lead_peek_gateR_ratios_v02.py with independent code.
R19  Track initialisations in the lead-braking runs: evaluated decisions by the age of the lead's track (prim_age, s) and by
     its consecutive misses (prim_miss); re-initialisations visible in the stored decisions (a drop of prim_age); the margin
     ratio by track-age band; and the 3 s room and D(N, F0) on the evaluated decisions whose lead track is younger than 4 s.
S9   The rows more than 5% from the median in lead braking: by set, run, track age, misses, phase and value of m.
Usage: python -B -X utf8 rev_c_ratio_tracks_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_C_RATIO_TRACKS_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
doc = dict(code='rev_c_ratio_tracks_v01.py', status='post hoc, descriptive; AMENDMENT_08', R20={}, R19={}, S9={})

# ------------------------------------------------------------------------------------------------ R20
fam_rows = {}
nruns = {}
lb = []           # per-row records of lead braking: set, run, decision index, row, m, prim_age, prim_miss
for f in sorted(C.STORED.glob('*.npz')):
    if f.name.endswith('.tmp.npz'):
        continue
    z = np.load(f, allow_pickle=False)
    meta = json.loads(str(z['meta']))
    fam = meta['family']; st = meta.get('set', '?')
    nruns[(fam, st)] = nruns.get((fam, st), 0) + 1
    ev = z['evaluated'].astype(bool)
    if not ev.any():
        continue
    c0 = z['cF0']; cn = z['cN']
    ok = ev[:, None] & np.isfinite(c0) & np.isfinite(cn) & (c0 > 0) & (cn > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        m = 1. / np.sqrt(cn / c0)
    di, ri = np.nonzero(ok)
    fam_rows.setdefault((fam, st), []).append(m[di, ri])
    fam_rows.setdefault((fam, 'all'), []).append(m[di, ri])
    nrows_ev = int(ev.sum()) * 17
    key = (fam, st, 'n_rows_evaluated'); fam_rows[key] = fam_rows.get(key, 0) + nrows_ev
    key = (fam, 'all', 'n_rows_evaluated'); fam_rows[key] = fam_rows.get(key, 0) + nrows_ev
    if fam == 'lead_braking':
        lb.append(dict(set=st, run=meta['run'], di=di, ri=ri, m=m[di, ri], age=z['prim_age'][di], miss=z['prim_miss'][di],
                       k=z['k'][di]))
fams = sorted({k[0] for k in fam_rows if len(k) == 2})
for fam in fams:
    doc['R20'][fam] = {}
    for st in ('all', 'tuning', 'fit'):
        if (fam, st) not in fam_rows:
            continue
        m = np.concatenate(fam_rows[(fam, st)])
        med = float(np.median(m))
        off = np.abs(m / med - 1.) > 0.05
        doc['R20'][fam][st] = dict(runs=(sum(v for k, v in nruns.items() if k[0] == fam) if st == 'all' else nruns.get((fam, st), 0)),
                                   rows=int(m.size), rows_evaluated=int(fam_rows[(fam, st, 'n_rows_evaluated')]),
                                   median_margin_ratio=med, off5_share=float(off.mean()), off5_n=int(off.sum()),
                                   within5_share=float(1. - off.mean()),
                                   pct_1_5_25_50_75_95_99=[float(x) for x in np.percentile(m, [1, 5, 25, 50, 75, 95, 99])])
ref = dict(lead_braking_all=(152264, 1.1029, 1127), stopped_all=(121685, 1.1027, 1542), cutin_all=(90227, 1.1025, 128),
           benign_all=(40120, 1.0927, 15868), pedestrian_crossing_all=(157972, 0.8826, 144536),
           vehicle_crossing_all=(42122, 0.9146, 40398))
chk = {}
for k, (rows, med, off) in ref.items():
    fam = k[:-4]; e = doc['R20'][fam]['all']
    chk[k] = dict(rows_equal=bool(e['rows'] == rows), median_equal_4dp=bool(round(e['median_margin_ratio'], 4) == med),
                  off5_n_equal=bool(e['off5_n'] == off))
doc['R20']['recount_against_lead_peek_gateR_ratios_v02_out'] = chk

# ------------------------------------------------------------------------------------------------ R19 and S9 (lead braking)
allm = np.concatenate([x['m'] for x in lb]); med_lb = float(np.median(allm))
EDGES = [0., 0.5, 1., 2., 4., 1e9]
BLAB = ['[0, 0.5)', '[0.5, 1)', '[1, 2)', '[2, 4)', '>= 4']


def band_table(recs):
    out = []
    age = np.concatenate([x['age'] for x in recs]); m = np.concatenate([x['m'] for x in recs])
    off = np.abs(m / med_lb - 1.) > 0.05
    for i, lab in enumerate(BLAB):
        s = (age >= EDGES[i]) & (age < EDGES[i + 1])
        out.append(dict(track_age_s=lab, rows=int(s.sum()), off5_n=int((off & s).sum()),
                        off5_share=float((off & s).sum() / s.sum()) if s.any() else None,
                        median_m=float(np.median(m[s])) if s.any() else None))
    return out


doc['R19']['lead_braking_median_margin_ratio'] = med_lb
doc['R19']['ratio_by_track_age_all55'] = band_table(lb)
doc['R19']['ratio_by_track_age_fit35'] = band_table([x for x in lb if x['set'] == 'fit'])
# evaluated decisions of the 35 evaluation runs by track age, misses, re-initialisations
runs = C.load_runs()
age = np.concatenate([r['prim_age'][r['ev']] for r in runs]); miss = np.concatenate([r['prim_miss'][r['ev']] for r in runs])
doc['R19']['evaluated_decisions_fit35'] = dict(
    n=int(age.size), by_track_age=[dict(track_age_s=lab, n=int(((age >= EDGES[i]) & (age < EDGES[i + 1])).sum()))
                                    for i, lab in enumerate(BLAB)],
    by_misses={str(int(v)): int(c) for v, c in zip(*np.unique(miss, return_counts=True))},
    min_track_age_s=float(age.min()),
    age_drops_in_stored_decisions=[dict(run=r['run'], n=int((np.diff(r['prim_age']) < 0).sum())) for r in runs
                                   if (np.diff(r['prim_age']) < 0).any()],
    stored_decisions_with_track_younger_than_4s=int(sum(int((r['prim_age'] < 4.).sum()) for r in runs)),
    stored_not_evaluated=int(sum(int((~r['ev']).sum()) for r in runs)))
# the 3 s room and D(N, F0) on evaluated decisions with a lead track younger than 4 s
for r in runs:
    r['masks_young'] = (r['ev'] & (r['prim_age'] < 4.), r['ev'] & (r['prim_age'] >= 4.))
X = C.tables(runs, ('W1',), ['F0', 'E', 'O', 'N', 'NA'], masks_key='masks_young')
pts = C.points(X, ['E', 'O', 'N', 'NA'], pops=range(2))
for i, nm in enumerate(['track_younger_than_4s', 'track_4s_or_older']):
    pe = pts[i]; n = pe['n']
    doc['R19'][nm] = dict(n=n, denE=pe['denE'], den0=pe['D']['O'], den0_dec_eq=L.dec_eq(pe['D']['O'], n) if n else None,
                          denE_dec_eq=L.dec_eq(pe['denE'], n) if n else None,
                          D_N_dec_eq=L.dec_eq(pe['D']['N'], n) if n else None, D_NA_dec_eq=L.dec_eq(pe['D']['NA'], n) if n else None)

# ------------------------------------------------------------------------------------------------ S9: the rows outside the band
off_rows = []
ph_of = {r['run']: r['ph'] for r in runs}
by_run = {}; by_set = {}; by_phase = {}; mvals = []
for x in lb:
    off = np.abs(x['m'] / med_lb - 1.) > 0.05
    if not off.any():
        continue
    by_run[x['run']] = int(off.sum()); by_set[x['set']] = by_set.get(x['set'], 0) + int(off.sum())
    mvals.append(x['m'][off])
    if x['run'] in ph_of:
        for p in ph_of[x['run']][x['di'][off]]:
            by_phase[int(p)] = by_phase.get(int(p), 0) + 1
    off_rows.append(dict(run=x['run'], set=x['set'], n=int(off.sum()), decisions=int(np.unique(x['di'][off]).size),
                         track_age_min=float(x['age'][off].min()), track_age_max=float(x['age'][off].max()),
                         misses=sorted({int(v) for v in x['miss'][off]}), m_min=float(x['m'][off].min()), m_max=float(x['m'][off].max()),
                         k_min=int(x['k'][off].min()), k_max=int(x['k'][off].max())))
mv = np.concatenate(mvals)
hist, edges = np.histogram(mv, bins=[0., 0.5, 0.8, 0.95 * med_lb, 1.05 * med_lb, 1.2, 1.4, 1.6, 1.8, 2.0, 3.0, 1e9])
doc['S9'] = dict(n_off=int(mv.size), by_set=by_set, n_runs_with_off_rows=len(by_run),
                 by_phase_fit_only={('phase%d' % p): n for p, n in sorted(by_phase.items())},
                 m_histogram=[dict(lo=float(edges[i]), hi=float(edges[i + 1]), n=int(hist[i])) for i in range(len(hist))],
                 per_run=sorted(off_rows, key=lambda d: -d['n'])[:25], share_in_top5_runs=float(sum(sorted(by_run.values())[-5:]) / mv.size))
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
OUT.write_text(C.jdump(doc), encoding='utf-8')
print(C.jdump({k: doc[k] for k in ('R20',)})[:6000])
print(C.jdump(doc['R19'])[:5000])
print(C.jdump(doc['S9'])[:5000])
