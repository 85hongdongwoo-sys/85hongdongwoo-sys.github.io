# 셔틀 위치 공유: 기사용 /drive/bus-share.html + 승객용 /drive/bus.html
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_maptools as G
API = 'https://hl-bus.a599307.workers.dev'
REL = [('/life/route-navi.html', '경유지 많은 노선 내비', '정류장 30곳 넘어도 순서대로 안내'), ('/life/midpoint.html', '중간지점 찾기', '친구들과 만날 곳 추천 + 공유 카드'), ('/life/taxi-fare.html', '택시비·통행료·기름값 계산기', '택시 vs 내 차 비용 비교')]

CSS = '''
.bs-st{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:14px;background:#F4F7FB;margin-top:12px;font-weight:700;color:var(--head);font-size:15px;line-height:1.45}
.bs-st i{flex:none;width:12px;height:12px;border-radius:50%;background:#B0B8C1}
.bs-st.on{background:#E8F3FF}.bs-st.on i{background:#16A34A;box-shadow:0 0 0 0 rgba(22,163,74,.5);animation:bsp 1.6s infinite}
.bs-st.warn{background:#FFF4E5}.bs-st.warn i{background:#F59E0B}.bs-st.end{background:#F2F4F6;color:var(--muted)}
@keyframes bsp{70%{box-shadow:0 0 0 10px rgba(22,163,74,0)}100%{box-shadow:0 0 0 0 rgba(22,163,74,0)}}
@media (prefers-reduced-motion:reduce){.bs-st.on i{animation:none}}
.bs-st small{display:block;font-weight:500;color:var(--muted);font-size:13px}
.bs-row{display:grid;grid-template-columns:1fr auto;gap:8px;margin-top:12px;align-items:end}
.bs-row label{display:flex;flex-direction:column;gap:5px;font-size:13.5px;font-weight:700;color:var(--head);min-width:0}
.bs-row select,.bs-row input{font:inherit;font-size:16px;padding:9px 10px;border:1px solid var(--line-s);border-radius:10px;min-height:46px;width:100%;box-sizing:border-box;background:#fff;min-width:0}
.bs-btn{font:inherit;font-size:14.5px;font-weight:700;border:1px solid var(--line-s);background:#fff;border-radius:10px;min-height:46px;padding:0 14px;cursor:pointer;white-space:nowrap;color:var(--head);text-decoration:none;display:inline-flex;align-items:center;justify-content:center}
.bs-go{display:block;width:100%;margin-top:14px;min-height:56px;border:0;border-radius:14px;background:#16A34A;color:#fff;font:inherit;font-size:18px;font-weight:800;cursor:pointer}
.bs-go.stop{background:#F04452}.bs-go:disabled{background:#B0B8C1;cursor:default}
.bs-link{margin-top:14px;padding:14px;border:1px dashed var(--line-s);border-radius:14px}
.bs-link p{margin:0 0 8px;font-size:13.5px;color:var(--muted)}
.bs-link code{display:block;font-size:14px;word-break:break-all;background:#F4F7FB;border-radius:8px;padding:10px;color:var(--head)}
.bs-acts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:10px}
.bs-acts .bs-btn{padding:0 6px;font-size:14px}
.bs-note{font-size:13.5px;line-height:1.6;color:var(--muted);margin:10px 0 0}
.bs-stops{list-style:none;margin:12px 0 0;padding:0;counter-reset:s}
.bs-stops li{display:grid;grid-template-columns:30px 1fr auto;gap:10px;align-items:center;padding:10px 4px;border-top:1px solid var(--line-s)}
.bs-stops li:first-child{border-top:0}
.bs-stops .no{width:28px;height:28px;border-radius:50%;background:#E8F3FF;color:#1B64DA;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center}
.bs-stops .nm{font-weight:700;color:var(--head);font-size:15px;min-width:0;overflow-wrap:anywhere}
.bs-stops .et{font-weight:800;font-size:15px;color:#1B64DA;white-space:nowrap;font-variant-numeric:tabular-nums}
.bs-stops li.past .no{background:#F2F4F6;color:#B0B8C1}.bs-stops li.past .nm,.bs-stops li.past .et{color:#B0B8C1;font-weight:500}
.bs-stops li.next{background:#F0F7FF;border-radius:10px}
.bs-stops li.mine .nm::after{content:"내 정류장";margin-left:6px;font-size:11.5px;font-weight:800;color:#fff;background:#F59E0B;border-radius:6px;padding:2px 6px;vertical-align:2px;white-space:nowrap}
.bs-stops button{all:unset;cursor:pointer;display:contents}
.bs-mine{margin-top:12px;padding:16px;border-radius:16px;background:#1B64DA;color:#fff}
.bs-mine span{display:block;font-size:13.5px;opacity:.9}.bs-mine b{display:block;font-size:26px;line-height:1.3;margin-top:2px;word-break:keep-all}
.bus-ic{width:40px;height:40px;border-radius:50%;background:#F59E0B;border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;font-size:21px;line-height:1}
.stop-ic{min-width:22px;height:22px;border-radius:11px;background:#fff;border:2px solid #1B64DA;color:#1B64DA;font:800 11.5px/18px system-ui,sans-serif;text-align:center;padding:0 3px;box-sizing:border-box}
.stop-ic.past{border-color:#B0B8C1;color:#B0B8C1}.stop-ic.mine{background:#F59E0B;border-color:#F59E0B;color:#fff}
'''

