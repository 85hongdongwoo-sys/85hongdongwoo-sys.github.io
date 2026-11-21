import re, urllib.request, urllib.parse, io, subprocess
UA={'User-Agent':'Mozilla/5.0'}
def raw(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read()
def get(u):
    try: return raw(u).decode('utf-8','replace')
    except Exception as e: return f'ERR {e}'
h=get('https://www.suneung.re.kr/boardCnts/list.do?boardID=1500230&m=0302&s=suneung&page=1&searchStr='+urllib.parse.quote('채점'))
i=h.find('<tbody'); print('=====LIST'); print(h[i:i+2500])
h=get('https://www.suneung.re.kr/boardCnts/view.do?boardID=1500230&boardSeq=5096683&lev=0&m=0302&s=suneung')
m=re.search(r"fileDown.do\?fileSeq=(\w+)' target='' >[^<]*등급구분",h); print(m)
i=h.find('fileDown'); print(h[i-400:i+200])
seq=m.group(1)
for base in ['https://www.suneung.re.kr/boardCnts/','https://www.kice.re.kr/boardCnts/']:
    try:
        b=raw(base+'fileDown.do?fileSeq='+seq); print('=====XLSX',base,len(b),b[:4]); open('/tmp/g.xlsx','wb').write(b); break
    except Exception as e: print('ERR',base,e)
subprocess.run(['pip','install','-q','openpyxl'])
import openpyxl
wb=openpyxl.load_workbook('/tmp/g.xlsx',data_only=True)
for ws in wb.worksheets:
    print('##',ws.title,ws.max_row,ws.max_column)
    for r in ws.iter_rows(values_only=True, max_row=60): 
        if any(c is not None for c in r): print(r)
h=get('https://www.q-net.or.kr/crf005.do?id=crf00503&gSite=L&gId=59&gbnn=gbnSubtab1')
print('=====QJS'); 
for m in re.findall(r'[\w/]*\.do\?[^"\'\s]{0,120}',h):
    if 'crf' in m: print(m)
for m in re.findall(r'(?s)function\s+\w*[Tt]ab\w*\s*\([^)]*\)\s*\{.{0,600}',h)[:4]: print('FN',m)
