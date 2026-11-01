/* Honglife world calculators (batch 2): JP, FR, ES, MX, BR — 2026 rules. Strings come from window.C */
(function(){
'use strict';
const C=window.C,$=id=>document.getElementById(id),S=C.s;
const num=id=>{const e=$(id);if(!e)return 0;const raw=String(e.value).trim();if(e.type==='number')return parseFloat(raw.replace(',','.'))||0;
  let t=raw.replace(/[^\d.,-]/g,'');const seps=t.match(/[.,]/g)||[];const last=Math.max(t.lastIndexOf('.'),t.lastIndexOf(','));
  if(last>=0){const after=t.length-last-1;if(after===3&&!(t.includes('.')&&t.includes(',')))t=t.replace(/[.,]/g,'');else{const d=t[last];t=t.slice(0,last).replace(/[.,]/g,'')+'.'+t.slice(last+1)}}
  const v=parseFloat(t);return isFinite(v)?v:0};
const val=n=>{const c=document.querySelector(`input[name="${n}"]:checked`);return c?c.value:($(n)?$(n).value:'')};
const m=(x,d)=>new Intl.NumberFormat(C.locale,{style:'currency',currency:C.cur,maximumFractionDigits:d??C.dig,minimumFractionDigits:d??C.dig}).format(x);
const pc=(x,d=1)=>new Intl.NumberFormat(C.locale,{style:'percent',maximumFractionDigits:d,minimumFractionDigits:d}).format(x);
const kv=rows=>'<div class="kv">'+rows.map(r=>`<div class="${r[2]||''}">${r[0]}</div><div class="${r[2]||''}">${r[1]}</div>`).join('')+'</div>';
const big=(l,v,s)=>`<div class="big"><span>${l}</span><b>${v}</b>${s?`<em>${s}</em>`:''}</div>`;
const bar=parts=>{const tot=parts.reduce((s,p)=>s+Math.max(0,p[1]),0)||1;return '<div class="bar">'+parts.map(p=>`<i style="width:${Math.max(0,p[1])/tot*100}%;background:${p[2]}"></i>`).join('')+'</div><div class="legend">'+parts.map(p=>`<span style="--c:${p[2]}">${p[0]} ${m(p[1])}</span>`).join('')+'</div>'};
const note=t=>`<p class="note">${t}</p>`;
const out=h=>$('out').innerHTML=h;
const prog=(x,b)=>{let t=0,lo=0;for(const [hi,r] of b){if(x>lo)t+=(Math.min(x,hi)-lo)*r;lo=hi}return t};

/* ===== shared: amortized loan (French/Price) and SAC ===== */
function loan(){
  const P=num('loan'),r=num('rate')/100/12,n=Math.round(num('years')*12),ins=num('ins')/100/12,type=val('sys')||'price';
  let bal=P,int=0,first=0,last=0,rows=[],yi=0,yp=0;const pmt=r?P*r/(1-Math.pow(1+r,-n)):P/n;const amortC=P/n;
  for(let k=1;k<=n;k++){const i=bal*r;const pr=type==='sac'?amortC:pmt-i;const pay=pr+i+P*ins;if(k===1)first=pay;if(k===n)last=pay;bal-=pr;int+=i;yi+=i;yp+=pr;if(k%12===0){rows.push([k/12,yi,yp,Math.max(0,bal)]);yi=yp=0}}
  const insT=P*ins*n;
  let h=big(type==='sac'?S.firstPay:S.monthly,m(first),type==='sac'?`${S.lastPay} ${m(last)}`:`${S.totalInt} ${m(int)}`);
  h+=kv([[S.principal,m(P)],[S.totalInt,m(int)],[S.insTotal,m(insT)],[S.totalPaid,m(P+int+insT),'t']]);
  h+=bar([[S.principal,P,'#1F5FD1'],[S.interest,int,'#C2413A'],[S.ins,insT,'#B8862B']]);
  h+='<div class="scroll"><table class="tbl"><tr><th>'+S.year+'</th><th>'+S.interest+'</th><th>'+S.principalPaid+'</th><th>'+S.balance+'</th></tr>'+rows.map(r=>`<tr><td>${r[0]}</td><td>${m(r[1],0)}</td><td>${m(r[2],0)}</td><td>${m(r[3],0)}</td></tr>`).join('')+'</table></div>';
  if(C.loanNote)h+=note(C.loanNote);
  if(val('sys')){const r2=r;const pmt2=r2?P*r2/(1-Math.pow(1+r2,-n)):P/n;const intPrice=pmt2*n-P;const intSac=r2*P*(n+1)/2;h+=note(S.cmp.replace('{p}',m(intPrice,0)).replace('{s}',m(intSac,0)))}
  out(h);
}

/* ===== Japan ===== */
function jpStock(){
  const gain=num('gain'),div=num('div'),nisa=val('nisa')==='y';const base=nisa?0:Math.max(0,gain)+div;
  const it=base*.15315,rt=base*.05,tot=it+rt;
  let h=big(S.taxTotal,m(tot),nisa?S.nisaFree:`${S.keep} ${m(gain+div-tot)}`);
  h+=kv([[S.gain,m(gain)],[S.div,m(div)],[S.itax,m(it)],[S.rtax,m(rt)],[S.total,m(tot),'t'],[S.nisaSave,m((Math.max(0,gain)+div)*.20315),'pos']]);
  out(h+note(S.n1));
}
function jpNisa(){
  const mo=num('monthly'),yrs=num('years'),r=num('ret')/100;const mr=Math.pow(1+r,1/12)-1;let bal=0,inv=0,rows=[];const capY=3600000,life=18000000;
  for(let y=1;y<=yrs;y++){for(let k=0;k<12;k++){const room=Math.min(mo,capY/12,Math.max(0,life-inv));bal=(bal+room)*(1+mr);inv+=room}rows.push([y,inv,bal])}
  const gain=bal-inv,taxSaved=gain*.20315;
  let h=big(S.final.replace('{y}',yrs),m(bal),`${S.invested} ${m(inv)} · ${S.profit} ${m(gain)}`);
  h+=kv([[S.invested,m(inv)],[S.profit,m(gain),'pos'],[S.taxSaved,m(taxSaved),'pos'],[S.taxable,m(bal-taxSaved)]]);
  h+=bar([[S.invested,inv,'#1F5FD1'],[S.profit,gain,'#0F8A5F']]);
  h+='<div class="scroll"><table class="tbl"><tr><th>'+S.year+'</th><th>'+S.invested+'</th><th>'+S.value+'</th></tr>'+rows.map(r=>`<tr><td>${r[0]}</td><td>${m(r[1])}</td><td>${m(r[2])}</td></tr>`).join('')+'</table></div>';
  out(h+note(S.n2));
}

/* ===== France ===== */
const FR=[[11600,0],[29579,.11],[84577,.30],[181917,.41],[Infinity,.45]];
function frIR(){
  const rev=num('rev'),parts=parseFloat(val('parts')),couple=val('sit')==='c';const base=couple?2:1;
  const tax1=prog(rev/parts,FR)*parts;const taxBase=prog(rev/base,FR)*base;const plaf=(parts-base)*2*1807;
  let tax=Math.max(tax1,taxBase-plaf);const brut=tax;
  const [seuil,forf]=couple?[3277,1483]:[1982,897];let dec=0;if(tax<seuil)dec=Math.min(tax,Math.max(0,forf-tax*.4525));tax-=dec;
  const tmi=FR.find(([hi])=>rev/parts<=hi)[1];
  let h=big(S.irDue,m(Math.round(tax)),`${S.tmi} ${pc(tmi,0)} · ${S.avg} ${pc(rev?tax/rev:0)}`);
  h+=kv([[S.rni,m(rev)],[S.parts,String(parts)],[S.qf,m(rev/parts)],[S.brut,m(brut)],[S.decote,m(-dec),'pos'],[S.irDue,m(Math.round(tax)),'t'],[S.monthlyPas,m(tax/12)]]);
  out(h+note(S.n3));
}
function frFlat(){
  const div=num('div'),pv=num('pv'),int=num('int'),tmi=num('tmi')/100,ps=.186;const tot=div+pv+int;
  const pfu=tot*(.128+ps);const bareme=(div*.6+pv+int)*tmi+tot*ps-(div*.6+pv+int)*.068*tmi;
  const best=bareme<pfu?S.optBar:S.optPfu;
  let h=big(S.flat314,m(pfu),`${S.better}: ${best}`);
  h+=kv([[S.income,m(tot)],['PFU 12,8 % IR',m(tot*.128)],[S.ps186,m(tot*ps)],[S.totPfu,m(pfu),'t'],[S.totBar,m(bareme)],[S.diff,m(Math.abs(pfu-bareme)),'pos']]);
  out(h+note(S.n4));
}

/* ===== Spain ===== */
function esAhorro(){
  const g=num('gain'),d=num('div'),i=num('int');const b=Math.max(0,g)+d+i;const T=[[6000,.19],[50000,.21],[200000,.23],[300000,.27],[Infinity,.30]];const t=prog(b,T);
  let h=big(S.taxTotal,m(t),b?`${S.eff} ${pc(t/b)} · ${S.keep} ${m(b-t)}`:'');
  h+=kv([[S.base,m(b)],['19 % (≤ 6.000 €)',m(Math.min(b,6000)*.19)],['21 % (6.000–50.000 €)',m(Math.max(0,Math.min(b,50000)-6000)*.21)],['23 % (50.000–200.000 €)',m(Math.max(0,Math.min(b,200000)-50000)*.23)],['27 % (200.000–300.000 €)',m(Math.max(0,Math.min(b,300000)-200000)*.27)],['30 % (> 300.000 €)',m(Math.max(0,b-300000)*.30)],[S.total,m(t),'t'],[S.withheld,m((d+i)*.19)]]);
  out(h+note(S.n5));
}

/* ===== Mexico ===== */
const MX=[[0.01,844.59,0,.0192],[844.60,7168.51,16.22,.064],[7168.52,12598.02,420.95,.1088],[12598.03,14644.64,1011.68,.16],[14644.65,17533.64,1339.14,.1792],[17533.65,35362.83,1856.84,.2136],[35362.84,55736.68,5665.16,.2352],[55736.69,106410.50,10457.09,.30],[106410.51,141880.66,25659.23,.32],[141880.67,425641.99,37009.69,.34],[425642,Infinity,133488.54,.35]];
function mxISR(){
  const s=num('sueldo');const row=MX.find(r=>s<=r[1])||MX[MX.length-1];const isr=s>0?row[2]+(s-row[0])*row[3]:0;
  const sub=val('sub')==='y'&&s<=11492.66?Math.min(isr,535.65):0;const neto=s-isr+sub;
  let h=big(S.isrMes,m(isr-sub,2),`${S.neto} ${m(neto,2)} · ${S.eff} ${pc(s?(isr-sub)/s:0,2)}`);
  h+=kv([[S.sueldo,m(s,2)],[S.li,m(row[0],2)],[S.exc,m(s-row[0],2)],[S.tasa,pc(row[3],2)],[S.cuota,m(row[2],2)],[S.isrDet,m(isr,2)],[S.subsidio,m(-sub,2),'pos'],[S.isrRet,m(isr-sub,2),'t'],[S.neto,m(neto,2)]]);
  out(h+note(S.n6));
}

/* ===== Brazil ===== */
const INSS=[[1621.00,.075],[2902.84,.09],[4354.27,.12],[8475.55,.14]];
const IR=[[2428.80,0,0],[2826.65,.075,182.16],[3751.05,.15,394.16],[4664.68,.225,675.49],[Infinity,.275,908.73]];
function brSal(){
  const sal=num('salario'),dep=num('dep'),out2=num('outros');
  const inss=prog(Math.min(sal,8475.55),INSS);
  const baseLegal=sal-inss-dep*189.59,baseSimp=sal-607.20;const base=Math.max(0,Math.min(baseLegal,baseSimp));
  const row=IR.find(r=>base<=r[0]);let ir=Math.max(0,base*row[1]-row[2]);
  let red=0;if(sal<=5000)red=Math.min(ir,312.89);else if(sal<=7350)red=Math.min(ir,Math.max(0,978.62-.133145*sal));ir-=red;
  const liq=sal-inss-ir-out2;
  let h=big(S.liquido,m(liq,2),`${S.descontos} ${m(sal-liq,2)} · ${pc(sal?1-liq/sal:0)}`);
  h+=kv([[S.bruto,m(sal,2)],['INSS',m(-inss,2),'neg'],[S.baseIr,m(base,2)],[S.irTab,m(-(ir+red),2),'neg'],[S.reducao,m(red,2),'pos'],[S.irFinal,m(-ir,2),'neg'],[S.outros,m(-out2,2),'neg'],[S.liquido,m(liq,2),'t'],[S.fgts,m(sal*.08,2),'pos']]);
  h+=bar([[S.liquido,liq,'#0F8A5F'],['INSS',inss,'#B8862B'],['IRRF',ir,'#C2413A']]);
  out(h+note(S.n7));
}

const P={loan,jpStock,jpNisa,frIR,frFlat,esAhorro,mxISR,brSal};
const fn=P[document.body.dataset.page];
if(fn){const f=$('form');const run=()=>{try{fn()}catch(e){console.error(e)}};f.addEventListener('input',run);f.addEventListener('change',run);run()}
window.W2={prog,MX,IR,INSS};
})();
