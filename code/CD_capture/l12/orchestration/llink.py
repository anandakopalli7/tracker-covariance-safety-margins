"""L12 twin of xlink.py: create the one link that l_pods_v13's LINKS lacks (trk_arrays_v01 puts the openloop folder of record on
sys.path by its full Windows path, a single file name on Linux), then run setup and accept. No frozen file is changed (as X-4).
Usage: python llink.py POD"""
import sys, pathlib
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.path[:0] = [str(CD / 'l12'), str(CD / 'tools')]
import l_pods_v13 as LP
name = sys.argv[1]
win = r'<library folder>\openloop'
cmd = "mkdir -p %s/job && cd %s/job && ( [ -L '%s' ] || ln -s %s/P/09_redesign/m2_decisions/openloop '%s' ) && ls -la | grep -c openloop" % (LP.R, LP.R, win, LP.R, win)
try:
    print('link', LP.BP.ssh(name, cmd).strip())
except SystemExit as e:
    print('link step (before the bundle exists):', str(e)[:200])
LP.setup(name)
LP.BP.ssh(name, cmd)
LP.accept(name)
