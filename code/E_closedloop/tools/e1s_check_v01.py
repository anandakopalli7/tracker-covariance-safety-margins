"""E1S check (STATUS.md departure 3): did the pod integration list pass? Reads ONLY status fields of the volume SUMMARY.json files
(job status, exits, review status and stages, failure, actor review, policy-failure frame present or not, and for the A1
controls the bit-identity flag). No contact, distance, time or any other outcome of an E1S run is printed or stored.

python -I e1s_check_v01.py [--tag v01] [--pod-suffix 01] [--ssh claude-v13e-01]   (--ssh: read the pod's /opt/claude_main/summaries instead of the volume)
Pass iff every one of the 8 jobs has status CAPTURED_AND_REVIEWED, review status PASS769_RECORDED_SENSOR_EGO_PREFIX, no policy
failure, actor review exit 0, and both A1 controls are bit-identical to their references.
"""
import argparse, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'shared' / 'tools')); sys.path.insert(0, str(HERE))
from rp_s3 import client   # noqa: E402

ROOT = 'claude_v13_e_v01/results/'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='v01'); ap.add_argument('--pod-suffix', default='01'); ap.add_argument('--ssh')
    a = ap.parse_args()
    jobs = json.loads((HERE.parent / 'jobs' / f'JOBS_E1S_claude-v13e-{a.pod_suffix}_{a.tag}.json').read_text(encoding='utf-8'))['jobs']
    if a.ssh:
        import pods_e_v01 as pv
        cmd = "cd /opt/claude_main/summaries && python3 -c \"import json,glob; print(json.dumps({f[:-5]: json.load(open(f)) for f in glob.glob('*.json')}))\""
        r = pv.ssh(a.ssh, cmd, timeout=120)
        remote = json.loads(r.stdout)
        def get(jid):
            runs = sorted(k for k in remote if k == jid or k.startswith(jid + '__'))
            if not runs: raise KeyError(jid)
            return remote[runs[-1]]
    else:
        s3, bucket = client()
        get = lambda jid: json.loads(s3.get_object(Bucket=bucket, Key=f"{ROOT}{jid}/SUMMARY.json")['Body'].read())
    rows = []; ok = True
    for j in jobs:
        try:
            s = get(j['id'])
        except Exception as e:
            rows.append(dict(job=j['id'], missing=True)); ok = False; continue
        ao = s.get('assessment_outcomes') or {}
        r = dict(job=j['id'], arm=s['arm'], status=s['status'], capture_exit=s['capture_exit'], review_exit=s['review_exit'],
                 review_status=s.get('review_status'), review_stages=s.get('review_stages'), actor_review_exit=s['actor_review_exit'],
                 actor_review_status=s.get('actor_review_status'), failure=(s.get('failure') or {}).get('error'),
                 policy_failure=ao.get('first_policy_failure_frame') is not None,
                 control_identical=(s.get('comparison_to_reference') or {}).get('identical') if j.get('role') == 'control' else None,
                 capture_wall_seconds=s.get('capture_wall_seconds'))
        good = (r['status'] == 'CAPTURED_AND_REVIEWED' and r['review_status'] == 'PASS769_RECORDED_SENSOR_EGO_PREFIX' and not r['policy_failure']
                and r['actor_review_exit'] == 0 and (j.get('role') != 'control' or r['control_identical'] is True))
        r['pass'] = good; ok &= good; rows.append(r)
    print(json.dumps(dict(e1s_pass=ok, jobs=rows), indent=1))


if __name__ == '__main__':
    main()
