"""Exports for session A (work\\A_text\\notes\\RESULTS_INTERFACE_SPRINT_v13.md): X (pedestrian crossing, prefix X.PC.) and Y. Clerical
mapping of the frozen programs' final outputs; no value is computed here except RR_N.dec = RR_N * R.dec for the second program (exact
algebra: D_gl(N) = RR_N * D_gl(E), dec_eq is linear). New file, 21 Nov 2026 (Claude Opus 5.5, session CD).
first : crossing\\out\\X_CROSS_pedestrian_crossing_v13.json + crossing\\out\\X_DESC_pedestrian_crossing_v13.json -> out\\A_EXPORT_X.json;
        ycheck\\out\\Y_TWIN_v13.json -> out\\A_EXPORT_Y.json
second: recount\\out\\RC_X_CROSS_pedestrian_crossing_v13.json + recount\\out\\RC_X_DESC_pedestrian_crossing_v13.json -> out\\A_RECOUNT_X.json;
        recount\\out\\RC_Y_TWIN_v13.json -> out\\A_RECOUNT_Y.json
A's keys first (status, n_runs, n_dec, R, R.ci, R.pos_share, R.dec, RR_E5N(.ci), RR_E5NmP(.ci), RR_N(.ci), RR_N.dec(.ci), within5, eff(.ci),
PO25/50/75; Y.status, Y.delta(.ci), Y.RR_B2p, Y.delta_s(.ci)), then every other flat value of the programs under the same prefix.
Usage: python -I -B make_export_xy_v13.py first|second [--x-in PATH --desc-in PATH --y-in PATH]   (inputs override the defaults)
"""
import datetime, hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; V13 = CD.parents[1]
ARGS = sys.argv[1:]; WHO = ARGS[0]
opt = lambda n, d: pathlib.Path(ARGS[ARGS.index(n) + 1]) if n in ARGS else d


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load(p):
    d = json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
    if d.get('pending_calibration') or 'PENDING' in pathlib.Path(p).name: raise SystemExit('REFUSED: %s is a pending-calibration output' % p)
    return d


def x_values(xd, dd):
    v, dv = xd['values'], dd['values']; o = {}
    g = lambda k: v.get('X.ped.' + k)
    o['status'] = 'under_run' if g('under_run') else 'ran'
    for a, b in (('n_runs', 'n_runs'), ('n_dec', 'n_dec'), ('R', 'R'), ('R.ci', 'R.ci'), ('R.pos_share', 'R.share_pos'), ('R.dec', 'R.dec'),
                 ('RR_E5N', 'RR_E5N'), ('RR_E5N.ci', 'RR_E5N.ci'), ('RR_E5NmP', 'RR_E5NmP'), ('RR_E5NmP.ci', 'RR_E5NmP.ci'),
                 ('RR_N', 'RR_N'), ('RR_N.ci', 'RR_N.ci'), ('within5', 'ratio.within5'), ('eff', 'X2.eff'), ('eff.ci', 'X2.eff.ci')):
        o[a] = g(b)
    dq = (xd.get('D_deceq') or {}).get('N')
    o['RR_N.dec'] = dq['point'] if dq else (g('RR_N') * g('R.dec') if g('RR_N') is not None and g('R.dec') is not None else None)
    if dq: o['RR_N.dec.ci'] = dq.get('ci')
    for p in ('PO25', 'PO50', 'PO75'): o[p] = dv.get('X.ped.' + p)
    for k, x in sorted(v.items()):
        kk = k[len('X.ped.'):]
        if kk not in o: o[kk] = x
    for k, x in sorted(dv.items()):
        kk = k[len('X.ped.'):]
        if kk not in o: o[kk] = x
    return {'X.PC.' + k: x for k, x in o.items()}


def y_values(yd):
    v = yd['values']; o = {'Y.status': 'ran'}
    for k in ('Y.delta', 'Y.delta.ci', 'Y.RR_B2p', 'Y.delta_s', 'Y.delta_s.ci'): o[k] = v.get(k)
    for k, x in sorted(v.items()):
        if k not in o: o[k] = x
    return o


def write(name, pkg, values, inputs):
    doc = dict(package=pkg, written=datetime.datetime.now(datetime.timezone.utc).isoformat(), program='make_export_xy_v13.py (%s)' % WHO,
               program_sha256=sha(__file__), lock_sha256=sha(V13 / 'LOCK_A11.txt'), values=values, inputs={str(p): sha(p) for p in inputs})
    out = CD / 'out' / name
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    out.write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')
    print(name, len(values), 'values', sha(out))


def main():
    if WHO == 'first':
        xi = opt('--x-in', HERE / 'out' / 'X_CROSS_pedestrian_crossing_v13.json'); di = opt('--desc-in', HERE / 'out' / 'X_DESC_pedestrian_crossing_v13.json')
        yi = opt('--y-in', CD / 'ycheck' / 'out' / 'Y_TWIN_v13.json'); names = ('A_EXPORT_X.json', 'A_EXPORT_Y.json')
    else:
        xi = opt('--x-in', CD / 'recount' / 'out' / 'RC_X_CROSS_pedestrian_crossing_v13.json')
        di = opt('--desc-in', CD / 'recount' / 'out' / 'RC_X_DESC_pedestrian_crossing_v13.json')
        yi = opt('--y-in', CD / 'recount' / 'out' / 'RC_Y_TWIN_v13.json'); names = ('A_RECOUNT_X.json', 'A_RECOUNT_Y.json')
    if xi.is_file() and di.is_file(): write(names[0], 'X', x_values(load(xi), load(di)), [xi, di])
    else: print('X inputs missing:', [str(p) for p in (xi, di) if not p.is_file()])
    if yi.is_file(): write(names[1], 'Y', y_values(load(yi)), [yi])
    else: print('Y input missing:', yi)


if __name__ == '__main__':
    main()
