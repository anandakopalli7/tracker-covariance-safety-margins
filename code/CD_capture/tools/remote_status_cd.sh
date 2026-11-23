#!/bin/bash
# Pod status for package C/D capture: counts only. Never prints S, T, contacts or any summary outcome (A10 sec. 5.2 sealing).
echo "== chain"; tail -n 4 /root/main_chain.log 2>/dev/null
echo "== bootstrap marks"; tail -n 3 /opt/claude_smoke/results/host/BOOTSTRAP_TIMINGS.jsonl 2>/dev/null; test -f /opt/claude_smoke/BOOTSTRAP_OK.json && echo BOOTSTRAP_OK
echo "== worker"
python3 - <<'PY'
import json,os
p='/opt/claude_main/worker_status.json'
if os.path.isfile(p):
    d=json.load(open(p))
    lc=d.get('last_control') or {}
    print(dict(status=d.get('status'),total=d.get('total'),done_ok=d.get('done_ok'),failed_final=len(d.get('failed_final') or []),
               failed_ids=d.get('failed_final'),pending=d.get('pending'),running=len(d.get('running') or []),
               runs_per_hour=d.get('runs_per_hour'),last_control_job=lc.get('job'),last_control_identical=lc.get('identical'),disabled=d.get('disabled_slots')))
else:print('no worker status yet')
PY
echo "== disk"; df -h /opt | tail -1
echo "== gpu"; nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader
