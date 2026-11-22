"""자동차 내비·빌트인 캠 업데이트 안내 (현대·기아·제네시스) → overlay/drive/update/
공식 업데이트 사이트(update.hyundai.com / update.kia.com / update.genesis.com) 이용가이드를 2026-11-21에 확인한 내용만 쓴다.
파일은 올리지 않고 공식 사이트로만 연결. 단계 그림은 직접 그린 SVG(로고 없음)."""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'overlay', 'drive', 'update')
SITE = 'https://honglife.co.kr'
CHECKED = '2026년 11월 21일'
E = html.escape

TPL = open(os.path.join(ROOT, 'overlay', 'drive', 'gas-station.html'), encoding='utf-8').read()
HEAD = re.sub(r'<script type="application/ld\+json">.*?</script>', '', TPL[:TPL.find('</head>')], flags=re.S)
BODY_TOP = TPL[TPL.find('</head>'):TPL.find('<main')]
FOOT = TPL[TPL.find('<footer', TPL.find('</main>')):]

CSS = ('<style id="cu-css">'
       '.cu-ans{background:#F3F8FF;border:1px solid #D6E6FD;border-radius:12px;padding:12px 14px;margin:12px 0 0;line-height:1.7;font-size:15px}'
       '.cu-step{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;align-items:center;padding:14px 0;border-top:1px solid var(--line-s,#E3E7EE)}'
       '.cu-step:first-of-type{border-top:0}.cu-step svg{width:100%;height:auto;display:block}'
       '.cu-step h3{margin:0 0 6px;font-size:17px;line-height:1.4;word-break:keep-all}.cu-step h3 em{font-style:normal;display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;background:#1D4ED8;color:#fff;font-size:14px;margin-right:6px;vertical-align:1px}'
       '.cu-step p{margin:0;line-height:1.7;font-size:15px;word-break:keep-all}.cu-step .tip{margin-top:6px;font-size:13.5px;color:var(--muted,#5B6B82)}'
       '.cu-go{display:inline-block;margin:6px 6px 0 0;padding:11px 16px;border-radius:12px;background:#1D4ED8;color:#fff!important;font-weight:800;text-decoration:none}'
       '.cu-go.s{background:#EEF4FF;color:#1D4ED8!important}'
       '.cu-t{width:100%;border-collapse:collapse;font-size:14.5px}.cu-t th,.cu-t td{padding:9px 8px;border-bottom:1px solid var(--line-s,#E3E7EE);text-align:left;vertical-align:top;word-break:keep-all}'
       '.cu-t th{color:var(--muted,#5B6B82);font-weight:700;white-space:nowrap}.cu-t td:first-child{min-width:5.5em}'
       '.cu-chk{list-style:none;padding:0;margin:0}.cu-chk li{padding:8px 0 8px 30px;position:relative;line-height:1.6;border-bottom:1px dashed var(--line-s,#E3E7EE)}'
       '.cu-chk li:before{content:"✓";position:absolute;left:4px;top:7px;width:20px;height:20px;border-radius:50%;background:#EEF4FF;color:#1D4ED8;font-weight:900;font-size:12px;display:grid;place-items:center}'
       '.cu-src{font-size:12.5px;color:var(--muted,#5B6B82);line-height:1.6}'
       '.cu-brand{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;list-style:none;margin:0;padding:0}'
       '.cu-brand a{display:block;padding:14px;border:1px solid var(--line-s,#E3E7EE);border-radius:14px;text-decoration:none;color:inherit;background:#fff}'
       '.cu-brand a b{display:block;font-size:17px;color:var(--head,#111)}.cu-brand a span{font-size:13px;color:var(--muted,#5B6B82)}'
       '@media(max-width:640px){.cu-step{grid-template-columns:1fr;gap:8px}.cu-t{font-size:13.5px}}'
       '</style>')

# ── 단계 그림 (직접 그린 SVG, 로고 없음) ──────────────────────────
FONT = "font-family=\"Pretendard Variable,Pretendard,'Noto Sans KR',sans-serif\""


def ring(x, y, w, h, n):
    return (f'<rect x="{x - 4}" y="{y - 4}" width="{w + 8}" height="{h + 8}" rx="9" fill="none" stroke="#E03131" stroke-width="3"/>'
            f'<circle cx="{x + w + 4}" cy="{y - 4}" r="10" fill="#E03131"/><text x="{x + w + 4}" y="{y}" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">{n}</text>')


def mark(x, y, n):
    return (f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="#E03131" stroke-width="3"/>'
            f'<circle cx="{x + 18}" cy="{y - 16}" r="10" fill="#E03131"/><text x="{x + 18}" y="{y - 12}" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">{n}</text>')


def pc(inner, url):
    return (f'<svg viewBox="0 0 360 230" role="img" {FONT}><rect x="20" y="8" width="320" height="196" rx="12" fill="#1F2937"/>'
            f'<rect x="30" y="18" width="300" height="176" rx="6" fill="#fff"/>'
            f'<rect x="30" y="18" width="300" height="22" rx="6" fill="#E9ECEF"/><circle cx="42" cy="29" r="3.5" fill="#FA5252"/><circle cx="53" cy="29" r="3.5" fill="#FAB005"/><circle cx="64" cy="29" r="3.5" fill="#40C057"/>'
            f'<rect x="76" y="23" width="200" height="12" rx="6" fill="#fff"/><text x="84" y="32.5" font-size="8.5" fill="#495057">{E(url)}</text>'
            f'{inner}<path d="M0 206 H360 L345 222 H15 Z" fill="#ADB5BD"/></svg>')


def car(inner):
    return (f'<svg viewBox="0 0 360 230" role="img" {FONT}><rect x="6" y="20" width="348" height="190" rx="18" fill="#111827"/>'
            f'<rect x="18" y="32" width="324" height="166" rx="10" fill="#1E293B"/>{inner}</svg>')


def btn(x, y, w, h, t, fill='#1D4ED8', fg='#fff', fs=11):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + fs / 2.8}" text-anchor="middle" font-size="{fs}" font-weight="700" fill="{fg}">{E(t)}</text>')


def S1(url):
    return pc('<text x="44" y="64" font-size="13" font-weight="800" fill="#111">차량 소프트웨어 업데이트</text>'
              '<text x="44" y="82" font-size="10" fill="#495057">PC에 프로그램을 먼저 설치해요</text>'
              + btn(44, 96, 120, 30, 'Windows용 받기') + btn(184, 96, 104, 30, 'Mac용 받기', '#E9ECEF', '#333')
              + '<rect x="44" y="140" width="244" height="40" rx="6" fill="#F8F9FA" stroke="#DEE2E6"/>'
              '<text x="56" y="164" font-size="11" fill="#333">프로그램 이름: Navigation Updater</text>' + ring(44, 96, 120, 30, 1), url)


def S2(url):
    return pc('<text x="44" y="62" font-size="13" font-weight="800" fill="#111">내 차 맞춤 업데이트 조회</text>'
              '<rect x="44" y="74" width="118" height="26" rx="5" fill="#fff" stroke="#ADB5BD"/><text x="54" y="91" font-size="10.5" fill="#333">차종 선택 ▾</text>'
              '<rect x="170" y="74" width="118" height="26" rx="5" fill="#fff" stroke="#ADB5BD"/><text x="180" y="91" font-size="10.5" fill="#333">연식·사양 선택 ▾</text>'
              '<rect x="44" y="110" width="244" height="46" rx="6" fill="#F8F9FA" stroke="#DEE2E6"/><text x="56" y="130" font-size="10.5" fill="#333">내비게이션 업데이트</text><text x="56" y="146" font-size="9.5" fill="#868E96">최신 지도·소프트웨어</text>'
              + btn(212, 120, 62, 26, '다운로드') + ring(212, 120, 62, 26, 2), url)


