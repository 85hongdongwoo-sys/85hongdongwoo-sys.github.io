"""입시·시험: 수능·모의평가 기출 페이지 생성 (배포 때 실행, build/exams/data/kice.json 기반).
- /ipsi/gichul/               기출 전체 허브 (학년도 목록, 많이 본 기출, 실전 타이머)
- /ipsi/gichul/suneung-YYYY.html  학년도별: 수능 + 6월·9월 모의평가, 과목별 공식 PDF 링크
- /ipsi/ 허브를 '입시·시험'으로 바꾸고 시험별 섹션 추가, 사이트 분류 이름 '입시' → '입시·시험'
파일은 우리 서버에 두지 않고 평가원 공식 다운로드 주소로만 연결한다.
사용: python3 build/exams/gen_exams.py _site"""
import html, json, os, re, sys, collections

root = sys.argv[1] if len(sys.argv) > 1 else '_site'
HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, 'data', 'kice.json'), encoding='utf-8'))
SITE = 'https://honglife.co.kr'
DL = 'https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq='
BOARD = {'su': 'https://www.suneung.re.kr/boardCnts/list.do?boardID=1500234&m=0403&s=suneung',
         'mo': 'https://www.suneung.re.kr/boardCnts/list.do?boardID=1500236&m=0403&s=suneung'}
CHECKED = K.get('checked', '')
E = html.escape


def fmt_date(d):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', d or '')
    return f'{int(m.group(1))}년 {int(m.group(2))}월 {int(m.group(3))}일' if m else ''


def man(n):
    return f'{n / 10000:.1f}만'.replace('.0만', '만') if n >= 10000 else f'{n:,}'


# ── 템플릿: 기존 페이지의 머리·바닥을 그대로 쓴다
TPL = open(os.path.join(root, 'ipsi', 'pyeonip-2027.html'), encoding='utf-8').read()
HEAD = TPL[:TPL.find('</head>')]
HEAD = re.sub(r'<script type="application/ld\+json">.*?</script>', '', HEAD, flags=re.S)
BODY_TOP = TPL[TPL.find('</head>'):TPL.find('<main')]
FOOT = TPL[TPL.find('<footer', TPL.find('</main>')):]

CSS = ('<style id="gc-css">'
       '.gc-ans{background:#F3F8FF;border:1px solid #D6E6FD;border-radius:12px;padding:12px 14px;margin:12px 0 0;line-height:1.65;font-size:14.5px}'
       '.qg{border:1px solid var(--line-s,#E3E7EE);border-radius:12px;margin:0 0 8px;background:#fff}'
       '.qg summary{cursor:pointer;padding:12px 14px;font-weight:800;color:var(--head,#111);font-size:15px;list-style-position:inside}'
       '.qg summary em{font-style:normal;font-weight:400;font-size:12.5px;color:var(--muted,#5B6B82);margin-left:4px}'
       '.qa{list-style:none;margin:0;padding:0 10px 8px}'
       '.qa li{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:9px 4px;border-top:1px solid var(--line-s,#E3E7EE)}'
       '.qa li>div{min-width:0}.qa li b{font-size:14.5px;color:var(--head,#111);word-break:keep-all}'
       '.qa li small{display:block;font-size:12px;color:var(--muted,#5B6B82);margin-top:2px}'
       '.ql{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end;flex:0 1 auto}'
       '.ql a{display:inline-block;padding:6px 10px;border-radius:8px;background:#EEF4FF;color:#1D4ED8;font-size:13px;font-weight:700;text-decoration:none;white-space:nowrap}'
       '.ql a.a{background:#FFF1E6;color:#B35C00}.ql a.l{background:#F1F3F5;color:#333}'
       '.gy{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;list-style:none;margin:0;padding:0}'
       '.gy a{display:block;padding:12px;border:1px solid var(--line-s,#E3E7EE);border-radius:12px;text-decoration:none;color:inherit;background:#fff}'
       '.gy a b{display:block;font-size:16px;color:var(--head,#111)}.gy a span{font-size:12.5px;color:var(--muted,#5B6B82)}'
       '.gc-t{width:100%;border-collapse:collapse;font-size:14px}.gc-t th,.gc-t td{padding:8px 6px;border-bottom:1px solid var(--line-s,#E3E7EE);text-align:left;vertical-align:top}'
       '.gc-t th{white-space:nowrap;color:var(--muted,#5B6B82);font-weight:700}.gc-t td.n{text-align:right;white-space:nowrap}'
       '.tm{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin:0 0 12px}'
       '.tm button{padding:10px 8px;border:1px solid var(--line-s,#E3E7EE);border-radius:10px;background:#fff;font:inherit;font-size:14px;cursor:pointer}'
       '.tm button[aria-pressed=true]{background:#1D4ED8;color:#fff;border-color:#1D4ED8}'
       '.tm-o{text-align:center;padding:16px;border-radius:14px;background:#F8FAFC;border:1px solid var(--line-s,#E3E7EE)}'
       '.tm-o b{display:block;font-size:44px;font-variant-numeric:tabular-nums;letter-spacing:1px;color:#111}'
       '.tm-o span{font-size:13px;color:var(--muted,#5B6B82)}.tm-c{display:flex;gap:8px;justify-content:center;margin-top:10px}'
       '.tm-c button{padding:9px 18px;border-radius:10px;border:0;background:#1D4ED8;color:#fff;font:inherit;font-weight:700;cursor:pointer}'
       '.tm-c button+button{background:#E9ECEF;color:#333}'
       '.gc-nav{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}.gc-nav a{font-weight:700}'
       '.gc-src{font-size:12.5px;color:var(--muted,#5B6B82);line-height:1.6}'
       '@media(max-width:640px){.qa li{flex-direction:column;align-items:stretch}.ql{justify-content:flex-start}.tm-o b{font-size:38px}'
       '.gc-t{font-size:13px}}'
       '</style>')

