# 공공데이터 지도 도구 (데이터: build/pubdata/fetch.py → /data/pub/) → overlay/<dir>/<slug>.html
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_maptools import shell, COMMON_CSS, KAKAO_JS

PUB_CSS = '''
.pub-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:10px 0 0}
.pub-bar select{font:inherit;font-size:16px;padding:9px 10px;border:1px solid var(--line-s);border-radius:10px;min-height:44px;background:#fff;width:auto!important;flex:0 0 auto}
.pub-bar .me{font:inherit;font-size:14.5px;font-weight:800;border:0;border-radius:10px;min-height:44px;padding:0 14px;background:var(--acc);color:#fff;cursor:pointer}
.pub-bar .q{flex:1 1 160px;font:inherit;font-size:16px;padding:9px 12px;border:1px solid var(--line-s);border-radius:10px;min-height:44px;min-width:0}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 0}
.chips button{font:inherit;font-size:13.5px;font-weight:700;border:1px solid var(--line-s);background:#fff;border-radius:999px;min-height:36px;padding:0 12px;cursor:pointer;color:var(--head)}
.chips button[aria-pressed=true]{background:#191F28;border-color:#191F28;color:#fff}
.pub-st{font-size:13px;color:var(--muted);margin:10px 0 0;line-height:1.5}
.pub-list{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}
.pub-list li{border:1px solid var(--line-s);border-radius:14px;background:#fff;padding:12px 14px;cursor:pointer}
.pub-list li.sel{border:2px solid var(--acc)}
.pub-list .h{display:flex;gap:8px;align-items:flex-start;justify-content:space-between}
.pub-list .h b{font-size:15.5px;color:var(--head);line-height:1.35;word-break:keep-all}
.pub-list .d{white-space:nowrap;font-size:12.5px;color:var(--muted);font-weight:700;padding-top:2px}
.pub-list .a{font-size:13px;color:var(--muted);margin:3px 0 0;line-height:1.45;word-break:keep-all}
.pub-list .m{display:flex;gap:6px;flex-wrap:wrap;margin-top:7px;font-size:13px}
.tg{display:inline-flex;align-items:center;border-radius:7px;padding:2px 8px;font-weight:800;font-size:12.5px;background:#F1F3F5;color:#333}
.tg.g{background:#E6FCF5;color:#087F5B}.tg.r{background:#FFF0F0;color:#C92A2A}.tg.b{background:#E7F0FF;color:#1D4ED8}.tg.y{background:#FFF4D6;color:#8A5A00}
.pub-list .lk{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.pub-list .lk a{font-size:13px;font-weight:800;text-decoration:none;border-radius:9px;padding:7px 11px;background:#F1F3F5;color:var(--head)}
.pub-list .lk a.k{background:#FEE500;color:#191919}
.pub-list img.th{width:100%;max-height:170px;object-fit:cover;border-radius:10px;margin-top:8px;background:#F1F3F5}
.pub-more{display:block;width:100%;margin-top:10px;min-height:44px;border:1px solid var(--line-s);border-radius:12px;background:#fff;font:inherit;font-weight:700;cursor:pointer}
.pub-empty{padding:18px;border-radius:14px;background:#F4F7FB;text-align:center;font-size:14.5px;line-height:1.6;color:var(--ink)}
.pub-src{font-size:12px;color:var(--muted);margin-top:10px}
.pub-list .lk a.rv{background:#E7F0FF;color:#1D4ED8}
.rvw{margin-top:9px;cursor:default}.rvbox{width:100%;height:230px;border-radius:10px;overflow:hidden;background:#F1F3F5}
.rvn{font-size:12px;color:var(--muted);margin:5px 0 0;line-height:1.45;word-break:keep-all}
'''

