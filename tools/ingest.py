"""Build D1 seed SQL from artwork JSON + Korean translations + colour palettes."""
import json, re, unicodedata, numpy as np
from PIL import Image
from sklearn.cluster import KMeans
A = json.load(open('data/artworks_en.json')); KA = json.load(open('data/ko_artists.json')); KT = json.load(open('data/ko_titles.json'))
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:60] or 'artwork'
def pal(path, k=5):
    im = Image.open(path).convert('RGB').resize((96, 96)); a = np.array(im).reshape(-1, 3).astype(float)
    km = KMeans(k, n_init=3, random_state=1).fit(a); n = np.bincount(km.labels_)
    return ['#%02x%02x%02x' % tuple(int(v) for v in km.cluster_centers_[i]) for i in np.argsort(-n)]
THEME_BY_SUB = [('flowers', r'flower|bouquet|rose|lil|iris|blossom|floral|chrysanthemum|peony'), ('sea', r'\bsea|coast|beach|harbor|ocean|boat|wave|marine'),
    ('landscapes', r'landscape|mountain|river|valley|field|forest|tree'), ('cats', r'\bcats?\b'), ('birds', r'bird|heron|crane|owl|hawk|duck'),
    ('horses', r'horse|equestrian'), ('winter', r'snow|winter|ice'), ('still-life', r'still life|fruit|apple|grape'), ('portraits', r'portrait|mrs\.|madame|self-portrait'),
    ('japanese-prints', r'hokusai|hiroshige|utamaro|harunobu|kiyonobu|shunsho|koryusai|sharaku|sekka|gakutei|moronobu|shigemasa|dohan|kiyomasu|shun.ei'), ('textiles', r'fragment|textile|fabric|panel|hanging|robe|kesa|chasuble|cravat|tassels')]
rows = []; seen = set(); missing = []
for o in A:
    text = ' '.join([o['short'], o['artist'], o.get('kind') or '', ' '.join(o.get('sub') or []), o.get('medium') or '']).lower()
    th = o.get('theme')
    if not th:
        for t, rx in THEME_BY_SUB:
            if re.search(rx, text): th = t; break
    th = 'flowers' if th == 'botanical' else (th or 'masterpieces')
    s = slug(o['short']); base = s; i = 2
    while s in seen: s = f'{base}-{i}'; i += 1
    seen.add(s)
    if o['id'] not in KT: missing.append(o['id'])
    rows.append(dict(id=o['id'], slug=s, title=o['short'], title_ko=KT.get(o['id'], ''), artist=o['artist'], artist_ko=KA.get(o['artist'], o['artist']),
        artist_slug=slug(o['artist']), date=o.get('date') or '', medium=o.get('medium') or '', credit=o.get('credit') or '', kind=o.get('kind') or '',
        theme=th, w=o['w'], h=o['h'], palette=json.dumps(pal(f"public/img/{o['id']}.jpg"))))
def q(v): return 'NULL' if v is None else (str(v) if isinstance(v, (int, float)) else "'" + str(v).replace("'", "''") + "'")
cols = list(rows[0].keys())
with open('data/seed.sql', 'w') as f:
    f.write('DELETE FROM artworks;\n')
    for r in rows: f.write(f"INSERT INTO artworks ({','.join(cols)}) VALUES ({','.join(q(r[c]) for c in cols)});\n")
import collections
print(len(rows), 'missing ko titles:', missing[:20], len(missing)); print(collections.Counter(r['theme'] for r in rows))
