"""Runs ON THE POD (Linux). Places B's recount inputs under the exact path strings the frozen second program builds, and checks every
file's SHA-256 against the laptop's manifest (coordinator condition 2, 20 Nov). New file, 20 Nov 2026 (Claude Opus 5.5).
The frozen code (recount_fresh.py, rf_core.py, b6tu.py) joins Windows path strings with backslashes, e.g.
r'C:\\Users\\...\\CD_capture\\arrays\\CV0\\<rid>.npz'. On Linux such a string is one file name (backslash is an ordinary character), relative
to the working directory /root/rc; a few joins use os.path.join and so contain '/'. Each input is therefore placed at
os.path.join('/root/rc', <the exact string>). Nothing is computed here.
Usage on the pod: python3 pod_place_v02.py /root/stage/manifest.json /root/stage
"""
import hashlib, json, os, shutil, sys

RC = '/root/rc'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    man = json.load(open(sys.argv[1])); stage = sys.argv[2]
    bad = []; n = 0
    for e in man['inputs']:
        tgt = os.path.join(RC, e['flat'])
        d = os.path.dirname(tgt)
        if d:
            os.makedirs(d, exist_ok=True)
        if e.get('marker'):
            open(tgt, 'wb').close()
        else:
            shutil.copyfile(os.path.join(stage, 'in', str(e['i'])), tgt)
        if sha(tgt) != e['sha256']:
            bad.append(e['flat'])
        n += 1
    for c in man['code']:
        shutil.copyfile(os.path.join(stage, 'code', c), os.path.join(RC, c))
        if sha(os.path.join(RC, c)) != man['code_sha256'][c]:
            bad.append(c)
    os.makedirs(os.path.join('/root', 'rc\\out'), exist_ok=True)      # OUTD = HERE + r'\out' with HERE = /root/rc
    print(json.dumps(dict(placed=n, code=len(man['code']), sha_mismatch=bad, all_ok=not bad)))
    sys.exit(0 if not bad else 3)


if __name__ == '__main__':
    main()
