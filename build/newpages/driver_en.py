"""English versions of the driver pages → overlay/en/driver/
Same official data as the Korean pages (HP/Sindoh files verified 2026-11-22). Visitors whose browser language is not Korean
are sent here from the Korean page (see driver_pages.REDIRECT); a 'Korean' link stores the choice and goes back."""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import driver_pages as kr

E = html.escape
ROOT, SITE = kr.ROOT, kr.SITE
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TPL = open(os.path.join(D, 'en_tpl.html'), encoding='utf-8').read()
HEAD = re.sub(r'<script type="application/ld\+json">.*?</script>', '', TPL[:TPL.find('</head>')], flags=re.S)
HEAD = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', HEAD)
HEAD = re.sub(r'<meta (property|name)="(og:image|twitter:image)[^"]*" content="[^"]*">', '', HEAD)
BODY_TOP = TPL[TPL.find('</head>'):TPL.find('<main')]
FOOT = TPL[TPL.find('<footer', TPL.find('</main>')):]
CHECKED = 'November 22, 2026'
DL = kr.DLICON
FONT = "font-family=\"Inter,'Noto Sans',sans-serif\""
pc, btn, ring = kr.pc, kr.btn, kr.ring


def head(title, desc, path, ld):
    url = SITE + path
    ko = SITE + kr.EN2KO[path]
    h = HEAD
    h = re.sub(r'<title>.*?</title>', f'<title>{E(title)}</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">'
               f'<link rel="alternate" hreflang="ko" href="{ko}"><link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="x-default" href="{ko}">', h, count=1)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(desc)}">', h, count=1)
    return h + kr.cu.CSS + kr.CSS + kr.HP_CSS + ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)


def write(path, title, desc, main, ld):
    out = os.path.join(ROOT, 'overlay', path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    ko = kr.EN2KO[path]
    langlink = (f'<p class="cu-src" style="margin:0 0 8px"><a href="{ko}" onclick="try{{localStorage.setItem(\'hl_lang\',\'ko\')}}catch(e){{}}">한국어로 보기 (Korean)</a></p>')
    top = BODY_TOP.replace('<a class="lang" href="/net/speed-test.html"', f'<a class="lang" href="{ko}" onclick="try{{localStorage.setItem(\'hl_lang\',\'ko\')}}catch(e){{}}"')
    open(out, 'w', encoding='utf-8').write(head(title, desc, path, ld) + top + '<main class="wrap wide">' + langlink + main + '</main>' + FOOT)


def crumb(items):
    parts = ['<a href="/en/">Home</a>', '<a href="/en/driver/">Drivers</a>'] + [f'<a href="{u}">{E(n)}</a>' if u else E(n) for n, u in items]
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
        for i, (n, u) in enumerate([('Home', '/en/'), ('Drivers', '/en/driver/')] + [(n, u) for n, u in items if u])]}
    return '<p class="crumb">' + ' › '.join(parts) + '</p>', ld


def faq(qa):
    return ('<section class="card"><h2>FAQ</h2><dl class="pe-faq">' + ''.join(f'<dt>{E(q)}</dt><dd>{a}</dd>' for q, a in qa) + '</dl></section>',
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in qa]})


def dl(url, title, sub, sec=False, newtab=True):
    return (f'<a class="dl3d{" s" if sec else ""}" href="{E(url)}"{" target=_blank" if newtab else ""} rel="noopener nofollow">'
            f'<span class="ic">{DL}</span><span class="tx"><b>{E(title)}</b><small>{E(sub)}</small></span></a>')


def step(n, title, body, svg):
    return kr.cu.step(n, title, body, svg)


# ── drawings (English labels) ──
def W_dl(fname, n):
    return pc('<rect x="150" y="44" width="170" height="104" rx="8" fill="#fff" stroke="#ADB5BD"/>'
              '<text x="162" y="64" font-size="11" font-weight="800" fill="#111">Downloads (Ctrl+J)</text>'
              '<rect x="160" y="74" width="150" height="40" rx="6" fill="#F8F9FA" stroke="#DEE2E6"/>'
              f'<text x="168" y="91" font-size="9.5" fill="#333">{E(fname)}</text><text x="168" y="105" font-size="8.5" fill="#868E96">Done</text>'
              + btn(250, 120, 60, 22, 'Open file', '#1B64DA', '#fff', 9.5) + ring(250, 120, 60, 22, n)
              + '<text x="44" y="80" font-size="10" fill="#495057">Files are saved</text><text x="44" y="96" font-size="10" fill="#495057">to your Downloads</text><text x="44" y="112" font-size="10" fill="#495057">folder</text>', 'Browser downloads')


