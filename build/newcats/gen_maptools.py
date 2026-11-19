# 지도(카카오모빌리티 길찾기) 웹 도구 → overlay/life/*.html
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = open(os.path.join(ROOT, 'overlay/ipsi/pyeonip-2027.html'), encoding='utf-8').read()
PROXY = 'https://hl-route.a599307.workers.dev/'
KAKAO_JS = 'c4a8d8392dd6a362db17cc44e5ae398b'

REL = [('/life/taxi-fare.html', '택시비·통행료·기름값 계산기', '택시 vs 내 차 비용 비교'), ('/life/midpoint.html', '중간지점 찾기', '친구들과 만날 곳 추천 + 공유 카드'), ('/life/route-navi.html', '경유지 많은 노선 내비', '정류장 30곳 넘어도 순서대로 안내')]

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def shell(slug, title, desc, h1, lead, css, main_html, js, faq, crumb=('자동차·지도', '/drive/'), dirn='life', rel=None):
    url = f'https://honglife.co.kr/{dirn}/{slug}.html'
    rel = REL if rel is None else rel
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": h1, "url": url, "applicationCategory": "TravelApplication", "operatingSystem": "Any", "inLanguage": "ko",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": "https://honglife.co.kr/"},
         {"@type": "ListItem", "position": 2, "name": crumb[0], "item": "https://honglife.co.kr" + crumb[1]},
         {"@type": "ListItem", "position": 3, "name": h1, "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    i_ld = base.find('<script type="application/ld'); i_st = base.find('<style', i_ld); i_ste = base.find('</style>', i_st) + len('</style>\n')
    i_main = base.find('<main'); i_ft = base.find('<footer')
    head = base[:i_ld]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', head)
    for prop in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + prop + r' content=")[^"]*', lambda m: m.group(1) + esc(desc), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(title), head)
    head = head.replace('https://honglife.co.kr/ipsi/pyeonip-2027.html', url)
    head = head.replace('<meta property="og:url" content="https://honglife.co.kr/ipsi/">', f'<meta property="og:url" content="{url}">')
    faq_html = ''.join(f'<dt>{esc(q)}</dt><dd>{esc(a)}</dd>' for q, a in faq)
    main = (f'<main class="wrap wide"><header class="top"><p class="crumb"><a href="/">홈</a> › <a href="{crumb[1]}">{crumb[0]}</a></p>'
            f'<h1>{h1}</h1><p class="lead">{lead}</p></header>\n' + main_html +
            f'<section class="card"><h2>자주 묻는 질문</h2><dl class="pe-faq">{faq_html}</dl></section>\n'
            '<section class="card rel"><h2>함께 쓰면 좋은 도구</h2><ul class="tlist">'
            + ''.join(f'<li><a href="{u}"><b>{n}</b><span>{d}</span></a></li>' for u, n, d in rel if u != f'/{dirn}/{slug}.html') +
            f'<li><a href="{crumb[1]}"><b>{crumb[0]} 도구 모음</b><span>{crumb[0]} 도구 전체 보기</span></a></li></ul></section>\n</main>\n')
    out = (head + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + css
           + base[i_ste:i_main] + main + js + base[i_ft:])
    out = out.replace('<a href="/ipsi/">입시</a>', f'<a href="{crumb[1]}">{crumb[0]}</a>')
    os.makedirs(os.path.join(ROOT, f'overlay/{dirn}'), exist_ok=True); open(os.path.join(ROOT, f'overlay/{dirn}/{slug}.html'), 'w', encoding='utf-8').write(out)
    print('wrote', slug, len(out))

# 공통 지도 + 장소 검색 + 카카오 길찾기 (전역 HLMAP)
COMMON_CSS = '''
.mp-wrap{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line-s);background:#EEF1F5}
#map{width:100%;height:min(56vh,440px)}
#map svg,#map img{max-width:none!important;max-height:none!important}
.mp-hint{position:absolute;left:10px;top:10px;z-index:3;background:rgba(255,255,255,.95);border-radius:10px;padding:6px 10px;font-size:13px;font-weight:700;color:var(--head);box-shadow:0 1px 4px rgba(0,0,0,.12);max-width:calc(100% - 70px)}
.pt{display:grid;grid-template-columns:auto 1fr auto;gap:8px;align-items:center;margin-top:10px}
.pt .dot{width:30px;height:30px;border-radius:50%;color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:14px}
.pt input{font:inherit;font-size:16px;padding:10px 12px;border:1px solid var(--line-s);border-radius:10px;min-height:44px;width:100%;box-sizing:border-box;background:#fff}
.pt input.on{border-color:var(--acc);box-shadow:0 0 0 3px rgba(49,130,246,.15)}
.pt button{font:inherit;font-size:13.5px;font-weight:700;border:1px solid var(--line-s);background:#fff;border-radius:10px;min-height:44px;padding:0 10px;cursor:pointer;white-space:nowrap}
.pt button[aria-pressed=true]{background:var(--acc);border-color:var(--acc);color:#fff}
.sug{list-style:none;margin:4px 0 0 38px;padding:0;border:1px solid var(--line-s);border-radius:10px;background:#fff;max-height:240px;overflow:auto}
.sug li button{display:block;width:100%;text-align:left;padding:9px 12px;border:0;background:none;font:inherit;font-size:14.5px;cursor:pointer;border-top:1px solid var(--line-s)}
.sug li:first-child button{border-top:0}.sug li button small{display:block;color:var(--muted);font-size:12px;margin-top:2px}
.sug li button:hover,.sug li button:focus{background:#F4F7FB}
.opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:12px}
.opts label{display:flex;flex-direction:column;gap:5px;font-size:13.5px;font-weight:700;color:var(--head)}
.opts select,.opts input[type=number]{font:inherit;font-size:16px;padding:9px 10px;border:1px solid var(--line-s);border-radius:10px;min-height:44px;width:100%;box-sizing:border-box;background:#fff}
.opts .ck{flex-direction:row;align-items:center;gap:8px;min-height:44px}.opts .ck input{width:20px;height:20px}
.go-btn{display:block;width:100%;margin-top:14px;min-height:52px;border:0;border-radius:14px;background:var(--acc);color:#fff;font:inherit;font-size:17px;font-weight:800;cursor:pointer}
.go-btn:disabled{background:#B0B8C1;cursor:default}
.tfr{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:14px}
.tfr div{background:#F4F7FB;border-radius:12px;padding:12px 6px;text-align:center}
.tfr b{display:block;font-size:21px;white-space:nowrap;color:var(--head);line-height:1.25;font-variant-numeric:tabular-nums;word-break:keep-all}
.tfr span{display:block;font-size:12.5px;color:var(--muted);margin-top:3px}
.tfr .big{grid-column:span 3;background:#0B5ED7}.tfr .big b,.tfr .big span{color:#fff}.tfr .big b{font-size:28px}
.tfm{font-size:13.5px;line-height:1.6;margin:10px 0 0;color:var(--ink)}
.tfm.err{color:#C92A2A;font-weight:700}
.ext{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.ext a{flex:1 1 140px;text-align:center;padding:12px;border-radius:12px;background:#FEE500;color:#191919;font-weight:800;text-decoration:none;font-size:14.5px}
.ext a.n{background:#03C75A;color:#fff}
.pe-faq dt{font-weight:700;margin-top:12px;color:var(--head)}.pe-faq dd{margin:4px 0 0;line-height:1.65;color:var(--ink)}
@media(max-width:520px){.tfr b{font-size:16.5px;letter-spacing:-.3px}.tfr .big b{font-size:24px}#map{height:46vh}}
'''

