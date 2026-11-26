"""색인 정리 (2026-11-26): 구글이 '발견됨 - 색인 안 됨'으로 남겨 둔 얇은 자동 생성 페이지에 noindex,follow.
- 대상: 아래 폴더의 개별 값 페이지(이모지 1개, 단위 1개 값, 도시 1곳 시간 등). 폴더 첫 화면(index.html)은 그대로.
- 사이트맵에 들어 있는 페이지는 건드리지 않음 (보강해서 색인을 노리는 페이지).
- 서치 콘솔 확인(2026-11-26): 이 폴더들의 색인된 페이지 0개, 사이트 전체 '발견됨-색인 안 됨' 5,453개의 대부분.
페이지는 그대로 열리고 링크도 따라가게 둬요 (사용자에게 바뀌는 것 없음). 사용: python3 build/patch_noindex_thin.py _site"""
import os, re, sys
root = sys.argv[1]
THIN = ['text/emoji', 'life/length', 'life/weight', 'life/temp', 'life/pyeong', 'life/volume', 'calendar/worldtime',
        'text/romanize', 'text/symbol', 'dev/color', 'dev/mime', 'dev/http', 'calendar/born', 'calendar/month', 'calendar/after']
sm = open(os.path.join(root, 'sitemap.xml'), encoding='utf-8').read()
insm = set(re.findall(r'<loc>https://honglife\.co\.kr(/[^<]*)</loc>', sm))
n = skip = 0
for d in THIN:
    dp = os.path.join(root, d)
    if not os.path.isdir(dp):
        continue
    for f in os.listdir(dp):
        if not f.endswith('.html') or f == 'index.html':
            continue
        url = '/' + d + '/' + f
        if url in insm:
            skip += 1; continue
        p = os.path.join(dp, f)
        s = open(p, encoding='utf-8').read()
        if re.search(r'<meta[^>]+name=["\']robots["\']', s, re.I):
            s2 = re.sub(r'(<meta[^>]+name=["\']robots["\'][^>]*content=["\'])[^"\']*', r'\1noindex,follow', s, count=1, flags=re.I)
        else:
            s2 = s.replace('<head>', '<head>\n<meta name="robots" content="noindex,follow">', 1)
        if s2 != s:
            open(p, 'w', encoding='utf-8').write(s2); n += 1
print('noindex thin pages:', n, 'kept (in sitemap):', skip)
