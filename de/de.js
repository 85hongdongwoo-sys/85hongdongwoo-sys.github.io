/* Honglife Deutschland-Rechner — Stand 2026 (§32a EStG 2026, SV-Rechengrößen 2026, Basiszins 2026) */
(function(){
'use strict';
const T={
  abg:.25,soli:.055,spb:{single:1000,joint:2000},
  tfs:{aktien:.30,misch:.15,immo:.60,immoAusl:.80,sonst:0},
  basiszins:.032,
  wkp:1230,sap:36,alleinerz:4260,
  soliFrei:{single:20350,joint:40700},
  rv:.186,av:.026,kv:.146,kvErm:.14,zusatz:.029,pv:.036,pvKinderlos:.006,
  bbgRV:101400,bbgKV:69750,
  grest:{BW:5,BY:3.5,BE:6,BB:6.5,HB:5.5,HH:5.5,HE:6,MV:6,NI:5,NW:6.5,RP:5,SL:6.5,SN:5.5,ST:5,SH:6.5,TH:5}
};
window.DE2026=T;
const $=id=>document.getElementById(id);
const num=id=>{const e=$(id);if(!e)return 0;const raw=String(e.value).trim();const v=e.type==='number'?parseFloat(raw.replace(',','.')):parseFloat(raw.replace(/[.\s€%]/g,'').replace(',','.'));return isFinite(v)?v:0};
const val=n=>{const c=document.querySelector(`input[name="${n}"]:checked`);return c?c.value:($(n)?$(n).value:'')};
const eur=(x,d=0)=>(x<0?'−':'')+Math.abs(x).toLocaleString('de-DE',{minimumFractionDigits:d,maximumFractionDigits:d})+' €';
const pc=(x,d=1)=>(x*100).toLocaleString('de-DE',{minimumFractionDigits:d,maximumFractionDigits:d})+' %';
const kv=rows=>'<div class="kv">'+rows.map(r=>`<div class="${r[2]||''}">${r[0]}</div><div class="${r[2]||''}">${r[1]}</div>`).join('')+'</div>';
const big=(l,v,s)=>`<div class="big"><span>${l}</span><b>${v}</b>${s?`<em>${s}</em>`:''}</div>`;
const bar=parts=>{const tot=parts.reduce((s,p)=>s+Math.max(0,p[1]),0)||1;return '<div class="bar">'+parts.map(p=>`<i style="width:${Math.max(0,p[1])/tot*100}%;background:${p[2]}"></i>`).join('')+'</div><div class="legend">'+parts.map(p=>`<span style="--c:${p[2]}">${p[0]} ${eur(p[1])}</span>`).join('')+'</div>'};

/* §32a EStG 2026 */
function est(zve){zve=Math.floor(Math.max(0,zve));let t;
  if(zve<=12348)t=0;
  else if(zve<=17799){const y=(zve-12348)/1e4;t=(914.51*y+1400)*y}
  else if(zve<=69878){const z=(zve-17799)/1e4;t=(173.10*z+2397)*z+1034.87}
  else if(zve<=277825)t=.42*zve-11135.63;
  else t=.45*zve-19470.38;
  return Math.floor(t)}
function estSplit(zve){return 2*est(zve/2)}
function soli(lst,joint){const fg=joint?T.soliFrei.joint:T.soliFrei.single;if(lst<=fg)return 0;return Math.min(lst*T.soli,(lst-fg)*.119)}
window.DETax={est,estSplit,soli};
// Abgeltungsteuer incl. Kirchensteuer (§32d Abs.1 EStG)
function abgeltung(base,kist){const k=kist/100;
  const ke=base*.25/(1+.25*k);return {kest:ke,soli:ke*T.soli,kist:ke*k,total:ke*(1+T.soli+k)}}

/* ---------- Abgeltungsteuer ---------- */
function calcAbg(){
  const joint=val('veranl')==='joint',kist=+val('kist');
  const zins=num('zinsen'),div=num('dividenden'),akt=num('aktien'),fonds=num('fonds'),ftyp=val('fondsart'),verl=num('verlust');
  const fondsSteuer=fonds*(1-T.tfs[ftyp]);
  let aktNet=akt-verl;let aktVortrag=0;if(aktNet<0){aktVortrag=-aktNet;aktNet=0}
  const summe=zins+div+aktNet+fondsSteuer;const spb=joint?T.spb.joint:T.spb.single;
  const used=Math.min(spb,Math.max(0,summe));const base=Math.max(0,summe-spb);const a=abgeltung(base,kist);
  const brutto=zins+div+akt+fonds-verl;
  let html=big('Steuer auf Ihre Kapitalerträge',eur(a.total,2),brutto>0?`Effektiv ${pc(a.total/brutto)} · netto bleiben ${eur(brutto-a.total,2)}`:'');
  html+=kv([['Kapitalerträge gesamt',eur(brutto,2)],['davon steuerfrei durch Teilfreistellung',eur(fonds-fondsSteuer,2),'pos'],['Sparerpauschbetrag genutzt',eur(used,2),'pos'],['Steuerpflichtige Erträge',eur(base,2)],
    ['Kapitalertragsteuer'+(kist?` (${pc(.25/(1+.25*kist/100),2)} wegen KiSt)`:' (25 %)'),eur(a.kest,2)],['Solidaritätszuschlag (5,5 %)',eur(a.soli,2)],['Kirchensteuer'+(kist?` (${kist} %)`:''),eur(a.kist,2)],['Summe Steuern',eur(a.total,2),'t']].concat(aktVortrag?[['Aktienverlust-Vortrag ins nächste Jahr',eur(aktVortrag,2)]]:[]));
  html+=bar([['Netto',Math.max(0,brutto-a.total),'#0F8A5F'],['KapESt',a.kest,'#1F5FD1'],['Soli',a.soli,'#D4A017'],['KiSt',a.kist,'#7A8AA8']]);
  if(summe<spb)html+=`<p class="note">💡 Sie haben noch <b>${eur(spb-summe)}</b> Sparerpauschbetrag frei. Prüfen Sie, ob Ihre Freistellungsaufträge richtig verteilt sind.</p>`;
  html+=`<p class="note">Abgeltungsteuer 25 % + 5,5 % Soli = 26,375 % (mit Kirchensteuer 8 %: 27,82 %, 9 %: 27,99 %). Für Kapitalerträge gibt es keine Soli-Freigrenze. Liegt Ihr persönlicher Steuersatz unter 25 %, beantragen Sie die Günstigerprüfung in der Anlage KAP. Aktienverluste dürfen nur mit Aktiengewinnen verrechnet werden.</p>`;
  $('out').innerHTML=html;
}

/* ---------- ETF-Sparplan mit Vorabpauschale ---------- */
function calcETF(){
  const start=num('start'),rate=num('rate'),r=num('rendite')/100,yrs=num('jahre'),ter=num('ter')/100,dyn=num('dyn')/100,bz=num('basiszins')/100,tfs=T.tfs[val('fondsart')],joint=val('veranl')==='joint',kist=+val('kist');
  const spb=joint?T.spb.joint:T.spb.single;const st=.25/(1+.25*kist/100)*(1+T.soli+kist/100);
  const mr=Math.pow(1+r-ter,1/12)-1;let bal=start,inv=start,m=rate,vpSum=0,vpTax=0,rows=[];
  for(let y=1;y<=yrs;y++){const anf=bal;let monthsW=0;
    for(let k=0;k<12;k++){bal=(bal+m)*(1+mr);inv+=m;monthsW+=m*(12-k)/12}
    const zuw=bal-anf-m*12;const basis=(anf+monthsW)*bz*.7;const vp=Math.max(0,Math.min(basis,zuw));
    const stpfl=Math.max(0,vp*(1-tfs)-spb);const tax=stpfl*st;vpSum+=vp;vpTax+=tax;
    rows.push([y,inv,bal,vp,tax]);m*=1+dyn}
  const gewinn=bal-inv;const stGew=Math.max(0,(gewinn-vpSum)*(1-tfs)-spb);const verkTax=stGew*st;
  let html=big(`Depotwert nach ${yrs} Jahren`,eur(bal),`Eingezahlt ${eur(inv)} · Gewinn ${eur(gewinn)} · nach Steuern bei Verkauf ${eur(bal-verkTax)}`);
  html+=kv([['Eingezahlt',eur(inv)],['Kursgewinn (nach TER)',eur(gewinn),'pos'],['Summe Vorabpauschalen',eur(vpSum)],['Bereits gezahlte Steuer auf Vorabpauschalen',eur(vpTax),'neg'],['Steuer bei Komplettverkauf am Ende',eur(verkTax),'neg'],['Netto nach allen Steuern',eur(bal-verkTax),'t'],['Teilfreistellung',pc(tfs,0)]]);
  html+=bar([['Eingezahlt',inv,'#1F5FD1'],['Gewinn nach Steuern',Math.max(0,gewinn-verkTax-vpTax),'#0F8A5F'],['Steuern',verkTax+vpTax,'#C2413A']]);
  html+='<div class="scroll"><table class="tbl"><tr><th>Jahr</th><th>Eingezahlt</th><th>Depotwert</th><th>Vorabpauschale</th><th>Steuer</th></tr>'+rows.map(r=>`<tr><td>${r[0]}</td><td>${eur(r[1])}</td><td>${eur(r[2])}</td><td>${eur(r[3])}</td><td>${eur(r[4])}</td></tr>`).join('')+'</table></div>';
  html+=`<p class="note">Vorabpauschale = Wert am Jahresanfang × Basiszins × 0,7 (für 2026: ${pc(T.basiszins,2)}), höchstens der tatsächliche Wertzuwachs; Käufe im Jahr zählen anteilig. Sie wird im Januar des Folgejahres besteuert und beim Verkauf angerechnet. Annahme: thesaurierender ETF, gleichbleibender Basiszins und vollständige Nutzung des Sparerpauschbetrags für diesen ETF.</p>`;
  $('out').innerHTML=html;
}

/* ---------- Brutto-Netto 2026 (Näherung) ---------- */
function calcBN(){
  const per=val('zeitraum')==='jahr'?1:12;const brutto=num('brutto')*per;const kl=val('klasse');const kist=+val('kist');const kinder=num('kinder');const alter=num('alter');const zus=num('zusatz')/100;const sachsen=val('sachsen')==='y';
  const rvB=Math.min(brutto,T.bbgRV),kvB=Math.min(brutto,T.bbgKV);
  const rv=rvB*T.rv/2,av=rvB*T.av/2,kvAN=kvB*(T.kv/2+zus/2);
  let pvAN=kvB*(sachsen?.023:T.pv/2);if(kinder===0&&alter>=23)pvAN+=kvB*T.pvKinderlos;else if(kinder>=2)pvAN-=kvB*.0025*Math.min(4,kinder-1);
  // Vorsorgepauschale (vereinfacht): RV-AN + KV-AN (ermäßigter Satz) + PV-AN + AV-AN
  const vsp=rv+kvB*(T.kvErm/2+zus/2)+pvAN+av;
  let zve=brutto-T.wkp-T.sap-vsp;if(kl==='2')zve-=T.alleinerz+Math.max(0,kinder-1)*240;
  const lst=kl==='3'?estSplit(Math.max(0,zve)):est(zve);
  const so=soli(lst,kl==='3');const ki=lst*kist/100;
  const sv=rv+av+kvAN+pvAN;const netto=brutto-lst-so-ki-sv;
  let html=big(`Netto pro ${per===12?'Monat':'Jahr'}`,eur(netto/per,2),`${eur(netto)} im Jahr · Abzüge ${pc(brutto?1-netto/brutto:0)} vom Brutto`);
  html+=kv([['Brutto',eur(brutto/per,2)],['Lohnsteuer',eur(-lst/per,2),'neg'],['Solidaritätszuschlag',eur(-so/per,2),'neg'],['Kirchensteuer',eur(-ki/per,2),'neg'],['Rentenversicherung (9,3 %)',eur(-rv/per,2),'neg'],['Arbeitslosenversicherung (1,3 %)',eur(-av/per,2),'neg'],['Krankenversicherung (7,3 % + '+pc(zus/2,2)+')',eur(-kvAN/per,2),'neg'],['Pflegeversicherung',eur(-pvAN/per,2),'neg'],['Netto',eur(netto/per,2),'t']]);
  html+=bar([['Netto',netto,'#0F8A5F'],['Steuern',lst+so+ki,'#1F5FD1'],['Sozialabgaben',sv,'#D4A017']]);
  html+=`<p class="note">Näherung nach §32a EStG 2026 mit Arbeitnehmer-Pauschbetrag (1.230 €), Vorsorgepauschale und SV-Werten 2026 (BBG Rente 8.450 €/Monat, Kranken 5.812,50 €/Monat, Ø-Zusatzbeitrag 2,9 %). Ihre Lohnabrechnung kann wegen Rundungen im Lohnsteuer-Programmablaufplan um wenige Euro abweichen. Steuerklasse V/VI und Freibeträge sind nicht berücksichtigt.</p>`;
  $('out').innerHTML=html;
}

/* ---------- Kaufnebenkosten / Grunderwerbsteuer ---------- */
function calcKNK(){
  const preis=num('preis'),land=$('land').value,makler=num('makler')/100,notar=num('notar')/100,inventar=num('inventar');
  const gs=T.grest[land]/100;const basis=Math.max(0,preis-inventar);
  const grest=basis*gs,no=preis*notar,ma=preis*makler,sum=grest+no+ma;
  let html=big('Kaufnebenkosten',eur(sum),`${pc(preis?sum/preis:0)} des Kaufpreises · Gesamtkosten ${eur(preis+sum)}`);
  html+=kv([['Grunderwerbsteuer ('+pc(gs,1)+')',eur(grest)],['Notar & Grundbuch',eur(no)],['Maklerprovision (Käuferanteil)',eur(ma)],['Summe Nebenkosten',eur(sum),'t'],['Empfohlenes Eigenkapital (Nebenkosten + 20 %)',eur(sum+preis*.2)]].concat(inventar?[['Ersparnis durch separat ausgewiesenes Inventar',eur(inventar*gs),'pos']]:[]));
  html+=bar([['Grunderwerbsteuer',grest,'#1F5FD1'],['Notar/Grundbuch',no,'#D4A017'],['Makler',ma,'#7A8AA8']]);
  const rows=Object.entries(T.grest).sort((a,b)=>a[1]-b[1]);const names={BW:'Baden-Württemberg',BY:'Bayern',BE:'Berlin',BB:'Brandenburg',HB:'Bremen',HH:'Hamburg',HE:'Hessen',MV:'Mecklenburg-Vorpommern',NI:'Niedersachsen',NW:'Nordrhein-Westfalen',RP:'Rheinland-Pfalz',SL:'Saarland',SN:'Sachsen',ST:'Sachsen-Anhalt',SH:'Schleswig-Holstein',TH:'Thüringen'};
  html+='<div class="scroll"><table class="tbl"><tr><th>Bundesland</th><th>Satz</th><th>Grunderwerbsteuer</th></tr>'+rows.map(([k,v])=>`<tr class="${k===land?'hl':''}"><td>${names[k]}</td><td>${v.toLocaleString('de-DE')} %</td><td>${eur(basis*v/100)}</td></tr>`).join('')+'</table></div>';
  html+='<p class="note">Notar- und Grundbuchkosten liegen meist bei 1,5–2 % des Kaufpreises. Seit 23.12.2020 teilen sich Käufer und Verkäufer die Maklerprovision bei Wohnungen und Einfamilienhäusern, wenn der Verkäufer den Makler beauftragt hat (üblich 3,57 % inkl. MwSt. je Seite).</p>';
  $('out').innerHTML=html;
}

/* ---------- Baufinanzierung (Annuitätendarlehen) ---------- */
function calcBau(){
  const D=num('darlehen'),z=num('zins')/100,t=num('tilgung')/100,bind=num('bindung'),sonder=num('sonder');
  const rate=D*(z+t)/12;let rest=D,m=0,zins=0,rows=[],yz=0,yt=0,restBind=null,zinsBind=0;
  while(rest>0.5&&m<1200){const zi=rest*z/12;const ti=Math.min(rest,rate-zi);rest-=ti;zins+=zi;yz+=zi;yt+=ti;m++;
    if(m%12===0){if(sonder>0&&rest>0){const s=Math.min(rest,sonder);rest-=s;yt+=s}rows.push([m/12,yz,yt,Math.max(0,rest)]);yz=yt=0}
    if(m===bind*12){restBind=rest;zinsBind=zins}}
  if(m%12)rows.push([Math.ceil(m/12),yz,yt,0]);
  let html=big('Monatliche Rate',eur(rate,2),`Restschuld nach ${bind} Jahren Zinsbindung: ${eur(restBind??0)}`);
  html+=kv([['Darlehen',eur(D)],['Sollzins / anfängliche Tilgung',pc(z,2)+' / '+pc(t,2)],['Zinsen während der Zinsbindung',eur(zinsBind||zins)],['Restschuld nach Zinsbindung',eur(restBind??0),'t'],['Volle Tilgung nach',`${Math.floor(m/12)} Jahren ${m%12} Monaten`],['Zinsen über die Gesamtlaufzeit (gleicher Zins)',eur(zins)]]);
  html+=bar([['Darlehen',D,'#1F5FD1'],['Zinsen gesamt',zins,'#C2413A']]);
  html+='<div class="scroll"><table class="tbl"><tr><th>Jahr</th><th>Zinsen</th><th>Tilgung</th><th>Restschuld</th></tr>'+rows.map(r=>`<tr class="${r[0]===bind?'hl':''}"><td>${r[0]}</td><td>${eur(r[1])}</td><td>${eur(r[2])}</td><td>${eur(r[3])}</td></tr>`).join('')+'</table></div>';
  html+='<p class="note">Annuitätendarlehen: Rate = Darlehen × (Sollzins + anfängliche Tilgung) ÷ 12, konstant über die Zinsbindung. Für die Anschlussfinanzierung wird hier derselbe Zins angenommen. Sondertilgungen werden jeweils zum Jahresende verbucht.</p>';
  $('out').innerHTML=html;
}

const PAGES={abg:calcAbg,etf:calcETF,bn:calcBN,knk:calcKNK,bau:calcBau};
const fn=PAGES[document.body.dataset.page];
if(fn){const f=$('form');const run=()=>{try{fn()}catch(e){console.error(e)}};f.addEventListener('input',run);f.addEventListener('change',run);run()}
})();
