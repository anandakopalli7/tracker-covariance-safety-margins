"""Package F recount: synthetic decision arrays in the format of notes\\ARRAYS_FORMAT_F_v01.md, for tests only.
New file, 19 Nov 2026 (Claude Fable 5.2). Nothing here reads a nuScenes file. Output: recount\\synth\\arrays_<tracker>\\<split>\\.
Usage: python -I fr_synth_v01.py
"""
import json, pathlib, sys, zlib
sys.dont_write_bytecode = True
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE / 'synth'


def make_scene(rng, name, split, n):
    R = 17
    des = float(rng.uniform(4, 15))
    vb = np.sort(rng.uniform(0, des, (n, R)), axis=1)[:, ::-1].copy()        # cost order: fast rows first, roughly
    sw = rng.random((n, R)) < 0.15
    vb = np.where(sw, np.roll(vb, 1, axis=1), vb)
    lead = rng.uniform(2, 60, n)                                             # a lead distance
    lead[rng.random(n) < 0.25] = np.inf
    clear = lead[:, None] - 3. * vb + rng.normal(0, 1.5, (n, R))
    clear = np.where(clear < 0, 0., clear)                                   # contact = 0
    clear2 = np.maximum(clear, lead[:, None] - 2. * vb + rng.normal(0, 1.0, (n, R)))
    clear2 = np.where(np.isinf(lead)[:, None], np.inf, clear2)
    d = lead[:, None] - 3. * vb                                              # nominal distance at the constraint
    idx55 = np.full(n, R - 1); idx55[rng.random(n) < 0.1] = R - 2
    ev = np.ones(n, bool); ev[n - 6:] = False
    ev2 = np.ones(n, bool); ev2[n - 4:] = False
    inpath = np.isfinite(lead) & (lead < 45) & (rng.random(n) < 0.9)
    base = dict(idx55=idx55, vbar=vb, evaluated=ev, evaluated2=ev2, inpath=inpath, des=np.full(n, des),
                v0=rng.uniform(0, des, n), clear=np.where(ev[:, None], clear, np.nan),
                clear2=np.where(ev2[:, None], clear2, np.nan), now=np.arange(n) * 0.1, sweep=np.arange(n) * 2 + 80)
    out = {}
    for trk, spread in (('T1', 0.02), ('IMM', 0.25)):
        r2 = np.random.default_rng([zlib.crc32(name.encode()), 0 if trk == 'T1' else 1])
        z = dict(base)
        for suf, dd in (('', d), ('_2', d + vb)):
            s0 = 4.0
            cF0 = np.where(dd >= 0, dd * dd / s0, -np.inf)
            sN = s0 * 1.2 * np.exp(spread * r2.normal(size=(n, 1)) + 0.01 * r2.normal(size=(n, R)))
            cN = np.where(dd >= 0, dd * dd / sN, -np.inf)
            err = (clear if suf == '' else clear2) - dd
            sE = np.where(err < 0, err * err, 0.)
            with np.errstate(divide='ignore', invalid='ignore'):
                cE = np.where(dd >= 0, np.where(sE > 0, dd * dd / sE, np.inf), -np.inf)
            cTG = np.where(dd >= 0, dd * dd / (2. + vb) ** 2, -np.inf)
            far = np.isinf(lead)[:, None]
            cF0 = np.where(far, np.inf, cF0); cN = np.where(far, np.inf, cN); cE = np.where(far, np.inf, cE)
            cTG = np.where(far, np.inf, cTG)
            tie = r2.random((n, R)) < 0.05                                   # exact ties and zeros
            cF0 = np.where(tie & np.isfinite(cF0), np.round(cF0), cF0)
            cN = np.where(tie & np.isfinite(cN), np.round(cN), cN)
            cE = np.where(tie & np.isfinite(cE), np.round(cE), cE)
            z['cF0' + suf] = cF0; z['cN' + suf] = cN; z['cE' + suf] = cE; z['cTG' + suf] = cTG
        z['meta'] = np.array(json.dumps(dict(scene=name, split=split, tracker=trk, desired=des, synthetic=True)))
        out[trk] = z
    return out


def main(n_train=40, n_val=30):
    rng = np.random.default_rng(777)
    for split, ns in (('train', n_train), ('val', n_val)):
        for k in range(ns):
            name = 'scene-%04d' % (k * 7 + (1 if split == 'train' else 3))
            sc = make_scene(rng, name, split, int(rng.integers(25, 60)))
            for trk, z in sc.items():
                d = ROOT / ('arrays_' + trk) / split
                d.mkdir(parents=True, exist_ok=True)
                np.savez(d / (name + '.npz'), **z)
            # clear_v02 (same as the arrays) and clear_v02mod (some contacts removed), for the tests of the departure path
            z = sc['T1']
            r3 = np.random.default_rng([zlib.crc32(name.encode()), 9])
            for sub, mod in (('clear_v02', False), ('clear_v02mod', True)):
                d = ROOT / sub / split
                d.mkdir(parents=True, exist_ok=True)
                c = {k: z[k].copy() for k in ('clear', 'clear2')}
                if mod:
                    for k in c:
                        flip = (c[k] <= 0) & (r3.random(c[k].shape) < 0.6)
                        c[k] = np.where(flip, 1.5, c[k])
                np.savez(d / (name + '.npz'), sweep=z['sweep'], clear_logged=c['clear'][:, 0], clear_logged2=c['clear2'][:, 0],
                         meta=z['meta'], **c)
    print('synthetic arrays written under', ROOT)


if __name__ == '__main__':
    main()
