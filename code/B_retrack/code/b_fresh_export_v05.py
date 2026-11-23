r"""v05 (22 Nov 2026, Claude Opus 5.5; AMENDMENT_12 s3c): b_fresh_export_v04.py plus IMM2, the two-noise IMM: B.IMM2C.* from
out\fresh\B_FRESH_IMM2_v04.json (the 105 C runs, secondary) and B.IMM2N.* from out\new\B_NEW_IMM2_v04.json (the new runs, primary),
each added only when its file exists, with the same suffixes as B.IMM.* plus p_one_sided and p_n_finite (A12 s3c, from the analysis
file's p_one_sided_RR_N). Before writing, every existing key must be unchanged and the only new keys are B.IMM2C.* / B.IMM2N.*
(else REFUSED); the previous export is kept as A_EXPORT_B_v04_<n>keys.json.
Text of b_fresh_export_v04.py follows.
v04 (21 Nov 2026; AMENDMENT_11 section 6): b_fresh_export_v03.py plus the B.IMMr.* keys (B1R, the re-tuned IMM) from
out\fresh\B_FRESH_B1R_v03.json, printed beside the unchanged B.IMM.* keys. Before writing, every existing key of out\A_EXPORT_B.json
must be unchanged and the only new keys are B.IMMr.* (else REFUSED); the previous export is kept as A_EXPORT_B_v03_222keys.json.
Text of b_fresh_export_v03.py follows.
v13 package B: export v03 = b_fresh_export_v02.py plus TU.RR_TG and TU.RR_TG.ci from out\tu\TU_v03.json (coordinator
request 21 Nov ~02:25 EST). New file, 21 Nov 2026 (Claude Opus 5.5); v02 kept unchanged. Before writing, every key of the current
out\A_EXPORT_B.json must be present with an identical value; the only new keys are TU.RR_TG and TU.RR_TG.ci (else REFUSED). The
previous export is kept as out\A_EXPORT_B_v02_220keys.json. Text of b_fresh_export_v02.py follows.
v13 package B: flat export of the fresh-run tracker-variant values under A's key names (B_FRESH_DEFINITIONS_v02.md section 5).
New file, 20 Nov 2026 (Claude Opus 5.5). Reads only out\\fresh\\B_FRESH_<x>_v02.json (b_fresh_analysis_v02.py); no number typed.
Writes out\\A_EXPORT_B.json ({key: value}; intervals as [lo, hi]) and out\\A_EXPORT_B_meta.json (sources, SHA-256, gate, status).
--test-old: reads out\\fresh_testold\\ and writes out\\fresh_testold\\TESTOLD_A_EXPORT_B.json (+ _meta).
Usage: python -I -B -X utf8 b_fresh_export_v02.py [--test-old]
"""
import sys, json, pathlib, time, hashlib
HERE = pathlib.Path(__file__).resolve().parents[1]
OUT = HERE / 'out'
VARS = [('CV0', 'CV'), ('B3', 'CV2'), ('B4', 'CA'), ('B1', 'IMM'), ('B2', 'AQ'), ('B1_d090', 'IMM090'), ('B1_d098', 'IMM098'), ('B1R', 'IMMr')]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def flat(d, name):
    I = d['intervals']['all']; P = d['points']; r = d['ratio_N_F0']; p = 'B.%s.' % name
    out = {}
    def put(k, s):                                   # noqa: E306
        out[p + k] = s['point']; out[p + k + '.ci'] = list(s['ci'])
    put('R', I['R_pp']); out[p + 'R.dec'] = P['all']['R_deceq']
    put('RR', I['RR_N']); put('c', I['RR_E5x']); put('RR_minus_c', I['RR_N_minus_E5x']); put('RR_CK3', I['RR_CK3'])
    out.update({p + 'm': r['median'], p + 'A': r['A'], p + 'q05': r['q05'], p + 'q95': r['q95'], p + 'within5': r['share_within_5pct'],
                p + 'barely': bool(r['barely_varies']), p + 'class': d['classification']['classification'],
                p + 'room_pre': P['est_before']['R_pp'], p + 'room_brk': P['est_braking']['R_pp'], p + 'room_stop': P['est_stopped']['R_pp'],
                p + 'as_room': P['tru_stopped']['R_deceq'], p + 'as_room.pp': P['tru_stopped']['R_pp'],
                p + 'lag': d['lag_dx3_first_second_after_stop']['median'], p + 'n_dec': d['n_dec'], p + 'n_runs': d['n_runs']})
    return out


