"""홍라이프 도구: 새 분류 '공문서·민원'(/gov/) — 주민센터에 직접 가서 내야 하는 서류 도우미 → overlay/ 에 씀"""
import os, json, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from gov_data import VISIT, FAQ_VISIT
D = os.path.dirname(__file__)
OUT = sys.argv[1]
E = lambda x: html.escape(str(x), quote=True)
HEAD = open(f'{D}/tpl_head.html').read(); MID = open(f'{D}/tpl_mid.html').read()
BRAND = open(f'{D}/tpl_brand.html').read(); TAIL = open(f'{D}/tpl_tail.html').read()
OTHER = open(f'{D}/tpl_other.html', encoding='utf-8').read()
SITE = 'https://honglife.co.kr'; UPD = '2026년 11월 19일'; COLOR = '#0B7285'
LOCK = '<div class="safe"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>입력한 이름·주소는 서버로 전송되지 않고 내 기기에서만 처리돼요</div>'

CSS = """<style id="hl-gov">
.gv-note{margin:12px 0 0;padding:12px 14px;border-radius:12px;background:#E6F6F8;color:#0B4F5C;font-size:14.5px;line-height:1.65;word-break:keep-all}
.gv-warn{margin:12px 0 0;padding:12px 14px;border-radius:12px;background:#FFF4E6;color:#7A3E00;font-size:14.5px;line-height:1.65;word-break:keep-all}
.gv-chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 2px}.gv-chips button{flex:none;padding:7px 11px;border:1px solid var(--line);border-radius:999px;background:#fff;font-size:13px;font-weight:650;color:var(--head);cursor:pointer;white-space:normal;text-align:left}
.gv-chips button:hover{border-color:#0B7285;color:#0B7285}
.gv-acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.gv-acts .btn{flex:1 1 160px}
.gv-h{margin:18px 0 8px!important;font-size:17px!important}
.gv-sheet-wrap{margin-top:14px;border:1px solid var(--line);border-radius:14px;background:#F1F3F5;padding:14px;overflow:hidden}
.gv-sheet{background:#fff;color:#000;max-width:640px;margin:0 auto;padding:26px 24px 30px;font-family:"Pretendard Variable",Pretendard,"Malgun Gothic",sans-serif;box-shadow:0 6px 20px -8px rgba(0,0,0,.25)}
.gv-sheet .lw{font-size:10.5px;color:#333;margin:0 0 10px}
.gv-sheet h3{text-align:center;font-size:24px;letter-spacing:.6em;margin:6px 0 16px!important;font-weight:800;text-indent:.6em}
.gv-sheet table{width:100%;border-collapse:collapse;font-size:12.5px;table-layout:fixed}
.gv-sheet th,.gv-sheet td{border:1px solid #000;padding:7px 6px;vertical-align:middle;word-break:break-all;line-height:1.45}
.gv-sheet th{background:#F4F4F4;font-weight:700;text-align:center}
.gv-sheet td small{display:block;color:#555;font-size:10.5px}
.gv-sheet .v{font-weight:600;min-height:1.4em}
.gv-sheet .stm{margin:16px 2px 6px;font-size:13px;line-height:1.75}
.gv-sheet .dt{text-align:center;margin:16px 0 10px;font-size:13.5px;letter-spacing:.15em}
.gv-sheet .sg{text-align:right;font-size:13.5px;margin:4px 0 0}
.gv-sheet .sg b{display:inline-block;min-width:90px;text-align:center;font-weight:700}
.gv-sheet .to{margin-top:18px;font-size:14px;font-weight:700}
.gv-sheet .ps{margin-top:14px;text-align:right;font-size:10px;color:#444}
.gv-ex{position:relative}.gv-ex::after{content:"작성 예시";position:absolute;right:14px;top:12px;padding:3px 9px;border-radius:999px;background:#C92A2A;color:#fff;font-size:11px;font-weight:800}
.gv-steps{display:grid;gap:10px;margin:8px 0 0;padding:0;list-style:none;counter-reset:s}
.gv-steps li{position:relative;padding:12px 14px 12px 50px;border:1px solid var(--line);border-radius:12px;background:#fff;line-height:1.6;font-size:15px;word-break:keep-all}
.gv-steps li::before{counter-increment:s;content:counter(s);position:absolute;left:14px;top:12px;width:26px;height:26px;border-radius:50%;background:#0B7285;color:#fff;font-weight:800;font-size:14px;display:grid;place-items:center}
.gv-steps li b{color:var(--head)}.gv-steps li em{display:block;font-style:normal;margin-top:4px;padding:6px 10px;border-radius:8px;background:#F8F9FA;font-family:"Nanum Pen Script","Pretendard Variable",cursive;font-size:17px;color:#1c3f94}
.gv-ck{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:6px}.gv-ck li{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:#fff;font-size:15px;line-height:1.55;word-break:keep-all}
.gv-ck input{flex:none;width:20px;height:20px;margin-top:2px;accent-color:#0B7285}
.gv-tab{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 10px}.gv-tab button{flex:1 1 140px;padding:11px 10px;border:1.5px solid var(--line);border-radius:12px;background:#fff;font-weight:700;font-size:14.5px;color:var(--muted);cursor:pointer;white-space:normal}
.gv-tab button[aria-pressed=true]{border-color:#0B7285;background:#E6F6F8;color:#0B4F5C}
.gv-pick{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}
.gv-pick button{display:flex;flex-direction:column;gap:3px;text-align:left;padding:13px 14px;border:1.5px solid var(--line);border-radius:14px;background:#fff;cursor:pointer;min-width:0;white-space:normal}
.gv-pick button b{font-size:15.5px;color:var(--head);line-height:1.35;word-break:keep-all}.gv-pick button span{font-size:12.5px;color:var(--muted);line-height:1.4;word-break:keep-all}
.gv-pick button[aria-pressed=true]{border-color:#0B7285;box-shadow:0 0 0 3px rgba(11,114,133,.15)}
.gv-res{margin-top:16px;border:1px solid var(--line);border-radius:16px;padding:18px 16px;background:linear-gradient(170deg,#EEF8FA,#fff 60%)}
.gv-res h3{margin:0 0 10px!important;font-size:20px!important;line-height:1.3}
.gv-kv{display:grid;grid-template-columns:96px 1fr;gap:6px 12px;margin:0 0 12px;font-size:15px;line-height:1.55}
.gv-kv dt{color:var(--muted);font-weight:700}.gv-kv dd{margin:0;color:var(--head);word-break:keep-all}
.gv-sub{margin:14px 0 6px!important;font-size:15.5px!important;color:var(--head)}
.gv-fee{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin-top:12px}
.gv-fee div{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:#fff}.gv-fee span{display:block;font-size:13px;color:var(--muted)}.gv-fee b{display:block;font-size:20px;margin-top:3px;color:var(--head)}
.gv-fee .hi{background:#0B7285;border-color:#0B7285}.gv-fee .hi span{color:rgba(255,255,255,.85)}.gv-fee .hi b{color:#fff}
.gv-src{font-size:13px!important;color:var(--muted);line-height:1.6}
@media(max-width:520px){.gv-sheet{padding:18px 12px 22px}.gv-sheet table{font-size:11.5px}.gv-sheet h3{font-size:20px}.gv-kv{grid-template-columns:82px 1fr}}
#gvpr{display:none}
@media print{@page{size:A4;margin:14mm}
 body>*:not(#gvpr){display:none!important}
 #gvpr{display:block!important}
 #gvpr .gv-sheet{max-width:none;box-shadow:none;padding:0;margin:0}
 .gv-ex::after{border:1px solid #C92A2A;color:#C92A2A;background:#fff}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap">"""

