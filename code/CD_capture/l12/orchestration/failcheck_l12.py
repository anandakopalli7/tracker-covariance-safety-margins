import sys, json
sys.path.insert(0, r'ARS_TRIAL\revision_v13\work\CD_capture\tools')
import pods_v13 as pv
PY = r'''
import json, glob, collections, os
by = collections.defaultdict(list)
for f in sorted(glob.glob('/opt/claude_main/summaries/pl12_*.json')):
    s = json.load(open(f)); by[s['job']].append((s.get('attempt'), s.get('status'), s.get('capture_exit')))
ok = sorted(j for j, v in by.items() if any(x[1] == 'CAPTURED_AND_REVIEWED' for x in v))
bad = {j: v for j, v in by.items() if j not in ok}
jobs = [j['id'] for j in json.load(open('/opt/claude_main/JOBS_current.json'))['jobs'] if j['id'].startswith('pl12_')]
miss = [j for j in jobs if j not in by]
sz = [os.path.getsize(p) for p in glob.glob('/opt/claude_v13_l12local/results/pl12_*/*.tar.gz')]
st = os.statvfs('/workspace') if os.path.isdir('/workspace') else None
print(json.dumps(dict(listed=len(jobs), ok=len(ok), failed=bad, never_started=miss, archives=len(sz), archive_mb=round(sum(sz)/1e6), mean_mb=round(sum(sz)/max(1,len(sz))/1e6,1),
      workspace_free_gb=(round(st.f_bavail*st.f_frsize/1e9,1) if st else None))))
'''
for name in sys.argv[1:]:
    r = pv.ssh(name, "python3 - <<'PYEOF'\n%s\nPYEOF" % PY, timeout=180)
    print(name, (r.stdout.strip().splitlines() or ['?'])[-1][:900], r.stderr[-200:] if r.returncode else '')
