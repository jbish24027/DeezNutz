"""cuirass_collider: give ANY cuirass nif a public per-triangle collider of its outer surface above the chest, for helmets whose
flap-skirt points name its tag (the coat builder does the same for the cuirasses it builds; this is for cuirasses that are not
built by it - the author's mesh as is, or a mesh already carrying someone's physics). The nif is re-emitted whole: every shape with
its own weights (the shader from a donor copy of the same file when one is given - a PBR patcher's output - else its own), every
custom node the mesh carries (someone's physics bones) re-created, the HDT link set to the XML written here.
  * the collider: from the visible shapes (not 'VirtualGround', not names containing 'coll' / 'Collide'), triangles above `zmin`
    whose face is seen from a point low in the chest (out / up, never a collar's inside), one hidden copy per source shape, the
    source's own weights; the triangle choice is decided on the first weight and reused (the game blends _0 / _1 by index)
  * the XML: an existing XML (physics already there) gets the missing kinematic bone declarations (before its first <bone>, under its
    first bone-default, which must be mass 0) and the shape block before </system>; otherwise a minimal XML of kinematic bones + shape
Design file (run in this module's namespace): STAGE, XD (XML dir, backslashes), WORK, CUIRASSES = {name: dict(src='path with {} for
the weight suffix', weights=('_1', '_0'), out='rel path with {}', donor='path with {}' or None, xml='existing XML path' or None,
xml_out='rel XML path', prefix='HC', zmin=92.0, tag='soscuirass', helm='soshelm', pen=2.0, margin=0.1)}.
usage: cuirass_collider.py <designs.py> [name ...]"""
import os, sys, json, runpy, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
load, Writer, NifFile, NiStringExtraData = C.load, C.Writer, C.NifFile, C.NiStringExtraData
STAGE = XD = WORK = None; CUIRASSES = {}
SKIP_NAMES = ('coll', 'Collide', 'VirtualGround')


def use_designs(path):
    ns = runpy.run_path(os.path.abspath(path).replace(os.sep, '/'), init_globals=dict(globals()))
    for k in ('STAGE', 'XD', 'WORK', 'CUIRASSES'):
        if k in ns: globals()[k] = ns[k]
    for k in ('STAGE', 'WORK'):
        if globals()[k]: globals()[k] = globals()[k].replace(os.sep, '/').rstrip('/') + '/'
    os.makedirs(WORK, exist_ok=True)


def has_shader(u):
    """False for a hidden collision shape without a shader block (PyNifly reports shaderPropertyID 0xFFFFFFFF)"""
    try: return int(u.s.properties.shaderPropertyID) != 0xFFFFFFFF
    except Exception: return False


def collider_tris(T, zmin, shared, log, label):
    """{shape name: triangle mask} of the outer surface above zmin, decided once per design (shared)"""
    vis = [t for t in T if not any(s in t.name for s in SKIP_NAMES) and len(t.tris)]
    big = max(vis, key=lambda t: len(t.pos)); band = big.pos[(big.pos[:, 2] > zmin) & (big.pos[:, 2] < zmin + 25.0)]
    if len(band) < 10: band = big.pos
    cx, cy = float(band[:, 0].mean()), float(band[:, 1].mean()); ctr = np.array([cx, cy, zmin - 6.0]); out = {}
    for i_, t in enumerate(vis):
        key = f'sel_{i_}'                              # by position, not name: the author's shape names carry the weight suffix (ArmorLight2M_1 / _0)
        if key not in shared:
            c = t.pos[t.tris].mean(1); fn = np.cross(t.pos[t.tris[:, 1]] - t.pos[t.tris[:, 0]], t.pos[t.tris[:, 2]] - t.pos[t.tris[:, 0]])
            dv = c - ctr; facing = (fn * dv).sum(1) / (np.linalg.norm(fn, axis=1) * np.linalg.norm(dv, axis=1) + 1e-12)
            shared[key] = (c[:, 2] > zmin) & (facing > 0.05)
        if shared[key].sum() >= 20: out[t.name] = shared[key]
    if not out: raise RuntimeError(f'{label}: no surface above z {zmin} (shapes {[t.name for t in vis]})')
    return out, (cx, cy)


