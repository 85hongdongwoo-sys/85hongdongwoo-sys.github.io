// Large catalog of generated products (calendars, art-print sets, postcard sets, coloring books).
// Data lives in KV (env.VIDS) under pk:index and pk:item:<slug>, written by the private /api/pk/put endpoint.
// PDFs are built in the buyer's browser after the licence key from the receipt is checked against the product's benefit.

const IMG_HOSTS = ['openaccess-cdn.clevelandart.org', 'images.metmuseum.org', 'www.parismuseescollections.paris.fr', 'parismuseescollections.paris.fr', 'api.nga.gov', 'media.nga.gov'];
let IDX = null, IDX_AT = 0;

export const KIND = {
  cal: { en: 'Wall calendar 2027–2030', ko: '벽걸이 달력 2027–2030', icon: '📅' },
  prints: { en: 'Printable art prints set', ko: '인쇄용 명화 포스터 세트', icon: '🖼' },
  cards: { en: 'Printable postcard set', ko: '인쇄용 엽서 세트', icon: '✉' },
  color: { en: 'Coloring book', ko: '컬러링북', icon: '🖍' },
  puz: { en: 'Large-print puzzle book', ko: '큰 글씨 퍼즐북', icon: '🧩' },
};
const KIND_ORDER = ['cal', 'prints', 'cards', 'puz', 'color'];

export async function pkIndex(env) {
  if (IDX && Date.now() - IDX_AT < 300000) return IDX;
  const j = env.VIDS ? await env.VIDS.get('pk:index', { type: 'json', cacheTtl: 300 }) : null;
  IDX = Array.isArray(j) ? j : []; IDX_AT = Date.now(); return IDX;
}
const CH = new Map();
async function pkItem(env, slug) {
  if (!env.VIDS) return null;
  const x = (await pkIndex(env)).find((i) => i.s === slug); if (!x) return null;
  let c = CH.get(x.ch);
  if (!c || Date.now() - c.at > 300000) { c = { at: Date.now(), d: (await env.VIDS.get('pk:ch:' + x.ch, { type: 'json', cacheTtl: 300 })) || {} }; CH.set(x.ch, c); }
  return c.d[slug] || null;
}

