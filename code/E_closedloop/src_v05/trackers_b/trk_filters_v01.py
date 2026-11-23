"""v13 shared tracker library: filter classes of the tracker variants of AMENDMENT_10_v13 section 3 (B1-B4). New file,
19 Nov 2026 (Claude Opus 5.5). Specification: IMM_AND_VARIANTS_SPEC_v01.md in this folder (the text both IMM implementations
follow). Requires trk_env_v01.setup() first (CANMOT on sys.path).

Classes (all keep CANMOT's KalmanFilter interface, so CANMOT's association, life cycle and score management run unchanged):
  RecEKFRotate   CANMOT's ExtendedKalmanFilterRotate (the online filter of record), unchanged arithmetic, plus recording of
                 the filter events and the update algebra (prior state, prior P, measurement, rotated R) into cfg['v13']['rec'].
  AdaptiveQEKF   B2: RecEKFRotate whose velocity-block process noise (state 6, 7, 8) is multiplied before each predict by
                 clip(m, 0.25, 10), m = mean of NIS_pos / 2 over the track's last (at most 3) updates; m = 1 before any update.
  CALinearKF     B4: CANMOT's LinearKalmanFilter arithmetic with CANMOT's CA motion model (13 states), world-frame Q and R from
                 cfg['v13']['car'], birth covariance P0_ca; the yaw innovation uses the online filter's axial rule (deviation
                 D-B4-1, see the spec); P symmetrised after each update (D-B4-3, bug fix of 19 Nov 15:45).
  IMMFilter      B1: interacting multiple model over {CV: the B3 rotated EKF, CA: the B4 linear KF} in the CA state space.
Dispatch: install() rebinds the name ExtendedKalmanFilterRotate in canmot.tracking.nusc_trajectory (the module whose
globals() CANMOT's Trajectory uses to build a filter) to Dispatch, which builds, per track, the class named by the tracker's own
config: cfg['v13']['car_filter'] for the car class (label 2) and RecEKFRotate for every other class. A config without the
'v13' key gets CANMOT's original class (so a tracker built without this library is unaffected).
"""
import math
import numpy as np
from canmot.motion_module import kalman_filter as KF
from canmot.motion_module import motion_model as MM
from canmot.motion_module.kalman_filter import ExtendedKalmanFilterRotate, LinearKalmanFilter, KalmanFilter, axis_residual_from_wrapped
from canmot.utils.math import warp_to_pi

CAR = 2
CV_IN_CA = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12]           # CA state index of each CV state component
ACC = [9, 10, 11]
YAW_CA = 12


def embed_cv(x, P):
    """CV (10) -> CA (13): accelerations 0, their variances and covariances 0."""
    X = np.zeros((13, 1)); X[CV_IN_CA, 0] = np.asarray(x, float).ravel()
    PP = np.zeros((13, 13)); PP[np.ix_(CV_IN_CA, CV_IN_CA)] = P
    return X, PP


def project_cv(X, PP):
    return X[CV_IN_CA, :].copy(), PP[np.ix_(CV_IN_CA, CV_IN_CA)].copy()


class Recorder:
    """Event and algebra sink of one tracker (the formats of Codex's tracker_audit, fields used downstream only)."""

    def __init__(self):
        self.events = []
        self.algebra = []
        self.modes = []          # IMM only: per track and frame, mode probabilities after update (or after predict on a miss)

    def event(self, ev):
        ev['index'] = len(self.events)
        self.events.append(ev)

    def reset(self):
        self.event(dict(kind='reset'))
        self.algebra.append(dict(kind='reset'))


def _rec(cfg):
    v = cfg.get('v13') if isinstance(cfg, dict) else None
    return v.get('rec') if v else None


def _nis_pos(z, x_prior, P_prior, R_used):
    nu = np.asarray(z, float).ravel()[0:2] - np.asarray(x_prior, float).ravel()[0:2]
    S = np.asarray(P_prior, float)[0:2, 0:2] + np.asarray(R_used, float)[0:2, 0:2]
    return float(nu @ np.linalg.solve(S, nu))


