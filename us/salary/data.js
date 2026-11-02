/* Honglife — US salary after-tax data & engine, tax year 2026 (returns filed in 2027).
   Single filer, wages only, standard deduction, no 401(k)/pre-tax benefits, no local income tax,
   no state payroll taxes (CA SDI, NY PFL/DI, NJ/WA/MA/OR/RI/HI payroll programs etc.).
   As of: 2026-11-03.
   Federal: IRS Rev. Proc. 2025-32 (2026 inflation adjustments incl. One Big Beautiful Bill Act changes);
            SSA 2026 COLA fact sheet (Social Security wage base $184,500); IRC §3101(b)(2) additional Medicare tax.
   States : Tax Foundation "State Individual Income Tax Rates and Brackets, 2026" (rates as of Jan 1, 2026),
            updated for laws enacted during 2026 and checked against state revenue departments — see `src` per state.
   Works in the browser (window.USSalary) and in Node (module.exports). */
(function (root) {
'use strict';

var FED = {
  year: 2026,
  std: 16100,
  // [upper bound, rate]; last bound Infinity
  br: [[12400, .10], [50400, .12], [105700, .22], [201775, .24], [256225, .32], [640600, .35], [Infinity, .37]],
  ssWage: 184500, ssRate: .062, medRate: .0145, addMedRate: .009, addMedThreshold: 200000,
  hours: 2080,
  src: ['IRS Rev. Proc. 2025-32 (tax year 2026)', 'SSA 2026 Social Security fact sheet (wage base $184,500)', 'IRS Topic 560 (Additional Medicare Tax 0.9% over $200,000 single)']
};

/* progressive tax from [[threshold, rate], ...] where rate applies to income ABOVE threshold */
function prog(ti, sch) {
  ti = Math.max(0, ti); var t = 0;
  for (var i = 0; i < sch.length; i++) {
    var lo = sch[i][0], hi = i + 1 < sch.length ? sch[i + 1][0] : Infinity;
    if (ti > lo) t += (Math.min(ti, hi) - lo) * sch[i][1];
  }
  return t;
}
function fedIncomeTax(ti) {
  ti = Math.max(0, ti); var t = 0, lo = 0;
  for (var i = 0; i < FED.br.length; i++) { var hi = FED.br[i][0]; if (ti > lo) t += (Math.min(ti, hi) - lo) * FED.br[i][1]; lo = hi; }
  return t;
}
function fedMarginal(ti) { for (var i = 0; i < FED.br.length; i++) if (ti <= FED.br[i][0]) return FED.br[i][1]; return .37; }
function steps(x, lo, size) { return x > lo ? Math.ceil((x - lo) / size) : 0; } // "each $size or fraction thereof"

/* ---------------- states ----------------
   b   : bracket schedule [[threshold, rate],...] applied to state taxable income
   std : standard deduction, ex: personal exemption (deductions), cr: flat nonrefundable credit
   base: 'agi' (default) or 'fedti' (state starts from federal taxable income, i.e. after the $16,100 federal standard deduction)
   fn  : custom function(w, ctx) -> tax  (overrides generic)                                                     */
var S = [
 {a:'AL',n:'Alabama',b:[[0,.02],[500,.04],[3000,.05]],std:3000,ex:1500,
  rule:'2% / 4% / 5% brackets; $3,000 standard deduction (falls to $2,500 as income rises), $1,500 personal exemption, and federal income tax paid is deductible.',
  fn:function(w,c){var std=Math.max(2500,3000-25*steps(w,23000,500));return prog(w-std-1500-c.fedTax,this.b)},
  local:'Some cities and counties (e.g. Birmingham, Bessemer) levy occupational taxes.',src:'Tax Foundation 2026; Alabama DOR (Ala. Code §40-18-15, -19)'},
 {a:'AK',n:'Alaska',none:true,rule:'No state income tax on wages.',src:'Tax Foundation 2026'},
 {a:'AZ',n:'Arizona',b:[[0,.025]],std:15750,
  rule:'Flat 2.5%; standard deduction $15,750 under HB 4168 (signed June 2026).',
  src:'Tax Foundation 2026; Arizona HB 4168 (2026), A.R.S. §43-1041'},
 {a:'AR',n:'Arkansas',std:2470,cr:29,
  rule:'Graduated tables topping out at 3.7% (cut from 3.9% retroactive to Jan 1, 2026 by HB 1001); $2,470 standard deduction, $29 personal credit.',
  fn:function(w){var ti=Math.max(0,w-2470),t;
    if(ti<=5599)t=0;else if(ti<=11199)t=.02*ti-111.98;else if(ti<=15999)t=.03*ti-223.97;else if(ti<=26399)t=.034*ti-287.97;
    else{var lo=.037*ti-367.17,hi=.037*ti-79.9;t=ti<=94700?lo:ti>=97600?hi:lo+(hi-lo)*(ti-94700)/2900}
    return Math.max(0,t-29)},
  approx:true,src:'Arkansas DFA 2026 withholding formula; Arkansas HB 1001 (2026 fiscal session, 3.7% top rate)'},
 {a:'CA',n:'California',b:[[0,.01],[11079,.02],[26264,.04],[41452,.06],[57542,.08],[72724,.093],[371479,.103],[445771,.113],[742953,.123],[1000000,.133]],std:5706,cr:153,
  rule:'1%–12.3% (+1% over $1M) with 2025 FTB brackets; $5,706 standard deduction; $153 personal exemption credit. FTB publishes inflation-indexed 2026 amounts in late December 2026.',
  approx:true,local:'State Disability Insurance (SDI, 1.3% of wages in 2026) is a payroll tax not included here.',src:'CA FTB 2025 Form 540 & tax rate schedules; Tax Foundation 2026'},
 {a:'CO',n:'Colorado',b:[[0,.044]],base:'fedti',
  rule:'Flat 4.4% of federal taxable income (so the $16,100 federal standard deduction applies).',
  local:'Denver, Aurora and a few other cities charge a small monthly occupational privilege tax.',src:'Tax Foundation 2026; Colorado DOR'},
 {a:'CT',n:'Connecticut',b:[[0,.02],[10000,.045],[50000,.055],[100000,.06],[200000,.065],[250000,.069],[500000,.0699]],
  rule:'2%–6.99%; $15,000 personal exemption phased out from $30,000 of income, a personal tax credit for lower incomes, plus the 2% phase-out add-back and "benefit recapture" for higher incomes.',
  fn:function(w){var ex=Math.max(0,15000-1000*steps(w,30000,1000));var t=prog(w-ex,this.b);
    t+=Math.min(250,25*steps(w,56500,5000));
    var rc=0;if(w>105000)rc=Math.min(250,25*steps(w,105000,5000));if(w>200000)rc=250+Math.min(2700,90*steps(w,200000,5000));if(w>500000)rc=2950+Math.min(450,50*steps(w,500000,5000));t+=rc;
    var p=0;if(w<=15000)p=0;else if(w<=18800)p=.75;else if(w<=22300)p=Math.max(.40,.75-.05*steps(w,18800,500));else if(w<=25000)p=.35;else if(w<=26500)p=.35-.05*steps(w,25000,500);else if(w<=31300)p=.15;else if(w<=33300)p=.15-.01*steps(w,31300,500);else if(w<=60000)p=.10;else if(w<=64500)p=.10-.01*steps(w,60000,500);
    if(w<=15000)return 0;return t*(1-p)},
  src:'Tax Foundation 2026; CT DRS withholding tables (Code F) & Conn. Gen. Stat. §12-700, -702, -703'},
 {a:'DE',n:'Delaware',b:[[0,0],[2000,.022],[5000,.039],[10000,.048],[20000,.052],[25000,.0555],[60000,.066]],std:3250,cr:110,
  rule:'0%–6.6%; $3,250 standard deduction; $110 personal credit.',local:'Wilmington levies a 1.25% city wage tax.',src:'Tax Foundation 2026; Delaware Division of Revenue'},
 {a:'DC',n:'District of Columbia',b:[[0,.04],[10000,.06],[40000,.065],[60000,.085],[250000,.0925],[500000,.0975],[1000000,.1075]],std:15000,
  rule:'4%–10.75%; DC decoupled from the One Big Beautiful Bill Act standard deduction and uses its own $15,000 single standard deduction (2025 amount; DC indexes it annually).',
  approx:true,src:'Tax Foundation 2026; DC Act A26-0214 (decoupling from OBBBA standard deduction)'},
 {a:'FL',n:'Florida',none:true,rule:'No state income tax.',src:'Tax Foundation 2026'},
 {a:'GA',n:'Georgia',b:[[0,.0499]],std:12000,
  rule:'Flat 4.99% (cut from 5.19% retroactive to Jan 1, 2026 by HB 463); $12,000 standard deduction.',src:'Georgia HB 463 (signed May 2026); Georgia DOR'},
 {a:'HI',n:'Hawaii',b:[[0,.014],[9600,.032],[14400,.055],[19200,.064],[24000,.068],[36000,.072],[48000,.076],[125000,.079],[175000,.0825],[225000,.09],[275000,.10],[325000,.11]],std:8000,ex:1144,
  rule:'1.4%–11%; standard deduction doubled to $8,000 for 2026 under Act 46 (2024); $1,144 personal exemption.',src:'Hawaii DOTAX Announcement 2024-03 (Act 46, SLH 2024); Tax Foundation 2026'},
 {a:'ID',n:'Idaho',b:[[0,0],[4811,.053]],base:'fedti',
  rule:'0% on the first $4,811, then 5.3%; starts from federal taxable income (federal standard deduction).',src:'Tax Foundation 2026; Idaho State Tax Commission'},
 {a:'IL',n:'Illinois',b:[[0,.0495]],ex:2925,rule:'Flat 4.95%; $2,925 personal exemption allowance.',src:'Tax Foundation 2026; Illinois DOR'},
 {a:'IN',n:'Indiana',b:[[0,.0295]],ex:1000,rule:'Flat 2.95% (2026); $1,000 personal exemption.',local:'All 92 counties add a county income tax (roughly 0.5%–3%), not included.',src:'Tax Foundation 2026; Indiana DOR'},
 {a:'IA',n:'Iowa',b:[[0,.038]],base:'fedti',cr:40,rule:'Flat 3.8% of federal taxable income; $40 personal credit.',local:'Some school districts add an income surtax.',src:'Tax Foundation 2026; Iowa DOR'},
 {a:'KS',n:'Kansas',b:[[0,.052],[23000,.0558]],std:3605,ex:9160,rule:'5.2% / 5.58%; $3,605 standard deduction; $9,160 personal exemption.',src:'Tax Foundation 2026; Kansas DOR'},
 {a:'KY',n:'Kentucky',b:[[0,.035]],std:3360,rule:'Flat 3.5% (2026); $3,360 standard deduction.',local:'Most cities and counties levy occupational license taxes (often 1%–2.5%).',src:'Tax Foundation 2026; Kentucky DOR'},
 {a:'LA',n:'Louisiana',b:[[0,.03]],std:12875,rule:'Flat 3%; $12,875 standard deduction.',src:'Tax Foundation 2026; Louisiana DOR'},
 {a:'ME',n:'Maine',b:[[0,.058],[27400,.0675],[64850,.0715]],ex:5300,
  rule:'5.8% / 6.75% / 7.15%; $15,700 standard deduction (phased out between $102,250 and $177,250 of income); $5,300 personal exemption.',
  fn:function(w){var std=15700*Math.max(0,1-Math.max(0,w-102250)/75000);return prog(w-std-5300,this.b)},
  src:'Maine Revenue Services 2026 rate schedule (rev. May 20, 2026) & 2026 standard deduction phase-out worksheet'},
 {a:'MD',n:'Maryland',b:[[0,.02],[1000,.03],[2000,.04],[3000,.0475],[100000,.05],[125000,.0525],[150000,.055],[250000,.0575],[500000,.0625],[1000000,.065]],std:3350,
  rule:'2%–6.5% state rates; $3,350 standard deduction; $3,200 exemption ($1,600 above $100k, $800 above $125k, none above $150k).',
  fn:function(w){var ex=w<=100000?3200:w<=125000?1600:w<=150000?800:0;return prog(w-3350-ex,this.b)},
  local:'Every Maryland county and Baltimore City adds a local income tax of about 2.25%–3.3% — not included, so real take-home is lower.',src:'Tax Foundation 2026; Comptroller of Maryland'},
 {a:'MA',n:'Massachusetts',b:[[0,.05],[1083150,.09]],ex:4400,rule:'Flat 5% (+4% surtax on very high incomes); $4,400 personal exemption.',local:'Paid Family & Medical Leave payroll contribution not included.',src:'Tax Foundation 2026; Mass. DOR'},
 {a:'MI',n:'Michigan',b:[[0,.0425]],ex:5900,rule:'Flat 4.25%; $5,900 personal exemption.',local:'Detroit (2.4%) and about 20 other cities levy city income taxes.',src:'Tax Foundation 2026; Michigan Treasury'},
 {a:'MN',n:'Minnesota',b:[[0,.0535],[33310,.068],[109430,.0785],[203150,.0985]],std:15300,rule:'5.35%–9.85%; $15,300 standard deduction.',src:'Minnesota DOR 2026 brackets & standard deduction'},
 {a:'MS',n:'Mississippi',b:[[0,0],[10000,.04]],std:2300,ex:6000,rule:'0% on the first $10,000, then 4% (2026); $2,300 standard deduction; $6,000 exemption.',src:'Tax Foundation 2026; Mississippi DOR'},
 {a:'MO',n:'Missouri',b:[[0,0],[1348,.02],[2696,.025],[4044,.03],[5392,.035],[6740,.04],[8088,.045],[9436,.047]],
  rule:'0%–4.7%; federal $16,100 standard deduction; part of federal income tax is deductible (35% → 0% as income rises, max $5,000).',
  fn:function(w,c){var pct=w<=25000?.35:w<=50000?.25:w<=100000?.15:w<=125000?.05:0;var fd=Math.min(5000,c.fedTax*pct);return prog(w-16100-fd,this.b)},
  local:'Kansas City and St. Louis levy a 1% earnings tax.',src:'Tax Foundation 2026; Missouri DOR (RSMo §143.171)'},
 {a:'MT',n:'Montana',b:[[0,.047],[47500,.0565]],base:'fedti',rule:'4.7% / 5.65% of federal taxable income (2026).',src:'Tax Foundation 2026; Montana DOR (HB 337)'},
 {a:'NE',n:'Nebraska',b:[[0,.0246],[4130,.0351],[24760,.0455]],std:8850,cr:176,rule:'2.46% / 3.51% / 4.55% (2026); $8,850 standard deduction; $176 personal credit.',src:'Tax Foundation 2026; Nebraska DOR'},
 {a:'NV',n:'Nevada',none:true,rule:'No state income tax.',src:'Tax Foundation 2026'},
 {a:'NH',n:'New Hampshire',none:true,rule:'No tax on wages (the interest & dividends tax was repealed from 2025).',src:'Tax Foundation 2026'},
 {a:'NJ',n:'New Jersey',b:[[0,.014],[20000,.0175],[35000,.035],[40000,.05525],[75000,.0637],[500000,.0897],[1000000,.1075]],ex:1000,rule:'1.4%–10.75%; no standard deduction; $1,000 personal exemption.',local:'Newark payroll tax and state disability/family leave contributions not included.',src:'Tax Foundation 2026; NJ Division of Taxation'},
 {a:'NM',n:'New Mexico',b:[[0,.015],[5500,.032],[16500,.043],[33500,.047],[66500,.049],[210000,.059]],base:'fedti',rule:'1.5%–5.9%; uses the federal standard deduction.',src:'Tax Foundation 2026; NM Taxation & Revenue'},
 {a:'NY',n:'New York',b:[[0,.039],[8500,.044],[11700,.0515],[13900,.054],[80650,.059],[215400,.0685],[1077550,.0965],[5000000,.103],[25000000,.109]],std:8000,
  rule:'3.9%–10.9% (lower rates cut for 2026); $8,000 standard deduction; above $107,650 of income the benefit of the lower brackets is recaptured.',
  fn:function(w){var ti=Math.max(0,w-8000),b=this.b,t=prog(ti,b);
    if(w>107650&&ti>80650&&ti<=215400){t+=(.059*ti-t)*Math.min(1,(w-107650)/50000)}
    else if(w>215400&&ti>215400&&ti<=1077550){t+=(.059*215400-prog(215400,b))+(.0685-.059)*215400*Math.min(1,(w-215400)/50000)}
    return t},
  local:'New York City (3.078%–3.876%) and Yonkers residents pay additional local income tax — not included.',src:'Tax Foundation 2026; NYS Tax Law §601 (FY2026 budget rate cuts, tax benefit recapture)'},
 {a:'NC',n:'North Carolina',b:[[0,.0399]],std:12750,rule:'Flat 3.99% (2026); $12,750 standard deduction.',src:'Tax Foundation 2026; NCDOR'},
 {a:'ND',n:'North Dakota',b:[[0,0],[48475,.0195],[244825,.025]],base:'fedti',rule:'0% / 1.95% / 2.5% of federal taxable income.',src:'Tax Foundation 2026; ND Office of State Tax Commissioner'},
 {a:'OH',n:'Ohio',
  rule:'No tax on the first $26,050 of Ohio taxable income, then $332 + 2.75% of the excess (flat rate from 2026); personal exemption $2,400 / $2,150 / $1,900 depending on income.',
  fn:function(w){var ex=w<=40000?2400:w<=80000?2150:1900;var ti=w-ex;var t=ti>26050?332+.0275*(ti-26050):0;if(ti<30000)t=Math.max(0,t-20);return t},
  local:'Most Ohio cities levy a municipal income tax (typically 1%–2.5%), and some school districts add more — not included.',src:'Ohio Rev. Code §5747.02(A)(3)(c) & §5747.025; Tax Foundation 2026'},
 {a:'OK',n:'Oklahoma',b:[[0,0],[3750,.025],[4900,.035],[7200,.045]],std:6350,ex:1000,rule:'0%–4.5% (brackets consolidated for 2026); $6,350 standard deduction; $1,000 exemption.',src:'Tax Foundation 2026; Oklahoma HB 2764 (2025)'},
 {a:'OR',n:'Oregon',b:[[0,.0475],[4550,.0675],[11400,.0875],[125000,.099]],std:2910,
  rule:'4.75%–9.9%; $2,910 standard deduction; federal income tax deductible up to $8,500 (phased out from $125,000 to $145,000); $256 personal exemption credit (not above $100,000).',
  fn:function(w,c){var pct=w<125000?1:w<130000?.8:w<135000?.6:w<140000?.4:w<145000?.2:0;var fs=Math.min(8500*pct,c.fedTax);var t=prog(w-fs-2910,this.b);if(w<=100000)t-=256;return Math.max(0,t)},
  local:'Statewide transit tax (0.1%) and Portland-area Metro/Multnomah County taxes not included.',src:'Tax Foundation 2026; Oregon DOR 2026 withholding tables ($8,500 federal tax subtraction), ORS 316.680/316.685'},
 {a:'PA',n:'Pennsylvania',b:[[0,.0307]],rule:'Flat 3.07% on gross compensation; no standard deduction or exemption.',local:'Most municipalities levy an earned income tax (often 1%, Philadelphia 3.74%) — not included.',src:'Tax Foundation 2026; PA DOR'},
 {a:'RI',n:'Rhode Island',b:[[0,.0375],[82050,.0475],[186450,.0599]],std:11200,ex:5250,rule:'3.75% / 4.75% / 5.99%; $11,200 standard deduction; $5,250 exemption.',local:'Temporary Disability Insurance payroll contribution not included.',src:'Tax Foundation 2026; RI Division of Taxation'},
 {a:'SC',n:'South Carolina',
  rule:'New structure from 2026 (H. 4216, signed March 30, 2026): 1.99% up to $30,000 and 5.21% above; new $15,000 SC income-adjusted deduction, phased out between $40,000 and $95,000 of AGI.',
  fn:function(w){var d=15000*Math.min(1,Math.max(0,(95000-w)/55000));var ti=Math.max(0,w-d);return ti<30000?ti*.0199:ti*.0521-966},
  src:'SCDOR "Information about H. 4216"; SC Revenue & Fiscal Affairs fiscal impact statement (H. 4216, signed 3/30/2026)'},
 {a:'SD',n:'South Dakota',none:true,rule:'No state income tax.',src:'Tax Foundation 2026'},
 {a:'TN',n:'Tennessee',none:true,rule:'No state income tax.',src:'Tax Foundation 2026'},
 {a:'TX',n:'Texas',none:true,rule:'No state income tax.',src:'Tax Foundation 2026'},
 {a:'UT',n:'Utah',
  rule:'Flat 4.45% (cut from 4.5% retroactive to Jan 1, 2026 by SB 60) with a taxpayer credit of 6% of the $16,100 federal standard deduction ($966) that phases out at 1.3% of income above $18,213.',
  fn:function(w){var cr=Math.max(0,966-.013*Math.max(0,w-18213));return Math.max(0,.0445*w-cr)},
  approx:true,src:'Utah SB 60 (2026); Utah State Tax Commission (taxpayer tax credit; 2025 phase-out base $18,213)'},
 {a:'VT',n:'Vermont',b:[[0,.0335],[49400,.066],[119700,.076],[249700,.0875]],std:7650,ex:5300,rule:'3.35%–8.75%; $7,650 standard deduction; $5,300 exemption.',src:'Tax Foundation 2026; Vermont Dept. of Taxes'},
 {a:'VA',n:'Virginia',b:[[0,.02],[3000,.03],[5000,.05],[17000,.0575]],std:8750,ex:930,rule:'2%–5.75%; $8,750 standard deduction; $930 personal exemption.',src:'Tax Foundation 2026; Virginia Tax (standard deduction page)'},
 {a:'WA',n:'Washington',none:true,rule:'No income tax on wages (a capital gains tax applies only to large investment gains).',local:'WA Cares (0.58%) and Paid Family & Medical Leave payroll premiums not included.',src:'Tax Foundation 2026'},
 {a:'WV',n:'West Virginia',b:[[0,.0211],[10000,.0281],[25000,.0316],[40000,.0422],[60000,.0458]],ex:2000,rule:'2.11%–4.58% (cut about 5% retroactive to Jan 1, 2026 by SB 392); $2,000 exemption.',src:'W. Va. Code §11-21-4j (taxable years beginning 2026)'},
 {a:'WI',n:'Wisconsin',b:[[0,.035],[15110,.044],[51950,.053],[332720,.0765]],ex:700,
  rule:'3.5%–7.65%; sliding standard deduction up to $13,960 that shrinks by 12% of income above about $19,860; $700 exemption.',
  fn:function(w){var std=Math.max(0,13960-.12*Math.max(0,w-19860));return prog(w-std-700,this.b)},
  approx:true,src:'Tax Foundation 2026; Wisconsin DOR (Wis. Stat. §71.05(22))'},
 {a:'WY',n:'Wyoming',none:true,rule:'No state income tax.',src:'Tax Foundation 2026'}
];
S.forEach(function (s) { s.slug = s.n.toLowerCase().replace(/ of /g, '-of-').replace(/\s+/g, '-'); });

function stateTax(s, w, fed) {
  if (s.none) return 0;
  var c = { fedTax: fed.incomeTax, fedTI: fed.ti };
  var t;
  if (s.fn) t = s.fn.call(s, w, c);
  else {
    var base = s.base === 'fedti' ? fed.ti : w - (s.std || 0) - (s.ex || 0);
    t = prog(base, s.b) - (s.cr || 0);
  }
  return Math.max(0, Math.round(t * 100) / 100);
}

function federal(w) {
  var ti = Math.max(0, w - FED.std);
  var it = fedIncomeTax(ti);
  var ss = Math.min(w, FED.ssWage) * FED.ssRate;
  var med = w * FED.medRate + Math.max(0, w - FED.addMedThreshold) * FED.addMedRate;
  return { gross: w, ti: ti, incomeTax: it, ss: ss, medicare: med, fica: ss + med, marginal: fedMarginal(ti), total: it + ss + med, net: w - it - ss - med };
}

function calc(w, abbr) {
  var f = federal(w);
  var s = S.filter(function (x) { return x.a === abbr; })[0];
  var st = s ? stateTax(s, w, f) : 0;
  return { fed: f, state: s, stateTax: st, net: f.net - st, totalTax: f.total + st };
}
function allStates(w) {
  var f = federal(w);
  return S.map(function (s) { var st = stateTax(s, w, f); return { s: s, stateTax: st, net: f.net - st }; });
}

var API = { asOf: '2026-11-03', taxYear: 2026, FED: FED, STATES: S, federal: federal, stateTax: stateTax, calc: calc, allStates: allStates, fedIncomeTax: fedIncomeTax };
if (typeof module !== 'undefined' && module.exports) module.exports = API; else root.USSalary = API;
})(typeof window !== 'undefined' ? window : this);
