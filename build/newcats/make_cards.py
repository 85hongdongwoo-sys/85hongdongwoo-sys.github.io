"""심리 테스트 결과 공유 카드 생성.
- 결과마다 인스타 피드용 1080x1350, 링크 미리보기용 1200x630 PNG를 Playwright로 그린다.
- 결과마다 공유 전용 페이지(/test/r/<slug>-<key>.html)를 만들어 og:image를 그 결과 카드로 둔다.
사용: python3 make_cards.py <overlay 경로>"""
import os, sys, json, html, re, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prep import TESTS
EXTRA = {}
from thumbs import ICON, COL
OUT = sys.argv[1]
E = lambda x: html.escape(str(x), quote=True)
AGE_G = [('초등학생 마음', '호기심 많고 솔직한 어린이 같은 마음이에요. 재미있는 일 앞에서는 망설이지 않아요.'),
         ('10대 마음', '유행에 빠르고 에너지가 넘쳐요. 하고 싶은 게 많은 청춘 그 자체예요.'),
         ('20대 마음', '새로운 경험을 즐기면서도 나름의 기준이 생긴 마음이에요.'),
         ('30대 마음', '열정과 현실 감각이 균형을 이룬 마음이에요. 할 땐 하고 쉴 땐 쉬어요.'),
         ('40대 마음', '여유롭고 차분하게 상황을 보는 어른스러운 마음이에요.'),
         ('60대 이상 마음', '웬만한 일에는 흔들리지 않는 넉넉한 마음이에요.')]

def results(t):
    k = t['kind']
    if k == 'score':
        n = len(t['bands'])
        return [(f'b{i}', b[1], b[2], dict(pos=i, n=n, tip=b[3][0])) for i, b in enumerate(t['bands'])]
    if k == 'dim':
        return [(key, v[0], v[1], dict(dims=[d[0] for d in t['dims'].values()], me=v[0], tip=v[2][0])) for key, v in t['dims'].items()]
    if k == 'axis2':
        return [(key, v[0], v[1], dict(quad=key, tip=v[2][0])) for key, v in t['axis']['types'].items()]
    if k == 'age':
        return [(f'g{i}', g[0], g[1], dict(pos=i, n=len(AGE_G))) for i, g in enumerate(AGE_G)]
    return []

def first_sentence(s):
    m = re.match(r'(.+?[요다]\.)', s)
    return (m.group(1) if m else s)[:70]

def hexmix(c, t):
    c = c.lstrip('#'); r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return '#%02X%02X%02X' % tuple(round(v + (255 - v) * t) for v in (r, g, b))

def shade(c, f=.72):
    c = c.lstrip('#'); return '#%02X%02X%02X' % tuple(round(int(c[i:i+2], 16) * f) for i in (0, 2, 4))

def extra_svg(info, c):
    if 'quad' in info:
        q = info['quad']; x = 70 if q[0] == 'H' else 26; y = 26 if q[1] == 'H' else 70
        return (f'<svg viewBox="0 0 96 96" class="viz"><rect x="2" y="2" width="92" height="92" rx="14" fill="#fff" stroke="{hexmix(c,.6)}" stroke-width="2"/>'
                f'<path d="M48 8v80M8 48h80" stroke="{hexmix(c,.6)}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="9" fill="{c}"/><circle cx="{x}" cy="{y}" r="16" fill="{c}" fill-opacity=".18"/></svg>')
    if 'pos' in info:
        n, p = info['n'], info['pos']
        segs = ''.join(f'<i style="background:{c if j == p else hexmix(c, .78)}"></i>' for j in range(n))
        return f'<div class="gauge">{segs}</div>'
    if 'dims' in info:
        return '<div class="dl">' + ''.join(f'<span class="{"on" if d == info["me"] else ""}">{E(d)}</span>' for d in info['dims']) + '</div>'
    return ''

