#!/usr/bin/env bash
# AMENDMENT_12 sec. 5b, the REMAINING steps after the stop of 22 Nov 03:49 EST (notes\FN5B_RECORDS_ADD02.md): scoring only, with
# fn06_score_v02.py, on the masked tracks and arrays made on pod claude-v13f-n03 (fetched SHA-256 checked, uploaded again SHA-256
# checked). Nothing is re-tracked or rebuilt. New file, 22 Nov 2026 (Claude Opus 5.5, worker of package F); started once by
# post\fn_post_v02.py start. Run from /root/fn/job with fn_pods_v01.ENV set. NP only sets processes / threads; it changes no value.
set -euo pipefail
V=/root/fn/ARS_TRIAL/revision_v13
H=$V/work/F_dropout_nus
C=$H/code
test -f $V/LOCK_A12c.txt && test -f $V/LOCK_A12e.txt || { echo "REFUSED: LOCK_A12c.txt or LOCK_A12e.txt does not exist"; exit 1; }
test ! -e $H/out/masked_val/partial.json || { echo "REFUSED: a scoring output exists"; exit 1; }
PYK="/opt/fnk/bin/python -I -B -X utf8"
NP=${NP:-14}
for d in tracks_masked arrays_masked; do
  n=$( (ls $H/cache/$d/val/scene-*.npz 2>/dev/null | grep -v tmp || true) | wc -l)
  test "$n" -eq 150 || { echo "$d: $n of 150"; exit 1; }
done
echo "$(date -u) step 3: scoring with fn06_score_v02.py"
$PYK $C/fn06_score_v02.py prep masked val --threads $NP
$PYK $C/fn06_score_v02.py calib masked val --seed 20261913 --threads $NP
if ! $PYK $C/fn06_score_v02.py finish masked val > $H/logs/finish_v02_1.out 2>&1; then
  cat $H/logs/finish_v02_1.out
  grep -q NEED_SECOND_SEED $H/logs/finish_v02_1.out || exit 1
  echo "$(date -u) the second inner seed is needed"
  $PYK $C/fn06_score_v02.py calib masked val --seed 20261914 --threads $NP
  $PYK $C/fn06_score_v02.py finish masked val
else
  cat $H/logs/finish_v02_1.out
fi
echo "$(date -u) done"
