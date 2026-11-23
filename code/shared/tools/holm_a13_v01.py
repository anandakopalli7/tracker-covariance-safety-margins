"""Holm across AMENDMENT_13's two primary hypotheses (A13 section 4), from the cleared export pairs. A copy of holm_a12_v01.py with only the family, m, names and dates changed.

Coordinator tool, written 22 Nov 2026 about 07:23 EST (laptop clock) by the coordinating session (Claude Opus 5.5), before any value of E6
existed (the coast-count p, 0.986, was known). It reads only the A_EXPORT_* / A_RECOUNT_* pairs and writes
work\\shared\\holm\\A13_HOLM_v01.json and .md. It computes no new statistic beyond Holm's step-down.

Rules (fixed in this file before the pending values exist):
  1. Registered p: each section's own one-sided bootstrap p, as exported (A13 2.5 and 3.4). The two programs'
     values must be equal (A10 10.1(c) already checked per pair; here exact equality or |diff| <= 1e-12 is required, else REFUSED).
  2. Family size m = 2 always. A hypothesis whose export pair does not exist at the cut-off is "not completed": p = 1 enters Holm
     (it cannot be rejected and it does not make another easier to reject). The table says so.
  3. Holm's step-down adjusted p: sort ascending; adj_(i) = max_{j<=i} min(1, (m - j + 1) p_(j)).
  4. Sensitivity, one convention for both: p_u = (1 + k) / (n + 1), where k = the count of resamples at or below the null
     (NaN counted, as each section says) and n = the resamples used by that section's p. Sections already in this form are
     unchanged; the others are converted from their exported p and n (k = round(p * n)).
  5. Rejection is reported at family-wise 0.05, one-sided, for both conventions. Labels follow A13 sections 2 and 3; Holm changes no label.
Usage: python -I holm_a13_v01.py [--write]
"""
import datetime as dt
import hashlib
import json
import math
import pathlib
import sys

WORK = pathlib.Path(__file__).resolve().parents[2]
OUT = WORK / "shared" / "holm"
B = 20000

# (id, label, first export, recount export, p key, convention, n key or fixed n)
FAMILY = [
    ("E6", "A13 section 2: closed-loop caution frontier, contact difference N - F0_D at N's time lost",
     "E_closedloop/out/A_EXPORT_E6.json", "E_closedloop/out/A_RECOUNT_E6.json", "E6.p_one", "plus1", B),
    ("COAST", "A13 section 3: N_DR against a fixed coast-count margin, open loop, 150 new runs",
     "F_nuscenes/out/A_EXPORT_DRF.json", "F_nuscenes/out/A_RECOUNT_DRF.json", "DRF.delta.p", "plus1", B),
]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def flat(d):
    out = {}

    def walk(x, pre):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{pre}.{k}" if pre else k)
        else:
            out[pre] = x
    walk(d, "")
    return out


def get(fl, key):
    for k in (key, "values." + key):
        if k in fl:
            return fl[k]
    raise KeyError(key)


def holm(ps):
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    adj = [None] * m
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (m - rank) * ps[i]))
        adj[i] = run
    return adj


def main(argv):
    rows, bad = [], []
    for hid, label, f1, f2, key, conv, nref in FAMILY:
        p1, p2 = WORK / f1, WORK / f2
        row = dict(id=hid, label=label, export=f1, recount=f2, key=key, convention=conv)
        if not (p1.exists() and p2.exists()):
            row.update(status="not completed", p=1.0, p_u=1.0, n=None, k=None)
            rows.append(row)
            continue
        a, b = flat(json.load(open(p1, encoding="utf-8-sig"))), flat(json.load(open(p2, encoding="utf-8-sig")))
        try:
            va, vb = get(a, key), get(b, key)
        except KeyError:
            bad.append(f"{hid}: key {key} missing in a program's export")
            continue
        if va is None or vb is None or abs(float(va) - float(vb)) > 1e-12:
            bad.append(f"{hid}: programs disagree on {key}: {va!r} vs {vb!r}")
            continue
        p = float(va)
        if conv == "plus1":
            n = int(nref)
            k = round(p * (n + 1)) - 1
            p_u = p
        else:
            if isinstance(nref, str):
                nv = float(get(a, nref))
                n = int(round(nv * B)) if nv <= 1.0 else int(nv)
            else:
                n = int(nref)
            k = int(round(p * n))
            p_u = (1 + k) / (n + 1)
        row.update(status="ran", p=p, p_u=p_u, n=n, k=k, sha_export=sha(p1), sha_recount=sha(p2))
        rows.append(row)
    if bad:
        print("REFUSED:\n  " + "\n  ".join(bad))
        return 1
    adj = holm([r["p"] for r in rows])
    adj_u = holm([r["p_u"] for r in rows])
    for r, x, y in zip(rows, adj, adj_u):
        r["p_holm"], r["p_u_holm"] = x, y
        r["reject_0.05"], r["reject_u_0.05"] = x <= 0.05, y <= 0.05
    doc = dict(tool="holm_a13_v01.py", tool_sha256=sha(__file__), written=dt.datetime.now().astimezone().isoformat(timespec="seconds"),
               m=len(rows), alpha_fw=0.05, rows=rows)
    md = ["# Holm across A13's primary hypotheses (A13 section 4)", "",
          f"Written {doc['written']} by holm_a13_v01.py (sha256 {doc['tool_sha256']}), coordinating session (Claude Opus 5.5).",
          "m = 2. A pair missing at the cut-off enters as p = 1 (not completed). Family-wise 0.05, one-sided.", "",
          "| id | hypothesis | status | registered p | Holm | reject | p, one convention (1+k)/(n+1) | Holm | reject |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['id']} | {r['label']} | {r['status']} | {r['p']:.3g} | {r['p_holm']:.3g} | {'yes' if r['reject_0.05'] else 'no'} "
                  f"| {r['p_u']:.3g} | {r['p_u_holm']:.3g} | {'yes' if r['reject_u_0.05'] else 'no'} |")
    text = "\n".join(md) + "\n"
    print(text)
    if "--write" in argv:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "A13_HOLM_v01.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
        (OUT / "A13_HOLM_v01.md").write_text(text, encoding="utf-8")
        print(f"WROTE {OUT / 'A13_HOLM_v01.json'} sha256 {sha(OUT / 'A13_HOLM_v01.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
