import json,collections
rows=[json.loads(l) for l in open('mot_adm_refs.jsonl',encoding='utf-8')][1:]
c=collections.Counter(); w=collections.Counter(); ws=collections.Counter(); fl=collections.Counter()
for r in rows:
    f=r['fields']
    if isinstance(f,list): f={x['path']:x.get('value',x.get('note')) for x in f}
    c[(f.get('EnableParent.Reference'),f.get('EnableParent.Flags'))]+=1
    w[r['winner']]+=1; ws[f.get('*parent.*parent.EditorID')]+=1; fl[f.get('SkyrimMajorRecordFlags')]+=1
print(c.most_common(10)); print(w.most_common(10)); print(ws.most_common(20)); print(fl)
