"""v13 package B: run B's FROZEN second program (recount_fresh, FREEZE_B_add3) on a Linux CPU pod (coordinator decision 20 Nov 09:28:
the laptop has no memory for it). New file, 20 Nov 2026 (Claude Opus 5.5). Tooling only: no recount code is changed.

  stage            write pods\\stage\\recount_inputs.tar.gz: every fresh input the frozen code reads, each under its index, a manifest with
                   the exact path string the code builds (B_FRESH_DEFINITIONS_v02.md section 2; recount_fresh.fresh_path, fresh_run_ids,
                   check_locks; b6tu.load_b6_inputs, capture_dir_fresh, realised_decel_rule) and the file's SHA-256; the frozen code files
                   (recount_fresh.py, rf_core.py, b6tu.py; SHA-256 checked against FREEZE_B_add3) and optA_lib_v02.py (read-only).
  up NAME          create the pod (b_pods_v02), upload the package and pod_place_v02.py, place and SHA-check every input on the pod,
                   install CPython 3.12 + numpy 2.5.4 + scipy 1.18.1 (the laptop's versions) with uv, print RAM and vCPUs.
  run NAME [K]     start the 7 tracker jobs (--fresh --variants X --K K) and the B6 job (--fresh --b6 --K K), K default 2000, in parallel if the
                   pod has >= 48 GB RAM, else in two waves; one process each, OPENBLAS_NUM_THREADS=1; logs /root/logs/.
  status NAME      tails of the logs, outputs present, free memory.
  fetch NAME       on the pod: copy the outputs to plain names with SHA-256; download; check; put them in recount_fresh\\out\\ under the
                   names the frozen --combine reads (part_fresh_<X>.json, boot_<X>.npz, part_fresh_b6.json, boot_b6.npz).
  down NAME        delete the pod (only after fetch), spend-log row.
The combine (recount_fresh.py --fresh --combine, which reads the TU part already computed) and the comparison run on the laptop.
Usage: python -I -B -X utf8 b_recount_pod_v02.py stage|up|run|status|fetch|down [NAME]
"""
import hashlib, json, os, pathlib, sys, tarfile, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import b_pods_v02 as PV

W = HERE.parents[1]                        # ...\revision_v13\work
B = W / 'B_retrack'; CDL = W / 'CD_capture'
RCL = B / 'recount_fresh'
STAGE = HERE / 'stage'
V13S = r'ARS_TRIAL\revision_v13'      # the strings the frozen code uses (recount_fresh.py, b6tu.py)
CDS = V13S + r'\work\CD_capture'
BRS = V13S + r'\work\B_retrack'
OPTA_DIR_S = r'<library folder>\code'   # rf_core.py sys.path entry
OPTA = pathlib.Path(OPTA_DIR_S) / 'optA_lib_v02.py'
CODE = ['recount_fresh.py', 'rf_core.py', 'b6tu.py']
NAMES = ['CV', 'IMM', 'CV2', 'CA', 'AQ', 'IMM090', 'IMM098']
VARS = {'CV': 'CV0', 'IMM': 'B1', 'CV2': 'B3', 'CA': 'B4', 'AQ': 'B2', 'IMM090': 'B1_d090', 'IMM098': 'B1_d098'}
PY = '/opt/rcv/bin/python'


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


