"""경유지 많은 노선 내비 (/life/route-navi.html) — 지도에서 찍어 정류장 등록 → 순서대로 내비 앱으로 안내"""
import os, json, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import navi_selfnav as SN, navi_adapter as AD
D = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
E = lambda x: html.escape(str(x), quote=True)
HEAD = open(f'{D}/tpl_head.html').read(); MID = open(f'{D}/tpl_mid.html').read()
BRAND = open(f'{D}/tpl_brand.html').read(); TAIL = open(f'{D}/tpl_tail.html').read()
SITE = 'https://honglife.co.kr'
PATH = '/life/route-navi.html'
TITLE = '경유지 30곳 넘는 노선 내비 · 지도에서 찍어 만드는 순서 길안내 | 홍라이프 도구'
DESC = '지도를 눌러 정류장을 차례로 찍으면 노선이 만들어지고, 운행 중엔 버튼 한 번으로 네이버·카카오·티맵 내비가 다음 정류장까지 안내해요. 셔틀·통학버스, 택배, 방문 영업처럼 들를 곳이 많을 때 쓰세요.'
FAQ = [
 ('경유지를 몇 곳까지 넣을 수 있나요?', '개수 제한이 없어요. 30곳, 50곳도 넣을 수 있어요. 일반 내비 앱은 경유지를 몇 곳까지만 받기 때문에, 이 도구는 정류장을 하나씩(네이버 지도는 최대 5곳씩 묶어서) 내비 앱에 넘겨 줘요.'),
 ('길 안내 음성은 어디서 나오나요?', '버튼을 누르면 휴대폰에 깔린 네이버 지도·카카오맵·티맵이 열려 평소처럼 음성 안내를 해요. 실시간 교통 정보도 그 앱의 것을 그대로 써요.'),
 ('만든 노선은 어디에 저장되나요?', '지금 쓰는 휴대폰(브라우저)에만 저장돼요. 서버로 보내지 않아요. 다른 기기로 옮기거나 다른 사람에게 보내려면 "노선 공유 링크"를 보내면 돼요.'),
 ('주소를 몰라도 되나요?', '네. 지도를 확대해 정류장 위치를 눌러 찍기만 하면 돼요. 찍은 핀은 길게 눌러 끌어서 위치를 고칠 수 있고, 이름은 목록에서 바꿀 수 있어요.'),
 ('전체 노선 한 번에 안내는 어떻게 작동하나요?', '출발할 때 한 번 누르면 모든 정류장을 이은 경로를 받아, 휴대폰 위치를 따라가며 회전 지점과 정류장 앞에서 음성으로 알려 줘요. 정류장에 닿으면 자동으로 다음 정류장으로 넘어가고, 길을 벗어나면 남은 정류장으로 경로를 다시 찾아요. 지금은 베타라 실시간 교통은 반영하지 않아요. 운전 전에 “모의 주행”으로 미리 확인해 보세요.'),
 ('운전 중에 써도 되나요?', '달리는 중에는 휴대폰을 만지면 안 돼요(도로교통법). 그래서 버튼 한 번에 6곳씩 내비로 넘기고, 누르면 다음 묶음이 자동으로 준비되게 만들었어요. 정류장에 섰을 때만 누르면 30곳 노선도 5번이면 끝나요. 노선 만들기와 순서 수정은 운행 전에 해 두세요.'),
]

