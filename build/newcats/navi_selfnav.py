# 자체 안내 모드 (30곳 이상 한 번에) — gen_navi.py 에서 import
HTML = r'''<div id="nav" class="nv" hidden role="dialog" aria-label="노선 길 안내">
 <div class="nv-top"><div class="nv-ic" id="nv-ic" aria-hidden="true"></div><div class="nv-tx"><p class="nv-d" id="nv-d">경로 준비 중…</p><p class="nv-r" id="nv-r"></p></div></div>
 <div id="nvmap"></div>
 <div class="nv-bot"><div class="nv-st"><p class="nv-k" id="nv-k"></p><p class="nv-s" id="nv-s"></p></div>
  <div class="nv-bt"><button type="button" id="nv-mute" aria-pressed="false">음성 켜짐</button><button type="button" id="nv-end">안내 끝</button></div></div>
 <p class="nv-sim" id="nv-simtag" hidden>모의 주행 중</p>
 <div class="nv-meter"><div class="nv-lim" id="nv-lim" hidden><b id="nv-limv">50</b></div><div class="nv-spd" id="nv-spd"><b id="nv-v">0</b><small>km/h</small></div></div>
 <p class="nv-cam" id="nv-cam" hidden></p>
</div>'''
CSS = r'''
.rn-opt{margin:0 0 14px;padding:14px;border-radius:14px;background:#fff;border:1px solid var(--line)}.rn-opt-h{margin:0 0 8px;font-size:14px;font-weight:800;color:var(--head)}
.rn-seg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px;background:#F2F4F6;border-radius:12px;padding:4px}.rn-seg button{border:0;background:none;min-height:40px;border-radius:9px;font-size:14px;font-weight:700;color:var(--muted);cursor:pointer;white-space:nowrap}.rn-seg button[aria-checked=true]{background:#fff;color:var(--head);box-shadow:0 1px 4px rgba(0,0,0,.08)}
.rn-chk{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;margin-top:10px}.rn-chk .hw{grid-column:1/-1;font-weight:700}.rn-chk input:disabled+*,.rn-chk label:has(input:disabled){opacity:.45}
.rn-chk label{display:flex;align-items:center;gap:6px;font-size:14px;color:var(--head);min-width:0;word-break:keep-all}.rn-chk input{width:18px;height:18px;flex:none;accent-color:#1B64DA}
.rn-vo{margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}.rn-vrow{display:flex;gap:6px}.rn-vrow select{flex:1;min-width:0;height:42px;border:1px solid var(--line);border-radius:10px;padding:0 10px;font-size:14px;background:#fff;color:var(--head)}.rn-vrow button{flex:none;height:42px;padding:0 14px;border-radius:10px;border:1px solid #1B64DA;background:#fff;color:#1B64DA;font-weight:700;font-size:14px;cursor:pointer}
.rn-rate{display:grid;grid-template-columns:52px 1fr 40px;align-items:center;gap:8px;margin-top:8px;font-size:14px;color:var(--head)}.rn-rate input{width:100%;accent-color:#1B64DA}.rn-rate output{font-size:13px;color:var(--muted);text-align:right}
.rn-opt-n{margin:10px 0 0;font-size:12.5px;color:var(--muted);line-height:1.5;word-break:keep-all}
@media(max-width:380px){.rn-chk{grid-template-columns:1fr}}
.nv{position:fixed;inset:0;z-index:10000;background:#111;display:flex;flex-direction:column}
@media(min-width:560px){.nv{left:50%;right:auto;width:440px;transform:translateX(-50%);box-shadow:0 0 0 100vmax rgba(17,17,17,.82)}}
@media(orientation:landscape) and (max-height:500px){.nv-top{min-height:64px;padding-top:8px;padding-bottom:8px}.nv-d{font-size:24px}.nv-ic{width:46px;height:46px}}
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
.nv-meter{position:absolute;right:12px;top:100px;z-index:600;display:flex;flex-direction:column;align-items:center;gap:8px}
.nv-lim{width:58px;height:58px;border-radius:50%;background:#fff;border:6px solid #E03131;display:grid;place-items:center;box-shadow:0 2px 8px rgba(0,0,0,.25)}.nv-lim b{font-size:22px;font-weight:900;color:#191F28;letter-spacing:-1px}
.nv-spd{min-width:58px;padding:6px 6px 4px;border-radius:14px;background:rgba(25,31,40,.88);color:#fff;text-align:center;line-height:1}.nv-spd b{display:block;font-size:22px;font-weight:800}.nv-spd small{font-size:10.5px;opacity:.8}.nv-spd.over{background:#E03131}
.nv-cam{position:absolute;left:12px;right:84px;top:100px;z-index:600;margin:0;padding:10px 12px;border-radius:12px;background:rgba(224,49,49,.94);color:#fff;font-size:15px;font-weight:800;line-height:1.35;word-break:keep-all}
.nv-car{width:34px;height:34px;display:grid;place-items:center}.nv-car svg{width:34px;height:34px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.35));transition:transform .4s}
.rn-self{position:relative;display:flex!important;flex-direction:row;align-items:center;justify-content:center;gap:14px;min-height:84px;width:100%;padding:14px 18px;text-align:left;white-space:normal;border:0!important;border-radius:22px!important;color:#fff!important;cursor:pointer;
 background:linear-gradient(180deg,#4C95FF 0%,#2471F0 48%,#1658D6 100%)!important;
 box-shadow:inset 0 1px 0 rgba(255,255,255,.45),inset 0 -2px 0 rgba(0,0,0,.12),0 10px 22px -6px rgba(22,88,214,.55),0 2px 4px rgba(22,88,214,.25);transition:transform .12s ease,box-shadow .12s ease}
.rn-self::before{content:"";position:absolute;inset:1px 1px 50% 1px;border-radius:21px 21px 40% 40%/21px 21px 14px 14px;background:linear-gradient(180deg,rgba(255,255,255,.28),rgba(255,255,255,0));pointer-events:none}
.rn-self:active{transform:scale(.98);box-shadow:inset 0 1px 0 rgba(255,255,255,.3),0 4px 10px -4px rgba(22,88,214,.6)}
.rn-self .pl{flex:none;width:52px;height:52px;border-radius:50%;display:grid;place-items:center;background:#fff;box-shadow:0 3px 8px rgba(0,0,0,.18),inset 0 -2px 0 rgba(0,0,0,.06)}
.rn-self .pl svg{width:22px;height:22px;margin-left:3px;fill:#1C64F2}
.rn-self .tx{display:flex;flex-direction:column;gap:2px;min-width:0;flex:1;white-space:normal}.rn-self b{font-size:24px;font-weight:800;letter-spacing:-.02em;line-height:1.1;text-shadow:0 1px 1px rgba(0,0,0,.15)}.rn-self span{font-size:13.5px;font-weight:600;opacity:.92;word-break:keep-all;line-height:1.35}
.rn-sim{display:block;margin:10px auto 0;border:0;background:none;color:#4E5968;font-size:14px;font-weight:600;text-decoration:underline;text-underline-offset:3px;cursor:pointer}
@media(max-width:380px){.nv-d{font-size:26px}.nv-bt button{padding:0 9px;font-size:13px}}
'''
BTN = r'''<div class="rn-opt"><p class="rn-opt-h">경로 설정</p><p class="rn-opt-n" style="margin:0 0 8px">기본은 카카오 추천 경로(실시간 교통 반영)예요. 필요한 것만 체크하세요.</p>
<div class="rn-chk"><label class="hw"><input type="checkbox" id="hwy">고속도로·큰길 위주로</label><label><input type="checkbox" data-av="uturn">유턴 피하기</label><label><input type="checkbox" data-av="schoolzone">어린이보호구역 피하기</label><label><input type="checkbox" data-av="toll">유료도로 피하기</label><label><input type="checkbox" data-av="motorway">자동차전용도로 피하기</label></div>
<div class="rn-vo"><p class="rn-opt-h">안내 목소리</p><div class="rn-vrow"><select id="vsel" aria-label="목소리 고르기"></select><button type="button" id="vtry">들어보기</button></div><label class="rn-rate">빠르기 <input type="range" id="vrate" min="0.8" max="1.4" step="0.05"><output id="vrv"></output></label><label class="rn-rate">높낮이 <input type="range" id="vpitch" min="0.6" max="1.4" step="0.05"><output id="vpv"></output></label><p class="rn-opt-n">목소리는 휴대폰에 깔린 음성 엔진을 써요. 원하는 목소리가 목록에 없으면 휴대폰 설정 → 텍스트 음성 변환(TTS)에서 한국어 음성을 더 내려받을 수 있어요.</p></div>
<p class="rn-opt-n">차량 높이·무게 제한은 카카오 길찾기에서 아직 고를 수 없어요. 낮은 굴다리 같은 곳은 통과할 길 위에 정류장 핀을 하나 더 찍어 경로를 고정해 주세요.</p></div>
<button type="button" class="btn rn-self" id="self-go"><i class="pl" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12-7.5a1 1 0 0 0 0-1.72l-12-7.5A1 1 0 0 0 7 4.5z"/></svg></i><span class="tx"><b>스타트</b><span id="self-s">전체 노선을 이어서 음성으로 안내해요</span></span></button>
  <button type="button" class="rn-sim" id="self-sim">안내 화면 미리 보기 (모의 주행)</button>
  <p class="rn-or">다른 지도 앱으로 안내받기</p>'''