def page(path, title, desc, crumb, body, ld, js=''):
    url = SITE + path
    h = HEAD + f'<title>{E(title)}</title>\n<meta name="description" content="{E(desc)}">\n<link rel="canonical" href="{url}">\n'
    h += f'<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="홍라이프 도구">\n'
    h += f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{SITE}/assets/og/site.png">\n'
    h += f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/assets/og/site.png">\n'
    h += MID + '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS + '\n</head>\n<body>\n\n' + BRAND
    h += f'<main class="wrap wide"><header class="top"><p class="crumb">{crumb}</p>' + body + '</main>' + js + TAIL
    fp = OUT + (path + 'index.html' if path.endswith('/') else path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(h)

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
def faqld(f):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in f]}
def faqhtml(f):
    return '<section class="card pe-faq"><h2>자주 묻는 질문</h2><dl>' + ''.join(f'<dt>{E(q)}</dt><dd>{E(a)}</dd>' for q, a in f) + '</dl></section>'

TOOLS = []  # (slug, name, lead, kw)
def rel(cur):
    lis = ''.join(f'<li><a href="/gov/{s}.html"><b>{E(n)}</b><span>{E(l[:46])}…</span></a></li>' for s, n, l, _ in TOOLS if s != cur)
    return f'<section class="card rel"><h2>다른 공문서·민원 도구</h2><ul>{lis}<li><a href="/gov/"><b>공문서·민원 모음</b><span>전체 목록 보기</span></a></li></ul></section>'

def tool_page(slug, name, h1, lead, title, desc, kw, tool_html, explain_html, faq, js, src):
    path = f'/gov/{slug}.html'
    crumb = '<a href="/">홈</a> › <a href="/gov/">공문서·민원</a>'
    body = (f'<h1><b>{E(h1)}</b></h1><p class="lead">{E(lead)}</p>{LOCK}</header>'
            f'<section class="card tool" id="tool">{tool_html}</section>'
            f'<section class="card xp" id="explain">{explain_html}<p class="gv-src">근거: {src}</p><p class="note">마지막 확인: {UPD}. 서식과 수수료는 바뀔 수 있으니 방문 전에 주민센터나 정부24에서 한 번 더 확인하세요. 정부·지자체와 관계없는 비공식 도우미예요.</p></section>'
            + faqhtml(faq) + '__REL__')
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebApplication", "name": h1, "url": SITE + path, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}, "description": desc},
          crumbs([('홈', '/'), ('공문서·민원', '/gov/'), (h1, path)]), faqld(faq)]}
    PAGES.append((path, title, desc, crumb, body, ld, js, slug))
    TOOLS.append((slug, name, lead, kw))
PAGES = []

TODAY_JS = "function td(){var d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}function kd(v){if(!v)return'&nbsp;&nbsp;&nbsp;&nbsp;년&nbsp;&nbsp;&nbsp;&nbsp;월&nbsp;&nbsp;&nbsp;&nbsp;일';var p=v.split('-');return p[0]+'년 '+(+p[1])+'월 '+(+p[2])+'일'}function esc(s){return String(s||'').replace(/[&<>\"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]})}function $(i){return document.getElementById(i)}function gvPrint(){var r=document.getElementById('gvpr');if(!r){r=document.createElement('div');r.id='gvpr';document.body.appendChild(r)}var c=$('sheet').cloneNode(true);c.removeAttribute('id');r.innerHTML='';r.appendChild(c);window.print()}"

# ───────────────────────── 1. 민원 위임장 (별지 제3호서식) ─────────────────────────
f = lambda i, l, ph='', t='text', extra='': f'<div class="f"{' style="grid-column:1/-1"' if '주소' in l else ''}><label for="{i}">{l}</label><input id="{i}" type="{t}" placeholder="{E(ph)}" autocomplete="off"{extra}></div>'
POA_TOOL = ('<h2 class="gv-h" style="margin-top:0!important">위임하는 사람 (본인)</h2><div class="grid g2">'
    + f('a1', '이름', '홍길동') + f('a2', '생년월일', '1984-05-12') + f('a3', '주소', '인천광역시 연수구 ○○로 00, 000동 000호') + f('a4', '전화번호', '010-0000-0000', 'tel') + '</div>'
    '<h2 class="gv-h">위임받는 사람 (대리인)</h2><div class="grid g2">'
    + f('b1', '이름', '홍민수') + f('b2', '생년월일', '1990-02-03') + f('b3', '위임하는 사람과의 관계', '형제, 배우자, 자녀 등') + f('b4', '전화번호', '010-0000-0000', 'tel') + f('b5', '주소', '대리인 주소') + '</div>'
    '<h2 class="gv-h">맡길 민원 내용</h2><div class="f"><label for="c1">서류 이름·통수·용도를 구체적으로</label><textarea id="c1" rows="3" placeholder="예: 건강보험 자격득실확인서 1통 발급 (회사 제출용)"></textarea></div>'
    '<div class="gv-chips" id="chips"><button type="button">지방세 납세증명서 1통 발급</button><button type="button">건축물대장 1통 발급</button><button type="button">토지대장 1통 발급</button><button type="button">건강보험 자격득실확인서 1통 발급</button><button type="button">소득금액증명 1통 발급</button><button type="button">장애인증명서 1통 발급</button></div>'
    '<div class="grid g2"><div class="f"><label for="d1">작성일</label><input id="d1" type="date"></div></div>'
    '<div class="gv-acts"><button class="btn" type="button" id="pr">인쇄·PDF로 저장</button><button class="btn ghost" type="button" id="bl">빈 양식 인쇄</button></div>'
    '<p class="gv-note">인쇄한 뒤 <b>위임하는 사람이 직접 서명하거나 도장</b>을 찍어요. 대리인은 이 위임장과 <b>자기 신분증</b>, 위임하는 사람의 신분증을 함께 가져가요.</p>'
    '<p class="gv-warn">주민등록 등·초본, 인감증명서, 전입세대확인서는 이 위임장이 아니라 <b>따로 정해진 서식</b>을 써요. 아래 “어떤 위임장을 써야 하나요?”를 보세요.</p>'
    '<div class="gv-sheet-wrap"><div class="gv-sheet gv-print" id="sheet"></div></div>')
