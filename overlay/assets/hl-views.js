/* Hong Life: Table / Bar chart switch for result tables.
   <script src="/assets/hl-views.js" defer data-target="#out" data-lang="en"></script>
   Every money table inside the target gets a two-button switch. Bars are plain HTML,
   so they wrap on small screens instead of being cut off. */
(function () {
  'use strict';
  var me = document.currentScript;
  var SEL = (me && me.getAttribute('data-target')) || '#out';
  var LANG = (me && me.getAttribute('data-lang')) || document.documentElement.lang.slice(0, 2) || 'en';
  var TXT = {
    en: ['Table', 'Bar chart'], ko: ['표', '막대그래프'], es: ['Tabla', 'Gráfico de barras'],
    de: ['Tabelle', 'Balkendiagramm'], fr: ['Tableau', 'Graphique à barres'], ja: ['表', '棒グラフ'],
    pt: ['Tabela', 'Gráfico de barras'], it: ['Tabella', 'Grafico a barre']
  }[LANG] || ['Table', 'Bar chart'];
  var LAST = me && me.getAttribute('data-series') === 'last';
  var KEY = 'hlView';
  var COLORS = ['#a1a1a6', '#1f7a3a', '#0a84ff', '#ff9f0a'];

  function pref() { try { return localStorage.getItem(KEY) || 'table'; } catch (e) { return 'table'; } }
  function setPref(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function money(s) {
    s = (s || '').trim();
    if (!s || s.indexOf('%') >= 0 || !/\d/.test(s)) return null;
    if (/[−-]\s*[$€£¥₩]?\s*\d/.test(s)) return null; // deductions shown as negatives: keep in table only
    var n = parseFloat(s.replace(/[^0-9.]/g, ''));
    return isFinite(n) ? n : null;
  }

  function cellsOf(tr) { return Array.prototype.map.call(tr.children, function (c) { return c.textContent.trim(); }); }

  function build(table) {
    var head = table.querySelector('thead tr');
    var heads = head ? cellsOf(head) : [];
    var rows = Array.prototype.map.call(table.querySelectorAll('tbody tr'), cellsOf);
    if (rows.length < 2) return null;
    var ncol = Math.max.apply(null, rows.map(function (r) { return r.length; }));
    var num = [];
    for (var c = 1; c < ncol; c++) {
      var hits = rows.filter(function (r) { return money(r[c]) !== null; }).length;
      if (hits >= 2) num.push(c);
    }
    if (!num.length) return null;
    // one money column = one series; for "Income | Tax" style tables use the last money column
    var series = !LAST && num.length > 1 && heads.length ? num : [num[num.length - 1]];
    var other = [];
    for (c = 1; c < ncol; c++) if (series.indexOf(c) < 0) other.push(c);
    var data = rows.map(function (r) {
      return { label: r[0], sub: other.map(function (i) { return r[i]; }).filter(Boolean).join(' · '),
               vals: series.map(function (i) { return { v: money(r[i]), t: r[i] }; }) };
    }).filter(function (d) { return d.vals.some(function (x) { return x.v !== null; }); });
    if (data.length < 2 && series.length < 2) return null;
    var max = 0;
    data.forEach(function (d) { d.vals.forEach(function (x) { if (x.v > max) max = x.v; }); });
    if (!max) return null;
    var h = '<div class="hlsw-bars">';
    if (series.length > 1) {
      h += '<div class="hlsw-leg">' + series.map(function (i, k) {
        return '<span><i style="background:' + COLORS[k % 4] + '"></i>' + (heads[i] || '') + '</span>';
      }).join('') + '</div>';
    }
    data.forEach(function (d) {
      h += '<div class="hlsw-row"><div class="hlsw-lab"><b>' + d.label + '</b>' + (d.sub ? '<small>' + d.sub + '</small>' : '') + '</div>';
      d.vals.forEach(function (x, k) {
        var w = x.v ? Math.max(1.5, x.v / max * 100) : 0;
        var col = series.length > 1 ? COLORS[k % 4] : COLORS[1];
        h += '<div class="hlsw-line"><span class="hlsw-trk"><span class="hlsw-bar" style="width:' + w.toFixed(1) + '%;background:' + col + '"></span></span><span class="hlsw-val">' + (x.t || '—') + '</span></div>';
      });
      h += '</div>';
    });
    return h + '</div>';
  }

  var busy = false;
  function apply() {
    var roots = document.querySelectorAll(SEL);
    if (!roots.length) return;
    busy = true;
    Array.prototype.forEach.call(roots, function (root) { Array.prototype.forEach.call(root.querySelectorAll('table'), function (t) {
      if (t.getAttribute('data-hlsw')) return;
      t.setAttribute('data-hlsw', '1');
      var chart = build(t);
      if (!chart) return;
      var box = document.createElement('div');
      box.className = 'hlsw';
      box.innerHTML = '<div class="hlsw-sw" role="group">' +
        '<button type="button" data-v="table">' + TXT[0] + '</button>' +
        '<button type="button" data-v="bars">' + TXT[1] + '</button></div><div class="hlsw-chart"></div>';
      var wrap = t.parentNode && t.parentNode.classList && t.parentNode.classList.contains('tblwrap') ? t.parentNode : t;
      wrap.parentNode.insertBefore(box, wrap);
      box.appendChild(wrap);
      box._tab = wrap;
      box.querySelector('.hlsw-chart').innerHTML = chart;
      show(box, pref());
      box.querySelector('.hlsw-sw').addEventListener('click', function (e) {
        var v = e.target.getAttribute('data-v');
        if (!v) return;
        setPref(v);
        Array.prototype.forEach.call(document.querySelectorAll('.hlsw'), function (b) { show(b, v); });
      });
    }); });
    busy = false;
  }
  function show(box, v) {
    (box._tab || box.querySelector('table')).style.display = v === 'bars' ? 'none' : '';
    box.querySelector('.hlsw-chart').style.display = v === 'bars' ? '' : 'none';
    Array.prototype.forEach.call(box.querySelectorAll('.hlsw-sw button'), function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false');
    });
  }

  var css = document.createElement('style');
  css.textContent =
    '.hlsw{margin:10px 0;width:100%;max-width:100%;min-width:0}' +
    '.hlsw-sw{display:inline-flex;background:#ececf0;border-radius:9px;padding:2px;margin:0 0 8px}' +
    '.hlsw-sw button{border:0;background:transparent;font:inherit;font-size:13px;padding:6px 14px;border-radius:7px;color:#3a3a3c;cursor:pointer;min-height:32px}' +
    '.hlsw-sw button[aria-pressed=true]{background:#fff;color:#1d1d1f;font-weight:600;box-shadow:0 1px 3px rgba(0,0,0,.12)}' +
    '.hlsw-bars{display:grid;grid-template-columns:minmax(0,1fr);gap:12px;padding:4px 0;width:100%}.hlsw-row{min-width:0}' +
    '.hlsw-leg{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12px;color:#6e6e73}' +
    '.hlsw-leg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}' +
    '.hlsw-lab{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 8px;font-size:14px;margin-bottom:4px}' +
    '.hlsw-lab small{color:#6e6e73;font-size:12px}' +
    '.hlsw-line{display:flex!important;flex-wrap:nowrap;align-items:center;gap:8px;margin:3px 0}' +
    '.hlsw-trk{flex:1;min-width:0;height:14px;background:#f2f2f5;border-radius:7px;overflow:hidden}' +
    '.hlsw-bar{display:block;height:100%;border-radius:7px;transition:width .3s}' +
    '.hlsw-line .hlsw-val{display:inline-block!important;flex:none;margin:0!important;font-style:normal;font-size:13px;font-variant-numeric:tabular-nums;white-space:nowrap;min-width:64px;text-align:right}' +
    '@media (prefers-reduced-motion:reduce){.hlsw-bar{transition:none}}';
  document.head.appendChild(css);

  function start() {
    apply();
    if (!window.MutationObserver) return;
    var timer;
    var mo = new MutationObserver(function () {
      if (busy) return;
      clearTimeout(timer);
      timer = setTimeout(apply, 30);
    });
    Array.prototype.forEach.call(document.querySelectorAll(SEL), function (root) { mo.observe(root, { childList: true, subtree: true }); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
