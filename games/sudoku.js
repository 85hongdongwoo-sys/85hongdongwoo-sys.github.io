/* 홍라이프 스도쿠 — 유일해 퍼즐 생성기 + 플레이 */
(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
var LV={easy:{n:'쉬움',giv:40,base:3000},normal:{n:'보통',giv:32,base:6000},hard:{n:'어려움',giv:26,base:10000}};
var PER_SEC=2,HINT_COST=300,MISS_COST=100,HINTS=3,SAVE_KEY='sudoku:cur';

/* ---------- 솔버 (비트마스크 + 최소 후보 우선) ---------- */
var ROW=[],COL=[],BOX=[],POP=new Uint8Array(1024),LOG={};
for(var i=0;i<81;i++){ROW[i]=i/9|0;COL[i]=i%9;BOX[i]=(ROW[i]/3|0)*3+(COL[i]/3|0)}
for(var m=1;m<1024;m++)POP[m]=POP[m>>1]+(m&1);
for(var v=1;v<=9;v++)LOG[1<<v]=v;
var PEERS=[];
for(i=0;i<81;i++){var s=[];for(var j=0;j<81;j++)if(j!==i&&(ROW[j]===ROW[i]||COL[j]===COL[i]||BOX[j]===BOX[i]))s.push(j);PEERS[i]=s}
function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.random()*(i+1)|0,t=a[i];a[i]=a[j];a[j]=t}return a}

/* grid: 길이 81 배열(0=빈칸). limit개까지 해의 수를 센다. random=true면 무작위 순서로 첫 해를 out에 담는다. */
function solve(grid,limit,out,random){
  var g=grid.slice(),r=[0,0,0,0,0,0,0,0,0],c=r.slice(),b=r.slice(),cnt=0;
  for(var i=0;i<81;i++){var v=g[i];if(v){var m=1<<v;if((r[ROW[i]]|c[COL[i]]|b[BOX[i]])&m)return 0;r[ROW[i]]|=m;c[COL[i]]|=m;b[BOX[i]]|=m}}
  function rec(){
    var best=-1,bm=0,bc=10;
    for(var i=0;i<81;i++)if(!g[i]){var m=~(r[ROW[i]]|c[COL[i]]|b[BOX[i]])&0x3FE,k=POP[m];if(k<bc){bc=k;best=i;bm=m;if(k<2)break}}
    if(best<0){cnt++;if(out&&!out.length)Array.prototype.push.apply(out,g);return cnt>=limit}
    if(!bc)return false;
    var bits=[];while(bm){var bit=bm&-bm;bm^=bit;bits.push(bit)}
    if(random)shuffle(bits);
    var R=ROW[best],C=COL[best],B=BOX[best];
    for(var k=0;k<bits.length;k++){var bt=bits[k];r[R]|=bt;c[C]|=bt;b[B]|=bt;g[best]=LOG[bt];
      if(rec())return true;
      r[R]^=bt;c[C]^=bt;b[B]^=bt}
    g[best]=0;return false;
  }
  rec();return cnt;
}
function fullGrid(){var out=[];solve(new Array(81).fill(0),1,out,true);return out}
function make(giv){
  var best=null;
  for(var at=0;at<8;at++){
    var sol=fullGrid(),p=sol.slice(),order=shuffle(Array.from({length:81},function(_,i){return i})),n=81;
    for(var k=0;k<81&&n>giv;k++){var idx=order[k],v=p[idx];p[idx]=0;if(solve(p,2)!==1)p[idx]=v;else n--}
    if(!best||n<best.n)best={p:p,sol:sol,n:n};
    if(n<=giv)break;
  }
  return best;
}