const sha = async (s) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)))).map((b) => b.toString(16).padStart(2, '0')).join('');
const J = (o, st = 200, h = {}) => new Response(JSON.stringify(o), { status: st, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', ...h } });
const CORS = { 'access-control-allow-origin': '*', 'access-control-allow-methods': 'POST, OPTIONS', 'access-control-allow-headers': 'content-type' };

// ---------- private writer (token-protected) ----------
export async function pkPut(req, env) {
  if (req.method === 'OPTIONS') return new Response(null, { headers: CORS });
  if (!env.PK_HASH || !env.VIDS) return J({ ok: false }, 501, CORS);
  let b; try { b = await req.json(); } catch { return J({ ok: false }, 400, CORS); }
  if ((await sha(String(b.tok || ''))) !== env.PK_HASH) return J({ ok: false }, 403, CORS);
  const puts = Array.isArray(b.puts) ? b.puts : [];
  for (const [k, v] of puts) if (/^pk:/.test(k)) await env.VIDS.put(k, typeof v === 'string' ? v : JSON.stringify(v));
  const dels = Array.isArray(b.dels) ? b.dels : [];
  for (const k of dels) if (/^pk:/.test(k)) await env.VIDS.delete(k);
  IDX = null; CH.clear();
  return J({ ok: true, n: puts.length, d: dels.length }, 200, CORS);
}

// ---------- image proxy (allow-listed museum hosts only) ----------
export async function pkImg(url, ctx) {
  const u = url.searchParams.get('u') || '';
  let t; try { t = new URL(u); } catch { return new Response('bad', { status: 400 }); }
  if (t.protocol !== 'https:' || !IMG_HOSTS.includes(t.hostname)) return new Response('host', { status: 403 });
  const key = new Request('https://arttripstudio.com/pi?u=' + encodeURIComponent(u));
  const hit = await caches.default.match(key); if (hit) return hit;
  const r = await fetch(u, { headers: { 'user-agent': 'ArttripStudio/1.0 (+https://arttripstudio.com)' }, cf: { cacheTtl: 2592000, cacheEverything: true } });
  if (!r.ok) return new Response('upstream ' + r.status, { status: 502 });
  const res = new Response(r.body, { headers: { 'content-type': r.headers.get('content-type') || 'image/jpeg', 'cache-control': 'public, max-age=2592000', 'access-control-allow-origin': '*' } });
  ctx && ctx.waitUntil && ctx.waitUntil(caches.default.put(key, res.clone()));
  return res;
}
const pi = (u) => (u && u[0] === '/') ? u : '/pi?u=' + encodeURIComponent(u || '');

// ---------- unlock: licence key must belong to this product's benefit (or an all-access benefit) ----------
export async function pkUnlock(req, env) {
  let b = {}; try { b = await req.json(); } catch { }
  const slug = String(b.slug || ''), key = String(b.key || '').trim().slice(0, 100);
  const it = await pkItem(env, slug); if (!it || !key) return J({ ok: false });
  let ok = !!(env.EDITOR_MASTER_KEY && key === env.EDITOR_MASTER_KEY);
  if (!ok && env.POLAR_ORG_ID) {
    try {
      const r = await fetch('https://api.polar.sh/v1/customer-portal/license-keys/validate', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ key, organization_id: env.POLAR_ORG_ID }) });
      const j = await r.json().catch(() => ({}));
      const all = String(env.PK_ALL_BENEFITS || '').split(',').filter(Boolean);
      ok = r.ok && j.status === 'granted' && (j.benefit_id === it.b || all.includes(j.benefit_id));
    } catch { ok = false; }
  }
  if (!ok) return J({ ok: false });
  if (it.k === 'puz') return J({ ok: true, k: 'puz', title: it.en.name, pz: it.pz });
  return J({ ok: true, k: it.k, title: it.en.name, works: it.w.map((w) => ({ t: w.t, a: w.a, d: w.d, u: pi(w.u || w.v), W: w.W, H: w.H })) });
}

