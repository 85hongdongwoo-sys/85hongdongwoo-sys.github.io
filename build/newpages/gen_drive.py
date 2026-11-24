#!/usr/bin/env python3
"""자동차 도구 페이지 (/drive/…) — 공식 법령·기관 자료로 확인한 기준만 씀 (2026-11-25 확인).
로컬에서 돌리고 overlay 결과를 커밋해요: python3 build/newpages/gen_drive.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

SEC = ('자동차·지도', '/drive/')
H2CSS = '<style>#tool h2{margin:26px 0 10px}#tool h2:first-of-type{margin-top:0}#tool .hk-out{white-space:normal}#tool .hk-tbl td,#tool .hk-tbl th{white-space:normal;max-width:none;overflow:visible}</style>'
REL = ('<section class="card rel"><h2>다른 자동차 도구</h2><ul>'
       '<li><a href="/drive/car-inspection.html"><b>자동차 정기검사 기간 계산기</b><span>다음 검사 날짜·검사 가능 기간·지연 과태료</span></a></li>'
       '<li><a href="/drive/tire.html"><b>타이어 규격·제조일자 읽기</b><span>225/55R17 뜻, 바깥지름, DOT 제조 주차, 교체 시기</span></a></li>'
       '<li><a href="/drive/gas-station.html"><b>싼 주유소 지도</b><span>동네별 최저가 휘발유·경유</span></a></li>'
       '<li><a href="/drive/parking.html"><b>공영·무료 주차장</b><span>요금·운영시간 지도</span></a></li>'
       '<li><a href="/drive/rest-area.html"><b>고속도로 휴게소</b><span>대표 메뉴·기름값 지도</span></a></li></ul></section>')

# ── 1. 자동차 정기검사 기간 계산기 ──
INSP_TOOL = ("""<section class="card tool" id="tool">""" + H2CSS + """
<h2>내 차 정보</h2>
<div class="grid g2"><div class="f"><label for="kd">차 종류</label><select id="kd"><option value="p" selected>자가용 승용차 (비사업용)</option><option value="b">영업용 승용차 (택시·렌터카 등 사업용)</option></select></div>
<div class="f"><label for="rg">처음 등록한 날 (신규 등록일)</label><input id="rg" type="date"></div>
<div class="f"><label for="nw">새 차로 등록했나요?</label><select id="nw"><option value="1" selected>네, 새 차(신차)로 등록</option><option value="0">아니요 (수입 중고 등)</option></select></div></div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">다음 검사 유효기간 만료일</div><div class="v" id="ex">—</div></div><div class="tile light"><div class="k">검사 받을 수 있는 기간</div><div class="v" id="wn" style="font-size:18px">—</div></div><div class="tile light"><div class="k">오늘 기준</div><div class="v" id="st" style="font-size:18px">—</div></div></div>
<p class="note" id="nt"></p>
<h2>앞으로의 검사 일정</h2>
<div class="hk-tbl"><table class="tbl"><thead><tr><th>회차</th><th>유효기간 만료일</th><th>검사 받을 수 있는 기간</th></tr></thead><tbody id="sch"><tr><td colspan="3">등록일을 넣으면 나와요</td></tr></tbody></table></div>
<h2>검사를 늦게 받으면 과태료</h2>
<div class="grid g2"><div class="f"><label for="ld">검사 기간이 끝나고 지난 날 수</label><input id="ld" type="number" inputmode="numeric" min="0" max="999" placeholder="예: 60"></div></div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">과태료</div><div class="v" id="fn">—</div></div></div>
</section>""", """<script>
(function(){var $=HL.$;var W='일월화수목금토';
function d0(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2])}
function addY(d,n){var x=new Date(d.getFullYear()+n,d.getMonth(),d.getDate());if(x.getMonth()!==d.getMonth())x=new Date(d.getFullYear()+n,d.getMonth()+1,0);return x}
function addD(d,n){return new Date(d.getFullYear(),d.getMonth(),d.getDate()+n)}
function f(d){return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.('+W[d.getDay()]+')'}
function fine(n){if(!(n>0))return 0;return Math.min(60,4+Math.floor(Math.max(0,n-30)/3)*2)}
function run(){var v=$('#rg').value;if(!v){return}var rg=d0(v),kd=$('#kd').value,nw=$('#nw').value==='1';
 var first=kd==='p'?(nw?(rg>=new Date(2025,0,1)?5:4):2):(nw?2:1),cyc=kd==='p'?2:1;
 var ex=addD(addY(rg,first),-1),list=[],t=new Date();t.setHours(0,0,0,0);
 for(var i=0;i<12;i++){list.push(addY(ex,i*cyc))}
 var nx=list.find(function(e){return addD(e,31)>=t})||list[list.length-1];
 $('#ex').textContent=f(nx);$('#wn').textContent=f(addD(nx,-90))+' ~ '+f(addD(nx,31));
 var a=addD(nx,-90),b=addD(nx,31),dd=Math.round((a-t)/864e5);
 $('#st').textContent=t<a?('검사 기간까지 '+dd+'일'):(t<=b?'지금 검사 받을 수 있어요':'검사 기간이 지났어요');
 $('#nt').textContent=kd==='p'&&nw?('신차 첫 검사는 등록일부터 '+first+'년('+(first===5?'2025년 1월 1일 이후 등록':'2024년 12월 31일까지 등록')+'), 그다음부터 2년마다예요. 제때 검사를 받았다고 보고 계산했어요.'):(kd==='b'?'사업용 승용차는 신차 첫 검사 2년, 그다음부터 1년마다예요.':'신차가 아니면 첫 검사도 2년 주기로 계산했어요. 정확한 날짜는 자동차등록증이나 TS 조회로 확인하세요.');
 $('#sch').innerHTML=list.filter(function(e){return addD(e,31)>=t}).slice(0,5).map(function(e,i){return '<tr><td>'+(i?(i+1)+'번째':'다음 검사')+'</td><td>'+f(e)+'</td><td>'+f(addD(e,-90))+' ~ '+f(addD(e,31))+'</td></tr>'}).join('')}
['#rg','#kd','#nw'].forEach(function(x){$(x).addEventListener('change',run);$(x).addEventListener('input',run)});
$('#ld').addEventListener('input',function(){var n=+$('#ld').value;$('#fn').textContent=this.value===''?'—':(n>0?fine(n)+'만 원':'0원')});
})();
</script>""")

INSP = dict(slug='car-inspection', url='/drive/car-inspection.html', sec=SEC, crumb3='',
  name='자동차 정기검사 기간 계산기 (신차 5년·이후 2년, 검사 가능 기간·과태료)',
  h1='자동차 <b>정기검사 기간</b> 계산기', lead='처음 등록한 날만 넣으면 다음 정기검사 만료일, 검사 받을 수 있는 기간(만료일 전 90일~후 31일), 늦었을 때 과태료를 바로 알려 줘요.',
  desc='자동차 정기검사 다음 날짜를 계산해요. 자가용 승용차는 2025년 1월 1일 이후 등록한 신차 5년(그전 등록 4년) 뒤 첫 검사, 이후 2년마다. 검사 가능 기간은 만료일 전 90일부터 후 31일까지, 지연 과태료 4만~60만 원도 계산해요.',
  tool=INSP_TOOL, warn='', nosafe=True,
  body=[
    ('자가용 승용차 정기검사 주기', '<table class="tbl"><thead><tr><th>구분</th><th>첫 검사</th><th>그다음</th></tr></thead><tbody>'
      '<tr><td>자가용 승용 신차, <b>2025년 1월 1일 이후</b> 등록</td><td>등록일부터 5년</td><td>2년마다</td></tr>'
      '<tr><td>자가용 승용 신차, 2024년 12월 31일까지 등록</td><td>등록일부터 4년</td><td>2년마다</td></tr>'
      '<tr><td>영업용(사업용) 승용 신차</td><td>등록일부터 2년</td><td>1년마다</td></tr></tbody></table>'
      '<p>자동차관리법 시행규칙 [별표 15의2]가 2024년 12월 17일 바뀌면서 자가용 승용 신차의 첫 검사 유효기간이 4년에서 5년으로 늘었어요. 그래서 아직 “새 차는 4년 뒤 첫 검사”라고 적힌 글이 많지만, 2025년부터 등록한 차는 5년이에요. 크기(경차·소형·중형·대형)와 상관없이 같아요.</p>'
      '<p>예: 2025년 1월 3일 새 차를 등록했다면 첫 유효기간 만료일은 <b>2030년 1월 2일</b>, 검사 받을 수 있는 기간은 <b>2029년 10월 4일 ~ 2030년 2월 2일</b>이에요.</p>'),
    ('검사 받을 수 있는 기간: 만료일 전 90일 ~ 후 31일', '<p>정기검사는 유효기간 만료일 <b>90일 전부터 31일 뒤까지</b> 받으면 돼요(약 4달). 이 기간 안에 합격하면 만료일에 검사를 받은 것으로 쳐 줘서, 일찍 받아도 다음 검사 날짜가 당겨지지 않아요. 예전에는 만료일 앞뒤 31일이었는데 바뀌었어요.</p>'),
    ('정기검사 늦으면 과태료 (4만~60만 원)', '<table class="tbl"><thead><tr><th>검사 기간이 끝나고 지난 날</th><th>과태료</th></tr></thead><tbody><tr><td>30일 이내</td><td>4만 원</td></tr><tr><td>31일째부터</td><td>3일 넘을 때마다 2만 원씩 더</td></tr><tr><td>예: 60일</td><td>4만 + (30÷3)×2만 = 24만 원</td></tr><tr><td>115일 이상</td><td>60만 원 (최고)</td></tr></tbody></table>'
      '<p>과태료는 만료일이 아니라 <b>검사 기간(만료일+31일)이 끝난 다음 날</b>부터 세요.</p>'),
    ('정기검사와 종합검사', '<p>수도권과 인구 50만 이상 도시처럼 정해진 지역에 등록된 차는 일정 차령이 지나면 배출가스 정밀검사가 더해진 <b>종합검사</b>를 받아요. 우리 차가 어느 검사 대상인지, 정확한 만료일은 자동차등록증이나 한국교통안전공단(TS) 자동차검사 조회로 확인하세요. 예약은 TS 사이버검사소에서 할 수 있어요.</p>'),
  ],
  faq=[('새 차는 몇 년 뒤에 첫 정기검사를 받나요?', '자가용 승용차는 2025년 1월 1일 이후 처음 등록한 새 차는 5년 뒤, 2024년 12월 31일까지 등록한 차는 4년 뒤에 첫 검사를 받고, 그다음부터 2년마다 받아요.'),
       ('정기검사는 언제부터 받을 수 있나요?', '유효기간 만료일 90일 전부터 만료일 31일 뒤까지 받을 수 있어요. 이 안에 합격하면 만료일에 받은 것으로 봐요.'),
       ('정기검사를 놓치면 과태료가 얼마예요?', '검사 기간이 끝나고 30일 안이면 4만 원, 그 뒤로 3일마다 2만 원씩 붙어 최고 60만 원이에요. 예를 들어 60일 늦으면 24만 원이에요.'),
       ('전기차도 정기검사를 받나요?', '네. 전기차도 정기검사를 받아요. 배출가스가 없어서 배출가스 정밀검사(종합검사 항목)는 해당되지 않아요.'),
       ('내 차 검사 만료일은 어디서 보나요?', '자동차등록증 뒷면의 검사 기록이나 한국교통안전공단(TS) 자동차검사 조회에서 확인할 수 있어요.')],
  rel=REL,
  src='<li><a href="https://www.easylaw.go.kr/CSP/CnpClsMainBtr.laf?popMenu=ov&csmSeq=675&ccfNo=2&cciNo=2&cnpClsNo=1" rel="noopener" target="_blank">찾기쉬운 생활법령정보 — 자동차 검사받기</a> (검사 유효기간 표, 검사 기간 90일 전~31일 후)</li><li><a href="https://www.law.go.kr/" rel="noopener" target="_blank">국가법령정보센터 — 자동차관리법 시행규칙 [별표 15의2] (2024. 12. 17. 개정)</a></li><li>과태료: 자동차관리법 시행령 (서울·수원·김해 등 지자체 안내와 같음) · 2026-11-25 확인</li>')

# ── 2. 타이어 규격·제조일자 ──
TIRE_TOOL = ("""<section class="card tool" id="tool">""" + H2CSS + """
<h2>타이어 규격 읽기</h2>
<div class="grid g2"><div class="f"><label for="sz">타이어 옆면 규격</label><input id="sz" value="225/55R17" placeholder="예: 225/55R17 97V" autocomplete="off"></div>
<div class="f"><label for="sz2">비교할 규격 (선택)</label><input id="sz2" placeholder="예: 235/45R18" autocomplete="off"></div></div>
<div class="hk-out" id="ro"></div>
<h2>제조일자(DOT) 읽기</h2>
<div class="grid g2"><div class="f"><label for="dot">DOT 뒤 마지막 숫자 4자리</label><input id="dot" inputmode="numeric" maxlength="4" placeholder="예: 2423"></div></div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">만든 때</div><div class="v" id="dm" style="font-size:18px">—</div></div><div class="tile light"><div class="k">지금까지</div><div class="v" id="da">—</div></div></div>
<p class="note" id="dn"></p>
</section>""", """<script>
(function(){var $=HL.$;
function parse(s){var m=String(s||'').toUpperCase().replace(/\\s+/g,'').match(/^(?:P|LT)?(\\d{3})\\/(\\d{2})Z?R(?:F)?(\\d{2})(?:(\\d{2,3})(?:\\/\\d{2,3})?([A-Z]))?/);if(!m)return null;return {w:+m[1],a:+m[2],r:+m[3],li:m[4]?+m[4]:null,sp:m[5]||null}}
function dia(t){return t.r*25.4+2*t.w*t.a/100}
var SP={L:120,M:130,N:140,P:150,Q:160,R:170,S:180,T:190,U:200,H:210,V:240,W:270,Y:300};
function show(){var a=parse($('#sz').value),b=parse($('#sz2').value),o=$('#ro');if(!a){o.innerHTML='225/55R17처럼 적어 주세요.';return}
 var sw=a.w*a.a/100,d=dia(a),c=d*Math.PI;var h='<p><b>'+a.w+'</b> = 타이어 폭 '+a.w+'mm · <b>'+a.a+'</b> = 편평비 '+a.a+'% (옆면 높이 '+sw.toFixed(1)+'mm) · <b>R</b> = 레이디얼 구조 · <b>'+a.r+'</b> = 휠 지름 '+a.r+'인치</p>';
 if(a.li)h+='<p><b>'+a.li+'</b> = 하중 지수'+(a.sp?' · <b>'+a.sp+'</b> = 속도 기호'+(SP[a.sp]?' (최고 '+SP[a.sp]+'km/h)':''):'')+'</p>';
 h+='<p>바깥지름 <b>'+d.toFixed(1)+'mm</b> · 한 바퀴 <b>'+(c/1000).toFixed(3)+'m</b></p>';
 if(b){var d2=dia(b),df=(d2-d)/d*100;h+='<p>비교: '+b.w+'/'+b.a+'R'+b.r+' 바깥지름 '+d2.toFixed(1)+'mm → 차이 <b>'+(df>0?'+':'')+df.toFixed(2)+'%</b>. 계기판이 100km/h일 때 실제 속도 약 <b>'+(100*d2/d).toFixed(1)+'km/h</b>. '+(Math.abs(df)>3?'3%가 넘게 달라서 권하지 않아요.':'보통 ±3% 안이면 많이 써요.')+'</p>'}
 o.innerHTML=h}
function dot(){var v=$('#dot').value.replace(/\\D/g,'');if(v.length!==4){$('#dm').textContent=$('#da').textContent='—';$('#dn').textContent=v.length===3?'3자리면 2000년 이전 타이어예요. 아주 오래된 타이어라 바로 교체하세요.':'';return}
 var wk=+v.slice(0,2),yr=2000+(+v.slice(2));if(wk<1||wk>53){$('#dn').textContent='앞 두 자리(주차)는 01~53이어야 해요.';return}
 var jan4=new Date(yr,0,4),dow=(jan4.getDay()+6)%7,mon=new Date(yr,0,4-dow+(wk-1)*7);var t=new Date();var mo=(t.getFullYear()-mon.getFullYear())*12+(t.getMonth()-mon.getMonth());
 $('#dm').textContent=yr+'년 '+wk+'번째 주 ('+(mon.getMonth()+1)+'월 무렵)';$('#da').textContent=mo<0?'—':(Math.floor(mo/12)+'년 '+(mo%12)+'개월');
 $('#dn').textContent=mo>=72?'만든 지 6년이 넘었어요. 홈이 남아 있어도 교체를 권해요.':mo>=60?'5년이 넘었어요. 갈라짐·경화를 점검하고 교체를 준비하세요.':''}
$('#sz').addEventListener('input',show);$('#sz2').addEventListener('input',show);$('#dot').addEventListener('input',dot);show();
})();
</script>""")

TIRE = dict(slug='tire', url='/drive/tire.html', sec=SEC, crumb3='',
  name='타이어 규격 보는 법·제조일자(DOT) 읽기 (225/55R17 뜻, 교체 시기 1.6mm)',
  h1='타이어 <b>규격·제조일자</b> 읽기', lead='타이어 옆면의 225/55R17 같은 숫자와 DOT 제조일자를 넣으면 뜻을 풀어 주고, 다른 크기로 바꿀 때 속도계 오차와 교체 시기까지 알려 줘요.',
  desc='타이어 옆면 규격(예: 225/55R17 97V)을 넣으면 폭·편평비·휠 지름·바깥지름·하중 지수·속도 기호를 풀어 주고, 다른 규격과 지름 차이(%)·속도계 오차를 비교해요. DOT 마지막 4자리로 제조 주차와 사용 연수, 홈 깊이 1.6mm 교체 기준도 정리했어요.',
  tool=TIRE_TOOL, warn='', nosafe=True,
  body=[
    ('225/55R17 97V는 무슨 뜻인가요', '<table class="tbl"><thead><tr><th>표시</th><th>뜻</th><th>예 (225/55R17 97V)</th></tr></thead><tbody>'
      '<tr><td>225</td><td>타이어 폭 (mm)</td><td>225mm</td></tr><tr><td>55</td><td>편평비: 옆면 높이 ÷ 폭 (%)</td><td>옆면 높이 123.75mm</td></tr>'
      '<tr><td>R</td><td>레이디얼 구조</td><td>대부분의 승용차 타이어</td></tr><tr><td>17</td><td>휠(림) 지름 (인치)</td><td>17인치 휠</td></tr>'
      '<tr><td>97</td><td>하중 지수</td><td>타이어 하나가 버틸 수 있는 무게 등급</td></tr><tr><td>V</td><td>속도 기호</td><td>최고 240km/h</td></tr></tbody></table>'
      '<p>바깥지름 = 휠 지름 × 25.4 + 옆면 높이 × 2 = 17 × 25.4 + 123.75 × 2 = <b>679.3mm</b>예요. 크기를 바꿀 때는 이 바깥지름 차이를 보통 ±3% 안으로 맞춰요. 차이가 크면 계기판 속도와 실제 속도가 달라져요.</p>'),
    ('제조일자(DOT) 읽는 법', '<p>타이어 옆면 <b>DOT</b> 글자 뒤 숫자·영문 가운데 <b>마지막 4자리</b>가 만든 때예요. 앞 두 자리는 그해의 몇 번째 주, 뒤 두 자리는 연도예요. 예를 들어 <b>2423</b>이면 2023년 24번째 주(6월 무렵)에 만든 타이어예요.</p>'
      '<p>타이어는 달리지 않아도 고무가 굳고 갈라져요. 기아 차량 취급설명서는 <b>제조일부터 6년이 지나면 쓰지 않았어도 새 타이어로 바꾸라</b>고 안내해요.</p>'),
    ('언제 교체하나요: 홈 깊이 1.6mm', '<table class="tbl"><thead><tr><th>기준</th><th>내용</th></tr></thead><tbody><tr><td>법정 한계</td><td>홈(트레드) 깊이 1.6mm 미만이면 안 돼요 — 정기검사 항목이기도 해요</td></tr><tr><td>권장 교체</td><td>빗길 제동을 생각해 3mm 안팎에서 바꾸라는 안내가 많아요</td></tr><tr><td>새 타이어</td><td>홈 깊이 약 8~9mm</td></tr><tr><td>나이</td><td>제조 후 5년 넘으면 점검, 6년 넘으면 교체</td></tr></tbody></table>'
      '<p>홈 안쪽에 튀어나온 <b>마모 한계 표시(TWI)</b>가 있어요. 옆면 삼각형(▲) 표시 쪽 홈을 보면 찾을 수 있고, 트레드 표면이 이 돌기와 같은 높이가 되면 1.6mm에 닿은 거예요.</p>'),
    ('사용 방법', '<ol><li>타이어 옆면의 규격(예: 225/55R17 97V)을 적으면 각 숫자의 뜻과 바깥지름이 나와요.</li><li>다른 크기로 바꾸려면 ‘비교할 규격’에 적어요. 지름 차이와 계기판 100km/h일 때 실제 속도가 나와요.</li><li>DOT 마지막 4자리를 적으면 만든 해·주와 지금까지 몇 년 됐는지 알려 줘요.</li></ol>'),
  ],
  faq=[('타이어 숫자 225/55R17에서 55는 무엇인가요?', '편평비예요. 옆면 높이가 폭(225mm)의 55%라는 뜻으로, 옆면 높이는 123.75mm예요.'),
       ('타이어 제조일자는 어떻게 보나요?', '옆면 DOT 뒤 마지막 4자리 숫자예요. 앞 두 자리는 주, 뒤 두 자리는 연도라서 2423이면 2023년 24번째 주에 만든 거예요.'),
       ('타이어는 몇 년마다 바꿔야 하나요?', '홈 깊이가 1.6mm 아래면 반드시 바꿔야 하고, 3mm 안팎에서 미리 바꾸라는 권장이 많아요. 홈이 남아 있어도 만든 지 6년이 넘으면 바꾸는 게 좋아요.'),
       ('타이어 크기를 바꿔도 되나요?', '바깥지름 차이가 보통 ±3% 안이면 많이 쓰지만, 차 제조사가 허용한 규격인지 먼저 확인하세요. 하중 지수와 속도 기호는 원래보다 낮추지 않아야 해요.')],
  rel=REL,
  src='<li><a href="https://ownersmanual.kia.com/full_webhelp/TAMEV/2026/ko_KR/topics/chapter8_12_5.html" rel="noopener" target="_blank">기아 차량 취급설명서 — 타이어 제조일자·6년 교체</a></li><li><a href="https://www.continental-tires.com/kr/ko/tire-knowledge/tread-depth/" rel="noopener" target="_blank">콘티넨탈 타이어 — 트레드 깊이 (새 타이어 8~9mm, 1.6mm)</a></li><li>자동차 및 자동차부품의 성능과 기준에 관한 규칙 — 타이어 요철형 무늬 깊이 1.6mm · 2026-11-25 확인</li>')

if __name__ == '__main__':
    for p in (INSP, TIRE):
        print('wrote', G.page(p))
