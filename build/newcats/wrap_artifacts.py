"""Claude 아티팩트(자격증 시험달력, 투자계산기)를 홍라이프 도구 디자인으로 감싸 overlay/에 씀.
- 사이트 공통 head·상단 메뉴·제목 영역·하단을 그대로 쓰고, 앱 부분은 #hlx 안에 넣어 CSS를 범위 제한한다.
- 앱 색·글꼴은 사이트 토큰(Pretendard, 파란 강조색)으로 바꾸고 다크 모드는 뺀다.
- 투자계산기 광고 칸(쿠팡·토스)은 숨긴다.
데이터 블록(const APT / const DATA / const ADS)은 원본 그대로라 예약 작업이 같은 방식으로 고칠 수 있다."""
import re, sys, os, html, json
OUT = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
HEAD = open(f'{D}/tpl_head.html').read()
MID = open(f'{D}/tpl_mid.html').read()
BRAND = open(f'{D}/tpl_brand.html').read()
TAIL = open(f'{D}/tpl_tail.html').read()
SITE = 'https://honglife.co.kr'
LOCK = '<div class="safe"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>{t}</div>'

THEME = """#hlx{--bg:#F2F4F6;--paper:#FFFFFF;--ink:#191F28;--muted:#6B7684;--line:#E5E8EB;--accent:#1B64DA;--accent-soft:#E8F3FF;
--stamp:#E03131;--stamp-soft:#FFF0F0;--tax:#E03131;--tax-soft:#FFF0F0;--ok:#2F9E44;--ok-soft:#EBFBEE;--warn:#B76E00;--warn-soft:#FFF4DB;
--f-display:var(--f);--f-body:var(--f);--f-mono:var(--f);--f-num:var(--f);font-family:var(--f);color:var(--ink);background:transparent;padding:0!important;font-size:15px}
#hlx .wrap{max-width:none!important;margin:0!important;padding:0!important}
#hlx [class*="num"],#hlx .asof,#hlx b{font-variant-numeric:tabular-nums}
#hlx .ad-slot,#hlx .ad,#hlx .ad-foot{display:none!important}
#hlx .info{background:none!important;border:0!important;padding:0!important;margin:0!important;box-shadow:none!important}
"""

def scope(css):
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        sel = css[i:j].strip()
        if sel.startswith('@media') or sel.startswith('@supports'):
            depth, k = 1, j + 1
            while depth and k < n:
                depth += {'{': 1, '}': -1}.get(css[k], 0); k += 1
            inner = css[j + 1:k - 1]
            if 'prefers-color-scheme' in sel:  # 다크 모드 제거
                i = k; continue
            out.append(sel + '{' + scope(inner) + '}'); i = k; continue
        if sel.startswith('@'):  # keyframes, font-face 등 그대로
            depth, k = 1, j + 1
            while depth and k < n:
                depth += {'{': 1, '}': -1}.get(css[k], 0); k += 1
            out.append(css[i:k]); i = k; continue
        k = css.find('}', j); body = css[j + 1:k]; i = k + 1
        sel = re.sub(r'/\*.*?\*/', '', sel, flags=re.S).strip()
        if not sel or 'data-theme="dark"' in sel: continue
        parts = []
        for s in sel.split(','):
            s = s.strip()
            s = re.sub(r'^:root(:not\([^)]*\))?', '#hlx', s)
            s = re.sub(r'^(html|body)\b', '#hlx', s)
            s = s.replace('header.top', 'header.hx-top')
            if not s.startswith('#hlx'):
                s = '#hlx ' + s
            parts.append(s)
        out.append(','.join(parts) + '{' + body + '}')
    return ''.join(out)

