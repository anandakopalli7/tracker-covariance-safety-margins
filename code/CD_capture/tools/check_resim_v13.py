"""Task 5 acceptance (A10 sec. 0.2): per re-simulated run rs13_<old job>, compare every frame's noisy-sweep SHA-256 (frames.jsonl
raw_sha256, in k order) and noise receipt (noisy_sha256) with the old run's logged values (old archive of record on the volume:
/workspace/claude_main_v01/results/<old job>/claude_main_<old job>.tar.gz). Accepted only if the frame counts are equal and every hash
is equal. Reads hashes only. Pod system python3. Usage: python3 check_resim_v13.py [results_dir]
"""
import json, pathlib, sys, tarfile

RES = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/opt/claude_v13_resim/results')
OLD = pathlib.Path('/workspace/claude_main_v01/results')


def hashes(arch):
    fr, nr = {}, []
    with tarfile.open(arch, 'r:gz') as t:
        for m in t:
            if not m.isfile() or '/capture/' not in m.name: continue
            if m.name.endswith('/frames.jsonl'):
                for l in t.extractfile(m).read().decode().splitlines():
                    if l.strip():
                        d = json.loads(l); fr[d['k']] = d.get('raw_sha256')
            elif m.name.endswith('/noise_receipts.jsonl'):
                nr = [json.loads(l)['noisy_sha256'] for l in t.extractfile(m).read().decode().splitlines() if l.strip()]
    return [fr[k] for k in sorted(fr)], nr


out = []
for d in sorted(RES.glob('rs13*')):
    rid = d.name; old = rid.split('_', 1)[1]                    # rs13_<old> (first attempt) or rs13r_<old> (retry)
    rec = list(d.glob('*.receipt.json'))
    if not rec: out.append(dict(run=rid, status='no receipt')); continue
    r = json.loads(rec[0].read_text())
    if r['status'] != 'CAPTURED_AND_REVIEWED': out.append(dict(run=rid, status=r['status'])); continue
    oa = OLD / old / f'claude_main_{old}.tar.gz'
    if not oa.is_file(): out.append(dict(run=rid, status='old archive not found')); continue
    nf, nn = hashes(d / r['archive']); of, on = hashes(oa)
    first = next((i for i, (a, b) in enumerate(zip(nf, of)) if a != b), None)
    ok = len(nf) == len(of) and first is None and nn == on
    out.append(dict(run=rid, old=old, accepted=ok, frames_new=len(nf), frames_old=len(of), first_mismatch_index=first,
                    noise_receipts_equal=nn == on))
print(json.dumps(dict(checked=len(out), accepted=sum(1 for x in out if x.get('accepted')), runs=out)))
