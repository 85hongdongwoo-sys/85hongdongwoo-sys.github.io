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
GRADES = [('9geup', '9급 공무원', [('국가직', '08'), ('지방직', '33')]),
          ('7geup', '7급 공무원', [('국가직', '06'), ('지방직(제2회)', '34')]),
          ('5geup', '5급 공채·외교관후보자', [('5급 행정', '03'), ('5급 과학기술', '05'), ('외교관후보자', '09')]),
          ('jiyeok', '지역인재 7·9급', [('지역인재 7급', '15'), ('지역인재 9급', '16')]),
          ('mingyeong', '민간경력자 5·7급', [('5급 민경채', '28'), ('7급 민경채', '38')]),
          ('gyeri', '우정9급(계리직)', [('계리직', '18')]),
          ('gisang', '기상직 7·9급', [('7급 기상직', '76'), ('9급 기상직', '78')]),
          ('geunro', '근로감독·산업안전 7급', [('근로감독·산업안전', '96')])]
COMMON = ('국어', '영어', '한국사', '헌법', '언어논리', '자료해석', '상황판단')
# 9급 대표 직렬별 전문과목 (2022년 고교과목 선택 폐지 이후 기준) — 그해 두 과목이 모두 있을 때만 묶어서 보여 준다
JIK = [('일반행정', ('행정법총론', '행정학개론')), ('세무', ('세법개론', '회계학')), ('관세', ('관세법개론', '회계원리')),
       ('교육행정', ('교육학개론', '행정법총론')), ('출입국관리', ('국제법개론', '행정법총론')), ('교정', ('교정학개론', '형사소송법개론')),
       ('보호', ('형사정책개론', '사회복지학개론')), ('검찰·마약수사·철도경찰', ('형사소송법개론', '형법총론')),
       ('고용노동', ('노동법개론', '행정법총론')), ('직업상담', ('노동법개론', '직업상담심리학개론')), ('통계', ('통계학개론', '행정법총론')),
       ('사회복지', ('사회복지학개론', '행정법총론')), ('전산', ('컴퓨터일반', '정보보호론')), ('전기', ('전기이론', '전기기기')),
       ('토목', ('응용역학개론', '토목설계')), ('건축', ('건축계획', '건축구조')), ('기계', ('기계일반', '기계설계')),
       ('화공', ('화학공학일반', '공업화학')), ('농업', ('재배학개론', '식용작물')), ('환경', ('환경공학개론', '화학')),
       ('보건', ('공중보건', '보건행정')), ('간호', ('지역사회간호', '간호관리'))]

def is_common(sub): return any(sub.startswith(c) for c in COMMON)

def chip(sub, items):
    bks = '·'.join(sorted({i['bk'] for i in items if i['bk']}))
    a = next((ANS.get(i['ans']) for i in items if ANS.get(i['ans']) == '최종정답'), '') or next((ANS.get(i['ans']) for i in items if ANS.get(i['ans'])), '')
    return (f'<li data-s="{E(sub)}">{E(sub)}{"<small>" + E(bks) + "책형</small>" if bks else ""}'
            f'{"<i" + ("" if a == "최종정답" else " class=p") + ">" + a + "</i>" if a else ""}</li>')

