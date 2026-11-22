"""드라이버·프로그램 다운로드 모음 → overlay/driver/
회사 1곳 = 페이지 1개. 파일은 올리지 않고 제조사 공식 다운로드 페이지로만 연결한다.
2026-11-22 공식 안내로 확인한 내용만 쓴다:
- HP: HP 고객지원 문서 'HP홈페이지에서 프린터 소프트웨어를 다운로드하는 방법'
- 신도리코: support.sindoh.com FAQ '프린터 드라이버는 어떻게 다운 받나요?', '프린터 드라이버(USB) -빠른설치-'
- Windows: Microsoft 지원 '최신 프린터 드라이버 다운로드 및 설치'
- 삼성 프린터 → HP: samsung.com 'Support for Samsung brand printers is now handled by HP'
단계 그림은 직접 그린 SVG(회사 로고 없음)."""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu  # 공통 틀·그림 도구 재사용 (pc, btn, ring, step, faq, head)

E, pc, btn, ring = cu.E, cu.pc, cu.btn, cu.ring
ROOT, SITE = cu.ROOT, cu.SITE
CHECKED = '2026년 11월 22일'

CSS = ('<style id="dr-css">'
       '.dl3d{display:inline-flex;align-items:center;gap:12px;margin:8px 8px 4px 0;padding:13px 20px 13px 14px;border-radius:16px;'
       'background:linear-gradient(180deg,#4F8DF7 0%,#2563EB 55%,#1D4ED8 100%);border:1px solid #1E40AF;color:#fff!important;text-decoration:none;'
       'box-shadow:0 6px 0 #1E3A8A,0 12px 22px rgba(29,78,216,.32),inset 0 1px 0 rgba(255,255,255,.35);transform:translateY(0);transition:transform .08s,box-shadow .08s;'
       'position:relative;max-width:100%;box-sizing:border-box}'
       '.dl3d:hover{filter:brightness(1.04)}.dl3d:active{transform:translateY(5px);box-shadow:0 1px 0 #1E3A8A,0 4px 10px rgba(29,78,216,.3),inset 0 1px 0 rgba(255,255,255,.3)}'
       '.dl3d .ic{flex:none;width:40px;height:40px;border-radius:12px;background:rgba(255,255,255,.18);box-shadow:inset 0 -2px 0 rgba(0,0,0,.15);display:grid;place-items:center}'
       '.dl3d .ic svg{width:22px;height:22px}.dl3d .tx{display:flex;flex-direction:column;line-height:1.25;min-width:0}'
       '.dl3d b{font-size:17px;font-weight:800;word-break:keep-all}.dl3d small{font-size:12.5px;opacity:.88;font-weight:600;word-break:keep-all}'
       '.dl3d.s{background:linear-gradient(180deg,#FFFFFF,#EEF4FF);border-color:#BFD3FB;color:#1D4ED8!important;box-shadow:0 5px 0 #BFD3FB,0 10px 18px rgba(29,78,216,.12)}'
       '.dl3d.s .ic{background:#E0EBFF}.dl3d.s:active{box-shadow:0 1px 0 #BFD3FB}'
       '.dr-sec{scroll-margin-top:70px}.dr-toc{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0;padding:0;list-style:none}'
       '.dr-toc a{display:inline-block;padding:7px 12px;border-radius:999px;background:#EEF4FF;color:#1D4ED8;font-weight:700;font-size:14px;text-decoration:none}'
       '.dr-m{width:100%;border-collapse:collapse;font-size:14.5px}.dr-m th,.dr-m td{padding:9px 8px;border-bottom:1px solid var(--line-s,#E3E7EE);text-align:left;vertical-align:middle;word-break:keep-all}'
       '.dr-m th{color:var(--muted,#5B6B82);font-weight:700;font-size:13px}.dr-m td:first-child{font-weight:800;white-space:nowrap}'
       '.dr-m a.mini{display:inline-block;padding:6px 11px;border-radius:10px;background:linear-gradient(#3B82F6,#1D4ED8);color:#fff!important;font-weight:800;font-size:13px;text-decoration:none;box-shadow:0 3px 0 #1E3A8A;white-space:nowrap}'
       '.dr-m a.mini:active{transform:translateY(2px);box-shadow:0 1px 0 #1E3A8A}'
       '.dr-q{display:flex;gap:8px;margin:12px 0 4px}.dr-q input{flex:1;min-width:0;padding:12px 14px;border:1.5px solid #BFD3FB;border-radius:12px;font-size:16px}'
       '.dr-q button{flex:none;padding:0 16px;border:0;border-radius:12px;background:#1D4ED8;color:#fff;font-weight:800;font-size:15px}'
       '#dr-res{list-style:none;margin:6px 0 0;padding:0}#dr-res li{padding:8px 2px;border-bottom:1px dashed var(--line-s,#E3E7EE)}#dr-res a{font-weight:700}'
       '.dr-warn{background:#FFF6E5;border:1px solid #FFE0A3;border-radius:12px;padding:12px 14px;line-height:1.7;font-size:15px}'
       '.dr-co{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;list-style:none;margin:0;padding:0}'
       '.dr-co a{display:block;padding:14px;border:1px solid var(--line-s,#E3E7EE);border-radius:14px;text-decoration:none;color:inherit;background:#fff;box-shadow:0 3px 0 #E3E7EE}'
       '.dr-co a b{display:block;font-size:17px;color:var(--head,#111)}.dr-co a span{font-size:13px;color:var(--muted,#5B6B82);word-break:keep-all}.dr-co a em{font-style:normal;font-size:12px;color:#1D4ED8;font-weight:700}'
       '@media(max-width:640px){.dl3d{width:100%}.dr-m{font-size:13.5px}}'
       '</style>')

DLICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>'


