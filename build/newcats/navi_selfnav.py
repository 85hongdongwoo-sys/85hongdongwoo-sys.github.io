# 자체 안내 모드 (30곳 이상 한 번에) — gen_navi.py 에서 import
HTML = r'''<div id="nav" class="nv" hidden role="dialog" aria-label="노선 길 안내">
 <div class="nv-top"><div class="nv-ic" id="nv-ic" aria-hidden="true"></div><div class="nv-tx"><p class="nv-d" id="nv-d">경로 준비 중…</p><p class="nv-r" id="nv-r"></p></div></div>
 <div id="nvmap"></div>
 <div class="nv-bot"><div class="nv-st"><p class="nv-k" id="nv-k"></p><p class="nv-s" id="nv-s"></p></div>
  <div class="nv-bt"><button type="button" id="nv-mute" aria-pressed="false">음성 켜짐</button><button type="button" id="nv-end">안내 끝</button></div></div>
 <p class="nv-sim" id="nv-simtag" hidden>모의 주행 중</p>
</div>'''
CSS = r'''
.nv{position:fixed;inset:0;z-index:10000;background:#111;display:flex;flex-direction:column}
.nv-top{display:flex;gap:12px;align-items:center;padding:calc(10px + env(safe-area-inset-top)) 14px 12px;background:#1B64DA;color:#fff;min-height:84px}
.nv-ic{flex:none;width:58px;height:58px;border-radius:14px;background:rgba(255,255,255,.16);display:grid;place-items:center}
.nv-ic svg{width:40px;height:40px}
.nv-tx{min-width:0}.nv-d{margin:0;font-size:30px;font-weight:800;line-height:1.1;letter-spacing:-.5px}.nv-r{margin:4px 0 0;font-size:16px;font-weight:600;opacity:.92;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#nvmap{flex:1;min-height:0;background:#E8EEF3}
.nv-bot{display:flex;gap:10px;align-items:center;justify-content:space-between;padding:12px 14px calc(12px + env(safe-area-inset-bottom));background:#fff}
.nv-st{min-width:0}.nv-k{margin:0;font-size:13px;font-weight:700;color:#F04452}.nv-s{margin:2px 0 0;font-size:17px;font-weight:800;color:#191F28;line-height:1.3;word-break:keep-all}
.nv-bt{display:flex;gap:6px;flex:none}.nv-bt button{min-height:46px;padding:0 12px;border-radius:12px;border:1px solid #E5E8EB;background:#F2F4F6;font-size:14px;font-weight:700;color:#333D4B;cursor:pointer}
#nv-end{background:#191F28;color:#fff;border-color:#191F28}
.nv-sim{position:absolute;left:50%;top:104px;transform:translateX(-50%);margin:0;background:#F59F00;color:#fff;font-size:13px;font-weight:800;padding:5px 12px;border-radius:99px;z-index:600}
.nv-car{width:34px;height:34px;display:grid;place-items:center}.nv-car svg{width:34px;height:34px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.35));transition:transform .4s}
.rn-self{display:flex!important;flex-direction:column;align-items:center;gap:3px;min-height:72px;width:100%;padding:12px 10px;text-align:center;background:#1B64DA!important;border-color:#1B64DA!important;color:#fff!important}.rn-self b{font-size:18px}.rn-self span{font-size:13.5px;font-weight:600;opacity:.92;word-break:keep-all}
.rn-sim{display:block;margin:8px auto 0;border:0;background:none;color:#1B64DA;font-size:14px;font-weight:700;text-decoration:underline;cursor:pointer}
@media(max-width:380px){.nv-d{font-size:26px}.nv-bt button{padding:0 9px;font-size:13px}}
'''
BTN = r'''<button type="button" class="btn rn-self" id="self-go"><b>전체 노선 한 번에 안내 (베타)</b><span id="self-s">정류장을 다 이어서 음성으로 안내해요</span></button>
  <button type="button" class="rn-sim" id="self-sim">운전하지 않고 모의 주행으로 미리 보기</button>
  <p class="rn-or">또는 내비 앱으로 넘기기</p>'''