def S3():
    return pc('<text x="44" y="62" font-size="13" font-weight="800" fill="#111">Navigation Updater</text>'
              '<text x="44" y="84" font-size="10.5" fill="#333">다운로드 완료</text><rect x="44" y="92" width="244" height="10" rx="5" fill="#E9ECEF"/><rect x="44" y="92" width="244" height="10" rx="5" fill="#1D4ED8"/>'
              '<text x="288" y="84" text-anchor="end" font-size="10.5" font-weight="800" fill="#1D4ED8">100%</text>'
              + btn(44, 118, 120, 30, 'USB로 복사') + ring(44, 118, 120, 30, 3)
              + '<g transform="translate(222 120)"><rect x="0" y="6" width="56" height="26" rx="5" fill="#495057"/><rect x="56" y="12" width="14" height="14" rx="2" fill="#ADB5BD"/><text x="28" y="23" text-anchor="middle" font-size="9" fill="#fff" font-weight="700">USB·SD</text></g>',
              '공식 업데이트 프로그램')


def S4():
    rows = [('설정', 60), ('일반', 92), ('SW 정보/업데이트', 124)]
    s = ''.join(f'<rect x="30" y="{y}" width="120" height="26" rx="6" fill="{"#334155" if i < 2 else "#1D4ED8"}"/>'
                f'<text x="42" y="{y + 17}" font-size="11.5" fill="#fff" font-weight="700">{E(t)}</text>'
                + (f'<text x="156" y="{y + 18}" font-size="13" fill="#94A3B8">›</text>' if i < 2 else '')
                for i, (t, y) in enumerate(rows))
    return car('<text x="30" y="52" font-size="11" fill="#94A3B8">전체 메뉴</text>' + s
               + '<rect x="176" y="60" width="152" height="90" rx="8" fill="#0F172A" stroke="#334155"/>'
               '<text x="188" y="82" font-size="11" fill="#CBD5E1">현재 버전 확인</text><text x="188" y="100" font-size="10" fill="#64748B">새 업데이트가 있어요</text>'
               + btn(212, 112, 80, 28, '업데이트') + ring(212, 112, 80, 28, 4))


def S5():
    return car('<text x="180" y="78" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">업데이트 중이에요</text>'
               '<rect x="60" y="92" width="240" height="10" rx="5" fill="#334155"/><rect x="60" y="92" width="150" height="10" rx="5" fill="#60A5FA"/>'
               '<text x="180" y="126" text-anchor="middle" font-size="11" fill="#FCD34D">⚠ 전원을 끄거나 USB·SD를 빼지 마세요</text>'
               '<text x="180" y="146" text-anchor="middle" font-size="10" fill="#94A3B8">끝나면 자동으로 다시 켜져요</text>'
               '<text x="180" y="178" text-anchor="middle" font-size="10" fill="#64748B">시간은 데이터 양에 따라 수십 분 걸릴 수 있어요</text>')


def SCAM():
    rows = [('빌트인 캠', 60), ('빌트인 캠 설정', 92), ('업데이트', 124)]
    s = ''.join(f'<rect x="30" y="{y}" width="130" height="26" rx="6" fill="{"#334155" if i < 2 else "#1D4ED8"}"/>'
                f'<text x="42" y="{y + 17}" font-size="11.5" fill="#fff" font-weight="700">{E(t)}</text>' for i, (t, y) in enumerate(rows))
    return car('<text x="30" y="52" font-size="11" fill="#94A3B8">전체 메뉴</text>' + s + ring(30, 124, 130, 26, '✓')
               + '<rect x="186" y="60" width="142" height="90" rx="8" fill="#0F172A" stroke="#334155"/>'
               '<text x="198" y="84" font-size="10.5" fill="#CBD5E1">빌트인 캠 전용</text><text x="198" y="100" font-size="10.5" fill="#CBD5E1">USB 단자에 꽂기</text>'
               '<text x="198" y="124" font-size="10" fill="#FCD34D">시동 ON · 기어 P</text>')


# ── 브랜드 데이터 (공식 이용가이드 확인값) ───────────────────────
COMMON_USB = ['고급형 1세대', '고급형 5세대', '표준형 5W세대', 'ccNC', '표준형 1·2세대 (DVD 포함)']
COMMON_SD = ['고급형 2세대', '표준형 3세대', '표준형 4세대', '표준형 5세대']
B = {
    'hyundai': {'name': '현대', 'full': '현대자동차', 'host': 'update.hyundai.com', 'conn': '블루링크',
                'usb': COMMON_USB + ['벨로스터 내비게이션', '베라크루즈 (DVD)'], 'sd': COMMON_SD + ['경제형 5세대'],
                'cam1': ['더 뉴 아반떼 (하이브리드 포함)', '더 뉴 코나 (하이브리드 포함)', 'DN8 쏘나타 (하이브리드 포함)', '아이오닉 5', '더 뉴 그랜저 (하이브리드 포함)', '아이오닉 6', '더 뉴 싼타페 (하이브리드 포함)', '더 뉴 팰리세이드', '디 올 뉴 투싼 (하이브리드 포함)', '스타리아'],
                'cam2': ['쏘나타 디 엣지 (하이브리드 포함)', '더 뉴 투싼 (하이브리드 포함)', '디 올 뉴 그랜저 (하이브리드 포함)', '아이오닉 5 N', '디 올 뉴 코나 (하이브리드, EV 포함)', '더 뉴 아이오닉 5', '디 올 뉴 싼타페 (하이브리드 포함)'],
                'g': {'info': 'lR1ECJ', 'cam': 'bOCI9f', 'ota': 'nnYbY8'}},
    'kia': {'name': '기아', 'full': '기아', 'host': 'update.kia.com', 'conn': '기아 커넥트(Kia Connect, 옛 UVO)',
            'usb': ['고급형 1세대', '고급형 5세대', '고급형 6세대', '표준형 5W세대', 'ccNC', '표준형 1·2세대 (DVD 포함)'], 'sd': COMMON_SD + ['경제형 5세대'],
            'cam1': ['EV6', '더 뉴 셀토스', '3세대 K5 (하이브리드 포함)', '디 올 뉴 기아 니로 (EV 포함)', 'K7 Premier (하이브리드 포함)', '스포티지 (하이브리드 포함)', 'K8 (하이브리드 포함)', '4세대 쏘렌토 (하이브리드 포함)', 'K9', '4세대 카니발'],
            'cam2': ['EV9', '더 뉴 K5 (하이브리드 포함)', 'EV6', '더 뉴 카니발 (하이브리드 포함)', '더 뉴 쏘렌토 (하이브리드 포함)'],
            'g': {'info': 'OsC7sO', 'cam': 'nvXhQ8', 'ota': 'ye6Yfa'}},
    'genesis': {'name': '제네시스', 'full': '제네시스', 'host': 'update.genesis.com', 'conn': '제네시스 커넥티드 서비스',
                'usb': ['고급형 1세대', '고급형 5세대', '고급형 6세대', 'ccIC', 'ccIC27', 'EQ900', '표준형 5W세대', '표준형 1·2세대 (DVD 포함)'], 'sd': COMMON_SD,
                'cam1': ['더 뉴 G70', 'GV60', '디 올 뉴 G80 (2022 이후 포함)', 'GV70', 'Electrified G80', 'Electrified G70', 'G90', 'GV80 (2022 이후 포함)'],
                'cam2': [],
                'g': {'info': 'oKQl3A', 'cam': 'Ows7Nt', 'ota': 'ya6Ige'}},
}


