/* Honglife India calculators — FY 2026-27 (Tax Year 2026-27, Income-tax Act 2025; rates per Finance Act 2026) */
(function(){
'use strict';
const T={
  newSlabs:[[400000,0],[800000,.05],[1200000,.10],[1600000,.15],[2000000,.20],[2400000,.25],[Infinity,.30]],
  newStd:75000,newRebateLimit:1200000,newRebateMax:60000,
  oldStd:50000,oldBasic:{u60:250000,s60:300000,s80:500000},oldRebateLimit:500000,oldRebateMax:12500,
  cess:.04,
  stcg:.20,ltcg:.125,ltcgExempt:125000,
  ppf:.071,fdTds:{normal:50000,senior:100000}
};
window.IN2027=T;
const $=id=>document.getElementById(id);
const num=id=>{const e=$(id);if(!e)return 0;const v=parseFloat(String(e.value).replace(/[,₹%\s]/g,''));return isFinite(v)?v:0};
const val=name=>{const c=document.querySelector(`input[name="${name}"]:checked`);return c?c.value:($(name)?$(name).value:'')};
const inr=(x,d=0)=>(x<0?'−':'')+'₹'+Math.abs(x).toLocaleString('en-IN',{minimumFractionDigits:d,maximumFractionDigits:d});
const lakh=x=>Math.abs(x)>=1e7?'₹'+(x/1e7).toFixed(2)+' Cr':Math.abs(x)>=1e5?'₹'+(x/1e5).toFixed(2)+' L':inr(x);
const pc=(x,d=1)=>(x*100).toFixed(d)+'%';
const kv=rows=>'<div class="kv">'+rows.map(r=>`<div class="${r[2]||''}">${r[0]}</div><div class="${r[2]||''}">${r[1]}</div>`).join('')+'</div>';
const big=(l,v,s)=>`<div class="big"><span>${l}</span><b>${v}</b>${s?`<em>${s}</em>`:''}</div>`;
const bar=parts=>{const tot=parts.reduce((s,p)=>s+Math.max(0,p[1]),0)||1;return '<div class="bar">'+parts.map(p=>`<i style="width:${Math.max(0,p[1])/tot*100}%;background:${p[2]}"></i>`).join('')+'</div><div class="legend">'+parts.map(p=>`<span style="--c:${p[2]}">${p[0]} ${lakh(p[1])}</span>`).join('')+'</div>'};

function slabTax(ti,slabs){let t=0,lo=0;for(const [hi,r] of slabs){if(ti>lo)t+=(Math.min(ti,hi)-lo)*r;lo=hi}return t}
function oldSlabs(age){const b=T.oldBasic[age];return [[b,0],[500000,.05],[1000000,.20],[Infinity,.30]]}
function surRate(inc,regime){if(inc>50000000&&regime==='old')return .37;if(inc>20000000)return .25;if(inc>10000000)return .15;if(inc>5000000)return .10;return 0}
const SUR_STEPS=[5000000,10000000,20000000,50000000];
// tax incl. surcharge with marginal relief, before cess
function withSurcharge(inc,taxFn,regime){
  const base=taxFn(inc);const r=surRate(inc,regime);let t=base*(1+r);
  const th=[...SUR_STEPS].reverse().find(s=>inc>s);
  if(th){const atTh=taxFn(th)*(1+surRate(th,regime));t=Math.min(t,atTh+(inc-th))}
  return {total:t,sur:t-base,base};
}
function regimeTax(ti,regime,age){
  const slabs=regime==='new'?T.newSlabs:oldSlabs(age);
  const fn=x=>{let t=slabTax(x,slabs);
    if(regime==='new'){if(x<=T.newRebateLimit)t=0;else t=Math.min(t,x-T.newRebateLimit)} // 87A + marginal relief
    else if(x<=T.oldRebateLimit)t=Math.max(0,t-T.oldRebateMax);
    return t};
  const s=withSurcharge(ti,fn,regime);const cess=s.total*T.cess;
  return {slab:slabTax(ti,slabs),afterRebate:s.base,sur:s.sur,cess,total:s.total+cess};
}
window.INTax={regimeTax,slabTax};

/* ---------- income tax: new vs old ---------- */
function calcIT(){
  const age=val('age'),sal=num('salary'),oth=num('other'),nps2=num('npsEmp');
  const hra=num('hra'),c80=Math.min(150000,num('c80')),d80=Math.min(100000,num('d80')),nps1b=Math.min(50000,num('nps1b')),hl=Math.min(200000,num('homeLoan')),misc=num('misc');
  const stdN=sal>0?Math.min(T.newStd,sal):0,stdO=sal>0?Math.min(T.oldStd,sal):0;
  const tiN=Math.max(0,sal-stdN+oth-nps2);
  const dedOld=hra+c80+d80+nps1b+hl+misc+nps2;
  const tiO=Math.max(0,sal-stdO+oth-dedOld);
  const n=regimeTax(tiN,'new',age),o=regimeTax(tiO,'old',age);
  const best=n.total<=o.total?'new':'old',save=Math.abs(n.total-o.total);
  const gross=sal+oth;
  let html=big(`Best for you: ${best==='new'?'New regime':'Old regime'}`,inr(Math.min(n.total,o.total)),save>0?`You save ${inr(save)} vs the ${best==='new'?'old':'new'} regime · take-home ${inr((gross-Math.min(n.total,o.total))/12)}/month`:'Both regimes give the same tax');
  html+='<table class="tbl"><tr><th></th><th>New regime</th><th>Old regime</th></tr>'+
   [['Gross income',gross,gross],['Standard deduction',-stdN,-stdO],['Other deductions',-nps2,-dedOld+0],['Taxable income',tiN,tiO],['Tax on slabs',n.slab,o.slab],['After 87A rebate',n.afterRebate,o.afterRebate],['Surcharge',n.sur,o.sur],['Health & education cess (4%)',n.cess,o.cess]].map(r=>`<tr><td>${r[0]}</td><td>${inr(r[1])}</td><td>${inr(r[2])}</td></tr>`).join('')+
   `<tr class="hl"><td>Total tax</td><td>${inr(n.total)}</td><td>${inr(o.total)}</td></tr><tr><td>Effective rate</td><td>${pc(gross?n.total/gross:0)}</td><td>${pc(gross?o.total/gross:0)}</td></tr><tr><td>Monthly take-home</td><td>${inr((gross-n.total)/12)}</td><td>${inr((gross-o.total)/12)}</td></tr></table>`;
  // breakeven deductions
  let lo=0,hi=gross;for(let k=0;k<40;k++){const m=(lo+hi)/2;const t=regimeTax(Math.max(0,sal-stdO+oth-m),'old',age).total;if(t>n.total)lo=m;else hi=m}
  if(hi<gross)html+=`<p class="note">💡 The old regime only beats the new one if your total old-regime deductions (HRA, 80C, 80D, home-loan interest, etc.) exceed about <b>${inr(hi)}</b>. Yours: ${inr(dedOld)}.</p>`;
  html+=`<p class="note">FY 2026-27 new regime: nil up to ₹4 L, then 5/10/15/20/25/30% every ₹4 L; ₹75,000 standard deduction; no tax up to ₹12 L taxable income (₹12.75 L salary) under section 87A with marginal relief. Caps applied: 80C ₹1.5 L, 80D ₹1 L, 80CCD(1B) ₹50,000, home-loan interest ₹2 L.</p>`;
  $('out').innerHTML=html;
}

/* ---------- capital gains on shares / equity MF ---------- */
function calcCG(){
  const regime=val('regime'),age=val('age'),slabInc=num('slabInc'),st=Math.max(0,num('stcg')),lt=Math.max(0,num('ltcg')),debt=Math.max(0,num('debt'));
  const slabTotal=slabInc+debt;
  const basic=regime==='new'?400000:T.oldBasic[age];
  let short=Math.max(0,basic-slabTotal);
  const stTaxable0=st;const ltTaxable0=Math.max(0,lt-T.ltcgExempt);
  const useSt=Math.min(short,stTaxable0);short-=useSt;const useLt=Math.min(short,ltTaxable0);
  const stT=stTaxable0-useSt,ltT=ltTaxable0-useLt;
  const capTax=stT*T.stcg+ltT*T.ltcg;
  const totalInc=slabTotal+st+lt;
  const sr=Math.min(.15,surRate(totalInc,regime));
  const capSur=capTax*sr,capCess=(capTax+capSur)*T.cess;
  const withDebt=regimeTax(slabTotal,regime,age).total,without=regimeTax(slabInc,regime,age).total;
  const debtTax=withDebt-without;
  const total=capTax+capSur+capCess+debtTax;const gains=st+lt+debt;
  let html=big('Tax on your capital gains',inr(total),gains?`Effective ${pc(total/gains)} · you keep ${inr(gains-total)}`:'');
  html+=kv([
    ['Short-term equity gain (≤ 12 months)',inr(st)],['… taxed at 20%',inr(stT)],
    ['Long-term equity gain (> 12 months)',inr(lt)],['… exempt up to ₹1.25 lakh',inr(Math.min(lt,T.ltcgExempt)),'pos'],['… taxed at 12.5%',inr(ltT)],
    ['Unused basic exemption set off against gains',inr(useSt+useLt),'pos'],
    ['Tax on equity gains',inr(capTax)],['Surcharge'+(sr?` (${pc(sr,0)}, capped at 15%)`:''),inr(capSur)],['Cess 4%',inr(capCess)],
    ['Tax on debt fund gains (slab rate)',inr(debtTax)],['Total',inr(total),'t']
  ]);
  if(st>0){const alt=Math.max(0,st+lt-T.ltcgExempt)*T.ltcg;const save=capTax-alt;if(save>0)html+=`<p class="note">💡 Holding the short-term shares past 12 months would cut the tax on equity gains by about <b>${inr(save*(1+sr)*(1+T.cess))}</b>.</p>`}
  if(lt>0&&lt<T.ltcgExempt)html+=`<p class="note">💡 Tax harvesting: you can still book about ${inr(T.ltcgExempt-lt)} more long-term gains tax-free this year (sell and buy back) to raise your cost price.</p>`;
  html+='<p class="note">Rates for transfers on or after 23 July 2024, unchanged for FY 2026-27: STCG on listed shares and equity funds 20% (STT paid), LTCG 12.5% above ₹1.25 lakh a year, no indexation. Residents can use any unused basic exemption against these gains. The 87A rebate cannot be used against tax on these special-rate gains. Debt funds bought after 1 April 2023 are taxed at slab rates.</p>';
  $('out').innerHTML=html;
}

/* ---------- SIP ---------- */
function calcSIP(){
  const mode=val('mode'),amt=num('amount'),r=num('ret')/100,yrs=num('years'),step=num('step')/100;const mr=Math.pow(1+r,1/12)-1;
  let bal=0,inv=0,m=amt,rows=[];
  if(mode==='lump'){bal=amt*Math.pow(1+r,yrs);inv=amt;for(let y=1;y<=yrs;y++)rows.push([y,amt,amt*Math.pow(1+r,y)])}
  else for(let y=1;y<=yrs;y++){for(let k=0;k<12;k++){bal=(bal+m)*(1+mr);inv+=m}rows.push([y,inv,bal]);m*=1+step}
  const gain=bal-inv;const tax=Math.max(0,gain-T.ltcgExempt)*T.ltcg*(1+T.cess);
  let html=big(`Value after ${yrs} years`,lakh(bal),`Invested ${lakh(inv)} · gains ${lakh(gain)} (${(bal/inv).toFixed(2)}×)`);
  html+=kv([['Total invested',inr(inv)],['Estimated returns',inr(gain),'pos'],['Maturity value',inr(bal),'t'],['LTCG tax if all redeemed in one year (12.5% above ₹1.25 L + cess)',inr(tax),'neg'],['Value after tax',inr(bal-tax)]]);
  html+=bar([['Invested',inv,'#1F5FD1'],['Returns',gain,'#0F8A5F']]);
  html+='<div class="scroll"><table class="tbl"><tr><th>Year</th><th>Invested</th><th>Value</th></tr>'+rows.map(r=>`<tr><td>${r[0]}</td><td>${inr(r[1])}</td><td>${inr(r[2])}</td></tr>`).join('')+'</table></div>';
  html+='<p class="note">Assumes the instalment is invested at the start of each month and a constant annual return (monthly compounding equivalent). Mutual fund returns are not guaranteed. Spreading redemptions over several financial years uses the ₹1.25 lakh exemption each year.</p>';
  $('out').innerHTML=html;
}

/* ---------- EMI ---------- */
function calcEMI(){
  const P=num('loan'),r=num('rate')/1200,yrs=num('tenure'),extra=num('extra'),lump=num('lump'),lumpY=num('lumpYear');const n=Math.round(yrs*12);
  const emi=r?P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1):P/n;
  let bal=P,m=0,int=0,yr=[],yi=0,yp=0;
  while(bal>0.5&&m<n){const i=bal*r;let p=Math.min(bal,emi-i+extra);bal-=p;int+=i;yi+=i;yp+=p;m++;if(lump>0&&m===lumpY*12){const l=Math.min(bal,lump);bal-=l;yp+=l}if(m%12===0||bal<=0.5){yr.push([Math.ceil(m/12),yi,yp,Math.max(0,bal)]);yi=yp=0}}
  const baseInt=emi*n-P;
  let html=big('Monthly EMI',inr(emi),`Total interest ${lakh(int)} · total payment ${lakh(P+int)}`);
  html+=kv([['Loan amount',inr(P)],['Total interest',inr(int)],['Total amount paid',inr(P+int),'t'],['Loan closes in',`${Math.floor(m/12)} yrs ${m%12} months`]].concat(extra||lump?[['Interest saved by prepayment',inr(baseInt-int),'pos'],['Tenure reduced by',`${Math.floor((n-m)/12)} yrs ${(n-m)%12} months`,'pos']]:[]));
  html+=bar([['Principal',P,'#1F5FD1'],['Interest',int,'#C2413A']]);
  html+='<div class="scroll"><table class="tbl"><tr><th>Year</th><th>Interest</th><th>Principal</th><th>Balance</th></tr>'+yr.map(r=>`<tr><td>${r[0]}</td><td>${inr(r[1])}</td><td>${inr(r[2])}</td><td>${inr(r[3])}</td></tr>`).join('')+'</table></div>';
  html+='<p class="note">EMI = P × r × (1+r)<sup>n</sup> ÷ ((1+r)<sup>n</sup> − 1). Banks do not charge prepayment penalties on floating-rate home loans to individuals (RBI rules). Home-loan tax benefits (section 24(b) interest up to ₹2 lakh, 80C principal) are available only under the old regime for a self-occupied house.</p>';
  $('out').innerHTML=html;
}

/* ---------- PPF ---------- */
function calcPPF(){
  const dep=Math.min(150000,Math.max(500,num('deposit'))),r=num('ret')/100,yrs=Math.max(15,num('years'));
  let bal=0,inv=0,rows=[];for(let y=1;y<=yrs;y++){bal=(bal+dep)*(1+r);inv+=dep;rows.push([y,inv,bal])}
  let html=big(`PPF maturity after ${yrs} years`,lakh(bal),`Deposited ${lakh(inv)} · tax-free interest ${lakh(bal-inv)}`);
  html+=kv([['Yearly deposit',inr(dep)],['Interest rate (Oct–Dec 2026)',pc(r,1)],['Total deposited',inr(inv)],['Total interest',inr(bal-inv),'pos'],['Maturity value (tax-free)',inr(bal),'t'],['80C deduction each year (old regime)',inr(dep)]]);
  html+=bar([['Deposits',inv,'#1F5FD1'],['Interest',bal-inv,'#0F8A5F']]);
  html+='<div class="scroll"><table class="tbl"><tr><th>Year</th><th>Deposited</th><th>Balance</th></tr>'+rows.map(r=>`<tr class="${r[0]===15?'hl':''}"><td>${r[0]}</td><td>${inr(r[1])}</td><td>${inr(r[2])}</td></tr>`).join('')+'</table></div>';
  html+='<p class="note">Assumes the full amount is deposited by 5 April each year so it earns interest for every month; interest is compounded yearly. PPF matures after 15 financial years and can be extended in 5-year blocks. Minimum ₹500, maximum ₹1.5 lakh per year. The rate is set every quarter by the Ministry of Finance.</p>';
  $('out').innerHTML=html;
}

/* ---------- FD ---------- */
function calcFD(){
  const P=num('principal'),r=num('ret')/100,yrs=num('years')+num('months')/12,q=+val('comp'),slab=num('slab')/100,senior=val('senior')==='y';
  const mat=q?P*Math.pow(1+r/q,q*yrs):P*(1+r*yrs);const int=mat-P;const perYear=int/Math.max(1,yrs);
  const th=senior?T.fdTds.senior:T.fdTds.normal;const tds=perYear>th?int*.10:0;const tax=int*slab*(1+T.cess);
  const eff=Math.pow(mat/P,1/yrs)-1;
  let html=big('Maturity amount',inr(mat),`Interest ${inr(int)} · effective yield ${pc(eff,2)} a year`);
  html+=kv([['Principal',inr(P)],['Interest earned',inr(int),'pos'],['Maturity value',inr(mat),'t'],['TDS deducted by bank (10%)',tds?inr(tds):'None — interest below '+inr(th)+'/year'],['Income tax at your slab (incl. cess)',inr(tax),'neg'],['Post-tax interest',inr(int-tax)],['Post-tax yield',pc(Math.pow((P+int-tax)/P,1/yrs)-1,2)]]);
  html+=`<p class="note">Banks compound FD interest quarterly. FD interest is taxed at your slab rate every year (accrual), and TDS of 10% applies when interest from one bank exceeds ${inr(T.fdTds.normal)} a year (${inr(T.fdTds.senior)} for senior citizens). Submit Form 15G/15H if your total income is below the taxable limit. Deposits up to ₹5 lakh per bank are insured by DICGC.</p>`;
  $('out').innerHTML=html;
}

const PAGES={it:calcIT,cg:calcCG,sip:calcSIP,emi:calcEMI,ppf:calcPPF,fd:calcFD};
const fn=PAGES[document.body.dataset.page];
if(fn){const form=$('form');const run=()=>{try{fn()}catch(e){console.error(e)}};form.addEventListener('input',run);form.addEventListener('change',run);
  new URLSearchParams(location.search).forEach((v,k)=>{const e=$(k);if(e)e.value=v;else{const r=document.querySelector(`input[name="${k}"][value="${v}"]`);if(r)r.checked=true}});run()}
})();
