#!/usr/bin/env python3
"""공공데이터 수집 → <site>/data/pub/... (GitHub Actions 배포 때 실행)
키는 환경변수(GitHub Secrets): DATA_GO_KR_KEY, OPINET_KEY, EX_KEY. 키가 없거나 실패하면 지금 사이트에 올라가 있는 파일을 그대로 다시 쓴다."""
import json, os, sys, time, re, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

OUT = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '_site', 'data', 'pub')
LIVE = 'https://honglife.co.kr/data/pub/'
KST = timezone(timedelta(hours=9)); NOW = datetime.now(KST)
DK = os.environ.get('DATA_GO_KR_KEY', '').strip(); OK = os.environ.get('OPINET_KEY', '').strip(); EK = os.environ.get('EX_KEY', '').strip()
FORCE = os.environ.get('PUB_FORCE', '')
SIDO = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
FULL = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시', '광주': '광주광역시', '대전': '대전광역시', '울산': '울산광역시',
        '세종': '세종특별자치시', '경기': '경기도', '강원': '강원특별자치도', '충북': '충청북도', '충남': '충청남도', '전북': '전북특별자치도', '전남': '전라남도',
        '경북': '경상북도', '경남': '경상남도', '제주': '제주특별자치도'}
ALIAS = {'서울특별시': '서울', '서울시': '서울', '부산광역시': '부산', '대구광역시': '대구', '인천광역시': '인천', '광주광역시': '광주', '대전광역시': '대전', '울산광역시': '울산',
         '세종특별자치시': '세종', '세종시': '세종', '경기도': '경기', '강원도': '강원', '강원특별자치도': '강원', '충청북도': '충북', '충청남도': '충남', '전라북도': '전북',
         '전북특별자치도': '전북', '전라남도': '전남', '경상북도': '경북', '경상남도': '경남', '제주특별자치도': '제주', '제주도': '제주'}
LOG = []

def log(*a):
    m = ' '.join(str(x) for x in a); print(m, flush=True); LOG.append(m)

def sido_of(addr):
    t = (addr or '').strip().split(' ')[0] if addr else ''
    if t in ALIAS: return ALIAS[t]
    for k in SIDO:
        if t.startswith(k): return k
    return None

def get(url, params=None, tries=3, timeout=40):
    if params: url = url + ('&' if '?' in url else '?') + urllib.parse.urlencode(params, safe=':')
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'HongLifeTools/1.0 (+https://honglife.co.kr)'})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            last = e; time.sleep(2 + i * 3)
    raise last

def items(text):
    """data.go.kr 응답(JSON 또는 XML)에서 item 목록과 totalCount"""
    t = text.lstrip()
    if t.startswith('{'):
        j = json.loads(t)
        body = j.get('response', {}).get('body') or j.get('body') or j
        if 'response' in j and 'header' in j['response']:
            h = j['response']['header']; code = str(h.get('resultCode', '00'))
            if code not in ('00', '0', '0000', 'INFO-000'): raise RuntimeError(f"API {code} {h.get('resultMsg')}")
        it = body.get('items', [])
        if isinstance(it, dict): it = it.get('item', [])
        if isinstance(it, dict): it = [it]
        return it or [], int(body.get('totalCount') or len(it or []))
    root = ET.fromstring(t)
    code = root.findtext('.//resultCode') or root.findtext('.//returnReasonCode')
    if code and code not in ('00', '0', '0000'): raise RuntimeError(f"API {code} {root.findtext('.//resultMsg') or root.findtext('.//returnAuthMsg')}")
    out = [{c.tag: (c.text or '').strip() for c in it} for it in root.iter('item')]
    tc = root.findtext('.//totalCount')
    return out, int(tc) if tc and tc.isdigit() else len(out)

def paged(url, base, rows=1000, maxpage=200, key='serviceKey'):
    allit = []; page = 1
    while page <= maxpage:
        p = dict(base); p.update({key: DK, 'pageNo': page, 'numOfRows': rows})
        it, total = items(get(url, p))
        allit += it
        if not it or len(allit) >= total: break
        page += 1; time.sleep(0.3)
    return allit

def f(x):
    try: return round(float(x), 6)
    except Exception: return None

