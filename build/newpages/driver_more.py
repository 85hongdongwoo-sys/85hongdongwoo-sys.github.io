"""엡손·브라더 드라이버 페이지 (한국어 + 영어)
데이터: data/epson_models.json, data/brother_models.json (2026-11-22 공식 사이트에서 수집)
- 엡손: epson.co.kr 고객지원 제품 페이지의 다운로드 탭 링크 (download.ebz.epson.net / my.epson.co.kr)
- 브라더: support.brother.com (c=kr, lang=ko) 윈도우 11 다운로드 목록. 받기 전 브라더 사용권(EULA) 동의 화면을 반드시 거침.
"""
import json, os, re, sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en

E = cu.E
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
EP = json.load(open(os.path.join(D, 'epson_models.json'), encoding='utf-8'))
BR = json.load(open(os.path.join(D, 'brother_models.json'), encoding='utf-8'))
DL = kr.DLICON

CSS = ('<style>.mg{border:1px solid var(--line-s,#E3E7EE);border-radius:14px;margin:10px 0;background:#fff}'
       '.mg>summary{cursor:pointer;padding:13px 14px;font-weight:800;font-size:16px;list-style:none;display:flex;justify-content:space-between;gap:8px}'
       '.mg>summary::-webkit-details-marker{display:none}.mg>summary span{font-weight:600;font-size:13px;color:var(--muted,#5B6B82);flex:none}'
       '.mg>summary:after{content:"▾";color:#1D4ED8;flex:none}.mg[open]>summary:after{content:"▴"}'
       '.ml{list-style:none;margin:0;padding:0 12px 6px}.mr{padding:12px 2px;border-top:1px dashed var(--line-s,#E3E7EE);scroll-margin-top:80px}'
       '.mr:target{background:#F2F7FF;border-radius:10px;padding:12px 8px}'
       '.mr h3{margin:0 0 6px;font-size:16px;line-height:1.4;word-break:keep-all}.mr .bt{display:flex;flex-wrap:wrap;gap:6px}'
       '.mb{display:inline-flex;flex-direction:column;justify-content:center;padding:9px 13px;border-radius:12px;background:var(--acc,#1B64DA);color:#fff!important;text-decoration:none;max-width:100%;box-sizing:border-box;min-height:44px}'
       '.mb:hover{background:var(--acc-d,#1957C2)}.mb b{font-size:14.5px;word-break:keep-all}.mb small{font-size:12px;opacity:.92;word-break:keep-all}'
       '.mb.s{background:var(--acc-soft,#EAF2FE);color:var(--acc,#1B64DA)!important}.mb.s:hover{background:var(--acc-line,#C9E2FF)}'
       '.mr .of{display:inline-block;margin-top:6px;font-size:13px;font-weight:700;color:#1D4ED8}'
       '.nm{display:flex;flex-wrap:wrap;gap:6px;list-style:none;padding:0;margin:8px 0 0}.nm a{display:inline-block;padding:6px 10px;border-radius:999px;background:#F1F3F5;color:#333;font-size:13px;text-decoration:none}'
       '@media(max-width:640px){.mb{width:100%}}</style>')


# ── 공통 도우미 ─────────────────────────────────────────
def ep_url(enc):
    if enc.count('|') == 2 and not enc.startswith('http'):
        cti, prn, osc = enc.split('|')
        return f'https://download.ebz.epson.net/dsc/du/02/DriverDownloadInfo.do?LG2=KO&CN2=KR&CTI={cti}&PRN={quote(prn)}&OSC={osc}'
    return enc


def ep_meta(s):
    parts = [p.strip().replace('\xa0', ' ') for p in s.split(' / ') if p.strip()]
    date = next((p for p in parts if re.match(r'\d{4}/\d{2}/\d{2}$', p)), '')
    size = next((p for p in parts if re.search(r'\d\s?(MB|KB|GB)$', p)), '')
    return date, size


def ep_id(code):
    return 'e-' + code


def br_url(prod, os_, enc):
    dlid, flang, t3 = enc.split('|')
    return f'https://support.brother.com/g/b/downloadend.aspx?c=kr&lang=ko&prod={prod}&os={os_}&dlid={dlid}&flang={flang}&type3={t3}'


def br_id(prod):
    return 'b-' + re.sub(r'[^a-z0-9]', '', prod)


