"""Package F recount: the horizon rule (A10 8.3) under the clearance departure of 19 Nov 2026
(notes\\F_DEPARTURE_CLEARANCE_v01.md section 2), on the design split only. New file, 20 Nov 2026; fr_horizon_v01.py and its
output are unchanged (the pre-registered record). The only difference from v01: `clear` and `clear2` are read from
cache\\clear_v02\\train instead of the arrays (the recount scores them; it does not recompute them). One application: if there
is no room at 3 s or 2 s, F stops with no further variant.
Also, descriptive (F0 and E only, A10 8.6): removed-contact counts at margin scale 1 (K.removed_counts).
--variant NAME (synthetic only): read synth\\NAME instead of synth\\clear_v02.

The v01 text follows.
Package F recount: the horizon rule (A10 8.3), on the design split (nuScenes train scenes) only. New file, 19 Nov 2026.
Writer: Claude Fable 5.2 (independent second program; see fr_core_v01.py).

Computes ONLY R_gl = D_gl(E, F0) / 201 of T1 (CANMOT) at 3 s and at 2 s, with the 20,000 scene resamples of
default_rng(20261923) (scenes in sorted name order): point, 95% percentile interval, share of resamples with D <= 0.
Primary population: all evaluated decisions (it decides the rule); secondary: evaluated decisions with `inpath`.
Nothing else is computed on the design split (A10 8.6): the critical scales of N and TG and the IMM files are never read.

Usage: python -I fr_horizon_v01.py            (the real train arrays; needs all 700 files)
       python -I fr_horizon_v01.py --synth    (synthetic arrays of fr_synth_v01.py; output under synth\\out)
"""
import sys, time
sys.dont_write_bytecode = True
import numpy as np
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import fr_core_v01 as K
import fr_run_v01 as R

SYNTH = '--synth' in sys.argv
N_EXPECT = 700
KEYS = ['sweep', 'idx55', 'vbar', 'des', 'inpath', 'evaluated', 'evaluated2', 'clear', 'clear2', 'cF0', 'cE', 'cF0_2', 'cE_2']
VAR = sys.argv[sys.argv.index('--variant') + 1] if '--variant' in sys.argv else 'clear_v02'
if VAR != 'clear_v02' and not SYNTH:
    raise SystemExit('--variant is for synthetic arrays only')
OUTF = (K.HERE / 'synth' / 'out' / ('F_RECOUNT_HORIZON_synth_%s.json' % VAR)) if SYNTH else (K.HERE / 'F_RECOUNT_HORIZON_v02.json')


def main():
    if OUTF.exists() and not SYNTH:
        raise SystemExit('REFUSED: %s exists' % OUTF)
    t0 = time.time()
    names, scenes = K.load_split('T1', 'train', KEYS, root=(K.HERE / 'synth') if SYNTH else None)
    n = len(names)
    if not SYNTH and n != N_EXPECT:
        raise SystemExit('REFUSED: %d train array files, %d expected' % (n, N_EXPECT))
    old = scenes
    scenes = K.swap_clear_v02(names, old, 'train', root=(K.HERE / 'synth') if SYNTH else None, sub=VAR)
    print('%d scenes loaded, clearances from %s (%.0f s)' % (n, VAR, time.time() - t0), flush=True)
    W = K.primary_counts(n)
    doc = dict(code='fr_horizon_v02.py', clearance='departure: cache\\clear_v02 (actors behind the ego dropped)', writer='Claude Fable 5.2 (claude-fable-5-2), independent second program',
               amendment='AMENDMENT_10_v13.md 8.3', split='train (design)', tracker='T1', synthetic=SYNTH,
               n_scenes=n, first_scene=names[0], last_scene=names[-1],
               draw='default_rng(20261923).integers(0, n_scenes, (20000, n_scenes)), scenes in sorted name order',
               frontier='gridless step frontier, margin scales in [0, 1e3], 201 caution levels', horizons={})
    for h in (3, 2):
        suf = R.HKEYS[h]['suf']
        ent = dict(counts=R.counts(scenes, h),
                   removed_contacts_g1={x: K.removed_counts(old, scenes, 'c' + x + suf, R.HKEYS[h]['clear'], R.HKEYS[h]['ev'])
                                        for x in ('F0', 'E')})
        print('%d s removed contacts at g = 1: %s' % (h, ent['removed_contacts_g1']), flush=True)
        for pop in R.POPS:
            pk, info = R.build_pack(scenes, h, pop, [('F0', lambda k, z: z['cF0' + suf]), ('E', lambda k, z: z['cE' + suf])])
            pt = K.kernel2(np.ones((1, n)), *pk)[0]
            B = R.run(W, pk, label='%d s, %s' % (h, pop))
            e = dict(n_decisions=float(pt[0]), c0_pp=float(pt[1]), C_pp=float(pt[2]), D_gl_E_F0=float(pt[3]),
                     R_gl_pp=R.summ_room(B[:, 3], pt[3]), room_decision_equivalents=float(K.L.dec_eq(pt[3], pt[0])),
                     sources=info)
            ent[pop] = e
            print('%d s, %-6s: n %d  R_gl %.6f pp  95%% [%.6f, %.6f]  share D<=0 %.5f  (%.0f s)'
                  % (h, pop, pt[0], e['R_gl_pp']['point'], e['R_gl_pp']['ci95'][0], e['R_gl_pp']['ci95'][1],
                     e['R_gl_pp']['share_le0'], time.time() - t0), flush=True)
        doc['horizons']['%ds' % h] = ent
    lo3 = doc['horizons']['3s']['all']['R_gl_pp']['ci95'][0]; lo2 = doc['horizons']['2s']['all']['R_gl_pp']['ci95'][0]
    if lo3 > 0:
        rule = dict(primary_horizon_s=3, reason='the lower 95% end of D(E, F0) at 3 s is > 0 on the design split')
    elif lo2 > 0:
        rule = dict(primary_horizon_s=2, reason='the lower 95% end at 3 s is not > 0; at 2 s it is > 0')
    else:
        rule = dict(primary_horizon_s=None, reason=K.STOP_SENTENCE + ': F stops')
    doc['horizon_rule'] = rule
    doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t0
    OUTF.parent.mkdir(parents=True, exist_ok=True)
    if SYNTH:
        OUTF.write_text(K.jdump(doc), encoding='utf-8')
    else:
        K.write_once(OUTF, doc)
    print('horizon rule:', rule); print('written', OUTF)


if __name__ == '__main__':
    main()
