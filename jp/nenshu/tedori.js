/* 年収→手取り 計算エンジン（2026年分・東京都・協会けんぽ）
   出典: 協会けんぽ 令和8年度保険料率（東京 9.85%、介護 1.62%、子ども・子育て支援金 0.23%）、日本年金機構（厚生年金 18.3%）、
   厚生労働省（雇用保険 令和8年度 労働者負担 5/1000）、国税庁・財務省（令和8年分 基礎控除・給与所得控除の特例）、総務省（ふるさと納税 控除上限の計算式）。
   概算であり、実際の源泉徴収・年末調整・住民税決定額とは異なる場合があります。 */
(function (root) {
  'use strict';
  var RATE = { kenpo: 0.0985, kaigo: 0.0162, kodomo: 0.0023, nenkin: 0.183, koyo: 0.005 };
  // 健康保険 標準報酬月額（等級1〜50）: [標準報酬, 報酬月額の上限(未満)]
  var G = [[58e3,63e3],[68e3,73e3],[78e3,83e3],[88e3,93e3],[98e3,101e3],[104e3,107e3],[110e3,114e3],[118e3,122e3],[126e3,130e3],[134e3,138e3],
    [142e3,146e3],[150e3,155e3],[160e3,165e3],[170e3,175e3],[180e3,185e3],[190e3,195e3],[200e3,210e3],[220e3,230e3],[240e3,250e3],[260e3,270e3],
    [280e3,290e3],[300e3,310e3],[320e3,330e3],[340e3,350e3],[360e3,370e3],[380e3,395e3],[410e3,425e3],[440e3,455e3],[470e3,485e3],[500e3,515e3],
    [530e3,545e3],[560e3,575e3],[590e3,605e3],[620e3,635e3],[650e3,665e3],[680e3,695e3],[710e3,730e3],[750e3,770e3],[790e3,810e3],[830e3,855e3],
    [880e3,905e3],[930e3,955e3],[980e3,1005e3],[1030e3,1055e3],[1090e3,1115e3],[1150e3,1175e3],[1210e3,1235e3],[1270e3,1295e3],[1330e3,1355e3],[1390e3,Infinity]];
  function std(m) { for (var i = 0; i < G.length; i++) if (m < G[i][1]) return G[i][0]; return 1390e3; }
  function pstd(m) { return Math.min(Math.max(std(m), 88e3), 650e3); }
  // 被保険者負担分: 50銭以下切り捨て・50銭超切り上げ
  function half(x) { return Math.ceil(x - 0.5 - 1e-9); }
  function fl(x, u) { return Math.floor(x / u + 1e-9) * u; }

  function kyuyoKojo(I) {
    var A = I < 6.6e6 ? fl(I, 4000) : I;
    if (I < 1.9e6 || A <= 2.2e6) return Math.min(I, Math.max(740e3, Math.floor(A * 0.3) + 80e3));
    if (A <= 3.6e6) return Math.floor(A * 0.3) + 80e3;
    if (A <= 6.6e6) return Math.floor(A * 0.2) + 440e3;
    if (I <= 8.5e6) return Math.floor(I * 0.1) + 1100e3;
    return 1950e3;
  }
  function kyuyoShotoku(I) {
    if (I < 2.191e6) return Math.max(0, I - 740e3); // 令和8年分の特例: 収入−74万円
    var A = I < 6.6e6 ? fl(I, 4000) : I;
    return Math.max(0, A - kyuyoKojo(I));
  }
  // 所得税の基礎控除（令和8・9年分）
  function kisoIT(s) {
    if (s <= 4.89e6) return 1040e3; if (s <= 6.55e6) return 670e3; if (s <= 23.5e6) return 620e3;
    if (s <= 24e6) return 480e3; if (s <= 24.5e6) return 320e3; if (s <= 25e6) return 160e3; return 0;
  }
  function kisoRT(s) { if (s <= 24e6) return 430e3; if (s <= 24.5e6) return 290e3; if (s <= 25e6) return 150e3; return 0; }
  var BR = [[1.95e6, .05, 0], [3.3e6, .10, 97500], [6.95e6, .20, 427500], [9e6, .23, 636000], [18e6, .33, 1536000], [40e6, .40, 2796000], [Infinity, .45, 4796000]];
  function brk(t) { for (var i = 0; i < BR.length; i++) if (t <= BR[i][0]) return BR[i]; }
  function itax(t) { if (t <= 0) return 0; var b = brk(t); return Math.floor(t * b[1] - b[2]); }

  /* opt: {age40:bool, bonusMonths:number(年間賞与の月数, 0=なし), spouse:bool(配偶者控除の対象), dep:number(16〜18歳等の一般扶養), tok:number(19〜22歳の特定扶養), ideco:number(年額)} */
  function calc(I, opt) {
    opt = opt || {};
    var bm = opt.bonusMonths || 0, n = 12 + bm;
    var monthly = Math.round(I / n), bonusTotal = I - monthly * 12;
    var bonusEach = bm > 0 ? bonusTotal / 2 : 0;
    var s = std(monthly), ps = pstd(monthly);
    var m = { kenpo: half(s * RATE.kenpo / 2), kodomo: half(s * RATE.kodomo / 2), kaigo: opt.age40 ? half(s * RATE.kaigo / 2) : 0,
      nenkin: half(ps * RATE.nenkin / 2), koyo: half(monthly * RATE.koyo) };
    var b = { kenpo: 0, kodomo: 0, kaigo: 0, nenkin: 0, koyo: 0 };
    var bEach = { kenpo: 0, kodomo: 0, kaigo: 0, nenkin: 0, koyo: 0 };
    if (bm > 0) {
      var hb = fl(bonusEach, 1000), cum = 0;
      for (var k = 0; k < 2; k++) {
        var hk = Math.max(0, Math.min(hb, 5.73e6 - cum)); cum += hk;
        var pk = Math.min(hb, 1.5e6);
        var e = { kenpo: half(hk * RATE.kenpo / 2), kodomo: half(hk * RATE.kodomo / 2), kaigo: opt.age40 ? half(hk * RATE.kaigo / 2) : 0,
          nenkin: half(pk * RATE.nenkin / 2), koyo: half(bonusEach * RATE.koyo) };
        for (var key in e) { b[key] += e[key]; if (k === 0) bEach[key] = e[key]; }
      }
    }
    var sh = {}; for (var kk in m) sh[kk] = m[kk] * 12 + b[kk];
    var shakai = sh.kenpo + sh.kodomo + sh.kaigo + sh.nenkin + sh.koyo;
    var ideco = opt.ideco || 0;
    var gs = kyuyoShotoku(I);
    var chosei = 0; // 所得金額調整控除（23歳未満の扶養親族がいる場合）
    if (I > 8.5e6 && ((opt.dep || 0) + (opt.tok || 0)) > 0) chosei = Math.ceil((Math.min(I, 10e6) - 8.5e6) * 0.1);
    var sotoku = Math.max(0, gs - chosei);
    // 配偶者控除・扶養控除
    var spIT = 0, spRT = 0, spDiff = 0;
    if (opt.spouse) {
      if (sotoku <= 9e6) { spIT = 380e3; spRT = 330e3; spDiff = 50e3; }
      else if (sotoku <= 9.5e6) { spIT = 260e3; spRT = 220e3; spDiff = 40e3; }
      else if (sotoku <= 10e6) { spIT = 130e3; spRT = 110e3; spDiff = 20e3; }
    }
    var dep = opt.dep || 0, tok = opt.tok || 0;
    var depIT = dep * 380e3 + tok * 630e3, depRT = dep * 330e3 + tok * 450e3, depDiff = dep * 50e3 + tok * 180e3;
    var kIT = kisoIT(sotoku), kRT = kisoRT(sotoku);
    var taxableIT = Math.max(0, fl(sotoku - shakai - ideco - kIT - spIT - depIT, 1000));
    var it0 = itax(taxableIT);
    var shotokuzei = fl(it0 * 1.021, 100);
    // 住民税（東京23区: 特別区民税6%＋都民税4%、均等割 区3,000＋都1,000＋森林環境税1,000）
    var nin = 1 + (opt.spouse ? 1 : 0) + dep + tok;
    var hikaKin = nin === 1 ? 450e3 : 350e3 * nin + 310e3;
    var hikaSho = nin === 1 ? 450e3 : 350e3 * nin + 420e3;
    var taxableRT = Math.max(0, fl(sotoku - shakai - ideco - kRT - spRT - depRT, 1000));
    var jinteki = (kRT > 0 ? 50e3 : 0) + spDiff + depDiff, adj = 0;
    if (sotoku <= 25e6 && taxableRT > 0) {
      if (taxableRT <= 2e6) adj = Math.min(jinteki, taxableRT) * 0.05;
      else adj = Math.max((jinteki - (taxableRT - 2e6)) * 0.05, 2500);
    }
    var shotokuwari = sotoku <= hikaSho ? 0 : Math.max(0, fl(taxableRT * 0.1 - adj, 100));
    var kintou = sotoku <= hikaKin ? 0 : 5000;
    var juminzei = shotokuwari + kintou;
    var tax = shotokuzei + juminzei;
    var net = I - shakai - tax - ideco;
    // ふるさと納税 控除上限（総務省の計算式）: 所得割×20% ÷ (90% − 所得税率×1.021) + 2,000
    var X = taxableRT - jinteki, rX = X < 0 ? 0 : brk(X)[1];
    var furusato = shotokuwari > 0 ? Math.floor(shotokuwari * 0.2 / (0.9 - rX * 1.021) + 2000) : 0;
    var rIT = taxableIT > 0 ? brk(taxableIT)[1] : 0;
    var r = {
      I: I, opt: opt, monthly: monthly, bonusEach: bonusEach, bonusTotal: bonusTotal, std: s, pstd: ps,
      m: m, mSum: m.kenpo + m.kodomo + m.kaigo + m.nenkin + m.koyo, b: b, bEach: bEach, sh: sh, shakai: shakai,
      kyuyoKojo: I - gs, kyuyoShotoku: gs, chosei: chosei, kisoIT: kIT, kisoRT: kRT, spIT: spIT, depIT: depIT,
      taxableIT: taxableIT, shotokuzei: shotokuzei, taxableRT: taxableRT, chosei2: adj, shotokuwari: shotokuwari, kintou: kintou,
      juminzei: juminzei, tax: tax, ideco: ideco, net: net, netM: net / 12, rate: net / I,
      rIT: rIT, rX: rX, furusato: furusato
    };
    // 賞与ありの場合の内訳（所得税は年額を支給額で按分、住民税は12等分）
    if (bm > 0) {
      var share = monthly * 12 / I;
      r.netMonthly = monthly - r.mSum - shotokuzei * share / 12 - juminzei / 12;
      var bs = bEach.kenpo + bEach.kodomo + bEach.kaigo + bEach.nenkin + bEach.koyo;
      r.netBonus = bonusEach - bs - shotokuzei * (1 - share) / 2;
      r.bonusShakai = bs;
    }
    return r;
  }
  var api = { calc: calc, RATE: RATE, kyuyoShotoku: kyuyoShotoku, kisoIT: kisoIT, itax: itax };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.Tedori = api;
})(this);
