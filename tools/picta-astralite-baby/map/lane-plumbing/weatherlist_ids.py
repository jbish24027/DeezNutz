"""Map every WeatherIDs entry of the live Picta-lane _weatherlist.ini to the WTHR records of the current order (24-bit mask)."""
import json, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(HERE, 'wthr_all_picta.jsonl'), encoding='utf-8')][1:]
by24 = collections.defaultdict(list)
for r in rows:
    rt = int(r['runtime_formid'], 16)
    by24[rt & 0xFFFFFF].append((r['formid'], r['runtime_formid'], r.get('editorid')))
WL = r'C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1/enbseries/_weatherlist.ini'
sec = None; secs = {}
for ln in open(WL, encoding='utf-8', errors='replace'):
    t = ln.strip()
    if not t or t.startswith(';'):
        continue
    m = re.match(r'^\[(.+)\]$', t)
    if m:
        sec = m.group(1); secs[sec] = {}; continue
    if '=' in t and sec:
        k, v = t.split('=', 1); secs[sec][k.strip().lower()] = v.strip()
light_hits = []; unresolved = []; multi = []; total = 0
for s, kv in secs.items():
    ids = [x.strip() for x in kv.get('weatherids', '').split(',') if x.strip()]
    for i in ids:
        total += 1
        try:
            v = int(i, 16) & 0xFFFFFF
        except ValueError:
            unresolved.append((s, i, 'bad hex')); continue
        hits = by24.get(v, [])
        if not hits:
            unresolved.append((s, i, kv.get('filename')))
        if len(hits) > 1:
            multi.append((s, i, hits))
        for h in hits:
            if h[1].upper().startswith('FE'):
                light_hits.append((s, i, h))
print('sections', len(secs), 'ids', total)
print('ids routed to a LIGHT-plugin weather (slot-dependent):', len(light_hits))
for x in light_hits:
    print('  ', x)
print('ids matching >1 weather (24-bit collisions):', len(multi))
for x in multi:
    print('  ', x)
print('ids matching no weather in the current order:', len(unresolved))
for x in unresolved:
    print('  ', x)
