"""Add two records to the exports of packages C and D, after the frozen exporter has written them (it writes `deviations: []` and no
hypothesis statuses). Computes no value; never changes `values` or any other field (checked; else REFUSED, file untouched).
New file, 20 Nov 2026 (Claude Opus 5.5); replaces add_deviations_cd_v13.py (never run on a real export).

1. `deviations`: the A10 sec. 11 records of out/DEVIATIONS_CD_v13.json, in all four exports (A_EXPORT_C/D, A_RECOUNT_C/D).
2. `outcomes` (C exports only): the hypothesis sequences, each from its own program's output, with A10 sec. 9 applied explicitly:
   if the gate of a sequence (H0 for lead braking, K0 for cut-in) fails, the gate is reported as "fails: no measurable room" and every
   later item as "not tested" (not as failed): "No measurable room in that data set. Nothing is tested there" (A10 sec. 9).
   Otherwise each item is "passes", "fails" or "not evaluable", with `confirmed` (it and every earlier one passed; A10 sec. 5.3).
   First: analysis/out/C_LEAD_H0_H5_v13.json, C_CUTIN_K0_K2_v13.json. Second: recount/out/RC_C_LEAD_v13.json, RC_C_CUTIN_v13.json.
   The two programs' statuses, confirmations and classifications must be identical (A10 sec. 10.1(c)); else REFUSED.
3. With --status-keys (approved by the coordinator 21 Nov 00:20; names agreed with A 21 Nov): A's status keys and flags are added to
   `values`, in A's vocabulary, each from its own program's outputs, first and second required identical:
   C: LB.H0-LB.H5, CI.K0-CI.K2 = "pass" | "fail" | "recovers" | "uninformative" | "amplitude_limited" | "inconclusive" |
   "not_evaluable" | "not_run" (A10 sec. 9 after a failed K0); flags LB.IMM.barely (H3's "barely varies"; must equal
   LB.IMM.within5 >= 0.95) and CI.Y.barely (from CI.Y.within5; null if that is null).
   D: D1.<const|mild|stopgo>.DH1 / .DH2 = "costs_progress" | "costs_safety" | "no_cost" | "inconclusive".
   A recomputes them from the interval ends and stops on a mismatch. Only new keys are added; no existing key is changed. If H0
   fails, LB.H1-H5 are not exported (A10 sec. 9: the author is consulted).
Writes out/[TESTOLD_]RECORDS_ADDED_v13.json (SHA-256 of each export before and after).
Usage: python -I add_records_cd_v13.py [--test-old] [--status-keys]
"""
import hashlib, json, math, pathlib, sys, time
CD = pathlib.Path(__file__).resolve().parents[1]
OUT = CD / 'out'
TEST = '--test-old' in sys.argv
PFX = 'TESTOLD_' if TEST else ''
DEV = OUT / 'DEVIATIONS_CD_v13.json'
SRC = dict(first=dict(lead=CD / 'analysis' / 'out' / f'{PFX}C_LEAD_H0_H5_v13.json', cutin=CD / 'analysis' / 'out' / f'{PFX}C_CUTIN_K0_K2_v13.json'),
           second=dict(lead=CD / 'recount' / 'out' / f'{PFX}RC_C_LEAD_v13.json', cutin=CD / 'recount' / 'out' / f'{PFX}RC_C_CUTIN_v13.json'))