# ------------------------------------------------------------------------------------------------ online CV with recording
class RecEKFRotate(ExtendedKalmanFilterRotate):
    def __init__(self, timestamp, config, track_id, det_infos):
        self._rec = _rec(config)
        super().__init__(timestamp, config, track_id, det_infos)

    def initialize(self, det_infos):
        super().initialize(det_infos)
        if self._rec is not None:
            self._rec.event(dict(kind='birth', track=int(self.tracking_id), seq=int(self.seq_id), timestamp=int(self.timestamp),
                                 yaw=float(det_infos['nusc_box'].yaw), dt=float(self.dt), Q=self.Q.tolist(), R=self.R.tolist()))

    def predict(self, timestamp):
        yaw = float(self.state[-1, 0])
        super().predict(timestamp)
        if self._rec is not None:
            self._rec.event(dict(kind='predict', track=int(self.tracking_id), timestamp=int(timestamp), yaw=yaw))

    def update(self, timestamp, det=None):
        yaw = float(self.state[-1, 0])
        if det is not None:
            x0 = self.state.copy(); P0 = self.P.copy()
            rotmat = self.model.get_rotation_matrix_for_measurement(self.state)
            Rr = rotmat @ self.R @ rotmat.T
            z = self.getMeasureInfo(det)
        super().update(timestamp, det)
        if self._rec is not None:
            self._rec.event(dict(kind='update' if det is not None else 'miss', track=int(self.tracking_id), timestamp=int(timestamp), yaw=yaw))
            if det is not None:
                self._rec.algebra.append(dict(kind='update', track=int(self.tracking_id), category=int(self.class_label), timestamp=int(timestamp),
                                              prior=dict(state=x0.tolist(), P=P0.tolist()), measurement=z.tolist(), rotated_R=Rr.tolist()))
        if det is not None:
            self._after_update(_nis_pos(z, x0, P0, Rr))

    def _after_update(self, nis):
        pass


# ------------------------------------------------------------------------------------------------ B2
class AdaptiveQEKF(RecEKFRotate):
    """B2: velocity-block process noise Q_v * clip(m, lo, hi) (states 6, 7, 8 of the CV state)."""

    def __init__(self, timestamp, config, track_id, det_infos):
        b2 = config['v13']['b2']
        self._lo, self._hi, self._last = float(b2['lo']), float(b2['hi']), int(b2['last'])
        self._nis = []
        super().__init__(timestamp, config, track_id, det_infos)
        self._Qbase = self.Q.copy()

    def factor(self):
        if not self._nis:
            return 1.0
        m = float(np.mean(self._nis[-self._last:])) / 2.0
        return min(max(m, self._lo), self._hi)

    def predict(self, timestamp):
        f = self.factor()
        Q = self._Qbase.copy()
        Q[6:9, 6:9] = Q[6:9, 6:9] * f
        self.Q = Q
        super().predict(timestamp)

    def _after_update(self, nis):
        self._nis.append(nis)


