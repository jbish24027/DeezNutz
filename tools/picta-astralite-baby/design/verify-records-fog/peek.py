import json,sys
B='C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/design/final/'
d=json.load(open(B+sys.argv[1]))
def show(v,depth=0,maxlen=int(sys.argv[2]) if len(sys.argv)>2 else 1500):
    pass
if isinstance(d,dict):
    for k,v in d.items():
        s=json.dumps(v)
        print('==',k,type(v).__name__,len(s)); print(s[:int(sys.argv[2]) if len(sys.argv)>2 else 1500])
else:
    print(len(d)); print(json.dumps(d[:3])[:3000])
