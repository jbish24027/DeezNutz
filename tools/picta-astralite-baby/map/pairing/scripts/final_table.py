import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pairing import *   # runs the pairing pass (prints suppressed) and exposes tables
stage=json.load(open(os.path.join(D,'pairing_stage.json')))
# ---- raw link values (unresolved Astralite-local links) ----
raw=collections.defaultdict(dict)
for fn in ('wthr_src_AstraliteWeathers.jsonl','wthr_src_AstraliteENB.jsonl','wthr_src_DawnWarmth.jsonl','wthr_src_WyrmAstralite.jsonl','wthr_src_GrayCowlAstralite.jsonl','wthr_picta_winners.jsonl'):
    for r in rows(fn):
        src=r.get('source') or r.get('winner')
        for f in r.get('fields',[]):
            if f['path'] in ('Precipitation','VisualEffect') and f.get('value'):
                raw[(r['formid'],src)][f['path']]=(f.get('link') or {}).get('editorid') or idmap.get(f['value']) or f['value']
def link_name(fid, lane, key):
    a=A[lane].get(fid) or {}
    src=a.get('pbr_winner') if lane=='pbr' else a.get('winner')
    v=raw.get((fid,src),{}).get(key)
    return v
runtime={}
for r in rows('wthr_picta_winners.jsonl'):
    if r.get('runtime_formid'): runtime[r['formid']]=r['runtime_formid']
# ---- Picta weather semantic notes ----
NOTES={
 'A03':'Clear + ground mist: colour partner = Astralite Clear*; Astralite clear weathers carry no mist, so the mist half has no Astralite donor (fog lens: borrow mist only from Astralite Fog* or the Soul RFCT mists, not from the clear partner).',
 'B01':'Lightly cloudy: panorama-only sky like A01; slot partner = Astralite Clear*; sky-likeness alternative = Astralite Cloudy* (listed under alt_partners_sky_likeness). Shares E11 ini B01_Lightly_Cloudy.ini with B02.',
 'B02':'Lightly cloudy aurora: SWF PleasantA slot; Astralite fills PleasantA with Clear*_A and Cloudy*_A, so partners split between both. Shares E11 ini with B01.',
 'A02':'Clear aurora: shares record colours and the E11 ini A01_Clear.ini with A01 (identical colour slots verified).',
 'A01':'Clear: identical record colours to A02; E11 ini A01_Clear.ini serves both A01 and A02.',
 'B03':'Misty fog: SWF Overcast slot. Where Snowy Holds gives Astralite no Overcast entry (snow-lane SN regions and the Whiterun tundra family) the pairing falls back to Astralite Cloudy*; the fog half should come from Astralite Fog* only.',
 'C03':'Cloudy light fog: same slot logic as B03.',
 'D01':'Overcast (no fog, no precip): Astralite has NO plain overcast weather; its Overcast slot is filled by Fog* weathers, so the slot partner is fog-heavy (day fog far 10k-25k vs Picta 150k). Sky-likeness alternative = Astralite OvercastRain* sky without the rain (Soul SoulOvercast.ini). Do not copy Astralite fog DISTANCE onto D01 from the slot partner.',
 'D02':'Overcast heavy fog: cleanest fog partner = Astralite Fog* (SoulFog.ini / SoulFogOvercast.ini).',
 'C01':'Cloudy: also the Picta lane climate fallback (PIC_CLMT_Skyrim -> C01 100%); Astralite lane fallback SkyrimClimate -> SkyrimCloudy 100% (same pairing).',
 'C02':'Cloudy-storm (dry, windy, Pleasant flag): slot partner Astralite Cloudy*; alt = StormRain* sky without rain.',
 'C04':'Very light rain under cloud: partner Astralite OvercastRain*.',
 'C05':'Very light snow under cloud: partner SkyrimOvercastSnow (+Seasons_CloudySnow/Seasons_OvercastSnow where Wyrmstooth/Bruma rolls them).',
 'E01':'Dry thunderstorm (Cloudy flag, no precip): slot partner Astralite StormRain*; regions whose Astralite list has no StormRain fall back to OvercastRain*.',
 'E02':'Dry cold thunderstorm (Cloudy flag, no precip, SWF Snow_Storm slot): partner SkyrimStormSnow (Astralite has no dry snow storm).',
 'E06':'Extreme snow: SkyrimStormSnow; SkyrimStormSnowBlizzard only rolls in one Astralite region (Forgotten Vale ice lake).',
}
def code(ed):
    m=re.match(r'PIC_WTHR_(?:MASTER|SUMMER)_([A-E]\d\d)',ed or ''); return m.group(1) if m else None
