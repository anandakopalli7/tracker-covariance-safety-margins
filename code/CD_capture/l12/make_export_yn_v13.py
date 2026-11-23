"""Export for session A: Y on the L12 runs (A12 sec. 3b), prefix YN. (Y on the New runs; as B's B.IMM2N.*). Clerical mapping of the frozen
programs' final outputs: every key Y.<k> of the program's `values` becomes YN.<k>; YN.status = 'ran' and YN.n_runs are added. No value is
computed here except the p counts (p * #finite, integer-checked; add12). Pattern of crossing/make_export_xy_v13.py (add6). New file, 22 Nov 2026 (Claude Opus 5.5, session CD).
first : ycheck/out/Y_TWIN_L12_v13.json     -> out/A_EXPORT_YN.json
second: recount/out/RC_Y_TWIN_L12_v13.json -> out/A_RECOUNT_YN.json
Usage: python -I -B make_export_yn_v13.py first|second [--in PATH]
"""
import datetime, hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; V13 = CD.parents[1]
PREFIX = 'YN.'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    who = sys.argv[1]; a = sys.argv[2:]
    default = CD / 'ycheck' / 'out' / 'Y_TWIN_L12_v13.json' if who == 'first' else CD / 'recount' / 'out' / 'RC_Y_TWIN_L12_v13.json'
    src = pathlib.Path(a[a.index('--in') + 1]) if '--in' in a else default
    d = json.loads(src.read_text(encoding='utf-8')); v = d['values']
    if any('PENDING' in str(k) for k in d) or 'PENDING' in src.name: raise SystemExit('REFUSED: a PENDING output')
    out = {PREFIX + 'status': 'ran', PREFIX + 'n_runs': len(d.get('runs') or d.get('run_ids') or []) or None}
    for k, x in sorted(v.items()):
        if not k.startswith('Y.'): raise SystemExit('unexpected key %s' % k)
        out[PREFIX + k[2:]] = x
    # counts behind YN.p_one_sided (coordinator 22 Nov about 03:00 EST, for one Holm convention): #finite from each program's own output;
    # #{Delta_b <= 0} = p * #finite, which must be an integer (add12)
    import re
    if who == 'first':
        nf = int(re.search(r'(\d+) run resamples', d['draw']).group(1)) - int(d['B2']['delta_main']['n_invalid'])
    else:
        nf = int(d['resamples']['delta']['n_finite'])
    p = v['Y.p_one_sided']; c = p * nf
    if abs(c - round(c)) > 1e-6: raise SystemExit('p_one_sided * n_finite is not an integer: %r' % c)
    out[PREFIX + 'p_count_le0'] = int(round(c)); out[PREFIX + 'p_count_finite'] = nf
    name = 'A_EXPORT_YN.json' if who == 'first' else 'A_RECOUNT_YN.json'
    dst = CD / 'out' / name
    if dst.exists(): raise SystemExit('REFUSED: %s exists' % name)
    doc = dict(package='YN (A12 sec. 3b, Y on the L12 runs)', written=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               program='make_export_yn_v13.py (%s)' % who, program_sha256=sha(__file__), lock_sha256=sha(V13 / 'LOCK_A12a.txt'),
               values=out, inputs={str(src): sha(src)})
    dst.write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')
    print(name, len(out), 'values', sha(dst))


if __name__ == '__main__':
    main()
