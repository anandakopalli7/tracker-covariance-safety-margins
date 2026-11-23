"""Second program (recount2): comparison with the first program's RESULT files (run only after RECOUNT2_RESULTS_v01.json exists).

Reads of the first program only: analysis\\out\\REV_E1_EXTRACT_SUMMARY_v01.json, analysis\\out\\REV_E2_EXTENDED_TRUTH_v01.json and the
arrays of analysis\\out\\ext\\<run>.npz (never its 'meta' string, never a .py). Writes RECOUNT2_COMPARE_v01.json and
RECOUNT2_COMPARE_v01.md into this folder.
Usage: python -B -X utf8 recount2_compare_v01.py
"""
import json, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
AN = HERE.parent / 'analysis' / 'out'
P = pathlib.Path(r'<library folder>')
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'


def main():
    mine = json.loads((HERE / 'RECOUNT2_RESULTS_v01.json').read_text(encoding='utf-8'))
    if not (HERE / 'out' / (mine['runs'][-1] + '.npz')).exists():
        raise RuntimeError('own results are not complete')
    e1 = json.loads((AN / 'REV_E1_EXTRACT_SUMMARY_v01.json').read_text(encoding='utf-8'))
    e2 = json.loads((AN / 'REV_E2_EXTENDED_TRUTH_v01.json').read_text(encoding='utf-8'))
    RUNS = mine['runs']; KEYS = mine['keys']
    out = dict(runs_equal=bool(e1['runs'] == RUNS), settings_equal=bool([list(v) for v in e1['variants']] == mine['settings']),
               keys_first_program_E1=list(e1['totals']), keys_first_program_E2=list(e2['pair_counts']), counts={}, elementwise={})

    # ---- own extra counts needed for the pair_counts of E2 (from own arrays and the stored 3 s clearance)
    extra = {kk: dict(unsafe_W1=0, decisions_no_safe_row_ext=0) for kk in KEYS}
    el = {kk: dict(n_eval_pairs=0, clearX_max_abs_diff=0., clearX_n_flag_differ=0, clearX_n_value_differ=0, clearX_n_nan_mismatch=0,
                   late_n_differ=0, cens_n_differ=0, clear61_max_abs_diff=0., clear61_n_flag_differ=0, tstop_max_abs_diff=0.,
                   J_vs_jend_n_differ=0, noneval_theirs_not_nan=0, shape_or_k_mismatch=0) for kk in KEYS}
    worst = dict(diff=0., run=None, key=None)
    for run in RUNS:
        a = np.load(HERE / 'out' / (run + '.npz'), allow_pickle=False)
        b = np.load(AN / 'ext' / (run + '.npz'), allow_pickle=False)
        z = np.load(STORED / (run + '.npz'), allow_pickle=False)
        ev = a['evaluated'].astype(bool); E2 = ev[:, None] & np.ones((1, 17), bool)
        clear3 = z['clear']
        same_k = bool(a['k'].shape == b['k'].shape and (a['k'] == b['k']).all())
        for kk in KEYS:
            e = el[kk]
            if not same_k or ('clearX_' + kk) not in b.files or b['clearX_' + kk].shape != a['clearX_' + kk].shape:
                e['shape_or_k_mismatch'] += 1
                continue
            ax = a['clearX_' + kk]; bx = b['clearX_' + kk]
            e['n_eval_pairs'] += int(E2.sum())
            nanmis = np.isnan(ax[E2]) != np.isnan(bx[E2])
            e['clearX_n_nan_mismatch'] += int(nanmis.sum())
            with np.errstate(invalid='ignore'):
                d = np.abs(ax[E2] - bx[E2])
            d = np.where(np.isnan(d), 0., d)            # inf - inf (same sign) counts as equal; NaN mismatches are counted above
            d = np.where((ax[E2] == bx[E2]), 0., d)
            m = float(d.max()) if d.size else 0.
            if m > worst['diff']:
                worst = dict(diff=m, run=run, key=kk)
            e['clearX_max_abs_diff'] = max(e['clearX_max_abs_diff'], m)
            e['clearX_n_value_differ'] += int((d > 0).sum())
            e['clearX_n_flag_differ'] += int(((ax > 0) != (bx > 0))[E2].sum())
            e['late_n_differ'] += int((a['late_' + kk] != b['late_' + kk])[E2].sum())
            e['cens_n_differ'] += int((a['cens_' + kk] != b['cens_' + kk])[E2].sum())
            e['noneval_theirs_not_nan'] += int((~np.isnan(bx[~E2])).sum())
            if ('clear61_' + kk) in b.files:
                a6 = a['clear61_' + kk][E2]; b6 = b['clear61_' + kk][E2]
                with np.errstate(invalid='ignore'):
                    d6 = np.where(a6 == b6, 0., np.abs(a6 - b6))
                e['clear61_max_abs_diff'] = max(e['clear61_max_abs_diff'], float(np.nanmax(d6)) if d6.size else 0.)
                e['clear61_n_flag_differ'] += int(((a6 > 0) != (b6 > 0)).sum())
            if ('tstop_' + kk) in b.files:
                dt = np.abs(a['tstop_' + kk][E2] - b['tstop_' + kk][E2])
                e['tstop_max_abs_diff'] = max(e['tstop_max_abs_diff'], float(np.nanmax(dt)) if dt.size else 0.)
            if ('jend_' + kk) in b.files:
                e['J_vs_jend_n_differ'] += int((a['J_' + kk] != b['jend_' + kk])[E2].sum())
            extra[kk]['unsafe_W1'] += int((~(clear3 > 0) & E2).sum())
            extra[kk]['decisions_no_safe_row_ext'] += int((ev & ~(ax > 0).any(axis=1)).sum())
    out['elementwise'] = el
    out['elementwise_overall'] = dict(max_abs_diff_clearX=max(e['clearX_max_abs_diff'] for e in el.values()), worst=worst,
                                      n_flag_differ_clearX=int(sum(e['clearX_n_flag_differ'] for e in el.values())),
                                      n_value_differ_clearX=int(sum(e['clearX_n_value_differ'] for e in el.values())),
                                      n_late_differ=int(sum(e['late_n_differ'] for e in el.values())),
                                      n_cens_differ=int(sum(e['cens_n_differ'] for e in el.values())),
                                      n_nan_mismatch=int(sum(e['clearX_n_nan_mismatch'] for e in el.values())),
                                      n_shape_or_k_mismatch=int(sum(e['shape_or_k_mismatch'] for e in el.values())),
                                      n_pairs_compared=int(sum(e['n_eval_pairs'] for e in el.values())))

    # ---- counts
    n_count_diff = 0
    for kk in KEYS:
        t = mine['totals'][kk]; f1 = e1['totals'].get(kk, {}); f2 = e2['pair_counts'].get(kk, {})
        rows = [
            ('pairs evaluated', t['n_pairs'], f1.get('n_pairs'), f2.get('pairs')),
            ('late pairs (stop ends after 3 s)', t['n_late'], f1.get('n_late'), None),
            ('late and safe on 61 frames', t['n_late_safe61'], f1.get('n_late_safe61'), f2.get('late_safe_as_scored')),
            ('of those: censored', t['n_cens_safe61'], f1.get('n_cens_safe61'), f2.get('censored_safe_as_scored')),
            ('late, safe on 61 frames, extended clearance <= 0', t['n_late_safe61_unsafeX'], f1.get('n_flag_changed_by_extension'),
             f2.get('late_safe_now_unsafe')),
            ('censored, safe on 61 frames and still > 0 on the frames seen', t['n_cens_safe61'] - t['n_late_safe61_unsafeX_censored'], None,
             f2.get('censored_safe_est')),
            ('pairs with 61-frame clearance <= 0', t['n_unsafe61'], None, f2.get('unsafe_as_scored')),
            ('pairs with extended clearance <= 0', t['n_unsafeX'], None, f2.get('unsafe_est')),
            ('pairs with 3 s commitment clearance <= 0', extra[kk]['unsafe_W1'], None, f2.get('unsafe_W1')),
            ('evaluated decisions without a row of extended clearance > 0', extra[kk]['decisions_no_safe_row_ext'], None,
             f2.get('decisions_no_safe_row_est')),
            ('non-late pairs changed by the extension', t['n_notlate_clearX_differs_from_61'], f1.get('n_nonlate_changed'), None),
            ('largest last frame J', t['J_max'], f1.get('jend_max'), None),
        ]
        ent = []
        for name, m, a1, a2 in rows:
            ok = all(x is None or x == m for x in (a1, a2))
            n_count_diff += int(not ok)
            ent.append(dict(what=name, recount2=m, first_E1=a1, first_E2=a2, agree=bool(ok)))
        out['counts'][kk] = ent
    out['n_count_differences'] = n_count_diff

    # ---- optional scoring
    sp = HERE / 'RECOUNT2_SCORING_v01.json'
    if sp.exists():
        s = json.loads(sp.read_text(encoding='utf-8'))
        opt = {}
        for pop in ('all', 'moving'):
            fp = e2['scorings']['est_t0p75_a6p0']['pops'].get(pop)
            if fp is None:
                continue
            me = s['pops'][pop]
            c = dict(
                n=(me['RS_extended']['n'], fp['n']),
                denE=(me['RS_extended']['denE'], fp['denE']['point']),
                den0=(me['RS_extended']['den0'], fp['den0']['point']),
                denE_over_3s=(me['denE_ext_over_denE_W1'], fp['denE_over_3s']['point']),
                den0_over_3s=(me['den0_ext_over_den0_W1'], fp['den0_over_3s']['point']))
            for a in ('N', 'NA', 'AM', 'CK3', 'Q'):
                fa = fp['arms'].get(a) or fp['arms'].get('A1' if a == 'AM' else a)
                if fa is not None and 'D' in fa:
                    c['D_' + a] = (me['RS_extended']['D'][a], fa['D'])
            opt[pop] = {k: dict(recount2=v[0], first=v[1], abs_diff=abs(v[0] - v[1])) for k, v in c.items()}
            opt[pop]['denE_ext_over_denE_RS61_recount2_only'] = me['denE_ext_over_denE_RS61']
        out['optional_scoring_t0p75_a6p0'] = opt
        out['optional_first_program_arm_names'] = list(e2['scorings']['est_t0p75_a6p0']['pops']['all']['arms'])
        asis = e2['scorings'].get('asscored_t0p75_a6p0', {}).get('pops', {}).get('all')
        if asis is not None:
            out['optional_asscored_all'] = dict(
                denE=dict(recount2=s['pops']['all']['RS_61frames_own']['denE'], first=asis['denE']['point']),
                den0=dict(recount2=s['pops']['all']['RS_61frames_own']['den0'], first=asis['den0']['point']))
        cz = e2['scorings'].get('cens_t0p75_a6p0', {}).get('pops', {}).get('all')
        if cz is not None:
            out['optional_cens_all'] = dict(
                denE=dict(recount2_censored_counted_unsafe=s['pops']['all']['RS_extended_censored_unsafe']['denE'], first=cz['denE']['point']),
                den0=dict(recount2_censored_counted_unsafe=s['pops']['all']['RS_extended_censored_unsafe']['den0'], first=cz['den0']['point']))
    (HERE / 'RECOUNT2_COMPARE_v01.json').write_text(json.dumps(out, indent=1), encoding='utf-8')

    # ---- report
    A = mine['anchors']; ov = out['elementwise_overall']
    L = ['# Recount 2 (independent second program): the extended truth of the reaction-and-stop scoring — comparison', '',
         'Written by `recount2_compare_v01.py` on the results of `recount2_ext_v01.py` (own code, written from the specification; the '
         'first program was not read). Files of the first program opened for this comparison, after the own results were written: '
         '`analysis\\out\\REV_E1_EXTRACT_SUMMARY_v01.json`, `analysis\\out\\REV_E2_EXTENDED_TRUTH_v01.json`, the arrays of '
         '`analysis\\out\\ext\\<run>.npz`. No `.py` of the first program was opened.', '',
         '## Anchors (own results against the stored results of record)', '',
         '| anchor | result |', '|---|---|',
         '| decision ticks rebuilt = stored `k` (35 runs) | yes (the program stops otherwise) |',
         '| own evaluated rule (target present, k + 60 <= kmax) = stored `evaluated` | %d mismatches |' % A['n_evaluated_flag_mismatch'],
         '| (a) own clearance on frames 0..60 against stored `clearR_<key>`: safe flags | %s (9 settings, %d pairs each) |' % (
             'identical' if A['a_flags_identical_all_settings'] else 'DIFFER', mine['totals'][KEYS[0]]['n_pairs']),
         '| (a) largest absolute difference of the values | %.3g m (within 1e-9: %s) |' % (A['a_max_abs_diff_all_settings'], A['a_within_1e9']),
         '| (a) same against the recount cache `<run>_pack.npz` | flags differing %d, largest difference %.3g m |' % (
             A['a_pack_flags_differ'], A['a_pack_max_abs_diff']),
         '| (b) own `t_stop_abs` against stored `tstopR_<key>` | largest difference %.3g s, %d values not bit-equal |' % (
             A['b_tstop_max_abs_diff'], A['b_tstop_n_not_bitwise_equal']),
         '| (c) (0.75 s, 6 m/s2): evaluated pairs | %d (expected 140,930) |' % A['c_t0p75_a6p0']['n_pairs'],
         '| (c) late and safe on the 61-frame window | %d (expected 5,356) |' % A['c_t0p75_a6p0']['n_late_safe61'],
         '| (c) of those censored | %d (expected 153) |' % A['c_t0p75_a6p0']['n_cens_safe61'],
         '| continuation formula reproduces `replan_s` on frames j_react+1 and 60 | %d differences |' % A['n_prefix_differs'],
         '| truth frames contiguous 0..kmax in every run; actor extents constant | %s; %s |' % (
             A['truth_frames_contiguous_all_runs'], A['actor_extents_constant_all_runs']),
         '| true actors per run (max); an actor ending before the window | %d; %d cases |' % (
             A['max_true_actors_per_run'], A['n_actor_ends_before_window']), '',
         '## Counts per setting: recount 2 beside the first program', '',
         'E1 = `REV_E1_EXTRACT_SUMMARY_v01.json` (`totals`), E2 = `REV_E2_EXTENDED_TRUTH_v01.json` (`pair_counts`). '
         'Evaluated pairs: %d in every setting.' % mine['totals'][KEYS[0]]['n_pairs'], '',
         '| setting | late & safe on 61 frames (R2 / E1 / E2) | of those censored (R2 / E1 / E2) | late, safe on 61, extended <= 0 (R2 / E1 / E2) | '
         'of those censored (R2) | clearance <= 0 on 61 frames (R2 / E2) | extended clearance <= 0 (R2 / E2) | all agree |',
         '|---|---|---|---|---|---|---|---|']
    for (tau, Aa), kk in zip(mine['settings'], KEYS):
        t = mine['totals'][kk]; f1 = e1['totals'].get(kk, {}); f2 = e2['pair_counts'].get(kk, {})
        ok = all(r['agree'] for r in out['counts'][kk])
        L.append('| tau %.2f s, A %.1f | %d / %s / %s | %d / %s / %s | %d / %s / %s | %d | %d / %s | %d / %s | %s |' % (
            tau, Aa, t['n_late_safe61'], f1.get('n_late_safe61'), f2.get('late_safe_as_scored'),
            t['n_cens_safe61'], f1.get('n_cens_safe61'), f2.get('censored_safe_as_scored'),
            t['n_late_safe61_unsafeX'], f1.get('n_flag_changed_by_extension'), f2.get('late_safe_now_unsafe'),
            t['n_late_safe61_unsafeX_censored'], t['n_unsafe61'], f2.get('unsafe_as_scored'), t['n_unsafeX'], f2.get('unsafe_est'),
            'yes' if ok else 'NO'))
    L += ['', 'Further shared counts (late pairs, censored pairs still > 0, pairs unsafe under the 3 s commitment, decisions without a safe row, '
          'non-late pairs changed, largest last frame) are in `RECOUNT2_COMPARE_v01.json` -> `counts`. Count entries that differ: **%d**.' % n_count_diff]
    if n_count_diff:
        L += ['', 'Differences:']
        for kk in KEYS:
            for r in out['counts'][kk]:
                if not r['agree']:
                    L.append('- %s, %s: recount2 %s, E1 %s, E2 %s' % (kk, r['what'], r['recount2'], r['first_E1'], r['first_E2']))
    L += ['', '## Element-wise comparison with `analysis\\out\\ext\\<run>.npz` (evaluated decisions x 17 rows)', '',
          '| setting | pairs | max abs diff `clearX` (m) | values differing | safe/unsafe flags differing | `late` differing | `cens` differing | '
          'max abs diff `clear61` (m) | max abs diff `tstop` (s) | last frame differing (own J vs `jend`) |', '|---|---|---|---|---|---|---|---|---|---|']
    for (tau, Aa), kk in zip(mine['settings'], KEYS):
        e = el[kk]
        L.append('| tau %.2f s, A %.1f | %d | %.3g | %d | %d | %d | %d | %.3g | %.3g | %d |' % (
            tau, Aa, e['n_eval_pairs'], e['clearX_max_abs_diff'], e['clearX_n_value_differ'], e['clearX_n_flag_differ'], e['late_n_differ'],
            e['cens_n_differ'], e['clear61_max_abs_diff'], e['tstop_max_abs_diff'], e['J_vs_jend_n_differ']))
    L += ['', 'Over all 9 settings (%d pairs): largest absolute difference of the extended clearance **%.3g m**%s; pairs whose safe/unsafe '
          'flag differs **%d**; `late` flags differing %d; `cens` flags differing %d; NaN mismatches %d; arrays with a different shape or '
          'decision list %d.' % (ov['n_pairs_compared'], ov['max_abs_diff_clearX'],
                                 (' (%s, %s)' % (ov['worst']['run'], ov['worst']['key'])) if ov['worst']['run'] else '',
                                 ov['n_flag_differ_clearX'], ov['n_late_differ'], ov['n_cens_differ'], ov['n_nan_mismatch'],
                                 ov['n_shape_or_k_mismatch']),
          'Non-evaluated decisions: NaN in the own arrays; entries of the first program that are not NaN there: %d.' % sum(
              e['noneval_theirs_not_nan'] for e in el.values())]
    if 'optional_scoring_t0p75_a6p0' in out:
        L += ['', '## OPTIONAL: scoring at (0.75 s, 6 m/s2) with the own extended clearances', '',
              'Own extended clearances scored with the earlier independent recount library `recount\\rc_lib_v01.py` (wrong go = extended '
              'clearance <= 0; caution axis from the 3 s commitment clearance; 201 levels; perfect oracle = first row with extended clearance '
              '> 0, else the fallback row). First program: `REV_E2_EXTENDED_TRUTH_v01.json` -> `scorings.est_t0p75_a6p0.pops`.', '',
              '| population | quantity | recount 2 | first program | abs diff |', '|---|---|---|---|---|']
        for pop, c in out['optional_scoring_t0p75_a6p0'].items():
            for k2, v in c.items():
                if isinstance(v, dict):
                    L.append('| %s | %s | %.12g | %.12g | %.3g |' % (pop, k2, v['recount2'], v['first'], v['abs_diff']))
        o = out['optional_scoring_t0p75_a6p0']['all']
        L += ['', '`denE_over_3s` of the first program equals denE(extended) / denE(3 s commitment scoring). The other reading, '
              'denE(extended) / denE(reaction-and-stop on the 61-frame window), is %.6f in the own computation (all evaluated decisions).' %
              o['denE_ext_over_denE_RS61_recount2_only']]
        if 'optional_asscored_all' in out:
            x = out['optional_asscored_all']
            L.append('As scored on 61 frames (all): denE recount 2 %.12g, first program (`asscored_t0p75_a6p0`) %.12g; den0 %.12g against %.12g.' % (
                x['denE']['recount2'], x['denE']['first'], x['den0']['recount2'], x['den0']['first']))
        if 'optional_cens_all' in out:
            x = out['optional_cens_all']
            L.append('Censored pairs counted unsafe (own reading: every late, 61-frame-safe, censored pair set unsafe; all): denE recount 2 %.12g, '
                     'first program (`cens_t0p75_a6p0`, whose exact definition was not checked) %.12g; den0 %.12g against %.12g.' % (
                         x['denE']['recount2_censored_counted_unsafe'], x['denE']['first'], x['den0']['recount2_censored_counted_unsafe'],
                         x['den0']['first']))
    L += ['', '## Points of the specification that needed a reading', '',
          '1. **Which true actors and frames.** `ol_extract_v01.window_truth` takes the actors present at the decision frame and follows each '
          'over its contiguous true frames (it stops at the first frame without the actor). The same was done beyond frame 60. In these 35 runs '
          'there is one true actor per run, present in every frame, with constant extents, so no other reading can change a number.',
          '2. **"Censored"** was taken literally as late and J > kmax - k. The extended clearance of a censored pair is the minimum over the frames '
          'that exist, so a censored pair with extended clearance <= 0 is a definite contact and one with > 0 is undetermined. The count of '
          'flag changes includes the censored ones (given separately above).',
          '3. **Frames after the stop** (j > J) are not examined: a contact after the ego has come to rest is not counted, as specified.',
          '4. **"Ratio to the 3 s denE"** (optional part) can mean the 3 s commitment scoring or the reaction-and-stop scoring on the 3 s window; '
          'both are given; the first program\'s `denE_over_3s` is the former.',
          '5. `oc.poly_dist` returns 0 for overlapping or touching rectangles, so "clearance <= 0" means clearance = 0.',
          '6. **What the agreement covers.** As the specification directs, the position profile comes from the code of record '
          '(`replan_s`, `brake_profile`) and the distances from `oc.rect_corners` / `oc.poly_dist`. The bit-identical values suggest the first '
          'program calls the same functions. The agreement therefore checks the extension logic (frames used, last frame J, late and censored '
          'flags, truth window, counting, and in the optional part the scoring), not those shared functions; an error inside them would not '
          'show here.', '']
    (HERE / 'RECOUNT2_COMPARE_v01.md').write_text('\n'.join(L), encoding='utf-8')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
