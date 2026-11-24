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
       '.dl3d{display:inline-flex;align-items:center;gap:12px;margin:8px 8px 4px 0;padding:12px 18px 12px 12px;border-radius:14px;min-height:48px;'
       'background:var(--acc,#1B64DA);border:0;color:#fff!important;text-decoration:none;box-shadow:none;transition:background .15s;max-width:100%;box-sizing:border-box}'
       '.dl3d:hover{background:var(--acc-d,#1957C2)}'
       '.dl3d .ic{flex:none;width:36px;height:36px;border-radius:10px;background:rgba(255,255,255,.16);display:grid;place-items:center}'
       '.dl3d .ic svg{width:20px;height:20px}.dl3d .tx{display:flex;flex-direction:column;line-height:1.3;min-width:0}'
       '.dl3d b{font-size:16px;font-weight:700;word-break:keep-all}.dl3d small{font-size:12.5px;opacity:.9;font-weight:500;word-break:keep-all}'
       '.dl3d.s{background:var(--acc-soft,#EAF2FE);color:var(--acc,#1B64DA)!important}.dl3d.s:hover{background:var(--acc-line,#C9E2FF)}'
       '.dl3d.s .ic{background:#fff}'
       '.dr-sec{scroll-margin-top:70px}.dr-toc{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0;padding:0;list-style:none}'
       '.dr-toc a{display:inline-block;padding:7px 12px;border-radius:999px;background:#EEF4FF;color:#1D4ED8;font-weight:700;font-size:14px;text-decoration:none}'
       '.dr-m{width:100%;border-collapse:collapse;font-size:14.5px}.dr-m th,.dr-m td{padding:9px 8px;border-bottom:1px solid var(--line-s,#E3E7EE);text-align:left;vertical-align:middle;word-break:keep-all}'
       '.dr-m th{color:var(--muted,#5B6B82);font-weight:700;font-size:13px}.dr-m td:first-child{font-weight:800;white-space:nowrap}'
       '.dr-m a.mini{display:inline-block;padding:7px 12px;border-radius:10px;background:var(--acc,#1B64DA);color:#fff!important;font-weight:700;font-size:13px;text-decoration:none;white-space:nowrap}'
       '.dr-q{display:flex;gap:8px;margin:12px 0 4px}.dr-q input{flex:1;min-width:0;padding:12px 14px;border:1.5px solid #BFD3FB;border-radius:12px;font-size:16px}'
       '.dr-q button{flex:none;padding:0 16px;border:0;border-radius:12px;background:var(--acc,#1B64DA);color:#fff;font-weight:800;font-size:15px}'
       '#dr-res{list-style:none;margin:6px 0 0;padding:0}#dr-res li{padding:8px 2px;border-bottom:1px dashed var(--line-s,#E3E7EE)}#dr-res a{font-weight:700}'
       '.dr-warn{background:#FFF6E5;border:1px solid #FFE0A3;border-radius:12px;padding:12px 14px;line-height:1.7;font-size:15px}'
       '.dr-co{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;list-style:none;margin:0;padding:0}'
       '.dr-co a{display:block;padding:14px;border:1px solid var(--line-s,#E3E7EE);border-radius:14px;text-decoration:none;color:inherit;background:#fff}'
       '.dr-co a b{display:block;font-size:17px;color:var(--head,#111)}.dr-co a span{font-size:13px;color:var(--muted,#5B6B82);word-break:keep-all}.dr-co a em{display:block;margin-top:6px;font-style:normal;font-size:12.5px;color:#1D4ED8;font-weight:700}'
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
KO2EN = {'/driver/': '/en/driver/', '/driver/hp.html': '/en/driver/hp.html', '/driver/sindoh.html': '/en/driver/sindoh.html',
         '/driver/nvidia.html': '/en/driver/nvidia.html', '/driver/amd.html': '/en/driver/amd.html', '/driver/intel.html': '/en/driver/intel.html',
         '/driver/epson.html': '/en/driver/epson.html', '/driver/brother.html': '/en/driver/brother.html', '/driver/lg.html': '/en/driver/lg.html', '/driver/apple.html': '/en/driver/apple.html', '/driver/surface.html': '/en/driver/surface.html', '/driver/lenovo.html': '/en/driver/lenovo.html', '/driver/dell.html': '/en/driver/dell.html', '/driver/asus.html': '/en/driver/asus.html', '/driver/acer.html': '/en/driver/acer.html', '/driver/roborock.html': '/en/driver/roborock.html', '/driver/samsung.html': '/en/driver/samsung.html', '/driver/ecovacs.html': '/en/driver/ecovacs.html', '/driver/dreame.html': '/en/driver/dreame.html', '/driver/narwal.html': '/en/driver/narwal.html', '/driver/wd.html': '/en/driver/wd.html', '/driver/seagate.html': '/en/driver/seagate.html', '/driver/crucial.html': '/en/driver/crucial.html', '/driver/synology.html': '/en/driver/synology.html', '/driver/qnap.html': '/en/driver/qnap.html', '/driver/benq.html': '/en/driver/benq.html', '/driver/viewsonic.html': '/en/driver/viewsonic.html', '/driver/huion.html': '/en/driver/huion.html', '/driver/xppen.html': '/en/driver/xppen.html', '/driver/msi.html': '/en/driver/msi.html', '/driver/gigabyte.html': '/en/driver/gigabyte.html', '/driver/asrock.html': '/en/driver/asrock.html', '/driver/hansung.html': '/en/driver/hansung.html', '/driver/razer.html': '/en/driver/razer.html', '/driver/canon.html': '/en/driver/canon.html', '/driver/fujifilm.html': '/en/driver/fujifilm.html', '/driver/kyocera.html': '/en/driver/kyocera.html', '/driver/ricoh.html': '/en/driver/ricoh.html', '/driver/logitech.html': '/en/driver/logitech.html', '/driver/wacom.html': '/en/driver/wacom.html', '/driver/realtek.html': '/en/driver/realtek.html', '/driver/iptime.html': '/en/driver/iptime.html', '/driver/tplink.html': '/en/driver/tplink.html', '/driver/steelseries.html': '/en/driver/steelseries.html', '/driver/corsair.html': '/en/driver/corsair.html', '/driver/hyperx.html': '/en/driver/hyperx.html', '/driver/creative.html': '/en/driver/creative.html', '/driver/jabra.html': '/en/driver/jabra.html', '/driver/epos.html': '/en/driver/epos.html', '/driver/mskb.html': '/en/driver/mskb.html', '/driver/android.html': '/en/driver/android.html', '/driver/elgato.html': '/en/driver/elgato.html', '/driver/ssd.html': '/en/driver/ssd.html', '/driver/vcredist.html': '/en/driver/vcredist.html', '/driver/directx.html': '/en/driver/directx.html', '/driver/dotnet.html': '/en/driver/dotnet.html', '/driver/xbox.html': '/en/driver/xbox.html'}
EN2KO = {v: k for k, v in KO2EN.items()}
# 한국어가 아닌 브라우저(검색 로봇 제외)는 영어판으로 바로 보냄. '한국어로 보기'를 누른 사람(hl_lang=ko)은 그대로.
REDIRECT = ("<script>(function(){try{var L=(navigator.languages&&navigator.languages[0])||navigator.language||'';"
            "if(/^ko/i.test(L)||/bot|crawl|spider|lighthouse|slurp|bing|yeti|daum/i.test(navigator.userAgent))return;"
            "if(localStorage.getItem('hl_lang')==='ko')return;var a=document.querySelector('link[rel=alternate][hreflang=en]');"
            "if(a)location.replace(a.getAttribute('href')+location.hash)}catch(e){}})();</script>")


def write(path, title, desc, main, ld):
    out = os.path.join(ROOT, 'overlay', path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    h = cu.head(title, desc, SITE + path, ld).replace(cu.CSS, cu.CSS + CSS)
    if path in KO2EN:
        alt = (f'<link rel="alternate" hreflang="ko" href="{SITE + path}"><link rel="alternate" hreflang="en" href="{SITE + KO2EN[path]}">'
               f'<link rel="alternate" hreflang="x-default" href="{SITE + path}">')
        h = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', h)
        h = h.replace(f'<link rel="canonical" href="{SITE + path}">', f'<link rel="canonical" href="{SITE + path}">' + alt + REDIRECT, 1)
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


HP_DATA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'hp_models.json'), encoding='utf-8'))


def mid(n):
    return 'm-' + re.sub(r'[^A-Za-z0-9]', '', n.replace('HP', '', 1))


def hp_cards():
    out = []
    for m in HP_DATA['models']:
        t, u, sz, ver, d = m['w']
        nav = f'https://support.hp.com/kr-ko/hp-pps-services/hub/navigation?h_product={m["o"]}&h_lang=ko&h_cc=kr&h_pagetype=s-002'
        btns = f'<a class="dl3d" href="{E(u)}" rel="nofollow"><span class="ic">{DLICON}</span><span class="tx"><b>윈도우용 바로 받기</b><small>{E(sz)} · 누르면 바로 다운로드 시작</small></span></a>'
        mt, mu, msz, app = m['m']
        btns += (f'<a class="dl3d s" href="{E(mu)}" rel="nofollow"{" target=_blank" if app else ""}><span class="ic">{DLICON}</span><span class="tx"><b>맥(Mac)용</b>'
                 f'<small>{E(mt)}{(" · " + E(msz)) if msz else ""}</small></span></a>')
        extra = ''
        if m.get('b'):
            extra += f'<a class="sm" href="{E(m["b"][0])}" rel="nofollow">기본 드라이버만 받기 ({E(m["b"][1])}, 64비트)</a>'
        extra += f'<a class="sm" href="{E(nav)}" target="_blank" rel="noopener nofollow">HP 공식 페이지에서 보기 ↗</a>'
        out.append(f'<li class="hpm" id="{mid(m["n"])}"><h3>{E(m["n"])}</h3><p class="fi">📦 {E(t)}<br><span>버전 {E(ver)} · 출시 {E(d)}</span></p>'
                   f'<div class="bt">{btns}</div><p class="ex">{extra}</p></li>')
    return '<ul class="hpl">' + ''.join(out) + '</ul>'


