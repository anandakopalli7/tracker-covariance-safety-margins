#!/bin/bash
# On an L12 capture pod, after its worker ends (A12 sec. 2.3/2.5; the 10 Hz option, coordinator 22 Nov 2026 about 00:55 EST: "Run B7
# re-detection (frozen, unchanged) on the capture pods right after each pod's capture ends; no lock needed, detections only").
# New file, 22 Nov 2026 (Claude Opus 5.5, session CD). Pattern of tools/remote_b7_and_seal.sh (C). It computes no value:
#   1. wait until /opt/claude_main/worker_status.json says FINISHED or HALTED_*;
#   2. sealing check + logs-only copies of every pl12_ archive (C's frozen tools/seal_extract_v13.py; 2 Hz first);
#   3. B7 re-detection (C's frozen tools/b7_redetect_v13.py, unchanged) of every pl12_ run that passed the seal, 2 GPU processes,
#      outputs in /opt/claude_v13_l12local/b7/<rid>/ (pod-local).
# Printed output: counts only. Usage (pod): setsid nohup bash /root/cmp/remote_l12_after_capture.sh > /root/l12_after.log 2>&1 < /dev/null &
set -u
VOL=/opt/claude_v13_l12local
PY=/opt/programme_a_gpu750/.venv/bin/python
ENVW=$(ls /root/cmp/packet_*/bootstrap/run_with_container_env_v01.sh | head -1)
while true; do
  s=$(python3 -c "import json; print(json.load(open('/opt/claude_main/worker_status.json')).get('status'))" 2>/dev/null)
  case "$s" in FINISHED|HALTED_*) break;; esac
  sleep 60
done
echo "worker ended: $s $(date -u +%FT%TZ)"
nice -n 5 $PY -I /root/cmp/seal_extract_v13.py --results $VOL/results --out $VOL --prefixes pl12_ --workers 6 > /root/l12_seal.log 2>&1
echo "sealing done $(date -u +%FT%TZ)"; tail -c 400 /root/l12_seal.log
RUNS=$(python3 -c "
import json, glob
r = [json.load(open(f)) for f in glob.glob('$VOL/sealing/pl12_*.json')]
print(' '.join(sorted(x['run_id'] for x in r if x['pass'])))")
A=$(echo $RUNS | tr ' ' '\n' | awk 'NF && NR%2==1' | paste -sd,); B=$(echo $RUNS | tr ' ' '\n' | awk 'NF && NR%2==0' | paste -sd,)
[ -n "$A" ] && setsid nohup bash $ENVW $PY -B /root/cmp/b7_redetect_v13.py --runs "$A" --folder $VOL --out-root $VOL > /root/b7_A.log 2>&1 < /dev/null &
[ -n "$B" ] && setsid nohup bash $ENVW $PY -B /root/cmp/b7_redetect_v13.py --runs "$B" --folder $VOL --out-root $VOL > /root/b7_B.log 2>&1 < /dev/null &
echo "b7 launched on $(echo $RUNS | wc -w) sealed runs $(date -u +%FT%TZ)"
