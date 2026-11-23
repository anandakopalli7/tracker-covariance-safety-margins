"""Poll every 10 minutes (up to 2.5 h): run each variant when its 35 arrays exist, rerun B6 when the delayed-stop clearances exist, combine."""
import os, subprocess, sys, time
from rc_core import VARIANTS, RUNS, have_variant, OUT

t0 = time.time()
b6dir = OUT.replace('recount', 'out') + r'\b6\clear'
b6_done = False
launched = {}
while time.time() - t0 < 2.5 * 3600:
    for x in VARIANTS:
        if x not in launched and have_variant(x):
            time.sleep(20)
            launched[x] = subprocess.Popen([sys.executable, 'b_variants.py', x, '2000'], stdout=open(OUT + r'\log_%s.txt' % x, 'w'), stderr=subprocess.STDOUT, cwd=OUT)
            print(time.strftime('%H:%M:%S'), 'launched', x, flush=True)
            while sum(p.poll() is None for p in launched.values()) >= 3:
                time.sleep(10)
    if not b6_done and all(os.path.exists(r'%s\%s.npz' % (b6dir, r)) for r in RUNS):
        time.sleep(20)
        subprocess.run([sys.executable, 'b6.py'], cwd=OUT, stdout=open(OUT + r'\log_b6.txt', 'w'), stderr=subprocess.STDOUT)
        b6_done = True; print(time.strftime('%H:%M:%S'), 'b6 rerun', flush=True)
    status = dict(variants=[x for x in VARIANTS if have_variant(x)], b6=b6_done)
    print(time.strftime('%H:%M:%S'), status, flush=True)
    if len(launched) == len(VARIANTS) and b6_done and all(p.poll() is not None for p in launched.values()):
        break
    time.sleep(600)
subprocess.run([sys.executable, 'combine.py'], cwd=OUT, stdout=open(OUT + r'\log_combine.txt', 'w'), stderr=subprocess.STDOUT)
print('combined', flush=True)