BODY = r'''<h1>경유지 많은 노선 내비</h1><p class="lead">지도를 눌러 정류장을 차례로 찍으면 노선이 돼요. 운행할 땐 “다음 정류장 안내”를 누르면 네이버 지도·카카오맵·티맵이 다음 정류장까지 길을 안내해요. 경유지가 30곳을 넘어도 괜찮아요.</p>
<div class="safe"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>노선과 정류장은 서버로 보내지 않고 이 기기에만 저장돼요</div></header>
<section class="card rn">
<div class="rn-top">
 <label class="rn-sel"><span>노선</span><select id="rsel" aria-label="노선 고르기"></select></label>
 <div class="rn-tb"><button type="button" class="btn ghost" id="rnew">새 노선</button><button type="button" class="btn ghost" id="rren">이름 바꾸기</button><button type="button" class="btn ghost" id="rdel">삭제</button></div>
</div>
<div class="rn-mode" role="tablist"><button type="button" role="tab" id="m-edit" aria-selected="true">노선 만들기</button><button type="button" role="tab" id="m-run" aria-selected="false">운행하기</button></div>
<div class="rn-map"><div id="map" aria-label="정류장 지도"></div>
 <p class="rn-hint" id="hint">지도를 눌러 1번 정류장부터 차례로 찍어 주세요</p>
 <button type="button" class="rn-me" id="me" aria-label="내 위치로 이동"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg></button>
</div>
<div id="pane-edit">
 <button type="button" class="btn rn-pv" id="pv">내가 찍은 노선, 실제 도로로 확인하기</button>
 <p class="rn-pvs" id="pvs" hidden></p>
 <p class="rn-sum" id="sum"></p>
 <ol class="rn-list" id="list"></ol>
 <div class="rn-tb rn-bot"><button type="button" class="btn ghost" id="undo">마지막 정류장 빼기</button><button type="button" class="btn ghost" id="rev">순서 뒤집기</button><button type="button" class="btn" id="share">노선 공유 링크</button></div>
</div>
<div id="pane-run" hidden>
 <div class="rn-next"><p class="rn-k" id="nk"></p><p class="rn-nm" id="nn"></p><p class="rn-sub" id="ns"></p>
  __SELFBTN__<a class="btn rn-nv rn-big" id="go-naver5" href="#"><b id="b5t">네이버 내비로 6곳 한 번에</b><span id="b5s"></span></a>
  <p class="rn-or">한 곳씩 안내</p>
  <div class="rn-go"><a class="btn rn-nv" id="go-naver" href="#">네이버</a><a class="btn rn-kk" id="go-kakao" href="#" target="_blank" rel="noopener">카카오맵</a><a class="btn rn-tm" id="go-tmap" href="#">티맵</a></div>
  <div class="rn-step"><button type="button" class="btn ghost" id="prev">이전 정류장</button><button type="button" class="btn ghost" id="next">다음 정류장으로</button></div>
  <button type="button" class="rn-reset" id="restart">처음 정류장부터 다시</button>
 </div>
 <p class="rn-warn">“전체 노선 한 번에 안내”는 출발 전 한 번만 누르면 끝까지 음성으로 안내하고, 정류장에 닿으면 알아서 다음 정류장으로 넘어가요. 화면을 켠 채 거치대에 꽂아 두세요. 내비 앱으로 넘기는 버튼은 정류장에 섰을 때만 누르세요.</p>
</div>
</section>
<section class="card"><h2>이렇게 쓰세요</h2><ol class="rn-how">
<li><b>노선 만들기</b>에서 지도를 확대하고 정류장 자리를 순서대로 눌러요. 번호가 붙은 핀이 생겨요.</li>
<li>핀은 길게 눌러 끌면 위치가 바뀌어요. 목록에서 이름을 적고, 화살표로 순서를 바꿔요.</li>
<li>노선을 여러 개(A코스, B코스…) 만들어 두고 위에서 골라 써요.</li>
<li><b>운행하기</b>를 누르고, 정류장에 서 있을 때 초록 버튼을 한 번 누르면 네이버 내비가 6곳을 한 번에 안내해요. 누르는 순간 다음 묶음이 자동으로 준비되니, 6곳을 다 돌고 마지막 정류장에 섰을 때 또 한 번만 누르면 돼요.</li>
<li><b>노선 공유 링크</b>를 보내면 받는 사람 휴대폰에서도 같은 노선이 그대로 열려요.</li>
</ol></section>
<section class="card"><h2>자주 묻는 질문</h2>__FAQ__</section>
<p class="upd">지도·경로 © Kakao, 카카오모빌리티 (연결이 안 될 때는 OpenStreetMap) · 내비 앱 안내는 각 앱이 제공해요 · 업데이트 2026년 11월 19일</p>'''

