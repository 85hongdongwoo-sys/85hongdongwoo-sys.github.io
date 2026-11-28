// Large catalog of generated products (calendars, art-print sets, postcard sets, coloring books).
// Data lives in KV (env.VIDS) under pk:index and pk:item:<slug>, written by the private /api/pk/put endpoint.
// PDFs are built in the buyer's browser after the licence key from the receipt is checked against the product's benefit.

const IMG_HOSTS = ['openaccess-cdn.clevelandart.org', 'images.metmuseum.org', 'www.parismuseescollections.paris.fr', 'parismuseescollections.paris.fr', 'api.nga.gov', 'media.nga.gov', 'gongu.copyright.or.kr'];
let IDX = null, IDX_AT = 0;

export const KIND = {
  cal: { en: 'Wall calendar 2027–2030', ko: '벽걸이 달력 2027–2030', ja: '壁掛けカレンダー 2027–2030', icon: '📅' },
  planner: { en: 'Planner 2027–2030', ko: '플래너 2027–2030', ja: 'プランナー 2027–2030', icon: '📒' },
  prints: { en: 'Printable art prints set', ko: '인쇄용 명화 포스터 세트', ja: '印刷用アートプリントセット', icon: '🖼' },
  cards: { en: 'Printable postcard set', ko: '인쇄용 엽서 세트', ja: '印刷用ポストカードセット', icon: '✉' },
  color: { en: 'Coloring book', ko: '컬러링북', ja: 'ぬりえ', icon: '🖍' },
  puz: { en: 'Large-print puzzle book', ko: '큰 글씨 퍼즐북', ja: '大きな文字のパズル本', icon: '🧩' },
  pbn: { en: 'Acrylic paint-by-number pattern', ko: '아크릴화 도안키트(범용)', ja: 'アクリル画 数字ぬりえ図案', icon: '🎨' },
};
const KIND_ORDER = ['cal', 'planner', 'prints', 'cards', 'puz', 'pbn', 'color'];

export async function pkIndex(env) {
  if (IDX && Date.now() - IDX_AT < 300000) return IDX;
  const j = env.VIDS ? await env.VIDS.get('pk:index', { type: 'json', cacheTtl: 300 }) : null;
  IDX = Array.isArray(j) ? j : []; IDX_AT = Date.now(); return IDX;
}
let RD = null, RD_AT = 0;
async function pkRedir(env, slug, lang) {
  if (!RD || Date.now() - RD_AT > 300000) { RD = (env.VIDS && await env.VIDS.get('pk:redir', { type: 'json', cacheTtl: 300 })) || {}; RD_AT = Date.now(); }
  const to = RD[slug]; if (!to) return null;
  return new Response(null, { status: 301, headers: { location: (lang === 'en' ? '' : '/' + lang) + '/shop/c/' + to } });
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
  if (req.method === 'GET') { const u = new URL(req.url); if ((await sha(u.searchParams.get('tok') || '')) !== env.PK_HASH) return J({ ok: false }, 403, CORS); const r = env.POLAR_TOKEN ? await fetch('https://api.polar.sh/v1/products/?limit=1', { headers: { authorization: 'Bearer ' + env.POLAR_TOKEN } }) : null; return J({ ok: true, token: !!env.POLAR_TOKEN, polar: r ? r.status : 0 }, 200, CORS); }
  if (!env.PK_HASH || !env.VIDS) return J({ ok: false }, 501, CORS);
  let b; try { b = await req.json(); } catch { return J({ ok: false }, 400, CORS); }
  if ((await sha(String(b.tok || ''))) !== env.PK_HASH) return J({ ok: false }, 403, CORS);
  const puts = Array.isArray(b.puts) ? b.puts : [];
  for (const [k, v] of puts) if (/^pk:/.test(k)) await env.VIDS.put(k, /^pk:img:/.test(k) && typeof v === 'string' ? Uint8Array.from(atob(v), (ch) => ch.charCodeAt(0)) : typeof v === 'string' ? v : JSON.stringify(v));
  const dels = Array.isArray(b.dels) ? b.dels : [];
  for (const k of dels) if (/^pk:/.test(k)) await env.VIDS.delete(k);
  IDX = null; CH.clear();
  return J({ ok: true, n: puts.length, d: dels.length }, 200, CORS);
}

// ---------- Paris Musées GraphQL relay (token-protected, used for harvesting) ----------
export async function pkParis(req, env) {
  if (req.method === 'OPTIONS') return new Response(null, { headers: CORS });
  let b; try { b = await req.json(); } catch { return J({ ok: false }, 400, CORS); }
  if ((await sha(String(b.tok || ''))) !== env.PK_HASH) return J({ ok: false }, 403, CORS);
  if (!env.PARIS_TOKEN) return J({ ok: false, err: 'no PARIS_TOKEN' }, 501, CORS);
  const r = await fetch('https://apicollections.parismusees.paris.fr/graphql', { method: 'POST', headers: { 'content-type': 'application/json', 'auth-token': env.PARIS_TOKEN }, body: JSON.stringify({ query: b.query, variables: b.variables || {} }) });
  return new Response(await r.text(), { status: r.status, headers: { 'content-type': 'application/json', ...CORS } });
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
  const res = new Response(r.body, { headers: { 'content-type': (r.headers.get('content-type') || 'image/jpeg').replace('pjpeg', 'jpeg'), 'cache-control': 'public, max-age=2592000', 'access-control-allow-origin': '*' } });
  ctx && ctx.waitUntil && ctx.waitUntil(caches.default.put(key, res.clone()));
  return res;
}
const pi = (u) => (u && u[0] === '/') ? u : '/pi?u=' + encodeURIComponent(u || '');

