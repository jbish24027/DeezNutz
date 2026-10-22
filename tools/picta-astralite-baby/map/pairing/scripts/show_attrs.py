import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
A=json.load(open(os.path.join(D,'wthr_attrs.json')))
sets=json.load(open(os.path.join(D,'wthr_sets.json')))
lane=sys.argv[1]
for fid,a in sorted(A[lane].items(), key=lambda x:(x[1].get('editorid') or '')):
    n=sets[lane].get(fid,0)
    fl=(a.get('Flags') or '').replace('SkyStaticsAlwaysVisible','SSAV')
    print(f"{fid:40s} {str(a.get('editorid'))[:44]:44s} refs={n:3d} [{fl}] P={a.get('Precipitation')} W={a.get('wind_0_255')} cl={a.get('cloud_layers')} fogD={a.get('FogDistanceDayNear'):.0f}/{a.get('FogDistanceDayFar'):.0f} fogN={a.get('FogDistanceNightNear'):.0f}/{a.get('FogDistanceNightFar'):.0f} win={a.get('pbr_winner',a.get('winner'))}")
