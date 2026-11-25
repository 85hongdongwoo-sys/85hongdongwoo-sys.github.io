// Arttrip Studio — pages are generated on request from D1 data, in English and Korean.
import { T, THEMES, PRODUCTS, IL_CATS, IL_STYLES, colorName } from './i18n.js';
import { memdb } from './memdb.js';

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
    if (!isKo && req.method === 'GET' && !/^\/(sitemap|robots|img|il|p|css|js|studio)/.test(rest)) {
      const cookie = req.headers.get('cookie') || '';
      const ua = req.headers.get('user-agent') || '';
      if (!/(?:^|;\s*)lang=/.test(cookie) && !BOT.test(ua) && /^ko\b/i.test(req.headers.get('accept-language') || '')) {
        return new Response(null, { status: 302, headers: { location: '/ko' + (rest === '/' ? '' : rest) + url.search, 'set-cookie': 'lang=ko; Path=/; Max-Age=31536000; SameSite=Lax', vary: 'Accept-Language' } });
      }
    }

    // cached HTML
    const cache = caches.default;
    const cacheKey = new Request(url.origin + path + url.search, { method: 'GET' });
    if (req.method === 'GET' && env.CACHE_HTML !== 'off') { const hit = await cache.match(cacheKey); if (hit) return hit; }

    let res;
    try { res = await route(rest, url, lang, env); } catch (e) { res = html(`<pre>${esc(e.stack || e)}</pre>`, 500); }
    if (!res) res = await notFound(lang, rest);
    if (res.status === 200 && req.method === 'GET' && (res.headers.get('content-type') || '').startsWith('text/html')) {
      res = new Response(res.body, res); res.headers.set('cache-control', 'public, max-age=600'); res.headers.set('vary', 'Accept-Language, Cookie');
      if (env.CACHE_HTML !== 'off') ctx.waitUntil(cache.put(cacheKey, res.clone()));
    }
    return res;
  },
};

