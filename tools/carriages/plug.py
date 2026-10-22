import struct,zlib,os,sys
sys.path.insert(0,os.path.dirname(__file__))
from recs import walk
def masters(b):
    s=struct.unpack('<I',b[4:8])[0]; body=b[24:24+s]; i=0; m=[]
    while i<len(body):
        t=body[i:i+4]; l=struct.unpack('<H',body[i+4:i+6])[0]
        if t==b'MAST': m.append(body[i+6:i+6+l].rstrip(b'\0').decode('cp1252'))
        i+=6+l
    return m
class Plugin:
    def __init__(s,p):
        b=open(p,'rb').read(); s.name=os.path.basename(p); s.masters=masters(b)
        sz=struct.unpack('<I',b[4:8])[0]; out={}; walk(b,24+sz,len(b),out)
        s.raw=out; s.recs={}
        for k,v in out.items(): s.recs[s.gid(k)]=v
    def gid(s,k):
        i=k>>24; f=s.masters[i] if i<len(s.masters) else s.name
        return (f.lower(),k&0xFFFFFF)
    def fid(s,k):
        """map global (file,local) back to this plugin's formid; None if not mastered"""
        ml=[m.lower() for m in s.masters]
        if k[0]==s.name.lower(): return (len(ml)<<24)|k[1]
        if k[0] in ml: return (ml.index(k[0])<<24)|k[1]
        return None
def subs(d):
    i=0;o=[]
    while i<len(d):
        t=d[i:i+4].decode('latin1'); l=struct.unpack('<H',d[i+4:i+6])[0]
        if t=='XXXX':
            big=struct.unpack('<I',d[i+6:i+10])[0]; t2=d[i+10:i+14].decode('latin1'); o.append((t2,d[i+16:i+16+big])); i+=16+big; continue
        o.append((t,d[i+6:i+6+l])); i+=6+l
    return o
