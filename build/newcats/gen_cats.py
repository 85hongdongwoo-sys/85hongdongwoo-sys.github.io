"""홍라이프 도구: 새 분류 2개(심리 테스트 /test/, 게임 계산기 /game/) 페이지 생성 → overlay/ 에 씀"""
import os, json, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from data_tests import TESTS
from data_games import GAMES
from data_tests_extra import EXTRA
import re as _re
for _t in TESTS:
    _t['q'] = _t['q'] + EXTRA.get(_t['slug'], [])
    _t['lead'] = _re.sub(r'\d+문항', f"{len(_t['q'])}문항", _t['lead'])
D = os.path.dirname(__file__)
OUT = sys.argv[1]  # repo/overlay
E = lambda x: html.escape(str(x), quote=True)
HEAD = open(f'{D}/tpl_head.html').read()
MID = open(f'{D}/tpl_mid.html').read()
BRAND = open(f'{D}/tpl_brand.html').read()
TAIL = open(f'{D}/tpl_tail.html').read()
SITE = 'https://honglife.co.kr'
UPD = '2026년 11월 18일'
LOCK = '<div class="safe"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>입력한 답과 결과는 서버로 전송되지 않고 내 기기에서만 처리돼요</div>'
CAT = {'test': ('심리 테스트', '심리·성격 테스트', '#C2255C'), 'game': ('게임 계산기', '게임 계산기·놀이', '#2B8A3E')}

CSS = """<style id="hl-newcat">
.qz{display:grid;gap:12px;margin-top:6px}
.qz .qi{border:1px solid var(--line);border-radius:14px;padding:14px 14px 12px;background:#fff}
.qz .qi.on{border-color:var(--acc);box-shadow:0 0 0 2px rgba(49,130,246,.12)}
.qz .qt{font-weight:700;font-size:15.5px;line-height:1.5;color:var(--head);margin:0 0 10px;word-break:keep-all}
.qz .qt i{font-style:normal;color:var(--acc);margin-right:6px}
.qz .lk{display:grid;grid-template-columns:repeat(var(--n,5),1fr);gap:6px}
.qz .lk button{flex:none;min-height:44px;padding:6px 2px;font-size:12.5px;font-weight:650;border:1px solid var(--line);background:var(--paper2,#f6f7f9);border-radius:10px;color:var(--muted);white-space:normal;line-height:1.25}
.qz .lk button[aria-pressed=true]{background:var(--acc);border-color:var(--acc);color:#fff}
.qbar{position:sticky;top:0;z-index:3;background:rgba(255,255,255,.92);backdrop-filter:blur(6px);padding:10px 0;margin:-4px 0 4px}
.qbar .pg{height:8px;border-radius:99px;background:var(--line);overflow:hidden}.qbar .pg i{display:block;height:100%;width:0;background:var(--acc);transition:width .25s}
.qbar p{margin:6px 0 0;font-size:13px;color:var(--muted)}
.qres{margin-top:18px;border-radius:18px;padding:22px 18px;background:linear-gradient(160deg,#F3F7FF,#FFF);border:1px solid var(--line)}
.qres .tag{display:inline-block;font-size:13px;font-weight:700;color:var(--acc);margin-bottom:6px}
.qres h2{margin:0 0 8px!important;font-size:26px!important;line-height:1.25}
.qres .sc{font-size:15px;color:var(--muted);margin:0 0 12px}
.qres p.d{font-size:16px;line-height:1.7;color:var(--head);margin:0 0 12px;word-break:keep-all}
.qres ul.tips{margin:0;padding-left:20px;line-height:1.75}
.qbars{display:grid;gap:8px;margin:14px 0}
.qbars div{display:grid;grid-template-columns:96px 1fr 44px;gap:8px;align-items:center;font-size:14px}
.qbars span{color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.qbars i{display:block;height:10px;border-radius:99px;background:var(--line);overflow:hidden}.qbars i em{display:block;height:100%;background:var(--acc);border-radius:99px}
.qbars b{text-align:right;font-variant-numeric:tabular-nums}
.qbars .top span,.qbars .top b{color:var(--head);font-weight:800}
.qmap{position:relative;width:100%;max-width:320px;aspect-ratio:1;margin:12px auto;border:1px solid var(--line);border-radius:12px;background:linear-gradient(90deg,transparent 49.6%,var(--line) 49.6% 50.4%,transparent 50.4%),linear-gradient(transparent 49.6%,var(--line) 49.6% 50.4%,transparent 50.4%)}
.qmap span{position:absolute;font-size:12px;color:var(--muted);font-weight:700}
.qmap .dot{position:absolute;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 5px rgba(49,130,246,.2)}
.qalert{margin:0 0 16px;padding:14px 16px;border-radius:12px;background:#FFF0F0;border:1px solid #F5B5B5;font-size:15px;line-height:1.65;color:#5a1414}.qalert a{font-weight:800;color:#C92A2A}
.qcare{margin-top:12px;padding:12px 14px;border-radius:12px;background:#FFF8E6;font-size:14px;line-height:1.6;color:#5c4400}
.gm-out{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-top:14px}
.gm-out div{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:#fff}
.gm-out span{display:block;font-size:13px;color:var(--muted)}
.gm-out b{display:block;font-size:20px;margin-top:4px;font-variant-numeric:tabular-nums;color:var(--head);word-break:break-all}
.gm-out .hi{background:var(--acc);border-color:var(--acc)}.gm-out .hi span{color:rgba(255,255,255,.85)}.gm-out .hi b{color:#fff;font-size:22px}
.gm-h{margin:22px 0 4px!important;font-size:17px!important}
.gm-bar{margin-top:14px;display:grid;gap:6px}.gm-bar div{display:grid;grid-template-columns:44px 1fr 64px;gap:8px;align-items:center;font-size:14px}.gm-bar i{display:block;height:10px;border-radius:99px;background:var(--acc)}.gm-bar b{text-align:right}.gm-cap{margin:0;font-size:13px;color:var(--muted)}
.bw{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:10px}@media(min-width:720px){.bw{grid-template-columns:repeat(10,1fr)}}
.bf{border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff;text-align:center}
.bf em{display:block;font-style:normal;font-size:12px;background:var(--paper2,#f6f7f9);color:var(--muted);padding:2px 0}
.bf div{display:flex}.bf input{width:100%;min-width:0;border:0;border-right:1px solid var(--line);text-align:center;font:inherit;font-weight:700;padding:8px 0;border-radius:0}.bf input:last-child{border-right:0}
.bf b{display:block;border-top:1px solid var(--line);padding:6px 0;font-size:16px;min-height:1.6em}
</style>"""

