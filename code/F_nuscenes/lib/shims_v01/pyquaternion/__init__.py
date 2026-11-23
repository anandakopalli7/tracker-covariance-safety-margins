"""LOCAL STAND-IN for the third-party package `pyquaternion` (not installed on this laptop; no network installs).

Only the parts of pyquaternion.Quaternion that the tracker path uses are provided, written to follow the published
pyquaternion 0.9.x arithmetic step by step (same order of floating-point operations). Anything else raises loudly.
Correctness is NOT assumed: it is checked by comparing the replayed tracker output with the logged output bit for bit
(tracker_harness_v0x.py). Used by: nuscenes-devkit Box, canmot NuscBox, canmot motion models / Kalman filters.
"""
from copy import deepcopy
from math import sqrt, pi, sin, cos, atan2

import numpy as np


class Quaternion:
    def __init__(self, *args, **kwargs):
        s = len(args)
        if s == 0:
            if kwargs:
                if ("scalar" in kwargs) or ("vector" in kwargs):
                    scalar = kwargs.get("scalar", 0.0)
                    scalar = 0.0 if scalar is None else float(scalar)
                    vector = self._validate_number_sequence(kwargs.get("vector", []), 3)
                    self.q = np.hstack((scalar, vector))
                elif ("axis" in kwargs) or ("radians" in kwargs) or ("degrees" in kwargs) or ("angle" in kwargs):
                    try:
                        axis = self._validate_number_sequence(kwargs["axis"], 3)
                    except KeyError:
                        raise ValueError("A valid rotation 'axis' parameter must be provided to describe a meaningful rotation.")
                    angle = kwargs.get('radians') or self.to_radians(kwargs.get('degrees')) or kwargs.get('angle') or 0.0
                    self.q = Quaternion._from_axis_angle(axis, angle).q
                elif "array" in kwargs:
                    self.q = self._validate_number_sequence(kwargs["array"], 4)
                elif "matrix" in kwargs:
                    raise NotImplementedError("stand-in pyquaternion: construction from a matrix is not provided")
                else:
                    raise NotImplementedError("stand-in pyquaternion: unsupported keyword construction %r" % sorted(kwargs))
            else:
                self.q = np.array([1.0, 0.0, 0.0, 0.0])
        elif s == 1:
            if isinstance(args[0], Quaternion):
                self.q = args[0].q
                return
            if args[0] is None:
                raise TypeError("Object cannot be initialised from {}".format(type(args[0])))
            try:
                r = float(args[0])
                self.q = np.array([r, 0.0, 0.0, 0.0])
                return
            except TypeError:
                pass
            self.q = self._validate_number_sequence(args[0], 4)
            return
        else:
            self.q = self._validate_number_sequence(args, 4)

    # ---- helpers (same arithmetic as pyquaternion)
    def _validate_number_sequence(self, seq, n):
        if seq is None:
            return np.zeros(n)
        if len(seq) == n:
            try:
                l = [float(e) for e in seq]
            except ValueError:
                raise ValueError("One or more elements in sequence <{!r}> cannot be interpreted as a real number".format(seq))
            else:
                return np.asarray(l)
        elif len(seq) == 0:
            return np.zeros(n)
        else:
            raise ValueError("Unexpected number of elements in sequence. Got: {}, Expected: {}.".format(len(seq), n))

    @classmethod
    def _from_axis_angle(cls, axis, angle):
        mag_sq = np.dot(axis, axis)
        if mag_sq == 0.0:
            raise ZeroDivisionError("Provided rotation axis has no length")
        if (abs(1.0 - mag_sq) > 1e-12):
            axis = axis / sqrt(mag_sq)
        theta = angle / 2.0
        r = cos(theta)
        i = axis * sin(theta)
        return cls(r, i[0], i[1], i[2])

    @staticmethod
    def to_radians(angle_deg):
        if angle_deg is not None:
            return float(angle_deg) / 180.0 * pi

    @staticmethod
    def to_degrees(angle_rad):
        if angle_rad is not None:
            return float(angle_rad) / pi * 180.0

    def __str__(self):
        return "{:.3f} {:+.3f}i {:+.3f}j {:+.3f}k".format(self.q[0], self.q[1], self.q[2], self.q[3])

    def __repr__(self):
        return "Quaternion({!r}, {!r}, {!r}, {!r})".format(self.q[0], self.q[1], self.q[2], self.q[3])

    def __hash__(self):
        return hash(tuple(self.q))

    def __copy__(self):
        return self.__class__(self.q)

    def __deepcopy__(self, memo):
        return self.__class__(deepcopy(self.q, memo))

    def __eq__(self, other):
        if isinstance(other, Quaternion):
            return bool(np.allclose(self.q, other.q, rtol=1.0e-13, atol=1.0e-14))
        return self.__eq__(self.__class__(other))

    def __neg__(self):
        return self.__class__(array=-self.q)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return self.__class__(array=np.dot(self._q_matrix(), other.q))
        return self * self.__class__(other)

    def _q_matrix(self):
        return np.array([
            [self.q[0], -self.q[1], -self.q[2], -self.q[3]],
            [self.q[1],  self.q[0], -self.q[3],  self.q[2]],
            [self.q[2],  self.q[3],  self.q[0], -self.q[1]],
            [self.q[3], -self.q[2],  self.q[1],  self.q[0]]])

    def _q_bar_matrix(self):
        return np.array([
            [self.q[0], -self.q[1], -self.q[2], -self.q[3]],
            [self.q[1],  self.q[0],  self.q[3], -self.q[2]],
            [self.q[2], -self.q[3],  self.q[0],  self.q[1]],
            [self.q[3],  self.q[2], -self.q[1],  self.q[0]]])

    def _sum_of_squares(self):
        return np.dot(self.q, self.q)

    @property
    def norm(self):
        return sqrt(self._sum_of_squares())

    def is_unit(self, tolerance=1e-14):
        return abs(1.0 - self._sum_of_squares()) < tolerance

    def _normalise(self):
        if not self.is_unit():
            n = self.norm
            if n > 0:
                self.q = self.q / n

    def _wrap_angle(self, theta):
        result = ((theta + pi) % (2 * pi)) - pi
        if result == -pi:
            result = pi
        return result

    @property
    def rotation_matrix(self):
        self._normalise()
        product_matrix = np.dot(self._q_matrix(), self._q_bar_matrix().conj().transpose())
        return product_matrix[1:][:, 1:]

    def get_axis(self, undefined=np.zeros(3)):
        tolerance = 1e-17
        self._normalise()
        norm = np.linalg.norm(self.vector)
        if norm < tolerance:
            return undefined
        else:
            return self.vector / norm

    @property
    def axis(self):
        return self.get_axis()

    @property
    def angle(self):
        self._normalise()
        norm = np.linalg.norm(self.vector)
        return self._wrap_angle(2.0 * atan2(norm, self.scalar))

    @property
    def degrees(self):
        return self.to_degrees(self.angle)

    @property
    def radians(self):
        return self.angle

    @property
    def scalar(self):
        return self.q[0]

    @property
    def vector(self):
        return self.q[1:4]

    @property
    def real(self):
        return self.scalar

    @property
    def imaginary(self):
        return self.vector

    @property
    def w(self):
        return self.q[0]

    @property
    def x(self):
        return self.q[1]

    @property
    def y(self):
        return self.q[2]

    @property
    def z(self):
        return self.q[3]

    @property
    def elements(self):
        return self.q

    def __getitem__(self, index):
        return self.q[int(index)]
