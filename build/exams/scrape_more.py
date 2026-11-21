"""공무원·임용 기출 목록 수집 → build/exams/data/gosi.json, imyong.json
- 공무원: 인사혁신처 국가공무원 채용시스템 '선택형 문제/정답' 목록(JSON) — 시험·과목·연도·책형·정답 구분.
  파일은 그 사이트 안에서만 내려받을 수 있어 목록과 공식 페이지 안내만 쓴다.
- 임용: 한국교육과정평가원 중등·초등 교원임용 기출 게시판 — 공식 파일 다운로드 주소(fileSeq).
GitHub Actions(exams.yml)에서 주 1회 실행."""
import html, http.cookiejar, json, os, re, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scrape_kice import rows   # 평가원 게시판 표 파서 재사용

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
UA = 'Mozilla/5.0 (honglife.co.kr exam-link index; contact via site)'
G = 'https://gongmuwon.gosi.kr'
TESTS = [('08', '9급 공채'), ('06', '7급 공채'), ('33', '지방직 제1회'), ('34', '지방직 제2회'), ('03', '5급 공채(행정)'),
         ('05', '5급 공채(과학기술)'), ('09', '외교관후보자'), ('18', '우정9급(계리)'), ('76', '7급 기상직'), ('78', '9급 기상직'),
         ('15', '지역인재 7급'), ('16', '지역인재 9급'), ('28', '5급 민간경력자'), ('38', '7급 민간경력자'), ('96', '근로감독·산업안전 7급')]

cj = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
def req(url, data=None, tries=3):
    for i in range(tries):
        try:
            r = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode() if data is not None else None,
                                       headers={'User-Agent': UA, 'X-Requested-With': 'XMLHttpRequest', 'Referer': G + '/oprut/EvmArChcPrblmCransSbjctInqSbjctLst.do'})
            with op.open(r, timeout=40) as f: return f.read().decode('utf-8', 'ignore')
        except Exception:
            if i == tries - 1: raise
            time.sleep(3 * (i + 1))

def gosi():
    req(G + '/oprut/EvmArChcPrblmCransSbjctInqSbjctLst.do')
    out = []
    for tc, tn in TESTS:
        subs = json.loads(req(G + '/oprut/EvmArChcPrblmCransSbjctLst.do', {'testCd': tc}) or '[]') or []
        n0 = len(out)
        for s in subs:
            p = 1
            while True:
                j = json.loads(req(G + '/oprut/EvmArChcPrblmCransSbjctInqSbjctTblLst.do',
                                   {'testCd': tc, 'sbjctCd': s['sbjctCd'], 'testCycl': s.get('testCycl') or '', 'hdn_curr_page': p}))
                for o in j.get('list', []):
                    out.append({'t': tc, 'y': o.get('enfcYr'), 'sub': (o.get('sbjctNm') or '').strip(), 'bk': o.get('bktpNm') or '',
                                'pdf': 1 if o.get('pdfPstFileId') else 0, 'hwp': 1 if o.get('kornPstFileId') else 0,
                                'ans': o.get('cransSeCd') or '', 'nm': o.get('testNm') or tn})
                pg = j.get('pageNavi') or {}
                if p >= int(pg.get('totalPageCount') or 1): break
                p += 1; time.sleep(0.25)
            time.sleep(0.25)
        print(tn, len(subs), '과목', len(out) - n0, '건', flush=True)
    if len(out) < 500: print('too few gosi rows — keep previous'); return None
    return {'source': G + '/oprut/EvmArChcPrblmCransSbjctInqSbjctLst.do', 'checked': time.strftime('%Y-%m-%d'),
            'tests': [list(t) for t in TESTS], 'rows': out}

K = 'https://www.kice.re.kr'
def kice_board(bid, m):
    data, seen = [], set()
    for p in range(1, 120):
        h = req(f'{K}/boardCnts/list.do?type=default&page={p}&m={m}&boardID={bid}&s=kice')
        rs = rows(h); new = 0
        for r in rs:
            if r['seq'] in seen: continue
            seen.add(r['seq']); new += 1
            c = [x for x in r['cells']]
            num = [x for x in c if re.fullmatch(r'\d+', x)]
            views = int(num[-1]) if len(num) >= 2 else 0
            date = next((x for x in c if re.fullmatch(r'\d{4}-\d{2}-\d{2}', x)), '')
            y = next((x for x in c if re.fullmatch(r'(19|20)\d\d', x)), '')
            kind = next((x for x in c if x in ('문제', '정답', '문제/정답', '채점기준', '답안')), '')
            title = max((x for x in c if x not in (y, kind, date) and not re.fullmatch(r'\d+', x)), key=len, default='')
            data.append({'y': y, 'kind': kind, 'title': title, 'seq': r['seq'], 'date': date, 'views': views, 'files': r['files'], 'cells': [x for x in c if x][:6]})
        if len(rs) < 10 or not new: break
        time.sleep(0.6)
    return data