def page(path, title, desc, crumb, body, ld, extra_js=''):
    url = SITE + path
    h = HEAD + f'<title>{E(title)}</title>\n<meta name="description" content="{E(desc)}">\n<link rel="canonical" href="{url}">\n'
    h += f'<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="홍라이프 도구">\n'
    h += f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{SITE}/assets/og/site.png">\n'
    h += '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://honglife.co.kr/assets/og/site.png">\n'
    h += MID + '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS + '\n</head>\n<body>\n\n' + BRAND
    h += f'<main class="wrap wide"><header class="top"><p class="crumb">{crumb}</p>' + body + '</main>' + extra_js + TAIL
    os.makedirs(os.path.dirname(OUT + path if not path.endswith('/') else OUT + path + 'x'), exist_ok=True)
    fp = OUT + (path + 'index.html' if path.endswith('/') else path)
    open(fp, 'w', encoding='utf-8').write(h)

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def faqld(f):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in f]}

def faqhtml(f):
    return '<section class="card pe-faq"><h2>자주 묻는 질문</h2><dl>' + ''.join(f'<dt>{E(q)}</dt><dd>{E(a)}</dd>' for q, a in f) + '</dl></section>'

def rel(cat, cur, items, label):
    lis = ''.join(f'<li><a href="/{cat}/{x["slug"]}.html"><b>{E(x["name"])}</b><span>{E(x["lead"][:46])}…</span></a></li>' for x in items if x['slug'] != cur)
    return f'<section class="card rel"><h2>다른 {label}</h2><ul>{lis}<li><a href="/{cat}/"><b>{label} 모음</b><span>전체 목록 보기</span></a></li></ul></section>'