def write(name, obj):
    p = os.path.join(OUT, name); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fp: json.dump(obj, fp, ensure_ascii=False, separators=(',', ':'))

def write_split(tool, rows, cols, extra=None):
    """rows: (sido, row) 목록 → data/pub/<tool>/<sido>.json + meta"""
    by = {s: [] for s in SIDO}
    for s, r in rows:
        if s in by: by[s].append(r)
    for s, rs in by.items(): write(f'{tool}/{s}.json', rs)
    meta = {'updated': NOW.strftime('%Y-%m-%d %H:%M'), 'cols': cols, 'count': {s: len(v) for s, v in by.items()}}
    if extra: meta.update(extra)
    write(f'{tool}/meta.json', meta); log(tool, 'ok', sum(meta['count'].values()))

def keep_live(tool, split=True):
    """수집 안 하는 시간·실패 때: 지금 배포된 파일을 그대로 다시 올린다"""
    try:
        meta = json.loads(get(LIVE + f'{tool}/meta.json' if split else LIVE + tool, tries=2))
    except Exception:
        log(tool, 'no live copy'); return False
    if not split:
        write(tool, meta); log(tool, 'kept'); return True
    write(f'{tool}/meta.json', meta)
    for s in SIDO:
        try: write(f'{tool}/{s}.json', json.loads(get(LIVE + f'{tool}/' + urllib.parse.quote(s) + '.json', tries=2)))
        except Exception: write(f'{tool}/{s}.json', [])
    log(tool, 'kept', meta.get('updated')); return True

def due(every_h, at=4):
    if FORCE: return True
    if every_h == 1: return True
    if every_h >= 24: return NOW.hour == at
    return NOW.hour % every_h == 0

# ── 1) 약국 (영업시간: 월~일·공휴일 8칸) ──
def pharmacy():
    it = paged('https://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire', {}, rows=1000)
    rows = []
    for x in it:
        la, lo = f(x.get('wgs84Lat')), f(x.get('wgs84Lon'))
        if not la or not lo: continue
        hrs = [[x.get(f'dutyTime{i}s', ''), x.get(f'dutyTime{i}c', '')] for i in range(1, 9)]
        rows.append((sido_of(x.get('dutyAddr')), [x.get('dutyName', ''), la, lo, x.get('dutyAddr', ''), x.get('dutyTel1', ''), hrs]))
    write_split('pharmacy', rows, ['name', 'lat', 'lng', 'addr', 'tel', 'hours'])

# ── 2) 응급실 (위치는 하루 1번, 가용병상은 매시간) ──
def er():
    base = {}
    try: base = {r[0]: r for r in json.loads(get(LIVE + 'er/base.json', tries=1))}
    except Exception: pass
    if due(24) or not base:
        it = paged('https://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire', {}, rows=500)
        base = {}
        for x in it:
            la, lo = f(x.get('wgs84Lat')), f(x.get('wgs84Lon'))
            if la and lo: base[x.get('hpid')] = [x.get('hpid'), x.get('dutyName', ''), la, lo, x.get('dutyAddr', ''), x.get('dutyTel3') or x.get('dutyTel1', ''), x.get('dutyEmclsName', '')]
    write('er/base.json', list(base.values()))
    beds = {}
    for s in SIDO:
        try:
            it = paged('https://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire', {'STAGE1': FULL[s]}, rows=300, maxpage=3)
            for x in it: beds[x.get('hpid')] = [x.get('hvec'), x.get('hvidate', '')]
        except Exception as e: log('er beds', s, e)
    rows = []
    for hp, b in base.items():
        bd = beds.get(hp, [None, ''])
        rows.append((sido_of(b[4]), b[1:] + [bd[0], bd[1]]))
    write_split('er', rows, ['name', 'lat', 'lng', 'addr', 'tel', 'level', 'beds', 'bedtime'])

# ── 3) 전기차 충전소 (충전소별로 묶음) ──
ZC = {'서울': ['11'], '부산': ['26'], '대구': ['27'], '인천': ['28'], '광주': ['29'], '대전': ['30'], '울산': ['31'], '세종': ['36'], '경기': ['41'], '강원': ['51', '42'],
      '충북': ['43'], '충남': ['44'], '전북': ['52', '45'], '전남': ['46'], '경북': ['47'], '경남': ['48'], '제주': ['50']}
