"""공무원·임용 기출 페이지 생성 (배포 때 실행, gen_exams.py 다음).
- /ipsi/gongmuwon/            공무원 기출 허브 (시험별)
- /ipsi/gongmuwon/<slug>.html 시험별: 연도 × 과목 × 책형, 정답 공개 여부, 공식 페이지 받는 법
- /ipsi/imyong/               임용 기출 허브 (학년도별)
- /ipsi/imyong/imyong-YYYY.html 학년도별: 중등·초등 문제 PDF (평가원 공식 다운로드로 바로 연결)
사용: python3 build/exams/gen_exams_more.py _site"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_exams as GE
from gen_exams import E, SITE, page, crumb, faq_ld, faq_html

root = GE.root
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
KDL = 'https://www.kice.re.kr/boardCnts/fileDown.do?fileSeq='
GOSI_URL = 'https://gongmuwon.gosi.kr/oprut/EvmArChcPrblmCransSbjctInqSbjctLst.do'
SLUG = {'08': '9geup', '06': '7geup', '33': 'jibang-1', '34': 'jibang-2', '03': '5geup-haengjeong', '05': '5geup-gwahak',
        '09': 'oegyogwan', '18': 'gyeri', '76': '7geup-gisang', '78': '9geup-gisang', '15': 'jiyeok-7', '16': 'jiyeok-9',
        '28': 'mingyeong-5', '38': 'mingyeong-7', '96': 'geunro-7'}
SHORT = {'08': '9급 공무원', '06': '7급 공무원', '33': '지방직 공무원(제1회)', '34': '지방직 공무원(제2회)', '03': '5급 공채(행정)',
         '05': '5급 공채(과학기술)', '09': '외교관후보자', '18': '우정9급(계리직)', '76': '7급 기상직', '78': '9급 기상직',
         '15': '지역인재 7급', '16': '지역인재 9급', '28': '5급 민간경력자', '38': '7급 민간경력자', '96': '근로감독·산업안전 7급'}
ANS = {'1': '정답가안', '3': '정답가안', '2': '최종정답', '4': '최종정답'}
XCSS = ('<style id="gc2">.gw-how{counter-reset:s;list-style:none;margin:8px 0 0;padding:0}.gw-how li{position:relative;padding:6px 0 6px 34px;line-height:1.6}'
        '.gw-how li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:6px;width:24px;height:24px;border-radius:50%;background:#1D4ED8;color:#fff;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center}'
        '.gw-btn{display:block;text-align:center;margin:12px 0 0;padding:14px;border-radius:12px;background:#1D4ED8;color:#fff!important;font-weight:800;text-decoration:none}'
        '.gw-sub{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:0;padding:4px 12px 12px}'
        '.gw-sub li{border:1px solid var(--line-s,#E3E7EE);border-radius:8px;padding:6px 9px;font-size:14px;background:#fff;max-width:100%;box-sizing:border-box;overflow-wrap:anywhere}'
        '.gw-sub li small{color:var(--muted,#5B6B82);font-size:12px;margin-left:4px}.gw-sub li i{font-style:normal;font-size:11.5px;font-weight:800;color:#047857;margin-left:5px}'
        '.gw-sub li i.p{color:#B35C00}'
        '</style>')

def load(n):
    try: return json.load(open(os.path.join(DATA, n + '.json'), encoding='utf-8'))
    except Exception: return None

# ───────────── 공무원 ─────────────
def gosi_pages(G):
    rows = [r for r in G['rows'] if r.get('y') and r.get('sub')]
    by = collections.defaultdict(list)
    for r in rows: by[r['t']].append(r)
    made, cards = [], []
    for tc, _ in G['tests']:
        rs = by.get(tc)
        if not rs: continue
        slug, nm = SLUG.get(tc, 'test-' + tc), SHORT.get(tc, rs[0]['nm'])
        path = f'/ipsi/gongmuwon/{slug}.html'
        ys = sorted({r['y'] for r in rs}, reverse=True)
        subs = collections.Counter(r['sub'] for r in rs)
        top = [s for s, _ in subs.most_common(6)]
        lo, hi = ys[-1], ys[0]
        title = f'{nm} 기출문제 PDF·정답 ({lo}~{hi}년, 과목별)'
        desc = (f'{nm} 필기시험 기출문제 PDF와 정답을 연도별·과목별로 정리했어요. {lo}년부터 {hi}년까지 {len(subs)}개 과목, '
                f'{", ".join(top[:4])} 등. 인사혁신처 공식 페이지에서 받는 방법도 함께 안내해요.')
        cr, crld = crumb(('공무원 기출', '/ipsi/gongmuwon/'), (nm, ''))
        secs = []
        for y in ys:
            g = sorted([r for r in rs if r['y'] == y], key=lambda r: (r['sub'], r['bk']))
            seen = collections.OrderedDict()
            for r in g: seen.setdefault(r['sub'], []).append(r)
            lis = []
            for sub, items in seen.items():
                bks = '·'.join(sorted({i['bk'] for i in items if i['bk']}))
                a = next((ANS.get(i['ans']) for i in items if ANS.get(i['ans'])), '')
                lis.append(f'<li>{E(sub)}{"<small>" + E(bks) + "책형</small>" if bks else ""}{"<i" + ("" if a == "최종정답" else " class=p") + ">" + a + "</i>" if a else ""}</li>')
            secs.append(f'<details class="qg"{" open" if y == ys[0] else ""}><summary>{y}년 {E(nm)} <em>{len(seen)}개 과목</em></summary><ul class="gw-sub">{"".join(lis)}</ul></details>')
        how = (f'<ol class="gw-how"><li>아래 버튼으로 인사혁신처 <b>국가공무원 채용시스템 → 선택형 문제/정답</b> 페이지를 열어요.</li>'
               f'<li>시험 종류에서 <b>{E(rs[0]["nm"])}</b>을 고르고, 과목을 하나 골라요.</li>'
               f'<li>연도·책형별로 나오는 <b>PDF 다운로드</b>와 <b>최종정답</b> 버튼을 누르면 돼요.</li></ol>'
               f'<a class="gw-btn" href="{GOSI_URL}" target="_blank" rel="noopener nofollow">인사혁신처 공식 페이지에서 받기</a>')
        ans = (f'<b>{nm}</b> 기출은 인사혁신처가 문제(PDF·한글 파일)와 정답을 공식 공개해요. 지금 확인되는 자료는 <b>{lo}~{hi}년 {len(ys)}개 연도, {len(subs)}개 과목</b>이에요 '
               f'({GE.fmt_date(G["checked"])} 확인). 파일은 공식 페이지 안에서만 내려받을 수 있어서, 이 페이지에서는 어떤 연도·과목이 있는지 한눈에 보고 공식 페이지에서 바로 찾을 수 있게 정리했어요.')
        qa = [(f'{nm} 기출문제 PDF는 어디서 받나요?', f'인사혁신처 국가공무원 채용시스템의 ‘선택형 문제/정답’ 메뉴에서 시험 종류와 과목을 고르면 연도별 PDF와 한글 파일, 정답을 받을 수 있어요. 무료이고 회원가입이 필요 없어요.'),
              ('정답가안과 최종정답은 뭐가 다른가요?', '시험 직후 먼저 공개하는 게 정답가안이고, 이의제기를 검토한 뒤 확정한 게 최종정답이에요. 공부할 때는 최종정답을 기준으로 채점하세요.'),
              ('책형(가·나)은 무엇인가요?', '부정행위를 막으려고 문제 순서만 바꾼 시험지예요. 문제 내용은 같으니 하나만 골라 풀고 같은 책형의 정답으로 채점하면 돼요.')]
        main = (f'<header class="top hub">{cr}<h1>{E(title.split(" (")[0])}</h1><p class="lead">{lo}년부터 {hi}년까지 {E(nm)} 필기시험 기출문제가 어떤 과목으로 공개돼 있는지 연도별로 정리했어요.</p>'
                f'<p class="gc-ans">{ans}</p></header>'
                f'<section class="card"><h2>공식 PDF 받는 법</h2>{how}</section>'
                f'<section class="card"><h2>연도별 공개 과목</h2>{"".join(secs)}<p class="gc-src">출처: 인사혁신처 국가공무원 채용시스템 선택형 문제/정답 목록</p></section>'
                + faq_html(qa) +
                '<section class="card"><h2>다른 공무원 시험 기출</h2><p class="gc-nav"><a href="/ipsi/gongmuwon/">공무원 기출 전체</a><a href="/ipsi/imyong/">임용시험 기출</a><a href="/ipsi/gichul/">수능 기출</a></p></section>')
        ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path, "description": desc, "inLanguage": "ko"}]
        made.append(page(path, title + ' | 홍라이프 도구', desc, XCSS + main, ld))
        cards.append((tc, nm, slug, lo, hi, len(subs), len(ys)))
    # 허브
    path = '/ipsi/gongmuwon/'
    title = '공무원 기출문제 PDF·정답 모음 (9급·7급·지방직·5급, 연도별)'
    desc = '9급·7급·지방직·5급·계리직·기상직 공무원 필기시험 기출문제 PDF와 정답을 시험별·연도별·과목별로 정리했어요. 인사혁신처 공식 페이지에서 받는 방법도 안내해요.'
    cr, crld = crumb(('공무원 기출', ''))
    li = ''.join(f'<li><a href="/ipsi/gongmuwon/{s}.html"><b>{E(n)}</b><span>{lo}~{hi}년 · {ns}과목</span></a></li>' for _, n, s, lo, hi, ns, _ in cards)
    qa = [('공무원 기출문제는 무료인가요?', '네. 인사혁신처가 국가직·지방직 필기시험 문제와 정답을 무료로 공개해요. 회원가입 없이 PDF와 한글 파일로 받을 수 있어요.'),
          ('지방직 기출도 있나요?', '인사혁신처가 출제하는 지방직 공무원 시험(제1회·제2회)도 같은 곳에서 공개돼요. 위 목록에서 지방직을 고르세요.')]
    main = (f'<header class="top hub">{cr}<h1>공무원 기출문제 PDF·정답 모음</h1><p class="lead">국가직·지방직 공무원 필기시험 기출문제가 시험별로 어떤 연도·과목까지 공개돼 있는지 정리했어요.</p>'
            f'<p class="gc-ans">인사혁신처는 공무원 필기시험의 문제와 정답을 공식 공개해요. 시험을 고르면 연도별 공개 과목과 공식 PDF 받는 법이 나와요 ({GE.fmt_date(G["checked"])} 확인).</p></header>'
            f'<section class="card"><h2>시험별 기출 ({len(cards)}개 시험)</h2><ul class="gy">{li}</ul></section>' + faq_html(qa) +
            '<section class="card"><h2>다른 시험 기출</h2><p class="gc-nav"><a href="/ipsi/imyong/">임용시험 기출</a><a href="/ipsi/gichul/">수능·모의평가 기출</a></p></section>')
    ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path, "description": desc, "inLanguage": "ko"}]
    made.append(page(path, title + ' | 홍라이프 도구', desc, XCSS + main, ld))
    return made

# ───────────── 임용 ─────────────
def flabel(fn):
    n = fn.rsplit('.', 1)[0]; ext = fn.rsplit('.', 1)[-1].upper() if '.' in fn else ''
    kind = '정답' if re.search('정답|답안|채점', n) else ('듣기' if re.search('듣기|음원', n) else '문제')
    m = re.search(r'([1-4])\s*교시', n) or re.search(r'([1-4])\s*차', n)
    part = (m.group(1) + ('교시' if '교시' in m.group(0) else '차')) if m else ''
    return ' '.join(x for x in (part, kind, ext) if x)

def links(files):
    return '<span class="ql">' + ''.join(f'<a{" class=a" if flabel(n).startswith("정답") else ""} href="{KDL}{s}" target="_blank" rel="noopener nofollow" title="{E(n)} (한국교육과정평가원 공식 파일)">{E(flabel(n))}</a>' for n, s in files) + '</span>'

def imyong_pages(I):
    B = I['boards']; made = []
    years = sorted({x['y'] for v in B.values() for x in v if x['y']}, reverse=True)
    for y in years:
        mid = [x for x in B.get('mid', []) if x['y'] == y and x['files']]
        ele = [x for x in B.get('ele', []) if x['y'] == y and x['files']]
        if not mid and not ele: continue
        path = f'/ipsi/imyong/imyong-{y}.html'
        title = f'{y}학년도 임용시험 기출문제 PDF (중등·초등, {int(y) - 1}년 시행)'
        desc = (f'{y}학년도 교원 임용시험 기출문제 PDF를 과목별로 모았어요. 중등 {len(mid)}개 과목(교육학·국어·수학·영어 등)과 유치원·초등·특수 시험지를 '
                f'한국교육과정평가원 공식 파일로 바로 받을 수 있어요.')
        cr, crld = crumb(('임용 기출', '/ipsi/imyong/'), (f'{y}학년도', ''))
        def ul(items):
            items = sorted(items, key=lambda x: (0 if '교육학' in x['title'] else 1, -x['views']))
            return '<ul class="qa">' + ''.join(f'<li><div><b>{E(x["title"])}</b><small>평가원 게시 {GE.fmt_date(x["date"])} · 조회 {GE.man(x["views"])}회</small></div>{links(x["files"])}</li>' for x in items) + '</ul>'
        secs = ''
        if mid: secs += f'<details class="qg" open><summary>{y}학년도 중등교사 임용시험 <em>{len(mid)}개 과목</em></summary>{ul(mid)}</details>'
        if ele: secs += f'<details class="qg"{"" if mid else " open"}><summary>{y}학년도 유치원·초등·특수 임용시험 <em>{len(ele)}개</em></summary>{ul(ele)}</details>'
        tv = sum(x['views'] for x in mid + ele)
        ans = (f'<b>{y}학년도 임용시험</b>은 {int(y) - 1}년 11월에 1차 시험을 치렀어요. 평가원이 공개한 문제지를 과목별로 모았고, 이 게시글들은 평가원 사이트에서 모두 {GE.man(tv)}회 조회됐어요. '
               '임용 1차는 서답형이라 평가원은 정답 대신 문제지를 공개해요.')
        qa = [('임용시험 정답도 있나요?', '중등 임용 1차는 쓰는 서답형이라 평가원이 정답표를 따로 공개하지 않아요. 채점기준은 응시자가 성적 발표 뒤 열람 신청으로 볼 수 있어요.'),
              ('파일을 내려받으면 바로 볼 수 있나요?', '대부분 PDF라 바로 열려요. 묶음 파일은 압축(ZIP)을 풀어야 해요.')]
        nav = ' '.join(f'<a href="/ipsi/imyong/imyong-{z}.html">{z}학년도</a>' for z in years[:8] if z != y)
        main = (f'<header class="top hub">{cr}<h1>{y}학년도 임용시험 기출문제 PDF</h1><p class="lead">중등교사와 유치원·초등·특수교사 임용시험 문제지를 과목별로 모았어요. 버튼을 누르면 한국교육과정평가원 공식 PDF가 바로 열려요.</p>'
                f'<p class="gc-ans">{ans}</p></header><section class="card"><h2>과목별 문제지 PDF</h2>{secs}'
                f'<p class="gc-src">출처: 한국교육과정평가원 교원임용 기출문제 게시판</p></section>' + faq_html(qa) +
                f'<section class="card"><h2>다른 학년도</h2><p class="gc-nav"><a href="/ipsi/imyong/">임용 기출 전체</a>{nav}</p></section>')
        ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path, "description": desc, "inLanguage": "ko"}]
        made.append(page(path, title + ' | 홍라이프 도구', desc, XCSS + main, ld))
    path = '/ipsi/imyong/'
    ys = [re.search(r'(\d{4})', p).group(1) for p in made]
    title = f'임용시험 기출문제 PDF 전체 ({ys[-1]}~{ys[0]}학년도) · 중등·초등 과목별'
    desc = f'{ys[-1]}학년도부터 {ys[0]}학년도까지 교원 임용시험(중등·유치원·초등·특수) 기출문제 PDF를 학년도별·과목별로 정리했어요. 한국교육과정평가원 공식 파일로 바로 연결돼요.'
    cr, crld = crumb(('임용 기출', ''))
    li = ''.join(f'<li><a href="/ipsi/imyong/imyong-{y}.html"><b>{y}학년도</b><span>{int(y) - 1}년 시행</span></a></li>' for y in ys)
    allm = [x for x in I['boards'].get('mid', []) if x['files']]
    top = sorted(allm, key=lambda x: -x['views'])[:10]
    rows = ''.join(f'<tr><td>{i + 1}</td><td><a href="/ipsi/imyong/imyong-{x["y"]}.html">{x["y"]}학년도 {E(x["title"])}</a></td><td class="n">{x["views"]:,}회</td></tr>' for i, x in enumerate(top))
    qa = [('임용 기출은 몇 년 치가 있나요?', f'평가원 게시판에 올라온 {ys[-1]}학년도부터 {ys[0]}학년도까지 정리했어요. 매주 게시판을 확인해 새 시험을 반영해요.')]
    main = (f'<header class="top hub">{cr}<h1>임용시험 기출문제 PDF 전체</h1><p class="lead">중등교사, 유치원·초등·특수교사 임용시험 문제지를 학년도별로 정리했어요.</p>'
            f'<p class="gc-ans">학년도를 고르면 과목별 평가원 공식 PDF 버튼이 나와요 ({GE.fmt_date(I["checked"])} 확인).</p></header>'
            f'<section class="card"><h2>학년도별 기출 ({len(ys)}개 학년도)</h2><ul class="gy">{li}</ul></section>'
            f'<section class="card"><h2>가장 많이 본 중등 임용 기출 TOP 10</h2><table class="gc-t"><thead><tr><th>순위</th><th>시험</th><th>조회</th></tr></thead><tbody>{rows}</tbody></table></section>'
            + faq_html(qa) + '<section class="card"><h2>다른 시험 기출</h2><p class="gc-nav"><a href="/ipsi/gongmuwon/">공무원 기출</a><a href="/ipsi/gichul/">수능·모의평가 기출</a></p></section>')
    ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path, "description": desc, "inLanguage": "ko"}]
    made.append(page(path, title + ' | 홍라이프 도구', desc, XCSS + main, ld))
    return made

def register(paths):
    sm = os.path.join(root, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
    smadd = ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{GE.CHECKED}</lastmod></url>\n' for p in paths if f'{SITE}{p}<' not in s)
    if smadd: open(sm, 'w', encoding='utf-8').write(s.replace('</urlset>', smadd + '</urlset>', 1))
    idx = os.path.join(root, 'index.html'); s = open(idx, encoding='utf-8').read()
    TRIP = '"u":"/trip/"}'
    ent = []
    if '/ipsi/gongmuwon/' in paths and '"u":"/ipsi/gongmuwon/"' not in s:
        ent.append({"t": "공무원 기출문제 PDF·정답 (9급·7급·지방직)", "d": "시험별·연도별 공개 과목, 공식 PDF 받는 법", "k": "공무원 기출 9급 기출 7급 기출 지방직 기출 국가직 기출 공무원 기출문제 pdf 공무원 정답 인사혁신처 기출 계리직 기출 국어 영어 한국사 행정법 행정학", "c": "입시·시험", "u": "/ipsi/gongmuwon/"})
    if '/ipsi/imyong/' in paths and '"u":"/ipsi/imyong/"' not in s:
        ent.append({"t": "임용시험 기출문제 PDF (중등·초등)", "d": "학년도별·과목별 평가원 공식 PDF", "k": "임용 기출 임용고시 기출 중등임용 기출 초등임용 기출 교육학 기출 임용 기출문제 pdf 평가원 임용", "c": "입시·시험", "u": "/ipsi/imyong/"})
    if ent and TRIP in s:
        open(idx, 'w', encoding='utf-8').write(s.replace(TRIP, TRIP + ',' + ','.join(json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in ent), 1))
    # /ipsi/ 허브 시험별 섹션에 링크 추가
    p = os.path.join(root, 'ipsi', 'index.html'); s = open(p, encoding='utf-8').read()
    if 'id="exam-sec"' in s and '/ipsi/gongmuwon/' not in s:
        add = ''
        if '/ipsi/gongmuwon/' in paths: add += '<h3 style="margin:14px 0 8px">공무원</h3><ul class="tlist"><li><a href="/ipsi/gongmuwon/"><b>공무원 기출문제 PDF·정답 모음</b><span>9급·7급·지방직·5급 시험별 연도·과목, 공식 PDF 받는 법</span></a></li></ul>'
        if '/ipsi/imyong/' in paths: add += '<h3 style="margin:14px 0 8px">임용시험</h3><ul class="tlist"><li><a href="/ipsi/imyong/"><b>임용시험 기출문제 PDF 전체</b><span>중등·초등 학년도별 과목별 평가원 공식 PDF</span></a></li></ul>'
        i = s.find('</section>', s.find('id="exam-sec"'))
        s = s[:i] + add + s[i:]; open(p, 'w', encoding='utf-8').write(s)
    print('more exam pages:', len(paths), 'sitemap +', smadd.count('<url>'))

if __name__ == '__main__':
    made = []
    g = load('gosi'); i = load('imyong')
    if g: made += gosi_pages(g)
    if i: made += imyong_pages(i)
    if made: register(made)
    else: print('no 공무원·임용 data yet')
