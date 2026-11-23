# Independent second program for the nuScenes adapter check (A10 10.1(b)). Written from ADAPTER_SPEC_F_v01 sections 1-5.
import sys, json, math, time, re, datetime
import numpy as np
ROOT = r'ARS_TRIAL\revision_v13'
D = ROOT + r'\data\nuscenes\v1.0-trainval'
F = ROOT + r'\work\F_nuscenes'
sys.path[:0] = [F + r'\lib\code149', F + r'\lib\vendor149']
import finite_primitive, consumer

T_START = time.time()
L_EGO, W_EGO, HALF_WB = 4.084, 1.730, 1.294


def stream_records(path):
    """Yield top-level dict records of a pretty-printed one-key-per-line JSON array."""
    buf = []
    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            if not buf and line.rstrip('\n') in ('[', ']'):
                continue
            buf.append(line)
            if line.rstrip('\n') in ('}', '},'):
                txt = ''.join(buf).rstrip().rstrip(',')
                buf = []
                yield json.loads(txt)


dec = json.load(open(F + r'\notes\ADAPTER_CHECK_DECISIONS_v01.json'))['decisions']
scene_names = sorted({d['scene'] for d in dec})

# check train split (text read only)
src = open(F + r'\lib\devkit\python-sdk\nuscenes\utils\splits.py', encoding='utf-8').read()


def split_list(name):
    m = re.search(r"^" + name + r"\s*=\s*\\?\s*\[(.*?)\]", src, re.S | re.M)
    return set(re.findall(r"scene-\d+", m.group(1)))


train = split_list('train_detect') | split_list('train_track')  # splits.py: train = sorted(set(train_detect + train_track))
assert len(train) == 700, len(train)
assert all(s in train for s in scene_names), 'non-train scene'

scenes = {s['name']: s for s in json.load(open(D + r'\scene.json')) if s['name'] in scene_names}
samples_all = {s['token']: s for s in json.load(open(D + r'\sample.json'))}
cal = {c['token']: c for c in json.load(open(D + r'\calibrated_sensor.json'))}
sens = {s['token']: s for s in json.load(open(D + r'\sensor.json'))}
lidar_cal = {t for t, c in cal.items() if sens[c['sensor_token']]['channel'] == 'LIDAR_TOP'}

scene_samples = {}
for n, sc in scenes.items():
    lst = []
    tok = sc['first_sample_token']
    while tok:
        s = samples_all[tok]
        lst.append(s)
        tok = s['next']
    scene_samples[n] = lst
tok2scene = {s['token']: n for n, l in scene_samples.items() for s in l}
del samples_all

sweeps = {n: [] for n in scenes}
for r in stream_records(D + r'\sample_data.json'):
    if r['sample_token'] in tok2scene and r['calibrated_sensor_token'] in lidar_cal:
        sweeps[tok2scene[r['sample_token']]].append(r)
need_pose = {r['ego_pose_token'] for l in sweeps.values() for r in l}
poses = {}
for r in stream_records(D + r'\ego_pose.json'):
    if r['token'] in need_pose:
        poses[r['token']] = r

sample_set = set(tok2scene)
anns = {}
by_sample = {}
for r in stream_records(D + r'\sample_annotation.json'):
    if r['sample_token'] in sample_set:
        anns[r['token']] = r
        by_sample.setdefault(r['sample_token'], []).append(r)
inst = {i['token']: i for i in json.load(open(D + r'\instance.json'))}
catname = {c['token']: c['name'] for c in json.load(open(D + r'\category.json'))}
TRUTH_CATS = {'vehicle.car', 'vehicle.truck', 'vehicle.bus.bendy', 'vehicle.bus.rigid', 'vehicle.trailer',
              'vehicle.motorcycle', 'vehicle.bicycle', 'human.pedestrian.adult', 'human.pedestrian.child',
              'human.pedestrian.construction_worker', 'human.pedestrian.police_officer'}


def qyaw(q):
    w, x, y, z = q
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


# ---------------- rectangle distance (own implementation) ----------------
def corners(cx, cy, hl, hw, h):
    c, s = math.cos(h), math.sin(h)
    return [(cx + c * a - s * b, cy + s * a + c * b) for a, b in ((hl, hw), (-hl, hw), (-hl, -hw), (hl, -hw))]


def pt_seg(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    dd = dx * dx + dy * dy
    t = 0.0 if dd == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / dd))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def sat_overlap(P, Q):
    for poly in (P, Q):
        for i in range(4):
            x0, y0 = poly[i]
            x1, y1 = poly[(i + 1) % 4]
            nx, ny = -(y1 - y0), (x1 - x0)
            p = [nx * x + ny * y for x, y in P]
            q = [nx * x + ny * y for x, y in Q]
            if max(p) < min(q) or max(q) < min(p):  # strictly separated on this axis
                return False
    return True


