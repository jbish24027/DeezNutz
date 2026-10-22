# list exterior REFRs (own + overrides) of a plugin with world, grid, pos, base
import struct,zlib,sys,os
sys.path.insert(0,os.path.dirname(__file__))
from plug import masters,subs
def iter_world_refs(path):
    b=open(path,'rb').read(); m=masters(b); name=os.path.basename(path)
    def gid(k):
        i=k>>24; return ((m[i] if i<len(m) else name).lower(), k&0xFFFFFF)
    s=struct.unpack('<I',b[4:8])[0]; off=24+s; out=[]
    def rec(o):
        sig=b[o:o+4]; size,flags,fid=struct.unpack('<III',b[o+4:o+16]); d=b[o+24:o+24+size]
        if flags&0x40000: d=zlib.decompress(d[4:])
        return sig,flags,fid,d,24+size
    def walk(o,end,world,grid):
        while o<end:
            sig=b[o:o+4]; size=struct.unpack('<I',b[o+4:o+8])[0]
            if sig==b'GRUP':
                gtype=struct.unpack('<i',b[o+12:o+16])[0]; label=b[o+8:o+12]
                w=world
                if gtype==1: w=gid(struct.unpack('<I',label)[0])
                walk(o+24,o+size,w,grid if gtype in(6,8,9,10) else None); o+=size; continue
            sig,flags,fid,d,l=rec(o)
            if sig==b'CELL':
                g=None
                for t,v in subs(d):
                    if t=='XCLC': g=struct.unpack('<ii',v[:8])
                grid=g
            elif sig in (b'REFR',b'ACHR') and world:
                ss=subs(d); dd=dict(ss)
                if 'DATA' in dd:
                    out.append(dict(fid=fid,gid=gid(fid),world=world,grid=grid,pos=list(struct.unpack('<6f',dd['DATA'])),base=gid(struct.unpack('<I',dd['NAME'])[0]) if 'NAME' in dd else None,flags=flags,off=o))
            o+=l
    while off<len(b):
        size=struct.unpack('<I',b[off+4:off+8])[0]; label=b[off+8:off+12]
        if label==b'WRLD': walk(off+24,off+size,None,None)
        off+=size
    return out
if __name__=='__main__':
    from collections import Counter
    r=iter_world_refs(sys.argv[1]); print(len(r),Counter(x['world'] for x in r)); print(r[:3])
