"""Niche sets of public-domain (CC0) artworks from the Art Institute of Chicago, at print resolution."""
import json, os, sys, time, urllib.request, urllib.parse
UA = {'AIC-User-Agent': 'muse-archive-fetch (personal art site)', 'User-Agent': 'muse-archive-fetch/1.0'}
FIELDS = 'id,title,artist_title,artist_display,date_display,date_start,image_id,classification_title,medium_display,credit_line,subject_titles,thumbnail'
NICHES = {
  'flowers':   'flowers bouquet',
  'cats':      'cat',
  'birds':     'birds',
  'sea':       'sea waves boats',
  'ukiyoe':    'Hokusai Hiroshige woodblock',
  'botanical': 'botanical plant',
  'mountains': 'mountains landscape',
  'winter':    'snow winter',
  'fruit':     'fruit still life',
  'horses':    'horse',
}
PER = int(os.environ.get('PER', '12'))

def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except Exception as e:
            print('retry', url[:120], e, file=sys.stderr); time.sleep(2 + i * 3)
    return None

def search(q, n):
    p = {'query': {'bool': {'must': [{'term': {'is_public_domain': True}}, {'exists': {'field': 'image_id'}}]}}}
    url = 'https://api.artic.edu/api/v1/artworks/search?' + urllib.parse.urlencode(
        {'q': q, 'params': json.dumps(p), 'fields': FIELDS, 'limit': 60})
    raw = get(url)
    return [d for d in json.loads(raw).get('data', []) if d.get('image_id')] if raw else []

os.makedirs('hires', exist_ok=True)
meta = json.load(open('hires/niche.json')) if os.path.exists('hires/niche.json') else {}
for niche, q in NICHES.items():
    got = [x for x in meta.values() if x['niche'] == niche]
    for d in search(q, PER * 3):
        if len(got) >= PER: break
        k = str(d['id'])
        if k in meta: continue
        th = d.get('thumbnail') or {}
        if th.get('width') and th.get('height') and max(th['width'], th['height']) < 1800: continue
        b = None
        for w in ('3000', '2400', '1686'):
            b = get(f"https://www.artic.edu/iiif/2/{d['image_id']}/full/{w},/0/default.jpg", tries=1)
            if b and len(b) > 50000: break
            b = None
        if not b: continue
        open(f'hires/{k}.jpg', 'wb').write(b)
        d.pop('thumbnail', None); d['niche'] = niche; meta[k] = d; got.append(d)
        time.sleep(0.5)
    print(niche, len(got), flush=True)
json.dump(meta, open('hires/niche.json', 'w'), ensure_ascii=False, indent=0)
print('total', len(meta))
