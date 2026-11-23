"""Move the 57 re-simulation archives (archives/rs13*, the old runs re-simulated frame-identically, task 5) from the laptop to the
network volume, to keep C: above its free-space floor. Coordinator's approval and conditions, 20 Nov 2026 05:34 EST:
  one short-lived pod with the volume mounted (spend log, watchdog), every file on the volume checked against its DOWNLOAD_OK receipt
  (SHA-256) before any laptop copy is deleted, a receipt list written first (resim_on_volume_v01.json), then only those 57 laptop
  archives deleted; nothing else touched. New file, 20 Nov 2026 (Claude Opus 5.5).

Usage: python -I move_resim_to_volume_v13.py POD   (POD = claude-v13cd-vNN; created if it has no record yet)
Steps: create/adopt the pod -> mkdir /workspace/claude_v13_cd_v01/resim/<rid>/ -> upload each .tar.gz (and its small receipt files)
in 3 parallel SFTP streams -> sha256sum on the volume -> compare with DOWNLOAD_OK.json -> write resim_on_volume_v01.json -> delete
the laptop .tar.gz of every matching run (DOWNLOAD_OK.json and the receipt stay; a MOVED_TO_VOLUME.json pointer is added) -> delete the pod.
Refuses to delete anything unless all 57 match.
"""
import datetime, hashlib, json, pathlib, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import pods_v13 as pv

POD = sys.argv[1]; assert POD.startswith('claude-v13cd-v')
VOL = '/workspace/claude_v13_cd_v01/resim'
REC = CD / 'resim_on_volume_v01.json'
LOG = CD / 'pods' / 'move_resim.log'


def say(m):
    line = f'{pv.est()} {m}'; print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def main():
    rids = sorted(p.name for p in (CD / 'archives').glob('rs13*') if p.is_dir())
    jobs = []
    for rid in rids:
        d = CD / 'archives' / rid; ok = json.loads((d / 'DOWNLOAD_OK.json').read_text(encoding='utf-8'))
        arch = d / ok['archive']
        if not arch.is_file(): raise SystemExit(f'REFUSED: {arch} missing (already moved?)')
        jobs.append(dict(rid=rid, arch=arch, sha256=ok['sha256'], bytes=ok['bytes'], extra=[x for x in d.iterdir() if x.name.endswith('.receipt.json')]))
    say(f'{len(jobs)} re-simulation archives, {sum(j["bytes"] for j in jobs) / 1e9:.2f} GB')
    if len(jobs) != 57: raise SystemExit(f'REFUSED: expected 57 rs13 archives, found {len(jobs)}')
    if not (CD / 'pods' / POD / 'pod.json').is_file():
        pv.create(POD, 'NVIDIA GeForce RTX 4090', 2.0, 'move the 57 rs13 re-sim archives to the volume (coordinator approval 05:34 EST)')
    r = pv.ssh(POD, f'mkdir -p {VOL} && df -h /workspace | tail -1', timeout=120); say(f'volume: {r.stdout.strip()}')
    pv.ssh(POD, 'mkdir -p ' + ' '.join(f'{VOL}/{j["rid"]}' for j in jobs), timeout=120)

    def up(chunk):
        lines = []
        for j in chunk:
            lines.append(f'put "{j["arch"]}" "{VOL}/{j["rid"]}/{j["arch"].name}"')
            for x in j['extra']: lines.append(f'put "{x}" "{VOL}/{j["rid"]}/{x.name}"')
        t0 = time.time(); rr = pv.sftp(POD, lines, timeout=6 * 3600)
        return rr.returncode, time.time() - t0, [j['rid'] for j in chunk]
    for attempt in range(3):
        remote = {}
        out = pv.ssh(POD, f'cd {VOL} && for d in */; do for f in $d*.tar.gz; do [ -f "$f" ] && sha256sum "$f"; done; done', timeout=3600).stdout
        for l in out.splitlines():
            if l.strip(): h, f = l.split(None, 1); remote[f.split('/')[0]] = h
        todo = [j for j in jobs if remote.get(j['rid']) != j['sha256']]
        say(f'attempt {attempt + 1}: {len(jobs) - len(todo)} of {len(jobs)} already on the volume with the right SHA-256; uploading {len(todo)}')
        if not todo: break
        chunks = [todo[i::3] for i in range(3)]
        with ThreadPoolExecutor(3) as ex:
            for rc, sec, rr in ex.map(up, [c for c in chunks if c]):
                say(f'sftp rc={rc} {len(rr)} archives in {sec:.0f} s')
    else:
        raise SystemExit('REFUSED: some archives still do not match after 3 attempts; nothing deleted')
    # final check, receipt list, then delete laptop copies
    now = datetime.datetime.now().astimezone().isoformat()
    out = pv.ssh(POD, f'cd {VOL} && for d in */; do for f in $d*.tar.gz; do [ -f "$f" ] && sha256sum "$f" && stat -c %s "$f"; done; done', timeout=3600).stdout.split()
    remote = {}; i = 0
    while i + 2 < len(out):
        h, f, sz = out[i], out[i + 1], out[i + 2]; remote[f.split('/')[0]] = (h, int(sz)); i += 3
    bad = [j['rid'] for j in jobs if remote.get(j['rid'], (None, 0))[0] != j['sha256'] or remote[j['rid']][1] != j['bytes']]
    if bad: raise SystemExit(f'REFUSED: volume copies differ for {bad}; nothing deleted')
    rec = dict(schema='RESIM_ON_VOLUME_V01', approval='coordinator 20 Nov 2026 05:34 EST', volume='<cloud volume id> (EU-RO-1)', pod=POD,
               note='The only copies of these 57 re-simulation archives are now on the network volume. They are regenerable: frame-identical '
                    're-simulations of the old runs (RESIM_SUMMARY_v13.json). Laptop folders keep DOWNLOAD_OK.json, the receipt and a pointer.',
               runs=[dict(run_id=j['rid'], volume_path=f'{VOL}/{j["rid"]}/{j["arch"].name}', sha256=j['sha256'], bytes=j['bytes'], checked=now)
                     for j in jobs])
    REC.write_text(json.dumps(rec, indent=1), encoding='utf-8')
    say(f'receipt list written: {REC.name} ({len(jobs)} runs), sha256 {sha(REC)}')
    for j in jobs:
        (j['arch'].parent / 'MOVED_TO_VOLUME.json').write_text(json.dumps(dict(volume_path=f'{VOL}/{j["rid"]}/{j["arch"].name}',
            sha256=j['sha256'], bytes=j['bytes'], checked=now, receipt_list='CD_capture/resim_on_volume_v01.json'), indent=1), encoding='utf-8')
        if sha(j['arch']) != j['sha256']: raise SystemExit(f'REFUSED: laptop copy of {j["rid"]} changed?')
        j['arch'].unlink()
    say(f'deleted {len(jobs)} laptop archives ({sum(j["bytes"] for j in jobs) / 1e9:.2f} GB)')
    pv.delete(POD, 'rs13 re-sim archives on the volume, all 57 SHA-256-checked; laptop copies deleted')
    say('pod deleted; done')


if __name__ == '__main__':
    main()