/* ---------- 상태 ---------- */
var S=null,boardEl=$('sd'),cells=[],timerI=0,board=HLG.mountBoard($('lb'),'sudoku','normal'),lv='normal';
function save(){if(S&&!S.done)HLG.store.set(SAVE_KEY,{lv:S.lv,p:S.p,sol:S.sol,cur:S.cur,notes:S.notes,lock:S.lock,mist:S.mist,hints:S.hints,el:S.el});else HLG.store.set(SAVE_KEY,null)}
function newGame(l){
  lv=l||lv;$('msg').textContent='퍼즐을 만드는 중…';$('msg').className='msg';
  setTimeout(function(){
    var mk=make(LV[lv].giv);
    S={lv:lv,p:mk.p,sol:mk.sol,cur:mk.p.slice(),notes:new Array(81).fill(0),lock:mk.p.map(function(x){return x?1:0}),mist:0,hints:0,el:0,hist:[],sel:-1,note:false,done:false,paused:false};
    $('msg').textContent='';selFirst();start();render();save();
  },20);
}
function load(){
  var o=HLG.store.get(SAVE_KEY,null);
  if(o&&LV[o.lv]&&Array.isArray(o.cur)&&o.cur.length===81&&Array.isArray(o.sol)&&o.sol.length===81){
    lv=o.lv;S={lv:o.lv,p:o.p,sol:o.sol,cur:o.cur,notes:o.notes||new Array(81).fill(0),lock:o.lock||o.p.map(function(x){return x?1:0}),mist:o.mist|0,hints:o.hints|0,el:+o.el||0,hist:[],sel:-1,note:false,done:false,paused:false};
    selFirst();start();render();$('msg').textContent='이어서 하던 퍼즐을 불러왔어요.';return true;
  }
  return false;
}
function selFirst(){S.sel=S.cur.indexOf(0);if(S.sel<0)S.sel=0}
var lastTick=0;
function start(){clearInterval(timerI);lastTick=performance.now();timerI=setInterval(tick,250)}
function tick(){var now=performance.now();if(S&&!S.done&&!S.paused&&!document.hidden)S.el+=(now-lastTick)/1000;lastTick=now;hud();if((now|0)%5000<260)save()}
function secs(){return Math.floor(S.el)}
function scoreNow(){var L=LV[S.lv];return Math.max(Math.round(L.base*0.1),L.base-PER_SEC*secs()-HINT_COST*S.hints-MISS_COST*S.mist)}
function mmss(t){var m=Math.floor(t/60),s=t%60;return m+':'+(s<10?'0':'')+s}
function hud(){if(!S)return;$('tm').textContent=mmss(secs());$('ms').textContent=S.mist;$('ht').textContent=(HINTS-S.hints)+'/'+HINTS;$('sc').textContent=HLG.fmt(scoreNow())}

