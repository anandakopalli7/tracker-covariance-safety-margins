"""Recount of package C: DRY RUN of the fresh-run code path with OLD runs relabelled, in a scratch tree. New file, 19 Nov 2026
(Claude Fable 5.2).

Purpose: the fresh-run loaders and the H3 (IMM) branch cannot be exercised on real fresh data before Lock 2. This tool builds, in a
scratch folder OUTSIDE the project (argument 1), a copy of the folder layout the programs expect, filled with OLD runs only:
  revision_v13\\work\\CD_capture\\CASES_C_v13.json        35 'lead_braking' cases and 20 'cutin' cases with made-up case names
  revision_v13\\work\\CD_capture\\arrays\\CV0\\*.npz       the 35 old evaluation runs / the 20 cut-in tuning runs under those names
  revision_v13\\work\\CD_capture\\arrays\\B1\\*.npz        the same lead runs with cN := cNA (a stand-in so that the IMM branch runs)
  revision_v13\\LOCK_A10_2.txt                            a file saying it is NOT the lock (the gate of the scratch tree only)
  revision_v11\\analysis, revision_v12\\analysis          the loader, a9_common and the old lead / TG arrays (copies)
It never reads or writes anything of a fresh run, and never touches the real lock. The programs are then run with
RC_ARS_TRIAL=<scratch> and RC_DRYRUN=1; their outputs are named DRYRUN_* and say so inside.
Usage: python -I -B -X utf8 dryrun_fresh_path_v13.py <scratch folder> [truth json of the old cut-in test]
"""
import json, pathlib, shutil, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rc_core_v13 as K


def main():
    scratch = pathlib.Path(sys.argv[1]).resolve()
    if str(K.ARS).lower() in str(scratch).lower() or 'ARS_TRIAL' in str(scratch):
        raise SystemExit('REFUSED: the scratch tree must be outside the project')
    cd = scratch / 'revision_v13' / 'work' / 'CD_capture'
    (cd / 'arrays' / 'CV0').mkdir(parents=True, exist_ok=True); (cd / 'arrays' / 'B1').mkdir(parents=True, exist_ok=True)
    for sub, files in (('revision_v11/analysis', ['rev_common_v01.py']), ('revision_v12/analysis', ['a9_common_v01.py'])):
        d = scratch / sub; d.mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.copy2(K.ARS / sub / f, d / f)
    # a9_common_v01 holds the absolute path of revision_v11 (the real one): its import still works
    for sub in ('lead', 'tg'):
        dst = scratch / 'revision_v12' / 'analysis' / 'out' / sub
        if not dst.exists():
            shutil.copytree(K.V12 / 'out' / sub, dst)
    shutil.copy2(K.V12 / 'out' / 'A9_3_PHASE_SCALE_CV_v02.json', scratch / 'revision_v12' / 'analysis' / 'out' / 'A9_3_PHASE_SCALE_CV_v02.json')
    cases = []
    old = K.load_old_eval_runs()
    for i, r in enumerate(old):
        case = 'dryrun_lead_%04d' % i; rid = 'pc13_%s_native' % case
        cases.append(dict(case=case, family='lead_braking', old_run=r['run']))
        base = dict(k=r['k'], evaluated=r['ev'], des=np.full(r['ev'].size, r['desired']), clear=r['clear1'], vbar=r['vbar'], idx55=r['idx55'],
                    cF0=r['crit']['F0'], cE=r['crit']['E'], cN=r['crit']['N'], cNA=r['crit']['NA'], cQ=r['crit']['Q'], cA1=r['crit']['A1'],
                    cCK3=r['crit']['CK3'], phase=r['ph'].astype(np.int8), lead_found=r['lead_found'], vhat=r['vhat'], ahat_long=r['ahat_long'],
                    meta=json.dumps(dict(family='lead_braking', run_id=rid, case=case, lead_variant=None, dryrun_of=r['run'])))
        np.savez(cd / 'arrays' / 'CV0' / (rid + '.npz'), cTG2=r['crit']['TG'], **base)
        b1 = dict(base); b1['cN'] = r['crit']['NA']
        np.savez(cd / 'arrays' / 'B1' / (rid + '.npz'), **b1)
    cut = K.load_old_cutin_runs()
    names = {}
    for i, r in enumerate(cut):
        case = 'dryrun_cutin_%04d' % i; rid = 'pc13_%s_native' % case
        names[r['run']] = rid
        cases.append(dict(case=case, family='cutin', old_run=r['run']))
        np.savez(cd / 'arrays' / 'CV0' / (rid + '.npz'), k=r['k'], evaluated=r['ev'], des=np.full(r['ev'].size, r['desired']), clear=r['clear1'],
                 vbar=r['vbar'], idx55=r['idx55'], cF0=r['crit']['F0'], cE=r['crit']['E'], cN=r['crit']['N'],
                 meta=json.dumps(dict(family='cutin', run_id=rid, case=case, lead_variant=None, dryrun_of=r['run'])))
    (cd / 'CASES_C_v13.json').write_text(json.dumps(dict(schema='DRYRUN, old runs relabelled', cases=cases), indent=1), encoding='utf-8')
    (scratch / 'revision_v13' / 'LOCK_A10_2.txt').write_text('DRY RUN scratch tree: this is NOT LOCK_A10_2. Old runs relabelled.\n', encoding='utf-8')
    if len(sys.argv) > 2:
        t = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding='utf-8'))
        t['mode'] = 'fresh'
        for x in t['truth']:
            x['run'] = names[x['run']]
        t['truth'].sort(key=lambda x: x['run'])
        t['runs'] = [x['run'] for x in t['truth']]
        (scratch / 'DRYRUN_CUTIN_TRUTH.json').write_text(json.dumps(t), encoding='utf-8')
    print('dry-run tree written: %s (%d lead, %d cut-in runs; old runs only)' % (scratch, len(old), len(cut)))


if __name__ == '__main__':
    main()
