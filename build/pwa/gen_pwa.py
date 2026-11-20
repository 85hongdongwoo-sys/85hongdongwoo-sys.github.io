"""페이지별 앱(PWA): 사이트맵의 모든 페이지에 전용 매니페스트를 달아, 그 페이지에서 '홈 화면에 추가/앱 설치'하면
그 도구가 바로 열리는 독립 앱이 되게 한다. 매일 쓰는 도구(apps.py)는 전용 아이콘 + 페이지 안 설치 띠.
배포 때 실행: python3 build/pwa/gen_pwa.py _site   (patch_site.py·gen_exams.py 다음)"""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apps import APPS, key  # noqa: E402

root = sys.argv[1] if len(sys.argv) > 1 else '_site'
SITE = 'https://honglife.co.kr'
A = {p: (n, e) for p, n, e, _ in APPS}
SITE_ICONS = [{"src": "/assets/brand/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
              {"src": "/assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
              {"src": "/assets/brand/icon-maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
              {"src": "/assets/brand/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]


def fpath(p):
    return os.path.join(root, p.lstrip('/') + ('index.html' if p.endswith('/') else ''))


def clip(s, n):
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= n else s[:n].rstrip(' ·,(-')


def short_of(title):
    t = re.split(r'\s*[|]\s*', title)[0]
    t = re.split(r'\s+[—–-]\s+|\s*\(|\s*:\s', t)[0].strip()
    if len(t) <= 12:
        return t or '홍라이프'
    w = t.split(' ')
    out = ''
    for x in w:
        if len((out + ' ' + x).strip()) > 12:
            break
        out = (out + ' ' + x).strip()
    out = out.rstrip(' ·/,')
    return out if len(out) >= 3 else clip(t, 12)


sm = open(os.path.join(root, 'sitemap.xml'), encoding='utf-8').read()
paths = [u[len(SITE):] or '/' for u in re.findall(r'<loc>(https://honglife\.co\.kr[^<]*)</loc>', sm)]
outdir = os.path.join(root, 'app', 'm')
os.makedirs(outdir, exist_ok=True)
n_page = n_app = 0
for p in paths:
    if p == '/':
        continue
    f = fpath(p)
    if not os.path.isfile(f):
        continue
    s = open(f, encoding='utf-8').read()
    if '<link rel="manifest" href="/manifest.webmanifest">' not in s:
        continue
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    title = html.unescape(t.group(1)) if t else p
    name = clip(re.split(r'\s*[|]\s*', title)[0], 45)
    k = key(p)
    if p in A:
        short, _ = A[p]
        icons = [{"src": f"/assets/app/{k}-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                 {"src": f"/assets/app/{k}-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                 {"src": f"/assets/app/{k}-m512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]
    else:
        short, icons = short_of(title), SITE_ICONS
    man = {"id": p, "name": name, "short_name": short, "start_url": p + "?source=pwa", "scope": "/",
           "display": "standalone", "background_color": "#FFFFFF", "theme_color": "#14286A", "lang": "ko",
           "description": f"홍라이프 도구 — {name}", "icons": icons,
           "shortcuts": [{"name": "홍라이프 도구 홈", "short_name": "홈", "url": "/?source=pwa",
                          "icons": [{"src": "/assets/brand/icon-192.png", "sizes": "192x192"}]}]}
    json.dump(man, open(os.path.join(outdir, k + '.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    s = s.replace('<link rel="manifest" href="/manifest.webmanifest">', f'<link rel="manifest" href="/app/m/{k}.webmanifest">', 1)
    s = s.replace('<meta name="apple-mobile-web-app-title" content="홍라이프">',
                  f'<meta name="apple-mobile-web-app-title" content="{html.escape(short)}">', 1)
    if p in A:
        s = re.sub(r'<link rel="apple-touch-icon"[^>]*>', f'<link rel="apple-touch-icon" href="/assets/app/{k}-180.png">', s, count=1)
        if 'name="hl-app"' not in s:
            s = s.replace('</head>', f'<meta name="hl-app" content="{html.escape(short)}|/assets/app/{k}-192.png">' + '</head>', 1)
        n_app += 1
    open(f, 'w', encoding='utf-8').write(s)
    n_page += 1
print('pwa: per-page manifests', n_page, '· app icons + install bar', n_app)
