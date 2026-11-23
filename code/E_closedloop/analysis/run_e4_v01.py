"""Package E, set E4 (A11 §6d): the post-capture sequence, straight through. Refuses unless revision_v13\\LOCK_A11b.txt exists
and every e4_ job of the requested level(s) has a fetched, receipt-verified run of record. Writes a log line per step to
out\\RUN_E4_v01_<tag>.log and never overwrites a result.

 1. first program:  analysis\\e4_analyse_v01.py --punish-num 3 --out-dir out\\e4_<tag>   (OUTCOMES_E4, E4_RESULTS, A_EXPORT_E4)
 2. second program: recount\\e_recount_v04.py outcomes runs e4_ --punish-num 3; compare_e4 (--e3 its E3 outcomes); e_recount_export_e4_v01
 3. comparison:     analysis\\e_compare_v01.py outcomes (per run) and export (all keys)
Exit 0 only if every step ran and both comparisons have 0 disagreements; else 3 (A10 10.1(c): stop and record the cause).
--tag: 'L' when only stage L is complete (the H keys are then absent on both sides), 'LH' when both are. The final A_EXPORT_E4.json /
A_RECOUNT_E4.json are copied to out\\ only from the LH run, or from the L run if H is declared not completed.

python -I -B analysis/run_e4_v01.py --tag L|LH [--publish]
"""
import argparse, datetime, hashlib, json, pathlib, shutil, subprocess, sys

E = pathlib.Path(__file__).resolve().parents[1]
REV = E.parents[1]
LOCK = REV / 'LOCK_A11b.txt'
OUT = E / 'out'
PY = [sys.executable, '-I', '-B']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True, choices=('L', 'LH')); ap.add_argument('--publish', action='store_true')
    a = ap.parse_args()
    if not LOCK.exists(): raise SystemExit('REFUSED: LOCK_A11b.txt does not exist')
    d = OUT / f'e4_{a.tag}'; d.mkdir(exist_ok=False)
    log = OUT / f'RUN_E4_v01_{a.tag}.log'

    def say(m):
        line = f'{datetime.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} {m}'; print(line, flush=True)
        with open(log, 'a', encoding='utf-8') as f: f.write(line + '\n')

    def run(name, args):
        cmd = [str(x) for x in args]; say('START ' + name)
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(E))
        say(f'END {name}: rc={r.returncode} | {(r.stdout + r.stderr).strip()[-900:]}')
        if r.returncode != 0: raise SystemExit(f'STEP FAILED: {name}')

    say(f'Lock A11b sha256 {sha(LOCK)}; mask table sha256 {sha(OUT / "E4_MASKS_v01.json")}')
    levels = ('E4L',) if a.tag == 'L' else ('E4L', 'E4H')
    want = [j['id'] for st in levels for f in sorted((E / 'jobs').glob(f'JOBS_{st}_*_v01.json'))
            for j in json.loads(f.read_text(encoding='utf-8'))['jobs'] if j['id'].startswith('e4_')]
    missing = [j for j in want if not [x for x in (E / 'runs').glob(j + '*') if (x.name == j or x.name.startswith(j + '__')) and (x / 'FETCH_OK.json').exists()]]
    say(f'coverage: {len(want)} e4 jobs in {levels}, {len(missing)} without a verified run {missing[:8]}')
    if missing: raise SystemExit('REFUSED: runs missing')
    A, R = E / 'analysis', E / 'recount'
    run('first program', PY + [A / 'e4_analyse_v01.py', '--punish-num', '3', '--out-dir', d])
    t4, tc, t3 = d / 'E4_RECOUNT_OUTCOMES_v04.json', d / 'E4_RECOUNT_COMPARE_v04.json', OUT / 'E3_RECOUNT_OUTCOMES_v03.json'
    run('recount outcomes', PY + [R / 'e_recount_v04.py', 'outcomes', 'runs', 'e4_', '--punish-num', '3', '--out', t4])
    run('recount compare_e4', PY + [R / 'e_recount_v04.py', 'compare_e4', t4, '--e3', t3, '--jobs-dir', 'jobs', '--out', tc])
    run('recount export', PY + [R / 'e_recount_export_e4_v01.py', '--e4', t4, '--compare-e4', tc, '--matched', OUT / 'E2_RECOUNT_MATCHED_v01.json',
                                '--punish-num', '3', '--status', 'ran', '--out', d / 'A_RECOUNT_E4.json'])
    total = 0
    for name, args in (('compare outcomes', ['outcomes', d / 'OUTCOMES_E4_v01.json', t4, '--out', d / 'E_COMPARE_OUTCOMES_E4.json']),
                       ('compare export', ['export', d / 'A_EXPORT_E4.json', d / 'A_RECOUNT_E4.json', '--out', d / 'E_COMPARE_EXPORT_E4.json'])):
        run(name, PY + [A / 'e_compare_v01.py'] + args)
        n = json.loads(pathlib.Path(args[-1]).read_text(encoding='utf-8'))['disagreements']; total += n; say(f'{name}: {n} disagreements')
    shas = {p.name: sha(p) for p in sorted(d.glob('*.json'))}
    (d / 'SHAS.json').write_text(json.dumps(dict(lock_a11b=sha(LOCK), outputs=shas, disagreements=total), indent=1), encoding='utf-8')
    if total == 0 and a.publish:
        for f in ('A_EXPORT_E4.json', 'A_RECOUNT_E4.json'):
            dst = OUT / f
            if dst.exists(): dst.rename(OUT / f'{dst.stem}_superseded_{datetime.datetime.now():%H%M%S}.json')
            shutil.copyfile(d / f, dst)
        say('published A_EXPORT_E4.json and A_RECOUNT_E4.json to out\\')
    say(f'DONE: total disagreements {total}')
    sys.exit(0 if total == 0 else 3)


if __name__ == '__main__':
    main()
