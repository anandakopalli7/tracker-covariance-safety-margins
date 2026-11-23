"""Package E: the whole post-Lock-2 sequence, straight through (coordinator 20 Nov 01:24: no step waits for a clock time).
Refuses unless revision_v13\\LOCK_A10_2.txt exists AND every one of the 1,200 E3 / E3b arm jobs of the frozen lists has a
fetched, receipt-verified run of record (FETCH_OK.json). Runs, in order, writing a log line per step to out\\RUN_AFTER_LOCK2_v01.log:

 0. checks: Lock 2 present (SHA logged); matched file SHA = the one in LOCK_A10_2b.txt; job coverage 900 + 300
 1. first program:  e_collect_v01 e3 / e3b -> out\\OUTCOMES_E3_v01.json, OUTCOMES_E3B_v01.json
                    e3_analyse_v01 -> out\\E3_RESULTS_v01.json
                    e_export_v03 -> out\\A_EXPORT_E.json
 2. second program: e_recount_v03 outcomes e3_ / e3b_ -> out\\E3_RECOUNT_OUTCOMES_v03.json, E3B_RECOUNT_OUTCOMES_v03.json
                    e_recount_v03 compare --low-power <from the matched file> -> out\\E3_RECOUNT_COMPARE_v03.json
                    e_recount_export_v02 -> out\\A_RECOUNT_E.json
 3. comparison:     e_compare_v01 outcomes (E3, E3b), compare, export -> out\\E_COMPARE_*_E3_v01.json
Exit 0 only if every step ran and every comparison has 0 disagreements; otherwise exit 3 (A10 10.1(c): stop and record the cause).

python -I -B analysis/run_e_after_lock2_v01.py [--skip-coverage-check]   (the flag only for a recorded, decided gap)
"""
import argparse, datetime, hashlib, json, pathlib, subprocess, sys

E = pathlib.Path(__file__).resolve().parents[1]
REV = E.parents[1]
LOCK2 = REV / 'LOCK_A10_2.txt'
LOCK2B = E.parent / 'locks' / 'LOCK_A10_2b.txt'
OUT = E / 'out'
LOG = OUT / 'RUN_AFTER_LOCK2_v01.log'
PY = [sys.executable, '-I', '-B']
MATCHED = OUT / 'E2_MATCHED_v01.json'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def log(msg):
    line = f'{datetime.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} {msg}'
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


def run(name, args):
    cmd = [str(x) for x in args]
    log(f'START {name}: {" ".join(cmd[3:])}')
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(E))
    tail = (r.stdout + r.stderr).strip()[-1500:]
    log(f'END {name}: rc={r.returncode} | {tail}')
    if r.returncode != 0: raise SystemExit(f'STEP FAILED: {name} rc={r.returncode}')
    return r


