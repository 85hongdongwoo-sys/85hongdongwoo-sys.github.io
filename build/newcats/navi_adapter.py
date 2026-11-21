KAKAO_JS = 'c4a8d8392dd6a362db17cc44e5ae398b'
KAKAO_REST = ''  # 공개 저장소에 넣지 않음 — 중계 서버(PROXY) 뒤에서만 사용
PROXY = 'https://hl-route.a599307.workers.dev/'
JS = r'''<script>
window.HM=(function(){
var READY=[],kind=null;
function done(k){if(kind)return;kind=k;READY.forEach(function(f){f(k)})}
function ready(f){if(kind)f(kind);else READY.push(f)}
(function(){var s=document.createElement('script');s.src='https://dapi.kakao.com/v2/maps/sdk.js?appkey=__JSKEY__&autoload=false&libraries=services';
 s.onload=function(){try{kakao.maps.load(function(){done('kakao')})}catch(e){done('leaflet')}};s.onerror=function(){done('leaflet')};document.head.appendChild(s);
 setTimeout(function(){done('leaflet')},6000)})();
function pinSvg(n,cls){var c=cls=='cur'?'#F04452':cls=='done'?'#B0B8C1':cls=='warn'?'#F08C00':'#3182F6',w=cls=='cur'?40:34;
 return 'data:image/svg+xml;charset=utf-8,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+Math.round(w*1.25)+'" viewBox="0 0 32 40"><path d="M16 39C16 39 3 24 3 15a13 13 0 0 1 26 0c0 9-13 24-13 24z" fill="'+c+'" stroke="#fff" stroke-width="2.4"/><text x="16" y="20" text-anchor="middle" font-family="system-ui,sans-serif" font-size="'+(String(n).length>2?10:13)+'" font-weight="800" fill="#fff">'+n+'</text></svg>')}
function lv(z){return Math.max(1,Math.min(14,20-z))}
function zk(l){return 20-l}
// 지도 유형(일반·위성·지형)·교통정보 버튼: 고른 값은 이 기기에 기억
var LK='hl-map-layer';function lget(){try{return JSON.parse(localStorage.getItem(LK))||{}}catch(e){return {}}}function lset(o){try{localStorage.setItem(LK,JSON.stringify(o))}catch(e){}}
function layerUI(el,a){if(!a.mtype)return;var st=lget(),t=st.t||'road',tf=!!st.tf&&!!a.traffic;
 if(!document.getElementById('hl-lyr-css')){var cs=document.createElement('style');cs.id='hl-lyr-css';cs.textContent='.hl-lyr{position:absolute;right:10px;top:58px;z-index:600;font-family:inherit}.hl-lyr>button{width:40px;height:40px;border-radius:12px;border:1px solid #E5E8EB;background:#fff;display:grid;place-items:center;color:#191F28;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.12);padding:0}.hl-lyr-p{position:absolute;right:0;top:46px;width:200px;background:#fff;border:1px solid #E5E8EB;border-radius:14px;box-shadow:0 6px 18px rgba(0,0,0,.16);padding:10px}.hl-lyr-p p{margin:0 0 6px;font-size:12.5px;font-weight:800;color:#4E5968}.hl-lyr-g{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:8px}.hl-lyr-p .b{height:36px;border-radius:10px;border:1px solid #E5E8EB;background:#F9FAFB;font-size:13.5px;font-weight:700;color:#333D4B;cursor:pointer;padding:0}.hl-lyr-p .b[aria-pressed=true]{background:#3182F6;border-color:#3182F6;color:#fff}.hl-lyr-p .w{width:100%}';document.head.appendChild(cs)}
 var w=document.createElement('div');w.className='hl-lyr';w.innerHTML='<button type="button" aria-label="지도 유형" aria-expanded="false"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/></svg></button><div class="hl-lyr-p" hidden><p>지도 유형</p><div class="hl-lyr-g"><button type="button" class="b" data-t="road">일반</button><button type="button" class="b" data-t="sat">위성</button><button type="button" class="b" data-t="terrain">지형</button></div>'+(a.traffic?'<p>지도 추가 정보</p><button type="button" class="b w" data-x="tf">교통정보</button>':'')+'</div>';
 ['mousedown','touchstart','click','dblclick','wheel','pointerdown'].forEach(function(e){w.addEventListener(e,function(ev){ev.stopPropagation()},{passive:true})});
 var bt=w.firstChild,pn=w.lastChild;function paint(){[].forEach.call(pn.querySelectorAll('[data-t]'),function(b){b.setAttribute('aria-pressed',b.getAttribute('data-t')==t)});var x=pn.querySelector('[data-x]');if(x)x.setAttribute('aria-pressed',tf)}
 bt.onclick=function(){pn.hidden=!pn.hidden;bt.setAttribute('aria-expanded',!pn.hidden)};
 pn.onclick=function(e){var b=e.target.closest('button');if(!b)return;if(b.dataset.t){t=b.dataset.t;a.mtype(t)}else if(b.dataset.x){tf=!tf;a.traffic(tf)}st=lget();st.t=t;st.tf=tf;lset(st);paint()};
 el.appendChild(w);if(t!='road')a.mtype(t);if(tf)a.traffic(true);paint()}
function make(el,lat,lng,z){var a=make0(el,lat,lng,z);try{layerUI(el,a)}catch(e){}return a}
function make0(el,lat,lng,z){
 if(kind=='kakao'){var K=kakao.maps,map=new K.Map(el,{center:new K.LatLng(lat,lng),level:lv(z)});map.addControl(new K.ZoomControl(),K.ControlPosition.RIGHT);
  return {kind:'kakao',
   onClick:function(f){K.event.addListener(map,'click',function(e){f(e.latLng.getLat(),e.latLng.getLng())})},
   view:function(a,b,zz){map.setCenter(new K.LatLng(a,b));if(zz)map.setLevel(lv(zz))},
   pan:function(a,b){map.panTo(new K.LatLng(a,b))},
   zoom:function(){return zk(map.getLevel())},
   fit:function(pts){if(!pts.length)return;var bd=new K.LatLngBounds();pts.forEach(function(p){bd.extend(new K.LatLng(p[0],p[1]))});map.setBounds(bd,40,40,40,40);if(map.getLevel()<3)map.setLevel(3)},
   pin:function(a,b,o){var w=o.cls=='cur'?40:34,mk=new K.Marker({map:map,position:new K.LatLng(a,b),draggable:!!o.drag,title:o.title||'',image:new K.MarkerImage(pinSvg(o.label,o.cls),new K.Size(w,Math.round(w*1.25)),{offset:new K.Point(w/2,Math.round(w*1.25))})});
    if(o.onDrag)K.event.addListener(mk,'dragend',function(){var p=mk.getPosition();o.onDrag(p.getLat(),p.getLng())});return {remove:function(){mk.setMap(null)}}},
   line:function(pts,o){var pl=new K.Polyline({map:map,path:pts.map(function(p){return new K.LatLng(p[0],p[1])}),strokeWeight:o.weight||5,strokeColor:o.color||'#3182F6',strokeOpacity:o.opacity||.8,strokeStyle:o.dash?'shortdash':'solid'});
    return {set:function(ps){pl.setPath(ps.map(function(p){return new K.LatLng(p[0],p[1])}))},remove:function(){pl.setMap(null)}}},
   car:function(a,b){var d=document.createElement('div');d.className='nv-car';d.innerHTML='<svg viewBox="0 0 24 24"><path d="M12 2l7 19-7-4-7 4z" fill="#1B64DA" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
    var ov=new K.CustomOverlay({map:map,position:new K.LatLng(a,b),content:d,zIndex:10});return {set:function(x,y,h){ov.setPosition(new K.LatLng(x,y));if(h!=null)d.firstChild.style.transform='rotate('+h+'deg)'},remove:function(){ov.setMap(null)}}},
   dot:function(a,b){var d=document.createElement('div');d.style.cssText='width:16px;height:16px;border-radius:50%;background:#3182F6;border:3px solid #fff;box-shadow:0 0 0 6px rgba(49,130,246,.25)';new K.CustomOverlay({map:map,position:new K.LatLng(a,b),content:d})},
   mtype:function(t){var M=K.MapTypeId;map.setMapTypeId(t=='sat'?M.HYBRID:M.ROADMAP);if(t=='terrain'){if(!map.__tr){map.addOverlayMapTypeId(M.TERRAIN);map.__tr=1}}else if(map.__tr){map.removeOverlayMapTypeId(M.TERRAIN);map.__tr=0}},
   traffic:function(on){var M=K.MapTypeId;if(on&&!map.__tf){map.addOverlayMapTypeId(M.TRAFFIC);map.__tf=1}else if(!on&&map.__tf){map.removeOverlayMapTypeId(M.TRAFFIC);map.__tf=0}},
   relayout:function(){map.relayout()}}}
 var m=L.map(el,{zoomControl:true}).setView([lat,lng],z),TL={road:['https://tile.openstreetmap.org/{z}/{x}/{y}.png',19,'&copy; OpenStreetMap'],sat:['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',19,'&copy; Esri'],terrain:['https://tile.opentopomap.org/{z}/{x}/{y}.png',17,'&copy; OpenStreetMap, SRTM, OpenTopoMap']},bl=L.tileLayer(TL.road[0],{maxZoom:19,attribution:TL.road[2]}).addTo(m);
 return {kind:'leaflet',
  onClick:function(f){m.on('click',function(e){f(e.latlng.lat,e.latlng.lng)})},
  view:function(a,b,zz){m.setView([a,b],zz||m.getZoom())},pan:function(a,b){m.panTo([a,b])},zoom:function(){return m.getZoom()},
  fit:function(pts){if(pts.length)m.fitBounds(L.latLngBounds(pts).pad(.2),{maxZoom:16})},
  pin:function(a,b,o){var w=o.cls=='cur'?40:34,h=Math.round(w*1.25),mk=L.marker([a,b],{draggable:!!o.drag,title:o.title||'',icon:L.icon({iconUrl:pinSvg(o.label,o.cls),iconSize:[w,h],iconAnchor:[w/2,h]})}).addTo(m);
   if(o.onDrag)mk.on('dragend',function(){var p=mk.getLatLng();o.onDrag(p.lat,p.lng)});return {remove:function(){mk.remove()}}},
  line:function(pts,o){var pl=L.polyline(pts,{color:o.color||'#3182F6',weight:o.weight||5,opacity:o.opacity||.8,dashArray:o.dash?'6 8':null}).addTo(m);return {set:function(ps){pl.setLatLngs(ps)},remove:function(){pl.remove()}}},
  car:function(a,b){var mk=L.marker([a,b],{zIndexOffset:1000,icon:L.divIcon({className:'nv-car',html:'<svg viewBox="0 0 24 24"><path d="M12 2l7 19-7-4-7 4z" fill="#1B64DA" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>',iconSize:[34,34],iconAnchor:[17,17]})}).addTo(m);
   return {set:function(x,y,h){mk.setLatLng([x,y]);var e=mk.getElement();if(e&&h!=null)e.querySelector('svg').style.transform='rotate('+h+'deg)'},remove:function(){mk.remove()}}},
  dot:function(a,b){L.circleMarker([a,b],{radius:8,color:'#fff',weight:3,fillColor:'#3182F6',fillOpacity:1}).addTo(m)},
  mtype:function(t){var d=TL[t]||TL.road;bl.remove();bl=L.tileLayer(d[0],{maxZoom:d[1],attribution:d[2]}).addTo(m)},
  relayout:function(){m.invalidateSize()}}}
// 경로: 카카오모빌리티 다중 경유지(30곳씩 나눠 이어 붙임) → 실패하면 OSRM
function hv(a,b){var r=Math.PI/180,dl=(b[0]-a[0])*r,dg=(b[1]-a[1])*r,x=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dg/2)*Math.sin(dg/2);return 12742000*Math.asin(Math.sqrt(x))}
function modOf(t){return /유턴/.test(t)?'uturn':/회전교차로/.test(t)?'round':/좌회전/.test(t)?'left':/우회전/.test(t)?'right':/왼쪽/.test(t)?'slight left':/오른쪽/.test(t)?'slight right':'straight'}
function kakaoChunk(pts,op){op=op||{};var o=pts[0],d=pts[pts.length-1],w=pts.slice(1,-1);
 if(!'__PROXY__')return Promise.reject(new Error('no proxy'));
 return fetch('__PROXY__',{method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({origin:{x:o[1],y:o[0]},destination:{x:d[1],y:d[0]},waypoints:w.map(function(p){return {x:p[1],y:p[0]}}),priority:op.pr||'RECOMMEND',avoid:(op.av&&op.av.length)?op.av:undefined,summary:false})}).then(function(r){return r.json()}).then(function(j){
  var R=j.routes&&j.routes[0];if(!R||R.result_code!==0)throw new Error(R?R.result_msg:'kakao');var co=[],steps=[];
  R.sections.forEach(function(sc){sc.roads.forEach(function(rd){for(var i=0;i<rd.vertexes.length;i+=2){var p=[rd.vertexes[i+1],rd.vertexes[i]],l=co[co.length-1];if(!l||l[0]!=p[0]||l[1]!=p[1])co.push(p)}});
   sc.guides.forEach(function(g){if(g.type==100||g.type==101||g.type==1000)return;steps.push({p:[g.y,g.x],text:g.guidance,name:g.name||'',mod:modOf(g.guidance)})})});
  return {co:co,steps:steps,dist:R.summary.distance,dur:R.summary.duration}})}
var OM={'left':'좌회전','right':'우회전','slight left':'왼쪽 방향','slight right':'오른쪽 방향','sharp left':'급좌회전','sharp right':'급우회전','uturn':'유턴','straight':'직진'};
function osrm(pts){return fetch('https://router.project-osrm.org/route/v1/driving/'+pts.map(function(p){return p[1].toFixed(6)+','+p[0].toFixed(6)}).join(';')+'?overview=full&geometries=geojson&steps=true').then(function(r){return r.json()}).then(function(j){
  var R=j.routes&&j.routes[0];if(!R)throw new Error('osrm');var steps=[];R.legs.forEach(function(l){l.steps.forEach(function(s){var t=s.maneuver.type;if(t=='depart'||t=='arrive')return;var m=s.maneuver.modifier||'straight';
   var tx=(t=='roundabout'||t=='rotary')?'회전교차로 '+(s.maneuver.exit||1)+'번째 출구':(OM[m]||'직진');steps.push({p:[s.maneuver.location[1],s.maneuver.location[0]],text:tx,name:s.name||'',mod:(t=='roundabout'||t=='rotary')?'round':m})})});
  return {co:R.geometry.coordinates.map(function(c){return [c[1],c[0]]}),steps:steps,dist:R.distance,dur:R.duration}})}
function route(pts,op){var chunks=[],i=0;while(i<pts.length-1){var c=pts.slice(i,i+32);chunks.push(c);i+=c.length-1}
 var all=function(fn){return Promise.all(chunks.map(function(c){return fn(c,op)})).then(function(rs){var co=[],steps=[],dist=0,dur=0;rs.forEach(function(r){co=co.concat(co.length?r.co.slice(1):r.co);steps=steps.concat(r.steps);dist+=r.dist;dur+=r.dur});
  var cum=[0];for(var k=1;k<co.length;k++)cum.push(cum[k-1]+hv(co[k-1],co[k]));
  steps.forEach(function(s){var b=0,bd=1e12;for(var k=0;k<co.length;k++){var d=hv(co[k],s.p);if(d<bd){bd=d;b=k}}s.ci=b});steps.sort(function(a,b){return a.ci-b.ci});
  return {co:co,cum:cum,steps:steps,spd:dist/Math.max(dur,1),src:fn===kakaoChunk?'kakao':'osrm'}})};
 return all(kakaoChunk).catch(function(){return all(osrm)})}
function search(q){return new Promise(function(res){if(kind!='kakao'||!kakao.maps.services){res(null);return}var S=kakao.maps.services,out=[],n=0,fin=function(){if(++n==2)res(out)};
 new S.Places().keywordSearch(q,function(d,st){if(st==S.Status.OK)d.slice(0,8).forEach(function(x){out.push({n:x.place_name,a:x.road_address_name||x.address_name,lat:+x.y,lng:+x.x})});fin()});
 new S.Geocoder().addressSearch(q,function(d,st){if(st==S.Status.OK)d.slice(0,3).forEach(function(x){out.unshift({n:x.address_name,a:(x.road_address&&x.road_address.address_name)||'',lat:+x.y,lng:+x.x})});fin()})})}
return {ready:ready,make:make,route:route,hv:hv,search:search}})();
</script>'''