POA_JS = '<script>(function(){' + TODAY_JS + r"""
$('d1').value=td();
function v(i){return esc($(i).value.trim())}
function draw(blank){var g=function(i){return blank?'':v(i)};var c=blank?'':esc($('c1').value.trim()).replace(/\n/g,'<br>');
$('sheet').innerHTML='<p class="lw">■ 민원 처리에 관한 법률 시행규칙 [별지 제3호서식]</p><h3>위임장</h3>'
+'<table><colgroup><col style="width:15%"><col style="width:15%"><col style="width:28%"><col style="width:15%"><col style="width:27%"></colgroup>'
+'<tr><th rowspan="2">위임하는<br>사람</th><th>이름</th><td class="v">'+g('a1')+'</td><th>생년월일</th><td class="v">'+g('a2')+'</td></tr>'
+'<tr><th>주소</th><td class="v">'+g('a3')+'</td><th>전화번호</th><td class="v">'+g('a4')+'</td></tr>'
+'<tr><th rowspan="3">위임받는<br>사람</th><th>이름</th><td class="v">'+g('b1')+'</td><th>생년월일</th><td class="v">'+g('b2')+'</td></tr>'
+'<tr><th>위임하는 사람과의 관계</th><td class="v">'+g('b3')+'</td><th>전화번호</th><td class="v">'+g('b4')+'</td></tr>'
+'<tr><th>주소</th><td class="v" colspan="3">'+g('b5')+'</td></tr>'
+'<tr><th colspan="2" style="height:70px">민원 내용</th><td class="v" colspan="3">'+c+'</td></tr></table>'
+'<p class="stm">위 위임하는 사람은 위 위임받는 사람에게 위 민원 내용의 신청 및 교부에 관한 모든 권리와 의무를 위임합니다.</p>'
+'<p class="dt">'+kd(blank?'':$('d1').value)+'</p>'
+'<p class="sg">위임하는 사람 <b>'+(g('a1')||'&nbsp;')+'</b> (서명 또는 인)</p>'
+'<p class="ps">210mm×297mm[백상지 80g/㎡]</p>';}
['a1','a2','a3','a4','b1','b2','b3','b4','b5','c1','d1'].forEach(function(i){$(i).addEventListener('input',function(){draw()})});
$('chips').onclick=function(e){var b=e.target.closest('button');if(!b)return;var t=$('c1');t.value=(t.value.trim()?t.value.trim()+'\n':'')+b.textContent;draw()};
$('pr').onclick=function(){draw();gvPrint()};$('bl').onclick=function(){draw(true);gvPrint();setTimeout(function(){draw()},500)};
draw();})();</script>"""
POA_EX = ('<h2>어떤 위임장을 써야 하나요?</h2>'
    '<p>관공서 위임장은 아무 종이에나 쓰는 게 아니에요. 법령이 서류마다 서식을 정해 두었어요.</p>'
    '<div class="tbl"><table><thead><tr><th>맡기는 일</th><th>써야 하는 서식</th><th>꼭 지킬 것</th></tr></thead><tbody>'
    '<tr><td>행정기관 민원 일반 (납세증명서, 건축물대장 등)</td><td>민원처리법 시행규칙 별지 제3호서식 — 이 페이지</td><td>신분증명서와 함께 확인해요</td></tr>'
    '<tr><td>주민등록표 등본·초본</td><td>주민등록법 시행규칙 별지 제9호서식</td><td>서명이나 날인만 되고 지문은 안 돼요 → <a href="/gov/resident-copy-poa.html">작성 예시</a></td></tr>'
    '<tr><td>인감증명서</td><td>인감증명법 시행령 별지 제13호서식</td><td>위임자가 직접 손으로 써요 → <a href="/gov/seal-poa.html">작성 예시</a></td></tr>'
    '<tr><td>전입세대확인서</td><td>주민등록법 시행규칙 별지 제15호서식</td><td>방문 신청만 돼요 → <a href="/gov/household-check.html">준비물</a></td></tr>'
    '</tbody></table></div>'
    '<h3>쓰는 요령</h3><ul><li>민원 내용은 “서류 이름 + 통수 + 용도”로 구체적으로 적어요. “관련 서류 일체”처럼 넓게 쓰면 창구에서 다시 물어볼 수 있어요.</li>'
    '<li>위임하는 사람의 서명이나 도장이 꼭 있어야 해요. 대리인이 대신 서명하면 안 돼요.</li>'
    '<li>다른 사람의 서명이나 도장을 몰래 쓰면 형법에 따라 처벌받을 수 있어요.</li></ul>')
tool_page('poa', '민원 위임장 만들기', '민원 위임장 만들기 (별지 제3호서식)',
    '주민센터·구청 같은 행정기관에 가족이 대신 서류를 떼러 갈 때 내는 위임장을, 빈칸만 채워 A4로 바로 인쇄하거나 PDF로 저장해요. 양식은 민원 처리에 관한 법률 시행규칙 별지 제3호서식 항목 그대로예요.',
    '민원 위임장 양식 만들기 | 주민센터 대리 발급 위임장 무료 인쇄 (별지 제3호서식) | 홍라이프 도구',
    '주민센터·구청 민원 서류를 가족이 대신 뗄 때 내는 위임장(민원처리법 시행규칙 별지 제3호서식)을 빈칸만 채워 A4로 인쇄·PDF 저장. 등·초본·인감은 따로 쓰는 서식도 안내.',
    '민원 위임장 양식 주민센터 위임장 대리 발급 위임장 별지 제3호서식 위임장 인쇄',
    POA_TOOL, POA_EX,
    [('위임장에 도장이 꼭 있어야 하나요?', '서명이나 도장 중 하나가 있으면 돼요. 위임하는 사람 본인이 직접 해야 해요.'),
     ('대리인은 무엇을 가져가나요?', '이 위임장, 대리인 본인의 신분증, 위임하는 사람의 신분증(또는 사본)을 가져가요. 기관마다 원본을 요구할 수 있으니 미리 물어보세요.'),
     ('등본도 이 위임장으로 뗄 수 있나요?', '주민등록 등·초본은 주민등록법 시행규칙 별지 제9호서식을 써요. 인감증명서는 별지 제13호서식을 위임자가 직접 손으로 써야 해요.')],
    POA_JS, '민원 처리에 관한 법률 시행규칙 제4조·별지 제3호서식, 주민등록법 시행규칙 별표 1, 인감증명법 시행령 제13조')

# ───────────────────────── 2. 등·초본 대리 발급 위임장 작성 예시 (별지 제9호서식) ─────────────────────────
RC_TOOL = ('<div class="grid g2">'
    + f('a1', '위임한 사람 (등본 주인) 이름', '홍길동') + f('a2', '세대주 이름', '홍길동') + f('a3', '위임한 사람 주소', '인천광역시 연수구 ○○로 00')
    + f('b1', '대리인 (가는 사람) 이름', '홍민수') + f('b2', '위임한 사람과의 관계', '아들') + '</div>'
    '<div class="grid g3"><div class="f"><label for="k">필요한 서류</label><select id="k"><option>등본</option><option>초본</option><option>등본·초본 둘 다</option></select></div>'
    '<div class="f"><label for="n">통수</label><select id="n"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></div>'
    '<div class="f"><label for="r">세대주와의 관계 표기</label><select id="r"><option value="g">일반 (세대원·동거인으로만)</option><option value="d">상세 (부·모·자녀 등)</option></select></div></div>'
    '<div class="f"><label for="u">용도·제출처</label><input id="u" placeholder="예: 은행 대출 서류 제출용" autocomplete="off"></div>'
    '<div class="gv-acts"><button class="btn" type="button" id="pr">작성 예시 인쇄</button></div>'
    '<p class="gv-warn">이 예시를 보고 <b>주민센터에 비치된 위임장(별지 제9호서식)</b>이나 정부24에서 내려받은 서식에 옮겨 적어요. 서식이 2026년 10월 29일에 바뀌었으니 최신 서식을 쓰세요.</p>'
    '<div class="gv-sheet-wrap"><div class="gv-sheet gv-print gv-ex" id="sheet"></div></div>'
    '<h2 class="gv-h">가져갈 것 체크</h2><ul class="gv-ck" id="ck"></ul>')
