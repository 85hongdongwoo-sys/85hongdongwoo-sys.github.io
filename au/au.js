/* Honglife Australia calculators — 2026-27 income year (1 July 2026 – 30 June 2027) */
(function(){
'use strict';
const T={br:[[18200,0],[45000,.15],[135000,.30],[190000,.37],[Infinity,.45]],med:.02,medLow:28011,medHigh:35014,
  helpTh:69528,help2:129717,help3:186050,sg:.12,ccCap:30000,cgtDisc:.5};
window.AU2627=T;
const $=id=>document.getElementById(id);
const num=id=>{const e=$(id);if(!e)return 0;const v=parseFloat(String(e.value).replace(/[,$%\s]/g,''));return isFinite(v)?v:0};
const val=n=>{const c=document.querySelector(`input[name="${n}"]:checked`);return c?c.value:($(n)?$(n).value:'')};
const aud=(x,d=0)=>(x<0?'−':'')+'$'+Math.abs(x).toLocaleString('en-AU',{minimumFractionDigits:d,maximumFractionDigits:d});
const pc=(x,d=1)=>(x*100).toFixed(d)+'%';
const kv=rows=>'<div class="kv">'+rows.map(r=>`<div class="${r[2]||''}">${r[0]}</div><div class="${r[2]||''}">${r[1]}</div>`).join('')+'</div>';
const big=(l,v,s)=>`<div class="big"><span>${l}</span><b>${v}</b>${s?`<em>${s}</em>`:''}</div>`;
const bar=parts=>{const tot=parts.reduce((s,p)=>s+Math.max(0,p[1]),0)||1;return '<div class="bar">'+parts.map(p=>`<i style="width:${Math.max(0,p[1])/tot*100}%;background:${p[2]}"></i>`).join('')+'</div><div class="legend">'+parts.map(p=>`<span style="--c:${p[2]}">${p[0]} ${aud(p[1])}</span>`).join('')+'</div>'};
function bands(x,b){let t=0,lo=0;for(const [hi,r] of b){if(x>lo)t+=(Math.min(x,hi)-lo)*r;lo=hi}return t}
function lito(ti){if(ti<=37500)return 700;if(ti<=45000)return 700-(ti-37500)*.05;if(ti<=66667)return Math.max(0,325-(ti-45000)*.015);return 0}
function medicare(ti){if(ti<=T.medLow)return 0;if(ti<=T.medHigh)return (ti-T.medLow)*.10;return ti*T.med}
function help(ri){if(ri<=T.helpTh)return 0;if(ri<=T.help2)return (ri-T.helpTh)*.15;if(ri<=T.help3)return 9028+(ri-T.help2)*.17;return ri*.10}
function tax(ti){return Math.max(0,bands(ti,T.br)-lito(ti))}
window.AUTax={tax,medicare,help,lito};
function calcPay(){
  const sal=num('salary'),inclSuper=val('super')==='incl',hasHelp=val('help')==='y',per=+val('freq'),ss=num('salsac');
  const base=inclSuper?sal/(1+T.sg):sal;const sg=base*T.sg;const ti=Math.max(0,base-ss);
  const it=tax(ti),ml=medicare(ti),hp=hasHelp?help(ti+ss):0;const net=ti-it-ml-hp;
  let html=big(`Take-home pay per ${per===12?'month':per===26?'fortnight':'week'}`,aud(net/per,2),`${aud(net)} a year · plus ${aud(sg+ss)} into super`);
  html+=kv([['Base salary (excl. super)',aud(base)],['Salary sacrificed to super',aud(-ss),'neg'],['Taxable income',aud(ti)],['Income tax (after LITO '+aud(lito(ti))+')',aud(-it),'neg'],['Medicare levy (2%)',aud(-ml),'neg'],['HELP / HECS repayment',aud(-hp),'neg'],['Take-home (year)',aud(net),'t'],['Employer super guarantee (12%)',aud(sg),'pos']]);
  html+=bar([['Take-home',net,'#0F8A5F'],['Income tax',it,'#00205B'],['Medicare',ml,'#B8860B'],['HELP',hp,'#A0AEC8']]);
  html+='<p class="note">2026-27 resident rates: nil to $18,200; 15% to $45,000 (down from 16%); 30% to $135,000; 37% to $190,000; 45% above. Includes the low income tax offset, Medicare levy with the low-income phase-in ($28,011 for singles) and the 2026-27 marginal HELP repayment system. Medicare levy surcharge (no private hospital cover above ~$101k) is not included.</p>';
  $('out').innerHTML=html;
}
function calcCGT(){
  const inc=num('income'),gain=num('gain'),held=val('held')==='y',loss=num('loss');const net=Math.max(0,gain-loss);const disc=held?net*T.cgtDisc:0;const taxable=net-disc;
  const t=(tax(inc+taxable)+medicare(inc+taxable))-(tax(inc)+medicare(inc));
  let html=big('Tax on your capital gain',aud(t,2),net?`Effective ${pc(t/net)} · you keep ${aud(net-t)}`:'');
  html+=kv([['Capital gain after losses',aud(net)],['50% CGT discount',aud(-disc),'pos'],['Net capital gain added to income',aud(taxable)],['Extra income tax + Medicare',aud(t,2),'t']]);
  html+='<p class="note">Australia has no separate CGT rate: the net capital gain is added to your taxable income. Individuals who held the asset at least 12 months get a 50% discount. The 2026 Budget proposed replacing the discount with inflation indexation from 1 July 2027 — not yet law.</p>';
  $('out').innerHTML=html;
}
function calcSuper(){
  const age=num('age'),ret=num('retAge'),sal=num('salary'),bal0=num('balance'),r=num('ret')/100,fee=num('fees')/100,extra=num('extra'),g=num('raise')/100;
  let bal=bal0,s=sal,rows=[],contrib=0;
  for(let a=age;a<ret;a++){const cc=Math.min(T.ccCap,s*T.sg+extra);const netC=cc*(1-.15);bal=bal*(1+r-fee)+netC*(1+(r-fee)/2);contrib+=netC;if((a-age)%5===4||a===ret-1)rows.push([a+1,bal]);s*=1+g}
  let html=big(`Super balance at ${ret}`,aud(bal),`Today's dollars not adjusted · net contributions ${aud(contrib)}`);
  html+=kv([['Employer contributions now (12%)',aud(sal*T.sg)],['Extra concessional contributions',aud(extra)],['15% contributions tax (first year)',aud(-Math.min(T.ccCap,sal*T.sg+extra)*.15),'neg'],['Concessional cap 2026-27',aud(T.ccCap)],['Projected balance',aud(bal),'t']]);
  html+='<table class="tbl"><tr><th>Age</th><th>Balance</th></tr>'+rows.map(r=>`<tr><td>${r[0]}</td><td>${aud(r[1])}</td></tr>`).join('')+'</table>';
  html+='<p class="note">Super guarantee is 12% of ordinary time earnings. Concessional (before-tax) contributions are taxed at 15% inside the fund and capped at $30,000 a year; earnings are taxed at up to 15% (shown here through the net return).</p>';
  $('out').innerHTML=html;
}
function calcMort(){
  const price=num('price'),dep=num('deposit')/100,rate=num('rate')/100,yrs=num('years'),freq=val('pfreq');
  const loan=price*(1-dep),n=yrs*12,mr=rate/12;const pay=loan*mr/(1-Math.pow(1+mr,-n));
  const fn=freq==='f'?pay/2:pay;let bal=loan,int=0,k=0;const per=freq==='f'?26:12,rr=rate/per;while(bal>0.5&&k<per*yrs){const i=bal*rr;bal-=fn-i;int+=i;k++}
  let html=big(freq==='f'?'Fortnightly repayment':'Monthly repayment',aud(fn,2),`Loan ${aud(loan)} · paid off in ${(k/per).toFixed(1)} years`);
  html+=kv([['Deposit',aud(price*dep)],['Loan amount (LVR '+pc(1-dep,0)+')',aud(loan)],['Total interest',aud(int)],['Paid off in',`${(k/per).toFixed(1)} years`,'t']].concat(dep<.2?[['Lenders mortgage insurance','Usually charged below 20% deposit','neg']]:[]));
  html+='<p class="note">Paying half the monthly amount every fortnight gives 26 payments a year (13 months’ worth), cutting years off the loan. Stamp duty differs by state and is not included.</p>';
  $('out').innerHTML=html;
}
const PAGES={pay:calcPay,cgt:calcCGT,sup:calcSuper,mort:calcMort};
const fn=PAGES[document.body.dataset.page];
if(fn){const f=$('form');const run=()=>{try{fn()}catch(e){console.error(e)}};f.addEventListener('input',run);f.addEventListener('change',run);run()}
})();
