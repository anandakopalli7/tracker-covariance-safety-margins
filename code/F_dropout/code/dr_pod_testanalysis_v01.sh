set -u
R=/root/dr; FD=$R/ARS_TRIAL/revision_v13/work/F_dropout; CDA=$R/ARS_TRIAL/revision_v13/work/CD_capture/analysis; PY=/opt/drpy/bin/python; W=13
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
cd $R/job
mkdir -p $R/superseded_v02_try1; mv $FD/out/calib_testold $FD/out/TESTOLD_DR_RESULTS_v01*.json $R/superseded_v02_try1/ 2>/dev/null
echo "$(date +%T) test analysis export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v01.py --test-old --calib export --outer 100 2>&1 | tail -4
echo "$(date +%T) test calib_remote"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $CDA/calib_remote_v13.py $FD/out/calib_testold dr_main --threads $W 2>&1 | tail -2
echo "$(date +%T) test analysis import"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v01.py --test-old --calib import --outer 100 2>&1 | tail -4
echo "$(date +%T) TEST ANALYSIS DONE"
