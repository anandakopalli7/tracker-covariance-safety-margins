#!/usr/bin/env bash
# Package F (revision v13): the held-out pipeline, part 2, after the pod double bootstrap (20 Nov 2026, Claude Opus 5.5).
# Needs out/calib/heldout_all_20261913.npz (and _20261914.npz if A10 2.6 uses the second inner seed), fetched and SHA-256 checked.
set -euo pipefail
cd "$(dirname "$0")/.."
test -f ../../LOCK_A10_2.txt || { echo "REFUSED: LOCK_A10_2.txt does not exist"; exit 1; }
PY="python -I"
VPY="venv/Scripts/python.exe -I"
echo "$(date) step 6: calibration and hypotheses from the pod results"
$VPY code/f06_score_v01.py heldout --calib=import > logs/f06_heldout_import_v02.out 2>&1
test -f out/F_DETECTOR_FINGERPRINT_v01.json || $PY code/f11_fingerprint_v01.py > logs/f11_fingerprint_v01.out 2>&1
echo "$(date) step 7: export for package A"
$PY code/f12_export_v01.py > logs/f12_export_v01.out 2>&1
echo "$(date) done"
