import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smp_audit import enabled_mods, MODS
targets = {
 (r'meshes\pulcharmsolis\indoril wayfarer', 'helmet'), (r'meshes\pulcharmsolis\indoril wayfarer', 'helmetwithscarfm'),
 (r'meshes\pulcharmsolis\ashlander seer', 'bootsm'), (r'meshes\pulcharmsolis\ashlander seer', 'bootsf'),
 (r'meshes\pulcharmsolis\camonnatong', 'steelglovesf'), (r'meshes\pulcharmsolis\ashlanderwarrior', 'steelbodyf'),
 (r'meshes\!ube\falmerslayer', 'falmerslayerhelmet'), (r'meshes\!ube\falmerslayer', 'falmerslayerfaceguard'),
 (r'meshes\smp wig6', '532_doa tsukushi'), (r'meshes\!ube\smp wig6', '532_doa tsukushi'),
 (r'meshes\weapons\vergi armoury\einarbow', 'dd - einar backpack'),
}
mods = enabled_mods()
hits = []
osp_seen = {}
for prio, m in enumerate(mods):
    d = os.path.join(MODS, m, 'CalienteTools', 'BodySlide', 'SliderSets')
    if not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        if not f.lower().endswith('.osp'):
            continue
        rel = f.lower()
        if rel in osp_seen:
            continue
        osp_seen[rel] = m
        try:
            txt = open(os.path.join(d, f), encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        for ss in re.finditer(r'<SliderSet name="([^"]+)">(.*?)</SliderSet>', txt, re.S):
            name, body = ss.group(1), ss.group(2)
            def tag(t):
                mm = re.search(r'<%s(?:\s[^>]*)?>(.*?)</%s>' % (t, t), body, re.S)
                return mm.group(1).strip() if mm else ''
            op = tag('OutputPath').lower().rstrip('\\')
            of = tag('OutputFile').lower()
            if (op, of) in targets:
                hits.append((op, of, name, m, f, tag('DataFolder'), tag('SourceFile')))
for h in sorted(hits):
    print('%s\\%s  <- set %r  [mod: %s | %s]  ShapeData: %s\\%s' % h)
print(len(hits), 'hits')
