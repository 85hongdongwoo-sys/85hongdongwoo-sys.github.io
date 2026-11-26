/* Arttrip Editor — layered page editor for calendars, art papers and cards.
   Units are millimetres. One renderer draws the screen and the print export, so what you see is what prints. */
(function () {
  'use strict';
  var app = document.getElementById('ed');
  var ko = (app.dataset.lang || 'en') === 'ko';
  var T = function (en, k) { return ko ? k : en; };
  var SIZES = { A4: [210, 297], Letter: [215.9, 279.4], A5: [148, 210], '5x7': [127, 177.8], Square: [203.2, 203.2], 'A4 landscape': [297, 210], 'Letter landscape': [279.4, 215.9], 'A3 poster': [297, 420], 'A2 poster': [420, 594], '11x14 poster': [279.4, 355.6], '16x20 poster': [406.4, 508], '18x24 poster': [457.2, 609.6], '24x36 poster': [609.6, 914.4] };
  // Big posters: browsers cap canvas area (~16.7 MP on Safari), and wall prints read fine at 150-200 dpi.
  function fullDpi() { var a = (doc.w / 25.4) * (doc.h / 25.4); return Math.max(100, Math.min(300, Math.floor(Math.sqrt(16e6 / a) / 10) * 10)); }
  var FONTS = [
    ['Lora', 'serif'], ['Playfair Display', 'serif'], ['Cormorant Garamond', 'serif'], ['DM Serif Display', 'serif'], ['Libre Baskerville', 'serif'],
    ['Special Elite', 'monospace'], ['Courier Prime', 'monospace'], ['Caveat', 'cursive'], ['Dancing Script', 'cursive'], ['Homemade Apple', 'cursive'],
    ['Amatic SC', 'cursive'], ['Josefin Sans', 'sans-serif'], ['Inter', 'sans-serif'], ['Bebas Neue', 'sans-serif'],
    ['Noto Serif KR', 'serif'], ['Gowun Batang', 'serif'], ['Noto Sans KR', 'sans-serif'], ['Nanum Pen Script', 'cursive'], ['Gaegu', 'cursive']
  ];
  var MONTHS = { en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ko: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'] };
  var WD = { en: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], ko: ['일', '월', '화', '수', '목', '금', '토'] };
  var PAPERS = { cream: '#f4ecdc', ivory: '#faf6ee', kraft: '#c8a77a', parchment: '#eadbbd', sage: '#d9dfcf', blush: '#f1ddd6', sky: '#dbe4ea', ink: '#22252b', white: '#ffffff' };

  // ---------- state ----------
  var doc = null, pageIx = 0, sel = null, zoom = 1, fit = 1, hist = [], fut = [], LIB = [], unlocked = false, clip = null;
  var uid = function () { return Math.random().toString(36).slice(2, 9); };
  var page = function () { return doc.pages[pageIx]; };
  var item = function (id) { var a = page().items; for (var i = 0; i < a.length; i++) if (a[i].id === id) return a[i]; return null; };
  var clone = function (o) { return JSON.parse(JSON.stringify(o)); };
  function newDoc(size) { var s = SIZES[size] || SIZES.A4; return { v: 1, title: T('Untitled', '제목 없음'), size: size || 'A4', w: s[0], h: s[1], pages: [blankPage()] }; }
  function blankPage() { return { id: uid(), bg: { kind: 'aged', color: PAPERS.cream, grain: 0.5, stain: 0.35, vignette: 0.45, pattern: 'none' }, items: [] }; }

  // ---------- history ----------
  var lastSnap = '';
  function commit() { var s = JSON.stringify(doc); if (s === lastSnap) return; hist.push(lastSnap); if (hist.length > 120) hist.shift(); fut = []; lastSnap = s; autosave(); }
  function undo() { if (!hist.length) return; fut.push(lastSnap); lastSnap = hist.pop(); doc = JSON.parse(lastSnap); if (pageIx >= doc.pages.length) pageIx = doc.pages.length - 1; sel = null; refresh(); autosave(); }
  function redo() { if (!fut.length) return; hist.push(lastSnap); lastSnap = fut.pop(); doc = JSON.parse(lastSnap); sel = null; refresh(); autosave(); }

  // ---------- images ----------
  var IMG = {}, FILT = {};
  function img(src) {
    if (!src) return null;
    var c = IMG[src]; if (c) return c.ok ? c.el : null;
    c = IMG[src] = { el: new Image(), ok: false }; c.el.crossOrigin = 'anonymous';
    c.el.onload = function () { c.ok = true; draw(); thumbs(); }; c.el.onerror = function () { c.bad = true; };
    c.el.src = src; return null;
  }
  function filtered(src, f, maxPx) {
    var el = img(src); if (!el) return null;
    var key = src + '|' + JSON.stringify(f || {}) + '|' + maxPx; if (FILT[key]) return FILT[key];
    var s = Math.min(1, maxPx / Math.max(el.naturalWidth, el.naturalHeight)), w = Math.max(1, Math.round(el.naturalWidth * s)), h = Math.max(1, Math.round(el.naturalHeight * s));
    var c = document.createElement('canvas'); c.width = w; c.height = h; var x = c.getContext('2d'); x.drawImage(el, 0, 0, w, h);
    if (f && (f.sepia || f.gray || f.bright || f.contrast || f.sat || f.warm || f.fade)) {
      var d = x.getImageData(0, 0, w, h), p = d.data, br = 1 + (f.bright || 0), ct = 1 + (f.contrast || 0), st = 1 + (f.sat || 0), sp = f.sepia || 0, gr = f.gray || 0, wm = f.warm || 0, fd = f.fade || 0;
      for (var i = 0; i < p.length; i += 4) {
        var r = p[i], g = p[i + 1], b = p[i + 2];
        r = (r - 128) * ct + 128; g = (g - 128) * ct + 128; b = (b - 128) * ct + 128;
        r *= br; g *= br; b *= br;
        var l = 0.299 * r + 0.587 * g + 0.114 * b; r = l + (r - l) * st * (1 - gr); g = l + (g - l) * st * (1 - gr); b = l + (b - l) * st * (1 - gr);
        if (sp) { var sr = 0.393 * r + 0.769 * g + 0.189 * b, sg = 0.349 * r + 0.686 * g + 0.168 * b, sb = 0.272 * r + 0.534 * g + 0.131 * b; r += (sr - r) * sp; g += (sg - g) * sp; b += (sb - b) * sp; }
        if (wm) { r += 18 * wm; b -= 18 * wm; }
        if (fd) { r += (235 - r) * fd * 0.5; g += (228 - g) * fd * 0.5; b += (212 - b) * fd * 0.5; }
        p[i] = r; p[i + 1] = g; p[i + 2] = b;
      }
      x.putImageData(d, 0, 0);
    }
    var keys = Object.keys(FILT); if (keys.length > 60) delete FILT[keys[0]];
    return FILT[key] = c;
  }
  var NOISE = null;
  function noise() {
    if (NOISE) return NOISE; var c = document.createElement('canvas'); c.width = c.height = 256; var x = c.getContext('2d'), d = x.createImageData(256, 256);
    for (var i = 0; i < d.data.length; i += 4) { var v = 128 + (Math.random() - 0.5) * 90; d.data[i] = v; d.data[i + 1] = v * 0.97; d.data[i + 2] = v * 0.9; d.data[i + 3] = 255; }
    x.putImageData(d, 0, 0); return NOISE = c;
  }
  function rnd(seed) { var s = seed % 2147483647; if (s <= 0) s += 2147483646; return function () { return (s = s * 16807 % 2147483647) / 2147483647; }; }
  function hash(str) { var h = 7; for (var i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) | 0; return Math.abs(h) + 1; }

  // ---------- renderer (mm space) ----------
  function shade(hex, k) { var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255; var f = function (v) { return Math.max(0, Math.min(255, Math.round(k < 0 ? v * (1 + k) : v + (255 - v) * k))); }; return 'rgb(' + f(r) + ',' + f(g) + ',' + f(b) + ')'; }
  function drawBg(x, pg, W, H, s) {
    var bg = pg.bg || {}; x.fillStyle = bg.color || '#fff'; x.fillRect(0, 0, W, H);
    if (bg.kind === 'image' && bg.src) { var el = filtered(bg.src, bg.filter, 2600 * s / 4 > 600 ? 2600 : 1200); if (el) coverDraw(x, el, 0, 0, W, H, { z: 1, ox: 0, oy: 0 }); }
    if (bg.kind === 'aged' || bg.kind === 'image') {
      var R = rnd(hash(pg.id || 'p'));
      if (bg.stain) for (var i = 0; i < 7; i++) { var cx = R() * W, cy = R() * H, r = (0.08 + R() * 0.22) * Math.max(W, H), g = x.createRadialGradient(cx, cy, r * 0.2, cx, cy, r); g.addColorStop(0, 'rgba(150,105,50,' + (0.10 * bg.stain) + ')'); g.addColorStop(0.75, 'rgba(150,105,50,' + (0.05 * bg.stain) + ')'); g.addColorStop(1, 'rgba(150,105,50,0)'); x.fillStyle = g; x.fillRect(0, 0, W, H); }
      if (bg.grain) { x.save(); x.globalAlpha = 0.18 * bg.grain; x.globalCompositeOperation = 'multiply'; var pat = x.createPattern(noise(), 'repeat'); var m = 1 / s; x.scale(m, m); x.fillStyle = pat; x.fillRect(0, 0, W * s, H * s); x.restore(); }
      if (bg.vignette) { var v = x.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.35, W / 2, H / 2, Math.hypot(W, H) * 0.62); v.addColorStop(0, 'rgba(90,60,30,0)'); v.addColorStop(1, 'rgba(90,60,30,' + (0.38 * bg.vignette) + ')'); x.fillStyle = v; x.fillRect(0, 0, W, H); }
    }
    var pt = bg.pattern; if (pt && pt !== 'none') {
      x.save(); x.strokeStyle = bg.lineColor || 'rgba(110,90,70,0.28)'; x.fillStyle = bg.lineColor || 'rgba(110,90,70,0.35)'; x.lineWidth = 0.2; var st = bg.step || 7;
      if (pt === 'lines') for (var y = st * 3; y < H - 8; y += st) { x.beginPath(); x.moveTo(12, y); x.lineTo(W - 12, y); x.stroke(); }
      if (pt === 'grid') { for (var gx = 0; gx <= W; gx += st / 1.4) { x.beginPath(); x.moveTo(gx, 0); x.lineTo(gx, H); x.stroke(); } for (var gy = 0; gy <= H; gy += st / 1.4) { x.beginPath(); x.moveTo(0, gy); x.lineTo(W, gy); x.stroke(); } }
      if (pt === 'dots') for (var dy = st / 1.4; dy < H; dy += st / 1.4) for (var dx = st / 1.4; dx < W; dx += st / 1.4) { x.beginPath(); x.arc(dx, dy, 0.28, 0, 7); x.fill(); }
      x.restore();
    }
  }
  function coverDraw(x, el, X, Y, W, H, c) {
    var iw = el.width || el.naturalWidth, ih = el.height || el.naturalHeight, k = Math.max(W / iw, H / ih) * (c.z || 1), dw = iw * k, dh = ih * k;
    var ox = (dw - W) / 2 * (c.ox || 0), oy = (dh - H) / 2 * (c.oy || 0);
    x.drawImage(el, X + (W - dw) / 2 - ox, Y + (H - dh) / 2 - oy, dw, dh);
  }
  function maskPath(x, m, w, h, r) {
    x.beginPath();
    if (m === 'ellipse') { x.ellipse(w / 2, h / 2, w / 2, h / 2, 0, 0, 7); return; }
    if (m === 'arch') { var rr = w / 2; x.moveTo(0, h); x.lineTo(0, rr); x.arc(rr, rr, rr, Math.PI, 0); x.lineTo(w, h); x.closePath(); return; }
    if (m === 'stamp') { var n = Math.max(6, Math.round(w / 3.2)), rad = w / n / 2, ny = Math.max(6, Math.round(h / (rad * 2))), ry = h / ny / 2; x.moveTo(0, 0); for (var i = 0; i < n; i++) x.arc(rad * (2 * i + 1), 0, rad, Math.PI, 0, true); for (var j = 0; j < ny; j++) x.arc(w, ry * (2 * j + 1), ry, -Math.PI / 2, Math.PI / 2, true); for (var k2 = n - 1; k2 >= 0; k2--) x.arc(rad * (2 * k2 + 1), h, rad, 0, Math.PI, true); for (var l = ny - 1; l >= 0; l--) x.arc(0, ry * (2 * l + 1), ry, Math.PI / 2, -Math.PI / 2, true); x.closePath(); return; }
    if (m === 'ticket') { var q = Math.min(w, h) * 0.12; x.moveTo(q, 0); x.lineTo(w - q, 0); x.arc(w, 0, q, Math.PI, Math.PI / 2, true); x.lineTo(w, h - q); x.arc(w, h, q, -Math.PI / 2, Math.PI, true); x.lineTo(q, h); x.arc(0, h, q, 0, -Math.PI / 2, true); x.lineTo(0, q); x.arc(0, 0, q, Math.PI / 2, 0, true); x.closePath(); return; }
    if (m === 'label') { var c2 = Math.min(w, h) * 0.18; x.moveTo(c2, 0); x.lineTo(w - c2, 0); x.lineTo(w, c2); x.lineTo(w, h - c2); x.lineTo(w - c2, h); x.lineTo(c2, h); x.lineTo(0, h - c2); x.lineTo(0, c2); x.closePath(); return; }
    if (m === 'tag') { var t = Math.min(w * 0.3, h * 0.5); x.moveTo(t, 0); x.lineTo(w, 0); x.lineTo(w, h); x.lineTo(t, h); x.lineTo(0, h / 2); x.closePath(); return; }
    if (m === 'torn') { var R2 = rnd(hash('t' + w + h)), st2 = 2.2; x.moveTo(0, 0); for (var a = 0; a <= w; a += st2) x.lineTo(a, (R2() - 0.5) * 1.6); for (var b = 0; b <= h; b += st2) x.lineTo(w + (R2() - 0.5) * 1.6, b); for (var c3 = w; c3 >= 0; c3 -= st2) x.lineTo(c3, h + (R2() - 0.5) * 1.6); for (var d2 = h; d2 >= 0; d2 -= st2) x.lineTo((R2() - 0.5) * 1.6, d2); x.closePath(); return; }
    if (r) { x.roundRect ? x.roundRect(0, 0, w, h, r) : x.rect(0, 0, w, h); return; }
    x.rect(0, 0, w, h);
  }
  function wrap(x, text, maxW) {
    var out = []; String(text).split('\n').forEach(function (para) {
      var words = para.split(/(\s+)/), line = '';
      if (/[ㄱ-힝]/.test(para) && words.length < 3) words = para.split('');
      words.forEach(function (w) { var t = line + w; if (x.measureText(t).width > maxW && line.trim()) { out.push(line.replace(/\s+$/, '')); line = w.replace(/^\s+/, ''); } else line = t; });
      out.push(line);
    }); return out;
  }
  function fontStr(it, px) { var f = FONTS.find(function (q) { return q[0] === it.font; }); return (it.italic ? 'italic ' : '') + (it.weight || 400) + ' ' + px + 'px "' + (it.font || 'Lora') + '", ' + (f ? f[1] : 'serif'); }
  var PT = 0.3528; // 1pt in mm
  function textHeight(x, it) { x.font = fontStr(it, it.size * PT); if (it.ls) x.letterSpacing = (it.ls * it.size * PT) + 'px'; var lines = wrap(x, it.upper ? it.text.toUpperCase() : it.text, it.w); x.letterSpacing = '0px'; return lines.length * it.size * PT * (it.lh || 1.25); }
  function drawItem(x, it, s, exporting) {
    if (it.hidden) return;
    x.save(); x.translate(it.x + it.w / 2, it.y + it.h / 2); x.rotate((it.rot || 0) * Math.PI / 180); x.translate(-it.w / 2, -it.h / 2); x.globalAlpha = it.opacity == null ? 1 : it.opacity;
    if (it.blend) x.globalCompositeOperation = it.blend;
    if (it.shadow) { x.shadowColor = 'rgba(40,25,10,' + (0.35 * it.shadow) + ')'; x.shadowBlur = 3 * it.shadow * s; x.shadowOffsetX = 0.6 * it.shadow * s; x.shadowOffsetY = 1.1 * it.shadow * s; }
    var t = it.type;
    if (t === 'image' || t === 'tape') {
      maskPath(x, it.mask, it.w, it.h, it.radius);
      if (it.shadow) { x.fillStyle = '#fff'; x.fill(); x.shadowColor = 'transparent'; }
      x.save(); x.clip();
      var maxPx = exporting ? 3200 : 1400, src = exporting && it.hi ? it.hi : it.src, el = filtered(src, it.filter, maxPx) || (exporting && it.hi ? filtered(it.src, it.filter, maxPx) : null);
      if (el) coverDraw(x, el, 0, 0, it.w, it.h, it.crop || {}); else { x.fillStyle = '#e7dfd0'; x.fillRect(0, 0, it.w, it.h); }
      if (it.aged) { var g = x.createRadialGradient(it.w / 2, it.h / 2, Math.min(it.w, it.h) * 0.3, it.w / 2, it.h / 2, Math.hypot(it.w, it.h) * 0.6); g.addColorStop(0, 'rgba(120,80,30,0)'); g.addColorStop(1, 'rgba(120,80,30,' + 0.45 * it.aged + ')'); x.fillStyle = g; x.fillRect(0, 0, it.w, it.h); x.globalAlpha *= 0.25 * it.aged; x.globalCompositeOperation = 'multiply'; var m = 1 / s; x.save(); x.scale(m, m); x.fillStyle = x.createPattern(noise(), 'repeat'); x.fillRect(0, 0, it.w * s, it.h * s); x.restore(); }
      x.restore();
      if (it.border) { x.shadowColor = 'transparent'; x.globalAlpha = it.opacity == null ? 1 : it.opacity; maskPath(x, it.mask, it.w, it.h, it.radius); x.lineWidth = it.border; x.strokeStyle = it.borderColor || '#fff'; x.stroke(); }
    } else if (t === 'shape') {
      maskPath(x, it.mask, it.w, it.h, it.radius);
      if (it.fill && it.fill !== 'none') { x.fillStyle = it.fill; x.fill(); }
      x.shadowColor = 'transparent';
      if (it.stroke && it.stroke !== 'none' && it.sw) { x.lineWidth = it.sw; x.strokeStyle = it.stroke; if (it.dash) x.setLineDash([it.sw * 3, it.sw * 2]); x.stroke(); x.setLineDash([]); }
      if (it.mask === 'tag') { x.beginPath(); x.arc(Math.min(it.w * 0.3, it.h * 0.5) * 0.75, it.h / 2, Math.min(it.h * 0.08, 2.2), 0, 7); x.fillStyle = '#f7f1e6'; x.fill(); x.lineWidth = 0.3; x.strokeStyle = 'rgba(0,0,0,0.25)'; x.stroke(); }
    } else if (t === 'line') {
      x.beginPath(); x.moveTo(0, it.h / 2); x.lineTo(it.w, it.h / 2); x.lineWidth = it.sw || 0.4; x.strokeStyle = it.stroke || '#333'; if (it.dash) x.setLineDash([it.sw * 3, it.sw * 2]); x.stroke(); x.setLineDash([]);
    } else if (t === 'text') {
      x.shadowColor = it.shadow ? x.shadowColor : 'transparent';
      if (it.bg && it.bg !== 'none') { x.fillStyle = it.bg; x.fillRect(-1.5, -1, it.w + 3, it.h + 2); }
      var fs = it.size * PT; x.font = fontStr(it, fs); x.fillStyle = it.color || '#222'; x.textBaseline = 'top'; if (it.ls) x.letterSpacing = (it.ls * fs) + 'px';
      var lines = wrap(x, it.upper ? it.text.toUpperCase() : it.text, it.w), lh = fs * (it.lh || 1.25);
      lines.forEach(function (ln, i) { var w = x.measureText(ln).width, ax = it.align === 'center' ? (it.w - w) / 2 : it.align === 'right' ? it.w - w : 0; x.fillText(ln, ax, i * lh + (lh - fs) / 2); });
      x.letterSpacing = '0px';
    } else if (t === 'cal') drawCal(x, it);
    x.restore();
  }
  function drawCal(x, it) {
    var L = it.lang === 'ko' ? 'ko' : 'en', y0 = 0, W = it.w, H = it.h, ws = it.weekStart || 0, yr = it.year || 2027, mo = it.month || 0;
    var col = it.color || '#2b2b2b', acc = it.accent || '#b0483a', f = it.font || 'Lora';
    var head = it.showHead !== false ? H * 0.2 : 0;
    if (head) { var hs = Math.min(head * 0.62, W / 8); x.font = (it.headWeight || 500) + ' ' + hs + 'px "' + f + '", serif'; x.fillStyle = col; x.textBaseline = 'middle'; var title = MONTHS[L][mo] + (it.showYear === false ? '' : (L === 'ko' ? '  ' + yr : '  ' + yr)); var tw = x.measureText(title).width; x.fillText(title, it.headAlign === 'left' ? 0 : (W - tw) / 2, head / 2); y0 = head; }
    var rowsH = H - y0, wdH = rowsH * 0.1, first = new Date(yr, mo, 1).getDay(), days = new Date(yr, mo + 1, 0).getDate(), off = (first - ws + 7) % 7, rows = Math.ceil((off + days) / 7), ch = (rowsH - wdH) / rows, cw = W / 7;
    x.font = '600 ' + Math.min(wdH * 0.5, cw * 0.28) + 'px "' + (it.font2 || 'Josefin Sans') + '", sans-serif'; x.textBaseline = 'middle';
    for (var i = 0; i < 7; i++) { var d = (i + ws) % 7, lab = WD[L][d].toUpperCase(); x.fillStyle = d === 0 ? acc : col; x.globalAlpha = 0.85; var lw = x.measureText(lab).width; x.fillText(lab, i * cw + (cw - lw) / 2, y0 + wdH / 2); }
    x.globalAlpha = 1;
    if (it.lines !== 'none') { x.strokeStyle = col; x.globalAlpha = 0.22; x.lineWidth = 0.18; for (var r = 0; r <= rows; r++) { x.beginPath(); x.moveTo(0, y0 + wdH + r * ch); x.lineTo(W, y0 + wdH + r * ch); x.stroke(); } if (it.lines === 'grid') for (var c = 0; c <= 7; c++) { x.beginPath(); x.moveTo(c * cw, y0 + wdH); x.lineTo(c * cw, H); x.stroke(); } x.globalAlpha = 1; }
    x.font = (it.numWeight || 400) + ' ' + Math.min(ch * 0.32, cw * 0.3) + 'px "' + f + '", serif'; x.textBaseline = 'top';
    for (var dd = 1; dd <= days; dd++) { var p = off + dd - 1, cx = p % 7, cy = Math.floor(p / 7), wd = (cx + ws) % 7; x.fillStyle = wd === 0 ? acc : col; var s2 = String(dd), sw = x.measureText(s2).width; x.fillText(s2, it.numAlign === 'center' ? cx * cw + (cw - sw) / 2 : cx * cw + cw * 0.12, y0 + wdH + cy * ch + ch * 0.12); }
  }
  function renderPage(x, pg, s, exporting) { x.save(); x.scale(s, s); drawBg(x, pg, doc.w, doc.h, s); pg.items.forEach(function (it) { drawItem(x, it, s, exporting); }); x.restore(); }

  // ---------- DOM ----------
  app.innerHTML =
    '<header class="ebar">' +
    '<a class="ebrand" href="' + (ko ? '/ko' : '') + '/studio">Arttrip <b>Editor</b></a>' +
    '<input class="etitle" id="eTitle" aria-label="' + T('Title', '제목') + '">' +
    '<div class="egroup"><button id="bUndo" title="' + T('Undo', '되돌리기') + ' (Ctrl+Z)">↶</button><button id="bRedo" title="' + T('Redo', '다시하기') + ' (Ctrl+Y)">↷</button></div>' +
    '<select id="eSize" title="' + T('Page size', '종이 크기') + '">' + Object.keys(SIZES).map(function (k) { return '<option>' + k + '</option>'; }).join('') + '</select>' +
    '<div class="egroup"><button id="bZo">−</button><span id="eZoom">100%</span><button id="bZi">+</button></div>' +
    '<span class="espace"></span><span id="eLock" class="elock"></span>' +
    '<button class="ebtn ghost" id="bSave">' + T('Save', '저장') + '</button><button class="ebtn" id="bExport">' + T('Download', '다운로드') + '</button>' +
    '</header>' +
    '<div class="ebody">' +
    '<nav class="erail">' + [['add', T('Add', '추가'), '+'], ['art', T('Art', '명화'), '❖'], ['word', T('Verses', '말씀'), '❝'], ['kit', T('Elements', '꾸미기'), '✂'], ['tpl', T('Templates', '템플릿'), '▦'], ['bg', T('Paper', '배경지'), '◧'], ['layers', T('Layers', '레이어'), '≡']].map(function (r, i) { return '<button data-tab="' + r[0] + '"' + (i === 0 ? ' class="on"' : '') + '><i>' + r[2] + '</i>' + r[1] + '</button>'; }).join('') + '</nav>' +
    '<aside class="epanel" id="ePanel"></aside>' +
    '<main class="estage" id="eStage"><div class="ecanvas" id="eWrap"><canvas id="eCv"></canvas><canvas id="eOv"></canvas><textarea id="eTx" class="etx" spellcheck="false"></textarea></div></main>' +
    '<aside class="eprops" id="eProps"></aside>' +
    '</div>' +
    '<footer class="epages" id="ePages"></footer>' +
    '<div class="emodal" id="eModal" hidden></div><div class="etoast" id="eToast"></div>';
  var $ = function (id) { return document.getElementById(id); };
  var cv = $('eCv'), ov = $('eOv'), cx = cv.getContext('2d'), ox = ov.getContext('2d'), stage = $('eStage'), wrapEl = $('eWrap'), tx = $('eTx');
  function toast(m) { var t = $('eToast'); t.textContent = m; t.classList.add('on'); clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('on'); }, 2200); }
  var DPR = Math.min(2, window.devicePixelRatio || 1), S = 1; // px per mm on screen
  function layout() {
    var r = stage.getBoundingClientRect(), m = window.innerWidth < 760 ? 12 : 28; wrapEl.style.margin = m + 'px';
    fit = Math.max(0.2, Math.min((r.width - m * 2 - 6) / doc.w, (r.height - m * 2 - 6) / doc.h)); S = fit * zoom;
    var w = Math.round(doc.w * S), h = Math.round(doc.h * S);
    [cv, ov].forEach(function (c) { c.width = w * DPR; c.height = h * DPR; c.style.width = w + 'px'; c.style.height = h + 'px'; });
    wrapEl.style.width = w + 'px'; wrapEl.style.height = h + 'px'; $('eZoom').textContent = Math.round(zoom * 100) + '%';
    draw();
  }
  var raf = 0; function draw() { if (raf) return; raf = requestAnimationFrame(function () { raf = 0; cx.setTransform(1, 0, 0, 1, 0, 0); cx.clearRect(0, 0, cv.width, cv.height); renderPage(cx, page(), S * DPR, false); if (!unlocked) wm(cx, cv.width, cv.height, 0.10); overlay(); }); }
  function wm(x, w, h, a) { x.save(); x.globalAlpha = a; x.fillStyle = '#5a4a3a'; x.font = '600 ' + Math.round(w / 26) + 'px "Josefin Sans", sans-serif'; x.translate(w / 2, h / 2); x.rotate(-0.5); for (var i = -3; i <= 3; i++) { var t = 'ARTTRIP STUDIO · PREVIEW'; x.fillText(t, -x.measureText(t).width / 2, i * w / 5); } x.restore(); }

  // ---------- geometry ----------
  function toMM(e) { var r = ov.getBoundingClientRect(); return { x: (e.clientX - r.left) / S, y: (e.clientY - r.top) / S }; }
  function local(it, p) { var a = -(it.rot || 0) * Math.PI / 180, cx0 = it.x + it.w / 2, cy0 = it.y + it.h / 2, dx = p.x - cx0, dy = p.y - cy0; return { x: dx * Math.cos(a) - dy * Math.sin(a) + it.w / 2, y: dx * Math.sin(a) + dy * Math.cos(a) + it.h / 2 }; }
  function world(it, lx, ly) { var a = (it.rot || 0) * Math.PI / 180, dx = lx - it.w / 2, dy = ly - it.h / 2; return { x: it.x + it.w / 2 + dx * Math.cos(a) - dy * Math.sin(a), y: it.y + it.h / 2 + dx * Math.sin(a) + dy * Math.cos(a) }; }
  function hit(p) { var a = page().items; for (var i = a.length - 1; i >= 0; i--) { var it = a[i]; if (it.hidden) continue; var l = local(it, p); if (l.x >= -1 && l.y >= -1 && l.x <= it.w + 1 && l.y <= it.h + 1) return it; } return null; }
  function handles(it) { var hs = [['nw', 0, 0], ['n', it.w / 2, 0], ['ne', it.w, 0], ['e', it.w, it.h / 2], ['se', it.w, it.h], ['s', it.w / 2, it.h], ['sw', 0, it.h], ['w', 0, it.h / 2], ['rot', it.w / 2, -9 / S]]; if (it.type === 'text' || it.type === 'line') hs = hs.filter(function (h) { return it.type === 'line' ? ['e', 'w', 'rot'].indexOf(h[0]) >= 0 : ['n', 's'].indexOf(h[0]) < 0; }); return hs.map(function (h) { var w = world(it, h[1], h[2]); return { k: h[0], x: w.x, y: w.y }; }); }
  var guides = [];
  function overlay() {
    ox.setTransform(1, 0, 0, 1, 0, 0); ox.clearRect(0, 0, ov.width, ov.height); ox.scale(S * DPR, S * DPR);
    var lw = 1 / S;
    guides.forEach(function (g) { ox.strokeStyle = '#e0457b'; ox.lineWidth = lw; ox.setLineDash([4 / S, 3 / S]); ox.beginPath(); if (g.v != null) { ox.moveTo(g.v, 0); ox.lineTo(g.v, doc.h); } else { ox.moveTo(0, g.h); ox.lineTo(doc.w, g.h); } ox.stroke(); ox.setLineDash([]); });
    var it = sel && item(sel); if (!it) return;
    ox.save(); ox.translate(it.x + it.w / 2, it.y + it.h / 2); ox.rotate((it.rot || 0) * Math.PI / 180); ox.strokeStyle = it.locked ? '#999' : '#2f6fde'; ox.lineWidth = 1.5 * lw; ox.strokeRect(-it.w / 2, -it.h / 2, it.w, it.h);
    if (!it.locked) { ox.beginPath(); ox.moveTo(0, -it.h / 2); ox.lineTo(0, -it.h / 2 - 9 / S); ox.stroke(); }
    ox.restore();
    if (it.locked) return;
    handles(it).forEach(function (h) { ox.beginPath(); if (h.k === 'rot') ox.arc(h.x, h.y, 5 / S, 0, 7); else ox.rect(h.x - 4.5 / S, h.y - 4.5 / S, 9 / S, 9 / S); ox.fillStyle = '#fff'; ox.fill(); ox.lineWidth = 1.5 * lw; ox.strokeStyle = '#2f6fde'; ox.stroke(); });
  }
  function snap(it, dx, dy) {
    guides = []; var th = 6 / S, nx = it.x + dx, ny = it.y + dy;
    var xs = [0, doc.w / 2, doc.w], ys = [0, doc.h / 2, doc.h];
    page().items.forEach(function (o) { if (o.id === it.id || o.hidden) return; xs.push(o.x, o.x + o.w / 2, o.x + o.w); ys.push(o.y, o.y + o.h / 2, o.y + o.h); });
    var bx = null, by = null;
    [[nx, 0], [nx + it.w / 2, it.w / 2], [nx + it.w, it.w]].forEach(function (c) { xs.forEach(function (v) { var d = Math.abs(c[0] - v); if (d < th && (!bx || d < bx.d)) bx = { d: d, x: v - c[1], g: v }; }); });
    [[ny, 0], [ny + it.h / 2, it.h / 2], [ny + it.h, it.h]].forEach(function (c) { ys.forEach(function (v) { var d = Math.abs(c[0] - v); if (d < th && (!by || d < by.d)) by = { d: d, y: v - c[1], g: v }; }); });
    if (bx) { nx = bx.x; guides.push({ v: bx.g }); } if (by) { ny = by.y; guides.push({ h: by.g }); }
    return { x: nx, y: ny };
  }

  // ---------- pointer ----------
  var drag = null;
  ov.addEventListener('pointerdown', function (e) {
    if (tx.style.display === 'block') endText();
    var p = toMM(e), it = sel && item(sel);
    if (it && !it.locked) { var hs = handles(it); for (var i = 0; i < hs.length; i++) if (Math.hypot(hs[i].x - p.x, hs[i].y - p.y) < 8 / S) { drag = { k: hs[i].k, it: it, p0: p, o: clone(it) }; ov.setPointerCapture(e.pointerId); return; } }
    var h = hit(p);
    if (e.altKey && h && h.type === 'image') { sel = h.id; drag = { k: 'pan', it: h, p0: p, o: clone(h) }; ov.setPointerCapture(e.pointerId); props(); draw(); return; }
    sel = h ? h.id : null; props(); layersPanel(); draw();
    if (h && !h.locked) { drag = { k: 'move', it: h, p0: p, o: clone(h) }; ov.setPointerCapture(e.pointerId); }
  });
  ov.addEventListener('pointermove', function (e) {
    var p = toMM(e);
    if (!drag) { var it0 = sel && item(sel), cur = 'default'; if (it0 && !it0.locked) handles(it0).forEach(function (h) { if (Math.hypot(h.x - p.x, h.y - p.y) < 8 / S) cur = h.k === 'rot' ? 'grab' : 'nwse-resize'; }); if (cur === 'default' && hit(p)) cur = 'move'; ov.style.cursor = cur; return; }
    var it = drag.it, o = drag.o, dx = p.x - drag.p0.x, dy = p.y - drag.p0.y;
    if (drag.k === 'move') { var s = e.shiftKey ? { x: o.x + dx, y: o.y + dy } : snap(o, dx, dy); it.x = s.x; it.y = s.y; }
    else if (drag.k === 'pan') { var c = it.crop || (it.crop = { z: 1, ox: 0, oy: 0 }); c.ox = Math.max(-1, Math.min(1, (o.crop ? o.crop.ox : 0) - dx / it.w * 2)); c.oy = Math.max(-1, Math.min(1, (o.crop ? o.crop.oy : 0) - dy / it.h * 2)); }
    else if (drag.k === 'rot') { var a = Math.atan2(p.y - (o.y + o.h / 2), p.x - (o.x + o.w / 2)) * 180 / Math.PI + 90; if (!e.shiftKey) { var r = Math.round(a / 15) * 15; if (Math.abs(r - a) < 4) a = r; } it.rot = Math.round(((a % 360) + 360) % 360 * 10) / 10; }
    else resize(it, o, drag.k, p, e.shiftKey);
    draw();
  });
  function resize(it, o, k, p, free) {
    var l = local(o, p), x0 = 0, y0 = 0, x1 = o.w, y1 = o.h;
    if (k.indexOf('w') >= 0) x0 = Math.min(l.x, o.w - 2); if (k.indexOf('e') >= 0) x1 = Math.max(l.x, 2);
    if (k.indexOf('n') >= 0) y0 = Math.min(l.y, o.h - 2); if (k.indexOf('s') >= 0) y1 = Math.max(l.y, 2);
    var nw = x1 - x0, nh = y1 - y0;
    var keep = k.length === 2 && !free && (o.type === 'image' || o.type === 'cal' || o.type === 'text');
    if (keep) { var r = Math.max(nw / o.w, nh / o.h); nw = o.w * r; nh = o.h * r; if (k.indexOf('w') >= 0) x0 = o.w - nw; if (k.indexOf('n') >= 0) y0 = o.h - nh; }
    if (o.type === 'text') { if (keep) it.size = Math.max(4, Math.round(o.size * nw / o.w * 10) / 10); nh = textHeight(cx, Object.assign({}, it, { w: nw })); if (k.indexOf('n') >= 0) y0 = o.h - nh; }
    if (o.type === 'line') { nh = o.h; y0 = 0; }
    var c = world(o, x0 + nw / 2, y0 + nh / 2); it.w = nw; it.h = nh; it.x = c.x - nw / 2; it.y = c.y - nh / 2;
  }
  ov.addEventListener('pointerup', function () { if (drag) { drag = null; guides = []; commit(); props(); thumbs(); draw(); } });
  ov.addEventListener('dblclick', function (e) { var it = hit(toMM(e)); if (it && it.type === 'text' && !it.locked) startText(it); });
  stage.addEventListener('wheel', function (e) { if (!(e.ctrlKey || e.metaKey)) return; e.preventDefault(); setZoom(zoom * (e.deltaY < 0 ? 1.1 : 0.9)); }, { passive: false });
  function setZoom(z) { zoom = Math.max(0.25, Math.min(4, z)); layout(); }

  // ---------- text editing ----------
  var editing = null;
  function startText(it) {
    editing = it.id; var fs = it.size * PT * S; tx.value = it.text; tx.style.display = 'block';
    Object.assign(tx.style, { left: it.x * S + 'px', top: it.y * S + 'px', width: it.w * S + 'px', minHeight: it.h * S + 'px', font: fontStr(it, fs), lineHeight: (it.lh || 1.25), color: it.color, textAlign: it.align || 'left', transform: 'rotate(' + (it.rot || 0) + 'deg)', letterSpacing: (it.ls || 0) * fs + 'px' });
    var keep = it.color; it.color = 'rgba(0,0,0,0)'; draw(); tx._keep = keep; tx.focus(); tx.select();
  }
  function endText() { var it = editing && item(editing); tx.style.display = 'none'; if (!it) return; it.color = tx._keep; it.text = tx.value; it.h = textHeight(cx, it); editing = null; commit(); props(); draw(); thumbs(); }
  tx.addEventListener('blur', endText); tx.addEventListener('keydown', function (e) { if (e.key === 'Escape') tx.blur(); e.stopPropagation(); });

  // ---------- keyboard ----------
  document.addEventListener('keydown', function (e) {
    if (/input|textarea|select/i.test(e.target.tagName)) return;
    var it = sel && item(sel), mod = e.ctrlKey || e.metaKey;
    if (mod && e.key.toLowerCase() === 'z') { e.preventDefault(); e.shiftKey ? redo() : undo(); return; }
    if (mod && e.key.toLowerCase() === 'y') { e.preventDefault(); redo(); return; }
    if (mod && e.key.toLowerCase() === 'c' && it) { clip = clone(it); toast(T('Copied', '복사했어요')); return; }
    if (mod && e.key.toLowerCase() === 'v' && clip) { var c = clone(clip); c.id = uid(); c.x += 4; c.y += 4; page().items.push(c); sel = c.id; clip = clone(c); commit(); refresh(); return; }
    if (mod && e.key.toLowerCase() === 'd' && it) { e.preventDefault(); dup(); return; }
    if (!it) return;
    if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); del(); return; }
    if (e.key === 'Enter' && it.type === 'text') { e.preventDefault(); startText(it); return; }
    var st = e.shiftKey ? 5 : 0.5, mv = { ArrowLeft: [-st, 0], ArrowRight: [st, 0], ArrowUp: [0, -st], ArrowDown: [0, st] }[e.key];
    if (mv && !it.locked) { e.preventDefault(); it.x += mv[0]; it.y += mv[1]; draw(); clearTimeout(this._k); this._k = setTimeout(function () { commit(); props(); }, 400); }
  });
  function dup() { var it = item(sel); if (!it) return; var c = clone(it); c.id = uid(); c.x += 4; c.y += 4; var a = page().items; a.splice(a.indexOf(it) + 1, 0, c); sel = c.id; commit(); refresh(); }
  function del() { var a = page().items, it = item(sel); if (!it) return; a.splice(a.indexOf(it), 1); sel = null; commit(); refresh(); }
  function order(dir) { var a = page().items, it = item(sel); if (!it) return; var i = a.indexOf(it); a.splice(i, 1); var j = dir === 'top' ? a.length : dir === 'bottom' ? 0 : Math.max(0, Math.min(a.length, i + dir)); a.splice(j, 0, it); commit(); refresh(); }
  function align(how) { var it = item(sel); if (!it) return; if (how === 'l') it.x = 0; if (how === 'c') it.x = (doc.w - it.w) / 2; if (how === 'r') it.x = doc.w - it.w; if (how === 't') it.y = 0; if (how === 'm') it.y = (doc.h - it.h) / 2; if (how === 'b') it.y = doc.h - it.h; commit(); refresh(); }


  // ---------- Scripture (verses) ----------
  var WL = ko ? 'ko' : 'en', BOOKS = null;
  function esc2(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function verseCard(text, ref) { return '<button class="ewv" data-t="' + esc2(text) + '" data-r="' + esc2(ref) + '"><span>' + esc2(text) + '</span><b>' + esc2(ref) + '</b></button>'; }
  function showVerses(list, box) {
    box.innerHTML = list.length ? list.map(function (v) { return WL === 'ko' ? verseCard(v.tk, v.k) : verseCard(v.te, v.e); }).join('') : '<p class="esmall">' + T('No verses found. Try other words.', '찾은 말씀이 없어요. 다른 말로 찾아보세요.') + '</p>';
    box.querySelectorAll('.ewv').forEach(function (b) { b.onclick = function () { addVerse(b.dataset.t, b.dataset.r); }; });
  }
  function wordFetch(qs) {
    var box = $('eWres'); box.innerHTML = '<p class="esmall">' + T('Searching…', '찾는 중…') + '</p>';
    fetch('/api/verses?' + qs).then(function (r) { return r.json(); }).then(function (d) {
      wordFetch.last = d.verses || [];
      if (d.topics && d.topics.length) $('eWtopics').querySelectorAll('button').forEach(function (b) { b.classList.toggle('on', d.topics.some(function (t) { return t.id === b.dataset.t; })); });
      showVerses(wordFetch.last, box);
    }).catch(function () { box.innerHTML = '<p class="esmall">' + T('Could not search right now.', '지금은 찾을 수 없어요.') + '</p>'; });
  }
  function wordInit() {
    fetch('/api/verses?list=1').then(function (r) { return r.json(); }).then(function (d) {
      $('eWtopics').innerHTML = d.topics.map(function (t) { return '<button data-t="' + t.id + '">' + esc2(ko ? t.ko : t.en) + '</button>'; }).join('');
      $('eWtopics').querySelectorAll('button').forEach(function (b) { b.onclick = function () { wordFetch('topic=' + b.dataset.t); }; });
    });
    $('eWgo').onclick = function () { var q = $('eWq').value.trim(); if (q) wordFetch('q=' + encodeURIComponent(q) + '&lang=' + WL); };
    $('eWq').onkeydown = function (e) { if (e.key === 'Enter') $('eWgo').onclick(); e.stopPropagation(); };
    $('eWlang').querySelectorAll('button').forEach(function (b) { b.onclick = function () { WL = b.dataset.l; $('eWlang').querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); }); if (wordFetch.last) showVerses(wordFetch.last, $('eWres')); fillBooks(); }; });
    function fillBooks() {
      var go = function () { $('eWbook').innerHTML = BOOKS[WL].map(function (n, i) { return '<option value="' + (i + 1) + '">' + esc2(n) + '</option>'; }).join(''); $('eWbook').value = String(fillBooks.b || 19); fillCh(); };
      if (BOOKS) go(); else fetch('/bible/books.json').then(function (r) { return r.json(); }).then(function (d) { BOOKS = d; go(); });
    }
    function fillCh() { var b = +$('eWbook').value; fillBooks.b = b; var n = BOOKS.chapters[b - 1]; $('eWch').innerHTML = Array.from({ length: n }, function (_, i) { return '<option value="' + (i + 1) + '">' + (i + 1) + (ko ? '장' : '') + '</option>'; }).join(''); $('eWch').value = String(Math.min(fillCh.c || 23, n)); loadCh(); }
    function loadCh() {
      var b = +$('eWbook').value, c = +$('eWch').value; fillCh.c = c;
      fetch('/bible/' + WL + '/' + b + '.json').then(function (r) { return r.json(); }).then(function (chs) {
        var name = BOOKS[WL][b - 1]; if (WL === 'en' && name === 'Psalms') name = 'Psalm';
        showVerses(chs[c - 1].map(function (t, i) { var r = name + ' ' + c + ':' + (i + 1); return WL === 'ko' ? { tk: t, k: r } : { te: t, e: r }; }), $('eWch_v'));
      });
    }
    $('eWbook').onchange = fillCh; $('eWch').onchange = loadCh; fillBooks();
  }
  function addVerse(text, ref) {
    var kr = /[가-힣]/.test(text), len = text.length, size = kr ? (len < 30 ? 22 : len < 60 ? 17 : 13) : (len < 50 ? 22 : len < 110 ? 16 : 12);
    var o = { type: 'text', text: text, font: kr ? 'Gowun Batang' : 'Cormorant Garamond', italic: !kr, size: size, color: '#2c241c', align: 'center', lh: 1.4, x: doc.w * 0.12, y: doc.h * 0.36, w: doc.w * 0.76 };
    o.h = textHeight(cx, o); add(o, true);
    var r = { type: 'text', text: ref, font: kr ? 'Noto Sans KR' : 'Josefin Sans', size: 9, color: '#8a5a3c', align: 'center', ls: 0.12, x: o.x, y: o.y + o.h + 4, w: o.w };
    if (!kr) r.upper = true; r.h = textHeight(cx, r); add(r);
    toast(T('Verse added', '말씀을 넣었어요'));
  }

  // ---------- adding ----------
  function add(o, noSel) { o.id = uid(); if (o.rot == null) o.rot = 0; page().items.push(o); if (!noSel) sel = o.id; commit(); refresh(); return o; }
  function addText(kind) {
    var P = { title: { text: T('A day in the museum', '미술관에서의 하루'), size: 34, font: 'Playfair Display', weight: 500 }, sub: { text: T('Notes from a quiet afternoon', '조용한 오후의 기록'), size: 14, font: 'Cormorant Garamond', italic: true }, body: { text: T('Write your story here. Double-click to edit.', '여기에 이야기를 적으세요. 두 번 눌러 고쳐요.'), size: 10, font: 'Lora' }, type: { text: 'NO. 1907 — ADMIT ONE', size: 11, font: 'Special Elite', ls: 0.08 }, hand: { text: T('with love', '사랑을 담아'), size: 24, font: ko ? 'Nanum Pen Script' : 'Caveat' } }[kind] || {};
    var o = Object.assign({ type: 'text', x: doc.w * 0.15, y: doc.h * 0.4, w: doc.w * 0.7, color: '#2c241c', align: 'center', lh: 1.25 }, P); o.h = textHeight(cx, o); add(o);
  }
  function addArt(a) { var r = a.w / a.h, w = Math.min(doc.w * 0.6, doc.h * 0.6 * r), h = w / r; add({ type: 'image', src: '/img/' + a.id + '.jpg', hi: '/hi/' + a.id + '.jpg', art: a.id, x: (doc.w - w) / 2, y: (doc.h - h) / 2, w: w, h: h, crop: { z: 1, ox: 0, oy: 0 }, credit: a.t + ' — ' + a.a }); }
  function addUpload(file) {
    if (!file || !/^image\//.test(file.type)) return;
    var r = new FileReader(); r.onload = function () { var im = new Image(); im.onload = function () { var c = document.createElement('canvas'), k = Math.min(1, 3000 / Math.max(im.width, im.height)); c.width = im.width * k; c.height = im.height * k; c.getContext('2d').drawImage(im, 0, 0, c.width, c.height); var url = c.toDataURL('image/jpeg', 0.9), ra = c.width / c.height, w = Math.min(doc.w * 0.6, doc.h * 0.6 * ra); add({ type: 'image', src: url, x: (doc.w - w) / 2, y: (doc.h - w / ra) / 2, w: w, h: w / ra, crop: { z: 1, ox: 0, oy: 0 }, upload: true }); }; im.src = r.result; }; r.readAsDataURL(file);
  }
  function addCal(m) { var w = doc.w * 0.8, h = w * 0.62; add({ type: 'cal', year: 2027, month: m == null ? 0 : m, weekStart: 0, lang: ko ? 'ko' : 'en', font: 'Lora', color: '#2c241c', accent: '#b0483a', lines: 'rows', x: (doc.w - w) / 2, y: doc.h - h - 14, w: w, h: h }); }
  function artPick(theme, i) { var a = LIB.filter(function (r) { return !theme || r.theme === theme; }); if (!a.length) a = LIB; return a[(i || 0) % a.length]; }
  function element(kind) {
    var a = artPick(null, Math.floor(Math.random() * 50)), src = a ? '/img/' + a.id + '.jpg' : '', hi = a ? '/hi/' + a.id + '.jpg' : '';
    var E = {
      stamp: { type: 'image', mask: 'stamp', src: src, hi: hi, w: 34, h: 42, shadow: 0.6, filter: { sat: -0.1, warm: 0.2 }, aged: 0.4 },
      ticket: { type: 'shape', mask: 'ticket', fill: '#e8d6b0', stroke: '#8a6a3f', sw: 0.35, dash: true, w: 70, h: 30, shadow: 0.4 },
      tag: { type: 'shape', mask: 'tag', fill: '#d8c2a0', stroke: 'none', w: 60, h: 28, shadow: 0.5 },
      label: { type: 'shape', mask: 'label', fill: '#f6efe0', stroke: '#6d5a44', sw: 0.4, w: 64, h: 26, shadow: 0.3 },
      tape: { type: 'tape', mask: 'torn', src: src, hi: hi, w: 70, h: 16, opacity: 0.82, filter: { fade: 0.6 }, rot: -6 },
      frame: { type: 'image', mask: 'arch', src: src, hi: hi, w: 60, h: 80, border: 2.5, borderColor: '#f7f1e6', shadow: 0.5, aged: 0.3 },
      oval: { type: 'image', mask: 'ellipse', src: src, hi: hi, w: 50, h: 64, border: 1.6, borderColor: '#c9a66b', shadow: 0.4 },
      torn: { type: 'image', mask: 'torn', src: src, hi: hi, w: 80, h: 60, shadow: 0.5, aged: 0.5, filter: { sepia: 0.25 } },
      polaroid: null,
      rule: { type: 'line', w: 80, h: 2, sw: 0.4, stroke: '#6d5a44' },
      dashed: { type: 'line', w: 80, h: 2, sw: 0.35, stroke: '#6d5a44', dash: true },
      circle: { type: 'shape', mask: 'ellipse', fill: 'none', stroke: '#8a3b2e', sw: 0.6, w: 36, h: 36 },
      rect: { type: 'shape', fill: '#efe3cc', stroke: 'none', w: 60, h: 40 }
    };
    if (kind === 'polaroid') { var x0 = doc.w / 2 - 32, y0 = doc.h / 2 - 38; var back = add({ type: 'shape', fill: '#fbf8f2', stroke: 'none', x: x0, y: y0, w: 64, h: 76, shadow: 0.6, rot: -3 }, true); add({ type: 'image', src: src, hi: hi, x: x0 + 4, y: y0 + 4, w: 56, h: 56, rot: -3, crop: { z: 1, ox: 0, oy: 0 } }); return back; }
    var o = E[kind]; if (!o) return; var nn = page().items.length % 6; o = Object.assign({}, o, { x: (doc.w - o.w) / 2 + (nn - 2.5) * 7, y: (doc.h - o.h) / 2 + (nn - 2.5) * 9, crop: { z: 1, ox: 0, oy: 0 } }); if (a && o.type !== 'shape' && o.type !== 'line') o.credit = a.t + ' — ' + a.a; add(o);
    if (kind === 'ticket') add({ type: 'text', text: 'ADMIT ONE · 1889', font: 'Special Elite', size: 11, color: '#5b4127', align: 'center', ls: 0.1, x: o.x + 4, y: o.y + o.h / 2 - 2.5, w: o.w - 8, h: 5 });
    if (kind === 'label') add({ type: 'text', text: T('Specimen No. 27', '표본 제27호'), font: 'Cormorant Garamond', italic: true, size: 14, color: '#3b2f24', align: 'center', x: o.x + 4, y: o.y + o.h / 2 - 3, w: o.w - 8, h: 6 });
  }

  // ---------- templates ----------
  function T_cover(artist, works, yr) {
    var p = blankPage(); p.bg = { kind: 'color', color: '#f6f1e7' }; var w = works[0];
    p.items = [
      { id: uid(), type: 'text', text: artist, font: 'Playfair Display', size: 38, color: '#1f1a15', align: 'center', x: 15, y: 22, w: doc.w - 30, h: 16, rot: 0 },
      { id: uid(), type: 'text', text: String(yr), font: 'Josefin Sans', size: 15, color: '#a2483b', align: 'center', ls: 0.3, x: 15, y: 42, w: doc.w - 30, h: 7, rot: 0 },
      w ? { id: uid(), type: 'image', src: '/img/' + w.id + '.jpg', hi: '/hi/' + w.id + '.jpg', x: 22, y: 60, w: doc.w - 44, h: doc.h - 110, crop: { z: 1, ox: 0, oy: 0 }, border: 0, shadow: 0.35, rot: 0, credit: w.t } : null,
      { id: uid(), type: 'text', text: T('A wall calendar of public-domain masterpieces', '퍼블릭 도메인 명화 벽걸이 달력'), font: 'Cormorant Garamond', italic: true, size: 13, color: '#5a4b3c', align: 'center', x: 15, y: doc.h - 38, w: doc.w - 30, h: 6, rot: 0 }
    ].filter(Boolean); return p;
  }
  function T_month(w, m, yr) {
    var p = blankPage(); p.bg = { kind: 'color', color: '#fbf8f2' };
    var ih = doc.h * 0.52;
    p.items = [
      w ? { id: uid(), type: 'image', src: '/img/' + w.id + '.jpg', hi: '/hi/' + w.id + '.jpg', x: 14, y: 14, w: doc.w - 28, h: ih, crop: { z: 1, ox: 0, oy: 0 }, rot: 0, credit: w.t } : null,
      w ? { id: uid(), type: 'text', text: w.t + ' — ' + w.a, font: 'Cormorant Garamond', italic: true, size: 9, color: '#6a5a4a', align: 'right', x: 14, y: 16 + ih, w: doc.w - 28, h: 4, rot: 0 } : null,
      { id: uid(), type: 'cal', year: yr, month: m, weekStart: 0, lang: ko ? 'ko' : 'en', font: 'Lora', color: '#2a231c', accent: '#a2483b', lines: 'rows', x: 18, y: ih + 26, w: doc.w - 36, h: doc.h - ih - 40, rot: 0 }
    ].filter(Boolean); return p;
  }
  function calendarDoc(artistSlug, size) {
    var works = LIB.filter(function (r) { return r.as === artistSlug; }); if (!works.length) works = LIB.slice(0, 12);
    var d = newDoc(size); doc = d; var name = works[0] ? works[0].a : 'Masterpieces', yr = 2027;
    d.title = name + ' ' + yr; d.pages = [T_cover(name, works, yr)]; for (var m = 0; m < 12; m++) d.pages.push(T_month(works[(m + 1) % works.length], m, yr)); return d;
  }
  function ln_(x, y, w, col, o) { return Object.assign({ id: uid(), type: 'line', x: x, y: y, w: w, h: 2, sw: 0.3, stroke: col || '#6d5a44', rot: 0 }, o || {}); }
  function aged(p, color, o) { p.bg = Object.assign({ kind: 'aged', color: color, grain: 0.7, stain: 0.5, vignette: 0.55, pattern: 'none' }, o || {}); }
  function artBg(p, a, f, o) { if (!a) return aged(p, PAPERS.cream); p.bg = Object.assign({ kind: 'image', src: '/img/' + a.id + '.jpg', hi: '/hi/' + a.id + '.jpg', filter: f, color: '#efe6d4', grain: 0.5, stain: 0.25, vignette: 0.5 }, o || {}); }
  var W_ = function () { return doc.w; }, H_ = function () { return doc.h; };
  var PAPER_TPL = [
    { id: 'botanical', n: T('Botanical collage', '보태니컬 콜라주'), f: function (p) { aged(p, PAPERS.cream, { pattern: 'grid', step: 9, lineColor: 'rgba(120,100,70,0.18)' }); var W = W_(), H = H_(); return [img_(artPick('flowers', 0), 'torn', 16, 24, W - 32, H * 0.42, { shadow: 0.5, aged: 0.35, filter: { warm: 0.2, fade: 0.1 } }), img_(artPick('flowers', 5), 'arch', W * 0.08, H * 0.5, W * 0.36, H * 0.3, { border: 2, borderColor: '#f8f2e6', shadow: 0.5, rot: -3 }), img_(artPick('flowers', 9), 'stamp', W * 0.62, H * 0.47, W * 0.22, H * 0.15, { shadow: 0.55, rot: 6 }), shp_('label', W * 0.5, H * 0.68, W * 0.42, H * 0.09, '#f7efdf', { stroke: '#7a6248', sw: 0.35, shadow: 0.3 }), txt_('Flora Botanica', 'Cormorant Garamond', 22, W * 0.52, H * 0.695, W * 0.38, 'center', '#3a2c20', { italic: true }), txt_('No. 27 · ' + T('pressed in June', '6월에 눌러 말림'), 'Special Elite', 9, W * 0.52, H * 0.74, W * 0.38, 'center', '#6a5238'), img_(artPick('flowers', 12), 'torn', W * 0.1, H * 0.84, W * 0.8, 8, { type: 'tape', opacity: 0.8, filter: { fade: 0.55 }, rot: -2 })]; } },
    { id: 'letter', n: T('Vintage letter', '빈티지 편지지'), f: function (p) { aged(p, PAPERS.parchment, { pattern: 'lines', step: 8.5, lineColor: 'rgba(110,80,50,0.25)', stain: 0.6, vignette: 0.7 }); var W = W_(), H = H_(); return [ln_(24, 0, H, '#b45a4a', { rot: 90, x: 24 - H / 2, y: H / 2 - 1, w: H, sw: 0.35 }), img_(artPick('flowers', 2), 'arch', W - 64, 14, 48, 64, { border: 2, borderColor: '#f3ead8', shadow: 0.5, aged: 0.35, rot: 4 }), txt_(T('Dear friend,', '사랑하는 친구에게,'), ko ? 'Nanum Pen Script' : 'Homemade Apple', ko ? 30 : 18, 30, 40, W - 100, 'left', '#3a2c20'), txt_(T('Paris, the twelfth of May', '파리에서, 5월 12일'), 'Cormorant Garamond', 12, 30, 28, 90, 'left', '#6a5238', { italic: true })]; } },
    { id: 'ledger', n: T('Old ledger', '오래된 장부'), f: function (p) { aged(p, '#efe6cf', { pattern: 'lines', step: 6.5, lineColor: 'rgba(60,90,130,0.25)', stain: 0.55 }); var W = W_(), H = H_(); return [shp_('rect', 0, 0, W, 22, 'rgba(162,72,59,0.08)'), ln_(18, 0, H, '#b45a4a', { rot: 90, x: 18 - H / 2, y: H / 2 - 1, w: H, sw: 0.3 }), ln_(W - 40, 0, H, '#b45a4a', { rot: 90, x: W - 40 - H / 2, y: H / 2 - 1, w: H, sw: 0.3 }), txt_('LEDGER · 1891', 'Special Elite', 14, 22, 8, 80, 'left', '#7a3e32', { ls: 0.12 }), img_(artPick('portraits', 3), 'oval', W - 58, H - 78, 44, 56, { mask: 'ellipse', border: 1.4, borderColor: '#b8955a', shadow: 0.4, filter: { sepia: 0.4, fade: 0.2 } })]; } },
    { id: 'tickets', n: T('Museum tickets', '미술관 티켓'), f: function (p) { aged(p, '#e9dcc0', { pattern: 'dots', step: 7 }); var W = W_(), H = H_(), out = [], cols = ['#e7cfa4', '#d9c3b0', '#cfd6c4', '#e3c9c0', '#d6d0e2']; var th = (H - 40) / 5; for (var i = 0; i < 5; i++) { var y = 20 + i * th; out.push(shp_('ticket', 18, y, W - 36, th - 8, cols[i], { stroke: '#7a5a38', sw: 0.35, dash: true, shadow: 0.35 })); out.push(ln_(W - 70, y + (th - 8) / 2, th - 16, '#7a5a38', { rot: 90, x: W - 70 - (th - 16) / 2, y: y + (th - 8) / 2 - 1, w: th - 16, dash: true, sw: 0.3 })); out.push(txt_('ADMIT ONE', 'Bebas Neue', 22, 30, y + 6, 90, 'left', '#4d3620', { ls: 0.08 })); out.push(txt_(T('Musée des Beaux-Arts · Gallery ', '미술관 · 전시실 ') + (i + 3) + ' · No. ' + (18807 + i * 131), 'Special Elite', 9, 30, y + 16, W - 110, 'left', '#5b4127')); out.push(img_(artPick(['masterpieces', 'japanese-prints', 'sea', 'flowers', 'landscapes'][i], i * 2), null, W - 64, y + 5, th - 18, th - 18, { radius: 1, filter: { fade: 0.15, warm: 0.15 } })); } return out; } },
    { id: 'stamps', n: T('Postage stamp sheet', '우표 시트'), f: function (p) { aged(p, '#f1e8d6', { stain: 0.25, vignette: 0.3 }); var W = W_(), H = H_(), out = [], c = 3, r = 4, gw = (W - 30) / c, gh = (H - 50) / r, th = ['masterpieces', 'flowers', 'japanese-prints', 'sea', 'birds', 'landscapes']; out.push(txt_(T('Masterpiece stamps — cut along the perforation', '명화 우표 — 톱니 모양을 따라 오려요'), 'Cormorant Garamond', 13, 15, 14, W - 30, 'center', '#5a4632', { italic: true })); for (var i = 0; i < c * r; i++) { var x = 15 + (i % c) * gw + gw * 0.12, y = 34 + Math.floor(i / c) * gh + gh * 0.06, w = gw * 0.76, h = gh * 0.86; out.push(shp_('stamp', x - 1.6, y - 1.6, w + 3.2, h + 3.2, '#fbf7ef', { shadow: 0.35 })); out.push(img_(artPick(th[i % th.length], i * 3 + 1), null, x + 2, y + 2, w - 4, h - 12, {})); out.push(txt_(['25c', '1 F', '50c', '3 F', '10c', '2 F'][i % 6], 'Bebas Neue', 11, x + 2, y + h - 9, 20, 'left', '#7a3e32')); out.push(txt_(['ART', 'POSTE', 'MUSÉE', 'PARIS', 'TOKYO', 'FLORA'][i % 6], 'Josefin Sans', 7, x + w - 26, y + h - 8, 24, 'right', '#5a4632', { ls: 0.15 })); } return out; } },
    { id: 'tags', n: T('Tags & labels', '꼬리표와 라벨'), f: function (p) { aged(p, PAPERS.kraft, { stain: 0.3, vignette: 0.45, grain: 0.9 }); var W = W_(), H = H_(), out = [], words = ko ? ['소중한 날', '기억', '여름 정원', '편지', '오늘의 그림', '산책'] : ['Keepsake', 'Memories', 'Summer garden', 'Letters', 'Today', 'Wanderlust']; for (var i = 0; i < 6; i++) { var x = i % 2 ? W / 2 + 6 : 16, y = 18 + Math.floor(i / 2) * ((H - 30) / 3); out.push(shp_('tag', x, y, W / 2 - 22, 34, ['#f3ead8', '#e8d3c4', '#dfe3d4'][i % 3], { stroke: '#6d5a44', sw: 0.3, shadow: 0.4 })); out.push(txt_(words[i], 'Cormorant Garamond', 17, x + 16, y + 10, W / 2 - 44, 'center', '#3a2c20', { italic: true })); out.push(shp_('label', x + 4, y + 46, W / 2 - 30, 22, '#f8f2e6', { stroke: '#7a6248', sw: 0.3, shadow: 0.3 })); out.push(txt_(['No. 01', 'No. 07', 'No. 12', 'No. 19', 'No. 23', 'No. 31'][i], 'Special Elite', 11, x + 8, y + 53, W / 2 - 38, 'center', '#5b4127', { ls: 0.1 })); } return out; } },
    { id: 'tape', n: T('Washi tape strips', '마스킹 테이프 스트립'), f: function (p) { aged(p, '#f6f1e6', { stain: 0.15, vignette: 0.2 }); var W = W_(), H = H_(), out = [], th = ['flowers', 'japanese-prints', 'textiles', 'sea', 'landscapes', 'birds', 'masterpieces', 'still-life']; out.push(txt_(T('Printable washi strips — print on sticker paper', '인쇄용 마스킹 테이프 — 스티커 용지에 인쇄하세요'), 'Cormorant Garamond', 13, 15, 12, W - 30, 'center', '#5a4632', { italic: true })); var n = 12, gap = (H - 40) / n; for (var i = 0; i < n; i++) out.push(img_(artPick(th[i % th.length], i * 5), 'torn', 18, 30 + i * gap, W - 36, gap * 0.62, { type: 'tape', opacity: 0.92, filter: { fade: 0.2, sat: 0.05, bright: 0.04 }, crop: { z: 2.2, ox: (i % 3 - 1) * 0.6, oy: 0 } })); return out; } },
    { id: 'cards', n: T('Journaling cards', '저널링 카드'), f: function (p) { p.bg = { kind: 'color', color: '#ffffff' }; var W = W_(), H = H_(), out = [], cw = (W - 24) / 2, ch = (H - 24) / 3, th = ['flowers', 'sea', 'japanese-prints', 'landscapes', 'birds', 'winter']; for (var i = 0; i < 6; i++) { var x = 12 + (i % 2) * cw, y = 12 + Math.floor(i / 2) * ch; out.push(shp_('rect', x + 2, y + 2, cw - 4, ch - 4, ['#f4ecdc', '#e8eef0', '#f1e6dd', '#eaeee2', '#f3ece8', '#e9edf2'][i], { stroke: 'rgba(0,0,0,0.12)', sw: 0.25, dash: true })); out.push(img_(artPick(th[i], i * 2 + 1), i % 3 === 0 ? 'arch' : null, x + 8, y + 8, cw * 0.42, ch - 16, { radius: i % 3 === 1 ? 3 : 0, border: i % 3 === 2 ? 1.5 : 0, borderColor: '#fff' })); for (var l = 0; l < 5; l++) out.push(ln_(x + cw * 0.48, y + 16 + l * (ch - 24) / 5, cw * 0.46, 'rgba(90,70,50,0.45)', { sw: 0.25 })); out.push(txt_(ko ? ['오늘', '바다', '꽃', '산책', '새', '겨울'][i] : ['Today', 'By the sea', 'In bloom', 'Wander', 'Birdsong', 'Winter'][i], 'Playfair Display', 13, x + cw * 0.48, y + 6, cw * 0.46, 'left', '#3a2c20', { italic: true })); } return out; } },
    { id: 'monet', n: T('Water lilies paper', '수련 아트페이퍼'), f: function (p) { var a = LIB.find(function (r) { return /water lil/i.test(r.t + ' ' + (r.tk || '')) || /수련/.test(r.tk || ''); }) || artPick('landscapes', 0); artBg(p, a, { fade: 0.45, sat: -0.15, warm: 0.15 }); return []; } },
    { id: 'wave', n: T('Great Wave paper', '큰 파도 아트페이퍼'), f: function (p) { var a = LIB.find(function (r) { return /great wave|kanagawa/i.test(r.t); }) || artPick('japanese-prints', 0); artBg(p, a, { fade: 0.4, sepia: 0.2 }, { crop: 1 }); return [shp_('label', W_() * 0.2, H_() * 0.78, W_() * 0.6, 26, '#f6efe0', { stroke: '#2d3c52', sw: 0.35, shadow: 0.35 }), txt_(T('Notes from the sea', '바다에서 온 메모'), 'DM Serif Display', 18, W_() * 0.22, H_() * 0.78 + 7, W_() * 0.56, 'center', '#2d3c52')]; } },
    { id: 'japanese-prints', n: T('Ukiyo-e journal', '우키요에 저널'), f: function (p) { aged(p, '#efe4cf', { pattern: 'dots', step: 7 }); var W = W_(), H = H_(); return [img_(artPick('japanese-prints', 1), null, 18, 18, W - 36, H * 0.38, { border: 1.5, borderColor: '#2c241c' }), shp_('rect', 18, H * 0.44, 7, H * 0.48, '#a2483b'), txt_(T('Notes', '메모'), 'DM Serif Display', 28, 32, H * 0.44, 100, 'left', '#2c241c'), img_(artPick('japanese-prints', 7), 'stamp', W - 56, H * 0.44, 36, 46, { shadow: 0.5, rot: 4 }), img_(artPick('birds', 2), null, W - 70, H - 74, 50, 56, { border: 2, borderColor: '#fbf7ef', shadow: 0.45, rot: -4 })]; } },
    { id: 'postcard', n: T('Postcards', '엽서 두 장'), f: function (p) { aged(p, PAPERS.ivory, { stain: 0.2, vignette: 0.2 }); var W = W_(), H = H_(), out = [], ph = (H - 30) / 2; for (var i = 0; i < 2; i++) { var y = 12 + i * (ph + 6); out.push(shp_('rect', 12, y, W - 24, ph, '#fbf7ef', { stroke: 'rgba(0,0,0,0.15)', sw: 0.25, dash: true })); out.push(txt_('POST CARD', 'Josefin Sans', 14, 20, y + 8, 80, 'left', '#3b4a58', { ls: 0.35 })); out.push(ln_(W / 2, y + ph / 2, ph - 24, '#5a6a78', { rot: 90, x: W / 2 - (ph - 24) / 2, y: y + ph / 2 - 1, w: ph - 24 })); for (var l = 0; l < 4; l++) out.push(ln_(W / 2 + 8, y + ph * 0.45 + l * 11, W / 2 - 30, '#5a6a78', { sw: 0.25 })); out.push(img_(artPick(i ? 'sea' : 'winter', 3 + i), 'stamp', W - 48, y + 8, 30, 36, { shadow: 0.4 })); out.push(shp_('ellipse', W - 72, y + 14, 26, 26, 'none', { stroke: 'rgba(80,50,40,0.55)', sw: 0.5, rot: -12 })); out.push(txt_(T('Write a little note here…', '짧은 안부를 적어 보세요…'), ko ? 'Nanum Pen Script' : 'Caveat', ko ? 20 : 16, 20, y + 24, W / 2 - 30, 'left', '#4b5a68')); } return out; } },
    { id: 'frames', n: T('Collage frames', '콜라주 액자'), f: function (p) { aged(p, '#ece3d3', { pattern: 'grid', step: 10, lineColor: 'rgba(120,100,70,0.15)' }); var W = W_(), H = H_(); return [img_(artPick('portraits', 1), 'ellipse', 18, 20, W * 0.38, H * 0.3, { border: 2.4, borderColor: '#c9a66b', shadow: 0.5 }), img_(artPick('landscapes', 4), 'arch', W * 0.5, 16, W * 0.42, H * 0.36, { border: 2.5, borderColor: '#fbf7ef', shadow: 0.5, rot: 3 }), img_(artPick('flowers', 7), 'torn', 16, H * 0.42, W * 0.55, H * 0.28, { shadow: 0.5, aged: 0.4, rot: -2 }), img_(artPick('cats', 0), null, W * 0.62, H * 0.45, W * 0.3, H * 0.24, { border: 3, borderColor: '#fff', shadow: 0.6, rot: 5 }), img_(artPick('sea', 6), 'stamp', W * 0.12, H * 0.76, W * 0.2, H * 0.15, { shadow: 0.5 }), shp_('ticket', W * 0.4, H * 0.8, W * 0.48, 28, '#e7cfa4', { stroke: '#7a5a38', sw: 0.35, dash: true, shadow: 0.35, rot: -3 }), txt_('ADMIT ONE · 1874', 'Special Elite', 12, W * 0.42, H * 0.8 + 10, W * 0.44, 'center', '#4d3620', { rot: -3 })]; } },
    { id: 'exhibit', n: T('Exhibition poster', '전시회 포스터'), f: function (p) { aged(p, '#f3eee4', { stain: 0.12, vignette: 0.2, grain: 0.35 }); var W = W_(), H = H_(), k = W / 210, a = artFit('masterpieces', 0); if (!a) return []; var f = fitBox(a, W * 0.09, H * 0.07, W * 0.82, H * 0.64); return [img_(a, null, f[0], f[1], f[2], f[3], { shadow: 0.25 }), txt_(ko ? (a.ak || a.a) : a.a, 'Josefin Sans', 30 * k, W * 0.08, H * 0.76, W * 0.84, 'center', '#2a2622', { upper: true, ls: 0.12, weight: 600 }), txt_(ko ? (a.tk || a.t) : a.t, 'Cormorant Garamond', 15 * k, W * 0.1, H * 0.84, W * 0.8, 'center', '#5b4f43', { italic: true }), ln_(W * 0.42, H * 0.905, W * 0.16, '#8a7a66', { sw: 0.35 * k }), txt_(T('ARTTRIP STUDIO · MASTERPIECE COLLECTION', '아트트립 스튜디오 · 명화 컬렉션'), 'Josefin Sans', 7.5 * k, W * 0.1, H * 0.925, W * 0.8, 'center', '#7a6c5c', { ls: 0.2 })]; } },
    { id: 'gallery', n: T('Gallery print', '갤러리 액자 포스터'), f: function (p) { aged(p, '#fbfaf7', { stain: 0, vignette: 0, grain: 0.15 }); var W = W_(), H = H_(), k = W / 210, a = artFit('landscapes', 3); if (!a) return []; var f = fitBox(a, W * 0.1, H * 0.07, W * 0.8, H * 0.8); return [img_(a, null, f[0], f[1], f[2], f[3]), txt_((ko ? (a.tk || a.t) : a.t) + '  —  ' + (ko ? (a.ak || a.a) : a.a), 'Cormorant Garamond', 10 * k, W * 0.1, f[1] + f[3] + H * 0.03, W * 0.8, 'center', '#4a4540', { italic: true })]; } },
    { id: 'blank', n: T('Blank aged paper', '빈 빈티지 종이'), f: function (p) { aged(p, PAPERS.cream, { stain: 0.55, vignette: 0.65 }); return []; } }
  ];
  function artFit(theme, i) { var port = H_() >= W_(), a = LIB.filter(function (r) { return (!theme || r.theme === theme) && r.w && r.h && ((r.h >= r.w * 1.05) === port); }); return a.length ? a[(i || 0) % a.length] : artPick(theme, i); }
  function fitBox(a, bx, by, bw, bh) { var r = (a.w && a.h) ? a.w / a.h : 0.8, w = bw, h = bw / r; if (h > bh) { h = bh; w = bh * r; } return [bx + (bw - w) / 2, by + (bh - h) / 2, w, h]; }
  function img_(a, mask, x, y, w, h, o) { if (!a) return null; return Object.assign({ id: uid(), type: 'image', src: '/img/' + a.id + '.jpg', hi: '/hi/' + a.id + '.jpg', mask: mask, x: x, y: y, w: w, h: h, rot: 0, crop: { z: 1, ox: 0, oy: 0 }, credit: a.t + ' — ' + a.a }, o || {}); }
  function txt_(t, f, sz, x, y, w, al, col, o) { var it = Object.assign({ id: uid(), type: 'text', text: t, font: f, size: sz, x: x, y: y, w: w, align: al, color: col, rot: 0, lh: 1.25 }, o || {}); it.h = textHeight(cx, it); return it; }
  function shp_(m, x, y, w, h, fill, o) { return Object.assign({ id: uid(), type: 'shape', mask: m === 'rect' ? null : m, fill: fill, x: x, y: y, w: w, h: h, rot: 0 }, o || {}); }
  function paperPage(t) { var p = blankPage(); p.items = t.f(p).filter(Boolean); return p; }

  // ---------- panels ----------
  var tab = 'add';
  function panel() {
    var P = $('ePanel'), h = '';
    if (tab === 'add') h = '<h3>' + T('Text', '글자') + '</h3><div class="egrid1">' + [['title', T('Add a heading', '제목 넣기'), 'Playfair Display', 20], ['sub', T('Add a subheading', '부제 넣기'), 'Cormorant Garamond', 16], ['body', T('Add body text', '본문 넣기'), 'Lora', 13], ['type', T('Typewriter label', '타자기 글씨'), 'Special Elite', 13], ['hand', T('Handwriting', '손글씨'), ko ? 'Nanum Pen Script' : 'Caveat', 20]].map(function (b) { return '<button class="etextbtn" data-text="' + b[0] + '" style="font-family:\'' + b[2] + '\';font-size:' + b[3] + 'px">' + b[1] + '</button>'; }).join('') + '</div>' +
      '<h3>' + T('Your photo', '내 사진') + '</h3><label class="eup"><input type="file" accept="image/*" id="eFile" multiple>' + T('Upload photos', '사진 올리기') + '<small>' + T('Stays on this device', '사진은 이 기기에만 저장돼요') + '</small></label>' +
      '<h3>' + T('Calendar grid', '달력') + '</h3><div class="egrid3">' + MONTHS[ko ? 'ko' : 'en'].map(function (m, i) { return '<button data-cal="' + i + '">' + (ko ? m : m.slice(0, 3)) + '</button>'; }).join('') + '</div>' +
      '<h3>' + T('Lines & shapes', '선과 도형') + '</h3><div class="egrid3">' + [['rule', T('Line', '선')], ['dashed', T('Dashed', '점선')], ['circle', T('Circle', '원')], ['rect', T('Block', '사각형')], ['label', T('Label', '라벨')], ['tag', T('Tag', '꼬리표')]].map(function (b) { return '<button data-el="' + b[0] + '">' + b[1] + '</button>'; }).join('') + '</div>';
    if (tab === 'word') h = '<h3>' + T('Find a verse with AI', 'AI로 말씀 찾기') + '</h3><div class="ewq"><input class="esearch" id="eWq" placeholder="' + T('e.g. comfort for a hard week, wedding, thanks', '예: 힘든 친구를 위로하는 말씀, 결혼, 감사') + '"><button id="eWgo">' + T('Find', '찾기') + '</button></div>' +
      '<div class="eseg" id="eWlang"><button data-l="ko"' + (ko ? ' class="on"' : '') + '>한글 (개역한글)</button><button data-l="en"' + (ko ? '' : ' class="on"') + '>English (KJV)</button></div>' +
      '<div class="echips" id="eWtopics"></div><div id="eWres" class="ewres"></div>' +
      '<h3>' + T('Browse by book', '성경 펼쳐 보기') + '</h3><div class="ewbrowse"><select id="eWbook"></select><select id="eWch"></select></div><div id="eWch_v" class="ewres"></div>' +
      '<p class="esmall">' + T('Verses come word for word from the KJV and the 1961 Korean Revised Version, both in the public domain. The AI only finds them; it never writes Scripture.', '말씀은 개역한글판(1961)과 KJV 원문 그대로 가져와요. 둘 다 저작권이 끝난 공개 본문이에요. AI는 찾아 주기만 하고 말씀을 지어내지 않아요.') + '</p>';
    if (tab === 'art') h = '<h3>' + T('Masterpieces', '명화') + '</h3><input class="esearch" id="eQ" placeholder="' + T('Search artist, title, theme', '화가·작품·주제 검색') + '"><div class="echips" id="eThemes"></div><div class="eart" id="eArt"></div><p class="esmall">' + T('All works are public domain (CC0). Click to add, then Alt+drag inside a picture to move it within its frame.', '모든 작품은 저작권이 끝난 퍼블릭 도메인이에요. 눌러서 넣고, 그림 안에서 Alt를 누른 채 끌면 틀 안에서 위치를 옮겨요.') + '</p>';
    if (tab === 'kit') h = '<h3>' + T('Journal elements', '저널 꾸미기') + '</h3><div class="ekit">' + [['stamp', T('Postage stamp', '우표')], ['ticket', T('Ticket', '티켓')], ['tape', T('Washi tape', '마스킹 테이프')], ['frame', T('Arch frame', '아치 액자')], ['oval', T('Oval cameo', '타원 액자')], ['torn', T('Torn scrap', '찢은 종이')], ['polaroid', T('Polaroid', '폴라로이드')], ['tag', T('Gift tag', '선물 꼬리표')], ['label', T('Specimen label', '표본 라벨')]].map(function (b) { return '<button data-el="' + b[0] + '"><span class="ek ek-' + b[0] + '"></span>' + b[1] + '</button>'; }).join('') + '</div><p class="esmall">' + T('Each element picks a random masterpiece. Change it in the panel on the right.', '꾸미기 요소는 명화를 하나 골라 채워요. 오른쪽 설정에서 다른 그림으로 바꿀 수 있어요.') + '</p>';
    if (tab === 'tpl') h = '<h3>' + T('Art papers', '아트페이퍼') + '</h3><div class="etpl">' + PAPER_TPL.map(function (t) { return '<button data-tpl="' + t.id + '"><canvas width="120" height="160" data-prev="' + t.id + '"></canvas><span>' + t.n + '</span></button>'; }).join('') + '</div><p class="esmall">' + T('Adds a new page with the design.', '디자인이 새 페이지로 추가돼요.') + '</p>' +
      '<h3>' + T('Calendars 2027', '2027 달력') + '</h3><div class="egrid1" id="eCalList"></div>';
    if (tab === 'bg') { var bg = page().bg || {}; h = '<h3>' + T('Paper colour', '종이 색') + '</h3><div class="eswatch">' + Object.keys(PAPERS).map(function (k) { return '<button data-paper="' + k + '" style="background:' + PAPERS[k] + '" title="' + k + '"></button>'; }).join('') + '<input type="color" id="eBgC" value="' + (bg.color || '#ffffff') + '"></div>' +
      '<h3>' + T('Vintage effect', '빈티지 효과') + '</h3>' + rng('bgGrain', T('Grain', '종이 결'), bg.grain || 0) + rng('bgStain', T('Stains', '얼룩'), bg.stain || 0) + rng('bgVig', T('Burnt edges', '가장자리 그을림'), bg.vignette || 0) +
      '<h3>' + T('Ruling', '줄무늬') + '</h3><div class="egrid3">' + [['none', T('None', '없음')], ['lines', T('Lines', '줄')], ['grid', T('Grid', '모눈')], ['dots', T('Dots', '점')]].map(function (b) { return '<button data-pat="' + b[0] + '"' + ((bg.pattern || 'none') === b[0] ? ' class="on"' : '') + '>' + b[1] + '</button>'; }).join('') + '</div>' +
      '<h3>' + T('Masterpiece as paper', '명화를 배경으로') + '</h3><p class="esmall">' + T('Select a picture, then press “Make background” in its settings.', '그림을 고른 뒤 오른쪽 설정에서 [배경으로]를 누르세요.') + '</p>'; }
    if (tab === 'layers') h = '<h3>' + T('Layers on this page', '이 페이지의 레이어') + '</h3><div id="eLayers"></div>';
    P.innerHTML = h;
    if (tab === 'word') wordInit(); if (tab === 'art') artGrid(); if (tab === 'layers') layersPanel(); if (tab === 'tpl') tplPrev();
  }
  function rng(id, lab, v, min, max, st) { return '<label class="erng"><span>' + lab + '</span><input type="range" data-r="' + id + '" min="' + (min == null ? 0 : min) + '" max="' + (max == null ? 1 : max) + '" step="' + (st || 0.01) + '" value="' + v + '"></label>'; }
  function artGrid() {
    var q = ($('eQ') && $('eQ').value || '').toLowerCase(), th = artGrid.th || '';
    var themes = {}; LIB.forEach(function (r) { themes[r.theme] = (themes[r.theme] || 0) + 1; });
    $('eThemes').innerHTML = ['', ...Object.keys(themes)].map(function (k) { return '<button data-th="' + k + '"' + (k === th ? ' class="on"' : '') + '>' + (k ? (THN[k] || k) : T('All', '전체')) + '</button>'; }).join('');
    var rows = LIB.filter(function (r) { return (!th || r.theme === th) && (!q || (r.t + ' ' + r.a + ' ' + (r.tk || '') + ' ' + (r.ak || '')).toLowerCase().indexOf(q) >= 0); }).slice(0, 160);
    $('eArt').innerHTML = rows.map(function (r) { return '<button data-art="' + r.id + '" title="' + esc(r.t + ' — ' + r.a) + '"><img src="/img/' + r.id + '.jpg" loading="lazy" alt=""></button>'; }).join('') || '<p class="esmall">' + T('Nothing found', '찾는 작품이 없어요') + '</p>';
  }
  var THN = ko ? { masterpieces: '명작', landscapes: '풍경', 'japanese-prints': '일본 목판화', sea: '바다', portraits: '초상화', flowers: '꽃', winter: '겨울', horses: '말', birds: '새', textiles: '문양', cats: '고양이', 'still-life': '정물' } : { masterpieces: 'Masterpieces', landscapes: 'Landscapes', 'japanese-prints': 'Japanese prints', sea: 'Sea', portraits: 'Portraits', flowers: 'Flowers', winter: 'Winter', horses: 'Horses', birds: 'Birds', textiles: 'Patterns', cats: 'Cats', 'still-life': 'Still life' };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function tplPrev() {
    var keepDoc = doc; PAPER_TPL.forEach(function (t) { var c = document.querySelector('[data-prev="' + t.id + '"]'); if (!c) return; var pg = paperPage(t), x = c.getContext('2d'); x.clearRect(0, 0, 120, 160); renderPage(x, pg, Math.min(120 / doc.w, 160 / doc.h), false); });
    doc = keepDoc;
    var artists = {}; LIB.forEach(function (r) { if (r.as) artists[r.as] = artists[r.as] || { n: r.a, c: 0 }; if (r.as) artists[r.as].c++; });
    $('eCalList').innerHTML = Object.keys(artists).filter(function (k) { return artists[k].c >= 4; }).sort(function (a, b) { return artists[b].c - artists[a].c; }).slice(0, 24).map(function (k) { return '<button data-calart="' + k + '">' + esc(artists[k].n) + ' <small>(' + artists[k].c + ')</small></button>'; }).join('');
  }
  function layersPanel() {
    var L = $('eLayers'); if (!L) return; var a = page().items.slice().reverse();
    var nm = function (it) { return it.type === 'text' ? '“' + it.text.slice(0, 22) + '”' : it.type === 'cal' ? T('Calendar ', '달력 ') + MONTHS[ko ? 'ko' : 'en'][it.month] : it.type === 'image' || it.type === 'tape' ? (it.upload ? T('My photo', '내 사진') : (it.credit || T('Picture', '그림')).slice(0, 26)) : T('Shape', '도형'); };
    L.innerHTML = a.length ? a.map(function (it) { return '<div class="elayer' + (it.id === sel ? ' on' : '') + '" data-lay="' + it.id + '"><span>' + esc(nm(it)) + '</span><button data-vis="' + it.id + '" title="' + T('Show/hide', '보이기/숨기기') + '">' + (it.hidden ? '◌' : '●') + '</button><button data-lock="' + it.id + '" title="' + T('Lock', '잠금') + '">' + (it.locked ? '🔒' : '🔓') + '</button></div>'; }).join('') : '<p class="esmall">' + T('This page is empty.', '이 페이지는 비어 있어요.') + '</p>';
  }

  // ---------- properties ----------
  function props() {
    var P = $('eProps'), it = sel && item(sel); if (!it) { P.innerHTML = '<div class="eempty"><b>' + T('Page', '페이지') + ' ' + (pageIx + 1) + '/' + doc.pages.length + '</b><p>' + T('Select something on the page to change it. Double-click text to type.', '페이지에서 요소를 눌러 고르면 여기서 바꿀 수 있어요. 글자는 두 번 눌러 바로 고쳐요.') + '</p><p class="esmall">' + T('Shortcuts: Ctrl+Z undo · Ctrl+D duplicate · arrows nudge · Shift+drag no snapping · Alt+drag move picture in frame', '단축키: Ctrl+Z 되돌리기 · Ctrl+D 복제 · 방향키 미세 이동 · Shift+끌기 자석 끔 · Alt+끌기 틀 안 그림 이동') + '</p></div>'; return; }
    var h = '<div class="eact"><button data-a="dup" title="' + T('Duplicate', '복제') + '">⧉</button><button data-a="up" title="' + T('Forward', '앞으로') + '">▲</button><button data-a="down" title="' + T('Backward', '뒤로') + '">▼</button><button data-a="lock" title="' + T('Lock', '잠금') + '">' + (it.locked ? '🔒' : '🔓') + '</button><button data-a="del" class="danger" title="' + T('Delete', '삭제') + '">🗑</button></div>';
    if (it.type === 'text') {
      h += '<h3>' + T('Text', '글자') + '</h3><textarea class="etxt" data-p="text" rows="3">' + esc(it.text) + '</textarea>' +
        '<label class="efld"><span>' + T('Font', '글꼴') + '</span><select data-p="font">' + FONTS.map(function (f) { return '<option' + (f[0] === it.font ? ' selected' : '') + ' style="font-family:\'' + f[0] + '\'">' + f[0] + '</option>'; }).join('') + '</select></label>' +
        '<div class="erow">' + num('size', T('Size (pt)', '크기(pt)'), it.size, 4, 300, 0.5) + col('color', T('Colour', '색'), it.color) + '</div>' +
        '<div class="egrid4">' + [['left', '⟸'], ['center', '≡'], ['right', '⟹']].map(function (a) { return '<button data-set="align:' + a[0] + '"' + (it.align === a[0] ? ' class="on"' : '') + '>' + a[1] + '</button>'; }).join('') + '<button data-tog="italic"' + (it.italic ? ' class="on"' : '') + '><i>I</i></button><button data-tog="upper"' + (it.upper ? ' class="on"' : '') + '>AA</button><button data-set="weight:' + ((it.weight || 400) >= 600 ? 400 : 700) + '"' + ((it.weight || 400) >= 600 ? ' class="on"' : '') + '><b>B</b></button></div>' +
        rng('ls', T('Letter spacing', '자간'), it.ls || 0, -0.05, 0.5, 0.01) + rng('lh', T('Line height', '줄 간격'), it.lh || 1.25, 0.8, 2.4, 0.05) +
        '<label class="efld"><span>' + T('Highlight', '글자 배경') + '</span><input type="color" data-p="bg" value="' + (it.bg && it.bg !== 'none' ? it.bg : '#f3e6c8') + '"><button class="mini" data-set="bg:none">' + T('None', '없음') + '</button></label>';
    }
    if (it.type === 'image' || it.type === 'tape') {
      h += '<h3>' + T('Picture', '그림') + '</h3>' + (it.credit ? '<p class="esmall">' + esc(it.credit) + '</p>' : '') +
        '<div class="egrid2"><button data-a="swap">' + T('Replace picture', '그림 바꾸기') + '</button><label class="ebtnl"><input type="file" accept="image/*" data-swapfile>' + T('Use my photo', '내 사진으로') + '</label></div>' +
        '<h3>' + T('Frame shape', '틀 모양') + '</h3><div class="egrid4">' + [['', '▭'], ['ellipse', '◯'], ['arch', '⌂'], ['stamp', '✉'], ['ticket', '🎟'], ['label', '⬡'], ['torn', '≈'], ['tag', '◁']].map(function (m) { return '<button data-set="mask:' + m[0] + '"' + ((it.mask || '') === m[0] ? ' class="on"' : '') + '>' + m[1] + '</button>'; }).join('') + '</div>' +
        rng('cz', T('Zoom in frame', '틀 안 확대'), (it.crop && it.crop.z) || 1, 1, 4, 0.01) + rng('radius', T('Rounded corners', '모서리 둥글게'), it.radius || 0, 0, 30, 0.5) +
        '<h3>' + T('Colour & age', '색감과 빈티지') + '</h3>' + rng('f.bright', T('Brightness', '밝기'), fv(it, 'bright'), -0.5, 0.5) + rng('f.contrast', T('Contrast', '대비'), fv(it, 'contrast'), -0.5, 0.6) + rng('f.sat', T('Saturation', '채도'), fv(it, 'sat'), -1, 0.8) + rng('f.warm', T('Warmth', '따뜻함'), fv(it, 'warm'), -1, 1) + rng('f.sepia', T('Sepia', '세피아'), fv(it, 'sepia'), 0, 1) + rng('f.fade', T('Faded', '바랜 느낌'), fv(it, 'fade'), 0, 1) + rng('aged', T('Aged paper', '오래된 종이'), it.aged || 0, 0, 1) +
        '<div class="egrid3">' + [['', T('Original', '원본')], ['vintage', T('Vintage', '빈티지')], ['bw', T('B&W', '흑백')], ['soft', T('Soft', '부드럽게')], ['vivid', T('Vivid', '선명하게')], ['tea', T('Tea-stained', '홍차 물들임')]].map(function (p) { return '<button data-preset="' + p[0] + '">' + p[1] + '</button>'; }).join('') + '</div>' +
        '<h3>' + T('Border & shadow', '테두리와 그림자') + '</h3><div class="erow">' + num('border', T('Border (mm)', '테두리(mm)'), it.border || 0, 0, 20, 0.5) + col('borderColor', T('Colour', '색'), it.borderColor || '#ffffff') + '</div>' + rng('shadow', T('Shadow', '그림자'), it.shadow || 0, 0, 1.5) +
        '<button class="ewide" data-a="asbg">' + T('Make background', '배경으로') + '</button>';
    }
    if (it.type === 'shape' || it.type === 'line') {
      h += '<h3>' + T('Shape', '도형') + '</h3>' + (it.type === 'shape' ? '<div class="egrid4">' + [['', '▭'], ['ellipse', '◯'], ['ticket', '🎟'], ['label', '⬡'], ['tag', '◁'], ['stamp', '✉'], ['arch', '⌂'], ['torn', '≈']].map(function (m) { return '<button data-set="mask:' + m[0] + '"' + ((it.mask || '') === m[0] ? ' class="on"' : '') + '>' + m[1] + '</button>'; }).join('') + '</div><div class="erow">' + col('fill', T('Fill', '채우기'), it.fill && it.fill !== 'none' ? it.fill : '#efe3cc') + '<button class="mini" data-set="fill:none">' + T('No fill', '채우기 없음') + '</button></div>' : '') +
        '<div class="erow">' + col('stroke', T('Line colour', '선 색'), it.stroke && it.stroke !== 'none' ? it.stroke : '#6d5a44') + num('sw', T('Line (mm)', '선 굵기'), it.sw || 0, 0, 5, 0.05) + '</div><button data-tog="dash"' + (it.dash ? ' class="on"' : '') + '>' + T('Dashed', '점선') + '</button>' + rng('radius', T('Rounded corners', '모서리 둥글게'), it.radius || 0, 0, 30, 0.5) + rng('shadow', T('Shadow', '그림자'), it.shadow || 0, 0, 1.5);
    }
    if (it.type === 'cal') {
      h += '<h3>' + T('Calendar', '달력') + '</h3><div class="erow"><label class="efld"><span>' + T('Month', '월') + '</span><select data-p="month">' + MONTHS[ko ? 'ko' : 'en'].map(function (m, i) { return '<option value="' + i + '"' + (i === it.month ? ' selected' : '') + '>' + m + '</option>'; }).join('') + '</select></label>' + num('year', T('Year', '연도'), it.year, 1900, 2100, 1) + '</div>' +
        '<div class="egrid2"><button data-set="weekStart:0"' + (!it.weekStart ? ' class="on"' : '') + '>' + T('Week starts Sun', '일요일 시작') + '</button><button data-set="weekStart:1"' + (it.weekStart === 1 ? ' class="on"' : '') + '>' + T('Week starts Mon', '월요일 시작') + '</button><button data-set="lang:en"' + (it.lang !== 'ko' ? ' class="on"' : '') + '>English</button><button data-set="lang:ko"' + (it.lang === 'ko' ? ' class="on"' : '') + '>한국어</button></div>' +
        '<label class="efld"><span>' + T('Font', '글꼴') + '</span><select data-p="font">' + FONTS.map(function (f) { return '<option' + (f[0] === it.font ? ' selected' : '') + '>' + f[0] + '</option>'; }).join('') + '</select></label>' +
        '<div class="erow">' + col('color', T('Text', '글자'), it.color) + col('accent', T('Sundays', '일요일'), it.accent) + '</div>' +
        '<div class="egrid3">' + [['none', T('No lines', '선 없음')], ['rows', T('Rows', '가로줄')], ['grid', T('Grid', '칸')]].map(function (b) { return '<button data-set="lines:' + b[0] + '"' + ((it.lines || 'rows') === b[0] ? ' class="on"' : '') + '>' + b[1] + '</button>'; }).join('') + '</div>' +
        '<div class="egrid2"><button data-tog="showHead"' + (it.showHead !== false ? ' class="on"' : '') + '>' + T('Month title', '월 제목') + '</button><button data-tog="showYear"' + (it.showYear !== false ? ' class="on"' : '') + '>' + T('Show year', '연도 표시') + '</button></div>' +
        '<button class="ewide" data-a="fillyear">' + T('Make all 12 months from this page', '이 페이지로 12개월 만들기') + '</button>';
    }
    h += '<h3>' + T('Position', '위치') + '</h3><div class="egrid6">' + [['l', '⇤'], ['c', '↔'], ['r', '⇥'], ['t', '⤒'], ['m', '↕'], ['b', '⤓']].map(function (a) { return '<button data-al="' + a[0] + '">' + a[1] + '</button>'; }).join('') + '</div>' +
      '<div class="erow">' + num('x', 'X', r1(it.x), -500, 800, 0.5) + num('y', 'Y', r1(it.y), -500, 800, 0.5) + '</div><div class="erow">' + num('w', T('Width', '너비'), r1(it.w), 1, 900, 0.5) + (it.type === 'text' ? '' : num('h', T('Height', '높이'), r1(it.h), 1, 900, 0.5)) + '</div>' +
      rng('rot', T('Rotate', '회전'), it.rot || 0, -180, 180, 1) + rng('opacity', T('Opacity', '투명도'), it.opacity == null ? 1 : it.opacity, 0.05, 1);
    P.innerHTML = h;
  }
  function r1(v) { return Math.round(v * 10) / 10; }
  function fv(it, k) { return (it.filter && it.filter[k]) || 0; }
  function num(p, lab, v, mn, mx, st) { return '<label class="efld"><span>' + lab + '</span><input type="number" data-n="' + p + '" value="' + v + '" min="' + mn + '" max="' + mx + '" step="' + st + '"></label>'; }
  function col(p, lab, v) { return '<label class="efld"><span>' + lab + '</span><input type="color" data-p="' + p + '" value="' + (v || '#000000') + '"></label>'; }
  var PRESETS = { '': {}, vintage: { sepia: 0.35, warm: 0.3, contrast: -0.08, fade: 0.25 }, bw: { gray: 1, contrast: 0.12 }, soft: { fade: 0.4, contrast: -0.15, sat: -0.15 }, vivid: { sat: 0.35, contrast: 0.12 }, tea: { sepia: 0.6, warm: 0.4, fade: 0.35, bright: 0.04 } };

  // ---------- events (delegated) ----------
  document.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return; var d = b.dataset, it = sel && item(sel);
    if (d.tab) { tab = d.tab; document.querySelectorAll('.erail button').forEach(function (x) { x.classList.toggle('on', x === b); }); document.body.classList.add('epanel-open'); panel(); return; }
    if (d.text) return addText(d.text);
    if (d.cal != null) return addCal(+d.cal);
    if (d.el) return element(d.el);
    if (d.art) { var a = LIB.find(function (r) { return r.id === d.art; }); if (swapMode && it) { it.src = '/img/' + a.id + '.jpg'; it.hi = '/hi/' + a.id + '.jpg'; it.credit = a.t + ' — ' + a.a; it.upload = false; swapMode = false; commit(); refresh(); toast(T('Picture replaced', '그림을 바꿨어요')); return; } return addArt(a); }
    if (d.th != null) { artGrid.th = d.th; artGrid(); return; }
    if (d.tpl) { var t = PAPER_TPL.find(function (x) { return x.id === d.tpl; }); doc.pages.splice(pageIx + 1, 0, paperPage(t)); pageIx++; sel = null; commit(); refresh(); return; }
    if (d.calart) { if (!confirm(T('Replace this document with a 13-page calendar?', '지금 문서를 13페이지 달력으로 바꿀까요?'))) return; calendarDoc(d.calart, doc.size); pageIx = 0; sel = null; commit(); layout(); refresh(); return; }
    if (d.paper) { page().bg.color = PAPERS[d.paper]; if (page().bg.kind === 'color' && d.paper !== 'white') page().bg.kind = 'aged'; commit(); draw(); thumbs(); return; }
    if (d.pat) { page().bg.pattern = d.pat; commit(); panel(); draw(); thumbs(); return; }
    if (d.lay) { sel = d.lay; props(); layersPanel(); draw(); return; }
    if (d.vis) { var v = item(d.vis); v.hidden = !v.hidden; commit(); layersPanel(); draw(); return; }
    if (d.lock) { var l = item(d.lock); l.locked = !l.locked; commit(); layersPanel(); props(); draw(); return; }
    if (d.al) return align(d.al);
    if (d.preset != null && it) { it.filter = Object.assign({}, PRESETS[d.preset]); it.aged = d.preset === 'vintage' || d.preset === 'tea' ? 0.4 : 0; commit(); props(); draw(); return; }
    if (d.set && it) { var kv = d.set.split(':'), val = kv[1]; if (kv[0] === 'weekStart') val = +val; if (kv[0] === 'weight') val = +val; it[kv[0]] = val === '' ? null : val; if (it.type === 'text') it.h = textHeight(cx, it); commit(); props(); draw(); thumbs(); return; }
    if (d.tog && it) { it[d.tog] = !(it[d.tog] === undefined ? (d.tog === 'showHead' || d.tog === 'showYear') : it[d.tog]); if (it.type === 'text') it.h = textHeight(cx, it); commit(); props(); draw(); return; }
    if (d.a && it) {
      if (d.a === 'dup') dup(); if (d.a === 'del') del(); if (d.a === 'up') order(1); if (d.a === 'down') order(-1); if (d.a === 'lock') { it.locked = !it.locked; commit(); props(); draw(); }
      if (d.a === 'swap') { swapMode = true; tab = 'art'; document.querySelectorAll('.erail button').forEach(function (x) { x.classList.toggle('on', x.dataset.tab === 'art'); }); document.body.classList.add('epanel-open'); panel(); toast(T('Pick the new picture on the left', '왼쪽에서 새 그림을 고르세요')); }
      if (d.a === 'asbg') { page().bg = { kind: 'image', src: it.src, hi: it.hi, filter: it.filter, color: '#f4ecdc', grain: 0.4, stain: 0.2, vignette: 0.4 }; del(); toast(T('Now the page background', '페이지 배경이 됐어요')); }
      if (d.a === 'fillyear') fillYear(it);
      return;
    }
    if (b.id === 'bUndo') undo(); if (b.id === 'bRedo') redo(); if (b.id === 'bZi') setZoom(zoom * 1.2); if (b.id === 'bZo') setZoom(zoom / 1.2);
    if (b.id === 'bExport') exportDialog(); if (b.id === 'bSave') save();
    if (d.pg != null) { pageIx = +d.pg; sel = null; refresh(); }
    if (d.pga) pageAct(d.pga);
  });
  var swapMode = false;
  function fillYear(c) {
    var base = page(), ix = base.items.indexOf(c), pics = LIB.filter(function (r) { var cur = base.items.find(function (q) { return q.type === 'image' && q.art; }); return cur ? r.as === (LIB.find(function (z) { return z.id === cur.art; }) || {}).as : false; });
    for (var m = 0; m < 12; m++) { if (m === c.month) continue; var p = clone(base); p.id = uid(); p.items.forEach(function (q) { q.id = uid(); }); p.items[ix].month = m; var im = p.items.find(function (q) { return q.type === 'image' && q.art; }); if (im && pics.length) { var w = pics[m % pics.length]; im.src = '/img/' + w.id + '.jpg'; im.hi = '/hi/' + w.id + '.jpg'; im.art = w.id; im.credit = w.t + ' — ' + w.a; } doc.pages.push(p); }
    commit(); refresh(); toast(T('12 months are ready — pages at the bottom', '12개월이 만들어졌어요 · 아래 페이지 목록을 보세요'));
  }
  document.addEventListener('input', function (e) {
    var el = e.target, it = sel && item(sel), d = el.dataset;
    if (el.id === 'eQ') return artGrid();
    if (el.id === 'eTitle') { doc.title = el.value; autosave(); return; }
    if (el.id === 'eBgC') { page().bg.color = el.value; draw(); clearTimeout(el._t); el._t = setTimeout(function () { commit(); thumbs(); }, 300); return; }
    if (d.r && /^bg/.test(d.r)) { var m = { bgGrain: 'grain', bgStain: 'stain', bgVig: 'vignette' }[d.r]; page().bg[m] = +el.value; if (page().bg.kind === 'color') page().bg.kind = 'aged'; draw(); clearTimeout(el._t); el._t = setTimeout(function () { commit(); thumbs(); }, 300); return; }
    if (!it) return;
    if (d.r) { var v = +el.value; if (d.r.indexOf('f.') === 0) { it.filter = it.filter || {}; it.filter[d.r.slice(2)] = v; } else if (d.r === 'cz') { it.crop = it.crop || { z: 1, ox: 0, oy: 0 }; it.crop.z = v; } else it[d.r] = v; if (it.type === 'text') it.h = textHeight(cx, it); draw(); clearTimeout(el._t); el._t = setTimeout(commit, 300); return; }
    if (d.n) { var n = parseFloat(el.value); if (isNaN(n)) return; it[d.n] = n; if (it.type === 'text') it.h = textHeight(cx, it); draw(); clearTimeout(el._t); el._t = setTimeout(function () { commit(); thumbs(); }, 300); return; }
    if (d.p) { it[d.p] = d.p === 'month' ? +el.value : el.value; if (it.type === 'text') it.h = textHeight(cx, it); if (d.p === 'font') loadFont(el.value).then(function () { if (it.type === 'text') it.h = textHeight(cx, it); draw(); }); draw(); clearTimeout(el._t); el._t = setTimeout(function () { commit(); thumbs(); }, 300); }
  });
  document.addEventListener('change', function (e) {
    var el = e.target;
    if (el.id === 'eFile') { Array.prototype.forEach.call(el.files, addUpload); el.value = ''; }
    if (el.id === 'eSize') { var s = SIZES[el.value]; var kx = s[0] / doc.w, ky = s[1] / doc.h; doc.pages.forEach(function (p) { p.items.forEach(function (it) { it.x *= kx; it.y *= ky; if (it.type === 'text') { it.w *= kx; it.size = Math.round(it.size * Math.sqrt(kx * ky) * 10) / 10; } else { it.w *= kx; it.h *= ky; } }); }); doc.size = el.value; doc.w = s[0]; doc.h = s[1]; commit(); layout(); thumbs(); toast(T('Page size changed — everything was rescaled', '종이 크기를 바꾸고 요소를 맞춰 옮겼어요')); }
    if (el.dataset.swapfile != null && el.files[0]) { var it = item(sel), r = new FileReader(); r.onload = function () { it.src = r.result; it.hi = null; it.upload = true; it.credit = ''; commit(); refresh(); }; r.readAsDataURL(el.files[0]); }
  });
  ['dragover', 'drop'].forEach(function (ev) { stage.addEventListener(ev, function (e) { e.preventDefault(); if (ev === 'drop') Array.prototype.forEach.call(e.dataTransfer.files, addUpload); }); });

  // ---------- pages ----------
  function thumbs() {
    clearTimeout(thumbs._t); thumbs._t = setTimeout(function () {
      var F = $('ePages'), tw = 54, s = tw / doc.w, th = doc.h * s;
      F.innerHTML = doc.pages.map(function (p, i) { return '<button class="ethumb' + (i === pageIx ? ' on' : '') + '" data-pg="' + i + '"><canvas width="' + Math.round(tw * 2) + '" height="' + Math.round(th * 2) + '" style="width:' + tw + 'px;height:' + Math.round(th) + 'px"></canvas><span>' + (i + 1) + '</span></button>'; }).join('') +
        '<div class="epgact"><button data-pga="add" title="' + T('Add page', '페이지 추가') + '">＋</button><button data-pga="dup" title="' + T('Duplicate page', '페이지 복제') + '">⧉</button><button data-pga="left" title="' + T('Move left', '앞으로') + '">◀</button><button data-pga="right" title="' + T('Move right', '뒤로') + '">▶</button><button data-pga="del" title="' + T('Delete page', '페이지 삭제') + '">🗑</button></div>';
      F.querySelectorAll('canvas').forEach(function (c, i) { renderPage(c.getContext('2d'), doc.pages[i], s * 2, false); });
    }, 120);
  }
  function pageAct(a) {
    var P = doc.pages;
    if (a === 'add') { P.splice(pageIx + 1, 0, blankPage()); pageIx++; }
    if (a === 'dup') { var c = clone(page()); c.id = uid(); c.items.forEach(function (q) { q.id = uid(); }); P.splice(pageIx + 1, 0, c); pageIx++; }
    if (a === 'del') { if (P.length === 1) return toast(T('A document needs one page', '페이지는 하나 이상 있어야 해요')); if (!confirm(T('Delete this page?', '이 페이지를 지울까요?'))) return; P.splice(pageIx, 1); pageIx = Math.max(0, pageIx - 1); }
    if (a === 'left' && pageIx > 0) { P.splice(pageIx - 1, 0, P.splice(pageIx, 1)[0]); pageIx--; }
    if (a === 'right' && pageIx < P.length - 1) { P.splice(pageIx + 1, 0, P.splice(pageIx, 1)[0]); pageIx++; }
    sel = null; commit(); refresh();
  }
  function refresh() { $('eTitle').value = doc.title || ''; $('eSize').value = doc.size; props(); if (tab === 'layers') layersPanel(); thumbs(); draw(); }

  // ---------- fonts ----------
  var loaded = {};
  function loadFont(f) { if (loaded[f]) return loaded[f]; return loaded[f] = (document.fonts && document.fonts.load ? Promise.all([document.fonts.load('400 20px "' + f + '"'), document.fonts.load('700 20px "' + f + '"'), document.fonts.load('italic 400 20px "' + f + '"')]).catch(function () { }) : Promise.resolve()); }
  function docFonts() { var s = {}; doc.pages.forEach(function (p) { p.items.forEach(function (it) { if (it.font) s[it.font] = 1; if (it.type === 'cal') s['Josefin Sans'] = 1; }); }); return Promise.all(Object.keys(s).map(loadFont)); }

  // ---------- export ----------
  function exportDialog() {
    var M = $('eModal'); M.hidden = false;
    M.innerHTML = '<div class="ebox"><h2>' + T('Download', '다운로드') + '</h2>' +
      '<div class="eopts"><label><input type="radio" name="ef" value="pdf" checked> <b>PDF</b> — ' + T('all pages, ready to print', '모든 페이지, 바로 인쇄') + '</label><label><input type="radio" name="ef" value="png"> <b>PNG</b> — ' + T('this page as an image', '이 페이지를 이미지로') + '</label><label><input type="radio" name="ef" value="pngall"> <b>PNG</b> — ' + T('every page', '모든 페이지') + '</label></div>' +
      '<label class="echk"><input type="checkbox" id="eBleed"> ' + T('Add 3 mm bleed and crop marks (for print shops)', '인쇄소용 여백 3mm와 재단선 넣기') + '</label>' +
      (unlocked ? '<p class="eok">✓ ' + T('Full quality ' + fullDpi() + ' dpi, no watermark', fullDpi() + 'dpi 고화질, 워터마크 없음') + (fullDpi() < 300 ? ' — ' + T('ideal for a wall poster', '벽에 거는 포스터에 알맞은 선명도예요') : '') + '</p>' : '<div class="elockbox"><p>' + T('Free preview: 100 dpi with a watermark. Buyers and members get full 300 dpi files.', '무료 미리보기는 100dpi에 워터마크가 들어가요. 구매자와 회원은 워터마크 없는 300dpi로 받아요.') + '</p><div class="erow"><input id="eKey" placeholder="' + T('License key from your receipt', '구매 영수증의 라이선스 키') + '"><button class="ebtn" id="eUnlock">' + T('Unlock', '잠금 해제') + '</button></div><p class="esmall">' + T('Find the key in your purchase email or receipt page.', '키는 구매 확인 이메일이나 영수증 화면에 있어요.') + '</p></div>') +
      '<div class="erow end"><button class="ebtn ghost" id="eCancel">' + T('Cancel', '취소') + '</button><button class="ebtn" id="eGo">' + T('Download', '다운로드') + '</button></div><div class="eprog" id="eProg"></div></div>';
    $('eCancel').onclick = function () { M.hidden = true; };
    if ($('eUnlock')) $('eUnlock').onclick = function () { checkKey($('eKey').value.trim()).then(function (ok) { if (ok) exportDialog(); }); };
    $('eGo').onclick = function () { var f = M.querySelector('input[name=ef]:checked').value; doExport(f, $('eBleed').checked).then(function () { M.hidden = true; }); };
  }
  function pageCanvas(pg, dpi, bleed) {
    var s = dpi / 25.4, b = bleed ? 3 : 0, c = document.createElement('canvas'); c.width = Math.round((doc.w + b * 2) * s); c.height = Math.round((doc.h + b * 2) * s);
    var x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height);
    if (b) { x.save(); x.translate(b * s, b * s); var sx = (doc.w + 2 * b) / doc.w; x.translate(-b * s, -b * s); x.scale(sx, (doc.h + 2 * b) / doc.h); renderPage(x, pg, s, true); x.restore(); marks(x, s, b); } else renderPage(x, pg, s, true);
    if (!unlocked) wm(x, c.width, c.height, 0.16);
    return c;
  }
  function marks(x, s, b) { x.save(); x.strokeStyle = '#000'; x.lineWidth = 0.25 * s; var W = (doc.w + 2 * b) * s, H = (doc.h + 2 * b) * s, o = b * s, L = 2.5 * s; [[o, 0, o, L], [0, o, L, o], [W - o, 0, W - o, L], [W, o, W - L, o], [o, H, o, H - L], [0, H - o, L, H - o], [W - o, H, W - o, H - L], [W, H - o, W - L, H - o]].forEach(function (l) { x.beginPath(); x.moveTo(l[0], l[1]); x.lineTo(l[2], l[3]); x.stroke(); }); x.restore(); }
  function waitImgs() { var srcs = []; doc.pages.forEach(function (p) { if (p.bg && p.bg.src) srcs.push(p.bg.src); if (p.bg && p.bg.hi && unlocked) srcs.push(p.bg.hi); p.items.forEach(function (it) { if (it.src) srcs.push(it.src); if (it.hi && unlocked) srcs.push(it.hi); }); }); srcs.forEach(img); return new Promise(function (res) { var t0 = Date.now(); (function chk() { var left = srcs.filter(function (s) { var c = IMG[s]; return c && !c.ok && !c.bad; }); if (!left.length || Date.now() - t0 > 20000) res(); else setTimeout(chk, 200); })(); }); }
  function doExport(f, bleed) {
    var dpi = unlocked ? fullDpi() : 100, prog = $('eProg'), name = (doc.title || 'arttrip').replace(/[^\w\-가-힣 ]+/g, '').trim().replace(/\s+/g, '_') || 'arttrip';
    prog.textContent = T('Preparing images…', '그림을 준비하는 중…');
    return Promise.all([docFonts(), waitImgs()]).then(function () {
      if (f === 'png') { prog.textContent = T('Rendering…', '만드는 중…'); return blobDl(pageCanvas(page(), dpi, bleed), name + '_p' + (pageIx + 1) + '.png'); }
      if (f === 'pngall') { var i = 0; return (function next() { if (i >= doc.pages.length) return Promise.resolve(); prog.textContent = (i + 1) + ' / ' + doc.pages.length; var c = pageCanvas(doc.pages[i], dpi, bleed); i++; return blobDl(c, name + '_p' + i + '.png').then(function () { return new Promise(function (r) { setTimeout(r, 400); }); }).then(next); })(); }
      return loadPdf().then(function () {
        var b = bleed ? 3 : 0, W = doc.w + 2 * b, H = doc.h + 2 * b, pdf = new window.jspdf.jsPDF({ unit: 'mm', format: [W, H], orientation: W > H ? 'l' : 'p', compress: true });
        doc.pages.forEach(function (p, i) { prog.textContent = T('Page ', '페이지 ') + (i + 1) + ' / ' + doc.pages.length; if (i) pdf.addPage([W, H], W > H ? 'l' : 'p'); var c = pageCanvas(p, dpi, bleed); pdf.addImage(c.toDataURL('image/jpeg', 0.92), 'JPEG', 0, 0, W, H, undefined, 'FAST'); });
        pdf.setProperties({ title: doc.title || 'Arttrip', creator: 'Arttrip Studio Editor' }); pdf.save(name + '.pdf');
      });
    }).then(function () { toast(T('Downloaded', '다운로드했어요')); });
  }
  function blobDl(c, fn) { return new Promise(function (res) { c.toBlob(function (bl) { var a = document.createElement('a'); a.href = URL.createObjectURL(bl); a.download = fn; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); res(); }, 300); }, 'image/png'); }); }
  var pdfP = null; function loadPdf() { return pdfP || (pdfP = new Promise(function (res, rej) { var s = document.createElement('script'); s.src = '/editor/jspdf.umd.min.js'; s.onload = res; s.onerror = rej; document.head.appendChild(s); })); }

  // ---------- unlock ----------
  function checkKey(k) {
    if (!k) return Promise.resolve(false);
    return fetch('/api/license', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ key: k }) }).then(function (r) { return r.json(); }).then(function (j) {
      if (j.ok) { unlocked = true; try { localStorage.setItem('at_key', k); } catch (e) { } lockUI(); draw(); toast(T('Unlocked — thank you!', '잠금이 풀렸어요. 고마워요!')); return true; }
      toast(T('That key did not work', '키가 맞지 않아요')); return false;
    }).catch(function () { toast(T('Could not check the key', '키를 확인하지 못했어요')); return false; });
  }
  function lockUI() { $('eLock').innerHTML = unlocked ? '<span class="eok">● ' + T('Full quality', '고화질') + '</span>' : '<button class="elockbtn" id="bLock">🔒 ' + T('Preview mode', '미리보기 모드') + '</button>'; if ($('bLock')) $('bLock').onclick = exportDialog; }

  // ---------- save ----------
  var DB = null;
  function idb() { return DB || (DB = new Promise(function (res, rej) { var r = indexedDB.open('arttrip-editor', 1); r.onupgradeneeded = function () { r.result.createObjectStore('docs'); }; r.onsuccess = function () { res(r.result); }; r.onerror = rej; })); }
  function autosave() { clearTimeout(autosave._t); autosave._t = setTimeout(function () { idb().then(function (db) { db.transaction('docs', 'readwrite').objectStore('docs').put(lastSnap || JSON.stringify(doc), docKey); }).catch(function () { }); }, 600); }
  function loadLocal() { return idb().then(function (db) { return new Promise(function (res) { var r = db.transaction('docs').objectStore('docs').get(docKey); r.onsuccess = function () { res(r.result ? JSON.parse(r.result) : null); }; r.onerror = function () { res(null); }; }); }).catch(function () { return null; }); }
  function save() {
    autosave();
    fetch('/api/me').then(function (r) { return r.ok ? r.json() : { user: null }; }).catch(function () { return { user: null }; }).then(function (m) {
      if (!m.user) { toast(T('Saved on this device. Sign in to keep it in your account.', '이 기기에 저장했어요. 로그인하면 계정에도 저장돼요.')); return; }
      var s = JSON.stringify(doc); if (s.indexOf('data:image') >= 0) { toast(T('Saved on this device (designs with your own photos stay on the device)', '이 기기에 저장했어요 (내 사진이 들어간 작업은 기기에만 저장돼요)')); return; }
      fetch('/api/designs', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ id: save.id, tool: 'editor', title: doc.title, state: doc }) }).then(function (r) { return r.json(); }).then(function (j) { if (j.id) { save.id = j.id; toast(T('Saved to your account', '계정에 저장했어요')); } else toast(T('Saved on this device', '이 기기에 저장했어요')); });
    });
  }

  // ---------- boot ----------
  var q = new URLSearchParams(location.search), docKey = 'doc:' + (q.get('tpl') || q.get('cal') || 'free');
  try { var k0 = localStorage.getItem('at_key'); if (k0) checkKey(k0); } catch (e) { }
  lockUI();
  fetch('/api/me').then(function (r) { return r.ok ? r.json() : {}; }).then(function (m) { if (m && m.user && m.user.plan === 'member') { unlocked = true; lockUI(); } }).catch(function () { });
  fetch('/api/art.json?all=1').then(function (r) { return r.json(); }).then(function (rows) {
    LIB = rows.map(function (r) { return { id: r.id, t: ko && r.tk ? r.tk : r.t, a: ko && r.ak ? r.ak : r.a, tk: r.tk, ak: r.ak, theme: r.theme, as: r.as, w: r.w, h: r.h }; });
    return loadLocal();
  }).then(function (saved) {
    doc = newDoc(q.get('size') || (ko ? 'A4' : 'Letter'));
    if (saved && !q.get('new')) doc = saved;
    else if (q.get('cal')) calendarDoc(q.get('cal'), doc.size);
    else if (q.get('tpl')) { var t = PAPER_TPL.find(function (x) { return x.id === q.get('tpl'); }); if (t) doc.pages = [paperPage(t)]; }
    else { var t2 = PAPER_TPL[0]; doc.pages = [paperPage(t2)]; doc.title = T('My art paper', '나의 아트페이퍼'); }
    lastSnap = JSON.stringify(doc); panel(); layout(); refresh(); docFonts().then(draw);
  });
  if (q.get('build') && /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) window.ATE = {
    list: PAPER_TPL.map(function (t) { return t.id; }),
    make: function (id, size) { doc = newDoc(size); var t = PAPER_TPL.find(function (x) { return x.id === id; }); doc.pages = [paperPage(t)]; pageIx = 0; unlocked = true; return Promise.all([docFonts(), waitImgs()]).then(function () { return new Promise(function (r) { setTimeout(r, 300); }); }); },
    jpg: function (dpi) { return pageCanvas(page(), dpi, false).toDataURL('image/jpeg', 0.92); }
  };
  window.addEventListener('resize', function () { layout(); });
  if (window.ResizeObserver) new ResizeObserver(function () { if (doc) layout(); }).observe(stage);
  document.addEventListener('click', function (e) { if (window.innerWidth < 900 && !e.target.closest('.epanel') && !e.target.closest('.erail')) document.body.classList.remove('epanel-open'); });
})();
