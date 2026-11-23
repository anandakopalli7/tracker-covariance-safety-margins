"""Recount4 helper (after the comparison): diagnostics of the own results file and of the comparison records.
Reads only this folder. Prints; writes r4_diag_v01_out.json."""
import json, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent
M = json.loads((HERE / 'RECOUNT4_RESULTS_v01.json').read_text(encoding='utf-8'))
C = json.loads((HERE / 'RECOUNT4_COMPARE_v01.json').read_text(encoding='utf-8'))
out = {}

# 1. resamples with a non-finite sum, undefined frontier levels, ratio points whose full-sample denominator is not positive
nf = []; und = []; masked = []; zero_den = []
for name, sc in M['scorings'].items():
    for pn, e in sc['pops'].items():
        for q in ('den0', 'denE'):
            if e['n_%s_not_finite' % q]:
                nf.append((name, pn, q, e['n_%s_not_finite' % q]))
        if e.get('resamples_with_undefined_frontier') or e.get('undefined_frontier_levels_point'):
            und.append((name, pn, e.get('undefined_frontier_levels_point'), e.get('resamples_with_undefined_frontier')))

        def chk(tag, r):
            if not r['point_denominator_positive']:
                (masked if r['point'] is not None else zero_den).append((name, pn, tag, r['point']))
        chk('RR0_E', e['RR0_E'])
        for a, s in e['src'].items():
            chk('RR0_' + a, s['RR0']); chk('RR_' + a, s['RR'])
        for rn, r in e['rel'].items():
            chk('rel.%s.denE' % rn, r['denE']); chk('rel.%s.den0' % rn, r['den0'])
print('resamples with a non-finite den0 or denE:', nf)
print('undefined frontier levels (point, resamples):', und)
print('ratio points with a full-sample denominator not positive: a number stored %d, undefined %d' % (len(masked), len(zero_den)))
for m in masked:
    print('   stored number although the denominator is not positive:', m)
by = collections.Counter((n, p) for n, p, _, _ in zero_den)
print('   undefined points by scoring and population:', dict(by))
out['non_finite'] = nf; out['undefined_frontier'] = und; out['masked_points'] = masked
out['undefined_points_by_scoring_pop'] = {'%s|%s' % k: v for k, v in by.items()}

# 2. comparison records: where "undefined in both" sits; a sample of records; the largest differences
ub = collections.Counter((r['scoring'], r['pop']) for r in C['records'] if r['status'] == 'undefined in both')
print('undefined in both, by scoring and population:', dict(ub))
out['undefined_in_both'] = {'%s|%s' % k: v for k, v in ub.items()}
big = sorted([r for r in C['records'] if r['abs_diff']], key=lambda r: -r['abs_diff'])[:8]
for r in big:
    print('   largest:', r['scoring'], r['pop'], r['entry'], r['first'], r['second'], r['abs_diff'])
nz = sum(1 for r in C['records'] if r['kind'] == 'number' and r['status'] == 'equal' and r['first'] == 0 and r['second'] == 0)
print('numbers equal because both are exactly 0:', nz, 'of', sum(1 for r in C['records'] if r['kind'] == 'number'))
out['both_exactly_zero'] = nz
exact = sum(1 for r in C['records'] if r['kind'] == 'number' and r['abs_diff'] == 0)
print('numbers bit-identical (difference exactly 0):', exact)
out['bit_identical'] = exact
kinds = collections.Counter(r['entry'].split('.')[-1].split('[')[0] for r in C['records'])
print('entries by last name:', dict(kinds))
out['entries_by_last_name'] = dict(kinds)
br = collections.Counter((r['first'], r['second']) for r in C['records'] if r['entry'].endswith('.branch'))
print('branch numbers (first, second):', dict(br))
out['branch'] = {'%s|%s' % k: v for k, v in br.items()}
(HERE / 'r4_diag_v01_out.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
