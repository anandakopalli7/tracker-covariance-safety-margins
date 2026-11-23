"""Y-L12 calibration on an extra pod (A11 newcal.py pattern): env (numpy + numba only), the frozen runners + the two L12 jobs, N workers at nice 19,
then take up to K unclaimed tasks from each OLD pod (atomic rename todo -> stolen on the old pod; a claimed task is never taken) and recreate
them on the new pod. Usage: python calnew_l12.py NEW N K OLD [OLD ...]"""
import sys, pathlib
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.path[:0] = [str(CD / 'ycheck'), str(CD / 'tools')]
import calib_capture_pods_v13 as CP
new, n, k, olds = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
PY = '/opt/b7py/bin/python'
print(CP.ssh(new, '( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/b7py && uv pip install -q --python %s numpy==2.5.4 numba==0.68.1 llvmlite==0.50.0 ) '
                  '> /root/cal_setup.log 2>&1; %s -c "import numpy, numba; print(numpy.__version__, numba.__version__)"' % (PY, PY), timeout=1800).strip())
J1 = CD / 'pods/claude-v13cd-l6/yl12_out/analysis/out/calib'; J2 = CD / 'pods/claude-v13cd-l6/yl12_out/recount/out/calib'
CP.prep(new, n, [str(J1 / 'y_l12_main.job.npz'), str(J1 / 'y_l12_main.meta.json'), str(J2 / 'rc_yl12.job.npz'), str(J2 / 'rc_yl12.meta.json'),
                 str(J2 / 'rc_yl12.state.npz')])
RUN = {'y_l12_main': 'y_calib_remote_v13.py', 'rc_yl12': 'rc_y_calib_remote_v13.py'}
tot = 0
for old in olds:
    moved = CP.ssh(old, 'cd /opt/calib && for f in $(ls todo | head -n %d); do mv todo/$f stolen/$f 2>/dev/null && echo $f; done' % k).split()
    lines = []
    for f in moved:
        lab, seed, rng = f[:-5].split('__'); lo, hi = rng.split('_')
        lines.append("printf '%s %s %d %d %s\\n' > /opt/calib/todo/%s" % (lab, seed, int(lo), int(hi), RUN[lab], f))
    for i in range(0, len(lines), 30): CP.ssh(new, ' && '.join(lines[i:i + 30]))
    print(new, 'took', len(moved), 'tasks from', old); tot += len(moved)
print(new, 'total', tot)
