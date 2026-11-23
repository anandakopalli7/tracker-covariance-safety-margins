"""Package E arms for the closed-loop probe (A10 section 7.2), with the braking fix F2 in every arm.

Writer: session E (Claude Opus 5.5), 19 Nov 2026. Lives in claude_smoke_v01/ of packet_e_v0x; imports the packet's
unchanged arms_adapter_v02 (for the native 712 SensorExecution / SensorPolicy, the rebind helper and the release gate).

Arms (job field 'arm'), all on the native 17-row finite selector and its (-5, -5) fallback:
  E_Z       zero margin: feasible iff d >= 0 on every constraint (g = 0)
  E_F0      g * s_F0 <= d^2, s_F0 = z' Pbar z (class average of record)
  E_N       g * p <= d^2, p = the consumer's projection of the tracker covariance
  E_CK3     g * s_F0 <= (d + SH)^2 with d + SH >= 0: the braking prediction (3 m/s^2) shifts the predicted path
  E_TG      g * (2 + v_e)^2 <= d^2: the time-gap margin, r0 = 2 m/s
  E_PS      g_phase * s_F0 <= d^2, g_phase = triple[phase], phase from the online lead track (A10 2.4)
  E_F0_IMM  as E_F0 on the online IMM tracker's actors with its class average Pbar_IMM
  E_N_IMM   as E_N on the online IMM tracker's actors
  E_BRAKE   brake test (E1): E_Z until tick brake_from_k, then the fallback at every decision
There is no acceleration-allowance term (beta = 0). Fix F5 is not applied.

How the margin enters: exactly as the packet's 'fixed' arm (arms_adapter_v01.unit_localization_library) replaces
p, the arm's constraint builder runs a line-for-line copy of consumer.constraints_for_trajectory
(e_sources_v01.constraints_full) and then sets row['p'] := s_A and row['d'] := d (+ SH for CK3). The unchanged
consumer.feasible then tests alpha * p + beta * q <= d^2 with alpha = g (PS: alpha = 1 and p already scaled) and
beta = 0. Rows keep their original keys.

F2 (P\\09_redesign\\DESIGN_NOTES_v01.md 6.4e; stand-in P\\09_redesign\\m3_plant_surrogate\\surrogate_v01.py
RunState.feedforward L257-265 and FixServo L274-306): the pedal of the inverse steady-state car model for the plan's
acceleration of the coming tick is added to the PI pedal (inside the anti-windup test as well). The plan's
acceleration is the selected row's 'a' at index tick - k (k = decision tick; 0 or 1); in warm-up, or without a current
plan, the servo's own acceleration reference clipped to [-5, 2]. It reaches the servo in-process (the wire is
unchanged: acceleration field 5). Car-model constants: E_F2_PLANT_v01.json (= m3 PLANT_PARAMS_v01.json).
"""
import copy, hashlib, importlib.util, json, math, pathlib, sys, types
import numpy as np

P = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(P))
import arms_adapter_v02 as arms
import e_sources_v01 as es

native = arms.native
ARMS = ('E_Z', 'E_F0', 'E_N', 'E_CK3', 'E_TG', 'E_PS', 'E_F0_IMM', 'E_N_IMM', 'E_BRAKE')
SOURCE = {'E_Z': 'Z', 'E_F0': 'F0', 'E_N': 'N', 'E_CK3': 'CK3', 'E_TG': 'TG', 'E_PS': 'PS',
          'E_F0_IMM': 'F0_IMM', 'E_N_IMM': 'N_IMM', 'E_BRAKE': 'BRAKE'}
IMM_ARMS = ('E_F0_IMM', 'E_N_IMM')
PBAR_FILE = {'CANMOT': 'E_PBAR_CANMOT_v01.json', 'IMM': 'E_PBAR_IMM_v01.json'}
PLANT_FILE = 'E_F2_PLANT_v01.json'
SCHEMA = 'E_ARM_METHOD_V01'
read = lambda p: json.loads(pathlib.Path(p).read_bytes())


def sha(path):
    h = hashlib.sha256()
    with pathlib.Path(path).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 ** 2), b''): h.update(block)
    return h.hexdigest()


def tracker_of(arm):
    return 'IMM' if arm in IMM_ARMS else 'CANMOT'