def coverage():
    want = []
    for f in sorted((E / 'jobs').glob('JOBS_E3*_claude-v13e-0[4-9]_v01.json')):
        want += [j['id'] for j in json.loads(f.read_text(encoding='utf-8'))['jobs'] if str(j.get('arm', '')).startswith('E_')]
    missing = []
    for j in want:
        ok = [d for d in (E / 'runs').glob(j + '*') if (d.name == j or d.name.startswith(j + '__')) and (d / 'FETCH_OK.json').exists()]
        if not ok: missing.append(j)
    return want, missing


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--skip-coverage-check', action='store_true')
    a = ap.parse_args()
    if not LOCK2.exists(): raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist')
    log(f'Lock 2 present, sha256 {sha(LOCK2)}')
    ms = sha(MATCHED); assert ms in LOCK2B.read_text(encoding='utf-8'), 'matched file SHA not in LOCK_A10_2b'
    log(f'matched file {MATCHED.name} sha256 {ms} is the one in LOCK_A10_2b')
    want, missing = coverage()
    log(f'coverage: {len(want)} arm jobs in the frozen lists, {len(missing)} without a verified run {missing[:10]}')
    if len(want) != 1200: raise SystemExit(f'expected 1200 arm jobs in the lists, found {len(want)}')
    if missing and not a.skip_coverage_check: raise SystemExit('REFUSED: runs missing; fetch first (or record the gap and pass --skip-coverage-check)')
    low_power = bool(json.loads(MATCHED.read_text(encoding='utf-8'))['levels']['low_power'])
    o = {k: OUT / v for k, v in dict(m3='OUTCOMES_E3_v01.json', m3b='OUTCOMES_E3B_v01.json', res='E3_RESULTS_v01.json', exp='A_EXPORT_E.json',
                                      t3='E3_RECOUNT_OUTCOMES_v03.json', t3b='E3B_RECOUNT_OUTCOMES_v03.json', tc='E3_RECOUNT_COMPARE_v03.json',
                                      rexp='A_RECOUNT_E.json', c3='E_COMPARE_OUTCOMES_E3_v01.json', c3b='E_COMPARE_OUTCOMES_E3B_v01.json',
                                      cr='E_COMPARE_RESULTS_E3_v01.json', ce='E_COMPARE_EXPORT_E3_v01.json').items()}
    for k, p in o.items():
        assert not p.exists(), f'{p.name} exists; never overwrite a result (rename it by hand with a recorded reason)'
    A, R = E / 'analysis', E / 'recount'
    # 1. first program
    run('collect e3', PY + [A / 'e_collect_v01.py', 'e3', '--out', o['m3']])
    run('collect e3b', PY + [A / 'e_collect_v01.py', 'e3b', '--out', o['m3b']])
    run('analyse', PY + [A / 'e3_analyse_v01.py', '--e3', o['m3'], '--e3b', o['m3b'], '--lock2b', MATCHED, '--out', o['res']])
    run('export', PY + [A / 'e_export_v03.py', '--status', 'ran', '--e1', OUT / 'E1_VERDICT_a1_v01.json', '--e1-attempts', '1', '--matched', MATCHED,
                        '--e3-outcomes', o['m3'], '--e3b-outcomes', o['m3b'], '--results', o['res'], '--out', o['exp']])
    # 2. second program
    run('recount outcomes e3', PY + [R / 'e_recount_v03.py', 'outcomes', 'runs', 'e3_', '--out', o['t3']])
    run('recount outcomes e3b', PY + [R / 'e_recount_v03.py', 'outcomes', 'runs', 'e3b_', '--out', o['t3b']])
    run('recount compare', PY + [R / 'e_recount_v03.py', 'compare', o['t3'], '--e3b', o['t3b'], '--low-power', str(low_power).lower(), '--out', o['tc']])
    run('recount export', PY + [R / 'e_recount_export_v02.py', '--e3', o['t3'], '--e3b', o['t3b'], '--compare', o['tc'], '--e1', OUT / 'E1_RECOUNT_a1_v01.json',
                                '--calib', OUT / 'E2_RECOUNT_CALIB_v01.json', '--matched', OUT / 'E2_RECOUNT_MATCHED_v01.json', '--status', 'ran',
                                '--e1-attempts', '1', '--out', o['rexp']])
    # 3. comparison of record
    total = 0
    for name, args in (('compare outcomes e3', ['outcomes', o['m3'], o['t3'], '--out', o['c3']]),
                       ('compare outcomes e3b', ['outcomes', o['m3b'], o['t3b'], '--out', o['c3b']]),
                       ('compare results', ['compare', o['res'], o['tc'], '--out', o['cr']]),
                       ('compare export', ['export', o['exp'], o['rexp'], '--out', o['ce']])):
        run(name, PY + [A / 'e_compare_v01.py'] + args)
        n = json.loads(pathlib.Path(args[-1]).read_text(encoding='utf-8'))['disagreements']; total += n
        log(f'{name}: {n} disagreements')
    shas = {k: sha(p) for k, p in o.items()}
    (OUT / 'RUN_AFTER_LOCK2_v01_SHAS.json').write_text(json.dumps(dict(lock2_sha256=sha(LOCK2), outputs=shas, disagreements=total), indent=1), encoding='utf-8')
    log(f'DONE: total disagreements {total}')
    sys.exit(0 if total == 0 else 3)


if __name__ == '__main__':
    main()