ENGINE = r'''
(function(){
var C=window.PUBCFG,$=function(i){return document.getElementById(i)},SIDO=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주'];
var CEN={'서울':[37.5665,126.978],'부산':[35.1796,129.0756],'대구':[35.8714,128.6014],'인천':[37.4563,126.7052],'광주':[35.1595,126.8526],'대전':[36.3504,127.3845],'울산':[35.5384,129.3114],'세종':[36.48,127.289],'경기':[37.2636,127.0286],'강원':[37.8813,127.7298],'충북':[36.6424,127.489],'충남':[36.6588,126.6728],'전북':[35.8242,127.148],'전남':[34.8161,126.4629],'경북':[36.576,128.5056],'경남':[35.2383,128.6924],'제주':[33.4996,126.5312]};
var AL={'서울특별시':'서울','부산광역시':'부산','대구광역시':'대구','인천광역시':'인천','광주광역시':'광주','대전광역시':'대전','울산광역시':'울산','세종특별자치시':'세종','경기도':'경기','강원특별자치도':'강원','강원도':'강원','충청북도':'충북','충청남도':'충남','전북특별자치도':'전북','전라북도':'전북','전라남도':'전남','경상북도':'경북','경상남도':'경남','제주특별자치도':'제주'};
var map,K,ROWS=[],META=null,me=null,flt=0,shown=40,mk=[],sel=-1,ov=null,cache={};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
window.PUB={esc:esc};
function dist(a,b,c,d){var R=6371,x=(c-a)*Math.PI/180,y=(d-b)*Math.PI/180,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*Math.PI/180)*Math.cos(c*Math.PI/180)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h))}
function dtxt(k){return k<1?Math.round(k*1000)+'m':(k<10?k.toFixed(1):Math.round(k))+'km'}
var sel_s=$('pub-sido');if(sel_s&&!C.single){SIDO.forEach(function(s){var o=document.createElement('option');o.value=o.textContent=s;sel_s.appendChild(o)})}else if(sel_s)sel_s.hidden=true;
var ch=$('pub-chips');(C.filters||[]).forEach(function(fl,i){var b=document.createElement('button');b.type='button';b.textContent=fl[0];b.setAttribute('aria-pressed',i===0);b.onclick=function(){flt=i;[].forEach.call(ch.children,function(x,j){x.setAttribute('aria-pressed',j===i)});shown=40;render()};ch.appendChild(b)});
function load(s){$('pub-st').textContent='불러오는 중…';var url=C.single?('/data/pub/'+C.single):('/data/pub/'+C.key+'/'+encodeURIComponent(s)+'.json');
 var mp=C.single?Promise.resolve(null):(META?Promise.resolve(META):fetch('/data/pub/'+C.key+'/meta.json',{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(m){META=m;return m}));
 return mp.then(function(){return cache[url]||fetch(url,{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json()})}).then(function(j){cache[url]=j;var cols,rows;
  if(C.single){cols=j.cols;rows=j.rows;META={updated:j.updated}}else{cols=META.cols;rows=j}
  ROWS=rows.map(function(r){var o={};cols.forEach(function(c,i){o[c]=r[i]});return o});shown=40;render()})
 .catch(function(){ROWS=[];$('pub-list').innerHTML='<li class="pub-empty" style="cursor:default">'+(C.empty||'자료를 준비하고 있어요. 잠시 후 다시 들어와 주세요.')+'</li>';$('pub-st').textContent='';$('pub-more').hidden=true})}
function center(){if(me)return me;var c=map.getCenter();return [c.getLat(),c.getLng()]}
function render(){var c=center(),f=(C.filters||[])[flt],q=($('pub-q')&&$('pub-q').value.trim())||'';
 var L=ROWS.filter(function(o){return (!f||!f[1]||f[1](o))&&(!q||(o.name+' '+(o.addr||'')+' '+(C.text?C.text(o):'')).indexOf(q)>=0)});
 L.forEach(function(o){o._d=dist(c[0],c[1],o.lat,o.lng)});
 if(C.sort&&C.sort(L)){}else L.sort(function(a,b){return a._d-b._d});
 var V=L.slice(0,shown),ul=$('pub-list');ul.innerHTML='';
 mk.forEach(function(m){m.setMap(null)});mk=[];if(ov){ov.setMap(null)}
 V.forEach(function(o,i){var li=document.createElement('li');li.innerHTML='<div class="h"><b>'+esc(o.name)+'</b><span class="d">'+dtxt(o._d)+'</span></div>'+(C.card?C.card(o):'')+
  '<div class="lk"><a class="k" target="_blank" rel="noopener" href="https://map.kakao.com/link/to/'+encodeURIComponent(o.name)+','+o.lat+','+o.lng+'">길찾기</a>'+(o.tel?'<a href="tel:'+esc(String(o.tel).replace(/[^0-9-]/g,''))+'">전화</a>':'')+(C.rv?'<a href="#" class="rv">📷 가게 앞 보기</a>':'')+(C.links?C.links(o):'')+'</div>';
  var rb=li.querySelector('a.rv');if(rb)rb.onclick=function(e){e.preventDefault();roadview(li,o,rb)};
  li.onclick=function(e){if(e.target.closest('a')||e.target.closest('.rvw'))return;focus(i,V)};ul.appendChild(li);
  var col=C.color?C.color(o):'#3182F6',svg='<svg xmlns="http://www.w3.org/2000/svg" width="26" height="33" viewBox="0 0 32 40"><path d="M16 39C16 39 3 24 3 15a13 13 0 0 1 26 0c0 9-13 24-13 24z" fill="'+col+'" stroke="#fff" stroke-width="2.6"/><circle cx="16" cy="15" r="5" fill="#fff"/></svg>';
  var m=new K.Marker({map:map,position:new K.LatLng(o.lat,o.lng),image:new K.MarkerImage('data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg),new K.Size(26,33),{offset:new K.Point(13,32)}),title:o.name});
  K.event.addListener(m,'click',function(){focus(i,V,true)});mk.push(m)});
 $('pub-more').hidden=L.length<=shown;
 $('pub-st').textContent=(L.length?((me?'내 위치':'지도 가운데')+'에서 가까운 순 '+Math.min(shown,L.length)+'곳 / 전체 '+L.length.toLocaleString()+'곳'):'조건에 맞는 곳이 없어요')+(META&&META.updated?' · '+META.updated+' 기준':'')+(C.note?' · '+C.note:'');
 if(!L.length)ul.innerHTML='<li class="pub-empty" style="cursor:default">조건에 맞는 곳이 없어요. 지역이나 필터를 바꿔 보세요.</li>'}
function roadview(li,o,btn){var w=li.querySelector('.rvw');if(w){w.remove();btn.textContent='📷 가게 앞 보기';return}
 [].forEach.call(document.querySelectorAll('.rvw'),function(x){var b=x.parentNode.querySelector('a.rv');if(b)b.textContent='📷 가게 앞 보기';x.remove()});
 w=document.createElement('div');w.className='rvw';w.innerHTML='<div class="rvbox"></div><p class="rvn">카카오 로드뷰의 주변 거리 사진이에요. 촬영 시점에 따라 지금 모습과 다를 수 있어요.</p>';li.appendChild(w);btn.textContent='✕ 닫기';
 if(window.gtag)gtag('event','pub_roadview',{t:C.key||C.single});
 var pos=new K.LatLng(o.lat,o.lng),box=w.firstChild;new K.RoadviewClient().getNearestPanoId(pos,70,function(id){if(id===null){box.style.height='auto';box.innerHTML='<p class="pub-empty" style="margin:0">이 근처는 로드뷰 사진이 없어요.</p>';return}
  var rv=new K.Roadview(box);rv.setPanoId(id,pos);K.event.addListener(rv,'init',function(){var p=rv.getPosition(),dy=o.lat-p.getLat(),dx=(o.lng-p.getLng())*Math.cos(o.lat*Math.PI/180),pan=(Math.atan2(dx,dy)*180/Math.PI+360)%360;rv.setViewpoint({pan:pan,tilt:0,zoom:0})})})}
function focus(i,V,fromMap){var o=V[i];[].forEach.call($('pub-list').children,function(li,j){li.classList.toggle('sel',j===i)});map.panTo(new K.LatLng(o.lat,o.lng));
 if(ov)ov.setMap(null);var d=document.createElement('div');d.style.cssText='background:#191F28;color:#fff;font-size:13px;font-weight:800;padding:6px 10px;border-radius:9px;white-space:nowrap;transform:translateY(-44px);box-shadow:0 2px 8px rgba(0,0,0,.2)';d.textContent=o.name;
 ov=new K.CustomOverlay({map:map,position:new K.LatLng(o.lat,o.lng),content:d,yAnchor:1});if(fromMap){var li=$('pub-list').children[i];if(li)li.scrollIntoView({block:'nearest',behavior:'smooth'})}}
$('pub-more').onclick=function(){shown+=40;render()};
if($('pub-q'))$('pub-q').addEventListener('input',function(){shown=40;render()});
function locate(){if(!navigator.geolocation){$('pub-st').textContent='이 브라우저는 위치를 지원하지 않아요. 지역을 골라 주세요.';return}
 $('pub-st').textContent='내 위치를 찾는 중…';navigator.geolocation.getCurrentPosition(function(p){me=[p.coords.latitude,p.coords.longitude];map.setCenter(new K.LatLng(me[0],me[1]));map.setLevel(6);
  if(window.gtag)gtag('event','pub_locate',{t:C.key||C.single});
  if(C.single){render();return}
  new K.services.Geocoder().coord2RegionCode(me[1],me[0],function(r,st){var s=st===K.services.Status.OK&&r[0]?(AL[r[0].region_1depth_name]||r[0].region_1depth_name.slice(0,2)):sel_s.value;if(SIDO.indexOf(s)<0)s=sel_s.value;sel_s.value=s;load(s)})},
 function(){$('pub-st').textContent='위치 권한이 없어서 지역 기준으로 보여 드려요.';load(sel_s?sel_s.value:'')},{enableHighAccuracy:false,timeout:8000,maximumAge:300000})}
$('pub-me').onclick=locate;
if(sel_s)sel_s.onchange=function(){me=null;var c=CEN[sel_s.value];map.setCenter(new K.LatLng(c[0],c[1]));map.setLevel(7);load(sel_s.value)};
var s=document.createElement('script');s.src='https://dapi.kakao.com/v2/maps/sdk.js?appkey=%KEY%&autoload=false&libraries=services';
s.onload=function(){kakao.maps.load(function(){K=kakao.maps;map=new K.Map($('map'),{center:new K.LatLng(37.5665,126.978),level:7});map.addControl(new K.ZoomControl(),K.ControlPosition.RIGHT);
 var t;K.event.addListener(map,'dragend',function(){me=null;clearTimeout(t);t=setTimeout(function(){shown=40;render()},250)});
 $('mp-hint').textContent=C.hint||'‘내 위치’를 누르거나 지역을 고르세요';load(sel_s&&!C.single?sel_s.value:'')})};
s.onerror=function(){$('mp-hint').textContent='지도를 불러오지 못했어요. 새로고침해 주세요.'};document.head.appendChild(s);
})();
'''.replace('%KEY%', KAKAO_JS)

