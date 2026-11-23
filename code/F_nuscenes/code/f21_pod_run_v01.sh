#!/usr/bin/env bash
# Revision v13, AMENDMENT_12 sec. 5: run the mechanism check's two programs ON A POD, four jobs in parallel (22 Nov 2026, Claude Opus 5.5,
# session F). Moves no data and changes no program: f21_mech_v01.py (first program) and fm_recount_v01.py (second program, Sonnet) as
# frozen, with the command lines of the laptop plan. The recount's hard-coded Windows root resolves through a link named literally after
# it in the working folder (the DR pods' route). Usage: bash f21_pod_run_v01.sh first50 | val
set -u
R=/root/dr; V13=$R/ARS_TRIAL/revision_v13; FN=$V13/work/F_nuscenes; PY=/opt/drpy/bin/python; W=$R/mjob
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p $W $FN/out/mech; cd $W
ln -sfn $V13 "$W/ARS_TRIAL\\revision_v13"
test -f "$W/ARS_TRIAL\\revision_v13/work/F_nuscenes/recount_mech/fm_recount_v01.py" || { echo "REFUSED: link does not resolve"; exit 1; }
case "${1:-}" in
  first50) A1="design train"; A2="train"; EXTRA="--scenes 50 --no-calib";;
  val)     test -f $V13/LOCK_A12c.txt || { echo "REFUSED: no LOCK_A12c.txt"; exit 1; }
           A1="score"; A2="val"; EXTRA="";;
  *) echo "usage: first50 | val"; exit 1;;
esac
for tr in T1 IMM; do
  $PY -I -B $FN/code/f21_mech_v01.py $A1 $tr $EXTRA > $W/f21_${1}_$tr.log 2>&1 &
  $PY -I -B $FN/recount_mech/fm_recount_v01.py $A2 $tr $EXTRA > $W/rc_${1}_$tr.log 2>&1 &
done
wait
echo "$(date +%T) MECH $1 DONE"
for f in $W/f21_${1}_*.log $W/rc_${1}_*.log; do echo "== $f"; tail -4 $f; done
ls -la $FN/out/mech $FN/recount_mech
