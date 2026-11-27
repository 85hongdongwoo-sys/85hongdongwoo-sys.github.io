import { VERSE_TOPICS } from './verses.js';
import { QUOTE_TOPICS } from './quotes.js';
import { PHOTOS } from './photos.js';
// Arttrip Studio — pages are generated on request from D1 data, in English and Korean.
import { T, THEMES, PRODUCTS, IL_CATS, IL_STYLES, colorName } from './i18n.js';
import { memdb } from './memdb.js';
import { api, currentUser, membersReady } from './auth.js';

const PER_PAGE = 48;
let ORIGIN = '';
const SITEMAP_SIZE = 45000;
const BOT = /bot|crawl|spider|slurp|bingpreview|facebookexternalhit|embedly|quora|pinterest|whatsapp|telegram|lighthouse|headless/i;

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const html = (body, status = 200, extra = {}) => new Response(body, { status, headers: { 'content-type': 'text/html; charset=utf-8', ...extra } });
const xml = (body) => new Response(body, { headers: { 'content-type': 'application/xml; charset=utf-8', 'cache-control': 'public, max-age=3600' } });

export default {
  async fetch(req, env, ctx) {
    if (!env.DB) env = { ...env, DB: memdb }; // no D1 bound yet → bundled data
    const url = new URL(req.url);
    ORIGIN = env.SITE_ORIGIN || url.origin;
    let path = url.pathname.replace(/\/+$/, '') || '/';

    // explicit language choice: ?setlang=ko|en → remember and redirect
    const set = url.searchParams.get('setlang');
    if (set === 'ko' || set === 'en') {
      const base = path.replace(/^\/ko(?=\/|$)/, '') || '/';
      const to = set === 'ko' ? '/ko' + (base === '/' ? '' : base) : base;
      return new Response(null, { status: 302, headers: { location: to || '/', 'set-cookie': `lang=${set}; Path=/; Max-Age=31536000; SameSite=Lax` } });
    }

    const isKo = path === '/ko' || path.startsWith('/ko/');
    const lang = isKo ? 'ko' : 'en';
    const rest = isKo ? (path.slice(3) || '/') : path;

    // first visit from a Korean browser → Korean page (people only, never crawlers)
    if (!isKo && req.method === 'GET' && !/^\/(sitemap|robots|img|il|p|ph|css|js|api|studio\/)/.test(rest)) {
      const cookie = req.headers.get('cookie') || '';
      const ua = req.headers.get('user-agent') || '';
      if (!/(?:^|;\s*)lang=/.test(cookie) && !BOT.test(ua) && /^ko\b/i.test(req.headers.get('accept-language') || '')) {
        return new Response(null, { status: 302, headers: { location: '/ko' + (rest === '/' ? '' : rest) + url.search, 'set-cookie': 'lang=ko; Path=/; Max-Age=31536000; SameSite=Lax', vary: 'Accept-Language' } });
      }
    }

    if (path.startsWith('/ph/')) return photoProxy(path, ctx);

    // cached HTML
    const cache = caches.default;
    const cacheKey = new Request(url.origin + path + url.search, { method: 'GET' });
    const noCache = /^\/(api|account)/.test(rest);
    if (req.method === 'GET' && env.CACHE_HTML !== 'off' && !noCache) { const hit = await cache.match(cacheKey); if (hit) return hit; }

    let res;
    try { res = await route(rest, url, lang, env, req); } catch (e) { res = html(`<pre>${esc(e.stack || e)}</pre>`, 500); }
    if (!res) res = await notFound(lang, rest);
    if (!noCache && res.status === 200 && req.method === 'GET' && (res.headers.get('content-type') || '').startsWith('text/html')) {
      res = new Response(res.body, res); res.headers.set('cache-control', 'public, max-age=600'); res.headers.set('vary', 'Accept-Language, Cookie');
      if (env.CACHE_HTML !== 'off') ctx.waitUntil(cache.put(cacheKey, res.clone()));
    }
    return res;
  },
};

async function route(p, url, lang, env, REQ) {
  let m;
  if (p === '/robots.txt') return new Response(`User-agent: *\nAllow: /\nSitemap: ${url.origin}/sitemap.xml\n`, { headers: { 'content-type': 'text/plain' } });
  if (p === '/sitemap.xml') return sitemapIndex(url, env);
  if ((m = p.match(/^\/sitemaps\/(art|pages)-(en|ko)-(\d+)\.xml$/))) return sitemapPart(url, env, m[1], m[2], +m[3]);
  if (p === '/api/art.json') return url.searchParams.get('all') ? libData(env) : studioData(url, env);
  if (p === '/api/license' && REQ.method === 'POST') return license(REQ, env);
  if (p === '/api/verses') return verses(url, env);
  if (p === '/api/quotes') return quotesApi(url, env);
  if (p === '/api/lineart') return lineart(url, env);
  if (p === '/editor') return editor(lang, url);
  if (p.startsWith('/api/')) return api(p, REQ, env);
  if (p === '/studio') return studio(lang, env);
  if (p === '/account') return account(lang, env, REQ);
  if (p === '/thanks') return thanks(lang, url);
  if (p === '/') return home(lang, env);
  if (p === '/art') return gallery(lang, env, url, null);
  if ((m = p.match(/^\/art\/theme\/([a-z-]+)$/)) && THEMES[m[1]]) return gallery(lang, env, url, { theme: m[1] });
  if ((m = p.match(/^\/artist\/([a-z0-9-]+)$/))) return gallery(lang, env, url, { artist: m[1] });
  if ((m = p.match(/^\/art\/([a-z0-9-]+)$/))) return artwork(lang, env, m[1]);
  if (p === '/collections') return collections(lang);
  if ((m = p.match(/^\/collections\/(architecture|landscape)$/))) return photoGallery(lang, m[1]);
  if (p === '/originals') return originals(lang);
  if (p === '/illustrations') return illus(lang, null);
  if ((m = p.match(/^\/illustrations\/([a-z-]+)$/)) && IL_CATS[m[1]]) return illus(lang, m[1]);
  if (p === '/shop') return shop(lang);
  if ((m = p.match(/^\/shop\/([a-z0-9-]+)$/))) return product(lang, env, m[1]);
  if (p === '/pricing') return pricing(lang, env);
  if (['/about', '/license', '/privacy', '/terms'].includes(p)) return info(lang, p.slice(1));
  return null;
}

// ---------- layout ----------
const L = (lang, p) => (lang === 'ko' ? '/ko' : '') + (p === '/' && lang === 'ko' ? '' : p);
function layout(lang, { title, desc, path, body, img, jsonld, head = '', noindex = false }) {
  const t = T[lang]; const other = lang === 'ko' ? 'en' : 'ko';
  const enUrl = ORIGIN + path, koUrl = ORIGIN + '/ko' + (path === '/' ? '' : path);
  const nav = [['col', '/collections'], ['illus', '/originals'], ['studio', '/studio'], ['shop', '/shop'], ['pricing', '/pricing']].map(([k, href]) => `<a href="${L(lang, href)}">${t.nav[k]}</a>`).join('');
  return `<!DOCTYPE html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${lang === 'ko' ? koUrl : enUrl}"><link rel="alternate" hreflang="en" href="${enUrl}"><link rel="alternate" hreflang="ko" href="${koUrl}"><link rel="alternate" hreflang="x-default" href="${enUrl}">
<meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}">${img ? `<meta property="og:image" content="${esc(ORIGIN + img)}">` : ''}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">${head}${noindex ? '<meta name="robots" content="noindex">' : ''}${jsonld ? `<script type="application/ld+json">${JSON.stringify(jsonld).replace(/</g, '\\u003c')}</script>` : ''}</head>
<body class="${lang}"><header class="top"><div class="wrap bar"><a class="logo" href="${L(lang, '/')}">Arttrip<span>Studio</span></a><nav>${nav}</nav>
<a class="acct" href="${L(lang, '/account')}" aria-label="${t.nav.myAccount}"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg></a><a class="lang" href="?setlang=${other}" hreflang="${other}">${t.switchTo}</a></div></header>
<main>${body}</main>
<footer class="foot"><div class="wrap"><div class="fl"><a class="logo" href="${L(lang, '/')}">Arttrip<span>Studio</span></a><p>${esc(t.footer)}</p></div>
<div class="fr">${['about', 'license', 'privacy', 'terms'].map((k) => `<a href="${L(lang, '/' + k)}">${t[k]}</a>`).join('')}</div></div></footer>
<script src="/js/site.js" defer></script></body></html>`;
}

// ---------- data helpers ----------
const tl = (a, lang) => (lang === 'ko' && a.title_ko ? a.title_ko : a.title);
const al = (a, lang) => (lang === 'ko' && a.artist_ko ? a.artist_ko : a.artist);
function tile(a, lang) {
  return `<a class="tile" href="${L(lang, '/art/' + a.slug)}"><div class="ph" style="aspect-ratio:${a.w}/${a.h}"><img src="/img/${a.id}.jpg" alt="${esc(tl(a, lang))} — ${esc(al(a, lang))}" loading="lazy" decoding="async" width="${a.w}" height="${a.h}"></div><b>${esc(tl(a, lang))}</b><span>${esc(al(a, lang))}</span></a>`;
}
async function all(env, sql, ...args) { return (await env.DB.prepare(sql).bind(...args).all()).results; }
async function one(env, sql, ...args) { return env.DB.prepare(sql).bind(...args).first(); }