JS = r'''<script>HM.ready(function(){
var $=function(i){return document.getElementById(i)};
function store(){try{return JSON.parse(localStorage.getItem('hl-route-navi-v1'))}catch(e){return null}}
function stops(){var S=store();if(!S)return [];var r=S.routes[S.cur]||[],p=Math.min(S.pos[S.cur]||0,Math.max(r.length-1,0));return r.slice(p).map(function(s,k){return {lat:s.lat,lng:s.lng,n:s.n||('정류장 '+(p+k+1)),no:p+k+1}})}
function hv(a,b){var r=Math.PI/180,dl=(b[0]-a[0])*r,dg=(b[1]-a[1])*r,x=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dg/2)*Math.sin(dg/2);return 12742000*Math.asin(Math.sqrt(x))}
function brg(a,b){var r=Math.PI/180,y=Math.sin((b[1]-a[1])*r)*Math.cos(b[0]*r),x=Math.cos(a[0]*r)*Math.sin(b[0]*r)-Math.sin(a[0]*r)*Math.cos(b[0]*r)*Math.cos((b[1]-a[1])*r);return (Math.atan2(y,x)/r+360)%360}
function icon(st){var m=st?st.mod:'straight',rot={'left':-90,'sharp left':-135,'slight left':-45,'right':90,'sharp right':135,'slight right':45,'straight':0}[m];
 if(m=='round')return '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><path d="M12 22v-5M17 12h5"/></svg>';
 if(m=='uturn')return '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21V9a4 4 0 0 1 8 0v4"/><path d="M13 11l3 3 3-3"/></svg>';
 return '<svg viewBox="0 0 24 24" style="transform:rotate('+(rot||0)+'deg)" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21V4"/><path d="M5 11l7-7 7 7"/></svg>'}
function say(st){return st.text}
function fmt(m){return m>=1000?(m/1000).toFixed(1)+'km':(Math.round(m/10)*10)+'m'}
var voice=true,KV=[];function vopt(){var S=store()||{};return S.voice||{}}
function pick(){var o=vopt();return KV.filter(function(v){return v.name==o.name})[0]||KV.filter(function(v){return v.localService!==false})[0]||KV[0]||null}
var CL={ok:null,a:null,q:[],base:'/assets/voice/ko/'};
fetch(CL.base+'try.mp3',{method:'HEAD'}).then(function(r){CL.ok=r.ok;if(r.ok)vlist()}).catch(function(){CL.ok=false});
function useClips(){return CL.ok&&(vopt().name||'__hl')=='__hl'}
function playNext(){if(!CL.q.length){CL.busy=false;return}CL.busy=true;var k=CL.q.shift();if(!CL.a){CL.a=new Audio()}var o=vopt();CL.a.src=CL.base+k+'.mp3';CL.a.playbackRate=o.rate?Math.max(.8,Math.min(1.4,o.rate/1.05)):1;CL.a.onended=CL.a.onerror=function(){setTimeout(playNext,120)};CL.a.play().catch(function(){CL.busy=false;CL.q=[]})}
function say2(keys,text,urgent){if(!voice)return;if(useClips()){if(urgent){CL.q=[];if(CL.a)CL.a.pause();CL.busy=false}CL.q=CL.q.concat(keys);if(!CL.busy)playNext()}else speak(text,urgent)}
function mk(m){return String(m||'straight').replace(/ /g,'_')}
function dk(dm){var B=[100,150,200,250,300,400,500,600,700,800,1000],b=B[0];B.forEach(function(x){if(Math.abs(x-dm)<Math.abs(b-dm))b=x});return b}
var LAST='';function speak(t,urgent){if(!voice||!window.speechSynthesis||!t)return;if(t==LAST&&speechSynthesis.speaking)return;LAST=t;var o=vopt(),u=new SpeechSynthesisUtterance(t);u.lang='ko-KR';u.rate=o.rate||1.05;u.pitch=o.pitch||1;var v=pick();if(v)u.voice=v;
 if(urgent||speechSynthesis.pending)speechSynthesis.cancel();speechSynthesis.resume();speechSynthesis.speak(u)}
setInterval(function(){if(window.speechSynthesis&&speechSynthesis.speaking&&!speechSynthesis.paused){speechSynthesis.pause();speechSynthesis.resume()}},10000);
function vput(k,val){var S=store();if(!S)return;S.voice=S.voice||{};S.voice[k]=val;try{localStorage.setItem('hl-route-navi-v1',JSON.stringify(S))}catch(e){}}
function vlist(){if(!window.speechSynthesis)return;KV=speechSynthesis.getVoices().filter(function(v){return /^ko/i.test(v.lang)});var sel=$('vsel'),o=vopt();
 if(!KV.length&&!CL.ok){sel.innerHTML='<option>이 기기에 한국어 목소리가 없어요</option>';return}
 sel.innerHTML=(CL.ok?'<option value="__hl"'+((o.name||'__hl')=='__hl'?' selected':'')+'>홍라이프 목소리 (권장 · 끊김 없음)</option>':'')+KV.map(function(v,i){var nm=v.name.replace(/Microsoft |Google |Samsung |\(.*?\)|Korean|한국어|ko[-_]KR/gi,'').replace(/\s+/g,' ').trim();return '<option value="'+v.name.replace(/"/g,'&quot;')+'"'+(v===pick()&&o.name&&o.name!='__hl'?' selected':'')+'>'+(i+1)+'. '+(nm||'기본 목소리')+(v.localService===false?' (온라인 · 끊길 수 있음)':' (휴대폰 안)')+'</option>'}).join('')}
if(window.speechSynthesis){vlist();speechSynthesis.onvoiceschanged=vlist}
(function(){var o=vopt();$('vrate').value=o.rate||1.05;$('vpitch').value=o.pitch||1;var show=function(){$('vrv').textContent=(+$('vrate').value).toFixed(2);$('vpv').textContent=(+$('vpitch').value).toFixed(2)};show();
 $('vsel').onchange=function(){vput('name',this.value);say2(['d300-right'],'300미터 앞에서 우회전입니다')};
 $('vrate').oninput=function(){vput('rate',+this.value);show()};$('vpitch').oninput=function(){vput('pitch',+this.value);show()};
 $('vrate').onchange=$('vpitch').onchange=function(){say2(['soon-3'],'곧 3번 정류장입니다')};
 $('vtry').onclick=function(){say2(['try'],'안내를 시작합니다. 300미터 앞에서 송도컨벤시아 방면으로 좌회전입니다')}})();
var N=null;
function route(from,list){var S0=store()||{};return HM.route((from?[from]:[]).concat(list.map(function(s){return [s.lat,s.lng]})),S0.opt||{pr:'RECOMMEND',av:['uturn']})}
// 경로 위로 맞추기(맵 매칭): 가까운 선분에 수직으로 내려 진행 거리(s)를 정확히 구한다
function proj(r,p,from,to){var co=r.co,best=null,c=Math.cos(p[0]*Math.PI/180),M=111320;
 for(var i=Math.max(0,from);i<Math.min(co.length-1,to);i++){var a=co[i],b=co[i+1],ax=(a[1]-p[1])*c*M,ay=(a[0]-p[0])*M,bx=(b[1]-p[1])*c*M,by=(b[0]-p[0])*M,dx=bx-ax,dy=by-ay,L=dx*dx+dy*dy,t=L?Math.max(0,Math.min(1,-(ax*dx+ay*dy)/L)):0,x=ax+dx*t,y=ay+dy*t,d=Math.sqrt(x*x+y*y);
  if(!best||d<best.d-0.5)best={i:i,t:t,d:d,s:r.cum[i]+(r.cum[i+1]-r.cum[i])*t,q:[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]}}return best}
function prep(r){var k=0;r.ss=N.stops.slice(N.si).map(function(st){var b=proj(r,[st.lat,st.lng],k,r.co.length);k=Math.max(0,b.i-2);return b.s});return r}
var CAMC={};function loadCams(r){var ks={};for(var i=0;i<r.co.length;i+=3){ks[Math.floor(r.co[i][0]*10)+'_'+Math.floor(r.co[i][1]*10)]=1}
 r.cams=[];return Promise.all(Object.keys(ks).map(function(k){return CAMC[k]?Promise.resolve(CAMC[k]):fetch('/assets/cam/'+k+'.json').then(function(x){return x.ok?x.json():[]}).catch(function(){return []}).then(function(a){CAMC[k]=a;return a})})).then(function(all){
  all.forEach(function(a){a.forEach(function(c){var b=0,bd=1e12;for(var i=0;i<r.co.length;i++){var d=Math.abs(r.co[i][0]-c[0])+Math.abs(r.co[i][1]-c[1]);if(d<bd){bd=d;b=i}}if(bd>0.003)return;var pr=proj(r,[c[0],c[1]],Math.max(0,b-2),b+2);if(pr&&pr.d<25)r.cams.push({s:pr.s,sp:c[2],t:c[3],z:c[4]})})});
  r.cams.sort(function(a,b){return a.s-b.s});return r})}
function camKeys(c){if(c.t=='z')return ['zs-'+c.sp];if(c.t=='e')return ['ze'];if(c.t=='l')return ['caml'];if(c.z=='c')return ['camc-'+c.sp];if(c.z=='o')return ['camo-'+c.sp];return ['cam-'+c.sp]}
function camText(c){if(c.t=='z')return '구간 단속이 시작됩니다. 제한속도 '+c.sp+'킬로미터입니다.';if(c.t=='e')return '구간 단속이 끝났습니다.';if(c.t=='l')return '신호 단속 카메라가 있습니다.';return (c.z=='c'?'어린이보호구역입니다. ':c.z=='o'?'노인보호구역입니다. ':'과속 단속 카메라가 있습니다. ')+'제한속도 '+c.sp+'킬로미터입니다.'}
function atS(r,s){var i=0;while(i<r.cum.length-2&&r.cum[i+1]<s)i++;var f=(s-r.cum[i])/Math.max(r.cum[i+1]-r.cum[i],.01);f=Math.max(0,Math.min(1,f));return {i:i,q:[r.co[i][0]+(r.co[i+1][0]-r.co[i][0])*f,r.co[i][1]+(r.co[i+1][1]-r.co[i][1])*f]}}
function start(sim){var st=stops();if(st.length<1){alert('먼저 정류장을 찍어 주세요');return}
 $('nav').hidden=false;document.documentElement.style.overflow='hidden';
 try{if(!sim&&screen.orientation&&screen.orientation.lock&&document.documentElement.requestFullscreen&&/Android/i.test(navigator.userAgent)){document.documentElement.requestFullscreen().then(function(){return screen.orientation.lock('portrait')}).catch(function(){})}}catch(e){}$('nv-simtag').hidden=!sim;
 if(!N||!N.map){N={map:HM.make(document.getElementById('nvmap'),st[0].lat,st[0].lng,16)}}
 setTimeout(function(){N.map.relayout()},60);
 N.stops=st;N.si=0;N.k=0;N.ci=0;N.off=0;N.said={};N.sim=sim;N.busy=false;
 (N.objs||[]).forEach(function(o){o.remove()});N.objs=st.map(function(s){return N.map.pin(s.lat,s.lng,{label:s.no})});
 N.car=N.map.car(st[0].lat,st[0].lng);N.objs.push(N.car);
 try{if(navigator.wakeLock)navigator.wakeLock.request('screen').then(function(w){N.wl=w}).catch(function(){})}catch(e){}
 $('nv-d').textContent='경로 준비 중…';$('nv-r').textContent='';
 var go=function(from){route(from,N.stops).then(function(r){N.r=prep(r);loadCams(N.r);N.ck=0;N.zone=null;N.k=0;N.ci=0;N.s=0;N.v=0;N.lt=Date.now();N.lastRe=0;N.base=0;
   N.todo=N.map.line(r.co,{color:'#F04452',weight:4,opacity:.9});N.done=N.map.line([],{color:'#9AA4B1',weight:4,opacity:.85});N.objs.push(N.todo,N.done);
   if(sim)simrun();else watch();say2(['first-'+N.stops[0].no],'안내를 시작합니다. 첫 정류장은 '+N.stops[0].n+'입니다.')}).catch(function(){$('nv-d').textContent='경로를 못 찾았어요';$('nv-r').textContent='인터넷 연결을 확인하거나 잠시 뒤 다시 시도해 주세요'})};
 if(sim)go(null);else{ // 정확한 GPS가 잡힐 때까지 최대 12초 기다렸다가 출발점으로 쓴다
  var best=null,t0=Date.now(),done=false,wid=null;$('nv-d').textContent='GPS 잡는 중…';$('nv-r').textContent='하늘이 보이는 곳에서 잠시만 기다려 주세요';
  var fin=function(){if(done)return;done=true;if(wid!=null)navigator.geolocation.clearWatch(wid);N.acc0=best?best.coords.accuracy:null;go(best?[best.coords.latitude,best.coords.longitude]:null)};
  wid=navigator.geolocation.watchPosition(function(g){if(!best||g.coords.accuracy<best.coords.accuracy)best=g;$('nv-r').textContent='현재 위치 정확도 약 '+Math.round(g.coords.accuracy)+'m'+(g.coords.accuracy>40?' · 더 정확해지길 기다리는 중':'');
   if(g.coords.accuracy<=30||(g.coords.accuracy<=60&&Date.now()-t0>5000))fin()},function(){fin()},{enableHighAccuracy:true,maximumAge:0,timeout:12000});
  setTimeout(fin,12000)}
}
function reroute(p){if(N.busy||Date.now()-(N.lastRe||0)<10000)return;N.busy=true;$('nv-r').textContent='경로를 다시 찾는 중…';say2(['reroute'],'경로를 다시 탐색합니다');
 route(p,N.stops.slice(N.si)).then(function(r){N.base=N.si;N.r=prep(r);loadCams(N.r);N.ck=0;N.k=0;N.ci=0;N.s=0;N.off=0;N.said={};N.todo.set(r.co);N.done.set([]);N.busy=false;N.lastRe=Date.now()}).catch(function(e){N.busy=false;try{console.warn('reroute fail',e&&e.message)}catch(_){}})}
function onPos(p,hd,acc,spd,dr){if(!N||!N.r||N.busy)return;var r=N.r,now=Date.now();
 if(!dr){if(acc&&acc>60){N.weak=(N.weak||0)+1;if(N.weak>2)$('nv-k').textContent='GPS 신호가 약해요 · 오차 약 '+Math.round(acc)+'m';return}N.weak=0;N.lt=now;}
 var pr=proj(r,p,Math.max(0,N.ci-3),N.ci+400),lim=Math.max(45,Math.min(acc||10,60)*1.5);
 if(!pr)return;
 if(pr.d>lim&&!N.sim&&!dr){if(++N.off>=3){reroute(p)}}else N.off=0;
 // 진행 거리: 뒤로는 거의 안 가게
 var ns0=pr.d<lim?pr.s:N.s;if(ns0<N.s-15)ns0=N.s;var dt=Math.max(.2,(now-(N.pt||now))/1000)||1;
 if(spd!=null&&!isNaN(spd)&&spd>=0)N.v=N.v*.4+spd*.6;else if(N.pt)N.v=N.v*.6+Math.max(0,(ns0-N.s)/dt)*.4;N.pt=now;
 N.s=ns0;var at=atS(r,N.s);N.ci=at.i;var show=pr.d<30||dr?at.q:p;
 var h=brg(r.co[Math.max(0,at.i)],r.co[Math.min(at.i+1,r.co.length-1)]);if(pr.d>=30&&hd!=null&&!isNaN(hd)&&N.v>2)h=hd;
 N.car.set(show[0],show[1],h);N.map.view(show[0],show[1],N.map.zoom()<15?17:null);
 N.done.set(r.co.slice(0,at.i+1).concat([at.q]));
 // 정류장 도착: 진행 거리 기준(가까이 오거나 지나치면)
 var j=N.si-N.base,sst=N.stops[N.si];
 if(sst&&r.ss[j]!=null&&(N.s>=r.ss[j]-25&&hv(show,[sst.lat,sst.lng])<90||N.s>r.ss[j]+40)){say2(['arr-'+sst.no].concat(N.stops[N.si+1]?['next-'+N.stops[N.si+1].no]:['last']),sst.no+'번 '+sst.n+'에 도착했습니다.'+(N.stops[N.si+1]?' 다음은 '+N.stops[N.si+1].n+'입니다.':' 마지막 정류장입니다. 수고하셨습니다.'));sync(sst.no);N.si++;j++;
  if(N.si>=N.stops.length){$('nv-d').textContent='운행 끝';$('nv-r').textContent='모든 정류장을 돌았어요';$('nv-ic').innerHTML=icon(null);stopWatch();return}}
 // 단속카메라·제한속도
 var cams=r.cams||[];while(N.ck<cams.length&&cams[N.ck].s<N.s-8){var pc=cams[N.ck];if(pc.t=='z')N.zone=pc.sp;if(pc.t=='e')N.zone=null;N.ck++}
 var cc=cams[N.ck],lim=N.zone||0,vk=Math.round((N.v||0)*3.6);
 if(cc){var dc=cc.s-N.s,va=Math.max(N.v||0,5);if(dc<Math.max(300,va*12)){if(cc.sp)lim=cc.sp;$('nv-cam').hidden=false;$('nv-cam').textContent=(cc.t=='z'?'구간 단속 시작':cc.t=='e'?'구간 단속 끝':cc.t=='l'?'신호 단속 카메라':cc.z=='c'?'어린이보호구역 단속':'과속 단속 카메라')+' · '+fmt(Math.max(0,dc))+' 앞';
   if(!N.said['c'+N.ck]){N.said['c'+N.ck]=1;say2(camKeys(cc),camText(cc))}}else $('nv-cam').hidden=true}else $('nv-cam').hidden=true;
 $('nv-lim').hidden=!lim;if(lim)$('nv-limv').textContent=lim;$('nv-v').textContent=vk;$('nv-spd').className='nv-spd'+(lim&&vk>lim?' over':'');
 // 다음 회전: 속도에 맞춰 미리 안내
 while(N.k<r.steps.length&&r.cum[r.steps[N.k].ci]<=N.s+5)N.k++;
 var nx=r.steps[N.k],ns=N.stops[N.si],v=Math.max(N.v||0,5),far=Math.min(800,Math.max(250,v*18)),near=Math.min(150,Math.max(40,v*5));
 if(nx){var dm=r.cum[nx.ci]-N.s;$('nv-ic').innerHTML=icon(nx);$('nv-d').textContent=fmt(dm);$('nv-r').textContent=say(nx)+(nx.name&&say(nx).indexOf(nx.name)<0?' · '+nx.name:'');
  var key=N.k;if(dm<far&&dm>near*1.8&&!N.said[key+'a']){N.said[key+'a']=1;say2(['d'+dk(dm)+'-'+mk(nx.mod)],fmt(Math.round(dm/50)*50).replace('km','킬로미터').replace('m','미터')+' 앞에서 '+say(nx)+(/다$|요$/.test(say(nx))?'':'입니다'))}
  if(dm<=near&&!N.said[key+'b']){N.said[key+'b']=1;say2(['now-'+mk(nx.mod)],say(nx),true)}}
 else{$('nv-ic').innerHTML=icon(null);$('nv-d').textContent=ns?fmt(Math.max(0,(r.ss[j]||0)-N.s)):'';$('nv-r').textContent='도로를 따라 직진'}
 if(ns&&r.ss[j]!=null){var sd=Math.max(0,r.ss[j]-N.s);$('nv-k').textContent='다음 정류장 '+ns.no+'번 · 남은 '+(N.stops.length-N.si)+'곳';$('nv-s').textContent=ns.n+' · '+fmt(sd)+' · 약 '+Math.max(1,Math.round(sd/Math.max(r.spd,1)/60))+'분';
  if(sd<Math.max(250,v*15)&&sd>Math.max(80,v*4)&&!N.said['s'+N.si]){N.said['s'+N.si]=1;say2(['soon-'+ns.no],'곧 '+ns.no+'번 '+ns.n+'입니다')}}}
function sync(no){var S=store();if(!S)return;S.pos[S.cur]=Math.min(no,(S.routes[S.cur]||[]).length-1);if(no>=(S.routes[S.cur]||[]).length)S.pos[S.cur]=0;try{localStorage.setItem('hl-route-navi-v1',JSON.stringify(S))}catch(e){}}
// 터널 등에서 위치가 끊기면 마지막 속도로 경로를 따라 잠깐 이어 간다(최대 20초)
setInterval(function(){if(!N||!N.r||N.sim||!N.w||N.busy)return;var gap=(Date.now()-N.lt)/1000;if(gap>3&&gap<20&&N.v>3){var q=atS(N.r,N.s+N.v).q;onPos(q,null,null,N.v,true)}},1000);
function watch(){stopWatch();N.w=navigator.geolocation.watchPosition(function(g){onPos([g.coords.latitude,g.coords.longitude],g.coords.heading,g.coords.accuracy,g.coords.speed)},function(){$('nv-r').textContent='위치를 받을 수 없어요. 위치 권한을 확인해 주세요'},{enableHighAccuracy:true,maximumAge:1000,timeout:15000})}
function simrun(){stopWatch();var co=N.r.co,cum=N.r.cum,t=0,v=14;N.t=setInterval(function(){t+=v;var i=0;while(i<cum.length-1&&cum[i+1]<t)i++;if(i>=cum.length-1){onPos(co[co.length-1],null,5,0);stopWatch();return}
  var f=(t-cum[i])/Math.max(cum[i+1]-cum[i],.01),p=[co[i][0]+(co[i+1][0]-co[i][0])*f,co[i][1]+(co[i+1][1]-co[i][1])*f];onPos(p,brg(co[i],co[i+1]),5,v*2)},500)}
function stopWatch(){if(N&&N.w!=null){navigator.geolocation.clearWatch(N.w);N.w=null}if(N&&N.t){clearInterval(N.t);N.t=null}}
function end(){try{if(document.fullscreenElement)document.exitFullscreen()}catch(e){}stopWatch();if(N&&N.wl){N.wl.release().catch(function(){});N.wl=null}if(window.speechSynthesis)speechSynthesis.cancel();$('nav').hidden=true;document.documentElement.style.overflow='';if(window.__rnRefresh)window.__rnRefresh()}
$('nv-end').onclick=end;
$('nv-mute').onclick=function(){voice=!voice;this.textContent=voice?'음성 켜짐':'음성 꺼짐';this.setAttribute('aria-pressed',!voice);if(!voice&&window.speechSynthesis)speechSynthesis.cancel()};
function unlock(){if(!CL.a)CL.a=new Audio();try{CL.a.src='data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA//tQxAADB8AhSmxhIIEVCSiJrDCQBTcu3UrAIwUdkRgQbFAZC1CQEwTJ9mjRvBA4UOLD8nKVOWfh+UlK3z/177OXrfOdKl7pyn3Xf//WreyTRUoAWgBgkOAGbZHBgG1OF6zM82DWbZaUmMBptgQhGjsyYqc9ae9XFz280948NMBWInljyzsNRFLPWdnZGWrddDsjK1unuSrVN9jJsK8KuQtQCtMBjCEtImISdNKJOopIpBFpNSMbIHCSRpRR5iakjTiyzLhchUUBwCgyKiweBv/7UsQbg8isVNoMPMjAAAA0gAAABEVFGmgqK////9bP/6XCykxBTUUzLjEwMKqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq';CL.a.play().catch(function(){})}catch(e){}}
$('self-go').onclick=function(){if(!navigator.geolocation){alert('이 기기에서는 위치를 쓸 수 없어요');return}unlock();speak('');start(false)};
$('self-sim').onclick=function(){unlock();speak('');start(true)};
document.addEventListener('visibilitychange',function(){if(!document.hidden&&N&&N.wl===null&&!$('nav').hidden&&navigator.wakeLock)navigator.wakeLock.request('screen').then(function(w){N.wl=w}).catch(function(){})});
(function(){function get(){var S=store()||{},o=S.opt||{pr:'RECOMMEND',av:['uturn']};o.av=(o.av||[]).filter(Boolean);if(o.pr!='TIME')o.pr='RECOMMEND';return o}function put(o){var S=store();if(!S)return;S.opt=o;try{localStorage.setItem('hl-route-navi-v1',JSON.stringify(S))}catch(e){}}
 function paint(){var o=get();var h=document.getElementById('hwy');h.checked=o.pr=='TIME';var mw=document.querySelector('.rn-chk input[data-av=motorway]');if(mw){mw.disabled=h.checked;if(h.checked)mw.checked=false}document.querySelectorAll('.rn-chk input[data-av]').forEach(function(c){c.checked=(o.av||[]).indexOf(c.dataset.av)>=0})}
 document.getElementById('hwy').onchange=function(){var o=get();o.pr=this.checked?'TIME':'RECOMMEND';if(this.checked)o.av=(o.av||[]).filter(function(x){return x!='motorway'});put(o);paint()};
 document.querySelectorAll('.rn-chk input[data-av]').forEach(function(c){c.onchange=function(){var o=get();o.av=[].slice.call(document.querySelectorAll('.rn-chk input[data-av]:checked')).map(function(x){return x.dataset.av});put(o)}});paint()})();
window.__selfnav={onPos:onPos,start:start,st:function(){return N&&{s:N.s,ci:N.ci,si:N.si,off:N.off,busy:N.busy,v:N.v,lt:N.lt}}};
});</script>'''
