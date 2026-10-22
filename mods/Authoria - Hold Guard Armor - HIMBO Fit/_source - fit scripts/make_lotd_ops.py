import json, os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from gnif import GNif
L = 'LegacyoftheDragonborn.esm'
D = 'out_lotd/meshes/DBM Resources/armor/AuthoriaHoldGuardDISP/'
REL = chr(92).join(['DBM Resources', 'armor', 'AuthoriaHoldGuardDISP', ''])
m = {'08F99F': 'CuirassEastmarch', '17C446': 'CuirassHjaalmarch', '17C44B': 'CuirassRift', '17C44C': 'CuirassDawnstar', '17C44E': 'CuirassMarkarth',
     '17C450': 'CuirassSolitude', '17C452': 'CuirassWhiterun', '17C454': 'CuirassWinterhold', '17C456': 'CuirassFalkreath'}
for f in ['08F9A0', '17C447', '17C44A', '17C44D', '17C44F', '17C451', '17C453', '17C455', '17C457']: m[f] = 'Helm'
for f in ['17C448', '09EECE', '00C42A']: m[f] = 'Boots'
for f in ['17C449', '09EECD', '00C42B']: m[f] = 'Gloves'
bounds = {}
for nm in set(m.values()):
    g = GNif(D + nm + '.nif')
    P = np.concatenate([g.positions(s) for s in g.shapes])
    bounds[nm] = (np.floor(P.min(0)).astype(int).tolist(), np.ceil(P.max(0)).astype(int).tolist())
ops = []
for f, nm in m.items():
    fid = f + ':' + L
    lo, hi = bounds[nm]
    ops += [{'formid': fid, 'field_path': 'Model.File', 'value': REL + nm + '.nif'},
            {'formid': fid, 'field_path': 'Model.AlternateTextures', 'op': 'ReplaceAll', 'composes': []},
            {'formid': fid, 'field_path': 'Model.Data', 'op': 'Remove'},
            {'formid': fid, 'field_path': 'ObjectBounds', 'compose': {'type': 'ObjectBounds', 'fields': {'First': '%d,%d,%d' % tuple(lo), 'Second': '%d,%d,%d' % tuple(hi)}}}]
json.dump(ops, open('ops_lotd.json', 'w'), indent=1)
print(len(ops), bounds)
