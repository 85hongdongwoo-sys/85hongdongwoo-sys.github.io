"""배포 마지막 단계: 모든 페이지에 사용 측정 스크립트(hl-track.js)와 '내 기기 통계 제외'(hl-notrack) 연결.
사용: python3 build/patch_track.py _site"""
import os, sys
root = sys.argv[1]
GA = "gtag('config','G-2PPV7NV8CP');"
GA2 = "try{if(localStorage.getItem('hl-notrack')==='1')window['ga-disable-G-2PPV7NV8CP']=true}catch(e){}" + GA
TAG = '<script src="/assets/js/hl-track.js?v=1" defer></script>'
k = g = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        try:
            s = open(p, encoding='utf-8').read()
        except Exception:
            continue
        if 'G-2PPV7NV8CP' not in s or '</head>' not in s:
            continue
        o = s
        if 'hl-notrack' not in s and GA in s:
            s = s.replace(GA, GA2, 1); g += 1
        if 'hl-track.js' not in s:
            s = s.replace('</head>', TAG + '</head>', 1); k += 1
        if s != o:
            open(p, 'w', encoding='utf-8').write(s)
print('track: script', k, 'notrack guard', g)