def search_js(var, data, ph, miss, label):
    return (f'<form class="dr-q" onsubmit="return {var}()"><input id="dr-in" placeholder="{E(ph)}" autocomplete="off" oninput="{var}()" aria-label="model search"><button type="submit">{E(label)}</button></form><ul id="dr-res"></ul>'
            f'<script>var {var}D={json.dumps(data, ensure_ascii=False)};function {var}(){{var q=document.getElementById("dr-in").value.replace(/[\\s-]/g,"").toUpperCase(),r=document.getElementById("dr-res");if(!q){{r.innerHTML="";return false}}'
            f'var h={var}D.filter(function(x){{return x[0].replace(/[\\s-]/g,"").toUpperCase().indexOf(q)>=0}}).slice(0,10);'
            'r.innerHTML=h.length?h.map(function(x){return\'<li><a href="\'+x[1]+\'" onclick="var e=document.querySelector(\\\'\'+x[1]+\'\\\');if(e){var d=e.closest(\\\'details\\\');if(d)d.open=true}">\'+x[0]+\' ›</a></li>\'}).join(""):'
            f'"<li>{miss}</li>";return false}}</script>'
            '<script>window.addEventListener("load",function(){var h=location.hash&&document.querySelector(location.hash);if(h){var d=h.closest("details");if(d){d.open=true;h.scrollIntoView()}}})</script>')


# ── 엡손 데이터 정리 ────────────────────────────────────
EP_LABEL = {'W': ('드라이버+프로그램 한 번에', 'Driver + utilities (web installer)'),
            'P': ('프린터 드라이버만', 'Printer driver only'),
            'S': ('스캐너 드라이버', 'Scanner driver')}


def ep_groups():
    g = {}
    for ci, name, code, items in EP['m']:
        g.setdefault(EP['cats'][ci], []).append((name, code, items))
    return g


def ep_btns(items, lang='ko'):
    out = []
    for i, (t, meta, enc) in enumerate(items):
        url = ep_url(enc)
        direct = 'my.epson.co.kr' in url
        date, size = ep_meta(meta)
        lab = EP_LABEL.get(t, (t, t))[0 if lang == 'ko' else 1]
        if lang == 'ko':
            sub = ('누르면 바로 다운로드' if direct else '엡손 다운로드 창 열림') + (f' · {size}' if size else '') + (f' · {date}' if date else '')
        else:
            sub = ('Starts downloading' if direct else 'Opens Epson download page') + (f' · {size}' if size else '') + (f' · {date}' if date else '')
        out.append(f'<a class="mb{" s" if i else ""}" href="{E(url)}" rel="nofollow"{"" if direct else " target=_blank"}><b>{E(lab)}</b><small>{E(sub)}</small></a>')
    return ''.join(out)


# ── 브라더 데이터 정리 ──────────────────────────────────
def br_label(t, lang='ko'):
    if t.startswith('EasySetup'):
        return ('EasySetup (처음 설치용)', 'EasySetup (first-time setup)')[lang != 'ko']
    if t.startswith('전체 드라이버'):
        return ('전체 드라이버·소프트웨어', 'Full driver & software package')[lang != 'ko']
    if 'iPrint' in t:
        return 'Brother iPrint&Scan'
    if 'Scanner' in t or '스캐너' in t:
        return ('스캐너 드라이버', 'Scanner driver')[lang != 'ko'] if 'Printer' not in t else (('프린터+스캐너 드라이버(USB)', 'Printer + scanner driver (USB)')[lang != 'ko'])
    if 'Printer Driver' in t or '프린터 드라이버' in t:
        return ('프린터 드라이버만', 'Printer driver only')[lang != 'ko']
    return t


def br_btns(prod, os_, items, lang='ko'):
    out = []
    for i, (t, date, size, enc) in enumerate(items):
        dd = re.match(r'(\d{2})/(\d{2})/(\d{4})', date)
        ds = f'{dd.group(3)}/{dd.group(2)}/{dd.group(1)}' if dd else ''
        sub = (('동의 후 다운로드' if lang == 'ko' else 'Accept EULA, then download') + (f' · {size}' if size else '') + (f' · {ds}' if ds else ''))
        out.append(f'<a class="mb{" s" if i else ""}" href="{E(br_url(prod, os_, enc))}" target="_blank" rel="noopener nofollow"><b>{E(br_label(t, lang))}</b><small>{E(sub)}</small></a>')
    return ''.join(out)


def br_groups():
    g = {}
    for ci, name, prod, os_, items in BR['m']:
        g.setdefault(BR['cats'][ci], []).append((name, prod, os_, items))
    for k in g:
        g[k].sort(key=lambda x: x[0])
    return g


# ── 한국어: 엡손 ────────────────────────────────────────
EP_HOME = 'https://www.epson.co.kr/%EA%B3%A0%EA%B0%9D%EC%A7%80%EC%9B%90/sl/s'


