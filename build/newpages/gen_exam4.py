#!/usr/bin/env python3
"""입시·시험 4종 페이지 생성 (공무원 9급·검정고시·JLPT·토익 Part5).
공식 공개 기출/샘플 안내 + 오리지널 연습 도구. 로컬에서 실행해 overlay 결과를 커밋해요:
    python3 build/newpages/gen_exam4.py
확인일: 2026-11-27 (국사편찬위·사이버국가고시센터·시도교육청·jlpt.jp)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

REL = ('<section class="card rel"><h2>함께 보면 좋은 시험 정보</h2><ul>'
 '<li><a href="/ipsi/hanneung.html"><b>한국사능력검정 기출·급수</b><span>57~80회 기출 받는 곳, 점수별 1~6급</span></a></li>'
 '<li><a href="/ipsi/gong9.html"><b>공무원 9급 기출문제</b><span>사이버국가고시센터 공식 PDF 받는 법</span></a></li>'
 '<li><a href="/ipsi/gumjeong.html"><b>검정고시 기출·합격 계산</b><span>초·중·고졸 기출, 평균 60점 합격 판정</span></a></li>'
 '<li><a href="/ipsi/jlpt.html"><b>JLPT 공식 샘플·합격 판정</b><span>N1~N5 샘플문제, 합격점 계산</span></a></li>'
 '<li><a href="/ipsi/toeic-part5.html"><b>토익 Part5 연습 10문항</b><span>문법·어휘 실전 연습, 해설·채점</span></a></li>'
 '<li><a href="/calendar/exam-schedule.html"><b>자격증 시험일정 달력</b><span>원서접수·시험일·합격발표 한눈에</span></a></li>'
 '</ul></section>')

def rel_for(url):
    # 자기 자신 링크는 뺌
    import re
    return re.sub(r'<li><a href="' + re.escape(url) + r'">.*?</a></li>', '', REL, count=1)

PAGES = []

# ─────────────────────────────────────────────────────────────────────────
# 1) 공무원 9급 기출 (/ipsi/gong9.html)
# ─────────────────────────────────────────────────────────────────────────
MAJORS = [
 ('일반행정', '행정법총론', '행정학개론'),
 ('세무', '세법개론', '회계학'),
 ('교육행정', '행정법총론', '교육학개론'),
 ('사회복지', '사회복지학개론', '행정법총론'),
 ('검찰', '형법', '형사소송법'),
]
maj_js = ','.join(f"['{n}','{a}','{b}']" for n, a, b in MAJORS)
GONG_TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:24px 0 10px}#tool h2:first-of-type{margin-top:0}</style>
<h2 style="margin-top:0">기출문제 바로 받기 (공식)</h2>
<p class="note">국가직은 사이버국가고시센터, 지방직은 지방자치단체 인터넷원서접수센터에서 문제지·정답을 무료로 받아요(로그인 없이). 아래 버튼이 그 화면이에요.</p>
<div class="btns"><a class="btn dl" href="https://www.gosi.kr/tcs/dsb/wc/selectQestInfoPblancList.do" target="_blank" rel="noopener">국가직 기출 (사이버국가고시센터)</a><a class="btn" href="https://local.gosi.go.kr" target="_blank" rel="noopener">지방직 원서접수센터</a><a class="btn" href="https://www.mpm.go.kr" target="_blank" rel="noopener">인사혁신처(시험 제도)</a></div>
<h2>내 직렬 전문과목 보기</h2>
<div class="grid g2"><div class="f"><label for="mj">직렬 고르기</label><select id="mj"><option value="0" selected>일반행정</option><option value="1">세무</option><option value="2">교육행정</option><option value="3">사회복지</option><option value="4">검찰</option></select></div>
<div class="f"><label>공통 3과목</label><div class="tile light" style="margin:0"><div class="v" style="font-size:17px">국어 · 영어 · 한국사</div></div></div></div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">전문과목 ①</div><div class="v" id="m1">행정법총론</div></div><div class="tile"><div class="k">전문과목 ②</div><div class="v" id="m2">행정학개론</div></div></div>
<p class="note">9급 공채는 <b>국어·영어·한국사 + 직렬별 전문 2과목 = 5과목 100문항</b>이에요. 전문과목은 직렬마다 다르니, 위에 없는 직렬은 공식 공고에서 꼭 확인하세요.</p>
</section>""", """<script>
(function(){var $=HL.$;var M=["""+maj_js+"""];
function g(){var m=M[+$('#mj').value]||M[0];$('#m1').textContent=m[1];$('#m2').textContent=m[2];}
$('#mj').addEventListener('change',g);g();
})();
</script>""")
PAGES.append(dict(slug='gong9', url='/ipsi/gong9.html', sec=('입시·시험', '/ipsi/'), crumb3=' › 공무원 9급 기출', nosafe=True, warn='',
  name='공무원 9급 기출문제 PDF 받는 법 (국가직·지방직 과목·직렬별 전문과목)',
  h1='공무원 9급 <b>기출문제</b>', lead='국가직·지방직 9급 기출문제를 공식 사이트에서 무료로 받는 법, 과목 구성, 직렬별 전문과목을 한 곳에 모았어요.',
  desc='공무원 9급 기출문제(문제지·정답)를 사이버국가고시센터와 지방자치단체 원서접수센터에서 무료로 받는 법, 국어·영어·한국사 공통 3과목과 직렬별 전문 2과목 구성, 주요 직렬 전문과목을 정리했어요.',
  tool=GONG_TOOL, rel=rel_for('/ipsi/gong9.html'),
  body=[
    ('9급 공무원 기출문제, 어디서 받나요', '<p>국가직 9급(국가공무원) 기출은 <b>사이버국가고시센터(gosi.kr)</b>의 [시험문제/정답] 메뉴에서 연도별로 받을 수 있어요. 회원가입이나 로그인 없이 문제지와 정답표 PDF를 바로 내려받을 수 있어요.</p>'
     '<ul><li><b>국가직 9급·7급·5급</b> → 사이버국가고시센터(gosi.kr)</li><li><b>지방직 9급·7급</b> → 지방자치단체 인터넷원서접수센터(local.gosi.go.kr)</li><li><b>시험 제도·공지</b> → 인사혁신처(mpm.go.kr)</li></ul>'
     '<p>국어·영어·한국사는 모든 직렬이 함께 보는 공통과목이라, 직렬이 달라도 연도별로 빠짐없이 모아 두면 좋아요. 공식 문제에는 해설이 없으니, 해설은 학원·수험 커뮤니티 자료로 따로 보완하세요.</p>'),
    ('9급 시험 과목과 문항 구성', '<p>2022년부터 9급 공채는 선택과목 없이 <b>직렬별 전문과목이 정해져</b> 있어요. 공통 3과목에 전문 2과목을 더해 모두 5과목이에요.</p>'
     '<table class="tbl"><thead><tr><th>구분</th><th>과목</th></tr></thead><tbody>'
     '<tr><td>공통 (3과목)</td><td>국어, 영어, 한국사</td></tr>'
     '<tr><td>전문 (2과목)</td><td>직렬마다 다름 (위 도구에서 확인)</td></tr>'
     '<tr><td>문항·시간</td><td>과목당 20문항, 총 100문항 / 100분</td></tr>'
     '<tr><td>배점</td><td>과목당 100점 만점, 4지 선다</td></tr></tbody></table>'
     '<p>필기 합격선은 과목별 40점 이상(과락 면제 기준)을 넘고, 선발 인원과 경쟁률에 따라 총점 순으로 정해져요. 과목별로 40점에 못 미치면 과락이라 다른 과목 점수가 높아도 불합격이에요.</p>'),
    ('2025년부터 바뀐 국어·영어 출제 방향', '<p>2025년부터 국가·지방직 9급의 국어와 영어가 <b>암기보다 현장 직무 중심</b>으로 바뀌었어요. 국어는 사자성어·한자어 단순 암기 비중이 줄고 독해·추론이 늘었고, 영어도 실무 지문(이메일·안내문 등) 이해를 더 묻는 방향이에요.</p>'
     '<p>그래서 오래된 기출로는 기본 유형을, 최근 기출로는 바뀐 경향을 익히는 식으로 나눠서 푸는 게 좋아요. 제도는 해마다 바뀔 수 있으니 응시 전 공식 공고를 꼭 확인하세요.</p>'),
    ('기출문제 효율적으로 푸는 법', '<ul><li>최근 5년 치를 실제 시험 시간(100분)에 맞춰 통째로 풀어 실전 감각을 길러요.</li><li>국어·영어·한국사는 국가직·지방직을 모두 모으면 문제 양이 두 배가 돼요.</li><li>같은 개념에서 반복 출제되는 문제가 많아서, 틀린 문제를 과목별 오답노트로 모아 다시 보는 게 점수를 가장 빨리 올려요.</li></ul>'),
  ],
  faq=[('9급 공무원 기출문제는 어디서 무료로 받나요?', '국가직은 사이버국가고시센터(gosi.kr)의 [시험문제/정답] 메뉴에서, 지방직은 지방자치단체 인터넷원서접수센터(local.gosi.go.kr)에서 로그인 없이 받을 수 있어요.'),
       ('9급 시험은 몇 과목인가요?', '국어·영어·한국사 공통 3과목에 직렬별 전문 2과목을 더해 모두 5과목, 100문항을 100분 동안 풀어요.'),
       ('공식 기출에 해설도 있나요?', '아니요. 공식 문제지와 정답표에는 해설이 없어요. 해설은 학원 자료나 수험 커뮤니티에서 따로 구해야 해요.'),
       ('기출문제 PDF에 회원가입이 필요한가요?', '아니요. 사이버국가고시센터는 회원가입 없이 연도별 문제지와 정답을 바로 내려받을 수 있어요.')],
  src='<li><a href="https://www.gosi.kr" rel="noopener" target="_blank">사이버국가고시센터</a> — 국가직 9급·7급·5급 기출문제·정답 (2026-11-27 확인)</li>'
      '<li><a href="https://www.mpm.go.kr" rel="noopener" target="_blank">인사혁신처</a> — 시험 제도·출제 기조 전환 안내 (2026-11-27 확인)</li>'))

