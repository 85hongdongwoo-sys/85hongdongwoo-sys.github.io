#!/usr/bin/env python3
"""전국 17개 시도 학교 급식 수집·집계 (나이스 교육정보 개방 포털)
사용: python3 fetch_meal.py <출력폴더>   → <출력폴더>/index.json, <slug>.json
환경변수: NEIS_KEY (없으면 샘플 모드: 한 번에 5건씩만 받아져서 학교 수를 LIMIT로 줄여 시험용으로만)
         LIMIT (시도당 학교 수 제한, 시험용)  THREADS (동시 요청 수, 기본 8)
"""
import json, os, re, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

OUT = sys.argv[1] if len(sys.argv) > 1 else 'meal-out'
KEY = os.environ.get('NEIS_KEY', '').strip()
LIMIT = int(os.environ.get('LIMIT') or (0 if KEY else 15))
THREADS = int(os.environ.get('THREADS') or 8)
PS = 1000 if KEY else 5
KST = timezone(timedelta(hours=9)); NOW = datetime.now(KST)
SIDO = [('B10', 'seoul', '서울'), ('C10', 'busan', '부산'), ('D10', 'daegu', '대구'), ('E10', 'incheon', '인천'), ('F10', 'gwangju', '광주'),
        ('G10', 'daejeon', '대전'), ('H10', 'ulsan', '울산'), ('I10', 'sejong', '세종'), ('J10', 'gyeonggi', '경기'), ('K10', 'gangwon', '강원'),
        ('M10', 'chungbuk', '충북'), ('N10', 'chungnam', '충남'), ('P10', 'jeonbuk', '전북'), ('Q10', 'jeonnam', '전남'), ('R10', 'gyeongbuk', '경북'),
        ('S10', 'gyeongnam', '경남'), ('T10', 'jeju', '제주')]
API = 'https://open.neis.go.kr/hub/'
STAT = {'calls': 0, 'err': 0}

def get(svc, **p):
    q = {'Type': 'json', 'pSize': PS}; q.update(p)
    if KEY: q['KEY'] = KEY
    url = API + svc + '?' + urllib.parse.urlencode(q)
    for i in range(4):
        try:
            STAT['calls'] += 1
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'HongLifeTools/1.0 (+https://honglife.co.kr)'}), timeout=40) as r:
                j = json.loads(r.read().decode('utf-8', 'replace'))
            if svc in j:
                h = j[svc][0]['head']; return j[svc][1]['row'], int(h[0]['list_total_count'])
            code = j.get('RESULT', {}).get('CODE', '')
            if code == 'INFO-200': return [], 0          # 해당 데이터 없음
            if code in ('ERROR-337', 'ERROR-500', 'ERROR-600'): time.sleep(5 + i * 10); continue
            raise RuntimeError(code + ' ' + j.get('RESULT', {}).get('MESSAGE', ''))
        except RuntimeError: raise
        except Exception:
            time.sleep(2 + i * 4)
    STAT['err'] += 1; return [], 0

def allrows(svc, cap=None, **p):
    out, page = [], 1
    while True:
        rows, total = get(svc, pIndex=page, **p); out += rows
        if not KEY or not rows or len(out) >= total or (cap and len(out) >= cap): return out   # 키 없으면 1쪽(5건)만 줌
        page += 1

# ── 날짜: 보여 줄 주(토·일이면 다음 주), 비교용 지난주, 미리보기 다음 주 ──
d0 = NOW.date(); mon = d0 - timedelta(days=d0.weekday()) + (timedelta(days=7) if d0.weekday() >= 5 else timedelta(0))
FROM, TO = mon - timedelta(days=7), mon + timedelta(days=11)
DAYS = [(FROM + timedelta(days=i)) for i in range((TO - FROM).days + 1) if (FROM + timedelta(days=i)).weekday() < 5]
DS = [d.strftime('%Y%m%d') for d in DAYS]
CUR = set(DS[5:10]); PREV = set(DS[:5])

