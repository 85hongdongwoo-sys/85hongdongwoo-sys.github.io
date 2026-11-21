import re, urllib.request
UA={'User-Agent':'Mozilla/5.0'}
def get(u, data=None):
    try: return urllib.request.urlopen(urllib.request.Request(u,data=data,headers=UA),timeout=40).read().decode('utf-8','replace')
    except Exception as e: return f'ERR {e}'
h=get('https://www.q-net.or.kr/crf005.do?id=crf00503&gSite=L&gId=59')
for m in sorted(set(re.findall(r'["\']([^"\']*\.do[^"\']*)["\']',h))): print('URL',m[:150])
for m in re.findall(r'(?s)\$\.ajax\(\{.{0,400}',h)[:8]: print('AJAX',m.replace('\n',' ')[:400])
for m in re.findall(r'(?s)function\s+(\w+)\s*\(([^)]*)\)\s*\{(.{0,300})',h):
    if 'Subtab' in m[2] or 'gbn' in m[2] or 'crf' in m[2]: print('FN',m[0],m[1],m[2].replace('\n',' ')[:300])
i=h.find('gbnSubtab1'); print('CTX',h[i-800:i+800])
