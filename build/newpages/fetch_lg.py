"""LG전자 공식 고객지원(lge.co.kr)에서 그램 노트북·PC 모니터 모델과 드라이버/소프트웨어 파일 목록을 모아 data/lg_models.json 저장.
GitHub Actions(driver-data.yml)에서 실행. 공식 사이트의 '매뉴얼/소프트웨어 다운로드' 화면이 쓰는 주소를 그대로 사용한다.
"""
import json, os, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = 'https://www.lge.co.kr'
H = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',
     'Referer': BASE + '/support/product-manuals'}
CAT = 'CT50019563'
SUBS = {'CT50019564': 'gram', 'CT50019602': 'monitor'}
CH = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def post(path, data, tries=4):
    body = urllib.parse.urlencode(data).encode()
    for t in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(BASE + path, data=body, headers=H), timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            if t == tries - 1:
                raise
            time.sleep(2 + t * 3)


def models():
    allm = {}
    calls = [0]

    def rec(sc, pre):
        calls[0] += 1
        j = post('/support/selectModelSearchEngine.lgajax?typeFlag=downloadFlag', {'category': CAT, 'subCategory': sc, 'page': 1, 'keyword': pre})
        L = (j.get('data') or {}).get('listData') or []
        for m in L:
            if m.get('subCategory') == sc:
                allm[m['modelCode']] = m
        if len(L) >= 120 and len(pre) < 6:  # 검색 결과가 120개에서 잘리므로 글자를 하나씩 늘려 다시 찾음
            for c in CH:
                rec(sc, pre + c)

    for sc in SUBS:
        for c in CH:
            rec(sc, c)
    print('model search calls', calls[0], 'models', len(allm))
    return list(allm.values())


def files(m):
    out, page, total = [], 1, None
    while page < 30:
        j = post('/support/manuals/searchManualDriverList.lgajax', {'modelCode': m['modelCode'], 'category': m['category'], 'subCategory': m['subCategory'], 'page': page})
        dr = ((j.get('data') or {}).get('driver')) or {}
        total = int((dr.get('listPage') or {}).get('totalCount') or 0)
        L = dr.get('listData') or []
        out += [[x.get('title', '').strip(), x.get('date', ''), x.get('os', ''), (x.get('file') or {}).get('size', ''), x.get('fileId', '')] for x in L]
        if not L or len(out) >= total:
            break
        page += 1
    return m['modelCode'], out


def main(dst):
    ms = models()
    if len(ms) < 1000:
        sys.exit('too few models — site changed? keep old data')
    res = {}
    with ThreadPoolExecutor(6) as ex:
        for code, fl in ex.map(files, ms):
            res[code] = fl
    fid = {}
    for fl in res.values():
        for f in fl:
            if f[4]:
                fid[f[4]] = f[:4]
    data = {'checked': time.strftime('%Y-%m-%d'), 'files': fid,
            'models': sorted([[SUBS[m['subCategory']], m['modelCode'], m.get('salesModelCode') or m['modelCode'], [f[4] for f in res[m['modelCode']] if f[4]]] for m in ms], key=lambda x: (x[0], x[1]))}
    json.dump(data, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('models', len(ms), 'with files', sum(1 for m in data['models'] if m[3]), 'unique files', len(fid))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'lg_models.json'))
