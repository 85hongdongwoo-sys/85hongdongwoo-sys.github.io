"""Fetch public-domain artworks (CC0) from the Art Institute of Chicago API for Muse Archive."""
import json, os, sys, time, urllib.request, urllib.parse
UA = {'AIC-User-Agent': 'muse-archive-fetch (personal art site)', 'User-Agent': 'muse-archive-fetch/1.0'}
FIELDS = 'id,title,artist_title,artist_display,date_display,date_start,image_id,classification_title,style_title,place_of_origin,medium_display,dimensions,credit_line,subject_titles,term_titles,color,is_boosted'
SETS = [('painting', 140), ('print', 60), ('drawing and watercolor', 30), ('textile', 20), ('book', 10)]
SIZE = os.environ.get('IMG', '600')

def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:
            print('retry', url, e, file=sys.stderr); time.sleep(2 + i * 3)
    return None

def search(cls, n):
    q = {'query': {'bool': {'must': [{'term': {'is_public_domain': True}}, {'exists': {'field': 'image_id'}},
                                      {'match': {'classification_title': cls}}],
                            'should': [{'term': {'is_boosted': True}}]}}}
    out, page = [], 1
    while len(out) < n and page < 20:
        url = 'https://api.artic.edu/api/v1/artworks/search?' + urllib.parse.urlencode(
            {'params': json.dumps(q), 'fields': FIELDS, 'limit': 100, 'page': page})
        raw = get(url)
        if not raw: break
        data = json.loads(raw).get('data', [])
        if not data: break
        out += [d for d in data if d.get('image_id')]
        page += 1; time.sleep(1)
    return out[:n]

os.makedirs('art/img', exist_ok=True)
seen, items = set(), []
for cls, n in SETS:
    for d in search(cls, n):
        if d['id'] in seen: continue
        seen.add(d['id'])
        f = f"art/img/{d['id']}.jpg"
        if not os.path.exists(f):
            b = get(f"https://www.artic.edu/iiif/2/{d['image_id']}/full/{SIZE},/0/default.jpg")
            if not b or len(b) < 2000: continue
            open(f, 'wb').write(b); time.sleep(0.4)
        d['set'] = cls
        items.append(d)
    print(cls, len(items), flush=True)
json.dump(items, open('art/aic.json', 'w'), ensure_ascii=False, indent=0)
print('total', len(items))
