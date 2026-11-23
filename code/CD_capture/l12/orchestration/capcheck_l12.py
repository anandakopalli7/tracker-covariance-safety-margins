"""Per pod: worker status, study jobs finished/failed (ids and statuses only), and every control's identity. No outcome is read."""
import sys, json, pathlib
sys.path.insert(0, r'ARS_TRIAL\revision_v13\work\CD_capture\tools')
import pods_v13 as pv
PY = r'''
import json, glob
st = json.load(open('/opt/claude_main/worker_status.json'))
ctl = []; fails = []; ok = 0
for f in sorted(glob.glob('/opt/claude_main/summaries/*.json')):
    s = json.load(open(f))
    if s.get('role') == 'control':
        c = s.get('comparison_to_reference') or {}; ctl.append([s['job'][-12:], s.get('status'), c.get('identical')])
    elif s.get('job', '').startswith('pl12_'):
        if s.get('status') == 'CAPTURED_AND_REVIEWED': ok += 1
        else: fails.append([s['job'], s.get('attempt'), s.get('status')])
print(json.dumps(dict(status=st.get('status'), study_ok=ok, not_ok=fails, controls=ctl, last_control=(st.get('last_control') or {}).get('identical'))))
'''
for name in sys.argv[1:]:
    r = pv.ssh(name, "python3 - <<'PYEOF'\n%s\nPYEOF" % PY, timeout=120)
    print(name, (r.stdout.strip().splitlines() or ["?"])[-1][:700], r.stderr[-300:] if r.returncode else "")