RC_JS = '<script>(function(){' + TODAY_JS + r"""
function v(i,d){return esc($(i).value.trim())||'<span style="color:#999">'+d+'</span>'}
function draw(){var k=$('k').value,n=$('n').value,det=$('r').value=='d',u=esc($('u').value.trim());
var doc=k=='등본·초본 둘 다'?'등본 '+n+'통, 초본 '+n+'통':k+' '+n+'통';
var rows=[['위임한 사람 성명',v('a1','홍길동'),'본인(등본 주인)의 이름'],['위임한 사람 주민등록번호','000000-0000000','본인 주민등록번호 13자리'],['세대주 성명',v('a2','홍길동'),'본인이 세대주면 본인 이름'],['주소',v('a3','주소'),'주민등록상 주소'],
['위임받은 사람 성명',v('b1','홍민수'),'창구에 가는 사람'],['관계',v('b2','아들'),'위임한 사람과의 관계'],['신청 내용',doc,'필요한 서류와 통수에 √'],['세대주와의 관계',det?'상세':'일반',det?'상세를 고르면 용도·목적을 꼭 적어요':'가족 관계를 드러내지 않고 세대원·동거인으로 표시'],['용도 및 목적',u||(det?'<span style="color:#C92A2A">꼭 적어야 해요</span>':'예: 회사 제출용'),'제출처와 용도를 구체적으로'],['위임한 사람 서명','(서명 또는 인)','본인이 직접 서명하거나 도장 — 지문은 안 돼요']];
$('sheet').innerHTML='<p class="lw">주민등록법 시행규칙 [별지 제9호서식] 주민등록표 열람 또는 등·초본 교부 신청 위임장 — 칸별 작성 예시</p><h3 style="letter-spacing:.1em;text-indent:0;font-size:20px">위임장 작성 예시</h3>'
+'<table><colgroup><col style="width:30%"><col style="width:36%"><col style="width:34%"></colgroup><tr><th>서식의 칸</th><th>이렇게 써요</th><th>요령</th></tr>'
+rows.map(function(r){return '<tr><th>'+r[0]+'</th><td class="v" style="font-family:\'Nanum Pen Script\',cursive;font-size:17px;color:#1c3f94">'+r[1]+'</td><td>'+r[2]+'</td></tr>'}).join('')+'</table>'
+'<p class="stm">작성일: '+kd(td())+' · 이 종이는 작성 예시예요. 제출은 주민센터 비치 서식이나 정부24 최신 서식에 하세요.</p>';
var ck=['위임장 (별지 제9호서식, 위임한 사람이 서명 또는 날인)','위임한 사람의 신분증 (사본)','가는 사람(대리인)의 신분증','수수료 '+(k=='등본·초본 둘 다'?n*2*400:n*400).toLocaleString()+'원 (1통 400원)'];
$('ck').innerHTML=ck.map(function(c,i){return '<li><input type="checkbox" id="c'+i+'"><label for="c'+i+'">'+c+'</label></li>'}).join('');}
['a1','a2','a3','b1','b2','k','n','r','u'].forEach(function(i){$(i).addEventListener('input',draw);$(i).addEventListener('change',draw)});
$('pr').onclick=function(){draw();gvPrint()};draw();})();</script>"""
RC_EX = ('<h2>등본·초본 대리 발급, 이렇게 준비해요</h2>'
    '<h3>누가 위임장 없이 뗄 수 있나요?</h3><p>본인과 같은 세대의 세대원은 신분증만 있으면 창구에서 바로 뗄 수 있어요. 따로 사는 가족이나 다른 사람이 대신 떼려면 위임장이 필요해요.</p>'
    '<h3>온라인으로는 안 되나요?</h3><p>정부24에서는 본인만 신청할 수 있어요. 대리인은 온라인으로 신청할 수 없어서 주민센터를 방문해야 해요.</p>'
    '<h3>2026년 10월 29일부터 달라진 점</h3><p>등·초본에 세대주와의 관계를 「일반」과 「상세」 중에서 골라 표시해요. 「일반」은 세대원·동거인으로만 나오고, 「상세」는 부·모·자녀처럼 나와요. 「상세」를 고르면 용도와 목적을 반드시 적어야 해요. 가족관계를 증명해야 하면 등본 대신 가족관계증명서를 내는 편이 정확해요.</p>'
    '<h3>주의할 점</h3><ul><li>위임한 사람은 서명하거나 도장을 찍어야 하고, 지문(손도장)은 쓸 수 없어요.</li><li>남의 서명·도장을 몰래 써서 위임장을 만들면 형법에 따라 처벌받아요.</li><li>수수료는 창구에서 1통 400원이에요. 소송·경매 목적 등 일부는 500원이에요.</li></ul>')
tool_page('resident-copy-poa', '등본 대리발급 위임장 작성 예시', '등본·초본 대리 발급 위임장 작성 예시',
    '가족이 대신 주민등록 등본·초본을 떼러 갈 때 쓰는 위임장(주민등록법 시행규칙 별지 제9호서식)을 칸별로 어떻게 채우는지 이름만 넣으면 예시로 만들어 줘요. 가져갈 것 체크리스트와 수수료도 같이 보여 줘요.',
    '등본 대리발급 위임장 작성 예시 | 초본 위임장 별지 제9호서식 쓰는 법·준비물 | 홍라이프 도구',
    '주민등록 등본·초본을 가족이 대신 뗄 때 쓰는 위임장(별지 제9호서식) 칸별 작성 예시, 2026년 10월 29일부터 바뀐 세대주 관계 일반·상세 표기, 준비물과 수수료.',
    '등본 대리발급 위임장 초본 위임장 등본 위임장 양식 별지 제9호서식 주민등록등본 대리발급 준비물',
    RC_TOOL, RC_EX,
    [('위임장 양식은 어디서 받나요?', '주민센터 창구에 비치돼 있고, 정부24 민원 안내 “주민등록표 등본(초본) 발급”의 신청서식에서도 내려받을 수 있어요.'),
     ('위임한 사람 신분증은 원본이 필요한가요?', '주민등록법 시행규칙 별표 1은 위임한 사람의 신분증 사본을 내도록 정하고 있어요. 창구에 따라 다를 수 있으니 미리 확인하세요.'),
     ('같이 사는 가족도 위임장이 필요한가요?', '같은 세대원이면 위임장 없이 신분증만으로 뗄 수 있어요.')],
    RC_JS, '주민등록법 시행규칙 제13조·별표 1·별지 제9호서식, 주민등록법 시행규칙 부칙(행정안전부령 제621호, 2026. 10. 29. 시행), 정부24 「주민등록표 등본(초본) 발급」 안내')