def year_block(items, use_jik):
    by = collections.OrderedDict()
    for r in sorted(items, key=lambda r: r['sub']): by.setdefault(r['sub'], []).append(r)
    com = [s for s in by if is_common(s)]
    com.sort(key=lambda s: next((i for i, c in enumerate(COMMON) if s.startswith(c)), 99))
    rest = [s for s in by if s not in com]
    h = ''
    if com: h += '<p class="gw-h">공통 과목</p><ul class="gw-sub">' + ''.join(chip(s, by[s]) for s in com) + '</ul>'
    used = set()
    if use_jik:
        grp = []
        for jn, subs in JIK:
            if all(x in by for x in subs):
                grp.append(f'<li class="gw-j" data-j="{E(jn)}"><b>{E(jn)}</b><ul class="gw-sub">' + ''.join(chip(x, by[x]) for x in subs) + '</ul></li>')
                used.update(subs)
        if grp: h += '<p class="gw-h gw-jh">직렬별 전문과목</p><ul class="gw-jl">' + ''.join(grp) + '</ul>'
    left = [s for s in rest if s not in used]
    if left: h += f'<p class="gw-h gw-x">{"그 밖의 직렬 과목" if used else "전공·선택 과목"}</p><ul class="gw-sub gw-x">' + ''.join(chip(s, by[s]) for s in left) + '</ul>'
    return h, len(by)

GX = ('<style id="gc3">.gw-h{font-size:12.5px;font-weight:800;color:var(--muted,#5B6B82);margin:10px 12px 0}'
      '.gw-jl{list-style:none;margin:0;padding:4px 12px 8px;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px}'
      '.gw-j{border:1px solid var(--line-s,#E3E7EE);border-radius:10px;padding:8px 8px 2px;background:#FAFBFD}.gw-j>b{font-size:13.5px;color:var(--head,#111);margin:0 4px}'
      '.gw-j .gw-sub{padding:6px 0 6px}.gw-org{margin:0 0 10px;border-top:1px dashed var(--line-s,#E3E7EE);padding-top:4px}.gw-org:first-of-type{border-top:0}'
      '.gw-org>h3{font-size:14.5px;margin:8px 12px 0;color:#1D4ED8}'
      '.gw-pick{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 0}.gw-pick button{font:inherit;font-size:13.5px;border:1px solid var(--line-s,#E3E7EE);background:#fff;border-radius:999px;padding:7px 11px;cursor:pointer;min-height:36px}'
      '.gw-pick button[aria-pressed=true]{background:#1D4ED8;border-color:#1D4ED8;color:#fff}'
      '.gw-on .gw-j:not(.hit){display:none}.gw-on .gw-sub li.dim{display:none}.gw-on .gw-x{display:none}.gw-on .gw-org.nohit .gw-jh{display:none}</style>')
GJS = r"""<script>(function(){var w=document.getElementById('gw-years'),bs=[].slice.call(document.querySelectorAll('.gw-pick button'));if(!w||!bs.length)return;var K='hl-gw-jik';
function go(j){bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.j===j?'true':'false')});w.classList.toggle('gw-on',!!j);
[].slice.call(w.querySelectorAll('.gw-j')).forEach(function(e){e.classList.toggle('hit',e.dataset.j===j)});[].slice.call(w.querySelectorAll('.gw-org')).forEach(function(o){o.classList.toggle('nohit',!o.querySelector('.gw-j.hit'))});try{localStorage.setItem(K,j||'')}catch(e){}}
bs.forEach(function(b){b.addEventListener('click',function(){go(b.getAttribute('aria-pressed')==='true'?'':b.dataset.j)})});
try{var s=localStorage.getItem(K);if(s&&bs.some(function(b){return b.dataset.j===s}))go(s)}catch(e){}})();</script>"""

