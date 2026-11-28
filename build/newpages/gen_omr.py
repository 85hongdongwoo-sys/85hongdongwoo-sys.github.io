#!/usr/bin/env python3
"""OMR 답안카드 + 시험 타이머 + 자동 채점 도구 (/ipsi/omr.html). 2026-11-28.
기출 PDF를 보며 시간 맞춰 풀고 OMR 마킹 → 정답 입력 → 채점. 범용. 실행:
    python3 build/newpages/gen_omr.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

TOOL = ("""<section class="card tool" id="tool"><style>
#tool h2{margin:22px 0 10px}#tool h2:first-of-type{margin-top:0}
#omr-set{display:flex;flex-wrap:wrap;gap:12px;align-items:end}
#omr-set .f{margin:0;max-width:130px}
#omr-set input,#omr-set select{text-align:center}
/* 타이머 바: 스크롤해도 화면 위에 계속 붙어 보임 */
#omr-timebar{display:none;align-items:center;gap:10px;flex-wrap:wrap;position:sticky;top:0;z-index:30;background:#fff;padding:8px 2px;border-bottom:1px solid #EEF0F3;margin:6px 0}
#omr-clock{font-size:30px;font-weight:800;font-variant-numeric:tabular-nums;color:#111;min-width:108px}
#omr-clock.warn{color:#C0392B}
#omr-clock.done{color:#13743A}
#omr-timebar .btn{padding:6px 12px;font-size:14px}
#omr-float{margin-left:auto}
#omr-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:3px 16px;margin:6px 0}
.omr-row{display:flex;align-items:center;gap:7px;padding:3px 0;border-bottom:1px solid #F0F1F3}
.omr-row .qn{flex:none;width:30px;text-align:right;font-weight:700;color:#5B6B82;font-size:14px}
.omr-b{flex:none;width:26px;height:26px;border:1.6px solid #C7CDD6;border-radius:50%;background:#fff;color:#8A94A6;font-size:12.5px;font-weight:700;cursor:pointer;display:grid;place-items:center;padding:0;font-family:inherit}
.omr-b.on{background:#1F2937;border-color:#1F2937;color:#fff}
.omr-row.correct .qn{color:#13743A}.omr-row.wrong .qn{color:#C0392B}
.omr-b.ans{box-shadow:0 0 0 2px #2BA85A inset;border-color:#2BA85A}
.omr-b.miss{background:#FDECEC;border-color:#D64545;color:#8A1C1C}
#omr-key{width:100%;box-sizing:border-box;min-height:58px;font-size:15px;line-height:1.7;font-family:inherit;padding:10px 12px;border:1px solid #D9DDE3;border-radius:12px;resize:vertical}
#omr-res{display:none;margin-top:12px}
.omr-score{font-size:34px;font-weight:800;color:#1D4ED8}.omr-score small{font-size:16px;color:#5B6B82;font-weight:600}
/* 옆에 띄우기(팝업) 모드: 문제 PDF 창 옆에 둘 수 있는 떠 있는 패널 */
.omr-head{display:none}
#omr-panel.float{position:fixed;top:14px;right:14px;width:min(360px,94vw);max-height:92vh;overflow:auto;background:#fff;border:1px solid #D9DDE3;border-radius:16px;box-shadow:0 20px 56px rgba(17,24,39,.24);z-index:9999;padding:12px 15px;resize:both}
#omr-panel.float .omr-head{display:flex;align-items:center;gap:8px;position:sticky;top:0;z-index:40;background:#fff;padding:2px 0 8px;margin-bottom:4px;border-bottom:1px solid #EEF0F3;cursor:move;touch-action:none}
#omr-panel.float .omr-head b{font-size:14px;color:#111}
#omr-panel.float .omr-head .dock{margin-left:auto;padding:5px 11px;font-size:13px}
#omr-panel.float #omr-grid{grid-template-columns:1fr 1fr}
#omr-panel.float #omr-timebar{top:34px}
#omr-panel.float h2,#omr-panel.float .note{font-size:14px}
@media(max-width:560px){#omr-panel.float{left:8px;right:8px;width:auto;resize:none}}
/* 좌측 문제지(PDF) + 우측 OMR 분할 뷰 */
.omr-pdfbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:4px 0 10px;padding:10px 12px;background:#F6F8FB;border:1px solid #E6EAF0;border-radius:12px}
.omr-pdfbar .note{margin:0}
.omr-split{display:flex;gap:16px;align-items:flex-start}
.omr-pdf{flex:1 1 56%;min-width:0;position:sticky;top:8px}
.omr-canvas{height:82vh;overflow:auto;border:1px solid #D9DDE3;border-radius:12px;background:#53585F;padding:10px;text-align:center}
.omr-canvas canvas{max-width:100%;margin:0 auto 10px;border-radius:4px;box-shadow:0 2px 10px rgba(0,0,0,.25)}
.omr-canvas .omr-loading{color:#fff;padding:40px 0;font-size:14px}
.omr-pdf iframe{width:100%;height:82vh;border:1px solid #D9DDE3;border-radius:12px;background:#fff;display:block}
.omr-split.has-pdf #omr-panel{flex:1 1 44%;min-width:300px}
#omr-name{font-weight:800;color:#1D4ED8}
@media(max-width:820px){.omr-split{flex-direction:column}.omr-pdf{position:static;width:100%}.omr-canvas,.omr-pdf iframe{height:64vh}}
</style>
<h2 style="margin-top:0">시험 설정</h2>
<div id="omr-set">
<div class="f"><label for="omr-n">문항 수</label><input id="omr-n" type="number" inputmode="numeric" min="1" max="200" value="20"></div>
<div class="f"><label for="omr-c">선택지</label><select id="omr-c"><option value="4" selected>4지선다 ①~④</option><option value="5">5지선다 ①~⑤</option></select></div>
<div class="f"><label for="omr-t">제한 시간(분)</label><input id="omr-t" type="number" inputmode="numeric" min="0" max="600" value="25"></div>
<button class="btn dl" id="omr-start" style="height:44px">시험 시작 ▶</button>
</div>
<div class="omr-pdfbar"><b>문제지</b><label class="btn" for="omr-file">📄 PDF 열기</label><input id="omr-file" type="file" accept="application/pdf" hidden><a class="btn" id="omr-newtab" target="_blank" rel="noopener" hidden>새 탭에서 열기</a><span class="note" id="omr-pdfhint">기출 PDF를 열면 <b>왼쪽에 문제지</b>, <b>오른쪽에 OMR</b>이 같이 떠요. (문제 창이 안 열리면 ‘새 탭에서 열기’)</span></div>
<div class="omr-split" id="omr-split">
<div class="omr-pdf" id="omr-pdfwrap" hidden><div id="omr-canvas" class="omr-canvas"></div><iframe id="omr-frame" title="문제지 PDF" hidden></iframe></div>
<div id="omr-panel">
<div class="omr-head"><b>⏱ 답안카드</b><button class="btn dock" id="omr-dock">본문에 넣기</button></div>
<div id="omr-timebar"><div id="omr-clock">00:00</div><button class="btn" id="omr-pause">일시정지</button><button class="btn" id="omr-reset">초기화</button><button class="btn" id="omr-float">⧉ 옆에 띄우기</button></div>
<h2>답안카드 (OMR)</h2>
<p class="note">기출 PDF를 보며 문제를 풀고, 아래에서 번호를 눌러 마킹하세요. 시간이 끝나면 <b>자동으로 채점</b>돼요. ‘옆에 띄우기’를 누르면 PDF 창 옆에 띄워 놓고 풀 수 있어요.</p>
<div id="omr-grid"></div>
<h2>정답 입력 후 채점</h2>
<p class="note">정답을 순서대로 입력하세요. 숫자만 붙여 써도 되고(예: <b>31242</b>) 띄어쓰기·줄바꿈·쉼표로 구분해도 돼요. 기출 PDF 뒤쪽 정답표를 보고 넣으면 돼요.</p>
<textarea id="omr-key" placeholder="예: 3 1 2 4 2 ... (문항 수만큼)"></textarea>
<div class="btns"><button class="btn dl" id="omr-grade">채점하기</button></div>
<div id="omr-res"></div>
</div>
</div>
</section>""", """<script>
(function(){var $=HL.$;
var N=20,C=4,timeLeft=0,timer=null,running=false;var CH=['①','②','③','④','⑤'];
var ans=[];
function buildGrid(){N=Math.max(1,Math.min(200,parseInt($('#omr-n').value,10)||20));C=parseInt($('#omr-c').value,10)||4;
 if(ans.length!==N)ans=new Array(N).fill(0);
 var h='';for(var i=1;i<=N;i++){h+='<div class="omr-row" id="orow'+i+'"><span class="qn">'+i+'</span>';
  for(var c=1;c<=C;c++)h+='<button class="omr-b'+(ans[i-1]===c?' on':'')+'" data-q="'+i+'" data-c="'+c+'">'+CH[c-1]+'</button>';
  h+='</div>';}
 $('#omr-grid').innerHTML=h;
 $('#omr-grid').querySelectorAll('.omr-b').forEach(function(b){b.addEventListener('click',mark);});}
function mark(e){var q=+e.currentTarget.getAttribute('data-q'),c=+e.currentTarget.getAttribute('data-c');
 ans[q-1]=(ans[q-1]===c)?0:c;
 var row=$('#orow'+q);row.querySelectorAll('.omr-b').forEach(function(b){b.classList.toggle('on',+b.getAttribute('data-c')===ans[q-1]);});}
function fmt(s){var m=Math.floor(s/60),x=s%60;return (m<10?'0':'')+m+':'+(x<10?'0':'')+x;}
function tick(){if(timeLeft<=0){stop();$('#omr-clock').classList.add('done');$('#omr-clock').textContent='종료';grade();return;}timeLeft--;$('#omr-clock').textContent=fmt(timeLeft);$('#omr-clock').classList.toggle('warn',timeLeft<=60);}
function start(){buildGrid();var mins=parseInt($('#omr-t').value,10)||0;
 $('#omr-clock').classList.remove('done');$('#omr-timebar').style.display='flex';
 if(mins>0){timeLeft=mins*60;$('#omr-clock').textContent=fmt(timeLeft);
  running=true;$('#omr-pause').textContent='일시정지';$('#omr-pause').style.display='';clearInterval(timer);timer=setInterval(tick,1000);}
 else{$('#omr-clock').textContent='시간 제한 없음';$('#omr-clock').style.fontSize='18px';$('#omr-pause').style.display='none';}
 $('#omr-start').textContent='다시 시작 ▶';
 var g=$('#omr-grid');if(g)window.scrollTo({top:g.getBoundingClientRect().top+window.scrollY-70,behavior:'smooth'});}
function stop(){running=false;clearInterval(timer);}
function parseKey(){var toks=$('#omr-key').value.trim().split(/[^0-9]+/).filter(Boolean);var key;
 if(toks.length===N)key=toks.map(Number);
 else{var digits=$('#omr-key').value.replace(/[^0-9]/g,'');key=digits.split('').map(Number);}
 return key;}
function grade(){var key=parseKey();
 if(key.length<N){alert('정답 '+N+'개가 필요해요. 지금 '+key.length+'개 입력됐어요. (기출 PDF 뒤쪽 정답표를 순서대로 넣어주세요)');return;}
 var right=0,blank=0;
 for(var i=1;i<=N;i++){var row=$('#orow'+i);row.classList.remove('correct','wrong');
  row.querySelectorAll('.omr-b').forEach(function(b){b.classList.remove('ans','miss');});
  var my=ans[i-1],co=key[i-1];
  row.querySelectorAll('.omr-b').forEach(function(b){var bc=+b.getAttribute('data-c');if(bc===co)b.classList.add('ans');});
  if(my===0)blank++;
  if(my===co){right++;row.classList.add('correct');}
  else{row.classList.add('wrong');if(my>0)row.querySelector('.omr-b[data-c="'+my+'"]').classList.add('miss');}}
 var pct=Math.round(right/N*1000)/10;
 var wrongList=[];for(var j=1;j<=N;j++)if(ans[j-1]!==key[j-1])wrongList.push(j);
 var el=$('#omr-res');el.style.display='block';
 el.innerHTML='<div class="tiles hk-tiles"><div class="tile"><div class="k">맞은 개수</div><div class="omr-score">'+right+'<small> / '+N+'</small></div></div>'
  +'<div class="tile light"><div class="k">정답률</div><div class="v">'+pct+'%</div></div>'
  +'<div class="tile"><div class="k">빈칸</div><div class="v">'+blank+'개</div></div></div>'
  +'<p class="note">초록 테두리가 정답, 빨간 칸이 내가 고른 오답이에요.'+(wrongList.length?' <b>틀린 문항</b>: '+wrongList.join(', '):' 전부 정답이에요! 🎉')+'</p>';
 stop();el.scrollIntoView({behavior:'smooth',block:'nearest'});}
$('#omr-n').addEventListener('change',buildGrid);$('#omr-c').addEventListener('change',buildGrid);
$('#omr-start').addEventListener('click',start);
$('#omr-grade').addEventListener('click',grade);
$('#omr-pause').addEventListener('click',function(){if(timeLeft<=0)return;if(running){stop();this.textContent='이어서';}else{running=true;this.textContent='일시정지';clearInterval(timer);timer=setInterval(tick,1000);}});
$('#omr-reset').addEventListener('click',function(){stop();ans=new Array(N).fill(0);$('#omr-res').style.display='none';buildGrid();$('#omr-timebar').style.display='none';$('#omr-start').textContent='시험 시작 ▶';});
// 옆에 띄우기(팝업) 토글
var panel=$('#omr-panel');
function setFloat(on){panel.classList.toggle('float',on);$('#omr-float').textContent=on?'⧉ 띄움':'⧉ 옆에 띄우기';if(!on){panel.style.left='';panel.style.top='';panel.style.right='';}}
$('#omr-float').addEventListener('click',function(){setFloat(!panel.classList.contains('float'));});
$('#omr-dock').addEventListener('click',function(){setFloat(false);window.scrollTo({top:panel.getBoundingClientRect().top+window.scrollY-70,behavior:'smooth'});});
// 떠 있는 패널 드래그(헤더 잡고 이동)
(function(){var head=panel.querySelector('.omr-head'),dx=0,dy=0,drag=false;
 head.addEventListener('pointerdown',function(e){if(e.target.closest('button'))return;if(!panel.classList.contains('float'))return;
  drag=true;var r=panel.getBoundingClientRect();panel.style.right='auto';panel.style.left=r.left+'px';panel.style.top=r.top+'px';
  dx=e.clientX-r.left;dy=e.clientY-r.top;head.setPointerCapture(e.pointerId);e.preventDefault();});
 head.addEventListener('pointermove',function(e){if(!drag)return;
  var x=Math.max(0,Math.min(window.innerWidth-60,e.clientX-dx)),y=Math.max(0,Math.min(window.innerHeight-40,e.clientY-dy));
  panel.style.left=x+'px';panel.style.top=y+'px';});
 head.addEventListener('pointerup',function(e){drag=false;try{head.releasePointerCapture(e.pointerId);}catch(_){}});
})();
// URL 설정값 자동 적용 + 문제지 PDF 열기
function qp(k){try{return new URLSearchParams(location.search).get(k);}catch(e){return null;}}
var _vn=qp('n'),_vc=qp('c'),_vt=qp('t'),_vkey=qp('key'),_vname=qp('name');
if(_vn)$('#omr-n').value=Math.max(1,Math.min(200,parseInt(_vn,10)||20));
if(_vc==='4'||_vc==='5')$('#omr-c').value=_vc;
if(_vt!==null&&_vt!=='')$('#omr-t').value=Math.max(0,Math.min(600,parseInt(_vt,10)||0));
if(_vkey)$('#omr-key').value=_vkey.replace(/[^0-9 ,\\n]/g,'');
if(_vname){var _h=document.querySelector('.lead')||document.querySelector('h1');if(_h&&_h.parentNode){var _s=document.createElement('p');_s.innerHTML='지금 푸는 시험: <span id="omr-name"></span>';_s.querySelector('#omr-name').textContent=_vname;_h.parentNode.insertBefore(_s,_h.nextSibling);}}
// PDF.js 내장 뷰어 — 받은 PDF를 페이지 안에 직접 렌더(기기·브라우저 무관)
var PJS='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/';var _pjs=null;
function loadPjs(){if(_pjs)return _pjs;_pjs=new Promise(function(res,rej){var s=document.createElement('script');s.src=PJS+'pdf.min.js';s.onload=function(){try{window.pdfjsLib.GlobalWorkerOptions.workerSrc=PJS+'pdf.worker.min.js';}catch(e){}res(window.pdfjsLib);};s.onerror=rej;document.head.appendChild(s);});return _pjs;}
function openWrap(){$('#omr-pdfwrap').hidden=false;$('#omr-split').classList.add('has-pdf');}
function iframeFallback(url){var f=$('#omr-frame');$('#omr-canvas').hidden=true;if(url){f.src=url;f.hidden=false;}$('#omr-pdfhint').textContent='문제 창이 비면 ‘새 탭에서 열기’로 보면서 OMR로 푸세요.';}
function renderPdf(src,fallbackUrl){openWrap();var wrap=$('#omr-canvas');wrap.hidden=false;$('#omr-frame').hidden=true;wrap.innerHTML='<div class="omr-loading">문제지 불러오는 중…</div>';
 loadPjs().then(function(lib){return lib.getDocument(src).promise;}).then(function(pdf){wrap.innerHTML='';var chain=Promise.resolve();
  for(var i=1;i<=pdf.numPages;i++){(function(p){chain=chain.then(function(){return pdf.getPage(p).then(function(page){
    var w=(wrap.clientWidth-20)||600;var vp=page.getViewport({scale:1});var sc=Math.min(2,w/vp.width);var v2=page.getViewport({scale:sc});
    var c=document.createElement('canvas');var dpr=Math.min(2,window.devicePixelRatio||1);c.width=v2.width*dpr;c.height=v2.height*dpr;c.style.width='100%';
    wrap.appendChild(c);var ctx=c.getContext('2d');ctx.scale(dpr,dpr);return page.render({canvasContext:ctx,viewport:v2}).promise;});});})(i);}
  return chain;}).catch(function(){iframeFallback(fallbackUrl);});}
function showPdf(url){if(!url)return;var nt=$('#omr-newtab');nt.href=url;nt.hidden=false;renderPdf(url,url);}
var _vpdf=qp('pdf');if(_vpdf)showPdf(_vpdf);
$('#omr-file').addEventListener('change',function(e){var f=e.target.files&&e.target.files[0];if(!f)return;$('#omr-newtab').hidden=true;
  var fr=new FileReader();fr.onload=function(){renderPdf({data:fr.result},null);};fr.readAsArrayBuffer(f);});
buildGrid();
})();
</script>""")

P = dict(slug='omr', url='/ipsi/omr.html', sec=('시험·공부', '/ipsi/'), crumb3=' › OMR 모의고사 채점', nosafe=True, warn='',
  name='OMR 답안카드·시험 타이머·자동 채점 — 기출 풀고 몇 점인지 채점 (무료)',
  h1='OMR <b>모의고사 채점기</b>',
  lead='기출문제를 실제 시험처럼 시간 맞춰 풀고, OMR 답안카드에 마킹한 뒤, 정답을 입력하면 몇 점인지·틀린 문항까지 바로 채점해 줘요. 어떤 시험에도 쓸 수 있어요.',
  desc='문항 수·선택지·제한 시간을 정하고 OMR 답안카드에 마킹해요. 기출 PDF를 보며 시간 맞춰 풀고 정답을 입력하면 점수·정답률·틀린 문항을 자동 채점해요. 한국사·공무원·검정고시 등 모든 기출에 사용할 수 있는 무료 도구예요.',
  tool=TOOL, rel=('<section class="card rel"><h2>이 도구로 풀기 좋은 기출</h2><ul>'
    '<li><a href="/ipsi/hanneung.html"><b>한국사능력검정 기출</b><span>회차별 문제 받아서 OMR로 풀기</span></a></li>'
    '<li><a href="/ipsi/gong9.html"><b>공무원 9급 기출</b><span>100문항 100분 실전처럼</span></a></li>'
    '<li><a href="/ipsi/gumjeong.html"><b>검정고시 기출</b></a></li>'
    '<li><a href="/ipsi/toeic-part5.html"><b>토익 Part5 연습 10문항</b></a></li></ul></section>'),
  body=[
    ('어떻게 쓰나요', '<ol><li><b>시험 설정</b> — 문항 수, 선택지(4·5지선다), 제한 시간을 정해요. 예: 한국사능력검정 50문항 80분, 공무원 9급 한 과목 20문항 20분.</li>'
     '<li><b>시험 시작</b>을 누르면 타이머가 돌아요. 기출 PDF를 다른 창(또는 종이)으로 보면서 문제를 풀어요.</li>'
     '<li><b>OMR 마킹</b> — 답을 번호판에서 눌러 마킹해요. 다시 누르면 지워져요.</li>'
     '<li>시간이 끝나면 <b>자동 채점</b>돼요. 끝나기 전에 다 풀었으면 정답을 넣고 ‘채점하기’를 눌러요.</li>'
     '<li><b>정답 입력</b> — 기출 PDF 뒤쪽 정답표를 보고 순서대로 넣어요(숫자만 붙여 써도 됨).</li></ol>'),
    ('실전처럼 푸는 게 왜 중요한가요', '<p>기출은 그냥 눈으로 보는 것과, <b>시간을 재고 OMR에 마킹하며 푸는 것</b>이 완전히 달라요. 실제 시험은 시간 압박과 마킹 실수가 점수를 크게 좌우해요.</p>'
     '<ul><li>제한 시간을 걸면 ‘한 문제에 몇 초’ 감각이 생겨요.</li><li>OMR 마킹을 연습하면 밀려 쓰는 실수를 줄여요.</li><li>채점 후 틀린 문항만 다시 보면 복습이 빨라져요.</li></ul>'),
    ('정답 입력은 어떻게 하나요', '<p>정답을 <b>순서대로</b> 넣으면 돼요. 세 가지 방식 다 인식해요.</p>'
     '<ul><li>숫자만 붙여서: <b>31242…</b> (한 자리가 한 문항)</li><li>띄어쓰기: <b>3 1 2 4 2 …</b></li><li>줄바꿈·쉼표도 OK</li></ul>'
     '<p>5지선다는 정답이 5(⑤)까지 나올 수 있어요. 입력한 정답 개수가 문항 수와 맞아야 채점돼요.</p>'),
    ('어떤 시험에 쓸 수 있나요', '<p>선택형(객관식) 시험이면 뭐든 가능해요. 한국사능력검정, 공무원 9급·7급, 검정고시, 토익, 각종 자격증 필기, 모의고사까지요. 문항 수와 선택지만 맞춰 설정하면 돼요.</p>'
     '<p>기출 PDF는 <a href="/ipsi/">입시·시험 자료실</a>에서 공식 출처로 받을 수 있어요.</p>'),
  ],
  faq=[('OMR 채점기는 무료인가요?', '네, 완전 무료예요. 가입도 필요 없어요. 문항 수·시간만 정하고 바로 쓰면 돼요.'),
       ('정답은 어디서 구하나요?', '기출문제 PDF 뒤쪽 정답표에 있어요. 그걸 보고 순서대로 입력하면 자동으로 채점돼요.'),
       ('5지선다도 되나요?', '네. 선택지를 5지선다로 바꾸면 ①~⑤까지 마킹과 채점이 돼요.'),
       ('시간이 끝나면 어떻게 되나요?', '제한 시간이 0이 되면 자동으로 채점돼요. 정답을 미리 입력해 두면 바로 점수가 나와요.'),
       ('몇 문항까지 되나요?', '1~200문항까지 설정할 수 있어서 공무원 100문항 같은 큰 시험도 한 번에 풀 수 있어요.')],
  src='<li>도구: 홍라이프 도구 자체 제작 OMR 채점기 (2026-11-28)</li>')

if __name__ == '__main__':
    print('wrote', G.page(P))