def epson():
    path = '/driver/epson.html'
    cr, crld = kr.crumb([('엡손 드라이버', '')])
    groups = ep_groups()
    have = [m for m in EP['m'] if m[3]]
    secs, search, nolist = [], [], []
    for gi, (cat, ms) in enumerate(groups.items()):
        rows = []
        for name, code, items in ms:
            if not items:
                nolist.append((name, code))
                continue
            rows.append(f'<li class="mr" id="{ep_id(code)}"><h3>엡손 {E(name)}</h3><div class="bt">{ep_btns(items)}</div>'
                        f'<a class="of" href="https://www.epson.co.kr/s/SPT_{code}" target="_blank" rel="noopener nofollow">엡손 공식 제품 페이지 (맥용·설명서) ↗</a></li>')
            search.append([name, '#' + ep_id(code)])
        if rows:
            secs.append(f'<details class="mg"{" open" if gi == 0 else ""}><summary>{E(cat)} <span>{len(rows)}개 모델</span></summary><ul class="ml">{"".join(rows)}</ul></details>')
    for name, code in nolist:
        search.append([name, f'https://www.epson.co.kr/s/SPT_{code}'])
    nol = ('<section class="card dr-sec" id="old"><h2>한국 엡손 사이트에 윈도우 파일이 안 걸린 모델</h2>'
           f'<p>아래 {len(nolist)}개 모델은 엡손 한국 사이트 제품 페이지에 윈도우 다운로드 버튼이 없어요(아주 오래된 모델이거나 새 모델이라 준비 중인 경우). '
           '이름을 누르면 엡손 공식 제품 페이지가 열려요. 거기서도 없으면 아래 \'윈도우 자동 설치\'를 먼저 해 보세요.</p><ul class="nm">'
           + ''.join(f'<li><a href="https://www.epson.co.kr/s/SPT_{c}" target="_blank" rel="noopener nofollow">{E(n)}</a></li>' for n, c in nolist) + '</ul></section>')
    ans = ('아래에서 <b>내 엡손 모델</b>을 찾아 파란 <b>[드라이버+프로그램 한 번에]</b>를 누르세요. 엡손 공식 다운로드 창(Epson Download Center)이 열리고, <b>\'위 내용에 동의합니다\'</b>에 체크한 뒤 <b>[다운로드]</b>를 누르면 파일이 받아져요. '
           '받은 파일을 열고 화면 안내대로 누르면 프린터·스캐너가 한 번에 설치돼요. 회원가입은 필요 없어요.')
    install = ('<section class="card dr-sec" id="install"><h2>받은 다음 설치하는 순서 (아주 쉽게)</h2><ol class="big-n">'
               '<li><b>준비:</b> 프린터 전원을 켜고, 다른 프로그램은 닫아 두세요. <b>USB 선은 설치 프로그램이 연결하라고 할 때</b> 꽂는 게 안전해요.</li>'
               '<li><b>파란 버튼 누르기:</b> 내 모델의 <b>[드라이버+프로그램 한 번에]</b>(엡손 \'웹 인스톨러\')를 눌러요. 새 창으로 <b>엡손 다운로드 센터</b>가 열리면 라이센스 계약의 <b>\'위 내용에 동의합니다\'</b>에 체크하고 <b>[다운로드]</b>를 눌러요. 일부 오래된 모델은 누르자마자 바로 받아져요.</li>'
               '<li><b>받은 파일 열기:</b> 키보드 <b>Ctrl + J</b> → 방금 받은 파일을 눌러요. 압축 파일(.zip)이면 오른쪽 버튼 → <b>[모두 압축 풀기]</b> 후 안의 Setup(설치) 파일을 실행해요.</li>'
               '<li><b>\'예\' 누르기:</b> "이 앱이 디바이스를 변경할 수 있도록 허용하시겠어요?"가 뜨면 <b>[예]</b>.</li>'
               '<li><b>사용권 동의 → 설치:</b> 사용권 계약에 <b>동의</b>하고, 설치할 프린터와 연결 방식(USB 또는 와이파이)을 골라 <b>[다음]/[설치]</b>를 눌러요.</li>'
               '<li><b>확인:</b> 설정 → Bluetooth 및 장치 → 프린터 및 스캐너 → 내 프린터 → <b>[테스트 페이지 인쇄]</b>.</li></ol>'
               '<p class="tipbox">💡 <b>버튼 3개, 뭘 받아요?</b><br><b>드라이버+프로그램 한 번에</b>(웹 인스톨러): 프린터 드라이버와 스캔 프로그램 등을 한꺼번에 설치해요. 처음이면 이걸 받으세요.<br>'
               '<b>프린터 드라이버만</b>: 인쇄만 할 때. <b>스캐너 드라이버</b>(Epson Scan 2): 복합기로 스캔할 때 따로 받아요.<br>'
               '엡손 안내에 따르면 파일을 내려받으면 엡손 소프트웨어 사용권 계약에 동의하는 것으로 봐요.</p></section>')
    pics = (cu.step(1, '파란 버튼 → 엡손 다운로드 창', '내 모델의 파란 버튼을 누르면 엡손 공식 다운로드 창이 열려요. 거기서 <b>\'위 내용에 동의합니다\'</b>에 체크하고 <b>[다운로드]</b>를 눌러요.',
                    kr.W_list('download-center.epson.com', 'Epson Download Center · 내 모델 Series', [('Drivers and Utilities Combo Package', ''), ('☑ 위 내용에 동의합니다', ''), ('파일 이름 · 크기', '다운로드')], 2, 1))
            + cu.step(2, '받은 파일 열고 \'예\'', '<b>Ctrl + J</b>로 받은 파일을 열고, 윈도우 확인 창이 뜨면 <b>[예]</b>를 눌러요.', kr.W_uac('Epson 설치 프로그램', 2))
            + cu.step(3, '동의하고 [다음]', '사용권 계약에 동의하고, 내 프린터와 연결 방식을 골라 진행해요.',
                      kr.W_installer('Epson 설치', ['사용권 계약에 동의합니다', '프린터: 내 모델 Series', '연결: ○ USB  ○ 무선'], '다음', 3))
            + cu.step(4, '테스트 페이지로 확인', '<b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b> → 내 프린터 → <b>[테스트 페이지 인쇄]</b>.', kr.W_testpage(4)))
    qa = [('정말 이 페이지에서 받을 수 있나요?', '네. 버튼은 엡손 공식 다운로드 서버(download.ebz.epson.net, my.epson.co.kr)로 바로 연결돼요. 홍라이프 도구는 파일을 직접 올리지 않아요.'),
          ('엡손 드라이버는 무료인가요?', '네. 엡손 공식 드라이버와 소프트웨어는 무료이고 회원가입도 필요 없어요.'),
          ('L3110 드라이버를 눌렀는데 L3100 이름이 나와요.', '엡손은 비슷한 모델을 한 드라이버로 묶어 \'L3100 Series\'처럼 시리즈 이름으로 제공해요. 엡손 공식 제품 페이지가 그렇게 연결한 파일이니 그대로 설치하면 돼요.'),
          ('맥(Mac)용은 어디서 받나요?', '모델 줄 아래 \'엡손 공식 제품 페이지\'를 누르면 맥용 드라이버·설명서를 볼 수 있어요.'),
          ('스캔이 안 돼요.', '복합기라면 \'스캐너 드라이버(Epson Scan 2)\'를 따로 설치하세요. \'드라이버+프로그램 한 번에\'로 설치했다면 이미 들어 있을 수 있어요.'),
          ('모델이 목록에 없어요.', '맨 위 검색창에 숫자만(예: 3250) 넣어 보세요. 그래도 없으면 엡손 고객지원 사이트에서 제품명을 검색하세요.')]
    fq, fqld = cu.faq(qa)
    n = len(have)
    main = (kr.HP_CSS + CSS + f'<header class="top hub">{cr}<h1>엡손(Epson) 프린터 드라이버 바로 다운로드·설치 방법 — 모델별 {n}개</h1>'
            f'<p class="lead">엡손 정품무한 L시리즈(L3250·L3210·L6290…), WorkForce, 라벨·대형·도트 프린터까지 {n}개 모델의 드라이버를 이 페이지에서 바로 받을 수 있어요. 파일은 엡손 공식 서버에서 내려와요.</p>'
            f'<p class="cu-ans">{ans}</p>'
            '<ul class="dr-toc"><li><a href="#models">모델별 바로 받기</a></li><li><a href="#install">설치 순서</a></li><li><a href="#easy">처음이세요?</a></li><li><a href="#old">목록에 버튼이 없는 모델</a></li></ul></header>'
            f'<section class="card dr-sec" id="models"><h2>모델별 바로 받기 ({n}개)</h2><p>모델 번호를 입력하면 그 모델로 바로 가요. 시리즈 이름을 누르면 모델 목록이 펼쳐져요.</p>'
            + search_js('epQ', search, '모델 번호 입력 (예: L3250, 3210)', '이 페이지에 없는 모델이에요. 엡손 고객지원에서 제품명을 검색해 주세요.', '찾기')
            + ''.join(secs)
            + f'<p class="cu-src" style="margin-top:10px">엡손 한국 공식 사이트(epson.co.kr) 각 제품 페이지의 윈도우 10·11용 다운로드를 {kr.CHECKED}에 확인했어요. 32비트 윈도우·맥은 \'엡손 공식 제품 페이지\'에서 고르세요.</p>'
            + kr.dl(EP_HOME, '엡손 고객지원 열기', '목록에 없을 때: 엡손 공식 사이트에서 제품명 검색', True) + '</section>'
            + install + kr.guide_sec('엡손', True) + f'<section class="card dr-sec" id="pics"><h2>그림으로 한 번 더 보기</h2>{pics}</section>'
            + nol + kr.WIN_SEC + fq
            + kr.src_sec('엡손 한국 공식 고객지원(epson.co.kr) 제품별 다운로드, 엡손 다운로드 서비스(download.ebz.epson.net), Microsoft 지원 \'최신 프린터 드라이버 다운로드 및 설치\'')
            + kr.REL)
    ld = [crld, fqld, kr.howto('엡손 프린터 드라이버 설치 방법', ['내 모델의 드라이버+프로그램 한 번에 누르기', '엡손 다운로드 센터에서 동의 체크 후 다운로드', '받은 파일 열고 예', '사용권 동의 후 프린터·연결 방식 선택', '테스트 페이지 인쇄'])]
    kr.write(path, f'엡손 프린터 드라이버 바로 다운로드 — 모델별 {n}개 (L3250·L3210·L6290·WF) 설치 방법 | 홍라이프 도구',
             f'엡손 정품무한 L3250·L3210·L3110·L6290·L8180, WorkForce, 라벨·대형 프린터 등 {n}개 모델의 드라이버를 이 페이지에서 바로 받고, 쉬운 설치 순서를 확인하세요. 파일은 엡손 공식 서버에서 내려와요.',
             main, ld)
    return path