def W_uac(app, n):
    return pc('<rect x="30" y="18" width="300" height="176" rx="6" fill="#E7EEF8"/><rect x="62" y="40" width="236" height="134" rx="8" fill="#fff" stroke="#ADB5BD"/>'
              '<text x="76" y="62" font-size="10" fill="#495057">User Account Control</text>'
              '<text x="76" y="82" font-size="11" font-weight="800" fill="#111">Do you want to allow this app</text>'
              '<text x="76" y="98" font-size="11" font-weight="800" fill="#111">to make changes to your device?</text>'
              f'<text x="76" y="118" font-size="9.5" fill="#868E96">{E(app)}</text>'
              + btn(150, 134, 64, 26, 'Yes', '#1B64DA') + btn(222, 134, 64, 26, 'No', '#E9ECEF', '#333') + ring(150, 134, 64, 26, n), 'Windows prompt')


def W_inst(title, lines, button, n):
    t = (f'<rect x="56" y="44" width="248" height="140" rx="8" fill="#fff" stroke="#ADB5BD"/>'
         f'<rect x="56" y="44" width="248" height="22" rx="8" fill="#334155"/><text x="66" y="59" font-size="10" fill="#fff" font-weight="700">{E(title)}</text>')
    y = 86
    for ln in lines:
        t += f'<text x="70" y="{y}" font-size="10.5" fill="#333">{E(ln)}</text>'
        y += 17
    return pc(t + btn(226, 148, 66, 26, button, '#1B64DA') + ring(226, 148, 66, 26, n), 'Installer')


def W_test(n):
    return pc('<text x="44" y="60" font-size="11" fill="#868E96">Settings › Bluetooth &amp; devices ›</text>'
              '<text x="44" y="78" font-size="13" font-weight="800" fill="#111">Printers &amp; scanners</text>'
              '<rect x="44" y="88" width="244" height="30" rx="6" fill="#F8F9FA" stroke="#DEE2E6"/><text x="56" y="107" font-size="10.5" fill="#333">🖨 My printer</text>'
              + btn(44, 128, 112, 28, 'Print test page', '#1B64DA') + ring(44, 128, 112, 28, n)
              + '<text x="166" y="146" font-size="9.5" fill="#868E96">Paper comes out = done!</text>', 'Windows Settings')


def W_devmgr(n):
    return pc('<text x="44" y="60" font-size="12.5" font-weight="800" fill="#111">Device Manager</text>'
              '<text x="52" y="82" font-size="10.5" fill="#333">› Network adapters</text>'
              '<text x="52" y="102" font-size="10.5" font-weight="800" fill="#1B64DA">⌄ Display adapters</text>'
              '<rect x="64" y="110" width="190" height="22" rx="4" fill="#EEF4FF"/><text x="72" y="125" font-size="10" fill="#111">Your graphics card name</text>'
              + ring(64, 110, 190, 22, n), 'Right-click Start → Device Manager')


