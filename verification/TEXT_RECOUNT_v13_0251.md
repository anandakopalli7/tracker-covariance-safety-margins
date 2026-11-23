# TEXT RECOUNT v13

Recount by **Claude Sonnet 5.5** (a different model from the writer, Claude Opus 5.5). Script: `TEXT_RECOUNT_v13.py` (this folder). Frozen copies: `out\freeze_v13\MANUSCRIPT_v13.md` (sha256 `14783e9b39ff992f3c5358f9ca7a76b76ac63fac36afbf811d7123f8398b75f6`) and `SUPPLEMENT_v13.md` (sha256 `1038b2577f6b023970ceb89c2e59aaea4049b6070ce26da0817ce198a1241b71`).

## 1. Totals (main text: Abstract, I, III-C/E counts, V-VII, Tables II-V)

- Numbers checked: **372** (each interval end counts once; "n.c." entries count once; counts, percentages and shares included)
- Agreeing: **372**
- Differing: **0**
- Fragments located verbatim in the frozen manuscript: 116 of 116 (a fragment not found would mean my transcription, not the text, is wrong)
- n.t. cells (cut-in and real-log columns, Table II): 20 underlying keys checked to be null or NaN; not null: []
- Export value equals its second-program (A_RECOUNT) value, for each of the 201 keys read (counts exactly, others within 1e-9): **201 agree, 0 differ**
- Hashes in Section IV-E: 85787f3d…8f6b matches the file and is in the text; 02048a43…a4df matches the file and is in the text; 94e06ed6…c0a6 matches the file and is in the text; LOCK_A10_1.txt carries the amendment hash matches the file and is in the text

## 2. Differences

None among the main-text numbers.

## 3. Hypothesis statuses recomputed from the interval ends (A10 rules, delta = 0.05)

| Item | Recomputed | Text / table |  Agrees |
|---|---|---|---|
| H0 pass -> "there is room (confirmed)" | as stated | V-A para 1, Table II (C) | yes |
| H1 pass -> "detects rank information ... (confirmed)" | as stated | V-A para 1, Table II | yes |
| H2 pass -> "equivalent ... within 5% of the room (confirmed)" | as stated | V-A para 2, Table II (C) | yes |
| H3 = amplitude-limited, passes; IMM "(confirmed)"; barely varies | as stated | V-B, Table II classification | yes |
| H4 pass -> PS "transfers (confirmed)" | as stated | V-A para 3, Table II (C) | yes |
| H5 pass -> CK3 "most of it (confirmed)" | as stated | V-A para 3, Table II (C) | yes |
| K0 fail -> "no measurable room at the event ... nothing is tested" (F) | as stated | V-A para 2, Table II (F) | yes |
| F-H0 fail -> "no measurable room ... nothing is tested on the logs" (F) | as stated | V-A para 2, Table II (F) | yes |
| E-H1 = safer at no extra cost (V-C, Abstract, VII) | as stated | V-C, Abstract | yes |
| E-H2 = equivalent | as stated | V-C, Table IV | yes |
| E-H3 = equivalent (IMM equivalent to own class average) | as stated | V-B, V-C | yes |
| Higher level: CK3, TG, PS inconclusive; N, IMM equivalent | as stated | Table IV | yes |
| Lower level: TG, PS safer at no extra cost | as stated | Table IV | yes |
| E3b: CK3 and PS inconclusive for const and mild, safer at a cost for stopgo | as stated | V-C para 2 | yes |
| D-H1/D-H2 = costs progress for all three variants | as stated | V-D, Table V, Abstract | yes |
| B3/B4 rule -> mechanism persists | as stated | V-D filter tuning | yes |
| B7 rate rule -> largely a consequence of the 2 Hz update | as stated | V-D update rate | yes |
| B7 N rule -> share stays inside the margin at every rate and latency | as stated | V-D update rate | yes |
| B6: all three terciles evaluable (range stated "0.055 to 0.168") | as stated | V-D commitment | yes |
| Transfer: N inside (-d,d) in every set, order CK3>AM>TG>NA>N | as stated | V-D recording policy | yes |
| Table III classification of the IMM = amplitude-limited | as stated | Table II, V-B | yes |

