/* Hong Life: link calculators to matching "result by amount" pages */
!function(){var d=document,P=location.pathname.replace(/\/index\.html$/,'/');
function n(v){return parseFloat(String(v||'').replace(/[^\d.]/g,''))}
function cl(x,a,b){return Math.max(a,Math.min(b,x))}
var C={
'/salary-net.html':{i:'sal',t:'result',f:function(v){if(!(v>0))return;var k=v<=10000?Math.round(cl(v,2000,10000)/100)*100:Math.round(cl(v,10000,15000)/500)*500;return['/salary/'+k+'.html','📊 연봉 '+k.toLocaleString('ko-KR')+'만 원 실수령액, 그림으로 자세히 보기']}},
'/wage.html':{i:'wage',t:'out',f:function(v){if(!(v>0))return;var k=Math.abs(v-10320)<150?10320:Math.abs(v-10700)<150?10700:Math.round(cl(v,10000,30000)/500)*500;return['/hourly/'+k+'.html','📊 시급 '+k.toLocaleString('ko-KR')+'원이면 월급·연봉은? 그림으로 보기']}},
'/pyeong.html':{i:'m2',t:null,f:function(v){if(!(v>0))return;var k=Math.round(cl(v/3.305785,5,100));return['/py/'+k+'.html','📐 '+k+'평은 몇 ㎡? 평면도 그림으로 보기']}},
'/age-table.html':{i:'birth',t:'result',f:function(v){var y=parseInt(String(v).slice(0,4),10);if(!(y>=1940&&y<=2026))return;return['/born/'+y+'.html','🐾 '+y+'년생 나이·띠, 그림으로 자세히 보기']}}
};
var c=C[P];if(!c)return;var inp=d.getElementById(c.i);if(!inp)return;
var st=d.createElement('style');st.textContent='.hl-dl{display:block;margin:14px 0;padding:14px 16px;border-radius:12px;background:#12305C;color:#fff!important;text-decoration:none;font-weight:700;font-size:15px;line-height:1.4;border-left:5px solid #C9A04A;box-shadow:0 2px 10px rgba(11,31,63,.15)}.hl-dl:after{content:" →";color:#E8C27A}.hl-dl:hover{background:#1B427A}html.hl-embed .hl-dl{display:none}';d.head.appendChild(st);
var a=d.createElement('a');a.className='hl-dl';a.hidden=true;
var tg=c.t&&d.getElementById(c.t);var host=tg||inp.closest('.card,section,form')||inp.parentNode;host.parentNode.insertBefore(a,host.nextSibling);
function up(){var r=c.f(c.i==='birth'?inp.value:n(inp.value));if(!r){a.hidden=true;return}a.href=r[0];a.textContent=r[1];a.hidden=false}
['input','change'].forEach(function(e){inp.addEventListener(e,up)});d.addEventListener('submit',function(){setTimeout(up,50)},true);up();
a.addEventListener('click',function(){try{gtag('event','deeplink',{to:a.getAttribute('href')})}catch(e){}});
}();