// ---------- pages ----------
async function home(lang, env) {
  const t = T[lang];
  const feat = await all(env, "SELECT * FROM artworks WHERE id IN ('89503','87088','14598','100829','33406','16617','59927','16549') ");
  const hero = feat.find((a) => a.id === '89503') || feat[0];
  const counts = await all(env, 'SELECT theme, COUNT(*) n, MIN(id) id FROM artworks GROUP BY theme ORDER BY n DESC');
  const cover = await all(env, "SELECT theme, id FROM artworks WHERE id IN (SELECT MIN(id) FROM artworks GROUP BY theme)");
  const covers = { ...Object.fromEntries(cover.map((c) => [c.theme, c.id])), birds: '222003', horses: '97890' };
  const total = counts.reduce((s, c) => s + c.n, 0);
  const ko = lang === 'ko';
  const rail = (list) => `<div class="rail">${list.map((p) => productCard(p, lang)).join('')}</div>`;
  const pick = (id) => feat.find((a) => a.id === id) || feat[0];
  const side = [pick('87088'), pick('14598')];
  const bento = [
    ['b1', L(lang, '/shop') + '#calendars', '/p/calendar-flowers.jpg', ko ? '명화 달력 2027' : '2027 art calendars', ko ? '화가 15명 · A4와 레터' : '15 artists · A4 and Letter'],
    ['b2', L(lang, '/shop/masterpiece-junk-journal-art-paper-kit'), '/p/art-paper-kit.jpg', ko ? '아트페이퍼 키트' : 'Art paper kit', ko ? '정크저널 14종 + 편집기' : '14 junk journal papers + editor'],
    ['b3', L(lang, '/editor') + '?tpl=exhibit&new=1', `/img/${side[1].id}.jpg`, ko ? '명화 포스터' : 'Masterpiece posters', ko ? 'A3부터 24×36인치까지' : 'A3 up to 24×36 in'],
    ['b4', L(lang, '/originals'), '/p/cafe-girl-clipart.jpg', ko ? '아트트립 오리지널' : 'Arttrip Originals', ko ? '일러스트 · 패턴 · 글씨' : 'Illustration · pattern · lettering'],
  ].map(([c, href, img, h, d]) => `<a class="bx ${c}" href="${href}"><img src="${img}" alt="" loading="lazy"><span><b>${esc(h)}</b><i>${esc(d)}</i></span></a>`).join('');
  const body = `<section class="hx"><div class="wrap hxg"><div class="hxt"><span class="eyebrow">${ko ? '명화 · 사진 · 일러스트 · 글씨' : 'Art · Photography · Illustration · Lettering'}</span><h1>${esc(t.heroTitle)}</h1><p class="sub">${esc(t.heroSub)}</p>
<div class="row"><a class="pill lt" href="${L(lang, '/editor')}?new=1">${ko ? '편집기로 만들기' : 'Start designing'}</a><a class="pill gh" href="${L(lang, '/shop')}">${ko ? '상품 보기' : 'Shop products'}</a></div>
<ul class="stats"><li><b>300<small>dpi</small></b><span>${ko ? '인쇄용 고화질' : 'print quality'}</span></li><li><b>A4<small>+Letter</small></b><span>${ko ? '두 가지 크기' : 'both sizes'}</span></li><li><b>0<small>${ko ? '초' : 's'}</small></b><span>${ko ? '결제 후 바로 다운로드' : 'wait to download'}</span></li></ul></div>
<div class="hxa"><a class="ha1" href="${L(lang, '/art/' + hero.slug)}"><img src="/img/${hero.id}.jpg" alt="${esc(tl(hero, lang))}" width="${hero.w}" height="${hero.h}"></a>${side.map((a, i) => `<a class="ha${i + 2}" href="${L(lang, '/art/' + a.slug)}"><img src="/img/${a.id}.jpg" alt="${esc(tl(a, lang))}" loading="lazy"></a>`).join('')}<span class="hcap">${esc(tl(hero, lang))} · ${esc(al(hero, lang))}</span></div></div></section>
<section class="wrap sec"><div class="sh"><div><span class="eyebrow dk">${ko ? '무엇을 만들까요' : 'Make something'}</span><h2>${ko ? '바로 쓰는 네 가지' : 'Four ways to start'}</h2></div></div><div class="bento">${bento}</div></section>
${colStrip(lang)}
<section class="wrap sec"><div class="sh"><h2>${t.products}</h2><a href="${L(lang, '/shop')}">${t.nav.shop} →</a></div>${rail(PRODUCTS.filter((p) => !isOrig(p) && !['artist-calendars', 'puzzles'].includes(p.cat)))}</section>
<section class="wrap sec"><div class="sh"><h2>${ko ? '큰 글씨 퍼즐북 · 컬러링북' : 'Large-print puzzle & coloring books'}</h2><a href="${L(lang, '/shop')}#puzzles">${ko ? '어르신도 편하게' : 'Easy on the eyes'} →</a></div>${rail(PRODUCTS.filter((p) => p.cat === 'puzzles'))}</section>
<section class="wrap sec"><div class="sh"><h2>${ko ? '화가별 명화 달력 2027' : 'Artist calendars 2027'}</h2><a href="${L(lang, '/shop')}#calendars">${ko ? '15명 모두 보기' : 'All 15 artists'} →</a></div>${rail(PRODUCTS.filter((p) => p.cat === 'artist-calendars'))}</section>
<section class="wrap sec"><div class="edcta"><div><span class="eyebrow">${ko ? '아트트립 편집기' : 'Arttrip Editor'}</span><h2>${ko ? '사고 나서도 내 마음대로' : 'Make it yours after you buy'}</h2><p>${ko ? '내 사진, 글꼴 19종, 빈티지 종이, 12개월 달력 자동 만들기. 브라우저에서 바로 꾸미고 인쇄용 PDF로 받아요.' : 'Your photos, 19 fonts, vintage paper and one-click 12-month calendars. Design in the browser, download a print-ready PDF.'}</p><a class="pill lt" href="${L(lang, '/editor')}?new=1">${ko ? '무료로 열어 보기' : 'Try it free'}</a></div><img src="/p/art-paper-kit.jpg" alt="" loading="lazy"></div></section>
<section class="wrap sec"><div class="sh"><h2>${ko ? '아트트립 오리지널' : 'Arttrip Originals'}</h2><a href="${L(lang, '/originals')}">${ko ? '모두 보기' : 'See all'} →</a></div>${rail(PRODUCTS.filter(isOrig))}</section>
<section class="wrap sec"><div class="sh"><h2>${t.themes}</h2><a href="${L(lang, '/art')}">${t.allArt} (${total}) →</a></div>
<div class="themes">${counts.map((c) => `<a class="theme" href="${L(lang, '/art/theme/' + c.theme)}"><img src="/img/${covers[c.theme]}.jpg" alt="" loading="lazy"><b>${esc(THEMES[c.theme]?.[lang] || c.theme)}</b><span>${c.n} ${ko ? '점' : 'artworks'}</span></a>`).join('')}</div></section>`;
  return html(layout(lang, { title: `${t.site} — ${t.tagline}`, desc: t.heroSub, path: '/', body, img: `/img/${hero.id}.jpg` }));
}

async function gallery(lang, env, url, f) {
  const t = T[lang]; const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10));
  let where = '1=1', args = [], title = t.allArt, path = '/art', h1 = t.allArt, intro = '';
  if (f?.theme) { where = 'theme = ?'; args = [f.theme]; h1 = THEMES[f.theme][lang]; path = '/art/theme/' + f.theme; title = lang === 'ko' ? `${h1} 명화 모음 — 인쇄용 고해상도` : `${h1} — Public-Domain Masterpieces to Print`;
    intro = lang === 'ko' ? `${h1}을(를) 주제로 한 저작권 없는 명화 모음이에요. 작품을 눌러 색상 팔레트를 보고, 달력·카드·포스터로 만들어 보세요.` : `Public-domain ${h1.toLowerCase()} masterpieces. Open any artwork for its colour palette, details and printable products.`; }
  if (f?.artist) { where = 'artist_slug = ?'; args = [f.artist]; path = '/artist/' + f.artist; }
  const total = (await one(env, `SELECT COUNT(*) n FROM artworks WHERE ${where}`, ...args)).n;
  if (!total) return null;
  const rows = await all(env, `SELECT * FROM artworks WHERE ${where} ORDER BY CASE WHEN title_ko <> '' THEN 0 ELSE 1 END, rowid LIMIT ? OFFSET ?`, ...args, PER_PAGE, (page - 1) * PER_PAGE);
  if (!rows.length) return null;
  if (f?.artist) { h1 = al(rows[0], lang); title = lang === 'ko' ? `${h1} 작품 모음 — 고해상도 명화` : `${h1} — Artworks in High Resolution`;
    intro = lang === 'ko' ? `${h1}의 퍼블릭 도메인 작품 ${total}점이에요.` : `${total} public-domain works by ${h1}.`; }
  const pages = Math.ceil(total / PER_PAGE);
  const q = (n) => (n > 1 ? `?page=${n}` : '');
  const pager = pages > 1 ? `<nav class="pager">${page > 1 ? `<a href="${L(lang, path)}${q(page - 1)}">‹ ${t.prev}</a>` : ''}<span>${t.page} ${page} / ${pages}</span>${page < pages ? `<a href="${L(lang, path)}${q(page + 1)}">${t.next} ›</a>` : ''}</nav>` : '';
  const chips = Object.keys(THEMES).map((k) => `<a href="${L(lang, '/art/theme/' + k)}" aria-current="${f?.theme === k}">${esc(THEMES[k][lang])}</a>`).join('');
  const body = `<section class="wrap sec"><span class="lbl">${lang === 'ko' ? '컬렉션' : 'Collection'}</span><h1>${esc(h1)}</h1>${intro ? `<p class="sub">${esc(intro)}</p>` : ''}
<div class="chips">${chips}</div>${(() => { const cal = f?.artist && PRODUCTS.find((p) => p.artist_slug === f.artist); return cal ? `<a class="promo" href="${L(lang, '/shop/' + cal.slug)}"><img src="${cal.img}" alt="" loading="lazy"><span><b>${esc(cal[lang].name)}</b><em>${esc(cal[lang].short)} · $${cal.price}</em></span></a>` : ''; })()}<p class="small">${total} ${lang === 'ko' ? '점' : 'artworks'}</p><div class="masonry">${rows.map((a) => tile(a, lang)).join('')}</div>${pager}</section>`;
  return html(layout(lang, { title: page > 1 ? `${title} — ${t.page} ${page}` : title, desc: intro || title, path: path + q(page), body, img: `/img/${rows[0].id}.jpg` }));
}