# ── shared sections ──
def easy(brand, zipnote=False):
    z = ('<h3>If you downloaded a .zip file</h3><ol class="big-n"><li>Right-click the <b>.zip</b> file.</li>'
         '<li>Choose <b>Extract All…</b> and then <b>Extract</b>.</li><li>Open the new folder and double-click <b>SETUP.EXE</b> (or a file starting with Setup / Install).</li></ol>') if zipnote else ''
    return ('<section class="card dr-sec" id="easy"><h2>Very detailed guide for first-timers</h2>'
            '<p class="cu-ans"><b>In 3 lines</b><br>① Find your printer\'s <b>model name</b>. ② Click the <b>blue button</b> for your model on this page. ③ Open the file and keep clicking <b>Next</b>.</p>'
            '<h3>1. Windows or Mac?</h3><ul class="cu-chk"><li>A <b>window-shaped Start button</b> at the bottom of the screen means <b>Windows</b>.</li>'
            '<li>An <b>apple logo</b> at the top-left means <b>Mac</b>.</li><li>To check 64-bit: <b>Settings → System → About → System type</b>. Almost all recent PCs are 64-bit.</li></ul>'
            f'<h3>2. Find your {E(brand)} model name</h3><ul class="cu-chk"><li>Look on the <b>front or top</b> of the printer.</li>'
            '<li>Or check the <b>label on the back or bottom</b>, next to "Model".</li><li>If it was installed before, it may appear in <b>Settings → Bluetooth &amp; devices → Printers &amp; scanners</b>.</li>'
            '<li>Typing just the <b>numbers</b> in the search box works too.</li></ul>'
            '<h3>3. Where does the download go?</h3><ul class="cu-chk"><li>Chrome and Edge show a <b>download arrow (↓)</b> at the top-right.</li>'
            '<li>Press <b>Ctrl + J</b> to open your downloads, or open <b>File Explorer → Downloads</b>.</li><li>Files over 100 MB can take a few minutes. Keep the window open.</li></ul>'
            + z +
            '<h3>4. Buttons you will see</h3><ul class="cu-chk"><li><b>Yes</b> on "Do you want to allow this app to make changes?" — it is the official file.</li>'
            '<li><b>I agree</b> — accept the license to continue.</li><li><b>Next</b> — if unsure, keep the default choice and press Next.</li><li><b>Install</b> → wait → <b>Finish</b>.</li></ul>'
            '<h3>5. USB or Wi-Fi?</h3><ul class="cu-chk"><li><b>USB:</b> one cable, easiest, best for one computer.</li>'
            '<li><b>Wi-Fi / network:</b> no cable, many devices can share it. The printer and computer must be on the <b>same router (same Wi-Fi)</b>.</li></ul>'
            '<h3>6. After installing</h3><ul class="cu-chk"><li><b>Print test page:</b> Settings → Bluetooth &amp; devices → Printers &amp; scanners → your printer → <b>Print test page</b>.</li>'
            '<li><b>Make it default:</b> on the same screen, press <b>Set as default</b> (turn off "Let Windows manage my default printer" if the button is missing).</li>'
            '<li><b>"Offline"?</b> Check power and cable/Wi-Fi, turn the printer off and on, then restart the PC.</li></ul></section>')


WIN = ('<section class="card dr-sec" id="win"><h2>Try first: Windows automatic install</h2><p>Windows often installs a printer driver by itself.</p><ul class="cu-chk">'
       '<li>Go to <b>Settings → Bluetooth &amp; devices → Printers &amp; scanners</b> and press <b>Add device</b>.</li>'
       '<li>Microsoft recommends getting drivers through <b>Windows Update</b>.</li>'
       '<li>If that does not work, download the latest software from the maker\'s official site (this page).</li></ul></section>')
REL = ('<section class="card rel"><h2>Other drivers</h2><ul class="dr-co">'
       '<li><a href="/en/driver/hp.html"><b>HP</b><span>Printers (incl. Samsung printers)</span></a></li>'
       '<li><a href="/en/driver/sindoh.html"><b>Sindoh</b><span>Multifunction printers</span></a></li>'
       '<li><a href="/en/driver/epson.html"><b>Epson</b><span>EcoTank, WorkForce</span></a></li>'
       '<li><a href="/en/driver/brother.html"><b>Brother</b><span>Inkjet, laser, label</span></a></li>'
       '<li><a href="/en/driver/lg.html"><b>LG</b><span>gram laptops, monitors</span></a></li>'
       '<li><a href="/en/driver/apple.html"><b>Apple</b><span>iPhone on Windows, iCloud, Boot Camp</span></a></li>'
       '<li><a href="/en/driver/surface.html"><b>Microsoft Surface</b><span>Drivers &amp; firmware</span></a></li>'
       '<li><a href="/en/driver/lenovo.html"><b>Lenovo</b><span>Official update tools</span></a></li>'
       '<li><a href="/en/driver/dell.html"><b>Dell</b><span>Official update tools</span></a></li>'
       '<li><a href="/en/driver/asus.html"><b>ASUS</b><span>Official update tools</span></a></li>'
       '<li><a href="/en/driver/acer.html"><b>Acer</b><span>Official update tools</span></a></li>'
       '<li><a href="/en/driver/roborock.html"><b>Roborock</b><span>Robot vacuum app &amp; firmware</span></a></li>'
       '<li><a href="/en/driver/ecovacs.html"><b>ECOVACS</b><span>Robot vacuum app &amp; firmware</span></a></li>'
       '<li><a href="/en/driver/dreame.html"><b>Dreame</b><span>Robot vacuum app &amp; firmware</span></a></li>'
       '<li><a href="/en/driver/narwal.html"><b>Narwal</b><span>Robot vacuum app &amp; firmware</span></a></li>'
       '<li><a href="/en/driver/nvidia.html"><b>NVIDIA</b><span>GeForce / RTX graphics</span></a></li>'
       '<li><a href="/en/driver/amd.html"><b>AMD</b><span>Radeon graphics, Ryzen chipset</span></a></li>'
       '<li><a href="/en/driver/intel.html"><b>Intel</b><span>Driver &amp; Support Assistant</span></a></li>'
       '<li><a href="/en/driver/"><b>All drivers</b><span>Find by brand</span></a></li></ul></section>')


