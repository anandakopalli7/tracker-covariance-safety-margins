"""Recount of package C: test of the pod path of the double bootstrap (export -> rc_calib_remote_v13.py on chunks -> import)
against the in-process path, on OLD runs only. New file, 20 Nov 2026 (Claude Fable 5.2). No fresh-run file is opened.

For lead braking and for cut-in (old runs, small sizes):
  (a) the in-process program;
  (b) --calib export; the runner on outer chunks 0:5 and 5:12 for each inner seed, each as its own process, called as on a pod
      (python -I -B rc_calib_remote_v13.py JOBDIR LABEL --seeds SEED --outer LO:HI --threads 1, from another working
      directory); --calib import.
  Every value of the two output JSONs is compared (==, NaN equal to NaN). Not compared: time stamps, run times, thread counts,
  the calibration mode and the import record (paths, chunk names).
Standalone check: the job files, the runner and rc_kern_v13.py are copied to a fresh folder under %TEMP%; one chunk is computed
there from another working directory; it must equal the chunk computed in the project folder.
Old-code check: rows of the chunks are compared with the checkpoints that the programs wrote BEFORE this change
(out\\ckpt\\*_b200_o10_i50*_inner1.npz: 10 outer samples, 50 inner), read-only.
Timing: a lead job with 1,000 inner resamples; the runner's seconds per outer sample, one thread.

Usage: python -I -B -X utf8 test_rc_calib_chunks_v13.py [--suffix X] [--skip-timing]
Output: out\\TEST_RC_CALIB_CHUNKS_v13<suffix>.json (never overwritten).
"""
import argparse, json, math, os, pathlib, shutil, subprocess, sys, tempfile, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'out'
CAL = OUT / 'calib_testold'
PY = [sys.executable, '-I', '-B', '-X', 'utf8']
PYR = [sys.executable, '-I', '-B']                       # the runner's call, as on a pod
SEEDS = [20261913, 20261914]
SIZES = ['--boot', '200', '--outer', '12', '--inner', '50', '--mc', '200']
CHUNKS = [(0, 5), (5, 12)]
SKIP = ('started', 'written', 'threads', 'calib_mode', 'calib_import')
CHUNK_KEYS = ('p_lt', 'p_le', 'p_lt_any', 'p_le_any', 'outer_est', 'n_inner_valid')
ENV = dict(os.environ, OPENBLAS_CORETYPE='Haswell')


