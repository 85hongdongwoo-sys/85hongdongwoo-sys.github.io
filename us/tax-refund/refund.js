/* Hong Life — 2026 federal tax refund estimator engine (tax year 2026, returns filed in 2027).
   Source of truth for /us/tax-refund/ pages AND the live estimator (copied to /us/tax-refund/refund.js by gen.js).
   ESTIMATES ONLY — wages-only W-2 model, not tax advice.  Parameters checked 2026-11-03:
   - Brackets, standard deduction ($16,100 / $32,200 / $24,150), additional 65+/blind ($2,050 unmarried, $1,650 married),
     CTC $2,200 (refundable ACTC up to $1,700), EITC table, investment-income limit $12,200:
       IRS Rev. Proc. 2025-32 (Oct 9, 2025), via KPMG TaxNewsFlash & Current Federal Tax Developments summaries.
   - Withholding tables: IRS Publication 15-T (2026), Annual Percentage Method, STANDARD schedules
       (line 1g $12,900 MFJ / $8,600 other; tables updated for P.L. 119-21).
   - Tips ($25,000), overtime premium ($12,500 / $25,000 MFJ), senior ($6,000 per person, 6% phase-out over $75k/$150k),
     car-loan interest ($10,000, $200 per $1,000 over $100k/$200k): IRS FS-2025-03 (Jul 14, 2025, upd. Jul 25, 2025),
     P.L. 119-21 (One Big Beautiful Bill Act, signed Jul 4, 2025), IRC §§224, 225, 151(d)(5)(C), 163(h)(4). Years 2025–2028.
   - Tips/overtime phase-out rate $100 per $1,000 of MAGI over $150,000 ($300,000 MFJ) — statute.
   - SALT cap 2026 $40,400, phase-down 30% over $505,000 MAGI, floor $10,000 (OBBBA; beancount.io May 17, 2026 summary).
   - Non-itemizer charitable deduction from 2026: $1,000 single / $2,000 MFJ (OBBBA §170(p)) — LABEL: secondary sources.
*/
(function (root) {
'use strict';
var P = {
  year: 2026, asOf: '2026-11-03',
  std: { s: 16100, mfj: 32200, hoh: 24150 },
  addl: { married: 1650, unmarried: 2050 },
  br: {
    s:   [[12400, .10], [50400, .12], [105700, .22], [201775, .24], [256225, .32], [640600, .35], [Infinity, .37]],
    mfj: [[24800, .10], [100800, .12], [211400, .22], [403550, .24], [512450, .32], [768700, .35], [Infinity, .37]],
    hoh: [[17700, .10], [67450, .12], [105700, .22], [201750, .24], [256200, .32], [640600, .35], [Infinity, .37]]
  },
  /* Pub 15-T 2026 STANDARD annual schedules: [at least, base tax, rate] — wages are first reduced by line 1g */
  wh1g: { s: 8600, mfj: 12900, hoh: 8600 },
  wh: {
    s:   [[0, 0, 0], [7500, 0, .10], [19900, 1240, .12], [57900, 5800, .22], [113200, 17966, .24], [209275, 41024, .32], [263725, 58448, .35], [648100, 192979.25, .37]],
    mfj: [[0, 0, 0], [19300, 0, .10], [44100, 2480, .12], [120100, 11600, .22], [230700, 35932, .24], [422850, 82048, .32], [531750, 116896, .35], [788000, 206583.5, .37]],
    hoh: [[0, 0, 0], [15550, 0, .10], [33250, 1770, .12], [83000, 7740, .22], [121250, 16155, .24], [217300, 39207, .32], [271750, 56631, .35], [656150, 191171, .37]]
  },
  supp: .22,                                   // optional flat rate for supplemental wages (bonuses) up to $1M
  ctc: { per: 2200, odc: 500, refMax: 1700, floor: 2500, refRate: .15, ph: { s: 200000, mfj: 400000, hoh: 200000 } },
  eitc: { // kids: [phase-in rate, earned income amount, max credit, phase-out rate]
    k: [[.0765, 8680, 664, .0765], [.34, 13020, 4427, .1598], [.40, 18290, 7316, .2106], [.45, 18290, 8231, .2106]],
    start: { s: [10860, 23890, 23890, 23890], mfj: [18140, 31160, 31160, 31160] }, invest: 12200 },
  tips: { max: 25000, ph: { s: 150000, mfj: 300000 }, rate: .10 },
  ot: { max: { s: 12500, mfj: 25000 }, ph: { s: 150000, mfj: 300000 }, rate: .10 },
  senior: { per: 6000, ph: { s: 75000, mfj: 150000 }, rate: .06 },
  car: { max: 10000, ph: { s: 100000, mfj: 200000 }, rate: .20 },
  salt: { cap: 40400, ph: 505000, rate: .30, floor: 10000 },
  charity: { s: 1000, mfj: 2000 },
  fica: { ss: .062, ssWage: 184500, med: .0145 }
};
var J = function (st) { return st === 'mfj' ? 'mfj' : 's'; };
function bracketTax(ti, st) {
  var b = P.br[st], t = 0, lo = 0; ti = Math.max(0, ti);
  for (var i = 0; i < b.length; i++) { var hi = b[i][0]; if (ti > lo) t += (Math.min(ti, hi) - lo) * b[i][1]; lo = hi; }
  return t;
}
function marginal(ti, st) { var b = P.br[st]; for (var i = 0; i < b.length; i++) if (ti <= b[i][0]) return b[i][1]; return .37; }
/* Pub 15-T annual percentage method, W-4 2020+, Step 2 unchecked, no Step 3/4 entries */
function withholding(wages, st) {
  var a = Math.max(0, wages - P.wh1g[st]), t = P.wh[st], row = t[0];
  for (var i = 0; i < t.length; i++) if (a >= t[i][0]) row = t[i];
  return row[1] + (a - row[0]) * row[2];
}
function phase(max, magi, start, rate) { return Math.max(0, max - Math.max(0, magi - start) * rate); }
function eitc(earned, agi, kids, st) {
  var k = P.eitc.k[Math.min(3, kids)], s0 = P.eitc.start[J(st)][Math.min(3, kids)];
  var c = Math.min(earned * k[0], k[2]);
  return Math.max(0, c - Math.max(0, Math.max(agi, earned) - s0) * k[3]);
}
/* o: {status:'s'|'mfj'|'hoh', wages, kids (under 17), otherDeps, age65 (count of filers 65+), tips, otPremium,
       carInterest, withheld (optional; default = Pub 15-T standard), bonus (portion of wages withheld at 22% flat), noEitc} */
function estimate(o) {
  var st = o.status || 's', w = Math.max(0, +o.wages || 0), kids = Math.max(0, o.kids | 0), deps = Math.max(0, o.otherDeps | 0);
  var n65 = Math.max(0, o.age65 | 0), j = J(st);
  var agi = w, magi = w; // wages-only model: Schedule 1-A deductions do not reduce AGI
  var std = P.std[st] + n65 * (st === 'mfj' ? P.addl.married : P.addl.unmarried);
  var dTips = Math.min(phase(P.tips.max, magi, P.tips.ph[j], P.tips.rate), Math.max(0, +o.tips || 0));
  var dOt = Math.min(phase(P.ot.max[j], magi, P.ot.ph[j], P.ot.rate), Math.max(0, +o.otPremium || 0));
  var dSen = n65 ? phase(P.senior.per * n65, magi, P.senior.ph[j], P.senior.rate) : 0;
  var dCar = Math.min(phase(P.car.max, magi, P.car.ph[j], P.car.rate), Math.max(0, +o.carInterest || 0));
  var ti = Math.max(0, agi - std - dTips - dOt - dSen - dCar);
  var tax = bracketTax(ti, st);
  var ctcMax = Math.max(0, kids * P.ctc.per + deps * P.ctc.odc - Math.ceil(Math.max(0, magi - P.ctc.ph[st]) / 1000) * 50);
  var nonref = Math.min(tax, ctcMax);
  var ctcKidsLeft = Math.max(0, Math.min(ctcMax, kids * P.ctc.per) - nonref);
  var actc = Math.min(ctcKidsLeft, kids * P.ctc.refMax, Math.max(0, w - P.ctc.floor) * P.ctc.refRate);
  var ei = o.noEitc ? 0 : eitc(w, agi, kids, st);
  var bonus = Math.min(w, Math.max(0, +o.bonus || 0));
  var withheld = o.withheld != null && o.withheld !== '' ? +o.withheld : withholding(w - bonus, st) + bonus * P.supp;
  var liability = tax - nonref;
  var refund = withheld - liability + actc + ei;
  return { status: st, wages: w, agi: agi, std: std, dTips: dTips, dOt: dOt, dSen: dSen, dCar: dCar, ti: ti, tax: tax,
    ctc: nonref, actc: actc, eitc: ei, liability: liability, withheld: withheld, refund: refund,
    marginal: marginal(ti, st), effective: w ? liability / w : 0 };
}
var api = { P: P, bracketTax: bracketTax, marginal: marginal, withholding: withholding, eitc: eitc, estimate: estimate, phase: phase };
if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.TaxRefund = api;
})(this);