CSS = r'''<link rel="stylesheet" href="/assets/vendor/leaflet/leaflet.css">
<style id="hl-rn">
.rn{padding-top:16px}
#map svg,#map img,#nvmap svg,#nvmap img{max-width:none!important;max-height:none!important}
.rn-top{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
.rn-sel{display:flex;align-items:center;gap:8px;min-width:0;flex:1 1 220px}.rn-sel span{font-weight:700;color:var(--head);flex:none}
.rn-sel select{flex:1;min-width:0;height:44px;border:1px solid var(--line);border-radius:12px;padding:0 12px;font-size:16px;font-weight:700;background:#fff;color:var(--head)}
.rn-tb{display:flex;flex-wrap:wrap;gap:6px}.rn-tb .btn{min-height:40px;padding:8px 12px;font-size:14px}
.rn-mode{display:grid;grid-template-columns:1fr 1fr;margin:14px 0 10px;background:#F2F4F6;border-radius:14px;padding:4px}
.rn-mode button{border:0;background:none;min-height:42px;border-radius:11px;font-size:15px;font-weight:700;color:var(--muted);cursor:pointer}
.rn-mode button[aria-selected=true]{background:#fff;color:var(--head);box-shadow:0 1px 4px rgba(0,0,0,.08)}
.rn-map{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line)}
#map{height:min(62vh,520px);min-height:340px;background:#E8EEF3}
.rn-hint{position:absolute;left:10px;right:10px;bottom:28px;text-align:center;margin:0;z-index:500;background:rgba(25,31,40,.86);color:#fff;font-size:13.5px;font-weight:600;padding:8px 12px;border-radius:10px;pointer-events:none;line-height:1.4;word-break:keep-all}
.rn-me{position:absolute;right:10px;top:10px;z-index:500;width:40px;height:40px;border-radius:12px;border:1px solid var(--line);background:#fff;display:grid;place-items:center;color:var(--head);cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.12)}
.rn-pin{display:grid;place-items:center;width:30px;height:30px;border-radius:50% 50% 50% 4px;transform:rotate(-45deg);background:#3182F6;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.rn-pin b{transform:rotate(45deg);color:#fff;font:800 12.5px/1 system-ui,sans-serif}
.rn-pin.done{background:#B0B8C1}.rn-pin.cur{background:#F04452;width:36px;height:36px}.rn-pin.cur b{font-size:14px}
.rn-pv{width:100%;min-height:52px;margin-top:12px;font-size:16px;background:#F04452!important;border-color:#F04452!important;color:#fff!important}
.rn-pvs{margin:10px 0 0;padding:10px 12px;border-radius:12px;background:#FFF0F1;color:#C9303E;font-size:14px;font-weight:700;line-height:1.5;word-break:keep-all}
.rn-sum{margin:14px 0 8px;font-size:14px;color:var(--muted)}
.rn-list{list-style:none;margin:0;padding:0;display:grid;gap:6px;max-height:420px;overflow:auto}
.rn-list li{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:8px;align-items:center;padding:6px 6px 6px 8px;border:1px solid var(--line);border-radius:12px;background:#fff}
.rn-list .no{width:26px;height:26px;border-radius:50%;background:#3182F6;color:#fff;font-size:12.5px;font-weight:800;display:grid;place-items:center}
.rn-list input{min-width:0;width:100%;height:38px;border:0;background:#F7F8FA;border-radius:9px;padding:0 10px;font-size:15px;color:var(--head)}
.rn-list .ac{display:flex;gap:2px}.rn-list .ac button{width:34px;height:36px;border:0;background:none;border-radius:9px;font-size:16px;color:var(--muted);cursor:pointer}
.rn-list .ac button:hover{background:#F2F4F6;color:var(--head)}.rn-list .ac button:disabled{opacity:.3}
.rn-list .em{grid-column:1/-1;text-align:center;color:var(--muted);font-size:14px;padding:14px;border-style:dashed}
.rn-bot{margin-top:12px}
.rn-next{margin-top:14px;padding:18px 16px;border-radius:16px;background:#F7F9FC;border:1px solid var(--line)}
.rn-k{margin:0;font-size:13px;font-weight:700;color:#F04452}.rn-nm{margin:4px 0 2px;font-size:24px;font-weight:800;color:var(--head);line-height:1.3;word-break:keep-all}
.rn-sub{margin:0 0 14px;font-size:14px;color:var(--muted)}
.rn-go{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.rn-go .btn{min-height:52px;font-size:15px;padding:8px 4px;justify-content:center;text-align:center;white-space:nowrap}
.rn-nv{background:#03C75A!important;border-color:#03C75A!important;color:#fff!important}.rn-kk{background:#FEE500!important;border-color:#FEE500!important;color:#191919!important}.rn-tm{background:#EB2D3A!important;border-color:#EB2D3A!important;color:#fff!important}
.rn-big{display:flex!important;flex-direction:column;align-items:center;gap:3px;min-height:72px;width:100%;padding:12px 10px;text-align:center}.rn-big b{font-size:18px}.rn-big span{font-size:13.5px;font-weight:600;opacity:.92;word-break:keep-all}
.rn-or{margin:14px 0 8px;font-size:13px;color:var(--muted);text-align:center}
.rn-step{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}.rn-step .btn{min-height:46px;font-size:15px}
.rn-reset{display:block;margin:12px auto 0;border:0;background:none;color:var(--muted);font-size:13.5px;text-decoration:underline;cursor:pointer}
.rn-warn{margin:12px 0 0;font-size:13px;color:var(--muted)}
.rn-how{margin:0;padding-left:20px;display:grid;gap:8px;line-height:1.6}
.rn-toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);background:#191F28;color:#fff;padding:12px 18px;border-radius:12px;font-size:14px;z-index:9999;max-width:90vw}
[hidden]{display:none!important}'''+SN.CSS+r'''
@media(max-width:480px){.rn-tb .btn{font-size:13.5px;padding:8px 10px}.rn-nm{font-size:21px}}
</style>'''

