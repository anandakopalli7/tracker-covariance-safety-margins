"""Recount: print a results JSON compactly (leaves as path = value). Usage: python -B -X utf8 rc_show_v01.py file.json [substring]"""
import json, sys


def flat(o, pre=''):
    if isinstance(o, dict):
        if set(o.keys()) >= {'point'} and all(not isinstance(v, dict) for v in o.values()):
            yield pre, o
            return
        for k, v in o.items():
            yield from flat(v, pre + '|' + str(k) if pre else str(k))
    else:
        yield pre, o


def fmt(v):
    if isinstance(v, float):
        return '%.6g' % v
    if isinstance(v, list):
        return '[' + ', '.join(fmt(x) for x in v) + ']'
    if isinstance(v, dict):
        return '{' + ', '.join('%s: %s' % (k, fmt(x)) for k, x in v.items()) + '}'
    return str(v)


j = json.load(open(sys.argv[1], encoding='utf-8'))
sub = sys.argv[2:] if len(sys.argv) > 2 else []
for k, v in flat(j):
    if all(s in k for s in sub):
        s = fmt(v)
        print(k, '=', s if len(s) < 400 else s[:400] + ' ...')
