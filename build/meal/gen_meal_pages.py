# 전국·시도별 급식 랭킹 페이지 → overlay/study/meal-ranking.html, overlay/study/meal/<slug>.html
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(os.path.dirname(H), 'newcats'))
import gen_maptools as G
from meal_common import SIDO, FULL
import importlib.util
_s = importlib.util.spec_from_file_location('fm', os.path.join(H, 'fetch_meal.py')); FM = importlib.util.module_from_spec(_s); sys.argv = sys.argv[:1]; _s.loader.exec_module(FM)

CSS = '''<style id="hl-meal">
.mr-sum{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:0 0 4px}
.mr-sum div{background:#F4F7FB;border-radius:12px;padding:12px 6px;text-align:center;min-width:0}
.mr-sum b{display:block;font-size:18px;color:var(--head);font-variant-numeric:tabular-nums;line-height:1.3;overflow-wrap:anywhere}
.mr-sum span{display:block;font-size:12.5px;color:var(--muted);margin-top:2px;word-break:keep-all}
.mr-rank{list-style:none;margin:6px 0 0;padding:0}
.mr-rank li{position:relative;display:grid;grid-template-columns:28px minmax(0,1fr) auto;gap:8px;align-items:center;padding:10px 10px;border-radius:10px;margin-top:4px;overflow:hidden;background:#F8FAFC}
.mr-rank .bar{position:absolute;left:0;top:0;bottom:0;background:#E3EEFF;z-index:0;border-radius:10px}
.mr-rank li>span{position:relative;z-index:1}
.mr-rank .rk{font-weight:800;color:#1B64DA;text-align:center;font-variant-numeric:tabular-nums}
.mr-rank li:nth-child(-n+3) .rk{color:#fff;background:#1B64DA;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:13.5px}
.mr-rank .nm{font-weight:700;color:var(--head);font-size:15.5px;overflow-wrap:anywhere;min-width:0}
.mr-rank .ct{font-weight:700;color:var(--ink);font-size:14px;white-space:nowrap;font-variant-numeric:tabular-nums;text-align:right}
.mr-rank .ct small{display:block;font-weight:500;color:var(--muted);font-size:12px}
.mr-rank.rise li{background:#FFF7ED}.mr-rank.rise .rk{color:#C2410C}.mr-rank.rise li:nth-child(-n+3) .rk{background:#EA580C;color:#fff}
.mr-empty{color:var(--muted);font-size:14.5px;margin:8px 0 0}
.mr-sido{list-style:none;margin:8px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px}
.mr-sido a{display:block;padding:12px;border:1px solid var(--line-s);border-radius:12px;text-decoration:none;background:#fff;min-height:44px;box-sizing:border-box}
.mr-sido b{display:block;color:var(--head);font-size:15px}.mr-sido span{display:block;color:#1B64DA;font-weight:700;font-size:13.5px;margin-top:3px;overflow-wrap:anywhere}
.mr-sido li.on a{border-color:#1B64DA;background:#EEF5FF}
.ms-row{display:grid;grid-template-columns:minmax(0,1fr);gap:8px;margin-top:10px}
.ms-row.two{grid-template-columns:110px minmax(0,1fr)}
.ms-row select,.ms-row input{font:inherit;font-size:16px;padding:10px 12px;border:1px solid var(--line-s);border-radius:10px;min-height:46px;width:100%;box-sizing:border-box;background:#fff;min-width:0}
.ms-sug{list-style:none;margin:4px 0 0;padding:0;border:1px solid var(--line-s);border-radius:10px;background:#fff;max-height:280px;overflow:auto}
.ms-sug button{display:block;width:100%;text-align:left;padding:10px 12px;border:0;border-top:1px solid var(--line-s);background:none;font:inherit;font-size:15px;cursor:pointer;color:var(--head)}
.ms-sug li:first-child button{border-top:0}.ms-sug small{color:var(--muted);margin-left:6px;font-size:12.5px}
.ms-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin:14px 0 4px}
.ms-head b{font-size:19px;color:var(--head)}.ms-head span{color:var(--muted);font-size:13.5px}
.ms-stat{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:8px}
.ms-stat div{border:1px solid var(--line-s);border-radius:12px;padding:10px 6px;text-align:center;min-width:0}
.ms-stat b{display:block;font-size:17px;color:var(--head);font-variant-numeric:tabular-nums;overflow-wrap:anywhere}
.ms-stat span{display:block;font-size:12px;color:var(--muted);margin-top:2px;word-break:keep-all}
.ms-stat em{display:block;font-style:normal;font-size:12px;font-weight:700;margin-top:3px}
.ms-stat em.up{color:#C2410C}.ms-stat em.dn{color:#1B64DA}
.ms-wk{display:flex;gap:6px;margin-top:12px}
.ms-wk button,.ms-acts button{font:inherit;font-size:14px;font-weight:700;border:1px solid var(--line-s);background:#fff;border-radius:999px;min-height:40px;padding:0 14px;cursor:pointer;color:var(--head)}
.ms-wk button[aria-pressed=true]{background:var(--head);color:#fff;border-color:var(--head)}
.ms-days{list-style:none;margin:10px 0 0;padding:0}
.ms-days>li{border:1px solid var(--line-s);border-radius:14px;padding:12px 14px;margin-top:8px}
.ms-days>li.today{border-color:#1B64DA;box-shadow:0 0 0 2px rgba(27,100,218,.12)}
.ms-days h3{margin:0 0 6px;font-size:15px;color:var(--head);display:flex;justify-content:space-between;gap:8px}
.ms-days h3 small{font-weight:500;color:var(--muted);font-size:12.5px;white-space:nowrap}
.ms-days .ml{font-size:12px;font-weight:800;color:#1B64DA;margin:8px 0 2px}
.ms-days ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.ms-days ul li{background:#F4F7FB;border-radius:8px;padding:5px 9px;font-size:14.5px;color:var(--ink);overflow-wrap:anywhere;max-width:100%;box-sizing:border-box}
.ms-days ul li.pop{background:#E3EEFF;color:#1B4FB0;font-weight:700}
.ms-days ul li.alg{background:#FEE2E2;color:#B91C1C;font-weight:700}
.ms-days ul li small{font-size:11.5px;margin-left:3px;opacity:.85}
.ms-none{color:var(--muted);font-size:14px}
.ms-acts{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.ms-alg summary{cursor:pointer;font-weight:700;color:var(--head);font-size:14.5px;margin-top:12px;min-height:32px}
.ms-alg div{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.ms-alg label{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--line-s);border-radius:999px;padding:6px 10px;font-size:13.5px;cursor:pointer;min-height:34px;box-sizing:border-box}
.ms-alg input{width:16px;height:16px;margin:0}
.ms-res{list-style:none;margin:10px 0 0;padding:0}
.ms-res li{padding:10px 4px;border-top:1px solid var(--line-s);font-size:14.5px;overflow-wrap:anywhere}
.ms-res li:first-child{border-top:0}.ms-res b{color:var(--head)}.ms-res span{color:var(--muted);font-size:13px;display:block}
.ms-res button{all:unset;cursor:pointer;display:block}
.ms-msg{font-size:14px;color:var(--muted);margin:10px 0 0}
</style>
'''

