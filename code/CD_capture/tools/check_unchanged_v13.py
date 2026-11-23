"""Read-only: compare the four current exports with kept copies, key by key (Python ==, no tolerance). New file, 21 Nov 2026
(Claude Opus 5.5). Keys allowed to change are named with --allow; for TRANSFER.structured the per-set values, orderings and the
'N inside delta' flag are shown old vs new.
Usage: python -I -B check_unchanged_v13.py KEEPDIR --allow KEY[,KEY...] --out NAME  -> out/NAME (refuses to overwrite)
"""
import hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; OUT = CD / 'out'
KEEP = pathlib.Path(sys.argv[1]); KEEP = KEEP if KEEP.is_absolute() else CD / KEEP
ALLOW = set(sys.argv[sys.argv.index('--allow') + 1].split(',')) if '--allow' in sys.argv else set()
NAME = sys.argv[sys.argv.index('--out') + 1]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    out = OUT / NAME
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    res = {}; transfer = {}
    for n in ('A_EXPORT_C', 'A_EXPORT_D', 'A_RECOUNT_C', 'A_RECOUNT_D'):
        old = json.loads((KEEP / f'{n}.json').read_text(encoding='utf-8')); new = json.loads((OUT / f'{n}.json').read_text(encoding='utf-8'))
        ov, nv = old['values'], new['values']
        changed = sorted(k for k in ov if k in nv and nv[k] != ov[k]); missing = sorted(k for k in ov if k not in nv)
        added = sorted(k for k in nv if k not in ov)
        res[n] = dict(old_sha256=sha(KEEP / f'{n}.json'), new_sha256=sha(OUT / f'{n}.json'), values=[len(ov), len(nv)],
                      changed=changed, missing=missing, added=added, changed_not_allowed=[k for k in changed if k not in ALLOW],
                      other_fields_differing=sorted(k for k in set(old) | set(new) if k != 'values' and old.get(k) != new.get(k)),
                      outcomes_equal=old.get('outcomes') == new.get('outcomes'), deviations_equal=old.get('deviations') == new.get('deviations'))
        res[n]['ok'] = not res[n]['changed_not_allowed'] and not missing and not added
        if 'TRANSFER.structured' in ov:
            a, b = ov['TRANSFER.structured'], nv['TRANSFER.structured']
            transfer[n] = dict(N_inside_delta=[a['N_inside_delta_all_sets'], b['N_inside_delta_all_sets']], sets=[a['sets'], b['sets']],
                               sets_missing=[a['sets_missing'], b['sets_missing']],
                               orderings_removed=[o for o in a['orderings'] if o not in b['orderings']],
                               orderings_added=[o for o in b['orderings'] if o not in a['orderings']], orderings_new=b['orderings'],
                               per_set_changed={s: {c: [a['per_set'].get(s, {}).get(c), b['per_set'][s].get(c)] for c in b['per_set'][s]
                                                    if a['per_set'].get(s, {}).get(c) != b['per_set'][s].get(c)} for s in b['per_set']
                                                if a['per_set'].get(s) != b['per_set'][s]})
    verdict = 'OK' if all(x['ok'] for x in res.values()) else 'NOT OK'
    out.write_text(json.dumps(dict(schema='CHECK_UNCHANGED_V13', keep=str(KEEP), allowed=sorted(ALLOW), verdict=verdict, files=res,
                                   transfer=transfer), indent=1), encoding='utf-8')
    for n, x in res.items():
        print(n, 'ok' if x['ok'] else 'NOT OK', '| values %s | changed %s | missing %d | added %d | other fields differing %s | outcomes equal %s | deviations equal %s'
              % (x['values'], x['changed'], len(x['missing']), len(x['added']), x['other_fields_differing'], x['outcomes_equal'], x['deviations_equal']))
    for n, t in transfer.items(): print(n, 'TRANSFER', json.dumps(t))
    print('verdict', verdict, '->', out.name)


if __name__ == '__main__':
    main()
