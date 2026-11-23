"""Write an AMENDMENT_11 lock file: revision_v13\\LOCK_A11.txt (stage 1: X, Y, B1r) or LOCK_A11b.txt (stage 2: DR, E4).

Coordinator tool, written 21 Nov 2026 by the coordinating session (Claude Opus 5.5). It changes nothing except the lock file
and one read-only snapshot copy of the amendment beside it. It refuses to overwrite an existing lock.

Spec (JSON) fields:
  stage      "1" or "b"
  title      one line
  groups     {name: [manifest path, ... in layering order]}   each group must verify layered with 0 mismatches
  files      {role: path}                                     hashed and listed (path, sha256, mtime)
  absent     {role: glob}                                     each glob must match no file (sealing evidence)
  state      [line, ...]                                      the coordinator's statement of state at writing
Usage: python -I make_lock_a11_v01.py <spec.json> [--write]
Without --write it prints the lock text and writes nothing.
"""
import contextlib
import datetime as dt
import glob
import hashlib
import io
import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_freeze as VF  # noqa: E402

WORK = HERE.parents[1]
REV = WORK.parent
A11 = REV / "AMENDMENT_11_v13.md"
if any(a.startswith("--amendment=") for a in sys.argv):
    A11 = REV / next(a.split("=", 1)[1] for a in sys.argv if a.startswith("--amendment="))


def sha(p):
    return VF.sha(p)


def mtime(p):
    return dt.datetime.fromtimestamp(pathlib.Path(p).stat().st_mtime).strftime("%d %b %H:%M:%S")


def main(argv):
    spec = json.load(open(argv[0], encoding="utf-8-sig"))
    write = "--write" in argv
    stage = spec["stage"]
    name = {"1": "LOCK_A11.txt", "b": "LOCK_A11b.txt", "c": "LOCK_A11c.txt",
            "a12a": "LOCK_A12a.txt", "a12b": "LOCK_A12b.txt", "a12c": "LOCK_A12c.txt", "a12d": "LOCK_A12d.txt",
            "a12e": "LOCK_A12e.txt", "a13a": "LOCK_A13a.txt", "a13b": "LOCK_A13b.txt", "a13c": "LOCK_A13c.txt"}[stage]
    allow = spec.get("allow", {})  # {substring of a manifest path: reason}; such entries are reported, not counted
    out = REV / name
    if out.exists():
        print(f"REFUSED: {out} exists")
        return 2
    now = dt.datetime.now().strftime("%d %b %Y %H:%M:%S")
    snap = REV / f"{A11.stem}_at_{name[:-4]}.md"
    lines = [spec["title"],
             f"Written: {now} EST by the laptop clock, by the coordinating session (Claude Opus 5.5), "
             f"with work\\shared\\tools\\make_lock_a11_v01.py (sha256 {sha(__file__)}).",
             "",
             f"Amendment: revision_v13\\{A11.name}, sha256 {sha(A11)}, modified {mtime(A11)}.",
             f"Snapshot copy at this lock: revision_v13\\{snap.name} (identical bytes).",
             "",
             "Freezes, verified layered at writing (verify_freeze.layered; 0 mismatches required):"]
    bad = 0
    for g, ms in spec["groups"].items():
        paths = [str(VF.resolve(m)) for m in ms]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = VF.layered(paths)
        summary = [x for x in buf.getvalue().splitlines() if x.startswith("layered")]
        lines.append(f"- {g}: {summary[0] if summary else '?'}")
        for m in paths:
            lines.append(f"    {pathlib.Path(m).name}  sha256 {sha(m)}  modified {mtime(m)}")
        if rc:
            miss = [x.strip() for x in buf.getvalue().splitlines() if "MISMATCH" in x or "MISSING" in x]
            unexplained = [x for x in miss if not any(k in x for k in allow)]
            for x in miss:
                why = next((r for k, r in allow.items() if k in x), None)
                lines.append(f"    {'ALLOWED' if why else 'FAILED'}: {x}" + (f"  ({why})" if why else ""))
            if unexplained:
                bad += 1
    lines += ["", "Files (path, sha256, modified):"]
    for role, p in spec["files"].items():
        q = VF.resolve(p)
        if not q.exists():
            bad += 1
            lines.append(f"- {role}: {p}  MISSING")
        else:
            lines.append(f"- {role}: {p}  sha256 {sha(q)}  modified {mtime(q)}")
    lines += ["", "Sealing evidence (each pattern must match no file at writing):"]
    for role, pat in spec.get("absent", {}).items():
        hits = glob.glob(str(VF.resolve(".") / pat) if not pathlib.Path(pat).is_absolute() else pat, recursive=True)
        lines.append(f"- {role}: {pat}  -> {len(hits)} file(s)")
        if hits:
            bad += 1
    lines += ["", "State at writing (coordinator's statement):"] + [f"- {s}" for s in spec["state"]]
    text = "\n".join(lines) + "\n"
    print(text)
    if bad:
        print(f"REFUSED: {bad} check(s) failed; nothing written")
        return 1
    if write:
        shutil.copyfile(A11, snap)
        out.write_text(text, encoding="utf-8")
        print(f"WROTE {out} sha256 {sha(out)}; snapshot {snap.name} sha256 {sha(snap)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