async function route(p, url, lang, env) {
  let m;
  if (p === '/robots.txt') return new Response(`User-agent: *\nAllow: /\nSitemap: ${url.origin}/sitemap.xml\n`, { headers: { 'content-type': 'text/plain' } });
  if (p === '/sitemap.xml') return sitemapIndex(url, env);
  if ((m = p.match(/^\/sitemaps\/(art|pages)-(en|ko)-(\d+)\.xml$/))) return sitemapPart(url, env, m[1], m[2], +m[3]);
  if (p === '/api/art.json') return studioData(url, env);
  if (p === '/') return home(lang, env);
  if (p === '/art') return gallery(lang, env, url, null);
  if ((m = p.match(/^\/art\/theme\/([a-z-]+)$/)) && THEMES[m[1]]) return gallery(lang, env, url, { theme: m[1] });
  if ((m = p.match(/^\/artist\/([a-z0-9-]+)$/))) return gallery(lang, env, url, { artist: m[1] });
  if ((m = p.match(/^\/art\/([a-z0-9-]+)$/))) return artwork(lang, env, m[1]);
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
function layout(lang, { title, desc, path, body, img, jsonld }) {
  const t = T[lang]; const other = lang === 'ko' ? 'en' : 'ko';
  const enUrl = ORIGIN + path, koUrl = ORIGIN + '/ko' + (path === '/' ? '' : path);
  const nav = [['art', '/art'], ['illus', '/illustrations'], ['shop', '/shop'], ['pricing', '/pricing']].map(([k, href]) => `<a href="${L(lang, href)}">${t.nav[k]}</a>`).join('');
  return `<!DOCTYPE html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${lang === 'ko' ? koUrl : enUrl}"><link rel="alternate" hreflang="en" href="${enUrl}"><link rel="alternate" hreflang="ko" href="${koUrl}"><link rel="alternate" hreflang="x-default" href="${enUrl}">
<meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}">${img ? `<meta property="og:image" content="${esc(ORIGIN + img)}">` : ''}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">${jsonld ? `<script type="application/ld+json">${JSON.stringify(jsonld).replace(/</g, '\\u003c')}</script>` : ''}</head>
<body class="${lang}"><header class="top"><div class="wrap bar"><a class="logo" href="${L(lang, '/')}">Arttrip<span>Studio</span></a><nav>${nav}</nav>
<a class="lang" href="?setlang=${other}" hreflang="${other}">${t.switchTo}</a></div></header>
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
  const covers = Object.fromEntries(cover.map((c) => [c.theme, c.id]));
  const total = counts.reduce((s, c) => s + c.n, 0);
  const prods = PRODUCTS.slice(0, 4).map((p) => productCard(p, lang)).join('');
  const body = `<section class="hero"><div class="wrap hgrid"><div class="htxt"><h1>${esc(t.heroTitle)}</h1><p class="sub">${esc(t.heroSub)}</p>
<div class="row"><a class="pill" href="${L(lang, '/shop')}">${t.shopNow}</a><a class="pill ghost" href="${L(lang, '/art')}">${t.browse}</a></div></div>
<a class="hart" href="${L(lang, '/art/' + hero.slug)}"><img src="/img/${hero.id}.jpg" alt="${esc(tl(hero, lang))}" width="${hero.w}" height="${hero.h}"><span>${esc(tl(hero, lang))} · ${esc(al(hero, lang))}</span></a></div></section>
<section class="wrap sec"><div class="sh"><h2>${t.products}</h2><a href="${L(lang, '/shop')}">${t.nav.shop} →</a></div><div class="pgrid">${prods}</div></section>
<section class="wrap sec"><div class="sh"><h2>${t.themes}</h2><a href="${L(lang, '/art')}">${t.allArt} (${total}) →</a></div>
<div class="themes">${counts.map((c) => `<a class="theme" href="${L(lang, '/art/theme/' + c.theme)}"><img src="/img/${covers[c.theme]}.jpg" alt="" loading="lazy"><b>${esc(THEMES[c.theme]?.[lang] || c.theme)}</b><span>${c.n} ${lang === 'ko' ? '점' : 'artworks'}</span></a>`).join('')}</div></section>
<section class="wrap sec"><div class="sh"><h2>${t.newIn}</h2></div><div class="masonry">${feat.map((a) => tile(a, lang)).join('')}</div></section>`;
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
<div class="chips">${chips}</div><p class="small">${total} ${lang === 'ko' ? '점' : 'artworks'}</p><div class="masonry">${rows.map((a) => tile(a, lang)).join('')}</div>${pager}</section>`;
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
  const mk = ['calendar', 'card', 'poster', 'wallpaper'].map((k) => `<a class="mk" href="/studio/?tool=${{ calendar: 'wallcal', card: 'card', poster: 'poster', wallpaper: 'wallpaper' }[k]}&art=${a.id}&lang=${lang}">${t.make[k]}</a>`).join('');
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
// ---------- original illustrations ----------
const IL_COVER = { everyday: '/il/everyday.png' };
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
    body = `<section class="wrap sec"><span class="lbl">${t.nav.illus}</span><h1>${ko ? '손그림 인물 일러스트' : 'Hand-drawn character illustrations'}</h1>
<p class="sub">${ko ? '한 인물을 여러 동작으로 그린 클립아트와 스티커 세트예요. 카드, 플래너, 블로그, 작은 가게 상품에 쓰세요.' : 'One character, many poses — clipart and sticker sets for cards, planners, blogs and small-shop products.'}</p>
<p class="small">${esc(IL_STYLES[lang])}</p><div class="chips wrapc">${chips}</div><div class="ilgrid">${tiles}</div></section>`;
  } else {
    const c = IL_CATS[cat]; const list = sets(cat);
    title = ko ? `${c.ko} 인물 일러스트 — 클립아트·스티커 | 아트트립 스튜디오` : `${c.en} Illustrations — Character Clipart & Stickers | Arttrip Studio`;
    desc = ko ? `${c.ko} 주제의 손그림 인물 클립아트와 스티커: ${c.topics.map((x) => x[1]).join(', ')}.` : `Hand-drawn ${c.en.toLowerCase()} character clipart and stickers: ${c.topics.map((x) => x[0].toLowerCase()).join(', ')}.`;
    path = '/illustrations/' + cat;
    const topics = c.topics.map((x, i) => { const has = list.some((p) => p.topic === i); return `<li${has ? ' class="on"' : ''}>${esc(ko ? x[1] : x[0])}<em>${has ? (ko ? '판매 중' : 'Available') : (ko ? '준비 중' : 'Coming soon')}</em></li>`; }).join('');
    body = `<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/illustrations')}">${t.nav.illus}</a></nav><h1>${esc(c[lang])}</h1>
<div class="chips wrapc">${chips}</div>${list.length ? `<div class="pgrid">${list.map((p) => productCard(p, lang)).join('')}</div>` : `<p class="sub">${ko ? '이 주제의 세트를 준비하고 있어요.' : 'Sets for this theme are on the way.'}</p>`}
<h2 class="h3">${ko ? '이 카테고리의 주제' : 'Topics in this category'}</h2><ul class="iltopics">${topics}</ul></section>`;
  }
  const jsonld = { '@context': 'https://schema.org', '@type': 'CollectionPage', name: title, description: desc };
  return html(layout(lang, { title, desc, path, body, img: cat ? sets(cat)[0]?.img : '/p/cafe-girl-clipart.jpg', jsonld }));
}

