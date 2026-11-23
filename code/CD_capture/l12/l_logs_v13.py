"""A12 sec. 2.3/2.5: sealing check and logs-only download of the L12 runs (keep_raw true; sweeps stay on the pod-local disk).
New file, 22 Nov 2026 (Claude Opus 5.5, session CD). Moves files only: it computes no value and parses no outcome of a run (it reads
receipts, the sealing records' booleans and hashes, and tar member names).

  seal NAME     upload C's frozen tools/seal_extract_v13.py (FREEZE_CD) to the pod and run it on every pl12_ archive with a receipt in
                /opt/claude_v13_l12local/results (nice 19, 3 workers): receipt SHA-256/bytes, status CAPTURED_AND_REVIEWED, frames_dropped 0,
                keep_raw true, every kept sweep's file hash = FILE_HASHES.json and array hash = its noise receipt; writes per run
                sealing/<rid>.json (booleans, counts, hashes) and logs/<rid>_logs.tar.gz (the archive without the sweep .npy, bytes
                copied, never parsed). Prints pass/fail counts only. Idempotent (a run with a sealing record is not redone).
  fetch NAME    download, for every passed run not yet on the laptop: logs/<rid>_logs.tar.gz, sealing/<rid>.json, the receipt. Checks:
                logs tar SHA-256/bytes = the sealing record; the receipt's sha256 = the sealing record's archive_sha256. Places them in
                archives_l12/<rid>/ and extracts the logs tar into runs/<rid>/ (members under <rid>/ only; no '..'; data filter), then
                writes runs/<rid>/LOGS_OK = the archive's SHA-256 (as c_extract_v13/x_extract_v13 extract_logs). Never overwrites.
  map           write l12/out/L12_RUNS_v13.json: "runs" = {job id: rid} for the 150 analysed job ids (CASES_L12_v13.json +
                REPLACEMENTS_L12_v13.json) whose logs are on the laptop (rid = job id, or the worker's suffixed id __p1/__r1 for a run
                captured on an allowed retry); "missing" = the job ids without logs; "detail" = one row per job (add9: "runs" was a list).
  fetch-b7 NAME (10 Hz option; add9) download finished B7 re-detections (C's frozen b7_redetect_v13.py, run on the pod by
                l12/remote_l12_after_capture.sh) into CD_capture/b7/<rid>/, checked against their manifests and the laptop receipts.
Usage: .venv/Scripts/python.exe -I -B -X utf8 l12/l_logs_v13.py seal|fetch|fetch-b7 NAME | map
"""
import hashlib, json, pathlib, shutil, sys, tarfile, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(CD / 'tools'))
import pods_v13 as pv                                   # noqa: E402
import b7_pods_v13 as BP                                # noqa: E402  (helpers: ssh, put, get)
VOL = '/opt/claude_v13_l12local'
PYCAP = '/opt/programme_a_gpu750/.venv/bin/python'
SEALER = CD / 'tools' / 'seal_extract_v13.py'
ARCH = CD / 'archives_l12'; RUNS = CD / 'runs'; STAGE = CD / 'pods' / 'l12_logs_staging'
CASES_SHA = 'ae494eb27637139132df1e258da489038087fd81452952ded73c6c842d4075eb'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def seal(name):
    BP.put(name, SEALER, '/root/cmp/seal_extract_v13.py')
    h = BP.ssh(name, 'sha256sum /root/cmp/seal_extract_v13.py').split()[0]
    if h != sha(SEALER): raise SystemExit('%s: sealer differs on the pod' % name)
    out = BP.ssh(name, 'nice -n 19 %s -I /root/cmp/seal_extract_v13.py --results %s/results --out %s --prefixes pl12_ --workers 3'
                 % (PYCAP, VOL, VOL), timeout=3600)
    s = json.loads(out[out.index('{'):])
    (CD / 'pods' / name).mkdir(parents=True, exist_ok=True)
    (CD / 'pods' / name / ('L_SEAL_%s.json' % time.strftime('%H%M%S'))).write_text(json.dumps(dict(s, at=pv.est()), indent=1), encoding='utf-8')
    print(json.dumps(dict(pod=name, archives=s['archives'], passed=s['passed'], failed=s['failed'])))


LIST_PY = r'''
import json, glob
print(json.dumps([{k: json.load(open(f)).get(k) for k in ('run_id', 'pass', 'logs_sha256', 'logs_bytes', 'archive_sha256')}
                  for f in sorted(glob.glob('%s/sealing/pl12_*.json'))]))
'''


