"""Map every colour-eligible (slot 32) armour to the texture the game really loads."""

import sys, pickle, os, json, collections, time, re
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\orf')
import mo2_vfs, esp_mesh_map as E, bsa

SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\a51f92a9-dc4d-4048-b276-0ba2edcd4eb4\scratchpad\orf'

v = mo2_vfs.Vfs()
v._index = pickle.load(open(os.path.join(SP, 'vfsindex.pkl'), 'rb'))
bi = bsa.BsaIndex()
bi.map = pickle.load(open(os.path.join(SP, 'bsaindex.pkl'), 'rb'))

NIFDDS = re.compile(rb'\.[Dd][Dd][Ss]')
BACK = chr(92)


def tex_from_bytes(d):
    out = []
    for m in NIFDDS.finditer(d):
        e = m.end()
        s = e
        while s > 0 and 32 <= d[s - 1] < 127:
            s -= 1
        t = d[s:e].decode('cp1252', 'replace').replace('/', BACK)
        if t.lower().startswith('textures'):
            out.append(t)
    return out


def get_bytes(path):
    """loose first, then BSA -- the real engine precedence."""
    mod, ab = v.resolve(path)
    if ab:
        try:
            return open(ab, 'rb').read(), mod
        except OSError:
            pass
    return bi.read(path)


def main():
    paths = json.load(open(os.path.join(SP, 'plugin_paths.json')))
    census = json.load(open(os.path.join(SP, 'census_final.json')))
    t0 = time.time()
    out, cache, stat = {}, {}, collections.Counter()
    for plug, ppath in paths.items():
        armo, arma, txst = E.build_map(ppath)
        by_edid = {r['edid'].lower(): (fid, r) for fid, r in armo.items() if r['edid']}
        items = {}
        for r in census.get(plug, []):
            if not r.get('n') or 32 not in r['slots']:
                continue
            hit = by_edid.get((r['e'] or '').lower())
            if not hit:
                stat['not in defining plugin'] += 1
                continue
            fid, ar = hit
            # 1. a per-item texture-set swap wins -- that is where colourways live
            tex = E.diffuse_for(ar, txst)
            if tex:
                tex = tex.lower()
            for m in ([] if tex else E.meshes_for(ar, arma)):
                ml = m.lower()
                if '_gnd' in ml or '1stperson' in ml:
                    continue
                key = os.path.join('meshes', m).lower().replace('/', BACK)
                if key not in cache:
                    d, mod = get_bytes(key)
                    # skip the body-skin texture: these outfits embed a body mesh,
                    # and its skin diffuse is not the garment colour
                    cache[key] = ([t for t in tex_from_bytes(d)
                                   if E.is_diffuse(t) and not E.looks_like_skin(t)] if d else [], mod)
                txs, _mod = cache[key]
                if txs:
                    tex = txs[0].lower()
                    break
            items[r['e']] = {'fid': fid, 'n': r['n'], 'tex': tex}
            stat['mapped' if tex else 'NO texture'] += 1
        out[plug] = items
    print('elapsed %.0fs' % (time.time() - t0))
    for k, c in stat.most_common():
        print('   %-28s %d' % (k, c))
    json.dump(out, open(os.path.join(SP, 'tex_map.json'), 'w'))

    inv = collections.Counter()
    for plug, items in out.items():
        for e, d in items.items():
            if d['tex']:
                inv[d['tex']] += 1
    loose = sum(1 for t in inv if v.resolve(t)[1])
    inbsa = sum(1 for t in inv if not v.resolve(t)[1] and t in bi.map)
    print()
    print('distinct diffuse textures: %d   loose %d   in BSA %d   unresolvable %d'
          % (len(inv), loose, inbsa, len(inv) - loose - inbsa))
    pickle.dump(inv, open(os.path.join(SP, 'texinv.pkl'), 'wb'))


if __name__ == '__main__':
    main()