# ───────────────────────── 3. 인감증명서 대리 발급 위임장 (별지 제13호서식, 자필) ─────────────────────────
SE_TOOL = ('<div class="grid g2">'
    + f('a1', '위임자 (인감 주인) 이름', '홍길동') + f('a3', '위임자 주소', '인천광역시 연수구 ○○로 00')
    + f('b1', '대리인 이름 (17세 이상)', '홍민수') + f('b2', '위임자와의 관계', '아들') + '</div>'
    '<div class="grid g3"><div class="f"><label for="u">용도</label><select id="u"><option>일반용</option><option>부동산 매도용</option><option>자동차 매도용</option><option>근저당 설정용</option><option>금융기관 제출용</option><option>법원 제출용</option></select></div>'
    '<div class="f"><label for="n">발급 통수</label><select id="n"><option>1</option><option>2</option><option>3</option></select></div>'
    '<div class="f"><label for="d1">위임하는 날</label><input id="d1" type="date"></div></div>'
    '<div class="f"><label for="w">위임 사유</label><input id="w" placeholder="예: 직장 근무로 평일 방문이 어려움" autocomplete="off"></div>'
    '<div class="gv-fee"><div class="hi"><span>위임장 유효기간</span><b id="exp">-</b></div><div><span>수수료</span><b id="fee">-</b></div></div>'
    '<p class="gv-warn"><b>인감증명서 위임장은 위임자가 직접 손으로 써야 해요.</b> 프린터로 채워 인쇄하면 안 받아 줘요. 아래 예시를 보고 주민센터에 비치된 별지 제13호서식(또는 정부24에서 내려받은 서식)에 따라 쓰세요.</p>'
    '<ol class="gv-steps" id="steps"></ol>'
    '<div class="gv-acts"><button class="btn ghost" type="button" id="pr">예시 인쇄해서 옆에 두고 쓰기</button></div>'
    '<div class="gv-sheet-wrap" style="display:none"><div class="gv-sheet gv-print gv-ex" id="sheet"></div></div>'
    '<h2 class="gv-h">가져갈 것 체크</h2><ul class="gv-ck" id="ck"></ul>')
SE_JS = '<script>(function(){' + TODAY_JS + r"""
$('d1').value=td();
function v(i,d){return esc($(i).value.trim())||d}
function draw(){var u=$('u').value,n=+$('n').value,d=$('d1').value;
var e=new Date(d);e.setMonth(e.getMonth()+6);e.setDate(e.getDate()-1);
$('exp').textContent=isNaN(e)?'-':(e.getFullYear()+'. '+(e.getMonth()+1)+'. '+e.getDate()+'.까지');$('fee').textContent=(n*600).toLocaleString()+'원';
var sale=/매도/.test(u);
var st=[['맨 위 구분','<b>[√] 인감증명서 발급 위임장</b> 칸에 체크해요.','√ 인감증명서 발급 위임장'],
['위임자 성명','본인 이름을 쓰고 옆에 서명하거나 도장을 찍어요. 도장은 인감도장이 아니어도 돼요.',v('a1','홍길동')+' (서명)'],
['주민등록번호·주소','위임자의 주민등록번호와 주소를 그대로 써요.',v('a3','인천광역시 연수구 ○○로 00')],
['신분증','들려 보낼 위임자 신분증 종류를 써요.','주민등록증'],
['용도','제출처에서 요구하는 용도를 구체적으로 써요. “모든 권한 위임”처럼 쓰면 안 돼요.',u+(sale?' (매수자 정보 필요)':'')],
['발급통수','숫자로 써요. 비워 두면 1통만 나와요.',n+'통'],
['대리인','성명·주민등록번호·주소·관계를 써요. 대리인은 17세 이상이어야 해요.',v('b1','홍민수')+' / 관계: '+v('b2','아들')],
['위임 사유','왜 직접 못 가는지 짧게 써요.',v('w','직장 근무로 평일 방문이 어려움')],
['날짜','위임하는 날을 써요. 이날부터 6개월 동안 유효해요.',kd(d)]];
if(sale)st.push(['매수자 정보','부동산·자동차 매도용이면 매수자의 성명·주민등록번호·주소가 필요해요. 대리인이 창구에서 알려 줄 수 있게 적어 보내요.','매수자 성명 / 주민등록번호 / 주소']);
$('steps').innerHTML=st.map(function(s){return '<li><b>'+s[0]+'</b> — '+s[1]+'<em>'+s[2]+'</em></li>'}).join('');
$('sheet').innerHTML='<p class="lw">인감증명법 시행령 [별지 제13호서식] 인감증명서 발급 위임장 — 손글씨 작성 예시 (제출용 아님)</p><h3 style="letter-spacing:.1em;text-indent:0;font-size:20px">따라 쓰기 예시</h3><table><colgroup><col style="width:28%"><col></colgroup>'+st.map(function(s){return '<tr><th>'+s[0]+'</th><td class="v" style="font-family:\'Nanum Pen Script\',cursive;font-size:18px;color:#1c3f94">'+s[2]+'</td></tr>'}).join('')+'</table><p class="stm">유효기간: '+$('exp').textContent+' · 수수료 '+$('fee').textContent+'</p>';
var ck=['위임장 — 위임자가 직접 손으로 작성 (별지 제13호서식)','위임자 신분증 (주민등록증·운전면허증·여권 등)','대리인 신분증','수수료 '+(n*600).toLocaleString()+'원'];if(sale)ck.push('매수자의 성명·주민등록번호·주소');
$('ck').innerHTML=ck.map(function(c,i){return '<li><input type="checkbox" id="c'+i+'"><label for="c'+i+'">'+c+'</label></li>'}).join('');}
['a1','a3','b1','b2','u','n','d1','w'].forEach(function(i){$(i).addEventListener('input',draw);$(i).addEventListener('change',draw)});
$('pr').onclick=function(){draw();gvPrint()};draw();})();</script>"""
SE_EX = ('<h2>인감증명서 대리 발급, 이렇게 준비해요</h2>'
    '<h3>왜 손으로 써야 하나요?</h3><p>인감증명서는 부동산·자동차 거래처럼 큰 재산이 오가는 데 쓰이기 때문에, 서식 안내문이 위임자가 직접 작성하도록 정하고 있어요. 그래서 컴퓨터로 채워 인쇄한 위임장은 받아 주지 않아요.</p>'
    '<h3>온라인 발급과의 차이</h3><p>2024년 9월 30일부터 정부24에서 일부 일반용 인감증명서를 본인이 온라인으로 받을 수 있어요. 하지만 부동산·자동차 매도용, 법원·금융기관 제출용은 온라인으로 안 되고, 대리인은 온라인 신청을 할 수 없어요.</p>'
    '<h3>인감증명서 대신 쓸 수 있는 것</h3><p>제출처가 허락하면 본인서명사실확인서로 대신할 수 있어요. 인감도장 등록 없이 본인이 주민센터에서 서명하면 발급되고, 2028년 12월 31일까지 수수료가 없어요. 다만 본인서명사실확인서는 대리 발급이 안 돼요.</p>'
    '<h3>주의할 점</h3><ul><li>위임장은 위임한 날부터 6개월 동안만 써요.</li><li>주민등록이 말소된 사람(국외이주 말소 제외)이나 거주불명 등록자는 위임할 수 없어요.</li><li>미성년자의 인감증명서는 위임장과 함께 법정대리인 동의서가 필요해요.</li><li>남의 도장·서명을 위조하거나 몰래 써서 발급받으면 형법에 따라 처벌받아요.</li></ul>')