ENGINE = r"""<script>(function(){var T=__T__;var L=T.L||['전혀 아니다','아니다','보통','그렇다','매우 그렇다'];var MX=L.length-1;var A=new Array(T.q.length).fill(null);var box=document.getElementById('qz'),res=document.getElementById('qres'),pg=document.querySelector('.qbar i'),pt=document.querySelector('.qbar p');
box.innerHTML=T.q.map(function(q,i){return '<div class="qi" id="q'+i+'"><p class="qt"><i>'+(i+1)+'</i>'+q[0]+'</p><div class="lk" role="group" aria-label="'+(i+1)+'번 응답">'+L.map(function(l,v){return '<button type="button" aria-pressed="false" data-i="'+i+'" data-v="'+v+'">'+l+'</button>'}).join('')+'</div></div>'}).join('');
function upd(){var n=A.filter(function(x){return x!==null}).length;pg.style.width=(n/A.length*100)+'%';pt.textContent=n+' / '+A.length+'문항 답했어요';document.getElementById('go').disabled=n<A.length;}
box.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var i=+b.dataset.i;A[i]=+b.dataset.v;b.parentNode.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});upd();var nx=document.getElementById('q'+(i+1));if(nx&&A[i+1]===null){nx.scrollIntoView({behavior:'smooth',block:'center'})}});
function val(i){var q=T.q[i];return q[2]?MX-A[i]:A[i]}
function dims(){var s={},c={};T.q.forEach(function(q,i){s[q[1]]=(s[q[1]]||0)+val(i);c[q[1]]=(c[q[1]]||0)+MX});var o={};for(var k in s)o[k]=Math.round(s[k]/c[k]*100);return o}
function bars(o,names,top){return '<div class="qbars">'+Object.keys(o).sort(function(a,b){return o[b]-o[a]}).map(function(k){return '<div class="'+(k==top?'top':'')+'"><span>'+names[k]+'</span><i><em style="width:'+o[k]+'%"></em></i><b>'+o[k]+'</b></div>'}).join('')+'</div>'}
function tips(t){return '<ul class="tips">'+t.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul>'}
document.getElementById('go').onclick=function(){var h='',tt='',total=0;T.q.forEach(function(q,i){total+=val(i)});var pct=Math.round(total/(T.q.length*MX)*100);
if(T.kind=='phq9'){var b=T.bands.find(function(x){return total<x[0]});tt=b[1]+' ('+total+'점)';if(A[8]>0)h+='<div class="qalert"><b>마지막 문항에 “있다”고 답하셨어요.</b> 점수와 상관없이 지금 바로 이야기를 나눠 보세요. <a href="tel:109">자살예방상담 109</a>(24시간, 무료)에 전화하거나, 위험하다고 느끼면 <a href="tel:112">112</a>·<a href="tel:119">119</a>에 연락하세요. 가까운 사람에게 지금 곁에 있어 달라고 말하는 것도 큰 도움이 돼요.</div>';h+='<span class="tag">'+T.name+' 결과</span><h2>'+b[1]+'</h2><p class="sc">총점 '+total+'점 / 27점</p><p class="d">'+b[2]+'</p>'+tips(b[3]);}
else if(T.kind=='score'){var b=T.bands.find(function(x){return pct<x[0]});tt=b[1];h='<span class="tag">'+T.name+' 결과</span><h2>'+b[1]+'</h2><p class="sc">'+(T.bip?(T.bip[0]+' '+(100-pct)+' : '+pct+' '+T.bip[1]):'점수 '+pct+'점 / 100점')+'</p><p class="d">'+b[2]+'</p>'+tips(b[3]);
 if(T.areas){var o=dims(),low=Object.keys(o).sort(function(a,b){return o[a]-o[b]})[0];h+='<p class="sc" style="margin-top:14px">영역별 점수 · 가장 먼저 챙길 영역: <b>'+T.areas[low]+'</b></p>'+bars(o,T.areas,low)}}
else if(T.kind=='dim'){var o=dims(),top=Object.keys(o).sort(function(a,b){return o[b]-o[a]})[0],d=T.dims[top],nm={};for(var k in T.dims)nm[k]=T.dims[k][0];tt=d[0];h='<span class="tag">'+T.name+' 결과</span><h2>'+d[0]+'</h2><p class="d">'+d[1]+'</p>'+tips(d[2])+bars(o,nm,top)}
else if(T.kind=='axis2'){var o=dims(),x=o.x,y=o.y,key=(x>=50?'H':'L')+(y>=50?'H':'L'),d=T.axis.types[key];tt=d[0];h='<span class="tag">'+T.name+' 결과</span><h2>'+d[0]+'</h2><p class="sc">'+T.axis.x+' '+x+'점 · '+T.axis.y+' '+y+'점</p><div class="qmap"><span style="left:8px;top:6px">회피형</span><span style="right:8px;top:6px">혼란형</span><span style="left:8px;bottom:6px">안정형</span><span style="right:8px;bottom:6px">불안형</span><i class="dot" style="left:'+x+'%;top:'+(100-y)+'%"></i></div><p class="sc" style="text-align:center">가로: '+T.axis.x+' · 세로: '+T.axis.y+'</p><p class="d">'+d[1]+'</p>'+tips(d[2])}
else if(T.kind=='age'){var o=dims(),age=Math.round(35+(o.o-o.y)*0.25);age=Math.max(8,Math.min(70,age));var g=age<15?['초등학생 마음','호기심 많고 솔직한 어린이 같은 마음이에요. 재미있는 일 앞에서는 망설이지 않아요.']:age<23?['10대 마음','유행에 빠르고 에너지가 넘쳐요. 하고 싶은 게 많은 청춘 그 자체예요.']:age<33?['20대 마음','새로운 경험을 즐기면서도 나름의 기준이 생긴 마음이에요.']:age<45?['30대 마음','열정과 현실 감각이 균형을 이룬 마음이에요. 할 땐 하고 쉴 땐 쉬어요.']:age<57?['40대 마음','여유롭고 차분하게 상황을 보는 어른스러운 마음이에요.']:['60대 이상 마음','웬만한 일에는 흔들리지 않는 넉넉한 마음이에요. 주변 사람들이 기대고 싶어 해요.'];tt='정신연령 '+age+'세';h='<span class="tag">'+T.name+' 결과</span><h2>정신연령 '+age+'세</h2><p class="sc">'+g[0]+' · 젊은 마음 '+o.y+'점 / 어른스러운 마음 '+o.o+'점</p><p class="d">'+g[1]+' 재미로 보는 결과이니 친구와 비교해 보세요.</p>'}
if(T.care)h+='<p class="qcare">이 결과는 스스로를 돌아보는 참고용이에요. 힘든 마음이 2주 넘게 이어지면 정신건강 위기상담 전화 <b>109</b>(24시간)나 가까운 정신건강복지센터에서 상담을 받을 수 있어요.</p>';
h+='<div class="btns">'+(T.kind=='phq9'?'':'<button class="btn" type="button" id="sh">결과 공유하기</button>')+'<button class="btn ghost" type="button" id="re">다시 하기</button></div>';
res.innerHTML=h;res.hidden=false;res.scrollIntoView({behavior:'smooth',block:'start'});
var SH=document.getElementById('sh');if(SH)SH.onclick=function(){var tx='['+T.name+'] 내 결과: '+tt+' — 나도 해 보기';if(navigator.share){navigator.share({title:T.name,text:tx,url:location.href}).catch(function(){})}else{navigator.clipboard.writeText(tx+' '+location.href).then(function(){alert('링크를 복사했어요')})}};
document.getElementById('re').onclick=function(){A.fill(null);box.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed','false')});res.hidden=true;upd();window.scrollTo({top:box.offsetTop-80,behavior:'smooth'})};};
upd();})();</script>"""

