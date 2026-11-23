"""AMENDMENT_12 sec. 5b, acceptance (before any masked value): the copied tracking (masks OFF, punish_num = 1) must reproduce F's
val T1 tracks bit for bit, or within 1e-14 absolute on every array (A10 B0(a)) where the pod's math library differs in the last
bit; the copied array builder on those tracks must reproduce F's val arrays within 1e-12 on every key (A10 B0(b)). New file,
22 Nov 2026 (Claude Opus 5.5, worker of package F). Light numpy only (no project code).
  hash DIR OUT.json                 per file and key: dtype, shape and SHA-256 of the C-order bytes; meta as JSON minus "seconds"
  diff REFDIR NEWDIR OUT.json [--keys-extra-ok k1,k2] [--meta-ignore k1,k2]
                                    per key: equal shapes and dtypes; for numbers the NaN / +-inf pattern, the count of elements that
                                    differ in any bit, the largest absolute difference and the largest relative difference (over
                                    finite pairs); strings must be equal; meta compared as JSON minus "seconds" and the ignored keys
                                    (numbers within the meta, e.g. identity-check maxima, compared as numbers and reported)
Every scene of REFDIR must exist in NEWDIR. Output: totals per key over all scenes, the worst scene per key, and verdicts:
bit_identical, max_abs over all numeric arrays, within_1e14_abs, within_1e12_abs, structure_identical (all non-float keys equal).
Usage: python -I fn07_accept_v01.py hash|diff ...
"""
import hashlib, json, pathlib, sys, time
import numpy as np


def files(d):
    return {p.stem: p for p in sorted(pathlib.Path(d).glob('*.npz')) if '.tmp' not in p.name}


def meta_of(z, ignore=()):
    m = json.loads(str(z['meta'])) if 'meta' in z.files else {}
    for k in ('seconds',) + tuple(ignore):
        m.pop(k, None)
    return m


def arr_sha(a):
    a = np.ascontiguousarray(a)
    h = hashlib.sha256(); h.update(a.dtype.str.encode()); h.update(repr(a.shape).encode()); h.update(a.tobytes())
    return h.hexdigest()


def do_hash(d, outf):
    res = {}
    for nm, p in files(d).items():
        z = np.load(p, allow_pickle=False)
        res[nm] = dict(meta=meta_of(z), keys={k: [z[k].dtype.str, list(z[k].shape), arr_sha(z[k])] for k in z.files if k != 'meta'})
    pathlib.Path(outf).write_text(json.dumps(dict(dir=str(d), n=len(res), files=res, written=time.strftime('%Y-%m-%d %H:%M:%S')),
                                             indent=0), encoding='utf-8')
    print('hashed', len(res), 'files ->', outf)


def num_cmp(a, b):
    """(bits_differ, pattern_differ, max_abs, max_rel) for two numeric arrays of equal shape."""
    a = np.asarray(a); b = np.asarray(b)
    if a.dtype.kind == 'b' or b.dtype.kind == 'b':
        nd = int((a != b).sum()); return nd, nd, float(nd > 0), float(nd > 0)
    af = a.astype(np.float64); bf = b.astype(np.float64)
    bits = int(np.sum(~((af == bf) | (np.isnan(af) & np.isnan(bf)))))
    pa = np.where(np.isnan(af), 3, np.where(np.isposinf(af), 1, np.where(np.isneginf(af), 2, 0)))
    pb = np.where(np.isnan(bf), 3, np.where(np.isposinf(bf), 1, np.where(np.isneginf(bf), 2, 0)))
    pat = int((pa != pb).sum())
    fin = (pa == 0) & (pb == 0)
    if fin.any():
        d = np.abs(af[fin] - bf[fin]); s = np.maximum(np.abs(af[fin]), np.abs(bf[fin]))
        mabs = float(d.max())
        with np.errstate(divide='ignore', invalid='ignore'):
            rel = np.where(s > 0, d / np.where(s > 0, s, 1.), 0.)
        mrel = float(rel.max())
    else:
        mabs = mrel = 0.
    return bits, pat, mabs, mrel


def flat_nums(x, pre=''):
    out = {}
    if isinstance(x, dict):
        for k, v in x.items():
            out.update(flat_nums(v, pre + str(k) + '.'))
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        out[pre[:-1]] = float(x)
    return out