GENERIC={'clear':'SkyrimClear','clearA':'SkyrimClear_A','cloudy':'SkyrimCloudy','fog':'SkyrimFog','overcast':'SkyrimFog','rain':'SkyrimOvercastRain',
         'rainstorm':'SkyrimStormRain','snow':'SkyrimOvercastSnow','snowstorm':'SkyrimStormSnow'}
HELIOS_EXIT={'PIC_WTHR_MASTER_A01_Clear':'Skyrim*Clear* (non-aurora)','PIC_WTHR_MASTER_A02_Clear_Aurora':'Skyrim*Clear*_A','PIC_WTHR_MASTER_C01_Cloudy':'Skyrim*Cloudy* (non-aurora)',
 'PIC_WTHR_MASTER_B02_Lightly_Cloudy_Aurora':'Skyrim*Cloudy*_A','PIC_WTHR_MASTER_D02_Overcast_Heavy_Fog':'Skyrim*Fog*','PIC_WTHR_MASTER_D03_Overcast_Rain_Light':'Skyrim*Rain* (non-storm)',
 'PIC_WTHR_MASTER_E03_Storm_Rain_Heavy_Thunder':'Skyrim*Storm* (non-snow)','PIC_WTHR_MASTER_D05_Overcast_Snow_Light':'Skyrim*Snow* (non-storm)','PIC_WTHR_MASTER_E05_Storm_Snow_Heavy':'Skyrim*StormSnow*',
 'PIC_WTHR_MASTER_D01_Overcast':'Skyrim*Overcast* (only names with none of Snow/Storm/Rain/Fog/Cloudy/Clear)'}
picta_rows=[]; leave_pure=[]; identity_rows=[]
for row in stage['picta']:
    ed=row['editorid'] or row['formid']; fid=row['formid']
    row['runtime_formid_picta_lane']=runtime.get(fid)
    row['precipitation']=link_name(fid,'pic','Precipitation') or row.get('precipitation')
    row['visual_effect']=link_name(fid,'pic','VisualEffect')
    c=code(ed)
    if c: row['note']=NOTES.get(c)
    if row['class'] in GENERIC:
        row['canonical_generic_partner']=GENERIC[row['class']]
        row['helios_exit_script_reverse_map']=HELIOS_EXIT.get(ed.replace('SUMMER','MASTER') if ed.startswith('PIC_WTHR_SUMMER') else ed)
        for p in row['partners']:
            p['visual_effect']=link_name(p['formid'],'pbr','VisualEffect'); p['precipitation']=link_name(p['formid'],'pbr','Precipitation')
            ap=A['pbr'].get(p['formid']) or {}
            p['fog_day_near_far']=[ap.get('FogDistanceDayNear'),ap.get('FogDistanceDayFar')]; p['fog_night_near_far']=[ap.get('FogDistanceNightNear'),ap.get('FogDistanceNightFar')]
            p['flags']=ap.get('Flags'); p['wind_0_255']=ap.get('wind_0_255')
        picta_rows.append(row)
    else:
        if ed.startswith('PIC_WTHR_MQ') or ed.startswith('VANILLA_ID_PIC') or row['formid'].startswith('1B0045') or ed in ('DLC2ApocryphaWeatherNew','SovngardeDark','SkuldafnCloudy','SkyrimDA02Weather','KarthspireRedoubtFog','FallowstoneClearSN'):
            leave_pure.append(row)
        else:
            identity_rows.append(row)
# all Picta-defined MQ weathers (rotation or not) for the leave-pure list
mq=[{'formid':fid,'editorid':a.get('editorid'),'e11_ini':e11_file(fid,'pic')} for fid,a in A['pic'].items() if (a.get('editorid') or '').startswith('PIC_WTHR_MQ')]
# reverse map: Astralite weather -> Picta weathers it feeds
rev=collections.defaultdict(dict)
for row in picta_rows:
    share=row['rolls']['region_month_share_sum']
    for p in row['partners']:
        rev[p['editorid']][row['editorid']]=round(p['weight']*share,3)