const MEDIUM_KO = [[/oil on canvas/i, '캔버스에 유채'], [/oil on panel|oil on wood/i, '목판에 유채'], [/oil on board/i, '보드에 유채'], [/color woodblock print|colour woodblock print/i, '다색 목판화'],
  [/woodblock print/i, '목판화'], [/watercolor|watercolour/i, '수채'], [/tempera/i, '템페라'], [/pastel/i, '파스텔'], [/etching/i, '에칭'], [/engraving/i, '판화(인그레이빙)'],
  [/albumen print/i, '알부민 프린트'], [/gelatin silver/i, '젤라틴 실버 프린트'], [/silk/i, '비단'], [/cotton/i, '면직물'], [/linen/i, '리넨'], [/charcoal/i, '목탄'], [/graphite/i, '흑연'], [/ink/i, '먹·잉크']];
const batchim = (w) => { for (let i = w.length - 1; i >= 0; i--) { const c = w.charCodeAt(i); if (c >= 0xac00 && c <= 0xd7a3) return (c - 0xac00) % 28 !== 0; if (/[0-9]/.test(w[i])) return '013678'.includes(w[i]); } return true; };
const iyo = (w) => w + (batchim(w) ? '이에요' : '예요');
const ro = (w) => { const c = w.charCodeAt(w.length - 1); const rieul = c >= 0xac00 && c <= 0xd7a3 && (c - 0xac00) % 28 === 8; return w + (batchim(w) && !rieul ? '으로' : '로'); };
function describe(a, lang, pal) {
  const kind = (a.kind || '').toLowerCase();
  const cols = [...new Set(pal.map((h) => colorName(h, lang)))].slice(0, 4);
  if (lang === 'ko') {
    const k = T.ko.kindLabel(a.kind) || '작품';
    const med = (MEDIUM_KO.find(([rx]) => rx.test(a.medium || '')) || [])[1];
    return [`「${tl(a, 'ko')}」${batchim(tl(a, 'ko')) ? '은' : '는'} ${al(a, 'ko')}의 ${a.date ? `${ro(k)}, 제작 연도는 ${iyo(/\d$/.test(a.date) ? a.date + '년' : a.date)}` : iyo(k)}.${med ? ` 재료는 ${iyo(med)}.` : ''}`,
      `원본은 시카고 미술관이 소장하고 있으며, 저작권이 없는 퍼블릭 도메인(CC0) 이미지로 공개되어 있어요. 이 그림의 주요 색은 ${iyo(cols.join(', '))}.`];
  }
  return [`${a.title} is a ${kind || 'work'} by ${a.artist}${a.date ? `, dated ${a.date}` : ''}.${a.medium ? ` Medium: ${a.medium}.` : ''}`,
    `The original is in the collection of the Art Institute of Chicago, which has released this image into the public domain (CC0). Its main colours are ${cols.join(', ')}.`];
}

async function artwork(lang, env, slug) {
  const t = T[lang];
  const a = await one(env, 'SELECT * FROM artworks WHERE slug = ?', slug);
  if (!a) return null;
  const pal = JSON.parse(a.palette || '[]');
  const same = await all(env, 'SELECT * FROM artworks WHERE artist_slug = ? AND id <> ? LIMIT 8', a.artist_slug, a.id);
  const rel = await all(env, 'SELECT * FROM artworks WHERE theme = ? AND id <> ? AND artist_slug <> ? ORDER BY ((CAST(id AS INTEGER) * 2654435761) % 1000) LIMIT 8', a.theme, a.id, a.artist_slug);
  const title = tl(a, lang), artist = al(a, lang);
  const d = describe(a, lang, pal);
  const mk = ['calendar', 'card', 'poster', 'wallpaper'].map((k) => `<a class="mk" href="${L(lang, "/studio")}?tool=${{ calendar: 'wallcal', card: 'card', poster: 'poster', wallpaper: 'wallpaper' }[k]}&art=${a.id}">${t.make[k]}</a>`).join('');
  const body = `<section class="wrap sec art">
<nav class="crumb"><a href="${L(lang, '/art')}">${t.nav.art}</a> › <a href="${L(lang, '/art/theme/' + a.theme)}">${esc(THEMES[a.theme]?.[lang] || a.theme)}</a></nav>
<div class="agrid"><figure class="big" style="aspect-ratio:${a.w}/${a.h}"><img src="/img/${a.id}.jpg" alt="${esc(title)} — ${esc(artist)}" width="${a.w}" height="${a.h}"></figure>
<div class="meta"><span class="lbl">${esc(t.kindLabel(a.kind) || '')}${a.date ? ' · ' + esc(a.date) : ''}</span><h1>${esc(title)}</h1>
<p class="by"><a href="${L(lang, '/artist/' + a.artist_slug)}">${esc(artist)}</a></p>${lang === 'ko' && a.title_ko ? `<p class="small orig">${esc(a.title)}</p>` : ''}
${d.map((x) => `<p>${esc(x)}</p>`).join('')}
<h2 class="h3">${t.palette}</h2><div class="pal">${pal.map((h) => `<button type="button" data-copy="${h}" style="--c:${h}"><i></i><span>${h}</span></button>`).join('')}</div><p class="small">${t.paletteHint}</p>
<h2 class="h3">${t.useIt}</h2><p class="small">${t.useItSub}</p><div class="mks">${mk}</div>
<div class="dl"><b>${t.download}</b><p class="small">${t.downloadSub}</p><a class="pill" href="${L(lang, '/pricing')}">${t.subscribe}</a></div>
<table class="tbl"><tr><th>${t.artist}</th><td>${esc(artist)}</td></tr>${a.date ? `<tr><th>${t.date}</th><td>${esc(a.date)}</td></tr>` : ''}${a.medium ? `<tr><th>${t.medium}</th><td>${esc(lang === 'ko' ? ((MEDIUM_KO.find(([rx]) => rx.test(a.medium)) || [])[1] || a.medium) : a.medium)}</td></tr>` : ''}<tr><th>${t.source}</th><td>${t.sourceText}${a.credit ? `<br><span class="small">${esc(a.credit)}</span>` : ''}</td></tr></table></div></div>
${same.length ? `<div class="sh"><h2>${t.sameArtist}${lang === 'ko' ? '' : ' ' + esc(a.artist)}</h2></div><div class="masonry">${same.map((x) => tile(x, lang)).join('')}</div>` : ''}
${rel.length ? `<div class="sh"><h2>${t.related}</h2></div><div class="masonry">${rel.map((x) => tile(x, lang)).join('')}</div>` : ''}</section>`;
  const jsonld = { '@context': 'https://schema.org', '@type': 'VisualArtwork', name: a.title, alternateName: a.title_ko || undefined, creator: { '@type': 'Person', name: a.artist }, dateCreated: a.date || undefined, artMedium: a.medium || undefined, image: `/img/${a.id}.jpg`, license: 'https://creativecommons.org/publicdomain/zero/1.0/' };
  const ttl = lang === 'ko' ? `${title} — ${artist} | 고해상도 명화` : `${title} by ${artist} — High-Resolution Public-Domain Art`;
  return html(layout(lang, { title: ttl, desc: d.join(' ').slice(0, 155), path: '/art/' + a.slug, body, img: `/img/${a.id}.jpg`, jsonld }));
}

