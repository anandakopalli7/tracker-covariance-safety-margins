#!/bin/bash
# One line per pod: worker counts only (sealing). Usage: bash status_all.sh
CD=ARS_TRIAL/revision_v13/work/CD_capture
for d in $CD/pods/claude-v13cd-*; do
  n=$(basename $d); [ -f $d/ssh_config ] || continue; [ -f $d/TERMINATED ] && { echo "$n TERMINATED"; continue; }
  w=$(cygpath -w $d/ssh_config)
  out=$(timeout 45 /c/Windows/System32/OpenSSH/ssh.exe -F "$w" $n "bash -s" < $CD/tools/remote_status_cd.sh 2>&1 | grep "^{'status'\|^no worker\|BOOTSTRAP_OK\|^[0-9]* %" | tr '\n' ' ')
  echo "$n $out"
done
