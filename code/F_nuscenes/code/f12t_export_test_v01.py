"""Package F (revision v13): test of f12_export_v01 (held-out branch and the fallback branch) on the SYNTHETIC held-out outputs of
f06t2_calib_path_test_v01.py. New file, 20 Nov 2026 (Claude Opus 5.5). Copies the real pre-registered horizon output and the
clear_v02 summary of the design split into the scratch folder (both are design-split files), patches FC.OUT to that folder and
the split gate in this process only, and runs the export twice (in force; --outcome-a). Writes only inside the scratch folder.
Usage: venv\\Scripts\\python.exe -I f12t_export_test_v01.py <scratch dir of f06t2>
"""
import pathlib, sys, shutil
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402

D = pathlib.Path(sys.argv[1])
for f in ('F_HORIZON_RULE_v01.json', 'F_CLEAR_V02_train_v01.json'):
    shutil.copy(FC.OUT / f, D / f)
FC.OUT = D; FC.require_split = lambda split: None
import f12_export_v01 as X                   # noqa: E402
X.FC.OUT = D; X.OUTF = D / 'A_EXPORT_F.json'
for p in (D / 'A_EXPORT_F.json',):
    if p.exists():
        p.unlink()
X.OUTCOME_A = False
X.main()
a = json.loads((D / 'A_EXPORT_F.json').read_text(encoding='utf-8'))
print('in force:', a['values']['F.status'], a['values']['F.clearance'], 'n keys', len(a['values']))
print(' keys:', sorted(a['values'])[:80])
(D / 'A_EXPORT_F.json').rename(D / 'A_EXPORT_F_inforce.json')
X.OUTCOME_A = True
X.DEVIATIONS[0] = dict(X.DEVIATIONS[0])
X.main()
b = json.loads((D / 'A_EXPORT_F.json').read_text(encoding='utf-8'))
print('outcome (a):', b['values']['F.status'], b['values']['F.clearance'], b['values'].get('F.horizon'), 'n keys', len(b['values']))
print('deviation 0 done:', b['values']['deviations'][0]['done'][:80])