// ---------- unlock: (1) signed download pass, (2) Polar checkout id after payment, (3) licence key from the receipt ----------
const enc = new TextEncoder();
async function hmac(env, msg) {
  const k = await crypto.subtle.importKey('raw', enc.encode('pk-pass:' + (env.POLAR_TOKEN || env.PK_HASH || 'x')), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return Array.from(new Uint8Array(await crypto.subtle.sign('HMAC', k, enc.encode(msg)))).map((b) => b.toString(16).padStart(2, '0')).join('').slice(0, 40);
}
const passFor = async (env, slug) => { const exp = Date.now() + 365 * 864e5; return exp + '.' + (await hmac(env, slug + '|' + exp)); };
async function passOk(env, slug, pass) { const [exp, sig] = String(pass || '').split('.'); return !!sig && +exp > Date.now() && sig === (await hmac(env, slug + '|' + exp)); }
const polar = (env, path) => fetch('https://api.polar.sh/v1' + path, { headers: { authorization: 'Bearer ' + env.POLAR_TOKEN, accept: 'application/json' } }).then((r) => r.ok ? r.json() : null).catch(() => null);
const tiers = (env) => { try { return JSON.parse(env.PK_TIERS || '{}'); } catch { return {}; } };
export const tierFor = (env, it) => { const t = tiers(env); return it.k === 'puz' ? t['puz' + it.p] : t[it.k]; };
export async function pkBuy(env, slug, url) {
  const it = await pkItem(env, slug); if (!it) return null;
  if (it.c) return Response.redirect(it.c, 302);
  const tid = tierFor(env, it); if (!tid || !env.POLAR_TOKEN) return null;
  const r = await fetch('https://api.polar.sh/v1/checkouts/', { method: 'POST', headers: { authorization: 'Bearer ' + env.POLAR_TOKEN, 'content-type': 'application/json' }, body: JSON.stringify({ products: [tid], metadata: { slug }, success_url: url.origin + '/dl/' + slug + '?checkout_id={CHECKOUT_ID}', allow_discount_codes: true }) }).catch(() => null);
  const j = r && r.ok ? await r.json().catch(() => null) : null;
  return j && j.url ? Response.redirect(j.url, 303) : new Response('Checkout is temporarily unavailable. Please try again in a minute or write to hello@arttripstudio.com.', { status: 503 });
}
async function paidByCheckout(env, it, cid) {
  if (!env.POLAR_TOKEN || !/^[0-9a-f-]{36}$/.test(cid)) return false;
  const c = await polar(env, '/checkouts/' + cid); if (!c || !['succeeded', 'confirmed'].includes(c.status)) return false;
  if (it.pid && (c.product_id === it.pid || (c.products || []).some((p) => p.id === it.pid))) return true;
  return !!(c.metadata && c.metadata.slug === it.s && c.product_id === tierFor(env, it));
}
async function paidByKey(env, it, key) {
  if (!env.POLAR_ORG_ID) return false;
  const r = await fetch('https://api.polar.sh/v1/customer-portal/license-keys/validate', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ key, organization_id: env.POLAR_ORG_ID }) }).catch(() => null);
  const j = r && r.ok ? await r.json().catch(() => ({})) : {};
  if (j.status !== 'granted') return false;
  const all = String(env.PK_ALL_BENEFITS || '').split(',').filter(Boolean);
  if (j.benefit_id === it.b || all.includes(j.benefit_id)) return true;
  if (!env.POLAR_TOKEN || !j.customer_id) return false;
  const pid = it.pid || tierFor(env, it); if (!pid) return false;
  const o = await polar(env, '/orders/?customer_id=' + encodeURIComponent(j.customer_id) + '&product_id=' + encodeURIComponent(pid) + '&limit=100');
  return !!o && (o.items || []).some((x) => x.paid !== false && x.status !== 'refunded' && (it.pid ? true : (x.metadata && x.metadata.slug === it.s)));
}
export async function pkUnlock(req, env) {
  let b = {}; try { b = await req.json(); } catch { }
  const slug = String(b.slug || ''), key = String(b.key || '').trim().slice(0, 100), cid = String(b.cid || '').trim(), pass = String(b.pass || '');
  const it = await pkItem(env, slug); if (!it) return J({ ok: false });
  let ok = (await passOk(env, slug, pass)) || !!(env.EDITOR_MASTER_KEY && key && key === env.EDITOR_MASTER_KEY);
  if (!ok && cid) ok = await paidByCheckout(env, it, cid);
  if (!ok && key) ok = await paidByKey(env, it, key);
  if (!ok) return J({ ok: false });
  const out = { ok: true, k: it.k, title: it.en.name, pass: await passFor(env, slug) };
  if (it.k === 'puz') return J({ ...out, pz: it.pz });
  if (it.k === 'pbn') { const ch = await env.VIDS.get('pk:pbnd:' + it.d, { type: 'json' }); const d = ch && ch[it.s]; if (!d) return J({ ok: false }); return J({ ...out, title: it.w[0].t, artist: it.w[0].a, pbn: d }); }
  return J({ ...out, works: it.w.map((w) => ({ t: w.t, a: w.a, d: w.d, u: pi(w.u || w.v), W: w.W, H: w.H })) });
}

