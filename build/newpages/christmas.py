import json,re,os
T='/home/claude/coio/overlay/life/taxi-fare.html'
s=open(T,encoding='utf-8').read()
a=s.find('<style id="hl-mt">'); b=s.find('</style>',a)+8
i=s.find('<main'); j=s.find('</main>')+7
head=s[:a]; between=s[b:i]
tail_scripts=s[j:]
k=tail_scripts.find('<script>window.HL_V=')
tail=tail_scripts[k:] if k>0 else '</body>\n</html>\n'
URL='https://honglife.co.kr/life/christmas.html'
TITLE='크리스마스 D-day · 선물 예산 계산기 2026 (12월 25일까지 남은 날)'
DESC='2026년 크리스마스(12월 25일 금요일)까지 남은 날·시간을 눈 내리는 카운트다운으로 보고, 가족·연인·친구 선물 예산을 사람별로 나눠 총액과 남은 돈을 계산해요. 무료, 저장 없음.'
FAQ=[
("2026년 크리스마스는 무슨 요일인가요?","2026년 12월 25일은 금요일이에요. 크리스마스(기독탄신일)는 법정 공휴일이라 24일 목요일 저녁부터 27일 일요일까지 사흘 연휴가 돼요."),
("D-day는 어떻게 세나요?","오늘 날짜에서 12월 25일까지 남은 날 수예요. 예를 들어 12월 24일이면 D-1, 12월 25일 당일은 D-day예요. 아래 카운트다운은 한국 시간 12월 25일 0시까지 남은 시간을 초 단위로 보여 줘요."),
("선물 예산은 어떻게 나누면 좋나요?","먼저 쓸 수 있는 총액을 정하고, 사람별 금액을 넣어 합계가 총액을 넘지 않게 맞춰요. 넘으면 빨간색으로 얼마나 넘었는지 알려 줘요. 포장비·배송비는 '기타' 줄로 따로 넣으면 정확해요."),
("입력한 내용이 저장되나요?","서버로 보내지 않아요. 이 기기의 브라우저에만 저장돼요."),
("연말 모임 비용은 어떻게 나누나요?","누가 얼마를 냈는지 넣으면 누가 누구에게 보내야 하는지 정리해 주는 N빵 정산 계산기를 함께 쓰세요.")]
ld={"@context":"https://schema.org","@graph":[{"@type":"WebApplication","name":"크리스마스 D-day · 선물 예산 계산기","url":URL,"applicationCategory":"UtilitiesApplication","operatingSystem":"Any","inLanguage":"ko","offers":{"@type":"Offer","price":"0","priceCurrency":"KRW"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"https://honglife.co.kr/"},{"@type":"ListItem","position":2,"name":"생활·행정","item":"https://honglife.co.kr/life/"},{"@type":"ListItem","position":3,"name":"크리스마스 D-day · 선물 예산","item":URL}]},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":x}} for q,x in FAQ]}]}
head=re.sub(r'<title>.*?</title>',f'<title>{TITLE} | 홍라이프 도구</title>',head,count=1,flags=re.S)
head=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{DESC}">',head,count=1)
head=head.replace('https://honglife.co.kr/life/taxi-fare.html',URL)
head=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m.group(1)+TITLE+' | 홍라이프 도구',head,count=1)
head=re.sub(r'(<meta property="og:description" content=")[^"]*',lambda m:m.group(1)+DESC,head,count=1)
head=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>',head,count=1,flags=re.S)
CSS='''<style id="hl-xm">
.xm-hero{position:relative;overflow:hidden;border-radius:20px;background:linear-gradient(165deg,#0B1F3F 0%,#1B2F5E 60%,#2A1E4A 100%);color:#fff;padding:20px 18px 18px;min-height:300px}
.xm-hero canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.xm-in{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 150px;gap:14px;align-items:center}
.xm-k{display:inline-block;font-size:13px;font-weight:800;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:3px 12px}
.xm-d{font-size:64px;font-weight:900;line-height:1;margin:10px 0 4px;letter-spacing:-1px;color:#FFE08A;font-variant-numeric:tabular-nums}
.xm-sub{font-size:15px;opacity:.92}
.xm-clock{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-top:14px;max-width:340px}
.xm-clock div{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:12px;text-align:center;padding:8px 2px}
.xm-clock b{display:block;font-size:24px;font-variant-numeric:tabular-nums}.xm-clock span{font-size:11.5px;opacity:.85}
.xm-tree svg{width:150px;height:190px;display:block}
.xm-tree .bulb{opacity:.18;transition:opacity .6s}.xm-tree .bulb.on{opacity:1;animation:tw 1.6s ease-in-out infinite}
@keyframes tw{50%{opacity:.45}}
.xm-bar{position:relative;height:10px;border-radius:999px;background:rgba(255,255,255,.15);margin-top:14px;overflow:hidden;max-width:340px}
.xm-bar i{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:linear-gradient(90deg,#F59E0B,#EF4444)}
.xm-note{font-size:12.5px;opacity:.85;margin-top:6px}
.xm-f{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.xm-f label{display:flex;flex-direction:column;gap:5px;font-size:13.5px;font-weight:700;color:var(--head);min-width:0}
.xm input,.xm select{font:inherit;font-size:16px;padding:9px 10px;border:1px solid var(--line-s);border-radius:10px;min-height:44px;width:100%;box-sizing:border-box;background:#fff;min-width:0}
.xm-list{display:flex;flex-direction:column;gap:8px;margin-top:10px}
.xm-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,8.5em) 36px;gap:8px;align-items:center}
.xm-row button{border:0;background:#F1F3F6;color:var(--muted);width:36px;height:36px;border-radius:50%;font-size:18px;cursor:pointer}
.xm-add{border:1px dashed #C2410C;color:#C2410C;background:#FFF7ED;border-radius:999px;min-height:40px;padding:0 14px;font:inherit;font-size:14.5px;font-weight:700;cursor:pointer;margin-top:10px}
.xm-pre{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 2px}
.xm-pre button{border:1px solid var(--line-s);background:#fff;border-radius:999px;padding:6px 12px;font:inherit;font-size:13.5px;cursor:pointer}
.xm-res{margin-top:14px;border-radius:16px;background:#FFF7ED;border:1px solid #FED7AA;padding:14px}
.xm-sum{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;text-align:center}
.xm-sum b{display:block;font-size:19px;color:var(--head);overflow-wrap:anywhere}.xm-sum span{font-size:12.5px;color:var(--muted)}
.xm-stack{display:flex;height:22px;border-radius:999px;overflow:hidden;margin-top:12px;background:#fff;border:1px solid #FED7AA}
.xm-stack i{display:block;height:100%;transition:width .5s}
.xm-leg{display:flex;flex-wrap:wrap;gap:6px 12px;font-size:13px;margin-top:8px;color:var(--head)}
.xm-leg span{display:inline-flex;align-items:center;gap:5px;min-width:0;overflow-wrap:anywhere}.xm-leg i{width:11px;height:11px;border-radius:3px;flex:none}
.xm-over{color:#B91C1C;font-weight:800}.xm-ok{color:#1D4ED8;font-weight:800}
.xm-msg{font-size:13px;color:var(--muted);margin-top:8px}
.xm-tb{width:100%;border-collapse:collapse;font-size:14.5px}.xm-tb th,.xm-tb td{border-bottom:1px solid var(--line-s);padding:8px 6px;text-align:left}
@media(max-width:560px){.xm-in{grid-template-columns:minmax(0,1fr) 96px;gap:8px}.xm-tree svg{width:96px;height:122px}.xm-d{font-size:48px}.xm-clock b{font-size:20px}.xm-f{grid-template-columns:1fr}.xm-sum b{font-size:16px}.xm-row{grid-template-columns:minmax(0,1fr) minmax(0,7.5em) 36px}}
@media(prefers-reduced-motion:reduce){.xm-tree .bulb.on{animation:none}}
</style>'''
# tree with 24 bulbs (Dec 1..24)
import math
B=[]
pts=[(75,40),(66,58),(84,58),(58,76),(75,72),(92,76),(50,96),(66,92),(84,92),(100,96),(44,116),(60,112),(75,118),(90,112),(106,116),(38,136),(54,134),(70,138),(84,136),(98,138),(112,136),(48,154),(75,156),(102,154)]
cols=['#F87171','#FBBF24','#60A5FA','#F472B6']
for n,(x,y) in enumerate(pts):
    B.append(f'<circle class="bulb" data-d="{n+1}" cx="{x}" cy="{y}" r="4.2" fill="{cols[n%4]}"/>')
