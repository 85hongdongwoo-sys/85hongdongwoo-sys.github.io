"""Find artworks whose open-access originals are big enough for poster prints (A3/A2, 16x20, 18x24)."""
import json, os, sys, time, urllib.request
UA = {'AIC-User-Agent': 'arttrip-studio-fetch (personal art site)', 'User-Agent': 'arttrip-studio-fetch/1.0'}
def req(url, method='GET'):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA, method=method), timeout=120)
        return r, (r.read() if method == 'GET' else b'')
    except Exception as e:
        print('err', url[:90], e, file=sys.stderr); return None, b''
os.makedirs('big', exist_ok=True)
out = {'aic': [], 'cma': []}
# Chicago: test the IIIF server at 6000px for works whose originals are >= 6000px
aic = []  # Chicago's IIIF server caps public downloads at 3000px (403 above), checked 2026-11-26
for i, x in enumerate(aic):
    base = x['img'].split('/full/')[0]
    got = None
    for sz in ('!6000,6000', '!4000,4000', '!3000,3000'):
        r, b = req(f'{base}/full/{sz}/0/default.jpg')
        if r and len(b) > 50000:
            got = {'size': sz, 'bytes': len(b), 'cors': r.headers.get('Access-Control-Allow-Origin')}; break
    out['aic'].append({**{k: x[k] for k in ('id', 'title', 'artist', 'class', 'w', 'h')}, 'base': base, 'max': got})
    if i < 3 or i % 40 == 0: print('aic', i, got, file=sys.stderr)
    time.sleep(0.4)
# Cleveland: list painting/print image sizes from the API (print jpg and full tif)
for typ in ('Painting', 'Print', 'Drawing'):
    skip = 0
    while True:
        r, b = req(f'https://openaccess-api.clevelandart.org/api/artworks/?cc0=1&has_image=1&type={typ}&limit=1000&skip={skip}&fields=id,accession_number,title,creators,type,images')
        d = json.loads(b or b'{}').get('data', [])
        for x in d:
            im = x.get('images') or {}
            pr, fu = im.get('print') or {}, im.get('full') or {}
            out['cma'].append({'id': x['id'], 'acc': x.get('accession_number'), 'title': x.get('title'), 'artist': ((x.get('creators') or [{}])[0] or {}).get('description'),
                               'type': x.get('type'), 'print': [pr.get('url'), int(pr.get('width') or 0), int(pr.get('height') or 0)], 'full': [fu.get('url'), int(fu.get('width') or 0), int(fu.get('height') or 0), fu.get('filesize')]})
        print('cma', typ, skip, len(d), file=sys.stderr)
        if len(d) < 1000 or skip >= 9000: break
        skip += 1000
r, _ = req(out['cma'][0]['print'][0], 'HEAD') if out['cma'] else (None, b'')
out['cma_cors'] = r.headers.get('Access-Control-Allow-Origin') if r else None
json.dump(out, open('big/probe.json', 'w'), ensure_ascii=False)
ok = [a for a in out['aic'] if a['max'] and a['max']['size'] == '!6000,6000']
cbig = [c for c in out['cma'] if c['print'][1] and max(c['print'][1], c['print'][2]) >= 3400]
cfull = [c for c in out['cma'] if c['full'][1] and max(c['full'][1], c['full'][2]) >= 5000]
print('SUMMARY aic6000', len(ok), '/', len(out['aic']), 'cma print>=3400', len(cbig), 'cma full>=5000', len(cfull), 'of', len(out['cma']), 'cors', out['cma_cors'], file=sys.stderr)
