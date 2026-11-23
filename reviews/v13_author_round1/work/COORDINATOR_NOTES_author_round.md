# Coordinator notes on the author-round panel (Claude Opus 5.5)

Written 22 Nov 2026, 19:05 to 19:06 EST (Get-Date 19:05:59). The seat and synthesis files are not edited; their hashes stay as recorded.

## 1. Time stamp in the synthesis header
`ARS_REVIEW_AUTHOR_ROUND_v01.md` line 5 says the record was written "19:02 to 19:30". The 19:30 is a typed time. The file was already complete, with SHA-256 3e5824bf…, at 19:05:19 by Get-Date, when the coordinator verified it. The synthesis agent's own run ended at about 19:05.

## 2. Hash checks by the coordinator
- **Seat files.** All ten were verified at hand-back (18:46 to 18:57) and again at 19:05:19, and none had changed. Each Phase 2 file's first line carries its Phase 1 file's hash, as the brief requires.
- **Synthesis files.**
  - ARS_REVIEW_AUTHOR_ROUND_v01.md: 3e5824bf59e734db45c5ff484b27b13f405774675d5d1284b78e5db328fd040d
  - ARS_AUTHOR_LETTER_AUTHOR_ROUND_v01.md: d64d395052ed8f63c99129aeabb0edd9461b415dba85956f868005b41e6eeb2f

## 3. Coordinator spot-checks in package_v13_1830 (text searches)
- **N-17, reference [27].** MANUSCRIPT_v13.md line 60 reads "a critical arrival rate beyond which the expected covariance is unbounded [27]". In Sinopoli et al. (2004) the expected covariance of an unstable system is unbounded when the arrival probability is at or below the critical value, so "beyond" has the direction wrong. This is from the coordinator's own knowledge of the paper; it was not checked online, and the author checks it.
- **N-1, the ACKNOWLEDGMENT.** Line 273 has "made every scientific decision". The DA and R1 raised it in Phase 1 without being told about it.
- **N-2, the permuted twin.**
  - The oracle's permuted twin is defined: E5p, at MANUSCRIPT line 110 and SUPPLEMENT line 62 ("E5p and its variants permute u_i within runs").
  - No definition of the adaptive filter's own twin was found. MANUSCRIPT lines 232 and 250 and SUPPLEMENT lines 143 and 789 use the term without defining it.
  - The synthesis ruling holds for the tracker's twin.

## 4. Not done, or done only in part
- No seat and no synthesis had web access, so the existence of the references and what they say were not checked (N-5, N-17).
- The synthesis opened only page07.png itself. Its other layout findings rest on the seats, who agree with each other.
- Only pages 1 to 3 of the supplement PDF were viewed as images. Its other pages are available from Paper work summary on request.
