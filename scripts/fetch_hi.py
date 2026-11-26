"""Print-size (2400px long edge) copies of the site's artworks, for the editor's 300 dpi exports."""
import json, os, sys, time, urllib.request
UA = {'AIC-User-Agent': 'arttrip-studio-fetch (personal art site)', 'User-Agent': 'arttrip-studio-fetch/1.0'}
def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r: return r.read()
        except Exception as e: print('retry', url[:100], e, file=sys.stderr); time.sleep(2 + 3 * i)
ids = [l.strip() for l in open('scripts/hi_ids.txt') if l.strip()]
os.makedirs('hi', exist_ok=True)
done = 0
for i in range(0, len(ids), 50):
    chunk = ids[i:i + 50]
    raw = get('https://api.artic.edu/api/v1/artworks?ids=' + ','.join(chunk) + '&fields=id,image_id&limit=50')
    for r in json.loads(raw).get('data', []) if raw else []:
        p = f"hi/{r['id']}.jpg"
        if os.path.exists(p) or not r.get('image_id'): continue
        img = get(f"https://www.artic.edu/iiif/2/{r['image_id']}/full/!2400,2400/0/default.jpg") or get(f"https://www.artic.edu/iiif/2/{r['image_id']}/full/1686,/0/default.jpg")
        if img and len(img) > 30000: open(p, 'wb').write(img); done += 1
        time.sleep(0.3)
print('hi', done, file=sys.stderr)
