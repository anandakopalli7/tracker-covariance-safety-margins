"""Revision v11, post hoc checks S13 and S14 (ARS review of draft v10). New file, 18 Nov 2026. Descriptive; AMENDMENT_08.

S13  Replay identity on the 35 evaluation runs. For every stored decision (assessment mode) the candidate rows are rebuilt with
     the planner library (finite_primitive.build_library) and the planner's own chooser is run with the logged margin constants
     (consumer.choose(rows, alpha, beta, Diagnostics(), steer)); the result is compared with the logged output: candidate
     index, target pair, fallback flag and the wire bytes. These are the comparisons of ol_extract_v01.process_run (lines
     105-110), which the paper reports for the tuning runs only. For the evaluation runs the recording arm is 'native', so the
     rows are used as built (no unit-variance replacement).
S14  The five short runs (they ended at a contact): evaluated decisions, decisions in which the NIS-inflated covariance changes
     the tracker covariance's critical values (any of the 17 rows), per run and in total, beside the totals of all 35 runs.
Usage: python -B -X utf8 rev_i_replay_shortruns_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
OJ = P / '11_ojits'
sys.path.insert(0, str(OJ / 'A5' / 'code'))
import oxsb_replan_v03 as rp                 # noqa: E402  (only for the import chain: planner library and loaders)
c3 = rp.c3; sb = rp.sb; gc = rp.gc; rx = rp.rx
consumer = rp.consumer; finite_primitive = rp.finite_primitive

OUT = HERE / 'out' / 'REV_I_REPLAY_SHORTRUNS_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t0 = time.time()
FIT = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
A4X = OJ / 'A4' / 'fit' / 'extract'
rep = []; s14 = []
for run in FIT:
    Lr = rx.load_run('fit', run, sb.YAW); cap = Lr['cap']
    z = np.load(c3.STORED / (run + '.npz'), allow_pickle=False)
    x = np.load(A4X / (run + '.npz'), allow_pickle=False)
    decs = list(gc.decisions(cap))
    n = 0; ok = 0; bad = dict(candidate=0, targets=0, fallback=0, wire=0); nfb = 0
    for k, dec in decs:
        ms = dec['model_state']; lo = dec['output']
        rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'], dec['actors'],
                                              dec['ego_length'], dec['ego_width'], dec['now'], consumer.Diagnostics())
        out = consumer.choose(rows, dec['alpha'], dec['beta'], consumer.Diagnostics(), dec['steer'])
        c = dict(candidate=out['candidate'] == lo['candidate'], targets=list(out['targets']) == list(lo['targets']),
                 fallback=out['fallback'] == lo['fallback'], wire=out['wire'].hex() == lo['wire'])
        n += 1; ok += int(all(c.values())); nfb += int(bool(lo['fallback']))
        for kk, v in c.items():
            bad[kk] += int(not v)
    rep.append(dict(run=run, decisions=n, reproduced=ok, differing=bad, logged_fallbacks=nfb, arm=Lr['arm']))
    ev = z['evaluated'].astype(bool)
    cN = z['cN']; cNA = x['cNA']
    ch = ~((cN == cNA) | (np.isnan(cN) & np.isnan(cNA)))
    s14.append(dict(run=run, evaluated=int(ev.sum()), na_changed_decisions=int((ch.any(axis=1) & ev).sum()),
                    contact_k=json.loads(str(z['meta'])).get('contact_k')))
    print('%s: %d / %d decisions reproduced (%.0f s)' % (run, ok, n, time.time() - t0), flush=True)
short = [r for r in s14 if r['evaluated'] < 100]
doc = dict(code='rev_i_replay_shortruns_v01.py', written=time.strftime('%Y-%m-%d %H:%M:%S'), seconds=time.time() - t0,
           S13=dict(runs=rep, decisions=int(sum(r['decisions'] for r in rep)), reproduced=int(sum(r['reproduced'] for r in rep)),
                    arms=sorted({r['arm'] for r in rep})),
           S14=dict(runs=s14, short_runs=short, evaluated_in_short_runs=int(sum(r['evaluated'] for r in short)),
                    na_changed_in_short_runs=int(sum(r['na_changed_decisions'] for r in short)),
                    na_changed_all=int(sum(r['na_changed_decisions'] for r in s14)),
                    runs_with_na_change=int(sum(1 for r in s14 if r['na_changed_decisions'] > 0)),
                    evaluated_all=int(sum(r['evaluated'] for r in s14))))
OUT.write_text(json.dumps(doc, indent=1), encoding='utf-8')
print(json.dumps(dict(S13=dict(decisions=doc['S13']['decisions'], reproduced=doc['S13']['reproduced']), S14={k: v for k, v in doc['S14'].items() if k != 'runs'}), indent=1))
