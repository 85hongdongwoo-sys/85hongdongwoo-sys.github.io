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
K.all=function(h){if(h.fallback)return h.fallback.map(function(p){return p.t}).join('\n');var a=[];for(var i=0;i<h.n;i++)a.push(K.pt(h,i).replace(/\n+$/,''));return a.join('\n\n')};
K.fmtN=function(n){return Number(n).toLocaleString('ko-KR')};
})();