def stage():
    add3 = json.loads((W / 'locks' / 'FREEZE_B_add3.json').read_text(encoding='utf-8'))
    frozen = {pathlib.Path(e['path']).name: e['sha256'] for e in add3['new'] + add3['changed'] if 'recount_fresh' in e['path']}
    code_sha = {c: sha(RCL / c) for c in CODE}
    bad = [c for c in CODE if frozen.get(c) != code_sha[c]]
    if bad:
        raise SystemExit('REFUSED: recount code differs from FREEZE_B_add3: %s' % bad)
    ent = []
    def add(local, flat, kind):                      # noqa: E306
        ent.append(dict(i=len(ent), local=str(local), flat=flat, kind=kind, sha256=sha(local)))
    add(W.parent / 'LOCK_A10_2.txt', V13S + r'\LOCK_A10_2.txt', 'lock')
    add(W.parent / 'LOCK_A10_2c.txt', V13S + r'\LOCK_A10_2c.txt', 'lock')
    add(CDL / 'CASES_C_v13.json', CDS + r'\CASES_C_v13.json', 'cases')
    add(CDL / 'REPLACEMENTS_C_v13.json', CDS + r'\REPLACEMENTS_C_v13.json', 'cases')
    ids = lead_ids()
    assert len(ids) == 105
    for rid in ids:
        for v in ('CV0', 'B1', 'RSX'):
            add(CDL / 'arrays' / v / (rid + '.npz'), r'%s\arrays\%s\%s.npz' % (CDS, v, rid), 'arrays_' + v)
        for v in ('B3', 'B4', 'B2', 'B1_d090', 'B1_d098'):
            add(B / 'out' / 'retrack_fresh' / v / (rid + '_arrays.npz'), r'%s\out\retrack_fresh\%s\%s_arrays.npz' % (BRS, v, rid), 'arrays_' + v)
        add(B / 'out' / 'fresh_b6' / 'clear' / (rid + '.npz'), r'%s\out\fresh_b6\clear\%s.npz' % (BRS, rid), 'b6_clear')
        caps = [p for p in (CDL / 'runs' / rid / rid / 'capture').iterdir() if p.is_dir()]
        assert len(caps) == 1, rid
        marker = r'%s\work\CD_capture\runs\%s\%s\capture\%s' % (V13S, rid, rid, caps[0].name) + '\\\\'   # glob(r'...\capture\*\\') match
        ent.append(dict(i=len(ent), local=None, flat=marker, kind='glob_marker', marker=True, sha256=hashlib.sha256(b'').hexdigest()))
        add(caps[0] / 'evaluation_truth.jsonl', marker + 'evaluation_truth.jsonl', 'truth')
        add(caps[0] / 'contract.json', marker + 'contract.json', 'contract')
    add(OPTA, OPTA_DIR_S + '/optA_lib_v02.py', 'optA_lib (read-only, imported via rf_core sys.path)')
    man = dict(written=PV.est(), code=CODE, code_sha256=code_sha, freeze='FREEZE_B_add3 sha256 ' + sha(W / 'locks' / 'FREEZE_B_add3.json'),
               inputs=[{k: v for k, v in e.items() if k != 'local'} for e in ent], locals={e['i']: e['local'] for e in ent})
    STAGE.mkdir(exist_ok=True)
    (STAGE / 'manifest.json').write_text(json.dumps(man, indent=1), encoding='utf-8')
    tgz = STAGE / 'recount_inputs.tar.gz'
    with tarfile.open(tgz, 'w:gz', compresslevel=6) as t:
        t.add(STAGE / 'manifest.json', arcname='manifest.json')
        for c in CODE:
            t.add(RCL / c, arcname='code/' + c)
        t.add(HERE / 'pod_place_v02.py', arcname='pod_place_v02.py')
        for e in ent:
            if e['local']:
                t.add(e['local'], arcname='in/%d' % e['i'])
    print(json.dumps(dict(inputs=len(ent), tar=str(tgz), mb=round(tgz.stat().st_size / 1e6, 1), sha256=sha(tgz))))


def ssh(name, cmd, timeout=1800):
    r = PV.ssh(name, cmd, timeout=timeout)
    if r.returncode != 0:
        raise SystemExit('%s: ssh failed rc=%d: %s %s' % (name, r.returncode, r.stdout[-800:], r.stderr[-800:]))
    return r.stdout