JS = r'''<script src="/assets/vendor/leaflet/leaflet.js"></script>
__ADAPTER__
<script>HM.ready(function(){
var KEY='hl-route-navi-v1',S;try{S=JSON.parse(localStorage.getItem(KEY))}catch(e){}
if(!S||!S.routes){S={routes:{'A코스':[]},cur:'A코스',pos:{}}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}}
function R(){return S.routes[S.cur]||(S.routes[S.cur]=[])}
function toast(m){var t=document.createElement('div');t.className='rn-toast';t.textContent=m;document.body.appendChild(t);setTimeout(function(){t.remove()},2400)}
var $=function(i){return document.getElementById(i)};
var map=HM.make(document.getElementById('map'),37.45,126.7,11),pins=[],line=map.line([],{color:'#3182F6',weight:4,opacity:.75,dash:true}),me=null;
var mode='edit';
function idx(){return Math.min(S.pos[S.cur]||0,Math.max(R().length-1,0))}
function km(a,b){var r=Math.PI/180,x=(b.lng-a.lng)*r*Math.cos((a.lat+b.lat)/2*r),y=(b.lat-a.lat)*r;return Math.sqrt(x*x+y*y)*6371}
var rl=null,rsig='';function sig(){return JSON.stringify(R().map(function(p){return [p.lat,p.lng]}))+S.cur}
function draw(fit){if(rl&&rsig!=sig()){rl.remove();rl=null;$('pvs').hidden=true}pins.forEach(function(x){x.remove()});var st=R(),ci=idx();
 pins=st.map(function(p,i){var cls=mode=='run'?(i<ci?'done':i==ci?'cur':''):'';
  return map.pin(p.lat,p.lng,{label:i+1,cls:cls,drag:mode=='edit',title:(i+1)+'. '+(p.n||'정류장'),onDrag:function(a,b){p.lat=+a.toFixed(6);p.lng=+b.toFixed(6);save();draw()}})});
 line.set(rl?[]:st.map(function(p){return [p.lat,p.lng]}));
 if(fit&&st.length)map.fit(st.map(function(p){return [p.lat,p.lng]}));
 list();run();}
function list(){var st=R(),ol=$('list');var d=0;for(var i=1;i<st.length;i++)d+=km(st[i-1],st[i]);
 $('sum').textContent=st.length?('정류장 '+st.length+'곳 · 직선거리 합계 약 '+d.toFixed(1)+'km (실제 도로는 더 길어요)'):'';
 $('hint').textContent=mode=='edit'?(st.length?'지도를 누르면 '+(st.length+1)+'번 정류장이 추가돼요':'지도를 눌러 1번 정류장부터 차례로 찍어 주세요'):'빨간 핀이 다음 정류장이에요';
 if(!st.length){ol.innerHTML='<li class="em">아직 정류장이 없어요. 위 지도를 눌러 추가하세요.</li>';return}
 ol.innerHTML=st.map(function(p,i){return '<li><span class="no">'+(i+1)+'</span><input value="'+(p.n||'').replace(/"/g,'&quot;')+'" placeholder="정류장 '+(i+1)+' 이름" data-i="'+i+'" aria-label="'+(i+1)+'번 정류장 이름"><span class="ac"><button type="button" data-a="up" data-i="'+i+'" aria-label="위로"'+(i?'':' disabled')+'>↑</button><button type="button" data-a="dn" data-i="'+i+'" aria-label="아래로"'+(i<st.length-1?'':' disabled')+'>↓</button><button type="button" data-a="go" data-i="'+i+'" aria-label="지도에서 보기">◎</button><button type="button" data-a="rm" data-i="'+i+'" aria-label="삭제">✕</button></span></li>'}).join('');}
$('list').addEventListener('input',function(e){var i=e.target.dataset.i;if(i==null)return;R()[+i].n=e.target.value.slice(0,40);save();draw()});
$('list').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var i=+b.dataset.i,st=R(),a=b.dataset.a;
 if(a=='up'&&i>0){st.splice(i-1,0,st.splice(i,1)[0])}else if(a=='dn'&&i<st.length-1){st.splice(i+1,0,st.splice(i,1)[0])}else if(a=='rm'){st.splice(i,1)}else if(a=='go'){map.view(st[i].lat,st[i].lng,17);return}
 save();draw()});
map.onClick(function(la,ln){if(mode!='edit')return;var st=R();st.push({lat:+la.toFixed(6),lng:+ln.toFixed(6),n:''});save();draw();
 var ins=$('list').querySelectorAll('input');if(ins.length&&window.innerWidth>700)ins[ins.length-1].focus({preventScroll:true})});
$('pv').onclick=function(){var st=R();if(st.length<2){toast('정류장을 2곳 이상 찍어 주세요');return}var b=this;b.disabled=true;b.textContent='실제 도로 경로를 찾는 중…';
 HM.route(st.map(function(p){return [p.lat,p.lng]}),S.opt||{}).then(function(r){if(rl)rl.remove();rl=map.line([r.co[0]],{color:'#F04452',weight:3.5,opacity:.95});rsig=sig();line.set([]);
  document.querySelector('.rn-map').scrollIntoView({behavior:'smooth',block:'center'});map.fit(st.map(function(p){return [p.lat,p.lng]}).concat(r.co.filter(function(_,i){return i%10==0})));
  var n=r.co.length,k=1,step=Math.max(1,Math.ceil(n/120)),me=rl;clearInterval(window.__rnAnim);window.__rnAnim=setInterval(function(){if(rl!==me){clearInterval(window.__rnAnim);return}k=Math.min(n,k+step);me.set(r.co.slice(0,k));if(k>=n)clearInterval(window.__rnAnim)},40);
  var km=r.cum[r.cum.length-1]/1000,mn=Math.round(r.cum[r.cum.length-1]/r.spd/60);$('pvs').hidden=false;$('pvs').textContent='1번부터 순서대로 그려지는 빨간 선이 실제로 달릴 길이에요 · 총 '+km.toFixed(1)+'km · 약 '+mn+'분'+(r.src=='kakao'?' (카카오 기준)':' (예비 경로 서버 기준)')+'. 이상한 길로 돌면 그 길 위에 핀을 하나 더 찍어 고정하세요.'})
 .catch(function(){toast('경로를 찾지 못했어요. 잠시 뒤 다시 눌러 주세요')}).then(function(){b.disabled=false;b.textContent='내가 찍은 노선, 실제 도로로 확인하기'})};
$('undo').onclick=function(){R().pop();save();draw()};
$('rev').onclick=function(){R().reverse();save();draw()};
function sel(){$('rsel').innerHTML=Object.keys(S.routes).map(function(k){return '<option'+(k==S.cur?' selected':'')+'>'+k.replace(/</g,'&lt;')+'</option>'}).join('')}
$('rsel').onchange=function(){S.cur=this.value;save();draw(true)};
$('rnew').onclick=function(){var n=prompt('새 노선 이름 (예: B코스)');if(!n)return;n=n.trim().slice(0,20);if(!n)return;if(!S.routes[n])S.routes[n]=[];S.cur=n;save();sel();draw()};
$('rren').onclick=function(){var n=prompt('노선 이름',S.cur);if(!n)return;n=n.trim().slice(0,20);if(!n||n==S.cur)return;S.routes[n]=R();delete S.routes[S.cur];S.pos[n]=S.pos[S.cur];S.cur=n;save();sel()};
$('rdel').onclick=function(){if(!confirm('“'+S.cur+'” 노선을 지울까요? 되돌릴 수 없어요.'))return;delete S.routes[S.cur];var k=Object.keys(S.routes);if(!k.length){S.routes={'A코스':[]};k=['A코스']}S.cur=k[0];save();sel();draw(true)};
function setMode(m){mode=m;$('m-edit').setAttribute('aria-selected',m=='edit');$('m-run').setAttribute('aria-selected',m=='run');$('pane-edit').hidden=m!='edit';$('pane-run').hidden=m!='run';draw();
 if(m=='run'){var p=R()[idx()];if(p)map.view(p.lat,p.lng,15)}}
$('m-edit').onclick=function(){setMode('edit')};$('m-run').onclick=function(){if(!R().length){toast('먼저 정류장을 찍어 주세요');return}setMode('run')};
function nm(p,i){return p.n||('정류장 '+(i+1))}
function run(){var st=R();if(mode!='run'||!st.length)return;var i=idx(),p=st[i],q=encodeURIComponent(nm(p,i));
 $('nk').textContent='다음 정류장 · '+(i+1)+' / '+st.length;$('nn').textContent=nm(p,i);
 $('ns').textContent=i<st.length-1?('그다음: '+(i+2)+'. '+nm(st[i+1],i+1)):'마지막 정류장이에요';
 $('go-naver').href='nmap://navigation?dlat='+p.lat+'&dlng='+p.lng+'&dname='+q+'&appname=honglife.co.kr';
 $('go-kakao').href='https://map.kakao.com/link/to/'+q+','+p.lat+','+p.lng;
 $('go-tmap').href='tmap://route?goalname='+q+'&goalx='+p.lng+'&goaly='+p.lat;
 var rest=st.slice(i,i+6),last=rest[rest.length-1],u='nmap://route/car?dlat='+last.lat+'&dlng='+last.lng+'&dname='+encodeURIComponent(nm(last,i+rest.length-1));
 rest.slice(0,-1).forEach(function(v,k){u+='&v'+(k+1)+'lat='+v.lat+'&v'+(k+1)+'lng='+v.lng+'&v'+(k+1)+'name='+encodeURIComponent(nm(v,i+k))});
 $('go-naver5').href=u+'&appname=honglife.co.kr';$('go-naver5').dataset.n=rest.length;
 $('b5t').textContent=rest.length>1?'네이버 내비로 '+rest.length+'곳 한 번에':'네이버 내비로 안내';
 $('b5s').textContent=rest.length>1?((i+1)+'번 '+nm(st[i],i)+' → '+(i+rest.length)+'번 '+nm(last,i+rest.length-1)):((i+1)+'번 '+nm(st[i],i));
 $('prev').disabled=i==0;$('next').textContent=i<st.length-1?'다음 정류장으로':'운행 끝';}
function mob(){return /Android|iPhone|iPad/i.test(navigator.userAgent)}
['go-naver','go-tmap','go-naver5'].forEach(function(id){$(id).addEventListener('click',function(e){if(!mob()){e.preventDefault();toast('휴대폰에서 누르면 내비 앱이 열려요')}})});
function adv(n){var st=R(),i=idx();setTimeout(function(){S.pos[S.cur]=Math.min(i+n,st.length-1);if(i+n>st.length-1)S.pos[S.cur]=0;save();draw()},1500)}
$('go-naver5').addEventListener('click',function(){if(mob())adv(+this.dataset.n)});
['go-naver','go-kakao','go-tmap'].forEach(function(id){$(id).addEventListener('click',function(){if(mob())adv(1)})});
$('next').onclick=function(){var st=R(),i=idx();if(i>=st.length-1){toast('운행을 마쳤어요. 수고하셨어요!');S.pos[S.cur]=0}else S.pos[S.cur]=i+1;save();draw();var p=R()[idx()];map.pan(p.lat,p.lng)};
$('prev').onclick=function(){S.pos[S.cur]=Math.max(0,idx()-1);save();draw();var p=R()[idx()];map.pan(p.lat,p.lng)};
$('restart').onclick=function(){S.pos[S.cur]=0;save();draw(true)};
$('me').onclick=function(){if(!navigator.geolocation){toast('이 기기에서는 위치를 쓸 수 없어요');return}navigator.geolocation.getCurrentPosition(function(g){map.view(g.coords.latitude,g.coords.longitude,16);map.dot(g.coords.latitude,g.coords.longitude)},function(){toast('위치 권한을 허용해 주세요')},{enableHighAccuracy:true,timeout:8000})};
$('share').onclick=function(){var st=R();if(!st.length){toast('정류장을 먼저 찍어 주세요');return}
 var enc=encodeURIComponent(S.cur)+'|'+st.map(function(p){return p.lat.toFixed(5)+','+p.lng.toFixed(5)+','+encodeURIComponent(p.n||'')}).join(';');
 var url=location.origin+location.pathname+'#r='+enc;
 if(navigator.share){navigator.share({title:S.cur+' 노선',text:S.cur+' 노선 ('+st.length+'곳)',url:url}).catch(function(){})}else{navigator.clipboard.writeText(url).then(function(){toast('공유 링크를 복사했어요')})}};
function imp(){var m=location.hash.match(/^#r=([^|]+)\|(.+)$/);if(!m)return;try{var n=decodeURIComponent(m[1]).slice(0,20),st=m[2].split(';').map(function(s){var a=s.split(',');return {lat:+a[0],lng:+a[1],n:decodeURIComponent(a.slice(2).join(',')).slice(0,40)}}).filter(function(p){return isFinite(p.lat)&&isFinite(p.lng)});
 if(!st.length)return;if(S.routes[n]&&S.routes[n].length&&!confirm('이미 “'+n+'” 노선이 있어요. 받은 노선으로 바꿀까요?'))n=n+' (받음)';S.routes[n]=st;S.cur=n;S.pos[n]=0;save();history.replaceState(null,'',location.pathname);toast('“'+n+'” 노선을 불러왔어요 ('+st.length+'곳)')}catch(e){}}
imp();sel();draw(true);window.__rnRefresh=function(){try{S=JSON.parse(localStorage.getItem(KEY))||S}catch(e){}draw()};
});</script>'''

