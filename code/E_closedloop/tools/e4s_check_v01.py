"""Package E, set E4: check the smoke (A11 §6d.6(3)) after its runs are fetched (fetch_e_v01.py with the e4s job ids).
Reads runs\\ only; computes no study value (the smoke runs are not study runs).

 1. A1 admission (crash, benign) and the control: SUMMARY status as in E1S (CAPTURED_AND_REVIEWED / the admission's expected
    terminal) and the control's 'identical' flag in the worker status record.
 2. The 4 masked runs (E_F0, E_N, E_F0_IMM, E_N_IMM at lo, c1109_tune_0000): status CAPTURED_AND_REVIEWED; review terminal PASS;
    perception PASS for the CANMOT arms; the E record's dropout block; ARM_METHOD dropout = the law (src_v04 e_dropout_v01);
    every detection row's masked / tracker_rows follow it; punish_num = 3; at least one masked row inside the window.
 3. Non-dropout identity: e4s_<tag>_repro_e3_c1109_eval_0480_e_f0_lo vs E3's e3_c1109_eval_0480_e_f0_lo, field by field on the
    deterministic content: detections (k, frame, time, model, tracks, combined_hash), e_decisions (all fields), frames
    (k, frame, time, state, execution), evaluation_truth (k, frame, time, ego, target, scenario_actors, directional_gap_m).
    Wall-clock fields (inference_s, clock receipts, inventory hashes) are excluded.

python -I e4s_check_v01.py --tag v01 [--out out\\E4S_CHECK_v01.json]
"""
import argparse, json, pathlib, sys

E = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(E / 'src_v04'))
import e_dropout_v01 as D   # noqa: E402

# CARLA's absolute frame counter depends on the simulator session (like a wall clock): it is excluded from the identity and
# required instead to differ from the reference by ONE constant offset on every row of every file.
FIELDS = {'detections.jsonl': ('k', 'time', 'model', 'tracks', 'combined_hash'),
          'e_decisions.jsonl': None,
          'frames.jsonl': ('k', 'time', 'state', 'execution'),
          'evaluation_truth.jsonl': ('k', 'time', 'ego', 'target', 'scenario_actors', 'directional_gap_m')}


def jl(p):
    with open(p, encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def cap_of(run):
    c = list((E / 'runs' / run / 'x' / run / 'capture').glob('*'))
    return c[0] if len(c) == 1 else None


def review_terminal(run):
    for p in (E / 'runs' / run / 'x' / run).rglob('terminal.json'):
        try: return json.loads(p.read_text(encoding='utf-8'))
        except Exception: pass
    return None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='v01'); ap.add_argument('--out', default=str(E / 'out' / 'E4S_CHECK_v01.json'))
    a = ap.parse_args(); t = a.tag
    rep = dict(schema='E4S_CHECK_V01', masked_runs={}, repro=None, admission={})
    ok = True
    for run in sorted(p.name for p in (E / 'runs').glob(f'a1e13_e4s_*_{t}_*')) + sorted(p.name for p in (E / 'runs').glob(f'ctl_e4s_*_{t}_*')):
        s = json.loads((E / 'runs' / run / 'SUMMARY.json').read_text(encoding='utf-8'))
        rep['admission'][run] = dict(status=s.get('status'), control_identical=(s.get('comparison_to_reference') or {}).get('identical'))
    for arm in ('e_f0', 'e_n', 'e_f0_imm', 'e_n_imm'):
        run = f'e4s_{t}_{arm}_lo'; r = dict(); rep['masked_runs'][run] = r
        sp = E / 'runs' / run / 'SUMMARY.json'
        if not sp.exists(): r['error'] = 'not fetched'; ok = False; continue
        s = json.loads(sp.read_text(encoding='utf-8')); r['status'] = s['status']
        cap = cap_of(run); term = review_terminal(run)
        r['review'] = None if term is None else term.get('status'); r['review_stages'] = None if term is None else term.get('stages')
        m = json.loads((cap / 'ARM_METHOD_v01.json').read_text(encoding='utf-8')).get('dropout')
        cid = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['id']
        mask, windows = D.mask_for_case(cid, m['n_updates'])
        det = jl(cap / 'detections.jsonl')
        follows = all(bool(x.get('masked')) == bool(mask[D.tick_index(x['k'])]) and x.get('tracker_rows') == (0 if mask[D.tick_index(x['k'])] else len(x['model'])) for x in det)
        r.update(case=cid, law=(m['mask'] == [int(v) for v in mask] and m['windows'] == [list(w) for w in windows]), rows_follow_mask=follows,
                 punish_num=m['punish_num'], masked_rows_in_window=sum(1 for x in det if x['k'] >= 99 and x.get('masked')), rows=len(det))
        good = (s['status'] == 'CAPTURED_AND_REVIEWED' and r['law'] and follows and m['punish_num'] == 3 and r['masked_rows_in_window'] > 0
                and (r['review'] or '').startswith('PASS'))
        if arm in ('e_f0', 'e_n'): good = good and (r['review_stages'] or {}).get('perception', '').startswith('PASS')
        r['pass'] = bool(good); ok &= good
    run = f'e4s_{t}_repro_e3_c1109_eval_0480_e_f0_lo'; ref = 'e3_c1109_eval_0480_e_f0_lo'
    ca, cb = cap_of(run), cap_of(ref); rr = dict(run=run, reference=ref, files={})
    if ca is None or cb is None: rr['error'] = 'capture missing'; ok = False
    else:
        allsame = True; offsets = set()
        for f, flds in FIELDS.items():
            A, B = jl(ca / f), jl(cb / f)
            if flds is not None: offsets |= {x.get('frame') - y.get('frame') for x, y in zip(A, B) if x.get('frame') is not None and y.get('frame') is not None}
            if flds is not None: A = [{k: x.get(k) for k in flds} for x in A]; B = [{k: x.get(k) for k in flds} for x in B]
            same = A == B
            first = None if same else next((i for i, (x, y) in enumerate(zip(A, B)) if x != y), min(len(A), len(B)))
            rr['files'][f] = dict(rows=[len(A), len(B)], identical=same, first_difference_row=first); allsame &= same
        mA = json.loads((ca / 'ARM_METHOD_v01.json').read_text(encoding='utf-8')); rr['no_dropout_record'] = mA.get('dropout') is None
        rr['frame_offsets'] = sorted(offsets)
        rr['pass'] = bool(allsame and rr['no_dropout_record'] and len(offsets) == 1); ok &= rr['pass']
    rep['repro'] = rr; rep['pass'] = bool(ok)
    pathlib.Path(a.out).write_text(json.dumps(rep, indent=1, default=str), encoding='utf-8')
    print(json.dumps(dict(pass_=rep['pass'], masked={k: v.get('pass') for k, v in rep['masked_runs'].items()}, repro=rr.get('pass'),
                          repro_files={k: v['identical'] for k, v in rr.get('files', {}).items()}, admission=rep['admission'])))


if __name__ == '__main__':
    main()