def rect_dist(P, Q):
    if sat_overlap(P, Q):
        return 0.0
    best = float('inf')
    for A, B in ((P, Q), (Q, P)):
        for v in A:
            for i in range(4):
                best = min(best, pt_seg(v, B[i], B[(i + 1) % 4]))
    return best


# ---------------- per-scene processing ----------------
class Scene:
    pass


def build_scene(name):
    S = Scene()
    S.name = name
    sps = scene_samples[name]
    t0 = sps[0]['timestamp']
    S.kf_t = np.array([(s['timestamp'] - t0) * 1e-6 for s in sps])
    S.kf_tok = [s['token'] for s in sps]
    sw = sorted(sweeps[name], key=lambda r: r['timestamp'])
    S.sw = sw
    S.sw_t = np.array([(r['timestamp'] - t0) * 1e-6 for r in sw])
    pos = np.array([poses[r['ego_pose_token']]['translation'][:2] for r in sw])
    psi = np.unwrap(np.array([qyaw(poses[r['ego_pose_token']]['rotation']) for r in sw]))
    S.psi = psi
    c = pos + HALF_WB * np.stack([np.cos(psi), np.sin(psi)], 1)
    S.c = c
    n = len(sw)
    travel = np.zeros(n)
    for k in range(n - 1):
        h = 0.5 * (psi[k] + psi[k + 1])
        travel[k + 1] = travel[k] + (c[k + 1] - c[k]) @ np.array([math.cos(h), math.sin(h)])
    vraw = np.zeros(n)
    araw = np.zeros(n)
    for i in range(n):
        tau = S.sw_t - S.sw_t[i]
        m = np.abs(tau) <= 0.5 + 1e-9
        A = np.stack([np.ones(m.sum()), tau[m], tau[m] ** 2], 1)
        coef = np.linalg.lstsq(A, travel[m], rcond=None)[0]
        vraw[i] = coef[1]
        araw[i] = 2 * coef[2]
    S.vraw, S.araw = vraw, araw
    S.desired = float(np.clip(vraw.max(), 1.0, 20.0))
    V = [c[0]]
    T = [psi[0]]
    for i in range(1, n):
        d = c[i] - V[-1]
        if np.hypot(*d) >= 0.25 and d @ np.array([math.cos(psi[i]), math.sin(psi[i])]) > 0:
            V.append(c[i])
            T.append(psi[i])
    V = np.array(V)
    T = np.array(T)
    first = V[0] - 400 * np.array([math.cos(T[0]), math.sin(T[0])])
    last = V[-1] + 400 * np.array([math.cos(T[-1]), math.sin(T[-1])])
    V = np.vstack([first, V, last])
    T = np.concatenate([[T[0]], T, [T[-1]]])
    seg = V[1:] - V[:-1]
    ln = np.hypot(seg[:, 0], seg[:, 1])
    S.V, S.T, S.seg, S.len, S.u = V, T, seg, ln, seg / ln[:, None]
    S.S = np.concatenate([[0.0], np.cumsum(ln)])
    S.nvert = len(V) - 2
    return S


def project(S, q):
    q = np.asarray(q, float)
    w = q - S.V[:-1]
    tau = np.clip((w * S.seg).sum(1) / (S.len ** 2), 0, 1)
    p = S.V[:-1] + tau[:, None] * S.seg
    d = np.hypot(*(q - p).T)
    i = int(np.argmin(d))  # first minimum -> lowest index on ties
    t = tau[i]
    pp = p[i]
    u = S.u[i]
    s = S.S[i] + t * S.len[i]
    l = u[0] * (q[1] - pp[1]) - u[1] * (q[0] - pp[0])
    th = S.T[i] + t * (S.T[i + 1] - S.T[i])
    return s, l, th


def ann_info(a):
    return (a['translation'][0], a['translation'][1], qyaw(a['rotation']))


def truth_at(S, t, k_ann):
    kf = S.kf_t
    k = int(np.searchsorted(kf, t, side='right')) - 1
    if k < 0:
        return None
    a = k_ann.get(k)
    if abs(t - kf[k]) <= 1e-9 and a is not None:
        return ann_info(a)
    if a is None or not a['next']:
        return None
    nx = anns.get(a['next'])
    if nx is None or k + 1 >= len(kf) or nx['sample_token'] != S.kf_tok[k + 1]:
        return None
    w = (t - kf[k]) / (kf[k + 1] - kf[k])
    x0, y0, yw0 = ann_info(a)
    x1, y1, yw1 = ann_info(nx)
    return (x0 + w * (x1 - x0), y0 + w * (y1 - y0), yw0 + w * wrap(yw1 - yw0))


def scene_truth(S):
    inst_ann = {}
    for k, tok in enumerate(S.kf_tok):
        for a in by_sample.get(tok, []):
            if catname[inst[a['instance_token']]['category_token']] in TRUTH_CATS:
                inst_ann.setdefault(a['instance_token'], {})[k] = a
    return inst_ann