# ------------------------------------------------------------------------------------------------ B4
class CALinearKF(LinearKalmanFilter):
    """B4: CANMOT LinearKalmanFilter + CANMOT CA model; Q, R, P0 from cfg['v13']['car']; axial yaw residual (D-B4-1)."""

    def __init__(self, timestamp, config, track_id, det_infos, record=True):
        self._rec = _rec(config) if record else None
        self._car = config['v13']['car']
        KalmanFilter.__init__(self, timestamp, config, track_id, det_infos)
        self.model_class = MM.CA
        self.model = MM.CA(self.has_velo, self.dt)
        self.initialize(det_infos)

    def initialize(self, det_infos):
        self.F = self.model.getTransitionF(None)
        self.Q = np.array(self._car['Q_ca'], float)
        self.SD = self.model.getStateDim()
        self.P = np.array(self._car['P0_ca'], float)
        self.R = np.array(self._car['R'], float)
        self.H = self.model.getMeaStateH()
        assert self.SD == 13 and self.Q.shape == (13, 13) and self.P.shape == (13, 13) and self.R.shape == (9, 9)
        self.state = self.model.getInitState(det_infos)
        tra_infos = {'inner_state': self.state, 'exter_state': det_infos['np_array']}
        self.addFrameObject(self.timestamp, tra_infos, 'predict')
        self.addFrameObject(self.timestamp, tra_infos, 'update')
        if self._rec is not None:
            self._rec.event(dict(kind='birth', track=int(self.tracking_id), seq=int(self.seq_id), timestamp=int(self.timestamp),
                                 yaw=float(det_infos['nusc_box'].yaw), dt=float(self.dt), Q=self.Q.tolist(), R=self.R.tolist()))

    def predict(self, timestamp):
        yaw = float(self.state[-1, 0])
        super().predict(timestamp)                       # LinearKalmanFilter.predict, unchanged
        if self._rec is not None:
            self._rec.event(dict(kind='predict', track=int(self.tracking_id), timestamp=int(timestamp), yaw=yaw))

    def residual(self, det):
        """z - H x_pred with the yaw component wrapped to [-pi, pi) and then to the axial range [-pi/2, pi/2)."""
        res = self.getMeasureInfo(det) - self.state_meas_space
        self.model.warpResYawToPi(res)
        res[-1, 0] = axis_residual_from_wrapped(float(res[-1, 0]))
        return res

    def update(self, timestamp, det=None):
        yaw = float(self.state[-1, 0])
        if det is not None:
            x0 = self.state.copy(); P0 = self.P.copy(); z = self.getMeasureInfo(det)
            q = KF.Quaternion(det['np_array'][8:12].tolist())
            q = -q if q.axis[-1] < 0 else q
            assert q.radians == det['nusc_box'].yaw
            _res = self.residual(det)
            _KF_GAIN = self.P @ self.H.T @ self.innovation_information
            self.state += _KF_GAIN @ _res
            self.P = (np.asarray(np.eye(self.SD)) - _KF_GAIN @ self.H) @ self.P
            self.P = 0.5 * (self.P + self.P.T)             # D-B4-3: symmetrise (the (I - KH) P form accumulates asymmetry)
            self.model.warpStateYawToPi(self.state)
            output_info = self.getOutputInfo(self.state)
            self.addFrameObject(timestamp, {'inner_state': self.state, 'exter_state': output_info}, 'update')
        if self._rec is not None:
            self._rec.event(dict(kind='update' if det is not None else 'miss', track=int(self.tracking_id), timestamp=int(timestamp), yaw=yaw))
            if det is not None:
                self._rec.algebra.append(dict(kind='update', track=int(self.tracking_id), category=int(self.class_label), timestamp=int(timestamp),
                                              prior=dict(state=x0.tolist(), P=P0.tolist()), measurement=z.tolist(), rotated_R=self.R.tolist()))


class _CVComponent(ExtendedKalmanFilterRotate):
    """The B3 rotated EKF as an IMM mode (no recording); residual() = the innovation its update uses."""

    def residual(self, det):
        res = self.getMeasureInfo(det) - self.state_meas_space
        self.model.warpResYawToPi(res)
        res[-1, 0] = axis_residual_from_wrapped(float(res[-1, 0]))
        return res

    def rotated_R(self):
        rotmat = self.model.get_rotation_matrix_for_measurement(self.state)
        return rotmat @ self.R @ rotmat.T


# ------------------------------------------------------------------------------------------------ B1
def transition(diag_per_half_s, dt):
    """2-state symmetric Markov matrix for one step of dt seconds: Pi(0.5)^(dt/0.5). Off-diagonal from the diagonal."""
    d = float(diag_per_half_s)
    r = float(dt) / 0.5
    lam = (2. * d - 1.) ** r if r != 1. else (2. * d - 1.)
    dd = 0.5 * (1. + lam) if r != 1. else d
    return np.array([[dd, 1. - dd], [1. - dd, dd]])


