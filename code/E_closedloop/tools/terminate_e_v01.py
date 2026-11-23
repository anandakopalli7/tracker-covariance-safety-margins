"""Package E: terminate one pod and confirm it is gone before marking or logging it (19 Nov 2026, 23:50 EST).

Why: CD saw `runpodctl pod delete` return rc=1 with the pod still running for 3 of 6 pods (22:36-23:02 EST), and a retry later
returned rc=0. pods_e_v01.delete (frozen) already requires rc=0 before writing TERMINATED and the spend row; this wrapper adds
the second condition: the pod's id must be absent from `runpodctl pod list`. Until both hold, it re-sends the delete
(at most 12 rounds, about 10 min) and writes nothing. runpodctl runs with GODEBUG=netdns=go (see acquire_e_v02.py).

python -I terminate_e_v01.py <pod name> --note TEXT
Exit 0 only after a confirmed delete (TERMINATED written with the evidence; spend row 'terminate' with the balance).
"""
import argparse, datetime, json, os, pathlib, sys, time

os.environ['GODEBUG'] = 'netdns=go'
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pods_e_v01 as pv   # noqa: E402


def listed_ids():
    for i in range(6):
        r = pv.rp('pod', 'list', check=False, timeout=180)
        if r.returncode == 0:
            try: return {q.get('id') for q in json.loads(r.stdout)}
            except Exception: pass
        print('pod list retry', i + 1, (r.stdout + r.stderr).strip()[-160:], flush=True); time.sleep(15)
    return None


def terminate(name, note):
    assert name.startswith(pv.PREFIX)
    d = pv.PODS / name; rec = json.loads((d / 'pod.json').read_text(encoding='utf-8')); pid = rec['id']
    if (d / 'TERMINATED').exists():
        print(name, 'already TERMINATED:', (d / 'TERMINATED').read_text(encoding='utf-8').strip()); return 0
    last_rc = None
    for rnd in range(12):
        r = pv.rp('pod', 'delete', pid, check=False, timeout=150); last_rc = r.returncode
        print(f'round {rnd + 1}: delete rc={r.returncode} {(r.stdout + r.stderr).strip()[-200:]}', flush=True)
        if r.returncode == 0:
            time.sleep(10)
            ids = listed_ids()
            if ids is not None and pid not in ids:
                ev = f'{pv.est()} delete rc=0; id {pid} absent from pod list ({len(ids)} pods listed)'
                (d / 'TERMINATED').write_text(ev + '\n', encoding='utf-8')
                pv.spend_row('terminate', pid, rec['gpu'], rec['costPerHr'], f'{name}; {note}; confirmed absent from pod list')
                print('CONFIRMED', ev, flush=True); return 0
            print('rc=0 but the pod is still listed (or the list failed); re-sending', flush=True)
        time.sleep(30)
    print(f'DELETE NOT CONFIRMED for {name} ({pid}), last rc={last_rc}; nothing written', flush=True); return 2


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('name'); ap.add_argument('--note', required=True)
    a = ap.parse_args()
    sys.exit(terminate(a.name, a.note))