def src(s):
    return (f'<section class="card"><h2>Sources</h2><p class="cu-src">Sources: {E(s)} · checked {CHECKED}.<br>'
            'HongLife Tools does not host driver files. Every download comes from the manufacturer\'s official server. '
            'Drawings are simplified and may differ from the real screens.</p></section>')


def howto(name, names):
    return kr.howto(name, names)


def search_box(items, ph, var):
    data = json.dumps(items, ensure_ascii=False)
    return (f'<form class="dr-q" onsubmit="return {var}()"><input id="dr-in" placeholder="{E(ph)}" autocomplete="off" oninput="{var}()" aria-label="Model search"><button type="submit">Find</button></form><ul id="dr-res"></ul>'
            f'<script>var {var}D={data};function {var}(){{var q=document.getElementById("dr-in").value.replace(/\\s/g,"").toUpperCase(),r=document.getElementById("dr-res");if(!q){{r.innerHTML="";return false}}'
            f'var h={var}D.filter(function(x){{return x[0].replace(/\\s/g,"").toUpperCase().indexOf(q)>=0}}).slice(0,8);'
            'r.innerHTML=h.length?h.map(function(x){return\'<li><a href="\'+x[1]+\'">\'+x[0]+\' ›</a></li>\'}).join(""):"<li>Not in this list. Use the official site search below.</li>";return false}</script>')


# ── HP ──
HPEN = json.load(open(os.path.join(D, 'hp_models_en.json'), encoding='utf-8'))


