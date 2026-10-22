import sys,struct,os
sys.path.insert(0,os.path.dirname(__file__))
from recs import load
def subs(d):
    i=0;o=[]
    while i<len(d):
        t=d[i:i+4].decode('latin1'); l=struct.unpack('<H',d[i+4:i+6])[0]; o.append((t,d[i+6:i+6+l])); i+=6+l
    return o
def show(s):
    out=[]
    for t,v in s:
        if t in('EDID','MODL','FULL'): out.append(f"{t}={v.rstrip(b'\0').decode('cp1252','replace')}")
        elif t=='VMAD':
            import re; out.append(f"VMAD[{len(v)}] "+' '.join(x.decode() for x in re.findall(rb'[A-Za-z_][A-Za-z0-9_]{3,}',v))[:600])
        else: out.append(f"{t}[{len(v)}]={v[:24].hex()}")
    return out
if __name__=="__main__":
  files=sys.argv[2:]; lid=int(sys.argv[1],16)
  for f in files:
      r=load(f)
      for k,v in r.items():
          if k&0xFFFFFF==lid:
              print('==',os.path.basename(f),hex(k),v[0]); print('\n'.join('  '+x for x in show(subs(v[3]))))