TREE=('<svg viewBox="0 0 150 190" role="img" aria-label="날마다 전구가 하나씩 켜지는 트리">'
      '<polygon points="75,8 79,18 90,18 81,24 84,34 75,28 66,34 69,24 60,18 71,18" fill="#FDE047"/>'
      '<polygon points="75,26 30,100 120,100" fill="#1E3A8A"/><polygon points="75,56 22,140 128,140" fill="#1E40AF"/><polygon points="75,92 16,168 134,168" fill="#1D4ED8"/>'
      '<rect x="66" y="168" width="18" height="16" rx="3" fill="#92400E"/>'+''.join(B)+'</svg>')
main=f'''<main class="wrap wide xm"><header class="top"><p class="crumb"><a href="/">홈</a> › <a href="/life/">생활·행정</a></p><h1>크리스마스 D-day · 선물 예산 계산기</h1><p class="lead">2026년 크리스마스는 <b>12월 25일 금요일</b>이에요. 남은 날을 세고, 누구에게 얼마짜리 선물을 살지 예산을 나눠 보세요.</p></header>
<section class="card tool" style="padding:0;overflow:hidden"><div class="xm-hero" id="hero"><canvas id="snow"></canvas><div class="xm-in"><div style="min-width:0"><span class="xm-k">🎄 2026. 12. 25. (금)</span><div class="xm-d" id="dd">D-30</div><div class="xm-sub" id="dsub">크리스마스까지</div>
<div class="xm-clock"><div><b id="c-d">0</b><span>일</span></div><div><b id="c-h">0</b><span>시간</span></div><div><b id="c-m">0</b><span>분</span></div><div><b id="c-s">0</b><span>초</span></div></div>
<div class="xm-bar"><i id="bar" style="width:0"></i></div><div class="xm-note" id="bnote">12월 1일부터 하루에 전구가 하나씩 켜져요.</div></div>
<div class="xm-tree" aria-hidden="false">{TREE}</div></div></div></section>
<section class="card tool"><h2>🎁 선물 예산 나누기</h2>
<div class="xm-f"><label>쓸 수 있는 총예산 (원)<input id="bud" inputmode="numeric" value="300,000"></label><label>빠른 채우기<div class="xm-pre"><button type="button" data-p="fam">가족 4명</button><button type="button" data-p="cp">연인·커플</button><button type="button" data-p="fr">친구·동료</button></div></label></div>
<div class="xm-list" id="list"></div>
<button type="button" class="xm-add" id="add">+ 선물 받을 사람 추가</button>
<div class="xm-res" id="out"></div>
<p class="xm-msg">입력 내용은 서버로 보내지 않고 이 기기에만 저장돼요.</p></section>
<section class="card"><h2>2026년 연말 날짜 한눈에</h2>
<table class="xm-tb"><thead><tr><th>날짜</th><th>요일</th><th>무슨 날</th></tr></thead><tbody>
<tr><td>12월 24일</td><td>목</td><td>크리스마스 이브</td></tr>
<tr><td>12월 25일</td><td>금</td><td>크리스마스 (기독탄신일, 공휴일)</td></tr>
<tr><td>12월 26~27일</td><td>토~일</td><td>주말 — 25일부터 3일 연휴</td></tr>
<tr><td>12월 31일</td><td>목</td><td>2026년 마지막 날</td></tr>
<tr><td>2027년 1월 1일</td><td>금</td><td>새해 첫날 (공휴일) — 1월 1~3일 3일 연휴</td></tr>
</tbody></table></section>
<section class="card"><h2>이렇게 계산해요</h2><ul class="xp">
<li><b>D-day</b>는 한국 시간 기준 오늘 날짜에서 12월 25일까지 남은 날 수예요. 25일 당일은 D-day, 지나면 내년 크리스마스로 넘어가요.</li>
<li><b>트리 전구</b>는 12월 1일부터 24일까지 하루에 하나씩 켜지는 어드벤트 달력이에요. 24개가 다 켜지면 크리스마스 이브예요.</li>
<li><b>선물 예산</b>: 사람별 금액을 모두 더한 합계를 총예산과 비교해 남은 돈 또는 넘친 돈을 보여 줘요. 막대는 사람별 비율이에요.</li></ul></section>
<section class="card"><h2>선물 예산 꿀팁</h2><ul class="xp">
<li>총예산부터 정하고 사람을 넣으면 '남은 돈'을 보면서 금액을 조절할 수 있어요.</li>
<li>택배 마감이 있으니 12월 셋째 주 안에 주문하는 게 안전해요. 정확한 마감은 쇼핑몰·택배사 공지를 확인하세요.</li>
<li>포장비·카드·배송비는 '기타' 한 줄로 따로 넣어 두면 예산이 정확해져요.</li></ul></section>
<section class="card"><h2>자주 묻는 질문</h2><dl class="pe-faq">{''.join(f"<dt>{q}</dt><dd>{x}</dd>" for q,x in FAQ)}</dl></section>
<section class="card rel"><h2>함께 쓰면 좋은 도구</h2><ul class="tlist"><li><a href="/life/split-bill.html"><b>N빵 정산 계산기</b><span>연말 모임·파티 비용 누가 누구에게 얼마</span></a></li><li><a href="/fortune-2027.html"><b>2027 신년운세</b><span>내년 총운·12달 월운</span></a></li><li><a href="/yet.html"><b>연말정산 환급 미리보기</b><span>13월의 월급 계산</span></a></li><li><a href="/leave.html"><b>2027 연차 꿀조합</b><span>연차 2일로 9일 쉬기</span></a></li></ul></section>
</main>
'''
JS=r'''<script>
(function(){
var $=function(i){return document.getElementById(i)},K='hl-xmas-v1';
var W=function(n){return Math.round(n).toLocaleString('ko-KR')+'원'};
var num=function(v){v=String(v||'').replace(/[^0-9.]/g,'');var n=parseFloat(v);return isFinite(n)?n:0};
var esc=function(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
/* KST helpers */
function kstNow(){var d=new Date();return new Date(d.getTime()+d.getTimezoneOffset()*60000+9*3600000)}
function tick(){var now=Date.now(),k=kstNow(),y=k.getFullYear();
 if(k.getMonth()===11&&k.getDate()>25)y++;
 var target=Date.UTC(y,11,24,15,0,0); /* Dec 25 00:00 KST */
 var today=Date.UTC(k.getFullYear(),k.getMonth(),k.getDate()),xd=Date.UTC(y,11,25);
 var dd=Math.round((xd-today)/86400000);
 $('dd').textContent=dd===0?'D-day':'D-'+dd;
 $('dsub').textContent=dd===0?'메리 크리스마스! 🎅':(dd===1?'내일이 크리스마스예요':'크리스마스까지');
 var r=Math.max(0,target-now),s=Math.floor(r/1000);
 $('c-d').textContent=Math.floor(s/86400);$('c-h').textContent=Math.floor(s%86400/3600);$('c-m').textContent=Math.floor(s%3600/60);$('c-s').textContent=s%60;
 var on=(k.getMonth()===11)?Math.min(24,k.getDate()):0;if(dd===0)on=24;
 document.querySelectorAll('.xm-tree .bulb').forEach(function(b){b.classList.toggle('on',+b.dataset.d<=on)});
 var st=Date.UTC(y,10,1),pct=Math.max(0,Math.min(100,(today-st)/(xd-st)*100));$('bar').style.width=pct.toFixed(1)+'%';
 $('bnote').textContent=on?('전구 '+on+'/24개 켜짐 · 11월 1일부터 '+Math.round(pct)+'% 지났어요'):('12월 1일부터 하루에 전구가 하나씩 켜져요 · 11월 1일부터 '+Math.round(pct)+'% 지났어요');}
tick();setInterval(tick,1000);
/* snow */
(function(){var c=$('snow'),x=c.getContext('2d'),F=[],w,h,red=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
 function rs(){var r=c.getBoundingClientRect(),p=window.devicePixelRatio||1;w=r.width;h=r.height;c.width=w*p;c.height=h*p;x.setTransform(p,0,0,p,0,0)}
 rs();addEventListener('resize',rs);for(var i=0;i<70;i++)F.push({x:Math.random()*w,y:Math.random()*h,r:1+Math.random()*2.6,v:.3+Math.random()*.9,o:Math.random()*6});
 function fr(t){x.clearRect(0,0,w,h);x.fillStyle='rgba(255,255,255,.85)';F.forEach(function(f){if(!red){f.y+=f.v;f.x+=Math.sin(t/1400+f.o)*.35;if(f.y>h+4){f.y=-4;f.x=Math.random()*w}}x.beginPath();x.arc(f.x,f.y,f.r,0,6.283);x.fill()});if(!red)requestAnimationFrame(fr)}
 requestAnimationFrame(fr)})();
/* budget */
var COL=['#DC2626','#D97706','#2563EB','#DB2777','#7C3AED','#0891B2','#B45309','#4F46E5','#BE123C','#0E7490'];
var PRE={fam:[['엄마',80000],['아빠',80000],['동생',50000],['조카',40000]],cp:[['연인',150000],['케이크·데이트',60000],['카드·포장',10000]],fr:[['친한 친구',30000],['친구',20000],['직장 동료',15000],['마니또',10000]]};
var S;function def(){return {b:300000,l:[['엄마',80000],['아빠',80000],['연인',100000],['친구',20000]]}}
function load(){try{var v=localStorage.getItem(K);if(v)return JSON.parse(v)}catch(e){}return def()}
function save(){try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}}
function renderL(){$('list').innerHTML=S.l.map(function(r,i){return '<div class="xm-row"><input aria-label="이름" data-n="'+i+'" value="'+esc(r[0])+'"><input aria-label="금액" inputmode="numeric" data-a="'+i+'" value="'+(r[1]?Math.round(r[1]).toLocaleString('ko-KR'):'')+'"><button type="button" data-x="'+i+'" aria-label="삭제">×</button></div>'}).join('')}
function upd(){var tot=0;S.l.forEach(function(r){tot+=+r[1]||0});var b=S.b,left=b-tot;
 var h='<div class="xm-sum"><div><b>'+W(tot)+'</b><span>선물 합계 ('+S.l.length+'명)</span></div><div><b>'+W(b)+'</b><span>총예산</span></div><div><b class="'+(left<0?'xm-over':'xm-ok')+'">'+(left<0?'+'+W(-left):W(left))+'</b><span>'+(left<0?'예산 초과':'남은 돈')+'</span></div></div>';
 var base=Math.max(tot,b)||1;h+='<div class="xm-stack" role="img" aria-label="사람별 예산 비율">'+S.l.map(function(r,i){return '<i style="width:'+((+r[1]||0)/base*100).toFixed(2)+'%;background:'+COL[i%COL.length]+'"></i>'}).join('')+'</div>';
 h+='<div class="xm-leg">'+S.l.map(function(r,i){return '<span><i style="background:'+COL[i%COL.length]+'"></i>'+esc(r[0]||'이름 없음')+' '+(tot?Math.round((+r[1]||0)/tot*100):0)+'%</span>'}).join('')+'</div>';
 if(S.l.length&&b>0)h+='<p class="xm-msg" style="color:var(--head)">총예산을 '+S.l.length+'명에게 똑같이 나누면 1명당 <b>'+W(Math.floor(b/S.l.length/1000)*1000)+'</b> (천 원 단위 내림)이에요.</p>';
 $('out').innerHTML=h;save()}
document.addEventListener('input',function(e){var t=e.target,d=t.dataset;
 if(t.id==='bud'){S.b=num(t.value);upd()}
 else if(d.n!==undefined){S.l[+d.n][0]=t.value;upd()}
 else if(d.a!==undefined){S.l[+d.a][1]=num(t.value);upd()}});
document.addEventListener('change',function(e){var t=e.target;if(t.dataset&&t.dataset.a!==undefined){t.value=num(t.value)?Math.round(num(t.value)).toLocaleString('ko-KR'):''}if(t.id==='bud'){t.value=Math.round(num(t.value)).toLocaleString('ko-KR')}});
document.addEventListener('click',function(e){var t=e.target;if(!t.dataset)return;
 if(t.dataset.x!==undefined){S.l.splice(+t.dataset.x,1);renderL();upd()}
 else if(t.dataset.p&&PRE[t.dataset.p]){S.l=PRE[t.dataset.p].map(function(r){return r.slice()});renderL();upd()}});
$('add').onclick=function(){if(S.l.length>=20)return;S.l.push(['',0]);renderL();upd();var x=document.querySelectorAll('[data-n]');if(x.length)x[x.length-1].focus()};
S=load();$('bud').value=Math.round(S.b).toLocaleString('ko-KR');renderL();upd();
})();
</script>
'''
out=head+CSS+between+main+JS+tail
open('/home/claude/coio/overlay/life/christmas.html','w',encoding='utf-8').write(out)
print(len(out))