def check_knobs(arm, g=None, triple=None, brake_from_k=None):
    if arm not in ARMS: raise ValueError('Unknown E arm: ' + repr(arm))
    def nonneg(name, v):
        v = float(v)
        if not math.isfinite(v) or v < 0: raise ValueError(name + ' must be finite and nonnegative')
        return v
    if arm == 'E_PS':
        if g is not None or triple is None or len(triple) != 3: raise ValueError('E_PS takes --triple g_before,g_braking,g_stopped only')
        triple = [nonneg('triple', x) for x in triple]
        return dict(g=None, triple=triple, brake_from_k=None)
    if triple is not None: raise ValueError('--triple is for E_PS only')
    if arm in ('E_Z', 'E_BRAKE'):
        if g is not None and float(g) != 0.: raise ValueError(arm + ' has g = 0')
        g = 0.
    elif g is None: raise ValueError('--g is required for ' + arm)
    if arm == 'E_BRAKE':
        k = int(brake_from_k if brake_from_k is not None else 199)
        if k < 99 or k % 2 == 0: raise ValueError('brake_from_k must be an odd decision tick >= 99')
        return dict(g=0., triple=None, brake_from_k=k)
    if brake_from_k is not None: raise ValueError('--brake-from-k is for E_BRAKE only')
    return dict(g=nonneg('g', g), triple=None, brake_from_k=None)


# ------------------------------------------------------------------------------------------------ F2 plant inverse
class PlantInverse:
    """m3 plant_v01.Plant.inverse_pedal with G(v) = g0 + g1 v + g2 v^2, C(v) = c0 + c1 v + c2 v^2, brake b1 b + b2 b^2."""

    def __init__(self, params):
        self.p = {k: float(params[k]) for k in ('g0', 'g1', 'g2', 'c0', 'c1', 'c2', 'b1', 'b2')}

    def G(self, v):
        p = self.p; return p['g0'] + p['g1'] * v + p['g2'] * v * v

    def C(self, v):
        p = self.p; return p['c0'] + p['c1'] * v + p['c2'] * v * v

    def inverse_pedal(self, accel, v, max_throttle=.75, max_brake=1.):
        p = self.p
        coast = -self.C(v)
        if accel >= coast:
            return float(min(max_throttle, (accel + self.C(v)) / max(self.G(v), 1e-6)))
        need = coast - accel
        if abs(p['b2']) < 1e-9:
            b = need / p['b1']
        else:
            disc = p['b1'] ** 2 + 4 * p['b2'] * need
            b = (-p['b1'] + np.sqrt(max(disc, 0.))) / (2 * p['b2'])
        return float(-min(max_brake, max(0., b)))


_PI = native.SensorExecution.__init__.__globals__['AccelerationPI']
_AS = sys.modules[_PI.__module__]
_f32 = _AS.f32; _scalars = _AS.scalars; _SIM_DT = _AS.SIM_DT