// ---------- copy ----------
function copy(it, lang) {
  const ko = lang === 'ko', c = it[lang] || it.en, k = KIND[it.k], n = (it.w || []).length;
  if (it.k === 'puz') { const z = it.pz, lv = { easy: ko ? '쉬움' : 'easy', medium: ko ? '보통' : 'medium', hard: ko ? '어려움' : 'hard' }[z.level], nm = { ws: ko ? '낱말찾기' : 'word search', sudoku: ko ? '스도쿠' : 'sudoku', maze: ko ? '미로' : 'maze' }[z.type];
    return { name: c.name, body: ko ? [`어르신도 편하게 볼 수 있는 큰 글씨 ${nm} ${z.n}문제 모음이에요(난이도: ${lv}).${z.type === 'ws' ? ` 주제는 '${c.theme || z.theme}'이고 한 문제에 단어 10~14개가 숨어 있어요.` : ''} 한 장에 한 문제씩, 칸과 글자를 크게 만들었어요.`, `맨 뒤에 정답이 모두 들어 있어요. 결제 후 A4나 레터 용지 PDF로 받아 몇 번이든 다시 인쇄할 수 있어서 복지관, 요양원, 가족 모임에서 쓰기 좋아요.`]
      : [`${z.n} large-print ${nm} puzzles (${lv})${z.type === 'ws' ? ` on the theme '${z.theme}', each hiding 10 to 14 words` : ''}. One puzzle per page with big, clear letters and boxes that are easy on the eyes.`, `All answers are at the back. Download as A4 or US Letter PDF and print as many copies as you like, for yourself, a parent or grandparent, a care home or an activity group.`] }; }
  const who = it.g === 'artist' ? (ko ? (it.ko.who || it.en.who) : it.en.who) : (ko ? (it.ko.theme || it.en.theme) : it.en.theme);
  const body = {
    cal: ko ? [`${who}의 그림 ${n}점으로 만든 벽걸이 달력이에요. 표지 1장과 1월부터 12월까지 달마다 그림 한 점, 그 아래 날짜 칸이 있어요. 한 번 사면 2027년부터 2030년까지 원하는 해의 달력을 모두 받을 수 있어요.`, `미술관이 저작권 없이 공개한 고해상도 원본으로 만들어 A4나 레터 용지에 바로 인쇄할 수 있어요. 결제 후 영수증의 라이선스 키로 PDF를 내려받아요.`]
      : [`A wall calendar with ${n} works by ${who}: a cover page plus one picture for every month from January to December, with a clean date grid below. One purchase covers every year from 2027 to 2030, so you can print a fresh one each January.`, `Made from high-resolution open-access museum files, ready to print on A4 or US Letter paper. Download the PDF with the licence key from your receipt.`],
    prints: ko ? [`${who}의 그림 ${n}점을 한 장에 한 점씩 담은 인쇄용 포스터 세트예요. 액자에 넣거나 벽에 붙이기 좋아요.`, `A4·레터·A3 크기로 내려받아 집이나 사무실 프린터, 인쇄소에서 뽑을 수 있어요.`]
      : [`${n} printable art prints of ${who}, one picture per page with a small caption, perfect for frames, gallery walls and gifts.`, `Download as A4, US Letter or A3 PDFs and print at home or at a print shop.`],
    cards: ko ? [`${who}의 그림 ${n}점으로 만든 엽서 세트예요. A4 한 장에 엽서 4장이 들어가고 자르는 선이 표시돼 있어요.`, `두꺼운 종이에 인쇄해 잘라서 카드, 초대장, 책갈피로 쓰세요.`]
      : [`A set of ${n} postcards featuring ${who}, four cards per A4 or Letter page with crop marks.`, `Print on card stock and cut out for notes, invitations, party favours and scrapbooks.`],
    color: ko ? [`${who}에서 고른 옛 판화와 드로잉 ${n}점을 색칠하기 좋은 선 그림으로 바꾼 어른용 컬러링북이에요.`, `한 장에 그림 하나씩, 원작 제목과 작가를 작게 적었어요. 몇 번이든 다시 인쇄해서 색칠할 수 있어요.`]
      : [`A grown-up coloring book of ${n} pages made from antique prints and drawings of ${who}, cleaned up into crisp line art.`, `One picture per page with the original title and artist. Print as many copies as you like.`],
  }[it.k];
  return { name: c.name, short: c.short || body[0], body };
}

const card = (it, lang, L, esc) => `<a class="pcard" href="${L(lang, '/shop/c/' + it.s)}"><div class="pimg"><img src="${pi(it.v)}" alt="${esc((it[lang] || it.en).name)}" loading="lazy"></div><b>${esc((it[lang] || it.en).name)}</b><span>${esc(KIND[it.k][lang])}</span><em>$${it.p}</em></a>`;