def ev():
    rows = []
    for s, zs in ZC.items():
        st = {}
        for z in zs:
            try: it = paged('https://apis.data.go.kr/B552584/EvCharger/getChargerInfo', {'zcode': z, 'dataType': 'JSON'}, rows=9999, maxpage=12)
            except Exception as e: log('ev', s, z, e); continue
            for x in it:
                sid = x.get('statId'); la, lo = f(x.get('lat')), f(x.get('lng'))
                if not sid or not la or not lo: continue
                a = st.setdefault(sid, [x.get('statNm', ''), la, lo, x.get('addr', ''), x.get('busiNm', ''), x.get('useTime', ''), 0, 0, 0, 0, x.get('parkingFree', ''), x.get('limitYn', '')])
                fast = (x.get('chgerType') not in ('02', '08')) or (str(x.get('output') or '0').isdigit() and int(x.get('output') or 0) >= 50)
                ok = str(x.get('stat')) == '2'
                a[6] += 1; a[7] += ok
                if fast: a[8] += 1; a[9] += ok
            if st: break
        rows += [(s, v) for v in st.values()]
    write_split('ev', rows, ['name', 'lat', 'lng', 'addr', 'op', 'time', 'total', 'avail', 'fast', 'fastAvail', 'parkFree', 'limit'])

# ── 4) 주차장 (표준데이터) ──
def parking():
    it = paged('http://api.data.go.kr/openapi/tn_pubr_prkplce_info_api', {'type': 'json'}, rows=1000)
    rows = []
    for x in it:
        la, lo = f(x.get('latitude')), f(x.get('longitude'))
        if not la or not lo: continue
        addr = x.get('rdnmadr') or x.get('lnmadr') or ''
        hrs = [[x.get('weekdayOperOpenHhmm', ''), x.get('weekdayOperColseHhmm', '')], [x.get('satOperOperOpenHhmm', ''), x.get('satOperCloseHhmm', '')], [x.get('holidayOperOpenHhmm', ''), x.get('holidayCloseOpenHhmm', '')]]
        rows.append((sido_of(addr), [x.get('prkplceNm', ''), la, lo, addr, x.get('phoneNumber', ''), x.get('prkplceSe', ''), x.get('prkplceType', ''), x.get('prkcmprt', ''),
                                     x.get('parkingchrgeInfo', ''), x.get('basicTime', ''), x.get('basicCharge', ''), x.get('addUnitTime', ''), x.get('addUnitCharge', ''), x.get('dayCmmtkt', ''), hrs]))
    write_split('parking', rows, ['name', 'lat', 'lng', 'addr', 'tel', 'kind', 'type', 'spaces', 'fee', 'baseMin', 'baseWon', 'addMin', 'addWon', 'day', 'hours'])

# ── 5) 공중화장실 (표준데이터) ──
def toilet():
    it = paged('http://api.data.go.kr/openapi/tn_pubr_public_toilet_api', {'type': 'json'}, rows=1000, maxpage=120)
    rows = []
    for x in it:
        la, lo = f(x.get('latitude')), f(x.get('longitude'))
        if not la or not lo: continue
        addr = x.get('rdnmadr') or x.get('lnmadr') or ''
        hc = any(str(x.get(k) or '0').strip() not in ('', '0') for k in ('menHandicapToiletBowlNumber', 'ladiesHandicapToiletBowlNumber'))
        rows.append((sido_of(addr), [x.get('toiletNm', ''), la, lo, addr, x.get('phoneNumber', ''), x.get('openTime', ''), int(hc), x.get('diaperExhgTablYn', ''), x.get('emgBellYn', '')]))
    write_split('toilet', rows, ['name', 'lat', 'lng', 'addr', 'tel', 'open', 'handicap', 'diaper', 'bell'])