COMMON = r'''
var API=(/^(localhost|127\.0\.0\.1)$/.test(location.hostname)&&new URLSearchParams(location.search).get('api'))||'%API%';
function dist(a,b,c,d){var R=6371000,x=(c-a)*Math.PI/180,y=(d-b)*Math.PI/180,s=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*Math.PI/180)*Math.cos(c*Math.PI/180)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(s))}
function ago(ms){var s=Math.max(0,Math.round(ms/1000));return s<60?s+'초 전':s<3600?Math.floor(s/60)+'분 전':Math.floor(s/3600)+'시간 전'}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
'''.replace('%API%', API)

# ───────── 기사용 ─────────
SH_MAIN = '''<section class="card tool"><h2>운행 위치 공유하기</h2>
<div class="bs-st" id="st"><i></i><div id="st-t">아직 공유하지 않고 있어요<small>노선을 고르고 아래 초록 버튼을 누르세요</small></div></div>
<div class="bs-row"><label>공유할 노선<select id="rsel"></select></label><a class="bs-btn" href="/life/route-navi.html">노선 편집</a></div>
<div class="bs-row"><label>승객에게 보일 이름<input id="bname" maxlength="30" placeholder="예: 송도복지관 A코스 셔틀"></label><span></span></div>
<button class="bs-go" id="go">위치 공유 시작</button>
<div class="bs-link" id="lk"><p>승객용 링크예요. 같은 노선은 매번 같은 링크라서 단톡방에 한 번만 올려 두면 돼요.</p><code id="url">–</code>
<div class="bs-acts"><button class="bs-btn" id="copy" type="button">링크 복사</button><button class="bs-btn" id="share" type="button">공유하기</button><a class="bs-btn" id="open" target="_blank" rel="noopener">승객 화면</a></div></div>
<p class="bs-note">공유하는 동안 화면을 켜 두세요. 화면이 꺼지거나 다른 앱으로 가면 휴대폰이 위치를 보내지 않을 수 있어요. 내비는 다른 휴대폰이나 차량 내비로 쓰는 게 가장 안정적이에요.</p>
</section>
<section class="card"><h2>이렇게 작동해요</h2><ul class="xp">
<li><b>기사님</b>이 이 페이지에서 시작을 누르면 휴대폰 위치가 20초쯤마다 올라가요. 차가 서 있으면 덜 자주 보내서 데이터를 거의 쓰지 않아요.</li>
<li><b>승객</b>은 링크만 열면 돼요. 앱 설치나 가입이 없어요. 지도에 버스 위치와 정류장별 도착 예상 시간이 나와요.</li>
<li><b>정류장 목록</b>은 <a href="/life/route-navi.html">노선 내비</a>에 저장한 노선을 그대로 써요. 정류장이 없으면 버스 위치만 보여 줘요.</li>
<li><b>운행 종료</b>를 누르면 승객 화면에 “운행 종료”가 뜨고, 위치는 10시간 뒤 서버에서 지워져요.</li></ul></section>
'''
SH_JS = '<script>\n' + COMMON + r'''
(function(){
var $=function(i){return document.getElementById(i)};
var NAV;try{NAV=JSON.parse(localStorage.getItem('hl-route-navi-v1'))}catch(e){}
if(!NAV||!NAV.routes)NAV={routes:{},cur:''};
var ST;try{ST=JSON.parse(localStorage.getItem('hl-bus-share-v1'))}catch(e){}if(!ST||!ST.r)ST={r:{}};
function save(){try{localStorage.setItem('hl-bus-share-v1',JSON.stringify(ST))}catch(e){}}
function rnd(n){var a=new Uint8Array(n),s='',c='abcdefghijkmnpqrstuvwxyz23456789';crypto.getRandomValues(a);for(var i=0;i<n;i++)s+=c[a[i]%c.length];return s}
var names=Object.keys(NAV.routes);if(!names.length)names=['내 셔틀'];
$('rsel').innerHTML=names.map(function(k){var n=(NAV.routes[k]||[]).length;return '<option value="'+esc(k)+'"'+(k==NAV.cur?' selected':'')+'>'+esc(k)+(n?' · 정류장 '+n+'곳':'')+'</option>'}).join('');
function cur(){var k=$('rsel').value,o=ST.r[k];if(!o){o=ST.r[k]={id:rnd(12),k:rnd(24),name:k};save()}return o}
function stops(){return (NAV.routes[$('rsel').value]||[]).map(function(p,i){return [p.lat,p.lng,(p.n||('정류장 '+(i+1))).slice(0,30)]})}
function link(){var o=cur(),u=location.origin+'/drive/bus.html?id='+o.id;$('url').textContent=u;$('open').href=u;$('bname').value=o.name||'';return u}
$('rsel').onchange=function(){if(on)return;link()};$('bname').oninput=function(){cur().name=this.value.slice(0,30);save()};link();
$('copy').onclick=function(){var u=link();(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){$('copy').textContent='복사됨'},function(){prompt('링크를 복사하세요',u)});setTimeout(function(){$('copy').textContent='링크 복사'},1800)};
$('share').onclick=function(){var u=link(),t=(cur().name||'셔틀')+' 지금 어디?';if(navigator.share)navigator.share({title:t,text:t+' 버스 위치를 실시간으로 볼 수 있어요.',url:u}).catch(function(){});else $('copy').onclick()};
var on=false,wid=null,lock=null,last=null,lastSent=0,ix=-1,pend=null,busy=false,okAt=0,fails=0,tick=null;
function status(cls,t,s){$('st').className='bs-st '+cls;$('st-t').innerHTML=esc(t)+(s?'<small>'+esc(s)+'</small>':'')}
function post(body){body.k=cur().k;return fetch(API+'/b/'+cur().id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){return r.json().then(function(j){if(!r.ok)throw new Error(j.err||r.status);return j})})}
function progress(lat,lng){var s=stops();for(var i=Math.max(0,ix);i<s.length;i++){if(dist(lat,lng,s[i][0],s[i][1])<90){ix=i;break}}}
function send(p,force){var c=p.coords,now=Date.now();
 var moved=!last||dist(last.lat,last.lng,c.latitude,c.longitude)>40;
 if(!force&&(now-lastSent<12000||(!moved&&now-lastSent<60000)))return;
 if(busy){pend=p;return}busy=true;progress(c.latitude,c.longitude);
 var b={lat:c.latitude,lng:c.longitude,ix:ix};if(c.speed!=null&&isFinite(c.speed))b.spd=Math.max(0,Math.min(60,c.speed));
 post(b).then(function(){last={lat:c.latitude,lng:c.longitude};lastSent=now;okAt=now;fails=0;show()},function(e){fails++;show(e.message)}).then(function(){busy=false;if(pend){var q=pend;pend=null;send(q)}})}
function show(err){if(!on)return;var s=stops();
 if(err&&fails>1)status('warn','위치를 보내지 못하고 있어요','인터넷 연결을 확인해 주세요 ('+err+')');
 else if(!okAt)status('warn','위치를 찾는 중…','GPS가 잡히면 바로 공유돼요');
 else status('on','위치 공유 중 · 마지막 전송 '+ago(Date.now()-okAt),s.length?(ix>=0?(ix+1)+'번 '+s[ix][2]+' 지남':'첫 정류장으로 가는 중')+' · 정류장 '+s.length+'곳':'정류장 없이 버스 위치만 공유 중')}
function wake(){if(navigator.wakeLock&&document.visibilityState=='visible')navigator.wakeLock.request('screen').then(function(l){lock=l},function(){})}
document.addEventListener('visibilitychange',function(){if(on&&document.visibilityState=='visible'){wake();if(last)lastSent=0}});
function start(){if(!navigator.geolocation){status('warn','이 브라우저는 위치를 지원하지 않아요');return}
 $('go').disabled=true;status('warn','시작하는 중…');var o=cur();ix=-1;
 post({start:1,name:(o.name||$('rsel').value).slice(0,40),stops:stops()}).then(function(){
  on=true;okAt=0;$('go').disabled=false;$('go').textContent='운행 종료';$('go').classList.add('stop');$('rsel').disabled=true;wake();show();
  wid=navigator.geolocation.watchPosition(function(p){send(p)},function(e){status('warn',e.code==1?'위치 권한이 꺼져 있어요':'위치를 잡지 못했어요',e.code==1?'브라우저 주소창의 자물쇠 → 위치 허용을 켜 주세요':'하늘이 보이는 곳에서 잠시 기다려 주세요')},{enableHighAccuracy:true,maximumAge:5000,timeout:30000});
  tick=setInterval(show,5000);if(window.gtag)gtag('event','bus_share_start')
 },function(e){$('go').disabled=false;status('warn','공유를 시작하지 못했어요','잠시 뒤 다시 눌러 주세요 ('+e.message+')')})}
function stop(){on=false;if(wid!=null)navigator.geolocation.clearWatch(wid);wid=null;clearInterval(tick);if(lock){lock.release().catch(function(){});lock=null}
 $('go').textContent='위치 공유 시작';$('go').classList.remove('stop');$('rsel').disabled=false;
 post({end:1}).then(function(){status('end','운행 종료했어요','승객 화면에 “운행 종료”로 보여요')},function(){status('warn','종료 신호를 보내지 못했어요','위치는 더 이상 보내지 않아요')})}
$('go').onclick=function(){on?(confirm('운행을 종료할까요?')&&stop()):start()};
window.addEventListener('beforeunload',function(e){if(on){e.preventDefault();e.returnValue=''}});
})();
</script>
'''
SH_FAQ = [
 ('승객도 앱을 깔아야 하나요?', '아니요. 기사님이 보낸 링크를 열기만 하면 돼요. 카카오톡 단톡방이나 문자로 보내면 되고, 가입도 필요 없어요.'),
 ('링크가 매번 바뀌나요?', '같은 휴대폰에서 같은 노선이면 링크가 그대로예요. 단톡방 공지에 한 번 올려 두고 매일 쓰면 돼요.'),
 ('데이터와 배터리는 얼마나 쓰나요?', '위치는 숫자 몇 개라서 하루 종일 공유해도 데이터는 1MB가 안 돼요. GPS와 화면을 켜 두니 배터리는 충전기를 꽂아 두는 걸 권해요.'),
 ('다른 사람이 제 위치를 바꿀 수 있나요?', '위치를 올릴 때 이 휴대폰에만 저장된 비밀 열쇠가 함께 가요. 링크를 아는 승객은 보기만 할 수 있어요.'),
 ('운행이 끝나면 위치가 남나요?', '운행 종료를 누르면 승객 화면에 종료로 표시되고, 마지막 위치도 10시간 뒤 자동으로 지워져요.'),
]