# 현행 수능 시간표 (평가원 시행 기본계획 기준, 2027학년도)
TIMER = [('국어', 80), ('수학', 100), ('영어', 70), ('한국사', 30), ('탐구 1과목', 30), ('탐구 2과목', 30), ('제2외국어/한문', 40)]
TIMER_HTML = ('<section class="card" id="timer"><h2>실전 타이머 (수능 시간표 그대로)</h2>'
              '<p class="gc-src" style="margin:0 0 10px">과목을 고르고 시작을 누르면 실제 수능 시험 시간만큼 거꾸로 세요. 끝나면 소리와 진동으로 알려요. 화면을 닫아도 시작한 시각 기준으로 다시 맞춰져요.</p>'
              '<div class="tm" role="group" aria-label="과목">' +
              ''.join(f'<button type="button" data-m="{m}" aria-pressed="{"true" if i == 0 else "false"}">{n}<br><small>{m}분</small></button>' for i, (n, m) in enumerate(TIMER)) +
              '</div><div class="tm-o"><b id="tmv">80:00</b><span id="tml">국어 · 80분</span></div>'
              '<div class="tm-c"><button type="button" id="tms">시작</button><button type="button" id="tmr">처음으로</button></div></section>')
TIMER_JS = r'''<script>(function(){var bs=[].slice.call(document.querySelectorAll('.tm button')),v=document.getElementById('tmv'),l=document.getElementById('tml'),s=document.getElementById('tms'),r=document.getElementById('tmr');if(!v)return;
var K='hl-exam-timer',min=80,name='국어',end=0,left=80*60,t=null;
function p(n){return(n<10?'0':'')+n}function show(x){x=Math.max(0,Math.round(x));v.textContent=(x>=3600?Math.floor(x/3600)+':'+p(Math.floor(x%3600/60)):p(Math.floor(x/60)))+':'+p(x%60);}
function save(){try{localStorage.setItem(K,JSON.stringify({min:min,name:name,end:end,left:left}))}catch(e){}}
function beep(){try{var c=new(window.AudioContext||window.webkitAudioContext)(),o=c.createOscillator();o.connect(c.destination);o.frequency.value=880;o.start();setTimeout(function(){o.stop()},900)}catch(e){}try{navigator.vibrate&&navigator.vibrate([300,150,300])}catch(e){}}
function tick(){var x=(end-Date.now())/1000;show(x);if(x<=0){clearInterval(t);t=null;end=0;left=0;s.textContent='시작';l.textContent=name+' · 시간 종료';beep();save();}}
function pick(b){bs.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});min=+b.dataset.m;name=b.childNodes[0].textContent;stop();left=min*60;show(left);l.textContent=name+' · '+min+'분';save();}
function stop(){if(t){clearInterval(t);t=null}if(end){left=(end-Date.now())/1000;end=0}s.textContent=left<min*60&&left>0?'이어서':'시작';}
bs.forEach(function(b){b.addEventListener('click',function(){pick(b)})});
s.addEventListener('click',function(){if(t){stop();save();return}if(left<=0)left=min*60;end=Date.now()+left*1000;t=setInterval(tick,250);tick();s.textContent='멈춤';save();});
r.addEventListener('click',function(){stop();left=min*60;show(left);s.textContent='시작';l.textContent=name+' · '+min+'분';save();});
try{var o=JSON.parse(localStorage.getItem(K)||'null');if(o){bs.forEach(function(b){if(+b.dataset.m===o.min&&b.childNodes[0].textContent===o.name)pick(b)});if(o.end&&o.end>Date.now()){end=o.end;t=setInterval(tick,250);tick();s.textContent='멈춤';}else if(o.left>0&&o.left<o.min*60){left=o.left;show(left);s.textContent='이어서';}}}catch(e){}
})();</script>'''