def hp():
    path = '/en/driver/hp.html'
    cr, crld = crumb([('HP drivers', '')])
    cards = []
    for m in kr.HP_DATA['models']:
        e = HPEN[str(m['o'])]
        name = e['n']
        t, u, sz, ver, d = m['w']
        mt, mu, msz, app = m['m']
        b = (f'<a class="dl3d" href="{E(u)}" rel="nofollow"><span class="ic">{DL}</span><span class="tx"><b>Download for Windows</b><small>{E(sz)} · starts right away</small></span></a>'
             f'<a class="dl3d s" href="{E(mu)}" rel="nofollow"{" target=_blank" if app else ""}><span class="ic">{DL}</span><span class="tx"><b>Mac</b><small>{E("HP Smart app (App Store)" if app else "HP Easy Start" if "Easy" in mt else "Mac printer driver")}{(" · " + E(msz)) if msz else ""}</small></span></a>')
        ex = (f'<a class="sm" href="{E(m["b"][0])}" rel="nofollow">Basic driver only ({E(m["b"][1])}, 64-bit)</a>' if m.get('b') else '')
        ex += f'<a class="sm" href="https://support.hp.com/us-en/hp-pps-services/hub/navigation?h_product={m["o"]}&amp;h_lang=en&amp;h_cc=us&amp;h_pagetype=s-002" target="_blank" rel="noopener nofollow">View on HP.com ↗</a>'
        cards.append(f'<li class="hpm" id="{kr.mid(m["n"])}"><h3>{E(name)}</h3><p class="fi">📦 {E(e["t"])}<br><span>Version {E(ver)} · released {E(d)}</span></p><div class="bt">{b}</div><p class="ex">{ex}</p></li>')
    items = [[HPEN[str(m['o'])]['n'], '#' + kr.mid(m['n'])] for m in kr.HP_DATA['models']]
    install = ('<section class="card dr-sec" id="install"><h2>How to install after downloading (step by step)</h2><ol class="big-n">'
               '<li><b>Prepare:</b> close other programs and <b>turn the printer on</b>.</li>'
               '<li><b>Do not plug in the USB cable yet.</b> HP\'s instructions say to connect it only when the installer asks.</li>'
               '<li><b>Open the file:</b> press <b>Ctrl + J</b> and click the file you just downloaded (it starts with Full_Webpack…).</li>'
               '<li><b>Click Yes</b> on "Do you want to allow this app to make changes to your device?". The file unpacks and setup starts.</li>'
               '<li><b>Follow the screens:</b> choose <b>USB</b> or <b>Wireless/Network</b> and press <b>Next</b>.</li>'
               '<li><b>USB users:</b> plug in the cable when the screen says so.</li>'
               '<li><b>Wait</b> a few minutes. Restart the PC if asked.</li>'
               '<li><b>Check:</b> Settings → Bluetooth &amp; devices → Printers &amp; scanners → your printer → <b>Print test page</b>.</li></ol>'
               '<p class="tipbox">💡 <b>Full software or basic driver?</b> If unsure, use the blue <b>Download for Windows</b> (full software). HP describes it as the complete set of driver, installer and tools that came on the printer CD. '
               '"Basic driver only" installs just the print driver (for IT admins, 64-bit Windows only).</p></section>')
    pics = (step(1, 'Click the blue button', 'The file downloads from HP\'s server and a download arrow appears at the top-right.', W_dl('Full_Webpack…exe', 1))
            + step(2, 'Click Yes', 'Windows asks for permission. Click <b>Yes</b>.', W_uac('HP installer', 2))
            + step(3, 'Pick USB or Wi-Fi, then Next', 'Choose how the printer connects. Plug in USB only when asked.', W_inst('HP printer setup', ['Choose a connection', '○ USB cable', '○ Wireless'], 'Next', 3))
            + step(4, 'Print a test page', 'Settings → Bluetooth &amp; devices → Printers &amp; scanners → your printer → <b>Print test page</b>.', W_test(4)))
    qa = [('Does it really download from this page?', 'Yes. "Download for Windows" points straight to HP\'s official file server (ftp.hp.com). HongLife Tools only links to the files HP publishes.'),
          ('Is it free?', 'Yes. HP drivers are free and no sign-in is needed.'),
          ('No CD?', 'No problem. The full software contains everything that was on the CD.'),
          ('Samsung printer?', 'Samsung printer support is now handled by HP (Samsung\'s official notice). Search your Samsung model (e.g. SL-…) on HP\'s driver page.'),
          ('The release date looks old.', 'It is the date HP last released that file. HP still offers it for Windows 11 (as of the check date).')]
    fq, fqld = faq(qa)
    main = (f'<header class="top hub">{cr}<h1>HP Printer Drivers — Direct Download &amp; Easy Install (incl. Samsung)</h1>'
            f'<p class="lead">Download drivers for {len(items)} popular HP printers right here. Files come from HP\'s official server.</p>'
            '<p class="cu-ans">Find your <b>model</b> below and click <b>Download for Windows</b> — the HP installer starts downloading immediately. Open it and follow the screens. No account needed. <b>Samsung printers</b> are now supported by HP too.</p>'
            '<ul class="dr-toc"><li><a href="#models">Models</a></li><li><a href="#install">Install steps</a></li><li><a href="#easy">First time?</a></li><li><a href="#notlisted">Not listed</a></li></ul></header>'
            f'<section class="card dr-sec" id="models"><h2>Direct downloads by model ({len(items)})</h2>'
            + search_box(items, 'Model number (e.g. 8210, M15, 2130)', 'hpE') + '<ul class="hpl">' + ''.join(cards) + '</ul>'
            + f'<p class="cu-src" style="margin-top:10px">File details checked on HP Support (Windows 11 / macOS 15) on {CHECKED}. For 32-bit or other versions, use "View on HP.com".</p></section>'
            + install + easy('HP') + f'<section class="card dr-sec"><h2>In pictures</h2>{pics}</section>'
            + '<section class="card dr-sec" id="notlisted"><h2>Model not listed?</h2><p>Open HP\'s Software and Drivers page, choose <b>Printer</b>, enter your model name and submit. HP picks your operating system automatically; download the <b>full feature software</b> and install it as above.</p>'
            + dl('https://support.hp.com/us-en/drivers', 'Search on HP Support', 'Official HP Software and Drivers') + '</section>'
            + WIN + fq + src('HP Support software and driver data (support.hp.com), HP install instructions, Samsung notice on printer support by HP, Microsoft Support') + REL)
    write(path, 'HP Printer Driver Download — Direct Links by Model (OfficeJet, LaserJet, DeskJet, Samsung) | HongLife Tools',
          'Download HP printer drivers for OfficeJet Pro 8210/8710/9010, LaserJet Pro M15/P1102, DeskJet 2130 and more directly from HP\'s official server, with an easy step-by-step install guide.',
          main, [crld, fqld, howto('How to install an HP printer driver', ['Download for Windows', 'Close programs and turn the printer on', 'Open the file', 'Click Yes', 'Choose USB or Wi-Fi and Next', 'Plug in USB when asked', 'Print a test page'])])
    return path


