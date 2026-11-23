"""Package E, set E6 (A13 §E6): driver, straight through. Never overwrites; a log line per step to out\\RUN_E6_v01_main.log.

  main  requires revision_v13\\LOCK_A13a.txt and every E5 main job (e5_) plus every e6_ job of jobs\\JOBS_E6_*_v01.json with a
        fetched, receipt-verified run. With --allow-missing (a balance stop, A13 §E6.9), missing e6_ jobs are logged and the
        programs run on what exists (K shrinks). First program e6_analyse_v01 main; second program e_recount_e6_v01 main;
        comparison e_compare_v01 outcomes and export. Exit 0 only with 0 disagreements; then A_EXPORT_E6.json /
        A_RECOUNT_E6.json are in out\\.

python -I -B analysis/run_e6_v01.py main [--allow-missing]
"""
import datetime, hashlib, json, pathlib, subprocess, sys

E = pathlib.Path(__file__).resolve().parents[1]
REV = E.parents[1]
OUT = E / 'out'; D6 = OUT / 'e6'
PY = [sys.executable, '-I', '-B']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def verified(j):
    return [x for x in (E / 'runs').glob(j + '*') if (x.name == j or x.name.startswith(j + '__')) and (x / 'FETCH_OK.json').exists()]


def main():
    assert sys.argv[1] == 'main'; allow = '--allow-missing' in sys.argv[2:]
    D6.mkdir(exist_ok=True); log = OUT / 'RUN_E6_v01_main.log'

    def say(m):
        line = f'{datetime.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} {m}'; print(line, flush=True)
        with open(log, 'a', encoding='utf-8') as f: f.write(line + '\n')

    def run(name, args):
        cmd = [str(x) for x in args]; say('START ' + name)
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(E))
        say(f'END {name}: rc={r.returncode} | {(r.stdout + r.stderr).strip()[-900:]}')
        if r.returncode != 0: raise SystemExit(f'STEP FAILED: {name}')

    lock = REV / 'LOCK_A13a.txt'
    if not lock.exists(): raise SystemExit('REFUSED: LOCK_A13a.txt does not exist')
    e6 = [j['id'] for f in sorted((E / 'jobs').glob('JOBS_E6_*_v01.json')) for j in json.loads(f.read_text(encoding='utf-8'))['jobs'] if j['id'].startswith('e6_')]
    e5 = [j['id'] for f in sorted((E / 'jobs').glob('JOBS_E5_*_v01.json')) for j in json.loads(f.read_text(encoding='utf-8'))['jobs'] if j['id'].startswith('e5_')]
    assert len(e6) == 270 and len(e5) == 270
    m5 = [j for j in e5 if not verified(j)]; m6 = [j for j in e6 if not verified(j)]
    say(f'coverage: E5 {len(e5)} jobs, {len(m5)} missing; E6 {len(e6)} jobs, {len(m6)} missing {m6[:8]}')
    if m5: raise SystemExit('REFUSED: E5 runs missing')
    if m6 and not allow: raise SystemExit('REFUSED: E6 runs missing (use --allow-missing only after a balance stop)')
    if m6: (D6 / 'MISSING_E6.json').write_text(json.dumps(dict(missing=m6), indent=1), encoding='utf-8')
    A, R = E / 'analysis', E / 'recount'
    run('first program main', PY + [A / 'e6_analyse_v01.py', 'main'])
    run('second program main', PY + [R / 'e_recount_e6_v01.py', 'main', 'runs', '--settings', OUT / 'E5_SETTINGS_v01.json',
                                    '--out-outcomes', D6 / 'E6_RECOUNT_OUTCOMES_v01.json', '--out-compare', D6 / 'E6_RECOUNT_COMPARE_v01.json',
                                    '--export', OUT / 'A_RECOUNT_E6.json'])
    total = 0
    for name, args in (('compare outcomes', ['outcomes', OUT / 'OUTCOMES_E6_v01.json', D6 / 'E6_RECOUNT_OUTCOMES_v01.json', '--out', D6 / 'E_COMPARE_OUTCOMES_E6.json']),
                       ('compare export', ['export', OUT / 'A_EXPORT_E6.json', OUT / 'A_RECOUNT_E6.json', '--out', D6 / 'E_COMPARE_EXPORT_E6.json'])):
        run(name, PY + [A / 'e_compare_v01.py'] + args)
        n = json.loads(pathlib.Path(args[-1]).read_text(encoding='utf-8'))['disagreements']; total += n; say(f'{name}: {n} disagreements')
    (D6 / 'SHAS_main.json').write_text(json.dumps(dict(lock_a13a=sha(lock), missing_e6=len(m6), outputs={p.name: sha(p) for p in [OUT / 'A_EXPORT_E6.json', OUT / 'A_RECOUNT_E6.json', OUT / 'OUTCOMES_E6_v01.json', OUT / 'E6_RESULTS_v01.json']}, disagreements=total), indent=1), encoding='utf-8')
    say(f'DONE: total disagreements {total}')
    sys.exit(0 if total == 0 else 3)


if __name__ == '__main__':
    main()