def main_html(title, extra_bar='', search_ph='이름·주소로 찾기'):
    return (f'<section class="card tool"><h2>{title}</h2>'
            '<div class="mp-wrap"><div id="map" role="application" aria-label="지도"></div><p class="mp-hint" id="mp-hint">지도를 불러오는 중…</p></div>'
            f'<div class="pub-bar"><button type="button" class="me" id="pub-me">내 위치</button><select id="pub-sido" aria-label="지역"></select>{extra_bar}'
            f'<input class="q" id="pub-q" placeholder="{search_ph}" aria-label="찾기"></div>'
            '<div class="chips" id="pub-chips" role="group" aria-label="필터"></div><p class="pub-st" id="pub-st" aria-live="polite"></p>'
            '<ul class="pub-list" id="pub-list"></ul><button type="button" class="pub-more" id="pub-more" hidden>더 보기</button>%SRC%</section>\n')

def page(slug, dirn, crumb, title, desc, h1, lead, list_title, cfg_js, src, explain, faq, rel, extra_bar='', search_ph='이름·주소로 찾기', extra_css=''):
    mh = main_html(list_title, extra_bar, search_ph).replace('%SRC%', f'<p class="pub-src">자료: {src}</p>')
    if explain: mh += f'<section class="card"><h2>알아두면 좋아요</h2><ul class="xp">{explain}</ul></section>\n'
    k = max(cfg_js.rfind('({key'), cfg_js.rfind('({single'))
    pre, obj = cfg_js[:k], cfg_js[k:]
    js = '<script>\nwindow.PUBCFG=(function(){' + pre.replace(' ;', ';') + '\nreturn ' + obj + ';})();\n' + ENGINE + '</script>\n'
    shell(slug, title, desc, h1, lead, '<style id="hl-mt">' + COMMON_CSS + PUB_CSS + extra_css + '</style>\n', mh, js, faq, crumb=crumb, dirn=dirn, rel=rel)

# ── 공통: 영업시간 (HHMM 문자열) ──
HOURS_JS = r'''function hm(x){x=String(x||'').replace(/[^0-9]/g,'');return x.length>=3?+x:null}
function openNow(s,c,now){s=hm(s);c=hm(c);if(s==null||c==null)return null;if(c<=s)c+=2400;return (now>=s&&now<c)||(now+2400>=s&&now+2400<c)}
function nowHM(){var d=new Date();return d.getHours()*100+d.getMinutes()}
function t4(x){x=String(x||'').replace(/[^0-9]/g,'');if(x.length<3)return '';x=('0'+x).slice(-4);return x.slice(0,2)+':'+x.slice(2)}'''

MED = ('병원·건강', '/medical/'); DRV = ('자동차·지도', '/drive/'); LIFE = ('생활·행정', '/life/'); TRIP = ('여행', '/trip/')
R_MED = [('/medical/pharmacy-open.html', '지금 문 연 약국', '밤·주말·공휴일 영업 약국 지도'), ('/medical/emergency-room.html', '응급실 실시간 병상', '근처 응급실 빈 병상 확인')]
R_DRV = [('/drive/gas-station.html', '싼 주유소 지도', '시군구별 최저가 주유소'), ('/drive/ev-charger.html', '전기차 충전소 지도', '지금 빈 충전기 확인'),
         ('/drive/parking.html', '공영·무료 주차장', '요금·운영시간 지도'), ('/drive/rest-area.html', '고속도로 휴게소', '대표 메뉴·기름값'), ('/life/taxi-fare.html', '택시비·통행료 계산기', '택시 vs 내 차 비용')]
R_LIFE = [('/life/toilet.html', '근처 공중화장실', '개방시간·장애인 화장실'), ('/life/air-quality.html', '우리 동네 미세먼지', '측정소별 실시간')]
R_TRIP = [('/trip/festival.html', '이번 주말 축제 지도', '지금 열리는 축제·행사'), ('/trip/camping.html', '캠핑장 찾기', '글램핑·카라반·반려견')]