def dl(url, title, sub, sec=False):
    return (f'<a class="dl3d{" s" if sec else ""}" href="{E(url)}" target="_blank" rel="noopener nofollow">'
            f'<span class="ic">{DLICON}</span><span class="tx"><b>{E(title)}</b><small>{E(sub)}</small></span></a>')


# ── 단계 그림 ──────────────────────────────────────────────
def W_search(url, kind_label, field, submit, n=1):
    return pc(f'<text x="44" y="62" font-size="13" font-weight="800" fill="#111">소프트웨어 및 드라이버</text>'
              f'<rect x="44" y="74" width="100" height="26" rx="5" fill="#fff" stroke="#ADB5BD"/><text x="54" y="91" font-size="10.5" fill="#333">{E(kind_label)} ▾</text>'
              f'<rect x="44" y="110" width="176" height="28" rx="5" fill="#fff" stroke="#1D4ED8" stroke-width="1.5"/><text x="54" y="128" font-size="10.5" fill="#868E96">{E(field)}</text>'
              + btn(228, 110, 60, 28, submit) + ring(44, 110, 244, 28, n), url)


def W_list(url, title, rows, hi, n=2):
    t = f'<text x="44" y="60" font-size="12.5" font-weight="800" fill="#111">{E(title)}</text>'
    y = 70
    for i, (a, b) in enumerate(rows):
        t += (f'<rect x="44" y="{y}" width="244" height="30" rx="5" fill="{"#EEF4FF" if i == hi else "#F8F9FA"}" stroke="#DEE2E6"/>'
              f'<text x="52" y="{y + 19}" font-size="10" fill="#333">{E(a)}</text>')
        if b:
            t += btn(226, y + 5, 56, 20, b, '#1D4ED8' if i == hi else '#ADB5BD', '#fff', 9.5)
            if i == hi:
                t += ring(226, y + 5, 56, 20, n)
        y += 36
    return pc(t, url)


def W_downloads(fname, n=3):
    return pc('<rect x="150" y="44" width="170" height="104" rx="8" fill="#fff" stroke="#ADB5BD"/>'
              '<text x="162" y="64" font-size="11" font-weight="800" fill="#111">다운로드 (Ctrl+J)</text>'
              '<rect x="160" y="74" width="150" height="40" rx="6" fill="#F8F9FA" stroke="#DEE2E6"/>'
              f'<text x="168" y="91" font-size="9.5" fill="#333">{E(fname)}</text><text x="168" y="105" font-size="8.5" fill="#868E96">완료</text>'
              + btn(250, 120, 60, 22, '파일 열기', '#1D4ED8', '#fff', 9.5) + ring(250, 120, 60, 22, n)
              + '<text x="44" y="80" font-size="10" fill="#495057">받은 파일은</text><text x="44" y="96" font-size="10" fill="#495057">다운로드 폴더에</text><text x="44" y="112" font-size="10" fill="#495057">저장돼요</text>',
              '브라우저 다운로드 목록')


def W_uac(app, n=4):
    return pc('<rect x="30" y="18" width="300" height="176" rx="6" fill="#E7EEF8"/>'
              '<rect x="62" y="40" width="236" height="134" rx="8" fill="#fff" stroke="#ADB5BD"/>'
              '<text x="76" y="62" font-size="10" fill="#495057">사용자 계정 컨트롤</text>'
              '<text x="76" y="82" font-size="11" font-weight="800" fill="#111">이 앱이 디바이스를 변경할 수</text>'
              '<text x="76" y="98" font-size="11" font-weight="800" fill="#111">있도록 허용하시겠어요?</text>'
              f'<text x="76" y="118" font-size="9.5" fill="#868E96">{E(app)}</text>'
              + btn(150, 134, 64, 26, '예') + btn(222, 134, 64, 26, '아니요', '#E9ECEF', '#333') + ring(150, 134, 64, 26, n), '윈도우 확인 창')


def W_installer(title, lines, button, n=5):
    t = (f'<rect x="56" y="44" width="248" height="140" rx="8" fill="#fff" stroke="#ADB5BD"/>'
         f'<rect x="56" y="44" width="248" height="22" rx="8" fill="#334155"/><text x="66" y="59" font-size="10" fill="#fff" font-weight="700">{E(title)}</text>')
    y = 86
    for ln in lines:
        t += f'<text x="70" y="{y}" font-size="10.5" fill="#333">{E(ln)}</text>'
        y += 17
    return pc(t + btn(226, 148, 66, 26, button) + ring(226, 148, 66, 26, n), '설치 프로그램')


def W_testpage(n=6):
    return pc('<text x="44" y="60" font-size="11" fill="#868E96">설정 › Bluetooth 및 장치 ›</text>'
              '<text x="44" y="78" font-size="13" font-weight="800" fill="#111">프린터 및 스캐너</text>'
              '<rect x="44" y="88" width="244" height="30" rx="6" fill="#F8F9FA" stroke="#DEE2E6"/><text x="56" y="107" font-size="10.5" fill="#333">🖨 내 프린터 (설치한 이름)</text>'
              + btn(44, 128, 112, 28, '테스트 페이지 인쇄') + ring(44, 128, 112, 28, n)
              + '<text x="166" y="146" font-size="9.5" fill="#868E96">종이가 나오면 성공!</text>', '윈도우 설정')


