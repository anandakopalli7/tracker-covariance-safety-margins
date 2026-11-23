"""Replace the pod-made B7 arrays of the runs that differ from the laptop's CV0 in a key B7 reads by laptop re-extractions (frozen
x_trk_extract_v13.py, all 8 chains), per the coordinator's rule of 20 Nov 08:45 EST (A10 sec. 11 record). Moves files only; computes
no value. New file, 20 Nov 2026 (Claude Opus 5.5).

For each replaced run: the laptop chain 2/0 must equal the laptop CV0 array bit for bit on EVERY common key (else REFUSED, nothing
moved); the pod file goes to arrays_pod_superseded/<chain>/<rid>.npz, the laptop file is copied to arrays/<chain>/<rid>.npz, both
SHA-256s recorded in analysis/out/B7_REPLACED_RUNS_v13.json.
Usage: python -I b7_replace_v13.py  (reads arrays_laptop_fix/)
"""
import hashlib, json, pathlib, shutil, sys, time
import numpy as np
CD = pathlib.Path(__file__).resolve().parents[1]
FIX = CD / 'arrays_laptop_fix'; ARR = CD / 'arrays'; OLD = CD / 'arrays_pod_superseded'
REC = CD / 'analysis' / 'out' / 'B7_REPLACED_RUNS_v13.json'
CHAINS = ['2_0', '2_0.1', '5_0', '5_0.1', '5_0.2', '10_0', '10_0.1', '10_0.2']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    runs = {}
    for f in sorted(FIX.glob('*/*.npz')):
        runs.setdefault((f.parent.name.split('_', 1)[0], f.stem), []).append(f)
    plan = []
    for (pre, rid), files in sorted(runs.items()):
        if len(files) != 8: raise SystemExit(f'REFUSED: {pre} {rid} has {len(files)} of 8 chains in arrays_laptop_fix')
        two = FIX / f'{pre}_2_0' / f'{rid}.npz'
        a = np.load(ARR / 'CV0' / f'{rid}.npz', allow_pickle=False); b = np.load(two, allow_pickle=False)
        common = [k for k in a.files if k in b.files and k != 'meta']
        diff = [k for k in common if not np.array_equal(a[k], b[k], equal_nan=True)]
        if diff: raise SystemExit(f'REFUSED: laptop {pre}_2_0 of {rid} differs from CV0 in {diff}')
        for c in CHAINS:
            plan.append(dict(run=rid, chain=f'{pre}_{c}', laptop=FIX / f'{pre}_{c}' / f'{rid}.npz', pod=ARR / f'{pre}_{c}' / f'{rid}.npz',
                             keys_checked_vs_cv0=len(common) if c == '2_0' else None))
    rows = []
    for p in plan:
        if not p['pod'].is_file(): raise SystemExit(f'REFUSED: pod file missing {p["pod"]}')
        dst_old = OLD / p['chain'] / p['pod'].name; dst_old.parent.mkdir(parents=True, exist_ok=True)
        rows.append(dict(run=p['run'], chain=p['chain'], pod_sha256=sha(p['pod']), laptop_sha256=sha(p['laptop']),
                         keys_equal_to_cv0_on_chain_2_0=p['keys_checked_vs_cv0']))
        shutil.move(str(p['pod']), str(dst_old)); shutil.copy2(p['laptop'], p['pod'])
        if sha(p['pod']) != rows[-1]['laptop_sha256']: raise SystemExit(f'copy failed {p["pod"]}')
    doc = dict(schema='B7_REPLACED_RUNS_V13', rule='coordinator 20 Nov 08:45 EST: a fresh run whose pod-made arrays differ from the laptop '
               'CV0 in any key B7 reads is re-extracted on the laptop with the frozen extractor (all 8 chains) and replaces the pod version',
               cause='extraction geometry uses glibc on the pod and Windows libm on the laptop; exact_trig covers the tracker path only',
               survey='analysis/out/B7_CROSSMACHINE_DIFF_v13.json', written=time.strftime('%Y-%m-%d %H:%M:%S'),
               runs=sorted({r['run'] for r in rows}), files=rows)
    REC.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(f'replaced {len(rows)} files for {len(doc["runs"])} runs: {doc["runs"]}')


if __name__ == '__main__':
    main()
