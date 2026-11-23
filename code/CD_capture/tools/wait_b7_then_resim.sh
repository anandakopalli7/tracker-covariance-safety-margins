#!/bin/bash
# For each pod: wait until no b7 process runs, then start its re-simulation list on packet_main_v03.
CD=ARS_TRIAL/revision_v13/work/CD_capture
for n in "$@"; do
  for i in $(seq 1 120); do
    c=$(timeout 60 /c/Windows/System32/OpenSSH/ssh.exe -F "$(cygpath -w $CD/pods/claude-v13cd-$n/ssh_config)" claude-v13cd-$n "pgrep -fc '[b]7_redetect'" < /dev/null 2>/dev/null)
    [ "$c" = "0" ] && break; sleep 30
  done
  echo "pod $n b7 done at $(date)"
  timeout 600 python -I $CD/tools/next_list_v13.py claude-v13cd-$n packet_main_v03 $CD/jobs/JOBS_RS13_claude-v13cd-${n}_v01.json 2 2>&1 | grep -v "^ *\^\|tail: option" | tail -2
done