function shop(lang) {
  const t = T[lang];
  const body = `<section class="wrap sec"><span class="lbl">${t.nav.shop}</span><h1>${t.products}</h1><p class="sub">${lang === 'ko' ? '명화로 만든 플래너, 달력, 패턴을 바로 내려받으세요.' : 'Planners, calendars and patterns made from masterpieces. Instant download.'}</p>
<div class="pgrid">${PRODUCTS.map((p) => productCard(p, lang)).join('')}</div></section>`;
  return html(layout(lang, { title: `${t.products} — ${t.site}`, desc: t.heroSub, path: '/shop', body }));
}
function product(lang, env, slug) {
  const t = T[lang]; const p = PRODUCTS.find((x) => x.slug === slug); if (!p) return null; const c = p[lang];
  const link = env[p.checkout];
  const buy = link ? `<a class="pill big" href="${esc(link)}" data-polar-checkout>${t.buy} · $${p.price}</a>` : `<span class="pill big off" aria-disabled="true">${t.soon} · $${p.price}</span>`;
  const body = `<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/shop')}">${t.nav.shop}</a></nav><div class="agrid">
<figure class="big"><img src="${p.img}" alt="${esc(c.name)}"></figure><div class="meta"><span class="lbl">${t.instant}</span><h1>${esc(c.name)}</h1>
${c.body.map((x) => `<p>${esc(x)}</p>`).join('')}<h2 class="h3">${t.whatYouGet}</h2><ul class="ul">${c.get.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>
<div class="buy">${buy}${lang === 'ko' ? `<p class="small">${esc(T.ko.payNote)}</p>` : ''}</div></div></div></section>`;
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
    paths = ['/', '/art', '/illustrations', ...Object.keys(IL_CATS).map((k) => '/illustrations/' + k), '/shop', '/pricing', '/about', '/license', ...Object.keys(THEMES).map((k) => '/art/theme/' + k), ...PRODUCTS.map((p) => '/shop/' + p.slug)];
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
async function studioData(url, env) {
  const want = (url.searchParams.get('art') || '').replace(/[^0-9]/g, '');
  const rows = await all(env, "SELECT id, title t, title_ko tk, artist a, artist_ko ak, w, h, theme FROM artworks WHERE title_ko <> '' ORDER BY rowid LIMIT 120");
  if (want && !rows.find((r) => r.id === want)) { const r = await one(env, 'SELECT id, title t, title_ko tk, artist a, artist_ko ak, w, h, theme FROM artworks WHERE id = ?', want); if (r) rows.unshift(r); }
  return new Response(JSON.stringify(rows), { headers: { 'content-type': 'application/json', 'cache-control': 'public, max-age=600' } });
}
