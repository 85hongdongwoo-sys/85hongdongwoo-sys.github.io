#!/usr/bin/env python3
"""고검색 페이지 2종: 2027 최저임금·주휴수당(/life/min-wage-2027.html), 2027 건강검진 대상(/medical/checkup-2027.html).
사실 출처: 고용노동부(2027 최저임금 10,700원 고시), 국민건강보험공단(검진 출생연도 기준). 2026-11-28. 실행:
    python3 build/newpages/gen_season3.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

PAGES = []

# ── 1) 2027 최저임금·주휴수당 계산 (/life/min-wage-2027.html) ──
WAGE_TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:0 0 10px}#tool .wf{max-width:340px}#tool .wf input{text-align:right}
#wout .v{font-size:19px}#wwarn{margin:8px 0 0;padding:10px 12px;border-radius:10px;font-size:14px;display:none}
#wwarn.bad{background:#FDECEC;border:1px solid #D64545;color:#8A1C1C}#wwarn.ok{background:#E7F7EC;border:1px solid #2BA85A;color:#13743A}</style>
<h2>최저임금·주휴수당 계산기</h2>
<p class="note">2027년 최저시급은 10,700원이에요. 시급과 주 근로시간을 넣으면 주휴수당을 포함한 주급·월급을 계산하고, 최저임금 미달인지 알려 줘요.</p>
<div class="grid g2"><div class="f wf"><label for="whr">시급 (원)</label><input id="whr" type="number" inputmode="numeric" value="10700"></div>
<div class="f wf"><label for="wwk">주 근로시간 (시간)</label><input id="wwk" type="number" inputmode="numeric" value="40"></div></div>
<div class="tiles hk-tiles" id="wout"><div class="tile"><div class="k">주휴 포함 주급</div><div class="v" id="wweek">—</div></div><div class="tile light"><div class="k">월급 환산</div><div class="v" id="wmon">—</div></div></div>
<div id="wwarn"></div>
<p class="note">주 15시간 이상 일하면 주휴수당이 생겨요(월급은 주급 × 약 4.345주로 환산). 고용형태(정규·계약·알바)와 무관하게 최저임금이 적용돼요.</p>
</section>""", """<script>
(function(){var $=HL.$;var MIN=10700;
function won(n){return Math.round(n).toLocaleString()+'원';}
function calc(){var h=+$('#whr').value||0,w=Math.max(0,+$('#wwk').value||0);
 var wh=(w>=15)?Math.min(w,40)/40*8:0; // 주휴시간
 var week=(w+wh)*h, mon=week*365/7/12;
 $('#wweek').textContent=h&&w?won(week):'—';$('#wmon').textContent=h&&w?won(mon):'—';
 var el=$('#wwarn');
 if(!h){el.style.display='none';return;}
 if(h<MIN){el.className='bad';el.style.display='block';el.innerHTML='⚠ 시급 '+won(h)+'은 2027년 최저임금('+won(MIN)+')보다 낮아요. 2027년 1월부터는 최저임금 위반이에요.';}
 else{el.className='ok';el.style.display='block';el.innerHTML='✓ 2027년 최저임금('+won(MIN)+') 이상이에요.';}}
$('#whr').addEventListener('input',calc);$('#wwk').addEventListener('input',calc);calc();
})();
</script>""")
PAGES.append(dict(slug='min-wage-2027', url='/life/min-wage-2027.html', sec=('생활', '/life/'), crumb3=' › 2027 최저임금', nosafe=True, warn='',
  name='2027 최저임금 10,700원 — 주휴수당·월급 계산기 (시급·월급·위반 확인)',
  h1='2027 최저임금 <b>·주휴수당 계산</b>',
  lead='2027년 최저시급은 10,700원이에요. 시급과 근로시간을 넣으면 주휴수당 포함 주급·월급을 계산하고 최저임금 미달 여부를 알려 줘요.',
  desc='2027년 최저임금 시급 10,700원(월 2,236,300원)을 기준으로 주휴수당 포함 주급·월급을 계산하고, 내 시급이 최저임금에 미달하는지 확인해요. 2026년보다 3.7% 인상, 2027년 1월 적용.',
  tool=WAGE_TOOL, rel=('<section class="card rel"><h2>함께 보면 좋은 도구</h2><ul>'
    '<li><a href="/life/yearend-tax.html"><b>연말정산 공제 체크리스트</b></a></li>'
    '<li><a href="/life/car-tax-yearly.html"><b>자동차세 연납 할인 계산</b></a></li>'
    '<li><a href="/life/"><b>생활 도구 모음</b></a></li></ul></section>'),
  body=[
    ('2027년 최저임금은 얼마인가요', '<p>2027년 최저임금은 <b>시간당 10,700원</b>이에요. 2026년(10,320원)보다 380원, <b>3.7%</b> 올랐어요. 주 40시간(월 209시간) 기준 월 환산액은 <b>2,236,300원</b>이고, 업종 구분 없이 모든 사업장에 똑같이 적용돼요.</p>'
     '<p>고용노동부가 2026년 8월 5일에 확정·고시했고, <b>2027년 1월 1일부터 12월 31일까지</b> 적용돼요. 2026년에 일한 급여에는 적용되지 않고, 2027년 1월 1일 이후 근무분부터 새 기준이 적용돼요.</p>'),
    ('주휴수당까지 포함하면?', '<p>주 15시간 이상 일하면 <b>주휴수당</b>이 생겨요. 하루치 임금을 유급휴일로 더 주는 건데, 주 40시간 근무라면 주휴 8시간이 붙어요. 그래서 실제 받는 주급·월급은 ‘근로시간 + 주휴시간’으로 계산해요.</p>'
     '<p>위 계산기에 시급과 주 근로시간을 넣으면 주휴수당을 포함한 주급·월급이 바로 나와요. 월급은 주급에 약 4.345주를 곱해 환산해요.</p>'),
    ('누구에게 적용되나요', '<ul><li>정규직·계약직·아르바이트·일용직 등 <b>고용형태와 무관</b>하게 최저임금법이 적용되는 모든 근로자에게 적용돼요.</li><li>수습 기간이라도 원칙적으로 최저임금을 지켜야 해요(일부 단순노무 외 1년 이상 계약의 수습 3개월은 90% 감액 가능 등 예외 규정 확인).</li><li>최저임금 미만으로 주면 사업주는 3년 이하 징역 또는 2천만원 이하 벌금 대상이에요.</li></ul>'),
    ('내 월급이 최저임금 위반인지 확인하기', '<p>월급제라면 ‘월급 ÷ 월 소정근로시간(주 40시간 기준 약 209시간)’으로 시급을 환산해 10,700원 이상인지 보면 돼요. 다만 식대·교통비 등 일부 수당은 최저임금 산입 범위가 정해져 있으니, 정확한 판단은 고용노동부 기준을 확인하세요.</p>'),
  ],
  faq=[('2027년 최저임금 시급은 얼마인가요?', '시간당 10,700원이에요. 2026년(10,320원)보다 3.7% 올랐고, 월 환산액은 2,236,300원(주 40시간 기준)이에요.'),
       ('언제부터 적용되나요?', '2027년 1월 1일부터 12월 31일까지예요. 2026년 근무분에는 적용되지 않아요.'),
       ('아르바이트도 최저임금을 받나요?', '네. 정규직·계약직·알바 등 고용형태와 무관하게 적용돼요. 주 15시간 이상이면 주휴수당도 생겨요.'),
       ('최저임금보다 적게 주면 어떻게 되나요?', '최저임금 미만 지급은 위법이에요. 사업주는 3년 이하 징역 또는 2천만원 이하 벌금 대상이 될 수 있어요.')],
  src='<li>고용노동부 — 2027년 적용 최저임금 10,700원 고시 (2026-08-05, 2026-11-28 확인)</li>'
      '<li>최저임금위원회 — 2027년 최저임금 의결 (2026-07-14)</li>'))