HP_CSS = ('<style>.hpl{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:12px}'
          '.hpm{border:1px solid var(--line-s,#E3E7EE);border-radius:16px;padding:14px;background:#fff;scroll-margin-top:80px}'
          '.hpm:target{border-color:#1D4ED8;box-shadow:0 0 0 3px #DCE8FF}.hpm h3{margin:0 0 6px;font-size:17px;line-height:1.4;word-break:keep-all}'
          '.hpm .fi{margin:0 0 4px;font-size:14px;line-height:1.55;color:#333;word-break:keep-all}.hpm .fi span{font-size:12.5px;color:var(--muted,#5B6B82)}'
          '.hpm .bt{display:flex;flex-wrap:wrap;gap:0 8px}.hpm .ex{margin:8px 0 0;display:flex;flex-wrap:wrap;gap:6px 14px}'
          '.hpm .ex a.sm{font-size:13.5px;font-weight:700;color:#1D4ED8}'
          '.big-n{counter-reset:s;list-style:none;padding:0;margin:0}.big-n>li{position:relative;padding:12px 0 12px 44px;border-bottom:1px dashed var(--line-s,#E3E7EE);line-height:1.75;font-size:15.5px;word-break:keep-all}'
          '.big-n>li:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:12px;width:32px;height:32px;border-radius:50%;background:var(--acc,#1B64DA);color:#fff;font-weight:800;display:grid;place-items:center}'
          '.tipbox{background:#FFF6E5;border:1px solid #FFE0A3;border-radius:12px;padding:10px 12px;margin:8px 0 0;font-size:14.5px;line-height:1.7}</style>')


def hp():
    path = '/driver/hp.html'
    cr, crld = crumb([('HP 드라이버', '')])
    ans = ('아래 목록에서 <b>내 프린터 모델</b>을 찾아 파란 <b>[윈도우용 바로 받기]</b>를 누르면 <b>HP 공식 서버에서 설치 파일이 바로 내려받아져요.</b> '
           '받은 파일을 열고 화면 안내대로 누르기만 하면 설치가 끝나요. 회원가입이나 로그인은 필요 없어요. <b>삼성 프린터</b>도 지금은 HP가 지원해요.')
    names = [m['n'] for m in HP_DATA['models']]
    data = json.dumps([[n, '#' + mid(n)] for n in names], ensure_ascii=False)
    search = ('<form class="dr-q" onsubmit="return hpQ()"><input id="dr-in" placeholder="모델 번호 입력 (예: 8210, M15, 2130)" autocomplete="off" oninput="hpQ()" aria-label="HP 모델 검색"><button type="submit">찾기</button></form><ul id="dr-res"></ul>'
              f'<script>var HPM={data};function hpQ(){{var q=document.getElementById("dr-in").value.replace(/\\s/g,"").toUpperCase(),r=document.getElementById("dr-res");if(!q){{r.innerHTML="";return false}}'
              'var h=HPM.filter(function(x){return x[0].replace(/\\s/g,"").toUpperCase().indexOf(q)>=0}).slice(0,8);'
              'r.innerHTML=h.length?h.map(function(x){return\'<li><a href="\'+x[1]+\'">\'+x[0]+\' 바로 받기 ›</a></li>\'}).join(""):"<li>이 목록에 없는 모델이에요. 아래 \\u0027목록에 없을 때\\u0027 방법으로 HP 공식 사이트에서 찾아 주세요.</li>";return false}</script>')
    install = ('<section class="card dr-sec" id="install"><h2>받은 다음 설치하는 순서 (아주 쉽게)</h2>'
               '<p>파일을 받았다면 아래 순서대로 따라 하세요. 처음 해 보는 분도 10분이면 끝나요.</p><ol class="big-n">'
               '<li><b>먼저 준비:</b> 켜져 있는 프로그램(한글·엑셀·인터넷 창 등)을 모두 닫고, <b>프린터 전원을 켜 두세요.</b></li>'
               '<li><b>USB 선은 아직 꽂지 마세요.</b> HP 공식 안내에 따르면 설치 프로그램이 "연결하세요"라고 말할 때 꽂아야 해요. 미리 꽂으면 설치가 꼬일 수 있어요.</li>'
               '<li><b>받은 파일 열기:</b> 키보드 <b>Ctrl + J</b>를 누르면 다운로드 목록이 열려요. 방금 받은 파일(이름이 Full_Webpack…처럼 시작해요)을 눌러요. 파일은 <b>다운로드</b> 폴더에도 있어요.</li>'
               '<li><b>\'예\' 누르기:</b> "이 앱이 디바이스를 변경할 수 있도록 허용하시겠어요?"라는 창이 뜨면 <b>[예]</b>를 눌러요. 그러면 파일 압축이 저절로 풀리고 설치가 시작돼요.</li>'
               '<li><b>안내대로 [다음] 누르기:</b> 설치 프로그램이 묻는 대로 진행해요. 연결 방식을 물으면 <b>USB</b>(선으로 연결) 또는 <b>무선/네트워크</b>(와이파이) 중 내 상황을 골라요.</li>'
               '<li><b>USB라면 이때 꽂기:</b> 화면에 "USB 케이블을 연결하세요"가 나오면 그때 프린터와 컴퓨터를 선으로 이어요.</li>'
               '<li><b>끝까지 기다리기:</b> 설치에는 몇 분 걸려요. 다시 시작하라고 하면 컴퓨터를 다시 시작해요.</li>'
               '<li><b>확인하기:</b> <b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b>에서 내 프린터를 누르고 <b>[테스트 페이지 인쇄]</b>를 눌러요. 종이가 나오면 성공이에요!</li></ol>'
               '<p class="tipbox">💡 <b>통합 소프트웨어와 기본 드라이버, 뭘 받아요?</b><br>잘 모르겠으면 파란 <b>[윈도우용 바로 받기]</b>(통합 소프트웨어)를 받으세요. HP 설명에 따르면 통합 소프트웨어는 <b>프린터 CD에 든 드라이버·설치 프로그램·관리 도구를 모두 담은 세트</b>예요. '
               '\'기본 드라이버만 받기\'는 인쇄용 기본 드라이버만 설치하는 작은 파일로, 회사 전산 담당자용이에요(64비트 윈도우 전용).</p></section>')
    pics = (cu.step(1, '파란 버튼 누르면 바로 다운로드', '내 모델 줄의 <b>[윈도우용 바로 받기]</b>를 누르면 HP 서버에서 파일이 내려받아져요. 브라우저 오른쪽 위에 다운로드 표시가 생겨요.',
                    W_downloads('Full_Webpack…exe', 1))
            + cu.step(2, '\'예\' 누르기', '받은 파일을 열면 윈도우가 허락을 물어요. <b>[예]</b>를 눌러요.', W_uac('HP 설치 프로그램', 2))
            + cu.step(3, '연결 방식 고르고 [다음]', 'USB 선으로 쓸지, 와이파이로 쓸지 골라요. USB는 화면이 "연결하세요"라고 할 때 꽂아요.',
                      W_installer('HP 프린터 설치', ['연결 방식을 고르세요', '○ USB 케이블', '○ 무선(와이파이)'], '다음', 3))
            + cu.step(4, '테스트 페이지로 확인', '<b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b> → 내 프린터 → <b>[테스트 페이지 인쇄]</b>.', W_testpage(4)))
    notlisted = (cu.step(1, 'HP 공식 다운로드 페이지 열기', '아래 버튼을 누르면 HP \'소프트웨어 및 드라이버\' 페이지가 열려요. 제품 종류에서 <b>프린터</b>를 골라요.',
                         W_search('support.hp.com', '프린터', '모델명 입력 (예: 프린터 이름)', '제출'))
                 + cu.step(2, '모델명 넣고 [제출] → 통합 소프트웨어 받기', '내 제품을 고르면 내 컴퓨터 운영체제에 맞는 목록이 자동으로 나와요. <b>제품 전용 통합 소프트웨어(인쇄 및 스캔 드라이버)</b>를 받아 위 \'설치 순서\'대로 설치해요.',
                           W_list('support.hp.com', '내 제품 · 운영체제 자동 선택', [('운영체제: 자동 선택됨', '다른 OS'), ('소프트웨어-유틸리티', ''), ('제품 전용 통합 소프트웨어', '다운로드')], 2)))
    samsung = ('<section class="card dr-sec" id="samsung"><h2>삼성 프린터 드라이버도 HP에서</h2>'
               '<p>삼성전자는 이제 프린터를 만들거나 지원하지 않고, <b>삼성 프린터의 드라이버와 지원은 HP가 맡고 있어요</b>(삼성전자 공식 안내). '
               '삼성 프린터는 아래 \'목록에 없을 때\' 방법으로 HP 페이지에서 모델명(예: SL-로 시작하는 이름)을 검색해 받으세요.</p></section>')
    trouble = ('<section class="card dr-sec" id="trouble"><h2>안 될 때</h2><ul class="cu-chk">'
               '<li><b>버튼을 눌렀는데 아무 일도 없어요:</b> 브라우저 오른쪽 위 다운로드 아이콘을 눌러 보세요. 큰 파일(100MB 이상)은 몇 분 걸릴 수 있어요.</li>'
               '<li><b>USB를 꽂았는데 인식이 안 돼요:</b> 선을 뺀 뒤 설치 프로그램을 다시 실행하고, "연결하세요"가 나올 때 꽂으세요.</li>'
               '<li><b>맥(Mac)에서 설치:</b> HP Easy Start를 받아 실행하면 내 프린터에 맞는 드라이버를 찾아 설치해 줘요. 일부 모델은 App Store의 HP Smart 앱으로 설치해요.</li>'
               '<li><b>단종된 오래된 프린터:</b> HP 검색에 안 나오면 윈도우 기본 드라이버로 설치해 보세요(아래 \'윈도우 자동 설치\').</li></ul>'
               + dl(HP_SETUP, 'HP 프린터 설정 안내', '와이파이·유선·USB 연결 방법 (HP 공식)', True) + '</section>')
    qa = [('정말 이 페이지에서 바로 받아지나요?', '네. [윈도우용 바로 받기]를 누르면 HP 공식 서버(ftp.hp.com)의 설치 파일이 바로 내려받아져요. 홍라이프 도구는 파일을 직접 올리지 않고, HP가 공개한 파일로 연결만 해요.'),
          ('HP 드라이버는 무료인가요?', '네. HP 공식 드라이버와 소프트웨어는 무료이고, 받을 때 회원가입이나 로그인도 필요 없어요.'),
          ('CD가 없어도 설치할 수 있나요?', '네. 통합 소프트웨어에 CD에 든 드라이버와 설치 프로그램이 모두 들어 있어요.'),
          ('모델명은 어디에 적혀 있나요?', '프린터 앞면이나 윗면에 적혀 있고, 뒷면·바닥의 제품 스티커에도 있어요. 숫자만(예: 8210) 검색창에 넣어도 찾을 수 있어요.'),
          ('파일이 예전 날짜인데 괜찮나요?', '네. 표시된 날짜는 HP가 그 파일을 마지막으로 낸 날이에요. HP 공식 페이지에서 지금도 윈도우 11용으로 제공하는 최신 파일이에요(확인일 기준).'),
          ('삼성 프린터는 어디서 받나요?', '삼성 프린터 지원은 HP로 넘어갔어요. HP 소프트웨어 및 드라이버 페이지에서 삼성 프린터 모델명으로 검색하세요.')]
    fq, fqld = cu.faq(qa)
    main = (HP_CSS + f'<header class="top hub">{cr}<h1>HP 프린터 드라이버 바로 다운로드·설치 방법 (삼성 프린터 포함)</h1>'
            f'<p class="lead">많이 쓰는 HP 프린터 {len(names)}개 모델의 드라이버를 이 페이지에서 바로 받을 수 있어요. 파일은 HP 공식 서버에서 내려와요.</p>'
            f'<p class="cu-ans">{ans}</p>'
            '<ul class="dr-toc"><li><a href="#models">모델별 바로 받기</a></li><li><a href="#install">설치 순서</a></li><li><a href="#easy">처음이세요?</a></li><li><a href="#notlisted">목록에 없을 때</a></li><li><a href="#samsung">삼성 프린터</a></li><li><a href="#trouble">안 될 때</a></li></ul></header>'
            f'<section class="card dr-sec" id="models"><h2>모델별 바로 받기 ({len(names)}개)</h2><p>모델 번호를 입력하면 그 모델로 바로 가요.</p>{search}{hp_cards()}'
            f'<p class="cu-src" style="margin-top:10px">파일 정보는 HP 공식 \'소프트웨어 및 드라이버\'(윈도우 11·macOS 15 기준)에서 {E(HP_DATA["checked"])}에 확인했어요. 32비트 윈도우나 다른 버전은 \'HP 공식 페이지에서 보기\'를 눌러 고르세요.</p></section>'
            + install + guide_sec('HP') + f'<section class="card dr-sec" id="pics"><h2>그림으로 한 번 더 보기</h2>{pics}</section>'
            + f'<section class="card dr-sec" id="notlisted"><h2>목록에 없을 때: HP 공식 사이트에서 찾기</h2>{notlisted}' + dl(HP_DRV, 'HP 드라이버 검색하러 가기', 'HP 공식 소프트웨어 및 드라이버 페이지') + '</section>'
            + samsung + trouble + WIN_SEC + fq
            + src_sec('HP 공식 소프트웨어 및 드라이버(support.hp.com/kr-ko) 제품별 다운로드 정보와 설치 안내, HP 고객지원 문서 \'HP홈페이지에서 프린터 소프트웨어를 다운로드하는 방법\', 삼성전자 \'삼성 프린터 지원은 HP가 맡음\' 안내, Microsoft 지원')
            + REL)
    ld = [crld, fqld, howto('HP 프린터 드라이버 설치 방법', ['모델 찾아 윈도우용 바로 받기', '프로그램 닫고 프린터 켜기', '받은 파일 열기', '예 누르기', '연결 방식 고르고 다음', 'USB는 안내가 나올 때 연결', '테스트 페이지 인쇄'])]
    write(path, 'HP 프린터 드라이버 바로 다운로드 — 모델별 설치 파일 (OfficeJet·LaserJet·DeskJet, 삼성 포함) | 홍라이프 도구',
          'HP OfficeJet Pro 8210·8710·9010, LaserJet Pro M15·P1102, DeskJet 2130 등 많이 쓰는 HP 프린터 드라이버를 이 페이지에서 바로 받고, 쉬운 설치 순서를 그림으로 확인하세요. 파일은 HP 공식 서버에서 내려와요.',
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


SD_DATA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'sindoh_models.json'), encoding='utf-8'))


