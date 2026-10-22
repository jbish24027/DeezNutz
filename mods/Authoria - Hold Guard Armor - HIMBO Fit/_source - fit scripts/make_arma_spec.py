"""Build the housecarl_create spec for the 12 armour addons + 2 armours folded in from 1GuarfArmor.esp
(values read from the mod's own records; paths point at the fitted meshes in the new mod folder)."""
import json, os
JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(JOB, 'guarf_new.json')))
by = {v['edid']: v for v in d.values()}
SLOT = {0: 'Head', 1: 'Hair', 2: 'Body', 3: 'Hands', 4: 'Forearms', 5: 'Amulet', 6: 'Ring', 7: 'Feet', 8: 'Calves',
        9: 'Shield', 10: 'Tail', 11: 'LongHair', 12: 'Circlet', 13: 'Ears'}
NEW_EDID = {
    '1GuardHelm': 'AHGA_HelmetAA',
    '1CuirassWhiterunAA': 'AHGA_CuirassWhiterunAA', '1CuirassWinterholdAA': 'AHGA_CuirassWinterholdAA',
    '1StormcloakCuirassAA': 'AHGA_CuirassEastmarchAA', '1CuirassDawnstarAA': 'AHGA_CuirassPaleAA',
    '1CuirassSolitudeAA': 'AHGA_CuirassHaafingarAA', '1CuirassRiftenAA': 'AHGA_CuirassRiftAA',
    '1CuirassMarkarthAA': 'AHGA_CuirassReachAA', '1CuirassHjaalmarchAA': 'AHGA_CuirassHjaalmarchAA',
    '1CuirassFalkreathAA': 'AHGA_CuirassFalkreathAA', '1GuardBootsAA': 'AHGA_BootsAA', '1GuardGlovesAA': 'AHGA_GauntletsAA'}
recs = []
for old, new in NEW_EDID.items():
    v = by[old]
    slots, atype = v['bod2']
    dn = v['dnam']
    ops = [
        {'field_path': 'BodyTemplate', 'compose': {'type': 'BodyTemplate', 'fields': {'ArmorType': 'Clothing'}}},
    ]
    for b in range(14):
        if slots >> b & 1:
            ops.append({'field_path': 'BodyTemplate.FirstPersonFlags', 'op': 'Add', 'value': SLOT[b]})
    ops += [
        {'field_path': 'Race', 'value': v['race']},
        {'field_path': 'AdditionalRaces', 'op': 'ReplaceAll', 'values': v['races']},
        {'field_path': 'Priority.Male', 'value': str(dn[0])}, {'field_path': 'Priority.Female', 'value': str(dn[1])},
        {'field_path': 'WeightSliderEnabled.Male', 'value': 'true' if dn[2] else 'false'},
        {'field_path': 'WeightSliderEnabled.Female', 'value': 'true' if dn[3] else 'false'},
        {'field_path': 'DetectionSoundValue', 'value': str(dn[6])},
        {'field_path': 'WorldModel.Male', 'compose': {'type': 'Model', 'fields': {'File': v['MOD2']}}},
        {'field_path': 'WorldModel.Female', 'compose': {'type': 'Model', 'fields': {'File': v['MOD3']}}},
    ]
    import struct
    wadj = struct.unpack('<f', bytes(dn[8:12]))[0]
    ops.append({'field_path': 'WeaponAdjust', 'value': repr(round(wadj, 4))})
    if 'MOD4' in v:
        m4 = {'type': 'Model', 'fields': {'File': v['MOD4']}}
        alt = v['alt'].get('MO4S')
        if alt:
            # the mod's Whiterun entry names 'MaleBodyStormcloak', a shape the winning (HIMBO) first-person mesh no
            # longer has; the hold colour lives on the 'StormCloak' shape like the other four holds
            m4['sets'] = [{'path': 'AlternateTextures', 'verb': 'Add',
                           'compose': {'type': 'AlternateTexture', 'fields': {'Name': 'StormCloak', 'NewTexture': a[1], 'Index': str(a[2])}}} for a in alt]
        ops.append({'field_path': 'FirstPersonModel.Male', 'compose': m4})
        ops.append({'field_path': 'FirstPersonModel.Female', 'compose': {'type': 'Model', 'fields': {'File': v['MOD5']}}})
    if v.get('sndd'):
        ops.append({'field_path': 'FootstepSound', 'value': v['sndd']})
    recs.append({'record_type': 'ArmorAddon', 'editorid': new, 'ops': ops})
json.dump(recs, open(os.path.join(JOB, 'spec_arma.json'), 'w'), indent=1)
print(len(recs), 'ARMA specs')
