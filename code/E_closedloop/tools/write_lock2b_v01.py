"""Write work\\locks\\LOCK_A10_2b.txt (A10 7.3: the E matched settings, from design data, after E2 and before E3). Never overwrites.

python -I write_lock2b_v01.py --matched ..\\out\\E2_MATCHED_v01.json --outcomes ..\\out\\OUTCOMES_E2_v01.json
       --recount ..\\out\\E2_RECOUNT_CALIB_v01.json [--note TEXT]
Records: SHA-256 of the matched-settings JSON (the file the E3/E3b job builder must use), of its inputs (E2 outcomes, the second
program's calibration, session B's IMM arrays and P-bar, the stored open-loop arrays are read by rev_common_v01 under its own
checks) and of the code that produced them; then the settings in plain text. Refuses if the second program's levels differ.
"""
import argparse, datetime, glob, hashlib, json, pathlib

E = pathlib.Path(__file__).resolve().parents[1]
LOCK = E.parent / 'locks' / 'LOCK_A10_2b.txt'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--matched', required=True); ap.add_argument('--outcomes', required=True)
    ap.add_argument('--recount', required=True); ap.add_argument('--recount-matched', required=True); ap.add_argument('--note', default='')
    a = ap.parse_args()
    assert not LOCK.exists(), 'LOCK_A10_2b.txt exists; never overwrite'
    m = json.loads(pathlib.Path(a.matched).read_text(encoding='utf-8'))
    rc = json.loads(pathlib.Path(a.recount).read_text(encoding='utf-8'))
    lv = m['levels']
    rlo, rhi, rlp = rc.get('g_lo'), rc.get('g_hi'), rc.get('low_power')
    if not (float(rlo) == float(lv['g_lo']) and float(rhi) == float(lv['g_hi']) and bool(rlp) == bool(lv['low_power'])):
        raise SystemExit('REFUSED: the second program gives other levels (%s, %s, %s)' % (rlo, rhi, rlp))
    rm = json.loads(pathlib.Path(a.recount_matched).read_text(encoding='utf-8'))['levels_out']
    for L in ('lo', 'hi'):
        mine = m['settings'][L]; theirs = rm[L]
        if mine['g_F0'] != theirs['g_L'] or abs(mine['F0_caution_pct'] - theirs['F0_caution_at_gL']) > 1e-9:
            raise SystemExit('REFUSED: F0 level or caution differs from the second program at ' + L)
        for nm, ent in mine['arms'].items():
            t = theirs['arms'][nm]
            if nm == 'PS':
                if list(ent['grid_indices']) != list(t['grid_indices']): raise SystemExit('REFUSED: PS triple differs at ' + L)
            elif ent['grid_index'] != t['grid_index'] or abs(ent['caution_pct'] - t['caution']) > 1e-9:
                raise SystemExit('REFUSED: %s differs from the second program at %s' % (nm, L))
    imm_files = sorted(glob.glob(str(E.parent / 'B_retrack' / 'out' / 'retrack' / 'B1' / 'p1b_fit_finite_*_arrays.npz')))
    lines = ['LOCK_A10_2b (AMENDMENT_10_v13.md 7.3): matched settings for E3 and E3b',
             'written %s by session E (Claude Opus 5.5), from design data only (E2 on the 30 lead-braking tuning cases; stored open-loop arrays of the 35 old evaluation runs)' % datetime.datetime.now().astimezone().isoformat(),
             '', 'matched-settings file (input of make_jobs_e_v01.py e3 / e3b):', '  %s  sha256 %s' % (pathlib.Path(a.matched).resolve(), sha(a.matched)),
             'inputs:',
             '  E2 outcomes (first program)  %s  sha256 %s' % (pathlib.Path(a.outcomes).resolve(), sha(a.outcomes)),
             '  E2 calibration (second program, Sonnet)  %s  sha256 %s' % (pathlib.Path(a.recount).resolve(), sha(a.recount)),
             '  matched settings (second program, Sonnet; identical grid indices, triple and cautions)  %s  sha256 %s' % (pathlib.Path(a.recount_matched).resolve(), sha(a.recount_matched)),
             '  IMM pair arrays (session B, variant B1): %d files, sha256 of the sorted list of their sha256: %s' % (
                 len(imm_files), hashlib.sha256(''.join(sha(f) for f in imm_files).encode()).hexdigest()),
             '  E_PBAR_IMM_v01.json  sha256 %s' % sha(E / 'src' / 'E_PBAR_IMM_v01.json'),
             'code:']
    for f in ('analysis/e_outcomes_v01.py', 'analysis/e_collect_v01.py', 'analysis/e2_matched_v01.py', 'recount/e_recount_v01.py'):
        lines.append('  %s  sha256 %s' % (f, sha(E / f)))
    lines += ['', 'E2 F0 contact shares (valid runs):']
    for g, ent in lv['per_g'].items():
        lines.append('  g = %-6s  %d / %d  share %.6f' % (g, ent['contacts'], ent['n'], ent['share']))
    lines += ['levels: g_lo = %g, g_hi = %g, low_power = %s' % (lv['g_lo'], lv['g_hi'], lv['low_power']), '']
    for L in ('lo', 'hi'):
        st = m['settings'][L]
        lines.append('level %s: F0 g = %g (open-loop caution %.6f %%)' % (L, st['g_F0'], st['F0_caution_pct']))
        for nm, ent in st['arms'].items():
            if nm == 'PS':
                lines.append('  PS   triple (before braking, braking, stopped) = %s  design caution %.6f %%' % (ent['triple'], ent['design_caution_pct']))
            else:
                lines.append('  %-6s g = %.12g (grid index %d), open-loop caution %.6f %% (|diff| %.6f%s)' % (
                    nm, ent['g'], ent['grid_index'], ent['caution_pct'], ent['abs_diff'], ', AT A GRID END' if ent.get('grid_end') else ''))
    if a.note: lines += ['', 'note: ' + a.note]
    LOCK.parent.mkdir(exist_ok=True)
    with open(LOCK, 'x', encoding='utf-8', newline='\n') as f: f.write('\n'.join(lines) + '\n')
    print(LOCK, 'sha256', sha(LOCK)); print('\n'.join(lines))


if __name__ == '__main__':
    main()
