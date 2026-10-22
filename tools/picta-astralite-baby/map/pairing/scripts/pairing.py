import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
st=json.load(open(os.path.join(D,'regn_lanes.json')))
A=json.load(open(os.path.join(D,'wthr_attrs.json')))
swf=json.load(open(os.path.join(D,'swf_defaults.json')))
MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']
SEASON={m:(swf['season_of_month'][m][0] if m!='December' else 'Winter') for m in MONTHS}
# ---------- id -> editorid maps (PBR-lane names) ----------
idmap={}
for fn in ('ids_AstraliteWeathers.jsonl','ids_AstraliteENB.jsonl'):
    for r in rows(fn): idmap[r['formid']]=r.get('editorid')
def pbr_ed(fid):
    a=A['pbr'].get(fid)
    return (a or {}).get('editorid') or idmap.get(fid)
def pic_ed(fid):
    a=A['pic'].get(fid); return (a or {}).get('editorid')
# ---------- E11 routing ----------
def parse_wl(path):
    t=open(path,encoding='utf-8',errors='replace').read().replace('\r','')
    out={}
    for sec,fn,ids in re.findall(r'^\[([^\]]+)\]\s*\nFileName\s*=\s*(.+?)\s*\nWeatherIDs\s*=\s*(.+?)\s*$',t,re.M):
        for i in ids.split(','):
            i=i.strip().upper()
            if i: out[int(i,16)&0xFFFFFF]=fn
    return out
pic_wl=parse_wl("C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1/enbseries/_weatherlist.ini")
soul_wl=parse_wl(os.path.join(D,'soul_weatherlist.ini'))
def e11_file(fid, lane):
    k=int(fid.split(':')[0],16)&0xFFFFFF
    return (pic_wl if lane=='pic' else soul_wl).get(k)
# ---------- classes ----------
PCODE={'A01':'clear','A03':'clear','B01':'clear','A02':'clearA','B02':'clearA','C01':'cloudy','C02':'cloudy',
       'B03':'fog','C03':'fog','D02':'fog','D01':'overcast','C04':'rain','D03':'rain','D04':'rain',
       'E01':'rainstorm','E03':'rainstorm','E04':'rainstorm','C05':'snow','D05':'snow','D06':'snow',
       'E02':'snowstorm','E05':'snowstorm','E06':'snowstorm'}
def pic_class(ed):
    if not ed: return 'unknown'
    m=re.match(r'PIC_WTHR_(MASTER|SUMMER)_([A-E]\d\d)',ed)
    if m: return PCODE[m.group(2)]
    return 'other'
SUF='(CO|FF|MA|RE|SN|TU|VT|FV)?'
def ast_class(ed):
    if not ed: return 'unknown'
    if re.match(r'^(DLC1_)?SkyrimClear'+SUF+'_A$',ed): return 'clearA'
    if re.match(r'^(DLC1_)?SkyrimClear'+SUF+'$',ed): return 'clear'
    if re.match(r'^(DLC1_)?SkyrimCloudy'+SUF+'_A$',ed): return 'cloudyA'
    if re.match(r'^(DLC1_)?SkyrimCloudy'+SUF+'$',ed): return 'cloudy'
    if re.match(r'^SkyrimFog(CO|FF|MA|RE|VT)?$',ed) or ed in ('RiftenOvercastFog','Seasons_Fog','KarthspireRedoubtFog','WyrmstoothFog'): return 'fog'
    if re.match(r'^SkyrimOvercastRain(FF|MA|RE|TU|VT)?$',ed) or ed=='Seasons_CloudyRain': return 'rain'
    if re.match(r'^SkyrimStormRain(FF|RE|TU)?$',ed) or ed=='JawzSkyrimStormRain': return 'rainstorm'
    if ed in ('SkyrimOvercastSnow','Seasons_OvercastSnow','Seasons_CloudySnow','Seasons_CloudySnow02','Lux_SkyrimOvercastSnow'): return 'snow'
    if ed in ('SkyrimStormSnow','SkyrimStormSnowBlizzard'): return 'snowstorm'
    if ed.startswith('DLC02Volcanic'): return 'ash'
    if ed=='WyrmstoothClear': return 'clear'
    if ed=='WyrmstoothStormFog': return 'fog'
    return 'other'