# ───────── 승객용 ─────────
BUS_MAIN = '''<section class="card tool">
<div class="bs-st" id="st"><i></i><div id="st-t">버스 위치를 불러오는 중…</div></div>
<div class="bs-mine" id="mine" hidden><span id="mine-l">내 정류장까지</span><b id="mine-t">–</b></div>
<div class="mp-wrap" style="margin-top:12px"><div id="map" role="application" aria-label="버스 위치 지도"></div><p class="mp-hint" id="mp-hint">지도를 불러오는 중…</p></div>
<div class="bs-row"><button class="bs-btn" id="fit" type="button">버스 위치로</button><button class="bs-btn" id="rf" type="button">새로고침</button></div>
<h2 style="margin-top:18px">정류장 도착 예상</h2>
<p class="bs-note" style="margin-top:0">정류장을 누르면 ‘내 정류장’으로 정해져서 위에 크게 보여요.</p>
<ol class="bs-stops" id="list"></ol>
<p class="bs-note">도착 시간은 버스 위치와 정류장 사이 거리로 계산한 대략적인 값이에요. 신호와 정체에 따라 몇 분 달라질 수 있어요.</p>
</section>
'''
BUS_JS = '<script>\n' + G.COMMON_JS + COMMON + r'''
(function(){
var $=function(i){return document.getElementById(i)},H=HLMAP;
var id=(new URLSearchParams(location.search).get('id')||'').toLowerCase();
var MK='hl-bus-mine-'+id,mine=-1;try{mine=+(localStorage.getItem(MK)||-1)}catch(e){}
var D=null,busOv=null,stopOv=[],line=null,fitted=false,timer=null,lastT=0;
function status(cls,t,s){$('st').className='bs-st '+cls;$('st-t').innerHTML=esc(t)+(s?'<small>'+esc(s)+'</small>':'')}
if(!/^[a-z0-9]{10,20}$/.test(id)){status('warn','링크가 올바르지 않아요','기사님께 받은 링크를 다시 열어 주세요');$('mp-hint').hidden=true;return}
function speed(){var v=D&&D.spd;return v&&v>3?Math.min(v,16):6.4}
function etas(){var s=D.stops||[],out=[],from=Math.max(0,(D.ix==null?-1:D.ix)+1),acc=0,pl=D.lat,pg=D.lng;
 for(var i=0;i<s.length;i++){if(i<from||pl==null){out.push(null);continue}acc+=dist(pl,pg,s[i][0],s[i][1])*1.35;pl=s[i][0];pg=s[i][1];out.push(acc/speed()+(i-from)*25)}return out}
function fmt(sec){if(sec==null)return '';var m=Math.round(sec/60);return m<1?'곧 도착':m>=60?Math.floor(m/60)+'시간 '+(m%60)+'분':'약 '+m+'분'}
function list(){var s=(D&&D.stops)||[],e=D&&!D.end?etas():[],ix=D&&D.ix!=null?D.ix:-1;
 if(!s.length){$('list').innerHTML='<li><span></span><span class="nm" style="font-weight:500;color:var(--muted)">기사님이 정류장을 등록하지 않았어요. 지도에서 버스 위치만 볼 수 있어요.</span><span></span></li>';$('mine').hidden=true;return}
 $('list').innerHTML=s.map(function(p,i){var cls=(i<=ix?'past':'')+(i==ix+1&&!D.end?' next':'')+(i==mine?' mine':'');
  return '<li class="'+cls+'"><button type="button" data-i="'+i+'" aria-label="'+esc(p[2])+' 내 정류장으로"><span class="no">'+(i+1)+'</span><span class="nm">'+esc(p[2])+'</span><span class="et">'+(i<=ix?'지남':D.end?'':fmt(e[i]))+'</span></button></li>'}).join('');
 if(mine>=0&&mine<s.length&&!D.end){$('mine').hidden=false;$('mine-l').textContent=(mine+1)+'. '+s[mine][2]+'까지';$('mine-t').textContent=mine<=ix?'버스가 이미 지나갔어요':fmt(e[mine])}else $('mine').hidden=true}
$('list').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var i=+b.dataset.i;mine=mine==i?-1:i;try{localStorage.setItem(MK,mine)}catch(x){}list();drawStops()});
function ov(lat,lng,html,z){return new H.K.CustomOverlay({map:H.map,position:new H.K.LatLng(lat,lng),content:html,yAnchor:.5,xAnchor:.5,zIndex:z||1})}
function drawStops(){if(!H.map||!D)return;stopOv.forEach(function(o){o.setMap(null)});stopOv=[];var s=D.stops||[],ix=D.ix!=null?D.ix:-1;
 s.forEach(function(p,i){stopOv.push(ov(p[0],p[1],'<div class="stop-ic'+(i<=ix?' past':'')+(i==mine?' mine':'')+'">'+(i+1)+'</div>',2))});
 if(line)line.setMap(null);if(s.length>1)line=new H.K.Polyline({map:H.map,path:s.map(function(p){return new H.K.LatLng(p[0],p[1])}),strokeWeight:4,strokeColor:'#1B64DA',strokeOpacity:.35,strokeStyle:'shortdash'})}
function drawBus(){if(!H.map||!D||D.lat==null)return;var pos=new H.K.LatLng(D.lat,D.lng);
 if(!busOv)busOv=ov(D.lat,D.lng,'<div class="bus-ic" aria-label="버스">🚌</div>',9);else busOv.setPosition(pos);
 if(!fitted){fitted=true;var b=new H.K.LatLngBounds();b.extend(pos);(D.stops||[]).forEach(function(p){b.extend(new H.K.LatLng(p[0],p[1]))});if((D.stops||[]).length)H.map.setBounds(b,40,40,40,40);else H.map.setCenter(pos)}}
function render(){var now=D.now||Date.now(),age=D.t?now-D.t:null;
 document.title=(D.name||'셔틀')+' 지금 어디? | 홍라이프 도구';
 if(D.end)status('end',(D.name||'셔틀')+' · 운행 종료','오늘 운행이 끝났어요. 다음 운행 때 이 링크를 다시 열면 돼요.');
 else if(age==null)status('warn',(D.name||'셔틀')+' · 출발 준비 중','기사님 휴대폰의 위치를 기다리고 있어요');
 else if(age>180000)status('warn',(D.name||'셔틀')+' · 위치 '+ago(age),'신호가 약하거나 잠시 멈췄을 수 있어요. 마지막 위치를 보여 줘요.');
 else status('on',(D.name||'셔틀')+' · 운행 중','위치 '+ago(age)+' 업데이트');
 list();if(H.map){drawStops();drawBus();$('mp-hint').hidden=true}}
function load(){fetch(API+'/b/'+id,{cache:'no-store'}).then(function(r){if(r.status==404)return {none:1};return r.json()}).then(function(j){
 if(j.none){D=null;status('warn','아직 운행 정보가 없어요','기사님이 위치 공유를 시작하면 자동으로 나타나요');$('list').innerHTML='';return}
 D=j;lastT=Date.now();render()}).catch(function(){status('warn','연결이 불안정해요','잠시 뒤 자동으로 다시 시도해요')})}
H.onReady(function(){H.init($('map'),37.39,126.65,7);$('mp-hint').textContent='버스 위치를 기다리는 중…';if(D)render()});
function loop(){clearTimeout(timer);load();timer=setTimeout(loop,document.visibilityState=='visible'?15000:60000)}
document.addEventListener('visibilitychange',function(){if(document.visibilityState=='visible')loop()});
setInterval(function(){if(D&&!D.end&&D.t){var a=Date.now()-lastT+(D.now-D.t);if(a<180000)$('st-t').querySelector('small')&&($('st-t').querySelector('small').textContent='위치 '+ago(a)+' 업데이트')}},5000);
$('rf').onclick=loop;$('fit').onclick=function(){if(D&&D.lat!=null&&H.map)H.map.panTo(new H.K.LatLng(D.lat,D.lng))};
loop();
})();
</script>
'''
BUS_FAQ = [
 ('도착 시간은 얼마나 정확한가요?', '버스 위치와 남은 정류장 사이 거리를 차가 다니는 평균 속도로 나눈 값이에요. 신호·정체·승하차 시간에 따라 몇 분 달라질 수 있어요.'),
 ('위치가 한동안 안 바뀌어요.', '버스가 정차 중이거나 기사님 휴대폰 신호가 약할 때 그래요. 3분 넘게 소식이 없으면 화면에 따로 알려 드려요.'),
 ('내 정류장은 어떻게 정하나요?', '정류장 목록에서 내가 타는 정류장을 누르세요. 이 휴대폰에 저장되고, 화면 위에 남은 시간이 크게 보여요.'),
]

