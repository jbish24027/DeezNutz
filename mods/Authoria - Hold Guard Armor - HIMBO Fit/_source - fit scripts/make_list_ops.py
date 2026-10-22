import json
P = 'Authoria - Patch - Hold Guard Armor.esp'; S = 'Sons of Skyrim - Requiem Patch.esp'; R = 'Requiem.esp'; K = 'Skyrim.esm'
B = '00080C:' + P; G = '00080D:' + P; WC = '00080E:' + P; WH = '00080F:' + P
otft = {
 '7FB3DF:' + R: [B, G, '0C7F5B:' + K, '0C7F5C:' + K],
 '845838:' + R: ['02151E:' + K, G, B, '021619:' + K],
 '84583C:' + R: ['02150D:' + K, G, B, '021615:' + K],
 '845840:' + R: ['021508:' + K, B, G, '021613:' + K],
 '845844:' + R: ['021520:' + K, G, B, '02161B:' + K],
 '969E93:' + R: [G, B, '00093B:' + S, '0009A5:' + S],
 '96C666:' + R: ['021525:' + K, G, B, '02161F:' + K],
 '96C66A:' + R: ['021507:' + K, G, B, '021622:' + K],
 '96C66E:' + R: ['021522:' + K, B, G, '021615:' + K],
 '96C66D:' + R: ['000A7D:' + S, '00094C:' + S, WH, WC, '00094D:' + S, '000988:' + S],
}
lvli = {
 '000A5E': {2: B, 3: G}, '000A62': {1: B, 2: G, 3: '021619:' + K}, '000A65': {2: G, 3: B}, '000A68': {2: B, 3: G},
 '000A6B': {2: B, 3: G}, '000A6E': {2: G, 3: B}, '000A71': {1: B, 2: G}, '000A74': {2: B, 3: G}, '000A6D': {0: WC, 1: WH},
}
ops = []
for f, items in otft.items():
    ops.append({'formid': f, 'field_path': 'Items', 'op': 'ReplaceAll', 'values': items})
for f, m in lvli.items():
    for i, ref in m.items():
        ops.append({'formid': f + ':' + S, 'field_path': 'Entries[%d].Data.Reference' % i, 'value': ref})
armo = ['02150D:' + K, '021522:' + K, '00093B:' + S, '021525:' + K, '0C7F5B:' + K, '021507:' + K, '021508:' + K, '021520:' + K, '02151E:' + K,
        '021615:' + K, '02161D:' + K, '0009A5:' + S, '02161F:' + K, '0C7F5C:' + K, '021622:' + K, '021613:' + K, '02161B:' + K, '021619:' + K]
for f in armo:
    ops.append({'formid': f, 'field_path': 'WorldModel.Male.Model.Data', 'op': 'Remove'})
json.dump(ops, open('ops_lists.json', 'w'), indent=1)
print(len(ops))
