import json
B='C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/design/final/'
d=json.load(open(B+'records_manifest.json'))
for r in d['new_records']: print(json.dumps(r))
print()
tot=0
for k,v in d['overrides'].items():
    ops=v['ops']; tot+=len(ops)
    nondalc=[o for o in ops if not o['field'].startswith('DirectionalAmbient')]
    print(k, v.get('editorid'), 'from', v.get('forward_from'), 'nops',len(ops))
    for o in nondalc: print('    ',json.dumps(o)[:300])
print('total ops',tot)
print([k for k in d.keys()])
for k in d:
    if k not in ('new_records','overrides','optional_off_by_default'): print(k, json.dumps(d[k])[:2000])
