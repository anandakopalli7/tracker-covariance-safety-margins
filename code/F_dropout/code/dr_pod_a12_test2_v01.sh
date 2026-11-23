#!/usr/bin/env bash
# Revision v13, A12 sec. 3a pre-lock test, part 2 (22 Nov 2026, Claude Opus 5.5, session F): re-run the dose step with the final
# dr_dose_v01.py (adds DR.masks_identical_all; the slope's remote results are reused, their full-sample value is checked on import),
# then the second program dr_recount_a12_v01.py on the same 35-run test set. Old runs only (exploratory).
set -u
R=/root/dr; FD=$R/ARS_TRIAL/revision_v13/work/F_dropout; PY=/opt/drpy/bin/python; W=${W:-13}
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
cd $R/job
mkdir -p $R/superseded_a12_test1; mv $FD/out_a12/TESTOLD_DR2_DOSE_v01*.json $R/superseded_a12_test1/
echo "$(date +%T) dose export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_dose_v01.py --test-old --calib export --outer 100 2>&1 | tail -1
echo "$(date +%T) dose import"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_dose_v01.py --test-old --calib import --outer 100 2>&1 | tail -1
echo "$(date +%T) recount"; cd $FD/recount && DR_ROOT=$FD DR_P_ROOT=$R/P NUMBA_CACHE_DIR=$R/numba_cache $PY -I dr_recount_a12_v01.py --test-old --outer 100 --nboot 20000 --threads $W 2>&1 | tail -4
echo "$(date +%T) TEST2 DONE"
