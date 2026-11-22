"""LG전자 드라이버 페이지 (그램 노트북·PC 모니터) — 한국어 /driver/lg.html, 영어 /en/driver/lg.html
데이터: data/lg_models.json (fetch_lg.py가 LG 공식 고객지원에서 매주 수집)
모델 이름은 모두 글로 페이지에 넣고(검색 노출), 파일 버튼은 모델을 고르면 /driver/data/lg.json 에서 불러와 보여 준다(페이지가 너무 무거워지지 않게).
공식 안내(2026-11-22 확인): LG 'LG Update 프로그램 설치 가이드', 'OnScreen Control 사용 방법'
"""
import json, os, re, sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en
import driver_more as dm

E = cu.E
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
LG = json.load(open(os.path.join(D, 'lg_models.json'), encoding='utf-8'))
GS = 'https://gscs-b2c.lge.com/downloadFile?fileId='
LGU = GS + 'oSxUlNAKD1EOIDjwbhBEQ'          # LG Update 프로그램 (LG Update 통합 런처)
OSC_W = GS + 'JNNIDscONmgtB3eXvwK3gg'        # OnScreen Control Windows 10·11 Ver 9.54
OSC_M = GS + 'OTn9J9ZVlaEorr2dzxJ4zg'        # OnScreen Control Mac Ver 7.30
LGU_GUIDE = 'https://www.lge.co.kr/support/solutions-20153165094477'
OSC_GUIDE = 'https://www.lge.co.kr/support/solutions-20152166068338'
LG_DL = 'https://www.lge.co.kr/support/product-manuals'


def mid(code):
    return 'm-' + re.sub(r'[^A-Za-z0-9]', '', code)


