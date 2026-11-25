"""Niche sets of public-domain (CC0) 2D artworks from the Art Institute of Chicago, at print resolution.
Only paintings, prints and drawings whose title or subjects actually match the theme."""
import json, os, re, shutil, sys, time, urllib.request, urllib.parse
UA = {'AIC-User-Agent': 'muse-archive-fetch (personal art site)', 'User-Agent': 'muse-archive-fetch/1.0'}
FIELDS = 'id,title,artist_title,date_display,image_id,classification_title,medium_display,credit_line,subject_titles,term_titles,thumbnail'
NICHES = {  # search text, words that must appear in title/subjects
  'flowers':   ('flowers', ['flower', 'bouquet', 'rose', 'peon', 'lil', 'iris', 'tulip', 'chrysanthemum', 'blossom', 'floral']),
  'cats':      ('cat', [r'\bcats?\b', 'kitten']),
  'birds':     ('bird', ['bird', 'crane', 'heron', 'owl', 'swallow', 'sparrow', 'rooster', 'duck', 'egret', 'parrot', 'hawk', 'pheasant']),
  'sea':       ('sea coast', [r'\bsea\b', 'seascape', 'coast', 'beach', 'wave', 'harbor', 'ocean', 'marine', 'boats?']),
  'ukiyoe':    ('Hiroshige Hokusai', ['hiroshige', 'hokusai', 'kuniyoshi', 'hasui']),
  'botanical': ('botanical', ['botan', 'plant', 'leaf', 'leaves', 'fern', 'specimen', 'herb']),
  'mountains': ('mountain', ['mountain', r'\bmount\b', 'alps', 'peak', 'fuji']),
  'winter':    ('snow winter', ['snow', 'winter', r'\bice\b', 'frost']),
  'fruit':     ('fruit still life', ['fruit', 'apple', 'grape', 'peach', 'pear', 'cherr', 'lemon', 'orange', 'melon', 'plum']),
  'horses':    ('horse', ['horse', 'races', 'jockey', 'equestrian', 'pony']),
}
OK_CLASS = ('painting', 'print', 'drawing', 'watercolor', 'woodblock')
PER = int(os.environ.get('PER', '12'))

def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except Exception as e:
            print('retry', url[:120], e, file=sys.stderr); time.sleep(2 + i * 3)
    return None

def search(q, page):
    p = {'query': {'bool': {'must': [{'term': {'is_public_domain': True}}, {'exists': {'field': 'image_id'}}]}}}
    url = 'https://api.artic.edu/api/v1/artworks/search?' + urllib.parse.urlencode(
        {'q': q, 'params': json.dumps(p), 'fields': FIELDS, 'limit': 100, 'page': page})
    raw = get(url)
    return json.loads(raw).get('data', []) if raw else []

def fits(d, words):
    cl = (d.get('classification_title') or '').lower()
    if not any(c in cl for c in OK_CLASS): return False
    text = ' '.join([d.get('title') or ''] + (d.get('subject_titles') or [])).lower()
    return any(re.search(w, text) for w in words)

if os.environ.get('FRESH'): shutil.rmtree('hires', ignore_errors=True)
os.makedirs('hires', exist_ok=True)
meta = {}
for niche, (q, words) in NICHES.items():
    got = 0
    for page in (1, 2, 3):
        for d in search(q, page):
            if got >= PER: break
            k = str(d['id'])
            if k in meta or not d.get('image_id') or not fits(d, words): continue
            th = d.get('thumbnail') or {}
            if th.get('width') and th.get('height') and max(th['width'], th['height']) < 1800: continue
            b = None
            for w in ('3000', '2400', '1686'):
                b = get(f"https://www.artic.edu/iiif/2/{d['image_id']}/full/{w},/0/default.jpg", tries=1)
                if b and len(b) > 50000: break
                b = None
            if not b: continue
            open(f'hires/{k}.jpg', 'wb').write(b)
            d.pop('thumbnail', None); d['niche'] = niche; meta[k] = d; got += 1
            time.sleep(0.4)
        if got >= PER: break
        time.sleep(1)
    print(niche, got, flush=True)
json.dump(meta, open('hires/niche.json', 'w'), ensure_ascii=False, indent=0)
print('total', len(meta))
