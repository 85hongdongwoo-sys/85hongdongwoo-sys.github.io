#!/usr/bin/env python3
"""한국사능력검정시험 기출·급수 페이지 (/ipsi/hanneung.html) — 국사편찬위원회 공식 자료(2026-11-24 확인) 기준.
로컬에서 돌리고 overlay 결과를 커밋해요: python3 build/newpages/gen_hanneung.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

# 시험 자료실 목록 (회차, 종류, 자료 올린 날) — historyexam.go.kr 시험 자료실, 2026-11-24 확인
ROUNDS = [(80,'심화','2026-10-17'),(79,'심화','2026-08-09'),(79,'기본','2026-08-09'),(78,'심화','2026-05-23'),(77,'심화','2026-02-07'),(77,'기본','2026-02-07'),
 (76,'심화','2025-10-18'),(75,'기본','2025-08-09'),(75,'심화','2025-08-09'),(74,'심화','2025-05-24'),(73,'심화','2025-02-16'),(73,'기본','2025-02-16'),
 (72,'심화','2024-10-20'),(71,'심화','2024-08-10'),(71,'기본','2024-08-10'),(70,'심화','2024-05-25'),(69,'기본','2024-02-17'),(69,'심화','2024-02-17'),
 (68,'심화','2023-12-02'),(67,'기본','2023-10-21'),(67,'심화','2023-10-21'),(66,'심화','2023-08-13'),(66,'기본','2023-08-13'),(65,'심화','2023-06-17'),
 (64,'심화','2023-04-15'),(64,'기본','2023-04-15'),(63,'심화','2023-02-21'),(63,'기본','2023-02-11'),(62,'심화','2022-12-03'),(61,'기본','2022-10-22'),
 (61,'심화','2022-10-22'),(60,'기본','2022-08-06'),(60,'심화','2022-08-06'),(59,'심화','2022-06-11'),(58,'기본','2022-04-10'),(58,'심화','2022-04-10'),
 (57,'기본','2022-02-12'),(57,'심화','2022-02-12')]
EXAMS = [('81','2026-11-28','심화'),('82','2027-02-13','심화'),('83','2027-05-23','기본·심화'),('84','2027-08-07','기본·심화'),('85','2027-10-16','심화'),('86','2027-11-27','심화')]
DAT = 'https://www.historyexam.go.kr/pst/list.do?bbs=dat'

by = {}
for r, k, d in ROUNDS:
    by.setdefault(r, {})[k] = d
rows = ''.join(f'<tr><td>제{r}회</td><td>{"○" if "심화" in v else "—"}</td><td>{"○" if "기본" in v else "—"}</td><td>{min(v.values())}</td></tr>' for r, v in sorted(by.items(), reverse=True))
ex_js = ','.join(f"['{n}','{d}','{k}']" for n, d, k in EXAMS)

TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:26px 0 10px}#tool h2:first-of-type{margin-top:0}</style>
<h2 style="margin-top:0">다음 시험까지</h2><div class="tiles hk-tiles" id="next"></div>
<h2>내 점수로 급수 알아보기</h2>
<div class="grid g2"><div class="f"><label for="kd">시험 종류</label><select id="kd"><option value="s" selected>심화 (1·2·3급)</option><option value="b">기본 (4·5·6급)</option></select></div>
<div class="f"><label for="sc">점수 (100점 만점)</label><input id="sc" type="number" inputmode="numeric" min="0" max="100" placeholder="예: 74"></div></div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">받는 급수</div><div class="v" id="gr">—</div></div><div class="tile light"><div class="k">다음 급수까지</div><div class="v" id="gap">—</div></div></div>
<h2>회차별 기출문제 (공식 시험 자료실)</h2>
<p class="note">문제지와 정답표 PDF는 국사편찬위원회 시험 자료실에서 받아요. 아래는 자료실에 올라와 있는 회차예요 (2026년 11월 24일 확인).</p>
<div class="hk-tbl"><table class="tbl"><thead><tr><th>회차</th><th>심화</th><th>기본</th><th>자료 올린 날</th></tr></thead><tbody>"""+rows+"""</tbody></table></div>
<div class="btns"><a class="btn dl" href="/ipsi/hanneung-gichul.html">▶ 기출 풀고 바로 채점 (44~81회)</a><a class="btn" href=\""""+DAT+"""\" target="_blank" rel="noopener">공식 자료실</a><a class="btn" href="https://www.historyexam.go.kr/answer/list.do" target="_blank" rel="noopener">공식 정답</a></div>
</section>""", """<script>
(function(){var $=HL.$;var EX=["""+ex_js+"""];
var t=new Date();t.setHours(0,0,0,0);var nx=EX.filter(function(e){return new Date(e[1]+'T00:00:00')>=t}).slice(0,2);var W='일월화수목금토';
$('#next').innerHTML=nx.map(function(e,i){var d=new Date(e[1]+'T00:00:00');var dd=Math.round((d-t)/864e5);return '<div class="tile'+(i?' light':'')+'"><div class="k">제'+e[0]+'회 · '+e[2]+'</div><div class="v">'+(dd?'D-'+dd:'오늘')+'</div><div class="k">'+(d.getMonth()+1)+'월 '+d.getDate()+'일('+W[d.getDay()]+')</div></div>'}).join('')||'<p class="note">다음 일정이 나오면 바로 넣을게요.</p>';
function g(){var s=$('#sc').value,k=$('#kd').value;if(s===''){$('#gr').textContent=$('#gap').textContent='—';return}s=Math.max(0,Math.min(100,+s));var L=k==='s'?['1급','2급','3급']:['4급','5급','6급'];var r=s>=80?L[0]:s>=70?L[1]:s>=60?L[2]:'불합격';$('#gr').textContent=r;
 $('#gap').textContent=s>=80?'최고 급수':(s>=70?80:s>=60?70:60)-s+'점 더'}
$('#sc').addEventListener('input',g);$('#kd').addEventListener('change',g);
})();
</script>""")