QN = 'https://www.q-net.or.kr'
QGIDS = [('07', '가맹거래사'), ('64', '감정사'), ('60', '감정평가사'), ('63', '검량사'), ('62', '검수사'), ('46', '경매사'), ('09', '경비지도사'),
         ('49', '경영지도사'), ('05', '공인노무사'), ('08', '공인중개사'), ('37', '관광통역안내사'), ('24', '관세사'), ('40', '국내여행안내사'),
         ('50', '기술지도사'), ('45', '농산물품질관리사'), ('43', '국가유산수리기능자'), ('42', '국가유산수리기술자'), ('61', '물류관리사'),
         ('35', '박물관 및 미술관 준학예사'), ('51', '변리사'), ('52', '사회복지사1급'), ('57', '산업보건지도사'), ('56', '산업안전지도사'),
         ('22', '세무사'), ('34', '소방시설관리사'), ('33', '소방안전교육사'), ('73', '손해평가사'), ('72', '수산물품질관리사'),
         ('54', '정수시설운영관리사'), ('59', '주택관리사보'), ('67', '청소년상담사'), ('66', '청소년지도사'), ('36', '한국어교육능력검정시험'),
         ('31', '행정사'), ('39', '호텔경영사'), ('38', '호텔관리사'), ('41', '호텔서비스사')]
def qnet():
    out = []
    for g, name in QGIDS:
        posts, seen = [], set()
        for page in range(1, 8):
            h = req(f'{QN}/cst003.do?id=cst00301s01&gSite=L&gId={g}&gName={urllib.parse.quote(name)}&page={page}&schText=&schType=&boardId=Q004&code=1008')
            rows = re.findall(r"goNext\('(\d+)'[^>]*>\s*([^<]+?)\s*</a>.*?(\d{4}\.\d{2}\.\d{2})", h, re.S)
            new = [r for r in rows if r[0] not in seen]
            if not new: break
            for a, t, d in new: seen.add(a); posts.append((a, re.sub(r'\s+', ' ', t).strip(), d.replace('.', '-')))
            time.sleep(0.4)
        n = 0
        for a, t, d in posts:
            if '공지' in t or '공공누리' in t: continue
            h = req(f'{QN}/cst003.do?id=cst00302&gSite=L&gId={g}&artlSeq={a}&boardId=Q004')
            files = [[html.unescape(nm), pth, sq] for pth, nm, sq in re.findall(r"fileDown\('([^']+)',\s*'([^']+)',\s*'(\d+)'\)", h)]
            y = re.search(r'(20\d\d|19\d\d)\s*년', t)
            out.append({'g': g, 'q': name, 'title': t, 'y': y.group(1) if y else '', 'date': d, 'seq': a, 'files': files}); n += 1
            time.sleep(0.4)
        print('자격', name, n, '건', flush=True)
    if len(out) < 100: print('too few qnet rows — keep previous'); return None
    return {'source': QN, 'checked': time.strftime('%Y-%m-%d'), 'license': '공공누리 제1유형(출처표시) — 한국산업인력공단', 'rows': out}

def imyong():
    res = {'source': K, 'checked': time.strftime('%Y-%m-%d'), 'boards': {}}
    for k, bid, m in (('mid', '1500212', '030306'), ('ele', '1500213', '030307'), ('gum', '1500211', '030305')):
        res['boards'][k] = kice_board(bid, m); print('임용', k, len(res['boards'][k]), '건', flush=True)
    if sum(len(v) for v in res['boards'].values()) < 300: print('too few imyong rows — keep previous'); return None
    return res

if __name__ == '__main__':
    os.makedirs(D, exist_ok=True)
    only = os.environ.get('ONLY', '')
    for name, fn in (('imyong', imyong), ('qnet', qnet), ('gosi', gosi)):
        if only and name not in only.split(','): continue
        try:
            r = fn()
            if r: json.dump(r, open(os.path.join(D, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':')); print('saved', name)
        except Exception as e:
            print('FAIL', name, e)
