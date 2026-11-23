"""Re-hash every file named in a v13 freeze manifest (locks\\FREEZE_<pkg>.json).

Any dict in the JSON with both "path" and "sha256" counts as an entry. A relative
path is resolved against work\\ first, then revision_v13\\. Read only.

Usage: python -I verify_freeze.py ..\\..\\locks\\FREEZE_B.json [more manifests]
Exit 0 if every entry matches, 1 otherwise.
"""
import hashlib
import json
import pathlib
import sys

WORK = pathlib.Path(__file__).resolve().parents[2]
REV = WORK.parent


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


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def layered(paths):
    """Later manifests override earlier ones for the same path (freeze plus addenda)."""
    want = {}
    for m in paths:
        for e in entries(json.load(open(m, encoding="utf-8"))):
            want[str(resolve(e["path"])).lower()] = (e["path"], e["sha256"].lower(), m)
    ok = bad = 0
    for _, (p, h, m) in sorted(want.items()):
        f = resolve(p)
        if not f.exists():
            bad += 1
            print(f"  MISSING  {p} (from {m})")
        elif sha(f) != h:
            bad += 1
            print(f"  MISMATCH {p} (from {m})")
        else:
            ok += 1
    print(f"layered {len(paths)} manifests: {len(want)} files, {ok} match, {bad} not")
    for m in paths:
        print(f"  {m} sha256 {sha(m)}")
    return 1 if bad else 0


def main(paths):
    if paths and paths[0] == "--layered":
        return layered(paths[1:])
    bad = 0
    for m in paths:
        d = json.load(open(m, encoding="utf-8"))
        es = list(entries(d))
        ok = miss = mism = 0
        for e in es:
            f = resolve(e["path"])
            if not f.exists():
                miss += 1
                print(f"  MISSING  {e['path']}")
            elif sha(f) != e["sha256"].lower():
                mism += 1
                print(f"  MISMATCH {e['path']}")
            else:
                ok += 1
        print(f"{m}: {len(es)} entries, {ok} match, {mism} mismatch, {miss} missing; manifest sha256 {sha(m)}")
        bad += mism + miss
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
