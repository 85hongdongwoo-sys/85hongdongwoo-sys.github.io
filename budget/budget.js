/* Honglife Budget — one app, many languages. Data stays in this browser (localStorage). */
(function(){
'use strict';
const L=window.L,$=id=>document.getElementById(id);
const KEY='hl_budget_v1';
let S={items:[],budget:0,cur:L.cur};
try{const s=JSON.parse(localStorage.getItem(KEY)||'null');if(s&&Array.isArray(s.items))S=Object.assign(S,s)}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const CUR={KRW:0,JPY:0,IDR:0,VND:0,USD:2,EUR:2,GBP:2,INR:2,THB:2,BRL:2,MXN:2,AUD:2,CAD:2,PHP:2};
const money=x=>{const d=CUR[S.cur]??2;try{return new Intl.NumberFormat(L.locale,{style:'currency',currency:S.cur,maximumFractionDigits:d,minimumFractionDigits:0}).format(x)}catch(e){return x.toFixed(d)+' '+S.cur}};
const today=new Date();let ym=today.toISOString().slice(0,7);
const COLORS=['#12305C','#C9A04A','#2E7D6B','#B4322B','#5B6B8C','#E0A458','#3E8EB0','#8C6D3F','#94A3B8','#7A4E8C'];
function fillCats(){const t=$('type').value;$('cat').innerHTML=(t==='in'?L.catsIn:L.catsOut).map((c,i)=>`<option value="${i}">${c}</option>`).join('')}
function monthLabel(){const [y,m]=ym.split('-').map(Number);return new Date(y,m-1,1).toLocaleDateString(L.locale,{year:'numeric',month:'long'})}
function render(){
  $('month').textContent=monthLabel();
  const list=S.items.filter(x=>x.d.startsWith(ym)).sort((a,b)=>b.d.localeCompare(a.d)||b.t-a.t);
  const inc=list.filter(x=>x.k==='in').reduce((s,x)=>s+x.a,0),exp=list.filter(x=>x.k==='out').reduce((s,x)=>s+x.a,0);
  $('sumIn').textContent=money(inc);$('sumOut').textContent=money(exp);$('sumBal').textContent=money(inc-exp);$('sumBal').className=inc-exp<0?'neg':'pos';
  // budget
  const b=S.budget;const bw=$('budgetBar');
  if(b>0){const r=exp/b;bw.hidden=false;$('budgetFill').style.width=Math.min(100,r*100)+'%';$('budgetFill').className=r>1?'over':r>.8?'warn':'';
    const [y,m]=ym.split('-').map(Number);const days=new Date(y,m,0).getDate();const isCur=ym===today.toISOString().slice(0,7);const left=isCur?days-today.getDate()+1:0;
    $('budgetTxt').textContent=r>1?L.over.replace('{x}',money(exp-b)):L.left.replace('{x}',money(b-exp))+(isCur&&left>0?' · '+L.perDay.replace('{x}',money((b-exp)/left)):'')}else bw.hidden=true;
  // categories
  const byCat={};list.filter(x=>x.k==='out').forEach(x=>byCat[x.c]=(byCat[x.c]||0)+x.a);
  const cats=Object.entries(byCat).sort((a,b)=>b[1]-a[1]);
  $('cats').innerHTML=cats.length?cats.map(([c,v],i)=>`<div class="crow"><span class="dot" style="background:${COLORS[c%10]}"></span><span>${L.catsOut[c]}</span><span class="pct">${(v/exp*100).toFixed(0)}%</span><b>${money(v)}</b><i style="width:${v/cats[0][1]*100}%;background:${COLORS[c%10]}"></i></div>`).join(''):`<p class="empty">${L.noData}</p>`;
  // list
  $('list').innerHTML=list.length?list.map(x=>`<li><span class="d">${x.d.slice(5).replace('-','/')}</span><span class="c">${(x.k==='in'?L.catsIn:L.catsOut)[x.c]}${x.m?`<small>${esc(x.m)}</small>`:''}</span><b class="${x.k==='in'?'pos':'neg'}">${x.k==='in'?'+':'−'}${money(x.a)}</b><button data-del="${x.t}" aria-label="${L.del}">×</button></li>`).join(''):`<li class="empty">${L.noData}</li>`;
  // 6-month trend
  const months=[];const [y0,m0]=ym.split('-').map(Number);for(let k=5;k>=0;k--){const d=new Date(y0,m0-1-k,1);months.push(d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0'))}
  const tr=months.map(mm=>{const l=S.items.filter(x=>x.d.startsWith(mm));return [mm,l.filter(x=>x.k==='in').reduce((s,x)=>s+x.a,0),l.filter(x=>x.k==='out').reduce((s,x)=>s+x.a,0)]});
  const mx=Math.max(1,...tr.map(t=>Math.max(t[1],t[2])));
  $('trend').innerHTML=tr.map(t=>`<div class="tcol"><div class="tb"><i class="ti" style="height:${t[1]/mx*100}%"></i><i class="to" style="height:${t[2]/mx*100}%"></i></div><span>${Number(t[0].slice(5))}</span></div>`).join('');
  {const lab=s=>{const e=$(s);return e&&e.previousElementSibling?e.previousElementSibling.textContent:''};const box=$('trend');let lg=box.nextElementSibling;if(!lg||!lg.classList.contains('tleg')){lg=document.createElement('div');lg.className='tleg';box.after(lg)}lg.innerHTML=`<span><i style="background:#12305C"></i>${lab('sumIn')}</span><span><i style="background:#C9A04A"></i>${lab('sumOut')}</span>`+(tr.every(t=>!t[1]&&!t[2])?`<span style="margin-left:auto">${L.noData}</span>`:'');}
}
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
$('type').addEventListener('change',fillCats);
$('form').addEventListener('submit',e=>{e.preventDefault();const a=parseFloat(String($('amt').value).replace(/[^\d.,-]/g,'').replace(/,/g,''));if(!(a>0)){$('amt').focus();return}
  S.items.push({t:Date.now(),d:$('date').value||today.toISOString().slice(0,10),k:$('type').value,c:+$('cat').value,a,m:$('memo').value.trim().slice(0,60)});save();$('amt').value='';$('memo').value='';ym=$('date').value.slice(0,7)||ym;render();$('amt').focus();
  try{gtag('event','budget_add')}catch(e){}});
$('list').addEventListener('click',e=>{const t=e.target.dataset.del;if(!t)return;S.items=S.items.filter(x=>String(x.t)!==t);save();render()});
$('prev').onclick=()=>{const [y,m]=ym.split('-').map(Number);const d=new Date(y,m-2,1);ym=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');render()};
$('next').onclick=()=>{const [y,m]=ym.split('-').map(Number);const d=new Date(y,m,1);ym=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');render()};
$('budget').value=S.budget||'';$('budget').addEventListener('input',()=>{S.budget=parseFloat($('budget').value)||0;save();render()});
$('currency').value=S.cur;$('currency').addEventListener('change',()=>{S.cur=$('currency').value;save();render()});
$('csv').onclick=()=>{const rows=[['date','type','category','amount','memo']].concat(S.items.map(x=>[x.d,x.k==='in'?'income':'expense',(x.k==='in'?L.catsIn:L.catsOut)[x.c],x.a,x.m||'']));
  const csv='﻿'+rows.map(r=>r.map(v=>`"${String(v).replace(/"/g,'""')}"`).join(',')).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='budget.csv';a.click()};
$('csvIn').addEventListener('change',async e=>{const f=e.target.files[0];if(!f)return;const txt=(await f.text()).replace(/^﻿/,'');let n=0;
  txt.split(/\r?\n/).slice(1).forEach(line=>{const v=(line.match(/("([^"]|"")*"|[^,]*)(,|$)/g)||[]).map(s=>s.replace(/,$/,'').replace(/^"|"$/g,'').replace(/""/g,'"'));if(v.length<4||!/^\d{4}-\d{2}-\d{2}$/.test(v[0]))return;
    const k=/^inc|수입/i.test(v[1])?'in':'out';const arr=k==='in'?L.catsIn:L.catsOut;let c=arr.indexOf(v[2]);if(c<0)c=arr.length-1;const a=parseFloat(v[3]);if(a>0){S.items.push({t:Date.now()+n,d:v[0],k,c,a,m:v[4]||''});n++}});
  save();render();alertBox(L.imported.replace('{n}',n))});
$('reset').onclick=()=>{if($('reset').dataset.ok){S.items=[];save();render();$('reset').textContent=L.reset;delete $('reset').dataset.ok}else{$('reset').dataset.ok=1;$('reset').textContent=L.confirm}};
function alertBox(t){const b=$('toast');b.textContent=t;b.hidden=false;setTimeout(()=>b.hidden=true,2500)}
$('date').value=today.toISOString().slice(0,10);fillCats();render();
})();
