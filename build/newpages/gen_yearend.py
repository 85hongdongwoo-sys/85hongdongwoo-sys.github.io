#!/usr/bin/env python3
"""연말정산 공제 체크리스트·일정 안내 (/life/yearend-tax.html). 2026-11-28.
사실 출처: 국세청 홈택스, 연합/머니투데이 등 2026-귀속 연말정산 보도. 로컬 실행:
    python3 build/newpages/gen_yearend.py"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

# [항목, 설명, 간소화 자동조회(True)/직접챙김(False)]
ITEMS = [
 ['신용·체크카드, 현금영수증', '총급여의 25%를 넘는 사용분부터 공제돼요. 대중교통·전통시장·문화비는 공제율이 더 높아요.', True],
 ['의료비', '총급여의 3%를 넘는 금액부터 공제. 안경·콘택트렌즈는 1명당 50만원까지 되는데 간소화에 안 뜨면 영수증을 직접 내야 해요.', False],
 ['교육비', '본인·자녀 학비, 취학 전 아동 학원비 등. 대부분 간소화에서 조회돼요.', True],
 ['보장성 보험료', '자동차·실손 등 보장성 보험료. 간소화 자동 조회.', True],
 ['기부금', '종교·법정·지정 기부금. 일부 단체는 간소화에 안 떠서 기부금 영수증을 직접 받아야 해요.', False],
 ['월세 세액공제', '무주택 세대주·총급여 8천만원 이하 대상. 2026년 귀속분부터 공제율이 15%로 올랐어요. 임대차계약서·월세 이체 증빙을 직접 제출해요.', False],
 ['주택청약저축', '무주택 세대주의 청약 납입액 소득공제. 무주택 확인서가 필요할 수 있어요.', False],
 ['연금저축·IRP', '연금저축과 IRP를 합쳐 세액공제를 받아요. 연말에 추가 납입하면 공제가 늘어요(노후 대비 겸 절세).', True],
 ['주택자금 이자', '전세자금·주택담보대출 이자 상환액. 간소화에서 조회되는 경우가 많아요.', True],
 ['부양가족 인적공제', '연소득 100만원(근로소득만 있으면 총급여 500만원) 이하인 가족만 올릴 수 있어요. 잘못 올리면 나중에 추징돼요.', False],
 ['중소기업 취업자 소득세 감면', '청년·고령자·장애인 등 요건에 맞으면 소득세를 감면받아요. 회사에 감면 신청서를 내야 해요.', False],
]
items_js = json.dumps(ITEMS, ensure_ascii=False)

TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:24px 0 10px}#tool h2:first-of-type{margin-top:0}
#ylist label{display:flex;gap:10px;align-items:flex-start;padding:11px 12px;border:1px solid #E3E6EB;border-radius:12px;margin:7px 0;cursor:pointer;background:#fff}
#ylist label:hover{border-color:#1D4ED8}
#ylist input{margin-top:3px;width:18px;height:18px;flex:none}
#ylist .yn{font-weight:700;color:#1F2937}
#ylist .yt{display:block;font-weight:400;color:#5B6B82;font-size:13.5px;margin-top:2px;line-height:1.55}
#ylist .ym{display:inline-block;margin-left:6px;font-size:11.5px;font-weight:700;color:#B45309;background:#FEF3C7;border-radius:6px;padding:1px 6px;vertical-align:middle}
#yprep{margin:6px 0 0;padding:12px 14px;background:#FFF7ED;border:1px solid #FED7AA;border-radius:12px;font-size:14px;line-height:1.7;display:none}
#yprep b{color:#9A3412}</style>
<h2 style="margin-top:0">홈택스 바로가기</h2>
<p class="note">간소화 서비스는 매년 1월 중순(보통 1월 15일경) 홈택스에서 열려요. 그 전에 ‘연말정산 미리보기’로 예상 세액을 확인할 수 있어요. 정확한 2027년 일정은 국세청 공지로 확인하세요.</p>
<div class="btns"><a class="btn dl" href="https://www.hometax.go.kr" target="_blank" rel="noopener">홈택스 (간소화·미리보기)</a><a class="btn" href="https://www.nts.go.kr" target="_blank" rel="noopener">국세청 (일정 공지)</a></div>
<h2>내 공제 체크리스트</h2>
<p class="note">해당되는 항목을 체크하세요. <b style="color:#B45309">직접챙김</b> 표시는 간소화에 안 뜰 수 있어 영수증·서류를 직접 준비해야 하는 항목이에요.</p>
<div id="ylist"></div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">챙긴 공제</div><div class="v" id="ycnt">0개</div></div><div class="tile light"><div class="k">직접 준비할 자료</div><div class="v" id="ymcnt">0건</div></div></div>
<div id="yprep"></div>
</section>""", """<script>
(function(){var $=HL.$;var I="""+items_js+""";
$('#ylist').innerHTML=I.map(function(it,i){return '<label><input type="checkbox" data-i="'+i+'"><span class="yn">'+it[0]+(it[2]?'':'<span class="ym">직접챙김</span>')+'<span class="yt">'+it[1]+'</span></span></label>';}).join('');
function upd(){var cs=$('#ylist').querySelectorAll('input:checked');var n=cs.length,prep=[];
 for(var k=0;k<cs.length;k++){var i=+cs[k].getAttribute('data-i');if(!I[i][2])prep.push(I[i][0]);}
 $('#ycnt').textContent=n+'개';$('#ymcnt').textContent=prep.length+'건';
 if(prep.length){$('#yprep').style.display='block';$('#yprep').innerHTML='<b>직접 준비할 자료</b><br>간소화에 안 뜰 수 있어요. 영수증·계약서·신청서를 미리 챙기세요 — '+prep.join(' · ');}
 else $('#yprep').style.display='none';}
$('#ylist').querySelectorAll('input').forEach(function(c){c.addEventListener('change',upd);});upd();
})();
</script>""")