// ---------- catalogue listing ----------
export async function pkList(lang, env, url, h) {
  const { layout, html, esc, L, T } = h; const ko = lang === 'ko', t = T[lang];
  const all = await pkIndex(env); if (!all.length) return null;
  const k = url.searchParams.get('k') || '', g = url.searchParams.get('g') || '', q = (url.searchParams.get('q') || '').toLowerCase().slice(0, 60);
  let list = all.filter((x) => (!k || x.k === k) && (!g || x.g === g) && (!q || (x.en.name + ' ' + (x.ko && x.ko.name)).toLowerCase().includes(q)));
  const per = 48, pages = Math.max(1, Math.ceil(list.length / per)), page = Math.min(pages, Math.max(1, +(url.searchParams.get('p') || 1)));
  const qs = (o) => { const s = new URLSearchParams(); const v = { k, g, q, ...o }; for (const [a, b] of Object.entries(v)) if (b && !(a === 'p' && b === 1)) s.set(a, b); const x = s.toString(); return L(lang, '/shop/c') + (x ? '?' + x : ''); };
  const chip = (label, href, on) => `<a href="${href}"${on ? ' aria-current="true"' : ''}>${esc(label)}</a>`;
  const body = `<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/shop')}">${t.nav.shop}</a></nav><span class="lbl">${ko ? `${all.length}종` : `${all.length} products`}</span><h1>${ko ? '명화 달력·포스터·엽서·컬러링북' : 'Masterpiece calendars, prints, postcards & coloring books'}</h1>
<p class="sub">${ko ? '세계 미술관이 공개한 명화로 만든 인쇄용 디지털 상품이에요. 결제 후 바로 PDF로 받아요.' : 'Printable digital products made from open-access museum masterpieces. Instant PDF download.'}</p>
<form class="row" action="${L(lang, '/shop/c')}" style="margin:14px 0"><input name="q" value="${esc(q)}" placeholder="${ko ? '작가나 주제 검색 (예: Monet, cats)' : 'Search an artist or theme (e.g. Monet, cats)'}" style="flex:1;min-width:0;padding:10px 14px;border:1px solid #d9d1c3;border-radius:999px;font:inherit">${k ? `<input type="hidden" name="k" value="${esc(k)}">` : ''}</form>
<div class="chips wrapc">${chip(ko ? '전체' : 'All', qs({ k: '', p: 1 }), !k)}${KIND_ORDER.map((x) => chip(KIND[x][lang], qs({ k: x, p: 1 }), k === x)).join('')}</div>
<div class="chips wrapc" style="margin-top:8px">${chip(ko ? '작가별' : 'By artist', qs({ g: g === 'artist' ? '' : 'artist', p: 1 }), g === 'artist')}${chip(ko ? '주제별' : 'By theme', qs({ g: g === 'theme' ? '' : 'theme', p: 1 }), g === 'theme')}</div>
<div class="pgrid" style="margin-top:22px">${list.slice((page - 1) * per, page * per).map((x) => card(x, lang, L, esc)).join('') || `<p>${ko ? '찾는 상품이 없어요.' : 'Nothing found.'}</p>`}</div>
${pages > 1 ? `<nav class="pager">${page > 1 ? `<a href="${qs({ p: page - 1 })}">←</a>` : ''}<span>${page} / ${pages}</span>${page < pages ? `<a href="${qs({ p: page + 1 })}">→</a>` : ''}</nav>` : ''}</section>`;
  return html(layout(lang, { title: `${ko ? '명화 달력·포스터·엽서·컬러링북' : 'Masterpiece calendars, prints, postcards & coloring books'}${page > 1 ? ` (${page})` : ''} — ${t.site}`, desc: ko ? '세계 미술관 명화로 만든 인쇄용 달력, 포스터, 엽서, 컬러링북.' : 'Printable calendars, art prints, postcards and coloring books from museum masterpieces.', path: '/shop/c', body, noindex: !!(q || page > 1 && (k || g)) }));
}

