import json,sys,re,os
# ingest.py <toolfile> <name> <start_idx>  -> writes chunks name_idx
d=json.load(open(sys.argv[1])); name=sys.argv[2]; i=int(sys.argv[3])
os.makedirs('/home/claude/arttrip/vchunks',exist_ok=True)
for x in d:
    t=x.get('text','')
    t=re.sub(r'^\[javascript_tool:javascript_exec\]\s*','',t)
    s,_=json.JSONDecoder().raw_decode(t.strip())
    open(f'/home/claude/arttrip/vchunks/{name}_{i:03d}.txt','w').write(s); print(i,len(s)); i+=1
