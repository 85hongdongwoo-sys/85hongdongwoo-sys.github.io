/* Honglife Canada salary-after-tax engine — 2026 tax year.
   Sources: CRA "Tax rates and income brackets for individuals – 2026" (modified 2026-06-25); CRA T4127 Payroll Deductions
   Formulas 122nd/123rd editions (Jan & Jul 2026); Revenu Québec "Principal changes for 2026"; B.C. tax reduction 2026 (gov.bc.ca). */
(function(root){
'use strict';
var F={br:[[58523,.14],[117045,.205],[181440,.26],[258482,.29],[Infinity,.33]],cr:.14,bpaMax:16452,bpaMin:14829,bpaLo:181440,bpaHi:258482,cea:1501,abateQC:.165};
var C={ympe:74600,ybe:3500,yampe:85000,cppBase:.0495,cppEnh:.01,cpp2:.04,qppBase:.053,qppEnh:.01,
  ei:.0163,eiQC:.013,eiMax:68900,qpip:.0043,qpipMax:103000};
/* slug, name, abbr, brackets, credit rate (lowest rate), basic personal amount */
var P=[
 {s:'alberta',n:'Alberta',a:'AB',br:[[61200,.08],[154259,.10],[185111,.12],[246813,.13],[370220,.14],[Infinity,.15]],bpa:22769},
 {s:'british-columbia',n:'British Columbia',a:'BC',br:[[50363,.056],[100728,.077],[115648,.105],[140430,.1229],[190405,.147],[265545,.168],[Infinity,.205]],bpa:13216},
 {s:'manitoba',n:'Manitoba',a:'MB',br:[[47000,.108],[100000,.1275],[Infinity,.174]],bpa:15780},
 {s:'new-brunswick',n:'New Brunswick',a:'NB',br:[[52333,.094],[104666,.14],[193861,.16],[Infinity,.195]],bpa:13664},
 {s:'newfoundland-and-labrador',n:'Newfoundland and Labrador',a:'NL',br:[[44678,.087],[89354,.145],[159528,.158],[223340,.178],[285319,.198],[570638,.208],[1141275,.213],[Infinity,.218]],bpa:13094},
 {s:'northwest-territories',n:'Northwest Territories',a:'NT',br:[[53003,.059],[106009,.086],[172346,.122],[Infinity,.1405]],bpa:18198},
 {s:'nova-scotia',n:'Nova Scotia',a:'NS',br:[[30995,.0879],[61991,.1495],[97417,.1667],[157124,.175],[Infinity,.21]],bpa:11932},
 {s:'nunavut',n:'Nunavut',a:'NU',br:[[55801,.04],[111602,.07],[181439,.09],[Infinity,.115]],bpa:19659},
 {s:'ontario',n:'Ontario',a:'ON',br:[[53891,.0505],[107785,.0915],[150000,.1116],[220000,.1216],[Infinity,.1316]],bpa:12989},
 {s:'prince-edward-island',n:'Prince Edward Island',a:'PE',br:[[33928,.095],[65820,.1347],[106890,.166],[142520,.1762],[200000,.19],[Infinity,.20]],bpa:15000},
 {s:'quebec',n:'Quebec',a:'QC',br:[[54345,.14],[108680,.19],[132245,.24],[Infinity,.2575]],bpa:18952},
 {s:'saskatchewan',n:'Saskatchewan',a:'SK',br:[[54532,.105],[155805,.125],[Infinity,.145]],bpa:20381},
 {s:'yukon',n:'Yukon',a:'YT',br:[[58523,.064],[117045,.09],[181440,.109],[500000,.128],[Infinity,.15]],bpa:16452}
];
var BY={};P.forEach(function(p){BY[p.a]=p;BY[p.s]=p});
function bands(x,b){var t=0,lo=0;for(var i=0;i<b.length;i++){var hi=b[i][0],r=b[i][1];if(x>lo)t+=(Math.min(x,hi)-lo)*r;lo=hi}return t}
function marg(x,b){for(var i=0;i<b.length;i++)if(x<=b[i][0])return b[i][1];return b[b.length-1][1]}
function fedBpa(ni){if(ni<=F.bpaLo)return F.bpaMax;if(ni>=F.bpaHi)return F.bpaMin;return F.bpaMax-(F.bpaMax-F.bpaMin)*(ni-F.bpaLo)/(F.bpaHi-F.bpaLo)}
function ohp(ti){if(ti<=20000)return 0;if(ti<=36000)return Math.min(300,(ti-20000)*.06);if(ti<=48000)return Math.min(450,300+(ti-36000)*.06);if(ti<=72000)return Math.min(600,450+(ti-48000)*.25);if(ti<=200000)return Math.min(750,600+(ti-72000)*.25);return Math.min(900,750+(ti-200000)*.25)}
function calc(sal,code){var p=BY[code];var qc=p.a==='QC';
  var pe=Math.max(0,Math.min(sal,C.ympe)-C.ybe);
  var base=pe*(qc?C.qppBase:C.cppBase),enh=pe*(qc?C.qppEnh:C.cppEnh),cpp2=Math.max(0,Math.min(sal,C.yampe)-C.ympe)*C.cpp2;
  var ei=Math.min(sal,C.eiMax)*(qc?C.eiQC:C.ei),qpip=qc?Math.min(sal,C.qpipMax)*C.qpip:0;
  var ni=Math.max(0,sal-enh-cpp2);
  // federal
  var fedBasic=Math.max(0,bands(ni,F.br)-F.cr*(fedBpa(ni)+base+ei+qpip+Math.min(sal,F.cea)));
  var fed=qc?fedBasic*(1-F.abateQC):fedBasic;
  // provincial / territorial
  var cr=p.br[0][1],prov,extra=0,note='';
  if(qc){var dw=Math.min(sal*.06,1450);prov=Math.max(0,bands(Math.max(0,ni-dw),p.br)-cr*p.bpa)}
  else{var bpa=p.bpa;
    if(p.a==='YT')bpa=fedBpa(ni);
    if(p.a==='MB')bpa=ni<=200000?p.bpa:ni>=400000?0:p.bpa*(400000-ni)/200000;
    var cred=bpa+base+ei+(p.a==='YT'?Math.min(sal,F.cea):0);
    prov=Math.max(0,bands(ni,p.br)-cr*cred);
    if(p.a==='ON'){var sur=Math.max(0,prov-5818)*.20+Math.max(0,prov-7446)*.36;prov+=sur;var red=Math.max(0,600-prov);prov=Math.max(0,prov-red);extra=ohp(ni)}
    if(p.a==='BC'){prov=Math.max(0,prov-Math.max(0,690-Math.max(0,ni-25570)*.0356))}
  }
  var cpp=base+enh+cpp2;var total=fed+prov+extra+cpp+ei+qpip;
  return {sal:sal,p:p,ni:ni,fed:fed,prov:prov,ohp:extra,cpp:cpp,ei:ei,qpip:qpip,incomeTax:fed+prov+extra,deductions:total,net:sal-total}}
function marginal(sal,code){var a=calc(sal,code),b=calc(sal+100,code);return 1-(b.net-a.net)/100}
var api={F:F,C:C,P:P,BY:BY,calc:calc,marginal:marginal,bands:bands,marg:marg};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.CASalary=api;
})(this);