def main():
    faq = ''.join(f'<details class="xp"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": "경유지 많은 노선 내비", "url": SITE + PATH, "applicationCategory": "TravelApplication", "operatingSystem": "Web", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}, "description": DESC},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "생활·행정", "item": SITE + "/life/"}, {"@type": "ListItem", "position": 3, "name": "경유지 많은 노선 내비", "item": SITE + PATH}]}]}
    h = HEAD + f'<title>{E(TITLE)}</title>\n<meta name="description" content="{E(DESC)}">\n<link rel="canonical" href="{SITE}{PATH}">\n'
    h += f'<meta property="og:type" content="website"><meta property="og:url" content="{SITE}{PATH}"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="홍라이프 도구">\n'
    h += f'<meta property="og:title" content="{E(TITLE)}"><meta property="og:description" content="{E(DESC)}"><meta property="og:image" content="{SITE}/assets/og/site.png">\n'
    h += MID + '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS + '\n</head>\n<body>\n\n' + BRAND
    h += '<main class="wrap wide"><header class="top"><p class="crumb"><a href="/">홈</a> › <a href="/life/">생활·행정</a></p>' + BODY.replace('__FAQ__', faq).replace('__SELFBTN__', SN.BTN) + '</main>' + SN.HTML + JS.replace('__ADAPTER__', AD.JS.replace('__JSKEY__', AD.KAKAO_JS).replace('__PROXY__', AD.PROXY)) + SN.JS + TAIL
    os.makedirs(OUT + '/life', exist_ok=True)
    open(OUT + PATH, 'w', encoding='utf-8').write(h)
    print('ok', PATH)
main()
