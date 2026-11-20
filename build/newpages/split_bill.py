import json,re,os
T='/home/claude/coio/overlay/life/taxi-fare.html'
s=open(T,encoding='utf-8').read()
a=s.find('<style id="hl-mt">'); b=s.find('</style>',a)+8
i=s.find('<main'); j=s.find('</main>')+7
head=s[:a]; between=s[b:i]
tail_scripts=s[j:]
# keep only the site-wide scripts after main (drop map script)
k=tail_scripts.find('<script>window.HL_V=')
tail=tail_scripts[k:] if k>0 else '</body>\n</html>\n'
URL='https://honglife.co.kr/life/split-bill.html'
TITLE='N빵 정산 계산기 · 모임·여행 더치페이 (누가 누구에게 얼마)'
DESC='모임·여행에서 각자 낸 돈을 넣으면 누가 누구에게 얼마를 보내면 되는지 송금 횟수가 가장 적게 정리해요. 항목별 참여자 지정, 100원 단위 반올림, 카톡 공유 문구까지. 무료, 저장 없음.'
FAQ=[
("N빵은 어떻게 계산하나요?","총액을 사람 수로 나누면 1인당 금액이에요. 예를 들어 127,000원을 4명이 나누면 31,750원이에요. 사람마다 먹은 게 다르면 항목별로 함께한 사람만 체크하면 그 사람들끼리만 나눠요."),
("누가 누구에게 보내야 하는지는 어떻게 정하나요?","각자 '실제로 낸 돈 − 내야 할 몫'을 계산해 받을 사람과 보낼 사람으로 나눈 뒤, 가장 많이 보내야 하는 사람과 가장 많이 받아야 하는 사람부터 짝지어요. 이렇게 하면 송금 횟수가 최대 (사람 수 − 1)번으로 줄어요."),
("100원 단위로 맞추면 금액이 안 맞지 않나요?","송금액만 100원 단위로 반올림하기 때문에 한 번 보낼 때 최대 50원까지 차이가 날 수 있어요. 정확히 맞추려면 반올림을 '1원'으로 두세요."),
("입력한 내용이 저장되나요?","서버로 보내지 않아요. 이 기기의 브라우저에만 자동 저장되고, '링크로 공유'를 누르면 내용이 주소에 담겨서 받은 사람도 같은 화면을 볼 수 있어요."),
("술 안 마신 사람은 어떻게 빼나요?","술값을 따로 한 줄로 넣고 '함께한 사람'에서 안 마신 사람의 체크를 풀면 돼요. 그 항목은 체크된 사람끼리만 나눠요.")]
ld={"@context":"https://schema.org","@graph":[{"@type":"WebApplication","name":"N빵 정산 계산기","url":URL,"applicationCategory":"FinanceApplication","operatingSystem":"Any","inLanguage":"ko","offers":{"@type":"Offer","price":"0","priceCurrency":"KRW"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"https://honglife.co.kr/"},{"@type":"ListItem","position":2,"name":"생활·행정","item":"https://honglife.co.kr/life/"},{"@type":"ListItem","position":3,"name":"N빵 정산 계산기","item":URL}]},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":x}} for q,x in FAQ]}]}
head=re.sub(r'<title>.*?</title>',f'<title>{TITLE} | 홍라이프 도구</title>',head,count=1,flags=re.S)
head=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{DESC}">',head,count=1)
head=head.replace('https://honglife.co.kr/life/taxi-fare.html',URL)
head=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m.group(1)+TITLE+' | 홍라이프 도구',head,count=1)
head=re.sub(r'(<meta property="og:description" content=")[^"]*',lambda m:m.group(1)+DESC,head,count=1)
head=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>',head,count=1,flags=re.S)
CSS='''<style id="hl-sb">
.sb-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.sb-chip{display:inline-flex;align-items:center;gap:4px;border:1px solid var(--line-s);border-radius:999px;background:#fff;padding:4px 6px 4px 12px;min-height:40px}
.sb-chip input{border:0;font:inherit;font-size:15px;width:6.5em;min-width:0;background:transparent;padding:4px 0}
.sb-chip button,.sb-x{border:0;background:#F1F3F6;color:var(--muted);width:28px;height:28px;border-radius:50%;font-size:16px;line-height:1;cursor:pointer;flex:none}
.sb-add{border:1px dashed var(--acc);color:var(--acc);background:#F3F8FF;border-radius:999px;min-height:40px;padding:0 14px;font:inherit;font-size:14.5px;font-weight:700;cursor:pointer}
.sb-items{display:flex;flex-direction:column;gap:10px;margin-top:6px}
.sb-it{border:1px solid var(--line-s);border-radius:14px;padding:12px;background:#FBFCFE}
.sb-it .r1{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,9em) auto;gap:8px;align-items:center}
.sb-it input,.sb-it select,.sb-f input,.sb-f select{font:inherit;font-size:16px;padding:9px 10px;border:1px solid var(--line-s);border-radius:10px;min-height:44px;width:100%;box-sizing:border-box;background:#fff}
.sb-it .r2{display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px;align-items:center;margin-top:8px;font-size:13.5px;font-weight:700;color:var(--head)}
.sb-it .who{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.sb-it .who label{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--line-s);border-radius:999px;padding:5px 10px;font-size:14px;background:#fff;cursor:pointer}
.sb-it .who input{width:18px;height:18px;min-height:0;margin:0}
.sb-f{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:12px}
.sb-f label{display:flex;flex-direction:column;gap:5px;font-size:13.5px;font-weight:700;color:var(--head)}
.sb-res{margin-top:14px;border-radius:16px;background:#F3F8FF;border:1px solid #D6E6FD;padding:14px}
.sb-sum{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;text-align:center}
.sb-sum b{display:block;font-size:20px;color:var(--head)}.sb-sum span{font-size:12.5px;color:var(--muted)}
.sb-tr{list-style:none;margin:12px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}
.sb-tr li{display:flex;justify-content:space-between;gap:10px;align-items:center;background:#fff;border-radius:12px;padding:10px 12px;border:1px solid #E3ECFA;font-size:15.5px;flex-wrap:wrap}
.sb-tr li b{color:#E8590C;font-size:17px;white-space:nowrap}
.sb-tb{width:100%;border-collapse:collapse;margin-top:12px;font-size:14px}
.sb-tb th,.sb-tb td{padding:7px 6px;border-bottom:1px solid #E3ECFA;text-align:right}
.sb-tb th:first-child,.sb-tb td:first-child{text-align:left}
.sb-btns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:12px}
.sb-btns button{min-height:46px;border-radius:12px;border:1px solid var(--line-s);background:#fff;font:inherit;font-size:14.5px;font-weight:700;cursor:pointer}
.sb-btns button.p{background:var(--acc);border-color:var(--acc);color:#fff}
.sb-msg{font-size:13px;color:var(--muted);margin-top:8px;min-height:1em}
.sb-q{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.sb-ex{width:100%;border-collapse:collapse;font-size:14.5px}.sb-ex th,.sb-ex td{border-bottom:1px solid var(--line-s);padding:8px 6px;text-align:left;vertical-align:top}
@media(max-width:560px){.sb-it .r1{grid-template-columns:minmax(0,1fr) minmax(0,8em) auto}.sb-q{grid-template-columns:1fr 1fr}.sb-q label:first-child{grid-column:1/-1}.sb-sum b{font-size:17px}.sb-btns{grid-template-columns:1fr 1fr}.sb-btns button.p{grid-column:1/-1}
.sb-ex thead{display:none}.sb-ex,.sb-ex tbody,.sb-ex tr{display:block}.sb-ex tr{border-bottom:1px solid var(--line-s);padding:6px 0}.sb-ex td{display:flex;justify-content:space-between;gap:10px;border:0;padding:3px 0;text-align:right}.sb-ex td::before{content:attr(data-l);font-weight:700;color:var(--muted);text-align:left;flex:none;white-space:nowrap}}
</style>'''
EX=[('저녁 모임 4명','고기 128,000원(민수 결제) · 2차 맥주 52,000원(지은 결제, 술 안 마신 현우 제외)','민수: 31,999원 받기 쪽 → 현우 32,000 · 서연 49,333…','현우 → 민수 32,000원, 서연 → 민수 49,333원, 서연 ↔ 지은 …'),]
main=f'''<main class="wrap wide"><header class="top"><p class="crumb"><a href="/">홈</a> › <a href="/life/">생활·행정</a></p><h1>N빵 정산 계산기</h1><p class="lead">모임·여행에서 각자 결제한 돈을 넣으면, <b>누가 누구에게 얼마를 보내면 끝나는지</b> 송금 횟수가 가장 적게 정리해 드려요. 항목마다 함께한 사람만 고를 수 있어서 술 안 마신 사람, 늦게 온 사람도 공평하게 나눌 수 있어요.</p></header>
<section class="card tool"><h2>간단 N빵</h2>
<div class="sb-q sb-f" style="margin-top:0"><label>총 금액 (원)<input id="q-t" inputmode="numeric" value="127,000"></label><label>사람 수<input id="q-n" inputmode="numeric" value="4"></label><label>단위<select id="q-u"><option value="1">1원</option><option value="10">10원</option><option value="100" selected>100원</option><option value="1000">1,000원</option></select></label></div>
<div class="sb-res" id="q-out"></div>
</section>
<section class="card tool"><h2>항목별 정산 (누가 누구에게)</h2>
<p style="margin:0 0 6px;font-size:14px;color:var(--muted)">① 함께한 사람 → ② 쓴 돈(낸 사람·함께한 사람) → ③ 결과에서 송금 목록 확인</p>
<h3 style="margin:10px 0 6px;font-size:15.5px">① 함께한 사람</h3>
<div class="sb-row" id="ppl"></div>
<h3 style="margin:16px 0 6px;font-size:15.5px">② 쓴 돈</h3>
<div class="sb-items" id="items"></div>
<button type="button" class="sb-add" id="add-it" style="margin-top:10px">+ 항목 추가</button>
<div class="sb-f"><label>송금 단위<select id="unit"><option value="1">1원 (정확히)</option><option value="10">10원</option><option value="100" selected>100원</option><option value="1000">1,000원</option></select></label><label>모임 이름 (공유 문구용)<input id="title" value="정산"></label></div>
<h3 style="margin:18px 0 6px;font-size:15.5px">③ 결과</h3>
<div class="sb-res" id="out"></div>
<div class="sb-btns"><button type="button" class="p" id="copy">카톡에 보낼 문구 복사</button><button type="button" id="share">링크로 공유</button><button type="button" id="reset">처음부터</button></div>
<p class="sb-msg" id="msg" aria-live="polite"></p>
<p class="sb-msg">입력 내용은 서버로 보내지 않고 이 기기에만 저장돼요.</p>
</section>
<section class="card"><h2>이렇게 계산해요</h2><ul class="xp">
<li><b>각자 몫</b> = 각 항목 금액 ÷ 그 항목을 함께한 사람 수를, 그 사람이 낀 항목마다 더한 값이에요.</li>
<li><b>차액</b> = 실제로 결제한 돈 − 내야 할 몫. 플러스면 받을 사람, 마이너스면 보낼 사람이에요.</li>
<li><b>송금 목록</b>은 가장 많이 보내야 하는 사람과 가장 많이 받아야 하는 사람부터 짝지어 만들어요. 사람이 n명이면 송금은 최대 n − 1번이에요.</li>
<li><b>송금 단위</b>를 100원으로 하면 송금액만 100원 단위로 반올림해요. 한 번 보낼 때 최대 50원까지 차이가 날 수 있어요.</li></ul></section>
<section class="card"><h2>정산 예시</h2>
<table class="sb-ex"><thead><tr><th>상황</th><th>입력</th><th>결과 (송금)</th></tr></thead><tbody>
<tr><td data-l="상황">저녁 4명, 한 명이 다 냄</td><td data-l="입력">민수가 128,000원 결제, 4명 모두 참여</td><td data-l="결과">지은·현우·서연 → 민수 각 32,000원 (3번)</td></tr>
<tr><td data-l="상황">1·2차 결제자가 다름</td><td data-l="입력">1차 120,000원 민수 결제 (4명) · 2차 60,000원 지은 결제 (현우 빼고 3명)</td><td data-l="결과">서연 → 민수 50,000원 · 현우 → 민수 20,000원 · 현우 → 지은 10,000원 (3번)</td></tr>
<tr><td data-l="상황">여행 3명, 셋 다 조금씩 냄</td><td data-l="입력">숙소 240,000원 A · 렌터카 90,000원 B · 식비 75,000원 C (모두 3명)</td><td data-l="결과">1인 몫 135,000원 → B → A 45,000원 · C → A 60,000원 (2번)</td></tr>
</tbody></table></section>
<section class="card"><h2>정산 꿀팁</h2><ul class="xp">
<li>결제할 때마다 바로 한 줄씩 넣어 두면 끝나고 다툴 일이 없어요. 링크로 공유하면 모두가 같은 화면을 봐요.</li>
<li>술값·디저트처럼 일부만 먹은 건 따로 한 줄로 넣고 함께한 사람만 체크하세요.</li>
<li>총무가 여러 번 결제했다면 결제한 사람만 총무로 바꿔 넣으면 돼요.</li>
<li>현금을 걷어 둔 '회비'가 있으면 그 사람이 회비만큼 결제한 것처럼 한 줄로 넣으면 정확해요.</li></ul></section>
<section class="card"><h2>자주 묻는 질문</h2><dl class="pe-faq">{''.join(f"<dt>{q}</dt><dd>{x}</dd>" for q,x in FAQ)}</dl></section>
<section class="card rel"><h2>함께 쓰면 좋은 도구</h2><ul class="tlist"><li><a href="/life/midpoint.html"><b>중간지점 찾기</b><span>친구들과 만날 곳 추천 + 공유 카드</span></a></li><li><a href="/life/taxi-fare.html"><b>택시비·통행료 계산기</b><span>택시비·기름값 비교, 인원 나누기</span></a></li><li><a href="/life/"><b>생활·행정 도구 모음</b><span>생활 도구 전체 보기</span></a></li></ul></section>
</main>
'''
JS=r'''<script>
(function(){
var $=function(i){return document.getElementById(i)},K='hl-splitbill-v1';
var W=function(n){return Math.round(n).toLocaleString('ko-KR')+'원'};
var num=function(v){v=String(v||'').replace(/[^0-9.\-]/g,'');var n=parseFloat(v);return isFinite(n)?n:0};
var esc=function(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
/* quick */
function quick(){var t=num($('q-t').value),n=Math.max(1,Math.floor(num($('q-n').value))),u=+$('q-u').value;var ex=t/n;
 var up=Math.ceil(ex/u)*u,dn=Math.floor(ex/u)*u;var h='<div class="sb-sum"><div><b>'+W(ex)+'</b><span>1인당 (정확히)</span></div><div><b>'+W(up)+'</b><span>'+u.toLocaleString()+'원 단위 올림</span></div><div><b>'+W(dn)+'</b><span>'+u.toLocaleString()+'원 단위 내림</span></div></div>';
 if(t>0&&up*n!==t)h+='<p class="sb-msg" style="color:var(--head)">올림으로 걷으면 '+W(up*n-t)+'이 남고, 내림으로 걷으면 결제한 사람이 '+W(t-dn*n)+'을 더 내요.</p>';
 $('q-out').innerHTML=h}
['q-t','q-n','q-u'].forEach(function(i){$(i).addEventListener('input',quick);$(i).addEventListener('change',quick)});
/* state */
var S;function def(){return {p:['나','친구1','친구2','친구3'],it:[{n:'1차 식사',a:128000,by:0,w:[0,1,2,3]},{n:'2차 카페',a:24000,by:1,w:[0,1,2,3]}],u:100,t:'정산'}}
function load(){try{var h=location.hash.slice(1);if(h.indexOf('s=')===0){return JSON.parse(decodeURIComponent(escape(atob(h.slice(2).replace(/-/g,'+').replace(/_/g,'/')))))}}catch(e){}
 try{var v=localStorage.getItem(K);if(v)return JSON.parse(v)}catch(e){}return def()}
function save(){try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}}
function renderP(){var h=S.p.map(function(n,i){return '<span class="sb-chip"><input data-p="'+i+'" value="'+esc(n)+'" aria-label="이름 '+(i+1)+'" maxlength="12">'+(S.p.length>2?'<button type="button" data-rp="'+i+'" aria-label="'+esc(n)+' 빼기">×</button>':'')+'</span>'}).join('')+'<button type="button" class="sb-add" id="add-p">+ 사람</button>';$('ppl').innerHTML=h;
 $('add-p').onclick=function(){if(S.p.length>=20)return;S.p.push('친구'+S.p.length);S.it.forEach(function(it){it.w.push(S.p.length-1)});all()}}
function renderI(){$('items').innerHTML=S.it.map(function(it,k){var opts=S.p.map(function(n,i){return '<option value="'+i+'"'+(it.by===i?' selected':'')+'>'+esc(n)+'</option>'}).join('');
  var who=S.p.map(function(n,i){return '<label><input type="checkbox" data-w="'+k+'" value="'+i+'"'+(it.w.indexOf(i)>=0?' checked':'')+'>'+esc(n)+'</label>'}).join('');
  return '<div class="sb-it"><div class="r1"><input data-n="'+k+'" value="'+esc(it.n)+'" aria-label="항목 이름" maxlength="20"><input data-a="'+k+'" inputmode="numeric" value="'+(it.a?Math.round(it.a).toLocaleString('ko-KR'):'')+'" placeholder="금액" aria-label="금액"><button type="button" class="sb-x" data-ri="'+k+'" aria-label="항목 삭제">×</button></div><div class="r2"><span>낸 사람</span><select data-b="'+k+'" aria-label="낸 사람">'+opts+'</select></div><div class="who"><span style="font-size:13px;color:var(--muted);align-self:center">함께한 사람</span>'+who+'</div></div>'}).join('')}
function calc(){var n=S.p.length,paid=Array(n).fill(0),owe=Array(n).fill(0),tot=0;
 S.it.forEach(function(it){var a=+it.a||0,w=it.w.filter(function(i){return i<n});if(a<=0||!w.length)return;tot+=a;paid[it.by]+=a;w.forEach(function(i){owe[i]+=a/w.length})});
 var bal=paid.map(function(p,i){return p-owe[i]}),u=S.u||1;
 var cr=[],db=[];bal.forEach(function(b,i){if(b>0.5)cr.push([i,b]);else if(b<-0.5)db.push([i,-b])});cr.sort(function(a,b){return b[1]-a[1]});db.sort(function(a,b){return b[1]-a[1]});
 var tr=[],ci=0,di=0;while(ci<cr.length&&di<db.length){var m=Math.min(cr[ci][1],db[di][1]);var r=Math.round(m/u)*u;if(r>0)tr.push([db[di][0],cr[ci][0],r]);cr[ci][1]-=m;db[di][1]-=m;if(cr[ci][1]<0.5)ci++;if(db[di][1]<0.5)di++}
 return {paid:paid,owe:owe,bal:bal,tot:tot,tr:tr}}
function show(){var R=calc(),P=S.p;
 var h='<div class="sb-sum"><div><b>'+W(R.tot)+'</b><span>총 지출</span></div><div><b>'+P.length+'명</b><span>참여</span></div><div><b>'+R.tr.length+'번</b><span>송금 횟수</span></div></div>';
 h+=R.tr.length?'<ul class="sb-tr">'+R.tr.map(function(t){return '<li><span>'+esc(P[t[0]])+' → '+esc(P[t[1]])+'</span><b>'+W(t[2])+'</b></li>'}).join('')+'</ul>':'<p class="sb-msg" style="color:var(--head)">보낼 돈이 없어요. 모두 자기 몫만큼 냈어요.</p>';
 h+='<table class="sb-tb"><thead><tr><th>이름</th><th>낸 돈</th><th>내야 할 몫</th><th>차액</th></tr></thead><tbody>'+P.map(function(n,i){var b=R.bal[i];return '<tr><td>'+esc(n)+'</td><td>'+W(R.paid[i])+'</td><td>'+W(R.owe[i])+'</td><td style="color:'+(b>0.5?'#1C64D9':b<-0.5?'#E8590C':'var(--muted)')+'">'+(b>0.5?'+':'')+W(b)+'</td></tr>'}).join('')+'</tbody></table>';
 $('out').innerHTML=h;return R}
function text(R){var P=S.p,L=['['+(S.t||'정산')+'] 총 '+W(R.tot)+' · '+P.length+'명'];S.it.forEach(function(it){if(+it.a>0)L.push('- '+it.n+' '+W(it.a)+' ('+P[it.by]+' 결제, '+it.w.length+'명)')});L.push('');
 if(R.tr.length){L.push('보낼 돈');R.tr.forEach(function(t){L.push(P[t[0]]+' → '+P[t[1]]+' '+W(t[2]))})}else L.push('보낼 돈 없음');L.push('');L.push('홍라이프 N빵 정산 계산기');return L.join('\n')}
function all(){S.u=+$('unit').value;S.t=$('title').value;renderP();renderI();var R=show();save();return R}
function upd(){S.u=+$('unit').value;S.t=$('title').value;show();save()}
document.addEventListener('input',function(e){var t=e.target,d=t.dataset;
 if(d.p!==undefined){S.p[+d.p]=t.value||('친구'+d.p);renderI();upd()}
 else if(d.n!==undefined){S.it[+d.n].n=t.value;upd()}
 else if(d.a!==undefined){S.it[+d.a].a=num(t.value);upd()}});
document.addEventListener('change',function(e){var t=e.target,d=t.dataset;
 if(d.a!==undefined){t.value=S.it[+d.a].a?Math.round(S.it[+d.a].a).toLocaleString('ko-KR'):''}
 if(d.b!==undefined){S.it[+d.b].by=+t.value;upd()}
 if(d.w!==undefined){var it=S.it[+d.w],v=+t.value,ix=it.w.indexOf(v);if(t.checked&&ix<0)it.w.push(v);if(!t.checked&&ix>=0)it.w.splice(ix,1);upd()}
 if(t.id==='unit'||t.id==='title')upd()});
document.addEventListener('click',function(e){var t=e.target.closest('button');if(!t)return;var d=t.dataset;
 if(d.rp!==undefined){var r=+d.rp;S.p.splice(r,1);S.it.forEach(function(it){if(it.by===r)it.by=0;else if(it.by>r)it.by--;it.w=it.w.filter(function(i){return i!==r}).map(function(i){return i>r?i-1:i})});all()}
 if(d.ri!==undefined){S.it.splice(+d.ri,1);all()}});
$('add-it').onclick=function(){S.it.push({n:(S.it.length+1)+'번째 항목',a:0,by:0,w:S.p.map(function(_,i){return i})});all();var x=document.querySelectorAll('[data-a]');if(x.length)x[x.length-1].focus()};
$('copy').onclick=function(){var t=text(calc());(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){$('msg').textContent='복사했어요. 카톡 대화방에 붙여넣으세요.'},function(){prompt('아래 내용을 복사하세요',t)})};
$('share').onclick=function(){var s=btoa(unescape(encodeURIComponent(JSON.stringify(S)))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');var u=location.origin+location.pathname+'#s='+s;
 if(navigator.share){navigator.share({title:(S.t||'정산')+' N빵',url:u}).catch(function(){})}else{(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){$('msg').textContent='공유 링크를 복사했어요.'},function(){prompt('공유 링크',u)})}};
$('reset').onclick=function(){S=def();try{localStorage.removeItem(K)}catch(e){}history.replaceState(null,'',location.pathname);$('unit').value='100';$('title').value='정산';all();$('msg').textContent='처음 상태로 돌렸어요.'};
S=load();$('unit').value=String(S.u||100);$('title').value=S.t||'정산';all();quick();
})();
</script>
'''
out=head+CSS+between+main+JS+tail
open('/home/claude/coio/overlay/life/split-bill.html','w',encoding='utf-8').write(out)
print(len(out))
