/* 홍라이프 도구 앱 설치(PWA): 서비스 워커 등록 + 상단 '앱 설치' 버튼(누르면 짧은 안내) */
(function () {
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', function () { navigator.serviceWorker.register('/hl-sw.js').catch(function () {}); });
  }
  if ((window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone) return;
  var ua = navigator.userAgent, deferred = null;
  var am = document.querySelector('meta[name="hl-app"]'), at = document.querySelector('meta[name="apple-mobile-web-app-title"]');
  var APP = am ? am.content.split('|') : null;
  var AN = APP ? APP[0] : (at && at.content !== '홍라이프' ? at.content : '홍라이프'), AI = APP ? APP[1] : '/assets/brand/icon-192.png';
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var android = /Android/.test(ua), kakao = /KAKAOTALK/i.test(ua), inapp = /NAVER\(|KAKAOTALK|Instagram|FBAN|FBAV|DaumApps|everytimeApp|Line\//i.test(ua);
  var iosSafari = ios && /Safari/.test(ua) && !/CriOS|FxiOS|EdgiOS|Whale/.test(ua) && !inapp;
  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); deferred = e; bar(); });
  window.addEventListener('appinstalled', function () { [].forEach.call(document.querySelectorAll('.hl-app,.hl-app2,#hl-ibar'), function (b) { b.remove(); }); try { localStorage.setItem('hl-ib:' + location.pathname, 'i'); } catch (e) {} });
  var CSS = '.brandbar nav a.hl-app{display:inline-flex!important;align-items:center;gap:6px;font-weight:700;color:#14286A;white-space:nowrap}'
    + '.hl-app img,.hl-app2 img{width:18px;height:18px;border-radius:5px;flex:none}'
    + '.brandbar .catbar a.hl-app2{display:none!important;align-items:center;gap:6px;background:#EEF2FF;color:#14286A;font-weight:800;position:sticky;left:0;z-index:2;box-shadow:6px 0 8px -2px rgba(255,255,255,.95),-12px 0 0 #fff}'
    + '@media(max-width:640px){.brandbar nav a.hl-app{display:none!important}.brandbar .catbar a.hl-app2{display:inline-flex!important}}'
    + '#hl-sheet{position:fixed;inset:0;z-index:9999;display:flex;align-items:flex-end;justify-content:center;background:rgba(0,0,0,.35)}'
    + '#hl-sheet .p{width:100%;max-width:420px;margin:0 8px 8px;background:#fff;border-radius:18px;padding:18px 18px 14px;box-shadow:0 8px 30px rgba(0,0,0,.2);text-align:center;font-size:15px;line-height:1.6;color:#191F28}'
    + '#hl-sheet img{width:52px;height:52px;border-radius:13px;display:block;margin:0 auto 8px}#hl-sheet b{display:block;font-size:17px;margin-bottom:4px}'
    + '#hl-sheet .r{display:flex;gap:8px;margin-top:14px}#hl-sheet button{flex:1;font:inherit;font-weight:800;border:0;border-radius:12px;min-height:46px;cursor:pointer;background:#14286A;color:#fff}'
    + '#hl-sheet button.x{background:#F1F3F5;color:#4E5968}#hl-sheet svg{vertical-align:-3px}'
    + '#hl-ibar{display:flex;align-items:center;gap:12px;margin:12px 0;padding:12px 14px;border-radius:16px;background:linear-gradient(135deg,#1D4ED8,#14286A);color:#fff;box-sizing:border-box;max-width:100%}'
    + '#hl-ibar img{width:44px;height:44px;border-radius:12px;flex:none;background:#fff}#hl-ibar .t{flex:1;min-width:0;line-height:1.4}'
    + '#hl-ibar .t b{display:block;font-size:15px;word-break:keep-all}#hl-ibar .t span{font-size:12.5px;opacity:.9}'
    + '#hl-ibar .go{flex:none;background:#fff;color:#1D4ED8;border:0;border-radius:10px;padding:9px 12px;font:inherit;font-weight:800;font-size:14px;cursor:pointer;white-space:nowrap}'
    + '#hl-ibar .x{flex:none;background:none;border:0;color:#fff;opacity:.75;font-size:18px;line-height:1;padding:4px;cursor:pointer}'
    + '#hl-ibar.ios{background:#fff;color:#191F28;border:1.5px dashed #1D4ED8}#hl-ibar.ios .x{color:#98A2B3}#hl-ibar.ios .t span{opacity:1;color:#4E5968}';
  var SH = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#3182F6" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M8 7l4-4 4 4"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>';
  function sheet(msg, label, fn) {
    var d = document.createElement('div'); d.id = 'hl-sheet'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-label', '앱 설치');
    d.innerHTML = '<div class="p"><img src="' + AI + '" alt=""><b></b><div class="m"></div><div class="r">' + (label ? '<button type="button" class="go"></button>' : '') + '<button type="button" class="x">닫기</button></div></div>';
    d.querySelector('.m').innerHTML = msg; d.querySelector('b').textContent = "'" + AN + "' 앱 설치";
    if (label) { var g = d.querySelector('.go'); g.textContent = label; g.onclick = fn; }
    d.querySelector('.x').onclick = function () { d.remove(); };
    d.onclick = function (e) { if (e.target === d) d.remove(); };
    document.body.appendChild(d);
  }
  function open(e) {
    e.preventDefault(); if (window.gtag) gtag('event', 'pwa_btn');
    if (deferred) { deferred.prompt(); deferred.userChoice.then(function (c) { if (window.gtag) gtag('event', 'pwa_install', { outcome: c.outcome }); }); return; }
    if (kakao) return sheet('카톡에선 설치가 안 돼요.', '브라우저로 열기', function () { location.href = 'kakaotalk://web/openExternal?url=' + encodeURIComponent(location.href); });
    if (inapp && android) return sheet('이 앱에선 설치가 안 돼요.', '크롬으로 열기', function () { location.href = 'intent://' + location.host + location.pathname + location.search + '#Intent;scheme=https;package=com.android.chrome;end'; });
    if (inapp) return sheet('⋯ 메뉴 → Safari로 열기 후 설치하세요.');
    if (iosSafari) return sheet('공유 ' + SH + ' → <b style="display:inline;font-size:inherit">홈 화면에 추가</b>');
    if (ios) return sheet('Safari로 열고 공유 ' + SH + ' → 홈 화면에 추가');
    if (android) return sheet('크롬 메뉴 ⋮ → <b style="display:inline;font-size:inherit">앱 설치</b>');
    sheet('주소창 오른쪽 설치 아이콘을 누르세요.');
  }
  var mob = ios || android;
  function bar() {
    if (!APP || !mob || document.getElementById('hl-ibar')) return;
    try { if (localStorage.getItem('hl-ib:' + location.pathname)) return; } catch (e) {}
    var cls = '', txt, btn = '';
    if (deferred) { txt = '홈 화면에서 바로 이 도구가 열려요'; btn = '<button type="button" class="go">설치</button>'; }
    else if (iosSafari) { cls = 'ios'; txt = '공유 ' + SH + ' → 홈 화면에 추가를 누르면 바로 이 도구가 열려요'; }
    else return;
    var top = document.querySelector('main header, main .top, main h1'); if (!top) return;
    if (top.tagName === 'H1') top = top.parentNode;
    if (!document.getElementById('hl-app-css')) { var st = document.createElement('style'); st.id = 'hl-app-css'; st.textContent = CSS; document.head.appendChild(st); }
    var d = document.createElement('div'); d.id = 'hl-ibar'; d.className = cls;
    d.innerHTML = '<img src="' + AI + '" alt=""><div class="t"><b></b><span>' + txt + '</span></div>' + btn + '<button type="button" class="x" aria-label="닫기">✕</button>';
    d.querySelector('b').textContent = (cls ? "홈 화면에 '" : "'") + AN + (cls ? "' 추가하기" : "' 앱으로 설치");
    var g = d.querySelector('.go'); if (g) g.onclick = open;
    d.querySelector('.x').onclick = function () { d.remove(); try { localStorage.setItem('hl-ib:' + location.pathname, 'x'); } catch (e) {} if (window.gtag) gtag('event', 'pwa_bar_close'); };
    top.parentNode.insertBefore(d, top.nextSibling);
    if (window.gtag) gtag('event', 'pwa_bar_show', { app: AN });
  }
  function add() {
    var nav = document.querySelector('.brandbar nav'); if (!nav || nav.querySelector('.hl-app')) return;
    if (!document.getElementById('hl-app-css')) { var s = document.createElement('style'); s.id = 'hl-app-css'; s.textContent = CSS; document.head.appendChild(s); }
    var L = '<img src="' + AI + '" alt="">앱으로 다운로드';
    var a = document.createElement('a'); a.className = 'lang hl-app'; a.href = '#app'; a.innerHTML = L; a.onclick = open;
    var srch = nav.querySelector('.srch'); if (srch && srch.nextSibling) nav.insertBefore(a, srch.nextSibling); else nav.appendChild(a);
    var cb = document.querySelector('.catbar .in2');
    if (cb) { var b = document.createElement('a'); b.className = 'hl-app2'; b.href = '#app'; b.innerHTML = L; b.onclick = open; cb.insertBefore(b, cb.firstChild); }
  }
  function init() { add(); if (iosSafari) bar(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
