#!/bin/bash
# On a pod after capture: B7 re-detection (2 GPU processes) on this pod's local C runs (+ the volume runs given as $1, comma list),
# then the sealing check + logs-only copies (8 CPU workers) on every local archive. Counts only are printed.
set -u
VOLRUNS=${1:-}
cd /root/cmp
ENVW=/root/cmp/packet_main_v03/bootstrap/run_with_container_env_v01.sh
[ -f $ENVW ] || ENVW=$(ls /root/cmp/packet_*/bootstrap/run_with_container_env_v01.sh | head -1)
PY=/opt/programme_a_gpu750/.venv/bin/python
LOCALRUNS=$(ls /opt/claude_v13_local/results | grep '^pc13_' | sort)
A=$(echo "$LOCALRUNS" | awk 'NR%2==1' | paste -sd,); B=$(echo "$LOCALRUNS" | awk 'NR%2==0' | paste -sd,)
setsid nohup bash $ENVW $PY -B /root/cmp/b7_redetect_v13.py --runs "$A" --folder /opt/claude_v13_local > /root/b7_A.log 2>&1 < /dev/null &
setsid nohup bash $ENVW $PY -B /root/cmp/b7_redetect_v13.py --runs "$B" --folder /opt/claude_v13_local > /root/b7_B.log 2>&1 < /dev/null &
if [ -n "$VOLRUNS" ]; then
  setsid nohup bash $ENVW $PY -B /root/cmp/b7_redetect_v13.py --runs "$VOLRUNS" --src-folder claude_v13_cd_v01 > /root/b7_V.log 2>&1 < /dev/null &
fi
setsid nohup $PY -I /root/cmp/seal_extract_v13.py --results /opt/claude_v13_local/results --out /opt/claude_v13_local --prefixes pc13_,pd13_ --workers 8 > /root/seal_local.log 2>&1 < /dev/null &
echo "launched: local C runs $(echo "$LOCALRUNS" | grep -c .), volume runs $(echo "$VOLRUNS" | tr ',' '\n' | grep -c .)"