def W_unzip(n=3):
    return pc('<rect x="44" y="52" width="120" height="70" rx="6" fill="#F8F9FA" stroke="#DEE2E6"/>'
              '<rect x="58" y="62" width="36" height="44" rx="4" fill="#FAB005"/><rect x="72" y="62" width="8" height="44" fill="#E67700"/>'
              '<text x="58" y="118" font-size="9" fill="#333">드라이버.zip</text>'
              '<rect x="150" y="70" width="140" height="96" rx="6" fill="#fff" stroke="#ADB5BD"/>'
              '<text x="162" y="90" font-size="10" fill="#333">열기</text>'
              '<rect x="154" y="98" width="132" height="22" rx="4" fill="#EEF4FF"/><text x="162" y="113" font-size="10" font-weight="800" fill="#1D4ED8">알아서 풀기</text>'
              '<text x="162" y="138" font-size="10" fill="#333">다른 이름으로 풀기…</text><text x="162" y="156" font-size="10" fill="#333">속성</text>'
              + ring(154, 98, 132, 22, n), '파일 탐색기 (마우스 오른쪽 클릭)')


def W_sindoh_tool(n=5):
    return pc('<rect x="50" y="42" width="260" height="146" rx="8" fill="#fff" stroke="#ADB5BD"/>'
              '<rect x="50" y="42" width="260" height="22" rx="8" fill="#334155"/><text x="60" y="57" font-size="10" fill="#fff" font-weight="700">Sindoh Easy 프린터 설치 툴</text>'
              '<text x="64" y="86" font-size="10.5" fill="#333">로컬 포트</text>'
              '<rect x="130" y="73" width="86" height="22" rx="4" fill="#fff" stroke="#1D4ED8" stroke-width="1.5"/><text x="140" y="88" font-size="10.5" font-weight="800" fill="#1D4ED8">USB ▾</text>'
              '<text x="222" y="88" font-size="9" fill="#868E96">(LPT1 → USB)</text>' + ring(130, 73, 86, 22, n)
              + '<text x="64" y="118" font-size="10" fill="#868E96">설치할 드라이버가 자동으로 선택돼요</text>'
              + btn(230, 150, 66, 26, '설치') + ring(230, 150, 66, 26, n + 1), '신도리코 설치 툴')


# ── 페이지 틀 ────────────────────────────────────────────
def write(path, title, desc, main, ld):
    out = os.path.join(ROOT, 'overlay', path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    h = cu.head(title, desc, SITE + path, ld).replace(cu.CSS, cu.CSS + CSS)
    open(out, 'w', encoding='utf-8').write(h + cu.BODY_TOP + '<main class="wrap wide">' + main + '</main>' + cu.FOOT)


def crumb(items):
    parts = ['<a href="/">홈</a>', '<a href="/driver/">드라이버</a>'] + [f'<a href="{u}">{E(n)}</a>' if u else E(n) for n, u in items]
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
        for i, (n, u) in enumerate([('홈', '/'), ('드라이버', '/driver/')] + [(n, u) for n, u in items if u])]}
    return '<p class="crumb">' + ' › '.join(parts) + '</p>', ld


def models_table(rows):
    return ('<div style="overflow-x:auto"><table class="dr-m"><thead><tr><th>모델</th><th>종류</th><th></th></tr></thead><tbody>'
            + ''.join(f'<tr id="m-{E(re.sub(r"[^A-Za-z0-9]", "", m))}"><td>{E(m)}</td><td>{E(k)}</td>'
                      f'<td><a class="mini" href="{E(u)}" target="_blank" rel="noopener nofollow">⬇ 다운로드</a></td></tr>' for m, k, u in rows)
            + '</tbody></table></div>')


def model_search(models):
    data = json.dumps([[m, '#m-' + re.sub(r'[^A-Za-z0-9]', '', m)] for m in models], ensure_ascii=False)
    return ('<form class="dr-q" onsubmit="return drQ()"><input id="dr-in" placeholder="모델명 입력 (예: D452)" autocomplete="off" oninput="drQ()" aria-label="모델명 검색">'
            '<button type="submit">찾기</button></form><ul id="dr-res"></ul>'
            f'<script>var DRM={data};function drQ(){{var q=document.getElementById("dr-in").value.replace(/\\s/g,"").toUpperCase(),r=document.getElementById("dr-res");'
            'if(!q){r.innerHTML="";return false}var h=DRM.filter(function(x){return x[0].replace(/\\s/g,"").toUpperCase().indexOf(q)>=0}).slice(0,8);'
            'r.innerHTML=h.length?h.map(function(x){return\'<li><a href="\'+x[1]+\'">\'+x[0]+\' 다운로드 줄로 가기 ›</a></li>\'}).join(""):"<li>이 페이지 표에 없는 모델이에요. 아래 순서대로 공식 사이트에서 모델명을 검색하세요.</li>";return false}</script>')


# ── HP (삼성 프린터 포함) ─────────────────────────────────
HP_DRV = 'https://support.hp.com/kr-ko/drivers'
HP_SETUP = 'https://support.hp.com/kr-ko/printer-setup'
HP_UPD = 'https://support.hp.com/kr-ko/drivers/hp-universal-print-driver-series-for-windows/4157320'


