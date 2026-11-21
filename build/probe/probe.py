import re, urllib.request
UA={'User-Agent':'Mozilla/5.0'}
def get(u, data=None):
    try: return urllib.request.urlopen(urllib.request.Request(u,data=data,headers=UA),timeout=40).read().decode('utf-8','replace')
    except Exception as e: return f'ERR {e}'
def text(h):
    h=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',h)
    h=re.sub(r'<(br|/p|/tr|/li|/h\d|/div|/dt|/dd|/caption)[^>]*>','\n',h)
    h=re.sub(r'</t[dh]>',' | ',h)
    t=re.sub(r'<[^>]+>','',h); t=t.replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&')
    return '\n'.join(l.strip() for l in t.split('\n') if l.strip())
h=get('https://www.q-net.or.kr/crf005.do?id=crf00503&gSite=L&gId=59')
i=h.find('function goContents'); print('GOC',h[i:i+1500])
for s in ['s01','s02','s03','s05']:
    for u in [f'https://www.q-net.or.kr/crf005.do?id=crf00503{s}&gSite=L&gId=59', f'https://www.q-net.or.kr/crf005.do?id=crf00503{s}&gSite=L&gId=59&jmCd=&jmNm=']:
        h=get(u); t=text(h); print('=====',u,len(h)); print(t[:2500]); break
