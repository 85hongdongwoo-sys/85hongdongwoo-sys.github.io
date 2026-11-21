import re, urllib.request, urllib.parse, json, openpyxl, io
UA={'User-Agent':'Mozilla/5.0'}
def raw(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
B='https://www.suneung.re.kr/boardCnts/'
posts=[]
for p in range(1,8):
    h=raw(B+'list.do?boardID=1500230&m=0302&s=suneung&page=%d&searchStr='%p+urllib.parse.quote('채점')).decode('utf-8','replace')
    rows=h.split('<tr')[1:]
    if not rows: break
    for r in rows:
        t=re.search(r'title="([^"]+)" onclick="javascript:goView',r)
        if not t: continue
        files=re.findall(r"fn_fileDown\('(\w+)'\);\" title='([^']+)'",r)
        d=re.search(r'<td>(\d{4}-\d\d-\d\d)</td>',r)
        posts.append((t.group(1),d.group(1) if d else '',files))
for t,d,f in posts: print(d,t,'|',[n for _,n in f])
# 수능 본시험 최신 1건 엑셀 구조
for t,d,f in posts:
    if '모의평가' in t: continue
    for s,n in f:
        if '등급' in n and n.endswith('xlsx'):
            wb=openpyxl.load_workbook(io.BytesIO(raw(B+'fileDown.do?fileSeq='+s)),data_only=True)
            print('#####',t,n)
            for ws in wb.worksheets:
                print('##',ws.title,ws.max_row,ws.max_column)
                for r in ws.iter_rows(values_only=True, max_row=80):
                    if any(c is not None for c in r): print(r)
            break
    else: continue
    break