tool_page('seal-poa', '인감증명서 대리발급 위임장 작성 예시', '인감증명서 대리발급 위임장 작성 예시',
    '가족이 대신 인감증명서를 떼러 갈 때 필요한 위임장(인감증명법 시행령 별지 제13호서식)은 위임자가 직접 손으로 써야 해요. 이름과 용도만 넣으면 칸별로 따라 쓸 예시, 유효기간(6개월), 수수료, 준비물을 정리해 줘요.',
    '인감증명서 대리발급 위임장 작성 예시 | 별지 제13호서식 쓰는 법·유효기간·준비물 | 홍라이프 도구',
    '인감증명서 대리발급 위임장(별지 제13호서식)은 위임자 자필 작성. 칸별 따라 쓰기 예시, 위임장 유효기간 6개월 계산, 매도용 매수자 정보, 수수료 600원, 준비물 체크리스트.',
    '인감증명서 대리발급 위임장 인감 위임장 작성법 별지 제13호서식 인감증명서 위임장 양식 인감 대리발급 준비물',
    SE_TOOL, SE_EX,
    [('인감 위임장에 인감도장을 찍어야 하나요?', '서식 안내에 따르면 위임자 서명은 사인 형태도 되고, 날인은 인감도장이 아니어도 돼요.'),
     ('대리인은 누구나 될 수 있나요?', '17세 이상이면 가족이 아니어도 될 수 있어요. 위임자와 대리인 신분증을 모두 가져가야 해요.'),
     ('위임장을 작년에 써 둔 게 있어요.', '위임장은 위임한 날부터 6개월 동안만 유효해요. 지났다면 새로 써야 해요.')],
    SE_JS, '인감증명법 시행령 제13조·제19조·별지 제13호서식, 본인서명사실 확인 등에 관한 법률 시행령, 정부24 인감증명서 발급 안내')

# ───────────────────────── 4. 전입세대확인서 (방문 전용) ─────────────────────────
HC_TOOL = ('<h2 class="gv-h" style="margin-top:0!important">누가 신청하나요?</h2>'
    '<div class="gv-tab" id="who"><button type="button" aria-pressed="true" data-v="ten">임차인·임대차 계약 당사자</button><button type="button" aria-pressed="false" data-v="own">집주인(소유자)</button><button type="button" aria-pressed="false" data-v="buy">매매 계약 당사자</button></div>'
    '<div class="gv-tab" id="how"><button type="button" aria-pressed="true" data-v="me">내가 직접 가요</button><button type="button" aria-pressed="false" data-v="px">다른 사람이 대신 가요</button></div>'
    '<div class="grid g3"><div class="f"><label for="cnt">확인할 건물 수</label><select id="cnt"><option>1</option><option>2</option><option>3</option></select></div>'
    '<div class="f"><label for="mode">받는 방법</label><select id="mode"><option value="r">열람 (보기만)</option><option value="i">교부 (종이로 받기)</option></select></div>'
    '<div class="f"><label for="both">지번·도로명 주소</label><select id="both"><option value="2">둘 다 (추천)</option><option value="1">한 가지만</option></select></div></div>'
    '<div class="gv-fee" id="fee"></div>'
    '<h2 class="gv-h">가져갈 것 체크</h2><ul class="gv-ck" id="ck"></ul>'
    '<p class="gv-warn">전입세대확인서는 <b>온라인 신청이 안 돼요.</b> 전국 어느 행정복지센터(주민센터)나 시군구청에 가서 신청해요.</p>')
HC_JS = '<script>(function(){' + TODAY_JS + r"""
var S={who:'ten',how:'me'};
['who','how'].forEach(function(g){$(g).onclick=function(e){var b=e.target.closest('button');if(!b)return;S[g]=b.dataset.v;$(g).querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});draw()}});
function draw(){var c=+$('cnt').value,m=$('mode').value,b=+$('both').value;var unit=m=='r'?300:400,tot=c*b*unit;
$('fee').innerHTML='<div class="hi"><span>예상 수수료</span><b>'+tot.toLocaleString()+'원</b></div><div><span>계산</span><b style="font-size:15px">'+c+'곳 × 주소 '+b+'가지 × '+unit+'원</b></div>';
var proof={ten:'임대차계약서 (임차인·임대차 계약 당사자임을 보여 주는 서류)',own:'등기사항증명서·건축물대장 등 소유자임을 보여 주는 서류',buy:'매매계약서 (매매 계약 당사자임을 보여 주는 서류)'}[S.who];
var ck=S.how=='me'?['신분증',proof+' — 행정정보로 확인되면 생략될 수 있어요','신청서 (전입세대확인서 열람 또는 교부 신청서, 창구 비치 · 별지 제15호서식)','확인할 집 주소 (지번 주소와 도로명 주소 둘 다 적어 가기)']:['대리인(가는 사람)의 신분증','위임장 (주민등록법 시행규칙 별지 제15호서식)','위임한 사람의 신분증',proof,'확인할 집 주소 (지번·도로명)'];
ck.push('수수료 '+tot.toLocaleString()+'원 (교부는 400원 또는 500원이라 조금 다를 수 있어요)');
$('ck').innerHTML=ck.map(function(x,i){return '<li><input type="checkbox" id="c'+i+'"><label for="c'+i+'">'+x+'</label></li>'}).join('');}
['cnt','mode','both'].forEach(function(i){$(i).addEventListener('change',draw)});draw();})();</script>"""
HC_EX = ('<h2>전입세대확인서, 이렇게 읽고 써요</h2>'
    '<h3>무엇을 확인하는 서류인가요?</h3><p>특정 건물 주소에 주민등록된 세대주와 동거인의 이름, 전입일자를 보여 줘요. 말소되거나 거주불명 등록된 사람도 포함돼요. 전세·월세 계약 전에 먼저 들어와 사는 세입자(선순위 임차인)가 있는지 볼 때 많이 써요.</p>'
    '<h3>누가 신청할 수 있나요?</h3><ul><li>집주인(소유자)과 그 세대원 — 등기사항증명서나 건축물대장 등으로 증명</li><li>임차인과 그 세대원, 임대차 계약 당사자 — 임대차계약서로 증명</li><li>매매 계약 당사자 — 매매계약서로 증명</li><li>경매 참가자, 금융기관 등 법에서 정한 사람</li></ul>'
    '<p>계약서를 쓰기 전이라 증명할 서류가 없으면 신청이 어려울 수 있어요. 이럴 때는 집주인에게 전입세대확인서를 떼어 보여 달라고 요청하세요.</p>'
    '<h3>결과를 볼 때 팁</h3><ul><li>지번 주소와 도로명 주소로 조회한 결과가 다르게 나올 수 있어요. 두 가지 모두 확인하면 숨은 세대를 놓칠 가능성이 줄어요.</li><li>배우자·자녀 같은 세대원은 표시되지 않고 세대주와 동거인만 나와요.</li><li>다가구주택은 등기부등본의 근저당과 함께 보고, 내 보증금보다 앞서는 보증금이 얼마인지 따져 보세요.</li></ul>')
