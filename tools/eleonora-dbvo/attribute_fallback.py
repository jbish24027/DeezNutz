"""Second pass: attribute .fuz names that no ACTIVE plugin explains.

The audit only saw the DEEZ CS NUTZ - PBR profile. A recording can belong to a mod
whose plugin is installed but disabled in that profile (or disabled entirely), so
this sweeps every .esp/.esm/.esl under mods\\ and Stock Game\\Data regardless of
profile, and reports which mod folder holds a plugin that asks for the name.
"""
import os, sys, pickle, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vfs, winners
from attribute import dbvo_name


def every_plugin():
    """(path, plugin filename, owning mod) for every plugin file on disk."""
    for mod in sorted(os.listdir(vfs.MODS)):
        d = os.path.join(vfs.MODS, mod)
        if not os.path.isdir(d):
            continue
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for n in names:
            if n.lower().endswith(('.esp', '.esm', '.esl')):
                yield os.path.join(d, n), n, mod
    try:
        for n in os.listdir(vfs.DATA):
            if n.lower().endswith(('.esp', '.esm', '.esl')):
                yield os.path.join(vfs.DATA, n), n, '<Stock Game>'
    except OSError:
        pass


def main(wanted_lower):
    hits = collections.defaultdict(lambda: collections.defaultdict(set))
    n_plug = 0
    for path, plug, mod in every_plugin():
        n_plug += 1
        if n_plug % 500 == 0:
            sys.stderr.write('  ...%d plugins\n' % n_plug)
        try:
            for key, line, edid, fid in winners.scan(path, plug):
                if not line or not line.strip():
                    continue
                nm = dbvo_name(line).lower()
                if nm in wanted_lower:
                    hits[nm][mod].add(plug)
        except Exception:
            continue
    sys.stderr.write('scanned %d plugin files\n' % n_plug)
    return hits


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    wanted = pickle.load(open(os.path.join(here, 'unmatched.pkl'), 'rb'))
    h = main(set(wanted))
    out = {k: {m: sorted(v) for m, v in d.items()} for k, d in h.items()}
    pickle.dump(out, open(os.path.join(here, 'fallback.pkl'), 'wb'))
    sys.stderr.write('resolved %d of %d unmatched names\n' % (len(out), len(wanted)))
