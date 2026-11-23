"""Package E's export for package A (work\\E_closedloop\\out\\A_EXPORT_E.json), in the format of the shared note
RESULTS_INTERFACE_v13.md (session A): {"package": "E", "written", "program", "program_sha256", "lock2_sha256", "values": {...}}.
Unrounded values; intervals as [lo, hi]; contact shares and errors as fractions.

Keys (A's list; copy in out\\A_INTERFACE_E_KEYS_copy.md):
  E.status                          'ran' | 'stopped_brake' | 'stopped_other'
  E1.attempts, E1.v<5|10|15>.dist / .model / .err (|dist/model - 1|), E1.maxerr
  E2.g<0|0_25|1|4|16|64>.contact, E2.g_lo, E2.g_hi, E2.low_power
  E3.<arm>.<lev>.contact / .fallback / .jerk / .peakdec / .restgap / .tlost / .vimp   (arm-level means over the arm's valid runs)
  E3.<arm>.<lev>.dc / .dc.ci (contact difference vs F0, or N_IMM vs F0_IMM) and .dt / .dt.ci (time lost difference)
  E3.n_cases, E3b.<const|mild|stopgo>.<arm>.dc / .dc.ci / .dt / .dt.ci, E3b.n_cases, EH1, EH2, EH3
Usage: python -I -B e_export_v01.py --status ran --e1 E1_VERDICT.json [--e1-attempts N] [--matched MATCHED.json]
          [--e3-outcomes OUTCOMES_E3.json --e3b-outcomes OUTCOMES_E3B.json --results E3_RESULTS.json] [--out PATH] [--recount]
"""
import argparse, datetime, hashlib, json, math, pathlib

E = pathlib.Path(__file__).resolve().parents[1]
LOCK2 = E.parents[1] / 'LOCK_A10_2.txt'
ARM = {'E_N': 'N', 'E_CK3': 'CK3', 'E_TG': 'TG', 'E_PS': 'PS', 'E_N_IMM': 'NIMM', 'E_F0': 'F0', 'E_F0_IMM': 'F0IMM'}
VAR = {'constant': 'const', 'mild_braking': 'mild', 'stop_and_go': 'stopgo'}
DESC = {'contact': 'contact', 'fallback': 'fallback_share', 'jerk': 'rms_jerk_mps3', 'peakdec': 'peak_decel_mps2',
        'restgap': 'rest_gap_m', 'tlost': 'time_lost_s', 'vimp': 'impact_speed_mps'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def gkey(g):
    return 'g' + ('%g' % g).replace('.', '_')


def mean(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return sum(xs) / len(xs) if xs else None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--status', required=True, choices=('ran', 'stopped_brake', 'stopped_other'))
    ap.add_argument('--e1'); ap.add_argument('--e1-attempts', type=int, default=1); ap.add_argument('--matched')
    ap.add_argument('--e3-outcomes'); ap.add_argument('--e3b-outcomes'); ap.add_argument('--results'); ap.add_argument('--out', default=str(E / 'out' / 'A_EXPORT_E.json'))
    a = ap.parse_args()
    v = {'E.status': a.status}
    if a.e1:
        e1 = json.loads(pathlib.Path(a.e1).read_text(encoding='utf-8'))
        v['E1.attempts'] = a.e1_attempts; errs = []
        for r in e1['runs']:
            sp = int(round(r['desired_mps']))
            if 'stop_dist_m' in r:
                err = abs(r['ratio_real_to_model'] - 1.); errs.append(err)
                v[f'E1.v{sp}.dist'] = r['stop_dist_m']; v[f'E1.v{sp}.model'] = r['model_dist_m']; v[f'E1.v{sp}.err'] = err
        if errs: v['E1.maxerr'] = max(errs)
    if a.matched:
        m = json.loads(pathlib.Path(a.matched).read_text(encoding='utf-8'))
        for g, ent in m['levels']['per_g'].items():
            v[f'E2.{gkey(float(g))}.contact'] = ent['share']
        v['E2.g_lo'] = m['levels']['g_lo']; v['E2.g_hi'] = m['levels']['g_hi']; v['E2.low_power'] = bool(m['levels']['low_power'])
        # PS is not caution-matched (work\locks\LOCK_A10_2b_NOTE_v01.txt): its design caution against F0's open-loop caution
        v['E3.PS.caution_matched'] = False
        v['E3.PS.design_caution_pct'] = m['settings']['lo']['arms']['PS']['design_caution_pct']
        v['E3.F0.lo.oc_caution_pct'] = m['settings']['lo']['F0_caution_pct']; v['E3.F0.hi.oc_caution_pct'] = m['settings']['hi']['F0_caution_pct']
    if a.e3_outcomes:
        rows = json.loads(pathlib.Path(a.e3_outcomes).read_text(encoding='utf-8'))['runs']
        v['E3.n_cases'] = len({r['case'] for r in rows})
        for arm, ak in ARM.items():
            for lev in ('lo', 'hi'):
                sel = [r for r in rows if r['arm'] == arm and r['level'] == lev and r['valid']]
                if not sel: continue
                for k, ok in DESC.items():
                    v[f'E3.{ak}.{lev}.{k}'] = mean([r['outcomes'][ok] for r in sel])
    if a.e3b_outcomes:
        rows = json.loads(pathlib.Path(a.e3b_outcomes).read_text(encoding='utf-8'))['runs']
        v['E3b.n_cases'] = len({r['case'] for r in rows})
    if a.results:
        res = json.loads(pathlib.Path(a.results).read_text(encoding='utf-8'))
        for c in res['comparisons']:
            if c['arm'] == 'E_Z' or c['classification'] == 'no pairs': continue
            ak = ARM[c['arm']]
            pre = f'E3.{ak}.{c["level_arm"]}' if c['stage'] == 'E3' else f'E3b.{VAR[c["lead_variant"]]}.{ak}'
            v[pre + '.dc'] = c['contact']['diff']; v[pre + '.dc.ci'] = [c['contact']['lo'], c['contact']['hi']]
            v[pre + '.dt'] = c['time_lost']['mean']; v[pre + '.dt.ci'] = [c['time_lost']['lo'], c['time_lost']['hi']]
            if c.get('hypothesis'): v[c['hypothesis'].replace('-', '')] = c['classification']
    def clean(x):
        if isinstance(x, list): return [clean(y) for y in x]
        if isinstance(x, float) and not math.isfinite(x): return None      # undefined (e.g. no pairs without contact)
        return x
    v = {k: clean(x) for k, x in v.items()}
    doc = dict(package='E', written=datetime.datetime.now().astimezone().isoformat(), program='e_export_v01.py', program_sha256=sha(__file__),
               lock2_sha256=sha(LOCK2) if LOCK2.exists() else None, values=v)
    pathlib.Path(a.out).write_text(json.dumps(doc, indent=1, allow_nan=False), encoding='utf-8')
    print(len(v), 'values ->', a.out)


if __name__ == '__main__':
    main()