// ---------- copy ----------
function copy(it, lang) {
  const ko = lang === 'ko', ja = lang === 'ja', c = it[lang] || it.en, k = KIND[it.k], n = (it.w || []).length;
  if (it.k === 'pbn') { const w = it.w[0], nc = it.nc || 20;
    return { name: c.name, body: ja ? [`${w.a}「${w.t}」（${w.d}）を数字ぬりえの図案にしました。キットを買わずに手持ちのアクリル絵の具で塗れるよう、番号ごとにリキテックス ベーシックスとウィンザー＆ニュートン ガレリアの絵の具名（または2色と白の混色比）を記しています。全${nc}色です。`, `2枚1セットです。1枚目は番号入りの図案のみ、2枚目は完成見本と色番号表です。A4・USレター・A3・A2でダウンロードでき、200g/m²以上の厚紙に印刷するか、カーボン紙でキャンバスに写してお使いください。`] : ko ? [`${w.a}의 「${w.t}」(${w.d})를 숫자 색칠 도안으로 만들었어요. 키트를 사지 않고 집에 있는 아크릴 물감으로 칠할 수 있게, 번호마다 리퀴텍스 베이직스와 윈저앤뉴튼 갤러리아 물감 이름(또는 두 물감과 흰색을 섞는 비율)을 적었어요. 모두 ${nc}가지 색이에요.`, `2장 한 세트예요. 1장은 번호 도안만, 2장은 완성작 미리보기와 색 번호표예요. A4·레터·A3·A2 크기로 받아 200g 이상 두꺼운 종이에 인쇄하거나, 먹지로 캔버스에 옮겨 그리세요.`]
      : [`${w.t} by ${w.a} (${w.d}) as a paint-by-number pattern you can paint with the acrylics you already own: every number is matched to real Liquitex BASICS and Winsor & Newton Galeria tube colours, or a simple mix of two tubes and white. ${nc} colours in all.`, `A 2-page set: page 1 is the numbered outline only, page 2 shows the finished picture and the colour key. Download A4, US Letter, A3 or A2 and print on 200 g/m² paper, or trace onto canvas with graphite transfer paper.`] }; }
  if (it.k === 'puz') { const z = it.pz, lv = { easy: ko ? '쉬움' : ja ? 'やさしい' : 'easy', medium: ko ? '보통' : ja ? 'ふつう' : 'medium', hard: ko ? '어려움' : ja ? 'むずかしい' : 'hard' }[z.level], nm = (ja ? { ws: '文字さがし', sudoku: 'ナンプレ（数独）', maze: '迷路', scramble: '文字並べかえ', numsearch: '数字さがし', crypto: '名言の暗号解き', mix: '脳トレ（文字さがし・数独・迷路・並べかえ・数字さがし・暗号）' } : { ws: ko ? '낱말찾기' : 'word search', sudoku: ko ? '스도쿠' : 'sudoku', maze: ko ? '미로' : 'maze', scramble: ko ? '단어 섞기' : 'word scramble', numsearch: ko ? '숫자 찾기' : 'number search', crypto: ko ? '명언 암호 풀기' : 'cryptogram', mix: ko ? '두뇌 게임(낱말찾기·스도쿠·미로·단어 섞기·숫자 찾기·암호 풀기)' : 'mixed brain-game' })[z.type];
    return { name: c.name, body: ja ? [`シニアの方にも見やすい大きな文字の${nm}${z.n}問集です（難易度：${lv}）。${z.type === 'ws' ? `テーマは「${c.theme || z.theme}」で、1問に10〜14語が隠れています。` : ''}1ページ1問、マスと文字を大きくしました。`, `解答はすべて巻末にあります。問題は英語です。お支払い後A4またはUSレターのPDFでダウンロードでき、何度でも印刷できるので、ご家族や介護施設、レクリエーションにも便利です。`] : ko ? [`어르신도 편하게 볼 수 있는 큰 글씨 ${nm} ${z.n}문제 모음이에요(난이도: ${lv}).${z.type === 'ws' ? ` 주제는 '${c.theme || z.theme}'이고 한 문제에 단어 10~14개가 숨어 있어요.` : z.type === 'scramble' ? ` 주제는 '${c.theme || z.theme}'이고 한 쪽에 섞인 단어 15개가 나와요.` : z.type === 'crypto' ? ' 셰익스피어, 프랭클린, 성경, 속담 같은 오래된 명언을 암호로 바꿨어요.' : ''} 한 장에 한 문제씩, 칸과 글자를 크게 만들었어요.`, `맨 뒤에 정답이 모두 들어 있어요. 결제 후 A4나 레터 용지 PDF로 받아 몇 번이든 다시 인쇄할 수 있어서 복지관, 요양원, 가족 모임에서 쓰기 좋아요.`]
      : [`${z.n} large-print ${nm} puzzles (${lv})${z.type === 'ws' ? ` on the theme '${z.theme}', each hiding 10 to 14 words` : ''}. One puzzle per page with big, clear letters and boxes that are easy on the eyes.`, `All answers are at the back. Download as A4 or US Letter PDF and print as many copies as you like, for yourself, a parent or grandparent, a care home or an activity group.`] }; }
  const L2 = (it[lang] || it.en), who = it.g === 'artist' ? (L2.who || it.en.who) : (L2.theme || it.en.theme);
  const body = {
    cal: ko ? [`${who}의 그림 ${n}점으로 만든 벽걸이 달력이에요. 표지 1장과 1월부터 12월까지 달마다 그림 한 점, 그 아래 날짜 칸이 있어요. 한 번 사면 2027년부터 2030년까지 원하는 해의 달력을 모두 받을 수 있어요.`, `미술관이 저작권 없이 공개한 고해상도 원본으로 만들어 A4나 레터 용지에 바로 인쇄할 수 있어요. 결제 후 영수증의 라이선스 키로 PDF를 내려받아요.`]
      : ja ? [`${who}の作品${n}点でつくった壁掛けカレンダーです。表紙と、1月から12月まで毎月1点の名画、その下に日付欄があります。一度購入すれば2027年から2030年まで、お好きな年のカレンダーを何度でもダウンロードできます。`, `美術館がオープンアクセスで公開した高解像度の原画からつくり、A4またはUSレターにそのまま印刷できます。お支払い後すぐにPDFをダウンロードできます。`]
      : [`A wall calendar with ${n} works by ${who}: a cover page plus one picture for every month from January to December, with a clean date grid below. One purchase covers every year from 2027 to 2030, so you can print a fresh one each January.`, `Made from high-resolution open-access museum files, ready to print on A4 or US Letter paper. Download the PDF with the licence key from your receipt.`],
    planner: ko ? [`${who}의 그림 ${n}점으로 꾸민 인쇄용 플래너예요. 표지, 한눈에 보는 1년, 달마다 그림 한 장과 월간 달력·메모 칸, 그리고 매주 요일별로 적는 주간 페이지가 들어 있어요.`, `한 번 사면 2027년부터 2030년까지 원하는 해의 플래너를 모두 받을 수 있어요. A4나 레터 용지에 인쇄해 바인더에 끼우거나 제본해서 쓰세요.`]
      : ja ? [`${who}の作品${n}点で彩った印刷用プランナーです。表紙、年間カレンダー、毎月の名画と月間カレンダー・メモ欄、そして毎週の曜日別ウィークリーページが入っています。`, `一度購入すれば2027年から2030年まで、お好きな年のプランナーをダウンロードできます。A4またはUSレターに印刷して、バインダーに挟んだり製本したりしてお使いください。`]
      : [`A printable planner decorated with ${n} works by ${who}: cover, year at a glance, a full-page picture and monthly calendar with notes for every month, plus a weekly page for every week.`, `One purchase covers every year from 2027 to 2030. Print on A4 or US Letter and keep it in a binder or have it bound.`],
    prints: ko ? [`${who}의 그림 ${n}점을 한 장에 한 점씩 담은 인쇄용 포스터 세트예요. 액자에 넣거나 벽에 붙이기 좋아요.`, `A4·레터·A3 크기로 내려받아 집이나 사무실 프린터, 인쇄소에서 뽑을 수 있어요.`]
      : ja ? [`${who}の作品${n}点を1ページに1点ずつ収めた印刷用アートプリントセットです。額に入れたり、壁に飾ったり、贈り物にもぴったりです。`, `A4・USレター・A3サイズでダウンロードし、ご家庭のプリンターや印刷店で印刷できます。`]
      : [`${n} printable art prints of ${who}, one picture per page with a small caption, perfect for frames, gallery walls and gifts.`, `Download as A4, US Letter or A3 PDFs and print at home or at a print shop.`],
    cards: ko ? [`${who}의 그림 ${n}점으로 만든 엽서 세트예요. A4 한 장에 엽서 4장이 들어가고 자르는 선이 표시돼 있어요.`, `두꺼운 종이에 인쇄해 잘라서 카드, 초대장, 책갈피로 쓰세요.`]
      : ja ? [`${who}の作品${n}点でつくったポストカードセットです。A4用紙1枚に4枚分、切り取り線つきで入っています。`, `厚手の紙に印刷して切り取れば、メッセージカードや招待状、しおりとして使えます。`]
      : [`A set of ${n} postcards featuring ${who}, four cards per A4 or Letter page with crop marks.`, `Print on card stock and cut out for notes, invitations, party favours and scrapbooks.`],
    color: ko ? [`${who}에서 고른 옛 판화와 드로잉 ${n}점을 색칠하기 좋은 선 그림으로 바꾼 어른용 컬러링북이에요.`, `한 장에 그림 하나씩, 원작 제목과 작가를 작게 적었어요. 몇 번이든 다시 인쇄해서 색칠할 수 있어요.`]
      : ja ? [`${who}の古版画や素描${n}点を、塗りやすい線画にした大人のぬりえです。`, `1ページに1作品、原作のタイトルと画家名を小さく記しています。何度でも印刷して楽しめます。`]
      : [`A grown-up coloring book of ${n} pages made from antique prints and drawings of ${who}, cleaned up into crisp line art.`, `One picture per page with the original title and artist. Print as many copies as you like.`],
  }[it.k];
  return { name: c.name, short: c.short || body[0], body };
}