def head(title, desc, url, ld):
    h = HEAD
    h = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h, count=1)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(desc)}">', h, count=1)
    lds = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)
    return h + CSS + lds


def page(path, title, desc, main, ld, extra_js=''):
    url = SITE + path
    s = head(title, desc, url, ld) + BODY_TOP + '<main class="wrap wide">' + main + '</main>' + extra_js + FOOT
    out = os.path.join(root, path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s)
    return path


def crumb(*items):
    parts = ['<a href="/">홈</a>', '<a href="/ipsi/">입시·시험</a>'] + [
        (f'<a href="{u}">{E(n)}</a>' if u else E(n)) for n, u in items]
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
        for i, (n, u) in enumerate([('홈', '/'), ('입시·시험', '/ipsi/')] + [(n, u) for n, u in items if u])]}
    return '<p class="crumb">' + ' › '.join(parts) + '</p>', ld


def faq_ld(qa):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in qa]}


def faq_html(qa):
    return '<section class="card"><h2>자주 묻는 질문</h2><dl class="pe-faq">' + ''.join(f'<dt>{E(q)}</dt><dd>{a}</dd>' for q, a in qa) + '</dl></section>'


# ── 파일 이름 → 버튼 이름
def label(fn):
    n = fn.rsplit('.', 1)[0]
    ext = fn.rsplit('.', 1)[-1].lower() if '.' in fn else ''
    var = ''
    for pat, lab in ((r'[AＡ]\s*형|A형|_A_|A-|수학A|영어A|국어_?A', 'A형'), (r'[BＢ]\s*형|B형|_B_|B-|수학B|영어B|국어_?B', 'B형'),
                     (r'가\s*형|\(가\)|가형', '가형'), (r'나\s*형|\(나\)|나형', '나형')):
        if re.search(pat, n):
            var = lab
            break
    side = '짝수형' if '짝수' in n else ''
    if '듣기' in n or '음원' in n or 'MP3' in n.upper():
        if '대본' in n:
            return '듣기 대본', 'l'
        return '듣기 MP3' + (' (' + var + ')' if var else ''), 'l'
    if '대본' in n:
        return '듣기 대본', 'l'
    kind, cls = ('정답', 'a') if '정답' in n else ('문제', '')
    lab = kind + (' ' + var if var else '') + (' ' + side if side else '')
    if ext == 'zip' and kind == '문제' and '듣기' not in n:
        lab += ' (ZIP)'
    elif ext == 'zip':
        lab += ' (ZIP)'
    return lab, cls


def file_links(files):
    out = []
    order = {'': 0, 'a': 1, 'l': 2}
    items = []
    for name, seq in files:
        lab, cls = label(name)
        items.append((order[cls], lab, cls, name, seq))
    items.sort(key=lambda x: (x[0], x[1]))
    for _, lab, cls, name, seq in items:
        out.append(f'<a{" class=" + chr(34) + cls + chr(34) if cls else ""} href="{DL}{seq}" target="_blank" rel="noopener nofollow" '
                   f'title="{E(name)} (한국교육과정평가원 공식 파일)">{E(lab)}</a>')
    return '<span class="ql">' + ''.join(out) + '</span>'


AREA_ORDER = ['국어', '언어', '수학', '수리', '영어', '외국어', '한국사', '사회탐구', '과학탐구', '직업탐구', '제2외국어/한문']
MON_ORDER = {'수능': 0, '9월': 1, '6월': 2, '예비': 3, '예시': 4, '모평': 5}
MON_NAME = {'수능': '대학수학능력시험(본 시험)', '9월': '9월 모의평가', '6월': '6월 모의평가', '예비': '예비평가', '예시': '예시문항', '모평': '모의평가'}