def test_page(t):
    path = f'/test/{t["slug"]}.html'
    nq = len(t['q'])
    title = f'{t["name"]} 무료 · {nq}문항 자가 점검 | 홍라이프 도구'
    desc = t['lead']
    T = dict(name=t['name'], kind=t['kind'], q=t['q'], care=t.get('care', False))
    if t.get('L'): T['L'] = t['L']
    if t['kind'] == 'phq9': T['bands'] = [list(b) for b in t['bands']]
    if t['kind'] == 'score':
        T['bands'] = [list(b) for b in t['bands']]
        if t.get('areas'): T['areas'] = t['areas']
        if t.get('bipolar'): T['bip'] = t['bipolar']
    if t['kind'] == 'dim': T['dims'] = t['dims']
    if t['kind'] == 'axis2': T['axis'] = t['axis']
    js = ENGINE.replace('__T__', json.dumps(T, ensure_ascii=False))
    crumb = '<a href="/">홈</a> › <a href="/test/">심리 테스트</a>'
    body = f'<h1><b>{E(t["h1"])}</b></h1><p class="lead">{E(t["lead"])}</p>{LOCK}</header>'
    body += f'<section class="card tool" id="tool"><div class="qbar"><div class="pg"><i></i></div><p></p></div><p class="note">{E(t["period"])} 기준으로 가장 가까운 답을 골라 주세요. 정답은 없어요.</p><div class="qz" id="qz"></div><div class="btns"><button class="btn" type="button" id="go" disabled>결과 보기</button></div><div class="qres" id="qres" hidden aria-live="polite"></div></section>'
    # 설명
    if t['kind'] in ('dim',):
        types = ''.join(f'<li><b>{E(v[0])}</b> — {E(v[1])}</li>' for v in t['dims'].values())
    elif t['kind'] == 'axis2':
        types = ''.join(f'<li><b>{E(v[0])}</b> — {E(v[1])}</li>' for v in t['axis']['types'].values())
    elif t['kind'] in ('score', 'phq9'):
        prev = 0; types = ''
        for b in t['bands']:
            types += f'<li><b>{E(b[1])}</b> ({prev}~{min(b[0]-1,100 if t["kind"]=="score" else 27)}점) — {E(b[2])}</li>'; prev = b[0]
    else:
        types = '<li>젊은 마음 문항과 어른스러운 마음 문항의 점수 차이를 8세~70세 사이 나이로 바꿔 보여 줘요.</li>'
    how = {'score': f'{nq}개 문항에 0~4점(전혀 아니다~매우 그렇다)을 매겨 더한 뒤 100점 만점으로 바꿔요. 표시된 몇몇 문항은 반대로 계산해요. 점수 구간에 따라 결과를 보여 줘요.',
           'dim': f'{nq}개 문항이 유형별로 나뉘어 있어요. 유형마다 0~4점 응답을 모아 100점 만점으로 바꾸고, 가장 높은 유형을 대표 결과로 보여 줘요. 모든 유형 점수도 막대로 함께 보여 줘요.',
           'axis2': '문항이 두 기준으로 나뉘어 있어요. 각 기준 점수를 100점 만점으로 바꿔 50점을 기준으로 높고 낮음을 나누고, 두 점수의 조합으로 네 유형 중 하나를 보여 줘요.',
           'age': '재미로 보는 테스트예요. 문항별 0~4점 응답을 모아 계산해요.',
           'phq9': '9개 문항에 0점(전혀 없음)~3점(거의 매일)을 매겨 더해요. 총점은 0~27점이고, 5·10·15·20점을 기준으로 우울 정도를 나눠요. 마지막 문항(죽음·자해에 대한 생각)에 1점 이상 답하면 점수와 관계없이 바로 도움을 받을 수 있는 곳을 먼저 안내해요.'}[t['kind']]
    note = ('PHQ-9은 우울증이 의심되는지 가려내는 선별 검사로, 진단 검사가 아니에요. 문항은 PHQ-9 원문(Kroenke·Spitzer·Williams)의 9가지 증상을 우리말로 옮긴 것이고, 결과는 정신건강의학과 진료를 대신하지 않아요. 점수가 낮아도 힘들다면 상담을 받아 보세요. 출처: Kroenke K. 외, The PHQ-9: validity of a brief depression severity measure (2001); 한국어판 PHQ-9 표준화 연구.' if t['kind'] == 'phq9' else '이 테스트의 문항은 홍라이프가 일상 상황을 바탕으로 새로 쓴 것으로, 병원이나 상담기관에서 쓰는 정식 심리검사가 아니에요. 그날의 기분에 따라 결과가 달라질 수 있으니 나를 돌아보는 참고용으로만 써 주세요.')
    xp = f'<section class="card xp" id="explain"><h2>{E(t["name"])}, 이렇게 계산해요</h2><h3>점수 계산 방식</h3><p>{E(how)}</p><h3>결과 유형</h3><ul>{types}</ul><h3>꼭 알아 두세요</h3><p>{E(note)} 마지막 수정: {UPD}</p></section>'
    extra = ''
    if t.get('rel_calc'):
        extra = f'<section class="card"><h2>함께 쓰면 좋은 계산기</h2><p><a href="{t["rel_calc"][0]}">{E(t["rel_calc"][1])}</a></p></section>'
    body += xp + faqhtml(t['faq']) + extra + rel('test', t['slug'], TESTS, '심리 테스트')
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebApplication", "name": t['name'], "url": SITE + path, "applicationCategory": "LifestyleApplication", "operatingSystem": "Any", "inLanguage": "ko", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}},
          crumbs([('홈', '/'), ('심리 테스트', '/test/'), (t['name'], path)]), faqld(t['faq'])]}
    page(path, title, desc, crumb, body, ld, js)

