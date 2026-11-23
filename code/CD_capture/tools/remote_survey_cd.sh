#!/bin/bash
# Survey after the quota failure: published runs on the volume (status only) and local leftovers. No outcome is read.
python3 - <<'PY'
import json,os,pathlib
R=pathlib.Path('/workspace/claude_v13_cd_v01/results')
pub=[];partial=[]
for d in sorted(R.iterdir()) if R.is_dir() else []:
    s=d/'SUMMARY.json';r=list(d.glob('*.receipt.json'))
    if s.is_file() and r:
        st=json.loads(r[0].read_text())['status'];pub.append((d.name,st))
    else:partial.append((d.name,[(f.name,f.stat().st_size) for f in d.iterdir()]))
print('VOLUME_PUBLISHED',json.dumps(pub));print('VOLUME_PARTIAL',json.dumps(partial))
L=pathlib.Path('/opt/claude_main')
print('LOCAL_ARCHIVES',json.dumps([(p.name,p.stat().st_size) for p in sorted((L/'archives').glob('*'))]))
print('LOCAL_JOBS',json.dumps([(p.name,(p/'SUMMARY.json').is_file()) for p in sorted((L/'jobs').glob('*'))]))
loc=[]
for p in sorted((L/'summaries').glob('*.json')):
    try:loc.append((p.stem,json.loads(p.read_text())['status']))
    except Exception as e:loc.append((p.stem,'unreadable'))
print('LOCAL_SUMMARY_STATUS',json.dumps(loc))
PY
