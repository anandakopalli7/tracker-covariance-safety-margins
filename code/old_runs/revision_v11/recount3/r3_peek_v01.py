"""Recount3: print the structure of the first program's four result files (opened only after RECOUNT3_RESULTS_v01.json was written).
Usage: python -B -X utf8 r3_peek_v01.py <G|D|E3|F2> [maxdepth]"""
import json, pathlib, sys
OUT = pathlib.Path(__file__).resolve().parent.parent / 'analysis' / 'out'
FILES = dict(G='REV_G_PARTIAL_DRAWS_v01.json', D='REV_D_BOOTSTRAP_v01.json', E3='REV_E3_EXTENDED_GAP2_v01.json', F2='REV_F2_BRAKING_PRIOR_v01.json')


def walk(o, path, depth, maxdepth):
    if isinstance(o, dict):
        if depth >= maxdepth:
            print('%s: {%d keys: %s}' % (path, len(o), ', '.join(list(o.keys())[:12]))); return
        for k, v in o.items():
            walk(v, path + '.' + str(k), depth + 1, maxdepth)
    elif isinstance(o, list):
        if len(o) and isinstance(o[0], (dict, list)) and depth < maxdepth:
            print('%s: list of %d' % (path, len(o)))
            walk(o[0], path + '[0]', depth + 1, maxdepth)
        else:
            s = json.dumps(o)
            print('%s: list(%d) %s' % (path, len(o), s if len(s) < 160 else s[:160] + ' ...'))
    else:
        s = json.dumps(o)
        print('%s: %s' % (path, s if len(s) < 300 else s[:300] + ' ...'))


which = sys.argv[1]
md = int(sys.argv[2]) if len(sys.argv) > 2 else 6
j = json.loads((OUT / FILES[which]).read_text(encoding='utf-8'))
if which == 'D':
    j = {'D3_sensitivities': {'m_out_of_n': j['D3_sensitivities']['m_out_of_n']}, '(other top-level keys, not opened)': list(j.keys())}
walk(j, which, 0, md)