def sd_cards():
    out = []
    ct, cv, cd, cu_ = SD_DATA['connect']
    for m, kind in SD_MODELS:
        x = SD_DATA['models'].get(m) or {}
        page = f'https://www.sindoh.com/support/download/{m.lower()}'
        btns = (f'<a class="dl3d" href="{E(cu_)}" rel="nofollow"><span class="ic">{DLICON}</span><span class="tx"><b>sindoh Connect 바로 받기</b><small>원클릭 통합 설치 · 신도리코 추천</small></span></a>')
        if x.get('q'):
            qt, qv, qd, qu = x['q']
            btns += f'<a class="dl3d s" href="{E(qu)}" rel="nofollow"><span class="ic">{DLICON}</span><span class="tx"><b>빠른 설치 드라이버</b><small>{E(qt)} · {E(qv)}</small></span></a>'
        extra = ''
        if x.get('s'):
            extra += f'<a class="sm" href="{E(x["s"][3])}" rel="nofollow">스캔 프로그램 받기 ({E(x["s"][0])})</a>'
        extra += f'<a class="sm" href="{E(page)}" target="_blank" rel="noopener nofollow">신도리코 공식 페이지에서 보기 ↗</a>'
        out.append(f'<li class="hpm" id="m-{m}"><h3>신도리코 {E(m)} <span style="font-size:13px;color:var(--muted,#5B6B82);font-weight:600">{E(kind)}</span></h3>'
                   f'<p class="fi">윈도우 10·11 (64비트)' + (f'<br><span>빠른 설치 드라이버 출시 {E(x["q"][2])}</span>' if x.get('q') else '') + '</p>'
                   f'<div class="bt">{btns}</div><p class="ex">{extra}</p></li>')
    return '<ul class="hpl">' + ''.join(out) + '</ul>'


