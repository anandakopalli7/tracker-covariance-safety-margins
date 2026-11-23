"""Coordinator pod watchdog for v13 (read-only: it never creates, stops or deletes a pod).

It polls the RunPod GraphQL API, appends one row per pod per poll to
watch\\pod_watch_log.csv, and EXITS with a printed reason when something needs a
person or a session to act. The coordinating session runs it as a tracked
background task, so its exit wakes the coordinator.

Exit reasons (exit code 10):
  LOW_BALANCE   balance below --alert-balance
  IDLE          a pod with GPU 0 % and CPU below --idle-cpu for --idle-polls polls in a row
  OVERDUE       a pod running longer than --max-uptime-h
  API_ERRORS    three failed polls in a row
  TIMEBOX       the watcher ran --run-h hours (re-arm it)

Usage:
  python -I rp_watch.py --once
  python -I rp_watch.py --alert-balance 100 --max-uptime-h 10.25 --run-h 6

The API key is read from %USERPROFILE%\\.runpod\\config.toml and sent only in an
Authorization: Bearer header. It is never printed or written.
"""
import argparse
import csv
import datetime as dt
import json
import os
import pathlib
import sys
import time
import urllib.request

import truststore

truststore.inject_into_ssl()

URL = "https://api.runpod.io/graphql"
HERE = pathlib.Path(__file__).resolve().parent
LOG = HERE / "watch" / "pod_watch_log.csv"
QUERY = """query { myself { clientBalance currentSpendPerHr pods {
  id name desiredStatus costPerHr
  runtime { uptimeInSeconds gpus { gpuUtilPercent memoryUtilPercent } container { cpuPercent memoryPercent } }
} } }"""


def api_key():
    cfg = pathlib.Path(os.environ["USERPROFILE"]) / ".runpod" / "config.toml"
    for line in cfg.read_text(encoding="utf-8").splitlines():
        k, _, v = line.partition("=")
        if k.strip() == "apikey":
            return v.strip().strip('"').strip("'")
    raise SystemExit("no apikey in config.toml")


def poll(key):
    req = urllib.request.Request(
        URL,
        data=json.dumps({"query": QUERY}).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key,
                 "User-Agent": "v13-pod-watch/1.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.loads(r.read())
    if body.get("errors"):
        raise RuntimeError(str(body["errors"])[:300])
    return body["data"]["myself"]


def summarise(me):
    rows = []
    for p in me.get("pods") or []:
        rt = p.get("runtime") or {}
        gpus = rt.get("gpus") or []
        cont = rt.get("container") or {}
        rows.append({
            "id": p["id"], "name": p.get("name"), "status": p.get("desiredStatus"),
            "usd_h": p.get("costPerHr"),
            "uptime_h": round((rt.get("uptimeInSeconds") or 0) / 3600, 2),
            "gpu_util": max([g.get("gpuUtilPercent") or 0 for g in gpus], default=None) if gpus else None,
            "cpu": cont.get("cpuPercent"),
        })
    return rows


def log_rows(now, me, rows):
    LOG.parent.mkdir(exist_ok=True)
    new = not LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["local_time", "balance", "spend_per_h", "pod_id", "name", "status",
                        "usd_h", "uptime_h", "gpu_util", "cpu"])
        if not rows:
            w.writerow([now, me.get("clientBalance"), me.get("currentSpendPerHr"), "", "", "", "", "", "", ""])
        for r in rows:
            w.writerow([now, me.get("clientBalance"), me.get("currentSpendPerHr"), r["id"], r["name"],
                        r["status"], r["usd_h"], r["uptime_h"], r["gpu_util"], r["cpu"]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--interval-s", type=int, default=300)
    ap.add_argument("--alert-balance", type=float, default=100.0)
    ap.add_argument("--max-uptime-h", type=float, default=10.25)
    ap.add_argument("--idle-cpu", type=float, default=5.0)
    ap.add_argument("--idle-polls", type=int, default=3)
    ap.add_argument("--ignore", default="", help="comma-separated pod ids to skip for IDLE")
    ap.add_argument("--run-h", type=float, default=6.0)
    a = ap.parse_args()
    key = api_key()
    ignore = {x for x in a.ignore.split(",") if x}
    idle_count = {}
    errors = 0
    t0 = time.time()
    while True:
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            me = poll(key)
            errors = 0
        except Exception as e:  # network or API error
            errors += 1
            print(f"{now} poll failed ({errors}): {type(e).__name__}: {str(e)[:200]}", flush=True)
            if errors >= 3:
                print("EXIT API_ERRORS", flush=True)
                return 10
            time.sleep(a.interval_s)
            continue
        rows = summarise(me)
        log_rows(now, me, rows)
        bal = me.get("clientBalance")
        print(f"{now} balance {bal} spend/h {me.get('currentSpendPerHr')} pods {len(rows)}", flush=True)
        for r in rows:
            print(f"   {r['id']} {r['name']} {r['status']} {r['usd_h']}/h up {r['uptime_h']} h gpu {r['gpu_util']} cpu {r['cpu']}", flush=True)
        if a.once:
            return 0
        reasons = []
        if bal is not None and bal < a.alert_balance:
            reasons.append(f"LOW_BALANCE {bal} < {a.alert_balance}")
        for r in rows:
            if r["status"] == "RUNNING" and r["uptime_h"] > a.max_uptime_h:
                reasons.append(f"OVERDUE {r['id']} {r['name']} up {r['uptime_h']} h")
            busy = (r["gpu_util"] or 0) > 0 or (r["cpu"] or 0) >= a.idle_cpu
            if r["status"] == "RUNNING" and r["uptime_h"] > 0 and not busy and r["id"] not in ignore:
                idle_count[r["id"]] = idle_count.get(r["id"], 0) + 1
                if idle_count[r["id"]] >= a.idle_polls:
                    reasons.append(f"IDLE {r['id']} {r['name']} for {idle_count[r['id']]} polls")
            else:
                idle_count[r["id"]] = 0
        if reasons:
            for x in reasons:
                print("EXIT " + x, flush=True)
            return 10
        if time.time() - t0 > a.run_h * 3600:
            print("EXIT TIMEBOX", flush=True)
            return 10
        time.sleep(a.interval_s)


if __name__ == "__main__":
    sys.exit(main())