def hp():
    path = '/driver/hp.html'
    cr, crld = crumb([('HP 드라이버', '')])
    ans = ('HP 프린터 드라이버는 <b>HP 공식 \'소프트웨어 및 드라이버\'</b> 페이지에서 받아요. 제품 종류에서 <b>프린터</b>를 고르고 모델명을 입력한 뒤, '
           '<b>소프트웨어-유틸리티</b>에 있는 <b>제품 전용 통합 소프트웨어(인쇄 및 스캔 드라이버)</b>를 받아 실행하면 돼요. 회원가입이나 로그인은 필요 없어요. '
           '<b>삼성 프린터</b>도 지금은 HP가 지원해서 같은 곳에서 받아요.')
    steps = (cu.step(1, 'HP 공식 다운로드 페이지 열기', '아래 파란 <b>[HP 드라이버 받으러 가기]</b> 버튼을 누르면 HP 공식 \'소프트웨어 및 드라이버\' 페이지가 열려요.',
                     W_search('support.hp.com', '프린터', '모델명 입력 (예: 프린터 이름)', '제출'),
                     '제품 종류가 여러 개 보이면 <b>프린터</b>를 고르세요.')
             + cu.step(2, '모델명 넣고 [제출]', '프린터 이름(모델명)을 입력하고 <b>[제출]</b>을 눌러요. 결과에서 내 제품을 고르면 내 컴퓨터 운영체제(윈도우·맥)에 맞는 목록이 자동으로 나와요.',
                       W_list('support.hp.com', '내 제품 · 운영체제 자동 선택', [('운영체제: 자동 선택됨', '다른 OS'), ('소프트웨어-유틸리티', ''), ('제품 전용 통합 소프트웨어', '다운로드')], 2),
                       '다른 운영체제용이 필요하면 <b>[다른 OS 선택하기]</b>를 누르세요. 결과가 하나뿐이면 목록이 바로 나와요.')
             + cu.step(3, '받은 파일 열기', '다운로드가 끝나면 키보드 <b>Ctrl + J</b>를 눌러 다운로드 목록을 열고, 받은 파일을 눌러 실행해요.',
                       W_downloads('HP_설치파일.exe'), '파일은 보통 <b>다운로드</b> 폴더에 저장돼요.')
             + cu.step(4, '\'예\' 누르기', '윈도우가 "이 앱이 디바이스를 변경할 수 있도록 허용하시겠어요?"라고 물으면 <b>[예]</b>를 눌러요.',
                       W_uac('HP 프린터 소프트웨어'))
             + cu.step(5, '화면 안내대로 설치하기', '설치 프로그램이 묻는 대로 연결 방식(USB 선 또는 와이파이)을 고르고 <b>[다음]</b>을 눌러 가며 설치해요. 다시 시작하라고 하면 컴퓨터를 다시 시작해요.',
                       W_installer('HP 프린터 설치', ['연결 방식을 고르세요', '○ USB 케이블', '○ 무선(와이파이)'], '다음'),
                       'USB 선은 설치 프로그램이 "연결하세요"라고 할 때 꽂는 게 안전해요. 실제 화면은 모델마다 조금 달라요.')
             + cu.step(6, '테스트 페이지로 확인', '<b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b>에서 내 프린터를 누르고 <b>[테스트 페이지 인쇄]</b>를 눌러요. 종이가 나오면 끝이에요.',
                       W_testpage()))
    trouble = ('<section class="card dr-sec" id="trouble"><h2>안 될 때</h2><ul class="cu-chk">'
               '<li><b>검색해도 내 프린터가 안 나와요:</b> 오래전에 단종된 프린터는 검색에 안 나올 수 있어요. 이때는 윈도우에 들어 있는 기본 드라이버로 설치해 보세요(아래 \'윈도우 자동 설치\').</li>'
               '<li><b>HP Smart를 먼저 추천해요:</b> HP Smart 앱이 먼저 보일 수 있어요. 프린터의 모든 기능(스캔 포함)을 쓰려면 <b>제품 전용 통합 소프트웨어</b>를 받아 설치하세요.</li>'
               '<li><b>회사에서 여러 대를 쓰는 레이저 프린터:</b> 사무실 공용 프린터는 \'HP 범용 프린트 드라이버(Universal Print Driver)\'를 쓰기도 해요.</li>'
               '<li><b>와이파이 연결이 어려워요:</b> HP 공식 \'프린터 설정\' 안내(와이파이·유선·USB)를 따라 해 보세요.</li></ul>'
               + dl(HP_SETUP, 'HP 프린터 설정 안내', '와이파이·유선·USB 연결 방법 (HP 공식)', True)
               + dl(HP_UPD, 'HP 범용 프린트 드라이버', '사무실 공용 프린터용 (HP 공식)', True) + '</section>')
    samsung = ('<section class="card dr-sec" id="samsung"><h2>삼성 프린터 드라이버도 여기서</h2>'
               '<p>삼성전자는 이제 프린터를 만들거나 지원하지 않고, <b>삼성 프린터의 드라이버와 지원은 HP가 맡고 있어요</b>(삼성전자 공식 안내). '
               '그래서 삼성 프린터도 위와 같은 순서로 <b>HP 소프트웨어 및 드라이버</b> 페이지에서 모델명(예: SL-로 시작하는 이름)을 검색해 받으면 돼요.</p>'
               + dl(HP_DRV, '삼성 프린터 드라이버 받기', 'HP 공식 페이지에서 모델명 검색') + '</section>')
    qa = [('HP 드라이버는 무료인가요?', '네. HP 공식 사이트의 드라이버와 소프트웨어는 무료이고, 받을 때 회원가입이나 로그인도 필요 없어요.'),
          ('CD가 없어도 설치할 수 있나요?', '네. CD에 든 것과 같은(더 새로운) 드라이버를 HP 공식 사이트에서 받을 수 있어요.'),
          ('모델명은 어디에 적혀 있나요?', '프린터 앞면이나 윗면에 적혀 있고, 뒷면·바닥의 제품 스티커에도 있어요. 숫자와 영어를 그대로 입력하세요.'),
          ('삼성 프린터는 어디서 받나요?', '삼성 프린터 지원은 HP로 넘어갔어요. HP 소프트웨어 및 드라이버 페이지에서 삼성 프린터 모델명으로 검색하세요.'),
          ('맥(Mac)에서도 되나요?', '네. HP 페이지가 내 컴퓨터 운영체제를 자동으로 골라 줘요. 다른 운영체제용은 [다른 OS 선택하기]로 바꿀 수 있어요.')]
    fq, fqld = cu.faq(qa)
    main = (f'<header class="top hub">{cr}<h1>HP 프린터 드라이버 다운로드·설치 방법 (삼성 프린터 포함)</h1>'
            '<p class="lead">HP 프린터·복합기 드라이버를 공식 사이트에서 받아 설치하는 순서를 그림으로 쉽게 정리했어요. 삼성 프린터도 같은 방법이에요.</p>'
            f'<p class="cu-ans">{ans}</p>'
            + dl(HP_DRV, 'HP 드라이버 받으러 가기', 'HP 공식 소프트웨어 및 드라이버 페이지')
            + '<ul class="dr-toc"><li><a href="#steps">설치 순서</a></li><li><a href="#samsung">삼성 프린터</a></li><li><a href="#trouble">안 될 때</a></li><li><a href="#win">윈도우 자동 설치</a></li></ul></header>'
            f'<section class="card dr-sec" id="steps"><h2>그림으로 보는 설치 순서 (6단계)</h2>{steps}'
            + dl(HP_DRV, 'HP 드라이버 받으러 가기', '1단계부터 시작해요') + '</section>'
            + samsung + trouble + WIN_SEC + fq + src_sec('HP 고객지원 문서 \'HP홈페이지에서 프린터 소프트웨어를 다운로드하는 방법\', 삼성전자 \'삼성 프린터 지원은 HP가 맡음\' 안내, Microsoft 지원 \'최신 프린터 드라이버 다운로드 및 설치\'')
            + REL)
    ld = [crld, fqld, howto('HP 프린터 드라이버 설치 방법', ['HP 소프트웨어 및 드라이버 페이지 열기', '프린터 모델명 입력 후 제출', '제품 전용 통합 소프트웨어 다운로드', '받은 파일 실행', '화면 안내대로 설치', '테스트 페이지 인쇄로 확인'])]
    write(path, 'HP 프린터 드라이버 다운로드·설치 방법 (삼성 프린터 포함, 2026) | 홍라이프 도구',
          'HP 프린터·복합기 드라이버를 HP 공식 사이트에서 받아 설치하는 6단계를 그림으로 쉽게 설명해요. 모델명 검색, 제품 전용 통합 소프트웨어, 삼성 프린터 드라이버 받는 곳, 안 될 때 해결법까지.',
          main, ld)
    return path


