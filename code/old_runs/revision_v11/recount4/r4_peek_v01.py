"""Recount4 helper (after the own results were written): structure of the first program's file REV_E2_EXTENDED_TRUTH_v01.json."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
F = HERE.parent / 'analysis' / 'out' / 'REV_E2_EXTENDED_TRUTH_v01.json'
d = json.loads(F.read_text(encoding='utf-8'))
depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
sub = sys.argv[2].split('/') if len(sys.argv) > 2 else []


def show(o, ind=0, dep=depth):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)) and dep > 0:
                print(' ' * ind + str(k) + (' {%d}' % len(v) if isinstance(v, dict) else ' [%d]' % len(v)))
                show(v, ind + 2, dep - 1)
            else:
                s = json.dumps(v)
                print(' ' * ind + str(k) + ': ' + (s if len(s) < 150 else s[:150] + ' ...'))
    elif isinstance(o, list):
        s = json.dumps(o)
        print(' ' * ind + (s if len(s) < 200 else s[:200] + ' ...'))
    else:
        print(' ' * ind + json.dumps(o))


o = d
for k in sub:
    o = o[k]
print('file bytes', F.stat().st_size, 'top keys', list(d.keys()) if isinstance(d, dict) else type(d))
show(o)
