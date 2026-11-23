"""E0 laptop check of E_PS's online phase (A10 2.4) on the 35 old evaluation runs, against the stored a9_4a lead-state
arrays (revision_v12\\analysis\\out\\lead): lead track (truth-matched there, online in-path rule here), vhat, ahat_long, and the
estimated phase with thresholds -1.0 (primary), -0.5, -2.0, as a9_3_phase_scale_cv_v02.py forms it from those arrays.
Writes tests\\out\\TEST_PS_PHASE_v01.json.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import json, math, pathlib, sys
import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
PK = E / 'packets' / 'dev_packet_e_v01' / 'claude_smoke_v01'
PRJ = pathlib.Path(r'<library folder>')
V12 = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out')
sys.path.insert(0, str(PK)); sys.dont_write_bytecode = True
import e_sources_v01 as es     # noqa: E402


def jl(p):
    with open(p, encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def events_prefix(events, i):
    out = []
    for e in events:
        if 'timestamp' in e and int(e['timestamp']) > i: break
        out.append(e)
    return out


def stored_phase(zl, thr):
    vh = zl['vhat']; ah = zl['ahat_long']; fd = zl['lead_found'].astype(bool)
    ph = np.zeros(vh.size, np.int64)
    ph[fd & (vh > 0.5) & np.isfinite(ah) & (ah <= thr)] = 1; ph[fd & (vh <= 0.5)] = 2
    return ph


def main():
    tot = dict(decisions=0, lead_found_both=0, lead_found_stored_only=0, lead_found_online_only=0, same_track=0,
               vhat_maxabs=0., ahat_maxabs=0., ahat_nan_mismatch=0)
    agree = {thr: [0, 0] for thr in (-1.0, -0.5, -2.0)}; conf = np.zeros((3, 3), int); runs = []
    for rd in sorted((PRJ / '07_fit_runs' / 'archives').glob('p1b_fit_finite_*')):
        if not (V12 / 'lead' / (rd.name + '.npz')).exists(): continue
        cap = next((rd / 'x' / rd.name / 'capture').iterdir())
        zl = np.load(V12 / 'lead' / (rd.name + '.npz'), allow_pickle=False)
        det = jl(cap / 'detections.jsonl'); ev = jl(cap / 'filter_events.jsonl')
        hist = es.OnlineHist(); di = 0
        decs = [fr['execution']['new_decision'] for fr in jl(cap / 'frames.jsonl')
                if fr.get('execution') and fr['execution'].get('new_decision') and fr['execution']['new_decision']['mode'] == 'assessment']
        assert [d['tick'] for d in decs] == list(zl['k'])
        mine = {thr: [] for thr in agree}; r_same = 0
        for i, d in enumerate(decs):
            while di < len(det) and det[di]['k'] <= d['tick']:
                hist.update(det[di]['tracks'], events_prefix(ev, di)); di += 1
            for thr in agree:
                ph, info = es.phase_of(d['actors'], d['now'], hist, thr)
                mine[thr].append(ph)
            fd = bool(zl['lead_found'][i]); on = info.get('lead') is not None
            tot['decisions'] += 1
            if fd and on:
                tot['lead_found_both'] += 1
                if int(zl['track_id'][i]) == info['track_id']:
                    tot['same_track'] += 1; r_same += 1
                    tot['vhat_maxabs'] = max(tot['vhat_maxabs'], abs(float(zl['vhat'][i]) - info['vhat']))
                    a1, a2 = float(zl['ahat_long'][i]), info['ahat_long']
                    if math.isfinite(a1) and math.isfinite(a2): tot['ahat_maxabs'] = max(tot['ahat_maxabs'], abs(a1 - a2))
                    elif math.isfinite(a1) != math.isfinite(a2): tot['ahat_nan_mismatch'] += 1
            elif fd: tot['lead_found_stored_only'] += 1
            elif on: tot['lead_found_online_only'] += 1
        for thr in agree:
            sp = stored_phase(zl, thr); mp = np.array(mine[thr])
            agree[thr][0] += int((sp == mp).sum()); agree[thr][1] += sp.size
            if thr == -1.0:
                for a, b in zip(sp, mp): conf[a, b] += 1
        runs.append(dict(run=rd.name, decisions=len(decs), same_track=r_same, agree_m1=int((stored_phase(zl, -1.0) == np.array(mine[-1.0])).sum())))
    out = dict(schema='E_TEST_PS_PHASE_V01', totals=tot, phase_agreement={str(k): v for k, v in agree.items()},
               confusion_thr_m1_stored_rows_online_cols=conf.tolist(), runs=runs)
    (E / 'tests' / 'out' / 'TEST_PS_PHASE_v01.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    print(json.dumps({k: v for k, v in out.items() if k != 'runs'}, indent=1))


if __name__ == '__main__':
    main()
