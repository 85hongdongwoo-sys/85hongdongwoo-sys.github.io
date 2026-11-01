/* Honglife UK calculators — tax year 2026/27 (6 April 2026 – 5 April 2027), England, Wales & NI rates */
(function(){
'use strict';
const T={pa:12570,taperStart:100000,basicBand:37700,addStart:125140,rates:[.20,.40,.45],
  pt:12570,uel:50270,ni:[.08,.02],
  divAllow:500,div:[.1075,.3575,.3935],psa:[1000,500,0],
  aea:3000,cgt:[.18,.24],
  sl:{none:[0,0],p1:[26900,.09],p2:[29385,.09],p4:[33795,.09],p5:[25000,.09]},pg:[21000,.06],
  sdlt:[[125000,0],[250000,.02],[925000,.05],[1500000,.10],[Infinity,.12]],sdltFtb:[[300000,0],[500000,.05]],sdltFtbMax:500000,sdltExtra:.05};
window.UK2627=T;
const $=id=>document.getElementById(id);
const num=id=>{const e=$(id);if(!e)return 0;const v=parseFloat(String(e.value).replace(/[,£%\s]/g,''));return isFinite(v)?v:0};
const val=n=>{const c=document.querySelector(`input[name="${n}"]:checked`);return c?c.value:($(n)?$(n).value:'')};
const gbp=(x,d=0)=>(x<0?'−':'')+'£'+Math.abs(x).toLocaleString('en-GB',{minimumFractionDigits:d,maximumFractionDigits:d});
const pc=(x,d=1)=>(x*100).toFixed(d)+'%';
const kv=rows=>'<div class="kv">'+rows.map(r=>`<div class="${r[2]||''}">${r[0]}</div><div class="${r[2]||''}">${r[1]}</div>`).join('')+'</div>';
const big=(l,v,s)=>`<div class="big"><span>${l}</span><b>${v}</b>${s?`<em>${s}</em>`:''}</div>`;
const bar=parts=>{const tot=parts.reduce((s,p)=>s+Math.max(0,p[1]),0)||1;return '<div class="bar">'+parts.map(p=>`<i style="width:${Math.max(0,p[1])/tot*100}%;background:${p[2]}"></i>`).join('')+'</div><div class="legend">'+parts.map(p=>`<span style="--c:${p[2]}">${p[0]} ${gbp(p[1])}</span>`).join('')+'</div>'};
function allowance(ani){return Math.max(0,T.pa-Math.max(0,ani-T.taperStart)/2)}
// tax on non-savings income given allowance; returns tax and band usage
function incomeTax(nonSav,pa){const ti=Math.max(0,nonSav-pa);const b=Math.min(ti,T.basicBand);
  // higher band ends where total income reaches £125,140
  const higherCap=Math.max(0,T.addStart-pa-T.basicBand);const hh=Math.min(Math.max(0,ti-T.basicBand),higherCap);const a=Math.max(0,ti-T.basicBand-higherCap);
  return {tax:b*T.rates[0]+hh*T.rates[1]+a*T.rates[2],ti,basicUsed:b,higherCap}}
window.UKTax={allowance,incomeTax};

/* ---------- take-home pay ---------- */
function calcPay(){
  const sal=num('salary'),pen=num('pension')/100,sac=val('pentype')==='sac',plan=val('plan'),pg=val('pg')==='y',bonus=num('bonus');
  const gross=sal+bonus;const penAmt=gross*pen;
  const taxable=gross-penAmt; // salary sacrifice or net pay arrangement both reduce taxable pay
  const niPay=sac?gross-penAmt:gross;
  const pa=allowance(taxable);const it=incomeTax(taxable,pa).tax;
  const ni=Math.max(0,Math.min(niPay,T.uel)-T.pt)*T.ni[0]+Math.max(0,niPay-T.uel)*T.ni[1];
  const [th,r]=T.sl[plan];const slr=plan==='none'?0:Math.max(0,niPay-th)*r;const pgr=pg?Math.max(0,niPay-T.pg[0])*T.pg[1]:0;
  const net=gross-penAmt-it-ni-slr-pgr;
  let html=big('Take-home pay per month',gbp(net/12,2),`${gbp(net)} a year · ${gbp(net/52,2)} a week`);
  html+=kv([['Gross pay',gbp(gross)],['Personal allowance',gbp(pa)+(pa<T.pa?' (tapered)':'')],['Income tax',gbp(-it),'neg'],['National Insurance',gbp(-ni),'neg'],['Pension contribution',gbp(-penAmt),'neg'],['Student loan',gbp(-slr),'neg'],['Postgraduate loan',gbp(-pgr),'neg'],['Take-home (year)',gbp(net),'t'],['Effective deduction rate',pc(gross?1-net/gross:0)]]);
  html+=bar([['Take-home',net,'#0F8A5F'],['Income tax',it,'#012169'],['NI',ni,'#C8102E'],['Pension',penAmt,'#6C4BD8'],['Loans',slr+pgr,'#A0AEC8']]);
  if(taxable>T.taperStart&&taxable<T.addStart)html+=`<p class="note">⚠️ Between £100,000 and £125,140 you lose £1 of personal allowance for every £2 earned — an effective 60% tax rate. Paying ${gbp(taxable-T.taperStart)} more into your pension would restore the full allowance.</p>`;
  html+='<p class="note">2026/27 rates for England, Wales and Northern Ireland: personal allowance £12,570; 20% up to £50,270; 40% up to £125,140; 45% above. Employee National Insurance 8% between £12,570 and £50,270 and 2% above. Scottish income tax bands are different and not included.</p>';
  $('out').innerHTML=html;
}
/* ---------- dividend tax ---------- */
function calcDiv(){
  const other=num('other'),div=num('div'),sav=num('savings');
  const pa=allowance(other+div+sav);let paLeft=pa;
  const nsTax=Math.max(0,other-paLeft);paLeft=Math.max(0,paLeft-other);
  const base=incomeTax(other,pa);let bandLeft=Math.max(0,T.basicBand-base.ti);let higherLeft=Math.max(0,base.higherCap-Math.max(0,base.ti-T.basicBand));
  // savings
  const higherRate=other+sav+div>T.pa+T.basicBand;const psa=other+sav+div>T.addStart?0:higherRate?T.psa[1]:T.psa[0];
  let s=Math.max(0,sav-paLeft);paLeft=Math.max(0,paLeft-sav);let sTax=0;let sFree=Math.min(s,psa);
  const take=(amt,rates)=>{let t=0;const b=Math.min(amt,bandLeft);t+=b*rates[0];bandLeft-=b;amt-=b;const h=Math.min(amt,higherLeft);t+=h*rates[1];higherLeft-=h;amt-=h;t+=amt*rates[2];return t};
  // PSA uses band but taxed at 0
  const tmp=take(sFree,[0,0,0]);sTax=take(s-sFree,T.rates);
  let d=Math.max(0,div-paLeft);const dFree=Math.min(d,T.divAllow);take(dFree,[0,0,0]);const dTax=take(d-dFree,T.div);
  let html=big('Tax on your dividends',gbp(dTax,2),div?`Effective ${pc(dTax/div)} · you keep ${gbp(div-dTax)}`:'');
  html+=kv([['Dividends received',gbp(div)],['Covered by personal allowance',gbp(Math.min(div,Math.max(0,div-d))),'pos'],['Dividend allowance (0%)',gbp(dFree),'pos'],['Taxable dividends',gbp(d-dFree)],['Dividend tax',gbp(dTax,2),'t'],['Tax on savings interest (after £'+psa+' allowance)',gbp(sTax,2)]]);
  html+='<p class="note">2026/27 dividend rates rose by 2 percentage points for basic and higher rate taxpayers: 10.75% (basic), 35.75% (higher), 39.35% (additional, unchanged). The first £500 of dividends is tax-free. Dividends in an ISA or pension are tax-free.</p>';
  $('out').innerHTML=html;
}
/* ---------- CGT ---------- */
function calcCGT(){
  const inc=num('income'),gain=num('gain'),loss=num('loss');const net=Math.max(0,gain-loss);const taxable=Math.max(0,net-T.aea);
  const pa=allowance(inc);const ti=Math.max(0,inc-pa);const basicLeft=Math.max(0,T.basicBand-ti);
  const low=Math.min(taxable,basicLeft),high=taxable-low;const tax=low*T.cgt[0]+high*T.cgt[1];
  let html=big('Capital Gains Tax',gbp(tax,2),net?`Effective ${pc(tax/net)} of your gain`:'');
  html+=kv([['Net gain after losses',gbp(net)],['Annual exempt amount',gbp(Math.min(net,T.aea)),'pos'],['Taxable gain',gbp(taxable)],['Taxed at 18% (within basic rate band)',gbp(low)],['Taxed at 24%',gbp(high)],['CGT due',gbp(tax,2),'t']]);
  html+='<p class="note">From 6 April 2025 the same rates apply to shares and residential property: 18% within your unused basic rate band and 24% above. The annual exempt amount is £3,000 for 2026/27. Residential property gains must be reported and paid within 60 days of completion.</p>';
  $('out').innerHTML=html;
}
/* ---------- Stamp Duty (England & NI) ---------- */
function bands(p,b){let t=0,lo=0;for(const [hi,r] of b){if(p>lo)t+=(Math.min(p,hi)-lo)*r;lo=hi}return t}
function calcSDLT(){
  const p=num('price'),type=val('buyer');let tax,ftb=false;
  if(type==='ftb'&&p<=T.sdltFtbMax){tax=bands(p,T.sdltFtb);ftb=true}else tax=bands(p,T.sdlt);
  const extra=type==='add'?p*T.sdltExtra:0;const total=tax+extra;
  let html=big('Stamp Duty to pay',gbp(total),p?`Effective rate ${pc(total/p,2)}`:'');
  html+=kv([['Purchase price',gbp(p)],[ftb?'First-time buyer rates':'Standard rates',gbp(tax)],['Higher rates for additional dwellings (+5%)',gbp(extra)],['Total SDLT',gbp(total),'t']].concat(type==='ftb'&&!ftb?[['First-time buyer relief','Not available above £500,000','neg']]:[]));
  html+='<table class="tbl"><tr><th>Price band</th><th>Standard</th><th>First-time buyer</th></tr><tr><td>Up to £125,000</td><td>0%</td><td>0% (up to £300,000)</td></tr><tr><td>£125,001–£250,000</td><td>2%</td><td>—</td></tr><tr><td>£250,001–£925,000</td><td>5%</td><td>5% (£300,001–£500,000)</td></tr><tr><td>£925,001–£1.5m</td><td>10%</td><td>—</td></tr><tr><td>Over £1.5m</td><td>12%</td><td>—</td></tr></table>';
  html+='<p class="note">Rates from 1 April 2025 for residential property in England and Northern Ireland. Scotland (LBTT) and Wales (LTT) have their own taxes. Non-UK residents pay a further 2%.</p>';
  $('out').innerHTML=html;
}
const PAGES={pay:calcPay,div:calcDiv,cgt:calcCGT,sdlt:calcSDLT};
const fn=PAGES[document.body.dataset.page];
if(fn){const f=$('form');const run=()=>{try{fn()}catch(e){console.error(e)}};f.addEventListener('input',run);f.addEventListener('change',run);run()}
})();
