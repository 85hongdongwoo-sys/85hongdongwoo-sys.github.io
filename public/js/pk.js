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
  function grid(p, m, x, y, w, h) {
    var first = new Date(2027, m, 1).getDay(), days = new Date(2027, m + 1, 0).getDate(), rows = Math.ceil((first + days) / 7), cw = w / 7, rh = (h - 7) / rows;
    p.setFont('helvetica', 'bold'); p.setFontSize(8); p.setTextColor(120, 100, 80);
    for (var i = 0; i < 7; i++) p.text(DOW[i].toUpperCase(), x + cw * i + cw / 2, y + 4, { align: 'center' });
    p.setDrawColor(210, 200, 185); p.setLineWidth(0.2); p.setFont('helvetica', 'normal');
    for (var r = 0; r <= rows; r++) p.line(x, y + 7 + rh * r, x + w, y + 7 + rh * r);
    for (var dd = 1; dd <= days; dd++) { var k = first + dd - 1, cx = x + cw * (k % 7), cy = y + 7 + rh * Math.floor(k / 7); p.setTextColor(k % 7 === 0 ? 170 : 50, k % 7 === 0 ? 60 : 44, k % 7 === 0 ? 50 : 36); p.setFontSize(10); p.text(String(dd), cx + 2, cy + 5); }
    p.setTextColor(0, 0, 0);
  }
  function build(k, works, imgs, size, title) {
    var S = SIZES[size], W = S[0], H = S[1], jp = window.jspdf.jsPDF, p = new jp({ unit: 'mm', format: [W, H] }), M = 12;
    function page(first) { if (!first) p.addPage([W, H]); }
    if (k === 'cal') {
      var a = imgs[0], f = fit(a.w, a.h, W - 2 * M, H * 0.66);
      p.addImage(a.d, a.f, (W - f[0]) / 2, M + 4, f[0], f[1]); p.setFont('times', 'normal'); p.setFontSize(30); p.text('2027', W / 2, H * 0.8, { align: 'center' }); p.setFontSize(15); caption(p, title, W / 2, H * 0.86, W - 2 * M, 15);
      for (var m = 0; m < 12; m++) {
        page(false); var im = imgs[(m + 1) % imgs.length], w0 = works[(m + 1) % works.length], ih = H * 0.52, ff = fit(im.w, im.h, W - 2 * M, ih);
        p.addImage(im.d, im.f, (W - ff[0]) / 2, M + (ih - ff[1]) / 2, ff[0], ff[1]); p.setFont('helvetica', 'italic'); p.setTextColor(110, 100, 90); caption(p, w0.t + (w0.a ? ' — ' + w0.a : ''), W / 2, M + ih + 5, W - 2 * M, 7.5); p.setTextColor(0, 0, 0);
        p.setFont('times', 'normal'); p.setFontSize(24); p.text(MON[m] + ' 2027', M, M + ih + 18); grid(p, m, M, M + ih + 22, W - 2 * M, H - (M + ih + 22) - M);
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
  function buildPuz(pz, size, title) {
    var S = SIZES[size], W = S[0], H = S[1], p = new window.jspdf.jsPDF({ unit: 'mm', format: [W, H] }), M = 14, R = rng(pz.seed), n = pz.n || 30, ans = [];
    p.setFont('helvetica', 'bold'); p.setFontSize(30); caption(p, title, W / 2, H * 0.36, W - 2 * M, 30); p.setFont('helvetica', 'normal'); p.setFontSize(14); p.text('Large print · ' + n + ' puzzles · answers at the back', W / 2, H * 0.5, { align: 'center' }); p.text('Arttrip Studio', W / 2, H * 0.9, { align: 'center' });
    for (var k = 1; k <= n; k++) {
      p.addPage([W, H]); p.setFont('helvetica', 'bold'); p.setFontSize(20); p.text((pz.type === 'ws' ? (pz.theme || 'Word search') : pz.type === 'sudoku' ? 'Sudoku' : 'Maze') + ' — ' + k, M, M + 6);
      if (pz.type === 'ws') {
        var sz = 13, ws = wordSearch(pz.words, sz, R, pz.level === 'hard'); var cell = Math.min((W - 2 * M) / sz, (H * 0.62) / sz), x0 = (W - cell * sz) / 2, y0 = M + 16;
        p.setFont('courier', 'bold'); p.setFontSize(cell * 2.0);
        for (var r = 0; r < sz; r++) for (var c = 0; c < sz; c++) p.text(ws.g[r][c], x0 + cell * c + cell / 2, y0 + cell * r + cell * 0.72, { align: 'center' });
        p.setDrawColor(120); p.setLineWidth(0.4); p.rect(x0 - 2, y0 - 2, cell * sz + 4, cell * sz + 4);
        p.setFont('helvetica', 'bold'); p.setFontSize(15); var words = ws.placed.map(function (o) { return o.w; }).sort(), colW = (W - 2 * M) / 3, yy = y0 + cell * sz + 14;
        words.forEach(function (w, i) { p.text(w, M + colW * (i % 3), yy + 9 * Math.floor(i / 3)); });
        ans.push({ k: k, t: 'ws', d: ws, cell: cell });
      } else if (pz.type === 'sudoku') {
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
      if (o.t === 'sudoku') { var c2 = Math.min(bw, bh) / 9; drawSudoku(p, o.d.s, o.d.p, qx, qy + 7, c2); }
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
    var key = document.getElementById('k').value.trim(); if (!key) { say(O.ko ? '라이선스 키를 넣어 주세요.' : 'Please enter your licence key.'); return; }
    var size = (document.querySelector('input[name=sz]:checked') || {}).value || 'A4', btn = document.getElementById('go'); btn.disabled = true;
    say(O.ko ? '키를 확인하는 중…' : 'Checking your key…');
    fetch('/api/pk/unlock', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ slug: O.slug, key: key }) }).then(function (r) { return r.json(); }).then(function (j) {
      if (!j.ok) { btn.disabled = false; say(O.ko ? '이 상품의 라이선스 키가 아니에요. 영수증 메일의 키를 다시 확인해 주세요.' : 'That key is not valid for this product. Please check the key in your receipt.'); return; }
      if (j.k === 'puz') { say(O.ko ? 'PDF 만드는 중…' : 'Building the PDF…'); setTimeout(function () { var pp = buildPuz(j.pz, size, j.title); pp.save(O.slug + '-' + size + '.pdf'); btn.disabled = false; say(O.ko ? '완료! 다운로드 폴더를 확인하세요.' : 'Done! Check your downloads.'); }, 30); return; }
      var done = 0, maxPx = j.k === 'cards' ? 1600 : j.k === 'color' ? 2200 : 2600;
      return Promise.all(j.works.map(function (w) { return load(w.u, maxPx, j.k === 'color' ? 'line' : '').then(function (x) { done++; say((O.ko ? '그림 불러오는 중 ' : 'Loading pictures ') + done + ' / ' + j.works.length); return x; }); })).then(function (imgs) {
        say(O.ko ? 'PDF 만드는 중…' : 'Building the PDF…');
        var p = build(j.k, j.works, imgs, size, j.title); p.save(O.slug + '-' + size + '.pdf'); btn.disabled = false;
        say(O.ko ? '완료! 다운로드 폴더를 확인하세요. 다른 크기도 같은 키로 받을 수 있어요.' : 'Done! Check your downloads. You can get other sizes with the same key.');
      });
    }).catch(function () { btn.disabled = false; say(O.ko ? '문제가 생겼어요. 잠시 후 다시 시도하거나 hello@arttripstudio.com 으로 연락 주세요.' : 'Something went wrong. Try again shortly or write to hello@arttripstudio.com.'); });
  }
  return { init: function (o) { O = o; st = document.getElementById('st'); document.getElementById('go').addEventListener('click', go); }, build: build, load: load, buildPuz: buildPuz };
})();
