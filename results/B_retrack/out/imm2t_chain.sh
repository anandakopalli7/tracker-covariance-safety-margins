cd ARS_TRIAL/revision_v13/work/B_retrack/code
L=../out/imm2t/chain.log
echo "check start $(date '+%T')" >> $L
python -I -B -X utf8 b_imm2_tune_v01.py check >> $L 2>&1 || { echo "check FAILED $(date '+%T')" >> $L; exit 1; }
python -I -c "import json,sys; d=json.load(open('../out/imm2t/IMM2_TUNE_CHECK_v01.json')); sys.exit(0 if d['identical_to_frozen_run_stat'] else 3)" || { echo "identity NOT identical; stop $(date '+%T')" >> $L; exit 3; }
echo "kq start $(date '+%T')" >> $L
python -I -B -X utf8 b_imm2_tune_v01.py kq >> $L 2>&1 || { echo "kq FAILED $(date '+%T')" >> $L; exit 1; }
echo "sa2 start $(date '+%T')" >> $L
python -I -B -X utf8 b_imm2_tune_v01.py sa2 >> $L 2>&1 || { echo "sa2 FAILED $(date '+%T')" >> $L; exit 1; }
echo "chain done $(date '+%T')" >> $L
