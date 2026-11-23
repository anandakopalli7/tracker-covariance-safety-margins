"""Independent second implementation of the B1 IMM (CV/CA) tracker filter (A10 v13 section 10.1(b)).

Written from IMM_AND_VARIANTS_SPEC_v01.md sections 1, 2, 4, 5, 7 only.  CANMOT's CV and CA model classes supply the
transition / observation / rotation matrices (same arithmetic as the filter of record); the Kalman equations and all IMM
logic below are written here.

Usage:  python -I -B -X utf8 imm2_v02.py <cap_dir> <constants_json> <diag> <out_json>
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import copy, json, math, sys

sys.dont_write_bytecode = True
_TRK = r'ARS_TRIAL\revision_v13\work\shared\trackers'
if _TRK not in sys.path:
    sys.path.append(_TRK)
import trk_env_v01
trk_env_v01.setup()
import numpy as np
from canmot.motion_module import kalman_filter as _kf
from canmot.motion_module.kalman_filter import KalmanFilter, axis_residual_from_wrapped
from canmot.motion_module.motion_model import CV, CA
from canmot.utils.math import warp_to_pi
from canmot.tracking import nusc_trajectory as _nt

CAR = 2
IDX = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12]      # CV index k  <->  CA index IDX[k]
HCA_ROWS = [0, 1, 2, 3, 4, 5, 6, 7, 12]
# CA state order [x, y, z, w, l, h, vx, vy, vz, ax, ay, az, yaw]: position = 0,1,2; velocity = 6,7,8
KAPPA_CA_IDX = (0, 1, 2, 6, 7, 8)
LOG2PI = math.log(2.0 * math.pi)

# ----------------------------------------------------------------------------------------------------------------------
# constants -> matrices (spec section 1)
# ----------------------------------------------------------------------------------------------------------------------


def derive_matrices(cfg_record, consts):
    """Return dict(R_B3 9x9, Q_B3 10x10, Q_CA 13x13, P0_CA 13x13) for the car class from the config of record + constants."""
    Rc = np.array(cfg_record['model_cfg']['matrix_r'][CAR], dtype=float).copy()
    Qc = np.array(cfg_record['model_cfg']['matrix_q'][CAR], dtype=float).copy()
    d = consts['R_car_diag']
    R_B3 = Rc.copy()
    for i, k in ((0, 'R_x'), (1, 'R_y'), (6, 'R_vx'), (7, 'R_vy')):
        R_B3[i, i] = d[k]
    Q_B3 = float(consts['kappa']) * Qc
    Q_CA = np.zeros((13, 13))
    dq = np.diag(Q_B3)
    for k in range(10):
        Q_CA[IDX[k], IDX[k]] = dq[k]
    for i in (9, 10, 11):
        Q_CA[i, i] = float(consts['sigma_a2'])
    if 'kappa_ca' in consts:      # A11 section 6 stage 2: scales only CA position and velocity process noise
        kc = float(consts['kappa_ca'])
        for i in KAPPA_CA_IDX:
            Q_CA[i, i] *= kc
    H = np.zeros((9, 13))
    for r, c in enumerate(HCA_ROWS):
        H[r, c] = 1.0
    P0 = H.T @ R_B3 @ H
    P0[8, 8] = 10.0
    for i in (9, 10, 11):
        P0[i, i] = float(consts['ca_acc_init_var'])
    return dict(R_B3=R_B3, Q_B3=Q_B3, Q_CA=Q_CA, P0_CA=P0)


H_CA = np.zeros((9, 13))
for _r, _c in enumerate(HCA_ROWS):
    H_CA[_r, _c] = 1.0

SETTINGS = None   # dict(R_B3, Q_CA, P0_CA, diag, mu0)


def configure(mats, diag=0.95, mu0=(0.9, 0.1)):
    global SETTINGS
    SETTINGS = dict(R_B3=np.array(mats['R_B3'], dtype=float), Q_CA=np.array(mats['Q_CA'], dtype=float),
                    P0_CA=np.array(mats['P0_CA'], dtype=float), diag=float(diag), mu0=np.array(mu0, dtype=float))

# ----------------------------------------------------------------------------------------------------------------------
# embedding, projection, moment matching
# ----------------------------------------------------------------------------------------------------------------------


def embed(x10, P10):
    x = np.zeros((13, 1))
    x[IDX, :] = x10
    P = np.zeros((13, 13))
    P[np.ix_(IDX, IDX)] = P10
    return x, P


def project(x13, P13):
    return x13[IDX, :].copy(), P13[np.ix_(IDX, IDX)].copy()


def mixture(xs, Ps, w):
    """Moment match of 13-state components with weights w; circular yaw (CA index 12); the first largest weight gives ref."""
    k = int(np.argmax(w))
    ref = float(xs[k][12, 0])
    xl = []
    for x in xs:
        y = x.copy()
        y[12, 0] = ref + warp_to_pi(float(x[12, 0]) - ref)
        xl.append(y)
    m = np.zeros((13, 1))
    for wi, y in zip(w, xl):
        m = m + wi * y
    P = np.zeros((13, 13))
    for wi, y, Pi in zip(w, xl, Ps):
        dv = y - m
        P = P + wi * (Pi + dv @ dv.T)
    m[12, 0] = warp_to_pi(float(m[12, 0]))
    return m, P


# ----------------------------------------------------------------------------------------------------------------------
# the IMM track filter
# ----------------------------------------------------------------------------------------------------------------------


class IMM2Filter(KalmanFilter):
    def __init__(self, timestamp, config, track_id, det_infos):
        super().__init__(timestamp, config, track_id, det_infos)   # seq_id, ids, dt, has_velo, frame_objects
        S = SETTINGS
        assert S is not None, 'imm2_v02.configure() not called'
        self.cv = CV(self.has_velo, self.dt, config['model_cfg']['matrix_q'], config['model_cfg']['matrix_r'])
        self.ca = CA(self.has_velo, self.dt)
        self.model = self.ca            # output format, yaw warping: CANMOT CA
        self.Fca = self.ca.getTransitionF(None)
        self.Qcv = np.asarray(config['model_cfg']['matrix_q'][self.class_label], dtype=float)
        self.Rcv = np.asarray(config['model_cfg']['matrix_r'][self.class_label], dtype=float)
        self.Rca = S['R_B3']
        self.Qca = S['Q_CA']
        d = S['diag']
        p = (2.0 * d - 1.0) ** (self.dt / 0.5)
        dd = (1.0 + p) / 2.0
        self.Pi = np.array([[dd, 1.0 - dd], [1.0 - dd, dd]])
        # --- birth of the mode filters
        xc = self.cv.getInitState(det_infos)
        U = self.cv.get_rotation_matrix_for_measurement(xc)
        Hc = self.cv.getMeaStateH(xc)
        Pc = Hc.T @ U @ self.Rcv @ U.T @ Hc
        Pc[8, 8] = 10.0
        xa = self.ca.getInitState(det_infos)
        Pa = S['P0_CA'].copy()
        self.xc, self.Pc, self.xa, self.Pa = xc, Pc, xa, Pa
        self.mu = S['mu0'].copy()
        xe, Pe = embed(xc, Pc)
        self.state, self.P = mixture([xe, xa], [Pe, Pa], self.mu)
        self.state_meas_space = H_CA @ self.state
        self.Rbar = self.Rca.copy()
        self.innovation_information = None
        self.log_lik = None
        tra_infos = {'inner_state': self.state, 'exter_state': det_infos['np_array']}
        self.addFrameObject(self.timestamp, tra_infos, 'predict')
        self.addFrameObject(self.timestamp, tra_infos, 'update')

    # -- one frame, step 1-3 of spec section 5
    def predict(self, timestamp):
        mu = self.mu
        c = self.Pi.T @ mu
        mix = np.zeros((2, 2))
        for j in range(2):
            for i in range(2):
                mix[i, j] = (self.Pi[i, j] * mu[i] / c[j]) if c[j] > 0.0 else mu[i]
        xe, Pe = embed(self.xc, self.Pc)
        xs, Ps = [xe, self.xa], [Pe, self.Pa]
        m1, P1 = mixture(xs, Ps, mix[:, 0])
        m2, P2 = mixture(xs, Ps, mix[:, 1])
        # CV mode: rotated-EKF predict
        cv = self.cv
        x0, Pcv = project(m1, P1)
        F = cv.getTransitionF(x0)
        rp = cv.get_rotation_matrix_for_state(x0)
        x1 = cv.stateTransition(x0)
        rq = cv.get_rotation_matrix_for_measurement(x1)
        Pcv = F @ Pcv @ F.T + rp @ self.Qcv @ rp.T
        H = cv.getMeaStateH(x1)
        Rrot = rq @ self.Rcv @ rq.T
        self.S_cv = H @ Pcv @ H.T + Rrot
        self.Sinv_cv = np.linalg.inv(self.S_cv)
        self.H_cv = H
        self.xm_cv = cv.StateToMeasure(x1)
        cv.warpStateYawToPi(x1)
        self.xc, self.Pc = x1, Pcv
        self.Rcv_rot = Rrot
        # CA mode: linear predict
        xca = self.Fca @ m2
        Pca = self.Fca @ P2 @ self.Fca.T + self.Qca
        self.S_ca = H_CA @ Pca @ H_CA.T + self.Rca
        self.Sinv_ca = np.linalg.inv(self.S_ca)
        self.xm_ca = H_CA @ xca
        self.ca.warpStateYawToPi(xca)
        self.xa, self.Pa = xca, Pca
        # combined prediction
        self.mu = c.copy()
        xe, Pe = embed(self.xc, self.Pc)
        self.state, self.P = mixture([xe, self.xa], [Pe, self.Pa], self.mu)
        self.state_meas_space = H_CA @ self.state
        self.Rbar = self.mu[0] * Rrot + self.mu[1] * self.Rca
        self.innovation_information = np.linalg.inv(H_CA @ self.P @ H_CA.T + self.Rbar)
        self.log_lik = None
        out = self.getOutputInfo(self.state)
        self.addFrameObject(timestamp, {'inner_state': self.state, 'exter_state': out}, 'predict')

    # -- step 4 (detection) / step 5 (miss)
    def update(self, timestamp, det=None):
        if det is None:
            return
        z = self.getMeasureInfo(det)
        cv, ca = self.cv, self.ca
        # CV mode residual
        rc = z - self.xm_cv
        cv.warpResYawToPi(rc)
        rc[-1, 0] = axis_residual_from_wrapped(float(rc[-1, 0]))
        # CA mode residual
        ra = z - self.xm_ca
        ca.warpResYawToPi(ra)
        ra[-1, 0] = axis_residual_from_wrapped(float(ra[-1, 0]))
        ll = []
        for r, S, Si in ((rc, self.S_cv, self.Sinv_cv), (ra, self.S_ca, self.Sinv_ca)):
            sign, logdet = np.linalg.slogdet(S)
            q = float((r.T @ Si @ r)[0, 0])
            ll.append(-0.5 * (q + logdet + 9 * LOG2PI))
        # CV update (Joseph, R rotated by the predicted (wrapped) yaw as in the filter of record)
        rot = cv.get_rotation_matrix_for_measurement(self.xc)
        R = rot @ self.Rcv @ rot.T
        K = self.Pc @ self.H_cv.T @ self.Sinv_cv
        IKH = np.eye(10) - K @ self.H_cv
        self.xc = self.xc + K @ rc
        self.Pc = IKH @ self.Pc @ IKH.T + K @ R @ K.T
        cv.warpStateYawToPi(self.xc)
        # CA update (plain form of spec section 4)
        K = self.Pa @ H_CA.T @ self.Sinv_ca
        self.xa = self.xa + K @ ra
        self.Pa = (np.eye(13) - K @ H_CA) @ self.Pa
        self.Pa = (self.Pa + self.Pa.T) / 2.0      # D-B4-3: symmetrise after the CA update
        ca.warpStateYawToPi(self.xa)
        # mode probabilities
        with np.errstate(divide='ignore'):
            lw = np.log(self.mu) + np.array(ll)
        lw = lw - np.max(lw)
        w = np.exp(lw)
        self.mu = w / w.sum()
        self.log_lik = ll
        xe, Pe = embed(self.xc, self.Pc)
        self.state, self.P = mixture([xe, self.xa], [Pe, self.Pa], self.mu)
        out = self.getOutputInfo(self.state)
        self.addFrameObject(timestamp, {'inner_state': self.state, 'exter_state': out}, 'update')

    def get_covariance_meas(self):
        return H_CA @ self.P @ H_CA.T

    def get_measurement_noise_covariance(self):
        return self.Rbar


# ----------------------------------------------------------------------------------------------------------------------
# integration: CANMOT's Trajectory builds filters through globals()[cfg filter name]; the name in the config of record
# is 'ExtendedKalmanFilterRotate' for every class, so the module-global of that name is replaced by a dispatcher.
# ----------------------------------------------------------------------------------------------------------------------
_ORIG_EKFR = _kf.ExtendedKalmanFilterRotate
INSTALLED = {'imm': False}
CREATED = []   # filters of the current run (diagnostics)


def _dispatch(timestamp, config, track_id, det_infos):
    if INSTALLED['imm'] and int(det_infos['np_array'][-1]) == CAR:
        f = IMM2Filter(timestamp, config, track_id, det_infos)
        CREATED.append(f)
        return f
    return _ORIG_EKFR(timestamp, config, track_id, det_infos)


_nt.ExtendedKalmanFilterRotate = _dispatch


def build_tracker(constants, diag=0.95, mu0=(0.9, 0.1), imm=True):
    """OnlineTracker on a deep copy of the config of record with Q_B3 / R_B3 for the car class (spec section 1)."""
    cfg = copy.deepcopy(trk_env_v01.tracker_config())
    mats = derive_matrices(cfg, constants)
    cfg['model_cfg']['matrix_q'][CAR] = mats['Q_B3'].tolist()
    cfg['model_cfg']['matrix_r'][CAR] = mats['R_B3'].tolist()
    configure(mats, diag, mu0)
    INSTALLED['imm'] = bool(imm)
    del CREATED[:]
    from online_tracker import OnlineTracker
    return OnlineTracker(cfg)


def retrack(cap_dir, constants_path, diag=0.95, mu0=(0.9, 0.1), imm=True):
    with open(constants_path, encoding='utf-8') as f:
        constants = json.load(f)
    tr = build_tracker(constants, diag, mu0, imm)
    out = []
    for row in trk_env_v01.jl(os.path.join(cap_dir, 'detections.jsonl')):
        res = tr.step(copy.deepcopy(row['model']), row['time'])
        out.append([copy.deepcopy(dict(id=r['id'], name=r['name'], P9=r['P9'], center=r['center'],
                                       velocity=r['velocity'], yaw=r['yaw'])) for r in res])
    return out


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    return o


if __name__ == '__main__':
    cap, cst, dg, outp = sys.argv[1:5]
    res = _clean(retrack(cap, cst, float(dg)))
    with open(outp, 'w', encoding='utf-8') as f:
        json.dump(res, f)
