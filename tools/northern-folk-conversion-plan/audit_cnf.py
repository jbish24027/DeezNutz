"""Read-only analysis of houseCARL exports. Writes audit artifacts to _staging only."""
import json, pathlib, re, collections
ROOT = pathlib.Path(r'C:\1. AUTHORIA')
ST = ROOT / '_staging'
def read(name):
    rows = [json.loads(x) for x in (ST / name).read_text(encoding='utf-8-sig').splitlines()]
    assert rows[0]['row_count'] == len(rows)-1, name
    return rows[1:]
def fs(r): return {x['path']:x.get('value') for x in r['fields']}
def links(r,prefix): return [x['value'] for x in r['fields'] if x['path'].startswith(prefix+'[') and x.get('link')]
def slots(r):
    return next((x.get('slots',[]) for x in r['fields'] if x['path']=='BodyTemplate.FirstPersonFlags'),[])
def index(name): return {r['formid']:r for r in read(name)}
npcs=read('cnf-recipients-post.jsonl')
outfits=index('cnf-assigned-outfits-post.jsonl')
armor=index('cnf-assigned-armor-post.jsonl')
addons=index('cnf-assigned-addons-post.jsonl')
rows=[]; paths=set()
for n in npcs:
    f=fs(n); female='Female' in (f.get('Configuration.Flags') or '')
    outfit=outfits[f['DefaultOutfit']]; items=[]
    for itemid in links(outfit,'Items'):
        a=armor[itemid]; candidates=[]
        for aid in links(a,'Armature'):
            ad=addons[aid]; af=fs(ad)
            supported=[af.get('Race')]+links(ad,'AdditionalRaces')
            model=af.get(f'WorldModel[{1 if female else 0}].File')
            candidate={'formid':aid,'race_supported':f['Race'] in supported,'model':model,'slots':slots(ad)}
            candidates.append(candidate)
            if candidate['race_supported'] and model:
                path='meshes\\'+model
                paths.add(path)
                # Both endpoints are checked conservatively when authored name is _1.
                if path.lower().endswith('_1.nif'): paths.add(path[:-6]+'_0.nif')
        valid=[c for c in candidates if c['race_supported'] and c['model']]
        items.append({'formid':itemid,'name':fs(a).get('Name'),'slots':slots(a),'supported':bool(valid),'addons':candidates})
    body=[a for a in items if 32 in a['slots']]
    rows.append({'formid':n['formid'],'type':n['type'],'editorid':n['editorid'],'name':f.get('Name'),'winner':n['winner'],'fields':f,'sex':'female' if female else 'male','outfit':{'formid':outfit['formid'],'editorid':outfit['editorid']},'items':items,'classification':'body_race_or_model_risk' if not body or not any(a['supported'] for a in body) else 'record_support_pass'})
doc={'job':'Northern Folk assigned-outfit compatibility audit','scope':{'recipients':126,'source':'SkyPatcher post overlay'},'total':len(rows),'complete':True,'notes':['Static record support, not proof of actual worn inventory. SPID, templates, save state, and mesh contents require separate checks.','Missing _0 is a conservative warning until weight-slider use is confirmed.','Race support is explicit primary/additional membership; race armor fallback is not inferred.'],'records':rows}
(ST/'cnf-compatibility-audit.json').write_text(json.dumps(doc,indent=2),encoding='utf-8')
(ST/'cnf-required-meshes.txt').write_text('\n'.join(sorted(paths)),encoding='utf-8')
print(json.dumps({'npcs':len(rows),'outfits':len(outfits),'items':len(armor),'addons':len(addons),'mesh_paths':len(paths),'body_risks':[r['name'] for r in rows if r['classification']!='record_support_pass'],'unsupported_items':[{ 'npc':r['name'],'items':[a['name'] for a in r['items'] if not a['supported']]} for r in rows if any(not a['supported'] for a in r['items'])],'template_users':[r['name'] for r in rows if r['fields'].get('Template')],'outfit_families':dict(collections.Counter(r['outfit']['editorid'] for r in rows))},indent=2))

# Potential conflicts only: no attempt to emulate full SPID or decide saved inventory.
if (ST/'spid-distributors-vfs.jsonl').exists():
    lines=[]
    for entry in read('spid-distributors-vfs.jsonl')+read('outfit-distributors-vfs.jsonl'):
        if not entry.get('exists') or entry.get('winner_kind')!='loose': continue
        owner=entry['winner_mod']
        base=ROOT/'overwrite' if owner=='overwrite' else ROOT/'mods'/owner
        path=base/entry['path']
        if not path.exists():
            lines.append({'file':str(path),'error':'cannot locate loose winner'}); continue
        for number,line in enumerate(path.read_text(encoding='utf-8-sig',errors='replace').splitlines(),1):
            if not re.search(r'^\s*(Outfit|SleepOutfit|Form)\s*=|outfitDefault=',line,re.I): continue
            if line.lstrip().startswith((';','#')): continue
            matches=[]
            for n in rows:
                eid=n['editorid']; fid,plugin=n['formid'].split(':')
                # Lexical candidates for review, never asserted to be evaluated filters.
                if re.search(r'(?<![\w])'+re.escape(eid)+r'(?![\w])',line,re.I) or re.search(re.escape(plugin)+r'\|0*'+fid.lstrip('0')+r'(?![0-9a-f])',line,re.I): matches.append(n['name'])
            lines.append({'file':str(path),'line_number':number,'text':line,'lexical_recipients':matches})
    (ST/'cnf-distribution-candidates.json').write_text(json.dumps(lines,indent=2),encoding='utf-8')
    print('DISTRIBUTION SUMMARY',json.dumps({'rules':len(lines),'direct_candidates_outside_cnf':[x for x in lines if x.get('lexical_recipients') and 'zzzClothesOfTheNorthernFolk' not in x['file']],'unmatched_outfit_rules':sum(not x.get('lexical_recipients') for x in lines)},indent=2))
