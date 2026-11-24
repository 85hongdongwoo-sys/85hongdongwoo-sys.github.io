#!/usr/bin/env python3
"""한글(HWP) 도구 페이지 만들기 — build/hwp/template.html(HWP→PDF 페이지)의 틀을 빌려 overlay/pdf/*.html 을 써요.
로컬에서 한 번 돌리고 결과(overlay)를 커밋해요:  python3 build/hwp/gen_hwp_tools.py"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TPL = open(os.path.join(ROOT, 'build/hwp/template.html'), encoding='utf-8').read()
OUT = os.path.join(ROOT, 'overlay/pdf')
SITE = 'https://honglife.co.kr'
KIT = '<script src="/assets/js/hlhwpkit.js?v=7"></script>'
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
    ('/pdf/hwp-to-image.html', 'HWP를 그림(PNG·JPG)으로', '쪽마다 한 장, 카톡·블로그용'),
    ('/pdf/hwp-to-docx.html', 'HWP를 워드(DOCX)로', '워드·구글 문서에서 열리게'),
    ('/pdf/excel-to-hwp.html', '엑셀·CSV를 한글 표로', '복사한 표도 HWP 표로'),
    ('/pdf/hwp-table-to-excel.html', 'HWP 표를 엑셀로', '문서 안 표를 XLSX·CSV로'),
    ('/pdf/hwp-image-extract.html', 'HWP 그림 꺼내기', '넣은 사진을 원본 그대로'),
    ('/pdf/hwp-password.html', 'HWP 암호 걸기·풀기', '보내기 전 열기 암호, 아는 암호 풀기'),
    ('/pdf/hwp-compare.html', '한글 문서 비교', '두 파일의 달라진 줄 찾기'),
    ('/pdf/hwp-privacy-check.html', 'HWP 개인정보 찾기', '주민번호·전화번호 확인'),
    ('/pdf/hwp-info.html', '한글 문서 정보·글꼴 확인', '버전·쪽 수·쓴 글꼴'),
    ('/pdf/hwp-shortcuts.html', '한글 단축키 모음', '표·쪽 번호·저장 단축키, 인쇄용'),
    ('/doc/gongmun-checker.html', '공문서 오류 검사기', 'HWP 공문 맞춤법·서식 점검'),
]

FILE_TOOL_CSS = '<style>.hk-out{white-space:pre-wrap;word-break:break-all;overflow-wrap:anywhere;max-height:420px;overflow:auto;background:#F7F8FA;border:1px solid #E3E6EB;border-radius:12px;padding:12px 14px;font-size:15px;line-height:1.7;margin-top:10px}.hk-tiles{margin-top:10px}#tool textarea{width:100%;box-sizing:border-box}.hk-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin-top:8px}.hk-grid figure{margin:0;border:1px solid #E3E6EB;border-radius:10px;padding:6px;background:#fff;text-align:center;min-width:0}.hk-grid canvas,.hk-grid img{max-width:100%;height:auto;display:block;margin:0 auto}.hk-grid figcaption{font-size:13px;color:#5B6B82;margin-top:4px;overflow-wrap:anywhere}.hk-tbl{overflow-x:auto;margin-top:8px}.hk-diff div{padding:1px 6px;border-radius:4px}.hk-add{background:#E7F0FF;color:#0B3D91}.hk-del{background:#FDECEC;color:#8A1C1C;text-decoration:line-through}.hk-skip{color:#8A94A6;font-size:13px;text-align:center}.hk-tbl kbd{font-family:inherit;background:#F1F3F6;border:1px solid #D9DDE3;border-radius:5px;padding:1px 6px;font-size:14px;white-space:nowrap}@media print{.brandbar,footer,.rel,.faq,.guide,#tool .btns,#tool .f,#cats,.warn,.safe{display:none!important}}.hk-chip{border:1px solid #D9DDE3;background:#fff;color:#1F2937;border-radius:999px;padding:6px 14px;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit}.hk-chip[aria-pressed=true]{background:#1D4ED8;border-color:#1D4ED8;color:#fff}.hk-big{padding:10px 18px;font-size:15px}.hk-fonts{columns:2;column-gap:20px;padding-left:18px}@media(max-width:520px){.hk-fonts{columns:1}}.hk-tbl td,.hk-tbl th{white-space:nowrap;max-width:240px;overflow:hidden;text-overflow:ellipsis}</style>'


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
<label class="chk" style="margin:4px 0 0"><input type="checkbox" id="sq" checked> 빈 줄 여러 개는 한 줄로</label>
<div class="hk-out" id="out" tabindex="0" aria-label="뽑은 글"></div>
<div class="btns"><button class="btn dl" id="dl" type="button">TXT로 받기</button><button class="btn" id="cp" type="button">글 복사</button></div>
<p class="note" id="st" aria-live="polite"></p>
</div>
<div class="prog" id="pb" hidden><i></i></div>
</section>''', '''<script>
(function(){var $=HL.$;var items=[];
function body(){var sq=$('#sq').checked;var parts=items.filter(function(it){return it.h}).map(function(it){var t=HLK.all(it.h);
  if(sq)t=t.replace(/\\n[ \\t]*\\n(\\s*\\n)+/g,'\\n\\n');return (items.length>1?'['+it.name+']\\n':'')+t.trim()});return parts.join('\\n\\n')}
function show(){var t=body();$('#out').textContent=t||'(글자가 없어요)';var s=HLK.stats(t);$('#cAll').textContent=HLK.fmtN(s.all);$('#cNo').textContent=HLK.fmtN(s.no);$('#cMs').textContent=HLK.fmtN(s.ms200)+'장';$('#cWp').textContent=HLK.fmtN(s.words)+' / '+HLK.fmtN(s.paras);$('#opt').hidden=!items.some(function(it){return it.h})}
function draw(){var ul=$('#list');ul.innerHTML='';items.forEach(function(it,i){var li=HL.el('li');li.appendChild(HL.el('span',{'class':'nm',text:(i+1)+'. '+it.name}));li.appendChild(HL.el('span',{'class':'sz',text:(it.h&&it.h.n?it.h.n+'쪽 · ':'')+HL.bytes(it.size)}));li.appendChild(HL.el('span',{'class':'stt'+(it.h?' ok':it.err?' bad':''),text:it.err||it.state||''}));var x=HL.el('button',{type:'button',text:'빼기'});x.onclick=function(){if(it.h&&it.h.free)it.h.free();items.splice(i,1);draw();show()};li.appendChild(x);ul.appendChild(li)})}
async function add(fs){for(var f of fs){var it={name:f.name,size:f.size,state:'여는 중…'};items.push(it);draw();try{it.h=await HLHWP.open(f,function(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%'});it.state=it.h.fallback?'글자만 읽음':'읽음'}catch(e){it.err=e.message}$('#pb').hidden=true;draw()}show()}
HL.dropzone($('#drop'),{multiple:true,accept:'.hwp,.hwpx',onFiles:add});$('#sq').onchange=show;
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

OPEN1 = """function prog(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%';$('#st').textContent='문서 엔진 받는 중… (처음 한 번만)'}
async function openOne(f){$('#st').textContent='‘'+f.name+'’ 여는 중…';var h=await HLHWP.open(f,prog);$('#pb').hidden=true;$('#st').textContent='';if(!h.doc)throw new Error('문서 엔진으로 읽지 못한 파일이에요. HWP 뷰어에서 글자만 볼 수 있어요.');return h}"""

IMG_TOOL = ("""<section class="card tool" id="tool">
<div class="drop" id="drop"><b>HWP·HWPX 파일을 놓거나 눌러서 고르세요</b><span>.hwp · .hwpx · 쪽마다 그림 한 장</span></div>
<div id="opt" hidden>
<p class="note" id="info"></p>
<div class="grid g2" style="margin-top:8px"><div class="f"><label for="fm">그림 형식</label><select id="fm"><option value="png" selected>PNG (선명)</option><option value="jpg">JPG (작은 용량)</option></select></div>
<div class="f"><label for="sc">크기</label><select id="sc"><option value="1.5">보통 1200px</option><option value="2" selected>선명 1600px</option><option value="3">인쇄 2400px</option></select></div>
<div class="f"><label for="rng">쪽 범위 (비우면 전체)</label><input id="rng" placeholder="예: 1-3, 5" inputmode="numeric"></div></div>
<div class="btns"><button class="btn dl" id="go" type="button">그림으로 저장</button></div>
<h3>미리보기</h3><div class="hk-grid" id="pv"></div>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var h=null;"""+OPEN1+"""
function pages(){var r=$('#rng').value.trim();if(!r)return Array.from({length:h.n},function(_,i){return i});var out=[];r.split(',').forEach(function(x){var m=x.trim().match(/^(\\d+)(?:\\s*-\\s*(\\d+))?$/);if(!m)throw new Error('쪽 범위는 1-3, 5처럼 적어 주세요');var a=+m[1],b=+(m[2]||m[1]);for(var i=Math.min(a,b);i<=Math.max(a,b);i++)if(i>=1&&i<=h.n&&out.indexOf(i-1)<0)out.push(i-1)});if(!out.length)throw new Error('범위에 맞는 쪽이 없어요 (전체 '+h.n+'쪽)');return out}
async function add(fs){try{if(h&&h.free)h.free();h=await openOne(fs[0]);$('#opt').hidden=false;$('#info').textContent='‘'+h.name+'’ · '+h.n+'쪽';var pv=$('#pv');pv.innerHTML='';for(var i=0;i<Math.min(h.n,6);i++){var cv=h.canvas(i,0.45);var fg=HL.el('figure');fg.appendChild(cv);fg.appendChild(HL.el('figcaption',{text:(i+1)+'쪽'}));pv.appendChild(fg)}if(h.n>6)pv.appendChild(HL.el('p',{'class':'note',text:'… 모두 '+h.n+'쪽'}))}catch(e){$('#pb').hidden=true;$('#st').textContent=e.message}}
HL.dropzone($('#drop'),{multiple:false,accept:'.hwp,.hwpx',onFiles:add});
$('#go').onclick=HL.run($('#go'),async function(){var list=pages(),fm=$('#fm').value,sc=+$('#sc').value,files=[];$('#pb').hidden=false;
 for(var k=0;k<list.length;k++){var i=list[k];var cv=h.canvas(i,sc);if(fm==='jpg'){var c2=document.createElement('canvas');c2.width=cv.width;c2.height=cv.height;var x=c2.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c2.width,c2.height);x.drawImage(cv,0,0);cv=c2}
  var bl=await HL.canvasBlob(cv,fm==='jpg'?'image/jpeg':'image/png',0.92);files.push({n:HL.baseName(h.name)+'_'+String(i+1).padStart(String(h.n).length,'0')+'쪽.'+fm,b:bl});$('#pb i').style.width=Math.round((k+1)/list.length*100)+'%';$('#st').textContent=(k+1)+'/'+list.length+'쪽';await new Promise(function(r){setTimeout(r,0)})}
 $('#pb').hidden=true;if(files.length===1){HL.download(files[0].b,files[0].n)}else{await HL.need('jszip');var z=new JSZip();files.forEach(function(f){z.file(f.n,f.b)});HL.download(await z.generateAsync({type:'blob'}),HL.baseName(h.name)+'_그림.zip')}
 $('#st').textContent=files.length+'장을 '+fm.toUpperCase()+'로 저장했어요.'},'그리는 중…');
})();
</script>""")

DOCX_TOOL = ("""<section class="card tool" id="tool">
<div class="drop" id="drop"><b>HWP·HWPX 파일을 놓거나 눌러서 고르세요</b><span>.hwp · .hwpx · 여러 개 → 파일마다 .docx</span></div>
<ul class="files" id="list"></ul>
<div id="opt" hidden>
<label class="chk" style="margin:6px 0"><input type="checkbox" id="sq" checked> 빈 줄 여러 개는 한 줄로</label>
<div class="btns"><button class="btn dl" id="go" type="button">워드(DOCX)로 변환</button></div>
<h3 id="pvh">글 미리보기</h3><div class="hk-out" id="pv"></div>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var items=[];"""+OPEN1+"""
function paras(it){var t=HLK.all(it.h);if($('#sq').checked)t=t.replace(/\\n[ \\t]*\\n(\\s*\\n)+/g,'\\n\\n');return HLK.splitText(t.trim())}
function draw(){var ul=$('#list');ul.innerHTML='';items.forEach(function(it,i){var li=HL.el('li');li.appendChild(HL.el('span',{'class':'nm',text:(i+1)+'. '+it.name}));li.appendChild(HL.el('span',{'class':'sz',text:(it.h?it.h.n+'쪽 · ':'')+HL.bytes(it.size)}));li.appendChild(HL.el('span',{'class':'stt'+(it.h?' ok':' bad'),text:it.err||'준비됨'}));var x=HL.el('button',{type:'button',text:'빼기'});x.onclick=function(){if(it.h&&it.h.free)it.h.free();items.splice(i,1);draw()};li.appendChild(x);ul.appendChild(li)});
 var ok=items.filter(function(it){return it.h});$('#opt').hidden=!ok.length;if(ok.length)$('#pv').textContent=paras(ok[0]).join('\\n').slice(0,3000)}
