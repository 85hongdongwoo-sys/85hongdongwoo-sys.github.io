/* 홍라이프 세금 계산기 공통 */
var TX=(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
function num(id){var e=$(id);if(!e)return 0;var v=parseFloat(String(e.value).replace(/[^\d.\-]/g,''));return isFinite(v)?v:0}
function won(n){return (n<0?'−':'')+Math.abs(Math.round(n)).toLocaleString('ko-KR')+'원'}
function man(n){var a=Math.abs(n),s=n<0?'−':'';if(a>=1e8){var e=Math.floor(a/1e8),r=Math.round((a-e*1e8)/1e4);return s+e+'억'+(r?' '+r.toLocaleString('ko-KR')+'만':'')+'원'}if(a>=1e4)return s+Math.round(a/1e4).toLocaleString('ko-KR')+'만원';return won(n)}
/* 종합소득세·양도소득세 기본세율 (2023년 이후) */
var INCOME=[[14e6,.06,0],[50e6,.15,1.26e6],[88e6,.24,5.76e6],[150e6,.35,15.44e6],[300e6,.38,19.94e6],[500e6,.40,25.94e6],[1e9,.42,35.94e6],[Infinity,.45,65.94e6]];
/* 상속·증여세율 */
var GIFT=[[1e8,.10,0],[5e8,.20,1e7],[10e8,.30,6e7],[30e8,.40,1.6e8],[Infinity,.50,4.6e8]];
function prog(x,T){if(x<=0)return {tax:0,rate:T[0][1]};for(var i=0;i<T.length;i++)if(x<=T[i][0])return {tax:x*T[i][1]-T[i][2],rate:T[i][1]};}
function kv(rows){return '<table class="kv">'+rows.map(function(r){return '<tr class="'+(r[2]||'')+'"><td>'+r[0]+(r[3]?'<small>'+r[3]+'</small>':'')+'</td><td>'+r[1]+'</td></tr>'}).join('')+'</table>'}
function score(items){return '<div class="score">'+items.map(function(i){return '<div><span>'+i[0]+'</span><b>'+i[1]+'</b>'+(i[2]?'<em>'+i[2]+'</em>':'')+'</div>'}).join('')+'</div>'}
function bind(formId,fn){var f=$(formId);var run=function(){try{fn()}catch(e){console.error(e)}};f.addEventListener('input',run);f.addEventListener('change',run);run()}
function tabs(){document.querySelectorAll('.tabs').forEach(function(t){var bs=t.querySelectorAll('button');bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.setAttribute('aria-selected',String(x===b));var p=$(x.dataset.p);if(p)p.hidden=x!==b});if(window.onTab)window.onTab(b.dataset.p)})})})}
/* 숫자 입력 콤마 */
document.addEventListener('blur',function(e){var el=e.target;if(el.matches&&el.matches('input[data-money]')){var v=parseFloat(String(el.value).replace(/[^\d.\-]/g,''));if(isFinite(v))el.value=v.toLocaleString('ko-KR')}},true);
return {$:$,num:num,won:won,man:man,INCOME:INCOME,GIFT:GIFT,prog:prog,kv:kv,score:score,bind:bind,tabs:tabs};
})();
