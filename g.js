/* Hong Life Calculators — multilingual engine (en / id / es) */
(function(){
const LANG = document.documentElement.lang.slice(0,2);
const LOC = {en:'en-US', id:'id-ID', es:'es-MX'}[LANG] || 'en-US';
const CUR = {en:'$', id:'Rp ', es:'$'}[LANG];
const T = (o) => (o && typeof o === 'object' && !Array.isArray(o)) ? (o[LANG] ?? o.en) : o;
const fmt = (n, d=0) => (isFinite(n) ? n : 0).toLocaleString(LOC, {minimumFractionDigits:d, maximumFractionDigits:d});
const money = (n, d) => (n<0?'-':'') + CUR + fmt(Math.abs(n), d ?? (LANG==='id'?0:2));
const krw = n => '₩' + fmt(Math.round(n));
const pct = (n, d=2) => fmt(n, d) + '%';
const $ = id => document.getElementById(id);

/* ---------- Korea helpers ---------- */
function krIncomeTax(g, pen, hc, deps){
  let d; if(g<=5e6)d=g*.7; else if(g<=15e6)d=3.5e6+(g-5e6)*.4; else if(g<=45e6)d=7.5e6+(g-15e6)*.15; else if(g<=1e8)d=12e6+(g-45e6)*.05; else d=14.75e6+(g-1e8)*.02;
  d=Math.min(d,2e7); const base=Math.max(0,g-d-1.5e6*(1+deps)-pen-hc);
  let t; if(base<=14e6)t=base*.06; else if(base<=5e7)t=84e4+(base-14e6)*.15; else if(base<=88e6)t=624e4+(base-5e7)*.24; else if(base<=15e7)t=1536e4+(base-88e6)*.35; else t=3706e4+(base-15e7)*.38;
  let cr=t<=13e5?t*.55:715000+(t-13e5)*.3; let cap; if(g<=33e6)cap=74e4; else if(g<=7e7)cap=Math.max(66e4,74e4-(g-33e6)*.008); else if(g<=12e7)cap=Math.max(5e5,66e4-(g-7e7)*.5); else cap=Math.max(2e5,5e5-(g-12e7)*.5);
  cr=Math.min(cr,cap); const dec=Math.max(0,t-cr-130000); return dec*1.1; // incl. local income tax
}
const KR = {2026:{wage:10320, pen:0.0475}, 2027:{wage:10700, pen:0.05}};
const HEALTH=0.03595, CARE=0.1314, EMP=0.009, PEN_CAP=6370000;

/* ---------- Calculators ---------- */
const C = {};

C.loan = {
  f:[ ['amt',{en:'Loan amount',id:'Jumlah pinjaman (Rp)',es:'Monto del préstamo'},'money',{en:250000,id:300000000,es:500000}],
      ['rate',{en:'Interest rate (% per year)',id:'Bunga (% per tahun)',es:'Tasa de interés (% anual)'},'num',{en:6.5,id:7.5,es:12}],
      ['yrs',{en:'Term (years)',id:'Jangka waktu (tahun)',es:'Plazo (años)'},'num',{en:30,id:15,es:5}],
      ['type',{en:'Repayment type',id:'Metode bunga',es:'Tipo de pago'},'select',[['ann',{en:'Fixed payment (amortizing)',id:'Anuitas (cicilan tetap)',es:'Pago fijo (francés)'}],['flat',{en:'Flat rate',id:'Flat (bunga tetap)',es:'Tasa plana'}]]] ],
  run(v){
    const n=v.yrs*12, r=v.rate/100/12; let pay, total;
    if(v.type==='flat'){ pay=v.amt/n + v.amt*v.rate/100/12; total=pay*n; }
    else { pay = r ? v.amt*r/(1-Math.pow(1+r,-n)) : v.amt/n; total=pay*n; }
    const int=total-v.amt, rows=[];
    let bal=v.amt; const yearsToShow=[1,2,3,5,10,15,20,25,30].filter(y=>y<=v.yrs);
    for(let m=1;m<=n;m++){ const i = v.type==='flat'? v.amt*v.rate/100/12 : bal*r; bal -= (pay-i); if(yearsToShow.includes(m/12)) rows.push([T({en:'Balance after year ',id:'Sisa pokok tahun ke-',es:'Saldo al año '})+(m/12),'',money(Math.max(bal,0))]); }
    return { k:T({en:'Monthly payment',id:'Cicilan per bulan',es:'Pago mensual'}), big:money(pay), sub:T({en:'Total interest ',id:'Total bunga ',es:'Intereses totales '})+money(int)+' · '+T({en:'Total paid ',id:'Total bayar ',es:'Total pagado '})+money(total),
      rows:[[T({en:'Principal',id:'Pokok pinjaman',es:'Capital'}),'',money(v.amt)],[T({en:'Total interest',id:'Total bunga',es:'Intereses'}),'',money(int)],['__t',T({en:'Total of payments',id:'Total pembayaran',es:'Total de pagos'}),money(total)],...rows],
      note: v.type==='flat'? T({en:'Flat-rate loans charge interest on the original amount every month, so the real annual rate is much higher than the quoted rate.',id:'Bunga flat dihitung dari pokok awal setiap bulan, sehingga bunga efektifnya jauh lebih tinggi dari angka yang ditawarkan.',es:'Con tasa plana el interés se cobra siempre sobre el monto original, por lo que la tasa efectiva es mucho mayor.'}) : '' };
  }
};

C.compound = {
  f:[ ['p',{en:'Initial deposit',id:'Setoran awal (Rp)',es:'Depósito inicial'},'money',{en:10000,id:10000000,es:20000}],
      ['m',{en:'Monthly contribution',id:'Setoran per bulan (Rp)',es:'Aportación mensual'},'money',{en:500,id:1000000,es:2000}],
      ['rate',{en:'Annual return (%)',id:'Imbal hasil per tahun (%)',es:'Rendimiento anual (%)'},'num',{en:7,id:6,es:9}],
      ['yrs',{en:'Years',id:'Lama (tahun)',es:'Años'},'num',{en:20,id:10,es:15}],
      ['tax',{en:'Tax on gains (%)',id:'Pajak atas bunga (%)',es:'Impuesto sobre ganancias (%)'},'num',{en:0,id:20,es:0}] ],
  run(v){
    const r=v.rate/100/12; let bal=v.p, rows=[];
    for(let m=1;m<=v.yrs*12;m++){ bal = bal*(1+r) + v.m; if(m%12===0 && ([1,3,5,10,15,20,25,30,40].includes(m/12)||m/12===v.yrs)) rows.push([T({en:'Year ',id:'Tahun ',es:'Año '})+(m/12),'',money(bal)]); }
    const paid=v.p+v.m*v.yrs*12, gain=bal-paid, net=paid+gain*(1-v.tax/100);
    return { k:T({en:'Future value',id:'Nilai akhir',es:'Valor futuro'}), big:money(net), sub:T({en:'You put in ',id:'Total setoran ',es:'Aportaste '})+money(paid)+' · '+T({en:'Growth ',id:'Hasil ',es:'Ganancia '})+money(gain*(1-v.tax/100)),
      rows:[[T({en:'Total contributions',id:'Total setoran',es:'Total aportado'}),'',money(paid)],[T({en:'Investment growth',id:'Hasil investasi',es:'Rendimiento'}),v.tax?T({en:'after tax',id:'setelah pajak',es:'después de impuestos'}):'',money(gain*(1-v.tax/100))],['__t',T({en:'Ending balance',id:'Saldo akhir',es:'Saldo final'}),money(net)],...rows],
      note:T({en:'Returns are compounded monthly and are not guaranteed. Try a lower rate to stress-test your plan.',id:'Bunga dihitung majemuk bulanan dan tidak dijamin. Deposito di Indonesia dikenai pajak bunga 20%.',es:'El rendimiento se capitaliza mensualmente y no está garantizado. Prueba con una tasa menor para ser conservador.'}) };
  }
};

C.percent = {
  f:[ ['mode',{en:'What do you want to know?',id:'Mau menghitung apa?',es:'¿Qué quieres calcular?'},'select',[['of',{en:'What is X% of Y?',id:'Berapa X% dari Y?',es:'¿Cuánto es X% de Y?'}],['is',{en:'X is what % of Y?',id:'X itu berapa persen dari Y?',es:'¿X qué porcentaje es de Y?'}],['chg',{en:'% change from X to Y',id:'Persentase kenaikan/penurunan X ke Y',es:'Variación % de X a Y'}],['disc',{en:'Price after X% discount on Y',id:'Harga setelah diskon X% dari Y',es:'Precio con X% de descuento sobre Y'}]]],
      ['x',{en:'X',id:'X',es:'X'},'num',{en:15,id:20,es:16}],
      ['y',{en:'Y',id:'Y',es:'Y'},'num',{en:240,id:150000,es:1250}] ],
  run(v){
    let big, sub;
    if(v.mode==='of'){ big=fmt(v.x/100*v.y,2); sub=`${fmt(v.x,2)}% × ${fmt(v.y,2)}`; }
    else if(v.mode==='is'){ big=pct(v.y? v.x/v.y*100:0); sub=`${fmt(v.x,2)} ÷ ${fmt(v.y,2)} × 100`; }
    else if(v.mode==='chg'){ const c=v.x? (v.y-v.x)/v.x*100:0; big=(c>0?'+':'')+pct(c); sub=`(${fmt(v.y,2)} − ${fmt(v.x,2)}) ÷ ${fmt(v.x,2)} × 100`; }
    else { const p=v.y*(1-v.x/100); big=fmt(p,2); sub=T({en:'You save ',id:'Hemat ',es:'Ahorras '})+fmt(v.y-p,2); }
    return {k:T({en:'Result',id:'Hasil',es:'Resultado'}), big, sub, rows:[], note:''};
  }
};

C.age = {
  f:[ ['b',{en:'Date of birth',id:'Tanggal lahir',es:'Fecha de nacimiento'},'date','1990-05-15'],
      ['d',{en:'Age on date',id:'Dihitung sampai tanggal',es:'Calcular a la fecha'},'date','today'] ],
  run(v){
    const b=new Date(v.b+'T00:00'), d=new Date(v.d+'T00:00'); if(isNaN(b)||isNaN(d)||d<b) return {k:'',big:'—',sub:'',rows:[]};
    let y=d.getFullYear()-b.getFullYear(), m=d.getMonth()-b.getMonth(), dd=d.getDate()-b.getDate();
    if(dd<0){ m--; dd+=new Date(d.getFullYear(), d.getMonth(), 0).getDate(); } if(m<0){ y--; m+=12; }
    const days=Math.round((d-b)/864e5); let nb=new Date(d.getFullYear(), b.getMonth(), b.getDate()); if(nb<d) nb.setFullYear(d.getFullYear()+1);
    const until=Math.round((nb-d)/864e5), wk=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    const wdays={en:wk,id:['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu'],es:['domingo','lunes','martes','miércoles','jueves','viernes','sábado']}[LANG];
    const Y=T({en:' years',id:' tahun',es:' años'}), M=T({en:' months',id:' bulan',es:' meses'}), D=T({en:' days',id:' hari',es:' días'});
    return {k:T({en:'Age',id:'Umur',es:'Edad'}), big:y+Y, sub:y+Y+' '+m+M+' '+dd+D,
      rows:[[T({en:'Total months',id:'Total bulan',es:'Meses totales'}),'',fmt(y*12+m)],[T({en:'Total weeks',id:'Total minggu',es:'Semanas totales'}),'',fmt(Math.floor(days/7))],[T({en:'Total days',id:'Total hari',es:'Días totales'}),'',fmt(days)],
        [T({en:'Day of the week you were born',id:'Hari lahir',es:'Día de la semana en que naciste'}),'',wdays[b.getDay()]],[T({en:'Next birthday in',id:'Ulang tahun berikutnya',es:'Próximo cumpleaños en'}),'',until+D]], note:''};
  }
};

C.bmi = {
  f:[ ['unit',{en:'Units',id:'Satuan',es:'Unidades'},'select',[['m',{en:'Metric (kg, cm)',id:'Metrik (kg, cm)',es:'Métrico (kg, cm)'}],['i',{en:'US (lb, ft/in)',id:'Imperial (lb, inci)',es:'Imperial (lb, pulgadas)'}]], {en:'i',id:'m',es:'m'}],
      ['w',{en:'Weight (kg or lb)',id:'Berat badan (kg)',es:'Peso (kg)'},'num',{en:170,id:65,es:72}],
      ['h',{en:'Height (cm, or total inches)',id:'Tinggi badan (cm)',es:'Estatura (cm)'},'num',{en:69,id:165,es:168}],
      ['asia',{en:'Use Asian BMI cut-offs',id:'Pakai standar Asia (Kemenkes)',es:'Usar puntos de corte asiáticos'},'check',{en:false,id:true,es:false}] ],
  run(v){
    const kg = v.unit==='i'? v.w*0.453592 : v.w, m = v.unit==='i'? v.h*0.0254 : v.h/100;
    const bmi = m? kg/(m*m) : 0;
    const cut = v.asia? [18.5,23,25,30] : [18.5,25,30,35];
    const lab = { en:['Underweight','Healthy weight','Overweight','Obese','Severely obese'], id:['Berat badan kurang','Normal','Berat badan lebih','Obesitas I','Obesitas II'], es:['Bajo peso','Peso saludable','Sobrepeso','Obesidad I','Obesidad II'] }[LANG];
    let i=0; while(i<cut.length && bmi>=cut[i]) i++;
    const lo=cut[0]*m*m, hi=cut[1]*m*m, toW = x => v.unit==='i'? fmt(x/0.453592,1)+' lb' : fmt(x,1)+' kg';
    return {k:'BMI', big:fmt(bmi,1), sub:lab[i], rows:[[T({en:'Healthy weight range for your height',id:'Berat ideal untuk tinggi Anda',es:'Rango de peso saludable para tu estatura'}),'',toW(lo)+' – '+toW(hi)],
      ...cut.map((c,j)=>[lab[j+1], '', '≥ '+fmt(c,1)])],
      note:T({en:'BMI is a screening tool, not a diagnosis. It does not account for muscle mass, age or body shape.',id:'BMI hanya alat skrining, bukan diagnosis. Tidak memperhitungkan massa otot, usia, atau bentuk tubuh.',es:'El IMC es una herramienta de detección, no un diagnóstico. No considera masa muscular, edad ni complexión.'})};
  }
};

/* ---- Korea (English) ---- */
C.krsalary = {
  f:[ ['g',{en:'Annual salary before tax (KRW)'},'money',{en:42000000}],
      ['nt',{en:'Non-taxable meal allowance (KRW / month)'},'money',{en:200000}],
      ['deps',{en:'Dependents (spouse, children)'},'num',{en:0}],
      ['yr',{en:'Tax year'},'select',[['2026',{en:'2026'}],['2027',{en:'2027'}]],{en:'2027'}],
      ['flat',{en:'Compare with 19% flat tax for foreigners'},'check',{en:true}] ],
  cur:'krw',
  run(v){
    const nt=Math.min(v.nt,200000)*12, taxable=Math.max(v.g-nt,0), mon=taxable/12, Y=KR[+v.yr];
    const pen=Math.min(mon,PEN_CAP)*Y.pen*12, h=taxable*HEALTH, care=h*CARE, emp=taxable*EMP;
    const tax=krIncomeTax(taxable,pen,h+care,v.deps), net=v.g-pen-h-care-emp-tax;
    const flatTax=v.g*0.19*1.1, netFlat=v.g-pen-h-care-emp-flatTax;
    const rows=[[`National Pension (${(Y.pen*100).toFixed(2)}%)`,'capped at ₩6.37M monthly income',krw(-pen)],['Health insurance (3.595%)','',krw(-h)],['Long-term care (13.14% of health)','',krw(-care)],['Employment insurance (0.9%)','',krw(-emp)],['Income tax + local tax','progressive rates, standard deductions',krw(-tax)],['__t','Take-home per year',krw(net)]];
    if(v.flat) rows.push(['19% flat-rate option','20.9% incl. local tax on gross pay (no deductions)', krw(netFlat/12)+' /mo']);
    return {k:'Monthly take-home pay', big:krw(net/12), sub:`${krw(net)} per year · ${pct(net/v.g*100,1)} of gross`, rows:rows.map(r=>[r[0],r[1],String(r[2]).replace('₩-','−₩')]),
      note:`The flat 19% option is available to foreign employees for their first 20 years of work in Korea. ${v.flat?(netFlat>net?'For your salary the flat rate gives more take-home pay.':'For your salary the normal progressive rates give more take-home pay.'):''} Monthly withholding follows the simplified tax table and is settled in the year-end tax settlement (Feb).`};
  }
};
C.krsev = {
  f:[ ['m',{en:'Average monthly pay over the last 3 months (KRW)'},'money',{en:3200000}],
      ['bonus',{en:'Annual bonus (KRW, optional)'},'money',{en:0}],
      ['s',{en:'Start date'},'date','2022-03-02'], ['e',{en:'Last working day'},'date','today'] ],
  cur:'krw',
  run(v){
    const s=new Date(v.s+'T00:00'), e=new Date(v.e+'T00:00'); const days=Math.round((e-s)/864e5)+1;
    if(!(days>0)) return {k:'',big:'—',sub:'',rows:[]};
    const daily=(v.m*3 + v.bonus*3/12)/91, pay = days>=365 ? daily*30*days/365 : 0;
    return {k:'Estimated severance pay', big: days>=365? krw(pay):'Not eligible yet', sub: days>=365? `${fmt(days/365,2)} years of service · average daily wage ${krw(daily)}` : `You need at least 1 year (365 days) of service. You have ${fmt(days)} days.`,
      rows:[['Days of service','',fmt(days)],['Average daily wage','last 3 months pay ÷ 91 days',krw(daily)],['Formula','daily wage × 30 days × (days of service ÷ 365)',''],['__t','Severance pay (before tax)',krw(pay)]],
      note:'Severance pay is required for anyone who worked at least 15 hours a week for 1 year or more, including foreign workers. It must be paid within 14 days of leaving. Retirement income tax is low (often a few percent). E-9 workers receive part of it through departure guarantee insurance.'};
  }
};
C.krpen = {
  f:[ ['m',{en:'Average monthly salary in Korea (KRW)'},'money',{en:3500000}],
      ['y',{en:'Years you paid into the National Pension'},'num',{en:5}],
      ['int',{en:'Interest added (% per year, approx.)'},'num',{en:2.5}] ],
  cur:'krw',
  run(v){
    const base=Math.min(v.m,PEN_CAP); let total=0, contrib=0;
    for(let i=0;i<v.y*12;i++){ const yr=2027-Math.ceil((v.y*12-i)/12); const rate= yr>=2027?0.10: yr===2026?0.095:0.09; const c=base*rate; contrib+=c; total = total*(1+v.int/100/12) + c; }
    return {k:'Estimated lump-sum refund', big:krw(total), sub:`Your share + employer share for ${v.y} years, with interest`,
      rows:[['Monthly contribution (you + employer)','9% until 2025 · 9.5% in 2026 · 10% in 2027',krw(base*0.10)],['Total contributions','',krw(contrib)],['Interest (approx.)','',krw(total-contrib)],['__t','Refund estimate',krw(total)]],
      note:'Foreigners can claim the National Pension lump-sum refund when leaving Korea if their home country has a refund agreement with Korea or refunds Koreans in the same way (e.g. USA, Canada, Australia, Indonesia, Vietnam, Philippines). Some countries (e.g. Germany) have totalization agreements instead. Check with the National Pension Service before leaving; you can apply at the airport.'};
  }
};

/* ---- Indonesia ---- */
C.idkorea = {
  f:[ ['yr',{id:'Tahun'},'select',[['2026',{id:'2026 (₩10.320 per jam)'}],['2027',{id:'2027 (₩10.700 per jam)'}]],{id:'2027'}],
      ['wage',{id:'Upah per jam (₩)'},'money',{id:10700}],
      ['ot',{id:'Lembur per bulan (jam)'},'num',{id:40}],
      ['night',{id:'Kerja malam 22.00–06.00 (jam/bulan)'},'num',{id:0}],
      ['hol',{id:'Kerja hari libur (jam/bulan)'},'num',{id:16}],
      ['rate',{id:'Kurs: 1 won = Rp'},'num',{id:11.5}],
      ['dorm',{id:'Potongan asrama/makan (₩/bulan)'},'money',{id:200000}] ],
  cur:'krw',
  run(v){
    const w=v.wage, basic=w*209, ot=w*1.5*v.ot, night=w*0.5*v.night, hol=w*1.5*v.hol, gross=basic+ot+night+hol;
    const Y=KR[+v.yr]; const pen=Math.min(gross,PEN_CAP)*Y.pen, h=gross*HEALTH, care=h*CARE, emp=gross*EMP;
    const tax=krIncomeTax(gross*12,pen*12,(h+care)*12,0)/12, net=gross-pen-h-care-emp-tax-v.dorm;
    return {k:'Gaji bersih per bulan', big:krw(net), sub:`≈ Rp ${fmt(net*v.rate)} · kotor ${krw(gross)}`,
      rows:[['Gaji pokok','209 jam × upah per jam (sudah termasuk hari libur mingguan)',krw(basic)],['Lembur','upah × 1,5 × '+v.ot+' jam',krw(ot)],['Tunjangan malam','upah × 0,5 × '+v.night+' jam',krw(night)],['Kerja hari libur','upah × 1,5 × '+v.hol+' jam',krw(hol)],['__t','Gaji kotor',krw(gross)],
        ['Pensiun nasional ('+(Y.pen*100).toFixed(2)+'%)','bisa diklaim kembali saat pulang',krw(-pen)],['Asuransi kesehatan + perawatan','',krw(-(h+care))],['Asuransi kerja (0,9%)','',krw(-emp)],['Pajak penghasilan','perkiraan',krw(-tax)],['Asrama / makan','',krw(-v.dorm)],['__t','Diterima bersih',krw(net)],['Dalam rupiah','kurs '+fmt(v.rate,2),'Rp '+fmt(net*v.rate)]].map(r=>[r[0],r[1],String(r[2]).replace('₩-','−₩')]),
      note:'Upah minimum Korea 2026 ₩10.320/jam, 2027 ₩10.700/jam (₩2.236.300/bulan). Lembur, kerja malam, dan hari libur dibayar 1,5 kali (malam +50%) di perusahaan dengan 5 karyawan atau lebih. Iuran pensiun nasional bisa diambil kembali saat pulang ke Indonesia.'};
  }
};
C.thr = {
  f:[ ['p',{id:'Gaji pokok per bulan (Rp)'},'money',{id:5000000}],
      ['a',{id:'Tunjangan tetap per bulan (Rp)'},'money',{id:500000}],
      ['mk',{id:'Masa kerja (bulan)'},'num',{id:8}] ],
  run(v){
    const upah=v.p+v.a, thr = v.mk>=12 ? upah : v.mk>=1 ? upah*v.mk/12 : 0;
    return {k:'THR yang diterima', big:money(thr), sub: v.mk>=12?'Masa kerja 12 bulan atau lebih: 1 bulan upah': v.mk>=1?`Proporsional: ${v.mk}/12 × upah sebulan`:'Belum berhak (masa kerja kurang dari 1 bulan)',
      rows:[['Upah sebulan','gaji pokok + tunjangan tetap',money(upah)],['Masa kerja','',v.mk+' bulan'],['__t','THR',money(thr)]],
      note:'Dasar hukum: Permenaker No. 6 Tahun 2016. THR wajib dibayar paling lambat 7 hari sebelum Hari Raya Keagamaan. Pekerja harian lepas dihitung dari rata-rata upah 12 bulan terakhir. THR dikenai PPh 21.'};
  }
};
C.zakat = {
  f:[ ['inc',{id:'Penghasilan per bulan (Rp)'},'money',{id:12000000}],
      ['other',{id:'Penghasilan lain per bulan (Rp)'},'money',{id:0}],
      ['gold',{id:'Harga emas per gram (Rp)'},'money',{id:2540000}],
      ['debt',{id:'Cicilan utang kebutuhan pokok per bulan (Rp, opsional)'},'money',{id:0}] ],
  run(v){
    const nisabY=85*v.gold, nisabM=nisabY/12, inc=v.inc+v.other-v.debt, wajib=inc>=nisabM, z= wajib? inc*0.025:0;
    return {k:'Zakat penghasilan per bulan', big:money(z), sub: wajib?'Penghasilan sudah mencapai nisab — wajib zakat 2,5%':'Penghasilan belum mencapai nisab — belum wajib zakat (tetap bisa berinfak)',
      rows:[['Nisab per tahun','85 gram emas × harga emas',money(nisabY)],['Nisab per bulan','',money(nisabM)],['Penghasilan dihitung','',money(inc)],['__t','Zakat per bulan (2,5%)',money(z)],['Zakat per tahun','',money(z*12)]],
      note:'Mengacu pada ketentuan BAZNAS (nisab setara 85 gram emas, kadar 2,5%). Harga emas berubah setiap hari; harga Antam akhir Oktober 2026 sekitar Rp2,5 juta per gram.'};
  }
};

/* ---- Mexico ---- */
const SM={gen:315.04, fr:440.87}, UMA=117.31;
function vacDays(y){ if(y<1) return 12; if(y<=5) return 12+2*(Math.ceil(y)-1); return 20+2*Math.ceil((Math.ceil(y)-5)/5); }
C.aguinaldo = {
  f:[ ['s',{es:'Sueldo mensual bruto ($)'},'money',{es:15000}],
      ['dias',{es:'Días de aguinaldo que da tu empresa'},'num',{es:15}],
      ['trab',{es:'Días trabajados en el año'},'num',{es:365}] ],
  run(v){
    const sd=v.s/30, ag=sd*v.dias*Math.min(v.trab,365)/365, ex=Math.min(ag,30*UMA), grav=ag-ex;
    return {k:'Tu aguinaldo (bruto)', big:money(ag), sub:`Salario diario ${money(sd)} × ${v.dias} días${v.trab<365?` × ${v.trab}/365`:''}`,
      rows:[['Salario diario','sueldo mensual ÷ 30',money(sd)],['Aguinaldo bruto','',money(ag)],['Parte exenta de ISR','hasta 30 UMA (30 × $117.31)',money(ex)],['Parte gravada','paga ISR',money(grav)]],
      note:'La Ley Federal del Trabajo (art. 87) obliga a pagar al menos 15 días de salario antes del 20 de diciembre. Si no trabajaste todo el año, recibes la parte proporcional. UMA 2026: $117.31 diarios.'};
  }
};
C.finiquito = {
  f:[ ['s',{es:'Sueldo mensual bruto ($)'},'money',{es:15000}],
      ['ini',{es:'Fecha de ingreso'},'date','2021-06-01'],['fin',{es:'Fecha de salida'},'date','today'],
      ['pend',{es:'Días de sueldo pendientes de pago'},'num',{es:10}],
      ['vacT',{es:'Días de vacaciones ya tomados este año'},'num',{es:0}],
      ['tipo',{es:'Motivo de salida'},'select',[['ren',{es:'Renuncia voluntaria (finiquito)'}],['desp',{es:'Despido injustificado (liquidación)'}]]],
      ['zona',{es:'Zona'},'select',[['gen',{es:'Resto del país'}],['fr',{es:'Zona libre de la frontera norte'}]]] ],
  run(v){
    const a=new Date(v.ini+'T00:00'), b=new Date(v.fin+'T00:00'); const days=Math.round((b-a)/864e5)+1; if(!(days>0)) return {k:'',big:'—',sub:'',rows:[]};
    const yrs=days/365, sd=v.s/30, pend=sd*v.pend;
    const yStart=new Date(b.getFullYear(),0,1), dY=Math.round((b-Math.max(yStart,a))/864e5)+1;
    const ag=sd*15*dY/365;
    const anniv=new Date(b.getFullYear(),a.getMonth(),a.getDate()); if(anniv>b) anniv.setFullYear(b.getFullYear()-1);
    const sinceAnniv=Math.max(0,Math.round((b-Math.max(anniv,a))/864e5)), vd=vacDays(Math.max(yrs,0.01)), vac=Math.max(0, sd*(vd*sinceAnniv/365 - v.vacT)), prima=vac*0.25;
    let rows=[['Sueldo pendiente',v.pend+' días',money(pend)],['Aguinaldo proporcional',`15 días × ${dY}/365`,money(ag)],['Vacaciones proporcionales',`${vd} días/año × ${sinceAnniv}/365 − tomados`,money(vac)],['Prima vacacional','25% de las vacaciones',money(prima)]];
    let total=pend+ag+vac+prima;
    if(v.tipo==='desp'){ const m3=sd*90, d20=sd*20*yrs, sdTope=Math.min(sd,2*SM[v.zona]), pa=sdTope*12*yrs; rows.push(['Indemnización 3 meses','90 días de salario',money(m3)],['20 días por año','solo si no hay reinstalación (art. 50)',money(d20)],['Prima de antigüedad','12 días por año, tope 2 salarios mínimos',money(pa)]); total+=m3+d20+pa; }
    rows.push(['__t',v.tipo==='desp'?'Total liquidación (bruto)':'Total finiquito (bruto)',money(total)]);
    return {k:v.tipo==='desp'?'Liquidación estimada':'Finiquito estimado', big:money(total), sub:`Antigüedad ${fmt(yrs,2)} años · salario diario ${money(sd)}`, rows,
      note:'Cálculo con LFT vigente (vacaciones dignas 2023: 12 días el primer año). Montos brutos antes de ISR. Los 20 días por año aplican en casos específicos; consulta a la PROFEDET (gratis) si te despidieron.'};
  }
};
C.vacaciones = {
  f:[ ['s',{es:'Sueldo mensual bruto ($)'},'money',{es:15000}],
      ['y',{es:'Años cumplidos en la empresa'},'num',{es:3}],
      ['pr',{es:'Prima vacacional (%)'},'num',{es:25}] ],
  run(v){
    const d=vacDays(Math.max(v.y,1)), sd=v.s/30, pago=sd*d, prima=pago*v.pr/100, ex=Math.min(prima,15*UMA);
    const tbl=[1,2,3,4,5,10,15,20,25,30].map(y=>[`${y} año${y>1?'s':''}`,'',vacDays(y)+' días']);
    return {k:'Días de vacaciones', big:d+' días', sub:`Prima vacacional ${money(prima)} (${v.pr}% de ${money(pago)})`,
      rows:[['Salario de los días de vacaciones',`${d} × ${money(sd)}`,money(pago)],['Prima vacacional',v.pr+'%',money(prima)],['Prima exenta de ISR','hasta 15 UMA',money(ex)],...tbl],
      note:'Desde 2023 (reforma "vacaciones dignas") son 12 días el primer año, +2 por año hasta 20 días en el quinto, y luego +2 cada 5 años. La prima vacacional mínima es 25%.'};
  }
};

/* ---------- renderer ---------- */
function build(id){
  const spec=C[id], form=$('form'), out=$('out'), q={};
  const today=new Date().toISOString().slice(0,10);
  form.innerHTML = spec.f.map(([key,label,type,a,b])=>{
    const L=T(label);
    if(type==='select'){ const def=T(b)||a[0][0]; return `<div class="field"><label for="f_${key}">${L}</label><select id="f_${key}">${a.map(([v,l])=>`<option value="${v}"${v===def?' selected':''}>${T(l)}</option>`).join('')}</select></div>`; }
    if(type==='check'){ return `<label class="check"><input type="checkbox" id="f_${key}"${T(a)?' checked':''}><span>${L}</span></label>`; }
    if(type==='date'){ return `<div class="field"><label for="f_${key}">${L}</label><input type="date" id="f_${key}" value="${a==='today'?today:a}"></div>`; }
    const dv=T(a); const shown= type==='money'? fmt(dv) : Number(dv).toLocaleString(LOC,{useGrouping:false,maximumFractionDigits:4}); return `<div class="field"><label for="f_${key}">${L}</label><input id="f_${key}" inputmode="decimal" value="${shown}"></div>`;
  }).join('');
  const read=()=>{ const v={}; spec.f.forEach(([key,,type])=>{ const el=$('f_'+key);
    if(type==='check') v[key]=el.checked; else if(type==='select'||type==='date') v[key]=el.value;
    else { const raw=String(el.value).replace(/\s/g,''); const s= LANG==='id' ? raw.replace(/\./g,'').replace(/,/g,'.') : raw.replace(/,/g,''); v[key]=parseFloat(s)||0; } }); return v; };
  const render=()=>{ const r=spec.run(read());
    out.innerHTML=`<p class="kicker">${r.k||''}</p><p class="big">${r.big}</p><p class="bigsub">${r.sub||''}</p>`+
      (r.rows&&r.rows.length?`<table>${r.rows.map(x=> x[0]==='__t'?`<tr class="t"><td>${x[1]}</td><td class="n">${x[2]}</td></tr>`:`<tr${String(x[2]).startsWith('−')?' class="m"':''}><td>${x[0]}${x[1]?`<span class="c">${x[1]}</span>`:''}</td><td class="n">${x[2]}</td></tr>`).join('')}</table>`:'')+
      (r.note?`<p class="note">${r.note}</p>`:''); };
  form.addEventListener('input',render); form.addEventListener('change',render);
  form.addEventListener('focusout',e=>{ const el=e.target; if(el.tagName!=='INPUT'||el.type!=='text'&&el.type!=='') return; const key=el.id.slice(2); const f=spec.f.find(x=>x[0]===key); if(f&&f[2]==='money'){ const v=read()[key]; el.value=fmt(v); } });
  render();
}
document.addEventListener('DOMContentLoaded',()=>{ const app=document.querySelector('[data-calc]'); if(app) build(app.dataset.calc); });
})();
