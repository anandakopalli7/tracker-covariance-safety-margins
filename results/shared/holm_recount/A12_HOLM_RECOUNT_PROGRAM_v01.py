# RECOVERED PROGRAM (second program, Holm table of the A12 family) -- header added by the coordinating session
# (Claude Opus 5.5) on 22 Nov 2026 in answer to Paper work summary. Everything below the line "# ---- verbatim ----"
# is the program exactly as written and run by a Claude Sonnet 5.5 helper (sub-agent of the coordinator) at 22 Nov 2026 06:34:24 EST (11:34:24Z).
# The helper wrote it with a shell here-document and ran it with python -I; the file was then left outside the project:
#   original file: <user folder>\h2.py  (SHA-256 6daa204289c240d6593f54f3bcca174ea5ed8ee7a77fca0a57f52ae7af43f4a2)
#   transcript:    agent-a1a8b0cf84dab30d6.jsonl, line 34, tool call toolu_011nFo3GQcdT9DHgeutVxQSF
#   transcript body SHA-256 6daa204289c240d6593f54f3bcca174ea5ed8ee7a77fca0a57f52ae7af43f4a2; original file equals transcript body: True
# Independence: the helper's brief said not to read the first program (shared\tools\holm_a12_v01.py) or its output
# (shared\holm\); its tool calls read only AMENDMENT_12_v13.md (lines 394-403 and a heading search) and the export pairs
# (A_EXPORT_* and A_RECOUNT_*) named in the code.
# Reproduction check (coordinator, 22 Nov 2026 19:25:54 EST): this body, run with its output redirected to a scratch file,
# gives A12_HOLM_RECOUNT_v01.json (SHA-256 e2fbd916...0b917dc) exactly, except the "written" time.
# Running this file as is rewrites A12_HOLM_RECOUNT_v01.json with a new "written" time.
# Run: python -I A12_HOLM_RECOUNT_PROGRAM_v01.py  (any working directory; it reads work\ by absolute path)
# ---- verbatim ----
import json,os,hashlib,datetime
W=r"ARS_TRIAL\revision_v13\work"
def get(d,key):
    for src in (d,d.get("values",{}) if isinstance(d.get("values"),dict) else {}):
        if key in src: return src[key]
        cur=src;ok=True
        for part in key.split("."):
            if isinstance(cur,dict) and part in cur: cur=cur[part]
            else: ok=False;break
        if ok: return cur
    # nested with partial dotted keys
    def rec(cur,prefix):
        if isinstance(cur,dict):
            for k,v in cur.items():
                kk=k if not prefix else prefix+"."+k
                if kk==key: return v
                if key.startswith(kk+"."):
                    r=rec(v,kk)
                    if r is not None: return r
        return None
    return rec(d,"")
def load(p): return json.load(open(os.path.join(W,p),encoding="utf-8"))
spec=[("DR2","F_nuscenes/out/{}_DR2.json","DR2.p_r","pl",None),
("DOSE","F_nuscenes/out/{}_DR2.json","DR2.slope.p","pl",None),
("Y1","CD_capture/out/{}_YN.json","YN.p_one_sided","k","YN.p_count_finite"),
("IMM2","B_retrack/out/{}_B.json","B.IMM2N.p_one_sided","k","B.IMM2N.p_n_finite"),
("M1","F_nuscenes/out/{}_M.json","M.p","pl",None),
("E5","E_closedloop/out/{}_E5.json","E5.p_one","k",None)]
R={}
for id,path,key,conv,nkey in spec:
    a=get(load(path.format("A_EXPORT")),key);b=get(load(path.format("A_RECOUNT")),key)
    na=nb=None
    if nkey: na=get(load(path.format("A_EXPORT")),nkey);nb=get(load(path.format("A_RECOUNT")),nkey)
    agree=(a==b) and na==nb
    p=a
    if conv=="pl": n=20000;k=round(p*(n+1))-1
    else:
        n=int(na) if nkey else 20000;k=round(p*n)
    pu=(1+k)/(n+1)
    R[id]=dict(p=p,k=k,n=n,p_u=pu,exports_agree=agree,recount_p=b,key=key,n_export=na,n_recount=nb,convention_of_p="(1+k)/(n+1)" if conv=="pl" else "k/n")
def holm(d):
    ids=sorted(d,key=lambda i:d[i]);m=len(ids);run=0;out={}
    for j,i in enumerate(ids,1):
        run=max(run,min(1,(m-j+1)*d[i]));out[i]=run
    return out
h=holm({i:R[i]["p"] for i in R});hu=holm({i:R[i]["p_u"] for i in R})
for i in R: R[i].update(p_holm=h[i],p_u_holm=hu[i],reject_0_05=h[i]<=0.05,reject_u_0_05=hu[i]<=0.05)
R={"results":R,"model":"Claude Sonnet 5.5","written":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
o=W+r"\shared\holm_recount\A12_HOLM_RECOUNT_v01.json"
open(o,"w",encoding="utf-8").write(json.dumps(R,indent=1))
print(hashlib.sha256(open(o,"rb").read()).hexdigest())
for i,v in R["results"].items(): print(i,v["p"],v["k"],v["n"],v["p_u"],v["p_holm"],v["p_u_holm"],v["reject_0_05"],v["reject_u_0_05"],v["exports_agree"],v["n_export"])