class F2Servo(_PI):
    """acceleration_servo.AccelerationPI with the F2 feed-forward term (stand-in FixServo with F3 off)."""

    def __init__(self, max_steer, ctx, plant):
        super().__init__(max_steer, .15, .02, .75, 1.)
        self.ctx = ctx; self.inv = plant

    def feedforward(self, tick, raw_speed, accel_ref):
        plan = self.ctx.f2_plan
        if plan is not None and tick - plan['k'] in (0, 1):
            a_ff = float(plan['a_cmd'][tick - plan['k']]); source = 'plan'
        else:
            a_ff = max(-5., min(2., accel_ref)); source = 'reference'
        return self.inv.inverse_pedal(a_ff, max(raw_speed, 0.)), a_ff, source

    def step(self, tick, raw_speed, raw_acceleration, reported_dt=_SIM_DT):
        if self.failed: raise RuntimeError('Latched executor fault')
        try:
            _scalars(raw_speed, raw_acceleration, reported_dt)
            if reported_dt != _SIM_DT or not -.1 <= raw_speed <= 20: raise ValueError('Outside declared observation domain')
            ref = self.reference.step(tick); stopped = abs(raw_speed) < .1 and ref['endpoint_speed_mps'] == 0.
            before = self.integral; accel_ref = (ref['reference_speed_mps'] - raw_speed) / reported_dt
            error = accel_ref - raw_acceleration; _scalars(accel_ref, error)
            ff, a_ff, ff_source = self.feedforward(tick, raw_speed, accel_ref); _scalars(ff)
            trial = self.integral + self.integral_per_tick * error
            trial_pedal = ff + self.proportional * error + trial
            _scalars(trial, trial_pedal)
            blocked = (trial_pedal > self.max_throttle and error > 0) or (trial_pedal < -self.max_brake and error < 0)
            if stopped:
                self.integral = 0.; throttle = 0.; brake = 1.; unclamped = None; pedal = None
            else:
                if not blocked: self.integral = trial
                unclamped = ff + self.proportional * error + self.integral
                pedal = max(-self.max_brake, min(self.max_throttle, unclamped))
                throttle = max(pedal, 0.); brake = max(-pedal, 0.)
            normalized = ref['steer'] / self.reference.max_steer
            control = dict(throttle=_f32(throttle), brake=_f32(brake), steer=_f32(max(-1., min(1., normalized))), reverse=False, hand_brake=False,
                           manual_gear_shift=False)
            return dict(control=control, reference=ref, raw_speed_mps=raw_speed, raw_acceleration_mps2=raw_acceleration,
                        acceleration_reference_mps2=accel_ref, acceleration_error_mps2=error,
                        integral_before=before, integral_trial=trial, integral_state=self.integral, integration_blocked=blocked,
                        pedal=pedal, unclamped_pedal=unclamped, stop_hold=stopped,
                        f2_feedforward_pedal=ff, f2_feedforward_accel=a_ff, f2_source=ff_source)
        except Exception:
            self.failed = True; raise


# ------------------------------------------------------------------------------------------------ per-episode context
class ECtx:
    """State shared by the arm's policy, its constraint builder and the F2 servo during one episode."""

    def __init__(self, arm, knobs, pbar, desired):
        self.arm = arm; self.source = SOURCE[arm]; self.g = knobs['g']; self.triple = knobs['triple']
        self.brake_from_k = knobs['brake_from_k']; self.pbar = pbar; self.desired = float(desired)
        self.hist = es.OnlineHist(); self.tick = None; self.phase = None; self.phase_info = None; self.phase_scale = None
        self.selected = None; self.f2_plan = None; self.records = []; self.n_flushed = 0; self.shifted = None

    def on_detector(self, tracks, events):
        self.hist.update(tracks, events)

    def pending_records(self):
        out = self.records[self.n_flushed:]; self.n_flushed = len(self.records)
        return out


