"""Rebuild the project's original folder layout from this repository.

The programs of this deposit expect the layout they were written in (ARS_TRIAL/revision_v13/work/<part>/...).
The repository groups the same files as code/, results/, plans/ and locks/. PROVENANCE_MAP.tsv records, for every
copied file, its original path under the folder ARS_TRIAL. This script copies each file back to that path.
Rows marked "extracted" (tables-only extracts of documents that are not deposited) are skipped: they have no
original file to restore.

Usage:
    python rebuild_tree.py <output folder>

Result: <output folder>/ARS_TRIAL/<original path> for every copied file of PROVENANCE_MAP.tsv, and a count.
Existing files are never overwritten. Unzip the array archives afterwards:
    arrays_B.zip, arrays_CD.zip, arrays_F_dropout.zip, arrays_F_nuscenes.zip  ->  <output folder>/ARS_TRIAL/revision_v13/work/
    arrays_old_runs.zip                                                       ->  <output folder>/ARS_TRIAL/

Standard library only. Written for the deposit (not part of the study's programs).
"""
import os
import shutil
import sys


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    out = os.path.join(os.path.abspath(sys.argv[1]), 'ARS_TRIAL')
    copied = skipped = missing = extracts = 0
    with open(os.path.join(repo, 'PROVENANCE_MAP.tsv'), encoding='utf-8') as f:
        next(f)
        for line in f:
            cols = line.rstrip('\n').split('\t')
            dep, src = cols[0], cols[1]
            if len(cols) > 5 and cols[5] == 'extracted':
                extracts += 1
                continue
            a = os.path.join(repo, *dep.split('/'))
            b = os.path.join(out, *src.split('/'))
            if not os.path.isfile(a):
                missing += 1
                continue
            if os.path.exists(b):
                skipped += 1
                continue
            os.makedirs(os.path.dirname(b), exist_ok=True)
            shutil.copyfile(a, b)
            copied += 1
    print('copied %d, already present %d, missing in the repository %d, extracts skipped %d -> %s' % (copied, skipped, missing, extracts, out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
