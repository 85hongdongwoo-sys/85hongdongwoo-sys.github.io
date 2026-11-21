import re, sys, urllib.request, ssl
UA={'User-Agent':'Mozilla/5.0'}
def get(u):
    try:
        return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read().decode('utf-8','replace')
    except Exception as e:
        return f'ERR {e}'
def links(u, pat=None, n=80):
    h=get(u); print('=====',u,len(h))
    seen=set()
    for href,txt in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',h,re.S):
        t=re.sub(r'<[^>]+>|\s+',' ',txt).strip()
        if pat and not re.search(pat,href+t): continue
        k=(href,t)
        if k in seen: continue
        seen.add(k); print('  ',t[:40],'|',href[:160])
        if len(seen)>=n: break
    return h
# KICE 수능 사이트
links('https://www.suneung.re.kr/main.do?s=suneung')
h=links('https://www.kice.re.kr/boardCnts/list.do?type=default&m=0403&boardID=1500234&s=suneung', 'boardID|m=04')
for kw in ['채점']:
    for bid in ['1500234','1500235','1500237','1500238','1500239','1500240','1500241']:
        h=get(f'https://www.kice.re.kr/boardCnts/list.do?type=default&boardID={bid}&m=0403&s=suneung&searchType=S&searchStr=%EC%B1%84%EC%A0%90')
        ts=re.findall(r'<td class="tit[^"]*"[^>]*>(.*?)</td>',h,re.S)
        print('--',bid,len(h),[re.sub(r'<[^>]+>|\s+',' ',t).strip()[:50] for t in ts[:6]])
# Q-Net 전문자격 정보
links('https://www.q-net.or.kr/man001.do?gSite=L&gId=59', 'gId|crf|cst|jmCd', 120)
