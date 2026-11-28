#!/usr/bin/env python3
"""한국사능력검정(심화) 기출 '풀면 바로 채점' 페이지 → overlay/ipsi/hanneung-gichul.html
정답을 미리 세팅(hanneung_answers.json)해서, 방문자는 문제지만 열어 풀고 OMR 마킹하면 바로 채점.
문제지 PDF는 저작권상 우리가 호스팅하지 않고 국사편찬위 공식 자료실로 연결. 실행:
    python3 build/newpages/gen_hanneung_gichul.py"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = json.load(open(os.path.join(ROOT, 'build/exams/data/hanneung_answers.json'), encoding='utf-8'))
ANS = DATA['answers']
ROUNDS = sorted((int(r) for r in ANS), reverse=True)
DAT = 'https://www.historyexam.go.kr/pst/list.do?bbs=dat'  # 공식 문제지 자료실(최근 15회차)

# 회차 카드: 문제지(공식 자료실) + 풀기(정답 미리 세팅)
_cards = []
for r in ROUNDS:
    key = ''.join(str(x) for x in ANS[str(r)])
    _cards.append(
        '<div class="hr-row"><b>제%d회</b><span class="hr-b">'
        '<a href="%s" target="_blank" rel="noopener nofollow">문제지</a>'
        '<a class="btn omr-solve" data-n="50" data-c="5" data-t="80" data-key="%s" data-name="%s" '
        'title="정답이 세팅돼 있어 풀고 마킹하면 바로 채점">▶ 풀고 채점</a>'
        '</span></div>' % (r, DAT, key, '제%d회 한국사 심화' % r))

TOOL = ("""<section class="card tool" id="tool"><style>
#tool h2{margin:22px 0 10px}#tool h2:first-of-type{margin-top:0}
.hr-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:4px 14px;margin:8px 0}
.hr-row{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #F0F1F3}
.hr-row b{flex:none;width:58px;color:#1D4ED8}
.hr-b{margin-left:auto;display:flex;gap:6px;align-items:center}
.hr-b a{font-size:13px}
.hr-b .omr-solve{cursor:pointer;padding:5px 11px}
.omr-dock{padding:10px 12px}.omr-dock-bar{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.omr-dock-bar b{font-size:16px}.omr-dock-bar .btn{margin-left:auto}
#omr-dock-frame{width:100%;height:88vh;border:1px solid #D9DDE3;border-radius:12px;background:#fff;display:block}
@media(max-width:820px){#omr-dock-frame{height:150vh}}
</style>
<h2 style="margin-top:0">회차 선택 → 바로 풀고 채점</h2>
<p class="note">정답이 <b>미리 세팅</b>돼 있어요. ‘문제지’로 공식 PDF를 받아서, ‘<b>풀고 채점</b>’을 누르면 그 자리에서 OMR이 열려요. 문제지를 <b>📄 PDF 열기</b>로 불러와 풀고 마킹한 뒤 <b>채점하기</b>를 누르면 — 정답 입력 없이 — 바로 점수가 나와요. 심화는 50문항·5지선다·80분이에요.</p>
<p class="btns"><a class="btn" href='""" + DAT + """' target="_blank" rel="noopener nofollow">📂 공식 문제지·정답 자료실(국사편찬위) ↗</a></p>
<section class="card omr-dock" id="omr-dock" hidden>
<div class="omr-dock-bar"><b>⏱ 풀고 채점</b><button class="btn" id="omr-dock-x" type="button">닫기 ✕</button></div>
<p class="note" style="margin:0 0 8px">정답은 이미 세팅돼 있어요. 받은 문제지를 <b>📄 PDF 열기</b>로 열고 풀어 마킹 → <b>채점하기</b>만 누르면 끝.</p>
<iframe id="omr-dock-frame" title="OMR 풀기" loading="lazy"></iframe></section>
<h2>전체 회차 (심화 44~81회)</h2>
<div class="hr-grid">""" + ''.join(_cards) + """</div>
</section>""", """<script>
(function(){var d=document.getElementById('omr-dock');if(!d)return;var fr=document.getElementById('omr-dock-frame');
document.querySelectorAll('.omr-solve').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();
var p=new URLSearchParams();p.set('embed','1');['n','c','t','key','name'].forEach(function(k){if(a.dataset[k])p.set(k,a.dataset[k]);});
fr.src='/ipsi/omr.html?'+p.toString();d.hidden=false;d.scrollIntoView({behavior:'smooth',block:'start'});});});
var x=document.getElementById('omr-dock-x');if(x)x.addEventListener('click',function(){d.hidden=true;fr.src='about:blank';});})();
</script>""")

P = dict(slug='hanneung-gichul', url='/ipsi/hanneung-gichul.html', sec=('시험·공부', '/ipsi/'), crumb3=' › 한국사능력검정 기출 채점', nosafe=True, warn='',
  name='한국사능력검정 심화 기출 풀고 바로 채점 — 44~81회 정답 세팅 OMR (무료)',
  h1='한국사능력검정 <b>기출 풀고 바로 채점</b>',
  lead='한국사능력검정시험 심화 기출(44~81회)을 실제처럼 풀고 바로 채점해요. 정답이 미리 들어 있어 따로 입력할 필요 없이, 문제지 받아서 풀고 OMR 마킹하면 몇 점인지·틀린 문항까지 바로 나와요.',
  desc='한국사능력검정 심화 기출 44~81회를 풀고 자동 채점하는 무료 도구예요. 공식 문제지(국사편찬위)를 열어 시간 맞춰 풀고 OMR에 마킹하면, 정답이 미리 세팅돼 있어 입력 없이 바로 점수·정답률·틀린 문항이 나와요. 50문항 5지선다 80분.',
  tool=TOOL, rel=('<section class="card rel"><h2>함께 보면 좋은 기출</h2><ul>'
    '<li><a href="/ipsi/hanneung.html"><b>한국사능력검정 급수·일정</b><span>시험 안내·합격 기준</span></a></li>'
    '<li><a href="/ipsi/gichul/"><b>수능·모의평가 기출</b><span>2005~2027학년도 풀고 채점</span></a></li>'
    '<li><a href="/ipsi/omr.html"><b>OMR 채점기</b><span>어떤 시험이든 풀고 채점</span></a></li></ul></section>'),
  body=[
    ('어떻게 쓰나요', '<ol><li><b>문제지 받기</b> — 회차 옆 ‘문제지’(또는 위 자료실 버튼)로 국사편찬위 공식 PDF를 받아요. 최근 15개 회차 문제지가 공식 제공돼요.</li>'
     '<li><b>풀고 채점</b>을 누르면 그 자리에서 OMR이 열려요. <b>📄 PDF 열기</b>로 받은 문제지를 불러와 왼쪽에 띄워요.</li>'
     '<li>시간(80분) 맞춰 풀고 OMR에 마킹해요.</li>'
     '<li><b>채점하기</b>를 누르면 정답이 이미 세팅돼 있어 <b>입력 없이</b> 점수·정답률·틀린 문항이 바로 나와요.</li></ol>'),
    ('급수·합격 기준', '<p>심화는 1·2·3급을 나눠요. 100점 만점에 <b>80점 이상 1급, 70~79점 2급, 60~69점 3급</b>이에요. 50문항이라 한 문항은 2점꼴(배점은 1~3점으로 조금씩 달라요).</p>'
     '<p>기본(4·5·6급)은 별도 시험이에요. 이 페이지는 심화 기출만 다뤄요.</p>'),
    ('정답은 어디서 온 거예요', '<p>국사편찬위원회 한국사능력검정시험 <b>공식 정답(정답 보기)</b>을 회차별로 그대로 반영했어요. 그래서 따로 입력할 필요가 없어요. 문제지 저작권은 원저작자에 있어 PDF는 공식 자료실로만 연결해요.</p>'),
  ],
  faq=[('정답을 입력해야 하나요?', '아니요. 회차별 공식 정답이 미리 세팅돼 있어요. 문제 풀고 OMR 마킹한 뒤 채점하기만 누르면 바로 점수가 나와요.'),
       ('문제지는 어디서 받나요?', '회차 옆 ‘문제지’ 또는 위 자료실 버튼으로 국사편찬위 공식 PDF를 받아요. 최근 15개 회차가 공식 제공돼요.'),
       ('심화는 몇 문항인가요?', '50문항, 5지선다, 제한 시간 80분이에요. 80점 이상이면 1급이에요.'),
       ('몇 회차까지 채점되나요?', '심화 44회부터 81회까지 공식 정답이 들어 있어 바로 채점돼요.')],
  src='<li>정답: 국사편찬위원회 한국사능력검정시험 공식 정답 (historyexam.go.kr, 2026-11-28 확인)</li><li>문제지: 국사편찬위 공식 자료실로 연결(저작권 원저작자)</li>')

if __name__ == '__main__':
    print('wrote', G.page(P), '| 회차', len(ROUNDS))
