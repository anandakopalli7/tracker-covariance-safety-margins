"""Package F (revision v13): compares the first program's horizon rule (out\\F_HORIZON_RULE_v01.json, f06_score_v01.py horizon) with
the independent second program's (recount\\F_RECOUNT_HORIZON_v01.json, Claude Fable 5.2). New file, 19 Nov 2026 (Claude Opus 5.5).
Counts must be equal; points, interval ends and shares of non-positive resamples within 1e-9 (absolute); the rule's outcome equal.
Writes out\\F_HORIZON_COMPARE_v01.json (refuses to overwrite).
20 Nov 2026: an optional version argument (v02: the clearance departure) compares out\\F_HORIZON_RULE_v02.json with
recount\\F_RECOUNT_HORIZON_v02.json and writes out\\F_HORIZON_COMPARE_v02.json; for v02 it also compares the descriptive
removed-contact counts (out\\F_CLEAR_V02_train_v01.json against the recount's), which must be equal.
Usage: python -I f13_compare_horizon_v01.py [v01|v02]
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402

TOL = 1e-9


def main():
    ver = sys.argv[1] if len(sys.argv) > 1 else 'v01'
    outf = FC.OUT / ('F_HORIZON_COMPARE_%s.json' % ver)
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    a_path = FC.OUT / ('F_HORIZON_RULE_%s.json' % ver); b_path = FC.F / 'recount' / ('F_RECOUNT_HORIZON_%s.json' % ver)
    A = json.loads(a_path.read_text(encoding='utf-8')); B = json.loads(b_path.read_text(encoding='utf-8'))
    rows = []; ok = True
    for h in (3, 2):
        a = A['horizons']['%d s' % h]; b = B['horizons']['%ds' % h]
        pairs = [('n_scenes', a['n_scenes'], b['counts']['scenes'], 'count'),
                 ('n_evaluated', a['n_evaluated'], b['counts']['evaluated'], 'count'),
                 ('R_gl_pp.point', a['R_gl_pp']['point'], b['all']['R_gl_pp']['point'], 'value'),
                 ('R_gl_pp.ci.lower', a['R_gl_pp']['ci'][0], b['all']['R_gl_pp']['ci95'][0], 'value'),
                 ('R_gl_pp.ci.upper', a['R_gl_pp']['ci'][1], b['all']['R_gl_pp']['ci95'][1], 'value'),
                 ('D_gl_E_F0.point', a['D_gl_E_F0']['point'], b['all']['D_gl_E_F0'], 'value'),
                 ('share_resamples_nonpositive', a['share_resamples_nonpositive'], b['all']['R_gl_pp']['share_le0'], 'value')]
        for name, x, y, kind in pairs:
            agree = (x == y) if kind == 'count' else (abs(float(x) - float(y)) <= TOL)
            ok &= bool(agree)
            rows.append(dict(horizon_s=h, quantity=name, first=x, second=y, abs_diff=abs(float(x) - float(y)), agree=bool(agree)))
    if ver == 'v02':
        rm = json.loads((FC.OUT / 'F_CLEAR_V02_train_v01.json').read_text(encoding='utf-8'))['g1_counts']
        for h in (3, 2):
            mine = rm['%d s' % h]; theirs = B['horizons']['%ds' % h]['removed_contacts_g1']
            for src in ('F0', 'E'):
                pairs = [('removed', mine[src]['removed'], theirs[src]['removed']), ('added', mine[src]['added'], theirs[src]['added']),
                         ('wrong_go_v01', mine[src]['wrong_go_v01'], theirs[src]['selected_unsafe_old']),
                         ('wrong_go_v02', mine[src]['wrong_go_v02'], theirs[src]['selected_unsafe_new']),
                         ('rows_unsafe_to_safe', mine['rows_unsafe_to_safe'], theirs[src]['pairs_unsafe_to_safe']),
                         ('rows_safe_to_unsafe', mine['rows_safe_to_unsafe'], theirs[src]['pairs_safe_to_unsafe']),
                         ('n_evaluated', mine['n_evaluated'], theirs[src]['evaluated'])]
                for name, x, y in pairs:
                    agree = (x == y); ok &= bool(agree)
                    rows.append(dict(horizon_s=h, quantity='removed_contacts_g1.%s.%s' % (src, name), first=x, second=y,
                                     abs_diff=abs(float(x) - float(y)), agree=bool(agree)))
    b_primary = B['horizon_rule']['primary_horizon_s']
    same_outcome = (A['primary_horizon_s'] == b_primary)
    ok &= same_outcome
    doc = dict(code='f13_compare_horizon_v01.py', written=FC.clock(), tolerance_abs=TOL,
               first=dict(file=str(a_path.relative_to(FC.F)), sha256=FC.sha256_file(a_path), primary_horizon_s=A['primary_horizon_s']),
               second=dict(file=str(b_path.relative_to(FC.F)), sha256=FC.sha256_file(b_path), writer=B.get('writer'),
                           primary_horizon_s=b_primary),
               same_outcome=same_outcome, all_agree=bool(ok), rows=rows)
    outf.write_text(FC.jdump(doc), encoding='utf-8')
    print('WROTE', outf, 'all agree:', ok, '| outcome first', A['primary_horizon_s'], 'second', b_primary)
    for r in rows:
        print('  %d s %-30s %r  %r  %s' % (r['horizon_s'], r['quantity'], r['first'], r['second'], 'ok' if r['agree'] else 'DIFFER'))


if __name__ == '__main__':
    main()
