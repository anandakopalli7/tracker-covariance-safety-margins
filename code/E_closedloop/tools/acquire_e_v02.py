"""Package E: acquire_e_v01.py with a DNS-robust RunPod API path (19 Nov 2026, 22:40 EST). Frozen files are not edited:
this wrapper patches pods_e_v01 in memory and then runs acquire_e_v01.main() unchanged.

Why: the laptop's resolver took 5-40 s per lookup of api.runpod.io and sometimes timed out (measured 22:33 EST), longer than
runpodctl's client timeout, so 28 of 28 create attempts for pods 05..09 since 21:38 failed with network errors (not stock).
A successful lookup is cached by Windows, so a lookup made just before runpodctl lets runpodctl resolve from the cache.

Changes, in memory only:
1. pv.rp: runpodctl runs with GODEBUG=netdns=go (Go's own resolver). Measured 22:50 EST: default resolver 0 of 2 calls
   succeeded, cgo 0 of 2, netdns=go 2 of 2 (8 s, 29 s). Warming the Windows cache from Python did not help runpodctl.
   If runpodctl still fails with a DNS error ("lookup api.runpod.io"), the request never left, so it is retried (any
   command, up to 4 times). A header timeout is retried only for read-only commands (pod list, pod get, user).
2. pv.create: first list pods (retried until the list succeeds, up to about 10 min). If a pod with this name already
   exists (an earlier uncertain create), adopt it instead of creating a second one.

python -I acquire_e_v02.py <same arguments as acquire_e_v01.py>
"""
import os, pathlib, socket, sys, time, json

os.environ['GODEBUG'] = 'netdns=go'   # inherited by every runpodctl subprocess (pv.rp copies os.environ minus the key)
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pods_e_v01 as pv   # noqa: E402

_rp0 = pv.rp
_create0 = pv.create
READ_ONLY = {('pod', 'list'), ('pod', 'get'), ('user',)}


def warm_dns():
    for i in range(4):
        try:
            socket.getaddrinfo('api.runpod.io', 443); return True
        except OSError as e:
            print('dns warm-up failed', i + 1, repr(e)[:100], flush=True); time.sleep(5)
    return False


def rp(*args, check=True, timeout=1200):
    ro = tuple(args[:2]) in READ_ONLY or tuple(args[:1]) in READ_ONLY
    r = None
    for i in range(4):
        r = _rp0(*args, check=False, timeout=timeout)
        if r.returncode == 0: break
        txt = r.stdout + r.stderr
        dns_fail = 'lookup api.runpod.io' in txt
        hdr_timeout = 'awaiting headers' in txt or 'context deadline exceeded' in txt
        if dns_fail or (ro and hdr_timeout):
            print(f'rp retry {i + 1} {args[:2]}: {txt.strip()[-140:]}', flush=True); time.sleep(10); continue
        break
    if check and r.returncode != 0:
        raise SystemExit(f'runpodctl {args[0]} {args[1] if len(args) > 1 else ""} failed rc={r.returncode}: {r.stdout[-2000:]} {r.stderr[-2000:]}')
    return r


def create(name, gpu, deadline_h, note):
    pods = None
    for i in range(40):
        try:
            pods = json.loads(rp('pod', 'list', timeout=180).stdout); break
        except BaseException as e:
            print('pre-create pod list retry', i + 1, repr(e)[:120], flush=True); time.sleep(15)
    if pods is None:
        raise SystemExit('pre-create pod list failed; not creating (cannot rule out an existing pod of this name)')
    found = [q for q in pods if q.get('name') == name]
    if found:
        print('pod named', name, 'already exists:', found[0]['id'], '- adopting it', flush=True)
        pv.adopt(name, found[0]['id'], gpu, deadline_h, note, None); return
    return _create0(name, gpu, deadline_h, note)


pv.rp = rp
pv.create = create

import acquire_e_v01   # noqa: E402  (uses the patched module object)

if __name__ == '__main__':
    acquire_e_v01.main()
