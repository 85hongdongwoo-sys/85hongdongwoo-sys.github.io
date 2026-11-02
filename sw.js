/* Hong Life service worker. Bump VERSION to drop old caches. */
const VERSION = 'hl-v1';
const PAGES = VERSION + '-pages';
const STATIC = VERSION + '-static';
const PRECACHE = ['/offline.html', '/assets/app.js', '/assets/icons/icon-192.png', '/manifest.webmanifest'];
const CDN = /^https:\/\/(cdn\.jsdelivr\.net|fonts\.googleapis\.com|fonts\.gstatic\.com)\//;
const MAX_PAGES = 40;

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(STATIC).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => !k.startsWith(VERSION + '-')).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

async function trim(name, max) {
  const c = await caches.open(name);
  const keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);
}

async function networkFirst(req) {
  const c = await caches.open(PAGES);
  try {
    const res = await fetch(req);
    if (res && res.ok && res.type === 'basic') {
      c.put(req, res.clone()).then(() => trim(PAGES, MAX_PAGES));
    }
    return res;
  } catch (err) {
    const hit = await c.match(req, { ignoreSearch: false }) || await c.match(req, { ignoreSearch: true });
    return hit || (await caches.match('/offline.html')) || Response.error();
  }
}

/* same-origin js/css: serve cache, refresh in background (files are not fingerprinted) */
async function staleWhileRevalidate(req, ev) {
  const c = await caches.open(STATIC);
  const hit = await c.match(req);
  const net = fetch(req).then((res) => {
    if (res && res.ok) c.put(req, res.clone());
    return res;
  }).catch(() => hit);
  if (hit) { ev.waitUntil(net); return hit; }
  return net;
}

async function cacheFirst(req) {
  const c = await caches.open(STATIC);
  const hit = await c.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res && (res.ok || res.type === 'opaque')) c.put(req, res.clone());
  return res;
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const same = url.origin === self.location.origin;
  if (same) {
    if (url.pathname === '/sw.js') return;
    if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
      e.respondWith(networkFirst(req));
      return;
    }
    if (/\.(?:js|css|json|webmanifest)$/.test(url.pathname)) { e.respondWith(staleWhileRevalidate(req, e)); return; }
    if (/\.(?:png|jpe?g|gif|webp|svg|ico|woff2?)$/.test(url.pathname)) { e.respondWith(cacheFirst(req)); return; }
    return;
  }
  /* Only versioned font/CSS files from these CDNs. Everything else (AdSense, gtag, analytics, models) is not touched. */
  if (CDN.test(req.url) && /\.(?:css|woff2?|ttf)$|\/css2?\?/.test(url.pathname + url.search)) {
    e.respondWith(cacheFirst(req));
  }
});