import base64
BHS64 = base64.b64encode(open("/root/.fonts/BlackHanSans-Regular.ttf","rb").read()).decode()
CSS = """@font-face{font-family:BHS;src:url(data:font/ttf;base64,__BHS__)}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif;-webkit-font-smoothing:antialiased;word-break:keep-all}
.card{position:relative;overflow:hidden;background:var(--paper)}
.top{position:relative;background:var(--c);color:#fff;overflow:hidden}
.top .pat{position:absolute;right:-60px;top:-40px;opacity:.16}
.top .pat svg{width:100%;height:100%}
.lab{display:inline-flex;align-items:center;gap:10px;font-weight:700;background:rgba(255,255,255,.18);border:2px solid rgba(255,255,255,.35);border-radius:999px}
.lab b{width:12px;height:12px;border-radius:50%;background:#fff}
.me{font-weight:500;opacity:.9}
.name{max-width:calc(100% - 150px);font-family:BHS,"Noto Sans CJK KR";font-weight:400;line-height:1.02;letter-spacing:-.01em}
.ico{position:absolute;border-radius:36px;background:rgba(255,255,255,.2);display:grid;place-items:center}
.ico svg{fill:none;stroke:#fff;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}
.bot{position:relative}
.desc{color:#1F2430;font-weight:500;line-height:1.55}
.gauge{display:flex;gap:10px}.gauge i{flex:1;border-radius:99px;display:block}
.dl{display:flex;flex-wrap:wrap;gap:10px}.dl span{border-radius:999px;font-weight:700;background:var(--soft);color:var(--ink2)}.dl span.on{background:var(--c);color:#fff}
.viz{display:block}
.top{background:linear-gradient(150deg,var(--c) 0%,var(--c2) 100%)}
.top:after{content:"";position:absolute;inset:0;background:radial-gradient(60% 50% at 15% 0%,rgba(255,255,255,.22),transparent 70%)}
.tip{display:flex;gap:16px;align-items:flex-start;background:var(--soft);border-radius:22px}
.tip em{font-style:normal;font-weight:900;color:var(--c2);white-space:nowrap}
.tip span{color:#2B303B;font-weight:500}
.tags{color:var(--c2);font-weight:700}
.v .tip{margin-top:36px;padding:26px 30px;font-size:30px;line-height:1.5}
.v .tags{font-size:24px;margin-top:22px}
.h .tip{margin-top:24px;padding:16px 20px;font-size:21px;line-height:1.45;border-radius:16px}
.h .tags{display:none}
.foot{position:absolute;left:0;right:0;bottom:0;display:flex;align-items:center;justify-content:space-between;border-top:2px dashed var(--line)}
.brand{display:flex;align-items:center;gap:14px;font-weight:800;color:#1F2430}
.brand i{display:grid;place-items:center;background:#16325C;color:#fff;font-style:normal;font-weight:900;border-radius:10px}
.url{font-weight:500;color:#6B7684}
.cta{font-weight:800;color:#fff;background:#191F28;border-radius:999px}
/* 4:5 */
.v .card{width:1080px;height:1350px}
.v .top{height:690px;padding:70px 80px}
.v .top .pat{width:620px;height:620px}
.v .lab{font-size:30px;padding:14px 26px}
.v .me{font-size:44px;margin-top:118px}
.v .name{font-size:148px;margin-top:10px}
.v .ico{right:80px;bottom:72px;width:150px;height:150px}.v .ico svg{width:96px;height:96px}
.v .bot{padding:54px 80px 0}
.v .desc{font-size:40px}
.v .xtra{margin-top:32px}
.v .gauge i{height:18px}
.v .dl span{font-size:28px;padding:10px 22px}
.v .viz{width:118px;height:118px}
.v .foot{padding:34px 80px 46px}
.v .brand{font-size:32px}.v .brand i{width:52px;height:52px;font-size:30px}
.v .url{font-size:24px;margin-top:2px}
.v .cta{font-size:30px;padding:20px 34px}
/* OG 1200x630 */
.h .card{width:1200px;height:630px;display:grid;grid-template-columns:600px 1fr}
.h .top{height:630px;padding:52px 56px}
.h .top .pat{width:440px;height:440px}
.h .lab{font-size:22px;padding:10px 20px}
.h .me{font-size:34px;margin-top:120px}
.h .name{font-size:104px;margin-top:6px}
.h .ico{right:48px;bottom:48px;width:104px;height:104px;border-radius:26px}.h .ico svg{width:66px;height:66px}
.h .bot{padding:64px 56px 0}
.h .desc{font-size:30px}
.h .xtra{margin-top:30px}
.h .gauge i{height:14px}
.h .dl span{font-size:21px;padding:8px 16px}
.h .viz{width:120px;height:120px}
.h .foot{left:600px;padding:26px 56px 30px}
.h .brand{font-size:24px}.h .brand i{width:40px;height:40px;font-size:22px}
.h .url{font-size:18px}
.h .cta{font-size:22px;padding:14px 24px}
"""

