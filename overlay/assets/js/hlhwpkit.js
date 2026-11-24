/* hlhwpkit.js — 한글(HWP·HWPX) 변환 도구 공용. hlhwp.js(엔진 rhwp) 위에서 동작, 모두 브라우저 안에서.
   HLK.save(h,'hwp'|'hwpx')      → Uint8Array (열린 문서를 다른 형식으로 저장)
   HLK.make(paras,{fmt,title})    → Uint8Array (문단 배열로 새 한글 문서 만들기, 첫 줄 제목 굵게)
   HLK.readText(file)            → 문단 배열 (.txt .md .docx .hwp .hwpx)
   HLK.stats(text)               → {all,no,words,lines,paras,b2,ms200} */
(function(){'use strict';var K=window.HLK={};
var MIME={hwp:'application/x-hwp',hwpx:'application/hwp+zip',txt:'text/plain;charset=utf-8'};K.mime=MIME;
K.save=function(h,to){if(!h||!h.doc)throw new Error('문서 엔진으로 열지 못한 파일이라 바꿀 수 없어요.');
  try{return to==='hwpx'?h.doc.exportHwpx():h.doc.exportHwp()}catch(e){throw new Error('저장하지 못했어요: '+String(e&&e.message||e).slice(0,140))}};
K.make=async function(paras,o){o=o||{};var m=await HLHWP.load(o.onProgress);var d=m.HwpDocument.createEmpty();d.createBlankDocument();
  paras=(paras||[]).map(function(s){return String(s).replace(/[\r\t]/g,function(c){return c==='\t'?'    ':''})});if(!paras.length)paras=[''];
  var p=0;for(var i=0;i<paras.length;i++){var s=paras[i];if(s)d.insertText(0,p,0,s);
    if(i===0&&o.title&&s){try{d.applyCharFormat(0,0,0,[...s].length,JSON.stringify({bold:true,fontSize:1500}))}catch(e){}}
    if(i<paras.length-1){var r=JSON.parse(d.splitParagraph(0,p,[...s].length));p=r.paraIdx}}
  var out=o.fmt==='hwpx'?d.exportHwpx():d.exportHwp();var n=d.pageCount();try{d.free()}catch(e){}return{bytes:out,pages:n}};
K.splitText=function(t){return String(t||'').replace(/\r\n?/g,'\n').replace(/ /g,' ').split('\n')};
K.docx=async function(file){await HL.need('jszip');var z=await JSZip.loadAsync(await HL.read(file));var f=z.file('word/document.xml');if(!f)throw new Error('워드(.docx) 본문을 찾지 못했어요.');
  var xml=new DOMParser().parseFromString(await f.async('string'),'application/xml');var ps=xml.getElementsByTagNameNS('*','p'),out=[];
  for(var i=0;i<ps.length;i++){var p=ps[i],s='';var w=document.createTreeWalker(p,NodeFilter.SHOW_ELEMENT);var n;while((n=w.nextNode())){if(n.localName==='t')s+=n.textContent;else if(n.localName==='tab')s+='    ';else if(n.localName==='br')s+='\n'}out.push(s)}return out};
K.readText=async function(file,onProgress){var nm=(file.name||'').toLowerCase();
  if(/\.docx$/.test(nm))return K.docx(file);
  if(/\.(hwp|hwpx)$/.test(nm)){var h=await HLHWP.open(file,onProgress);var t=K.all(h);if(h.free)h.free();return K.splitText(t)}
  if(/\.doc$/.test(nm))throw new Error('예전 워드(.doc)는 읽지 못해요. 워드에서 .docx로 저장한 뒤 넣어 주세요.');
  var buf=new Uint8Array(await HL.read(file));var t;try{t=new TextDecoder('utf-8',{fatal:true}).decode(buf)}catch(e){t=new TextDecoder('euc-kr').decode(buf)}
  return K.splitText(t.replace(/^﻿/,''))};
K.stats=function(t){t=String(t||'').replace(/\r\n?/g,'\n');var noNl=t.replace(/\n/g,'');var b2=0;for(var c of noNl)b2+=c.charCodeAt(0)>127?2:1;
  var lines=t?t.split('\n').length:0;var paras=t.split(/\n\s*\n+/).filter(function(x){return x.trim()}).length;
  return{all:[...noNl].length,no:[...noNl.replace(/\s/g,'')].length,words:(t.match(/\S+/g)||[]).length,lines:lines,paras:paras,b2:b2,ms200:Math.ceil([...noNl].length/200)}};
/* rhwp getPageText는 JSON 문자열(따옴표·\\n 포함)로 돌려줄 때가 있어 풀어 줘요 */
K.pt=function(h,i){var t=h.text(i);if(/^\s*"/.test(t)){try{t=JSON.parse(t.trim())}catch(e){}}return String(t).replace(/\r\n?/g,'\n')};
K.all=function(h){if(h.fallback)return h.fallback.map(function(p){return p.t}).join('\n');if(h.doc&&h.doc.getTextFileText){try{var t=String(h.doc.getTextFileText());if(/^\s*"/.test(t))t=JSON.parse(t.trim());t=t.replace(/\r\n?/g,'\n');if(t.trim())return t.replace(/\n+$/,'')}catch(e){}}/* 문서 전체 글(표 칸 포함) */var a=[];for(var i=0;i<h.n;i++)a.push(K.pt(h,i).replace(/\n+$/,''));return a.join('\n\n')};

/* 표 읽기: 본문 맨 바깥 표 → [{sec,para,grid:[[칸 글자]]}] */
K.tables=function(h){var d=h&&h.doc;if(!d)return[];var out=[];var cs=[];try{cs=JSON.parse(d.getControls())}catch(e){}
  cs.forEach(function(c){if(c.ctrlId!=='tbl')return;var s=c.list||0,p=c.para,k=c.controlIndex;try{var dim=JSON.parse(d.getTableDimensions(s,p,k));var g=[];for(var r=0;r<dim.rowCount;r++){g.push(new Array(dim.colCount).fill(''))}
    for(var ci=0;ci<dim.cellCount;ci++){var inf=JSON.parse(d.getCellInfo(s,p,k,ci));var n=d.getCellParagraphCount(s,p,k,ci),ps=[];for(var j=0;j<n;j++){var L=d.getCellParagraphLength(s,p,k,ci,j);ps.push(L?d.getTextInCell(s,p,k,ci,j,0,L):'')}if(g[inf.row])g[inf.row][inf.col]=ps.join('\n').trim()}
    out.push({sec:s,para:p,grid:g})}catch(e){}});return out};
/* 그림 꺼내기: 본문 맨 바깥 그림 개체 → [{mime,ext,bytes}] */
K.images=function(h){var d=h&&h.doc;if(!d)return[];var out=[],cs=[];try{cs=JSON.parse(d.getControls())}catch(e){}
  cs.forEach(function(c){if(/^(secd|cold|tbl|pgnp|head|foot|fn|en|atno|nwno|pghd|bokm|%)/.test(c.ctrlId))return;try{var m=d.getControlImageMime(c.list||0,c.para,'[]',c.controlIndex);if(!m)return;var b=d.getControlImageData(c.list||0,c.para,'[]',c.controlIndex);if(b&&b.length){var ext=(m.split('/')[1]||'bin').replace('jpeg','jpg').replace('x-wmf','wmf').replace('x-emf','emf').replace('svg+xml','svg');out.push({mime:m,ext:ext,bytes:b})}}catch(e){}});return out};
/* 표 한 개짜리 한글 문서 만들기 (첫 줄 제목) */
K.makeTable=async function(rows,o){o=o||{};var m=await HLHWP.load(o.onProgress);var d=m.HwpDocument.createEmpty();d.createBlankDocument();
  var title=o.title||'';d.insertText(0,0,0,title||' ');if(title){try{d.applyCharFormat(0,0,0,[...title].length,JSON.stringify({bold:true,fontSize:1400}))}catch(e){}}
  d.splitParagraph(0,0,[...(title||' ')].length);var R=rows.length,C=Math.max.apply(null,rows.map(function(r){return r.length}));var T=JSON.parse(d.createTable(0,1,0,R,C));
  for(var r=0;r<R;r++)for(var c=0;c<C;c++){var v=rows[r][c];v=v==null?'':String(v).replace(/[\r\n\t]+/g,' ');if(v)d.insertTextInCell(0,T.paraIdx,T.controlIdx||0,r*C+c,0,0,v);if(o.onCell&&(r*C+c)%200===0)await o.onCell(r*C+c,R*C)}
  if(o.boldHead){for(var c2=0;c2<C;c2++){try{var L=[...String(rows[0][c2]||'')].length;if(L)d.applyCharFormatInCell(0,T.paraIdx,T.controlIdx||0,c2,0,0,L,JSON.stringify({bold:true}))}catch(e){}}}
  var out=o.fmt==='hwpx'?d.exportHwpx():d.exportHwp();var n=d.pageCount();try{d.free()}catch(e){}return{bytes:out,pages:n}};
/* 문단 배열 → 아주 단순한 워드(.docx) */
K.docxFrom=async function(paras,title){await HL.need('jszip');var z=new JSZip();var esc=function(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g,'')};
  var body=paras.map(function(t){return '<w:p><w:r><w:t xml:space="preserve">'+esc(t)+'</w:t></w:r></w:p>'}).join('');
  z.file('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>');
  z.file('_rels/.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>');
  z.file('docProps/core.xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>'+esc(title||'')+'</dc:title><dc:creator>홍라이프 도구</dc:creator></cp:coreProperties>');
  z.file('word/document.xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'+body+'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1701" w:right="1440" w:bottom="1440" w:left="1440" w:header="851" w:footer="992" w:gutter="0"/></w:sectPr></w:body></w:document>');
  return z.generateAsync({type:'uint8array',mimeType:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})};
K.mime.docx='application/vnd.openxmlformats-officedocument.wordprocessingml.document';K.mime.xlsx='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
K.fmtN=function(n){return Number(n).toLocaleString('ko-KR')};
})();
