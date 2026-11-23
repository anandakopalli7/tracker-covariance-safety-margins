#!/usr/bin/env bash
# Revision v13, AMENDMENT_12 sec. 3d: DR at 10 Hz on the NEW runs, post-lock chain ON THE POD (22 Nov 2026, Claude Opus 5.5, session F).
# Written after LOCK_A12d; it only starts the frozen programs (FREEZE_DR_A12_ADD03) in the order of sec. 3d: identity arrays (id0: no
# mask, configuration of record; id3: punish_num = 15, no mask), the masked arrays (dr), the analysis with the calibration exported,
# and the first inner seed of the calibration (calib_remote_v13, as sec. 3a). The coverage check, the second seed if needed, and the
# import are started separately. Needs LOCK_A12d.txt on the pod and the b7l12 rows.
set -u
R=/root/dr
V13=$R/ARS_TRIAL/revision_v13
FD=$V13/work/F_dropout
CA=$V13/work/CD_capture/analysis
PY=/opt/drpy/bin/python
W=${W:-13}
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
test -f $V13/LOCK_A12d.txt || { echo "REFUSED: no LOCK_A12d.txt"; exit 1; }
cd $R/job
X="$PY -I -B -X utf8 $FD/code/dr_extract_v03.py"
for m in id0 id3 dr; do echo "$(date +%T) $m"; $X $m --workers $W | tail -1; done
echo "$(date +%T) ARRAYS DONE"
echo "$(date +%T) analysis export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v03.py --calib export 2>&1 | tail -2
echo "$(date +%T) calibration seed 20261913"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $CA/calib_remote_v13.py $FD/out_a12/hz10/calib dr_main --seeds 20261913 --threads $W 2>&1 | tail -2
echo "$(date +%T) HZ10 EXPORT AND SEED 1 DONE"
