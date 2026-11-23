"""Package E, set E6 (A13 §E6.9): balance watchdog. Every --sleep seconds, reads the account balance (runpodctl user, with
GODEBUG=netdns=go). If it is below --floor (default 3.5 USD), it writes pods\\STOP_FINISH_E5 (the finisher stops) and deletes
every listed E6 pod that has no TERMINATED record, each with terminate_e_v01.py (rc = 0 and absent from the pod list). Runs
already finished are on the network volume and are fetched afterwards over S3. Reads only the balance otherwise. Log:
pods\\E6_BALANCE.log. Stop: pods\\STOP_E6_BALANCE.

python -I balance_watch_e6_v01.py --pods 41,42,43,44,45,46 [--floor 3.5] [--sleep 120]
"""
import argparse, datetime, os, pathlib, subprocess, sys, time

os.environ['GODEBUG'] = 'netdns=go'
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pods_e_v01 as pv   # noqa: E402
LOG = pv.PODS / 'E6_BALANCE.log'


def say(m):
    line = f'{datetime.datetime.now():%H:%M:%S} {m}'; print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--pods', required=True); ap.add_argument('--floor', type=float, default=3.5)
    ap.add_argument('--sleep', type=float, default=120)
    a = ap.parse_args(); names = [f'claude-v13e-{n}' for n in a.pods.split(',')]
    while not (pv.PODS / 'STOP_E6_BALANCE').exists():
        live = [n for n in names if not (pv.PODS / n / 'TERMINATED').exists()]
        if not live: say('all E6 pods deleted; watchdog ends'); return
        try: bal, rate = pv.balance()
        except BaseException as e: say(f'balance read failed: {str(e)[-160:]}'); time.sleep(30); continue
        say(f'balance {bal:.2f} rate {rate:.3f}/h live {len(live)}')
        if bal < a.floor:
            say(f'FLOOR {bal:.2f} < {a.floor}: stopping the finisher and deleting {live}')
            (pv.PODS / 'STOP_FINISH_E5').write_text('E6 balance floor\n', encoding='utf-8')
            for n in live:
                t = subprocess.run([sys.executable, '-I', str(HERE / 'terminate_e_v01.py'), n, '--note', f'E6 balance floor {a.floor} reached (balance {bal:.2f})'],
                                   capture_output=True, text=True, cwd=str(HERE))
                say(f'{"DELETED" if t.returncode == 0 else "DELETE NOT CONFIRMED"} {n} rc={t.returncode} {(t.stdout + t.stderr).strip()[-160:]!r}')
            return
        time.sleep(a.sleep)


if __name__ == '__main__':
    main()
