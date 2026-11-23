"""Plumbing test of the E3 / E3b analysis and the first-vs-second comparison, before any real E3 value exists, on real-shaped
values: the 180 E2 runs (design data, F0 at six g values on 30 tuning cases; not sealed) are relabelled into an E3-shaped design,
and both programs' comparison steps run on the same relabelled outcomes:
  first:  analysis/e3_analyse_v01.py (Newcombe, McNemar, case bootstrap, classification)
  second: recount/e_recount_v0X.py compare
then analysis/e_compare_v01.py comparisons() checks counts exact, values within 1e-9, classifications equal.

Relabelling (a g set may stand for several arms; every (arm, level) gets one g set, so no duplicates):
  g0 -> E_Z (level None); g0.25 -> E_CK3 lo, E_F0_IMM lo; g1 -> E_N lo, E_TG hi; g4 -> E_F0 lo, E_N_IMM lo, E_PS hi;
  g16 -> E_F0 hi, E_TG lo, E_F0_IMM hi; g64 -> E_N hi, E_CK3 hi, E_PS lo, E_N_IMM hi.
  E3b: the lo rows of E_F0, E_N, E_CK3, E_TG, E_PS, with the 30 cases split by sorted index mod 3 into the variants
  constant / mild_braking / stop_and_go (10 cases each).
The Lock 2 guard of e3_analyse is pointed at a stand-in file: these are E2 values, not E3 / E3b runs.

python -I -B tests/test_e_compare_e2relabel_v01.py [--recount recount/e_recount_v02.py]
"""
import argparse, json, pathlib, subprocess, sys

E = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(E / 'analysis'))
import e3_analyse_v01 as EA, e_compare_v01 as CMP   # noqa: E402

OUT = E / 'tests' / 'out'; OUT.mkdir(exist_ok=True)
MAP = {0.0: [('E_Z', None)], 0.25: [('E_CK3', 'lo'), ('E_F0_IMM', 'lo')], 1.0: [('E_N', 'lo'), ('E_TG', 'hi')],
       4.0: [('E_F0', 'lo'), ('E_N_IMM', 'lo'), ('E_PS', 'hi')], 16.0: [('E_F0', 'hi'), ('E_TG', 'lo'), ('E_F0_IMM', 'hi')],
       64.0: [('E_N', 'hi'), ('E_CK3', 'hi'), ('E_PS', 'lo'), ('E_N_IMM', 'hi')]}
E3B_ARMS = ('E_F0', 'E_N', 'E_CK3', 'E_TG', 'E_PS')
VARS = ('constant', 'mild_braking', 'stop_and_go')


def relabel(rows, gkey, prog):
    cases = sorted({r['case'] for r in rows}); vi = {c: VARS[i % 3] for i, c in enumerate(cases)}
    e3, e3b = [], []
    for r in rows:
        for arm, lev in MAP[float(r[gkey] if r.get(gkey) is not None else r['e_job']['g'])]:
            x = dict(r); x.update(arm=arm, level=lev, lead_variant=None, job=f"{r['job']}__as_{arm}_{lev}")
            if 'run_id' in x: x['run_id'] = x['job']
            e3.append(x)
            if lev == 'lo' and arm in E3B_ARMS:
                y = dict(x); y.update(lead_variant=vi[r['case']], job=f"{r['job']}__as_{arm}_{lev}_{vi[r['case']]}")
                if 'run_id' in y: y['run_id'] = y['job']
                e3b.append(y)
    return e3, e3b


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--recount', default=str(E / 'recount' / 'e_recount_v02.py'))
    a = ap.parse_args()
    mine = json.loads((E / 'out' / 'OUTCOMES_E2_v01.json').read_text(encoding='utf-8'))
    tag = pathlib.Path(a.recount).stem.split('_')[-1]
    theirs = json.loads((E / 'out' / f'E2_RECOUNT_OUTCOMES_{tag}.json').read_text(encoding='utf-8'))
    m3, m3b = relabel(mine['runs'], 'g', 'first'); t3, t3b = relabel(theirs['runs'], 'g', 'second')
    print('relabelled: first', len(m3), len(m3b), 'second', len(t3), len(t3b))
    p = {}
    for name, rows, base in (('M3', m3, mine), ('M3B', m3b, mine), ('T3', t3, theirs), ('T3B', t3b, theirs)):
        doc = dict(base); doc['runs'] = rows
        p[name] = OUT / f'RELABEL_{name}_{tag}.json'; p[name].write_text(json.dumps(doc, indent=1), encoding='utf-8')
    stand_in = OUT / 'RELABEL_LOCK2_STAND_IN.txt'; stand_in.write_text('stand-in for the Lock 2 guard: E2 values relabelled\n', encoding='utf-8')
    EA.LOCK2 = stand_in
    lp = OUT / 'RELABEL_LOCK2B_STAND_IN.json'; lp.write_text(json.dumps({'levels': {'low_power': False}}), encoding='utf-8')
    res_m = OUT / f'RELABEL_RESULTS_FIRST_{tag}.json'
    sys.argv = ['e3_analyse_v01.py', '--e3', str(p['M3']), '--e3b', str(p['M3B']), '--lock2b', str(lp), '--out', str(res_m)]
    EA.main()
    res_t = OUT / f'RELABEL_RESULTS_SECOND_{tag}.json'
    r = subprocess.run([sys.executable, '-I', '-B', a.recount, 'compare', str(p['T3']), '--e3b', str(p['T3B']), '--low-power', 'false', '--out', str(res_t)],
                       capture_output=True, text=True, cwd=str(E))
    print('recount compare rc', r.returncode, (r.stdout + r.stderr).strip()[-600:])
    c = CMP.comparisons(res_m, res_t)
    (OUT / f'RELABEL_COMPARE_{tag}.json').write_text(json.dumps(c, indent=1, default=str), encoding='utf-8')
    print('COMPARED', c['comparisons_compared'], 'DISAGREEMENTS', c['disagreements'], 'extras', [x['label'] for x in c['extras_in_recount']])
    for d in c['list'][:20]: print('  ', d)


if __name__ == '__main__':
    main()