async function add(fs){for(var f of fs){var it={name:f.name,size:f.size};try{it.h=await openOne(f)}catch(e){it.err=e.message;$('#pb').hidden=true}items.push(it);draw()}}
HL.dropzone($('#drop'),{multiple:true,accept:'.hwp,.hwpx',onFiles:add});$('#sq').onchange=draw;
$('#go').onclick=HL.run($('#go'),async function(){var ok=items.filter(function(it){return it.h}),out=[];for(var it of ok){out.push({n:HL.baseName(it.name)+'.docx',b:await HLK.docxFrom(paras(it),HL.baseName(it.name))})}
 if(out.length===1)HL.download(new Blob([out[0].b],{type:HLK.mime.docx}),out[0].n);else{await HL.need('jszip');var z=new JSZip();out.forEach(function(f){z.file(f.n,f.b)});HL.download(await z.generateAsync({type:'blob'}),'한글문서_워드_'+HL.stamp()+'.zip')}
 $('#st').textContent=out.length+'개 파일을 워드(.docx)로 바꿨어요.'},'변환 중…');
})();
</script>""")

X2H_TOOL = ("""<section class="card tool" id="tool">
<div class="drop" id="drop"><b>엑셀·CSV 파일을 놓거나 눌러서 고르세요</b><span>.xlsx · .xls · .csv · 또는 아래에 표를 붙여 넣기</span></div>
<div class="f" style="margin-top:12px"><label for="paste">엑셀에서 복사한 표 붙여 넣기 <span class="note">— 칸은 탭, 줄은 줄바꿈</span></label><textarea id="paste" rows="5" placeholder="이름&#9;부서&#9;연락처&#10;홍길동&#9;총무과&#9;010-0000-0000"></textarea></div>
<div id="opt" hidden>
<div class="grid g2" style="margin-top:8px"><div class="f" id="shw" hidden><label for="sh">시트</label><select id="sh"></select></div>
<div class="f"><label for="ti">표 위 제목 (비워도 돼요)</label><input id="ti" maxlength="60" placeholder="예: 2026 직원 연락처"></div>
<div class="f"><label for="fmt">저장 형식</label><select id="fmt"><option value="hwp" selected>HWP (기본)</option><option value="hwpx">HWPX (새 형식)</option></select></div></div>
<label class="chk" style="margin:6px 0"><input type="checkbox" id="bh" checked> 첫 줄(머리글)을 굵게</label>
<p class="note" id="info"></p><div class="hk-tbl" id="pv"></div>
<div class="btns"><button class="btn dl" id="go" type="button">한글 표로 만들기</button></div>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var wb=null,rows=[],name='표';var MAX=3000;
function clean(r){r=r.map(function(x){return x.map(function(v){return v==null?'':String(v)})});while(r.length&&!r[r.length-1].some(function(v){return v.trim()}))r.pop();var C=0;r.forEach(function(x){for(var i=x.length-1;i>=0;i--){if(String(x[i]).trim()){C=Math.max(C,i+1);break}}});return r.map(function(x){x=x.slice(0,C);while(x.length<C)x.push('');return x})}
function show(){var R=rows.length,C=R?rows[0].length:0;$('#opt').hidden=!R;$('#info').textContent=R?R+'줄 × '+C+'칸'+(R*C>MAX?' — 칸이 '+MAX+'개가 넘어 앞부분만 넣어요':''):'';var t='<table class="tbl"><tbody>'+rows.slice(0,12).map(function(r,i){return '<tr>'+r.map(function(v){return (i?'<td>':'<th>')+HL.esc(v)+(i?'</td>':'</th>')}).join('')+'</tr>'}).join('')+'</tbody></table>'+(R>12?'<p class="note">… '+(R-12)+'줄 더</p>':'');$('#pv').innerHTML=t}
function useSheet(){var ws=wb.Sheets[$('#sh').value];rows=clean(XLSX.utils.sheet_to_json(ws,{header:1,raw:false,defval:''}));show()}
async function add(fs){var f=fs[0];if(!f)return;name=HL.baseName(f.name);try{await HL.need('xlsx');var buf=await HL.read(f);if(/\\.csv$/i.test(f.name)){var b=new Uint8Array(buf),t;try{t=new TextDecoder('utf-8',{fatal:true}).decode(b)}catch(e){t=new TextDecoder('euc-kr').decode(b)}wb=XLSX.read(t.replace(/^\\ufeff/,''),{type:'string'})}else wb=XLSX.read(buf,{type:'array'});
 var sel=$('#sh');sel.innerHTML='';wb.SheetNames.forEach(function(n){sel.appendChild(HL.el('option',{value:n,text:n}))});$('#shw').hidden=wb.SheetNames.length<2;useSheet();$('#st').textContent=''}catch(e){$('#st').textContent='파일을 읽지 못했어요: '+e.message}}
HL.dropzone($('#drop'),{multiple:false,accept:'.xlsx,.xls,.csv',onFiles:add});$('#sh').onchange=useSheet;
$('#paste').addEventListener('input',function(){var t=$('#paste').value;if(!t.trim()){rows=[];show();return}wb=null;$('#shw').hidden=true;name='붙여넣은 표';rows=clean(t.replace(/\\r/g,'').split('\\n').map(function(l){return l.split('\\t')}));show()});
$('#go').onclick=HL.run($('#go'),async function(){var C=rows[0].length,use=rows.slice(0,Math.max(1,Math.floor(MAX/C)));var fmt=$('#fmt').value;
 var r=await HLK.makeTable(use,{title:$('#ti').value.trim(),fmt:fmt,boldHead:$('#bh').checked,onProgress:function(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%'},onCell:async function(a,b){$('#pb').hidden=false;$('#pb i').style.width=Math.round(a/b*100)+'%';$('#st').textContent='칸 채우는 중… '+a+'/'+b;await new Promise(function(x){setTimeout(x,0)})}});
 $('#pb').hidden=true;HL.download(new Blob([r.bytes],{type:HLK.mime[fmt]}),(name||'표')+'.'+fmt);$('#st').textContent=use.length+'줄 표를 '+r.pages+'쪽짜리 .'+fmt+' 파일로 만들었어요.'},'만드는 중…');
})();
</script>""")

T2X_TOOL = ("""<section class="card tool" id="tool">
<div class="drop" id="drop"><b>HWP·HWPX 파일을 놓거나 눌러서 고르세요</b><span>.hwp · .hwpx · 문서 안 표를 모두 찾아요</span></div>
<div id="opt" hidden>
<p class="note" id="info"></p>
<div class="btns"><button class="btn dl" id="go" type="button">엑셀(XLSX)로 받기</button><button class="btn" id="csv" type="button">CSV로 받기</button></div>
<div id="pv"></div>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var h=null,tbs=[];"""+OPEN1+"""
async function add(fs){try{if(h&&h.free)h.free();h=await openOne(fs[0]);tbs=HLK.tables(h);$('#opt').hidden=false;$('#info').textContent=tbs.length?'‘'+h.name+'’에서 표 '+tbs.length+'개를 찾았어요. 엑셀은 표마다 시트 하나로 들어가요.':'이 문서 본문에서 표를 찾지 못했어요. 글상자 안이나 머리말의 표는 읽지 못해요.';$('#go').disabled=$('#csv').disabled=!tbs.length;
 $('#pv').innerHTML=tbs.slice(0,10).map(function(t,i){var g=t.grid;return '<h3>표 '+(i+1)+' · '+g.length+'줄 × '+(g[0]||[]).length+'칸</h3><div class="hk-tbl"><table class="tbl"><tbody>'+g.slice(0,8).map(function(r){return '<tr>'+r.map(function(v){return '<td>'+HL.esc(v).replace(/\\n/g,'<br>')+'</td>'}).join('')+'</tr>'}).join('')+'</tbody></table></div>'+(g.length>8?'<p class="note">… '+(g.length-8)+'줄 더</p>':'')}).join('')}catch(e){$('#pb').hidden=true;$('#st').textContent=e.message}}
HL.dropzone($('#drop'),{multiple:false,accept:'.hwp,.hwpx',onFiles:add});
$('#go').onclick=HL.run($('#go'),async function(){await HL.need('xlsx');var wb=XLSX.utils.book_new();tbs.forEach(function(t,i){XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet(t.grid),'표'+(i+1))});var out=XLSX.write(wb,{bookType:'xlsx',type:'array'});HL.download(new Blob([out],{type:HLK.mime.xlsx}),HL.baseName(h.name)+'_표.xlsx');$('#st').textContent='표 '+tbs.length+'개를 엑셀로 저장했어요.'},'만드는 중…');
$('#csv').onclick=function(){var q=function(v){v=String(v);return /[",\\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};var t=tbs.map(function(tb,i){return (tbs.length>1?'표 '+(i+1)+'\\r\\n':'')+tb.grid.map(function(r){return r.map(q).join(',')}).join('\\r\\n')}).join('\\r\\n\\r\\n');HL.download(new Blob(['\\ufeff'+t],{type:'text/csv;charset=utf-8'}),HL.baseName(h.name)+'_표.csv')};
})();
</script>""")

IX_TOOL = ("""<section class="card tool" id="tool">
<div class="drop" id="drop"><b>HWP·HWPX 파일을 놓거나 눌러서 고르세요</b><span>.hwp · .hwpx · 문서에 넣은 사진·그림을 원본 그대로</span></div>
<div id="opt" hidden>
<p class="note" id="info"></p>
<div class="btns"><button class="btn dl" id="go" type="button">그림 모두 받기 (ZIP)</button></div>
<div class="hk-grid" id="pv"></div>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var h=null,ims=[];"""+OPEN1+"""
function nm(i,im){return HL.baseName(h.name)+'_그림'+String(i+1).padStart(2,'0')+'.'+im.ext}
async function add(fs){try{if(h&&h.free)h.free();h=await openOne(fs[0]);ims=HLK.images(h);$('#opt').hidden=false;$('#go').disabled=!ims.length;
 $('#info').textContent=ims.length?'그림 '+ims.length+'개를 찾았어요. 그림을 누르면 하나씩 받아요.':'본문에서 그림을 찾지 못했어요. 표 칸이나 글상자 안 그림은 아직 꺼내지 못해요.';
 var pv=$('#pv');pv.innerHTML='';ims.forEach(function(im,i){var fg=HL.el('figure');var bl=new Blob([im.bytes],{type:im.mime});if(/png|jpe?g|gif|bmp|webp|svg/.test(im.mime)){var img=HL.el('img',{alt:'그림 '+(i+1)});img.src=URL.createObjectURL(bl);fg.appendChild(img)}else fg.appendChild(HL.el('div',{'class':'note',text:im.ext.toUpperCase()+' 파일'}));fg.appendChild(HL.el('figcaption',{text:(i+1)+' · '+im.ext.toUpperCase()+' · '+HL.bytes(im.bytes.length)}));fg.style.cursor='pointer';fg.onclick=function(){HL.download(bl,nm(i,im))};pv.appendChild(fg)})}catch(e){$('#pb').hidden=true;$('#st').textContent=e.message}}
HL.dropzone($('#drop'),{multiple:false,accept:'.hwp,.hwpx',onFiles:add});
$('#go').onclick=HL.run($('#go'),async function(){await HL.need('jszip');var z=new JSZip();ims.forEach(function(im,i){z.file(nm(i,im),im.bytes)});HL.download(await z.generateAsync({type:'blob'}),HL.baseName(h.name)+'_그림.zip');$('#st').textContent='그림 '+ims.length+'개를 ZIP으로 받았어요.'},'묶는 중…');
})();
</script>""")

PW_TOOL = ("""<section class="card tool" id="tool">
<div style="display:flex;gap:8px;margin-bottom:12px"><button class="hk-chip hk-big" id="mL" type="button" aria-pressed="true">암호 걸기</button><button class="hk-chip hk-big" id="mU" type="button" aria-pressed="false">암호 풀기</button></div>
<div class="drop" id="drop"><b>HWP·HWPX 파일을 놓거나 눌러서 고르세요</b><span id="dsub">.hwp · .hwpx · 암호를 걸 문서</span></div>
<p class="note" id="info"></p>
<div id="opt" hidden>
<div class="grid g2" style="margin-top:8px"><div class="f"><label for="pw">암호</label><input id="pw" type="password" autocomplete="new-password" maxlength="64" placeholder="5자 이상"></div>
<div class="f" id="pw2w"><label for="pw2">암호 한 번 더</label><input id="pw2" type="password" autocomplete="new-password" maxlength="64"></div>
<div class="f" id="fmw"><label for="fmt">저장 형식</label><select id="fmt"><option value="same" selected>원래대로</option><option value="hwp">HWP</option><option value="hwpx">HWPX</option></select></div></div>
<label class="chk" style="margin:6px 0"><input type="checkbox" id="sh"> 암호 보이기</label>
<div class="btns"><button class="btn dl" id="go" type="button">암호 건 파일 받기</button></div>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var mode='lock',file=null,buf=null,kind='';
function setMode(m){mode=m;$('#mL').setAttribute('aria-pressed',m==='lock');$('#mU').setAttribute('aria-pressed',m==='unlock');$('#pw2w').hidden=m!=='lock';$('#fmw').hidden=m!=='lock';$('#go').textContent=m==='lock'?'암호 건 파일 받기':'암호 푼 파일 받기';$('#dsub').textContent=m==='lock'?'.hwp · .hwpx · 암호를 걸 문서':'.hwp · .hwpx · 암호가 걸린 문서 (암호를 알고 있어야 해요)';$('#st').textContent='';$('#pw').value=$('#pw2').value=''}
$('#mL').onclick=function(){setMode('lock')};$('#mU').onclick=function(){setMode('unlock')};
$('#sh').onchange=function(){$('#pw').type=$('#pw2').type=this.checked?'text':'password'};
async function add(fs){file=fs[0];if(!file)return;buf=new Uint8Array(await HL.read(file));kind=buf[0]===0x50&&buf[1]===0x4B?'hwpx':buf[0]===0xD0&&buf[1]===0xCF?'hwp':'';if(!kind){$('#st').textContent='한글(HWP·HWPX) 파일이 아니에요.';$('#opt').hidden=true;return}
 $('#info').textContent='‘'+file.name+'’ · '+HL.bytes(file.size)+' · '+kind.toUpperCase();$('#opt').hidden=false;$('#st').textContent='';$('#pw').focus()}