# ── 신도리코 ─────────────────────────────────────────────
SD_HOME = 'https://www.sindoh.com/ko/'
SD_CONNECT = 'https://www.sindoh.com/support/download/d470'
SD_LAN = 'https://support.sindoh.com/%ED%94%84%EB%A6%B0%ED%84%B0-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84lan-%EB%B9%A0%EB%A5%B8%EC%84%A4%EC%B9%98-1'
SD_USB = 'https://support.sindoh.com/%ED%94%84%EB%A6%B0%ED%84%B0-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-usb-%EB%B9%A0%EB%A5%B8%EC%84%A4%EC%B9%98-'
SD_SCAN = 'https://support.sindoh.com/%EC%8A%A4%EC%BA%90%EB%84%88-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84scanner-driver-%EC%84%A4%EC%B9%98-%EB%B0%A9%EB%B2%95'
SD_MAC = 'https://support.sindoh.com/manual/%EC%A0%84%EA%B8%B0%EC%A2%85/mac-%ED%94%84%EB%A6%B0%ED%84%B0%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-lan-%EC%84%A4%EC%B9%98'
SD_SEARCH = 'https://www.sindoh.com/ko/customer/total-search-result.php?key_word='
SD_MODELS = ([(m, 'A3 컬러 복합기') for m in ['D320', 'D321', 'D450', 'D451', 'D452', 'D470', 'D471', 'D472', 'D500', 'D740', 'D741', 'D742', 'D750', 'D751']]
             + [(m, 'A3 흑백 복합기') for m in ['N501', 'N502', 'N631', 'N633', 'N920', 'N921', 'N922', 'N923']] + [('M702', 'A4 흑백 복합기')])


