"""Package F (revision v13): the 20 design-split decisions of the adapter's second-program check (A10 section 10.1(b)).
New file, 19 Nov 2026 (Claude Opus 5.5). Train scenes only. Selection with default_rng(20261917) (A10 section 5.8: hand-check
subset seed): 20 distinct scenes drawn from the sorted train scene list; in each, one evaluated (3 s) built decision drawn
uniformly from that scene's evaluated decisions in sweep order. Writes notes\\ADAPTER_CHECK_DECISIONS_v01.json with the scene,
the sweep's LIDAR_TOP timestamp (us), the keyframe sample token and the sweep's position in the scene's decision list. Computes
nothing else.
Usage: python -I f07_check_select_v01.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
import numpy as np                           # noqa: E402
import f03_adapter_v01 as AD                 # noqa: E402

OUTF = FC.F / 'notes' / 'ADAPTER_CHECK_DECISIONS_v01.json'


def main():
    if OUTF.exists():
        raise SystemExit('REFUSED: %s exists' % OUTF)
    FC.require_split('train')
    names = sorted(FC.splits()['train'])
    rng = np.random.default_rng(20261917)
    picks = rng.choice(len(names), size=20, replace=False)
    out = []
    for pi in picks:
        nm = names[int(pi)]
        z = np.load(FC.CACHE / 'train' / (nm + '.npz'), allow_pickle=False)
        sc = AD.Scene(z)
        last = float(sc.kf_t[-1])
        ev = [(j, kf) for j, kf in sc.decision_sweeps() if -0.1 <= sc.v[j] <= 20. and float(sc.sw_t[j]) + 3. <= last + 1e-9]
        j, kf = ev[int(rng.integers(0, len(ev)))]
        out.append(dict(scene=nm, sweep_index=int(j), sweep_timestamp_us=int(sc.meta['t0_us'] + round(float(sc.sw_t[j]) * 1e6)),
                        keyframe_index=int(kf), keyframe_sample_token=str(z['kf_token'][kf]),
                        now_s_from_first_keyframe=float(sc.sw_t[j])))
    doc = dict(code='f07_check_select_v01.py', seed=20261917, written=FC.clock(), decisions=out)
    OUTF.write_text(FC.jdump(doc), encoding='utf-8')
    print('WROTE', OUTF)


if __name__ == '__main__':
    main()
