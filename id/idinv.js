/* Honglife Kalkulator Keuangan Indonesia — aturan 2026 (UU HPP, PP 55/2022, PMK 168/2023, PP 41/1994 jo. PP 14/1997, PP 131/2000) */
(function(){
'use strict';
const T={
  ptkpBase:54e6,ptkpKawin:4.5e6,ptkpTanggungan:4.5e6,
  pasal17:[[60e6,.05],[250e6,.15],[500e6,.25],[5e9,.30],[Infinity,.35]],
  biayaJabatan:.05,biayaJabatanMax:6e6,
  jht:.02,jp:.01,jpCapDefault:10547400,bpjsKes:.01,bpjsKesCap:12e6,
  saham:.001,dividen:.10,deposito:.20,depositoBebas:7.5e6,sbn:.10
};
window.ID2026=T;
const $=id=>document.getElementById(id);
const num=id=>{const e=$(id);if(!e)return 0;const raw=String(e.value).trim();const v=e.type==='number'?parseFloat(raw.replace(',','.')):parseFloat(raw.replace(/[.\sRp%]/g,'').replace(',','.'));return isFinite(v)?v:0};
const val=n=>{const c=document.querySelector(`input[name="${n}"]:checked`);return c?c.value:($(n)?$(n).value:'')};
const rp=(x)=>(x<0?'−':'')+'Rp'+Math.round(Math.abs(x)).toLocaleString('id-ID');
const jt=x=>Math.abs(x)>=1e9?'Rp'+(x/1e9).toLocaleString('id-ID',{maximumFractionDigits:2})+' M':Math.abs(x)>=1e6?'Rp'+(x/1e6).toLocaleString('id-ID',{maximumFractionDigits:1})+' jt':rp(x);
const pc=(x,d=1)=>(x*100).toLocaleString('id-ID',{minimumFractionDigits:d,maximumFractionDigits:d})+'%';
const kv=rows=>'<div class="kv">'+rows.map(r=>`<div class="${r[2]||''}">${r[0]}</div><div class="${r[2]||''}">${r[1]}</div>`).join('')+'</div>';
const big=(l,v,s)=>`<div class="big"><span>${l}</span><b>${v}</b>${s?`<em>${s}</em>`:''}</div>`;
const bar=parts=>{const tot=parts.reduce((s,p)=>s+Math.max(0,p[1]),0)||1;return '<div class="bar">'+parts.map(p=>`<i style="width:${Math.max(0,p[1])/tot*100}%;background:${p[2]}"></i>`).join('')+'</div><div class="legend">'+parts.map(p=>`<span style="--c:${p[2]}">${p[0]} ${jt(p[1])}</span>`).join('')+'</div>'};
function p17(pkp){pkp=Math.floor(Math.max(0,pkp)/1000)*1000;let t=0,lo=0;for(const [hi,r] of T.pasal17){if(pkp>lo)t+=(Math.min(pkp,hi)-lo)*r;lo=hi}return t}
window.IDTax={p17};

/* ---------- PPh 21 & gaji bersih ---------- */
function calcPPh(){
  const gaji=num('gaji'),tunj=num('tunjangan'),thr=num('thr'),kawin=val('kawin')==='k',tg=Math.min(3,num('tanggungan')),jpCap=num('jpCap')||T.jpCapDefault,npwp=true;
  const brutoBulan=gaji+tunj;const bruto=brutoBulan*12+thr;
  const jhtB=brutoBulan*T.jht,jpB=Math.min(brutoBulan,jpCap)*T.jp,kesB=Math.min(brutoBulan,T.bpjsKesCap)*T.bpjsKes;
  const bj=Math.min(bruto*T.biayaJabatan,T.biayaJabatanMax);
  const neto=bruto-bj-(jhtB+jpB)*12;const ptkp=T.ptkpBase+(kawin?T.ptkpKawin:0)+tg*T.ptkpTanggungan;
  const pkp=Math.max(0,neto-ptkp);const pph=p17(pkp);
  const take=bruto-pph-(jhtB+jpB+kesB)*12;
  const bersihBulan=brutoBulan-(jhtB+jpB+kesB)-pph/12;
  let html=big('Gaji bersih per bulan (rata-rata)',rp(bersihBulan),`Setahun ${jt(take)} termasuk THR/bonus · PPh 21 setahun ${rp(pph)}`);
  html+=kv([['Penghasilan bruto setahun',rp(bruto)],['Biaya jabatan (5%, maks Rp6 jt)',rp(-bj),'neg'],['Iuran JHT 2% + JP 1% setahun',rp(-(jhtB+jpB)*12),'neg'],['Penghasilan neto',rp(neto)],['PTKP ('+(kawin?'K':'TK')+'/'+tg+')',rp(-ptkp),'pos'],['PKP (dibulatkan ke ribuan)',rp(Math.floor(pkp/1000)*1000)],['PPh 21 terutang setahun',rp(pph),'t'],['Tarif efektif',pc(bruto?pph/bruto:0,2)],
    ['Potongan per bulan: PPh 21 (rata-rata)',rp(pph/12)],['… BPJS Kesehatan 1%',rp(kesB)],['… JHT 2%',rp(jhtB)],['… JP 1%',rp(jpB)]]);
  html+=bar([['Diterima',take,'#0F8A5F'],['PPh 21',pph,'#D9363E'],['BPJS',(jhtB+jpB+kesB)*12,'#7A8AA8']]);
  html+=`<p class="note">Dihitung setahun dengan tarif Pasal 17 UU HPP (5% s.d. Rp60 jt, 15% s.d. Rp250 jt, 25% s.d. Rp500 jt, 30% s.d. Rp5 M, 35% di atasnya). Sejak 2024 pemotongan bulanan Januari–November memakai Tarif Efektif Rata-rata (TER, PP 58/2023), lalu disetel di Desember sehingga total setahun sama dengan angka di atas. Batas upah JP disesuaikan setiap Maret oleh BPJS Ketenagakerjaan.</p>`;
  $('out').innerHTML=html;
}

/* ---------- pajak saham & dividen ---------- */
function calcSaham(){
  const beli=num('beli'),jual=num('jual'),lot=num('lot'),fb=num('feeBeli')/100,fj=num('feeJual')/100,dps=num('dps'),rein=val('reinvest')==='y';
  const lembar=lot*100;const nb=beli*lembar,nj=jual*lembar;
  const biayaB=nb*fb,biayaJ=nj*fj;const pph=nj*T.saham;
  const div=dps*lembar;const pphDiv=rein?0:div*T.dividen;
  const laba=nj-nb-biayaB-biayaJ-pph+div-pphDiv;
  let html=big(laba>=0?'Keuntungan bersih':'Kerugian bersih',rp(laba),nb?`Return ${pc(laba/(nb+biayaB),2)} dari modal ${rp(nb+biayaB)}`:'');
  html+=kv([['Nilai beli ('+lembar.toLocaleString('id-ID')+' lembar)',rp(nb)],['Fee broker beli',rp(-biayaB),'neg'],['Nilai jual',rp(nj)],['Fee broker jual (di luar PPh)',rp(-biayaJ),'neg'],['PPh final penjualan saham 0,1%',rp(-pph),'neg'],['Dividen tunai',rp(div),'pos'],['PPh dividen'+(rein?' (dikecualikan, diinvestasikan kembali)':' 10% final'),rp(-pphDiv),'neg'],['Hasil bersih',rp(laba),'t']]);
  const be=(nb+biayaB)/(lembar*(1-fj-T.saham));
  html+=`<p class="note">💡 Harga jual impas (break-even): <b>${rp(be)}</b> per lembar.</p>`;
  html+='<p class="note">PPh final 0,1% dipotong dari nilai bruto penjualan saham di BEI, baik untung maupun rugi (PP 41/1994 jo. PP 14/1997). Dividen dari perusahaan dalam negeri bebas pajak bagi WP orang pribadi dalam negeri bila diinvestasikan kembali di Indonesia dalam 3 tahun (UU HPP, PMK 18/2021); jika tidak, kena PPh final 10%. Fee broker umumnya 0,15% beli dan 0,25% jual (sudah termasuk PPh di sebagian sekuritas — cek aplikasi Anda).</p>';
  $('out').innerHTML=html;
}

/* ---------- deposito vs SBN ---------- */
function calcDepo(){
  const P=num('pokok'),r=num('bunga')/100,bln=num('tenor'),ro=val('aro')==='y',sbnR=num('kupon')/100;
  const pajak=P>T.depositoBebas?T.deposito:0;
  let bal=P,grossTot=0,taxTot=0;const periods=ro?Math.max(1,Math.round(bln)):1;
  if(ro){for(let k=0;k<bln;k++){const g=bal*r/12;const t=g*(bal>T.depositoBebas?T.deposito:0);grossTot+=g;taxTot+=t;bal+=g-t}}
  else{const g=P*r*bln/12;grossTot=g;taxTot=g*pajak;bal=P+g-taxTot}
  const net=grossTot-taxTot;const sbnNet=P*sbnR*bln/12*(1-T.sbn);
  let html=big('Bunga bersih deposito',rp(net),`Saldo akhir ${rp(bal)} · imbal hasil bersih ${pc(P?Math.pow(bal/P,12/Math.max(1,bln))-1:0,2)} per tahun`);
  html+=kv([['Bunga kotor',rp(grossTot)],['PPh final '+(pajak?'20%':'(saldo ≤ Rp7,5 juta: bebas)'),rp(-taxTot),'neg'],['Bunga bersih',rp(net),'t'],['Bunga bersih per bulan',rp(net/Math.max(1,bln))],['Pembanding: SBN ritel kupon '+pc(sbnR,2)+' (pajak 10%)',rp(sbnNet),sbnNet>net?'pos':''],['Selisih SBN − deposito',rp(sbnNet-net),sbnNet>net?'pos':'neg']]);
  html+='<p class="note">Bunga deposito dan tabungan kena PPh final 20%, kecuali total saldo di bank tersebut tidak melebihi Rp7,5 juta (PMK 212/2018). Kupon SBN ritel (ORI, SBR, ST, SR) kena PPh final 10%. Deposito dijamin LPS sampai Rp2 miliar per nasabah per bank, selama bunga tidak melebihi tingkat bunga penjaminan LPS.</p>';
  $('out').innerHTML=html;
}

/* ---------- KPR fixed + floating ---------- */
function calcKPR(){
  const harga=num('harga'),dp=num('dp')/100,thn=num('tenor'),fixR=num('fix')/100,fixY=num('fixYears'),floR=num('floating')/100;
  const P=harga*(1-dp),n=thn*12;
  const ang=(bal,r,m)=>r?bal*r/12/(1-Math.pow(1+r/12,-m)):bal/m;
  let bal=P,int=0,rows=[],yi=0,yp=0;let a1=ang(P,fixR,n),a2=null;
  for(let m=1;m<=n;m++){let a=a1;if(m>fixY*12){if(a2===null)a2=ang(bal,floR,n-m+1);a=a2}
    const r=(m>fixY*12?floR:fixR)/12;const i=bal*r;const p=a-i;bal-=p;int+=i;yi+=i;yp+=p;if(m%12===0){rows.push([m/12,a,yi,yp,Math.max(0,bal)]);yi=yp=0}}
  const gaji=a2?Math.max(a1,a2)/0.3:a1/0.3;
  let html=big('Angsuran masa bunga fixed',rp(a1)+'/bln',a2?`Setelah ${fixY} tahun (floating ${pc(floR,2)}): ${rp(a2)}/bln`:'');
  html+=kv([['Harga rumah',rp(harga)],['Uang muka (DP)',rp(harga*dp)],['Pokok pinjaman',rp(P)],['Angsuran tahun 1–'+fixY,rp(a1)],['Angsuran setelahnya (perkiraan)',a2?rp(a2):'-'],['Total bunga',rp(int)],['Total dibayar',rp(P+int),'t'],['Gaji minimal disarankan (angsuran ≤ 30%)',rp(gaji)]]);
  html+=bar([['Pokok',P,'#1F5FD1'],['Bunga',int,'#D9363E']]);
  html+='<div class="scroll"><table class="tbl"><tr><th>Tahun</th><th>Angsuran/bln</th><th>Bunga</th><th>Pokok</th><th>Sisa</th></tr>'+rows.map(r=>`<tr class="${r[0]===fixY?'hl':''}"><td>${r[0]}</td><td>${rp(r[1])}</td><td>${rp(r[2])}</td><td>${rp(r[3])}</td><td>${rp(r[4])}</td></tr>`).join('')+'</table></div>';
  html+='<p class="note">Angsuran anuitas dihitung ulang saat bunga berubah dari fixed ke floating. Bunga floating bank biasanya 9–13% per tahun dan bisa naik-turun. Biaya lain saat akad: provisi ±1%, notaris, appraisal, asuransi jiwa & kebakaran, serta BPHTB 5% dari NJOP setelah dikurangi NPOPTKP.</p>';
  $('out').innerHTML=html;
}

/* ---------- reksa dana / investasi rutin ---------- */
function calcRD(){
  const awal=num('awal'),bul=num('bulanan'),r=num('return')/100,thn=num('tahun'),naik=num('naik')/100,target=num('target');
  const mr=Math.pow(1+r,1/12)-1;let bal=awal,inv=awal,m=bul,rows=[],hitY=null;
  for(let y=1;y<=thn;y++){for(let k=0;k<12;k++){bal=(bal+m)*(1+mr);inv+=m}rows.push([y,inv,bal]);if(target&&hitY===null&&bal>=target)hitY=y;m*=1+naik}
  let html=big(`Nilai investasi setelah ${thn} tahun`,jt(bal),`Modal ${jt(inv)} · keuntungan ${jt(bal-inv)} · bebas pajak untuk reksa dana`);
  html+=kv([['Total modal disetor',rp(inv)],['Keuntungan',rp(bal-inv),'pos'],['Nilai akhir',rp(bal),'t']].concat(target?[['Target dana',rp(target)],['Target tercapai',hitY?`tahun ke-${hitY}`:'belum tercapai',hitY?'pos':'neg']]:[]));
  html+=bar([['Modal',inv,'#1F5FD1'],['Keuntungan',bal-inv,'#0F8A5F']]);
  html+='<div class="scroll"><table class="tbl"><tr><th>Tahun</th><th>Modal</th><th>Nilai</th></tr>'+rows.map(r=>`<tr class="${r[0]===hitY?'hl':''}"><td>${r[0]}</td><td>${rp(r[1])}</td><td>${rp(r[2])}</td></tr>`).join('')+'</table></div>';
  html+='<p class="note">Keuntungan dari penjualan kembali (redemption) unit reksa dana bukan objek pajak bagi investor (UU PPh Pasal 4 ayat 3). Asumsi return: pasar uang ±4–5%, pendapatan tetap ±6–7%, saham jangka panjang ±8–12% per tahun — tidak dijamin.</p>';
  $('out').innerHTML=html;
}

const PAGES={pph:calcPPh,saham:calcSaham,depo:calcDepo,kpr:calcKPR,rd:calcRD};
const fn=PAGES[document.body.dataset.page];
if(fn){const f=$('form');const run=()=>{try{fn()}catch(e){console.error(e)}};f.addEventListener('input',run);f.addEventListener('change',run);run()}
})();
