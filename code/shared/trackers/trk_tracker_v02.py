"""v13 shared tracker library, ADDITIVE module (21 Nov 2026, Claude Opus 5.5; AMENDMENT_11_v13 §6, IMM re-tune stage 2, coordinator OK
21 Nov ~13:58 EST). No frozen library file is edited.

One new constant, kappa_ca: it multiplies only the CA filter's position and velocity process-noise terms, i.e. the diagonal entries of
Q_ca at CA-state indices 0, 1, 2 (x, y, z) and 6, 7, 8 (vx, vy, vz); the size, yaw and acceleration terms are unchanged. Q_cv (the CV
filter and the IMM's CV component) is unchanged. It acts through trk_tracker_v01.car_matrices, which make_config calls by its module
name: importing this module replaces that function by car_matrices below, which calls the frozen one and, only when the constants
dict carries 'kappa_ca', scales those six entries. With no 'kappa_ca' the returned matrices are the frozen ones (the same objects).
Identity test (frozen with this file): with kappa_ca absent the re-tracked B4 and B1 arrays of the 20 lead-braking tuning runs are
bit-identical to the stored v01 arrays (B_retrack\\code\\b_kca_identity_v02.py).
Use: import trk_tracker_v02 (after trk_tracker_v01) in any process that needs kappa_ca; then pass const=dict(..., kappa_ca=k).
"""
import numpy as np
import trk_tracker_v01 as T1

CA_POS_VEL = (0, 1, 2, 6, 7, 8)
_FROZEN = T1.car_matrices if not getattr(T1.car_matrices, '_v02', False) else T1.car_matrices._frozen


def car_matrices(const, base_cfg):
    cm = _FROZEN(const, base_cfg)
    if const is None or 'kappa_ca' not in const:
        return cm
    k = float(const['kappa_ca'])
    Q = np.array(cm['Q_ca'], float).copy()
    for i in CA_POS_VEL:
        Q[i, i] = k * Q[i, i]
    return dict(cm, Q_ca=Q)


car_matrices._v02 = True
car_matrices._frozen = _FROZEN


def install():
    T1.car_matrices = car_matrices


install()
