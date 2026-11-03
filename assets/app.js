/* Hong Life — app.js (PWA register, add-to-home chip, embed code dialog, embed mode). No deps. */
!function(){"use strict";
if(window.__hlApp)return;window.__hlApp=1;
var d=document,w=window,H=d.documentElement,
lang=(H.getAttribute("lang")||"en").toLowerCase(),L2=lang.slice(0,2),
rtl=(H.getAttribute("dir")||"").toLowerCase()==="rtl",
embed=/[?&]embed=1(&|$)/.test(location.search);
var T={
ko:{a2hs:"홈 화면에 추가",ios:"Safari 아래 공유 버튼(□↑)을 누른 뒤 ‘홈 화면에 추가’를 선택하세요.",close:"닫기",emb:"내 블로그에 넣기",embT:"이 계산기를 블로그·카페에 넣기",embD:"아래 코드를 블로그 글의 HTML 편집 화면에 붙여 넣으세요. 광고 없이 계산기만 보여요.",h:"높이",copy:"코드 복사",copied:"복사했어요",view:"홍라이프 계산기에서 보기 ↗"},
en:{a2hs:"Add to Home Screen",ios:"Tap the Share button (□↑) in Safari, then choose “Add to Home Screen”.",close:"Close",emb:"Embed on your site",embT:"Embed this calculator",embD:"Paste this code into the HTML view of your blog or website. The embedded calculator shows no ads.",h:"Height",copy:"Copy code",copied:"Copied",view:"Open on Hong Life ↗"},
es:{a2hs:"Añadir a inicio",ios:"Toca Compartir (□↑) en Safari y elige «Añadir a pantalla de inicio».",close:"Cerrar",emb:"Insertar en tu web",embT:"Inserta esta calculadora",embD:"Pega este código en la vista HTML de tu blog o web. La calculadora insertada no muestra anuncios.",h:"Altura",copy:"Copiar código",copied:"Copiado",view:"Abrir en Hong Life ↗"},
pt:{a2hs:"Adicionar à tela inicial",ios:"Toque em Compartilhar (□↑) no Safari e escolha “Adicionar à Tela de Início”.",close:"Fechar",emb:"Incorporar no seu site",embT:"Incorpore esta calculadora",embD:"Cole este código na visualização HTML do seu blog ou site. A calculadora incorporada não exibe anúncios.",h:"Altura",copy:"Copiar código",copied:"Copiado",view:"Abrir no Hong Life ↗"},
fr:{a2hs:"Ajouter à l’écran d’accueil",ios:"Touchez Partager (□↑) dans Safari puis « Sur l’écran d’accueil ».",close:"Fermer",emb:"Intégrer à votre site",embT:"Intégrer ce calculateur",embD:"Collez ce code dans la vue HTML de votre blog ou site. Le calculateur intégré n’affiche pas de publicité.",h:"Hauteur",copy:"Copier le code",copied:"Copié",view:"Ouvrir sur Hong Life ↗"},
de:{a2hs:"Zum Startbildschirm",ios:"Tippen Sie in Safari auf Teilen (□↑) und dann auf „Zum Home-Bildschirm“.",close:"Schließen",emb:"Auf Ihrer Website einbinden",embT:"Diesen Rechner einbinden",embD:"Fügen Sie diesen Code in die HTML-Ansicht Ihres Blogs oder Ihrer Website ein. Der eingebundene Rechner zeigt keine Werbung.",h:"Höhe",copy:"Code kopieren",copied:"Kopiert",view:"Auf Hong Life öffnen ↗"},
id:{a2hs:"Tambah ke layar utama",ios:"Ketuk Bagikan (□↑) di Safari, lalu pilih “Tambah ke Layar Utama”.",close:"Tutup",emb:"Pasang di blog",embT:"Pasang kalkulator ini",embD:"Tempel kode ini di tampilan HTML blog atau situs Anda. Kalkulator yang dipasang tidak menampilkan iklan.",h:"Tinggi",copy:"Salin kode",copied:"Disalin",view:"Buka di Hong Life ↗"},
ja:{a2hs:"ホーム画面に追加",ios:"Safariの共有ボタン（□↑）から「ホーム画面に追加」を選んでください。",close:"閉じる",emb:"ブログに埋め込む",embT:"この計算ツールを埋め込む",embD:"このコードをブログやサイトのHTML編集画面に貼り付けてください。埋め込み表示では広告は出ません。",h:"高さ",copy:"コードをコピー",copied:"コピーしました",view:"Hong Lifeで開く ↗"},
zh:{a2hs:"添加到主屏幕",ios:"在 Safari 中点按分享按钮（□↑），然后选择“添加到主屏幕”。",close:"关闭",emb:"嵌入到网站",embT:"嵌入此计算器",embD:"将此代码粘贴到博客或网站的 HTML 编辑模式中。嵌入的计算器不显示广告。",h:"高度",copy:"复制代码",copied:"已复制",view:"在 Hong Life 打开 ↗"},
ru:{a2hs:"На главный экран",ios:"Нажмите «Поделиться» (□↑) в Safari и выберите «На экран „Домой“».",close:"Закрыть",emb:"Встроить на сайт",embT:"Встроить этот калькулятор",embD:"Вставьте этот код в HTML-режим вашего блога или сайта. Во встроенном калькуляторе нет рекламы.",h:"Высота",copy:"Копировать код",copied:"Скопировано",view:"Открыть на Hong Life ↗"},
hi:{a2hs:"होम स्क्रीन पर जोड़ें",ios:"Safari में शेयर (□↑) दबाएँ, फिर “Add to Home Screen” चुनें।",close:"बंद करें",emb:"अपनी साइट पर लगाएँ",embT:"यह कैलकुलेटर एम्बेड करें",embD:"यह कोड अपने ब्लॉग या वेबसाइट के HTML व्यू में पेस्ट करें। एम्बेड किए गए कैलकुलेटर में विज्ञापन नहीं दिखते।",h:"ऊँचाई",copy:"कोड कॉपी करें",copied:"कॉपी हो गया",view:"Hong Life पर खोलें ↗"},
ar:{a2hs:"أضف إلى الشاشة الرئيسية",ios:"اضغط زر المشاركة (□↑) في Safari ثم اختر «إضافة إلى الشاشة الرئيسية».",close:"إغلاق",emb:"تضمين في موقعك",embT:"تضمين هذه الحاسبة",embD:"الصق هذا الرمز في وضع HTML في مدونتك أو موقعك. الحاسبة المضمّنة لا تعرض إعلانات.",h:"الارتفاع",copy:"نسخ الرمز",copied:"تم النسخ",view:"افتح في Hong Life ↗"},
th:{a2hs:"เพิ่มไปยังหน้าจอโฮม",ios:"แตะปุ่มแชร์ (□↑) ใน Safari แล้วเลือก “เพิ่มไปยังหน้าจอโฮม”",close:"ปิด",emb:"ฝังในเว็บไซต์",embT:"ฝังเครื่องมือนี้",embD:"วางโค้ดนี้ในโหมด HTML ของบล็อกหรือเว็บไซต์ เครื่องมือที่ฝังไว้จะไม่แสดงโฆษณา",h:"ความสูง",copy:"คัดลอกโค้ด",copied:"คัดลอกแล้ว",view:"เปิดใน Hong Life ↗"},
vi:{a2hs:"Thêm vào màn hình chính",ios:"Nhấn nút Chia sẻ (□↑) trong Safari rồi chọn “Thêm vào MH chính”.",close:"Đóng",emb:"Nhúng vào trang của bạn",embT:"Nhúng công cụ này",embD:"Dán mã này vào chế độ HTML của blog hoặc website. Công cụ được nhúng không hiển thị quảng cáo.",h:"Chiều cao",copy:"Sao chép mã",copied:"Đã sao chép",view:"Mở trên Hong Life ↗"}};
var S=T[L2]||T.en;
function ls(k,v){try{if(v===undefined)return w.localStorage.getItem(k);w.localStorage.setItem(k,v)}catch(e){return null}}
function ev(n,p){try{typeof w.gtag==="function"&&w.gtag("event",n,p||{})}catch(e){}}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function canon(){var c=d.querySelector('link[rel="canonical"]'),u=c&&c.href||("https://honglife.co.kr"+location.pathname);return u.split("#")[0].split("?")[0]}
function el(tag,cls,html){var e=d.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e}
var css=".hl-chip{all:unset;box-sizing:border-box;position:fixed;left:14px;bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:899;display:flex;align-items:center;gap:6px;max-width:calc(100% - 90px);padding:0 4px 0 12px;height:40px;border-radius:20px;background:#fff;color:#12305C;font-weight:700;font-size:13.5px;line-height:1.2;font-family:inherit;box-shadow:0 4px 16px rgba(11,31,63,.28),inset 0 0 0 1.5px #B8862B;opacity:0;transform:translateY(8px);transition:opacity .25s,transform .25s}html[dir=rtl] .hl-chip{left:auto;right:14px;padding:0 12px 0 4px}.hl-chip.hl-on{opacity:1;transform:none}.hl-chip button{all:unset;box-sizing:border-box;cursor:pointer;display:flex;align-items:center;gap:6px;min-height:40px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;-webkit-tap-highlight-color:transparent}.hl-chip button:focus-visible{outline:2px solid #B8862B;outline-offset:2px;border-radius:8px}.hl-chip .hl-x{width:32px;justify-content:center;color:#5B6B82;font-size:18px;flex:none}.hl-chip svg{flex:none;color:#B8862B}.hl-chip-tip{position:fixed;left:14px;right:14px;bottom:calc(132px + env(safe-area-inset-bottom,0px));z-index:899;background:#0B1F3F;color:#fff;border:1px solid #B8862B;border-radius:12px;padding:11px 14px;font-size:13.5px;line-height:1.5;box-shadow:0 6px 24px rgba(0,0,0,.25)}"
+".hl-embed-row{margin:12px 0 0;display:flex;justify-content:flex-start}.hl-embed-btn{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:7px;min-height:38px;padding:7px 12px;border-radius:10px;background:#F6F1E6;color:#12305C;font:inherit;font-size:13.5px;font-weight:700;box-shadow:inset 0 0 0 1px #E2CFA4;max-width:100%}.hl-embed-btn:hover{background:#EFE5CF}.hl-embed-btn:focus-visible{outline:3px solid #B8862B;outline-offset:2px}.hl-embed-btn svg{color:#B8862B;flex:none}.hl-embed-row--solo{width:min(1080px,calc(100% - 32px));margin:16px auto}"
+".hl-dlg{position:fixed;inset:0;z-index:2147483001;background:rgba(5,14,30,.62);display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box}.hl-dlg *{box-sizing:border-box}.hl-dlg-box{width:100%;max-width:560px;max-height:calc(100vh - 32px);overflow:auto;background:#fff;color:#2F343B;border-radius:16px;border-top:4px solid #B8862B;padding:20px 18px 18px;font-family:inherit;text-align:start;box-shadow:0 20px 60px rgba(0,0,0,.35)}.hl-dlg h2{margin:0 0 6px;font-size:18px;color:#12305C;line-height:1.35}.hl-dlg p{margin:0 0 12px;font-size:14px;line-height:1.55;color:#4A5568}.hl-dlg textarea{display:block;width:100%;height:118px;resize:vertical;font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:#12305C;background:#F5F7FA;border:1px solid #D5DCE6;border-radius:10px;padding:10px;direction:ltr;text-align:left}.hl-dlg-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;margin-top:12px}.hl-dlg label{font-size:13.5px;color:#4A5568;display:flex;align-items:center;gap:6px}.hl-dlg select{font:inherit;font-size:14px;padding:6px 8px;border:1px solid #D5DCE6;border-radius:8px;background:#fff;color:#12305C}.hl-dlg .hl-b{all:unset;box-sizing:border-box;cursor:pointer;min-height:40px;padding:8px 14px;border-radius:10px;font:inherit;font-size:14px;font-weight:700;text-align:center}.hl-dlg .hl-b1{background:#12305C;color:#fff}.hl-dlg .hl-b1:hover{background:#1B427A}.hl-dlg .hl-b2{background:#fff;color:#12305C;box-shadow:inset 0 0 0 1.5px #12305C}.hl-dlg .hl-b:focus-visible{outline:3px solid #B8862B;outline-offset:2px}.hl-dlg-btns{display:flex;gap:8px;margin-inline-start:auto}"
+"html.hl-embed .hl-embed-bar{display:flex}.hl-embed-bar{display:none;justify-content:center;margin:14px auto 18px;padding:0 16px}.hl-embed-bar a{display:inline-flex;align-items:center;min-height:36px;padding:7px 14px;border-radius:999px;background:#12305C;color:#fff!important;font-size:13.5px;font-weight:700;text-decoration:none;box-shadow:inset 0 0 0 1.5px #B8862B}";
function addCss(){if(d.getElementById("hl-app-css"))return;var s=el("style");s.id="hl-app-css";s.textContent=css;d.head.appendChild(s)}
var IC_EMB='<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M8.6 16.6 4 12l4.6-4.6L7.2 6 1.2 12l6 6zm6.8 0L20 12l-4.6-4.6L16.8 6l6 6-6 6z"/></svg>',
IC_ADD='<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M7 2h10a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm0 3v13h10V5zm4 2h2v3h3v2h-3v3h-2v-3H8v-3h3z"/></svg>';

/* ---------- embed mode ---------- */
function embedMode(){
  H.classList.add("hl-embed");
  try{(w.adsbygoogle=w.adsbygoogle||[]).pauseAdRequests=1}catch(e){}
  var bar=el("div","hl-embed-bar",'<a target="_blank" rel="noopener" href="'+esc(canon())+'">'+esc(S.view)+"</a>");
  d.body.appendChild(bar);
  // links leave the iframe
  [].forEach.call(d.querySelectorAll("a[href]"),function(a){var h=a.getAttribute("href")||"";if(h.charAt(0)==="#"||/^(javascript|mailto|tel):/i.test(h))return;a.target="_blank";if(!/noopener/.test(a.rel))a.rel=(a.rel+" noopener").trim()});
  // report height to parent (optional auto-resize hosts)
  function post(){try{w.parent!==w&&w.parent.postMessage({hlEmbed:1,height:Math.ceil(d.documentElement.scrollHeight)},"*")}catch(e){}}
  post();w.addEventListener("load",post);if("ResizeObserver"in w)new ResizeObserver(post).observe(d.body);
}

/* ---------- embed dialog ---------- */
var lastFocus;
function openDlg(){
  var url=canon(),title=(d.querySelector("h1")||{}).textContent||d.title;title=String(title).replace(/\s+/g," ").trim();
  var code=function(h){return '<iframe src="'+url+'?embed=1" width="100%" height="'+h+'" style="border:0;max-width:760px;width:100%" loading="lazy" title="'+esc(title)+'"></iframe>'};
  lastFocus=d.activeElement;
  var o=el("div","hl-dlg");o.setAttribute("role","dialog");o.setAttribute("aria-modal","true");o.setAttribute("aria-labelledby","hl-dlg-t");
  o.innerHTML='<div class="hl-dlg-box"><h2 id="hl-dlg-t">'+esc(S.embT)+"</h2><p>"+esc(S.embD)+'</p><textarea readonly spellcheck="false" aria-label="iframe"></textarea><div class="hl-dlg-row"><label>'+esc(S.h)+' <select><option>600</option><option selected>800</option><option>1000</option><option>1400</option></select></label><div class="hl-dlg-btns"><button type="button" class="hl-b hl-b2" data-x>'+esc(S.close)+'</button><button type="button" class="hl-b hl-b1" data-c>'+esc(S.copy)+"</button></div></div></div>";
  var ta=o.querySelector("textarea"),sel=o.querySelector("select"),cb=o.querySelector("[data-c]");
  ta.value=code(sel.value);sel.onchange=function(){ta.value=code(sel.value)};
  function close(){o.remove();d.removeEventListener("keydown",key,!0);try{lastFocus&&lastFocus.focus()}catch(e){}}
  function key(e){if(e.key==="Escape"){e.preventDefault();close()}else if(e.key==="Tab"){var f=o.querySelectorAll("textarea,select,button"),a=f[0],b=f[f.length-1];if(e.shiftKey&&d.activeElement===a){e.preventDefault();b.focus()}else if(!e.shiftKey&&d.activeElement===b){e.preventDefault();a.focus()}}}
  o.addEventListener("click",function(e){if(e.target===o||e.target.hasAttribute("data-x"))close()});
  cb.onclick=function(){var v=ta.value,ok=function(){cb.textContent=S.copied;setTimeout(function(){cb.textContent=S.copy},1800)};
    if(navigator.clipboard&&w.isSecureContext)navigator.clipboard.writeText(v).then(ok,function(){ta.select();try{d.execCommand("copy");ok()}catch(e){}});else{ta.focus();ta.select();try{d.execCommand("copy");ok()}catch(e){}}
    ev("embed_copy",{page_path:location.pathname})};
  d.addEventListener("keydown",key,!0);d.body.appendChild(o);ta.focus();ta.select();ev("embed_open",{page_path:location.pathname});
}
function isCalc(){var j=d.querySelectorAll('script[type="application/ld+json"]');for(var i=0;i<j.length;i++)if(/"WebApplication"/.test(j[i].textContent))return!0;return!1}
function addEmbedBtn(){
  if(!isCalc()||d.querySelector(".hl-embed-btn"))return;
  var row=el("div","hl-embed-row",'<button type="button" class="hl-embed-btn">'+IC_EMB+"<span>"+esc(S.emb)+"</span></button>");
  row.firstChild.addEventListener("click",openDlg);
  var sh=d.getElementById("hl-share");
  if(sh)sh.appendChild(row);
  else{var ref=d.querySelector(".hl-rel")||d.querySelector("nav.calc-index")||d.querySelector("footer");if(ref&&ref.parentNode)ref.parentNode.insertBefore(row,ref);else d.body.appendChild(row);if(row.parentNode===d.body)row.classList.add("hl-embed-row--solo")}
}

/* ---------- service worker + install chip ---------- */
function sw(){if(!("serviceWorker"in navigator)||!(w.isSecureContext||location.hostname==="localhost"))return;
  w.addEventListener("load",function(){navigator.serviceWorker.register("/sw.js").catch(function(){})})}
function chip(){
  var standalone=(w.matchMedia&&w.matchMedia("(display-mode: standalone)").matches)||navigator.standalone;
  if(standalone||ls("hl-a2hs-off"))return;
  var mobile=w.matchMedia&&w.matchMedia("(pointer:coarse)").matches&&w.innerWidth<=820;if(!mobile)return;
  var ua=navigator.userAgent||"",ios=/iPhone|iPad|iPod/.test(ua)&&/Safari/.test(ua)&&!/CriOS|FxiOS|EdgiOS|FBAN|FBAV|Instagram|KAKAOTALK|NAVER|Line\//.test(ua),deferred=null,c,tip;
  function show(){if(c||ls("hl-a2hs-off"))return;
    c=el("div","hl-chip",'<button type="button" class="hl-go">'+IC_ADD+"<span>"+esc(S.a2hs)+'</span></button><button type="button" class="hl-x" aria-label="'+esc(S.close)+'">×</button>');
    d.body.appendChild(c);setTimeout(function(){c.classList.add("hl-on")},30);
    c.querySelector(".hl-x").onclick=function(){ls("hl-a2hs-off",String(Date.now()));c.remove();tip&&tip.remove();ev("a2hs_dismiss")};
    c.querySelector(".hl-go").onclick=function(){ev("a2hs_click");
      if(deferred){deferred.prompt();(deferred.userChoice||Promise.resolve({})).then(function(r){if(r&&r.outcome==="accepted"){ls("hl-a2hs-off","installed");c.remove()}});deferred=null}
      else if(ios){if(tip){tip.remove();tip=null;return}tip=el("div","hl-chip-tip");tip.setAttribute("role","status");tip.textContent=S.ios;d.body.appendChild(tip);setTimeout(function(){tip&&tip.remove();tip=null},9000)}};
  }
  function later(){var shown=!1,go=function(){if(shown)return;shown=!0;w.removeEventListener("scroll",sc);show()},sc=function(){if(w.scrollY>400)go()};w.addEventListener("scroll",sc,{passive:!0});setTimeout(go,25000)}
  w.addEventListener("beforeinstallprompt",function(e){e.preventDefault();deferred=e;later()});
  w.addEventListener("appinstalled",function(){ls("hl-a2hs-off","installed");c&&c.remove()});
  if(ios)later();
}

/* ---------- remember inputs + recently used calculators ---------- */
var RT={ko:{rec:"최근 쓴 계산기",rest:"지난번 입력값을 불러왔어요",clr:"지우기"},ja:{rec:"最近使った計算ツール",rest:"前回の入力値を復元しました",clr:"消去"},de:{rec:"Zuletzt genutzt",rest:"Ihre letzten Eingaben wurden geladen",clr:"Löschen"},es:{rec:"Usadas recientemente",rest:"Hemos cargado tus últimos datos",clr:"Borrar"},fr:{rec:"Utilisés récemment",rest:"Vos dernières saisies ont été chargées",clr:"Effacer"},pt:{rec:"Usadas recentemente",rest:"Carregamos seus últimos dados",clr:"Limpar"},it:{rec:"Usati di recente",rest:"Abbiamo caricato i tuoi ultimi dati",clr:"Cancella"},nl:{rec:"Recent gebruikt",rest:"Je laatste invoer is geladen",clr:"Wissen"},pl:{rec:"Ostatnio używane",rest:"Wczytaliśmy Twoje ostatnie dane",clr:"Wyczyść"},id:{rec:"Terakhir dipakai",rest:"Input terakhir Anda dimuat",clr:"Hapus"},en:{rec:"Recently used",rest:"Your last inputs were restored",clr:"Clear"}};
var R=RT[L2]||RT.en;
var NOSAVE=/^\/(budget|shorts|games)\/|iq-test|personality|mbti-test|clock|stopwatch|char-count|word-counter|countdown|suneung/;
function fields(){var out=[],q=d.querySelectorAll("input[id],select[id]");for(var i=0;i<q.length;i++){var f=q[i],ty=(f.getAttribute("type")||"text").toLowerCase();
  if(f.closest("[data-hl-nosave]")||f.closest(".hl-dlg")||f.disabled)continue;
  if(f.tagName==="SELECT"||/^(text|number|range|date|month|tel|checkbox)$/.test(ty))out.push(f)}return out}
function memo(){
  if(!isCalc()||NOSAVE.test(location.pathname))return;
  var key="hl-in:"+location.pathname,fs=fields();if(!fs.length)return;
  var save=function(){var o={};fs.forEach(function(f){o[f.id]=f.type==="checkbox"?(f.checked?1:0):f.value});ls(key,JSON.stringify(o))};
  var raw=!location.search&&ls(key),n=0;
  if(raw){try{var o=JSON.parse(raw);fs.forEach(function(f){if(!(f.id in o))return;var v=o[f.id];
      if(f.type==="checkbox"){if(f.checked!==!!v){f.checked=!!v;n++}}
      else if(f.tagName==="SELECT"){if(f.value!==v&&[].some.call(f.options,function(op){return op.value===v})){f.value=v;n++}}
      else if(f.value!==v){f.value=v;n++}});
    if(n){var fire=function(f){f.dispatchEvent(new Event("input",{bubbles:!0}));f.dispatchEvent(new Event("change",{bubbles:!0}))},txt=fs.filter(function(f){return f.tagName!=="SELECT"&&f.type!=="checkbox"});fs.filter(function(f){return txt.indexOf(f)<0}).forEach(fire);txt.forEach(function(f){if(f.id in o)f.value=o[f.id];fire(f)});
      var t=el("div","hl-rest",'<span>'+esc(R.rest)+'</span><button type="button">'+esc(R.clr)+'</button>');t.setAttribute("role","status");
      t.querySelector("button").onclick=function(){try{w.localStorage.removeItem(key)}catch(e){}ev("inputs_clear");location.reload()};
      d.body.appendChild(t);setTimeout(function(){t.classList.add("hl-rest--out");setTimeout(function(){t.remove()},400)},7000);ev("inputs_restored",{n:n})}
  }catch(e){}}
  var tm;d.addEventListener("input",function(){clearTimeout(tm);tm=setTimeout(save,400)},!0);d.addEventListener("change",function(){clearTimeout(tm);tm=setTimeout(save,400)},!0);
}
function recent(){
  var path=location.pathname,list=[];try{list=JSON.parse(ls("hl-recent")||"[]")}catch(e){}
  if(isCalc()&&!NOSAVE.test(path)){var ti=(d.title||"").split(/ [|·—–-] /)[0].trim().slice(0,40);
    list=list.filter(function(x){return x.u!==path});list.unshift({u:path,t:ti});list=list.slice(0,8);ls("hl-recent",JSON.stringify(list))}
  var show=list.filter(function(x){return x.u!==path}).slice(0,6);if(!show.length)return;
  var ref=d.querySelector("nav.calc-index");if(!ref&&/\/$/.test(path))ref=d.querySelector("footer");if(!ref||!ref.parentNode)return;
  var box=el("nav","hl-recent");box.setAttribute("aria-label",R.rec);
  box.innerHTML="<b>"+esc(R.rec)+"</b><div>"+show.map(function(x){return'<a href="'+esc(x.u)+'">'+esc(x.t)+"</a>"}).join("")+"</div>";
  ref.parentNode.insertBefore(box,ref)}
function qaLink(){var n=d.querySelector("nav.calc-index .ci-grid")||d.querySelector("nav.calc-index");if(!n||n.querySelector('a[href^="/qa/"]'))return;
  var m={ko:["국가별 Q&A · 질문하기","/qa/"],ja:["税金・給与 Q&A","/qa/jp.html"],de:["Fragen & Antworten","/qa/de.html"],es:["Preguntas y respuestas","/qa/es.html"],fr:["Questions-réponses","/qa/fr.html"],pt:["Perguntas e respostas","/qa/br.html"],it:["Domande e risposte","/qa/it.html"],nl:["Vragen en antwoorden","/qa/nl.html"],pl:["Pytania i odpowiedzi","/qa/pl.html"],id:["Tanya jawab","/qa/id.html"],en:["Ask a question (Q&A)","/qa/"]}[L2]||["Ask a question (Q&A)","/qa/"];
  var g=el("div",null,"<b>Q&amp;A</b><ul><li><a href=\""+m[1]+"\">"+esc(m[0])+"</a></li></ul>");n.appendChild(g)}
function css2(){var s=d.createElement("style");s.textContent=".hl-recent{box-sizing:border-box;max-width:1100px;margin:18px auto;padding:14px 16px;border-radius:14px;background:#12305C;color:#fff;font-size:14px}.hl-recent b{display:block;margin-bottom:8px;color:#C9A04A;font-size:13px;letter-spacing:.02em}.hl-recent div{display:flex;flex-wrap:wrap;gap:8px}.hl-recent a{display:inline-block;max-width:100%;padding:7px 12px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(201,160,74,.55);color:#fff;text-decoration:none;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.hl-recent a:hover{background:rgba(201,160,74,.25)}.hl-rest{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(24px + env(safe-area-inset-bottom,0px));z-index:900;display:flex;align-items:center;gap:12px;max-width:calc(100% - 32px);padding:10px 12px 10px 16px;border-radius:12px;background:#12305C;color:#fff;font-size:13.5px;box-shadow:0 6px 24px rgba(0,0,0,.25);border-left:4px solid #C9A04A;transition:opacity .4s}.hl-rest button{all:unset;cursor:pointer;padding:5px 10px;border-radius:8px;background:#C9A04A;color:#12305C;font-weight:700;white-space:nowrap}.hl-rest--out{opacity:0}";d.head.appendChild(s)}
function init(){addCss();if(embed){embedMode();return}addEmbedBtn();try{css2();memo();recent();qaLink()}catch(e){}}
if(!embed){sw();chip()}
/* wait for DOMContentLoaded (fires after every deferred script, incl. share.js) */
if(d.readyState==="complete")init();else d.addEventListener("DOMContentLoaded",init);
}();