HELP = r"""<script>(function(){function $(i){return document.getElementById(i)}function N(i){var v=($(i).value||'').toString().replace(/[^0-9.\-]/g,'');return parseFloat(v)||0}function S(i,v){$(i).textContent=v}function K(n){return Math.round(n).toLocaleString('ko-KR')}
function M(n){n=Math.floor(n);var j=Math.floor(n/1e12),e=Math.floor(n%1e12/1e8),m=Math.floor(n%1e8/1e4),r=n%1e4,s=[];if(j)s.push(j+'조');if(e)s.push(e+'억');if(m)s.push(m+'만');if(r||!s.length)s.push(r);return s.join(' ')+' 메소'}function G(n){return K(n)+' 골드'}
__JS__
document.querySelectorAll('#tool input,#tool select').forEach(function(x){x.addEventListener('input',c);x.addEventListener('change',c)});c();})();</script>"""

def game_page(g):
    path = f'/game/{g["slug"]}.html'
    title = f'{g["name"]} | 홍라이프 도구'
    crumb = '<a href="/">홈</a> › <a href="/game/">게임 계산기</a>'
    body = f'<h1><b>{E(g["h1"])}</b></h1><p class="lead">{E(g["lead"])}</p>{LOCK.replace("입력한 답과 결과는", "입력한 숫자는")}</header>'
    body += f'<section class="card tool" id="tool">{g["body"]}</section>'
    xp = ''.join(f'<h3>{E(h)}</h3><p>{E(p)}</p>' for h, p in g['xp'])
    src = ''
    if g.get('src'):
        src = f'<h3>출처</h3><p><a href="{g["src"][1]}" rel="noopener" target="_blank">{E(g["src"][0])}</a> (확인: {g["src"][2]}). 게임 정책은 업데이트로 바뀔 수 있으니 게임 안 화면을 함께 확인하세요.</p>'
    body += f'<section class="card xp" id="explain"><h2>{E(g["name"])}, 계산 원리 그대로</h2>{xp}{src}<p class="note">마지막 수정: {UPD}. 게임사와 관계없는 비공식 도구예요.</p></section>'
    body += faqhtml(g['faq']) + rel('game', g['slug'], GAMES, '게임 계산기')
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebApplication", "name": g['name'], "url": SITE + path, "applicationCategory": "GameApplication", "operatingSystem": "Any", "inLanguage": "ko", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}},
          crumbs([('홈', '/'), ('게임 계산기', '/game/'), (g['name'], path)]), faqld(g['faq'])]}
    page(path, title, g['lead'], crumb, body, ld, HELP.replace('__JS__', g['js']))

