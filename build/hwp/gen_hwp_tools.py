#!/usr/bin/env python3
"""한글(HWP) 도구 페이지 만들기 — build/hwp/template.html(HWP→PDF 페이지)의 틀을 빌려 overlay/pdf/*.html 을 써요.
로컬에서 한 번 돌리고 결과(overlay)를 커밋해요:  python3 build/hwp/gen_hwp_tools.py"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TPL = open(os.path.join(ROOT, 'build/hwp/template.html'), encoding='utf-8').read()
OUT = os.path.join(ROOT, 'overlay/pdf')
SITE = 'https://honglife.co.kr'
KIT = '<script src="/assets/js/hlhwpkit.js?v=4"></script>'
DATE = '2026-11-24'

SAFE = ('<div class="safe"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2.5"/>'
        '<path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>파일은 서버로 전송되지 않고 내 기기에서만 처리돼요</div>')

HWP_TOOLS = [
    ('/pdf/hwp-viewer.html', 'HWP 뷰어 (한글 파일 열기)', '한컴오피스 없이 HWP·HWPX 보기, 글자 복사·인쇄'),
    ('/pdf/hwp-to-pdf.html', 'HWP를 PDF로 변환', '여러 개 한 번에, 검색·복사 되는 PDF'),
    ('/pdf/hwp-to-hwpx.html', 'HWP를 HWPX로 변환', '옛 한글 파일을 새 형식으로, 여러 개 ZIP'),
    ('/pdf/hwpx-to-hwp.html', 'HWPX를 HWP로 변환', '옛 버전 한글에서도 열리게'),
    ('/pdf/hwp-to-txt.html', 'HWP 텍스트 추출', '글자만 TXT로, 글자 수·원고지 매수'),
    ('/pdf/text-to-hwp.html', '텍스트·워드를 한글 파일로', 'TXT·DOCX → HWP·HWPX 만들기'),
    ('/doc/gongmun-checker.html', '공문서 오류 검사기', 'HWP 공문 맞춤법·서식 점검'),
]

FILE_TOOL_CSS = '<style>.hk-out{white-space:pre-wrap;word-break:break-all;overflow-wrap:anywhere;max-height:420px;overflow:auto;background:#F7F8FA;border:1px solid #E3E6EB;border-radius:12px;padding:12px 14px;font-size:15px;line-height:1.7;margin-top:10px}.hk-tiles{margin-top:10px}#tool textarea{width:100%;box-sizing:border-box}</style>'


def conv_tool(src, dst):
    """HWP↔HWPX 여러 파일 변환 도구 (같은 틀)."""
    S, D = src.upper(), dst.upper()
    return f'''<section class="card tool" id="tool">
<div class="drop" id="drop"><b>{S} 파일을 놓거나 눌러서 고르세요</b><span>.{src} · 여러 개 → 파일마다 .{dst}</span></div>
<ul class="files" id="list"></ul>
<div id="opt" hidden>
<div class="btns"><button class="btn dl" id="go" type="button" disabled>{D}로 변환</button></div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
<h3 id="pvh" hidden>미리보기 (첫 쪽)</h3><div class="preview" id="pv" hidden></div>
</div>
</section>''', f'''<script>
(function(){{var $=HL.$;var items=[],running=false;var TO='{dst}';
function draw(){{var ul=$('#list');ul.innerHTML='';items.forEach(function(it,i){{var li=HL.el('li');li.appendChild(HL.el('span',{{'class':'nm',text:(i+1)+'. '+it.name}}));li.appendChild(HL.el('span',{{'class':'sz',text:(it.h&&it.h.n?it.h.n+'쪽 · ':'')+HL.bytes(it.size)}}));li.appendChild(HL.el('span',{{'class':'stt'+(it.out?' ok':it.err?' bad':''),text:it.err||it.state||''}}));
 if(it.out){{var b=HL.el('button',{{type:'button',text:'받기'}});b.onclick=function(){{HL.download(new Blob([it.out],{{type:HLK.mime[TO]}}),HL.baseName(it.name)+'.'+TO)}};li.appendChild(b)}}
 if(!running){{var x=HL.el('button',{{type:'button',text:'빼기'}});x.onclick=function(){{if(it.h&&it.h.free)it.h.free();items.splice(i,1);draw()}};li.appendChild(x)}}ul.appendChild(li)}});
 $('#opt').hidden=!items.length;$('#go').disabled=running||!items.some(function(it){{return it.h&&it.h.doc}})}}
async function add(fs){{var first=null;for(var f of fs){{var it={{name:f.name,size:f.size,state:'여는 중…'}};items.push(it);draw();
 try{{if(!/\\.{src}$/i.test(f.name))throw new Error('.{src} 파일이 아니에요');it.h=await HLHWP.open(f,function(a,b){{$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%';$('#st').textContent='문서 엔진 받는 중… (처음 한 번만)'}});
  if(!it.h.doc)it.err='문서 엔진으로 읽지 못해 바꿀 수 없어요';else{{it.state='준비됨';first=first||it}}}}catch(e){{it.err=e.message}}$('#pb').hidden=true;$('#st').textContent='';draw()}}
 if(first){{$('#pv').innerHTML=first.h.svg(0);$('#pv').hidden=$('#pvh').hidden=false;$('#pvh').textContent='미리보기 — '+first.name}}}}
HL.dropzone($('#drop'),{{multiple:true,accept:'.{src}',onFiles:add}});
$('#go').onclick=HL.run($('#go'),async function(){{running=true;draw();var ok=[];try{{for(var it of items){{if(!it.h||!it.h.doc)continue;it.state='변환 중';draw();await new Promise(function(r){{setTimeout(r,0)}});
  try{{it.out=HLK.save(it.h,TO);it.state='완료 · '+HL.bytes(it.out.length);ok.push(it)}}catch(e){{it.err=e.message}}draw()}}}}finally{{running=false;draw()}}
 $('#st').textContent=ok.length+'개 파일을 .'+TO+'로 바꿨어요.';if(!ok.length)return;
 if(ok.length===1){{HL.download(new Blob([ok[0].out],{{type:HLK.mime[TO]}}),HL.baseName(ok[0].name)+'.'+TO);return}}
 await HL.need('jszip');var z=new JSZip(),used={{}};ok.forEach(function(it){{var n=HL.baseName(it.name)+'.'+TO;while(used[n])n=n.replace(/(\\.\\w+)$/,'_1$1');used[n]=1;z.file(n,it.out)}});
 HL.download(await z.generateAsync({{type:'blob'}}),'한글문서_'+TO.toUpperCase()+'_'+HL.stamp()+'.zip')}},'변환 중…');
}})();
</script>'''


TXT_TOOL = ('''<section class="card tool" id="tool">
<div class="drop" id="drop"><b>HWP·HWPX 파일을 놓거나 눌러서 고르세요</b><span>.hwp · .hwpx · 여러 개면 글을 이어 붙여요</span></div>
<ul class="files" id="list"></ul>
<div id="opt" hidden>
<div class="tiles hk-tiles">
 <div class="tile"><div class="k">공백 포함</div><div class="v" id="cAll">0</div></div>
 <div class="tile"><div class="k">공백 제외</div><div class="v" id="cNo">0</div></div>
 <div class="tile light"><div class="k">200자 원고지</div><div class="v" id="cMs">0</div></div>
 <div class="tile light"><div class="k">단어 / 문단</div><div class="v" id="cWp">0</div></div>
</div>
<label class="chk" style="margin:10px 0 0"><input type="checkbox" id="pg"> 쪽마다 구분선(— 2쪽 —) 넣기</label>
<label class="chk" style="margin:4px 0 0"><input type="checkbox" id="sq" checked> 빈 줄 여러 개는 한 줄로</label>
<div class="hk-out" id="out" tabindex="0" aria-label="뽑은 글"></div>
<div class="btns"><button class="btn dl" id="dl" type="button">TXT로 받기</button><button class="btn" id="cp" type="button">글 복사</button></div>
<p class="note" id="st" aria-live="polite"></p>
</div>
<div class="prog" id="pb" hidden><i></i></div>
</section>''', '''<script>
(function(){var $=HL.$;var items=[];
function body(){var pg=$('#pg').checked,sq=$('#sq').checked;var parts=items.filter(function(it){return it.h}).map(function(it){var h=it.h,t;
  if(h.fallback)t=h.fallback.map(function(p){return p.t}).join('\\n');else{var a=[];for(var i=0;i<h.n;i++){var s=HLK.pt(h,i).replace(/\\n+$/,'');a.push(pg&&i?'\\n— '+(i+1)+'쪽 —\\n'+s:s)}t=a.join('\\n')}
  if(sq)t=t.replace(/\\n[ \\t]*\\n(\\s*\\n)+/g,'\\n\\n');return (items.length>1?'['+it.name+']\\n':'')+t.trim()});return parts.join('\\n\\n')}
function show(){var t=body();$('#out').textContent=t||'(글자가 없어요)';var s=HLK.stats(t);$('#cAll').textContent=HLK.fmtN(s.all);$('#cNo').textContent=HLK.fmtN(s.no);$('#cMs').textContent=HLK.fmtN(s.ms200)+'장';$('#cWp').textContent=HLK.fmtN(s.words)+' / '+HLK.fmtN(s.paras);$('#opt').hidden=!items.some(function(it){return it.h})}
function draw(){var ul=$('#list');ul.innerHTML='';items.forEach(function(it,i){var li=HL.el('li');li.appendChild(HL.el('span',{'class':'nm',text:(i+1)+'. '+it.name}));li.appendChild(HL.el('span',{'class':'sz',text:(it.h&&it.h.n?it.h.n+'쪽 · ':'')+HL.bytes(it.size)}));li.appendChild(HL.el('span',{'class':'stt'+(it.h?' ok':it.err?' bad':''),text:it.err||it.state||''}));var x=HL.el('button',{type:'button',text:'빼기'});x.onclick=function(){if(it.h&&it.h.free)it.h.free();items.splice(i,1);draw();show()};li.appendChild(x);ul.appendChild(li)})}
async function add(fs){for(var f of fs){var it={name:f.name,size:f.size,state:'여는 중…'};items.push(it);draw();try{it.h=await HLHWP.open(f,function(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%'});it.state=it.h.fallback?'글자만 읽음':'읽음'}catch(e){it.err=e.message}$('#pb').hidden=true;draw()}show()}
HL.dropzone($('#drop'),{multiple:true,accept:'.hwp,.hwpx',onFiles:add});['#pg','#sq'].forEach(function(x){$(x).onchange=show});
$('#dl').onclick=function(){var n=items.length===1?HL.baseName(items[0].name):'한글문서_글자_'+HL.stamp();HL.download(new Blob(['\\ufeff'+body().replace(/\\n/g,'\\r\\n')],{type:HLK.mime.txt}),n+'.txt')};
$('#cp').onclick=function(){HL.copy?HL.copy(body()):navigator.clipboard.writeText(body());$('#st').textContent='복사했어요.'};
})();
</script>''')


MAKE_TOOL = ('''<section class="card tool" id="tool">
<div class="drop" id="drop"><b>TXT·워드(DOCX) 파일을 놓거나, 아래에 글을 붙여 넣으세요</b><span>.txt · .md · .docx · .csv</span></div>
<div class="f" style="margin-top:12px"><label for="txt">한글 문서에 넣을 글 <span class="note">— 줄을 바꾼 곳이 문단이 돼요</span></label>
<textarea id="txt" rows="12" placeholder="예) 2026년 송년회 안내&#10;&#10;일시: 12월 19일(금) 오후 6시&#10;장소: 본관 2층 회의실"></textarea></div>
<div class="grid g2" style="margin-top:8px"><div class="f"><label for="fmt">저장 형식</label><select id="fmt"><option value="hwp" selected>HWP (기본)</option><option value="hwpx">HWPX (새 형식)</option></select></div>
<div class="f"><label for="nm">파일 이름</label><input id="nm" placeholder="비우면 첫 줄" maxlength="60"></div></div>
<label class="chk" style="margin:6px 0"><input type="checkbox" id="tt" checked> 첫 줄을 제목처럼 굵고 크게</label>
<div class="tiles hk-tiles"><div class="tile light"><div class="k">문단(줄)</div><div class="v" id="cL">0</div></div><div class="tile light"><div class="k">글자 (공백 포함)</div><div class="v" id="cA">0</div></div></div>
<div class="btns"><button class="btn dl" id="go" type="button" disabled>한글 파일 만들기</button><button class="btn ghost" id="clr" type="button">지우기</button></div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>''', '''<script>
(function(){var $=HL.$;var K='text-to-hwp';var sv=HL.store.get(K,null);if(sv&&sv.fmt)$('#fmt').value=sv.fmt;if(sv&&sv.tt!=null)$('#tt').checked=!!sv.tt;
function upd(){var t=$('#txt').value;var s=HLK.stats(t);$('#cL').textContent=HLK.fmtN(t?HLK.splitText(t).length:0);$('#cA').textContent=HLK.fmtN(s.all);$('#go').disabled=!t.trim()}
$('#txt').addEventListener('input',upd);['#fmt','#tt'].forEach(function(x){$(x).addEventListener('change',function(){HL.store.set(K,{fmt:$('#fmt').value,tt:$('#tt').checked})})});
async function add(fs){var f=fs[0];if(!f)return;$('#st').textContent='‘'+f.name+'’ 읽는 중…';try{var ps=await HLK.readText(f);$('#txt').value=ps.join('\\n');if(!$('#nm').value)$('#nm').value=HL.baseName(f.name);$('#st').textContent='‘'+f.name+'’에서 '+ps.length+'개 문단을 가져왔어요. 고칠 곳이 있으면 고친 뒤 만드세요.'}catch(e){$('#st').textContent=e.message}upd()}
HL.dropzone($('#drop'),{multiple:false,accept:'.txt,.md,.docx,.csv,.doc,text/plain',onFiles:add});
$('#clr').onclick=function(){$('#txt').value='';$('#nm').value='';upd()};
$('#go').onclick=HL.run($('#go'),async function(){var ps=HLK.splitText($('#txt').value);while(ps.length>1&&!ps[ps.length-1].trim())ps.pop();var fmt=$('#fmt').value;
 var r=await HLK.make(ps,{fmt:fmt,title:$('#tt').checked,onProgress:function(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%';$('#st').textContent='문서 엔진 받는 중… (처음 한 번만)'}});$('#pb').hidden=true;
 var nm=($('#nm').value.trim()||ps[0].trim().slice(0,30)||'새 문서').replace(/[\\\\/:*?"<>|]/g,'_');HL.download(new Blob([r.bytes],{type:HLK.mime[fmt]}),nm+'.'+fmt);
 $('#st').textContent=r.pages+'쪽짜리 .'+fmt+' 파일을 만들었어요 ('+HL.bytes(r.bytes.length)+').'},'만드는 중…');upd();
})();
</script>''')


PAGES = [
  dict(slug='hwp-to-hwpx', name='HWP HWPX 변환 (한글 HWP를 HWPX로 바꾸기, 여러 개 한 번에)',
    h1='HWP를 <b>HWPX로 변환</b>', lead='옛 한글 파일(.hwp)을 새 형식(.hwpx)으로 바꿔요. 여러 개를 놓으면 ZIP으로 묶어 줘요.',
    desc='한글 .hwp 파일을 .hwpx로 바꿔요. 여러 파일을 한 번에 놓으면 ZIP으로 받고, 한컴오피스 설치나 회원가입 없이 이 기기 안에서만 변환해요. HWPX는 한글 2014 이후 기본 저장 형식이에요.',
    tool=conv_tool('hwp', 'hwpx'),
    warn='<b>중요한 문서는 바꾼 뒤 한 번 열어 보세요.</b> 오픈소스 엔진(rhwp)이 문서를 읽어 다시 저장하는 방식이라, 글맵시·차트·특수 개체가 많은 문서는 일부 모양이 달라질 수 있어요.',
    body=[
      ('HWP와 HWPX는 무엇이 다른가요', '<p>둘 다 한글(한컴오피스) 문서예요. <b>.hwp</b>는 1990년대부터 쓰던 형식이고, <b>.hwpx</b>는 2014년부터 들어온 새 형식이에요. HWPX는 속이 ZIP 파일과 XML 글로 되어 있어서 다른 프로그램이 읽기 쉽고, 공공기관에서는 HWPX로 내라고 하는 곳이 늘고 있어요.</p>'
        '<table class="tbl"><thead><tr><th></th><th>HWP</th><th>HWPX</th></tr></thead><tbody><tr><td>나온 때</td><td>한글 97 무렵부터</td><td>한글 2014부터 (2020 이후 기본)</td></tr><tr><td>속 구조</td><td>바이너리(사람이 못 읽음)</td><td>ZIP + XML(글)</td></tr><tr><td>옛 한글에서 열기</td><td>잘 열림</td><td>한글 2010 이하는 안 열림</td></tr><tr><td>다른 프로그램 호환</td><td>낮음</td><td>높음 (표준 OWPML)</td></tr></tbody></table>'),
      ('HWPX로 바꿔야 할 때', '<ul><li>기관·학교 제출 안내에 ‘HWPX 형식으로’라고 적혀 있을 때</li><li>문서 관리 시스템이나 AI 도구가 HWP는 못 읽고 HWPX만 읽을 때</li><li>예전 HWP 파일 수십 개를 새 형식으로 한꺼번에 정리할 때</li></ul>'),
      ('사용 방법', '<ol><li>.hwp 파일을 놓아요. 여러 개도 돼요. 처음 한 번은 문서 엔진(약 4MB)을 받아요.</li><li>첫 파일의 첫 쪽이 미리보기로 나와요. 내용이 맞는지 봐요.</li><li>‘HWPX로 변환’을 누르면 파일이 하나면 바로, 여러 개면 ZIP으로 받아져요.</li></ol>'),
      ('HWP HWPX 변환이 안 될 때', '<ul><li><b>암호가 걸린 문서</b>는 한글에서 암호를 푼 뒤 넣어 주세요.</li><li><b>배포용 문서</b>(복사·인쇄 막힘)는 바꿀 수 없어요.</li><li>HWP 3.0 같은 아주 옛 파일은 글자만 읽혀 변환이 안 될 수 있어요.</li></ul>'),
    ],
    faq=[('한컴오피스 없이 HWP를 HWPX로 바꿀 수 있나요?', '네. 이 페이지는 브라우저 안의 문서 엔진으로 바꾸기 때문에 한컴오피스가 없어도 돼요. 파일은 서버로 올라가지 않아요.'),
         ('한글 프로그램에서 직접 바꾸려면 어떻게 하나요?', '한글에서 파일을 연 뒤 [파일] → [다른 이름으로 저장]에서 파일 형식을 ‘한글 표준 문서(*.hwpx)’로 고르면 돼요.'),
         ('바꾼 HWPX가 한글 2010에서 안 열려요.', '한글 2010 이하 버전은 HWPX를 못 여는 경우가 많아요. 받는 사람이 옛 버전을 쓰면 HWP 그대로 보내거나 PDF로 바꿔 보내세요.'),
         ('여러 파일을 한 번에 바꿀 수 있나요?', '네. 파일 여러 개를 한꺼번에 놓으면 모두 바꿔서 ZIP 하나로 받아요. 개수 제한은 없지만 휴대전화는 수십 개씩 나눠 하세요.')]),
  dict(slug='hwpx-to-hwp', name='HWPX HWP 변환 (HWPX를 옛날 한글 HWP로 바꾸기, 무료)',
    h1='HWPX를 <b>HWP로 변환</b>', lead='HWPX 파일이 안 열리는 옛 한글(2010 이하)에서도 열리게 .hwp로 바꿔요.',
    desc='한글 .hwpx 파일을 .hwp로 바꿔요. 한글 2010 이하나 HWPX를 못 여는 프로그램에서 열어야 할 때 써요. 여러 파일은 ZIP으로 받고, 설치·가입 없이 이 기기 안에서만 변환해요.',
    tool=conv_tool('hwpx', 'hwp'),
    warn='<b>중요한 문서는 바꾼 뒤 한 번 열어 보세요.</b> 오픈소스 엔진(rhwp)이 다시 저장하는 방식이라 특수 개체가 많은 문서는 모양이 조금 달라질 수 있어요.',
    body=[
      ('HWPX 파일이 안 열릴 때', '<p>HWPX는 한글 2014 이후 형식이라 <b>한글 2010, 한글 2007</b> 같은 옛 버전이나 일부 뷰어·문서 관리 프로그램에서는 열리지 않아요. 이럴 때 HWP로 바꾸면 거의 모든 한글 버전에서 열려요.</p>'
        '<table class="tbl"><thead><tr><th>한글 버전</th><th>HWP 열기</th><th>HWPX 열기</th></tr></thead><tbody><tr><td>한글 2007·2010</td><td>O</td><td>X (대부분)</td></tr><tr><td>한글 2014·2018</td><td>O</td><td>O</td></tr><tr><td>한글 2020 이후</td><td>O</td><td>O (기본 저장)</td></tr></tbody></table>'),
      ('사용 방법', '<ol><li>.hwpx 파일을 놓아요. 여러 개도 돼요.</li><li>첫 쪽 미리보기로 내용을 확인해요.</li><li>‘HWP로 변환’을 누르면 .hwp 파일(여러 개면 ZIP)이 받아져요.</li></ol>'),
      ('HWPX를 HWP로 바꿀 때 알아 둘 점', '<ul><li>글자·문단·표·그림은 그대로 옮겨요. 글꼴은 받는 사람 컴퓨터에 없으면 비슷한 글꼴로 보여요.</li><li>암호가 걸린 HWPX는 한글에서 암호를 푼 뒤 넣어 주세요.</li><li>그래도 안 열리면 <a href="/pdf/hwp-to-pdf.html">PDF로 바꿔서</a> 보내는 게 가장 확실해요.</li></ul>'),
    ],
    faq=[('HWPX를 HWP로 바꾸면 내용이 빠지나요?', '보통 글·표·그림은 그대로 있어요. 차트, 글맵시, 양식 개체처럼 특수한 것은 모양이 달라질 수 있으니 중요한 문서는 바꾼 뒤 한 번 열어 확인하세요.'),
         ('한글 프로그램에서 HWP로 저장하는 방법은?', '한글에서 HWPX를 연 뒤 [파일] → [다른 이름으로 저장] → 파일 형식 ‘한글 문서(*.hwp)’를 고르면 돼요.'),
         ('휴대전화에서도 되나요?', '네. 휴대전화 브라우저에서 파일을 골라 바꿀 수 있어요. 처음 한 번 문서 엔진(약 4MB)을 받아요.')]),
  dict(slug='hwp-to-txt', name='HWP 텍스트 추출 (한글 파일 글자만 TXT로, 글자 수·원고지 매수)',
    h1='HWP <b>텍스트 추출</b>', lead='한글 문서의 글자만 뽑아 TXT로 받거나 복사해요. 글자 수(공백 포함·제외)와 원고지 매수도 바로 세요.',
    desc='한글(.hwp·.hwpx) 문서에서 글자만 뽑아 TXT 파일로 받거나 복사해요. 공백 포함·제외 글자 수, 200자 원고지 매수, 단어·문단 수를 함께 보여 주고, 여러 파일은 이어 붙여요. 한컴오피스 없이 기기 안에서만 처리해요.',
    tool=TXT_TOOL, warn='',
    body=[
      ('한글 파일에서 글자만 뽑는 경우', '<ul><li>한컴오피스가 없는데 HWP 안의 글을 복사해야 할 때</li><li>자기소개서·보고서가 몇 자인지 <b>공백 포함/제외 글자 수</b>를 세야 할 때</li><li>HWP 글을 블로그, 카톡, 메일, AI 도구에 붙여 넣을 때</li></ul>'),
      ('글자 수는 어떻게 세나요', '<table class="tbl"><thead><tr><th>숫자</th><th>세는 방법</th><th>주로 쓰는 곳</th></tr></thead><tbody><tr><td>공백 포함</td><td>띄어쓰기까지 모두 (줄바꿈은 뺌)</td><td>자기소개서, 대부분의 채용 사이트</td></tr><tr><td>공백 제외</td><td>띄어쓰기·줄바꿈 빼고</td><td>논술, 일부 공모전</td></tr><tr><td>200자 원고지</td><td>공백 포함 글자 수 ÷ 200, 올림</td><td>원고료, 기사·수필 분량</td></tr></tbody></table>'
        '<p>예를 들어 공백 포함 1,530자면 원고지 8장(1,530÷200=7.65 → 올림)이에요. 한글 프로그램의 [파일] → [문서 정보] → [문서 통계]와 세는 방법이 조금 다를 수 있어요.</p>'),
      ('사용 방법', '<ol><li>.hwp나 .hwpx 파일을 놓아요. 여러 개를 놓으면 파일 이름을 붙여 차례로 이어 붙여요.</li><li>뽑힌 글과 글자 수가 바로 나와요. 쪽 구분선이 필요하면 체크하세요.</li><li>‘TXT로 받기’ 또는 ‘글 복사’를 눌러요. TXT는 메모장에서 한글이 안 깨지게 저장돼요.</li></ol>'),
      ('표 안의 글자도 나오나요', '<p>네. 표 칸 안 글자도 쪽에 보이는 순서대로 나와요. 다만 칸 구분은 줄바꿈으로만 남아서, 표 모양 그대로 옮기려면 <a href="/pdf/hwp-viewer.html">HWP 뷰어</a>에서 표를 복사하는 게 좋아요.</p>'),
    ],
    faq=[('HWP 파일 글자 수는 어디서 확인하나요?', '한글 프로그램에서는 [파일] → [문서 정보] → [문서 통계]에서 봐요. 한글이 없으면 이 페이지에 파일을 놓으면 공백 포함·제외 글자 수가 바로 나와요.'),
         ('뽑은 TXT를 메모장에서 열면 한글이 깨져요.', '이 페이지는 UTF-8(BOM 포함)으로 저장해서 윈도우 메모장에서도 깨지지 않아요. 그래도 깨지면 다른 프로그램에서 인코딩을 UTF-8로 골라 여세요.'),
         ('스캔해서 만든 HWP(그림만 있는 문서)도 되나요?', '그림 속 글자는 뽑히지 않아요. 그런 경우 PDF로 바꾼 뒤 PDF OCR로 글자를 읽으세요.'),
         ('암호가 걸린 한글 파일은요?', '암호 문서는 열 수 없어요. 한글에서 암호를 푼 뒤 다시 넣어 주세요.')]),
  dict(slug='text-to-hwp', name='텍스트를 한글 파일로 (TXT·워드 DOCX → HWP·HWPX 만들기)',
    h1='텍스트·워드를 <b>한글 파일로</b>', lead='붙여 넣은 글이나 TXT·워드(DOCX) 파일로 한글(.hwp·.hwpx) 문서를 만들어요. 한컴오피스가 없어도 돼요.',
    desc='붙여 넣은 글이나 TXT·워드(.docx) 파일의 내용으로 한글 문서(.hwp 또는 .hwpx)를 만들어요. 줄바꿈은 문단으로, 첫 줄은 제목처럼 굵게 만들 수 있어요. 한컴오피스 없이 이 기기 안에서만 만들어요.',
    tool=MAKE_TOOL, warn='<b>글 내용을 옮기는 도구예요.</b> 워드의 글꼴·색·표·그림 같은 꾸밈은 옮기지 않고 글과 문단만 한글 문서로 만들어요.',
    body=[
      ('한컴오피스 없이 HWP 파일 만들기', '<p>기관이나 학교에서 ‘한글 파일로 내세요’라고 하는데 한컴오피스가 없을 때 써요. 글을 붙여 넣고 버튼을 누르면 한글에서 바로 열리는 .hwp(또는 .hwpx) 파일이 만들어져요. 받은 사람은 한글에서 글꼴과 모양을 다듬으면 돼요.</p>'),
      ('워드(DOCX)를 한글(HWP)로 바꾸기', '<p>워드 파일을 놓으면 문단 글을 차례로 가져와요. 표 안의 글자도 문단으로 들어와요. 꾸밈까지 그대로 옮겨야 하면 한글 프로그램에서 워드 파일을 직접 열어 [다른 이름으로 저장] → HWP를 고르는 게 가장 정확해요.</p>'
        '<table class="tbl"><thead><tr><th>넣는 것</th><th>옮겨지는 것</th><th>안 옮겨지는 것</th></tr></thead><tbody><tr><td>붙여 넣은 글·TXT</td><td>글, 줄바꿈(문단)</td><td>—</td></tr><tr><td>워드 .docx</td><td>글, 문단, 탭</td><td>글꼴·색·표 모양·그림</td></tr><tr><td>워드 .doc(옛 형식)</td><td colspan="2">읽지 못해요. 워드에서 .docx로 저장 후 넣으세요</td></tr></tbody></table>'),
      ('HWP와 HWPX 중 무엇으로 만들까요', '<p>받는 사람이 어떤 한글 버전을 쓰는지 모르면 <b>HWP</b>가 안전해요. 기관 안내에 HWPX라고 적혀 있으면 HWPX를 고르세요. 만든 뒤에도 <a href="/pdf/hwp-to-hwpx.html">HWP→HWPX</a>, <a href="/pdf/hwpx-to-hwp.html">HWPX→HWP</a>로 바꿀 수 있어요.</p>'),
      ('사용 방법', '<ol><li>글을 붙여 넣거나 TXT·DOCX 파일을 놓아요.</li><li>저장 형식(HWP/HWPX)과 파일 이름을 정해요. 첫 줄 제목 굵게는 켜고 끌 수 있어요.</li><li>‘한글 파일 만들기’를 누르면 바로 받아져요. 글이 길면 쪽이 저절로 넘어가요.</li></ol>'),
    ],
    faq=[('메모장 글을 한글 파일로 저장하려면?', '메모장 글을 복사해 이 페이지 칸에 붙여 넣고 ‘한글 파일 만들기’를 누르면 .hwp 파일이 받아져요. TXT 파일을 그대로 끌어다 놓아도 돼요.'),
         ('만든 한글 파일은 어떤 글꼴인가요?', '한글 기본 글꼴(함초롬바탕, 10pt)로 만들어져요. 한글에서 열어 글꼴과 크기를 바꾸면 돼요.'),
         ('휴대전화에서 HWP 파일을 만들 수 있나요?', '네. 휴대전화 브라우저에서 글을 붙여 넣고 만들면 파일이 다운로드 폴더에 저장돼요. 카톡이나 메일로 바로 보낼 수 있어요.'),
         ('엑셀 표를 한글 표로 만들 수 있나요?', '이 페이지는 글만 옮겨요. 표는 엑셀에서 복사해 한글에 붙여 넣으면 표로 들어가요.')]),
]


def jesc(s):
    return re.sub(r'<[^>]+>', '', s)


def page(p):
    url = f"/pdf/{p['slug']}.html"
    full = SITE + url
    name, desc = p['name'], p['desc']
    s = TPL
    head, rest = s.split('</head>', 1)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(name, quote=False)} | 홍라이프 도구</title>', head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), head)
    head = head.replace('https://honglife.co.kr/pdf/hwp-to-pdf.html', full)
    old_name = 'HWP를 PDF로 변환 (한글 파일 PDF 변환, 여러 개 한 번에)'
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(name) + ' | 홍라이프 도구', head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), head)
    head = head.replace(old_name, html.escape(name))
    # JSON-LD: rebuild
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "url": full, "description": desc,
           "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": "ko",
           "browserRequirements": "JavaScript 사용 가능한 최신 브라우저", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"},
           "isAccessibleForFree": True, "dateModified": DATE}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홍라이프 도구", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "PDF 도구", "item": SITE + "/pdf/"},
        {"@type": "ListItem", "position": 3, "name": name, "item": full}]}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": jesc(a)}} for q, a in p['faq']]}
    ld = ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>' for o in (app, bc, fq))
    head = head + ld + FILE_TOOL_CSS + '\n'
    # body
    pre, main_and_after = rest.split('<main class="wrap wide">', 1)
    after = main_and_after.split('</main>', 1)[1]
    tool_html, tool_js = p['tool']
    sec = []
    toc = ''.join(f'<a href="#g-{i+1}">{t}</a>' for i, (t, _) in enumerate(p['body']))
    sec.append(f'<section class="card guide"><h2>{p["h1"].replace("<b>", "").replace("</b>", "")} 자세히 알아보기</h2>'
               f'<p class="note">홍라이프 도구 · {DATE} 업데이트</p><nav class="xp-toc" aria-label="차례">{toc}</nav>')
    for i, (t, b) in enumerate(p['body']):
        sec.append(f'<h3 id="g-{i+1}">{t}</h3>{b}')
    sec.append('<h3>참고한 자료</h3><ul class="src"><li><a href="https://www.hancom.com/support/downloadCenter/hwpOwpml" rel="noopener" target="_blank">한글과컴퓨터 — 한글 문서 파일 형식 공개</a> — HWP 5.0·HWPX(OWPML) 형식 문서</li>'
               '<li><a href="https://github.com/edwardkim/rhwp" rel="noopener" target="_blank">rhwp (MIT)</a> — 브라우저용 한글 문서 엔진, 0.8.7 사용</li></ul></section>')
    faq = '<section class="card faq"><h2>자주 묻는 질문</h2>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in p['faq']) + '</section>'
    rel = '<section class="card rel"><h2>다른 한글(HWP) 도구</h2><ul>' + ''.join(
        f'<li><a href="{u}"><b>{t}</b><span>{d}</span></a></li>' for u, t, d in HWP_TOOLS if u != url) + '</ul></section>'
    warn = f'<div class="warn">{p["warn"]}</div>' if p['warn'] else ''
    main = (f'<main class="wrap wide">\n<header class="top"><p class="crumb"><a href="/">홈</a> › <a href="/pdf/">PDF 도구</a> › 한글(HWP)</p>'
            f'<h1>{p["h1"]}</h1><p class="lead">{p["lead"]}</p>{SAFE}</header>\n{warn}{tool_html}\n' + ''.join(sec) + faq + rel + '\n</main>')
    # scripts: drop the template's tool script (last inline script) and add kit + ours
    after = re.sub(r'<script>\s*\(function\(\)\{var \$=HL\.\$;var items=\[\],stop=false.*?</script>', '', after, flags=re.S)
    after = after.replace('<script src="/assets/js/hlhwp.js', KIT.replace('<script', '<script') + '\n<script src="/assets/js/hlhwp.js', 1) if False else after
    after = re.sub(r'(<script src="/assets/js/hlhwp\.js[^"]*"></script>)', r'\1\n' + KIT + '\n' + tool_js.replace('\\', '\\\\'), after, count=1)
    out = head + '</head>' + pre + main + after
    assert 'hwp-to-pdf.html' not in out.split('</head>')[0], p['slug']
    open(os.path.join(OUT, p['slug'] + '.html'), 'w', encoding='utf-8').write(out)
    return url


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for p in PAGES:
        print('wrote', page(p))
