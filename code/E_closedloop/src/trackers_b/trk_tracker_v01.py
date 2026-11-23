"""v13 shared tracker library: the step-wise tracker interface and the variant configurations. New file, 19 Nov 2026
(Claude Opus 5.5). See README.md for the API and IMM_AND_VARIANTS_SPEC_v01.md for the definitions.

    import trk_env_v01 as env; env.setup()            # FIRST (before numpy in a fresh process if bit-exact replay is wanted)
    import trk_tracker_v01 as T
    trk = T.V13Tracker('B1')                           # or 'CV0', 'B2', 'B3', 'B4', 'B1_d090', 'B1_d098'
    tracks = trk.step(detections, state_time)          # one call per detector frame; returns OnlineTracker-format track dicts
    actors = T.planner_actors(tracks, ego_world_rh, route_yaw)   # Codex's planner_actors (unchanged): 4x4 P per actor

Variants (car class = CANMOT label 2 only; every other class runs the online filter of record):
    CV0      the online tracker of record (CANMOT CV, ExtendedKalmanFilterRotate, configuration of record) + recording
    B3       CV re-tuned: car R diagonal (x, y, vx, vy) = measured mean squared errors; car Q = kappa * Q of record
    B2       B3 + innovation-adaptive velocity-block Q
    B4       CA (CANMOT CA model, CANMOT linear KF arithmetic, world-frame noise, axial yaw residual)
    B1       IMM over {B3 CV, B4 CA}, transition diagonal 0.95 per 0.5 s, initial mode probabilities (0.9, 0.1)
    B1_d090, B1_d098   B1 with diagonal 0.90 / 0.98
Rates (B7): V13Tracker(variant, dt=0.1 or 0.2): every Q of every class (and the CA Q) scaled by dt / 0.5 elementwise unless
q_scale=False; R unchanged; deletion ages kept in seconds (frames = round(max_age * 0.5 / dt)); the IMM transition becomes
Pi(0.5)^(dt / 0.5).
"""
import copy, json, pathlib
import numpy as np
import trk_env_v01 as env

HERE = pathlib.Path(__file__).resolve().parent
CONSTANTS_FILE = HERE / 'trk_constants_v01.json'
CAR = 2
VARIANTS = {
    'CV0': dict(car_filter='RecEKFRotate', tuned=False),
    'B3': dict(car_filter='RecEKFRotate', tuned=True),
    'B2': dict(car_filter='AdaptiveQEKF', tuned=True),
    'B4': dict(car_filter='CALinearKF', tuned=True),
    'B1': dict(car_filter='IMMFilter', tuned=True, diag=0.95),
    'B1_d090': dict(car_filter='IMMFilter', tuned=True, diag=0.90),
    'B1_d098': dict(car_filter='IMMFilter', tuned=True, diag=0.98),
}
IMM_MU0 = [0.9, 0.1]
B2_RULE = dict(lo=0.25, hi=10.0, last=3)
_F = None


def _filters():
    global _F
    if _F is None:
        env.setup()
        import trk_filters_v01 as F
        F.install()
        _F = F
    return _F


def load_constants(path=None):
    p = pathlib.Path(path) if path else CONSTANTS_FILE
    return json.loads(p.read_text(encoding='utf-8'))


def car_matrices(const, base_cfg):
    """B3 / B4 car-class matrices from the tuned constants (see the spec, sections B3 and B4)."""
    R = np.array(base_cfg['model_cfg']['matrix_r'][CAR], float)
    for i, key in ((0, 'R_x'), (1, 'R_y'), (6, 'R_vx'), (7, 'R_vy')):
        R[i, i] = float(const['R_car_diag'][key])
    kappa = float(const['kappa'])
    Qcv = kappa * np.array(base_cfg['model_cfg']['matrix_q'][CAR], float)
    s2 = float(const.get('sigma_a2', 1.0))
    qd = np.diag(Qcv)
    Qca = np.zeros((13, 13))
    for cv_i, ca_i in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8, 12]):
        Qca[ca_i, ca_i] = qd[cv_i]
    for i in (9, 10, 11):
        Qca[i, i] = s2
    H = np.zeros((9, 13))
    for r, c in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 12]):
        H[r, c] = 1.
    P0 = H.T @ R @ H
    P0[8, 8] = 10.
    for i in (9, 10, 11):
        P0[i, i] = float(const.get('ca_acc_init_var', 10.0))
    return dict(R=R, Q_cv=Qcv, Q_ca=Qca, P0_ca=P0)


