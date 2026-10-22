import json, os, collections
D = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/pairing"
T=json.load(open(os.path.join(D,'pairing_table.json')))
st=json.load(open(os.path.join(D,'regn_lanes.json')))
same=[];diff=[];helios_only=[]
for f,r in st.items():
    ed=r.get('editorid') or ''
    if not ed.startswith('Helios_'): continue
    if r.get('pic_winner')=='Authoria - Patch - Picta Seasonal.esp':
        a=sorted((w['w'],w.get('g_ed')) for w in r['pic_weathers']); b=sorted((w['w'],w.get('g_ed')) for w in r['pbr_weathers'])
        (same if a==b else diff).append(ed)
    else:
        helios_only.append({'region':ed,'picta_lane_winner':r.get('pic_winner'),'pbr_lane_winner':r.get('pbr_winner')})
T['interiors']={
 'picta_lane_helios_plugins':{'Helios.esp':'active','Helios_Lux.esp':'active','Helios_Astralite.esp':'UNTICKED (plugins.txt line 150, no *)','Helios_Astralite_Radiant.esp':'unticked',
     'Helios_Astralite_Seasonal.esp':'UNTICKED (line 1254)','Authoria - Patch - Astralite Dawn Warmth.esp':'mod disabled'},
 'twin_weather_records_picta_lane':'All 85 Helios_<name> WTHR are won by Helios.esp (houseCARL aggregate) = Helios default interior grade, NOT Astralite-graded. In the PBR lane Helios_Astralite.esp overrides 84 of them and Dawn Warmth re-wins 64 (forwards).',
 'helios_astralite_masters':['Skyrim.esm','Dragonborn.esm','Helios.esp','Astralite Weathers.esp','Dawnguard.esm','Update.esm'],
 'interior_regions_picta_lane':{'won_by_Picta_Seasonal':35,'identical_to_Helios_Astralite_Seasonal':same,'retimed_vs_Helios_Astralite_Seasonal':diff,
     'retime_rule':'snow entries moved from Common to Autumn+Winter copies (no summer snow), rain moved from Common to Spring/Summer/Autumn copies (no winter rain), some regional rain twins (Helios_SkyrimOvercastRainTU/FF/VT/MA) swapped for the generic Helios_SkyrimOvercastRain',
     'won_by_Helios_esp_static':helios_only},
 'entry_logic':'Helios_Alias (Authoria Picta exit-weather build) builds "Helios_"+outgoing EditorID on entry. No Helios_PIC_WTHR_MASTER_* / SUMMER_* twin exists (the only Helios_PIC_* record is A10001 Helios_PIC_WTHR_SKYFPF_01_Clear, a Picta 1.0 stub), so every Picta outdoor weather misses the twin lookup -> ForceCurrentWeather(); the interior then shows whatever its Helios interior region rolls (Helios twins named after vanilla/Astralite weathers, seasonally gated by Picta Seasonal). Outdoor-to-indoor MATCH does not exist in the Picta lane.',
 'exit_logic':'On exit a Helios_Skyrim*/Helios_DLC1_Skyrim* twin is mapped by PictaEquivalent(): Snow+Storm->E05, Snow->D05, Storm->E03, Rain->D03, Fog->D02, Cloudy_A->B02, Cloudy->C01, Clear_A->A02, Clear->A01, Overcast->D01, names containing War or not starting Skyrim/DLC1_Skyrim -> no mapping (original lookup). GameMonth 5-7 swaps A01/A02/A03/B01/B02 for the injected SUMMER variants. This is the existing reverse (Astralite-name -> Picta) pairing table and agrees with the forward table here except A03/B01/B03/C02/C03/C04/C05/D04/D06/E01/E02/E04/E06, which the exit map never targets.',
 'e11_interiors':'Picta lane E11 routes interiors by LOCATION (_locationweather.ini section [0], 961 bare lines -> fake ids AA001/AA004/AA007 -> Authoria - Interiors/House|Inn|Dungeon.ini); no Helios twin FormID appears in either lane\'s _weatherlist.ini, so twins never get their own E11 file in either lane.',
 'pairing_implication':'Interior "Astralite colours" in the baby = tick Helios_Astralite.esp (needs Astralite Weathers.esp as an ACTIVE master; it is ESL-flagged, 147 records) or forward its 84 twin colour sets into a baby plugin; region wiring stays Picta Seasonal\'s 35 REGN (already Helios-twin-based, seasonally retimed). Twin names are vanilla names, so the twin <-> Astralite weather pairing is identity (Helios_SkyrimClearTU <-> SkyrimClearTU).'}
T['climates']={
 'picta_lane':{'SkyrimClimate 000812':'PIC_CLMT_Skyrim (Darkened patch) -> PIC C01_Cloudy 100','DefaultClimate 00015F':'PIC_CLMT_Default -> PIC A01_Clear 100',
   'Wanderers Fair 000A15':'Picta Seasonal -> C01 45 / A01 35 / A02 10 / B02 10 (no summer variant)','Karthspire F91':'KarthspireRedoubtFog 100','Sovngarde':'SovngardeDark 100','Blackreach 0239FB':'PIC_WTHR_MQ_Blackreach 100',
   'BloatedMans':'PIC E02_Storm_Cold_Thunder 100','SoulCairn 001409':'1B0043:Picta esm (DANGLING - no such WTHR in Picta 1.1.1)','Wyrmstooth 54AD21':'WyrmstoothFog 70 / StormFog 50 / Clear 30 (Wyrmstooth.esp)'},
 'astralite_lane_overrides_from_Astralite_ENB':{'SkyrimClimate':'SkyrimCloudy 100','DefaultClimate':'SkyrimClear 100','KarthspireClimate':'KarthspireRedoubtFog 82 + 9 storm/rain x2','SoulCairnClimate':'SoulCairnAmb01 80 + Blood 15 + 3x5','BloatedMans':'SkyrimCloudy 100','new SkyrimDaySpring 000837':'FF set (unreferenced?)'},
 'pairing':'Climate fallback pairs C01_Cloudy <-> SkyrimCloudy and A01_Clear <-> SkyrimClear, consistent with the region table.'}
json.dump(T,open(os.path.join(D,'pairing_table.json'),'w'),indent=1)
print(len(same),len(diff),len(helios_only))