# ── 2) 2027 건강검진 대상 확인 (/medical/checkup-2027.html) ──
CHK_TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:0 0 10px}#tool .cf{max-width:280px}
#cres{margin:8px 0 0;padding:14px 16px;border-radius:12px;font-size:16px;line-height:1.6;display:none}
#cres.y{background:#E7F7EC;border:1px solid #2BA85A}#cres.n{background:#FFF7ED;border:1px solid #FED7AA}
#cres b{font-size:18px}</style>
<h2>2027년 건강검진 대상 확인</h2>
<p class="note">2027년은 홀수 해예요. 일반건강검진은 2년 주기라, 홀수 해에는 홀수년도 출생자가 기본 대상이에요. 출생연도를 넣어 보세요.</p>
<div class="f cf"><label for="cby">출생연도 (예: 1985)</label><input id="cby" type="number" inputmode="numeric" placeholder="1985"></div>
<div id="cres"></div>
<div class="btns"><a class="btn dl" href="https://www.nhis.or.kr" target="_blank" rel="noopener">건보공단 대상조회(정확)</a></div>
<p class="note">비사무직 직장가입자는 출생연도와 상관없이 매년 대상이 될 수 있어요. 최종 대상 여부와 암검진 항목은 건보공단 조회가 가장 정확해요.</p>
</section>""", """<script>
(function(){var $=HL.$;
function go(){var y=parseInt($('#cby').value,10);var el=$('#cres');
 if(!y||y<1900||y>2027){el.style.display='none';return;}
 el.style.display='block';var odd=(y%2===1);
 if(odd){el.className='y';el.innerHTML='<b>✓ 2027년 일반건강검진 대상이에요</b><br>'+y+'년생(홀수년도)은 2027년 일반건강검진 기본 대상이에요. 연령·성별에 따라 국가암검진도 함께 받을 수 있어요.';}
 else{el.className='n';el.innerHTML='<b>2027년은 기본 대상이 아니에요</b><br>'+y+'년생(짝수년도)은 2027년엔 2년 주기 일반검진 대상이 아니에요(짝수 해 대상). 단, 비사무직 직장가입자는 매년 대상일 수 있으니 건보공단에서 꼭 확인하세요.';}}
$('#cby').addEventListener('input',go);
})();
</script>""")
PAGES.append(dict(slug='checkup-2027', url='/medical/checkup-2027.html', sec=('건강', '/medical/'), crumb3=' › 2027 건강검진 대상', nosafe=True, warn='',
  name='2027 국가건강검진 대상자 확인 — 출생연도로 홀짝 조회 (일반검진·암검진)',
  h1='2027 건강검진 <b>대상자 확인</b>',
  lead='2027년은 홀수 해라 홀수년도 출생자가 일반건강검진 기본 대상이에요. 출생연도를 넣으면 대상 여부를 바로 알려 주고, 바뀌는 검진 항목도 정리했어요.',
  desc='2027년 국가건강검진 대상자를 출생연도(홀짝)로 확인해요. 홀수 해인 2027년은 홀수년도 출생자가 일반건강검진 기본 대상이고, 비사무직 직장가입자는 매년 대상이에요. 2027년 흉부 X-ray 대상 변경도 안내해요.',
  tool=CHK_TOOL, rel=('<section class="card rel"><h2>함께 보면 좋은 도구</h2><ul>'
    '<li><a href="/medical/"><b>병원·건강 도구 모음</b></a></li>'
    '<li><a href="/calendar/dday.html"><b>디데이 계산기</b></a></li>'
    '<li><a href="/life/yearend-tax.html"><b>연말정산 체크리스트</b></a></li></ul></section>'),
  body=[
    ('2027년 건강검진, 누가 대상인가요', '<p>국가 일반건강검진은 보통 <b>2년에 한 번</b>, 출생연도를 기준으로 대상이 정해져요. <b>짝수 해에는 짝수년도 출생자, 홀수 해에는 홀수년도 출생자</b>가 대상이에요. 2027년은 홀수 해라, <b>출생연도 끝자리가 1·3·5·7·9</b>인 사람이 기본 대상이에요.</p>'
     '<ul><li>대상: 직장가입자, 세대주인 지역가입자, 20세 이상 지역가입자·피부양자 등</li><li><b>비사무직 직장가입자</b>는 출생연도와 상관없이 <b>매년</b> 검진 대상이 될 수 있어요.</li><li>연령·성별에 따라 위암·대장암·유방암·자궁경부암 등 국가암검진 대상이 추가돼요.</li></ul>'
     '<p>위 도구에서 출생연도를 넣으면 2027년 대상 여부를 바로 확인할 수 있어요. 다만 최종 대상은 국민건강보험공단 ‘건강검진 대상조회’가 가장 정확해요.</p>'),
    ('2027년부터 달라지는 검진', '<p>2027년부터 <b>흉부 방사선(X-ray) 검사 대상 나이가 20세 이상에서 50세 이상으로</b> 바뀌어요. 20~49세는 고위험 직업군에 한해 한시적으로 지원해요(2026년까지는 20세 이상이면 받을 수 있었어요).</p>'
     '<p>또 검진 후 이상 소견이 있을 때 받는 확진검사 기한이 다음 해 1월 31일에서 <b>3월 31일까지</b>로 연장됐어요. 일반검진 자체의 마감일(그해 12월 31일)이 늘어난 건 아니니 일정은 미리 잡는 게 좋아요.</p>'),
    ('검진은 어디서, 언제 받나요', '<ul><li>주소지와 상관없이 전국 어디서나 지정 검진기관에서 받을 수 있어요. 집·회사 근처 기관은 건보공단 누리집·앱에서 찾아요.</li><li>대상 연도(2027년) 1월 1일부터 12월 31일까지 받으면 돼요. 연초(봄)에 받으면 연말 혼잡을 피할 수 있어요.</li><li>직장가입자가 검진을 안 받으면 사업주·근로자에게 과태료가 부과될 수 있어요.</li></ul>'),
  ],
  faq=[('2027년 건강검진 대상은 누구인가요?', '홀수 해인 2027년은 홀수년도 출생자(끝자리 1·3·5·7·9)가 일반건강검진 기본 대상이에요. 비사무직 직장가입자는 출생연도와 무관하게 매년 대상일 수 있어요.'),
       ('짝수년생인데 2027년에 받을 수 있나요?', '2년 주기 일반검진은 2027년엔 기본 대상이 아니에요(짝수 해 대상). 다만 비사무직 직장가입자 등은 매년 대상일 수 있으니 건보공단 조회로 확인하세요.'),
       ('2027년부터 바뀌는 검진 항목이 있나요?', '흉부 X-ray 검사 대상이 20세 이상에서 50세 이상으로 바뀌어요(20~49세는 고위험 직업군 한시 지원). 확진검사 기한도 다음 해 3월 31일까지로 연장됐어요.'),
       ('검진은 어디서 받나요?', '전국 지정 검진기관 어디서나 받을 수 있어요. 국민건강보험공단 누리집·앱에서 근처 기관을 찾을 수 있어요.')],
  src='<li><a href="https://www.nhis.or.kr" rel="noopener" target="_blank">국민건강보험공단</a> — 건강검진 대상조회, 출생연도 기준 (2026-11-28 확인)</li>'
      '<li>보건복지부 제4차 국가건강검진종합계획 — 2027년 흉부 X-ray 대상 조정 (2026-11-28 확인)</li>'))

if __name__ == '__main__':
    for p in PAGES:
        print('wrote', G.page(p))