// ---------- product page ----------
export async function pkPage(lang, env, slug, h) {
  const { layout, html, esc, L, T } = h; const ko = lang === 'ko', t = T[lang];
  const it = await pkItem(env, slug); if (!it) return null;
  const c = copy(it, lang), k = KIND[it.k];
  const sibs = (await pkIndex(env)).filter((x) => x.f === it.f && x.s !== it.s).slice(0, 6);
  const btn = it.c ? `<a class="paybtn gl" href="${esc(it.c)}" rel="noopener"><b>${ko ? '해외결제' : t.buy}</b><span>${ko ? '카드 · Apple Pay · Google Pay' : 'Card · Apple Pay · Google Pay'}</span></a>` : `<span class="paybtn off"><b>${t.buy}</b><span>${t.soon}</span></span>`;
  const body = `<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/shop')}">${t.nav.shop}</a> › <a href="${L(lang, '/shop/c?k=' + it.k)}">${esc(k[lang])}</a></nav><div class="agrid">
<figure class="big"><img src="${pi(it.v || it.w[0].v || it.w[0].u)}" alt="${esc(c.name)}"></figure><div class="meta"><span class="lbl">${t.instant} · ${esc(k[lang])}</span><h1>${esc(c.name)}</h1>
${c.body.map((x) => `<p>${esc(x)}</p>`).join('')}
<div class="buy"><div class="price">$${it.p}</div><div class="paybtns">${btn}</div><p class="small">✓ ${t.guest}</p><p class="small"><a href="${L(lang, '/dl/' + it.s)}">${ko ? '이미 구매했어요 → 라이선스 키로 받기' : 'Already bought? Download with your licence key →'}</a></p></div></div></div>
${it.k === 'puz' ? '' : `<h2 class="h3" style="margin-top:34px">${ko ? `들어 있는 그림 ${it.w.length}점` : `The ${it.w.length} works inside`}</h2>
<div class="stgrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px">${it.w.map((w) => `<figure style="margin:0"><img src="${pi(w.v || w.u)}" alt="${esc(w.t)}" loading="lazy" style="width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px;background:#eee"><figcaption class="small" style="margin-top:6px;overflow-wrap:anywhere">${esc(w.t)}${w.d ? ', ' + esc(w.d) : ''}<br><span style="opacity:.7">${esc(w.a || '')}</span></figcaption></figure>`).join('')}</div>`}
${sibs.length ? `<h2 class="h3" style="margin-top:34px">${ko ? '같은 그림으로 만든 다른 상품' : 'Same pictures, other formats'}</h2><div class="pgrid">${sibs.map((x) => card(x, lang, L, esc)).join('')}</div>` : ''}</section>`;
  const jsonld = { '@context': 'https://schema.org', '@type': 'Product', name: it.en.name, image: 'https://arttripstudio.com' + pi(it.v || it.w[0].v || it.w[0].u), description: copy(it, 'en').body[0], offers: { '@type': 'Offer', price: it.p, priceCurrency: 'USD', availability: it.c ? 'https://schema.org/InStock' : 'https://schema.org/PreOrder' } };
  return html(layout(lang, { title: `${c.name} — ${t.site}`, desc: c.body[0].slice(0, 155), path: '/shop/c/' + it.s, body, img: pi(it.v || it.w[0].v || it.w[0].u), jsonld }));
}

// ---------- download page (PDF built in the browser) ----------
export async function pkDownload(lang, env, slug, h) {
  const { layout, html, esc, L, T } = h; const ko = lang === 'ko', t = T[lang];
  const it = await pkItem(env, slug); if (!it) return null;
  const sizes = it.k === 'prints' ? ['A4', 'Letter', 'A3'] : ['A4', 'Letter'];
  const body = `<section class="wrap sec narrow"><nav class="crumb"><a href="${L(lang, '/shop/c/' + it.s)}">${esc((it[lang] || it.en).name)}</a></nav><h1>${ko ? 'PDF 내려받기' : 'Download your PDF'}</h1>
<p class="sub">${ko ? '결제 영수증 메일에 있는 라이선스 키를 넣어 주세요. 파일은 이 브라우저에서 바로 만들어져요(그림이 많으면 1~2분 걸려요).' : 'Enter the licence key from your receipt email. The file is put together right here in your browser (large sets can take a minute or two).'}</p>
<div class="dl" style="text-align:left"><label class="small">${ko ? '라이선스 키' : 'Licence key'}</label><input id="k" autocomplete="off" style="width:100%;padding:10px 12px;margin:6px 0 12px;border:1px solid #d9d1c3;border-radius:10px;font:inherit">
<label class="small">${ko ? '용지 크기' : 'Paper size'}</label><div class="row" id="sz" style="margin:6px 0 14px">${sizes.map((s, i) => `<label style="margin-right:14px"><input type="radio" name="sz" value="${s}"${i ? '' : ' checked'}> ${s}</label>`).join('')}</div>
${it.k === 'cal' ? `<label class="small">${ko ? '연도' : 'Year'}</label><div class="row" style="margin:6px 0 14px;flex-wrap:wrap">${[2027, 2028, 2029, 2030].map((y, i) => `<label style="margin-right:14px"><input type="radio" name="yr" value="${y}"${i ? '' : ' checked'}> ${y}</label>`).join('')}</div>` : ''}
<button class="pill" id="go">${ko ? 'PDF 만들기' : 'Make my PDF'}</button><p class="small" id="st" style="margin-top:12px"></p></div></section>
<script src="/editor/jspdf.umd.min.js"></script><script src="/js/pk.js?v=2"></script><script>PK.init(${JSON.stringify({ slug: it.s, lang, ko })})</script>`;
  return html(layout(lang, { title: `${ko ? 'PDF 내려받기' : 'Download'} — ${t.site}`, desc: '', path: '/dl/' + it.s, body, noindex: true }));
}