def build_json():
    """모델→파일 목록 JSON (화면에서 모델을 고를 때만 불러옴). 파일은 번호로, 같은 파일 묶음은 한 번만 적어 크기를 줄임"""
    ids = sorted(LG['files'])
    ix = {k: i for i, k in enumerate(ids)}
    sets, sx, m = [], {}, {}
    for kind, code, sales, fl in LG['models']:
        key = tuple(dict.fromkeys(ix[f] for f in fl if f in ix))
        if key not in sx:
            sx[key] = len(sets)
            sets.append(list(key))
        m[code] = [kind[0], sales, sx[key]]
    out = os.path.join(kr.ROOT, 'overlay', 'driver', 'data', 'lg.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({'i': ids, 'f': [LG['files'][k] for k in ids], 's': sets, 'm': m, 'c': LG['checked']}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))


def groups(kind):
    """판매 모델명 기준으로 묶고, 그램은 화면 크기(앞 2자리)·모니터는 인치(앞 2자리)로 칸 나누기"""
    by = OrderedDict()
    for k, code, sales, fl in LG['models']:
        if k != kind:
            continue
        by.setdefault(sales, []).append((code, fl))
    g = OrderedDict()
    for sales in sorted(by, key=lambda s: (re.match(r'\d+', s) is None, int((re.match(r'\d+', s) or [0])[0]) if re.match(r'\d+', s) else 0, s)):
        key = (re.match(r'\d{2}', sales) or [None])[0]
        g.setdefault(key or '기타', []).append((sales, by[sales]))
    return g


CSS = ('<style>.lgc{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:8px 0 4px;padding:0}'
       '.lgc a{display:inline-block;padding:6px 10px;border-radius:999px;background:#F1F3F5;color:#222;font-size:13px;font-weight:600;text-decoration:none}'
       '.lgc a.f{background:var(--acc-soft,#EAF2FE);color:var(--acc,#1B64DA)}'
       '#lgp{scroll-margin-top:80px}.lgp{border:2px solid var(--acc,#1B64DA);border-radius:16px;padding:14px;margin:12px 0;background:#fff}'
       '.lgp h3{margin:0 0 8px;font-size:18px}.lgp .bt{display:flex;flex-direction:column;gap:6px}'
       '.lgp .bt a{display:flex;flex-direction:column;padding:10px 13px;border-radius:12px;background:var(--acc-soft,#EAF2FE);color:var(--acc,#1B64DA)!important;text-decoration:none}'
       '.lgp .bt a:first-child{background:var(--acc,#1B64DA);color:#fff!important}.lgp .bt a b{font-size:14.5px;word-break:break-all}.lgp .bt a small{font-size:12px;opacity:.9}'
       '.lgp p{margin:6px 0;line-height:1.6}</style>')


def panel_js(lang):
    ko = lang == 'ko'
    t = {'load': '불러오는 중…' if ko else 'Loading…',
         'none': ('LG 고객지원에 이 모델용으로 올라온 개별 파일이 없어요. 노트북이면 위 [LG Update 프로그램]으로, 모니터면 OnScreen Control로 설치하세요.' if ko
                  else 'LG has no separate files for this model. Use LG Update (laptops) or OnScreen Control (monitors) above.'),
         'off': 'LG 공식 지원 페이지 ↗' if ko else 'Official LG support page ↗',
         'dl': '누르면 LG 서버에서 바로 다운로드' if ko else 'Downloads directly from LG',
         'gram': '그램 노트북' if ko else 'LG gram laptop', 'mon': 'PC 모니터' if ko else 'PC monitor',
         'tipg': ('💡 노트북은 LG Update 프로그램이 내 모델에 맞는 드라이버를 자동으로 찾아 설치해 줘요(LG 권장). 아래 파일은 인터넷(랜·무선랜)이 안 될 때 먼저 깔거나, 오래된 모델을 직접 설치할 때 쓰세요.' if ko
                  else 'Tip: LG recommends the LG Update program for laptops. Use the files below when the network driver is missing or for older models.')}
    return ('<script>var LGJ=null,LGT=' + json.dumps(t, ensure_ascii=False) + ';'
            'function lgEsc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})}'
            'function lgShow(code){var p=document.getElementById("lgp");if(!p)return;p.innerHTML="<div class=lgp>"+LGT.load+"</div>";'
            'var go=function(){var m=LGJ.m[code];if(!m){p.innerHTML="";return}var fl=LGJ.s[m[2]].map(function(i){return[LGJ.i[i],LGJ.f[i]]});'
            'fl.sort(function(a,b){var r=function(t){return /\\[(무선랜|랜|WLAN|LAN)/.test(t)?0:1};return r(a[1][0])-r(b[1][0])||(b[1][1]||"").localeCompare(a[1][1]||"")});'
            'var h="<div class=lgp><h3>LG "+lgEsc(m[1])+" <small style=\'font-size:13px;color:#5B6B82\'>"+(code!=m[1]?lgEsc(code)+" · ":"")+(m[0]=="g"?LGT.gram:LGT.mon)+"</small></h3>";'
            'if(m[0]=="g")h+="<p class=tipbox>"+LGT.tipg+"</p>";'
            'h+=fl.length?"<div class=bt>"+fl.map(function(x){var f=x[1];return"<a href=\'https://gscs-b2c.lge.com/downloadFile?fileId="+encodeURIComponent(x[0])+"\' rel=nofollow><b>"+lgEsc(f[0])+"</b><small>"+LGT.dl+(f[3]?" · "+lgEsc(f[3]):"")+(f[1]?" · "+lgEsc(f[1]):"")+(f[2]?" · "+lgEsc(f[2]):"")+"</small></a>"}).join("")+"</div>":"<p>"+LGT.none+"</p>";'
            'h+="<p><a href=\'https://www.lge.co.kr/support/product-"+encodeURIComponent(code)+"\' target=_blank rel=\'noopener nofollow\'>"+LGT.off+"</a></p></div>";p.innerHTML=h;p.scrollIntoView({block:"start"})};'
            'if(LGJ)go();else fetch("/driver/data/lg.json").then(function(r){return r.json()}).then(function(j){LGJ=j;go()})}'
            'function lgHash(){var h=decodeURIComponent(location.hash||"");if(h.indexOf("#m=")==0)lgShow(h.slice(3))}'
            'window.addEventListener("hashchange",lgHash);window.addEventListener("load",lgHash);</script>')


def chips(kind, label_fmt):
    out = []
    for key, items in groups(kind).items():
        lis = []
        for sales, codes in items:
            has = any(fl for _, fl in codes)
            code = codes[0][0] if not has else next(c for c, fl in codes if fl)
            lis.append(f'<li><a{" class=f" if has else ""} href="#m={E(code)}">{E(sales)}</a></li>')
        out.append(f'<h3 style="font-size:15px;margin:14px 0 2px">{E(label_fmt(key))} <span style="font-size:13px;color:var(--muted,#5B6B82);font-weight:600">{len(items)}</span></h3><ul class="lgc">{"".join(lis)}</ul>')
    return ''.join(out)


def search_items(prefix=''):
    seen, items = set(), []
    for k, code, sales, fl in LG['models']:
        for nm in (sales, code):
            key = (nm, code)
            if nm in seen:
                continue
            seen.add(nm)
            items.append([nm, f'{prefix}/driver/lg.html#m={code}'])
    return items


def search_box(var, ph, miss, btn):
    """검색 목록은 아래 모델 이름 단추에서 바로 만들어 페이지 무게를 줄임 (판매 모델명·세부 모델 코드 둘 다 찾힘)"""
    return (f'<form class="dr-q" onsubmit="return {var}(1)"><input id="dr-in" placeholder="{E(ph)}" autocomplete="off" oninput="{var}()" aria-label="model search"><button type="submit">{E(btn)}</button></form><ul id="dr-res"></ul>'
            f'<script>var {var}D=null;function {var}(go){{if(!{var}D){var}D=[].map.call(document.querySelectorAll(".lgc a"),function(a){{var c=a.getAttribute("href").slice(3);return[a.textContent,c,(a.textContent+c).replace(/[\\s-]/g,"").toUpperCase()]}});'
            'var q=document.getElementById("dr-in").value.replace(/[\\s-]/g,"").toUpperCase(),r=document.getElementById("dr-res");if(!q){r.innerHTML="";return false}'
            f'var h={var}D.filter(function(x){{return x[2].indexOf(q)>=0}}).slice(0,10);'
            'if(go&&h.length){location.hash="m="+h[0][1];r.innerHTML="";return false}'
            'r.innerHTML=h.length?h.map(function(x){return\'<li><a href="#m=\'+x[1]+\'">LG \'+x[0]+\' ›</a></li>\'}).join(""):'
            f'"<li>{miss}</li>";return false}}</script>')


def lg():
    path = '/driver/lg.html'
    cr, crld = kr.crumb([('LG전자 드라이버', '')])
    ng = len({s for k, c, s, f in LG['models'] if k == 'gram'})
    nm = len({s for k, c, s, f in LG['models'] if k == 'monitor'})
    ans = ('<b>LG 그램 노트북</b>은 아래 <b>[LG Update 프로그램 바로 받기]</b>를 눌러 설치하면, 내 노트북에 맞는 드라이버와 전용 프로그램을 <b>자동으로 찾아 설치</b>해 줘요(LG전자 공식 권장 방법). '
           '<b>LG 모니터</b>는 <b>OnScreen Control</b>로 화면 분할·설정과 모니터 소프트웨어 업데이트를 해요. 모델별 개별 파일(랜·무선랜·모니터 드라이버 등)은 아래에서 모델명을 고르면 바로 받을 수 있어요.')
    lgu_steps = ('<ol class="big-n">'
                 '<li>아래 <b>[LG Update 프로그램 바로 받기]</b>를 누르면 LG 서버에서 파일(LG Update 통합 런처)이 바로 내려받아져요.</li>'
                 '<li>받은 파일의 <b>압축을 풀어요</b>(파일에서 마우스 오른쪽 버튼 → [모두 압축 풀기]).</li>'
                 '<li>파일 탐색기에서 <b>[LG Update Installer]</b> 파일을 두 번 눌러 실행해요.</li>'
                 '<li>\'시스템에 맞는 LG Update 앱을 설치합니다\'라는 창이 나오면 <b>[확인]</b>을 눌러요. 최신 버전으로 자동 업데이트돼요.</li>'
                 '<li>설치가 끝나면 <b>[LG Update 실행하기]</b>에 체크하고 <b>[마침]</b>을 눌러요. 업데이트 목록에서 <b>전체 설치</b>를 하면 돼요.</li></ol>'
                 '<p class="tipbox">💡 <b>꼭 인터넷이 연결돼 있어야 해요.</b> LG Update는 내 PC에 맞는 최신 드라이버를 실시간으로 찾아 받는 방식이에요. '
                 '윈도우를 새로 깔아서 <b>와이파이·랜이 안 잡히면</b>, 아래 모델별 파일에서 <b>[랜]·[무선랜]</b> 드라이버를 다른 컴퓨터로 받아 USB로 옮겨 먼저 설치하세요.<br>'
                 'Microsoft Store에서 <b>LG Update Installer</b>를 검색해 설치해도 돼요(LG 안내).</p>')
    years = ('<div style="overflow-x:auto"><table class="dr-m"><thead><tr><th>출시</th><th>윈도우</th><th>LG Update 앱</th></tr></thead><tbody>'
             '<tr><td>25년 이후</td><td>윈도우 11 / 윈도우 없음</td><td>LG Update &amp; Renew</td></tr>'
             '<tr><td>22년 이후</td><td>윈도우 11</td><td>LG Update &amp; Recovery</td></tr>'
             '<tr><td>22년 이후</td><td>윈도우 없음</td><td>LG Update</td></tr>'
             '<tr><td>18년 이후</td><td>윈도우 10</td><td>LG Update Center</td></tr>'
             '<tr><td>18년 이후</td><td>윈도우 없음</td><td>LG DnA Center Plus</td></tr>'
             '<tr><td>17년 이전</td><td>윈도우 8·8.1</td><td>LG전자 다운로드 센터(모델별 파일)</td></tr></tbody></table></div>'
             '<p class="cu-src">LG전자 \'LG Update 프로그램 설치 가이드\'의 연도별 표. 모델마다 다를 수 있으니 사용설명서도 함께 확인하세요.</p>')
    osc = ('<p><b>OnScreen Control</b>은 LG 모니터의 <b>화면 분할, 모니터 설정, 소프트웨어(펌웨어) 업데이트</b>를 PC에서 마우스로 할 수 있게 해 주는 LG 전용 앱이에요. 일부 모델만 지원해요.</p>'
           + kr.dl(OSC_W, 'OnScreen Control 바로 받기 (윈도우 10·11)', 'Ver 9.54 · LG 서버에서 바로 다운로드') + kr.dl(OSC_M, '맥(Mac)용 OnScreen Control', 'Ver 7.30 · macOS 12·13', True)
           + '<ol class="big-n"><li>위 버튼으로 받아 설치하고, 작업 표시줄 검색창에서 <b>OnScreen Control</b>을 실행해요.</li>'
           '<li><b>모니터 소프트웨어 업데이트</b>는 PC와 모니터를 <b>USB 케이블</b>(USB C to A, A to B, C to C, 썬더볼트 중 하나)로 연결하고 인터넷이 된 상태에서 [모니터 설정] 메뉴로 해요.</li>'
           '<li>\'연결된 모니터가 없습니다\'가 나오면: 미러(복제) 모드 대신 <b>확장</b>으로 바꾸고, 제품에 들어 있던 케이블로 다시 연결하고, 그래픽 드라이버를 최신으로 업데이트해 보세요(LG 안내).</li></ol>'
           '<p class="cu-src">모니터 드라이버(.inf)·OnScreen Control 지원 여부는 모델마다 달라요. 아래에서 내 모델명을 누르면 그 모델용 파일만 보여 줘요.</p>')
    qa = [('그램 드라이버를 하나씩 따로 받을 수 있나요?', 'LG전자 안내에 따르면 최근 노트북은 개별 드라이버 파일만 따로 받는 기능을 제공하지 않고, LG Update 프로그램으로 통합 설치해요. 다만 랜·무선랜 드라이버처럼 모델별로 올라온 파일은 이 페이지에서 모델을 고르면 바로 받을 수 있어요.'),
          ('윈도우를 새로 깔았더니 화면 밝기·와이파이·터치패드가 안 돼요.', '장치 드라이버가 아직 안 깔린 상태예요. 인터넷이 되면 LG Update 프로그램을 설치해 업데이트 목록에서 전체 설치를 하세요. 인터넷이 안 되면 다른 컴퓨터로 내 모델의 랜·무선랜 드라이버를 받아 먼저 설치하세요.'),
          ('윈도우 버전을 바꿨는데 LG Update가 안 맞아요.', 'LG전자는 처음 들어 있던 윈도우가 아닌 다른 버전을 깔면 LG Update로 드라이버 설치가 지원되지 않을 수 있다고 안내해요.'),
          ('\'시스템에 맞는 LG Update 앱이 이미 설치되어 있습니다\'라고 나와요.', '이미 설치된 상태예요. 윈도우 시작 메뉴에서 LG Update를 검색해 바로 실행하세요(LG 안내).'),
          ('모델명은 어디서 봐요?', '노트북은 바닥면 스티커, 모니터는 뒷면 스티커에 적혀 있어요. 마침표(.)가 있는 모델명은 마침표 앞까지만 넣으세요(LG 안내).'),
          ('파일은 어디서 받아지나요?', '모든 버튼은 LG전자 공식 다운로드 서버(gscs-b2c.lge.com)로 바로 연결돼요. 홍라이프 도구는 파일을 올리지 않아요.')]
    fq, fqld = cu.faq(qa)
    main = (kr.HP_CSS + dm.CSS + CSS + f'<header class="top hub">{cr}<h1>LG전자 드라이버 다운로드 — 그램 노트북 LG Update·모니터 OnScreen Control·모델별 파일</h1>'
            f'<p class="lead">LG 그램 노트북 {ng:,}개, LG PC 모니터 {nm:,}개 모델의 드라이버·소프트웨어를 LG전자 공식 서버에서 바로 받고, 설치 순서를 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{ans}</p>' + kr.dl(LGU, 'LG Update 프로그램 바로 받기', '그램 노트북 드라이버 자동 설치 · LG 서버에서 바로 다운로드')
            + '<ul class="dr-toc"><li><a href="#gram">그램 LG Update</a></li><li><a href="#monitor">모니터 OnScreen Control</a></li><li><a href="#models">모델별 파일</a></li><li><a href="#easy">처음이세요?</a></li></ul></header>'
            f'<section class="card dr-sec" id="gram"><h2>LG 그램 노트북: LG Update로 한 번에 설치</h2><p>LG전자는 노트북 드라이버와 전용 소프트웨어를 <b>LG Update 프로그램</b>으로 설치하는 것을 가장 쉽고 안전한 방법으로 안내해요. 빠진 드라이버를 자동으로 찾아 설치해 줘요.</p>{lgu_steps}'
            + kr.dl(LGU, 'LG Update 프로그램 바로 받기', 'LG Update 통합 런처 · LG 서버에서 바로 다운로드') + f'<h3>출시 연도별 LG Update 앱</h3>{years}</section>'
            f'<section class="card dr-sec" id="monitor"><h2>LG 모니터: OnScreen Control·드라이버</h2>{osc}</section>'
            f'<section class="card dr-sec" id="models"><h2>모델별 파일 바로 받기</h2><p>모델명을 입력하거나 아래 목록에서 누르면 그 모델용 파일이 바로 나와요. <b>파란 이름</b>은 LG가 모델별 파일을 올려 둔 모델이에요.</p>'
            + search_box('lgQ', '모델명 입력 (예: 17Z90S, 27GR93U)', '목록에 없는 모델이에요. LG전자 매뉴얼/소프트웨어 다운로드에서 검색하세요.', '찾기')
            + '<div id="lgp"></div>'
            + f'<details class="mg" open><summary>LG 그램·노트북 <span>{ng:,}개 모델</span></summary><div style="padding:0 12px 10px">{chips("gram", lambda k: ("모델명이 " + k + "로 시작 (" + k + "인치대)") if k != "기타" else "기타 모델")}</div></details>'
            + f'<details class="mg"><summary>LG PC 모니터 <span>{nm:,}개 모델</span></summary><div style="padding:0 12px 10px">{chips("monitor", lambda k: (k + "인치 모니터") if k != "기타" else "기타 모델")}</div></details>'
            + f'<p class="cu-src" style="margin-top:10px">모델과 파일 목록은 LG전자 공식 고객지원 \'매뉴얼/소프트웨어 다운로드\'에서 {E(LG["checked"])}에 받아 왔고, 매주 새로 확인해요.</p>'
            + kr.dl(LG_DL, 'LG전자 매뉴얼/소프트웨어 다운로드', '목록에 없을 때: LG 공식 사이트에서 모델 검색', True) + '</section>'
            + kr.guide_pc('LG') + kr.WIN_PC + fq
            + kr.src_sec('LG전자 고객지원(lge.co.kr) \'LG Update 프로그램 설치 가이드\', \'OnScreen Control 사용 방법\', \'매뉴얼/소프트웨어 다운로드\' 모델별 파일')
            + kr.REL + panel_js('ko'))
    ld = [crld, fqld, kr.howto('LG 그램 노트북 드라이버 설치 방법 (LG Update)', ['LG Update 프로그램 다운로드', '압축 풀기', 'LG Update Installer 실행', '확인 눌러 설치', 'LG Update 실행 후 전체 설치'])]
    kr.write(path, 'LG 그램·모니터 드라이버 다운로드 — LG Update·OnScreen Control 바로 받기, 모델별 파일 | 홍라이프 도구',
             f'LG 그램 노트북 드라이버는 LG Update 프로그램으로, LG 모니터는 OnScreen Control로. 그램 {ng:,}개·모니터 {nm:,}개 모델의 랜·무선랜·모니터 드라이버를 LG 공식 서버에서 바로 받고 설치 순서를 쉽게 확인하세요.',
             main, ld)
    return path


def lg_en():
    path = '/en/driver/lg.html'
    cr, crld = en.crumb([('LG drivers', '')])
    ng = len({s for k, c, s, f in LG['models'] if k == 'gram'})
    nm = len({s for k, c, s, f in LG['models'] if k == 'monitor'})
    steps = ('<ol class="big-n"><li>Click <b>Download LG Update</b> (LG Update integrated launcher, straight from LG).</li>'
             '<li>Extract the file, then run <b>LG Update Installer</b>.</li><li>Click <b>OK</b> when it says it will install the LG Update app for your system.</li>'
             '<li>Tick <b>Run LG Update</b>, click <b>Finish</b>, then install everything in the update list.</li></ol>'
             '<p class="tipbox">An internet connection is required. If Wi-Fi/LAN is missing after reinstalling Windows, download your model\'s LAN/WLAN driver below on another PC first.</p>')
    qa = [('Can I download single gram drivers?', 'LG says recent laptops use the LG Update program instead of separate files. Files LG posts per model (e.g. LAN/WLAN) are listed below.'),
          ('Where do files come from?', 'Directly from LG\'s official server (gscs-b2c.lge.com). HongLife Tools does not host files.')]
    fq, fqld = en.faq(qa)
    sb = search_box('lgE', 'Model (e.g. 17Z90S, 27GR93U)', 'Not in this list.', 'Find')
    main = (kr.HP_CSS + dm.CSS + CSS + f'<header class="top hub">{cr}<h1>LG Drivers — gram Laptop (LG Update), Monitor (OnScreen Control), Files by Model</h1>'
            f'<p class="lead">{ng:,} LG gram laptop models and {nm:,} LG PC monitor models, with downloads straight from LG\'s official server.</p>'
            + en.dl(LGU, 'Download LG Update', 'Auto-installs gram drivers · from LG') + '</header>'
            f'<section class="card dr-sec" id="gram"><h2>LG gram: install with LG Update</h2>{steps}</section>'
            '<section class="card dr-sec" id="monitor"><h2>LG monitors: OnScreen Control</h2><p>Split screen, monitor settings and monitor firmware updates from your PC (some models). Firmware updates need a USB cable between PC and monitor.</p>'
            + en.dl(OSC_W, 'OnScreen Control (Windows 10/11)', 'Ver 9.54 · from LG') + en.dl(OSC_M, 'OnScreen Control (Mac)', 'Ver 7.30', True) + '</section>'
            f'<section class="card dr-sec" id="models"><h2>Files by model</h2>{sb}<div id="lgp"></div>'
            + f'<details class="mg" open><summary>LG gram / laptops <span>{ng:,}</span></summary><div style="padding:0 12px 10px">{chips("gram", lambda k: k + " series")}</div></details>'
            + f'<details class="mg"><summary>LG PC monitors <span>{nm:,}</span></summary><div style="padding:0 12px 10px">{chips("monitor", lambda k: k + "-inch")}</div></details>'
            + f'<p class="cu-src">Lists fetched from LG Korea support on {E(LG["checked"])} and refreshed weekly. File names are shown as LG posts them (Korean).</p></section>'
            + en.easy_pc('LG') + en.WIN_PC + fq + en.src('LG Electronics Korea support (lge.co.kr): LG Update install guide, OnScreen Control guide, manuals & software downloads') + en.REL + panel_js('en'))
    en.write(path, 'LG gram & Monitor Driver Download — LG Update, OnScreen Control, Files by Model | HongLife Tools',
             f'Download LG Update for LG gram laptops and OnScreen Control for LG monitors, plus per-model LAN/WLAN and monitor drivers for {ng:,} gram and {nm:,} monitor models from LG\'s official server.',
             main, [crld, fqld])
    return path


if __name__ == '__main__':
    build_json()
    print('\n'.join([lg(), lg_en()]))
