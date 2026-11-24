#!/usr/bin/env python3
"""한글(HWP) 도구 페이지 만들기 — build/hwp/template.html(HWP→PDF 페이지)의 틀을 빌려 overlay/pdf/*.html 을 써요.
로컬에서 한 번 돌리고 결과(overlay)를 커밋해요:  python3 build/hwp/gen_hwp_tools.py"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TPL = open(os.path.join(ROOT, 'build/hwp/template.html'), encoding='utf-8').read()
OUT = os.path.join(ROOT, 'overlay/pdf')
SITE = 'https://honglife.co.kr'
KIT = '<script src="/assets/js/hlhwpkit.js?v=6"></script>'
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
    ('/doc/gongmun-checker.html', '공문서 오류 검사기', 'HWP 공문 맞춤법·서식 점검'),
]

FILE_TOOL_CSS = '<style>.hk-out{white-space:pre-wrap;word-break:break-all;overflow-wrap:anywhere;max-height:420px;overflow:auto;background:#F7F8FA;border:1px solid #E3E6EB;border-radius:12px;padding:12px 14px;font-size:15px;line-height:1.7;margin-top:10px}.hk-tiles{margin-top:10px}#tool textarea{width:100%;box-sizing:border-box}.hk-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin-top:8px}.hk-grid figure{margin:0;border:1px solid #E3E6EB;border-radius:10px;padding:6px;background:#fff;text-align:center;min-width:0}.hk-grid canvas,.hk-grid img{max-width:100%;height:auto;display:block;margin:0 auto}.hk-grid figcaption{font-size:13px;color:#5B6B82;margin-top:4px;overflow-wrap:anywhere}.hk-tbl{overflow-x:auto;margin-top:8px}.hk-tbl td,.hk-tbl th{white-space:nowrap;max-width:240px;overflow:hidden;text-overflow:ellipsis}</style>'


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
