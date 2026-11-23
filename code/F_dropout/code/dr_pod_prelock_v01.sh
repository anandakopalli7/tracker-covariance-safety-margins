#!/usr/bin/env bash
# Revision v13, AMENDMENT_11 sec. 6c: DR's pre-lock chain ON THE POD (21 Nov 2026, Claude Opus 5.5, session F). No DR value:
# identity checks (i) and (ii) on the fresh runs (no mask), and the whole DR pipeline on the 35 OLD lead-braking fit runs (exploratory
# test set): masked P-bar pass, combine, masked arrays, analysis export, calib_remote (100 outer x 1000 inner), import.
set -u
R=/root/dr
FD=$R/ARS_TRIAL/revision_v13/work/F_dropout
CDA=$R/ARS_TRIAL/revision_v13/work/CD_capture/analysis
PY=/opt/drpy/bin/python
W=${W:-13}
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
cd $R/job
X="$PY -I -B -X utf8 $FD/code/dr_extract_v01.py"
echo "$(date +%T) id0"; $X id0 --workers $W | tail -2
echo "$(date +%T) id3"; $X id3 --workers $W | tail -2
echo "$(date +%T) test pbar"; $X pbar --test-old --runs all --workers $W | tail -2
echo "$(date +%T) test combine"; $X combine --test-old | tail -2
echo "$(date +%T) test dr"; $X dr --test-old --runs all --workers $W | tail -2
echo "$(date +%T) test analysis export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v01.py --test-old --calib export --outer 100 2>&1 | tail -3
echo "$(date +%T) test calib_remote"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $CDA/calib_remote_v13.py $FD/out/calib_testold dr_main --threads $W 2>&1 | tail -3
echo "$(date +%T) test analysis import"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v01.py --test-old --calib import --outer 100 2>&1 | tail -3
echo "$(date +%T) PRELOCK CHAIN DONE"