def hub(cat, items, h1, lead, title, desc):
    path = f'/{cat}/'
    lis = ''.join(f'<li><a href="/{cat}/{x["slug"]}.html"><i class="th"><img src="/assets/art/hl/cs-{cat}.svg" alt="" width="200" height="140" loading="lazy"></i><img class="pg" src="/assets/art/hl/pg-{cat}.svg" alt="" width="26" height="26" loading="lazy"><b>{E(x["name"])}</b><span>{E(x["lead"][:60])}…</span></a></li>' for x in items)
    body = f'<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>{LOCK}</header><section class="card"><h2>{E(h1)} {len(items)}가지</h2><ul class="tlist hl-grid">{lis}</ul></section>'
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "CollectionPage", "name": h1, "url": SITE + path, "hasPart": [{"@type": "WebApplication", "name": x['name'], "url": f'{SITE}/{cat}/{x["slug"]}.html'} for x in items]}, crumbs([('홈', '/'), (h1, path)])]}
    page(path, title, desc, f'<a href="/">홈</a> › {E(h1)}', body.replace('<header class="top">', ''), ld)
    # hub uses header class "top hub"
    fp = OUT + path + 'index.html'
    s = open(fp, encoding='utf-8').read().replace('<header class="top"><p class="crumb">', '<header class="top hub"><p class="crumb">', 1)
    open(fp, 'w', encoding='utf-8').write(s)