# ── 한국어: 브라더 ──────────────────────────────────────
BR_HOME = 'https://support.brother.com/g/b/productsearch.aspx?c=kr&lang=ko&content=dl'


def brother():
    path = '/driver/brother.html'
    cr, crld = kr.crumb([('브라더 드라이버', '')])
    groups = br_groups()
    secs, search, nodl = [], [], []
    for gi, (cat, ms) in enumerate(groups.items()):
        rows = []
        for name, prod, os_, items in ms:
            top = f'https://support.brother.com/g/b/downloadtop.aspx?c=kr&lang=ko&prod={prod}'
            if not items:
                nodl.append((name, top))
                continue
            rows.append(f'<li class="mr" id="{br_id(prod)}"><h3>브라더 {E(name)}</h3><div class="bt">{br_btns(prod, os_, items)}</div>'
                        f'<a class="of" href="{E(top)}" target="_blank" rel="noopener nofollow">브라더 공식 다운로드 (맥·다른 윈도우) ↗</a></li>')
            search.append([name, '#' + br_id(prod)])
        if rows:
            secs.append(f'<details class="mg"{" open" if gi == 0 else ""}><summary>{E(cat)} <span>{len(rows)}개 모델</span></summary><ul class="ml">{"".join(rows)}</ul></details>')
    for name, top in nodl:
        search.append([name, top])
    n = len(search) - len(nodl)
    ans = ('아래에서 <b>내 브라더 모델</b>을 찾아 파란 버튼을 누르면 <b>브라더 공식 다운로드 화면</b>이 열려요. 브라더는 받기 전에 사용권 계약(EULA)을 보여 주는데, '
           '<b>[EULA에 동의 및 다운로드]</b>를 한 번 누르면 파일이 바로 받아져요. 그다음 받은 파일을 열고 화면 안내대로 설치하면 돼요.')
    install = ('<section class="card dr-sec" id="install"><h2>받은 다음 설치하는 순서 (아주 쉽게)</h2><ol class="big-n">'
               '<li><b>준비:</b> 프린터 전원을 켜 두세요. <b>USB 선은 설치 프로그램이 연결하라고 할 때</b> 꽂으세요.</li>'
               '<li><b>파란 버튼 누르기:</b> 처음 설치라면 <b>[전체 드라이버·소프트웨어]</b>나 <b>[EasySetup]</b>을 눌러요. 브라더 공식 화면이 새 창으로 열려요.</li>'
               '<li><b>동의하고 받기:</b> 사용권 계약 아래의 <b>[EULA에 동의 및 다운로드]</b>를 눌러요. 그러면 파일이 바로 받아져요.</li>'
               '<li><b>받은 파일 열기:</b> 키보드 <b>Ctrl + J</b> → 받은 파일 실행 → 윈도우 확인 창에서 <b>[예]</b>. 파일이 스스로 압축을 풀고 설치 화면이 열려요.</li>'
               '<li><b>안내대로 진행:</b> 언어·사용권 동의 → 연결 방식(<b>USB(로컬 연결)</b> 또는 <b>무선/유선 네트워크</b>)을 고르고 <b>[다음]</b>을 눌러요.</li>'
               '<li><b>확인:</b> 설정 → Bluetooth 및 장치 → 프린터 및 스캐너 → 내 프린터 → <b>[테스트 페이지 인쇄]</b>.</li></ol>'
               '<p class="tipbox">💡 <b>버튼이 여러 개예요. 뭘 받아요?</b><br><b>EasySetup</b>: 프린터를 처음 설정하고 컴퓨터에 연결하는 과정을 안내해 줘요(브라더 설명).<br>'
               '<b>전체 드라이버·소프트웨어</b>: 기기에 쓸 수 있는 드라이버와 소프트웨어를 모두 담은 파일이에요. 이미 프린터 설정을 마친 경우 브라더가 이걸 권해요.<br>'
               '<b>프린터 드라이버만</b>: 인쇄용 드라이버만 설치해요. <b>Brother iPrint&amp;Scan</b>: 스캔·인쇄를 쉽게 하는 브라더 앱이에요.</p></section>')
    pics = (cu.step(1, '파란 버튼 → 브라더 동의 화면', '파란 버튼을 누르면 브라더 공식 화면에 사용권 계약이 나와요. 맨 아래 <b>[EULA에 동의 및 다운로드]</b>를 눌러요.',
                    kr.W_list('support.brother.com', '최종 사용자 사용권 계약 (EULA)', [('사용권 계약 내용…', ''), ('', ''), ('EULA에 동의 및 다운로드', '동의')], 2, 1))
            + cu.step(2, '받은 파일 열고 \'예\'', '<b>Ctrl + J</b>로 받은 파일을 열고 윈도우 확인 창에서 <b>[예]</b>를 눌러요.', kr.W_uac('Brother 설치 프로그램', 2))
            + cu.step(3, '연결 방식 고르고 [다음]', 'USB 선이면 \'로컬 연결(USB)\', 와이파이면 \'무선 네트워크 연결\'을 골라요.',
                      kr.W_installer('Brother 설치', ['연결 방식을 고르세요', '○ 로컬 연결 (USB)', '○ 무선 네트워크 연결'], '다음', 3))
            + cu.step(4, '테스트 페이지로 확인', '<b>설정 → Bluetooth 및 장치 → 프린터 및 스캐너</b> → 내 프린터 → <b>[테스트 페이지 인쇄]</b>.', kr.W_testpage(4)))
    qa = [('왜 바로 안 받아지고 동의 화면이 나와요?', '브라더는 모든 드라이버를 받기 전에 사용권 계약(EULA)에 동의하도록 정해 두었어요. 동의 버튼은 꼭 본인이 직접 눌러야 해서, 이 페이지는 그 동의 화면까지 바로 연결해 드려요. 한 번만 누르면 받아져요.'),
          ('브라더 드라이버는 무료인가요?', '네. 브라더 공식 드라이버와 소프트웨어는 무료예요.'),
          ('윈도우 10이에요. 이 버튼 받아도 되나요?', '버튼은 윈도우 11(오래된 모델은 윈도우 10) 기준으로 연결했어요. 대부분 같은 파일을 쓰지만, 다르면 \'브라더 공식 다운로드\'를 눌러 내 윈도우 버전을 고르세요.'),
          ('맥(Mac)용은요?', '모델 줄의 \'브라더 공식 다운로드\'를 누르고 OS에서 macOS를 고르면 돼요.'),
          ('모델명이 어디 있어요?', '프린터 앞면이나 윗면에 DCP-T720DW, MFC-L2700D처럼 적혀 있어요. 검색창에는 숫자만(예: 720) 넣어도 돼요.')]
    fq, fqld = cu.faq(qa)
    main = (kr.HP_CSS + CSS + f'<header class="top hub">{cr}<h1>브라더(Brother) 프린터 드라이버 바로 다운로드·설치 방법 — 모델별 {n}개</h1>'
            f'<p class="lead">브라더 잉크젯(DCP-T·MFC-T·MFC-J), 레이저(HL·DCP-L·MFC-L), 라벨(P-touch·QL), 스캐너(ADS)까지 {n}개 모델의 드라이버를 이 페이지에서 바로 받을 수 있어요. 파일은 브라더 공식 서버에서 내려와요.</p>'
            f'<p class="cu-ans">{ans}</p>'
            '<ul class="dr-toc"><li><a href="#models">모델별 바로 받기</a></li><li><a href="#install">설치 순서</a></li><li><a href="#easy">처음이세요?</a></li></ul></header>'
            f'<section class="card dr-sec" id="models"><h2>모델별 바로 받기 ({n}개)</h2><p>모델 번호를 입력하면 그 모델로 바로 가요. 종류 이름을 누르면 모델 목록이 펼쳐져요.</p>'
            + search_js('brQ', search, '모델 번호 입력 (예: T720, L2700)', '이 페이지에 없는 모델이에요. 브라더 지원 사이트에서 검색해 주세요.', '찾기')
            + ''.join(secs)
            + f'<p class="cu-src" style="margin-top:10px">브라더 공식 지원 사이트(support.brother.com, 대한민국·한국어)의 윈도우 10·11용 다운로드를 {kr.CHECKED}에 확인했어요. 날짜·크기는 그때 기준이에요.</p>'
            + kr.dl(BR_HOME, '브라더 지원 및 다운로드 열기', '목록에 없을 때: 브라더 공식 사이트에서 모델 검색', True) + '</section>'
            + install + kr.guide_sec('브라더') + f'<section class="card dr-sec" id="pics"><h2>그림으로 한 번 더 보기</h2>{pics}</section>'
            + kr.WIN_SEC + fq
            + kr.src_sec('브라더 공식 지원 사이트(support.brother.com) 대한민국 다운로드 목록·설명, Microsoft 지원 \'최신 프린터 드라이버 다운로드 및 설치\'')
            + kr.REL)
    ld = [crld, fqld, kr.howto('브라더 프린터 드라이버 설치 방법', ['내 모델의 전체 드라이버 버튼 누르기', 'EULA에 동의 및 다운로드', '받은 파일 열고 예', '연결 방식 선택 후 다음', '테스트 페이지 인쇄'])]
    kr.write(path, f'브라더 프린터 드라이버 바로 다운로드 — 모델별 {n}개 (DCP-T720DW·MFC-L2700D·HL-L2321D) 설치 방법 | 홍라이프 도구',
             f'브라더 DCP-T720DW·DCP-T420W·MFC-T920DW·MFC-L2700D·HL-L2321D 등 {n}개 모델의 드라이버를 이 페이지에서 바로 받고 쉬운 설치 순서를 확인하세요. 파일은 브라더 공식 서버에서 내려와요.',
             main, ld)
    return path