def head(title, desc, url, ld):
    h = HEAD
    h = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h, count=1)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(desc)}">', h, count=1)
    return h + CSS + ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)


def write(path, title, desc, main, ld):
    out = os.path.join(ROOT, 'overlay', path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(head(title, desc, SITE + path, ld) + BODY_TOP + '<main class="wrap wide">' + main + '</main>' + FOOT)


def crumb(items):
    parts = ['<a href="/">홈</a>', '<a href="/drive/">자동차·지도</a>'] + [f'<a href="{u}">{E(n)}</a>' if u else E(n) for n, u in items]
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
        for i, (n, u) in enumerate([('홈', '/'), ('자동차·지도', '/drive/')] + [(n, u) for n, u in items if u])]}
    return '<p class="crumb">' + ' › '.join(parts) + '</p>', ld


def faq(qa):
    return ('<section class="card"><h2>자주 묻는 질문</h2><dl class="pe-faq">' + ''.join(f'<dt>{E(q)}</dt><dd>{a}</dd>' for q, a in qa) + '</dl></section>',
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in qa]})


def step(n, title, body, svg, tip=''):
    return (f'<div class="cu-step"><div>{svg}</div><div><h3><em>{n}</em>{E(title)}</h3><p>{body}</p>'
            + (f'<p class="tip">{tip}</p>' if tip else '') + '</div></div>')


