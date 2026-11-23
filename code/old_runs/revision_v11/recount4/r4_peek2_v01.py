"""Recount4 helper (after the own results were written): leaf paths of the first program's file, per scoring family."""
import json, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent
F = HERE.parent / 'analysis' / 'out' / 'REV_E2_EXTENDED_TRUTH_v01.json'
d = json.loads(F.read_text(encoding='utf-8'))


def leaves(o, pre=()):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, pre + (str(k),))
    elif isinstance(o, list):
        if all(not isinstance(x, (dict, list)) for x in o):
            yield pre, o
        else:
            for i, v in enumerate(o):
                yield from leaves(v, pre + ('[%d]' % i,))
    else:
        yield pre, o


for name, sc in d['scorings'].items():
    print('==', name, 'keys', list(sc.keys()), 'pops', list(sc['pops'].keys()))
    extra = {k: v for k, v in sc.items() if k != 'pops'}
    if extra:
        print('   non-pop entries:', json.dumps(extra)[:600])
    shapes = collections.OrderedDict()
    for pn, pe in sc['pops'].items():
        paths = tuple('.'.join(p) for p, _ in leaves(pe))
        shapes.setdefault(paths, []).append(pn)
    for paths, pns in shapes.items():
        print('   pops', pns, 'leaves', len(paths))
        # collapse the arms
        coll = []
        for p in paths:
            q = p
            for a in ('N', 'NA', 'CK3', 'A1', 'Q'):
                q = q.replace('arms.%s.' % a, 'arms.*.')
            if q not in coll:
                coll.append(q)
        print('     ', coll)
print('pair_counts', json.dumps(d['pair_counts']['t0p75_a6p0'], indent=1))
print({k: v for k, v in d.items() if k not in ('scorings', 'pair_counts')})
