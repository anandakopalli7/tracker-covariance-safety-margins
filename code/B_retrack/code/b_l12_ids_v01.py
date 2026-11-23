r"""v13 round 2 (AMENDMENT_12 s2.4): the new lead-braking run ids, by session CD's rule (ycheck\y_twin_l12_v13.l12_run_ids, copied):
the 150 non-reserve rows of CD_capture\l12\CASES_L12_v13.json, each replaced by l12\REPLACEMENTS_L12_v13.json (append-only; a
replacement must have the same desired speed) if listed, as pl12_<case>_native, ascending. New file, 22 Nov 2026 (Claude Opus 5.5).
Run folders: <runs root>\<rid>\<rid>\capture\<case>\ with <runs root>\<rid>\LOGS_OK (CD's l_extract_v13.extract_logs layout).
"""
import json, pathlib

WORK = pathlib.Path(__file__).resolve().parents[2]
L12 = WORK / 'CD_capture' / 'l12'


def l12_run_ids():
    X = json.loads((L12 / 'CASES_L12_v13.json').read_text(encoding='utf-8'))
    rp = L12 / 'REPLACEMENTS_L12_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8'))['replacements'] if rp.is_file() else {}
    rows = [r for r in X['cases'] if not r['reserve']]
    assert len(rows) == 150, len(rows)
    res = {r['case']: r for r in X['cases'] if r['reserve']}
    for r in rows:
        if r['case'] in rep:
            assert res[rep[r['case']]]['desired_mps'] == r['desired_mps']
    return sorted('pl12_%s_native' % rep.get(r['case'], r['case']) for r in rows)


def capture_dir(runs_root, rid):
    rd = pathlib.Path(runs_root) / rid / rid
    caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    assert len(caps) == 1, rid
    return rd, caps[0]


def logs_ok(runs_root, rid):
    return (pathlib.Path(runs_root) / rid / 'LOGS_OK').is_file()
