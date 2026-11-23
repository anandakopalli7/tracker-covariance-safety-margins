r"""v02 (21 Nov 2026, Claude Opus 5.5; AMENDMENT_11 section 6, B1r): imm_compare_v01.py with kappa_ca. The library side imports the
additive shared\trackers\trk_tracker_v02.py (kappa_ca, when the constants file carries it); the second implementation is
imm2\imm2_v02.py (its own kappa_ca, written from the spec and A11). Same comparison and threshold (1e-9 relative). Text of
imm_compare_v01.py follows.
v13 package B: A10 section 10.1(b) second-IMM check. The library's B1 (trk_tracker_v01, IMMFilter) against the independent second
implementation (B_retrack\\imm2\\imm2_v01.py, written by a Sonnet subagent from IMM_AND_VARIANTS_SPEC_v01.md only) on the same
detection stream. New file, 19 Nov 2026 (Claude Opus 5.5).
Compared per detector frame: the output track ids (exact) and every track's 9x9 combined covariance P9: relative difference
max|P_a - P_b| / max|P_b| (A10: within 1e-9 relative); also centre and velocity (absolute).
Usage: python -I -B -X utf8 imm_compare_v01.py <constants_json> <diag> <out_json> <cap_dir> [<cap_dir> ...]
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time
LIB = pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers')
sys.path.insert(0, str(LIB))
import trk_env_v01 as env
env.setup()
import numpy as np
import trk_tracker_v01 as T
import trk_tracker_v02  # noqa: F401  (kappa_ca)
import subprocess, tempfile
IMM2 = pathlib.Path(__file__).resolve().parents[1] / 'imm2' / 'imm2_v02.py'


def run_imm2(cap, cpath, diag):
    """The second implementation in its OWN process (both implementations patch CANMOT's filter factory name)."""
    with tempfile.TemporaryDirectory() as td:
        o = pathlib.Path(td) / 'imm2.json'
        env_ = dict(os.environ, OPENBLAS_CORETYPE='Haswell')
        subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', str(IMM2), str(cap), str(cpath), repr(diag), str(o)], check=True, env=env_)
        return json.loads(o.read_text(encoding='utf-8'))

VAR = {0.95: 'B1', 0.90: 'B1_d090', 0.98: 'B1_d098'}


def main():
    cpath = pathlib.Path(sys.argv[1]); diag = float(sys.argv[2]); out = pathlib.Path(sys.argv[3]); caps = [pathlib.Path(c) for c in sys.argv[4:]]
    const = json.loads(cpath.read_text(encoding='utf-8'))
    res = []
    for cap in caps:
        t0 = time.time()
        ov, rec = T.retrack_capture(cap, VAR[diag], const=const, frames=False)
        a = [r['tracks'] for r in ov['detections.jsonl']]
        b = run_imm2(cap, cpath, diag)
        ids_ok = True; worst_rel = 0.; worst_c = 0.; worst_v = 0.; n_tr = 0; n_car = 0
        for fa, fb in zip(a, b):
            if [t['id'] for t in fa] != [t['id'] for t in fb]:
                ids_ok = False; continue
            for ta, tb in zip(fa, fb):
                Pa = np.array(ta['P9'], float); Pb = np.array(tb['P9'], float)
                worst_rel = max(worst_rel, float(np.abs(Pa - Pb).max() / np.abs(Pb).max()))
                worst_c = max(worst_c, float(np.abs(np.array(ta['center']) - np.array(tb['center'])).max()))
                worst_v = max(worst_v, float(np.abs(np.array(ta['velocity']) - np.array(tb['velocity'])).max()))
                n_tr += 1; n_car += ta['name'] == 'car'
        res.append(dict(cap=str(cap), frames=len(a), frames_b=len(b), ids_identical=ids_ok, track_states=n_tr, car_states=n_car,
                        P9_max_rel_diff=worst_rel, centre_max_abs_diff=worst_c, velocity_max_abs_diff=worst_v,
                        pass_1e9=bool(ids_ok and len(a) == len(b) and worst_rel <= 1e-9), seconds=round(time.time() - t0, 1)))
        print(json.dumps(res[-1]), flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(dict(code='imm_compare_v02.py', kappa_ca=const.get('kappa_ca'), constants=str(cpath), diag=diag, runs=res,
                                   all_pass=bool(all(r['pass_1e9'] for r in res)), written=time.strftime('%Y-%m-%d %H:%M:%S')), indent=1),
                   encoding='utf-8')


if __name__ == '__main__':
    main()