def sindoh():
    path = '/driver/sindoh.html'
    cr, crld = crumb([('신도리코 드라이버', '')])
    ans = ('신도리코 드라이버는 <b>신도리코 홈페이지 → 고객 지원 → 다운로드</b>에서 <b>기종 검색</b>에 모델명을 넣고, '
           '<b>드라이버/유틸리티</b>에서 받아요. 아래 표에 있는 복합기는 <b>sindoh Connect</b>로 설치하는 게 공식 권장이고, '
           '표에 없는 기종은 <b>빠른 설치 드라이버</b>를 쓰면 돼요.')
    rows = [(m, k + ' · sindoh Connect 지원', SD_SEARCH + m) for m, k in SD_MODELS]
    steps = (cu.step(1, '내 모델의 [빠른 설치 드라이버] 누르기', '위 목록에서 내 모델(예: D452)을 찾아 <b>[빠른 설치 드라이버]</b>를 누르면 신도리코 서버에서 압축 파일(zip)이 바로 내려받아져요. 목록에 없는 모델은 <b>신도리코 홈페이지 → 고객 지원 → 다운로드 → 기종 검색</b>에서 찾아 <b>드라이버/유틸리티</b>의 빠른 설치 드라이버를 받으세요.',
                     W_downloads('Sindoh_PCL6(빠른설치).zip', 1))
             + cu.step(2, '받은 파일 찾기', '키보드 <b>Ctrl + J</b>를 누르면 다운로드 목록이 열려요. <b>[폴더 열기]</b>로 받은 압축 파일이 있는 곳(보통 다운로드 폴더)을 열어요.',
                       W_list('다운로드 폴더', '다운로드 폴더', [('Sindoh_…PCL6(빠른설치).zip', '파일'), ('', '')], 0, 2))
             + cu.step(3, '압축 풀기', '받은 압축 파일에서 마우스 <b>오른쪽 버튼</b>을 누르고 <b>[알아서 풀기]</b>를 골라요.', W_unzip(),
                       '압축 프로그램에 따라 메뉴 이름이 \'압축 풀기\', \'여기에 풀기\'처럼 다를 수 있어요.')
             + cu.step(4, 'SETUP.EXE 실행 → \'예\'', '풀린 폴더에서 <b>SETUP.EXE</b>를 실행해요. "이 앱이 디바이스를 변경할 수 있도록 허용하시겠어요?" 창이 뜨면 <b>[예]</b>를 눌러요.',
                       W_uac('SETUP.EXE'))
             + cu.step(5, '포트를 USB로 바꾸고 [설치]', '<b>Sindoh Easy 프린터 설치 툴</b>이 열리면 로컬 포트를 <b>LPT1 → USB</b>로 바꾸고 <b>[설치]</b>를 눌러요. 끝나면 설치 툴이 저절로 닫혀요.',
                       W_sindoh_tool(), '네트워크(랜선)로 연결한 복합기는 아래 \'LAN 빠른 설치\' 안내를 따르세요.')
             + cu.step(7, '테스트 페이지로 확인', '<b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b>(또는 제어판 → 장치 및 프린터 보기)에서 설치한 프린터를 고르고 <b>[테스트 페이지 인쇄]</b>를 눌러요.',
                       W_testpage(7)))
    connect = ('<section class="card dr-sec" id="connect"><h2>sindoh Connect로 설치하기 (권장 기종)</h2>'
               '<p>위 목록의 복합기는 신도리코가 <b>sindoh Connect(원클릭 통합 설치) 설치를 권장</b>해요. 민수용·관수용 모두 해당돼요.</p><ol class="big-n">'
               '<li><b>[sindoh Connect 바로 받기]</b>를 누르면 설치 파일이 내려받아져요.</li>'
               '<li>키보드 <b>Ctrl + J</b>로 다운로드 목록을 열고 받은 파일을 눌러 실행해요.</li>'
               '<li>"이 앱이 디바이스를 변경할 수 있도록 허용하시겠어요?" 창이 뜨면 <b>[예]</b>를 눌러요.</li>'
               '<li>프로그램 화면 안내대로 내 복합기를 고르고 설치해요.</li>'
               '<li>끝나면 <b>테스트 페이지 인쇄</b>로 확인해요. 잘 안 되면 \'빠른 설치 드라이버\'를 받아 아래 그림 순서대로 설치하세요.</li></ol>'
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
    main = (HP_CSS + f'<header class="top hub">{cr}<h1>신도리코 프린터·복합기 드라이버 바로 다운로드·설치 방법</h1>'
            '<p class="lead">신도리코 복합기 드라이버를 공식 사이트에서 받아 설치하는 순서를 그림으로 쉽게 정리했어요. 아래 표에서 내 모델을 찾아 바로 받을 수 있어요.</p>'
            f'<p class="cu-ans">{ans}</p>' + dl(SD_HOME, '신도리코 다운로드 받으러 가기', '신도리코 공식 홈페이지 → 고객 지원 → 다운로드')
            + '<ul class="dr-toc"><li><a href="#models">모델별 바로 받기</a></li><li><a href="#easy">처음이세요?</a></li><li><a href="#steps">설치 순서</a></li><li><a href="#connect">sindoh Connect</a></li><li><a href="#more">USB·LAN·스캔·맥</a></li></ul></header>'
            '<section class="card dr-sec" id="models"><h2>모델별 바로 받기 (23개)</h2>'
            '<p>모델명을 입력하면 그 모델로 바로 가요. 파란 버튼을 누르면 신도리코 공식 서버에서 파일이 바로 내려받아져요.</p>'
            + model_search([m for m, _ in SD_MODELS]) + sd_cards()
            + f'<p class="cu-src" style="margin-top:8px">파일은 신도리코 공식 다운로드 페이지에서 {E(SD_DATA["checked"])}에 확인한 것이고, 누르면 신도리코 서버에서 바로 받아져요. 표는 신도리코가 sindoh Connect 지원 기종으로 안내한 모델이에요. 다른 모델도 신도리코 다운로드의 기종 검색에서 찾을 수 있어요.</p></section>'
            f'<section class="card dr-sec" id="steps"><h2>그림으로 보는 설치 순서 (USB 빠른 설치)</h2>{steps}</section>'
            + connect + guide_sec('신도리코', True) + more + WIN_SEC + fq
            + src_sec('신도리코 고객지원 FAQ \'프린터 드라이버는 어떻게 다운 받나요?\', \'프린터 드라이버(USB) -빠른설치-\', Microsoft 지원 \'최신 프린터 드라이버 다운로드 및 설치\'')
            + REL)
    ld = [crld, fqld, howto('신도리코 프린터 드라이버 설치 방법 (USB 빠른 설치)', ['신도리코 다운로드에서 기종 검색', '드라이버/유틸리티에서 빠른 설치 드라이버 다운로드', '압축 풀기', 'SETUP.EXE 실행 후 예', '로컬 포트를 USB로 바꾸고 설치', '테스트 페이지 인쇄로 확인'])]
    write(path, '신도리코 복합기 드라이버 바로 다운로드 — 모델별 sindoh Connect·빠른 설치 (D452·D472·N502) | 홍라이프 도구',
          '신도리코 D452·D472·D742·N502·M702 등 복합기 드라이버를 이 페이지에서 바로 받고, sindoh Connect·빠른 설치 드라이버 설치 순서를 그림으로 쉽게 확인하세요. 파일은 신도리코 공식 서버에서 내려와요.',
          main, ld)
    return path



def guide_sec(brand, zipnote=False):
    """처음 하는 분을 위한 아주 자세한 안내 (윈도우 11 기준, 사진 없이 글로만)"""
    z = ('<h3>압축 파일(.zip)을 받았다면</h3><ol class="big-n">'
         '<li>받은 <b>.zip 파일</b>을 마우스 <b>오른쪽 버튼</b>으로 눌러요.</li>'
         '<li>윈도우 기본 메뉴의 <b>[모두 압축 풀기]</b>를 누르고 <b>[압축 풀기]</b>를 눌러요. 반디집·알집을 쓰면 <b>[알아서 풀기]</b>나 <b>[여기에 풀기]</b>를 눌러도 돼요.</li>'
         '<li>새로 생긴 폴더를 열고 <b>SETUP.EXE</b>(또는 Setup, Install로 시작하는 파일)를 두 번 눌러 실행해요.</li></ol>') if zipnote else ''
    return ('<section class="card dr-sec" id="easy"><h2>처음 하는 분을 위한 아주 자세한 안내</h2>'
            '<p class="cu-ans"><b>3줄 요약</b><br>① 내 프린터 <b>모델명</b>을 확인해요. ② 이 페이지에서 내 모델의 <b>파란 버튼</b>을 눌러 파일을 받아요. ③ 받은 파일을 열고 화면이 시키는 대로 <b>[다음]</b>만 누르면 끝나요.</p>'
            '<h3>1. 내 컴퓨터가 윈도우인지 맥인지 모르겠어요</h3><ul class="cu-chk">'
            '<li>화면 왼쪽 아래(또는 가운데 아래)에 <b>창문 모양 시작 버튼</b>이 있으면 <b>윈도우</b>예요.</li>'
            '<li>화면 맨 위 왼쪽에 <b>사과 모양</b>이 있으면 <b>맥(Mac)</b>이에요.</li>'
            '<li>윈도우가 64비트인지 궁금하면 <b>설정 → 시스템 → 정보</b>에서 <b>시스템 종류</b>를 보세요. 요즘 컴퓨터는 거의 64비트예요.</li></ul>'
            f'<h3>2. 내 {E(brand)} 프린터 모델명 찾기</h3><ul class="cu-chk">'
            '<li>프린터 <b>앞면이나 윗면</b>(종이 나오는 곳 근처)에 영어와 숫자로 적혀 있어요.</li>'
            '<li>안 보이면 프린터 <b>뒷면이나 바닥의 흰 스티커</b>를 보세요. \'Model\' 또는 \'모델\' 옆에 있어요.</li>'
            '<li>예전에 설치한 적이 있다면 <b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b> 목록에 이름이 보일 수 있어요.</li>'
            '<li>검색창에는 <b>숫자 부분만</b> 넣어도 찾을 수 있어요.</li></ul>'
            '<h3>3. 다운로드는 어디로 받아져요?</h3><ul class="cu-chk">'
            '<li>파란 버튼을 누르면 크롬·엣지 오른쪽 위에 <b>아래 화살표(↓) 모양</b>이 생기고 받는 중이라고 나와요.</li>'
            '<li>다 받아지면 그 화살표를 누르거나 키보드 <b>Ctrl + J</b>를 눌러 받은 파일을 열 수 있어요.</li>'
            '<li>못 찾겠으면 <b>파일 탐색기</b>(노란 폴더 아이콘)를 열고 왼쪽의 <b>다운로드</b>를 누르세요. 가장 위에 방금 받은 파일이 있어요.</li>'
            '<li>파일이 100MB 넘게 크면 인터넷 속도에 따라 몇 분 걸려요. 끝날 때까지 창을 닫지 마세요.</li></ul>'
            + z +
            '<h3>4. 설치 화면에서 자주 나오는 버튼</h3><ul class="cu-chk">'
            '<li><b>[예]</b>: "이 앱이 디바이스를 변경할 수 있도록 허용하시겠어요?" 창이에요. 공식 파일이니 [예]를 눌러요.</li>'
            '<li><b>[동의] / [I agree]</b>: 사용 약관에 동의하는 버튼이에요. 동의해야 설치가 진행돼요.</li>'
            '<li><b>[다음] / [Next]</b>: 다음 단계로 넘어가요. 잘 모르겠으면 처음 골라져 있는 그대로 [다음]을 눌러요.</li>'
            '<li><b>[설치] / [Install]</b> → 기다리기 → <b>[마침] / [Finish]</b>: 끝났다는 뜻이에요.</li></ul>'
            '<h3>5. USB로 연결할까, 와이파이로 연결할까?</h3><ul class="cu-chk">'
            '<li><b>USB:</b> 프린터와 컴퓨터를 선으로 바로 이어요. 가장 쉽고 확실해요. 컴퓨터 한 대만 쓸 때 좋아요.</li>'
            '<li><b>와이파이(무선)·네트워크:</b> 선 없이 여러 컴퓨터·휴대폰에서 같이 쓸 수 있어요. 프린터와 컴퓨터가 <b>같은 공유기(같은 와이파이)</b>에 연결돼 있어야 해요.</li>'
            '<li>회사 복합기처럼 랜선이 꽂혀 있는 기계는 보통 <b>네트워크</b>를 골라요.</li></ul>'
            '<h3>6. 설치가 끝난 뒤</h3><ul class="cu-chk">'
            '<li><b>테스트 페이지:</b> 설정 → Bluetooth 및 장치 → 프린터 및 스캐너 → 내 프린터 → <b>[테스트 페이지 인쇄]</b>. 종이가 나오면 성공이에요.</li>'
            '<li><b>기본 프린터로 정하기:</b> 같은 화면에서 <b>[기본값으로 설정]</b>을 누르면 인쇄할 때마다 이 프린터가 먼저 골라져요. 버튼이 안 보이면 위쪽 \'Windows에서 기본 프린터 관리\'를 끄세요.</li>'
            '<li><b>\'오프라인\'이라고 나와요:</b> 프린터 전원과 선(또는 와이파이)을 확인하고, 프린터를 껐다 켠 뒤 컴퓨터도 다시 시작해 보세요.</li></ul></section>')


# ── 공통 조각 ────────────────────────────────────────────

def guide_pc(brand):
    """노트북·PC용 처음 안내 (프린터 내용 없이)"""
    return ('<section class="card dr-sec" id="easy"><h2>처음 하는 분을 위한 아주 자세한 안내</h2>'
            '<p class="cu-ans"><b>3줄 요약</b><br>① 내 제품 <b>모델명</b>을 확인해요. ② 이 페이지의 <b>파란 버튼</b>으로 공식 앱이나 파일을 받아요. ③ 앱에서 <b>업데이트 확인 → 설치</b>를 누르고, 다시 시작하라고 하면 다시 시작해요.</p>'
            '<h3>1. 내 윈도우 버전 확인하기</h3><ul class="cu-chk">'
            '<li><b>설정 → 시스템 → 정보</b>에서 <b>윈도우 사양</b>(예: Windows 11, 버전 24H2)과 <b>시스템 종류</b>(64비트)를 볼 수 있어요.</li>'
            '<li>작업표시줄 검색에 <b>winver</b>를 쳐도 버전이 나와요.</li></ul>'
            f'<h3>2. 내 {E(brand)} 제품 모델명 찾기</h3><ul class="cu-chk">'
            '<li>노트북은 <b>바닥면</b> 스티커나 새겨진 글자, 모니터는 <b>뒷면 스티커</b>를 보세요.</li>'
            '<li>윈도우 <b>설정 → 시스템 → 정보</b>에도 장치 이름이 나와요.</li></ul>'
            '<h3>3. Microsoft Store 앱 설치하기</h3><ul class="cu-chk">'
            '<li>파란 버튼을 누르면 Microsoft Store 페이지가 열려요. <b>[받기]</b> 또는 <b>[스토어 앱에서 보기]</b> → <b>[받기]</b>를 눌러요.</li>'
            '<li>설치가 끝나면 작업표시줄 검색에서 앱 이름을 쳐서 열어요.</li></ul>'
            '<h3>4. 파일(.exe)을 받았다면</h3><ul class="cu-chk">'
            '<li>키보드 <b>Ctrl + J</b>로 받은 파일을 열어요. "이 앱이 디바이스를 변경할 수 있도록 허용하시겠어요?"에는 <b>[예]</b>를 눌러요.</li>'
            '<li>설치 화면은 <b>[다음] → [설치] → [마침]</b> 순서예요.</li></ul>'
            '<h3>5. 업데이트할 때 꼭 지킬 것</h3><ul class="cu-chk">'
            '<li>노트북은 <b>충전기를 꽂고</b> 하세요.</li>'
            '<li>BIOS(바이오스)·펌웨어 업데이트 중에는 <b>절대 전원을 끄거나 덮개를 닫지 마세요</b>.</li>'
            '<li>여러 개를 설치한 뒤에는 <b>다시 시작</b>해야 적용되는 경우가 많아요.</li></ul></section>')


WIN_PC = ('<section class="card dr-sec" id="win"><h2>먼저 해 볼 것: Windows 업데이트</h2>'
          '<p>윈도우는 많은 드라이버를 Windows 업데이트로 자동으로 받아요.</p><ul class="cu-chk">'
          '<li><b>설정 → Windows 업데이트 → [업데이트 확인]</b>을 눌러요.</li>'
          '<li><b>고급 옵션 → 선택적 업데이트</b>에 드라이버 업데이트가 따로 있을 수 있어요.</li>'
          '<li>그래도 안 되면 제조사 공식 앱·사이트에서 받아요(이 페이지의 방법).</li></ul></section>')

WIN_SEC = ('<section class="card dr-sec" id="win"><h2>먼저 해 볼 것: 윈도우 자동 설치</h2>'
           '<p>요즘 윈도우는 프린터를 연결하면 드라이버를 스스로 찾아 설치하는 경우가 많아요. 제조사 사이트에 가기 전에 한 번 해 보세요.</p><ul class="cu-chk">'
           '<li><b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b>에서 <b>[장치 추가]</b>를 눌러 프린터를 추가해요.</li>'
           '<li><b>Windows 업데이트</b>로 드라이버를 받는 방법을 Microsoft가 권장해요.</li>'
           '<li>그래도 안 되면 제조사 공식 사이트에서 모델명을 검색해 윈도우 버전에 맞는 최신 소프트웨어를 받아요(이 페이지의 방법).</li></ul></section>')
REL = ('<section class="card rel"><h2>다른 회사 드라이버</h2><ul class="dr-co">'
       '<li><a href="/driver/hp.html"><b>HP</b><span>프린터·복합기 (삼성 프린터 포함)</span></a></li>'
       '<li><a href="/driver/sindoh.html"><b>신도리코</b><span>복합기 · 모델별 바로가기</span></a></li>'
       '<li><a href="/driver/epson.html"><b>엡손</b><span>정품무한 L시리즈·WorkForce</span></a></li>'
       '<li><a href="/driver/brother.html"><b>브라더</b><span>잉크젯·레이저·라벨</span></a></li>'
       '<li><a href="/driver/samsung.html"><b>삼성</b><span>갤럭시 북·모니터·USB·SSD</span></a></li>'
       '<li><a href="/driver/lg.html"><b>LG전자</b><span>그램 노트북·모니터</span></a></li>'
       '<li><a href="/driver/apple.html"><b>애플</b><span>아이폰 PC 연결·iCloud·Boot Camp</span></a></li>'
       '<li><a href="/driver/surface.html"><b>마이크로소프트 서피스</b><span>Surface 드라이버·펌웨어</span></a></li>'
       '<li><a href="/driver/lenovo.html"><b>레노버</b><span>ThinkPad·IdeaPad·Legion</span></a></li>'
       '<li><a href="/driver/dell.html"><b>델</b><span>Inspiron·XPS·Latitude</span></a></li>'
       '<li><a href="/driver/asus.html"><b>에이수스</b><span>Vivobook·Zenbook·ROG·메인보드</span></a></li>'
       '<li><a href="/driver/acer.html"><b>에이서</b><span>Aspire·Swift·Nitro</span></a></li>'
       '<li><a href="/driver/roborock.html"><b>로보락</b><span>로봇청소기 앱·펌웨어</span></a></li>'
       '<li><a href="/driver/ecovacs.html"><b>에코백스</b><span>DEEBOT 로봇청소기 앱·펌웨어</span></a></li>'
       '<li><a href="/driver/dreame.html"><b>드리미</b><span>로봇청소기 앱·펌웨어</span></a></li>'
       '<li><a href="/driver/narwal.html"><b>나르왈</b><span>Freo 로봇청소기 앱·펌웨어</span></a></li>'
       '<li><a href="/driver/wd.html"><b>웨스턴디지털</b><span>WD·샌디스크 SSD·HDD Dashboard</span></a></li>'
       '<li><a href="/driver/seagate.html"><b>씨게이트</b><span>외장하드 백업 Toolkit</span></a></li>'
       '<li><a href="/driver/crucial.html"><b>크루셜</b><span>SSD Storage Executive</span></a></li>'
       '<li><a href="/driver/synology.html"><b>시놀로지</b><span>NAS Assistant·Drive Client</span></a></li>'
       '<li><a href="/driver/qnap.html"><b>큐냅</b><span>NAS Qfinder Pro·Qsync</span></a></li>'
       '<li><a href="/driver/benq.html"><b>벤큐</b><span>모니터·프로젝터</span></a></li>'
       '<li><a href="/driver/viewsonic.html"><b>뷰소닉</b><span>모니터·프로젝터</span></a></li>'
       '<li><a href="/driver/huion.html"><b>휴이온</b><span>펜 태블릿</span></a></li>'
       '<li><a href="/driver/xppen.html"><b>엑스피펜</b><span>펜 태블릿</span></a></li>'
       '<li><a href="/driver/nvidia.html"><b>엔비디아</b><span>지포스·RTX 그래픽</span></a></li>'
       '<li><a href="/driver/amd.html"><b>AMD</b><span>라데온 그래픽·라이젠 칩셋</span></a></li>'
       '<li><a href="/driver/intel.html"><b>인텔</b><span>그래픽·칩셋·무선랜 (지원 도우미)</span></a></li>'
       '<li><a href="/driver/msi.html"><b>MSI</b><span>노트북·메인보드 MSI Center</span></a></li>'
       '<li><a href="/driver/gigabyte.html"><b>기가바이트</b><span>메인보드·그래픽카드 GCC</span></a></li>'
       '<li><a href="/driver/asrock.html"><b>애즈락</b><span>메인보드 자동 설치(ADI)</span></a></li>'
       '<li><a href="/driver/hansung.html"><b>한성컴퓨터</b><span>노트북 고객센터 다운로드</span></a></li>'
       '<li><a href="/driver/razer.html"><b>레이저</b><span>Synapse 4 마우스·키보드</span></a></li>'
       '<li><a href="/driver/canon.html"><b>캐논</b><span>PIXMA·imageCLASS·LBP</span></a></li>'
       '<li><a href="/driver/fujifilm.html"><b>후지필름</b><span>옛 후지제록스 복합기</span></a></li>'
       '<li><a href="/driver/kyocera.html"><b>교세라</b><span>TASKalfa·ECOSYS KX</span></a></li>'
       '<li><a href="/driver/ricoh.html"><b>리코</b><span>IM·MP 복합기 PCL6</span></a></li>'
       '<li><a href="/driver/logitech.html"><b>로지텍</b><span>Options+·G HUB</span></a></li>'
       '<li><a href="/driver/wacom.html"><b>와콤</b><span>펜 타블렛 드라이버</span></a></li>'
       '<li><a href="/driver/realtek.html"><b>리얼텍</b><span>랜·오디오 칩</span></a></li>'
       '<li><a href="/driver/iptime.html"><b>ipTIME</b><span>랜카드 드라이버·공유기 펌웨어</span></a></li>'
       '<li><a href="/driver/tplink.html"><b>TP-Link</b><span>무선랜카드·공유기</span></a></li>'
       '<li><a href="/driver/steelseries.html"><b>스틸시리즈</b><span>GG 마우스·헤드셋</span></a></li>'
       '<li><a href="/driver/corsair.html"><b>커세어</b><span>iCUE RGB·키보드</span></a></li>'
       '<li><a href="/driver/hyperx.html"><b>하이퍼X</b><span>NGENUITY 헤드셋</span></a></li>'
       '<li><a href="/driver/creative.html"><b>크리에이티브</b><span>사운드 블라스터</span></a></li>'
       '<li><a href="/driver/jabra.html"><b>자브라</b><span>Jabra Direct 헤드셋</span></a></li>'
       '<li><a href="/driver/epos.html"><b>에포스</b><span>EPOS Connect 헤드셋</span></a></li>'
       '<li><a href="/driver/mskb.html"><b>MS 마우스·키보드</b><span>마우스 및 키보드 센터</span></a></li>'
       '<li><a href="/driver/android.html"><b>안드로이드 USB</b><span>구글 USB·ADB</span></a></li>'
       '<li><a href="/driver/elgato.html"><b>엘가토</b><span>스트림덱·웹캠</span></a></li>'
       '<li><a href="/driver/ssd.html"><b>SSD 관리 프로그램</b><span>크루셜·킹스톤·WD</span></a></li>'
       '<li><a href="/driver/vcredist.html"><b>Visual C++ 재배포</b><span>MSVCP140.dll 오류 해결</span></a></li>'
       '<li><a href="/driver/directx.html"><b>DirectX 런타임</b><span>d3dx9·XINPUT 오류 해결</span></a></li>'
       '<li><a href="/driver/dotnet.html"><b>.NET 런타임</b><span>.NET 필요 오류 해결</span></a></li>'
       '<li><a href="/driver/xbox.html"><b>Xbox 컨트롤러</b><span>엑박 패드 PC 연결</span></a></li>'
       '<li><a href="/driver/"><b>드라이버 모음 전체</b><span>회사별·기기별로 찾기</span></a></li></ul></section>')


def src_sec(s):
    return (f'<section class="card"><h2>출처와 안내</h2><p class="cu-src">출처: {E(s)} · 확인 {CHECKED}.<br>'
            '홍라이프 도구는 드라이버 파일을 직접 올리지 않아요. 모든 다운로드는 제조사 공식 사이트에서 이루어져요. '
            '그림은 이해를 돕기 위해 단순하게 그린 것이라 실제 화면과 다를 수 있어요.</p></section>')


def howto(name, names):
    return {"@context": "https://schema.org", "@type": "HowTo", "name": name,
            "step": [{"@type": "HowToStep", "position": i + 1, "name": n} for i, n in enumerate(names)]}


# ── 허브 ────────────────────────────────────────────────
EXT = []


def hub():
    path = '/driver/'
    cr = '<p class="crumb"><a href="/">홈</a> › 드라이버</p>'
    crld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + '/'}, {"@type": "ListItem", "position": 2, "name": "드라이버", "item": SITE + path}]}
    import driver_more as dm
    allm = [(n, u) for n, u in dm.ep_hub_items()] + [(n, u) for n, u in dm.br_hub_items()] + [(m['n'], '/driver/hp.html#' + mid(m['n'])) for m in HP_DATA['models']] + [(m, '/driver/sindoh.html#m-' + re.sub(r'[^A-Za-z0-9]', '', m)) for m, _ in SD_MODELS] + [(m, '/driver/amd.html#m-' + re.sub(r'[^A-Za-z0-9]', '', m)) for m, _, _ in AMD_MODELS]
    data = json.dumps(allm, ensure_ascii=False)
    co = ('<li><a href="/driver/hp.html"><b>HP</b><span>프린터·복합기, 삼성 프린터 포함</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/sindoh.html"><b>신도리코</b><span>복합기, 모델별 다운로드 바로가기</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/nvidia.html"><b>엔비디아</b><span>지포스·RTX 그래픽카드</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/amd.html"><b>AMD</b><span>라데온 그래픽·라이젠 칩셋</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/intel.html"><b>인텔</b><span>그래픽·칩셋·무선랜</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/epson.html"><b>엡손</b><span>정품무한 L시리즈·WorkForce 등 모델별 바로 받기</span><em>모델별 바로 받기 ›</em></a></li>'
          '<li><a href="/driver/brother.html"><b>브라더</b><span>잉크젯·레이저·라벨 모델별 바로 받기</span><em>모델별 바로 받기 ›</em></a></li>'
          '<li><a href="/driver/samsung.html"><b>삼성</b><span>갤럭시 북 노트북·모니터·갤럭시 USB·SSD·프린터</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/lg.html"><b>LG전자</b><span>그램 노트북 LG Update·모니터 OnScreen Control, 모델별 파일</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/apple.html"><b>애플</b><span>윈도우에서 아이폰 연결(Apple 기기 앱)·iCloud·Boot Camp</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/surface.html"><b>마이크로소프트 서피스</b><span>Surface Pro·Laptop·Go 모델별 드라이버·펌웨어</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/lenovo.html"><b>레노버</b><span>ThinkPad·IdeaPad·Legion 노트북·PC 드라이버 공식 프로그램</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/dell.html"><b>델</b><span>Inspiron·XPS·Latitude 노트북·PC 드라이버 공식 프로그램</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/asus.html"><b>에이수스</b><span>Vivobook·Zenbook·ROG·메인보드 노트북·PC 드라이버 공식 프로그램</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/acer.html"><b>에이서</b><span>Aspire·Swift·Nitro 노트북·PC 드라이버 공식 프로그램</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/roborock.html"><b>로보락</b><span>로봇청소기 Roborock 앱·펌웨어 업데이트</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/ecovacs.html"><b>에코백스</b><span>DEEBOT 로봇청소기 ECOVACS HOME 앱·펌웨어 업데이트</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/dreame.html"><b>드리미</b><span>로봇청소기 Dreamehome 앱·펌웨어 업데이트</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/narwal.html"><b>나르왈</b><span>Freo 로봇청소기 Narwal 앱·펌웨어 업데이트</span><em>그림 설명 ›</em></a></li>'
          '<li><a href="/driver/wd.html"><b>웨스턴디지털</b><span>WD·샌디스크 SSD·HDD Dashboard</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/seagate.html"><b>씨게이트</b><span>외장하드 백업 Toolkit</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/crucial.html"><b>크루셜</b><span>SSD Storage Executive</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/synology.html"><b>시놀로지</b><span>NAS Assistant·Drive Client</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/qnap.html"><b>큐냅</b><span>NAS Qfinder Pro·Qsync</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/benq.html"><b>벤큐</b><span>모니터·프로젝터</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/viewsonic.html"><b>뷰소닉</b><span>모니터·프로젝터</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/huion.html"><b>휴이온</b><span>펜 태블릿</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/xppen.html"><b>엑스피펜</b><span>펜 태블릿</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/msi.html"><b>MSI</b><span>노트북·메인보드·그래픽카드·모니터</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/gigabyte.html"><b>기가바이트</b><span>메인보드·그래픽카드·AORUS 노트북</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/asrock.html"><b>애즈락</b><span>메인보드·그래픽카드</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/hansung.html"><b>한성컴퓨터</b><span>노트북·데스크톱·모니터</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/razer.html"><b>레이저</b><span>마우스·키보드·헤드셋·Blade 노트북</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/canon.html"><b>캐논</b><span>PIXMA 잉크젯·imageCLASS·LBP 레이저</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/fujifilm.html"><b>후지필름</b><span>Apeos·ApeosPort·DocuPrint 복합기·프린터</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/kyocera.html"><b>교세라</b><span>TASKalfa 복합기·ECOSYS 프린터</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/ricoh.html"><b>리코</b><span>IM·MP 복합기·SP 프린터</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/logitech.html"><b>로지텍</b><span>마우스·키보드·웹캠·Logitech G</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/wacom.html"><b>와콤</b><span>Intuos·Cintiq·Wacom One 펜 타블렛</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/realtek.html"><b>리얼텍</b><span>랜카드(이더넷)·오디오·카드리더 칩</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/iptime.html"><b>ipTIME</b><span>공유기·USB 무선랜카드(A3000UA 등)</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/tplink.html"><b>TP-Link</b><span>USB 무선랜카드(Archer T·TX)·공유기</span><em>공식 다운로드 ›</em></a></li>'
          '<li><a href="/driver/steelseries.html"><b>스틸시리즈</b><span>게이밍 마우스·키보드·헤드셋(Arctis)</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/corsair.html"><b>커세어</b><span>게이밍 키보드·마우스·헤드셋·RGB 팬·쿨러</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/hyperx.html"><b>하이퍼X</b><span>게이밍 헤드셋·마우스·키보드</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/creative.html"><b>크리에이티브</b><span>사운드 블라스터·스피커·헤드셋</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/jabra.html"><b>자브라</b><span>업무용 헤드셋·스피커폰·이어버드</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/epos.html"><b>에포스</b><span>업무용·게이밍 헤드셋(옛 젠하이저 커뮤니케이션)</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/mskb.html"><b>MS 마우스·키보드</b><span>마이크로소프트 마우스·키보드(Ergonomic·Sculpt 등)</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/android.html"><b>안드로이드 USB</b><span>구글 픽셀·안드로이드 폰 PC 연결·ADB</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/elgato.html"><b>엘가토</b><span>스트림덱·웹캠·캡처보드</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/ssd.html"><b>SSD 관리 프로그램</b><span>크루셜·킹스톤·WD·씨게이트 SSD·HDD 펌웨어·상태 검사</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/vcredist.html"><b>Visual C++ 재배포</b><span>MSVCP140.dll·VCRUNTIME140.dll 오류 해결</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/directx.html"><b>DirectX 런타임</b><span>d3dx9_43.dll·XINPUT1_3.dll 오류 해결</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/dotnet.html"><b>.NET 런타임</b><span>&quot;.NET이 필요합니다&quot; 오류 해결</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/driver/xbox.html"><b>Xbox 컨트롤러</b><span>엑스박스 패드 PC 연결·무선 어댑터·펌웨어</span><em>바로 받기 ›</em></a></li>'
          '<li><a href="/drive/update/tesla.html"><b>테슬라</b><span>차량 소프트웨어 무선 업데이트 방법</span><em>그림 설명 ›</em></a></li>'
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
            '<p class="lead">프린터·복합기와 그래픽카드 드라이버를 회사별로 모아, 공식 사이트에서 받는 방법과 설치 순서를 그림으로 쉽게 정리했어요. 회사와 기기는 계속 늘려요.</p>'
            '<p class="cu-ans">① 기기 <b>모델명</b>을 확인하고 → ② 아래에서 <b>회사</b>를 고른 뒤 → ③ 파란 <b>[다운로드]</b> 버튼으로 공식 사이트에서 받아 → ④ 그림 순서대로 설치하세요. '
            '파일은 모두 제조사 공식 사이트에서 받아요.</p>'
            '<form class="dr-q" onsubmit="return drH()"><input id="dr-in" placeholder="모델명 검색 (예: 8210, D452)" autocomplete="off" oninput="drH()" aria-label="모델명 검색"><button type="submit">찾기</button></form><ul id="dr-res"></ul>'
            f'<script>var DRA={data};function drH(){{var q=document.getElementById("dr-in").value.replace(/\\s/g,"").toUpperCase(),r=document.getElementById("dr-res");if(!q){{r.innerHTML="";return false}}'
            'var h=DRA.filter(function(x){return x[0].toUpperCase().indexOf(q)>=0}).slice(0,8);r.innerHTML=h.length?h.map(function(x){return\'<li><a href="\'+x[1]+\'">\'+x[0]+\' 드라이버 받기 ›</a></li>\'}).join(""):'
            '"<li>아직 모델 표에 없는 모델이에요. 아래에서 회사를 고르면 공식 사이트에서 모델명으로 찾을 수 있어요.</li>";return false}</script></header>'
            f'<section class="card"><h2>회사 고르기</h2><ul class="dr-co">{co}</ul>'
            '</section>'
            f'<section class="card"><h2>시작 전에 알아 두기</h2>{what}{name}</section>'
            + WIN_SEC
            + '<section class="card"><h2>가짜 드라이버 사이트 조심하기</h2><p class="dr-warn">검색 광고에 나오는 \'드라이버 자동 설치\' 프로그램이나 블로그에 올라온 설치 파일은 받지 마세요. '
              '원치 않는 프로그램이나 광고가 함께 깔릴 수 있어요. <b>제조사 공식 사이트</b>나 <b>Windows 업데이트</b>에서 받는 게 가장 안전해요.</p></section>'
            + fq + src_sec('각 제조사 공식 고객지원 안내, Microsoft 지원 \'최신 프린터 드라이버 다운로드 및 설치\''))
    write(path, '드라이버 다운로드 모음 — 프린터·그래픽카드 드라이버 설치 방법 (HP·삼성·신도리코·엔비디아·AMD·인텔) | 홍라이프 도구',
          '프린터·복합기와 그래픽카드 드라이버를 회사별로 모아 공식 사이트에서 받는 방법과 설치 순서를 그림으로 쉽게 정리했어요. 모델명 찾는 법, 윈도우 자동 설치, 가짜 드라이버 사이트 주의, HP·삼성·신도리코·엔비디아·AMD·인텔·캐논·엡손·브라더.',
          main, [crld, fqld])
    return path