def make_config(variant='CV0', const=None, base_cfg=None, dt=0.5, q_scale=True, recorder=None, imm_diag=None):
    """Tracker configuration of one variant (a deep copy; the base configuration is never changed)."""
    if variant not in VARIANTS:
        raise ValueError('unknown variant %r' % (variant,))
    spec = VARIANTS[variant]
    cfg = copy.deepcopy(base_cfg if base_cfg is not None else env.tracker_config())
    v = dict(variant=variant, car_filter=spec['car_filter'], rec=recorder, b2=dict(B2_RULE))
    if spec['tuned']:
        if const is None:
            const = load_constants()
        cm = car_matrices(const, cfg)
        cfg['model_cfg']['matrix_q'][CAR] = cm['Q_cv'].tolist()
        cfg['model_cfg']['matrix_r'][CAR] = cm['R'].tolist()
        v['car'] = dict(R=cm['R'].tolist(), Q_ca=cm['Q_ca'].tolist(), P0_ca=cm['P0_ca'].tolist())
    if spec['car_filter'] == 'IMMFilter':
        v['imm'] = dict(diag=float(imm_diag if imm_diag is not None else spec['diag']), mu0=list(IMM_MU0))
    if float(dt) != 0.5:
        cfg['basic']['LiDAR_interval'] = float(dt)
        if q_scale:
            f = float(dt) / 0.5
            cfg['model_cfg']['matrix_q'] = [(np.array(q, float) * f).tolist() for q in cfg['model_cfg']['matrix_q']]
            if 'car' in v:
                v['car']['Q_ca'] = (np.array(v['car']['Q_ca'], float) * f).tolist()
        cfg['life_cycle']['max_age'] = {c: int(round(a * 0.5 / float(dt))) for c, a in cfg['life_cycle']['max_age'].items()}
    v['dt'] = float(dt); v['q_scale'] = bool(q_scale)
    cfg['v13'] = v
    return cfg


class V13Tracker:
    """One tracker instance; step() once per detector frame, in time order (CANMOT's own frame bookkeeping)."""

    def __init__(self, variant='CV0', const=None, base_cfg=None, dt=0.5, q_scale=True, record=True, imm_diag=None):
        F = _filters()
        from online_tracker import OnlineTracker
        self.rec = F.Recorder() if record else None
        self.variant = variant
        self.cfg = make_config(variant, const, base_cfg, dt, q_scale, self.rec, imm_diag)
        self.ot = OnlineTracker(self.cfg)

    def step(self, detections, state_time):
        _F.install()           # re-assert the dispatcher (another module in the process may have rebound CANMOT's factory name)
        if self.ot.index == 0 and self.rec is not None:
            self.rec.reset()
        return self.ot.step(detections, state_time)


def planner_actors(tracks, ego_world_rh, route_yaw):
    _filters()
    from online_tracker import planner_actors as pa
    return pa(tracks, ego_world_rh, route_yaw)


def serial_actors(actors):
    _filters()
    from sensor_policy import serial_actors as sa
    return sa(actors)


# ------------------------------------------------------------------------------------------------ offline re-tracking of a capture
SIM_DT = 0.05


def retrack_capture(cap, variant='CV0', const=None, base_cfg=None, frames=True, imm_diag=None, det_rows=None, dt=0.5, q_scale=True,
                    latency=0.0):
    """Feed a capture's detections through a variant and rebuild the planner actor list of every decision tick (REFLECT @
    state.center_lh, route yaw of the first truth record), as tracker_harness_v02.check_run does. Returns the overlays (records that
    replace the logged files) and the recorder.
    Default: the logged 2 Hz detections (detections.jsonl, logged order and times), dt 0.5, no latency; then a decision at tick k uses
    the detector frame kd = 19 + 10 ((k - 19) // 10) (the paid chain). B7 (session CD): det_rows = rows {k, time, model} at another rate
    (time order), dt = 0.2 / 0.1, latency L: a decision at tick k uses the last frame whose k_frame * 0.05 + L <= k * 0.05 (+1e-9);
    with L = 0 and the logged rows this is exactly the paid chain's kd. No frame -> no actors (as before the first detection)."""
    cap = pathlib.Path(cap)
    logged = det_rows is None
    det = list(env.jl(cap / 'detections.jsonl')) if logged else list(det_rows)
    trk = V13Tracker(variant, const, base_cfg, dt=dt, q_scale=q_scale, imm_diag=imm_diag)
    outs = []
    for row in det:
        outs.append(copy.deepcopy(trk.step(copy.deepcopy(row['model']), row['time'])))
    new_det = []
    for row, out in zip(det, outs):
        r2 = dict(row); r2['tracks'] = out; new_det.append(r2)
    ov = {'detections.jsonl': new_det, 'filter_events.jsonl': trk.rec.events, 'filter_algebra.jsonl': trk.rec.algebra}
    if frames:
        truth0 = next(env.jl(cap / 'evaluation_truth.jsonl'))
        route_yaw = float(truth0['ego']['derived']['route_yaw_rh'])
        by_k = {d['k']: out for d, out in zip(det, outs)}
        kframes = np.array(sorted(by_k), dtype=np.int64)
        fr_new = []
        for fr in env.jl(cap / 'frames.jsonl'):
            ex = fr.get('execution')
            if ex and ex.get('new_decision') is not None:
                k = fr['k']
                if logged and latency == 0.0:
                    kd = None if k < 19 else 19 + 10 * ((k - 19) // 10)
                    tracks = [] if kd is None else by_k.get(kd)
                else:
                    ok = kframes[kframes * SIM_DT + latency <= k * SIM_DT + 1e-9]
                    tracks = by_k[int(ok[-1])] if ok.size else []
                if tracks is None:
                    raise RuntimeError('no detector frame for decision k=%d' % k)
                c = fr['state']['center_lh']
                ego = np.array([c[0], -c[1], c[2]])
                acts = serial_actors(planner_actors(tracks, ego, route_yaw))
                fr = copy.deepcopy(fr)
                fr['execution']['new_decision']['actors'] = acts
            fr_new.append(fr)
        ov['frames.jsonl'] = fr_new
    return ov, trk.rec
