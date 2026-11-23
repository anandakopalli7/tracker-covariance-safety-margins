#!/usr/bin/env bash
# Package F (revision v13): the held-out pipeline, run once after LOCK_A10_2.txt exists. New file, 19 Nov 2026 (Claude Opus 5.5).
# v02 (20 Nov 2026, 06:00 EST, after Lock 2): run_val_v01.sh (frozen in FREEZE_F) with ONE fix: the step-1 guard counted the val
# caches with ls | wc -l, and ls exits 2 when there are none, which pipefail + set -e turned into a stop before step 1. No other line
# differs; no computation is affected (recorded in locks\FREEZE_F_ADD01.json and STATUS.md).
# Every step refuses the val scenes without Lock 2 (f_common_v01.require_split). Logs in work\F_nuscenes\logs\.
set -euo pipefail
cd "$(dirname "$0")/.."
test -f ../../LOCK_A10_2.txt || { echo "REFUSED: LOCK_A10_2.txt does not exist"; exit 1; }
PY="python -I"
VPY="venv/Scripts/python.exe -I"
# 20 Nov 2026: the clearance in force is the departure's (notes/F_DEPARTURE_CLEARANCE_v01.md). If its horizon rule found no room,
# F stops: no val tracking or scoring, only the provenance check and the export (both outcomes).
FA=""
if [ ! -f out/F_HORIZON_RULE_v02.json ]; then FA="--outcome-a"; HZ="None"   # fallback (a): the departure was not recounted in time
else HZ=$($PY -c "import json; print(json.load(open('out/F_HORIZON_RULE_v02.json'))['primary_horizon_s'])"); fi
if [ "$HZ" = "None" ]; then
  echo "$(date) F stopped at the horizon rule ${FA:-(v02)}: provenance check and export only"
  $PY code/f11_fingerprint_v01.py > logs/f11_fingerprint_v01.out 2>&1
  $PY code/f12_export_v01.py $FA > logs/f12_export_v01.out 2>&1
  echo "$(date) done"; exit 0
fi
# process budget (coordinator, 20 Nov 01:10 EST: at most 3 laptop processes until CD's extraction ends, about 15:00): NP worker
# processes per step, steps one after another. Each step skips scenes already written, so the run can be stopped and restarted
# with a larger NP.
NP=${NP:-3}
echo "$(date) step 0: detector consistency check (val NDS against 68.5; reported to the coordinator before any text)"
test -f out/F_DETECTOR_FINGERPRINT_v01.json || $PY code/f11_fingerprint_v01.py > logs/f11_fingerprint_v01.out 2>&1
echo "$(date) step 1: caches"
nc=$( (ls cache/val/scene-*.npz 2>/dev/null || true) | wc -l)
if [ "$nc" -ne 150 ]; then $PY code/f01_prepare_v01.py val > logs/f01_prepare_val_v01.out 2>&1; else echo "  150 val caches exist; step 1 skipped"; fi
echo "$(date) step 2: tracking (T1, then IMM), $NP processes"
$PY code/f02_track_v01.py T1 val $NP > logs/f02_track_T1_val_v01.out 2>&1
$PY code/f02_track_v01.py IMM val $NP > logs/f02_track_IMM_val_v01.out 2>&1
for t in T1 IMM; do n=$(ls cache/tracks_$t/val/*.npz | grep -v tmp | wc -l); test "$n" -eq 150 || { echo "tracks_$t: $n of 150"; exit 1; }; done
echo "$(date) step 3: arrays (T1, then IMM), $NP processes"
$PY code/f05_arrays_v01.py arrays T1 val $NP > logs/f05_arrays_T1_val_v01.out 2>&1
$PY code/f05_arrays_v01.py arrays IMM val $NP > logs/f05_arrays_IMM_val_v01.out 2>&1
for t in T1 IMM; do n=$(ls cache/arrays_$t/val/*.npz | grep -v tmp | wc -l); test "$n" -eq 150 || { echo "arrays_$t: $n of 150"; exit 1; }; done
echo "$(date) step 3b: clearances under the departure (and their checks), $NP processes"
$PY code/f15_clear_v02.py val $NP > logs/f15_clear_v02_val.out 2>&1
$PY code/f15_clear_v02.py summary val > logs/f15_clear_v02_val_summary.out 2>&1
$PY -c "import json,sys; d=json.load(open('out/F_CLEAR_V02_val_v01.json')); sys.exit(0 if d['checks_passed'] else 1)" || { echo "clear_v02 val checks failed"; exit 1; }
echo "$(date) step 4: scoring up to the double bootstrap; its job for the pod (out/calib/heldout_all.*)"
$VPY code/f06_score_v01.py heldout --calib=export > logs/f06_heldout_export_v02.out 2>&1
echo "$(date) step 5 (by hand, with the session watchdog): the double bootstrap on pods (f17_calib_pod_v01.py up / push / run /"
echo "  fetch into out/calib / down), then: bash code/run_val_finish_v01.sh"
echo "$(date) done (part 1)"