Recomputed values: H0 = pass; H1 = pass; H2 = pass; H3 = amplitude-limited; H3.barely = True; H4 = pass; H5 = pass; K0 = fail; K1 = not_run; K2 = not_run; F-H0 = fail; F-H1 = not_run; F-H2 (if it had been run) = inconclusive; E-H1 = safer at no extra cost; E-H2 = equivalent; E-H3 = equivalent; B3/B4 CV2 = mechanism persists; B3/B4 CA = mechanism persists; B3/B4 = mechanism persists; B7 rate = largely a consequence of the 2 Hz update; B7 N inside (-d,d) at all 8 rate/latency cells = holds; B7 identity = pass; B6 terciles evaluable (den0>=10) = all; TRANSFER order CK3>AM>TG>NA>N in every set where defined = True; TRANSFER N inside (-d,d) in every set = True

Confirmation along the lead-braking sequence: H0=True, H1=True, H2=True, H3=True, H4=True, H5=True

The packages' own status keys against my recomputation:

| Key | Package value | Recomputed | Agree |
|---|---|---|---|
| LB.H0..H5 | ['pass', 'pass', 'pass', 'amplitude_limited', 'pass', 'pass'] | ['pass', 'pass', 'pass', 'amplitude_limited', 'pass', 'pass'] | yes |
| CI.K0,K1,K2 | ['fail', 'not_run', 'not_run'] | ['fail', 'not_run', 'not_run'] | yes |
| D1.const.DH1/DH2 | ['costs_progress', 'costs_progress'] | ['costs_progress', 'costs_progress'] | yes |
| D1.mild.DH1/DH2 | ['costs_progress', 'costs_progress'] | ['costs_progress', 'costs_progress'] | yes |
| D1.stopgo.DH1/DH2 | ['costs_progress', 'costs_progress'] | ['costs_progress', 'costs_progress'] | yes |
| EH1,EH2,EH3 | ['safer at no extra cost', 'equivalent', 'equivalent'] | ['safer at no extra cost', 'equivalent', 'equivalent'] | yes |
| F own_statuses | [False, False] | [False, False] | yes |
| B.rule.outcome | ['mechanism persists'] | ['mechanism persists'] | yes |
| B7.rule_N, B7.rule_rate, B7.identity | ['holds', 'consequence', 'pass'] | ['holds', 'consequence', 'pass'] | yes |

## 4. Keys chosen (number location -> export key)