// ---------- sitemap paths ----------
export async function pkPaths(env) { return (await pkIndex(env)).map((x) => '/shop/c/' + x.s).concat(['/shop/c']); }

// ---------- puzzle book cover (SVG) ----------
export async function pkCover(env, slug) {
  const it = await pkItem(env, slug); if (!it || it.k !== 'puz') return new Response('nf', { status: 404 });
  const z = it.pz, e = (x) => String(x).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const pal = { ws: ['#f3e6c8', '#8a3b2b'], sudoku: ['#dfe8f1', '#23466b'], maze: ['#e3efd9', '#2f5d34'] }[z.type];
  let R = z.seed >>> 0; const rnd = () => ((R = (R * 1664525 + 1013904223) >>> 0) / 4294967296);
  let motif = '';
  if (z.type === 'ws') { const L = 'ABCDEFGHIJKLMNOPRSTUW'; for (let r = 0; r < 7; r++) for (let c = 0; c < 7; c++) motif += `<text x="${330 + c * 64}" y="${560 + r * 64}" font-size="44" font-family="Courier New,monospace" font-weight="700" fill="${pal[1]}" opacity=".85" text-anchor="middle">${L[Math.floor(rnd() * L.length)]}</text>`; }
  else if (z.type === 'sudoku') { for (let i = 0; i <= 9; i++) motif += `<line x1="280" y1="${500 + i * 50}" x2="730" y2="${500 + i * 50}" stroke="${pal[1]}" stroke-width="${i % 3 ? 2 : 6}"/><line x1="${280 + i * 50}" y1="500" x2="${280 + i * 50}" y2="950" stroke="${pal[1]}" stroke-width="${i % 3 ? 2 : 6}"/>`; for (let k = 0; k < 30; k++) motif += `<text x="${305 + Math.floor(rnd() * 9) * 50}" y="${538 + Math.floor(rnd() * 9) * 50}" font-size="34" font-family="Arial" font-weight="700" text-anchor="middle" fill="${pal[1]}">${1 + Math.floor(rnd() * 9)}</text>`; }
  else { for (let k = 0; k < 90; k++) { const x = 280 + Math.floor(rnd() * 9) * 50, y = 500 + Math.floor(rnd() * 9) * 50; motif += rnd() < .5 ? `<line x1="${x}" y1="${y}" x2="${x + 50}" y2="${y}" stroke="${pal[1]}" stroke-width="7" stroke-linecap="round"/>` : `<line x1="${x}" y1="${y}" x2="${x}" y2="${y + 50}" stroke="${pal[1]}" stroke-width="7" stroke-linecap="round"/>`; } motif += `<rect x="280" y="500" width="450" height="450" fill="none" stroke="${pal[1]}" stroke-width="8"/>`; }
  const t = e(it.en.name), lines = []; let cur = ''; for (const w of t.split(' ')) { if ((cur + ' ' + w).trim().length > 24) { lines.push(cur.trim()); cur = w; } else cur += ' ' + w; } lines.push(cur.trim());
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" width="1000" height="1200"><rect width="1000" height="1200" fill="${pal[0]}"/><rect x="40" y="40" width="920" height="1120" fill="none" stroke="${pal[1]}" stroke-width="4"/>
${lines.slice(0, 3).map((l, i) => `<text x="500" y="${160 + i * 78}" font-size="66" font-family="Georgia,serif" font-weight="700" text-anchor="middle" fill="${pal[1]}">${l}</text>`).join('')}
<text x="500" y="${180 + Math.min(3, lines.length) * 78}" font-size="34" font-family="Arial" text-anchor="middle" fill="#444">LARGE PRINT · ${z.n} PUZZLES · ANSWERS INCLUDED</text>${motif}
<text x="500" y="1110" font-size="30" font-family="Georgia,serif" text-anchor="middle" fill="#555">Arttrip Studio</text></svg>`;
  return new Response(svg, { headers: { 'content-type': 'image/svg+xml', 'cache-control': 'public, max-age=86400' } });
}
