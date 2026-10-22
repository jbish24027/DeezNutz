import sys,struct,zlib
def walk(b,off,end,out):
    while off<end:
        sig=b[off:off+4]; size=struct.unpack('<I',b[off+4:off+8])[0]
        if sig==b'GRUP':
            walk(b,off+24,off+size,out); off+=size
        else:
            flags,fid=struct.unpack('<II',b[off+8:off+16])
            data=b[off+24:off+24+size]
            if flags&0x40000:
                try: data=zlib.decompress(data[4:])
                except: data=b''
            edid=''
            if data[:4]==b'EDID':
                l=struct.unpack('<H',data[4:6])[0]; edid=data[6:6+l].rstrip(b'\0').decode('cp1252','replace')
            out[fid]=(sig.decode(),edid,flags,data)
            off+=24+size
def load(p):
    b=open(p,'rb').read(); s=struct.unpack('<I',b[4:8])[0]; out={}
    walk(b,24+s,len(b),out); return out
if __name__=='__main__':
    a=load(sys.argv[1]); c=load(sys.argv[2])
    print('old',len(a),'new',len(c))
    same=[k for k in a if k in c and a[k][:2]==c[k][:2]]
    moved=[k for k in a if k not in c or a[k][:2]!=c[k][:2]]
    print('same id+type+edid',len(same),'changed/missing',len(moved))
    for k in moved[:30]: print(hex(k),a[k][:2], c.get(k,('-','-'))[:2])
    new=[k for k in c if k not in a]; print('new ids',len(new))
    for k in new[:30]: print(hex(k),c[k][:2])
    print('max local id old',hex(max(k&0xFFFFFF for k in a if k>>24==4)), 'new', hex(max(k&0xFFFFFF for k in c if k>>24==4)))
    diff=[k for k in same if a[k][3]!=c[k][3]]; print('content-changed',len(diff))
    from collections import Counter; print(Counter(a[k][0] for k in diff))
