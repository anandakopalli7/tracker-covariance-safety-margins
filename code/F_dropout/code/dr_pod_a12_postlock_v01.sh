#!/usr/bin/env bash
# Revision v13, AMENDMENT_12 sec. 3a: DR on the NEW runs, post-lock chain ON THE POD (22 Nov 2026, Claude Opus 5.5, session F). Needs
# LOCK_A12a.txt on the pod (dr_pods_v02.py stage-data locka12 / upload NAME locka12) and the new runs' logs (stage-data l12). Order
# (sec. 3a.7): identity arrays (no mask), then per p the masked P-bar, combine and arrays; the P-bar identity at p = 0.10 against
# F_dropout\out\PBAR_DR_v01.json (sec. 3a.3); the values with the calibration exported (dr_analysis_v02 p = 0.10; dr_dose_v01). The
# double bootstraps (calib_remote_v13 for dr_main, dr_slope_remote_v01 in outer chunks) and the imports are started separately.
set -u
R=/root/dr
V13=$R/ARS_TRIAL/revision_v13
FD=$V13/work/F_dropout
PY=/opt/drpy/bin/python
W=${W:-13}
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
test -f $V13/LOCK_A12a.txt || { echo "REFUSED: no LOCK_A12a.txt"; exit 1; }
cd $R/job
X="$PY -I -B -X utf8 $FD/code/dr_extract_v02.py"
echo "$(date +%T) identity arrays id0 / id3 (no mask)"; $X id0 --p 0.10 --workers $W | tail -1; $X id3 --p 0.10 --workers $W | tail -1
for p in 0.10 0.05 0.20 0.30; do
  echo "$(date +%T) p=$p pbar / combine / dr"
  $X pbar --p $p --workers $W | tail -1
  $X combine --p $p | tail -1
  $X dr --p $p --workers $W | tail -1
done
echo "$(date +%T) ARRAYS DONE"
$PY -I -c "
import json, numpy as np
a = json.load(open('$FD/out_a12/p010/PBAR_DR_v01.json')); b = json.load(open('$FD/out/PBAR_DR_v01.json'))
d = max(float(np.abs(np.array(a['Pbar'][c]) - np.array(b['Pbar'][c])).max()) for c in ('vehicle', 'pedestrian'))
print('PBAR identity p=0.10 vs A11 PBAR_DR_v01: max abs diff', d, 'counts', a['counts'], b['counts'], 'IDENTICAL' if d == 0 and a['counts'] == b['counts'] else 'DIFFERENT')"
echo "$(date +%T) analysis export (DR0-DR2, p = 0.10)"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v02.py --p 0.10 --calib export 2>&1 | tail -2
echo "$(date +%T) dose export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_dose_v01.py --calib export 2>&1 | tail -2
echo "$(date +%T) EXPORTS DONE"
