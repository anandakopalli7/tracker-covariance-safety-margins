"""Revision v13, AMENDMENT_12 sec. 3a: the first program's two result files as ONE `values` dict, for the comparison with the second
program (which writes one file). New file, 22 Nov 2026 (Claude Opus 5.5, session F); the pre-lock test did the same inline
(out_a12\\TESTOLD_DR2_FIRST_MERGED_v01.json). Computes nothing: a key present in both files must hold the same value, else it refuses.
  out_a12\\p010\\DR2_RESULTS_v01.json (dr_analysis_v02, DR0-DR2 at p = 0.10) + out_a12\\DR2_DOSE_v01.json (dr_dose_v01, dose-response
  and decomposition) -> out_a12\\DR2_FIRST_MERGED_v01.json   (refuses to overwrite; refuses PENDING_CALIB inputs)
Usage: python -I dr_merge_first_v01.py
"""
import hashlib, json, pathlib, time
DRD = pathlib.Path(__file__).resolve().parent.parent
A = DRD / 'out_a12' / 'p010' / 'DR2_RESULTS_v01.json'
B = DRD / 'out_a12' / 'DR2_DOSE_v01.json'
OUT = DRD / 'out_a12' / 'DR2_FIRST_MERGED_v01.json'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    if OUT.exists(): raise SystemExit('REFUSED: %s exists' % OUT)
    va = json.loads(A.read_text(encoding='utf-8'))['values']
    vb = json.loads(B.read_text(encoding='utf-8'))['values']
    clash = [k for k in va if k in vb and va[k] != vb[k]]
    if clash: raise SystemExit('REFUSED: keys in both files with different values: %s' % clash)
    v = dict(va); v.update(vb)
    doc = dict(code='dr_merge_first_v01.py', sources={str(A.relative_to(DRD)): sha(A), str(B.relative_to(DRD)): sha(B)},
               shared_keys=sorted(k for k in va if k in vb), written=time.strftime('%Y-%m-%d %H:%M:%S'), values=v)
    OUT.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('WROTE', OUT, len(v), 'values', sha(OUT))


if __name__ == '__main__':
    main()
