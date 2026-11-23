"""Recount of test Y (A11 6b): standalone runner of chunks of the A10 section 2.6 double bootstrap (copy of rc_x_calib_remote_v13.py with
rc_y_kern_v13 in place of rc_x_kern_v13; 21 Nov 2026, Claude Sonnet 5.5). No first program and no pod tool was read.

Call (one process per call; any working directory; Linux or Windows; CPython 3.12, numpy, numba, nothing else):

    python -I -B rc_y_calib_remote_v13.py JOBDIR LABEL --seeds SEED [SEED] --outer LO:HI --threads 1

Needs in JOBDIR <LABEL>.job.npz and <LABEL>.meta.json (written by rc_y_twin_v13.py --calib export) and next to this script rc_y_kern_v13.py
and rc_kern_v13.py. Writes JOBDIR/<LABEL>_<SEED>_o<LO>_<HI>.npz (rows LO..HI-1 of the double bootstrap of that inner seed); an existing chunk
is not computed again. Details as rc_x_calib_remote_v13.py.
"""
import os, sys


def _threads_from_argv(argv):
    for i, x in enumerate(argv):
        if x == '--threads' and i + 1 < len(argv):
            return argv[i + 1]
        if x.startswith('--threads='):
            return x.split('=', 1)[1]
    return '1'


# thread counts and the BLAS kernel are fixed BEFORE numpy and numba are imported
_T = _threads_from_argv(sys.argv)
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_k] = '1'                       # BLAS is used on small arrays only; one thread, as in rc_core_v13
os.environ['NUMBA_NUM_THREADS'] = _T if _T.isdigit() and int(_T) > 0 else '1'
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')      # the BLAS kernel the exporting machine uses (same rounding of dot products)

import argparse, platform, time                # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # python -I: the script folder is not on sys.path
import numpy as np                             # noqa: E402
import numba                                   # noqa: E402
import rc_kern_v13 as KN                       # noqa: E402
import rc_y_kern_v13                       # noqa: E402,F401  (registers the statistic kind "ytwin")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('jobdir')
    ap.add_argument('label')
    ap.add_argument('--seeds', required=True, nargs='+', help='inner seed(s); several separated by blanks or commas')
    ap.add_argument('--outer', required=True, help='LO:HI, outer samples LO..HI-1')
    ap.add_argument('--threads', type=int, default=1)
    a = ap.parse_args()
    seeds = [int(x) for part in a.seeds for x in part.split(',') if x]
    try:
        lo, hi = (int(x) for x in a.outer.split(':'))
    except ValueError:
        raise SystemExit('REFUSED: --outer must be LO:HI')
    numba.set_num_threads(max(1, min(a.threads, numba.config.NUMBA_NUM_THREADS)))
    jobf = os.path.join(a.jobdir, a.label + '.job.npz')
    metaf = os.path.join(a.jobdir, a.label + '.meta.json')
    if not os.path.isfile(jobf):
        raise SystemExit('REFUSED: no job file %s' % jobf)
    sha = KN.sha256_file(jobf)
    if os.path.isfile(metaf):
        import json
        with open(metaf, encoding='utf-8') as f:
            meta = json.load(f)
        if meta.get('job_sha256') != sha:
            raise SystemExit('REFUSED: %s does not have the SHA-256 recorded in %s' % (jobf, metaf))
        if meta.get('label') != a.label:
            raise SystemExit('REFUSED: %s is the job of label %s' % (metaf, meta.get('label')))
        for s in seeds:
            if s not in meta.get('pod_seeds', [s]):
                print('note: seed %d is not in pod_seeds %s' % (s, meta.get('pod_seeds')), flush=True)
    else:
        print('note: no %s; the SHA-256 of the job file is recorded in the chunk unchecked' % metaf, flush=True)
    stat, J = KN.load_job(jobf)
    if str(J['label']) != a.label:
        raise SystemExit('REFUSED: %s holds label %s' % (jobf, str(J['label'])))
    n_outer = int(J['n_outer']); n_inner = int(J['n_inner'])
    if not (0 <= lo < hi <= n_outer):
        raise SystemExit('REFUSED: outer range %d:%d is not inside 0:%d' % (lo, hi, n_outer))
    for seed in seeds:
        outf = os.path.join(a.jobdir, '%s_%d_o%d_%d.npz' % (a.label, seed, lo, hi))
        if os.path.exists(outf):
            print('exists, not computed again: %s' % outf, flush=True)
            continue
        t0 = time.time()
        tfirst = [None]

        def progress(done, t0=t0, tfirst=tfirst):
            if tfirst[0] is None and done > lo:
                tfirst[0] = time.time() - t0               # first outer sample: includes compilation of the kernel
            if done > lo and ((done - lo) % 10 == 0 or done == hi):
                print('  %s seed %d: outer %d of %d:%d (%.0f s)' % (a.label, seed, done, lo, hi, time.time() - t0), flush=True)

        R = KN.calib_rows(stat, J, seed, lo, hi, progress)
        secs = time.time() - t0
        tmp = outf + '.tmp%d' % os.getpid()
        with open(tmp, 'wb') as f:
            np.savez(f, label=np.array(a.label), seed=np.int64(seed), lo=np.int64(lo), hi=np.int64(hi), n_outer=np.int64(n_outer),
                     n_inner=np.int64(n_inner), job_sha256=np.array(sha), seconds=np.float64(secs),
                     seconds_first_outer=np.float64(tfirst[0] if tfirst[0] is not None else np.nan), threads=np.int64(numba.get_num_threads()),
                     versions=np.array('python %s; numpy %s; numba %s; %s; OPENBLAS_CORETYPE=%s'
                                       % (platform.python_version(), np.__version__, numba.__version__, platform.platform(),
                                          os.environ.get('OPENBLAS_CORETYPE'))),
                     **{k: R[k] for k in KN.CHUNK_KEYS})
        os.replace(tmp, outf)
        print('written %s (%d outer samples x %d inner, %.1f s; %.2f s per outer sample after the first)'
              % (outf, hi - lo, n_inner, secs, (secs - (tfirst[0] or 0.)) / max(1, hi - lo - 1)), flush=True)


if __name__ == '__main__':
    main()
