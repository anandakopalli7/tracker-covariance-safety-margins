"""Recount4 helper: print the own results (RECOUNT4_RESULTS_v01.json) as tables. Reads only this folder."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
res = json.loads((HERE / 'RECOUNT4_RESULTS_v01.json').read_text(encoding='utf-8'))
S = res['scorings']
POPS = ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted')


def f(x, d=4):
    return 'n/a' if x is None else ('%.' + str(d) + 'f') % x


def pc(e, d=4):
    if e['ci'] is None:
        return '%s [n/a]' % f(e['point'], d)
    return '%s [%s, %s]' % (f(e['point'], d), f(e['ci'][0], d), f(e['ci'][1], d))


names = sys.argv[1:] or list(S)
for name in names:
    sc = S[name]
    print('=' * 20, name, 'refs', sc['reference_scorings'])
    for pn in POPS:
        e = sc['pops'][pn]
        print(' %-15s n %6d  den0 pp %s  deceq %s  | denE pp %s deceq %s | share den0<=0 %.5f denE<=0 %.5f' % (
            pn, e['n'], pc(e['den0']['pp']), pc(e['den0']['deceq'], 2), pc(e['denE']['pp']), pc(e['denE']['deceq'], 2),
            e['share_den0_le0'], e['share_denE_le0']))
        for rn, r in e['rel'].items():
            print('     rel %-24s denE %s (left out %d)  den0 %s (left out %d)' % (rn, pc(r['denE']), r['denE']['n_left_out'], pc(r['den0']), r['den0']['n_left_out']))
        for a, s in e['src'].items():
            print('     %-4s D pp %s deceq %s RR0 %s (out %d) RR %s (out %d)' % (a, pc(s['D_pp']), pc(s['D_deceq'], 2), pc(s['RR0']), s['RR0']['n_left_out'],
                                                                              pc(s['RR']), s['RR']['n_left_out']))
        print('     RR0_E %s (out %d)' % (pc(e['RR0_E']), e['RR0_E']['n_left_out']))
print('counts')
for k, c in res['counts'].items():
    print(' ', k, c)