# ── Sindoh ──
def sindoh():
    path = '/en/driver/sindoh.html'
    cr, crld = crumb([('Sindoh drivers', '')])
    S = kr.SD_DATA
    cards = []
    kind_en = {'A3 컬러 복합기': 'A3 color MFP', 'A3 흑백 복합기': 'A3 mono MFP', 'A4 흑백 복합기': 'A4 mono MFP'}
    for m, kind in kr.SD_MODELS:
        x = S['models'].get(m) or {}
        b = f'<a class="dl3d" href="{E(S["connect"][3])}" rel="nofollow"><span class="ic">{DL}</span><span class="tx"><b>sindoh Connect</b><small>One-click installer · recommended by Sindoh</small></span></a>'
        if x.get('q'):
            b += f'<a class="dl3d s" href="{E(x["q"][3])}" rel="nofollow"><span class="ic">{DL}</span><span class="tx"><b>Quick-install driver</b><small>{E(x["q"][0].replace("빠른설치", "quick install").replace("빠른 설치 드라이버", "quick install").replace("빠른 설치", "quick install"))} · {E(x["q"][1])}</small></span></a>'
        ex = (f'<a class="sm" href="{E(x["s"][3])}" rel="nofollow">Scan software ({E(x["s"][0])})</a>' if x.get('s') else '')
        ex += f'<a class="sm" href="https://www.sindoh.com/support/download/{m.lower()}" target="_blank" rel="noopener nofollow">Official Sindoh page ↗</a>'
        cards.append(f'<li class="hpm" id="m-{m}"><h3>Sindoh {m} <span style="font-size:13px;color:var(--muted,#5B6B82);font-weight:600">{kind_en[kind]}</span></h3><p class="fi">Windows 10/11 (64-bit)</p><div class="bt">{b}</div><p class="ex">{ex}</p></li>')
    items = [[f'Sindoh {m}', f'#m-{m}'] for m, _ in kr.SD_MODELS]
    steps = ('<ol class="big-n"><li>Click <b>sindoh Connect</b> for your model (recommended by Sindoh for these models).</li>'
             '<li>Open it with <b>Ctrl + J</b>, click <b>Yes</b>, pick your machine and install.</li>'
             '<li>If that fails, download the <b>Quick-install driver</b> (.zip), right-click → <b>Extract All</b>, run <b>SETUP.EXE</b>.</li>'
             '<li>In <b>Sindoh Easy Printer Setup Tool</b>, change the local port from <b>LPT1</b> to <b>USB</b> (for USB) and click <b>Install</b>.</li>'
             '<li>Print a test page from Settings → Bluetooth &amp; devices → Printers &amp; scanners.</li></ol>')
    qa = [('Where do the files come from?', 'Directly from Sindoh\'s official servers (sindoh.com / sindoh Connect).'),
          ('Help in English?', 'Sindoh is a Korean company; its support center number is 1588-5850 (Korea).')]
    fq, fqld = faq(qa)
    main = (f'<header class="top hub">{cr}<h1>Sindoh Printer / MFP Drivers — Direct Download by Model</h1>'
            '<p class="lead">Drivers for 23 Sindoh multifunction printers (D452, D472, N502, M702 …) straight from Sindoh\'s server, with easy install steps.</p>'
            '<ul class="dr-toc"><li><a href="#models">Models</a></li><li><a href="#steps">Install steps</a></li><li><a href="#easy">First time?</a></li></ul></header>'
            '<section class="card dr-sec" id="models"><h2>Direct downloads by model (23)</h2>' + search_box(items, 'Model (e.g. D452)', 'sdE')
            + '<ul class="hpl">' + ''.join(cards) + '</ul>' + f'<p class="cu-src" style="margin-top:10px">Files checked on Sindoh\'s official download pages on {CHECKED}.</p></section>'
            + f'<section class="card dr-sec" id="steps"><h2>Install steps</h2>{steps}</section>' + easy('Sindoh', True) + WIN + fq
            + src('Sindoh official download pages and support FAQ (sindoh.com, support.sindoh.com)') + REL)
    write(path, 'Sindoh Driver Download — Direct Links by Model (D452, D472, N502) | HongLife Tools',
          'Download Sindoh MFP drivers (sindoh Connect, quick-install driver, scan software) for D452, D472, D742, N502, M702 and more directly from Sindoh, with an easy install guide.',
          main, [crld, fqld])
    return path


