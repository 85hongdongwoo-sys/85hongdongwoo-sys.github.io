"""SEO/GEO freshness: (1) sitemap <lastmod> for pages listed in build/lastmod.json (path -> YYYY-MM-DD),
(2) adds schema.org WebPage dateModified (= sitemap lastmod) to every sitemap page that has none.
Usage: python3 build/patch_datemod.py _site https://host"""
import json, os, re, sys
root, base = sys.argv[1], sys.argv[2].rstrip('/')
here = os.path.dirname(os.path.abspath(__file__))
LM = {}
p = os.path.join(here, 'lastmod.json')
if os.path.exists(p):
    LM = json.load(open(p, encoding='utf-8'))
smp = os.path.join(root, 'sitemap.xml')
s = open(smp, encoding='utf-8').read()
def fix(m):
    blk = m.group(0); loc = re.search(r'<loc>\s*([^<\s]+)', blk).group(1)
    d = LM.get(loc[len(base):] if loc.startswith(base) else loc)
    if d:
        blk = re.sub(r'<lastmod>[^<]*</lastmod>', f'<lastmod>{d}</lastmod>', blk) if '<lastmod>' in blk else blk.replace('</loc>', f'</loc><lastmod>{d}</lastmod>', 1)
    return blk
s = re.sub(r'<url>.*?</url>', fix, s, flags=re.S)
open(smp, 'w', encoding='utf-8').write(s)
n = 0
for loc, d in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>\s*<lastmod>([^<]+)</lastmod>', s):
    if not loc.startswith(base): continue
    path = loc[len(base):] or '/'
    f = os.path.join(root, path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    if not os.path.isfile(f): continue
    h = open(f, encoding='utf-8', errors='ignore').read()
    if '"dateModified"' in h or '</head>' not in h: continue
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": loc, "dateModified": d.strip()[:10]})
    open(f, 'w', encoding='utf-8').write(h.replace('</head>', f'<script type="application/ld+json">{ld}</script>\n</head>', 1)); n += 1
print('lastmod overrides', len(LM), 'dateModified added', n)