ALG = re.compile(r'\(\s*\d{1,2}(?:\s*[.,]\s*\d{1,2})*\s*\.?\s*\)')
def norm(s):
    s = ALG.sub('', s)
    s = re.sub(r'[\*★☆♥♡#@&※◆◇■□●○▶►◀~!^`$%+=|\\/]+', ' ', s)
    s = re.sub(r'\((?:[가-힣A-Za-z]{1,4})\)\s*$', '', s.strip())
    s = re.sub(r'^\d+[.)]?\s*', '', s)
    s = re.sub(r'(?<=[가-힣])\s*[A-Za-z]$', '', s)
    return re.sub(r'\s+', '', s).strip('-_.,·:;')[:24]
KEEP_RICE = re.compile(r'볶음밥|비빔밥|덮밥|김밥|주먹밥|컵밥|초밥|짜장밥|카레|오므라이스|필라프|리조또|라이스|국밥|솥밥')
def staple(n):
    if not n or len(n) < 2: return True
    if re.search(r'김치|깍두기|단무지|우유|석박지|섞박지|겉절이|장아찌|피클', n) and not re.search(r'볶음밥|찌개|전$|만두|볶음|찜|국$|탕$', n): return True
    if n.endswith('밥') and not KEEP_RICE.search(n): return True
    return False
DES = re.compile(r'주스|쥬스|쿠키|케이크|케익|요구르트|요거트|아이스|젤리|푸딩|머핀|와플|츄러스|마카롱|도넛|도너츠|타르트|에이드|스무디|라떼|식혜|수정과|약과|브라우니|빙수|탕후루|초코|바나나|딸기|포도|귤|오렌지|사과|수박|멜론|파인애플|키위|망고|체리|블루베리|자몽|복숭아|샤인머스캣|청포도|요플레|슈크림|롤케|카스테라|크로플|츄|파이$|빵$|떡$|과일|음료|쿨피스|감귤|한라봉|천혜향|레드향|홍시|단감|곶감|배$|^배|자두|토마토')
def dessert(n): return bool(DES.search(n)) and not re.search(r'탕$|국$|찌개|볶음$|조림|무침|구이|찜$|전$|김치', n)

def kind(k):
    return {'초등학교': '초', '중학교': '중', '고등학교': '고', '특수학교': '특'}.get(k, '기타')

def fetch_sido(code, slug, name):
    t = time.time()
    sch = allrows('schoolInfo', cap=(LIMIT or None), ATPT_OFCDC_SC_CODE=code)
    seen = set(); sch = [s for s in sch if s.get('SCHUL_KND_SC_NM') in ('초등학교', '중학교', '고등학교', '특수학교') and (s.get('SD_SCHUL_CODE') or '').strip() and not (s['SD_SCHUL_CODE'] in seen or seen.add(s['SD_SCHUL_CODE']))]
    if LIMIT: sch = sch[:LIMIT]
    def one(s):
        rows = allrows('mealServiceDietInfo', ATPT_OFCDC_SC_CODE=code, SD_SCHUL_CODE=s['SD_SCHUL_CODE'], MLSV_FROM_YMD=DS[0], MLSV_TO_YMD=DS[-1])
        return s, rows
    with ThreadPoolExecutor(THREADS) as ex: res = list(ex.map(one, sch))
    print(f'{name}: 학교 {len(sch)} · {round(time.time()-t)}s · 호출 누적 {STAT["calls"]} · 실패 {STAT["err"]}', flush=True)
    return res

