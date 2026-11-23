"""Combine parts/*.json into RECOUNT_B_v01.json and print the summary table."""
import json, os, time
from rc_core import OUT, VARIANTS, RUNS, have_variant

P = OUT + r'\parts'


def ld(n):
    p = r'%s\%s.json' % (P, n)
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    out = dict(written=time.strftime('%Y-%m-%d %H:%M:%S'), program='independent second program, package B (recount)',
               variants_present={x: have_variant(x) for x in VARIANTS}, per_variant={}, summary={})
    for x in VARIANTS:
        d = ld(x)
        if d is not None:
            out['per_variant'][x] = d
    out['B6'] = ld('b6'); out['B9'] = ld('b9')
    cv = out['per_variant'].get('CV0')
    rows = []
    for x, d in out['per_variant'].items():
        row = dict(variant=x, room_pp=d['room_pp'], room_deceq=d['room_deceq'], RR_gl_N=d['all']['RR_N'], RR_N_ci=d['intervals']['RR_N']['ci'],
                   c_x=d['ceiling_c'], c_ci=d['intervals']['RR_E5x']['ci'], m_x=d['margin_ratio']['median'], A_x=d['margin_ratio']['A'],
                   after_stop_room_deceq=d['after_stop_room_deceq'], lag_median=d['lag']['median_dx_pred3'], RR_CK3=d['all']['RR_CK3'],
                   RR_E5=d['all']['RR_E5'], RR_E5p=d['all']['RR_E5p'], H3=d['H3']['cls'], grid_RR_N=d['grid']['RR_N'])
        if cv is not None and x in ('B3', 'B4'):
            half = d['after_stop_room_deceq'] < 0.5 * cv['after_stop_room_deceq']
            dd = abs(d['all']['RR_CK3'] - cv['all']['RR_CK3']) > 0.10
            row['B3B4_rule'] = 'depends on filter tuning' if (half or dd) else 'persists with NIS near 2 and with a CA filter'
            row['B3B4_rule_parts'] = dict(after_stop_below_half=bool(half), RR_CK3_diff_gt_0p10=bool(dd), RR_CK3_diff=d['all']['RR_CK3'] - cv['all']['RR_CK3'])
        rows.append(row)
    out['summary']['table'] = rows
    json.dump(out, open(OUT + r'\RECOUNT_B_v01.json', 'w'), indent=1, default=float)
    for r in rows:
        print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items() if k not in ('RR_N_ci', 'c_ci', 'B3B4_rule_parts')})


if __name__ == '__main__':
    main()
