r"""v13 sprint step 0: flat export of the step-0 design data for package A (coordinator 21 Nov 13:50). New file, 21 Nov 2026 (Claude
Opus 5.5). COPIES values from out\step0\STEP0_CROSSING_v01.json; computes nothing. Keys (VC = vehicle crossing, PC = pedestrian
crossing): S0.<fam>.* on all stored runs, S0T.<fam>.* on the tuning runs only, S0.LB.R the lead-braking tuning reference (pp).
  n_runs, n_dec (evaluated decisions), R (pp) and R.ci (95%), R_deceq, RR_N and RR_N.ci, RR_E5N and RR_E5N.ci (95%),
  nobind (share of evaluated decisions with no binding F0 constraint), unsafe3s (share with any 3 s-unsafe row).
Writes out\step0\A_EXPORT_S0.json (+ _meta). Usage: python -I -B -X utf8 b_step0_export_v01.py
"""
import json, pathlib, hashlib, time
HERE = pathlib.Path(__file__).resolve().parents[1]
SRC = HERE / 'out' / 'step0' / 'STEP0_CROSSING_v01.json'
FAM = {'vehicle_crossing': 'VC', 'pedestrian_crossing': 'PC'}


def keys(f, pre):
    p = f['points']; I = f['intervals']; fl = f['flags']
    return {pre + 'n_runs': f['n_runs'], pre + 'n_dec': f['evaluated_decisions'], pre + 'R': p['R_pp'], pre + 'R.ci': I['R_pp']['0.95'],
            pre + 'R_deceq': p['R_deceq'], pre + 'RR_N': p['RR']['N'], pre + 'RR_N.ci': I['RR']['N']['0.95'],
            pre + 'RR_E5N': p['RR']['E5N'], pre + 'RR_E5N.ci': I['RR']['E5N']['0.95'],
            pre + 'nobind': fl['share_no_binding_constraint_F0'], pre + 'unsafe3s': fl['share_with_some_row_unsafe_3s']}


def main():
    d = json.loads(SRC.read_text(encoding='utf-8'))
    E = {}
    for fam, ab in FAM.items():
        E.update(keys(d['families'][fam], 'S0.%s.' % ab))
        E.update(keys(d['tuning_only'][fam], 'S0T.%s.' % ab))
    E['S0.LB.R'] = d['reference_lead_braking_tuning']['points']['R_pp']
    out = HERE / 'out' / 'step0' / 'A_EXPORT_S0.json'
    out.write_text(json.dumps(E, indent=1, default=float), encoding='utf-8')
    meta = dict(code='b_step0_export_v01.py', source=str(SRC.relative_to(HERE)), source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),
                status=d['status'], n_keys=len(E), written=time.strftime('%Y-%m-%d %H:%M:%S'))
    out.with_name('A_EXPORT_S0_meta.json').write_text(json.dumps(meta, indent=1), encoding='utf-8')
    print('wrote', out, len(E), 'keys; source sha256', meta['source_sha256'])


if __name__ == '__main__':
    main()