def fetch(name):
    recs = json.loads(BP.ssh(name, "python3 - <<'PYEOF'\n%s\nPYEOF" % (LIST_PY % VOL)).strip().splitlines()[-1])
    failed = [r['run_id'] for r in recs if not r['pass']]
    need = [r for r in recs if r['pass'] and not (ARCH / r['run_id'] / 'DONE').is_file()]
    if not need:
        print(json.dumps(dict(pod=name, sealed=len(recs), failed=failed, fetched=0))); return
    files = []
    for r in need:
        rid = r['run_id']
        files += ['logs/%s_logs.tar.gz' % rid, 'sealing/%s.json' % rid, 'results/%s/claude_main_%s.tar.gz.receipt.json' % (rid, rid)]
    lst = STAGE / ('%s_list.txt' % name); STAGE.mkdir(parents=True, exist_ok=True)
    lst.write_text('\n'.join(files) + '\n', encoding='ascii', newline='\n')
    BP.put(name, lst, '/root/l12_fetch_list.txt')
    BP.ssh(name, 'cd %s && tar cf /root/l12_fetch.tar -T /root/l12_fetch_list.txt' % VOL, timeout=1800)
    loc = STAGE / ('%s_fetch.tar' % name)
    BP.get(name, '/root/l12_fetch.tar', str(loc))
    tmp = STAGE / ('%s_tmp' % name); shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
    with tarfile.open(loc) as t:
        names = set(t.getnames())
        assert names == set(files), 'the fetch tar differs from the list'
        t.extractall(tmp, filter='data')
    done = []
    for r in need:
        rid = r['run_id']
        lt = tmp / 'logs' / ('%s_logs.tar.gz' % rid); sj = tmp / 'sealing' / ('%s.json' % rid)
        rc = tmp / 'results' / rid / ('claude_main_%s.tar.gz.receipt.json' % rid)
        srec = json.loads(sj.read_text(encoding='utf-8')); rec = json.loads(rc.read_text(encoding='utf-8'))
        assert srec['pass'] is True and srec['run_id'] == rid
        assert sha(lt) == srec['logs_sha256'] and lt.stat().st_size == srec['logs_bytes'], 'logs tar differs from its sealing record: ' + rid
        assert rec['sha256'] == srec['archive_sha256'] and rec['status'] == 'CAPTURED_AND_REVIEWED' and rec['keep_raw'] is True, rid
        dest = RUNS / rid
        if (dest / 'LOGS_OK').exists() or (ARCH / rid / 'DONE').exists(): raise SystemExit('REFUSED: %s exists (never overwrite)' % rid)
        with tarfile.open(lt, 'r:gz') as t:
            for m in t:
                parts = m.name.split('/')
                if '..' in parts or m.name.startswith('/') or parts[0] != rid: raise SystemExit('unsafe member %s in %s' % (m.name, rid))
                if m.isfile() and m.name.endswith('.npy') and len(parts) >= 2 and parts[-2] in ('raw', 'clean'):
                    raise SystemExit('a sweep file in a logs tar: ' + m.name)
            dest.mkdir(parents=True)
            t.extractall(dest, filter='data')
        (dest / 'LOGS_OK').write_text(rec['sha256'] + '\n')
        a = ARCH / rid; a.mkdir(parents=True, exist_ok=True)
        for f in (lt, sj, rc): shutil.move(str(f), str(a / f.name))
        (a / 'DONE').write_text(json.dumps(dict(pod=name, logs_sha256=srec['logs_sha256'], archive_sha256=rec['sha256'], at=pv.est())))
        done.append(rid)
    shutil.rmtree(tmp, ignore_errors=True); loc.unlink()
    print(json.dumps(dict(pod=name, sealed=len(recs), failed=failed, fetched=len(done))))


B7_LIST_PY = r'''
import json, glob, os
out = []
for f in sorted(glob.glob('%s/b7/pl12_*/B7_MANIFEST_v13.json')):
    m = json.load(open(f)); out.append(dict(run_id=m['run_id'], output_sha256=m['output_sha256'], archive_sha256=m['archive_sha256']))
print(json.dumps(out))
'''


