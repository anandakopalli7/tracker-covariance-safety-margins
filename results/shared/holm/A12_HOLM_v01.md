# Holm across A12's primary hypotheses (A12 section 4)

Written 2026-11-22T06:18:27-05:00 by holm_a12_v01.py (sha256 e2505a2be1386b049d3ae31238fc349861f7844dced292ef470eb268500ace32), coordinating session (Claude Opus 5.5).
m = 6. A pair missing at the cut-off enters as p = 1 (not completed). Family-wise 0.05, one-sided.

| id | hypothesis | status | registered p | Holm | reject | p, one convention (1+k)/(n+1) | Holm | reject |
|---|---|---|---|---|---|---|---|---|
| DR2 | DR2's class on the new runs (A12 3a.3): r = RR_gl(N_DR) | ran | 0.00395 | 0.0079 | yes | 0.00395 | 0.0079 | yes |
| DOSE | Dose-response trend (A12 3a.4): OLS slope b of r on p | ran | 0.0059 | 0.0079 | yes | 0.0059 | 0.0079 | yes |
| Y1 | Y1 on the new runs (A12 3b): Delta = RR_gl(N_B2) - RR_gl(B2p) | ran | 0 | 0 | yes | 5e-05 | 0.0003 | yes |
| IMM2 | IMM2's class on the new runs (A12 3c): RR_gl(N_IMM2) | ran | 0 | 0 | yes | 5e-05 | 0.0003 | yes |
| M1 | Section 5's tau for CANMOT over miss pairs (nuScenes val) | ran | 5e-05 | 0.0002 | yes | 5e-05 | 0.0003 | yes |
| E5 | Section 6's primary comparison (caution-matched closed loop): contact N - F0_D | ran | 5e-05 | 0.0002 | yes | 0.0001 | 0.0003 | yes |