function productCard(p, lang) {
  const c = p[lang];
  return `<a class="pcard" href="${L(lang, '/shop/' + p.slug)}"><div class="pimg"><img src="${p.img}" alt="${esc(c.name)}" loading="lazy"></div><b>${esc(c.name)}</b><span>${esc(c.short)}</span><em>$${p.price}</em></a>`;
}
// ---------- studio, members, thanks ----------
function studio(lang, env) {
  const ko = lang === 'ko';
  const head = `<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Dancing+Script:wght@600&display=swap" rel="stylesheet"><link rel="stylesheet" href="/studio/studio.css">`;
  const body = `<div class="wrap edban"><a href="${L(lang, '/editor')}?new=1"><b>${ko ? '새로 나온 아트트립 에디터' : 'New: the Arttrip Editor'}</b><span>${ko ? '레이어, 내 사진, 글꼴 19종, 빈티지 효과, 달력 12개월 자동 만들기까지 — 아트페이퍼와 달력을 자유롭게 꾸며요' : 'Layers, your own photos, 19 fonts, vintage effects and 12-month calendars — design art papers and calendars freely'}</span><em>${ko ? '열기 →' : 'Open →'}</em></a></div><div id="app" data-lang="${lang}"><div class="wrap sec"><p class="small">${ko ? '불러오는 중…' : 'Loading…'}</p></div></div>
<script src="/studio/studio.js"></script><script src="/studio/boot.js"></script>`;
  return html(layout(lang, { title: ko ? '스튜디오 — 명화로 달력·카드·포스터 만들기 | 아트트립 스튜디오' : 'Studio — Make Calendars, Cards and Posters from Masterpieces | Arttrip Studio',
    desc: ko ? '명화를 골라 달력, 카드, 포스터, 스티커, 배경화면을 만들고 인쇄용 파일로 내려받으세요. 회원은 작업을 저장할 수 있어요.' : 'Pick a masterpiece and make a calendar, card, poster, sticker sheet or wallpaper. Download a print-ready file. Members can save their work.',
    path: '/studio', body, head }));
}
async function account(lang, env, req) {
  const ko = lang === 'ko', t = T[lang];
  if (!membersReady(env)) return html(layout(lang, { title: `${t.nav.myAccount} — ${t.site}`, desc: '', path: '/account', noindex: true,
    body: `<section class="wrap sec narrow center"><span class="lbl">${t.nav.account}</span><h1>${ko ? '회원 기능을 준비하고 있어요' : 'Member accounts are on the way'}</h1><p class="sub">${ko ? '지금은 로그인 없이 모든 상품을 구매할 수 있어요. 곧 구글 계정으로 가입해 스튜디오 작업을 저장할 수 있게 돼요.' : 'You can buy everything without an account today. Soon you will be able to sign in with Google and save your Studio work.'}</p><div class="row" style="justify-content:center"><a class="pill" href="${L(lang, '/shop')}">${t.nav.shop}</a><a class="pill ghost" href="${L(lang, '/studio')}">${t.nav.studio}</a></div></section>` }));
  const u = await currentUser(req, env);
  const gsi = `<script src="https://accounts.google.com/gsi/client" async></script>`;
  let body;
  if (!u) {
    body = `<section class="wrap sec narrow center"><span class="lbl">${t.nav.account}</span><h1>${ko ? '구글 계정으로 시작하기' : 'Sign in with Google'}</h1>
<p class="sub">${ko ? '가입하면 스튜디오 작업을 저장하고 이어서 편집할 수 있어요. 구독 회원은 워터마크 없는 고해상도 파일과 고급 편집 기능을 써요.' : 'Save your Studio work and come back to it. Subscribers get watermark-free print files and the advanced editor.'}</p>
<div id="g_id_onload" data-client_id="${esc(env.GOOGLE_CLIENT_ID)}" data-callback="atGoogle" data-auto_prompt="false"></div>
<div class="g_id_signin" data-type="standard" data-size="large" data-shape="pill" data-text="continue_with" data-locale="${lang}" style="display:flex;justify-content:center"></div>
<p class="small" style="margin-top:22px">${ko ? '구매는 회원가입 없이도 할 수 있어요.' : 'You can also buy without an account.'}</p></section>
<script>function atGoogle(r){fetch('/api/auth/google',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({credential:r.credential})}).then(function(x){if(x.ok)location.reload();else alert('${ko ? '로그인에 실패했어요. 다시 시도해 주세요.' : 'Sign-in failed. Please try again.'}')})}</script>`;
  } else {
    const ds = (await env.UDB.prepare('SELECT id, tool, title, updated FROM designs WHERE user_id = (SELECT id FROM users WHERE email = ?) ORDER BY updated DESC LIMIT 100').bind(u.email).all()).results;
    const member = u.plan === 'member';
    body = `<section class="wrap sec"><span class="lbl">${t.nav.myAccount}</span><h1>${esc(u.name || u.email)}</h1><p class="small">${esc(u.email)} · ${member ? (ko ? '구독 회원' : 'Subscriber') : (ko ? '무료 회원' : 'Free member')}</p>
${member ? '' : `<div class="dl"><b>${ko ? '구독하면 더 많이 쓸 수 있어요' : 'Get more with a subscription'}</b><p>${ko ? '워터마크 없는 고해상도 파일, 저장 500개, 고급 편집 기능.' : 'Watermark-free print files, 500 saved designs and the advanced editor.'}</p><a class="pill" href="${L(lang, '/pricing')}">${t.nav.pricing}</a></div>`}
<div class="sh"><h2>${ko ? '내 작업' : 'My designs'}</h2><a href="${L(lang, '/studio')}">${ko ? '새로 만들기' : 'New design'} →</a></div>
${ds.length ? `<ul class="iltopics">${ds.map((d) => `<li><a href="${L(lang, '/studio')}#/studio/${esc(d.tool)}?d=${d.id}">${esc(d.title || d.tool)}</a><em>${new Date(d.updated).toISOString().slice(0, 10)}</em></li>`).join('')}</ul>` : `<p class="sub">${ko ? '아직 저장한 작업이 없어요. 스튜디오에서 만들고 [저장]을 누르세요.' : 'No saved designs yet. Make something in the Studio and press Save.'}</p>`}
<p style="margin-top:30px"><button class="pill ghost" onclick="fetch('/api/logout',{method:'POST'}).then(function(){location.reload()})">${ko ? '로그아웃' : 'Sign out'}</button></p></section>`;
  }
  return html(layout(lang, { title: `${t.nav.myAccount} — ${t.site}`, desc: '', path: '/account', body, head: gsi, noindex: true }));
}
function thanks(lang, url) {
  const ko = lang === 'ko', t = T[lang], via = url.searchParams.get('via');
  const p = PRODUCTS.find((x) => x.slug === url.searchParams.get('p'));
  const name = p ? p[lang].name : '';
  const msg = via === 'kr'
    ? (ko ? '결제가 확인되면 결제할 때 남긴 연락처(문자 또는 이메일)로 24시간 안에 다운로드 링크를 보내 드려요.' : 'Once your payment is confirmed we will send the download link to the contact you gave within 24 hours.')
    : (ko ? '결제 확인 메일에 다운로드 링크가 들어 있어요. 메일이 안 보이면 스팸함도 확인해 주세요.' : 'Your download link is in the receipt email from our payment partner. Please check your spam folder if you cannot see it.');
  const body = `<section class="wrap sec narrow center"><span class="lbl">${ko ? '결제 완료' : 'Thank you'}</span><h1>${ko ? '구매해 주셔서 고마워요' : 'Thank you for your order'}</h1>${name ? `<p class="by">${esc(name)}</p>` : ''}<p class="sub">${msg}</p>
<div class="dl" style="text-align:left;margin:22px 0"><b>${ko ? '편집기로 꾸미기' : 'Edit it in the Arttrip Editor'}</b><p>${ko ? '영수증에 있는 라이선스 키(ARTTRIP-로 시작)를 편집기의 [다운로드] 창에 한 번 넣으면, 워터마크 없는 300dpi 파일로 받을 수 있어요. 그림을 바꾸고 내 사진과 글도 넣을 수 있어요.' : 'Enter the license key from your receipt (it starts with ARTTRIP-) once in the editor’s Download window to get watermark-free 300 dpi files. Swap paintings and add your own photos and words.'}</p><a class="pill" href="${L(lang, '/editor')}${p && p.editor ? '?tpl=' + p.editor + '&new=1' : p && p.artist_slug ? '?cal=' + p.artist_slug + '&new=1' : ''}">${ko ? '편집기 열기' : 'Open the editor'}</a></div>
<p class="small">${ko ? '문제가 있으면 hello@arttripstudio.com 으로 연락 주세요.' : 'Any problem? Write to hello@arttripstudio.com.'}</p><div class="row" style="justify-content:center;margin-top:20px"><a class="pill" href="${L(lang, '/studio')}">${t.nav.studio}</a><a class="pill ghost" href="${L(lang, '/shop')}">${t.nav.shop}</a></div></section>`;
  return html(layout(lang, { title: `${ko ? '결제 완료' : 'Thank you'} — ${t.site}`, desc: '', path: '/thanks', body, noindex: true }));
}




// ---------- Scripture search: keyword match first, then AI picks topics. The AI never writes verse text. ----------
const AI_MODELS = ['@cf/meta/llama-3.3-70b-instruct-fp8-fast', '@cf/meta/llama-4-scout-17b-16e-instruct', '@cf/google/gemma-3-12b-it', '@cf/qwen/qwen3-30b-a3b-fp8', '@cf/deepseek-ai/deepseek-v4-flash-0731', '@cf/moonshotai/kimi-k2.5'];
let AI_MODEL = null;
async function verses(url, env) {
  const J = (o) => new Response(JSON.stringify(o), { headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'public, max-age=300' } });
  const pub = (t) => ({ id: t.id, ko: t.ko, en: t.en });
  if (url.searchParams.get('list')) return J({ topics: VERSE_TOPICS.map(pub) });
  const pack = (ids) => { const seen = new Set(), out = []; for (const id of ids) { const t = VERSE_TOPICS.find((x) => x.id === id); if (!t) continue; for (const v of t.v) if (!seen.has(v.k)) { seen.add(v.k); out.push(v); } } return out.slice(0, 14); };
  const tp = url.searchParams.get('topic');
  if (tp) return J({ topics: VERSE_TOPICS.filter((t) => t.id === tp).map(pub), verses: pack([tp]) });
  const q = (url.searchParams.get('q') || '').trim().slice(0, 200), ql = q.toLowerCase();
  if (!q) return J({ topics: [], verses: [] });
  const score = VERSE_TOPICS.map((t) => [t.id, t.kw.reduce((n, k) => n + (ql.includes(k.toLowerCase()) ? 2 : 0), 0) + (ql.includes(t.ko) || ql.includes(t.en.toLowerCase()) ? 3 : 0)]).filter((x) => x[1] > 0).sort((a, b) => b[1] - a[1]);
  const short = !/\s/.test(q) && q.length <= 12;
  let ids = short ? score.slice(0, 3).map((x) => x[0]) : [], via = 'keywords';
  if (!ids.length && env.AI) {
    try {
      const list = VERSE_TOPICS.map((t) => `${t.id}: ${t.en} / ${t.ko}`).join('\n');
      const msgs = [
        { role: 'system', content: 'You map a request for a Bible verse to topic ids. Think about what the person needs (for example, someone whose friend lost a parent needs grief and comfort). Reply with only a JSON array of 1 to 3 topic ids from this list, most relevant first. No other text.\n' + list },
        { role: 'user', content: q } ];
      let r = null, lastErr = '';
      for (const model of (AI_MODEL ? [AI_MODEL] : AI_MODELS)) {
        try { r = await env.AI.run(model, { max_tokens: 80, messages: msgs }); AI_MODEL = model; break; } catch (e) { lastErr = String(e && e.message || e); if (AI_MODEL) { AI_MODEL = null; } }
      }
      if (!r) throw new Error(lastErr || 'no model');
      const txt = typeof r === 'string' ? r : (r.response ?? r.choices?.[0]?.message?.content ?? r.result?.response ?? '');
      const m = String(typeof txt === 'string' ? txt : JSON.stringify(txt)).match(/\[[^\]]*\]/);
      if (m) ids = JSON.parse(m[0]).filter((id) => VERSE_TOPICS.some((t) => t.id === id)).slice(0, 3);
      via = 'ai:' + AI_MODEL;
    } catch (e) { ids = []; via = 'ai-error: ' + String(e && e.message || e).slice(0, 160); }
  } else if (!ids.length) via = env.AI ? via : 'no-ai-binding';
  if (!ids.length) { ids = score.slice(0, 3).map((x) => x[0]); if (String(via).startsWith('ai:')) via = 'ai-empty ' + via; }
  if (!ids.length) {
    const hits = []; for (const t of VERSE_TOPICS) for (const v of t.v) if ((v.tk + ' ' + v.te).toLowerCase().includes(ql) && !hits.some((h) => h.k === v.k)) hits.push(v);
    return J({ topics: [], verses: hits.slice(0, 14), via: 'text' });
  }
  return J({ topics: VERSE_TOPICS.filter((t) => ids.includes(t.id)).map(pub), verses: pack(ids), via });
}

