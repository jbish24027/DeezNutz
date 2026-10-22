"""Turn records_plan_sX.json + the mist assignment table into a houseCARL build manifest for the baby ESL.
Nothing is written to the instance; the manifest is input for the main session's houseCARL calls."""
import json, sys
BASE = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/design/picta-safe"
S = sys.argv[1] if len(sys.argv) > 1 else '0.60'
rp = json.load(open(f"{BASE}/out/records_plan_s{S}.json", encoding='utf-8'))['records']
PLUGIN = "Authoria - Patch - Picta x Astralite.esp"
ESM = "Picta - Weathers of Aurbis.esm"
SRC = {"file": "Astralite ENB.esp", "mod": "[NoDelete] Soul Core Plugin and Assets"}
MOT = [f"{x:06X}:Mists of Tamriel.esp" for x in range(0x80B, 0x817)]
RINGS = {  # new RFCT (copied from Astralite ENB.esp, EffectArt relinked to the copied ARTO), begin/end copied from the Astralite partner
    'Lite': dict(rfct='000834', arto='000802', edid='PxA_Distant_Mounts_Lite', begin=0.0, end=0.0),
    'Heavy': dict(rfct='000812', arto='000803', edid='PxA_Distant_Mounts_Heavy', begin=0.498, end=0.498),
    'Rain': dict(rfct='00081C', arto='00080C', edid='PxA_Distant_Mounts_Rain', begin=0.0, end=0.0)}
RING_OF = {'19FA01': 'Lite', '19FA03': 'Lite', '19FB01': 'Lite', '5AFA01': 'Lite', '5AFA03': 'Lite', '5AFB01': 'Lite', '19FC01': 'Lite',
           '19FB03': 'Heavy', '19FC03': 'Heavy', '19FD01': 'Heavy', '19FD02': 'Heavy',
           '19FC04': 'Rain', '19FD03': 'Rain', '19FD04': 'Rain', '19FC05': 'Rain', '19FD05': 'Rain', '19FD06': 'Rain'}
# untouched VisualEffect: aurora weathers (Astralite Clear_A partners carry none) and C02/E01-E06 (Picta's needles stay)
MOT_ON = ['19FA02', '19FB02', '5AFA02', '5AFB02', '19FC01', '19FC02', '19FB03', '19FC03', '19FD01', '19FD02']

def col(c): return f"{c[0]},{c[1]},{c[2]},0"
m = dict(plugin=PLUGIN, mod_folder="houseCARL - Authoria - Patch - Picta x Astralite",
         create_plugin=dict(esl=True, form_version=44,
                            masters=["Skyrim.esm", "Update.esm", "Dawnguard.esm", "Dragonborn.esm", ESM, "Mists of Tamriel.esp",
                                     "Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp", "Authoria - Patch - Picta Seasonal.esp"]),
         forward=[], copy_new=[], apply=[], checks=[])
for fid, e in rp.items():
    m['forward'].append(dict(formid=f"{fid}:{ESM}", editorid=e['editorid'], from_winner=e['winner'],
                             note="verbatim copy of the current winner, then only the fields below change"))
for name, r in RINGS.items():
    m['copy_new'].append(dict(type='ARTO', from_formid=f"{r['arto']}:Astralite ENB.esp", source=SRC, new_editorid=r['edid'] + '01',
                              note='FormVersion 44 at source = same as the baby ESL, so Model.Data (MODT) is safe to carry'))
    m['copy_new'].append(dict(type='RFCT', from_formid=f"{r['rfct']}:Astralite ENB.esp", source=SRC, new_editorid=r['edid'],
                              set=dict(EffectArt=f"<new {r['edid']}01>"), note='Flags AttachToCamera kept'))
for fid, e in rp.items():
    fk = f"{fid}:{ESM}"
    for slot, axes in e['DALC'].items():
        for ax, v in axes.items():
            if v['old'] != v['new']:
                m['apply'].append(dict(formid=fk, field_path=f"DirectionalAmbientLightingColors.{slot}.{ax}", op='Set', value=col(v['new']), was=col(v['old'])))
    for slot, v in e['SkyStaticsColor'].items():
        if v['old'] != v['new']:
            m['apply'].append(dict(formid=fk, field_path=f"SkyStaticsColor.{slot}", op='Set', value=col(v['new']), was=col(v['old'])))
    if fid in RING_OF:
        r = RINGS[RING_OF[fid]]
        m['apply'].append(dict(formid=fk, field_path="VisualEffect", op='Set', value=f"<new {r['edid']}>", was="null"))
        m['apply'].append(dict(formid=fk, field_path="VisualEffectBegin", op='Set', value=r['begin']))
        m['apply'].append(dict(formid=fk, field_path="VisualEffectEnd", op='Set', value=r['end']))
    if fid in MOT_ON:
        for s in MOT: m['apply'].append(dict(formid=fk, field_path="SkyStatics", op='Add', value=s))
m['checks'] = [
    "record count: 28 WTHR overrides + 3 ARTO + 3 RFCT new; 0 REGN/CLMT/IMGS/VOLI touched",
    "housecarl delta source=baby versus=previous_provider: only DirectionalAmbientLightingColors.(Sunrise|Day|Sunset).*, SkyStaticsColor.(Sunrise|Day|Sunset), VisualEffect(+Begin/End), SkyStatics differ",
    "Night slots, fog distances, imagespaces, VOLI links, precipitation, flags, clouds, sky colours byte-equal to the winner",
    "every SkyStatics add resolves to a Static in Mists of Tamriel.esp (slot A1 in the copied profile)"]
json.dump(m, open(f"{BASE}/out/records_manifest_s{S}.json", 'w'), indent=1)
print(len(m['forward']), 'forwards,', len(m['copy_new']), 'new records,', len(m['apply']), 'field ops')
from collections import Counter
print(Counter(a['field_path'].split('.')[0] for a in m['apply']))