# ── 6) 대기질 (전국 측정소, 매시간) ──
def air():
    it = paged('https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty', {'sidoName': '전국', 'returnType': 'json', 'ver': '1.3'}, rows=1000, maxpage=2)
    rows = [[x.get('sidoName'), x.get('stationName'), x.get('dataTime'), x.get('pm10Value'), x.get('pm25Value'), x.get('pm10Grade1h') or x.get('pm10Grade'),
             x.get('pm25Grade1h') or x.get('pm25Grade'), x.get('o3Value'), x.get('khaiGrade')] for x in it]
    write('air.json', {'updated': NOW.strftime('%Y-%m-%d %H:%M'), 'cols': ['sido', 'station', 'time', 'pm10', 'pm25', 'pm10g', 'pm25g', 'o3', 'khai'], 'rows': rows}); log('air ok', len(rows))

# ── 7) 축제 (한국관광공사) ──
def festival():
    start = (NOW - timedelta(days=0)).strftime('%Y%m%d')
    it = paged('https://apis.data.go.kr/B551011/KorService2/searchFestival2', {'MobileOS': 'ETC', 'MobileApp': 'HongLife', '_type': 'json', 'eventStartDate': (NOW - timedelta(days=60)).strftime('%Y%m%d'), 'arrange': 'A'}, rows=1000, maxpage=5)
    rows = []
    for x in it:
        if (x.get('eventenddate') or '0') < start: continue
        la, lo = f(x.get('mapy')), f(x.get('mapx'))
        if not la or not lo: continue
        rows.append((sido_of(x.get('addr1')), [x.get('title', ''), la, lo, x.get('addr1', ''), x.get('tel', ''), x.get('eventstartdate', ''), x.get('eventenddate', ''), x.get('firstimage2') or x.get('firstimage', ''), x.get('contentid', '')]))
    write_split('festival', rows, ['name', 'lat', 'lng', 'addr', 'tel', 'start', 'end', 'img', 'id'])

# ── 8) 캠핑장 (고캠핑) ──
def camping():
    it = paged('https://apis.data.go.kr/B551011/GoCamping/basedList', {'MobileOS': 'ETC', 'MobileApp': 'HongLife', '_type': 'json'}, rows=1000, maxpage=10)
    rows = []
    for x in it:
        la, lo = f(x.get('mapY')), f(x.get('mapX'))
        if not la or not lo: continue
        rows.append((sido_of(x.get('addr1')) or ALIAS.get((x.get('doNm') or '').strip()) or (x.get('doNm') or '')[:2], [x.get('facltNm', ''), la, lo, x.get('addr1', ''), x.get('tel', ''), x.get('induty', ''), x.get('animalCmgCl', ''),
                     x.get('firstImageUrl', ''), x.get('resveUrl') or x.get('homepage', ''), (x.get('lineIntro') or '')[:60], x.get('sbrsCl', '')]))
    write_split('camping', rows, ['name', 'lat', 'lng', 'addr', 'tel', 'type', 'pet', 'img', 'url', 'intro', 'fac'])

# ── 9) 주유소 최저가 (오피넷, 시군구별 상위 10곳) ──
OPI_SIDO = {'서울': '01', '경기': '02', '강원': '03', '충북': '04', '충남': '05', '전북': '06', '전남': '07', '경북': '08', '경남': '09', '부산': '10', '제주': '11', '대구': '14', '인천': '15', '광주': '16', '대전': '17', '울산': '18', '세종': '19'}
def fuel():
    from pyproj import Transformer
    tr = Transformer.from_crs('+proj=tmerc +lat_0=38 +lon_0=128 +k=0.9999 +x_0=400000 +y_0=600000 +ellps=bessel +units=m +towgs84=-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43', 'EPSG:4326', always_xy=True)
    avg = json.loads(get('https://www.opinet.co.kr/api/avgSidoPrice.do', {'out': 'json', 'code': OK}))['RESULT']['OIL']
    # 오피넷 일반 키는 하루 300건: 시도별 최저가 상위 20곳 × 휘발유·경유 = 34건 + 평균 1건 (6시간마다 → 하루 140건)
    st = {}
    for s, c in OPI_SIDO.items():
        for prod in ('B027', 'D047'):
            try: oil = json.loads(get('https://www.opinet.co.kr/api/lowTop10.do', {'out': 'json', 'code': OK, 'prodcd': prod, 'area': c, 'cnt': 20}))['RESULT']['OIL']
            except Exception as e: log('fuel low', s, e); continue
            for o in oil:
                k = o['UNI_ID']
                if k not in st:
                    lo, la = tr.transform(float(o['GIS_X_COOR']), float(o['GIS_Y_COOR']))
                    adr = o.get('NEW_ADR') or o.get('VAN_ADR', '')
                    parts = adr.split()
                    st[k] = [s, [o.get('OS_NM', ''), round(la, 6), round(lo, 6), adr, o.get('POLL_DIV_CD', ''), None, None, parts[1] if len(parts) > 1 else s]]
                st[k][1][5 if prod == 'B027' else 6] = o.get('PRICE')
            time.sleep(0.2)
    write_split('fuel', [tuple(v) for v in st.values()], ['name', 'lat', 'lng', 'addr', 'brand', 'gasoline', 'diesel', 'area'],
                {'avg': [[x.get('SIDONM'), x.get('PRODCD'), x.get('PRICE')] for x in avg]})