P = dict(slug='hanneung', url='/ipsi/hanneung.html', sec=('입시·시험', '/ipsi/'), crumb3=' › 한국사능력검정',
  name='한국사능력검정시험 기출문제·급수 기준 (57~80회 회차별, 2027 시험 일정)',
  h1='한국사능력검정 <b>기출·급수</b>', lead='한능검 회차별 기출문제 받는 곳, 점수별 급수(1~6급), 2027년 시험 일정을 한 곳에 모았어요. 점수를 넣으면 몇 급인지 바로 알려 줘요.',
  desc='한국사능력검정시험(한능검) 57회~80회 기출문제·정답표를 받는 공식 자료실 안내, 심화(1·2·3급)·기본(4·5·6급) 점수 기준, 2027년 82~86회 시험 일정과 원서접수 기간을 정리했어요. 점수를 넣으면 급수와 다음 급수까지 남은 점수를 보여 줘요.',
  tool=TOOL, warn='', nosafe=True,
  body=[
    ('한능검 급수 기준 (몇 점이면 몇 급)', '<p>한능검은 등수로 자르는 시험이 아니라 <b>점수로 급수를 주는 인증 시험</b>이에요. 그래서 회차마다 바뀌는 ‘등급컷’이 없고, 아래 점수 기준이 항상 같아요.</p>'
      '<table class="tbl"><thead><tr><th></th><th>심화</th><th>기본</th></tr></thead><tbody><tr><td>80점 이상</td><td>1급</td><td>4급</td></tr><tr><td>70~79점</td><td>2급</td><td>5급</td></tr><tr><td>60~69점</td><td>3급</td><td>6급</td></tr><tr><td>문항</td><td>50문항 (5지 선다)</td><td>50문항 (4지 선다)</td></tr><tr><td>배점</td><td colspan="2">100점 만점, 문항마다 1~3점</td></tr><tr><td>시험 시간</td><td>80분 (10:30~11:50)</td><td>70분 (10:30~11:40)</td></tr><tr><td>응시료</td><td>27,000원</td><td>22,000원</td></tr></tbody></table>'
      '<p>예를 들어 심화에서 74점이면 2급이고, 1급까지 6점이 모자라요. 공무원·교원임용·공기업 등에서 요구하는 급수가 다르니 지원하는 곳의 공고를 꼭 확인하세요.</p>'),
    ('2027년 한국사능력검정시험 일정', '<table class="tbl"><thead><tr><th>회차</th><th>시험일</th><th>종류</th><th>원서접수 (정기)</th></tr></thead><tbody>'
      '<tr><td>제82회</td><td>2월 13일(토)</td><td>심화</td><td>1월 12일(화) 10시 ~ 1월 19일(화) 17시</td></tr>'
      '<tr><td>제83회</td><td>5월 23일(일)</td><td>기본·심화</td><td>4월 20일(화) 10시 ~ 4월 27일(화) 17시</td></tr>'
      '<tr><td>제84회</td><td>8월 7일(토)</td><td>기본·심화</td><td>7월 6일(화) 10시 ~ 7월 13일(화) 17시</td></tr>'
      '<tr><td>제85회</td><td>10월 16일(토)</td><td>심화</td><td>9월 6일 10시 ~ 9월 13일 17시 (공지 표기)</td></tr>'
      '<tr><td>제86회</td><td>11월 27일(토)</td><td>심화</td><td>11월 2일(화) 10시 ~ 11월 9일(화) 17시</td></tr></tbody></table>'
      '<p>제83회는 토요일에 일하는 사람을 위해 <b>일요일</b>에 봐요. <b>기본 시험은 5월(83회)과 8월(84회) 두 번뿐</b>이에요. 원서접수 첫날은 지역별로 나눠 받는 경우가 있으니 공지를 확인하세요. 85회 접수 날짜는 공지에 9월 6일(화)로 적혀 있지만 2027년 9월 6일은 월요일이라, 접수 전에 공식 공지를 다시 확인하세요.</p>'
      '<p>바로 앞 시험인 <b>제81회는 2026년 11월 28일(토), 심화만</b> 치러요.</p>'),
    ('한능검 기출문제 받는 법', '<ol><li>국사편찬위원회 한국사능력검정시험 홈페이지에서 [문제 관리] → [시험 자료실]로 가요. 위 ‘공식 시험 자료실 열기’ 버튼이 바로 그 화면이에요.</li><li>회차와 심화·기본을 골라 <b>시험지 파일</b>(문제지)과 <b>답안지 파일</b>(정답표)을 받아요. 로그인 없이 받을 수 있어요.</li><li>정답만 빨리 보려면 [문제 관리] → [정답 보기]를 써요.</li></ol>'
      '<p>사람이 몰리면 대기 화면(접속 대기)이 뜰 수 있어요. 문항에 쓰인 사진 등의 저작권은 원저작자에게 있어서, 홍라이프는 파일을 따로 올리지 않고 공식 자료실로 안내해요.</p>'),
    ('기출을 어떻게 풀면 좋을까요', '<ul><li>최근 5회차 정도를 실제 시간(심화 80분, 기본 70분)에 맞춰 풀고, 위 칸에 점수를 넣어 급수를 확인해요.</li><li>틀린 문제는 시대(선사·고대·고려·조선·근현대)별로 모아 다시 봐요.</li><li>심화와 기본은 문항 수는 같지만 보기 수(5지·4지)와 난도가 달라요. 필요한 급수에 맞는 종류를 풀어요.</li></ul>'),
    ('성적과 인증서 확인', '<p>성적은 한국사능력검정시험 홈페이지의 [나의 시험 정보] → [나의 응시 결과]에서 보고, 인증서는 홈페이지나 정부24에서 출력해요. 따로 성적통지서나 인증 카드를 보내 주지 않아요.</p>'),
  ],
  faq=[('한능검 등급컷이 회차마다 다른가요?', '아니요. 점수 기준이 정해져 있어요. 심화는 80점 이상 1급, 70~79점 2급, 60~69점 3급이고, 기본은 같은 점수로 4·5·6급이에요.'),
       ('한능검 기출문제는 몇 회차까지 받을 수 있나요?', '2026년 11월 24일 기준 공식 시험 자료실에 제57회(2022년 2월)부터 제80회(2026년 10월)까지 올라와 있어요.'),
       ('2027년 기본 시험은 언제 있나요?', '제83회(5월 23일, 일요일)와 제84회(8월 7일, 토요일) 두 번이에요. 나머지 회차는 심화만 치러요.'),
       ('한능검 응시료는 얼마인가요?', '심화 27,000원, 기본 22,000원이에요.'),
       ('시험 볼 때 필기구를 가져가야 하나요?', '아니요. 개인 필기구는 가져갈 수 없고, 컴퓨터용 사인펜과 수정테이프는 시험장에서 줘요. 수험표와 신분증만 챙기세요.')],
  rel='<section class="card rel"><h2>함께 보면 좋은 시험 정보</h2><ul><li><a href="/calendar/exam-schedule.html"><b>2026·2027 자격증 시험일정 달력</b><span>국가기술·국가전문·한국사·토익 일정 한눈에</span></a></li><li><a href="/ipsi/gongmuwon/"><b>공무원 기출문제</b><span>9급·7급·지방직 연도별 기출</span></a></li><li><a href="/ipsi/gumjung/"><b>검정고시 기출문제</b><span>초졸·중졸·고졸 회차별</span></a></li><li><a href="/ipsi/jagyeok/"><b>자격증 기출문제</b><span>공인중개사·사회복지사 등 국가전문자격</span></a></li></ul></section>',
  src='<li><a href="https://www.historyexam.go.kr" rel="noopener" target="_blank">국사편찬위원회 한국사능력검정시험</a> — 시험 요강·응시 안내·시험 자료실·2027년 시행 일정 공지 (2026-11-24 확인)</li>')

if __name__ == '__main__':
    print('wrote', G.page(P))