def card_html(t, key, name, desc, info, mode, tip=''):
    c, soft = COL[t['slug']]
    icon = ICON[t['slug']]
    tname = t['name'].split(' (')[0]
    style = f'--c:{c};--c2:{shade(c)};--soft:{soft};--paper:#FFFDF9;--line:{hexmix(c,.75)};--ink2:{hexmix(c,-0) if False else "#3A3F4B"}'
    ic = f'<svg viewBox="0 0 48 48">{icon}</svg>'
    if 'quad' in info:
        q = info['quad']; x = 34 if q[0] == 'H' else 14; y = 14 if q[1] == 'H' else 34
        ic = f'<svg viewBox="0 0 48 48" style="stroke-width:2.4"><rect x="5" y="5" width="38" height="38" rx="8"/><path d="M24 7v34M7 24h34"/><circle cx="{x}" cy="{y}" r="5" fill="#fff"/></svg>'
        info = {k: v for k, v in info.items() if k != 'quad'}
    L = len(name.replace(' ', ''))
    fsv = 148 if L <= 5 else 124 if L <= 7 else 100 if L <= 10 else 84
    fsh = 104 if L <= 5 else 88 if L <= 7 else 70 if L <= 10 else 58
    pat = f'<svg viewBox="0 0 48 48" fill="none" stroke="#fff" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{icon}</svg>'
    me = '내 마음 나이는' if t['kind'] == 'age' else ('나는' if t['kind'] in ('dim', 'axis2') else '지금 나는')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS.replace("__BHS__", BHS64)}</style></head><body class="{mode}">'
            f'<div class="card" style="{style}"><div class="top"><div class="pat">{pat}</div><span class="lab"><b></b>{E(tname)} 결과</span>'
            f'<p class="me">{me}</p><h1 class="name" style="font-size:{fsv if mode == "v" else fsh}px">{E(name)}</h1><div class="ico">{ic}</div></div>'
            f'<div class="bot"><p class="desc">{E(first_sentence(desc))}</p><div class="xtra">{extra_svg(info, c)}</div>'
            + (f'<div class="tip"><em>한 걸음</em><span>{E(tip)}</span></div>' if tip else '')
            + f'<p class="tags">#{E(tname.replace(" ",""))} #{E(name.replace(" ",""))} #홍라이프도구</p></div>'
            f'<div class="foot"><div><div class="brand"><i>H</i>홍라이프 도구</div><div class="url">honglife.co.kr/test</div></div><span class="cta">나도 해 보기 →</span></div></div></body></html>')