// ---------- product mock-ups drawn in HTML/CSS (no stored images needed) ----------
export const MOCK_CSS = `<style>.mk{position:relative;width:100%;aspect-ratio:4/3;background:#e9e2d6;border-radius:14px;overflow:hidden;container-type:inline-size}.pimg .mk{height:100%;aspect-ratio:auto;border-radius:0}
.mk img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:cover}.mk .pic,.mk .q4 div{position:relative;overflow:hidden;background:#e7e0d3}
.mk .cv,.mk .sp{position:absolute;background:#fffdf9;box-shadow:.6cqw 1.2cqw 2.6cqw rgba(60,45,25,.28)}
.mk .cv{left:6%;top:14%;width:31%;height:72%;display:flex;flex-direction:column;padding:2.2cqw 2.2cqw 1.6cqw}
.mk .cv .pic{flex:0 0 58%;overflow:hidden;border:.25cqw solid #e2dbcf}.mk .cv b{font:700 2.5cqw/1.15 Georgia,serif;color:#222;text-align:center;margin-top:1.6cqw;overflow:hidden;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical}
.mk .cv small{font:1.4cqw/1.2 system-ui,sans-serif;color:#8a8175;text-align:center;margin-top:auto;letter-spacing:.06em;text-transform:uppercase}
.mk .sp{left:41%;right:5%;top:19%;height:62%;display:flex}.mk .sp>div{flex:1;padding:1.8cqw;display:flex;flex-direction:column;gap:1cqw}.mk .sp>div+div{border-left:.3cqw solid #e6dfd2}
.mk .sp .pic{flex:0 0 55%;overflow:hidden}.mk .t{font:700 1.5cqw/1 system-ui,sans-serif;color:#444;letter-spacing:.05em}
.mk .gr{flex:1;display:grid;grid-template-columns:repeat(7,1fr);gap:.3cqw;font:1.1cqw/1 system-ui,sans-serif;color:#777}.mk .gr i{border-top:.15cqw solid #ddd;padding-top:.3cqw;font-style:normal}
.mk .ln{flex:1;background:repeating-linear-gradient(transparent 0 2.2cqw,#ddd6c9 2.2cqw 2.4cqw)}.mk .q4{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:1cqw}.mk .q4 div{overflow:hidden}</style>`;
function mock(it, lang) {
  const ws = (it.w || []).map((w) => pi(w.v || w.u)), vs = ws.length ? ws : [pi(it.v)].concat((it.vs || []).map(pi));
  const im = (i) => `<img src="${vs[i % vs.length]}" alt="" loading="lazy">`;
  const T = { en: ['JANUARY 2027', 'WEEK 1', 'NOTES'], ko: ['2027년 1월', '1주차', '메모'], ja: ['2027年1月', '第1週', 'メモ'] }[lang] || ['JANUARY 2027', 'WEEK 1', 'NOTES'];
  const days = Array.from({ length: 35 }, (_, i) => `<i>${i >= 5 && i - 4 <= 31 ? i - 4 : ''}</i>`).join('');
  const nm = String((it[lang] || it.en).name || '').replace(/\s+—\s.*$/, '').replace(/\s*\(Vol\.[^)]*\)|\s*\d+집$|（第\d+集）/g, '');
  const kind = (KIND[it.k] || {})[lang] || '';
  const right = it.k === 'cal' ? `<div><div class="pic">${im(1)}</div><div class="t">${T[0]}</div><div class="gr">${days}</div></div>`
    : it.k === 'planner' ? `<div><div class="t">${T[1]}</div><div class="ln"></div></div>`
    : it.k === 'cards' ? `<div><div class="q4">${[2, 3, 4, 5].map((i) => `<div>${im(i)}</div>`).join('')}</div></div>`
    : `<div><div class="pic" style="flex:1">${im(2)}</div></div>`;
  const left = it.k === 'planner' ? `<div><div class="t">${T[0]}</div><div class="pic">${im(1)}</div><div class="gr">${days}</div></div>` : `<div><div class="pic" style="flex:1">${im(1)}</div></div>`;
  return `<div class="mk"><div class="cv"><div class="pic">${im(0)}</div><b>${nm}</b><small>${kind}</small></div><div class="sp">${left}${right}</div></div>`;
}