def era(y):
    y = int(y)
    if y <= 2013:
        return ('언어·수리(가/나형)·외국어(영어) 체제',
                '이 시기 수능은 언어·수리·외국어(영어)·탐구·제2외국어/한문 영역으로 치렀어요. 수리는 자연계 중심의 가형과 인문계 중심의 나형으로 나뉘었고, 언어·외국어 영역에는 듣기 평가가 있었어요.')
    if y <= 2016:
        return ('국어·수학 A/B형(수준별) 체제',
                '2014~2016학년도에는 영역 이름이 국어·수학·영어로 바뀌고, 쉬운 A형과 어려운 B형 중 하나를 고르는 수준별 시험을 치렀어요. 영어 수준별 시험은 2014학년도 한 해만 시행됐어요.')
    if y <= 2021:
        return ('국어 통합 · 수학 가/나형 · 한국사 필수 체제',
                '2017학년도부터 국어는 하나의 시험으로 합쳐지고 수학은 가형·나형으로 나뉘었어요. 한국사는 2017학년도부터 필수 영역이 되었고, 영어는 2018학년도부터 원점수 90점 이상이면 1등급인 절대평가로 바뀌었어요.')
    return ('공통+선택과목 체제 (문·이과 통합형)',
            '2022학년도부터 국어(화법과 작문/언어와 매체)와 수학(확률과 통계/미적분/기하)은 공통과목에 선택과목 하나를 더해 치르고, 탐구는 사회·과학 구분 없이 2과목까지 골라요. 영어·한국사는 절대평가예요.')


def build():
    su, mo = K['boards']['su'], K['boards']['mo']
    allp = [dict(x, b='su') for x in su] + [dict(x, b='mo') for x in mo]
    years = collections.defaultdict(list)
    for x in allp:
        # 2005학년도(7차 교육과정 수능) 이후 수능·6월·9월만 — 예비평가·예시문항은 게시판 학년도 표기가 섞여 있어 제외
        if re.fullmatch(r'\d{4}', x['y']) and int(x['y']) >= 2005 and x['mon'] in ('수능', '6월', '9월') and x['files']:
            years[x['y']].append(x)
    ys = sorted(years, reverse=True)
    made = []
    for i, y in enumerate(ys):
        made.append(year_page(y, years[y], ys))
    made.append(hub_page(ys, years, allp))
    return made


