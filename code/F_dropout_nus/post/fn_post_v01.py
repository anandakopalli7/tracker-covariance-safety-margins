r"""AMENDMENT_12 sec. 5b, the run after LOCK_A12c / LOCK_A12e (sec. 5b.10): a NEW helper, written 22 Nov 2026 03:40 EST (Claude Opus
5.5, worker of package F) after the freeze work\locks\FREEZE_F_NUS5B.json. It changes no frozen file and computes no value; it uses the
frozen fn_pods_v01.py (imported read only) to move files and start the frozen run script. Additions only:
  preflight            every FREEZE_F_NUS5B entry and both bundle tars match their recorded SHA-256; both locks exist
  stage-locks          pods\locks_bundle.tar.gz (+ .json): LOCK_A12c.txt and LOCK_A12e.txt at ARS_TRIAL/revision_v13/ (fn_pods' 'lock'
                       bundle carries only LOCK_A12c.txt)
  start NAME           runs code/fn_run_masked_v01.sh ONCE on the pod (refuses if its log exists), from /root/fn/job with fn_pods.ENV,
                       log /root/fn/masked_val.log (copied to the folder's logs/ at the end of the run by `status --copy`)
  status NAME [--copy] tail of the run log; --copy copies it into .../F_dropout_nus/logs/masked_val_run.log for the fetch
  values               out\FN5B_VALUES_v01.json from out\masked_val\FN5B_RESULTS_v01.json (the DR-style values; refuses to overwrite)
Usage: python -I -B fn_post_v01.py CMD ...
"""
import hashlib, json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent
HOME = HERE.parent
V13 = HOME.parents[1]
sys.path.insert(0, str(HOME / 'code'))
sys.dont_write_bytecode = True
import fn_pods_v01 as FP                               # noqa: E402  (frozen; read only)

LOCKS = ('LOCK_A12c.txt', 'LOCK_A12e.txt')
RUNLOG = FP.R + '/masked_val.log'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def preflight():
    fz = json.loads((V13 / 'work' / 'locks' / 'FREEZE_F_NUS5B.json').read_text(encoding='utf-8'))
    bad = [e['path'] for e in fz['entries'] if sha(V13 / e['path']) != e['sha256']]
    for b in ('code', 'val'):
        m = json.loads((FP.STAGE / ('%s_bundle.json' % b)).read_text(encoding='utf-8'))
        if sha(FP.STAGE / ('%s_bundle.tar.gz' % b)) != m['tar_sha256']:
            bad.append('%s_bundle.tar.gz' % b)
    missing = [l for l in LOCKS if not (V13 / l).is_file()]
    print(json.dumps(dict(freeze_entries=len(fz['entries']), mismatches=bad, locks_missing=missing,
                          locks={l: sha(V13 / l) for l in LOCKS if (V13 / l).is_file()})))
    if bad or missing:
        raise SystemExit('PREFLIGHT FAILED')


def stage_locks():
    preflight()
    FP.bundle(FP.STAGE / 'locks_bundle.tar.gz', [(V13 / l, FP.A13 + l) for l in LOCKS])


def start(name):
    out = FP.pv.ssh(name, 'test -e %s && echo EXISTS || echo NEW' % RUNLOG, timeout=60).stdout
    if 'NEW' not in out:
        raise SystemExit('REFUSED: the run log exists; the run is made once')
    chk = FP.ssh(name, 'test -f %s/ARS_TRIAL/revision_v13/LOCK_A12c.txt && test -f %s/ARS_TRIAL/revision_v13/LOCK_A12e.txt && echo LOCKS_OK'
                 % (FP.R, FP.R))
    if 'LOCKS_OK' not in chk:
        raise SystemExit('REFUSED: the locks are not on the pod')
    FP.ssh(name, '%s && cd %s/job && (setsid nohup bash %s/code/fn_run_masked_v01.sh > %s 2>&1 < /dev/null &) ; sleep 2; echo started'
           % (FP.ENV, FP.R, FP.HN, RUNLOG))
    print('started fn_run_masked_v01.sh', FP.pv.est())