# ── 영어 ───────────────────────────────────────────────
def epson_en():
    path = '/en/driver/epson.html'
    cr, crld = en.crumb([('Epson drivers', '')])
    secs, search = [], []
    for gi, (cat, ms) in enumerate(ep_groups().items()):
        rows = []
        for name, code, items in ms:
            if not items:
                continue
            nm = re.sub(r'[가-힣]+\s*', '', name).strip() or name
            rows.append(f'<li class="mr" id="{ep_id(code)}"><h3>Epson {E(nm)}</h3><div class="bt">{ep_btns(items, "en")}</div>'
                        f'<a class="of" href="https://www.epson.co.kr/s/SPT_{code}" target="_blank" rel="noopener nofollow">Official Epson product page (Mac, manuals) ↗</a></li>')
            search.append([nm, '#' + ep_id(code)])
        if rows:
            cat_en = cat.replace('정품무한 L 시리즈', 'EcoTank L series').replace('정품무한 M 시리즈', 'EcoTank M series').replace('기타 제품', 'Other products').replace('시리즈', 'series')
            secs.append(f'<details class="mg"{" open" if gi == 0 else ""}><summary>{E(cat_en)} <span>{len(rows)} models</span></summary><ul class="ml">{"".join(rows)}</ul></details>')
    n = len(search)
    steps = ('<ol class="big-n"><li>Click the blue <b>Driver + utilities</b> button for your model. Epson Download Center opens — tick <b>I agree</b> under the license and click <b>Download</b>.</li>'
             '<li>Open the file with <b>Ctrl + J</b>. If it is a .zip, right-click → <b>Extract All</b> and run Setup.</li>'
             '<li>Click <b>Yes</b> on the Windows prompt, accept the license, choose your printer and USB or Wi-Fi, then <b>Next</b>.</li>'
             '<li>Print a test page: Settings → Bluetooth &amp; devices → Printers &amp; scanners.</li></ol>'
             '<p class="tipbox">Epson states that downloading the software means you agree to the Epson software license agreement.</p>')
    qa = [('Where do the files come from?', 'Directly from Epson\'s official servers (download.ebz.epson.net, my.epson.co.kr). HongLife Tools does not host files.'),
          ('The link says "L3100 Series" for my L3110.', 'Epson ships one driver per series; the official product page links the same file.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + CSS + f'<header class="top hub">{cr}<h1>Epson Printer Drivers — Direct Download for {n} Models</h1>'
            f'<p class="lead">EcoTank L3250, L3210, L6290, WorkForce, label and large-format printers — {n} Epson models with links to Epson\'s official download servers and easy install steps.</p>'
            '<ul class="dr-toc"><li><a href="#models">Models</a></li><li><a href="#steps">Install steps</a></li><li><a href="#easy">First time?</a></li></ul></header>'
            f'<section class="card dr-sec" id="models"><h2>Direct downloads by model ({n})</h2>'
            + search_js('epE', search, 'Model (e.g. L3250)', 'Not in this list. Search on Epson\'s support site.', 'Find') + ''.join(secs)
            + f'<p class="cu-src" style="margin-top:10px">Windows 10/11 downloads checked on Epson Korea product pages on {en.CHECKED}.</p></section>'
            + f'<section class="card dr-sec" id="steps"><h2>Install steps</h2>{steps}</section>' + en.easy('Epson', True) + en.WIN + fq
            + en.src('Epson Korea official support (epson.co.kr), Epson download service (download.ebz.epson.net)') + en.REL)
    en.write(path, f'Epson Printer Driver Download — {n} Models (L3250, L3210, L6290) | HongLife Tools',
             f'Download Epson printer drivers for {n} models (EcoTank L3250, L3210, L3110, L6290, WorkForce) from Epson\'s official servers, with easy install steps.',
             main, [crld, fqld])
    return path


def brother_en():
    path = '/en/driver/brother.html'
    cr, crld = en.crumb([('Brother drivers', '')])
    cat_en = {'흑백 레이저 프린터': 'Mono laser printers', '컬러 레이저 프린터': 'Color laser printers', '흑백 레이저 복합기': 'Mono laser MFPs',
              '잉크젯 복합기·프린터': 'Inkjet printers / MFPs', '모바일 프린터': 'Mobile printers', 'P-touch 라벨': 'P-touch labelers',
              '컬러 레이저 복합기': 'Color laser MFPs', '라벨 프린터(QL/TD)': 'Label printers (QL/TD)', '문서 스캐너': 'Document scanners'}
    secs, search = [], []
    for gi, (cat, ms) in enumerate(br_groups().items()):
        rows = []
        for name, prod, os_, items in ms:
            if not items:
                continue
            top = f'https://support.brother.com/g/b/downloadtop.aspx?c=kr&lang=ko&prod={prod}'
            rows.append(f'<li class="mr" id="{br_id(prod)}"><h3>Brother {E(name)}</h3><div class="bt">{br_btns(prod, os_, items, "en")}</div>'
                        f'<a class="of" href="{E(top)}" target="_blank" rel="noopener nofollow">Official Brother downloads (Mac, other Windows) ↗</a></li>')
            search.append([name, '#' + br_id(prod)])
        if rows:
            secs.append(f'<details class="mg"{" open" if gi == 0 else ""}><summary>{E(cat_en.get(cat, cat))} <span>{len(rows)} models</span></summary><ul class="ml">{"".join(rows)}</ul></details>')
    n = len(search)
    steps = ('<ol class="big-n"><li>Click a blue button for your model. Brother\'s official page shows the license (EULA).</li>'
             '<li>Click <b>Agree to the EULA and Download</b> — the file downloads right away.</li>'
             '<li>Open it with <b>Ctrl + J</b>, click <b>Yes</b>, then choose <b>Local (USB)</b> or <b>Wireless network</b> and follow the steps.</li>'
             '<li>Print a test page: Settings → Bluetooth &amp; devices → Printers &amp; scanners.</li></ol>'
             '<p class="tipbox"><b>Which file?</b> EasySetup guides first-time setup. The Full Driver &amp; Software Package contains every driver and app for the machine (Brother recommends it if setup is already done).</p>')
    qa = [('Why is there a license page?', 'Brother requires you to accept its EULA before every download. You must click it yourself; it takes one click.'),
          ('Where do the files come from?', 'From Brother\'s official support site (support.brother.com). HongLife Tools does not host files.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + CSS + f'<header class="top hub">{cr}<h1>Brother Printer Drivers — Direct Download for {n} Models</h1>'
            f'<p class="lead">Brother inkjet (DCP-T, MFC-T, MFC-J), laser (HL, DCP-L, MFC-L), label (P-touch, QL) and scanners (ADS) — {n} models linked to Brother\'s official downloads.</p>'
            '<ul class="dr-toc"><li><a href="#models">Models</a></li><li><a href="#steps">Install steps</a></li><li><a href="#easy">First time?</a></li></ul></header>'
            f'<section class="card dr-sec" id="models"><h2>Direct downloads by model ({n})</h2>'
            + search_js('brE', search, 'Model (e.g. T720)', 'Not in this list. Search on Brother support.', 'Find') + ''.join(secs)
            + f'<p class="cu-src" style="margin-top:10px">Windows 10/11 downloads checked on Brother support (Korea) on {en.CHECKED}.</p></section>'
            + f'<section class="card dr-sec" id="steps"><h2>Install steps</h2>{steps}</section>' + en.easy('Brother') + en.WIN + fq
            + en.src('Brother official support (support.brother.com)') + en.REL)
    en.write(path, f'Brother Printer Driver Download — {n} Models (DCP-T720DW, MFC-L2700D) | HongLife Tools',
             f'Download Brother printer drivers for {n} models (DCP-T720DW, MFC-T920DW, MFC-L2700D, HL-L2321D) from Brother\'s official site, with easy install steps.',
             main, [crld, fqld])
    return path


def ep_hub_items(prefix=''):
    return [[f'엡손 {m[1]}' if not prefix else 'Epson ' + (re.sub(r'[가-힣]+\s*', '', m[1]).strip() or m[1]), f'{prefix}/driver/epson.html#' + ep_id(m[2])] for m in EP['m'] if m[3]]


def br_hub_items(prefix=''):
    return [[('브라더 ' if not prefix else 'Brother ') + m[1], f'{prefix}/driver/brother.html#' + br_id(m[2])] for m in BR['m'] if m[4]]


if __name__ == '__main__':
    print('\n'.join([epson(), brother(), epson_en(), brother_en()]))
