"""Attribute every generated .fuz to the mod(s) whose live player dialogue asks for it.

Builds the full winner map for the whole load order (not just the missing lines),
turns each winning string into its DBVO filename, and records which mod owns the
plugin that wins it. Cached in attribute.pkl.
"""
import os, sys, pickle, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vfs, winners
from dbvoname import dbvo_name

def build():
    pp = vfs.plugin_paths()
    order = winners.load_order()
    # (definer, localfid, kind) -> (plugin, text)
    win = {}
    for plug in order:
        ent = pp.get(plug.lower())
        if not ent:
            continue
        try:
            for key, line, edid, fid in winners.scan(ent[0], plug):
                win[key] = (plug, line, fid)
        except Exception as e:
            sys.stderr.write('skip %s: %r\n' % (plug, e))
    sys.stderr.write('winning dialogue strings: %d\n' % len(win))

    # filename -> {mod: {plugin, ...}}   plus one representative text / formid
    name_mods = collections.defaultdict(lambda: collections.defaultdict(set))
    name_text = {}
    name_fid = collections.defaultdict(set)
    for ((definer, lfid), kind), (plug, line, fid) in win.items():
        if not line or not line.strip():
            continue
        n = dbvo_name(line)
        mod = pp.get(plug.lower(), (None, '<unknown>'))[1]
        name_mods[n.lower()][mod].add(plug)
        name_text.setdefault(n.lower(), line)
        name_fid[n.lower()].add(fid & 0xFFFFFF)
    return ({k: {m: sorted(v) for m, v in d.items()} for k, d in name_mods.items()},
            name_text,
            {k: sorted(v) for k, v in name_fid.items()})


if __name__ == '__main__':
    nm, txt, fid = build()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'attribute.pkl'), 'wb') as f:
        pickle.dump({'name_mods': nm, 'name_text': txt, 'name_fid': fid}, f)
    sys.stderr.write('distinct dbvo filenames across the load order: %d\n' % len(nm))