def gosi_pages(G):
    rows = [r for r in G['rows'] if r.get('y') and r.get('sub')]
    by = collections.defaultdict(list)
    for r in rows: by[r['t']].append(r)
    made, cards = [], []
    for slug, nm, orgs in GRADES:
        orgs = [(on, tc) for on, tc in orgs if by.get(tc)]
        if not orgs: continue
        rs = [r for _, tc in orgs for r in by[tc]]
        path = f'/ipsi/gongmuwon/{slug}.html'
        ys = sorted({r['y'] for r in rs}, reverse=True); lo, hi = ys[-1], ys[0]
        subs = collections.Counter(r['sub'] for r in rs)
        use_jik = slug == '9geup'
        jiks = [jn for jn, ss in JIK if all(x in subs for x in ss)] if use_jik else []
        on = ' · '.join(o for o, _ in orgs)
        title = f'{nm} 기출문제 PDF·정답 ({lo}~{hi}년, {on}, 과목별)'
        desc = (f'{nm} 필기시험 기출문제 PDF와 정답을 연도별로 {on}을 나눠 정리했어요. 공통 과목(국어·영어·한국사)과 '
                + ('직렬별 전문과목(' + ', '.join(jiks[:5]) + ' 등)' if jiks else '전공 과목') + '을 구분하고, 인사혁신처 공식 페이지에서 받는 방법도 안내해요.')
        cr, crld = crumb(('공무원 기출', '/ipsi/gongmuwon/'), (nm, ''))
        secs = []
        for y in ys:
            blocks, total = '', 0
            for o, tc in orgs:
                it = [r for r in by[tc] if r['y'] == y]
                if not it: continue
                h, n = year_block(it, use_jik); total += n
                blocks += f'<div class="gw-org"><h3>{E(o)} <small style="color:var(--muted,#5B6B82);font-weight:500">{n}개 과목</small></h3>{h}</div>'
            secs.append(f'<details class="qg"{" open" if y == ys[0] else ""}><summary>{y}년 {E(nm)} <em>{" · ".join(o for o, tc in orgs if any(r["y"] == y for r in by[tc]))}</em></summary>{blocks}</details>')
        pick = ('<section class="card"><h2>내 직렬 고르기</h2><p class="gc-src" style="margin:0">고르면 아래 연도별 목록에서 공통 과목과 그 직렬 전문과목만 보여 줘요. 다음에 열 때도 기억해요.</p>'
                '<div class="gw-pick">' + ''.join(f'<button type="button" data-j="{E(j)}" aria-pressed="false">{E(j)}</button>' for j in jiks) + '</div>'
                '<p class="gc-src" style="margin:8px 0 0">대표 직렬 기준이에요. 정확한 시험 과목은 그해 시험 공고를 확인하세요.</p></section>') if jiks else ''
        how = (f'<ol class="gw-how"><li>아래 버튼으로 인사혁신처 <b>국가공무원 채용시스템 → 선택형 문제/정답</b> 페이지를 열어요.</li>'
               f'<li>시험 종류에서 <b>{E(" 또는 ".join(by[tc][0]["nm"] for _, tc in orgs))}</b>을 고르고, 과목을 하나 골라요.</li>'
               f'<li>연도·책형별로 나오는 <b>PDF 다운로드</b>와 <b>최종정답</b> 버튼을 누르면 돼요.</li></ol>'
               f'<a class="gw-btn" href="{GOSI_URL}" target="_blank" rel="noopener nofollow">인사혁신처 공식 페이지에서 받기</a>')
        ans = (f'<b>{nm}</b> 기출은 인사혁신처가 문제(PDF·한글 파일)와 정답을 공식 공개해요. 지금 확인되는 자료는 <b>{lo}~{hi}년 {len(ys)}개 연도, {len(subs)}개 과목</b>이에요 '
               f'({GE.fmt_date(G["checked"])} 확인). 파일은 공식 페이지 안에서만 받을 수 있어서, 여기서는 연도마다 {on}을 나누고 공통·직렬 과목을 구분해 어떤 기출이 있는지 한눈에 보여 줘요.')
        qa = [(f'{nm} 기출문제 PDF는 어디서 받나요?', '인사혁신처 국가공무원 채용시스템의 ‘선택형 문제/정답’ 메뉴에서 시험 종류와 과목을 고르면 연도별 PDF와 한글 파일, 정답을 받을 수 있어요. 무료이고 회원가입이 필요 없어요.'),
              ('국가직과 지방직 문제는 다른가요?', '시험이 따로 치러져서 문제도 달라요. 공통 과목은 출제 경향이 비슷해서 둘 다 풀어 보면 좋아요.'),
              ('정답가안과 최종정답은 뭐가 다른가요?', '시험 직후 먼저 공개하는 게 정답가안이고, 이의제기를 검토한 뒤 확정한 게 최종정답이에요. 공부할 때는 최종정답으로 채점하세요.'),
              ('책형(가·나)은 무엇인가요?', '부정행위를 막으려고 문제 순서만 바꾼 시험지예요. 하나만 골라 풀고 같은 책형의 정답으로 채점하면 돼요.')]
        others = ''.join(f'<a href="/ipsi/gongmuwon/{s}.html">{E(n)}</a>' for s, n, o in GRADES if s != slug and any(by.get(tc) for _, tc in o))
        main = (f'<header class="top hub">{cr}<h1>{E(nm)} 기출문제 PDF·정답</h1><p class="lead">{lo}년부터 {hi}년까지 연도별로 {E(on)}을 나누고, 공통 과목과 직렬 과목을 구분해 정리했어요.</p>'
                f'<p class="gc-ans">{ans}</p></header>{pick}'
                f'<section class="card"><h2>연도별 기출 과목</h2><div id="gw-years">{"".join(secs)}</div><p class="gc-src">출처: 인사혁신처 국가공무원 채용시스템 선택형 문제/정답 목록</p></section>'
                f'<section class="card"><h2>공식 PDF 받는 법</h2>{how}</section>' + faq_html(qa) +
                f'<section class="card"><h2>다른 공무원 시험 기출</h2><p class="gc-nav"><a href="/ipsi/gongmuwon/">공무원 기출 전체</a>{others}</p></section>')
        ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path, "description": desc, "inLanguage": "ko"}]
        made.append(page(path, title + ' | 홍라이프 도구', desc, XCSS + GX + main, ld, GJS if jiks else ''))
        cards.append((nm, slug, lo, hi, len(subs), on))
    path = '/ipsi/gongmuwon/'
    title = '공무원 기출문제 PDF·정답 모음 (9급·7급 국가직·지방직, 직렬별)'
    desc = '9급·7급 국가직·지방직, 5급·계리직·기상직 공무원 필기시험 기출문제 PDF와 정답을 연도별·직렬별로 정리했어요. 인사혁신처 공식 페이지에서 받는 방법도 안내해요.'
    cr, crld = crumb(('공무원 기출', ''))
    li = ''.join(f'<li><a href="/ipsi/gongmuwon/{s}.html"><b>{E(n)}</b><span>{lo}~{hi}년 · {E(o)}</span></a></li>' for n, s, lo, hi, ns, o in cards)
    qa = [('공무원 기출문제는 무료인가요?', '네. 인사혁신처가 국가직·지방직 필기시험 문제와 정답을 무료로 공개해요. 회원가입 없이 PDF와 한글 파일로 받을 수 있어요.'),
          ('지방직 기출도 있나요?', '인사혁신처가 문제를 내는 지방직 시험도 같은 곳에 공개돼요. 9급·7급 페이지에서 연도마다 국가직과 지방직을 나눠 보여 줘요.')]
    main = (f'<header class="top hub">{cr}<h1>공무원 기출문제 PDF·정답 모음</h1><p class="lead">국가직·지방직 공무원 필기시험 기출을 시험별로, 연도마다 국가직·지방직과 직렬 과목을 나눠 정리했어요.</p>'
            f'<p class="gc-ans">인사혁신처는 공무원 필기시험 문제와 정답을 공식 공개해요. 시험을 고르면 연도별 과목과 공식 PDF 받는 법이 나와요 ({GE.fmt_date(G["checked"])} 확인).</p></header>'
            f'<section class="card"><h2>시험별 기출</h2><ul class="gy">{li}</ul></section>' + faq_html(qa) +
            '<section class="card"><h2>다른 시험 기출</h2><p class="gc-nav"><a href="/ipsi/imyong/">임용시험 기출</a><a href="/ipsi/gichul/">수능·모의평가 기출</a></p></section>')
    ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path, "description": desc, "inLanguage": "ko"}]
    made.append(page(path, title + ' | 홍라이프 도구', desc, XCSS + GX + main, ld))
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

