import os, sys, struct, json
sys.path.insert(0, '.')
from niflib import Nif
from smp_audit import enabled_mods, walk_files, smp_info, MODS, OVERWRITE
def tree(n):
    parent = {}; info = {}
    for i in n.blocks_of('NiNode'):
        o = n.offsets[i]
        name_i, ned = struct.unpack_from('<II', n.data, o); p = o + 8 + 4*ned + 4 + 4
        tr = struct.unpack_from('<3f', n.data, p); p += 12 + 36 + 4 + 4
        nch, = struct.unpack_from('<I', n.data, p); p += 4
        for c in struct.unpack_from('<%di' % nch, n.data, p):
            if c >= 0: parent[c] = i
        info[i] = (n.s(name_i), tr)
    return parent, info
def orphan_phys(n):
    """non-NPC nodes (physics bones) whose parent is the root node"""
    parent, info = tree(n)
    roots = [i for i in info if i not in parent]
    out = []
    for i, (nm, tr) in info.items():
        if i in roots: continue
        if nm.startswith('NPC ') or nm.startswith('CME ') or nm in ('Scene Root',): continue
        pi = parent.get(i)
        if pi in roots:
            out.append(nm)
    return out, len(info)
mods = enabled_mods()
providers = {}
for prio, (name, root) in enumerate([('overwrite', OVERWRITE)] + [(m, os.path.join(MODS, m)) for m in mods]):
    for rel, full in walk_files(root):
        if rel.endswith('.nif'):
            providers.setdefault(rel, []).append((prio, name, full))
conv = r"C:\1. AUTHORIA\mods\Authoria - UBE Converter Output"
flat = []; ok = 0; checked = 0
for rel, full in walk_files(conv):
    if not rel.endswith('.nif'): continue
    s, x, e = smp_info(full)
    if not s: continue
    checked += 1
    n = Nif(full)
    orph, nn = orphan_phys(n)
    PFX = 'meshes' + chr(92) + '!ube' + chr(92)
    src_rel = ('meshes' + chr(92) + rel[len(PFX):]) if rel.startswith(PFX) else None
    src_orph = None
    if src_rel and src_rel in providers:
        try:
            sn = Nif(sorted(providers[src_rel])[0][2]); src_orph, _ = orphan_phys(sn)
        except Exception as ex:
            src_orph = 'err'
    if orph and (src_orph is None or src_orph == 'err' or len(orph) > len(src_orph)):
        flat.append((rel, len(orph), orph[:4], None if src_orph is None else (len(src_orph) if src_orph != 'err' else 'err')))
    else:
        ok += 1
print('UBE Converter Output SMP-tagged nifs checked: %d ; with physics nodes re-parented to root vs source: %d ; ok: %d' % (checked, len(flat), ok))
for f in sorted(flat):
    print('   %-75s orphan phys nodes=%d e.g. %s | source orphan count=%s' % f)
json.dump(flat, open('ube_flatten_result.json', 'w'), indent=1)
