r"""Revision v13, AMENDMENT_12 sec. 3a.6: identity checks (i) and (ii) of A11 sec. 6c.8 on the NEW runs. New file, 22 Nov 2026 (Claude
Opus 5.5, session F): a copy of dr_identity_v01.py (frozen in FREEZE_DR) with only the run set and folders changed:
  runs: the 'fresh' job ids of F_dropout\out_a12\p010\DR_MASKS_p010.json; ID0 / ID3: out_a12\p010rrays\{ID0,ID3}\<job id>.npz;
  reference: CD_capturerrays_l12\CV0\<job id>.npz (CD's CV0 arrays of record of the new runs, A12 sec. 2.3).
The rule (A10 B0(b), 1e-12 on every key both builders produce) and the report are v01's.
Usage: python -I dr_identity_v02.py   -> out_a12\DR2_IDENTITY_v01.json (refuses to overwrite)
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
OUT = DRD / 'out'
CV0 = WORK / 'CD_capture' / 'arrays_l12' / 'CV0'
A12 = DRD / 'out_a12' / 'p010'
READ_KEYS = ['k', 'idx55', 'evaluated', 'clear', 'vbar', 'des', 'cF0', 'cE', 'cN', 'cCK3', 'phase', 'lead_found', 'dx_pred3', 'now', 'age',
             'v0', 'track_id']
TOL = 1e-12
OWN = {'meta', 'dr_frame', 'dr_masked', 'dr_age', 'dr_gap'}


def ids():
    return sorted(json.loads((A12 / 'DR_MASKS_p010.json').read_text(encoding='utf-8'))['fresh'])


def cmp(a, b):
    za = np.load(a, allow_pickle=False); zb = np.load(b, allow_pickle=False)
    ka = set(za.files) - OWN; kb = set(zb.files) - OWN
    only_first, only_second = sorted(ka - kb), sorted(kb - ka)
    per = {}
    for k in sorted(ka & kb):
        x, y = za[k], zb[k]
        if x.dtype == y.dtype and x.shape == y.shape and np.array_equal(x, y, equal_nan=x.dtype.kind == 'f'):
            continue
        d = dict(dtype_shape_equal=bool(x.dtype == y.dtype and x.shape == y.shape))
        if d['dtype_shape_equal'] and x.dtype.kind in 'fiub':
            xx = x.astype(float); yy = y.astype(float); m = np.isfinite(xx) & np.isfinite(yy)
            dd = np.abs(xx[m] - yy[m])
            d.update(finite_pattern_equal=bool(np.array_equal(np.isfinite(xx), np.isfinite(yy)) and np.array_equal(np.isnan(xx), np.isnan(yy))),
                     max_abs=float(dd.max()) if dd.size else 0., n_values=int((dd > 0).sum()),
                     max_rel=float((dd / np.maximum(np.abs(yy[m]), 1e-300)).max()) if dd.size else 0.)
        per[k] = d
    return dict(only_first=only_first, only_second=only_second, n_common=len(ka & kb), all_identical=not per,
                read_keys_identical=not any(k in per for k in READ_KEYS),
                within_tol=all(v.get('dtype_shape_equal') and v.get('finite_pattern_equal') and v.get('max_abs', 1.) <= TOL for v in per.values()),
                differing=per)


def main():
    outf = DRD / 'out_a12' / 'DR2_IDENTITY_v01.json'
    if outf.exists(): raise SystemExit('REFUSED: %s exists' % outf)
    rids = ids(); res_i = {}; res_ii = {}
    for rid in rids:
        res_i[rid] = cmp(A12 / 'arrays' / 'ID0' / (rid + '.npz'), CV0 / (rid + '.npz'))
        a = np.load(A12 / 'arrays' / 'ID0' / (rid + '.npz')); b = np.load(A12 / 'arrays' / 'ID3' / (rid + '.npz'))
        ev = a['evaluated'].astype(bool)
        ch = np.zeros(ev.size, bool)
        for k in ('cF0', 'cE', 'cN'):
            x, y = a[k], b[k]
            ch |= ~np.all((x == y) | (np.isnan(x) & np.isnan(y)), axis=1)
        res_ii[rid] = dict(n_evaluated=int(ev.sum()), n_changed=int((ch & ev).sum()), evaluated_equal=bool(np.array_equal(a['evaluated'], b['evaluated'])))
    i_ok = all(v['within_tol'] and not v['only_first'] for v in res_i.values())
    keys = sorted({k for v in res_i.values() for k in v['differing']})
    doc = dict(code='dr_identity_v02.py', amendment='AMENDMENT_12 sec. 3a.6 (A11 sec. 6c.8)', reference=str(CV0),
               rule=dict(tol_abs=TOL, compared='every key both builders produce', read_keys=READ_KEYS,
                         citation='A10 sec. 3 B0(b): arrays rebuilt from replayed actor lists within 1e-12 of the stored ones; '
                                  'session B (21 Nov): CD CV0 arrays are built from logged tracks, so (b) applies'),
               check_i=dict(passed=i_ok, n_runs=len(rids),
                            all_common_keys_identical_runs=sum(1 for v in res_i.values() if v['all_identical']),
                            read_keys_identical_runs=sum(1 for v in res_i.values() if v['read_keys_identical']),
                            keys_only_in_reference=sorted({x for v in res_i.values() for x in v['only_second']}),
                            keys_only_in_replay=sorted({x for v in res_i.values() for x in v['only_first']}),
                            by_key={k: dict(runs=sum(1 for v in res_i.values() if k in v['differing']),
                                            max_abs=max(v['differing'][k].get('max_abs', float('inf')) for v in res_i.values() if k in v['differing']),
                                            max_rel=max(v['differing'][k].get('max_rel', float('inf')) for v in res_i.values() if k in v['differing']))
                                    for k in keys},
                            runs_read_keys_not_identical={k: v['differing'] for k, v in res_i.items() if not v['read_keys_identical']}),
               check_ii=dict(n_runs=len(rids), n_evaluated=sum(v['n_evaluated'] for v in res_ii.values()),
                             n_changed=sum(v['n_changed'] for v in res_ii.values()), runs_with_changes={k: v for k, v in res_ii.items() if v['n_changed']}),
               written=time.strftime('%Y-%m-%d %H:%M:%S'))
    outf.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps(dict(check_i=dict(passed=i_ok, read_keys_identical_runs=doc['check_i']['read_keys_identical_runs'],
                                       by_key=doc['check_i']['by_key']),
                          check_ii=dict(changed=doc['check_ii']['n_changed'], of=doc['check_ii']['n_evaluated']))))


if __name__ == '__main__':
    main()