HL.dropzone($('#drop'),{multiple:false,accept:'.hwp,.hwpx',onFiles:add});
$('#go').onclick=HL.run($('#go'),async function(){var pw=$('#pw').value;if(!pw)throw new Error('암호를 적어 주세요.');
 var m=await HLHWP.load(function(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%';$('#st').textContent='문서 엔진 받는 중… (처음 한 번만)'});$('#pb').hidden=true;var d,out,ext;
 if(mode==='lock'){if([...pw].length<5)throw new Error('암호는 5자 이상으로 해 주세요. 한글 프로그램도 5자 이상만 받아요.');if(pw!==$('#pw2').value)throw new Error('두 번 적은 암호가 달라요.');
  try{d=new m.HwpDocument(buf)}catch(e){throw new Error(/비밀번호|암호/.test(String(e))?'이미 암호가 걸린 문서예요. ‘암호 풀기’에서 먼저 풀어 주세요.':'문서를 읽지 못했어요: '+String(e).slice(0,100))}
  ext=$('#fmt').value==='same'?kind:$('#fmt').value;out=ext==='hwpx'?d.exportHwpxWithPassword(pw):d.exportHwpWithPassword(pw)}
 else{try{d=m.HwpDocument.openWithPassword(buf,pw)}catch(e){throw new Error(/일치/.test(String(e))?'암호가 맞지 않아요. 대소문자·띄어쓰기를 확인해 주세요.':'문서를 열지 못했어요: '+String(e).slice(0,100))}ext=kind;out=ext==='hwpx'?d.exportHwpx():d.exportHwp()}
 try{d.free()}catch(e){}var nm=HL.baseName(file.name)+(mode==='lock'?'_암호':'_암호해제')+'.'+ext;HL.download(new Blob([out],{type:HLK.mime[ext]}),nm);$('#pw').value=$('#pw2').value='';
 $('#st').textContent=(mode==='lock'?'암호를 건 ':'암호를 푼 ')+'‘'+nm+'’을(를) 받았어요. 원본 파일은 그대로 두세요.'},'처리 중…');
setMode('lock');
})();
</script>""")

CMP_TOOL = ("""<section class="card tool" id="tool">
<div class="grid g2"><div><div class="drop" id="dA"><b>원래 문서 (A)</b><span>.hwp · .hwpx</span></div><p class="note" id="nA"></p></div>
<div><div class="drop" id="dB"><b>고친 문서 (B)</b><span>.hwp · .hwpx</span></div><p class="note" id="nB"></p></div></div>
<div id="opt" hidden>
<label class="chk" style="margin:6px 0"><input type="checkbox" id="ws" checked> 띄어쓰기·빈 줄 차이는 무시</label>
<div class="tiles hk-tiles"><div class="tile light"><div class="k">바뀐 줄</div><div class="v" id="cC">0</div></div><div class="tile light"><div class="k">더한 줄 (B에만)</div><div class="v" id="cA">0</div></div><div class="tile light"><div class="k">뺀 줄 (A에만)</div><div class="v" id="cD">0</div></div></div>
<div class="hk-out hk-diff" id="out"></div>
<div class="btns"><button class="btn" id="dl" type="button">비교 결과 TXT로 받기</button></div>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var A=null,B=null,res=[];
async function load(fs,w){try{var h=await HLHWP.open(fs[0],function(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%'});$('#pb').hidden=true;var t=HLK.all(h);var r={name:h.name,n:h.n,t:t};if(h.free)h.free();if(w==='A')A=r;else B=r;$('#n'+w).textContent='‘'+r.name+'’ · '+r.n+'쪽 · '+HLK.fmtN(HLK.stats(t).all)+'자'}catch(e){$('#pb').hidden=true;$('#n'+w).textContent=e.message}run()}
HL.dropzone($('#dA'),{multiple:false,accept:'.hwp,.hwpx',onFiles:function(f){load(f,'A')}});HL.dropzone($('#dB'),{multiple:false,accept:'.hwp,.hwpx',onFiles:function(f){load(f,'B')}});$('#ws').onchange=run;
function lines(t){var ws=$('#ws').checked;var l=HLK.splitText(t);if(ws)l=l.map(function(x){return x.replace(/\\s+/g,' ').trim()}).filter(function(x){return x});return l}
function diff(a,b){var n=a.length,m=b.length;if(n*m>4e6)throw new Error('문서가 너무 길어 비교하지 못했어요 (줄 수 '+n+' × '+m+'). 나눠서 비교해 주세요.');var dp=[];for(var i=0;i<=n;i++){dp.push(new Uint16Array(m+1))}for(i=n-1;i>=0;i--)for(var j=m-1;j>=0;j--)dp[i][j]=a[i]===b[j]?dp[i+1][j+1]+1:Math.max(dp[i+1][j],dp[i][j+1]);
 var out=[];i=0;j=0;while(i<n&&j<m){if(a[i]===b[j]){out.push([0,a[i]]);i++;j++}else if(dp[i+1][j]>=dp[i][j+1]){out.push([-1,a[i]]);i++}else{out.push([1,b[j]]);j++}}while(i<n)out.push([-1,a[i++]]);while(j<m)out.push([1,b[j++]]);return out}
function run(){if(!A||!B){$('#opt').hidden=true;return}try{res=diff(lines(A.t),lines(B.t))}catch(e){$('#st').textContent=e.message;return}$('#opt').hidden=false;
 var add=0,del=0,chg=0;for(var k=0;k<res.length;k++){if(res[k][0]===-1&&res[k+1]&&res[k+1][0]===1){chg++;k++}else if(res[k][0]===1)add++;else if(res[k][0]===-1)del++}
 $('#cC').textContent=HLK.fmtN(chg);$('#cA').textContent=HLK.fmtN(add);$('#cD').textContent=HLK.fmtN(del);
 var html=[],skip=0;res.forEach(function(r,idx){var near=res.slice(Math.max(0,idx-2),idx+3).some(function(x){return x[0]});if(!r[0]&&!near){skip++;return}if(skip){html.push('<div class="hk-skip">… 같은 줄 '+skip+'개 …</div>');skip=0}html.push('<div class="'+(r[0]>0?'hk-add':r[0]<0?'hk-del':'hk-same')+'">'+(r[0]>0?'+ ':r[0]<0?'− ':'  ')+HL.esc(r[1])+'</div>')});if(skip)html.push('<div class="hk-skip">… 같은 줄 '+skip+'개 …</div>');
 $('#out').innerHTML=(add+del+chg)?html.join(''):'<div class="hk-same">두 문서의 글이 같아요.</div>';$('#st').textContent=''}
$('#dl').onclick=function(){var t='A: '+A.name+'\\r\\nB: '+B.name+'\\r\\n\\r\\n'+res.map(function(r){return (r[0]>0?'+ ':r[0]<0?'- ':'  ')+r[1]}).join('\\r\\n');HL.download(new Blob(['\\ufeff'+t],{type:HLK.mime.txt}),'한글문서_비교_'+HL.stamp()+'.txt')};
})();
</script>""")

PRIV_TOOL = ("""<section class="card tool" id="tool">
<div class="drop" id="drop"><b>HWP·HWPX 파일을 놓거나 눌러서 고르세요</b><span>.hwp · .hwpx · 여러 개도 돼요</span></div>
<div id="opt" hidden>
<div class="tiles hk-tiles" id="tl"></div>
<div id="out"></div>
<div class="btns"><button class="btn" id="dl" type="button">가린 글 TXT로 받기</button></div>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var docs=[];
var R=[['jumin','주민등록번호',/(?<!\\d)(\\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\\d|3[01]))\\s?[-–]\\s?([1-8]\\d{6})(?!\\d)/g],
 ['phone','휴대전화',/(?<!\\d)(01[016789])[-.\\s]?(\\d{3,4})[-.\\s]?(\\d{4})(?!\\d)/g],
 ['tel','일반 전화',/(?<!\\d)(0(?:2|[3-6][1-5]|70))[-.)\\s]\\s?(\\d{3,4})[-.\\s](\\d{4})(?!\\d)/g],
 ['mail','이메일',/[\\w.+-]+@[\\w-]+(?:\\.[\\w-]+)+/g],
 ['card','카드번호로 보이는 숫자',/(?<!\\d)\\d{4}[-\\s]\\d{4}[-\\s]\\d{4}[-\\s]\\d{4}(?!\\d)/g],
 ['acct','계좌번호로 보이는 숫자',/(?<![\\d-])\\d{2,6}-\\d{2,6}-\\d{2,7}(?:-\\d{1,3})?(?![\\d-])/g]];
