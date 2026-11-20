"""평가원 수능 홈페이지 '기출문제' 게시판 목록을 읽어 build/exams/data/kice.json 으로 저장.
파일은 받지 않고, 공식 다운로드 주소(fileDown.do?fileSeq=…)와 게시글 정보만 모은다.
GitHub Actions(exams.yml)에서 주 1회 실행 — 새 시험이 게시되면 자동으로 페이지에 반영된다."""
import html, json, os, re, sys, time, urllib.request

BASE = 'https://www.suneung.re.kr'
BOARDS = {'su': '1500234', 'mo': '1500236'}   # 대학수학능력시험 / 수능 모의평가
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'kice.json')
UA = {'User-Agent': 'Mozilla/5.0 (honglife.co.kr exam-link index; contact via site)'}


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode('utf-8', 'ignore')
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(3 * (i + 1))


def text(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def rows(page_html):
    body = re.search(r'<tbody>(.*?)</tbody>', page_html, re.S)
    if not body:
        return []
    out = []
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', body.group(1), re.S):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if len(tds) < 6:
            continue
        files = re.findall(r"fn_fileDown\('([0-9a-f]+)'\);\"\s*title=\"([^\"]*)\"", tr)
        seq = re.search(r"goView\('\d+','(\d+)'", tr)
        cells = [text(t) for t in tds]
        out.append({'cells': cells, 'seq': seq.group(1) if seq else '',
                    'files': [[html.unescape(t), f] for f, t in files]})
    return out


def scrape(kind, bid):
    data, seen = [], set()
    for p in range(1, 80):
        h = get(f'{BASE}/boardCnts/list.do?type=default&page={p}&m=0403&boardID={bid}&s=suneung')
        rs = rows(h)
        new = 0
        for r in rs:
            c = r['cells']
            if r['seq'] in seen:
                continue
            seen.add(r['seq'])
            new += 1
            num = [x for x in c if re.fullmatch(r'\d+', x)]
            views = int(num[-1]) if len(num) >= 2 else 0
            date = next((x for x in c if re.fullmatch(r'\d{4}-\d{2}-\d{2}', x)), '')
            if kind == 'su':   # 번호, 학년도, 영역, 제목, 등록일, 조회, 파일
                item = {'y': c[1], 'mon': '수능', 'area': c[2]}
            else:              # 번호, 학년도, 월, 영역, 제목, 등록일, 파일, 조회
                item = {'y': c[1], 'mon': c[2], 'area': c[3]}
            item.update({'seq': r['seq'], 'date': date, 'views': views, 'files': r['files']})
            data.append(item)
        if len(rs) < 10 or not new:
            break
        time.sleep(0.7)
    return data


def main():
    res = {'source': BASE + '/boardCnts/list.do?boardID=1500234&m=0403&s=suneung',
           'checked': time.strftime('%Y-%m-%d'), 'boards': {}}
    for k, b in BOARDS.items():
        res['boards'][k] = scrape(k, b)
        print(k, len(res['boards'][k]), 'posts')
    if sum(len(v) for v in res['boards'].values()) < 300:   # 사이트 오류 시 기존 데이터 유지
        print('too few rows — keeping previous data'); sys.exit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('saved', OUT)


if __name__ == '__main__':
    main()
