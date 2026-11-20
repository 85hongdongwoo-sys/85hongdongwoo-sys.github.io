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
       '.cu-t th{color:var(--muted,#5B6B82);font-weight:700;white-space:nowrap}'
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


def hub():
    path = '/drive/update/'
    title = '자동차 내비·블랙박스 업데이트 모음 (현대·기아·제네시스) — 그림으로 쉽게'
    desc = '현대·기아·제네시스 순정 내비게이션 지도 업데이트와 빌트인 캠 업데이트 방법을 그림으로 쉽게 정리했어요. 공식 업데이트 사이트로 바로 연결돼요.'
    cr, crld = crumb([('차 업데이트 모음', '')])
    cards = ''.join(f'<li><a href="/drive/update/{k}.html"><b>{b["name"]}</b><span>내비 지도·SW 업데이트 · 빌트인 캠</span></a></li>' for k, b in B.items())
    qa = [('차 내비 업데이트는 왜 해야 하나요?', '새로 생긴 도로와 바뀐 길, 과속 단속 정보가 반영되고 내비 오류도 고쳐져요. 오래 안 하면 없는 길로 안내하거나 새 도로를 모를 수 있어요.'),
          ('무선으로 자동 업데이트되는 차도 있나요?', '현대 블루링크, 기아 커넥트, 제네시스 커넥티드 서비스에 가입한 차는 무선(OTA)으로 자동 업데이트돼요. 가입하지 않았다면 PC로 USB·SD 카드에 받아서 하면 돼요.'),
          ('다른 브랜드도 있나요?', '르노코리아, 쉐보레, KG모빌리티, 수입차와 블랙박스 업데이트를 공식 안내를 확인하는 대로 차례로 추가할게요.')]
    fq, fqld = faq(qa)
    main = (f'<header class="top hub">{cr}<h1>차 내비·블랙박스 업데이트 모음</h1>'
            '<p class="lead">내 차 내비 지도와 블랙박스를 최신으로 바꾸는 방법을 브랜드별로 그림과 함께 쉽게 정리했어요. 파일은 꼭 제조사 공식 사이트에서 받으세요.</p>'
            '<p class="cu-ans">현대·기아·제네시스는 같은 방식이에요. <b>① PC에 Navigation Updater 설치 → ② 내 차 고르고 다운로드 → ③ USB·SD 카드에 복사 → ④ 차에서 설정 → 일반 → SW 정보/업데이트 → 업데이트</b>. 커넥티드 서비스에 가입한 차는 무선으로 자동 업데이트돼요.</p></header>'
            f'<section class="card"><h2>브랜드 고르기</h2><ul class="cu-brand">{cards}</ul></section>'
            f'<section class="card"><h2>한눈에 보는 순서</h2>{step(1, "PC에 프로그램 깔기", "브랜드 공식 업데이트 사이트에서 Navigation Updater를 받아요.", S1("공식 업데이트 사이트"))}'
            f'{step(4, "차에서 업데이트 누르기", "USB·SD를 꽂고 설정 → 일반 → SW 정보/업데이트 → 업데이트.", S4())}</section>'
            + fq + '<section class="card rel"><h2>함께 보면 좋은 도구</h2><ul class="tlist">'
            '<li><a href="/drive/"><b>자동차·지도 도구 모음</b><span>주유소·충전소·주차장·휴게소</span></a></li>'
            '<li><a href="/life/route-navi.html"><b>경유지 많은 노선 내비</b><span>정류장 30곳 넘어도 순서대로 길안내</span></a></li></ul></section>')
    write(path, title + ' | 홍라이프 도구', desc, main, [crld, fqld])
    return path


if __name__ == '__main__':
    made = [hub()] + [brand_page(k) for k in B]
    print('\n'.join(made))
