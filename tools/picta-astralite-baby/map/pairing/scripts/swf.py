import re, json, os
SRC="C:/1. AUTHORIA/mods/Seasonal Weathers Framework - 1.01/source/scripts/SeasonsFrameworkMain.psc"
D = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/pairing"
t=open(SRC,encoding='utf-8',errors='replace').read()
months=['January','February','March','April','May','June','July','August','September','October','November','December']
vals={}
for m in re.finditer(r'int_(SN_)?Season_(PleasantA|Pleasant|Overcast|Rain_Storm|Rain|Snow_Storm|Snow)_(\w+?)\s*=\s*(\d+)',t):
    lane='SN' if m.group(1) else 'plain'; b=m.group(2); mon=m.group(3); v=int(m.group(4))
    if mon in months: vals.setdefault(mon,{}).setdefault(lane,{})[b]=v
# season scope per month: parse Season() blocks
season_of={}
body=t[t.find('Function Season('):]
blocks=re.split(r'(?:else)?if Month == (\d+)',body)
for i in range(1,len(blocks),2):
    k=int(blocks[i]); blk=blocks[i+1]
    s=set(re.findall(r'\n\s*Season_(Spring|Summer|Autumn|Winter)_Pleasant\.SetValue',blk))
    season_of[months[k]]=sorted(s)
json.dump({'values':vals,'season_of_month':season_of,'source':SRC},open(os.path.join(D,'swf_defaults.json'),'w'),indent=1)
for mo in months: print(mo, season_of.get(mo), vals[mo]['plain'], vals[mo]['SN'])