def build():
    # 1) 지금 문 연 약국
    page('pharmacy-open', 'medical', MED, '지금 문 연 약국 찾기 · 밤·주말·공휴일 영업 약국 지도 | 홍라이프 도구',
         '내 위치 근처에서 지금 영업 중인 약국을 지도로 찾아요. 요일별 영업시간, 밤늦게·일요일·공휴일 여는 약국, 전화·길찾기까지. 국립중앙의료원 약국 정보 기준.',
         '지금 문 연 약국', '내 위치 근처에서 지금 열려 있는 약국을 가까운 순으로 보여줘요. 밤늦게나 일요일·공휴일에 여는 약국도 바로 걸러 볼 수 있어요.', '근처 약국',
         HOURS_JS + r''' ;({key:'pharmacy',rv:1,hint:'‘내 위치’를 누르면 지금 문 연 약국이 나와요',
          filters:[['지금 영업 중',function(o){return isOpen(o)===true}],['전체',null],['밤 10시 이후',function(o){var h=today(o);return h&&hm(h[1])>=2200||(h&&hm(h[1])<hm(h[0]))}],['일요일 영업',function(o){return !!hm(o.hours[6][0])}],['공휴일 영업',function(o){return !!hm(o.hours[7][0])}]],
          color:function(o){return isOpen(o)?'#12B886':'#ADB5BD'},
          card:function(o){var h=today(o),op=isOpen(o);return '<p class="a">'+PUB.esc(o.addr)+'</p><div class="m">'+(op===true?'<span class="tg g">영업 중</span>':op===false?'<span class="tg r">영업 끝</span>':'<span class="tg">시간 정보 없음</span>')+(h?'<span class="tg">오늘 '+t4(h[0])+'~'+t4(h[1])+'</span>':'')+(hm(o.hours[7][0])?'<span class="tg b">공휴일 '+t4(o.hours[7][0])+'~'+t4(o.hours[7][1])+'</span>':'')+'</div>'}})'''
         .replace(';({', 'function today(o){var d=new Date().getDay();return o.hours[d===0?6:d-1]}\nfunction isOpen(o){var h=today(o);return h?openNow(h[0],h[1],nowHM()):null}\n({'),
         '국립중앙의료원 전국 약국 정보 (매일 갱신)',
         '<li>영업시간은 약국이 신고한 요일별 시간이에요. 명절·공휴일에는 실제와 다를 수 있으니 <b>전화로 한 번 확인</b>하세요.</li><li>‘공휴일 영업’은 공휴일 시간을 따로 신고한 약국이에요. 설·추석 연휴에는 지자체가 지정한 당번 약국을 함께 확인하세요.</li><li>급하게 약이 필요하면 편의점 안전상비의약품(해열제·감기약·소화제 등)도 살 수 있어요.</li>',
         [('지금 영업 중인 약국은 어떻게 확인하나요?', '‘내 위치’를 누르면 근처 약국을 가까운 순으로 보여주고, 오늘 요일의 영업시간으로 지금 열려 있는지 표시해요. 초록색 표시가 지금 영업 중인 곳이에요.'),
          ('일요일이나 공휴일에 여는 약국도 나오나요?', '네. ‘일요일 영업’, ‘공휴일 영업’ 필터를 누르면 그날 영업시간을 신고한 약국만 보여줘요. 명절에는 실제 영업 여부를 전화로 확인하세요.'),
          ('영업시간이 틀리면 어떻게 하나요?', '약국이 신고한 시간이라 실제와 다를 수 있어요. 방문 전에 전화 버튼으로 확인하는 게 가장 정확해요.')], R_MED + R_LIFE)
    # 2) 응급실
    page('emergency-room', 'medical', MED, '응급실 실시간 빈 병상 · 근처 응급실 지도 | 홍라이프 도구',
         '내 위치 근처 응급실과 지금 남은 응급실 병상 수를 지도로 확인해요. 권역·지역응급의료센터 구분, 응급실 전화, 길찾기까지. 국립중앙의료원 실시간 자료 기준.',
         '응급실 실시간 병상', '근처 응급실과 지금 남아 있는 응급실 병상 수를 함께 보여줘요. 위급할 때는 먼저 119에 전화하세요.', '근처 응급실',
         r'''({key:'er',hint:'위급하면 먼저 119에 전화하세요',
          filters:[['전체',null],['빈 병상 있음',function(o){return +o.beds>0}],['권역·지역센터',function(o){return /권역|지역응급의료센터/.test(o.level)}]],
          color:function(o){return o.beds==null||o.beds===''?'#ADB5BD':(+o.beds>0?'#12B886':'#F04452')},
          card:function(o){var b=o.beds;return '<p class="a">'+PUB.esc(o.addr)+'</p><div class="m">'+(b==null||b===''?'<span class="tg">병상 정보 없음</span>':(+b>0?'<span class="tg g">응급실 빈 병상 '+b+'</span>':'<span class="tg r">빈 병상 없음 ('+b+')</span>'))+(o.level?'<span class="tg b">'+PUB.esc(o.level)+'</span>':'')+(o.bedtime?'<span class="tg">'+String(o.bedtime).replace(/^(\d{4})(\d\d)(\d\d)(\d\d)(\d\d).*/,'$2/$3 $4:$5')+' 기준</span>':'')+'</div>'}})''',
         '국립중앙의료원 응급의료기관·실시간 가용병상 (매시간 갱신)',
         '<li><b>위급하면 먼저 119</b>에 전화하세요. 구급대가 받을 수 있는 병원을 찾아 이송해요.</li><li>병상 수는 병원이 입력한 실시간 값이라 몇 분 사이에도 바뀌어요. 출발 전에 응급실 전화로 확인하세요.</li><li>경증이면 응급실보다 가까운 달빛어린이병원·야간 진료 의원이 빠를 수 있어요.</li>',
         [('빈 병상 숫자는 얼마나 정확한가요?', '병원이 국가응급진료정보망에 입력한 값을 매시간 받아와요. 실제 상황은 몇 분 사이에도 바뀌니 출발 전 전화 확인이 가장 정확해요.'),
          ('권역·지역응급의료센터는 무엇인가요?', '중증 응급환자를 주로 보는 큰 병원 응급실이에요. 지역응급의료기관은 그보다 작은 규모예요.')], R_MED + R_LIFE)
    # 3) 전기차 충전소
    page('ev-charger', 'drive', DRV, '전기차 충전소 지도 · 지금 빈 충전기·급속 충전 찾기 | 홍라이프 도구',
         '내 근처 전기차 충전소를 지도로 찾고 지금 비어 있는 충전기 수, 급속·완속, 이용시간, 주차 무료 여부를 확인해요. 환경부 충전소 정보 기준.',
         '전기차 충전소 지도', '근처 충전소에서 지금 비어 있는 충전기가 몇 대인지, 급속 충전이 되는지 한눈에 봐요.', '근처 충전소',
         r'''({key:'ev',filters:[['전체',null],['지금 빈 충전기',function(o){return o.avail>0}],['급속 빈 충전기',function(o){return o.fastAvail>0}],['주차 무료',function(o){return o.parkFree==='Y'}],['누구나 이용',function(o){return o.limit!=='Y'}]],
          color:function(o){return o.avail>0?'#12B886':'#F04452'},
          card:function(o){return '<p class="a">'+PUB.esc(o.addr)+'</p><div class="m"><span class="tg '+(o.avail>0?'g':'r')+'">빈 충전기 '+o.avail+'/'+o.total+'</span>'+(o.fast?'<span class="tg b">급속 '+o.fastAvail+'/'+o.fast+'</span>':'<span class="tg">완속만</span>')+(o.parkFree==='Y'?'<span class="tg y">주차 무료</span>':'')+(o.limit==='Y'?'<span class="tg">이용 제한</span>':'')+'</div><p class="a">'+PUB.esc(o.op||'')+(o.time?' · '+PUB.esc(o.time):'')+'</p>'}})''',
         '환경부 전기자동차 충전소 정보 (오전 8시~오후 6시 30분마다, 그 밖에는 3시간마다 갱신)',
         '<li>빈 충전기 수는 충전기가 보낸 마지막 상태라 실제와 조금 다를 수 있어요.</li><li>‘이용 제한’은 아파트·회사 등 거주자나 직원만 쓸 수 있는 곳이에요.</li><li>급속은 50kW 이상이거나 DC 콤보·차데모 충전기예요.</li>',
         [('빈 충전기 숫자는 실시간인가요?', '환경부 충전기 상태 정보를 오전 8시~오후 6시에는 30분마다, 그 밖의 시간에는 3시간마다 받아와요. 실시간은 아니에요. 바로 가기 전에는 충전 앱에서 한 번 더 확인하세요.'), ('누구나 이용할 수 있나요?', '‘누구나 이용’ 필터를 켜면 거주자·직원 전용(이용 제한) 충전소를 뺀 곳만 보여줘요.')], R_DRV)
    # 4) 주차장
    page('parking', 'drive', DRV, '공영·무료 주차장 지도 · 요금·운영시간 한눈에 | 홍라이프 도구',
         '근처 공영주차장과 무료 주차장을 지도로 찾고 기본요금, 추가요금, 1일 주차권, 운영시간, 주차면 수를 확인해요. 전국주차장정보 표준데이터 기준.',
         '공영·무료 주차장 지도', '목적지 근처 공영주차장과 무료 주차장을 요금과 운영시간까지 함께 보여줘요.', '근처 주차장',
         r'''({key:'parking',filters:[['전체',null],['무료',function(o){return /무료/.test(o.fee)}],['공영',function(o){return /공영/.test(o.kind)}],['노외(건물·부지)',function(o){return /노외/.test(o.type)}]],
          color:function(o){return /무료/.test(o.fee)?'#12B886':'#3182F6'},
          card:function(o){var fee=/무료/.test(o.fee)?'<span class="tg g">무료</span>':(o.baseWon?'<span class="tg b">'+o.baseMin+'분 '+(+o.baseWon).toLocaleString()+'원</span>'+(o.addWon?'<span class="tg">추가 '+o.addMin+'분 '+(+o.addWon).toLocaleString()+'원</span>':''):'<span class="tg">'+PUB.esc(o.fee||'요금 정보 없음')+'</span>');
           var h=o.hours&&o.hours[0];return '<p class="a">'+PUB.esc(o.addr)+'</p><div class="m">'+fee+(o.day?'<span class="tg y">1일 '+(+o.day).toLocaleString()+'원</span>':'')+(o.spaces?'<span class="tg">'+o.spaces+'면</span>':'')+'<span class="tg">'+PUB.esc(o.kind||'')+' '+PUB.esc(o.type||'')+'</span>'+(h&&h[0]?'<span class="tg">평일 '+h[0]+'~'+h[1]+'</span>':'')+'</div>'}})''',
         '전국주차장정보 표준데이터 (매주 갱신)',
         '<li>요금은 지자체가 등록한 기본 요금이에요. 경차·친환경차·장애인 차량은 보통 50% 이상 감면돼요.</li><li>노상은 길가 주차장, 노외는 별도 부지·건물 주차장이에요.</li>',
         [('요금이 실제와 다를 수 있나요?', '지자체가 등록한 표준데이터라 최근 바뀐 요금은 반영이 늦을 수 있어요. 현장 안내판을 확인하세요.'), ('무료 주차장만 볼 수 있나요?', '‘무료’ 필터를 누르면 요금 정보가 무료로 등록된 곳만 보여줘요.')], R_DRV)
    # 5) 주유소
    page('gas-station', 'drive', DRV, '싼 주유소 찾기 · 우리 동네 최저가 주유소 지도 (휘발유·경유) | 홍라이프 도구',
         '시군구별 최저가 주유소를 지도로 보고 휘발유·경유 가격을 비교해요. 시도 평균 가격과 비교, 길찾기까지. 오피넷 유가 정보 기준.',
         '싼 주유소 지도', '동네별로 가장 싼 주유소를 가격순으로 보여줘요. 휘발유와 경유를 골라 비교해요.', '최저가 주유소',
         r'''({key:'fuel',note:'시군구별 최저가 10곳씩',filters:[['휘발유 싼 순',function(o){return !!o.gasoline}],['경유 싼 순',function(o){return !!o.diesel}],['가까운 순',null]],
          sort:function(L){var b=document.querySelector('#pub-chips [aria-pressed=true]'),t=b?b.textContent:'';if(/휘발유/.test(t)){L.sort(function(a,b){return (a.gasoline-b.gasoline)||(a._d-b._d)});L.splice(0,L.length,...L.filter(function(o){return o._d<15}).concat(L.filter(function(o){return o._d>=15})));return true}
           if(/경유/.test(t)){L.sort(function(a,b){return (a.diesel-b.diesel)||(a._d-b._d)});L.splice(0,L.length,...L.filter(function(o){return o._d<15}).concat(L.filter(function(o){return o._d>=15})));return true}return false},
          color:function(o){return '#F59F00'},
          card:function(o){var B={SKE:'SK에너지',GSC:'GS칼텍스',HDO:'HD현대오일뱅크',SOL:'S-OIL',RTE:'자영알뜰',RTX:'고속도로알뜰',NHO:'농협알뜰',ETC:'자가상표',E1G:'E1',SKG:'SK가스'};
           return '<p class="a">'+PUB.esc(o.addr)+'</p><div class="m">'+(o.gasoline?'<span class="tg y">휘발유 '+(+o.gasoline).toLocaleString()+'원</span>':'')+(o.diesel?'<span class="tg b">경유 '+(+o.diesel).toLocaleString()+'원</span>':'')+'<span class="tg">'+PUB.esc(B[o.brand]||o.brand||'')+'</span><span class="tg">'+PUB.esc(o.area||'')+'</span></div>'}})''',
         '오피넷 유가 정보 (6시간마다 갱신)',
         '<li>가격순은 지도 가운데(또는 내 위치)에서 15km 안의 주유소를 먼저 싼 순으로 보여줘요.</li><li>가격은 주유소가 오피넷에 보고한 값이라 실제와 몇 원 차이가 날 수 있어요.</li><li>택시비·통행료 계산기에서 이 가격을 넣으면 내 차 기름값을 더 정확하게 계산할 수 있어요.</li>',
         [('얼마나 자주 바뀌나요?', '오피넷 가격을 6시간마다 받아와요. 주유소 가격은 보통 하루 한두 번 바뀌어요.'), ('모든 주유소가 나오나요?', '시군구마다 휘발유·경유 최저가 10곳씩만 모아 보여줘요. 가장 싼 곳을 찾는 데 맞춘 목록이에요.')], R_DRV)
    # 6) 휴게소
    page('rest-area', 'drive', DRV, '고속도로 휴게소 대표 메뉴·기름값 지도 | 홍라이프 도구',
         '고속도로 휴게소 위치를 지도로 보고 대표 메뉴와 가격, 휴게소 주유소 휘발유·경유·LPG 가격을 확인해요. 한국도로공사 자료 기준.',
         '고속도로 휴게소 맛집·기름값', '경로에 있는 휴게소의 대표 메뉴와 가격, 주유소 기름값을 지도로 한눈에 봐요.', '근처 휴게소',
         r'''({single:'rest.json',filters:[['전체',null],['주유소 있음',function(o){return !!o.oil}],['대표 메뉴 있음',function(o){return o.foods&&o.foods.length}]],
          text:function(o){return (o.route||'')+' '+(o.foods||[]).map(function(f){return f[0]}).join(' ')},color:function(o){return '#7950F2'},
          card:function(o){var fd=(o.foods||[]).slice(0,4).map(function(f){return '<span class="tg'+(f[2]==='Y'?' y':'')+'">'+PUB.esc(f[0])+(f[1]?' '+(+String(f[1]).replace(/[^0-9]/g,'')).toLocaleString()+'원':'')+'</span>'}).join('');
           var ol=o.oil?'<span class="tg y">휘발유 '+PUB.esc(o.oil[0])+'</span><span class="tg b">경유 '+PUB.esc(o.oil[1])+'</span>'+(o.oil[2]&&o.oil[2]!=='X'?'<span class="tg">LPG '+PUB.esc(o.oil[2])+'</span>':''):'';
           return '<p class="a">'+PUB.esc(o.route||'')+'</p>'+(fd?'<div class="m">'+fd+'</div>':'')+(ol?'<div class="m">'+ol+'</div>':'')}})''',
         '한국도로공사 휴게소 위치·대표음식·주유소 가격 (6시간마다 갱신)',
         '<li>노란색 메뉴는 휴게소가 정한 대표 메뉴(베스트 푸드)예요.</li><li>검색창에 노선 이름(예: 경부선)이나 메뉴(예: 호두과자)를 넣으면 걸러 볼 수 있어요.</li>',
         [('메뉴 가격은 최신인가요?', '한국도로공사가 공개한 휴게소 대표 음식 자료를 6시간마다 받아와요. 현장 가격과 다를 수 있어요.')], R_DRV, search_ph='휴게소·노선·메뉴로 찾기')
    # 7) 공중화장실
    page('toilet', 'life', LIFE, '근처 공중화장실 찾기 · 개방시간·장애인 화장실 지도 | 홍라이프 도구',
         '급할 때 내 위치 근처 공중화장실을 지도로 찾아요. 개방시간, 장애인 화장실, 기저귀 교환대, 비상벨 여부까지. 전국공중화장실 표준데이터 기준.',
         '근처 공중화장실', '급할 때 내 위치에서 가장 가까운 공중화장실을 찾아요. 개방시간과 장애인 화장실, 기저귀 교환대도 함께 보여줘요.', '가까운 화장실',
         r'''({key:'toilet',hint:'‘내 위치’를 누르면 가장 가까운 화장실이 나와요',filters:[['전체',null],['24시간',function(o){return /24|상시/.test(o.open)}],['장애인 화장실',function(o){return o.handicap==1}],['기저귀 교환대',function(o){return o.diaper==='Y'}],['비상벨',function(o){return o.bell==='Y'}]],
          color:function(o){return /24|상시/.test(o.open)?'#12B886':'#3182F6'},
          card:function(o){return '<p class="a">'+PUB.esc(o.addr)+'</p><div class="m">'+(o.open?'<span class="tg '+(/24|상시/.test(o.open)?'g':'')+'">'+PUB.esc(o.open)+'</span>':'')+(o.handicap==1?'<span class="tg b">장애인 화장실</span>':'')+(o.diaper==='Y'?'<span class="tg y">기저귀 교환대</span>':'')+(o.bell==='Y'?'<span class="tg">비상벨</span>':'')+'</div>'}})''',
         '전국공중화장실 표준데이터 (매주 갱신)',
         '<li>지하철역·공원·관공서 화장실은 건물 개방시간에만 쓸 수 있어요.</li><li>밤에는 ‘24시간’ 필터로 상시 개방 화장실을 먼저 찾으세요.</li>', [('밤에도 쓸 수 있나요?', '‘24시간’ 필터를 누르면 개방시간이 24시간·상시로 등록된 곳만 보여줘요.')], R_LIFE + R_MED)
    # 8) 축제
    page('festival', 'trip', TRIP, '이번 주말 축제 지도 · 지금 열리는 축제·행사 찾기 | 홍라이프 도구',
         '내 위치 근처에서 지금 열리고 있거나 곧 열리는 축제·행사를 지도로 찾아요. 기간, 장소, 사진, 길찾기까지. 한국관광공사 관광정보 기준.',
         '이번 주말 축제 지도', '지금 열리고 있는 축제와 곧 열릴 행사를 가까운 순으로 보여줘요. 이번 주말에 갈 만한 곳을 바로 골라 보세요.', '근처 축제·행사',
         r'''({key:'festival',filters:[['진행 중',function(o){var t=td();return o.start<=t&&o.end>=t}],['이번 주말',function(o){var w=wk();return o.start<=w[1]&&o.end>=w[0]}],['전체',null]],
          color:function(o){var t=td();return o.start<=t&&o.end>=t?'#F04452':'#F59F00'},
          card:function(o){var f=function(x){return x?x.slice(4,6)+'.'+x.slice(6,8):''},t=td(),on=o.start<=t&&o.end>=t;return '<p class="a">'+PUB.esc(o.addr)+'</p><div class="m">'+(on?'<span class="tg r">진행 중</span>':'<span class="tg y">'+(+o.start.slice(4,6))+'월 '+(+o.start.slice(6,8))+'일 시작</span>')+'<span class="tg">'+f(o.start)+' ~ '+f(o.end)+'</span></div>'+(o.img?'<img class="th" loading="lazy" alt="" src="'+PUB.esc(String(o.img).replace(/^http:/,'https:'))+'">':'')},
          links:function(o){return '<a target="_blank" rel="noopener" href="https://korean.visitkorea.or.kr/detail/fes_detail.do?cotid='+encodeURIComponent(o.id)+'">자세히</a><a target="_blank" rel="noopener" href="/trip/">근처 숙소</a>'}})'''
         .replace("({key:'festival'", "function td(){var d=new Date();return d.getFullYear()+('0'+(d.getMonth()+1)).slice(-2)+('0'+d.getDate()).slice(-2)}\nfunction ymd(d){return d.getFullYear()+('0'+(d.getMonth()+1)).slice(-2)+('0'+d.getDate()).slice(-2)}\nfunction wk(){var d=new Date(),s=new Date(d),k=d.getDay();s.setDate(d.getDate()+((6-k+7)%7));var e=new Date(s);e.setDate(s.getDate()+1);if(k===0){s=new Date(d);e=new Date(d)}return [ymd(s),ymd(e)]}\n({key:'festival'"),
         '한국관광공사 국문 관광정보 (매일 갱신)',
         '<li>일정과 장소는 주최 측 사정으로 바뀔 수 있어요. 출발 전에 ‘자세히’에서 확인하세요.</li><li>사진은 한국관광공사가 공개한 축제 사진이에요.</li>',
         [('축제 정보는 얼마나 자주 바뀌나요?', '한국관광공사 자료를 매일 받아와요. 끝난 축제는 자동으로 빠져요.')], R_TRIP)
    # 9) 캠핑장
    page('camping', 'trip', TRIP, '캠핑장 찾기 지도 · 글램핑·카라반·반려견 동반 | 홍라이프 도구',
         '전국 캠핑장을 지도로 찾아요. 일반야영장·자동차야영장·글램핑·카라반 구분, 반려견 동반 가능 여부, 예약 링크, 사진까지. 고캠핑 자료 기준.',
         '캠핑장 찾기', '가까운 캠핑장을 종류별로 골라 보고, 반려견 동반이 되는지와 예약 링크까지 한 번에 확인해요.', '근처 캠핑장',
         r'''({key:'camping',filters:[['전체',null],['글램핑',function(o){return /글램핑/.test(o.type)}],['카라반',function(o){return /카라반/.test(o.type)}],['자동차야영장',function(o){return /자동차/.test(o.type)}],['반려견 동반',function(o){return /가능/.test(o.pet)&&!/불가/.test(o.pet)}]],
          color:function(o){return '#2B8A3E'},text:function(o){return (o.type||'')+' '+(o.intro||'')},
          card:function(o){return '<p class="a">'+PUB.esc(o.addr)+'</p>'+(o.intro?'<p class="a">'+PUB.esc(o.intro)+'</p>':'')+'<div class="m">'+(o.type||'').split(',').filter(Boolean).map(function(t){return '<span class="tg b">'+PUB.esc(t)+'</span>'}).join('')+(/가능/.test(o.pet)&&!/불가/.test(o.pet)?'<span class="tg y">반려견 '+PUB.esc(o.pet)+'</span>':'')+'</div>'+(o.img?'<img class="th" loading="lazy" alt="" src="'+PUB.esc(String(o.img).replace(/^http:/,'https:'))+'">':'')},
          links:function(o){return o.url?'<a target="_blank" rel="noopener" href="'+PUB.esc(o.url)+'">예약·홈페이지</a>':''}})''',
         '한국관광공사 고캠핑 (매주 갱신)', '<li>예약 방법과 요금은 캠핑장마다 달라요. ‘예약·홈페이지’에서 확인하세요.</li>',
         [('반려견 동반 캠핑장만 볼 수 있나요?', '‘반려견 동반’ 필터를 누르면 동반 가능으로 등록된 캠핑장만 보여줘요. 크기 제한 등 조건은 캠핑장에 확인하세요.')], R_TRIP)


