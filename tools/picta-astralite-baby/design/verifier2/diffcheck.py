import os, re, hashlib, sys
S = 'C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/design/final/stage/'
DARK = 'C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1'
SHIP = 'C:/1. AUTHORIA/mods/[NoDelete] Picta ENB 1.1.2 - Data (shipped)'
DOF = 'C:/1. AUTHORIA/mods/Authoria - Picta - July Depth of Field (AMON ADOF)'
def L(p): return chr(92) * 2 + '?' + chr(92) + os.path.abspath(p).replace('/', chr(92))
def rd(p): return open(L(p), 'rb').read()
for br in ('alive', 'newly_on'):
    root = S + br + '/Authoria - Picta x Astralite - E11'
    changed = {}; badclamp = []; crlf = []; nfiles = 0
    for dp, dn, fn in os.walk(L(root)):
        for f in fn:
            full = os.path.join(dp, f); rel = full[len(L(root)) + 1:].replace(chr(92), '/')
            if rel == 'manifest.json': continue
            nfiles += 1
            src = None
            for base in (DOF, DARK, SHIP):
                if os.path.exists(L(base + '/' + rel)): src = base + '/' + rel; break
            if rel.endswith('B01_Lightly_Cloudy_PictaPure.ini'): src = DARK + '/enbseries/Picta - Weathers/00_Master/B01_Lightly_Cloudy.ini'
            if src is None: print('NO SOURCE', rel); continue
            a = rd(src); b = open(full, 'rb').read()
            if a == b: continue
            if b.count(b'\r\n') != a.count(b'\r\n') or a.count(b'\n') != b.count(b'\n'): crlf.append(rel)
            al = a.decode('utf-8', 'replace').split('\n'); bl = b.decode('utf-8', 'replace').split('\n'); sec = None
            for x, y in zip(al, bl):
                m = re.match(r'^\[(.+)\]', x.strip())
                if m: sec = m.group(1)
                if x != y:
                    k = y.split('=', 1)[0].strip(); changed.setdefault((sec, re.sub(r'(Dawn|Sunrise|Day|Sunset|Dusk|Night|InteriorDay|InteriorNight)$', '', k), re.search(r'(InteriorDay|InteriorNight|Dawn|Sunrise|Day|Sunset|Dusk|Night)$', k).group(1) if re.search(r'(InteriorDay|InteriorNight|Dawn|Sunrise|Day|Sunset|Dusk|Night)$', k) else ''), []).append(rel)
                    v = y.split('=', 1)[1].strip() if '=' in y else ''
                    try:
                        nums = [float(t) for t in v.split(',')]
                        if 'ColorFilter' in k or 'ScatteringColor' in k:
                            if min(nums) < 0 or max(nums) > 10: badclamp.append((rel, k, v))
                    except ValueError: pass
    print('==', br, 'files', nfiles, 'crlf/line-count changes', crlf)
    for (sec, k, p), files in sorted(changed.items(), key=lambda kv: (str(kv[0][0]), kv[0][1], kv[0][2])):
        print(f'   [{sec}] {k} {p}: {len(files)} files')
    print('   clamp violations', badclamp)