def _json_safe(x):
    """Plain JSON values; non-finite floats become None (the probe writes with allow_nan=False)."""
    if isinstance(x, dict): return {str(k): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [_json_safe(v) for v in x]
    if isinstance(x, (bool, str)) or x is None: return x
    if isinstance(x, (int, np.integer)): return int(x)
    v = float(x)
    return v if math.isfinite(v) else None


def _policy_class(ctx):
    step = native.SensorPolicy.step
    build = step.__globals__['build_library']                     # finite_primitive.build_library
    lib_scope = build.__globals__
    original_library = lib_scope['original_library']; original_constraints = lib_scope['constraints_for_trajectory']
    if original_library.__globals__.get('constraints_for_trajectory') is not original_constraints: raise ValueError('Native constraint builder differs')
    cm = types.SimpleNamespace(finite_array=original_constraints.__globals__['finite_array'], check_psd=original_constraints.__globals__['check_psd'])
    support = original_constraints.__globals__['support']
    finite_array = cm.finite_array
    original_choose = step.__globals__['choose']                   # native_capture_v02.finite_choose
    command_bytes = step.__globals__['command_bytes']

    def e_constraints(tr, actors, ego_length, ego_width, now, diag):
        tr = es.constraints_full(cm, support, tr, actors, ego_length, ego_width, now, diag)
        d, s = es.apply_source(tr, actors, now, ctx.source, ctx.pbar, ctx.hist, ctx.phase_scale)
        if ctx.source == 'CK3' and ctx.shifted is None:
            ctx.shifted = es.ck3_shift(tr, actors, now, ctx.hist)[1]
        for key in ('e_n', 'e_te', 'e_oi', 'e_j'): del tr[key]
        tr['p'] = finite_array(s); tr['d'] = finite_array(d)
        return tr

    library = arms._rebind(original_library, constraints_for_trajectory=e_constraints)
    e_build = arms._rebind(build, original_library=library, constraints_for_trajectory=e_constraints)

    def e_choose(rows, alpha, beta, diagnostics, steer=0., selection_sink=None):
        if ctx.source == 'BRAKE' and ctx.tick >= ctx.brake_from_k:
            # consumer.choose's fallback branch and native_capture_v02.finite_choose's export, forced
            row = next(r for r in rows if r['targets'] == (-5., -5.))
            output = dict(candidate=-1, targets=row['targets'], fallback=True, wire=command_bytes(row['command_speed'], steer))
            if selection_sink is not None: selection_sink(copy.deepcopy(row), copy.deepcopy(output))
        else:
            output = original_choose(rows, alpha, beta, diagnostics, steer, selection_sink=selection_sink)
            row = next(r for r in rows if r['targets'] == (-5., -5.)) if output['fallback'] else rows[output['candidate']]
        if tuple(row['targets']) != tuple(output['targets']): raise ValueError('E selection export differs')
        ctx.selected = dict(targets=tuple(float(x) for x in row['targets']), a=np.array(row['a'][:2], dtype=np.float64))
        return output

    e_step = arms._rebind(step, build_library=e_build, choose=e_choose)

    class EPolicy(native.SensorPolicy):
        __doc__ = 'Native 712 SensorPolicy with the E arm constraint builder and selection record (' + ctx.arm + ')'

        def step(self, tick, raw_speed, raw_acceleration, steer, now, actors, selection_sink=None):
            ctx.tick = tick; ctx.selected = None; ctx.shifted = None
            ctx.phase = ctx.phase_info = None; ctx.phase_scale = None
            if tick >= 99 and ctx.source == 'PS':
                ctx.phase, ctx.phase_info = es.phase_of(actors, now, ctx.hist)
                ctx.phase_scale = ctx.triple[ctx.phase]
            result = e_step(self, tick, raw_speed, raw_acceleration, steer, now, actors, selection_sink=selection_sink)
            if result['mode'] == 'assessment':
                if ctx.selected is None: raise ValueError('E selection missing')
                ctx.f2_plan = dict(k=tick, a_cmd=ctx.selected['a'].copy())
                rec = dict(tick=tick, now=float(now), arm=ctx.arm, source=ctx.source, alpha=self.alpha, beta=self.beta, g=ctx.g,
                           phase=ctx.phase, phase_scale=ctx.phase_scale, phase_info=ctx.phase_info,
                           ck3_shifted_actors=ctx.shifted, targets=list(ctx.selected['targets']), fallback=bool(result['output']['fallback']),
                           a_cmd=[float(x) for x in ctx.selected['a']], n_actors=len(actors),
                           forced_fallback=bool(ctx.source == 'BRAKE' and tick >= ctx.brake_from_k))
                ctx.records.append(_json_safe(rec))
            else:
                ctx.f2_plan = None
            return result

    return EPolicy


def load_pbar(tracker):
    path = P / PBAR_FILE[tracker]
    data = read(path)
    pbar = {k: np.asarray(v, dtype=np.float64) for k, v in data['Pbar'].items()}
    if set(pbar) != {'vehicle', 'pedestrian'} or any(v.shape != (4, 4) for v in pbar.values()): raise ValueError('Pbar file differs')
    return pbar, sha(path)


def build_execution(arm, case, length, width, max_steer, frames, g=None, triple=None, brake_from_k=None):
    """Executor (type native.SensorExecution, F2 servo installed), method record, episode context."""
    knobs = check_knobs(arm, g, triple, brake_from_k)
    consumer, desired = case['consumer'], case['desired_mps']
    if consumer != 'finite' or frames != 700: raise ValueError('E arms use the 700-frame finite selector only')
    tracker = tracker_of(arm)
    pbar, pbar_sha = load_pbar(tracker)
    plant_params = read(P / PLANT_FILE)['params']
    ctx = ECtx(arm, knobs, pbar, desired)
    policy_class = _policy_class(ctx)
    alpha = 1. if arm == 'E_PS' else knobs['g']; beta = 0.
    execution = arms._execution_with_policy(policy_class, consumer, desired, length, width, max_steer, alpha, beta, frames)
    execution.adapter = F2Servo(max_steer, ctx, PlantInverse(plant_params))
    if type(execution) is not native.SensorExecution: raise ValueError('Unexpected executor type')
    rule = ('feasible iff d>=0 and alpha*p<=d^2 for every constraint (149 consumer.feasible, beta=0), with p := s_A of the arm '
            'and, for E_CK3, d := d + SH; E_BRAKE forces the fallback from brake_from_k')
    method = dict(schema=SCHEMA, arm=arm, source=SOURCE[arm], tracker=tracker, knobs=knobs, alpha=alpha, beta=beta,
                  constructor=dict(consumer=consumer, desired_mps=desired, ego_length_m=length, ego_width_m=width, max_steer_rad=max_steer, frames=frames,
                                   execution_class='policy_capture_v01.SensorExecution', policy_class='e_arms_v01.EPolicy', adapter_class='e_arms_v01.F2Servo'),
                  feasibility=rule, pbar_file=PBAR_FILE[tracker], pbar_sha256=pbar_sha, plant_file=PLANT_FILE, plant_sha256=sha(P / PLANT_FILE),
                  f2=dict(feedforward='inverse steady-state pedal of the plan acceleration a[tick-k], k the decision tick; warm-up: clip(accel_ref,-5,2)',
                          plant_params={k: plant_params[k] for k in ('g0', 'g1', 'g2', 'c0', 'c1', 'c2', 'b1', 'b2')}),
                  ck3=dict(a0=es.CK_A0, vmin=es.VMIN), tg=dict(r0=es.TG_R0),
                  phase=dict(stop_v=es.PHASE_STOP_V, brake_a=es.PHASE_BRAKE_A, lead_rule='nearest predicted centre ahead (x>0) with |y|<=%.2f m' % es.LEAD_LATERAL_M),
                  f5_applied=False, acceleration_allowance=False,
                  e_sources_sha256=sha(P / 'e_sources_v01.py'), e_arms_sha256=sha(__file__))
    return execution, json.loads(json.dumps(method, allow_nan=False)), ctx


def make_capture_class(arm):
    """The 747 ordered-capture bridge admitting native.SensorExecution (arms_adapter_v02._make_capture_class_v01 with this
    arm's label); the source binding includes every bound packet file."""
    arms.require_release()
    exec_type = native.SensorExecution
    path = arms.R / '747_full_scenario_binding_20261103/outcome_bridge_v01.py'; sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location('e_capture_' + arm, path); original = importlib.util.module_from_spec(spec); spec.loader.exec_module(original)
    extra = {v['path']: v['sha256'] for v in read(P / 'RUNTIME_SOURCE_BINDING_SMOKE_v01.json')['files']}
    for source in (P / 'RELEASE_SMOKE_v01.json', P / 'RUNTIME_SOURCE_BINDING_SMOKE_v01.json'): extra[source.relative_to(arms.R).as_posix()] = sha(source)

    def source_binding():
        for name, digest in extra.items():
            if sha(arms.R / name) != digest: raise ValueError('E source changed: ' + name)
        return dict(native.source_binding(), **extra)

    class ArmCaptureBridge(original.EpisodeBridge):
        def __init__(self, execution, episode, base_frame, local, backup, mode):
            if mode != 'LIVE_SIX_FAMILY_DEVELOPMENT' or type(execution) is not exec_type: raise ValueError('Arm execution differs')
            fn = original.EpisodeBridge.__init__; scope = dict(fn.__globals__); scope.update(SensorExecution=exec_type, source_binding=source_binding)
            types.FunctionType(fn.__code__, scope, fn.__name__, fn.__defaults__, fn.__closure__)(self, execution, episode, base_frame, local, backup, mode)

    return ArmCaptureBridge, dict(original_capture_sha256=sha(path), arm=arm, execution_type=exec_type.__name__, source_bindings=extra,
                                  original_capture_methods_unchanged=True, package='E', paper_go=False)
