"""Tie Fig. 2's plotted frontier curves (first program) to the recounted shares (second program).

For each fresh-run family prefix (LB, and CI when present), read <P>.frontier.<SRC> = [[caution %...], [wrong-go %...]]
from the first program's C export. Then check:
  - every source uses the same caution levels (A10 section 2.3: 201 levels);
  - D(SRC) = fsum over levels of (F_F0 - F_SRC);
  - RR(SRC) = D(SRC) / D(E) equals the recount's RR key within TOL;
  - the room D(E) / n_levels (mean gap, pp) or D(E) (summed) equals the recount's <P>.R within TOL (both are reported).
Read only. Written by the coordinating session (Claude Opus 5.5) on 21 Nov 2026; not part of either program.

Usage: python -I check_frontier_tie_v01.py <A_EXPORT_C.json> <A_RECOUNT_C.json> <out.json>
Exit 0 if every check passes, 1 otherwise.
"""
import json
import math
import sys

TOL = 1e-9
RR_KEYS = {"E5": ["RR_E5"], "N": ["RR_N"], "CK3": ["RR_CK3"], "IMM": ["all.RR_IMM", "IMM.r"], "E": []}


def vals(p):
    d = json.load(open(p, encoding="utf-8"))
    return d.get("values", d)


def imm_group(P, ev, rv):
    """The IMM share is on the IMM tracker's own room: RR(IMM) = D(IMM, F0_IMM) / D(E_IMM, F0_IMM) vs <P>.IMM.r."""
    ks = {s: f"{P}.frontier.{s}" for s in ("IMM", "F0_IMM", "E_IMM")}
    if not all(k in ev for k in ks.values()):
        return None
    fr = {s: ev[k] for s, k in ks.items()}
    lv = fr["F0_IMM"][0]
    same = all(len(fr[s][0]) == len(lv) and all(a == b for a, b in zip(fr[s][0], lv)) for s in fr)
    f0 = fr["F0_IMM"][1]
    D = {s: math.fsum(a - b for a, b in zip(f0, fr[s][1])) for s in ("IMM", "E_IMM")}
    rec = rv.get(f"{P}.IMM.r")
    chk = [{"what": "IMM group: same caution levels", "n_levels": len(lv), "ok": same}]
    if D["E_IMM"] == 0 or rec is None:
        chk.append({"what": f"RR(IMM) vs {P}.IMM.r", "D": D, "recount": rec, "ok": None})
    else:
        rr = D["IMM"] / D["E_IMM"]
        chk.append({"what": f"RR(IMM) on its own room vs {P}.IMM.r", "first_curves": rr, "recount": rec,
                    "abs_diff": abs(rr - rec), "ok": abs(rr - rec) <= TOL})
    return chk


def family(P, ev, rv):
    srcs = sorted(k.split(".", 2)[2] for k in ev if k.startswith(P + ".frontier."))
    imm = imm_group(P, ev, rv)
    if imm is not None:
        srcs = [s for s in srcs if s not in ("IMM", "F0_IMM", "E_IMM")]
    out = {"prefix": P, "sources": srcs, "checks": list(imm or []), "ok": True}
    if imm is not None:
        out["ok"] = all(c["ok"] is True for c in imm)
    if not srcs:
        out["ok"] = None
        return out
    if "F0" not in srcs or "E" not in srcs:
        out["checks"].append({"what": "F0 and E present", "ok": False})
        out["ok"] = False
        return out
    fr = {s: ev[f"{P}.frontier.{s}"] for s in srcs}
    lv = fr["F0"][0]
    same = all(len(fr[s][0]) == len(lv) and all(a == b for a, b in zip(fr[s][0], lv)) for s in srcs)
    out["checks"].append({"what": "same caution levels for every source", "n_levels": len(lv), "ok": same})
    out["ok"] &= same
    f0 = fr["F0"][1]
    D = {s: math.fsum(a - b for a, b in zip(f0, fr[s][1])) for s in srcs if s != "F0"}
    out["D_summed"] = D
    room_rec = rv.get(f"{P}.R")
    for name, room in (("mean gap", D["E"] / len(lv)), ("summed gap", D["E"])):
        if room_rec is None or (isinstance(room_rec, float) and math.isnan(room_rec)):
            out["checks"].append({"what": f"room ({name}) vs recount {P}.R", "first_curves": room, "recount": room_rec,
                                  "ok": None})
        else:
            out["checks"].append({"what": f"room ({name}) vs recount {P}.R", "first_curves": room, "recount": room_rec,
                                  "abs_diff": abs(room - room_rec), "ok": abs(room - room_rec) <= TOL})
    room_ok = [c["ok"] for c in out["checks"] if c["what"].startswith("room")]
    if room_rec is not None and not any(room_ok):
        out["ok"] = False
    for s in srcs:
        if s in ("F0", "E"):
            continue
        keys = [f"{P}.{k}" for k in RR_KEYS.get(s, [f"RR_{s}"]) if f"{P}.{k}" in rv]
        if not keys:
            out["checks"].append({"what": f"RR({s})", "ok": None, "note": "no recount key found"})
            continue
        rec = rv[keys[0]]
        if D["E"] == 0 or rec is None or (isinstance(rec, float) and math.isnan(rec)):
            out["checks"].append({"what": f"RR({s}) vs {keys[0]}", "D": D[s], "D_E": D["E"], "recount": rec,
                                  "ok": D[s] == 0 if D["E"] == 0 else None,
                                  "note": "ratio undefined (room zero or recount undefined); summed gap must be 0 if room is 0"})
            continue
        rr = D[s] / D["E"]
        ok = abs(rr - rec) <= TOL
        out["checks"].append({"what": f"RR({s}) vs {keys[0]}", "first_curves": rr, "recount": rec,
                              "abs_diff": abs(rr - rec), "ok": ok})
        out["ok"] &= ok
    return out


def main(a):
    ev, rv = vals(a[0]), vals(a[1])
    res = {"tolerance": TOL, "export": a[0], "recount": a[1],
           "families": [family(P, ev, rv) for P in ("LB", "CI")]}
    res["ok"] = all(f["ok"] is not False for f in res["families"]) and res["families"][0]["ok"] is True
    json.dump(res, open(a[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
    print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
