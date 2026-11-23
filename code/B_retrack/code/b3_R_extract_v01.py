"""v13 package B, B3 step (1) (AMENDMENT_10_v13 section 3, row B3): car-class measurement-noise terms from the detection errors.
New file, 19 Nov 2026 (Claude Opus 5.5). Read-only on P; writes only B_retrack\\out\\b3\\.

Rule (A10 B3 (1), spec IMM_AND_VARIANTS_SPEC_v01.md section 2): car-label boxes (CANMOT label 2) that ENTER THE TRACKER
(the tracker's own pre-processing: score threshold and NMS, M4 extract_tables_v01.preprocess), each matched to the nearest TRUE
VEHICLE (cache object cls == 'vehicle', present at the tick) within 5 m (2-D centre distance) on the same tick; clear view
(2-D visibility >= 0.99, M4 vis_ticks_v01.pkl); range <= 54 m (sensor to the object's centre); the 120 tuning runs only.
Errors in the object frame of the true heading h: position (along, across) = R(-h) (box centre - true centre); velocity
(along, across) = R(-h) (box velocity - true velocity). R terms = mean squared errors (bias included).
Inputs: M4 cache_v01 (per-run pickles built from the logs), vis_ticks_v01.pkl, run_index_m4_v02.csv (set == 'tune', use == 1).
Usage: python -I -B -X utf8 b3_R_extract_v01.py
"""
import pathlib, sys, json, math, pickle, time
M4 = pathlib.Path(r'<library folder>\m4_perception_model')
sys.path.insert(0, str(M4))
import m4_common_v02 as C            # read-only (pins BLAS; paths)
import numpy as np
import build_cache_v01 as B
import extract_tables_v01 as E1
import m4_geom_v01 as G

OUT = pathlib.Path(__file__).resolve().parents[1] / 'out' / 'b3'
OUT.mkdir(parents=True, exist_ok=True)
CAR = 2
MATCH_M = 5.0
RANGE_M = 54.0
VIS = 0.99


def main():
    C.setup_codex()
    from online_tracker import OnlineTracker
    rows = [r for r in C.load_index() if r['set'] == 'tune']
    assert len(rows) == 120, len(rows)
    L = OnlineTracker(C.tracker_config()).loader
    with open(M4 / 'vis_ticks_v01.pkl', 'rb') as f:
        vis_all = pickle.load(f)
    rec = []          # per matched box: run, k, along, across, v_along, v_across, range, dist
    n_car = 0; n_nomatch = 0; n_notclear = 0; n_far = 0
    t0 = time.time()
    for r in rows:
        c = B.load(r)
        key = B.key_of(r)
        assert abs(c['route_yaw']) < 1e-12
        objs = c['objects']; ego = c['ego']; K = c['K']
        v2 = vis_all[key]['vis2d']
        for fi, d in enumerate(c['det']):
            k = d['k']
            if k >= K:
                continue
            post = E1.preprocess(L, d['model'], fi)
            vehicles = [i for i, o in enumerate(objs) if o['present'][k] and o['cls'] == 'vehicle']
            sx, sy = ego['sx'][k], ego['sy'][k]
            for p in post:
                if int(p[13]) != CAR:
                    continue
                n_car += 1
                best, bd = -1, float('inf')
                for i in vehicles:
                    dd = math.hypot(p[0] - objs[i]['cx'][k], p[1] - objs[i]['cy'][k])
                    if dd < bd:
                        best, bd = i, dd
                if best < 0 or not (bd <= MATCH_M):
                    n_nomatch += 1
                    continue
                o = objs[best]
                ox, oy = o['cx'][k], o['cy'][k]
                rng = math.hypot(ox - sx, oy - sy)
                vis = float(v2[best, k])
                if not (vis >= VIS):
                    n_notclear += 1
                    continue
                if not (rng <= RANGE_M):
                    n_far += 1
                    continue
                h = float(o['heading'][k]); ch, sh = math.cos(h), math.sin(h)
                ex, ey = p[0] - ox, p[1] - oy
                evx, evy = p[6] - o['vx'][k], p[7] - o['vy'][k]
                rec.append((r['archive'], r['family'], k, ch * ex + sh * ey, -sh * ex + ch * ey, ch * evx + sh * evy, -sh * evx + ch * evy, rng, bd))
    a = np.array([x[3:] for x in rec], float)
    names = ['along', 'across', 'v_along', 'v_across']
    stats = {}
    for j, nm in enumerate(names):
        e = a[:, j]
        stats[nm] = dict(n=int(e.size), mean=float(e.mean()), sd=float(e.std(ddof=1)), mse=float(np.mean(e * e)))
    cfg = C.tracker_config()
    R0 = np.array(cfg['model_cfg']['matrix_r'][CAR], float)
    res = dict(code='b3_R_extract_v01.py', rule='A10 B3 (1); spec IMM_AND_VARIANTS_SPEC_v01.md section 2', runs=len(rows),
               n_car_boxes_entering=n_car, n_no_vehicle_within_5m=n_nomatch, n_not_clear=n_notclear, n_beyond_54m=n_far,
               n_used=len(rec), stats=stats,
               R_car_diag=dict(R_x=stats['along']['mse'], R_y=stats['across']['mse'], R_vx=stats['v_along']['mse'], R_vy=stats['v_across']['mse']),
               R_of_record_diag=dict(R_x=R0[0, 0], R_y=R0[1, 1], R_vx=R0[6, 6], R_vy=R0[7, 7]),
               by_family={fam: int(sum(1 for x in rec if x[1] == fam)) for fam in sorted({x[1] for x in rec})},
               seconds=time.time() - t0, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (OUT / 'B3_R_EXTRACT_v01.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
    print(json.dumps({k: res[k] for k in ('n_car_boxes_entering', 'n_no_vehicle_within_5m', 'n_not_clear', 'n_beyond_54m', 'n_used', 'R_car_diag',
                                         'R_of_record_diag', 'by_family')}, indent=1))


if __name__ == '__main__':
    main()
