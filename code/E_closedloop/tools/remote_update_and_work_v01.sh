#!/bin/bash
# On a bootstrapped pod whose worker has finished: switch to a newer packet and run the next job list.
# Launched detached: setsid nohup bash /root/cmp/remote_update_and_work_v01.sh <packet_name> <slots> > /root/main_chain_<stamp>.log 2>&1 < /dev/null &
set -Eeuo pipefail
PK=${1:?packet name}; SLOTS=${2:-2}; STAMP=$(date --utc +%Y%m%dT%H%M%SZ)
cd /root/cmp
echo "update start $STAMP"
test -d "$PK" || tar -xzf "$PK.tar.gz"
B=/root/cmp/$PK/bootstrap
test -f /opt/claude_smoke/BOOTSTRAP_OK.json
CUR=$(sha256sum /opt/programme_a_gpu750/workspace/claude_smoke_v01/RUNTIME_SOURCE_BINDING_SMOKE_v01.json | cut -d' ' -f1)
NEW=$(sha256sum /root/cmp/$PK/claude_smoke_v01/RUNTIME_SOURCE_BINDING_SMOKE_v01.json | cut -d' ' -f1)
if [ "$CUR" != "$NEW" ]; then
  bash $B/run_with_container_env_v01.sh python3 -B /root/cmp/$PK/claude_smoke_v01/update_main_packet_v01.py /root/cmp/$PK
  echo "packet updated $(date --utc +%FT%TZ)"
else
  echo "packet already current"
fi
cp /root/cmp/JOBS_NEXT.json /opt/claude_main/JOBS_$STAMP.json
echo "worker start $(date --utc +%FT%TZ) jobs=/opt/claude_main/JOBS_$STAMP.json"
bash $B/run_with_container_env_v01.sh /opt/programme_a_gpu750/.venv/bin/python -B /opt/programme_a_gpu750/workspace/claude_smoke_v01/worker_main_v01.py --jobs /opt/claude_main/JOBS_$STAMP.json --slots "$SLOTS" > /root/main_worker_$STAMP.log 2>&1
echo "worker finished $(date --utc +%FT%TZ)"