def main():
    test = '--test-old' in sys.argv
    src = OUT / ('fresh_testold' if test else 'fresh')
    E = {}; meta = dict(code='b_fresh_export_v05.py', written=time.strftime('%Y-%m-%d %H:%M:%S'), sources={},
                        definitions='B_retrack/B_FRESH_DEFINITIONS_v02.md')
    docs = {}
    for v, name in VARS:
        p = src / ('B_FRESH_%s_%s.json' % (v, 'v03' if v == 'B1R' else 'v02'))
        if not p.exists():
            raise SystemExit('REFUSED: %s missing' % p)
        d = json.loads(p.read_text(encoding='utf-8')); docs[name] = d
        E.update(flat(d, name)); meta['sources'][name] = dict(file=str(p.relative_to(HERE)), sha256=sha(p), gate=d['gate'],
                                                              status=d['status'], nboot=d['nboot'], draw=d['draw'])
    for x in ('CV2', 'CA'):                         # A10 section 3, B3 row: the rule, applied descriptively (definitions section 5)
        E['B.rule.%s' % x] = dict(as_room_below_half=bool(E['B.%s.as_room' % x] < 0.5 * E['B.CV.as_room']),
                                  ck3_differs=bool(abs(E['B.%s.RR_CK3' % x] - E['B.CV.RR_CK3']) > 0.10))
    E['B.rule.outcome'] = ('depends on filter tuning' if any(v for x in ('CV2', 'CA') for v in E['B.rule.%s' % x].values())
                           else 'mechanism persists')
    # B6 and the stop reliance (B_FRESH_DEFINITIONS_v02.md section 6b), online tracker of record
    p6 = (src / 'B6_TESTOLD_v02.json') if test else (OUT / 'fresh_b6' / 'B6_FRESH_v02.json')
    if not p6.exists():
        raise SystemExit('REFUSED: %s missing' % p6)
    d6 = json.loads(p6.read_text(encoding='utf-8'))
    meta['sources']['B6'] = dict(file=str(p6.relative_to(HERE)), sha256=sha(p6), gate=d6['gate'], status=d6['status'], nboot=d6['nboot'], draw=d6['draw'])
    E['LB.RS075.rel'] = d6['RS075_rel']['point']; E['LB.RS075.rel.ci'] = list(d6['RS075_rel']['ci'])
    for i, t in enumerate(d6['terciles'][1:], start=1):
        E['LB.T%d.rel' % i] = t['room_ratio_WR_over_3s']; E['LB.T%d.den0.dec' % i] = t['W_R']['den0_deceq']
        E['LB.T%d.evaluable' % i] = bool(t['W_R']['evaluable_den0'])
        E['LB.T%d.range' % i] = ('%.2f–%.2f' % tuple(t['decel_min_max'])) if t['decel_min_max'] else None
    rr = d6['tercile_rel_range']
    if rr['relmin'] is not None:
        E['LB.T.relmin'] = rr['relmin']; E['LB.T.relmax'] = rr['relmax']
    E['LB.DS.rel'] = d6['DS_rel']['point']; E['LB.DS.rel.ci'] = list(d6['DS_rel']['ci']); E['LB.DS.den0.dec'] = d6['delayed_stop']['den0_deceq']
    for a in ('F0', 'N', 'CK3'):
        E['LB.REL_%s' % a] = d6['reliance']['all'][a]['share_safe_only_with_stop']
    # TU: the 20 lead-braking tuning runs (section 6c; old data, identical in test and fresh mode)
    pt = OUT / 'tu' / 'TU_v03.json'
    if not pt.exists():
        raise SystemExit('REFUSED: %s missing' % pt)
    dt = json.loads(pt.read_text(encoding='utf-8'))
    meta['sources']['TU'] = dict(file=str(pt.relative_to(HERE)), sha256=sha(pt), status=dt['status'], nboot=dt['nboot'], draw=dt['draw'])
    I = dt['intervals']['all']
    E['TU.R'] = I['R_pp']['point']; E['TU.R.ci'] = list(I['R_pp']['ci'])
    for a in ('N', 'NA', 'AM', 'CK3', 'TG'):
        E['TU.RR_%s' % a] = I['RR_' + a]['point']; E['TU.RR_%s.ci' % a] = list(I['RR_' + a]['ci'])
    for k, pn in (('R_pre', 'est_before'), ('R_brk', 'est_braking'), ('R_stop', 'est_stopped')):
        E['TU.' + k] = dt['points'][pn]['R_pp']
    for sub, fn, name in (('fresh', 'B_FRESH_IMM2_v04.json', 'IMM2C'), ('new', 'B_NEW_IMM2_v04.json', 'IMM2N')):
        p2 = OUT / sub / fn
        if test or not p2.exists():
            continue
        d2 = json.loads(p2.read_text(encoding='utf-8'))
        E.update(flat(d2, name))
        E['B.%s.p_one_sided' % name] = d2['p_one_sided_RR_N']['p']; E['B.%s.p_n_finite' % name] = d2['p_one_sided_RR_N']['n_valid']
        meta['sources'][name] = dict(file=str(p2.relative_to(HERE)), sha256=sha(p2), gate=d2['gate'], status=d2['status'],
                                     nboot=d2['nboot'], draw=d2['draw'], run_set=d2['run_set'])
    gates = {m['gate'] for m in meta['sources'].values() if 'gate' in m}
    meta['gate'] = sorted(gates); meta['status'] = sorted({m['status'] for m in meta['sources'].values()}); meta['n_keys'] = len(E)
    o = (src / 'TESTOLD_A_EXPORT_B.json') if test else (OUT / 'A_EXPORT_B.json')
    if o.exists():                                   # v03: the existing keys must not change
        cur = json.loads(o.read_text(encoding='utf-8'))
        new_keys = sorted(set(E) - set(cur)); gone = sorted(set(cur) - set(E))
        changed = [k for k in cur if k in E and json.dumps(cur[k], default=float) != json.dumps(E[k], default=float)]
        if gone or changed or not all(k.startswith(('B.IMM2C.', 'B.IMM2N.')) for k in new_keys):
            raise SystemExit('REFUSED: existing export would change: gone %s, changed %s, new %s' % (gone, changed[:5], new_keys))
        keep = o.with_name(o.stem + '_v04_%dkeys.json' % len(cur))
        if not keep.exists():
            keep.write_text(o.read_text(encoding='utf-8'), encoding='utf-8')
        meta['v05_check'] = dict(previous_keys=len(cur), unchanged=len(cur), new_keys=new_keys, previous_kept_as=keep.name,
                                 previous_sha256=sha(keep))
        print('v05 check: %d existing keys unchanged; %d new keys %s' % (len(cur), len(new_keys), new_keys[:4]))
    o.write_text(json.dumps(E, indent=1, default=float), encoding='utf-8')
    o.with_name(o.stem + '_meta.json').write_text(json.dumps(meta, indent=1), encoding='utf-8')
    print('wrote', o, len(E), 'keys; rule outcome:', E['B.rule.outcome'], flush=True)


if __name__ == '__main__':
    main()
