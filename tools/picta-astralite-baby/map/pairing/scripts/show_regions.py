import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
st=json.load(open(os.path.join(D,'regn_lanes.json')))
A=json.load(open(os.path.join(D,'wthr_attrs.json')))
pbr_name=lambda fid:(A['pbr'].get(fid) or {}).get('editorid')
scope_ws={'Tamriel','DLC2SolstheimWorld','BSHeartland','WyrmstoothWorld','WhiterunWorld','SolitudeWorld','RiftenWorld','MarkarthWorld','WindhelmWorld','DLC01FalmerValley','Blackreach','JaphetsFollyWorld','SancreTorWorld','PalePass','DeepwoodRedoubtWorld','LabyrinthianMazeWorld','KarthspireRedoubtWorld','SkuldafnWorld','Sovngarde','WhiterunDragonsreachWorld','DLC2ApocryphaWorld','DLC01SoulCairn','FallowstoneCaveWorldEnd','CYRFrostfireGlade'}
sel=sys.argv[1] if len(sys.argv)>1 else None
for fid,r in st.items():
    ed=r.get('editorid') or ''
    if not (r.get('worldspace') in scope_ws or ed.startswith('CYR') or (r.get('pic_winner') or '').startswith('Authoria - Patch - Picta Seasonal') and not ed.startswith('Helios')):
        continue
    if sel and sel not in ed and sel not in (r.get('worldspace') or ''): continue
    print('='*100); print(fid, ed, '| ws', r.get('worldspace'), '| PIC', r.get('pic_winner'), '| PBR', r.get('pbr_winner'))
    pw=r.get('pic_weathers') or []; bw=r.get('pbr_weathers') or []
    agg=collections.defaultdict(lambda:[[],[]])
    for w in pw:
        b=bucket(w.get('g_ed')); agg[(b[0],b[2])][0].append(f"{w['w_ed']}({w['chance']:g}{'/'+b[1][:2] if b[1] else ''})")
    for w in bw:
        b=bucket(w.get('g_ed')); agg[(b[0],b[2])][1].append(f"{pbr_name(w['w']) or w['w_ed']}({w['chance']:g}{'/'+b[1][:2] if b[1] else ''})")
    for k,(a,b) in sorted(agg.items(),key=lambda x:str(x[0])):
        print('  ',k); print('     P:',' '.join(a)); print('     A:',' '.join(b))