function mask(k,v){if(k==='jumin')return v.replace(/(\\d{6}\\s?[-–]\\s?\\d)\\d{6}/,'$1******');if(k==='mail')return v.replace(/^(.{2})[^@]*/,'$1***');return v.replace(/\\d(?=[\\d\\s.-]{4})/g,function(c,i){return i<3?c:'*'})}
function scan(t){var hits=[],taken=[];R.forEach(function(r){var re=new RegExp(r[2].source,'g'),m;while((m=re.exec(t))){var s=m.index,e=s+m[0].length;if(taken.some(function(x){return s<x[1]&&e>x[0]}))continue;if(r[0]==='acct'&&/^(19|20)\\d\\d-\\d\\d?-\\d\\d?$/.test(m[0]))continue;taken.push([s,e]);var a=t.lastIndexOf('\\n',s)+1,b=t.indexOf('\\n',e);if(b<0)b=t.length;hits.push({k:r[0],nm:r[1],v:m[0],s:s,e:e,line:t.slice(Math.max(a,s-30),Math.min(b,e+30))})}});return hits.sort(function(x,y){return x.s-y.s})}
function show(){$('#opt').hidden=!docs.length;var tot={};docs.forEach(function(d){d.hits.forEach(function(h){tot[h.nm]=(tot[h.nm]||0)+1})});var all=docs.reduce(function(a,d){return a+d.hits.length},0);
 $('#tl').innerHTML='<div class="tile'+(all?'':' light')+'"><div class="k">찾은 개인정보</div><div class="v">'+all+'건</div></div>'+R.filter(function(r){return tot[r[1]]}).map(function(r){return '<div class="tile light"><div class="k">'+r[1]+'</div><div class="v">'+tot[r[1]]+'</div></div>'}).join('');
 $('#out').innerHTML=docs.map(function(d){return '<h3>'+HL.esc(d.name)+' — '+(d.hits.length?d.hits.length+'건':'찾은 것 없음')+'</h3>'+(d.hits.length?'<div class="hk-tbl"><table class="tbl"><thead><tr><th>종류</th><th>가린 값</th><th>앞뒤 글</th></tr></thead><tbody>'+d.hits.slice(0,200).map(function(h){return '<tr><td>'+h.nm+'</td><td>'+HL.esc(mask(h.k,h.v))+'</td><td>'+HL.esc(h.line.split(h.v).join(mask(h.k,h.v)))+'</td></tr>'}).join('')+'</tbody></table></div>':'')}).join('')}