const card = (it, lang, L, esc) => `<a class="pcard" href="${L(lang, '/shop/c/' + it.s)}"><div class="pimg">${["cal", "planner", "prints", "cards"].includes(it.k) ? mock(it, lang) : `<img src="${pi(it.v)}" alt="${esc((it[lang] || it.en).name)}" loading="lazy">`}</div><b>${esc((it[lang] || it.en).name)}</b><span>${esc(KIND[it.k][lang])}</span><em>$${it.p}</em></a>`;

// ---------- shop front: catalogue sections ----------
export async function pkShopTop(lang, env, h) {
  const { L, esc } = h; const ko = lang === 'ko', ja = lang === 'ja';
  const all = await pkIndex(env); if (!all.length) return '';
  const S = [
    ['korea', ko ? '한국 명화 (이중섭·김홍도·신윤복…)' : ja ? '韓国の名画（イ・ジュンソプ、キム・ホンド…）' : 'Korean masterpieces', (x) => x.s.startsWith('korean-'), '?c=korea'],
    ['paris', ko ? '파리 시립미술관 명화' : ja ? 'パリ市立美術館の名画' : 'Paris Musées masterpieces', (x) => x.s.startsWith('paris-'), '?c=paris'],
    ['pbn', KIND.pbn[lang], (x) => x.k === 'pbn', '?k=pbn'],
    ['puz', ko ? '어르신 큰 글씨 퍼즐북' : ja ? '大きな文字のパズル本' : 'Large-print puzzle books', (x) => x.k === 'puz', '?k=puz'],
    ['cal', KIND.cal[lang], (x) => x.k === 'cal' && !/^(korean|paris)-/.test(x.s), '?k=cal'],
    ['prints', KIND.prints[lang], (x) => x.k === 'prints' && !/^(korean|paris)-/.test(x.s), '?k=prints'],
  ];
  return MOCK_CSS + S.map(([id, h2, f, q]) => { const l = all.filter(f); if (!l.length) return ''; return `<div class="sh" id="c-${id}" style="margin-top:30px"><h2>${esc(h2)}</h2><a href="${L(lang, '/shop/c')}${q}">${ko ? `${l.length}종 모두 보기` : ja ? `全${l.length}点を見る` : `See all ${l.length}`} →</a></div><div class="pgrid">${l.slice(0, 8).map((x) => card(x, lang, L, esc)).join('')}</div>`; }).join('');
}