JS = r'''<script>
(function(){
var PAGE='%PAGE%',SIDO=%SIDO%,$=function(i){return document.getElementById(i)};
var ALG=['','난류','우유','메밀','땅콩','대두','밀','고등어','게','새우','돼지고기','복숭아','토마토','아황산류','호두','닭고기','쇠고기','오징어','조개류','잣'];
var DES=new RegExp(%DES%),RX=/\(\s*\d{1,2}(?:\s*[.,]\s*\d{1,2})*\s*\.?\s*\)/;
var C={},IDX=null,cur=null,wk=0,mine=[];try{mine=JSON.parse(localStorage.getItem('hl-meal-alg'))||[]}catch(e){}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function norm(s){s=s.replace(RX,'').replace(/[\*★☆♥♡#@&※◆◇■□●○▶►◀~!^`$%+=|\\\/]+/g,' ').trim().replace(/\((?:[가-힣A-Za-z]{1,4})\)\s*$/,'').replace(/^\d+[.)]?\s*/,'').replace(/([가-힣])\s*[A-Za-z]$/,'$1');return s.replace(/\s+/g,'').replace(/^[-_.,·:;]+|[-_.,·:;]+$/g,'').slice(0,24)}
function algOf(s){var m=s.match(RX);return m?m[0].replace(/[()\s]/g,'').split(/[.,]/).filter(Boolean).map(Number):[]}
function load(slug){if(C[slug])return Promise.resolve(C[slug]);return fetch('/data/meal/'+slug+'.json',{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){
 var pop={};(d.top||[]).forEach(function(t){pop[t[0]]=1});d.pop=pop;d.dn=d.dict.map(norm);
 var tot=0,cnt=0,dsum=0;Object.keys(d.meals).forEach(function(k){var ds=0,has=0;d.meals[k].forEach(function(m){if(m[0]>=5&&m[0]<10){has=1;m[2].forEach(function(i){if(DES.test(d.dn[i]))ds++})}});if(has){cnt++;dsum+=ds}});
 d.desAvg=cnt?dsum/cnt:0;return C[slug]=d})}
function sidoName(s){for(var i=0;i<SIDO.length;i++)if(SIDO[i][0]==s)return SIDO[i][1];return ''}
function dayLab(ds){var y=+ds.slice(0,4),m=+ds.slice(4,6),d=+ds.slice(6,8),w='일월화수목금토'[new Date(y,m-1,d).getDay()];return m+'/'+d+' ('+w+')'}
function todayS(){var t=new Date(Date.now()+9*3600e3);return t.toISOString().slice(0,10).replace(/-/g,'')}
// ── 우리 학교 ──
var selS=$('ms-sido'),q=$('ms-q'),sug=$('ms-sug');
if(selS){selS.innerHTML='<option value="">시·도</option>'+SIDO.map(function(s){return '<option value="'+s[0]+'">'+s[1]+'</option>'}).join('');}
function sidoSel(){return PAGE=='nat'?(selS.value||''):PAGE}
var t=null;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(find,200)});q.addEventListener('focus',function(){var s=sidoSel();if(s)load(s).catch(function(){})});
if(selS)selS.addEventListener('change',function(){if(selS.value)load(selS.value).catch(function(){});find();if(selS.value)$('mf-sido').value=selS.value});
function find(){var s=sidoSel(),v=q.value.replace(/\s/g,'');if(!s||v.length<1){sug.hidden=true;if(!s&&v)msg('먼저 시·도를 고르세요');return}
 load(s).then(function(d){var r=d.schools.filter(function(x){return x[1].replace(/\s/g,'').indexOf(v)>=0}).slice(0,30);
  sug.innerHTML=r.length?r.map(function(x){return '<li><button type="button" data-c="'+x[0]+'">'+esc(x[1])+'<small>'+esc(x[3]||'')+'</small></button></li>'}).join(''):'<li><button type="button" disabled>찾는 학교가 없어요. 이름 일부만 넣어 보세요</button></li>';sug.hidden=false;sug.dataset.s=s},function(){msg('급식 데이터를 불러오지 못했어요. 잠시 뒤 다시 해 주세요')})}
sug.addEventListener('click',function(e){var b=e.target.closest('button[data-c]');if(!b)return;sug.hidden=true;show(sug.dataset.s,b.dataset.c,true)});
function msg(m){$('ms-out').innerHTML='<p class="ms-msg">'+esc(m)+'</p>'}
function show(slug,code,save){load(slug).then(function(d){var s=null;for(var i=0;i<d.schools.length;i++)if(d.schools[i][0]==code){s=d.schools[i];break}
 if(!s){msg('학교를 찾지 못했어요');return}cur={slug:slug,code:code,d:d,s:s};if(save)try{localStorage.setItem('hl-meal-school',JSON.stringify({slug:slug,code:code}))}catch(e){}
 q.value=s[1];render()},function(){msg('급식 데이터를 불러오지 못했어요')})}
function render(){if(!cur)return;var d=cur.d,s=cur.s,ms=d.meals[cur.code]||[],td=todayS(),a0=5+wk*5;
 var cal=[],des=0,pop=0;ms.forEach(function(m){if(m[0]>=5&&m[0]<10){if(m[1]==2&&m[3])cal.push(m[3]);m[2].forEach(function(i){var n=d.dn[i];if(DES.test(n))des++;if(d.pop[n])pop++})}});
 var avg=cal.length?Math.round(cal.reduce(function(a,b){return a+b},0)/cal.length):0;
 function cmp(a,b,u){if(!a||!b)return '';var df=a-b;if(Math.abs(df)<(u=='kcal'?15:0.5))return '<em>'+sidoName(cur.slug)+' 평균과 비슷</em>';return '<em class="'+(df>0?'up':'dn')+'">'+sidoName(cur.slug)+' 평균보다 '+(u=='kcal'?Math.abs(df)+'kcal':Math.abs(df).toFixed(1)+'번')+' '+(df>0?'많음':'적음')+'</em>'}
 var h='<div class="ms-head"><b>'+esc(s[1])+'</b><span>'+esc(sidoName(cur.slug)+' '+(s[3]||''))+'</span></div>';
 h+='<div class="ms-stat"><div><b>'+(avg?avg.toLocaleString()+'kcal':'–')+'</b><span>이번 주 점심 평균</span>'+cmp(avg,d.avgCal,'kcal')+'</div><div><b>'+des+'번</b><span>이번 주 후식·디저트</span>'+cmp(des,d.desAvg,'n')+'</div><div><b>'+pop+'개</b><span>'+sidoName(cur.slug)+' 인기 TOP30 메뉴가 나온 수</span></div></div>';
 h+='<div class="ms-wk"><button type="button" data-w="0" aria-pressed="'+(wk==0)+'">이번 주</button><button type="button" data-w="1" aria-pressed="'+(wk==1)+'">다음 주</button></div><ul class="ms-days">';
 for(var di=a0;di<a0+5;di++){var ds=d.days[di];if(!ds)continue;var rows=ms.filter(function(m){return m[0]==di}).sort(function(a,b){return a[1]-b[1]});
  h+='<li'+(ds==td?' class="today"':'')+'><h3>'+dayLab(ds)+(ds==td?' · 오늘':'')+(function(){var l=rows.filter(function(r){return r[1]==2&&r[3]})[0];return l?'<small>점심 '+l[3]+'kcal</small>':''})()+'</h3>';
  if(!rows.length)h+='<p class="ms-none">급식 정보가 없어요 (방학·휴일이거나 아직 안 올라왔어요)</p>';
  rows.forEach(function(r){if(rows.length>1)h+='<p class="ml">'+(['','조식','중식','석식'][r[1]]||'')+'</p>';
   h+='<ul>'+r[2].map(function(i){var raw=d.dict[i],n=d.dn[i]||raw,al=algOf(raw),hit=al.filter(function(x){return mine.indexOf(x)>=0});
    return '<li class="'+(hit.length?'alg':(d.pop[n]?'pop':''))+'">'+esc(n)+(hit.length?'<small>⚠ '+hit.map(function(x){return ALG[x]}).join('·')+'</small>':'')+'</li>'}).join('')+'</ul>'});
  h+='</li>'}
 h+='</ul><div class="ms-acts"><button type="button" id="ms-share">이 학교 급식 링크 공유</button></div>';
 $('ms-out').innerHTML=h}
$('ms-out').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;if(b.dataset.w){wk=+b.dataset.w;render()}
 if(b.id=='ms-share'&&cur){var u=location.origin+'/study/meal/'+cur.slug+'.html?s='+cur.code,tt=cur.s[1]+' 이번 주 급식';if(navigator.share)navigator.share({title:tt,url:u}).catch(function(){});else if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){b.textContent='링크 복사됨'})}});
// 알레르기
var ab=$('ms-algs');ab.innerHTML=ALG.slice(1).map(function(n,i){return '<label><input type="checkbox" value="'+(i+1)+'"'+(mine.indexOf(i+1)>=0?' checked':'')+'>'+n+'</label>'}).join('');
ab.addEventListener('change',function(){mine=[].slice.call(ab.querySelectorAll('input:checked')).map(function(x){return +x.value});try{localStorage.setItem('hl-meal-alg',JSON.stringify(mine))}catch(e){}render()});
// 메뉴로 학교 찾기
var fs=$('mf-sido'),fq=$('mf-q');if(fs){fs.innerHTML='<option value="">시·도</option>'+SIDO.map(function(s){return '<option value="'+s[0]+'">'+s[1]+'</option>'}).join('')}
function ffind(){var s=PAGE=='nat'?fs.value:PAGE,v=norm(fq.value);if(!s){$('mf-out').innerHTML='<p class="ms-msg">시·도를 고르세요</p>';return}if(v.length<1){$('mf-out').innerHTML='';return}
 $('mf-out').innerHTML='<p class="ms-msg">찾는 중…</p>';
 load(s).then(function(d){var hit=[];d.dn.forEach(function(n,i){if(n.indexOf(v)>=0)hit.push(i)});var hs={};hit.forEach(function(i){hs[i]=1});var out=[];
  d.schools.forEach(function(x){var ms=d.meals[x[0]]||[],f=null;for(var k=0;k<ms.length;k++){var m=ms[k];if(m[0]<5)continue;for(var j=0;j<m[2].length;j++)if(hs[m[2][j]]){f=[m[0],d.dn[m[2][j]]];break}if(f)break}if(f)out.push([x,f])});
  out.sort(function(a,b){return a[1][0]-b[1][0]});
  $('mf-out').innerHTML='<p class="ms-msg">'+sidoName(s)+'에서 이번 주·다음 주에 ‘'+esc(fq.value.trim())+'’ 나오는 학교 <b>'+out.length.toLocaleString()+'곳</b></p><ul class="ms-res">'+out.slice(0,60).map(function(o){return '<li><button type="button" data-s="'+s+'" data-c="'+o[0][0]+'"><b>'+esc(o[0][1])+'</b><span>'+dayLab(d.days[o[1][0]])+' · '+esc(o[1][1])+(o[0][3]?' · '+esc(o[0][3]):'')+'</span></button></li>'}).join('')+'</ul>'+(out.length>60?'<p class="ms-msg">60곳까지만 보여 줘요. 검색어를 더 자세히 넣어 보세요.</p>':'')},function(){$('mf-out').innerHTML='<p class="ms-msg">데이터를 불러오지 못했어요</p>'})}
var ft=null;fq.addEventListener('input',function(){clearTimeout(ft);ft=setTimeout(ffind,300)});if(fs)fs.addEventListener('change',ffind);
$('mf-out').addEventListener('click',function(e){var b=e.target.closest('button[data-c]');if(!b)return;if(selS)selS.value=b.dataset.s;show(b.dataset.s,b.dataset.c,true);$('ms-card').scrollIntoView({behavior:'smooth',block:'start'})});
// 처음 열 때: ?s=학교코드 또는 저장한 우리 학교
var sp=new URLSearchParams(location.search).get('s'),sv=null;try{sv=JSON.parse(localStorage.getItem('hl-meal-school'))}catch(e){}
if(sp&&PAGE!='nat')show(PAGE,sp,true);else if(sv&&sv.slug&&(PAGE=='nat'||PAGE==sv.slug)){if(selS)selS.value=sv.slug;show(sv.slug,sv.code,false)}
if(PAGE!='nat'&&fs==null){}
})();
</script>
'''

