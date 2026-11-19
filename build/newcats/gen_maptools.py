# 지도(카카오모빌리티 길찾기) 웹 도구 → overlay/life/*.html
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = open(os.path.join(ROOT, 'overlay/ipsi/pyeonip-2027.html'), encoding='utf-8').read()
PROXY = 'https://hl-route.a599307.workers.dev/'
KAKAO_JS = 'c4a8d8392dd6a362db17cc44e5ae398b'

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def shell(slug, title, desc, h1, lead, css, main_html, js, faq, crumb=('생활·행정', '/life/')):
    url = f'https://honglife.co.kr/life/{slug}.html'
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
    faq_html = ''.join(f'<dt>{esc(q)}</dt><dd>{esc(a)}</dd>' for q, a in faq)
    main = (f'<main class="wrap wide"><header class="top"><p class="crumb"><a href="/">홈</a> › <a href="{crumb[1]}">{crumb[0]}</a></p>'
            f'<h1>{h1}</h1><p class="lead">{lead}</p></header>\n' + main_html +
            f'<section class="card"><h2>자주 묻는 질문</h2><dl class="pe-faq">{faq_html}</dl></section>\n'
            '<section class="card rel"><h2>함께 쓰면 좋은 도구</h2><ul class="tlist">'
            '<li><a href="/life/route-navi.html"><b>경유지 많은 노선 내비</b><span>정류장 30곳 넘어도 순서대로 안내</span></a></li>'
            '<li><a href="/life/"><b>생활·행정 도구 모음</b><span>생활 계산기·지도 도구 전체 보기</span></a></li></ul></section>\n</main>\n')
    out = (head + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + css
           + base[i_ste:i_main] + main + js + base[i_ft:])
    out = out.replace('<a href="/ipsi/">입시</a>', '<a href="/life/">생활·행정</a>')
    open(os.path.join(ROOT, f'overlay/life/{slug}.html'), 'w', encoding='utf-8').write(out)
    print('wrote', slug, len(out))

# 공통 지도 + 장소 검색 + 카카오 길찾기 (전역 HLMAP)
COMMON_CSS = '''
.mp-wrap{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line-s);background:#EEF1F5}
#map{width:100%;height:min(56vh,440px)}
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
.res{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:14px}
.res div{background:#F4F7FB;border-radius:12px;padding:12px 6px;text-align:center}
.res b{display:block;font-size:21px;color:var(--head);line-height:1.25;font-variant-numeric:tabular-nums;word-break:keep-all}
.res span{display:block;font-size:12.5px;color:var(--muted);margin-top:3px}
.res .big{grid-column:span 3;background:#0B5ED7}.res .big b,.res .big span{color:#fff}.res .big b{font-size:28px}
.msg{font-size:13.5px;line-height:1.6;margin:10px 0 0;color:var(--ink)}
.msg.err{color:#C92A2A;font-weight:700}
.ext{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.ext a{flex:1 1 140px;text-align:center;padding:12px;border-radius:12px;background:#FEE500;color:#191919;font-weight:800;text-decoration:none;font-size:14.5px}
.ext a.n{background:#03C75A;color:#fff}
.pe-faq dt{font-weight:700;margin-top:12px;color:var(--head)}.pe-faq dd{margin:4px 0 0;line-height:1.65;color:var(--ink)}
@media(max-width:520px){.res b{font-size:18px}.res .big b{font-size:24px}#map{height:46vh}}
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
<div id="out" hidden><div class="res">
<div class="big"><b id="o-taxi">–</b><span id="o-taxi-l">예상 택시비 (주간)</span></div>
<div><b id="o-dist">–</b><span>거리</span></div><div><b id="o-time">–</b><span>예상 시간</span></div><div><b id="o-toll">–</b><span>통행료</span></div>
<div><b id="o-gas">–</b><span>내 차 기름값</span></div><div><b id="o-car">–</b><span>내 차 합계</span></div><div><b id="o-per">–</b><span>택시 1인당</span></div>
</div>
<p class="msg" id="o-msg"></p>
<div class="ext"><a id="o-kakao" target="_blank" rel="noopener">카카오맵으로 길안내</a><a class="n" id="o-naver" target="_blank" rel="noopener">네이버 지도로 보기</a></div></div>
<p class="msg err" id="err" hidden></p>
<p class="msg" style="color:var(--muted)">기름값 1,700원은 예시예요. 주유소 가격으로 바꿔 넣으면 바로 다시 계산돼요. 택시비는 카카오 길찾기가 알려 주는 주간 기본요금 기준이고, 심야·시계외 할증과 호출비는 빠져 있어요.</p>
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

if __name__ == '__main__':
    shell('taxi-fare', '택시비 계산기 · 통행료·기름값까지 한 번에 (카카오 길찾기 지도) | 홍라이프 도구',
          '출발지와 도착지를 지도에서 고르면 예상 택시비, 고속도로 통행료, 내 차 기름값, 거리·시간을 카카오모빌리티 길찾기로 바로 계산해요. 왕복·인원 나누기·유료도로 피하기도 돼요.',
          '택시비·통행료·기름값 계산기',
          '출발지와 도착지만 고르면 예상 택시비, 고속도로 통행료, 내 차로 갈 때 기름값까지 한 번에 비교해요. 카카오모빌리티 길찾기로 지금 교통 상황을 반영해요.',
          '<style id="hl-mt">' + COMMON_CSS + '</style>\n', TAXI_MAIN, TAXI_JS, TAXI_FAQ)
