"""Write revision_v13\\LOCK_A10_2.txt (stage 1 of Lock 2), or LOCK_A10_2c.txt (stage 2), after re-verifying every freeze.

Stage 1 (default): every package's freeze manifests, layered per package (FREEZE_<pkg>.json then its addenda,
in file-name order; FREEZE_CD_2* is stage 2 and excluded), plus Lock 1, LOCK_A10_2b and its note, F's departure
file and F's horizon-rule file. The values that A10 section 4 asks the lock to record are copied from the frozen
files (never typed here).
Stage 2 (--stage 2c): FREEZE_CD_2* layered over the CD core freeze, and LOCK_A10_2.txt's own hash.

A mismatch is allowed only for a living status note (file name STATUS.md); it is listed as excluded.
Any other mismatch or missing file, a Lock 1 mismatch, or an existing lock file stops the script.

Usage: python -I make_lock2_v01.py [--stage 2|2c] [--dry-run]
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import sys

WORK = pathlib.Path(__file__).resolve().parents[2]
REV = WORK.parent
LOCKS = WORK / "locks"
LIVING = {"status.md"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def entries(o):
    """Entries {path, sha256}; an addendum's replacement {path, sha256_after} counts with sha256_after."""
    if isinstance(o, dict):
        if "path" in o and "sha256" in o:
            yield o
        elif "path" in o and "sha256_after" in o:
            yield {"path": o["path"], "sha256": o["sha256_after"]}
        for v in o.values():
            yield from entries(v)
    elif isinstance(o, list):
        for v in o:
            yield from entries(v)


def resolve(p):
    q = pathlib.Path(p)
    if q.is_absolute():
        return q
    for base in (WORK, REV, REV.parent):
        if (base / q).exists():
            return base / q
    return WORK / q


def layered(manifests):
    want = {}
    for m in manifests:
        for e in entries(json.load(open(m, encoding="utf-8"))):
            want[str(resolve(e["path"])).lower()] = (e["path"], e["sha256"].lower())
    ok, living, bad = 0, [], []
    for _, (p, h) in sorted(want.items()):
        f = resolve(p)
        if not f.exists():
            bad.append(("MISSING", p))
        elif sha(f) != h:
            (living if f.name.lower() in LIVING else bad).append(("MISMATCH", p))
        else:
            ok += 1
    return dict(files=len(want), match=ok, living=living, bad=bad)