# ── 그래픽·칩셋 3사 (공식 페이지 2026-11-22 확인) ─────────────
def W_select(url, title, rows, button, n=2):
    t = f'<text x="44" y="58" font-size="12.5" font-weight="800" fill="#111">{E(title)}</text>'
    y = 66
    for a in rows:
        t += f'<rect x="44" y="{y}" width="170" height="20" rx="4" fill="#fff" stroke="#ADB5BD"/><text x="52" y="{y + 14}" font-size="9.5" fill="#333">{E(a)} ▾</text>'
        y += 24
    return pc(t + btn(222, y - 26, 66, 24, button) + ring(44, 66, 170, y - 70, n) + ring(222, y - 26, 66, 24, n + 1), url)


def W_devmgr(n=1):
    return pc('<text x="44" y="60" font-size="12.5" font-weight="800" fill="#111">장치 관리자</text>'
              '<text x="52" y="82" font-size="10.5" fill="#333">› 네트워크 어댑터</text>'
              '<text x="52" y="102" font-size="10.5" font-weight="800" fill="#1D4ED8">⌄ 디스플레이 어댑터</text>'
              '<rect x="64" y="110" width="190" height="22" rx="4" fill="#EEF4FF"/><text x="72" y="125" font-size="10" fill="#111">내 그래픽카드 이름이 여기 보여요</text>'
              + ring(64, 110, 190, 22, n) + '<text x="52" y="152" font-size="10.5" fill="#333">› 마우스 및 기타 포인팅 장치</text>', '시작 버튼 오른쪽 클릭 → 장치 관리자')