def main_html(page, name):
    scope = '전국' if page == 'nat' else name
    sel = '<select id="ms-sido" aria-label="시·도"></select>' if page == 'nat' else ''
    fsel = '<select id="mf-sido" aria-label="시·도"></select>' if page == 'nat' else ''
    two = ' two' if page == 'nat' else ''
    out = f'''<section class="card tool" id="ms-card"><h2>우리 학교 이번 주 급식</h2>
<p class="ms-msg" style="margin-top:0">학교를 한 번 고르면 다음에 열 때 바로 보여요. {scope} 평균과 비교하고, 알레르기 음식은 빨갛게 표시해요.</p>
<div class="ms-row{two}">{sel}<input id="ms-q" placeholder="학교 이름 (예: 송도중)" autocomplete="off" aria-label="학교 이름"></div>
<ul class="ms-sug" id="ms-sug" hidden></ul>
<div id="ms-out"></div>
<details class="ms-alg"><summary>알레르기 표시할 음식 고르기</summary><div id="ms-algs"></div></details>
</section>
<section class="card"><h2>{scope} 이번 주 급식 TOP 20</h2>
<div class="mr-sum"><div><b><!--M:served-->–<!--/M:served--></b><span>급식 나온 학교</span></div><div><b><!--M:cal-->–<!--/M:cal-->kcal</b><span>점심 평균 열량</span></div><div><b><!--M:label-->–<!--/M:label--></b><span>기준 주</span></div></div>
<!--M:top--><p class="mr-empty">이번 주 데이터를 모으는 중이에요.</p><!--/M:top-->
<p class="ms-msg">밥·김치·우유처럼 매일 나오는 기본 메뉴는 빼고, 그 메뉴가 한 번이라도 나온 학교 수로 셌어요. 마지막 업데이트 <!--M:updated-->–<!--/M:updated--></p>
</section>
<section class="card"><h2>{scope} 후식·디저트 TOP 10</h2><!--M:dessert--><p class="mr-empty">이번 주 데이터를 모으는 중이에요.</p><!--/M:dessert--></section>
<section class="card"><h2>이번 주 새로 뜬 메뉴</h2><p class="ms-msg" style="margin-top:0">지난주보다 나온 학교가 크게 늘어난 메뉴예요.</p><!--M:rising--><p class="mr-empty">이번 주 데이터를 모으는 중이에요.</p><!--/M:rising--></section>
<section class="card"><h2>메뉴로 학교 찾기</h2><p class="ms-msg" style="margin-top:0">이번 주와 다음 주에 그 메뉴가 나오는 학교를 찾아요. 예: 마라탕, 탕후루, 피자</p>
<div class="ms-row{two}">{fsel}<input id="mf-q" placeholder="메뉴 이름" autocomplete="off" aria-label="메뉴 이름"></div><div id="mf-out"></div></section>
<section class="card"><h2>{"시·도별 이번 주 1위" if page == "nat" else "다른 지역 급식 랭킹"}</h2><!--M:sido--><!--/M:sido-->
{"" if page == "nat" else '<p class="ms-msg"><a href="/study/meal-ranking.html">전국 급식 랭킹 보기</a></p>'}</section>
<section class="card"><h2>이렇게 모았어요</h2><ul class="xp">
<li><b>데이터</b>: 나이스 교육정보 개방 포털에 학교가 올린 급식 식단을 매일 새벽에 모아요. 학교가 늦게 올리면 하루 늦게 반영될 수 있어요.</li>
<li><b>순위</b>: 이번 주 월~금에 그 메뉴가 한 번이라도 나온 학교 수예요. 같은 학교에서 두 번 나와도 한 번으로 셌어요.</li>
<li><b>메뉴 이름</b>: 알레르기 번호와 꾸밈 기호를 빼고 같은 이름끼리 묶었어요. ‘돈까스’와 ‘돈가스’처럼 학교마다 쓰는 이름이 다르면 따로 세어져요.</li>
<li><b>토요일·일요일</b>에는 다음 주 식단으로 바뀌어요.</li></ul></section>
'''
    return out

