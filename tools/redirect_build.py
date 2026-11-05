#!/usr/bin/env python3
"""Build _site for honglife.co.kr: copy repo, replace foreign-language pages with redirects to honglifecalc.com."""
import os, shutil, html
NEW = 'https://honglifecalc.com'
F = ['us','uk','ca','au','in','de','fr','es','it','mx','br','ph','pt','nl','pl','id','jp','en','ru','ar','zh','hi']
SKIP = {'.git', '.github', '_site', 'tools'}
ACTIVE = os.path.exists('tools/MOVE_ON')  # create tools/MOVE_ON once https://honglifecalc.com has a certificate
os.makedirs('_site', exist_ok=True)
for name in os.listdir('.'):
    if name in SKIP: continue
    src = name; dst = os.path.join('_site', name)
    if os.path.isdir(src): shutil.copytree(src, dst)
    else: shutil.copy2(src, dst)
n = 0
for d in (F if ACTIVE else []):
    base = os.path.join('_site', d)
    if not os.path.isdir(base): continue
    for root, _, files in os.walk(base):
        for fn in files:
            if not fn.endswith('.html'): continue
            rel = os.path.relpath(os.path.join(root, fn), '_site').replace(os.sep, '/')
            path = rel[:-len('index.html')] if fn == 'index.html' else rel
            url = NEW + '/' + path
            u = html.escape(url, quote=True)
            open(os.path.join(root, fn), 'w', encoding='utf-8').write(
                '<!doctype html><html><head><meta charset="utf-8"><title>Moved to honglifecalc.com</title>'
                f'<link rel="canonical" href="{u}"><meta http-equiv="refresh" content="0; url={u}">'
                f'<script>location.replace({url!r}+location.search+location.hash)</script></head>'
                f'<body><p>This page moved to <a href="{u}">{u}</a></p></body></html>\n')
            n += 1
print('redirect stubs:', n)

# --- remove pages that were dropped from the Korean site (tools/REMOVE.txt, one path per line) ---
if os.path.exists('tools/REMOVE.txt'):
    for line in open('tools/REMOVE.txt', encoding='utf-8'):
        rel = line.strip().lstrip('/')
        if not rel or rel.startswith('#') or '..' in rel: continue
        t = os.path.join('_site', rel)
        if os.path.isfile(t): os.remove(t)


# --- point Korean pages, sitemap and RSS at the new domain ---
import re, posixpath
OLD = 'https://honglife.co.kr'
FA = '|'.join(F)
abs_re = re.compile(r'https://honglife\.co\.kr/(' + FA + r')(?=[/"\'?#\s<]|$)')
attr_re = re.compile(r'((?:href|src)=")([^"]*)(")')
def fix(m, rd):
    pre, u, post = m.groups()
    if not u or u.startswith(('http:', 'https:', 'mailto:', 'data:', 'javascript:', '#', 'tel:', '//')): return m.group(0)
    path, _, frag = u.partition('#'); path, _, q = path.partition('?')
    r = path[1:] if path.startswith('/') else posixpath.normpath(posixpath.join(rd, path))
    if r.split('/')[0] not in F: return m.group(0)
    return pre + NEW + '/' + r + ('/' if path.endswith('/') else '') + ('?' + q if q else '') + ('#' + frag if frag else '') + post
k = 0
for root, dirs, files in (os.walk('_site') if ACTIVE else []):
    rel_root = os.path.relpath(root, '_site').replace(os.sep, '/')
    if rel_root.split('/')[0] in F: continue
    rd = '' if rel_root == '.' else rel_root
    for fn in files:
        if not fn.endswith('.html'): continue
        p = os.path.join(root, fn); s = open(p, encoding='utf-8', errors='surrogateescape').read(); o = s
        s = abs_re.sub(NEW + r'/\1', s)
        s = attr_re.sub(lambda m: fix(m, rd), s)
        if s != o: open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s); k += 1
print('korean pages relinked:', k)
sm = '_site/sitemap.xml'
if ACTIVE and os.path.exists(sm):
    s = open(sm, encoding='utf-8').read()
    s2 = re.sub(r'\s*<url><loc>https://honglife\.co\.kr/(?:' + FA + r')/[^<]*</loc>.*?</url>', '', s, flags=re.S)
    open(sm, 'w', encoding='utf-8').write(s2); print('sitemap urls:', s2.count('<url>'))
rs = '_site/rss.xml'
if ACTIVE and os.path.exists(rs):
    s = open(rs, encoding='utf-8').read(); open(rs, 'w', encoding='utf-8').write(abs_re.sub(NEW + r'/\1', s))
