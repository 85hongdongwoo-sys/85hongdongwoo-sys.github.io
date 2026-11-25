// Studio boot: language, artwork list, member status, save/load designs.
(function () {
  var app = document.getElementById('app'), lang = app.dataset.lang === 'ko' ? 'ko' : 'en', ko = lang === 'ko';
  var q = new URLSearchParams(location.search);
  var toast = function (m) { var t = document.querySelector('.toast'); if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); } t.textContent = m; t.classList.add('on'); clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('on'); }, 1800); };
  var me = null, designId = null;
  Promise.all([
    fetch('/api/art.json?art=' + (q.get('art') || '')).then(function (r) { return r.json(); }),
    fetch('/api/me').then(function (r) { return r.ok ? r.json() : { user: null }; }).catch(function () { return { user: null, off: true }; })
  ]).then(function (res) {
    var rows = res[0]; me = res[1].user; var membersOn = !res[1].off && res[1].user !== undefined;
    var A = {}; rows.forEach(function (r) { A[r.id] = { t: ko && r.tk ? r.tk : r.t, a: ko && r.ak ? r.ak : r.a, s: r.theme, w: r.w, h: r.h }; });
    window.MA = { A: A, ORDER: rows.map(function (r) { return r.id; }), lang: lang, st: { unlocked: !!(me && me.plan === 'member') }, toast: toast, svg: function (id) { return '<img src="/img/' + id + '.jpg" alt="" loading="lazy">'; } };
    function render() {
      var h = location.hash.match(/^#\/studio\/([a-z]+)(?:\?d=(\d+))?/);
      var go = function () { app.innerHTML = Studio.html(h ? h[1] : (q.get('tool') || 'wallcal'), q.get('art')); Studio.mount(); addSave(); };
      if (h && h[2] && me) { fetch('/api/designs/' + h[2]).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) { if (d) { Studio.load(d.state); designId = d.id; } go(); }); }
      else go();
    }
    function addSave() {
      var row = app.querySelector('.stage .row'); if (!row) return;
      var b = document.createElement('button'); b.className = 'pill ghost'; b.textContent = ko ? '저장' : 'Save';
      b.onclick = function () {
        if (!me) { if (confirm(ko ? '작업을 저장하려면 로그인이 필요해요. 로그인 화면으로 갈까요?' : 'Sign in to save your design. Go to sign in?')) location.href = (ko ? '/ko' : '') + '/account'; return; }
        var st = Studio.state(), title = (st.title || '') || (Studio.tools[st.tool].name + ' · ' + (window.MA.A[st.art] ? window.MA.A[st.art].t : ''));
        fetch('/api/designs', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ id: designId, tool: st.tool, title: title, state: st }) })
          .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
          .then(function (x) { if (x.ok) { designId = x.j.id; toast(ko ? '저장했어요 · 내 정보에서 다시 열 수 있어요' : 'Saved · find it on My page'); } else if (x.j.error === 'limit') toast(ko ? '무료 회원은 ' + x.j.limit + '개까지 저장할 수 있어요' : 'Free members can save ' + x.j.limit + ' designs'); else toast(ko ? '저장하지 못했어요' : 'Could not save'); });
      };
      if (membersOn !== false) row.appendChild(b);
    }
    window.addEventListener('hashchange', render); render();
  });
})();