def gpu_name_step(n):
    return cu.step(n, '내 그래픽카드 이름 확인', '<b>시작 버튼을 마우스 오른쪽으로 누르고 → 장치 관리자 → 디스플레이 어댑터</b>를 펼치면 그래픽카드 이름이 나와요. 노트북은 두 개(인텔 + 엔비디아 등)가 보일 수 있어요.', W_devmgr())


NV_DRV = 'https://www.nvidia.com/ko-kr/geforce/drivers/'


def nvidia():
    path = '/driver/nvidia.html'
    cr, crld = crumb([('엔비디아 드라이버', '')])
    ans = ('엔비디아(NVIDIA) 그래픽 드라이버는 <b>NVIDIA 공식 드라이버 페이지</b>에서 받아요. <b>제품 범주 → 제품 시리즈 → 제품 → 운영 체제</b>를 고르고 <b>[Find Drivers]</b>를 누른 뒤 <b>[다운로드]</b>하면 돼요. '
           '매번 찾기 귀찮다면 <b>NVIDIA App</b>을 깔면 새 드라이버가 나올 때 알림을 받고 바로 업데이트할 수 있어요.')
    steps = (gpu_name_step(1)
             + cu.step(2, '드라이버 페이지에서 내 제품 고르기', 'NVIDIA 드라이버 페이지의 수동 검색에서 <b>제품 범주, 제품 시리즈, 제품, 운영 체제, 언어, 다운로드 유형</b>을 차례로 고르고 <b>[Find Drivers]</b>를 눌러요.',
                       W_select('nvidia.com', '수동 드라이버 검색', ['제품 범주', '제품 시리즈', '제품', '운영 체제', '다운로드 유형'], 'Find Drivers'),
                       '다운로드 유형: 게임을 주로 하면 <b>Game Ready</b>, 영상 편집·디자인 프로그램을 주로 쓰면 <b>Studio</b>를 고르세요.')
             + cu.step(4, '다운로드하고 실행', '결과에서 <b>[다운로드]</b>를 누르고, 받은 파일을 Ctrl + J로 열어 실행해요.', W_downloads('NVIDIA_드라이버.exe', 4))
             + cu.step(5, '\'예\' 누르고 설치', '윈도우 확인 창에서 <b>[예]</b>를 누르고, 설치 프로그램 안내대로 진행해요. 설치 중 화면이 잠깐 깜빡이는 건 정상이에요.', W_uac('NVIDIA 설치 프로그램', 5)))
    app = ('<section class="card dr-sec" id="app"><h2>자동으로 받기: NVIDIA App</h2>'
           '<p>NVIDIA 공식 안내에 따르면 NVIDIA App을 설치하면 <b>새 드라이버가 나올 때 자동 알림</b>을 받고, <b>클릭 한 번으로 바로 업데이트</b>할 수 있어요.</p>'
           + dl(NV_DRV, 'NVIDIA App·드라이버 받기', 'NVIDIA 공식 드라이버 페이지') + '</section>')
    qa = [('Game Ready와 Studio 드라이버는 뭐가 달라요?', 'NVIDIA 안내에 따르면 Game Ready는 주요 게임에, Studio는 주요 크리에이티브(영상·디자인) 앱에 맞춰진 드라이버예요. 잘 모르겠으면 평소 많이 하는 쪽을 고르세요.'),
          ('내 그래픽카드가 엔비디아인지 어떻게 알아요?', '시작 버튼 오른쪽 클릭 → 장치 관리자 → 디스플레이 어댑터에서 이름을 보세요. GeForce, RTX, GTX 같은 이름이면 엔비디아예요.'),
          ('드라이버는 무료인가요?', '네. NVIDIA 공식 사이트의 드라이버는 무료예요.'),
          ('리눅스는요?', 'NVIDIA 안내에 따르면 리눅스는 배포판이 제공하는 패키지를 쓰는 걸 권장해요.')]
    fq, fqld = cu.faq(qa)
    main = (f'<header class="top hub">{cr}<h1>엔비디아(NVIDIA) 그래픽 드라이버 다운로드·설치 방법</h1>'
            '<p class="lead">지포스(GeForce)·RTX 그래픽카드 드라이버를 공식 사이트에서 받아 설치하는 순서를 그림으로 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{ans}</p>' + dl(NV_DRV, '엔비디아 드라이버 받으러 가기', 'NVIDIA 공식 드라이버 페이지')
            + '<ul class="dr-toc"><li><a href="#steps">설치 순서</a></li><li><a href="#app">자동 업데이트</a></li></ul></header>'
            f'<section class="card dr-sec" id="steps"><h2>그림으로 보는 설치 순서</h2>{steps}</section>' + app + fq
            + src_sec('NVIDIA 공식 드라이버 페이지(nvidia.com/ko-kr/geforce/drivers), Microsoft 지원') + REL)
    write(path, '엔비디아(NVIDIA) 그래픽 드라이버 다운로드·설치 방법 (Game Ready·Studio, 2026) | 홍라이프 도구',
          '엔비디아 지포스·RTX 그래픽 드라이버를 공식 사이트에서 받아 설치하는 방법을 그림으로 쉽게 설명해요. 내 그래픽카드 확인, 수동 검색, Game Ready와 Studio 차이, NVIDIA App 자동 업데이트까지.',
          main, [crld, fqld, howto('엔비디아 그래픽 드라이버 설치 방법', ['장치 관리자에서 그래픽카드 확인', '드라이버 페이지에서 제품 선택 후 Find Drivers', '다운로드 후 실행', '예를 누르고 설치'])])
    return path