def group(prefix, exclude=()):
    ms = sorted(p for p in LOCKS.glob(prefix + "*.json")
                if not any(p.name.startswith(x) for x in exclude))
    return ms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="2", choices=["2", "2c"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    out = REV / ("LOCK_A10_2.txt" if a.stage == "2" else "LOCK_A10_2c.txt")
    stop = []
    if out.exists():
        stop.append(f"{out.name} already exists")
    lines = []
    if a.stage == "2":
        groups = {
            "B": group("FREEZE_B"),
            "CD (core)": group("FREEZE_CD", exclude=("FREEZE_CD_2",)),
            "E": group("FREEZE_E"),
            "F": group("FREEZE_F"),
        }
    else:
        if not (REV / "LOCK_A10_2.txt").exists():
            stop.append("LOCK_A10_2.txt does not exist")
        core = group("FREEZE_CD", exclude=("FREEZE_CD_2",))
        groups = {"CD (core + stage-2 additions)": core + group("FREEZE_CD_2")}
        if not group("FREEZE_CD_2"):
            stop.append("no FREEZE_CD_2*.json")
    for name, ms in groups.items():
        if not ms:
            stop.append(f"{name}: no manifest")
            continue
        r = layered(ms)
        lines.append(f"[{name}] layered {len(ms)} manifest(s): {r['files']} files, {r['match']} match")
        for m in ms:
            lines.append(f"  {m.relative_to(WORK)}  sha256 {sha(m)}")
        for kind, p in r["living"]:
            lines.append(f"  excluded (living status note, {kind.lower()}): {p}")
        for kind, p in r["bad"]:
            stop.append(f"{name}: {kind} {p}")
    extra = []
    if a.stage == "2":
        l1 = (REV / "LOCK_A10_1.txt").read_text(encoding="utf-8")
        amd = sha(REV / "AMENDMENT_10_v13.md")
        if amd not in l1:
            stop.append("AMENDMENT_10_v13.md hash differs from LOCK_A10_1.txt")
        for p in (REV / "LOCK_A10_1.txt", REV / "AMENDMENT_10_v13.md", LOCKS / "LOCK_A10_2b.txt",
                  LOCKS / "LOCK_A10_2b_NOTE_v01.txt", WORK / "F_nuscenes/notes/F_DEPARTURE_CLEARANCE_v01.md",
                  WORK / "F_nuscenes/out/F_HORIZON_RULE_v01.json", WORK / "F_nuscenes/out/F_HORIZON_RULE_v02.json"):
            if not p.exists():
                stop.append(f"missing {p}")
            else:
                extra.append(f"  {p.relative_to(REV)}  sha256 {sha(p)}")
        fb = json.load(open(LOCKS / "FREEZE_B.json", encoding="utf-8"))
        hz = json.load(open(WORK / "F_nuscenes/out/F_HORIZON_RULE_v02.json", encoding="utf-8"))
        rec = {
            "tuned_constants (FREEZE_B.json)": fb.get("tuned_constants"),
            "b4_filter_class (FREEZE_B.json)": fb.get("b4_filter_class"),
            "cut_in_lateral_threshold_m (FREEZE_B.json)": fb.get("cut_in_lateral_threshold_m"),
            "imm (FREEZE_B.json)": fb.get("imm"),
            "E matched settings": "LOCK_A10_2b.txt (hash above), with LOCK_A10_2b_NOTE_v01.txt on PS",
            "F route": "F-B, nuScenes (A10 section 0.3)",
            "F split (F_HORIZON_RULE_v02.json)": hz.get("split"),
            "F primary horizon s (F_HORIZON_RULE_v02.json, under the disclosed clearance departure)": hz.get("primary_horizon_s"),
        }
    else:
        extra.append(f"  LOCK_A10_2.txt  sha256 {sha(REV / 'LOCK_A10_2.txt')}" if (REV / "LOCK_A10_2.txt").exists() else "")
        rec = {}
    title = "LOCK_A10_2 (stage 1 of Lock 2, AMENDMENT_10_v13.md section 4)" if a.stage == "2" else \
        "LOCK_A10_2c (stage 2 of Lock 2: CD's section 5.7 additions)"
    body = [title, f"written: {now} by the coordinating session (Claude Opus 5.5), with shared/tools/make_lock2_v01.py "
            f"(sha256 {sha(pathlib.Path(__file__))})", "", "Freeze manifests, re-verified now:"] + lines
    body += ["", "Other files:"] + extra
    if rec:
        body += ["", "Values A10 section 4 asks the lock to record (copied from the frozen files):"]
        body += [f"  {k}: {json.dumps(v, ensure_ascii=False)}" for k, v in rec.items()]
    if a.stage == "2":
        body += ["", "Two-stage rule (README_COORDINATION.md, 20 Nov 01:53 EST; A10 section 11 departure, Table S4):",
                 "  - This lock covers every package's code except CD's section 5.7 additions (FREEZE_CD_2*).",
                 "  - Until LOCK_A10_2c.txt exists, no fresh C or D value and no fresh B value (Table III, TU, B6) is computed;",
                 "    frozen extractors and B's frozen re-tracking may write arrays that nobody reads;",
                 "    B's five-run second-IMM check (stage-1 code) may run.",
                 "  - E, F and the stage-1 parts start now."]
    if a.stage == "2":
        body += ["", "State: per each package's report and the gates in its code, no value of fresh, held-out or "
                 "closed-loop data had been computed when this lock was written."]
    else:
        body += ["", "State: per each package's report and the gates in its code, no fresh C or D value and no fresh B value "
                 "(Table III, TU, B6) had been computed when this lock was written. Under stage 1 (LOCK_A10_2) E's "
                 "closed-loop values and B's five-run second-IMM check had been computed, and F's held-out run had "
                 "started; their writers do not write stage-2 code.",
                 "Stage-1 deviation recorded since LOCK_A10_2: FREEZE_CD_add1 (REPLACEMENTS_C_v13.json [] -> {}, same "
                 "meaning, no code change; README_COORDINATION.md freeze ledger)."]
    text = "\n".join(body) + "\n"
    if stop:
        print("NOT WRITTEN:")
        for s in stop:
            print("  " + s)
        print("\n--- draft ---\n" + text)
        return 1
    if a.dry_run:
        print(text)
        return 0
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"{out} sha256 {sha(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