FAQ = [('급식 정보는 어디서 가져오나요?', '나이스 교육정보 개방 포털의 학교 급식 식단 정보예요. 전국 초·중·고·특수학교가 직접 올린 식단을 매일 새벽에 모아요.'),
       ('우리 학교가 안 나와요.', '학교 이름의 일부만 넣어 보세요(예: 송도중). 급식을 하지 않거나 식단을 나이스에 올리지 않는 학교는 나오지 않을 수 있어요.'),
       ('순위는 어떻게 정하나요?', '이번 주 월~금에 그 메뉴가 나온 학교 수로 정해요. 밥·김치·우유처럼 매일 나오는 기본 메뉴는 뺐어요.'),
       ('알레르기 표시는 정확한가요?', '학교가 식단에 적은 알레르기 번호를 그대로 읽어서 표시해요. 실제 재료는 학교 공지와 영양 선생님 안내를 꼭 함께 확인하세요.')]

def build():
    sid = json.dumps(SIDO, ensure_ascii=False); des = json.dumps(FM.DES.pattern, ensure_ascii=False)
    css = CSS
    rel = [('/study/meal-ranking.html', '전국 급식 랭킹', '이번 주 전국 학교 급식 TOP 20')] + [(f'/study/meal/{s}.html', f'{n} 급식 랭킹', f'{n} 학교 이번 주 인기 메뉴') for s, n in SIDO[:5]]
    G.shell('meal-ranking', '전국 학교 급식 랭킹 · 이번 주 가장 많이 나온 메뉴 TOP 20 | 홍라이프 도구',
            '전국 초·중·고 급식을 매일 모아 이번 주 가장 많이 나온 메뉴, 후식 TOP 10, 새로 뜬 메뉴를 보여 줘요. 우리 학교 이번 주 급식, 지역 평균 비교, 메뉴로 학교 찾기까지.',
            '전국 학교 급식 랭킹', '전국 초·중·고 급식을 매일 모아서 이번 주 가장 많이 나온 메뉴를 세었어요. 우리 학교 급식과 지역 평균도 비교해 보세요.',
            css, main_html('nat', '전국'), JS.replace('%PAGE%', 'nat').replace('%SIDO%', sid).replace('%DES%', des), FAQ,
            crumb=('학생·공부', '/study/'), dirn='study', rel=rel)
    for slug, name in SIDO:
        G.shell(slug, f'{name} 학교 급식 랭킹 · 이번 주 인기 메뉴 TOP 20, 우리 학교 급식 | 홍라이프 도구',
                f'{FULL[name]} 초·중·고 급식을 매일 모아 이번 주 가장 많이 나온 메뉴, 후식 TOP 10, 새로 뜬 메뉴를 보여 줘요. 우리 학교 이번 주·다음 주 급식과 {name} 평균 비교까지.',
                f'{name} 학교 급식 랭킹', f'{FULL[name]} 학교 급식을 매일 모아서 이번 주 가장 많이 나온 메뉴를 세었어요. 우리 학교 이번 주 급식도 바로 볼 수 있어요.',
                css, main_html(slug, name), JS.replace('%PAGE%', slug).replace('%SIDO%', sid).replace('%DES%', des), FAQ,
                crumb=('전국 급식 랭킹', '/study/meal-ranking.html'), dirn='study/meal', rel=[r for r in rel if r[0] != f'/study/meal/{slug}.html'][:1] + [(f'/study/meal/{s}.html', f'{n} 급식 랭킹', f'{n} 이번 주 인기 메뉴') for s, n in SIDO if s != slug][:4])

if __name__ == '__main__':
    build()
