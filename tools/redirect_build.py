#!/usr/bin/env python3
"""honglife.co.kr is now empty: every page redirects to honglifecalc.com.
Korean pages -> https://honglifecalc.com/ko/<same path>, foreign folders -> https://honglifecalc.com/<same path>.
The repo files stay as a backup; only redirect stubs (and verification files) are published."""
import os, shutil, html, fnmatch
NEW = 'https://honglifecalc.com'
F = set('us uk ca au in de fr es it mx br ph pt nl pl id jp en ru ar zh hi tw vn ie nz sg za ae ng my se no dk tr ch at be eg arg co cl hk'.split())
SKIP = {'.git', '.github', '_site', 'tools'}
KEEP = ['CNAME', 'ads.txt', 'robots.txt', 'sitemap.xml', 'google*.html', 'naver*.html', '6b2e18c347379a40e0b8abb404160efc.txt', '8ac73bfae945e03a847933dd28733f13.txt']
removed = set()
if os.path.exists('tools/REMOVE.txt'):
    removed = {l.strip().lstrip('/') for l in open('tools/REMOVE.txt', encoding='utf-8') if l.strip()}
if os.path.exists('_site'): shutil.rmtree('_site')
os.makedirs('_site')
for name in os.listdir('.'):
    if os.path.isfile(name) and any(fnmatch.fnmatch(name, k) for k in KEEP):
        shutil.copy2(name, os.path.join('_site', name))

def stub(rel):
    top = rel.split('/')[0]
    path = rel[:-10] if rel.endswith('index.html') else rel
    u = f'{NEW}/{path}' if top in F else f'{NEW}/ko/{path}'
    if rel in removed: u = f'{NEW}/ko/' if top not in F else f'{NEW}/{top}/'
    e = html.escape(u)
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>홍라이프 계산기가 honglifecalc.com으로 이사했어요</title>'
            f'<link rel="canonical" href="{e}"><meta http-equiv="refresh" content="0; url={e}">'
            f'<script>location.replace({u!r}+location.search+location.hash)</script></head>'
            f'<body><p>홍라이프 계산기는 이제 <a href="{e}">{e}</a> 에서 볼 수 있어요.</p></body></html>\n')

n = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not (root == '.' and d in SKIP)]
    for fn in files:
        if not fn.endswith('.html'): continue
        rel = os.path.relpath(os.path.join(root, fn), '.').replace(os.sep, '/')
        if '/' not in rel and any(fnmatch.fnmatch(rel, k) for k in ('google*.html', 'naver*.html')): continue
        out = os.path.join('_site', rel)
        os.makedirs(os.path.dirname(out) or '_site', exist_ok=True)
        open(out, 'w', encoding='utf-8').write(stub(rel))
        n += 1
# old service worker: remove itself and its caches, then reload into the redirect
open('_site/sw.js', 'w').write("self.addEventListener('install',()=>self.skipWaiting());"
    "self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.map(x=>caches.delete(x))))"
    ".then(()=>self.registration.unregister()).then(()=>self.clients.matchAll()).then(c=>c.forEach(w=>w.navigate(w.url)))));\n")
open('_site/404.html', 'w', encoding='utf-8').write(stub('index.html').replace("location.replace('https://honglifecalc.com/ko/'+location.search+location.hash)",
    "var F="+repr(sorted(F)).replace("'",'"')+";var t=location.pathname.split('/')[1];location.replace('https://honglifecalc.com'+(F.indexOf(t)<0?'/ko':'')+location.pathname+location.search+location.hash)"))
print('redirect stubs:', n)
