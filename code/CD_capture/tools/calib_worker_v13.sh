#!/bin/bash
# Pod-side worker pool for the A10 sec. 2.6 double bootstrap (revision v13, packages C and D; 20 Nov 2026, Claude Opus 5.5).
# Usage: calib_worker_v13.sh N   (start N single-threaded workers; they run until the pod is deleted)
# Queue: /opt/calib/todo/<task> files, each one line "LABEL SEED LO HI". A worker claims a task by an atomic rename into running/,
# runs jobs/calib_remote_v13.py ... --outer LO:HI --threads 1, then moves the task to done/ (or failed/). The laptop may take
# unclaimed tasks away (rename todo/x -> stolen/x) to give them to another pod; a claimed task is never taken away.
cd /opt/calib || exit 1
mkdir -p todo running done failed stolen logs
PY=$(cat /opt/calib/PY)
N=${1:-$(nproc)}
worker() {
  while true; do
    f=$(ls todo 2>/dev/null | head -1)
    if [ -z "$f" ]; then sleep 10; continue; fi
    mv "todo/$f" "running/$f" 2>/dev/null || continue
    read -r L S LO HI R < <(tr -d '\r' < "running/$f")   # tolerate CRLF task files (20 Nov dry run)
    R=${R:-calib_remote_v13.py}          # 5th field: the runner (first program by default; the recount has its own runner)
    if OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1 \
       "$PY" -I -B "jobs/$R" jobs "$L" --seeds "$S" --outer "$LO:$HI" --threads 1 > "logs/$f.log" 2>&1; then
      mv "running/$f" "done/$f"
    else
      mv "running/$f" "failed/$f"
    fi
  done
}
for i in $(seq 1 "$N"); do worker "$i" & done
echo "started $N workers $(date -u +%FT%TZ)"
wait
