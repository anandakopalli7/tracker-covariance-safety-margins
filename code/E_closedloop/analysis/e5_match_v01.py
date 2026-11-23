"""Package E, set E5 (A12 §6.5): N's scale matched to F0_D's open-loop caution under dropouts. Design data only.

Inputs (read only): session F's masked DR arrays of the 105 fresh lead-braking runs, work\\F_dropout\\out\\arrays\\DR\\*.npz
(A11 §6c masks DR_MASKS_v02, output.punish_num = 3; cF0 with P-bar_DR = F0_D's class average; cN from the tracker).
Each file's meta must say mode 'dr', punish_num 3, pbar 'P-bar_DR (PBAR_DR_v01.json)'.
Open-loop caution: the scoring of record, exactly as E2's matching (e2_matched_v01.caution_at): rev_common_v01 / optA_lib_v02,
3 s commitment (W1), population 'all' (evaluated decisions), pooled over the runs, caution % from stats_scored / rates.
Grid of record: [0] + logspace(-2, 3, 201).

Output (written BEFORE any calibration run, so the mapping is fixed by design data alone):
  out\\E5_MATCH_TABLE_v01.json: for each candidate g_D in {4, 8, 16, 32}: F0_D's caution at g_D, g_N = the grid scale whose
  N caution is nearest it (ties: smaller g), N's caution there, and the difference; plus both full caution curves.
After the calibration, LOCK_A12b records the row of the chosen g_D.

python -I -B e5_match_v01.py
"""
import hashlib, json, pathlib, sys

import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
W = E.parent
FARR = W / 'F_dropout' / 'out' / 'arrays' / 'DR'
PBAR_DR = W / 'F_dropout' / 'out' / 'PBAR_DR_v01.json'
V11 = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis')
sys.path.insert(0, str(V11))
import rev_common_v01 as C          # noqa: E402  (read only; imports optA_lib_v02)
L = C.L
sys.path.insert(0, str(E / 'analysis'))
import e2_matched_v01 as M          # noqa: E402  (caution_at, nearest: E2's matching, frozen)

GRID = np.concatenate([[0.], np.logspace(-2, 3, 201)])
CANDIDATES = (4., 8., 16., 32.)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load_runs():
    files = sorted(FARR.glob('*.npz'))
    if len(files) != 105: raise SystemExit('REFUSED: expected 105 DR arrays, found %d' % len(files))
    runs = []
    for f in files:
        z = np.load(f, allow_pickle=False); m = json.loads(str(z['meta']))
        if m.get('mode') != 'dr' or m.get('punish_num') != 3 or m.get('pbar') != 'P-bar_DR (PBAR_DR_v01.json)' or m.get('family') != 'lead_braking':
            raise SystemExit('REFUSED: %s is not a masked DR lead-braking array with punish 3 and P-bar_DR' % f.name)
        ev = z['evaluated'].astype(bool); v0 = z['v0']; ph = z['phase'].astype(np.int64)
        runs.append(dict(run=f.stem, desired=float(m['desired']), clear1=L.clean_clear(z['clear']), vbar=z['vbar'], idx55=z['idx55'],
                         masks=C.masks_of(ev, v0, ph), crit={'F0D': z['cF0'], 'N': z['cN']}, n_eval=int(ev.sum()), sha256=sha(f)))
    return runs


def main():
    out = E / 'out' / 'E5_MATCH_TABLE_v01.json'
    assert not out.exists(), 'never overwrite'
    runs = load_runs()
    cF, _ = M.caution_at(runs, 'F0D', GRID)
    cN, _ = M.caution_at(runs, 'N', GRID)
    rows = []
    for g in CANDIDATES:
        target = float(M.caution_at(runs, 'F0D', [g])[0][0])
        j = M.nearest(cN, target)
        rows.append(dict(g_D=g, caution_F0D_pct=target, g_N=float(GRID[j]), g_N_index=j, caution_N_pct=float(cN[j]),
                         caution_diff_pp=float(cN[j] - target), grid_end=bool(j in (0, len(GRID) - 1))))
    doc = dict(schema='E5_MATCH_TABLE_V01', code='e5_match_v01.py', code_sha256=sha(__file__), design_data='F DR arrays, 105 fresh lead-braking runs',
               arrays=dict(dir=str(FARR.relative_to(W)).replace(chr(92), '/'), n=len(runs), sha256_of_sorted_list=hashlib.sha256(''.join(r['sha256'] for r in runs).encode()).hexdigest()),
               pbar_dr_sha256=sha(PBAR_DR), grid='[0] + logspace(-2, 3, 201)', scoring='rev_common_v01 / optA_lib_v02 stats_scored, W1, population all, pooled',
               evaluated_decisions=sum(r['n_eval'] for r in runs), candidates=rows,
               curves=dict(F0D=[float(x) for x in cF], N=[float(x) for x in cN]))
    with open(out, 'x', encoding='utf-8', newline='\n') as fh: fh.write(json.dumps(doc, indent=1) + '\n')
    for r in rows: print(r)
    print('->', out.name, sha(out))


if __name__ == '__main__':
    main()
