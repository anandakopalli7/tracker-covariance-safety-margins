# RECOVERED PROGRAM (second program, Holm table of the A13 family) -- header added by the coordinating session
# (Claude Opus 5.5) on 22 Nov 2026 in answer to Paper work summary. Everything below the line "# ---- verbatim ----"
# is the program exactly as written and run by a Claude Sonnet 5.5 helper (sub-agent of the coordinator) at 22 Nov 2026 09:04:15 EST (14:04:15Z).
# The helper wrote it with a shell here-document and ran it with python -I; the file was then left outside the project:
#   original file: <user folder>\h.py  (SHA-256 1de275413b17f1a358acceeb6c4075f20a998be7cacc299c3db9336625f499d0)
#   transcript:    agent-a55f2644b21807d91.jsonl, line 29, tool call toolu_01PEPFgX5mnNRhZcn86DX58E
#   transcript body SHA-256 1de275413b17f1a358acceeb6c4075f20a998be7cacc299c3db9336625f499d0; original file equals transcript body: True
# Independence: the helper's brief said not to read the first program (shared\tools\holm_a13_v01.py) or its output
# (shared\holm\); its tool calls read only AMENDMENT_13_v13.md (lines 81-120 and a search) and the export pairs
# (A_EXPORT_* and A_RECOUNT_*) named in the code.
# Reproduction check (coordinator, 22 Nov 2026 19:25:54 EST): this body, run with its output redirected to a scratch file,
# gives A13_HOLM_RECOUNT_v01.json (SHA-256 a984f843...77c943d8) exactly, except the "written" time.
# Running this file as is rewrites A13_HOLM_RECOUNT_v01.json with a new "written" time.
# Run: cd revision_v13\work, then python -I shared\holm_recount\A13_HOLM_RECOUNT_PROGRAM_v01.py  (paths are relative to work\)
# ---- verbatim ----
import json,hashlib,datetime,sys
b='.'
def get(f,key):
    v=json.load(open(f))['values']
    if key in v: return v[key]
    x=v
    for p in key.split('.'): x=x[p]
    return x
def pair(a,b_,key):
    x,y=get(a,key),get(b_,key); return x,y
e,e2=pair('E_closedloop/out/A_EXPORT_E6.json','E_closedloop/out/A_RECOUNT_E6.json','E6.p_one')
c,c2=pair('F_nuscenes/out/A_EXPORT_DRF.json','F_nuscenes/out/A_RECOUNT_DRF.json','DRF.delta.p')
n=20000
def rec(p,ag):
    k=round(p*(n+1)-1); pu=(1+k)/(n+1); return dict(p=p,k=k,n=n,p_u=pu,exports_agree=ag)
R={'E6':rec(e,e==e2),'COAST':rec(c,c==c2)}
def holm(ps):
    o=sorted(ps,key=lambda t:t[1]);m=len(o);run=0;res={}
    for i,(nm,p) in enumerate(o):
        run=max(run,min(1,(m-i)*p));res[nm]=run
    return res
h=holm([(k,v['p']) for k,v in R.items()]);hu=holm([(k,v['p_u']) for k,v in R.items()])
for k,v in R.items():
    v['p_holm']=h[k];v['p_u_holm']=hu[k];v['reject_0_05']=h[k]<=0.05;v['reject_u_0_05']=hu[k]<=0.05
    v={kk:v[kk] for kk in ['p','k','n','p_u','p_holm','p_u_holm','reject_0_05','reject_u_0_05','exports_agree']};R[k]=v
R['model']='Claude Sonnet 5.5';R['written']=datetime.datetime.now().isoformat(timespec='seconds')
f='shared/holm_recount/A13_HOLM_RECOUNT_v01.json'
open(f,'w').write(json.dumps(R,indent=2))
print(json.dumps(R),hashlib.sha256(open(f,'rb').read()).hexdigest())
