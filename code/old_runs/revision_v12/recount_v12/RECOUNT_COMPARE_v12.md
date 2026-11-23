# RECOUNT_COMPARE_v12: independent recount of the A9 analyses against the first program

Written 19 Nov 2026 by the recount agent (second program). Programs: `rc_lib_v12.py`, `rc_main_v12.py` (values), `rc_compare_v12.py` (the table below; also RECOUNT_COMPARE_TABLE_v12.json), `rc_diag_a93*_v12.py` (diagnostics written after the comparison; they do not change the values). No `a9_*.py` file was opened. `RECOUNT_VALUES_v12.json` was written at 00:42 EST, before any first-program JSON was opened; its SHA-256 at that moment is in `RECOUNT_VALUES_v12.sha256_before_compare.txt` (7a9ca823...158a), and it was not changed afterwards.

Imported unchanged: `optA_lib_v02.py` (select_grid, stats_scored, eval_scoring, frontier, dec_eq, clean_clear, select_first_safe, ratio) and `rev_common_v01.py` (load_runs, masks_of, GRID). My own code, cross-checked against the library: the per-row contribution sums, a separate step-frontier and frontier-point routine (equal to `eval_scoring` to 0.0 on every grid evaluation), the gridless event algorithm (equal to the grid tables at the 202 grid values, integer columns exact, caution sums within 9.1e-13), the leave-one-run-out choice (checked against a brute-force lexicographic search), the attribution, the stop-reliance shares and the tuning-run loader.

## Result

**338 values compared; 330 agree within 1e-9 (327 exactly, the other 3 within 2.3e-16); 8 differ. All 8 are in A9-3, in the leave-one-run-out (LORO) held-out frontiers.** A9-1 (a, b, c), A9-4(b), A9-5, A9-6 and A9-7 agree completely. In A9-3 these agree: the in-sample gains and shares, both phase sources; the confusion matrix and agreement; the number of run-level pairs with no qualifying training point; and, for the estimated phase, Σ(F1_in − Fps_cv), exactly (1076.357056694813).

| Disagreement | Recount | First program | Abs. difference |
|---|---|---|---|
| A9-3(a) truth phase, LORO G_cv share Σ(F1_cv − Fps_cv)/Σ(F_F0 − F_E) | 0.9034905823397271 | 0.2976499049593918 | 0.606 |
| A9-3(a) truth phase, LORO G_cv (pp) | 5.020494631786783 | 1.6539737980783655 | 3.37 |
| A9-3(a) truth phase, LORO G_cv_vs_in share Σ(F1_in − Fps_cv)/same | 0.8678503542422673 | 0.8714791774667361 | 0.00363 |
| A9-3(a) truth phase, LORO G_cv_vs_in (pp) | 4.82244987367145 | 4.842614430861375 | 0.0202 |
| A9-3(a) Σ(F1_cv − F1_in), single-scale held-out minus in-sample | +39.80699638118214 | −640.9167671893848 | 680.7 |
| A9-3(b) estimated phase, LORO G_cv share | 0.9993303957145329 | 0.38986089510972877 | 0.609 |
| A9-3(b) estimated phase, LORO G_cv (pp) | 5.553054990427837 | 2.1663695995294936 | 3.39 |
| A9-3(b) Σ(F1_cv − F1_in) (the single-scale part has no phase, so this is the same as in (a)) | +39.80699638118214 | −640.9167671893848 | 680.7 |

### What I did about them
I re-read A9-3 of Amendment 09: "for each of the 35 runs and each of the 201 pooled caution levels of record, the scale triple … with the lowest wrong-go among triples whose caution on the other 34 runs is at or below the level (ties: lowest caution, then lowest index) is chosen on those 34 runs and applied to the left-out run. The left-out counts are summed over the 35 runs, and the held-out frontier is the step frontier of the 201 resulting points, with F0's zero-margin point. The same procedure with one scale gives a held-out single-scale frontier." My code does exactly this. Nothing in the amendment says my reading is wrong, so **I did not change my code.** The values in `RECOUNT_VALUES_v12.json` stand as computed. The disagreements have two separate sources:

1. **The single-scale held-out frontier F1_cv (drives both G_cv shares).** The first program's Σ(F1_cv − F1_in) = −640.92 puts its held-out single-scale frontier 3.19 pp below the in-sample single-scale frontier on average. Mine is 0.198 pp above it (+39.81). Under the amendment's procedure such a gap cannot be reached (`rc_diag_a93e_v12.json`):
   - Each held-out point's wrong go differs from the full-sample point at the same level by at most 0.97 pp (mean +0.067 pp).
   - Its caution lies within 0.9 pp of the level (`rc_diag_a93_v12.json`).
   - The single-scale choice is the same for every phase source, and the first program prints −640.92 for both.

   Other ways to build the frontier do not reproduce −640.92 (`rc_diag_a93_v12.json`):
   - placing each held-out point at its own level: +13.44;
   - dropping F0's zero-margin point: +39.81;
   - letting every point qualify at every level: −1202.81.

   Constructions that do not apply the chosen scale to every phase come close (`rc_diag_a93b_v12.json`):
   - scale on phases 0 and 1, phase 2 left at zero margin: −643.49;
   - scale on phase 1 only: −634.17.

   This suggests, but does not prove, that the first program's single-scale held-out points do not apply the chosen scale to all decisions. I could not identify its exact construction without reading it.
