r"""v13 round 2 (AMENDMENT_12 s3c): flat export of IMM2's descriptive extras for package A: mode probabilities by truth phase and
the permuted twin. New file, 22 Nov 2026 (Claude Opus 5.5). Copies values from files (no number typed, nothing recomputed):
  B.MP.<label>.<phase>.{n, mean, mean.ci, median, median.ci, share_gt05, share_gt05.ci}   from out\modeprob\MODEPROB_<label>_<set>_v01.json
      labels: IMM2N (IMM2, new runs), IMM2C (IMM2, C runs), IMMrC (B1r, C runs); phases pre, braking, stopped; each label only if its file exists
  B.IMM2N.twin.<k>   from CD_capture\ycheck_imm2\out\Y_TWIN_L12_v13.json (CD's frozen Y program run on IMM2's arrays): every key 'Y.<k>' of
      its `values` except the online-tracker reference 'Y.ref.*' (the program names IMM2's values RR_NB2 / RR_B2s / RR_B2p: B2 is its
      input slot, here IMM2); only if the file exists.
Writes out\A_EXPORT_B12X.json (+ _meta.json); refuses to change an existing key's value.
Usage: python -I -B -X utf8 b_export_b12x_v01.py
"""
import json, pathlib, time, hashlib
HERE = pathlib.Path(__file__).resolve().parents[1]
OUT = HERE / 'out'
CD = HERE.parent / 'CD_capture'
MP = [('IMM2N', 'MODEPROB_IMM2_new_v01.json'), ('IMM2C', 'MODEPROB_IMM2_fresh_v01.json'), ('IMMrC', 'MODEPROB_B1R_fresh_v01.json')]
TWIN = CD / 'ycheck_imm2' / 'out' / 'Y_TWIN_L12_v13.json'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    E = {}; meta = dict(code='b_export_b12x_v01.py', written=time.strftime('%Y-%m-%d %H:%M:%S'), sources={})
    for label, fn in MP:
        p = OUT / 'modeprob' / fn
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding='utf-8'))
        for ph, s in d['by_phase'].items():
            pre = 'B.MP.%s.%s.' % (label, ph)
            E[pre + 'n'] = s['n']
            for k in ('mean', 'median', 'share_gt05'):
                E[pre + k] = s[k]; E[pre + k + '.ci'] = s[k + '_ci']
        meta['sources'][label] = dict(file=str(p.relative_to(HERE)), sha256=sha(p), run_set=d['run_set'], n_runs=d['n_runs'], seed=d['seed'])
    if TWIN.exists():
        d = json.loads(TWIN.read_text(encoding='utf-8'))
        for k, v in d['values'].items():
            if k.startswith('Y.') and not k.startswith('Y.ref.'):
                E['B.IMM2N.twin.' + k[2:]] = v
        meta['sources']['twin'] = dict(file=str(TWIN.relative_to(HERE.parent)), sha256=sha(TWIN), gate=d['gate'], intervals=d['intervals'],
                                       code=d['code'], code_sha256=d.get('code_sha256'))
    o = OUT / 'A_EXPORT_B12X.json'
    if o.exists():
        cur = json.loads(o.read_text(encoding='utf-8'))
        changed = [k for k in cur if k in E and json.dumps(cur[k], default=float) != json.dumps(E[k], default=float)]
        gone = [k for k in cur if k not in E]
        if changed or gone:
            raise SystemExit('REFUSED: existing keys would change or vanish: %s %s' % (changed[:5], gone[:5]))
    meta['n_keys'] = len(E)
    o.write_text(json.dumps(E, indent=1, default=float), encoding='utf-8')
    o.with_name(o.stem + '_meta.json').write_text(json.dumps(meta, indent=1), encoding='utf-8')
    print('wrote', o.name, len(E), 'keys; sources', sorted(meta['sources']))


if __name__ == '__main__':
    main()
