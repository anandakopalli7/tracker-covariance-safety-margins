"""CUDA-first entrypoint for the smoke capture or the independent review.

Adapted from 906 cuda_entry_v01.py: the old pod-id/release check is replaced by
our RELEASE_SMOKE_v01.json gate (status, current RUNPOD_POD_ID, content hashes).
"""
import argparse, json, os, pathlib, resource, runpy, sys

resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
if 'RUNPOD_API_KEY' in os.environ:
    raise ValueError('Account credentials must not enter the sensor process')
P = pathlib.Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('stage', choices=('capture', 'review', 'capture_e', 'review_e'))  # package E (v13): capture_e, review_e
known, remaining = parser.parse_known_args()
release = json.loads((P/'RELEASE_SMOKE_v01.json').read_bytes())
if (release['status'] != 'RELEASED_CLAUDE_SMOKE_V01'
        or not os.environ.get('RUNPOD_POD_ID')
        or release['pod_id'] != os.environ.get('RUNPOD_POD_ID')):
    raise ValueError('Current smoke release and host required')
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
os.environ['OPENBLAS_CORETYPE'] = 'HASWELL'
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import torch
torch.cuda.init()
assert torch.cuda.is_initialized()
target = {'capture': P/'probe_arms_v01.py', 'review': P/'review/review_case_v01.py',
          'capture_e': P/'probe_e_v01.py', 'review_e': P/'review/review_case_e_v01.py'}[known.stage]
sys.path.insert(0, str(target.parent))
sys.argv = [str(target), *remaining]
runpy.run_path(str(target), run_name='__main__')
