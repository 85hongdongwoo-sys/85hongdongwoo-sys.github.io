/* Honglife Australia salary-after-tax engine — 2026-27 income year (1 Jul 2026 – 30 Jun 2027), resident individual.
   Sources: ATO individual income tax rates; ATO study and training support loans repayment thresholds 2026-27;
   ATO Medicare levy reduction for low-income earners (latest published single threshold $28,011 / $35,013). */
(function(root){
'use strict';
var R={br:[[18200,0],[45000,.15],[135000,.30],[190000,.37],[Infinity,.45]],
  br2526:[[18200,0],[45000,.16],[135000,.30],[190000,.37],[Infinity,.45]],
  med:.02,medLo:28011,medHi:35013,sg:.12,
  help:{th:69528,t2:129717,base2:9028,t3:186050}};
function bands(x,b){var t=0,lo=0;for(var i=0;i<b.length;i++){var hi=b[i][0],r=b[i][1];if(x>lo)t+=(Math.min(x,hi)-lo)*r;lo=hi}return t}
function lito(ti){if(ti<=37500)return 700;if(ti<=45000)return 700-(ti-37500)*.05;if(ti<=66667)return Math.max(0,325-(ti-45000)*.015);return 0}
function medicare(ti){if(ti<=R.medLo)return 0;if(ti<=R.medHi)return (ti-R.medLo)*.10;return ti*R.med}
function help(ri){var h=R.help;if(ri<=h.th)return 0;if(ri<=h.t2)return (ri-h.th)*.15;if(ri<=h.t3)return h.base2+(ri-h.t2)*.17;return ri*.10}
function calc(sal,o){o=o||{};var br=o.y2526?R.br2526:R.br;
  var gross=bands(sal,br),off=Math.min(gross,lito(sal));var tax=gross-off;
  var ml=medicare(sal),hp=o.help?help(sal):0;var net=sal-tax-ml-hp;
  return {sal:sal,grossTax:gross,lito:off,tax:tax,medicare:ml,help:hp,net:net,sup:sal*R.sg}}
function marginal(sal,o){var a=calc(sal,o),b=calc(sal+100,o);return 1-(b.net-a.net)/100}
var api={R:R,calc:calc,marginal:marginal,lito:lito,medicare:medicare,help:help};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.AUSalary=api;
})(this);
