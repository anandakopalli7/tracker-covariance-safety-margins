r"""v13 sprint (AMENDMENT_11 s6): run the FROZEN second program for IMMr (recount_fresh\immr_v03.py, FREEZE_B_add8, on top of
recount_fresh.py and rf_core.py of FREEZE_B_add3) on a Linux CPU pod, as the K = 20,000 recount of the seven variants ran on
20 Nov (b_recount_pod_v02.py, pod claude-v13b-rc03). New file, 21 Nov 2026 (Claude Opus 5.5). Tooling only: no recount code is
changed; b_pods_v02.py and pod_place_v02.py (frozen in add8) are reused unchanged.

  stage            pods\stage_immr\immr_inputs.tar.gz: every input the IMMr path reads (the three lock files, CASES_C_v13.json,
                   REPLACEMENTS_C_v13.json, the 105 B1R arrays out\retrack_fresh\B1R\<rid>_arrays.npz, optA_lib_v02.py), each under
                   the exact path string the frozen code builds, with its SHA-256; the code (immr_v03.py checked against add8;
                   recount_fresh.py, rf_core.py, b6tu.py checked against add3). REFUSES unless LOCK_A10_2, LOCK_A10_2c and LOCK_A11 exist
                   and all 105 B1R arrays are present.
  up NAME          create the pod (b_pods_v02.create), upload, place and SHA-check every input (pod_place_v02.py), install CPython
                   3.12 + numpy 2.5.4 + scipy 1.18.1 with uv.
  run NAME [K]     start immr_v03.py --fresh --K K (default 20000), OPENBLAS_NUM_THREADS=1, log /root/logs/IMMr.log.
  status NAME      log tail, EXIT file, free memory.
  fetch NAME       copy part_fresh_IMMr.json and boot_IMMr.npz on the pod with SHA-256, download, check, place in recount_fresh\out\
                   (REFUSES to overwrite a different existing file).
  down NAME        only after fetch: runpodctl pod delete; counts only if rc = 0 AND pod get returns not found AND the id is absent
                   from pod list (coordinator rule, 20 Nov); only then TERMINATED and the spend-log row are written.
Usage: python -I -B -X utf8 b_recount_pod_v03.py stage|up|run|status|fetch|down [NAME] [K]
"""
import hashlib, json, os, pathlib, sys, tarfile, time
os.environ.setdefault('GODEBUG', 'netdns=go')          # runpodctl DNS on this laptop
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import b_pods_v02 as PV

W = HERE.parents[1]                        # ...\revision_v13\work
B = W / 'B_retrack'; CDL = W / 'CD_capture'
RCL = B / 'recount_fresh'
STAGE = HERE / 'stage_immr'
V13S = r'ARS_TRIAL\revision_v13'      # the strings the frozen code uses
CDS = V13S + r'\work\CD_capture'
BRS = V13S + r'\work\B_retrack'
OPTA_DIR_S = r'<library folder>\code'   # rf_core.py sys.path entry
OPTA = pathlib.Path(OPTA_DIR_S) / 'optA_lib_v02.py'
CODE_ADD3 = ['recount_fresh.py', 'rf_core.py', 'b6tu.py']
CODE_ADD8 = ['immr_v03.py']
CODE = CODE_ADD3 + CODE_ADD8
PY = '/opt/rcv/bin/python'
OUTS = ['part_fresh_IMMr.json', 'boot_IMMr.npz']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def lead_ids():
    cases = json.loads((CDL / 'CASES_C_v13.json').read_text(encoding='utf-8'))['cases']
    rep = json.loads((CDL / 'REPLACEMENTS_C_v13.json').read_text(encoding='utf-8'))['replacements']
    return sorted('pc13_%s_native' % rep.get(c['case'], c['case']) for c in cases if c['family'] == 'lead_braking')


def frozen_sha(addfile, names):
    d = json.loads((W / 'locks' / addfile).read_text(encoding='utf-8'))
    return {pathlib.Path(e['path']).name: e['sha256'] for e in d['new'] + d['changed']
            if 'recount_fresh' in e['path'] and pathlib.Path(e['path']).name in names}