def up(name, deadline_h=4.0):
    tgz = STAGE / 'recount_inputs.tar.gz'
    if not (PV.PODS / name / 'pod.json').is_file():
        PV.create(name, 'NVIDIA GeForce RTX 4090', deadline_h, 'package B: frozen second program (recount_fresh) on fresh runs; laptop out of memory')
    print(ssh(name, 'nproc; free -g | head -2; df -h /root | tail -1'))
    r = PV.sftp(name, ['-mkdir /root/stage', 'put "%s" "/root/stage/recount_inputs.tar.gz"' % tgz], timeout=3600)
    if r.returncode != 0:
        raise SystemExit('upload failed: ' + r.stderr[-500:])
    got = ssh(name, 'sha256sum /root/stage/recount_inputs.tar.gz').split()[0]
    if got != sha(tgz):
        raise SystemExit('tar SHA-256 differs after upload')
    print(ssh(name, 'cd /root/stage && tar xzf recount_inputs.tar.gz && mkdir -p /root/rc /root/logs && python3 pod_place_v02.py manifest.json /root/stage'))
    setup = ('(python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/rcv && uv pip install -q --python %s numpy==2.5.4 scipy==1.18.1) '
             '> /root/logs/setup.log 2>&1; %s -c "import sys,numpy,scipy; print(sys.version.split()[0], numpy.__version__, scipy.__version__)"' % (PY, PY))
    print(ssh(name, setup))
    (PV.PODS / name / 'UP_DONE').write_text(PV.est() + ' tar ' + sha(tgz) + '\n', encoding='utf-8')


def run(name, K=2000):
    mem = int(ssh(name, "free -g | awk '/Mem:/{print $2}'").strip())
    jobs = [('--fresh --variants %s --K %d' % (n, K), n) for n in NAMES] + [('--fresh --b6 --K %d' % K, 'b6')]
    waves = [jobs] if mem >= 48 else [jobs[:4], jobs[4:]]
    script = ['cd /root/rc', 'export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1']
    for w in waves:
        script.append(' & '.join('(%s -B -X utf8 recount_fresh.py %s > /root/logs/%s.log 2>&1; echo "%s exit $?" >> /root/logs/EXIT)'
                                 % (PY, a, n, n) for a, n in w) + ' & wait')
    script.append('echo ALL_DONE >> /root/logs/EXIT')
    (PV.PODS / name / 'run.sh').write_text('\n'.join(script) + '\n', encoding='ascii', newline='\n')
    r = PV.sftp(name, ['put "%s" "/root/run.sh"' % (PV.PODS / name / 'run.sh')])
    if r.returncode != 0:
        raise SystemExit('upload of run.sh failed')
    print(ssh(name, 'setsid nohup bash /root/run.sh > /root/logs/run.log 2>&1 < /dev/null & sleep 3; echo started; cat /root/logs/EXIT 2>/dev/null', 120))
    print('RAM %d GB, waves %d' % (mem, len(waves)))


def status(name):
    print(ssh(name, 'cat /root/logs/EXIT 2>/dev/null; for f in /root/logs/*.log; do echo "== $f"; tail -2 "$f" | cut -c1-200; done; '
                    'ls /root | grep -c "rc.out"; free -g | head -2', 120))


def fetch(name):
    names = ['part_fresh_%s.json' % n for n in NAMES] + ['boot_%s.npz' % n for n in NAMES] + ['part_fresh_b6.json']
    cmd = ['mkdir -p /root/outpkg && cd /root']
    for f in names:
        cmd.append('cp "/root/rc\\out\\%s" /root/outpkg/%s' % (f, f))
    cmd.append('cp "/root/rc\\out/boot_b6.npz" /root/outpkg/boot_b6.npz')
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
    bad = [f for f, h in sums.items() if sha(xd / f) != h]
    if bad:
        raise SystemExit('SHA-256 differs after download: %s' % bad)
    od = RCL / 'out'
    for f in sums:
        (od / f).write_bytes((xd / f).read_bytes())
        assert sha(od / f) == sums[f]
    (PV.PODS / name / 'FETCHED').write_text(PV.est() + '\n' + json.dumps(sums, indent=1), encoding='utf-8')
    print('fetched and checked:', sorted(sums))


def main():
    c = sys.argv[1]
    if c == 'stage':
        stage()
    elif c == 'up':
        up(sys.argv[2])
    elif c == 'run':
        run(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2000)
    elif c == 'status':
        status(sys.argv[2])
    elif c == 'fetch':
        fetch(sys.argv[2])
    elif c == 'down':
        if not (PV.PODS / sys.argv[2] / 'FETCHED').is_file():
            raise SystemExit('REFUSED: outputs not fetched yet')
        PV.delete(sys.argv[2], 'package B recount: outputs fetched and SHA-256 checked')
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