/* ---------- 렌더 ---------- */
function build(){
  var h='';
  for(var i=0;i<81;i++){h+='<button type="button" class="c'+(COL[i]%3===2&&COL[i]<8?' br':'')+(ROW[i]%3===2&&ROW[i]<8?' bb':'')+'" data-i="'+i+'"></button>'}
  boardEl.innerHTML=h;cells=Array.prototype.slice.call(boardEl.children);
}
function render(){
  if(!S)return;
  var sel=S.sel,sv=sel>=0?S.cur[sel]:0,cnt=[0,0,0,0,0,0,0,0,0,0];
  for(var i=0;i<81;i++){
    var v=S.cur[i],c=cells[i],cl='c'+(COL[i]%3===2&&COL[i]<8?' br':'')+(ROW[i]%3===2&&ROW[i]<8?' bb':'');
    if(v)cnt[v]++;
    if(S.p[i])cl+=' gv';else if(S.lock[i])cl+=' hn';else if(v)cl+=' us';
    if(i===sel)cl+=' sel';
    else if(sel>=0&&(ROW[i]===ROW[sel]||COL[i]===COL[sel]||BOX[i]===BOX[sel]))cl+=' pr';
    if(v&&sv&&v===sv&&i!==sel)cl+=' same';
    if(v){var pe=PEERS[i];for(var k=0;k<pe.length;k++)if(S.cur[pe[k]]===v){cl+=' cf';break}}
    if(v&&!S.p[i]&&v!==S.sol[i])cl+=' wr';
    c.className=cl;
    var lab=(ROW[i]+1)+'행 '+(COL[i]+1)+'열';
    if(v){c.innerHTML=v;c.setAttribute('aria-label',lab+', '+v+(S.p[i]?' (주어진 숫자)':''))}
    else if(S.notes[i]){var n='<span class="nt">';for(var d=1;d<=9;d++)n+='<i'+(sv===d&&(S.notes[i]>>d&1)?' class="on"':'')+'>'+((S.notes[i]>>d&1)?d:'')+'</i>';c.innerHTML=n+'</span>';c.setAttribute('aria-label',lab+', 메모')}
    else{c.innerHTML='';c.setAttribute('aria-label',lab+', 빈칸')}
  }
  document.querySelectorAll('#pad .key[data-n]').forEach(function(b){var d=+b.dataset.n,left=9-cnt[d];b.querySelector('small').textContent=left>0?left:'';b.classList.toggle('full',left<=0)});
  $('memo').setAttribute('aria-pressed',S.note);$('memo').querySelector('b').textContent=S.note?'ON':'OFF';
  $('undo').disabled=!S.hist.length;$('hint').disabled=S.hints>=HINTS||S.done;
  boardEl.classList.toggle('paused',S.paused);$('pz').hidden=!S.paused;$('pauseT').textContent=S.paused?'계속':'일시정지';$('pause').setAttribute('aria-pressed',S.paused);
  hud();
}

/* ---------- 입력 ---------- */
function editable(i){return i>=0&&!S.lock[i]&&!S.done&&!S.paused}
function push(ch){S.hist.push(ch);if(S.hist.length>300)S.hist.shift()}
function input(d){
  var i=S.sel;if(!editable(i))return;
  if(S.note){if(S.cur[i])return;push([[i,S.cur[i],S.notes[i]]]);S.notes[i]^=1<<d;render();save();return}
  if(S.cur[i]===d)return;
  var ch=[[i,S.cur[i],S.notes[i]]];
  S.cur[i]=d;S.notes[i]=0;
  PEERS[i].forEach(function(p){if(S.notes[p]>>d&1){ch.push([p,S.cur[p],S.notes[p]]);S.notes[p]&=~(1<<d)}});
  push(ch);
  if(d!==S.sol[i]){S.mist++;msg('이 칸에는 '+d+'이(가) 맞지 않아요. 실수 +1','bad')}else msg('');
  render();save();check();
}
function erase(){var i=S.sel;if(!editable(i)||(!S.cur[i]&&!S.notes[i]))return;push([[i,S.cur[i],S.notes[i]]]);S.cur[i]=0;S.notes[i]=0;render();save()}
function undo(){if(!S.hist.length||S.done)return;var ch=S.hist.pop();for(var k=ch.length-1;k>=0;k--){var x=ch[k];if(S.lock[x[0]])continue;S.cur[x[0]]=x[1];S.notes[x[0]]=x[2]}S.sel=ch[0][0];render();save()}
function hint(){
  if(S.hints>=HINTS||S.done||S.paused)return;
  var i=S.sel;
  if(i<0||S.lock[i]||S.cur[i]===S.sol[i]){var c=[];for(var k=0;k<81;k++)if(!S.lock[k]&&S.cur[k]!==S.sol[k])c.push(k);if(!c.length)return;i=c[Math.random()*c.length|0]}
  S.cur[i]=S.sol[i];S.notes[i]=0;S.lock[i]=1;S.hints++;S.sel=i;
  PEERS[i].forEach(function(p){S.notes[p]&=~(1<<S.sol[i])});
  msg((ROW[i]+1)+'행 '+(COL[i]+1)+'열에 '+S.sol[i]+'을(를) 채웠어요. 힌트 −'+HINT_COST+'점','ok');
  render();save();check();
}
function msg(t,c){$('msg').textContent=t;$('msg').className='msg'+(c?' '+c:'')}
function check(){
  for(var i=0;i<81;i++)if(S.cur[i]!==S.sol[i])return;
  S.done=true;var sc=scoreNow();save();render();
  boardEl.classList.add('win');
  setTimeout(function(){
    HLG.result({game:'sudoku',level:S.lv,score:sc,title:'퍼즐 완성!',save:true,board:board,
      facts:[['시간',mmss(secs())],['실수',S.mist+'회'],['힌트',S.hints+'회']],
      extra:mmss(secs())+' · 실수 '+S.mist+' · 힌트 '+S.hints,
      shareLine:HLG.fmt(sc)+'점 ('+mmss(secs())+')',onAgain:function(){newGame(S.lv)}});
    board.show(S.lv);
  },450);
}