def brand_page(k):
    b = B[k]
    base = f'https://{b["host"]}/KR/KO'
    path = f'/drive/update/{k}.html'
    title = f'{b["name"]} 내비게이션 업데이트 방법 (USB·SD 카드, 2026 최신) + 빌트인 캠 업데이트'
    desc = (f'{b["name"]} 순정 내비게이션 지도·소프트웨어 업데이트를 그림으로 쉽게 설명해요. Navigation Updater 설치, 내 차 맞춤 업데이트 조회, '
            f'USB·SD 카드 준비(32GB·exFAT), 차에서 업데이트하는 순서와 빌트인 캠 업데이트까지 공식 안내 기준으로 정리했어요.')
    cr, crld = crumb([('차 업데이트 모음', '/drive/update/'), (f'{b["name"]} 내비 업데이트', '')])
    ans = (f'<b>{b["conn"]}</b>에 가입한 차는 업데이트가 <b>무선으로 자동</b> 내려와요(도착 시점은 통신·차량 상태에 따라 달라요). '
           f'가입하지 않았거나 빨리 받고 싶다면, PC에 <b>Navigation Updater</b>를 깔고 '
           f'<b>32GB 이상 USB 메모리나 SD 카드(exFAT)</b>에 파일을 받아 차에 꽂으면 돼요. 차에서는 <b>설정 → 일반 → SW 정보/업데이트 → 업데이트</b>를 누르세요.')
    steps = (step(1, 'PC에 업데이트 프로그램 깔기',
                  f'{b["name"]} 공식 업데이트 사이트에서 <b>Navigation Updater</b>를 받아 설치해요. 윈도우용과 맥용이 따로 있어요.',
                  S1(f'{b["host"]}'), '맥에서 "확인되지 않은 개발자" 창이 뜨면 시스템 설정 → 보안 및 개인 정보 보호에서 "확인 없이 열기"를 누르면 돼요.')
             + step(2, '내 차 고르고 다운로드 누르기',
                    '사이트 첫 화면의 <b>[내 차 맞춤 업데이트 조회]</b>에서 차종을 고르고 <b>[다운로드]</b>를 누르면 설치한 프로그램이 열려요. 회원가입을 안 해도 비회원 메뉴로 받을 수 있어요.',
                    S2(f'{b["host"]}'))
             + step(3, 'USB·SD 카드에 복사하기',
                    '프로그램에서 받을 위치를 정하고 다운로드가 끝나면 <b>[USB로 복사]</b>를 눌러요. 처음부터 USB·SD 카드를 저장 위치로 골랐다면 이 단계는 건너뛰어요.',
                    S3(), 'PC에서 USB가 "로컬 디스크"로 보이면 복사가 안 될 수 있어요. 다른 USB를 쓰세요.')
             + step(4, '차에 꽂고 업데이트 누르기',
                    '차에 USB 메모리나 SD 카드를 꽂고 내비 <b>전체 메뉴 → 설정 → 일반 → SW 정보/업데이트</b>에서 <b>[업데이트]</b>를 눌러요.',
                    S4(), '오래된 내비는 메뉴 이름이 조금 달라요(예: 표준형 1·2세대는 SW 정보 → USB 업데이트). 공식 이용가이드의 내비 종류별 방법을 함께 보세요.')
             + step(5, '끝날 때까지 기다리기',
                    '업데이트 중에는 <b>전원을 끄거나 USB·SD를 빼면 안 돼요.</b> 끝나면 내비가 저절로 다시 켜지고 버전이 바뀌어요.',
                    S5(), '시동 버튼 ON 상태로 한다면 배터리가 충분한지 먼저 확인하세요. 겨울이나 오래 안 탄 차는 방전되기 쉬워요.'))
    t_usb = ', '.join(b['usb'])
    t_sd = ', '.join(b['sd'])
    stor = ('<section class="card"><h2>USB인지 SD 카드인지 확인하기</h2>'
            '<p>내비 종류에 따라 꽂는 저장장치가 달라요. 내 차 내비 종류는 공식 사이트에서 차종을 고르면 알려줘요.</p>'
            '<div style="overflow-x:auto"><table class="cu-t"><thead><tr><th>필요한 것</th><th>내비 종류 (공식 안내)</th></tr></thead><tbody>'
            f'<tr><td><b>USB 메모리</b></td><td>{E(t_usb)}</td></tr><tr><td><b>SD 카드</b></td><td>{E(t_sd)}</td></tr></tbody></table></div>'
            '<h3 style="margin-top:16px">준비물 체크</h3><ul class="cu-chk">'
            '<li><b>용량 32GB 이상</b> (공식 권장)</li><li><b>exFAT</b> 형식 — 형식이 다르면 내비가 못 알아볼 수 있어요</li>'
            '<li>SD 카드는 <b>UHS-I(초당 10MB 이상)</b> 권장</li><li>일부 내비는 <b>USB-C</b> 타입이 필요해요</li>'
            '<li>PC (윈도우 또는 맥) + 인터넷</li></ul>'
            '<p class="cu-src">USB·SD 문제로 생긴 데이터 손실은 제조사 책임 범위가 아니라고 공식 안내에 적혀 있어요. 중요한 파일이 든 USB는 쓰지 마세요.</p></section>')
    cam_rows = ''.join(f'<li>{E(x)}</li>' for x in b['cam1'])
    cam = ('<section class="card"><h2>빌트인 캠(블랙박스) 업데이트</h2>'
           + step('✓', '빌트인 캠 1: USB로 직접 업데이트',
                  '공식 사이트 [내 차 맞춤 업데이트 조회]에서 빌트인 캠 파일을 받아 <b>압축을 풀지 말고 그대로</b> USB 최상위 폴더에 넣어요. '
                  '<b>내비 USB 단자가 아닌 빌트인 캠 전용 USB 단자</b>에 꽂고, 전체 메뉴 → 빌트인 캠 → 빌트인 캠 설정 → 업데이트를 눌러요.',
                  SCAM(), '업데이트 중에는 시동을 켜고 기어를 P에 두세요. 그동안 녹화는 안 돼요. USB는 FAT16·FAT32·NTFS·exFAT 모두 돼요.')
           + f'<p style="margin-top:10px"><b>빌트인 캠 1 적용 차종</b></p><ul style="columns:2;gap:16px;padding-left:20px;margin:6px 0">{cam_rows}</ul>'
           + (f'<p style="margin-top:10px"><b>빌트인 캠 2</b>는 무선(OTA)으로 시동을 켤 때 자동 업데이트돼요. {E(b["conn"])}에 가입해야 하고, 내비를 USB로 수동 업데이트하면 빌트인 캠 2도 함께 업데이트돼요.</p>'
              f'<ul style="columns:2;gap:16px;padding-left:20px;margin:6px 0">' + ''.join(f'<li>{E(x)}</li>' for x in b['cam2']) + '</ul>' if b['cam2'] else '')
           + '</section>')
    ota = ('<section class="card"><h2>무선 업데이트(OTA)는 언제 되나요?</h2>'
           f'<p>{E(b["conn"])} 적용 차량이고 서비스에 가입했다면, 새 업데이트가 있을 때 <b>시동을 걸면 자동으로</b> 업데이트돼요. '
           '일부 오래된 차종은 무선 업데이트 지원이 끝났으니 공식 사이트에서 내 차를 확인하세요.</p></section>')
    links = (f'<section class="card"><h2>공식 사이트 바로가기</h2><p>파일은 아래 {E(b["full"])} 공식 업데이트 사이트에서만 받으세요.</p>'
             f'<a class="cu-go" href="{base}/updateGuide/{b["g"]["info"]}" target="_blank" rel="noopener nofollow">내비게이션 이용가이드</a>'
             f'<a class="cu-go s" href="{base}/updateNoticeList" target="_blank" rel="noopener nofollow">업데이트 소식(새 버전)</a>'
             f'<a class="cu-go s" href="{base}/updateGuide/{b["g"]["cam"]}" target="_blank" rel="noopener nofollow">빌트인 캠 가이드</a>'
             f'<a class="cu-go s" href="{base}/updateGuide/{b["g"]["ota"]}" target="_blank" rel="noopener nofollow">무선 업데이트 가이드</a>'
             f'<p class="cu-src" style="margin-top:10px">출처: {E(b["full"])} 차량 소프트웨어 업데이트 공식 사이트({E(b["host"])}) 이용가이드 · 확인 {CHECKED}. 그림은 이해를 돕기 위해 단순하게 그린 것이라 실제 화면과 다를 수 있어요.</p></section>')
    qa = [(f'{b["name"]} 내비 업데이트는 돈이 드나요?',
           f'공식 사이트와 Navigation Updater는 무료예요. 다만 지도 업데이트 무료 기간이 차량·내비마다 정해져 있어요. 예를 들어 현대 표준형 5세대 내비 사용 설명서에는 "차량 구매 후 8년까지 보장"이라고 적혀 있어요. 내 차 기간은 공식 사이트나 사용 설명서에서 확인하세요.'),
          ('USB가 인식이 안 돼요.', '32GB 이상, exFAT 형식인지 확인하세요. PC에서 USB가 이동식 디스크가 아니라 로컬 디스크로 보이면 복사가 안 될 수 있어요. 다른 USB로 바꿔 보는 게 가장 빨라요.'),
          ('업데이트는 얼마나 걸리나요?', '데이터 양에 따라 수십 분이 걸릴 수 있어요. 시간이 넉넉할 때, 배터리가 충분할 때 하세요.'),
          ('업데이트 중에 시동이 꺼지면 어떻게 되나요?', '전원이 끊기거나 USB·SD를 빼면 내비가 제대로 작동하지 않을 수 있어요. 꼭 끝날 때까지 기다리세요. 문제가 생기면 공식 고객센터나 서비스센터에 문의하세요.'),
          ('회원가입을 해야 하나요?', '아니요. 공식 사이트의 비회원 메뉴로도 업데이트 파일을 받을 수 있어요. 로그인하면 내 차 정보가 저장돼 다음부터 편해요.')]
    fq, fqld = faq(qa)
    other = ''.join(f'<li><a href="/drive/update/{x}.html"><b>{B[x]["name"]} 내비 업데이트</b><span>USB·SD 카드 준비부터 차에서 업데이트까지</span></a></li>' for x in B if x != k)
    main = (f'<header class="top hub">{cr}<h1>{E(b["name"])} 내비게이션 업데이트 방법</h1>'
            f'<p class="lead">{E(b["name"])} 순정 내비 지도와 소프트웨어를 최신으로 바꾸는 방법을 그림으로 쉽게 정리했어요. 차 한 번, PC 한 번이면 끝나요.</p>'
            f'<p class="cu-ans">{ans}</p></header>'
            f'<section class="card"><h2>그림으로 보는 업데이트 순서 (5단계)</h2>{steps}</section>'
            + stor + cam + ota + links + fq +
            '<section class="card rel"><h2>함께 보면 좋은 페이지</h2><ul class="tlist">' + other +
            '<li><a href="/drive/update/"><b>차 업데이트 모음</b><span>브랜드별 내비·블랙박스 업데이트</span></a></li>'
            '<li><a href="/drive/gas-station.html"><b>싼 주유소 지도</b><span>동네별 최저가 주유소</span></a></li></ul></section>')
    ld = [crld, fqld, {"@context": "https://schema.org", "@type": "HowTo", "name": f'{b["name"]} 내비게이션 업데이트 방법',
                       "supply": [{"@type": "HowToSupply", "name": "USB 메모리 또는 SD 카드 (32GB 이상, exFAT)"}],
                       "tool": [{"@type": "HowToTool", "name": "PC (Navigation Updater)"}],
                       "step": [{"@type": "HowToStep", "position": i + 1, "name": n} for i, n in enumerate(
                           ['PC에 Navigation Updater 설치', '내 차 맞춤 업데이트 조회에서 다운로드', 'USB·SD 카드에 복사', '차에서 설정 → 일반 → SW 정보/업데이트 → 업데이트', '끝날 때까지 전원 유지'])]}]
    write(path, title + ' | 홍라이프 도구', desc, main, ld)
    return path

# ── 2차: 방식이 다른 브랜드 (공식 안내 2026-11-21 확인) ─────────────
def pcwin(title, lines, buttons, hi, url='공식 업데이트 사이트', extra=''):
    t = f'<text x="44" y="62" font-size="13" font-weight="800" fill="#111">{E(title)}</text>'
    y = 80
    for ln in lines:
        t += f'<text x="44" y="{y}" font-size="10.5" fill="#495057">{E(ln)}</text>'
        y += 15
    bx = 44
    by = max(y + 4, 108)
    for i, b_ in enumerate(buttons):
        w = 12 * len(b_) + 22
        t += btn(bx, by, w, 28, b_, '#1D4ED8' if i == hi else '#E9ECEF', '#fff' if i == hi else '#333', 10.5)
        if i == hi:
            t += ring(bx, by, w, 28, '✓')
        bx += w + 10
    return pc(t + extra, url)


def carpop(title, sub, buttons, hi, note=''):
    t = ('<rect x="70" y="56" width="220" height="118" rx="12" fill="#0F172A" stroke="#475569"/>'
         f'<text x="180" y="86" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">{E(title)}</text>'
         f'<text x="180" y="106" text-anchor="middle" font-size="10.5" fill="#CBD5E1">{E(sub)}</text>')
    n = len(buttons)
    w = 72
    x0 = 180 - (n * w + (n - 1) * 12) / 2
    for i, b_ in enumerate(buttons):
        x = x0 + i * (w + 12)
        t += btn(x, 124, w, 30, b_, '#1D4ED8' if i == hi else '#334155', '#fff', 11)
        if i == hi:
            t += ring(x, 124, w, 30, '✓')
    if note:
        t += f'<text x="180" y="192" text-anchor="middle" font-size="10" fill="#FCD34D">{E(note)}</text>'
    return car(t)


