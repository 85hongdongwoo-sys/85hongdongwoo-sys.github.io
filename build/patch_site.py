"""Overlay patch for honglife.co.kr: adds 입시·여행 to the top menu and the home page.
Runs in the deploy workflow after the tools bundle is unpacked into _site/."""
import os, sys, re
root = sys.argv[1] if len(sys.argv) > 1 else '_site'
OLD = '<a href="/design/">디자인</a>'
NEW = OLD + '<a href="/ipsi/" style="display:inline-flex;align-items:center">입시</a><a href="/trip/" style="display:inline-flex;align-items:center">여행</a>'
n = 0
for dp, dn, fn in os.walk(root):
    if os.path.relpath(dp, root).split(os.sep)[0] == 'trip':
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        s = open(p, encoding='utf-8').read()
        if OLD in s and 'href="/trip/" style=' not in s:
            open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1)); n += 1
print('menu patched:', n)

p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
reps = [
 ('<title>홍라이프 도구 | 엑셀 수식·양식, PDF·이미지 변환, 문서 만들기 무료 도구</title>',
  '<title>홍라이프 도구 | 엑셀 수식·양식, PDF·이미지 변환, 입시·여행까지 무료 도구</title>'),
 ('<meta name="description" content="말로 쓰면 엑셀 수식,',
  '<meta name="description" content="엑셀 수식·양식, PDF·이미지 변환에 정시 입시 계산과 출발확정 여행 패키지까지. 말로 쓰면 엑셀 수식,'),
 ('<a href="/ipsi/"><img src="/assets/art/cat2-ipsi.svg" alt="" width="64" height="64"><b>입시</b><em>3개</em></a>',
  '<a href="/ipsi/"><img src="/assets/art/cat2-ipsi.svg" alt="" width="64" height="64"><b>입시</b><em>3개</em></a>'
  '<a href="/trip/"><img src="/assets/art/cat2-trip.svg" alt="" width="64" height="64"><b>여행·패키지</b><em>NEW</em></a>'),
]
for a, b in reps:
    if a in s and b not in s:
        s = s.replace(a, b, 1); print('index:', a[:30])
open(p, 'w', encoding='utf-8').write(s)

p = os.path.join(root, 'sitemap.xml')
s = open(p, encoding='utf-8').read()
if 'honglife.co.kr/trip/' not in s:
    s = s.replace('<url><loc>https://honglife.co.kr/excel/</loc>',
                  '<url><loc>https://honglife.co.kr/trip/</loc><lastmod>2026-11-15</lastmod></url>\n<url><loc>https://honglife.co.kr/excel/</loc>', 1)
    open(p, 'w', encoding='utf-8').write(s); print('sitemap patched')