COMMON_JS = r'''
window.HLMAP=(function(){
var PROXY='%PROXY%',map=null,K=null,ready=[],ok=false,places=null,geo=null,line=null;
function onReady(f){ok?f():ready.push(f)}
(function(){var s=document.createElement('script');s.src='https://dapi.kakao.com/v2/maps/sdk.js?appkey=%KEY%&autoload=false&libraries=services';
 s.onload=function(){kakao.maps.load(function(){K=kakao.maps;places=new K.services.Places();geo=new K.services.Geocoder();ok=true;ready.forEach(function(f){f()})})};
 s.onerror=function(){var h=document.getElementById('mp-hint');if(h)h.textContent='지도를 불러오지 못했어요. 새로고침해 주세요.'};document.head.appendChild(s)})();
function init(el,lat,lng,lv){map=new K.Map(el,{center:new K.LatLng(lat,lng),level:lv||8});map.addControl(new K.ZoomControl(),K.ControlPosition.RIGHT);return map}
function pin(lat,lng,label,color){var svg='<svg xmlns="http://www.w3.org/2000/svg" width="34" height="43" viewBox="0 0 32 40"><path d="M16 39C16 39 3 24 3 15a13 13 0 0 1 26 0c0 9-13 24-13 24z" fill="'+color+'" stroke="#fff" stroke-width="2.4"/><text x="16" y="20" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" font-weight="800" fill="#fff">'+label+'</text></svg>';
 var img=new K.MarkerImage('data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg),new K.Size(34,43),{offset:new K.Point(17,42)});
 return new K.Marker({map:map,position:new K.LatLng(lat,lng),image:img})}
function search(q,cb){if(!places||!q)return cb([]);var c=map?map.getCenter():null;
 places.keywordSearch(q,function(d,st){cb(st===K.services.Status.OK?d.slice(0,7).map(function(p){return {name:p.place_name,addr:p.road_address_name||p.address_name,lat:+p.y,lng:+p.x}}):[])},c?{location:c,sort:K.services.SortBy.ACCURACY}:{})}
function nameAt(lat,lng,cb){if(!geo)return cb('지도에서 고른 곳');geo.coord2Address(lng,lat,function(r,st){if(st===K.services.Status.OK&&r[0]){var a=r[0].road_address||r[0].address;cb((r[0].road_address&&r[0].road_address.building_name)||a.address_name)}else cb('지도에서 고른 곳')})}
function route(o,d,w,opt){opt=opt||{};return fetch(PROXY,{method:'POST',headers:{'Content-Type':'application/json'},
 body:JSON.stringify({origin:{x:o.lng,y:o.lat},destination:{x:d.lng,y:d.lat},waypoints:(w||[]).map(function(p){return {x:p.lng,y:p.lat}}),priority:opt.priority||'RECOMMEND',avoid:opt.avoid&&opt.avoid.length?opt.avoid:undefined,summary:!!opt.summaryOnly})})
 .then(function(r){if(!r.ok)throw new Error('http '+r.status);return r.json()}).then(function(j){var R=j.routes&&j.routes[0];if(!R||R.result_code!==0)throw new Error(R?R.result_msg:'길찾기 실패');
  var pts=[];(R.sections||[]).forEach(function(sc){(sc.roads||[]).forEach(function(rd){for(var i=0;i<rd.vertexes.length;i+=2)pts.push([rd.vertexes[i+1],rd.vertexes[i]])})});
  return {distance:R.summary.distance,duration:R.summary.duration,taxi:(R.summary.fare||{}).taxi||0,toll:(R.summary.fare||{}).toll||0,pts:pts}})}
function draw(pts,color){if(line)line.setMap(null);if(!pts.length)return;var path=pts.map(function(p){return new K.LatLng(p[0],p[1])});
 line=new K.Polyline({map:map,path:path,strokeWeight:6,strokeColor:color||'#3182F6',strokeOpacity:.9});var b=new K.LatLngBounds();path.forEach(function(p){b.extend(p)});map.setBounds(b,40,40,40,40)}
function fmtMin(s){var m=Math.round(s/60);return m>=60?Math.floor(m/60)+'시간 '+(m%60)+'분':m+'분'}
function won(n){return Math.round(n).toLocaleString('ko-KR')+'원'}
function km(m){return (m/1000).toFixed(m<10000?1:0)+'km'}
return {onReady:onReady,init:init,pin:pin,search:search,nameAt:nameAt,route:route,draw:draw,fmtMin:fmtMin,won:won,km:km,get map(){return map},get K(){return K}};
})();
'''.replace('%PROXY%', PROXY).replace('%KEY%', KAKAO_JS)

