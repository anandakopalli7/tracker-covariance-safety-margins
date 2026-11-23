r"""v13 round 2 (AMENDMENT_12 s3c): the kappa_q search as a NOTE (not a design input; the coordinator chose the kappa of record at
22 Nov 00:18 EST). New file, 22 Nov 2026 (Claude Opus 5.5). The search (b_imm2_tune_v01.py kq, run 1, 00:12:26-00:18:58 EST) evaluated
all 121 grid points and printed every median to its log out\imm2t\kq_run1_killed.out; it was stopped (chain stopped for the
coordinator's decision) while evaluating its final point, so it wrote no JSON. This script copies the 121 medians from that log
(no recomputation) into out\imm2t\IMM2_TUNE_KQ_v01.json with the rule's reading: first sign change of (median - 2), or the grid
value nearest 2.
Usage: python -I -B -X utf8 b_imm2_kq_note_v01.py
"""
import json, pathlib, re, hashlib, time
import numpy as np
D = pathlib.Path(__file__).resolve().parents[1] / 'out' / 'imm2t'
LOG = D / 'kq_run1_killed.out'
GRID = [10. ** (-3 + 0.05 * j) for j in range(121)]


def main():
    med = []
    for line in LOG.read_text(encoding='utf-8').splitlines():
        m = re.match(r'kq (\d+)/121 medians \[([-0-9.e]+), ([-0-9.e]+)\]', line)
        if m:                                   # the log prints the last two medians; the final line (121) adds one new value
            n = int(m.group(1))
            assert n in (len(med) + 2, len(med) + 1)
            med += [float(m.group(2)), float(m.group(3))][-(n - len(med)):]
        m1 = re.match(r'kq (\d+)/121 medians \[([-0-9.e]+)\]', line)
        if m1:
            assert int(m1.group(1)) == len(med) + 1
            med.append(float(m1.group(2)))
    assert len(med) == 121, len(med)
    dev = np.array(med) - 2.
    jx = next((j for j in range(120) if np.sign(dev[j]) != np.sign(dev[j + 1]) or dev[j] == 0), None)
    jn = int(np.argmin(np.abs(dev)))
    doc = dict(code='b_imm2_kq_note_v01.py', status='NOTE (not used): kappa_q = the kappa of record by the coordinator, 22 Nov 00:18 EST',
               source_log='out/imm2t/kq_run1_killed.out', source_log_sha256=hashlib.sha256(LOG.read_bytes()).hexdigest(),
               search='kq: variant B3, truth phase pre, A10 B3 rule (2) restricted (b_imm2_tune_v01.py)', grid=GRID, grid_median=med,
               j_first_sign_change=jx, nearest_j=jn, nearest_kappa=GRID[jn], nearest_median=med[jn], window_reached=bool(1.8 <= med[jn] <= 2.2),
               median_range_j0_60=[min(med[:61]), max(med[:61])], written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (D / 'IMM2_TUNE_KQ_v01.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps({k: doc[k] for k in ('j_first_sign_change', 'nearest_j', 'nearest_kappa', 'nearest_median', 'window_reached', 'median_range_j0_60')}))


if __name__ == '__main__':
    main()
