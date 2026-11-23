"""Read-only checks after FREEZE_CD_2_add4 (Fig. 2 frontier curves). New file, 21 Nov 2026 (Claude Opus 5.5).

(1) Unchanged keys: every key of the four exports kept in out/KEEP_before_add4 (A_EXPORT_C c7ad0499..., A_EXPORT_D 1100f41f...,
    A_RECOUNT_C a0804329..., A_RECOUNT_D e6a932fb...) is present in the new export with an identical value (Python ==, no tolerance);
    the only added keys are '<LB|CI>.frontier.*'. Other top-level fields are listed when they differ.
(2) Tie to the second program (coordinator's check, A10 sec. 10.1(c) tolerance 1e-9): each exported curve's summed gap to its F0
    over the 201 levels against the recount's values in out/A_RECOUNT_C.json:
      D_gl(E, F0) = 201 * LB.R;  D_gl(SRC, F0) = LB.RR_SRC * 201 * LB.R = LB.RR_SRC.dec * 20100 / LB.n_dec  (SRC = E5, N, CK3);
      IMM: sum(F0_IMM - IMM) = LB.IMM.r.dec * 20100 / LB.n_dec, and sum(F0_IMM - IMM) / sum(F0_IMM - E_IMM) = LB.IMM.r;
      CI: sum(F0 - E) = 201 * CI.R; sum(F0 - N) = CI.RR_N.dec * 20100 / CI.n_dec.
    (dec_eq of record: D / 201 / 100 * n, optA_lib_v02.dec_eq.)
Usage: python -I -B check_frontier_add4_v13.py  -> out/CHECK_FRONTIER_ADD4_v13.json (refuses to overwrite)
"""
import hashlib, json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; OUT = CD / 'out'; KEEP = OUT / 'KEEP_before_add4'
TOL = 1e-9


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def unchanged():
    res = {}
    for n in ('A_EXPORT_C', 'A_EXPORT_D', 'A_RECOUNT_C', 'A_RECOUNT_D'):
        old = json.loads((KEEP / f'{n}.json').read_text(encoding='utf-8')); new = json.loads((OUT / f'{n}.json').read_text(encoding='utf-8'))
        ov, nv = old['values'], new['values']
        changed = sorted(k for k in ov if k not in nv or nv[k] != ov[k])
        added = sorted(k for k in nv if k not in ov)
        bad_added = [k for k in added if '.frontier.' not in k]
        fields = sorted(k for k in set(old) | set(new) if k != 'values' and old.get(k) != new.get(k))
        res[n] = dict(old_sha256=sha(KEEP / f'{n}.json'), new_sha256=sha(OUT / f'{n}.json'), old_values=len(ov), new_values=len(nv),
                      changed_or_missing=changed, added=added, added_not_frontier=bad_added, other_fields_differing=fields,
                      deviations=[len(old.get('deviations', [])), len(new.get('deviations', []))],
                      outcomes_equal=old.get('outcomes') == new.get('outcomes'),
                      ok=not changed and not bad_added)
    return res


def tie():
    a = json.loads((OUT / 'A_EXPORT_C.json').read_text(encoding='utf-8'))['values']
    b = json.loads((OUT / 'A_RECOUNT_C.json').read_text(encoding='utf-8'))['values']

    def gap(p, x, y):
        cx, wx = a[f'{p}.frontier.{x}']; cy, wy = a[f'{p}.frontier.{y}']
        assert cx == cy and len(cx) == 201, (p, x, y)
        return math.fsum(u - v for u, v in zip(wx, wy))

    rows = []

    def add(name, curve, rec, how):
        rows.append(dict(check=name, from_curves=curve, from_recount=rec, recount_keys=how, abs_diff=abs(curve - rec), ok=abs(curve - rec) <= TOL))

    n, nc = b['LB.n_dec'], b['CI.n_dec']
    dE = gap('LB', 'F0', 'E')
    add('LB D_gl(E,F0)', dE, 201 * b['LB.R'], '201 * LB.R')
    add('LB D_gl(E,F0) (dec)', dE, b['LB.R.dec'] * 20100 / n, 'LB.R.dec * 20100 / LB.n_dec')
    for s in ('E5', 'N', 'CK3'):
        d = gap('LB', 'F0', s)
        add(f'LB D_gl({s},F0)', d, b[f'LB.RR_{s}'] * 201 * b['LB.R'], f'LB.RR_{s} * 201 * LB.R')
        add(f'LB D_gl({s},F0) (dec)', d, b[f'LB.RR_{s}.dec'] * 20100 / n, f'LB.RR_{s}.dec * 20100 / LB.n_dec')
        add(f'LB RR_gl({s})', d / dE, b[f'LB.RR_{s}'], f'LB.RR_{s}')
    di = gap('LB', 'F0_IMM', 'IMM'); dEi = gap('LB', 'F0_IMM', 'E_IMM')
    add('LB D_gl(IMM,F0_IMM) (dec)', di, b['LB.IMM.r.dec'] * 20100 / n, 'LB.IMM.r.dec * 20100 / LB.n_dec')
    add('LB RR_gl(IMM) on its own room', di / dEi, b['LB.IMM.r'], 'LB.IMM.r')
    add('CI D_gl(E,F0)', gap('CI', 'F0', 'E'), 201 * b['CI.R'], '201 * CI.R')
    add('CI D_gl(N,F0) (dec)', gap('CI', 'F0', 'N'), b['CI.RR_N.dec'] * 20100 / nc, 'CI.RR_N.dec * 20100 / CI.n_dec')
    return rows


def main():
    out = OUT / 'CHECK_FRONTIER_ADD4_v13.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    u = unchanged(); t = tie()
    verdict = 'OK' if all(x['ok'] for x in u.values()) and all(r['ok'] for r in t) else 'NOT OK'
    out.write_text(json.dumps(dict(schema='CHECK_FRONTIER_ADD4_V13', verdict=verdict, tolerance=TOL, unchanged=u, tie_to_recount=t), indent=1),
                   encoding='utf-8')
    for k, x in u.items():
        print(k, 'ok' if x['ok'] else 'NOT OK', '| values %d -> %d | changed %d | added %s | other fields differing %s | deviations %s | outcomes equal %s'
              % (x['old_values'], x['new_values'], len(x['changed_or_missing']), x['added'], x['other_fields_differing'], x['deviations'], x['outcomes_equal']))
    for r in t: print('%-34s %.17g  %.17g  diff %.2e %s' % (r['check'], r['from_curves'], r['from_recount'], r['abs_diff'], 'ok' if r['ok'] else 'FAIL'))
    print('verdict', verdict, '->', out.name)


if __name__ == '__main__':
    main()
