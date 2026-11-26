"""Catalogue of public-domain (CC0) paintings and prints with print-size image URLs from three open museum APIs.
Writes more/met.json, more/cma.json, more/aic.json (metadata + image URLs, no images)."""
import json, os, sys, time, urllib.request, urllib.parse
UA = {'User-Agent': 'arttrip-studio-catalogue/1.0 (personal art site)', 'AIC-User-Agent': 'arttrip-studio-catalogue'}
def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r: return json.loads(r.read())
        except Exception as e: print('retry', url[:90], e, file=sys.stderr); time.sleep(1.5 + 2 * i)
os.makedirs('more', exist_ok=True)
LIMIT = int(os.environ.get('LIMIT', '2500'))
# --- The Met ---
met = []
for dept, q in ((11, '*'), (6, 'woodblock'), (9, 'print'), (1, 'painting'), (21, 'painting')):
    s = get(f'https://collectionapi.metmuseum.org/public/collection/v1/search?isPublicDomain=true&hasImages=true&departmentId={dept}&q={q}') or {}
    ids = (s.get('objectIDs') or [])[: LIMIT]
    for oid in ids:
        if len(met) >= LIMIT * 2: break
        o = get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}')
        time.sleep(0.03)
        if not o or not o.get('isPublicDomain') or not o.get('primaryImage'): continue
        cl = (o.get('classification') or '').lower()
        if not any(k in cl for k in ('painting', 'print', 'drawing', 'watercolor', 'pastel')): continue
        met.append({'src': 'met', 'id': str(o['objectID']), 'title': o.get('title'), 'artist': o.get('artistDisplayName'), 'date': o.get('objectDate'), 'medium': o.get('medium'),
                    'class': o.get('classification'), 'culture': o.get('culture'), 'dept': o.get('department'), 'img': o.get('primaryImage'), 'thumb': o.get('primaryImageSmall'), 'url': o.get('objectURL')})
    print('met', dept, len(met), file=sys.stderr)
json.dump(met, open('more/met.json', 'w'), ensure_ascii=False)
# --- Cleveland Museum of Art ---
cma = []
for typ in ('Painting', 'Print', 'Drawing'):
    skip = 0
    while skip < LIMIT:
        d = get('https://openaccess-api.clevelandart.org/api/artworks/?' + urllib.parse.urlencode({'cc0': 1, 'has_image': 1, 'type': typ, 'limit': 500, 'skip': skip, 'fields': 'id,title,creators,creation_date,technique,type,culture,images,url'})) or {}
        rows = d.get('data') or []
        for r in rows:
            im = r.get('images') or {}
            big = (im.get('print') or im.get('full') or im.get('web') or {}).get('url')
            if not big: continue
            cr = r.get('creators') or []
            cma.append({'src': 'cma', 'id': str(r['id']), 'title': r.get('title'), 'artist': (cr[0].get('description') if cr else '') or '', 'date': r.get('creation_date'), 'medium': r.get('technique'),
                        'class': r.get('type'), 'culture': (r.get('culture') or [''])[0] if isinstance(r.get('culture'), list) else r.get('culture'), 'img': big, 'thumb': (im.get('web') or {}).get('url'), 'url': r.get('url')})
        if len(rows) < 500: break
        skip += 500
    print('cma', typ, len(cma), file=sys.stderr)
json.dump(cma, open('more/cma.json', 'w'), ensure_ascii=False)
# --- Art Institute of Chicago ---
aic = []
for cls in ('painting', 'print', 'drawing and watercolor'):
    for page in range(1, 11):
        p = {'query': {'bool': {'must': [{'term': {'is_public_domain': True}}, {'exists': {'field': 'image_id'}}, {'match': {'classification_title': cls}}]}}, 'sort': [{'is_boosted': 'desc'}]}
        d = get('https://api.artic.edu/api/v1/artworks/search?' + urllib.parse.urlencode({'params': json.dumps(p), 'fields': 'id,title,artist_title,date_display,medium_display,classification_title,image_id,thumbnail,place_of_origin', 'limit': 100, 'page': page})) or {}
        rows = d.get('data') or []
        for r in rows:
            aic.append({'src': 'aic', 'id': str(r['id']), 'title': r.get('title'), 'artist': r.get('artist_title'), 'date': r.get('date_display'), 'medium': r.get('medium_display'), 'class': r.get('classification_title'), 'culture': r.get('place_of_origin'),
                        'img': f"https://www.artic.edu/iiif/2/{r['image_id']}/full/!3000,3000/0/default.jpg", 'thumb': f"https://www.artic.edu/iiif/2/{r['image_id']}/full/600,/0/default.jpg", 'w': (r.get('thumbnail') or {}).get('width'), 'h': (r.get('thumbnail') or {}).get('height')})
        if len(rows) < 100: break
    print('aic', cls, len(aic), file=sys.stderr)
json.dump(aic, open('more/aic.json', 'w'), ensure_ascii=False)
print('total', len(met), len(cma), len(aic), file=sys.stderr)