def carusb(label, note):
    return car('<text x="180" y="70" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">' + E(label) + '</text>'
               '<g transform="translate(150 86)"><rect x="0" y="6" width="44" height="22" rx="4" fill="#94A3B8"/><rect x="44" y="11" width="12" height="12" rx="2" fill="#CBD5E1"/></g>'
               '<path d="M214 103 h40" stroke="#60A5FA" stroke-width="3" marker-end="url(#a)"/><defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#60A5FA"/></marker></defs>'
               f'<text x="180" y="150" text-anchor="middle" font-size="10.5" fill="#CBD5E1">{E(note)}</text>')


O = {
    'renault': {'name': '르노코리아', 'title': '르노코리아 내비게이션·openR link 업데이트 방법 (무선 + 지도 USB)',
                'desc': '르노코리아 openR link는 주행 중 무선으로 소프트웨어를 받고 시동을 끈 뒤 설치해요. openR link 9.3인치 세로형 지도는 TMAP 공식 페이지에서 받아 16GB 이상 FAT32 USB로 설치해요. 그림으로 쉽게 정리했어요.',
                'ans': '<b>openR link 소프트웨어</b>는 새 버전이 있으면 <b>주행 중 무선으로 자동 다운로드</b>되고, 시동을 끄면 설치할지 묻는 창이 떠요. <b>[예]</b>를 누르면 끝이에요. '
                       '<b>openR link 9.3인치(세로형) 지도</b>는 TMAP 공식 페이지에서 파일을 받아 <b>16GB 이상, FAT32</b> USB 맨 위 폴더에 넣고 차에 꽂으면 자동으로 업데이트돼요.',
                'parts': [('소프트웨어: 무선으로 자동 (openR link)', [
                    ('주행하면 저절로 받아져요', '새 소프트웨어가 있으면 차가 <b>주행 중에 알아서 내려받아요.</b> 받는 동안에도 내비와 멀티미디어는 그대로 쓸 수 있어요.',
                     carpop('업데이트 받는 중', '주행하면서 자동으로 받아요', [], -1, '받는 동안 내비 사용 가능'), '주행 시간이 짧으면 다음 주행 때 이어서 받아요.'),
                    ('시동 끄고 [예] 누르기', '다 받으면 <b>시동을 끌 때 설치할지 묻는 창</b>이 떠요. <b>[예]</b>를 누르면 운전자 없이 설치가 진행되고, 끝나면 시스템이 저절로 꺼져요.',
                     carpop('업데이트를 설치할까요?', '시동을 끈 상태로 설치돼요', ['아니요', '예'], 1))]),
                    ('지도: openR link 9.3인치 세로형 (USB)', [
                    ('TMAP 공식 페이지에서 지도 받기', 'TMAP 모빌리티 공식 페이지에서 <b>르노코리아 openR link 9.3" 지도 파일</b>을 받아 <b>압축을 풀어요.</b> 그러면 <b>TMAP 폴더</b>가 생겨요.',
                     pcwin('르노코리아 openR link 9.3"', ['세로형 전용 지도', '압축 파일 받기 → 압축 풀기'], ['다운로드'], 0, 'tmapmobility.com')),
                    ('USB 맨 위에 TMAP 폴더 넣기', '<b>16GB 이상 USB</b>를 <b>FAT32</b>로 포맷한 뒤, TMAP 폴더를 <b>USB 맨 위(루트)</b>에 복사해요.',
                     pcwin('USB 드라이브 (E:)', ['📁 TMAP  ← 여기에 그대로'], ['FAT32 포맷', '복사'], 1, '내 PC'), '8GB 이하 USB는 설치가 제대로 안 될 수 있다고 공식 안내에 적혀 있어요.'),
                    ('차에 꽂으면 자동 업데이트', '차의 USB 단자에 꽂으면 지도 업데이트가 <b>자동으로</b> 진행돼요.',
                     carusb('USB 꽂기', '꽂으면 지도 업데이트가 자동으로 시작돼요'))])],
                'links': [('르노코리아 openR link 무선 업데이트 안내', 'https://www.renault.co.kr/ko/service/easy_connect_sub02.jsp'),
                          ('openR link 9.3" 지도 업데이트 (TMAP 공식)', 'https://www.tmapmobility.com/support/auto/renault/easyconnect/update')],
                'src': '르노코리아 공식 사이트(renault.co.kr) connectivity 차량관리 안내, TMAP 모빌리티 르노코리아 openR link 9.3" 지도 업데이트 안내',
                'faq': [('openR link 업데이트는 직접 해야 하나요?', '아니요. 새 소프트웨어가 있으면 차가 주행 중 알아서 받고, 시동을 끌 때 설치할지 물어요. [예]만 누르면 돼요.'),
                        ('지도 업데이트 USB는 몇 GB가 필요해요?', 'TMAP 공식 안내는 16GB 이상을 권장하고, FAT32로 포맷하라고 해요. 8GB 이하는 설치가 안 될 수 있어요.'),
                        ('문의는 어디로 하나요?', '르노코리아 엔젤센터 080-300-3000이에요(공식 사이트 기재). 지도 파일 문의는 TMAP 앱 마이 → 고객센터 → 1:1 문의로 하라고 TMAP 공식 페이지에 안내돼 있어요.')]},
    'chevrolet': {'name': '쉐보레', 'title': '쉐보레 내비게이션 지도 업데이트 방법 (SD 카드 + 업데이터, 인증번호 백업)',
                  'desc': '쉐보레 말리부·트레일블레이저·트래버스·콜로라도·이쿼녹스·볼트 내비 지도는 SD 카드를 PC에 꽂아 공식 업데이터로 업데이트해요. 처음 한 번 인증번호 백업이 중요해요. 그림으로 쉽게 정리했어요.',
                  'ans': '쉐보레 내비 지도는 <b>차에서 SD 카드를 빼서 PC에 꽂고</b>, 쉐보레 공식 사이트의 <b>내비게이션 업데이터</b>로 최신 지도를 넣는 방식이에요. '
                         '파일은 <b>차대번호(VIN) 인증</b>이나 쉐보레 멤버스 로그인 후 받을 수 있고, <b>처음 한 번은 꼭 [인증 번호 백업]</b>을 눌러 두세요.',
                  'models': ['더 뉴 말리부 (2019년형~)', '트레일블레이저', '트래버스', '콜로라도', '더 뉴 카마로 (2019년형~)', '이쿼녹스 (2019년형~)', 'BOLT EUV', 'BOLT EV (2022년형~)'],
                  'parts': [('지도 업데이트 (SD 카드)', [
                      ('차에서 SD 카드 빼기', '시동을 끄고 화면이 <b>완전히 꺼진 뒤</b> SD 카드를 빼요. 차종에 따라 홈 화면 알림 아이콘의 <b>꺼내기</b> 메뉴를 먼저 눌러야 해요.',
                       carpop('SD 카드 꺼내기', '화면이 꺼진 뒤 빼세요', ['꺼내기'], 0), '키로 시동 거는 차는 키를 차에서 완전히 뺀 뒤 진행하세요.'),
                      ('업데이터와 지도 파일 받기', '쉐보레 공식 사이트에서 <b>차대번호 인증</b>(또는 쉐보레 멤버스 로그인 후 차량 등록)을 하고 <b>내비게이션 업데이터</b>와 <b>최신 지도 파일(zip)</b>을 받아요.',
                       pcwin('쉐보레 내비게이션 업데이트', ['차대번호(VIN) 인증', '업데이터 + 지도 파일(zip)'], ['업데이터', '지도 파일'], 1, 'chevrolet.co.kr')),
                      ('SD 카드 꽂고 인증번호 백업 (처음 1번)', 'SD 카드 옆 <b>잠금 스위치가 위로</b> 올라가 있는지 보고 PC에 꽂아요. 업데이터에서 <b>[인증 번호 백업]</b>을 눌러 SD 카드 고유 번호를 저장해 두세요.',
                       pcwin('내비게이션 업데이터', ['SD 카드 인식됨'], ['인증 번호 백업', '맵 업데이트'], 0, 'PC 프로그램'), 'SD 카드 슬롯이 없는 PC는 카드 리더기가 필요해요.'),
                      ('지도 업데이트 누르기', '받은 <b>zip 지도 파일을 고르고 업데이트</b>해요. 시간은 PC 성능에 따라 달라요.',
                       pcwin('내비게이션 업데이터', ['지도 파일: 최신.zip'], ['인증 번호 백업', '맵 업데이트'], 1, 'PC 프로그램'), '"인증 파일이 없다"는 경고가 나오면 백업 폴더를 고르거나 [최근 사용된 인증파일로 복구]를 누르세요. 오류가 계속되면 SD 카드를 포맷한 뒤 [수동 업데이트]를 쓰라고 공식 안내에 있어요.'),
                      ('안전하게 빼고 차에 꽂기', '윈도우에서 <b>하드웨어 안전하게 제거</b> 후 SD 카드를 빼요. <b>시동을 끈 상태</b>에서 차에 꽂고, 시동을 걸어 내비가 잘 켜지는지 확인해요.',
                       carusb('SD 카드 꽂기', '시동 끈 상태에서 꽂고 → 시동 켜서 확인'))])],
                  'links': [('쉐보레 내비게이션 업데이트 (적용 차종·다운로드)', 'https://www.chevrolet.co.kr/telenav/navigation-update'),
                            ('쉐보레 내비게이션 업데이트 공지사항', 'https://www.chevrolet.co.kr/telenav/notice')],
                  'src': '쉐보레 공식 사이트(chevrolet.co.kr) 내비게이션 업데이트 — 적용 차종 및 업데이트 안내',
                  'faq': [('인증번호 백업은 왜 해요?', 'SD 카드에는 고유 인증 정보가 있어요. 처음 업데이트할 때 [인증 번호 백업]을 해 두면, 나중에 인증 파일 오류가 나도 백업 폴더로 복구할 수 있어요.'),
                          ('내 차가 대상인지 어떻게 알아요?', '공식 안내의 적용 차종은 더 뉴 말리부(2019년형~), 트레일블레이저, 트래버스, 콜로라도, 더 뉴 카마로(2019년형~), 이쿼녹스(2019년형~), BOLT EUV, BOLT EV(2022년형~)예요.'),
                          ('SD 카드를 그냥 빼도 되나요?', '아니요. 시동을 끄고 화면이 완전히 꺼진 뒤 빼야 해요. 차종에 따라 알림 아이콘의 꺼내기 메뉴를 먼저 눌러야 해요.')]},
    'kgm': {'name': 'KG모빌리티(KGM)', 'title': 'KGM(쌍용) 내비게이션 업데이트 방법 — 차종별 공식 업데이트 사이트 정리',
            'desc': 'KG모빌리티(옛 쌍용) 토레스·액티언·무쏘·코란도·렉스턴·티볼리 순정 내비 업데이트는 차종에 따라 아이나비·지니 등 공식 업데이트 사이트가 달라요. 내 차에 맞는 곳을 쉽게 찾게 정리했어요.',
            'ans': 'KGM 순정 내비는 <b>내 차가 커넥티드카 서비스 적용 모델인지</b>에 따라 업데이트하는 곳이 달라요. KGM 공식 사이트 S/W 업데이트 메뉴가 연결하는 곳은 '
                   '<b>커넥티드카 적용 모델 → 아이나비 업그레이드</b>, <b>미적용 모델 → 지니(현대오토에버) 업데이트</b>예요. 체어맨 W는 업데이트 서비스가 끝났어요.',
            'table': [('커넥티드카 적용', '액티언/토레스 하이브리드, 액티언(신형), 토레스/EVX, 무쏘 스포츠/칸, 코란도/EV/이모션, 렉스턴(G4/올뉴/뉴아레나), 티볼리', '아이나비 업그레이드 (아이나비 매니저)', 'https://www.inavi.com/upgrades/autosmartupgrade/'),
                      ('커넥티드카 미적용', '체어맨H, 코란도, 렉스턴(W/G4/올뉴), 티볼리, 렉스턴스포츠/칸 (체어맨W 제외)', '지니(GINI) 업데이트 — 현대오토에버', 'https://update.hyundai-autoever.com/Gproduct/'),
                      ('체어맨 W', '업데이트 서비스 종료 (마지막 버전 2022.11)', '—', ''),
                      ('체어맨 W 카이져', '업데이트 서비스 종료 (마지막 버전 2022.12.21)', '—', '')],
            'parts': [('커넥티드카 적용 모델: 아이나비로 업데이트', [
                ('아이나비 매니저 설치·회원가입', 'PC에 <b>아이나비 매니저</b>를 설치하고 <b>아이나비 회원가입</b>을 해요. 회원가입 후에 업그레이드를 할 수 있어요.',
                 pcwin('아이나비 매니저', ['회원가입 후 업그레이드 가능'], ['다운로드 받기'], 0, 'inavi.com')),
                ('메모리카드를 PC에 꽂기', '카드 리더기로 내비 <b>메모리카드를 PC에 꽂으면</b> 오토스마트 업그레이드가 <b>자동 실행</b>되고 매니저에 접속돼요. 매니저가 없으면 자동으로 설치돼요.',
                 pcwin('오토스마트 업그레이드', ['메모리카드 인식', '매니저 자동 실행'], ['다음'], 0, 'PC 프로그램')),
                ('원클릭 업그레이드', '<b>[최신지도 원클릭 업그레이드]</b>를 누르면 지도와 펌웨어가 함께 설치돼요. 메모리카드 용량은 자동으로 인식해요.',
                 pcwin('아이나비 매니저', ['최신 지도 + 펌웨어 자동 설치'], ['원클릭 업그레이드'], 0, 'PC 프로그램'))])],
            'links': [('KGM 공식 S/W 업데이트 안내', 'https://www.kg-mobility.com/sr/update-download/software-update'),
                      ('아이나비 내비게이션 업그레이드', 'https://www.inavi.com/upgrades/autosmartupgrade/'),
                      ('지니(GINI) 업데이트 — 현대오토에버', 'https://update.hyundai-autoever.com/Gproduct/')],
            'src': 'KGM 공식 사이트(kg-mobility.com) 고객 서비스 → 차량 운영 지원 → S/W 업데이트, 아이나비 공식 내비게이션 업그레이드 안내',
            'faq': [('토레스 내비 업데이트는 어디서 해요?', 'KGM 공식 사이트 기준 토레스/EVX는 커넥티드카 서비스 적용 모델이라 아이나비 업그레이드로 연결돼요.'),
                    ('체어맨 W도 업데이트되나요?', '아니요. KGM 공식 안내에 따르면 체어맨 W(마지막 2022.11)와 체어맨 W 카이져(마지막 2022.12.21)는 내비 업데이트 서비스가 끝났어요.'),
                    ('KGM 고객센터 번호는요?', 'KGM 공식 사이트에 적힌 고객센터는 080-500-5582예요.')]},
    'inavi': {'name': '아이나비', 'title': '아이나비 내비게이션 지도 업그레이드 방법 (아이나비 매니저 원클릭)',
              'desc': '아이나비 내비 지도 업그레이드는 메모리카드를 PC에 꽂고 아이나비 매니저로 원클릭 업그레이드하면 돼요. 회원가입, 제품등록, 순서를 그림으로 쉽게 정리했어요.',
              'ans': '아이나비 내비는 <b>메모리카드를 PC에 꽂고</b> <b>아이나비 매니저</b>에서 <b>[최신지도 원클릭 업그레이드]</b>를 누르면 지도와 펌웨어가 함께 최신으로 바뀌어요. <b>아이나비 회원가입</b>이 먼저 필요해요.',
              'parts': [('지도 업그레이드 4단계', [
                  ('아이나비 매니저 설치·회원가입', '아이나비 공식 사이트에서 <b>아이나비 매니저</b>를 받아 설치하고 회원가입해요.',
                   pcwin('아이나비 매니저', ['회원가입 후 업그레이드 가능'], ['다운로드 받기'], 0, 'inavi.com')),
                  ('카드 리더기로 메모리카드 꽂기', '내비에서 뺀 <b>메모리카드를 카드 리더기로 PC에 꽂아요.</b> 메모리카드에 오토스마트 업그레이드 파일이 있으면 자동 실행돼요.',
                   pcwin('오토스마트 업그레이드', ['메모리카드 인식됨'], ['다음'], 0, 'PC 프로그램'), '자동 실행 파일이 없으면 아이나비 매니저를 직접 실행하면 돼요.'),
                  ('매니저 접속', '매니저가 없으면 자동으로 설치되고 접속돼요.',
                   pcwin('아이나비 매니저', ['나의 제품 확인'], ['로그인'], 0, 'PC 프로그램')),
                  ('원클릭 업그레이드', '<b>[최신지도 원클릭 업그레이드]</b>를 누르면 백업 → 다운로드 → 설치 → 데이터 복사까지 자동으로 해요. 메모리카드에 있던 데이터는 그대로 두고 최신 지도를 넣어줘요.',
                   pcwin('아이나비 매니저', ['최신 지도 + 펌웨어 자동 설치'], ['원클릭 업그레이드'], 0, 'PC 프로그램'))])],
              'links': [('아이나비 내비게이션 업그레이드 안내', 'https://www.inavi.com/upgrades/autosmartupgrade/')],
              'src': '아이나비 공식 사이트(inavi.com) 업그레이드 센터 — 내비게이션 업그레이드 안내',
              'faq': [('회원가입을 꼭 해야 하나요?', '네. 아이나비 공식 안내에 "회원가입 후 업그레이드를 진행할 수 있다"고 적혀 있어요.'),
                      ('메모리카드 안의 데이터가 지워지나요?', '공식 안내에는 원클릭 업그레이드가 "SD 메모리에 있던 데이터는 그대로" 최신 지도를 설치해 준다고 적혀 있어요. 그래도 중요한 파일은 미리 따로 복사해 두세요.'),
                      ('펌웨어도 따로 해야 하나요?', '원클릭 업그레이드로 지도를 설치하면 최신 펌웨어도 자동으로 설치된다고 공식 안내에 있어요.')]},
    'tesla': {'name': '테슬라', 'title': '테슬라 소프트웨어 업데이트 방법 (와이파이 무선 업데이트·예약·자동 설치)',
              'desc': '테슬라 모델 3·Y·S·X 소프트웨어 업데이트는 와이파이로 무선(OTA) 진행돼요. 컨트롤 → 소프트웨어에서 확인·예약·자동 설치하는 방법과 업데이트 중 주의할 점을 그림으로 쉽게 정리했어요.',
              'ans': '테슬라는 PC로 받는 드라이버나 USB 업데이트가 없고, <b>와이파이로 차가 직접 받는 무선 업데이트</b>예요. 터치스크린 <b>컨트롤 → 소프트웨어</b>에서 확인하고 <b>지금 설치</b>하거나 <b>예약</b>하면 돼요. 설치 중에는 <b>운전할 수 없고</b>, 시작하면 <b>취소·되돌리기가 안 돼요</b>.',
              'parts': [('업데이트 받는 순서', [
                  ('차를 와이파이에 연결', '업데이트는 <b>와이파이로 무선 배포</b>돼요. 집이나 회사 와이파이에 연결해 두세요. 신호 막대가 <b>3개 이상</b>이면 가장 빠르고 안정적이에요(테슬라 안내).',
                   carpop('Wi-Fi', '신호 막대 3개 이상 권장', ['연결'], 0)),
                  ('알림이 뜨면 지금 설치 또는 예약', '업데이트가 있으면 터치스크린에 알림이 떠요. 바로 설치하거나, <b>노란색 시계 아이콘</b>을 눌러 원하는 시간으로 <b>예약</b>할 수 있어요. Tesla 앱 첫 화면에도 설치할 수 있는 업데이트가 보여요.',
                   carpop('소프트웨어 업데이트', '지금 설치하거나 예약하세요', ['지금 설치', '예약'], 0)),
                  ('컨트롤 → 소프트웨어에서 확인·설정', '<b>컨트롤 → 소프트웨어</b>에서 업데이트가 있는지 보고, <b>업데이트 자동 설치</b>를 켜면 밤에 자동으로 설치돼요. <b>소프트웨어 업데이트 설정</b>에서 <b>표준</b> 또는 <b>우선 업데이트</b>를 고를 수 있어요.',
                   carpop('컨트롤 › 소프트웨어', '소프트웨어 업데이트 설정', ['표준', '우선'], 0, '우선 업데이트는 2019.16 이상')),
                  ('설치 중에는 주차 상태로 기다리기', '설치하는 동안에는 <b>운전할 수 없고</b>, 충전 중이면 설치가 끝날 때까지 <b>충전이 멈춰요</b>. 내려받는 중에 기어를 P에서 바꾸면 와이파이가 끊겨 다운로드가 멈출 수 있어요. 일부 업데이트는 <b>몇 시간</b> 걸려요.',
                   carpop('업데이트 설치 중', '주차(P) 상태로 기다려 주세요', ['확인'], 0, '설치 시작 후에는 취소 불가'))])],
              'links': [('테슬라 소프트웨어 업데이트 안내 (공식)', 'https://www.tesla.com/ko_kr/support/software-updates')],
              'src': '테슬라 공식 지원 \'소프트웨어 업데이트\'(tesla.com/ko_kr/support/software-updates)',
              'faq': [('테슬라 드라이버를 PC로 받아야 하나요?', '아니요. 테슬라 차량 소프트웨어는 와이파이로 차가 직접 받는 무선 업데이트예요. PC 프로그램이나 USB로 설치하는 방식이 아니에요.'),
                      ('왜 내 차만 업데이트가 안 와요?', '테슬라 안내에 따르면 업데이트는 정기적으로 나오지만 모든 차가 동시에 받지 않고, 따로 요청해서 받을 수도 없어요. 와이파이 연결을 유지하고 기다리면 돼요.'),
                      ('업데이트가 3시간 넘게 안 끝나요.', '테슬라 안내: 시작 후 3시간이 지나도 앱에 완료 알림이 없으면 스티어링 휠의 두 스크롤 버튼을 약 20초 길게 눌러 터치스크린을 다시 시작하세요. 그래도 안 되면 서비스를 예약하세요.'),
                      ('업데이트를 이전 버전으로 되돌릴 수 있나요?', '아니요. 설치가 시작되면 취소할 수 없고 이전 버전으로 되돌릴 수도 없어요(테슬라 안내).')]},
}


