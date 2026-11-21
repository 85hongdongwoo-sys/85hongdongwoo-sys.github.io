"""공무원·임용 기출 목록 수집 → build/exams/data/gosi.json, imyong.json
- 공무원: 인사혁신처 국가공무원 채용시스템 '선택형 문제/정답' 목록(JSON) — 시험·과목·연도·책형·정답 구분.
  파일은 그 사이트 안에서만 내려받을 수 있어 목록과 공식 페이지 안내만 쓴다.
- 임용: 한국교육과정평가원 중등·초등 교원임용 기출 게시판 — 공식 파일 다운로드 주소(fileSeq).
GitHub Actions(exams.yml)에서 주 1회 실행."""
import http.cookiejar, json, os, re, sys, time, urllib.parse, urllib.request
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
            data.append({'y': y, 'kind': kind, 'title': title, 'seq': r['seq'], 'date': date, 'views': views, 'files': r['files']})
        if len(rs) < 10 or not new: break
        time.sleep(0.6)
    return data

def imyong():
    res = {'source': K, 'checked': time.strftime('%Y-%m-%d'), 'boards': {}}
    for k, bid, m in (('mid', '1500212', '030306'), ('ele', '1500213', '030307')):
        res['boards'][k] = kice_board(bid, m); print('임용', k, len(res['boards'][k]), '건', flush=True)
    if sum(len(v) for v in res['boards'].values()) < 100: print('too few imyong rows — keep previous'); return None
    return res

if __name__ == '__main__':
    os.makedirs(D, exist_ok=True)
    for name, fn in (('imyong', imyong), ('gosi', gosi)):
        try:
            r = fn()
            if r: json.dump(r, open(os.path.join(D, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':')); print('saved', name)
        except Exception as e:
            print('FAIL', name, e)