# ── NVIDIA / AMD / Intel ──
def nvidia():
    path = '/en/driver/nvidia.html'
    cr, crld = crumb([('NVIDIA drivers', '')])
    steps = (step(1, 'Find your graphics card', 'Right-click Start → <b>Device Manager → Display adapters</b>. GeForce, RTX or GTX means NVIDIA.', W_devmgr(1))
             + step(2, 'Pick your product and Find Drivers', 'On NVIDIA\'s driver page choose product category, series, product, operating system, language and download type, then click <b>Find Drivers</b>. Gamers pick <b>Game Ready</b>; creators pick <b>Studio</b>.', W_dl('NVIDIA_driver.exe', 2))
             + step(3, 'Run and click Yes', 'Open the file, click <b>Yes</b> and follow the installer. The screen may flicker — that is normal.', W_uac('NVIDIA installer', 3)))
    qa = [('Game Ready or Studio?', 'Per NVIDIA, Game Ready is tuned for games and Studio for creative apps.'), ('Automatic updates?', 'Install the NVIDIA App to get notified and update with one click.')]
    fq, fqld = faq(qa)
    main = (f'<header class="top hub">{cr}<h1>NVIDIA Graphics Driver — Download &amp; Install</h1><p class="lead">GeForce / RTX drivers from NVIDIA\'s official site, step by step.</p>'
            + dl('https://www.nvidia.com/en-us/geforce/drivers/', 'Go to NVIDIA drivers', 'Official NVIDIA driver page') + '</header>'
            f'<section class="card dr-sec"><h2>Steps</h2>{steps}</section>' + fq + src('NVIDIA official driver page') + REL)
    write(path, 'NVIDIA Graphics Driver Download & Install (Game Ready / Studio) | HongLife Tools',
          'How to download and install NVIDIA GeForce / RTX drivers from the official site: find your GPU, Game Ready vs Studio, NVIDIA App updates.', main, [crld, fqld])
    return path


def amd():
    path = '/en/driver/amd.html'
    cr, crld = crumb([('AMD drivers', '')])
    rows = ''.join(f'<li class="hpm" id="{kr.re.sub(r"[^A-Za-z0-9]", "", m) and "m-" + kr.re.sub(r"[^A-Za-z0-9]", "", m)}"><h3>{E(m)}</h3><div class="bt">'
                   f'<a class="dl3d s" href="{E(u.replace("/ko/", "/en/"))}" target="_blank" rel="noopener nofollow"><span class="ic">{DL}</span><span class="tx"><b>Official AMD page</b><small>Auto-Detect &amp; driver downloads</small></span></a></div></li>'
                   for m, _, u in kr.AMD_MODELS)
    steps = (step(1, 'Find your graphics card', 'Right-click Start → <b>Device Manager → Display adapters</b>.', W_devmgr(1))
             + step(2, 'Download Auto-Detect and Install', 'On any AMD product page, under Windows 10/11, click <b>Download Auto-Detect and Install</b> (a small tool). It detects your graphics card and Windows version and installs the matching official driver.', W_dl('amd-software-auto-detect.exe', 2))
             + step(3, 'Run, click Yes, follow the tool', 'Open the file, click <b>Yes</b>, and let the tool install AMD Software: Adrenalin Edition.', W_uac('AMD installer', 3)))
    main = (f'<header class="top hub">{cr}<h1>AMD Radeon &amp; Ryzen Chipset Drivers — Download &amp; Install</h1><p class="lead">The easiest way is AMD\'s Auto-Detect and Install tool.</p></header>'
            f'<section class="card dr-sec"><h2>Steps</h2>{steps}</section><section class="card dr-sec"><h2>Product pages</h2><ul class="hpl">{rows}</ul></section>'
            + src('AMD official drivers and downloads pages') + REL)
    write(path, 'AMD Radeon & Ryzen Chipset Driver Download (Auto-Detect) | HongLife Tools',
          'Download AMD Radeon graphics and Ryzen chipset drivers from AMD: Auto-Detect and Install, Adrenalin Edition, product links.', main, [crld])
    return path