def other_page(k):
    o = O[k]
    path = f'/drive/update/{k}.html'
    cr, crld = crumb([('차 업데이트 모음', '/drive/update/'), (f'{o["name"]} 업데이트', '')])
    body = ''
    n = 0
    for sec, steps_ in o['parts']:
        inner = ''
        for st in steps_:
            n += 1
            inner += step(n, st[0], st[1], st[2], st[3] if len(st) > 3 else '')
        body += f'<section class="card"><h2>{E(sec)}</h2>{inner}</section>'
    extra = ''
    if 'models' in o:
        extra += '<section class="card"><h2>적용 차종 (공식 안내)</h2><ul style="columns:2;gap:16px;padding-left:20px;margin:6px 0">' + ''.join(f'<li>{E(x)}</li>' for x in o['models']) + '</ul></section>'
    if 'table' in o:
        extra += ('<section class="card"><h2>내 차는 어디서 업데이트하나요?</h2><div style="overflow-x:auto"><table class="cu-t"><thead><tr><th>구분</th><th>차종</th><th>업데이트하는 곳</th></tr></thead><tbody>'
                  + ''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b_)}</td><td>' + (f'<a href="{u}" target="_blank" rel="noopener nofollow">{E(c)}</a>' if u else E(c)) + '</td></tr>' for a, b_, c, u in o['table'])
                  + '</tbody></table></div><p class="cu-src">KGM 공식 사이트 S/W 업데이트 메뉴가 연결하는 곳 기준이에요.</p></section>')
    links = ('<section class="card"><h2>공식 사이트 바로가기</h2>' + ''.join(
        f'<a class="cu-go{"" if i == 0 else " s"}" href="{u}" target="_blank" rel="noopener nofollow">{E(t)}</a>' for i, (t, u) in enumerate(o['links']))
        + f'<p class="cu-src" style="margin-top:10px">출처: {E(o["src"])} · 확인 {CHECKED}. 그림은 이해를 돕기 위해 단순하게 그린 것이라 실제 화면과 다를 수 있어요.</p></section>')
    fq, fqld = faq(o['faq'])
    rel = ''.join(f'<li><a href="/drive/update/{x}.html"><b>{nm} 업데이트</b><span>그림으로 쉽게</span></a></li>'
                  for x, nm in [(x, B[x]['name']) for x in B] + [(x, O[x]['name']) for x in O] if x != k)
    main = (f'<header class="top hub">{cr}<h1>{E(o["title"].split(" (")[0].split(" —")[0])}</h1>'
            f'<p class="lead">{E(o["name"])} 내비·소프트웨어를 최신으로 바꾸는 방법을 그림으로 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{o["ans"]}</p></header>' + extra + body + links + fq +
            f'<section class="card rel"><h2>다른 브랜드</h2><ul class="tlist">{rel}<li><a href="/drive/update/"><b>차 업데이트 모음</b><span>브랜드별 전체</span></a></li></ul></section>')
    write(path, o['title'] + ' | 홍라이프 도구', o['desc'], main, [crld, fqld])
    return path