def sindoh():
    path = '/driver/sindoh.html'
    cr, crld = crumb([('신도리코 드라이버', '')])
    ans = ('신도리코 드라이버는 <b>신도리코 홈페이지 → 고객 지원 → 다운로드</b>에서 <b>기종 검색</b>에 모델명을 넣고, '
           '<b>드라이버/유틸리티</b>에서 받아요. 아래 표에 있는 복합기는 <b>sindoh Connect</b>로 설치하는 게 공식 권장이고, '
           '표에 없는 기종은 <b>빠른 설치 드라이버</b>를 쓰면 돼요.')
    rows = [(m, k + ' · sindoh Connect 지원', SD_SEARCH + m) for m, k in SD_MODELS]
    steps = (cu.step(1, '신도리코 다운로드에서 기종 검색', '<b>신도리코 홈페이지 → 고객 지원 → 다운로드</b>로 가서 <b>기종 검색</b>에 모델명(예: D452)을 넣어요. 위 표의 [다운로드] 버튼을 누르면 이 검색 결과로 바로 가요.',
                     W_search('sindoh.com', '고객 지원 › 다운로드', '기종 검색: 모델명 입력', '검색'))
             + cu.step(2, '빠른 설치 드라이버 받기', '검색 결과 아래 <b>드라이버/유틸리티</b>에서 <b>빠른 설치 드라이버</b>를 내려받아요.',
                       W_list('sindoh.com', '드라이버/유틸리티', [('프린터 드라이버', ''), ('빠른 설치 드라이버', '다운로드'), ('매뉴얼', '')], 1))
             + cu.step(3, '압축 풀기', '받은 압축 파일에서 마우스 <b>오른쪽 버튼</b>을 누르고 <b>[알아서 풀기]</b>를 골라요.', W_unzip(),
                       '압축 프로그램에 따라 메뉴 이름이 \'압축 풀기\', \'여기에 풀기\'처럼 다를 수 있어요.')
             + cu.step(4, 'SETUP.EXE 실행 → \'예\'', '풀린 폴더에서 <b>SETUP.EXE</b>를 실행해요. "이 앱이 디바이스를 변경할 수 있도록 허용하시겠어요?" 창이 뜨면 <b>[예]</b>를 눌러요.',
                       W_uac('SETUP.EXE'))
             + cu.step(5, '포트를 USB로 바꾸고 [설치]', '<b>Sindoh Easy 프린터 설치 툴</b>이 열리면 로컬 포트를 <b>LPT1 → USB</b>로 바꾸고 <b>[설치]</b>를 눌러요. 끝나면 설치 툴이 저절로 닫혀요.',
                       W_sindoh_tool(), '네트워크(랜선)로 연결한 복합기는 아래 \'LAN 빠른 설치\' 안내를 따르세요.')
             + cu.step(7, '테스트 페이지로 확인', '<b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b>(또는 제어판 → 장치 및 프린터 보기)에서 설치한 프린터를 고르고 <b>[테스트 페이지 인쇄]</b>를 눌러요.',
                       W_testpage(7)))
    connect = ('<section class="card dr-sec" id="connect"><h2>sindoh Connect로 설치하기 (권장 기종)</h2>'
               '<p>아래 표의 복합기는 신도리코가 <b>sindoh Connect 설치를 권장</b>해요. 민수용·관수용 모두 해당돼요. 표에 없는 기종은 위 \'빠른 설치 드라이버\' 순서를 따르세요.</p>'
               + dl(SD_CONNECT, 'sindoh Connect 받기', '신도리코 공식 다운로드') + '</section>')
    more = ('<section class="card dr-sec" id="more"><h2>연결 방식별 공식 설치 안내</h2><p>연결 방식에 따라 설치 방법이 조금 달라요. 내 상황에 맞는 공식 안내를 여세요.</p>'
            + dl(SD_USB, 'USB 빠른 설치 안내', 'USB 케이블로 연결할 때 (신도리코 공식)', True)
            + dl(SD_LAN, 'LAN 빠른 설치 안내', '랜선·네트워크로 연결할 때 (신도리코 공식)', True)
            + dl(SD_SCAN, '스캐너 드라이버(USB) 설치', '스캔이 안 될 때 (신도리코 공식)', True)
            + dl(SD_MAC, '맥(Mac) 드라이버 설치', '맥에서 랜선 연결로 인쇄할 때 (신도리코 공식)', True)
            + '<p class="cu-src" style="margin-top:10px">신도리코 고객지원센터 <b>1588-5850</b> (공식 안내 기준)</p></section>')
    qa = [('신도리코 드라이버는 어디서 받나요?', '신도리코 홈페이지 → 고객 지원 → 다운로드에서 기종 검색에 모델명을 넣고, 결과의 드라이버/유틸리티에서 받아요.'),
          ('sindoh Connect와 빠른 설치 드라이버는 뭐가 달라요?', '신도리코가 정한 지원 기종(이 페이지 표)은 sindoh Connect 설치를 권장해요. 표에 없는 기종은 빠른 설치 드라이버를 쓰면 돼요.'),
          ('설치했는데 프린터가 안 보여요.', '설정 → Bluetooth 및 장치 → 프린터 및 스캐너에서 프린터가 있는지 확인하고, USB로 연결했다면 설치 툴에서 포트를 USB로 골랐는지 다시 확인하세요.'),
          ('스캔은 어떻게 하나요?', '스캔용 드라이버는 따로 있어요. 위 \'스캐너 드라이버(USB) 설치\' 공식 안내를 따르세요.'),
          ('도움이 더 필요해요.', '신도리코 고객지원센터(1588-5850)나 신도리코 홈페이지로 문의하세요.')]
    fq, fqld = cu.faq(qa)
    main = (f'<header class="top hub">{cr}<h1>신도리코 프린터·복합기 드라이버 다운로드·설치 방법</h1>'
            '<p class="lead">신도리코 복합기 드라이버를 공식 사이트에서 받아 설치하는 순서를 그림으로 쉽게 정리했어요. 아래 표에서 내 모델을 찾아 바로 받을 수 있어요.</p>'
            f'<p class="cu-ans">{ans}</p>' + dl(SD_HOME, '신도리코 다운로드 받으러 가기', '신도리코 공식 홈페이지 → 고객 지원 → 다운로드')
            + '<ul class="dr-toc"><li><a href="#models">모델별 다운로드</a></li><li><a href="#steps">설치 순서</a></li><li><a href="#connect">sindoh Connect</a></li><li><a href="#more">USB·LAN·스캔·맥</a></li></ul></header>'
            '<section class="card dr-sec" id="models"><h2>모델별 다운로드 바로가기</h2>'
            '<p>모델명을 입력하면 그 줄로 바로 가요. [다운로드]를 누르면 신도리코 공식 다운로드 검색 결과가 열려요.</p>'
            + model_search([m for m, _ in SD_MODELS]) + models_table(rows)
            + '<p class="cu-src" style="margin-top:8px">표는 신도리코가 sindoh Connect 지원 기종으로 안내한 모델이에요. 다른 모델도 신도리코 다운로드의 기종 검색에서 똑같이 찾을 수 있어요.</p></section>'
            f'<section class="card dr-sec" id="steps"><h2>그림으로 보는 설치 순서 (USB 빠른 설치)</h2>{steps}</section>'
            + connect + more + WIN_SEC + fq
            + src_sec('신도리코 고객지원 FAQ \'프린터 드라이버는 어떻게 다운 받나요?\', \'프린터 드라이버(USB) -빠른설치-\', Microsoft 지원 \'최신 프린터 드라이버 다운로드 및 설치\'')
            + REL)
    ld = [crld, fqld, howto('신도리코 프린터 드라이버 설치 방법 (USB 빠른 설치)', ['신도리코 다운로드에서 기종 검색', '드라이버/유틸리티에서 빠른 설치 드라이버 다운로드', '압축 풀기', 'SETUP.EXE 실행 후 예', '로컬 포트를 USB로 바꾸고 설치', '테스트 페이지 인쇄로 확인'])]
    write(path, '신도리코 프린터·복합기 드라이버 다운로드·설치 방법 (모델별 바로가기, 2026) | 홍라이프 도구',
          '신도리코 복합기 드라이버를 공식 사이트에서 받아 설치하는 방법을 그림으로 쉽게 설명해요. D452·D472·N502 등 모델별 다운로드 바로가기, sindoh Connect, USB·LAN 빠른 설치, 스캐너·맥 드라이버까지.',
          main, ld)
    return path