// ---------- Quotes: AI only maps a request to topic ids; quotes come from /quotes.json ----------
async function quotesApi(url, env) {
  const J = (o) => new Response(JSON.stringify(o), { headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'public, max-age=300' } });
  const q = (url.searchParams.get('q') || '').trim().slice(0, 200), ql = q.toLowerCase();
  if (!q) return J({ topics: [] });
  const score = QUOTE_TOPICS.map((t) => [t.id, t.kw.reduce((n, k) => n + (ql.includes(k) ? 2 : 0), 0) + (ql.includes(t.ko) || ql.includes(t.en.toLowerCase()) ? 3 : 0)]).filter((x) => x[1] > 0).sort((a, b) => b[1] - a[1]);
  let ids = [], via = 'keywords';
  if (env.AI) {
    try {
      const list = QUOTE_TOPICS.map((t) => `${t.id}: ${t.en} / ${t.ko}`).join('\n');
      const msgs = [
        { role: 'system', content: 'You map a request for a famous quote to topic ids. Think about the occasion and what the person wants to say (for example, a graduation card needs learning, hope and success; comforting someone after a loss needs death first, then peace and hope). Reply with only a JSON array of 1 to 3 topic ids from this list, most relevant first. No other text.\n' + list },
        { role: 'user', content: q } ];
      let r = null, lastErr = '';
      for (const model of (AI_MODEL ? [AI_MODEL] : AI_MODELS)) {
        try { r = await env.AI.run(model, { max_tokens: 60, messages: msgs }); AI_MODEL = model; break; } catch (e) { lastErr = String(e && e.message || e); if (AI_MODEL) AI_MODEL = null; }
      }
      if (!r) throw new Error(lastErr || 'no model');
      const txt = typeof r === 'string' ? r : (r.response ?? r.choices?.[0]?.message?.content ?? r.result?.response ?? '');
      const m = String(typeof txt === 'string' ? txt : JSON.stringify(txt)).match(/\[[^\]]*\]/);
      if (m) ids = JSON.parse(m[0]).filter((id) => QUOTE_TOPICS.some((t) => t.id === id)).slice(0, 3);
      via = 'ai:' + AI_MODEL;
    } catch (e) { ids = []; via = 'ai-error: ' + String(e && e.message || e).slice(0, 160); }
  } else via = 'no-ai-binding';
  if (!ids.length) ids = score.slice(0, 3).map((x) => x[0]);
  return J({ topics: ids, via });
}

// ---------- Collections: the big image categories ----------
const COLS = [
  ['art', { en: 'Masterpieces', ko: '명화' }, { en: 'Oil paintings, woodblock prints and drawings from the great museums.', ko: '세계 미술관의 유화, 판화, 드로잉' }, '/img/14598.jpg', '/art', true],
  ['illustration', { en: 'Arttrip Illustration', ko: '아트트립 일러스트' }, { en: 'Our own hand-drawn characters, cozy scenes and seasons.', ko: '우리가 직접 그린 인물, 포근한 일상, 계절' }, '/p/cafe-girl-clipart.jpg', '/illustrations', true],
  ['landscape', { en: 'Landscape Photography', ko: '풍경 사진' }, { en: 'Mountains, lakes, mist, dunes, coasts and night skies by award-winning photographers.', ko: '산, 호수, 안개, 사막, 바다, 밤하늘. 수상작 수준의 풍경 사진' }, '/ph/w956090e0.jpg', '/collections/landscape', true],
  ['architecture', { en: 'Architecture & Light', ko: '건축과 빛' }, { en: 'Modern buildings, spiral stairs, glass and light.', ko: '현대 건축, 나선 계단, 유리와 빛' }, '/ph/we533e122.jpg', '/collections/architecture', true],
  ['portraits', { en: 'Vintage Portraits', ko: '빈티지 인물' }, { en: 'Portrait photographs and faces from the 1800s and early 1900s.', ko: '1800년대부터 1900년대 초의 인물 사진' }, '/img/29230.jpg', null, false],
  ['natural-history', { en: 'Vintage Natural History', ko: '빈티지 도감' }, { en: 'Botanical plates, birds, insects, old maps and science prints.', ko: '식물도감, 새, 곤충, 옛 지도, 과학 그림' }, '/img/127282.jpg', null, false],
  ['lettering', { en: 'Lettering', ko: '글씨' }, { en: 'Scripture, sutras, Hangul, Latin and famous quotes set in beautiful type.', ko: '성경 말씀, 불경, 한글, 라틴어, 명언을 아름다운 글씨로' }, '/p/cat-lettering.jpg', '/originals#lettering', true],
  ['patterns', { en: 'Patterns & Textures', ko: '패턴·질감' }, { en: 'Seamless repeats and paper textures for backgrounds and goods.', ko: '배경과 굿즈에 쓰는 반복 무늬와 종이 질감' }, '/p/patterns-originals.jpg', '/originals#patterns', true],
];
function colTile(c, lang, big) {
  const [k, n, d, img, href, live] = c, ko = lang === 'ko';
  const tag = live ? '' : `<em class="soon">${ko ? '곧 공개' : 'Coming soon'}</em>`;
  const inner = `<img src="${img}" alt="" loading="lazy"><span><b>${esc(n[lang])}</b>${big ? `<i>${esc(d[lang])}</i>` : ''}</span>${tag}`;
  return href ? `<a class="ct" href="${L(lang, href)}">${inner}</a>` : `<div class="ct off">${inner}</div>`;
}
function colStrip(lang) {
  const ko = lang === 'ko';
  return `<section class="wrap sec"><div class="sh"><div><span class="eyebrow dk">${ko ? '8가지 컬렉션' : '8 collections'}</span><h2>${ko ? '무엇을 찾으세요?' : 'What are you looking for?'}</h2></div><a href="${L(lang, '/collections')}">${ko ? '모든 컬렉션' : 'All collections'} →</a></div><div class="cgrid">${COLS.map((c) => colTile(c, lang, false)).join('')}</div></section>`;
}
function collections(lang) {
  const ko = lang === 'ko', t = T[lang];
  const title = ko ? '컬렉션 — 명화, 사진, 일러스트, 글씨 | 아트트립 스튜디오' : 'Collections — Art, Photography, Illustration & Lettering | Arttrip Studio';
  const desc = ko ? '명화, 아트트립 일러스트, 풍경 사진, 건축물, 빈티지 인물, 빈티지 도감, 글씨, 패턴까지 8가지 컬렉션.' : 'Eight collections: masterpieces, Arttrip illustration, landscape photography, architecture, vintage portraits, natural history, lettering and patterns.';
  const body = `<section class="wrap sec"><span class="lbl">${t.nav.col}</span><h1>${ko ? '8가지 컬렉션' : 'Eight collections'}</h1>
<p class="sub">${ko ? '공개된 명화와 사진을 정성껏 다듬은 것, 그리고 우리가 직접 만든 일러스트와 글씨와 패턴. 모두 인쇄와 굿즈에 바로 쓸 수 있어요.' : 'Carefully restored public-domain art and photography, plus illustration, lettering and patterns we make ourselves. All ready to print and use.'}</p>
<div class="cgrid wide">${COLS.map((c) => colTile(c, lang, true)).join('')}</div>
<div class="edban" style="margin-top:44px"><a href="${L(lang, '/editor')}?new=1"><b>${ko ? '내 사진으로 만들기' : 'Make it with your own photos'}</b><span>${ko ? '가족사진, 여행 사진을 올려 달력, 청첩장, 포스터로 꾸며 보세요. 컬렉션의 그림과 글씨를 함께 쓸 수 있어요.' : 'Upload family or travel photos and turn them into calendars, invitations and posters, mixed with anything from our collections.'}</span><em>${ko ? '편집기 열기 →' : 'Open the editor →'}</em></a></div></section>`;
  return html(layout(lang, { title, desc, path: '/collections', body, img: '/img/14598.jpg', jsonld: { '@context': 'https://schema.org', '@type': 'CollectionPage', name: title, description: desc } }));
}

// ---------- Studio-only line-art generator (used to make our own coloring pages; token-protected, temporary) ----------
async function lineart(url, env) {
  const k = url.searchParams.get('k') || '';
  const h = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(k)))).map((b) => b.toString(16).padStart(2, '0')).join('');
  if (h !== 'fe6c93b862feb1ab753ab4692e7ff27969792bf99e903c101eb778845b7c924f' || Date.now() > Date.UTC(2027, 0, 31) || !env.AI) return new Response('no', { status: 403 });
  const subject = (url.searchParams.get('q') || '').slice(0, 300), seed = +(url.searchParams.get('seed') || 1);
  const prompt = `Coloring book page: ${subject}. Absolutely no text, no letters, no numbers, no captions. Clean black outlines on pure white background, bold uniform line weight, large closed shapes to color, no shading, no gray, no hatching, no text, no border, whole subject in frame, simple fun cartoon style, high contrast line art.`;
  const model = url.searchParams.get('m') || '@cf/black-forest-labs/flux-1-schnell';
  let r;
  try { r = await env.AI.run(model, model.includes('schnell') ? { prompt, steps: 8 } : { prompt: prompt + ` (variation ${seed})`, width: 1024, height: 1024, seed }); }
  catch (e) { return new Response(String(e && e.message || e), { status: 500 }); }
  if (r instanceof ReadableStream) return new Response(r, { headers: { 'content-type': 'image/png', 'cache-control': 'no-store' } });
  const b64 = r.image || r; const bin = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
  return new Response(bin, { headers: { 'content-type': 'image/jpeg', 'cache-control': 'no-store' } });
}

