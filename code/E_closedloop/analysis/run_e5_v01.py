"""Package E, set E5 (A12 §6): drivers, straight through. Never overwrites; a log line per step to out\\RUN_E5_v01_<stage>.log.

  cal   requires every e5c job of jobs\\JOBS_E5C_*_v01.json to have a fetched, receipt-verified run. First program
        e5_analyse_v01 cal (E5_CAL_v01.json, E5_SETTINGS_v01.json); second program e_recount_e5_v01 cal and match (out\\e5\\);
        comparison: per-g valid counts and contacts equal, shares within 1e-9, g_D and low_power equal; the g_D row of the match
        table: g_N equal, both cautions and the signed difference within 1e-9. Exit 0 only if all agree (then LOCK_A12b may record
        E5_SETTINGS_v01.json).
  main  requires LOCK_A12b (recording the settings) and every e5 job verified. First program e5_analyse_v01 main; second program
        e_recount_e5_v01 main (--settings, --cal, --match); comparison e_compare_v01 outcomes and export. Exit 0 only with 0
        disagreements; then A_EXPORT_E5.json / A_RECOUNT_E5.json are in out\\.

python -I -B analysis/run_e5_v01.py cal|main
"""
import datetime, hashlib, json, math, pathlib, subprocess, sys

E = pathlib.Path(__file__).resolve().parents[1]
REV = E.parents[1]
OUT = E / 'out'; D5 = OUT / 'e5'
PY = [sys.executable, '-I', '-B']
TOL = 1e-9


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    stage = sys.argv[1]; assert stage in ('cal', 'main')
    D5.mkdir(exist_ok=True); log = OUT / f'RUN_E5_v01_{stage}.log'

    def say(m):
        line = f'{datetime.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} {m}'; print(line, flush=True)
        with open(log, 'a', encoding='utf-8') as f: f.write(line + '\n')

    def run(name, args, ok_rc=(0,)):
        cmd = [str(x) for x in args]; say('START ' + name)
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(E))
        say(f'END {name}: rc={r.returncode} | {(r.stdout + r.stderr).strip()[-900:]}')
        if r.returncode not in ok_rc: raise SystemExit(f'STEP FAILED: {name}')

    st = 'E5C' if stage == 'cal' else 'E5'
    want = [j['id'] for f in sorted((E / 'jobs').glob(f'JOBS_{st}_*_v01.json')) for j in json.loads(f.read_text(encoding='utf-8'))['jobs']
            if j['id'].startswith('e5c_' if stage == 'cal' else 'e5_')]
    missing = [j for j in want if not [x for x in (E / 'runs').glob(j + '*') if (x.name == j or x.name.startswith(j + '__')) and (x / 'FETCH_OK.json').exists()]]
    say(f'coverage: {len(want)} {st} jobs, {len(missing)} without a verified run {missing[:8]}')
    if missing: raise SystemExit('REFUSED: runs missing')
    A, R = E / 'analysis', E / 'recount'
    if stage == 'cal':
        run('first program cal', PY + [A / 'e5_analyse_v01.py', 'cal'])
        run('second program cal', PY + [R / 'e_recount_e5_v01.py', 'cal', 'runs', '--out', D5 / 'E5_CAL_RECOUNT_v01.json'])
        run('second program match', PY + [R / 'e_recount_e5_v01.py', 'match', '--out', D5 / 'E5_MATCH_RECOUNT_v01.json'])
        mine = json.loads((OUT / 'E5_CAL_v01.json').read_text(encoding='utf-8')); s = json.loads((OUT / 'E5_SETTINGS_v01.json').read_text(encoding='utf-8'))
        th = json.loads((D5 / 'E5_CAL_RECOUNT_v01.json').read_text(encoding='utf-8')); tm = json.loads((D5 / 'E5_MATCH_RECOUNT_v01.json').read_text(encoding='utf-8'))
        diffs = []
        tp = {float(x['g']): x for x in th['per_g'] if x.get('g') is not None}
        for g, v in mine['shares'].items():
            t = tp.get(float(g))
            if t is None: diffs.append(('presence', g)); continue
            if v['n_valid'] != t['n_valid'] or v['contacts'] != t['contacts']: diffs.append(('counts', g, v, t))
            if (v['share'] is None) != (t.get('share') is None) or (v['share'] is not None and abs(v['share'] - t['share']) > TOL): diffs.append(('share', g, v['share'], t.get('share')))
        if float(th['g_D']) != float(s['g_D']) or bool(th['low_power']) != bool(s['low_power']): diffs.append(('g_D', s['g_D'], th['g_D'], s['low_power'], th['low_power']))
        row = [r for r in tm['rows'] if abs(float(r['g_D']) - float(s['g_D'])) < 1e-12][0]
        for fm, ft in (('g_N', 'g_N'), ('caution_F0D_pct', 'caution_F0D'), ('caution_N_pct', 'caution_N'), ('caution_diff_pp', 'caution_diff')):
            if abs(float(s[fm]) - float(row[ft])) > (1e-12 if fm == 'g_N' else TOL): diffs.append((fm, s[fm], row[ft]))
        (D5 / 'E5_CAL_COMPARE_v01.json').write_text(json.dumps(dict(disagreements=len(diffs), list=diffs, settings_sha256=sha(OUT / 'E5_SETTINGS_v01.json')), indent=1, default=str), encoding='utf-8')
        say(f'cal comparison: {len(diffs)} disagreements {diffs[:4]}; g_D {s["g_D"]}, g_N {s["g_N"]}, shares {s["shares"]}; settings sha256 {sha(OUT / "E5_SETTINGS_v01.json")}')
        sys.exit(0 if not diffs else 3)
    lock = REV / 'LOCK_A12b.txt'
    if not lock.exists() or sha(OUT / 'E5_SETTINGS_v01.json') not in lock.read_text(encoding='utf-8'): raise SystemExit('REFUSED: LOCK_A12b missing or not recording the settings')
    run('first program main', PY + [A / 'e5_analyse_v01.py', 'main'])
    run('second program main', PY + [R / 'e_recount_e5_v01.py', 'main', 'runs', '--settings', OUT / 'E5_SETTINGS_v01.json', '--cal', D5 / 'E5_CAL_RECOUNT_v01.json',
                                    '--match', D5 / 'E5_MATCH_RECOUNT_v01.json', '--out-outcomes', D5 / 'E5_RECOUNT_OUTCOMES_v01.json',
                                    '--out-compare', D5 / 'E5_RECOUNT_COMPARE_v01.json', '--export', OUT / 'A_RECOUNT_E5.json'])
    total = 0
    for name, args in (('compare outcomes', ['outcomes', OUT / 'OUTCOMES_E5_v01.json', D5 / 'E5_RECOUNT_OUTCOMES_v01.json', '--out', D5 / 'E_COMPARE_OUTCOMES_E5.json']),
                       ('compare export', ['export', OUT / 'A_EXPORT_E5.json', OUT / 'A_RECOUNT_E5.json', '--out', D5 / 'E_COMPARE_EXPORT_E5.json'])):
        run(name, PY + [A / 'e_compare_v01.py'] + args)
        n = json.loads(pathlib.Path(args[-1]).read_text(encoding='utf-8'))['disagreements']; total += n; say(f'{name}: {n} disagreements')
    (D5 / 'SHAS_main.json').write_text(json.dumps(dict(lock_a12b=sha(lock), outputs={p.name: sha(p) for p in [OUT / 'A_EXPORT_E5.json', OUT / 'A_RECOUNT_E5.json', OUT / 'OUTCOMES_E5_v01.json', OUT / 'E5_RESULTS_v01.json']}, disagreements=total), indent=1), encoding='utf-8')
    say(f'DONE: total disagreements {total}')
    sys.exit(0 if total == 0 else 3)


if __name__ == '__main__':
    main()
