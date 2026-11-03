#!/usr/bin/env python3
"""Build /student/ pages. Run from site root: python3 student/gen.py"""
import json, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = open(os.path.join(ROOT, "student", "_head.html"), encoding="utf-8").read()
E = html.escape
TODAY = "2026-11-03"

def page(fn, title, desc, body, faq, crumb, og="student"):
    path = "/student/" + ("" if fn == "index.html" else fn)
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://honglife.co.kr/"},
            {"@type": "ListItem", "position": 2, "name": "학생 계산기", "item": "https://honglife.co.kr/student/"}] +
            ([{"@type": "ListItem", "position": 3, "name": crumb, "item": "https://honglife.co.kr" + path}] if fn != "index.html" else [])},
    ]
    if fn != "index.html":
        ld.append({"@context": "https://schema.org", "@type": "WebApplication", "name": crumb, "url": "https://honglife.co.kr" + path,
                   "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "inLanguage": "ko-KR",
                   "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}})
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    h = (HEAD.replace("{LANG}", "ko").replace("{TITLE}", E(title)).replace("{DESC}", E(desc))
         .replace("{URL}", "https://honglife.co.kr" + path).replace("{ROBOTS}", "")
         .replace("{OG}", "https://honglife.co.kr/assets/og/%s.png" % og)
         .replace("{LD}", "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in ld)))
    faqhtml = ""
    if faq:
        faqhtml = '<section class="card"><h2>자주 묻는 질문</h2>' + "".join(
            "<h3>%s</h3><p>%s</p>" % (E(q), E(a)) for q, a in faq) + "</section>"
    nav = ('<div class="brandbar"><div class="in"><a class="logo" href="/"><i>₩</i>홍라이프 계산기</a><span class="meta">'
           '<a href="/student/naesin.html">내신</a><a href="/student/suneung-score.html">수능 점수</a><a href="/student/average.html">비율 평균</a></span></div></div>\n')
    crumbs = '<nav class="crumb" aria-label="현재 위치"><a href="/">홈</a> › ' + (
        '<span>학생 계산기</span>' if fn == "index.html" else '<a href="/student/">학생 계산기</a> › <span>%s</span>' % E(crumb)) + "</nav>"
    full = (h + nav + '<div class="wrap">' + crumbs + body + faqhtml +
            '<p class="note">홍라이프 학생 계산기 · 2026년 11월 3일 기준. 학교·대학별 산출 방식이 다를 수 있으니 최종 성적은 학교 성적표와 대학 모집요강으로 확인하세요.</p></div>\n'
            '<script src="/assets/app.js" defer></script>\n<script src="/assets/share.js" defer></script>\n</body>\n</html>\n')
    open(os.path.join(ROOT, "student", fn), "w", encoding="utf-8").write(full)

# ---------------------------------------------------------------- 내신
NAESIN_BODY = r'''
<header class="top"><p class="kicker">학생 · 내신 · 2026년 기준</p><h1><b>내신 등급</b> 계산기</h1>
<p class="lead">과목별 학점(단위수)과 등급을 넣으면 학점 가중 평균 등급을 바로 계산해요. 2025년 고1부터 적용된 <b>5등급제</b>와 기존 <b>9등급제</b>를 모두 지원하고, 학년별 반영 비율(예: 20:40:40)과 반영 교과(국영수사과 등)도 직접 조절할 수 있어요. 석차로 등급을 구하는 계산기도 함께 있어요.</p></header>

<section class="calc" id="c1">
<h2>평균 등급 계산</h2>
<div class="seg" role="group" aria-label="등급제"><button type="button" data-sys="5" aria-pressed="true">5등급제 (2025 고1부터)</button><button type="button" data-sys="9" aria-pressed="false">9등급제 (2024 입학생까지)</button></div>
<p class="hint" id="sysHint"></p>
<div class="rows" id="rows"></div>
<button type="button" class="addr" id="add">+ 과목 추가</button>

<h3 style="margin-top:16px">학년별 반영 비율 (%)</h3>
<div class="grid3"><label class="fld">1학년<input id="w1" type="number" inputmode="decimal" value="33.3" min="0"></label><label class="fld">2학년<input id="w2" type="number" inputmode="decimal" value="33.3" min="0"></label><label class="fld">3학년<input id="w3" type="number" inputmode="decimal" value="33.4" min="0"></label></div>
<div class="seg" role="group" aria-label="반영 비율 빠른 선택"><button type="button" class="wp" data-w="1,1,1" aria-pressed="false">동일 반영</button><button type="button" class="wp" data-w="20,40,40" aria-pressed="false">20:40:40</button><button type="button" class="wp" data-w="20,30,50" aria-pressed="false">20:30:50</button><button type="button" class="wp" data-w="30,30,40" aria-pressed="false">30:30:40</button></div>

<h3>반영 교과</h3>
<div class="seg" role="group" aria-label="반영 교과" id="grp"></div>

<div class="res">
 <div class="main"><div class="k">반영 교과 평균 등급</div><div class="big" id="rMain">-</div><div class="sub" id="rMainS"></div></div>
 <div><div class="k">학년 비율 적용 등급</div><div class="big" id="rW">-</div><div class="sub" id="rWS"></div></div>
 <div><div class="k">전 과목 평균 등급</div><div class="big" id="rAll">-</div><div class="sub" id="rAllS"></div></div>
</div>
<div class="scroll"><table class="tbl" id="yr"></table></div>
<p class="hint">평균 등급 = Σ(등급 × 학점) ÷ Σ학점. 학년 비율 적용 등급은 학년마다 학점 가중 평균을 먼저 낸 뒤, 입력이 있는 학년끼리 비율을 다시 100%로 맞춰 계산해요.</p>
</section>

<section class="calc" id="c2">
<h2>석차로 등급 구하기</h2>
<div class="seg" role="group" aria-label="등급제"><button type="button" data-sys2="5" aria-pressed="true">5등급제</button><button type="button" data-sys2="9" aria-pressed="false">9등급제</button></div>
<div class="grid3"><label class="fld">내 석차<input id="rk" type="number" inputmode="numeric" value="12" min="1"></label><label class="fld">동석차 인원(나 포함)<input id="tie" type="number" inputmode="numeric" value="1" min="1"></label><label class="fld">수강자 수<input id="n" type="number" inputmode="numeric" value="150" min="1"></label></div>
<div class="res"><div class="main"><div class="k">석차 등급</div><div class="big" id="g2">-</div><div class="sub" id="g2s"></div></div><div><div class="k">중간석차 백분율</div><div class="big" id="p2">-</div><div class="sub">상위 몇 %인지</div></div></div>
<div class="scale" id="scale"></div><div class="mark" id="mark"></div>
<div class="scroll"><table class="tbl" id="cut"></table></div>
<p class="hint">중간석차 = 석차 + (동석차 인원 − 1) ÷ 2, 중간석차 백분율 = 중간석차 ÷ 수강자 수 × 100. 이 백분율이 등급별 누적 비율 이하이면 그 등급이에요. 등급별 인원은 수강자 수 × 누적 비율로 계산한 참고값이며, 학교는 학업성적관리규정에 따라 산출해요.</p>
</section>

<section class="card"><h2>5등급제와 9등급제, 무엇이 달라졌나</h2>
<p>2025학년도 고1부터 고교학점제와 함께 내신이 <b>5등급 상대평가</b>로 바뀌었어요. 2026년 기준으로 <b>고1·고2는 5등급제</b>, <b>고3(2024년 입학생)은 9등급제</b>를 그대로 써요.</p>
<div class="scroll"><table class="tbl"><tr><th>등급</th><th>5등급제 누적 비율</th><th>9등급제 누적 비율</th></tr>
<tr><td>1</td><td>상위 10%</td><td>상위 4%</td></tr><tr><td>2</td><td>34%</td><td>11%</td></tr><tr><td>3</td><td>66%</td><td>23%</td></tr><tr><td>4</td><td>90%</td><td>40%</td></tr><tr><td>5</td><td>100%</td><td>60%</td></tr><tr><td>6</td><td>-</td><td>77%</td></tr><tr><td>7</td><td>-</td><td>89%</td></tr><tr><td>8</td><td>-</td><td>96%</td></tr><tr><td>9</td><td>-</td><td>100%</td></tr></table></div>
<p>5등급제에서는 성취도(A~E)와 석차 등급이 함께 기재되고, 1학년 공통과목뿐 아니라 2·3학년 선택과목도 상대평가 등급이 붙어요(사회·과학 융합선택 등 일부 과목은 성취도만 기재). 대학마다 등급 환산 점수와 반영 교과가 달라서, 이 계산기의 평균 등급은 <b>내 위치를 가늠하는 기준값</b>으로 보세요.</p></section>
'''
NAESIN_JS = r'''<script>
(function(){
const $=id=>document.getElementById(id);
const CUM={5:[10,34,66,90,100],9:[4,11,23,40,60,77,89,96,100]};
const COL=['#12305C','#1F4A86','#3E6BA8','#C9A04A','#B8862B','#8C6418','#A3A9B5','#7C8494','#5B6372'];
const GROUPS=['국어','수학','영어','사회','과학','기타'];
let sys=5, sel=new Set(['국어','수학','영어','사회','과학']);
const DEF=[[1,1,'국어','국어',4,2],[1,1,'수학','수학',4,3],[1,1,'영어','영어',4,2],[1,1,'통합사회','사회',3,2],[1,1,'통합과학','과학',3,3],[1,1,'한국사','사회',3,1]];
function grpOpts(v){return GROUPS.map(g=>'<option'+(g===v?' selected':'')+'>'+g+'</option>').join('')}
function gradeOpts(v){let s='';for(let i=1;i<=sys;i++)s+='<option value="'+i+'"'+(i==v?' selected':'')+'>'+i+'등급</option>';return s}
function addRow(r){r=r||[1,1,'','국어',4,Math.min(3,sys)];const d=document.createElement('div');d.className='row ns';
 const o=(n,v,suf)=>{let s='';for(let i=1;i<=n;i++)s+='<option value="'+i+'"'+(i==v?' selected':'')+'>'+i+suf+'</option>';return s};
 d.innerHTML='<input class="nm" placeholder="과목명 (예: 국어)" value="'+(r[2]||'')+'" aria-label="과목명"><select class="g" aria-label="교과">'+grpOpts(r[3])+'</select>'+
 '<select class="y" aria-label="학년">'+o(3,r[0],'학년')+'</select><select class="s" aria-label="학기">'+o(2,r[1],'학기')+'</select>'+
 '<label class="uc"><input class="u" type="number" inputmode="decimal" min="0" step="0.5" value="'+r[4]+'" aria-label="학점"><span>학점</span></label>'+
 '<select class="gr" aria-label="등급">'+gradeOpts(r[5])+'</select><button type="button" class="x" aria-label="삭제">×</button>';
 d.querySelector('.x').onclick=()=>{d.remove();calc()};$('rows').appendChild(d)}
function rows(){return [...document.querySelectorAll('#rows .row')].map(d=>({y:+d.querySelector('.y').value,s:+d.querySelector('.s').value,g:d.querySelector('.g').value,u:parseFloat(d.querySelector('.u').value)||0,gr:+d.querySelector('.gr').value}))}
const f2=x=>isFinite(x)?x.toFixed(2):'-';
function avg(list){const U=list.reduce((a,r)=>a+r.u,0);return U?{v:list.reduce((a,r)=>a+r.gr*r.u,0)/U,u:U}:{v:NaN,u:0}}
function calc(){
 const R=rows().filter(r=>r.u>0);const inc=R.filter(r=>sel.has(r.g));
 const all=avg(R),m=avg(inc);
 $('rAll').textContent=f2(all.v);$('rAllS').textContent='전체 '+R.length+'과목 · '+all.u+'학점';
 $('rMain').textContent=f2(m.v);$('rMainS').textContent=[...sel].join('·')+' '+inc.length+'과목 · '+m.u+'학점';
 const w=[+$('w1').value||0,+$('w2').value||0,+$('w3').value||0];let ws=0,acc=0,rowsH='<tr><th>학년</th><th>반영 과목</th><th>학점</th><th>평균 등급</th><th>반영 비율</th></tr>';
 const ys=[1,2,3].map(y=>avg(inc.filter(r=>r.y===y)));const tw=ys.reduce((a,o,i)=>a+(o.u?w[i]:0),0);
 ys.forEach((o,i)=>{if(o.u&&tw){acc+=o.v*w[i]/tw;ws+=w[i]}rowsH+='<tr><td>'+(i+1)+'학년</td><td>'+inc.filter(r=>r.y===i+1).length+'</td><td>'+o.u+'</td><td>'+f2(o.v)+'</td><td>'+(o.u&&tw?(w[i]/tw*100).toFixed(1)+'%':'-')+'</td></tr>'});
 $('rW').textContent=ws?f2(acc):'-';$('rWS').textContent='입력된 학년 비율 '+w.join(':');$('yr').innerHTML=rowsH;
}
function setSys(v){sys=v;document.querySelectorAll('[data-sys]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.sys==v));
 document.querySelectorAll('#rows .gr').forEach(s=>{const c=Math.min(+s.value,sys);s.innerHTML=gradeOpts(c)});
 $('sysHint').textContent=v==5?'2025년 이후 고교 입학생(2026년 기준 고1·고2). 1~5등급, 누적 10·34·66·90·100%.':'2024년 이전 고교 입학생(2026년 기준 고3). 1~9등급, 누적 4·11·23·40·60·77·89·96·100%.';calc()}
document.querySelectorAll('[data-sys]').forEach(b=>b.onclick=()=>setSys(+b.dataset.sys));
document.querySelectorAll('.wp').forEach(b=>b.onclick=()=>{const w=b.dataset.w.split(',').map(Number),s=w.reduce((a,c)=>a+c,0);['w1','w2','w3'].forEach((id,i)=>$(id).value=(w[i]/s*100).toFixed(1));calc()});
$('grp').innerHTML=GROUPS.map(g=>'<button type="button" data-g="'+g+'" aria-pressed="'+sel.has(g)+'">'+g+'</button>').join('');
$('grp').onclick=e=>{const b=e.target.closest('button');if(!b)return;const g=b.dataset.g;sel.has(g)?sel.delete(g):sel.add(g);b.setAttribute('aria-pressed',sel.has(g));calc()};
$('add').onclick=()=>{const last=rows().pop();addRow([last?last.y:1,last?last.s:1,'',last?last.g:'국어',4,Math.min(3,sys)]);calc()};
document.getElementById('c1').addEventListener('input',calc);document.getElementById('c1').addEventListener('change',calc);
DEF.forEach(addRow);setSys(5);
// 석차
let sys2=5;
function calc2(){const rk=+$('rk').value||0,t=Math.max(1,+$('tie').value||1),n=+$('n').value||0;const C=CUM[sys2];
 if(!n||!rk||rk>n){$('g2').textContent='-';$('p2').textContent='-';return}
 const mid=rk+(t-1)/2,p=mid/n*100;let g=C.findIndex(c=>p<=c+1e-9)+1;
 $('g2').textContent=g+'등급';$('g2s').textContent=sys2+'등급제 · 중간석차 '+(+mid.toFixed(1))+'등';$('p2').textContent=p.toFixed(2)+'%';
 let prev=0,sc='',tb='<tr><th>등급</th><th>누적 비율</th><th>누적 인원(참고)</th></tr>';
 C.forEach((c,i)=>{sc+='<span style="width:'+(c-prev)+'%;background:'+COL[sys2==5?[0,2,3,5,7][i]:i]+'">'+(i+1)+'</span>';tb+='<tr'+(i+1===g?' class="on"':'')+'><td>'+(i+1)+'</td><td>'+c+'%</td><td>'+Math.round(n*c/100)+'명</td></tr>';prev=c});
 $('scale').innerHTML=sc;$('mark').innerHTML='<i style="left:'+Math.min(100,p)+'%"></i>';$('cut').innerHTML=tb}
document.querySelectorAll('[data-sys2]').forEach(b=>b.onclick=()=>{sys2=+b.dataset.sys2;document.querySelectorAll('[data-sys2]').forEach(x=>x.setAttribute('aria-pressed',x===b));calc2()});
['rk','tie','n'].forEach(id=>$(id).addEventListener('input',calc2));calc2();
})();
</script>'''
NAESIN_FAQ = [
 ("내신 평균 등급은 어떻게 계산하나요?", "과목마다 등급에 학점(단위수)을 곱해 모두 더한 뒤, 학점 합계로 나눠요. 예를 들어 국어 4학점 2등급, 수학 4학점 3등급, 통합과학 3학점 3등급이면 (8+12+9)÷11 = 2.64등급이에요."),
 ("5등급제는 언제부터 적용되나요?", "2025년 고등학교 1학년(2028학년도 대입 응시 학년)부터 적용돼요. 2026년 기준 고1·고2는 5등급제, 고3은 기존 9등급제를 써요."),
 ("5등급제 1등급은 몇 %인가요?", "누적 상위 10%까지가 1등급이에요. 2등급은 34%, 3등급 66%, 4등급 90%, 나머지가 5등급이에요. 9등급제 1등급(4%)보다 넓어요."),
 ("동점자가 있으면 등급은 어떻게 정하나요?", "동석차가 있으면 중간석차를 써요. 중간석차 = 석차 + (동석차 인원 − 1) ÷ 2이고, 이를 수강자 수로 나눈 백분율이 등급 누적 비율 이하인지로 등급을 정해요."),
 ("학년별 반영 비율은 어디서 확인하나요?", "대학 수시 모집요강의 학생부 교과 반영 방법에서 확인할 수 있어요. 최근에는 학년별 비율 없이 전 학년을 동일하게 반영하는 대학이 많지만, 일부 전형은 학년별 비율을 두기도 해요."),
]

# ---------------------------------------------------------------- 수능
SUN_BODY = r'''
<header class="top"><p class="kicker">학생 · 수능 · 2026학년도 실채점 기준</p><h1><b>수능 표준점수·백분위·등급</b> 계산기</h1>
<p class="lead">표준점수로 등급과 백분위를 확인하고, 원점수·평균·표준편차로 표준점수를 직접 계산해요. 등급 기준은 한국교육과정평가원이 2025년 12월 4일 발표한 <b>2026학년도 수능 채점 결과</b>예요. 2027학년도 수능(2026년 11월 19일)의 등급컷은 12월 채점 결과 발표 뒤 바뀌어요.</p></header>

<section class="calc" id="s1">
<h2>표준점수 → 등급·백분위</h2>
<label class="fld">영역·과목<select id="subj"></select></label>
<label class="fld" id="scLab">표준점수<input id="sc" type="number" inputmode="numeric" value="130"></label>
<div class="res">
 <div class="main"><div class="k">등급</div><div class="big" id="gr">-</div><div class="sub" id="grs"></div></div>
 <div id="pctBox"><div class="k">백분위(추정)</div><div class="big" id="pct">-</div><div class="sub" id="pcts">등급컷 사이를 선으로 이어 추정</div></div>
 <div><div class="k">다음 등급까지</div><div class="big" id="up">-</div><div class="sub" id="ups"></div></div>
</div>
<div class="scroll"><table class="tbl" id="tb"></table></div>
<p class="hint" id="note"></p>
</section>

<section class="calc" id="s2">
<h2>원점수 → 표준점수</h2>
<div class="seg" role="group" aria-label="영역 유형"><button type="button" data-t="20" aria-pressed="true">국어·수학 (평균 100, 표준편차 20)</button><button type="button" data-t="10" aria-pressed="false">탐구·제2외국어 (평균 50, 표준편차 10)</button></div>
<div class="grid3"><label class="fld">내 원점수<input id="raw" type="number" inputmode="decimal" value="85"></label><label class="fld">전체 평균<input id="mu" type="number" inputmode="decimal" value="58.2"></label><label class="fld">표준편차<input id="sd" type="number" inputmode="decimal" value="20.5"></label></div>
<div class="res"><div class="main"><div class="k">표준점수</div><div class="big" id="ss">-</div><div class="sub" id="sss"></div></div><div><div class="k">평균과의 거리</div><div class="big" id="z">-</div><div class="sub">표준편차 몇 배인지 (z)</div></div><div><div class="k">백분위(정규분포 가정)</div><div class="big" id="zp">-</div><div class="sub">실제 백분위와 다를 수 있어요</div></div></div>
<p class="hint">표준점수 = (원점수 − 평균) ÷ 표준편차 × 20 + 100 (탐구는 × 10 + 50), 소수점 첫째 자리에서 반올림해요. 국어·수학은 선택과목에 따라 점수를 조정한 뒤 계산하기 때문에, 공통·선택 원점수만으로 낸 값은 실제 성적표와 1~3점 차이 날 수 있어요. 평균과 표준편차는 모의고사 성적 통지표나 평가원 채점 결과에서 확인하세요.</p>
</section>

<section class="calc" id="s3">
<h2>영어·한국사 등급 (절대평가)</h2>
<div class="grid2"><label class="fld">영어 원점수 (100점)<input id="en" type="number" inputmode="numeric" value="84"></label><label class="fld">한국사 원점수 (50점)<input id="hi" type="number" inputmode="numeric" value="38"></label></div>
<div class="res"><div class="main"><div class="k">영어 등급</div><div class="big" id="eng">-</div><div class="sub" id="engs"></div></div><div><div class="k">한국사 등급</div><div class="big" id="his">-</div><div class="sub" id="hiss"></div></div></div>
<p class="hint">영어는 90점 이상 1등급부터 10점 간격, 한국사는 40점 이상 1등급부터 5점 간격이에요. 비율은 2026학년도 수능 영어 등급별 인원 비율이에요.</p>
</section>

<section class="card"><h2>2026학년도 수능, 숫자로 보면</h2>
<ul><li>응시자 493,896명(재학생 333,102명, 졸업생 등 160,794명)</li>
<li>국어 표준점수 최고점 147점, 1등급 컷 133점</li>
<li>수학 표준점수 최고점 139점, 1등급 컷 128점</li>
<li>영어 1등급(90점 이상) 3.11% — 절대평가 도입 뒤 가장 낮은 비율</li></ul>
<p>표준점수는 시험이 어려울수록 최고점이 올라가요. 그래서 같은 등급이라도 해마다 표준점수가 달라요. 백분위는 "나보다 점수가 낮은 학생 비율"로, 99면 상위 1% 안쪽이에요.</p></section>
'''
SUN_DATA = {
 "국어": {"type": "ks", "max": 147, "cut": [133,126,117,107,94,83,73,66], "pct": [96,89,77,61,40,23,11,4]},
 "수학": {"type": "ks", "max": 139, "cut": [128,124,119,111,92,79,74,71], "pct": [96,88,76,60,40,23,12,5]},
 "생활과 윤리": {"type": "t", "cut": [66,64,59,53,46,42,36,33]},
 "윤리와 사상": {"type": "t", "cut": [66,64,59,53,45,41,38,34]},
 "한국지리": {"type": "t", "cut": [68,65,59,52,45,41,39,36]},
 "세계지리": {"type": "t", "cut": [68,63,59,53,45,40,38,35]},
 "동아시아사": {"type": "t", "cut": [65,62,59,55,46,40,37,35]},
 "세계사": {"type": "t", "cut": [68,64,59,52,45,41,38,36]},
 "경제": {"type": "t", "cut": [68,65,59,52,45,41,39,36]},
 "정치와 법": {"type": "t", "cut": [65,62,59,55,46,40,37,34]},
 "사회·문화": {"type": "t", "cut": [65,62,59,54,47,41,36,33]},
 "물리학Ⅰ": {"type": "t", "cut": [66,64,60,53,46,41,38,35]},
 "화학Ⅰ": {"type": "t", "cut": [67,64,59,52,46,41,38,36]},
 "생명과학Ⅰ": {"type": "t", "cut": [67,63,59,54,47,42,37,33]},
 "지구과학Ⅰ": {"type": "t", "cut": [65,63,59,54,46,40,37,35]},
 "물리학Ⅱ": {"type": "t", "cut": [66,63,60,54,45,40,38,36]},
 "화학Ⅱ": {"type": "t", "cut": [68,64,59,53,45,41,39,36]},
 "생명과학Ⅱ": {"type": "t", "cut": [65,63,60,54,45,41,37,35]},
 "지구과학Ⅱ": {"type": "t", "cut": [68,65,60,51,44,41,39,38]},
}
SUN_JS = r'''<script>
(function(){
const $=id=>document.getElementById(id);const D=__DATA__;
const ENG=[3.11,14.35,26.30,24.53,13.28,8.02,5.64,3.65,1.13];
$('subj').innerHTML='<optgroup label="국어·수학"><option>국어</option><option>수학</option></optgroup><optgroup label="사회탐구">'+['생활과 윤리','윤리와 사상','한국지리','세계지리','동아시아사','세계사','경제','정치와 법','사회·문화'].map(s=>'<option>'+s+'</option>').join('')+'</optgroup><optgroup label="과학탐구">'+['물리학Ⅰ','화학Ⅰ','생명과학Ⅰ','지구과학Ⅰ','물리학Ⅱ','화학Ⅱ','생명과학Ⅱ','지구과학Ⅱ'].map(s=>'<option>'+s+'</option>').join('')+'</optgroup>';
function c1(){const s=$('subj').value,d=D[s],v=parseFloat($('sc').value);if(!isFinite(v)){return}
 let g=d.cut.findIndex(c=>v>=c)+1;if(!g)g=9;$('gr').textContent=g+'등급';$('grs').textContent=s+' 2026학년도 수능 기준';
 if(d.type==='ks'){$('pctBox').hidden=false;const xs=[d.max].concat(d.cut),ys=[100].concat(d.pct);let p;
  if(v>=d.max)p=100;else if(v<d.cut[7]){p=Math.max(0,d.pct[7]-(d.cut[7]-v)*0.4)}else{for(let i=0;i<xs.length-1;i++){if(v<=xs[i]&&v>=xs[i+1]){p=ys[i+1]+(ys[i]-ys[i+1])*(v-xs[i+1])/(xs[i]-xs[i+1]);break}}}
  $('pct').textContent=Math.round(Math.max(0,Math.min(100,p)));}
 else $('pctBox').hidden=true;
 if(g>1){const need=d.cut[g-2]-v;$('up').textContent='+'+need+'점';$('ups').textContent=(g-1)+'등급 컷 '+d.cut[g-2]+'점'}else{$('up').textContent='1등급';$('ups').textContent=d.max?'최고점 '+d.max+'점':'최고 등급'}
 let t='<tr><th>등급</th><th>표준점수 컷</th>'+(d.type==='ks'?'<th>컷 백분위</th>':'')+'</tr>';d.cut.forEach((c,i)=>{t+='<tr'+(i+1===g?' class="on"':'')+'><td>'+(i+1)+'</td><td>'+c+'점 이상</td>'+(d.type==='ks'?'<td>'+d.pct[i]+'</td>':'')+'</tr>'});
 t+='<tr'+(g===9?' class="on"':'')+'><td>9</td><td>'+d.cut[7]+'점 미만</td>'+(d.type==='ks'?'<td>-</td>':'')+'</tr>';$('tb').innerHTML=t;
 $('note').textContent=d.type==='ks'?'국어·수학 등급컷은 평가원 2026학년도 수능 채점 결과의 등급 구분 표준점수예요. 백분위는 등급컷 지점의 백분위를 선으로 이어 계산한 추정값이라 실제 성적표와 1~2 차이 날 수 있어요.':'탐구 등급컷은 2026학년도 수능 채점 결과의 과목별 등급 구분 표준점수예요. 탐구 백분위는 과목마다 분포가 달라 추정하지 않았어요.'}
$('subj').addEventListener('change',()=>{const d=D[$('subj').value];$('sc').value=d.cut[1];c1()});$('sc').addEventListener('input',c1);c1();
let T=20;function c2(){const r=parseFloat($('raw').value),m=parseFloat($('mu').value),s=parseFloat($('sd').value);if(!(s>0)||!isFinite(r)||!isFinite(m))return;
 const z=(r-m)/s,ss=Math.round(z*T+(T===20?100:50));$('ss').textContent=ss+'점';$('sss').textContent='('+r+' − '+m+') ÷ '+s+' × '+T+' + '+(T===20?100:50);$('z').textContent=z.toFixed(2);
 const cdf=x=>{const t=1/(1+0.2316419*Math.abs(x)),dd=0.3989423*Math.exp(-x*x/2),p=dd*t*(0.3193815+t*(-0.3565638+t*(1.781478+t*(-1.821256+t*1.330274))));return x>0?1-p:p};$('zp').textContent=Math.round(cdf(z)*100)}
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{T=+b.dataset.t;document.querySelectorAll('[data-t]').forEach(x=>x.setAttribute('aria-pressed',x===b));if(T===10){$('raw').value=42;$('mu').value=31.5;$('sd').value=11.2}else{$('raw').value=85;$('mu').value=58.2;$('sd').value=20.5}c2()});
['raw','mu','sd'].forEach(id=>$(id).addEventListener('input',c2));c2();
function c3(){const e=parseFloat($('en').value),h=parseFloat($('hi').value);
 if(isFinite(e)){const gg=e>=90?1:Math.max(1,Math.min(9,10-Math.floor(e/10)));$('eng').textContent=gg+'등급';$('engs').textContent='2026 수능 '+gg+'등급 비율 '+ENG[gg-1]+'%'}
 if(isFinite(h)){const g2=h>=40?1:Math.max(1,Math.min(9,9-Math.floor(h/5)));$('his').textContent=g2+'등급';$('hiss').textContent=g2===1?'40점 이상':(g2<9?(45-g2*5)+'~'+(49-g2*5)+'점 구간':'5점 미만')}}
['en','hi'].forEach(id=>$(id).addEventListener('input',c3));c3();
})();
</script>'''
SUN_FAQ = [
 ("2026학년도 수능 국어·수학 1등급 컷은 몇 점인가요?", "평가원 채점 결과 기준 표준점수로 국어 133점, 수학 128점이에요. 표준점수 최고점은 국어 147점, 수학 139점이었어요."),
 ("표준점수는 어떻게 계산하나요?", "국어·수학은 (원점수 − 평균) ÷ 표준편차 × 20 + 100, 탐구는 × 10 + 50이에요. 평균보다 표준편차 1배 높으면 국어·수학 120점, 탐구 60점이 돼요."),
 ("백분위는 무엇인가요?", "나보다 표준점수가 낮은 수험생의 비율(0~100)이에요. 백분위 96이면 상위 약 4%로, 국어·수학에서는 1등급 경계 부근이에요."),
 ("영어 1등급은 몇 점인가요?", "영어는 절대평가라 원점수 90점 이상이면 1등급이에요. 2026학년도 수능은 영어 1등급 비율이 3.11%로 절대평가 도입 이후 가장 낮았어요."),
 ("2027학년도 수능 등급컷은 언제 나오나요?", "2027학년도 수능은 2026년 11월 19일에 치러지고, 평가원 채점 결과(확정 등급컷)는 보통 12월 초에 발표돼요. 발표 전까지는 이 계산기의 2026학년도 기준을 참고용으로 쓰세요."),
]

# ---------------------------------------------------------------- 비율 평균
AVG_BODY = r'''
<header class="top"><p class="kicker">학생 · 성적 · 가중 평균</p><h1><b>과목별 비율</b> 평균 계산기</h1>
<p class="lead">과목 수와 점수, 만점, 반영 비율(%)을 직접 정해서 평균을 구해요. 중간고사 40% · 기말고사 40% · 수행평가 20%처럼 비율이 다른 성적이나, 대학별 과목 반영 비율을 넣어 환산 점수를 볼 때 쓰세요. 막대를 움직이면 비율이 바로 바뀌어요.</p></header>
<section class="calc" id="a1">
<h2>점수와 반영 비율 입력</h2>
<div class="seg" role="group" aria-label="예시"><button type="button" class="pre" data-p="exam" aria-pressed="false">중간·기말·수행</button><button type="button" class="pre" data-p="subj" aria-pressed="false">국·수·영·탐 4과목</button><button type="button" class="pre" data-p="eq" aria-pressed="false">비율 모두 같게</button></div>
<div class="rh av"><span>과목·항목</span><span>점수</span><span>만점</span><span></span></div>
<div class="rows" id="rows"></div>
<button type="button" class="addr" id="add">+ 과목 추가</button>
<label class="fld" style="margin-top:10px"><span><input type="checkbox" id="norm" checked style="width:auto"> 비율 합계가 100%가 아니면 자동으로 100%에 맞춰 계산</span></label>
<div class="res">
 <div class="main"><div class="k">비율 반영 평균 (100점 환산)</div><div class="big" id="wa">-</div><div class="sub" id="was"></div></div>
 <div><div class="k">단순 평균 (100점 환산)</div><div class="big" id="sa">-</div><div class="sub" id="sas"></div></div>
 <div><div class="k">비율 합계</div><div class="big" id="ws">-</div><div class="sub" id="wss"></div></div>
</div>
<div class="scroll"><table class="tbl" id="bd"></table></div>
<p class="hint">비율 반영 평균 = Σ(점수 ÷ 만점 × 100 × 비율) ÷ Σ비율. 만점이 다른 항목(예: 수행평가 20점 만점)도 100점으로 바꿔 공정하게 더해요.</p>
</section>
<section class="card"><h2>이렇게 쓰세요</h2>
<ul><li><b>학교 시험:</b> 중간고사 35% · 기말고사 35% · 수행평가 30%처럼 학교에서 공지한 반영 비율을 넣으면 과목 최종 점수(원점수)를 미리 계산할 수 있어요.</li>
<li><b>대학 정시 환산:</b> 국어 30 · 수학 35 · 영어 15 · 탐구 20처럼 모집요강의 영역별 반영 비율과 백분위·표준점수를 넣으면 대학별 유불리를 비교할 수 있어요. 다만 대학마다 영어·한국사 가산점, 변환표준점수가 따로 있어 실제 환산 점수와는 차이가 나요.</li>
<li><b>목표 점수 역산:</b> 기말고사 칸 점수를 바꿔 보며 목표 평균에 몇 점이 필요한지 확인해 보세요.</li></ul></section>
'''
AVG_JS = r'''<script>
(function(){
const $=id=>document.getElementById(id);
const P={exam:[['중간고사',82,100,40],['기말고사',76,100,40],['수행평가',18,20,20]],subj:[['국어',88,100,30],['수학',92,100,35],['영어',95,100,15],['탐구',85,100,20]],};
function add(r){r=r||['',80,100,25];const d=document.createElement('div');d.className='row av';
 d.innerHTML='<input class="nm" placeholder="과목" value="'+r[0]+'" aria-label="과목명"><input class="sc" type="number" inputmode="decimal" value="'+r[1]+'" aria-label="점수"><input class="mx" type="number" inputmode="decimal" value="'+r[2]+'" aria-label="만점"><button type="button" class="x" aria-label="삭제">×</button>'+
 '<div class="w">반영 비율<input class="wr" type="range" min="0" max="100" step="1" value="'+r[3]+'" aria-label="반영 비율"><input class="wn" type="number" inputmode="decimal" min="0" value="'+r[3]+'" style="width:70px" aria-label="반영 비율 숫자"><output>%</output></div>';
 d.querySelector('.x').onclick=()=>{d.remove();calc()};d.querySelector('.wr').oninput=e=>{d.querySelector('.wn').value=e.target.value;calc()};d.querySelector('.wn').oninput=e=>{d.querySelector('.wr').value=e.target.value;calc()};$('rows').appendChild(d)}
const f1=x=>isFinite(x)?(Math.round(x*100)/100).toString():'-';
function calc(){const R=[...document.querySelectorAll('#rows .row')].map(d=>({n:d.querySelector('.nm').value||'항목',s:parseFloat(d.querySelector('.sc').value),m:parseFloat(d.querySelector('.mx').value),w:parseFloat(d.querySelector('.wn').value)||0})).filter(r=>isFinite(r.s)&&r.m>0);
 const W=R.reduce((a,r)=>a+r.w,0),norm=$('norm').checked;let tb='<tr><th>항목</th><th>100점 환산</th><th>비율</th><th>기여 점수</th></tr>';
 const wa=W?R.reduce((a,r)=>a+r.s/r.m*100*r.w,0)/(norm?W:100):NaN;
 R.forEach(r=>{tb+='<tr><td>'+r.n.replace(/[<>&]/g,'')+'</td><td>'+f1(r.s/r.m*100)+'</td><td>'+f1(norm&&W?r.w/W*100:r.w)+'%</td><td>'+f1(r.s/r.m*100*r.w/(norm?W:100))+'</td></tr>'});
 $('bd').innerHTML=tb;$('wa').textContent=f1(wa);$('was').textContent=R.length+'개 항목 · 비율 반영';
 const sa=R.length?R.reduce((a,r)=>a+r.s/r.m*100,0)/R.length:NaN;$('sa').textContent=f1(sa);$('sas').textContent='비율 무시, 모두 같은 비중';
 $('ws').textContent=f1(W)+'%';$('wss').textContent=Math.abs(W-100)<1e-9?'정확히 100%':(norm?'100%에 맞춰 계산 중':'입력한 비율 그대로 계산 (합계 '+f1(W)+'%)')}
document.querySelectorAll('.pre').forEach(b=>b.onclick=()=>{const p=b.dataset.p;if(p==='eq'){const ds=[...document.querySelectorAll('#rows .row')],v=ds.length?(100/ds.length).toFixed(2):0;ds.forEach(d=>{d.querySelector('.wn').value=v;d.querySelector('.wr').value=v})}else{$('rows').innerHTML='';P[p].forEach(add)}calc()});
$('add').onclick=()=>{add();calc()};$('a1').addEventListener('input',calc);$('a1').addEventListener('change',calc);
P.exam.forEach(add);calc();
})();
</script>'''
AVG_FAQ = [
 ("반영 비율이 다른 점수의 평균은 어떻게 구하나요?", "각 점수를 100점 만점으로 바꾼 뒤 반영 비율을 곱해 더하고, 비율 합계로 나눠요. 중간 82점(40%), 기말 76점(40%), 수행 18/20점(20%)이면 32.8 + 30.4 + 18 = 81.2점이에요."),
 ("비율 합계가 100%가 아니면 어떻게 되나요?", "자동 맞춤을 켜 두면 입력한 비율을 합계 기준으로 다시 나눠 100%로 맞춰 계산해요. 끄면 입력한 비율 그대로 곱한 점수를 보여 줘요."),
 ("만점이 다른 항목도 같이 계산할 수 있나요?", "네. 만점 칸에 20, 50처럼 그 항목의 만점을 넣으면 100점 기준으로 환산해서 합쳐요."),
]

# ---------------------------------------------------------------- hub
HUB_BODY = r'''
<header class="top"><p class="kicker">학생 · 중고등학생 · 수험생</p><h1><b>학생</b> 계산기</h1>
<p class="lead">내신 등급, 수능 표준점수·백분위, 과목별 비율 평균까지 2026년 최신 기준으로 계산해요. 2025년 고1부터 바뀐 5등급제와 2026학년도 수능 실채점 등급컷을 반영했어요.</p></header>
<section class="card"><h2>계산기</h2><div class="tiles">
<a class="tile" href="/student/naesin.html"><b>📘 내신 등급 계산기</b><span>5등급·9등급 · 학점 가중 평균 · 학년 비율 · 석차 → 등급</span></a>
<a class="tile" href="/student/suneung-score.html"><b>📝 수능 표준점수·백분위</b><span>2026학년도 등급컷 · 원점수 → 표준점수 · 영어·한국사</span></a>
<a class="tile" href="/student/average.html"><b>⚖️ 과목별 비율 평균</b><span>중간·기말·수행 비율 · 대학 반영 비율 · 만점 환산</span></a>
<a class="tile" href="/suneung.html"><b>⏱️ 수능 D-day 시간표</b><span>2027학년도 수능 11월 19일 · 교시별 타이머</span></a>
<a class="tile" href="/age-table.html"><b>🎂 나이표·학년</b><span>출생연도별 나이·띠·학년</span></a>
<a class="tile" href="/percent.html"><b>％ 퍼센트 계산기</b><span>몇 %, 증감률, 비율 나누기</span></a>
</div></section>
<section class="card"><h2>2026년 달라진 점</h2><ul>
<li><b>내신 5등급제:</b> 2025년 고1부터 1등급이 상위 4% → 10%로 넓어졌어요. 2026년 기준 고1·고2가 5등급제, 고3은 9등급제예요.</li>
<li><b>2026학년도 수능:</b> 국어 표준점수 최고점 147점, 수학 139점, 영어 1등급 3.11%로 국어·영어가 어려웠어요.</li>
<li><b>2027학년도 수능:</b> 2026년 11월 19일(목) 시행. 등급컷은 12월 채점 결과 발표 후 업데이트할게요.</li></ul></section>
'''

page("naesin.html", "내신 등급 계산기 2026 | 5등급제·9등급제 평균 등급, 석차 등급", "과목별 학점과 등급으로 내신 평균 등급을 계산해요. 2025 고1부터 적용된 5등급제와 9등급제, 학년별 반영 비율, 반영 교과 선택, 석차로 등급 구하기까지.", NAESIN_BODY + NAESIN_JS, NAESIN_FAQ, "내신 등급 계산기", og="student-naesin")
page("suneung-score.html", "수능 표준점수 백분위 등급 계산기 | 2026학년도 실채점 등급컷", "표준점수로 수능 등급과 백분위를 확인하고, 원점수·평균·표준편차로 표준점수를 계산해요. 2026학년도 수능 국어 133·수학 128 1등급 컷 등 평가원 채점 결과 기준.", SUN_BODY + SUN_JS.replace("__DATA__", json.dumps(SUN_DATA, ensure_ascii=False)), SUN_FAQ, "수능 표준점수·백분위 계산기", og="student-suneung")
page("average.html", "과목별 비율 평균 계산기 | 반영 비율(%) 가중 평균, 수행평가 환산", "과목 수와 점수, 만점, 반영 비율(%)을 직접 조절해 가중 평균을 계산해요. 중간·기말·수행평가 비율, 대학 영역별 반영 비율 환산에 사용하세요.", AVG_BODY + AVG_JS, AVG_FAQ, "과목별 비율 평균 계산기", og="student-average")
page("index.html", "학생 계산기 | 내신 등급·수능 표준점수·백분위·비율 평균", "내신 등급(5등급·9등급), 수능 표준점수·백분위·등급, 과목별 비율 평균 계산기를 2026년 최신 기준으로 모았어요.", HUB_BODY, None, "학생 계산기", og="student")
print("ok")
