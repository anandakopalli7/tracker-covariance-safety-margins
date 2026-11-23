import numpy as np, time
from rc_core import *
data={r:load_record(r) for r in RUNS}
rs=RunSet(data,RUNS)
print('n eval',sum(rs.n_eval))
# engine vs library
q=rs.d[3]; C=q['cN']; G=breakpoints([C])
c1,sx=scoring_3s(q); masks=[np.ones(len(C),bool)]
t=time.time(); A=stats_curve(C,G,c1,sx,q['vbar'],q['des'],q['idx55'],masks); print('t',time.time()-t,len(G))
idx=np.random.default_rng(1).choice(len(G),300,replace=False)
sel=L.select_grid(C,G[idx],q['idx55']); B=L.stats_scored(sel,c1,sx,q['vbar'],q['des'],masks)
print('max diff',np.abs(A[idx]-B).max())
# also at breakpoints just above/below
for gg in [0.0, G[5]+1e-9, G[7]-1e-9, 1000.]:
    sel=L.select_grid(C,np.array([gg]),q['idx55']); B=L.stats_scored(sel,c1,sx,q['vbar'],q['des'],masks)
    j=np.searchsorted(G,gg,'left') if gg in G else np.searchsorted(G,gg,'left')
    print(gg, 'ok' if gg in G else 'not a bp (cmp at next bp)', np.abs(A[min(j,len(G)-1)]-B[0]).max())
# whole gridless for CV0 record
def run(names):
    Cs={n:[q[n] for q in rs.d] for n in names}
    out={}
    for n in names:
        G,T=source_stats(rs,Cs[n],scoring_3s,lambda q:[np.ones(len(q['k']),bool)])
        out[n]=(G,T)
    return out
t=time.time()
S=run(['cF0','cE','cN','cCK3'])
print('time',time.time()-t)
Td={nm:S[c][1].sum(axis=0)[:,0,:] for nm,c in [('F0','cF0'),('E','cE'),('N','cN'),('CK3','cCK3')]}
print({k:len(v[0]) for k,v in S.items()})
ev=L.eval_scoring(Td,['N','CK3'])
print('R_pp',ev['denE']/201,'RR_N',ev['D']['N']/ev['denE'],'RR_CK3',ev['D']['CK3']/ev['denE'],'n',ev['n'])
