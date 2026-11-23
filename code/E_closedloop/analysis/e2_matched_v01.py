"""E2 -> matched settings (A10 7.3), the content of work\\locks\\LOCK_A10_2b.txt. Design data only (the 30 lead-braking
tuning cases of E2, and the 35 old evaluation runs' stored open-loop arrays).

Writer: session E (Claude Opus 5.5), 19 Nov 2026. Rules (A10 7.3), fixed before any closed-loop run:
  Levels  g_lo = the E2 grid value whose F0 contact share on the tuning cases is nearest 0.20; g_hi nearest 0.05 (ties: smaller
          g). If every share is below 0.05: g_lo = 0.25, g_hi = 1, and the contact comparisons are labelled low-power.
  Other arms  g_A,L = the grid scale (202-value grid of record) whose open-loop caution on the old evaluation runs is nearest
          F0's open-loop caution at g_L (ties: smaller g); the IMM pair from session B's arrays of the IMM tracker.
  PS      its H4 triple at that caution level: the scale triple with the lowest wrong-go among triples whose design caution
          (phases by the tracker's estimate, threshold -1.0 m/s^2) is at most F0's caution at g_L; ties to the lowest caution,
          then the lowest index (a9_3_phase_scale_cv_v02.triple_choice, copied verbatim below).
Open-loop caution: the scoring of record (rev_common_v01 / optA_lib_v02, imported read only): 3 s commitment (W1), all
evaluated decisions, statistics summed over the 35 runs, caution % = 100 * sum of (oracle row speed - selected row speed) /
desired over decisions whose selection is W1-safe, divided by their number (optA_lib_v02.stats_scored, rates).

Usage: python -I -B e2_matched_v01.py --e2 <E2_OUTCOMES.json> [--imm-dir <B arrays dir>] --out <MATCHED.json>
  E2_OUTCOMES.json: {"runs": [{"case":..., "g":..., "contact": 0|1, "valid": true|false}, ...]} from e_outcomes_v01 over the
  E2 runs (180). Invalid runs (policy failure, status not CAPTURED_AND_REVIEWED) are excluded from the shares and listed.
  --curves-only: write only the open-loop caution curves (no E2 input needed; for the freeze and the review).
"""
import argparse, json, pathlib, sys, time
import numpy as np

V11 = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis')
V12OUT = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out')
sys.path.insert(0, str(V11))
import rev_common_v01 as C          # noqa: E402  (read only; imports optA_lib_v02)
L = C.L
GRID = C.GRID
E2_GRID = (0., 0.25, 1., 4., 16., 64.)
TARGET = dict(lo=0.20, hi=0.05)
PHASE_THR = -1.0
PH = [2, 3, 4]
_PBAR_FILE = pathlib.Path(__file__).resolve().parents[1] / 'src' / 'E_PBAR_IMM_v01.json'
PBAR_IMM = json.loads(_PBAR_FILE.read_text(encoding='utf-8'))['Pbar'] if _PBAR_FILE.exists() else None


# ---------------------------------------------------------------------------- a9_3_phase_scale_cv_v02.triple_choice (verbatim)
def triple_choice(Tph, lev):
    """Tph: three (G, NST) training tables -> per level (g0, g1, g2) scale indices (or -1)."""
    U = []; IX = []
    for T in Tph:
        Arr = np.stack([T[:, 1], T[:, 2], T[:, 3]], axis=1)
        u, ix = np.unique(Arr, axis=0, return_index=True)
        U.append(u); IX.append(ix)
    n = float(Tph[0][0, 0] + Tph[1][0, 0] + Tph[2][0, 0])
    W = (U[0][:, 0][:, None, None] + U[1][:, 0][None, :, None] + U[2][:, 0][None, None, :]).ravel()
    S = (U[0][:, 1][:, None, None] + U[1][:, 1][None, :, None] + U[2][:, 1][None, None, :]).ravel()
    K = (U[0][:, 2][:, None, None] + U[1][:, 2][None, :, None] + U[2][:, 2][None, None, :]).ravel()
    with np.errstate(divide='ignore', invalid='ignore'):
        c = 100. * S / K; w = 100. * W / n
    ok = np.isfinite(c) & np.isfinite(w)
    idx_ok = np.nonzero(ok)[0]
    o = np.argsort(c[ok], kind='stable'); cs = c[ok][o]; ws = w[ok][o]; src = idx_ok[o]
    cm = np.minimum.accumulate(ws)
    new = np.concatenate([[True], cm[1:] < cm[:-1]])
    pos = np.maximum.accumulate(np.where(new, np.arange(ws.size), 0))
    j = np.searchsorted(cs, lev, side='right') - 1
    flat = np.where(j >= 0, src[pos[np.clip(j, 0, None)]], -1)
    sh = (U[0].shape[0], U[1].shape[0], U[2].shape[0])
    out = np.full((lev.size, 3), -1, int)
    okl = flat >= 0
    i0, i1, i2 = np.unravel_index(flat[okl], sh)
    out[okl, 0] = IX[0][i0]; out[okl, 1] = IX[1][i1]; out[okl, 2] = IX[2][i2]
    return out