AMD_RX = 'https://www.amd.com/ko/support/downloads/drivers.html/graphics/radeon-rx/radeon-rx-6000-series/amd-radeon-rx-6600.html'
AMD_MODELS = [('Radeon RX 9000 Series', '그래픽카드 시리즈', 'https://www.amd.com/ko/support/downloads/drivers.html/graphics/radeon-rx/radeon-rx-9000-series.html'),
              ('Radeon RX 6750 GRE 12GB', '그래픽카드', 'https://www.amd.com/ko/support/downloads/drivers.html/graphics/radeon-rx/radeon-rx-6000-series/amd-radeon-rx-6750-gre-12gb.html'),
              ('Radeon RX 6600', '그래픽카드', AMD_RX),
              ('Radeon RX 6300M', '노트북 그래픽', 'https://www.amd.com/ko/support/downloads/drivers.html/graphics/radeon-rx/radeon-rx-6000-series/amd-radeon-rx-6300m.html'),
              ('Radeon R9 285', '그래픽카드 (구형)', 'https://www.amd.com/ko/support/downloads/drivers.html/graphics/radeon-r9-r7-r5/radeon-r9-200-series/amd-radeon-r9-285.html'),
              ('Radeon R9 M375X', '노트북 그래픽 (구형)', 'https://www.amd.com/ko/support/downloads/drivers.html/graphics/radeon-r9-r7-r5/radeon-r9-300-series/amd-radeon-r9-m375x.html'),
              ('Ryzen·Athlon 모바일 칩셋', '노트북 칩셋', 'https://amd.com/ko/support/downloads/drivers.html/chipsets/laptop-chipsets/amd-ryzen-and-athlon-mobile-chipset.html')]


