"""Export for session A: the exploratory crossing heading decomposition (prefix XH.; Supplement S15; coordinator 22 Nov 2026 about 03:05 EST).
Clerical mapping of the two programs' outputs (no value computed):
first : crossing/out/X_HEADING_v13.json      -> out/A_EXPORT_XH.json
second: recount/out/RC_X_HEADING_v13.json    -> out/A_RECOUNT_XH.json
Keys (both files the same set):
  XH.status ('exploratory'), XH.n_runs, XH.n_ticks, XH.y_bind.median, XH.y_bind.q25, XH.y_bind.q75;
  for B in (bind = the margin ratio at the binding constraint, dec = at the decision, row idx55):
    XH.<B>.r2, XH.<B>.r2.ci, XH.<B>.share.<g>, XH.<B>.shapley.<g>, XH.<B>.shapley.<g>.ci, XH.<B>.r2_single.<g> for g in geometry/schedule/error,
    XH.<B>.rho.<x> for x in cos_phi2, te, miss, ln1p_age_upd, abs_e_n; XH.dec.n_ticks;
  XH.frame.aligned10, XH.frame.across10, XH.frame.abs_sin.median, XH.frame.axis_ratio.median, XH.frame.axis_ratio.iqr.
New file, 22 Nov 2026 (Claude Opus 5.5, session CD). Usage: python -I -B make_export_xh_v13.py first|second
"""
import datetime, hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
G = ('geometry', 'schedule', 'error')
NM = {'cos_phi2': 'cos_phi^2', 'te': 'te', 'miss': 'miss', 'ln1p_age_upd': 'ln(1+age_upd)', 'abs_e_n': '|e_n|'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def first(a):
    o = {'XH.n_runs': a['decomposition_y_bind']['n_runs'], 'XH.n_ticks': a['ticks']['analysed'], 'XH.y_bind.median': a['y_bind']['median'],
         'XH.y_bind.q25': a['y_bind']['iqr'][0], 'XH.y_bind.q75': a['y_bind']['iqr'][1]}
    for b, dk, sp in (('bind', 'decomposition_y_bind', 'spearman_y_bind'), ('dec', 'decomposition_y_dec', 'spearman_y_dec')):
        d = a[dk]; o['XH.%s.r2' % b] = d['r2_full']; o['XH.%s.r2.ci' % b] = d['r2_full_ci95']
        for g in G:
            o['XH.%s.share.%s' % (b, g)] = d['shapley_share_of_r2'][g]; o['XH.%s.shapley.%s' % (b, g)] = d['shapley_r2'][g]
            o['XH.%s.shapley.%s.ci' % (b, g)] = d['shapley_r2_ci95'][g]; o['XH.%s.r2_single.%s' % (b, g)] = d['r2_single_group'][g]
        for x in NM: o['XH.%s.rho.%s' % (b, x)] = a[sp][x]
    o['XH.dec.n_ticks'] = a['decomposition_y_dec']['n_ticks']
    f = a['object_frame_check']
    o.update({'XH.frame.aligned10': f['share_aligned_within_10deg'], 'XH.frame.across10': f['share_across_within_10deg'],
              'XH.frame.abs_sin.median': f['abs_sin_major_vs_heading']['median'], 'XH.frame.axis_ratio.median': f['axis_ratio']['median'],
              'XH.frame.axis_ratio.iqr': f['axis_ratio']['iqr']})
    return o


def second(b):
    p = b['part1']; c = p['counts']
    o = {'XH.n_runs': p['y_bind']['n_runs'], 'XH.n_ticks': c['ticks_analysed'], 'XH.y_bind.median': c['y_bind']['median'],
         'XH.y_bind.q25': c['y_bind']['q25'], 'XH.y_bind.q75': c['y_bind']['q75']}
    for k, key in (('bind', 'y_bind'), ('dec', 'y_dec')):
        d = p[key]; o['XH.%s.r2' % k] = d['r2_full']; o['XH.%s.r2.ci' % k] = d['r2_full_ci95']
        for g in G:
            o['XH.%s.share.%s' % (k, g)] = d['shapley_share_of_r2'][g]; o['XH.%s.shapley.%s' % (k, g)] = d['shapley_r2'][g]
            o['XH.%s.shapley.%s.ci' % (k, g)] = d['shapley_r2_ci95'][g]; o['XH.%s.r2_single.%s' % (k, g)] = d['r2_single_group'][g]
        for x, m in NM.items(): o['XH.%s.rho.%s' % (k, x)] = d['spearman_rho'][m]
    o['XH.dec.n_ticks'] = p['y_dec']['n_ticks']
    f = p['object_frame']
    o.update({'XH.frame.aligned10': f['abs_sin_angle']['share_aligned_lt_sin10'], 'XH.frame.across10': f['abs_sin_angle']['share_across_gt_cos10'],
              'XH.frame.abs_sin.median': f['abs_sin_angle']['median'], 'XH.frame.axis_ratio.median': f['axis_ratio']['median'],
              'XH.frame.axis_ratio.iqr': [f['axis_ratio']['p25'], f['axis_ratio']['p75']]})
    return o


def main():
    who = sys.argv[1]
    src = HERE / 'out' / 'X_HEADING_v13.json' if who == 'first' else CD / 'recount' / 'out' / 'RC_X_HEADING_v13.json'
    vals = (first if who == 'first' else second)(json.loads(src.read_text(encoding='utf-8')))
    vals = dict({'XH.status': 'exploratory'}, **vals)
    name = 'A_EXPORT_XH.json' if who == 'first' else 'A_RECOUNT_XH.json'
    dst = CD / 'out' / name
    if dst.exists(): raise SystemExit('REFUSED: %s exists' % name)
    doc = dict(package='XH (exploratory crossing heading decomposition; A12 task 4; Supplement S15)', written=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               program='make_export_xh_v13.py (%s)' % who, program_sha256=sha(__file__), values=vals, inputs={str(src): sha(src)})
    dst.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(name, len(vals), 'values', sha(dst))


if __name__ == '__main__':
    main()
