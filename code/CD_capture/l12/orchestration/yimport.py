"""Y-L12 import on l6 (the pod that ran the exports and holds the bundle): upload the merged first-program table(s) into analysis/out/calib and the
second program's chunk files into /root/yl/rc_chunks, then run both frozen programs with --intervals calibrated --calib import (same arguments as
the export, from pods/yl12_staging/ARGS.json), one after the other; fetch with ycheck/y_pods_l12_v13.py fetch afterwards.
Usage: python yimport.py up POD TABLE... | run POD THREADS | status POD"""
import json, pathlib, sys
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.path[:0] = [str(CD / 'ycheck'), str(CD / 'tools')]
import y_pods_l12_v13 as YP
BP = YP.BP; R = YP.R; A = YP.A
CAL = R + '/' + A + 'work/CD_capture/analysis/out/calib'


def up(pod, tables):
    for t in tables:
        BP.put(pod, t, CAL + '/' + pathlib.Path(t).name)
        h = BP.ssh(pod, 'sha256sum %s/%s' % (CAL, pathlib.Path(t).name)).split()[0]
        assert h == YP.sha(t), t
    chunks = sorted((CD / 'pods' / 'yl12_chunks').glob('rc_yl12_*_o*.npz'))
    tar = CD / 'pods' / 'yl12_staging' / 'rc_chunks.tar'
    import tarfile
    with tarfile.open(tar, 'w') as tf:
        for c in chunks: tf.add(c, arcname=c.name)
    BP.ssh(pod, 'mkdir -p %s/rc_chunks' % R)
    BP.put(pod, tar, R + '/rc_chunks.tar')
    BP.ssh(pod, 'cd %s/rc_chunks && tar xf ../rc_chunks.tar && rm ../rc_chunks.tar && sha256sum *.npz > ../rc_chunks.sha' % R)
    got = dict(reversed(l.split()) for l in BP.ssh(pod, 'cat %s/rc_chunks.sha' % R).splitlines() if l.strip())
    bad = [c.name for c in chunks if got.get(c.name) != YP.sha(c)]
    print('tables', len(tables), '| rc chunks', len(chunks), 'uploaded; sha mismatches', bad)


def run(pod, threads):
    g = json.loads((YP.STAGE / 'ARGS.json').read_text(encoding='utf-8'))
    fa = ('--cases-sha %s --b2-dir %s/b2_l12/B2 --b2-manifest %s/b2_l12/%s --b2-manifest-sha %s --cv0-dir %s/%swork/CD_capture/arrays_l12/CV0'
          % (g['cases_sha'], R, R, g['manifest'], g['manifest_sha'], R, A))
    cmd = ('%s NUMBA_NUM_THREADS=%d && cd %s/job && (setsid nohup bash -c "%s -I -B -X utf8 %s --intervals calibrated --calib import %s > %s/first_import.log 2>&1; '
           '%s -I -B -X utf8 %s --intervals calibrated --calib import --calib-chunks %s/rc_chunks %s > %s/second_import.log 2>&1" > /dev/null 2>&1 < /dev/null &) ; sleep 2; echo started'
           % (YP.ENV, int(threads), R, YP.PY, YP.FIRST, fa, R, YP.PY, YP.SECOND, R, fa, R))
    print(BP.ssh(pod, cmd).strip())


def status(pod):
    print(BP.ssh(pod, 'tail -2 %s/first_import.log 2>/dev/null; echo ---; tail -2 %s/second_import.log 2>/dev/null; echo; pgrep -fc [y]_twin_l12_v13 || true' % (R, R)).strip())


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'up': up(sys.argv[2], sys.argv[3:])
    elif c == 'run': run(sys.argv[2], int(sys.argv[3]))
    else: status(sys.argv[2])