SUBJ_SLUG = {'교육학': 'education', '국어': 'korean', '수학': 'math', '영어': 'english', '물리': 'physics', '화학': 'chemistry', '생물': 'biology',
             '지구과학': 'earth-science', '일반사회': 'social', '역사': 'history', '지리': 'geography', '도덕·윤리': 'ethics', '도덕윤리': 'ethics', '윤리': 'ethics',
             '음악': 'music', '미술': 'art', '체육': 'pe', '정보·컴퓨터': 'computer', '정보컴퓨터': 'computer', '한문': 'hanmun', '가정': 'home-ec',
             '기술': 'technology', '보건': 'health', '영양': 'nutrition', '사서': 'librarian', '전문상담': 'counseling', '특수': 'special-ed',
             '중국어': 'chinese', '일본어': 'japanese', '독일어': 'german', '프랑스어': 'french', '스페인어': 'spanish', '러시아어': 'russian',
             '아랍어': 'arabic', '베트남어': 'vietnamese', '공통과학': 'general-science', '공통사회': 'general-social', '농업': 'agriculture',
             '상업': 'commerce', '공업': 'industry', '전기': 'electric', '전자': 'electronics', '기계': 'mechanical', '디자인': 'design', '조리': 'cooking'}
import hashlib
def base_subj(t):
    b = re.sub(r'\s*\((?:[0-9]차|[0-9]교시|[^)]*차)\)\s*$', '', t).strip()
    b = re.sub(r'^\d{4}학년도\s*', '', b)
    return b
