/* 홍라이프 게임 공통 모듈 — 이 기기 순위(localStorage), 결과 대화상자, 결과 공유.
   모든 기록은 이 브라우저에만 저장되며 외부 서버로 보내지 않습니다. */
(function(){
'use strict';
var D=document,W=window,PFX='hlg:';
var GAMES={
  sudoku:{name:'스도쿠',url:'https://honglife.co.kr/games/sudoku.html',asc:false,unit:'점',levels:[['easy','쉬움'],['normal','보통'],['hard','어려움']]},
  omok:{name:'오목',url:'https://honglife.co.kr/games/omok.html',asc:true,unit:'수',levels:[['easy','쉬움'],['normal','보통'],['hard','어려움']]},
  math:{name:'수학 스피드 게임',url:'https://honglife.co.kr/games/math.html',asc:false,unit:'점',levels:[['low','초등 저학년'],['high','초등 고학년'],['mid','중등']]}
};
function sget(k,d){try{var v=W.localStorage.getItem(PFX+k);return v==null?d:JSON.parse(v)}catch(e){return d}}
function sset(k,v){try{W.localStorage.setItem(PFX+k,JSON.stringify(v));return true}catch(e){return false}}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function cleanName(s){
  s=String(s==null?'':s).replace(/[\u0000-\u001f\u007f-\u009f​-‏‪-‮⁠-⁩﻿]/g,'').replace(/\s+/g,' ').trim();
  return Array.from(s).slice(0,12).join('').trim();
}
function fmt(n){return Number(n).toLocaleString('ko-KR')}
function levelName(g,l){var a=GAMES[g].levels;for(var i=0;i<a.length;i++)if(a[i][0]===l)return a[i][1];return l}
function scoreText(g,s){return GAMES[g].unit==='수'?s+'수':fmt(s)+'점'}
function dstr(t){var d=new Date(t);function p(n){return(n<10?'0':'')+n}return String(d.getFullYear()).slice(2)+'.'+p(d.getMonth()+1)+'.'+p(d.getDate())}

var LB={
  all:function(g){var o=sget('lb:'+g,{});return(o&&typeof o==='object')?o:{}},
  list:function(g,l){var a=LB.all(g)[l];return Array.isArray(a)?a.filter(function(e){return e&&typeof e.s==='number'}):[]},
  sort:function(g,a){var asc=GAMES[g].asc;return a.sort(function(x,y){return(asc?x.s-y.s:y.s-x.s)||(x.t-y.t)})},
  add:function(g,l,e){
    var all=LB.all(g),a=LB.list(g,l);
    var ent={id:Date.now().toString(36)+Math.random().toString(36).slice(2,6),n:cleanName(e.n)||'익명',s:e.s,t:Date.now(),x:e.x?String(e.x).slice(0,40):''};
    a.push(ent);LB.sort(g,a);var rank=a.indexOf(ent)+1;a=a.slice(0,10);
    all[l]=a;var ok=sset('lb:'+g,all);
    return{rank:rank<=10?rank:0,total:rank,entry:ent,list:a,saved:ok};
  },
  best:function(g){var r={};GAMES[g].levels.forEach(function(lv){var a=LB.list(g,lv[0]);if(a.length)r[lv[0]]=LB.sort(g,a)[0]});return r},
  clear:function(g){try{W.localStorage.removeItem(PFX+'lb:'+g)}catch(e){}}
};
var NAME={get:function(){var n=sget('name','');return typeof n==='string'?cleanName(n):''},set:function(n){sset('name',cleanName(n))}};

function table(g,l,hid){
  var a=LB.list(g,l);
  if(!a.length)return '<table class="lb"><tbody><tr><td class="empty">아직 기록이 없어요. 첫 기록의 주인공이 되어 보세요.</td></tr></tbody></table>';
  var h='<table class="lb"><thead><tr><th class="rn">순위</th><th>이름</th><th class="sc" style="text-align:right">'+(GAMES[g].asc?'승리 수':'점수')+'</th><th class="dt" style="text-align:right">날짜</th></tr></thead><tbody>';
  LB.sort(g,a).forEach(function(e,i){
    h+='<tr'+(e.id===hid?' class="me"':'')+'><td class="rn"><span class="medal'+(i<3?' m'+(i+1):'')+'">'+(i+1)+'</span></td><td class="nm">'+esc(e.n)+(e.x?'<small>'+esc(e.x)+'</small>':'')+'</td><td class="sc">'+esc(scoreText(g,e.s))+'</td><td class="dt">'+dstr(e.t)+'</td></tr>';
  });
  return h+'</tbody></table>';
}

/* 페이지 안의 '이 기기 순위' 영역: <div data-lb="game"></div> */
function mountBoard(el,g,cur){
  var lv=cur||GAMES[g].levels[0][0];
  function draw(hid){
    var tabs='<div class="seg" role="group" aria-label="순위 구분">'+GAMES[g].levels.map(function(x){return '<button type="button" data-l="'+x[0]+'" aria-pressed="'+(x[0]===lv)+'">'+x[1]+'</button>'}).join('')+'</div>';
    el.innerHTML=tabs+table(g,lv,hid)+'<button type="button" class="linkbtn" data-clear>이 기기 기록 모두 지우기</button>';
  }
  el.addEventListener('click',function(ev){
    var b=ev.target.closest('button');if(!b)return;
    if(b.dataset.l){lv=b.dataset.l;draw()}
    else if(b.hasAttribute('data-clear')){if(W.confirm(GAMES[g].name+' 기록을 이 기기에서 모두 지울까요?')){LB.clear(g);draw()}}
  });
  draw();
  return{show:function(l,hid){lv=l;draw(hid)}};
}

var toastT;
function toast(m){var t=D.querySelector('.gtoast');if(!t){t=D.createElement('div');t.className='gtoast';t.setAttribute('role','status');D.body.appendChild(t)}t.textContent=m;t.hidden=false;clearTimeout(toastT);toastT=setTimeout(function(){t.hidden=true},2600)}
function copyText(s){
  function legacy(){var a=D.createElement('textarea');a.value=s;a.setAttribute('readonly','');a.style.cssText='position:fixed;top:0;left:0;opacity:0';D.body.appendChild(a);a.select();var ok=false;try{ok=D.execCommand('copy')}catch(e){}D.body.removeChild(a);return ok}
  if(navigator.clipboard&&navigator.clipboard.writeText){return navigator.clipboard.writeText(s).then(function(){return true},function(){return legacy()})}
  return Promise.resolve(legacy());
}
function share(text,url){
  var full=text+'\n'+url;
  if(navigator.share){
    return navigator.share({title:'홍라이프 게임',text:text,url:url}).catch(function(e){if(e&&e.name==='AbortError')return;return copyText(full).then(function(ok){toast(ok?'결과를 복사했어요.':'복사하지 못했어요.')})});
  }
  return copyText(full).then(function(ok){toast(ok?'결과를 복사했어요. 원하는 곳에 붙여 넣으세요.':'복사하지 못했어요.')});
}

/* 결과 대화상자
   o:{game,level,score,title,facts:[[라벨,값]],save:true|false,extra:'',shareLine:'',onAgain:fn,board:{show}} */
function result(o){
  var g=GAMES[o.game],old=D.querySelector('.gdlg');if(old)old.remove();
  var last=D.activeElement,savedEnt=null;
  var wrap=D.createElement('div');wrap.className='gdlg';
  wrap.innerHTML='<div class="box" role="dialog" aria-modal="true" aria-labelledby="gdT" tabindex="-1">'+
   '<div class="hd"><button type="button" class="x" data-a="close" aria-label="닫기">×</button><p class="eb">'+esc(g.name)+(o.level?' · '+esc(levelName(o.game,o.level)):'')+'</p><h2 id="gdT">'+esc(o.title)+'</h2>'+
   (o.score!=null?'<div class="score">'+(g.unit==='수'?esc(o.score)+'<span>수 승리</span>':esc(fmt(o.score))+'<span>점</span>')+'</div>':'')+'</div>'+
   (o.facts&&o.facts.length?'<dl class="facts">'+o.facts.map(function(f){return '<div><dt>'+esc(f[0])+'</dt><dd>'+esc(f[1])+'</dd></div>'}).join('')+'</dl>':'')+
   '<div class="bd">'+
   (o.save?'<form class="sv" novalidate><label for="gdN">이름 또는 아이디 <span class="tag">이 기기 순위</span></label><div class="row"><input id="gdN" name="n" maxlength="12" autocomplete="nickname" enterkeyhint="done" placeholder="최대 12자" value="'+esc(NAME.get())+'"><button class="btn gold" type="submit">기록 저장</button></div><p class="note" style="margin:6px 0 0">기록은 이 기기(브라우저)에만 저장돼요. 서버로 보내지 않아요.</p></form><div class="done" hidden></div>':(o.note?'<p class="note" style="margin:10px 0 0;text-align:center">'+esc(o.note)+'</p>':''))+
   '</div><div class="acts"><button type="button" class="btn gold" data-a="again">다시 하기</button><button type="button" class="btn ghost" data-a="share">결과 공유</button><button type="button" class="btn ghost wide" data-a="close">닫기</button></div></div>';
  D.body.appendChild(wrap);
  var box=wrap.querySelector('.box');
  function close(){wrap.remove();D.removeEventListener('keydown',onKey);try{last&&last.focus&&last.focus({preventScroll:true})}catch(e){}}
  function onKey(e){if(e.key==='Escape')close()}
  D.addEventListener('keydown',onKey);
  var form=wrap.querySelector('form.sv');
  if(form)form.addEventListener('submit',function(e){
    e.preventDefault();
    var inp=form.querySelector('input'),n=cleanName(inp.value);
    if(!n){inp.focus();toast('이름이나 아이디를 입력해 주세요.');return}
    NAME.set(n);
    var r=LB.add(o.game,o.level,{n:n,s:o.score,x:o.extra});savedEnt=r.entry;
    var done=wrap.querySelector('.done');form.hidden=true;done.hidden=false;
    done.innerHTML='<div class="rk">'+(r.saved?(r.rank?esc(n)+' 님, 이 기기 순위 '+r.rank+'위!':'이 기기 순위 10위 밖이에요. 다시 도전해 보세요!'):'이 브라우저에서는 저장할 수 없어요(저장소 차단).')+'</div>'+table(o.game,o.level,r.entry.id);
    if(o.board)o.board.show(o.level,r.entry.id);
  });
  wrap.addEventListener('click',function(e){
    if(e.target===wrap){close();return}
    var b=e.target.closest('[data-a]');if(!b)return;var a=b.dataset.a;
    if(a==='close')close();
    else if(a==='again'){close();o.onAgain&&o.onAgain()}
    else if(a==='share'){
      var nm=savedEnt?savedEnt.n:(form?cleanName(form.querySelector('input').value):'');
      var t='[홍라이프 '+g.name+'] '+(o.level?levelName(o.game,o.level)+' · ':'')+(o.shareLine||(o.score!=null?scoreText(o.game,o.score):o.title))+(nm?' · '+nm:'');
      share(t,g.url);
    }
  });
  setTimeout(function(){var bt=form&&NAME.get()?form.querySelector('button'):null;(bt||box).focus({preventScroll:true})},30);
  return{close:close};
}

W.HLG={games:GAMES,lb:LB,name:NAME,esc:esc,cleanName:cleanName,fmt:fmt,levelName:levelName,scoreText:scoreText,mountBoard:mountBoard,result:result,share:share,toast:toast,store:{get:sget,set:sset}};
})();
