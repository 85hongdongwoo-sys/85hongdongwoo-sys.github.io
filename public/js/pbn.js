/* Arttrip paint-by-number engine (browser). Turns a painting into numbered regions matched to real
   Liquitex BASICS and Winsor & Newton Galeria acrylic tube colours, and renders the 2-page PDF set. */
var PBN = (function () {
  var TUBES = [
    [432, 'Titanium White', 644, 'Titanium White', [246, 245, 240]], [434, 'Unbleached Titanium', 422, 'Naples Yellow', [232, 214, 172]],
    [159, 'Cadmium Yellow Light Hue', 114, 'Cadmium Yellow Pale Hue', [250, 214, 40]], [830, 'Cadmium Yellow Medium Hue', 120, 'Cadmium Yellow Medium Hue', [246, 178, 22]],
    [720, 'Cadmium Orange Hue', 90, 'Cadmium Orange Hue', [234, 108, 32]], [151, 'Cadmium Red Medium Hue', 95, 'Cadmium Red Hue', [198, 38, 36]],
    [116, 'Alizarin Crimson Hue Permanent', 203, 'Crimson', [136, 22, 42]], [186, 'Dioxazine Purple', 728, 'Winsor Violet', [68, 32, 92]],
    [680, 'Light Blue Violet', 444, 'Pale Violet', [168, 162, 214]], [380, 'Ultramarine Blue', 660, 'Ultramarine', [36, 46, 140]],
    [316, 'Phthalocyanine Blue', 706, 'Winsor Blue', [16, 40, 96]], [470, 'Cerulean Blue Hue', 138, 'Cerulean Blue Hue', [32, 112, 182]],
    [770, 'Light Blue Permanent', 446, 'Powder Blue', [142, 190, 224]], [46, 'Turquoise Blue', 232, 'Deep Turquoise', [0, 128, 140]],
    [312, 'Light Green Permanent', 483, 'Permanent Green Light', [92, 178, 72]], [224, "Hooker's Green Hue Permanent", 482, 'Permanent Green Deep', [32, 86, 48]],
    [317, 'Phthalocyanine Green', 522, 'Phthalo Green', [0, 82, 66]], [330, 'Raw Sienna', 552, 'Raw Sienna', [184, 118, 52]],
    [127, 'Burnt Sienna', 74, 'Burnt Sienna', [138, 60, 32]], [331, 'Raw Umber', 554, 'Raw Umber', [92, 72, 52]],
    [128, 'Burnt Umber', 76, 'Burnt Umber', [74, 46, 32]], [310, "Payne's Gray", 465, 'Paynes Gray', [46, 56, 72]], [276, 'Mars Black', 386, 'Mars Black', [26, 26, 26]]];
  function lin(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
  function srgb(l) { l = Math.min(1, Math.max(0, l)); return Math.round(255 * (l <= 0.0031308 ? l * 12.92 : 1.055 * Math.pow(l, 1 / 2.4) - 0.055)); }
  function mix(parts) { var tot = 0, lg = [0, 0, 0]; parts.forEach(function (p) { tot += p[1]; for (var c = 0; c < 3; c++) lg[c] += p[1] * Math.log(Math.max(lin(TUBES[p[0]][4][c]), 1e-4)); }); return lg.map(function (x) { return srgb(Math.exp(x / tot)); }); }
  function lab(r, g, b) {
    var R = lin(r), G = lin(g), B = lin(b), X = (R * 0.4124 + G * 0.3576 + B * 0.1805) / 0.95047, Y = R * 0.2126 + G * 0.7152 + B * 0.0722, Z = (R * 0.0193 + G * 0.1192 + B * 0.9505) / 1.08883;
    function f(t) { return t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116; } var fx = f(X), fy = f(Y), fz = f(Z); return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
  }
  var CAND = null;
  function candidates() {
    if (CAND) return CAND; var c = [], n = TUBES.length, i, j;
    for (i = 0; i < n; i++) { c.push([[i, 1]]); if (i) [1, 2, 4].forEach(function (w) { c.push([[i, 1], [0, w]]); }); }
    for (i = 1; i < n; i++) for (j = i + 1; j < n; j++) { c.push([[i, 1], [j, 1]]); c.push([[i, 1], [j, 1], [0, 2]]); }
    CAND = c.map(function (p) { var rgb = mix(p); return { parts: p, rgb: rgb, lab: lab(rgb[0], rgb[1], rgb[2]) }; }); return CAND;
  }
  function d2(a, b) { var x = a[0] - b[0], y = a[1] - b[1], z = a[2] - b[2]; return x * x + y * y + z * z; }

  // ---------- segmentation ----------
  function process(img, opt) {
    opt = opt || {}; var ncol = opt.ncol || 24, long = opt.long || 1500;
    var s = long / Math.max(img.width, img.height), W = Math.round(img.width * s), H = Math.round(img.height * s);
    var cv = document.createElement('canvas'); cv.width = W; cv.height = H; var x = cv.getContext('2d'); x.filter = 'blur(2.2px)'; x.drawImage(img, 0, 0, W, H);
    var px = x.getImageData(0, 0, W, H).data, N = W * H, L = new Float32Array(N * 3), i, k;
    for (i = 0; i < N; i++) { var l = lab(px[i * 4], px[i * 4 + 1], px[i * 4 + 2]); L[i * 3] = l[0]; L[i * 3 + 1] = l[1]; L[i * 3 + 2] = l[2]; }
    // k-means on a sample
    var S = [], step = Math.max(1, Math.floor(N / 30000)); for (i = 0; i < N; i += step) S.push(i);
    var C = []; for (k = 0; k < ncol; k++) { var q = S[Math.floor((k + 0.5) / ncol * S.length * 0.999)]; C.push([L[q * 3], L[q * 3 + 1], L[q * 3 + 2]]); }
    S.sort(function (a, b) { return L[a * 3] - L[b * 3]; }); for (k = 0; k < ncol; k++) { var q2 = S[Math.floor((k + 0.5) / ncol * S.length)]; C[k] = [L[q2 * 3], L[q2 * 3 + 1], L[q2 * 3 + 2]]; }
    for (var it = 0; it < 14; it++) {
      var sum = C.map(function () { return [0, 0, 0, 0]; });
      S.forEach(function (q) { var v = [L[q * 3], L[q * 3 + 1], L[q * 3 + 2]], b = 0, bd = 1e9; for (var c = 0; c < ncol; c++) { var dd = d2(v, C[c]); if (dd < bd) { bd = dd; b = c; } } sum[b][0] += v[0]; sum[b][1] += v[1]; sum[b][2] += v[2]; sum[b][3]++; });
      C = C.map(function (c, j) { return sum[j][3] ? [sum[j][0] / sum[j][3], sum[j][1] / sum[j][3], sum[j][2] / sum[j][3]] : c; });
    }
    var cand = candidates(), pick = {}; C.forEach(function (c) { var b = 0, bd = 1e9; cand.forEach(function (p, j) { var dd = d2(c, p.lab); if (dd < bd) { bd = dd; b = j; } }); pick[b] = 1; });
    var P = Object.keys(pick).map(Number).sort(function (a, b) { return cand[b].lab[0] - cand[a].lab[0]; }), PL = P.map(function (j) { return cand[j].lab; });
    var lbl = new Uint8Array(N); for (i = 0; i < N; i++) { var v2 = [L[i * 3], L[i * 3 + 1], L[i * 3 + 2]], b2 = 0, bd2 = 1e9; for (k = 0; k < PL.length; k++) { var e = d2(v2, PL[k]); if (e < bd2) { bd2 = e; b2 = k; } } lbl[i] = b2; }
    lbl = modeFilter(lbl, W, H, PL.length, 3);
    var minA = Math.round((opt.minFrac || 0.00028) * N);
    for (var pass = 0; pass < 4; pass++) if (!mergeSmall(lbl, W, H, minA)) break;
    // compact palette
    var used = {}, map = [], paints = []; for (i = 0; i < N; i++) used[lbl[i]] = 1;
    Object.keys(used).map(Number).sort(function (a, b) { return a - b; }).forEach(function (o, n) { map[o] = n; paints.push({ parts: cand[P[o]].parts, rgb: cand[P[o]].rgb }); });
    for (i = 0; i < N; i++) lbl[i] = map[lbl[i]];
    return { w: W, h: H, lbl: lbl, paints: paints, marks: marks(lbl, W, H) };
  }
  function modeFilter(lbl, W, H, K, r) {
    var out = new Uint8Array(lbl.length), cnt = new Int32Array(K), x, y, dx, dy;
    for (y = 0; y < H; y++) for (x = 0; x < W; x++) {
      cnt.fill(0); for (dy = -r; dy <= r; dy++) { var yy = Math.min(H - 1, Math.max(0, y + dy)); for (dx = -r; dx <= r; dx++) { var xx = Math.min(W - 1, Math.max(0, x + dx)); cnt[lbl[yy * W + xx]]++; } }
      var b = lbl[y * W + x], bc = 0; for (var k = 0; k < K; k++) if (cnt[k] > bc) { bc = cnt[k]; b = k; } out[y * W + x] = b;
    }
    return out;
  }
  function components(lbl, W, H) {
    var comp = new Int32Array(lbl.length).fill(-1), sizes = [], st = new Int32Array(lbl.length), n = 0;
    for (var s = 0; s < lbl.length; s++) { if (comp[s] >= 0) continue; var v = lbl[s], top = 0, sz = 0; st[top++] = s; comp[s] = n;
      while (top) { var p = st[--top]; sz++; var x = p % W, y = (p / W) | 0;
        if (x > 0 && comp[p - 1] < 0 && lbl[p - 1] === v) { comp[p - 1] = n; st[top++] = p - 1; } if (x < W - 1 && comp[p + 1] < 0 && lbl[p + 1] === v) { comp[p + 1] = n; st[top++] = p + 1; }
        if (y > 0 && comp[p - W] < 0 && lbl[p - W] === v) { comp[p - W] = n; st[top++] = p - W; } if (y < H - 1 && comp[p + W] < 0 && lbl[p + W] === v) { comp[p + W] = n; st[top++] = p + W; } }
      sizes.push(sz); n++; }
    return { comp: comp, sizes: sizes };
  }
  function mergeSmall(lbl, W, H, minA) {
    var c = components(lbl, W, H), comp = c.comp, sizes = c.sizes, changed = false, nb = {};
    for (var p = 0; p < lbl.length; p++) { var ci = comp[p]; if (sizes[ci] >= minA) continue; var x = p % W, y = (p / W) | 0, o = nb[ci] || (nb[ci] = {});
      [[x > 0, p - 1], [x < W - 1, p + 1], [y > 0, p - W], [y < H - 1, p + W]].forEach(function (q) { if (q[0] && comp[q[1]] !== ci) o[lbl[q[1]]] = (o[lbl[q[1]]] || 0) + 1; }); }
    var to = {}; Object.keys(nb).forEach(function (ci) { var o = nb[ci], b = -1, bc = 0; Object.keys(o).forEach(function (k) { if (o[k] > bc) { bc = o[k]; b = +k; } }); if (b >= 0) to[ci] = b; });
    for (p = 0; p < lbl.length; p++) { var t = to[comp[p]]; if (t !== undefined) { lbl[p] = t; changed = true; } }
    return changed;
  }
  function marks(lbl, W, H) {
    var N = lbl.length, D = new Float32Array(N), INF = 1e9, x, y, p;
    for (p = 0; p < N; p++) { x = p % W; y = (p / W) | 0; var e = (x > 0 && lbl[p - 1] !== lbl[p]) || (x < W - 1 && lbl[p + 1] !== lbl[p]) || (y > 0 && lbl[p - W] !== lbl[p]) || (y < H - 1 && lbl[p + W] !== lbl[p]) || x === 0 || y === 0 || x === W - 1 || y === H - 1; D[p] = e ? 0 : INF; }
    for (y = 0; y < H; y++) for (x = 0; x < W; x++) { p = y * W + x; if (x > 0) D[p] = Math.min(D[p], D[p - 1] + 1); if (y > 0) D[p] = Math.min(D[p], D[p - W] + 1); if (x > 0 && y > 0) D[p] = Math.min(D[p], D[p - W - 1] + 1.414); if (x < W - 1 && y > 0) D[p] = Math.min(D[p], D[p - W + 1] + 1.414); }
    for (y = H - 1; y >= 0; y--) for (x = W - 1; x >= 0; x--) { p = y * W + x; if (x < W - 1) D[p] = Math.min(D[p], D[p + 1] + 1); if (y < H - 1) D[p] = Math.min(D[p], D[p + W] + 1); if (x < W - 1 && y < H - 1) D[p] = Math.min(D[p], D[p + W + 1] + 1.414); if (x > 0 && y < H - 1) D[p] = Math.min(D[p], D[p + W - 1] + 1.414); }
    var c = components(lbl, W, H), best = new Int32Array(c.sizes.length).fill(-1);
    for (p = 0; p < N; p++) { var ci = c.comp[p]; if (best[ci] < 0 || D[p] > D[best[ci]]) best[ci] = p; }
    var out = []; for (var k = 0; k < best.length; k++) { p = best[k]; if (p < 0 || D[p] < 3.5) continue; out.push([p % W, (p / W) | 0, Math.round(D[p] * 10) / 10, lbl[p] + 1]); }
    return out;
  }

  // ---------- data packing (label map as PNG red channel) ----------
  function pack(r) {
    var cv = document.createElement('canvas'); cv.width = r.w; cv.height = r.h; var x = cv.getContext('2d'), id = x.createImageData(r.w, r.h);
    for (var i = 0; i < r.lbl.length; i++) { id.data[i * 4] = r.lbl[i]; id.data[i * 4 + 1] = 0; id.data[i * 4 + 2] = 0; id.data[i * 4 + 3] = 255; } x.putImageData(id, 0, 0);
    return { w: r.w, h: r.h, paints: r.paints, marks: r.marks, png: cv.toDataURL('image/png') };
  }
  function unpack(d) {
    return new Promise(function (res) { var im = new Image(); im.onload = function () { var cv = document.createElement('canvas'); cv.width = d.w; cv.height = d.h; var x = cv.getContext('2d'); x.drawImage(im, 0, 0); var px = x.getImageData(0, 0, d.w, d.h).data, lbl = new Uint8Array(d.w * d.h); for (var i = 0; i < lbl.length; i++) lbl[i] = px[i * 4]; res({ w: d.w, h: d.h, lbl: lbl, paints: d.paints, marks: d.marks }); }; im.src = d.png; });
  }

  // ---------- rendering ----------
  function outline(r, scale) {
    var W = r.w * scale, H = r.h * scale, cv = document.createElement('canvas'); cv.width = W; cv.height = H; var x = cv.getContext('2d'), id = x.createImageData(W, H), d = id.data, L = r.lbl, w = r.w;
    for (var Y = 0; Y < H; Y++) for (var X = 0; X < W; X++) { var sx = (X / scale) | 0, sy = (Y / scale) | 0, p = sy * w + sx, e = false;
      var th = Math.max(1, Math.round(scale * 0.75)); if (X % scale < th && sx > 0 && L[p - 1] !== L[p]) e = true; if (Y % scale < th && sy > 0 && L[p - w] !== L[p]) e = true;
      var o = (Y * W + X) * 4, v = e ? 55 : 255; d[o] = d[o + 1] = d[o + 2] = v; d[o + 3] = 255; }
    x.putImageData(id, 0, 0); return cv;
  }
  function preview(r) { var cv = document.createElement('canvas'); cv.width = r.w; cv.height = r.h; var x = cv.getContext('2d'), id = x.createImageData(r.w, r.h); for (var i = 0; i < r.lbl.length; i++) { var c = r.paints[r.lbl[i]].rgb; id.data[i * 4] = c[0]; id.data[i * 4 + 1] = c[1]; id.data[i * 4 + 2] = c[2]; id.data[i * 4 + 3] = 255; } x.putImageData(id, 0, 0); return cv; }
  function code(t, brand) { return brand ? ' #' + String(t[2]).padStart(3, '0') : ' #' + String(t[0]).padStart(3, '0'); }
  function recipe(parts, brand) { if (parts.length === 1) { var t0 = TUBES[parts[0][0]]; return (brand ? t0[3] : t0[1]) + code(t0, brand); } return parts.map(function (p) { var t = TUBES[p[0]]; return (p[1] > 1 ? p[1] + 'x ' : '1x ') + (brand ? t[3] : t[1]) + code(t, brand); }).join(' + '); }
  function nearest(rgb, brand) { var L = lab(rgb[0], rgb[1], rgb[2]), b = 0, bd = 1e9; TUBES.forEach(function (t, i) { var d = d2(L, lab(t[4][0], t[4][1], t[4][2])); if (d < bd) { bd = d; b = i; } }); var t = TUBES[b]; return (brand ? t[3] : t[1]) + code(t, brand); }
  var SZ = { A4: [210, 297], Letter: [215.9, 279.4], A3: [297, 420], A2: [420, 594] };
  function pdf(r, size, title, artist) {
    var S = SZ[size], land = r.w > r.h, W = land ? S[1] : S[0], H = land ? S[0] : S[1], M = 10, jp = window.jspdf.jsPDF, p = new jp({ unit: 'mm', format: [W, H] });
    var f = Math.min((W - 2 * M) / r.w, (H - 2 * M - 8) / r.h), iw = r.w * f, ih = r.h * f, x0 = (W - iw) / 2, y0 = M;
    p.addImage(outline(r, 3).toDataURL('image/png'), 'PNG', x0, y0, iw, ih, undefined, 'FAST'); p.setTextColor(45); p.setFont('helvetica', 'normal');
    r.marks.forEach(function (m) { var fs = Math.max(5, Math.min(11, m[2] * f * 2.4)); p.setFontSize(fs); p.text(String(m[3]), x0 + m[0] * f, y0 + m[1] * f + fs * 0.12, { align: 'center' }); });
    p.setFontSize(7); p.setTextColor(140); p.text(title + ' - ' + artist + ' - Arttrip Studio paint-by-number pattern', W / 2, H - M + 2, { align: 'center' });
    // key page (portrait)
    p.addPage([S[0], S[1]]); W = S[0]; H = S[1]; p.setTextColor(30); p.setFont('times', 'bold'); p.setFontSize(20); p.text(p.splitTextToSize(title, W - 2 * M), M, M + 8);
    p.setFont('helvetica', 'normal'); p.setFontSize(10); p.setTextColor(90); p.text(artist + ' · Paint by numbers colour key · ' + r.paints.length + ' colours', M, M + 16);
    var pv = preview(r), pf = Math.min((W - 2 * M) / r.w, H * 0.3 / r.h); p.addImage(pv.toDataURL('image/jpeg', 0.85), 'JPEG', M, M + 20, r.w * pf, r.h * pf);
    var ty = M + 26 + r.h * pf, rh = Math.min(7.5, (H - ty - 40) / r.paints.length); p.setFontSize(8); p.setTextColor(60); p.setFont('helvetica', 'bold'); p.text('No.', M, ty); p.text('Liquitex BASICS', M + 22, ty); p.text('Winsor & Newton Galeria', M + 22 + (W - 2 * M - 22) / 2, ty); p.setFont('helvetica', 'normal');
    r.paints.forEach(function (c, i) { var yy = ty + 3 + rh * i; p.setFillColor(c.rgb[0], c.rgb[1], c.rgb[2]); p.rect(M + 7, yy, 11, rh * 0.8, 'F'); p.setTextColor(30); p.setFontSize(Math.min(8, rh * 1.6)); p.text(String(i + 1), M, yy + rh * 0.6); p.text(recipe(c.parts, 0), M + 22, yy + rh * 0.6); p.text(recipe(c.parts, 1), M + 22 + (W - 2 * M - 22) / 2, yy + rh * 0.6); });
    p.setFontSize(7.5); p.setTextColor(90);
    p.text(p.splitTextToSize('How to read the key: "1x A + 2x Titanium White" means 1 part A mixed with 2 parts white. Mix enough for every area with that number before you start. Paint one flat colour per area, light colours first. Print page 1 at 100% (no scaling) on 200 g/m² or heavier paper, or trace it onto canvas with graphite transfer paper. Liquitex and Winsor & Newton are trademarks of their owners; Arttrip Studio is not affiliated with them.', W - 2 * M), M, H - M - 18);
    // page 3: printable colour key + shopping list (closest single tube and exact mix, by brand)
    p.addPage([S[0], S[1]]); W = S[0]; H = S[1]; p.setTextColor(30); p.setFont('helvetica', 'bold'); p.setFontSize(16); p.text('Colour key & paint shopping list', M, M + 6);
    p.setFont('helvetica', 'normal'); p.setFontSize(8.5); p.setTextColor(80); p.text(p.splitTextToSize(title + ' - ' + artist + '. Bold = the single tube closest to that colour (# = colour number printed on the tube). Second line = exact mix for a closer match.', W - 2 * M), M, M + 12);
    var used = [{}, {}]; r.paints.forEach(function (c) { c.parts.forEach(function (q) { used[0][TUBES[q[0]][1] + code(TUBES[q[0]], 0)] = 1; used[1][TUBES[q[0]][3] + code(TUBES[q[0]], 1)] = 1; }); [0, 1].forEach(function (b) { used[b][nearest(c.rgb, b)] = 1; }); });
    var cx = (W - 2 * M - 20) / 2, y3 = M + 24; p.setTextColor(30); p.setFont('helvetica', 'bold'); p.setFontSize(10); p.text('Shopping list: Liquitex BASICS', M, y3); p.text('Shopping list: Winsor & Newton Galeria', M + 20 + cx, y3);
    p.setFont('helvetica', 'normal'); p.setFontSize(8.5); var L0 = Object.keys(used[0]).sort(), L1 = Object.keys(used[1]).sort(), lh = 4.2;
    L0.forEach(function (t, i) { p.text('[  ] ' + t, M, y3 + 5 + i * lh); }); L1.forEach(function (t, i) { p.text('[  ] ' + t, M + 20 + cx, y3 + 5 + i * lh); });
    var ky = y3 + 9 + Math.max(L0.length, L1.length) * lh, rh3 = Math.min(10, (H - M - 6 - ky) / r.paints.length);
    p.setFont('helvetica', 'bold'); p.setFontSize(9); p.text('No.', M, ky); p.text('Liquitex BASICS', M + 22, ky); p.text('Winsor & Newton Galeria', M + 22 + cx, ky);
    r.paints.forEach(function (c, i) { var yy = ky + 2 + rh3 * i, fs = Math.min(8.5, rh3 * 0.9); p.setFillColor(c.rgb[0], c.rgb[1], c.rgb[2]); p.rect(M + 7, yy, 11, rh3 * 0.85, 'F'); p.setTextColor(30); p.setFont('helvetica', 'bold'); p.setFontSize(fs);
      p.text(String(i + 1), M, yy + fs * 0.4); p.text(nearest(c.rgb, 0), M + 22, yy + fs * 0.4); p.text(nearest(c.rgb, 1), M + 22 + cx, yy + fs * 0.4);
      p.setFont('helvetica', 'normal'); p.setFontSize(fs * 0.85); p.setTextColor(90); p.text(recipe(c.parts, 0), M + 22, yy + fs * 0.4 + fs * 0.42); p.text(recipe(c.parts, 1), M + 22 + cx, yy + fs * 0.4 + fs * 0.42); });
    return p;
  }
  return { process: process, pack: pack, unpack: unpack, pdf: pdf, preview: preview, outline: outline, recipe: recipe, nearest: nearest, candidates: candidates };
})();