ART = {
 'test': ('#C2255C', '<circle cx="32" cy="27" r="13" fill="none" stroke="{c}" stroke-width="3.2"/><path d="M27 23c1-3 9-3 9 1 0 3-4 3-4 6" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="34" r="1.8" fill="{c}"/><path d="M18 52c2-7 8-10 14-10s12 3 14 10" fill="none" stroke="{c}" stroke-width="3.2" stroke-linecap="round"/>'),
 'game': ('#2B8A3E', '<rect x="10" y="22" width="44" height="24" rx="12" fill="none" stroke="{c}" stroke-width="3.2"/><path d="M21 29v10M16 34h10" stroke="{c}" stroke-width="3.2" stroke-linecap="round"/><circle cx="41" cy="31" r="2.6" fill="{c}"/><circle cx="47" cy="37" r="2.6" fill="{c}"/>'),
}
def art():
    d = OUT + '/assets/art/hl'; os.makedirs(d, exist_ok=True)
    for k, (col, p) in ART.items():
        pg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"><rect x="2" y="2" width="60" height="60" rx="14" fill="#fff" stroke="#1f2430" stroke-opacity=".18" stroke-width="2"/>{p.format(c="#1f2430")}</svg>'
        open(f'{d}/pg-{k}.svg', 'w').write(pg)
        if k == 'test':
            rows = ''
            for r, (yy, sel) in enumerate([(44, 3), (64, 1), (84, 4)]):
                rows += f'<rect x="50" y="{yy-8}" width="{40+r*8}" height="5" rx="2.5" fill="#E9ECF2"/>'
                for c in range(5):
                    cx = 56 + c * 15
                    rows += f'<circle cx="{cx}" cy="{yy+4}" r="4.5" fill="{"#B14FC5" if c == sel else "#fff"}" stroke="{"#B14FC5" if c == sel else "#CDD2DB"}" stroke-width="1.5"/>'
            cs = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="40.0 16.0 120.0 108.0" width="120" height="108"><g>'
                  '<rect x="40" y="16" width="120" height="108" rx="6" fill="#fff"/><rect x="40" y="16" width="120" height="16" rx="6" fill="#B14FC5"/><rect x="40" y="26" width="120" height="6" fill="#B14FC5"/>'
                  '<text x="48" y="27.5" font-family="Arial,Helvetica,sans-serif" font-size="8" font-weight="700" fill="#fff">애착유형 테스트</text>'
                  '<rect x="122" y="21" width="30" height="5" rx="2.5" fill="#fff" fill-opacity=".35"/><rect x="122" y="21" width="20" height="5" rx="2.5" fill="#fff"/>'
                  + rows +
                  '<rect x="128" y="40" width="26" height="54" rx="5" fill="#F6E8F9"/><circle cx="141" cy="56" r="8" fill="none" stroke="#B14FC5" stroke-width="3"/><path d="M137 76h8M135 83h12" stroke="#D9A8E4" stroke-width="3" stroke-linecap="round"/>'
                  '<rect x="50" y="102" width="56" height="13" rx="6.5" fill="#B14FC5"/><text x="60" y="111" font-family="Arial,Helvetica,sans-serif" font-size="7.5" font-weight="700" fill="#fff">결과: 안정형</text>'
                  '</g></svg>')
        else:
            cs = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="30.0 18.0 140.0 106.0" width="140" height="106"><g>'
                  '<rect x="30" y="18" width="140" height="106" rx="9" fill="#fff"/><rect x="30" y="18" width="140" height="18" rx="9" fill="#5C7A12"/><rect x="30" y="28" width="140" height="8" fill="#5C7A12"/>'
                  '<circle cx="40" cy="27" r="2.5" fill="#fff" fill-opacity=".7"/><circle cx="48" cy="27" r="2.5" fill="#fff" fill-opacity=".7"/><circle cx="56" cy="27" r="2.5" fill="#fff" fill-opacity=".7"/>'
                  '<text x="66" y="30" font-family="Arial,Helvetica,sans-serif" font-size="8" font-weight="700" fill="#fff">가챠 확률 · 강화 기댓값</text>'
                  '<circle cx="70" cy="74" r="22" fill="none" stroke="#EAF3D2" stroke-width="9"/><path d="M70 52a22 22 0 1 1-21.6 26" fill="none" stroke="#7FA21B" stroke-width="9" stroke-linecap="round"/>'
                  '<text x="59" y="78" font-family="Arial,Helvetica,sans-serif" font-size="11" font-weight="700" fill="#1A1D24">63%</text>'
                  '<rect x="106" y="50" width="52" height="7" rx="3.5" fill="#EAF3D2"/><rect x="106" y="50" width="40" height="7" rx="3.5" fill="#7FA21B"/>'
                  '<rect x="106" y="64" width="52" height="7" rx="3.5" fill="#EAF3D2"/><rect x="106" y="64" width="26" height="7" rx="3.5" fill="#A8C64A"/>'
                  '<rect x="106" y="78" width="52" height="7" rx="3.5" fill="#EAF3D2"/><rect x="106" y="78" width="46" height="7" rx="3.5" fill="#5C7A12"/>'
                  '<rect x="104" y="98" width="56" height="16" rx="8" fill="#1A1D24"/><path d="M114 106h6M117 103v6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/><circle cx="148" cy="104" r="1.8" fill="#C8E06A"/><circle cx="152" cy="108" r="1.8" fill="#C8E06A"/>'
                  '</g></svg>')
        open(f'{d}/cs-{k}.svg', 'w').write(cs)