def intel():
    path = '/en/driver/intel.html'
    cr, crld = crumb([('Intel drivers', '')])
    steps = ('<ol class="big-n"><li>Check <b>Device Manager</b> for items with <b>Intel</b> in the name (display, Wi-Fi, Bluetooth).</li>'
             '<li>Download <b>Intel® Driver &amp; Support Assistant</b> from Intel\'s official page.</li>'
             '<li>Install it by following the on-screen instructions.</li>'
             '<li>Run the assistant to get driver and software updates for your Intel hardware.</li>'
             '<li>On laptops, if something goes wrong, use the laptop maker\'s driver instead.</li></ol>')
    main = (f'<header class="top hub">{cr}<h1>Intel Drivers — Driver &amp; Support Assistant</h1><p class="lead">Update Intel graphics, chipset, Wi-Fi and Bluetooth drivers in one place.</p>'
            + dl('https://www.intel.com/content/www/us/en/support/detect.html', 'Get Intel Driver & Support Assistant', 'Official Intel page') + '</header>'
            f'<section class="card dr-sec"><h2>Steps</h2>{steps}</section>' + src('Intel Driver & Support Assistant official page') + REL)
    write(path, 'Intel Driver Download — Intel Driver & Support Assistant | HongLife Tools',
          'Update Intel graphics, chipset, Wi-Fi and Bluetooth drivers with Intel Driver & Support Assistant, step by step.', main, [crld])
    return path


def hub():
    path = '/en/driver/'
    cr = '<p class="crumb"><a href="/en/">Home</a> › Drivers</p>'
    co = ''.join(f'<li><a href="/en/driver/{k}.html"><b>{n}</b><span>{d}</span></a></li>' for k, n, d in [
        ('hp', 'HP', 'Printers, direct download for 22 models (incl. Samsung)'), ('sindoh', 'Sindoh', 'MFPs, direct download for 23 models'), ('epson', 'Epson', 'EcoTank, WorkForce and more, by model'), ('brother', 'Brother', 'Inkjet, laser, label, by model'), ('lg', 'LG', 'gram laptops (LG Update), monitors (OnScreen Control)'), ('apple', 'Apple', 'Apple Devices, iCloud, iTunes, Boot Camp'), ('surface', 'Microsoft Surface', 'Drivers & firmware by model'), ('lenovo', 'Lenovo', 'Official driver update tools'), ('dell', 'Dell', 'Official driver update tools'), ('asus', 'ASUS', 'Official driver update tools'), ('acer', 'Acer', 'Official driver update tools'), ('roborock', 'Roborock', 'Robot vacuum app & firmware update'), ('ecovacs', 'ECOVACS', 'Robot vacuum app & firmware update'), ('dreame', 'Dreame', 'Robot vacuum app & firmware update'), ('narwal', 'Narwal', 'Robot vacuum app & firmware update'),
        ('nvidia', 'NVIDIA', 'GeForce / RTX graphics'), ('amd', 'AMD', 'Radeon graphics, Ryzen chipset'), ('intel', 'Intel', 'Driver & Support Assistant')])
    items = [[HPEN[str(m['o'])]['n'], '/en/driver/hp.html#' + kr.mid(m['n'])] for m in kr.HP_DATA['models']] + [[f'Sindoh {m}', f'/en/driver/sindoh.html#m-{m}'] for m, _ in kr.SD_MODELS]
    import driver_more as dm
    items += dm.ep_hub_items('/en') + dm.br_hub_items('/en')
    main = (f'<header class="top hub">{cr}<h1>Driver Downloads — Printers &amp; Graphics</h1>'
            '<p class="lead">Drivers collected by brand, with direct downloads from official servers and very easy install steps.</p>'
            + search_box(items, 'Model (e.g. 8210, D452)', 'hubE') + '</header>'
            f'<section class="card"><h2>Choose a brand</h2><ul class="dr-co">{co}</ul></section>' + WIN
            + '<section class="card"><h2>Avoid fake driver sites</h2><p class="dr-warn">Do not install "driver updater" programs from ads or files posted on blogs — they may add unwanted software. Use the maker\'s official site or Windows Update.</p></section>'
            + src('Manufacturers\' official support sites, Microsoft Support'))
    write(path, 'Driver Downloads — Printer & Graphics Drivers by Brand (HP, Samsung, Epson, Brother, Sindoh, NVIDIA, AMD, Intel) | HongLife Tools',
          'Printer and graphics drivers by brand with direct downloads from official servers and easy install steps: HP, Samsung, Sindoh, NVIDIA, AMD, Intel.', main, [])
    return path


if __name__ == '__main__':
    print('\n'.join([hub(), hp(), sindoh(), nvidia(), amd(), intel()]))