# ───────────────── 1) 택시비·통행료·기름값 계산기 ─────────────────
TAXI_MAIN = '''<section class="card tool"><h2>출발지·도착지 고르기</h2>
<div class="mp-wrap"><div id="map" role="application" aria-label="지도"></div><p class="mp-hint" id="mp-hint">지도를 불러오는 중…</p></div>
<div class="pt"><span class="dot" style="background:#3182F6">출</span><input id="qa" placeholder="출발지 검색" autocomplete="off" aria-label="출발지"><button type="button" id="pa" aria-pressed="true">지도에서</button></div>
<ul class="sug" id="sa" hidden></ul>
<div class="pt"><span class="dot" style="background:#F04452">도</span><input id="qb" placeholder="도착지 검색" autocomplete="off" aria-label="도착지"><button type="button" id="pb" aria-pressed="false">지도에서</button></div>
<ul class="sug" id="sb" hidden></ul>
<div class="opts">
<label>경로<select id="pr"><option value="RECOMMEND">추천 경로</option><option value="TIME">빠른 길</option><option value="DISTANCE">짧은 길</option></select></label>
<label>택시 나눠 탈 사람<select id="ppl"><option>1</option><option>2</option><option>3</option><option>4</option></select></label>
<label>내 차 연비 (km/L)<input id="eff" type="number" inputmode="decimal" min="1" max="60" step="0.1" value="12"></label>
<label>기름값 (원/L)<input id="fuel" type="number" inputmode="numeric" min="500" max="5000" step="10" value="1700"></label>
<label class="ck"><input type="checkbox" id="toll">유료도로 피하기</label>
<label class="ck"><input type="checkbox" id="rt">왕복으로 계산</label>
</div>
<button class="go-btn" id="go" disabled>요금 계산하기</button>
<div id="out" hidden><div class="tfr">
<div class="big"><b id="o-taxi">–</b><span id="o-taxi-l">예상 택시비 (주간)</span></div>
<div><b id="o-dist">–</b><span>거리</span></div><div><b id="o-time">–</b><span>예상 시간</span></div><div><b id="o-toll">–</b><span>통행료</span></div>
<div><b id="o-gas">–</b><span>내 차 기름값</span></div><div><b id="o-car">–</b><span>내 차 합계</span></div><div><b id="o-per">–</b><span>택시 1인당</span></div>
</div>
<p class="tfm" id="o-msg"></p>
<div class="ext"><a id="o-kakao" target="_blank" rel="noopener">카카오맵으로 길안내</a><a class="n" id="o-naver" target="_blank" rel="noopener">네이버 지도로 보기</a></div></div>
<p class="tfm err" id="err" hidden></p>
<p class="tfm" style="color:var(--muted)">기름값 1,700원은 예시예요. 주유소 가격으로 바꿔 넣으면 바로 다시 계산돼요. 택시비는 카카오 길찾기가 알려 주는 주간 기본요금 기준이고, 심야·시계외 할증과 호출비는 빠져 있어요.</p>
</section>
<section class="card"><h2>이렇게 계산해요</h2><ul class="xp">
<li><b>거리·시간·택시비·통행료</b>는 카카오모빌리티 자동차 길찾기 결과를 그대로 써요. 실시간 교통이 반영된 지금 출발 기준이에요.</li>
<li><b>내 차 기름값</b> = 거리 ÷ 연비 × 기름값. 왕복을 고르면 거리·시간·요금을 모두 두 배로 계산해요.</li>
<li><b>내 차 합계</b> = 기름값 + 통행료. 주차비는 들어 있지 않아요.</li>
<li><b>택시 1인당</b>은 택시비를 나눠 탈 사람 수로 나눈 값이에요.</li></ul></section>
'''
TAXI_JS = '<script>\n' + COMMON_JS + r'''
(function(){
var H=HLMAP,A=null,B=null,mA=null,mB=null,pick='a',last=null;
var $=function(i){return document.getElementById(i)};
H.onReady(function(){H.init($('map'),37.5547,126.9707,8);$('mp-hint').textContent='출발지를 검색하거나 지도를 눌러 고르세요';
 kakao.maps.event.addListener(H.map,'click',function(e){var p=e.latLng;set(pick,{lat:p.getLat(),lng:p.getLng(),name:'지도에서 고른 곳'},true)})});
function setPick(w){pick=w;$('pa').setAttribute('aria-pressed',w=='a');$('pb').setAttribute('aria-pressed',w=='b');
 $('qa').classList.toggle('on',w=='a');$('qb').classList.toggle('on',w=='b');$('mp-hint').textContent=(w=='a'?'출발지':'도착지')+'를 지도에서 누르거나 검색하세요'}
function set(w,p,fromMap){if(w=='a'){A=p;if(mA)mA.setMap(null);mA=H.pin(p.lat,p.lng,'출','#3182F6');$('qa').value=p.name}else{B=p;if(mB)mB.setMap(null);mB=H.pin(p.lat,p.lng,'도','#F04452');$('qb').value=p.name}
 if(fromMap)H.nameAt(p.lat,p.lng,function(n){p.name=n;$(w=='a'?'qa':'qb').value=n});
 $('s'+w).hidden=true;if(w=='a'&&!B)setPick('b');$('go').disabled=!(A&&B);if(A&&B)calc()}
function bindSearch(w){var t=null,inp=$('q'+w),ul=$('s'+w);
 inp.addEventListener('focus',function(){setPick(w)});
 inp.addEventListener('input',function(){clearTimeout(t);var q=inp.value.trim();if(q.length<2){ul.hidden=true;return}
  t=setTimeout(function(){H.search(q,function(r){ul.innerHTML='';r.forEach(function(p){var li=document.createElement('li'),b=document.createElement('button');b.type='button';
   b.innerHTML='';b.textContent=p.name;var sm=document.createElement('small');sm.textContent=p.addr;b.appendChild(sm);
   b.onclick=function(){set(w,p);H.map.setCenter(new kakao.maps.LatLng(p.lat,p.lng))};li.appendChild(b);ul.appendChild(li)});ul.hidden=!r.length})},250)});}
bindSearch('a');bindSearch('b');$('pa').onclick=function(){setPick('a')};$('pb').onclick=function(){setPick('b')};setPick('a');
function show(){if(!last)return;var r=$('rt').checked?2:1,eff=Math.max(1,parseFloat($('eff').value)||12),fuel=Math.max(0,parseFloat($('fuel').value)||0),ppl=+$('ppl').value;
 var gas=last.distance/1000/eff*fuel*r,toll=last.toll*r,taxi=last.taxi*r;
 $('o-taxi').textContent=H.won(taxi);$('o-taxi-l').textContent='예상 택시비 (주간'+(r>1?', 왕복':'')+')';
 $('o-dist').textContent=H.km(last.distance*r);$('o-time').textContent=H.fmtMin(last.duration*r);$('o-toll').textContent=toll?H.won(toll):'없음';
 $('o-gas').textContent=H.won(gas);$('o-car').textContent=H.won(gas+toll);$('o-per').textContent=H.won(taxi/ppl);
 $('o-msg').textContent='택시를 타면 '+H.won(taxi)+', 내 차로 가면 기름값과 통행료를 합쳐 약 '+H.won(gas+toll)+'이에요.'+(ppl>1?' '+ppl+'명이 나누면 택시비는 1인당 '+H.won(taxi/ppl)+'이에요.':'');
 $('o-kakao').href='https://map.kakao.com/link/by/car/'+encodeURIComponent(A.name)+','+A.lat+','+A.lng+'/'+encodeURIComponent(B.name)+','+B.lat+','+B.lng;
 $('o-naver').href='https://map.naver.com/p/directions/'+A.lng+','+A.lat+','+encodeURIComponent(A.name)+',,/'+B.lng+','+B.lat+','+encodeURIComponent(B.name)+',,/-/car';
 $('out').hidden=false}
function calc(){$('err').hidden=true;$('go').disabled=true;$('go').textContent='계산하는 중…';
 H.route(A,B,[],{priority:$('pr').value,avoid:$('toll').checked?['toll']:[]}).then(function(r){last=r;H.draw(r.pts);show();if(window.gtag)gtag('event','taxi_calc')})
 .catch(function(e){$('err').textContent='길을 찾지 못했어요. 출발지·도착지를 도로 가까이 다시 골라 보세요. ('+e.message+')';$('err').hidden=false})
 .then(function(){$('go').disabled=!(A&&B);$('go').textContent='요금 다시 계산하기'})}
$('go').onclick=calc;['pr','toll'].forEach(function(i){$(i).addEventListener('change',function(){if(A&&B)calc()})});
['eff','fuel','ppl','rt'].forEach(function(i){$(i).addEventListener('input',show);$(i).addEventListener('change',show)});
})();
</script>
'''
TAXI_FAQ = [
 ('택시비는 얼마나 정확한가요?', '카카오모빌리티 길찾기가 지금 교통 상황으로 계산한 주간 기본요금 추정값이에요. 실제 요금은 신호 대기와 정체 시간에 따라 달라지고, 심야 할증(밤 10시~새벽 4시)과 시 경계를 넘는 시계외 할증, 호출비는 들어 있지 않아요.'),
 ('통행료는 어떤 차 기준인가요?', '일반 승용차(1종) 기준 고속도로·유료도로 통행료예요. 경차·전기차 감면이나 출퇴근 할인은 반영되지 않아요.'),
 ('기름값은 어떻게 넣으면 되나요?', '자주 가는 주유소의 리터당 가격과 내 차 연비를 넣으세요. 연비는 계기판 평균 연비를 쓰면 실제와 가장 가까워요. 숫자를 바꾸면 바로 다시 계산돼요.'),
 ('유료도로 피하기를 켜면 어떻게 되나요?', '고속도로 같은 유료 구간을 빼고 다시 길을 찾아요. 통행료는 줄지만 시간이 늘 수 있으니 두 결과를 비교해 보세요.'),
]