def stage():
    locks = [W.parent / n for n in ('LOCK_A10_2.txt', 'LOCK_A10_2c.txt', 'LOCK_A11.txt')]
    miss = [str(p) for p in locks if not p.is_file()]
    if miss:
        raise SystemExit('REFUSED: lock files missing: %s' % miss)
    frozen = dict(frozen_sha('FREEZE_B_add3.json', CODE_ADD3), **frozen_sha('FREEZE_B_add8.json', CODE_ADD8))
    code_sha = {c: sha(RCL / c) for c in CODE}
    bad = [c for c in CODE if frozen.get(c) != code_sha[c]]
    if bad:
        raise SystemExit('REFUSED: recount code differs from FREEZE_B_add3/add8: %s' % bad)
    ids = lead_ids()
    assert len(ids) == 105 and len(set(ids)) == 105
    arr = [B / 'out' / 'retrack_fresh' / 'B1R' / (rid + '_arrays.npz') for rid in ids]
    gone = [p.name for p in arr if not p.is_file()]
    if gone:
        raise SystemExit('REFUSED: %d B1R arrays missing (re-track not finished): %s' % (len(gone), gone[:5]))
    ent = []

    def add(local, flat, kind):
        ent.append(dict(i=len(ent), local=str(local), flat=flat, kind=kind, sha256=sha(local)))
    for p in locks:
        add(p, V13S + '\\' + p.name, 'lock')
    add(CDL / 'CASES_C_v13.json', CDS + r'\CASES_C_v13.json', 'cases')
    add(CDL / 'REPLACEMENTS_C_v13.json', CDS + r'\REPLACEMENTS_C_v13.json', 'cases')
    for rid, p in zip(ids, arr):
        add(p, r'%s\out\retrack_fresh\B1R\%s_arrays.npz' % (BRS, rid), 'arrays_B1R')
    add(OPTA, OPTA_DIR_S + '/optA_lib_v02.py', 'optA_lib (read-only, imported via rf_core sys.path)')
    man = dict(written=PV.est(), code=CODE, code_sha256=code_sha,
               freeze='FREEZE_B_add3 sha256 %s; FREEZE_B_add8 sha256 %s' % (sha(W / 'locks' / 'FREEZE_B_add3.json'),
                                                                          sha(W / 'locks' / 'FREEZE_B_add8.json')),
               inputs=[{k: v for k, v in e.items() if k != 'local'} for e in ent], locals={e['i']: e['local'] for e in ent})
    STAGE.mkdir(exist_ok=True)
    (STAGE / 'manifest.json').write_text(json.dumps(man, indent=1), encoding='utf-8')
    tgz = STAGE / 'immr_inputs.tar.gz'
    with tarfile.open(tgz, 'w:gz', compresslevel=6) as t:
        t.add(STAGE / 'manifest.json', arcname='manifest.json')
        for c in CODE:
            t.add(RCL / c, arcname='code/' + c)
        t.add(HERE / 'pod_place_v02.py', arcname='pod_place_v02.py')
        for e in ent:
            t.add(e['local'], arcname='in/%d' % e['i'])
    print(json.dumps(dict(inputs=len(ent), tar=str(tgz), mb=round(tgz.stat().st_size / 1e6, 1), sha256=sha(tgz))))


def ssh(name, cmd, timeout=1800):
    r = PV.ssh(name, cmd, timeout=timeout)
    if r.returncode != 0:
        raise SystemExit('%s: ssh failed rc=%d: %s %s' % (name, r.returncode, r.stdout[-800:], r.stderr[-800:]))
    return r.stdout


def up(name, gpu='NVIDIA GeForce RTX 4090', deadline_h=3.0):
    tgz = STAGE / 'immr_inputs.tar.gz'
    if not tgz.is_file():
        raise SystemExit('REFUSED: stage first')
    if not (PV.PODS / name / 'pod.json').is_file():
        PV.create(name, gpu, deadline_h, 'package B: frozen second program for IMMr (immr_v03, A11 s6) at K=20000')
    print(ssh(name, 'nproc; free -g | head -2; df -h /root | tail -1'))
    r = PV.sftp(name, ['-mkdir /root/stage', 'put "%s" "/root/stage/immr_inputs.tar.gz"' % tgz], timeout=3600)
    if r.returncode != 0:
        raise SystemExit('upload failed: ' + r.stderr[-500:])
    got = ssh(name, 'sha256sum /root/stage/immr_inputs.tar.gz').split()[0]
    if got != sha(tgz):
        raise SystemExit('tar SHA-256 differs after upload')
    print(ssh(name, 'cd /root/stage && tar xzf immr_inputs.tar.gz && mkdir -p /root/rc /root/logs && python3 pod_place_v02.py manifest.json /root/stage'))
    setup = ('(python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/rcv && uv pip install -q --python %s numpy==2.5.4 scipy==1.18.1) '
             '> /root/logs/setup.log 2>&1; %s -c "import sys,numpy,scipy; print(sys.version.split()[0], numpy.__version__, scipy.__version__)"' % (PY, PY))
    print(ssh(name, setup))
    (PV.PODS / name / 'UP_DONE').write_text(PV.est() + ' tar ' + sha(tgz) + '\n', encoding='utf-8')


def run(name, K=20000):
    script = ['cd /root/rc', 'export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1',
              '%s -I -B -X utf8 immr_v03.py --fresh --K %d > /root/logs/IMMr.log 2>&1; echo "IMMr exit $?" >> /root/logs/EXIT' % (PY, K),
              'echo ALL_DONE >> /root/logs/EXIT']
    (PV.PODS / name / 'run.sh').write_text('\n'.join(script) + '\n', encoding='ascii', newline='\n')
    r = PV.sftp(name, ['put "%s" "/root/run.sh"' % (PV.PODS / name / 'run.sh')])
    if r.returncode != 0:
        raise SystemExit('upload of run.sh failed')
    r = PV.ssh(name, 'setsid nohup bash /root/run.sh > /root/logs/run.log 2>&1 < /dev/null & sleep 5; echo started; cat /root/logs/EXIT 2>/dev/null; tail -3 /root/logs/IMMr.log', 120)
    print(r.returncode, r.stdout, r.stderr[-300:])


