# imm2_v02.py: imm2_v01 plus kappa_CA (A11 section 6 stage 2)

Copy of imm2_v01.py. Only change: in `derive_matrices`, if the constants dict has `kappa_ca`, Q_CA diagonal entries at
CA indices `KAPPA_CA_IDX = (0, 1, 2, 6, 7, 8)` are multiplied by it. Absent key: no change. CLI as v01:
`python -I -B -X utf8 imm2_v02.py <cap_dir> <constants_json> <diag> <out_json>` (OPENBLAS_CORETYPE=Haswell).

## Index choice
CA order [x, y, z, w, l, h, vx, vy, vz, ax, ay, az, yaw]. Position terms = 0,1,2; velocity terms = 6,7,8. Not scaled: sizes
3,4,5, accelerations 9,10,11 (sigma_a2), yaw 12.
Text relied on: A11 section 6: "A new, additive library constant kappa_CA multiplies only the CA filter's position and velocity
process-noise terms"; spec section 1: "Q_CA ... entries at 9, 10, 11 = sigma_a2" and section 3 (B2) "velocity block ... CV indices 6, 7, 8"
(precedent that velocity includes vz). z and vz are included for the same reason.
Ambiguity: whether z (2) and vz (8) count. They do not enter P9's x,y,vx,vy block (no coupling in F or the diagonal Q),
but they enter the 9-dim mode likelihood, so they can change mu. Changing the tuple is one line.

## Tests (old data, fit_finite_0012, trk_constants_v01.json, diag 0.95)
- No kappa_ca: out_v02.json byte-identical to out_v01.json (cmp).
- kappa_ca = 0.5: output differs (first difference at char 2117). Outputs in scratch_v02/.
