"""A10 sec. 10.1(c) comparison for package D: first programs (analysis/) against second programs (recount_d/).
Counts exact; points and interval ends within 1e-9; classifications equal. Usage: python -I compare_d_v13.py FIRST_DNB SECOND_DNB FIRST_D2 SECOND_D2 [--variant-map old_as_variant=constant]
Writes out/COMPARE_D_v13.json (never overwrites) and prints the number of disagreements.
"""
import json, pathlib, sys

TOL = 1e-9
HERE = pathlib.Path(__file__).resolve().parent
NAME = {'A1': 'AM'}
SC = {'3s': 'commit_3s', 'RS075': 'react_stop_tau0p75'}


def close(a, b):
    if a is None or b is None: return a is None and b is None
    if isinstance(a, float) and a != a: return isinstance(b, float) and b != b
    return abs(float(a) - float(b)) <= TOL


def main():
    f1, f2, g1, g2 = (json.loads(pathlib.Path(x).read_text(encoding='utf-8')) for x in sys.argv[1:5])
    vmap = dict(x.split('=') for x in sys.argv[sys.argv.index('--variant-map') + 1].split(',')) if '--variant-map' in sys.argv else {}
    rows = []; bad = 0

    def chk(what, a, b, exact=False):
        nonlocal bad
        ok = (a == b) if exact else close(a, b)
        if not ok: bad += 1
        rows.append(dict(item=what, first=a, second=b, agree=ok))

    m1 = f1['matched']; m2 = f2['matched_settings']
    chk('c_star', m1['caution_F0_g1_pp'], m2['c_star'])
    for a, v in m1['scales'].items(): chk(f'matched_index_{a}', v['index'], m2['sources'][NAME.get(a, a)]['idx'], True)
    chk('PS_triple', m1['PS_triple']['indices'], list(m2['PS']['idx']), True)
    for k1, v in f1['variants'].items():
        k2 = next((x for x, y in vmap.items() if y == k1), k1)
        if k2 not in f2['variants']: continue
        w = f2['variants'][k2]
        chk(f'{k1}/D-H1', v['D_H1'], w['D-H1'], True); chk(f'{k1}/D-H2', v['D_H2'], w['D-H2'], True)
        for a in ('N', 'NA', 'A1', 'CK3', 'Q', 'TG', 'PS'):
            s1 = v['sources'][a]; s2 = w['sources'][NAME.get(a, a)]
            for q1, q2 in (('caution_diff_pp', 'd_caution'), ('wrong_go_diff_pp', 'd_wrong_go')):
                chk(f'{k1}/{a}/{q1}/point', s1[q1]['point'], s2[q2]['point'])
                chk(f'{k1}/{a}/{q1}/lo', s1[q1]['ci'][0], s2[q2]['ci'][0]); chk(f'{k1}/{a}/{q1}/hi', s1[q1]['ci'][1], s2[q2]['ci'][1])
            chk(f'{k1}/{a}/classification', s1['classification'], s2['classification'], True)
    for sc, t in g1['table'].items():
        for a, byt in t.items():
            for tg, x in byt.items():
                y = g2['table'][a][SC[sc]][tg.rstrip('%')] if tg.rstrip('%') in g2['table'][a][SC[sc]] else g2['table'][a][SC[sc]][str(float(tg.rstrip('%')))]
                chk(f'D2/{sc}/{a}/{tg}/g', x['operating_point']['g'], y['g'])
                chk(f'D2/{sc}/{a}/{tg}/runs_with_wrong_go', x['runs_with_wrong_go'], y['n_runs_with_wrong_go'], True)
                chk(f'D2/{sc}/{a}/{tg}/median_of_medians', x['median_of_run_medians'], y['median_of_run_medians_mps'])
    out = HERE / 'out' / ('COMPARE_D_v13' + ('_TESTOLD' if '--variant-map' in sys.argv else '') + '.json')
    out.parent.mkdir(exist_ok=True)
    if out.exists(): raise SystemExit('REFUSED: exists ' + str(out))
    out.write_text(json.dumps(dict(compared=len(rows), disagreements=bad, rows=rows), indent=1, default=str), encoding='utf-8')
    print(json.dumps(dict(compared=len(rows), disagreements=bad)))


if __name__ == '__main__':
    main()
