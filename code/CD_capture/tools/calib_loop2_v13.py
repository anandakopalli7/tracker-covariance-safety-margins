"""Calibration pod loop, version 2 (20 Nov 2026, 07:50 EST, Claude Opus 5.5). Moves files only; computes no value.

Why: the frozen tools/calib_pods_v13.py uploads task files straight into a pod's todo/ folder. A worker polling that folder can claim a
task file while SFTP is still writing it (0 bytes) and then runs with an empty task line; 4 of 96 tasks moved to new pods at 07:42 failed
that way (ValueError on '--seeds'). The frozen tool is not edited. This loop reuses its functions but uploads every task under a hidden
temporary name (todo/.<name>.part, which `ls todo` does not list) and renames it in the same SFTP batch, and it repairs failed tasks whose
pod copy is empty by re-uploading the laptop copy the same way. Fetch and delete are the frozen tool's own functions.
Usage: python -I calib_loop2_v13.py [--final-after]   (loops every 5 min until no claude-v13cd-k pod is left; deletes pods only after
pods/calib_run/ASSIGN_FINAL exists, as the frozen loop does)
"""
import pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_argv = sys.argv; sys.argv = [sys.argv[0]]            # the frozen module parses sys.argv at import
import calib_pods_v13 as C                             # noqa: E402
sys.argv = _argv
pv = C.pv
RUN = C.RUN
LOG = RUN / 'loop2.log'


def say(m):
    line = f'{pv.est()} {m}'; print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


def put_tasks(n, paths):
    lines = []
    for t in paths:
        tmp = f'/opt/calib/todo/.{t.name}.part'
        lines += [f'put "{t}" "{tmp}"', f'rename "{tmp}" "/opt/calib/todo/{t.name}"']
    r = pv.sftp(n, lines)
    if r.returncode != 0: raise RuntimeError(f'{n}: task upload failed {r.stderr[-300:]}')


def steal2():
    st = {n: C.pod_state(n)[0] for n in C.live_pods()}
    idle = [n for n, c in st.items() if c['todo'] == 0 and c['running'] < C.nproc_of(n)]
    for n in idle:
        donor = max(st, key=lambda m: st[m]['todo'])
        k = min(st[donor]['todo'] // 2, C.nproc_of(n) - st[n]['running'])
        if k <= 0: continue
        moved = C.ssh(donor, f'cd /opt/calib && for f in $(ls todo | tail -n {k}); do mv todo/$f stolen/$f 2>/dev/null && echo $f; done').split()
        if not moved: continue
        src = RUN / 'assigned' / donor; dst = RUN / 'assigned' / n; dst.mkdir(parents=True, exist_ok=True)
        put_tasks(n, [src / f for f in moved])
        for f in moved: (src / f).replace(dst / f)
        st[donor]['todo'] -= len(moved); st[n]['todo'] += len(moved)
        say(f'moved {len(moved)} queued tasks {donor} -> {n} (temp-name upload)')


def assign2():
    """As the frozen assign (deal unassigned tasks in proportion to vCPUs), with temp-name uploads."""
    td = RUN / 'tasks'; tasks = sorted(td.glob('*.task'))
    pods = [n for n in C.live_pods() if (C.CD / 'pods' / n / 'CALIB_UP').is_file()]
    if not tasks or not pods: say(f'nothing to assign ({len(tasks)} tasks, {len(pods)} pods)'); return
    w = [C.nproc_of(n) for n in pods]; tot = sum(w)
    quota = [round(len(tasks) * x / tot) for x in w]; quota[-1] = len(tasks) - sum(quota[:-1])
    order = sorted(tasks, key=lambda p: (p.name.split('__')[2], p.name)); i = 0
    for n, q in zip(pods, quota):
        mine = order[i:i + q]; i += q
        if not mine: continue
        ad = RUN / 'assigned' / n; ad.mkdir(parents=True, exist_ok=True)
        put_tasks(n, mine)
        for t in mine: t.replace(ad / t.name)
        say(f'{n}: assigned {len(mine)} (temp-name upload)')


def repair():
    for n in C.live_pods():
        out = C.ssh(n, 'cd /opt/calib && for f in $(ls failed); do echo "$f $(wc -c < failed/$f)"; done', timeout=120)
        for line in out.splitlines():
            if not line.strip(): continue
            f, size = line.split()
            local = RUN / 'assigned' / n / f
            if int(size) == 0 and local.is_file() and local.stat().st_size > 0:
                C.ssh(n, f'cd /opt/calib && rm -f failed/{f} logs/{f}.log')
                put_tasks(n, [local]); say(f'{n}: re-queued empty failed task {f} from the laptop copy')
            elif local.is_file() and int(size) == local.stat().st_size:
                # the worker read the file while SFTP was still writing it (partial line); SFTP then completed the same file, so the
                # pod copy is now whole: move it back to the queue (atomic rename)
                C.ssh(n, f'cd /opt/calib && mv failed/{f} todo/{f} && rm -f logs/{f}.log'); say(f'{n}: re-queued failed task {f} (pod copy complete)')
            else:
                say(f'{n}: failed task left for inspection: {f} (pod {size} bytes)')


def main():
    while C.live_pods():
        final = (RUN / 'ASSIGN_FINAL').is_file()
        for step in ((C.fetch, steal2, repair, C.down) if final else (C.fetch, steal2, repair)):
            try: step()
            except Exception as e: say(f'{step.__name__} failed: {type(e).__name__} {str(e)[:200]}')
        try:
            for n in C.live_pods():
                cnt, _ = C.pod_state(n); say(f'{n} {cnt}')
        except Exception as e: say(f'status failed: {type(e).__name__}')
        have = len(list((RUN / 'chunks').glob('*.npz'))) if (RUN / 'chunks').exists() else 0
        say(f'chunk files on the laptop: {have} of {len(list((RUN / "assigned").rglob("*.task")))} assigned')
        if C.live_pods(): time.sleep(300)
    say('loop2 done: no calibration pod left')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'assign':
        assign2()
    else:
        main()