tool_page('household-check', '전입세대확인서 준비물·수수료', '전입세대확인서 (전입세대 열람) 준비물·수수료',
    '전세·월세 계약 전후에 그 집에 누가 전입해 있는지 확인하는 전입세대확인서는 주민센터에 가서만 신청할 수 있어요. 누가 가는지만 고르면 준비물 체크리스트와 예상 수수료, 결과 읽는 법을 알려 줘요.',
    '전입세대확인서 발급 준비물·수수료 | 전입세대 열람 방문 신청, 대리 위임장 | 홍라이프 도구',
    '전입세대확인서(전입세대 열람)는 방문 신청만 가능. 임차인·집주인·매매 당사자별 준비물, 대리 신청 위임장(별지 제15호서식), 열람 300원·교부 수수료 계산, 지번·도로명 둘 다 확인하는 팁.',
    '전입세대확인서 발급 전입세대 열람 준비물 전입세대열람원 수수료 전세 계약 선순위 임차인 확인',
    HC_TOOL, HC_EX,
    [('전입세대확인서는 인터넷으로 뗄 수 있나요?', '아니요. 정부24 안내상 신청 방법은 방문뿐이에요. 전국 행정복지센터나 시군구청 어디서나 신청할 수 있어요.'),
     ('수수료는 얼마인가요?', '정부24 안내 기준 열람은 건물 1곳당 300원, 교부는 400원 또는 500원이에요.'),
     ('세대원은 왜 안 나오나요?', '전입세대확인서는 세대주와 동거인의 이름과 전입일만 보여 주는 서류라, 배우자·자녀 같은 세대원은 따로 표시되지 않아요.')],
    HC_JS, '주민등록법 제29조의2, 주민등록법 시행규칙 제14조·별표 2·별지 제15호서식, 정부24 「전입세대확인서 열람·발급」 안내')

# ───────────────────────── 5. 주민센터 방문 서류 준비물 찾기 ─────────────────────────
VD_TOOL = ('<h2 class="gv-h" style="margin-top:0!important">무슨 일로 가세요?</h2><div class="gv-pick" id="pick">'
    + ''.join(f'<button type="button" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}"><b>{E(x["name"])}</b><span>{E(x["short"])}</span></button>' for i, x in enumerate(VISIT))
    + '</div><div class="gv-tab" id="how" style="margin-top:14px"><button type="button" aria-pressed="true" data-v="self">본인이 가요</button><button type="button" aria-pressed="false" data-v="proxy">가족·다른 사람이 대신 가요</button></div>'
    '<div class="gv-res" id="res"></div>')
VD_JS = '<script>(function(){' + TODAY_JS + 'var V=' + json.dumps(VISIT, ensure_ascii=False) + r""";var S={i:0,how:'self'};
$('pick').onclick=function(e){var b=e.target.closest('button');if(!b)return;S.i=+b.dataset.i;$('pick').querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});draw();$('res').scrollIntoView({behavior:'smooth',block:'nearest'})};
$('how').onclick=function(e){var b=e.target.closest('button');if(!b)return;S.how=b.dataset.v;$('how').querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});draw()};
function draw(){var x=V[S.i],L=S.how=='self'?x.self:x.proxy;
$('res').innerHTML='<h3>'+esc(x.name)+'</h3><dl class="gv-kv"><dt>어디서</dt><dd>'+esc(x.where)+'</dd><dt>온라인</dt><dd>'+esc(x.online)+'</dd><dt>수수료</dt><dd>'+esc(x.fee)+'</dd></dl>'
+'<p class="gv-sub">'+(S.how=='self'?'본인이 갈 때 챙길 것':'대신 갈 때 챙길 것')+'</p><ul class="gv-ck">'+L.map(function(c,i){return '<li><input type="checkbox" id="k'+i+'"><label for="k'+i+'">'+esc(c)+'</label></li>'}).join('')+'</ul>'
+'<p class="gv-sub">알아 둘 점</p><ul>'+x.notes.map(function(n){return '<li>'+esc(n)+'</li>'}).join('')+'</ul>'
+(x.link?'<div class="gv-acts"><a class="btn" href="'+x.link+'">작성 예시·자세한 준비 보기</a></div>':'');}
draw();})();</script>"""
VD_EX = ('<h2>주민센터에 꼭 가야 하는 일, 미리 알면 한 번에 끝나요</h2>'
    '<p>요즘은 등본·가족관계증명서처럼 본인이 인터넷으로 떼는 서류가 많아요. 그래도 대리인이 떼거나, 본인 확인이 꼭 필요한 일은 여전히 창구에 가야 해요. 다시 가는 일을 막으려면 세 가지만 확인하세요.</p>'
    '<ul><li><b>누가 가는지</b> — 본인이 아니면 위임장과 두 사람의 신분증이 필요한 경우가 많아요.</li><li><b>어떤 서식인지</b> — 등·초본, 인감, 전입세대확인서는 위임장 서식이 각각 정해져 있어요.</li><li><b>대리가 되는 일인지</b> — 본인서명사실확인서처럼 본인만 되는 일도 있어요.</li></ul>'
    '<p>목록에 없는 민원은 정부24 민원 안내에서 이름으로 찾으면 신청 방법(방문·인터넷), 구비서류, 수수료를 볼 수 있어요.</p>')
tool_page('visit-docs', '주민센터 방문 서류 준비물 찾기', '주민센터 방문 서류 준비물 찾기',
    '등본 대리 발급, 인감증명서, 본인서명사실확인서, 전입세대확인서, 인감 신고, 장애인 등록처럼 주민센터에 직접 가야 하는 일을 고르면, 본인·대리인별 준비물과 수수료, 온라인 가능 여부를 한 번에 보여 줘요.',
    '주민센터 방문 서류 준비물 찾기 | 대리 발급·인감·전입세대확인서 준비물과 수수료 | 홍라이프 도구',
    '주민센터(행정복지센터)에 직접 가야 하는 민원별 준비물·수수료·온라인 가능 여부. 등본 대리 발급, 인감증명서, 본인서명사실확인서, 전입세대확인서, 인감 신고, 장애인 등록, 전입신고 대리.',
    '주민센터 준비물 행정복지센터 서류 대리 발급 준비물 인감증명서 준비물 본인서명사실확인서 전입세대확인서 장애인 등록 서류',
    VD_TOOL, VD_EX, FAQ_VISIT, VD_JS,
    '주민등록법·시행규칙, 인감증명법 시행령, 본인서명사실 확인 등에 관한 법률 시행령, 장애인복지법 시행규칙 제3조, 정부24 민원 안내, 지자체 민원 안내 (2026년 11월 확인)')

# 허브 순서: 준비물 찾기 → 위임장 → 예시들 → 전입세대
ORDER = ['visit-docs', 'poa', 'resident-copy-poa', 'seal-poa', 'household-check']
TOOLS.sort(key=lambda t: ORDER.index(t[0]))
for path, title, desc, crumb, body, ld, js, slug in PAGES:
    page(path, title, desc, crumb, body.replace('__REL__', rel(slug)), ld, js)

# 썸네일(허브 카드)
ICON = {'visit-docs': '<rect x="8" y="6" width="28" height="34" rx="4"/><path d="M14 16h16M14 23h16M14 30h9"/><path d="M28 32l3 3 6-7"/>',
        'poa': '<rect x="9" y="5" width="26" height="36" rx="3"/><path d="M15 14h14M15 20h14"/><path d="M15 32c3-4 5 2 8-2s4 2 6 0"/>',
        'resident-copy-poa': '<rect x="7" y="7" width="22" height="30" rx="3"/><rect x="15" y="11" width="22" height="30" rx="3" fill="#0B7285"/><path d="M20 20h12M20 26h12M20 32h7"/>',
        'seal-poa': '<circle cx="22" cy="15" r="8"/><path d="M18 23h8v8h-8z"/><rect x="10" y="31" width="24" height="8" rx="2"/>',
        'household-check': '<path d="M7 22L22 9l15 13"/><path d="M11 20v18h22V20"/><circle cx="22" cy="28" r="4"/><path d="M25 31l4 4"/>'}
