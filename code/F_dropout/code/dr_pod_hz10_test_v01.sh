#!/usr/bin/env bash
# Revision v13, AMENDMENT_12 sec. 3d: pre-lock TEST of DR at 10 Hz ON THE POD (22 Nov 2026, Claude Opus 5.5, session F). Old run
# p1b_fit_finite_0037 only (the one old run with B7 rows; exploratory): id0 (no mask, configuration of record; compared on the laptop
# with CD's accepted B7_10_0.1 test array), id3 (punish_num = 15, no mask), dr (10 Hz masks, punish_num = 15, A11's P-bar_DR), and the
# analysis code path (dr_analysis_v03 --test-old --no-calib; one run, so the bootstrap is degenerate: a code test only).
set -u
R=/root/dr; FD=$R/ARS_TRIAL/revision_v13/work/F_dropout; PY=/opt/drpy/bin/python
export V13_CODEX_ROOT=$R/codex V13_P_ROOT=$R/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=$R/numba_cache
cd $R/job
X="$PY -I -B -X utf8 $FD/code/dr_extract_v03.py"
for m in id0 id3 dr; do echo "$(date +%T) test $m"; $X $m --test-old --workers 1 | tail -1; done
echo "$(date +%T) analysis v03 test (code path)"; NUMBA_NUM_THREADS=4 $PY -I -B -X utf8 $FD/code/dr_analysis_v03.py --test-old --no-calib --nboot 2000 2>&1 | tail -2
echo "$(date +%T) HZ10 TEST DONE"
