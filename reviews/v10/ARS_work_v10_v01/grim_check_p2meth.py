from fractions import Fraction as F
import math
cases = [
 ("77.5% of 8290", 8290, F(775,1000), F(1,1000)),
 ("82.7% of 8290", 8290, F(827,1000), F(1,1000)),
 ("0.74% of 152264", 152264, F(74,10000), F(1,10000)),
 ("P25 0.2440 of 9307", 9307, F(2440,10000), F(1,10000)),
 ("P50 0.4977 of 9307", 9307, F(4977,10000), F(1,10000)),
 ("P75 0.7456 of 9307", 9307, F(7456,10000), F(1,10000)),
]
for name,n,rep,unit in cases:
    lo_h, hi_h = rep-unit/2, rep+unit/2   # half rounding interval
    lo_t, hi_t = rep, rep+unit            # truncation interval
    ks_h=[k for k in range(math.floor(lo_h*n)-2, math.ceil(hi_h*n)+3) if lo_h<=F(k,n)<=hi_h]
    ks_t=[k for k in range(math.floor(lo_t*n)-2, math.ceil(hi_t*n)+3) if lo_t<=F(k,n)<hi_t]
    kb=math.floor(rep*n); 
    below=F(kb,n); above=F(kb+1,n)
    print(name, "half:",[ (k, float(F(k,n))) for k in ks_h], "trunc:", [(k,float(F(k,n))) for k in ks_t])
    print("   straddle:", kb, float(below), kb+1, float(above), " interval half", float(lo_h), float(hi_h), "trunc", float(lo_t), float(hi_t))
print(1127/152264, 151137/152264, 6427/8290, 6857/8290)
print(1-0.05**(1/130))
# basic interval for RR(N)
th=0.00122; lo=-0.00108; hi=0.00119
print("basic", 2*th-hi, 2*th-lo)
th=0.0068; lo=-0.0061; hi=0.0065
print("basic D/201", 2*th-hi, 2*th-lo, (2*th-hi)/(1116.91/201), (2*th-lo)/(1116.91/201))
