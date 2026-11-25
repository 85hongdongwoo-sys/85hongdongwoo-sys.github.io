/* Muse Archive Studio — print-ready product makers (runs entirely in the browser) */
window.Studio = (function () {
  var MA = window.MA || {};
  var FONTS = { serif: '"Cormorant Garamond", Georgia, serif', display: '"Playfair Display", Georgia, serif', sans: 'Inter, Helvetica, Arial, sans-serif', script: '"Dancing Script", cursive' };
  var FONT_NAMES = { serif: 'Classic serif', display: 'Display serif', sans: 'Modern sans', script: 'Handwritten' };
  var COLORS = ['#111111', '#ffffff', '#f3ece0', '#1e3550', '#a7573f', '#4f6b3a', '#b8902f'];
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var IN = 25.4;
  var KO = {"Print at home": "집에서 인쇄", "Products": "굿즈", "Screens": "화면용", "Poster": "포스터", "Gallery-style print with a mat and caption.": "여백과 캡션이 있는 갤러리 스타일 인쇄물.", "Wall calendar": "벽걸이 달력", "Cover plus 12 months, one artwork or a mix.": "표지와 12개월. 한 작품 또는 여러 작품 섞기.", "Desk calendar": "탁상 달력", "Small landscape pages for a desk stand.": "책상 거치대용 작은 가로 페이지.", "Folded card": "접는 카드", "Print both sides, fold in half. Front, back and inside.": "양면 인쇄 후 반으로 접어요. 앞·뒤·안쪽.", "Postcard": "엽서", "Art on the front, message and address on the back.": "앞면은 그림, 뒷면은 메시지와 주소.", "Invitation": "초대장", "Weddings, birthdays, dinners. Art on top, your words below.": "결혼식·생일·모임. 위에는 그림, 아래는 내 문구.", "Sticker sheet": "스티커 시트", "Round stickers with cut lines for scissors or a cutting machine.": "가위나 커팅기로 자르는 원형 스티커.", "Gift tags": "선물 태그", "Nine tags per sheet with a punch-hole mark.": "한 장에 9개, 구멍 위치 표시.", "Bookmarks": "책갈피", "Four tall bookmarks per sheet.": "한 장에 세로 책갈피 4개.", "Wrapping paper": "포장지", "A repeating pattern sheet for gifts and paper crafts.": "선물 포장과 종이공예용 반복 패턴.", "Mug wrap": "머그 랩", "Full-wrap print file for sublimation or print-on-demand mugs.": "승화전사·주문제작 머그용 전체 감싸기 파일.", "Phone case": "폰 케이스", "Case-back artwork with a camera guide.": "카메라 위치 안내가 있는 케이스 뒷면 그림.", "Phone wallpaper": "폰 배경화면", "Lock and home screen, with an optional quote.": "잠금·홈 화면용, 문구 넣기 가능.", "Social post": "SNS 이미지", "Instagram post or story, YouTube thumbnail.": "인스타그램 게시물·스토리, 유튜브 썸네일.", "Studio": "스튜디오", "Make something real.": "명화로 직접 만들어 보세요.", "Pick a product, pick an artwork, add your words. Download a print-ready file.": "만들 것과 그림을 고르고 문구를 넣으면, 바로 인쇄할 수 있는 파일이 나와요.", "Download PNG": "PNG 내려받기", "Print or save as PDF": "인쇄 또는 PDF로 저장", "Artwork": "그림", "Size": "크기", "Headline": "제목", "Small line": "작은 문구", "Message": "메시지", "Year": "연도", "Week starts": "한 주 시작", "Sunday": "일요일", "Monday": "월요일", "Stickers per row": "한 줄 스티커 수", "Typeface": "글꼴", "Text color": "글자 색", "Background": "배경", "Mix artworks": "여러 작품 섞기", "White mat and caption": "흰 여백과 캡션", "Show cut and fold lines": "자르는 선·접는 선 표시", "Optional": "선택", "Your words": "내 문구", "Classic serif": "클래식 세리프", "Display serif": "디스플레이 세리프", "Modern sans": "모던 고딕", "Handwritten": "손글씨", "Outside": "바깥면", "Inside": "안쪽", "Front": "앞면", "Back": "뒷면", "Cover": "표지", "Each case maker has its own template. Use this as the artwork, then place it on their template.": "케이스 업체마다 템플릿이 달라요. 이 파일을 그림으로 쓰고 업체 템플릿에 올리세요."};
  var MONTHS_KO = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"];
  function ko() { return MA && MA.lang === 'ko'; }
  function tr(x) { return ko() && KO[x] ? KO[x] : x; }
  function trH(h) { if (!ko()) return h; Object.keys(KO).sort(function (a, b) { return b.length - a.length; }).forEach(function (k) { h = h.split('>' + k + '<').join('>' + KO[k] + '<').split('"' + k + '"').join('"' + KO[k] + '"'); }); return h; }

  // ---------- tools ----------
  var T = {};
  function tool(id, d) { d.id = id; T[id] = d; }

  tool('poster', { g: 'Print at home', name: 'Poster', desc: 'Gallery-style print with a mat and caption.',
    sizes: [['A4', 210, 297], ['A3', 297, 420], ['8 × 10 in', 8 * IN, 10 * IN], ['11 × 14 in', 11 * IN, 14 * IN], ['12 × 16 in', 12 * IN, 16 * IN], ['18 × 24 in', 18 * IN, 24 * IN]],
    fields: ['title', 'sub', 'font', 'color', 'mat'], pages: one,
    draw: function (c, W, H, p, o, k) {
      if (!o.mat) { cover(c, o.art, 0, 0, W, H); if (o.title) caption(c, o, W / 2, H - 14 * k, k * 7, '#fff', true); return; }
      fill(c, 0, 0, W, H, '#faf8f3'); var m = Math.min(W, H) * 0.09, cap = o.title ? 26 * k : 0;
      cover(c, o.art, m, m, W - 2 * m, H - 2 * m - cap);
      if (o.title) { txt(c, o.title, W / 2, H - m - cap * 0.38, 6.5 * k, o.font, o.color === '#ffffff' ? '#111' : o.color, 'center', 600); if (o.sub) txt(c, o.sub.toUpperCase(), W / 2, H - m + 1 * k, 2.6 * k, 'sans', '#777', 'center', 500, 0.18); }
    } });

  tool('wallcal', { g: 'Print at home', name: 'Wall calendar', desc: 'Cover plus 12 months, one artwork or a mix.',
    sizes: [['A4', 210, 297], ['US Letter', 8.5 * IN, 11 * IN], ['A3', 297, 420], ['11 × 17 in', 11 * IN, 17 * IN]],
    fields: ['year', 'start', 'mix', 'font', 'color', 'title'], pages: function () { return 13; },
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#fff'); var m = 12 * k, a = artFor(o, p);
      if (p === 0) { cover(c, a, 0, 0, W, H * 0.78); txt(c, String(o.year), W / 2, H * 0.88, 22 * k, o.font, ink(o), 'center', 600); txt(c, (o.title || 'A Year of Art').toUpperCase(), W / 2, H * 0.94, 3.4 * k, 'sans', '#777', 'center', 500, 0.2); return; }
      cover(c, a, m, m, W - 2 * m, H * 0.5);
      month(c, m, H * 0.5 + m * 1.6, W - 2 * m, H - (H * 0.5 + m * 2.4), o.year, p - 1, o, k);
    } });

  tool('deskcal', { g: 'Print at home', name: 'Desk calendar', desc: 'Small landscape pages for a desk stand.',
    sizes: [['6 × 4 in', 6 * IN, 4 * IN], ['A6', 148, 105], ['7 × 5 in', 7 * IN, 5 * IN]],
    fields: ['year', 'start', 'mix', 'font', 'color'], pages: function () { return 12; },
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#fff'); cover(c, artFor(o, p + 1), 0, 0, W * 0.46, H);
      var m = 7 * k; month(c, W * 0.46 + m, m, W * 0.54 - 2 * m, H - 2 * m, o.year, p, o, k * 0.62);
    } });

  tool('card', { g: 'Print at home', name: 'Folded card', desc: 'Print both sides, fold in half. Front, back and inside.',
    sizes: [['A5 card (A4 sheet)', 297, 210], ['5.5 × 8.5 in card (Letter sheet)', 11 * IN, 8.5 * IN]],
    fields: ['title', 'msg', 'font', 'color', 'cut'], pages: function () { return 2; }, pageNames: ['Outside', 'Inside'],
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#fff'); var h = W / 2;
      if (p === 0) {
        var band = o.title ? 34 * k : 0; cover(c, o.art, h, 0, h, H - band);
        if (o.title) txt(c, o.title, h * 1.5, H - band * 0.42, 8 * k, o.font, ink(o), 'center', 600);
        txt(c, 'ARTTRIP STUDIO', h / 2, H - 14 * k, 2.4 * k, 'sans', '#999', 'center', 500, 0.25);
      } else { para(c, o.msg || 'Wishing you a beautiful day.', h * 1.5, H / 2, h * 0.7, 7 * k, o.font, ink(o)); }
      if (o.cut) dash(c, [[h, 0, h, H]], k);
    } });

  tool('postcard', { g: 'Print at home', name: 'Postcard', desc: 'Art on the front, message and address on the back.',
    sizes: [['6 × 4 in', 6 * IN, 4 * IN], ['A6', 148, 105], ['7 × 5 in', 7 * IN, 5 * IN]],
    fields: ['title', 'msg', 'font', 'color'], pages: function () { return 2; }, pageNames: ['Front', 'Back'],
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#fff');
      if (p === 0) { cover(c, o.art, 0, 0, W, H); if (o.title) caption(c, o, W / 2, H - 9 * k, 6 * k, '#fff', true); return; }
      var m = 8 * k; line(c, W / 2, m, W / 2, H - m, '#ccc', 0.3 * k);
      para(c, o.msg || 'Greetings from here.', W / 4, H / 2, W / 2 - 2 * m, 5 * k, o.font, ink(o));
      for (var i = 0; i < 4; i++) line(c, W / 2 + m, H * 0.45 + i * 10 * k, W - m, H * 0.45 + i * 10 * k, '#bbb', 0.3 * k);
      c.strokeStyle = '#bbb'; c.lineWidth = 0.3 * k; c.strokeRect(W - m - 18 * k, m, 18 * k, 22 * k);
      txt(c, MA.A[o.art].t.slice(0, 50) + ' · ' + MA.A[o.art].a, m, H - 5 * k, 2.2 * k, 'sans', '#999', 'left', 400);
    } });

  tool('invite', { g: 'Print at home', name: 'Invitation', desc: 'Weddings, birthdays, dinners. Art on top, your words below.',
    sizes: [['5 × 7 in', 5 * IN, 7 * IN], ['A5', 148, 210], ['A6', 105, 148]],
    fields: ['title', 'msg', 'font', 'color'], pages: one,
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#faf8f3'); var m = 9 * k; cover(c, o.art, m, m, W - 2 * m, H * 0.44);
      txt(c, o.title || 'You are invited', W / 2, H * 0.58, 9 * k, o.font, ink(o), 'center', 600);
      para(c, o.msg || 'Saturday, June 12\n6 o\'clock in the evening\nThe Garden House', W / 2, H * 0.76, W - 4 * m, 4.6 * k, 'serif', '#444');
    } });

  tool('stickers', { g: 'Print at home', name: 'Sticker sheet', desc: 'Round stickers with cut lines for scissors or a cutting machine.',
    sizes: [['A4', 210, 297], ['US Letter', 8.5 * IN, 11 * IN]],
    fields: ['count', 'mix', 'cut'], pages: one,
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#fff'); var cols = +o.count || 4, m = 12 * k, cell = (W - 2 * m) / cols, r = cell * 0.42, rows = Math.floor((H - 2 * m) / cell), n = 0;
      for (var y = 0; y < rows; y++) for (var x = 0; x < cols; x++) {
        var cx = m + cell * (x + 0.5), cy = m + cell * (y + 0.5), a = o.mix ? ML()[n++ % ML().length] : o.art;
        c.save(); c.beginPath(); c.arc(cx, cy, r, 0, 7); c.clip(); cover(c, a, cx - r, cy - r, 2 * r, 2 * r); c.restore();
        c.lineWidth = 2.2 * k; c.strokeStyle = '#fff'; c.beginPath(); c.arc(cx, cy, r, 0, 7); c.stroke();
        if (o.cut) { c.setLineDash([1.2 * k, 1.2 * k]); c.lineWidth = 0.25 * k; c.strokeStyle = '#999'; c.beginPath(); c.arc(cx, cy, r + 1.4 * k, 0, 7); c.stroke(); c.setLineDash([]); }
      }
    } });

  tool('tags', { g: 'Print at home', name: 'Gift tags', desc: 'Nine tags per sheet with a punch-hole mark.',
    sizes: [['A4', 210, 297], ['US Letter', 8.5 * IN, 11 * IN]],
    fields: ['title', 'mix', 'font', 'color', 'cut'], pages: one,
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#fff'); var tw = 55 * k, th = 88 * k, gx = (W - 3 * tw) / 4, gy = (H - 3 * th) / 4, n = 0;
      for (var y = 0; y < 3; y++) for (var x = 0; x < 3; x++) {
        var X = gx + x * (tw + gx), Y = gy + y * (th + gy), a = o.mix ? ML()[n++ % ML().length] : o.art, ch = 9 * k;
        c.save(); tagPath(c, X, Y, tw, th, ch); c.clip(); fill(c, X, Y, tw, th, '#faf8f3'); cover(c, a, X, Y, tw, th * 0.56); c.restore();
        c.fillStyle = '#fff'; c.beginPath(); c.arc(X + tw / 2, Y + 7 * k, 2.6 * k, 0, 7); c.fill(); c.strokeStyle = '#999'; c.lineWidth = 0.25 * k; c.stroke();
        txt(c, o.title || 'For you', X + tw / 2, Y + th * 0.7, 4.6 * k, o.font, ink(o), 'center', 600);
        line(c, X + 7 * k, Y + th * 0.84, X + tw - 7 * k, Y + th * 0.84, '#ccc', 0.25 * k);
        if (o.cut) { c.setLineDash([1.2 * k, 1.2 * k]); c.strokeStyle = '#999'; c.lineWidth = 0.25 * k; tagPath(c, X, Y, tw, th, ch); c.stroke(); c.setLineDash([]); }
      }
    } });

  tool('bookmarks', { g: 'Print at home', name: 'Bookmarks', desc: 'Four tall bookmarks per sheet.',
    sizes: [['A4', 210, 297], ['US Letter', 8.5 * IN, 11 * IN]],
    fields: ['title', 'mix', 'font', 'cut'], pages: one,
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#fff'); var bw = 44 * k, bh = 180 * k, gx = (W - 4 * bw) / 5, Y = (H - bh) / 2;
      for (var i = 0; i < 4; i++) {
        var X = gx + i * (bw + gx), a = o.mix ? ML()[i % ML().length] : o.art;
        cover(c, a, X, Y, bw, bh - 22 * k); fill(c, X, Y + bh - 22 * k, bw, 22 * k, '#faf8f3');
        txt(c, o.title || MA.A[a].a.split(' ').slice(-1)[0], X + bw / 2, Y + bh - 9 * k, 3.4 * k, o.font, '#111', 'center', 600);
        if (o.cut) dashRect(c, X, Y, bw, bh, k);
      }
    } });

  tool('wrap', { g: 'Print at home', name: 'Wrapping paper', desc: 'A repeating pattern sheet for gifts and paper crafts.',
    sizes: [['A4', 210, 297], ['US Letter', 8.5 * IN, 11 * IN], ['A3', 297, 420]],
    fields: ['scale', 'mix'], pages: one,
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#fff'); var s = (+o.scale || 50) * k, n = 0;
      for (var y = -1; y * s * 1.33 < H; y++) for (var x = -1; x * s < W + s; x++) {
        var X = x * s + (y % 2 ? s / 2 : 0), Y = y * s * 1.33, a = o.mix ? ML()[n++ % ML().length] : o.art;
        cover(c, a, X + s * 0.06, Y + s * 0.06, s * 0.88, s * 1.2);
      }
    } });

  tool('mug', { g: 'Products', name: 'Mug wrap', desc: 'Full-wrap print file for sublimation or print-on-demand mugs.',
    sizes: [['11 oz mug (8.5 × 3.5 in)', 8.5 * IN, 3.5 * IN], ['15 oz mug (9 × 4 in)', 9 * IN, 4 * IN]],
    fields: ['title', 'font', 'color', 'bg'], pages: one, note: 'Sizes follow common sublimation templates. Check your print service\'s template before ordering.',
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, o.bg || '#faf8f3'); var h = H * 0.82, w = h * 0.75;
      [0.25, 0.75].forEach(function (f) { cover(c, o.art, W * f - w / 2, (H - h) / 2, w, h); });
      if (o.title) txt(c, o.title, W / 2, H / 2 + 3 * k, 7 * k, o.font, ink(o), 'center', 600);
    } });

  tool('case', { g: 'Products', name: 'Phone case', desc: 'Case-back artwork with a camera guide.',
    sizes: [['Generic large phone (78 × 162 mm)', 78, 162], ['Generic small phone (72 × 148 mm)', 72, 148]],
    fields: ['title', 'font', 'color', 'cut'], pages: one, note: 'Each case maker has its own template. Use this as the artwork, then place it on their template.',
    draw: function (c, W, H, p, o, k) {
      cover(c, o.art, 0, 0, W, H); if (o.title) caption(c, o, W / 2, H - 16 * k, 6 * k, '#fff', true);
      if (o.cut) { dashRect(c, 6 * k, 6 * k, 38 * k, 38 * k, k); c.setLineDash([1.2 * k, 1.2 * k]); c.strokeStyle = '#fff'; c.lineWidth = 0.4 * k; rr(c, 0.5 * k, 0.5 * k, W - k, H - k, 9 * k); c.stroke(); c.setLineDash([]); }
    } });

  tool('wallpaper', { g: 'Screens', name: 'Phone wallpaper', desc: 'Lock and home screen, with an optional quote.', px: true,
    sizes: [['iPhone (1179 × 2556)', 1179, 2556], ['Android (1440 × 3200)', 1440, 3200], ['Desktop (2560 × 1440)', 2560, 1440]],
    fields: ['title', 'font', 'color'], pages: one,
    draw: function (c, W, H, p, o, k) { cover(c, o.art, 0, 0, W, H); if (o.title) caption(c, o, W / 2, H * 0.8, Math.min(W, H) * 0.06, '#fff', false); } });

  tool('social', { g: 'Screens', name: 'Social post', desc: 'Instagram post or story, YouTube thumbnail.', px: true,
    sizes: [['Instagram post (1080 × 1350)', 1080, 1350], ['Instagram story (1080 × 1920)', 1080, 1920], ['YouTube thumbnail (1280 × 720)', 1280, 720]],
    fields: ['title', 'sub', 'font', 'color'], pages: one,
    draw: function (c, W, H, p, o, k) {
      fill(c, 0, 0, W, H, '#faf8f3'); var land = W > H;
      if (land) { cover(c, o.art, 0, 0, W * 0.5, H); txt(c, o.title || 'Your headline', W * 0.75, H * 0.5, H * 0.1, o.font, ink(o), 'center', 700); if (o.sub) txt(c, o.sub, W * 0.75, H * 0.64, H * 0.045, 'sans', '#666', 'center', 500); return; }
      cover(c, o.art, 0, 0, W, H * 0.68); txt(c, o.title || 'Your headline', W / 2, H * 0.81, W * 0.075, o.font, ink(o), 'center', 700);
      if (o.sub) txt(c, o.sub.toUpperCase(), W / 2, H * 0.89, W * 0.03, 'sans', '#777', 'center', 500, 0.2);
    } });

  function one() { return 1; }
  var MIXN = 24;
  function mixList() { var s = MA.A[o.art].s, l = MA.ORDER.filter(function (x) { return MA.A[x].s === s; }); l = l.filter(function (x) { return x !== o.art; }); l.unshift(o.art); return l.slice(0, MIXN); }
  function picks() { var l = MA.ORDER.filter(function (x, i) { return i % 9 === 0; }).slice(0, 19); if (l.indexOf(o.art) < 0) l.unshift(o.art); return l.slice(0, 20); }
  function used() { return mixList(); }
  var schT; function schedule() { clearTimeout(schT); schT = setTimeout(preview, 60); }

  // ---------- drawing helpers ----------
  var cache = {};
  function img(id) {
    if (cache[id]) return cache[id];
    var im = new Image(); im.src = '/img/' + id + '.jpg'; cache[id] = im; return im;
  }
  function ready() { return Promise.all(used().map(function (id) { var i = img(id); return i.complete && i.naturalWidth ? 0 : new Promise(function (r) { i.onload = i.onerror = r; }); })); }
  function cover(c, id, x, y, w, h) {
    var i = img(id), iw = i.naturalWidth || 600, ih = i.naturalHeight || 800;
    if (!i.naturalWidth) { i.addEventListener('load', schedule, { once: true }); fill(c, x, y, w, h, '#e5e1d8'); return; }
    var s = Math.max(w / iw, h / ih), sw = w / s, sh = h / s;
    c.save(); c.beginPath(); c.rect(x, y, w, h); c.clip(); c.drawImage(i, (iw - sw) / 2, (ih - sh) / 2, sw, sh, x, y, w, h); c.restore();
  }
  function fill(c, x, y, w, h, col) { c.fillStyle = col; c.fillRect(x, y, w, h); }
  function line(c, a, b, d, e, col, lw) { c.strokeStyle = col; c.lineWidth = lw; c.beginPath(); c.moveTo(a, b); c.lineTo(d, e); c.stroke(); }
  function txt(c, s, x, y, size, font, col, align, weight, track) {
    c.fillStyle = col; c.textAlign = align || 'left'; c.textBaseline = 'alphabetic';
    c.font = (weight || 400) + ' ' + Math.max(1, size) + 'px ' + (FONTS[font] || FONTS.serif);
    if (track && 'letterSpacing' in c) c.letterSpacing = (size * track) + 'px';
    c.fillText(s, x, y); if ('letterSpacing' in c) c.letterSpacing = '0px';
  }
  function para(c, s, x, cy, maxW, size, font, col) {
    c.font = '400 ' + size + 'px ' + (FONTS[font] || FONTS.serif); var out = [];
    String(s).split('\n').forEach(function (ln) { var w = ln.split(' '), cur = ''; w.forEach(function (word) { var t = cur ? cur + ' ' + word : word; if (c.measureText(t).width > maxW && cur) { out.push(cur); cur = word; } else cur = t; }); out.push(cur); });
    var lh = size * 1.45, y0 = cy - (out.length - 1) * lh / 2 + size * 0.35;
    out.forEach(function (l, i) { txt(c, l, x, y0 + i * lh, size, font, col, 'center', 400); });
  }
  function caption(c, o, x, y, size, col, band) {
    if (band) { var g = c.createLinearGradient(0, y - size * 4, 0, y + size); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,.45)'); c.fillStyle = g; c.fillRect(0, y - size * 4, c.canvas.width, size * 5 + 2000); }
    else { c.save(); c.shadowColor = 'rgba(0,0,0,.45)'; c.shadowBlur = size * 0.6; }
    txt(c, o.title, x, y, size, o.font, o.color === '#111111' ? col : o.color, 'center', 600);
    if (!band) c.restore();
  }
  function ink(o) { return o.color === '#ffffff' ? '#111111' : o.color; }
  function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  function tagPath(c, x, y, w, h, ch) { c.beginPath(); c.moveTo(x + ch, y); c.lineTo(x + w - ch, y); c.lineTo(x + w, y + ch); c.lineTo(x + w, y + h); c.lineTo(x, y + h); c.lineTo(x, y + ch); c.closePath(); }
  function dash(c, segs, k) { c.setLineDash([1.5 * k, 1.5 * k]); segs.forEach(function (s) { line(c, s[0], s[1], s[2], s[3], '#aaa', 0.25 * k); }); c.setLineDash([]); }
  function dashRect(c, x, y, w, h, k) { c.setLineDash([1.2 * k, 1.2 * k]); c.strokeStyle = '#999'; c.lineWidth = 0.25 * k; c.strokeRect(x, y, w, h); c.setLineDash([]); }
  var _ml = null, _mlk = '';
  function ML() { if (_mlk !== o.art) { _ml = mixList(); _mlk = o.art; } return _ml; }
  function artFor(o, p) { return o.mix ? ML()[p % ML().length] : o.art; }
  function month(c, x, y, w, h, year, m, o, k) {
    txt(c, MONTHS[m], x, y + 9 * k, 11 * k, o.font, ink(o), 'left', 600);
    txt(c, String(year), x + w, y + 9 * k, 4 * k, 'sans', '#999', 'right', 500, 0.15);
    var days = o.start === 'mon' ? ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'] : ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
    var gy = y + 18 * k, cw = w / 7, ch = (y + h - gy - 6 * k) / 6;
    days.forEach(function (d, i) { txt(c, d, x + cw * i + cw / 2, gy, 2.6 * k, 'sans', '#999', 'center', 500, 0.12); });
    line(c, x, gy + 3 * k, x + w, gy + 3 * k, '#ddd', 0.25 * k);
    var first = new Date(Date.UTC(year, m, 1)).getUTCDay(), off = o.start === 'mon' ? (first + 6) % 7 : first, n = new Date(Date.UTC(year, m + 1, 0)).getUTCDate();
    for (var d = 1; d <= n; d++) {
      var idx = off + d - 1, col = idx % 7, row = Math.floor(idx / 7), wk = o.start === 'mon' ? col >= 5 : (col === 0 || col === 6);
      txt(c, String(d), x + cw * col + cw / 2, gy + 6 * k + ch * row + ch * 0.55, 4.4 * k, 'sans', wk ? '#a7573f' : '#222', 'center', 500);
    }
  }
  function watermark(c, W, H) {
    c.save(); c.translate(W / 2, H / 2); c.rotate(-Math.PI / 6); c.fillStyle = 'rgba(255,255,255,.55)'; c.strokeStyle = 'rgba(0,0,0,.18)';
    var s = Math.max(W, H) * 0.035; c.font = '600 ' + s + 'px Inter, sans-serif'; c.textAlign = 'center'; c.lineWidth = s * 0.03;
    for (var y = -H; y < H; y += s * 6) for (var x = -W; x < W; x += s * 17) { c.fillText('ARTTRIP STUDIO · PREVIEW', x, y); c.strokeText('ARTTRIP STUDIO · PREVIEW', x, y); }
    c.restore();
  }

  // ---------- state & UI ----------
  var o = { tool: 'wallcal', art: '', size: 0, title: '', sub: '', msg: '', font: 'display', color: '#111111', bg: '#faf8f3', year: 2027, start: 'sun', mix: true, cut: true, mat: true, count: 4, scale: 50, page: 0 };
  function cur() { return T[o.tool]; }
  function dims(t) { var s = t.sizes[o.size] || t.sizes[0]; return { w: s[1], h: s[2], px: !!t.px, label: s[0] }; }

  function html(id, art) {
    MA = window.MA; if (!MA.A[o.art]) o.art = MA.ORDER[0];
    if (art && MA.A[art]) o.art = art;
    if (id && T[id] && id !== o.tool) { o.tool = id; o.size = 0; o.page = 0; }
    var groups = {}; Object.keys(T).forEach(function (k) { (groups[T[k].g] = groups[T[k].g] || []).push(T[k]); });
    var t = cur();
    return trH('<div class="wrap"><div class="sthead"><span class="lbl">Studio</span><h2>Make something real.</h2><p class="sub">Pick a product, pick an artwork, add your words. Download a print-ready file.</p></div><div class="studio">' +
      '<aside class="stools">' + Object.keys(groups).map(function (g) { return '<div class="stg"><span class="lbl">' + g + '</span>' + groups[g].map(function (x) { return '<a href="#/studio/' + x.id + '" class="stool" aria-current="' + (x.id === o.tool) + '">' + x.name + '</a>'; }).join('') + '</div>'; }).join('') + '</aside>' +
      '<section class="stage"><div class="sname"><h3>' + t.name + '</h3><p class="small">' + t.desc + '</p></div><div class="cwrap" id="cwrap"><canvas id="sc" aria-label="Preview of ' + t.name + '"></canvas></div>' +
      '<div class="pager" id="pager"></div><div class="row" style="margin-top:16px"><button class="pill" id="sPng">Download PNG</button><button class="pill ghost" id="sPdf">Print or save as PDF</button></div><p class="small" id="sInfo" style="margin-top:10px"></p>' + (t.note ? '<p class="small">' + t.note + '</p>' : '') + '</section>' +
      '<aside class="sopts" id="sopts">' + opts() + '</aside></div></div><div id="printArea" aria-hidden="true"></div>');
  }
  function opts() {
    var t = cur(), f = t.fields, h = '';
    h += '<span class="lbl">Artwork</span><div class="sarts">' + picks().map(function (id) { return '<button class="sart" data-art="' + id + '" aria-pressed="' + (o.art === id) + '" aria-label="' + esc(MA.A[id].t) + '">' + MA.svg(id) + '</button>'; }).join('') + '</div><p class="small">' + esc(MA.A[o.art].t) + ' · ' + esc(MA.A[o.art].a) + '</p><a class="small" href="' + (ko() ? '/ko' : '') + '/art" style="text-decoration:underline">' + (ko() ? '명화 ' + MA.ORDER.length + '점 모두 보기' : 'Browse all ' + MA.ORDER.length + ' artworks') + '</a>';
    h += '<label class="lbl" for="sSize">Size</label><select id="sSize" data-k="size">' + t.sizes.map(function (s, i) { return '<option value="' + i + '"' + (i == o.size ? ' selected' : '') + '>' + s[0] + '</option>'; }).join('') + '</select>';
    if (f.indexOf('title') > -1) h += '<label class="lbl" for="sTitle">Headline</label><input type="text" id="sTitle" data-k="title" maxlength="60" value="' + esc(o.title) + '" placeholder="Optional">';
    if (f.indexOf('sub') > -1) h += '<label class="lbl" for="sSub">Small line</label><input type="text" id="sSub" data-k="sub" maxlength="60" value="' + esc(o.sub) + '" placeholder="Optional">';
    if (f.indexOf('msg') > -1) h += '<label class="lbl" for="sMsg">Message</label><textarea id="sMsg" data-k="msg" rows="3" maxlength="240" placeholder="Your words">' + esc(o.msg) + '</textarea>';
    if (f.indexOf('year') > -1) h += '<div class="two"><div><label class="lbl" for="sYear">Year</label><select id="sYear" data-k="year">' + [2026, 2027, 2028].map(function (y) { return '<option' + (y == o.year ? ' selected' : '') + '>' + y + '</option>'; }).join('') + '</select></div><div><label class="lbl" for="sStart">Week starts</label><select id="sStart" data-k="start"><option value="sun"' + (o.start === 'sun' ? ' selected' : '') + '>Sunday</option><option value="mon"' + (o.start === 'mon' ? ' selected' : '') + '>Monday</option></select></div></div>';
    if (f.indexOf('count') > -1) h += '<label class="lbl" for="sCount">Stickers per row</label><select id="sCount" data-k="count">' + [3, 4, 5, 6].map(function (n) { return '<option' + (n == o.count ? ' selected' : '') + '>' + n + '</option>'; }).join('') + '</select>';
    if (f.indexOf('scale') > -1) h += '<label class="lbl" for="sScale">' + (ko() ? '패턴 크기 · ' : 'Pattern size · ') + o.scale + ' mm</label><input type="range" id="sScale" data-k="scale" min="25" max="100" step="5" value="' + o.scale + '">';
    if (f.indexOf('font') > -1) h += '<label class="lbl" for="sFont">Typeface</label><select id="sFont" data-k="font">' + Object.keys(FONTS).map(function (k) { return '<option value="' + k + '"' + (o.font === k ? ' selected' : '') + '>' + FONT_NAMES[k] + '</option>'; }).join('') + '</select>';
    if (f.indexOf('color') > -1) h += '<span class="lbl">Text color</span><div class="sw">' + COLORS.map(function (col) { return '<button data-color="' + col + '" aria-pressed="' + (o.color === col) + '" style="background:' + col + '" aria-label="Color ' + col + '"></button>'; }).join('') + '</div>';
    if (f.indexOf('bg') > -1) h += '<span class="lbl">Background</span><div class="sw">' + ['#faf8f3', '#ffffff', '#111111', '#1e3550', '#e9dfcf'].map(function (col) { return '<button data-bg="' + col + '" aria-pressed="' + (o.bg === col) + '" style="background:' + col + '" aria-label="Background ' + col + '"></button>'; }).join('') + '</div>';
    var ch = [];
    if (f.indexOf('mix') > -1) ch.push(['mix', 'Mix artworks']);
    if (f.indexOf('mat') > -1) ch.push(['mat', 'White mat and caption']);
    if (f.indexOf('cut') > -1) ch.push(['cut', 'Show cut and fold lines']);
    h += ch.map(function (x) { return '<label class="chk"><input type="checkbox" data-k="' + x[0] + '"' + (o[x[0]] ? ' checked' : '') + '> ' + tr(x[1]) + '</label>'; }).join('');
    return trH(h);
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function draw(canvas, scale, page, wm) {
    var t = cur(), d = dims(t), k = d.px ? 1 : scale, W = Math.round(d.w * (d.px ? scale : k)), H = Math.round(d.h * (d.px ? scale : k));
    if (d.px) k = scale; // px tools: 1 unit = 1 px * scale
    canvas.width = W; canvas.height = H; var c = canvas.getContext('2d');
    c.save(); if (d.px) { c.scale(scale, scale); W = d.w; H = d.h; k = 1; }
    t.draw(c, W, H, page, o, d.px ? Math.min(d.w, d.h) / 150 : k);
    c.restore(); if (wm) watermark(c, canvas.width, canvas.height);
  }
  function preview() {
    var cv = document.getElementById('sc'); if (!cv) return; var t = cur(), d = dims(t), box = document.getElementById('cwrap');
    var maxW = Math.min(box.clientWidth - 32, 640), maxH = Math.min(window.innerHeight * 0.62, 680), r = Math.min(maxW / d.w, maxH / d.h), dpr = window.devicePixelRatio || 1;
    draw(cv, r * dpr, o.page, !MA.st.unlocked); cv.style.width = Math.round(d.w * r) + 'px'; cv.style.height = Math.round(d.h * r) + 'px';
    var n = t.pages(o), names = t.pageNames;
    document.getElementById('pager').innerHTML = n > 1 ? '<button class="pill sm ghost" data-pg="-1" aria-label="Previous page"' + (o.page ? '' : ' disabled') + '>‹</button><span class="small">' + (names ? tr(names[o.page]) : (o.tool === 'wallcal' ? (o.page ? (ko() ? MONTHS_KO : MONTHS)[o.page - 1] : tr('Cover')) : (ko() ? MONTHS_KO : MONTHS)[o.page])) + ' · ' + (o.page + 1) + (ko() ? ' / ' : ' of ') + n + '</span><button class="pill sm ghost" data-pg="1" aria-label="Next page"' + (o.page < n - 1 ? '' : ' disabled') + '>›</button>' : '';
    var ex = exportScale(d);
    document.getElementById('sInfo').textContent = d.label + ' · ' + (d.px ? d.w + ' × ' + d.h + ' px' : Math.round(ex * IN) + (ko() ? 'dpi 인쇄용 파일' : ' dpi print file')) + (n > 1 ? ' · ' + n + (ko() ? '페이지' : ' pages') : '') + (MA.st.unlocked ? '' : (ko() ? ' · 구독하면 워터마크가 사라져요' : ' · Subscribe to remove the watermark'));
  }
  function exportScale(d) { if (d.px) return 1; var s = 300 / IN, area = d.w * d.h * s * s; if (area > 16e6) s = Math.sqrt(16e6 / (d.w * d.h)); return s; }
  function png() {
    var t = cur(), d = dims(t), cv = document.createElement('canvas'), s = exportScale(d);
    draw(cv, s, o.page, !MA.st.unlocked);
    cv.toBlob(function (b) { var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'arttrip-' + o.tool + '-' + o.art + (t.pages(o) > 1 ? '-p' + (o.page + 1) : '') + '.png'; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500); }, 'image/png');
    MA.toast(MA.st.unlocked ? (ko() ? '인쇄용 파일을 내려받아요' : 'Downloading print file') : (ko() ? '워터마크가 있는 미리보기를 내려받아요' : 'Downloading preview with watermark'));
  }
  function pdf() {
    var t = cur(), d = dims(t), n = t.pages(o), area = document.getElementById('printArea'), s = Math.min(exportScale(d), d.px ? 1 : 200 / IN), unit = d.px ? 'px' : 'mm';
    area.innerHTML = ''; for (var p = 0; p < n; p++) { var cv = document.createElement('canvas'); draw(cv, s, p, !MA.st.unlocked); var im = new Image(); im.src = cv.toDataURL('image/jpeg', 0.92); im.style.width = d.w + unit; im.style.height = d.h + unit; area.appendChild(im); }
    var st = document.getElementById('pageSize') || document.head.appendChild(Object.assign(document.createElement('style'), { id: 'pageSize' }));
    st.textContent = '@page{size:' + d.w + unit + ' ' + d.h + unit + ';margin:0}';
    document.body.classList.add('printing'); setTimeout(function () { window.print(); }, 300);
  }
  window.addEventListener('afterprint', function () { document.body.classList.remove('printing'); });

  function mount() {
    var root = document.querySelector('.studio'); if (!root) return;
    ready().then(function () { return document.fonts && document.fonts.load ? Promise.all(['600 20px "Playfair Display"', '600 20px "Cormorant Garamond"', '600 20px "Dancing Script"', '500 20px Inter'].map(function (f) { return document.fonts.load(f).catch(function () {}); })) : 0; }).then(preview);
    root.addEventListener('click', function (e) {
      var b = e.target.closest('[data-art],[data-color],[data-bg],[data-pg]'); if (!b) return;
      if (b.dataset.art) { o.art = b.dataset.art; ready().then(preview); var so = document.getElementById('sopts'); var y = window.scrollY; so.innerHTML = opts(); window.scrollTo(0, y); } if (b.dataset.color) o.color = b.dataset.color; if (b.dataset.bg) o.bg = b.dataset.bg;
      if (b.dataset.pg) { o.page = Math.max(0, Math.min(cur().pages(o) - 1, o.page + +b.dataset.pg)); }
      root.querySelectorAll('[data-art]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.art === o.art)); });
      root.querySelectorAll('[data-color]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.color === o.color)); });
      root.querySelectorAll('[data-bg]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.bg === o.bg)); });
      preview();
    });
    root.addEventListener('input', function (e) {
      var el = e.target, k = el.dataset.k; if (!k) return;
      o[k] = el.type === 'checkbox' ? el.checked : (['size', 'year', 'count', 'scale'].indexOf(k) > -1 ? +el.value : el.value);
      if (k === 'size') o.page = Math.min(o.page, cur().pages(o) - 1);
      if (k === 'scale') { var l = root.querySelector('label[for=sScale]'); if (l) l.textContent = (ko() ? '패턴 크기 · ' : 'Pattern size · ') + o.scale + ' mm'; }
      preview();
    });
    document.getElementById('sPng').onclick = png; document.getElementById('sPdf').onclick = pdf;
    window.addEventListener('resize', preview);
  }
  return { html: html, mount: mount, tools: T, state: function () { return JSON.parse(JSON.stringify(o)); }, load: function (x) { if (x && T[x.tool]) Object.keys(o).forEach(function (k) { if (k in x) o[k] = x[k]; }); } };
})();
