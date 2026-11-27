#!/usr/bin/env python3
"""교원임용 선발·경쟁률·합격선 안내 페이지 (/ipsi/imyong.html).
교육부·시도교육청 공식 발표 기준(2026-11-27 확인). 로컬 실행:
    python3 build/newpages/gen_imyong.py"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

# 전국 선발인원 추이 (교육부/연합뉴스·뉴시스 공식 집계) — [학년도, 인원]
JUNG = [['2025', 5504], ['2026', 7147], ['2027', 4932]]   # 공립 중등 교과
CHO = [['2024', 3157], ['2025', 4272], ['2026', 3113], ['2027', 2821]]  # 공립 초등 (2027 사전예고)
trend_js = json.dumps({'중등': JUNG, '초등': CHO}, ensure_ascii=False)

TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:24px 0 10px}#tool h2:first-of-type{margin-top:0}
#tool .seg{display:inline-flex;border:1px solid #D9DDE3;border-radius:999px;overflow:hidden;margin-bottom:6px}
#tool .seg button{border:0;background:#fff;color:#1F2937;padding:8px 20px;font-size:15px;font-weight:700;font-family:inherit;cursor:pointer}
#tool .seg button[aria-pressed=true]{background:#1D4ED8;color:#fff}</style>
<h2 style="margin-top:0">연도별 선발인원 추이 (전국 공립)</h2>
<div class="seg" id="seg"><button data-k="중등" aria-pressed="true">중등 교과</button><button data-k="초등">초등</button></div>
<div class="tiles hk-tiles" id="trend"></div>
<p class="note" id="tnote"></p>
<h2>합격선·경쟁률 공식 확인</h2>
<p class="note">지역별·과목별 1차 합격선과 경쟁률은 교육청이 공식 공개해요(합격자 3명 이상 과목). 아래에서 내 지역·과목을 바로 확인하세요.</p>
<div class="btns"><a class="btn dl" href="https://www.edurecruit.go.kr" target="_blank" rel="noopener">교직원 채용시스템 (성적·합격선)</a><a class="btn" href="https://www.moe.go.kr" target="_blank" rel="noopener">교육부 (선발계획)</a></div>
</section>""", """<script>
(function(){var $=HL.$;var T="""+trend_js+""";var cur='중등';
var NOTE={'중등':'공립 중등 교과 교사 선발인원이에요. 2026학년도에 고교학점제·과밀학급 대응으로 크게 늘었다가, 2027학년도는 4,932명으로 2,215명 줄었어요(서울 900→553, 경기 2,250→1,523 등 수도권이 특히 감소).','초등':'공립 초등 교사 선발인원이에요. 늘봄학교 수요로 2025학년도에 크게 늘었다가 다시 줄어드는 흐름이에요. 2027학년도는 사전예고 기준 2,821명이에요.'};
function draw(){var d=T[cur];var mx=Math.max.apply(null,d.map(function(x){return x[1]}));
 $('#trend').innerHTML=d.map(function(x,i){var last=i===d.length-1;return '<div class="tile'+(last?'':' light')+'"><div class="k">'+x[0]+'학년도</div><div class="v">'+x[1].toLocaleString()+'명</div></div>'}).join('');
 $('#tnote').textContent=NOTE[cur];
 var bs=$('#seg').querySelectorAll('button');for(var i=0;i<bs.length;i++)bs[i].setAttribute('aria-pressed', bs[i].getAttribute('data-k')===cur);}
$('#seg').querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){cur=b.getAttribute('data-k');draw();});});
draw();
})();
</script>""")