def fetch_b7(name):
    """10 Hz option: download every finished B7 re-detection (b7/<rid>/b7_detections_v13.jsonl + B7_MANIFEST_v13.json) not yet in
    CD_capture/b7/; checks: the detections file SHA-256 = the manifest's output_sha256, the manifest's archive_sha256 = the run's receipt
    on the laptop (archives_l12/<rid>/). Never overwrites."""
    recs = json.loads(BP.ssh(name, "python3 - <<'PYEOF'\n%s\nPYEOF" % (B7_LIST_PY % VOL)).strip().splitlines()[-1])
    need = [r for r in recs if not (CD / 'b7' / r['run_id'] / 'B7_MANIFEST_v13.json').is_file()]
    if not need:
        print(json.dumps(dict(pod=name, b7_finished=len(recs), fetched=0))); return
    files = ['b7/%s/%s' % (r['run_id'], f) for r in need for f in ('b7_detections_v13.jsonl', 'B7_MANIFEST_v13.json')]
    lst = STAGE / ('%s_b7_list.txt' % name); STAGE.mkdir(parents=True, exist_ok=True)
    lst.write_text('\n'.join(files) + '\n', encoding='ascii', newline='\n')
    BP.put(name, lst, '/root/l12_b7_list.txt')
    BP.ssh(name, 'cd %s && tar czf /root/l12_b7.tar.gz -T /root/l12_b7_list.txt' % VOL, timeout=1800)
    loc = STAGE / ('%s_b7.tar.gz' % name)
    BP.get(name, '/root/l12_b7.tar.gz', str(loc))
    tmp = STAGE / ('%s_b7_tmp' % name); shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
    with tarfile.open(loc) as t:
        assert set(t.getnames()) == set(files), 'the b7 tar differs from the list'
        t.extractall(tmp, filter='data')
    n = 0
    for r in need:
        rid = r['run_id']; s = tmp / 'b7' / rid
        man = json.loads((s / 'B7_MANIFEST_v13.json').read_text(encoding='utf-8'))
        assert sha(s / 'b7_detections_v13.jsonl') == man['output_sha256'] == r['output_sha256'], 'b7 output differs from its manifest: ' + rid
        rc = ARCH / rid / ('claude_main_%s.tar.gz.receipt.json' % rid)
        if not rc.is_file() or json.loads(rc.read_text(encoding='utf-8'))['sha256'] != man['archive_sha256']:
            raise SystemExit('b7 manifest does not match a receipt on the laptop (fetch logs first): ' + rid)
        d = CD / 'b7' / rid
        if d.exists(): raise SystemExit('REFUSED: %s exists (never overwrite)' % d)
        shutil.move(str(s), str(d)); n += 1
    shutil.rmtree(tmp, ignore_errors=True); loc.unlink()
    print(json.dumps(dict(pod=name, b7_finished=len(recs), fetched=n)))


def runs_map():
    cf = HERE / 'CASES_L12_v13.json'
    if sha(cf) != CASES_SHA: raise SystemExit('REFUSED: CASES_L12_v13.json differs')
    X = json.loads(cf.read_text(encoding='utf-8'))
    rp = HERE / 'REPLACEMENTS_L12_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8'))['replacements'] if rp.is_file() else {}
    rows = []
    for r in (x for x in X['cases'] if not x['reserve']):
        c = rep.get(r['case'], r['case']); job = 'pl12_%s_native' % c
        cands = [d for d in (job, job + '__p1', job + '__r1') if (RUNS / d / 'LOGS_OK').is_file()]
        rows.append(dict(position=r['position'], job=job, case=c, replaced=(c != r['case']), desired_mps=r['desired_mps'],
                         run_folder=('runs/%s' % cands[0]) if len(cands) == 1 else None, capture_run_id=cands[0] if len(cands) == 1 else None,
                         note=None if len(cands) == 1 else ('missing' if not cands else 'ambiguous: %s' % cands)))
    rows = sorted(rows, key=lambda r: r['job'])
    out = dict(schema='L12_RUNS_V13', cases_sha256=CASES_SHA, replacements=rep, n=len(rows), n_present=sum(r['run_folder'] is not None for r in rows),
               layout='runs/<rid>/LOGS_OK and runs/<rid>/<rid>/{SUMMARY.json, FILE_HASHES.json, capture/<case>/...}',
               written=pv.est(), runs={r['job']: r['capture_run_id'] for r in rows if r['capture_run_id']},   # {job id: rid}, the shape B and F read
               missing=[r['job'] for r in rows if not r['capture_run_id']], detail=rows)
    (HERE / 'out').mkdir(exist_ok=True)
    (HERE / 'out' / 'L12_RUNS_v13.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    print('L12_RUNS_v13.json: %d of %d present' % (out['n_present'], out['n']))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'seal': seal(sys.argv[2])
    elif c == 'fetch': fetch(sys.argv[2])
    elif c == 'fetch-b7': fetch_b7(sys.argv[2])
    elif c == 'map': runs_map()
    else: raise SystemExit(__doc__)