// ---------- Photography: real photos from Wikimedia Commons (CC0 / public domain / CC BY / CC BY-SA), served through our own cache ----------
const PH = Object.fromEntries(PHOTOS.map((x) => [x.id, x]));
const LIC_URL = (l) => /^CC0/.test(l) ? 'https://creativecommons.org/publicdomain/zero/1.0/' : /^Public domain/i.test(l) ? null
  : 'https://creativecommons.org/licenses/' + (l.match(/BY-SA/) ? 'by-sa' : 'by') + '/' + ((l.match(/(\d\.\d)/) || [])[1] || '4.0') + '/';
async function photoProxy(path, ctx) {
  const m = path.match(/^\/ph\/(w[0-9a-f]{8})(-hi)?\.jpg$/); const ph = m && PH[m[1]];
  if (!ph) return new Response('Not found', { status: 404 });
  const cache = caches.default, key = new Request('https://arttripstudio.com' + path);
  const hit = await cache.match(key); if (hit) return hit;
  const file = ph.p.split('/').pop();
  const sizes = m[2] ? [3840, 2560, 1920, 1280].filter((w) => w < ph.w) : [1280, 960];
  let r = null;
  for (const w of sizes.length ? sizes : [1280]) {
    r = await fetch(`https://upload.wikimedia.org/wikipedia/commons/thumb/${ph.p}/${w}px-${file}`, { headers: { 'user-agent': 'ArttripStudio/1.0 (https://arttripstudio.com; hello@arttripstudio.com)' }, cf: { cacheTtl: 2592000, cacheEverything: true } });
    if (r.ok) break;
  }
  if (!r || !r.ok) { r = await fetch(`https://upload.wikimedia.org/wikipedia/commons/${ph.p}`, { headers: { 'user-agent': 'ArttripStudio/1.0 (https://arttripstudio.com)' } }); if (!r.ok) return new Response('Upstream error', { status: 502 }); }
  const res = new Response(r.body, { headers: { 'content-type': 'image/jpeg', 'cache-control': 'public, max-age=2592000, immutable', 'access-control-allow-origin': '*' } });
  ctx.waitUntil(cache.put(key, res.clone()));
  return res;
}
function photoGallery(lang, cat) {
  const ko = lang === 'ko', t = T[lang], list = PHOTOS.filter((x) => x.c === cat);
  const name = cat === 'architecture' ? (ko ? '건축과 빛' : 'Architecture & Light') : (ko ? '풍경 사진' : 'Landscape Photography');
  const sub = cat === 'architecture'
    ? (ko ? '빛이 머무는 현대 건축: 나선 계단, 유리 지붕, 콘크리트와 그림자. 세계 사진가들이 자유 이용을 허락한 사진만 골랐어요.' : 'Modern architecture where light lingers: spiral stairs, glass roofs, concrete and shadow, chosen only from photographers who share their work under free licences.')
    : (ko ? '알프스와 로키의 호수, 안개 낀 숲, 사막의 모래 언덕, 오로라와 은하수. 위키미디어 공용의 우수 사진 가운데 골랐어요.' : 'Alpine and Rocky Mountain lakes, misty forests, desert dunes, auroras and the Milky Way, chosen from Wikimedia Commons featured pictures.');
  const title = `${name} — ${ko ? '인쇄용 고화질 사진' : 'High-resolution photos to print'} | ${ko ? '아트트립 스튜디오' : 'Arttrip Studio'}`;
  const tiles = list.map((x) => `<figure class="phc" data-id="${x.id}" data-t="${esc(x.t)}" data-a="${esc(x.a)}" data-l="${esc(x.l)}" data-lu="${esc(LIC_URL(x.l) || '')}" data-w="${x.w}" data-h="${x.h}" data-src="https://commons.wikimedia.org/wiki/File:${esc(x.p.split('/').pop())}"><img src="/ph/${x.id}.jpg" alt="${esc(x.t)}" loading="lazy" width="${x.w}" height="${x.h}"><figcaption>${esc(x.t)}<span>${esc(x.a)}</span></figcaption></figure>`).join('');
  const other = cat === 'architecture' ? 'landscape' : 'architecture';
  const body = `<section class="wrap sec"><a class="lbl" href="${L(lang, '/collections')}">${t.nav.col}</a><h1>${name}</h1><p class="sub">${sub}</p>
<div class="chips"><a aria-current="true" href="${L(lang, '/collections/' + cat)}">${name} · ${list.length}</a><a href="${L(lang, '/collections/' + other)}">${other === 'architecture' ? (ko ? '건축과 빛' : 'Architecture & Light') : (ko ? '풍경 사진' : 'Landscape Photography')}</a><a href="${L(lang, '/art')}">${ko ? '명화' : 'Masterpieces'}</a></div>
<div class="phgrid">${tiles}</div>
<p class="small" style="margin-top:28px">${ko ? '사진마다 찍은 사람과 이용 허락(라이선스)을 적었어요. CC BY·CC BY-SA 사진은 인쇄하거나 공유할 때 사진가 이름과 라이선스를 함께 적어 주세요. 우리 편집기는 이 표기를 자동으로 넣어요.' : 'Every photo lists its photographer and licence. For CC BY and CC BY-SA photos, credit the photographer and licence when you print or share. Our editor adds this credit for you.'}</p></section>
<div class="phbox" id="phbox" hidden><div class="phin"><button class="phx" aria-label="close">×</button><img id="phimg" alt=""><div class="phmeta"><b id="pht"></b><span id="pha"></span><div class="phbtn"><a id="phed" class="btn">${ko ? '편집기에서 쓰기' : 'Use in the editor'}</a><a id="phsrc" target="_blank" rel="noopener">${ko ? '원본 · 라이선스' : 'Source · licence'}</a></div></div></div></div>
<script>(function(){var b=document.getElementById('phbox');document.querySelectorAll('.phc').forEach(function(f){f.onclick=function(){var d=f.dataset;document.getElementById('phimg').src='/ph/'+d.id+'.jpg';document.getElementById('pht').textContent=d.t;document.getElementById('pha').textContent='${ko ? '사진' : 'Photo'}: '+d.a+' · '+d.l;document.getElementById('phed').href='${L(lang, '/editor')}?new=1&photo='+d.id;document.getElementById('phsrc').href=d.src;b.hidden=false;};});b.onclick=function(e){if(e.target===b||e.target.classList.contains('phx'))b.hidden=true;};document.addEventListener('keydown',function(e){if(e.key==='Escape')b.hidden=true;});})();</script>`;
  return html(layout(lang, { title, desc: sub, path: '/collections/' + cat, body, img: '/ph/' + list[0].id + '.jpg', jsonld: { '@context': 'https://schema.org', '@type': 'CollectionPage', name, description: sub } }));
}

// ---------- Arttrip Originals: our own illustrations, patterns and lettering ----------
const isOrig = (p) => p.cat === 'illustrations' || p.cat === 'originals';
const ORIG_LINES = [
  ['illustrations', { en: 'Illustration sets', ko: '일러스트 세트' }, { en: 'Characters, cozy scenes and seasons — clipart, stickers and calendars.', ko: '인물, 포근한 일상, 계절 장면 — 클립아트, 스티커, 달력' }],
  ['patterns', { en: 'Patterns', ko: '패턴' }, { en: 'Seamless repeat tiles for wrapping paper, fabric, tumblers and backgrounds.', ko: '포장지, 원단, 텀블러, 배경에 쓰는 이어지는 반복 무늬' }],
  ['lettering', { en: 'Lettering', ko: '글씨 디자인' }, { en: 'Quotes and celebration words set in beautiful type — for T-shirts, posters and cards.', ko: '명언과 축하 문구를 예쁜 글씨로 — 티셔츠, 포스터, 카드용' }],
];
function originals(lang) {
  const ko = lang === 'ko', t = T[lang];
  const line = (k) => PRODUCTS.filter((p) => isOrig(p) && (p.line || 'illustrations') === k);
  const jump = ORIG_LINES.map(([k, n]) => `<a href="#${k}">${esc(n[lang])}</a>`).join('') + `<a href="${L(lang, '/illustrations')}">${ko ? '인물 일러스트 주제' : 'Character themes'}</a>`;
  const secs = ORIG_LINES.map(([k, n, d]) => { const list = line(k);
    return `<div class="sh" id="${k}" style="margin-top:38px"><h2>${esc(n[lang])}</h2><span class="small">${list.length ? list.length : ''}</span></div><p class="small">${esc(d[lang])}</p>` +
      (list.length ? `<div class="pgrid">${list.map((p) => productCard(p, lang)).join('')}</div>` : `<p class="sub">${ko ? '첫 세트를 만들고 있어요. 곧 공개돼요.' : 'The first sets are in the studio now — coming soon.'}</p>`); }).join('');
  const tiles = Object.entries(IL_CATS).filter(([k]) => IL_COVER[k]).map(([k, c]) => `<a class="ilcat" href="${L(lang, '/illustrations/' + k)}"><div class="ilimg">${IL_COVER[k] ? `<img src="${IL_COVER[k]}" alt="" loading="lazy">` : `<i>${esc(c[lang].slice(0, 1))}</i>`}</div><b>${esc(c[lang])}</b></a>`).join('');
  const title = ko ? '아트트립 오리지널 — 자체 일러스트·패턴·글씨 디자인 | 아트트립 스튜디오' : 'Arttrip Originals — Our Own Illustrations, Patterns & Lettering | Arttrip Studio';
  const desc = ko ? '아트트립 스튜디오가 직접 만든 일러스트, 반복 패턴, 글씨 디자인. 명화와 섞어 편집기에서 바로 꾸밀 수 있어요.' : 'Illustrations, seamless patterns and lettering made in-house by Arttrip Studio. Mix them with masterpieces in the online editor.';
  const body = `<section class="wrap sec"><span class="lbl">${t.nav.illus}</span><h1>${ko ? '아트트립 오리지널' : 'Arttrip Originals'}</h1>
<p class="sub">${ko ? '명화 컬렉션 옆에, 우리가 직접 그리고 다듬은 디자인을 모았어요. 일러스트, 반복 패턴, 글씨 디자인을 명화와 섞어 쓰면 어디에도 없는 작품이 돼요.' : 'Alongside the masterpiece collection, these are designs we draw and finish ourselves. Mix illustrations, patterns and lettering with old masters to make something no one else has.'}</p>
<div class="chips wrapc">${jump}</div>${secs}
<div class="sh" style="margin-top:38px"><h2>${ko ? '인물 일러스트 주제' : 'Character illustration themes'}</h2><a href="${L(lang, '/illustrations')}">${ko ? '10가지 주제 모두' : 'All 10 themes'} →</a></div><div class="ilgrid">${tiles}</div>
<div class="edban" style="margin-top:40px"><a href="${L(lang, '/editor')}?new=1"><b>${ko ? '명화와 오리지널을 한 장에' : 'Masterpieces and Originals on one page'}</b><span>${ko ? '편집기에서 명화 배경 위에 일러스트와 글씨를 얹어 보세요.' : 'Layer our illustrations and lettering over a masterpiece in the editor.'}</span><em>${ko ? '편집기 열기 →' : 'Open the editor →'}</em></a></div></section>`;
  return html(layout(lang, { title, desc, path: '/originals', body, img: '/p/cafe-girl-clipart.jpg', jsonld: { '@context': 'https://schema.org', '@type': 'CollectionPage', name: title, description: desc } }));
}