def run(cmd, cwd, log):
    t0 = time.time()
    with open(log, 'a', encoding='utf-8') as f:
        f.write('\n$ %s   (cwd %s)\n' % (' '.join(str(c) for c in cmd), cwd)); f.flush()
        rc = subprocess.run([str(c) for c in cmd], cwd=str(cwd), env=ENV, stdout=f, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        raise SystemExit('FAILED (%d): %s  -- see %s' % (rc, ' '.join(str(c) for c in cmd), log))
    return time.time() - t0


def run_pairs(cmds, cwd, log):
    """At most two processes at a time (the laptop is shared)."""
    for i in range(0, len(cmds), 2):
        ps = []
        for k, cmd in enumerate(cmds[i:i + 2]):
            f = open('%s.p%d' % (log, k), 'w', encoding='utf-8')
            ps.append((subprocess.Popen([str(c) for c in cmd], cwd=str(cwd), env=ENV, stdout=f, stderr=subprocess.STDOUT), f, cmd))
        for p, f, cmd in ps:
            rc = p.wait(); f.close()
            with open(log, 'a', encoding='utf-8') as g:
                g.write('\n$ %s   (cwd %s)\n%s' % (' '.join(str(c) for c in cmd), cwd, pathlib.Path(f.name).read_text(encoding='utf-8')))
            os.remove(f.name)
            if rc != 0:
                raise SystemExit('FAILED (%d): %s -- see %s' % (rc, ' '.join(str(c) for c in cmd), log))


def leaves(o, path=()):
    if isinstance(o, dict):
        for k in sorted(o):
            if k in SKIP or k.startswith('seconds'):
                continue
            yield from leaves(o[k], path + (k,))
    elif isinstance(o, list):
        yield path + ('#len',), len(o)
        for i, v in enumerate(o):
            yield from leaves(v, path + (i,))
    else:
        yield path, o


def same(x, y):
    if isinstance(x, float) and isinstance(y, float) and math.isnan(x) and math.isnan(y):
        return True
    return type(x) is type(y) and x == y


def compare_json(fa, fb):
    A = dict(leaves(json.loads(pathlib.Path(fa).read_text(encoding='utf-8'))))
    B = dict(leaves(json.loads(pathlib.Path(fb).read_text(encoding='utf-8'))))
    keys = sorted(set(A) | set(B), key=str)
    diff = [('/'.join(str(x) for x in k), A.get(k, '<absent>'), B.get(k, '<absent>')) for k in keys
            if k not in A or k not in B or not same(A[k], B[k])]
    return dict(a=str(fa), b=str(fb), values_compared=len(keys), values_differing=len(diff), first_differences=diff[:20])


def chunk_file(d, label, seed, lo, hi):
    return pathlib.Path(d) / ('%s_%d_o%d_%d.npz' % (label, seed, lo, hi))


def compare_chunks(fa, fb):
    with np.load(fa, allow_pickle=False) as a, np.load(fb, allow_pickle=False) as b:
        bad = [k for k in CHUNK_KEYS if not np.array_equal(a[k], b[k], equal_nan=True)]
        bad += [k for k in ('label', 'seed', 'lo', 'hi', 'n_outer', 'n_inner', 'job_sha256') if str(a[k]) != str(b[k])]
        n = int(sum(a[k].size for k in CHUNK_KEYS))
        return dict(a=str(fa), b=str(fb), values_compared=n, entries_differing=bad, versions_a=str(a['versions']), versions_b=str(b['versions']))


def old_ckpt_check(label, ckpt):
    """Rows 0..9 of seed 20261913 (chunks 0:5 and 5:12) against a checkpoint written by the program before this change."""
    if not pathlib.Path(ckpt).is_file():
        return dict(ckpt=str(ckpt), available=False)
    with np.load(ckpt, allow_pickle=False) as z:
        if int(z['n_inner']) != 50 or int(z['seed']) != SEEDS[0] or int(z['done']) < 10:
            return dict(ckpt=str(ckpt), available=False)
        old = {k: z[k][:10] for k in CHUNK_KEYS}; full_old = z['full']
    parts = [np.load(chunk_file(CAL, label, SEEDS[0], lo, hi), allow_pickle=False) for lo, hi in CHUNKS]
    new = {k: np.concatenate([p[k] for p in parts])[:10] for k in CHUNK_KEYS}
    with np.load(CAL / (label + '.job.npz'), allow_pickle=False) as j:
        full_same = bool(np.array_equal(j['full'], full_old, equal_nan=True))
    bad = [k for k in CHUNK_KEYS if not np.array_equal(old[k], new[k], equal_nan=True)]
    return dict(ckpt=str(ckpt), available=True, rows=10, values_compared=int(sum(old[k].size for k in CHUNK_KEYS)),
                entries_differing=bad, full_sample_values_equal=full_same)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--suffix', default='')
    ap.add_argument('--skip-timing', action='store_true')
    a = ap.parse_args()
    sfx = a.suffix
    outf = OUT / ('TEST_RC_CALIB_CHUNKS_v13%s.json' % sfx)
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    log = OUT / ('test_rc_calib_chunks%s_log.txt' % sfx)
    other_cwd = pathlib.Path(tempfile.gettempdir())
    doc = dict(code='test_rc_calib_chunks_v13.py', started=time.strftime('%Y-%m-%d %H:%M:%S'), sizes=SIZES, chunks=CHUNKS, seeds=SEEDS,
               note='old runs only; the laptop was shared and heavily loaded during every measurement', not_compared=list(SKIP) + ['seconds*'],
               log=str(log))
    progs = [('lead', 'rc_c_lead_v13.py', 'rc_lead' + sfx, [], 'RC_C_LEAD_TESTOLD_b200_o12_i50',
              OUT / 'ckpt' / 'RC_C_LEAD_TESTOLD_b200_o10_i50_v2_inner1.npz'),
             ('cutin', 'rc_c_cutin_v13.py', 'rc_cutin' + sfx, ['--truth-file', str(OUT / 'RC_C_CUTIN_TESTOLD_TRUTH_v13.json')],
              'RC_C_CUTIN_TESTOLD_b200_o12_i50', OUT / 'ckpt' / 'RC_C_CUTIN_TESTOLD_b200_o10_i50_inner1.npz')]
    ok = True
    for key, prog, label, extra, stem, ckpt in progs:
        base = PY + [HERE / prog, '--test-old'] + SIZES + ['--workers', '2'] + extra
        d = {}
        d['seconds_inprocess'] = run(base + ['--tag', '_inproc' + sfx], HERE, log)
        d['seconds_export'] = run(base + ['--calib', 'export', '--calib-label', label, '--tag', '_pod' + sfx], HERE, log)
        cmds = [PYR + [HERE / 'rc_calib_remote_v13.py', CAL, label, '--seeds', str(s), '--outer', '%d:%d' % (lo, hi), '--threads', '1']
                for s in SEEDS for lo, hi in CHUNKS]
        t0 = time.time(); run_pairs(cmds, other_cwd, log); d['seconds_chunks_wall'] = time.time() - t0
        d['runner_calls'] = [' '.join(str(c) for c in cmd[3:]) for cmd in cmds]
        d['seconds_import'] = run(base + ['--calib', 'import', '--calib-chunks', CAL, '--calib-label', label, '--tag', '_pod' + sfx], HERE, log)
        fa = OUT / ('%s_inproc%s.json' % (stem, sfx)); fb = OUT / ('%s_pod%s.json' % (stem, sfx))
        d['json'] = compare_json(fa, fb)
        jb = json.loads(fb.read_text(encoding='utf-8'))
        d['second_seed_used'] = jb['calibration']['second_seed_run']; d['needed_second_seed'] = jb['calibration']['needed_second_seed']
        d['pending_output'] = str(OUT / ('%s_pod%s.PENDING.json' % (stem, sfx)))
        d['meta'] = json.loads((CAL / (label + '.meta.json')).read_text(encoding='utf-8'))
        d['old_code_checkpoint'] = old_ckpt_check(label, ckpt)
        d['pass'] = bool(d['json']['values_differing'] == 0 and not d['old_code_checkpoint'].get('entries_differing'))
        ok = ok and d['pass']
        doc[key] = d
        print('%s: %d values compared, %d differ; old-code checkpoint: %s' % (key, d['json']['values_compared'],
              d['json']['values_differing'], d['old_code_checkpoint']), flush=True)

    # ---- standalone: only the job files, the runner and its module, in a fresh folder outside the project
    label = 'rc_lead' + sfx
    sd = pathlib.Path(tempfile.mkdtemp(prefix='rc_standalone_'))
    files = [label + '.job.npz', label + '.meta.json']
    for f in files:
        shutil.copy2(CAL / f, sd / f)
    for f in ('rc_calib_remote_v13.py', 'rc_kern_v13.py'):
        shutil.copy2(HERE / f, sd / f)
    lo, hi = CHUNKS[1]
    cmd = PYR + [sd / 'rc_calib_remote_v13.py', sd, label, '--seeds', str(SEEDS[0]), '--outer', '%d:%d' % (lo, hi), '--threads', '1']
    cwd2 = pathlib.Path.home()
    secs = run(cmd, cwd2, log)
    st = compare_chunks(chunk_file(CAL, label, SEEDS[0], lo, hi), chunk_file(sd, label, SEEDS[0], lo, hi))
    st.update(folder=str(sd), files_copied=files + ['rc_calib_remote_v13.py', 'rc_kern_v13.py'], working_directory=str(cwd2),
              call=' '.join(str(c) for c in cmd), seconds=secs, folder_listing_after=sorted(p.name for p in sd.iterdir()),
              **{'pass': not st['entries_differing']})
    doc['standalone'] = st; ok = ok and st['pass']
    print('standalone: %s' % ('equal' if st['pass'] else st['entries_differing']), flush=True)

    # ---- timing: full inner size (1,000), one thread, old lead job
    if not a.skip_timing:
        tl = 'rc_lead_timing' + sfx
        run(PY + [HERE / 'rc_c_lead_v13.py', '--test-old', '--boot', '200', '--outer', '4', '--inner', '1000', '--mc', '200', '--workers', '2',
                  '--no-library', '--calib', 'export', '--calib-label', tl, '--tag', '_timing' + sfx], HERE, log)
        run(PYR + [HERE / 'rc_calib_remote_v13.py', CAL, tl, '--seeds', str(SEEDS[0]), '--outer', '0:3', '--threads', '1'], other_cwd, log)
        with np.load(chunk_file(CAL, tl, SEEDS[0], 0, 3), allow_pickle=False) as z:
            s_all = float(z['seconds']); s_first = float(z['seconds_first_outer'])
        meta = json.loads((CAL / (tl + '.meta.json')).read_text(encoding='utf-8'))
        doc['timing'] = dict(job=tl, n_run=meta['n_run'], n_inner=meta['n_inner'], threads=1, outer_samples=3, seconds_total=s_all,
                             seconds_first_outer_incl_compilation=s_first, seconds_per_outer_sample=(s_all - s_first) / 2.,
                             job_bytes=meta['job_bytes'], note='loaded laptop; an upper bound')
        print('timing: %.1f s per outer sample (1 thread, %d inner)' % (doc['timing']['seconds_per_outer_sample'], meta['n_inner']), flush=True)
    doc['all_pass'] = bool(ok); doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(outf, 'x', encoding='utf-8') as f:
        json.dump(doc, f, indent=1, default=str)
    print('%s; written %s' % ('ALL PASS' if ok else 'FAILED', outf))


if __name__ == '__main__':
    main()
