"""A11 Bonferroni check (rule: BONFERRONI_A11_RULE_v13.md, written first). Reads existing exports only; writes BONFERRONI_A11_v13.json (never
overwritten). New file, 22 Nov 2026 (Claude Opus 5.5, session CD). Usage: python -I -B bonferroni_a11_v13.py"""
import hashlib, json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent; W = HERE.parents[1]
SRC = dict(X=W / 'CD_capture' / 'out' / 'A_EXPORT_X.json', Y=W / 'CD_capture' / 'out' / 'A_EXPORT_Y.json', DR=W / 'F_dropout' / 'out' / 'DR_RESULTS_v01.json')
Z = lambda L: {0.95: 1.959963984540054, 0.99: 2.5758293035489004}[round(L, 4)]
PHI = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))


def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def step(name, t, ci, L, t0, aB):
    lo = ci[0]
    if L >= 1 - 2 * aB:
        return dict(step=name, point=t, ci=ci, level=L, null=t0, method='direct (level >= 1 - 2 alpha_B)', survives=bool(lo > t0))
    se = (t - lo) / Z(L); z = (t - t0) / se; p = 1 - PHI(z)
    return dict(step=name, point=t, ci=ci, level=L, null=t0, method='normal approximation on the lower side', se_low=se, z=z, p_approx=p,
                survives=bool(p <= aB))


def main():
    out = HERE / 'BONFERRONI_A11_v13.json'
    if out.exists(): raise SystemExit('REFUSED: exists')
    X = json.loads(SRC['X'].read_text(encoding='utf-8'))['values']; Y = json.loads(SRC['Y'].read_text(encoding='utf-8'))['values']
    D = json.loads(SRC['DR'].read_text(encoding='utf-8')); D = D.get('values', D)
    res = {}
    for m in (4, 3):
        aB = 0.025 / m; s = {}
        s['X0'] = [step('X0 R_gl > 0', X['X.PC.R'], X['X.PC.R.ci'], X['X.PC.R.level'], 0., aB),
                   dict(step='X0 share D>0', share=X['X.PC.R.pos_share'], need=1 - aB, survives=bool(X['X.PC.R.pos_share'] >= 1 - aB))]
        s['X1'] = [step('X1 RR_E5N > 0', X['X.PC.RR_E5N'], X['X.PC.RR_E5N.ci'], X['X.PC.RR_E5N.level'], 0., aB),
                   step('X1 RR_E5N - RR_E5pN > 0', X['X.PC.RR_E5NmP'], X['X.PC.RR_E5NmP.ci'], X['X.PC.RR_E5NmP.level'], 0., aB)]
        s['X2'] = [dict(step='X2 r = RR_N not above 0 (a wider interval keeps it)', point=X['X.PC.RR_N'], ci=X['X.PC.RR_N.ci'],
                        survives=bool(X['X.PC.RR_N.ci'][0] <= 0)),
                   step('X2 c = RR_E5N > delta', X['X.PC.RR_E5N'], X['X.PC.RR_E5N.ci'], X['X.PC.RR_E5N.level'], 0.05, aB)]
        s['Y1'] = [step('Y1 Delta > 0', Y['Y.delta'], Y['Y.delta.ci'], Y['Y.delta.level'], 0., aB)]
        s['DR0'] = [step('DR0 R_gl > 0', D['DR.R_gl'], D['DR.R_gl.ci'], D['DR.R_gl.level'], 0., aB),
                    dict(step='DR0 share D>0', share=D['DR.R_gl.share_pos'], need=1 - aB, survives=bool(D['DR.R_gl.share_pos'] >= 1 - aB))]
        s['DR1'] = [step('DR1 c_DR > 0', D['DR.c'], D['DR.c.ci'], D['DR.c.level'], 0., aB),
                    step('DR1 c_DR - c_DRp > 0', D['DR.cdiff'], D['DR.cdiff.ci'], D['DR.cdiff.level'], 0., aB)]
        s['DR2'] = [step('DR2 recovers: r_DR > 0', D['DR.r'], D['DR.r.ci'], D['DR.r.level'], 0., aB)]
        if not s['DR2'][0]['survives']:
            s['DR2'].append(step('DR2 re-read: c_DR > delta (uninformative variation)', D['DR.c'], D['DR.c.ci'], D['DR.c.level'], 0.05, aB))
        seq = {'X': all(r['survives'] for k in ('X0', 'X1', 'X2') for r in s[k]), 'Y': all(r['survives'] for r in s['Y1']),
               'DR': all(r['survives'] for k in ('DR0', 'DR1') for r in s[k]) and (s['DR2'][0]['survives'] or s['DR2'][-1]['survives'])}
        dr2 = 'recovers' if s['DR2'][0]['survives'] else ('uninformative variation' if s['DR2'][-1]['survives'] else 'not surviving')
        res['m%d' % m] = dict(alpha_B=aB, steps=s, sequences_survive=seq, DR2_class_under_bonferroni=dr2)
    doc = dict(rule='BONFERRONI_A11_RULE_v13.md (sha256 %s), written before this computation' % sha(HERE / 'BONFERRONI_A11_RULE_v13.md'),
               program_sha256=sha(__file__), inputs={str(p): sha(p) for p in SRC.values()}, results=res)
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    for m in ('m4', 'm3'):
        r = res[m]; print(m, 'alpha_B', r['alpha_B'], r['sequences_survive'], 'DR2:', r['DR2_class_under_bonferroni'])
        for k, v in r['steps'].items():
            for x in v: print('  ', x['step'], '| survives', x['survives'], '| p≈%.2g' % x['p_approx'] if 'p_approx' in x else '')


if __name__ == '__main__':
    main()
