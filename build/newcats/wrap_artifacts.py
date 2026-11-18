"""Claude 아티팩트(자격증 시험달력, 투자계산기)를 홍라이프 도구 페이지로 감싸 overlay/에 씀.
페이지 본문(디자인·스크립트)은 그대로 두고, 사이트 공통 head(제목·설명·애널리틱스·애드센스)와 상단 바·하단 안내만 붙인다."""
import re, sys, os, html
OUT = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
HEAD = open(f'{D}/tpl_head.html').read()  # <!doctype ... gtag, adsense, viewport, naver verif, color-scheme
SITE = 'https://honglife.co.kr'
PAGES = [
 dict(src='art_exam.html', path='/calendar/exam-schedule.html', title='2026·2027 자격증 시험일정 달력 (국가기술·국가전문·한국사·토익·JLPT) | 홍라이프 도구',
      desc='큐넷 국가기술자격(기사·산업기사·기능사·기술사)과 국가전문자격, 한국사능력검정시험, 토익, JLPT, 전산세무회계 시험의 원서접수·시험일·합격발표를 한 달력에 모았어요. D-day와 접수 중인 시험을 바로 확인하세요.',
      crumb=('날짜·달력', '/calendar/'), name='자격증 시험일정 달력'),
 dict(src='art_invest.html', path='/life/invest.html', title='청약·줍줍 일정 + 투자계산기 (주식 세금·대출·연금·부동산) | 홍라이프 도구',
      desc='오늘 넣을 수 있는 아파트 청약과 무순위 줍줍 일정을 매일 업데이트하고, 주식 매도 세금·배당·대출 한도·청약 가점·연금 계산기까지 한 페이지에서 계산해요.',
      crumb=('생활·행정', '/life/'), name='청약·줍줍 일정 + 투자계산기'),
]
BAR = ('<div style="position:relative;z-index:50;background:#fff;border-bottom:1px solid #E5E8EB;font:600 14px/1.4 -apple-system,BlinkMacSystemFont,\'Pretendard\',sans-serif">'
       '<div style="max-width:1100px;margin:0 auto;padding:10px 16px;display:flex;gap:10px;align-items:center;justify-content:space-between">'
       '<a href="/" style="display:flex;gap:8px;align-items:center;color:#191F28;text-decoration:none"><img src="/assets/brand/symbol-small.svg" width="26" height="26" alt="">홍라이프 도구</a>'
       '<span style="font-weight:500;font-size:13px;color:#6B7684"><a href="/" style="color:inherit">홈</a> › <a href="{cu}" style="color:inherit">{cn}</a></span></div></div>')
FOOT = ('<div style="max-width:960px;margin:24px auto 0;padding:18px 16px 40px;border-top:1px solid #E5E8EB;font:13px/1.6 -apple-system,BlinkMacSystemFont,sans-serif;color:#6B7684">'
        '<a href="/" style="color:inherit;margin-right:12px">홍라이프 도구 홈</a><a href="/about.html" style="color:inherit;margin-right:12px">사이트 소개</a><a href="/privacy.html" style="color:inherit">개인정보처리방침</a>'
        '<div style="margin-top:6px">이 페이지의 일정과 숫자는 공식 발표를 바탕으로 정기적으로 업데이트해요. 접수 전에는 반드시 공식 기관 공고를 확인하세요. © 홍라이프 · honglife.co.kr</div></div>')
for p in PAGES:
    s = open(f'{D}/{p["src"]}', encoding='utf-8').read()
    s = re.sub(r'<title>[^<]*</title>', '', s, count=1)
    i = s.find('<body>')
    body = s[i + len('<body>'):].replace('</body>', '').replace('</html>', '')
    art_head_style = s[:i]
    st = re.search(r'<head>(.*?)</head>', art_head_style, flags=re.S)
    inner_head = re.sub(r'<meta charset=[^>]*>|<meta name=viewport[^>]*>', '', st.group(1)) if st else ''
    url = SITE + p['path']
    h = HEAD + f'<title>{html.escape(p["title"])}</title>\n<meta name="description" content="{html.escape(p["desc"])}">\n<link rel="canonical" href="{url}">\n'
    h += f'<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:title" content="{html.escape(p["title"])}"><meta property="og:description" content="{html.escape(p["desc"])}"><meta property="og:image" content="{SITE}/assets/og/site.png"><meta property="og:site_name" content="홍라이프 도구">\n'
    h += '<link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="any">\n'
    h += ('<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"WebApplication","name":"' + p['name'] + '","url":"' + url + '","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","inLanguage":"ko","offers":{"@type":"Offer","price":"0","priceCurrency":"KRW"}},'
          '{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"' + SITE + '/"},{"@type":"ListItem","position":2,"name":"' + p['crumb'][0] + '","item":"' + SITE + p['crumb'][1] + '"},{"@type":"ListItem","position":3,"name":"' + p['name'] + '","item":"' + url + '"}]}]}</script>\n')
    h += inner_head + '\n</head>\n<body>\n' + BAR.format(cu=p['crumb'][1], cn=p['crumb'][0]) + body + FOOT + '\n</body>\n</html>\n'
    fp = OUT + p['path']; os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(h)
    print('wrote', fp, len(h))