Each entry in the script (`ENT`) names its keys in the template. Keys read (package where found): `B.AQ.RR`, `B.AQ.RR.ci`, `B.AQ.RR_CK3`, `B.AQ.c`, `B.AQ.c.ci`, `B.AQ.lag`, `B.AQ.room_brk`, `B.AQ.room_pre`, `B.AQ.room_stop`, `B.AQ.within5`, `B.CA.RR`, `B.CA.RR.ci`, `B.CA.RR_CK3`, `B.CA.as_room`, `B.CA.c`, `B.CA.c.ci`, `B.CA.lag`, `B.CA.room_brk`, `B.CA.room_pre`, `B.CA.room_stop`, `B.CA.within5`, `B.CV.RR`, `B.CV.RR.ci`, `B.CV.RR_CK3`, `B.CV.as_room`, `B.CV.c`, `B.CV.c.ci`, `B.CV.lag`, `B.CV.room_brk`, `B.CV.room_pre`, `B.CV.room_stop`, `B.CV.within5`, `B.CV2.RR`, `B.CV2.RR.ci`, `B.CV2.RR_CK3`, `B.CV2.as_room`, `B.CV2.c`, `B.CV2.c.ci`, `B.CV2.lag`, `B.CV2.room_brk`, `B.CV2.room_pre`, `B.CV2.room_stop`, `B.CV2.within5`, `B.IMM.RR`, `B.IMM.RR.ci`, `B.IMM.RR_CK3`, `B.IMM.c`, `B.IMM.c.ci`, `B.IMM.lag`, `B.IMM.room_brk`, `B.IMM.room_pre`, `B.IMM.room_stop`, `B.IMM.within5`, `B7.10.0.1.R`, `B7.10.0.1.RR_N`, `B7.10.0.1.RR_N.ci`, `B7.10.0.1.as_room`, `B7.2.0.R`, `B7.2.0.as_room`, `B7.5.0.1.R`, `B7.5.0.1.as_room`, `CI.R`, `CI.R.ci`, `CI.den0.dec`, `CI.n_dec`, `CI.n_events`, `CI.n_runs`, `D1.const.CK3.dcau`, `D1.const.CK3.dwg`, `D1.const.PS.dcau`, `D1.const.PS.dwg`, `D1.mild.CK3.dcau`, `D1.mild.CK3.dcau.ci`, `D1.mild.CK3.dwg`, `D1.mild.CK3.dwg.ci`, `D1.mild.PS.dcau`, `D1.mild.PS.dwg`, `D1.n_runs`, `D1.stopgo.CK3.dcau`, `D1.stopgo.CK3.dcau.ci`, `D1.stopgo.CK3.dwg`, `D1.stopgo.CK3.dwg.ci`, `D1.stopgo.PS.dcau`, `D1.stopgo.PS.dwg`, `E1.maxerr`, `E3.CK3.hi.contact`, `E3.CK3.hi.dc`, `E3.CK3.hi.dc.ci`, `E3.CK3.hi.dt`, `E3.CK3.hi.dt.ci`, `E3.CK3.hi.vimp`, `E3.CK3.lo.contact`, `E3.CK3.lo.dc`, `E3.CK3.lo.dc.ci`, `E3.CK3.lo.dt`, `E3.CK3.lo.dt.ci`, `E3.CK3.lo.vimp`, `E3.F0.hi.caution`, `E3.F0.hi.contact`, `E3.F0.hi.vimp`, `E3.F0.lo.caution`, `E3.F0.lo.contact`, `E3.F0.lo.vimp`, `E3.N.hi.contact`, `E3.N.hi.dc`, `E3.N.hi.dc.ci`, `E3.N.hi.dt`, `E3.N.hi.dt.ci`, `E3.N.hi.vimp`, `E3.N.lo.contact`, `E3.N.lo.dc`, `E3.N.lo.dc.ci`, `E3.N.lo.dt`, `E3.N.lo.dt.ci`, `E3.N.lo.vimp`, `E3.NIMM.hi.contact`, `E3.NIMM.hi.dc`, `E3.NIMM.hi.dc.ci`, `E3.NIMM.hi.dt`, `E3.NIMM.hi.dt.ci`, `E3.NIMM.hi.vimp`, `E3.NIMM.lo.contact`, `E3.NIMM.lo.dc`, `E3.NIMM.lo.dc.ci`, `E3.NIMM.lo.dt`, `E3.NIMM.lo.dt.ci`, `E3.NIMM.lo.vimp`, `E3.PS.hi.caution`, `E3.PS.hi.contact`, `E3.PS.hi.dc`, `E3.PS.hi.dc.ci`, `E3.PS.hi.dt`, `E3.PS.hi.dt.ci`, `E3.PS.hi.vimp`, `E3.PS.lo.caution`, `E3.PS.lo.contact`, `E3.PS.lo.dc`, `E3.PS.lo.dc.ci`, `E3.PS.lo.dt`, `E3.PS.lo.dt.ci`, `E3.PS.lo.vimp`, `E3.TG.hi.contact`, `E3.TG.hi.dc`, `E3.TG.hi.dc.ci`, `E3.TG.hi.dt`, `E3.TG.hi.dt.ci`, `E3.TG.hi.vimp`, `E3.TG.lo.contact`, `E3.TG.lo.dc`, `E3.TG.lo.dc.ci`, `E3.TG.lo.dt`, `E3.TG.lo.dt.ci`, `E3.TG.lo.vimp`, `E3.n_cases`, `E3b.n_cases`, `F.R`, `F.R.ci`, `F.n_dec`, `F.n_heldout`, `LB.DS.rel`, `LB.DS.rel.ci`, `LB.IMM.c`, `LB.IMM.c.ci`, `LB.IMM.r`, `LB.IMM.r.ci`, `LB.IMM.within5`, `LB.PO25`, `LB.PO50`, `LB.PO75`, `LB.PS.like`, `LB.PS.rec`, `LB.PS.rec.ci`, `LB.R`, `LB.R.ci`, `LB.R.dec`, `LB.REL_F0`, `LB.RR_CK3`, `LB.RR_CK3.ci`, `LB.RR_E5`, `LB.RR_E5.ci`, `LB.RR_E5mP`, `LB.RR_E5mP.ci`, `LB.RR_N`, `LB.RR_N.ci`, `LB.RR_N.dec`, `LB.RR_N.dec.ci`, `LB.RS075.rel`, `LB.RS075.rel.ci`, `LB.T.relmax`, `LB.T.relmin`, `LB.T0.RR_CK3`, `LB.T1.rel`, `LB.T2.rel`, `LB.T20.RR_CK3`, `LB.T3.rel`, `LB.mov.RR_CK3`, `LB.n_dec`, `LB.n_runs`, `TU.R`, `TU.RR_CK3`, `TU.RR_N`