# ─────────────────────────────────────────────────────────────────────────
# 2) 검정고시 (/ipsi/gumjeong.html)
# ─────────────────────────────────────────────────────────────────────────
GUM_TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:24px 0 10px}#tool h2:first-of-type{margin-top:0}#tool .gm-row{display:grid;grid-template-columns:1fr 90px;gap:8px;align-items:center;margin:6px 0}#tool .gm-row label{margin:0}#tool .gm-row input{text-align:center}</style>
<h2 style="margin-top:0">기출문제 바로 받기 (공식)</h2>
<p class="note">검정고시 기출문제는 각 시·도 교육청 누리집의 검정고시 안내 게시판에서 무료로 받아요. 전국 공통 문제라 어느 교육청 자료든 같아요.</p>
<div class="btns"><a class="btn dl" href="https://www.goe.go.kr/home/ensealgo/gmgosi/index.do" target="_blank" rel="noopener">경기도교육청 검정고시</a><a class="btn" href="https://buseo.sen.go.kr/web/services/page/viewPage.action?page=kor/qualification/qualification_01.html" target="_blank" rel="noopener">서울시교육청 검정고시</a></div>
<h2>고졸 검정고시 합격 계산기</h2>
<p class="note">과목별 점수(100점 만점)를 넣으면 평균과 합격 여부를 알려 줘요. 응시한 과목만 넣으세요. 합격 기준은 평균 60점 이상이에요.</p>
<div id="gmrows"></div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">평균 점수</div><div class="v" id="gmavg">—</div></div><div class="tile light"><div class="k">합격 여부</div><div class="v" id="gmres">—</div></div></div>
<p class="note">과목 60점 이상이면 그 과목은 ‘과목 합격’으로 다음 회차에 면제돼요. 전 과목 평균 60점 이상이면 최종 합격이에요(일부 교육청은 과락 없이 평균만 봐요).</p>
</section>""", """<script>
(function(){var $=HL.$;var S=['국어','수학','영어','사회','과학','한국사','선택'];
$('#gmrows').innerHTML=S.map(function(n,i){return '<div class="gm-row"><label for="gm'+i+'">'+n+'</label><input id="gm'+i+'" type="number" inputmode="numeric" min="0" max="100" placeholder="점수"></div>'}).join('');
function g(){var sum=0,cnt=0;for(var i=0;i<S.length;i++){var v=$('#gm'+i).value;if(v!==''){v=Math.max(0,Math.min(100,+v));sum+=v;cnt++;}}
 if(!cnt){$('#gmavg').textContent=$('#gmres').textContent='—';return;}
 var avg=Math.round(sum/cnt*10)/10;$('#gmavg').textContent=avg+'점';
 $('#gmres').textContent=avg>=60?'합격 (평균 60점 이상)':'불합격 (평균 '+(60-avg).toFixed(1)+'점 부족)';}
for(var i=0;i<S.length;i++)$('#gm'+i).addEventListener('input',g);
})();
</script>""")
PAGES.append(dict(slug='gumjeong', url='/ipsi/gumjeong.html', sec=('입시·시험', '/ipsi/'), crumb3=' › 검정고시', nosafe=True, warn='',
  name='검정고시 기출문제·합격 계산 (고졸·중졸·초졸 과목·일정)',
  h1='검정고시 <b>기출·합격 계산</b>', lead='고졸·중졸·초졸 검정고시 기출문제 받는 곳, 과목 구성, 평균 60점 합격 판정을 한 곳에 모았어요. 과목 점수를 넣으면 합격 여부를 바로 알려 줘요.',
  desc='검정고시(고졸·중졸·초졸) 기출문제를 시·도 교육청에서 무료로 받는 법, 시험 과목과 연 2회 일정, 과목 60점·평균 60점 합격 기준을 정리했어요. 과목별 점수를 넣으면 평균과 합격 여부를 계산해 줘요.',
  tool=GUM_TOOL, rel=rel_for('/ipsi/gumjeong.html'),
  body=[
    ('검정고시 기출문제 받는 곳', '<p>검정고시는 각 <b>시·도 교육청</b>이 시행하고, 기출문제(문제지·정답)도 교육청 누리집의 검정고시 안내 게시판에 공개해요. 문제는 전국 공통이라 어느 교육청 자료든 내용이 같아요.</p>'
     '<ul><li>경기도교육청, 서울시교육청 등 각 시·도 교육청 검정고시 페이지에서 회차별로 받아요.</li><li>최근 몇 년 치가 PDF로 올라와 있고, 로그인 없이 받을 수 있어요.</li><li>교재로는 ‘기출 3~5년’ 묶음도 있지만, 공식 문제만으로도 무료로 충분히 풀 수 있어요.</li></ul>'),
    ('검정고시 과목 (고졸·중졸·초졸)', '<table class="tbl"><thead><tr><th>구분</th><th>필수</th><th>선택</th></tr></thead><tbody>'
     '<tr><td>고졸</td><td>국어·수학·영어·사회·과학·한국사 (6)</td><td>도덕·기술가정·체육·음악·미술 중 1</td></tr>'
     '<tr><td>중졸</td><td>국어·수학·영어·사회·과학 (5)</td><td>도덕·기술가정·체육·음악·미술·정보 중 1</td></tr>'
     '<tr><td>초졸</td><td>국어·수학·사회·과학 (4)</td><td>도덕·체육·음악·미술·실과·영어 중 1</td></tr></tbody></table>'
     '<p>중졸 사회 과목에는 역사(한국사)가 포함돼요. 모든 급에서 과목당 100점 만점, 보통 25문항 안팎이에요.</p>'),
    ('합격 기준 — 과목 60점, 평균 60점', '<p>검정고시는 <b>전 과목 평균 60점 이상</b>이면 합격이에요. 그리고 어떤 과목에서 <b>60점 이상</b>을 받으면 그 과목은 ‘과목 합격’으로 처리돼, 다음 회차에 다시 안 봐도 돼요(한 번에 다 못 붙어도 나눠서 합격 가능).</p>'
     '<p>위 계산기에 응시한 과목 점수를 넣으면 평균과 합격 여부를 바로 보여 줘요. 다만 세부 합격 사정(과락 적용 여부 등)은 시행하는 교육청 공고가 기준이에요.</p>'),
    ('검정고시 일정 — 연 2회', '<p>검정고시는 보통 <b>1년에 두 번</b> 치러요. 제1회는 4월, 제2회는 8월쯤이고, 초·중·고졸 일정이 같은 날로 진행돼요. 원서 접수는 시험 약 한 달 전에 거주지 시·도 교육청에서 받아요.</p>'
     '<p>합격률은 해마다 80% 후반으로 높은 편이에요. 내신 대신 수능 정시로 대입을 준비하려는 학생이 늘면서 고졸 검정고시 응시자도 꾸준히 늘고 있어요.</p>'),
  ],
  faq=[('검정고시 기출문제는 어디서 받나요?', '각 시·도 교육청(경기도교육청·서울시교육청 등) 누리집의 검정고시 안내 게시판에서 회차별 문제지와 정답을 무료로 받을 수 있어요. 문제는 전국 공통이에요.'),
       ('검정고시는 몇 점이면 합격인가요?', '전 과목 평균 60점 이상이면 합격이에요. 과목별로 60점 이상이면 그 과목은 다음 회차에 면제돼요.'),
       ('검정고시는 1년에 몇 번 있나요?', '보통 연 2회로, 1회는 4월·2회는 8월쯤이에요. 초·중·고졸 일정이 같은 날로 진행돼요.'),
       ('고졸 검정고시 과목은 몇 개인가요?', '국어·수학·영어·사회·과학·한국사 6개 필수에 선택 1과목을 더해 모두 7과목이에요.')],
  src='<li><a href="https://www.goe.go.kr" rel="noopener" target="_blank">경기도교육청</a> — 검정고시 시행 공고·기출문제 (2026-11-27 확인)</li>'
      '<li><a href="https://buseo.sen.go.kr" rel="noopener" target="_blank">서울특별시교육청</a> — 검정고시 안내·기출문제 (2026-11-27 확인)</li>'))

# ─────────────────────────────────────────────────────────────────────────
# 3) JLPT (/ipsi/jlpt.html)
# ─────────────────────────────────────────────────────────────────────────
# 레벨: [종합합격점, 만점, [ (영역명, 기준점, 만점) ... ]]
JLPT = {
 'N1': [100, 180, [['언어지식(문자·어휘·문법)', 19, 60], ['독해', 19, 60], ['청해', 19, 60]]],
 'N2': [90, 180, [['언어지식(문자·어휘·문법)', 19, 60], ['독해', 19, 60], ['청해', 19, 60]]],
 'N3': [95, 180, [['언어지식(문자·어휘·문법)', 19, 60], ['독해', 19, 60], ['청해', 19, 60]]],
 'N4': [90, 180, [['언어지식·독해', 38, 120], ['청해', 19, 60]]],
 'N5': [80, 180, [['언어지식·독해', 38, 120], ['청해', 19, 60]]],
}
import json as _json
jlpt_js = _json.dumps(JLPT, ensure_ascii=False)
JLPT_TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:24px 0 10px}#tool h2:first-of-type{margin-top:0}#tool .jp-row{display:grid;grid-template-columns:1fr 92px;gap:8px;align-items:center;margin:6px 0}#tool .jp-row label{margin:0;font-size:15px}#tool .jp-row input{text-align:center}</style>
<h2 style="margin-top:0">공식 샘플문제 받기 (무료)</h2>
<p class="note">JLPT는 지난 시험지를 공개하지 않지만, 공식 사이트에서 레벨별 샘플문제(유형 예시)를 무료로 제공해요. 아래가 공식 페이지예요.</p>
<div class="btns"><a class="btn dl" href="https://www.jlpt.jp/e/samples/forlearners.html" target="_blank" rel="noopener">레벨별 샘플문제 (N1~N5)</a><a class="btn" href="https://www.jlpt.jp/e/samples/sampleindex.html" target="_blank" rel="noopener">공식 문제집 안내</a></div>
<h2>JLPT 합격 판정기</h2>
<div class="grid g2"><div class="f"><label for="jl">레벨</label><select id="jl"><option>N1</option><option>N2</option><option>N3</option><option>N4</option><option>N5</option></select></div><div class="f"><label>종합 합격점</label><div class="tile light" style="margin:0"><div class="v" id="jpass" style="font-size:17px">100 / 180</div></div></div></div>
<div id="jprows"></div>
<div class="tiles hk-tiles"><div class="tile"><div class="k">내 총점</div><div class="v" id="jtot">—</div></div><div class="tile light"><div class="k">합격 여부</div><div class="v" id="jres">—</div></div></div>
<p class="note">합격하려면 ① 종합 점수가 합격점 이상이면서 ② 모든 영역이 각 기준점(보통 19점, N4·N5 언어지식·독해는 38점) 이상이어야 해요. 한 영역이라도 기준점 미만이면 불합격이에요.</p>
</section>""", """<script>
(function(){var $=HL.$;var J="""+jlpt_js+""";
function draw(){var lv=$('#jl').value,d=J[lv];$('#jpass').textContent=d[0]+' / '+d[1];
 $('#jprows').innerHTML=d[2].map(function(s,i){return '<div class="jp-row"><label for="jp'+i+'">'+s[0]+' <span style="color:#8A94A6">(기준 '+s[1]+'·만점 '+s[2]+')</span></label><input id="jp'+i+'" type="number" inputmode="numeric" min="0" max="'+s[2]+'" placeholder="점수"></div>'}).join('');
 for(var i=0;i<d[2].length;i++)$('#jp'+i).addEventListener('input',calc);calc();}
function calc(){var lv=$('#jl').value,d=J[lv],tot=0,any=false,okSec=true;
 for(var i=0;i<d[2].length;i++){var v=$('#jp'+i).value;if(v===''){okSec=false;continue;}any=true;v=Math.max(0,Math.min(d[2][i][2],+v));tot+=v;if(v<d[2][i][1])okSec='low';}
 if(!any){$('#jtot').textContent=$('#jres').textContent='—';return;}
 $('#jtot').textContent=tot+' / '+d[1];
 if(okSec===false){$('#jres').textContent='영역 점수를 모두 넣어 주세요';return;}
 var pass=(tot>=d[0])&&(okSec===true);
 $('#jres').textContent=pass?'합격':'불합격'+(okSec==='low'?' (기준점 미달 영역 있음)':' (종합 점수 부족)');}
$('#jl').addEventListener('change',draw);draw();
})();
</script>""")
PAGES.append(dict(slug='jlpt', url='/ipsi/jlpt.html', sec=('입시·시험', '/ipsi/'), crumb3=' › JLPT', nosafe=True, warn='',
  name='JLPT 공식 샘플문제·합격 판정 (N1~N5 합격점·기준점)',
  h1='JLPT <b>샘플·합격 판정</b>', lead='일본어능력시험(JLPT) 공식 샘플문제 받는 곳, 레벨별 합격점과 영역 기준점을 한 곳에 모았어요. 영역 점수를 넣으면 합격 여부를 바로 알려 줘요.',
  desc='JLPT(일본어능력시험) 공식 샘플문제를 jlpt.jp에서 무료로 받는 법, N1~N5 종합 합격점(180점 만점)과 영역별 기준점을 정리했어요. 영역 점수를 넣으면 합격 여부를 계산해 줘요.',
  tool=JLPT_TOOL, rel=rel_for('/ipsi/jlpt.html'),
  body=[
    ('JLPT 공식 문제, 어디서 받나요', '<p>JLPT는 토익처럼 실제 시험지를 공개하지 않아요. 대신 공식 사이트(jlpt.jp)에서 <b>레벨별 샘플문제</b>를 무료로 제공해, 문제 유형과 형식을 미리 볼 수 있어요.</p>'
     '<ul><li>‘Let’s Try Sample Questions!’ — N1~N5 레벨별로 유형마다 예시 문제 1개씩 제공해요.</li><li>공식 문제집(New JLPT Sample Questions, 공식 모의고사집)도 안내돼 있어요(일부는 유료 교재).</li><li>실제 시험과 완전히 같지는 않지만, 유형·배점·시간 감을 잡기에 좋아요.</li></ul>'),
    ('JLPT 레벨과 합격 기준', '<p>JLPT는 N5(가장 쉬움)부터 N1(가장 어려움)까지 다섯 레벨이에요. 총점은 180점 만점이고, <b>합격하려면 종합 점수가 합격점 이상이면서 모든 영역이 기준점 이상</b>이어야 해요.</p>'
     '<table class="tbl"><thead><tr><th>레벨</th><th>종합 합격점</th><th>영역 구성</th></tr></thead><tbody>'
     '<tr><td>N1</td><td>100 / 180</td><td>언어지식·독해·청해 (각 60점, 각 19점 이상)</td></tr>'
     '<tr><td>N2</td><td>90 / 180</td><td>언어지식·독해·청해 (각 60점, 각 19점 이상)</td></tr>'
     '<tr><td>N3</td><td>95 / 180</td><td>언어지식·독해·청해 (각 60점, 각 19점 이상)</td></tr>'
     '<tr><td>N4</td><td>90 / 180</td><td>언어지식·독해(120점, 38점 이상) + 청해(60점, 19점 이상)</td></tr>'
     '<tr><td>N5</td><td>80 / 180</td><td>언어지식·독해(120점, 38점 이상) + 청해(60점, 19점 이상)</td></tr></tbody></table>'
     '<p>예를 들어 N2에서 총점 95점이어도 청해가 18점이면 기준점(19점) 미달이라 불합격이에요. 위 판정기로 영역별 기준까지 한 번에 확인하세요.</p>'),
    ('시험은 언제, 어디서 보나요', '<p>JLPT는 한국에서 보통 <b>연 2회(7월·12월)</b> 치러요. 접수와 일정은 국내 시행 기관 안내를 따르고, 레벨은 한 회차에 하나만 선택해요.</p>'
     '<p>점수 보고서에는 2025년부터 참고용 CEFR 등급도 함께 표기돼요. 유효기간이 따로 없지만, 기관·학교에서 보통 2년 이내 성적을 요구하는 경우가 많아요.</p>'),
    ('공부 순서 추천', '<ul><li>먼저 목표 레벨의 샘플문제로 유형(문자·어휘·문법·독해·청해)을 확인해요.</li><li>언어지식(문자·어휘·문법)에서 점수를 쌓고, 독해·청해는 시간 배분 연습이 중요해요.</li><li>영역 하나가 기준점에 못 미치면 전체가 불합격이라, 약한 영역을 기준점 이상으로 끌어올리는 걸 우선해요.</li></ul>'),
  ],
  faq=[('JLPT 기출문제를 받을 수 있나요?', '실제 시험지는 공개되지 않아요. 대신 공식 사이트 jlpt.jp에서 레벨별 샘플문제(유형 예시)를 무료로 받을 수 있어요.'),
       ('JLPT는 몇 점이면 합격인가요?', 'N1 100점, N2 90점, N3 95점, N4 90점, N5 80점(180점 만점) 이상이면서, 모든 영역이 기준점(보통 19점, N4·N5 언어지식·독해는 38점) 이상이어야 합격이에요.'),
       ('한 영역 점수가 낮으면 어떻게 되나요?', '종합 점수가 합격점을 넘어도, 한 영역이라도 기준점 미만이면 불합격이에요.'),
       ('JLPT는 1년에 몇 번 보나요?', '한국에서는 보통 7월과 12월, 연 2회 치러요.')],
  src='<li><a href="https://www.jlpt.jp/e/samples/forlearners.html" rel="noopener" target="_blank">JLPT 공식 사이트 (Japan Foundation·JEES)</a> — 레벨별 샘플문제·합격 기준 (2026-11-27 확인)</li>'))

