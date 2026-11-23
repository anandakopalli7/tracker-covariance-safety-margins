"""A11 §6d / F's D: the detection-dropout mask, one rule shared by package E (closed loop, set E4) and package F (open loop).

Writer: session E (Claude Opus 5.5), 21 Nov 2026. The law, A11 §6c "One mask law for D and §6d" (final wording, about 14:00
EST by the laptop clock; gap row added about 14:08), implemented exactly:
  - seed per run: rng = numpy.random.default_rng(int.from_bytes(hashlib.sha256(("A11/D/" + case_id).encode()).digest()[:8], "big"))
    (the same integer as int(hexdigest()[:16], 16)); case_id is the protocol case id, e.g. c1109_eval_0480;
  - rows: the run's 2 Hz detector update ticks in order, i = 0, 1, 2, ...; row 0 is never masked (and draws nothing);
  - from row 1 on, at each row not inside a window, draw u = rng.random(); if u < 0.10, draw L = rng.integers(1, 4) (uniform on
    {1, 2, 3}) and mask rows i .. i+L-1; a window is cut at the run's end; rows inside a window draw nothing;
  - the row right after a window is never masked and draws nothing; draws resume at the row after it. Every masked stretch is
    therefore 1-3 rows (0.5-1.5 s).
In the closed loop, row i is sim frame k = 19 + 10 i (the probe's detector condition k >= 19 and k % 10 == 9). The mask depends
on the case only: every arm of a case sees the same mask. Draws do not depend on the number of rows (truncation only).
"""
import hashlib, pathlib

import numpy as np

LAW = 'A11D2'          # A11 §6c final wording (row 0 unmasked, gap row); the first wording was never run
PUNISH_NUM = 3         # A11 §6c: punish_num = 3 for every arm of D and §6d (pinned)
P_START = 0.10
L_MIN, L_MAX = 1, 3
FIRST_K, PERIOD_K = 19, 10
SEED_PREFIX = 'A11/D/'


def seed_for(case_id):
    return int.from_bytes(hashlib.sha256((SEED_PREFIX + str(case_id)).encode()).digest()[:8], 'big')


def mask_for_case(case_id, n_ticks):
    """Returns (mask, windows): mask[i] True when update tick i is dropped; windows = [(start tick, length)] in draw order
    (a window may run past n_ticks; its length is the drawn L, its masked ticks are truncated at n_ticks)."""
    assert type(n_ticks) is int and n_ticks >= 0
    rng = np.random.default_rng(seed_for(case_id))
    mask = [False] * n_ticks; windows = []; i = 1                 # row 0 is never masked and draws nothing
    while i < n_ticks:
        u = rng.random()
        if u < P_START:
            L = int(rng.integers(L_MIN, L_MAX + 1))
            for j in range(i, min(i + L, n_ticks)):                # a window is cut at the run's end
                mask[j] = True
            windows.append((i, L)); i += L + 1                     # the row after a window: unmasked, no draw
        else:
            i += 1
    return mask, windows


def n_updates(frames):
    """Number of detector update ticks k = 19 + 10 i with k < frames."""
    return 0 if frames <= FIRST_K else (frames - 1 - FIRST_K) // PERIOD_K + 1


def tick_index(k):
    assert k >= FIRST_K and (k - FIRST_K) % PERIOD_K == 0, k
    return (k - FIRST_K) // PERIOD_K


def describe(case_id, frames, punish_num):
    n = n_updates(frames); mask, windows = mask_for_case(case_id, n)
    return dict(schema='E4_DROPOUT_V01', law=LAW, law_file_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(), p_start=P_START, length_ticks=[L_MIN, L_MAX], seed_rule='default_rng(int.from_bytes(sha256(("A11/D/" + case_id).encode()).digest()[:8], "big")); row 0 unmasked; gap row after each window (A11 §6c)',
                case_id=str(case_id), seed=seed_for(case_id), first_k=FIRST_K, period_k=PERIOD_K, n_updates=n,
                mask=[int(x) for x in mask], windows=[list(w) for w in windows], masked_ticks=int(sum(mask)), punish_num=int(punish_num))
