"""Per-artist sets of public-domain (CC0) works from the Art Institute of Chicago at print size, for artist calendars.
Paintings first (most-viewed first), then prints and drawings, until 16 per artist."""
import json, os, re, sys, time, urllib.request, urllib.parse
UA = {'AIC-User-Agent': 'arttrip-studio-fetch (personal art site)', 'User-Agent': 'arttrip-studio-fetch/1.0'}
FIELDS = 'id,title,artist_title,date_display,image_id,classification_title,medium_display,credit_line,thumbnail,is_boosted'
ARTISTS = ['Claude Monet', 'Édouard Manet', 'Edgar Degas', 'Pierre-Auguste Renoir', 'Paul Cezanne', 'Vincent van Gogh',
           'Georges Seurat', 'Camille Pissarro', 'Gustave Caillebotte', 'Mary Cassatt', 'Berthe Morisot', 'Paul Gauguin',
           'Henri de Toulouse-Lautrec', 'Alfred Sisley', 'Odilon Redon', 'Katsushika Hokusai', 'Utagawa Hiroshige',
           'Kitagawa Utamaro', 'Winslow Homer', 'James McNeill Whistler', 'John Singer Sargent', 'Gustave Courbet']
PER = int(os.environ.get('PER', '16'))
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower().replace('é', 'e')).strip('-')

def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r: return r.read()
        except Exception as e: print('retry', url[:110], e, file=sys.stderr); time.sleep(2 + 3 * i)
    return None

def search(artist, page):
    p = {'query': {'bool': {'must': [{'term': {'is_public_domain': True}}, {'exists': {'field': 'image_id'}},
                                     {'match_phrase': {'artist_title': artist}}]}}}
    raw = get('https://api.artic.edu/api/v1/artworks/search?' + urllib.parse.urlencode({'params': json.dumps(p), 'fields': FIELDS, 'limit': 100, 'page': page}))
    return json.loads(raw).get('data', []) if raw else []

os.makedirs('artists', exist_ok=True)
meta = {}
for artist in ARTISTS:
    rows = []
    for page in (1, 2, 3):
        got = search(artist, page)
        rows += got
        if len(got) < 100: break
    rows = [r for r in rows if (r.get('artist_title') or '').lower().replace('é', 'e') .startswith(artist.lower().replace('é', 'e')[:8])]
    def rank(r):
        cl = (r.get('classification_title') or '').lower(); t = r.get('thumbnail') or {}
        w, h = t.get('width') or 1, t.get('height') or 1
        return (0 if 'painting' in cl else 1 if ('print' in cl or 'woodblock' in cl or 'pastel' in cl or 'watercolor' in cl) else 2, 0 if r.get('is_boosted') else 1, 0 if w >= h else 1)
    rows.sort(key=rank)
    sl = slug(artist); os.makedirs(f'artists/{sl}', exist_ok=True); meta[sl] = {'artist': artist, 'works': []}
    for r in rows:
        if len(meta[sl]['works']) >= PER: break
        if 'sculpture' in (r.get('classification_title') or '').lower(): continue
        img = get(f"https://www.artic.edu/iiif/2/{r['image_id']}/full/3000,/0/default.jpg") or get(f"https://www.artic.edu/iiif/2/{r['image_id']}/full/1686,/0/default.jpg")
        if not img or len(img) < 50000: continue
        n = len(meta[sl]['works']); open(f'artists/{sl}/{n:02d}.jpg', 'wb').write(img)
        meta[sl]['works'].append({k: r.get(k) for k in ('id', 'title', 'date_display', 'classification_title', 'medium_display', 'credit_line')} | {'file': f'{n:02d}.jpg'})
        time.sleep(0.4)
    print(artist, len(meta[sl]['works']), file=sys.stderr)
json.dump(meta, open('artists/meta.json', 'w'), ensure_ascii=False, indent=1)
