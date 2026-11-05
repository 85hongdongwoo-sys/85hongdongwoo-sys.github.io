/* 홍라이프 간식·내 방 — 계산하면 간식 1개, 메뉴별 물건이 방에 생김. 기기 브라우저(localStorage)에만 저장 */
(function(){
  'use strict';
  var D=document, H=D.documentElement;
  if(!/^ko/i.test(H.lang||'')||H.classList.contains('hl-embed')||window.__hlp) return;
  window.__hlp=1;
  var KEY='hlp1';
  // 메뉴(분야) → 방 자리
  var CATS={
    avatar:{n:'직장인·세금·급여',t:['정장','금색 손목시계','고급 가죽 가방']},
    car:{n:'자동차',t:['소형차','세단','빨간 스포츠카']},
    stock:{n:'주식·ETF',t:['주가 그래프 액자','금고','금괴 더미']},
    save:{n:'저축·연금',t:['돼지 저금통','금화 항아리','금고 안 금화']},
    estate:{n:'부동산·대출',t:['새 벽지','큰 창문과 커튼','한강뷰 창밖']},
    tools:{n:'생활·도구',t:['벽시계','큰 TV','고급 소파']},
    fortune:{n:'건강·운세',t:['별자리 액자','수정구슬','샹들리에']},
    baby:{n:'출산·육아',t:['아기 옷 빨랫줄','아기 침대','고급 유모차']},
    exam:{n:'대입',t:['책 더미','학사모','피아노']},
    games:{n:'게임',t:['오목판','게임기','당구대']},
    other:{n:'기타 계산기',t:[]}
  };
  var STEP=[3,11,26]; // 누적 간식: 1단계 3개, 2단계 +8개, 3단계 +15개
  var G2C={stock:'stock',save:'save',estate:'estate',tax:'avatar',gw:'avatar',labor:'avatar',car:'car',health:'fortune',look:'other',math:'other',tools:'tools',exam:'exam',games:'games'};
  var TAB={sell:'stock',us:'stock',div:'stock',avg:'stock',risk:'stock',gold:'stock',ipo:'stock',int:'save',grow:'save',pen:'save',fire:'save',fin:'save',nhis:'save',yet:'save',nps:'save',sev:'save',eitc:'save',buy:'estate',dsr:'estate',score:'estate',safe:'estate',rent:'estate',refi:'estate',ptax:'estate',gift:'estate',yield:'estate',auc:'estate',dist:'estate'};
  var PAGE={'stock-value':'stock','youth-savings':'save','side-tax':'gw','wage':'labor','unemp':'labor','parental':'baby','salary-net':'gw','leave':'gw','salary-rank':'gw','gw-pay':'gw','gw-overtime':'gw','gw-pension':'gw','car-cost':'car','car-commute':'car','car-tax':'car','car-buy':'car','car-parts':'car','car-ev':'car','calorie':'health','health':'health','life-left':'health','fortune-2027':'health','due-date':'baby','saju':'health','mbti':'health','mbti-test':'health','iq-test':'health','calc':'math','fraction':'math','sci-calc':'math','root-power':'math','percent':'tools','char-count':'tools','couple-dday':'tools','suneung':'exam','age-table':'tools','pyeong':'tools','travel':'tools','elec':'tools','date':'tools','exam':'tools','clock':'tools'};
  var DIR={salary:'avatar',hourly:'avatar',tax:'avatar',yearend:'save',car:'car',saju:'fortune',born:'other',py:'tools','loan-int':'estate',budget:'tools',shorts:'tools',student:'exam',games:'games'};
  var path=location.pathname.replace(/index\.html$/,'');
  var seg=path.split('/').filter(Boolean);
  var NOAWARD=/^(guide|qa)$/.test(seg[0]||'')||/^(about|privacy|offline|room)(\.html)?$/.test(seg[seg.length-1]||'');
  function pageCat(){
    if(seg.length===0){ // 메인: 지금 열린 탭의 분야
      var t=D.querySelector('.subtabs [role=tab][aria-selected=true]');
      var id=t&&t.getAttribute('data-tab');
      return id&&TAB[id]?TAB[id]:null;
    }
    if(seg.length===1&&/\.html$/.test(seg[0])){
      var b=seg[0].replace(/\.html$/,'');
      if(TAB[b]) return TAB[b];
      if(PAGE[b]) return PAGE[b]==='baby'?'baby':(G2C[PAGE[b]]||PAGE[b]);
      return null;
    }
    return DIR[seg[0]]||null;
  }
  function pageKey(){
    if(seg.length===0){var t=D.querySelector('.subtabs [role=tab][aria-selected=true]');return '/#'+(t?t.getAttribute('data-tab'):'');}
    return path;
  }
  // 저장소
  function today(){var d=new Date();return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2);}
  function load(){var s;try{s=JSON.parse(localStorage.getItem(KEY)||'null');}catch(e){}
    if(!s||typeof s!=='object') s={};
    s.total=+s.total||0; s.c=s.c||{}; s.d=s.d||{}; s.days=+s.days||0; s.last=s.last||''; return s;}
  function save(s){try{localStorage.setItem(KEY,JSON.stringify(s));return true;}catch(e){return false;}}
  function tier(n){var t=0;while(t<3&&n>=STEP[t])t++;return t;}
  window.hlPets={CATS:CATS,STEP:STEP,load:load,tier:tier};
  // 최근 쓴 계산기 (이 기기에만, 최대 8개)
  var RKEY='hlp1r';
  function recentList(){try{var r=JSON.parse(localStorage.getItem(RKEY)||'[]');return Array.isArray(r)?r:[];}catch(e){return [];}}
  function pageTitle(){var h=D.querySelector('h1');var t=(h&&h.textContent||D.title||'').replace(/\s+/g,' ').trim();t=t.split(/[|·\-–]/)[0].trim()||t;return t.length>22?t.slice(0,21)+'…':t;}
  function remember(){
    if(NOAWARD||!seg.length||!pageCat()) return;
    var r=recentList().filter(function(x){return x&&x.p!==path;});
    r.unshift({p:path,t:pageTitle()}); r=r.slice(0,8);
    try{localStorage.setItem(RKEY,JSON.stringify(r));}catch(e){}
  }
  window.hlPets.recent=recentList;
  // 오른쪽 아래 동물 버튼
  var fab;
  function drawFab(s){
    if(/\/room(\.html)?$/.test(path)) return;
    if(!fab){fab=D.createElement('a');fab.className='hlp-fab';fab.href='/room.html';fab.setAttribute('aria-label','내 동물 방 열기');fab.appendChild(D.createElement('b'));D.body.appendChild(fab);}
    var b=fab.querySelector('b');b.textContent=s.total>99?'99+':String(s.total);b.hidden=!s.total;
    fab.setAttribute('aria-label','내 동물 방 열기, 간식 '+s.total+'개');
  }
  // 알림
  var toastT;
  function toast(title,sub){
    var old=D.querySelector('.hlp-toast');if(old)old.remove();
    var el=D.createElement('div');el.className='hlp-toast';el.setAttribute('role','status');
    el.innerHTML='<i aria-hidden="true"></i><div><strong></strong><span></span></div><a href="/room.html">내 방 →</a>';
    el.querySelector('strong').textContent=title;el.querySelector('span').textContent=sub;
    D.body.appendChild(el);clearTimeout(toastT);
    toastT=setTimeout(function(){el.classList.add('out');setTimeout(function(){el.remove();},450);},5200);
  }
  function award(){
    if(NOAWARD) return;
    var cat=pageCat(); if(!cat) return;
    var s=load(), day=today(), key=pageKey();
    if(!s.d[day]){ // 날짜 바뀌면 오래된 기록 정리 + 출석
      var y=new Date(Date.now()-864e5), yd=y.getFullYear()+'-'+('0'+(y.getMonth()+1)).slice(-2)+'-'+('0'+y.getDate()).slice(-2);
      s.days=(s.last===yd)?s.days+1:1; s.last=day; s.d={}; s.d[day]={};
    }
    if(s.d[day][key]) return;
    s.d[day][key]=1;
    var before=s.c[cat]||0; s.c[cat]=before+1; s.total++;
    if(!save(s)) return;
    drawFab(s);
    var c=CATS[cat], tb=tier(before), ta=tier(s.c[cat]);
    if(ta>tb&&c.t[ta-1]) toast('새 물건이 생겼어요!',c.n+' 간식으로 「'+c.t[ta-1]+'」을(를) 방에 들였어요.');
    else if(c.t.length&&ta<3) toast('간식 1개 받았어요!',c.n+' · 「'+c.t[ta]+'」까지 '+(STEP[ta]-s.c[cat])+'개 남았어요');
    else toast('간식 1개 받았어요!','지금까지 모은 간식 '+s.total+'개');
  }
  // 계산을 했다고 보는 순간: 계산 버튼 누름, 또는 입력값을 바꾸고 잠시 뒤(바로 계산되는 화면)
  var RX=/계산|확인|보기|풀이|결과|시작|변환|조회|분석|검사|뽑기|보러|알아보기|적용/;
  var typed;
  function inUI(t){return t.closest&&t.closest('nav,header,footer,.brandbar,.hl-rel,.hl-share,.hlp-fab,.hlp-toast,[role=tablist]');}
  D.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('button,[role=button],input[type=submit],input[type=button]');
    if(!b||inUI(b)) return;
    var txt=(b.textContent||b.value||'')+' '+(b.getAttribute('aria-label')||'');
    if(RX.test(txt)) setTimeout(award,600);
  },true);
  D.addEventListener('input',function(e){
    var t=e.target; if(!t.matches||!t.matches('input,select,textarea')||inUI(t)) return;
    clearTimeout(typed); typed=setTimeout(award,1800);
  },true);
  D.addEventListener('change',function(e){
    var t=e.target; if(!t.matches||!t.matches('select,input[type=radio],input[type=checkbox],input[type=date],input[type=range]')||inUI(t)) return;
    clearTimeout(typed); typed=setTimeout(award,1200);
  },true);
  window.hlPets.pageCat=pageCat;
  // ── 출석 간식: 하루 첫 방문 +1, 7일 연속마다 +3 ──
  function attend(){
    var s=load(),day=today();if(s.att===day)return;
    var y=new Date(Date.now()-864e5),yd=y.getFullYear()+'-'+('0'+(y.getMonth()+1)).slice(-2)+'-'+('0'+y.getDate()).slice(-2);
    s.as=(s.att===yd)?(+s.as||0)+1:1;s.att=day;var gain=1+(s.as%7===0?3:0);s.total+=gain;
    if(!save(s))return;drawFab(s);
    setTimeout(function(){toast(s.as%7===0?'7일 연속 출석! 간식 +4':'출석 간식 +1',s.as>1?('연속 '+s.as+'일째 방문 중 · 7일마다 보너스 3개'):'내일 또 오면 연속 출석이 시작돼요');},900);
  }
  // ── 분야별 추천 칸 (쿠팡 파트너스, ads.js에서 관리) ──
  var REC={car:'coupang_car',baby:'coupang_baby',fortune:'coupang_health',exam:'coupang_study',avatar:'coupang_work',stock:'coupang_book',save:'coupang_book',estate:'coupang_home',tools:'coupang_all',games:'coupang_all',other:'coupang_all'};
  function reco(){
    if(NOAWARD||!seg.length||D.getElementById('adCoupang')||D.querySelector('.hl-reco'))return;
    var cat=pageCat();if(!cat)return;
    function show(){try{
      if(typeof ADS==='undefined')return;var a=ADS[REC[cat]]||{},all=ADS.coupang_all||{},now=today();
      var it=a.url?a:null;if(!it){var L=(all.items||[]).filter(function(x){return /^https:\/\//.test(x.url||'')&&!x.off&&(!x.until||x.until>=now);});if(!L.length)return;it=L[Math.floor(Math.random()*L.length)];}
      var box=D.createElement('aside');box.className='hl-reco';box.setAttribute('aria-label','추천 상품');
      var link=D.createElement('a');link.href=it.url;link.target='_blank';link.rel='noopener sponsored';
      if(it.banner){var im=D.createElement('img');im.src='/'+String(it.banner).replace(/^\//,'');im.alt=it.title||'쿠팡';im.loading='lazy';link.appendChild(im);}
      else{link.innerHTML='<b></b><span></span><em></em>';link.querySelector('b').textContent=it.title||'';link.querySelector('span').textContent=it.desc||'';link.querySelector('em').textContent=(a.button||'쿠팡에서 보기')+' →';}
      box.innerHTML='<span class="hl-reco-tag">AD · 쿠팡</span>';box.appendChild(link);
      var p=D.createElement('p');p.className='hl-reco-disc';p.textContent=(a.disclosure||all.disclosure||'');box.appendChild(p);
      var at=D.querySelector('.hl-share')||D.querySelector('.hl-rel')||D.querySelector('footer');
      if(at&&at.parentNode)at.parentNode.insertBefore(box,at);else D.body.appendChild(box);
    }catch(e){}}
    if(typeof ADS!=='undefined'){show();return;}
    var sc=D.createElement('script');sc.src='/ads.js';sc.onload=show;D.head.appendChild(sc);
  }
  // ── 내 정보 자동 채우기 (이 기기에만 저장) ──
  var PKEY='hlp1p',PF=[['salary',/연봉|연소득|총급여/],['monthly',/월급|월 급여|월 소득/],['age',/(만\s*)?나이/]],MONEY={salary:1,monthly:1};
  function nv(x){var v=parseFloat(String(x).replace(/[,\s원]/g,''));return isFinite(v)?v:NaN}
  function toWon(k,v){return MONEY[k]&&v<100000?v*10000:v}
  function fromWon(k,el,v){if(!MONEY[k])return String(v);var cur=nv(el.value||el.defaultValue);var x=(isFinite(cur)&&cur<100000)?v/10000:v;return String(Math.round(x)).replace(/\B(?=(\d{3})+(?!\d))/g,',')}
  function labelOf(el){var l=el.closest&&el.closest('label');if(l)return l.textContent;if(el.id){var f=D.querySelector('label[for="'+el.id+'"]');if(f)return f.textContent;}return el.getAttribute('aria-label')||'';}
  function keyOf(el){if(!el.matches||!el.matches('input[type=text],input[type=number],input[type=tel],input:not([type])'))return null;var t=labelOf(el);for(var i=0;i<PF.length;i++)if(PF[i][1].test(t))return PF[i][0];return null;}
  function profile(){
    var prof;try{prof=JSON.parse(localStorage.getItem(PKEY)||'{}')||{};}catch(e){prof={};}
    D.addEventListener('change',function(e){var k=keyOf(e.target);if(!k||inUI(e.target))return;var v=nv(e.target.value);if(!isFinite(v)||v<=0)return;prof[k]=toWon(k,v);try{localStorage.setItem(PKEY,JSON.stringify(prof));}catch(x){}},true);
    if(!seg.length)return;
    var fields=[].slice.call(D.querySelectorAll('input,select')).filter(function(el){var k=keyOf(el);return k&&prof[k]!=null&&nv(el.value)!==nv(fromWon(k,el,prof[k]));});
    if(!fields.length)return;
    var bar=D.createElement('div');bar.className='hl-prof';bar.innerHTML='<span>지난번에 입력한 내 정보(연봉·월급·나이)로 채울까요?</span><button type="button">채우기</button><button type="button" class="x" aria-label="닫기">×</button>';
    bar.querySelector('button').onclick=function(){fields.forEach(function(el){var k=keyOf(el);el.value=fromWon(k,el,prof[k]);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));});bar.remove();};
    bar.querySelector('.x').onclick=function(){bar.remove();};
    var f=fields[0].closest('form,section,.card')||fields[0].parentNode;f.parentNode.insertBefore(bar,f);
  }
  // ── 연말정산 시즌 안내 (11월~2월) ──
  function season(){
    var m=new Date().getMonth()+1;if(!(m>=11||m<=2))return;var cat=seg.length?pageCat():'home';
    if(!(cat==='home'||cat==='avatar'||cat==='save')||/^yearend$/.test(seg[0]||''))return;
    var y=new Date().getFullYear()+(m>=11?1:0),open=new Date(y,0,15),dd=Math.ceil((open-new Date())/864e5);
    var a=D.createElement('a');a.className='hl-season';a.href='/yearend/';
    a.innerHTML='<b>🧾 연말정산 시즌</b><span>'+(dd>0?'간소화 서비스 오픈 D-'+dd+' · ':'')+'지금 미리 계산하고 환급 늘리기 →</span>';
    var home=D.querySelector('.hl-home');if(home){home.insertBefore(a,home.firstChild);return;}
    var h=D.querySelector('main')||D.querySelector('.wrap');if(h)h.insertBefore(a,h.firstChild);
  }
  function boot(){drawFab(load());remember();attend();reco();profile();season();}
  if(D.readyState==='loading') D.addEventListener('DOMContentLoaded',boot); else boot();
})();
