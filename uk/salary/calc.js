/* Honglife UK salary-after-tax engine — tax year 2026/27 (6 Apr 2026 – 5 Apr 2027).
   Sources: GOV.UK "Rates and thresholds for employers 2026 to 2027"; gov.scot Scottish income tax 2026-27. */
(function(root){
'use strict';
var R={pa:12570,taper:100000,
  ruk:[[37700,.20],[125140,.40],[Infinity,.45]],
  scot:[[3967,.19],[16956,.20],[31092,.21],[62430,.42],[125140,.45],[Infinity,.48]],
  pt:12570,uel:50270,ni:[.08,.02],plan2:[29385,.09]};
function bands(x,b){var t=0,lo=0;for(var i=0;i<b.length;i++){var hi=b[i][0],r=b[i][1];if(x>lo)t+=(Math.min(x,hi)-lo)*r;lo=hi}return t}
function allowance(ani){return Math.max(0,R.pa-Math.floor(Math.max(0,ani-R.taper)/2))}
/* opts: scot (bool), plan2 (bool), pen (fraction e.g. .05), sac (bool: salary sacrifice) */
function calc(gross,o){o=o||{};var pen=gross*(o.pen||0);var sac=!!o.sac;
  var taxable=gross-pen;            // net pay arrangement & salary sacrifice both cut taxable pay
  var niPay=sac?gross-pen:gross;     // only salary sacrifice cuts NI / student-loan pay
  var pa=allowance(taxable);var ti=Math.max(0,taxable-pa);
  var tax=bands(ti,o.scot?R.scot:R.ruk);
  var ni=Math.max(0,Math.min(niPay,R.uel)-R.pt)*R.ni[0]+Math.max(0,niPay-R.uel)*R.ni[1];
  var sl=o.plan2?Math.floor(Math.max(0,niPay-R.plan2[0])*R.plan2[1]):0;
  var net=gross-pen-tax-ni-sl;
  return {gross:gross,pension:pen,pa:pa,taxable:ti,tax:tax,ni:ni,sl:sl,net:net}}
/* marginal rate on next £100 of salary (tax + NI + loan) */
function marginal(gross,o){var a=calc(gross,o),b=calc(gross+100,o);return 1-(b.net-a.net)/100}
var api={R:R,calc:calc,marginal:marginal,allowance:allowance};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.UKSalary=api;
})(this);
