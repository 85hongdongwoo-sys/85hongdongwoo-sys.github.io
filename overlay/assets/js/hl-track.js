/* 홍라이프 도구 사용 측정 (GA4 이벤트) — 개인정보·파일 내용은 보내지 않아요.
   tool_use(도구 처음 사용) · (결과 저장은 hl.js가 보내는 file_download) · official_link(공식 기관 링크) · search(사이트 검색어)
   related_click(관련 도구 이동) · app_install(앱 설치 완료) */
(function () {
  try { if (localStorage.getItem('hl-notrack') === '1') return; } catch (e) {}
  var P = location.pathname, used = false;
  function ev(n, o) { try { if (window.gtag) gtag('event', n, Object.assign({ page_path: P }, o || {})); } catch (e) {} }
  function inTool(el) { return el && el.closest && el.closest('#tool, .tool, .hk-tool, [data-tool]'); }

  /* 도구 처음 사용: 도구 칸 안의 버튼·파일 선택·입력 */
  function use(how) { if (used) return; used = true; ev('tool_use', { how: how }); }
  document.addEventListener('click', function (e) {
    var t = e.target;
    var b = t.closest && t.closest('button, [role=button], input[type=submit], input[type=button], label');
    if (b && inTool(b)) use('click');
    var a = t.closest && t.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (a.hasAttribute('download') || /^blob:|^data:/.test(h)) return;
    if (/^https?:\/\//i.test(h) && a.hostname && a.hostname.indexOf('honglife') < 0) {
      ev('official_link', { link_domain: a.hostname.replace(/^www\./, '') });
      return;
    }
    if (a.closest('.rel, .tlist, .hl-grid, #exam-list, .lk')) ev('related_click', { to: a.pathname || h });
  }, true);
  document.addEventListener('change', function (e) {
    var t = e.target;
    if (inTool(t)) use(t.type === 'file' ? 'file' : 'input');
  }, true);
  document.addEventListener('drop', function (e) { if (inTool(e.target)) use('drop'); }, true);

  /* 사이트 검색어 (첫 화면 검색칸) */
  var q = document.getElementById('q'), last = '';
  if (q) {
    var send = function () { var v = (q.value || '').trim(); if (v.length >= 2 && v !== last) { last = v; ev('search', { search_term: v.slice(0, 40) }); } };
    q.addEventListener('keydown', function (e) { if (e.key === 'Enter') send(); });
    q.addEventListener('blur', send);
  }

  /* 앱 설치 완료 */
  window.addEventListener('appinstalled', function () { ev('app_install'); });
})();