async function add(fs){for(var f of fs){try{var h=await HLHWP.open(f,function(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%'});$('#pb').hidden=true;var t=HLK.all(h);if(h.free)h.free();docs.push({name:f.name,t:t,hits:scan(t)})}catch(e){$('#pb').hidden=true;$('#st').textContent=e.message}}show()}
HL.dropzone($('#drop'),{multiple:true,accept:'.hwp,.hwpx',onFiles:add});
$('#dl').onclick=function(){var out=docs.map(function(d){var t=d.t;d.hits.slice().reverse().forEach(function(h){t=t.slice(0,h.s)+mask(h.k,h.v)+t.slice(h.e)});return (docs.length>1?'['+d.name+']\\r\\n':'')+t}).join('\\r\\n\\r\\n');HL.download(new Blob(['\\ufeff'+out.replace(/\\n/g,'\\r\\n')],{type:HLK.mime.txt}),'개인정보_가린글_'+HL.stamp()+'.txt')};
})();
</script>""")

INFO_TOOL = ("""<section class="card tool" id="tool">
<div class="drop" id="drop"><b>HWP·HWPX 파일을 놓거나 눌러서 고르세요</b><span>.hwp · .hwpx · 버전·쪽 수·글꼴·표·그림 수</span></div>
<div id="opt" hidden>
<div class="tiles hk-tiles" id="tl"></div>
<h3>문서 정보</h3><div class="hk-tbl"><table class="tbl" id="tb"><tbody></tbody></table></div>
<h3>쓴 글꼴</h3><ul class="hk-fonts" id="fl"></ul>
<p class="note">글꼴 이름 옆 ‘대체’는 이 기기에 그 글꼴이 없어 비슷한 글꼴로 그렸다는 뜻이에요. 받는 사람 컴퓨터에도 없으면 모양이 달라질 수 있어요.</p>
</div>
<div class="prog" id="pb" hidden><i></i></div><p class="note" id="st" aria-live="polite"></p>
</section>""", """<script>
(function(){var $=HL.$;var h=null;
var FREE=['함초롬바탕','함초롬돋움','맑은 고딕','굴림','굴림체','돋움','돋움체','바탕','바탕체','궁서','궁서체','나눔고딕','나눔명조','나눔바른고딕','나눔스퀘어','본고딕','본명조','Noto Sans KR','Noto Serif KR','Arial','Times New Roman','Calibri','Cambria','Courier New','Tahoma','Verdana','Segoe UI','Symbol','Wingdings'];
async function add(fs){try{if(h&&h.free)h.free();var f=fs[0];h=await HLHWP.open(f,function(a,b){$('#pb').hidden=false;$('#pb i').style.width=(b?Math.round(a/b*100):30)+'%'});$('#pb').hidden=true;if(!h.doc)throw new Error('문서 엔진으로 읽지 못한 파일이에요.');
 var mi=h.meta||{};var t=HLK.all(h),s=HLK.stats(t),tb=HLK.tables(h),im=HLK.images(h);var p0=h.info(0);var mm=function(px){return Math.round(px*25.4/96)};
 $('#tl').innerHTML=[['쪽',h.n],['글자 (공백 포함)',HLK.fmtN(s.all)],['표',tb.length],['그림',im.length]].map(function(x,i){return '<div class="tile'+(i?' light':'')+'"><div class="k">'+x[0]+'</div><div class="v">'+x[1]+'</div></div>'}).join('');
 var ver=String(mi.version||'');var rows=[['파일',f.name+' ('+HL.bytes(f.size)+')'],['형식',h.kind==='hwpx'?'HWPX (한글 2014 이후 표준 문서)':h.kind==='hwp3'?'HWP 3.0 (아주 옛 형식)':'HWP 5.x (한글 2002 이후 문서)'],['문서 버전',ver||'—'],['구역 수',mi.sectionCount||'—'],['첫 쪽 용지',mm(p0.width)+' × '+mm(p0.height)+'mm'+(Math.abs(mm(p0.width)-210)<=2&&Math.abs(mm(p0.height)-297)<=2?' (A4 세로)':Math.abs(mm(p0.width)-297)<=2&&Math.abs(mm(p0.height)-210)<=2?' (A4 가로)':'')],['공백 제외 글자',HLK.fmtN(s.no)],['200자 원고지',HLK.fmtN(s.ms200)+'장'],['암호',mi.encrypted?'걸려 있음':'없음']];
 $('#tb tbody').innerHTML=rows.map(function(r){return '<tr><th>'+r[0]+'</th><td>'+HL.esc(String(r[1]))+'</td></tr>'}).join('');
 var sub={};(mi.fontSubstitutions||[]).forEach(function(x){if(x&&x.from)sub[x.from]=x.to||true;else if(typeof x==='string')sub[x]=true});
 $('#fl').innerHTML=(mi.fontsUsed||[]).map(function(n){var free=FREE.indexOf(n)>=0;return '<li><b>'+HL.esc(n)+'</b>'+(free?' <span class="note">· 윈도우·한글 기본 글꼴</span>':'')+(sub[n]?' <span class="note">· 대체</span>':'')+'</li>'}).join('')||'<li>글꼴 정보를 찾지 못했어요</li>';
 $('#opt').hidden=false;$('#st').textContent=''}catch(e){$('#pb').hidden=true;$('#st').textContent=e.message}}
HL.dropzone($('#drop'),{multiple:false,accept:'.hwp,.hwpx',onFiles:add});
})();
</script>""")

SC_TOOL = ("""<section class="card tool" id="tool">
<div class="f"><label for="q">기능 이름이나 키로 찾기</label><input id="q" type="search" placeholder="예: 표, 쪽 번호, 저장, Ctrl+N" autocomplete="off"></div>
<div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0" id="cats"></div>
<div class="hk-tbl"><table class="tbl" id="sc"><thead><tr><th>분류</th><th>기능</th><th>단축키</th></tr></thead><tbody><tr data-k="파일 새 문서 Alt+N"><td>파일</td><td>새 문서</td><td><kbd>Alt+N</kbd></td></tr><tr data-k="파일 불러오기(열기) Alt+O"><td>파일</td><td>불러오기(열기)</td><td><kbd>Alt+O</kbd></td></tr><tr data-k="파일 저장하기 Alt+S / Ctrl+S"><td>파일</td><td>저장하기</td><td><kbd>Alt+S / Ctrl+S</kbd></td></tr><tr data-k="파일 다른 이름으로 저장하기 Alt+V"><td>파일</td><td>다른 이름으로 저장하기</td><td><kbd>Alt+V</kbd></td></tr><tr data-k="파일 인쇄 Alt+P / Ctrl+P"><td>파일</td><td>인쇄</td><td><kbd>Alt+P / Ctrl+P</kbd></td></tr><tr data-k="파일 문서 닫기 Ctrl+F4"><td>파일</td><td>문서 닫기</td><td><kbd>Ctrl+F4</kbd></td></tr><tr data-k="파일 한글 끝내기 Alt+X"><td>파일</td><td>한글 끝내기</td><td><kbd>Alt+X</kbd></td></tr><tr data-k="파일 문서마당(서식 고르기) Ctrl+Alt+N"><td>파일</td><td>문서마당(서식 고르기)</td><td><kbd>Ctrl+Alt+N</kbd></td></tr><tr data-k="파일 최근 작업 문서 Alt+F3"><td>파일</td><td>최근 작업 문서</td><td><kbd>Alt+F3</kbd></td></tr><tr data-k="파일 문서 정보 Ctrl+Q, I"><td>파일</td><td>문서 정보</td><td><kbd>Ctrl+Q, I</kbd></td></tr><tr data-k="쪽 쪽 번호 매기기 Ctrl+N, P"><td>쪽</td><td>쪽 번호 매기기</td><td><kbd>Ctrl+N, P</kbd></td></tr><tr data-k="쪽 쪽 번호 등 감추기 Ctrl+N, S"><td>쪽</td><td>쪽 번호 등 감추기</td><td><kbd>Ctrl+N, S</kbd></td></tr><tr data-k="쪽 쪽 나누기 Ctrl+Enter"><td>쪽</td><td>쪽 나누기</td><td><kbd>Ctrl+Enter</kbd></td></tr><tr data-k="쪽 단 나누기 Ctrl+Shift+Enter"><td>쪽</td><td>단 나누기</td><td><kbd>Ctrl+Shift+Enter</kbd></td></tr><tr data-k="쪽 구역 나누기 Alt+Shift+Enter"><td>쪽</td><td>구역 나누기</td><td><kbd>Alt+Shift+Enter</kbd></td></tr><tr data-k="표 표 만들기 Ctrl+N, T"><td>표</td><td>표 만들기</td><td><kbd>Ctrl+N, T</kbd></td></tr><tr data-k="표 셀 블록(현재 칸 고르기) F5"><td>표</td><td>셀 블록(현재 칸 고르기)</td><td><kbd>F5</kbd></td></tr><tr data-k="표 표 나누기 Ctrl+N, A"><td>표</td><td>표 나누기</td><td><kbd>Ctrl+N, A</kbd></td></tr><tr data-k="표 표 붙이기 Ctrl+N, Z"><td>표</td><td>표 붙이기</td><td><kbd>Ctrl+N, Z</kbd></td></tr><tr data-k="표 계산식 Ctrl+N, F"><td>표</td><td>계산식</td><td><kbd>Ctrl+N, F</kbd></td></tr><tr data-k="표 가로 합계 Ctrl+Shift+H"><td>표</td><td>가로 합계</td><td><kbd>Ctrl+Shift+H</kbd></td></tr><tr data-k="표 세로 합계 Ctrl+Shift+V"><td>표</td><td>세로 합계</td><td><kbd>Ctrl+Shift+V</kbd></td></tr><tr data-k="글자 진하게 Ctrl+B / Alt+Shift+B"><td>글자</td><td>진하게</td><td><kbd>Ctrl+B / Alt+Shift+B</kbd></td></tr><tr data-k="글자 기울임 Ctrl+I / Alt+Shift+I"><td>글자</td><td>기울임</td><td><kbd>Ctrl+I / Alt+Shift+I</kbd></td></tr><tr data-k="글자 밑줄 Ctrl+U / Alt+Shift+U"><td>글자</td><td>밑줄</td><td><kbd>Ctrl+U / Alt+Shift+U</kbd></td></tr><tr data-k="글자 위 첨자 Alt+Shift+P"><td>글자</td><td>위 첨자</td><td><kbd>Alt+Shift+P</kbd></td></tr><tr data-k="글자 아래 첨자 Alt+Shift+S"><td>글자</td><td>아래 첨자</td><td><kbd>Alt+Shift+S</kbd></td></tr><tr data-k="글자 보통 모양(꾸밈 지우기) Alt+Shift+C"><td>글자</td><td>보통 모양(꾸밈 지우기)</td><td><kbd>Alt+Shift+C</kbd></td></tr><tr data-k="글자 글자 크게 Alt+Shift+E"><td>글자</td><td>글자 크게</td><td><kbd>Alt+Shift+E</kbd></td></tr><tr data-k="글자 자간 넓히기 Alt+Shift+W"><td>글자</td><td>자간 넓히기</td><td><kbd>Alt+Shift+W</kbd></td></tr><tr data-k="글자 자간 좁히기 Alt+Shift+N"><td>글자</td><td>자간 좁히기</td><td><kbd>Alt+Shift+N</kbd></td></tr><tr data-k="문단 양쪽 정렬 Ctrl+Shift+M"><td>문단</td><td>양쪽 정렬</td><td><kbd>Ctrl+Shift+M</kbd></td></tr><tr data-k="문단 왼쪽 정렬 Ctrl+Shift+L"><td>문단</td><td>왼쪽 정렬</td><td><kbd>Ctrl+Shift+L</kbd></td></tr><tr data-k="문단 가운데 정렬 Ctrl+Shift+C"><td>문단</td><td>가운데 정렬</td><td><kbd>Ctrl+Shift+C</kbd></td></tr><tr data-k="문단 오른쪽 정렬 Ctrl+Shift+R"><td>문단</td><td>오른쪽 정렬</td><td><kbd>Ctrl+Shift+R</kbd></td></tr><tr data-k="문단 배분 정렬 Ctrl+Shift+T"><td>문단</td><td>배분 정렬</td><td><kbd>Ctrl+Shift+T</kbd></td></tr><tr data-k="문단 문단 번호 모양 Ctrl+K, N"><td>문단</td><td>문단 번호 모양</td><td><kbd>Ctrl+K, N</kbd></td></tr><tr data-k="편집 한 줄 지우기 Ctrl+Y"><td>편집</td><td>한 줄 지우기</td><td><kbd>Ctrl+Y</kbd></td></tr><tr data-k="편집 커서 뒤 줄 끝까지 지우기 Alt+Y"><td>편집</td><td>커서 뒤 줄 끝까지 지우기</td><td><kbd>Alt+Y</kbd></td></tr><tr data-k="편집 한 단어 지우기 Ctrl+T"><td>편집</td><td>한 단어 지우기</td><td><kbd>Ctrl+T</kbd></td></tr><tr data-k="편집 문서 처음으로 Ctrl+Page Up"><td>편집</td><td>문서 처음으로</td><td><kbd>Ctrl+Page Up</kbd></td></tr><tr data-k="편집 문서 끝으로 Ctrl+Page Down"><td>편집</td><td>문서 끝으로</td><td><kbd>Ctrl+Page Down</kbd></td></tr><tr data-k="편집 문자표(특수문자) Ctrl+F10"><td>편집</td><td>문자표(특수문자)</td><td><kbd>Ctrl+F10</kbd></td></tr><tr data-k="편집 맞춤법 검사 F8"><td>편집</td><td>맞춤법 검사</td><td><kbd>F8</kbd></td></tr><tr data-k="편집 수식 넣기 Ctrl+N, M"><td>편집</td><td>수식 넣기</td><td><kbd>Ctrl+N, M</kbd></td></tr><tr data-k="편집 차례 새로 고침 Ctrl+K, U"><td>편집</td><td>차례 새로 고침</td><td><kbd>Ctrl+K, U</kbd></td></tr></tbody></table></div>
<p class="note" id="cnt"></p>
<div class="btns"><button class="btn" id="pr" type="button">이 표 인쇄하기</button></div>
</section>""", """<script>
(function(){var $=HL.$;var cat='전체';var trs=[].slice.call(document.querySelectorAll('#sc tbody tr'));var cats=['전체'];trs.forEach(function(t){var c=t.cells[0].textContent;if(cats.indexOf(c)<0)cats.push(c)});
cats.forEach(function(c){var b=HL.el('button',{type:'button','class':'hk-chip','aria-pressed':String(c===cat),text:c});b.onclick=function(){cat=c;[].forEach.call($('#cats').children,function(x){x.setAttribute('aria-pressed',String(x.textContent===c))});f()};$('#cats').appendChild(b)});
function f(){var q=$('#q').value.replace(/\\s+/g,'').toLowerCase(),n=0;trs.forEach(function(t){var ok=(cat==='전체'||t.cells[0].textContent===cat)&&(!q||t.getAttribute('data-k').replace(/\\s+/g,'').toLowerCase().indexOf(q)>=0);t.hidden=!ok;if(ok)n++});$('#cnt').textContent=n+'개 단축키'}
$('#q').addEventListener('input',f);$('#pr').onclick=function(){window.print()};f();
})();
</script>""")


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
      ('표 안의 글자도 나오나요', '<p>네. 표 칸 안 글자도 문서 순서대로 나와요. 다만 칸마다 한 줄씩 나와서, 표 모양 그대로 옮기려면 <a href="/pdf/hwp-viewer.html">HWP 뷰어</a>에서 표를 복사하는 게 좋아요.</p>'),
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
  dict(slug='hwp-to-image', name='HWP 이미지 변환 (한글 파일을 PNG·JPG 그림으로, 쪽마다 한 장)',
    h1='HWP를 <b>그림(PNG·JPG)으로</b>', lead='한글 문서를 쪽마다 PNG나 JPG 그림으로 저장해요. 카톡·블로그·발표 자료에 바로 붙일 수 있어요.',
    desc='한글(.hwp·.hwpx) 문서의 각 쪽을 PNG 또는 JPG 그림으로 저장해요. 크기(보통·선명·인쇄용)와 쪽 범위를 고를 수 있고, 여러 쪽은 ZIP으로 받아요. 한컴오피스 없이 이 기기 안에서만 처리해요.',
    tool=IMG_TOOL, warn='<b>모양은 오픈소스 엔진(rhwp)이 그려요.</b> 기기에 없는 글꼴·수식·차트가 많은 문서는 한컴오피스와 조금 다르게 보일 수 있으니 미리보기로 확인하세요.',
    body=[
      ('한글 파일을 그림으로 바꾸는 경우', '<ul><li>단톡방에 공지문을 <b>파일 대신 그림으로</b> 올려 바로 보이게 할 때 (상대가 한글이 없어도 돼요)</li><li>블로그·카페·인스타에 안내문이나 시간표를 올릴 때</li><li>PPT·발표 자료에 한글 문서의 한 쪽을 그대로 넣을 때</li></ul>'),
      ('PNG와 JPG 중 무엇을 고를까요', '<table class="tbl"><thead><tr><th></th><th>PNG</th><th>JPG</th></tr></thead><tbody><tr><td>글자 선명도</td><td>가장 선명 (번짐 없음)</td><td>조금 번질 수 있음</td></tr><tr><td>용량 (A4 한 쪽, 선명)</td><td>대략 150~600KB</td><td>대략 100~300KB</td></tr><tr><td>추천</td><td>글·표 위주 문서</td><td>사진이 많은 문서, 용량 제한 있는 곳</td></tr></tbody></table><p>‘선명(약 1600px)’이면 휴대전화로 확대해도 글자가 잘 읽혀요. 인쇄할 거면 ‘인쇄용’을 고르세요.</p>'),
      ('사용 방법', '<ol><li>.hwp나 .hwpx 파일을 놓아요. 앞 6쪽이 작은 그림으로 보여요.</li><li>그림 형식·크기를 고르고, 필요한 쪽만 쓰려면 쪽 범위(예: 1-3, 5)를 적어요.</li><li>‘그림으로 저장’을 누르면 한 쪽은 그림 파일 하나, 여러 쪽은 ZIP으로 받아요. 파일 이름에 쪽 번호가 붙어요.</li></ol>'),
    ],
    faq=[('한글 파일을 JPG로 바꾸려면 어떻게 하나요?', '이 페이지에 파일을 놓고 그림 형식에서 JPG를 고른 뒤 ‘그림으로 저장’을 누르면 돼요. 한글 프로그램에서는 [파일] → [인쇄] → 프린터를 ‘그림으로 저장하기’로 골라도 돼요.'),
         ('여러 쪽을 한 장의 긴 그림으로 만들 수 있나요?', '지금은 쪽마다 한 장씩 만들어요. 긴 그림이 필요하면 받은 그림을 이미지 이어 붙이기 도구로 합치세요.'),
         ('배경이 투명한 PNG가 되나요?', '쪽 바탕은 흰색으로 그려져요. 문서 모양 그대로 보이게 하려는 거예요.')]),
  dict(slug='hwp-to-docx', name='HWP 워드 변환 (한글 파일을 워드 DOCX로, 여러 개 한 번에)',
    h1='HWP를 <b>워드(DOCX)로 변환</b>', lead='한글 문서의 글을 워드(.docx) 파일로 옮겨요. 워드만 있는 사람에게 보내거나 구글 문서에서 열 때 써요.',
    desc='한글(.hwp·.hwpx) 문서의 글과 문단을 워드(.docx) 파일로 옮겨요. 여러 파일은 ZIP으로 받고, 워드·구글 문서·페이지스에서 바로 열려요. 한컴오피스 없이 이 기기 안에서만 변환해요.',
    tool=DOCX_TOOL, warn='<b>글과 문단만 옮겨요.</b> 표 칸의 글은 문단으로 들어가고, 글꼴·색·표 테두리·그림은 옮기지 않아요. 모양까지 같아야 하면 한글에서 [다른 이름으로 저장] → 워드 형식을 고르세요.',
    body=[
      ('HWP를 워드로 바꿔야 할 때', '<ul><li>외국 회사·해외 학교처럼 한글(HWP)을 못 여는 곳에 보낼 때</li><li>구글 문서, MS 워드, 맥 페이지스에서 내용을 고쳐야 할 때</li><li>한글 문서 내용을 번역기나 AI 도구에 넣을 때 (대부분 DOCX를 읽어요)</li></ul>'),
      ('무엇이 옮겨지나요', '<table class="tbl"><thead><tr><th>한글 문서의</th><th>워드 파일에서</th></tr></thead><tbody><tr><td>글, 문단, 줄바꿈</td><td>그대로</td></tr><tr><td>표</td><td>칸 글자가 칸마다 한 문단씩 차례대로 (표 모양 X)</td></tr><tr><td>그림·도형</td><td>빠져요 → <a href="/pdf/hwp-image-extract.html">HWP 그림 꺼내기</a>로 따로 받기</td></tr><tr><td>글꼴·크기·색</td><td>워드 기본 글꼴로</td></tr></tbody></table><p>표를 표 그대로 쓰려면 <a href="/pdf/hwp-table-to-excel.html">HWP 표를 엑셀로</a> 뽑은 뒤 워드에 붙여 넣으세요.</p>'),
      ('사용 방법', '<ol><li>.hwp나 .hwpx 파일을 놓아요. 여러 개도 돼요.</li><li>첫 파일의 글 미리보기를 확인해요.</li><li>‘워드(DOCX)로 변환’을 누르면 .docx(여러 개면 ZIP)가 받아져요.</li></ol>'),
    ],
    faq=[('한컴오피스 없이 HWP를 워드로 바꿀 수 있나요?', '네. 이 페이지는 한컴오피스 없이 브라우저에서 글을 뽑아 워드 파일을 만들어요. 파일은 서버로 가지 않아요.'),
         ('한글 프로그램에서 워드로 저장하는 방법은?', '한글에서 [파일] → [다른 이름으로 저장] → 파일 형식에서 ‘MS 워드 문서(*.docx)’를 고르면 모양까지 최대한 맞춰 저장돼요.'),
         ('반대로 워드를 한글로 바꿀 수도 있나요?', '네. <a href="/pdf/text-to-hwp.html">텍스트·워드를 한글 파일로</a>에서 .docx를 넣으면 .hwp로 만들어요.')]),
  dict(slug='excel-to-hwp', name='엑셀 한글 변환 (엑셀·CSV 표를 한글 HWP 표로 만들기)',
    h1='엑셀·CSV를 <b>한글 표로</b>', lead='엑셀(.xlsx)·CSV 표나 복사한 표를 한글(.hwp) 문서의 표로 만들어요. 한컴오피스가 없어도 돼요.',
    desc='엑셀(.xlsx·.xls)·CSV 파일이나 엑셀에서 복사한 표를 한글(.hwp·.hwpx) 문서의 표로 만들어요. 시트를 고르고, 표 위 제목과 굵은 머리글을 넣을 수 있어요. 한컴오피스 없이 이 기기 안에서만 만들어요.',
    tool=X2H_TOOL, warn='<b>칸의 글자만 옮겨요.</b> 엑셀의 색·테두리·병합·수식은 옮기지 않고, 보이는 값(계산 결과)만 한글 표 칸에 넣어요. 칸이 아주 많으면 앞 3,000칸까지만 넣어요.',
    body=[
      ('엑셀 표를 한글 문서로 옮기는 경우', '<ul><li>엑셀로 정리한 명단·일정표를 <b>한글 공문·보고서 양식</b>으로 내야 할 때</li><li>CSV로 받은 자료를 한글 문서로 출력해야 할 때</li><li>한컴오피스가 없는 컴퓨터·휴대전화에서 한글 표 파일이 필요할 때</li></ul>'),
      ('붙여 넣기와 파일 넣기', '<table class="tbl"><thead><tr><th>방법</th><th>이럴 때</th></tr></thead><tbody><tr><td>엑셀에서 범위 복사 → 칸에 붙여 넣기</td><td>표의 일부만 옮길 때 (가장 빠름)</td></tr><tr><td>.xlsx·.xls 파일 놓기</td><td>시트 전체를 옮길 때, 시트가 여러 개일 때</td></tr><tr><td>.csv 파일 놓기</td><td>공공데이터·프로그램에서 받은 자료 (한글 깨짐 자동 처리)</td></tr></tbody></table>'),
      ('사용 방법', '<ol><li>엑셀·CSV 파일을 놓거나 표를 붙여 넣어요.</li><li>앞 12줄 미리보기를 보고, 시트·제목·저장 형식을 골라요.</li><li>‘한글 표로 만들기’를 누르면 표가 든 .hwp 파일이 받아져요. 한글에서 열어 표 너비와 글꼴을 다듬으면 돼요.</li></ol>'),
      ('한글 프로그램이 있다면', '<p>한글에서는 엑셀 범위를 복사해 [편집] → [골라 붙이기] → ‘HTML 형식’으로 붙이면 표로 들어가요. 이 페이지는 한글이 없을 때나 CSV·여러 시트를 정리할 때 편해요.</p>'),
    ],
    faq=[('엑셀을 한글 파일로 변환하면 수식도 옮겨지나요?', '아니요. 수식 결과로 보이는 값만 옮겨요. 한글 표에서 계산이 필요하면 한글의 [표] → [계산식]을 쓰세요.'),
         ('CSV를 열면 한글이 깨져요.', '이 페이지는 UTF-8과 EUC-KR(CP949) CSV를 알아서 구분해 읽어요. 그래도 깨지면 CSV 한글 깨짐 고치기 도구로 먼저 바꿔 보세요.'),
         ('병합된 칸은 어떻게 되나요?', '병합은 풀려서 첫 칸에만 값이 들어가요. 한글에서 칸을 골라 [표] → [셀 합치기]로 다시 합치면 돼요.')]),
  dict(slug='hwp-table-to-excel', name='HWP 표 엑셀 변환 (한글 문서 표를 엑셀 XLSX·CSV로)',
    h1='HWP 표를 <b>엑셀로</b>', lead='한글 문서 안의 표를 찾아 엑셀(.xlsx)이나 CSV로 뽑아요. 표가 여러 개면 표마다 시트 하나로 넣어요.',
    desc='한글(.hwp·.hwpx) 문서 안의 표를 모두 찾아 엑셀(.xlsx) 또는 CSV로 저장해요. 표마다 시트가 하나씩 만들어지고, 칸 안 줄바꿈도 그대로예요. 한컴오피스 없이 이 기기 안에서만 처리해요.',
    tool=T2X_TOOL, warn='',
    body=[
      ('한글 표를 엑셀로 옮기는 경우', '<ul><li>공문으로 받은 <b>명단·예산표·실적표</b>를 엑셀에서 정렬·합계 내야 할 때</li><li>한글 표를 복사해 엑셀에 붙이면 칸이 뒤섞일 때</li><li>한컴오피스가 없는데 HWP 안의 표 숫자가 필요할 때</li></ul>'),
      ('엑셀로 옮기면 어떻게 되나요', '<table class="tbl"><thead><tr><th>한글 표</th><th>엑셀에서</th></tr></thead><tbody><tr><td>칸 글자</td><td>같은 줄·칸 자리에 그대로</td></tr><tr><td>병합된 칸</td><td>왼쪽 위 칸에만 글자 (나머지 빈칸)</td></tr><tr><td>칸 안 줄바꿈</td><td>칸 안 줄바꿈으로 유지</td></tr><tr><td>숫자 1,234</td><td>글자로 들어가요 → 엑셀에서 [데이터] → [텍스트 나누기]로 숫자로 바꾸기</td></tr></tbody></table>'),
      ('사용 방법', '<ol><li>.hwp나 .hwpx 파일을 놓아요. 찾은 표가 앞 8줄씩 보여요.</li><li>엑셀(XLSX)이나 CSV를 골라 받아요. XLSX는 표마다 시트 ‘표1, 표2…’로 들어가요.</li></ol>'),
      ('표를 못 찾을 때', '<p>본문에 바로 놓인 표만 읽어요. <b>글상자 안 표, 머리말·꼬리말 표, 표 안의 표</b>는 아직 못 찾아요. 이럴 때는 <a href="/pdf/hwp-to-txt.html">HWP 텍스트 추출</a>로 글자를 뽑아 쓰세요.</p>'),
    ],
    faq=[('한글 표를 엑셀로 복사하면 칸이 깨져요.', '한글에서 표 전체를 골라 복사한 뒤 엑셀에 붙이면 대부분 되지만, 병합 칸이 많으면 흐트러져요. 이 페이지는 칸 위치를 기준으로 옮겨서 줄·칸이 어긋나지 않아요.'),
         ('여러 표를 한 시트에 모을 수 있나요?', 'CSV로 받으면 표 사이에 ‘표 2’ 같은 줄을 넣어 한 파일에 이어 붙여요.'),
         ('숫자 합계가 안 돼요.', '쉼표가 든 숫자는 글자로 들어가요. 엑셀에서 열을 골라 [데이터] → [텍스트 나누기] → [마침]을 누르면 숫자로 바뀌어요.')]),
  dict(slug='hwp-image-extract', name='HWP 그림 추출 (한글 파일 안 사진·이미지 한 번에 저장)',
    h1='HWP <b>그림 꺼내기</b>', lead='한글 문서에 넣은 사진·그림을 원본 그대로 꺼내요. 하나씩 받거나 ZIP으로 모두 받아요.',
    desc='한글(.hwp·.hwpx) 문서에 들어 있는 사진·그림 파일을 원본 그대로 꺼내요. 그림마다 형식(PNG·JPG 등)과 용량을 보여 주고, 하나씩 또는 ZIP으로 모두 받아요. 한컴오피스 없이 이 기기 안에서만 처리해요.',
    tool=IX_TOOL, warn='',
    body=[
      ('한글 파일 안 그림이 필요할 때', '<ul><li>받은 공문·안내문에 든 <b>사진이나 로고 원본</b>이 필요할 때</li><li>캡처하면 화질이 떨어져서 원래 크기 그대로 받고 싶을 때</li><li>보고서에 넣었던 사진을 다시 모아야 할 때</li></ul>'),
      ('캡처와 무엇이 다른가요', '<table class="tbl"><thead><tr><th></th><th>화면 캡처</th><th>그림 꺼내기</th></tr></thead><tbody><tr><td>화질</td><td>화면 크기만큼 (작아짐)</td><td>넣었던 원본 그대로</td></tr><tr><td>여러 장</td><td>한 장씩</td><td>ZIP으로 한 번에</td></tr><tr><td>파일 형식</td><td>PNG</td><td>원래 형식 (JPG·PNG·BMP·GIF 등)</td></tr></tbody></table>'),
      ('사용 방법', '<ol><li>.hwp나 .hwpx 파일을 놓아요.</li><li>찾은 그림이 작게 보여요. 그림을 누르면 그 그림만 받아요.</li><li>‘그림 모두 받기’를 누르면 ZIP 하나로 받아요.</li></ol>'),
      ('그림이 안 나올 때', '<p>본문에 바로 넣은 그림만 꺼내요. <b>표 칸 안, 글상자 안, 머리말</b>에 든 그림과 한글에서 그린 도형은 아직 못 꺼내요. 그럴 때는 <a href="/pdf/hwp-to-image.html">HWP를 그림으로</a> 쪽 전체를 저장한 뒤 잘라 쓰세요.</p>'),
    ],
    faq=[('WMF·EMF 그림은 어떻게 여나요?', '옛 클립아트에 많은 형식이에요. 윈도우 그림판이나 워드에 넣으면 열리고, 미리보기는 나오지 않아도 받기는 돼요.'),
         ('그림 크기가 문서에서 본 것과 달라요.', '문서에는 줄여서 넣었더라도 원본은 더 클 수 있어요. 꺼낸 파일이 원래 크기예요.')]),
  dict(slug='hwp-password', name='HWP 암호 설정·해제 (한글 문서 비밀번호 걸기·풀기, 설치 없이)',
    h1='HWP <b>암호 걸기·풀기</b>', lead='한글 문서에 열기 암호를 걸거나, 암호를 아는 문서의 암호를 풀어 저장해요. 한컴오피스가 없어도 돼요.',
    desc='한글(.hwp·.hwpx) 문서에 열기 암호(비밀번호)를 걸거나, 암호를 알고 있는 문서의 암호를 풀어 다시 저장해요. 파일과 암호는 서버로 보내지 않고 이 기기 안에서만 처리해요. 잊어버린 암호를 찾아 주는 도구는 아니에요.',
    tool=PW_TOOL, warn='<b>원본 파일은 꼭 따로 두세요.</b> 오픈소스 엔진(rhwp)이 문서를 다시 저장하면서 암호를 걸어요. 중요한 문서는 받은 파일을 한글에서 한 번 열어 암호가 잘 걸렸는지 확인하세요. 암호를 잊으면 아무도 열 수 없어요.',
    body=[
      ('한글 문서에 암호를 거는 경우', '<ul><li>개인정보(주민번호·연락처)가 든 <b>명단·신청서</b>를 메일이나 메신저로 보낼 때</li><li>인사·급여·평가 자료처럼 받는 사람만 봐야 하는 문서</li><li>기관 지침에 ‘개인정보 파일은 암호를 걸어 보내라’고 되어 있을 때</li></ul><p>암호는 메일 본문이 아니라 <b>문자나 전화처럼 다른 길로</b> 알려 주는 게 안전해요.</p>'),
      ('암호 걸기와 풀기', '<table class="tbl"><thead><tr><th></th><th>암호 걸기</th><th>암호 풀기</th></tr></thead><tbody><tr><td>넣는 파일</td><td>암호 없는 HWP·HWPX</td><td>암호가 걸린 HWP·HWPX</td></tr><tr><td>필요한 것</td><td>새 암호 (5자 이상)</td><td>지금 걸린 암호</td></tr><tr><td>받는 파일</td><td>파일이름_암호.hwp</td><td>파일이름_암호해제.hwp</td></tr></tbody></table>'),
      ('사용 방법', '<ol><li>위에서 ‘암호 걸기’ 또는 ‘암호 풀기’를 골라요.</li><li>파일을 놓고 암호를 적어요. 걸 때는 같은 암호를 두 번 적어요.</li><li>버튼을 누르면 새 파일이 받아져요. 원본은 바뀌지 않아요.</li></ol>'),
      ('한글 프로그램에서 직접 걸려면', '<p>한글에서 [보안] → [문서 암호 설정](또는 [파일] → [문서 암호])에서 걸고, 같은 메뉴의 [문서 암호 변경/해제]에서 풀어요. 한글이 없는 컴퓨터나 휴대전화에서는 이 페이지를 쓰면 돼요.</p>'),
    ],
    faq=[('한글 파일 암호를 잊어버렸어요. 풀 수 있나요?', '아니요. 이 페이지는 암호를 아는 문서만 풀 수 있어요. 암호를 찾아 주거나 뚫는 기능은 없고, 그런 방법도 안내하지 않아요. 원본을 만든 사람에게 암호 없는 파일을 다시 받으세요.'),
         ('암호를 걸면 휴대전화에서도 열리나요?', '한컴오피스 뷰어 앱처럼 암호 문서를 지원하는 앱에서 암호를 넣으면 열려요.'),
         ('적은 암호가 어딘가에 저장되나요?', '아니요. 암호와 파일은 이 브라우저 안에서만 쓰이고 서버로 가지 않아요. 파일을 받은 뒤 입력칸도 바로 비워요.'),
         ('배포용 문서(복사·인쇄 막기)도 되나요?', '배포용 문서 설정은 한글 프로그램의 [보안] → [배포용 문서로 저장]에서 해요. 이 페이지는 열기 암호만 다뤄요.')]),
  dict(slug='hwp-compare', name='HWP 문서 비교 (한글 파일 두 개 달라진 곳 찾기)',
    h1='한글 문서 <b>비교</b>', lead='한글 파일 두 개를 놓으면 더한 줄·뺀 줄·바뀐 줄을 색으로 보여 줘요. 수정본에서 무엇이 바뀌었는지 빨리 찾을 때 써요.',
    desc='한글(.hwp·.hwpx) 파일 두 개의 글을 줄 단위로 비교해 더한 줄, 뺀 줄, 바뀐 줄을 색으로 표시해요. 띄어쓰기 차이를 무시할 수 있고 결과를 TXT로 받아요. 한컴오피스 없이 이 기기 안에서만 처리해요.',
    tool=CMP_TOOL, warn='',
    body=[
      ('두 한글 문서를 비교하는 경우', '<ul><li>결재 올린 문서가 <b>수정돼서 돌아왔을 때</b> 어디가 바뀌었는지 볼 때</li><li>계약서·약관의 새 버전에서 달라진 조항을 찾을 때</li><li>공고문·지침의 올해 판과 작년 판을 견줄 때</li></ul>'),
      ('결과 보는 법', '<table class="tbl"><thead><tr><th>표시</th><th>뜻</th></tr></thead><tbody><tr><td><span class="hk-add">+ 파란 줄</span></td><td>고친 문서(B)에만 있는 줄 — 새로 넣었거나 고친 뒤의 줄</td></tr><tr><td><span class="hk-del">− 빨간 줄</span></td><td>원래 문서(A)에만 있는 줄 — 지웠거나 고치기 전의 줄</td></tr><tr><td>… 같은 줄 N개 …</td><td>두 문서가 같은 부분 (접어 둠)</td></tr></tbody></table><p>빨간 줄 바로 다음에 파란 줄이 오면 그 줄을 고친 거예요. 위 숫자의 ‘바뀐 줄’로 세요.</p>'),
      ('사용 방법', '<ol><li>왼쪽(A)에 원래 문서, 오른쪽(B)에 고친 문서를 놓아요.</li><li>두 파일이 다 들어오면 바로 비교 결과가 나와요.</li><li>띄어쓰기만 다른 줄까지 보려면 ‘띄어쓰기·빈 줄 차이는 무시’를 꺼요. 결과는 TXT로 받을 수 있어요.</li></ol>'),
      ('한글 프로그램의 문서 비교와 다른 점', '<p>한글에는 [검토] → [문서 비교] 기능이 있어서 글자 모양까지 비교해요. 이 페이지는 <b>글 내용만</b> 줄 단위로 비교하고, 한글이 없는 컴퓨터·휴대전화에서도 돼요. 표 칸 글자도 칸마다 한 줄로 비교해요.</p>'),
    ],
    faq=[('HWP와 HWPX를 서로 비교할 수 있나요?', '네. 형식이 달라도 글 내용으로 비교해요.'),
         ('글꼴이나 색이 바뀐 것도 찾나요?', '아니요. 글 내용만 비교해요. 모양 변경까지 보려면 한글의 [검토] → [문서 비교]를 쓰세요.'),
         ('아주 긴 문서도 되나요?', '줄 수가 수천 줄씩이면 기기에 따라 느릴 수 있고, 너무 길면 나눠서 비교하라고 알려 줘요.')]),
  dict(slug='hwp-privacy-check', name='HWP 개인정보 검사 (한글 문서 주민번호·전화번호 찾기)',
    h1='HWP <b>개인정보 찾기</b>', lead='한글 문서에 주민등록번호, 전화번호, 이메일, 계좌·카드번호처럼 보이는 글이 있는지 찾아 가려서 보여 줘요. 보내기 전에 한 번 확인하세요.',
    desc='한글(.hwp·.hwpx) 문서에서 주민등록번호, 휴대전화·일반 전화번호, 이메일, 카드·계좌번호처럼 보이는 글을 찾아 가린 값과 앞뒤 글로 보여 줘요. 여러 파일을 한 번에 검사하고 가린 글을 TXT로 받아요. 문서는 서버로 보내지 않아요.',
    tool=PRIV_TOOL, warn='<b>찾는 것은 ‘모양’이에요.</b> 숫자 모양으로 찾기 때문에 개인정보가 아닌 숫자(문서 번호 등)가 잡히거나, 띄어 쓰는 방식이 특이한 번호는 놓칠 수 있어요. 결과를 보고 한글에서 직접 지우거나 가리세요.',
    body=[
      ('보내기 전에 개인정보를 확인하는 이유', '<p>공문·명단·신청서를 다른 기관이나 외부에 보낼 때 <b>주민등록번호 뒷자리나 개인 연락처</b>가 그대로 남아 있으면 개인정보 유출이 돼요. 표 안 깊숙이 들어간 번호는 눈으로 찾기 어려워서, 보내기 전에 한 번 훑어보는 용도로 써요.</p>'),
      ('찾는 개인정보', '<table class="tbl"><thead><tr><th>종류</th><th>찾는 모양 (예)</th><th>가린 모양</th></tr></thead><tbody><tr><td>주민등록번호</td><td>900101-1234567</td><td>900101-1******</td></tr><tr><td>휴대전화</td><td>010-1234-5678</td><td>010-****-5678</td></tr><tr><td>일반 전화</td><td>02-123-4567, 032-123-4567</td><td>02-***-4567</td></tr><tr><td>이메일</td><td>hong@example.com</td><td>ho***@example.com</td></tr><tr><td>카드번호로 보이는 숫자</td><td>1234-5678-1234-5678</td><td>123*-****-****-5678</td></tr><tr><td>계좌번호로 보이는 숫자</td><td>123-456789-01</td><td>가운데 숫자를 *로 가림</td></tr></tbody></table>'),
      ('사용 방법', '<ol><li>.hwp나 .hwpx 파일을 놓아요. 여러 개를 한꺼번에 놓아도 돼요.</li><li>파일마다 찾은 개인정보가 종류·가린 값·앞뒤 글로 나와요. 화면에도 가린 값만 보여요.</li><li>한글에서 그 앞뒤 글로 찾아(Ctrl+F) 지우거나 가려요. 글만 필요하면 ‘가린 글 TXT로 받기’를 눌러요.</li></ol>'),
      ('찾은 뒤 한글에서 가리는 법', '<p>한글의 [편집] → [찾아 바꾸기]에서 번호를 찾아 ‘*’로 바꾸거나, 한글 2018 이후라면 [보안] → [개인 정보 보호하기]로 가릴 수 있어요. 글만 가리면 되는 경우에는 <a href="/text/privacy-mask.html">개인정보 가리기</a> 도구도 쓸 수 있어요.</p>'),
    ],
    faq=[('이 페이지에서 한글 파일 속 번호를 바로 지워 주나요?', '아니요. 원본 한글 파일은 바꾸지 않아요. 어디에 있는지 찾아 주고, 가린 글을 TXT로 받을 수 있어요. 한글 파일 자체는 한글 프로그램에서 고쳐 주세요.'),
         ('그림으로 들어간 주민등록증 사본도 찾나요?', '아니요. 글자로 된 번호만 찾아요. 그림 속 글자는 찾지 못해요.'),
         ('문서 내용이 어디로 전송되나요?', '아니요. 검사는 이 브라우저 안에서만 하고, 문서와 결과는 서버로 가지 않아요.')]),
  dict(slug='hwp-info', name='HWP 문서 정보 확인 (한글 파일 버전·쪽 수·사용 글꼴 보기)',
    h1='한글 문서 <b>정보·글꼴 확인</b>', lead='한글 파일의 형식과 버전, 쪽 수, 용지 크기, 글자 수, 표·그림 개수, 쓴 글꼴을 한눈에 보여 줘요.',
    desc='한글(.hwp·.hwpx) 파일을 놓으면 형식·문서 버전, 쪽 수, 용지 크기, 글자 수, 표와 그림 개수, 문서에 쓴 글꼴 목록을 보여 줘요. 받는 사람 컴퓨터에서 글꼴이 바뀔지 미리 확인할 때 좋아요. 한컴오피스 없이 기기 안에서만 처리해요.',
    tool=INFO_TOOL, warn='',
    body=[
      ('문서 정보를 확인하는 경우', '<ul><li>다른 컴퓨터에서 열었더니 <b>글꼴이 바뀌어 줄이 밀릴 때</b>, 어떤 글꼴을 썼는지 확인</li><li>제출 조건(쪽 수, A4 용지, 글자 수)을 맞췄는지 볼 때</li><li>이 파일이 HWP인지 HWPX인지, 옛 형식인지 알고 싶을 때</li></ul>'),
      ('HWP 형식 구분', '<table class="tbl"><thead><tr><th>표시</th><th>뜻</th></tr></thead><tbody><tr><td>HWP 5.x</td><td>한글 2002 이후의 일반 .hwp 문서</td></tr><tr><td>HWPX</td><td>한글 2014 이후 표준 문서 (2020부터 기본 저장)</td></tr><tr><td>HWP 3.0</td><td>1990년대 옛 문서 — 요즘 한글에서도 열리지만 바꿔 두는 게 좋아요</td></tr></tbody></table>'),
      ('글꼴 목록 보는 법', '<p>‘윈도우·한글 기본 글꼴’이라고 붙은 것(함초롬바탕, 맑은 고딕, 굴림 등)은 대부분 컴퓨터에 있어요. 그 밖의 글꼴은 받는 사람 컴퓨터에 없으면 다른 글꼴로 바뀌어 줄 바꿈과 쪽 나눔이 달라질 수 있어요. 모양을 고정하려면 <a href="/pdf/hwp-to-pdf.html">PDF로 바꿔서</a> 보내세요.</p>'),
      ('사용 방법', '<ol><li>.hwp나 .hwpx 파일을 놓아요.</li><li>위쪽 칸에 쪽·글자·표·그림 수, 아래 표에 형식·버전·용지 크기·암호 여부가 나와요.</li><li>맨 아래에 문서에 쓴 글꼴이 나와요.</li></ol>'),
    ],
    faq=[('한글 프로그램에서 문서 정보는 어디서 보나요?', '[파일] → [문서 정보]에서 일반 정보·문서 요약·문서 통계·글꼴 정보를 볼 수 있어요.'),
         ('작성자 이름 같은 문서 요약도 나오나요?', '지금은 형식·쪽·글자·표·그림·글꼴을 보여 줘요. 작성자·제목 같은 문서 요약은 한글의 [파일] → [문서 정보] → [문서 요약]에서 확인하세요.'),
         ('암호가 걸린 문서도 되나요?', '암호 문서는 내용을 읽을 수 없어요. 먼저 <a href="/pdf/hwp-password.html">HWP 암호 풀기</a>로 푼 뒤 넣으세요.')]),
  dict(slug='hwp-shortcuts', name='한글 단축키 모음 (한컴오피스 표·쪽 번호·저장 단축키 찾기, 인쇄용)',
    h1='한글 <b>단축키 모음</b>', lead='한컴오피스 한글에서 자주 쓰는 단축키를 분류별로 모았어요. 기능 이름으로 찾고, 표로 인쇄할 수 있어요.',
    desc='한컴오피스 한글의 자주 쓰는 단축키를 파일·쪽·표·글자·문단·편집으로 나눠 정리했어요. 표 만들기 Ctrl+N,T, 쪽 번호 Ctrl+N,P, 다른 이름으로 저장 Alt+V처럼 기능 이름으로 찾고 인쇄할 수 있어요. 단축키가 안 먹을 때 확인할 점도 함께 적었어요.',
    tool=SC_TOOL, warn='', nosafe=True,
    body=[
      ('‘Ctrl+N, T’ 같은 겹치는 단축키 누르는 법', '<p>쉼표가 있는 단축키는 <b>두 번에 나눠</b> 눌러요. Ctrl+N, T라면 Ctrl을 누른 채 N을 누르고 손을 뗀 다음, T를 한 번 더 눌러요. 한글에서는 이런 ‘겹글쇠’ 단축키가 많아요.</p>'),
      ('가장 많이 쓰는 한글 단축키 10개', '<table class="tbl"><thead><tr><th>하고 싶은 것</th><th>단축키</th></tr></thead><tbody><tr><td>저장</td><td>Alt+S</td></tr><tr><td>다른 이름으로 저장 (HWPX·PDF로 저장할 때)</td><td>Alt+V</td></tr><tr><td>표 만들기</td><td>Ctrl+N, T</td></tr><tr><td>쪽 번호 넣기</td><td>Ctrl+N, P</td></tr><tr><td>다음 쪽으로 넘기기</td><td>Ctrl+Enter</td></tr><tr><td>표에서 칸 고르기</td><td>F5 (여러 번 누르면 넓어져요)</td></tr><tr><td>가운데 정렬</td><td>Ctrl+Shift+C</td></tr><tr><td>꾸밈 지우고 보통 글자로</td><td>Alt+Shift+C</td></tr><tr><td>특수문자(※ ○ ㉮)</td><td>Ctrl+F10</td></tr><tr><td>맞춤법 검사</td><td>F8</td></tr></tbody></table>'),
      ('단축키가 안 먹을 때', '<ul><li><b>Alt+N이 안 되고 Ctrl+N이 새 문서로 열릴 때</b>: 한글의 단축키 설정이 ‘Office 호환’으로 되어 있는 경우예요. 환경 설정의 단축키 모음을 ‘한컴오피스’로 바꾸면 이 표의 단축키대로 돼요.</li><li><b>Ctrl+Shift 단축키가 안 될 때</b>: 윈도우의 입력 언어 바꾸기 단축키(Ctrl+Shift)와 겹칠 수 있어요. 윈도우 입력 설정에서 바꾸기 키를 다른 것으로 바꿔 보세요.</li><li>한글 버전에 따라 일부 단축키가 다를 수 있어요. 메뉴 오른쪽에 적힌 단축키가 가장 정확해요.</li></ul>'),
      ('한컴오피스 없이 한글 파일을 다룰 때', '<p>한글이 설치되지 않은 컴퓨터나 휴대전화에서는 <a href="/pdf/hwp-viewer.html">HWP 뷰어</a>로 열어 보고, <a href="/pdf/hwp-to-pdf.html">PDF로 바꾸거나</a> <a href="/pdf/hwp-to-txt.html">글만 뽑아</a> 쓸 수 있어요.</p>'),
    ],
    faq=[('한글에서 다른 이름으로 저장 단축키는?', 'Alt+V예요. 파일 형식에서 HWPX·PDF·DOCX 등을 고를 수 있어요.'),
         ('한글 표 만들기 단축키는?', 'Ctrl+N을 누르고 뗀 다음 T를 눌러요(Ctrl+N, T). 줄·칸 수를 정하는 창이 떠요.'),
         ('한글 쪽 번호 넣는 단축키는?', 'Ctrl+N, P예요. 번호 위치와 모양을 고를 수 있어요.'),
         ('이 단축키는 어느 버전 기준인가요?', '한글 2014~2024 등 요즘 버전에서 기본(한컴오피스) 단축키 설정 기준이에요. 설정을 바꿨다면 다를 수 있어요.')],
    src='<li><a href="https://www.goe.go.kr/resource/old/BBSMSTR_000000030111/BBS_202405091213318590.pdf" rel="noopener" target="_blank">경기도교육청 — 한컴오피스 단축키 안내(PDF)</a></li><li><a href="https://www.hancom.com/" rel="noopener" target="_blank">한글과컴퓨터</a> — 프로그램 메뉴에 표시된 단축키</li>'),
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
    sec.append('<h3>참고한 자료</h3><ul class="src">' + (p.get('src') or '<li><a href="https://www.hancom.com/support/downloadCenter/hwpOwpml" rel="noopener" target="_blank">한글과컴퓨터 — 한글 문서 파일 형식 공개</a> — HWP 5.0·HWPX(OWPML) 형식 문서</li>'
               '<li><a href="https://github.com/edwardkim/rhwp" rel="noopener" target="_blank">rhwp (MIT)</a> — 브라우저용 한글 문서 엔진, 0.8.7 사용</li>') + '</ul></section>')
    faq = '<section class="card faq"><h2>자주 묻는 질문</h2>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in p['faq']) + '</section>'
    rel = '<section class="card rel"><h2>다른 한글(HWP) 도구</h2><ul>' + ''.join(
        f'<li><a href="{u}"><b>{t}</b><span>{d}</span></a></li>' for u, t, d in HWP_TOOLS if u != url) + '</ul></section>'
    warn = f'<div class="warn">{p["warn"]}</div>' if p['warn'] else ''
    main = (f'<main class="wrap wide">\n<header class="top"><p class="crumb"><a href="/">홈</a> › <a href="/pdf/">PDF 도구</a> › 한글(HWP)</p>'
            f'<h1>{p["h1"]}</h1><p class="lead">{p["lead"]}</p>{"" if p.get("nosafe") else SAFE}</header>\n{warn}{tool_html}\n' + ''.join(sec) + faq + rel + '\n</main>')
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
