"""Sanity checks for imm2_v01 (run: python -I -B -X utf8 check_imm2.py <const_json> <cap_dir> [<cap_dir> ...])."""
import os, sys, copy, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import imm2_v01 as M
import trk_env_v01

const = json.load(open(sys.argv[1], encoding='utf-8'))


def run(cap, diag, mu0, imm, watch=False):
    tr = M.build_tracker(const, diag, mu0, imm)
    out, stats = [], dict(mu_min=1.0, mu_max=0.0, musum=0.0, asym=0.0, mineig=0.0, nupd=0, n13eig=0.0)
    for row in trk_env_v01.jl(os.path.join(cap, 'detections.jsonl')):
        res = tr.step(copy.deepcopy(row['model']), row['time'])
        out.append([dict(id=r['id'], name=r['name'], P9=np.array(r['P9']), center=r['center'], velocity=r['velocity'], yaw=r['yaw']) for r in res])
        if watch:
            for tid, t in tr.tracker.valid_tras.items():
                f = t.motion_management
                if isinstance(f, M.IMM2Filter):
                    stats['mu_min'] = min(stats['mu_min'], f.mu.min()); stats['mu_max'] = max(stats['mu_max'], f.mu.max())
                    stats['musum'] = max(stats['musum'], abs(f.mu.sum() - 1))
                    P = f.P
                    stats['asym'] = max(stats['asym'], np.abs(P - P.T).max() / max(1e-300, np.abs(P).max()))
                    stats['mineig'] = min(stats['mineig'], np.linalg.eigvalsh((P + P.T) / 2).min())
                    stats['nupd'] += 1
    return out, stats


def cmp(a, b):
    worst = 0.0; n = 0
    assert len(a) == len(b)
    for fa, fb in zip(a, b):
        assert [r['id'] for r in fa] == [r['id'] for r in fb], 'track id sets differ'
        for ra, rb in zip(fa, fb):
            n += 1
            for k in ('P9',):
                d = np.abs(ra[k] - rb[k]).max() / max(1e-300, np.abs(rb[k]).max())
                worst = max(worst, d)
            for k in ('center', 'velocity'):
                d = np.abs(np.array(ra[k]) - np.array(rb[k])).max()
                worst = max(worst, d / max(1.0, np.abs(np.array(rb[k])).max()))
            worst = max(worst, abs(ra['yaw'] - rb['yaw']))
    return worst, n


for cap in sys.argv[2:]:
    print('CAPTURE', cap)
    o, st = run(cap, 0.95, (0.9, 0.1), True, watch=True)
    print(' IMM diag .95 run ok; frames', len(o), 'car-track-frames', st['nupd'], 'mu range [%.3e, %.6f]' % (st['mu_min'], st['mu_max']),
          'max|sum(mu)-1| %.2e' % st['musum'], 'max rel asym(P13) %.2e' % st['asym'], 'min eig(P13) %.3e' % st['mineig'])
    p9min = min(np.linalg.eigvalsh((r['P9'] + r['P9'].T) / 2).min() for f in o for r in f)
    p9as = max(np.abs(r['P9'] - r['P9'].T).max() / np.abs(r['P9']).max() for f in o for r in f)
    print(' P9 min eig %.3e, max rel asym %.2e (all classes)' % (p9min, p9as))
    o1, _ = run(cap, 1.0, (1.0, 0.0), True)
    ob3, _ = run(cap, 1.0, (1.0, 0.0), False)
    w, n = cmp(o1, ob3)
    print(' diag=1, mu0=(1,0) vs pure B3 (CANMOT EKFRotate, B3 cfg): %d track-frames, worst rel diff %.3e' % (n, w))
    ob3b, _ = run(cap, 1.0, (1.0, 0.0), False)
    # also: IMM(0.95) differs from B3 (sanity that the IMM is not a no-op)
    w2, _ = cmp(o, ob3)
    print(' IMM(.95,(.9,.1)) vs B3 worst rel diff %.3e (should be > 0)' % w2)
