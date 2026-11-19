/* 홍라이프 도구 앱 설치용 서비스 워커 — 캐시하지 않고 항상 네트워크로 (오프라인 기능 없음) */
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function (e) {
  if (e.request.mode !== 'navigate') return;
  e.respondWith(fetch(e.request).catch(function () {
    return new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>홍라이프 도구</title><body style="font-family:system-ui;padding:40px 20px;text-align:center;color:#191F28"><h1 style="font-size:20px">인터넷 연결이 없어요</h1><p style="color:#4E5968">연결되면 다시 열어 주세요.</p><button onclick="location.reload()" style="font:inherit;padding:12px 20px;border:0;border-radius:12px;background:#14286A;color:#fff">다시 시도</button></body>', { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
  }));
});