# ── 10) 고속도로 휴게소 (도로공사: 위치·대표음식·기름값) ──
def rest():
    def ex(path, extra=None, pages=20):
        out = []
        for p in range(1, pages + 1):
            prm = {'key': EK, 'type': 'json', 'numOfRows': 99, 'pageNo': p}; prm.update(extra or {})
            j = json.loads(get('https://data.ex.co.kr/openapi/' + path, prm))
            lst = j.get('list') or []
            out += lst
            if len(lst) < 99 or len(out) >= int(j.get('count') or 0): break
        return out
    loc = ex('locationinfo/locationinfoRest', pages=10)
    food = ex('restinfo/restBestfoodList', pages=30)
    oil = ex('business/curStateStation', pages=10)
    def key(n): return re.sub(r'\(.*?\)|휴게소|주유소|\s', '', n or '')
    fd = {}
    for x in food: fd.setdefault(key(x.get('stdRestNm')), []).append([x.get('foodNm', ''), x.get('foodCost', ''), x.get('bestfoodyn', ''), x.get('recommendyn', '')])
    ol = {key(x.get('serviceAreaName')): [x.get('gasolinePrice', ''), x.get('diselPrice', ''), x.get('lpgPrice', ''), x.get('telNo', '')] for x in oil}
    rows = []
    for x in loc:
        la, lo = f(x.get('yValue')), f(x.get('xValue'))
        if not la or not lo: continue
        k = key(x.get('unitName'))
        rows.append([x.get('unitName', ''), la, lo, x.get('routeName', ''), (fd.get(k) or [])[:6], ol.get(k)])
    write('rest.json', {'updated': NOW.strftime('%Y-%m-%d %H:%M'), 'cols': ['name', 'lat', 'lng', 'route', 'foods', 'oil'], 'rows': rows}); log('rest ok', len(rows))

JOBS = [  # (이름, 함수, 필요한 키, 몇 시간마다, 나눠 저장?)
    ('pharmacy', pharmacy, DK, 24, True), ('er', er, DK, 1, True), ('ev', ev, DK, 3, True), ('parking', parking, DK, 24 * 7, True),
    ('toilet', toilet, DK, 24 * 7, True), ('air.json', air, DK, 1, False), ('festival', festival, DK, 24, True), ('camping', camping, DK, 24 * 7, True),
    ('fuel', fuel, OK, 6, True), ('rest.json', rest, EK, 6, False)]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn, key, every, split in JOBS:
        run = bool(key) and (due(every) if every < 24 * 7 else (FORCE or (NOW.weekday() == 0 and NOW.hour == 4)))
        if run:
            try: fn(); continue
            except Exception as e: log(name, 'FAILED', repr(e)[:300])
        elif not key: log(name, 'no key')
        if not keep_live(name, split) and run is False and key and not FORCE:
            try: fn()  # 사이트에 아직 파일이 없으면 지금 한 번 받는다
            except Exception as e: log(name, 'FAILED(first)', repr(e)[:300])
    write('status.json', {'run': NOW.strftime('%Y-%m-%d %H:%M'), 'log': LOG[-80:]})