AIR_MAIN = """<section class="card tool"><h2>측정소별 지금 미세먼지</h2>
<div class="pub-bar"><button type="button" class="me" id="a-me">내 위치</button><select id="a-sido" aria-label="지역"></select><input class="q" id="a-q" placeholder="동네·측정소 이름" aria-label="찾기"></div>
<div class="aq-sum" id="a-sum"></div><p class="pub-st" id="a-st" aria-live="polite"></p><ul class="aq" id="a-list"></ul>
<p class="pub-src">자료: 한국환경공단 에어코리아 실시간 측정 (매시간 갱신, 확정 전 자료)</p></section>
<section class="card"><h2>등급 기준</h2><ul class="xp"><li><b>미세먼지(PM10)</b> 좋음 0~30 · 보통 31~80 · 나쁨 81~150 · 매우나쁨 151 이상 (㎍/㎥)</li><li><b>초미세먼지(PM2.5)</b> 좋음 0~15 · 보통 16~35 · 나쁨 36~75 · 매우나쁨 76 이상 (㎍/㎥)</li><li>나쁨 이상이면 KF80 이상 마스크를 쓰고, 어린이·노약자는 바깥 활동을 줄이세요.</li></ul></section>
"""
AIR_CSS = """.aq-sum{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:12px}.aq-sum div{border-radius:14px;padding:14px;text-align:center;color:#fff}.aq-sum b{display:block;font-size:26px}.aq-sum span{font-size:13px;opacity:.95}
.aq{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}.aq li{display:grid;grid-template-columns:1fr auto auto;gap:8px;align-items:center;border:1px solid var(--line-s);border-radius:12px;padding:10px 12px;background:#fff}
.aq li b{font-size:15px;color:var(--head);word-break:keep-all}.aq li small{display:block;color:var(--muted);font-size:12px;font-weight:400}.aq .v{min-width:74px;text-align:center;border-radius:9px;padding:5px 6px;font-weight:800;font-size:13px;color:#fff;white-space:nowrap}
"""
AIR_JS = r"""<script>
(function(){var $=function(i){return document.getElementById(i)},SIDO=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주'],D=null;
var G=[['좋음','#3182F6'],['보통','#12B886'],['나쁨','#F59F00'],['매우나쁨','#F04452']];
function g10(v){v=+v;return isNaN(v)?-1:v<=30?0:v<=80?1:v<=150?2:3}function g25(v){v=+v;return isNaN(v)?-1:v<=15?0:v<=35?1:v<=75?2:3}
function badge(v,g,u){if(g<0)return '<span class="v" style="background:#ADB5BD">점검중</span>';return '<span class="v" style="background:'+G[g][1]+'">'+u+' '+v+'</span>'}
SIDO.forEach(function(s){var o=document.createElement('option');o.value=o.textContent=s;$('a-sido').appendChild(o)});
function render(){if(!D)return;var s=$('a-sido').value,q=$('a-q').value.trim(),C=D.cols,R=D.rows.map(function(r){var o={};C.forEach(function(c,i){o[c]=r[i]});return o}).filter(function(o){return o.sido===s&&(!q||o.station.indexOf(q)>=0)});
 var a10=R.map(function(o){return +o.pm10}).filter(function(x){return !isNaN(x)}),a25=R.map(function(o){return +o.pm25}).filter(function(x){return !isNaN(x)});
 var m10=a10.length?Math.round(a10.reduce(function(a,b){return a+b},0)/a10.length):null,m25=a25.length?Math.round(a25.reduce(function(a,b){return a+b},0)/a25.length):null;
 $('a-sum').innerHTML=m10==null?'':'<div style="background:'+G[g10(m10)][1]+'"><b>'+G[g10(m10)][0]+'</b><span>'+s+' 미세먼지 평균 '+m10+'</span></div><div style="background:'+G[g25(m25)][1]+'"><b>'+G[g25(m25)][0]+'</b><span>'+s+' 초미세먼지 평균 '+m25+'</span></div>';
 $('a-list').innerHTML=R.map(function(o){return '<li><b>'+o.station.replace(/[<>&]/g,'')+'<small>'+(o.time||'')+'</small></b>'+badge(o.pm10,g10(o.pm10),'미세')+badge(o.pm25,g25(o.pm25),'초미세')+'</li>'}).join('');
 $('a-st').textContent=R.length+'개 측정소 · '+D.updated+' 기준'}
fetch('/data/pub/air.json',{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){D=j;render()}).catch(function(){$('a-st').textContent='자료를 준비하고 있어요. 잠시 후 다시 들어와 주세요.'});
$('a-sido').onchange=render;$('a-q').oninput=render;
$('a-me').onclick=function(){if(!navigator.geolocation)return;$('a-st').textContent='내 위치를 찾는 중…';navigator.geolocation.getCurrentPosition(function(p){var s=document.createElement('script');s.src='https://dapi.kakao.com/v2/maps/sdk.js?appkey=%KEY%&autoload=false&libraries=services';s.onload=function(){kakao.maps.load(function(){new kakao.maps.services.Geocoder().coord2RegionCode(p.coords.longitude,p.coords.latitude,function(r,st){if(st!==kakao.maps.services.Status.OK||!r[0])return render();var n=r[0].region_1depth_name,x=SIDO.filter(function(k){return n.indexOf(k)===0||(k==='충북'&&n==='충청북도')||(k==='충남'&&n==='충청남도')||(k==='전북'&&/전북|전라북/.test(n))||(k==='전남'&&n==='전라남도')||(k==='경북'&&n==='경상북도')||(k==='경남'&&n==='경상남도')})[0];if(x)$('a-sido').value=x;$('a-q').value='';render();var d=(r[0].region_3depth_name||'').replace(/[0-9]+동$|동$|읍$|면$/,'');if(d&&D&&D.rows.some(function(z){return z[1].indexOf(d)>=0})){$('a-q').value=d;render()}})})};document.head.appendChild(s)},function(){render()})}})();
</script>
""".replace('%KEY%', KAKAO_JS)

def build_air():
    shell('air-quality', '우리 동네 미세먼지 · 초미세먼지 실시간 (측정소별) | 홍라이프 도구',
          '내 위치나 지역을 고르면 측정소별 실시간 미세먼지·초미세먼지 수치와 좋음·보통·나쁨 등급을 보여줘요. 에어코리아 실시간 자료 기준, 매시간 갱신.',
          '우리 동네 미세먼지', '지금 우리 동네 미세먼지와 초미세먼지를 측정소별로 보여줘요. 지역 평균 등급도 한눈에 확인해요.',
          '<style id="hl-mt">' + COMMON_CSS + PUB_CSS + AIR_CSS + '</style>\n', AIR_MAIN, AIR_JS,
          [('수치는 얼마나 자주 바뀌나요?', '에어코리아 실시간 측정값을 매시간 받아와요. 확정 전 자료라 나중에 조금 바뀔 수 있어요.'), ('내 동네가 안 나와요', '측정소가 있는 동네 이름만 나와요. 가장 가까운 측정소나 지역 평균을 참고하세요.')],
          crumb=LIFE, dirn='life', rel=R_LIFE + R_MED)

if __name__ == '__main__':
    build(); build_air()