JS = r'''<script>(function(){
var $=function(i){return document.getElementById(i)};
function store(){try{return JSON.parse(localStorage.getItem('hl-route-navi-v1'))}catch(e){return null}}
function stops(){var S=store();if(!S)return [];var r=S.routes[S.cur]||[],p=Math.min(S.pos[S.cur]||0,Math.max(r.length-1,0));return r.slice(p).map(function(s,k){return {lat:s.lat,lng:s.lng,n:s.n||('정류장 '+(p+k+1)),no:p+k+1}})}
function hv(a,b){var r=Math.PI/180,dl=(b[0]-a[0])*r,dg=(b[1]-a[1])*r,x=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dg/2)*Math.sin(dg/2);return 12742000*Math.asin(Math.sqrt(x))}
function brg(a,b){var r=Math.PI/180,y=Math.sin((b[1]-a[1])*r)*Math.cos(b[0]*r),x=Math.cos(a[0]*r)*Math.sin(b[0]*r)-Math.sin(a[0]*r)*Math.cos(b[0]*r)*Math.cos((b[1]-a[1])*r);return (Math.atan2(y,x)/r+360)%360}
var MOD={'left':'좌회전','right':'우회전','slight left':'왼쪽 방향','slight right':'오른쪽 방향','sharp left':'급좌회전','sharp right':'급우회전','uturn':'유턴','straight':'직진'};
function say(st){var t=st.maneuver.type,m=st.maneuver.modifier||'straight';
 if(t=='roundabout'||t=='rotary')return '회전교차로 '+(st.maneuver.exit||1)+'번째 출구';
 if(t=='on ramp')return (m.indexOf('left')>=0?'왼쪽':'오른쪽')+' 진입로';
 if(t=='off ramp')return (m.indexOf('left')>=0?'왼쪽':'오른쪽')+' 출구';
 if(t=='fork')return (m.indexOf('left')>=0?'왼쪽':'오른쪽')+' 길';
 if(t=='merge')return '합류';
 return MOD[m]||'직진'}
function icon(st){var m=st?st.maneuver.modifier||'straight':'straight',t=st?st.maneuver.type:'',rot={'left':-90,'sharp left':-135,'slight left':-45,'right':90,'sharp right':135,'slight right':45,'straight':0}[m];
 if(t=='roundabout'||t=='rotary')return '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><path d="M12 22v-5M17 12h5"/></svg>';
 if(m=='uturn')return '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21V9a4 4 0 0 1 8 0v4"/><path d="M13 11l3 3 3-3"/></svg>';
 return '<svg viewBox="0 0 24 24" style="transform:rotate('+(rot||0)+'deg)" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21V4"/><path d="M5 11l7-7 7 7"/></svg>'}
function fmt(m){return m>=1000?(m/1000).toFixed(1)+'km':(Math.round(m/10)*10)+'m'}
var voice=true,ko=null;function speak(t){if(!voice||!window.speechSynthesis)return;var u=new SpeechSynthesisUtterance(t);u.lang='ko-KR';u.rate=1.05;if(ko)u.voice=ko;speechSynthesis.cancel();speechSynthesis.speak(u)}
if(window.speechSynthesis){var lv=function(){ko=speechSynthesis.getVoices().filter(function(v){return /ko/i.test(v.lang)})[0]||null};lv();speechSynthesis.onvoiceschanged=lv}
var N=null;
function route(from,list){var pts=(from?[from]:[]).concat(list.map(function(s){return [s.lat,s.lng]}));
 var url='https://router.project-osrm.org/route/v1/driving/'+pts.map(function(p){return p[1].toFixed(6)+','+p[0].toFixed(6)}).join(';')+'?overview=full&geometries=geojson&steps=true';
 return fetch(url).then(function(r){return r.json()}).then(function(j){if(!j.routes||!j.routes.length)throw new Error('no route');var R0=j.routes[0];
  var co=R0.geometry.coordinates.map(function(c){return [c[1],c[0]]}),cum=[0];for(var i=1;i<co.length;i++)cum.push(cum[i-1]+hv(co[i-1],co[i]));
  var steps=[];R0.legs.forEach(function(l,li){l.steps.forEach(function(s){if(s.maneuver.type=='depart'||s.maneuver.type=='arrive')return;steps.push({st:s,p:[s.maneuver.location[1],s.maneuver.location[0]],leg:li})})});
  steps.forEach(function(s){var b=0,bd=1e12;for(var i=0;i<co.length;i++){var d=hv(co[i],s.p);if(d<bd){bd=d;b=i}}s.ci=b});
  return {co:co,cum:cum,steps:steps,spd:R0.distance/Math.max(R0.duration,1)}})}
function nearest(co,p,from){var b=from||0,bd=1e12,lim=Math.min(co.length,(from||0)+400);for(var i=Math.max(0,(from||0)-20);i<lim;i++){var d=hv(co[i],p);if(d<bd){bd=d;b=i}}return {i:b,d:bd}}
function start(sim){var st=stops();if(st.length<1){alert('먼저 정류장을 찍어 주세요');return}
 $('nav').hidden=false;document.documentElement.style.overflow='hidden';$('nv-simtag').hidden=!sim;
 if(!N||!N.map){var m=L.map('nvmap',{zoomControl:false,attributionControl:true}).setView([st[0].lat,st[0].lng],16);L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap'}).addTo(m);N={map:m}}
 setTimeout(function(){N.map.invalidateSize()},50);
 N.stops=st;N.si=0;N.k=0;N.ci=0;N.off=0;N.said={};N.sim=sim;N.busy=false;
 if(N.lay)N.lay.remove();N.lay=L.layerGroup().addTo(N.map);
 st.forEach(function(s){L.marker([s.lat,s.lng],{icon:L.divIcon({className:'',html:'<div class="rn-pin"><b>'+s.no+'</b></div>',iconSize:[30,30],iconAnchor:[4,30]})}).addTo(N.lay)});
 N.car=L.marker([st[0].lat,st[0].lng],{icon:L.divIcon({className:'nv-car',html:'<svg viewBox="0 0 24 24"><path d="M12 2l7 19-7-4-7 4z" fill="#1B64DA" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>',iconSize:[34,34],iconAnchor:[17,17]}),zIndexOffset:1000}).addTo(N.map);
 try{if(navigator.wakeLock)navigator.wakeLock.request('screen').then(function(w){N.wl=w}).catch(function(){})}catch(e){}
 $('nv-d').textContent='경로 준비 중…';$('nv-r').textContent='';
 var go=function(from){route(from,N.stops).then(function(r){N.r=r;N.k=0;N.ci=0;
   if(N.done)N.done.remove();N.done=L.polyline([],{color:'#9AA4B1',weight:7,opacity:.7}).addTo(N.lay);if(N.todo)N.todo.remove();N.todo=L.polyline(r.co,{color:'#1B64DA',weight:7,opacity:.85}).addTo(N.lay);
   if(sim)simrun();else watch();speak('안내를 시작합니다. 첫 정류장은 '+N.stops[0].n+'입니다.')}).catch(function(){$('nv-d').textContent='경로를 못 찾았어요';$('nv-r').textContent='인터넷 연결을 확인하거나 잠시 뒤 다시 시도해 주세요'})};
 if(sim)go(null);else navigator.geolocation.getCurrentPosition(function(g){go([g.coords.latitude,g.coords.longitude])},function(){go(null)},{enableHighAccuracy:true,timeout:8000});
}
function reroute(p){if(N.busy)return;N.busy=true;$('nv-r').textContent='경로를 다시 찾는 중…';speak('경로를 다시 탐색합니다');
 route(p,N.stops.slice(N.si)).then(function(r){N.r=r;N.k=0;N.ci=0;N.off=0;N.said={};N.todo.setLatLngs(r.co);N.busy=false}).catch(function(){N.busy=false})}
function onPos(p,hd){if(!N||!N.r)return;var r=N.r,nb=nearest(r.co,p,N.ci);
 if(nb.d>70&&!N.sim){if(++N.off>=3){reroute(p);return}}else N.off=0;
 if(nb.i>N.ci)N.ci=nb.i;
 var h=hd;if(h==null||isNaN(h)){var nx=r.co[Math.min(N.ci+3,r.co.length-1)];h=brg(p,nx)}
 N.car.setLatLng(p);var el=N.car.getElement();if(el)el.querySelector('svg').style.transform='rotate('+h+'deg)';
 N.map.setView(p,Math.max(N.map.getZoom()<15?17:N.map.getZoom(),15),{animate:true});
 N.done.setLatLngs(r.co.slice(0,N.ci+1).concat([p]));
 // 정류장 도착
 var s=N.stops[N.si];if(s&&hv(p,[s.lat,s.lng])<45){speak(s.no+'번 '+s.n+'에 도착했습니다.'+(N.stops[N.si+1]?' 다음은 '+N.stops[N.si+1].n+'입니다.':' 마지막 정류장입니다. 수고하셨습니다.'));sync(s.no);N.si++;
  if(N.si>=N.stops.length){$('nv-d').textContent='운행 끝';$('nv-r').textContent='모든 정류장을 돌았어요';$('nv-ic').innerHTML=icon(null);stopWatch();return}}
 // 다음 회전
 while(N.k<r.steps.length&&r.steps[N.k].ci<=N.ci)N.k++;
 var nx=r.steps[N.k],ns=N.stops[N.si];
 if(nx){var dm=r.cum[nx.ci]-r.cum[N.ci];$('nv-ic').innerHTML=icon(nx.st);$('nv-d').textContent=fmt(dm);$('nv-r').textContent=say(nx.st)+(nx.st.name?' · '+nx.st.name:'');
  var key=N.k;if(dm<320&&dm>150&&!N.said[key+'a']){N.said[key+'a']=1;speak(fmt(dm).replace('m','미터').replace('km','킬로미터')+' 앞에서 '+say(nx.st)+'입니다')}
  if(dm<60&&!N.said[key+'b']){N.said[key+'b']=1;speak(say(nx.st))}}
 else{$('nv-ic').innerHTML=icon(null);$('nv-d').textContent=ns?fmt(hv(p,[ns.lat,ns.lng])):'';$('nv-r').textContent='도로를 따라 직진'}
 if(ns){var sd=hv(p,[ns.lat,ns.lng]);$('nv-k').textContent='다음 정류장 '+ns.no+'번 · 남은 '+(N.stops.length-N.si)+'곳';$('nv-s').textContent=ns.n+' · '+fmt(sd)+' · 약 '+Math.max(1,Math.round(sd*1.3/r.spd/60))+'분';
  if(sd<300&&sd>120&&!N.said['s'+N.si]){N.said['s'+N.si]=1;speak('곧 '+ns.no+'번 '+ns.n+'입니다')}}}
function sync(no){var S=store();if(!S)return;S.pos[S.cur]=Math.min(no,(S.routes[S.cur]||[]).length-1);if(no>=(S.routes[S.cur]||[]).length)S.pos[S.cur]=0;try{localStorage.setItem('hl-route-navi-v1',JSON.stringify(S))}catch(e){}}
function watch(){stopWatch();N.w=navigator.geolocation.watchPosition(function(g){onPos([g.coords.latitude,g.coords.longitude],g.coords.heading)},function(){$('nv-r').textContent='위치를 받을 수 없어요. 위치 권한을 확인해 주세요'},{enableHighAccuracy:true,maximumAge:1000,timeout:15000})}
function simrun(){stopWatch();var co=N.r.co,cum=N.r.cum,t=0,v=16;N.t=setInterval(function(){t+=v*1.0;var i=0;while(i<cum.length-1&&cum[i+1]<t)i++;if(i>=cum.length-1){onPos(co[co.length-1]);stopWatch();return}
  var f=(t-cum[i])/Math.max(cum[i+1]-cum[i],.01),p=[co[i][0]+(co[i+1][0]-co[i][0])*f,co[i][1]+(co[i+1][1]-co[i][1])*f];onPos(p,brg(co[i],co[i+1]))},250)}
function stopWatch(){if(N&&N.w!=null){navigator.geolocation.clearWatch(N.w);N.w=null}if(N&&N.t){clearInterval(N.t);N.t=null}}
function end(){stopWatch();if(N&&N.wl){N.wl.release().catch(function(){});N.wl=null}if(window.speechSynthesis)speechSynthesis.cancel();$('nav').hidden=true;document.documentElement.style.overflow='';if(window.__rnRefresh)window.__rnRefresh()}
$('nv-end').onclick=end;
$('nv-mute').onclick=function(){voice=!voice;this.textContent=voice?'음성 켜짐':'음성 꺼짐';this.setAttribute('aria-pressed',!voice);if(!voice&&window.speechSynthesis)speechSynthesis.cancel()};
$('self-go').onclick=function(){if(!navigator.geolocation){alert('이 기기에서는 위치를 쓸 수 없어요');return}speak('');start(false)};
$('self-sim').onclick=function(){speak('');start(true)};
document.addEventListener('visibilitychange',function(){if(!document.hidden&&N&&N.wl===null&&!$('nav').hidden&&navigator.wakeLock)navigator.wakeLock.request('screen').then(function(w){N.wl=w}).catch(function(){})});
window.__selfnav={onPos:onPos,start:start};
})();</script>'''