ACCEPT={'clear':['clear'],'clearA':['clearA'],'cloudy':['cloudy'],'fog':['fog'],'overcast':['fog'],
        'rain':['rain'],'rainstorm':['rainstorm'],'snow':['snow'],'snowstorm':['snowstorm']}
FALLBACK={'clear':['clearA','cloudy'],'clearA':['cloudyA','clear'],'cloudy':['cloudyA','clear'],'fog':['cloudy'],'overcast':['rain','cloudy'],
          'rain':['rainstorm'],'rainstorm':['rain'],'snow':['snowstorm'],'snowstorm':['snow']}
ALT={'PIC_WTHR_MASTER_B01_Lightly_Cloudy':['cloudy'],'PIC_WTHR_SUMMER_B01_Lightly_Cloudy':['cloudy'],
     'PIC_WTHR_MASTER_B02_Lightly_Cloudy_Aurora':['cloudyA'],'PIC_WTHR_SUMMER_B02_Lightly_Cloudy_Aurora':['cloudyA'],
     'PIC_WTHR_MASTER_D01_Overcast':['rain'],'PIC_WTHR_MASTER_C02_Cloudy_Storm':['rainstorm'],
     'PIC_WTHR_MASTER_E01_Storm_Thunder':['rain'],'PIC_WTHR_MASTER_E02_Storm_Cold_Thunder':['snow']}
# ---------- region family ----------
FAMNAME={'SKYFPF':'Falkreath pine forest','SKYRFF':'Rift fall forest','SKYHMA':'Hjaalmarch marsh','SKYWTU':'Whiterun tundra','SKYRMT':'Reach mountains',
 'SKYEVT':'Eastmarch volcanic tundra','SKYSTU':'snow tundra','SKYNCO':'north coast','SKYCOA':'coast (Japhets Folly)','SKYSMT':'snow mountains','SKYFVA':'Forgotten Vale',
 'SKYSAT':'Solstheim ash tundra','SKYSST':'Solstheim snow tundra','SKYSMC':'Solstheim mountain coast','BRUMA':'Bruma (Beyond Skyrim)','WYRMSTOOTH':'Wyrmstooth',
 'SANCRETOR':'Sancre Tor (LotD)','PALEPASS':'Pale Pass (LotD)'}
def family(fid, r):
    ed=r.get('editorid') or ''
    m=re.search(r'\[(SKY[A-Z]{3})_',ed)
    if m: return m.group(1)
    if ed.startswith('CYR'): return 'BRUMA'
    if ed.startswith('Wyrmstooth'): return 'WYRMSTOOTH'
    ws=r.get('worldspace') or ''
    return {'SancreTorWorld':'SANCRETOR','PalePass':'PALEPASS','DLC01FalmerValley':'SKYFVA'}.get(ws, 'UNIQUE:'+ed)
SCOPE_WS={'Tamriel','DLC2SolstheimWorld','BSHeartland','WyrmstoothWorld','WhiterunWorld','SolitudeWorld','RiftenWorld','MarkarthWorld','WindhelmWorld',
 'DLC01FalmerValley','JaphetsFollyWorld','SancreTorWorld','PalePass','DeepwoodRedoubtWorld','LabyrinthianMazeWorld','WhiterunDragonsreachWorld','CYRFrostfireGlade',
 'Blackreach','KarthspireRedoubtWorld','SkuldafnWorld','Sovngarde','DLC2ApocryphaWorld','DLC01SoulCairn','FallowstoneCaveWorldEnd'}
def in_scope(fid,r):
    ed=r.get('editorid') or ''
    if ed.startswith('Helios_') or ed.startswith('FX'): return False
    if r.get('worldspace') in SCOPE_WS: return True
    if ed.startswith('CYRWeather'): return True
    return False
# ---------- monthly weights ----------
def entry_weight(e, month):
    if e.get('g_ed'):
        lane,scope,b=bucket(e['g_ed'])
        if lane=='other': return 0.0
        if scope!='Common' and scope!=SEASON[month]: return 0.0
        return float(swf['values'][month][lane][b])
    return float(e.get('chance') or 0)
def monthly(entries, month, namefn):
    out=[]
    for e in entries:
        w=entry_weight(e,month)
        if w<=0 or not e.get('w'): continue
        lane,scope,b=bucket(e.get('g_ed'))
        out.append({'fid':e['w'],'ed':namefn(e['w']) or e.get('w_ed'),'w':w,'lane':lane,'scope':scope,'bucket':b})
    return out