def thumb(slug, title):
    c, bg = COLOR, '#D7EEF2'
    lab = {'visit-docs':'방문 준비물','poa':'민원 위임장','resident-copy-poa':'등본 위임장','seal-poa':'인감 위임장','household-check':'전입세대 확인'}[slug]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="64.0 6.0 72.0 128.0" width="72" height="128"><g>'
            '<rect x="64" y="6" width="72" height="128" rx="12" fill="#1A1D24"/><rect x="68" y="10" width="64" height="120" rx="9" fill="#fff"/><rect x="91.0" y="13" width="18" height="4" rx="2" fill="#1A1D24"/>'
            f'<text x="74" y="32" font-family="Arial,Helvetica,sans-serif" font-size="8.5" font-weight="700" fill="#1A1D24">{E(lab)}</text>'
            f'<rect x="76" y="40" width="48" height="48" rx="13" fill="{c}"/>'
            f'<g transform="translate(78 42) scale(.917)" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">{ICON[slug]}</g>'
            f'<rect x="74" y="94" width="52" height="5" rx="2.5" fill="{bg}"/><rect x="74" y="94" width="{20 + (sum(map(ord, slug)) % 30)}" height="5" rx="2.5" fill="{c}"/>'
            f'<rect x="72" y="106" width="56" height="12" rx="6" fill="{c}"/><text x="83" y="114.6" font-family="Arial,Helvetica,sans-serif" font-size="8" font-weight="700" fill="#fff">작성하기</text>'
            '</g></svg>')
os.makedirs(OUT + '/assets/art/hl/t', exist_ok=True)
for s, n, l, k in TOOLS:
    open(OUT + f'/assets/art/hl/t/gov-{s}.svg', 'w').write(thumb(s, n))
PG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"><rect x="2" y="2" width="60" height="60" rx="14" fill="#fff" stroke="#1f2430" stroke-opacity=".18" stroke-width="2"/><g fill="none" stroke="#1f2430" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 26L32 13l18 13"/><path d="M18 26v22h28V26"/><path d="M26 48V36h12v12"/></g></svg>'
open(OUT + '/assets/art/hl/pg-gov.svg', 'w').write(PG)
CS = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="30.0 18.0 140.0 106.0" width="140" height="106"><g>'
      '<rect x="30" y="18" width="140" height="106" rx="9" fill="#fff"/><rect x="30" y="18" width="140" height="18" rx="9" fill="#0B7285"/><rect x="30" y="28" width="140" height="8" fill="#0B7285"/>'
      '<text x="40" y="30" font-family="Arial,Helvetica,sans-serif" font-size="8" font-weight="700" fill="#fff">위임장 · 주민센터 준비물</text>'
      '<rect x="44" y="46" width="62" height="70" rx="4" fill="#fff" stroke="#1A1D24" stroke-width="1.6"/><text x="62" y="58" font-family="Arial,Helvetica,sans-serif" font-size="7" font-weight="700" fill="#1A1D24">위 임 장</text>'
      '<path d="M50 66h50M50 74h50M50 82h50M50 90h32" stroke="#C5D9DE" stroke-width="3" stroke-linecap="round"/><path d="M76 106c4-6 8 3 12-3s5 3 8 0" fill="none" stroke="#1c3f94" stroke-width="1.8" stroke-linecap="round"/>'
      '<circle cx="96" cy="100" r="7" fill="none" stroke="#E03131" stroke-width="2"/>'
      '<rect x="116" y="48" width="44" height="12" rx="6" fill="#E6F6F8"/><path d="M121 54l3 3 5-6" stroke="#0B7285" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="132" y="52" width="22" height="4" rx="2" fill="#0B7285"/>'
      '<rect x="116" y="66" width="44" height="12" rx="6" fill="#E6F6F8"/><path d="M121 72l3 3 5-6" stroke="#0B7285" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="132" y="70" width="18" height="4" rx="2" fill="#0B7285"/>'
      '<rect x="116" y="84" width="44" height="12" rx="6" fill="#E6F6F8"/><path d="M121 90l3 3 5-6" stroke="#0B7285" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="132" y="88" width="24" height="4" rx="2" fill="#0B7285"/>'
      '<rect x="116" y="104" width="44" height="12" rx="6" fill="#0B7285"/><text x="125" y="112.5" font-family="Arial,Helvetica,sans-serif" font-size="7" font-weight="700" fill="#fff">인쇄하기</text>'
      '</g></svg>')
open(OUT + '/assets/art/hl/cs-gov.svg', 'w').write(CS)

# 허브
H1 = '공문서·민원'
lead = '주민센터·구청에 직접 가서 내야 하는 서류를 준비하는 도구 모음이에요. 민원 위임장을 바로 인쇄하고, 등본·인감증명서 대리 발급 위임장 작성 예시와 전입세대확인서 준비물, 민원별 준비물·수수료를 확인해요.'
lis = ''.join(f'<li><a href="/gov/{s}.html"><i class="th"><img src="/assets/art/hl/t/gov-{s}.svg" alt="" width="200" height="140" loading="lazy"></i><img class="pg" src="/assets/art/hl/pg-gov.svg" alt="" width="26" height="26" loading="lazy"><b>{E(n)}</b><span>{E(l[:60])}…</span></a></li>' for s, n, l, k in TOOLS)
body = f'<h1>{E(H1)}</h1><p class="lead">{E(lead)}</p>{LOCK}</header><section class="card"><h2>{H1} 도구 {len(TOOLS)}가지</h2><ul class="tlist hl-grid">{lis}</ul></section>' + OTHER
ld = {"@context": "https://schema.org", "@graph": [{"@type": "CollectionPage", "name": H1, "url": SITE + '/gov/', "hasPart": [{"@type": "WebApplication", "name": n, "url": f'{SITE}/gov/{s}.html'} for s, n, l, k in TOOLS]}, crumbs([('홈', '/'), (H1, '/gov/')])]}
page('/gov/', '공문서·민원 도우미 | 민원 위임장 인쇄·대리 발급 위임장 예시·주민센터 준비물 | 홍라이프 도구',
     '주민센터·구청 방문 민원 도우미 모음. 민원 위임장(별지 제3호서식) 인쇄, 등본·인감증명서 대리발급 위임장 작성 예시, 전입세대확인서 준비물·수수료, 민원별 준비물 찾기.',
     f'<a href="/">홈</a> › {H1}', body, ld)
fp = OUT + '/gov/index.html'
s = open(fp, encoding='utf-8').read().replace('<header class="top"><p class="crumb">', '<header class="top hub"><p class="crumb">', 1)
open(fp, 'w', encoding='utf-8').write(s)
json.dump([[f'/gov/{s}.html', n, l[:70], k] for s, n, l, k in TOOLS], open(OUT + '/govcats.json', 'w'), ensure_ascii=False)
print('gov pages', len(TOOLS) + 1)
