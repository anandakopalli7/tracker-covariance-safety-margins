#!/usr/bin/env bash
# Revision v13, AMENDMENT_11 sec. 6c: DR's post-lock chain ON THE POD (21 Nov 2026, Claude Opus 5.5, session F). Needs LOCK_A11c.txt
# on the pod (dr_pods_v01.py stage-data lock / upload NAME lock); every DR program refuses without it. Order (sec. 6c.9): P-bar_DR on
# the 120 masked tuning runs, the fresh DR arrays (P-bar_DR and the record), the values with the calibration exported, the double
# bootstrap (calib_remote_v13.py, both inner seeds), the import (final values).
set -u
R=/root/dr
V13=$R/ARS_TRIAL/revision_v13
FD=$V13/work/F_dropout
CDA=$V13/work/CD_capture/analysis
PY=/opt/drpy/bin/python
W=${W:-13}
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
test -f $V13/LOCK_A11c.txt || { echo "REFUSED: no LOCK_A11c.txt"; exit 1; }
cd $R/job
X="$PY -I -B -X utf8 $FD/code/dr_extract_v01.py"
echo "$(date +%T) pbar (120 masked tuning runs)"; $X pbar --workers $W | tail -2
echo "$(date +%T) combine"; $X combine | tail -2
echo "$(date +%T) dr (105 fresh runs)"; $X dr --workers $W | tail -2
echo "$(date +%T) ARRAYS DONE"
echo "$(date +%T) analysis export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v01.py --calib export 2>&1 | tail -3
echo "$(date +%T) EXPORT DONE"
if [ "${CALIB_HERE:-1}" = "1" ]; then
  echo "$(date +%T) calib_remote"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $CDA/calib_remote_v13.py $FD/out/calib dr_main --threads $W 2>&1 | tail -3
  echo "$(date +%T) analysis import"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v01.py --calib import 2>&1 | tail -3
fi
echo "$(date +%T) POSTLOCK CHAIN DONE"