def new_roll(): return {'regions':set(),'families':collections.Counter(),'months':collections.Counter(),'slots':collections.Counter(),'share':0.0}
pic_roll=collections.defaultdict(new_roll); ast_roll=collections.defaultdict(new_roll)
partners=collections.defaultdict(lambda:collections.defaultdict(float))
partners_alt=collections.defaultdict(lambda:collections.defaultdict(float))
partners_fam=collections.defaultdict(lambda:collections.defaultdict(lambda:collections.defaultdict(float)))
match_mode=collections.defaultdict(collections.Counter)
region_out=[]
for fid,r in st.items():
    if not in_scope(fid,r): continue
    fam=family(fid,r)
    reg={'formid':fid,'editorid_picta_lane':r.get('editorid'),'worldspace':r.get('worldspace'),'family':fam,'family_name':FAMNAME.get(fam,fam),
         'picta_lane_winner':r.get('pic_winner'),'pbr_lane_winner':r.get('pbr_winner'),
         'seasonal_picta':any(e.get('g_ed') for e in (r.get('pic_weathers') or [])),'seasonal_astralite':any(e.get('g_ed') for e in (r.get('pbr_weathers') or [])),
         'months':{}}
    for mo in MONTHS:
        P=monthly(r.get('pic_weathers') or [], mo, pic_ed)
        Q=monthly(r.get('pbr_weathers') or [], mo, pbr_ed)
        tp=sum(x['w'] for x in P) or 1; tq=sum(x['w'] for x in Q) or 1
        mp={}; mq={}
        for x in P:
            mp[x['ed'] or x['fid']]=round(mp.get(x['ed'] or x['fid'],0)+x['w']/tp,4)
            pr=pic_roll[x['fid']]; pr['regions'].add(fid); pr['families'][fam]+=x['w']/tp; pr['months'][mo]+=x['w']/tp; pr['slots'][f"{x['lane']}/{x['bucket']}/{x['scope']}"]+=1; pr['share']+=x['w']/tp
        for x in Q:
            mq[x['ed'] or x['fid']]=round(mq.get(x['ed'] or x['fid'],0)+x['w']/tq,4)
            ar=ast_roll[x['fid']]; ar['regions'].add(fid); ar['families'][fam]+=x['w']/tq; ar['months'][mo]+=x['w']/tq; ar['slots'][f"{x['lane']}/{x['bucket']}/{x['scope']}"]+=1; ar['share']+=x['w']/tq
        reg['months'][mo]={'picta':mp,'astralite':mq}
        for x in P:
            pc=pic_class(x['ed']); wP=x['w']/tp
            if pc in ('other','unknown'):
                same=[q for q in Q if q['fid']==x['fid']]
                if same:
                    partners[x['fid']][same[0]['fid']]+=wP; partners_fam[x['fid']][fam][same[0]['fid']]+=wP; match_mode[x['fid']]['same_formid']+=1
                else:
                    match_mode[x['fid']]['none']+=1
                continue
            def pick(classes, need_slot):
                return [q for q in Q if ast_class(q['ed']) in classes and (not need_slot or (q['bucket']==x['bucket'] and q['lane']==x['lane']))]
            cand=[]; mode=None
            if x['bucket'] is not None:
                cand=pick(ACCEPT[pc], True); mode='slot+class'
                if not cand:
                    cand=[q for q in Q if q['bucket']==x['bucket'] and q['lane']==x['lane']]; mode='slot_only'
            if not cand:
                cand=pick(ACCEPT[pc], False); mode='class_only'
            if not cand:
                cand=pick(FALLBACK[pc], False); mode='fallback_class'
            if not cand:
                match_mode[x['fid']]['none']+=1; continue
            match_mode[x['fid']][mode]+=1
            tw=sum(q['w'] for q in cand)
            for q in cand:
                partners[x['fid']][q['fid']]+=wP*q['w']/tw
                partners_fam[x['fid']][fam][q['fid']]+=wP*q['w']/tw
            alt=ALT.get(x['ed'])
            if alt:
                c2=pick(alt, False); t2=sum(q['w'] for q in c2)
                for q in c2: partners_alt[x['fid']][q['fid']]+=wP*q['w']/t2
    region_out.append(reg)
def norm(d):
    t=sum(d.values()) or 1
    return sorted(((k,v/t) for k,v in d.items()), key=lambda kv:-kv[1])
