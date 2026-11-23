"""Package E's export for package A (work\\E_closedloop\\out\\A_EXPORT_E.json), in the format of the shared note
RESULTS_INTERFACE_v13.md (session A): {"package": "E", "written", "program", "program_sha256", "lock2_sha256", "values": {...}}.
Unrounded values; intervals as [lo, hi]; contact shares and errors as fractions.

v02 (20 Nov 2026, ~01:15 EST, before any E3 / E3b value; LOCK_A10_2 does not exist): v01 checked against the interface's E key
list (regenerated 19 Nov 21:15) and the text's captions (Table IV, Table S9); changes:
  - per-arm summaries follow the captions: contact share; MEDIAN impact speed (runs with contact); mean time lost (runs
    without contact); mean rest gap; MEDIAN peak deceleration; MEDIAN RMS jerk; fallback = share of decisions in full braking,
    pooled over the arm's decisions (sum of full-braking decisions / sum of decisions). v01 used means throughout.
  - caution keys under the interface's names: E3.F0.<lev>.caution (F0's open-loop caution at g_L, %), E3.PS.<lev>.caution
    (PS's design caution, %); v01 wrote them as E3.F0.<lev>.oc_caution_pct / E3.PS.design_caution_pct.
  - E3.NIMM.dropped (bool, read by A): False when the IMM pair ran in closed loop (both IMM arms have valid E3 runs).
  - E3.PS.caution_matched = False is kept (the coordinator's PS caveat; LOCK_A10_2b_NOTE_v01.txt).

Keys (A's list; RESULTS_INTERFACE_v13.md section 3, E):
  E.status                          'ran' | 'stopped_brake' | 'stopped_other'
  E1.attempts, E1.v<5|10|15>.dist / .model / .err (|dist/model - 1|), E1.maxerr
  E2.g<0|0_25|1|4|16|64>.contact, E2.g_lo, E2.g_hi, E2.low_power
  E3.<arm>.<lev>.contact / .vimp / .tlost / .restgap / .peakdec / .jerk / .fallback (summaries above, over the arm's valid runs)
  E3.<arm>.<lev>.dc / .dc.ci (contact difference vs F0, or NIMM vs F0IMM) and .dt / .dt.ci (time lost difference)
  E3.F0.<lev>.caution, E3.PS.<lev>.caution, E3.NIMM.dropped, E3.n_cases
  E3b.<const|mild|stopgo>.<arm>.dc / .dc.ci / .dt / .dt.ci, E3b.n_cases, EH1, EH2, EH3
Usage: python -I -B e_export_v02.py --status ran --e1 E1_VERDICT.json [--e1-attempts N] [--matched MATCHED.json]
          [--e3-outcomes OUTCOMES_E3.json --e3b-outcomes OUTCOMES_E3B.json --results E3_RESULTS.json] [--out PATH]
"""
import argparse, datetime, hashlib, json, math, pathlib, statistics

E = pathlib.Path(__file__).resolve().parents[1]
LOCK2 = E.parents[1] / 'LOCK_A10_2.txt'
ARM = {'E_N': 'N', 'E_CK3': 'CK3', 'E_TG': 'TG', 'E_PS': 'PS', 'E_N_IMM': 'NIMM', 'E_F0': 'F0', 'E_F0_IMM': 'F0IMM'}
VAR = {'constant': 'const', 'mild_braking': 'mild', 'stop_and_go': 'stopgo'}
MEAN = {'contact': 'contact', 'tlost': 'time_lost_s', 'restgap': 'rest_gap_m'}
MEDIAN = {'vimp': 'impact_speed_mps', 'peakdec': 'peak_decel_mps2', 'jerk': 'rms_jerk_mps3'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def gkey(g):
    return 'g' + ('%g' % g).replace('.', '_')


def defined(xs):
    return [float(x) for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]


def mean(xs):
    xs = defined(xs); return sum(xs) / len(xs) if xs else None


def median(xs):
    xs = defined(xs); return float(statistics.median(xs)) if xs else None


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
        for lev in ('lo', 'hi'):
            v[f'E3.F0.{lev}.caution'] = m['settings'][lev]['F0_caution_pct']
            v[f'E3.PS.{lev}.caution'] = m['settings'][lev]['arms']['PS']['design_caution_pct']
        # PS is not caution-matched (work\locks\LOCK_A10_2b_NOTE_v01.txt)
        v['E3.PS.caution_matched'] = False
    if a.e3_outcomes:
        rows = json.loads(pathlib.Path(a.e3_outcomes).read_text(encoding='utf-8'))['runs']
        v['E3.n_cases'] = len({r['case'] for r in rows})
        for arm, ak in ARM.items():
            for lev in ('lo', 'hi'):
                sel = [r for r in rows if r['arm'] == arm and r['level'] == lev and r['valid']]
                if not sel: continue
                for k, ok in MEAN.items():
                    v[f'E3.{ak}.{lev}.{k}'] = mean([r['outcomes'][ok] for r in sel])
                for k, ok in MEDIAN.items():
                    v[f'E3.{ak}.{lev}.{k}'] = median([r['outcomes'][ok] for r in sel])
                n_dec = sum(int(r['outcomes']['decisions'] or 0) for r in sel)
                v[f'E3.{ak}.{lev}.fallback'] = (sum(int(r['outcomes']['fallback_decisions'] or 0) for r in sel) / n_dec) if n_dec else None
        v['E3.NIMM.dropped'] = not (any(r['arm'] == 'E_N_IMM' and r['valid'] for r in rows) and any(r['arm'] == 'E_F0_IMM' and r['valid'] for r in rows))
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
        if isinstance(x, float) and not math.isfinite(x): return None      # undefined (e.g. fewer than 2 pairs)
        return x
    v = {k: clean(x) for k, x in v.items()}
    doc = dict(package='E', written=datetime.datetime.now().astimezone().isoformat(), program='e_export_v02.py', program_sha256=sha(__file__),
               lock2_sha256=sha(LOCK2) if LOCK2.exists() else None, values=v)
    pathlib.Path(a.out).write_text(json.dumps(doc, indent=1, allow_nan=False), encoding='utf-8')
    print(len(v), 'values ->', a.out)


if __name__ == '__main__':
    main()