// ---------- catalogue listing ----------
export async function pkList(lang, env, url, h) {
  const { layout, html, esc, L, T } = h; const ko = lang === 'ko', ja = lang === 'ja', t = T[lang];
  const all = await pkIndex(env); if (!all.length) return null;
  const k = url.searchParams.get('k') || '', g = url.searchParams.get('g') || '', cc = url.searchParams.get('c') || '', q = (url.searchParams.get('q') || '').toLowerCase().slice(0, 60);
  let list = all.filter((x) => (!k || x.k === k) && (!g || x.g === g) && (!cc || (cc === 'korea' ? x.s.startsWith('korean-') : cc === 'paris' ? x.s.startsWith('paris-') : true)) && (!q || (x.en.name + ' ' + (x.ko && x.ko.name)).toLowerCase().includes(q)));
  const per = 48, pages = Math.max(1, Math.ceil(list.length / per)), page = Math.min(pages, Math.max(1, +(url.searchParams.get('p') || 1)));
  const qs = (o) => { const s = new URLSearchParams(); const v = { k, g, c: cc, q, ...o }; for (const [a, b] of Object.entries(v)) if (b && !(a === 'p' && b === 1)) s.set(a, b); const x = s.toString(); return L(lang, '/shop/c') + (x ? '?' + x : ''); };
  const chip = (label, href, on) => `<a href="${href}"${on ? ' aria-current="true"' : ''}>${esc(label)}</a>`;
  const body = `${MOCK_CSS}<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/shop')}">${t.nav.shop}</a></nav><span class="lbl">${ko ? `${all.length}종` : ja ? `${all.length}点` : `${all.length} products`}</span><h1>${ko ? '명화 달력·플래너·포스터·엽서·퍼즐북' : ja ? '名画カレンダー・プランナー・ポスター・ポストカード・パズル本' : 'Masterpiece calendars, planners, prints, postcards & puzzle books'}</h1>
<p class="sub">${ko ? '세계 미술관이 공개한 명화로 만든 인쇄용 디지털 상품이에요. 결제 후 바로 PDF로 받아요.' : ja ? '世界の美術館が公開した名画でつくった、印刷して使えるデジタル商品です。お支払い後すぐにPDFをダウンロードできます。' : 'Printable digital products made from open-access museum masterpieces. Instant PDF download.'}</p>
<form class="row" action="${L(lang, '/shop/c')}" style="margin:14px 0"><input name="q" value="${esc(q)}" placeholder="${ko ? '작가나 주제 검색 (예: Monet, cats)' : ja ? '画家やテーマで検索（例：Monet, cats）' : 'Search an artist or theme (e.g. Monet, cats)'}" style="flex:1;min-width:0;padding:10px 14px;border:1px solid #d9d1c3;border-radius:999px;font:inherit">${k ? `<input type="hidden" name="k" value="${esc(k)}">` : ''}</form>
<div class="chips wrapc">${chip(ko ? '전체' : ja ? 'すべて' : 'All', qs({ k: '', p: 1 }), !k)}${KIND_ORDER.map((x) => chip(KIND[x][lang], qs({ k: x, p: 1 }), k === x)).join('')}</div>
<div class="chips wrapc" style="margin-top:8px">${chip(ko ? '작가별' : ja ? '画家別' : 'By artist', qs({ g: g === 'artist' ? '' : 'artist', p: 1 }), g === 'artist')}${chip(ko ? '주제별' : ja ? 'テーマ別' : 'By theme', qs({ g: g === 'theme' ? '' : 'theme', p: 1 }), g === 'theme')}</div>
<div class="pgrid" style="margin-top:22px">${list.slice((page - 1) * per, page * per).map((x) => card(x, lang, L, esc)).join('') || `<p>${ko ? '찾는 상품이 없어요.' : ja ? '該当する商品がありません。' : 'Nothing found.'}</p>`}</div>
${pages > 1 ? `<nav class="pager">${page > 1 ? `<a href="${qs({ p: page - 1 })}">←</a>` : ''}<span>${page} / ${pages}</span>${page < pages ? `<a href="${qs({ p: page + 1 })}">→</a>` : ''}</nav>` : ''}</section>`;
  return html(layout(lang, { title: `${ko ? '명화 달력·플래너·포스터·엽서·퍼즐북' : ja ? '名画カレンダー・プランナー・ポスター・パズル本' : 'Masterpiece calendars, planners, prints, postcards & puzzle books'}${page > 1 ? ` (${page})` : ''} — ${t.site}`, desc: ko ? '세계 미술관 명화로 만든 인쇄용 달력, 플래너, 포스터, 엽서, 큰 글씨 퍼즐북.' : ja ? '世界の美術館の名画でつくった印刷用カレンダー、プランナー、ポスター、ポストカード、大きな文字のパズル本。' : 'Printable calendars, planners, art prints, postcards and large-print puzzle books from museum masterpieces.', path: '/shop/c', body, jaReady: true, noindex: !!(q || page > 1 && (k || g || cc)) }));
}