def year_page(y, items, ys):
    yi = int(y)
    path = f'/ipsi/gichul/suneung-{y}.html'
    groups = collections.defaultdict(list)
    for x in items:
        groups[x['mon']].append(x)
    mons = sorted(groups, key=lambda m: MON_ORDER.get(m, 9))
    has_su = '수능' in groups
    era_t, era_d = era(y)
    total_views = sum(x['views'] for x in items)
    su_date = fmt_date(groups['수능'][0]['date']) if has_su else ''
    title = f'{y}학년도 수능 기출문제 PDF·정답 ({int(y) - 1}년 11월 시행) + 6월·9월 모의평가 PDF'
    if not has_su:
        title = f'{y}학년도 6월·9월 모의평가 기출문제 PDF·정답 (평가원 공식)'
    desc = (f'{y}학년도 ' + (f'수능({int(y) - 1}년 11월 시행)과 ' if has_su else '') + '6월·9월 모의평가 기출문제 PDF·정답표 PDF·영어 듣기 파일을 과목별로 정리했어요. '
            f'한국교육과정평가원 공식 다운로드로 바로 연결되고, 실제 시험 시간 타이머와 그해 시험 체제({era_t}) 설명을 함께 담았어요.')
    cr, crld = crumb(('수능·모의평가 기출', '/ipsi/gichul/'), (f'{y}학년도', ''))
    secs = []
    for m in mons:
        g = sorted(groups[m], key=lambda x: (AREA_ORDER.index(x['area']) if x['area'] in AREA_ORDER else 99, -x['views']))
        lis = []
        for x in g:
            sub = f'평가원 게시 {fmt_date(x["date"])} · 조회 {man(x["views"])}회'
            lis.append(f'<li><div><b>{E(x["area"])}</b><small>{sub}</small></div>{file_links(x["files"])}</li>')
        nm = MON_NAME.get(m, m)
        board = BOARD['su' if m == '수능' else 'mo']
        secs.append(f'<details class="qg"{" open" if m == mons[0] else ""}><summary>{y}학년도 {nm} <em>{len(g)}개 영역</em></summary>'
                    f'<ul class="qa">{"".join(lis)}</ul><p class="gc-src" style="margin:0 14px 10px">출처: <a href="{board}" target="_blank" rel="noopener nofollow">한국교육과정평가원 기출문제 게시판</a></p></details>')
    lead = (f'{y}학년도 ' + ('대학수학능력시험(수능)과 ' if has_su else '') + '6월·9월 모의평가의 문제지 PDF와 정답표 PDF를 영역별로 모았어요. '
            '버튼을 누르면 한국교육과정평가원 공식 PDF 파일이 바로 열려요.')
    ans = (f'<b>{y}학년도 수능</b>은 {yi - 1}년 11월에 치러졌고, 평가원은 {su_date}에 문제지와 정답표를 공개했어요. '
           if has_su else f'<b>{y}학년도 수능</b> 문제는 평가원 게시판에 아직 올라오지 않았어요. ')
    ans += (f'이 페이지의 {len(items)}개 영역 게시글은 평가원 사이트에서 모두 {man(total_views)}회 조회됐어요. '
            f'그해 시험은 <b>{era_t}</b>였어요.')
    if y == '2027':
        ans += ' 2027학년도 수능(2026년 11월 19일) 문제·정답과 예상 등급컷은 <a href="/ipsi/suneung-2027.html">2027 수능 등급컷 페이지</a>에 있어요.'
    idx = ys.index(y)
    newer = ys[idx - 1] if idx > 0 else None
    older = ys[idx + 1] if idx + 1 < len(ys) else None
    nav = ('<nav class="gc-nav" aria-label="다른 학년도">' +
           (f'<a href="/ipsi/gichul/suneung-{older}.html">‹ {older}학년도</a>' if older else '<span></span>') +
           '<a href="/ipsi/gichul/">전체 학년도</a>' +
           (f'<a href="/ipsi/gichul/suneung-{newer}.html">{newer}학년도 ›</a>' if newer else '<span></span>') + '</nav>')
    how = ('<section class="card"><h2>기출문제 이렇게 활용하세요</h2><ul>'
           '<li><b>실전처럼 시간 재기:</b> 아래 실전 타이머로 국어 80분, 수학 100분, 영어 70분처럼 실제 시간에 맞춰 풀어 보세요.</li>'
           '<li><b>정답표로 채점:</b> 정답 버튼을 열어 맞춰 보고, 틀린 문항 번호를 따로 적어 두었다가 일주일 뒤 다시 풀어요.</li>'
           '<li><b>체제가 다른 해는 골라서:</b> ' + E(era_t) + ' 시기 문제예요. 지금 수능과 과목 구성이 다르면 같은 개념을 묻는 문항 위주로 풀면 돼요.</li>'
           '<li><b>탐구·제2외국어는 ZIP:</b> 과목이 많은 영역은 압축 파일 하나에 과목별 PDF가 들어 있어요.</li></ul></section>')
    qa = [(f'{y}학년도 수능 기출문제는 어디서 받나요?',
           f'한국교육과정평가원 수능 홈페이지의 기출문제 게시판에서 무료로 받을 수 있어요. 이 페이지의 버튼은 그 공식 파일로 바로 연결돼요.'),
          (f'{y}학년도 수능은 언제 시행됐나요?',
           f'학년도는 대학에 들어가는 해를 뜻해서, {y}학년도 수능은 그 전해인 {yi - 1}년 11월에 치러졌어요.'),
          ('문제지 저작권은 누구에게 있나요?',
           '문제지 저작권은 한국교육과정평가원에 있어요. 개인 공부용으로 내려받아 풀 수 있지만, 허락 없이 복제해 배포하거나 출판하면 안 돼요. 홍라이프는 파일을 올리지 않고 공식 주소로만 연결해요.'),
          ('6월·9월 모의평가는 수능과 어떻게 다른가요?',
           '6월·9월 모의평가는 평가원이 그해 수능과 같은 방식으로 출제하는 시험이에요. 난이도와 출제 경향을 가늠할 수 있어서 수능 기출 다음으로 많이 풀어요.'),
          ('수능 시험 시간은 과목별로 얼마인가요?',
           '현행 수능은 국어 80분, 수학 100분, 영어 70분, 한국사 30분, 탐구 과목당 30분, 제2외국어/한문 40분이에요.')]
    main = (f'<header class="top hub">{cr}<h1>{E(title.split(" (")[0])}</h1><p class="lead">{lead}</p>'
            f'<p class="gc-ans">{ans}</p></header>'
            f'<section class="card"><h2>{y}학년도 문제지·정답표</h2>{"".join(secs)}'
            f'<p class="gc-src">파일은 홍라이프 서버에 없고 평가원 공식 주소로 열려요. 마지막 확인: {fmt_date(CHECKED)}. '
            f'문제지 저작권은 한국교육과정평가원에 있어요.</p></section>'
            f'<section class="card"><h2>{y}학년도 시험 체제: {E(era_t)}</h2><p>{era_d}</p></section>'
            + TIMER_HTML + how + faq_html(qa) +
            f'<section class="card">{nav}</section>'
            '<section class="card rel"><h2>함께 쓰면 좋은 도구</h2><ul class="tlist">'
            f'<li><a href="/ipsi/gichul/"><b>수능·모의평가 기출 전체</b><span>{ys[-1]}~{ys[0]}학년도 학년도별 모음</span></a></li>'
            '<li><a href="/ipsi/suneung-2027.html"><b>2027 수능 등급컷·예상 백분위</b><span>작년 수능과 비교, 수험표 할인</span></a></li>'
            '<li><a href="/ipsi/jeongsi-2027.html"><b>2027 정시 합격 가능성 계산기</b><span>4년제 202개 대학 입결 비교</span></a></li></ul></section>')
    ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path,
                             "description": desc, "inLanguage": "ko",
                             "isBasedOn": {"@type": "WebSite", "name": "한국교육과정평가원 대학수학능력시험", "url": "https://www.suneung.re.kr/"}}]
    return page(path, title + ' | 홍라이프 도구', desc, main, ld, TIMER_JS)


