import re, urllib.request, urllib.parse
UA={'User-Agent':'Mozilla/5.0'}
def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
    except Exception as e: return f'ERR {e}'
def text(h):
    h=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',h)
    h=re.sub(r'<(br|/p|/tr|/li|/h\d|/div|/dt|/dd)[^>]*>','\n',h)
    h=re.sub(r'</t[dh]>',' | ',h)
    t=re.sub(r'<[^>]+>','',h); t=re.sub(r'&nbsp;',' ',t)
    return '\n'.join(l.strip() for l in t.split('\n') if l.strip())
for tab in ['gbnSubtab1','gbnSubtab2']:
    h=get(f'https://www.q-net.or.kr/crf005.do?id=crf00503&gSite=L&gId=59&gbnn={tab}')
    t=text(h); i=t.find('시험과목'); print('=====QNET',tab,len(h)); print(t[max(0,i-1500):i+3500] if i>=0 else t[:3000])
h=get('https://www.q-net.or.kr/cst003.do?id=cst00308&gSite=L&gId=59'); print('=====STAT'); t=text(h); i=t.find('통계'); print(t[i:i+2500])
for p in [1,2,3]:
    h=get(f'https://www.suneung.re.kr/boardCnts/list.do?boardID=1500230&m=0302&s=suneung&page={p}&searchType=S&searchStr='+urllib.parse.quote('채점 결과'))
    print('=====SN list',p,len(h))
    for seq,t in re.findall(r'boardSeq=(\d+)[^>]*>(.*?)</a>',h,re.S): print('  ',seq,re.sub(r'<[^>]+>|\s+',' ',t).strip()[:70])
h=get('https://www.suneung.re.kr/boardCnts/view.do?boardID=1500230&boardSeq=5096683&lev=0&m=0302&s=suneung')
print('=====view'); print(re.findall(r'fileDown[^"\']*["\'][^>]*>?[^<]{0,80}',h)[:10]); print(re.findall(r'href="([^"]*[Ff]ile[^"]*)"[^>]*>([^<]*)',h)[:10])
h=get('https://www.suneung.re.kr/sub/info.do?m=0404&s=suneung'); print('=====stat'); print(text(h)[-3000:])