var fitted=false;function fit(){if(fitted)return;fitted=true;var pl=document.querySelector('.play'),r=pl.getBoundingClientRect();if(r.bottom>innerHeight&&r.height<=innerHeight)try{pl.scrollIntoView({block:'end',behavior:'smooth'})}catch(e){}}
boardEl.addEventListener('click',function(e){var b=e.target.closest('.c');if(!b||!S||S.paused)return;S.sel=+b.dataset.i;render();fit()});
$('pad').addEventListener('click',function(e){var b=e.target.closest('.key[data-n]');if(b&&S)input(+b.dataset.n)});
$('undo').onclick=function(){S&&undo()};$('erase').onclick=function(){S&&erase()};$('hint').onclick=function(){S&&hint()};
$('memo').onclick=function(){if(!S)return;S.note=!S.note;render()};
$('pause').onclick=function(){if(!S||S.done)return;S.paused=!S.paused;render()};
$('pz').onclick=function(){if(S){S.paused=false;render()}};
$('new').onclick=function(){if(S&&!S.done&&S.cur.some(function(v,i){return v&&!S.p[i]})&&!confirm('지금 퍼즐을 그만두고 새 퍼즐을 시작할까요?'))return;newGame(lv)};
document.querySelectorAll('#lvl button').forEach(function(b){b.onclick=function(){
  if(S&&!S.done&&S.cur.some(function(v,i){return v&&!S.p[i]})&&!confirm(LV[b.dataset.l].n+' 난이도로 새 퍼즐을 시작할까요?'))return;
  setLv(b.dataset.l);newGame(b.dataset.l);board.show(b.dataset.l)}});
function setLv(l){document.querySelectorAll('#lvl button').forEach(function(x){x.setAttribute('aria-pressed',x.dataset.l===l)})}
document.addEventListener('keydown',function(e){
  if(!S||e.target.closest('input,textarea,.gdlg'))return;var k=e.key;
  if(/^[1-9]$/.test(k)){input(+k);e.preventDefault()}
  else if(k==='Backspace'||k==='Delete'||k==='0'){erase();e.preventDefault()}
  else if(k==='n'||k==='N'){S.note=!S.note;render()}
  else if((e.ctrlKey||e.metaKey)&&(k==='z'||k==='Z')){undo();e.preventDefault()}
  else if(k.indexOf('Arrow')===0&&S.sel>=0){var r=ROW[S.sel],c=COL[S.sel];if(k==='ArrowUp')r=(r+8)%9;if(k==='ArrowDown')r=(r+1)%9;if(k==='ArrowLeft')c=(c+8)%9;if(k==='ArrowRight')c=(c+1)%9;S.sel=r*9+c;render();e.preventDefault()}
});
document.addEventListener('visibilitychange',function(){if(document.hidden)save()});

build();
if(!load())newGame('normal');
setLv(lv);board.show(lv);
window.HLG_SD={solve:solve,make:make,state:function(){return S},LV:LV};
})();
