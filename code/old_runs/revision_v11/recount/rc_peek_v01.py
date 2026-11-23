"""Recount, comparison stage: print the structure of a first-program results JSON (keys, types, short values).
Usage: python -B -X utf8 rc_peek_v01.py <file.json> [max_depth] [max_items]"""
import json, sys

j = json.load(open(sys.argv[1], encoding='utf-8'))
MD = int(sys.argv[2]) if len(sys.argv) > 2 else 4
MI = int(sys.argv[3]) if len(sys.argv) > 3 else 40


def show(o, ind, depth):
    if isinstance(o, dict):
        ks = list(o.keys())
        for k in ks[:MI]:
            v = o[k]
            if isinstance(v, (dict, list)) and depth < MD and not (isinstance(v, list) and all(not isinstance(x, (dict, list)) for x in v)):
                print('%s%s: %s(%d)' % (ind, k, type(v).__name__, len(v)))
                show(v, ind + '  ', depth + 1)
            else:
                s = json.dumps(v)
                print('%s%s = %s' % (ind, k, s if len(s) < 230 else s[:230] + ' ...'))
        if len(ks) > MI:
            print('%s... %d more keys: %s' % (ind, len(ks) - MI, ks[MI:MI + 30]))
    elif isinstance(o, list):
        for i, v in enumerate(o[:3]):
            print('%s[%d]:' % (ind, i))
            show(v, ind + '  ', depth + 1)
        if len(o) > 3:
            print('%s... %d more items' % (ind, len(o) - 3))
    else:
        print(ind + json.dumps(o)[:230])


show(j, '', 0)