def build(name, D, wt, shared, log):
    src = D['src'].format(wt); out = STAGE + D['out'].format(wt).lower(); p = D.get('prefix', 'HC'); label = f'{name}{wt}'
    n, T = load(src); C.to_world(T)
    donor = {}
    dp = D.get('donor') and D['donor'].format(wt)
    if dp and os.path.exists(dp):
        dn, DT = load(dp); donor = {x.name: x for x in DT}
    elif dp: log.append(f'{label}: donor missing ({dp}) - shaders from the source')
    sel, (cx, cy) = collider_tris(T, float(D.get('zmin', 92.0)), shared, log, label)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    w = Writer(n, out); w.skel_G = {}
    for u in T:
        for nm, xf in u.s2b.items(): w.skel_G.setdefault(nm, np.linalg.inv(C.tb2m(xf)))
    # the mesh's own custom nodes (someone's physics bones): everything that is not a skeleton bone nor the root, parents first
    extra = {nm: nd for nm, nd in n.nodes.items() if not nm.startswith('NPC ') and nm not in (n.rootName, 'Root', 'NPC') and getattr(nd, 'parent', None) is not None}

    def depth(nm):
        d = 0
        while nm in extra: nm = extra[nm].parent.name; d += 1
        return d
    custom = {}
    for nm in sorted(extra, key=lambda x: (depth(x), x)):
        nd = extra[nm]; par = nd.parent.name
        if par.startswith('NPC ') or par in custom:        # a node riding a skeleton bone (or a chain of them): re-created under it, as the author had it
            w.custom_G[nm] = C.tb2m(nd.global_transform); w.parent[nm] = par; custom[nm] = nd
            if par.startswith('NPC ') and par not in w.skel_G: w.skel_G[par] = C.tb2m(nd.global_transform) @ np.linalg.inv(C.tb2m(nd.transform))
            if par not in w.out.nodes and par not in custom: w.node(par, w.skel_G[par], None)
            w.node(nm, w.custom_G[nm], par)
        else:                                              # a node under the root / the 'NPC' node (a skirt bone the skeleton may or may not have): static, added like a skeleton bone
            w.skel_G[nm] = C.tb2m(nd.global_transform)
    nb = {}
    for u in T:
        pid = list(C.part_ids(u, T))
        # someone's hidden collision shapes (coll_body, VirtualGround) carry no shader: re-emitted without one (copying a missing shader
        # wrote a nif that would not open again)
        sf = donor.get(u.name, u) if has_shader(u) else None
        nb[u.name] = w.emit(u.name, u.pos, u.uv, u.norm, u.tris, u.s.flags, pid, [C.top4(x) for x in u.w], u.s2b, shader_from=sf,
                            colors=[tuple(c) for c in u.s.colors] if u.s.colors else None)
    tnames = []
    for u in T:
        if u.name not in sel: continue
        m = sel[u.name]; vv = np.unique(u.tris[m]); rm = np.full(len(u.pos), -1); rm[vv] = np.arange(len(vv)); nm = f'{p} Torso Collide {len(tnames)}'
        ww = [C.top4({b: x for b, x in u.w[i].items() if b.startswith('NPC ')} or u.w[i]) for i in vv]
        nb[nm] = w.emit(nm, u.pos[vv], np.zeros((len(vv), 2)), None, rm[u.tris[m]], 0xe, [32] * int(m.sum()), ww, u.s2b)
        tnames.append((nm, int(m.sum()), len(vv), u.name))
    NiStringExtraData.New(w.out, name='HDT Skinned Mesh Physics Object', string_value=D['xml_out'], parent=w.out.root)
    w.out.save()
    bones = sorted({b for nm_, _, _, _ in tnames for b in NifFile(out).shape_dict[nm_].bone_names} if hasattr(NifFile(out), 'shape_dict') else
                   {b for sh in NifFile(out).shapes if ' Torso Collide' in sh.name for b in sh.bone_names})
    log.append(f'{label}: wrote {out.replace(STAGE, "")}: ' + ', '.join(f'{nm_} = {nt} tris / {nv} pts of {src_}' for nm_, nt, nv, src_ in tnames)
               + f'; axis ({cx:.1f}, {cy:.1f}); custom nodes re-created {len(custom)}; shapes {len(nb)}')
    return dict(out=out, src=src, tris=[(nm_, nt, nv) for nm_, nt, nv, _ in tnames], bones=bones, custom_nodes=len(custom))