SITE = 'https://honglife.co.kr'
def share_page(t, key, name, desc, tpl):
    HEAD, MID, BRAND, TAIL = tpl
    path = f'/test/r/{t["slug"]}-{key}.html'
    url = SITE + path; turl = f'/test/{t["slug"]}.html'
    title = f'나는 {name} — {t["name"].split(" (")[0]} 결과 | 홍라이프 도구'
    d = first_sentence(desc) + ' 나도 무료로 해 보기.'
    h = HEAD.replace('<meta name="viewport"', '<meta name="robots" content="noindex,follow">\n<meta name="viewport"', 1)
    h += f'<title>{E(title)}</title>\n<meta name="description" content="{E(d)}">\n<link rel="canonical" href="{SITE}{turl}">\n'
    h += (f'<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:site_name" content="홍라이프 도구"><meta property="og:locale" content="ko_KR">'
          f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(d)}">'
          f'<meta property="og:image" content="{SITE}/assets/share/test/og-{t["slug"]}-{key}.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n'
          f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/assets/share/test/og-{t["slug"]}-{key}.png">\n')
    h += MID + '<style>.rs{max-width:520px;margin:0 auto;text-align:center}.rs img{width:100%;height:auto;border-radius:22px;box-shadow:0 18px 40px -18px rgba(16,24,48,.35)}.rs .btn{margin-top:18px;width:100%}.rs p{margin:16px 0 0;color:var(--muted)}</style>\n</head>\n<body>\n\n' + BRAND
    h += (f'<main class="wrap"><header class="top"><p class="crumb"><a href="/">홈</a> › <a href="/test/">심리 테스트</a></p><h1>친구의 {E(t["name"].split(" (")[0])} 결과</h1></header>'
          f'<section class="card rs"><img src="/assets/share/test/{t["slug"]}-{key}.png" width="1080" height="1350" alt="{E(t["name"])} 결과: {E(name)}. {E(first_sentence(desc))}">'
          f'<a class="btn" href="{turl}">나도 {E(t["name"].split(" (")[0])} 해 보기</a><p>{t.get("qlabel", str(len(t["q"]))+"문항")} · 회원가입 없이 무료 · 답은 서버로 보내지 않아요</p></section></main>' + TAIL)
    fp = OUT + path; os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(h)

async def main():
    from playwright.async_api import async_playwright
    D = os.path.dirname(os.path.abspath(__file__))
    tpl = [open(f'{D}/tpl_{n}.html').read() for n in ('head', 'mid', 'brand', 'tail')]
    os.makedirs(OUT + '/assets/share/test', exist_ok=True)
    keys = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pv = await b.new_page(viewport={'width': 1080, 'height': 1350})
        ph = await b.new_page(viewport={'width': 1200, 'height': 630})
        for t in TESTS:
            if t['kind'] == 'phq9': continue
            t = dict(t)
            rs = results(t); keys[t['slug']] = [r[0] for r in rs]
            for key, name, desc, info in rs:
                for pg, mode, fn in ((pv, 'v', f'{t["slug"]}-{key}.png'), (ph, 'h', f'og-{t["slug"]}-{key}.png')):
                    await pg.set_content(card_html(t, key, name, desc, info, mode, info.get('tip', ''))); await pg.wait_for_timeout(120)
                    await pg.screenshot(path=f'{OUT}/assets/share/test/{fn}', type='png')
                share_page(t, key, name, desc, tpl)
        os.makedirs(OUT + '/assets/share/game', exist_ok=True)
        from data_games import GAMES
        for kind, L in (('test', TESTS), ('game', GAMES)):
            for t in L:
                t = dict(t); nm = t['name'].split(' (')[0]
                head = nm
                desc = t['lead']
                info = {}
                html_ = card_html(dict(t, name=('심리 테스트' if kind == 'test' else '게임 계산기'), kind='dim'), 'intro', head, desc, info, 'h', '')
                html_ = html_.replace('>나는<', '>' + ('무료 · ' + t['qlabel'] if kind == 'test' else '무료 계산기') + '<').replace(' 결과</span>', '</span>').replace('honglife.co.kr/test', 'honglife.co.kr/' + kind).replace('나도 해 보기 →', '바로 해 보기 →' if kind == 'test' else '계산해 보기 →')
                await ph.set_content(html_); await ph.wait_for_timeout(120)
                await ph.screenshot(path=f'{OUT}/assets/share/{kind}/og-{t["slug"]}.png', type='png')
        await b.close()
    json.dump(keys, open(f'{D}/card_keys.json', 'w'))
    print(sum(len(v) for v in keys.values()), 'results')
asyncio.run(main())
