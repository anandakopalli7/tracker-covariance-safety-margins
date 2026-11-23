"""Speculative copies of slow running calibration tasks: queue on TARGET (an idle pod) the tasks that SOURCE is still running (each chunk is a
deterministic function of label, seed and outer range; whichever copy finishes first is fetched, the fetch skips names already on the laptop,
calib_merge checks the tiling and full-sample values). Skips tasks whose chunk is already in pods/yl12_chunks or already on TARGET.
Usage: python dup_l12.py TARGET SOURCE [MAX]"""
import sys, pathlib
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.path[:0] = [str(CD / 'ycheck'), str(CD / 'tools')]
import calib_capture_pods_v13 as CP
tgt, src = sys.argv[1], sys.argv[2]; mx = int(sys.argv[3]) if len(sys.argv) > 3 else 999
RUN = {'y_l12_main': 'y_calib_remote_v13.py', 'rc_yl12': 'rc_y_calib_remote_v13.py'}
have = {p.name for p in (CD / 'pods' / 'yl12_chunks').glob('*.npz')}
running = CP.ssh(src, 'ls /opt/calib/running').split()
on_tgt = set(CP.ssh(tgt, 'ls /opt/calib/todo /opt/calib/running /opt/calib/done 2>/dev/null').split())
lines = []
for f in running:
    lab, seed, rng = f[:-5].split('__'); lo, hi = (int(x) for x in rng.split('_'))
    if '%s_%s_o%d_%d.npz' % (lab, seed, lo, hi) in have or f in on_tgt: continue
    lines.append("printf '%s %s %d %d %s\\n' > /opt/calib/todo/%s" % (lab, seed, lo, hi, RUN[lab], f))
lines = lines[:mx]
for i in range(0, len(lines), 30): CP.ssh(tgt, ' && '.join(lines[i:i + 30]))
print(tgt, 'queued', len(lines), 'copies of tasks running on', src)
