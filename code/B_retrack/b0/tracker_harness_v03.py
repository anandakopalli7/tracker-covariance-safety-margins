"""Step 1: exact offline tracker harness, v03 = v02 (Haswell BLAS kernel, local stand-ins for missing packages)
+ correctly rounded sin/cos/atan2 on the tracker path (m4_exact_math_v01.install), replacing this laptop's Windows
math library whose last-bit errors were the cause of the v02 residual (<= 8.9e-16) in runs with turned objects.

Usage: python -I -B -X utf8 tracker_harness_v03.py <mode> [out_csv] [parts]
   mode  = 'one:<cap dir>' | 'sel20' | 'all'
   parts = comma list out of mm,nu,nd,ta,pq (default all): which trig call sites are switched (for diagnosis)
Output default: harness_match_<mode>_v03.csv (same columns as v02; column 'blas' = kernel + '+crtrig').
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import m4_common_v02 as C                      # before numpy: pins the BLAS kernel
import tracker_harness_v02 as H                # imports the tracker (setup_codex) and the comparison code
import m4_exact_math_v01 as X

parts = tuple(sys.argv[3].split(',')) if len(sys.argv) > 3 else ('mm', 'nu', 'nd', 'ta', 'pq')
X.install(parts)
H.BLAS = H.BLAS + '+crtrig(' + ','.join(parts) + ')'

if __name__ == '__main__':
    mode = sys.argv[1]
    if not mode.startswith('one:') and len(sys.argv) < 3:
        sys.argv.append('harness_match_%s_v03.csv' % mode)
    H.main()
    print('trig calls', X.calls(), flush=True)