def hub_page(ys, years, allp):
    path = '/ipsi/gichul/'
    lo, hi = ys[-1], ys[0]
    title = f'수능·모의평가 기출문제 PDF 전체 ({lo}~{hi}학년도) · 정답 PDF·듣기 파일 모음'
    desc = (f'{lo}학년도부터 {hi}학년도까지 수능과 6월·9월 모의평가 기출문제 PDF·정답표 PDF·영어 듣기 파일을 학년도별로 정리했어요. '
            '한국교육과정평가원 공식 파일로 바로 연결되고, 가장 많이 본 기출 순위와 실전 타이머도 있어요.')
    cr, crld = crumb(('수능·모의평가 기출', ''))
    cards = []
    for y in ys:
        it = years[y]
        ms = sorted({x['mon'] for x in it}, key=lambda m: MON_ORDER.get(m, 9))
        cards.append(f'<li><a href="/ipsi/gichul/suneung-{y}.html"><b>{y}학년도</b><span>{" · ".join("수능" if m == "수능" else (m + " 모평" if m in ("6월", "9월") else m) for m in ms)}</span></a></li>')
    allp = [x for v in years.values() for x in v]
    top = sorted(allp, key=lambda x: -x['views'])[:15]
    rows = ''.join(f'<tr><td>{i + 1}</td><td><a href="/ipsi/gichul/suneung-{x["y"]}.html">{x["y"]}학년도 {E(MON_NAME.get(x["mon"], x["mon"]).replace("대학수학능력시험(본 시험)", "수능"))} {E(x["area"])}</a></td><td class="n">{x["views"]:,}회</td></tr>'
                   for i, x in enumerate(top))
    su_v = sum(x['views'] for x in allp if x['b'] == 'su')
    mo_v = sum(x['views'] for x in allp if x['b'] == 'mo')
    n_su = len({x['y'] for x in allp if x['b'] == 'su' and x['files']})
    ans = (f'평가원 게시판에 올라온 <b>수능 {n_su}개 학년도</b>와 6월·9월 모의평가 기출을 학년도별로 묶었어요. '
           f'수능 기출 게시글은 평가원 사이트에서 모두 <b>{man(su_v)}회</b>, 모의평가는 <b>{man(mo_v)}회</b> 조회됐어요 ({fmt_date(CHECKED)} 확인). '
           '버튼은 평가원 공식 파일로 바로 연결돼요.')
    qa = [('수능 기출문제는 몇 년도 것부터 받을 수 있나요?',
           f'평가원 게시판에는 2005학년도 수능부터, 모의평가는 그보다 앞선 학년도부터 올라와 있어요. 이 페이지는 2005학년도부터 정리하고, 그 게시판을 매주 확인해서 학년도별로 정리해요. 2004학년도 이전 시험과 예비평가는 평가원 게시판에서 직접 볼 수 있어요.'),
          ('기출은 몇 년 치를 푸는 게 좋나요?',
           '지금 체제와 같은 2022학년도 이후 수능·모의평가를 먼저 모두 풀고, 그 다음 2017~2021학년도처럼 과목 구성이 비슷한 해로 넓히는 방법을 많이 써요. 영역마다 바뀐 범위가 다르니 출제 범위를 확인하며 고르세요.'),
          ('문제지를 인쇄해서 써도 되나요?',
           '개인 공부를 위해 내려받아 인쇄해 푸는 것은 괜찮아요. 다만 저작권은 평가원에 있으니 다른 사람에게 배포하거나 판매하면 안 돼요.'),
          ('파일이 안 열려요.',
           '탐구·제2외국어처럼 과목이 많은 영역은 ZIP 압축 파일이라 압축을 풀어야 PDF가 보여요. 휴대폰에서는 파일 앱의 압축 풀기 기능을 쓰면 돼요. 그래도 안 되면 평가원 게시판에서 직접 받아 보세요.')]
    main = (f'<header class="top hub">{cr}<h1>수능·모의평가 기출문제 PDF 전체</h1>'
            '<p class="lead">수능과 6월·9월 모의평가 기출문제 PDF·정답표 PDF·영어 듣기 파일을 학년도별로 정리했어요. 학년도를 고르면 영역별 공식 파일 버튼이 나와요.</p>'
            f'<p class="gc-ans">{ans}</p></header>'
            f'<section class="card"><h2>학년도별 기출 ({len(ys)}개 학년도)</h2><ul class="gy">{"".join(cards)}</ul></section>'
            f'<section class="card"><h2>가장 많이 본 기출 TOP 15</h2><p class="gc-src" style="margin:0 0 8px">평가원 기출문제 게시판의 게시글 조회수 기준이에요 ({fmt_date(CHECKED)}).</p>'
            f'<div style="overflow-x:auto"><table class="gc-t"><thead><tr><th>순위</th><th>시험</th><th style="text-align:right">조회</th></tr></thead><tbody>{rows}</tbody></table></div></section>'
            '<section class="card"><h2>시험 체제가 바뀐 해</h2><div style="overflow-x:auto"><table class="gc-t"><thead><tr><th>학년도</th><th>체제</th></tr></thead><tbody>'
            + ''.join(f'<tr><td>{a}</td><td>{era(b)[0]}</td></tr>' for a, b in (('2005~2013', 2013), ('2014~2016', 2016), ('2017~2021', 2021), ('2022~', 2027)))
            + '</tbody></table></div></section>'
            + TIMER_HTML + faq_html(qa) +
            '<section class="card rel"><h2>함께 쓰면 좋은 도구</h2><ul class="tlist">'
            '<li><a href="/ipsi/suneung-2027.html"><b>2027 수능 등급컷·예상 백분위</b><span>작년 수능과 비교, 수험표 할인</span></a></li>'
            '<li><a href="/ipsi/jeongsi-2027.html"><b>2027 정시 합격 가능성 계산기</b><span>4년제 202개 대학 입결 비교</span></a></li>'
            '<li><a href="/ipsi/"><b>입시·시험 도구 모음</b><span>입시 도구와 시험별 기출 전체</span></a></li></ul></section>')
    ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + path,
                             "description": desc, "inLanguage": "ko",
                             "hasPart": [{"@type": "WebPage", "url": f"{SITE}/ipsi/gichul/suneung-{y}.html", "name": f"{y}학년도 수능·모의평가 기출"} for y in ys]}]
    return page(path, title + ' | 홍라이프 도구', desc, main, ld, TIMER_JS)