# ─────────────────────────────────────────────────────────────────────────
# 4) 토익 Part5 (/ipsi/toeic-part5.html) — 오리지널 10문항
# ─────────────────────────────────────────────────────────────────────────
Q = [
 ['The marketing team will finalize the budget ______ the end of this week.',
  ['by','until','during','within'],0,
  '기한 안에 ‘완료’되는 동작에는 by(~까지)를 써요. until은 상태가 그때까지 계속될 때, within은 ‘~이내에’예요.'],
 ['All employees are required to ______ their identification badges at all times.',
  ['wear','wears','wearing','worn'],0,
  'be required to 뒤에는 동사원형이 와요. 그래서 wear가 정답이에요.'],
 ['The new software runs ______ than the previous version.',
  ['efficient','efficiently','more efficiently','most efficiently'],2,
  'than이 있으니 비교급이 필요하고, 동사(runs)를 꾸미니 부사예요. 둘 다 만족하는 more efficiently가 정답이에요.'],
 ['______ the heavy rain, the outdoor event was held as scheduled.',
  ['Although','Despite','Because','Therefore'],1,
  '뒤에 명사구(the heavy rain)가 오니 전치사 Despite(~에도 불구하고)가 맞아요. Although·Because는 뒤에 「주어+동사」 절이 와야 해요.'],
 ['Ms. Carter, ______ joined the firm last year, was promoted to manager.',
  ['who','which','whose','whom'],0,
  '사람(Ms. Carter)을 설명하는 주격 관계대명사는 who예요. whom은 목적격, whose는 소유격이에요.'],
 ['Please review the attached report ______ submitting your feedback.',
  ['before','ago','once','already'],0,
  '뒤에 동명사(submitting)가 오고 ‘제출하기 전에’라는 뜻이니 전치사 before가 정답이에요.'],
 ['The manager was very ______ with the quarterly results.',
  ['satisfy','satisfied','satisfying','satisfaction'],1,
  '사람이 느끼는 감정은 과거분사(-ed)로 써요. 그래서 satisfied(만족한)가 맞아요. satisfying은 ‘만족을 주는(사물)’이에요.'],
 ['Employees should submit their reports to ______ supervisor by noon.',
  ['they','them','their','theirs'],2,
  '명사(supervisor) 앞에서 ‘누구의’를 나타내니 소유격 their가 필요해요.'],
 ['The shipment is expected to ______ no later than Friday.',
  ['arrive','arrives','arrival','arriving'],0,
  'to 뒤에는 동사원형이 와요(to부정사). 그래서 arrive가 정답이에요. arrival은 명사예요.'],
 ['The two proposals are similar, but the first one is ______ detailed.',
  ['more','much','many','very'],0,
  'detailed(형용사)를 비교 의미로 꾸미려면 more detailed가 자연스러워요. much는 비교급 앞 강조로 쓰고, many는 셀 수 있는 명사에 써요.'],
]
toeic_js = _json.dumps(Q, ensure_ascii=False)
TOEIC_TOOL = ("""<section class="card tool" id="tool"><style>#tool h2{margin:0 0 10px}
#tq{font-size:18px;line-height:1.7;margin:4px 0 14px;font-weight:700}
#topts button{display:block;width:100%;text-align:left;box-sizing:border-box;margin:8px 0;padding:12px 14px;border:1px solid #D9DDE3;background:#fff;border-radius:12px;font-size:16px;font-family:inherit;cursor:pointer;color:#1F2937}
#topts button:hover{border-color:#1D4ED8}
#topts button.ok{background:#E7F7EC;border-color:#2BA85A;color:#13743A;font-weight:700}
#topts button.no{background:#FDECEC;border-color:#D64545;color:#8A1C1C}
#topts button:disabled{cursor:default}
#texp{margin:12px 0 0;padding:12px 14px;background:#F7F8FA;border:1px solid #E3E6EB;border-radius:12px;font-size:15px;line-height:1.7;display:none}
#tbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;color:#5B6B82;font-size:14px;font-weight:700}
.tnext{margin-top:14px}</style>
<h2>토익 Part 5 연습 — 10문항</h2>
<p class="note">홍라이프가 토익 Part 5(단문 빈칸) 형식으로 직접 만든 오리지널 연습문제예요. 보기를 고르면 정답과 해설이 바로 나와요. 실제 시험 문제가 아니라 유형 연습용이에요.</p>
<div id="tbar"><span id="tnum">1 / 10</span><span id="tsc">맞힌 개수 0</span></div>
<p id="tq">—</p>
<div id="topts"></div>
<div id="texp"></div>
<div class="tnext"><button class="btn dl" id="tnext" style="display:none">다음 문제 →</button><button class="btn" id="tretry" style="display:none">다시 풀기</button></div>
</section>""", """<script>
(function(){var $=HL.$;var Q="""+toeic_js+""";var i=0,score=0,done=false;var L=['(A)','(B)','(C)','(D)'];
function show(){done=false;var q=Q[i];$('#tnum').textContent=(i+1)+' / '+Q.length;$('#tsc').textContent='맞힌 개수 '+score;
 $('#tq').textContent=q[0];$('#texp').style.display='none';$('#tnext').style.display='none';$('#tretry').style.display='none';
 var h='';for(var k=0;k<q[1].length;k++)h+='<button data-k="'+k+'">'+L[k]+' '+q[1][k]+'</button>';$('#topts').innerHTML=h;
 var bs=$('#topts').querySelectorAll('button');for(var k=0;k<bs.length;k++)bs[k].addEventListener('click',pick);}
function pick(e){if(done)return;done=true;var k=+e.currentTarget.getAttribute('data-k');var q=Q[i];var bs=$('#topts').querySelectorAll('button');
 for(var j=0;j<bs.length;j++){bs[j].disabled=true;if(j===q[2])bs[j].className='ok';else if(j===k)bs[j].className='no';}
 if(k===q[2])score++;
 $('#tsc').textContent='맞힌 개수 '+score;
 $('#texp').style.display='block';$('#texp').innerHTML='<b>정답: '+L[q[2]]+' '+q[1][q[2]]+'</b><br>'+q[3];
 if(i<Q.length-1)$('#tnext').style.display='inline-block';else{$('#texp').innerHTML+='<br><br><b>끝! 10문항 중 '+score+'개를 맞혔어요.</b>';$('#tretry').style.display='inline-block';}}
$('#tnext').addEventListener('click',function(){i++;show();});
$('#tretry').addEventListener('click',function(){i=0;score=0;show();});
show();
})();
</script>""")
PAGES.append(dict(slug='toeic-part5', url='/ipsi/toeic-part5.html', sec=('입시·시험', '/ipsi/'), crumb3=' › 토익 Part5 연습', nosafe=True, warn='',
  name='토익 Part 5 연습문제 10문항 (문법·어휘 오리지널, 해설·채점)',
  h1='토익 Part 5 <b>연습 10문항</b>', lead='토익 Part 5(단문 빈칸) 형식으로 홍라이프가 직접 만든 오리지널 연습문제 10개예요. 보기를 고르면 정답과 해설이 바로 나오고, 맞힌 개수를 세어 줘요.',
  desc='토익 Part 5(단문 빈칸) 형식의 오리지널 연습문제 10문항을 풀고 정답·해설·점수를 바로 확인하세요. 전치사·접속사, 품사, 수동태, 비교급, 관계대명사 등 자주 나오는 문법·어휘 유형을 담았어요.',
  tool=TOEIC_TOOL, rel=rel_for('/ipsi/toeic-part5.html'),
  body=[
    ('토익 Part 5는 어떤 문제인가요', '<p>Part 5는 <b>한 문장에 빈칸 하나</b>가 있고, 보기 네 개(A~D) 중 알맞은 것을 고르는 문법·어휘 문제예요. 실제 토익에서 30문항이 나오고, 독해(RC) 시간을 아끼려면 한 문항을 20~30초 안에 푸는 게 중요해요.</p>'
     '<p>이 페이지의 10문항은 실제 기출이 아니라, 같은 유형으로 홍라이프가 직접 만든 연습문제예요. 그래서 저작권 걱정 없이 마음껏 풀 수 있어요.</p>'),
    ('Part 5에서 자주 나오는 유형', '<ul><li><b>품사 자리</b> — 빈칸이 형용사/부사/명사 중 무엇인지(동사를 꾸미면 부사).</li><li><b>전치사 vs 접속사</b> — 뒤에 명사면 전치사(Despite), 「주어+동사」면 접속사(Although).</li><li><b>동사 형태</b> — to 뒤 동사원형, 수동태(be+p.p.), 수일치.</li><li><b>관계대명사</b> — 사람·사물, 주격·목적격·소유격.</li><li><b>혼동 어휘</b> — satisfied/satisfying처럼 -ed/-ing 구분.</li></ul>'),
    ('빨리 푸는 요령', '<ul><li>빈칸 <b>앞뒤 단어</b>만 봐도 품사 자리가 보이는 문제가 많아요. 문장 전체를 해석하기 전에 자리부터 확인해요.</li><li>보기가 wear·wears·wearing·worn처럼 한 단어의 변형이면 <b>문법 문제</b>예요. 뜻이 다른 단어들이면 <b>어휘 문제</b>라 해석이 필요해요.</li><li>모르는 문제는 찍고 넘어가 독해 시간을 확보하세요. Part 5에서 오래 끌면 RC 전체가 밀려요.</li></ul>'),
    ('더 공부하려면', '<p>공식 샘플 문항은 토익 주관사 누리집(exam.toeic.co.kr)의 샘플 문제에서 볼 수 있어요. 실전 감각은 시중 문제집으로, 기본 유형은 이 연습문제로 반복하면 좋아요. 점수 환산·시간 배분 같은 안내는 홍라이프 도구에 이어서 올릴게요.</p>'),
  ],
  faq=[('이 문제는 실제 토익 기출인가요?', '아니요. 토익 Part 5 형식으로 홍라이프가 직접 만든 오리지널 연습문제예요. 실제 시험 문제가 아니라 유형 연습용이에요.'),
       ('토익 Part 5는 몇 문제 나오나요?', '실제 토익에서 Part 5는 30문항이에요. 독해(RC) 시간을 아끼려면 한 문항을 20~30초 안에 푸는 게 좋아요.'),
       ('문법과 어휘 중 뭐가 더 중요한가요?', '보기가 한 단어의 변형이면 문법, 뜻이 다른 단어들이면 어휘 문제예요. 둘 다 자주 나와서 유형을 익혀 두면 빨리 풀 수 있어요.'),
       ('정답 해설도 있나요?', '네. 보기를 고르면 정답과 한국어 해설이 바로 나오고, 10문항을 다 풀면 맞힌 개수를 알려 줘요.')],
  src='<li>문항·해설: 홍라이프 도구 자체 제작 (토익 Part 5 형식 참고, 2026-11-27)</li>'
      '<li><a href="https://exam.toeic.co.kr" rel="noopener" target="_blank">한국 토익위원회(YBM)</a> — 공식 샘플 문항·시험 안내 (2026-11-27 확인)</li>'))

if __name__ == '__main__':
    for p in PAGES:
        print('wrote', G.page(p))