2. **The truth-phase per-phase held-out frontier Fps_cv** (Σ(F_F0 − Fps_cv): recount 969.3124246079614, first program 973.3655006031364). The same machinery on the estimated phase agrees exactly, so the shared LORO conventions (levels, frontier, zero-margin point, dropping of levels without a qualifying training triple) are the same in both programs. Variants I tried for the truth phase, none of which gives 973.37:
   - tie order g2-first, or highest index among caution ties: 969.31;
   - ignoring caution in ties: 971.07;
   - highest caution among ties: 970.37;
   - training sums formed as total minus left-out run, or by tensordot: 969.31 (bitwise unchanged);
   - zero-margin fallback at the no-choice level: 969.71;
   - lowest-caution fallback at the no-choice level: 969.88.

   Files: `rc_diag_a93d_v12_partial_output.txt`, `rc_diag_a93f_v12.json`, `rc_diag_a93g_v12.json`, and the variant stored in `RECOUNT_VALUES_v12.json`. This disagreement is unexplained. It is small in G_cv_vs_in (0.0036 of R) but above 1e-9.

Following Amendment 09 §3, these disagreements (above 1e-9) stop the revision for A9-3's held-out values until they are resolved.

## Definitional ambiguities and how I resolved them
1. **A9-3, levels with no qualifying training point.** At level 0 (= F0's full-sample zero-margin caution), no training triple and no training scale has caution at or below the level for 30 of the 35 left-out runs (26 for the estimated-phase triples). The amendment does not say what to do. I left out that level's held-out point, so the held-out frontier uses 200 points plus F0's zero-margin point. Variant applying the zero-margin choice instead: G_cv share 0.90385 (truth) / 0.99955 (estimated); G_cv_vs_in share 0.86821 / 0.96391 (stored under `variant_fallback_zero`). The first program reports the same counts (30/30, 26/30), and its estimated-phase value equals my primary treatment exactly.
2. **A9-3, choice rule.** Training wrong go is compared as counts, which is equivalent to rates because n_train is common. Training caution is 100·ΣS/ΣK, with S and K summed over the three phases. Ties are broken by lowest caution, then lowest flat index (g0·202² + g1·202 + g2). The single-scale choice uses the pooled per-run tables, so it does not depend on the phase source. The in-sample triple frontier and F0's single-scale frontier use the pooled levels of record; no zero-margin point is prepended to F0's own triples.
3. **A9-1(c), gridless points.**
   - A point is taken at g = 0 and just above every distinct critical value c in [0, 1000) at which some decision's selected row changes. That point holds on (c, next c], and on (last c, 1000] it equals the point at g = 1000.
   - Values that are NaN, negative or at least 1000 create no point.
   - Caution sums are accumulated exactly (integers in units of 2^-1100) and rounded once.
   - Sources other than F0 and E get F0's g = 0 point prepended through `eval_scoring`/`curves_w`, as the brief says.
   - Point counts agree with the first program for all 8 sources.
4. **A9-1(b).** u = round(0.05 j, 2), j = 1..20; critical scales are divided by 10^(0.025 u). Each offset source gets F0's g = 0 point prepended.
5. **A9-4(b), frontier point.** At each level the point taken is the one with the lowest wrong go among points with caution at or below the level, then the lowest caution, then the lowest point index. For CK3, A1 and N, point 0 is F0's g = 0 point.
6. **A9-4(b), time since stop.** The stop time is the `now` of the run's first decision, evaluated or not, with truth phase 2 (lead npz `phase`, identical to the A4 extract phase). In 5 runs (0008, 0025, 0031, 0033, 0034) that decision is not evaluated, but those runs have no evaluated phase-2 decision at all, so using the first evaluated phase-2 decision gives the same bins. All 35 runs reach phase 2. Lead-speed bins (extra) follow the amendment's edges, with "no estimate" separate (empty).
7. **A9-6.**
   - Shares are fractions of the population's decisions, averaged over the population's 201 levels.
   - Levels come from the W1 caution axis, as `stats_scored` with a supplied safe set gives.
   - The frontier point uses the rule in item 5.
   - The oracle O gets F0's g = 0 point prepended by the `curves_w` convention. In "all" and "moving", O's own point is the frontier point at all 201 levels, so "O as one selection" gives the same value; both are stored. In phase 0 (extra), F0's g = 0 point attains O's frontier at every level. The convention value and O as one selection are equal there (0.050147), and so is the first program's value.
   - NA and phases 0–2 were also computed and compared.
8. **A9-5.** Tuning runs are the 20 stems of `A4\dryrun\extract\*.npz`; k is identical between stored and extract files; no decision is in phase 3. Each phase's room uses its own levels. The weighted mean of the phase rooms uses the evaluated decisions per phase (378, 279, 2361) as weights.
9. **A9-3(b), estimated phase.** Phase 2 if lead_found and vhat ≤ 0.5; phase 1 if lead_found, vhat > 0.5, ahat_long finite and ≤ −1.0; otherwise phase 0. Every evaluated decision has a lead estimate.
10. **D(N, P).** Taken as D(N,F0) − D(P,F0), the frontier difference P − N, in decision-equivalents. It agrees with the first program's `D_N_minus_P_deceq`.

## Every compared value
Flag = absolute difference above 1e-9 (integers: any difference).

### A9-1a

| Value | Recount | First program | Abs. difference | Flag |
|---|---|---|---|---|
| all n | 8290 | 8290 | 0 |  |
| all R (pp) | 5.5567758313378812 | 5.5567758313378812 | 0 |  |
| all RR(N) | 0.0012204078106099951 | 0.0012204078106099951 | 0 |  |
| all RR(P) | 0.0014904095386210547 | 0.0014904095386210547 | 0 |  |
| all RR(N)-RR(P) | -0.0002700017280110596 | -0.00027000172801105966 | 5.42e-20 |  |
| all D(N,F0) dec-eq | 0.56218905472637137 | 0.56218905472637137 | 0 |  |
| all D(P,F0) dec-eq | 0.68656716417910779 | 0.68656716417910779 | 0 |  |
| moving n | 1863 | 1863 | 0 |  |
| moving R (pp) | 10.164155070060325 | 10.164155070060325 | 0 |  |
| moving RR(N) | -0.00013136806705026899 | -0.00013136806705026899 | 0 |  |
| moving RR(P) | 0.0021807099130343372 | 0.0021807099130343372 | 0 |  |
| moving RR(N)-RR(P) | -0.0023120779800846064 | -0.0023120779800846064 | 0 |  |
| moving D(N,F0) dec-eq | -0.024875621890548691 | -0.024875621890548691 | 0 |  |
| moving D(P,F0) dec-eq | 0.41293532338308414 | 0.41293532338308414 | 0 |  |
| phase0 n | 678 | 678 | 0 |  |
| phase0 R (pp) | 0.43147096376524441 | 0.43147096376524441 | 0 |  |
| phase0 RR(N) | 0.0051020408163265345 | 0.0051020408163265345 | 0 |  |
| phase0 RR(P) | 0.0051020408163265345 | 0.0051020408163265345 | 0 |  |
| phase0 RR(N)-RR(P) | 0 | 0 | 0 |  |
| phase0 D(N,F0) dec-eq | 0.014925373134328363 | 0.014925373134328363 | 0 |  |
| phase0 D(P,F0) dec-eq | 0.014925373134328363 | 0.014925373134328363 | 0 |  |
| phase1 n | 755 | 755 | 0 |  |
| phase1 R (pp) | 15.587624789957497 | 15.587624789957497 | 0 |  |
| phase1 RR(N) | -0.0024519129148171735 | -0.0024519129148171735 | 0 |  |
| phase1 RR(P) | -0.001437328260410071 | -0.001437328260410071 | 0 |  |
| phase1 RR(N)-RR(P) | -0.0010145846544071025 | -0.0010145846544071025 | 0 |  |
| phase1 D(N,F0) dec-eq | -0.28855721393034944 | -0.28855721393034944 | 0 |  |
| phase1 D(P,F0) dec-eq | -0.16915422885572254 | -0.16915422885572254 | 0 |  |
| phase2 n | 6857 | 6857 | 0 |  |
| phase2 R (pp) | 0.82060167298261499 | 0.82060167298261499 | 0 |  |
| phase2 RR(N) | 0.0018567639257294458 | 0.0018567639257294458 | 0 |  |
| phase2 RR(P) | 0.0028293545534924876 | 0.0028293545534924876 | 0 |  |
| phase2 RR(N)-RR(P) | -0.00097259062776304181 | -0.00097259062776304203 | 2.17e-19 |  |
| phase2 D(N,F0) dec-eq | 0.10447761194029866 | 0.10447761194029866 | 0 |  |
| phase2 D(P,F0) dec-eq | 0.15920398009950268 | 0.15920398009950268 | 0 |  |

### A9-1b

| Value | Recount | First program | Abs. difference | Flag |
|---|---|---|---|---|
| RR offset u=0.05 | 0.00016200103680663762 | 0.00016200103680663762 | 0 |  |
| RR offset u=0.10 | 0.00046440297217902212 | 0.00046440297217902212 | 0 |  |
| RR offset u=0.15 | 0.0006048038707447737 | 0.0006048038707447737 | 0 |  |
| RR offset u=0.20 | 0.001004406428201146 | 0.001004406428201146 | 0 |  |
| RR offset u=0.25 | 0.0010368066355624771 | 0.0010368066355624771 | 0 |  |
| RR offset u=0.30 | 0.0010044064282011497 | 0.0010044064282011497 | 0 |  |
| RR offset u=0.35 | 0.0012312078797304393 | 0.0012312078797304393 | 0 |  |
| RR offset u=0.40 | 0.0015120096768619392 | 0.0015120096768619392 | 0 |  |
| RR offset u=0.45 | 0.0016848107827890195 | 0.0016848107827890195 | 0 |  |
| RR offset u=0.50 | 0.0011124071194055722 | 0.0011124071194055722 | 0 |  |
| RR offset u=0.55 | 0.0014580093312597288 | 0.0014580093312597288 | 0 |  |
| RR offset u=0.60 | 0.0017280110592707855 | 0.0017280110592707855 | 0 |  |
| RR offset u=0.65 | 0.0010692068429238 | 0.0010692068429238 | 0 |  |
| RR offset u=0.70 | 0.0013500086400553008 | 0.0013500086400553008 | 0 |  |
| RR offset u=0.75 | 0.0012744081562122075 | 0.0012744081562122075 | 0 |  |
| RR offset u=0.80 | 0.0011016070502851275 | 0.0011016070502851275 | 0 |  |
| RR offset u=0.85 | 0.00092880594435804781 | 0.00092880594435804781 | 0 |  |
| RR offset u=0.90 | 0.00064800414722654832 | 0.00064800414722654832 | 0 |  |
| RR offset u=0.95 | 1.0800069120441885e-05 | 1.0800069120441885e-05 | 0 |  |
| RR offset u=1.00 | 0 | 0 | 0 |  |
| RR offset min | 0 | 0 | 0 |  |
| RR offset max | 0.0017280110592707855 | 0.0017280110592707855 | 0 |  |

### A9-1c

| Value | Recount | First program | Abs. difference | Flag |
|---|---|---|---|---|
| all R (pp) | 5.5125458353587913 | 5.5125458353587913 | 0 |  |
| all RR(N) | -0.00041369549833977597 | -0.00041369549833977597 | 0 |  |
| all RR(P) | 0 | 0 | 0 |  |
| all RR(NA) | 0.01506722551848021 | 0.01506722551848021 | 0 |  |
| all RR(A1) | 0.38239616787327857 | 0.38239616787327857 | 0 |  |
| all RR(CK3) | 0.83660116487942948 | 0.83660116487942948 | 0 |  |
| all RR(Q) | -0.0023950792009144913 | -0.0023950792009144913 | 0 |  |
| all D(N,F0) dec-eq | -0.18905472636815979 | -0.18905472636815979 | 0 |  |
| all D(P,F0) dec-eq | 0 | 0 | 0 |  |
| all D(N,P) dec-eq | -0.18905472636815979 | -0.18905472636815979 | 0 |  |
| moving R (pp) | 9.9729479280997051 | 9.9729479280997051 | 0 |  |
| moving RR(N) | -0.0023028517873878674 | -0.0023028517873878674 | 0 |  |
| moving RR(P) | 0 | 0 | 0 |  |
| moving RR(NA) | 0.013736778685232298 | 0.013736778685232298 | 0 |  |
| moving RR(A1) | 0.29141786049002544 | 0.29141786049002544 | 0 |  |
| moving RR(CK3) | 0.46488151024233498 | 0.46488151024233498 | 0 |  |
| moving RR(Q) | -0.00053554692729950294 | -0.00053554692729950294 | 0 |  |
| moving D(N,F0) dec-eq | -0.42786069651741254 | -0.42786069651741254 | 0 |  |
| moving D(P,F0) dec-eq | 0 | 0 | 0 |  |
| moving D(N,P) dec-eq | -0.42786069651741254 | -0.42786069651741254 | 0 |  |
| phase0 R (pp) | 0.42046405142429433 | 0.42046405142429433 | 0 |  |
| phase0 RR(N) | 0.0017452006980802808 | 0.0017452006980802808 | 0 |  |
| phase0 RR(P) | 0 | 0 | 0 |  |
| phase0 RR(NA) | 0.0017452006980802808 | 0.0017452006980802808 | 0 |  |
| phase0 RR(A1) | -0.12216404886561959 | -0.12216404886561959 | 0 |  |
| phase0 RR(CK3) | -0.58464223385689384 | -0.58464223385689384 | 0 |  |
| phase0 RR(Q) | 0.001745200698080265 | 0.001745200698080265 | 0 |  |
| phase0 D(N,F0) dec-eq | 0.0049751243781094552 | 0.0049751243781094552 | 0 |  |
| phase0 D(P,F0) dec-eq | 0 | 0 | 0 |  |
| phase0 D(N,P) dec-eq | 0.0049751243781094552 | 0.0049751243781094552 | 0 |  |
| phase1 R (pp) | 15.237718691311652 | 15.237718691311652 | 0 |  |
| phase1 RR(N) | 0.0001729804532087838 | 0.0001729804532087838 | 0 |  |
| phase1 RR(P) | 0 | 0 | 0 |  |
| phase1 RR(NA) | -0.0054488842760768135 | -0.0054488842760768135 | 0 |  |
| phase1 RR(A1) | -0.057472755578619618 | -0.057472755578619618 | 0 |  |
| phase1 RR(CK3) | 0.59600415153087716 | 0.59600415153087716 | 0 |  |
| phase1 RR(Q) | 0.00038920601971975818 | 0.00038920601971975818 | 0 |  |
| phase1 D(N,F0) dec-eq | 0.019900497512437394 | 0.019900497512437394 | 0 |  |
| phase1 D(P,F0) dec-eq | 0 | 0 | 0 |  |
| phase1 D(N,P) dec-eq | 0.019900497512437394 | 0.019900497512437394 | 0 |  |
| phase2 R (pp) | 0.79564261237200318 | 0.79564261237200318 | 0 |  |
| phase2 RR(N) | -0.00091190953857377458 | -0.00091190953857377458 | 0 |  |
| phase2 RR(P) | 0 | 0 | 0 |  |
| phase2 RR(NA) | 0.079883275579062565 | 0.079883275579062565 | 0 |  |
| phase2 RR(A1) | 0.76226518329381732 | 0.76226518329381732 | 0 |  |
| phase2 RR(CK3) | 1.0223417836950575 | 1.0223417836950575 | 0 |  |
| phase2 RR(Q) | -0.004833120554440999 | -0.004833120554440999 | 0 |  |
| phase2 D(N,F0) dec-eq | -0.049751243781094585 | -0.049751243781094585 | 0 |  |
| phase2 D(P,F0) dec-eq | 0 | 0 | 0 |  |
| phase2 D(N,P) dec-eq | -0.049751243781094585 | -0.049751243781094585 | 0 |  |
| number of gridless points F0 | 61770 | 61770 | 0 |  |
| number of gridless points E | 53722 | 53722 | 0 |  |
| number of gridless points N | 61805 | 61805 | 0 |  |
| number of gridless points P | 61770 | 61770 | 0 |  |
| number of gridless points NA | 61805 | 61805 | 0 |  |
| number of gridless points A1 | 62027 | 62027 | 0 |  |
| number of gridless points CK3 | 58908 | 58908 | 0 |  |
| number of gridless points Q | 62018 | 62018 | 0 |  |

### A9-3

| Value | Recount | First program | Abs. difference | Flag |
|---|---|---|---|---|
| R (pp), pooled | 5.5567758313378812 | 5.5567758313378812 | 0 |  |
| truth phase in-sample gain (pp) | 4.9609011636629878 | 4.9609011636629878 | 0 |  |
| truth phase in-sample gain share of R | 0.89276611370312797 | 0.89276611370312797 | 0 |  |
| truth phase LORO G_cv share | 0.90349058233972712 | 0.29764990495939181 | 0.606 | **DIFFERS** |
| truth phase LORO G_cv (pp) | 5.0204946317867831 | 1.6539737980783655 | 3.37 | **DIFFERS** |
| truth phase LORO G_cv_vs_in share | 0.86785035424226731 | 0.87147917746673609 | 0.00363 | **DIFFERS** |
| truth phase LORO G_cv_vs_in (pp) | 4.8224498736714496 | 4.8426144308613752 | 0.0202 | **DIFFERS** |
| truth phase LORO sum(F1_cv - F1_in) | 39.806996381182138 | -640.91676718938481 | 681 | **DIFFERS** |
| truth phase LORO run-level pairs without a qualifying triple | 30 | 30 | 0 |  |
| truth phase LORO run-level pairs without a qualifying single scale | 30 | 30 | 0 |  |
| estimated phase in-sample gain (pp) | 5.4658552832940241 | 5.4658552832940241 | 0 |  |
| estimated phase in-sample gain share of R | 0.98363789528252987 | 0.98363789528252987 | 0 |  |
| estimated phase LORO G_cv share | 0.99933039571453286 | 0.38986089510972877 | 0.609 | **DIFFERS** |
| estimated phase LORO G_cv (pp) | 5.553054990427837 | 2.1663695995294936 | 3.39 | **DIFFERS** |
| estimated phase LORO G_cv_vs_in share | 0.96369016761707305 | 0.96369016761707305 | 0 |  |
| estimated phase LORO G_cv_vs_in (pp) | 5.3550102323125026 | 5.3550102323125026 | 0 |  |
| estimated phase LORO sum(F1_cv - F1_in) | 39.806996381182138 | -640.91676718938481 | 681 | **DIFFERS** |
| estimated phase LORO run-level pairs without a qualifying triple | 26 | 26 | 0 |  |
| estimated phase LORO run-level pairs without a qualifying single scale | 30 | 30 | 0 |  |
| estimated phase agreement with truth | 0.95645355850422198 | 0.95645355850422198 | 0 |  |
| confusion truth 0 / estimated 0 | 675 | 675 | 0 |  |
| confusion truth 0 / estimated 1 | 3 | 3 | 0 |  |
| confusion truth 0 / estimated 2 | 0 | 0 | 0 |  |
| confusion truth 1 / estimated 0 | 226 | 226 | 0 |  |
| confusion truth 1 / estimated 1 | 529 | 529 | 0 |  |
| confusion truth 1 / estimated 2 | 0 | 0 | 0 |  |
| confusion truth 2 / estimated 0 | 4 | 4 | 0 |  |
| confusion truth 2 / estimated 1 | 128 | 128 | 0 |  |
| confusion truth 2 / estimated 2 | 6725 | 6725 | 0 |  |

### A9-4b

| Value | Recount | First program | Abs. difference | Flag |
|---|---|---|---|---|
| all E total (dec-eq) | 460.65671641791045 | 460.65671641791045 | 0 |  |
| all E D dec-eq of record | 460.65671641791033 | 460.65671641791033 | 0 |  |
| all E time since stop before stop | 419.08955223880594 | 419.08955223880594 | 0 |  |
| all E time since stop 0-1 s | 41.711442786069647 | 41.711442786069647 | 0 |  |
| all E time since stop 1-2 s | -0.14427860696517411 | -0.14427860696517411 | 0 |  |
| all E time since stop 2-5 s | 0 | 0 | 0 |  |
| all E time since stop 5-10 s | 0 | 0 | 0 |  |
| all E time since stop >=10 s | 0 | 0 | 0 |  |
| all E lead speed estimate <=0.5 | 2.3582089552238807 | 2.3582089552238807 | 0 |  |
| all E lead speed estimate 0.5-1 | 5.0746268656716413 | 5.0746268656716413 | 0 |  |
| all E lead speed estimate 1-2 | 18.069651741293534 | 18.069651741293534 | 0 |  |
| all E lead speed estimate >2 | 435.15422885572133 | 435.15422885572133 | 0 |  |
| all CK3 total (dec-eq) | 383.02487562189043 | 383.02487562189043 | 0 |  |
| all CK3 D dec-eq of record | 383.02487562189066 | 383.02487562189066 | 0 |  |
| all CK3 time since stop before stop | 345.8656716417911 | 345.8656716417911 | 0 |  |
| all CK3 time since stop 0-1 s | 37.432835820895527 | 37.432835820895527 | 0 |  |
| all CK3 time since stop 1-2 s | -0.27363184079601993 | -0.27363184079601993 | 0 |  |
| all CK3 time since stop 2-5 s | 0 | 0 | 0 |  |
| all CK3 time since stop 5-10 s | 0 | 0 | 0 |  |
| all CK3 time since stop >=10 s | 0 | 0 | 0 |  |
| all CK3 lead speed estimate <=0.5 | -1.8905472636815923 | -1.8905472636815923 | 0 |  |
| all CK3 lead speed estimate 0.5-1 | 5.2786069651741299 | 5.2786069651741299 | 0 |  |
| all CK3 lead speed estimate 1-2 | 18.860696517412933 | 18.860696517412933 | 0 |  |
| all CK3 lead speed estimate >2 | 360.77611940298505 | 360.77611940298505 | 0 |  |
| all A1 total (dec-eq) | 173.11442786069651 | 173.11442786069651 | 0 |  |
| all A1 D dec-eq of record | 173.11442786069651 | 173.11442786069651 | 0 |  |
| all A1 time since stop before stop | 143.20398009950247 | 143.20398009950247 | 0 |  |
| all A1 time since stop 0-1 s | 30.014925373134325 | 30.014925373134325 | 0 |  |
| all A1 time since stop 1-2 s | -0.10447761194029849 | -0.10447761194029849 | 0 |  |
| all A1 time since stop 2-5 s | 0 | 0 | 0 |  |
| all A1 time since stop 5-10 s | 0 | 0 | 0 |  |
| all A1 time since stop >=10 s | 0 | 0 | 0 |  |
| all A1 lead speed estimate <=0.5 | 1.3432835820895526 | 1.3432835820895526 | 0 |  |
| all A1 lead speed estimate 0.5-1 | 3.6666666666666665 | 3.6666666666666665 | 0 |  |
| all A1 lead speed estimate 1-2 | 13.412935323383081 | 13.412935323383081 | 0 |  |
| all A1 lead speed estimate >2 | 154.6915422885572 | 154.6915422885572 | 0 |  |
| all N total (dec-eq) | 0.56218905472636826 | 0.56218905472636826 | 0 |  |
| all N D dec-eq of record | 0.56218905472637137 | 0.56218905472637137 | 0 |  |
| all N time since stop before stop | 0.41791044776119407 | 0.41791044776119407 | 0 |  |
| all N time since stop 0-1 s | 0.14427860696517408 | 0.14427860696517408 | 0 |  |
| all N time since stop 1-2 s | 0 | 0 | 0 |  |
| all N time since stop 2-5 s | 0 | 0 | 0 |  |
| all N time since stop 5-10 s | 0 | 0 | 0 |  |
| all N time since stop >=10 s | 0 | 0 | 0 |  |
| all N lead speed estimate <=0.5 | 0 | 0 | 0 |  |
| all N lead speed estimate 0.5-1 | 0 | 0 | 0 |  |
| all N lead speed estimate 1-2 | 0.054726368159203974 | 0.054726368159203974 | 0 |  |
| all N lead speed estimate >2 | 0.50746268656716431 | 0.50746268656716431 | 0 |  |
| after_stop E total (dec-eq) | 56.268656716417922 | 56.268656716417922 | 0 |  |
| after_stop E D dec-eq of record | 56.268656716417908 | 56.268656716417908 | 0 |  |
| after_stop E time since stop before stop | 0 | 0 | 0 |  |
| after_stop E time since stop 0-1 s | 56.114427860696523 | 56.114427860696523 | 0 |  |
| after_stop E time since stop 1-2 s | 0.154228855721393 | 0.154228855721393 | 0 |  |
| after_stop E time since stop 2-5 s | 0 | 0 | 0 |  |
| after_stop E time since stop 5-10 s | 0 | 0 | 0 |  |
| after_stop E time since stop >=10 s | 0 | 0 | 0 |  |
| after_stop E lead speed estimate <=0.5 | 4.0995024875621882 | 4.0995024875621882 | 0 |  |
| after_stop E lead speed estimate 0.5-1 | 6.6616915422885574 | 6.6616915422885574 | 0 |  |
| after_stop E lead speed estimate 1-2 | 18.587064676616919 | 18.587064676616919 | 0 |  |
| after_stop E lead speed estimate >2 | 26.920398009950254 | 26.920398009950254 | 0 |  |
| after_stop CK3 total (dec-eq) | 55.895522388059703 | 55.895522388059703 | 0 |  |
| after_stop CK3 D dec-eq of record | 55.895522388059703 | 55.895522388059703 | 0 |  |
| after_stop CK3 time since stop before stop | 0 | 0 | 0 |  |
| after_stop CK3 time since stop 0-1 s | 55.895522388059703 | 55.895522388059703 | 0 |  |
| after_stop CK3 time since stop 1-2 s | 0 | 0 | 0 |  |
| after_stop CK3 time since stop 2-5 s | 0 | 0 | 0 |  |
| after_stop CK3 time since stop 5-10 s | 0 | 0 | 0 |  |
| after_stop CK3 time since stop >=10 s | 0 | 0 | 0 |  |
| after_stop CK3 lead speed estimate <=0.5 | 0.0099502487562189053 | 0.0099502487562189053 | 0 |  |
| after_stop CK3 lead speed estimate 0.5-1 | 8.3034825870646749 | 8.3034825870646749 | 0 |  |
| after_stop CK3 lead speed estimate 1-2 | 20.776119402985074 | 20.776119402985074 | 0 |  |
| after_stop CK3 lead speed estimate >2 | 26.805970149253731 | 26.805970149253731 | 0 |  |
| after_stop A1 total (dec-eq) | 39.512437810945279 | 39.512437810945279 | 0 |  |
| after_stop A1 D dec-eq of record | 39.512437810945272 | 39.512437810945272 | 0 |  |
| after_stop A1 time since stop before stop | 0 | 0 | 0 |  |
| after_stop A1 time since stop 0-1 s | 39.671641791044784 | 39.671641791044784 | 0 |  |
| after_stop A1 time since stop 1-2 s | -0.15920398009950248 | -0.15920398009950248 | 0 |  |
| after_stop A1 time since stop 2-5 s | 0 | 0 | 0 |  |
| after_stop A1 time since stop 5-10 s | 0 | 0 | 0 |  |
| after_stop A1 time since stop >=10 s | 0 | 0 | 0 |  |
| after_stop A1 lead speed estimate <=0.5 | 1.6567164179104477 | 1.6567164179104477 | 0 |  |
| after_stop A1 lead speed estimate 0.5-1 | 4.8258706467661705 | 4.8258706467661705 | 0 |  |
| after_stop A1 lead speed estimate 1-2 | 14.129353233830845 | 14.129353233830845 | 0 |  |
| after_stop A1 lead speed estimate >2 | 18.900497512437809 | 18.900497512437809 | 0 |  |
| after_stop N total (dec-eq) | 0.10447761194029852 | 0.10447761194029852 | 0 |  |
| after_stop N D dec-eq of record | 0.10447761194029866 | 0.10447761194029866 | 0 |  |
| after_stop N time since stop before stop | 0 | 0 | 0 |  |
| after_stop N time since stop 0-1 s | 0.10447761194029852 | 0.10447761194029852 | 0 |  |
| after_stop N time since stop 1-2 s | 0 | 0 | 0 |  |
| after_stop N time since stop 2-5 s | 0 | 0 | 0 |  |
| after_stop N time since stop 5-10 s | 0 | 0 | 0 |  |
| after_stop N time since stop >=10 s | 0 | 0 | 0 |  |
| after_stop N lead speed estimate <=0.5 | 0.029850746268656712 | 0.029850746268656712 | 0 |  |
| after_stop N lead speed estimate 0.5-1 | -0.014925373134328358 | -0.014925373134328358 | 0 |  |
| after_stop N lead speed estimate 1-2 | 0.0099502487562189088 | 0.0099502487562189088 | 0 |  |
| after_stop N lead speed estimate >2 | 0.079601990049751242 | 0.079601990049751242 | 0 |  |

### A9-5

| Value | Recount | First program | Abs. difference | Flag |
|---|---|---|---|---|
| number of tuning runs | 20 | 20 | 0 |  |
| all n | 3018 | 3018 | 0 |  |
| all R (pp) | 1.1803144647867356 | 1.1803144647867356 | 0 |  |
| all RR(N) | 0.0022346368715083793 | 0.0022346368715083793 | 0 |  |
| all RR(NA) | 0.063268156424580987 | 0.063268156424580987 | 0 |  |
| all RR(A1) | 0.2451117318435754 | 0.2451117318435754 | 0 |  |
| all RR(CK3) | 0.37681564245810051 | 0.37681564245810051 | 0 |  |
| all RR(Q) | 0.0037709497206703914 | 0.0037709497206703914 | 0 |  |
| moving n | 897 | 897 | 0 |  |
| moving R (pp) | 4.0527573947431179 | 4.0527573947431179 | 0 |  |
| moving RR(N) | -2.7257973260948832e-19 | -2.7257973260948832e-19 | 0 |  |
| moving RR(NA) | 0.067743259887778851 | 0.067743259887778851 | 0 |  |
| moving RR(A1) | 0.25359244560010952 | 0.25359244560010952 | 0 |  |
| moving RR(CK3) | 0.15108799781031892 | 0.15108799781031892 | 0 |  |
| moving RR(Q) | 0.0023265361981661412 | 0.0023265361981661412 | 0 |  |
| phase0 n | 378 | 378 | 0 |  |
| phase0 R (pp) | 0.071073205401563616 | 0.071073205401563616 | 0 |  |
| phase0 RR(N) | -7.771561172376095e-18 | -7.771561172376095e-18 | 0 |  |
| phase0 RR(NA) | -7.771561172376095e-18 | -7.771561172376095e-18 | 0 |  |
| phase0 RR(A1) | -0.074074074074074098 | -0.074074074074074098 | 0 |  |
| phase0 RR(CK3) | -5.2222222222222223 | -5.2222222222222223 | 0 |  |
| phase0 RR(Q) | 0.074074074074074056 | 0.074074074074074056 | 0 |  |
| phase1 n | 279 | 279 | 0 |  |
| phase1 R (pp) | 10.14283421601669 | 10.14283421601669 | 0 |  |
| phase1 RR(N) | 0.0035161744022503372 | 0.0035161744022503372 | 0 |  |
| phase1 RR(NA) | 0.079817158931083002 | 0.079817158931083002 | 0 |  |
| phase1 RR(A1) | 0.062587904360056262 | 0.062587904360056262 | 0 |  |
| phase1 RR(CK3) | 0.30098452883263016 | 0.30098452883263016 | 0 |  |
| phase1 RR(Q) | 0.011603375527426147 | 0.011603375527426147 | 0 |  |
| phase2 n | 2361 | 2361 | 0 |  |
| phase2 R (pp) | 1.1996350311129655 | 1.1996350311129655 | 0 |  |
| phase2 RR(N) | -0.0010539258738802057 | -0.0010539258738802057 | 0 |  |
| phase2 RR(NA) | -0.0015808888108203084 | -0.0015808888108203084 | 0 |  |
| phase2 RR(A1) | 0.062532935183558763 | 0.062532935183558763 | 0 |  |
| phase2 RR(CK3) | 0.93676444756718791 | 0.93676444756718791 | 0 |  |
| phase2 RR(Q) | -0.03460389952573336 | -0.03460389952573336 | 0 |  |
| decision-weighted mean phase room (pp) | 1.8850413274911062 | 1.8850413274911064 | 2.22e-16 |  |
| pooled room / weighted phase room | 0.62614779186707481 | 0.62614779186707481 | 0 |  |

### A9-6

| Value | Recount | First program | Abs. difference | Flag |
|---|---|---|---|---|
| all F0 share W1-unsafe but stop-safe | 0.058171146679149487 | 0.058171146679149487 | 0 |  |
| all E share W1-unsafe but stop-safe | 0.005510445360651507 | 0.005510445360651507 | 0 |  |
| all N share W1-unsafe but stop-safe | 0.058175947764194706 | 0.058175947764194706 | 0 |  |
| all NA share W1-unsafe but stop-safe | 0.057258340384926991 | 0.057258340384926991 | 0 |  |
| all A1 share W1-unsafe but stop-safe | 0.046676148809630974 | 0.046676148809630974 | 0 |  |
| all CK3 share W1-unsafe but stop-safe | 0.03286762808394697 | 0.03286762808394697 | 0 |  |
| all O share W1-unsafe but stop-safe | 0.72255729794933654 | 0.72255729794933654 | 0 |  |
| moving F0 share W1-unsafe but stop-safe | 0.19021371937948475 | 0.19021371937948475 | 0 |  |
| moving E share W1-unsafe but stop-safe | 0.0087431869103222482 | 0.0087431869103222482 | 0 |  |
| moving N share W1-unsafe but stop-safe | 0.19186408269975938 | 0.19186408269975938 | 0 |  |
| moving NA share W1-unsafe but stop-safe | 0.18678747967088874 | 0.18678747967088874 | 0 |  |
| moving A1 share W1-unsafe but stop-safe | 0.17766508306561662 | 0.17766508306561662 | 0 |  |
| moving CK3 share W1-unsafe but stop-safe | 0.15273338086806973 | 0.15273338086806973 | 0 |  |
| moving O share W1-unsafe but stop-safe | 0.51583467525496507 | 0.51583467525496507 | 0 |  |
| phase0 F0 share W1-unsafe but stop-safe | 0.050147492625368731 | 0.050147492625368731 | 0 |  |
| phase0 E share W1-unsafe but stop-safe | 0.050147492625368731 | 0.050147492625368731 | 0 |  |
| phase0 N share W1-unsafe but stop-safe | 0.050147492625368731 | 0.050147492625368731 | 0 |  |
| phase0 NA share W1-unsafe but stop-safe | 0.050147492625368731 | 0.050147492625368731 | 0 |  |
| phase0 A1 share W1-unsafe but stop-safe | 0.050147492625368731 | 0.050147492625368731 | 0 |  |
| phase0 CK3 share W1-unsafe but stop-safe | 0.050147492625368731 | 0.050147492625368731 | 0 |  |
| phase0 O share W1-unsafe but stop-safe | 0.050147492625368731 | 0.050147492625368731 | 0 |  |
| phase1 F0 share W1-unsafe but stop-safe | 0.41744917795130304 | 0.41744917795130304 | 0 |  |
| phase1 E share W1-unsafe but stop-safe | 0.65695364238410592 | 0.65695364238410592 | 0 |  |
| phase1 N share W1-unsafe but stop-safe | 0.42240453362327435 | 0.42240453362327435 | 0 |  |
| phase1 NA share W1-unsafe but stop-safe | 0.4104642351158117 | 0.4104642351158117 | 0 |  |
| phase1 A1 share W1-unsafe but stop-safe | 0.37920991071134391 | 0.37920991071134391 | 0 |  |
| phase1 CK3 share W1-unsafe but stop-safe | 0.40471813119831312 | 0.40471813119831312 | 0 |  |
| phase1 O share W1-unsafe but stop-safe | 0.70198675496688745 | 0.70198675496688745 | 0 |  |
| phase2 F0 share W1-unsafe but stop-safe | 0.01211385104519694 | 0.01211385104519694 | 0 |  |
| phase2 E share W1-unsafe but stop-safe | 0.0033244888290064915 | 0.0033244888290064915 | 0 |  |
| phase2 N share W1-unsafe but stop-safe | 0.012144324316872688 | 0.012144324316872688 | 0 |  |
| phase2 NA share W1-unsafe but stop-safe | 0.011777919502676206 | 0.011777919502676206 | 0 |  |
| phase2 A1 share W1-unsafe but stop-safe | 0.0072083798594891951 | 0.0072083798594891951 | 0 |  |
| phase2 CK3 share W1-unsafe but stop-safe | 0.0043148701584682682 | 0.0043148701584682682 | 0 |  |
| phase2 O share W1-unsafe but stop-safe | 0.79130815225317197 | 0.79130815225317197 | 0 |  |

### A9-7

| Value | Recount | First program | Abs. difference | Flag |
|---|---|---|---|---|
| all R (pp) | 5.5567758313378812 | 5.5567758313378812 | 0 |  |
| all RR(TG2) | 0.31421721099015038 | 0.31421721099015038 | 0 |  |
| all RR(TG1) | 0.38730127872818393 | 0.38730127872818393 | 0 |  |
| all RR(TG4) | 0.21293416277864183 | 0.21293416277864183 | 0 |  |
| all D(TG2,F0) dec-eq | 144.74626865671641 | 144.74626865671641 | 0 |  |
| moving R (pp) | 10.164155070060325 | 10.164155070060325 | 0 |  |
| moving RR(TG2) | 0.16780956885000398 | 0.16780956885000398 | 0 |  |
| moving RR(TG1) | 0.18491369117994799 | 0.18491369117994799 | 0 |  |
| moving RR(TG4) | 0.11576154068469038 | 0.11576154068469038 | 0 |  |
| moving D(TG2,F0) dec-eq | 31.776119402985078 | 31.776119402985078 | 0 |  |
| phase0 R (pp) | 0.43147096376524441 | 0.43147096376524441 | 0 |  |
| phase0 RR(TG2) | -0.48129251700680276 | -0.48129251700680276 | 0 |  |
| phase0 RR(TG1) | -0.72619047619047661 | -0.72619047619047661 | 0 |  |
| phase0 RR(TG4) | -0.25850340136054428 | -0.25850340136054428 | 0 |  |
| phase0 D(TG2,F0) dec-eq | -1.4079601990049748 | -1.4079601990049748 | 0 |  |
| phase1 R (pp) | 15.587624789957497 | 15.587624789957497 | 0 |  |
| phase1 RR(TG2) | 0.087888395688015236 | 0.087888395688015236 | 0 |  |
| phase1 RR(TG1) | 0.053096596913971665 | 0.053096596913971665 | 0 |  |
| phase1 RR(TG4) | 0.092707672796448939 | 0.092707672796448939 | 0 |  |
| phase1 D(TG2,F0) dec-eq | 10.343283582089553 | 10.343283582089553 | 0 |  |
| phase2 R (pp) | 0.82060167298261499 | 0.82060167298261499 | 0 |  |
| phase2 RR(TG2) | 0.16127320954907165 | 0.16127320954907165 | 0 |  |
| phase2 RR(TG1) | 0.18505747126436781 | 0.18505747126436781 | 0 |  |
| phase2 RR(TG4) | 0.066224580017683526 | 0.066224580017683526 | 0 |  |
| phase2 D(TG2,F0) dec-eq | 9.0746268656716431 | 9.0746268656716431 | 0 |  |