def wthr_brief(fid, lane):
    a=A[lane].get(fid) or {}
    ed=a.get('editorid') or (pbr_ed(fid) if lane=='pbr' else None)
    return {'formid':fid,'editorid':ed,'flags':a.get('Flags'),'precipitation':a.get('Precipitation'),
            'wind_0_255':a.get('wind_0_255'),'cloud_layers':a.get('cloud_layers'),
            'cloud_panorama':[t for t in a.get('cloud_textures',[]) if 'Panorama' in t] if lane=='pic' else None,
            'fog_day_near_far':[a.get('FogDistanceDayNear'),a.get('FogDistanceDayFar')],'fog_night_near_far':[a.get('FogDistanceNightNear'),a.get('FogDistanceNightFar')],
            'visual_effect':a.get('VisualEffect'),
            'record_winner':a.get('pbr_winner') if lane=='pbr' else a.get('winner'),
            'e11_ini':e11_file(fid, lane)}
pic_table=[]
for fid,pr in sorted(pic_roll.items(), key=lambda kv:(pic_ed(kv[0]) or '')):
    ed=pic_ed(fid); pc=pic_class(ed)
    row=wthr_brief(fid,'pic'); row['class']=pc
    row['rolls']={'n_regions':len(pr['regions']),'region_month_share_sum':round(pr['share'],3),
                  'families':{FAMNAME.get(k,k):round(v,3) for k,v in pr['families'].most_common()},
                  'months':{m:round(pr['months'][m],3) for m in MONTHS if pr['months'][m]>0},
                  'swf_slots':dict(pr['slots'])}
    p=norm(partners.get(fid,{}))
    row['partners']=[{'formid':k,'editorid':pbr_ed(k),'class':ast_class(pbr_ed(k)),'weight':round(v,3),'soul_e11_ini':e11_file(k,'pbr'),'record_winner_pbr':(A['pbr'].get(k) or {}).get('pbr_winner')} for k,v in p if v>=0.005]
    ini=collections.defaultdict(float)
    for k,v in p: ini[e11_file(k,'pbr') or '(unrouted -> Soul base enbseries.ini)']+=v
    row['partner_soul_ini_weights']={k:round(v,3) for k,v in sorted(ini.items(), key=lambda kv:-kv[1])}
    if partners_alt.get(fid):
        row['alt_partners_sky_likeness']=[{'formid':k,'editorid':pbr_ed(k),'weight':round(v,3),'soul_e11_ini':e11_file(k,'pbr')} for k,v in norm(partners_alt[fid]) if v>=0.01]
    row['by_family']={FAMNAME.get(f,f):[(pbr_ed(k),round(v,3)) for k,v in norm(d)[:4]] for f,d in partners_fam.get(fid,{}).items()}
    row['match_modes']=dict(match_mode.get(fid,{}))
    pic_table.append(row)
ast_table=[]
for fid,ar in sorted(ast_roll.items(), key=lambda kv:(pbr_ed(kv[0]) or '')):
    row=wthr_brief(fid,'pbr'); row['class']=ast_class(row['editorid'])
    row['rolls']={'n_regions':len(ar['regions']),'region_month_share_sum':round(ar['share'],3),
                  'families':{FAMNAME.get(k,k):round(v,3) for k,v in ar['families'].most_common()},
                  'months':{m:round(ar['months'][m],3) for m in MONTHS if ar['months'][m]>0},'swf_slots':dict(ar['slots'])}
    ast_table.append(row)
json.dump({'picta':pic_table,'astralite':ast_table,'regions':region_out},open(os.path.join(D,'pairing_stage.json'),'w'),indent=1)
for row in (pic_table if __name__=='__main__' else []):
    print(f"{(row['editorid'] or row['formid'])[:46]:46s} {row['class']:9s} regs={row['rolls']['n_regions']:3d} share={row['rolls']['region_month_share_sum']:7.2f} ini={row['e11_ini']}")
    print('    ->', ', '.join(f"{p['editorid']}:{p['weight']}" for p in row['partners'][:9]))
    print('    ini->', row['partner_soul_ini_weights'], row['match_modes'])
    if row.get('alt_partners_sky_likeness'): print('    alt->', ', '.join(f"{p['editorid']}:{p['weight']}" for p in row['alt_partners_sky_likeness'][:6]))