def shape_block(nm, D):
    return C.shape('per-triangle-shape', nm, D.get('tag', 'soscuirass'), D.get('margin', 0.1), can=(D.get('helm', 'soshelm'),), pen=D.get('pen', 2.0), shared='public')


def write_xml(name, D, rep, log):
    rel = D['xml_out'].replace('\\', '/'); path = STAGE + rel; os.makedirs(os.path.dirname(path), exist_ok=True)
    bones = sorted({b for r in rep.values() for b in r['bones']}); names = [t[0] for t in next(iter(rep.values()))['tris']]
    head = [f'\t<!-- the cuirass above z {D.get("zmin", 92.0):.0f}: its outer surface as a collider for the Sons of Skyrim helmets\' flap skirts (shared across files:',
            f'\t     the helmets\' collision points name the tag {D.get("tag", "soscuirass")} and this names theirs; nothing in this file meets it) -->']
    if D.get('xml'):
        s = open(D['xml'], encoding='utf-8').read()
        m = re.search(r'<bone-default>\s*<mass>([\d.]+)</mass>', s)
        if not m or float(m.group(1)) != 0.0: raise RuntimeError(f'{name}: the existing XML\'s first bone-default is not mass 0 ({D["xml"]})')
        have = set(re.findall(r'<bone name="([^"]+)"', s)); missing = [b for b in bones if b not in have]
        i = s.index('<bone name=')
        s = s[:i] + ''.join(f'<bone name="{b}"/>\n\t' for b in missing) + s[i:]
        j = s.rindex('</system>')
        s = s[:j] + '\n'.join(head + sum((shape_block(nm, D) for nm in names), [])) + '\n' + s[j:]
        log.append(f'{name}: XML {rel} = the existing physics + {len(missing)} bone declarations + {len(names)} collider shape(s)')
    else:
        L = ['<?xml version="1.0" encoding="UTF-8"?>',
             f'<!-- {name}: no physics of its own - only a public collider of its outer surface above the chest for the Sons of Skyrim helmets\' flap',
             '     skirts (made ' + D.get('date', '2026-10-12') + '). Mesh, UVs and textures are the author\'s, unchanged. -->',
             '<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="description.xsd">', '',
             '\t<!-- kinematic: the body bones the collider is skinned to -->'] + [f'\t<bone name="{b}"/>' for b in bones] + ['']
        L += head + sum((shape_block(nm, D) for nm in names), []) + ['</system>', '']
        s = '\n'.join(L); log.append(f'{name}: XML {rel} = kinematic bones + {len(names)} collider shape(s) (no physics of its own)')
    with open(path, 'w', encoding='utf-8', newline='\r\n') as f: f.write(s)


def main(names):
    rp = WORK + 'cuirass_colliders_report.json'; allrep = json.load(open(rp)) if os.path.exists(rp) else {}; log = []
    try:
        for name in names:
            D = CUIRASSES[name]; shared = {}; rep = {}
            for wt in D.get('weights', ('_1', '_0')): rep[wt] = build(name, D, wt, shared, log)
            tris = {tuple(r['tris']) for r in rep.values()}
            if len(tris) != 1: raise RuntimeError(f'{name}: the weights differ in their collider ({tris})')
            write_xml(name, D, rep, log); allrep[name] = dict(variants=rep, xml=D['xml_out'])
            json.dump(allrep, open(rp, 'w'), indent=1)
    finally:
        open(WORK + 'cuirass_colliders.log', 'w', encoding='utf-8').write('\n'.join(log) + '\n'); print('\n'.join(log))


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    use_designs(sys.argv[1]); main([a for a in sys.argv[2:] if a in CUIRASSES] or list(CUIRASSES))