P = dict(slug='imyong', url='/ipsi/imyong.html', sec=('입시·시험', '/ipsi/'), crumb3=' › 교원임용', nosafe=True, warn='',
  name='교원임용 선발인원·경쟁률·1차 합격선 (중등·초등 연도별·지역별)',
  h1='교원임용 <b>선발·경쟁률·합격선</b>',
  lead='중등·초등 교원임용 연도별 선발인원 추이, 올해 지역 변화, 1차 필기 합격선과 경쟁률을 공식 자료 기준으로 모았어요. 지역·과목별 합격선은 공식 공개처로 바로 연결해요.',
  desc='공립 중등·초등 교원임용 선발인원 연도별 추이(2024~2027), 2027학년도 지역별 변화, 1차 필기 합격선 공개 규정과 경쟁률 구조를 교육부·시도교육청 공식 자료로 정리했어요. 지역별·과목별 합격선은 교직원 채용시스템에서 확인하는 법을 안내해요.',
  tool=TOOL, rel=('<section class="card rel"><h2>함께 보면 좋은 시험 정보</h2><ul>'
    '<li><a href="/ipsi/hanneung.html"><b>한국사능력검정 기출·급수</b><span>임용 응시자격(한능검)도 여기서</span></a></li>'
    '<li><a href="/ipsi/gong9.html"><b>공무원 9급 기출문제</b><span>국가직·지방직 공식 기출</span></a></li>'
    '<li><a href="/ipsi/suneung-2027.html"><b>2027 수능 등급컷·백분위</b></a></li>'
    '<li><a href="/calendar/exam-schedule.html"><b>자격증 시험일정 달력</b><span>원서접수·시험일 한눈에</span></a></li></ul></section>'),
  body=[
    ('중등·초등 임용, 몇 명이나 뽑나요 (선발 추이)', '<p>교원임용 선발인원은 학령인구와 교원 수급계획에 따라 해마다 크게 바뀌어요. 공식 집계 기준으로 최근 흐름은 이래요.</p>'
     '<table class="tbl"><thead><tr><th>학년도</th><th>공립 중등(교과)</th><th>공립 초등</th></tr></thead><tbody>'
     '<tr><td>2024</td><td>—</td><td>3,157명</td></tr>'
     '<tr><td>2025</td><td>5,504명</td><td>4,272명</td></tr>'
     '<tr><td>2026</td><td>7,147명</td><td>3,113명</td></tr>'
     '<tr><td>2027</td><td>4,932명(확정)</td><td>2,821명(예고)</td></tr></tbody></table>'
     '<p>중등은 2026학년도에 고교학점제·과밀학급 대응으로 크게 늘었다가, 2027학년도는 4,932명으로 2,215명 줄었어요. 초등은 늘봄학교 수요로 2025학년도에 반짝 늘었다가 다시 감소세예요. 위 추이 도구에서 중등·초등을 바꿔 가며 볼 수 있어요.</p>'),
    ('2027학년도 지역별 변화', '<p>2027학년도 공립 중등 교과는 전국 4,932명이에요. 수도권 감소 폭이 특히 컸어요.</p>'
     '<table class="tbl"><thead><tr><th>지역</th><th>2026 모집</th><th>2027</th></tr></thead><tbody>'
     '<tr><td>서울(중등)</td><td>900명</td><td>553명</td></tr>'
     '<tr><td>경기(공립 중등 교과)</td><td>2,250명</td><td>1,523명</td></tr>'
     '<tr><td>전북(중등)</td><td>—</td><td>240명</td></tr>'
     '<tr><td>경북(중등)</td><td>—</td><td>117명</td></tr></tbody></table>'
     '<p>초등도 서울 267명, 경기 883명 등으로 전년보다 줄었어요. 나머지 시·도의 과목별 인원은 각 교육청 시행계획 공고(중등은 9월 30일, 유·초는 9월 9일 공고)와 교육부 취합 자료에서 확인할 수 있어요. 지역을 옮기는 것만으로 당락이 갈릴 만큼 지역별 편차가 크니, 지원 전 반드시 원문 공고를 확인하세요.</p>'),
    ('경쟁률은 어떻게 정해지나요', '<p>임용은 1차(필기)에서 <b>모집 인원의 1.5배수</b>를 뽑고, 그 합격자만 2차(수업실연·면접 등)를 봐요. 합격선에 걸린 동점자는 모두 합격 처리해요.</p>'
     '<ul><li>1차 과목: 1교시 교육학(20점), 2·3교시 전공 A·B(각 40점). 2027학년도부터 한국사는 한국사능력검정시험으로 대체돼요.</li><li>평균 경쟁률은 지역·과목마다 크게 달라요. 예를 들어 2026학년도 대전 중등은 평균 8.7대 1이었고, 모집 1명인 과목은 수십 대 1까지 치솟기도 해요.</li><li>모집 인원이 많은 수도권은 경쟁률이 낮아 보여도 지원자가 많고, 소수 모집 지역은 ‘눈치 싸움’으로 경쟁률이 크게 요동쳐요.</li></ul>'),
    ('1차 필기 합격선(커트라인) 확인법', '<p>지역별·과목별 <b>1차 합격선은 교육청이 공식 공개</b>해요. 1차 합격자 발표 때 <b>합격자가 3명 이상인 과목</b>은 합격선(커트라인)을 공개하고, 1명만 뽑는 과목은 개인정보 보호를 위해 비공개로 해요.</p>'
     '<ol><li>온라인 교직원 채용시스템(edurecruit.go.kr)에서 본인 성적과 과목별 합격선을 확인해요.</li><li>각 시·도교육청 누리집 ‘고시/공고’에도 과목별 합격선·경쟁률이 올라와요.</li><li>같은 과목이라도 지역에 따라 합격선이 10점 이상 벌어지기도 해요. 그래서 커트라인은 ‘난이도’보다 지역·과목 선택 전략의 문제예요.</li></ol>'
     '<p>교육청은 1차 합격자 발표 공고의 붙임 자료로 <b>과목별 1차 합격선</b>을 공개해요(합격자 3명 이상 과목). 아래는 2026학년도 서울·경기 공립 일반 모집의 과목별 1차 합격선(원점수)이에요. 같은 과목도 지역에 따라 꽤 달라요.</p>'
     '<table class="tbl"><thead><tr><th>과목 (2026학년도)</th><th>서울</th><th>경기</th></tr></thead><tbody>'
     '<tr><td>국어</td><td>67.00</td><td>65.00</td></tr>'
     '<tr><td>수학</td><td>57.00</td><td>52.67</td></tr>'
     '<tr><td>영어</td><td>67.33</td><td>63.33</td></tr>'
     '<tr><td>물리</td><td>45.00</td><td>47.67</td></tr>'
     '<tr><td>화학</td><td>50.33</td><td>54.33</td></tr>'
     '<tr><td>생물</td><td>61.67</td><td>66.00</td></tr>'
     '<tr><td>지구과학</td><td>52.00</td><td>55.00</td></tr>'
     '<tr><td>일반사회</td><td>82.00</td><td>78.33</td></tr>'
     '<tr><td>역사</td><td>73.67</td><td>68.67</td></tr>'
     '<tr><td>지리</td><td>82.00</td><td>86.00</td></tr>'
     '<tr><td>도덕·윤리</td><td>67.67</td><td>67.34</td></tr>'
     '<tr><td>체육</td><td>70.33</td><td>70.00</td></tr>'
     '<tr><td>음악</td><td>73.67</td><td>70.00</td></tr>'
     '<tr><td>미술</td><td>74.00</td><td>66.67</td></tr>'
     '<tr><td>기술</td><td>64.33</td><td>59.33</td></tr>'
     '<tr><td>가정</td><td>61.33</td><td>55.67</td></tr>'
     '<tr><td>정보·컴퓨터</td><td>56.67</td><td>49.00</td></tr>'
     '<tr><td>전기</td><td>64.00</td><td>71.33</td></tr>'
     '<tr><td>전자</td><td>—</td><td>63.00</td></tr>'
     '<tr><td>기계</td><td>—</td><td>65.67</td></tr>'
     '<tr><td>디자인</td><td>—</td><td>66.33</td></tr>'
     '<tr><td>일본어</td><td>—</td><td>71.33</td></tr>'
     '<tr><td>중국어</td><td>—</td><td>82.00</td></tr>'
     '<tr><td>한문</td><td>—</td><td>75.33</td></tr>'
     '<tr><td>미용</td><td>—</td><td>81.33</td></tr>'
     '<tr><td>특수(중등)</td><td>70.33</td><td>67.00</td></tr>'
     '<tr><td>보건(중등)</td><td>60.00</td><td>55.33</td></tr>'
     '<tr><td>영양(중등)</td><td>70.33</td><td>71.00</td></tr>'
     '<tr><td>사서(중등)</td><td>84.33</td><td>80.67</td></tr>'
     '<tr><td>전문상담(중등)</td><td>75.67</td><td>70.00</td></tr></tbody></table>'
     '<p class="note">※ 2026학년도 공립 일반 모집 1차 합격선(원점수, 교육학+전공 100점 환산 전 원점수 기준), 각 교육청 1차 합격자 공고 자료 기준이에요. 합격자 2명 이하 과목, 국립·장애 구분 모집은 개인정보 보호로 비공개라 ‘—’로 뒀어요. 서울에 ‘—’인 과목(전자·기계·중국어 등)은 해당 연도에 선발이 없거나 비공개인 경우예요.</p>'
     '<p>전국으로 넓혀 보면 같은 과목도 지역 차가 훨씬 커요. 예를 들어 2026학년도 영어 1차 합격선은 광주 73.34점이 최고, 인천·제주 60.00점이 최저였어요. 다른 지역·연도·과목은 아래 공식 공개처(교직원 채용시스템·각 교육청 1차 합격 공고)에서 본인 과목으로 확인하세요.</p>'),
    ('임용시험 일정 (2027학년도 기준)', '<p>1차 필기시험은 중등이 11월 28일(토), 초등은 11월 7일에 치러요(지역별로 다를 수 있어요). 2차 시험은 이듬해 1월 중 실기·실험평가(체육·음악·미술·과학 등), 수업실연, 심층면접 순으로 진행되고, 최종 합격자는 2월 초에 발표해요.</p>'
     '<p>원서접수는 보통 10월 중순(중등)과 그 전후로 진행돼요. 한 번에 한 개 시·도에만 지원할 수 있으니(장애 구분모집 일부 예외), 지역 선택이 특히 중요해요.</p>'),
  ],
  faq=[('임용 1차 합격선은 어디서 보나요?', '온라인 교직원 채용시스템(edurecruit.go.kr)과 각 시·도교육청 누리집 고시/공고에서 지역별·과목별로 공개돼요. 합격자가 3명 이상인 과목만 공개하고, 1명 선발 과목은 개인정보 보호로 비공개예요.'),
       ('2027학년도 중등은 몇 명 뽑나요?', '전국 공립 중등 교과 4,932명으로 확정됐어요. 2026학년도(7,147명)보다 2,215명 줄었고, 서울·경기 등 수도권 감소가 컸어요.'),
       ('임용 경쟁률은 어떻게 계산되나요?', '1차 필기에서 모집 인원의 1.5배수를 뽑고 동점자는 전원 합격시켜요. 평균 경쟁률은 지역·과목별로 공개되며, 소수 모집 과목일수록 경쟁률이 크게 올라가요.'),
       ('초등 임용은 과목이 나뉘나요?', '초등은 과목 구분 없이 지역(시·도)별로 선발해요. 중등은 국어·수학·영어 등 표시과목(전공)별로 지역마다 따로 뽑아요.'),
       ('임용 1차 시험 과목은 무엇인가요?', '1교시 교육학(20점), 2·3교시 전공 A·B(각 40점)예요. 2027학년도부터 한국사 과목은 한국사능력검정시험으로 대체돼요.')],
  src='<li><a href="https://www.moe.go.kr" rel="noopener" target="_blank">교육부</a> — 2026·2027학년도 공립 교원 임용 선발 규모 집계 발표 (2026-11-27 확인)</li>'
      '<li><a href="https://www.edurecruit.go.kr" rel="noopener" target="_blank">온라인 교직원 채용시스템</a> — 지역별·과목별 1차 합격선·성적 공개</li>'
      '<li>연합뉴스·뉴시스·머니투데이 등 — 2025~2027학년도 시도별 선발인원 보도 (교육부·시도교육청 발표 인용, 2026-11-27 확인)</li>'
      '<li><a href="https://www.goe.go.kr" rel="noopener" target="_blank">경기도교육청</a>·서울시교육청 — 2026학년도 중등 임용 제1차 합격자 공고(과목별 합격선 붙임) (2026-11-27 확인)</li>')

if __name__ == '__main__':
    print('wrote', G.page(P))
