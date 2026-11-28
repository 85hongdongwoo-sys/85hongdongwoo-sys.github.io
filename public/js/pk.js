/* Arttrip catalogue PDF builder: runs in the buyer's browser after the licence key is accepted. */
var PK = (function () {
  var SIZES = { A4: [210, 297], Letter: [215.9, 279.4], A3: [297, 420] };
  var MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DOW = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var O = {}, st;
  function say(m) { st.textContent = m; }
  function load(u, maxPx, mode) {
    return new Promise(function (res, rej) {
      var im = new Image(); im.crossOrigin = 'anonymous';
      im.onload = function () {
        var s = Math.min(1, maxPx / Math.max(im.naturalWidth, im.naturalHeight)), w = Math.round(im.naturalWidth * s), h = Math.round(im.naturalHeight * s);
        var c = document.createElement('canvas'); c.width = w; c.height = h; var x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, w, h); x.drawImage(im, 0, 0, w, h);
        if (mode === 'line') lineArt(x, w, h);
        res({ d: c.toDataURL(mode === 'line' ? 'image/png' : 'image/jpeg', 0.9), w: w, h: h, f: mode === 'line' ? 'PNG' : 'JPEG' });
      };
      im.onerror = function () { rej(new Error('image')); };
      im.src = u;
    });
  }
  // turn an engraving / drawing into clean black lines on white (local adaptive threshold)
  function lineArt(x, w, h) {
    var id = x.getImageData(0, 0, w, h), d = id.data, n = w * h, g = new Float32Array(n), i;
    for (i = 0; i < n; i++) g[i] = 0.299 * d[i * 4] + 0.587 * d[i * 4 + 1] + 0.114 * d[i * 4 + 2];
    var I = new Float64Array((w + 1) * (h + 1)), r = Math.max(6, Math.round(Math.min(w, h) / 60)), y, xx;
    for (y = 0; y < h; y++) { var row = 0; for (xx = 0; xx < w; xx++) { row += g[y * w + xx]; I[(y + 1) * (w + 1) + xx + 1] = I[y * (w + 1) + xx + 1] + row; } }
    for (y = 0; y < h; y++) for (xx = 0; xx < w; xx++) {
      var a = Math.max(0, xx - r), b = Math.max(0, y - r), c2 = Math.min(w, xx + r + 1), e = Math.min(h, y + r + 1);
      var m = (I[e * (w + 1) + c2] - I[b * (w + 1) + c2] - I[e * (w + 1) + a] + I[b * (w + 1) + a]) / ((c2 - a) * (e - b));
      var v = g[y * w + xx] < m - 12 ? 0 : 255, k = (y * w + xx) * 4; d[k] = d[k + 1] = d[k + 2] = v; d[k + 3] = 255;
    }
    x.putImageData(id, 0, 0);
  }
  function fit(iw, ih, bw, bh) { var s = Math.min(bw / iw, bh / ih); return [iw * s, ih * s]; }
  function caption(p, t, x, y, w, size, align) { p.setFontSize(size); var s = p.splitTextToSize(t, w); p.text(s.slice(0, 2), x, y, { align: align || 'center' }); }
  function grid(p, m, x, y, w, h, Y) {
    var first = new Date(Y, m, 1).getDay(), days = new Date(Y, m + 1, 0).getDate(), rows = Math.ceil((first + days) / 7), cw = w / 7, rh = (h - 7) / rows;
    p.setFont('helvetica', 'bold'); p.setFontSize(8); p.setTextColor(120, 100, 80);
    for (var i = 0; i < 7; i++) p.text(DOW[i].toUpperCase(), x + cw * i + cw / 2, y + 4, { align: 'center' });
    p.setDrawColor(210, 200, 185); p.setLineWidth(0.2); p.setFont('helvetica', 'normal');
    for (var r = 0; r <= rows; r++) p.line(x, y + 7 + rh * r, x + w, y + 7 + rh * r);
    for (var dd = 1; dd <= days; dd++) { var k = first + dd - 1, cx = x + cw * (k % 7), cy = y + 7 + rh * Math.floor(k / 7); p.setTextColor(k % 7 === 0 ? 170 : 50, k % 7 === 0 ? 60 : 44, k % 7 === 0 ? 50 : 36); p.setFontSize(10); p.text(String(dd), cx + 2, cy + 5); }
    p.setTextColor(0, 0, 0);
  }
  function build(k, works, imgs, size, title, Y) {
    Y = Y || 2027; title = String(title).replace(/2027/g, Y);
    var S = SIZES[size], W = S[0], H = S[1], jp = window.jspdf.jsPDF, p = new jp({ unit: 'mm', format: [W, H] }), M = 12;
    function page(first) { if (!first) p.addPage([W, H]); }
    if (k === 'cal') {
      var a = imgs[0], f = fit(a.w, a.h, W - 2 * M, H * 0.66);
      p.addImage(a.d, a.f, (W - f[0]) / 2, M + 4, f[0], f[1]); p.setFont('times', 'normal'); p.setFontSize(30); p.text(String(Y), W / 2, H * 0.8, { align: 'center' }); p.setFontSize(15); caption(p, title, W / 2, H * 0.86, W - 2 * M, 15);
      for (var m = 0; m < 12; m++) {
        page(false); var im = imgs[(m + 1) % imgs.length], w0 = works[(m + 1) % works.length], ih = H * 0.52, ff = fit(im.w, im.h, W - 2 * M, ih);
        p.addImage(im.d, im.f, (W - ff[0]) / 2, M + (ih - ff[1]) / 2, ff[0], ff[1]); p.setFont('helvetica', 'italic'); p.setTextColor(110, 100, 90); caption(p, w0.t + (w0.a ? ' — ' + w0.a : ''), W / 2, M + ih + 5, W - 2 * M, 7.5); p.setTextColor(0, 0, 0);
        p.setFont('times', 'normal'); p.setFontSize(24); p.text(MON[m] + ' ' + Y, M, M + ih + 18); grid(p, m, M, M + ih + 22, W - 2 * M, H - (M + ih + 22) - M, Y);
      }

    } else if (k === 'planner') {
      var a0 = imgs[0], f0 = fit(a0.w, a0.h, W - 2 * M, H * 0.62);
      p.addImage(a0.d, a0.f, (W - f0[0]) / 2, M + 6, f0[0], f0[1]); p.setFont('times', 'normal'); p.setFontSize(34); p.text(Y + ' Planner', W / 2, H * 0.8, { align: 'center' }); p.setFontSize(13); caption(p, title, W / 2, H * 0.86, W - 2 * M, 13);
      // year at a glance
      page(false); p.setFont('times', 'normal'); p.setFontSize(24); p.text(Y + ' at a glance', M, M + 8);
      var gw = (W - 2 * M) / 3, gh = (H - 2 * M - 16) / 4;
      for (var mm = 0; mm < 12; mm++) { var gx = M + gw * (mm % 3), gy = M + 16 + gh * Math.floor(mm / 3); p.setFont('helvetica', 'bold'); p.setFontSize(10); p.setTextColor(120, 60, 50); p.text(MON[mm], gx + 2, gy + 5); p.setTextColor(0);
        var f1 = new Date(Y, mm, 1).getDay(), d1 = new Date(Y, mm + 1, 0).getDate(), cw2 = (gw - 6) / 7; p.setFont('helvetica', 'normal'); p.setFontSize(7);
        for (var q = 0; q < 7; q++) p.text('SMTWTFS'[q], gx + 2 + cw2 * q + cw2 / 2, gy + 11, { align: 'center' });
        for (var dd = 1; dd <= d1; dd++) { var kk = f1 + dd - 1; p.text(String(dd), gx + 2 + cw2 * (kk % 7) + cw2 / 2, gy + 16 + 5 * Math.floor(kk / 7), { align: 'center' }); } }
      for (var m2 = 0; m2 < 12; m2++) {
        page(false); var im2 = imgs[(m2 + 1) % imgs.length], w2 = works[(m2 + 1) % works.length], ff2 = fit(im2.w, im2.h, W - 2 * M, H - 2 * M - 22);
        p.addImage(im2.d, im2.f, (W - ff2[0]) / 2, M + (H - 2 * M - 22 - ff2[1]) / 2, ff2[0], ff2[1]); p.setFont('times', 'normal'); p.setFontSize(26); p.text(MON[m2], W / 2, H - M - 8, { align: 'center' });
        p.setFont('helvetica', 'italic'); p.setFontSize(8); p.setTextColor(110); caption(p, w2.t + (w2.a ? ' — ' + w2.a : ''), W / 2, H - M - 1, W - 2 * M, 8); p.setTextColor(0);
        page(false); p.setFont('times', 'normal'); p.setFontSize(24); p.text(MON[m2] + ' ' + Y, M, M + 8); grid(p, m2, M, M + 14, W - 2 * M, H * 0.62, Y);
        p.setFont('helvetica', 'bold'); p.setFontSize(10); p.setTextColor(120, 100, 80); p.text('NOTES & GOALS', M, M + 14 + H * 0.62 + 10); p.setTextColor(0); p.setDrawColor(215, 205, 190); p.setLineWidth(0.2);
        for (var ln = M + 14 + H * 0.62 + 18; ln < H - M; ln += 8) p.line(M, ln, W - M, ln);
        // weekly pages for this month (weeks that start in this month)
        var d0 = new Date(Y, m2, 1); while (d0.getDay() !== 1) d0.setDate(d0.getDate() + 1);
        for (; d0.getMonth() === m2; d0.setDate(d0.getDate() + 7)) {
          page(false); p.setFont('times', 'normal'); p.setFontSize(18); var e0 = new Date(d0); e0.setDate(e0.getDate() + 6);
          p.text('Week of ' + MON[d0.getMonth()].slice(0, 3) + ' ' + d0.getDate() + ' – ' + MON[e0.getMonth()].slice(0, 3) + ' ' + e0.getDate() + ', ' + Y, M, M + 8);
          var rows2 = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Notes'], rh2 = (H - 2 * M - 14) / rows2.length;
          rows2.forEach(function (nm, ri) { var yy = M + 14 + rh2 * ri; p.setDrawColor(190, 175, 155); p.setLineWidth(0.4); p.line(M, yy, W - M, yy); p.setFont('helvetica', 'bold'); p.setFontSize(10); p.setTextColor(120, 60, 50); p.text(nm.toUpperCase(), M, yy + 5); p.setTextColor(0);
            if (ri < 7) { var dt = new Date(d0); dt.setDate(dt.getDate() + ri); p.setFont('helvetica', 'normal'); p.text(String(dt.getDate()), W - M, yy + 5, { align: 'right' }); }
            p.setDrawColor(225, 218, 205); p.setLineWidth(0.15); for (var l2 = yy + 12; l2 < yy + rh2 - 2; l2 += 7) p.line(M, l2, W - M, l2); });
        }
      }
    } else if (k === 'prints') {
      imgs.forEach(function (im, i) { page(i === 0); var w0 = works[i], ff = fit(im.w, im.h, W - 2 * M, H - 2 * M - 14); p.addImage(im.d, im.f, (W - ff[0]) / 2, M + (H - 2 * M - 14 - ff[1]) / 2, ff[0], ff[1]); p.setFont('helvetica', 'normal'); p.setTextColor(90, 85, 80); caption(p, w0.t + (w0.d ? ', ' + w0.d : '') + (w0.a ? ' — ' + w0.a : ''), W / 2, H - M - 4, W - 2 * M, 8); p.setTextColor(0, 0, 0); });
    } else if (k === 'cards') {
      var cw = W / 2, ch = H / 2;
      imgs.forEach(function (im, i) {
        if (i % 4 === 0) { page(i === 0); p.setDrawColor(170); p.setLineWidth(0.15); p.setLineDashPattern([1.5, 1.5], 0); p.line(cw, 0, cw, H); p.line(0, ch, W, ch); p.setLineDashPattern([], 0); }
        var q = i % 4, x0 = (q % 2) * cw, y0 = Math.floor(q / 2) * ch, pad = 7, ff = fit(im.w, im.h, cw - 2 * pad, ch - 2 * pad - 8);
        p.addImage(im.d, im.f, x0 + (cw - ff[0]) / 2, y0 + pad + (ch - 2 * pad - 8 - ff[1]) / 2, ff[0], ff[1]); p.setFont('helvetica', 'normal'); p.setTextColor(110); caption(p, works[i].t, x0 + cw / 2, y0 + ch - pad - 2, cw - 2 * pad, 6.5); p.setTextColor(0);
      });
    } else {
      p.setFont('times', 'normal'); p.setFontSize(28); caption(p, title, W / 2, H * 0.4, W - 2 * M, 26); p.setFontSize(12); p.text('Arttrip Studio', W / 2, H * 0.55, { align: 'center' });
      imgs.forEach(function (im, i) { page(false); var w0 = works[i], ff = fit(im.w, im.h, W - 2 * M, H - 2 * M - 12); p.addImage(im.d, im.f, (W - ff[0]) / 2, M + (H - 2 * M - 12 - ff[1]) / 2, ff[0], ff[1]); p.setFont('helvetica', 'normal'); p.setTextColor(120); caption(p, w0.t + (w0.a ? ' — ' + w0.a : ''), W / 2, H - M, W - 2 * M, 7); p.setTextColor(0); });
    }
    return p;
  }

  // ---------- large-print puzzle books (generated from a fixed seed, so every copy of a book is identical) ----------
  function rng(seed) { var a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function shuffle(a, R) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(R() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function wordSearch(words, size, R, hard) {
    var dirs = hard ? [[0, 1], [1, 0], [1, 1], [-1, 1], [0, -1], [-1, 0]] : [[0, 1], [1, 0], [1, 1]];
    for (var tries = 0; tries < 60; tries++) {
      var g = [], placed = [], i, r, c; for (r = 0; r < size; r++) { g.push([]); for (c = 0; c < size; c++) g[r].push(''); }
      var list = shuffle(words.filter(function (w) { return w.length <= size; }).slice(), R);
      for (i = 0; i < list.length && placed.length < 14; i++) {
        var w = list[i], ok = false;
        for (var k = 0; k < 120 && !ok; k++) {
          var d = dirs[Math.floor(R() * dirs.length)], r0 = Math.floor(R() * size), c0 = Math.floor(R() * size), rr = r0 + d[0] * (w.length - 1), cc = c0 + d[1] * (w.length - 1);
          if (rr < 0 || rr >= size || cc < 0 || cc >= size) continue; var fits = true;
          for (var q = 0; q < w.length; q++) { var x = g[r0 + d[0] * q][c0 + d[1] * q]; if (x && x !== w[q]) { fits = false; break; } }
          if (!fits) continue; for (q = 0; q < w.length; q++) g[r0 + d[0] * q][c0 + d[1] * q] = w[q]; placed.push({ w: w, r: r0, c: c0, d: d }); ok = true;
        }
      }
      if (placed.length >= 10) { var AL = 'ABCDEFGHIJKLMNOPRSTUW'; for (r = 0; r < size; r++) for (c = 0; c < size; c++) if (!g[r][c]) g[r][c] = AL[Math.floor(R() * AL.length)]; return { g: g, placed: placed }; }
    }
    return null;
  }
  function sudoku(R, givens) {
    var b = new Array(81).fill(0);
    function okAt(b, i, v) { var r = Math.floor(i / 9), c = i % 9, br = r - r % 3, bc = c - c % 3; for (var k = 0; k < 9; k++) { if (b[r * 9 + k] === v || b[k * 9 + c] === v || b[(br + Math.floor(k / 3)) * 9 + bc + k % 3] === v) return false; } return true; }
    function fill(i) { if (i === 81) return true; var vs = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9], R); for (var k = 0; k < 9; k++) { if (okAt(b, i, vs[k])) { b[i] = vs[k]; if (fill(i + 1)) return true; } } b[i] = 0; return false; }
    fill(0); var sol = b.slice(), puz = b.slice();
    function count(p, lim) { var i = p.indexOf(0); if (i < 0) return 1; var n = 0; for (var v = 1; v <= 9 && n < lim; v++) if (okAt(p, i, v)) { p[i] = v; n += count(p, lim - n); p[i] = 0; } return n; }
    var order = shuffle(Array.from({ length: 81 }, function (_, i) { return i; }), R), left = 81;
    for (var k = 0; k < 81 && left > givens; k++) { var i = order[k], keep = puz[i]; puz[i] = 0; if (count(puz.slice(), 2) !== 1) puz[i] = keep; else left--; }
    return { p: puz, s: sol };
  }
  function maze(cols, rows, R) {
    var cells = [], i, st = [0], seen = new Array(cols * rows).fill(false); for (i = 0; i < cols * rows; i++) cells.push({ n: 1, s: 1, e: 1, w: 1 }); seen[0] = true;
    while (st.length) { var cur = st[st.length - 1], x = cur % cols, y = Math.floor(cur / cols), nb = [];
      if (y > 0 && !seen[cur - cols]) nb.push(['n', cur - cols]); if (y < rows - 1 && !seen[cur + cols]) nb.push(['s', cur + cols]); if (x < cols - 1 && !seen[cur + 1]) nb.push(['e', cur + 1]); if (x > 0 && !seen[cur - 1]) nb.push(['w', cur - 1]);
      if (!nb.length) { st.pop(); continue; } var pk = nb[Math.floor(R() * nb.length)], opp = { n: 's', s: 'n', e: 'w', w: 'e' }; cells[cur][pk[0]] = 0; cells[pk[1]][opp[pk[0]]] = 0; seen[pk[1]] = true; st.push(pk[1]); }
    // solution path (BFS)
    var prev = new Array(cols * rows).fill(-1), q = [0], dir = { n: -cols, s: cols, e: 1, w: -1 }; prev[0] = 0;
    while (q.length) { var u = q.shift(); ['n', 's', 'e', 'w'].forEach(function (d) { if (!cells[u][d]) { var v = u + dir[d]; if (prev[v] < 0) { prev[v] = u; q.push(v); } } }); }
    var path = [], t = cols * rows - 1; while (t !== 0) { path.push(t); t = prev[t]; } path.push(0);
    return { cells: cells, path: path.reverse() };
  }

  function scramble(w, R) { var a = w.split(''), t = 0, out; do { out = shuffle(a.slice(), R).join(''); t++; } while (out === w && t < 10); return out; }
  function numSearch(size, R) {
    var g = [], r, c; for (r = 0; r < size; r++) { g.push([]); for (c = 0; c < size; c++) g[r].push(''); }
    var dirs = [[0, 1], [1, 0], [1, 1]], placed = [];
    for (var t = 0; t < 400 && placed.length < 14; t++) { var L = 4 + Math.floor(R() * 4), n = ''; for (var i = 0; i < L; i++) n += Math.floor(R() * 10); var d = dirs[Math.floor(R() * 3)], r0 = Math.floor(R() * size), c0 = Math.floor(R() * size), rr = r0 + d[0] * (L - 1), cc = c0 + d[1] * (L - 1);
      if (rr >= size || cc >= size) continue; var ok = true; for (i = 0; i < L; i++) { var x = g[r0 + d[0] * i][c0 + d[1] * i]; if (x && x !== n[i]) { ok = false; break; } } if (!ok) continue;
      for (i = 0; i < L; i++) g[r0 + d[0] * i][c0 + d[1] * i] = n[i]; placed.push({ w: n, r: r0, c: c0, d: d }); }
    for (r = 0; r < size; r++) for (c = 0; c < size; c++) if (!g[r][c]) g[r][c] = String(Math.floor(R() * 10)); return { g: g, placed: placed };
  }
  function cipher(R) { var A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''), B; do { B = shuffle(A.slice(), R); } while (B.some(function (x, i) { return x === A[i]; })); var m = {}; A.forEach(function (x, i) { m[x] = B[i]; }); return m; }
  function buildPuz(pz, size, title) {
    var S = SIZES[size], W = S[0], H = S[1], p = new window.jspdf.jsPDF({ unit: 'mm', format: [W, H] }), M = 14, R = rng(pz.seed), n = pz.n || 30, ans = [];
    p.setFont('helvetica', 'bold'); p.setFontSize(30); caption(p, title, W / 2, H * 0.36, W - 2 * M, 30); p.setFont('helvetica', 'normal'); p.setFontSize(14); p.text('Large print · ' + n + ' puzzles · answers at the back', W / 2, H * 0.5, { align: 'center' }); p.text('Arttrip Studio', W / 2, H * 0.9, { align: 'center' });
    for (var k = 1; k <= n; k++) {
      var ty = pz.type === 'mix' ? ['ws', 'sudoku', 'maze', 'scramble', 'numsearch', 'crypto'][(k - 1) % 6] : pz.type;
      p.addPage([W, H]); p.setFont('helvetica', 'bold'); p.setFontSize(20); p.text(({ ws: pz.theme || 'Word Search', sudoku: 'Sudoku', maze: 'Maze', scramble: 'Word Scramble' + (pz.theme ? ': ' + pz.theme : ''), numsearch: 'Number Search', crypto: 'Cryptogram' })[ty] + ' — ' + k, M, M + 6);
      if (ty === 'scramble') {
        var wl = shuffle(pz.words.slice(), R).slice(0, 15); p.setFont('helvetica', 'normal'); p.setFontSize(12); p.text('Unscramble each word. Hint: they are all about ' + (pz.theme || 'everyday things').toLowerCase() + '.', M, M + 16);
        wl.forEach(function (w, i) { var yy = M + 30 + i * ((H - M - 40) / 15); p.setFont('courier', 'bold'); p.setFontSize(20); p.text(scramble(w, R).split('').join(' '), M, yy); p.setDrawColor(150); p.setLineWidth(0.3); p.line(W / 2 + 5, yy + 1, W - M, yy + 1); });
        ans.push({ k: k, t: 'list', d: wl });
      } else if (ty === 'numsearch') {
        var nsz = 12, ns = numSearch(nsz, R), ncell = Math.min((W - 2 * M) / nsz, (H * 0.6) / nsz), nx0 = (W - ncell * nsz) / 2, ny0 = M + 16;
        p.setFont('courier', 'bold'); p.setFontSize(ncell * 2.0); for (var r3 = 0; r3 < nsz; r3++) for (var c4 = 0; c4 < nsz; c4++) p.text(ns.g[r3][c4], nx0 + ncell * c4 + ncell / 2, ny0 + ncell * r3 + ncell * 0.72, { align: 'center' });
        p.setDrawColor(120); p.setLineWidth(0.4); p.rect(nx0 - 2, ny0 - 2, ncell * nsz + 4, ncell * nsz + 4); p.setFont('helvetica', 'bold'); p.setFontSize(15);
        ns.placed.map(function (o) { return o.w; }).forEach(function (w, i) { p.text(w, M + (W - 2 * M) / 3 * (i % 3), ny0 + ncell * nsz + 14 + 9 * Math.floor(i / 3)); });
        ans.push({ k: k, t: 'ws', d: ns });
      } else if (ty === 'crypto') {
        var qs = pz.quotes || ['A JOURNEY OF A THOUSAND MILES BEGINS WITH A SINGLE STEP|LAO TZU'], qq = qs[Math.floor(R() * qs.length)].split('|'), cm = cipher(R), enc = qq[0].replace(/[A-Z]/g, function (ch) { return cm[ch]; });
        p.setFont('helvetica', 'normal'); p.setFontSize(12); p.text('Each letter stands for another letter. Crack the code to reveal a famous saying.', M, M + 16);
        var lines = p.splitTextToSize(enc, W - 2 * M - 10), yq = M + 40; p.setFont('courier', 'bold'); p.setFontSize(20);
        lines.forEach(function (ln) { p.text(ln.split('').join(' '), M, yq); p.setDrawColor(170); p.setLineWidth(0.3); p.line(M, yq + 10, W - M, yq + 10); yq += 26; });
        p.setFont('helvetica', 'italic'); p.setFontSize(13); p.text('— ' + qq[1], W - M, yq + 4, { align: 'right' });
        var hint = shuffle(Object.keys(cm).filter(function (x) { return qq[0].indexOf(x) >= 0; }), R)[0]; p.setFont('helvetica', 'normal'); p.text('Hint: ' + cm[hint] + ' = ' + hint, M, yq + 18);
        ans.push({ k: k, t: 'text', d: qq[0] + '  — ' + qq[1] });
      } else if (ty === 'ws') {
        var sz = 13, ws = wordSearch(pz.words, sz, R, pz.level === 'hard'); var cell = Math.min((W - 2 * M) / sz, (H * 0.62) / sz), x0 = (W - cell * sz) / 2, y0 = M + 16;
        p.setFont('courier', 'bold'); p.setFontSize(cell * 2.0);
        for (var r = 0; r < sz; r++) for (var c = 0; c < sz; c++) p.text(ws.g[r][c], x0 + cell * c + cell / 2, y0 + cell * r + cell * 0.72, { align: 'center' });
        p.setDrawColor(120); p.setLineWidth(0.4); p.rect(x0 - 2, y0 - 2, cell * sz + 4, cell * sz + 4);
        p.setFont('helvetica', 'bold'); p.setFontSize(15); var words = ws.placed.map(function (o) { return o.w; }).sort(), colW = (W - 2 * M) / 3, yy = y0 + cell * sz + 14;
        words.forEach(function (w, i) { p.text(w, M + colW * (i % 3), yy + 9 * Math.floor(i / 3)); });
        ans.push({ k: k, t: 'ws', d: ws, cell: cell });
      } else if (ty === 'sudoku') {
        var giv = { easy: 40, medium: 33, hard: 28 }[pz.level] || 36, sd = sudoku(R, giv), cs = Math.min((W - 2 * M) / 9, (H - 60) / 9), sx = (W - cs * 9) / 2, sy = M + 20;
        drawSudoku(p, sd.p, null, sx, sy, cs); ans.push({ k: k, t: 'sudoku', d: sd });
      } else {
        var mc = pz.level === 'hard' ? 22 : pz.level === 'medium' ? 16 : 11, mr = Math.round(mc * 1.3), mz = maze(mc, mr, R), ms = Math.min((W - 2 * M) / mc, (H - 50) / mr), mx = (W - ms * mc) / 2, my = M + 20;
        drawMaze(p, mz, mc, mr, mx, my, ms, false); ans.push({ k: k, t: 'maze', d: mz, mc: mc, mr: mr });
      }
    }
    // answers: 4 per page
    for (var a = 0; a < ans.length; a++) {
      if (a % 4 === 0) { p.addPage([W, H]); p.setFont('helvetica', 'bold'); p.setFontSize(16); p.text('Answers', M, M + 4); }
      var o = ans[a], qx = M + (a % 2) * (W - 2 * M) / 2, qy = M + 12 + Math.floor((a % 4) / 2) * (H - M - 12) / 2, bw = (W - 2 * M) / 2 - 8, bh = (H - M - 12) / 2 - 14;
      p.setFont('helvetica', 'bold'); p.setFontSize(11); p.text('#' + o.k, qx, qy + 4);
      if (o.t === 'list' || o.t === 'text') { p.setFont('helvetica', 'normal'); p.setFontSize(10); var tl = o.t === 'list' ? o.d.join(', ') : o.d; p.text(p.splitTextToSize(tl, bw), qx, qy + 12); }
      else if (o.t === 'sudoku') { var c2 = Math.min(bw, bh) / 9; drawSudoku(p, o.d.s, o.d.p, qx, qy + 7, c2); }
      else if (o.t === 'maze') { var s2 = Math.min(bw / o.mc, bh / o.mr); drawMaze(p, o.d, o.mc, o.mr, qx, qy + 7, s2, true); }
      else { var g = o.d.g, n2 = g.length, c3 = Math.min(bw, bh) / n2; p.setFont('courier', 'normal'); p.setFontSize(c3 * 2); p.setTextColor(150);
        for (var r2 = 0; r2 < n2; r2++) for (var cc2 = 0; cc2 < n2; cc2++) p.text(g[r2][cc2], qx + c3 * cc2 + c3 / 2, qy + 7 + c3 * r2 + c3 * 0.72, { align: 'center' });
        p.setTextColor(0); p.setDrawColor(200, 60, 50); p.setLineWidth(c3 * 0.45); p.setLineCap && p.setLineCap('round');
        o.d.placed.forEach(function (w) { var L = w.w.length - 1; p.line(qx + c3 * w.c + c3 / 2, qy + 7 + c3 * w.r + c3 / 2, qx + c3 * (w.c + w.d[1] * L) + c3 / 2, qy + 7 + c3 * (w.r + w.d[0] * L) + c3 / 2); });
        p.setLineWidth(0.2); p.setDrawColor(0); }
    }
    return p;
  }
  function drawSudoku(p, vals, giv, x, y, cs) {
    p.setDrawColor(0); for (var i = 0; i <= 9; i++) { p.setLineWidth(i % 3 === 0 ? 0.8 : 0.2); p.line(x, y + cs * i, x + cs * 9, y + cs * i); p.line(x + cs * i, y, x + cs * i, y + cs * 9); }
    p.setFont('helvetica', 'bold'); p.setFontSize(cs * 1.9);
    for (var k = 0; k < 81; k++) if (vals[k]) { if (giv) p.setTextColor(giv[k] ? 0 : 200, giv[k] ? 0 : 60, giv[k] ? 0 : 50); p.text(String(vals[k]), x + cs * (k % 9) + cs / 2, y + cs * Math.floor(k / 9) + cs * 0.68, { align: 'center' }); }
    p.setTextColor(0);
  }
  function drawMaze(p, mz, cols, rows, x, y, s, sol) {
    p.setDrawColor(0); p.setLineWidth(Math.max(0.3, s * 0.08));
    for (var i = 0; i < cols * rows; i++) { var cx = x + s * (i % cols), cy = y + s * Math.floor(i / cols), c = mz.cells[i];
      if (c.n && i !== 0) p.line(cx, cy, cx + s, cy); if (c.w) p.line(cx, cy, cx, cy + s); if (c.s && i !== cols * rows - 1) p.line(cx, cy + s, cx + s, cy + s); if (c.e) p.line(cx + s, cy, cx + s, cy + s); }
    if (sol) { p.setDrawColor(200, 60, 50); p.setLineWidth(s * 0.25); for (var k = 1; k < mz.path.length; k++) { var a = mz.path[k - 1], b = mz.path[k]; p.line(x + s * (a % cols) + s / 2, y + s * Math.floor(a / cols) + s / 2, x + s * (b % cols) + s / 2, y + s * Math.floor(b / cols) + s / 2); } p.setDrawColor(0); }
    p.setFontSize(Math.max(8, s * 1.4)); p.text('START', x, y - 2); p.text('FINISH', x + s * cols, y + s * rows + s * 0.9, { align: 'right' });
  }
  function go() {
    var key = document.getElementById('k').value.trim(), qs = new URLSearchParams(location.search), cid = qs.get('checkout_id') || '', pass = ''; try { pass = localStorage.getItem('pkpass:' + O.slug) || ''; } catch (e) { }
    if (!key && !cid && !pass) { say(O.ko ? '라이선스 키를 넣어 주세요.' : O.ja ? 'ライセンスキーを入力してください。' : 'Please enter your licence key.'); return; }
    var size = (document.querySelector('input[name=sz]:checked') || {}).value || 'A4', Y = +((document.querySelector('input[name=yr]:checked') || {}).value || 2027), btn = document.getElementById('go'); btn.disabled = true;
    say(O.ko ? '키를 확인하는 중…' : O.ja ? 'キーを確認しています…' : 'Checking your key…');
    fetch('/api/pk/unlock', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ slug: O.slug, key: key, cid: cid, pass: pass }) }).then(function (r) { return r.json(); }).then(function (j) {
      if (j.ok && j.pass) { try { localStorage.setItem('pkpass:' + O.slug, j.pass); } catch (e) { } }
      if (!j.ok) { btn.disabled = false; say(O.ko ? '이 상품의 라이선스 키가 아니에요. 영수증 메일의 키를 다시 확인해 주세요.' : O.ja ? 'この商品のキーではありません。領収書メールのキーをご確認ください。' : 'That key is not valid for this product. Please check the key in your receipt.'); return; }
      if (j.k === 'pbn') { say(O.ko ? '도안 그리는 중…' : O.ja ? '図案を描いています…' : 'Drawing your pattern…'); PBN.unpack(j.pbn).then(function (r) { var pp = PBN.pdf(r, size, j.title, j.artist); pp.save(O.slug + '-' + size + '.pdf'); btn.disabled = false; say(O.ko ? '완료! 다운로드 폴더를 확인하세요. 다른 크기도 같은 키로 받을 수 있어요.' : O.ja ? '完了しました！ダウンロードフォルダをご確認ください。同じキーで他のサイズも作れます。' : 'Done! Check your downloads. Other sizes work with the same key.'); }); return; }
      if (j.k === 'puz') { say(O.ko ? 'PDF 만드는 중…' : O.ja ? 'PDFを作成しています…' : 'Building the PDF…'); setTimeout(function () { var pp = buildPuz(j.pz, size, j.title); pp.save(O.slug + '-' + size + '.pdf'); btn.disabled = false; say(O.ko ? '완료! 다운로드 폴더를 확인하세요.' : O.ja ? '完了しました！ダウンロードフォルダをご確認ください。' : 'Done! Check your downloads.'); }, 30); return; }
      var done = 0, maxPx = j.k === 'cards' ? 1600 : j.k === 'color' ? 2200 : 2600;
      return Promise.all(j.works.map(function (w) { return load(w.u, maxPx, j.k === 'color' ? 'line' : '').then(function (x) { done++; say((O.ko ? '그림 불러오는 중 ' : O.ja ? '画像を読み込み中 ' : 'Loading pictures ') + done + ' / ' + j.works.length); return x; }); })).then(function (imgs) {
        say(O.ko ? 'PDF 만드는 중…' : O.ja ? 'PDFを作成しています…' : 'Building the PDF…');
        var p = build(j.k, j.works, imgs, size, j.title, Y); p.save(O.slug.replace(/2027/, (j.k === 'cal' || j.k === 'planner') ? Y : 2027) + '-' + size + '.pdf'); btn.disabled = false;
        say(O.ko ? '완료! 다운로드 폴더를 확인하세요. 다른 크기와 다른 해도 같은 키로 받을 수 있어요.' : O.ja ? '完了しました！ダウンロードフォルダをご確認ください。同じキーで他のサイズや年も作れます。' : 'Done! Check your downloads. You can get other sizes and years with the same key.');
      });
    }).catch(function () { btn.disabled = false; say(O.ko ? '문제가 생겼어요. 잠시 후 다시 시도하거나 hello@arttripstudio.com 으로 연락 주세요.' : O.ja ? '問題が発生しました。少し待ってからもう一度お試しいただくか、hello@arttripstudio.com までご連絡ください。' : 'Something went wrong. Try again shortly or write to hello@arttripstudio.com.'); });
  }
  return { init: function (o) { O = o; st = document.getElementById('st'); document.getElementById('go').addEventListener('click', go);
      var has = false; try { has = !!localStorage.getItem('pkpass:' + O.slug); } catch (e) { }
      if (has || new URLSearchParams(location.search).get('checkout_id')) { var kb = document.getElementById('k'); kb.placeholder = O.ko ? '결제가 확인되면 키 없이 바로 받을 수 있어요' : O.ja ? 'お支払い直後ならキーは不要です — ボタンを押してください' : 'Paid just now? No key needed — press the button'; say(O.ko ? '결제해 주셔서 고마워요! 용지 크기를 고르고 버튼을 누르세요.' : O.ja ? 'ご購入ありがとうございます！用紙サイズを選んでボタンを押してください。' : 'Thank you for your purchase! Pick a paper size and press the button.'); } }, build: build, load: load, buildPuz: buildPuz };
})();