Old-evaluation values in Table V (5.51, 0.837, −0.0004) are read from the v12 record (`revision_v12\draft\DERIVED_v12.json`, `GL_R`, `GL_RR_CK3`, `GL_RRN`); 0.837 and −0.0004 are also compared with `TRANSFER.structured.per_set.old` (0.8366, −0.000414), which agrees. 5.51 has no v13 second source.

## 5. Supplement (weaker check)

I did not map every supplement cell to a key. Instead every decimal number in `SUPPLEMENT_v13.md` (1227 tokens, 746 distinct) was tested for being a correctly rounded value, at its own number of decimals (also x100 for percentages), of **some** scalar or interval end in the exports, the B summary, B8 or F extras. This finds numbers with no source; it cannot find a correct-looking number placed in the wrong cell.

- Tokens with a matching export value: 1184; without: **43** (35 distinct)
- Distinct unmatched tokens (count in text): 10.1109 (x6), 99.86 (x2), 1.093 (x2), 60.45 (x2), 4.86 (x1), 5.412 (x1), 7.550 (x1), 0.9995 (x1), 97.5% (x1), 10.16 (x1), 12.39 (x1), 15.59 (x1), −0.000131 (x1), −0.00577 (x1), −0.00478 (x1), 0.00428 (x1), −0.00638 (x1), −0.0312 (x1), −0.0437 (x1), 0.903 (x1), 0.353 (x1), 0.606 (x1), 0.468 (x1), 0.711 (x1), 4.53 (x1), 99.26 (x1), 99.57 (x1), 98.73 (x1), 98.28 (x1), 25.260745 (x1), 2018.8569495 (x1), 2004.1336491 (x1), 45743.2020 (x1), 10.3390 (x1), 10.1007 (x1)

Where I looked at them (supplement line numbers of the frozen file): L18 (car length, a design constant); L68 and L80 (calibration and rule thresholds); L233-L237 (old-evaluation and tuning-run intervals of the earlier analysis: records outside the v13 exports, not verifiable here); L262 (tercile range 4.53, the text of `LB.T3.range` = "4.53–5.71", a string key); L467-L470 (S11 margin-ratio table: old-run records, not in the exports); the 10.1109 / 25.260745 / 2018.8569495 style tokens are DOI or reference fragments.

Unmatched tokens can be legitimate: design constants (tuning settings, thresholds, hash-free parameters), values from records outside the exports, or sums and differences of exported numbers; they need a human look at the supplement line.
