import pool_a, pool_b, pool_c, pool_d, pool_e
POOL = {}
for m in (pool_a, pool_b, pool_c, pool_d, pool_e):
    for slug, dd in m.P.items():
        L = POOL.setdefault(slug, [])
        for dim, txt in dd.items():
            for ln in txt.strip().split('\n'):
                ln = ln.strip()
                if not ln: continue
                rev = 1 if ln.startswith('!') else 0
                L.append((ln.lstrip('!').strip(), dim, rev))

def build(t, extra, n=160):
    """기존 문항 우선 + 풀 문항, 차원별 라운드로빈 순서로 n개. 앞 40개가 간편 세트."""
    base = list(t['q']) + list(extra)
    if t['kind'] == 'phq9':
        return base
    seen = set(); items = []
    for x in base + POOL.get(t['slug'], []):
        x = tuple(x)
        if x[0] in seen: continue
        seen.add(x[0]); items.append(x)
    keyf = (lambda x: x[2]) if len({x[1] for x in items}) == 1 else (lambda x: x[1])
    groups = {}
    for x in items: groups.setdefault(keyf(x), []).append(x)
    ks = list(groups); out = []; i = 0
    while len(out) < n and any(groups.values()):
        k = ks[i % len(ks)]; i += 1
        if groups[k]: out.append(groups[k].pop(0))
    return out