for t in TESTS: test_page(t)
for g in GAMES: game_page(g)
hub('test', TESTS, '심리 테스트', '번아웃·애착유형·소비성향·HSP·직업 적성·연애 성향까지, 나를 돌아보는 심리·성격 테스트 모음이에요. 문항은 모두 새로 쓴 참고용이고, 답과 결과는 서버로 보내지 않아요.', '심리 테스트 모음 | 번아웃·애착유형·소비성향·HSP·직업 적성 무료 테스트 | 홍라이프 도구', '번아웃 테스트, 애착유형 테스트, 소비성향 테스트, HSP 테스트, 행복지수, 스마트폰 의존도, 직업 적성, 4기질, 좌뇌 우뇌, 정신연령, 연애 성향, 갈등 대처 유형까지 무료 심리 테스트 모음.')
hub('game', GAMES, '게임 계산기', '메이플 경매장 수수료, 로아 경매 입찰가, 가챠 확률, 강화 기댓값, FPS 감도 변환, 볼링 점수, 승률까지 게임할 때 쓰는 계산기 모음이에요.', '게임 계산기 모음 | 메이플 수수료·로아 경매·가챠 확률·강화 기댓값·감도 변환 | 홍라이프 도구', '메이플 경매장 수수료, 로스트아크 경매 입찰 적정가, 게임 거래소 수수료, 가챠 확률(천장), 강화 기댓값, eDPI 감도 변환, 볼링 점수, 승률·KDA 계산기 무료 모음.')
art()
json.dump({'test': [[f'/test/{t["slug"]}.html', t['name'], t['lead'][:70], t['kw']] for t in TESTS], 'game': [[f'/game/{g["slug"]}.html', g['name'], g['lead'][:70], g['kw']] for g in GAMES]}, open(OUT + '/newcats.json', 'w'), ensure_ascii=False)
print('pages', len(TESTS) + len(GAMES) + 2)