def build():
    css = '<style id="hl-mt">' + G.COMMON_CSS + CSS + '</style>\n'
    G.shell('bus-share', '셔틀버스 위치 공유 (기사용) · 링크로 실시간 위치 보내기 | 홍라이프 도구',
            '셔틀·통학버스·학원차 기사님이 버튼 하나로 실시간 위치를 공유해요. 승객은 링크만 열면 버스 위치와 정류장별 도착 예상 시간을 볼 수 있어요. 앱 설치·가입 없음.',
            '셔틀버스 위치 공유 (기사용)',
            '기사님 휴대폰으로 버스 위치를 승객에게 실시간으로 보여 줘요. 링크 하나를 단톡방에 올려 두면 승객은 앱 없이 “버스 지금 어디?”를 바로 확인해요.',
            css, SH_MAIN, SH_JS, SH_FAQ, dirn='drive', rel=REL)
    G.shell('bus', '셔틀 지금 어디? 실시간 버스 위치 | 홍라이프 도구',
            '기사님이 공유한 셔틀버스의 실시간 위치와 정류장별 도착 예상 시간을 보여 줘요.',
            '셔틀 지금 어디?', '기사님이 공유한 버스 위치예요. 15초마다 자동으로 새로 고쳐져요.',
            css, BUS_MAIN, BUS_JS, BUS_FAQ, dirn='drive',
            rel=[('/drive/bus-share.html', '셔틀버스 위치 공유 (기사용)', '우리 버스도 위치 공유하기')] + REL[:1])
    p = os.path.join(G.ROOT, 'overlay/drive/bus.html'); h = open(p, encoding='utf-8').read()
    h = re.sub(r'<meta name="robots"[^>]*>', '', h).replace('<head>', '<head>\n<meta name="robots" content="noindex,follow">', 1)
    open(p, 'w', encoding='utf-8').write(h)

if __name__ == '__main__':
    build()
