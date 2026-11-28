#!/usr/bin/env python3
"""고검색 시즌 페이지 2종: 자동차세 연납(/life/car-tax-yearly.html), 2027 설날(/calendar/seollal-2027.html).
사실 출처: 행정안전부(연납 공제율 5%), 우주항공청 2027 월력요항. 2026-11-28 확인. 로컬 실행:
    python3 build/newpages/gen_season2.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

PAGES = []

# ── 1) 자동차세 연납 계산·안내 (/life/car-tax-yearly.html, group drive) ──
CAR_TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:24px 0 10px}#tool h2:first-of-type{margin-top:0}
#tool .cf{max-width:320px}#ctax{text-align:right}
#crow{width:100%;border-collapse:collapse;margin:8px 0}
#crow th,#crow td{border:1px solid #E3E6EB;padding:9px 10px;text-align:center;font-size:14.5px}
#crow th{background:#F4F5F7;font-weight:700}
#crow td.hl{background:#E7F7EC;font-weight:700;color:#13743A}</style>
<h2 style="margin-top:0">연납 할인액 계산기</h2>
<p class="note">1년치 자동차세(연세액)를 넣으면 신청 월별 할인액과 실제 납부액을 보여 줘요. 2026년 기준 공제율 5%로 계산해요(1월이 가장 많이 할인).</p>
<div class="f cf"><label for="ctax">자동차세 연세액 (원)</label><input id="ctax" type="number" inputmode="numeric" min="0" placeholder="예: 520000"></div>
<table id="crow"><thead><tr><th>신청 시기</th><th>적용 기간</th><th>할인액</th><th>실납부액</th></tr></thead><tbody id="cbody"></tbody></table>
<div class="btns"><a class="btn dl" href="https://www.wetax.go.kr" target="_blank" rel="noopener">위택스 (전국 연납 신청)</a><a class="btn" href="https://etax.seoul.go.kr" target="_blank" rel="noopener">서울시 이택스</a></div>
</section>""", """<script>
(function(){var $=HL.$;
// 공제율 5% × (적용 개월수/12). 1월=11개월, 3월=9개월, 6월=6개월, 9월=3개월
var M=[['1월 (16~31일경)','2~12월',11],['3월','4~12월',9],['6월','7~12월',6],['9월','10~12월',3]];
function won(n){return Math.round(n).toLocaleString()+'원';}
function calc(){var v=+$('#ctax').value||0;
 $('#cbody').innerHTML=M.map(function(m,i){var disc=v*0.05*m[2]/12;var pay=v-disc;
  return '<tr'+(i===0?' ':'')+'><td'+(i===0?' class="hl"':'')+'>'+m[0]+'</td><td>'+m[1]+'</td><td'+(i===0?' class="hl"':'')+'>'+(v?won(disc):'—')+'</td><td>'+(v?won(pay):'—')+'</td></tr>';}).join('');}
$('#ctax').addEventListener('input',calc);calc();
})();
</script>""")
PAGES.append(dict(slug='car-tax-yearly', url='/life/car-tax-yearly.html', sec=('자동차·내비', '/drive/'), crumb3=' › 자동차세 연납', nosafe=True, warn='',
  name='자동차세 연납 할인 계산기·신청 방법 (2026 공제율 5%, 위택스·이택스)',
  h1='자동차세 <b>연납 할인 계산</b>',
  lead='1년치 자동차세를 1월에 미리 내면(연납) 세금을 깎아 줘요. 연세액을 넣으면 신청 월별 할인액을 계산하고, 신청 기간·방법도 정리했어요.',
  desc='자동차세 연납 할인액을 연세액으로 계산하고, 1·3·6·9월 신청 시기별 공제율(2026년 기준 5%), 위택스·이택스 신청 방법, 중도 매각 환급까지 정리했어요.',
  tool=CAR_TOOL, rel=('<section class="card rel"><h2>함께 보면 좋은 도구</h2><ul>'
    '<li><a href="/life/taxi-fare.html"><b>택시비·통행료 계산기</b></a></li>'
    '<li><a href="/life/yearend-tax.html"><b>연말정산 공제 체크리스트</b></a></li>'
    '<li><a href="/drive/"><b>자동차·내비 도구 모음</b></a></li></ul></section>'),
  body=[
    ('자동차세 연납이란', '<p>자동차세는 원래 1년에 두 번(6월·12월) 나눠 내요. 이걸 <b>1월에 1년치를 한 번에 미리 내면(연납)</b> 남은 기간만큼 세금을 깎아 주는 제도예요. 확정적인 절세라 ‘세테크 필수 코스’로 꼽혀요.</p>'
     '<p>2026년 기준 공제율은 <b>5%</b>예요(행정안전부). 과거엔 10%였지만 단계적으로 내려와 2025·2026년은 5%로 유지됐어요. 2027년 공제율은 행안부 확정 공지로 확인하세요.</p>'),
    ('언제 신청해야 가장 많이 할인되나요', '<p>연납은 1·3·6·9월에 신청할 수 있는데, <b>빠를수록(1월) 할인이 가장 커요.</b> 남은 개월 수가 많을수록 깎이는 금액이 크기 때문이에요(공제율 5% × 남은 개월/12).</p>'
     '<table class="tbl"><thead><tr><th>신청 시기</th><th>적용 기간</th><th>실질 할인율(연세액 대비)</th></tr></thead><tbody>'
     '<tr><td>1월</td><td>2~12월 (11개월)</td><td>약 4.6%</td></tr>'
     '<tr><td>3월</td><td>4~12월 (9개월)</td><td>약 3.8%</td></tr>'
     '<tr><td>6월</td><td>7~12월 (6개월)</td><td>약 2.5%</td></tr>'
     '<tr><td>9월</td><td>10~12월 (3개월)</td><td>약 1.3%</td></tr></tbody></table>'
     '<p>위 계산기에 연세액을 넣으면 시기별 할인액이 바로 나와요. 1월 신청기간은 보통 1월 16일~31일경이에요(연도별로 1월 중순~2월 초 운영).</p>'),
    ('어디서, 어떻게 신청하나요', '<ul><li><b>전국</b> — 위택스(wetax.go.kr) 또는 스마트위택스 앱</li><li><b>서울</b> — 이택스(etax.seoul.go.kr)·STAX 앱</li><li>간편인증으로 로그인하면 내 자동차세가 바로 조회돼요. 카드사별 무이자 할부·포인트 결제 혜택도 챙기면 좋아요.</li></ul>'
     '<p>한 번 연납을 신청하면 이후에는 매년 1월에 연납 고지서가 자동으로 오는 경우가 많아요.</p>'),
    ('차를 중간에 팔면 손해인가요', '<p>아니에요. 연납 후 <b>중도에 차량을 처분하면 남은 기간분을 환급</b>받아요. 그래서 연납해 두고 차를 팔아도 불이익이 없어요. 연납은 할인을 확정으로 받는 만큼, 보유 중이라면 1월에 신청하는 게 유리해요.</p>'),
  ],
  faq=[('자동차세 연납 할인율은 얼마인가요?', '2026년 기준 공제율은 5%예요. 1월에 신청하면 남은 11개월분에 적용돼 연세액의 약 4.6%를 할인받아요. 신청이 늦을수록 할인폭이 줄어요.'),
       ('연납은 어디서 신청하나요?', '전국은 위택스(wetax.go.kr)·스마트위택스 앱, 서울은 이택스(etax.seoul.go.kr)에서 신청해요. 간편인증 로그인하면 자동 조회돼요.'),
       ('1월을 놓치면 연납 못 하나요?', '3월·6월·9월에도 신청할 수 있어요. 다만 적용 기간이 줄어 할인폭이 작아져요. 9월 신청이 그해 마지막 기회예요.'),
       ('연납 후 차를 팔면 어떻게 되나요?', '남은 기간분을 환급받아요. 불이익이 없으니 보유 중이면 1월 연납이 유리해요.')],
  src='<li><a href="https://www.wetax.go.kr" rel="noopener" target="_blank">위택스</a>·서울 이택스 — 자동차세 연납 신청 (2026-11-28 확인)</li>'
      '<li>행정안전부 — 2026년 자동차세 연납 공제율 5% (지방세법 시행령, 2026-11-28 확인)</li>'))