def subj_slug(b):
    if b in SUBJ_SLUG: return SUBJ_SLUG[b]
    for k, v in SUBJ_SLUG.items():
        if b.startswith(k): return v + '-' + hashlib.md5(b.encode()).hexdigest()[:4] if b != k else v
    return 's-' + hashlib.md5(b.encode()).hexdigest()[:8]

def ul_items(items, show_year=False):
    return '<ul class="qa">' + ''.join(
        f'<li><div><b>{(x["y"] + "학년도 ") if show_year else ""}{E(x["title"])}</b><small>평가원 게시 {GE.fmt_date(x["date"])} · 조회 {GE.man(x["views"])}회</small></div>{links(x["files"])}</li>'
        for x in items) + '</ul>'

def imyong_pages(I):
    B = I['boards']; made = []
    mid = [x for x in B.get('mid', []) if x['files'] and x['y']]
    ele = [x for x in B.get('ele', []) if x['files'] and x['y']]
    years = sorted({x['y'] for x in mid + ele}, reverse=True)
    # ── 과목별 페이지 (중등) + 유치원·초등·특수
    groups = collections.defaultdict(list)
    for x in mid: groups[base_subj(x['title'])].append(x)
    if ele: groups['__ele__'] = ele
    subj_cards = []
    for b, items in sorted(groups.items(), key=lambda kv: (0 if kv[0] == '교육학' else 1 if kv[0] == '__ele__' else 2, -sum(i['views'] for i in kv[1]))):
        is_ele = b == '__ele__'
        name = '유치원·초등·특수 임용' if is_ele else f'중등 임용 {b}'
        slug = 'elementary' if is_ele else subj_slug(b)
        path = f'/ipsi/imyong/{slug}.html'
        ys = sorted({i['y'] for i in items}, reverse=True); lo, hi = ys[-1], ys[0]
        title = f'{name} 기출문제 PDF ({lo}~{hi}학년도, 연도별)'
        desc = f'{name} 시험 기출문제 PDF를 {lo}학년도부터 {hi}학년도까지 연도별로 모았어요. 한국교육과정평가원 공식 파일로 바로 받을 수 있어요.'
        cr, crld = crumb(('임용 기출', '/ipsi/imyong/'), (name, ''))
        secs = ''
        for y in ys:
            it = sorted([i for i in items if i['y'] == y], key=lambda i: i['title'])
            secs += f'<details class="qg"{" open" if y in ys[:2] else ""}><summary>{y}학년도 <em>{int(y) - 1}년 시행 · {len(it)}건</em></summary>{ul_items(it)}</details>'
        tv = sum(i['views'] for i in items)
        qa = [(f'{name} 기출 정답도 있나요?', '임용 1차는 쓰는 서답형이라 평가원이 정답표를 따로 공개하지 않아요. 채점기준은 응시자가 성적 발표 뒤 열람 신청으로 볼 수 있어요.'),
              ('몇 년 치를 풀면 좋나요?', '지금 시험 체제가 시작된 2014학년도 이후 기출을 먼저 모두 풀고, 교육과정이 바뀐 해는 출제 범위를 확인하며 보세요.')]
        main = (f'<header class="top hub">{cr}<h1>{E(name)} 기출문제 PDF</h1><p class="lead">{lo}학년도부터 {hi}학년도까지 {E(name)} 시험지를 연도별로 모았어요. 버튼을 누르면 평가원 공식 PDF가 바로 열려요.</p>'
                f'<p class="gc-ans"><b>{len(ys)}개 학년도</b> 기출이 있고, 이 게시글들은 평가원 사이트에서 모두 {GE.man(tv)}회 조회됐어요 ({GE.fmt_date(I["checked"])} 확인).</p></header>'
                f'<section class="card"><h2>연도별 시험지 PDF</h2>{secs}<p class="gc-src">출처: 한국교육과정평가원 교원임용 기출문제 게시판</p></section>' + faq_html(qa) +
                '<section class="card"><h2>다른 과목</h2><p class="gc-nav"><a href="/ipsi/imyong/">임용 기출 전체 (과목별)</a><a href="/ipsi/imyong/education.html">교육학</a><a href="/ipsi/gongmuwon/">공무원 기출</a></p></section>')
        ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path, "description": desc, "inLanguage": "ko"}]
        made.append(page(path, title + ' | 홍라이프 도구', desc, XCSS + main, ld))
        subj_cards.append((name.replace('중등 임용 ', ''), slug, lo, hi, tv))
    # ── 학년도별 페이지
    for y in years:
        m = [x for x in mid if x['y'] == y]; e2 = [x for x in ele if x['y'] == y]
        path = f'/ipsi/imyong/imyong-{y}.html'
        title = f'{y}학년도 임용시험 기출문제 PDF ({int(y) - 1}년 시행, 과목별)'
        desc = f'{y}학년도 교원 임용시험 기출문제 PDF를 과목별로 모았어요. 중등 {len({base_subj(x["title"]) for x in m})}개 과목과 유치원·초등·특수 시험지를 평가원 공식 파일로 바로 받을 수 있어요.'
        cr, crld = crumb(('임용 기출', '/ipsi/imyong/'), (f'{y}학년도', ''))
        m.sort(key=lambda x: (0 if '교육학' in x['title'] else 1, x['title']))
        secs = ''
        if m: secs += f'<details class="qg" open><summary>{y}학년도 중등교사 임용시험 <em>{len(m)}건</em></summary>{ul_items(m)}</details>'
        if e2: secs += f'<details class="qg"{"" if m else " open"}><summary>{y}학년도 유치원·초등·특수 <em>{len(e2)}건</em></summary>{ul_items(e2)}</details>'
        nav = ''.join(f'<a href="/ipsi/imyong/imyong-{z}.html">{z}학년도</a>' for z in years[:8] if z != y)
        main = (f'<header class="top hub">{cr}<h1>{y}학년도 임용시험 기출문제 PDF</h1><p class="lead">{int(y) - 1}년에 치른 임용시험 문제지를 과목별로 모았어요. 버튼을 누르면 평가원 공식 PDF가 바로 열려요.</p></header>'
                f'<section class="card"><h2>과목별 시험지 PDF</h2>{secs}<p class="gc-src">출처: 한국교육과정평가원 교원임용 기출문제 게시판</p></section>'
                f'<section class="card"><h2>다른 학년도</h2><p class="gc-nav"><a href="/ipsi/imyong/">과목별로 보기</a>{nav}</p></section>')
        made.append(page(path, title + ' | 홍라이프 도구', desc, XCSS + main, [crld]))
    # ── 허브: 과목별이 먼저
    path = '/ipsi/imyong/'
    title = f'임용시험 기출문제 PDF 과목별 모음 ({years[-1]}~{years[0]}학년도, 중등·초등)'
    desc = f'교원 임용시험 기출문제 PDF를 과목별·학년도별로 정리했어요. 교육학·국어·수학·영어 등 중등 과목과 유치원·초등·특수 시험지를 평가원 공식 파일로 바로 받을 수 있어요.'
    cr, crld = crumb(('임용 기출', ''))
    sc = ''.join(f'<li><a href="/ipsi/imyong/{s}.html"><b>{E(n)}</b><span>{lo}~{hi}학년도</span></a></li>' for n, s, lo, hi, tv in subj_cards)
    yc = ''.join(f'<li><a href="/ipsi/imyong/imyong-{y}.html"><b>{y}학년도</b><span>{int(y) - 1}년 시행</span></a></li>' for y in years)
    qa = [('임용 기출은 몇 년 치가 있나요?', f'평가원 게시판에 올라온 {years[-1]}학년도부터 {years[0]}학년도까지 정리했어요. 매주 게시판을 확인해 새 시험을 반영해요.')]
    main = (f'<header class="top hub">{cr}<h1>임용시험 기출문제 PDF 과목별 모음</h1><p class="lead">과목을 고르면 그 과목 기출을 학년도별로 모아 보여 줘요. 학년도별로도 볼 수 있어요.</p>'
            f'<p class="gc-ans">버튼은 한국교육과정평가원 공식 PDF로 바로 연결돼요 ({GE.fmt_date(I["checked"])} 확인).</p></header>'
            f'<section class="card"><h2>과목별 ({len(subj_cards)}개)</h2><ul class="gy">{sc}</ul></section>'
            f'<section class="card"><h2>학년도별</h2><ul class="gy">{yc}</ul></section>' + faq_html(qa) +
            '<section class="card"><h2>다른 시험 기출</h2><p class="gc-nav"><a href="/ipsi/gongmuwon/">공무원 기출</a><a href="/ipsi/gichul/">수능·모의평가 기출</a></p></section>')
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
    if 'id="exam-list"' in s and '/ipsi/gongmuwon/' not in s:
        add = ''
        if '/ipsi/gongmuwon/' in paths: add += '<li><a href="/ipsi/gongmuwon/"><b>공무원 기출문제 PDF·정답</b><span>9급·7급 국가직·지방직, 직렬별 과목, 공식 PDF 받는 법</span></a></li>'
        if '/ipsi/imyong/' in paths: add += '<li><a href="/ipsi/imyong/"><b>임용시험 기출문제 PDF</b><span>교육학·국어·수학 등 과목별, 학년도별 평가원 공식 PDF</span></a></li>'
        i = s.find('</ul>', s.find('id="exam-list"'))
        s = s[:i] + add + s[i:]; open(p, 'w', encoding='utf-8').write(s)
    print('more exam pages:', len(paths), 'sitemap +', smadd.count('<url>'))

if __name__ == '__main__':
    made = []
    g = load('gosi'); i = load('imyong')
    if g: made += gosi_pages(g)
    if i: made += imyong_pages(i)
    if made: register(made)
    else: print('no 공무원·임용 data yet')