def amd():
    path = '/driver/amd.html'
    cr, crld = crumb([('AMD 드라이버', '')])
    ans = ('AMD 라데온(Radeon) 그래픽 드라이버는 <b>AMD 공식 다운로드 페이지</b>에서 받아요. 가장 쉬운 방법은 <b>Auto-Detect and Install(자동 감지 및 설치)</b> 도구예요. '
           '실행하면 <b>내 그래픽카드와 윈도우 버전을 알아서 찾아</b> 맞는 최신 공식 드라이버를 받아 설치해 줘요. 직접 고르려면 내 제품 페이지에서 <b>AMD Software: Adrenalin Edition</b>을 받으면 돼요.')
    steps = (gpu_name_step(1)
             + cu.step(2, 'Auto-Detect and Install 받기', 'AMD 드라이버 페이지의 Windows 10·11 칸에서 <b>[Download Auto-Detect and Install]</b>을 눌러요. 작은 프로그램(약 46MB)이라 금방 받아져요.',
                       W_list('amd.com', 'Windows 11 · Windows 10', [('Auto-Detect and Install (자동 감지)', '다운로드'), ('AMD Software: Adrenalin Edition', '다운로드')], 0, 2),
                       '인터넷이 연결돼 있어야 해요. 그래픽카드와 윈도우 버전을 감지해 맞는 드라이버를 받아 줘요.')
             + cu.step(3, '실행하고 \'예\'', '받은 파일을 Ctrl + J로 열어 실행하고, 윈도우 확인 창에서 <b>[예]</b>를 눌러요.', W_uac('AMD 설치 프로그램', 3))
             + cu.step(4, '안내대로 설치', '도구가 맞는 드라이버를 찾아 주면 화면 안내대로 설치해요. 다시 시작하라고 하면 컴퓨터를 다시 시작해요.',
                       W_installer('AMD Software 설치', ['그래픽카드를 찾았어요', '맞는 드라이버를 설치할게요'], '설치', 4)))
    qa = [('Auto-Detect와 Adrenalin Edition은 뭐가 달라요?', 'Auto-Detect and Install은 내 그래픽카드와 윈도우 버전을 찾아 맞는 드라이버를 받아 주는 작은 도구예요. AMD Software: Adrenalin Edition은 드라이버와 관리 프로그램이 들어 있는 본 설치 파일이에요. 모르겠으면 Auto-Detect를 쓰세요.'),
          ('윈도우 7도 되나요?', '일부 그래픽카드는 윈도우 7용 드라이버가 있지만, AMD는 이를 추가 출시 계획이 없는 레거시 지원으로 안내해요. 가능하면 윈도우 10·11을 쓰세요.'),
          ('라이젠 칩셋 드라이버는 어디서 받아요?', 'AMD 다운로드 페이지의 칩셋(Chipsets) 항목에서 받아요. 위 표의 \'Ryzen·Athlon 모바일 칩셋\'이 노트북용이에요. 데스크톱은 메인보드 회사 사이트에서도 받을 수 있어요.')]
    fq, fqld = cu.faq(qa)
    main = (f'<header class="top hub">{cr}<h1>AMD 라데온 그래픽·칩셋 드라이버 다운로드·설치 방법</h1>'
            '<p class="lead">AMD 라데온 그래픽카드와 라이젠 칩셋 드라이버를 공식 사이트에서 받아 설치하는 순서를 그림으로 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{ans}</p>' + dl(AMD_RX, 'AMD 드라이버 받으러 가기', 'AMD 공식 다운로드 페이지 (Auto-Detect 포함)')
            + '<ul class="dr-toc"><li><a href="#models">제품별 바로가기</a></li><li><a href="#steps">설치 순서</a></li></ul></header>'
            '<section class="card dr-sec" id="models"><h2>제품별 다운로드 바로가기</h2>' + model_search([m for m, _, _ in AMD_MODELS])
            + models_table(AMD_MODELS) + '<p class="cu-src" style="margin-top:8px">다른 제품도 AMD 다운로드 페이지에서 그래픽 → 제품군 → 시리즈 → 제품 순으로 찾을 수 있어요. 어느 제품 페이지에서든 Auto-Detect and Install을 받을 수 있어요.</p></section>'
            f'<section class="card dr-sec" id="steps"><h2>그림으로 보는 설치 순서 (자동 감지)</h2>{steps}</section>' + fq
            + src_sec('AMD 공식 드라이버 및 다운로드 페이지(amd.com/ko/support/downloads)') + REL)
    write(path, 'AMD 라데온 그래픽·라이젠 칩셋 드라이버 다운로드·설치 방법 (Auto-Detect, 2026) | 홍라이프 도구',
          'AMD 라데온 그래픽 드라이버와 라이젠 칩셋 드라이버를 공식 사이트에서 받아 설치하는 방법을 그림으로 쉽게 설명해요. Auto-Detect and Install 자동 감지, Adrenalin Edition, 제품별 바로가기.',
          main, [crld, fqld, howto('AMD 그래픽 드라이버 설치 방법', ['장치 관리자에서 그래픽카드 확인', 'Auto-Detect and Install 다운로드', '실행 후 예', '안내대로 설치'])])
    return path


INTEL_DSA = 'https://intel.co.kr/content/www/kr/ko/support/detect.html'


def intel():
    path = '/driver/intel.html'
    cr, crld = crumb([('인텔 드라이버', '')])
    ans = ('인텔 그래픽·칩셋·무선랜 같은 인텔 부품 드라이버는 <b>인텔 드라이버 및 지원 도우미</b>로 한 번에 챙기는 게 가장 쉬워요. '
           '인텔 공식 페이지에서 받아 <b>화면 안내대로 설치</b>하고 <b>지원 도우미를 실행</b>하면, 내 컴퓨터의 인텔 하드웨어에 맞는 드라이버·소프트웨어 업데이트를 알려 줘요.')
    check = cu.step('!', '내 컴퓨터에 인텔 부품이 있는지 확인', '<b>시작 버튼 오른쪽 클릭 → 장치 관리자</b>에서 <b>디스플레이 어댑터</b>(그래픽), <b>네트워크 어댑터</b>(무선랜), <b>Bluetooth</b> 항목을 펼쳐 보세요. 이름에 <b>Intel</b>이 들어 있으면 이 페이지 방법으로 업데이트할 수 있어요.', W_devmgr())
    steps = (cu.step(1, '지원 도우미 받기', '아래 <b>[인텔 지원 도우미 받으러 가기]</b>를 눌러 인텔 공식 페이지에서 \'인텔 드라이버 및 지원 도우미\'를 내려받아요.',
                     W_list('intel.co.kr', '인텔® 드라이버 및 지원 도우미', [('맞춤 지원과 편리한 업데이트', ''), ('드라이버 및 소프트웨어 다운로드', '다운로드')], 1, 1))
             + cu.step(2, '설치하기', '받은 파일을 실행하고 <b>화면에 나오는 안내에 따라</b> 설치해요. 윈도우 확인 창이 뜨면 [예]를 눌러요.', W_uac('Intel Driver & Support Assistant', 2))
             + cu.step(3, '지원 도우미 실행 → 업데이트', '지원 도우미를 실행하면 <b>내 인텔 하드웨어에 맞는 드라이버와 소프트웨어 업데이트</b>가 목록으로 나와요. 필요한 것만 받아 설치하세요.',
                       W_list('intel.co.kr', '내 컴퓨터 · 업데이트 목록', [('그래픽 드라이버', '다운로드'), ('무선(Wi-Fi) 드라이버', '다운로드'), ('블루투스', '다운로드')], 0, 3)))
    note = ('<section class="card"><h2>노트북이라면 먼저 확인하세요</h2><p>삼성·LG·레노버 같은 노트북은 노트북 회사가 맞춰 둔 드라이버가 따로 있어요. '
            '인텔 최신 드라이버가 노트북 회사 버전과 다를 수 있으니, 문제가 생기면 노트북 회사 지원 페이지의 드라이버를 쓰세요.</p></section>')
    qa = [('인텔 드라이버 및 지원 도우미는 뭐예요?', '인텔 안내에 따르면 대부분의 인텔 하드웨어를 위해 맞춤 지원과 편리한 업데이트를 제공하는 프로그램이에요.'),
          ('무료인가요?', '네. 인텔 공식 사이트에서 무료로 받아요.'),
          ('무선 인터넷(와이파이)이 자꾸 끊겨요.', '장치 관리자 → 네트워크 어댑터에 Intel 무선 장치가 있다면 지원 도우미로 무선 드라이버를 최신으로 바꿔 보세요. 노트북이면 노트북 회사 지원 페이지의 무선 드라이버도 함께 확인하세요.'),
          ('화면이 깨지거나 해상도가 이상해요.', '그래픽 드라이버가 오래됐거나 윈도우 기본 드라이버로 잡혀 있을 수 있어요. 장치 관리자 → 디스플레이 어댑터 이름을 확인하고, 인텔이면 지원 도우미로 그래픽 드라이버를 업데이트하세요.'),
          ('업데이트가 하나도 안 나와요.', '이미 최신이거나, 노트북 회사가 드라이버를 따로 관리하는 경우일 수 있어요. 노트북이면 노트북 회사 지원 페이지도 확인하세요.')]
    fq, fqld = cu.faq(qa)
    main = (f'<header class="top hub">{cr}<h1>인텔 드라이버 다운로드 — 드라이버 및 지원 도우미 설치 방법</h1>'
            '<p class="lead">인텔 그래픽·칩셋·무선랜·블루투스 드라이버를 한 번에 확인하고 업데이트하는 방법을 그림으로 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{ans}</p>' + dl(INTEL_DSA, '인텔 지원 도우미 받으러 가기', '인텔 공식 페이지 (드라이버 및 지원 도우미)')
            + f'<ul class="dr-toc"><li><a href="#check">인텔 부품 확인</a></li><li><a href="#steps">설치 순서</a></li></ul></header><section class="card dr-sec" id="check"><h2>먼저 확인하기</h2>{check}</section><section class="card dr-sec" id="steps"><h2>그림으로 보는 순서</h2>{steps}</section>'
            + note + fq + src_sec('인텔 공식 \'인텔® 드라이버 및 지원 도우미\' 페이지(intel.co.kr)') + REL)
    write(path, '인텔 드라이버 다운로드 — 드라이버 및 지원 도우미 설치·업데이트 방법 (2026) | 홍라이프 도구',
          '인텔 그래픽·칩셋·무선랜·블루투스 드라이버를 인텔 드라이버 및 지원 도우미로 한 번에 업데이트하는 방법을 그림으로 쉽게 설명해요.',
          main, [crld, fqld, howto('인텔 드라이버 및 지원 도우미 사용 방법', ['지원 도우미 다운로드', '화면 안내대로 설치', '지원 도우미 실행 후 업데이트'])])
    return path


if __name__ == '__main__':
    print('\n'.join([hub(), hp(), sindoh(), nvidia(), amd(), intel()]))