def status(name, copy=False):
    print(FP.ssh(name, 'tail -n 6 %s | cut -c1-400; for d in tracks_masked arrays_masked; do echo $d $(ls %s/cache/$d/val 2>/dev/null | '
                       'grep -vc tmp); done; ls %s/out/masked_val 2>/dev/null; uptime' % (RUNLOG, FP.HN, FP.HN)))
    if copy:
        FP.ssh(name, 'cp %s %s/logs/masked_val_run.log' % (RUNLOG, FP.HN))
        print('copied the run log into logs/')


def values():
    src = HOME / 'out' / 'masked_val' / 'FN5B_RESULTS_v01.json'
    outf = HOME / 'out' / 'FN5B_VALUES_v01.json'
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    d = json.loads(src.read_text(encoding='utf-8'))
    q = d['sequence']; cal = d['calibration']; de = d['descriptive']
    doc = dict(name='FN5B_VALUES_v01', amendment='AMENDMENT_12 sec. 5b (masked val run, once, after LOCK_A12c and LOCK_A12e)',
               source=dict(file='out\\masked_val\\FN5B_RESULTS_v01.json', sha256=sha(src)),
               locks={l: sha(V13 / l) for l in LOCKS}, written=time.strftime('%Y-%m-%d %H:%M:%S'),
               dr_style=dict(
                   DR0_room=dict(passes=q['room']['passes'], R_gl_pp=q['room']['R_gl_pp'], ci=cal['R']['ci'], level=cal['R']['level'],
                                 share_resamples_R_nonpositive=q['room']['share_resamples_R_nonpositive'], status=q['room']['status']),
                   DR1_E5N=dict(passes=q['E5_N']['passes'], c=q['E5_N']['c'], c_ci=q['E5_N']['c_ci'], c_level=cal['c']['level'],
                                cdiff=q['E5_N']['cdiff'], cdiff_ci=q['E5_N']['cdiff_ci'], cdiff_level=cal['cdiff']['level'],
                                status=q['E5_N']['status']),
                   DR2_class=dict(classification=q['N_class']['classification'], passes=q['N_class']['passes'], r=q['N_class']['r'],
                                  r_ci=q['N_class']['r_ci'], r_level=cal['r']['level'], efficiency=q['N_class']['efficiency_r_over_c'],
                                  status=q['N_class']['status']),
                   p_r=d['p_r'], E5_N=dict(m=d['E5x']['m'], A=d['E5x']['A'], ratio_summary=d['ratio_summary_N_F0']),
                   second_inner_seed=d['second_inner_seed'], calibration={k: dict(level=v['level'], reason=v['reason'])
                                                                          for k, v in cal.items()}),
               descriptive=dict(n_scenes=d['n_scenes'], n_evaluated=de['n_evaluated'], n_in_dropout=de['n_in_dropout'],
                                share_evaluated_in_dropout=de['share_evaluated_in_dropout'], keyframes=de['keyframes'],
                                keyframes_masked=de['keyframes_masked'], masked_share_keyframes=de['masked_share_keyframes'],
                                in_dropout=de.get('in_dropout'), ratio_summary_in_dropout=de.get('ratio_summary_in_dropout'),
                                R_deceq=d['library_point']['R_deceq'], R_deceq_ci95=d['R_deceq_ci95'], D_N_deceq=d['D_N_deceq']),
               checks=d['checks'], verify=d['verify'], values=d['values'])
    outf.write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print('WROTE', outf, sha(outf))


if __name__ == '__main__':
    a = sys.argv[1:]
    c = a[0]
    if c == 'preflight': preflight()
    elif c == 'stage-locks': stage_locks()
    elif c == 'start': start(a[1])
    elif c == 'status': status(a[1], '--copy' in a)
    elif c == 'values': values()
    else: raise SystemExit('unknown command')
