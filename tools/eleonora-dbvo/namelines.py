"""Every live player topic that carries a player-name token.

DBVO looks the .fuz up by the text the GAME shows, so a topic containing
<Alias=Player> needs one recording per player name. This lists them all,
attributed to the winning plugin/mod, with the name substituted in.
"""
import os, sys, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vfs, winners as W
from pasrepro import should_ignore

TOKEN = re.compile(r'<[^<>]{0,80}>')
PLAYERISH = re.compile(
    r'^<alias(?:\.(?:shortname|basename|fullname))?='
    r'(player[a-z]*|pc|dragonborn|db|hero|listener|thePlayer)>$', re.I)


def build():
    pp = vfs.plugin_paths()
    win = {}
    for plug in W.load_order():
        ent = pp.get(plug.lower())
        if not ent:
            continue
        try:
            for key, line, edid, fid in W.scan(ent[0], plug):
                win[key] = (plug, line, edid, fid)
        except Exception as e:
            sys.stderr.write('skip %s: %r\n' % (plug, e))
    sys.stderr.write('winning dialogue strings: %d\n' % len(win))

    rows = []
    for (key, kind), (plug, line, edid, fid) in win.items():
        if not line:
            continue
        s = line.strip()
        if not s or should_ignore(s, edid, fid):
            continue
        toks = TOKEN.findall(s)
        if not toks:
            continue
        if not any(PLAYERISH.match(t) for t in toks):
            continue
        mod = pp.get(plug.lower(), (None, '<unknown>'))[1]
        rows.append({'text': s, 'plugin': plug, 'mod': mod, 'edid': edid,
                     'fid': '%06X' % (fid & 0xFFFFFF), 'kind': kind,
                     'tokens': toks})
    return rows


if __name__ == '__main__':
    rows = build()
    rows.sort(key=lambda r: (r['mod'].lower(), r['text'].lower()))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'namelines.json')
    json.dump(rows, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    sys.stderr.write('player-name topics: %d in %d mods\n'
                     % (len(rows), len({r['mod'] for r in rows})))