def build(res, name):
    D, dix = [], {}
    def di(s):
        if s not in dix: dix[s] = len(D); D.append(s)
        return dix[s]
    schools, meals = [], {}
    cnt_cur, cnt_prev, des_cur, cals = {}, {}, {}, []
    for s, rows in res:
        sc = s['SD_SCHUL_CODE']; addr = (s.get('ORG_RDNMA') or '').split(' ')
        schools.append([sc, s['SCHUL_NM'], kind(s['SCHUL_KND_SC_NM']), addr[1] if len(addr) > 1 else ''])
        seen_c, seen_p, out, got = set(), set(), [], set()
        for r in rows:
            day = r.get('MLSV_YMD')
            if day not in DS or (day, r.get('MMEAL_SC_CODE')) in got: continue
            got.add((day, r.get('MMEAL_SC_CODE')))
            items = [x.strip() for x in re.split(r'<br\s*/?>', r.get('DDISH_NM') or '') if x.strip()]
            cal = r.get('CAL_INFO', '').replace('Kcal', '').strip()
            try: cal = round(float(cal))
            except Exception: cal = 0
            out.append([DS.index(day), int(r.get('MMEAL_SC_CODE') or 2), [di(x[:40]) for x in items], cal])
            if r.get('MMEAL_SC_CODE') == '2' and day in CUR and cal: cals.append(cal)
            for x in items:
                n = norm(x)
                if staple(n): continue
                if day in CUR: seen_c.add(n)
                elif day in PREV: seen_p.add(n)
        for n in seen_c:
            cnt_cur[n] = cnt_cur.get(n, 0) + 1
            if dessert(n): des_cur[n] = des_cur.get(n, 0) + 1
        for n in seen_p: cnt_prev[n] = cnt_prev.get(n, 0) + 1
        meals[sc] = out
    return {'schools': schools, 'dict': D, 'meals': meals}, cnt_cur, cnt_prev, des_cur, cals

def ranks(cur, prev, des, nsch):
    top = sorted(cur.items(), key=lambda x: -x[1])
    mn = max(3, nsch // 200)
    rise = [(n, c, prev.get(n, 0)) for n, c in cur.items() if c >= mn and c >= 2 * prev.get(n, 0) + 2]
    rise.sort(key=lambda x: -(x[1] - x[2]) / (x[2] + 3))
    return {'top': [[n, c] for n, c in top[:30]], 'dessert': [[n, c] for n, c in sorted(des.items(), key=lambda x: -x[1])[:15]],
            'rising': [[n, c, p] for n, c, p in rise[:12]]}

def main():
    os.makedirs(OUT, exist_ok=True); t0 = time.time()
    lab = lambda a, b: f'{a.month}월 {a.day}일 ~ {b.month}월 {b.day}일'
    idx = {'updated': NOW.strftime('%Y-%m-%d %H:%M'), 'sample': not KEY, 'days': DS, 'cur': [DS[5], DS[9]],
           'label': lab(DAYS[5], DAYS[9]), 'sido': []}
    N_cur, N_prev, N_des, N_sch, allcal = {}, {}, {}, 0, []
    only = os.environ.get('ONLY', '')
    for code, slug, name in SIDO:
        if only and slug not in only.split(','): continue
        try: res = fetch_sido(code, slug, name)
        except RuntimeError as e: print('중단:', name, e, flush=True); continue
        data, cur, prev, des, cals = build(res, name)
        served = sum(1 for sc in data['meals'] if any(m[0] in range(5, 10) for m in data['meals'][sc]))
        r = ranks(cur, prev, des, served)
        avg = round(sum(cals) / len(cals)) if cals else 0
        data.update({'name': name, 'slug': slug, 'updated': idx['updated'], 'days': DS, 'label': idx['label'], 'avgCal': avg, 'served': served}, **r)
        with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as fp: json.dump(data, fp, ensure_ascii=False, separators=(',', ':'))
        idx['sido'].append({'slug': slug, 'name': name, 'schools': len(data['schools']), 'served': served, 'avgCal': avg,
                            'top': r['top'][:5], 'dessert': r['dessert'][:3], 'rising': r['rising'][:3]})
        for a, b in ((N_cur, cur), (N_prev, prev), (N_des, des)):
            for n, c in b.items(): a[n] = a.get(n, 0) + c
        N_sch += served; allcal += cals
    idx['national'] = ranks(N_cur, N_prev, N_des, N_sch); idx['national']['served'] = N_sch
    idx['national']['avgCal'] = round(sum(allcal) / len(allcal)) if allcal else 0
    idx['stat'] = dict(STAT, sec=round(time.time() - t0))
    with open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8') as fp: json.dump(idx, fp, ensure_ascii=False, separators=(',', ':'))
    print('완료', idx['stat'], '급식 학교', N_sch, flush=True)

if __name__ == '__main__':
    main()