def status(name):
    print(ssh(name, 'cat /root/logs/EXIT 2>/dev/null; tail -4 /root/logs/IMMr.log | cut -c1-200; ls -la "/root/rc\\out" 2>/dev/null; ls /root | head -30; free -g | head -2', 120))


def fetch(name):
    cmd = ['mkdir -p /root/outpkg && cd /root']
    for f in OUTS:
        cmd.append('cp "/root/rc\\out\\%s" /root/outpkg/%s' % (f, f))
    cmd.append('cd /root/outpkg && sha256sum * > SHA256SUMS && tar czf /root/outpkg.tar.gz * && sha256sum /root/outpkg.tar.gz')
    out = ssh(name, ' && '.join(cmd))
    dl = PV.PODS / name / 'outpkg.tar.gz'
    r = PV.sftp(name, ['get "/root/outpkg.tar.gz" "%s"' % dl], timeout=1800)
    if r.returncode != 0 or sha(dl) != out.split()[-2]:
        raise SystemExit('download failed or SHA-256 differs')
    xd = PV.PODS / name / 'outpkg'; xd.mkdir(exist_ok=True)
    with tarfile.open(dl) as t:
        t.extractall(xd, filter='data')
    sums = dict(reversed(l.split()) for l in (xd / 'SHA256SUMS').read_text().splitlines() if l.strip())
    if sorted(sums) != sorted(OUTS):
        raise SystemExit('unexpected outputs: %s' % sorted(sums))
    bad = [f for f, h in sums.items() if sha(xd / f) != h]
    if bad:
        raise SystemExit('SHA-256 differs after download: %s' % bad)
    od = RCL / 'out'
    clash = [f for f in sums if (od / f).exists() and sha(od / f) != sums[f]]
    if clash:
        raise SystemExit('REFUSED: a different file already exists in recount_fresh\\out: %s' % clash)
    for f in sums:
        (od / f).write_bytes((xd / f).read_bytes())
        assert sha(od / f) == sums[f]
    (PV.PODS / name / 'FETCHED').write_text(PV.est() + '\n' + json.dumps(sums, indent=1), encoding='utf-8')
    print('fetched and checked:', json.dumps(sums, indent=1))


def down(name, note):
    d = PV.PODS / name
    if not (d / 'FETCHED').is_file():
        raise SystemExit('REFUSED: outputs not fetched yet')
    rec = json.loads((d / 'pod.json').read_text(encoding='utf-8'))
    pid = rec['id']
    log = d / 'delete.log'
    for attempt in range(1, 6):
        r = PV.rp('pod', 'delete', pid, check=False)
        with open(log, 'a', encoding='utf-8') as fh:
            fh.write('%s attempt %d rc=%d\n%s\n%s\n' % (PV.est(), attempt, r.returncode, r.stdout[-500:], r.stderr[-500:]))
        if r.returncode == 0:
            break
        time.sleep(30)
    else:
        raise SystemExit('%s: pod delete rc != 0 five times; TERMINATED not written, no spend row' % name)
    for attempt in range(1, 7):
        g = PV.rp('pod', 'get', pid, check=False)
        lst = PV.rp('pod', 'list', check=False)
        absent = lst.returncode == 0 and pid not in lst.stdout
        notfound = g.returncode != 0 and ('not_found' in (g.stdout + g.stderr) or '404' in (g.stdout + g.stderr))
        with open(d / 'get_after_delete.log', 'a', encoding='utf-8') as fh:
            fh.write('%s attempt %d get rc=%d %s %s | list rc=%d absent=%s\n'
                     % (PV.est(), attempt, g.returncode, g.stdout[-200:].strip(), g.stderr[-200:].strip(), lst.returncode, absent))
        if notfound and absent:
            break
        time.sleep(20)
    else:
        raise SystemExit('%s: delete rc=0 but the pod is still visible (get or list); TERMINATED not written, no spend row' % name)
    (d / 'TERMINATED').write_text('%s rc=0; get not_found; absent from list\n' % PV.est(), encoding='utf-8')
    PV.spend_row('terminate', pid, rec['gpu'], rec['costPerHr'], '%s; %s' % (name, note))


def main():
    c = sys.argv[1]
    if c == 'stage':
        stage()
    elif c == 'up':                                   # up NAME [GPU id]; 21 Nov 14:45: RTX 4090 out of stock (create refused, no pod)
        up(sys.argv[2], *sys.argv[3:4])
    elif c == 'run':
        run(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20000)
    elif c == 'status':
        status(sys.argv[2])
    elif c == 'fetch':
        fetch(sys.argv[2])
    elif c == 'down':
        down(sys.argv[2], 'package B IMMr recount: outputs fetched and SHA-256 checked')
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
