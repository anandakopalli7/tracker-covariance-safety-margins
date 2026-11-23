"""v13 package B: re-track the stored runs with one tracker variant (AMENDMENT_10_v13 section 3). New file, 19 Nov 2026 (Claude Opus 5.5).
Read-only on P; writes only B_retrack\\out\\retrack\\<variant>\\ (and out\\pbar\\).

pass pbar  : the 120 tuning runs (all six families). Per run: re-track (trk_tracker_v01.retrack_capture), then the P-bar rule of record
             (ol_pbar_v01: primary's nearest actor within 4 m at every assessment decision with a true target; class vehicle /
             pedestrian) on the re-tracked actors -> per-run sums; plus the per-run tracker record (tracks per frame, update NIS).
             'combine' then writes out\\pbar\\PBAR_<variant>_v01.json = {'Pbar': class -> sum / count, counts, runs}.
pass arrays: the 35 old evaluation lead-braking runs, the 20 lead-braking and the 20 cut-in tuning runs. Per run: re-track and
             trk_arrays_v01.extract with P-bar of the variant (F0_x, A10 section 2.1) -> <run>.npz (all keys) + the tracker record.
Tracker record per run (<run>_trk.npz): for every output track state (frame i, id, name, centre x y, velocity x y, P9 rows/cols
x y vx vy (4x4), state_time) and every update (track, frame, NIS position block, IMM mode probabilities after it).
Usage: python -I -B -X utf8 b_retrack_v01.py <variant> pbar|arrays <part> <nparts> [constants_json]
       python -I -B -X utf8 b_retrack_v01.py <variant> combine
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time, csv, traceback
LIB = pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers')
sys.path.insert(0, str(LIB))
import trk_env_v01 as env
env.setup()
import numpy as np
import trk_tracker_v01 as T
import trk_arrays_v01 as A

P = pathlib.Path(r'<library folder>')
M4 = P / '09_redesign' / 'm4_perception_model'
ROOT = pathlib.Path(__file__).resolve().parents[1] / 'out'
PBAR_DIR = ROOT / 'pbar'
PBAR_RECORD = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'


def index():
    rows = [r for r in csv.DictReader(open(M4 / 'run_index_m4_v02.csv', encoding='utf-8')) if r['use'] == '1']
    for r in rows:
        r['cap'] = pathlib.Path(r['cap']); r['rd'] = r['cap'].parents[3]
    return rows


def run_list(what):
    rows = index()
    if what == 'pbar':
        sel = [r for r in rows if r['set'] == 'tune']
        assert len(sel) == 120
    else:
        sel = [r for r in rows if (r['set'] == 'fit' and r['family'] == 'lead_braking')
               or (r['set'] == 'tune' and r['family'] in ('lead_braking', 'cutin'))]
        assert len(sel) == 75
    return sorted(sel, key=lambda r: (r['set'], r['archive']))


def tracker_record(ov, rec):
    fi = []; tid = []; nm = []; cx = []; cy = []; vx = []; vy = []; P4 = []; st = []
    for i, row in enumerate(ov['detections.jsonl']):
        for t in row['tracks']:
            P9 = np.asarray(t['P9'], float)
            fi.append(i); tid.append(int(t['id'])); nm.append(t['name']); cx.append(t['center'][0]); cy.append(t['center'][1])
            vx.append(t['velocity'][0]); vy.append(t['velocity'][1]); P4.append(P9[np.ix_([0, 1, 6, 7], [0, 1, 6, 7])]); st.append(t['state_time'])
    ut = []; uf = []; unis = []
    for r in rec.algebra:
        if r.get('kind') != 'update':
            continue
        x = np.asarray(r['prior']['state'], float).ravel(); Pp = np.asarray(r['prior']['P'], float)
        z = np.asarray(r['measurement'], float).ravel(); R = np.asarray(r['rotated_R'], float)
        nu = z[0:2] - x[0:2]; S = Pp[0:2, 0:2] + R[0:2, 0:2]
        ut.append(int(r['track'])); uf.append(int(r['timestamp'])); unis.append(float(nu @ np.linalg.solve(S, nu)))
    mt = []; mf = []; mstage = []; mmu = []
    for m in rec.modes:
        mt.append(m['track']); mf.append(m['timestamp']); mstage.append(m['stage']); mmu.append(m['mu'])
    return dict(trk_frame=np.array(fi, np.int32), trk_id=np.array(tid, np.int64), trk_name=np.array(nm, dtype='U16'),
                trk_cx=np.array(cx), trk_cy=np.array(cy), trk_vx=np.array(vx), trk_vy=np.array(vy),
                trk_P4=np.array(P4).reshape(-1, 4, 4), trk_state_time=np.array(st),
                upd_track=np.array(ut, np.int64), upd_frame=np.array(uf, np.int32), upd_nis=np.array(unis),
                mode_track=np.array(mt, np.int64), mode_frame=np.array(mf, np.int32), mode_stage=np.array(mstage, dtype='U8'),
                mode_mu=np.array(mmu, float).reshape(-1, 2))


def save(path, meta, arrs):
    tmp = path.with_name(path.name[:-4] + '.tmp.npz')
    np.savez_compressed(tmp, meta=json.dumps(meta), **arrs)
    os.replace(tmp, path)


def main():
    variant, what = sys.argv[1], sys.argv[2]
    out = ROOT / 'retrack' / variant
    out.mkdir(parents=True, exist_ok=True)
    if what == 'combine':
        acc = {c: np.zeros((4, 4)) for c in ('vehicle', 'pedestrian')}; cnt = {c: 0 for c in acc}; runs = []
        for r in run_list('pbar'):
            f = out / ('%s_pbar.npz' % r['archive'])
            z = np.load(f, allow_pickle=False)
            for c in acc:
                acc[c] += z['acc_' + c]; cnt[c] += int(z['cnt_' + c])
            runs.append(r['archive'])
        Pbar = {c: (acc[c] / max(cnt[c], 1)).tolist() for c in acc}
        doc = dict(code='b_retrack_v01.py combine', variant=variant, rule='ol_pbar_v01 on the re-tracked actors of the 120 tuning runs',
                   runs=len(runs), counts=cnt, Pbar=Pbar, written=time.strftime('%Y-%m-%d %H:%M:%S'))
        if variant == 'CV0':
            rec = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))
            doc['identity_vs_pbar_of_record'] = {c: float(np.abs(np.array(rec['Pbar'][c]) - np.array(Pbar[c])).max()) for c in acc}
            doc['identity_counts_of_record'] = rec.get('counts')
        PBAR_DIR.mkdir(parents=True, exist_ok=True)
        (PBAR_DIR / ('PBAR_%s_v01.json' % variant)).write_text(json.dumps(doc, indent=1), encoding='utf-8')
        print(json.dumps({k: doc[k] for k in doc if k != 'Pbar'}), flush=True)
        return
    part, nparts = int(sys.argv[3]), int(sys.argv[4])
    const = json.loads(pathlib.Path(sys.argv[5]).read_text(encoding='utf-8')) if len(sys.argv) > 5 else None
    PB = None
    if what == 'arrays':
        PB = json.loads((PBAR_DIR / ('PBAR_%s_v01.json' % variant)).read_text(encoding='utf-8'))['Pbar']
    log = out / ('%s_part%d.log' % (what, part))
    for i, r in enumerate(run_list(what)):
        if i % nparts != part:
            continue
        f = out / ('%s_%s.npz' % (r['archive'], 'pbar' if what == 'pbar' else 'arrays'))
        if f.exists():
            continue
        t0 = time.time()
        try:
            ov, rec = T.retrack_capture(r['cap'], variant, const=const)
            trk = tracker_record(ov, rec)
            with A.overlay(r['cap'], ov):
                if what == 'pbar':
                    acc, cnt = A.pbar_accumulate(r['cap'])
                    arrs = dict(acc_vehicle=acc['vehicle'], acc_pedestrian=acc['pedestrian'], cnt_vehicle=cnt['vehicle'],
                                cnt_pedestrian=cnt['pedestrian'], **trk)
                    meta = dict(run=r['archive'], set=r['set'], family=r['family'], variant=variant)
                else:
                    meta, ax = A.extract(r['rd'], r['cap'], PB, lead=True, a4=True)
                    meta.update(run=r['archive'], set=r['set'], variant=variant, pbar=PB)
                    arrs = dict(ax, **trk)
            meta['seconds'] = time.time() - t0
            save(f, meta, arrs)
            msg = '%s %s ok %.1fs' % (variant, r['archive'], meta['seconds'])
        except Exception as e:
            (out / ('%s_%s.err.json' % (r['archive'], what))).write_text(json.dumps(dict(error=repr(e)[:500], tb=traceback.format_exc()[-2500:])),
                                                                        encoding='utf-8')
            msg = '%s %s ERROR %s' % (variant, r['archive'], repr(e)[:200])
        with open(log, 'a', encoding='utf-8') as fh:
            fh.write(time.strftime('%H:%M:%S ') + msg + '\n')
        print(msg, flush=True)


if __name__ == '__main__':
    main()
