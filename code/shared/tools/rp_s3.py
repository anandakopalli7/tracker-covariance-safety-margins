"""List the Programme A RunPod network volume over its S3 API (read-only). Secrets are never printed."""
import truststore; truststore.inject_into_ssl()
import json, subprocess, sys, collections, boto3
from botocore.config import Config
BASE = r"<user folder>\programme-a"
def dpapi(path):
    ps = ("$s = Get-Content -Raw '%s' | ForEach-Object { $_.Trim() } | ConvertTo-SecureString;"
          "[Console]::Out.Write([Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)))") % path
    return subprocess.run(["powershell","-NoProfile","-Command",ps],capture_output=True,text=True,check=True).stdout.strip()
def client():
    acc = json.load(open(BASE+r"\s3_access.json"))
    secret = dpapi(BASE+r"\s3_credential.dpapi")
    if secret.startswith("{"):
        secret = json.loads(secret).get("secret_access_key") or json.loads(secret).get("secret")
    return boto3.client("s3", aws_access_key_id=acc["access_key"], aws_secret_access_key=secret,
        region_name="eu-ro-1", endpoint_url="https://s3api-eu-ro-1.runpod.io",
        config=Config(retries={"max_attempts":5}, s3={"addressing_style":"path"})), acc["source_volume"]
if __name__ == "__main__":
    s3, bucket = client()
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    sizes = collections.Counter(); counts = collections.Counter(); npy = collections.Counter()
    tok = None
    while True:
        kw = dict(Bucket=bucket, MaxKeys=1000)
        if tok: kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            k = o["Key"]; pre = "/".join(k.split("/")[:depth])
            sizes[pre] += o["Size"]; counts[pre] += 1
            if k.endswith(".npy") and ("/clean/" in k or "/raw/" in k):
                npy["/".join(k.split("/")[:-2])] += 1
        if not r.get("IsTruncated"): break
        tok = r["NextContinuationToken"]
    for p, s in sorted(sizes.items(), key=lambda x: -x[1])[:60]:
        print(f"{s/1e9:8.2f} GB {counts[p]:8d} files  {p}")
    print("--- sweep folders (clean/raw .npy):", len(npy))
    for p, c in sorted(npy.items())[:40]: print(c, p)