# ── 공통 조각 ────────────────────────────────────────────
WIN_SEC = ('<section class="card dr-sec" id="win"><h2>먼저 해 볼 것: 윈도우 자동 설치</h2>'
           '<p>요즘 윈도우는 프린터를 연결하면 드라이버를 스스로 찾아 설치하는 경우가 많아요. 제조사 사이트에 가기 전에 한 번 해 보세요.</p><ul class="cu-chk">'
           '<li><b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b>에서 <b>[장치 추가]</b>를 눌러 프린터를 추가해요.</li>'
           '<li><b>Windows 업데이트</b>로 드라이버를 받는 방법을 Microsoft가 권장해요.</li>'
           '<li>그래도 안 되면 제조사 공식 사이트에서 모델명을 검색해 윈도우 버전에 맞는 최신 소프트웨어를 받아요(이 페이지의 방법).</li></ul></section>')
REL = ('<section class="card rel"><h2>다른 회사 드라이버</h2><ul class="dr-co">'
       '<li><a href="/driver/hp.html"><b>HP</b><span>프린터·복합기 (삼성 프린터 포함)</span></a></li>'
       '<li><a href="/driver/sindoh.html"><b>신도리코</b><span>복합기 · 모델별 바로가기</span></a></li>'
       '<li><a href="/driver/"><b>드라이버 모음 전체</b><span>회사별·기기별로 찾기</span></a></li></ul></section>')


def src_sec(s):
    return (f'<section class="card"><h2>출처와 안내</h2><p class="cu-src">출처: {E(s)} · 확인 {CHECKED}.<br>'
            '홍라이프 도구는 드라이버 파일을 직접 올리지 않아요. 모든 다운로드는 제조사 공식 사이트에서 이루어져요. '
            '그림은 이해를 돕기 위해 단순하게 그린 것이라 실제 화면과 다를 수 있어요.</p></section>')


def howto(name, names):
    return {"@context": "https://schema.org", "@type": "HowTo", "name": name,
            "step": [{"@type": "HowToStep", "position": i + 1, "name": n} for i, n in enumerate(names)]}


# ── 허브 ────────────────────────────────────────────────
EXT = [('캐논', 'https://svc.kr.canon/', '캐논코리아 고객지원 다운로드'),
       ('엡손', 'https://www.epson.co.kr/%EA%B3%A0%EA%B0%9D%EC%A7%80%EC%9B%90/sl/s', '엡손 고객지원'),
       ('브라더', 'https://support.brother.com/g/b/productsearch.aspx?c=kr&lang=ko', '브라더 지원 및 다운로드')]


