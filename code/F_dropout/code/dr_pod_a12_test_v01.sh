#!/usr/bin/env bash
# Revision v13, AMENDMENT_12 sec. 3a: pre-lock TEST of DR on new runs, ON THE POD (22 Nov 2026, Claude Opus 5.5, session F). No new-run
# value: the whole A12 pipeline on the 35 OLD lead-braking fit runs (exploratory) at p in {0.05, 0.10, 0.20, 0.30}: masked P-bar, combine
# and masked arrays per p; DR0-DR2 at p = 0.10 (dr_analysis_v02: export, calib_remote 100 x 1000, import); the dose-response with the
# slope's double bootstrap (dr_dose_v01 export, dr_slope_remote_v01 100 x 1000, import) and the decomposition.
set -u
R=/root/dr
FD=$R/ARS_TRIAL/revision_v13/work/F_dropout
CDA=$R/ARS_TRIAL/revision_v13/work/CD_capture/analysis
PY=/opt/drpy/bin/python
W=${W:-13}
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
cd $R/job
X="$PY -I -B -X utf8 $FD/code/dr_extract_v02.py"
echo "$(date +%T) test id3 p=0.10"; $X id3 --p 0.10 --test-old --runs all --workers $W | tail -1
for p in 0.05 0.10 0.20 0.30; do
  echo "$(date +%T) test p=$p pbar/combine/dr"
  $X pbar --p $p --test-old --runs all --workers $W | tail -1
  $X combine --p $p --test-old | tail -1
  $X dr --p $p --test-old --runs all --workers $W | tail -1
done
echo "$(date +%T) test analysis v02 export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v02.py --p 0.10 --test-old --calib export --outer 100 2>&1 | tail -2
echo "$(date +%T) test calib_remote"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $CDA/calib_remote_v13.py $FD/out_a12/testold_p010/calib dr_main --threads $W 2>&1 | tail -1
echo "$(date +%T) test analysis v02 import"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v02.py --p 0.10 --test-old --calib import --outer 100 2>&1 | tail -2
echo "$(date +%T) test dose export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_dose_v01.py --test-old --calib export --outer 100 2>&1 | tail -3
echo "$(date +%T) test slope remote"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_slope_remote_v01.py $FD/out_a12/calib_dose_testold --threads $W 2>&1 | tail -3
echo "$(date +%T) test dose import"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_dose_v01.py --test-old --calib import --outer 100 2>&1 | tail -3
echo "$(date +%T) A12 TEST DONE"