P = dict(slug='yearend-tax', url='/life/yearend-tax.html', sec=('생활', '/life/'), crumb3=' › 연말정산 체크리스트', nosafe=True, warn='',
  name='연말정산 공제 체크리스트·일정 (2026년 귀속, 2027년 진행) — 간소화·놓친 공제 찾기',
  h1='연말정산 <b>공제 체크리스트</b>',
  lead='2026년 귀속 연말정산(2027년 초 진행)의 공제 항목을 체크리스트로 점검하고, 간소화에 안 뜨는 ‘직접 챙길 자료’를 놓치지 않게 알려 줘요. 일정과 바뀐 점도 정리했어요.',
  desc='2026년 귀속 연말정산(2027년 1~2월 진행) 공제 항목 체크리스트, 간소화 서비스 일정, 월세·주택청약 등 바뀐 공제를 정리했어요. 해당 항목을 체크하면 직접 준비할 서류를 알려 줘요.',
  tool=TOOL, rel=('<section class="card rel"><h2>함께 보면 좋은 도구</h2><ul>'
    '<li><a href="/life/invest.html"><b>연금저축·IRP 세액공제 계산</b><span>연말 추가납입 절세</span></a></li>'
    '<li><a href="/calendar/holidays.html"><b>2027 공휴일·대체공휴일</b></a></li>'
    '<li><a href="/life/"><b>생활 도구 모음</b><span>행정·금융 생활 도구</span></a></li></ul></section>'),
  body=[
    ('연말정산, 언제 어떻게 진행되나요', '<p>2026년 귀속 연말정산은 <b>2026년 1~12월에 받은 급여와 지출</b>을 기준으로, <b>2027년 1~2월</b>에 진행해요. 간소화 서비스는 매년 1월 중순(보통 1월 15일경)에 홈택스에서 열리고, 정산 결과(환급 또는 추가납부)는 대부분 2월 급여에 반영돼요.</p>'
     '<ul><li><b>2026년 11~12월</b> — ‘연말정산 미리보기’로 예상 세액 확인, 남은 기간 절세(연금계좌 납입 등)</li><li><b>2027년 1월</b> — 간소화 서비스 개통, 자료 조회</li><li><b>2027년 1~2월</b> — 회사에 공제 자료 제출</li><li><b>2027년 2~3월</b> — 환급·추가납부 반영</li></ul>'
     '<p>정확한 2027년 개통일·제출 기한은 회사마다, 그리고 국세청 공지에 따라 달라질 수 있으니 인사부서와 홈택스 공지를 확인하세요.</p>'),
    ('13월의 월급? 환급 구조 먼저 이해하기', '<p>연말정산은 ‘돈을 많이 썼다고 환급이 늘어나는’ 구조가 아니에요. <b>1년간 미리 낸 세금(원천징수)과 실제 내야 할 세금(결정세액)의 차이</b>를 정산하는 거예요. 미리 낸 게 많으면 돌려받고(환급), 적으면 더 내요(추가납부).</p>'
     '<p>그래서 환급을 늘리려면 ‘요건에 맞는 공제를 빠짐없이 챙기는 것’이 핵심이에요. 위 체크리스트로 내가 받을 수 있는 공제를 점검해 보세요.</p>'),
    ('2026년 귀속부터 달라지는 공제', '<p>해마다 공제 제도가 조금씩 바뀌어요. 2026년 귀속분에서 눈에 띄는 변화예요(세부 요건·시행 여부는 국세청 확정 공지 기준).</p>'
     '<ul><li><b>월세 세액공제 확대</b> — 공제율이 12%에서 15%로, 한도가 연 750만원에서 1,000만원으로 올랐어요(총급여 7,000만원 이하 등 요건).</li><li><b>주택청약·결혼 관련 세액공제</b> 등 신설·확대 항목이 있어요. 본인 해당 여부는 홈택스·국세청 안내로 확인하세요.</li></ul>'
     '<p>이런 변화는 매년 1월 국세청이 확정 안내하니, 미리보기 단계에서 내 항목에 적용되는지 보는 게 좋아요.</p>'),
    ('놓치기 쉬운 공제 — 직접 챙겨야 하는 것', '<p>간소화 서비스가 대부분 자동으로 불러오지만, <b>간소화에 안 뜨는 항목</b>은 본인이 영수증·서류를 직접 내야 해요. 자주 놓치는 것들이에요.</p>'
     '<ul><li><b>안경·콘택트렌즈</b> — 1명당 50만원까지. 간소화에 없으면 구입 영수증을 판매처에서 받아요.</li><li><b>월세</b> — 임대차계약서와 월세 이체 증빙(계좌이체 내역 등)을 직접 제출.</li><li><b>일부 기부금</b> — 간소화에 안 뜨는 단체는 기부금 영수증을 직접 받기.</li><li><b>부양가족 인적공제</b> — 연소득 100만원(근로만 있으면 총급여 500만원) 이하만. 잘못 올리면 가산세와 함께 추징돼요.</li></ul>'
     '<p>위 체크리스트에서 <b style="color:#B45309">직접챙김</b> 표시 항목을 체크하면, 준비할 자료를 한 번에 모아 보여 줘요.</p>'),
  ],
  faq=[('2026년 귀속 연말정산은 언제 하나요?', '2026년 1~12월 소득을 기준으로 2027년 1~2월에 진행해요. 간소화 서비스는 보통 1월 15일경 홈택스에서 열려요.'),
       ('연말정산 미리보기는 언제부터 되나요?', '보통 전년도 11월 초 전후에 홈택스에서 열려요. 예상 세액을 확인하고 연말에 연금계좌 납입 등으로 절세할 수 있어요.'),
       ('간소화에 다 나오는데 따로 챙길 게 있나요?', '네. 안경·콘택트렌즈, 월세, 일부 기부금, 부양가족 요건 등은 간소화에 안 뜰 수 있어 영수증·계약서를 직접 준비해야 해요.'),
       ('돈을 많이 쓰면 환급을 많이 받나요?', '아니요. 연말정산은 미리 낸 세금과 실제 세금의 차이를 정산하는 거예요. 요건에 맞는 공제를 빠짐없이 챙기는 게 환급의 핵심이에요.'),
       ('2026년 귀속분에 바뀐 공제가 있나요?', '월세 세액공제율이 15%로, 한도가 1,000만원으로 올랐고, 주택청약·결혼 관련 공제 등 변화가 있어요. 본인 적용 여부는 국세청 안내로 확인하세요.')],
  src='<li><a href="https://www.hometax.go.kr" rel="noopener" target="_blank">국세청 홈택스</a> — 연말정산 간소화·미리보기 (2026-11-28 확인)</li>'
      '<li>국세청 보도자료·연합뉴스·머니투데이 등 — 간소화 1월 15일 개통, 2026년 귀속 월세·공제 변경 (2026-11-28 확인)</li>')

if __name__ == '__main__':
    print('wrote', G.page(P))