def mix_gaussians(xs, Ps, w, yaw_idx=YAW_CA):
    """Weighted mixture moment match: mean sum w_i x_i, covariance sum w_i [P_i + (x_i - m)(x_i - m)'].
    The yaw component is averaged on the circle: each x_i's yaw is replaced by ref + wrap(yaw_i - ref), ref = the yaw of the
    component with the largest weight (first on ties); the mean yaw is wrapped to [-pi, pi) afterwards."""
    w = np.asarray(w, float)
    ref = float(xs[int(np.argmax(w))][yaw_idx, 0])
    adj = []
    for x in xs:
        x = np.array(x, float, copy=True)
        x[yaw_idx, 0] = ref + warp_to_pi(float(x[yaw_idx, 0]) - ref)
        adj.append(x)
    m = sum(wi * xi for wi, xi in zip(w, adj))
    P = sum(wi * (Pi + (xi - m) @ (xi - m).T) for wi, xi, Pi in zip(w, adj, Ps))
    m[yaw_idx, 0] = warp_to_pi(float(m[yaw_idx, 0]))
    return m, P


class IMMFilter(KalmanFilter):
    """B1: IMM over CV (B3 rotated EKF, embedded) and CA (B4 linear KF). See the spec for every step."""

    def __init__(self, timestamp, config, track_id, det_infos):
        self._rec = _rec(config)
        v = config['v13']
        KalmanFilter.__init__(self, timestamp, config, track_id, det_infos)
        self.model_class = MM.CA
        self.model = MM.CA(self.has_velo, self.dt)
        self.SD = 13
        self.H = self.model.getMeaStateH()
        self.Pi = transition(v['imm']['diag'], self.dt)
        self.mu = np.array(v['imm']['mu0'], float)
        self.cv = _CVComponent(timestamp, config, track_id, det_infos)
        self.ca = CALinearKF(timestamp, config, track_id, det_infos, record=False)
        self.R = np.array(v['car']['R'], float)                  # B3 R (object frame) - for bookkeeping only
        self._combine(self.mu)
        tra_infos = {'inner_state': self.state, 'exter_state': det_infos['np_array']}
        self.addFrameObject(self.timestamp, tra_infos, 'predict')
        self.addFrameObject(self.timestamp, tra_infos, 'update')
        self.c = self.mu.copy()
        if self._rec is not None:
            self._rec.event(dict(kind='birth', track=int(self.tracking_id), seq=int(self.seq_id), timestamp=int(self.timestamp),
                                 yaw=float(det_infos['nusc_box'].yaw), dt=float(self.dt), Q=self.ca.Q.tolist(), R=self.R.tolist()))
            self._rec.modes.append(dict(track=int(self.tracking_id), timestamp=int(self.timestamp), stage='birth', mu=self.mu.tolist()))

    def _modes(self):
        x1, P1 = embed_cv(self.cv.state, self.cv.P)
        return [x1, np.array(self.ca.state, float)], [P1, np.array(self.ca.P, float)]

    def _combine(self, w):
        xs, Ps = self._modes()
        self.state, self.P = mix_gaussians(xs, Ps, w)

    def predict(self, timestamp):
        yaw = float(self.state[-1, 0])
        # 1. interaction (mixing)
        c = self.Pi.T @ self.mu                               # c_j = sum_i Pi_ij mu_i
        W = (self.Pi * self.mu[:, None]) / c[None, :]          # W[i, j] = mu_{i|j}
        xs, Ps = self._modes()
        x01, P01 = mix_gaussians(xs, Ps, W[:, 0])
        x02, P02 = mix_gaussians(xs, Ps, W[:, 1])
        # 2. mode-matched prediction
        self.cv.state, self.cv.P = project_cv(x01, P01)
        self.ca.state, self.ca.P = x02, P02
        self.cv.predict(timestamp)
        self.ca.predict(timestamp)
        # 3. combined prediction (association, output and the miss case)
        self.c = c
        self._combine(c)
        Rbar = c[0] * self.cv.rotated_R() + c[1] * self.ca.R
        self._Rbar = Rbar
        self.state_meas_space = self.H @ self.state
        self.innovation_information = np.linalg.inv(self.H @ self.P @ self.H.T + Rbar)
        self.model.warpStateYawToPi(self.state)
        output_info = self.getOutputInfo(self.state)
        self.addFrameObject(timestamp, {'inner_state': self.state, 'exter_state': output_info}, 'predict')
        self.mu = c.copy()
        if self._rec is not None:
            self._rec.event(dict(kind='predict', track=int(self.tracking_id), timestamp=int(timestamp), yaw=yaw))

    def update(self, timestamp, det=None):
        yaw = float(self.state[-1, 0])
        if det is not None:
            x0 = self.state.copy(); P0 = self.P.copy(); z = self.getMeasureInfo(det)
            ll = np.empty(2)
            for j, f in enumerate((self.cv, self.ca)):
                nu = f.residual(det)
                Sinv = f.innovation_information
                sign, logdet_inv = np.linalg.slogdet(Sinv)
                ll[j] = -0.5 * float((nu.T @ Sinv @ nu)[0, 0]) + 0.5 * logdet_inv - 0.5 * nu.shape[0] * math.log(2. * math.pi)
            self.cv.update(timestamp, det)
            self.ca.update(timestamp, det)
            a = ll + np.log(self.c)
            a = a - a.max()
            mu = np.exp(a)
            self.mu = mu / mu.sum()
            self._combine(self.mu)
            self.model.warpStateYawToPi(self.state)
            output_info = self.getOutputInfo(self.state)
            self.addFrameObject(timestamp, {'inner_state': self.state, 'exter_state': output_info}, 'update')
            if self._rec is not None:
                self._rec.algebra.append(dict(kind='update', track=int(self.tracking_id), category=int(self.class_label), timestamp=int(timestamp),
                                              prior=dict(state=x0.tolist(), P=P0.tolist()), measurement=z.tolist(), rotated_R=self._Rbar.tolist(),
                                              loglik=ll.tolist()))
        if self._rec is not None:
            self._rec.event(dict(kind='update' if det is not None else 'miss', track=int(self.tracking_id), timestamp=int(timestamp), yaw=yaw))
            self._rec.modes.append(dict(track=int(self.tracking_id), timestamp=int(timestamp), stage='update' if det is not None else 'miss',
                                        mu=self.mu.tolist()))

    def get_covariance_meas(self):
        return self.H @ self.P @ self.H.T

    def get_measurement_noise_covariance(self):
        return self._Rbar if hasattr(self, '_Rbar') else self.R


# ------------------------------------------------------------------------------------------------ dispatch
CAR_FILTERS = {'RecEKFRotate': RecEKFRotate, 'AdaptiveQEKF': AdaptiveQEKF, 'CALinearKF': CALinearKF, 'IMMFilter': IMMFilter}
_ORIGINAL = ExtendedKalmanFilterRotate


class Dispatch:
    def __new__(cls, timestamp, config, track_id, det_infos):
        v = config.get('v13') if isinstance(config, dict) else None
        if v is None:
            return _ORIGINAL(timestamp, config, track_id, det_infos)
        label = int(det_infos['np_array'][-1])
        name = v['car_filter'] if label == CAR else 'RecEKFRotate'
        return CAR_FILTERS[name](timestamp, config, track_id, det_infos)


def install():
    import canmot.tracking.nusc_trajectory as NT
    if NT.ExtendedKalmanFilterRotate is not Dispatch:
        NT.ExtendedKalmanFilterRotate = Dispatch
    return NT
