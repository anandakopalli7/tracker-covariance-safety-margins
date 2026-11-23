r"""v13 round 2 (AMENDMENT_12 s3c, s7): the second program's side of out\A_EXPORT_B12X.json, and the key-by-key comparison.
New file, 22 Nov 2026 (Claude Opus 5.5). Copies values from the second programs' files (no number typed, nothing recomputed):
  B.MP.<label>.<phase>.*   from recount_fresh\out\MODEPROB2_<IMM2|B1R>_<new|fresh>_v01.json (Claude Sonnet's modeprob2_v01.py)
  B.IMM2N.twin.<k>         from CD_capture\recount_imm2\out\RC_Y_TWIN_L12_v13.json (byte-identical copy of CD's frozen Sonnet recount
                           rc_y_twin_l12_v13.py run on IMM2's arrays): every 'Y.<k>' of its `values` except 'Y.ref.*'
  recount  -> out\A_RECOUNT_B12X.json (+ _meta.json)
  compare  -> out\compare\B_B12X_COMPARE_v01.json: every key of A_EXPORT_B12X.json against A_RECOUNT_B12X.json; integers, booleans and
              strings exact, numbers and interval ends within 1e-9 relative (max(1, |a|, |b|)), null only against null. A key the first
              program does not produce by design is listed, not failed: B.IMM2N.twin.p_one_sided (the first Y program writes it only
              with calibrated intervals; the twin is run with nominal95).
Usage: python -I -B -X utf8 b_b12x_second_v01.py recount | compare
"""
import json, math, pathlib, sys, time, hashlib
HERE = pathlib.Path(__file__).resolve().parents[1]
OUT = HERE / 'out'; RC = HERE / 'recount_fresh' / 'out'
CD = HERE.parent / 'CD_capture'
MP = [('IMM2N', 'MODEPROB2_IMM2_new_v01.json'), ('IMM2C', 'MODEPROB2_IMM2_fresh_v01.json'), ('IMMrC', 'MODEPROB2_B1R_fresh_v01.json')]
TWIN = CD / 'recount_imm2' / 'out' / 'RC_Y_TWIN_L12_v13.json'
BY_DESIGN_SECOND_ONLY = {'B.IMM2N.twin.p_one_sided'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def recount():
    E = {}; meta = dict(code='b_b12x_second_v01.py recount', written=time.strftime('%Y-%m-%d %H:%M:%S'), sources={})
    for label, fn in MP:
        p = RC / fn
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding='utf-8')); d = d.get('by_phase', d)
        for ph in ('pre', 'braking', 'stopped'):
            s = d[ph]; pre = 'B.MP.%s.%s.' % (label, ph)
            E[pre + 'n'] = s['n']
            for k in ('mean', 'median', 'share_gt05'):
                E[pre + k] = s[k]; E[pre + k + '.ci'] = s[k + '_ci']
        meta['sources'][label] = dict(file=str(p.relative_to(HERE)), sha256=sha(p))
    if TWIN.exists():
        d = json.loads(TWIN.read_text(encoding='utf-8'))
        for k, v in d['values'].items():
            if k.startswith('Y.') and not k.startswith('Y.ref.'):
                E['B.IMM2N.twin.' + k[2:]] = v
        meta['sources']['twin'] = dict(file=str(TWIN.relative_to(HERE.parent)), sha256=sha(TWIN))
    meta['n_keys'] = len(E)
    o = OUT / 'A_RECOUNT_B12X.json'
    o.write_text(json.dumps(E, indent=1, default=float), encoding='utf-8')
    o.with_name(o.stem + '_meta.json').write_text(json.dumps(meta, indent=1), encoding='utf-8')
    print('wrote', o.name, len(E), 'keys; sources', sorted(meta['sources']))


def same(a, b):
    if isinstance(a, list) or isinstance(b, list):
        return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, (bool, str)) or isinstance(b, (bool, str)) or (isinstance(a, int) and isinstance(b, int)):
        return a == b
    a = float(a); b = float(b)
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    return abs(a - b) <= 1e-9 * max(1., abs(a), abs(b))


def compare():
    A = json.loads((OUT / 'A_EXPORT_B12X.json').read_text(encoding='utf-8'))
    B = json.loads((OUT / 'A_RECOUNT_B12X.json').read_text(encoding='utf-8'))
    rows = [dict(key=k, first=A[k], second=B[k], agree=same(A[k], B[k])) for k in sorted(set(A) & set(B))]
    only_a = sorted(set(A) - set(B)); only_b = sorted(set(B) - set(A))
    by_design = sorted(set(only_b) & BY_DESIGN_SECOND_ONLY)
    ok = all(r['agree'] for r in rows) and not only_a and set(only_b) <= BY_DESIGN_SECOND_ONLY
    doc = dict(code='b_b12x_second_v01.py compare', keys_compared=len(rows), keys_agree=sum(r['agree'] for r in rows),
               disagree=[r for r in rows if not r['agree']], only_first=only_a, only_second=only_b, only_second_by_design=by_design,
               all_agree=ok, first_sha256=sha(OUT / 'A_EXPORT_B12X.json'), second_sha256=sha(OUT / 'A_RECOUNT_B12X.json'),
               written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (OUT / 'compare').mkdir(parents=True, exist_ok=True)
    (OUT / 'compare' / 'B_B12X_COMPARE_v01.json').write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print('B12X: %d of %d keys agree; only first %s; only second %s (by design %s); ALL AGREE: %s'
          % (doc['keys_agree'], len(rows), only_a, only_b, by_design, ok))


if __name__ == '__main__':
    {'recount': recount, 'compare': compare}[sys.argv[1]]()
