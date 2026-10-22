"""Map every Devotion FOMOD option to the .esp it keys off, and check that esp against the
active plugin list. Reports options that are APPLICABLE but were NOT installed.
"""
import re, os, io, sys, xml.etree.ElementTree as ET

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ARCH = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\d28e33fc-d149-4807-b06a-e5dc283cde4d\scratchpad\ex\devotion_new'
PROF = r'C:\1. AUTHORIA\profiles\DEEZ CS NUTZ'
INST = r'C:\1. AUTHORIA\mods\Devotion'

cfg = os.path.join(ARCH, 'fomod', 'ModuleConfig.xml')
raw = open(cfg, 'rb').read()
if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
    text = raw.decode('utf-16')
else:
    text = raw.decode('utf-8-sig')
root = ET.fromstring(text)

# active plugins
active = set()
for l in open(os.path.join(PROF, 'plugins.txt'), encoding='utf-8-sig'):
    l = l.strip()
    if l.startswith('*'):
        active.add(l[1:].lower())
# implicit masters + CC live in game Data and are always on
DATA = r'C:\1. AUTHORIA\Stock Game\Data'
for e in os.listdir(DATA):
    el = e.lower()
    if el.endswith(('.esm', '.esl', '.esp')) and (el.startswith('cc') or el in (
            'skyrim.esm', 'update.esm', 'dawnguard.esm', 'hearthfires.esm', 'dragonborn.esm')):
        active.add(el)

# installed file set (lowercased relative paths)
installed = set()
for dp, dn, fn in os.walk(INST):
    for f in fn:
        if f.lower() == 'meta.ini':
            continue
        installed.add(os.path.relpath(os.path.join(dp, f), INST).lower())


def dest_paths(files_el):
    """destination paths an option installs (lowercased), walking source folders on disk."""
    out = []
    if files_el is None:
        return out
    for el in files_el:
        src = el.get('source', '').replace('/', '\\')
        dest = el.get('destination', '').replace('/', '\\')
        ap = os.path.join(ARCH, src)
        if el.tag == 'folder':
            if os.path.isdir(ap):
                for dp, dn, fn in os.walk(ap):
                    for f in fn:
                        rel = os.path.relpath(os.path.join(dp, f), ap)
                        out.append(os.path.join(dest, rel).lower().lstrip('\\'))
        else:
            base = os.path.basename(src)
            d = dest if dest else base
            if dest.endswith('\\'):
                d = os.path.join(dest, base)
            out.append(d.lower().lstrip('\\'))
    return out


rows = []
for si, st in enumerate(root.iter('installStep')):
    sname = st.get('name', '').strip()
    for g in st.iter('group'):
        gname = g.get('name', '').strip()
        for p in g.iter('plugin'):
            pname = p.get('name', '').strip()
            deps = [fd.get('file') for fd in p.iter('fileDependency')]
            paths = dest_paths(p.find('files'))
            present = [q for q in paths if q in installed]
            rows.append({
                'step': sname, 'group': gname, 'option': pname,
                'esp': deps, 'n_files': len(paths),
                'n_present': len(present),
            })

print('total options: %d' % len(rows))
print()
print('=== APPLICABLE (a required esp is ACTIVE) but NOT INSTALLED ===')
gap = 0
for r in rows:
    if r['n_files'] == 0:
        continue
    esp_active = [e for e in r['esp'] if e and e.lower() in active]
    if esp_active and r['n_present'] == 0:
        gap += 1
        print('  %-52s needs %s  [ACTIVE] -> %d file(s) NOT installed' % (r['option'][:52], esp_active, r['n_files']))
if not gap:
    print('  (none — every option whose quest mod you have is already installed)')

print()
print('=== INSTALLED but the required esp is NOT active (stale//harmless) ===')
stale = 0
for r in rows:
    if r['n_files'] == 0 or r['n_present'] == 0:
        continue
    if r['esp'] and not any(e and e.lower() in active for e in r['esp']):
        stale += 1
        print('  %-52s needs %s  [NOT ACTIVE]' % (r['option'][:52], r['esp']))
if not stale:
    print('  (none)')

print()
print('=== NOT installed and esp not active (correctly skipped) — count only ===')
n = sum(1 for r in rows if r['n_files'] and r['n_present'] == 0 and not any(e and e.lower() in active for e in r['esp']))
print('  %d options' % n)
for r in rows:
    if r['n_files'] and r['n_present'] == 0 and not any(e and e.lower() in active for e in r['esp']):
        print('     %-50s needs %s' % (r['option'][:50], r['esp']))
