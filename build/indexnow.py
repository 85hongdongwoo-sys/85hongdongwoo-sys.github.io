"""Notify Naver (Search Advisor IndexNow) and the shared IndexNow endpoint about new/changed pages.
MODE=all  -> every <loc> in https://honglife.co.kr/sitemap.xml
MODE=changed -> overlay/*.html files changed in the last commit (+ home, rss)."""
import glob, json, os, re, subprocess, urllib.request

HOST = 'honglife.co.kr'
KEY = [os.path.basename(p)[:-4] for p in glob.glob('overlay/*.txt') if re.fullmatch(r'[0-9a-f]{32}\.txt', os.path.basename(p))][0]
ENDPOINTS = ['https://searchadvisor.naver.com/indexnow', 'https://api.indexnow.org/indexnow']

def live_sitemap():
    req = urllib.request.Request(f'https://{HOST}/sitemap.xml', headers={'User-Agent': 'Mozilla/5.0 indexnow-ping'})
    xml = urllib.request.urlopen(req, timeout=60).read().decode('utf-8')
    return re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', xml)

def changed():
    out = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'], capture_output=True, text=True).stdout.split()
    urls = []
    for f in out:
        if f.startswith('overlay/') and f.endswith('.html') and os.path.exists(f):
            p = f[len('overlay/'):]
            p = p[:-10] if p.endswith('index.html') else p
            urls.append(f'https://{HOST}/{p}')
    if os.path.exists('build/newcats') and any(f.startswith('build/newcats/') for f in out):
        urls += [u for u in live_sitemap() if '/gov/' in u]
    return urls + [f'https://{HOST}/', f'https://{HOST}/rss.xml']

mode = os.environ.get('MODE', 'changed')
urls = live_sitemap() if mode == 'all' else changed()
urls = list(dict.fromkeys(u for u in urls if u.startswith(f'https://{HOST}/')))
print('mode', mode, 'urls', len(urls))
for ep in ENDPOINTS:
    for i in range(0, len(urls), 10000):
        body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt',
                           'urlList': urls[i:i + 10000]}).encode()
        req = urllib.request.Request(ep, data=body, method='POST',
                                     headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            r = urllib.request.urlopen(req, timeout=60)
            print(ep, r.status, r.read()[:200])
        except urllib.error.HTTPError as e:
            print(ep, 'HTTP', e.code, e.read()[:300])
        except Exception as e:
            print(ep, 'ERR', e)
