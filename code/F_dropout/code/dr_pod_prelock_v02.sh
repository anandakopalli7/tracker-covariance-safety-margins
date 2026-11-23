#!/usr/bin/env bash
# Revision v13, AMENDMENT_11 sec. 6c: DR's pre-lock TEST chain ON THE POD, v02 (21 Nov 2026, Claude Opus 5.5, session F): the code
# after the one mask law (dr_masks_v02: protocol case id, gap row) and the coordinator's 14:36 descriptives. No DR value: the whole DR
# pipeline on the 35 OLD lead-braking fit runs (exploratory test set). The fresh identity arrays (ID0, ID3) of v01's chain do not
# depend on the masks and are kept. The v01 test outputs (old mask wording) are moved aside, not used.
set -u
R=/root/dr
FD=$R/ARS_TRIAL/revision_v13/work/F_dropout
CDA=$R/ARS_TRIAL/revision_v13/work/CD_capture/analysis
PY=/opt/drpy/bin/python
W=${W:-13}
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
cd $R/job
mkdir -p $R/superseded_v01_test
for d in testold calib_testold TESTOLD_DR_RESULTS_v01_PENDING_CALIB.json; do [ -e $FD/out/$d ] && mv $FD/out/$d $R/superseded_v01_test/; done
X="$PY -I -B -X utf8 $FD/code/dr_extract_v01.py"
echo "$(date +%T) test id3"; $X id3 --test-old --runs all --workers $W | tail -2
echo "$(date +%T) test pbar"; $X pbar --test-old --runs all --workers $W | tail -2
echo "$(date +%T) test combine"; $X combine --test-old | tail -2
echo "$(date +%T) test dr"; $X dr --test-old --runs all --workers $W | tail -2
echo "$(date +%T) test analysis export"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v01.py --test-old --calib export --outer 100 2>&1 | tail -4
echo "$(date +%T) test calib_remote"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $CDA/calib_remote_v13.py $FD/out/calib_testold dr_main --threads $W 2>&1 | tail -3
echo "$(date +%T) test analysis import"; NUMBA_NUM_THREADS=$W $PY -I -B -X utf8 $FD/code/dr_analysis_v01.py --test-old --calib import --outer 100 2>&1 | tail -4
echo "$(date +%T) PRELOCK TEST V02 DONE"