# ---------------- main ----------------
out = []
cache = {}
for d in dec:
    name = d['scene']
    if name not in cache:
        S = build_scene(name)
        S.inst_ann = scene_truth(S)
        cache[name] = S
    S = cache[name]
    ts = d['sweep_timestamp_us']
    cand = [i for i, r in enumerate(S.sw) if r['timestamp'] == ts]
    assert len(cand) == 1, (name, ts)
    i = cand[0]
    now = float(S.sw_t[i])
    assert abs(now - d['now_s_from_first_keyframe']) < 1e-6
    v_raw, a_raw = float(S.vraw[i]), float(S.araw[i])
    v0 = max(0.0, v_raw)
    a0 = a_raw
    s_e, l_e, th_e = project(S, S.c[i])
    kb = int(np.searchsorted(S.kf_t, now, side='right')) - 1
    actors = []
    for itok, kann in S.inst_ann.items():
        if truth_at(S, now, kann) is None:
            continue
        a = kann.get(kb)
        actors.append((itok, kann, a['size'][1] / 2, a['size'][0] / 2))
    rows = finite_primitive.build_library(v0, a0, S.desired, [], L_EGO, W_EGO, now, consumer.Diagnostics())
    tracks = []
    for itok, kann, hl, hw in actors:
        frames = []
        for j in range(61):
            tr = truth_at(S, now + 0.05 * j, kann)
            if tr is None:
                break
            s, l, th = project(S, (tr[0], tr[1]))
            frames.append((s - s_e, l, tr[2] - th))
        tracks.append((hl, hw, frames))
    clears = []
    clears_v01 = []
    targets = []
    ndrop = 0
    for r in rows:
        sr = np.asarray(r['s'], float)
        targets.append([float(x) for x in r['targets']])
        best_old = float('inf')
        best_new = float('inf')
        for hl, hw, frames in tracks:
            for j, (x, y, h) in enumerate(frames):
                P = corners(float(sr[j]), 0.0, L_EGO / 2, W_EGO / 2, 0.0)
                Q = corners(x, y, hl, hw, h)
                dd = rect_dist(P, Q)
                if dd < best_old:
                    best_old = dd
                # departure v01 section 2: row ego centre (sr[j], 0), heading 0 -> x_rel = c_x - sr[j];
                # drop the pair when x_rel < 0 (strictly)
                x_rel = x - float(sr[j])
                if x_rel < 0:
                    ndrop += 1
                    continue
                if dd < best_new:
                    best_new = dd
        clears_v01.append('inf' if best_old == float('inf') else best_old)
        clears.append('inf' if best_new == float('inf') else best_new)
    out.append(dict(scene=name, sweep_timestamp_us=ts, keyframe_sample_token=d['keyframe_sample_token'],
                    now=now, v_raw=v_raw, a_raw=a_raw, v0=v0, desired=S.desired,
                    s_e=s_e, l_e=l_e, theta_e=th_e, n_truth_actors=len(actors),
                    n_rows=len(rows), targets=targets, clearance_3s=clears, clearance_3s_v01=clears_v01, n_pairs_dropped=ndrop, route_vertices=S.nvert))
    print(name, now, len(rows), len(actors), ndrop, flush=True)

# ---- verification against v01 output ----
v1 = json.load(open(F + r'\check2\ADAPTER_CHECK2_v01.json'))['records']
assert len(v1) == len(out)
def fv(c):
    return float('inf') if c == 'inf' else float(c)
maxdiff = 0.0
n_ge = True
summary = []
for a, b in zip(out, v1):
    assert a['scene'] == b['scene'] and a['sweep_timestamp_us'] == b['sweep_timestamp_us']
    for x, y in zip(a['clearance_3s_v01'], b['clearance_3s']):
        x, y = fv(x), fv(y)
        if x == y:
            continue
        maxdiff = max(maxdiff, abs(x - y))
    changed = 0
    neg_to_pos = False
    for o, n in zip(a['clearance_3s_v01'], a['clearance_3s']):
        o, n = fv(o), fv(n)
        if n < o:
            n_ge = False
        if n != o:
            changed += 1
        if o <= 0 and n > 0:
            neg_to_pos = True
    summary.append((a['scene'], a['sweep_timestamp_us'], changed, neg_to_pos, a['n_pairs_dropped']))
print('v01 reproduction max abs diff', maxdiff, '; all new >= v01:', n_ge)
for sm in summary:
    print(sm)
res = dict(code='check2_adapter_v02.py', model='Claude Sonnet 5.5',
           written=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
           runtime_s=round(time.time() - T_START, 1), v01_reproduction_max_abs_diff=maxdiff,
           all_new_ge_v01=n_ge, records=out)
OUT = F + r'\check2\ADAPTER_CHECK2_v02.json'
import os
assert not os.path.exists(OUT)
json.dump(res, open(OUT, 'w'), indent=1)
print('done', time.time() - T_START)
