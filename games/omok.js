/* 홍라이프 오목 — 15×15 자유룰, 컴퓨터 대전(패턴·위협 평가 + 알파베타 + VCF) / 2인 대전 */
(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
var N=15,NN=N*N,BL=1,WH=2;

/* ===================== 엔진 ===================== */
var B=new Int8Array(NN),NB=new Int16Array(NN),LINES=[],CL=[];
for(var i=0;i<NN;i++)CL.push([]);
function addLine(x,y,dx,dy){var a=[];while(x>=0&&x<N&&y>=0&&y<N){a.push(y*N+x);x+=dx;y+=dy}if(a.length<5)return;var id=LINES.length;LINES.push(a);a.forEach(function(c){CL[c].push(id)})}
for(i=0;i<N;i++){addLine(0,i,1,0);addLine(i,0,0,1)}
for(i=0;i<N;i++){addLine(0,i,1,1);if(i)addLine(i,0,1,1)}
for(i=0;i<N;i++){addLine(N-1,i,-1,1);if(i<N-1)addLine(i,0,-1,1)}
var NL=LINES.length;
/* 패턴 지표: 0 오목 1 열린4 2 막힌4 3 열린3 4 막힌3 5 열린2 6 막힌2 */
var WT=[1e7,1e5,2600,2200,320,130,15];
var LC=new Int32Array(NL*2*7),LW=new Float64Array(NL*2),TOT=[null,new Int32Array(7),new Int32Array(7)],TW=[0,0,0];
var buf=new Int8Array(N+2),tmp=new Int32Array(7);
function uniqPush(a,k){for(var i=0;i<a.length;i++)if(a[i]===k)return;a.push(k)}
function diffCount(a,b){var n=0;for(var i=0;i<a.length;i++)if(b.indexOf(a[i])<0)n++;return n}
function analyze(li,p,o){
  var cells=LINES[li],L=cells.length,k,s,t,v;
  for(k=0;k<7;k++)o[k]=0;
  buf[0]=2;buf[L+1]=2;
  for(k=0;k<L;k++){v=B[cells[k]];buf[k+1]=v===0?0:(v===p?1:2)}
  var run=0;for(k=1;k<=L;k++){if(buf[k]===1){if(++run>=5)o[0]=1}else run=0}
  var f4=[],t3=[],t2=[],o4=[],o3=[],o2=[],E=L+2;
  for(s=0;s+5<=E;s++){
    var ones=0,key=0,bad=false;
    for(t=0;t<5;t++){v=buf[s+t];if(v===2){bad=true;break}if(v===1){ones++;key|=1<<(s+t)}}
    if(bad)continue;
    if(ones===4)uniqPush(f4,key);else if(ones===3)uniqPush(t3,key);else if(ones===2)uniqPush(t2,key);
  }
  for(s=0;s+6<=E;s++){
    if(buf[s]!==0||buf[s+5]!==0)continue;
    ones=0;key=0;bad=false;
    for(t=1;t<5;t++){v=buf[s+t];if(v===2){bad=true;break}if(v===1){ones++;key|=1<<(s+t)}}
    if(bad)continue;
    if(ones===4)uniqPush(o4,key);else if(ones===3)uniqPush(o3,key);else if(ones===2)uniqPush(o2,key);
  }
  o[1]=o4.length;o[2]=diffCount(f4,o4);o[3]=o3.length;o[4]=diffCount(t3,o3);o[5]=o2.length;o[6]=diffCount(t2,o2);
  var w=0;for(k=0;k<7;k++)w+=o[k]*WT[k];return w;
}
function updCell(c){
  var ls=CL[c];
  for(var j=0;j<ls.length;j++){var li=ls[j];
    for(var p=1;p<=2;p++){var base=(li*2+p-1)*7,T=TOT[p];
      for(var k=0;k<7;k++)T[k]-=LC[base+k];
      TW[p]-=LW[li*2+p-1];
      var w=analyze(li,p,tmp);
      for(k=0;k<7;k++){LC[base+k]=tmp[k];T[k]+=tmp[k]}
      LW[li*2+p-1]=w;TW[p]+=w;
    }
  }
}
function nbAdd(c,d){var x=c%N,y=c/N|0;for(var yy=Math.max(0,y-2);yy<=Math.min(N-1,y+2);yy++)for(var xx=Math.max(0,x-2);xx<=Math.min(N-1,x+2);xx++)NB[yy*N+xx]+=d}
function place(c,p){B[c]=p;updCell(c);nbAdd(c,1)}
function unplace(c){B[c]=0;updCell(c);nbAdd(c,-1)}
function resetEngine(){B.fill(0);NB.fill(0);LC.fill(0);LW.fill(0);TOT[1].fill(0);TOT[2].fill(0);TW[1]=TW[2]=0;
  for(var li=0;li<NL;li++)for(var p=1;p<=2;p++){/* 빈 판: 모든 패턴 0 */}}
var DIRS=[[1,0],[0,1],[1,1],[1,-1]];
function runLen(c,p,dx,dy){var x=c%N,y=c/N|0,n=0;x+=dx;y+=dy;while(x>=0&&x<N&&y>=0&&y<N&&B[y*N+x]===p){n++;x+=dx;y+=dy}return n}
function makesFive(c,p){if(B[c])return false;for(var d=0;d<4;d++){var D=DIRS[d];if(1+runLen(c,p,D[0],D[1])+runLen(c,p,-D[0],-D[1])>=5)return true}return false}
function cands(){var a=[];for(var c=0;c<NN;c++)if(!B[c]&&NB[c]>0)a.push(c);return a}
function winCells(p,list){var r=[];list=list||cands();for(var i=0;i<list.length;i++)if(makesFive(list[i],p))r.push(list[i]);return r}
function gainAt(c,p){var ls=CL[c],g=0;B[c]=p;for(var j=0;j<ls.length;j++){var li=ls[j];g+=analyze(li,p,tmp)-LW[li*2+p-1]}B[c]=0;return g}
function order(p,wdef,list){
  list=list||cands();var q=3-p,r=[];
  for(var i=0;i<list.length;i++){var c=list[i],a=gainAt(c,p),d=gainAt(c,q);r.push({c:c,s:a+d*wdef,a:a,d:d})}
  r.sort(function(x,y){return y.s-x.s});return r;
}
var WIN=1e9;
function evalStatic(p){
  var q=3-p,A=TOT[p],O=TOT[q];
  if(O[0])return -WIN;if(A[0])return WIN;
  if(A[1]+A[2]>0)return WIN*0.9;
  if(O[1]>0||O[2]>=2)return -WIN*0.8;
  if(A[3]>0&&O[2]===0)return WIN*0.5;
  if(O[3]>=2&&A[2]===0)return -WIN*0.3;
  return TW[p]-TW[q]*1.05;
}
var deadline=0,aborted=false,nodes=0;
function negamax(p,depth,alpha,beta,ply,beam){
  if((++nodes&63)===0&&performance.now()>deadline){aborted=true;return 0}
  var q=3-p;
  if(TOT[q][0])return -(WIN-ply);
  if(TOT[p][1]+TOT[p][2]>0)return WIN-ply-1;
  if(depth===0)return evalStatic(p);
  var list=cands(),must=TOT[q][1]+TOT[q][2]>0?winCells(q,list):null;
  var mv=must&&must.length?must.map(function(c){return{c:c}}):order(p,1,list).slice(0,beam[ply]||4);
  var best=-Infinity;
  for(var i=0;i<mv.length;i++){
    place(mv[i].c,p);var v=-negamax(q,depth-1,-beta,-alpha,ply+1,beam);unplace(mv[i].c);
    if(aborted)return 0;
    if(v>best)best=v;if(v>alpha)alpha=v;if(alpha>=beta)break;
  }
  return best;
}
/* VCF: 연속 4로 몰아서 이기는 수순 탐색 */
var vcfNodes=0;
function vcf(p,d){
  if(d<=0||++vcfNodes>4000||performance.now()>deadline)return -1;
  var q=3-p,list=cands();
  var w=winCells(p,list);if(w.length)return w[0];
  if(winCells(q,list).length)return -1;
  for(var i=0;i<list.length;i++){
    var c=list[i],f=TOT[p][1]+TOT[p][2];
    place(c,p);
    if(TOT[p][1]+TOT[p][2]>f){
      var wc=winCells(p);
      if(wc.length>=2){unplace(c);return c}
      if(wc.length===1){
        var blk=wc[0];place(blk,q);
        var ok=!TOT[q][0]&&!(TOT[q][1]+TOT[q][2]>0)&&vcf(p,d-1)>=0;
        unplace(blk);
        if(ok){unplace(c);return c}
      }
    }
    unplace(c);
  }
  return -1;
}
var LEVELS={easy:{wdef:0.55,depth:0,top:4},normal:{wdef:0.95,depth:2,beam:[9,9],ms:140},hard:{wdef:1,depth:5,beam:[12,10,8,7,6,5],ms:190,vcf:true}};
function think(p,lvName){
  var L=LEVELS[lvName],q=3-p,t0=performance.now(),list=cands();
  if(!list.length)return 7*N+7;
  var w=winCells(p,list);if(w.length)return w[0];
  var must=winCells(q,list);
  if(must.length){
    if(lvName==='easy'&&Math.random()<0.12){/* 쉬움: 가끔 놓침 */}
    else if(must.length===1)return must[0];
    else return order(p,1,must)[0].c;
  }
  var ord=order(p,L.wdef,list);
  if(lvName==='easy'){
    var top=ord.slice(0,L.top).filter(function(m,i){return i===0||m.s>ord[0].s*0.35});
    if(ord[0].a>=WT[1])return ord[0].c;
    return top[Math.random()*top.length|0].c;
  }
  deadline=t0+L.ms;
  if(L.vcf){vcfNodes=0;var dl=deadline;deadline=t0+50;var v=vcf(p,10);deadline=dl;if(v>=0)return v}
  var rootMoves=ord.slice(0,L.beam[0]),best=rootMoves[0].c,scores={};
  for(var depth=1;depth<=L.depth;depth++){
    aborted=false;nodes=0;var alpha=-Infinity,bm=-1,bs=-Infinity,res=[];
    for(var i=0;i<rootMoves.length;i++){
      var c=rootMoves[i].c;place(c,p);
      var sc=-negamax(q,depth-1,-Infinity,-alpha,1,L.beam);unplace(c);
      if(aborted)break;
      sc+=rootMoves[i].s*1e-3;res.push({c:c,s:sc});
      if(sc>bs){bs=sc;bm=c}if(sc>alpha)alpha=sc;
    }
    if(aborted)break;
    best=bm;res.sort(function(a,b){return b.s-a.s});
    rootMoves=res.map(function(r){for(var k=0;k<ord.length;k++)if(ord[k].c===r.c)return ord[k]});
    if(bs>=WIN*0.85)break;
  }
  if(L.vcf){/* 상대 VCF 방어 확인 */
    deadline=Math.min(performance.now()+40,t0+250);
    var tries=[best].concat(rootMoves.map(function(m){return m.c}).filter(function(c){return c!==best})).slice(0,6);
    for(var k=0;k<tries.length;k++){place(tries[k],p);vcfNodes=0;var r=vcf(q,8);unplace(tries[k]);if(r<0){best=tries[k];break}if(performance.now()>deadline)break}
  }
  if(lvName==='normal'&&rootMoves.length>1&&Math.random()<0.15&&Math.abs(rootMoves[1].s-rootMoves[0].s)<rootMoves[0].s*0.15)best=rootMoves[1].c;
  return best;
}
function fiveLine(c){var p=B[c];for(var d=0;d<4;d++){var D=DIRS[d],a=runLen(c,p,D[0],D[1]),b=runLen(c,p,-D[0],-D[1]);if(a+b+1>=5){var x=c%N,y=c/N|0;return[(y-b*D[1])*N+(x-b*D[0]),(y+a*D[1])*N+(x+a*D[0])]}}return null}

/* ===================== 게임 UI ===================== */
var cv=$('bd'),ctx=cv.getContext('2d'),S={mode:'cpu',lv:'normal',me:BL,hist:[],over:false,win:null,thinking:false,undos:0,ghost:-1};
var board=HLG.mountBoard($('lb'),'omok','normal');
var coarse=window.matchMedia&&matchMedia('(pointer:coarse)').matches;
$('dbl').checked=coarse;
var size=0;
function resize(){var r=cv.parentNode.getBoundingClientRect(),w=Math.floor(r.width),dpr=Math.min(3,window.devicePixelRatio||1);size=w;cv.style.width=w+'px';cv.style.height=w+'px';cv.width=w*dpr;cv.height=w*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);draw()}
function turn(){return S.hist.length%2===0?BL:WH}
function pos(i){var s=size/N;return[s/2+(i%N)*s,s/2+(i/N|0)*s]}
function draw(){
  var s=size/N,g=ctx;g.clearRect(0,0,size,size);
  var gr=g.createLinearGradient(0,0,size,size);gr.addColorStop(0,'#F3DFAE');gr.addColorStop(1,'#E2C27F');g.fillStyle=gr;g.fillRect(0,0,size,size);
  g.strokeStyle='rgba(74,52,16,.75)';g.lineWidth=1;g.beginPath();
  for(var k=0;k<N;k++){var a=Math.round(s/2+k*s)+.5;g.moveTo(s/2,a);g.lineTo(size-s/2,a);g.moveTo(a,s/2);g.lineTo(a,size-s/2)}g.stroke();
  g.lineWidth=2;g.strokeRect(Math.round(s/2)+.5,Math.round(s/2)+.5,Math.round(s*(N-1)),Math.round(s*(N-1)));
  g.fillStyle='#4A3410';[[3,3],[11,3],[7,7],[3,11],[11,11]].forEach(function(p){var c=pos(p[1]*N+p[0]);g.beginPath();g.arc(Math.round(c[0])+.5,Math.round(c[1])+.5,Math.max(2,s*.11),0,7);g.fill()});
  var r=s*.46;
  for(var i=0;i<NN;i++)if(B[i])stone(i,B[i],r,1);
  if(S.ghost>=0&&!B[S.ghost])stone(S.ghost,turn(),r,.45);
  var last=S.hist[S.hist.length-1];
  if(last!=null&&!S.win){var c=pos(last);g.fillStyle=B[last]===BL?'#E5B850':'#C0392B';g.beginPath();g.arc(c[0],c[1],Math.max(2.5,s*.13),0,7);g.fill()}
  if(S.win){var a1=pos(S.win[0]),a2=pos(S.win[1]);g.strokeStyle='rgba(201,160,74,.95)';g.lineCap='round';g.lineWidth=Math.max(4,s*.22);g.beginPath();g.moveTo(a1[0],a1[1]);g.lineTo(a2[0],a2[1]);g.stroke();g.strokeStyle='#fff';g.lineWidth=Math.max(1.5,s*.06);g.stroke()}
}
function stone(i,p,r,al){
  var c=pos(i),g=ctx;g.globalAlpha=al;
  g.fillStyle='rgba(0,0,0,.25)';g.beginPath();g.arc(c[0]+r*.08,c[1]+r*.12,r,0,7);g.fill();
  var gr=g.createRadialGradient(c[0]-r*.35,c[1]-r*.4,r*.1,c[0],c[1],r);
  if(p===BL){gr.addColorStop(0,'#5A6475');gr.addColorStop(.55,'#1B2230');gr.addColorStop(1,'#05080D')}
  else{gr.addColorStop(0,'#FFFFFF');gr.addColorStop(.7,'#EEF0F3');gr.addColorStop(1,'#C9CED6')}
  g.fillStyle=gr;g.beginPath();g.arc(c[0],c[1],r,0,7);g.fill();g.globalAlpha=1;
}
function status(t,cl){var m=$('st');m.innerHTML=t;m.className='msg'+(cl?' '+cl:'')}
function stoneName(p){return p===BL?'흑':'백'}
function dot(p){return '<i class="sdot '+(p===BL?'b':'w')+'"></i>'}
function upd(){
  $('mv').textContent=S.hist.length;$('uc').textContent=S.undos;
  $('undo').disabled=S.over||S.thinking||!S.hist.length||(S.mode==='cpu'&&!S.hist.some(function(_,i){return(i%2===0?BL:WH)===S.me}));
  if(S.over)return;
  if(S.thinking)status('컴퓨터가 생각하는 중…');
  else if(S.mode==='pvp')status(dot(turn())+stoneName(turn())+' 차례예요');
  else status(dot(S.me)+'내 차례예요 ('+stoneName(S.me)+')');
  draw();
}
function newGame(){
  resetEngine();S.hist=[];S.over=false;S.win=null;S.undos=0;S.ghost=-1;S.thinking=false;$('cfg').classList.toggle('pvp',S.mode==='pvp');
  draw();upd();
  if(S.mode==='cpu'&&S.me===WH)cpuMove();
}
function play(c){
  var p=turn();place(c,p);S.hist.push(c);S.ghost=-1;
  if(TOT[p][0]){S.over=true;S.win=fiveLine(c);draw();upd();setTimeout(function(){end(p)},350);return}
  if(S.hist.length>=NN){S.over=true;draw();status('무승부예요');return}
  draw();upd();
}
function cpuMove(){
  S.thinking=true;upd();
  setTimeout(function(){
    var t=performance.now(),c=think(turn(),S.lv);S.lastMs=Math.round(performance.now()-t);
    setTimeout(function(){S.thinking=false;play(c)},Math.max(0,260-S.lastMs));
  },30);
}
function end(p){
  var meStones=Math.ceil(S.hist.length/2);
  if(S.mode==='pvp'){status(dot(p)+stoneName(p)+' 승리! ('+meStones+'수)','ok');
    HLG.result({game:'omok',level:null,score:null,title:stoneName(p)+' 승리!',facts:[['승리한 쪽',stoneName(p)],['둔 수',meStones+'수'],['전체 수',S.hist.length+'수']],save:false,note:'2인 대전은 순위에 기록하지 않아요. 컴퓨터를 이기면 기록할 수 있어요.',shareLine:'2인 대전 '+stoneName(p)+' 승리 ('+meStones+'수)',onAgain:newGame});return}
  if(p===S.me){status('승리! '+meStones+'수 만에 이겼어요','ok');
    HLG.result({game:'omok',level:S.lv,score:meStones,title:'컴퓨터를 이겼어요!',save:true,board:board,facts:[['내 돌',stoneName(S.me)],['둔 수',meStones+'수'],['무르기',S.undos+'회']],extra:stoneName(S.me)+(S.undos?' · 무르기 '+S.undos+'회':''),shareLine:'컴퓨터('+HLG.levelName('omok',S.lv)+')에게 '+meStones+'수 만에 승리',onAgain:newGame});
    board.show(S.lv);
  }else{status('컴퓨터가 이겼어요. 다시 도전해 보세요!','bad');
    HLG.result({game:'omok',level:S.lv,score:null,title:'아쉽게 졌어요',facts:[['컴퓨터 돌',stoneName(p)],['전체 수',S.hist.length+'수']],save:false,note:'컴퓨터를 이기면 이름을 넣어 이 기기 순위에 기록할 수 있어요.',shareLine:'컴퓨터('+HLG.levelName('omok',S.lv)+')와 접전 끝에 패배',onAgain:newGame})}
}
function cellAt(ev){var r=cv.getBoundingClientRect(),s=r.width/N,x=Math.floor((ev.clientX-r.left)/s),y=Math.floor((ev.clientY-r.top)/s);if(x<0||y<0||x>=N||y>=N)return -1;return y*N+x}
cv.addEventListener('click',function(ev){
  if(S.over||S.thinking)return;
  if(S.mode==='cpu'&&turn()!==S.me)return;
  var c=cellAt(ev);if(c<0||B[c])return;
  if(!S.fit){S.fit=1;var r=cv.getBoundingClientRect();if(r.top<0||r.bottom+48>innerHeight)try{$('st').scrollIntoView({block:'end',behavior:'smooth'})}catch(e){}}
  if($('dbl').checked&&S.ghost!==c){S.ghost=c;draw();status('같은 자리를 한 번 더 누르면 둬요','');return}
  play(c);
  if(!S.over&&S.mode==='cpu')cpuMove();
});
$('undo').onclick=function(){
  if(S.over||S.thinking)return;
  var n=S.mode==='cpu'?(turn()===S.me?2:1):1;
  for(var k=0;k<n&&S.hist.length;k++)unplace(S.hist.pop());
  if(S.mode==='cpu'&&turn()!==S.me&&S.hist.length)unplace(S.hist.pop());
  S.undos++;S.ghost=-1;draw();upd();
  if(S.mode==='cpu'&&turn()!==S.me)cpuMove();
};
$('new').onclick=function(){if(S.hist.length&&!S.over&&!confirm('지금 대국을 그만두고 새로 시작할까요?'))return;newGame()};
function segs(id,attr,fn){document.querySelectorAll('#'+id+' button').forEach(function(b){b.onclick=function(){
  if(S.hist.length&&!S.over&&!confirm('설정을 바꾸면 새 대국을 시작해요. 계속할까요?'))return;
  document.querySelectorAll('#'+id+' button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});fn(b.dataset[attr]);newGame()}})}
segs('mode','m',function(v){S.mode=v});
segs('lvl','l',function(v){S.lv=v;board.show(v)});
segs('col','c',function(v){S.me=+v});
window.addEventListener('resize',function(){clearTimeout(S.rt);S.rt=setTimeout(resize,80)});
resize();newGame();
window.HLG_OM={
  load:function(moves){resetEngine();S.hist=[];S.over=false;S.win=null;moves.forEach(function(m){var c=m[1]*N+m[0];place(c,turn());S.hist.push(c)});draw();return turn()},
  think:function(lv){var t=performance.now(),c=think(turn(),lv);return{x:c%N,y:c/N|0,ms:performance.now()-t}},
  play:function(x,y){play(y*N+x)},state:function(){return S},tot:TOT
};
})();
