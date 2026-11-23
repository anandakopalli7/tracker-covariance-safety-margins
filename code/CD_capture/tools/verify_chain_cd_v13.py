"""Chain-aware check of CD's freeze manifests with their addenda (read-only). New file, 21 Nov 2026 (Claude Opus 5.5).

Why: the frozen make_freeze_cd_v13.py --verify keeps one addendum per path and applies it only when its sha256_before equals the frozen
sha256. FREEZE_CD_2_add2 changes a file that FREEZE_CD_2_add1 already changed (export/make_export_cd_v13.py), so its sha256_before is
add1's sha256_after and the frozen verifier reports the file as changed. This check applies a manifest's addenda in file order
(<manifest>_add1, _add2, ...): each addendum entry must start from the SHA-256 the chain has reached for that path (the frozen one, or
an earlier addendum's sha256_after); the file on disk must equal the end of its chain. Any break is reported.
Usage: python -I verify_chain_cd_v13.py
"""
import hashlib, json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; WORK = CD.parent; REV = WORK.parent
LOCKS = WORK / 'locks'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def norm(x):
    parts = [q.lower() for q in pathlib.PureWindowsPath(x).parts]
    return '/'.join(parts[parts.index('revision_v13') + 1:] if 'revision_v13' in parts else parts)


def check(manifest):
    d = json.loads(manifest.read_text(encoding='utf-8'))
    state = {}
    for g, es in d['groups'].items():
        for e in es:
            key = norm(e['path']) if pathlib.PureWindowsPath(e['path']).is_absolute() else norm('revision_v13/' + e['path'])
            state[key] = dict(path=e['path'], sha=e['sha256'], chain=[('frozen', e['sha256'])])
    adds = sorted(LOCKS.glob(manifest.stem + '_add*.json'), key=lambda p: int(re.search(r'_add(\d+)\.json$', p.name).group(1)))
    breaks = []
    for af in adds:
        for r in json.loads(af.read_text(encoding='utf-8')).get('replaces', []):
            k = norm(r['path'])
            if k not in state: breaks.append(f'{af.name}: {r["path"]} is not in {manifest.name}'); continue
            if state[k]['sha'] != r['sha256_before']:
                breaks.append(f'{af.name}: {r["path"]} starts from {r["sha256_before"][:12]}, chain is at {state[k]["sha"][:12]}'); continue
            state[k]['sha'] = r['sha256_after']; state[k]['chain'].append((af.name, r['sha256_after']))
    bad = []
    for k, s in state.items():
        p = pathlib.Path(s['path']); p = p if p.is_absolute() else REV.parent / p if str(s['path']).lower().startswith('revision_v13') else WORK.parent / p
        if not p.is_file() or sha(p) != s['sha']: bad.append(s['path'])
    chained = {s['path']: [f'{a}:{h[:12]}' for a, h in s['chain']] for s in state.values() if len(s['chain']) > 1}
    return dict(manifest=manifest.name, manifest_sha256=sha(manifest), addenda=[a.name for a in adds], files=len(state),
                changed_or_missing=bad, chain_breaks=breaks, chained_files=chained)


if __name__ == '__main__':
    for m in ('FREEZE_CD.json', 'FREEZE_CD_2.json'):
        print(json.dumps(check(LOCKS / m), indent=1))