PAGES = [
 dict(src='art_exam.html', path='/calendar/exam-schedule.html', name='자격증 시험일정 달력',
      title='2026·2027 자격증 시험일정 달력 (국가기술·국가전문·한국사·토익·JLPT) | 홍라이프 도구',
      desc='큐넷 국가기술자격(기사·산업기사·기능사·기술사)과 국가전문자격, 한국사능력검정시험, 토익, JLPT, 전산세무회계 시험의 원서접수·시험일·합격발표를 한 달력에 모았어요. D-day와 접수 중인 시험을 바로 확인하세요.',
      h1='자격증 시험일정 달력', lead='국가기술·국가전문자격, 한국사, 토익·JLPT, 전산회계·컴활 일정을 한곳에서 보고 공식 접수 페이지로 바로 가요. 접수 중인 시험은 맨 위에 D-day로 보여 줘요.',
      crumb=('날짜·달력', '/calendar/'), lock='관심 시험 표시는 이 기기에만 저장되고 서버로 보내지 않아요',
      hide='#hlx .wrap>header h1,#hlx .wrap>header>p{display:none}#hlx .wrap>header{margin:0 0 4px}'),
 dict(src='art_invest.html', path='/life/invest.html', name='청약·줍줍 일정 + 투자계산기',
      title='청약·줍줍 일정 + 투자계산기 (주식 세금·대출 한도·청약 가점·연금) | 홍라이프 도구',
      desc='오늘 넣을 수 있는 아파트 청약과 무순위 줍줍 일정을 매일 업데이트하고, 주식 매도 세금·배당·대출 한도·청약 가점·연금 계산기까지 한 페이지에서 계산해요.',
      h1='청약·줍줍 일정 + 투자계산기', lead='청약홈에 올라온 일반 청약과 무순위 줍줍 공고를 매일 아침 새로 모으고, 주식·ETF 세금부터 연금·은퇴, 대출 한도·청약 가점·전세 안전도까지 계산기 29가지를 탭으로 바로 써요.',
      crumb=('생활·행정', '/life/'), lock='입력한 숫자는 서버로 전송되지 않고 내 기기에서만 계산돼요',
      hide='#hlx header.hx-top h1,#hlx header.hx-top .sub{display:none}#hlx header.hx-top{padding:0 0 10px!important}'),
]

for p in PAGES:
    s = open(f'{D}/{p["src"]}', encoding='utf-8').read()
    body = s[s.find('<body>') + 6:].replace('</body>', '').replace('</html>', '')
    body = re.sub(r'<title>[^<]*</title>', '', body)
    body = re.sub(r'<link rel="(preconnect|stylesheet)"[^>]*fonts\.(googleapis|gstatic)[^>]*>', '', body)
    css = ''
    def grab(m):
        global css
        css += m.group(1); return ''
    body = re.sub(r'<style[^>]*>(.*?)</style>', grab, body, flags=re.S)
    body = body.replace('<header class="top">', '<header class="hx-top">')
    style = '<style id="hlx-css">' + scope(css) + THEME + p['hide'] + '</style>'
    url = SITE + p['path']
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": p['name'], "url": url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": "ko", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": p['crumb'][0], "item": SITE + p['crumb'][1]}, {"@type": "ListItem", "position": 3, "name": p['name'], "item": url}]}]}
    h = HEAD + f'<title>{html.escape(p["title"])}</title>\n<meta name="description" content="{html.escape(p["desc"])}">\n<link rel="canonical" href="{url}">\n'
    h += f'<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="홍라이프 도구">\n<meta property="og:title" content="{html.escape(p["title"])}"><meta property="og:description" content="{html.escape(p["desc"])}"><meta property="og:image" content="{SITE}/assets/og/site.png">\n'
    h += MID + '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + style + '\n</head>\n<body>\n\n' + BRAND
    h += f'<main class="wrap wide"><header class="top"><p class="crumb"><a href="/">홈</a> › <a href="{p["crumb"][1]}">{p["crumb"][0]}</a></p><h1><b>{html.escape(p["h1"])}</b></h1><p class="lead">{html.escape(p["lead"])}</p>{LOCK.format(t=p["lock"])}</header>'
    h += '<section class="card tool" id="hlx">' + body + '</section></main>' + TAIL
    fp = OUT + p['path']; os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fp, len(h))