def hub():
    path = '/driver/'
    cr = '<p class="crumb"><a href="/">홈</a> › 드라이버</p>'
    crld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + '/'}, {"@type": "ListItem", "position": 2, "name": "드라이버", "item": SITE + path}]}
    allm = [(m, '/driver/sindoh.html#m-' + re.sub(r'[^A-Za-z0-9]', '', m)) for m, _ in SD_MODELS]
    data = json.dumps(allm, ensure_ascii=False)
    co = ('<li><a href="/driver/hp.html"><b>HP</b><span>프린터·복합기, 삼성 프린터 포함</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/sindoh.html"><b>신도리코</b><span>복합기, 모델별 다운로드 바로가기</span><em>그림 설명 ›</em></a></li>'
          + ''.join(f'<li><a href="{E(u)}" target="_blank" rel="noopener nofollow"><b>{E(n)}</b><span>{E(d)}</span><em>공식 사이트로 바로 가기 ↗</em></a></li>' for n, u, d in EXT))
    what = cu.step('?', '드라이버가 뭐예요?', '드라이버는 <b>기기와 컴퓨터를 이어 주는 통역 프로그램</b>이에요. 프린터를 USB로 꽂아도 드라이버가 없으면 컴퓨터가 \'이게 무슨 기계인지\' 몰라서 인쇄가 안 돼요.',
                   pc('<rect x="50" y="70" width="70" height="60" rx="8" fill="#334155"/><rect x="60" y="56" width="50" height="18" rx="2" fill="#EAF1FC"/><text x="85" y="148" text-anchor="middle" font-size="10" fill="#333">프린터</text>'
                      '<path d="M128 100 H232" stroke="#1D4ED8" stroke-width="3" stroke-dasharray="6 5"/><rect x="146" y="86" width="68" height="28" rx="14" fill="#1D4ED8"/><text x="180" y="104" text-anchor="middle" font-size="11" font-weight="800" fill="#fff">드라이버</text>'
                      '<rect x="240" y="66" width="60" height="44" rx="5" fill="#1E293B"/><rect x="262" y="110" width="16" height="10" fill="#ADB5BD"/><text x="270" y="148" text-anchor="middle" font-size="10" fill="#333">컴퓨터</text>', '드라이버 = 통역'))
    name = cu.step('!', '내 기기 모델명 찾기', '드라이버는 <b>모델명</b>으로 찾아요. 프린터는 보통 <b>앞면이나 윗면</b>에 모델명이 적혀 있고, <b>뒷면·바닥 스티커</b>에도 있어요. 영어와 숫자를 그대로 적어 두세요.',
                   pc('<rect x="70" y="60" width="150" height="90" rx="12" fill="#334155"/><rect x="92" y="44" width="106" height="24" rx="3" fill="#EAF1FC"/>'
                      '<rect x="84" y="76" width="70" height="16" rx="3" fill="#F8F9FA"/><text x="90" y="88" font-size="10" font-weight="800" fill="#111">모델명 ○○○</text>' + ring(84, 76, 70, 16, 1)
                      + '<rect x="236" y="90" width="80" height="44" rx="4" fill="#FFF6E5" stroke="#FFC078"/><text x="244" y="106" font-size="9" fill="#333">뒷면 스티커</text><text x="244" y="122" font-size="9" font-weight="800" fill="#111">Model: ○○○</text>' + ring(236, 90, 80, 44, 2), '모델명 위치'))
    qa = [('드라이버는 꼭 설치해야 하나요?', '요즘 윈도우는 연결만 해도 기본 드라이버를 자동으로 설치하는 경우가 많아요. 다만 스캔·양면 인쇄 같은 기능까지 다 쓰려면 제조사 드라이버를 설치하는 게 좋아요.'),
          ('CD를 잃어버렸어요.', '괜찮아요. CD에 든 드라이버는 제조사 공식 사이트에서 무료로(더 새로운 버전으로) 받을 수 있어요.'),
          ('\'드라이버 자동 설치\' 프로그램을 써도 되나요?', '광고에 나오는 출처가 불분명한 드라이버 프로그램이나 블로그 파일은 쓰지 마세요. 원치 않는 프로그램이 함께 깔릴 수 있어요. 제조사 공식 사이트나 Windows 업데이트를 쓰세요.'),
          ('32비트, 64비트는 어떻게 골라요?', '제조사 사이트가 대부분 내 컴퓨터를 자동으로 알아봐요. 직접 골라야 하면 설정 → 시스템 → 정보에서 \'시스템 종류\'를 확인하세요.'),
          ('이 사이트에서 파일을 받는 건가요?', '아니요. 홍라이프 도구는 파일을 올리지 않고, 버튼을 누르면 제조사 공식 다운로드 페이지로 바로 연결돼요.')]
    fq, fqld = cu.faq(qa)
    main = (f'<header class="top hub">{cr}<h1>드라이버·프로그램 다운로드 모음</h1>'
            '<p class="lead">프린터·복합기 드라이버를 회사별로 모아, 공식 사이트에서 받는 방법과 설치 순서를 그림으로 쉽게 정리했어요. 회사와 기기는 계속 늘려요.</p>'
            '<p class="cu-ans">① 기기 <b>모델명</b>을 확인하고 → ② 아래에서 <b>회사</b>를 고른 뒤 → ③ 파란 <b>[다운로드]</b> 버튼으로 공식 사이트에서 받아 → ④ 그림 순서대로 설치하세요. '
            '파일은 모두 제조사 공식 사이트에서 받아요.</p>'
            '<form class="dr-q" onsubmit="return drH()"><input id="dr-in" placeholder="모델명 검색 (예: D452)" autocomplete="off" oninput="drH()" aria-label="모델명 검색"><button type="submit">찾기</button></form><ul id="dr-res"></ul>'
            f'<script>var DRA={data};function drH(){{var q=document.getElementById("dr-in").value.replace(/\\s/g,"").toUpperCase(),r=document.getElementById("dr-res");if(!q){{r.innerHTML="";return false}}'
            'var h=DRA.filter(function(x){return x[0].toUpperCase().indexOf(q)>=0}).slice(0,8);r.innerHTML=h.length?h.map(function(x){return\'<li><a href="\'+x[1]+\'">\'+x[0]+\' 드라이버 받기 ›</a></li>\'}).join(""):'
            '"<li>아직 모델 표에 없는 모델이에요. 아래에서 회사를 고르면 공식 사이트에서 모델명으로 찾을 수 있어요.</li>";return false}</script></header>'
            f'<section class="card"><h2>회사 고르기</h2><ul class="dr-co">{co}</ul>'
            '<p class="cu-src" style="margin-top:10px">캐논·엡손·브라더는 그림 설명을 준비하는 동안 공식 다운로드 사이트로 바로 연결해요.</p></section>'
            f'<section class="card"><h2>시작 전에 알아 두기</h2>{what}{name}</section>'
            + WIN_SEC
            + '<section class="card"><h2>가짜 드라이버 사이트 조심하기</h2><p class="dr-warn">검색 광고에 나오는 \'드라이버 자동 설치\' 프로그램이나 블로그에 올라온 설치 파일은 받지 마세요. '
              '원치 않는 프로그램이나 광고가 함께 깔릴 수 있어요. <b>제조사 공식 사이트</b>나 <b>Windows 업데이트</b>에서 받는 게 가장 안전해요.</p></section>'
            + fq + src_sec('각 제조사 공식 고객지원 안내, Microsoft 지원 \'최신 프린터 드라이버 다운로드 및 설치\''))
    write(path, '드라이버 다운로드 모음 — 프린터·복합기 드라이버 설치 방법 (HP·삼성·신도리코·캐논·엡손·브라더) | 홍라이프 도구',
          '프린터·복합기 드라이버를 회사별로 모아 공식 사이트에서 받는 방법과 설치 순서를 그림으로 쉽게 정리했어요. 모델명 찾는 법, 윈도우 자동 설치, 가짜 드라이버 사이트 주의, HP·삼성·신도리코·캐논·엡손·브라더.',
          main, [crld, fqld])
    return path


if __name__ == '__main__':
    print('\n'.join([hub(), hp(), sindoh()]))
