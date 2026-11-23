"""A12 sec. 2.2 change (coordinator, 22 Nov 2026 about 00:35 EST, the 10 Hz hedge): the L12 study jobs with keep_raw = true, sweeps on
the pod-local disk only. Writes l12/jobs_l12/JOBS_PL12_<pod>_v02.json from the frozen _v01 lists (FREEZE_CD_add7), identical except
keep_raw = true on every study (role eval) job, as C's study jobs (make_jobs_c_v13.py); controls unchanged (keep_raw false, as in C).
New file, 22 Nov 2026 (Claude Opus 5.5, session CD). Never overwrites.
"""
import copy, hashlib, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent; J = HERE / 'jobs_l12'


def main():
    for k in range(1, 7):
        src = J / f'JOBS_PL12_claude-v13cd-l{k}_v01.json'; dst = J / f'JOBS_PL12_claude-v13cd-l{k}_v02.json'
        d = json.loads(src.read_text(encoding='utf-8')); e = copy.deepcopy(d)
        n = 0
        for j in e['jobs']:
            if j.get('role') == 'eval':
                assert j['keep_raw'] is False and j['id'].startswith('pl12_'); j['keep_raw'] = True; n += 1
            else:
                assert j['keep_raw'] is False
        e['note'] = d['note'] + (' | v02 (A12 sec. 2.2 change, 10 Hz hedge): keep_raw true on every study job, sweeps on the pod-local disk '
                                 'only; derived from %s (sha256 %s) by make_jobs_l12_raw_v13.py; nothing else differs.'
                                 % (src.name, hashlib.sha256(src.read_bytes()).hexdigest()))
        diff = [(a['id'], x) for a, b in zip(d['jobs'], e['jobs']) for x in set(a) | set(b) if a.get(x) != b.get(x)]
        assert len(d['jobs']) == len(e['jobs']) and all(x == 'keep_raw' for _, x in diff) and len(diff) == n
        assert {x for x in set(d) | set(e) if d.get(x) != e.get(x)} == {'jobs', 'note'}
        text = json.dumps(e, indent=1) + '\n'
        if dst.exists():
            if dst.read_text(encoding='utf-8') != text: raise SystemExit('REFUSED: %s exists with different content' % dst.name)
        else: dst.write_text(text, encoding='utf-8', newline='\n')
        print(dst.name, hashlib.sha256(dst.read_bytes()).hexdigest(), 'study jobs keep_raw true:', n, 'controls:', len(e['jobs']) - n)


if __name__ == '__main__':
    main()