def build_all():
    shell('taxi-fare', '택시비 계산기 · 통행료·기름값까지 한 번에 (카카오 길찾기 지도) | 홍라이프 도구',
          '출발지와 도착지를 지도에서 고르면 예상 택시비, 고속도로 통행료, 내 차 기름값, 거리·시간을 카카오모빌리티 길찾기로 바로 계산해요. 왕복·인원 나누기·유료도로 피하기도 돼요.',
          '택시비·통행료·기름값 계산기',
          '출발지와 도착지만 고르면 예상 택시비, 고속도로 통행료, 내 차로 갈 때 기름값까지 한 번에 비교해요. 카카오모빌리티 길찾기로 지금 교통 상황을 반영해요.',
          '<style id="hl-mt">' + COMMON_CSS + '</style>\n', TAXI_MAIN, TAXI_JS, TAXI_FAQ)

# ───────────────── 2) 중간지점 찾기 (약속 장소) + 공유 카드 ─────────────────
MID_CSS = '''
.pp{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}
.pp li{display:grid;grid-template-columns:auto 84px 1fr auto;gap:6px;align-items:center}
.pp .dot{width:30px;height:30px;border-radius:50%;color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:14px}
.pp input{font:inherit;font-size:16px;padding:10px;border:1px solid var(--line-s);border-radius:10px;min-height:44px;width:100%;box-sizing:border-box;background:#fff}
.pp input.on{border-color:var(--acc);box-shadow:0 0 0 3px rgba(49,130,246,.15)}
.pp button{font:inherit;font-size:13px;font-weight:700;border:1px solid var(--line-s);background:#fff;border-radius:10px;min-height:44px;padding:0 9px;cursor:pointer;white-space:nowrap}
.pp button[aria-pressed=true]{background:var(--acc);border-color:var(--acc);color:#fff}
.pp .sug{grid-column:2/-1;margin:0}
.addp{margin-top:10px;font:inherit;font-size:14.5px;font-weight:700;border:1px dashed #9AA6B2;background:#fff;border-radius:12px;min-height:44px;width:100%;cursor:pointer;color:var(--head)}
.rk{list-style:none;margin:14px 0 0;padding:0;display:flex;flex-direction:column;gap:10px}
.rk li{border:1px solid var(--line-s);border-radius:14px;padding:12px 14px;background:#fff}
.rk li.best{border:2px solid #F59F00;background:#FFF9E6}
.rk h3{margin:0;font-size:17px;color:var(--head);display:flex;gap:8px;align-items:center;flex-wrap:wrap;word-break:keep-all}
.rk h3 em{font-style:normal;font-size:12px;font-weight:800;background:#F59F00;color:#fff;border-radius:999px;padding:2px 8px}
.rk .sub{font-size:13px;color:var(--muted);margin:3px 0 8px}
.bars{display:flex;flex-direction:column;gap:5px}
.bar{display:grid;grid-template-columns:52px 1fr 56px;gap:8px;align-items:center;font-size:13.5px}
.bar i{display:block;height:10px;border-radius:6px}
.bar b{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.bar span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:700}
.near{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.near a{padding:7px 11px;border-radius:999px;background:#F1F3F5;color:var(--head);font-size:13px;font-weight:700;text-decoration:none}
.shr{margin-top:16px;border-radius:16px;background:#F4F7FB;padding:14px}
.shr h3{margin:0 0 10px;font-size:16px;color:var(--head)}
.shr canvas{display:block;width:100%;max-width:360px;margin:0 auto;border-radius:14px;box-shadow:0 4px 18px rgba(0,0,0,.12)}
.shb{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:12px}
.shb button{font:inherit;font-size:14px;font-weight:800;border:0;border-radius:12px;min-height:48px;cursor:pointer;background:#191F28;color:#fff}
.shb button:nth-child(2){background:#FEE500;color:#191919}.shb button:nth-child(3){background:#fff;color:var(--head);border:1px solid var(--line-s)}
.prog{height:6px;border-radius:4px;background:#E9ECEF;overflow:hidden;margin-top:12px}.prog i{display:block;height:100%;width:0;background:var(--acc);transition:width .2s}
@media(max-width:520px){.pp li{grid-template-columns:auto 70px 1fr auto}.shb button{font-size:13px}}
'''
MID_MAIN = '''<section class="card tool"><h2>누가 어디서 출발하나요?</h2>
<div class="mp-wrap"><div id="map" role="application" aria-label="지도"></div><p class="mp-hint" id="mp-hint">지도를 불러오는 중…</p></div>
<ul class="pp" id="pp"></ul>
<button type="button" class="addp" id="addp">+ 사람 추가 (최대 6명)</button>
<div class="opts"><label>만날 곳 후보<select id="ct"><option value="SW8">지하철역 근처</option><option value="CE7">카페</option><option value="FD6">음식점</option><option value="CT1">문화시설(영화관·공연장)</option></select></label>
<label>기준<select id="mode"><option value="max">가장 오래 걸리는 사람 기준 (공평)</option><option value="sum">모두 합친 시간 기준</option></select></label></div>
<button class="go-btn" id="go" disabled>중간지점 찾기</button>
<div class="prog" id="prog" hidden><i id="progi"></i></div>
<p class="tfm err" id="err" hidden></p>
<div id="out" hidden><ol class="rk" id="rk"></ol>
<div class="shr"><h3>단톡방에 보낼 공유 카드</h3><canvas id="cv" width="1080" height="1350" aria-label="중간지점 공유 카드"></canvas>
<div class="shb"><button type="button" id="b-share">공유하기</button><button type="button" id="b-link">링크 복사</button><button type="button" id="b-save">이미지 저장</button></div>
<p class="tfm" id="shmsg" style="text-align:center"></p></div></div>
<p class="tfm" style="color:var(--muted)">자동차로 가는 시간 기준이에요. 카카오모빌리티 길찾기로 지금 교통 상황을 반영해 각자 출발지에서 후보 장소까지 걸리는 시간을 하나씩 계산해요.</p>
</section>
<section class="card"><h2>이렇게 찾아요</h2><ul class="xp">
<li>모두의 출발지 한가운데를 잡고, 그 주변 4km 안에서 지하철역·카페·음식점 같은 후보를 최대 8곳 골라요.</li>
<li>후보마다 각자 차로 몇 분 걸리는지 길찾기로 계산해요.</li>
<li><b>공평 기준</b>은 가장 오래 걸리는 사람의 시간이 제일 짧은 곳을 1등으로, <b>합계 기준</b>은 모두의 시간을 더한 값이 제일 작은 곳을 1등으로 골라요.</li>
<li>공유 카드는 이 기기 안에서 그림으로 만들어져요. 출발지는 링크를 연 사람에게만 보여요.</li></ul></section>
'''
MID_JS = '<script>\n' + COMMON_JS + r'''
(function(){
var H=HLMAP,$=function(i){return document.getElementById(i)},COL=['#3182F6','#F04452','#12B886','#F59F00','#7950F2','#E64980'],P=[],pick=0,best=null,RES=[];
function blank(i){return {name:'친구'+(i+1),pt:null,mk:null}}
P=[blank(0),blank(1)];P[0].name='나';
function render(){var ul=$('pp');ul.innerHTML='';P.forEach(function(p,i){var li=document.createElement('li');
 li.innerHTML='<span class="dot" style="background:'+COL[i]+'">'+(i+1)+'</span><input class="nm" maxlength="6" aria-label="이름"><input class="q" placeholder="출발지 검색" autocomplete="off" aria-label="출발지"><button type="button">'+(P.length>2?'빼기':'지도에서')+'</button><ul class="sug" hidden></ul>';
 var nm=li.querySelector('.nm'),q=li.querySelector('.q'),bt=li.querySelector('button'),sg=li.querySelector('.sug');nm.value=p.name;q.value=p.pt?p.pt.name:'';
 nm.oninput=function(){p.name=nm.value.trim()||('친구'+(i+1));if(best)drawCard()};
 q.onfocus=function(){setPick(i)};var t;q.oninput=function(){clearTimeout(t);var s=q.value.trim();if(s.length<2){sg.hidden=true;return}
  t=setTimeout(function(){H.search(s,function(r){sg.innerHTML='';r.forEach(function(o){var l2=document.createElement('li'),b=document.createElement('button');b.type='button';b.textContent=o.name;var sm=document.createElement('small');sm.textContent=o.addr;b.appendChild(sm);b.onclick=function(){setPt(i,o);sg.hidden=true;H.map.setCenter(new kakao.maps.LatLng(o.lat,o.lng))};l2.appendChild(b);sg.appendChild(l2)});sg.hidden=!r.length})},250)};
 bt.onclick=function(){if(P.length>2){if(p.mk)p.mk.setMap(null);P.splice(i,1);P.forEach(function(x,j){if(x.mk){x.mk.setMap(null);x.mk=H.pin(x.pt.lat,x.pt.lng,j+1,COL[j])}});render()}else setPick(i)};
 ul.appendChild(li)});$('addp').hidden=P.length>=6;upd();setPick(Math.min(pick,P.length-1))}
function setPick(i){pick=i;[].forEach.call(document.querySelectorAll('.pp .q'),function(q,j){q.classList.toggle('on',j==i)});$('mp-hint').textContent=(i+1)+'번 '+(P[i]?P[i].name:'')+'의 출발지를 검색하거나 지도를 누르세요'}
function setPt(i,o){var p=P[i];p.pt=o;if(p.mk)p.mk.setMap(null);p.mk=H.pin(o.lat,o.lng,i+1,COL[i]);var q=document.querySelectorAll('.pp .q')[i];if(q)q.value=o.name;
 var nx=P.findIndex(function(x){return !x.pt});if(nx>=0)setPick(nx);upd()}
function upd(){$('go').disabled=P.filter(function(p){return p.pt}).length<2}
$('addp').onclick=function(){if(P.length<6){P.push(blank(P.length));render();setPick(P.length-1)}};
H.onReady(function(){H.init($('map'),37.5547,126.9707,8);
 kakao.maps.event.addListener(H.map,'click',function(e){var ll=e.latLng,o={lat:ll.getLat(),lng:ll.getLng(),name:'지도에서 고른 곳'};setPt(pick,o);var k=pick;H.nameAt(o.lat,o.lng,function(n){o.name=n;var q=document.querySelectorAll('.pp .q')[k];if(q&&P[k]&&P[k].pt===o)q.value=n})});
 loadShared()});
render();
function cats(c,lat,lng){return new Promise(function(res){var ps=new kakao.maps.services.Places();ps.categorySearch(c,function(d,st){res(st===kakao.maps.services.Status.OK?d:[])},{location:new kakao.maps.LatLng(lat,lng),radius:4000,sort:kakao.maps.services.SortBy.DISTANCE})})}
function pool(tasks,n,onp){var i=0,done=0,out=new Array(tasks.length);return new Promise(function(res){function next(){if(i>=tasks.length){if(done===tasks.length)res(out);return}var k=i++;tasks[k]().then(function(v){out[k]=v},function(){out[k]=null}).then(function(){done++;onp(done/tasks.length);next()})}for(var j=0;j<Math.min(n,tasks.length);j++)next();if(!tasks.length)res(out)})}
var cand=[];
function run(){var ps=P.filter(function(p){return p.pt});if(ps.length<2)return;$('err').hidden=true;$('go').disabled=true;$('go').textContent='계산하는 중…';$('prog').hidden=false;$('progi').style.width='0';
 var lat=ps.reduce(function(a,p){return a+p.pt.lat},0)/ps.length,lng=ps.reduce(function(a,p){return a+p.pt.lng},0)/ps.length;
 cats($('ct').value,lat,lng).then(function(d){var seen={};var c=d.filter(function(x){var k=x.place_name.replace(/\s*\d+번?\s*출구.*/,'');if(seen[k])return false;seen[k]=1;return true}).slice(0,8).map(function(x){return {name:x.place_name,addr:x.road_address_name||x.address_name,lat:+x.y,lng:+x.x,url:x.place_url}});
  if(!c.length)c=[{name:'한가운데 지점',addr:'',lat:lat,lng:lng}];cand=c;
  var tasks=[];c.forEach(function(cd,ci){ps.forEach(function(p,pi){tasks.push(function(){return H.route(p.pt,cd,[],{summaryOnly:true}).then(function(r){return {ci:ci,pi:pi,s:r.duration,m:r.distance}})})})});
  return pool(tasks,4,function(f){$('progi').style.width=Math.round(f*100)+'%'}).then(function(rs){
   RES=c.map(function(cd,ci){var t=ps.map(function(p,pi){var r=rs.find(function(x){return x&&x.ci===ci&&x.pi===pi});return r?r.s:null});return {c:cd,t:t,ok:t.every(function(x){return x!=null})}}).filter(function(x){return x.ok});
   if(!RES.length)throw new Error('후보까지 길을 찾지 못했어요');var md=$('mode').value;
   RES.forEach(function(r){r.max=Math.max.apply(null,r.t);r.sum=r.t.reduce(function(a,b){return a+b},0);r.gap=r.max-Math.min.apply(null,r.t)});
   RES.sort(function(a,b){return md=='max'?(a.max-b.max)||(a.sum-b.sum):(a.sum-b.sum)||(a.max-b.max)});best=RES[0];show(ps);if(window.gtag)gtag('event','midpoint_calc',{n:ps.length})})})
 .catch(function(e){$('err').textContent='중간지점을 찾지 못했어요. 출발지를 도로 가까이 다시 골라 보세요. ('+e.message+')';$('err').hidden=false})
 .then(function(){$('go').disabled=false;$('go').textContent='다시 찾기';$('prog').hidden=true})}
$('go').onclick=run;
var cmk=[];
function show(ps){var ol=$('rk');ol.innerHTML='';var mx=Math.max.apply(null,RES.slice(0,3).map(function(r){return r.max}));
 cmk.forEach(function(m){m.setMap(null)});cmk=[];
 RES.slice(0,3).forEach(function(r,k){var li=document.createElement('li');if(!k)li.className='best';
  li.innerHTML='<h3>'+(k?(k+1)+'위':'<em>추천</em>')+' <span></span></h3><p class="sub"></p><div class="bars"></div><div class="near"></div>';
  li.querySelector('h3 span').textContent=r.c.name;li.querySelector('.sub').textContent=(r.c.addr||'')+' · 가장 오래 '+H.fmtMin(r.max)+' · 차이 '+H.fmtMin(r.gap);
  var bs=li.querySelector('.bars');ps.forEach(function(p,i){var pi=P.indexOf(p),d=document.createElement('div');d.className='bar';
   d.innerHTML='<span></span><i style="background:'+COL[pi]+';width:'+Math.max(6,Math.round(r.t[i]/mx*100))+'%"></i><b>'+H.fmtMin(r.t[i])+'</b>';d.querySelector('span').textContent=p.name;bs.appendChild(d)});
  var nr=li.querySelector('.near'),base=r.c.name.replace(/\s*\d+번?\s*출구.*/,'');['맛집','카페','주차장'].forEach(function(w){var a=document.createElement('a');a.href='https://map.kakao.com/link/search/'+encodeURIComponent(base+' '+w);a.target='_blank';a.rel='noopener';a.textContent=w;nr.appendChild(a)});
  if(r.c.url){var a=document.createElement('a');a.href=r.c.url;a.target='_blank';a.rel='noopener';a.textContent='장소 정보';nr.appendChild(a)}
  ol.appendChild(li);
  var svg='<svg xmlns="http://www.w3.org/2000/svg" width="40" height="50" viewBox="0 0 32 40"><path d="M16 39C16 39 3 24 3 15a13 13 0 0 1 26 0c0 9-13 24-13 24z" fill="'+(k?'#868E96':'#F59F00')+'" stroke="#fff" stroke-width="2.4"/><text x="16" y="20" text-anchor="middle" font-family="system-ui,sans-serif" font-size="13" font-weight="800" fill="#fff">'+(k?k+1:'★')+'</text></svg>';
  cmk.push(new kakao.maps.Marker({map:H.map,position:new kakao.maps.LatLng(r.c.lat,r.c.lng),image:new kakao.maps.MarkerImage('data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg),new kakao.maps.Size(40,50),{offset:new kakao.maps.Point(20,49)}),zIndex:k?1:5}))});
 var b=new kakao.maps.LatLngBounds();ps.forEach(function(p){b.extend(new kakao.maps.LatLng(p.pt.lat,p.pt.lng))});b.extend(new kakao.maps.LatLng(best.c.lat,best.c.lng));H.map.setBounds(b,50,40,50,40);
 $('out').hidden=false;drawCard();history.replaceState(null,'',location.pathname+'?p='+shareParam())}
function shareParam(){return encodeURIComponent(P.filter(function(p){return p.pt}).map(function(p){return [p.name.replace(/[~|]/g,''),p.pt.lat.toFixed(5),p.pt.lng.toFixed(5),p.pt.name.replace(/[~|]/g,'').slice(0,30)].join('~')}).join('|'))+'&c='+$('ct').value+'&m='+$('mode').value}
function loadShared(){var q=new URLSearchParams(location.search),s=q.get('p');if(!s)return;try{var arr=s.split('|').map(function(x){var a=x.split('~');return {name:a[0],pt:{lat:+a[1],lng:+a[2],name:a[3]||'출발지'}}}).filter(function(x){return isFinite(x.pt.lat)&&isFinite(x.pt.lng)}).slice(0,6);
 if(arr.length<2)return;if(q.get('c'))$('ct').value=q.get('c');if(q.get('m'))$('mode').value=q.get('m');
 P=arr.map(function(a,i){return {name:a.name||('친구'+(i+1)),pt:a.pt,mk:null}});render();P.forEach(function(p,i){p.mk=H.pin(p.pt.lat,p.pt.lng,i+1,COL[i])});run()}catch(e){}}
// 공유 카드
function rr(x,a,b,w,h,r){x.beginPath();x.moveTo(a+r,b);x.arcTo(a+w,b,a+w,b+h,r);x.arcTo(a+w,b+h,a,b+h,r);x.arcTo(a,b+h,a,b,r);x.arcTo(a,b,a+w,b,r);x.closePath()}
function fit(x,t,max,size,weight){var s=size;do{x.font=weight+' '+s+'px "Pretendard Variable",Pretendard,system-ui,sans-serif';s-=2}while(x.measureText(t).width>max&&s>24);return s+2}
function drawCard(){if(!best)return;var cv=$('cv'),x=cv.getContext('2d'),W=1080,Hh=1350,ps=P.filter(function(p){return p.pt});
 var g=x.createLinearGradient(0,0,W,Hh);g.addColorStop(0,'#FFE066');g.addColorStop(1,'#FFA94D');x.fillStyle=g;x.fillRect(0,0,W,Hh);
 x.fillStyle='rgba(255,255,255,.35)';for(var i=0;i<6;i++){x.beginPath();x.arc(900-i*40,140+i*20,120-i*14,0,7);x.fill()}
 x.fillStyle='#3B2F00';x.font='800 54px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.fillText('우리 어디서 만나?',80,150);
 x.font='600 34px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.fillStyle='#6B5300';x.fillText(ps.length+'명 모두 차로 공평하게 가는 곳',80,206);
 rr(x,60,250,960,330,36);x.fillStyle='#fff';x.fill();
 x.fillStyle='#F59F00';rr(x,100,290,170,56,28);x.fill();x.fillStyle='#fff';x.font='800 30px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.fillText('★ 추천',128,328);
 var nm=best.c.name;fit(x,nm,880,88,'800');x.fillStyle='#191F28';x.fillText(nm,100,450);
 x.font='600 34px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.fillStyle='#4E5968';var ad=best.c.addr||'';while(x.measureText(ad).width>880&&ad.length)ad=ad.slice(0,-1);x.fillText(ad,100,510);
 x.fillStyle='#868E96';x.font='600 30px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.fillText('가장 오래 걸려도 '+H.fmtMin(best.max),100,556);
 var top=640,rowH=Math.min(110,(1180-top)/Math.max(ps.length,1)),mx=best.max;
 ps.forEach(function(p,i){var pi=P.indexOf(p),y=top+i*rowH;x.fillStyle=COL[pi];x.beginPath();x.arc(110,y+30,30,0,7);x.fill();
  x.fillStyle='#fff';x.font='800 30px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.textAlign='center';x.fillText(String(i+1),110,y+41);x.textAlign='left';
  x.fillStyle='#3B2F00';var n=p.name;fit(x,n,190,38,'800');x.fillText(n,160,y+44);
  rr(x,370,y+14,500,32,16);x.fillStyle='rgba(255,255,255,.6)';x.fill();rr(x,370,y+14,Math.max(40,500*best.t[i]/mx),32,16);x.fillStyle=COL[pi];x.fill();
  x.fillStyle='#3B2F00';x.font='800 36px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.textAlign='right';x.fillText(H.fmtMin(best.t[i]),1020,y+44);x.textAlign='left'});
 x.fillStyle='rgba(59,47,0,.75)';x.font='700 30px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.fillText('홍라이프 도구 · 중간지점 찾기',80,1290);
 x.textAlign='right';x.font='600 26px "Pretendard Variable",Pretendard,system-ui,sans-serif';x.fillText('honglife.co.kr',1000,1290);x.textAlign='left'}
function shareURL(){return location.origin+location.pathname+'?p='+shareParam()}
function blob(){return new Promise(function(r){$('cv').toBlob(r,'image/png')})}
$('b-save').onclick=function(){blob().then(function(b){var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='중간지점-'+(best?best.c.name:'')+'.png';a.click();$('shmsg').textContent='이미지를 저장했어요.'})};
$('b-link').onclick=function(){var u=shareURL();(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){$('shmsg').textContent='링크를 복사했어요. 단톡방에 붙여 넣으세요.'},function(){prompt('이 링크를 복사하세요',u)})};
$('b-share').onclick=function(){var u=shareURL(),t='우리 '+(best?best.c.name:'')+'에서 만나요! 각자 걸리는 시간 보기';
 blob().then(function(b){var f=new File([b],'midpoint.png',{type:'image/png'});
  if(navigator.canShare&&navigator.canShare({files:[f]}))return navigator.share({files:[f],title:'중간지점',text:t+' '+u});
  if(navigator.share)return navigator.share({title:'중간지점',text:t,url:u});$('b-link').onclick()}).catch(function(){})};
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){if(best)drawCard()});
})();
</script>
'''
MID_FAQ = [
 ('중간지점은 어떻게 정하나요?', '모두의 출발지 한가운데 근처에서 지하철역·카페 같은 후보를 고른 뒤, 후보마다 각자 차로 걸리는 시간을 카카오모빌리티 길찾기로 계산해요. 공평 기준이면 가장 오래 걸리는 사람의 시간이 제일 짧은 곳이 1등이에요.'),
 ('대중교통으로도 계산되나요?', '지금은 자동차 기준이에요. 지하철역 근처 후보를 고르면 대중교통으로 모이기에도 좋은 곳이 나오는 경우가 많아요.'),
 ('공유 카드에 내 주소가 나오나요?', '카드에는 추천 장소와 사람별 이름·걸리는 시간만 나오고 출발지 주소는 넣지 않아요. 다만 링크 복사로 보낸 링크에는 출발 위치 좌표가 들어 있어서, 링크를 연 사람의 화면에 같은 결과가 다시 계산돼요.'),
 ('몇 명까지 되나요?', '2명부터 6명까지 넣을 수 있어요. 사람이 많을수록 계산할 길이 늘어나서 몇 초 더 걸려요.'),
]

def build_mid():
    shell('midpoint', '중간지점 찾기 · 약속 장소 추천 (차로 공평하게, 공유 카드) | 홍라이프 도구',
          '친구들 출발지를 지도에 찍으면 모두 차로 공평하게 갈 수 있는 지하철역·카페·음식점을 카카오모빌리티 길찾기로 찾아 줘요. 사람별 걸리는 시간과 단톡방 공유 카드까지.',
          '중간지점 찾기 (약속 장소 추천)',
          '친구들 출발지를 넣으면 모두가 차로 비슷하게 걸리는 만날 곳을 찾아요. 사람별 걸리는 시간을 비교하고, 결과를 공유 카드로 단톡방에 바로 보낼 수 있어요.',
          '<style id="hl-mt">' + COMMON_CSS + MID_CSS + '</style>\n', MID_MAIN, MID_JS, MID_FAQ)

if __name__ == '__main__':
    build_all(); build_mid()