# ── 2) 2027 설날 가이드 (/calendar/seollal-2027.html, group calendar) ──
SEOL_TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:0 0 10px}
#sdday{font-size:40px;font-weight:800;color:#C0392B;text-align:center;margin:6px 0}
#sdday small{display:block;font-size:15px;color:#5B6B82;font-weight:600;margin-top:2px}</style>
<h2>2027 설날까지</h2>
<div id="sdday">—</div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">설날 당일</div><div class="v">2월 7일 (일)</div></div><div class="tile"><div class="k">연휴</div><div class="v">2/6~2/9 (4일)</div></div><div class="tile light"><div class="k">대체공휴일</div><div class="v">2월 9일 (화)</div></div></div>
<p class="note">연차 1~2일을 앞뒤로 붙이면 더 길게 쉴 수 있어요. 열차 예매일·택배 마감은 매년 명절 약 한 달 전 코레일·택배사 공지로 확인하세요.</p>
</section>""", """<script>
(function(){var $=HL.$;var t=new Date('2027-02-06T00:00:00+09:00');
function upd(){var now=new Date();var d=Math.ceil((t-now)/86400000);
 if(d>0)$('#sdday').innerHTML='D-'+d+'<small>2027년 2월 6일 연휴 시작</small>';
 else if(d===0)$('#sdday').innerHTML='오늘!<small>설 연휴 시작</small>';
 else $('#sdday').innerHTML='설 연휴<small>지났어요</small>';}
upd();
})();
</script>""")
PAGES.append(dict(slug='seollal-2027', url='/calendar/seollal-2027.html', sec=('날짜·달력', '/calendar/'), crumb3=' › 2027 설날', nosafe=True, warn='',
  name='2027 설날 날짜·연휴 (2월 7일, 연휴 2/6~2/9 4일, 대체공휴일 2/9)',
  h1='2027 설날 <b>날짜·연휴</b>',
  lead='2027년 설날은 2월 7일(일)이고, 연휴는 2월 6일(토)부터 9일(화)까지 4일이에요. D-day, 연차 활용, 귀성 준비까지 한눈에 정리했어요.',
  desc='2027년 설날(구정)은 2월 7일 일요일, 연휴는 2월 6일~9일 4일이고 2월 9일이 대체공휴일이에요. D-day 카운트다운, 연차 활용, 열차 예매·택배·세뱃돈 준비를 정리했어요.',
  tool=SEOL_TOOL, rel=('<section class="card rel"><h2>함께 보면 좋은 도구</h2><ul>'
    '<li><a href="/calendar/holidays.html"><b>2027 공휴일·대체공휴일</b></a></li>'
    '<li><a href="/calendar/dday.html"><b>디데이 계산기</b></a></li>'
    '<li><a href="/calendar/"><b>날짜·달력 도구 모음</b></a></li></ul></section>'),
  body=[
    ('2027년 설날은 며칠인가요', '<p>2027년 설날(음력 1월 1일)은 <b>2월 7일 일요일</b>이에요. 설 연휴는 설날 전날과 다음 날을 포함해 <b>2월 6일(토)부터 2월 9일(화)까지 나흘</b>이에요.</p>'
     '<ul><li>2월 6일(토) — 설 연휴 (전날)</li><li>2월 7일(일) — 설날 당일</li><li>2월 8일(월) — 설 연휴 (다음 날)</li><li>2월 9일(화) — <b>대체공휴일</b> (설날이 일요일과 겹쳐 생김)</li></ul>'
     '<p>설날이 일요일이라 하루가 대체공휴일로 밀려 나흘 연휴가 됐어요.</p>'),
    ('연차를 붙이면 얼마나 쉴 수 있나요', '<p>2월 10일(수)·11일(목)·12일(금)에 <b>연차 3일</b>을 붙이면, 2월 6일(토)부터 2월 14일(일)까지 <b>최대 9일</b>을 이어서 쉴 수 있어요. 연차 2일(10·11일)만 써도 금요일 하루만 일하고 긴 휴가가 돼요.</p>'
     '<p>2027년은 토·일에 겹친 공휴일이 많아 대체공휴일이 7일이나 생기고, 3일 이상 황금연휴가 10번이라 연차 계획을 미리 세우면 좋아요.</p>'),
    ('귀성 준비 — 열차·고속도로·택배', '<ul><li><b>열차(KTX·SRT)</b> — 명절 승차권은 보통 설 약 한 달 전에 코레일·SR에서 예매를 받아요. 정확한 2027 설 예매일은 코레일 공지로 확인하세요.</li><li><b>고속도로</b> — 연휴 교통량은 한국도로공사의 설 연휴 교통전망으로 미리 확인하면 혼잡을 피할 수 있어요.</li><li><b>택배</b> — 명절 전 택배 물량이 몰려 배송이 지연돼요. 선물은 연휴 1~2주 전에 미리 보내는 게 안전해요(택배사별 명절 마감일 공지 확인).</li></ul>'),
    ('세뱃돈·차례상 참고', '<p><b>세뱃돈</b>은 정해진 금액은 없지만, 보통 미취학·초등은 1만원, 중·고등은 3~5만원, 성인은 5~10만원 선을 많이 해요(가정·형편에 따라 다름).</p>'
     '<p><b>차례상</b>은 성균관의례정립위원회가 간소화 기준(기본 음식 중심, 기름에 튀기거나 지지는 음식은 꼭 올리지 않아도 됨)을 권고했어요. 형식보다 가족이 모이는 데 의미를 두는 흐름이에요.</p>'),
  ],
  faq=[('2027년 설날은 며칠인가요?', '2027년 설날은 2월 7일 일요일이에요. 연휴는 2월 6일(토)부터 9일(화)까지 나흘이에요.'),
       ('2027 설날 대체공휴일은 언제인가요?', '2월 9일 화요일이에요. 설날이 일요일과 겹쳐 하루가 대체공휴일로 지정됐어요.'),
       ('연차를 붙이면 며칠 쉴 수 있나요?', '2월 10~12일에 연차 3일을 붙이면 2월 6일부터 14일까지 최대 9일 연휴를 만들 수 있어요.'),
       ('설날 열차표는 언제 예매하나요?', '보통 설 약 한 달 전에 코레일·SR이 명절 승차권 예매를 받아요. 2027년 정확한 예매일은 코레일 공지로 확인하세요.')],
  src='<li>우주항공청 「2027년 월력요항」 — 설날 2월 7일, 대체공휴일 2월 9일 (2026-11-28 확인)</li>'
      '<li>인사혁신처 「관공서의 공휴일에 관한 규정」 — 대체공휴일 기준 (2026-11-28 확인)</li>'))

if __name__ == '__main__':
    for p in PAGES:
        print('wrote', G.page(p))
