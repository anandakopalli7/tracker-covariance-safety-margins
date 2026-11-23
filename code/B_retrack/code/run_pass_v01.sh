#!/usr/bin/env bash
# v13 package B: run one pass (pbar|arrays) for the listed variants, 6 processes each, then combine (pbar).
cd "$(dirname "$0")"
PASS=$1; shift
for V in "$@"; do
  for p in 0 1 2 3 4 5; do
    OPENBLAS_CORETYPE=Haswell python -I -B -X utf8 b_retrack_v01.py "$V" "$PASS" $p 6 > /dev/null 2>&1 &
  done
  wait
  if [ "$PASS" = "pbar" ]; then OPENBLAS_CORETYPE=Haswell python -I -B -X utf8 b_retrack_v01.py "$V" combine; fi
  echo "$(date +%H:%M:%S) $PASS $V done"
done
