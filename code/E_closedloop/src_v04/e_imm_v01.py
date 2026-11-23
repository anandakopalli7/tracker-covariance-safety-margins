"""Online IMM tracker for the E IMM arms (A10 7.2: "the IMM pair runs the frozen B1 tracker online").

Writer: session E (Claude Opus 5.5), 19 Nov 2026. A thin adapter around session B's step-wise interface
(work\\shared\\trackers\\trk_tracker_v01.V13Tracker, variant 'B1'), whose frozen files are copied unchanged into this
packet folder's trackers_b\\ (hash-bound with the packet). It is called exactly where the probe calls Codex's
OnlineTracker: tracks = tracker.step(detector_rows, now), once per detector update, and returns the same track dicts
(id, name, center, size, yaw, velocity, P9 = the IMM's combined covariance, state_time, score); the planner actors are then
built by the unchanged ObservationStream / planner_actors. Nothing else in the perception chain changes.
"""
import hashlib, json, os, pathlib, sys

L = pathlib.Path(__file__).resolve().parent
ROOT = L.parent
P149 = ROOT / '149_supported_sensor_preparation_20261101'
TRK = L / 'trackers_b'
VARIANT = 'B1'
FILES = ('trk_env_v01.py', 'trk_filters_v01.py', 'trk_tracker_v01.py', 'trk_constants_v01.json')


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


class OnlineIMM:
    def __init__(self, codex_root=None, variant=VARIANT, const=None, punish_num=None):
        root = pathlib.Path(codex_root) if codex_root is not None else P149
        os.environ.setdefault('V13_CODEX_ROOT', str(root))
        if str(TRK) not in sys.path:
            sys.path.insert(0, str(TRK))
        import trk_env_v01 as env
        env.setup(codex_root=str(root), exact_trig=None)
        import trk_tracker_v01 as T
        self.env = env; self.T = T; self.variant = variant
        self.trk = T.V13Tracker(variant, const=const, record=True)
        # E4 (A11 §6d): CANMOT's output.punish_num for this tracker (None = the config of record, unchanged)
        self.punish_num = None if punish_num is None else int(punish_num)
        if self.punish_num is not None:
            assert 1 <= self.punish_num <= 14
            self.trk.cfg['output']['punish_num'] = self.punish_num
            self.trk.ot.tracker.punish_num = self.punish_num
        self.n_events = self.n_algebra = self.n_modes = 0

    @property
    def index(self):
        return self.trk.ot.index

    def step(self, detections, state_time):
        return self.trk.step(detections, state_time)

    def new_records(self):
        """Recorder entries added since the last call: (events, algebra, modes)."""
        rec = self.trk.rec
        out = (rec.events[self.n_events:], rec.algebra[self.n_algebra:], rec.modes[self.n_modes:])
        self.n_events, self.n_algebra, self.n_modes = len(rec.events), len(rec.algebra), len(rec.modes)
        return out

    def describe(self):
        return dict(schema='E_IMM_TRACKER_V01', variant=self.variant, library='work\\shared\\trackers (session B), frozen copy in trackers_b',
                    files={f: (sha(TRK / f) if (TRK / f).exists() else None) for f in FILES},
                    env=dict(codex=self.env.STATE['codex'], exact_trig=self.env.STATE['exact_trig'], blas=self.env.STATE['blas']),
                    imm=self.trk.cfg['v13'].get('imm'), car_filter=self.trk.cfg['v13'].get('car_filter'),
                    punish_num=self.trk.ot.tracker.punish_num)