// ---------- product page ----------
export async function pkPage(lang, env, slug, h) {
  const { layout, html, esc, L, T } = h; const ko = lang === 'ko', ja = lang === 'ja', t = T[lang];
  const it = await pkItem(env, slug); if (!it) return pkRedir(env, slug, lang);
  const c = copy(it, lang), k = KIND[it.k];
  const sibs = (await pkIndex(env)).filter((x) => x.f === it.f && x.s !== it.s).slice(0, 6);
  const btn = (it.c || tierFor(env, it)) ? `<a class="paybtn gl" href="${esc(it.c || '/buy/' + it.s)}" rel="nofollow noopener"><b>${ko ? '해외결제' : t.buy}</b><span>${ko ? '카드 · Apple Pay · Google Pay' : ja ? 'カード · Apple Pay · Google Pay（米ドル）' : 'Card · Apple Pay · Google Pay'}</span></a>` : `<span class="paybtn off"><b>${t.buy}</b><span>${t.soon}</span></span>`;
  const body = `${it.k === 'cal' || it.k === 'planner' || it.k === 'prints' || it.k === 'cards' ? '' : MOCK_CSS}<section class="wrap sec"><nav class="crumb"><a href="${L(lang, '/shop')}">${t.nav.shop}</a> › <a href="${L(lang, '/shop/c?k=' + it.k)}">${esc(k[lang])}</a></nav><div class="agrid">
<figure class="big">${["cal", "planner", "prints", "cards"].includes(it.k) ? MOCK_CSS + mock(it, lang) : `<img src="${pi(it.v || it.w[0].v || it.w[0].u)}" alt="${esc(c.name)}">`}</figure><div class="meta"><span class="lbl">${t.instant} · ${esc(k[lang])}</span><h1>${esc(c.name)}</h1>
${c.body.map((x) => `<p>${esc(x)}</p>`).join('')}
<div class="buy"><div class="price">$${it.p}</div><div class="paybtns">${btn}</div><p class="small">✓ ${t.guest}</p><p class="small"><a href="${L(lang, '/dl/' + it.s)}">${ko ? '이미 구매했어요 → 라이선스 키로 받기' : ja ? '購入済みの方 → ライセンスキーでダウンロード' : 'Already bought? Download with your licence key →'}</a></p></div></div></div>
${it.k === 'pbn' && it.key ? `<h2 class="h3" style="margin-top:34px">${ko ? `색 번호표 (${it.key.length}색) — 회사별 가장 비슷한 물감 이름·번호` : ja ? `色番号表（${it.key.length}色）— メーカー別の絵の具名` : `Colour key (${it.key.length} colours) — closest tube name and number by brand`}</h2><div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:14px;min-width:520px"><thead><tr style="text-align:left;border-bottom:2px solid #ddd"><th style="padding:6px">No.</th><th></th><th style="padding:6px">Liquitex BASICS</th><th style="padding:6px">Winsor &amp; Newton Galeria</th></tr></thead><tbody>${it.key.map((k, i) => `<tr style="border-bottom:1px solid #eee"><td style="padding:6px;font-weight:700">${i + 1}</td><td style="padding:6px"><span style="display:inline-block;width:34px;height:20px;border-radius:4px;background:rgb(${k[2]})"></span></td><td style="padding:6px">${k[3] ? `<b>${esc(k[3])}</b><br><span class="small">${ko ? '정확한 색: ' : ja ? '正確な色: ' : 'Exact mix: '}${esc(k[0])}</span>` : esc(k[0])}</td><td style="padding:6px">${k[4] ? `<b>${esc(k[4])}</b><br><span class="small">${ko ? '정확한 색: ' : ja ? '正確な色: ' : 'Exact mix: '}${esc(k[1])}</span>` : esc(k[1])}</td></tr>`).join('')}</tbody></table></div><p class="small" style="margin-top:8px">${ko ? '굵은 글씨는 그 색과 가장 비슷한 물감 한 가지(# 뒤는 물감 번호)예요. 더 정확하게 칠하려면 아래 혼합 비율대로 섞으세요. "1x A + 2x Titanium White"는 A 물감 1 : 흰색 2 비율이라는 뜻이에요.' : ja ? '「1x A + 2x Titanium White」は、絵の具A 1に対して白2の割合で混ぜるという意味です。' : '"1x A + 2x Titanium White" means one part A mixed with two parts white.'}</p>` : ''}
${it.k === 'puz' || it.k === 'pbn' ? '' : `<h2 class="h3" style="margin-top:34px">${ko ? `들어 있는 그림 ${it.w.length}점` : ja ? `収録作品 ${it.w.length}点` : `The ${it.w.length} works inside`}</h2>
<div class="stgrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px">${it.w.map((w) => `<figure style="margin:0"><img src="${pi(w.v || w.u)}" alt="${esc(w.t)}" loading="lazy" style="width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px;background:#eee"><figcaption class="small" style="margin-top:6px;overflow-wrap:anywhere">${esc(w.t)}${w.d ? ', ' + esc(w.d) : ''}<br><span style="opacity:.7">${esc(w.a || '')}</span></figcaption></figure>`).join('')}</div>`}
${sibs.length ? `<h2 class="h3" style="margin-top:34px">${ko ? '같은 작가의 다른 상품' : ja ? '同じ画家の他の商品' : 'More from this artist'}</h2><div class="pgrid">${sibs.map((x) => card(x, lang, L, esc)).join('')}</div>` : ''}</section>`;
  const jsonld = { '@context': 'https://schema.org', '@type': 'Product', name: it.en.name, image: 'https://arttripstudio.com' + pi(it.v || it.w[0].v || it.w[0].u), description: copy(it, 'en').body[0], offers: { '@type': 'Offer', price: it.p, priceCurrency: 'USD', availability: it.c ? 'https://schema.org/InStock' : 'https://schema.org/PreOrder' } };
  return html(layout(lang, { title: `${c.name} — ${t.site}`, desc: c.body[0].slice(0, 155), path: '/shop/c/' + it.s, body, img: pi(it.v || it.w[0].v || it.w[0].u), jsonld }));
}

// ---------- download page (PDF built in the browser) ----------
export async function pkDownload(lang, env, slug, h) {
  const { layout, html, esc, L, T } = h; const ko = lang === 'ko', ja = lang === 'ja', t = T[lang];
  const it = await pkItem(env, slug); if (!it) return pkRedir(env, slug, lang);
  const sizes = it.k === 'prints' ? ['A4', 'Letter', 'A3'] : it.k === 'pbn' ? ['A3', 'A2', 'A4', 'Letter'] : ['A4', 'Letter'];
  const body = `<section class="wrap sec narrow"><nav class="crumb"><a href="${L(lang, '/shop/c/' + it.s)}">${esc((it[lang] || it.en).name)}</a></nav><h1>${ko ? 'PDF 내려받기' : ja ? 'PDFをダウンロード' : 'Download your PDF'}</h1>
<p class="sub">${ko ? '결제 영수증 메일에 있는 라이선스 키를 넣어 주세요. 파일은 이 브라우저에서 바로 만들어져요(그림이 많으면 1~2분 걸려요).' : ja ? 'お支払い直後はキーなしでそのままダウンロードできます。あとで再ダウンロードするときは、領収書メールのライセンスキーを入力してください。ファイルはこのブラウザで作成されます（1〜2分かかることがあります）。' : 'Enter the licence key from your receipt email. The file is put together right here in your browser (large sets can take a minute or two).'}</p>
<div class="dl" style="text-align:left"><label class="small">${ko ? '라이선스 키' : ja ? 'ライセンスキー' : 'Licence key'}</label><input id="k" autocomplete="off" style="width:100%;padding:10px 12px;margin:6px 0 12px;border:1px solid #d9d1c3;border-radius:10px;font:inherit">
<label class="small">${ko ? '용지 크기' : ja ? '用紙サイズ' : 'Paper size'}</label><div class="row" id="sz" style="margin:6px 0 14px">${sizes.map((s, i) => `<label style="margin-right:14px"><input type="radio" name="sz" value="${s}"${i ? '' : ' checked'}> ${s}</label>`).join('')}</div>
${it.k === 'cal' || it.k === 'planner' ? `<label class="small">${ko ? '연도' : ja ? '年' : 'Year'}</label><div class="row" style="margin:6px 0 14px;flex-wrap:wrap">${[2027, 2028, 2029, 2030].map((y, i) => `<label style="margin-right:14px"><input type="radio" name="yr" value="${y}"${i ? '' : ' checked'}> ${y}</label>`).join('')}</div>` : ''}
<button class="pill" id="go">${ko ? 'PDF 만들기' : ja ? 'PDFを作成' : 'Make my PDF'}</button><p class="small" id="st" style="margin-top:12px"></p></div></section>
<script src="/editor/jspdf.umd.min.js"></script>${it.k === 'pbn' ? '<script src="/js/pbn.js?v=3"></script>' : ''}<script src="/js/pk.js?v=7"></script><script>PK.init(${JSON.stringify({ slug: it.s, lang, ko, ja })})</script>`;
  return html(layout(lang, { title: `${ko ? 'PDF 내려받기' : ja ? 'ダウンロード' : 'Download'} — ${t.site}`, desc: '', path: '/dl/' + it.s, body, noindex: true }));
}

// ---------- sitemap paths ----------
export async function pkPaths(env) { return (await pkIndex(env)).map((x) => '/shop/c/' + x.s).concat(['/shop/c']); }

// ---------- puzzle book cover (SVG) ----------
export async function pkCover(env, slug) {
  const it = await pkItem(env, slug); if (!it || it.k !== 'puz') return new Response('nf', { status: 404 });
  const z = it.pz, e = (x) => String(x).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const pal = { ws: ['#f3e6c8', '#8a3b2b'], scramble: ['#f6e2d6', '#9a4a2a'], sudoku: ['#dfe8f1', '#23466b'], numsearch: ['#e6e2f2', '#4a3b7a'], crypto: ['#efe9d8', '#5a4a22'], mix: ['#f1e4ec', '#7a2b55'], maze: ['#e3efd9', '#2f5d34'] }[z.type] || ['#eee', '#333'];
  let R = z.seed >>> 0; const rnd = () => ((R = (R * 1664525 + 1013904223) >>> 0) / 4294967296);
  let motif = '';
  if (z.type === 'ws' || z.type === 'scramble' || z.type === 'crypto' || z.type === 'mix') { const L = 'ABCDEFGHIJKLMNOPRSTUW'; for (let r = 0; r < 7; r++) for (let c = 0; c < 7; c++) motif += `<text x="${330 + c * 64}" y="${560 + r * 64}" font-size="44" font-family="Courier New,monospace" font-weight="700" fill="${pal[1]}" opacity=".85" text-anchor="middle">${L[Math.floor(rnd() * L.length)]}</text>`; }
  else if (z.type === 'sudoku' || z.type === 'numsearch') { for (let i = 0; i <= 9; i++) motif += `<line x1="280" y1="${500 + i * 50}" x2="730" y2="${500 + i * 50}" stroke="${pal[1]}" stroke-width="${i % 3 ? 2 : 6}"/><line x1="${280 + i * 50}" y1="500" x2="${280 + i * 50}" y2="950" stroke="${pal[1]}" stroke-width="${i % 3 ? 2 : 6}"/>`; for (let k = 0; k < 30; k++) motif += `<text x="${305 + Math.floor(rnd() * 9) * 50}" y="${538 + Math.floor(rnd() * 9) * 50}" font-size="34" font-family="Arial" font-weight="700" text-anchor="middle" fill="${pal[1]}">${1 + Math.floor(rnd() * 9)}</text>`; }
  else { for (let k = 0; k < 90; k++) { const x = 280 + Math.floor(rnd() * 9) * 50, y = 500 + Math.floor(rnd() * 9) * 50; motif += rnd() < .5 ? `<line x1="${x}" y1="${y}" x2="${x + 50}" y2="${y}" stroke="${pal[1]}" stroke-width="7" stroke-linecap="round"/>` : `<line x1="${x}" y1="${y}" x2="${x}" y2="${y + 50}" stroke="${pal[1]}" stroke-width="7" stroke-linecap="round"/>`; } motif += `<rect x="280" y="500" width="450" height="450" fill="none" stroke="${pal[1]}" stroke-width="8"/>`; }
  const t = e(it.en.name), lines = []; let cur = ''; for (const w of t.split(' ')) { if ((cur + ' ' + w).trim().length > 24) { lines.push(cur.trim()); cur = w; } else cur += ' ' + w; } lines.push(cur.trim());
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" width="1000" height="1200"><rect width="1000" height="1200" fill="${pal[0]}"/><rect x="40" y="40" width="920" height="1120" fill="none" stroke="${pal[1]}" stroke-width="4"/>
${lines.slice(0, 3).map((l, i) => `<text x="500" y="${160 + i * 78}" font-size="66" font-family="Georgia,serif" font-weight="700" text-anchor="middle" fill="${pal[1]}">${l}</text>`).join('')}
<text x="500" y="${180 + Math.min(3, lines.length) * 78}" font-size="34" font-family="Arial" text-anchor="middle" fill="#444">LARGE PRINT · ${z.n} PUZZLES · ANSWERS INCLUDED</text>${motif}
<text x="500" y="1110" font-size="30" font-family="Georgia,serif" text-anchor="middle" fill="#555">Arttrip Studio</text></svg>`;
  return new Response(svg, { headers: { 'content-type': 'image/svg+xml', 'cache-control': 'public, max-age=86400' } });
}