SEQ = dict(lead=['H0', 'H1', 'H2', 'H3', 'H4', 'H5'], cutin=['K0', 'K1', 'K2'])
GATE_TEXT = dict(lead='No measurable room in the fresh lead-braking runs', cutin='No measurable room at the cut-in event in the fresh runs')
SEC9 = 'A10 sec. 9: "No measurable room in that data set. Nothing is tested there."'
ADDED = ('deviations', 'deviations_source', 'outcomes', 'outcomes_source')


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def num(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else x


def items_first(fam, d):
    out = {}
    for h in SEQ[fam]:
        s = d['sequence'][h]; it = dict(passes=bool(s['passes']))
        if h == 'H3': it['classification'] = d['H3'].get('classification'); it['barely_varies'] = d['H3'].get('barely_varies')
        if h == 'K2':
            if d['K2'].get('status') == 'not evaluable': it['passes'] = None; it['evaluable'] = False
            else: it['evaluable'] = True; it['classification'] = d['K2'].get('classification')
        out[h] = it
    gate = dict(lead=None, cutin=dict(R_gl_lower=num(d['K0']['R_gl']['ci_level'][0]) if fam == 'cutin' else None,
                                      R_gl_level=d['K0']['R_gl'].get('level') if fam == 'cutin' else None,
                                      den0_deceq=num(d['K0']['den0_deceq']) if fam == 'cutin' else None))[fam]
    return out, gate


def items_second(fam, d):
    H = d['hypotheses']; out = {}
    for h in SEQ[fam]:
        x = H[h]; it = dict(passes=None if x.get('passes') is None else bool(x['passes']))
        if h == 'H3': it['classification'] = x.get('classification'); it['barely_varies'] = x.get('barely_varies')
        if h == 'K2':
            if x.get('evaluable') is False: it['passes'] = None; it['evaluable'] = False
            else: it['evaluable'] = True; it['classification'] = x.get('classification')
        out[h] = it
    gate = None
    if fam == 'cutin':
        r = H['K0']['R_gl_pp']; gate = dict(R_gl_lower=num(r['ci'][0]), R_gl_level=r.get('level'), den0_deceq=num(H['K0']['den0_deceq']))
    return out, gate


def statuses(fam, items, gate):
    seq = SEQ[fam]; g = seq[0]; res = {}
    if items[g]['passes'] is not True:
        res[g] = dict(items[g], status='fails: no measurable room', confirmed=False)
        for h in seq[1:]:
            res[h] = dict(status='not tested', reason=f'{g} failed; ' + SEC9, confirmed=False,
                          program_record={k: v for k, v in items[h].items()})
        txt = (f'{GATE_TEXT[fam]} ({g} fails). Nothing is tested there (A10 sec. 9): '
               + ', '.join(seq[1:]) + ' are reported as not tested, not as failed.')
        return dict(gate=g, gate_passes=False, tested=False, statement=txt, gate_values=gate, items=res)
    ok = True
    for h in seq:
        it = items[h]
        st = 'not evaluable' if it.get('evaluable') is False else ('passes' if it['passes'] else 'fails')
        ok = ok and it['passes'] is True
        res[h] = dict(it, status=st, confirmed=ok, label='confirmatory' if ok else 'not confirmatory')
    return dict(gate=g, gate_passes=True, tested=True, gate_values=gate, items=res)


def outcomes(who):
    doc = {}
    for fam in ('lead', 'cutin'):
        d = json.loads(SRC[who][fam].read_text(encoding='utf-8'))
        items, gate = (items_first if who == 'first' else items_second)(fam, d)
        doc['C.lead' if fam == 'lead' else 'C.cutin'] = statuses(fam, items, gate)
    return doc


def comparable(o):
    """Statuses, confirmations, classifications and the gate decision; not the source-specific `program_record` details."""
    return {s: dict(gate_passes=v['gate_passes'], tested=v['tested'],
                    items={h: {k: x for k, x in it.items() if k in ('status', 'confirmed', 'classification', 'evaluable', 'barely_varies')}
                           for h, it in v['items'].items()}) for s, v in o.items()}


A_CLASS = {'recovers': 'recovers', 'uninformative variation': 'uninformative', 'amplitude-limited': 'amplitude_limited',
           'inconclusive': 'inconclusive'}


def status_keys(o):
    """A's optional status keys from one program's outcomes (A's vocabulary, A_text/gen/outcomes_v13.py)."""
    out = {}
    for seq, pre, keys in (('C.lead', 'LB.', ['H0', 'H1', 'H2', 'H3', 'H4', 'H5']), ('C.cutin', 'CI.', ['K0', 'K1', 'K2'])):
        s = o[seq]
        for h in keys:
            it = s['items'][h]
            if it['status'] == 'not tested':
                if seq == 'C.lead': continue                     # H0 failed: the author is consulted; A decides
                out[pre + h] = 'not_run'
            elif it['status'] == 'not evaluable': out[pre + h] = 'not_evaluable'
            elif h in ('H3', 'K2'): out[pre + h] = A_CLASS[it['classification']]
            else: out[pre + h] = 'pass' if it['status'] == 'passes' else 'fail'
            if h == 'H3' and it['status'] != 'not tested' and it.get('barely_varies') is not None:
                out['LB.IMM.barely'] = bool(it['barely_varies'])   # A10 sec. 5.3 H3 flag; name agreed with A (21 Nov 01:0x)
    return out


D_SRC = dict(first=CD / 'analysis' / 'out' / f'{PFX}D_NONBRAKING_DH1_DH2_v13.json', second=CD / 'recount_d' / 'out' / f'{PFX}RC_D_NONBRAKING_v13.json')
D_VAR = dict(constant='const', mild_braking='mild', stop_and_go='stopgo')
D_WORD = {'costs progress': 'costs_progress', 'costs safety': 'costs_safety', 'no measurable cost': 'no_cost', 'inconclusive': 'inconclusive'}


def d_status_keys(who):
    """D-H1 / D-H2 per variant (A10 sec. 6) from each D program's own output, in A's vocabulary (D1.<v>.DH1 / .DH2)."""
    d = json.loads(D_SRC[who].read_text(encoding='utf-8')); out = {}
    for kind, short in D_VAR.items():
        x = d['variants'][kind]
        h1, h2 = (x['D_H1'], x['D_H2']) if who == 'first' else (x['D-H1'], x['D-H2'])
        out[f'D1.{short}.DH1'] = D_WORD[h1]; out[f'D1.{short}.DH2'] = D_WORD[h2]
    return out


def y_barely(values):
    """CI.Y.barely (name agreed with A): the 'barely varies' flag of the young-track population from the export's own CI.Y.within5
    (each program's output); null if that value is null (no young-track row)."""
    w = values.get('CI.Y.within5')
    return None if w is None else bool(w >= 0.95)


def main():
    dev = json.loads(DEV.read_text(encoding='utf-8')); items = dev['items']
    oc = dict(first=outcomes('first'), second=outcomes('second'))
    if comparable(oc['first']) != comparable(oc['second']):
        raise SystemExit('REFUSED: first and second programs give different hypothesis statuses:\n'
                         + json.dumps(dict(first=comparable(oc['first']), second=comparable(oc['second'])), indent=1))
    sk = None
    if '--status-keys' in sys.argv:
        vals = {w: json.loads((OUT / f'{PFX}A_{n}_C.json').read_text(encoding='utf-8'))['values'] for w, n in (('first', 'EXPORT'), ('second', 'RECOUNT'))}
        sk = {w: dict(C=dict(status_keys(oc[w]), **{'CI.Y.barely': y_barely(vals[w])}), D=d_status_keys(w)) for w in oc}
        if sk['first'] != sk['second']: raise SystemExit(f'REFUSED: status keys differ: {sk}')
        w5 = vals['first'].get('LB.IMM.within5')
        if w5 is not None and sk['first']['C'].get('LB.IMM.barely') != (w5 >= 0.95):
            raise SystemExit('REFUSED: H3 barely_varies disagrees with LB.IMM.within5 >= 0.95')
    rows = []
    for n in ('A_EXPORT_C', 'A_EXPORT_D', 'A_RECOUNT_C', 'A_RECOUNT_D'):
        p = OUT / f'{PFX}{n}.json'
        if not p.is_file(): raise SystemExit(f'REFUSED: {p.name} missing')
        before = sha(p); doc = json.loads(p.read_text(encoding='utf-8'))
        if doc.get('deviations') not in ([], items): raise SystemExit(f'REFUSED: {p.name} already has other deviations')
        new = dict(doc); new['deviations'] = items; new['deviations_source'] = dict(file=DEV.name, sha256=sha(DEV))
        who = 'first' if 'EXPORT' in n else 'second'; pk = n[-1]
        if n.endswith('_C'):
            new['outcomes'] = oc[who]
            new['outcomes_source'] = dict(rule='A10 sec. 5.3-5.4 sequences; sec. 9 consequence rules applied (a failed gate makes every '
                                               'later item "not tested")', program=who,
                                          files={f: dict(file=str(q.relative_to(CD)), sha256=sha(q)) for f, q in SRC[who].items()},
                                          first_vs_second='identical statuses, confirmations and classifications (checked)')
        if sk is not None:
            vals = dict(doc['values'])
            for k, x in sk[who][pk].items():
                if k in vals and vals[k] != x: raise SystemExit(f'REFUSED: {p.name} already has {k} = {vals[k]!r}')
                vals[k] = x
            new['values'] = dict(sorted(vals.items()))
            new['status_keys_added'] = dict(keys=sorted(sk[who][pk]), rule="A's status keys and flags (RESULTS_INTERFACE_v13 sec. 2; names "
                                            "agreed with A 21 Nov), A's vocabulary, from this program's own outputs; A10 sec. 9 applied "
                                            "(not_run after a failed K0); first and second identical (checked)")
        ADDED_NOW = ADDED + ('status_keys_added',)
        rest = lambda d: {k: v for k, v in d.items() if k not in ADDED_NOW and k != 'values'}
        oldv = lambda d: {k: x for k, x in d.get('values', {}).items() if not (sk is not None and k in sk['first'][pk])}
        if json.dumps(rest(new), sort_keys=True, default=str) != json.dumps(rest(doc), sort_keys=True, default=str) or \
           json.dumps(oldv(new), sort_keys=True, default=str) != json.dumps(oldv(doc), sort_keys=True, default=str):
            raise SystemExit('REFUSED: other fields changed')
        p.write_text(json.dumps(new, indent=1, default=str), encoding='utf-8')
        chk = json.loads(p.read_text(encoding='utf-8'))
        if json.dumps(rest(chk), sort_keys=True, default=str) != json.dumps(rest(doc), sort_keys=True, default=str) or \
           json.dumps(oldv(chk), sort_keys=True, default=str) != json.dumps(oldv(doc), sort_keys=True, default=str):
            raise SystemExit(f'write check failed {p.name}')
        rows.append(dict(file=p.name, sha256_before=before, sha256_after=sha(p), n_values=len(doc.get('values', {})),
                         n_deviations=len(items), outcomes='outcomes' in new))
        print(f'{p.name}: {len(items)} deviation records' + (' + outcomes' if 'outcomes' in new else '') + f'; values unchanged ({len(doc.get("values", {}))})')
    for s, v in oc['first'].items():
        print(s, 'tested' if v['tested'] else 'NOT TESTED', {h: it['status'] for h, it in v['items'].items()})
    (OUT / f'{PFX}RECORDS_ADDED_v13.json').write_text(json.dumps(dict(written=time.strftime('%Y-%m-%d %H:%M:%S'), program=pathlib.Path(__file__).name,
        program_sha256=sha(__file__), deviations_source=DEV.name, deviations_sha256=sha(DEV), files=rows), indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
