"""Package F (revision v13): the export for package A, out\\A_EXPORT_F.json, in the format of RESULTS_INTERFACE_v13.md section 1.
New file, 19 Nov 2026 (Claude Opus 5.5). Reads only F's own outputs: out\\F_HORIZON_RULE_v01.json, out\\F_HELDOUT_v01.json,
out\\F_HELDOUT_BOOT_v01.npz (every resample array), out\\F_DETECTOR_FINGERPRINT_v01.json. Computes no new quantity: points come
from the reference path (trk_score_v01.rr_gl) in F_HELDOUT, intervals are percentiles of the stored resamples.
  * hypothesis statistics (R, RR_N, IMM.r, IMM.c, IMM.eff): interval at the level of A10 section 2.6, with X.level and X.cal;
    their decision-equivalents (X.dec.ci) at the same level;
  * descriptive shares (TG, E5, E5mP, PO25/50/75) and the in-path population: 95% percentile intervals;
  * F.RR_CK3 and F.RR_AM are not exported (not computed on nuScenes; departure in STATUS.md and in "deviations");
  * if F_HELDOUT does not exist: F.status "design_only" (A10 section 0.5) with the design-split values only; if the horizon rule
    stopped F: "no_room_design".
Counts: F.n_design = design-split scenes (700), F.n_heldout = held-out scenes (150), F.n_dec = held-out evaluated decisions at the
primary horizon (all-decisions population). Status keys F.H0/F.H1/F.H2 are left to package A (optional; A recomputes them); F's
own verdicts are written beside the values under "own_statuses".
20 Nov 2026 (clearance departure, notes\\F_DEPARTURE_CLEARANCE_v01.md): the values in force come from the v02 outputs
(F_HORIZON_RULE_v02.json, F_HELDOUT_v02.json, F_HELDOUT_BOOT_v02.npz); the pre-registered outcome under the clearance of record
(F_HORIZON_RULE_v01.json) is exported beside them as F.prereg.* (status, horizon sentence, design R at 3 s and 2 s with intervals),
with the descriptive removed-contact counts of F_CLEAR_V02_train_v01.json (F.design.removed.*) and the departure in "deviations".
If the author vetoes the departure, package A prints F.prereg.* (outcome (a)). `--outcome-a` exports outcome (a) as the values in
force (the coordinator's fallback if the departure is not recounted by 20 Nov 14:00 EST).
Usage: python -I f12_export_v01.py [--outcome-a]   (writes out\\A_EXPORT_F.json; refuses to overwrite)
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
import numpy as np                           # noqa: E402

OUTF = FC.OUT / 'A_EXPORT_F.json'
OUTCOME_A = '--outcome-a' in sys.argv
HYP = {'R': 'R', 'RR_N': 'RR_N', 'r_IMM': 'IMM.r', 'c_IMM': 'IMM.c', 'eff_IMM': 'IMM.eff'}

DEVIATIONS = [
    dict(item='True clearance of F (A10 sections 8.1 F-B and 11; departure file notes\\F_DEPARTURE_CLEARANCE_v01.md)',
         planned="clearance of record: minimum rectangle distance to every truth actor over the window (W1)",
         done="(actor, frame) pairs whose actor centre has a negative longitudinal coordinate in the ego frame are dropped; "
              "chosen by the coordinator on 19 Nov 2026 (23:58 EST) after the design-split horizon rule stopped F; pinned before any "
              "value under it; val unread at the time; the pre-registered outcome is exported as F.prereg.*",
         why="on the design split the stop came from rear-end contacts of the hard-brake fallback by replayed traffic, which does "
             "not react to the counterfactual brake (out\\F_ROOM_MECHANISM_T1_train_v01.json)"),
    dict(item='F sources CK3 and AM (A10 sections 8.2 and 11)', planned='RR_gl(CK3) and RR_gl(AM) on the held-out nuScenes scenes',
         done='not computed; F.RR_CK3 and F.RR_AM are absent (departure accepted by the coordinator, 19 Nov 2026, 19:25 EST)',
         why="The triggers need the filter's acceleration-sign history and a primary actor, which the real-log tracker does not "
             "provide."),
    dict(item='TG on nuScenes', planned='as of record', done='computed, descriptive only', why='see the CK3 item; reported for orderings with N'),
    dict(item="Package B's IMM (B1) on nuScenes", planned='frozen B1 tracker', done='frozen B1 with exact_trig=False',
         why='the correctly rounded trig functions exist only to reproduce Linux pod logs bit for bit; nuScenes has none'),
]


def lvl_name(level):
    return 'nominal95' if abs(level - 0.95) < 1e-12 else ('nominal99' if abs(level - 0.99) < 1e-12 else 'calibrated')


def pct_level(b, level):
    b = np.asarray(b, float); f = np.isfinite(b)
    a = (1. - level) / 2.
    return [float(x) for x in np.percentile(b[f], [100. * a, 100. * (1. - a)])] if f.any() else [float('nan'), float('nan')]


def main():
    if OUTF.exists():
        raise SystemExit('REFUSED: %s exists' % OUTF)
    hz1 = json.loads((FC.OUT / 'F_HORIZON_RULE_v01.json').read_text(encoding='utf-8'))
    dep_sha = FC.sha256_file(FC.F / 'notes' / 'F_DEPARTURE_CLEARANCE_v01.md')
    V = {'F.provenance': 'confirmed', 'F.n_design': hz1['horizons']['3 s']['n_scenes'],
         'F.prereg.status': 'no_room_design' if hz1['primary_horizon_s'] is None else 'room_design',
         'F.prereg.horizon': hz1.get('stop') if hz1['primary_horizon_s'] is None else hz1['primary_horizon_s']}
    for h in (3, 2):
        e1 = hz1['horizons']['%d s' % h]
        V['F.prereg.design.R%d' % h] = e1['R_gl_pp']['point']; V['F.prereg.design.R%d.ci' % h] = e1['R_gl_pp']['ci']
    extras = dict(prereg_share_nonpositive={k: v['share_resamples_nonpositive'] for k, v in hz1['horizons'].items()},
                  departure=dict(file='notes\\F_DEPARTURE_CLEARANCE_v01.md', sha256=dep_sha))
    if OUTCOME_A:
        # the coordinator's fallback (condition 6): the departure was not recounted by 20 Nov 14:00 EST; outcome (a) is in force
        hz = hz1
        V['F.clearance'] = 'of record'
        DEVIATIONS[0] = dict(DEVIATIONS[0], done='not applied: the departure was not recounted by 20 Nov 2026 14:00 EST; outcome (a) '
                                                 'is in force (F.prereg.* = the values in force)')
    else:
        hz = json.loads((FC.OUT / 'F_HORIZON_RULE_v02.json').read_text(encoding='utf-8'))
        if hz['clearance']['version'] != 'v02' or hz['clearance']['sha256'] != dep_sha:
            raise RuntimeError('the v02 horizon output does not carry the pinned departure file')
        V['F.clearance'] = 'departure'
        rm = json.loads((FC.OUT / 'F_CLEAR_V02_train_v01.json').read_text(encoding='utf-8'))
        if not rm['checks_passed']:
            raise RuntimeError('clear_v02 checks did not pass')
        for h in (3, 2):
            g = rm['g1_counts']['%d s' % h]
            for src in ('F0', 'E'):
                V['F.design.removed%d.%s' % (h, src)] = g[src]['removed']
        extras.update(design_share_nonpositive={k: v['share_resamples_nonpositive'] for k, v in hz['horizons'].items()},
                      design_removed_contacts_g1=rm['g1_counts'])
    for h in (3, 2):
        e = hz['horizons']['%d s' % h]
        V['F.design.R%d' % h] = e['R_gl_pp']['point']; V['F.design.R%d.ci' % h] = e['R_gl_pp']['ci']
    extras['design_n_evaluated'] = {k: v['n_evaluated'] for k, v in hz['horizons'].items()}
    own = {}
    hfile = FC.OUT / 'F_HELDOUT_v02.json'
    if hz['primary_horizon_s'] is None:
        V['F.status'] = 'no_room_design'
        V['F.horizon'] = hz.get('stop')
    elif not hfile.exists():
        V['F.status'] = 'design_only'
        V['F.horizon'] = hz['primary_horizon_s']
    else:
        FC.require_split('val')
        H = json.loads(hfile.read_text(encoding='utf-8'))
        B = np.load(FC.OUT / 'F_HELDOUT_BOOT_v02.npz')
        if H['horizon_s'] != hz['primary_horizon_s']:
            raise RuntimeError('horizon mismatch')
        if H['clearance'] != hz['clearance']:
            raise RuntimeError('held-out and horizon outputs use different clearances')
        V['F.status'] = 'heldout'
        V['F.horizon'] = H['horizon_s']
        V['F.n_heldout'] = H['n_scenes']
        A = H['populations']['all']; P = H['populations']['inpath']
        V['F.n_dec'] = int(round(A['n']))
        cal = H['calibration']
        pts = {'R': A['T1']['R_pp'], 'RR_N': A['T1']['RR_N'], 'r_IMM': A['IMM']['RR_N_IMM'], 'c_IMM': A['IMM']['c_IMM'],
               'eff_IMM': (A['IMM']['RR_N_IMM'] / A['IMM']['c_IMM']) if A['IMM']['c_IMM'] not in (0, None) else float('nan')}
        dec_pts = {'R': A['T1']['R_deceq'], 'RR_N': A['T1']['D_N_deceq'], 'r_IMM': A['IMM']['D_N_IMM_deceq'], 'c_IMM': A['IMM']['D_E5x_deceq']}
        for s, key in HYP.items():
            lev = cal[s]['level']
            V['F.' + key] = pts[s]
            V['F.' + key + '.ci'] = cal[s]['ci']
            V['F.' + key + '.level'] = lev
            V['F.' + key + '.cal'] = lvl_name(lev)
            if s in dec_pts:
                V['F.' + key + '.dec'] = dec_pts[s]
                V['F.' + key + '.dec.ci'] = pct_level(B['all__' + key + '.dec'], lev)
            if not np.allclose(cal[s]['point'], pts[s], rtol=1e-9, atol=1e-12, equal_nan=True):
                raise RuntimeError('fast and reference points differ for %s' % s)
        V['F.R.nonpos_share'] = A['share_R_nonpositive']
        V['F.IMM.within5'] = H['ratio_IMM']['share_within_5pct']
        D = A['descriptive']
        for a in ('TG', 'E5', 'E5mP'):
            V['F.RR_' + a] = D['RR_' + a]['point']; V['F.RR_' + a + '.ci'] = D['RR_' + a]['ci']
            V['F.RR_' + a + '.dec'] = D['RR_' + a]['D_deceq']; V['F.RR_' + a + '.dec.ci'] = D['RR_' + a]['D_deceq_ci']
        for a in ('PO25', 'PO50', 'PO75'):
            V['F.' + a] = D['RR_' + a]['point']; V['F.' + a + '.ci'] = D['RR_' + a]['ci']
            V['F.' + a + '.dec'] = D['RR_' + a]['D_deceq']; V['F.' + a + '.dec.ci'] = D['RR_' + a]['D_deceq_ci']
        V['F.inpath.R'] = P['T1']['R_pp']; V['F.inpath.R.ci'] = P['boot']['R']['ci']
        V['F.inpath.RR_N'] = P['T1']['RR_N']; V['F.inpath.RR_N.ci'] = P['boot']['RR_N']['ci']
        V['F.inpath.RR_N.dec'] = P['T1']['D_N_deceq']; V['F.inpath.RR_N.dec.ci'] = P['boot']['RR_N.dec']['ci']
        own = {k: v for k, v in H['hypotheses'].items()}
        extras.update(heldout_n_evaluated_inpath=P['n'], IMM_R_pp=A['IMM']['R_pp'], IMM_ratio=H['ratio_IMM'], T1_ratio=H.get('ratio_T1'),
                      second_inner_seed_run=H.get('second_inner_seed_run'))
        fp = FC.OUT / 'F_DETECTOR_FINGERPRINT_v01.json'
        if fp.exists():
            f = json.loads(fp.read_text(encoding='utf-8'))
            extras['detector_val_NDS'] = f['nd_score']; extras['detector_val_mAP'] = f['mean_ap']
            extras['detector_NDS_reference'] = 0.685
    V['deviations'] = DEVIATIONS
    doc = dict(package='F', written=FC.clock(), program='f12_export_v01.py', program_sha256=FC.sha256_file(pathlib.Path(__file__)),
               lock2_sha256=FC.sha256_file(FC.LOCK2) if FC.LOCK2.exists() else None, values=V, own_statuses=own, extras=extras)
    OUTF.write_text(FC.jdump(doc), encoding='utf-8')
    print('WROTE', OUTF, len(V), 'values; status', V['F.status'])


if __name__ == '__main__':
    main()