def do_diff(ref, new, outf, extra_ok=(), meta_ignore=()):
    R = files(ref); N = files(new)
    missing = sorted(set(R) - set(N))
    tot = {}; worst = {}; probs = []; meta_num = {}
    for nm, p in R.items():
        if nm not in N:
            continue
        a = np.load(p, allow_pickle=False); b = np.load(N[nm], allow_pickle=False)
        ka = set(a.files) - {'meta'}; kb = set(b.files) - {'meta'} - set(extra_ok)
        if ka != kb:
            probs.append('%s: keys differ %s / %s' % (nm, sorted(ka - kb), sorted(kb - ka)))
        ma = meta_of(a, meta_ignore); mb = meta_of(b, meta_ignore)
        na_, nb_ = flat_nums(ma), flat_nums(mb)
        sa = {k: v for k, v in ma.items() if not isinstance(v, (dict, float))}
        sb = {k: v for k, v in mb.items() if not isinstance(v, (dict, float)) and k in sa}
        if sa != sb or set(na_) != set(nb_):
            probs.append('%s: meta differs %s / %s' % (nm, sa, sb))
        for k in na_:
            if k in nb_:
                d = abs(na_[k] - nb_[k]); meta_num[k] = max(meta_num.get(k, 0.), d)
        for k in sorted(ka & kb):
            x, y = a[k], b[k]
            t = tot.setdefault(k, dict(files=0, bits_differ=0, pattern_differ=0, max_abs=0., max_rel=0., shape_or_dtype_differ=0,
                                       string_differ=0, elements=0))
            t['files'] += 1
            if x.shape != y.shape or x.dtype != y.dtype:
                t['shape_or_dtype_differ'] += 1; probs.append('%s.%s: shape/dtype %s %s / %s %s' % (nm, k, x.shape, x.dtype, y.shape, y.dtype))
                continue
            t['elements'] += int(x.size)
            if x.dtype.kind in 'USO':
                t['string_differ'] += int((x != y).sum()); continue
            bits, pat, mabs, mrel = num_cmp(x, y)
            t['bits_differ'] += bits; t['pattern_differ'] += pat
            if mabs > t['max_abs']:
                t['max_abs'] = mabs; worst[k] = nm
            t['max_rel'] = max(t['max_rel'], mrel)
    float_keys = [k for k, t in tot.items() if t['elements'] and k in tot]
    allabs = max([t['max_abs'] for t in tot.values()] or [0.])
    structure = all(t['shape_or_dtype_differ'] == 0 and t['string_differ'] == 0 and t['pattern_differ'] == 0 for t in tot.values())
    bit_identical = (not missing and not probs and all(t['bits_differ'] == 0 and t['string_differ'] == 0
                                                       and t['shape_or_dtype_differ'] == 0 for t in tot.values()))
    doc = dict(ref=str(ref), new=str(new), n_ref=len(R), n_new=len(N), missing=missing, problems=probs[:50], n_problems=len(probs),
               per_key=tot, worst_scene_per_key=worst, meta_numbers_max_abs=meta_num, float_keys=float_keys,
               verdict=dict(bit_identical=bool(bit_identical), structure_identical=bool(structure and not missing and not probs),
                            max_abs_all_arrays=allabs, max_rel_all_arrays=max([t['max_rel'] for t in tot.values()] or [0.]),
                            within_1e14_abs=bool(structure and not missing and not probs and allabs <= 1e-14),
                            within_1e12_abs=bool(structure and not missing and not probs and allabs <= 1e-12)),
               written=time.strftime('%Y-%m-%d %H:%M:%S'))
    pathlib.Path(outf).write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print(json.dumps(doc['verdict']), 'problems', len(probs), 'missing', len(missing))


def opt(a, name):
    return tuple(x for x in a[a.index(name) + 1].split(',') if x) if name in a else ()


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'hash':
        do_hash(a[1], a[2])
    elif a[0] == 'diff':
        do_diff(a[1], a[2], a[3], opt(a, '--keys-extra-ok'), opt(a, '--meta-ignore'))
    else:
        raise SystemExit('mode?')
