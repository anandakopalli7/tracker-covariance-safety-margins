"""Driver: run b_variants for each variant whose 35 arrays all exist (at most 3 at a time), then combine. usage: python run_all.py"""
import subprocess, sys, os, time
from rc_core import VARIANTS, have_variant, OUT

done = set()
for x in VARIANTS:
    # a part is stale if written before the variant's last array file
    pass
procs = {}
todo = [x for x in VARIANTS if have_variant(x) and not os.path.exists(OUT + r'\parts\%s.json' % x)]
print('todo', todo, flush=True)
while todo or procs:
    while todo and len(procs) < 3:
        x = todo.pop(0)
        procs[x] = subprocess.Popen([sys.executable, 'b_variants.py', x, '2000'], stdout=open(OUT + r'\log_%s.txt' % x, 'w'), stderr=subprocess.STDOUT, cwd=OUT)
    for x in list(procs):
        if procs[x].poll() is not None:
            print(x, 'exit', procs[x].returncode, flush=True); del procs[x]
    time.sleep(5)
