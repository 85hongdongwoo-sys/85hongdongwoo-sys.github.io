"""페이지별 유사도 검사 (honglife.co.kr)
배포된 사이트(_site)의 sitemap.xml 에 있는 페이지만 대상으로, 본문 글자(머리말·메뉴·바닥글·스크립트 제외)를
단어 3개 묶음(shingle)으로 쪼개 MinHash(256)로 페이지끼리 겹치는 비율(자카드 유사도)을 추정한다.
결과: out/sim.json — 페이지마다 '가장 비슷한 페이지'와 그 비율, 50% 이상 겹치는 쌍 목록, 사이트 공통 문구 비율.
사용법: python3 build/sim/similarity.py _site out"""
import json, os, re, sys, time, hashlib
from html.parser import HTMLParser
import numpy as np

SITE, OUT = sys.argv[1], sys.argv[2]
BASE = 'https://honglife.co.kr'
SKIP_TAGS = {'script', 'style', 'noscript', 'svg', 'nav', 'header', 'footer', 'template', 'button', 'select', 'option'}


class Txt(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.parts = []; self.title = ''; self._t = False
    def handle_starttag(self, tag, a):
        if tag in SKIP_TAGS: self.skip += 1
        if tag == 'title': self._t = True
    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip: self.skip -= 1
        if tag == 'title': self._t = False
    def handle_data(self, d):
        if self._t: self.title += d
        elif not self.skip: self.parts.append(d)


def page_text(path):
    p = Txt()
    try: p.feed(open(path, encoding='utf-8', errors='ignore').read())
    except Exception: pass
    words = re.findall(r'[0-9A-Za-z가-힣]+', ' '.join(p.parts).lower())
    return p.title.strip(), words


# 1) sitemap 페이지
locs = []
for sm in ['sitemap.xml'] + [f for f in os.listdir(SITE) if f.startswith('sitemap') and f.endswith('.xml') and f != 'sitemap.xml']:
    fp = os.path.join(SITE, sm)
    if os.path.isfile(fp):
        locs += re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', open(fp, encoding='utf-8').read())
locs = [u for u in dict.fromkeys(locs) if u.startswith(BASE) and not u.endswith('.xml')]
pages = []
for u in locs:
    rel = u[len(BASE):].split('#')[0].split('?')[0].lstrip('/')
    fp = os.path.join(SITE, rel)
    if rel == '' or rel.endswith('/'): fp = os.path.join(SITE, rel, 'index.html')
    elif not os.path.splitext(rel)[1]: fp = fp + '.html' if os.path.isfile(fp + '.html') else os.path.join(fp, 'index.html')
    if os.path.isfile(fp): pages.append((u[len(BASE):] or '/', fp))
print('sitemap urls', len(locs), 'files found', len(pages))

# 2) 글자 추출 + 사이트 공통 문구(40% 넘는 페이지에 나오는 3단어 묶음) 표시
docs = []
df = {}
for url, fp in pages:
    title, w = page_text(fp)
    sh = {' '.join(w[i:i + 3]) for i in range(max(0, len(w) - 2))} or ({' '.join(w)} if w else set())
    docs.append((url, title, len(w), sh))
    for s in sh: df[s] = df.get(s, 0) + 1
N = len(docs)
common = {s for s, c in df.items() if c > 0.4 * N}
print('pages', N, 'boilerplate shingles', len(common))

# 3) MinHash (공통 문구 뺀 본문 기준)
K = 256
rng = np.random.default_rng(7)
A = rng.integers(1, (1 << 61) - 1, K, dtype=np.uint64); B = rng.integers(0, (1 << 61) - 1, K, dtype=np.uint64)
P = np.uint64((1 << 61) - 1)
sig = np.full((N, K), np.iinfo(np.uint64).max, dtype=np.uint64)
info = []
for i, (url, title, nw, sh) in enumerate(docs):
    own = sh - common
    info.append({'u': url, 't': title[:90], 'w': nw, 'own': len(own), 'boiler': round(100 * (len(sh) - len(own)) / max(1, len(sh)))})
    if not own: continue
    h = np.fromiter((int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') >> 3 for s in own), dtype=np.uint64)
    sig[i] = ((np.outer(h, A) + B) % P).min(axis=0)

# 4) 모든 쌍 비교 (덩어리로)
empty = np.array([x['own'] == 0 for x in info])
best = np.zeros(N); bestj = np.full(N, -1)
pairs = []
CH = 200
for s in range(0, N, CH):
    blk = sig[s:s + CH]
    eq = np.zeros((len(blk), N), dtype=np.float32)
    for k in range(K): eq += (blk[:, k][:, None] == sig[:, k][None, :])
    eq /= K
    for r in range(len(blk)):
        i = s + r
        eq[r, i] = 0
        if empty[i]: eq[r, :] = 0; continue
        eq[r, empty] = 0
        j = int(eq[r].argmax()); best[i] = eq[r, j]; bestj[i] = j
        for j2 in np.nonzero(eq[r] >= 0.5)[0]:
            if j2 > i: pairs.append((i, int(j2), round(float(eq[r, j2]), 3)))
    print('rows', min(N, s + CH), '/', N)
for i, x in enumerate(info):
    x['sim'] = round(float(best[i]) * 100); x['to'] = info[bestj[i]]['u'] if bestj[i] >= 0 else None
pairs.sort(key=lambda p: -p[2])
os.makedirs(OUT, exist_ok=True)
json.dump({'built': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'site': BASE, 'n': N,
           'method': '본문(메뉴·머리말·바닥글 제외)에서 사이트 공통 문구를 빼고, 단어 3개 묶음이 겹치는 비율(MinHash 256 추정)',
           'pages': info, 'pairs': [[info[i]['u'], info[j]['u'], v] for i, j, v in pairs[:20000]], 'npairs': len(pairs)},
          open(os.path.join(OUT, 'sim.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('done pairs>=50%', len(pairs))