// ---------- original illustrations ----------
const IL_COVER = { everyday: '/il/everyday.png', seasons: '/il/seasons.jpg' };
function illus(lang, cat) {
  const ko = lang === 'ko'; const t = T[lang];
  const sets = (k) => PRODUCTS.filter((p) => p.il === k);
  const chips = `<a href="${L(lang, '/illustrations')}" aria-current="${!cat}">${ko ? '전체' : 'All'}</a>` + Object.keys(IL_CATS).map((k) => `<a href="${L(lang, '/illustrations/' + k)}" aria-current="${cat === k}">${esc(IL_CATS[k][lang])}</a>`).join('');
  let body, title, desc, path;
  if (!cat) {
    title = ko ? '손그림 인물 일러스트 — 클립아트·스티커 | 아트트립 스튜디오' : 'Hand-Drawn Character Illustrations — Clipart & Stickers | Arttrip Studio';
    desc = ko ? '마카·색연필·디지털 손그림 스타일의 인물 클립아트와 스티커. 일상, 가족, 결혼, 직업, 계절 등 10가지 주제.' : 'Hand-drawn character clipart and stickers in marker, coloured pencil and digital styles. Everyday life, family, wedding, jobs, seasons and more.';
    path = '/illustrations';
    const tiles = Object.entries(IL_CATS).map(([k, c]) => { const n = sets(k).length; const cover = IL_COVER[k];
      return `<a class="ilcat" href="${L(lang, '/illustrations/' + k)}"><div class="ilimg">${cover ? `<img src="${cover}" alt="" loading="lazy">` : `<i>${esc(c[lang].slice(0, 1))}</i>`}</div><b>${esc(c[lang])}</b><span>${n ? (ko ? `상품 ${n}개` : `${n} ${n > 1 ? 'sets' : 'set'}`) : (ko ? '준비 중' : 'Coming soon')} · ${ko ? `주제 ${c.topics.length}가지` : `${c.topics.length} topics`}</span></a>`; }).join('');
    body = `<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/originals')}">${t.nav.illus}</a></nav><h1>${ko ? '손그림 인물 일러스트' : 'Hand-drawn character illustrations'}</h1>
<p class="sub">${ko ? '한 인물을 여러 동작으로 그린 클립아트와 스티커 세트예요. 카드, 플래너, 블로그, 작은 가게 상품에 쓰세요.' : 'One character, many poses — clipart and sticker sets for cards, planners, blogs and small-shop products.'}</p>
<p class="small">${esc(IL_STYLES[lang])}</p><div class="chips wrapc">${chips}</div><div class="ilgrid">${tiles}</div></section>`;
  } else {
    const c = IL_CATS[cat]; const list = sets(cat);
    title = ko ? `${c.ko} 인물 일러스트 — 클립아트·스티커 | 아트트립 스튜디오` : `${c.en} Illustrations — Character Clipart & Stickers | Arttrip Studio`;
    desc = ko ? `${c.ko} 주제의 손그림 인물 클립아트와 스티커: ${c.topics.map((x) => x[1]).join(', ')}.` : `Hand-drawn ${c.en.toLowerCase()} character clipart and stickers: ${c.topics.map((x) => x[0].toLowerCase()).join(', ')}.`;
    path = '/illustrations/' + cat;
    const topics = c.topics.map((x, i) => { const has = list.some((p) => p.topic === i); return `<li${has ? ' class="on"' : ''}>${esc(ko ? x[1] : x[0])}<em>${has ? (ko ? '판매 중' : 'Available') : (ko ? '준비 중' : 'Coming soon')}</em></li>`; }).join('');
    body = `<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/originals')}">${t.nav.illus}</a> › <a href="${L(lang, '/illustrations')}">${ko ? '인물 일러스트' : 'Characters'}</a></nav><h1>${esc(c[lang])}</h1>
<div class="chips wrapc">${chips}</div>${list.length ? `<div class="pgrid">${list.map((p) => productCard(p, lang)).join('')}</div>` : `<p class="sub">${ko ? '이 주제의 세트를 준비하고 있어요.' : 'Sets for this theme are on the way.'}</p>`}
<h2 class="h3">${ko ? '이 카테고리의 주제' : 'Topics in this category'}</h2><ul class="iltopics">${topics}</ul></section>`;
  }
  const jsonld = { '@context': 'https://schema.org', '@type': 'CollectionPage', name: title, description: desc };
  return html(layout(lang, { title, desc, path, body, img: cat ? sets(cat)[0]?.img : '/p/cafe-girl-clipart.jpg', jsonld }));
}

