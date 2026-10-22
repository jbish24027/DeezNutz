import json, sys, os
S = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(S, sys.argv[1] if len(sys.argv) > 1 else 'picta_wthr_colours.json')))
sel = sys.argv[2] if len(sys.argv) > 2 else 'masters'
if sel == 'masters':
    keys = [k for k in d if k.startswith('19F') or k.startswith('5AF')]
else:
    keys = [k for k in d if not (k.startswith('19F') or k.startswith('5AF'))]
TOD = ['Sunrise', 'Day', 'Sunset', 'Night']
for k in keys:
    r = d[k]; c = r['colours']['DALC']
    print(k.split(':')[0], (r['editorid'] or '').replace('PIC_WTHR_', ''), '| winner', r['winner'])
    for t in TOD:
        x = c[t]
        if x['DirectionalXPlus'] is None:
            print('   ', t, 'no DALC'); continue
        same = x['DirectionalXPlus'] == x['DirectionalXMinus'] == x['DirectionalYPlus'] == x['DirectionalYMinus']
        extra = '' if same else ' SIDES ' + str([x[a] for a in ['DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus']])
        print(f"   {t:7} side{tuple(x['DirectionalXPlus'])}{extra} up{tuple(x['DirectionalZPlus'])} down{tuple(x['DirectionalZMinus'])} spec{tuple(x['Specular'])} fres{x['Scale']}")
    cl = [(q['layer'], (q['texture'] or '').replace('\\', '/').split('/')[-1], q['colors']['Day'], q['alphas']['Day']) for q in r['clouds_enabled']]
    print('    clouds(day):', cl)
    if sel != 'masters':
        col = r['colours']
        for f in ['SkyUpperColor', 'HorizonColor', 'FogFarColor', 'SunlightColor', 'AmbientColor']:
            print('    ', f, [col[f][t] for t in TOD])
        sc = r['scalars']
        print('     fog day', sc['FogDistanceDayNear'], sc['FogDistanceDayFar'], sc['FogDistanceDayMax'], 'night', sc['FogDistanceNightNear'], sc['FogDistanceNightFar'], 'voli', r['voli'])