astralite_rows=stage['astralite']
for a in astralite_rows:
    a['visual_effect']=link_name(a['formid'],'pbr','VisualEffect'); a['precipitation']=link_name(a['formid'],'pbr','Precipitation')
    a['feeds_picta']=dict(sorted(rev.get(a['editorid'],{}).items(), key=lambda kv:-kv[1]))
    a['has_picta_partner']=bool(a['feeds_picta'])
# compact region view (bucket-aligned lists + 4 sample months)
regions=[]
st_all=json.load(open(os.path.join(D,'regn_lanes.json')))
for reg in stage['regions']:
    r=st_all[reg['formid']]
    def lst(ws, namefn):
        out=collections.defaultdict(list)
        for e in ws or []:
            lane,scope,b=bucket(e.get('g_ed'))
            key=f"{lane}/{b}" if b else 'static'
            out[key].append(f"{namefn(e['w']) or e.get('w_ed') or e['w']}[{scope or 'chance '+str(int(e.get('chance') or 0))}]")
        return dict(out)
    regions.append({k:reg[k] for k in ('formid','editorid_picta_lane','worldspace','family','family_name','picta_lane_winner','pbr_lane_winner','seasonal_picta','seasonal_astralite')} |
                   {'picta_list':lst(r.get('pic_weathers'),pic_ed),'astralite_list':lst(r.get('pbr_weathers'),pbr_ed),
                    'sample_month_odds':{m:reg['months'][m] for m in ('January','April','July','October')}})
# family-level summary: for each family, Picta class -> top Astralite partners
fam_summary=collections.defaultdict(dict)
for row in picta_rows:
    for fam,lst2 in row['by_family'].items():
        fam_summary[fam][row['editorid']]=lst2
out={
 'meta':{
   'generated':'2026-10-17','epoch':'e2-2e8a422a1a87271e','picta_lane_profile':'DEEZ CS NUTZ - PICTA (selected_profile, verified in ModOrganizer.ini)',
   'astralite_lane_profile':'DEEZ CS NUTZ - PBR (winners resolved by PBR plugins.txt order: PICTA touchers minus 8 PICTA-only plugins plus 11 PBR-only plugins)',
   'pbr_only_plugins':json.load(open(os.path.join(D,'lanediff.json')))['only_pbr'],
   'picta_only_plugins':json.load(open(os.path.join(D,'lanediff.json')))['only_pic'],
   'weighting':'Region-month odds from SWF DefaultValues (MCM can change them). A filled REGN Global replaces the static Chance (engine rule; static chances shown only for global-less entries). Each in-scope region and each month counts once (no area weighting). Partner weight = share of the Picta weather\'s odds that lands on each Astralite weather rolling in the SAME region, month, SWF lane and bucket, split by Astralite odds; class filter first, then slot-only, class-only (unseasonal lists), fallback class.',
   'scope':'Exterior regions of Tamriel, Solstheim, Bruma (BSHeartland + CYRWeather*), Wyrmstooth, city/child worldspaces, Forgotten Vale, Pale Pass, Sancre Tor and the unique MQ worldspaces. Helios interior regions and FX light regions excluded from the outdoor table (see interiors).',
   'e11_note':'Picta E11 ini groups: A01_Clear.ini = A01+A02; B01_Lightly_Cloudy.ini = B01+B02 (+4 vanilla tundra IDs); A02_Clear_Mist.ini = A03; B02_Lightly_Cloudy_Misty_Fog.ini = B03; summer A01 ini = 5AFA01+5AFA02, summer B01 ini = 5AFB01+5AFB02. Soul Core E11 is class-level (SoulClear.ini covers every Clear{XX}), so at the ini layer the region family does not matter; at the WTHR-record layer it does (Astralite regional variants differ by a median 38-83/255 per colour slot).'},
 'picta_rotation':picta_rows,
 'picta_identity_paired_vanilla_ids':identity_rows,
 'leave_pure_picta':{'rolled_in_regions':leave_pure,'all_picta_MQ_weathers':mq},
 'astralite_rotation':astralite_rows,
 'family_partner_summary':fam_summary,
 'regions':regions,
}
json.dump(out,open(os.path.join(D,'pairing_table.json'),'w'),indent=1)
print('picta rows',len(picta_rows),'identity',len(identity_rows),'leave_pure',len(leave_pure),'astralite',len(astralite_rows),'regions',len(regions))
for a in astralite_rows:
    if not a['has_picta_partner'] and a['class'] not in ('other',):
        print('astralite w/o picta partner:', a['editorid'], a['class'], a['rolls']['n_regions'], list(a['rolls']['families'])[:4])
