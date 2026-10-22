"""Intersect the bespoke 'Devotion - PatchHub' mod against everything Devotion 1.5.0e can install."""
import os, io, sys, hashlib, xml.etree.ElementTree as ET
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ARCH = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\d28e33fc-d149-4807-b06a-e5dc283cde4d\scratchpad\ex\devotion_new'
HUB = r'C:\1. AUTHORIA\mods\Devotion - PatchHub'
DEV = r'C:\1. AUTHORIA\mods\Devotion'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def tree(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.lower() == 'meta.ini':
                continue
            ap = os.path.join(dp, f)
            out[os.path.relpath(ap, root).lower()] = ap
    return out


cfg = os.path.join(ARCH, 'fomod', 'ModuleConfig.xml')
raw = open(cfg, 'rb').read()
text = raw.decode('utf-16') if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else raw.decode('utf-8-sig')
root = ET.fromstring(text)


def dest_map(files_el, label, into):
    if files_el is None:
        return
    for el in files_el:
        src = el.get('source', '').replace('/', '\\')
        dest = el.get('destination', '').replace('/', '\\')
        ap = os.path.join(ARCH, src)
        if el.tag == 'folder':
            if os.path.isdir(ap):
                for dp, dn, fn in os.walk(ap):
                    for f in fn:
                        rel = os.path.relpath(os.path.join(dp, f), ap)
                        into[os.path.join(dest, rel).lower().lstrip('\\')].append((label, os.path.join(dp, f)))
        else:
            base = os.path.basename(src)
            d = os.path.join(dest, base) if dest.endswith('\\') else (dest or base)
            into[d.lower().lstrip('\\')].append((label, ap))


arch = defaultdict(list)
dest_map(root.find('requiredInstallFiles'), 'REQUIRED(core)', arch)
for st in root.iter('installStep'):
    for g in st.iter('group'):
        for p in g.iter('plugin'):
            dest_map(p.find('files'), 'opt:' + p.get('name', '').strip(), arch)

hub = tree(HUB)
dev = tree(DEV)

print('archive can install %d distinct destination paths' % len(arch))
print('PatchHub has %d files' % len(hub))
print('installed Devotion has %d files' % len(dev))
print()

inter = sorted(set(hub) & set(arch))
print('=== OVERLAP: PatchHub path also provided by the 1.5.0e archive: %d ===' % len(inter))
for k in inter:
    labels = [l for l, _ in arch[k]]
    same = any(sha(hub[k]) == sha(p) for _, p in arch[k])
    print('  %-72s %s   from %s' % (k, 'IDENTICAL' if same else 'DIFFERENT', labels[:3]))

only_hub = sorted(set(hub) - set(arch))
print()
print('=== ONLY in PatchHub (would be LOST if you retire it): %d ===' % len(only_hub))
for k in only_hub:
    print('  %s  [%d B]' % (k, os.path.getsize(hub[k])))

print()
print('=== PatchHub vs the CURRENTLY INSTALLED Devotion folder ===')
both = sorted(set(hub) & set(dev))
print('paths in both: %d' % len(both))
for k in both:
    print('  %-72s %s' % (k, 'IDENTICAL' if sha(hub[k]) == sha(dev[k]) else 'DIFFERENT'))

print()
print('=== does the archive ship ANY QRM channel file? ===')
ch = [k for k in arch if 'channels' in k]
print('archive channel paths: %d' % len(ch))
for k in sorted(ch)[:20]:
    print('   ', k, '<-', [l for l, _ in arch[k]][:2])
hubch = [k for k in hub if 'channels' in k]
print('PatchHub channel paths: %d' % len(hubch))
for k in sorted(hubch):
    print('   ', k)