def hub():
    path = '/drive/update/'
    title = '자동차 내비·소프트웨어 업데이트 모음 (현대·기아·제네시스·르노코리아·쉐보레·KGM·테슬라·아이나비) — 그림으로 쉽게'
    desc = '현대·기아·제네시스·르노코리아·쉐보레·KG모빌리티 순정 내비와 아이나비 지도 업데이트 방법을 그림으로 쉽게 정리했어요. 공식 업데이트 사이트로 바로 연결돼요.'
    cr, crld = crumb([('차 업데이트 모음', '')])
    cards = ''.join(f'<li><a href="/drive/update/{k}.html"><b>{b["name"]}</b><span>내비 지도·SW 업데이트 · 빌트인 캠</span></a></li>' for k, b in B.items()) + ''.join(
        f'<li><a href="/drive/update/{k}.html"><b>{o["name"]}</b><span>{"애프터마켓 내비 지도" if k == "inavi" else ("와이파이 무선 업데이트" if k == "tesla" else "지도·SW 업데이트")}</span></a></li>' for k, o in O.items())
    qa = [('차 내비 업데이트는 왜 해야 하나요?', '새로 생긴 도로와 바뀐 길, 과속 단속 정보가 반영되고 내비 오류도 고쳐져요. 오래 안 하면 없는 길로 안내하거나 새 도로를 모를 수 있어요.'),
          ('무선으로 자동 업데이트되는 차도 있나요?', '현대 블루링크, 기아 커넥트, 제네시스 커넥티드 서비스에 가입한 차는 무선(OTA)으로 자동 업데이트돼요. 가입하지 않았다면 PC로 USB·SD 카드에 받아서 하면 돼요.'),
          ('브랜드마다 방법이 다른가요?', '네. 현대·기아·제네시스는 PC 프로그램(Navigation Updater)과 USB·SD, 르노코리아는 무선 + 지도 USB, 쉐보레는 SD 카드 + 업데이터, KGM은 차종에 따라 아이나비 또는 지니 업데이트예요. 수입차와 블랙박스도 차례로 추가할게요.')]
    fq, fqld = faq(qa)
    main = (f'<header class="top hub">{cr}<h1>차 내비·블랙박스 업데이트 모음</h1>'
            '<p class="lead">내 차 내비 지도와 블랙박스를 최신으로 바꾸는 방법을 브랜드별로 그림과 함께 쉽게 정리했어요. 파일은 꼭 제조사 공식 사이트에서 받으세요.</p>'
            '<p class="cu-ans">브랜드마다 방법이 조금씩 달라요. 가장 많은 현대·기아·제네시스는 <b>① PC에 Navigation Updater 설치 → ② 내 차 고르고 다운로드 → ③ USB·SD 카드에 복사 → ④ 차에서 설정 → 일반 → SW 정보/업데이트 → 업데이트</b>. 커넥티드 서비스에 가입한 차는 무선으로 자동 업데이트돼요.</p></header>'
            f'<section class="card"><h2>브랜드 고르기</h2><ul class="cu-brand">{cards}</ul></section>'
            f'<section class="card"><h2>한눈에 보는 순서</h2>{step(1, "PC에 프로그램 깔기", "브랜드 공식 업데이트 사이트에서 Navigation Updater를 받아요.", S1("공식 업데이트 사이트"))}'
            f'{step(4, "차에서 업데이트 누르기", "USB·SD를 꽂고 설정 → 일반 → SW 정보/업데이트 → 업데이트.", S4())}</section>'
            + fq + '<section class="card rel"><h2>함께 보면 좋은 도구</h2><ul class="tlist">'
            '<li><a href="/drive/"><b>자동차·지도 도구 모음</b><span>주유소·충전소·주차장·휴게소</span></a></li>'
            '<li><a href="/life/route-navi.html"><b>경유지 많은 노선 내비</b><span>정류장 30곳 넘어도 순서대로 길안내</span></a></li></ul></section>')
    write(path, title + ' | 홍라이프 도구', desc, main, [crld, fqld])
    return path


if __name__ == '__main__':
    made = [hub()] + [brand_page(k) for k in B] + [other_page(k) for k in O]
    print('\n'.join(made))
