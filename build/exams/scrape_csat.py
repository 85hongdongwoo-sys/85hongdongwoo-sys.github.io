# 평가원 수능 홈페이지 보도자료 게시판의 '채점 결과' 첨부 엑셀(등급 구분 표준점수)을 읽어
# 학년도·시험(수능/6월/9월)별 과목 등급컷(표준점수·인원·비율)을 build/exams/data/csat_grades.json 으로 저장
import io, json, os, re, sys, urllib.parse, urllib.request
import openpyxl

UA = {'User-Agent': 'Mozilla/5.0 (honglife.co.kr exam index)'}
B = 'https://www.suneung.re.kr/boardCnts/'
OUT = os.path.join(os.path.dirname(__file__), 'data', 'csat_grades.json')


def raw(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read()


def posts():
    res, seen = [], set()
    for p in range(1, 12):
        h = raw(B + f'list.do?boardID=1500230&m=0302&s=suneung&page={p}&searchStr=' + urllib.parse.quote('채점')).decode('utf-8', 'replace')
        rows = h.split('<tr')[1:]
        got = 0
        for r in rows:
            t = re.search(r'title="([^"]+)" onclick="javascript:goView\(\'\d+\',\s*\'(\d+)\'', r)
            if not t:
                continue
            got += 1
            title, seq = t.group(1), t.group(2)
            if seq in seen:
                continue
            seen.add(seq)
            files = re.findall(r"fn_fileDown\('(\w+)'\);\" title='([^']+)'", r)
            d = re.search(r'<td>(\d{4}-\d\d-\d\d)</td>', r)
            res.append({'title': title, 'seq': seq, 'date': d.group(1) if d else '', 'files': files})
        if not got:
            break
    return res


def num(v):
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        s = v.strip().replace(',', '')
        try:
            return float(s) if '.' in s else int(s)
        except ValueError:
            return s
    return v


def parse(b):
    wb = openpyxl.load_workbook(io.BytesIO(b), data_only=True)
    out = {}
    for ws in wb.worksheets:
        cols = {}
        for r in ws.iter_rows(values_only=True):
            r = list(r)
            c0 = r[0].strip() if isinstance(r[0], str) else r[0]
            if c0 == '등급' or (isinstance(c0, str) and c0.replace(' ', '') in ('등급', '영역', '과목')):
                names = {i: re.sub(r'\s+', ' ', str(v)).strip() for i, v in enumerate(r) if i > 0 and isinstance(v, str) and v.strip() and '등급' not in v}
                if names:
                    cols = names
                continue
            g = num(c0)
            if isinstance(g, (int, float)) and 1 <= g <= 9 and cols:
                for i, name in cols.items():
                    if i + 2 < len(r) and r[i] is not None:
                        out.setdefault(name, []).append([int(g), num(r[i]), num(r[i + 1]), num(r[i + 2])])
    return {k: v for k, v in out.items() if len(v) >= 5}


def main():
    data = {}
    for p in posts():
        t = p['title']
        m = re.search(r'(\d{4})학년도', t)
        if not m or '채점' not in t:
            continue
        y = m.group(1)
        kind = '6월' if '6월' in t else '9월' if '9월' in t else '수능'
        xs = [(s, n) for s, n in p['files'] if n.lower().endswith('xlsx') and '등급' in n]
        if not xs:
            continue
        subj = {}
        for s, n in xs:
            try:
                subj.update(parse(raw(B + 'fileDown.do?fileSeq=' + s)))
            except Exception as e:
                print('ERR', t, n, e, file=sys.stderr)
        if not subj:
            continue
        key = data.setdefault(y, {})
        if kind in key:  # 같은 시험 두 번째 글(정정 등)은 먼저 나온 최신 글을 우선
            continue
        key[kind] = {'date': p['date'], 'title': t,
                     'src': B + f'view.do?boardID=1500230&boardSeq={p["seq"]}&lev=0&m=0302&s=suneung',
                     'subjects': subj}
        print(y, kind, p['date'], len(subj), list(subj)[:6])
    json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('years', sorted(data))


if __name__ == '__main__':
    main()
