import os,sys,urllib.request,urllib.parse
sha=sys.argv[1]; out=sys.argv[2]; base=sys.argv[3]
n=0
for root,dirs,files in os.walk(base):
    for f in files:
        p=os.path.join(root,f).replace(os.sep,'/')
        rel=p[len(base)+1:]
        o=os.path.join(out,rel)
        os.makedirs(os.path.dirname(o),exist_ok=True)
        url='https://raw.githubusercontent.com/InTheBottle/Bottled-Shaders/'+sha+'/'+urllib.parse.quote(rel)
        try:
            open(o,'wb').write(urllib.request.urlopen(url).read()); n+=1
        except Exception as e:
            print('ERR',rel,e)
print('fetched',n)
