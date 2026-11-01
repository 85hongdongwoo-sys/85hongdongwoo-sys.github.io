/* Honglife US calculators — 2026 tax year (IRS Rev. Proc. 2025-32, SSA 2026 fact sheet) */
(function(){
'use strict';
const T={
  year:2026,
  std:{single:16100,mfj:32200,mfs:16100,hoh:24150},
  // upper bounds of 10,12,22,24,32,35% brackets; 37% above
  br:{single:[12400,50400,105700,201775,256225,640600],mfj:[24800,100800,211400,403550,512450,768700],mfs:[12400,50400,105700,201775,256225,384350],hoh:[17700,67450,105700,201750,256200,640600]},
  rates:[.10,.12,.22,.24,.32,.35,.37],
  ltcg:{single:[49450,545500],mfj:[98900,613700],mfs:[49450,306850],hoh:[66200,579600]},
  niit:{single:200000,mfj:250000,mfs:125000,hoh:200000},       // 3.8%, not indexed
  addMed:{single:200000,mfj:250000,mfs:125000,hoh:200000},     // 0.9%, not indexed
  ssWage:184500, ssRate:.062, medRate:.0145,
  ctc:2200, ctcPhase:{single:200000,mfj:400000,mfs:200000,hoh:200000},
  capLoss:{single:3000,mfj:3000,mfs:1500,hoh:3000},
  k401:24500,k401catch:8000,k401super:11250,ira:7500,iraCatch:1100
};
window.US2026=T;
const $=id=>document.getElementById(id);
const num=id=>{const e=$(id);if(!e)return 0;const v=parseFloat(String(e.value).replace(/[,$%\s]/g,''));return isFinite(v)?v:0};
const val=name=>{const c=document.querySelector(`input[name="${name}"]:checked`);return c?c.value:($(name)?$(name).value:'')};
const usd=(x,d=0)=>(x<0?'−':'')+'$'+Math.abs(x).toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
const pc=(x,d=1)=>(x*100).toFixed(d)+'%';
const kv=rows=>'<div class="kv">'+rows.map(r=>`<div class="${r[2]||''}">${r[0]}</div><div class="${r[2]||''}">${r[1]}</div>`).join('')+'</div>';
const big=(label,value,sub)=>`<div class="big"><span>${label}</span><b>${value}</b>${sub?`<em>${sub}</em>`:''}</div>`;
const bar=parts=>{const tot=parts.reduce((s,p)=>s+Math.max(0,p[1]),0)||1;return '<div class="bar">'+parts.map(p=>`<i style="width:${Math.max(0,p[1])/tot*100}%;background:${p[2]}"></i>`).join('')+'</div><div class="legend">'+parts.map(p=>`<span style="--c:${p[2]}">${p[0]} ${usd(p[1])}</span>`).join('')+'</div>'};

/* ---------- federal engine ---------- */
function ordTax(ti,st){ti=Math.max(0,ti);const b=T.br[st];let tax=0,lo=0;for(let i=0;i<7;i++){const hi=i<6?b[i]:Infinity;if(ti>lo)tax+=(Math.min(ti,hi)-lo)*T.rates[i];lo=hi}return tax}
function marginal(ti,st){const b=T.br[st];for(let i=0;i<6;i++)if(ti<=b[i])return T.rates[i];return .37}
// Qualified dividends & capital gain tax worksheet
function fedTax(ti,pref,st){
  ti=Math.max(0,ti);pref=Math.max(0,Math.min(pref,ti));const o=ti-pref;const [z,f]=T.ltcg[st];
  const zero=Math.max(0,Math.min(pref,z-o));
  const fif=Math.max(0,Math.min(pref-zero,f-(o+zero)));
  const twenty=pref-zero-fif;
  const tax=ordTax(o,st)+fif*.15+twenty*.20;
  return {tax:Math.min(tax,ordTax(ti,st)),ord:ordTax(o,st),zero,fif,twenty,o};
}
window.USTax={ordTax,fedTax,marginal};

/* ---------- capital gains & dividends ---------- */
function calcInvest(mode){
  const st=val('status');const wages=num('wages');const ded=val('dedType')==='item'?num('itemized'):T.std[st];
  let stcg=num('stcg'),ltcg=num('ltcg');const qd=num('qdiv'),od=num('odiv'),stRate=num('stateRate')/100;
  // netting short and long term
  let netST=stcg,netLT=ltcg;
  if(netST<0&&netLT>0){const u=Math.min(-netST,netLT);netLT-=u;netST+=u}
  else if(netLT<0&&netST>0){const u=Math.min(-netLT,netST);netST-=u;netLT+=u}
  const net=netST+netLT;let lossDed=0,carry=0;
  if(net<0){lossDed=Math.min(-net,T.capLoss[st]);carry=-net-lossDed}
  const gainOrd=Math.max(0,netST),gainLT=Math.max(0,netLT);
  const agiBase=wages;const agi=wages+gainOrd+gainLT+qd+od-lossDed;
  const ti=Math.max(0,agi-ded);const pref=gainLT+qd;
  const withInv=fedTax(ti,pref,st).tax;
  const tiBase=Math.max(0,agiBase-ded);const without=ordTax(tiBase,st);
  const nii=Math.max(0,gainOrd+gainLT+qd+od);const niit=Math.max(0,Math.min(nii,agi-T.niit[st]))*.038;
  const fedInv=withInv-without;const state=Math.max(0,(gainOrd+gainLT+qd+od-lossDed))*stRate;
  const invIncome=gainOrd+gainLT+qd+od;const totInv=fedInv+niit+state;
  const w=fedTax(ti,pref,st);
  const ltRate=gainLT+qd>0?(w.twenty>0?'20%':w.fif>0?'15%':'0%'):'—';
  let html=big(mode==='div'?'Total tax on your dividends':'Total tax on your gains & dividends',usd(totInv),invIncome>0?`Effective rate ${pc(totInv/invIncome)} · you keep ${usd(invIncome-totInv)}`:(net<0?`Net capital loss — ${usd(lossDed)} deducted this year`:''));
  html+=kv([
    ['Federal income tax on investment income',usd(fedInv)],
    ['Net investment income tax (3.8%)',usd(niit)],
    ['State tax (your rate)',usd(state)],
    ['Total investment tax',usd(totInv),'t'],
    ['Qualified (0/15/20%) income taxed at 0%',usd(w.zero)],
    ['… taxed at 15%',usd(w.fif)],
    ['… taxed at 20%',usd(w.twenty)],
    ['Top long-term rate reached',ltRate],
    ['Ordinary marginal bracket',pc(marginal(w.o,st),0)],
    ['Taxable income (after deduction)',usd(ti)],
  ].concat(net<0?[['Capital loss deducted this year',usd(lossDed),'pos'],['Loss carried forward to 2027',usd(carry)]]:[]))
  html+=bar([['Federal',fedInv,'#1F5FD1'],['NIIT',niit,'#B8862B'],['State',state,'#7A8AA8'],['You keep',Math.max(0,invIncome-totInv),'#0F8A5F']]);
  // short vs long comparison hint
  if(mode!=='div'&&netST>0){const alt=fedTax(ti,pref+netST,st).tax;const save=withInv-alt;if(save>1)html+=`<p class="note">💡 If your short-term gains of ${usd(netST)} were held over one year, federal tax would be about <b>${usd(save)}</b> lower.</p>`}
  if(mode==='div'&&od>0){const alt=fedTax(ti,pref+od,st).tax;const save=withInv-alt;if(save>1)html+=`<p class="note">💡 If your ${usd(od)} of ordinary dividends were qualified, you would save about <b>${usd(save)}</b>.</p>`}
  html+=`<p class="note">2026 federal rules: standard deduction ${usd(T.std[st])}, long-term 0% up to ${usd(T.ltcg[st][0])} and 15% up to ${usd(T.ltcg[st][1])} of taxable income. NIIT applies above ${usd(T.niit[st])} of modified AGI.</p>`;
  $('out').innerHTML=html;
}

/* ---------- paycheck ---------- */
function calcPay(){
  const st=val('status');const gross=num('salary');const per=+val('freq');const k=num('k401pct')/100;const pre=num('pretax');const kids=num('kids');const stRate=num('stateRate')/100;const extra=num('otherInc');
  const kAmt=Math.min(gross*k,T.k401+(num('age')>=60&&num('age')<=63?T.k401super:num('age')>=50?T.k401catch:0));
  const ficaWages=Math.max(0,gross-pre);
  const ss=Math.min(ficaWages,T.ssWage)*T.ssRate;
  const med=ficaWages*T.medRate+Math.max(0,ficaWages-T.addMed[st])*.009;
  const agi=gross-kAmt-pre+extra;const ti=Math.max(0,agi-T.std[st]);
  let fed=ordTax(ti,st);
  let ctc=Math.max(0,kids*T.ctc-Math.ceil(Math.max(0,agi-T.ctcPhase[st])/1000)*50);const ctcUsed=Math.min(ctc,fed);fed-=ctcUsed;
  const state=Math.max(0,agi-extra)*stRate;
  const net=gross-kAmt-pre-fed-ss-med-state;
  const tot=fed+ss+med+state;
  let html=big(`Take-home pay per ${per===12?'month':per===24?'semi-monthly check':per===26?'two weeks':'week'}`,usd(net/per,2),`${usd(net)} per year · total tax ${pc(gross?tot/gross:0)} of gross`);
  html+=kv([
    ['Gross pay',usd(gross/per,2)],
    ['Federal income tax',usd(-fed/per,2),'neg'],
    ['Social Security (6.2%)',usd(-ss/per,2),'neg'],
    ['Medicare (1.45% + 0.9%)',usd(-med/per,2),'neg'],
    ['State income tax',usd(-state/per,2),'neg'],
    ['401(k) contribution',usd(-kAmt/per,2),'neg'],
    ['Pre-tax health / HSA / FSA',usd(-pre/per,2),'neg'],
    ['Net pay',usd(net/per,2),'t'],
  ]);
  html+=bar([['Take-home',net,'#0F8A5F'],['Federal',fed,'#1F5FD1'],['FICA',ss+med,'#B8862B'],['State',state,'#7A8AA8'],['401(k)',kAmt,'#6C4BD8'],['Pre-tax benefits',pre,'#A0AEC8']]);
  html+=`<p class="note">Federal marginal bracket ${pc(marginal(ti,st),0)} · taxable income ${usd(ti)}${ctcUsed?` · child tax credit applied ${usd(ctcUsed)}`:''}. Uses the 2026 standard deduction (${usd(T.std[st])}) and assumes your W-4 matches your filing status. Social Security stops at the ${usd(T.ssWage)} wage base.</p>`;
  $('out').innerHTML=html;
}

/* ---------- 401(k) ---------- */
function calcK(){
  const age=num('age'),ret=num('retAge'),sal0=num('salary'),pct=num('k401pct')/100,mPct=num('match')/100,mCap=num('matchCap')/100,bal0=num('balance'),r=num('ret')/100,g=num('raise')/100,tNow=num('taxNow')/100,tRet=num('taxRet')/100;
  let bal=bal0,sal=sal0,you=0,emp=0,rows=[];
  for(let a=age;a<ret;a++){
    const lim=T.k401+(a>=60&&a<=63?T.k401super:a>=50?T.k401catch:0);
    const c=Math.min(sal*pct,lim);const m=Math.min(sal*Math.min(pct,mCap),sal*mCap)*mPct;
    bal=bal*(1+r)+(c+m)*(1+r/2);you+=c;emp+=m;
    if((a-age)%5===4||a===ret-1)rows.push([a+1,bal,you,emp]);sal*=1+g}
  const growth=bal-bal0-you-emp;
  const trad=bal*(1-tRet),roth=bal*(1-tNow); // same pre-tax budget: Roth pays tax now
  let html=big(`Your 401(k) at age ${ret}`,usd(bal),`${usd(you)} from you · ${usd(emp)} employer match · ${usd(growth)} investment growth`);
  html+=kv([
    ['First-year contribution (you)',usd(Math.min(sal0*pct,T.k401+(age>=60&&age<=63?T.k401super:age>=50?T.k401catch:0)))],
    ['First-year employer match',usd(sal0*Math.min(pct,mCap)*mPct)],
    ['2026 employee limit',usd(T.k401)+(age>=50?` + ${usd(age>=60&&age<=63?T.k401super:T.k401catch)} catch-up`:'')],
    ['Traditional: value after paying '+pc(tRet,0)+' tax at withdrawal',usd(trad)],
    ['Roth: same budget after paying '+pc(tNow,0)+' tax today',usd(roth)],
    ['Better choice for you',tNow<tRet?'Roth':tNow>tRet?'Traditional':'Same','t'],
  ]);
  html+=bar([['Your contributions',you,'#1F5FD1'],['Employer match',emp,'#B8862B'],['Growth',Math.max(0,growth),'#0F8A5F'],['Starting balance',bal0,'#A0AEC8']]);
  if(mPct>0&&pct<mCap)html+=`<p class="note">⚠️ You contribute ${pc(pct,0)} but your employer matches up to ${pc(mCap,0)}. Raising your contribution to ${pc(mCap,0)} adds ${usd(sal0*(mCap-pct)*mPct)} of free match this year.</p>`;
  html+='<div class="scroll"><table class="tbl"><tr><th>Age</th><th>Balance</th><th>You paid in</th><th>Match</th></tr>'+rows.map(r=>`<tr><td>${r[0]}</td><td>${usd(r[1])}</td><td>${usd(r[2])}</td><td>${usd(r[3])}</td></tr>`).join('')+'</table></div>';
  html+=`<p class="note">Limits held at 2026 levels (${usd(T.k401)}; catch-up ${usd(T.k401catch)} at 50+, ${usd(T.k401super)} at 60–63). Not adjusted for inflation; returns are compounded yearly with mid-year contributions.</p>`;
  $('out').innerHTML=html;
}

/* ---------- mortgage ---------- */
function calcMort(){
  const price=num('price'),dpP=num('down')/100,rate=num('rate')/100/12,yrs=+val('term'),taxY=num('ptax')/100,ins=num('ins'),hoa=num('hoa'),pmiR=num('pmi')/100,extra=num('extra');
  const loan=price*(1-dpP),n=yrs*12;const pi=rate?loan*rate/(1-Math.pow(1+rate,-n)):loan/n;
  let bal=loan,m=0,int=0,pmiTot=0,yr=[],yInt=0,yPri=0,pmiMonths=0;
  while(bal>0.005&&m<n){const i=bal*rate;let p=Math.min(bal,pi-i+extra);bal-=p;int+=i;m++;yInt+=i;yPri+=p;
    if(bal+p>price*.78&&dpP<.2){pmiTot+=loan*pmiR/12;pmiMonths++}
    if(m%12===0||bal<=0.005){yr.push([Math.ceil(m/12),yInt,yPri,Math.max(0,bal)]);yInt=yPri=0}}
  const base=(()=>{let b=loan,t=0;for(let k=0;k<n;k++){const i=b*rate;b-=pi-i;t+=i}return t})();
  const pmi0=dpP<.2?loan*pmiR/12:0;const tx=price*taxY/12;const pay=pi+tx+ins/12+hoa+pmi0;
  let html=big('Monthly payment',usd(pay,2),`Principal & interest ${usd(pi,2)} · loan ${usd(loan)}`);
  html+=kv([
    ['Principal & interest',usd(pi,2)],['Property tax',usd(tx,2)],['Home insurance',usd(ins/12,2)],['HOA',usd(hoa,2)],
    ['PMI'+(pmi0?` (until ~${Math.ceil(pmiMonths/12)} yrs)`:''),usd(pmi0,2)],['Total monthly',usd(pay,2),'t'],
    ['Down payment',usd(price*dpP)],['Total interest',usd(int)],['Paid off in',`${Math.floor(m/12)} yrs ${m%12} mo`],
  ].concat(extra>0?[['Interest saved by extra payments',usd(base-int),'pos'],['Time saved',`${Math.floor((n-m)/12)} yrs ${(n-m)%12} mo`,'pos']]:[]));
  html+=bar([['Principal',loan,'#1F5FD1'],['Interest',int,'#C2413A'],['PMI',pmiTot,'#B8862B']]);
  html+='<div class="scroll"><table class="tbl"><tr><th>Year</th><th>Interest</th><th>Principal</th><th>Balance</th></tr>'+yr.map(r=>`<tr><td>${r[0]}</td><td>${usd(r[1])}</td><td>${usd(r[2])}</td><td>${usd(r[3])}</td></tr>`).join('')+'</table></div>';
  html+='<p class="note">PMI is estimated until the balance reaches 78% of the purchase price, when lenders must cancel it automatically. Property tax and insurance are held flat.</p>';
  $('out').innerHTML=html;
}

/* ---------- FIRE ---------- */
function calcFire(){
  const sp=num('spend'),port=num('portfolio'),save=num('save'),r=num('ret')/100,swr=num('swr')/100,age=num('age');
  const fi=sp/swr;let b=port,y=0;while(b<fi&&y<100){b=b*(1+r)+save;y++}
  const coastAt=n=>fi/Math.pow(1+r,n);const yrsTo65=Math.max(0,65-age);
  let html=big('Your FIRE number',usd(fi),y<100?`Reached in about ${y} years — age ${age+y}`:'Not reached in 100 years at this savings rate');
  html+=kv([
    ['Annual spending in retirement',usd(sp)],['Safe withdrawal rate',pc(swr,1)],['Monthly income from portfolio',usd(fi*swr/12)],
    ['Current progress',pc(Math.min(1,port/fi),1)],['Coast FI today (stop saving, retire at 65)',usd(coastAt(yrsTo65))],
    ['Status',port>=coastAt(yrsTo65)?'✅ Already Coast FI':'Keep saving','t'],
    ['Lean FI (spending × 0.7)',usd(fi*.7)],['Fat FI (spending × 1.5)',usd(fi*1.5)]
  ]);
  const rows=[];b=port;for(let k=0;k<=Math.min(y,60);k+=Math.max(1,Math.ceil(Math.min(y,60)/12))){let bb=port;for(let j=0;j<k;j++)bb=bb*(1+r)+save;rows.push([age+k,bb])}
  html+='<table class="tbl"><tr><th>Age</th><th>Portfolio</th><th>% of goal</th></tr>'+rows.map(r=>`<tr><td>${r[0]}</td><td>${usd(r[1])}</td><td>${pc(Math.min(1,r[1]/fi),0)}</td></tr>`).join('')+'</table>';
  html+='<p class="note">Use a real (after-inflation) return, e.g. 5–7% for a stock-heavy portfolio, so all figures are in today\'s dollars. The 4% rule comes from historical U.S. 30-year retirement studies; longer retirements often use 3.25–3.5%.</p>';
  $('out').innerHTML=html;
}

/* ---------- Social Security ---------- */
function fraMonths(by){if(by<=1937)return 65*12;if(by<=1942)return 65*12+(by-1937)*2;if(by<=1954)return 66*12;if(by<=1959)return 66*12+(by-1954)*2;return 67*12}
function ssFactor(claimM,fra){const d=claimM-fra;if(d>=0)return 1+Math.min(d,70*12-fra)*(2/3)/100;const e=-d;return 1-(Math.min(e,36)*5/9+Math.max(0,e-36)*5/12)/100}
function calcSS(){
  const by=num('birth'),pia=num('pia'),cy=num('claimY'),cm=num('claimM'),life=num('life');const fra=fraMonths(by);const claim=cy*12+cm;
  const f=ssFactor(claim,fra);const ben=pia*f;
  const cum=c=>{const b=pia*ssFactor(c,fra);return Math.max(0,life*12-c)*b};
  const ages=[62,63,64,65,66,67,68,69,70];
  let best=ages.map(a=>[a,cum(a*12)]).sort((x,y)=>y[1]-x[1])[0];
  // breakeven vs FRA
  const bF=pia,bC=ben;let be='—';if(claim<fra&&bF>bC){be=((fra*bF-claim*bC)/(bF-bC)/12).toFixed(1)}else if(claim>fra){be=((claim*bC-fra*bF)/(bC-bF)/12).toFixed(1)}
  let html=big(`Monthly benefit at ${cy}${cm?` and ${cm} mo`:''}`,usd(ben),`${f>=1?'+':'−'}${pc(Math.abs(f-1),1)} vs. full retirement age (${Math.floor(fra/12)}${fra%12?` and ${fra%12} mo`:''})`);
  html+=kv([['Benefit at full retirement age (PIA)',usd(pia)],['Your claiming adjustment',(f>=1?'+':'−')+pc(Math.abs(f-1),2)],['Yearly benefit',usd(ben*12)],
    ['Lifetime total to age '+life,usd(cum(claim)),'t'],['Break-even age vs. claiming at FRA',be],['Highest lifetime total if you live to '+life,`Claim at ${best[0]}`,'pos']]);
  html+='<table class="tbl"><tr><th>Claim at</th><th>Monthly</th><th>vs. FRA</th><th>Total to '+life+'</th></tr>'+ages.map(a=>{const ff=ssFactor(a*12,fra);return `<tr class="${a===cy&&!cm?'hl':''}"><td>${a}</td><td>${usd(pia*ff)}</td><td>${(ff>=1?'+':'')+pc(ff-1,1)}</td><td>${usd(cum(a*12))}</td></tr>`}).join('')+'</table>';
  html+=`<p class="note">Before FRA, benefits drop 5/9 of 1% per month for the first 36 months and 5/12 of 1% for each month beyond. After FRA, delayed credits add 2/3 of 1% per month (8% a year) until 70. Amounts are in today's dollars; 2026 COLA was 2.8% and the maximum benefit at FRA is $4,152. If you work before FRA, the 2026 earnings test withholds $1 per $2 above $24,480.</p>`;
  $('out').innerHTML=html;
}

const PAGES={cg:()=>calcInvest('cg'),div:()=>calcInvest('div'),pay:calcPay,k401:calcK,mort:calcMort,fire:calcFire,ss:calcSS};
const page=document.body.dataset.page;const fn=PAGES[page];
if(fn){const form=$('form');const run=()=>{try{fn()}catch(e){console.error(e)}};form.addEventListener('input',run);form.addEventListener('change',()=>{const it=$('itemizedWrap');if(it)it.hidden=val('dedType')!=='item';run()});
  // restore from URL
  const q=new URLSearchParams(location.search);q.forEach((v,k)=>{const e=$(k);if(e)e.value=v;else{const r=document.querySelector(`input[name="${k}"][value="${v}"]`);if(r)r.checked=true}});
  const it=$('itemizedWrap');if(it)it.hidden=val('dedType')!=='item';run();}
})();
