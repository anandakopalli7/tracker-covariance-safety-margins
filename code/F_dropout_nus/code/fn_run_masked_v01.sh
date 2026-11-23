#!/usr/bin/env bash
# AMENDMENT_12 sec. 5b: the masked val run, once, on the pod, after LOCK_A12c.txt exists. New file, 22 Nov 2026 (Claude Opus 5.5,
# worker of package F). Order: T1 tracking with the masks and punish_num = 3 (fn02 masked) -> arrays (fn05 masked) -> scoring
# (fn06 prep, the double bootstrap of the first inner seed, finish; the second inner seed only if finish asks for it).
# val_order_v01.txt only orders the scenes for scheduling (longest first); it changes no value.
# Run from /root/fn/job (the links of the scoring modules' Windows paths) with fn_pods_v01.ENV set.
set -euo pipefail
H=/root/fn/ARS_TRIAL/revision_v13/work/F_dropout_nus
C=$H/code
test -f /root/fn/ARS_TRIAL/revision_v13/LOCK_A12c.txt || { echo "REFUSED: LOCK_A12c.txt does not exist"; exit 1; }
PYT="/opt/fnt/bin/python -I -B -X utf8"
PYK="/opt/fnk/bin/python -I -B -X utf8"
NP=${NP:-14}
echo "$(date -u) step 1: masked tracking"
$PYT $C/fn02_track_v01.py masked val $NP $(cat $C/val_order_v01.txt)
n=$( (ls $H/cache/tracks_masked/val/scene-*.npz 2>/dev/null | grep -v tmp || true) | wc -l); test "$n" -eq 150 || { echo "tracks: $n of 150"; exit 1; }
echo "$(date -u) step 2: arrays"
$PYT $C/fn05_arrays_v01.py arrays masked val $NP $(cat $C/val_order_v01.txt)
n=$( (ls $H/cache/arrays_masked/val/scene-*.npz 2>/dev/null | grep -v tmp || true) | wc -l); test "$n" -eq 150 || { echo "arrays: $n of 150"; exit 1; }
echo "$(date -u) step 3: scoring"
$PYK $C/fn06_score_v01.py prep masked val --threads $NP
$PYK $C/fn06_score_v01.py calib masked val --seed 20261913 --threads $NP
if ! $PYK $C/fn06_score_v01.py finish masked val > $H/logs/finish_1.out 2>&1; then
  cat $H/logs/finish_1.out
  grep -q NEED_SECOND_SEED $H/logs/finish_1.out || exit 1
  $PYK $C/fn06_score_v01.py calib masked val --seed 20261914 --threads $NP
  $PYK $C/fn06_score_v01.py finish masked val
else
  cat $H/logs/finish_1.out
fi
echo "$(date -u) done"