# ── /ipsi/ 허브: '입시·시험' + 시험별 섹션
def patch_hub(ys):
    p = os.path.join(root, 'ipsi', 'index.html')
    s = open(p, encoding='utf-8').read()
    if 'id="exam-sec"' in s:
        return
    s = s.replace('<title>입시 도구 모음 | 홍라이프 도구</title>', '<title>입시·시험 도구 모음 (수능·모의평가 기출, 정시 계산기) | 홍라이프 도구</title>', 1)
    s = s.replace('› 입시</p><h1>입시</h1>', '› 입시·시험</p><h1>입시·시험</h1>', 1)
    s = re.sub(r'(<meta (?:name="description"|property="og:description") content=")',
               lambda m: m.group(1) + f'수능·모의평가 기출문제({ys[-1]}~{ys[0]}학년도)를 평가원 공식 파일로 바로 받고, ', s, count=2)
    s = s.replace('<h2>입시 도구', '<h2>대학 입시 도구', 1)
    recent = ''.join(f'<li><a href="/ipsi/gichul/suneung-{y}.html"><b>{y}학년도 수능·모의평가 기출</b><span>문제지·정답표·듣기 파일 (평가원 공식)</span></a></li>' for y in ys[:4])
    sec = ('<section class="card" id="exam-sec"><h2>시험별 기출문제</h2>'
           '<h3 style="margin:6px 0 8px">수능·모의평가</h3><ul class="tlist">'
           f'<li><a href="/ipsi/gichul/"><b>수능·모의평가 기출문제 전체 ({ys[-1]}~{ys[0]}학년도)</b><span>학년도별 문제지·정답·듣기, 많이 본 기출 순위, 실전 타이머</span></a></li>'
           + recent + '</ul></section>')
    i = s.find('<section class="card rel">')
    s = s[:i] + sec + ' ' + s[i:] if i > 0 else s.replace('</main>', sec + '</main>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('ipsi hub: 입시·시험 + exam section')


def rename_category():
    n = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.html'):
                continue
            fp = os.path.join(dp, f)
            s = open(fp, encoding='utf-8', errors='ignore').read()
            s2 = re.sub(r'(<a href="/ipsi/"[^>]*>)입시(</a>)', r'\1입시·시험\2', s)
            s2 = s2.replace('"c":"입시"', '"c":"입시·시험"')
            s2 = re.sub(r'(<a href="/ipsi/"><img[^>]*><b>)입시(</b>)', r'\1입시·시험\2', s2)
            s2 = re.sub(r'(href="/ipsi/"[^>]*>.{0,400}?<b>)입시(</b>)', r'\1입시·시험\2', s2, flags=re.S)
            if s2 != s:
                open(fp, 'w', encoding='utf-8').write(s2)
                n += 1
    print('category label 입시 → 입시·시험 in', n, 'files')


def register(paths):
    sm = os.path.join(root, 'sitemap.xml')
    s = open(sm, encoding='utf-8').read()
    add = ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{CHECKED}</lastmod></url>\n' for p in paths if f'{SITE}{p}<' not in s)
    if add:
        open(sm, 'w', encoding='utf-8').write(s.replace('</urlset>', add + '</urlset>', 1))
    idx = os.path.join(root, 'index.html')
    s = open(idx, encoding='utf-8').read()
    TRIP = '"u":"/trip/"}'
    if '"u":"/ipsi/gichul/"' not in s and TRIP in s:
        ent = [{"t": "수능·모의평가 기출문제 전체 (학년도별)", "d": "학년도별 문제지·정답·듣기 파일, 많이 본 기출, 실전 타이머",
                "k": "수능 기출 기출문제 수능기출 모의고사 모의평가 모평 6월 모평 9월 모평 수능 정답 정답표 평가원 기출 다운로드 수능 듣기 파일 기출 pdf 시험지 문제지 수능 타이머",
                "c": "입시·시험", "u": "/ipsi/gichul/"}]
        for p in sorted([p for p in paths if 'suneung-' in p], reverse=True):
            y = re.search(r'(\d{4})', p).group(1); y2 = y[2:]
            ent.append({"t": f"{y}학년도 수능·모의평가 기출문제", "d": f"{y}학년도 수능·6월·9월 모평 문제지·정답·듣기 (평가원 공식)",
                        "k": f"{y} 수능 {y}수능 {y2}수능 {y} 기출 {y}학년도 수능 기출 {y} 6월 모평 {y} 9월 모평 {y} 모의고사 {y} 수능 정답 {int(y) - 1} 수능 기출문제 시험지",
                        "c": "입시·시험", "u": p})
        e = ','.join(json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in ent)
        open(idx, 'w', encoding='utf-8').write(s.replace(TRIP, TRIP + ',' + e, 1))
    print('exam pages registered:', len(paths), 'sitemap +', add.count('<url>'))


if __name__ == '__main__':
    made = build()
    ys = sorted({re.search(r'(\d{4})', p).group(1) for p in made if 'suneung-' in p}, reverse=True)
    patch_hub(ys)
    rename_category()
    register(made)
