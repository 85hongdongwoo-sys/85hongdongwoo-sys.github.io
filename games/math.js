/* 홍라이프 수학 스피드 게임 — 60초 암산 */
(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
var LV={low:{n:'초등 저학년',base:10,neg:false},high:{n:'초등 고학년',base:15,neg:false},mid:{n:'중등',base:20,neg:true}};
var CFG={dur:60000};
var M='−';
function R(a,b){return a+Math.floor(Math.random()*(b-a+1))}
function pick(a){return a[Math.random()*a.length|0]}
function par(n){return n<0?'('+M+(-n)+')':String(n)}
function num(n){return n<0?M+(-n):String(n)}
function gen(l){
  var a,b,c,q;
  if(l==='low'){
    if(Math.random()<.5){a=R(1,19);b=R(1,20-a);return{q:a+' + '+b,a:a+b}}
    a=R(2,20);b=R(1,a);return{q:a+' '+M+' '+b,a:a-b};
  }
  if(l==='high'){
    switch(pick(['mul','mul','div','add','sub'])){
      case'mul':a=R(2,9);b=R(2,9);return{q:a+' × '+b,a:a*b};
      case'div':b=R(2,9);q=R(2,9);return{q:(b*q)+' ÷ '+b,a:q};
      case'add':a=R(10,89);b=R(10,99-a>10?99-a:10);if(Math.random()<.5)b=R(10,99);return{q:a+' + '+b,a:a+b};
      default:a=R(20,99);b=R(10,a-1);return{q:a+' '+M+' '+b,a:a-b};
    }
  }
  function nz(x,y){var v=0;while(!v)v=R(x,y);return v}
  switch(pick(['neg','neg','ord','ord','par','div'])){
    case'neg':a=nz(-20,20);b=nz(-20,20);
      if(Math.random()<.5)return{q:num(a)+' + '+par(b),a:a+b};
      return{q:num(a)+' '+M+' '+par(b),a:a-b};
    case'ord':a=R(1,30);b=R(2,9);c=R(2,9);
      switch(R(0,2)){case 0:return{q:a+' + '+b+' × '+c,a:a+b*c};case 1:return{q:a+' '+M+' '+b+' × '+c,a:a-b*c};default:return{q:b+' × '+c+' '+M+' '+a,a:b*c-a}}
    case'par':a=R(1,12);b=R(1,12);c=nz(-6,9);
      if(Math.random()<.5)return{q:'('+a+' + '+b+') × '+par(c),a:(a+b)*c};
      return{q:'('+a+' '+M+' '+b+') × '+par(c),a:(a-b)*c};
    default:b=nz(-9,9);q=nz(-9,9);if(Math.abs(b)===1)b=b*R(2,9);return{q:par(b*q)+' ÷ '+par(b),a:q};
  }
}
var lv='low',S=null,raf=0,board=HLG.mountBoard($('lb'),'math','low');
function setLv(l){lv=l;document.querySelectorAll('#lvl button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===l)});$('kneg').hidden=!LV[l].neg;$('kclr').hidden=LV[l].neg;board.show(l)}
document.querySelectorAll('#lvl button').forEach(function(b){b.onclick=function(){if(S&&S.on)return;setLv(b.dataset.l)}});
function show(id){['intro','game'].forEach(function(x){$(x).hidden=x!==id})}
function start(){
  S={lv:lv,on:false,score:0,ok:0,bad:0,combo:0,maxc:0,input:'',cur:null,t0:0,last:''};
  show('game');$('ans').textContent='';$('fb').textContent='';$('fb').className='fb';$('q').textContent='';
  hud();var box=$('mpanel');try{box.scrollIntoView({block:'start',behavior:'smooth'})}catch(e){}
  var n=3;$('q').innerHTML='<span class="cd">'+n+'</span>';
  var iv=setInterval(function(){n--;if(n>0){$('q').innerHTML='<span class="cd">'+n+'</span>'}else{clearInterval(iv);S.on=true;S.t0=performance.now();next();loop()}},CFG.dur<60000?50:650);
}
function next(){var p;do{p=gen(S.lv)}while(p.q===S.last);S.last=p.q;S.cur=p;S.input='';$('q').textContent=p.q+' = ?';$('ans').textContent='';$('ans').classList.remove('neg')}
function left(){return Math.max(0,CFG.dur-(performance.now()-S.t0))}
function loop(){
  if(!S||!S.on)return;var l=left();
  $('tl').textContent=Math.ceil(l/1000);$('bar').style.transform='scaleX('+(l/CFG.dur)+')';$('bar').classList.toggle('low',l<10000);
  if(l<=0){finish();return}raf=requestAnimationFrame(loop);
}
function hud(){$('scv').textContent=HLG.fmt(S.score);$('cb').textContent=S.combo>1?'×'+(1+0.1*Math.min(S.combo-1,10)).toFixed(1):'×1.0';$('okc').textContent=S.ok}
function flash(ok,t){var f=$('fb');f.textContent=t;f.className='fb '+(ok?'ok':'bad');var p=$('qbox');p.classList.remove('ok','bad');void p.offsetWidth;p.classList.add(ok?'ok':'bad')}
function judge(force){
  if(!S||!S.on||!S.cur)return;var v=S.input===''||S.input==='-'?null:parseInt(S.input,10);
  if(v===S.cur.a){
    S.ok++;S.combo++;S.maxc=Math.max(S.maxc,S.combo);
    var pts=Math.round(LV[S.lv].base*(1+0.1*Math.min(S.combo-1,10)));S.score+=pts;
    flash(true,'정답! +'+pts+(S.combo>1?' · '+S.combo+'콤보':''));hud();next();
  }else if(force){
    if(v===null)return;
    S.bad++;S.combo=0;flash(false,'아쉬워요. 정답은 '+num(S.cur.a));hud();next();
  }
}
function key(k){
  if(!S||!S.on)return;
  if(k==='ok'){judge(true);return}
  if(k==='bk')S.input=S.input.slice(0,-1);
  else if(k==='clr')S.input='';
  else if(k==='neg')S.input=S.input.charAt(0)==='-'?S.input.slice(1):'-'+S.input;
  else if(S.input.replace('-','').length<5)S.input+=k;
  $('ans').textContent=S.input.replace('-',M);
  judge(false);
}
function finish(){
  S.on=false;cancelAnimationFrame(raf);$('tl').textContent='0';$('bar').style.transform='scaleX(0)';
  var tot=S.ok+S.bad,acc=tot?Math.round(S.ok/tot*100):0;
  $('q').textContent='끝!';$('ans').textContent='';
  HLG.result({game:'math',level:S.lv,score:S.score,title:S.ok>=20?'대단해요!':S.ok>=10?'잘했어요!':'수고했어요!',save:true,board:board,
    facts:[['정답',S.ok+'개'],['정확도',acc+'%'],['최대 콤보',S.maxc]],extra:'정답 '+S.ok+' · 정확도 '+acc+'%',
    shareLine:HLG.fmt(S.score)+'점 (60초에 '+S.ok+'문제, 정확도 '+acc+'%)',onAgain:start});
  setTimeout(function(){show('intro')},300);
}
$('pad').addEventListener('click',function(e){var b=e.target.closest('[data-k]');if(b)key(b.dataset.k)});
$('go').onclick=start;
$('quit').onclick=function(){if(S&&S.on&&confirm('게임을 그만둘까요? 기록은 남지 않아요.')){S.on=false;cancelAnimationFrame(raf);show('intro')}};
document.addEventListener('keydown',function(e){
  if(!S||!S.on||e.target.closest('input,textarea,.gdlg'))return;var k=e.key;
  if(/^[0-9]$/.test(k))key(k);else if(k==='Backspace')key('bk');else if(k==='-'&&LV[S.lv].neg)key('neg');else if(k==='Enter'){key('ok')}else return;
  e.preventDefault();
});
setLv('low');show('intro');
window.HLG_MA={cfg:CFG,state:function(){return S},gen:gen,key:key};
})();
