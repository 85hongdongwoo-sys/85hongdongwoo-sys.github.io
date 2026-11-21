import re, urllib.request, urllib.parse
UA={'User-Agent':'Mozilla/5.0'}
def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
    except Exception as e: return f'ERR {e}'
def text(h):
    h=re.sub(r'(?s)<!--.*?-->','',h)
    h=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',h)
    h=re.sub(r'<(br|/p|/tr|/li|/h\d|/div|/dt|/dd|/caption)[^>]*>','\n',h)
    h=re.sub(r'</t[dh]>',' | ',h)
    t=re.sub(r'<[^>]+>','',h); t=t.replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace('&middot;','·')
    return '\n'.join(l.strip() for l in t.split('\n') if l.strip())
for g in ['59','08']:
    h=get(f'https://www.q-net.or.kr/crf005.do?id=crf00503&gSite=L&gId={g}')
    jm=re.search(r'name="jmCd"[^>]*value="([^"]*)"',h) or re.search(r'id="jmCd"[^>]*value="([^"]*)"',h)
    nm=re.search(r'id="jmNm"[^>]*value="([^"]*)"',h) or re.search(r'name="jmNm"[^>]*value="([^"]*)"',h)
    jm=jm.group(1) if jm else ''; nm=nm.group(1) if nm else ''
    print('#####',g,jm,nm)
    for sid,cc in [('s02','B0'),('s01','A0')]:
        u=f'https://www.q-net.or.kr/crf005.do?id=crf00503{sid}&gSite=L&gId={g}&jmCd={jm}&jmInfoDivCcd={cc}&jmNm={urllib.parse.quote(nm)}&seriesCd={g}'
        t=text(get(u)); print('=====',sid,len(t)); print(t[:3500])
