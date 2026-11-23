"""Until all 400 seed-1 chunks (y_l12_main and rc_yl12, 200 each) are on the laptop: fetch finished chunks from every pod; when a c pod has an
empty queue, queue copies of the tasks l3/l6 are still running (dup_l12 logic). Prints a line per round. Usage: python cal_loop_l12.py"""
import sys, pathlib, time, subprocess
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.path[:0] = [str(CD / 'ycheck'), str(CD / 'tools')]
import calib_capture_pods_v13 as CP
DEST = CD / 'pods' / 'yl12_chunks'
PODS = ['claude-v13cd-' + p for p in ('c1', 'c2', 'c3', 'c4', 'l3', 'l6')]
HERE = pathlib.Path(__file__).resolve().parent
while True:
    for p in PODS:
        try: CP.fetch(p, DEST)
        except SystemExit as e: print('fetch', p, str(e)[:200])
    n = {lab: len(list(DEST.glob(lab + '_20261913_o*.npz'))) for lab in ('y_l12_main', 'rc_yl12')}
    print(time.strftime('%H:%M:%S'), n, flush=True)
    if n['y_l12_main'] >= 200 and n['rc_yl12'] >= 200: break
    for c in PODS[:4]:
        st = CP.ssh(c, 'echo $(ls /opt/calib/todo | wc -l) $(ls /opt/calib/running | wc -l)').split()
        if st[0] == '0' and int(st[1]) < 11:
            for src in PODS[4:]:
                r = subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', str(HERE / 'dup_l12.py'), c, src, str(11 - int(st[1]))], capture_output=True, text=True)
                print(r.stdout.strip()[-200:], flush=True)
    time.sleep(150)
print('ALL CHUNKS ON THE LAPTOP', time.strftime('%H:%M:%S'))