def caution_at(runs, name, grid):
    """Pooled open-loop caution % (W1, population 'all') of source `name` at each scale of `grid`."""
    T = None
    for r in runs:
        sel = L.select_grid(r['crit'][name], np.asarray(grid, float), r['idx55'])
        st = L.stats_scored(sel, r['clear1'], r['clear1'] > 0., r['vbar'], r['desired'], r['masks'])
        T = st if T is None else T + st
    return L.rates(T[:, 0, :])[1], T


def nearest(curve, target):
    d = np.abs(np.asarray(curve) - target)
    d = np.where(np.isfinite(d), d, np.inf)
    return int(np.argmin(d))                 # first minimum = smallest g (grid ascending)


def load(imm_dir):
    runs = C.load_runs()
    for r in runs:
        z = np.load(V12OUT / 'tg' / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(z['k'], r['k']): raise SystemExit('REFUSED: TG arrays of %s differ in k' % r['run'])
        r['crit']['TG'] = z['cTG2']
        zl = np.load(V12OUT / 'lead' / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(zl['k'], r['k']): raise SystemExit('REFUSED: lead arrays of %s differ in k' % r['run'])
        vh = zl['vhat']; ah = zl['ahat_long']; fd = zl['lead_found'].astype(bool)
        ph = np.zeros(vh.size, np.int64)
        ph[fd & (vh > 0.5) & np.isfinite(ah) & (ah <= PHASE_THR)] = 1; ph[fd & (vh <= 0.5)] = 2
        r['masks_hat'] = C.masks_of(r['ev'], r['v0'], ph)
        if imm_dir is not None:
            # session B's B1 arrays (work\B_retrack\out\retrack\B1\<run>_arrays.npz): cF0 with P-bar_IMM, cN from the B1 tracks.
            zi = np.load(pathlib.Path(imm_dir) / (r['run'] + '_arrays.npz'), allow_pickle=False)
            for key, mine in (('k', r['k']), ('idx55', r['idx55']), ('evaluated', r['ev']), ('vbar', r['vbar']), ('clear', r['clear_raw'])):
                if not np.array_equal(zi[key], mine, equal_nan=True): raise SystemExit('REFUSED: IMM arrays of %s differ in %s' % (r['run'], key))
            mi = json.loads(str(zi['meta']))
            if mi.get('variant') != 'B1': raise SystemExit('REFUSED: IMM arrays of %s are not variant B1' % r['run'])
            if PBAR_IMM is not None and any(not np.array_equal(np.asarray(mi['pbar'][c]), np.asarray(PBAR_IMM[c])) for c in ('vehicle', 'pedestrian')):
                raise SystemExit('REFUSED: IMM arrays of %s used another P-bar than E_PBAR_IMM_v01.json' % r['run'])
            r['crit']['F0_IMM'] = zi['cF0']; r['crit']['N_IMM'] = zi['cN']
    return runs


def levels_from_e2(e2):
    rows = []
    for x in e2['runs']:                       # e_collect_v01 output (stage e2) or a plain list of {case, g, contact, valid}
        if 'outcomes' in x or 'contact' not in x:
            c = (x.get('outcomes') or {}).get('contact')
            rows.append(dict(case=x['case'], g=x['g'], contact=c, valid=bool(x['valid']) and c is not None, job=x.get('job')))
        else:
            if 'valid' not in x: raise SystemExit('REFUSED: E2 row without a validity flag: %r' % (x,))
            rows.append(x)
    out = {}; invalid = []
    for g in E2_GRID:
        rr = [x for x in rows if float(x['g']) == g]
        ok = [x for x in rr if x['valid']]
        invalid += [x for x in rr if not x['valid']]
        out[g] = dict(n=len(ok), n_listed=len(rr), contacts=sum(int(x['contact']) for x in ok),
                      share=(sum(int(x['contact']) for x in ok) / len(ok)) if ok else float('nan'))
    shares = [out[g]['share'] for g in E2_GRID]
    low_power = all(s < 0.05 for s in shares if np.isfinite(s))
    if low_power:
        g_lo, g_hi = 0.25, 1.
    else:
        pick = lambda t: E2_GRID[int(np.argmin([abs(s - t) if np.isfinite(s) else np.inf for s in shares]))]
        g_lo, g_hi = pick(TARGET['lo']), pick(TARGET['hi'])
    # A10 is silent when the rule gives g_lo == g_hi or g_lo = 0 (the zero margin itself): stop and ask (A10 11; review Minor 4).
    ask = []
    if g_lo == g_hi: ask.append('g_lo equals g_hi (%g)' % g_lo)
    if g_lo == 0. or g_hi == 0.: ask.append('a level is the zero margin (g = 0)')
    return dict(per_g={str(g): v for g, v in out.items()}, g_lo=g_lo, g_hi=g_hi, low_power=low_power, invalid_runs=invalid, ask_author=ask)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--e2'); ap.add_argument('--imm-dir'); ap.add_argument('--out', required=True)
    ap.add_argument('--curves-only', action='store_true')
    a = ap.parse_args()
    t0 = time.time()
    runs = load(a.imm_dir)
    names = ['F0', 'N', 'CK3', 'TG'] + (['F0_IMM', 'N_IMM'] if a.imm_dir else [])
    curves = {nm: caution_at(runs, nm, GRID)[0] for nm in names}
    doc = dict(schema='E_MATCHED_SETTINGS_V01', code='e2_matched_v01.py', runs=[r['run'] for r in runs], grid_size=int(GRID.size),
               caution_curves_pct={nm: [float(x) for x in c] for nm, c in curves.items()}, imm_dir=a.imm_dir)
    if not a.curves_only:
        e2 = json.loads(pathlib.Path(a.e2).read_text(encoding='utf-8'))
        lv = levels_from_e2(e2); doc['levels'] = lv
        if lv['ask_author']:
            doc['settings'] = None; doc['stopped'] = 'A10 7.3 does not cover this case; the author is asked before E3: ' + '; '.join(lv['ask_author'])
            pathlib.Path(a.out).write_text(json.dumps(doc, indent=1), encoding='utf-8'); print(json.dumps(lv, indent=1)); raise SystemExit(doc['stopped'])
        # F0 phase tables (estimated phase) for the PS triple
        Xh = C.tables(runs, ('W1',), ['F0'], masks_key='masks_hat')['F0']          # (35, G, 6, NST)
        Tph = [Xh[:, :, pi, :].sum(axis=0) for pi in PH]
        settings = {}
        for L_name, gL in (('lo', lv['g_lo']), ('hi', lv['g_hi'])):
            cL = float(caution_at(runs, 'F0', [gL])[0][0])
            ent = dict(g_F0=gL, F0_caution_pct=cL, arms={})
            for nm in names:
                if nm == 'F0': continue
                i = nearest(curves[nm], cL)
                ent['arms'][nm] = dict(g=float(GRID[i]), grid_index=i, caution_pct=float(curves[nm][i]), abs_diff=float(abs(curves[nm][i] - cL)),
                                       grid_end=bool(i in (0, GRID.size - 1)))   # review Minor 6: an end of the grid means the curve may not reach F0's caution
            ch = triple_choice(Tph, np.array([cL]))[0]
            if (ch < 0).any():
                ent['arms']['PS'] = dict(triple=None, note='no triple with design caution <= level; the author is asked (A10 11)')
            else:
                rt_c = [float(L.rates(Tph[q][ch[q]])[1]) for q in range(3)]
                Wt = sum(Tph[q][ch[q], 1] for q in range(3)); St = sum(Tph[q][ch[q], 2] for q in range(3)); Kt = sum(Tph[q][ch[q], 3] for q in range(3))
                n = sum(Tph[q][0, 0] for q in range(3))
                ent['arms']['PS'] = dict(triple=[float(GRID[i]) for i in ch], grid_indices=[int(i) for i in ch],
                                         design_caution_pct=float(100. * St / Kt), design_wrong_go_pct=float(100. * Wt / n), per_phase_caution_pct=rt_c)
            settings[L_name] = ent
        doc['settings'] = settings
    doc['seconds'] = round(time.time() - t0, 1); doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    pathlib.Path(a.out).write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps({k: v for k, v in doc.items() if k != 'caution_curves_pct'}, indent=1))


if __name__ == '__main__':
    main()
