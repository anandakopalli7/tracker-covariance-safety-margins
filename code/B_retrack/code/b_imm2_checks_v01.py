r"""v13 round 2 (AMENDMENT_12 s3c, s7): first-vs-second-program checks that the frozen comparator b_fresh_compare_v02.py does not do.
New file, 22 Nov 2026 (Claude Opus 5.5); additive, no frozen file changed. (Its key comparison of out\A_EXPORT_B.json against
out\A_RECOUNT_B.json covers the B.IMM2C.* and B.IMM2N.* keys.)
  rows <set>      set = fresh | new: per-resample arrays denE, n, D_N, D_E5x, D_CK3 of out\<fresh|new>\boot_IMM2.npz (first program)
                  against recount_fresh\out\boot_IMM2C.npz | boot_IMM2N.npz (second program); relative difference <= 1e-9 with
                  max(1, |a|, |b|) scaling, NaN = NaN (the rule of b_fresh_compare_v02.py). Writes out\compare\B_IMM2_ROWS_<set>_v01.json.
  modeprob <label> <set>   out\modeprob\MODEPROB_<label>_<set>_v01.json against recount_fresh\out\MODEPROB2_<label>_<set>_v01.json:
                  n, mean, median, share_gt05 and their intervals per phase, the same rule. Writes out\compare\B_MODEPROB_<label>_<set>_v01.json.
Usage: python -I -B -X utf8 b_imm2_checks_v01.py rows fresh|new   |   modeprob <label> old|fresh|new
"""
import sys, json, math, pathlib, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parents[1]
OUT = HERE / 'out'; RC = HERE / 'recount_fresh' / 'out'
TOL = 1e-9


def close(a, b):
    if a is None or b is None:
        return a is None and b is None
    a = float(a); b = float(b)
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    return abs(a - b) <= TOL * max(1., abs(a), abs(b))


def rows(rset):
    pa = OUT / rset / 'boot_IMM2.npz'
    pb = RC / ('boot_IMM2C.npz' if rset == 'fresh' else 'boot_IMM2N.npz')
    a = np.load(pa); b = np.load(pb); ent = {}
    for k in ('denE', 'n', 'D_N', 'D_E5x', 'D_CK3'):
        m = min(a[k].size, b[k].size); x = a[k][:m].astype(float); y = b[k][:m].astype(float)
        both = np.isnan(x) & np.isnan(y)
        err = np.where(both, 0., np.abs(x - y) / np.maximum(1., np.maximum(np.abs(x), np.abs(y))))
        ent[k] = dict(rows=int(m), rows_first=int(a[k].size), rows_second=int(b[k].size), max_rel=float(np.nanmax(err)) if m else None,
                      agree=bool(m and a[k].size == b[k].size and np.all(np.isfinite(err) & (err <= TOL))))
    doc = dict(code='b_imm2_checks_v01.py rows', run_set=rset, first=str(pa.relative_to(HERE)), second=str(pb.relative_to(HERE)), tol=TOL,
               arrays=ent, all_agree=all(e['agree'] for e in ent.values()), written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (OUT / 'compare').mkdir(parents=True, exist_ok=True)
    (OUT / 'compare' / ('B_IMM2_ROWS_%s_v01.json' % rset)).write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('IMM2 %s rows: %s; %s' % (rset, 'ALL AGREE' if doc['all_agree'] else 'DIFFER',
          '; '.join('%s %d/%d max_rel %.2g' % (k, e['rows'], e['rows_first'], e['max_rel']) for k, e in ent.items())))


def modeprob(label, rset):
    fa = OUT / 'modeprob' / ('MODEPROB_%s_%s_v01.json' % (label, rset))
    fb = RC / ('MODEPROB2_%s_%s_v01.json' % (label, rset))
    a = json.loads(fa.read_text(encoding='utf-8'))['by_phase']; b = json.loads(fb.read_text(encoding='utf-8'))
    b = b.get('by_phase', b)
    items = []
    for ph in ('pre', 'braking', 'stopped'):
        for k in ('n', 'mean', 'median', 'share_gt05', 'mean_ci', 'median_ci', 'share_gt05_ci'):
            x = a[ph][k]; y = b[ph][k]
            xs = x if isinstance(x, list) else [x]; ys = y if isinstance(y, list) else [y]
            items.append(dict(phase=ph, key=k, first=x, second=y, agree=bool(len(xs) == len(ys) and all(close(u, v) for u, v in zip(xs, ys)))))
    doc = dict(code='b_imm2_checks_v01.py modeprob', label=label, run_set=rset, first=str(fa.relative_to(HERE)), second=str(fb.relative_to(HERE)),
               compared=len(items), agree=sum(i['agree'] for i in items), differing=[i for i in items if not i['agree']],
               all_agree=all(i['agree'] for i in items), written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (OUT / 'compare').mkdir(parents=True, exist_ok=True)
    (OUT / 'compare' / ('B_MODEPROB_%s_%s_v01.json' % (label, rset))).write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print('mode probabilities %s %s: %d of %d agree' % (label, rset, doc['agree'], doc['compared']))


if __name__ == '__main__':
    if sys.argv[1] == 'rows':
        rows(sys.argv[2])
    elif sys.argv[1] == 'modeprob':
        modeprob(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(__doc__)
