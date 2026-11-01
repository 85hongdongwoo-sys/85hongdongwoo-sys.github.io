/* Honglife Canada calculators — 2026 tax year, federal + Ontario (CRA T4032ON, January 2026) */
(function(){
'use strict';
const T={fed:[[58523,.14],[117045,.205],[181440,.26],[258482,.29],[Infinity,.33]],bpaMax:16452,bpaMin:14829,cea:1501,
  cpp:.0595,cppBase:.0495,ympe:74600,ybe:3500,cpp2:.04,yampe:85000,ei:.0163,eiMax:68900,
  on:[[53891,.0505],[107785,.0915],[150000,.1116],[220000,.1216],[Infinity,.1316]],onBpa:12989,onSur:[[5818,.20],[7446,.36]],
  incl:.5,tfsa:7000,rrspMax:33810};
window.CA2026=T;
const $=id=>document.getElementById(id);
const num=id=>{const e=$(id);if(!e)return 0;const v=parseFloat(String(e.value).replace(/[,$%\s]/g,''));return isFinite(v)?v:0};
const val=n=>{const c=document.querySelector(`input[name="${n}"]:checked`);return c?c.value:($(n)?$(n).value:'')};
const cad=(x,d=0)=>(x<0?'−':'')+'$'+Math.abs(x).toLocaleString('en-CA',{minimumFractionDigits:d,maximumFractionDigits:d});
const pc=(x,d=1)=>(x*100).toFixed(d)+'%';
const kv=rows=>'<div class="kv">'+rows.map(r=>`<div class="${r[2]||''}">${r[0]}</div><div class="${r[2]||''}">${r[1]}</div>`).join('')+'</div>';
const big=(l,v,s)=>`<div class="big"><span>${l}</span><b>${v}</b>${s?`<em>${s}</em>`:''}</div>`;
const bar=parts=>{const tot=parts.reduce((s,p)=>s+Math.max(0,p[1]),0)||1;return '<div class="bar">'+parts.map(p=>`<i style="width:${Math.max(0,p[1])/tot*100}%;background:${p[2]}"></i>`).join('')+'</div><div class="legend">'+parts.map(p=>`<span style="--c:${p[2]}">${p[0]} ${cad(p[1])}</span>`).join('')+'</div>'};
function bands(x,b){let t=0,lo=0;for(const [hi,r] of b){if(x>lo)t+=(Math.min(x,hi)-lo)*r;lo=hi}return t}
function marg(x,b){for(const [hi,r] of b)if(x<=hi)return r;return b[b.length-1][1]}
function bpa(ni){if(ni<=181440)return T.bpaMax;if(ni>=258482)return T.bpaMin;return T.bpaMax-(T.bpaMax-T.bpaMin)*(ni-181440)/(258482-181440)}
function healthPremium(ti){if(ti<=20000)return 0;if(ti<=36000)return Math.min(300,(ti-20000)*.06);if(ti<=48000)return Math.min(450,300+Math.max(0,ti-36000)*.06);if(ti<=72000)return Math.min(600,450+Math.max(0,ti-48000)*.25);if(ti<=200000)return Math.min(750,600+Math.max(0,ti-72000)*.25);return Math.min(900,750+(ti-200000)*.25)}
// full personal tax for employment income + other income + taxable capital gains
function taxes(emp,other,rrsp){
  const cppE=Math.max(0,Math.min(emp,T.ympe)-T.ybe);const cppBase=cppE*T.cppBase,cppEnh=cppE*(T.cpp-T.cppBase);const cpp2=Math.max(0,Math.min(emp,T.yampe)-T.ympe)*T.cpp2;
  const ei=Math.min(emp,T.eiMax)*T.ei;
  const ni=Math.max(0,emp+other-rrsp-cppEnh-cpp2);
  const fedCred=(bpa(ni)+cppBase+ei+Math.min(emp,T.cea))*.14;
  const fed=Math.max(0,bands(ni,T.fed)-fedCred);
  const onCred=(T.onBpa+cppBase+ei)*.0505;let onBasic=Math.max(0,bands(ni,T.on)-onCred);
  const sur=Math.max(0,onBasic-T.onSur[0][0])*.20+Math.max(0,onBasic-T.onSur[1][0])*.36;
  const ohp=healthPremium(ni);const on=onBasic+sur+ohp;
  return {cpp:cppBase+cppEnh+cpp2,ei,ni,fed,on,sur,ohp,total:fed+on,margin:marg(ni,T.fed)+marg(ni,T.on)*(onBasic>T.onSur[1][0]?1.56:onBasic>T.onSur[0][0]?1.2:1)};
}
window.CATax={taxes};
function calcPay(){
  const sal=num('salary'),rrsp=num('rrsp'),per=+val('freq');const t=taxes(sal,0,rrsp);const net=sal-t.total-t.cpp-t.ei-rrsp;
  let html=big(`Take-home pay per ${per===12?'month':per===26?'two weeks':per===24?'semi-monthly check':'week'}`,cad(net/per,2),`${cad(net)} a year · average tax ${pc(sal?t.total/sal:0)} · marginal ${pc(t.margin)}`);
  html+=kv([['Gross salary',cad(sal)],['Federal income tax',cad(-t.fed),'neg'],['Ontario income tax (incl. surtax)',cad(-(t.on-t.ohp)),'neg'],['Ontario Health Premium',cad(-t.ohp),'neg'],['CPP + CPP2',cad(-t.cpp),'neg'],['EI premiums',cad(-t.ei),'neg'],['RRSP contribution',cad(-rrsp),'neg'],['Net pay (year)',cad(net),'t']]);
  html+=bar([['Take-home',net,'#0F8A5F'],['Federal',t.fed,'#5A0F14'],['Ontario',t.on,'#D80621'],['CPP/EI',t.cpp+t.ei,'#7A8AA8'],['RRSP',rrsp,'#6C4BD8']]);
  html+='<p class="note">2026 federal brackets 14% / 20.5% / 26% / 29% / 33% and Ontario 5.05% / 9.15% / 11.16% / 12.16% / 13.16%, with basic personal amounts, Canada employment amount, CPP (5.95% to $74,600, CPP2 4% to $85,000) and EI (1.63% to $68,900). Ontario low-income tax reduction and other credits are not included.</p>';
  $('out').innerHTML=html;
}
function calcCG(){
  const sal=num('salary'),gain=num('gain'),acct=val('acct');
  if(acct!=='taxable'){$('out').innerHTML=big('Tax on this gain','$0',acct==='tfsa'?'Gains inside a TFSA are never taxed':'Gains inside an RRSP are not taxed until you withdraw')+'<p class="note">Withdrawals from an RRSP/RRIF are taxed as regular income in the year you take them out.</p>';return}
  const a=taxes(sal,0,0),b=taxes(sal,gain*T.incl,0);const tax=b.total-a.total;
  let html=big('Tax on your capital gain (Ontario)',cad(tax,2),gain?`Effective ${pc(tax/gain)} · you keep ${cad(gain-tax)}`:'');
  html+=kv([['Capital gain',cad(gain)],['Taxable portion (50% inclusion)',cad(gain*T.incl)],['Federal tax',cad(b.fed-a.fed)],['Ontario tax (incl. surtax & health premium)',cad(b.on-a.on)],['Total',cad(tax,2),'t'],['Marginal rate on gains',pc(b.margin*T.incl)]]);
  html+='<p class="note">Only half of a capital gain is added to taxable income. The proposed increase of the inclusion rate to two-thirds was cancelled in March 2025, so 50% applies for 2026. Gains on your principal residence are generally exempt.</p>';
  $('out').innerHTML=html;
}
function calcMort(){
  const price=num('price'),dp=num('down')/100,rate=num('rate')/100,yrs=+val('amort'),freq=val('pfreq');
  const insPrem=dp>=.2?0:dp>=.15?.028:dp>=.10?.031:.04;const base=price*(1-dp);const loan=base*(1+insPrem);
  const eff=Math.pow(1+rate/2,2)-1; // Canadian semi-annual compounding
  const m=Math.pow(1+eff,1/12)-1,n=yrs*12;const pay=loan*m/(1-Math.pow(1+m,-n));
  const per=freq==='acc'?pay/2:freq==='bw'?pay*12/26:pay;const nPer=freq==='m'?12:26;
  let bal=loan,int=0,k=0;const r=Math.pow(1+eff,1/nPer)-1;const pp=freq==='m'?pay:per;while(bal>0.5&&k<nPer*yrs){const i=bal*r;bal-=pp-i;int+=i;k++}
  let html=big(freq==='m'?'Monthly payment':freq==='acc'?'Accelerated bi-weekly payment':'Bi-weekly payment',cad(freq==='m'?pay:per,2),`Mortgage ${cad(loan)} · paid off in ${(k/nPer).toFixed(1)} years`);
  html+=kv([['Down payment',cad(price*dp)],['CMHC insurance premium',insPrem?cad(base*insPrem)+` (${pc(insPrem,1)})`:'Not required (20%+ down)'],['Total mortgage',cad(loan)],['Effective annual rate',pc(eff,3)],['Total interest',cad(int)],['Paid off in',`${(k/nPer).toFixed(1)} years`,'t']]);
  html+='<p class="note">Canadian fixed-rate mortgages compound semi-annually, not monthly. Accelerated bi-weekly payments (half the monthly payment every two weeks) add one extra monthly payment a year. With less than 20% down, mortgage default insurance is required (purchase price under $1.5 million).</p>';
  $('out').innerHTML=html;
}
const PAGES={pay:calcPay,cg:calcCG,mort:calcMort};
const fn=PAGES[document.body.dataset.page];
if(fn){const f=$('form');const run=()=>{try{fn()}catch(e){console.error(e)}};f.addEventListener('input',run);f.addEventListener('change',run);run()}
})();
