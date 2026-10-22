import json, os, collections
D = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/pairing"
st=json.load(open(os.path.join(D,'regn_lanes.json')))
pic=collections.Counter(); pbr=collections.Counter(); names={}
for f,r in st.items():
    for w in r.get('pic_weathers') or []:
        pic[w['w']]+=1; names[w['w']]=w['w_ed']
    for w in r.get('pbr_weathers') or []:
        pbr[w['w']]+=1; names[w['w']]=w['w_ed']
allw=sorted(set(pic)|set(pbr))
print(len(pic),len(pbr),len(allw))
open(os.path.join(D,'wthr_all_ids.txt'),'w').write('\n'.join(allw)+'\n')
json.dump({'pic':pic,'pbr':pbr,'names':names},open(os.path.join(D,'wthr_sets.json'),'w'),indent=1)
