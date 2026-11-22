"""국가교통정보센터(ITS) 오픈API → 노선 내비용 데이터 파일.
ITS_KEY 가 없으면 아무것도 하지 않는다(사이트는 CCTV·돌발 버튼을 숨긴다).
  _site/data/its/cctv.json   [[위도, 경도, 이름, HTTPS 영상주소, 도로유형(e=고속도로 i=국도)], ...]
  _site/data/its/events.json {t: 생성시각, e: [[위도, 경도, 유형, 세부, 도로명, 방향, 차단, 내용, 시작, 종료, 도로종류], ...]}"""
import json, os, sys, time, urllib.parse, urllib.request

KEY = os.environ.get('ITS_KEY', '').strip()
out = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '_site', 'data', 'its')
BASE = 'https://openapi.its.go.kr:9443/'
BOX = dict(minX=124.5, maxX=131.9, minY=33.0, maxY=38.7)


def get(path, **q):
    q.update(apiKey=KEY, getType='json')
    url = BASE + path + '?' + urllib.parse.urlencode(q)
    for i in range(3):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'honglife-route-navi'}), timeout=60).read()
            return json.loads(raw.decode('utf-8', 'replace'))
        except Exception as e:
            print(path, q.get('type'), 'try', i + 1, 'ERR', str(e)[:200]); time.sleep(3)
    return None


def rows(d):
    """응답 구조가 조금 달라도 dict 목록을 찾아 꺼낸다."""
    if isinstance(d, list):
        if d and isinstance(d[0], dict):
            return d
        for x in d:
            r = rows(x)
            if r:
                return r
    if isinstance(d, dict):
        for k in ('data', 'items', 'item', 'body', 'response'):
            if k in d:
                r = rows(d[k])
                if r:
                    return r
        for v in d.values():
            r = rows(v)
            if r:
                return r
    return []


def f(x, *ks):
    for k in ks:
        for kk in (k, k.lower(), k[0].upper() + k[1:]):
            if kk in x and x[kk] not in (None, ''):
                return x[kk]
    return ''


if not KEY:
    print('ITS_KEY 없음 — 건너뜀'); sys.exit(0)
os.makedirs(out, exist_ok=True)

cams = []
for typ, tag in (('ex', 'e'), ('its', 'i')):
    d = get('cctvInfo', type=typ, cctvType=4, **BOX)
    rs = rows(d) if d else []
    print('cctv', typ, len(rs))
    for x in rs:
        try:
            la, ln = float(f(x, 'coordy', 'coordY')), float(f(x, 'coordx', 'coordX'))
        except ValueError:
            continue
        u = str(f(x, 'cctvurl', 'cctvUrl'))
        if not (33 < la < 39 and 124 < ln < 132) or not u.startswith('https://'):
            continue
        cams.append([round(la, 5), round(ln, 5), str(f(x, 'cctvname', 'cctvName'))[:40], u, tag])
if cams:
    json.dump(cams, open(os.path.join(out, 'cctv.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print('cctv saved', len(cams))

d = get('eventInfo', type='all', eventType='all')
ev = []
for x in (rows(d) if d else []):
    try:
        la, ln = float(f(x, 'coordY', 'coordy')), float(f(x, 'coordX', 'coordx'))
    except ValueError:
        continue
    if not (33 < la < 39 and 124 < ln < 132):
        continue
    ev.append([round(la, 5), round(ln, 5), str(f(x, 'eventType'))[:10], str(f(x, 'eventDetailType'))[:20],
               str(f(x, 'roadName'))[:30], str(f(x, 'roadDrcType'))[:10], str(f(x, 'lanesBlocked'))[:30],
               str(f(x, 'message'))[:140], str(f(x, 'startDate'))[:14], str(f(x, 'endDate'))[:14], str(f(x, 'type'))[:6]])
if d is not None:
    json.dump({'t': time.strftime('%Y%m%d%H%M', time.gmtime(time.time() + 9 * 3600)), 'e': ev},
              open(os.path.join(out, 'events.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print('events saved', len(ev))