function shop(lang) {
  const t = T[lang], ko = lang === 'ko';
  const groups = [
    ['planners', ko ? '플래너·인쇄물' : 'Planners & printables', PRODUCTS.filter((p) => !isOrig(p) && !['artist-calendars', 'puzzles'].includes(p.cat))],
    ['puzzles', ko ? '퍼즐북 · 컬러링북' : 'Puzzle & coloring books', PRODUCTS.filter((p) => p.cat === 'puzzles')],
    ['calendars', ko ? '화가별 명화 달력 2027' : 'Artist wall calendars 2027', PRODUCTS.filter((p) => p.cat === 'artist-calendars')],
    ['originals', ko ? '아트트립 오리지널' : 'Arttrip Originals', PRODUCTS.filter(isOrig)],
  ];
  const body = `<section class="wrap sec"><span class="lbl">${t.nav.shop}</span><h1>${ko ? '바로 쓰는 디지털 상품' : 'Ready-to-use digital products'}</h1><p class="sub">${ko ? '명화와 손그림 일러스트로 만든 플래너, 달력, 클립아트를 바로 내려받으세요. 회원가입 없이 구매할 수 있어요.' : 'Planners, calendars and clipart made from masterpieces and hand-drawn illustrations. Instant download, no account needed.'}</p>
<div class="chips wrapc">${groups.map(([id, h]) => `<a href="#${id}">${esc(h)}</a>`).join('')}</div>
${groups.map(([id, h, list]) => `<div class="sh" id="${id}" style="margin-top:34px"><h2>${esc(h)}</h2><span class="small">${list.length}</span></div><div class="pgrid">${list.map((p) => productCard(p, lang)).join('')}</div>`).join('')}</section>`;
  return html(layout(lang, { title: `${ko ? '상품' : 'Shop'} — ${t.site}`, desc: t.heroSub, path: '/shop', body }));
}
function product(lang, env, slug) {
  const t = T[lang]; const p = PRODUCTS.find((x) => x.slug === slug); if (!p) return null; const c = p[lang];
  const link = env[p.checkout], kr = p.payapp && env[p.payapp];
  const edUrl = p.editor ? L(lang, '/editor') + '?tpl=' + p.editor + '&new=1' : p.artist_slug ? L(lang, '/editor') + '?cal=' + p.artist_slug + '&new=1' : '';
  const btn = (href, label, note, cls) => href ? `<a class="paybtn ${cls}" href="${esc(href)}" rel="noopener"><b>${label}</b><span>${note}</span></a>` : `<span class="paybtn off" aria-disabled="true"><b>${label}</b><span>${t.soon}</span></span>`;
  const buy = lang === 'ko'
    ? `<div class="price">$${p.price}</div><div class="paybtns">${kr ? btn(kr, t.payKr, t.payKrNote, 'kr') : ''}${btn(link, t.payGlobal, t.payGlobalNote, 'gl')}</div><p class="small">✓ ${t.guest}</p>`
    : `<div class="price">$${p.price}</div><div class="paybtns">${btn(link, t.buy, 'Card · Apple Pay · Google Pay', 'gl')}</div><p class="small">✓ ${t.guest}</p>`;
  const body = `<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/shop')}">${t.nav.shop}</a></nav><div class="agrid">
<figure class="big"><img src="${p.img}" alt="${esc(c.name)}"></figure><div class="meta"><span class="lbl">${t.instant}</span><h1>${esc(c.name)}</h1>
${c.body.map((x) => `<p>${esc(x)}</p>`).join('')}<h2 class="h3">${t.whatYouGet}</h2><ul class="ul">${c.get.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>
<div class="buy">${buy}</div>${edUrl ? `<a class="pill ghost tryed" href="${edUrl}">${lang === 'ko' ? '편집기에서 미리 꾸며 보기 →' : 'Try it in the editor →'}</a><p class="small">${lang === 'ko' ? '구매 전에도 무료로 꾸며 볼 수 있어요. 구매하면 워터마크 없는 300dpi 파일로 받아요.' : 'Design for free before you buy. After purchase, download watermark-free 300 dpi files.'}</p>` : ''}</div></div></section>`;
  const jsonld = { '@context': 'https://schema.org', '@type': 'Product', name: p.en.name, image: p.img, description: p.en.short, offers: { '@type': 'Offer', price: p.price, priceCurrency: 'USD', availability: link ? 'https://schema.org/InStock' : 'https://schema.org/PreOrder' } };
  return html(layout(lang, { title: `${c.name} — ${t.site}`, desc: c.short, path: '/shop/' + p.slug, body, img: p.img, jsonld }));
}
function pricing(lang, env) {
  const t = T[lang];
  const plan = (k, price, per, link, best) => `<div class="plan${best ? ' best' : ''}">${best ? `<span class="tag">${t.bestValue}</span>` : ''}<b>${t[k]}</b><div class="pr">$${price}<small>${per}</small></div>
<ul class="ul">${t.planPerks.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>${link ? `<a class="pill" href="${esc(link)}" data-polar-checkout>${t.subscribe}</a>` : `<span class="pill off">${t.soon}</span>`}</div>`;
  const body = `<section class="wrap sec center"><span class="lbl">${t.nav.pricing}</span><h1>${t.pricingTitle}</h1><p class="sub">${t.pricingSub}</p>
<div class="plans">${plan('monthly', 9, t.perMonth, env.POLAR_SUB_MONTHLY)}${plan('yearly', 79, t.perYear, env.POLAR_SUB_YEARLY, true)}</div>${lang === 'ko' ? `<p class="small">${esc(T.ko.payNote)}</p>` : ''}</section>`;
  return html(layout(lang, { title: `${t.nav.pricing} — ${t.site}`, desc: t.pricingSub, path: '/pricing', body }));
}
const INFO = {
  about: { en: ['About Arttrip Studio', 'We restore public-domain masterpieces from museum open-access collections and turn them into planners, calendars, prints and patterns.'], ko: ['아트트립 스튜디오 소개', '미술관이 공개한 퍼블릭 도메인 명화를 손질해 플래너, 달력, 인쇄용 그림, 패턴으로 만들어요.'] },
  license: { en: ['License', 'The artworks themselves are in the public domain. Our designs, layouts and restored files may be used for personal projects and small-shop products (up to 500 physical units per design). Reselling or sharing the files themselves is not allowed.'], ko: ['이용 범위', '작품 자체는 퍼블릭 도메인이에요. 우리가 만든 디자인·레이아웃·보정 파일은 개인 용도와 소규모 상품 제작(디자인당 실물 500개까지)에 쓸 수 있어요. 파일 자체를 재판매하거나 공유하는 것은 안 돼요.'] },
  privacy: { en: ['Privacy', 'We only keep what we need to deliver your purchase. Payments are handled by our payment partner; we never see your card details.'], ko: ['개인정보', '구매한 파일을 전달하는 데 필요한 정보만 보관해요. 결제는 결제 대행사가 처리하며, 카드 정보는 저희가 볼 수 없어요.'] },
  terms: { en: ['Terms', 'Digital products are delivered instantly. If a file does not work as described, contact us and we will fix it or refund you.'], ko: ['약관', '디지털 상품은 결제 즉시 전달돼요. 설명과 다르게 작동하면 연락 주세요. 고쳐 드리거나 환불해 드려요.'] },
};
function info(lang, k) {
  const [h, p] = INFO[k][lang];
  return html(layout(lang, { title: `${h} — ${T[lang].site}`, desc: p.slice(0, 150), path: '/' + k, body: `<section class="wrap sec narrow"><h1>${esc(h)}</h1><p>${esc(p)}</p></section>` }));
}
async function notFound(lang) {
  const t = T[lang];
  return html(layout(lang, { title: t.notFound, desc: t.notFound, path: '/', body: `<section class="wrap sec center"><h1>${t.notFound}</h1><a class="pill" href="${L(lang, '/')}">${t.back}</a></section>` }), 404);
}

// ---------- sitemaps ----------
async function sitemapIndex(url, env) {
  const n = (await one(env, 'SELECT COUNT(*) n FROM artworks')).n; const parts = Math.max(1, Math.ceil(n / SITEMAP_SIZE));
  const locs = [];
  for (const lg of ['en', 'ko']) { locs.push(`${url.origin}/sitemaps/pages-${lg}-1.xml`); for (let i = 1; i <= parts; i++) locs.push(`${url.origin}/sitemaps/art-${lg}-${i}.xml`); }
  return xml(`<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${locs.map((l) => `<sitemap><loc>${l}</loc></sitemap>`).join('')}</sitemapindex>`);
}
async function sitemapPart(url, env, kind, lg, n) {
  const pre = url.origin + (lg === 'ko' ? '/ko' : '');
  const alt = (p) => `<xhtml:link rel="alternate" hreflang="en" href="${url.origin}${p}"/><xhtml:link rel="alternate" hreflang="ko" href="${url.origin}/ko${p === '/' ? '' : p}"/>`;
  let paths = [];
  if (kind === 'pages') {
    paths = ['/', '/collections', '/collections/architecture', '/collections/landscape', '/art', '/studio', '/originals', '/illustrations', ...Object.keys(IL_CATS).map((k) => '/illustrations/' + k), '/shop', '/pricing', '/about', '/license', ...Object.keys(THEMES).map((k) => '/art/theme/' + k), ...PRODUCTS.map((p) => '/shop/' + p.slug)];
    const artists = await all(env, 'SELECT artist_slug s, COUNT(*) c FROM artworks GROUP BY artist_slug HAVING c >= 2');
    paths.push(...artists.map((a) => '/artist/' + a.s));
  } else {
    const rows = await all(env, 'SELECT slug FROM artworks ORDER BY rowid LIMIT ? OFFSET ?', SITEMAP_SIZE, (n - 1) * SITEMAP_SIZE);
    paths = rows.map((r) => '/art/' + r.slug);
  }
  const body = paths.map((p) => `<url><loc>${pre}${p === '/' && lg === 'ko' ? '' : p}</loc>${alt(p)}</url>`).join('');
  return xml(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${body}</urlset>`);
}

// ---------- studio data ----------
async function libData(env) {
  const rows = await all(env, 'SELECT id, title t, title_ko tk, artist a, artist_ko ak, artist_slug "as", w, h, theme FROM artworks ORDER BY rowid');
  return new Response(JSON.stringify(rows), { headers: { 'content-type': 'application/json', 'cache-control': 'public, max-age=600' } });
}
// License keys from Polar purchases unlock full-quality editor exports.
async function license(req, env) {
  let key = '';
  try { key = String((await req.json()).key || '').trim().slice(0, 100); } catch { }
  const J = (o) => new Response(JSON.stringify(o), { headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
  if (!key) return J({ ok: false });
  if (env.EDITOR_MASTER_KEY && key === env.EDITOR_MASTER_KEY) return J({ ok: true });
  if (!env.POLAR_ORG_ID) return J({ ok: false, reason: 'not configured' });
  try {
    const r = await fetch('https://api.polar.sh/v1/customer-portal/license-keys/validate', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ key, organization_id: env.POLAR_ORG_ID }) });
    const j = await r.json().catch(() => ({}));
    return J({ ok: r.ok && (j.status === 'granted' || j.status === undefined) && !!j.id });
  } catch { return J({ ok: false }); }
}
function editor(lang, url) {
  const ko = lang === 'ko';
  const fams = ['Lora:ital,wght@0,400;0,600;1,400', 'Playfair+Display:ital,wght@0,400;0,600;1,400', 'Cormorant+Garamond:ital,wght@0,400;0,600;1,400', 'DM+Serif+Display', 'Libre+Baskerville:ital,wght@0,400;0,700;1,400', 'Special+Elite', 'Courier+Prime', 'Caveat:wght@400;700', 'Dancing+Script:wght@400;700', 'Homemade+Apple', 'Amatic+SC:wght@400;700', 'Josefin+Sans:wght@400;600', 'Inter:wght@400;600;700', 'Bebas+Neue', 'Noto+Serif+KR:wght@400;700', 'Gowun+Batang:wght@400;700', 'Noto+Sans+KR:wght@400;700', 'Nanum+Pen+Script', 'Gaegu:wght@400;700'];
  const title = ko ? '아트트립 에디터 — 명화 달력·아트페이퍼 편집' : 'Arttrip Editor — Edit Masterpiece Calendars and Art Papers';
  return new Response(`<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>${title}</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?${fams.map((f) => 'family=' + f).join('&')}&display=swap" rel="stylesheet"><link rel="stylesheet" href="/editor/editor.css"></head><body><div id="ed" data-lang="${lang}"></div><script src="/editor/editor.js"></script></body></html>`, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } });
}
async function studioData(url, env) {
  const want = (url.searchParams.get('art') || '').replace(/[^0-9]/g, '');
  const rows = await all(env, "SELECT id, title t, title_ko tk, artist a, artist_ko ak, w, h, theme FROM artworks WHERE title_ko <> '' ORDER BY rowid LIMIT 120");
  if (want && !rows.find((r) => r.id === want)) { const r = await one(env, 'SELECT id, title t, title_ko tk, artist a, artist_ko ak, w, h, theme FROM artworks WHERE id = ?', want); if (r) rows.unshift(r); }
  return new Response(JSON.stringify(rows), { headers: { 'content-type': 'application/json', 'cache-control': 'public, max-age=600' } });
}
