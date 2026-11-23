"""Delimiter listing of the Programme A volume: python -I rp_s3_ls.py <prefix> [<prefix> ...]. Read-only; secrets never printed."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rp_s3 import client
s3, bucket = client()
for pre in (sys.argv[1:] or [""]):
    kw = dict(Bucket=bucket, Prefix=pre, Delimiter="/", MaxKeys=1000)
    r = s3.list_objects_v2(**kw)
    print("==", pre or "<root>")
    for p in r.get("CommonPrefixes", []): print("  D", p["Prefix"])
    for o in r.get("Contents", [])[:200]: print("  F", o["Size"], o["Key"])
    if r.get("IsTruncated"): print("  ... truncated")
