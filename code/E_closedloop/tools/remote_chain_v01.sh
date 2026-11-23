#!/bin/bash
# On a fresh pod: (1) rehearse worker_main in simulate mode (no CARLA, separate volume folder),
# (2) run the smoke-verified bootstrap, (3) start the real worker on JOBS.json.
# Launched detached: setsid nohup bash /root/cmp/remote_chain_v01.sh <packet_name> <slots> > /root/main_chain.log 2>&1 < /dev/null &
set -Eeuo pipefail
PK=${1:?packet name}; SLOTS=${2:-2}
cd /root/cmp
echo "chain start $(date --utc +%FT%TZ)"
test -d "$PK" || tar -xzf "$PK.tar.gz"
B=/root/cmp/$PK/bootstrap; C=/root/cmp/$PK/claude_smoke_v01
mkdir -p /opt/claude_main
if [ ! -f /opt/claude_main/SIMULATE_OK ]; then
  python3 - <<'PY'
import json
cfg=json.load(open('/root/cmp/JOBS.json'));cfg['jobs']=cfg['jobs'][:3];cfg['concurrent_start_stagger_s']=2
json.dump(cfg,open('/root/cmp/JOBS_SIMULATE.json','w'))
PY
  bash $B/run_with_container_env_v01.sh python3 -B $C/worker_main_v01.py --jobs /root/cmp/JOBS_SIMULATE.json --slots 2 --simulate
  # v13 fix (19 Nov 2026): simulate mode writes to /opt/claude_main_simulate; the old mv aborted the chain under set -e.
  mv /opt/claude_main_simulate/worker_status.json /opt/claude_main/worker_status_simulate.json 2>/dev/null || true
  touch /opt/claude_main/SIMULATE_OK
  echo "simulate ok $(date --utc +%FT%TZ)"
fi
if [ ! -f /opt/claude_smoke/BOOTSTRAP_OK.json ]; then
  bash $B/run_with_container_env_v01.sh bash $B/bootstrap_smoke_v01.sh > /root/main_bootstrap.log 2>&1
fi
test -f /opt/claude_smoke/BOOTSTRAP_OK.json
echo "bootstrap ok $(date --utc +%FT%TZ)"
cp /root/cmp/JOBS.json /opt/claude_main/JOBS_current.json
bash $B/run_with_container_env_v01.sh /opt/programme_a_gpu750/.venv/bin/python -B /opt/programme_a_gpu750/workspace/claude_smoke_v01/worker_main_v01.py --jobs /opt/claude_main/JOBS_current.json --slots "$SLOTS" > /root/main_worker.log 2>&1
echo "worker finished $(date --utc +%FT%TZ)"
