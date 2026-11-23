"""Diagnostic 5 (post comparison): how often the LORO single-scale choice equals the full-sample choice, and the bound this
puts on the held-out single-scale frontier. Does not change RECOUNT_VALUES_v12.json."""
import json, numpy as np
exec(open('rc_diag_a93b_v12.py', encoding='utf-8').read().split('def heldout')[0])
Wa = W.sum(1); Sa = S.sum(1); Ka = K.sum(1)                   # (runs, 202) pooled over phases
chf = choose(100. * Sa.sum(0) / Ka.sum(0), Wa.sum(0), LEV)    # full-sample choice
same = 0; tot = 0; HO = np.zeros((NLEV, 3)); nof = np.zeros(NLEV, int)
for ri in range(len(runs)):
    oth = np.array([j for j in range(len(runs)) if j != ri])
    ch = choose(100. * Sa[oth].sum(0) / Ka[oth].sum(0), Wa[oth].sum(0), LEV)
    ok = (ch >= 0) & (chf >= 0)
    same += int((ch[ok] == chf[ok]).sum()); tot += int(ok.sum())
    g = np.where(ch >= 0, ch, 0); nof += ch < 0
    HO[ch >= 0] += np.stack([Wa[ri, g], Sa[ri, g], Ka[ri, g]], 1)[ch >= 0]
v = nof == 0
c = 100. * HO[v, 1] / HO[v, 2]; w = 100. * HO[v, 0] / N_ALL
wf = 100. * Wa.sum(0)[chf[v]] / N_ALL
out = dict(share_same_choice=same / tot, n_pairs=tot,
           max_abs_heldout_w_minus_fullsample_w_pp=float(np.max(np.abs(w - wf))),
           mean_heldout_w_minus_fullsample_w_pp=float(np.mean(w - wf)),
           sum_F_F0=float(F_F0.sum()))
print(json.dumps(out, indent=1))
open('rc_diag_a93e_v12.json', 'w', encoding='utf-8').write(json.dumps(out, indent=1))
