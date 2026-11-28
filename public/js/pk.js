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
  function go() {
    var key = document.getElementById('k').value.trim(); if (!key) { say(O.ko ? '라이선스 키를 넣어 주세요.' : 'Please enter your licence key.'); return; }
    var size = (document.querySelector('input[name=sz]:checked') || {}).value || 'A4', btn = document.getElementById('go'); btn.disabled = true;
    say(O.ko ? '키를 확인하는 중…' : 'Checking your key…');
    fetch('/api/pk/unlock', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ slug: O.slug, key: key }) }).then(function (r) { return r.json(); }).then(function (j) {
      if (!j.ok) { btn.disabled = false; say(O.ko ? '이 상품의 라이선스 키가 아니에요. 영수증 메일의 키를 다시 확인해 주세요.' : 'That key is not valid for this product. Please check the key in your receipt.'); return; }
      var done = 0, maxPx = j.k === 'cards' ? 1600 : j.k === 'color' ? 2200 : 2600;
      return Promise.all(j.works.map(function (w) { return load(w.u, maxPx, j.k === 'color' ? 'line' : '').then(function (x) { done++; say((O.ko ? '그림 불러오는 중 ' : 'Loading pictures ') + done + ' / ' + j.works.length); return x; }); })).then(function (imgs) {
        say(O.ko ? 'PDF 만드는 중…' : 'Building the PDF…');
        var p = build(j.k, j.works, imgs, size, j.title); p.save(O.slug + '-' + size + '.pdf'); btn.disabled = false;
        say(O.ko ? '완료! 다운로드 폴더를 확인하세요. 다른 크기도 같은 키로 받을 수 있어요.' : 'Done! Check your downloads. You can get other sizes with the same key.');
      });
    }).catch(function () { btn.disabled = false; say(O.ko ? '문제가 생겼어요. 잠시 후 다시 시도하거나 hello@arttripstudio.com 으로 연락 주세요.' : 'Something went wrong. Try again shortly or write to hello@arttripstudio.com.'); });
  }
  return { init: function (o) { O = o; st = document.getElementById('st'); document.getElementById('go').addEventListener('click', go); }, build: build, load: load };
})();
